#!/usr/bin/env python3
"""Turn a CSV of tagged notes into: a theme table (DISTINCT participants, not mentions),
grouping by group/tag and a priority table.

Usage:
  python3 analyze_notes.py notes.csv [--total-participants N] [--format md|csv]
                           [--min-participants 1] [--separator ";"] [--output file]
                           [--pattern-rule three|third|both] [--threshold-table]
                           [--lang en|es]

CSV columns (case-insensitive headers; only the first 3 are required):
  note          text of the observation/quote (one idea per row)        [alias: nota]
  participant   ID (P1, P2...). Counts how many DISTINCT IDs mention each tag   [alias: participante]
  tags          one or more codes separated by ';' (e.g. "payment;trust")
  group         (optional) affinity cluster already assigned             [alias: grupo]
  type          (optional) attitude | behavior                           [alias: tipo]
  severity      (optional) 1 = annoyance, 2 = hinders, 3 = blocks the task/goal   [alias: severidad]
  effort        (optional) 1 = low, 2 = medium, 3 = high (estimated with the team) [alias: esfuerzo]
  method        (optional) interview | survey | usability | analytics ... If present, adds the
                topic x method matrix and flags themes found in a single method.   [alias: metodo]

Pattern threshold (optional, see references/pattern-threshold.md): --pattern-rule three flags themes
with >= 3 distinct participants; third flags those reaching 1/3 of the total (rounded up); both
requires both. These are practical rules from different sources, not statistical criteria.
--threshold-table prints thresholds for several N and exits (no CSV needed).

Priority (editable heuristic, NOT a standard): score = (n/N) * max_severity / mean_effort.
It orders the discussion with the team; it does not decide on its own. Without severity/effort
1 is assumed. A theme with severity 3 and few participants is flagged "review even if minority".

Exit codes: 0 ok; 1 input error (missing file, missing columns, empty input, bad N); 2 usage error (bad flags).
"""
import argparse, csv, io, sys
from collections import defaultdict

ALIASES = {  # Spanish header -> canonical English header
    "nota": "note", "participante": "participant", "grupo": "group", "tipo": "type",
    "severidad": "severity", "esfuerzo": "effort", "metodo": "method", "método": "method",
}
RULE_ALIASES = {"tres": "three", "tercio": "third", "ambas": "both"}

