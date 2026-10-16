#!/usr/bin/env python3
"""Consolidate the findings CSVs of several evaluators into one prioritized summary.

Usage: consolidate_findings.py eval_ana.csv eval_ben.csv [...] [--output summary.md] [--lang en|es]

Each CSV needs a header with these columns (any order):
  where, problem, heuristic, severity, recommendation   (recommendation is optional)
Spanish aliases are also accepted:
  donde, problema, heuristica, severidad, recomendacion
- heuristic: number 1-10.   - severity: 0-4.
The file name (without extension) is used as the evaluator name.

What it does: groups findings with the same place + heuristic, counts how many evaluators
reported each (agreement), averages severity and sorts (severity desc, agreement desc).
Findings seen by only one evaluator are marked: they may be valid, but discuss them.
Severity gaps of 2 or more points are listed for the team discussion.

Exit codes: 0 ok, 1 no usage / no valid rows, 2 missing file, unreadable CSV or missing columns.
"""
import argparse
import csv
import os
import sys
from collections import defaultdict

ALIASES = {
    "where": ("where", "donde", "dónde"),
    "problem": ("problem", "problema"),
    "heuristic": ("heuristic", "heuristica", "heurística"),
    "severity": ("severity", "severidad"),
    "recommendation": ("recommendation", "recomendacion", "recomendación"),
}

NAMES = {
    "en": {1: "Visibility of system status", 2: "Match with the real world", 3: "User control and freedom",
           4: "Consistency and standards", 5: "Error prevention", 6: "Recognition over recall",
           7: "Flexibility and efficiency", 8: "Aesthetic and minimalist design", 9: "Error recovery",
           10: "Help and documentation"},
    "es": {1: "Visibilidad del estado", 2: "Sistema y mundo real", 3: "Control y libertad",
           4: "Consistencia y estándares", 5: "Prevención de errores", 6: "Reconocimiento > recuerdo",
           7: "Flexibilidad y eficiencia", 8: "Estética y minimalismo", 9: "Recuperación de errores",
           10: "Ayuda y documentación"},
}

TXT = {
    "en": {
        "nofile": "file not found: {p!r}",
        "cols": "{p}: missing columns {c} (accepted names: where/donde, problem/problema, heuristic/heuristica, severity/severidad)",
        "read": "could not read {p!r} as UTF-8 CSV: {e}",
        "skip": "[warning] {p} row {n}: invalid heuristic/severity (heuristic 1-10, severity 0-4), skipped",
        "none": "no valid findings found in the given files",
        "title": "# Consolidated findings ({t} evaluators, {u} unique problems)\n",
        "head": ["#", "Where", "Heuristic", "Avg. sev.", "Sev. range", "Agreement", "Problem (first report)", "Recommendation"],
        "solo": " (only 1: discuss)",
        "byh": "\n## Problems per heuristic\n",
        "dis": "\n## Severity disagreements (gap >= 2): take to the team discussion\n",
        "dis_line": "- {w} / heuristic {h}: severities {s}",
        "wrote": "Written {p}",
    },
    "es": {
        "nofile": "no existe el archivo {p!r}",
        "cols": "{p}: faltan columnas {c} (nombres aceptados: where/donde, problem/problema, heuristic/heuristica, severity/severidad)",
        "read": "no pude leer {p!r} como CSV UTF-8: {e}",
        "skip": "[aviso] {p} fila {n}: heurística/severidad inválida (heurística 1-10, severidad 0-4), se omite",
        "none": "no hay hallazgos válidos en los archivos indicados",
        "title": "# Hallazgos consolidados ({t} evaluadores, {u} problemas únicos)\n",
        "head": ["#", "Dónde", "Heurística", "Sev. prom.", "Rango sev.", "Acuerdo", "Problema (primer reporte)", "Recomendación"],
        "solo": " (solo 1: discutir)",
        "byh": "\n## Problemas por heurística\n",
        "dis": "\n## Desacuerdos de severidad (diferencia >= 2): llevar a la discusión del equipo\n",
        "dis_line": "- {w} / heurística {h}: severidades {s}",
        "wrote": "Escrito {p}",
    },
}


