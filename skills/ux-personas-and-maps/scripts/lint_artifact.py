#!/usr/bin/env python3
"""Lint a UX artifact (persona, empathy map, journey) written in Markdown.

Works on English and Spanish artifacts.

Usage:
  python3 lint_artifact.py file.md [--type persona|empathy|journey|auto] [--lang en|es]
  python3 lint_artifact.py --pairs N     # pairwise comparisons for N concepts (mental-model studies)

Checks: status/date/version/evidence base, notes without a source or assumption tag,
empty table rows, number of personas and, in proto-personas, the share of assumptions.
Accepted tags (case-insensitive):
  source/data  : [E1] [E1, E2] [Quote] [Obs] [DATA]   (Spanish: [Cita] [DATO])
  inference    : [Inf]
  assumption   : [ASSUMPTION—VALIDATE] [Hypothesis]   (Spanish: [SUPUESTO—VALIDAR] [Hipótesis])
The dash in the assumption tag may be an em dash, en dash or hyphen. All assumption tags are
equivalent. The linter checks traceability and structure only, not the quality of the content.

Spanish aliases: --tipo (persona|empatia|journey), --pares.

Exit codes: 0 ok or warnings only; 1 errors found in the artifact; 2 unreadable file or bad usage.
"""
import argparse
import re
import sys

DASH = r"\s*[—–-]\s*"
ASSUMPTION = r"(?:ASSUMPTION%sVALIDATE|SUPUESTO%sVALIDAR|Hypothesis|Hip[oó]tesis)" % (DASH, DASH)
TAG = re.compile(r"\[(E\d+(\s*,\s*E\d+)*|Quote|Cita|Obs|Inf|DATA|DATO|%s)\]" % ASSUMPTION, re.I)
TAG_ASSUMPTION = re.compile(r"\[%s\]" % ASSUMPTION, re.I)
TAG_DATA = re.compile(r"\[(DATA|DATO|E\d+(\s*,\s*E\d+)*|Quote|Cita|Obs)\]", re.I)
STATUS_ASSUMPTION = re.compile(r"hypothesis|hip[oó]tesis|proto-?persona|assumption|supuesto", re.I)
STATUS_LINE = re.compile(r"(?:status|estado)\s*:?\s*[^\n]*(validated|validad|hypothesis|hip[oó]tesis|proto|assumption|supuesto|research|investigaci)", re.I)
DATE = re.compile(r"\b(20\d{2}[-/]\d{1,2}([-/]\d{1,2})?|\d{1,2}/\d{1,2}/20\d{2})\b")

