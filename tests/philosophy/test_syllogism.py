"""Syllogistic: the textbook counts, and Leibniz's arithmetic agrees with the traditional valid moods."""

from explainer.philosophy.reasoner.syllogism import NAMES, all_moods, leibniz_countermodel, valid


def test_counts():
    moods = all_moods()
    assert len(moods) == 256
    boolean = {m for m in moods if valid(m)}
    trad = {m for m in moods if valid(m, existential=True)}
    assert len(boolean) == 15 and len(trad) == 24
    assert trad == set(NAMES)
    assert boolean < trad


def test_leibniz_matches_tradition():
    leib = {m for m in all_moods() if leibniz_countermodel(m) is None}
    assert leib == set(NAMES)
