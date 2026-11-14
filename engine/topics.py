"""Load topics from content/.

A topic is a self-contained curriculum: a folder under content/ with its own
site.yml, courses and lessons. The engine only knows that shape — it never knows
what a topic is about. Adding a subject means adding a folder and listing its id
in topics.yml; no code changes.

    content/<id>/site.yml
    content/<id>/courses/*.yml
    content/<id>/lessons/<lang>/<course>/*.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

LANG = "en"


@dataclass(frozen=True)
class Topic:
    """One curriculum, ready to build."""

    id: str
    root: Path
    config: dict
    courses: list[dict]
    lessons: dict[str, list[dict]]

    @property
    def base(self) -> str:
        """URL prefix of the topic's subtree in the built site."""
        return f"{self.id}/"

    @property
    def title(self) -> str:
        return self.config.get("title", self.id)

    def has_models(self) -> bool:
        return (self.root / "models" / "catalog.json").exists()

    def has_resources(self) -> bool:
        return (self.root / "RESOURCES.md").exists()


def split_front_matter(text: str) -> tuple[dict, str]:
    """Split a lesson's YAML front matter from its markdown body."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    meta = yaml.safe_load(text[3:end]) or {}
    return meta, text[end + 4:].lstrip("\n")


def _load_config(path: Path) -> dict:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cfg.setdefault("nav", [])
    cfg.setdefault("levels", [])
    return cfg


def _load_courses(root: Path) -> list[dict]:
    courses = []
    for path in sorted((root / "courses").glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data["slug"] = path.stem
        data["en"] = (data.get("translations") or {}).get(LANG, {})
        courses.append(data)
    courses.sort(key=lambda c: (c.get("order_index", 99), c["slug"]))
    return courses


def _load_lessons(root: Path, courses: list[dict]) -> dict[str, list[dict]]:
    by_course: dict[str, list[dict]] = {c["slug"]: [] for c in courses}
    for path in sorted((root / "lessons" / LANG).glob("*/*.md")):
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        meta["slug"] = path.stem
        meta["course"] = path.parent.name
        meta["body"] = body
        meta["words"] = len(body.split())
        meta["minutes"] = max(4, round(meta["words"] / 190))
        if meta["course"] in by_course:
            by_course[meta["course"]].append(meta)
    for lessons in by_course.values():
        lessons.sort(key=lambda lesson: lesson.get("order_index", 99))
    return by_course


def load_topic(content_root: Path, topic_id: str) -> Topic:
    """Load one topic folder."""
    root = content_root / topic_id
    cfg = _load_config(root / "site.yml")
    cfg["id"] = topic_id
    cfg["base"] = f"{topic_id}/"
    courses = _load_courses(root)
    return Topic(
        id=topic_id,
        root=root,
        config=cfg,
        courses=courses,
        lessons=_load_lessons(root, courses),
    )


def load_topics(repo_root: Path) -> list[Topic]:
    """Every topic listed in topics.yml, in the order it lists them.

    A listed id with no content folder is skipped rather than failing the build,
    so adding a topic in one commit and its lessons in the next still builds.
    """
    registry = yaml.safe_load((repo_root / "topics.yml").read_text(encoding="utf-8")) or {}
    content_root = repo_root / "content"
    topics = []
    for entry in registry.get("topics", []):
        topic_id = entry if isinstance(entry, str) else entry.get("id")
        if topic_id and (content_root / topic_id / "site.yml").exists():
            topics.append(load_topic(content_root, topic_id))
    return topics
