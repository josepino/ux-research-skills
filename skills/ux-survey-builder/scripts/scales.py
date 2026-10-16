#!/usr/bin/env python3
"""Score and quality-check standard UX scales. Python 3 standard library only.

Subcommands:
  sus       SUS score per participant + suspicious-response flags (our heuristics)
  standard  compare your questionnaire items with the standard SUS wording
  umux      UMUX-Lite (7-point): raw 0-100 score and SUS-equivalent (Lewis et al.)
  seq       SEQ (7-point): mean per task and share of answers below 5
  nps       NPS from 0-10 answers

Examples:
  scales.py sus responses.csv
  scales.py sus --row 4,2,5,1,4,2,5,1,4,2
  scales.py standard my_questionnaire.txt --lang en     # one item per line
  scales.py umux --row 6,7
  scales.py seq 7,6,5,4,7
  scales.py nps 10,9,7,3
  scales.py sus responses.csv --lang es                 # Spanish output

CSV: one row per participant; the last N numeric cells are used
(N = 10 for sus, 2 for umux, 1 for seq). Header and ID cells are ignored.
Exit codes: 0 ok, 1 standard wording differs, 2 bad input (missing file, invalid values, no usable rows).
"""
import argparse
import csv
import difflib
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sus_score as S  # noqa: E402

REF = os.path.join(HERE, "..", "references")

T = {
    "en": {
        "nofile": "file not found: {p!r}",
        "cant": "could not read {p!r} as CSV: {e}",
        "norows": "no rows with at least {n} numeric values in {p!r}",
        "ints": "{what} must be whole numbers separated by commas (got: {t!r})",
        "count": "expected {n} {what}, got {k}",
        "oor": "{what} outside {lo}-{hi}: {v}",
        "need": "pass a CSV file or --row",
        "answers": "answers",
        "skip15": "row {i}: outside 1-5, skipped",
        "skip17": "row {i}: outside 1-7, skipped",
        "novalid": "no valid rows",
        "sus_row": "row {i}: SUS {s:.1f}",
        "review": "  [REVIEW: {f}]",
        "sus_sum": "n = {n}  mean = {m:.1f} ({g}; {a})  average reference = 68",
        "sus_note": "Note: 'REVIEW' uses our own heuristics (not a published standard); decide case by case and report the score with and without those rows.",
        "n_diff": "WARNING: your questionnaire has {a} items and the standard {b}. SUS requires all 10, in order.",
        "missing": "Item {i}: MISSING",
        "ok": "Item {i}: OK (the word 'system' may be replaced by site/app/product)",
        "mod": "Item {i}: MODIFIED (similarity {r:.0%}{note})\n   standard: {s}\n   yours:    {t}",
        "moved": "; seems to be at position {j} (order altered)",
        "res_ok": "Result: standard wording kept.",
        "res_bad": "Result: {m} item(s) differ: the score is no longer comparable with SUS benchmarks.",
        "std_limit": "Limit: reference text for --lang {lang}; the 1-5 answer options are not checked.",
        "umux_row": "row {i}: item 1 (meets requirements) = {x}, item 2 (easy to use) = {y} -> raw 0-100 = {r:.1f}; SUS-equivalent (Lewis et al. regression) = {g:.1f}",
        "umux_sum": "n = {n}  mean raw = {a:.1f}  mean SUS-equivalent = {b:.1f}",
        "umux_note": "7-point version only (Lewis et al.). No verified cutoffs: compare with your own baseline. The regression comes from the source cited in references/sources.md; MeasuringU says more research is needed to refine it.",
        "seq_need": "pass comma-separated answers or a CSV",
        "seq_range": "SEQ runs from 1 to 7",
        "seq_a": "n = {n}  mean = {m:.2f}  median = {md:.1f}",
        "seq_b": "answers below 5: {k} of {n} ({p:.0%}) -> ask those people to explain what made the task difficult",
        "seq_c": "Reference (MeasuringU): historical average between 5.3 and 5.6 over 400+ tasks and 10,000+ users (updated 2019); no formal cutoffs. Compare the same task across rounds.",
        "nps_line": "NPS = {s:.0f} (promoters {p}, passives {pa}, detractors {d}, n = {n})",
        "nps_warn": "Warning: with few answers NPS is unstable.",
        "flag_same": "identical answers on all 10 items (all {v}): SUS mixes positive and negative items, so this is contradictory",
    },
    "es": {
        "nofile": "no existe el archivo {p!r}",
        "cant": "no pude leer {p!r} como CSV: {e}",
        "norows": "no encontré filas con al menos {n} valores numéricos en {p!r}",
        "ints": "{what} deben ser enteros separados por comas (recibí: {t!r})",
        "count": "se esperaban {n} {what}, llegaron {k}",
        "oor": "{what} fuera de rango {lo}-{hi}: {v}",
        "need": "pasá un CSV o --row",
        "answers": "respuestas",
        "skip15": "fila {i}: respuestas fuera de 1-5, se omite",
        "skip17": "fila {i}: fuera de 1-7, se omite",
        "novalid": "ninguna fila válida",
        "sus_row": "fila {i}: SUS {s:.1f}",
        "review": "  [REVISAR: {f}]",
        "sus_sum": "n = {n}  media = {m:.1f} ({g}; {a})  referencia promedio = 68",
        "sus_note": "Nota: 'REVISAR' usa heurísticas nuestras (no un estándar publicado); decidí caso por caso y reportá el puntaje con y sin esas filas.",
        "n_diff": "AVISO: tu cuestionario tiene {a} ítems y el estándar {b}. El SUS exige los 10, en orden.",
        "missing": "Ítem {i}: FALTA",
        "ok": "Ítem {i}: OK (el término 'sistema' puede reemplazarse por sitio/app/producto)",
        "mod": "Ítem {i}: MODIFICADO (parecido {r:.0%}{note})\n   estándar: {s}\n   tuyo:     {t}",
        "moved": "; parece estar en la posición {j} (orden alterado)",
        "res_ok": "Resultado: redacción estándar conservada.",
        "res_bad": "Resultado: {m} ítem(s) difieren: el puntaje ya no es comparable con los benchmarks del SUS.",
        "std_limit": "Límite: texto de referencia para --lang {lang}; no se verifican las opciones de respuesta 1-5.",
        "umux_row": "fila {i}: ítem 1 (cumple requisitos) = {x}, ítem 2 (fácil de usar) = {y} -> crudo 0-100 = {r:.1f}; equivalente SUS (regresión Lewis et al.) = {g:.1f}",
        "umux_sum": "n = {n}  media cruda = {a:.1f}  media equivalente SUS = {b:.1f}",
        "umux_note": "Solo versión de 7 puntos (Lewis et al.). Sin puntos de corte verificados: comparalo con tu propia línea base. La regresión es de la fuente citada en references/sources.md; MeasuringU pide más investigación para refinarla.",
        "seq_need": "pasá respuestas separadas por coma o un CSV",
        "seq_range": "el SEQ va de 1 a 7",
        "seq_a": "n = {n}  media = {m:.2f}  mediana = {md:.1f}",
        "seq_b": "respuestas menores a 5: {k} de {n} ({p:.0%}) -> pedí a esas personas que expliquen la dificultad",
        "seq_c": "Referencia (MeasuringU): promedio histórico entre 5,3 y 5,6 en más de 400 tareas y 10.000 usuarios (actualizado 2019); sin cortes formales. Compará la misma tarea entre rondas.",
        "nps_line": "NPS = {s:.0f} (promotores {p}, pasivos {pa}, detractores {d}, n = {n})",
        "nps_warn": "Aviso: con pocas respuestas el NPS es inestable.",
    },
}


