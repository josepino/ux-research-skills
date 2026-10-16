#!/usr/bin/env python3
"""Calculate how many participants to recruit (including a margin for no-shows).

Usage:
  python3 sample_size.py --method usability --segments 2
  python3 sample_size.py --method quant-binary --confidence 95 --margin 15
  python3 sample_size.py --method quant-continuous --confidence 90 --margin 20
  python3 sample_size.py --method card-sorting --segments 3 --no-show-margin 25
  python3 sample_size.py --method usability --segments 2 --lang es

Methods: usability, card-sorting, eyetracking, interviews, quant-binary,
quant-continuous. Spanish names are accepted as aliases (usabilidad,
entrevistas, cuanti-binaria, cuanti-continua; --metodo/--segmentos/
--confianza/--margen/--margen-ausencias also work).

Base figures (see references/sample-size.md and references/sources.md):
 - qualitative usability: 5 per segment (3-4 if segments overlap) - NN/g 2012
 - card sorting: 15 per group - NN/g 2012
 - eye tracking (stable heatmaps): 39 - NN/g 2012
 - interviews: 5-8 per segment until saturation (we use 6; heuristic of ours)
 - quantitative, binary / continuous metric: NN/g 2021 tables

Exit codes: 0 ok, 1 invalid input (e.g. unsupported confidence/margin pair).
"""
import argparse
import math
import sys

BINARY = {(95, 15): 39, (95, 20): 21, (90, 15): 28, (90, 20): 15}
CONTINUOUS = {(95, 15): 47, (95, 20): 26, (90, 15): 33, (90, 20): 19}
PER_SEGMENT = {"usability": 5, "card-sorting": 15, "eyetracking": 39,
               "interviews": 6}  # interviews: 5-8, midpoint (heuristic of ours)
ALIASES = {"usabilidad": "usability", "entrevistas": "interviews",
           "cuanti-binaria": "quant-binary", "cuanti-continua": "quant-continuous",
           "eye-tracking": "eyetracking", "interview": "interviews"}
METHODS = list(PER_SEGMENT) + ["quant-binary", "quant-continuous"]

TXT = {
    "en": {
        "method": "Method", "base": "Base", "eff": "Effective sessions",
        "recruit": "To recruit (+{m}% no-shows/discards)",
        "per_seg": "{b} per segment x {s} segment(s)",
        "overlap": " (if segments overlap, 3-4 per segment: minimum {m})",
        "quant": "{b} (confidence {c}%, margin {m}%)",
        "note": "Reminder: these are references, not laws. Run a separate pilot (1-2 people).",
        "err_method": "unknown method '{m}'. Valid: {v}",
        "err_pair": "no table value for confidence {c}% and margin {m}%.",
        "err_neg": "--segments must be 1 or more and --no-show-margin cannot be negative.",
    },
    "es": {
        "method": "Método", "base": "Base", "eff": "Sesiones efectivas",
        "recruit": "A reclutar (+{m}% ausencias/descartes)",
        "per_seg": "{b} por segmento x {s} segmento(s)",
        "overlap": " (si los segmentos se solapan, 3-4 por segmento: mínimo {m})",
        "quant": "{b} (confianza {c}%, margen {m}%)",
        "note": "Recordatorio: son referencias, no leyes. Piloto aparte (1-2 personas).",
        "err_method": "método desconocido '{m}'. Válidos: {v}",
        "err_pair": "no hay valor en la tabla para confianza {c}% y margen {m}%.",
        "err_neg": "--segments debe ser 1 o más y --no-show-margin no puede ser negativo.",
    },
}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--method", "--metodo", dest="method", required=True,
                   help="one of: " + ", ".join(METHODS) + " (Spanish aliases accepted)")
    p.add_argument("--segments", "--segmentos", dest="segments", type=int, default=1,
                   help="number of user segments (default 1)")
    p.add_argument("--confidence", "--confianza", dest="confidence", type=int,
                   default=95, choices=[90, 95], help="confidence level for quant studies")
    p.add_argument("--margin", "--margen", dest="margin", type=int, default=15,
                   choices=[15, 20], help="margin of error (%%) for quant studies")
    p.add_argument("--no-show-margin", "--margen-ausencias", dest="noshow", type=int,
                   default=25, help="extra %% for no-shows/discards (default 25)")
    p.add_argument("--lang", choices=["en", "es"], default="en",
                   help="output language (default en)")
    a = p.parse_args()
    t = TXT[a.lang]

    method = ALIASES.get(a.method.lower(), a.method.lower())
    if method not in METHODS:
        print("Error: " + t["err_method"].format(m=a.method, v=", ".join(METHODS)),
              file=sys.stderr)
        return 1
    if a.segments < 1 or a.noshow < 0:
        print("Error: " + t["err_neg"], file=sys.stderr)
        return 1

    if method.startswith("quant"):
        table = BINARY if method == "quant-binary" else CONTINUOUS
        key = (a.confidence, a.margin)
        if key not in table:
            print("Error: " + t["err_pair"].format(c=a.confidence, m=a.margin),
                  file=sys.stderr)
            return 1
        base = table[key]
        effective = base
        detail = t["quant"].format(b=base, c=a.confidence, m=a.margin)
    else:
        base = PER_SEGMENT[method]
        effective = base * a.segments
        detail = t["per_seg"].format(b=base, s=a.segments)
        if method == "usability" and a.segments > 1:
            detail += t["overlap"].format(m=3 * a.segments)
    to_recruit = math.ceil(effective * (1 + a.noshow / 100))
    print("%s: %s\n%s: %s\n%s: %d" % (t["method"], method, t["base"], detail,
                                     t["eff"], effective))
    print("%s: %d" % (t["recruit"].format(m=a.noshow), to_recruit))
    print(t["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
