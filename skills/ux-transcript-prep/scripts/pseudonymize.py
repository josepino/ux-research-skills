#!/usr/bin/env python3
"""Pseudonymize and redact personal data in a transcript (Python 3 standard library only).

IMPORTANT: automatic detection is NOT exhaustive. A human must always review the whole
result (name variants, nicknames, job titles, places, indirectly identifying data).
This is not legal advice.

What it does
  * Replaces names from a CSV ('name,code[,type]') with codes (P01, [BOSS]...). Several rows
    may share a code (variants of the same name). Spanish headers 'nombre,codigo,tipo' are
    accepted as aliases.
  * Detects by pattern and redacts: emails, URLs, @handles, phone numbers (7-15 digits),
    long digit runs (6+ digits: IDs, account numbers), SSN-like numbers, and street addresses
    (English "123 Main Street" and Spanish "calle Mitre 123").
  * Lists capitalized words in mid-sentence that are not in your CSV (possible names,
    places, brands) for human review.
  * Writes the identity map (code <-> original) to a SEPARATE file created with permissions
    0600 (owner read/write only) on Unix-like systems.

--detect-only writes nothing: it only reports what would be detected.

Exit codes: 0 = ok; 2 = error (missing file, bad CSV headers, output exists, ...).
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter, OrderedDict

TAGS = {
    "en": {"EMAIL": "EMAIL", "URL": "URL", "HANDLE": "HANDLE", "ADDRESS": "ADDRESS", "PHONE": "PHONE",
           "NUMBER": "NUMBER", "ID": "ID"},
    "es": {"EMAIL": "EMAIL", "URL": "URL", "HANDLE": "USUARIO", "ADDRESS": "DIRECCION", "PHONE": "TELEFONO",
           "NUMBER": "NUMERO", "ID": "ID"},
}

MSG = {
    "en": {
        "warn": ("WARNING: automatic detection is not exhaustive. A misspelled name, a nickname, an unusual job "
                 "title or a place can go undetected. Review the whole result by hand before sharing it or "
                 "uploading it to an external tool."),
        "err_nofile": "input file not found: {p}",
        "err_utf8": "the file is not UTF-8; save it as UTF-8 and try again",
        "err_read": "could not read {p} ({e})",
        "err_nonames": "names CSV not found: {p}",
        "err_namesread": "could not read the names CSV ({e})",
        "err_namecols": "the names CSV needs a header 'name,code' (optional: 'type'). Headers found: {h}",
        "err_namerows": "the names CSV has no rows with both 'name' and 'code'",
        "err_needout": "give the output file with -o (or use --detect-only)",
        "err_needmap": "say where to save the identity map with --identity-map (keep it apart from the text)",
        "err_overwrite_in": "the input file is never overwritten: {p}",
        "err_exists": "{p} already exists; use --force or pick another name",
        "err_samefile": "the output and the identity map must be different files",
        "err_write": "could not write an output file ({e})",
        "report": "# Pseudonymization report", 
        "names_h": "## Names from the CSV found",
        "none": "none",
        "unused": "- In the CSV but NOT present in the text: {s}",
        "det_h": "## Detected by pattern ({mode})",
        "mode_dry": "unchanged", "mode_list": "listed only", "mode_red": "redacted",
        "det_line": "- line {l}: {t} -> {v}",
        "cand_h": "## Capitalized words in mid-sentence NOT in your CSV (possible names, places or brands)",
        "labels_h": "## Speaker labels seen (check they are not real names): {s}",
        "human_h": "## Mandatory human review",
        "human1": ("- Indirectly identifying data: unusual job titles, company + area, cities/neighborhoods, "
                   "specific dates, unique events, combinations of traits. See references/pseudonymization-and-privacy.md."),
        "human2": "- The identity map is the most sensitive data: keep it apart, with restricted access.",
        "dry": "\n(--detect-only mode: no file was written.)",
        "written": ("\nWritten: {o}\nIdentity map (RESTRICTED ACCESS, do not upload it with the text): {m}"),
        "map_header": ["code", "original_value", "type"],
    },
    "es": {
        "warn": ("AVISO: la deteccion automatica no es exhaustiva. Un nombre mal escrito, un apodo, un cargo "
                 "poco comun o un lugar pueden quedar sin detectar. Revisa el resultado completo a mano "
                 "antes de compartirlo o subirlo a una herramienta externa."),
        "err_nofile": "no existe el archivo de entrada: {p}",
        "err_utf8": "el archivo no esta en UTF-8; guardalo como UTF-8 y volve a probar",
        "err_read": "no se pudo leer {p} ({e})",
        "err_nonames": "no existe el CSV de nombres: {p}",
        "err_namesread": "no se pudo leer el CSV de nombres ({e})",
        "err_namecols": "el CSV de nombres necesita encabezado 'nombre,codigo' (opcional: 'tipo'). Encabezados encontrados: {h}",
        "err_namerows": "el CSV de nombres no tiene filas con 'nombre' y 'codigo'",
        "err_needout": "indica el archivo de salida con -o (o usa --detect-only)",
        "err_needmap": "indica donde guardar el mapa de identidad con --identity-map (guardalo separado del texto)",
        "err_overwrite_in": "no se sobrescribe el archivo de entrada: {p}",
        "err_exists": "ya existe {p}; usa --force o elegi otro nombre",
        "err_samefile": "la salida y el mapa de identidad deben ser archivos distintos",
        "err_write": "no se pudo escribir un archivo de salida ({e})",
        "report": "# Informe de seudonimizacion",
        "names_h": "## Nombres del CSV encontrados",
        "none": "ninguno",
        "unused": "- En el CSV pero NO aparecen en el texto: {s}",
        "det_h": "## Detectado por patrones ({mode})",
        "mode_dry": "sin modificar", "mode_list": "solo listado", "mode_red": "redactado",
        "det_line": "- linea {l}: {t} -> {v}",
        "cand_h": "## Palabras con mayuscula en medio de frase que NO estan en tu CSV (posibles nombres, lugares o marcas)",
        "labels_h": "## Etiquetas de hablante vistas (revisa que no sean nombres reales): {s}",
        "human_h": "## Revision humana obligatoria",
        "human1": ("- Datos indirectamente identificantes: cargos poco comunes, empresa + area, ciudades/barrios, "
                   "fechas puntuales, eventos unicos, combinaciones de rasgos. Ver references/pseudonymization-and-privacy.md."),
        "human2": "- El mapa de identidad es el dato mas sensible: guardalo aparte, con acceso restringido.",
        "dry": "\n(Modo --detect-only: no se escribio ningun archivo.)",
        "written": ("\nEscrito: {o}\nMapa de identidad (ACCESO RESTRINGIDO, no lo subas junto al texto): {m}"),
        "map_header": ["codigo", "dato_original", "tipo"],
    },
}
M = MSG["en"]

RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_URL = re.compile(r"(?:https?://|www\.)[^\s<>\"')]*[^\s<>\"').,;:!?]", re.I)
RE_HANDLE = re.compile(r"(?<![\w.@])@\w{2,30}")
RE_SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$|^\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}$")
RE_NUMCAND = re.compile(r"(?<![\w.])\+?\d[\d\s().-]{4,}\d(?![\w])")
# Spanish: street word first ("calle Mitre 123"); English: number first ("123 Main Street")
RE_ADDR_ES = re.compile(
    r"\b(?:calle|av\.?|avenida|pasaje|ruta|boulevard|bv\.?|diagonal)\s+[^,.;\n]{1,40}?\s*\d{1,5}\b", re.I)
RE_ADDR_EN = re.compile(
    r"\b\d{1,5}\s+(?:[A-Z][\w.'-]*\s+){1,3}(?:[Ss]treet|St|[Aa]venue|Ave|[Rr]oad|Rd|[Bb]oulevard|Blvd|[Ll]ane|Ln|"
    r"[Dd]rive|Dr|[Ww]ay|[Cc]ourt|Ct)\b\.?")
RE_CAPS = re.compile(r"(?<=[a-záéíóúñü,]\s)[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}")
RE_LABEL = re.compile(r"^([^\W\d_][^:\n]{0,40}?)\s*:(?:\s+|$)")


def fail(key, **kw):
    print("Error: " + M[key].format(**kw), file=sys.stderr)
    sys.exit(2)


def read_text(path):
    if not os.path.isfile(path):
        fail("err_nofile", p=path)
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        fail("err_utf8")
    except OSError as e:
        fail("err_read", p=path, e=e.strerror)


def read_names(path):
    """Names CSV. Canonical header: name,code[,type]. Aliases: nombre,codigo,tipo."""
    if not os.path.isfile(path):
        fail("err_nonames", p=path)
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            cols = [c.strip().lower() for c in (reader.fieldnames or [])]
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        fail("err_namesread", e=e)
    name_col = "name" if "name" in cols else "nombre"
    code_col = "code" if "code" in cols else "codigo"
    type_col = "type" if "type" in cols else "tipo"
    if name_col not in cols or code_col not in cols:
        fail("err_namecols", h=", ".join(cols) or "none")
    pairs = []
    for row in rows:
        r2 = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
        if r2.get(name_col) and r2.get(code_col):
            pairs.append((r2[name_col], r2[code_col], r2.get(type_col) or "name"))
    if not pairs:
        fail("err_namerows")
    return pairs


def detect(text, tags):
    """Return a list of (start, end, tag, value) without overlaps."""
    found = []
    for rx, tag in ((RE_EMAIL, "EMAIL"), (RE_URL, "URL"), (RE_HANDLE, "HANDLE"), (RE_ADDR_ES, "ADDRESS"),
                    (RE_ADDR_EN, "ADDRESS"), (RE_SSN, "ID")):
        for m in rx.finditer(text):
            found.append((m.start(), m.end(), tags[tag], m.group(0)))
    for m in RE_NUMCAND.finditer(text):
        v = m.group(0)
        if RE_DATE.match(v.strip()):
            continue
        digits = len(re.sub(r"\D", "", v))
        compact = re.fullmatch(r"\d+", v) is not None
        if digits >= 6 and compact:
            tag = "NUMBER"
        elif 7 <= digits <= 15:
            tag = "PHONE"
        elif digits > 15:
            tag = "NUMBER"
        else:
            continue
        found.append((m.start(), m.end(), tags[tag], v))
    found.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    final, prev_end = [], -1
    for h in found:
        if h[0] >= prev_end:
            final.append(h)
            prev_end = h[1]
    return final


def write_private(path, writer_fn):
    """Create `path` with mode 0600 from the start (no window with looser permissions)."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        writer_fn(f)
    try:
        os.chmod(path, 0o600)  # also tighten a pre-existing file (--force)
    except OSError:
        pass