class Bad(Exception):
    pass


def fail(L, key, **kw):
    print("Error: " + T[L][key].format(**kw), file=sys.stderr)
    sys.exit(2)


def ints(L, txt, lo, hi, n=None):
    what = T[L]["answers"]
    try:
        v = [int(x) for x in txt.split(",") if x.strip() != ""]
    except ValueError:
        fail(L, "ints", what=what, t=txt)
    if n and len(v) != n:
        fail(L, "count", n=n, what=what, k=len(v))
    if not v or any(not lo <= x <= hi for x in v):
        fail(L, "oor", what=what, lo=lo, hi=hi, v=v)
    return v


def rows(L, path, n):
    if not os.path.isfile(path):
        fail(L, "nofile", p=path)
    try:
        found = S.parse_rows(path, n)
    except (UnicodeDecodeError, csv.Error, OSError) as e:
        fail(L, "cant", p=path, e=e)
    # skip a numeric header such as 1,2,...,10
    found = [(i, v) for i, v in found if not (n == 10 and v == list(range(1, 11)))]
    if not found:
        fail(L, "norows", n=n, p=path)
    return found


def cmd_sus(a):
    L = a.lang
    data = [(0, ints(L, a.row, 1, 5, 10))] if a.row else rows(L, a.file, 10) if a.file else fail(L, "need")
    pts, flagged = [], 0
    for i, it in data:
        if any(not 1 <= x <= 5 for x in it):
            print(T[L]["skip15"].format(i=i), file=sys.stderr)
            continue
        s = S.sus(it)
        pts.append(s)
        fl = S.flags(it, L)
        flagged += bool(fl)
        print(T[L]["sus_row"].format(i=i, s=s) + (T[L]["review"].format(f="; ".join(fl)) if fl else ""))
    if not pts:
        fail(L, "novalid")
    m = statistics.mean(pts)
    g = S.MSG[L]["grade"].format(g=S.grade(m))
    print(T[L]["sus_sum"].format(n=len(pts), m=m, g=g, a=S.MSG[L]["acc"][S.acceptability_key(m)]))
    if flagged:
        print(T[L]["sus_note"])
    return 0


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"\b(sistema|sitio web|aplicacion|app|producto|plataforma|sitio|system|website|web site|site|application|product|platform)\b", "X", t)
    t = re.sub(r"^\s*\d+[\).:-]\s*", "", t)
    return re.sub(r"[^a-zx ]+", "", t).split()


