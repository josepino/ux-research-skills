#!/usr/bin/env python3
"""Render a Markdown research report as a standalone, self-contained HTML file.

Python 3 standard library only. No network access, no JavaScript in the output.
All text from the Markdown is HTML-escaped, so untrusted content cannot inject
scripts or markup. Local images are embedded as base64 data URIs.

Supported Markdown: headings, paragraphs, **bold**, *italic*, ~~strike~~,
`code`, links, images, ordered/unordered/nested lists, task lists, tables,
blockquotes (participant quotes; end with a line starting with an em dash for
attribution), fenced code, horizontal rules, and callouts:
    > [!insight] text      > [!recommendation] text
    > [!risk] text         > [!note] text
Optional front matter at the top:  --- / title: ... / subtitle: ... / author: ...
/ date: ... / lang: ... / ---

Usage:
    python3 render_report.py --input report.md --output report.html --lang es
    python3 render_report.py -i r.md -o r.html --lang fr --labels labels.fr.json

Exit codes: 0 success, 1 input/labels/output error, 2 invalid arguments.
"""
import argparse
import base64
import datetime
import html
import json
import math
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COVER = os.path.join(SCRIPT_DIR, "..", "assets", "cover.png")  # optional; the built-in brand art is used when absent
TOOL_NAME = "UX Research Skills"
TOOL_VERSION = "2.2"
BRAND_DEFAULT = "UX Research"
RTL_LANGS = {"ar", "he", "fa", "ur"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024
IMAGE_MIMES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
               ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}
CALLOUTS = ("insight", "recommendation", "risk", "note")

LABELS = {
    "en": {
        "contents": "Contents", "skip": "Skip to content", "prepared_by": "Prepared by",
        "date": "Date", "generated_with": "Generated with UX Research Skills",
        "print_hint": "Tip: use your browser's Print / Save as PDF (A4) for a paper copy.",
        "callout_insight": "Insight", "callout_recommendation": "Recommendation",
        "callout_risk": "Risk", "callout_note": "Note",
        "cover_alt": "Report cover illustration", "table": "Table", "missing_image": "Image not found",
        "researcher": "UX Researcher", "organization": "Organization", "version": "Version", "generated": "Generated",
        "figure": "Figure", "chart_data": "Chart data", "page": "Page", "report_type": "Report",
        "no_researcher": "UX Researcher name not provided",
    },
    "es": {
        "contents": "Contenido", "skip": "Saltar al contenido", "prepared_by": "Preparado por",
        "date": "Fecha", "generated_with": "Generado con UX Research Skills",
        "print_hint": "Consejo: usa Imprimir / Guardar como PDF (A4) del navegador para una copia en papel.",
        "callout_insight": "Insight", "callout_recommendation": "Recomendación",
        "callout_risk": "Riesgo", "callout_note": "Nota",
        "cover_alt": "Ilustración de portada del informe", "table": "Tabla", "missing_image": "Imagen no encontrada",
        "researcher": "UX Researcher", "organization": "Organización", "version": "Versión", "generated": "Generado",
        "figure": "Figura", "chart_data": "Datos del gráfico", "page": "Página", "report_type": "Informe",
        "no_researcher": "Falta el nombre del UX Researcher",
    },
}


class RenderError(Exception):
    """A user-facing error (bad input, labels or output)."""


def warn(msg):
    print("warning: " + msg, file=sys.stderr)


# ----------------------------------------------------------------- inline ---
def esc(text):
    return html.escape(text, quote=True)


def safe_url(url):
    """Return the url if its scheme is allowed, else None."""
    u = re.sub(r"[\x00-\x20\x7f]", "", html.unescape(url))
    if not u:
        return None
    low = u.lower()
    if low.startswith(("http://", "https://", "mailto:", "#")):
        return u
    m = re.match(r"^[^/]*:", u)
    if m:  # some other scheme (javascript:, data:, file:, ...)
        return None
    return u


# ----------------------------------------------------------------- visuals ---
SERIES = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)", "var(--s5)", "var(--s6)"]
MAX_ITEMS = 30


def _num(v, what):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v or v in (float("inf"), float("-inf")):
        raise ValueError("%s must be a finite number" % what)
    return float(v)


def _fmt(v, unit=""):
    t = str(int(v)) if v == int(v) else ("%.1f" % v).rstrip("0").rstrip(".")
    return t + unit


def _short(text, n):
    text = str(text)
    return text if len(text) <= n else text[:n - 1] + "…"


def _series(spec):
    """Return (labels, [(name, values)]) from {"data": [[label, v]...]} or {"labels": [...], "series": [...]}."""
    if "data" in spec:
        data = spec["data"]
        if not isinstance(data, list) or not data:
            raise ValueError("data must be a non-empty list of [label, value]")
        labels = [str(d[0]) for d in data]
        vals = [_num(d[1], "value") for d in data]
        return labels, [(str(spec.get("series_name", "")), vals)]
    labels = [str(x) for x in spec.get("labels", [])]
    ser = spec.get("series")
    if not labels or not isinstance(ser, list) or not ser:
        raise ValueError('use "data": [["A", 3], ...] or "labels" plus "series": [{"name": ..., "values": [...]}]')
    out = []
    for s_ in ser[:6]:
        vals = [_num(v, "value") for v in s_.get("values", [])]
        if len(vals) != len(labels):
            raise ValueError("every series needs one value per label")
        out.append((str(s_.get("name", "")), vals))
    return labels, out


def _legend(series, x, y):
    if len([s_ for s_ in series if s_[0]]) < 1 or len(series) < 2:
        return ""
    out = ""
    for k, (name, _) in enumerate(series):
        out += '<rect x="%d" y="%d" width="12" height="12" rx="3" fill="%s"/><text class="ax" x="%d" y="%d">%s</text>' % (
            x, y + k * 20, SERIES[k], x + 18, y + 11 + k * 20, esc(_short(name, 26)))
    return out


