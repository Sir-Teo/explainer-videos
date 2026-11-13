"""The course kit: what turns a series of films into a course, shared by every series but *Quant, Built* (which
came first and keeps its own copy in ``videos/quant/course`` and ``videos/quant/labs``).

A series becomes a course by adding three things beside its films:

* ``videos/<series>/course/``: the course table.  ``__init__.py`` holds ``COURSE = Course(...)`` (the tracks'
  names); every other module in the folder holds ``PARTS = [Part(...), ...]`` for some of the parts.
* ``videos/<series>/labs/labNN.py``: one runnable lab per part (:mod:`videos.coursekit.labs`).
* ``videos/<series>/course/site/widgets/*.js``: one interactive per part, on the site's canvas library
  (``videos/quant/course/site/widgets/00_core.js``), registered as ``QB.W.<name>``.

``tools/series_site.py`` reads all three; ``tests/test_courses.py`` checks them against the manifests.

Every chapter has one home tier: ``U``, ``M``, ``D`` or ``I``.  What the letters are called is the series' choice
(``Course.tracks``): a first course, the full course, the research tier, and practice.  A track watches its own
tier and those it builds on (``TRACK_TIERS``).

    from videos.coursekit import course
    stats = course("stats")
    stats.parts[12].question
    stats.chapters(12)        # [(index, number or None, title, tier), ...] in the film's order
"""

from __future__ import annotations

import functools
import importlib
import re
import runpy
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEOS = ROOT / "videos"
SERIES = ("ai", "stats", "cs", "philosophy", "analysis", "music")
TRACK_TIERS = {"U": "U", "M": "UMI", "D": "UMDI", "I": "UI"}  # the tiers each track watches
TOLERANT = False  # tools/check_course.py sets this: skip a table module that does not import (someone is writing it)
_NUMBERED = re.compile(r"^(\d+)\.\s+(.*)$")


@dataclass(frozen=True)
class Part:
    """One part's course entry.  ``U``, ``D`` and ``I`` list the chapters whose home tier that is, by the number
    in the film's chapter title (0 is the cold open) or, for a chapter without a number, by its scene module
    (``"s12_exam"``).  Chapters in none of them are ``M``; the last chapter, the recap, belongs to every track."""

    n: int
    level: str  # the tier at which the part can first be followed: "U", "M" or "D"
    question: str  # the question the part opens with
    story: str  # the arc, in a paragraph
    handoff: str  # what it leaves for later parts
    objectives: dict  # tier -> things you can do afterwards ("U", "M", "D", "I": at least one each)
    results: list  # [(name, TeX)], the part's key results
    widget: str  # the interactive on the part's page: QB.W.<widget>
    prereq: tuple = ()  # parts of this series to watch first
    outside: str = ""  # what you need from outside the series
    U: tuple = ()
    D: tuple = ()
    I: tuple = ()  # noqa: E741
    also: tuple = field(default_factory=tuple)  # [(label, repo path)]: companion material in this repository


@dataclass(frozen=True)
class Course:
    """A series as a course.  ``tracks`` maps "U", "M", "D", "I" to (name, one-line description)."""

    series: str
    tracks: dict
    track_intro: dict = field(default_factory=dict)  # tier -> a paragraph for the tracks page
    lab_needs: str = "numpy, scipy, matplotlib"  # what a lab needs installed
    library: tuple = ()  # (name, repo path, one line): the series' own library, which the labs call

    @functools.cached_property
    def parts(self) -> dict:
        """{n: Part}, from every module of ``videos/<series>/course`` that has ``PARTS``."""
        out = {}
        for path in sorted((VIDEOS / self.series / "course").glob("*.py")):
            if path.name == "__init__.py":
                continue
            try:
                module = importlib.import_module(f"videos.{self.series}.course.{path.stem}")
            except Exception:  # noqa: BLE001
                if not TOLERANT:
                    raise
                continue
            for p in module.PARTS:
                assert p.n not in out, f"{self.series}: Part {p.n} listed twice"
                out[p.n] = p
        return dict(sorted(out.items()))

    @functools.cached_property
    def n_parts(self) -> int:
        n = 0
        while (VIDEOS / self.series / f"{self.series}{n + 1}" / "manifest.py").exists():
            n += 1
        return n

    def manifest(self, n: int) -> tuple:
        """(film title, [(module, class, chapter title)]) of Part ``n``."""
        m = runpy.run_path(str(VIDEOS / self.series / f"{self.series}{n}" / "manifest.py"))
        return m["TITLE"], [tuple(s) for s in m["SCENES"]]

    def title(self, n: int) -> str:
        t = self.manifest(n)[0]
        m = re.search(r"Part \d+[,:]\s*(.*)$", t)
        return m.group(1) if m else t

    def chapters(self, n: int) -> list:
        """Part ``n``'s chapters in the film's order: (index, number or None, title, tier).  Tiers: ``U``,
        ``M``, ``D``, ``I``, or ``*`` for the recap, which every track watches."""
        part = self.parts[n]
        scenes = self.manifest(n)[1]
        out = []
        for i, (module, _, title) in enumerate(scenes):
            m = _NUMBERED.match(title)
            number = int(m.group(1)) if m else (0 if i == 0 else None)
            keys = {number, module} - {None}
            if i == len(scenes) - 1:
                tier = "*"
            elif keys & set(part.U):
                tier = "U"
            elif keys & set(part.D):
                tier = "D"
            elif keys & set(part.I):
                tier = "I"
            else:
                tier = "M" if part.level == "U" else part.level  # a doctoral part's unlisted chapters are doctoral
            out.append((i, number, m.group(2) if m else title, tier))
        return out

    def track_parts(self, track: str) -> list:
        """The parts a track watches: those with a chapter of the track's own tier (every part, for ``M``)."""
        if track == "M":
            return list(self.parts)
        return [n for n in self.parts if any(c[3] == track for c in self.chapters(n))]


@functools.lru_cache(maxsize=None)
def course(series: str) -> Course | None:
    """The course of a series, or None if it has no course table yet."""
    if not (VIDEOS / series / "course" / "__init__.py").exists():
        return None
    return importlib.import_module(f"videos.{series}.course").COURSE