def cmd_standard(a):
    L = a.lang
    ref = a.standard or os.path.join(REF, f"sus-items-{L}.txt")
    for p in (a.file, ref):
        if not os.path.isfile(p):
            fail(L, "nofile", p=p)
    try:
        read = lambda p: [l.strip() for l in open(p, encoding="utf-8-sig") if l.strip()]
        mine, std = read(a.file), read(ref)
    except UnicodeDecodeError:
        fail(L, "cant", p=a.file, e="not UTF-8")
    if not mine:
        fail(L, "norows", n=1, p=a.file)
    if len(mine) != len(std):
        print(T[L]["n_diff"].format(a=len(mine), b=len(std)))
    sim = lambda x, y: difflib.SequenceMatcher(None, " ".join(norm(x)), " ".join(norm(y))).ratio()
    bad = 0
    for i, s in enumerate(std, 1):
        if i > len(mine):
            print(T[L]["missing"].format(i=i))
            bad += 1
            continue
        r = sim(s, mine[i - 1])
        if r >= 0.98:
            print(T[L]["ok"].format(i=i))
        else:
            bad += 1
            j = max(range(len(mine)), key=lambda k: sim(s, mine[k]))
            note = T[L]["moved"].format(j=j + 1) if j != i - 1 and norm(s) == norm(mine[j]) else ""
            print(T[L]["mod"].format(i=i, r=r, note=note, s=s, t=mine[i - 1]))
    print(T[L]["res_ok"] if not bad else T[L]["res_bad"].format(m=bad))
    print(T[L]["std_limit"].format(lang=L))
    return 0 if not bad else 1


def cmd_umux(a):
    L = a.lang
    data = [(0, ints(L, a.row, 1, 7, 2))] if a.row else rows(L, a.file, 2) if a.file else fail(L, "need")
    out = []
    for i, (x, y) in data:
        if not (1 <= x <= 7 and 1 <= y <= 7):
            print(T[L]["skip17"].format(i=i), file=sys.stderr)
            continue
        r = (x + y - 2) * 100 / 12
        g = 0.65 * r + 22.9
        out.append((r, g))
        print(T[L]["umux_row"].format(i=i, x=x, y=y, r=r, g=g))
    if not out:
        fail(L, "novalid")
    print(T[L]["umux_sum"].format(n=len(out), a=statistics.mean(r for r, _ in out), b=statistics.mean(g for _, g in out)))
    print(T[L]["umux_note"])
    return 0


def cmd_seq(a):
    L = a.lang
    if a.answers and os.path.isfile(a.answers):
        v = [r[0] for _, r in rows(L, a.answers, 1)]
    elif a.answers:
        v = ints(L, a.answers, 1, 7)
    else:
        fail(L, "seq_need")
    if any(not 1 <= x <= 7 for x in v):
        fail(L, "seq_range")
    k = sum(x < 5 for x in v)
    print(T[L]["seq_a"].format(n=len(v), m=statistics.mean(v), md=statistics.median(v)))
    print(T[L]["seq_b"].format(k=k, n=len(v), p=k / len(v)))
    print(T[L]["seq_c"])
    return 0


def cmd_nps(a):
    L = a.lang
    v = ints(L, a.answers, 0, 10)
    s, p, pa, d, n = S.nps(v)
    print(T[L]["nps_line"].format(s=s, p=p, pa=pa, d=d, n=n))
    if n < 30:
        print(T[L]["nps_warn"])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, h in [("sus", cmd_sus, "SUS score and consistency"), ("standard", cmd_standard, "compare items with standard SUS wording"),
                        ("umux", cmd_umux, "UMUX-Lite 7-point"), ("seq", cmd_seq, "SEQ 7-point"), ("nps", cmd_nps, "NPS 0-10")]:
        p = sp.add_parser(name, help=h)
        p.add_argument("--lang", choices=["en", "es"], default=argparse.SUPPRESS)
        if name in ("sus", "umux"):
            p.add_argument("file", nargs="?"); p.add_argument("--row")
        elif name == "standard":
            p.add_argument("file"); p.add_argument("--standard", help="reference items file (default: bundled, per --lang)")
        else:
            p.add_argument("answers", nargs="?" if name == "seq" else None)
        p.set_defaults(f=fn)
    a = ap.parse_args()
    sys.exit(a.f(a))


if __name__ == "__main__":
    main()
