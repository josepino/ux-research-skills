#!/usr/bin/env python3
"""Lint interview or survey questions and flag typical wording problems.

Single source of the logic: used by ux-interview-guide and called by
ux-ethics-bias-review (which ships a thin wrapper that runs this same file).

Heuristic, regex based, and bilingual: the rules cover English AND Spanish
(Rioplatense and neutral) wording. Confirm every alert by eye; a flag is a
prompt to look again, not a verdict.

Checks: closed (yes/no), hypothetical or prediction, generic or absolute words
("usually", "always", "everyone"), leading or value-loaded wording, presupposed
positive experience, price anchoring, possible double-barreled question, jargon,
and very long questions.

Input: a UTF-8 text file, one question per line (bullets and numbering are
ignored), or '-' for stdin. Output language: --lang en|es (default en).

Exit codes: 0 = ran fine (alerts or not); 1 = alerts found and --strict was
given; 2 = bad input (missing file, unreadable file, no questions).
"""
import argparse
import re
import sys

# Each rule: (key, regex). Keys map to the labels in LABELS below.
# Closed questions are handled apart because open openers cancel them.
RULES = [
    ("hypothetical",
     # English
     r"\bwould you (?:use|buy|pay|purchase|recommend|switch|consider|like|want|try|subscribe|download|prefer)\b"
     r"|\bwould you ever\b|\bhow likely\b|\bhow probable\b|\bif you (?:had|were|could|have)\b"
     r"|\bif (?:it|this|we|there) (?:existed|were|was|had)\b|\bin the future\b|\bwill you (?:use|buy|pay)\b"
     r"|\bimagine (?:that |if |you)\b|\bsuppose\b|\bhypothetically\b|\bdo you think you(?:'d| would| will)\b"
     # Spanish
     r"|\b(?:usar[ií]as|comprar[ií]as|pagar[ií]as|recomendar[ií]as|cambiar[ií]as|probar[ií]as|considerar[ií]as"
     r"|te gustar[ií]a|ser[ií]as|descargar[ií]as|contratar[ií]as|elegir[ií]as)\b"
     r"|\bcrees que (?:vas|va) a\b|\bqu[eé] tan probable\b|\bsi tuvieras\b|\bsi existiera\b|\bsi pudieras\b"
     r"|\ben el futuro\b|\bimagin[aá]\b|\bsupone(?:r|mos)?\b|\bhipot[eé]ticamente\b"),
    ("absolute",
     r"\b(?:usually|normally|generally|typically|habitually|always|never|everyone|everybody|nobody|no one"
     r"|all the time|in general|as a rule|most of the time|on a regular basis)\b"
     r"|\b(?:normalmente|generalmente|habitualmente|usualmente|siempre|nunca|jam[aá]s|todos|nadie"
     r"|todo el tiempo|en general|por lo general|de costumbre|la mayor[ií]a de las veces)\b"),
    ("leading",
     # English: loaded adjectives, tag questions, assumed opinions
     r"\b(?:beautiful|gorgeous|ugly|terrible|awful|horrible|amazing|awesome|great|wonderful|fantastic|excellent"
     r"|confusing|intuitive|annoying|frustrating|clunky|slick|sad|happy)\b"
     r"|\b(?:don't|doesn't|wouldn't|isn't|aren't|didn't|shouldn't|couldn't) (?:you|it|that|this|they)\b"
     r"|\byou(?:'d| would) (?:agree|say)\b|\bobviously\b|\bclearly\b|\bof course\b|\bsurely\b"
     r"|,\s*(?:right|correct|isn't it|don't you|no)\s*\?\s*$|\bwhat's (?:so )?(?:good|great|nice|beautiful) about\b"
     r"|\bhow (?:easy|difficult|hard|great|annoying|frustrating|useful)\b"
     # Spanish
     r"|\b(?:hermos[oa]|horrible|incre[ií]ble|molest[oa]|frustr\w+|genial|excelente|maravillos[oa]"
     r"|terrible|lind[oa]|fe[oa]|confus[oa]|intuitiv[oa]|triste|feliz)\b"
     r"|\bno (?:crees|cree|piensas|piensa|pens[aá]s|te parece|le parece)\b|\bverdad\s*\?|\bqu[eé] tan (?:f[aá]cil|dif[ií]cil|[uú]til)\b"
     r"|\bobviamente\b|\bclaramente\b|\bpor supuesto\b|\bseguro que\b|\bqu[eé] tiene de (?:bueno|bello|hermos\w+|lindo)\b"
     r"|(?<!\w)no\s*\?\s*$"),
    ("positive_presupposition",
     r"\bwhy do you (?:like|love|enjoy|prefer)\b|\bwhat do you (?:like|love|enjoy) (?:most |best )?(?:about|the most)\b"
     r"|\bhow (?:did|does) (?:it|this|that) help\b|\bwhat (?:did you|do you) (?:like|love) (?:most |best )?about\b"
     r"|\bpor qu[eé] te (?:gust|encant)\w*|\bqu[eé] te (?:gust[oó]|encant[oó]) (?:m[aá]s )?de\b|\bc[oó]mo te ayud[oó]\b"),
    ("price_anchor",
     r"(?:[$€£]\s?\d|\b(?:usd|us\$|eur|gbp|ars|mxn|clp|cop|brl)\s?\d)"
     r"|\b\d+(?:[.,]\d+)?\s?(?:dollars?|bucks|euros?|pounds?|pesos|d[oó]lares|reales)\b"),
    ("double_barreled",
     r"\?[^?]*\?"
     # English: "X and how/what..." and "the A and the B"
     r"|,?\s+and\s+(?:what|how|why|when|where|who|do you|did you|would you|is it|are they)\b"
     r"|\b(?:about|of|with|on) (?:the|your) \w+ and (?:the |your )?\w+"
     # Spanish
     r"|,?\s+y\s+(?:qu[eé]|c[oó]mo|por qu[eé]|cu[aá]ndo|cu[aá]nto|d[oó]nde)\b"
     r"|\b(?:de|sobre|con) (?:la|el|los|las|tu|tus) \w+ y (?:la |el |los |las |tu |tus )?\w+"),
    ("jargon",
     r"\b(?:onboarding|engagement|feature|features|funnel|ux|ui|user journey|journey|pain points?|workflow|touchpoints?"
     r"|checkout|cta|kpi|mvp|friction|affordance|value proposition|stakeholders?|conversion|retention|churn|persona)\b"),
]

