"""The series' reading map (videos/music/READING.md) is true and up to date: every textbook and theory it lists is
cited by at least one part, and the file is what ``python -m videos.music.reading`` writes."""

from __future__ import annotations

import pytest

from videos.music import reading


@pytest.mark.parametrize("area,short,book,pattern", reading.SPINE, ids=[s for _, s, _, _ in reading.SPINE])
def test_every_textbook_is_cited(area, short, book, pattern):
    assert reading.cited_by(pattern), f"{short}: no part cites {book}"


@pytest.mark.parametrize("area,theory,who,pattern", reading.THEORIES, ids=[t for _, t, _, _ in reading.THEORIES])
def test_every_theory_is_taught(area, theory, who, pattern):
    assert reading.cited_by(pattern), f"{theory} ({who}): no part teaches it"


def test_every_part_has_a_reference_card():
    cards = reading.reference_cards()
    assert sorted(cards) == list(reading.PARTS)
    for n, (books, papers) in cards.items():
        assert books and papers, n


def test_the_map_is_up_to_date():
    on_disk = (reading.HERE / "READING.md").read_text()
    assert on_disk == reading.render(), "run: python -m videos.music.reading"