M = {
    "en": {
        "type": "Detected type: {t}",
        "pairs": "{n} concepts -> {c} pairwise comparisons",
        "pairs_warn": "Warning: risk of participant fatigue; consider card sorting or fewer concepts.",
        "no_file": "missing file (give a .md file or use --pairs N)",
        "err_open": "ERROR: could not open '{p}': {e}",
        "err_utf": "ERROR: '{p}' is not UTF-8 text.",
        "e_status": "Missing 'Status' (Validated / Hypothesis or Proto-persona / Research-based).",
        "w_date": "No date (YYYY-MM-DD): without a date you cannot decide when to review.",
        "w_version": "No version.",
        "e_base": "No evidence base declared (n=__ / sources).",
        "w_gaps": "No information gaps section.",
        "w_next": "No 'Next research step' section.",
        "cells": "Table rows with content: {n}; with a source or assumption tag: {k} ({r:.0%})",
        "w_ratio": "Fewer than half of the notes have a source/tag. Tag them or label the artifact as Hypothesis.",
        "w_empty": "{n} empty table row(s): fill them in, or mark as an information gap if research is missing.",
        "e_quad": "Missing the quadrant '{q}'.",
        "w_emotion": "Emotion without a reason: use 'adjective: reason'.",
        "e_missing": "Missing {k}.",
        "w_cf": "It does not say whether this is a current or future map.",
        "w_actors": "Several 'actor' entries in one map: one map per actor.",
        "tags": "Tags: {d} data/source, {a} assumption ([ASSUMPTION—VALIDATE] / [Hypothesis]).",
        "w_proto": "Everything is an assumption but the status does not say Proto-persona/Hypothesis: label it that way in the header.",
        "w_validated": "It says Validated but more than 30% of the claims are assumptions: it is not a validated persona until those are closed (criterion in references/proto-persona.md).",
        "h1": "Level-1 headings (approx. personas): {n}",
        "w_many": "More than 5 personas: sources suggest the team must be able to remember them (range 1-7 depending on the source). Consider merging.",
        "w_quote": "No representative quote.",
        "ok": "OK: no findings.",
        "quads": ("says", "thinks", "does", "feels"),
        "k_actor": "actor", "k_scenario": "scenario", "k_opps": "opportunities",
        "d_file": "Markdown file to check",
        "d_type": "artifact type (default auto)",
        "d_pairs": "print pairwise comparisons for N concepts and exit",
        "d_lang": "language of the messages",
    },
    "es": {
        "type": "Tipo detectado: {t}",
        "pairs": "{n} conceptos -> {c} comparaciones por pares",
        "pairs_warn": "Aviso: riesgo de fatiga del participante; considera card sorting o reducir conceptos.",
        "no_file": "falta el archivo (indica un .md o usa --pairs N)",
        "err_open": "ERROR: no pude abrir '{p}': {e}",
        "err_utf": "ERROR: '{p}' no es texto UTF-8.",
        "e_status": "Falta 'Estado' (Validada / Hipótesis o Proto-persona / Basado en investigación).",
        "w_date": "No hay fecha (AAAA-MM-DD): sin fecha no se puede decidir cuándo revisar.",
        "w_version": "No hay versión.",
        "e_base": "No se declara base de evidencia (n=__ / fuentes).",
        "w_gaps": "No hay sección de vacíos de información.",
        "w_next": "No hay sección 'Siguiente paso de investigación'.",
        "cells": "Filas de tabla con contenido: {n}; con etiqueta de fuente o de supuesto: {k} ({r:.0%})",
        "w_ratio": "Menos de la mitad de las notas tiene fuente/etiqueta. Etiquétalas o rotula el artefacto como Hipótesis.",
        "w_empty": "{n} fila(s) de tabla vacías: completar, o marcar como vacío de información si falta investigación.",
        "e_quad": "Falta el cuadrante '{q}'.",
        "w_emotion": "Emoción sin motivo: usa 'adjetivo: motivo'.",
        "e_missing": "Falta {k}.",
        "w_cf": "No indica si es mapa actual o futuro.",
        "w_actors": "Varios 'actor' en un mismo mapa: un mapa por actor.",
        "tags": "Etiquetas: {d} de dato/fuente, {a} de supuesto ([SUPUESTO—VALIDAR] / [Hipótesis]).",
        "w_proto": "Todo son supuestos pero el estado no dice Proto-persona/Hipótesis: rotúlalo así en el encabezado.",
        "w_validated": "Dice Validada pero más del 30 % de las afirmaciones son supuestos: no pasa a persona validada hasta cerrar esos supuestos (criterio en references/proto-persona.md).",
        "h1": "Encabezados de nivel 1 (personas aprox.): {n}",
        "w_many": "Más de 5 personas: las fuentes sugieren que el equipo debe poder recordarlas (rango 1-7 según fuente). Considera fusionar.",
        "w_quote": "Sin cita representativa.",
        "ok": "OK: sin observaciones.",
        "quads": ("dice", "piensa", "hace", "siente"),
        "k_actor": "actor", "k_scenario": "escenario", "k_opps": "oportunidades",
        "d_file": "archivo Markdown a revisar",
        "d_type": "tipo de artefacto (default auto)",
        "d_pairs": "imprime las comparaciones por pares para N conceptos y termina",
        "d_lang": "idioma de los mensajes",
    },
}
QUAD_ALTS = {  # canonical quadrant -> regex accepting EN and ES
    0: r"says|dice", 1: r"thinks|piensa", 2: r"does|hace", 3: r"feels|siente",
}


def detect(txt):
    t = txt.lower()
    head = t[:600]
    # an explicit persona header wins over journey-like words in the body
    if re.search(r"(?:status|estado)\s*:?[^\n]*proto-?persona", head) or re.search(r"^#\s+[^\n]*persona", head, re.M):
        return "persona"
    if (("dice" in t and "piensa" in t and "siente" in t) or ("says" in t and "thinks" in t and "feels" in t)):
        return "empathy"
    if (("actor" in t and ("escenario" in t or "scenario" in t))
            or (re.search(r"fase|etapa|phase|stage", t) and re.search(r"puntos? de contacto|emoci|touchpoint|emotion", t))):
        return "journey"
    if re.search(r"persona|objetivos|goals", t):
        return "persona"
    return "unknown"


def table_rows(txt):
    for ln in txt.splitlines():
        s = ln.strip()
        if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", s):
            yield [c.strip() for c in s.strip("|").split("|")]