def build_parser():
    ap = argparse.ArgumentParser(
        description="Pseudonymize a transcript: replace names from a CSV (name->code) and detect emails, "
                    "phones, URLs, @handles, addresses and long numbers. Automatic detection is NOT "
                    "exhaustive: always review the result by hand. Not legal advice.",
        epilog="Exit codes: 0 ok; 2 error. Example: python3 pseudonymize.py s01.txt --names names.csv "
               "-o s01_pseudo.txt --identity-map ../restricted/s01_identity.csv")
    ap.add_argument("input", help="transcript .txt/.md")
    ap.add_argument("--names", "--nombres", dest="names", metavar="NAMES.CSV",
                    help="CSV 'name,code[,type]'; several rows may share a code (name variants)")
    ap.add_argument("-o", "--output", help="pseudonymized file (required unless --detect-only)")
    ap.add_argument("--identity-map", "--mapa-identidad", dest="identity_map", metavar="MAP.CSV",
                    help="where to save the code<->original map (keep it APART, restricted access; created 0600)")
    ap.add_argument("--detect-only", "--solo-detectar", dest="detect_only", action="store_true",
                    help="write nothing: only list what would be detected")
    ap.add_argument("--no-redact-detected", "--no-redactar-detectados", dest="no_redact", action="store_true",
                    help="replace only the CSV names; pattern-detected items are only listed")
    ap.add_argument("--force", "--forzar", dest="force", action="store_true",
                    help="allow overwriting existing output files")
    ap.add_argument("--lang", choices=["en", "es"], default="en",
                    help="language of the report and of the placeholders, e.g. [PHONE_1] vs [TELEFONO_1] (default: en)")
    return ap


