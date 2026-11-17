"""videos/psychology/READING.md, the map of textbooks, theories and classic studies, must point at the films.

Every "where" in its tables (``28 · ch. 5``, or ``28 · hook``) must name a part and a chapter that exist, and the
author (or another capitalized name) in the row's source column must be named in the scenes of at least one of
the parts given, so the map cannot drift from what the films actually show.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
READING = ROOT / "videos" / "psychology" / "READING.md"
WHERE = re.compile(r"(\d+) · (?:ch\. (\d+)|hook)")
STOP = {"The", "And", "With", "From", "Part"}


def chapters(part: int) -> dict[int, str]:
    m = importlib.import_module(f"videos.psychology.psych{part}.manifest")
    out = {}
    for module, cls, title in m.SCENES:
        hit = re.match(r"(\d+)\.", title)
        if hit:
            out[int(hit.group(1))] = module
        elif cls == "Hook":
            out[0] = module
    return out


def scenes_text(part: int) -> str:
    return "\n".join(p.read_text() for p in sorted((ROOT / "videos" / "psychology" / f"psych{part}").glob("s*.py")))


def rows():
    """(section, cells) for every table row whose last-but-maybe-one cell names a place in the films."""
    section = ""
    for line in READING.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:]
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if any(WHERE.search(c) for c in cells) and section[:2] in ("2.", "3.", "4."):
            yield section, cells


ROWS = list(rows())


def test_the_map_has_rows():
    assert len(ROWS) > 150
    sections = {s[:2] for s, _ in ROWS}
    assert sections == {"2.", "3.", "4."}


@pytest.mark.parametrize("section,cells", ROWS, ids=[c[0][:40] for _, c in ROWS])
def test_every_place_exists_and_names_its_source(section, cells):
    where = next(c for c in cells if WHERE.search(c))
    places = [(int(p), int(ch) if ch else 0) for p, ch in WHERE.findall(where)]
    for part, ch in places:
        assert 1 <= part <= 62, (cells[0], part)
        assert ch in chapters(part), f"{cells[0]}: Part {part} has no chapter {ch}"
    who = cells[1]
    names = [w for w in re.findall(r"[A-ZÀ-Ý][\w'’\-]{3,}", who) if w not in STOP]
    if not names:
        return
    text = "\n".join(scenes_text(p) for p, _ in places)
    plain = text.replace('\\"o', "ö").replace("\\'e", "é").replace("\\o ", "ø").replace("\\o{}", "ø")
    assert any(n in plain or n.replace("ø", "o") in plain for n in names), \
        f"{cells[0]}: none of {names} is named in Parts {[p for p, _ in places]}"


def test_every_part_is_on_the_spine():
    spine = READING.read_text().split("## 2.")[0]
    named = set()
    for a, b in re.findall(r"(\d+)(?:–(\d+))?", spine):
        a = int(a)
        if a > 62:
            continue
        named.update(range(a, int(b) + 1) if b else [a])
    missing = set(range(1, 63)) - named
    assert not missing, f"parts not on the textbook spine: {sorted(missing)}"


def test_nothing_left_unlocated():
    assert "MISSING" not in READING.read_text()