def main():
    lang = "en"
    if "--lang" in sys.argv:
        i = sys.argv.index("--lang")
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in M:
            lang = sys.argv[i + 1]
    L = M[lang]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help=L["d_file"])
    ap.add_argument("--type", "--tipo", dest="type", default="auto",
                    choices=["auto", "persona", "empathy", "empatia", "journey"], help=L["d_type"])
    ap.add_argument("--pairs", "--pares", dest="pairs", type=int, help=L["d_pairs"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=L["d_lang"])
    a = ap.parse_args()

    if a.pairs is not None:
        n = a.pairs
        if n < 0:
            print("ERROR: --pairs must be >= 0", file=sys.stderr)
            return 2
        print(L["pairs"].format(n=n, c=n * (n - 1) // 2))
        if n > 10:
            print(L["pairs_warn"])
        return 0
    if not a.file:
        ap.error(L["no_file"])

    try:
        with open(a.file, encoding="utf-8") as fh:
            txt = fh.read()
    except OSError as e:
        print(L["err_open"].format(p=a.file, e=e.strerror or e), file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print(L["err_utf"].format(p=a.file), file=sys.stderr)
        return 2
    kind = detect(txt) if a.type == "auto" else ("empathy" if a.type == "empatia" else a.type)
    errs, warns = [], []
    print(L["type"].format(t=kind))

    head = txt[:600]
    if not STATUS_LINE.search(txt) and not STATUS_ASSUMPTION.search(txt):
        errs.append(L["e_status"])
    if not DATE.search(txt):
        warns.append(L["w_date"])
    if not re.search(r"version|versi[oó]n|\bv\d+\b", txt, re.I):
        warns.append(L["w_version"])
    if not re.search(r"n\s*=\s*\d+|evidence base|base de evidencia|base\s*:|sources?|fuentes?|no research|sin investigaci", txt, re.I):
        errs.append(L["e_base"])
    if not re.search(r"gaps|what we don.t know|next questions|vac[ií]os|qu[eé] no sabemos|pr[oó]ximas preguntas", txt, re.I):
        warns.append(L["w_gaps"])

    if not re.search(r"next research step|next step|siguiente paso de investigaci|pr[oó]ximo paso de investigaci|pr[oó]ximos pasos", txt, re.I):
        warns.append(L["w_next"])

    # a table row counts as "with content" if some cell is long enough (first column is a label),
    # and as "tagged" if any cell of the row carries a source or assumption tag
    rows = [r for r in table_rows(txt) if any(len(c) > 12 and not TAG.fullmatch(c) for c in r[1:])]
    if rows:
        k = sum(1 for r in rows if any(TAG.search(c) for c in r))
        ratio = k / len(rows)
        print(L["cells"].format(n=len(rows), k=k, r=ratio))
        if ratio < 0.5 and not STATUS_ASSUMPTION.search(head):
            warns.append(L["w_ratio"])
    empty = sum(1 for r in table_rows(txt) if len(r) > 1 and all(c == "" for c in r[1:]))
    if empty:
        warns.append(L["w_empty"].format(n=empty))

    if kind == "empathy":
        for idx in range(4):
            if not re.search(QUAD_ALTS[idx], txt, re.I):
                errs.append(L["e_quad"].format(q=L["quads"][idx]))
        if re.search(r"(feels|siente)[^\n]*\n[^\n]*\b(frustrated|anxious|confused|frustrad[oa]|ansios[oa]|confundid[oa])\b\s*\|", txt, re.I):
            warns.append(L["w_emotion"])
    if kind == "journey":
        for key, pat in (("k_actor", r"actor|persona"), ("k_scenario", r"scenario|escenario"), ("k_opps", r"opportunit|oportunidad")):
            if not re.search(pat, txt, re.I):
                errs.append(L["e_missing"].format(k=L[key]))
        if not re.search(r"current|future|actual|futuro", txt, re.I):
            warns.append(L["w_cf"])
        if len(re.findall(r"^#\s+", txt, re.M)) == 0 and len(re.findall(r"actor\s*:", txt, re.I)) > 1:
            warns.append(L["w_actors"])

    n_ass = len(TAG_ASSUMPTION.findall(txt))
    n_dat = len(TAG_DATA.findall(txt))
    if n_ass or n_dat:
        print(L["tags"].format(d=n_dat, a=n_ass))
    if kind == "persona":
        if n_ass and n_dat == 0 and not re.search(r"proto|hypothesis|hip[oó]tesis", head, re.I):
            warns.append(L["w_proto"])
        says_validated = re.search(r"validated|validad[ao]", head, re.I)
        negated = re.search(r"not validated|unvalidated|no validad|sin validar|proto", head, re.I)
        if n_ass and says_validated and not negated and n_ass / max(1, n_ass + n_dat) > 0.3:
            warns.append(L["w_validated"])
        h1 = len(re.findall(r"^#\s+", txt, re.M))
        print(L["h1"].format(n=h1))
        if h1 > 5:
            warns.append(L["w_many"])
        if not re.search(r"quote|cita|\"", txt, re.I):
            warns.append(L["w_quote"])

    w_label = "WARNING:" if lang == "en" else "AVISO:"
    for e in errs:
        print("ERROR:", e)
    for w in warns:
        print(w_label, w)
    if not errs and not warns:
        print(L["ok"])
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
