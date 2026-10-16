#!/usr/bin/env python3
"""Create the folder structure (and base files) of a UX research study.

Usage:
  python3 create_study_structure.py "checkout usability" --dest ./research --participants 6
  python3 create_study_structure.py "onboarding interviews" --date 2025-03-12 --global-repo
  python3 create_study_structure.py "checkout usabilidad" --lang es --participants 6

Options:
  --dest DIR           Root folder of the repository (default ./research)
  --date YYYY-MM-DD    Start date (default today)
  --participants N     Create N empty note files p01..pNN (default 0)
  --global-repo        Also create the global folders (00-guides, 03-insights,
                       99-archive...) if missing
  --lang {en,es}       Language of folder names, file names and file contents
                       (default en). With es the names are Spanish
                       (02-estudios, consentimiento, datos-crudos, notas...).
  --dry-run            Only show what would be created

Spanish option names are accepted as aliases (--destino, --fecha,
--participantes, --repo-global).
Never overwrites anything existing. Python standard library only.
Exit codes: 0 ok, 2 invalid input (bad date, empty study name, bad number,
destination is a file).
"""
import argparse
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path


def slug(text: str) -> str:
    """lowercase, no accents, no spaces: 'Checkout Usability' -> 'checkout-usability'."""
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


NAMES = {
    "en": {
        "studies": "02-studies",
        "study_dirs": ["consent", "raw-data", "notes", "debriefs", "synthesis", "deliverables"],
        "global_dirs": ["00-guides", "01-plans", "03-insights", "04-personas-maps", "99-archive"],
        "notes_dir": "notes", "debriefs_dir": "debriefs", "synthesis_dir": "synthesis",
        "note": "note", "debrief": "debrief_template", "codebook": "codebook",
        "log_folder": "folder ", "log_file": "file    ", "exists": "exists  ",
        "untouched": "(left untouched)",
    },
    "es": {
        "studies": "02-estudios",
        "study_dirs": ["consentimiento", "datos-crudos", "notas", "debriefs", "sintesis", "entregables"],
        "global_dirs": ["00-guias", "01-planes", "03-insights", "04-personas-mapas", "99-archivo"],
        "notes_dir": "notas", "debriefs_dir": "debriefs", "synthesis_dir": "sintesis",
        "note": "nota", "debrief": "debrief_plantilla", "codebook": "libro-de-codigos",
        "log_folder": "carpeta ", "log_file": "archivo ", "exists": "existe  ",
        "untouched": "(no se toca)",
    },
}

NOTES = {
"en": """# Session {pid} - {date} - {study}
Interviewer: ... | Note-taker: ... | Duration: ... | Recording: yes/no (path)
Profile (code only, no real name): ...

## Observations (facts and verbatim quotes)
| Min | Question/task | Observation or quote | Emotion | Tag | V/M |
|---|---|---|---|---|---|

## Interpretations (kept apart from facts; in brackets if written live)
- ...

## Surprises / contradictions
- ...

## Open questions
- ...
""",
"es": """# Sesión {pid} - {date} - {study}
Entrevistador: ... | Anotador: ... | Duración: ... | Grabación: sí/no (ruta)
Perfil (solo código, sin nombre real): ...

## Observaciones (hechos y citas textuales)
| Min | Pregunta/tarea | Observación o cita | Emoción | Tag | V/M |
|---|---|---|---|---|---|

## Interpretaciones (separadas de los hechos, entre corchetes si van en vivo)
- ...

## Sorpresas / contradicciones
- ...

## Preguntas abiertas
- ...
""",
}

DEBRIEF = {
"en": """# Debrief - {study} - {date}
Participant/session: ...   Attendees: ...   Duration: 15-30 min (scheduled in the same invitation)

Method: write in silence (one idea per note) -> post all at once -> group -> parking lot.
Guiding questions: What stood out? What surprised us? What contradicts our assumptions?
Which questions were missing or unnecessary for the next session? What do we adjust (questions / participants / logistics)?

## Top findings (tally: how many sessions show it)
| Finding | P01 | P02 | P03 | ... | Total |
|---|---|---|---|---|---|

## Parking lot (what / who / when)
| Topic | Owner | Date |
|---|---|---|

## Minutes
Learnings: ... | Surprises: ... | Contradictions: ... | Open questions: ... | Next steps: ...
""",
"es": """# Debrief - {study} - {date}
Participante/sesión: ...   Asistentes: ...   Duración: 15-30 min (agendado en la misma invitación)

Dinámica: escribir en silencio (una idea por nota) -> publicar a la vez -> agrupar -> estacionamiento.
Preguntas guía: ¿Qué destacó? ¿Qué nos sorprendió? ¿Qué contradice nuestras suposiciones?
¿Qué preguntas faltaron o sobran para la próxima sesión? ¿Qué ajustamos (preguntas / participantes / logística)?

## Top hallazgos (tally: cuántas sesiones lo muestran)
| Hallazgo | P01 | P02 | P03 | ... | Total |
|---|---|---|---|---|---|

## Estacionamiento (qué / quién / cuándo)
| Tema | Responsable | Fecha |
|---|---|---|

## Acta
Aprendizajes: ... | Sorpresas: ... | Contradicciones: ... | Preguntas abiertas: ... | Próximos pasos: ...
""",
}

