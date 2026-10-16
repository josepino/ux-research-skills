#!/usr/bin/env python3
"""Heuristic linter for usability-test tasks (one task per line).

Flags clues that give away the answer, in English AND Spanish:
 - product labels you pass with --labels (menus, buttons), plus soft alerts for
   singular/plural or stem matches of a label word (receta / Recetas)
 - words that prejudge: easy, simply, quick, just, obvious... (fácil, simplemente...)
 - click/tap verbs aimed at the interface (click, tap, press, select the button...)
 - step-by-step instructions or navigation paths (first/then, 1., A > B, go to X and...)
 - no clear end point (how does the person know they are done?)
 - very short tasks with no motive or context

Usage:
  python3 lint_tasks.py tasks.txt
  python3 lint_tasks.py tasks.txt --labels labels.txt --lang es

Input: UTF-8 text file, one task per line; blank lines and lines starting
with # are ignored. Labels file: one menu/button name per line.
It is a heuristic: confirm every alert by eye.
Exit codes: 0 no alerts, 1 at least one task has alerts, 2 error
(missing file, not UTF-8, empty file).
"""
import argparse
import re
import sys

HEURISTIC = {"en": "Heuristic: confirm every alert by eye.",
             "es": "Heurístico: confirmá cada alerta a ojo."}

HEDGE_WORDS = [
    # English
    "easy", "easily", "simple", "simply", "straightforward", "quick", "quickly", "just",
    "only have to", "all you have to do", "obvious", "obviously", "clearly",
    # Spanish
    "fácil", "facil", "fácilmente", "facilmente", "simplemente", "simple", "sencillo",
    "rápido", "rapido", "rápidamente", "solo tenés", "solo tenes", "solo tienes",
    "nada más", "nada mas", "obvio", "claramente",
]

CLICK_VERBS = [
    # English
    r"\bdouble[- ]?click\b", r"\bright[- ]?click\b", r"\bclick(s|ed|ing)?\b",
    r"\btap(s|ped|ping)?\b", r"\bpress(es|ed|ing)?\b", r"\bhit\s+(the\s+)?\w+\s+(button|link)\b",
    r"\bpush\b", r"\bhover\b", r"\bscroll\s+(down\s+)?to\b",
    r"\bselect\s+(the\s+)?[\w\- ]{0,20}?(button|menu|tab|icon|link|dropdown)\b",
    r"\bchoose\s+(the\s+)?[\w\- ]{0,20}?(button|menu|tab|icon|link|dropdown)\b",
    # Spanish
    r"\bhac[eé]\s+(un\s+)?clic\b", r"\bhac[eé]\s+click\b", r"\bhaga\s+clic\b", r"\bclic\b",
    r"\bclicke[aá]\b", r"\btoc[aá]\b", r"\bpresion[aá]\b", r"\bpuls[aá]\b", r"\bapret[aá]\b",
    r"\bseleccion[aá]\s+(el|la)\s+(bot[oó]n|men[uú]|pesta[nñ]a)\b",
    r"\belig[eí]\s+(el|la)\s+(bot[oó]n|men[uú]|pesta[nñ]a)\b",
]

STEP_PATTERNS = [
    # English
    r"\b(first|then|next|after that|afterwards|finally|lastly)\b", r"\bstep\s+\d+\b",
    r"\bgo to\b.*\b(and|then)\b", r"\b(open|navigate to|head to)\b.*\b(and|then)\b",
    # Spanish
    r"\b(primero|luego|despu[eé]s|a continuaci[oó]n|finalmente)\b", r"\bpaso\s+\d+\b",
    r"\b(and[aá]|ir|ve|entr[aá]|abr[ií])\s+(a|al|a la|en)\s+\S+.*\b(y|luego|despu[eé]s)\b",
    # Both
    r"^\s*\d+[.)]\s", r">", r"→",
]

END_POINTS = [
    # English
    r"\buntil\b", r"\bwhen you (have|see|get|reach|finish|are done)\b", r"\btell me\b",
    r"\blet me know\b", r"\bsay\b", r"\bread (out|me)\b", r"\bconfirm", r"\bto the point where\b",
    r"\bup to (the point|where)\b", r"\bso that\b", r"\bfinish", r"\bcomplete", r"\bonce you\b",
    r"\bfind out\b", r"\btell\b", r"\breport\b", r"\bpaid\b", r"\bsubmitted?\b",
    # Spanish
    r"hasta (que|tener|ver|llegar|haber|completar|confirm)", r"cuando (ya )?(tengas|veas|hayas|termin)",
    r"\bdecime\b", r"\bdec[ií]\b", r"\bavis[aá]\b", r"\bindic[aá]\b", r"confirm",
    r"hasta el punto", r"\bpagaste\b", r"complet[eao]", r"termin[eao]", r"finaliz",
    r"\by (me )?(dec[ií]|cont[aá])\b", r"averigu[aá]", r"\bcont[aá]me\b",
]

