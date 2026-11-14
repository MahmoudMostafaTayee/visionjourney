"""Present a tutorial page one step at a time.

A tutorial is a sequence of steps. Each step is a paragraph — or a heading
together with the material it introduces — plus whatever belongs to it: a list,
a code block, a figure, or a check. The reader shows one step at a time and
offers a centred Continue; a step that ends in a check holds Continue until the
check is answered (app.js enforces that, the markup carries the hooks).

The engine renders markup only. It has no idea what the lesson is about, and it
does not decide where "next lesson" goes; the caller passes that in.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

from .blocks import split_blocks, starts_with

HEADING_TAGS = ("h1", "h2", "h3", "h4")
_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class Tutorial:
    """A tutorial page: its steps, the control bar under them, and the count."""

    steps_html: str
    controls_html: str
    count: int


def _text(markup: str) -> str:
    """Plain text of a heading, for the control bar's section label."""
    return _SPACE.sub(" ", html.unescape(_TAG.sub("", markup))).strip()


def _steps(blocks: list[str]) -> list[tuple[list[str], str]]:
    """Group blocks into steps: one paragraph each, headings riding along."""
    steps: list[tuple[list[str], str]] = []
    pending: list[str] = []
    body: list[str] = []
    section = ""

    def flush() -> None:
        nonlocal pending, body
        if not body and not pending:
            return
        group = pending + body
        title = next((_text(b) for b in group if starts_with(b, *HEADING_TAGS)), "")
        # A slide can name itself without a heading, so the control bar still
        # says what you are looking at.
        if not title:
            label = re.search(r'data-step-label="([^"]*)"', group[0])
            title = html.unescape(label.group(1)) if label else ""
        steps.append((group, title or section))
        pending, body = [], []

    for block in blocks:
        if starts_with(block, *HEADING_TAGS):
            if body:
                flush()
            pending.append(block)
            section = _text(block)
        elif starts_with(block, "p"):
            if body:
                flush()
            body.append(block)
        elif starts_with(block, "figure") and any(starts_with(b, "figure") for b in body):
            # One figure per step: a slide follows a slide, not the text of the
            # slide before it. A figure after a paragraph still belongs to it.
            flush()
            body.append(block)
        else:
            # Lists, code, figures, callouts and checks belong to the paragraph
            # they follow, so a step never strands a heading or a list alone.
            body.append(block)
    flush()
    return steps


def present_tutorial(
    content: str,
    *,
    finish_href: str,
    finish_label: str,
    min_steps: int = 2,
) -> Tutorial:
    """Render lesson HTML as a stepped tutorial with a centred Continue."""
    steps = _steps(split_blocks(content))
    if len(steps) < min_steps:
        # Too short to walk through: show the page as it is, with no controls.
        return Tutorial(steps_html=content, controls_html="", count=len(steps))

    steps_html = "".join(
        f'<section class="step" data-step="{n}" '
        f'data-step-title="{html.escape(title, quote=True)}">{"".join(blocks)}</section>'
        for n, (blocks, title) in enumerate(steps, start=1)
    )

    controls_html = f"""<div class="stepctl" data-stepctl hidden>
  <div class="stepctl__track">
    <span class="stepctl__count">Step <b data-step-pos>1</b> of <b data-step-total>{len(steps)}</b></span>
    <span class="stepctl__meter"><i data-step-meter></i></span>
    <span class="stepctl__name" data-step-name aria-live="polite"></span>
  </div>
  <div class="stepctl__actions">
    <button class="btn btn--ghost btn--sm" type="button" data-step-prev>Back</button>
    <button class="btn btn--primary" type="button" data-step-next>Continue</button>
    <a class="btn btn--primary" data-step-finish href="{html.escape(finish_href, quote=True)}" hidden>{html.escape(finish_label)} →</a>
  </div>
  <p class="stepctl__gate" data-step-gate hidden>Answer the question above to continue.</p>
</div>"""

    return Tutorial(steps_html=steps_html, controls_html=controls_html, count=len(steps))