def chart_svg(spec):
    kind = spec.get("type", "bar")
    if kind not in ("bar", "hbar", "line", "donut"):
        raise ValueError("type must be bar, hbar, line or donut")
    labels, series = _series(spec)
    if len(labels) > MAX_ITEMS:
        raise ValueError("too many categories (max %d)" % MAX_ITEMS)
    unit = str(spec.get("unit", ""))
    allv = [v for _, vals in series for v in vals]
    vmax = _num(spec["max"], "max") if "max" in spec else (max(allv) if max(allv) > 0 else 1.0)
    n = len(labels)
    W = 720
    if kind == "donut":
        vals = series[0][1]
        if any(v < 0 for v in vals) or sum(vals) <= 0:
            raise ValueError("donut values must be non-negative and not all zero")
        total = sum(vals)
        r, C = 78, 2 * math.pi * 78
        parts, off = "", 0.0
        for k, v in enumerate(vals):
            ln = v / total * C
            parts += ('<circle cx="130" cy="130" r="%d" fill="none" stroke="%s" stroke-width="44" stroke-dasharray="%.2f %.2f" '
                      'stroke-dashoffset="%.2f" transform="rotate(-90 130 130)"/>' % (r, SERIES[k % 6], ln, C - ln, -off))
            off += ln
        centre = "" if unit == "%" else '<text class="big" x="130" y="136" text-anchor="middle">%s</text>' % esc(_fmt(total, unit))
        leg = ""
        for k, (lab, v) in enumerate(zip(labels, vals)):
            y = 40 + k * 24
            leg += ('<rect x="300" y="%d" width="14" height="14" rx="3" fill="%s"/><text class="ax2" x="322" y="%d">%s</text>'
                    '<text class="val" x="700" y="%d" text-anchor="end">%s (%s%%)</text>') % (
                y, SERIES[k % 6], y + 12, esc(_short(lab, 30)), y + 12, esc(_fmt(v, unit if unit != "%" else "")),
                _fmt(round(v / total * 100, 1)))
        H = max(260, 60 + 24 * n)
        return W, H, parts + centre + leg
    if kind == "hbar":
        left, right, bh = 200, 80, 18
        grp = bh * len(series) + 3 * (len(series) - 1)
        row = grp + 14
        H = row * n + 20 + (20 * len(series) if len(series) > 1 else 0)
        pw = W - left - right
        out = ""
        for i, lab in enumerate(labels):
            y0 = 8 + i * row
            out += '<text class="ax2" x="%d" y="%d" text-anchor="end">%s</text>' % (left - 10, y0 + grp / 2 + 4, esc(_short(lab, 30)))
            for j, (_, vals) in enumerate(series):
                v = max(vals[i], 0)
                w = min(v / vmax, 1.0) * pw
                y = y0 + j * (bh + 3)
                out += '<rect x="%d" y="%.1f" width="%.1f" height="%d" rx="4" fill="%s"/>' % (left, y, max(w, 1), bh, SERIES[j])
                out += '<text class="val" x="%.1f" y="%.1f">%s</text>' % (left + w + 6, y + bh - 5, esc(_fmt(vals[i], unit)))
        out += '<line class="gridl" x1="%d" y1="4" x2="%d" y2="%d"/>' % (left, left, H - 8 - (20 * len(series) if len(series) > 1 else 0))
        out += _legend(series, left, H - 20 * len(series) - 2) if len(series) > 1 else ""
        return W, H, out
    # bar and line share a frame
    H, x0, x1, y0, y1 = 360, 56, W - 12, 24, 360 - (80 if n > 7 else 56)
    out = ""
    for g in range(5):
        v = vmax * g / 4
        y = y1 - (y1 - y0) * g / 4
        out += '<line class="gridl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/><text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (
            x0, y, x1, y, x0 - 8, y + 4, esc(_fmt(round(v, 2), unit)))
    gw = (x1 - x0) / n
    for i, lab in enumerate(labels):
        cx = x0 + gw * (i + 0.5)
        if n > 7:
            out += '<text class="ax" x="%.1f" y="%d" text-anchor="end" transform="rotate(-35 %.1f %d)">%s</text>' % (
                cx, y1 + 16, cx, y1 + 16, esc(_short(lab, 18)))
        else:
            out += '<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (cx, y1 + 20, esc(_short(lab, 16)))
    if kind == "bar":
        bw = gw * 0.72 / len(series)
        for i in range(n):
            for j, (_, vals) in enumerate(series):
                v = max(vals[i], 0)
                h = min(v / vmax, 1.0) * (y1 - y0)
                x = x0 + gw * i + gw * 0.14 + j * bw
                out += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>' % (x, y1 - h, max(bw - 2, 2), h, SERIES[j])
                out += '<text class="val" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (x + bw / 2, y1 - h - 5, esc(_fmt(vals[i], unit)))
    else:
        for j, (_, vals) in enumerate(series):
            pts = [(x0 + gw * (i + 0.5), y1 - min(max(v, 0) / vmax, 1.0) * (y1 - y0)) for i, v in enumerate(vals)]
            out += '<polyline fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round" points="%s"/>' % (
                SERIES[j], " ".join("%.1f,%.1f" % p for p in pts))
            for (px, py), v in zip(pts, vals):
                out += '<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="var(--bg)" stroke-width="2"/>' % (px, py, SERIES[j])
                if len(series) == 1:
                    out += '<text class="val" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (px, py - 10, esc(_fmt(v, unit)))
    out += '<line class="axisl" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x0, y1, x1, y1)
    out += _legend(series, x1 - 170, 4) if len(series) > 1 else ""
    return W, H, out


def chart_table(spec):
    labels, series = _series(spec)
    head = "<tr><th></th>%s</tr>" % "".join("<th>%s</th>" % esc(nm or "") for nm, _ in series)
    rows = "".join("<tr><th>%s</th>%s</tr>" % (esc(lab), "".join("<td>%s</td>" % esc(_fmt(v)) for _, vals in series for v in [vals[i]]))
                   for i, lab in enumerate(labels))
    return "<table>%s%s</table>" % (head, rows)


def matrix_svg(spec):
    items = spec.get("items")
    if not isinstance(items, list) or not items or len(items) > 20:
        raise ValueError('matrix needs "items": [{"label": ..., "x": 0-1, "y": 0-1}] (1 to 20 items)')
    W, H, x0, x1, y0, y1 = 720, 440, 74, 704, 18, 388
    qs = spec.get("quadrants") or []
    out = ""
    names = [str(q) for q in qs[:4]] + [""] * (4 - len(qs[:4]))
    fills = ["var(--q1)", "var(--q2)", "var(--q3)", "var(--q4)"]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    boxes = [(x0, y0), (mx, y0), (x0, my), (mx, my)]
    for k, (bx, by) in enumerate(boxes):
        out += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (bx, by, (x1 - x0) / 2, (y1 - y0) / 2, fills[k])
        if names[k]:
            out += '<text class="qn" x="%.1f" y="%.1f">%s</text>' % (bx + 12, by + 24, esc(_short(names[k], 30)))
    out += '<rect x="%d" y="%d" width="%d" height="%d" fill="none" class="axisl"/>' % (x0, y0, x1 - x0, y1 - y0)
    out += '<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % ((x0 + x1) / 2, H - 22, esc(str(spec.get("x_label", ""))))
    out += '<text class="ax" x="16" y="%.1f" text-anchor="middle" transform="rotate(-90 16 %.1f)">%s</text>' % (
        (y0 + y1) / 2, (y0 + y1) / 2, esc(str(spec.get("y_label", ""))))
    out += '<text class="ax" x="%d" y="%d">%s</text><text class="ax" x="%d" y="%d" text-anchor="end">%s</text>' % (
        x0, H - 40, esc(str(spec.get("x_low", ""))), x1, H - 40, esc(str(spec.get("x_high", ""))))
    out += '<text class="ax" x="%d" y="%d" text-anchor="end">%s</text><text class="ax" x="%d" y="%d" text-anchor="end">%s</text>' % (
        x0 - 6, y1, esc(str(spec.get("y_low", ""))), x0 - 6, y0 + 10, esc(str(spec.get("y_high", ""))))
    for k, it in enumerate(items, 1):
        x = min(max(_num(it.get("x"), "x"), 0), 1)
        y = min(max(_num(it.get("y"), "y"), 0), 1)
        cx, cy = x0 + 16 + x * (x1 - x0 - 32), y1 - 16 - y * (y1 - y0 - 32)
        out += ('<circle cx="%.1f" cy="%.1f" r="14" fill="var(--s2)" stroke="var(--bg)" stroke-width="2"/>'
                '<text class="pin" x="%.1f" y="%.1f" text-anchor="middle">%d</text>') % (cx, cy, cx, cy + 5, k)
    return W, H, out


def journey_svg(spec):
    stages = spec.get("stages")
    if not isinstance(stages, list) or not (2 <= len(stages) <= 8):
        raise ValueError('journey needs "stages": [{"name": ..., "score": 1-5, "note": ...}] (2 to 8 stages)')
    W, H, x0, x1, y0, y1 = 720, 320, 40, 690, 30, 250
    n = len(stages)
    out = ""
    for g in range(5):
        y = y1 - (y1 - y0) * g / 4
        out += '<line class="gridl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (x0, y, x1, y)
    out += '<text class="ax" x="%d" y="%d">%s</text>' % (x0, 16, esc(str(spec.get("y_high", ""))))
    out += '<text class="ax" x="%d" y="%d">%s</text>' % (x0, y1 + 16, esc(str(spec.get("y_low", ""))))
    pts = []
    gw = (x1 - x0) / n
    for i, st in enumerate(stages):
        sc = min(max(_num(st.get("score"), "score"), 1), 5)
        pts.append((x0 + gw * (i + 0.5), y1 - (sc - 1) / 4 * (y1 - y0), sc))
    out += '<polyline fill="none" stroke="var(--s2)" stroke-width="4" stroke-linejoin="round" points="%s"/>' % " ".join("%.1f,%.1f" % (p[0], p[1]) for p in pts)
    for i, ((px, py, sc), st) in enumerate(zip(pts, stages), 1):
        out += '<circle cx="%.1f" cy="%.1f" r="12" fill="var(--s1)" stroke="var(--bg)" stroke-width="2"/><text class="pin" x="%.1f" y="%.1f" text-anchor="middle">%d</text>' % (px, py, px, py + 4, i)
        out += '<text class="ax2" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (px, y1 + 40, esc(_short(st.get("name", ""), 16)))
    return W, H, out


