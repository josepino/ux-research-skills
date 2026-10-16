#!/usr/bin/env python3
"""Quality check of cards (card sorting) and tasks (tree testing). Python 3 standard library only.

Usage:
  check_study.py --cards cards.txt [--lang en|es]
  check_study.py --tasks tasks.txt --tree tree.txt
  (the options can be combined; Spanish aliases: --tarjetas, --tareas, --arbol)

Text files, one item per line:
  cards.txt  one card per line
  tasks.txt  one task (scenario) per line
  tree.txt   one tree label per line (indentation and bullets are ignored)

Checks (practical rules of ours, not published standards; they are warnings, not verdicts):
  cards: more than 50 (fatigue, NN/g suggests 30-50), fewer than 15, one idea per card
         (connectors and/or/y/o, commas, slashes), long labels, duplicates,
         keywords shared between cards (people group by the word, not the concept).
  tasks: words from the tree labels that appear in the task (obvious clue), very short scenarios.
Word lists cover English and Spanish.
Exit codes: 0 ok (even with warnings), 2 missing/unreadable file or bad options.
"""
import argparse
import os
import re
import sys
import unicodedata
from collections import defaultdict

STOP = {
    # Spanish
    "de", "la", "el", "los", "las", "y", "o", "e", "u", "en", "a", "un", "una", "con", "por", "para", "del", "al",
    "tu", "mi", "su", "que", "se", "lo", "como", "sobre",
    # English
    "the", "and", "or", "of", "to", "in", "for", "on", "with", "your", "my", "our", "a", "an", "at", "by", "from", "about", "how", "my",
}
CONNECTORS = r"\b(y|e|o|u|and|or)\b|,|/| & "

T = {
    "en": {
        "nofile": "file not found: {p!r}",
        "enc": "{p!r} is not UTF-8",
        "need": "pass --cards and/or --tasks (with --tree)",
        "needtree": "--tasks needs --tree to detect clues",
        "many": "WARNING: {n} cards; more than ~50 tires people and they dump everything in 'Misc'.",
        "few": "WARNING: only {n} cards; may be too few to see structure.",
        "idea": "ONE IDEA: {t!r} seems to join more than one concept",
        "long": "LONG: {t!r} has {n} words",
        "dup": "DUPLICATE: {t!r} appears {n} times",
        "word": "REPEATED WORD '{w}' in {n} cards: {ts} (people may group by the word, not the concept)",
        "clue": "CLUE: task {t!r} uses tree words: {w}",
        "short": "SHORT SCENARIO: {t!r} (does it have motive and context?)",
        "end": "\n{n} warning(s)." ,
        "review": " Review them; they are indicative.",
        "clean": " No warnings with these rules (this does not guarantee quality: run a pilot).",
        "empty": "{p!r} has no items",
    },
    "es": {
        "nofile": "no existe el archivo {p!r}",
        "enc": "{p!r} no está en UTF-8",
        "need": "pasá --cards/--tarjetas y/o --tasks/--tareas (con --tree/--arbol)",
        "needtree": "--tasks necesita --tree para detectar pistas",
        "many": "AVISO: {n} tarjetas; más de ~50 cansa y la gente tira todo a 'Varios'.",
        "few": "AVISO: solo {n} tarjetas; puede ser poco para ver estructura.",
        "idea": "UNA IDEA: {t!r} parece juntar más de un concepto",
        "long": "LARGA: {t!r} tiene {n} palabras",
        "dup": "DUPLICADA: {t!r} aparece {n} veces",
        "word": "PALABRA REPETIDA «{w}» en {n} tarjetas: {ts} (pueden agruparse por la palabra, no por el concepto)",
        "clue": "PISTA: la tarea {t!r} usa palabras del árbol: {w}",
        "short": "ESCENARIO CORTO: {t!r} (¿tiene motivo y contexto?)",
        "end": "\n{n} aviso(s).",
        "review": " Revisalos; son orientativos.",
        "clean": " Sin avisos con estas reglas (no garantiza calidad: hacé un piloto).",
        "empty": "{p!r} no tiene elementos",
    },
}


def die(L, key, **kw):
    print("Error: " + T[L][key].format(**kw), file=sys.stderr)
    sys.exit(2)


def read(path, L):
    if not os.path.isfile(path):
        die(L, "nofile", p=path)
    try:
        with open(path, encoding="utf-8-sig") as f:
            items = [re.sub(r"^[\s\-\*•\d\.\)]+", "", l).strip() for l in f if l.strip()]
    except UnicodeDecodeError:
        die(L, "enc", p=path)
    if not items:
        die(L, "empty", p=path)
    return items


def words(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return [w for w in re.findall(r"[a-z0-9]+", t) if w not in STOP and len(w) > 3]


def check_cards(items, L):
    n_warn = 0
    seen, use = defaultdict(list), defaultdict(list)
    if len(items) > 50:
        print(T[L]["many"].format(n=len(items))); n_warn += 1
    if len(items) < 15:
        print(T[L]["few"].format(n=len(items))); n_warn += 1
    for t in items:
        seen[t.lower()].append(t)
        for w in set(words(t)):
            use[w].append(t)
        if re.search(CONNECTORS, t.lower()):
            print(T[L]["idea"].format(t=t)); n_warn += 1
        if len(t.split()) > 8:
            print(T[L]["long"].format(t=t, n=len(t.split()))); n_warn += 1
    for v in seen.values():
        if len(v) > 1:
            print(T[L]["dup"].format(t=v[0], n=len(v))); n_warn += 1
    for w, ts in sorted(use.items()):
        if len(ts) > 1:
            print(T[L]["word"].format(w=w, n=len(ts), ts="; ".join(ts))); n_warn += 1
    return n_warn


def check_tasks(items, tree, L):
    n_warn = 0
    labels = defaultdict(list)
    for e in tree:
        for w in set(words(e)):
            labels[w].append(e)
    for t in items:
        hit = sorted(w for w in set(words(t)) if w in labels)
        if hit:
            print(T[L]["clue"].format(t=t, w=", ".join(hit))); n_warn += 1
        if len(t.split()) < 6:
            print(T[L]["short"].format(t=t)); n_warn += 1
    return n_warn


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cards", "--tarjetas", dest="cards")
    ap.add_argument("--tasks", "--tareas", dest="tasks")
    ap.add_argument("--tree", "--arbol", dest="tree")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="output language (default en)")
    a = ap.parse_args(argv)
    L = a.lang
    if not (a.cards or a.tasks):
        print("Error: " + T[L]["need"], file=sys.stderr); return 2
    if a.tasks and not a.tree:
        print("Error: " + T[L]["needtree"], file=sys.stderr); return 2
    total = 0
    if a.cards:
        total += check_cards(read(a.cards, L), L)
    if a.tasks:
        total += check_tasks(read(a.tasks, L), read(a.tree, L), L)
    print(T[L]["end"].format(n=total) + (T[L]["review"] if total else T[L]["clean"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
