"""The Vision Journey content engine.

The engine turns rendered lesson content into presentable pages. It knows
nothing about computer vision: lesson text lives in `lessons/`, the engine
lives here, and `tools/build.py` wires the two together into `site/`.

Modules:
    blocks      — split rendered lesson HTML into top-level blocks
    tutorial    — present a tutorial/lesson page one step at a time
"""

from .tutorial import Tutorial, present_tutorial

__all__ = ["Tutorial", "present_tutorial"]