def flow_html(spec):
    nodes = spec.get("steps") or spec.get("nodes")
    if not isinstance(nodes, list) or not (2 <= len(nodes) <= 14):
        raise ValueError('flow needs "steps": ["A", "B", ...] or [{"label": ..., "note": ...}] (2 to 14 steps)')
    hi = set(spec.get("highlight", [])) if isinstance(spec.get("highlight", []), list) else set()
    items = ""
    for i, nd in enumerate(nodes, 1):
        label, note = (nd.get("label", ""), nd.get("note", "")) if isinstance(nd, dict) else (nd, "")
        cls = ' class="hi"' if i in hi else ""
        items += "<li%s><span class=\"n\">%d</span><b>%s</b>%s</li>" % (
            cls, i, esc(str(label)), "<small>%s</small>" % esc(str(note)) if note else "")
    return '<ol class="flow c%d">%s</ol>' % (min(len(nodes), 4), items)


def journey_notes(spec):
    rows = "".join("<li><b>%s</b>%s</li>" % (esc(str(st.get("name", ""))), (" — " + esc(str(st.get("note")))) if st.get("note") else "")
                   for st in spec.get("stages", []))
    return '<ol class="journey-notes">%s</ol>' % rows


def matrix_legend(spec):
    return '<ol class="journey-notes">%s</ol>' % "".join("<li>%s</li>" % esc(str(it.get("label", ""))) for it in spec.get("items", []))


GUIDE = """UX Research Skills: report syntax (Markdown + JSON blocks)

Front matter (all optional except the researcher name, which must be given here or with --researcher):
---
title: Checkout usability study
subtitle: Findings and recommendations
type: Usability report            (small label on the cover)
author: Ana Pérez                  (the UX Researcher; alias: researcher)
role: Senior UX Researcher
organization: Acme
version: 1.0
date: 2026-10-15                   (study or delivery date; generation time is stamped automatically)
---

Screenshots (describe every one: what is seen and why it matters; never invent a screenshot):
![Checkout step 3 with the shipping cost shown for the first time](shots/step3.png "What is seen: the cost appears only at the last step. Why it matters: 4 of 6 participants hesitated here.")

Charts (JSON inside a ```chart fence; types: bar, hbar, line, donut):
{"type": "hbar", "title": "Participants who completed each task", "unit": "", "max": 6,
 "data": [["Find product", 6], ["Add to cart", 5], ["Pay", 2]], "caption": "n = 6 participants"}
{"type": "bar", "labels": ["Round 1", "Round 2"], "series": [{"name": "Success", "values": [3, 5]}, {"name": "Errors", "values": [4, 1]}]}

Diagrams (JSON inside a ```diagram fence; types: flow, matrix, journey):
{"type": "flow", "title": "Research flow", "steps": ["Plan", {"label": "Recruit", "note": "6 people"}, "Test", "Report"], "highlight": [3], "caption": "Sequence of the study."}
{"type": "matrix", "x_label": "Effort", "y_label": "Impact", "x_low": "Low", "x_high": "High", "y_low": "Low", "y_high": "High",
 "quadrants": ["Quick wins", "Big bets", "Fill-ins", "Avoid"], "items": [{"label": "Show shipping cost early", "x": 0.2, "y": 0.85}], "caption": "Placement is the team's estimate."}
{"type": "journey", "y_high": "Positive", "y_low": "Negative", "stages": [{"name": "Search", "score": 4, "note": "Finds items fast"}, {"name": "Pay", "score": 1, "note": "Surprised by the cost"}], "caption": "Scores are the researcher's rating."}

Callouts: > [!insight] ...   > [!recommendation] ...   > [!risk] ...   > [!note] ...
Always add a caption with n and the source of every figure. Charts only show numbers you were given."""


