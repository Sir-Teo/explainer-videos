"""The Facts, the Dials and Called it?: their schemas hold, and the parts they name exist."""

from explainer.economics import calls, dials, facts, island


def test_facts():
    keys = [f.key for f in facts.FACTS]
    assert len(keys) == len(set(keys)) >= 30
    for f in facts.FACTS:
        assert f.group in facts.GROUPS and 1 <= f.shown <= 68 and 1 <= f.explained <= 68
    assert set(facts.AGORA) <= set(keys)


def test_dials():
    for d in dials.DIALS.values():
        assert d.status in dials.STATUSES and all(1 <= p <= 68 for p in d.parts)
    assert all(isinstance(reason, str) and reason for rows in dials.SHOWN.values() for _, reason in rows)


def test_calls_and_cast():
    for c in calls.CALLS.values():
        assert c.verdict in calls.VERDICTS and 1 <= c.part <= 68 and c.sources
    assert {"crusoe", "friday"} <= set(island.CAST) and all(1 <= x.arrives <= 68 for x in island.CAST.values())