# Open openers: a question that starts like this is not "closed".
OPENERS = (
    r"^\W*(?:¿)?\s*(?:"
    # English
    r"what|how|why|when|where|who|which|whom|whose|in what|tell me|describe|walk me|talk me|take me|show me|"
    r"help me understand|think back|recall|remember when|"
    r"(?:can|could|would|will) you (?:please )?(?:tell|walk|describe|show|explain|share|talk|take|give|help|think|recall|remember|say)|"
    # Spanish
    r"qu[eé]|c[oó]mo|cu[eé]ntame|cont[aá]me|describ\w+|mostr\w+|record\w+|por qu[eé]|cu[aá]ndo|d[oó]nde|"
    r"qui[eé]n|cu[aá]l(?:es)?|cu[aá]nt[oa]s?|en qu[eé]|para qu[eé]|a qu[eé]|de qu[eé]|"
    r"(?:pod[eé]s|puedes|podr[ií]as|podr[ií]a) (?:contarme|decirme|describir\w*|mostrar\w*|explicar\w*|contar\w*)|"
    r"acordate|pens[aá]|imagin[aá] la [uú]ltima"
    r")\b"
)

# Closed: starts with an auxiliary/verb that invites yes/no.
CLOSED = (
    r"^\W*(?:¿)?\s*(?:"
    r"do|does|did|is|are|was|were|have|has|had|can|could|would|will|should|shall|may|might|am|"
    r"te|le|les|se|lo|la|has|ha|hay|es|era|fue|fueron|son|puedes|pod[eé]s|podr[ií]as|tienes|ten[eé]s|usas|us[aá]s|usa|"
    r"compras|compr[aá]s|conoces|conoc[eé]s|sabes|sab[eé]s|alguna vez|quieres|quer[eé]s|prefieres|prefer[ií]s|"
    r"piensas|pens[aá]s|crees|cre[eé]s|necesitas|necesit[aá]s|ten[ií]as|hiciste|usaste|probaste|"
    r"viste|miraste|le[ií]ste|llegaste|sent[ií]s|hac[eé]s|vas|ten[eé]s|sos|eres|est[aá]s|estaba|estuvo"
    r")\b.*\?\s*$"
)

