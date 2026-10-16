#!/usr/bin/env python3
"""Heuristic moderator scorecard from a transcript with speaker labels (stdlib only).

This is an orientative SELF-assessment, not a performance evaluation of anyone.
Alerts are text heuristics (English and Spanish): they can be wrong and do not replace
listening to the session.

Measures: share of words and turns per speaker, longest turns, interruptions that are
MARKED in the text (e.g. [interrupts], [crosstalk], [se superponen], a trailing dash),
and moderator questions with alerts: possibly closed (yes/no), tag questions that invite
agreement ("right?", "¿verdad?"), possibly loaded or suggestive, options offered
("A or B?"), and turns that stack 3+ questions. It also counts filler/hedge words in the
moderator's turns (descriptive only).

Exit codes: 0 = ok; 2 = error (missing file, no speaker lines, label not found, ...).
"""
import argparse
import os
import re
import sys
from collections import Counter

TS = r"\d{1,2}:\d{2}(?::\d{2})?"
RE_LEAD_TS = re.compile(r"^\s*[\[\(]?(" + TS + r")[\]\)]?\s+(?=\S)")
RE_LINE = re.compile(
    r"^([^\W\d_][^:\n]{0,40}?)(?:\s+[\[\(]?(" + TS + r")[\]\)]?)?\s*:(?:\s+|$)(.*)$"
)
RE_ANNOT = re.compile(r"\[[^\]\n]*\]|\([^)\n]{1,40}\)")
# Interruption / overlap markers, English + Spanish.
#   END marker: this turn was cut off (trailing dash, [interrupted], [cortado]).
#   START marker: this turn interrupts the previous one ([interrupts], [interrumpe], [se pisan]).
#   ANY marker: overlap noted anywhere in the turn ([crosstalk], [overlap], [se superponen]).
RE_CUT_END = re.compile(r"(?:—|–|--)\s*$|\[(?:interrupted|interrumpid[oa]|cut off|cortad[oa])\]\s*$", re.I)
RE_CUT_START = re.compile(r"^\s*\[(?:interrupts|interrupting|talking over|interrumpe|se pisan\w*)\]", re.I)
RE_OVERLAP = re.compile(r"\[(?:cross-?talk|overlap\w*|se superpon\w*)\]", re.I)

CLOSED = re.compile(
    r"^¿?\s*(?:"
    # English
    r"do you|did you|does it|do they|is it|is that|are you|are there|was it|were you|have you|has it|had you|"
    r"can you|could you|would you|will you|should|did it|"
    # Spanish
    r"te result[oó]|le result[oó]|te pareci[oó]|le pareci[oó]|"
    r"es|fue|era|est[aá]|estaba|son|ten[eé]s|tienes|tiene|tuviste|tuvo|us[aá]s|usas|usa|usaste|"
    r"hay|hab[ií]a|pod[eé]s|puedes|puede|pudiste|ha|has|hiciste|hizo|hac[eé]s|conoc[eé]s|conoces|sab[eé]s|sabes|"
    r"te gusta|le gusta|te gust[oó]|le gust[oó]|te sirve|te sirvi[oó]|volver[ií]as|lo usar[ií]as|recomendar[ií]as"
    r")\b", re.I)
TAG = re.compile(
    r"(?:,|\s)\s*¿?\s*(?:right|correct|yeah|ok|okay|no|isn't it|don't you think|you know|"
    r"cierto|verdad|o no|vio|viste|s[ií]|no es cierto)\s*[?¿]\s*$", re.I)
LOADED = re.compile(
    # English
    r"\bdid you (?:find|think|feel) (?:it |that )?(?:very |pretty |quite |too )?"
    r"(?:easy|hard|difficult|confusing|clear|intuitive|annoying|frustrating|useful|slow|fast)\b"
    r"|\b(?:was|is) (?:it|that|this) (?:very |pretty |quite |too )?"
    r"(?:easy|hard|difficult|confusing|clear|intuitive|annoying|frustrating|useful|slow|fast)\b"
    r"|\b(?:don't|wouldn't|isn't|doesn't|aren't) (?:you|it|that|this)\b.*\?"
    r"|\b(?:surely|obviously|clearly|of course|i bet|i assume you|you must have)\b"
    # Spanish
    r"|\b(?:te|le)\s+(?:pareci\w+|result\w+)\s+(?:muy |bastante |algo |tan )?"
    r"(?:f[aá]cil|dif[ií]cil|confus\w+|clar\w+|intuitiv\w+|molest\w+|frustr\w+|[uú]til|lent\w+|r[aá]pid\w+)"
    r"|\bno (?:te|le|crees|cree|piensa|pens[aá]s|piensas)\b.*\?"
    r"|\b(?:seguro que|obviamente|claramente|evidentemente|por supuesto|sin duda)\b", re.I)
