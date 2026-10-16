#!/usr/bin/env python3
"""Summarize a log of research-influenced decisions (CSV -> Markdown).

Canonical columns: date, finding, recommendation, decision, owner, status,
metric, result.  Spanish aliases are accepted for the headers (fecha, hallazgo,
recomendacion, decision, responsable, estado, metrica, resultado) and for the
status values (aceptada, en backlog, implementada, rechazada, pendiente).

Python 3 standard library only.

Exit codes:
  0  summary printed (or template printed)
  1  input problem: missing/unreadable file, empty file, missing columns, bad --today
  2  command-line usage error (argparse)
"""
import argparse
import csv
import sys
import unicodedata
from collections import Counter
from datetime import date, datetime

COLUMNS = ["date", "finding", "recommendation", "decision", "owner",
           "status", "metric", "result"]

COLUMN_ALIASES = {
    "fecha": "date", "hallazgo": "finding", "recomendacion": "recommendation",
    "responsable": "owner", "estado": "status", "metrica": "metric",
    "resultado": "result",
}

# canonical statuses (in display order) and the spellings accepted for each
STATUSES = ["accepted", "backlog", "implemented", "rejected", "pending"]
STATUS_ALIASES = {
    "accepted": "accepted", "aceptada": "accepted", "aceptado": "accepted",
    "backlog": "backlog", "in backlog": "backlog", "en backlog": "backlog",
    "implemented": "implemented", "implementada": "implemented",
    "implementado": "implemented",
    "rejected": "rejected", "rechazada": "rejected", "rechazado": "rejected",
    "pending": "pending", "pendiente": "pending",
}
OPEN = {"pending", "backlog", "accepted"}  # neither implemented nor rejected yet
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")

TEXT = {
    "en": {
        "err": "Error: ",
        "empty_file": "the file is empty.",
        "missing_cols": "missing columns: %s. Expected: %s (Spanish aliases also accepted). Use --template to see the format.",
        "no_file": "file '%s' does not exist.",
        "is_dir": "'%s' is a folder, not a CSV.",
        "bad_enc": "could not read '%s' as UTF-8. Save it as UTF-8 CSV.",
        "cannot_open": "could not open '%s': %s",
        "no_rows": "the CSV has headers but no data rows.",
        "bad_today": "--today must use the format YYYY-MM-DD.",
        "need_csv": "the CSV path is missing (or use --template).",
        "title": "# Decision log summary\n",
        "cutoff": "Cutoff date: %s. Recommendations logged: %d.\n",
        "h_status": "## Status of the recommendations\n",
        "t_status": "| Status | Count | % |\n|---|---|---|",
        "no_status": "(no status)",
        "impl_rate": "**Implementation rate:** %d of %d (%.0f%%) implemented.",
        "impl_decided": "Of those with a decision (%d): %.0f%%.",
        "rate_note": "A low rate does not by itself prove the research failed: look at the reasons for rejection and backlog before concluding.\n",
        "h_oldest": "## Oldest open decisions\n",
        "t_oldest": "| Days open | Recommendation | Status | Owner |\n|---|---|---|---|",
        "no_owner": "NO OWNER",
        "none_open": "None open with a valid date.",
        "h_exec": "## Table for leadership\n",
        "t_exec": "| Date | Finding | Decision | Owner | Status | Metric | Result |\n|---|---|---|---|---|---|---|",
        "no_data": "no data",
        "exec_note": "Note: the Result column shows what was recorded; it does not imply causality unless the row documents it.\n",
        "h_warn": "## Warnings\n",
        "no_warn": "No warnings.",
        "row": "row %d (%s)",
        "no_text": "no text",
        "w_owner": "%s: no owner.",
        "w_metric": "%s: no metric.",
        "w_date": "%s: no date.",
        "w_bad_date": "%s: date not recognized ('%s'); use YYYY-MM-DD.",
        "w_status": "%s: no status.",
        "w_bad_status": "%s: unknown status ('%s'); valid: %s.",
        "w_rejected": "%s: rejected without a reason in 'decision'.",
        "w_impl": "%s: implemented but no measured result yet.",
        "desc": "Read a decision-log CSV and produce a Markdown summary.",
        "epilog": "Columns: %s. Dates YYYY-MM-DD (or DD/MM/YYYY). Statuses: %s (Spanish equivalents accepted). Exit codes: 0 ok, 1 input error, 2 usage error.",
        "h_csv": "path of the decision-log CSV",
        "h_template": "print an empty CSV with the headers",
        "h_today": "cutoff date YYYY-MM-DD (default: today)",
        "h_lang": "output language (default: en)",
    },
    "es": {
        "err": "Error: ",
        "empty_file": "el archivo esta vacio.",
        "missing_cols": "faltan columnas: %s. Se esperan: %s (tambien se aceptan los nombres en espanol). Usa --template para ver el formato.",
        "no_file": "no existe el archivo '%s'.",
        "is_dir": "'%s' es una carpeta, no un CSV.",
        "bad_enc": "no se pudo leer '%s' como UTF-8. Guardalo como CSV UTF-8.",
        "cannot_open": "no se pudo abrir '%s': %s",
        "no_rows": "el CSV tiene encabezados pero ninguna fila de datos.",
        "bad_today": "--today debe tener formato AAAA-MM-DD.",
        "need_csv": "falta la ruta del CSV (o usa --template).",
        "title": "# Resumen del registro de decisiones\n",
        "cutoff": "Fecha de corte: %s. Recomendaciones registradas: %d.\n",
        "h_status": "## Estado de las recomendaciones\n",
        "t_status": "| Estado | Cantidad | % |\n|---|---|---|",
        "no_status": "(sin estado)",
        "impl_rate": "**Tasa de implementacion:** %d de %d (%.0f%%) implementadas.",
        "impl_decided": "Sobre las que ya tienen decision (%d): %.0f%%.",
        "rate_note": "Una tasa baja no prueba por si sola que la investigacion fallo: mira los motivos de rechazo y de backlog antes de concluir.\n",
        "h_oldest": "## Decisiones abiertas mas antiguas\n",
        "t_oldest": "| Dias abiertas | Recomendacion | Estado | Responsable |\n|---|---|---|---|",
        "no_owner": "SIN RESPONSABLE",
        "none_open": "Ninguna abierta con fecha valida.",
        "h_exec": "## Tabla para direccion\n",
        "t_exec": "| Fecha | Hallazgo | Decision | Responsable | Estado | Metrica | Resultado |\n|---|---|---|---|---|---|---|",
        "no_data": "sin dato",
        "exec_note": "Nota: la columna Resultado muestra lo registrado; no implica causalidad salvo que la fila lo documente.\n",
        "h_warn": "## Avisos\n",
        "no_warn": "Sin avisos.",
        "row": "fila %d (%s)",
        "no_text": "sin texto",
        "w_owner": "%s: sin responsable.",
        "w_metric": "%s: sin metrica.",
        "w_date": "%s: sin fecha.",
        "w_bad_date": "%s: fecha no reconocida ('%s'); usa AAAA-MM-DD.",
        "w_status": "%s: sin estado.",
        "w_bad_status": "%s: estado desconocido ('%s'); validos: %s.",
        "w_rejected": "%s: rechazada sin motivo en 'decision'.",
        "w_impl": "%s: implementada sin resultado medido todavia.",
        "desc": "Lee un CSV del registro de decisiones y genera un resumen en Markdown.",
        "epilog": "Columnas: %s. Fechas AAAA-MM-DD (o DD/MM/AAAA). Estados: %s (se aceptan los equivalentes en espanol). Codigos de salida: 0 ok, 1 error de entrada, 2 error de uso.",
        "h_csv": "ruta del CSV del registro",
        "h_template": "imprime un CSV vacio con los encabezados",
        "h_today": "fecha de corte AAAA-MM-DD (por defecto, hoy)",
        "h_lang": "idioma de la salida (por defecto: en)",
    },
}

