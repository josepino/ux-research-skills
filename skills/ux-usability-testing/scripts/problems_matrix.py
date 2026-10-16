#!/usr/bin/env python3
"""Frequency and average severity table from a CSV of usability problems.

Input CSV columns (header required):
  participant,problem,severity        (severity 0-4, NN/g scale)
Spanish aliases are accepted: participante, problema, severidad.
Column matching ignores case and surrounding spaces.

Usage:
  python3 problems_matrix.py data.csv
  python3 problems_matrix.py data.csv --n 5 --lang es

Output: for each problem, how many participants had it, the average
severity and a suggested order (average severity x frequency). The final
decision on priority belongs to the team. With n < 20 use counts, not
percentages.
Exit codes: 0 ok, 2 error (missing file, bad columns, empty file, severity
not a number or outside 0-4, empty participant/problem, --n too small).
"""
import argparse
import csv
import sys

ALIASES = {
    "participant": ["participant", "participante", "participant_id", "id"],
    "problem": ["problem", "problema", "issue"],
    "severity": ["severity", "severidad", "sev"],
}
CANON = list(ALIASES)

MSG = {
    "en": {
        "desc": "Reads a CSV with columns participant,problem,severity (0-4) and shows, per problem, how many participants had it, the average severity and a suggested order.",
        "csv": "CSV file with a header", "n": "total number of participants (default: those found in the CSV)",
        "lang": "output language (default en)",
        "e_open": "could not open {p}: {e}", "e_utf": "{p} is not UTF-8; save it as UTF-8 CSV.",
        "e_cols": "missing columns: {c}. Expected: participant,problem,severity (Spanish: participante,problema,severidad).",
        "e_sev": "line {i}: severity '{v}' is not a number.",
        "e_range": "line {i}: severity {v} is outside the 0-4 range.",
        "e_empty_cell": "line {i}: participant or problem is empty.",
        "e_nodata": "the CSV has no data rows.",
        "e_n": "--n={n} is smaller than the participants in the CSV ({k}).",
        "head": "Participants: {n}. Suggested order = average severity x frequency (the team makes the final call).",
        "col": ["Problem", "Freq.", "Avg. sev."], "of": "{c} of {n}",
        "note": "Note: small n, use counts, not percentages.",
    },
    "es": {
        "desc": "Lee un CSV con columnas participant,problem,severity (0-4) y muestra, por problema, cuántos participantes lo tuvieron, severidad promedio y orden sugerido.",
        "csv": "archivo CSV con encabezado", "n": "total de participantes (por defecto: los que aparecen en el CSV)",
        "lang": "idioma de la salida (por defecto en)",
        "e_open": "no se pudo abrir {p}: {e}", "e_utf": "{p} no está en UTF-8; guardalo como CSV UTF-8.",
        "e_cols": "faltan columnas: {c}. Se esperan: participante,problema,severidad (inglés: participant,problem,severity).",
        "e_sev": "línea {i}: severidad «{v}» no es un número.",
        "e_range": "línea {i}: severidad {v} fuera del rango 0-4.",
        "e_empty_cell": "línea {i}: participante o problema vacío.",
        "e_nodata": "el CSV no tiene filas de datos.",
        "e_n": "--n={n} es menor que los participantes en el CSV ({k}).",
        "head": "Participantes: {n}. Orden sugerido = severidad promedio × frecuencia (decisión final del equipo).",
        "col": ["Problema", "Frec.", "Sev. prom."], "of": "{c} de {n}",
        "note": "Nota: n chico, usá los conteos, no porcentajes.",
    },
}


def die(msg):
    print("Error: " + msg, file=sys.stderr)
    sys.exit(2)


def main():
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=["en", "es"], default="en")
    known, _ = pre.parse_known_args()
    m = MSG[known.lang]
    ap = argparse.ArgumentParser(description=m["desc"])
    ap.add_argument("csv", help=m["csv"])
    ap.add_argument("--n", type=int, help=m["n"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=m["lang"])
    a = ap.parse_args()

    try:
        f = open(a.csv, newline="", encoding="utf-8-sig")
    except OSError as e:
        die(m["e_open"].format(p=a.csv, e=e.strerror))
    data, everyone = {}, set()
    with f:
        try:
            r = csv.DictReader(f)
            fields = r.fieldnames or []
            colmap = {}
            for canon in CANON:
                for fld in fields:
                    if fld.strip().lower() in ALIASES[canon]:
                        colmap[canon] = fld
                        break
            missing = [c for c in CANON if c not in colmap]
            if missing:
                die(m["e_cols"].format(c=", ".join(missing)))
            for i, row in enumerate(r, 2):
                p = (row[colmap["participant"]] or "").strip()
                pr = (row[colmap["problem"]] or "").strip()
                raw = row[colmap["severity"]]
                try:
                    s = float(raw)
                except (TypeError, ValueError):
                    die(m["e_sev"].format(i=i, v=raw))
                if not 0 <= s <= 4:
                    die(m["e_range"].format(i=i, v="%g" % s))
                if not p or not pr:
                    die(m["e_empty_cell"].format(i=i))
                everyone.add(p)
                data.setdefault(pr, {})[p] = s
        except UnicodeDecodeError:
            die(m["e_utf"].format(p=a.csv))
        except csv.Error as e:
            die(str(e))
    if not data:
        die(m["e_nodata"])
    n = a.n or len(everyone)
    if n < len(everyone):
        die(m["e_n"].format(n=n, k=len(everyone)))
    rows = [(pr, len(d), sum(d.values()) / len(d)) for pr, d in data.items()]
    rows.sort(key=lambda x: (-x[2] * x[1], -x[1]))
    print(m["head"].format(n=n) + "\n")
    c = m["col"]
    print("%-50s %7s %10s" % (c[0], c[1], c[2]))
    for pr, k, s in rows:
        print("%-50s %7s %10.1f" % (pr[:50], m["of"].format(c=k, n=n), s))
    if n < 20:
        print("\n" + m["note"])


if __name__ == "__main__":
    main()