OPTIONS = re.compile(r"\b\w+(?: \w+){0,3} (?:o|or) \w+(?: \w+){0,3}\s*\?\s*$", re.I)
FILLER_HEDGE = re.compile(
    r"\b(?:um+|uh+|er+m?|you know|i mean|kind of|sort of|i guess|maybe|"
    r"eh+|em+|o sea|este|digamos|tipo|capaz|quiz[aá]s?|tal vez|creo que)\b", re.I)

MSG = {
    "en": {
        "err_nofile": "input file not found: {p}",
        "err_utf8": "the file is not UTF-8; save it as UTF-8 and try again",
        "err_read": "could not read {p} ({e})",
        "err_noturns": "no 'Speaker: text' lines found in {p}",
        "err_emptymod": "--moderator cannot be empty",
        "err_nolabel": "no label matches --moderator. Labels found: {s}",
        "err_exists": "{p} already exists; use --force or pick another name",
        "err_write": "could not write {p} ({e})",
        "title": "# Moderator scorecard (heuristic)",
        "file": "File: {p} | Session type: {t}",
        "use": "Intended use: self-assessment or coaching you asked for. It is NOT a performance evaluation.",
        "caveat": "Alerts rely on text patterns: they can give false positives and negatives. Listen to the session.",
        "speech_h": "## Speech per speaker",
        "cols": "| Speaker | Words | % words | Turns | % turns | Words per turn |",
        "mod_tag": " (moderator)",
        "read_int": ("Reading: the moderator produces {p:.0f}% of the words. As a practice reference (our heuristic, "
                     "not a norm), in an interview the participant should talk well over half of the time; "
                     "above ~35% check whether you explained too much or filled silences."),
        "read_use": ("Reading: in usability / think-aloud sessions there is silent work on tasks and the moderator talks "
                     "little by design; the moderator's {p:.0f}% of words is NOT compared with an interview goal. "
                     "Look instead at the quality of interventions (below)."),
        "label_warn": ("If speaker labels are wrongly assigned (common in automatic transcripts), these percentages "
                       "invert or distort: check a sample against the audio."),
        "long_h": "## Longest moderator turns (>= {n} words)",
        "long_line": "- line {l}{ts}: {w} words: {x}",
        "none": "- none",
        "longest_mod": "- longest moderator turn: {w} words (line {l})",
        "longest_other": "- longest turn of other speakers: {w} words ({s}, line {l})",
        "cuts_h": "## Interruptions and cut-off turns (only those MARKED in the text)",
        "cut_part": "- Participant cut off and next turn by the moderator: {n}",
        "cut_line": "  - line {a} ({s}) cut off by line {b}",
        "cut_mod": "- Moderator cut off by another speaker: {n}",
        "cut_note": ("(Counts turns ending in a dash/double hyphen or with a marker such as [interrupts] / [crosstalk] / "
                     "[se superponen]. If your tool does not mark overlaps, this stays at 0 even if there were some.)"),
        "q_h": "## Moderator questions",
        "q_total": "- Total questions detected: {n}",
        "q_alerts": "- Questions with alerts: {n}",
        "q_line": "  - line {l}: «{q}» -> {t}",
        "q_more": "  - ... and {n} more",
        "q_stack": ("- Turns with 3 or more questions in a row (the participant usually answers only the last one): "
                    "lines {s}"),
        "q_note": ("A closed question can be right (confirming a fact, closing a topic). Look at the context: the "
                   "alert is a clue to re-listen, not a verdict. Alternatives in ux-interview-guide."),
        "a_closed": "possibly closed (yes/no)",
        "a_tag": "tag question inviting agreement",
        "a_loaded": "possibly loaded/suggestive",
        "a_options": "offers options (may steer)",
        "fill_line": "- Filler/hedge words in moderator turns (descriptive): {n}",
        "qc_h": "## Quality check of this analysis",
        "qc_one": "- There is a single speaker: labels were probably not separated properly.",
        "qc_single": "- Labels with a single turn (possible transcription error): {s}",
        "qc_group": "- There are {n} speakers: if this is a group, read the percentages with care.",
        "qc_audio": "- Did you check the speaker labels against the audio? If not, do it before drawing conclusions.",
        "t_interview": "interview", "t_usability": "usability",
    },
    "es": {
        "err_nofile": "no existe el archivo de entrada: {p}",
        "err_utf8": "el archivo no esta en UTF-8; guardalo como UTF-8 y volve a probar",
        "err_read": "no se pudo leer {p} ({e})",
        "err_noturns": "no encontre lineas con formato 'Hablante: texto' en {p}",
        "err_emptymod": "--moderator no puede estar vacio",
        "err_nolabel": "ninguna etiqueta coincide con --moderator. Etiquetas halladas: {s}",
        "err_exists": "ya existe {p}; usa --force o elegi otro nombre",
        "err_write": "no se pudo escribir {p} ({e})",
        "title": "# Scorecard del moderador (heuristico)",
        "file": "Archivo: {p} | Tipo de sesion: {t}",
        "use": "Uso previsto: autoevaluacion o coaching que vos pediste. NO es una evaluacion de desempeno.",
        "caveat": "Las alertas se basan en patrones de texto: pueden dar falsos positivos y negativos. Escucha la sesion.",
        "speech_h": "## Habla por hablante",
        "cols": "| Hablante | Palabras | % palabras | Turnos | % turnos | Palabras por turno |",
        "mod_tag": " (moderador)",
        "read_int": ("Lectura: el moderador produce {p:.0f}% de las palabras. Como referencia de practica "
                     "(heuristica nuestra, no norma), en una entrevista conviene que el participante hable bastante mas "
                     "que vos; si pasas del ~35%, revisa si explicaste de mas o llenaste silencios."),
        "read_use": ("Lectura: en sesiones de usabilidad/think-aloud hay trabajo silencioso en tareas y el moderador "
                     "habla poco por diseno; el {p:.0f}% de palabras del moderador NO se compara con un objetivo de entrevista. "
                     "Mira mejor la calidad de las intervenciones (abajo)."),
        "label_warn": ("Si las etiquetas de hablante estan mal asignadas (comun en transcripciones automaticas), estos "
                       "porcentajes se invierten o distorsionan: verifica una muestra contra el audio."),
        "long_h": "## Turnos mas largos del moderador (>= {n} palabras)",
        "long_line": "- linea {l}{ts}: {w} palabras: {x}",
        "none": "- ninguno",
        "longest_mod": "- turno mas largo del moderador: {w} palabras (linea {l})",
        "longest_other": "- turno mas largo de otros hablantes: {w} palabras ({s}, linea {l})",
        "cuts_h": "## Interrupciones y turnos cortados (solo las que estan MARCADAS en el texto)",
        "cut_part": "- Participante cortado y siguiente turno del moderador: {n}",
        "cut_line": "  - linea {a} ({s}) cortado por linea {b}",
        "cut_mod": "- Moderador cortado por otro hablante: {n}",
        "cut_note": ("(Cuenta turnos que terminan en raya/guion doble o con marca [interrumpe] / [crosstalk] / "
                     "[se superponen]. Si tu herramienta no marca superposiciones, este numero queda en 0 aunque haya habido.)"),
        "q_h": "## Preguntas del moderador",
        "q_total": "- Total de preguntas detectadas: {n}",
        "q_alerts": "- Preguntas con alerta: {n}",
        "q_line": "  - linea {l}: «{q}» -> {t}",
        "q_more": "  - ... y {n} mas",
        "q_stack": ("- Turnos con 3 o mas preguntas seguidas (el participante suele contestar solo la ultima): "
                    "lineas {s}"),
        "q_note": ("Una pregunta cerrada puede ser correcta (confirmar un dato, cerrar un tema). Mira el contexto: "
                   "la alerta es una pista para reescuchar, no un veredicto. Alternativas en ux-interview-guide."),
        "a_closed": "posible cerrada (si/no)",
        "a_tag": "pregunta con 'cola' que invita a asentir",
        "a_loaded": "posible carga/sugerencia",
        "a_options": "ofrece opciones (puede dirigir)",
        "fill_line": "- Muletillas/atenuadores en turnos del moderador (descriptivo): {n}",
        "qc_h": "## Control de calidad de este analisis",
        "qc_one": "- Hay un unico hablante: las etiquetas probablemente no se separaron bien.",
        "qc_single": "- Etiquetas con un solo turno (posible error de transcripcion): {s}",
        "qc_group": "- Hay {n} hablantes: si es un grupo, interpreta los porcentajes con cuidado.",
        "qc_audio": "- Revisaste las etiquetas de hablante contra el audio? Si no, hacelo antes de sacar conclusiones.",
        "t_interview": "entrevista", "t_usability": "usabilidad",
    },
}
M = MSG["en"]


