#!/usr/bin/env python3
"""
Import a lecture deck (PDF) as a course: one lesson per deck section, one step
per slide.

The decks are Beamer files, which means three things have to be handled before a
PDF page can become a page of this site:

    overlay builds    one idea spread over several PDF pages, each adding a
                      line to the same slide. Only the most complete page is a
                      slide; the others are animation states.
    running headers   the section name repeats at the top of every page, so the
                      first line of text is not the slide's title.
    contents pages    the deck's table of contents is reprinted before each
                      section, with the current section highlighted and therefore
                      missing from the page's text. These pages are section
                      boundaries, not slides.

Titles come from the page's largest type in its top band, body text from
everything below it, and overlay builds are detected as a page whose lines are a
subset of the next page's lines with the same title.

Usage:
    python3 tools/import_slides.py --src /path/to/decks --lecture 1
    python3 tools/import_slides.py --src /path/to/decks --lecture 1 --report

Writes content/<topic>/slides/<course>/slide-NNN.webp and
content/<topic>/lessons/en/<course>/*.md. Content is regenerated, so edits made
to the generated lessons by hand are lost on the next run — change the importer
instead.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ROW_TOLERANCE = 8  # pt: runs closer than this vertically are one line


# --------------------------------------------------------------------------------------
# PDF text model
# --------------------------------------------------------------------------------------

@dataclass
class Run:
    top: float
    left: float
    size: float
    text: str


@dataclass
class Page:
    number: int
    width: float
    height: float
    rows: list[list[Run]] = field(default_factory=list)

    @property
    def title(self) -> str:
        return " ".join(r.text for r in self.rows[0]).strip() if self.rows else ""

    @property
    def lines(self) -> list[str]:
        """Every line below the title, left to right."""
        return [clean(" ".join(r.text for r in row)) for row in self.rows[1:]]

    @property
    def all_text(self) -> str:
        return " ".join(clean(" ".join(r.text for r in row)) for row in self.rows)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_pdf(pdf: Path) -> list[Page]:
    """Read every page's positioned text runs with pdftohtml's XML mode."""
    xml = subprocess.run(
        ["pdftohtml", "-xml", "-i", "-stdout", str(pdf)],
        capture_output=True, text=True, check=True,
    ).stdout
    root = ET.fromstring(xml)
    sizes = {spec.get("id"): float(spec.get("size", 0)) for spec in root.iter("fontspec")}

    pages: list[Page] = []
    for element in root.findall("page"):
        page = Page(
            number=int(element.get("number")),
            width=float(element.get("width") or 0),
            height=float(element.get("height") or 0),
        )
        runs = []
        for node in element.findall("text"):
            text = clean("".join(node.itertext()))
            if not text:
                continue
            runs.append(Run(
                top=float(node.get("top") or 0),
                left=float(node.get("left") or 0),
                size=sizes.get(node.get("font"), 0.0),
                text=text,
            ))
        page.rows = _rows(runs)
        pages.append(page)
    return pages


def _rows(runs: list[Run]) -> list[list[Run]]:
    """Group runs into visual lines, top to bottom, each ordered left to right."""
    rows: list[list[Run]] = []
    for run in sorted(runs, key=lambda r: (r.top, r.left)):
        if rows and run.top - rows[-1][0].top <= ROW_TOLERANCE:
            rows[-1].append(run)
        else:
            rows.append([run])
    for row in rows:
        row.sort(key=lambda r: r.left)
    return rows


def promote_title(page: Page) -> Page:
    """Move the title row to the front: the topmost line that carries words.

    Arrow diagrams put labels anywhere, including larger type than the title, so
    size is not a reliable signal. Position is: Beamer titles sit at the top of
    the frame. Rows that are only punctuation (`. . .` placeholders) are skipped.
    """
    if not page.rows:
        return page
    rows = sorted(page.rows, key=lambda row: row[0].top)
    best = next((i for i, row in enumerate(rows)
                 if re.search(r"[A-Za-z]", " ".join(r.text for r in row))), 0)
    if best:
        rows.insert(0, rows.pop(best))
    page.rows = rows
    return page


# --------------------------------------------------------------------------------------
# Deck structure
# --------------------------------------------------------------------------------------

@dataclass
class Section:
    name: str
    pages: list[Page]


def contents_pages(pages: list[Page]) -> tuple[list[int], list[str]]:
    """Find the reprinted table-of-contents pages and the section names.

    A contents page keeps all its text in the right half of the slide; the
    current section is drawn highlighted, so it vanishes from the extracted
    text. The missing entry names the section that is starting.
    """
    def items(page: Page) -> list[tuple[float, str]]:
        """Entries written in the right-hand column: the contents list."""
        right = [r for row in page.rows for r in row if r.left > page.width * 0.45]
        grouped: list[list[Run]] = []
        for run in sorted(right, key=lambda r: (r.top, r.left)):
            if grouped and run.top - grouped[-1][0].top <= ROW_TOLERANCE:
                grouped[-1].append(run)
            else:
                grouped.append([run])
        return [(row[0].top, clean(" ".join(r.text for r in row))) for row in grouped]

    def signature(page: Page) -> tuple[str, ...]:
        return tuple(sorted({t for _, t in items(page)}))

    candidates = [(p, signature(p)) for p in pages if 5 <= len(items(p)) <= 9]
    if len(candidates) < 3:
        return [], []

    # The contents page is the only right-hand list that is reprinted verbatim
    # before every section. Figure diagrams also fill the right column, but each
    # of those appears once, so the most repeated signature wins.
    counts: dict[tuple[str, ...], int] = {}
    for _, sig in candidates:
        counts[sig] = counts.get(sig, 0) + 1
    sig, repeated = max(counts.items(), key=lambda item: item[1])
    if repeated < 3:
        return [], []

    markers = sorted(p.number for p, s in candidates if s == sig)
    return markers, list(sig)


def cover_title(page: Page, lecture: int) -> str:
    """The cover's largest type, in reading order: the deck's subject."""
    if not page.rows:
        return f"Lecture {lecture}"
    biggest = max(r.size for row in page.rows for r in row)
    rows = [row for row in page.rows if max(r.size for r in row) >= biggest - 0.01]
    title = clean(" ".join(" ".join(r.text for r in row) for row in rows))
    return title or f"Lecture {lecture}"


def sections(pages: list[Page], deck_title: str) -> list[Section]:
    markers, names = contents_pages(pages)
    if not markers:
        return [Section(deck_title, pages)]

    by_number = {p.number: p for p in pages}
    out: list[Section] = []
    first = markers[0]
    intro = [p for p in pages if p.number < first]
    if intro:
        out.append(Section(deck_title, intro))

    for i, start in enumerate(markers):
        end = markers[i + 1] if i + 1 < len(markers) else pages[-1].number + 1
        body = [p for p in pages if start < p.number < end]
        if body:
            # The section is named after its first slide, which is more specific
            # than the chapter title reprinted on the divider.
            out.append(Section("", body))
    return out


STOPWORDS = {"a", "an", "and", "as", "at", "for", "in", "is", "of", "on", "the", "to", "with"}


def _tokens(page: Page) -> set[str]:
    return {t for t in re.findall(r"[\w']+", page.all_text.lower()) if t not in STOPWORDS}


def collapse_overlays(pages: list[Page]) -> list[Page]:
    """Keep only the most complete page of each animated build.

    A build is the same slide with more on it, so the comparison is on word sets
    rather than lines: reflowing a two-column slide changes its lines without
    changing its content.
    """
    kept: list[Page] = []
    for page in pages:
        if kept:
            previous = kept[-1]
            earlier, current = _tokens(previous), _tokens(page)
            if previous.title and previous.title == page.title and earlier <= current:
                kept[-1] = page
                continue
        kept.append(page)
    return kept


def slide_text(page: Page) -> list[str]:
    """Body lines as bullets, with the bullet glyphs the deck draws kept as markers."""
    out = []
    for line in page.lines:
        line = clean(line.lstrip("●○•").strip())
        if not line or len(line) < 2:
            continue
        out.append(line.replace(":::", ": : :"))
    return out


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------

def render(pdf: Path, page: int, dest: Path, dpi: int, quality: int) -> None:
    """Render one PDF page to WebP, quietly and at one resolution."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            ["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
             "-png", "-singlefile", str(pdf), str(prefix)],
            check=True, capture_output=True,
        )
        png = prefix.with_suffix(".png")
        try:
            from PIL import Image
        except ImportError:
            shutil.move(str(png), str(dest.with_suffix(".png")))
            return
        with Image.open(png) as image:
            image.load()
            image.convert("RGB").save(dest, "WEBP", quality=quality, method=6)


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

