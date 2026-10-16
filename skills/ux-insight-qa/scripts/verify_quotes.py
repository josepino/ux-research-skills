#!/usr/bin/env python3
"""Verify that the verbatim quotes in a report appear in the transcripts.

Usage:
  python3 verify_quotes.py --report report.md --transcripts folder/
  python3 verify_quotes.py --report report.md --transcripts p1.txt p2.md --min-words 5 --threshold 0.85 [--lang es]

How it works (standard library only):
  1. Extracts text between quotation marks (curly, straight or guillemets) with at least N words.
  2. Normalizes report and transcripts: lowercase, no accents, no punctuation, simple filler
     words removed (English: um, uh, er, erm, hmm, mhm...; Spanish: ehh, mmm, eh, ah...),
     whitespace collapsed.
  3. Looks up each quote: normalized exact match = verified; otherwise the most similar
     window of text (difflib) with similarity >= threshold = approximate; otherwise not
     found (the closest match is shown as a hint). Quotes with "[...]" or "..." are checked
     fragment by fragment.

A "not found" quote is NOT an accusation: a transcript may be missing, or the quote may be a
translation, a paraphrase or come from another source. The person decides.

Spanish flags still work as aliases: --informe, --transcripciones, --min-palabras, --umbral.

Exit codes: 0 all verified/approximate; 1 some quotes not found; 2 usage or input error
(missing file, empty folder, bad option); 130 interrupted.
"""
import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path

# Bilingual fillers: es: ehh, emm, mmm, ahh, eeh ; en: um, umm, uh, uhh, er, erm, hmm, mhm
FILLER = re.compile(r"^(?:e+h+m*|e+m+|e+r+m*|h?m+h*m*|a+h+|u+h+m*|u+m+|h+m+)$")
EXTENSIONS = {".txt", ".md", ".markdown"}
PAIRS = [("«", "»"), ("“", "”")]
ELLIPSIS_SPLIT = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…")