class Renderer:
    def __init__(self, base_dir, labels):
        self.base_dir = base_dir
        self.labels = labels
        self.ids = {}
        self.headings = []  # (level, id, plain text)
        self.fig_n = 0

    # image handling -----------------------------------------------------
    def image_html(self, alt, src):
        alt_e = esc(alt)
        raw = html.unescape(src).strip()
        if re.match(r"^data:image/(png|jpeg|gif|webp);base64,[A-Za-z0-9+/=]+$", raw):
            return '<img src="%s" alt="%s" loading="lazy">' % (esc(raw), alt_e)
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw) or raw.startswith("//"):
            # remote or unknown scheme: never fetched; keep a safe link only for http(s)
            u = safe_url(src)
            if u and u.lower().startswith(("http://", "https://")):
                return '<a href="%s" rel="noopener noreferrer">%s</a>' % (esc(u), alt_e or esc(u))
            return alt_e
        path = os.path.normpath(os.path.join(self.base_dir, raw))
        if not os.path.isfile(path) and os.path.isfile(os.path.normpath(raw)):
            path = os.path.normpath(raw)  # also accept a path relative to the current folder
        ext = os.path.splitext(path)[1].lower()
        if ext in IMAGE_MIMES and os.path.isfile(path):
            try:
                if os.path.getsize(path) <= MAX_IMAGE_BYTES:
                    with open(path, "rb") as fh:
                        data = base64.b64encode(fh.read()).decode("ascii")
                    return '<img src="data:%s;base64,%s" alt="%s" loading="lazy">' % (IMAGE_MIMES[ext], data, alt_e)
                warn("image too large to embed (>5MB): " + raw)
            except OSError as exc:
                warn("cannot read image %s: %s" % (raw, exc))
        else:
            warn("image not found or unsupported type: " + raw)
        return '<span class="missing-img">%s: %s</span>' % (esc(self.labels["missing_image"]), alt_e or esc(raw))

    # figures and visual blocks -------------------------------------------
    def figure(self, inner, caption, cls="shot", title=None):
        self.fig_n += 1
        if not caption and title:
            caption, title = title, None
        head = '<div class="fig-title">%s</div>' % self.inline(title) if title else ""
        cap = "<figcaption><strong>%s %d.</strong> %s</figcaption>" % (esc(self.labels["figure"]), self.fig_n, self.inline(caption) if caption else "")
        return '<figure class="figure %s">%s%s%s</figure>' % (cls, head, inner, cap)

    def lone_image(self, raw):
        m = re.match(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"(.*)")?\)$', raw.strip())
        if not m:
            return None
        alt, src, cap = m.group(1), m.group(2), m.group(3)
        if not alt.strip() and not cap:
            warn("screenshot without a description: %s (say what is seen and why it matters)" % src)
        img = self.image_html(alt or (cap or ""), src)
        return self.figure('<div class="shot-frame">%s</div>' % img, cap or alt)

    def visual_block(self, kind, text):
        try:
            spec = json.loads(text)
            if not isinstance(spec, dict):
                raise ValueError("the block must be one JSON object")
            title = spec.get("title")
            cap = spec.get("caption", "")
            if not cap:
                warn("%s without a caption: add one with n and the source" % kind)
            if kind == "chart":
                w, h, svg = chart_svg(spec)
                lab0, ser0 = _series(spec)
                desc = esc("; ".join("%s: %s" % (lb, _fmt(v)) for lb, v in zip(lab0, ser0[0][1])))
                inner = ('<svg class="svgfig" role="img" viewBox="0 0 %d %d" aria-label="%s"><title>%s</title><desc>%s</desc>%s</svg>'
                         '<div class="sr-only"><p>%s</p>%s</div>') % (w, h, esc(str(title or "")), esc(str(title or "")), desc, svg,
                                                                      esc(self.labels["chart_data"]), chart_table(spec))
                return self.figure(inner, cap, "chart", title)
            t = spec.get("type")
            if t == "flow":
                return self.figure(flow_html(spec), cap, "diagram", title)
            if t in ("matrix", "journey"):
                w, h, svg = (matrix_svg if t == "matrix" else journey_svg)(spec)
                extra = matrix_legend(spec) if t == "matrix" else journey_notes(spec)
                inner = '<svg class="svgfig" role="img" viewBox="0 0 %d %d" aria-label="%s"><title>%s</title>%s</svg>%s' % (
                    w, h, esc(str(title or t)), esc(str(title or t)), svg, extra)
                return self.figure(inner, cap, "diagram", title)
            raise ValueError("diagram type must be flow, matrix or journey")
        except (ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
            warn("%s block not rendered (%s); shown as code" % (kind, exc))
            return "<pre><code>%s</code></pre>" % esc(text)

    # inline markdown ----------------------------------------------------
    def inline(self, text):
        text = text.replace("\x00", "").replace("\x02", "")
        stash = []

        def put(htmltext):
            stash.append(htmltext)
            return "\x00%d\x00" % (len(stash) - 1)

        # code spans
        text = re.sub(r"(`+)(.+?)\1", lambda m: put("<code>%s</code>" % esc(m.group(2).strip())), text)
        # backslash escapes
        text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|>~<])", lambda m: put(esc(m.group(1))), text)
        text = esc(text)
        # images, then links
        text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;.*?&quot;)?\)",
                      lambda m: put(self.image_html(html.unescape(m.group(1)), m.group(2))), text)

        def link(m):
            label = self.inline_core(m.group(1), put)
            u = safe_url(m.group(2))
            if not u:
                return label
            ext = ' rel="noopener noreferrer"' if u.lower().startswith(("http://", "https://", "mailto:")) else ""
            return put('<a href="%s"%s>%s</a>' % (esc(u), ext, label))
        text = re.sub(r"\[([^\]]+)\]\(((?:[^()\s]|\([^()\s]*\))+)(?:\s+&quot;.*?&quot;)?\)", link, text)
        text = re.sub(r"&lt;(https?://[^\s&]+)&gt;",
                      lambda m: put('<a href="%s" rel="noopener noreferrer">%s</a>' % (m.group(1), m.group(1))), text)
        text = self.inline_core(text, put)
        text = text.replace("\x01", "<br>")
        # restore stash (may nest)
        for _ in range(4):
            text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
        return text

    @staticmethod
    def inline_core(text, put):
        text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w_])__(?=\S)(.+?)(?<=\S)__(?![\w_])", r"<strong>\1</strong>", text)
        text = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<del>\1</del>", text)
        text = re.sub(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"(?<![\w_])_(?=[^\s_])(.+?)(?<=[^\s_])_(?![\w_])", r"<em>\1</em>", text)
        return text

    @staticmethod
    def plain(text):
        t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
        t = re.sub(r"[`*_~\\]", "", t)
        return t.strip()

    def slug(self, text):
        s = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
        s = re.sub(r"[\s_]+", "-", s).strip("-") or "section"
        n = self.ids.get(s, 0)
        self.ids[s] = n + 1
        return s if n == 0 else "%s-%d" % (s, n)

    # blocks -------------------------------------------------------------
    LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
    HR_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
    FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([\w+#.-]*)")
    HEAD_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
    DELIM_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")

    def is_block_start(self, line, allow_list=True):
        if self.HR_RE.match(line) or self.FENCE_RE.match(line) or self.HEAD_RE.match(line):
            return True
        if line.lstrip().startswith(">"):
            return True
        if allow_list:
            m = self.LIST_RE.match(line)
            if m and (not m.group(2)[0].isdigit() or m.group(2).startswith("1")):
                return True
        return False

    @staticmethod
    def split_row(line):
        s = line.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|") and not s.endswith("\\|"):
            s = s[:-1]
        cells, cur, i = [], "", 0
        in_code = False
        while i < len(s):
            ch = s[i]
            if ch == "`":
                in_code = not in_code
            if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
                cur += "|"
                i += 2
                continue
            if ch == "|" and not in_code:
                cells.append(cur.strip())
                cur = ""
            else:
                cur += ch
            i += 1
        cells.append(cur.strip())
        return cells

    def parse_blocks(self, lines, tight=False):
        out, i, n = [], 0, len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            fm = self.FENCE_RE.match(line)
            if fm:
                fence, lang = fm.group(1), fm.group(2)
                i += 1
                buf = []
                while i < n and not re.match(r"^\s{0,3}%s{%d,}\s*$" % (re.escape(fence[0]), len(fence)), lines[i]):
                    buf.append(lines[i])
                    i += 1
                i += 1
                if lang in ("chart", "diagram"):
                    out.append(self.visual_block(lang, "\n".join(buf)))
                    continue
                cls = ' class="language-%s"' % esc(lang) if lang else ""
                out.append("<pre><code%s>%s</code></pre>" % (cls, esc("\n".join(buf))))
                continue
            hm = self.HEAD_RE.match(line)
            if hm:
                level = len(hm.group(1))
                txt = hm.group(2)
                hid = self.slug(self.plain(txt))
                self.headings.append((level, hid, self.plain(txt)))
                lvl = 2 if level == 1 else level
                out.append('<h%d id="%s">%s</h%d>' % (lvl, esc(hid), self.inline(txt), lvl))
                i += 1
                continue
            if self.HR_RE.match(line):
                out.append("<hr>")
                i += 1
                continue
            if "|" in line and i + 1 < n and self.DELIM_RE.match(lines[i + 1]) and "|" in lines[i + 1] + line:
                head = self.split_row(line)
                delim = self.split_row(lines[i + 1])
                if len(head) == len(delim):
                    aligns = []
                    for d in delim:
                        d = d.strip()
                        aligns.append("center" if d.startswith(":") and d.endswith(":") and len(d) > 1
                                      else "right" if d.endswith(":") else "left" if d.startswith(":") else "")
                    i += 2
                    rows = []
                    while i < n and lines[i].strip() and "|" in lines[i]:
                        rows.append(self.split_row(lines[i]))
                        i += 1

                    def cell(tag, txt, k):
                        a = ' class="a-%s"' % aligns[k] if aligns[k] else ""
                        sc = ' scope="col"' if tag == "th" else ""
                        return "<%s%s%s>%s</%s>" % (tag, a, sc, self.inline(txt), tag)
                    th = "".join(cell("th", c, k) for k, c in enumerate(head))
                    body = ""
                    for r in rows:
                        r = (r + [""] * len(head))[:len(head)]
                        body += "<tr>%s</tr>" % "".join(cell("td", c, k) for k, c in enumerate(r))
                    out.append('<div class="table-wrap" role="region" aria-label="%s" tabindex="0">'
                               "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>"
                               % (esc(self.labels["table"]), th, body))
                    continue
            if line.lstrip().startswith(">"):
                buf = []
                while i < n and lines[i].lstrip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                out.append(self.blockquote(buf))
                continue
            if self.LIST_RE.match(line):
                html_list, i = self.parse_list(lines, i)
                out.append(html_list)
                continue
            # paragraph
            buf = []
            while i < n and lines[i].strip() and not (buf and self.is_block_start(lines[i])):
                if buf and "|" in lines[i] and i + 1 < n and self.DELIM_RE.match(lines[i + 1]):
                    break
                raw = lines[i]
                hard = raw.endswith("  ") or raw.endswith("\\")
                t = raw.strip()
                if raw.endswith("\\"):
                    t = t[:-1]
                buf.append(t + ("\x01" if hard and i + 1 < n and lines[i + 1].strip() else ""))
                i += 1
            raw_par = " ".join(b.replace("\x01", "") for b in buf)
            fig = None if tight else self.lone_image(raw_par)
            if fig:
                out.append(fig)
                continue
            text = self.inline("\n".join(buf))
            out.append(text if tight else "<p>%s</p>" % text)
        return "\n".join(out)

    def blockquote(self, buf):
        # callout?
        first = next((k for k, l in enumerate(buf) if l.strip()), None)
        if first is not None:
            m = re.match(r"^\[!(\w+)\][ \t]*(.*)$", buf[first].strip())
            if m and m.group(1).lower() in CALLOUTS:
                kind = m.group(1).lower()
                inner = ([m.group(2)] if m.group(2) else []) + buf[first + 1:]
                label = self.labels["callout_" + kind]
                return ('<aside class="callout callout-%s"><p class="callout-label">%s</p>\n%s</aside>'
                        % (kind, esc(label), self.parse_blocks(inner)))
        # attribution line
        last = next((k for k in range(len(buf) - 1, -1, -1) if buf[k].strip()), None)
        if last is not None and last > 0:
            am = re.match(r"^(?:—|–|--)\s*(.+)$", buf[last].strip())
            if am:
                body = self.parse_blocks(buf[:last])
                return ('<figure class="quote"><blockquote>%s</blockquote><figcaption>— %s</figcaption></figure>'
                        % (body, self.inline(am.group(1))))
        return '<blockquote class="quote">%s</blockquote>' % self.parse_blocks(buf)

    def parse_list(self, lines, i):
        n = len(lines)
        m0 = self.LIST_RE.match(lines[i])
        base = len(m0.group(1))
        ordered = m0.group(2)[0].isdigit()
        start = int(re.match(r"\d+", m0.group(2)).group(0)) if ordered else None
        items = []
        while i < n:
            m = self.LIST_RE.match(lines[i])
            if not m or len(m.group(1)) >= base + 2 or m.group(2)[0].isdigit() != ordered:
                break
            content = [m.group(3)]
            i += 1
            has_blank = False
            while i < n:
                l = lines[i]
                if not l.strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and len(lines[j]) - len(lines[j].lstrip()) >= base + 2:
                        content.extend([""] * (j - i))
                        has_blank = True
                        i = j
                        continue
                    break
                ind = len(l) - len(l.lstrip())
                if ind >= base + 2:
                    content.append(l[base + 2:])
                elif self.LIST_RE.match(l) or self.is_block_start(l, allow_list=False):
                    break
                else:
                    content.append(l.strip())
                i += 1
            items.append((content, has_blank))
            # blank lines between sibling items
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and j > i:
                mm = self.LIST_RE.match(lines[j])
                if mm and len(mm.group(1)) < base + 2 and mm.group(2)[0].isdigit() == ordered:
                    i = j
        lis = []
        for content, loose in items:
            task = ""
            mt = re.match(r"^\[([ xX])\]\s+(.*)$", content[0])
            if mt:
                checked = mt.group(1) in "xX"
                content[0] = mt.group(2)
                task = '<input type="checkbox" disabled%s> ' % (" checked" if checked else "")
            body = self.parse_blocks(content, tight=not loose)
            cls = ' class="task"' if task else ""
            lis.append("<li%s>%s%s</li>" % (cls, task, body))
        tag = "ol" if ordered else "ul"
        st = ' start="%d"' % start if ordered and start not in (None, 1) else ""
        cls = ' class="tasks"' if any('class="task"' in x for x in lis) else ""
        return "<%s%s%s>\n%s\n</%s>" % (tag, st, cls, "\n".join(lis), tag), i


# ------------------------------------------------------------- front matter ---
def split_front_matter(text):
    meta = {}
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for k in range(1, min(len(lines), 40)):
            if lines[k].strip() == "---":
                for l in lines[1:k]:
                    m = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", l)
                    if m:
                        v = m.group(2).strip()
                        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                            v = v[1:-1]
                        meta[m.group(1).lower()] = v
                    elif l.strip():
                        meta = {}
                        break
                else:
                    return meta, "\n".join(lines[k + 1:])
                break
    return {}, text


# --------------------------------------------------------------------- css ---
CSS = """
:root{--s1:#3b82f6;--s2:#8b2cf5;--s3:#e11df0;--s4:#14b8a6;--s5:#f59e0b;--s6:#64748b;--q1:#eef4ff;--q2:#f4efff;--q3:#f6f6fb;--q4:#fdf0f2;--bg:#fff;--ink:#0a0a0a;--muted:#525264;--line:#e4e4ee;--soft:#f6f6fb;--card:#f4f1fd;--link:#5b21b6;
--g1:#3b82f6;--g2:#8b2cf5;--g3:#e11df0;--h-solid:#6d28d9;--c-insight:#1d4ed8;--c-rec:#15803d;--c-risk:#b91c1c;--c-note:#5b21b6;
--focus:#8b2cf5;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--s1:#60a5fa;--s2:#a78bfa;--s3:#f472b6;--s4:#2dd4bf;--s5:#fbbf24;--s6:#94a3b8;--q1:#14203a;--q2:#1e1838;--q3:#161622;--q4:#2a1620;--bg:#0b0b14;--ink:#f4f4fb;--muted:#a9a9c0;--line:#2a2a3d;
--soft:#14141f;--card:#1a1730;--link:#b99bff;--g1:#60a5fa;--g2:#a78bfa;--g3:#f472b6;--h-solid:#c4b5fd;--c-insight:#7db3ff;
--c-rec:#5fd38a;--c-risk:#ff8a8a;--c-note:#c4b5fd;--focus:#c4b5fd;color-scheme:dark}}
:root[data-theme="dark"]{--s1:#60a5fa;--s2:#a78bfa;--s3:#f472b6;--s4:#2dd4bf;--s5:#fbbf24;--s6:#94a3b8;--q1:#14203a;--q2:#1e1838;--q3:#161622;--q4:#2a1620;--bg:#0b0b14;--ink:#f4f4fb;--muted:#a9a9c0;--line:#2a2a3d;--soft:#14141f;--card:#1a1730;--link:#b99bff;
--g1:#60a5fa;--g2:#a78bfa;--g3:#f472b6;--h-solid:#c4b5fd;--c-insight:#7db3ff;--c-rec:#5fd38a;--c-risk:#ff8a8a;--c-note:#c4b5fd;
--focus:#c4b5fd;color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:1.2rem}
body{margin:0;background:var(--bg);color:var(--ink);font:1.125rem/1.7 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;
-webkit-text-size-adjust:100%}
a{color:var(--link);text-underline-offset:.15em}
a:focus-visible,.table-wrap:focus-visible,summary:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:4px}
.skip{position:absolute;inset-inline-start:1rem;top:-4rem;background:var(--ink);color:var(--bg);padding:.6rem 1rem;border-radius:8px;z-index:10}
.skip:focus{top:1rem}
.wrap{max-width:74rem;margin:0 auto;padding:0 1rem}
.cover{padding:2rem 0 1rem}
.cover-img{display:block;width:100%;max-height:22rem;object-fit:cover;border-radius:20px;border:1px solid var(--line)}
.cover h1{font-size:clamp(2.2rem,6vw,3.6rem);line-height:1.1;margin:1.6rem 0 .5rem;font-weight:800;letter-spacing:-.02em}
.grad{background:linear-gradient(90deg,var(--g1),var(--g2) 55%,var(--g3));-webkit-background-clip:text;background-clip:text;
-webkit-text-fill-color:transparent;color:var(--h-solid)}
.subtitle{font-size:1.35rem;color:var(--muted);margin:0 0 1rem}
.meta{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;color:var(--muted);font-size:1rem;margin:0;padding:0;list-style:none}
.meta strong{color:var(--ink)}
.layout{display:block;padding-bottom:3rem}
.toc{border:1px solid var(--line);background:var(--soft);border-radius:16px;padding:1rem 1.2rem;margin:1.2rem 0;font-size:.98rem}
.toc h2{font-size:1rem;margin:0 0 .5rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);-webkit-text-fill-color:currentColor;background:none}
.toc ol{list-style:none;margin:0;padding:0}.toc li{margin:.25rem 0;line-height:1.35}.toc .l3{padding-inline-start:1rem;font-size:.92rem}
.toc a{text-decoration:none;color:var(--ink)}.toc a:hover{color:var(--link);text-decoration:underline}
@media (min-width:62rem){.layout{display:grid;grid-template-columns:16rem minmax(0,1fr);gap:3rem;align-items:start}
.toc{position:sticky;top:1.2rem;max-height:calc(100vh - 2.4rem);overflow:auto;margin:0}}
.report{max-width:46rem;min-width:0}
.report>*:first-child{margin-top:0}
h2,h3,h4{line-height:1.2;margin:2.4rem 0 .8rem;letter-spacing:-.01em}
h2{font-size:2.1rem;font-weight:800;background:linear-gradient(90deg,var(--g1),var(--g2) 55%,var(--g3));-webkit-background-clip:text;
background-clip:text;-webkit-text-fill-color:transparent;color:var(--h-solid);padding-bottom:.15em}
h3{font-size:1.5rem;font-weight:750;border-inline-start:5px solid var(--g2);padding-inline-start:.7rem}
h4,h5,h6{font-size:1.15rem;font-weight:700}
p,ul,ol{margin:0 0 1.1rem}ul,ol{padding-inline-start:1.5rem}li{margin:.3rem 0}li>ul,li>ol{margin:.3rem 0 .3rem}
ul.tasks{list-style:none;padding-inline-start:.4rem}li.task input{margin-inline-end:.5rem;accent-color:var(--g2);transform:scale(1.2)}
strong{font-weight:750}
code{font:.88em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:.1em .35em}
pre{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:1rem;overflow:auto;margin:0 0 1.2rem;line-height:1.5}
pre code{background:none;border:0;padding:0;font-size:.9rem}
hr{border:0;height:3px;border-radius:3px;background:linear-gradient(90deg,var(--g1),var(--g2),var(--g3));opacity:.5;margin:2.5rem 0}
img{max-width:100%;height:auto;border-radius:12px}.missing-img{color:var(--c-risk);font-style:italic}
.table-wrap{overflow-x:auto;margin:0 0 1.4rem;border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:.98rem;line-height:1.45}
th,td{padding:.65rem .9rem;text-align:start;vertical-align:top;border-bottom:1px solid var(--line)}
th{background:var(--soft);font-weight:750;white-space:nowrap}tbody tr:nth-child(even){background:var(--soft)}tbody tr:last-child td{border-bottom:0}
.a-right{text-align:end}.a-center{text-align:center}
blockquote,figure.quote{margin:0 0 1.4rem}
blockquote.quote,figure.quote blockquote{background:var(--card);border-radius:16px;border-inline-start:6px solid var(--g2);padding:1rem 1.3rem;
font-size:1.2rem;font-style:italic;margin:0}
blockquote.quote p:last-child,figure.quote blockquote p:last-child{margin:0}
figure.quote{border-radius:16px}
figure.quote figcaption{margin:.5rem .4rem 0;color:var(--muted);font-size:.95rem;font-style:normal}
.callout{border-radius:14px;border:1px solid var(--line);border-inline-start:6px solid var(--cc);background:var(--soft);padding:.9rem 1.2rem;margin:0 0 1.4rem}
.callout>p:last-child,.callout>*:last-child{margin-bottom:0}
.callout-label{margin:0 0 .3rem;font-weight:800;font-size:.85rem;text-transform:uppercase;letter-spacing:.07em;color:var(--cc)}
.callout-insight{--cc:var(--c-insight)}.callout-recommendation{--cc:var(--c-rec)}.callout-risk{--cc:var(--c-risk)}.callout-note{--cc:var(--c-note)}
.footer{border-top:1px solid var(--line);color:var(--muted);font-size:.92rem;padding:1.5rem 0 2.5rem;margin-top:1rem}
.footer p{margin:.2rem 0}

.cover{padding:1.4rem 0 .6rem}
.cover-band{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:1rem}
.brand{display:flex;align-items:center;gap:.6rem;font-weight:800;letter-spacing:.01em}.brand svg,.brand img{height:2.2rem;width:auto;border-radius:10px}
.kicker{font-size:.8rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.25rem .8rem}
.cover-art{display:block;width:100%;height:auto;border-radius:20px;border:1px solid var(--line)}
.meta-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:.7rem;margin:1.4rem 0 0;padding:0}
.meta-grid div{border:1px solid var(--line);background:var(--soft);border-radius:14px;padding:.7rem 1rem;border-top:4px solid var(--g2)}
.meta-grid dt{font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0 0 .2rem}
.meta-grid dd{margin:0;font-weight:700;font-size:1.05rem;line-height:1.3}.meta-grid dd small{display:block;font-weight:400;color:var(--muted);font-size:.85rem}
.meta-grid .warn dd{color:var(--c-risk);font-style:italic}
.runfoot{display:none}
figure.figure{margin:0 0 1.6rem;border:1px solid var(--line);border-radius:16px;background:var(--soft);padding:.9rem 1rem 0;overflow:hidden}
.fig-title{font-weight:800;font-size:1.05rem;margin:0 0 .6rem}
.shot-frame{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;box-shadow:0 6px 22px rgba(60,30,120,.10);line-height:0}
.shot-frame img{display:block;width:100%;border-radius:0}
figure.figure figcaption{font-size:.95rem;color:var(--muted);padding:.7rem .2rem .9rem;line-height:1.45}
figure.figure figcaption strong{color:var(--ink)}
.svgfig{display:block;width:100%;height:auto}
.svgfig .ax{fill:var(--muted);font:12px system-ui,sans-serif}.svgfig .ax2{fill:var(--ink);font:13px system-ui,sans-serif}
.svgfig .val{fill:var(--ink);font:700 12px system-ui,sans-serif}.svgfig .big{fill:var(--ink);font:800 22px system-ui,sans-serif}
.svgfig .qn{fill:var(--muted);font:800 12px system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em}
.svgfig .pin{fill:#fff;font:800 12px system-ui,sans-serif}
.svgfig .gridl{stroke:var(--line);stroke-width:1}.svgfig .axisl{stroke:var(--muted);stroke-width:1.2}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
ol.flow{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem 2rem;margin:0 0 1rem;padding:.3rem 0}ol.flow.c2{grid-template-columns:repeat(2,minmax(0,1fr))}ol.flow.c3{grid-template-columns:repeat(3,minmax(0,1fr))}ol.flow.c4 li:nth-child(4n)::after,ol.flow.c3 li:nth-child(3n)::after,ol.flow.c2 li:nth-child(2n)::after{display:none}@media (max-width:40rem){ol.flow,ol.flow.c2,ol.flow.c3{grid-template-columns:1fr}ol.flow li::after{display:none!important}}
ol.flow li{position:relative;background:var(--bg);border:1px solid var(--line);border-top:4px solid var(--s2);border-radius:12px;padding:.7rem .8rem;margin:0}
ol.flow li.hi{border-top-color:var(--s3);box-shadow:0 0 0 2px var(--s3) inset}
ol.flow li:not(:last-child)::after{content:"\\2192";position:absolute;inset-inline-end:-1.55rem;top:50%;transform:translateY(-50%);color:var(--s2);font-weight:800;font-size:1.3rem}
[dir=rtl] ol.flow li:not(:last-child)::after{content:"\\2190"}
ol.flow .n{display:inline-flex;width:1.5rem;height:1.5rem;align-items:center;justify-content:center;border-radius:50%;background:var(--s2);color:#fff;font-size:.8rem;font-weight:800;margin-inline-end:.5rem}
ol.flow b{font-size:1rem}ol.flow small{display:block;color:var(--muted);margin-top:.3rem;font-size:.85rem;line-height:1.35}
ol.journey-notes{margin:.8rem 0 .2rem;padding-inline-start:1.4rem;font-size:.95rem}
@media (max-width:40rem){body{font-size:1.05rem}h2{font-size:1.7rem}h3{font-size:1.3rem}.subtitle{font-size:1.15rem}}
@media print{
:root,:root:not([data-theme="light"]),:root[data-theme="dark"]{--bg:#fff;--ink:#000;--muted:#444;--line:#cfcfdc;--soft:#f6f6fb;--card:#f4f1fd;
--link:#4c1d95;--h-solid:#5b21b6;--c-insight:#1d4ed8;--c-rec:#15803d;--c-risk:#b91c1c;--c-note:#5b21b6}
@page{size:A4;margin:18mm 16mm 20mm;@bottom-right{content:counter(page) " / " counter(pages);font-size:9pt;color:#555}}
body{font-size:11pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.skip,.no-print{display:none!important}.layout{display:block}.report{max-width:none}
.wrap{max-width:none;padding:0}.cover{padding:0 0 .5rem;page-break-after:avoid}.cover-img{max-height:9cm}
h2,h3,h4{page-break-after:avoid;break-after:avoid}.grad,h2{-webkit-text-fill-color:currentColor;background:none;color:var(--h-solid)}
.cover h1.grad{-webkit-text-fill-color:currentColor;background:none;color:var(--h-solid)}
h2{font-size:18pt}h3{font-size:14pt}
.cover{page-break-after:avoid;padding:0}.cover-art{border-radius:12px}.meta-grid{grid-template-columns:repeat(4,1fr)}
.toc{display:block!important;position:static;max-height:none;margin:.8rem 0 0;page-break-after:always;break-after:page}
.table-wrap{overflow:visible}figure.figure{background:#fff;break-inside:avoid;page-break-inside:avoid}
table,pre,blockquote,figure,.callout,img,tr{page-break-inside:avoid;break-inside:avoid}
.table-wrap{overflow:visible}a{color:inherit}}
"""


# ------------------------------------------------------------------ render ---
def load_labels(lang, labels_path):
    base = dict(LABELS["en"])
    base.update(LABELS.get(lang.split("-")[0].lower(), {}))
    if labels_path:
        try:
            with open(labels_path, encoding="utf-8") as fh:
                data = json.load(fh)
        except FileNotFoundError:
            raise RenderError("labels file not found: " + labels_path)
        except json.JSONDecodeError as exc:
            raise RenderError("labels file is not valid JSON (%s): %s" % (labels_path, exc))
        except (OSError, UnicodeDecodeError) as exc:
            raise RenderError("cannot read labels file %s: %s" % (labels_path, exc))
        if not isinstance(data, dict):
            raise RenderError("labels file must contain a JSON object of key: translated text")
        for k, v in data.items():
            if not isinstance(v, str):
                raise RenderError("label '%s' must be a string" % k)
            if k not in base:
                warn("unknown label key ignored: " + k)
            else:
                base[k] = v
    return base


def cover_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in IMAGE_MIMES:
        raise RenderError("cover must be png, jpg, gif, webp or svg: " + path)
    try:
        if os.path.getsize(path) > MAX_IMAGE_BYTES:
            raise RenderError("cover image is larger than 5MB: " + path)
        with open(path, "rb") as fh:
            return "data:%s;base64,%s" % (IMAGE_MIMES[ext], base64.b64encode(fh.read()).decode("ascii"))
    except FileNotFoundError:
        raise RenderError("cover image not found: " + path)
    except OSError as exc:
        raise RenderError("cannot read cover image %s: %s" % (path, exc))


def stamp(now=None):
    """Generation date, time and time zone, e.g. 2026-10-15 20:19 (UTC-03:00)."""
    now = now or datetime.datetime.now().astimezone()
    off = now.strftime("%z")
    tz = "UTC%s:%s" % (off[:3], off[3:]) if len(off) == 5 else "UTC"
    return "%s (%s)" % (now.strftime("%Y-%m-%d %H:%M"), tz)


BRAND_ART = (
    '<svg class="cover-art" viewBox="0 0 1200 240" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset=".55" stop-color="#8b2cf5"/>'
    '<stop offset="1" stop-color="#e11df0"/></linearGradient></defs>'
    '<rect width="1200" height="240" fill="url(#cg)"/>'
    '<circle cx="1010" cy="40" r="150" fill="#fff" fill-opacity=".10"/><circle cx="1130" cy="210" r="110" fill="#fff" fill-opacity=".10"/>'
    '<circle cx="120" cy="250" r="140" fill="#fff" fill-opacity=".08"/>'
    '<g fill="#fff" fill-opacity=".92"><rect x="420" y="130" width="46" height="64" rx="8"/><rect x="486" y="96" width="46" height="98" rx="8"/>'
    '<rect x="552" y="62" width="46" height="132" rx="8"/><rect x="618" y="110" width="46" height="84" rx="8"/></g>'
    '<g fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"><circle cx="820" cy="108" r="42"/><path d="M850 140l34 34"/></g>'
    '<path d="M800 108l14 14 28-30" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
BRAND_MARK = (
    '<svg viewBox="0 0 40 40" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="bm" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#3b82f6"/><stop offset=".55" stop-color="#8b2cf5"/><stop offset="1" stop-color="#e11df0"/></linearGradient></defs>'
    '<rect width="40" height="40" rx="10" fill="url(#bm)"/><g fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="18" cy="18" r="8"/><path d="M24 24l8 8"/><path d="M14.5 18l2.6 2.6 4.6-5"/></g></svg>')


def render(md, base_dir, lang, labels, title=None, subtitle=None, author=None, date=None,
           cover=None, theme="auto", researcher=None, role=None, organization=None, version=None,
           kicker=None, brand=None, brand_color=None, logo=None, generated=None, use_cover_art=True):
    md = md.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ").replace("\x01", "")
    meta, md = split_front_matter(md)
    title = title or meta.get("title")
    subtitle = subtitle or meta.get("subtitle")
    researcher = researcher or author or meta.get("researcher") or meta.get("author")
    role = role or meta.get("role")
    organization = organization or meta.get("organization")
    version = version or meta.get("version") or "1.0"
    kicker = kicker or meta.get("type")
    brand = brand or meta.get("brand") or BRAND_DEFAULT
    date = date or meta.get("date")
    generated = generated or stamp()
    if not researcher or not researcher.strip():
        warn("UX Researcher name is missing: ask the user for it and pass --researcher (or author: in the front matter)")
        researcher = None

    r = Renderer(base_dir, labels)
    lines = md.split("\n")
    for k, l in enumerate(lines):  # promote a leading H1 to the document title
        if l.strip():
            hm = Renderer.HEAD_RE.match(l)
            if hm and len(hm.group(1)) == 1:
                if not title:
                    title = r.plain(hm.group(2))
                lines.pop(k)
            break
    title = title or "Report"
    body = r.parse_blocks(lines)

    toc_items = [(2 if lv == 1 else lv, hid, txt) for lv, hid, txt in r.headings if lv in (1, 2, 3)]
    toc = ""
    if len(toc_items) >= 2:
        li = "".join('<li class="l%d"><a href="#%s">%s</a></li>' % (lv, esc(hid), esc(txt)) for lv, hid, txt in toc_items)
        toc = '<nav class="toc" aria-labelledby="toc-title"><h2 id="toc-title">%s</h2><ol>%s</ol></nav>' % (esc(labels["contents"]), li)

    who = esc(researcher) if researcher else esc(labels["no_researcher"])
    sub = " · ".join(esc(x) for x in (role, organization) if x)
    cards = [('<div%s><dt>%s</dt><dd>%s%s</dd></div>' % ("" if researcher else ' class="warn"', esc(labels["researcher"]), who,
                                                       "<small>%s</small>" % sub if sub and researcher else ""))]
    if date:
        cards.append("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(labels["date"]), esc(date)))
    cards.append("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(labels["version"]), esc(str(version))))
    cards.append("<div><dt>%s</dt><dd>%s</dd></div>" % (esc(labels["generated"]), esc(generated)))
    mark = '<img src="%s" alt="">' % esc(logo) if logo else BRAND_MARK
    if cover:
        art = '<img class="cover-art" src="%s" alt="%s">' % (esc(cover), esc(labels["cover_alt"]))
    elif use_cover_art:
        art = BRAND_ART % esc(labels["cover_alt"])
    else:
        art = ""
    header = ('<header class="cover wrap"><div class="cover-band"><div class="brand">%s<span>%s</span></div>%s</div>%s'
              '<h1 class="grad">%s</h1>%s<dl class="meta-grid">%s</dl></header>') % (
        mark, esc(brand), '<span class="kicker">%s</span>' % esc(kicker or labels["report_type"]), art, esc(title),
        '<p class="subtitle">%s</p>' % esc(subtitle) if subtitle else "", "".join(cards))
    foot_txt = " · ".join(x for x in (_short(title, 48), "%s %s" % (labels["version"], version), researcher or "", "%s %s" % (labels["generated"], generated)) if x)
    foot_css = '@media print{@page{@bottom-left{content:"%s";font-size:8pt;color:#555}}}' % foot_txt.replace("\\", "\\\\").replace('"', '\\"').replace("<", "").replace("\n", " ")
    runfoot = ""

    base_lang = lang.split("-")[0].lower()
    direction = "rtl" if base_lang in RTL_LANGS else "ltr"
    theme_attr = ' data-theme="%s"' % theme if theme in ("light", "dark") else ""
    extra_css = ""
    if brand_color:
        extra_css = ":root,:root[data-theme]{--g2:%s;--s2:%s;--h-solid:%s;--link:%s}" % ((brand_color,) * 4)
    return ("<!DOCTYPE html>\n<html lang=\"%s\" dir=\"%s\"%s>\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<meta name=\"generator\" content=\"%s %s render_report.py\">\n"
            "<meta name=\"author\" content=\"%s\"><meta name=\"version\" content=\"%s\"><meta name=\"generated\" content=\"%s\">\n"
            "<title>%s</title>\n<style>%s%s%s</style>\n</head>\n<body>\n"
            "<a class=\"skip\" href=\"#content\">%s</a>\n%s\n"
            "<div class=\"wrap layout\">\n%s\n<main id=\"content\" class=\"report\">\n%s\n</main>\n</div>\n%s\n"
            "<footer class=\"wrap footer\"><p>%s · %s %s</p><p class=\"no-print\">%s</p></footer>\n</body>\n</html>\n") % (
        esc(lang), direction, theme_attr, TOOL_NAME, TOOL_VERSION, esc(researcher or ""), esc(str(version)), esc(generated),
        esc(title), CSS, extra_css, foot_css, esc(labels["skip"]), header, toc, body, runfoot,
        esc(labels["generated_with"]), esc(labels["generated"]), esc(generated), esc(labels["print_hint"]))


# --------------------------------------------------------------------- pdf ---
def find_browser():
    cands = [os.environ.get("CHROME", ""),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
             r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
             "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "microsoft-edge"]
    for c in cands:
        if c and (os.path.isfile(c) or shutil.which(c)):
            return c
    return None


def html_to_pdf(html_text, pdf_path):
    browser = find_browser()
    if not browser:
        raise RenderError("no Chrome, Chromium or Edge found for the PDF (set the CHROME environment variable). "
                          "The HTML report was written: open it and use Print > Save as PDF (A4)")
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "report.html")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(html_text)
        os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--user-data-dir=" + os.path.join(tmp, "profile"),
               "--print-to-pdf=" + os.path.abspath(pdf_path), "file://" + page.replace(os.sep, "/") if os.sep == "/" else "file:///" + page.replace(os.sep, "/")]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RenderError("could not run %s: %s" % (browser, exc))
    if not os.path.isfile(pdf_path) or os.path.getsize(pdf_path) < 1000:
        raise RenderError("the browser did not produce the PDF: %s" % (res.stderr or "").strip()[-200:])


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render a Markdown research report as a branded, self-contained HTML file or PDF (stdlib only).",
        epilog="Callouts: > [!insight] / [!recommendation] / [!risk] / [!note]. Charts and diagrams: run with --guide. Exit codes: 0 ok, 1 error, 2 bad arguments.")
    ap.add_argument("-i", "--input", help="Markdown report to render")
    ap.add_argument("-o", "--output", help="HTML file to write; a name ending in .pdf writes a PDF instead")
    ap.add_argument("--pdf", action="store_true", help="also write a PDF next to the HTML (needs Chrome, Chromium or Edge)")
    ap.add_argument("--lang", default="en", help="language code of the report (html lang attribute; en and es have built-in labels)")
    ap.add_argument("--title", help="document title (default: front matter or first H1)")
    ap.add_argument("--subtitle", help="subtitle shown under the title")
    ap.add_argument("--researcher", "--author", dest="researcher", help="name of the UX Researcher shown on the cover (ask the user; never invent it)")
    ap.add_argument("--role", help="role of the researcher, e.g. Senior UX Researcher")
    ap.add_argument("--organization", help="organization shown under the researcher name")
    ap.add_argument("--version", help="report version shown on the cover (default 1.0; bump it on every revision)")
    ap.add_argument("--type", dest="kicker", help="small label on the cover, e.g. Usability report")
    ap.add_argument("--date", help="study or delivery date shown on the cover (generation time is stamped automatically)")
    ap.add_argument("--brand", help="brand or team name next to the logo (default: UX Research)")
    ap.add_argument("--brand-color", help="main accent colour as #rrggbb")
    ap.add_argument("--logo", help="your logo image (png/jpg/gif/webp/svg) shown on the cover")
    ap.add_argument("--cover", help="custom cover image instead of the built-in brand art")
    ap.add_argument("--no-cover", action="store_true", help="no cover art")
    ap.add_argument("--labels", help="JSON file with translated UI labels (see --print-labels)")
    ap.add_argument("--print-labels", action="store_true", help="print the English labels as JSON to translate and exit")
    ap.add_argument("--guide", action="store_true", help="print the syntax for front matter, screenshots, charts and diagrams, then exit")
    ap.add_argument("--strict", action="store_true", help="fail when the researcher name is missing")
    ap.add_argument("--generated", help=argparse.SUPPRESS)
    ap.add_argument("--theme", choices=("auto", "light", "dark"), default="auto", help="colour theme (default: follow the system)")
    a = ap.parse_args(argv)
    if a.guide:
        print(GUIDE)
        return 0
    if a.print_labels:
        print(json.dumps(LABELS["en"], ensure_ascii=False, indent=2))
        return 0
    if not a.input or not a.output:
        ap.error("-i/--input and -o/--output are required")
    try:
        if not re.match(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$", a.lang):
            raise RenderError("invalid --lang code: %r (use e.g. en, es, pt-BR, ar)" % a.lang)
        if a.brand_color and not re.match(r"^#[0-9a-fA-F]{6}$", a.brand_color):
            raise RenderError("--brand-color must look like #8b2cf5")
        try:
            with open(a.input, encoding="utf-8") as fh:
                md = fh.read()
        except FileNotFoundError:
            raise RenderError("input file not found: " + a.input)
        except IsADirectoryError:
            raise RenderError("input is a directory, not a file: " + a.input)
        except UnicodeDecodeError:
            raise RenderError("input is not valid UTF-8 text: " + a.input)
        except OSError as exc:
            raise RenderError("cannot read input %s: %s" % (a.input, exc))
        if not md.strip():
            raise RenderError("input file is empty: " + a.input)
        labels = load_labels(a.lang, a.labels)
        cover = cover_data_uri(a.cover) if (a.cover and not a.no_cover) else None
        if not cover and not a.no_cover and os.path.isfile(DEFAULT_COVER) and False:
            cover = cover_data_uri(DEFAULT_COVER)
        logo = cover_data_uri(a.logo) if a.logo else None
        pdf_mode = a.output.lower().endswith(".pdf")
        out = render(md, os.path.dirname(os.path.abspath(a.input)), a.lang, labels, a.title, a.subtitle, None, a.date, cover,
                     "light" if (pdf_mode or a.pdf) and a.theme == "auto" else a.theme, a.researcher, a.role, a.organization,
                     a.version, a.kicker, a.brand, a.brand_color, logo, a.generated, not a.no_cover)
        if a.strict and 'class="warn"' in out:
            raise RenderError("the UX Researcher name is missing (--strict)")
        written = []
        if not pdf_mode:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
                with open(a.output, "w", encoding="utf-8") as fh:
                    fh.write(out)
            except OSError as exc:
                raise RenderError("cannot write output %s: %s" % (a.output, exc))
            written.append("%s (%d KB)" % (a.output, (len(out.encode("utf-8")) + 1023) // 1024))
        if pdf_mode or a.pdf:
            pdf_path = a.output if pdf_mode else os.path.splitext(a.output)[0] + ".pdf"
            try:
                html_to_pdf(out, pdf_path)
            except RenderError:
                if pdf_mode:  # keep the report usable: leave the HTML next to the requested PDF
                    fb = os.path.splitext(a.output)[0] + ".html"
                    with open(fb, "w", encoding="utf-8") as fh:
                        fh.write(out)
                    print("wrote fallback " + fb, file=sys.stderr)
                raise
            written.append("%s (%d KB)" % (pdf_path, (os.path.getsize(pdf_path) + 1023) // 1024))
    except RenderError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote " + " and ".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