def slugify(text: str, limit: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (slug[:limit].rstrip("-")) or "slides"


def front_matter(meta: dict) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip() + "\n---\n\n"


def lesson_markdown(section: Section, lecture: int, course: str, slides: list[Page]) -> str:
    body = [f"## {section.name}\n"]
    for page in slides:
        title = page.title or section.name
        body.append(
            f':::slide{{src="../../slides/{course}/slide-{page.number:03d}.webp" n="{page.number}"}} '
            f"{title}\n"
        )
        lines = slide_text(page)
        if lines:
            body.extend(f"- {line}" for line in lines)
        body.append(":::\n")
    return "\n".join(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a lecture PDF as a course.")
    parser.add_argument("--src", required=True, help="folder holding the lecture PDFs")
    parser.add_argument("--lecture", type=int, action="append", required=True, help="lecture number (repeatable)")
    parser.add_argument("--topic", default="cme295", help="topic id under content/")
    parser.add_argument("--course", help="course id; defaults to lecture-NN")
    parser.add_argument("--course-title", help="course title; read from the deck if omitted")
    parser.add_argument("--level", default="foundations", help="category id in site.yml")
    parser.add_argument("--intro-title", default="Course overview",
                        help="lesson title for the slides before the first section")
    parser.add_argument("--dpi", type=int, default=120)
    parser.add_argument("--quality", type=int, default=82)
    parser.add_argument("--report", action="store_true", help="print the parse without writing")
    args = parser.parse_args()

    source = Path(args.src).expanduser()
    if not source.is_dir():
        print(f"No such folder: {source}", file=sys.stderr)
        return 1

    topic = ROOT / "content" / args.topic
    for lecture in args.lecture:
        matches = sorted(source.glob(f"*lecture{lecture}.pdf")) or sorted(source.glob(f"*{lecture}*.pdf"))
        if not matches:
            print(f"No PDF for lecture {lecture} in {source}", file=sys.stderr)
            return 1
        pdf = matches[0]
        course = args.course or f"lecture-{lecture:02d}"

        pages = [promote_title(p) for p in parse_pdf(pdf)]
        deck_title = cover_title(pages[0], lecture)
        sections_ = sections(pages, deck_title)
        print(f"lecture {lecture}: {len(pages)} pages → {len(sections_)} sections")

        for index, section in enumerate(sections_, start=1):
            slides = collapse_overlays(section.pages)
            if section.name == deck_title and index == 1:
                section.name = args.intro_title
            elif not section.name:
                section.name = next((p.title for p in slides if p.title), deck_title)
            print(f"  {index:02d} {section.name[:52]:<52} {len(section.pages):>3} pages → {len(slides):>3} slides")
            if args.report:
                for page in slides:
                    print(f"       p{page.number:>3}  {page.title[:70]}")
                continue

            lessons_dir = topic / "lessons" / "en" / course
            lessons_dir.mkdir(parents=True, exist_ok=True)
            slug = f"section-{index:02d}-{slugify(section.name)}"
            numbers = [p.number for p in slides]
            meta = {
                "lesson_id": slug,
                "course_id": course,
                "lang": "en",
                "order_index": index,
                "title": section.name,
                "description": (f"Slides {numbers[0]}–{numbers[-1]} of lecture {lecture}: "
                                f"{len(slides)} slides from the original deck."),
                "meta_title": f"{section.name} — Lecture {lecture}",
                "meta_description": f"Slide-by-slide walkthrough of {section.name}, lecture {lecture}.",
                "meta_keywords": f"{section.name}, lecture {lecture}, slides",
            }
            (lessons_dir / f"{slug}.md").write_text(
                front_matter(meta) + lesson_markdown(section, lecture, course, slides), encoding="utf-8")

            for page in slides:
                render(pdf, page.number, topic / "slides" / course / f"slide-{page.number:03d}.webp",
                       args.dpi, args.quality)

        if args.report:
            continue
        course_file = topic / "courses" / f"{course}.yml"
        if not course_file.exists():
            course_file.parent.mkdir(parents=True, exist_ok=True)
            title = args.course_title or deck_title
            course_file.write_text(yaml.safe_dump({
                "id": course,
                "category": {"id": args.level},
                "order_index": lecture - 1,
                "translations": {"en": {
                    "title": title,
                    "description": f"Slide-by-slide companion to lecture {lecture} of Stanford CME 295.",
                    "meta_title": f"{title} — CME 295",
                    "meta_description": f"Every slide of lecture {lecture}, illustrated and parsed.",
                    "meta_keywords": f"transformers, large language models, lecture {lecture}",
                }},
            }, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
