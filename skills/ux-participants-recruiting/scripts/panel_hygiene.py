#!/usr/bin/env python3
"""Hygiene report for a participant panel (CSV). Read-only.

Usage:
  python3 panel_hygiene.py panel.csv
  python3 panel_hygiene.py panel.csv --email email --fields job_title,country --threshold 0.85
  python3 panel_hygiene.py panel.csv --proposals proposed_changes.csv
  python3 panel_hygiene.py panel.csv --lang es

What it does (it never modifies the original file):
 - empty fields: percentage of empty cells per column
 - exact duplicates (identical rows) and duplicates by normalized email
   (lowercase, trimmed; for gmail, dots and +alias are ignored)
 - similar values in the chosen columns: grouped by simple normalization
   (lowercase, no accents, no punctuation) and by difflib similarity
 - with --proposals it writes a CSV of PROPOSED changes (column, current_value,
   proposed_value, reason, approved). Nothing is applied: a person reviews it
   and marks approved=yes; this script never applies changes.
Caveats:
 - Similarity groups are suggestions: "Employed"/"Unemployed" look alike but
   are not the same. Review each group.
 - Abbreviations and synonyms ("PM" vs "Product Manager") are NOT detected by
   shape: add them by hand to the proposals CSV. The report flags values that
   look like common job-title abbreviations so you can check them.
Column names: email column is auto-detected (email, e-mail, mail, correo,
correo electronico). Spanish and English panels both work.
Exit codes: 0 ok, 1 error (missing file, bad columns, empty input, existing
output file).
"""
import argparse
import csv
import difflib
import sys
import unicodedata
from collections import Counter, defaultdict

EMAIL_NAMES = ("email", "e-mail", "mail", "email address", "correo",
               "correo electronico", "correo electrónico")

# Common English job-title abbreviations (awareness list, NOT auto-merged).
# Spanish titles often reuse these too (PM, PO, UX).
TITLE_ABBREVIATIONS = {
    "pm": "product/project manager", "po": "product owner", "pmm": "product marketing manager",
    "vp": "vice president", "svp": "senior vice president", "evp": "executive vice president",
    "ceo": "chief executive officer", "cto": "chief technology officer",
    "cfo": "chief financial officer", "coo": "chief operating officer",
    "cpo": "chief product officer", "cmo": "chief marketing officer",
    "swe": "software engineer", "sde": "software development engineer",
    "dev": "developer", "eng": "engineer", "mgr": "manager", "dir": "director",
    "sr": "senior", "jr": "junior", "asst": "assistant", "assoc": "associate",
    "ux": "user experience (designer/researcher)", "uxr": "UX researcher",
    "ui": "user interface designer", "qa": "quality assurance", "ba": "business analyst",
    "hr": "human resources", "sm": "scrum master/senior manager", "tl": "team lead",
    "cs": "customer success/support", "csm": "customer success manager",
    "sdr": "sales development rep", "ae": "account executive", "ds": "data scientist",
}