LABELS = {
    "en": {
        "closed": "closed (yes/no): rewrite as 'tell me about the last time...' or 'what / how...'",
        "hypothetical": "hypothetical or prediction: ask about the most recent real episode instead",
        "absolute": "generic or absolute word ('usually', 'always', 'everyone'): anchor in the last time it happened",
        "leading": "leading or value-loaded wording: use neutral language and offer both poles",
        "positive_presupposition": "presupposes a positive experience: ask what happened, not why they liked it",
        "price_anchor": "price anchoring: do not reveal a number first; ask open or about past spending",
        "double_barreled": "possible double-barreled question: split into two questions",
        "jargon": "jargon: use the participant's own words",
        "too_long": "very long (>{n} words): split it or move it to a survey",
    },
    "es": {
        "closed": "cerrada (si/no): reescribila como 'contame la ultima vez que...' o 'que / como...'",
        "hypothetical": "hipotetica o prediccion: pregunta por el episodio real mas reciente",
        "absolute": "generica o absoluta ('normalmente', 'siempre', 'todos'): ancla en la ultima vez que paso",
        "leading": "capciosa o con carga de valor: usa lenguaje neutro y ofrece ambos polos",
        "positive_presupposition": "presupone experiencia positiva: pregunta que paso, no por que le gusto",
        "price_anchor": "anclaje de precio: no reveles una cifra primero; pregunta abierto o por gasto pasado",
        "double_barreled": "posible doble pregunta: partila en dos",
        "jargon": "jerga: usa las palabras del participante",
        "too_long": "muy larga (>{n} palabras): partila o pasala a un cuestionario",
    },
}

MSG = {
    "en": {
        "ok": "OK (no automatic alerts)",
        "summary": "{n} questions reviewed, {c} with alerts. Reminder: every question should map to a research question.",
        "no_file": "Error: file not found: '{p}'. Pass the path of a .txt file with one question per line.",
        "unreadable": "Error: could not read '{p}' as UTF-8 text ({e}).",
        "empty": "Error: the input has no questions (it is empty).",
    },
    "es": {
        "ok": "OK (sin alertas automaticas)",
        "summary": "{n} preguntas revisadas, {c} con alertas. Recorda: cada pregunta debe mapear a una pregunta de investigacion.",
        "no_file": "Error: no existe el archivo '{p}'. Pasa la ruta de un .txt con una pregunta por linea.",
        "unreadable": "Error: no pude leer '{p}' como texto UTF-8 ({e}).",
        "empty": "Error: el archivo no tiene preguntas (esta vacio).",
    },
}

MAX_WORDS = 30


def analyze(question, lang="en"):
    """Return the list of alert labels (in `lang`) for one question."""
    labels = LABELS[lang]
    keys = []
    is_open = re.search(OPENERS, question, re.I) is not None
    if not is_open and re.search(CLOSED, question, re.I):
        keys.append("closed")
    for key, pattern in RULES:
        if re.search(pattern, question, re.I):
            keys.append(key)
    if len(question.split()) > MAX_WORDS:
        keys.append("too_long")
    return [labels[k].format(n=MAX_WORDS) for k in keys]


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def read_lines(path):
    if path == "-":
        return sys.stdin.read().splitlines()
    with open(path, encoding="utf-8-sig") as f:
        return f.read().splitlines()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Flag closed, hypothetical, generic/absolute, leading, double-barreled, jargon-heavy and "
                    "price-anchored questions, in English and Spanish. One question per line "
                    "(bullets and numbering are ignored). Heuristic: confirm each alert by eye.",
        epilog="Example: python3 lint_questions.py questions.txt   |   cat guide.md | python3 lint_questions.py -   |   "
               "python3 lint_questions.py preguntas.txt --lang es")
    ap.add_argument("file", help="UTF-8 text file, or '-' to read from stdin")
    ap.add_argument("--lang", choices=["en", "es"], default="en", help="language of the report (default: en)")
    ap.add_argument("--only-alerts", "--solo-alertas", dest="only_alerts", action="store_true",
                    help="show only the questions that have alerts")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if any question has alerts")
    args = ap.parse_args(argv)
    m = MSG[args.lang]
    try:
        lines = read_lines(args.file)
    except FileNotFoundError:
        fail(m["no_file"].format(p=args.file))
    except (OSError, UnicodeDecodeError) as e:
        fail(m["unreadable"].format(p=args.file, e=e.__class__.__name__))
    n = flagged = 0
    for i, line in enumerate(lines, 1):
        q = re.sub(r"^[\s\-*•>]*(?:\d+[.)]\s*)?", "", line).strip()
        if not q or q.startswith("#"):
            continue
        n += 1
        alerts = analyze(q, args.lang)
        flagged += bool(alerts)
        if args.only_alerts and not alerts:
            continue
        print(f"[{i}] {q}")
        print("    " + ("; ".join(alerts) if alerts else m["ok"]))
    if n == 0:
        fail(m["empty"])
    print("\n" + m["summary"].format(n=n, c=flagged))
    if args.strict and flagged:
        sys.exit(1)


if __name__ == "__main__":
    main()