MSG = {
    "en": {
        "read_err": "could not read '{p}': {e}",
        "missing": "'{p}' does not exist.",
        "no_files": "no transcripts (.txt or .md) found in the given paths; the folder is empty or has no such formats.",
        "empty_tr": "the transcripts are empty.",
        "bad_min": "--min-words must be 1 or more.",
        "bad_thr": "--threshold must be between 0 and 1.",
        "no_report": "report '{p}' does not exist.",
        "header": "Report: {r} | transcripts: {n} file(s) | minimum {w} words | approximate threshold {t:.2f}\n",
        "no_quotes": "No quotes of {w} words or more found between quotation marks. Try a lower --min-words or check that quotes use « », “ ” or \" \".",
        "item": "[{i}] (report, line {l}) «{q}»",
        "verified": "    VERIFIED in {f}, line {l} (matches after normalizing accents, punctuation and fillers)",
        "approx": "    APPROXIMATE in {f}, line {l} (similarity {s:.2f})",
        "says": "    Transcript says (normalized): {c}",
        "check": "    Check whether the difference is light cleanup or a change of meaning.",
        "nf_close": "    NOT FOUND. Closest: {f}, line {l} (similarity {s:.2f})",
        "nf_none": "    NOT FOUND. Nothing similar in the given transcripts.",
        "causes": "    Possible causes: that transcript is missing, it is a translation or paraphrase, it comes from notes (not the recording) or it was altered. The person decides.",
        "summary": "Summary: {v} verified, {a} approximate, {n} not found out of {t} quote(s).",
        "d_report": "report in .md or .txt",
        "d_tr": "folder and/or .txt/.md files with the transcripts",
        "d_min": "minimum quote length to verify, in words (default 6)",
        "d_thr": "minimum similarity (0-1) to count as 'approximate' (default 0.85)",
        "d_lang": "language of the output messages",
        "desc": "Verify that the quoted passages of a report appear in the transcripts.",
        "epilog": "Flags, does not accuse: a quote not found is something to review, not a verdict.",
        "err": "Error: {m}",
    },
    "es": {
        "read_err": "no pude leer «{p}»: {e}",
        "missing": "no existe «{p}».",
        "no_files": "no encontré transcripciones (.txt o .md) en las rutas indicadas; la carpeta está vacía o sin esos formatos.",
        "empty_tr": "las transcripciones están vacías.",
        "bad_min": "--min-words debe ser 1 o más.",
        "bad_thr": "--threshold debe estar entre 0 y 1.",
        "no_report": "no existe el informe «{p}».",
        "header": "Informe: {r} | transcripciones: {n} archivo(s) | mínimo {w} palabras | umbral aproximada {t:.2f}\n",
        "no_quotes": "No encontré citas de {w} palabras o más entre comillas. Probá con --min-words menor o revisá que las citas estén entre « », “ ” o \" \".",
        "item": "[{i}] (informe, línea {l}) «{q}»",
        "verified": "    VERIFICADA en {f}, línea {l} (coincide tras normalizar tildes, puntuación y muletillas)",
        "approx": "    APROXIMADA en {f}, línea {l} (similitud {s:.2f})",
        "says": "    Transcripción dice (normalizado): {c}",
        "check": "    Revisá si la diferencia es limpieza leve o un cambio de sentido.",
        "nf_close": "    NO ENCONTRADA. Lo más cercano: {f}, línea {l} (similitud {s:.2f})",
        "nf_none": "    NO ENCONTRADA. No hay nada parecido en las transcripciones dadas.",
        "causes": "    Posibles causas: falta esa transcripción, es traducción o paráfrasis, viene de notas (no de la grabación) o fue modificada. Lo decide la persona.",
        "summary": "Resumen: {v} verificada(s), {a} aproximada(s), {n} no encontrada(s) de {t} cita(s).",
        "d_report": "informe en .md o .txt",
        "d_tr": "carpeta y/o archivos .txt/.md con las transcripciones",
        "d_min": "largo mínimo de una cita a verificar, en palabras (default 6)",
        "d_thr": "similitud mínima (0-1) para considerar «aproximada» (default 0.85)",
        "d_lang": "idioma de los mensajes de salida",
        "desc": "Verifica que las citas entre comillas de un informe aparezcan en las transcripciones.",
        "epilog": "Señala, no acusa: una cita no encontrada es algo para revisar, no un veredicto.",
        "err": "Error: {m}",
    },
}
M = MSG["en"]


def fail(msg):
    print(M["err"].format(m=msg), file=sys.stderr)
    sys.exit(2)


def read_text(path):
    try:
        data = Path(path).read_bytes()
    except OSError as e:
        fail(M["read_err"].format(p=path, e=e.strerror or e))
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def tokens(text):
    """Normalized words (lowercase, no accents, no punctuation, no fillers)."""
    t = unicodedata.normalize("NFD", text.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^\w\s]|_", " ", t)
    return [w for w in t.split() if not FILLER.match(w)]


def extract_quotes(text, min_words):
    """List of (line, original quote) with at least min_words words."""
    found = []
    for op, cl in PAIRS:
        for m in re.finditer(re.escape(op) + r"(.{1,800}?)" + re.escape(cl), text, re.S):
            found.append((m.start(), m.group(1)))
    for m in re.finditer(r'"([^"\n]{1,800}?)"', text):
        found.append((m.start(), m.group(1)))
    found.sort()
    out, seen = [], set()
    for pos, quote in found:
        clean = " ".join(quote.split())
        if len(tokens(clean)) < min_words or clean in seen:
            continue
        seen.add(clean)
        out.append((text.count("\n", 0, pos) + 1, clean))
    return out


def load_transcripts(paths):
    files = []
    for r in paths:
        p = Path(r)
        if not p.exists():
            fail(M["missing"].format(p=r))
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in EXTENSIONS)
        else:
            files.append(p)
    if not files:
        fail(M["no_files"])
    corpus = []  # (name, [tokens], [line of each token])
    for f in files:
        toks, lines = [], []
        for n, line in enumerate(read_text(f).splitlines(), 1):
            for w in tokens(line):
                toks.append(w)
                lines.append(n)
        if toks:
            corpus.append((f.name, toks, lines))
    if not corpus:
        fail(M["empty_tr"])
    return corpus


