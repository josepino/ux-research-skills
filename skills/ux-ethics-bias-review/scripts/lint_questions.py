#!/usr/bin/env python3
"""Thin wrapper: runs the single question linter that lives in ux-interview-guide.

This folder does not duplicate the logic. It looks for the script in the sibling
skill (../../ux-interview-guide/scripts/lint_questions.py) and passes it the same
arguments (including --lang en|es, --only-alerts and --strict).
If you installed only ux-ethics-bias-review, also install ux-interview-guide.

Exit codes: those of the real linter (0 ok, 1 alerts with --strict, 2 bad input),
plus 2 if the sibling script cannot be found.
"""
import os
import runpy
import sys

SIBLING = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "ux-interview-guide", "scripts", "lint_questions.py"))
if not os.path.isfile(SIBLING):
    print("Error: cannot find ux-interview-guide/scripts/lint_questions.py next to this skill "
          f"(looked in {SIBLING}). Install the ux-interview-guide skill or copy that script here.",
          file=sys.stderr)
    sys.exit(2)
sys.argv[0] = SIBLING
runpy.run_path(SIBLING, run_name="__main__")
