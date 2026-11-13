"""Split rendered lesson HTML into top-level blocks.

The lesson renderer emits well-formed block markup, so a block is a single
top-level element. Keeping the split here means the tutorial presenter can
reason in blocks (paragraph, heading, list, figure, quiz …) without re-parsing
the whole document.
"""

from __future__ import annotations

import re

# Block-level elements the lesson renderer can emit at the top level.
BLOCK_TAGS = ("p", "h1", "h2", "h3", "h4", "ul", "ol", "pre", "div", "figure", "aside", "table", "blockquote")

_START = re.compile(r"<(" + "|".join(BLOCK_TAGS) + r")\b", re.I)


def _close_index(markup: str, start: int, tag: str) -> int:
    """Return the index just past the element's matching close tag."""
    open_re = re.compile(rf"<{tag}\b", re.I)
    close_re = re.compile(rf"</{tag}\s*>", re.I)
    depth = 0
    pos = start
    while True:
        opened = open_re.search(markup, pos)
        closed = close_re.search(markup, pos)
        if not closed:
            return len(markup)
        if opened and opened.start() < closed.start():
            depth += 1
            pos = opened.end()
        else:
            depth -= 1
            pos = closed.end()
            if depth == 0:
                return pos


def split_blocks(markup: str) -> list[str]:
    """Return the top-level blocks of a rendered lesson, in document order."""
    blocks: list[str] = []
    pos = 0
    while True:
        match = _START.search(markup, pos)
        if not match:
            tail = markup[pos:].strip()
            if tail:
                blocks.append(tail)
            return blocks
        lead = markup[pos:match.start()].strip()
        if lead:
            blocks.append(lead)
        end = _close_index(markup, match.start(), match.group(1).lower())
        blocks.append(markup[match.start():end].strip())
        pos = end


def starts_with(block: str, *tags: str) -> bool:
    """True when a block opens with one of the given tag names."""
    head = block.lstrip()[:12].lower()
    return any(head.startswith(f"<{tag}") and not head[len(tag) + 1:len(tag) + 2].isalnum() for tag in tags)