def main(argv=None):
    global M
    args = build_parser().parse_args(argv)
    M = MSG[args.lang]
    tags = TAGS[args.lang]

    text = read_text(args.input)
    pairs = read_names(args.names) if args.names else []
    if not args.detect_only:
        if not args.output:
            fail("err_needout")
        if not args.identity_map:
            fail("err_needmap")
        for p in (args.output, args.identity_map):
            if os.path.abspath(p) == os.path.abspath(args.input):
                fail("err_overwrite_in", p=p)
            if os.path.exists(p) and not args.force:
                fail("err_exists", p=p)
        if os.path.abspath(args.output) == os.path.abspath(args.identity_map):
            fail("err_samefile")

    identity = OrderedDict()  # (code, original) -> type
    counts = Counter()
    result = text

    # 1) patterns, over the original text (before touching names, so emails/URLs are not broken)
    hits = detect(text, tags)
    counters = Counter()
    labels = {}
    if not args.no_redact:
        pieces, pos = [], 0
        for start, end, tag, val in hits:
            key = (tag, val)
            if key not in labels:
                counters[tag] += 1
                labels[key] = "[%s_%d]" % (tag, counters[tag])
                identity[(labels[key], val)] = tag.lower()
            pieces.append(result[pos:start])
            pieces.append(labels[key])
            pos = end
        pieces.append(result[pos:])
        result = "".join(pieces)

    # 2) CSV names, longest variants first (with --detect-only they are counted, nothing is written)
    for name, code, typ in sorted(pairs, key=lambda p: -len(p[0])):
        rx = re.compile(r"(?<!\w)" + re.escape(name) + r"(?!\w)", re.IGNORECASE)
        n = len(rx.findall(result))
        if n:
            counts["name:" + name] = n
            identity[(code, name)] = typ
            result = rx.sub(code, result)
    unused = [n for n, _, _ in pairs if counts["name:" + n] == 0]

    # 3) capitalized candidates not covered (for human review)
    known = {n.lower() for n, _, _ in pairs}
    for _, _, _, v in hits:
        known.add(v.lower())
    cand = Counter(w for w in RE_CAPS.findall(text)
                   if w.lower() not in known and not any(w.lower() in k.split() for k in known))
    speaker_labels = set()
    for ln in text.splitlines():
        m = RE_LABEL.match(ln.strip())
        if m:
            speaker_labels.add(m.group(1).strip())

    mode = M["mode_dry"] if args.detect_only else M["mode_list"] if args.no_redact else M["mode_red"]
    print(M["report"] + "\n")
    print(M["warn"] + "\n")
    print(M["names_h"])
    print("\n".join("- %s x%d" % (k[5:], v) for k, v in counts.items()) or "- " + M["none"])
    if unused:
        print(M["unused"].format(s=", ".join(unused)))
    print("\n" + M["det_h"].format(mode=mode))
    if hits:
        for start, _, tag, val in hits:
            print(M["det_line"].format(l=text.count("\n", 0, start) + 1, t=tag, v=val))
    else:
        print("- " + M["none"])
    print("\n" + M["cand_h"])
    print(", ".join("%s (%d)" % kv for kv in cand.most_common(30)) or "- " + M["none"])
    if speaker_labels:
        print("\n" + M["labels_h"].format(s=", ".join(sorted(speaker_labels))))
    print("\n" + M["human_h"])
    print(M["human1"])
    print(M["human2"])

    if args.detect_only:
        print(M["dry"])
        return
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)

        def write_map(f):
            w = csv.writer(f)
            w.writerow(M["map_header"])
            for (code, orig), typ in identity.items():
                w.writerow([code, orig, typ])
        write_private(args.identity_map, write_map)
    except OSError as e:
        fail("err_write", e=e.strerror)
    print(M["written"].format(o=args.output, m=args.identity_map))


if __name__ == "__main__":
    main()
