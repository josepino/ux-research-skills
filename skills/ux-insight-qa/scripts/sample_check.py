#!/usr/bin/env python3
"""Flag percentages that can mislead with small samples in a report.

OUR HEURISTIC (not a statistical rule): if the report declares an n below --n-threshold
(default 20), flag percentages that have decimals or are not accompanied by "X of N" in
the same sentence. With small samples, report "6 of 8" instead of "75%" or "62.5%": the
percentage suggests a precision the sample does not have. It is a prompt to review, not an error.

Usage:
  python3 sample_check.py --report report.md [--n-threshold 20] [--lang en|es]

Recognized sample declarations: "n=8", "8 participants/people/users/interviewees/respondents/
sessions" and the Spanish equivalents ("8 participantes", "muestra de 8"), plus "sample of 8".
Recognized counts: "6 of 8", "6 out of 8" and Spanish "6 de 8".
Spanish flag aliases: --informe, --umbral-n.

Exit codes: 0 no alerts; 1 alerts (or percentages with no declared n); 2 usage or input error
(missing/unreadable file, bad option); 130 interrupted.
"""
import argparse
import re
import sys
from pathlib import Path

PCT = re.compile(r"(\d+(?:[.,]\d+)?)\s?%")
N_DECL = [
    re.compile(r"\bn\s*=\s*(\d+)", re.I),
    re.compile(r"\b(\d+)\s+(?:participants|people|persons|users|interviewees|respondents|respondents|sessions|"
               r"participantes|personas|usuarios|usuarias|entrevistad[oa]s|encuestad[oa]s|sesiones|respondientes)\b", re.I),
    re.compile(r"\b(?:sample\s+of|muestra\s+de)\s+(\d+)\b", re.I),
]
X_OF_N = re.compile(r"\b\d+\s+(?:of|out\s+of|de)\s+(?:the\s+|los\s+|las\s+)?\d+\b", re.I)

MSG = {
    "en": {
        "err": "Error: {m}",
        "no_file": "report '{p}' does not exist.",
        "read": "could not read the report: {e}",
        "head": "Report: {r} | our heuristic, threshold n < {t}",
        "no_pct": "No percentages in the report: nothing to check.",
        "no_n": "There are {k} percentage(s) but the report does not declare n (e.g. \"n=8\" or \"8 participants\"). Declaring n is the first fix.",
        "ns": "declared n: {ns} (the smallest is used: {m})",
        "big": "The smallest n is not small by this threshold: no alerts. Still check subgroups if percentages are computed over them.",
        "dec": "has decimals (precision the sample does not support)",
        "nox": "does not show \"X of N\"",
        "and": " and ",
        "alert": "- line {l}: \"{p}\" {why}",
        "ctx": "    Context: {c}",
        "tail": "\n{a} alert(s). Suggestion: report \"k of {n}\" and add the percentage only as support, without decimals. If the declared n belongs to another subgroup, ignore the alert.",
        "ok": "No alerts: percentages come with \"X of N\" and without decimals.",
        "d_report": "report in .md or .txt",
        "d_thr": "n below which to alert (default 20)",
        "d_lang": "language of the output messages",
        "epilog": "Our heuristic: it guides the review, it does not replace statistical judgment.",
    },
    "es": {
        "err": "Error: {m}",
        "no_file": "no existe el informe «{p}».",
        "read": "no pude leer el informe: {e}",
        "head": "Informe: {r} | heurística nuestra, umbral n < {t}",
        "no_pct": "No hay porcentajes en el informe: nada que chequear.",
        "no_n": "Hay {k} porcentaje(s) pero el informe no declara n (ej. «n=8» o «8 participantes»). Declarar el n es el primer arreglo.",
        "ns": "n declarados: {ns} (se usa el menor: {m})",
        "big": "El n más chico no es pequeño según este umbral: sin alertas. Igual revisá los subgrupos si los porcentajes se calculan sobre ellos.",
        "dec": "tiene decimales (precisión que la muestra no sostiene)",
        "nox": "no muestra «X de N»",
        "and": " y ",
        "alert": "- línea {l}: «{p}» {why}",
        "ctx": "    Contexto: {c}",
        "tail": "\n{a} alerta(s). Sugerencia: reportar «k de {n}» y agregar el porcentaje solo como apoyo, sin decimales. Si el n declarado es de otro subgrupo, ignorá la alerta.",
        "ok": "Sin alertas: los porcentajes vienen con «X de N» y sin decimales.",
        "d_report": "informe en .md o .txt",
        "d_thr": "n por debajo del cual se alerta (default 20)",
        "d_lang": "idioma de los mensajes de salida",
        "epilog": "Heurística nuestra: orienta la revisión, no reemplaza el criterio estadístico.",
    },
}
M = MSG["en"]


def fail(msg):
    print(M["err"].format(m=msg), file=sys.stderr)
    sys.exit(2)


def main():
    global M
    lang = "en"
    if "--lang" in sys.argv:
        i = sys.argv.index("--lang")
        if i + 1 < len(sys.argv) and sys.argv[i + 1] in MSG:
            lang = sys.argv[i + 1]
    M = MSG[lang]
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], epilog=M["epilog"])
    ap.add_argument("--report", "--informe", dest="report", required=True, help=M["d_report"])
    ap.add_argument("--n-threshold", "--umbral-n", dest="nthr", type=int, default=20, help=M["d_thr"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=M["d_lang"])
    a = ap.parse_args()
    p = Path(a.report)
    if not p.is_file():
        fail(M["no_file"].format(p=a.report))
    try:
        text = p.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as e:
        fail(M["read"].format(e=e.strerror or e))

    ns = sorted({int(m.group(1)) for rx in N_DECL for m in rx.finditer(text) if int(m.group(1)) > 0})
    pcts = list(PCT.finditer(text))
    print(M["head"].format(r=a.report, t=a.nthr))
    if not pcts:
        print(M["no_pct"])
        return 0
    if not ns:
        print(M["no_n"].format(k=len(pcts)))
        return 1
    n_min = ns[0]
    print(M["ns"].format(ns=", ".join(map(str, ns)), m=n_min))
    if n_min >= a.nthr:
        print(M["big"])
        return 0

    alerts = 0
    for m in pcts:
        start = max(text.rfind(".", 0, m.start()), text.rfind("\n", 0, m.start())) + 1
        ends = [i for i in (text.find(". ", m.end()), text.find("\n", m.end())) if i != -1]
        end = min(ends) if ends else len(text)
        sentence = text[start:end]
        why = []
        if re.search(r"[.,]\d", m.group(1)):
            why.append(M["dec"])
        if not X_OF_N.search(sentence):
            why.append(M["nox"])
        if why:
            alerts += 1
            line = text.count("\n", 0, m.start()) + 1
            print(M["alert"].format(l=line, p=m.group(0), why=M["and"].join(why)))
            print(M["ctx"].format(c=" ".join(sentence.split())[:140]))
    if alerts:
        print(M["tail"].format(a=alerts, n=n_min))
        return 1
    print(M["ok"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
