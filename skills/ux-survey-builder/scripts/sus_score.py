#!/usr/bin/env python3
"""Score the System Usability Scale (SUS) and NPS. Python 3 standard library only.

Usage:
  sus_score.py responses.csv            # CSV: one row per participant, 10 answers (1-5)
  sus_score.py --row 4,2,5,1,4,2,5,1,4,2
  sus_score.py --nps 10,9,7,3,8,10,6    # NPS from 0-10 answers
  sus_score.py responses.csv --lang es  # Spanish output

The CSV may have a header and a leading ID column: the last 10 numeric cells of
each row are used. Rows with fewer than 10 numeric cells (headers, blanks) are skipped.
Each participant row is also checked for suspicious patterns (straight-lining,
contradictory item pairs). Those flags are OUR heuristics, not a published standard.

Exit codes: 0 ok, 1 no valid rows / wrong usage, 2 unreadable input or invalid values.
For UMUX-Lite, SEQ and the standard-wording check use scales.py.
"""
import argparse
import csv
import statistics
import sys

MSG = {
    "en": {
        "need10": "expected 10 answers, got {n}",
        "range": "answers outside the 1-5 range: {v}",
        "ints": "answers must be whole numbers separated by commas",
        "nps_range": "NPS needs whole-number answers between 0 and 10",
        "unreadable": "could not read the file ({why}): {path}",
        "nofile": "file not found: {path}",
        "badcsv": "could not parse {path} as CSV: {why}",
        "novalid": "no valid responses found.",
        "grade": "grade {g}",
        "acc": {"acceptable": "acceptable", "unacceptable": "unacceptable", "marginal": "marginal"},
        "nps_line": "NPS = {s:.0f} (promoters {p}, passives {pa}, detractors {d}, n = {n})",
        "nps_warn": "Warning: with few answers NPS is unstable; treat it as indicative.",
        "row": "participant (row {n}): {s:.1f}",
        "review": "  [REVIEW: {f}]",
        "mean": "mean = {m:.1f} ({g}; {a}); reference average = 68",
        "median": "median = {v:.1f}",
        "minmax": "min-max = {lo:.1f} - {hi:.1f}",
        "sd": "standard deviation = {v:.1f}",
        "small": "Warning: with few participants the margin of error is wide; indicative only (the n threshold is a practical rule of ours, not from the sources).",
        "flag_note": "Note: 'REVIEW' flags use our own heuristics (not a published standard). Decide case by case and report the score with and without those rows.",
        "same": "identical answers on all 10 items (all {v}): SUS mixes positive and negative items, so this is contradictory",
        "line": "{k} of 10 answers are identical ({v}): possible straight-lining",
        "contra": "strong contradictions in item pairs {pairs}",
        "n": "n = {n}",
    },
    "es": {
        "need10": "se esperaban 10 respuestas, llegaron {n}",
        "range": "respuestas fuera del rango 1-5: {v}",
        "ints": "las respuestas deben ser números enteros separados por comas",
        "nps_range": "el NPS requiere respuestas enteras entre 0 y 10",
        "unreadable": "no pude leer el archivo ({why}): {path}",
        "nofile": "no existe el archivo: {path}",
        "badcsv": "no pude leer {path} como CSV: {why}",
        "novalid": "no se encontraron respuestas válidas.",
        "grade": "grado {g}",
        "acc": {"acceptable": "aceptable", "unacceptable": "inaceptable", "marginal": "marginal"},
        "nps_line": "NPS = {s:.0f} (promotores {p}, pasivos {pa}, detractores {d}, n = {n})",
        "nps_warn": "Aviso: con pocas respuestas el NPS es inestable; tomalo como orientativo.",
        "row": "participante (fila {n}): {s:.1f}",
        "review": "  [REVISAR: {f}]",
        "mean": "media = {m:.1f} ({g}; {a}); referencia promedio = 68",
        "median": "mediana = {v:.1f}",
        "minmax": "mín-máx = {lo:.1f} - {hi:.1f}",
        "sd": "desvío estándar = {v:.1f}",
        "small": "Aviso: con pocos participantes el margen de error es amplio; resultado orientativo (el umbral de n es un criterio práctico nuestro, no de las fuentes).",
        "flag_note": "Nota: 'REVISAR' usa heurísticas nuestras (no un estándar publicado). Decidí caso por caso y reportá el puntaje con y sin esas filas.",
        "same": "respuestas idénticas en los 10 ítems (todo {v}): el SUS mezcla ítems positivos y negativos, así que es contradictorio",
        "line": "{k} de 10 respuestas son idénticas ({v}): posible respuesta automática",
        "contra": "contradicciones fuertes en los pares de ítems {pairs}",
        "n": "n = {n}",
    },
}

# Positive/negative SUS item pairs (1-based) that measure almost the same thing from opposite
# poles. Answering both on the same side (both >= 4 or both <= 2) is contradictory.
# This is a heuristic of ours, not a published standard.
PAIRS = [(3, 8), (2, 3), (7, 10), (4, 7), (3, 4)]

# Curve grading (Sauro, as cited by TeaCup Lab). Indicative only.
# https://www.teacuplab.com/es/blog/que-es-la-escala-sus-y-como-usarla-para-medir-la-usabilidad/
GRADES = [(78.9, "A"), (72.6, "B"), (62.7, "C"), (51.7, "D"), (0.0, "F")]