def best_match(frag, corpus):
    """Best match for a fragment (token list) -> (similarity, file, line, text)."""
    n = len(frag)
    target = " ".join(frag)
    best = (0.0, "", 0, "")
    for name, toks, lines in corpus:
        text = " ".join(toks)
        i = text.find(target)
        if i != -1 and (i == 0 or text[i - 1] == " ") and (i + len(target) == len(text) or text[i + len(target)] == " "):
            idx = text[:i].count(" ") if i else 0
            return (1.0, name, lines[idx], target)
        sm = difflib.SequenceMatcher(None, autojunk=False)
        sm.set_seq2(target)
        sizes = sorted({max(1, int(n * f)) for f in (0.8, 0.9, 1.0, 1.1, 1.25)})
        for size in sizes:
            for s in range(0, max(1, len(toks) - size + 1)):
                window = " ".join(toks[s:s + size])
                sm.set_seq1(window)
                if sm.real_quick_ratio() <= best[0] or sm.quick_ratio() <= best[0]:
                    continue
                r = sm.ratio()
                if r > best[0]:
                    best = (r, name, lines[s], window)
    return best


def verify(quote, corpus, threshold):
    """-> (status, similarity, file, line, closest text)"""
    frags = [tokens(f) for f in ELLIPSIS_SPLIT.split(quote)]
    frags = [f for f in frags if len(f) >= 3]
    if not frags:
        frags = [tokens(quote)]
    worst = None
    for f in frags:
        res = best_match(f, corpus)
        if worst is None or res[0] < worst[0]:
            worst = res
    sim, fname, line, text = worst
    if sim >= 0.9999:
        return ("verified", 1.0, fname, line, text)
    if sim >= threshold:
        return ("approximate", sim, fname, line, text)
    return ("not_found", sim, fname, line, text)


def main():
    global M
    lang = "en"
    if "--lang" in sys.argv:
        i = sys.argv.index("--lang")
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in MSG:
            lang = sys.argv[i + 1]
    M = MSG[lang]
    ap = argparse.ArgumentParser(description=M["desc"], epilog=M["epilog"])
    ap.add_argument("--report", "--informe", dest="report", required=True, help=M["d_report"])
    ap.add_argument("--transcripts", "--transcripciones", dest="transcripts", required=True, nargs="+", help=M["d_tr"])
    ap.add_argument("--min-words", "--min-palabras", dest="min_words", type=int, default=6, help=M["d_min"])
    ap.add_argument("--threshold", "--umbral", dest="threshold", type=float, default=0.85, help=M["d_thr"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=M["d_lang"])
    a = ap.parse_args()

    if a.min_words < 1:
        fail(M["bad_min"])
    if not 0 < a.threshold <= 1:
        fail(M["bad_thr"])
    if not Path(a.report).is_file():
        fail(M["no_report"].format(p=a.report))

    report = read_text(a.report)
    corpus = load_transcripts(a.transcripts)
    quotes = extract_quotes(report, a.min_words)
    print(M["header"].format(r=a.report, n=len(corpus), w=a.min_words, t=a.threshold))
    if not quotes:
        print(M["no_quotes"].format(w=a.min_words))
        return 0

    count = {"verified": 0, "approximate": 0, "not_found": 0}
    for i, (line, quote) in enumerate(quotes, 1):
        status, sim, fname, ln, close = verify(quote, corpus, a.threshold)
        count[status] += 1
        short = quote if len(quote) <= 90 else quote[:87] + "..."
        print(M["item"].format(i=i, l=line, q=short))
        if status == "verified":
            print(M["verified"].format(f=fname, l=ln))
        elif status == "approximate":
            print(M["approx"].format(f=fname, l=ln, s=sim))
            print(M["says"].format(c=close))
            print(M["check"])
        else:
            if sim >= 0.5:
                print(M["nf_close"].format(f=fname, l=ln, s=sim))
                print(M["says"].format(c=close))
            else:
                print(M["nf_none"])
            print(M["causes"])
        print()
    print(M["summary"].format(v=count["verified"], a=count["approximate"], n=count["not_found"], t=len(quotes)))
    return 1 if count["not_found"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
