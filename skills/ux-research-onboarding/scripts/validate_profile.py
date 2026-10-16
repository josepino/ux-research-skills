#!/usr/bin/env python3
"""Validate a research-profile.md file written by ux-research-onboarding.

Checks that the required fields are present and filled, that enumerated
fields use allowed values, that the file stays short, and warns when the
content looks like personal data or a secret (emails, phone numbers,
tokens, passwords). Python 3 standard library only.

Exit codes:
  0  valid (warnings may be printed)
  1  invalid: missing/empty required fields, bad values, or --strict warnings
  2  usage or file error (missing file, unreadable, empty input)
"""
import argparse
import re
import sys

REQUIRED = ["updated", "language", "audience", "researcher_name", "role", "experience", "product",
            "stage", "decisions_pending"]
RECOMMENDED = ["organization", "team", "users", "user_access", "time", "privacy_rules",
               "convincing_evidence", "output_formats", "detail_level"]
ALLOWED = {
    "experience": {"beginner", "intermediate", "advanced"},
    "stage": {"discover", "validate", "post-launch", "unknown"},
    "detail_level": {"brief", "standard", "deep"},
    "mode": {"practitioner", "learner", "consultant"},
}
MAX_LINES = 80
# Spanish key aliases accepted for convenience.
ALIASES = {
    "actualizado": "updated", "idioma": "language", "audiencia": "audience",
    "rol": "role", "nombre_investigador": "researcher_name", "investigador": "researcher_name", "organizacion": "organization", "experiencia": "experience", "equipo": "team",
    "producto": "product", "etapa": "stage", "decisiones_pendientes": "decisions_pending",
    "usuarios": "users", "acceso_usuarios": "user_access", "tiempo": "time",
    "reglas_privacidad": "privacy_rules", "evidencia_convincente": "convincing_evidence",
    "formatos": "output_formats", "nivel_detalle": "detail_level", "modo": "mode",
}
EMPTY_VALUES = {"", "tbd", "todo", "?", "-", "n/a", "..."}

PII_PATTERNS = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("phone", re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")),
    ("secret", re.compile(r"(?i)\b(?:password|passwd|contrase[nñ]a|api[_ -]?key|secret|token)\b\s*[:=]\s*\S+")),
    ("secret", re.compile(r"\b(?:sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[\w-]{10,})\b")),
    ("url-credentials", re.compile(r"https?://[^/\s:@]+:[^/\s@]+@")),
]

KIND_ES = {"email": "un correo electrónico", "phone": "un teléfono",
           "secret": "un secreto o credencial", "url-credentials": "credenciales en una URL"}

MSG = {
    "en": {
        "no_file": "Cannot read '{p}': {e}",
        "empty": "'{p}' is empty. Nothing to validate.",
        "missing": "ERROR: required field '{k}' is missing.",
        "blank": "ERROR: required field '{k}' is empty or a placeholder.",
        "badval": "ERROR: '{k}' has value '{v}'; allowed: {a}.",
        "reco": "WARNING: recommended field '{k}' is missing or empty.",
        "long": "WARNING: file has {n} lines; keep it under {m}.",
        "pii": "WARNING line {n}: looks like {kind} data. Profiles must not contain personal data or secrets.",
        "date": "ERROR: 'updated' should look like YYYY-MM-DD (got '{v}').",
        "ok": "Profile is valid ({w} warning(s)).",
        "bad": "Profile is invalid: {e} error(s), {w} warning(s).",
        "strict": "Strict mode: warnings are treated as errors.",
    },
    "es": {
        "no_file": "No se puede leer '{p}': {e}",
        "empty": "'{p}' está vacío. No hay nada que validar.",
        "missing": "ERROR: falta el campo obligatorio '{k}'.",
        "blank": "ERROR: el campo obligatorio '{k}' está vacío o es un marcador.",
        "badval": "ERROR: '{k}' tiene el valor '{v}'; permitidos: {a}.",
        "reco": "AVISO: falta o está vacío el campo recomendado '{k}'.",
        "long": "AVISO: el archivo tiene {n} líneas; mantenelo por debajo de {m}.",
        "pii": "AVISO línea {n}: parece contener {kind}. El perfil no debe tener datos personales ni secretos.",
        "date": "ERROR: 'updated' debe tener formato AAAA-MM-DD (se recibió '{v}').",
        "ok": "El perfil es válido ({w} aviso(s)).",
        "bad": "El perfil no es válido: {e} error(es), {w} aviso(s).",
        "strict": "Modo estricto: los avisos se tratan como errores.",
    },
}


