#!/usr/bin/env python3
"""
Align a lecture transcript to the slides of an imported course.

The deck has no timestamps and the captions have no slide numbers, so the two
have to be matched by what they talk about. Both are in teaching order, which is
the strong constraint: the alignment is monotonic, and each slide claims the
stretch of speech between its neighbours.

    sentences ────────────────────────────────────────────────────────► time
    slides    [cover][tasks][tokenization][vectors][rnn]…

Each slide gets an anchor — the sentence window that best matches its own words,
weighted by how distinctive those words are across the lecture — then adjacent
slides split the transcript at the midpoint between their anchors. A slide with
no distinct words inherits its neighbour's speech rather than pulling unrelated
material towards it.

Usage:
    python3 tools/align_transcript.py --vtt lecture1.en.vtt --course lecture-01
    python3 tools/align_transcript.py --vtt lecture1.en.vtt --course lecture-01 --report

Prints what it aligned and, with --write, saves a draft
content/<topic>/notes/<course>.auto.yml for review. The draft is a working aid:
the published notes are handwritten from it, because a transcript explains the
slide rather than summarising it.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STOP = {
    "a", "about", "after", "again", "all", "also", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "but", "by", "can", "could", "did", "do",
    "does", "doing", "don", "down", "each", "few", "for", "from", "further", "get", "go",
    "going", "got", "had", "has", "have", "having", "he", "her", "here", "hers", "him",
    "his", "how", "i", "if", "in", "into", "is", "it", "its", "just", "let", "like",
    "make", "me", "more", "most", "my", "no", "not", "now", "of", "off", "on", "once",
    "one", "only", "or", "other", "our", "out", "over", "own", "really", "right", "said",
    "same", "say", "see", "she", "should", "so", "some", "such", "take", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "thing", "this", "those",
    "through", "to", "too", "two", "up", "us", "use", "very", "want", "was", "we", "well",
    "were", "what", "when", "where", "which", "while", "who", "why", "will", "with",
    "would", "you", "your", "s", "t",
}


@dataclass
class Sentence:
    start: float
    text: str
    words: set[str]


def clock(seconds: float) -> str:
    return f"{int(seconds // 60)}:{int(seconds % 60):02d}"


def parse_vtt(path: Path) -> list[Sentence]:
    """Cue text, joined into sentences at the punctuation the captions carry."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    cues: list[tuple[float, str]] = []
    for block in re.split(r"\n\s*\n", raw):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines or "-->" not in " ".join(lines[:2]):
            continue
        stamp = next(line for line in lines if "-->" in line)
        text = " ".join(line for line in lines if "-->" not in line and not line.isdigit())
        if not text:
            continue
        start = _seconds(stamp.split("-->")[0])
        cues.append((start, text))

    sentences: list[Sentence] = []
    buffer, started = "", 0.0
    for start, text in cues:
        if text == buffer.split(" ")[-1]:
            continue
        if not buffer:
            started = start
        buffer = f"{buffer} {text}".strip()
        if re.search(r"[.?!]\s*$", text) or len(buffer.split()) > 42:
            sentences.append(Sentence(started, buffer, words_of(buffer)))
            buffer = ""
    if buffer:
        sentences.append(Sentence(started, buffer, words_of(buffer)))
    return sentences


def _seconds(stamp: str) -> float:
    parts = stamp.strip().split(":")
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part.replace(",", "."))
    return seconds


