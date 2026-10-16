#!/usr/bin/env python3
"""Tree testing results summary. Python 3 standard library only.

CSV (with header): participant,task,correct,direct,seconds
  (Spanish aliases accepted: participante,tarea,correcto,directo,segundos)
  correct / direct = 1 or 0 (also yes/no/true/false/si/sí). direct and seconds are optional.

Usage: tree_test_summary.py results.csv [--lang en|es]

Reading guide printed per task (rules of thumb of this script, NOT a published standard):
  success < 50% critical; 50-75% review; 75-80% acceptable; > 80% good.
Maze cites (attributed to NN/g, not verified there) 60-80% good, 80-90% very good, > 90% excellent.
Exit codes: 0 ok, 1 no usable rows, 2 missing file, unreadable CSV or missing columns.
"""
import argparse
import csv
import os
import statistics
import sys
from collections import defaultdict

ALIASES = {"participant": ("participant", "participante"), "task": ("task", "tarea"),
           "correct": ("correct", "correcto"), "direct": ("direct", "directo"), "seconds": ("seconds", "segundos")}
TRUE = {"1", "si", "sí", "true", "yes", "y", "x", "ok"}

T = {
    "en": {
        "nofile": "file not found: {p!r}",
        "cols": "the CSV needs at least participant, task, correct (Spanish: participante, tarea, correcto); missing: {m}",
        "read": "could not read the CSV (UTF-8?): {e}",
        "empty": "no usable rows",
        "head": ("Task", "n", "Success", "Direct", "Median s", "95% CI success", "Reading"),
        "v": {"critical": "critical", "review": "review", "ok": "acceptable", "good": "good"},
        "warn": "\nWarning: with fewer than ~15-30 participants the percentages are indicative; use the confidence interval (3 of 4 successes is '75%' but the CI runs from ~30 to ~95%).",
        "nodirect": "\nNote: no 'direct' column found; directness is shown as 0%.",
    },
    "es": {
        "nofile": "no existe el archivo {p!r}",
        "cols": "el CSV necesita al menos participant, task, correct (o participante, tarea, correcto); faltan: {m}",
        "read": "no pude leer el CSV (¿UTF-8?): {e}",
        "empty": "no hay filas utilizables",
        "head": ("Tarea", "n", "Éxito", "Directo", "Mediana s", "IC 95% éxito", "Lectura"),
        "v": {"critical": "crítico", "review": "revisar", "ok": "aceptable", "good": "bueno"},
        "warn": "\nAviso: con menos de ~15-30 participantes los porcentajes son orientativos; mirá el intervalo de confianza (3 de 4 éxitos es '75 %' pero el IC va de ~30 a ~95 %).",
        "nodirect": "\nNota: no hay columna 'direct'/'directo'; la directitud se muestra como 0 %.",
    },
}


def die(L, key, **kw):
    print("Error: " + T[L][key].format(**kw), file=sys.stderr)
    sys.exit(2)


def wilson(k, n, z=1.96):
    """95% Wilson confidence interval for a proportion, in %."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return 100 * max(0, c - h), 100 * min(1, c + h)


def verdict(rate):
    return "critical" if rate < 50 else "review" if rate < 75 else "ok" if rate <= 80 else "good"


def load(path, L):
    if not os.path.isfile(path):
        die(L, "nofile", p=path)
    tasks = defaultdict(list)
    has_direct = False
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            low = {(h or "").strip().lower(): h for h in (reader.fieldnames or [])}
            col = {k: next((low[n] for n in names if n in low), None) for k, names in ALIASES.items()}
            missing = [k for k in ("participant", "task", "correct") if col[k] is None]
            if missing:
                die(L, "cols", m=", ".join(missing))
            has_direct = col["direct"] is not None
            for r in reader:
                task = (r[col["task"]] or "").strip()
                if not task:
                    continue
                secs = None
                if col["seconds"]:
                    try:
                        secs = float(str(r[col["seconds"]]).replace(",", "."))
                    except ValueError:
                        pass
                tasks[task].append((str(r[col["correct"]]).strip().lower() in TRUE,
                                    has_direct and str(r[col["direct"]]).strip().lower() in TRUE, secs))
    except (UnicodeDecodeError, csv.Error) as e:
        die(L, "read", e=e)
    if not tasks:
        print("Error: " + T[L]["empty"], file=sys.stderr)
        sys.exit(1)
    return tasks, has_direct


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    a = ap.parse_args(argv)
    L = a.lang
    tasks, has_direct = load(a.file, L)
    h = T[L]["head"]
    print(f"{h[0]:40} {h[1]:>3} {h[2]:>7} {h[3]:>8} {h[4]:>10}  {h[5]:>14}  {h[6]}")
    for t, rows in tasks.items():
        n = len(rows)
        ok = 100.0 * sum(r[0] for r in rows) / n
        direct = 100.0 * sum(r[1] for r in rows) / n
        secs = [r[2] for r in rows if r[2] is not None]
        med = f"{statistics.median(secs):.0f}" if secs else "-"
        lo, hi = wilson(sum(r[0] for r in rows), n)
        print(f"{t[:40]:40} {n:>3} {ok:>6.0f}% {direct:>7.0f}% {med:>10}  {lo:>6.0f}-{hi:>3.0f}%      {T[L]['v'][verdict(ok)]}")
    if any(len(r) < 15 for r in tasks.values()):
        print(T[L]["warn"])
    if not has_direct:
        print(T[L]["nodirect"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
