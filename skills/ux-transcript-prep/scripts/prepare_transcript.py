#!/usr/bin/env python3
"""Clean a research transcript for analysis (Python 3 standard library only).

Input: a txt/md file with lines "Speaker: text", with optional timestamps at the
start or next to the label ([00:01:23] Ana: hi / Ana 00:01:23: hi / 00:01:23 Ana: hi).
Lines without a speaker label are treated as a continuation of the previous turn.

Guarantees:
  * Text inside quotes ("...", curly quotes, guillemets) and short annotations such as
    [laughs] / (pause) is never touched.
  * Content words are never changed. Possible transcription errors are FLAGGED in the
    report, not corrected.
  * Before writing, the script re-checks that every quoted passage is byte-identical;
    if not, it aborts and writes nothing.

Bilingual (English and Spanish):
  * Sound fillers removed with --strip-fillers: um, uh, er, erm, hmm, mm (English) and
    eh, em, mm, hmm (Spanish). Words that can carry meaning are NOT removed by default.
  * Discourse fillers (you know, I mean, like, o sea, este, bueno, ¿vio?...) are removed
    only with --strip-discourse-fillers (conservative: only when set off by commas) or by
    name with --extra-fillers.
  * Hedges (I guess, maybe, kind of / creo que, tal vez, más o menos...) are NEVER removed;
    the report only counts them, because uncertainty is data.
  * Interruption/overlap markers are recognized in both languages.

Column names of the speaker map CSV: 'original,normalized' (the Spanish names
'original,normalizado' are accepted as aliases).

Exit codes: 0 = ok; 2 = error (missing file, bad CSV, no speaker lines, output exists, ...).
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter

TS = r"\d{1,2}:\d{2}(?::\d{2})?"
RE_LEAD_TS = re.compile(r"^\s*[\[\(]?(" + TS + r")[\]\)]?\s+(?=\S)")
RE_LINE = re.compile(
    r"^([^\W\d_][^:\n]{0,40}?)(?:\s+[\[\(]?(" + TS + r")[\]\)]?)?\s*:(?:\s+|$)(.*)$"
)
RE_INLINE_TS = re.compile(r"[\[\(]" + TS + r"[\]\)]")
RE_PROTECT = re.compile(
    r'("[^"\n]*"|“[^”\n]*”|«[^»\n]*»|\[[^\]\n]*\]|\([^)\n]{1,40}\))'
)
RE_QUOTE = re.compile(r'("[^"\n]*"|“[^”\n]*”|«[^»\n]*»)')

# Sound fillers only (hesitation noises with no content), English + Spanish.
FILLER = re.compile(
    r"\b(?:e+h+m*|e+m+|e+r+m*|h?m{2,}|hm+|u+h+m*|u+m+|a+h+m+)\b,?[ \t]*", re.IGNORECASE
)

# Discourse fillers: opt-in and conservative. Each needs punctuation around it so that
# content uses ("I like it", "este proyecto", "bueno para mí") are left alone.
DISCOURSE = [
    # English: set off by a trailing comma
    re.compile(r"\b(?:you know|i mean|like|kind of|sort of|basically|you see)\b,[ \t]*", re.I),
    # English: trailing "you know" after a comma
    re.compile(r",[ \t]*you know(?=[ \t]*[.?!]|$)", re.I),
    # Spanish: set off by a trailing comma or ellipsis
    re.compile(r"\b(?:o sea|este|bueno|digamos|tipo|a ver|mir[aá]|dale)\b(?:,|\.\.\.|…)[ \t]*", re.I),
    # Spanish tag questions after a comma: ", ¿vio?" ", ¿viste?" ", ¿sabés?"
    re.compile(r",[ \t]*¿?(?:vio|viste|sab[eé]s|entend[eé]s|entiendes|cierto)\?", re.I),
]

# Hedges and uncertainty markers: counted in the report, never removed.
HEDGES = re.compile(
    r"\b(?:i guess|i think|i suppose|maybe|perhaps|probably|kind of|sort of|i'm not sure|not sure|"
    r"creo que|supongo|quiz[aá]s?|tal vez|capaz|a lo mejor|m[aá]s o menos|me parece|no s[eé]|"
    r"no estoy seguro|no estoy segura|como que)\b", re.I)

REVIEW = re.compile(
    r"\[(?:inaudible|ininteligible|unintelligible|illegible|\?)[^\]]*\]|\?\?\?", re.I)
RE_REPEAT = re.compile(r"\b(\w{2,})\s+\1\b", re.IGNORECASE)

MSG = {
    "en": {
        "err_nofile": "input file not found: {p}",
        "err_utf8": "the file is not UTF-8; save it as UTF-8 and try again: {p}",
        "err_read": "could not read {p} ({e})",
        "err_nomapfile": "speaker CSV not found: {p}",
        "err_mapread": "could not read the speaker CSV ({e})",
        "err_mapcols": "the speaker CSV needs a header 'original,normalized' and at least one row",
        "err_noturns": "no 'Speaker: text' lines found in {p}. Check that each turn starts with the label followed by a colon.",
        "err_same": "the output cannot be the input file (the original is never overwritten)",
        "err_exists": "{p} already exists; use --force to overwrite it or pick another name with -o",
        "err_quotes": "internal check failed: this would change text inside quotes. Nothing was written.",
        "err_write": "could not write {p} ({e})",
        "err_report": "could not write the report ({e})",
        "title": "# Preparation report",
        "input": "Input: {p}", "output": "Output: {p}",
        "turns_in": "- Turns in the input: {n}", "turns_out": "- Turns in the output: {n}",
        "speakers_in": "- Speakers in the input: {s}",
        "pre": "- Lines before the first speaker (kept as is): {n}",
        "quotes_ok": "- Quoted passages verified unchanged: {n}",
        "labels_changed": "- Speaker labels changed: {n}",
        "unmapped": "- WARNING, labels with no entry in the map (left as they were): {s}",
        "ts_removed": "- Timestamps removed: {a} (turn level) + {b} (inside text)",
        "fillers_removed": "- Fillers removed: {s}", "none": "none",
        "merged": "- Turns merged: {n}",
        "hedges": "- Hedges / uncertainty markers present (KEPT, they are data): {s}",
        "review_h": "## For a person to review (nothing was corrected)",
        "r_audio": "line {l} ({s}): doubtful audio marker (inaudible/???) -> check against the audio",
        "r_repeat": "line {l} ({s}): repeated word '{w} {w}' -> may be real stammering; not touched",
        "r_none": "(nothing flagged automatically)",
        "r_rare": "- Labels with a single turn (possible labeling error): {s}",
        "reminder1": "Reminder: this is mechanical cleaning. Check a sample against the audio before analyzing,",
        "reminder2": "and keep the original file untouched.",
    },
    "es": {
        "err_nofile": "no existe el archivo de entrada: {p}",
        "err_utf8": "el archivo no esta en UTF-8; guardalo como UTF-8 y volve a probar: {p}",
        "err_read": "no se pudo leer {p} ({e})",
        "err_nomapfile": "no existe el CSV de hablantes: {p}",
        "err_mapread": "no se pudo leer el CSV de hablantes ({e})",
        "err_mapcols": "el CSV de hablantes necesita encabezado 'original,normalizado' y al menos una fila",
        "err_noturns": "no encontre lineas con formato 'Hablante: texto' en {p}. Revisa que cada turno empiece con la etiqueta seguida de dos puntos.",
        "err_same": "la salida no puede ser el archivo de entrada (no se sobrescribe el original)",
        "err_exists": "ya existe {p}; usa --force para sobrescribirlo o elegi otro con -o",
        "err_quotes": "verificacion interna fallida: cambiaria texto entre comillas. No se escribio nada.",
        "err_write": "no se pudo escribir {p} ({e})",
        "err_report": "no se pudo escribir el informe ({e})",
        "title": "# Informe de preparacion",
        "input": "Entrada: {p}", "output": "Salida: {p}",
        "turns_in": "- Turnos en la entrada: {n}", "turns_out": "- Turnos en la salida: {n}",
        "speakers_in": "- Hablantes en la entrada: {s}",
        "pre": "- Lineas previas al primer hablante (conservadas tal cual): {n}",
        "quotes_ok": "- Citas entre comillas verificadas sin cambios: {n}",
        "labels_changed": "- Etiquetas de hablante cambiadas: {n}",
        "unmapped": "- ATENCION, etiquetas sin entrada en el mapa (quedaron como estaban): {s}",
        "ts_removed": "- Marcas de tiempo quitadas: {a} (de turno) + {b} (dentro del texto)",
        "fillers_removed": "- Muletillas quitadas: {s}", "none": "ninguna",
        "merged": "- Turnos unidos: {n}",
        "hedges": "- Atenuadores / marcas de incertidumbre presentes (CONSERVADOS, son datos): {s}",
        "review_h": "## A revisar por una persona (no se corrigio nada)",
        "r_audio": "linea {l} ({s}): marca de audio dudoso (inaudible/???) -> revisar contra el audio",
        "r_repeat": "linea {l} ({s}): palabra repetida '{w} {w}' -> puede ser tartamudeo real; no se toco",
        "r_none": "(nada marcado automaticamente)",
        "r_rare": "- Etiquetas con un solo turno (posible error de etiquetado): {s}",
        "reminder1": "Recordatorio: esto es limpieza mecanica. Revisa una muestra contra el audio antes de analizar,",
        "reminder2": "y conserva el archivo original sin tocar.",
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
        fail("err_utf8", p=path)
    except OSError as e:
        fail("err_read", p=path, e=e.strerror)


def parse(lines):
    """Return (preamble, turns). Turn = dict(label, ts, text, line)."""
    pre, turns = [], []
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        lead_ts = None
        m = RE_LEAD_TS.match(line)
        rest = line
        if m:
            lead_ts, rest = m.group(1), line[m.end():]
        mm = RE_LINE.match(rest)
        if mm:
            label = re.sub(r"\s+", " ", mm.group(1)).strip()
            turns.append({"label": label, "ts": lead_ts or mm.group(2),
                          "text": mm.group(3).strip(), "line": n})
        elif turns:
            turns[-1]["text"] = (turns[-1]["text"] + " " + line).strip()
        else:
            pre.append(line)
    return pre, turns


def read_map(path):
    """Speaker map CSV. Canonical header: original,normalized (alias: normalizado)."""
    if not os.path.isfile(path):
        fail("err_nomapfile", p=path)
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
            cols = [c.strip().lower() for c in (rows and rows[0].keys() or []) if c]
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        fail("err_mapread", e=e)
    norm_col = "normalized" if "normalized" in cols else "normalizado"
    if not rows or "original" not in cols or norm_col not in cols:
        fail("err_mapcols")
    mapping = {}
    for row in rows:
        r2 = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
        if r2.get("original") and r2.get(norm_col):
            mapping[r2["original"].lower()] = r2[norm_col]
    return mapping


def apply_outside_protected(text, fn):
    """Apply fn only to the NOT protected stretches (outside quotes/annotations)."""
    parts = RE_PROTECT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = fn(parts[i])
    return "".join(parts)


def clean_text(text, args, counter):
    def mark(seg, m):
        """Return a sentinel when the removed filler opened a sentence (so the next word can be capitalized)."""
        before = seg[:m.start()].rstrip()
        return "\x00" if before and before[-1] in ".?!" else ""

    def strip(seg):
        if args.strip_fillers:
            def rep(m):
                counter["filler:" + re.sub(r"[, \t]+$", "", m.group(0)).lower()] += 1
                return mark(seg, m)
            seg = FILLER.sub(rep, seg)
        if args.strip_discourse_fillers:
            for rx in DISCOURSE:
                def rep2(m):
                    counter["filler:" + re.sub(r"^[, \t¿]+|[, \t?.…]+$", "", m.group(0)).lower()] += 1
                    # a removed tag question ", ¿vio?" may have been closing the sentence: keep a period
                    if m.group(0).rstrip().endswith("?") and re.match(r"\s*(?:[A-ZÁÉÍÓÚÑ¿¡]|$)", m.string[m.end():]):
                        return "."
                    return ""
                seg = rx.sub(rep2, seg)
        for extra in args.extras:
            pat = re.compile(r"\b" + re.escape(extra) + r"\b,?[ \t]*", re.IGNORECASE)
            seg, k = pat.subn("", seg)
            counter["filler:" + extra] += k
        if args.strip_timestamps:
            seg, k = RE_INLINE_TS.subn("", seg)
            counter["inline_timestamps"] += k
        return seg

    new = apply_outside_protected(text, strip)
    new = re.sub(r"\x00\s*([^\W\d_])", lambda m: m.group(1).upper(), new)
    new = new.replace("\x00", "")
    new = re.sub(r"[ \t]{2,}", " ", new)
    new = re.sub(r"\s+([,;])", r"\1", new)
    new = re.sub(r",\s*,", ",", new).strip()
    new = re.sub(r"^[,;\s]+", "", new)
    if new != text and new[:1].islower() and text[:1].isupper():
        new = new[:1].upper() + new[1:]
    return new


def build_parser():
    ap = argparse.ArgumentParser(
        description="Clean a 'Speaker: text' transcript for analysis. Never modifies text inside quotes or "
                    "annotations such as [laughs]/(pause). Possible errors are flagged in the report, "
                    "never corrected silently. English and Spanish fillers/markers supported.",
        epilog="Exit codes: 0 ok; 2 error. Example: python3 prepare_transcript.py s01.txt --strip-fillers "
               "--strip-timestamps --normalize-speakers speakers.csv -o s01_clean.txt")
    ap.add_argument("input", help="file .txt/.md with lines 'Speaker: text'")
    ap.add_argument("-o", "--output", help="output file (default <input>_clean.<ext>)")
    ap.add_argument("--strip-fillers", "--quitar-muletillas", dest="strip_fillers", action="store_true",
                    help="remove sound fillers only (um, uh, er, hmm, mm / eh, em, mm); does NOT touch words like "
                         "'like', 'you know', 'o sea', 'este'")
    ap.add_argument("--strip-discourse-fillers", dest="strip_discourse_fillers", action="store_true",
                    help="also remove discourse fillers when set off by commas (you know, I mean, like, o sea, "
                         "este, bueno, ¿vio?...). Use consciously: they can signal evasion or uncertainty")
    ap.add_argument("--extra-fillers", "--muletillas-extra", dest="extra_fillers", default="",
                    help="comma-separated list of extra words to remove by name (conscious use; e.g. 'o sea,you know')")
    ap.add_argument("--strip-timestamps", "--quitar-tiempos", dest="strip_timestamps", action="store_true",
                    help="remove timestamps")
    ap.add_argument("--normalize-speakers", "--normalizar-hablantes", dest="normalize_speakers", metavar="MAP.CSV",
                    help="CSV with header 'original,normalized' to unify labels")
    ap.add_argument("--merge-turns", "--unir-turnos", dest="merge_turns", action="store_true",
                    help="merge consecutive turns by the same speaker (after normalizing)")
    ap.add_argument("--report", "--informe", dest="report", metavar="FILE",
                    help="also save the report to a file")
    ap.add_argument("--force", "--forzar", dest="force", action="store_true",
                    help="allow overwriting the output if it exists")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="language of the report (default: en)")
    return ap


def main(argv=None):
    global M
    args = build_parser().parse_args(argv)
    M = MSG[args.lang]
    args.extras = [e.strip() for e in args.extra_fillers.split(",") if e.strip()]

    lines = read_lines(args.input)
    pre, turns = parse(lines)
    if not turns:
        fail("err_noturns", p=args.input)

    base, ext = os.path.splitext(args.input)
    out_path = args.output or (base + "_clean" + (ext or ".txt"))
    if os.path.abspath(out_path) == os.path.abspath(args.input):
        fail("err_same")
    if os.path.exists(out_path) and not args.force:
        fail("err_exists", p=out_path)

    mapping = read_map(args.normalize_speakers) if args.normalize_speakers else {}
    counter = Counter()
    originals = Counter(t["label"] for t in turns)
    unmapped = set()
    quotes_before = [q for t in turns for q in RE_QUOTE.findall(t["text"])]
    hedge_count = Counter()
    for t in turns:
        for h in HEDGES.findall(t["text"]):
            hedge_count[h.lower()] += 1

    for t in turns:
        if mapping:
            new = mapping.get(t["label"].lower())
            if new:
                if new != t["label"]:
                    counter["labels_changed"] += 1
                t["label"] = new
            else:
                unmapped.add(t["label"])
        t["text"] = clean_text(t["text"], args, counter)
        if args.strip_timestamps:
            if t["ts"]:
                counter["timestamps_removed"] += 1
            t["ts"] = None

    if args.merge_turns:
        merged = []
        for t in turns:
            if merged and merged[-1]["label"] == t["label"]:
                merged[-1]["text"] = (merged[-1]["text"] + " " + t["text"]).strip()
                counter["merged"] += 1
            else:
                merged.append(dict(t))
        turns = merged

    quotes_after = [q for t in turns for q in RE_QUOTE.findall(t["text"])]
    if quotes_before != quotes_after:
        fail("err_quotes")

    out_lines = list(pre)
    for t in turns:
        ts = "[%s] " % t["ts"] if t["ts"] else ""
        out_lines.append("%s%s: %s" % (ts, t["label"], t["text"]))
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")
    except OSError as e:
        fail("err_write", p=out_path, e=e.strerror)

    review = []
    for t in turns:
        if REVIEW.search(t["text"]):
            review.append(M["r_audio"].format(l=t["line"], s=t["label"]))
        for m in RE_REPEAT.finditer(t["text"]):
            review.append(M["r_repeat"].format(l=t["line"], s=t["label"], w=m.group(1)))
    labels = Counter(t["label"] for t in turns)
    rare = [e for e, n in labels.items() if n == 1 and len(labels) > 2]

    out = [M["title"], "", M["input"].format(p=args.input), M["output"].format(p=out_path), "",
           M["turns_in"].format(n=sum(originals.values())),
           M["turns_out"].format(n=len(turns)),
           M["speakers_in"].format(s=", ".join("%s (%d)" % kv for kv in originals.most_common())),
           M["pre"].format(n=len(pre)),
           M["quotes_ok"].format(n=len(quotes_after))]
    if mapping:
        out.append(M["labels_changed"].format(n=counter["labels_changed"]))
        if unmapped:
            out.append(M["unmapped"].format(s=", ".join(sorted(unmapped))))
    if args.strip_timestamps:
        out.append(M["ts_removed"].format(a=counter["timestamps_removed"], b=counter["inline_timestamps"]))
    removed = {k[len("filler:"):]: v for k, v in counter.items() if k.startswith("filler:")}
    if args.strip_fillers or args.strip_discourse_fillers or args.extras:
        out.append(M["fillers_removed"].format(
            s=", ".join("%s x%d" % kv for kv in sorted(removed.items())) or M["none"]))
    if args.merge_turns:
        out.append(M["merged"].format(n=counter["merged"]))
    if hedge_count:
        out.append(M["hedges"].format(s=", ".join("%s x%d" % kv for kv in hedge_count.most_common(8))))
    out += ["", M["review_h"]]
    out += ["- " + r for r in review] or ["- " + M["r_none"]]
    if rare:
        out.append(M["r_rare"].format(s=", ".join(rare)))
    out += ["", M["reminder1"], M["reminder2"]]
    text = "\n".join(out)
    print(text)
    if args.report:
        try:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError as e:
            fail("err_report", e=e.strerror)


if __name__ == "__main__":
    main()