def fail(key, **kw):
    print("Error: " + M[key].format(**kw), file=sys.stderr)
    sys.exit(2)


def read_lines(path):
    if not os.path.isfile(path):
        fail("err_nofile", p=path)
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read().splitlines()
    except UnicodeDecodeError:
        fail("err_utf8")
    except OSError as e:
        fail("err_read", p=path, e=e.strerror)


def parse(lines):
    turns = []
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        rest, ts = line, None
        m = RE_LEAD_TS.match(line)
        if m:
            ts, rest = m.group(1), line[m.end():]
        mm = RE_LINE.match(rest)
        if mm:
            turns.append({"label": re.sub(r"\s+", " ", mm.group(1)).strip(),
                          "ts": ts or mm.group(2), "text": mm.group(3).strip(), "line": n})
        elif turns:
            turns[-1]["text"] += " " + line
    return turns


def words(text):
    return len(re.findall(r"\w+", RE_ANNOT.sub(" ", text), re.UNICODE))


def questions(text):
    plain = RE_ANNOT.sub(" ", text)
    return [q.strip() for q in re.findall(r"[^?¿.!]*¿?[^?.!]*\?", plain) if q.strip(" ¿?")]


def build_parser():
    ap = argparse.ArgumentParser(
        description="HEURISTIC moderator scorecard: % of words and turns, longest turns, marked interruptions "
                    "and questions with closed / loaded / tag-question alerts, in English and Spanish. "
                    "For self-assessment and requested coaching; NOT for evaluating people's performance.",
        epilog="Exit codes: 0 ok; 2 error. Example: python3 moderator_scorecard.py s01_clean.txt --moderator Moderator")
    ap.add_argument("input", help="transcript .txt/.md with lines 'Speaker: text'")
    ap.add_argument("--moderator", required=True,
                    help="moderator label(s) exactly as they appear, comma-separated (e.g. 'Moderator' or 'Ana,Interviewer')")
    ap.add_argument("--session-type", "--tipo-sesion", dest="session_type",
                    choices=["interview", "usability", "entrevista", "usabilidad"], default="interview",
                    help="in 'usability' (think-aloud) speech share is not compared with an interview goal")
    ap.add_argument("-o", "--output", "--salida", dest="output", help="also save the report to a file")
    ap.add_argument("--force", "--forzar", dest="force", action="store_true", help="allow overwriting the output")
    ap.add_argument("--long-turn", "--largo-turno", dest="long_turn", type=int, default=60,
                    help="words from which a moderator turn is listed as long (default 60, our heuristic)")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="language of the report (default: en)")
    return ap