STATUS_LABEL = {
    "en": {"accepted": "accepted", "backlog": "backlog", "implemented": "implemented",
           "rejected": "rejected", "pending": "pending"},
    "es": {"accepted": "aceptada", "backlog": "en backlog", "implemented": "implementada",
           "rejected": "rechazada", "pending": "pendiente"},
}


def fail(msg):
    print("Error: " + msg, file=sys.stderr)
    sys.exit(1)


def strip_accents(txt):
    return "".join(c for c in unicodedata.normalize("NFD", txt)
                   if unicodedata.category(c) != "Mn")


def canonical_header(name):
    key = strip_accents((name or "").strip().lower())
    return COLUMN_ALIASES.get(key, key)


def canonical_status(raw):
    """Return the canonical status key, or None if empty/unknown."""
    return STATUS_ALIASES.get(strip_accents((raw or "").strip().lower()))


def parse_date(txt):
    txt = (txt or "").strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(txt, f).date()
        except ValueError:
            pass
    return None


def esc(txt):
    return (txt or "").replace("|", "/").replace("\n", " ").strip()


def read_log(path, T):
    def err(msg):
        fail(msg)
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            sample = fh.read(4096)
            fh.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel
            reader = csv.DictReader(fh, dialect=dialect)
            if not reader.fieldnames:
                err(T["empty_file"])
            mapping = {c: canonical_header(c) for c in reader.fieldnames if c}
            present = set(mapping.values())
            missing = [c for c in COLUMNS if c not in present]
            if missing:
                err(T["missing_cols"] % (", ".join(missing), ", ".join(COLUMNS)))
            rows = []
            for row in reader:
                clean = {mapping[k]: (v or "").strip()
                         for k, v in row.items() if k and k in mapping}
                if any(clean.values()):
                    rows.append(clean)
    except FileNotFoundError:
        err(T["no_file"] % path)
    except IsADirectoryError:
        err(T["is_dir"] % path)
    except UnicodeDecodeError:
        err(T["bad_enc"] % path)
    except OSError as e:
        err(T["cannot_open"] % (path, e))
    if not rows:
        err(T["no_rows"])
    return rows