def sus(items):
    """SUS score 0-100. Odd items: answer-1; even items: 5-answer; sum x 2.5."""
    if len(items) != 10:
        raise ValueError(("need10", {"n": len(items)}))
    if any(not 1 <= x <= 5 for x in items):
        raise ValueError(("range", {"v": items}))
    return sum((x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(items)) * 2.5


def grade(score):
    for floor, name in GRADES:
        if score >= floor:
            return name
    return "F"


def acceptability_key(score):
    # Same source: > 70 acceptable, < 50 unacceptable, otherwise marginal.
    return "acceptable" if score > 70 else "unacceptable" if score < 50 else "marginal"


def flags(items, lang="en"):
    """Review flags for one participant. Signals to check, not proof of bad answers (our heuristics)."""
    m = MSG[lang]
    out = []
    if len(set(items)) == 1:
        out.append(m["same"].format(v=items[0]))
    else:
        top = max(set(items), key=items.count)
        if items.count(top) >= 8:
            out.append(m["line"].format(k=items.count(top), v=top))
    contra = [(p, n) for p, n in PAIRS
              if (items[p - 1] >= 4 and items[n - 1] >= 4) or (items[p - 1] <= 2 and items[n - 1] <= 2)]
    if len(contra) >= 2 and len(set(items)) > 1:
        out.append(m["contra"].format(pairs=", ".join(f"{p}-{n}" for p, n in contra)))
    return out


def nps(scores):
    """NPS = % promoters (9-10) - % detractors (0-6). Source: Drive Research."""
    if not scores or any(not 0 <= x <= 10 for x in scores):
        raise ValueError(("nps_range", {}))
    n = len(scores)
    prom = sum(x >= 9 for x in scores)
    det = sum(x <= 6 for x in scores)
    return (prom - det) / n * 100, prom, n - prom - det, det, n


def parse_rows(path, n=10):
    """Return [(row_number, last n numeric values)] for rows with at least n numeric cells."""
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for i, rec in enumerate(csv.reader(f), start=1):
            vals = []
            for cell in rec:
                try:
                    vals.append(float(cell.replace(",", ".")))
                except ValueError:
                    pass
            if len(vals) >= n:
                rows.append((i, [int(v) for v in vals[-n:]]))
    return rows


def err(lang, key, **kw):
    print("Error: " + MSG[lang][key].format(**kw), file=sys.stderr)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="CSV with one SUS response row per participant")
    ap.add_argument("--row", help="one participant, 10 comma-separated answers (1-5)")
    ap.add_argument("--nps", help="comma-separated 0-10 answers")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    a = ap.parse_args(argv)
    L = a.lang
    m = MSG[L]
    try:
        if a.row:
            try:
                items = [int(x) for x in a.row.split(",")]
            except ValueError:
                return err(L, "ints")
            s = sus(items)
            print(f"SUS = {s:.1f} ({m['grade'].format(g=grade(s))}; {m['acc'][acceptability_key(s)]})")
            for f in flags(items, L):
                print(m["review"].format(f=f).strip())
            return 0
        if a.nps:
            try:
                vals = [int(x) for x in a.nps.split(",")]
            except ValueError:
                return err(L, "ints")
            score, p, pa, d, n = nps(vals)
            print(m["nps_line"].format(s=score, p=p, pa=pa, d=d, n=n))
            if n < 30:
                print(m["nps_warn"])
            return 0
        if not a.file:
            ap.print_usage(sys.stderr)
            return 1
        try:
            rows = parse_rows(a.file)
        except FileNotFoundError:
            return err(L, "nofile", path=a.file)
        except OSError as e:
            return err(L, "unreadable", why=e.strerror, path=a.file)
        except (UnicodeDecodeError, csv.Error) as e:
            return err(L, "badcsv", path=a.file, why=e)
        scores, flagged = [], 0
        for n, items in rows:
            try:
                s = sus(items)
            except ValueError as e:
                key, kw = e.args[0]
                print(f"row {n}: " + m[key].format(**kw), file=sys.stderr)
                continue
            scores.append(s)
            fl = flags(items, L)
            flagged += bool(fl)
            print(m["row"].format(n=n, s=s) + (m["review"].format(f="; ".join(fl)) if fl else ""))
        if not scores:
            print(m["novalid"], file=sys.stderr)
            return 1
        mean = statistics.mean(scores)
        print("-" * 36)
        print(m["n"].format(n=len(scores)))
        print(m["mean"].format(m=mean, g=m["grade"].format(g=grade(mean)), a=m["acc"][acceptability_key(mean)]))
        print(m["median"].format(v=statistics.median(scores)))
        print(m["minmax"].format(lo=min(scores), hi=max(scores)))
        if len(scores) > 1:
            print(m["sd"].format(v=statistics.stdev(scores)))
        if flagged:
            print(m["flag_note"])
        if len(scores) < 12:
            print(m["small"])
        return 0
    except ValueError as e:
        key, kw = e.args[0] if isinstance(e.args[0], tuple) else ("ints", {})
        return err(L, key, **kw)


if __name__ == "__main__":
    sys.exit(main())
