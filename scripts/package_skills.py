#!/usr/bin/env python3
"""Build upload-ready zip files into ./dist

  dist/<skill>.zip                 one zip per skill (for Claude.ai: Settings > Capabilities > Skills)
  dist/ux-research-skills-all.zip  every skill in one archive
  dist/ux-research-skills-plugin.zip  the whole plugin (for Claude Code `--plugin-dir` or manual install)

Usage:  python3 scripts/package_skills.py [--skills-dir skills] [--out dist]
"""
import argparse
import sys
import zipfile
from pathlib import Path

SKIP = {"__pycache__", ".DS_Store"}


def files_under(folder: Path):
    for p in sorted(folder.rglob("*")):
        if p.is_file() and not (set(p.parts) & SKIP) and p.suffix != ".pyc":
            yield p


def main():
    ap = argparse.ArgumentParser(description="Package skills as zip files.")
    ap.add_argument("--skills-dir", default="skills")
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    skills_dir, out = Path(a.skills_dir), Path(a.out)
    if not skills_dir.is_dir():
        sys.exit(f"Error: skills directory not found: {skills_dir}")
    out.mkdir(parents=True, exist_ok=True)
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if not skills:
        sys.exit("Error: no skills found")

    with zipfile.ZipFile(out / "ux-research-skills-all.zip", "w", zipfile.ZIP_DEFLATED) as allz:
        for s in skills:
            target = out / f"{s.name}.zip"
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
                for f in files_under(s):
                    arc = Path(s.name) / f.relative_to(s)
                    z.write(f, arc)
                    allz.write(f, arc)
            print(f"wrote {target}")
    root = Path(".")
    with zipfile.ZipFile(out / "ux-research-skills-plugin.zip", "w", zipfile.ZIP_DEFLATED) as pz:
        for rel in [".claude-plugin", "skills", "LICENSE", "README.md"]:
            p = root / rel
            if p.is_file():
                pz.write(p, rel)
            elif p.is_dir():
                for f in files_under(p):
                    pz.write(f, f)
    print(f"wrote {out / 'ux-research-skills-plugin.zip'}")


if __name__ == "__main__":
    main()