def parse(text):
    """Return {key: value} from 'key: value' lines (comments after '#' stripped)."""
    fields = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "<!--", "-", "```")):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key = ALIASES.get(m.group(1).lower(), m.group(1).lower())
        value = re.sub(r"\s+#.*$", "", m.group(2)).strip()
        fields.setdefault(key, value)
    return fields


def validate(text, lang="en"):
    """Return (errors, warnings) as lists of message strings."""
    t = MSG[lang]
    errors, warnings = [], []
    fields = parse(text)
    for k in REQUIRED:
        if k not in fields:
            errors.append(t["missing"].format(k=k))
        elif fields[k].lower() in EMPTY_VALUES:
            errors.append(t["blank"].format(k=k))
    for k, allowed in ALLOWED.items():
        v = fields.get(k, "")
        if v and v.lower() not in EMPTY_VALUES:
            first = re.split(r"[\s;,]", v.lower(), 1)[0]
            if first not in allowed and k != "user_access":
                errors.append(t["badval"].format(k=k, v=v, a=", ".join(sorted(allowed))))
    if fields.get("updated") and not re.match(r"^\d{4}-\d{2}-\d{2}$", fields["updated"]):
        if fields["updated"].lower() not in EMPTY_VALUES:
            errors.append(t["date"].format(v=fields["updated"]))
    for k in RECOMMENDED:
        if k not in fields or fields[k].lower() in EMPTY_VALUES:
            warnings.append(t["reco"].format(k=k))
    n_lines = len(text.splitlines())
    if n_lines >= MAX_LINES:
        warnings.append(t["long"].format(n=n_lines, m=MAX_LINES))
    for i, line in enumerate(text.splitlines(), 1):
        if "example.com" in line:
            continue
        for kind, pat in PII_PATTERNS:
            if pat.search(line):
                if kind == "phone" and re.search(r"\d{4}-\d{2}-\d{2}", line) and not re.search(r"\+\d", line):
                    # ISO dates look like phone numbers; skip unless a '+' prefix.
                    stripped = re.sub(r"\d{4}-\d{2}-\d{2}", "", line)
                    if not pat.search(stripped):
                        continue
                warnings.append(t["pii"].format(n=i, kind=KIND_ES[kind] if lang == "es" else kind))
                break
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Validate a research-profile.md: required fields, allowed values, "
                    "length, and PII/secret-looking content.",
        epilog="Exit codes: 0 valid, 1 invalid, 2 usage or file error.")
    ap.add_argument("file", nargs="?", default="research-profile.md",
                    help="path to the profile (default: research-profile.md)")
    ap.add_argument("--lang", choices=["en", "es"], default="en",
                    help="language of messages (default: en)")
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    args = ap.parse_args(argv)
    t = MSG[args.lang]
    try:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as e:
        print(t["no_file"].format(p=args.file, e=e), file=sys.stderr)
        return 2
    if not text.strip():
        print(t["empty"].format(p=args.file), file=sys.stderr)
        return 2
    errors, warnings = validate(text, args.lang)
    for m in errors + warnings:
        print(m)
    bad = bool(errors) or (args.strict and bool(warnings))
    if args.strict and warnings and not errors:
        print(t["strict"])
    if bad:
        print(t["bad"].format(e=len(errors), w=len(warnings)))
        return 1
    print(t["ok"].format(w=len(warnings)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