def main(argv=None):
    global M
    args = build_parser().parse_args(argv)
    M = MSG[args.lang]
    usability = args.session_type in ("usability", "usabilidad")

    turns = parse(read_lines(args.input))
    if not turns:
        fail("err_noturns", p=args.input)
    labels = Counter(t["label"] for t in turns)
    mods = {m.strip().lower() for m in args.moderator.split(",") if m.strip()}
    if not mods:
        fail("err_emptymod")
    real_mods = {e for e in labels if e.lower() in mods}
    if not real_mods:
        fail("err_nolabel", s=", ".join("%s (%d)" % kv for kv in labels.most_common()))
    if args.output and os.path.exists(args.output) and not args.force:
        fail("err_exists", p=args.output)

    wc, tc = Counter(), Counter()
    for t in turns:
        t["w"] = words(t["text"])
        wc[t["label"]] += t["w"]
        tc[t["label"]] += 1
    total_w, total_t = sum(wc.values()) or 1, sum(tc.values())
    is_mod = lambda t: t["label"] in real_mods
    mod_w = sum(wc[e] for e in real_mods)

    out = [M["title"], "",
           M["file"].format(p=args.input, t=M["t_usability"] if usability else M["t_interview"]),
           M["use"], M["caveat"], "",
           M["speech_h"], M["cols"], "|---|---|---|---|---|---|"]
    for e, _ in labels.most_common():
        tag = M["mod_tag"] if e in real_mods else ""
        out.append("| %s%s | %d | %.0f%% | %d | %.0f%% | %.0f |" % (
            e, tag, wc[e], 100.0 * wc[e] / total_w, tc[e], 100.0 * tc[e] / total_t, wc[e] / max(tc[e], 1)))
    out.append("")
    share = 100.0 * mod_w / total_w
    out.append((M["read_use"] if usability else M["read_int"]).format(p=share))
    out.append(M["label_warn"])

    out += ["", M["long_h"].format(n=args.long_turn)]
    long_turns = sorted([t for t in turns if is_mod(t) and t["w"] >= args.long_turn], key=lambda t: -t["w"])[:5]
    for t in long_turns:
        snippet = (t["text"][:100] + "...") if len(t["text"]) > 100 else t["text"]
        out.append(M["long_line"].format(l=t["line"], ts=" [%s]" % t["ts"] if t["ts"] else "", w=t["w"], x=snippet))
    if not long_turns:
        out.append(M["none"])
    mod_turns = [t for t in turns if is_mod(t)]
    longest = max(mod_turns, key=lambda t: t["w"])
    out.append(M["longest_mod"].format(w=longest["w"], l=longest["line"]))
    others = [t for t in turns if not is_mod(t)]
    if others:
        lo = max(others, key=lambda t: t["w"])
        out.append(M["longest_other"].format(w=lo["w"], s=lo["label"], l=lo["line"]))

    out += ["", M["cuts_h"]]
    cuts = {}  # index of the cut-off turn -> turn that cut it
    for i, t in enumerate(turns):
        if i + 1 < len(turns) and RE_CUT_END.search(t["text"]) and turns[i + 1]["label"] != t["label"]:
            cuts.setdefault(i, turns[i + 1])
        if i > 0 and (RE_CUT_START.search(t["text"]) or RE_OVERLAP.search(t["text"])) \
                and turns[i - 1]["label"] != t["label"]:
            cuts.setdefault(i - 1, t)
    pairs = [(turns[i], by) for i, by in sorted(cuts.items())]
    by_mod = [c for c in pairs if is_mod(c[1]) and not is_mod(c[0])]
    to_mod = [c for c in pairs if is_mod(c[0]) and not is_mod(c[1])]
    out.append(M["cut_part"].format(n=len(by_mod)))
    for a, b in by_mod[:8]:
        out.append(M["cut_line"].format(a=a["line"], s=a["label"], b=b["line"]))
    out.append(M["cut_mod"].format(n=len(to_mod)))
    out.append(M["cut_note"])

    out += ["", M["q_h"]]
    all_q = [(t, q) for t in turns if is_mod(t) for q in questions(t["text"])]
    out.append(M["q_total"].format(n=len(all_q)))
    flagged = []
    for t, q in all_q:
        kinds = []
        if CLOSED.search(q):
            kinds.append(M["a_closed"])
        if TAG.search(q):
            kinds.append(M["a_tag"])
        if LOADED.search(q):
            kinds.append(M["a_loaded"])
        if OPTIONS.search(q) and not CLOSED.search(q):
            kinds.append(M["a_options"])
        if kinds:
            flagged.append((t, q, kinds))
    stacked = [t for t in turns if is_mod(t) and len(questions(t["text"])) >= 3]
    out.append(M["q_alerts"].format(n=len(flagged)))
    for t, q, kinds in flagged[:15]:
        out.append(M["q_line"].format(l=t["line"], q=q[:110], t="; ".join(kinds)))
    if len(flagged) > 15:
        out.append(M["q_more"].format(n=len(flagged) - 15))
    if stacked:
        out.append(M["q_stack"].format(s=", ".join(str(t["line"]) for t in stacked[:10])))
    out.append(M["fill_line"].format(n=sum(len(FILLER_HEDGE.findall(RE_ANNOT.sub(" ", t["text"]))) for t in mod_turns)))
    out.append(M["q_note"])

    out += ["", M["qc_h"]]
    if len(labels) == 1:
        out.append(M["qc_one"])
    singles = [e for e, n in labels.items() if n == 1]
    if singles and len(labels) > 2:
        out.append(M["qc_single"].format(s=", ".join(singles)))
    if len(labels) > 2:
        out.append(M["qc_group"].format(n=len(labels)))
    out.append(M["qc_audio"])
    text = "\n".join(out)
    print(text)
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError as e:
            fail("err_write", p=args.output, e=e.strerror)


if __name__ == "__main__":
    main()
