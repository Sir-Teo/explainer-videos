"""The Ledger gate (``tools/check_ledger.py``): every study a part shows has a Ledger row, or a stated reason."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import check_ledger as gate  # noqa: E402

from explainer.psychology import archive, ledger  # noqa: E402

PARTS = gate.built_parts()


@pytest.mark.parametrize("video", list(PARTS.values()))
def test_every_built_part_passes(video):
    problems, notes = gate.check(video)
    assert not problems, "\n".join(problems)
    assert notes[0].endswith("rows entered")


def test_rows_name_datasets_the_archive_holds():
    named = {name for f in ledger.rows() for name in f.data}
    assert named and all(hasattr(archive, name) for name in named)
    assert "PFUNGST_1907" in ledger.get("clever_hans").data


def test_a_study_shown_without_a_row_is_caught(monkeypatch):
    kept = [s for s in ledger.SHOWN if s.name != "PEIRCE_JASTROW_1884"]
    monkeypatch.setattr(ledger, "SHOWN", kept)
    problems, _ = gate.check("psych2")
    assert any("PEIRCE_JASTROW_1884" in p and "no Ledger row" in p for p in problems)


def test_a_tag_citing_a_study_outside_the_ledger_is_caught(monkeypatch):
    kept = [s for s in ledger.SHOWN if "Arnett" not in s.name]
    monkeypatch.setattr(ledger, "SHOWN", kept)
    problems, _ = gate.check("psych2")
    assert any("Arnett (2008)" in p and "Henrich (2010)" in p for p in problems)


def test_a_declaration_nothing_needs_is_stale(monkeypatch):
    extra = ledger.SHOWN + [ledger.Shown(2, "KANT_1786", "not shown in Part 2 at all")]
    monkeypatch.setattr(ledger, "SHOWN", extra)
    problems, _ = gate.check("psych2")
    assert any("stale" in p and "KANT_1786" in p for p in problems)


def test_a_deferred_row_comes_due_when_its_part_is_built(monkeypatch):
    monkeypatch.setattr(gate, "built_parts", lambda: {**PARTS, 38: "psych38"})
    problems, _ = gate.check("psych2")
    assert any("deferred to Part 38" in p for p in problems)
    assert not any("Part 42" in p for p in problems)


def test_a_declaration_needs_a_reason_and_a_later_part():
    with pytest.raises(ValueError):
        ledger.Shown(2, "X", "  ")
    with pytest.raises(ValueError):
        ledger.Shown(5, "X", "a reason", row_in=5)


def test_what_a_part_shows_is_read_from_its_sources(tmp_path):
    (tmp_path / "s01_demo.py").write_text(
        "def f():\n"
        "    a = historical_tag(archive.PFUNGST_1907.cite + r', ch.~II')\n"
        "    b = published_tag(r'Woodley et al.\\ (2013); \\ ' + archive.WOODS_2015.cite)\n"
        "    c = published_tag(r'Somebody \\& Other (1999)')\n")
    (tmp_path / "compute.py").write_text("x = archive.LIT_2011.data\n")
    datasets, literals = gate.shown_in(tmp_path)
    assert set(datasets) == {"PFUNGST_1907", "WOODS_2015", "LIT_2011"}
    assert set(literals) == {r"Woodley et al.\ (2013)", r"Somebody \& Other (1999)"}
    assert gate.cited("Woodley", 2013, ledger.rows(upto=1)) and not gate.cited("Somebody", 1999, ledger.rows())


def test_the_readme_table_is_read():
    table = gate.readme_table("x\n| Finding | Original | Status |\n|---|---|---|\n| A | B 1900 | replicated (so) |\n\ny")
    assert table == [("A", "B 1900", "replicated (so)")]
