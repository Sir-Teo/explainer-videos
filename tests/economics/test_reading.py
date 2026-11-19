"""The series' reading map (videos/economics/READING.md) is true and up to date: every textbook and paper it lists
is planned by the syllabus for at least one part, every built part has a reference card, and the file is what
``python -m videos.economics.reading`` writes."""

from __future__ import annotations

import pytest

from videos.economics import reading


@pytest.mark.parametrize("tier,short,book,pattern", reading.SPINE, ids=[s for _, s, _, _ in reading.SPINE])
def test_every_textbook_is_planned(tier, short, book, pattern):
    assert reading.planned_in(pattern), f"{short}: no part's syllabus entry names {book}"


@pytest.mark.parametrize("area,model,paper,pattern", reading.PAPERS, ids=[m for _, m, _, _ in reading.PAPERS])
def test_every_paper_is_planned(area, model, paper, pattern):
    assert reading.planned_in(pattern), f"{model} ({paper}): no part's syllabus entry names it"


def test_the_syllabus_has_every_part():
    assert sorted(reading.syllabus_entries()) == list(reading.PARTS)


def test_every_built_part_has_a_reference_card():
    cards = reading.reference_cards()
    assert sorted(cards) == reading.built_parts()
    for n, (books, papers) in cards.items():
        assert books and papers, n


def test_the_map_is_up_to_date():
    on_disk = (reading.HERE / "READING.md").read_text()
    assert on_disk == reading.render(), "run: python -m videos.economics.reading"
