"""Every transcribed table names its source, URL and checked date, and holds numbers."""

import datetime as dt

from explainer.industry.data import tables


def _numbers(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from _numbers(v)
        else:
            yield v


def test_tables_are_sourced_and_numeric():
    assert tables.TABLES
    for k, t in tables.TABLES.items():
        assert t.key == k and t.source and t.url.startswith("http") and t.unit and t.definition
        dt.date.fromisoformat(t.checked)
        vals = list(_numbers(t.data))
        assert vals and all(isinstance(v, (int, float)) for v in vals), k


def test_worldsteel_china_share_rises():
    w, c = tables.table("worldsteel.world"), tables.table("worldsteel.china")
    assert c[1995] / w[1995] < 0.15 and c[2025] / w[2025] > 0.5
