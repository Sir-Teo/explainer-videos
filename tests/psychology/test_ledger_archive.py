"""The Ledger's records are well formed, and the Archive's numbers support the arithmetic the films do with them."""

import datetime
import math

import pytest

from explainer.psychology import archive, battery, ledger
from explainer.psychology.psyche import chronometry as ch


def test_every_row_has_a_status_sources_and_a_date():
    assert ledger.rows()
    for f in ledger.rows():
        assert f.status in ledger.STATUSES and f.sources and f.claim.endswith(".")
        datetime.date.fromisoformat(f.checked)
        assert f.original.year <= min([s.year for s in f.record] or [9999]) or f.key == "donders_insertion"
    assert sum(ledger.counts().values()) == len(ledger.rows())
    assert [f.key for f in ledger.rows(part=1)][:2] == ["nerve_speed", "donders_ordering"]


def test_a_row_without_sources_is_refused():
    with pytest.raises(ValueError):
        ledger.Finding("x", 1, "X", "A claim.", ledger.Study("Someone", 1900), "replicated")
    with pytest.raises(ValueError):
        ledger.Finding("x", 1, "X", "A claim.", ledger.Study("Someone", 1900), "probably fine", sources=("s",),
                       checked="2026-01-01")


def test_helmholtz_range_follows_from_his_numbers():
    d = archive.HELMHOLTZ_1850.data
    lo = ch.conduction_speed(d["length_mm"][0], d["delay_s"][1])
    hi = ch.conduction_speed(d["length_mm"][1], d["delay_s"][0])
    assert (round(lo), round(hi)) == tuple(round(v) for v in d["speed_frog"])
    row = ledger.get("nerve_speed").original
    assert (row.lo, row.hi) == d["speed_frog"]


def test_donders_differences():
    d = archive.DONDERS_1868.data
    assert d["c"] - d["a"] == 36 and d["b"] - d["c"] == 47 and d["a"] < d["c"] < d["b"]
    assert ch.DONDERS_1868 == {k: d[k] for k in "abc"}


def test_ebbinghaus_formula_reproduces_his_fitted_column():
    d = archive.EBBINGHAUS_1885.data
    for t, calc, obs, hours in zip(d["minutes"], d["calculated"], d["saving"], d["hours"]):
        b = 100 * d["k"] / (math.log10(t) ** d["c"] + d["k"])
        assert b == pytest.approx(calc, abs=0.15)
        assert abs(b - obs) < 3.5
        assert t == pytest.approx(60 * hours, rel=0.07)


def test_every_dataset_is_registered_with_a_check():
    for d in archive.ALL.values():
        assert d.source and d.cite and d.licence and "2026" in d.checked


def test_battery_lists_thirteen_tasks_and_runs_the_first():
    assert len(battery.TASKS) == 13 and [t.number for t in battery.TASKS][-1] == "Q"
    tr = battery.run("rt_choice", ch.donders_models()["b"], 500, seed=1)
    assert len(tr) == 500 and set(tr.condition) == {"b"} and tr.mean_rt("b") == pytest.approx(284, abs=8)
