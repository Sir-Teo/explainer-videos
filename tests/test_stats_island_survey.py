import numpy as np

from explainer.stats.viz import IslandMap
from explainer.stats.world import World


def test_island_map_has_a_dot_per_town_sized_by_population():
    w = World()
    m = IslandMap(w.towns)
    assert len(m.dots) == 200
    big, small = int(np.argmax(w.towns["weight"])), int(np.argmin(w.towns["weight"]))
    assert m.radii[big] > m.radii[small]


def test_survey_block_is_adult_only_and_biased_as_documented():
    w = World()
    s = w.survey
    A = w.adult
    assert not s["vote_blue"][~A].any() and not s["listed"][~A].any()
    v, L = s["vote_blue"][A], s["listed"][A]
    assert abs(v.mean() - 0.382) < 0.002 and v[L].mean() > v.mean() + 0.05
    p = s["propensity"][A]
    assert p[v].mean() > p[~v].mean()
    assert np.isclose(w.truth("blue_share"), v.mean())