TXT = {
    "en": {
        "panel": "Panel: %s · %d rows · %d columns",
        "empty": "== Empty fields ==", "empty_line": "  %-25s %5.1f %% empty (%d/%d)%s",
        "review": "  <- review",
        "dups": "== Duplicates ==", "exact": "  Identical rows: %d groups",
        "lines": "    file lines:", "email_dup": "  Repeated emails after normalizing (column '%s'): %d",
        "email_line": "    %s -> lines %s",
        "no_email": "  (no email column: use --email to check duplicates by email)",
        "similar": "== Similar values (suggestions; nothing is applied) ==",
        "col": "  Column '%s':", "none": "  Column '%s': no obvious variants",
        "proposed": "  -> proposed: '%s'",
        "same_form": "same form after normalizing", "close": "similar (difflib >= %.2f)",
        "grouped": "grouped",
        "abbr_head": "== Possible abbreviations (review by hand) ==",
        "abbr_line": "  Column '%s': '%s' (%d) may stand for: %s",
        "abbr_none": "  none found among the checked columns",
        "limit": "Limitation: abbreviations or synonyms (e.g. 'PM' vs 'Product Manager') are not detected by shape; add them by hand to the proposals CSV.",
        "wrote": "Wrote %d proposed changes to %s ('approved' column empty: a person decides).",
        "untouched": "The original file was not modified.",
        "hdr": ["column", "current_value", "proposed_value", "reason", "approved"],
        "e_empty": "the CSV is empty or has no headers.",
        "e_norows": "the CSV has no data rows.",
        "e_missing": "file '%s' does not exist.",
        "e_utf": "could not read '%s' as UTF-8; save it as UTF-8 CSV.",
        "e_read": "could not read '%s': %s",
        "e_thr": "--threshold must be between 0 and 1.",
        "e_ecol": "email column '%s' does not exist. Columns: %s",
        "e_cols": "columns not found: %s. Columns: %s",
        "e_exists": "'%s' already exists; choose another name (I do not overwrite).",
        "e_write": "could not write '%s': %s",
    },
    "es": {
        "panel": "Panel: %s · %d filas · %d columnas",
        "empty": "== Campos vacíos ==", "empty_line": "  %-25s %5.1f %% vacío (%d/%d)%s",
        "review": "  <- revisar",
        "dups": "== Duplicados ==", "exact": "  Filas idénticas: %d grupos",
        "lines": "    líneas del archivo:", "email_dup": "  Emails repetidos tras normalizar (columna '%s'): %d",
        "email_line": "    %s -> líneas %s",
        "no_email": "  (sin columna de email: usá --email para revisar duplicados por email)",
        "similar": "== Valores similares (sugerencias; nada se aplica) ==",
        "col": "  Columna '%s':", "none": "  Columna '%s': sin variantes obvias",
        "proposed": "  -> propuesto: '%s'",
        "same_form": "misma forma tras normalizar", "close": "parecidos (difflib >= %.2f)",
        "grouped": "agrupado",
        "abbr_head": "== Posibles siglas (revisar a mano) ==",
        "abbr_line": "  Columna '%s': '%s' (%d) podría significar: %s",
        "abbr_none": "  ninguna en las columnas revisadas",
        "limit": "Limitación: siglas o sinónimos (p. ej. «PM» vs «Product Manager») no se detectan por forma; agregalos a mano en el CSV de propuestas.",
        "wrote": "Escribí %d cambios propuestos en %s (columna 'aprobado' vacía: una persona decide).",
        "untouched": "El archivo original no fue modificado.",
        "hdr": ["columna", "valor_actual", "valor_propuesto", "motivo", "aprobado"],
        "e_empty": "el CSV está vacío o no tiene encabezados.",
        "e_norows": "el CSV no tiene filas de datos.",
        "e_missing": "no existe el archivo '%s'.",
        "e_utf": "no pude leer '%s' como UTF-8; guardalo como CSV UTF-8.",
        "e_read": "no pude leer '%s': %s",
        "e_thr": "--threshold debe estar entre 0 y 1.",
        "e_ecol": "la columna de email '%s' no existe. Columnas: %s",
        "e_cols": "columnas inexistentes: %s. Columnas: %s",
        "e_exists": "'%s' ya existe; elegí otro nombre (no sobrescribo).",
        "e_write": "no pude escribir '%s': %s",
    },
}