CODEBOOK = {
"en": """# Codebook (tags) - {study}
Start with a few broad tags and refine them later. Document every code.

| Tag | Definition | Example | When NOT to use it |
|---|---|---|---|
| nav | Trouble finding things or moving around | "I can't find the cart" | ... |
""",
"es": """# Libro de códigos (tags) - {study}
Empezá con pocos tags amplios y afinalos luego. Documentá cada código.

| Tag | Definición | Ejemplo | Cuándo NO usarlo |
|---|---|---|---|
| nav | Problemas para encontrar o moverse | "No encuentro el carrito" | ... |
""",
}

README = {
"en": """# {study}
Start: {date} | Status: planned | Owner: ... | Method: ... | n participants: ...
Product/area: ... | Tags: ... | Decision it informs: ...

## Naming convention
YYYY-MM-DD_study_type_id_vNN.ext  (lowercase, no spaces or accents, leading zeros)
E.g.: {date}_{slug}_note_p01_v01.md
Participant codes (P01, P02...) in names and notes; the table that links them to people
lives only in raw-data/ with restricted access.

## Map
plan.md / guide.md / consent/ -> raw-data/ (restricted) -> notes/ -> debriefs/ -> synthesis/ -> report.md
""",
"es": """# {study}
Inicio: {date} | Estado: planificado | Responsable: ... | Método: ... | n participantes: ...
Producto/área: ... | Tags: ... | Decisión que informa: ...

## Convención de nombres
AAAA-MM-DD_estudio_tipo_id_vNN.ext  (minúsculas, sin espacios ni tildes, ceros a la izquierda)
Ej.: {date}_{slug}_nota_p01_v01.md
Códigos de participante (P01, P02...) en nombres y notas; la tabla que los vincula con personas
vive solo en datos-crudos/ con acceso restringido.

## Mapa
plan.md / guia.md / consentimiento/ -> datos-crudos/ (restringido) -> notas/ -> debriefs/ -> sintesis/ -> informe.md
""",
}

ERR = {
    "en": {"date": "--date must be YYYY-MM-DD", "name": "empty study name",
           "num": "--participants must be between 0 and 200",
           "dest": "destination '%s' exists and is not a folder",
           "os": "could not create '%s': %s"},
    "es": {"date": "--fecha debe ser AAAA-MM-DD", "name": "nombre de estudio vacío",
           "num": "--participantes debe estar entre 0 y 200",
           "dest": "el destino '%s' existe y no es una carpeta",
           "os": "no pude crear '%s': %s"},
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("study", help="short study name, e.g. 'checkout usability'")
    ap.add_argument("--dest", "--destino", dest="dest", default="./research")
    ap.add_argument("--date", "--fecha", dest="date", default=date.today().isoformat())
    ap.add_argument("--participants", "--participantes", dest="participants", type=int, default=0)
    ap.add_argument("--global-repo", "--repo-global", dest="global_repo", action="store_true")
    ap.add_argument("--lang", choices=["en", "es"], default="en")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    lang = a.lang
    err, n = ERR[lang], NAMES[lang]

    try:
        datetime.strptime(a.date, "%Y-%m-%d")
    except ValueError:
        print("Error: " + err["date"], file=sys.stderr)
        return 2
    s = slug(a.study)
    if not s:
        print("Error: " + err["name"], file=sys.stderr)
        return 2
    if not 0 <= a.participants <= 200:
        print("Error: " + err["num"], file=sys.stderr)
        return 2
    root = Path(a.dest)
    if root.exists() and not root.is_dir():
        print("Error: " + err["dest"] % root, file=sys.stderr)
        return 2

    study_dir = root / n["studies"] / f"{a.date}_{s}"
    folders = [study_dir / d for d in n["study_dirs"]]
    if a.global_repo:
        folders += [root / d for d in n["global_dirs"]]
    files = {
        study_dir / "README.md": README[lang].format(study=a.study, date=a.date, slug=s),
        study_dir / n["debriefs_dir"] / f"{a.date}_{s}_{n['debrief']}_v01.md":
            DEBRIEF[lang].format(study=a.study, date=a.date),
        study_dir / n["synthesis_dir"] / f"{s}_{n['codebook']}_v01.md":
            CODEBOOK[lang].format(study=a.study),
    }
    for i in range(1, a.participants + 1):
        pid = f"p{i:02d}"
        files[study_dir / n["notes_dir"] / f"{a.date}_{s}_{n['note']}_{pid}_v01.md"] = \
            NOTES[lang].format(pid=pid.upper(), date=a.date, study=a.study)

    pre = "[dry] " if a.dry_run else ""
    try:
        for c in folders:
            print(pre + n["log_folder"] + str(c))
            if not a.dry_run:
                c.mkdir(parents=True, exist_ok=True)
        for f, txt in files.items():
            if f.exists():
                print(f"{n['exists']}{f} {n['untouched']}")
                continue
            print(pre + n["log_file"] + str(f))
            if not a.dry_run:
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(txt, encoding="utf-8")
    except OSError as e:
        print("Error: " + err["os"] % (e.filename, e.strerror), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