def words_of(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", text.lower()) if w not in STOP and len(w) > 2}


def load_slides(topic: Path, course: str) -> list[dict]:
    """Slides in reading order, with the words printed on them."""
    slides = []
    folder = topic / "lessons" / "en" / course
    for path in sorted(folder.glob("*.md")):
        order = int(re.search(r"order_index:\s*(\d+)", path.read_text()).group(1))
        for block in re.split(r"\n(?=:::slide)", path.read_text()):
            match = re.match(r':::slide\{[^}]*n="(\d+)"\}\s*(.*)', block)
            if not match:
                continue
            title = match.group(2).split("\n")[0].strip()
            body = "\n".join(line.lstrip("- ").strip() for line in block.splitlines()[1:]
                             if line.startswith("- "))
            slides.append({"order": order, "page": int(match.group(1)), "title": title,
                           "words": words_of(f"{title} {body}") | words_of(title)})
    slides.sort(key=lambda s: (s["order"], s["page"]))
    return slides


def align(slides: list[dict], sentences: list[Sentence], cost: float = 0.30) -> None:
    """Partition the transcript among the slides, monotonically and globally.

    Greedy anchoring drifts: a slide that scores best late in the lecture drags
    the cursor with it and everything after piles up at the end. So the split is
    solved as one partition — every sentence belongs to exactly one slide, slides
    keep their order, and the total match is maximised:

        best[i][j] = max over k < j of best[i-1][k] + match(i, k..j) - cost*(j-k)
    """
    frequency: dict[str, int] = {}
    for sentence in sentences:
        for word in sentence.words:
            frequency[word] = frequency.get(word, 0) + 1
    total = max(len(sentences), 1)
    weight = {w: math.log(1 + total / (1 + n)) for w, n in frequency.items()}

    count = len(sentences)
    # emissions[i][j]: how much sentence j talks about slide i.
    emissions = []
    for slide in slides:
        title = slide["title"].lower()
        row = []
        for sentence in sentences:
            value = sum(weight.get(w, 0.0) for w in slide["words"] & sentence.words)
            if title and len(title) > 6 and title in sentence.text.lower():
                value += 3.0
            row.append(value)
        emissions.append(row)

    def prefix(row: list[float]) -> list[float]:
        out = [0.0]
        for value in row:
            out.append(out[-1] + value)
        return out

    sums = [prefix(row) for row in emissions]
    n, m = len(slides), count
    # Every slide needs at least one sentence; dropping the last slides is worse
    # than giving them a few weakly-matching sentences.
    negative = -1e18
    previous = [negative] * (m + 1)
    for j in range(1, m + 1):
        previous[j] = sums[0][j] - cost * j
    back: list[list[int]] = [[0] * (m + 1) for _ in range(n)]

    for i in range(1, n):
        current = [negative] * (m + 1)
        row = sums[i]
        for j in range(i + 1, m + 1):
            best, best_k = negative, i
            for k in range(i, j):
                if previous[k] == negative:
                    continue
                value = previous[k] + row[j] - row[k] - cost * (j - k)
                if value > best:
                    best, best_k = value, k
            current[j] = best
            back[i][j] = best_k
        previous = current

    # Walk the split back: the boundaries are where each slide starts.
    bounds = [m]
    j = m
    for i in range(n - 1, 0, -1):
        j = back[i][j]
        bounds.append(j)
    bounds.reverse()
    bounds = [0] + bounds

    for i, slide in enumerate(slides):
        start, end = bounds[i], bounds[i + 1]
        slide["start"] = sentences[start].start if start < count else 0.0
        slide["span"] = sentences[start:end]
        slide["text"] = " ".join(s.text for s in slide["span"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Align a lecture transcript to imported slides.")
    parser.add_argument("--vtt", required=True, help="caption file, .vtt")
    parser.add_argument("--course", required=True, help="course id, e.g. lecture-01")
    parser.add_argument("--topic", default="cme295")
    parser.add_argument("--report", action="store_true", help="print the aligned text")
    parser.add_argument("--write", action="store_true", help="save notes/<course>.auto.yml")
    args = parser.parse_args()

    vtt = Path(args.vtt).expanduser()
    topic = ROOT / "content" / args.topic
    slides = load_slides(topic, args.course)
    if not slides:
        print("No slides found for that course.", file=sys.stderr)
        return 1
    sentences = parse_vtt(vtt)
    if not sentences:
        print("No captions parsed.", file=sys.stderr)
        return 1
    align(slides, sentences)

    print(f"{len(slides)} slides, {len(sentences)} caption sentences, "
          f"last sentence at {clock(sentences[-1].start)}")
    for slide in slides:
        print(f"  p{slide['page']:>3} {clock(slide['start']):>6}  {slide['title'][:44]:<44} "
              f"{len(slide['text'].split()):>4}w")
        if args.report:
            print(f"        {slide['text'][:400]}")

    if args.write:
        out = topic / "notes" / f"{args.course}.auto.yml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump({
            s["page"]: {"title": s["title"], "at": clock(s["start"]), "transcript": s["text"]}
            for s in slides
        }, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
