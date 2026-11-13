#!/usr/bin/env python3
"""
Build Vision Journey: a static, dependency-free learning site.

Content lives in courses/*.yml and lessons/<lang>/<course>/<lesson>.md as
markdown with front matter and three Vision Journey directives:

    :::demo{id="conv" title="Convolution explorer"} body :::     interactive lab
    :::model{src="resnet18" title="ResNet-18"} :::               ONNX graph viewer
    :::callout{type="warning" title="Careful"} body :::           aside

Usage: python3 tools/build.py
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
LANG = "en"

# The content engine lives beside the content, not inside this script.
sys.path.insert(0, str(ROOT))
from engine.tutorial import present_tutorial  # noqa: E402


def asset_version(rel: str) -> str:
    """Short content hash appended to asset URLs so edits are never hidden by browser cache."""
    path = ROOT / rel
    return hashlib.md5(path.read_bytes()).hexdigest()[:10] if path.exists() else "0"


CSS_V = asset_version("assets/css/style.css")
JS_V = {name: asset_version(f"assets/js/{name}") for name in ("app.js", "viz.js", "graph.js")}

# --------------------------------------------------------------------------------------
# Inline rendering
# --------------------------------------------------------------------------------------

def esc(text: str) -> str:
    return html.escape(text, quote=False)


def inline(text: str) -> str:
    """Render a small, safe Markdown inline subset."""
    text = esc(text)
    stash: list[str] = []

    def keep(value: str) -> str:
        stash.append(value)
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: keep(f'<code>{m.group(1)}</code>'), text)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: keep(
            f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">'
        ),
        text,
    )

    def link(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        attrs = ' rel="noopener"'
        if href.startswith("http"):
            attrs += ' target="_blank"'
        return keep(f'<a href="{href}"{attrs}>{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)

    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<em>\1</em>", text)

    # Inline math: keep TeX verbatim for KaTeX, which renders data-tex.
    text = re.sub(
        r"\$([^$\n]+)\$",
        lambda m: keep(
            f'<span class="math" data-tex="{html.escape(m.group(1), quote=True)}">{m.group(1)}</span>'
        ),
        text,
    )
    text = re.sub(r"\\([A-Za-z]+)", lambda m: keep("<kbd>" + m.group(1) + "</kbd>"), text)

    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def parse_attrs(raw: str) -> dict:
    """Parse {#id .class key="value" flag} into a dict."""
    attrs: dict = {"classes": []}
    if not raw:
        return attrs
    for token in re.findall(r'[\w-]+="[^"]*"|#[\w-]+|\.[\w-]+|[\w-]+', raw):
        if token.startswith("#"):
            attrs["id"] = token[1:]
        elif token.startswith("."):
            attrs["classes"].append(token[1:])
        elif "=" in token:
            key, value = token.split("=", 1)
            attrs[key] = value.strip('"')
        else:
            attrs.setdefault("flags", []).append(token)
    return attrs


# --------------------------------------------------------------------------------------
# Block rendering
# --------------------------------------------------------------------------------------

FENCE = re.compile(r"^```(\w*)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
UL = re.compile(r"^([-*+])\s+(.*)$")
OL = re.compile(r"^(\d+)\.\s+(.*)$")
TABLE = re.compile(r"^\|.*\|$")
HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")
DIRECTIVE = re.compile(r"^:::\s*([\w-]+)\s*(\{[^}]*\})?\s*(.*)$")


def is_block_start(line: str) -> bool:
    s = line.strip()
    return bool(
        not s
        or FENCE.match(s)
        or HEADING.match(s)
        or UL.match(s)
        or OL.match(s)
        or TABLE.match(s)
        or HR.match(s)
        or s.startswith(">")
        or s.startswith("$$")
        or s.startswith(":::")
    )


def render_table(rows: list[str]) -> str:
    def cells(row: str) -> list[str]:
        return [c.strip() for c in row.strip().strip("|").split("|")]

    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]] if len(rows) > 2 else []
    out = ['<div class="table-wrap"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out += ["</tr></thead><tbody>"]
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_quiz(attrs: dict, question: str, options: list[tuple[dict, str]]) -> str:
    quiz_id = attrs.get("id", "quiz")
    out = [
        f'<div class="quiz" data-quiz="{quiz_id}">',
        '<div class="quiz__eyebrow"><span class="quiz__dot"></span>Check your understanding</div>',
        f'<p class="quiz__question">{inline(question)}</p>',
        '<div class="quiz__options" role="group">',
    ]
    for opt_attrs, label in options:
        correct = "correct" in opt_attrs.get("classes", [])
        explain = opt_attrs.get("explanation", "")
        out.append(
            '<button type="button" class="quiz__option" '
            f'data-correct="{str(correct).lower()}" '
            f'data-explain="{html.escape(explain, quote=True)}">'
            f'<span class="quiz__marker"></span><span>{inline(label)}</span></button>'
        )
    out.append("</div>")
    out.append('<p class="quiz__feedback" role="status" hidden></p>')
    out.append("</div>")
    return "".join(out)


def render_demo(attrs: dict, title: str, body: str) -> str:
    demo_id = attrs.get("id", "")
    caption = title or attrs.get("title", "")
    return (
        f'<figure class="demo" data-demo="{demo_id}">'
        f'<div class="demo__head"><span class="demo__badge">Interactive</span>'
        f"<h4>{inline(caption)}</h4></div>"
        f'<div class="demo__stage"></div>'
        f'<figcaption class="demo__body">{body}</figcaption>'
        "</figure>"
    )


def render_callout(attrs: dict, body: str) -> str:
    kind = attrs.get("type", "note")
    title = attrs.get("title", kind.title())
    return (
        f'<aside class="callout callout--{html.escape(kind)}">'
        f'<p class="callout__title">{inline(title)}</p>{body}</aside>'
    )


def render_markdown(text: str, ctx: dict) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue

        # Fenced code
        m = FENCE.match(s)
        if m:
            lang = m.group(1)
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            code = esc("\n".join(buf))
            cls = f' class="language-{lang}"' if lang else ""
            out.append(
                '<div class="code"><button class="code__copy" type="button">Copy</button>'
                f"<pre><code{cls}>{code}</code></pre></div>"
            )
            continue

        # Display math
        if s.startswith("$$"):
            buf = [s]
            i += 1
            while not buf[-1].strip().endswith("$$") or len(buf[-1].strip()) < 4:
                if i >= len(lines):
                    break
                buf.append(lines[i])
                i += 1
            body = "\n".join(buf).strip()
            if body.startswith("$$"):
                body = body[2:]
            if body.endswith("$$"):
                body = body[:-2]
            body = body.strip()
            out.append(
                f'<div class="math-block" data-tex="{html.escape(body, quote=True)}">{esc(body)}</div>'
            )
            continue

        # Headings
        m = HEADING.match(s)
        if m:
            level = len(m.group(1))
            body = inline(m.group(2))
            anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            if level == 2:
                out.append(f'<h2 id="{anchor}">{body}</h2>')
                ctx["headings"].append((anchor, m.group(2)))
            elif level == 3:
                out.append(f'<h3 id="{anchor}">{body}</h3>')
            else:
                out.append(f'<h{level} id="{anchor}">{body}</h{level}>')
            i += 1
            continue

        # Directives
        if s.startswith(":::"):
            m = DIRECTIVE.match(s)
            if m:
                kind = m.group(1)
                attrs = parse_attrs(m.group(2) or "")
                rest = m.group(3) or ""
                i += 1

                if kind == "single-choice":
                    options: list[tuple[dict, str]] = []
                    while i < len(lines):
                        line = lines[i].strip()
                        if line.startswith(":::"):
                            i += 1
                            break
                        om = re.match(r"^::option\[(.*?)\]\{([^}]*)\}\s*$", line)
                        if om:
                            options.append((parse_attrs(om.group(2)), om.group(1)))
                        i += 1
                    out.append(render_quiz(attrs, rest, options))
                    continue

                body_lines = []
                while i < len(lines):
                    if lines[i].strip().startswith(":::"):
                        i += 1
                        break
                    body_lines.append(lines[i])
                    i += 1
                inner = render_markdown("\n".join(body_lines), {"headings": []})

                if kind == "demo":
                    out.append(render_demo(attrs, rest, inner))
                elif kind == "callout":
                    out.append(render_callout(attrs, inner))
                elif kind == "model":
                    src = attrs.get("src", "demo-cnn")
                    title = rest or attrs.get("title", src)
                    out.append(
                        f'<figure class="graph-embed" data-model="{html.escape(src)}">'
                        f'<div class="graph-embed__head"><span class="demo__badge">Computation graph</span>'
                        f"<h4>{inline(title)}</h4></div><div class=\"graph-embed__stage\"></div>"
                        "</figure>"
                    )
                else:
                    out.append(f'<section class="md-{kind}">{inner}</section>')
                continue

        # Table
        if TABLE.match(s):
            rows = []
            while i < len(lines) and TABLE.match(lines[i].strip()):
                rows.append(lines[i].strip())
                i += 1
            out.append(render_table(rows))
            continue

        # Blockquote
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{render_markdown(chr(10).join(buf), {'headings': []})}</blockquote>")
            continue

        # Lists
        if UL.match(s):
            items = []
            while i < len(lines) and UL.match(lines[i].strip()):
                items.append(inline(UL.match(lines[i].strip()).group(2)))
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        if OL.match(s):
            items = []
            while i < len(lines) and OL.match(lines[i].strip()):
                items.append(inline(OL.match(lines[i].strip()).group(2)))
                i += 1
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue

        if HR.match(s):
            out.append("<hr>")
            i += 1
            continue

        # Paragraph
        buf = [s]
        i += 1
        while i < len(lines) and not is_block_start(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")

    return "\n".join(out)


# --------------------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------------------

def load_site_config() -> dict:
    return yaml.safe_load((ROOT / "site.yml").read_text(encoding="utf-8"))


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    meta = yaml.safe_load(text[3:end]) or {}
    return meta, text[end + 4 :].lstrip("\n")


def load_courses() -> list[dict]:
    courses = []
    for path in sorted((ROOT / "courses").glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["slug"] = path.stem
        data["en"] = (data.get("translations") or {}).get(LANG, {})
        courses.append(data)
    courses.sort(key=lambda c: (c.get("order_index", 99), c["slug"]))
    return courses


def load_lessons(courses: list[dict]) -> dict[str, list[dict]]:
    by_course: dict[str, list[dict]] = {c["slug"]: [] for c in courses}
    for path in sorted((ROOT / "lessons" / LANG).glob("*/*.md")):
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        meta["slug"] = path.stem
        meta["course"] = path.parent.name
        meta["body"] = body
        meta["words"] = len(body.split())
        meta["minutes"] = max(4, round(meta["words"] / 190))
        if meta["course"] in by_course:
            by_course[meta["course"]].append(meta)
    for lessons in by_course.values():
        lessons.sort(key=lambda l: l.get("order_index", 99))
    return by_course


# --------------------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------------------

def course_art(slug: str, index: int) -> str:
    """Deterministic 'vision' cover art, generated as SVG (no binary assets)."""
    palettes = [
        ("#0f172a", "#22d3ee"), ("#111827", "#a78bfa"), ("#0b1220", "#34d399"),
        ("#161022", "#f472b6"), ("#101828", "#fbbf24"), ("#0c1a1a", "#60a5fa"),
        ("#1a1024", "#fb923c"), ("#0a1628", "#4ade80"), ("#1b1220", "#e879f9"),
        ("#0d1b2a", "#facc15"), ("#131313", "#38bdf8"), ("#0e1726", "#f87171"),
        ("#101820", "#2dd4bf"),
    ]
    bg, ink = palettes[index % len(palettes)]
    gid = f"g{index}"
    cells = []
    size, gap = 14, 4
    cols, rows = 12, 5
    for r in range(rows):
        for c in range(cols):
            v = ((c * 7 + r * 13 + index * 5) % 11) / 11
            x = 26 + c * (size + gap)
            y = 26 + r * (size + gap)
            op = 0.08 + v * 0.55
            cells.append(
                f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2" '
                f'fill="{ink}" opacity="{op:.2f}"/>'
            )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 150" role="img">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{bg}"/><stop offset="1" stop-color="#000"/></linearGradient>'
        f'<clipPath id="c{index}"><rect width="260" height="150" rx="12"/></clipPath></defs>'
        f'<g clip-path="url(#c{index})"><rect width="260" height="150" fill="url(#{gid})"/>'
        + "".join(cells)
        + f'<circle cx="215" cy="42" r="26" fill="none" stroke="{ink}" stroke-width="1.4" opacity=".55"/>'
        f'<circle cx="215" cy="42" r="13" fill="none" stroke="{ink}" stroke-width="1.4" opacity=".75"/>'
        f'<circle cx="215" cy="42" r="4" fill="{ink}" opacity=".9"/></g></svg>'
    )


LOGO = """<svg class="logo__mark" viewBox="0 0 32 32" aria-hidden="true"><path d="M2 16s5.2-8 14-8 14 8 14 8-5.2 8-14 8S2 16 2 16z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="16" cy="16" r="4.6" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="16" cy="16" r="1.7" fill="currentColor"/></svg>"""


def layout(
    *,
    cfg: dict,
    depth: int,
    title: str,
    description: str,
    body: str,
    body_class: str = "",
    nav_active: str = "",
    head_extra: str = "",
    show_sidebar: str = "",
) -> str:
    root = "../" * depth
    nav = ""
    for item in cfg.get("nav", []):
        active = " is-active" if item["id"] == nav_active else ""
        nav += f'<a class="nav__link{active}" href="{root}{item["href"]}">{item["label"]}</a>'
    return f"""<!doctype html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="dark light">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/css/style.css?v={CSS_V}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
{head_extra}
</head>
<body class="{body_class}" data-root="{root}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar__inner">
    <a class="logo" href="{root}index.html">{LOGO}<span class="logo__text">Vision<span>Journey</span></span></a>
    <nav class="nav" aria-label="Primary">{nav}</nav>
    <div class="topbar__actions">
      <button class="searchbtn" type="button" data-search-open aria-label="Search lessons">
        <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12.7 12.7 17 17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        <span>Search</span><kbd>⌘K</kbd>
      </button>
      <button class="iconbtn" type="button" data-theme-toggle aria-label="Toggle theme">◐</button>
      <button class="iconbtn menu-btn" type="button" data-menu-toggle aria-label="Toggle navigation">☰</button>
    </div>
  </div>
</header>
{show_sidebar}
<main id="main">{body}</main>
<footer class="footer">
  <div class="footer__inner">
    <p><strong>Vision Journey</strong> — an open curriculum for computer vision, from the camera obscura to foundation models.</p>
    <p class="footer__meta">Content licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a> · Code MIT</p>
  </div>
</footer>
<div class="search" data-search hidden>
  <div class="search__panel">
    <input class="search__input" type="search" placeholder="Search lessons, courses, models…" data-search-input autocomplete="off">
    <div class="search__results" data-search-results></div>
    <div class="search__hint">↑↓ navigate · ↵ open · esc close</div>
  </div>
</div>
<script src="{root}assets/js/app.js?v={JS_V['app.js']}" defer></script>
<script src="{root}assets/js/viz.js?v={JS_V['viz.js']}" defer></script>
<script src="{root}assets/js/graph.js?v={JS_V['graph.js']}" defer></script>
</body>
</html>"""


def sidebar(cfg: dict, courses: list[dict], lessons: dict, current_course: str, current_lesson: str, root: str) -> str:
    levels_html = []
    for level in cfg["levels"]:
        group = [c for c in courses if c.get("category", {}).get("id") == level["id"]]
        if not group:
            continue
        open_attr = " open" if any(c["slug"] == current_course for c in group) else ""
        items = ""
        for c in group:
            is_current = c["slug"] == current_course
            cls = " is-current" if is_current else ""
            if is_current:
                lesson_items = "".join(
                    f'<li><a class="side__lesson{" is-active" if l["slug"] == current_lesson else ""}" '
                    f'href="{root}lessons/{c["slug"]}/{l["slug"]}.html" data-lesson-link="{c["slug"]}/{l["slug"]}">'
                    f'<span class="side__num">{l.get("order_index", 0):02d}</span>{html.escape(l["title"])}</a></li>'
                    for l in lessons[c["slug"]]
                )
                items += (
                    f'<div class="side__course is-current{cls}">'
                    f'<a class="side__courselink" href="{root}courses/{c["slug"]}.html">{html.escape(c["en"].get("title", c["slug"]))}</a>'
                    f"<ul>{lesson_items}</ul></div>"
                )
            else:
                items += (
                    f'<div class="side__course{cls}">'
                    f'<a class="side__courselink" href="{root}courses/{c["slug"]}.html">{html.escape(c["en"].get("title", c["slug"]))}</a></div>'
                )
        levels_html.append(
            f'<details class="side__level"{open_attr}><summary>{level["rank"]}. {html.escape(level["name"])}</summary>{items}</details>'
        )
    # Only the sidebar itself: the lesson template owns the <div class="shell"> wrapper.
    # Emitting a shell here too used to nest two grids and squeeze the reading column
    # into the 280px sidebar track.
    return (
        '<aside class="sidebar" data-sidebar><div class="sidebar__inner">'
        f'<a class="side__back" href="{root}index.html">← Full curriculum</a>'
        + "".join(levels_html)
        + "</div></aside>"
    )


def shell_open() -> str:
    return '<div class="shell__content">'


def close_shell() -> str:
    return "</div></div>"


# --------------------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------------------

def ordered_pairs(courses: list[dict], lessons: dict) -> list[tuple[dict, dict]]:
    """Every (course, lesson) pair in curriculum order: courses by order_index, then lessons."""
    return [(c, l) for c in courses for l in lessons.get(c["slug"], [])]


def build_path_page(cfg: dict, courses: list[dict], lessons: dict) -> str:
    pairs = ordered_pairs(courses, lessons)
    total = len(pairs)
    total_minutes = sum(l["minutes"] for _, l in pairs)
    first_course, first_lesson = pairs[0]

    levels_html = ""
    pos = 0
    for level in cfg["levels"]:
        group = [c for c in courses if c.get("category", {}).get("id") == level["id"]]
        if not group:
            continue
        courses_html = ""
        for c in group:
            items = ""
            for l in lessons[c["slug"]]:
                pos += 1
                items += f"""<li><a class="path__item" href="lessons/{c['slug']}/{l['slug']}.html" data-lesson-link="{c['slug']}/{l['slug']}">
  <span class="path__num">{pos:02d}</span>
  <span class="path__title">{html.escape(l['title'])}</span>
  <span class="path__time">{l['minutes']} min</span>
  <span class="path__dot" data-progress-dot aria-hidden="true"></span>
</a></li>"""
            courses_html += f"""<div class="path__course">
  <div class="path__coursehead"><h3>{html.escape(c['en']['title'])}</h3><a href="courses/{c['slug']}.html">Course page →</a></div>
  <ol class="path__list">{items}</ol>
</div>"""
        levels_html += f"""<section>
  <div class="path__level"><h2>{html.escape(level['name'])}</h2><span>Level {level['rank']} · {html.escape(level['tagline'])}</span></div>
  {courses_html}
</section>"""

    body = f"""<div class="wrap">
<p class="eyebrow">Guided path</p>
<h1 class="page-title">Start at the beginning. Finish at the frontier.</h1>
<p class="lede">All {total} lessons in the order they are meant to be read: {total_minutes} minutes of material across three levels. Each lesson ends with a link to the next one, so you can keep going without returning here.</p>
<div class="path">
  <section class="path__cta">
    <div>
      <h2>{html.escape(first_lesson['title'])}</h2>
      <p>Level {cfg['levels'][0]['rank']} · {html.escape(first_course['en']['title'])}. Work through the list in order, or jump to the next unfinished lesson.</p>
      <p class="path__progress" data-path-progress>0 of {total} lessons complete</p>
      <div class="path__bar"><i data-path-bar></i></div>
    </div>
    <a class="btn btn--primary" data-continue href="lessons/{first_course['slug']}/{first_lesson['slug']}.html">Start lesson 01</a>
  </section>
  {levels_html}
</div>
</div>"""
    return layout(cfg=cfg, depth=0, title=f"Guided path — {cfg['title']}",
                  description=f"A single ordered path through all {total} lessons of Vision Journey, from image formation to research practice.",
                  body=body, body_class="page-path", nav_active="path")


def build_home(cfg: dict, courses: list[dict], lessons: dict) -> str:
    total_lessons = sum(len(v) for v in lessons.values())
    stats = [
        (str(len(courses)), "courses"),
        (str(total_lessons), "lessons"),
        ("9", "interactive labs"),
        ("5", "inspectable models"),
    ]
    stat_html = "".join(f'<div class="stat"><b>{n}</b><span>{label}</span></div>' for n, label in stats)

    levels_html = ""
    for level in cfg["levels"]:
        group = [c for c in courses if c.get("category", {}).get("id") == level["id"]]
        cards = ""
        for c in group:
            idx = courses.index(c)
            en = c["en"]
            count = len(lessons[c["slug"]])
            cards += f"""<a class="card" href="courses/{c['slug']}.html">
  <div class="card__art">{course_art(c['slug'], idx)}</div>
  <div class="card__body">
    <div class="card__meta"><span>{len(lessons[c['slug']])} lessons</span><span>{sum(l['minutes'] for l in lessons[c['slug']])} min</span></div>
    <h3>{html.escape(en.get('title', c['slug']))}</h3>
    <p>{inline(en.get('description', ''))}</p>
    <span class="card__cta">Explore course <span aria-hidden="true">→</span></span>
  </div>
</a>"""
        levels_html += f"""<section class="level" id="{level['id']}">
  <div class="level__head">
    <div class="level__rank">{level['rank']}</div>
    <div>
      <h2>{html.escape(level['name'])} <span class="level__tag">{html.escape(level['tagline'])}</span></h2>
      <p>{inline(level['description'])}</p>
    </div>
    <a class="btn btn--ghost" href="levels/{level['id']}.html">Level overview</a>
  </div>
  <div class="grid">{cards}</div>
</section>"""

    history_rail = "".join(
        f'<li><span class="t">{html.escape(item["year"])}</span><span>{inline(item["event"])}</span></li>'
        for item in cfg.get("timeline", [])
    )

    body = f"""
<section class="hero">
  <div class="hero__inner">
    <p class="eyebrow">An open curriculum · 1960 → today</p>
    <h1>Learn computer vision the way it <em>actually</em> happened.</h1>
    <p class="hero__lede">From pinhole cameras and edge detectors to convolutional networks, transformers and Gaussian splatting. Read the ideas, run the math, open the architectures, then reproduce the papers.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="path.html">Start the guided path</a>
      <a class="btn btn--ghost" href="models.html">Open the model lab</a>
    </div>
    <div class="stats">{stat_html}</div>
  </div>
  <aside class="hero__rail">
    <p class="hero__railtitle">The short version</p>
    <ol class="timeline">{history_rail}</ol>
  </aside>
</section>

<section class="principles">
  <div class="principle"><h3>Read the primary source</h3><p>Every lesson points at the paper, spec or canonical text behind the idea — not just a blog summary.</p></div>
  <div class="principle"><h3>See inside the model</h3><p>Real ONNX graphs, tensor shapes and layer costs. Zoom into ResNet, ViT and U-Net instead of trusting a diagram.</p></div>
  <div class="principle"><h3>Build to the research bar</h3><p>Evaluation protocol, ablations, reproducibility and failure modes are taught as first-class skills.</p></div>
</section>

{levels_html}
"""
    return layout(
        cfg=cfg,
        depth=0,
        title=f"{cfg['title']} — {cfg['tagline']}",
        description=cfg["description"],
        body=body,
        body_class="page-home",
        nav_active="home",
    )


def build_level(cfg: dict, courses: list[dict], lessons: dict, level: dict) -> str:
    group = [c for c in courses if c.get("category", {}).get("id") == level["id"]]
    rows = ""
    for c in group:
        idx = courses.index(c)
        rows += f"""<a class="rowcard" href="../courses/{c['slug']}.html">
  <div class="rowcard__art">{course_art(c['slug'], idx)}</div>
  <div class="rowcard__body"><h3>{html.escape(c['en']['title'])}</h3><p>{inline(c['en']['description'])}</p>
  <p class="rowcard__meta">{len(lessons[c['slug']])} lessons · {sum(l['minutes'] for l in lessons[c['slug']])} min · {', '.join(html.escape(l['title']) for l in lessons[c['slug']])}</p></div>
  <span class="rowcard__arrow" aria-hidden="true">→</span>
</a>"""
    body = f"""<div class="wrap">
<p class="eyebrow">Level {level['rank']} · {html.escape(level['tagline'])}</p>
<h1 class="page-title">{html.escape(level['name'])}</h1>
<p class="lede">{inline(level['description'])}</p>
<div class="stack">{rows}</div>
</div>"""
    return layout(cfg=cfg, depth=1, title=f"{level['name']} — {cfg['title']}",
                  description=level["description"], body=body, body_class="page-level",
                  nav_active="journey")


def build_course(cfg: dict, courses: list[dict], lessons: dict, course: dict) -> str:
    en = course["en"]
    items = ""
    for l in lessons[course["slug"]]:
        items += f"""<li><a class="lessonitem" href="../lessons/{course['slug']}/{l['slug']}.html" data-lesson-link="{course['slug']}/{l['slug']}">
  <span class="lessonitem__num">{l.get('order_index', 0):02d}</span>
  <span class="lessonitem__body"><strong>{html.escape(l['title'])}</strong><em>{inline(l.get('description', ''))}</em></span>
  <span class="lessonitem__time">{l['minutes']} min</span>
  <span class="lessonitem__check" data-progress-dot aria-hidden="true"></span>
</a></li>"""
    faqs = ""
    for faq in en.get("faqs", []) or []:
        faqs += f'<details class="faq"><summary>{inline(faq["question"])}</summary><p>{inline(faq["answer"])}</p></details>'

    level = next((lv for lv in cfg["levels"] if lv["id"] == course.get("category", {}).get("id")), None)
    course_lessons = lessons[course["slug"]]
    total = sum(l["minutes"] for l in course_lessons)
    start = (
        f'<a class="btn btn--primary" href="../lessons/{course["slug"]}/{course_lessons[0]["slug"]}.html">Start course</a>'
        if course_lessons
        else '<p class="muted">Lessons for this course are being prepared.</p>'
    )
    body = f"""<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Curriculum</a><span>/</span>
<a href="../levels/{level['id']}.html">{html.escape(level['name'])}</a><span>/</span><span>{html.escape(en['title'])}</span></nav>
<header class="coursehead">
  <div class="coursehead__art">{course_art(course['slug'], courses.index(course))}</div>
  <div>
    <p class="eyebrow">{html.escape(level['name'])} · Course {course.get('order_index', 0) + 1}</p>
    <h1>{html.escape(en['title'])}</h1>
    <p class="lede">{inline(en['description'])}</p>
    <p class="coursehead__meta">{len(lessons[course['slug']])} lessons · {total} min · {sum(l['words'] for l in lessons[course['slug']]):,} words</p>
    {start}
  </div>
</header>
<ol class="lessons">{items}</ol>
{f'<h2 class="block-title">Questions this course answers</h2><div class="faqs">{faqs}</div>' if faqs else ''}
</div>"""
    return layout(cfg=cfg, depth=1, title=f"{en['title']} — {cfg['title']}",
                  description=en.get("meta_description", en.get("description", "")),
                  body=body, body_class="page-course", nav_active="journey")


def build_lesson(cfg: dict, courses: list[dict], lessons: dict, course: dict, lesson: dict) -> str:
    ctx = {"headings": []}
    content = render_markdown(lesson["body"], ctx)
    flat = ordered_pairs(courses, lessons)
    pos = next(i for i, (c, l) in enumerate(flat)
               if c["slug"] == course["slug"] and l["slug"] == lesson["slug"])
    prev_pair = flat[pos - 1] if pos > 0 else None
    next_pair = flat[pos + 1] if pos + 1 < len(flat) else None

    toc = ""
    if len(ctx["headings"]) > 1:
        toc = '<aside class="toc"><p class="toc__title">On this page</p><ol>' + "".join(
            f'<li><a href="#{a}">{inline(t)}</a></li>' for a, t in ctx["headings"]
        ) + "</ol></aside>"

    level = next((lv for lv in cfg["levels"] if lv["id"] == course.get("category", {}).get("id")), None)
    nav = ""
    if prev_pair:
        pc, pl = prev_pair
        nav += (f'<a class="pager__link pager__link--prev" href="../{pc["slug"]}/{pl["slug"]}.html">'
                f'<span>Previous · {html.escape(pc["en"]["title"])}</span><strong>{html.escape(pl["title"])}</strong></a>')
    if next_pair:
        nc, nl = next_pair
        nav += (f'<a class="pager__link pager__link--next" href="../{nc["slug"]}/{nl["slug"]}.html">'
                f'<span>Next · {html.escape(nc["en"]["title"])}</span><strong>{html.escape(nl["title"])}</strong></a>')
    else:
        nav += ('<a class="pager__link pager__link--next" href="../../path.html">'
                '<span>Curriculum complete</span><strong>Review the guided path</strong></a>')

    # The engine presents the tutorial: one paragraph (with the heading it belongs
    # to) per step, checks inline, Continue centred underneath. app.js only switches.
    finish_href = f'../{next_pair[0]["slug"]}/{next_pair[1]["slug"]}.html' if next_pair else "../../path.html"
    finish_label = "Next lesson" if next_pair else "Back to the path"
    tutorial = present_tutorial(content, finish_href=finish_href, finish_label=finish_label)
    steps_html, stepper = tutorial.steps_html, tutorial.controls_html

    body = f"""<div class="shell">
{sidebar(cfg, courses, lessons, course["slug"], lesson["slug"], "../../")}
<div class="shell__content">
<article class="lesson" data-lesson="{course['slug']}/{lesson['slug']}">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Curriculum</a><span>/</span>
  <a href="../../levels/{level['id']}.html">{html.escape(level['name'])}</a><span>/</span>
  <a href="../../courses/{course['slug']}.html">{html.escape(course['en']['title'])}</a></nav>
  <header class="lesson__head">
    <p class="eyebrow">Lesson {pos + 1:02d} of {len(flat)} · {lesson['minutes']} min read</p>
    <h1>{html.escape(lesson['title'])}</h1>
    <p class="lede">{inline(lesson.get('description', ''))}</p>
    <button class="chip" type="button" data-complete="{course['slug']}/{lesson['slug']}">
      <span class="chip__box" aria-hidden="true"></span><span data-complete-label>Mark as complete</span>
    </button>
  </header>
  <div class="prose">{steps_html}</div>
  {stepper}
  <footer class="lesson__foot">
    <p class="lesson__license">Found an error or want to go deeper? <a href="https://github.com/" target="_blank" rel="noopener">Open a PR</a> — this curriculum is versioned like software.</p>
    <nav class="pager" aria-label="Lesson navigation">{nav}</nav>
  </footer>
</article>
{toc}
</div></div>"""
    return layout(cfg=cfg, depth=2, title=f"{lesson['title']} — {course['en']['title']}",
                  description=lesson.get("meta_description", lesson.get("description", "")),
                  body=body, body_class="page-lesson", nav_active="journey",
                  head_extra=f'<meta name="keywords" content="{html.escape(lesson.get("meta_keywords", ""), quote=True)}">')


# --------------------------------------------------------------------------------------
# Extra pages
# --------------------------------------------------------------------------------------

def build_models_page(cfg: dict, catalog: dict) -> str:
    cards = ""
    for m in catalog["models"]:
        cards += f"""<button class="modelcard" type="button" data-model-pick="{m['id']}">
  <span class="modelcard__name">{html.escape(m['name'])}</span>
  <span class="modelcard__meta">{m['params']} · {m['size']}</span>
  <span class="modelcard__task">{html.escape(m['task'])}</span>
</button>"""

    netron_rows = ""
    for m in catalog["models"]:
        netron_rows += f"""<li><button class="linkbtn" type="button" data-netron-open="{m['file']}">{html.escape(m['name'])}</button>
      <span>{html.escape(m['task'])} · <a href="models/{m['file']}" download>download .onnx</a></span></li>"""

    body = f"""<div class="wrap wrap--wide">
<header class="pagehead">
  <p class="eyebrow">Model lab</p>
  <h1>Look inside the architecture.</h1>
  <p class="lede">Networks are not black boxes — they are directed graphs of typed tensor operations. Trace the shapes, count the FLOPs and find the layer where a 224×224 image becomes a 7×7 grid of semantics.</p>
</header>

<section class="lab">
  <div class="lab__panel">
    <p class="panel__title">Local models <span>(exported from PyTorch, inspectable offline)</span></p>
    <div class="modelpicker">{cards}</div>
    <div class="lab__controls">
      <label class="field"><span>Layout</span>
        <select data-graph-layout><option value="vertical">Vertical</option><option value="horizontal">Horizontal</option></select>
      </label>
      <label class="field"><span>Detail</span>
        <select data-graph-detail><option value="all">All nodes</option><option value="blocks">Collapse repeats</option></select>
      </label>
      <button class="btn btn--ghost btn--sm" type="button" data-graph-fit>Fit view</button>
    </div>
    <div class="legend">
      <span><i style="background:var(--c-conv)"></i>convolution</span>
      <span><i style="background:var(--c-norm)"></i>normalisation</span>
      <span><i style="background:var(--c-act)"></i>activation</span>
      <span><i style="background:var(--c-pool)"></i>pool / reshape</span>
      <span><i style="background:var(--c-linear)"></i>linear</span>
    </div>
  </div>
  <div class="lab__canvas" data-graph-stage>
    <div class="lab__empty">Select a model to render its graph.</div>
  </div>
  <aside class="lab__inspect" data-graph-inspect>
    <p class="panel__title">Node inspector</p>
    <p class="muted">Click any node to see its type, input and output shapes, and parameter count.</p>
  </aside>
</section>

<section class="netron">
  <div>
    <h2>Open in Netron</h2>
    <p>Netron renders the same files as an interactive graph with weights, attributes and per-node tensor metadata. The links below open a model directly in Netron; the files in <code>models/</code> can be dragged onto <code>netron.app</code> for offline use.</p>
    <ul class="linklist">{netron_rows}</ul>
    <p class="muted">Tip: in Netron press <kbd>H</kbd> for the horizontal layout, click a node to see attributes, and use the sidebar to jump between layers. Export a model with <code>torch.onnx.export(model, dummy, "m.onnx", opset_version=17)</code>.</p>
  </div>
  <div class="netron__frame">
    <iframe title="Netron model viewer" data-netron src="https://netron.app/" loading="lazy"></iframe>
    <p class="netron__hint" data-netron-note>Netron loads a model when you drop it here — or use the links on the left. Netron can only fetch a model by URL when this page is served over HTTPS.</p>
  </div>
</section>

<section class="compare">
  <h2>Reading a graph like an engineer</h2>
  <div class="compare__grid">
    <div><h3>Shapes are the contract</h3><p>Every edge carries a tensor with a rank, dtype and layout (NCHW for PyTorch, NHWC for TensorFlow/TFLite). A shape mismatch is the most common export failure, and a graph view localises it instantly.</p></div>
    <div><h3>Repeats are abstraction</h3><p>A ResNet-18 is four stages of two residual blocks. Collapse repeats and the 70-node graph becomes a nine-step story: stem → four stages → pool → classifier.</p></div>
    <div><h3>Cost is not uniform</h3><p>Early layers are huge in pixels and tiny in channels; late layers are the reverse. Most FLOPs sit in the middle, most memory traffic in the stem. Inspect before you optimise.</p></div>
  </div>
</section>
</div>"""
    return layout(cfg=cfg, depth=0, title=f"Model lab — {cfg['title']}",
                  description="Inspect real ONNX computer-vision architectures with an interactive graph explorer and Netron.",
                  body=body, body_class="page-models", nav_active="models")


def build_resources_page(cfg: dict) -> str:
    path = ROOT / "RESOURCES.md"
    ctx = {"headings": []}
    content = render_markdown(path.read_text(encoding="utf-8"), ctx) if path.exists() else "<p>No resources yet.</p>"
    body = f"""<div class="wrap">
<header class="pagehead"><p class="eyebrow">Library</p><h1>Resources &amp; references</h1>
<p class="lede">The primary texts, courses, datasets and tools this curriculum is built on — curated, not scraped.</p></header>
<div class="prose">{content}</div>
</div>"""
    return layout(cfg=cfg, depth=0, title=f"Resources — {cfg['title']}",
                  description="Curated computer vision books, courses, papers, datasets and tooling.",
                  body=body, body_class="page-resources", nav_active="resources")


def build_search_index(courses: list[dict], lessons: dict) -> list[dict]:
    entries = []
    for c in courses:
        for l in lessons[c["slug"]]:
            text = re.sub(r":::[^\n]*|::option\[[^\]]*\]\{[^}]*\}|[#*`>|-]", " ", l["body"])
            text = re.sub(r"\s+", " ", text).strip()
            entries.append({
                "title": l["title"],
                "course": c["en"]["title"],
                "url": f"lessons/{c['slug']}/{l['slug']}.html",
                "snippet": l.get("description", ""),
                "text": text[:1600],
            })
    return entries


def main() -> int:
    cfg = load_site_config()
    courses = load_courses()
    lessons = load_lessons(courses)
    catalog = json.loads((ROOT / "models" / "catalog.json").read_text(encoding="utf-8"))

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "lessons").mkdir()
    (SITE / "courses").mkdir()
    (SITE / "levels").mkdir()

    for sub in ("css", "js"):
        shutil.copytree(ROOT / "assets" / sub, SITE / "assets" / sub)
    (SITE / "assets" / "img").mkdir()
    (SITE / "assets" / "img" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="8" fill="#0b1220"/>'
        '<path d="M4 16s4.6-7 12-7 12 7 12 7-4.6 7-12 7S4 16 4 16z" fill="none" stroke="#22d3ee" stroke-width="1.8"/>'
        '<circle cx="16" cy="16" r="4" fill="none" stroke="#22d3ee" stroke-width="1.8"/>'
        '<circle cx="16" cy="16" r="1.6" fill="#22d3ee"/></svg>',
        encoding="utf-8",
    )
    shutil.copytree(ROOT / "models" / "graphs", SITE / "models" / "graphs")
    for onnx in (ROOT / "models").glob("*.onnx"):
        (SITE / "models").mkdir(exist_ok=True)
        shutil.copy2(onnx, SITE / "models" / onnx.name)
    shutil.copy2(ROOT / "models" / "catalog.json", SITE / "models" / "catalog.json")
    for art in (ROOT / "images" / "courses").glob("*.svg"):
        shutil.copy2(art, SITE / "assets" / "img" / art.name)

    (SITE / "index.html").write_text(build_home(cfg, courses, lessons), encoding="utf-8")
    (SITE / "path.html").write_text(build_path_page(cfg, courses, lessons), encoding="utf-8")
    for level in cfg["levels"]:
        (SITE / "levels" / f"{level['id']}.html").write_text(
            build_level(cfg, courses, lessons, level), encoding="utf-8")
    for c in courses:
        (SITE / "courses" / f"{c['slug']}.html").write_text(
            build_course(cfg, courses, lessons, c), encoding="utf-8")
        (SITE / "lessons" / c["slug"]).mkdir(exist_ok=True)
        for l in lessons[c["slug"]]:
            (SITE / "lessons" / c["slug"] / f"{l['slug']}.html").write_text(
                build_lesson(cfg, courses, lessons, c, l), encoding="utf-8")

    (SITE / "models.html").write_text(build_models_page(cfg, catalog), encoding="utf-8")
    (SITE / "resources.html").write_text(build_resources_page(cfg), encoding="utf-8")
    (SITE / "search-index.json").write_text(
        json.dumps(build_search_index(courses, lessons), ensure_ascii=False), encoding="utf-8")

    total = sum(len(v) for v in lessons.values())
    print(f"Built {total} lessons in {len(courses)} courses → {SITE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