MSG = {
    "en": {
        "label": "uses the product label '{e}' (gives the answer away)",
        "soft": "[soft] '{w}' shares a stem with the product label '{e}': reword it or justify it",
        "hedge": "prejudging word: '{p}'",
        "click": "click/tap verb aimed at the interface: ask for the result, not the gesture",
        "steps": "looks like a step-by-step instruction or navigation path",
        "end": "no clear end point (how does the person know they are done?)",
        "short": "very short: missing motive/context for the scenario",
        "ok": "Task {i}: OK", "task": "Task {i}: {t}",
        "summary": "{c} of {n} tasks with alerts.",
        "e_missing": "the {what} file does not exist: {path}",
        "e_utf": "{path} is not UTF-8.",
        "e_read": "could not read {path}: {err}",
        "e_empty": "the tasks file is empty (no tasks found).",
        "what_tasks": "tasks", "what_labels": "labels",
        "desc": "Flags usability tasks that give clues: product labels, steps, words like 'easy', click verbs and a missing end point (English and Spanish).",
        "h_tasks": "text file with one task per line (# = comment)",
        "h_labels": "file with menu/button names, one per line",
        "h_lang": "output language (default en); detection works in both languages",
    },
    "es": {
        "label": "usa la etiqueta del producto «{e}» (da la pista)",
        "soft": "[suave] «{w}» comparte raíz con la etiqueta del producto «{e}»: reformulala o justificala",
        "hedge": "palabra que prejuzga: «{p}»",
        "click": "verbo de clic/acción sobre la interfaz: pedí el resultado, no el gesto",
        "steps": "parece instrucción paso a paso o ruta de navegación",
        "end": "sin punto de término claro (¿cómo sabe la persona que terminó?)",
        "short": "muy corta: falta motivo/contexto del escenario",
        "ok": "Tarea {i}: OK", "task": "Tarea {i}: {t}",
        "summary": "{c} de {n} tareas con alertas.",
        "e_missing": "no existe el archivo de {what}: {path}",
        "e_utf": "{path} no está en UTF-8.",
        "e_read": "no se pudo leer {path}: {err}",
        "e_empty": "el archivo de tareas está vacío (no hay tareas).",
        "what_tasks": "tareas", "what_labels": "etiquetas",
        "desc": "Marca tareas de usabilidad que dan pistas: etiquetas del producto, pasos, palabras como «fácil», verbos de clic y falta de punto de término (inglés y español).",
        "h_tasks": "archivo de texto con una tarea por línea (# = comentario)",
        "h_labels": "archivo con nombres de menús/botones, uno por línea",
        "h_lang": "idioma de la salida (por defecto en); la detección funciona en ambos idiomas",
    },
}


def die(msg):
    print("Error: " + msg, file=sys.stderr)
    sys.exit(2)


def read_lines(path, what, m):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    except FileNotFoundError:
        die(m["e_missing"].format(what=what, path=path))
    except UnicodeDecodeError:
        die(m["e_utf"].format(path=path))
    except OSError as e:
        die(m["e_read"].format(path=path, err=e.strerror))


def analyze(task, labels, m):
    t = task.lower()
    alerts = []
    words = re.findall(r"\w+", t)
    for e in labels:
        if e.lower() in t:
            alerts.append(m["label"].format(e=e))
            continue
        # soft alert: singular/plural or stem match of a label word (receta / Recetas)
        hit = next((w for lw in re.findall(r"\w{4,}", e.lower())
                    for w in words if w.startswith(lw[:max(4, len(lw) - 2)])), None)
        if hit:
            alerts.append(m["soft"].format(w=hit, e=e))
    for p in HEDGE_WORDS:
        if re.search(r"(?<!\w)" + re.escape(p) + r"(?!\w)", t):
            alerts.append(m["hedge"].format(p=p))
            break
    if any(re.search(v, t) for v in CLICK_VERBS):
        alerts.append(m["click"])
    if any(re.search(p, t) for p in STEP_PATTERNS):
        alerts.append(m["steps"])
    if not any(re.search(p, t) for p in END_POINTS):
        alerts.append(m["end"])
    if len(task.split()) < 6:
        alerts.append(m["short"])
    return alerts


def main():
    # parse --lang first so --help and errors use the right language
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=["en", "es"], default="en")
    known, _ = pre.parse_known_args()
    m = MSG[known.lang]
    ap = argparse.ArgumentParser(description=__doc__ if known.lang == "en" else m["desc"] + "\n\n" + HEURISTIC["es"],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tasks", help=m["h_tasks"])
    ap.add_argument("--labels", "--etiquetas", dest="labels", help=m["h_labels"])
    ap.add_argument("--lang", choices=["en", "es"], default="en", help=m["h_lang"])
    a = ap.parse_args()
    tasks = read_lines(a.tasks, m["what_tasks"], m)
    if not tasks:
        die(m["e_empty"])
    labels = read_lines(a.labels, m["what_labels"], m) if a.labels else []
    with_alerts = 0
    for i, t in enumerate(tasks, 1):
        al = analyze(t, labels, m)
        if al:
            with_alerts += 1
            print(m["task"].format(i=i, t=t))
            for x in al:
                print("  - " + x)
        else:
            print(m["ok"].format(i=i))
    print("\n" + m["summary"].format(c=with_alerts, n=len(tasks)) + " " + HEURISTIC[known.lang])
    sys.exit(1 if with_alerts else 0)


if __name__ == "__main__":
    main()