def summarize(rows, today, lang):
    T = TEXT[lang]
    L = STATUS_LABEL[lang]
    out = []
    statuses = [canonical_status(r["status"]) or ("" if not r["status"] else "?")
                for r in rows]
    count = Counter(statuses)
    total = len(rows)
    impl = count.get("implemented", 0)
    out.append(T["title"])
    out.append(T["cutoff"] % (today.isoformat(), total))

    out.append(T["h_status"])
    out.append(T["t_status"])
    for s in STATUSES:
        if count.get(s):
            out.append("| %s | %d | %.0f%% |" % (L[s], count[s], 100 * count[s] / total))
    if count.get(""):
        out.append("| %s | %d | %.0f%% |" % (T["no_status"], count[""], 100 * count[""] / total))
    if count.get("?"):
        out.append("| ? | %d | %.0f%% |" % (count["?"], 100 * count["?"] / total))
    decided = total - count.get("pending", 0) - count.get("", 0) - count.get("?", 0)
    out.append("")
    out.append(T["impl_rate"] % (impl, total, 100 * impl / total))
    if decided and decided != total:
        out.append(T["impl_decided"] % (decided, 100 * impl / decided))
    out.append(T["rate_note"])

    open_rows = []
    for r, s in zip(rows, statuses):
        if s in OPEN or s == "":
            d = parse_date(r["date"])
            if d:
                open_rows.append(((today - d).days, r, s))
    open_rows.sort(key=lambda x: -x[0])
    out.append(T["h_oldest"])
    if open_rows:
        out.append(T["t_oldest"])
        for days, r, s in open_rows[:5]:
            out.append("| %d | %s | %s | %s |" % (
                days, esc(r["recommendation"]), L.get(s, "-"),
                esc(r["owner"]) or T["no_owner"]))
    else:
        out.append(T["none_open"])
    out.append("")

    out.append(T["h_exec"])
    out.append(T["t_exec"])
    for r, s in sorted(zip(rows, statuses),
                       key=lambda p: parse_date(p[0]["date"]) or date.min):
        out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            esc(r["date"]) or "-", esc(r["finding"]), esc(r["decision"]) or "-",
            esc(r["owner"]) or "-", L.get(s) or esc(r["status"]) or "-",
            esc(r["metric"]) or "-", esc(r["result"]) or T["no_data"]))
    out.append("")
    out.append(T["exec_note"])

    warnings = []
    for i, (r, s) in enumerate(zip(rows, statuses), start=2):  # row 1 = header
        label = T["row"] % (i, esc(r["recommendation"])[:60] or T["no_text"])
        if not r["owner"]:
            warnings.append(T["w_owner"] % label)
        if not r["metric"]:
            warnings.append(T["w_metric"] % label)
        if not r["date"]:
            warnings.append(T["w_date"] % label)
        elif not parse_date(r["date"]):
            warnings.append(T["w_bad_date"] % (label, r["date"]))
        if not r["status"]:
            warnings.append(T["w_status"] % label)
        elif s == "?":
            warnings.append(T["w_bad_status"] % (label, r["status"], ", ".join(L[k] for k in STATUSES)))
        if s == "rejected" and not r["decision"]:
            warnings.append(T["w_rejected"] % label)
        if s == "implemented" and not r["result"]:
            warnings.append(T["w_impl"] % label)
    out.append(T["h_warn"])
    out.extend(["- " + w for w in warnings] if warnings else [T["no_warn"]])
    return "\n".join(out)


def main():
    # pick the help language before parsing so --help matches --lang
    lang = "en"
    if "--lang" in sys.argv:
        i = sys.argv.index("--lang")
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in TEXT:
            lang = sys.argv[i + 1]
    T = TEXT[lang]
    p = argparse.ArgumentParser(
        description=T["desc"],
        epilog=T["epilog"] % (", ".join(COLUMNS), ", ".join(STATUSES)))
    p.add_argument("csv", nargs="?", help=T["h_csv"])
    p.add_argument("--template", "--plantilla", action="store_true", dest="template",
                   help=T["h_template"])
    p.add_argument("--today", "--hoy", dest="today", help=T["h_today"])
    p.add_argument("--lang", choices=sorted(TEXT), default="en", help=T["h_lang"])
    a = p.parse_args()
    T = TEXT[a.lang]
    if a.template:
        print(",".join(COLUMNS))
        return
    if not a.csv:
        p.error(T["need_csv"])
    today = date.today()
    if a.today:
        today = parse_date(a.today)
        if not today:
            fail(T["bad_today"])
    print(summarize(read_log(a.csv, T), today, a.lang))


if __name__ == "__main__":
    main()