def die(L, key, **kw):
    print("Error: " + TXT[L][key].format(**kw), file=sys.stderr)
    sys.exit(2)


def map_columns(fieldnames):
    """Return {canonical: actual header} or the set of missing canonical names."""
    low = {(h or "").strip().lower(): h for h in fieldnames}
    found = {}
    for canon, names in ALIASES.items():
        for nm in names:
            if nm in low:
                found[canon] = low[nm]
                break
    return found


def cell(v):
    return (v or "").strip()


def load(paths, L):
    groups = defaultdict(lambda: {"evals": set(), "sev": [], "probs": [], "recs": []})
    for path in paths:
        if not os.path.isfile(path):
            die(L, "nofile", p=path)
        ev = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                cols = map_columns(reader.fieldnames or [])
                missing = {"where", "problem", "heuristic", "severity"} - set(cols)
                if missing:
                    die(L, "cols", p=path, c=", ".join(sorted(missing)))
                for n, row in enumerate(reader, start=2):
                    try:
                        h = int(cell(row[cols["heuristic"]]))
                        s = int(cell(row[cols["severity"]]))
                        assert 1 <= h <= 10 and 0 <= s <= 4
                    except (ValueError, TypeError, AssertionError):
                        print(TXT[L]["skip"].format(p=path, n=n), file=sys.stderr)
                        continue
                    g = groups[(cell(row[cols["where"]]).lower(), h)]
                    g["evals"].add(ev)
                    g["sev"].append(s)
                    g["probs"].append(cell(row[cols["problem"]]))
                    g["recs"].append(cell(row[cols["recommendation"]]) if "recommendation" in cols else "")
        except (UnicodeDecodeError, csv.Error) as e:
            die(L, "read", p=path, e=e)
    return groups


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="one findings CSV per evaluator")
    ap.add_argument("--output", "--salida", dest="output", help="write the summary to this Markdown file")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    a = ap.parse_args(argv)
    L, T = a.lang, TXT[a.lang]
    groups = load(a.files, L)
    total = len({os.path.splitext(os.path.basename(p))[0] for p in a.files})
    rows = [(sum(g["sev"]) / len(g["sev"]), len(g["evals"]), w, h, g) for (w, h), g in groups.items()]
    if not rows:
        print("Error: " + T["none"], file=sys.stderr)
        return 1
    rows.sort(key=lambda x: (-x[0], -x[1]))
    names = NAMES[L]
    out = [T["title"].format(t=total, u=len(rows)),
           "| " + " | ".join(T["head"]) + " |", "|" + "---|" * len(T["head"])]
    for i, (sp, ne, where, h, g) in enumerate(rows, 1):
        flag = "" if ne > 1 else T["solo"]
        rec = next((r for r in g["recs"] if r), "")
        out.append(f"| {i} | {where} | {h} {names[h]} | {sp:.1f} | {min(g['sev'])}-{max(g['sev'])} | {ne}/{total}{flag} | "
                   f"{g['probs'][0].replace('|', '/')} | {rec.replace('|', '/')} |")
    per = defaultdict(int)
    for r in rows:
        per[r[3]] += 1
    out.append(T["byh"])
    out += [f"- {h} {names[h]}: {per[h]}" for h in range(1, 11)]
    dis = [r for r in rows if max(r[4]["sev"]) - min(r[4]["sev"]) >= 2]
    if dis:
        out.append(T["dis"])
        out += [T["dis_line"].format(w=r[2], h=r[3], s=sorted(r[4]["sev"])) for r in dis]
    text = "\n".join(out)
    if a.output:
        try:
            with open(a.output, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
        print(T["wrote"].format(p=a.output))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