T = {
    "en": {
        "err_open": "ERROR: could not open '{p}': {e}",
        "err_cols": "ERROR: missing required columns: {m} (headers found: {f}). Use note, participant, tags (Spanish nota, participante, tags also work).",
        "none": "none",
        "warn_row": "WARNING row {i}: missing note or participant, ignored",
        "warn_tags": "WARNING row {i}: note without tags (goes to 'uncoded')",
        "uncoded": "uncoded",
        "warn_num": "WARNING: non-numeric value '{v}' in severity/effort, using {d}",
        "err_empty": "ERROR: the CSV has no valid rows (check that 'note' and 'participant' are not empty)",
        "err_total": "ERROR: --total-participants must be >= 1",
        "err_write": "ERROR: could not write '{p}': {e}",
        "err_nocsv": "the CSV file is missing (required unless --threshold-table)",
        "err_decode": "ERROR: '{p}' is not valid UTF-8 text",
        "th_head": ["N participants", "3 independent mentions", "One third (rounded up)", "Stricter rule"],
        "th_foot": "Practical rules from different sources (see references/pattern-threshold.md); not statistical thresholds.",
        "h_summary": "# Coding summary ({n} notes, {t} participants)\n",
        "h_themes": "## Themes by distinct participants\n",
        "c_tag": "Tag", "c_parts": "Participants (n of N)", "c_mentions": "Mentions", "c_type": "Type",
        "c_quote": "Quote (check)", "c_pattern": "Pattern ({r})", "yes": "yes", "no": "no",
        "h_prio": "\n## Priority table (heuristic: frequency x severity / effort)\n",
        "c_freq": "Frequency", "c_sev": "Max severity", "c_eff": "Mean effort", "c_score": "Score", "c_note": "Note",
        "flag": "review even if minority",
        "h_matrix": "\n## Topic x method matrix (distinct participants per cell)\n",
        "c_methods": "Methods", "single": "single method: treat as a hypothesis to contrast",
        "matrix_foot": "\nA theme found in one method is not discarded: label it and plan how to contrast it (references/triangulation-across-methods.md).",
        "h_groups": "\n## Grouping by group/tag (for Miro/FigJam)\n",
        "g_title": "### {g} ({k} participants)",
        "reminder": "Reminder: the score orders the conversation; validate codes with a second person and look for disconfirming evidence.",
        "csv_head": ["tag", "participants_n", "total", "mentions", "type", "max_severity", "mean_effort", "score", "note", "participants", "pattern"],
        "csv_yes": "yes", "csv_no": "no",
        "d_csv": "notes CSV (required unless --threshold-table)",
        "d_total": "total N (default: distinct IDs in the CSV)",
        "d_min": "hide themes with fewer distinct participants",
        "d_sep": "tag separator inside the tags column",
        "d_out": "write the result to this file instead of stdout",
        "d_rule": "flag themes meeting the rule: three (>=3 participants), third (>=1/3 of total) or both",
        "d_thr": "print thresholds by N and exit",
        "d_lang": "language of the output labels",
    },
    "es": {
        "err_open": "ERROR: no pude abrir '{p}': {e}",
        "err_cols": "ERROR: faltan columnas obligatorias: {m} (encabezados encontrados: {f}). Usa note, participant, tags (o nota, participante, tags).",
        "none": "ninguno",
        "warn_row": "AVISO fila {i}: sin nota o participante, se ignora",
        "warn_tags": "AVISO fila {i}: nota sin tags (queda en 'sin-codigo')",
        "uncoded": "sin-codigo",
        "warn_num": "AVISO: valor no numerico '{v}' en severidad/esfuerzo, se usa {d}",
        "err_empty": "ERROR: el CSV no tiene filas validas (revisa que 'nota' y 'participante' no esten vacias)",
        "err_total": "ERROR: --total-participants debe ser >= 1",
        "err_write": "ERROR: no pude escribir '{p}': {e}",
        "err_nocsv": "falta el archivo CSV (obligatorio salvo con --threshold-table)",
        "err_decode": "ERROR: '{p}' no es texto UTF-8 valido",
        "th_head": ["N participantes", "3 menciones independientes", "Un tercio (redondeo arriba)", "Regla mas exigente"],
        "th_foot": "Reglas practicas de distintas fuentes (ver references/pattern-threshold.md); no son umbrales estadisticos.",
        "h_summary": "# Resumen de codificacion ({n} notas, {t} participantes)\n",
        "h_themes": "## Temas por participantes distintos\n",
        "c_tag": "Tag", "c_parts": "Participantes (n de N)", "c_mentions": "Menciones", "c_type": "Tipo",
        "c_quote": "Cita (revisar)", "c_pattern": "Patron ({r})", "yes": "si", "no": "no",
        "h_prio": "\n## Tabla de prioridades (heuristica: frecuencia x severidad / esfuerzo)\n",
        "c_freq": "Frecuencia", "c_sev": "Severidad max", "c_eff": "Esfuerzo medio", "c_score": "Puntaje", "c_note": "Nota",
        "flag": "revisar aunque sea minoritario",
        "h_matrix": "\n## Matriz tema x metodo (participantes distintos por celda)\n",
        "c_methods": "Metodos", "single": "un solo metodo: tratar como hipotesis a contrastar",
        "matrix_foot": "\nUn tema en un solo metodo no se descarta: se etiqueta y se planea como contrastarlo (references/triangulation-across-methods.md).",
        "h_groups": "\n## Agrupacion por grupo/tag (para Miro/FigJam)\n",
        "g_title": "### {g} ({k} participantes)",
        "reminder": "Recordatorio: el puntaje ordena la conversacion; validar codigos con una segunda persona y buscar evidencia en contra.",
        "csv_head": ["tag", "participantes_n", "total", "menciones", "tipo", "severidad_max", "esfuerzo_medio", "puntaje", "nota", "participantes", "patron"],
        "csv_yes": "si", "csv_no": "no",
        "d_csv": "CSV de notas (obligatorio salvo con --threshold-table)",
        "d_total": "N total (default: IDs distintos en el CSV)",
        "d_min": "oculta temas con menos participantes distintos",
        "d_sep": "separador de tags dentro de la columna tags",
        "d_out": "escribe el resultado en este archivo en vez de stdout",
        "d_rule": "marca temas que cumplen la regla: three (>=3 participantes), third (>=1/3 del total) o both",
        "d_thr": "imprime los umbrales por N y termina",
        "d_lang": "idioma de las etiquetas de salida",
    },
}


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def read_rows(path, sep, L):
    try:
        f = open(path, newline="", encoding="utf-8-sig")
    except OSError as e:
        die(L["err_open"].format(p=path, e=e.strerror or e))
    with f:
        try:
            rd = csv.DictReader(f)
            rd.fieldnames = [ALIASES.get(h.strip().lower(), h.strip().lower()) for h in (rd.fieldnames or [])]
            missing = {"note", "participant", "tags"} - set(rd.fieldnames)
            if missing:
                die(L["err_cols"].format(m=", ".join(sorted(missing)), f=", ".join(rd.fieldnames) or L["none"]))
            rows = []
            for i, r in enumerate(rd, start=2):
                r = {k: (v or "").strip() for k, v in r.items() if k}
                tags = [t.strip().lower() for t in r["tags"].split(sep) if t.strip()]
                if not r["note"] or not r["participant"]:
                    print(L["warn_row"].format(i=i), file=sys.stderr)
                    continue
                if not tags:
                    print(L["warn_tags"].format(i=i), file=sys.stderr)
                    tags = [L["uncoded"]]
                r["_tags"] = tags
                rows.append(r)
        except UnicodeDecodeError:
            die(L["err_decode"].format(p=path))
        except csv.Error as e:
            die("ERROR: CSV: %s" % e)
    return rows


