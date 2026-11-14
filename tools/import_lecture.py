#!/usr/bin/env python3
"""
One command per lecture: PDF → slides → lessons → captions → notes skeleton.

Everything below the writing is mechanical, and this runs all of it:

    1. find the lecture PDF and the matching recording
    2. import the deck (tools/import_slides.py): sections, slides, WebP images
    3. download the captions with yt-dlp (or accept a local .vtt)
    4. align the transcript to the slides (tools/align_transcript.py)
    5. add the missing entries to the notes file, with a verbatim quote drafted

What it cannot do is write the explanation. The notes file keeps any `gist`
already written and only fills the gaps, so re-running after new lectures, a
better caption file or a re-import never damages the prose:

    python3 tools/import_lecture.py --lecture 1              # import + draft notes
    python3 tools/import_lecture.py --lecture 2 --plan       # report, write nothing

The lecture's sources are declared in the topic's site.yml:

    source:
      pdf: "fall25-cme295-lecture{n}.pdf"
      dir: "/path/with/the/pdfs"        # optional, --src overrides
      playlist: "https://www.youtube.com/playlist?list=..."

Requires poppler (pdftohtml, pdftoppm), Pillow, and yt-dlp for captions.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from align_transcript import Sentence, align, clock, load_slides, parse_vtt  # noqa: E402

FILLERS = ("okay", "ok", "yeah", "and", "so", "cool", "great", "all right", "right")


def read_source(topic: Path) -> dict:
    site = yaml.safe_load((topic / "site.yml").read_text(encoding="utf-8")) or {}
    return site.get("source", {}) or {}


def find_pdf(source: dict, lecture: int, override: str | None) -> Path | None:
    pattern = source.get("pdf", "*lecture{n}.pdf").replace("{n}", str(lecture))
    folder = Path(override or os.environ.get("SLIDES_DIR") or source.get("dir", "")).expanduser()
    if not folder.is_dir():
        return None
    matches = sorted(folder.glob(pattern)) or sorted(folder.glob(f"*lecture{lecture}.pdf"))
    return matches[0] if matches else None


def find_video(source: dict, lecture: int, ytdlp: str) -> str | None:
    """The recording for a lecture: nth match in the playlist, by title."""
    playlist = source.get("playlist")
    if not playlist:
        return None
    result = subprocess.run(
        [ytdlp, "--flat-playlist", "--print", "%(id)s\t%(title)s", playlist],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  yt-dlp could not list the playlist: {result.stderr.strip()[:120]}")
        return None
    rows = [line.split("\t", 1) for line in result.stdout.splitlines() if "\t" in line]
    for video_id, title in rows:
        if re.search(rf"lecture\s*{lecture}\b", title, re.I):
            return f"https://www.youtube.com/watch?v={video_id}"
    return None


def fetch_captions(url: str, outdir: Path, ytdlp: str) -> Path | None:
    outdir.mkdir(parents=True, exist_ok=True)
    before = set(outdir.glob("*.vtt"))
    subprocess.run(
        [ytdlp, "--skip-download", "--write-auto-subs", "--write-subs",
         "--sub-langs", "en.*", "--sub-format", "vtt", "-o", str(outdir / "%(id)s.%(ext)s"), url],
        capture_output=True, text=True,
    )
    added = sorted(set(outdir.glob("*.vtt")) - before, key=lambda p: p.stat().st_size, reverse=True)
    return added[0] if added else next(iter(sorted(outdir.glob("*.vtt"), key=lambda p: p.stat().st_size, reverse=True)), None)


def weight_sentences(sentences: list[Sentence]) -> dict[str, float]:
    frequency: dict[str, int] = {}
    for sentence in sentences:
        for word in sentence.words:
            frequency[word] = frequency.get(word, 0) + 1
    total = max(len(sentences), 1)
    return {w: math.log(1 + total / (1 + n)) for w, n in frequency.items()}


def pick_quote(slide: dict, weight: dict[str, float]) -> str:
    """The clearest verbatim line in the slide's stretch of speech."""
    best, best_score = "", 0.0
    for sentence in slide.get("span", []):
        words = sentence.text.split()
        if not 10 <= len(words) <= 32:
            continue
        if sentence.text.lower().startswith(FILLERS) or "?" in sentence.text:
            continue
        if not sentence.text.rstrip().endswith((".", "!")):
            continue
        score = sum(weight.get(w, 0.0) for w in sentence.words & slide["words"])
        score /= len(words) ** 0.5
        if score > best_score:
            best, best_score = sentence.text.strip(), score
    return best


def draft_notes(path: Path, slides: list[dict], sentences: list[Sentence]) -> tuple[int, int]:
    """Append an entry for every slide that has none; never rewrite prose.

    The notes file is the one thing in the pipeline a person writes, so it is
    edited by addition only: existing text keeps its wording and its formatting,
    and a re-run after a re-import, a new lecture or better captions cannot
    damage it. Returns (slides still needing prose, quotes drafted).
    """
    text = path.read_text(encoding="utf-8") if path.exists() else (
        "# Per-slide notes, keyed by PDF page number. `gist` is the explanation,\n"
        "# written by hand; `said` quotes the lecturer. Blank gists are the queue.\n")
    existing = yaml.safe_load(text) or {}

    weight = weight_sentences(sentences)
    blocks: list[str] = []
    drafted = 0
    for slide in slides:
        if slide["page"] in existing:
            continue
        block = f"\n{slide['page']}:\n  gist: \"\"\n"
        quote = pick_quote(slide, weight)
        if quote:
            body = textwrap.fill(quote, width=76, initial_indent="    ",
                                 subsequent_indent="    ")
            block += f"  said: >-\n{body}\n"
            drafted += 1
        blocks.append(block)

    if blocks:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip("\n") + "\n" + "".join(blocks), encoding="utf-8")

    merged = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    missing = sum(1 for entry in merged.values() if not (entry or {}).get("gist"))
    return missing, drafted