def norm(s):
    s = unicodedata.normalize("NFD", s.strip().lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join("".join(c if c.isalnum() else " " for c in s).split())


def norm_email(e):
    e = e.strip().lower()
    if "@" not in e:
        return e
    u, d = e.rsplit("@", 1)
    if d in ("gmail.com", "googlemail.com"):
        u = u.split("+")[0].replace(".", "")
        d = "gmail.com"
    return u + "@" + d


def make_fail(t):
    def fail(msg):
        print("Error: " + msg, file=sys.stderr)
        sys.exit(1)
    return fail


def read_csv(path, t, fail):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel
            r = csv.DictReader(f, dialect=dialect)
            if not r.fieldnames:
                fail(t["e_empty"])
            return r.fieldnames, list(r)
    except FileNotFoundError:
        fail(t["e_missing"] % path)
    except UnicodeDecodeError:
        fail(t["e_utf"] % path)
    except (OSError, csv.Error) as e:
        fail(t["e_read"] % (path, e))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", help="panel CSV (with headers)")
    p.add_argument("--email", help="email column (auto-detected if named email/mail/correo)")
    p.add_argument("--fields", "--campos", dest="fields",
                   help="comma-separated columns to check for similar values (default: all short-text columns)")
    p.add_argument("--threshold", "--umbral", dest="threshold", type=float, default=0.85,
                   help="difflib similarity 0-1 (default 0.85)")
    p.add_argument("--proposals", "--propuestas", dest="proposals",
                   help="path of a NEW CSV with proposed changes (never overwrites)")
    p.add_argument("--lang", choices=["en", "es"], default="en",
                   help="output language (default en)")
    a = p.parse_args()
    t = TXT[a.lang]
    fail = make_fail(t)
    if not 0 < a.threshold <= 1:
        fail(t["e_thr"])

    cols, rows = read_csv(a.csv, t, fail)
    if not rows:
        fail(t["e_norows"])
    n = len(rows)
    print(t["panel"] % (a.csv, n, len(cols)) + "\n")

    print(t["empty"])
    for c in cols:
        v = sum(1 for r in rows if not (r.get(c) or "").strip())
        print(t["empty_line"] % (c, 100 * v / n, v, n, t["review"] if v / n >= 0.3 else ""))

    print("\n" + t["dups"])
    seen = defaultdict(list)
    for i, r in enumerate(rows, start=2):
        seen[tuple((r.get(c) or "").strip() for c in cols)].append(i)
    ex = [v for v in seen.values() if len(v) > 1]
    print(t["exact"] % len(ex))
    for g in ex[:20]:
        print(t["lines"], ", ".join(map(str, g)))
    ecol = a.email
    if not ecol:
        ecol = next((c for c in cols if c.strip().lower() in EMAIL_NAMES), None)
    elif ecol not in cols:
        fail(t["e_ecol"] % (ecol, ", ".join(cols)))
    if ecol:
        bym = defaultdict(list)
        for i, r in enumerate(rows, start=2):
            e = norm_email(r.get(ecol) or "")
            if e:
                bym[e].append(i)
        dup = {k: v for k, v in bym.items() if len(v) > 1}
        print(t["email_dup"] % (ecol, len(dup)))
        for k, v in list(dup.items())[:20]:
            print(t["email_line"] % (k, ", ".join(map(str, v))))
    else:
        print(t["no_email"])

    if a.fields:
        fields = [c.strip() for c in a.fields.split(",")]
        bad = [c for c in fields if c not in cols]
        if bad:
            fail(t["e_cols"] % (", ".join(bad), ", ".join(cols)))
    else:
        fields = [c for c in cols if c != ecol
                  and 1 < len({(r.get(c) or "").strip() for r in rows}) <= max(50, n // 2)
                  and all(len(r.get(c) or "") <= 60 for r in rows)]

    print("\n" + t["similar"])
    props = []
    abbr_found = []
    for c in fields:
        cnt = Counter((r.get(c) or "").strip() for r in rows if (r.get(c) or "").strip())
        values = list(cnt)
        for v in values:
            key = norm(v).replace(" ", "")
            if key in TITLE_ABBREVIATIONS and len(norm(v).split()) <= 2:
                abbr_found.append((c, v, cnt[v], TITLE_ABBREVIATIONS[key]))
        parent = {v: v for v in values}

        def root(v):
            while parent[v] != v:
                v = parent[v]
            return v
        reason = {}
        for i, x in enumerate(values):
            for y in values[i + 1:]:
                nx, ny = norm(x), norm(y)
                if nx == ny:
                    m = t["same_form"]
                elif len(nx) > 3 and len(ny) > 3 and difflib.SequenceMatcher(None, nx, ny).ratio() >= a.threshold:
                    m = t["close"] % a.threshold
                else:
                    continue
                rx, ry = root(x), root(y)
                if rx != ry:
                    parent[ry] = rx
                    reason[y] = m
        groups = defaultdict(list)
        for v in values:
            groups[root(v)].append(v)
        found = False
        for g in groups.values():
            if len(g) > 1:
                if not found:
                    print(t["col"] % c)
                    found = True
                g.sort(key=lambda v: -cnt[v])
                print("    " + " | ".join("%s (%d)" % (v, cnt[v]) for v in g) + t["proposed"] % g[0])
                for v in g[1:]:
                    props.append([c, v, g[0], reason.get(v, t["grouped"]), ""])
        if not found:
            print(t["none"] % c)

    print("\n" + t["abbr_head"])
    if abbr_found:
        for c, v, k, meaning in abbr_found:
            print(t["abbr_line"] % (c, v, k, meaning))
    else:
        print(t["abbr_none"])
    print("\n" + t["limit"])

    if a.proposals:
        try:
            with open(a.proposals, "x", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(t["hdr"])
                w.writerows(props)
        except FileExistsError:
            fail(t["e_exists"] % a.proposals)
        except OSError as e:
            fail(t["e_write"] % (a.proposals, e))
        print("\n" + t["wrote"] % (len(props), a.proposals))
    print(t["untouched"])


if __name__ == "__main__":
    main()