def num(v, d, L):
    try:
        return float(v)
    except ValueError:
        print(L["warn_num"].format(v=v, d=d), file=sys.stderr)
        return d


def third_threshold(total):
    """One third of the total, rounded up (practical rule, not statistical)."""
    return -(-total // 3)


def meets(n, total, rule):
    if not rule:
        return None
    three = n >= 3
    third = n >= third_threshold(total)
    return {"three": three, "third": third, "both": three and third}[rule]


def threshold_table(L):
    h = L["th_head"]
    o = ["| " + " | ".join(h) + " |", "|---|---|---|---|"]
    for n in (5, 6, 8, 10, 12, 15, 20, 30):
        t = third_threshold(n)
        o.append(f"| {n} | 3 | {t} | {max(3, t)} |")
    o.append("\n" + L["th_foot"])
    return "\n".join(o)


def analyze(rows, total, rule, L):
    by_tag = defaultdict(lambda: {"parts": set(), "notes": [], "sev": [], "eff": [], "types": set(),
                                  "groups": set(), "methods": defaultdict(set)})
    for r in rows:
        for t in r["_tags"]:
            d = by_tag[t]
            d["parts"].add(r["participant"])
            d["notes"].append((r["participant"], r["note"]))
            if r.get("severity"): d["sev"].append(num(r["severity"], 1, L))
            if r.get("effort"): d["eff"].append(num(r["effort"], 1, L))
            if r.get("type"): d["types"].add(r["type"].lower())
            if r.get("group"): d["groups"].add(r["group"])
            if r.get("method"): d["methods"][r["method"].lower()].add(r["participant"])
    themes = []
    for t, d in by_tag.items():
        n = len(d["parts"])
        sev = max(d["sev"]) if d["sev"] else 1
        eff = sum(d["eff"]) / len(d["eff"]) if d["eff"] else 1
        score = round((n / total) * sev / max(eff, 0.01), 2)
        quote = max(d["notes"], key=lambda x: len(x[1]))  # longest note: usually the most informative; check by hand
        flag = L["flag"] if sev >= 3 and n / total < 0.5 else ""
        themes.append({"tag": t, "n": n, "total": total, "mentions": len(d["notes"]), "sev": sev,
                       "eff": round(eff, 1), "score": score, "quote": quote, "types": "/".join(sorted(d["types"])),
                       "groups": ", ".join(sorted(d["groups"])), "participants": ", ".join(sorted(d["parts"])),
                       "flag": flag, "pattern": meets(n, total, rule),
                       "methods": {m: len(p) for m, p in d["methods"].items()}})
    themes.sort(key=lambda x: (-x["score"], -x["n"], x["tag"]))
    return themes


def render_md(themes, rows, total, minp, rule, L):
    o = [L["h_summary"].format(n=len(rows), t=total), L["h_themes"]]
    ph = f" {L['c_pattern'].format(r=rule)} |" if rule else ""
    o.append(f"| {L['c_tag']} | {L['c_parts']} | {L['c_mentions']} | {L['c_type']} | {L['c_quote']} |" + ph)
    o.append("|---|---|---|---|---|" + ("---|" if rule else ""))
    for t in sorted(themes, key=lambda x: (-x["n"], x["tag"])):
        if t["n"] < minp: continue
        pc = f" {L['yes'] if t['pattern'] else L['no']} |" if rule else ""
        o.append(f"| {t['tag']} | {t['n']}/{t['total']} | {t['mentions']} | {t['types'] or '-'} | \"{t['quote'][1]}\" ({t['quote'][0]}) |{pc}")
    o.append(L["h_prio"])
    o.append(f"| {L['c_tag']} | {L['c_freq']} | {L['c_sev']} | {L['c_eff']} | {L['c_score']} | {L['c_note']} |\n|---|---|---|---|---|---|")
    for t in themes:
        if t["n"] < minp: continue
        o.append(f"| {t['tag']} | {t['n']}/{t['total']} | {t['sev']:g} | {t['eff']:g} | {t['score']} | {t['flag']} |")
    methods = sorted({m for t in themes for m in t["methods"]})
    if methods:
        o.append(L["h_matrix"])
        o.append(f"| {L['c_tag']} | " + " | ".join(methods) + f" | {L['c_methods']} | {L['c_note']} |\n|---|" + "---|" * (len(methods) + 2))
        for t in sorted(themes, key=lambda x: (-len(x["methods"]), -x["n"], x["tag"])):
            if t["n"] < minp: continue
            cells = [str(t["methods"].get(m, "-")) for m in methods]
            note = L["single"] if len(t["methods"]) == 1 else ""
            o.append(f"| {t['tag']} | " + " | ".join(cells) + f" | {len(t['methods'])} | {note} |")
        o.append(L["matrix_foot"])
    o.append(L["h_groups"])
    groups = defaultdict(list)
    for r in rows:
        groups[r.get("group") or r["_tags"][0]].append(r)
    for g in sorted(groups):
        o.append(L["g_title"].format(g=g, k=len({r["participant"] for r in groups[g]})))
        for r in groups[g]:
            o.append(f"- {r['note']} ({r['participant']}) [{'; '.join(r['_tags'])}]")
        o.append("")
    o.append(L["reminder"])
    return "\n".join(o)


def render_csv(themes, minp, L):
    s = io.StringIO()
    w = csv.writer(s)
    w.writerow(L["csv_head"])
    for t in themes:
        if t["n"] >= minp:
            w.writerow([t["tag"], t["n"], t["total"], t["mentions"], t["types"], t["sev"], t["eff"], t["score"], t["flag"],
                        t["participants"], "" if t["pattern"] is None else (L["csv_yes"] if t["pattern"] else L["csv_no"])])
    return s.getvalue()


def main():
    lang = "en"
    if "--lang" in sys.argv:
        i = sys.argv.index("--lang")
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in T:
            lang = sys.argv[i + 1]
    L = T[lang]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", help=L["d_csv"])
    ap.add_argument("--total-participants", "--total-participantes", dest="total", type=int, help=L["d_total"])
    ap.add_argument("--format", "--formato", dest="fmt", choices=["md", "csv"], default="md")
    ap.add_argument("--min-participants", "--min-participantes", dest="minp", type=int, default=1, help=L["d_min"])
    ap.add_argument("--separator", "--separador", dest="sep", default=";", help=L["d_sep"])
    ap.add_argument("--output", "--salida", dest="out", help=L["d_out"])
    ap.add_argument("--pattern-rule", "--regla-patron", dest="rule",
                    choices=["three", "third", "both", "tres", "tercio", "ambas"], help=L["d_rule"])
    ap.add_argument("--threshold-table", "--tabla-umbrales", dest="thr", action="store_true", help=L["d_thr"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=L["d_lang"])
    a = ap.parse_args()
    rule = RULE_ALIASES.get(a.rule, a.rule)
    if a.thr:
        print(threshold_table(L))
        return
    if not a.csv:
        ap.error(L["err_nocsv"])
    rows = read_rows(a.csv, a.sep, L)
    if not rows:
        die(L["err_empty"])
    total = a.total or len({r["participant"] for r in rows})
    if total < 1:
        die(L["err_total"])
    themes = analyze(rows, total, rule, L)
    out = render_md(themes, rows, total, a.minp, rule, L) if a.fmt == "md" else render_csv(themes, a.minp, L)
    if a.out:
        try:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(out)
        except OSError as e:
            die(L["err_write"].format(p=a.out, e=e.strerror or e))
    else:
        print(out)


if __name__ == "__main__":
    main()
