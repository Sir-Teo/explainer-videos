"""Monochord's money (Part 60): the waterfall, recoupment, two divisions of a pool, the social-influence market, the
cost disease, ticket pricing, and how many melodies a model makes.

    python -m pytest -q tests/music/test_business.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import business as B
from explainer.music.monochord import melody as M


def test_waterfall_adds_up():
    t = B.Terms()
    rows = B.waterfall(100.0, t)
    whole = sum(r["amount"] for r in rows if not r.get("part"))
    assert whole == pytest.approx(100.0)
    d = {r["who"]: r["amount"] for r in rows}
    assert d["the service"] == pytest.approx(30.0)
    assert d["each songwriter"] * t.writers == pytest.approx(d[f"the songwriters ({t.writers})"])
    # a distributor and no label: the label keeps nothing
    indie = {r["who"]: r["amount"] for r in B.waterfall(100.0, B.Terms(distributor=0.15, artist_royalty=0.97))}
    assert indie["the label"] == pytest.approx(0.0, abs=1e-9)


def test_recoupment():
    r = B.recoup(100.0, [0, 1000, 2000], rate_label=0.5, royalty=0.2)
    assert r["need"] == pytest.approx(1000.0)
    assert r["balance"].tolist() == pytest.approx([-100.0, 0.0, 100.0])
    assert r["label"].tolist() == pytest.approx([-100.0, 300.0, 700.0])


def test_pools():
    p = B.population(n_users=600, seed=1, bots=5)
    a, b = B.pro_rata(p), B.user_centric(p)
    assert a.sum() == pytest.approx(p.fees.sum()) and b.sum() == pytest.approx(p.fees[p.plays.sum(axis=1) > 0].sum())
    ga, gb = B.by_group(p, a), B.by_group(p, b)
    bot_fees = p.fees[np.array(p.kinds) == "bot"].sum()
    assert gb["fraud"] == pytest.approx(bot_fees) and ga["fraud"] > 2 * bot_fees
    assert gb["niche"] > ga["niche"]
    # a hand-made case: two users, one fee each; user-centric pays each user's fee to their own artist
    q = B.Population(np.array([10.0, 10.0]), np.array([[90.0, 0.0], [0.0, 10.0]]), ["x", "y"], ["a", "b"])
    assert B.pro_rata(q).tolist() == pytest.approx([18.0, 2.0]) and B.user_centric(q).tolist() == pytest.approx([10.0, 10.0])


def test_inequality_and_influence():
    assert B.gini([1, 1, 1, 1]) == pytest.approx(0.0)
    assert B.gini([0, 0, 0, 1]) == pytest.approx(0.75)
    assert B.top_share([5, 3, 1, 1], 0.25) == pytest.approx(0.5)
    ml = B.musiclab(songs=24, participants=400, worlds=4, seed=2)
    assert ml["gini_social"] > ml["gini_independent"]
    assert all(abs(s.sum() - 1) < 1e-9 for s in ml["social"])


def test_baumol_and_tickets():
    assert B.baumol([1790 + 35], 0.02, 1790)[0] == pytest.approx(math.exp(0.7))
    t = B.tickets(seats=1000, fans=3000, face=80.0, seed=1)
    assert t["dynamic"]["artist"] >= t["clearing_price"]["artist"] >= t["face_value"]["artist"]
    assert t["face_value"]["artist"] == pytest.approx(80.0 * 1000)
    assert t["clearing_price"]["resellers"] == 0.0 and t["face_value"]["resellers"] > 0


def test_collision_exact():
    # a model with a uniform alphabet of size A: the collision probability of k notes is A^-k
    class Uniform:
        order = 1
        def distribution(self, ctx):
            return {a: 0.25 for a in range(4)}
    assert B.collision(Uniform(), 3) == pytest.approx(4.0 ** -3)
    m = M.NGram(2).fit(M.corpus())
    q4 = B.collision(m, 4)
    # against sampling: the share of pairs of independent draws that share an opening
    rng_pairs = [(tuple(m.generate(4, start=(), seed=2 * i)), tuple(m.generate(4, start=(), seed=2 * i + 1))) for i in range(3000)]
    share = np.mean([a == b for a, b in rng_pairs])
    assert share == pytest.approx(q4, abs=4 * math.sqrt(q4 / 3000) + 1e-4)
    assert B.collision(m, 6) < q4 and B.effective_melodies(m, 8) < len(m.alphabet) ** 8
    assert B.shared_window_prob(1e-6, 10, 10) == pytest.approx(1 - math.exp(-1e-4))
    assert B.birthday(1e-6, 1001) == pytest.approx(1001 * 1000 / 2 * 1e-6)