def _format_notes(notes: dict) -> str:
    """Stable, readable YAML: one block per slide, folded prose under a key."""
    blocks = ["# Per-slide notes, keyed by PDF page number. `gist` is the explanation,\n"
              "# written by hand; `said` quotes the lecturer.\n"]
    for page in sorted(notes):
        entry = notes[page] or {}
        block = [f"{page}:"]
        gist = " ".join(str(entry.get("gist", "")).split())
        if gist:
            block.append("  gist: >-\n" + textwrap.fill(gist, 76, initial_indent="    ",
                                                          subsequent_indent="    "))
        else:
            block.append('  gist: ""')
        said = " ".join(str(entry.get("said", "")).split())
        if said:
            block.append("  said: >-\n" + textwrap.fill(said, 76, initial_indent="    ",
                                                          subsequent_indent="    "))
        blocks.append("\n".join(block) + "\n")
    return "\n".join(blocks)


def apply_gists(notes_path: Path, gists_path: Path) -> int:
    """Merge written explanations (page → prose) into a notes file."""
    notes = yaml.safe_load(notes_path.read_text(encoding="utf-8")) or {}
    gists = yaml.safe_load(gists_path.read_text(encoding="utf-8")) or {}
    written = 0
    for page, text in gists.items():
        entry = notes.setdefault(int(page), {}) or {}
        text = " ".join(str(text).split())
        if text and entry.get("gist") != text:
            entry["gist"] = text
            written += 1
        notes[int(page)] = entry
    notes_path.write_text(_format_notes(notes), encoding="utf-8")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a lecture: slides, captions and notes.")
    parser.add_argument("--lecture", type=int, action="append", required=True)
    parser.add_argument("--topic", default="cme295")
    parser.add_argument("--src", help="folder with the lecture PDFs (overrides site.yml)")
    parser.add_argument("--vtt", help="use this caption file instead of downloading one")
    parser.add_argument("--yt-dlp", default=shutil.which("yt-dlp") or "yt-dlp")
    parser.add_argument("--captions-dir", default=str(ROOT / ".cache" / "captions"))
    parser.add_argument("--course", help="course id; defaults to lecture-NN")
    parser.add_argument("--plan", action="store_true", help="report what would happen, write nothing")
    parser.add_argument("--skip-import", action="store_true", help="only refresh captions and notes")
    args = parser.parse_args()

    topic = ROOT / "content" / args.topic
    source = read_source(topic)
    status = 0

    for lecture in args.lecture:
        course = args.course or f"lecture-{lecture:02d}"
        pdf = None if args.skip_import else find_pdf(source, lecture, args.src)
        print(f"lecture {lecture} → course {course}")
        if not args.skip_import:
            print(f"  pdf:      {pdf or 'NOT FOUND'}")
            if not pdf:
                status = 1
                continue
        if args.plan:
            print("  plan only: stopping before import")
            continue

        if not args.skip_import:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "import_slides.py"),
                 "--src", str(pdf.parent), "--lecture", str(lecture),
                 "--topic", args.topic, "--course", course],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  import failed:\n{result.stderr[-400:]}")
                status = 1
                continue
            for line in result.stdout.splitlines():
                if line.startswith("  "):
                    print(f"  {line.strip()}")

        slides = load_slides(topic, course)
        if not slides:
            print("  no slides found after import")
            status = 1
            continue

        vtt = Path(args.vtt).expanduser() if args.vtt else None
        if vtt is None:
            url = find_video(source, lecture, args.yt_dlp)
            print(f"  video:    {url or 'not found'}")
            if not url:
                print("  no recording, so no transcript: notes must be written from the slides")
                continue
            vtt = fetch_captions(url, Path(args.captions_dir), args.yt_dlp)
            print(f"  captions: {vtt or 'download failed'}")
        if not vtt or not vtt.exists():
            print("  no captions available")
            continue

        sentences = parse_vtt(vtt)
        align(slides, sentences)
        print(f"  aligned:  {len(sentences)} sentences, last at {clock(sentences[-1].start)}")

        notes_path = topic / "notes" / f"{course}.yml"
        missing, drafted = draft_notes(notes_path, slides, sentences)
        print(f"  notes:    {len(slides)} slides, {drafted} quotes drafted, "
              f"{missing} explanations still to write")
        if missing:
            pending = [s for s in slides if not (yaml.safe_load(notes_path.read_text())
                                                 .get(s["page"], {}) or {}).get("gist")]
            for slide in pending[:6]:
                print(f"            p{slide['page']:>3} {slide['title'][:60]}")
            if len(pending) > 6:
                print(f"            … and {len(pending) - 6} more in {notes_path}")

    return status


if __name__ == "__main__":
    sys.exit(main())
