#!/usr/bin/env python3
"""Card sorting similarity matrix and suggested grouping. Python 3 standard library only.

Input CSV (with header): participant,group,card
  (Spanish aliases accepted: participante,grupo,tarjeta)
Each row = one card placed in one group by one participant.

Usage: cardsort_matrix.py results.csv [--threshold 60] [--agreement] [--lang en|es]
  --threshold N  average-link clustering threshold, % of participants (default 60)
  --agreement    also print the card x category agreement and flag ambiguous cards (top
                 category below 50%). Standardize group names first (e.g. "Contact"/"Contact us").
Exit codes: 0 ok, 1 no usable rows, 2 missing file, unreadable CSV, missing columns or bad option.
"""
import argparse
import csv
import os
import sys
from collections import defaultdict
from itertools import combinations

ALIASES = {"participant": ("participant", "participante"), "group": ("group", "grupo"), "card": ("card", "tarjeta")}

T = {
    "en": {
        "nofile": "file not found: {p!r}",
        "cols": "the CSV needs the columns participant, group, card (Spanish: participante, grupo, tarjeta); missing: {m}",
        "read": "could not read the CSV (UTF-8?): {e}",
        "empty": "no usable rows (each row needs a participant and a card)",
        "head": "Participants: {n} · Cards: {c}\n",
        "pairs": "Strongest pairs (% of participants who grouped them together):",
        "clusters": "\nSuggested grouping (average similarity >= {t:.0f}%):",
        "orphan": "orphan", "cards": "{k} cards", "grp": "  Group {i} ({tag}): ",
        "agree": "\nCard x category agreement (top 3 per card; ! = leading category < 50%):",
        "noname": "(unnamed)",
        "names": "\nMost repeated group names:",
        "small": "\nNote: with few participants percentages are coarse (e.g. with {n}, one person = {p:.0f}%). Do not over-read them.",
    },
    "es": {
        "nofile": "no existe el archivo {p!r}",
        "cols": "el CSV necesita las columnas participant, group, card (o participante, grupo, tarjeta); faltan: {m}",
        "read": "no pude leer el CSV (¿UTF-8?): {e}",
        "empty": "no hay filas utilizables (cada fila necesita participante y tarjeta)",
        "head": "Participantes: {n} · Tarjetas: {c}\n",
        "pairs": "Pares más fuertes (% de participantes que los agruparon):",
        "clusters": "\nAgrupación sugerida (similitud promedio >= {t:.0f}%):",
        "orphan": "huérfana", "cards": "{k} tarjetas", "grp": "  Grupo {i} ({tag}): ",
        "agree": "\nAcuerdo tarjeta x categoría (top 3 por tarjeta; ! = categoría líder < 50 %):",
        "noname": "(sin nombre)",
        "names": "\nNombres de grupo más repetidos:",
        "small": "\nNota: con pocos participantes los porcentajes son gruesos (con {n}, una persona = {p:.0f} %). No los sobreinterpretes.",
    },
}


def die(L, key, **kw):
    print("Error: " + T[L][key].format(**kw), file=sys.stderr)
    sys.exit(2)


def load(path, L):
    if not os.path.isfile(path):
        die(L, "nofile", p=path)
    groups = defaultdict(lambda: defaultdict(set))  # participant -> group -> cards
    cards = set()
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            low = {(h or "").strip().lower(): h for h in (reader.fieldnames or [])}
            col = {}
            for canon, names in ALIASES.items():
                col[canon] = next((low[n] for n in names if n in low), None)
            missing = [k for k, v in col.items() if v is None]
            if missing:
                die(L, "cols", m=", ".join(missing))
            for r in reader:
                p, g, c = (r[col["participant"]] or "").strip(), (r[col["group"]] or "").strip(), (r[col["card"]] or "").strip()
                if p and c:
                    groups[p][g].add(c)
                    cards.add(c)
    except (UnicodeDecodeError, csv.Error) as e:
        die(L, "read", e=e)
    if not groups:
        print("Error: " + T[L]["empty"], file=sys.stderr)
        sys.exit(1)
    return groups, sorted(cards)


def similarity(groups):
    n = len(groups)
    pair = defaultdict(int)
    for p in groups:
        for members in groups[p].values():
            for a, b in combinations(sorted(members), 2):
                pair[(a, b)] += 1
    return {k: 100.0 * v / n for k, v in pair.items()}, n


def clusters(cards, sim, threshold):
    """Simple average-link clustering on the similarity."""
    cl = [{c} for c in cards]

    def avg(x, y):
        vals = [sim.get(tuple(sorted((a, b))), 0.0) for a in x for b in y]
        return sum(vals) / len(vals)

    while len(cl) > 1:
        best, bi, bj = -1.0, None, None
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                s = avg(cl[i], cl[j])
                if s > best:
                    best, bi, bj = s, i, j
        if best < threshold:
            break
        cl[bi] |= cl[bj]
        del cl[bj]
    return cl


def agreement(groups, cards, L):
    n = len(groups)
    cnt = defaultdict(lambda: defaultdict(int))
    for p in groups:
        for g, members in groups[p].items():
            for c in members:
                cnt[c][(g or T[L]["noname"]).lower()] += 1
    print(T[L]["agree"])
    for c in cards:
        top = sorted(cnt[c].items(), key=lambda kv: -kv[1])[:3]
        lead = 100.0 * top[0][1] / n if top else 0
        print(f"  {'!' if lead < 50 else ' '} {c}: " + ", ".join(f"{g} {100.0 * v / n:.0f}%" for g, v in top))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--threshold", type=float, default=60.0)
    ap.add_argument("--agreement", action="store_true")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    a = ap.parse_args(argv)
    L = a.lang
    groups, cards = load(a.file, L)
    sim, n = similarity(groups)
    print(T[L]["head"].format(n=n, c=len(cards)))
    print(T[L]["pairs"])
    for (x, y), v in sorted(sim.items(), key=lambda kv: -kv[1])[:20]:
        print(f"  {v:5.0f}%  {x}  <->  {y}")
    print(T[L]["clusters"].format(t=a.threshold))
    for k, grp in enumerate(sorted(clusters(cards, sim, a.threshold), key=len, reverse=True), start=1):
        tag = T[L]["orphan"] if len(grp) == 1 else T[L]["cards"].format(k=len(grp))
        print(T[L]["grp"].format(i=k, tag=tag) + "; ".join(sorted(grp)))
    if a.agreement:
        agreement(groups, cards, L)
    names = defaultdict(int)
    for p in groups:
        for g in groups[p]:
            if g:
                names[g.lower()] += 1
    if names:
        print(T[L]["names"])
        for g, c in sorted(names.items(), key=lambda kv: -kv[1])[:10]:
            print(f"  {c}x  {g}")
    if n < 15:
        print(T[L]["small"].format(n=n, p=100.0 / n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
