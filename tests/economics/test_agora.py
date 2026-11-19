"""Agora's Part 1 modules, each checked against something it does not compute itself: a brute-force optimum, a
closed form, or a property any correct answer must have."""

from itertools import combinations

import numpy as np
import pytest

from explainer.economics.agora import crusoe as cr
from explainer.economics.agora import market as mk
from explainer.economics.agora import signals
from explainer.economics.island import truths


def brute_surplus(values, costs) -> float:
    """The largest total gain over every way of choosing k buyers and k sellers to trade (any k)."""
    best = 0.0
    for k in range(1, min(len(values), len(costs)) + 1):
        for b in combinations(values, k):
            for s in combinations(costs, k):
                best = max(best, sum(b) - sum(s))
    return best


@pytest.mark.parametrize("seed", range(8))
def test_equilibrium_against_brute_force(seed):
    rng = np.random.default_rng(seed)
    values = tuple(np.round(rng.uniform(1, 4, 6), 2))
    costs = tuple(np.round(rng.uniform(1, 4, 6), 2))
    m = mk.Market(values, costs)
    eq = m.equilibrium()
    assert abs(eq["surplus"] - brute_surplus(values, costs)) < 1e-9
    # every price strictly inside the band clears the market: as many willing buyers as willing sellers, q of each
    if eq["p_hi"] > eq["p_lo"] + 1e-9:
        p = (eq["p_lo"] + eq["p_hi"]) / 2
        assert m.demand(p) == m.supply(p) == eq["q"]


def test_the_pit_of_part_one():
    pit = truths(1)["pit"]
    m = mk.Market(pit["values"], pit["costs"])
    eq = m.equilibrium()
    assert (eq["q"], eq["p_lo"], eq["p_hi"]) == (6, 2.2, 2.3)
    assert abs(eq["surplus"] - 6.7) < 1e-9


def test_traders():
    pit = truths(1)["pit"]
    m = mk.Market(pit["values"], pit["costs"])
    zi = [mk.double_auction(m, "zi", periods=4, seed=s) for s in range(12)]
    zp = [mk.double_auction(m, "zip", periods=6, seed=s) for s in range(12)]
    # nobody trades at a loss, and no trade is outside the traders' cards
    for r in zi + zp:
        for p in r["periods"]:
            for t in p["trades"]:
                assert t["cost"] <= t["price"] <= t["value"]
            assert 0 <= p["efficiency"] <= 1 + 1e-9
    assert np.mean([p["efficiency"] for r in zi for p in r["periods"]]) > 0.85  # Gode and Sunder's result
    a0 = np.median([r["periods"][0]["alpha"] for r in zp])
    a5 = np.median([r["periods"][-1]["alpha"] for r in zp])
    assert a5 < a0 / 2  # traders who learn converge
    assert mk.convergence_alpha([2.0, 2.0], 2.0) == 0.0


def test_crusoe_closed_form():
    """With square-root technologies and Cobb-Douglas tastes the best split is h* = theta T."""
    for theta in (0.3, 0.5, 0.6, 0.8):
        c = cr.Crusoe(theta=theta)
        b = c.best()
        assert abs(b["h"] - theta * c.hours) < 1e-5
        assert abs(b["mrs"] - b["mrt"]) < 1e-5
    c = cr.Crusoe()
    for h in (1.0, 5.0, 9.0):
        oc = c.marginal(h)["opportunity_cost"]
        assert abs(oc - 4 / 3 * np.sqrt(h / (10 - h))) < 1e-12
        # the slope of the frontier, by a finite difference
        e = 1e-6
        slope = (c.coconuts(h + e) - c.coconuts(h - e)) / (c.fish(h + e) - c.fish(h - e))
        assert abs(-slope - oc) < 1e-5


def test_ricardo():
    r = cr.ricardo(**truths(1)["two"])
    # with full specialization the fish market clears at p = theta C_f / ((1 - theta) F_c)
    theta = r["theta"]
    fc = r["people"][0]["makes"]["fish"]
    cf = r["people"][1]["makes"]["coconuts"]
    assert abs(r["price"] - theta * cf / ((1 - theta) * fc)) < 1e-9
    assert r["band"][0] < r["price"] < r["band"][1]
    assert all(p["gain_u"] > 0 for p in r["people"])
    # a very productive fish maker leaves the price at his own opportunity cost: he gains nothing, the other gains
    big = cr.ricardo(hours_per_fish=(1.0, 4.0), hours_per_coconut=(1.0, 2.0), theta=0.6)
    assert abs(big["price"] - big["band"][0]) < 1e-9 and "makes both" in big["regime"]
    assert abs(big["people"][0]["gain_u"]) < 1e-9 and big["people"][1]["gain_u"] > 0


def test_hayek():
    u = signals.users(60, seed=1945)
    c = signals.clear(u, 0.2)
    assert abs(c["q1"].sum() - 0.8 * u["supply"]) < 1e-6
    t = signals.tatonnement(u, 0.2)
    assert abs(t["path"][-1] - c["price"]) < 1e-6
    cmp_ = signals.compare(u, 0.2)
    assert cmp_["loss_price"] < cmp_["loss_rationing"]
    # when every user has the same elasticity, the price cuts everyone by the same share: rationing loses nothing more
    same = {"a": u["a"], "e": np.full(u["n"], 0.8), "n": u["n"], "supply": u["supply"]}
    s = signals.compare(same, 0.2)
    assert abs(s["loss_price"] - s["loss_rationing"]) < 1e-6 * s["loss_price"]


# ---------------------------------------------------------------------------
# Part 2: smooth curves, wedges and controls
# ---------------------------------------------------------------------------
def test_curves_tax_incidence_and_equivalence():
    from explainer.economics.agora.curves import Linear, buyers_share

    L = Linear.from_crowd(1000, 4.0, 0.5, 4.0)
    el = L.elasticity()
    on_s, on_b = L.tax(0.4, "sell"), L.tax(0.4, "buy")
    assert abs(on_s["paid"] - on_b["paid"]) < 1e-12 and abs(on_s["received"] - on_b["received"]) < 1e-12
    assert abs(on_s["buyers_share"] - buyers_share(el["demand"], el["supply"])) < 1e-9  # exact on straight lines
    assert abs(on_s["buyers_share"] + on_s["sellers_share"] - 1) < 1e-12
    e = L.equilibrium()
    assert abs(on_s["dwl"] - 0.5 * 0.4 * (e["q"] - on_s["q"])) < 1e-9


def test_curves_arc_elasticity_is_symmetric_and_revenue_peaks_at_unit_elasticity():
    from explainer.economics.agora.curves import Linear, arc_elasticity

    assert abs(arc_elasticity(100, 80, 2, 3) - arc_elasticity(80, 100, 3, 2)) < 1e-12
    L = Linear(a=100, b=10, c=0, d=10)
    p = np.linspace(0.01, 9.99, 9999)
    best = p[np.argmax(L.revenue(p))]
    assert abs(best - 5) < 1e-2 and abs(L.elasticity(5.0)["demand"] + 1) < 1e-12


def test_curves_cap_lottery_matches_a_simulated_crowd():
    from explainer.economics.agora.curves import Linear, crowd

    n, pm = 200_000, 1.8
    L = Linear.from_crowd(n, 4.0, 0.5, 4.0)
    v, c = crowd(n, 4.0, 0.5, 4.0, seed=3)
    k = int((c <= pm).sum())
    win = np.random.default_rng(0).choice(v[v >= pm], k, replace=False)
    lottery = (v[:k].sum() - win.sum())
    assert abs(lottery / L.cap(pm)["lottery"] - 1) < 0.02


def test_the_pit_with_a_tax_and_with_controls():
    """Who remits the tax does not matter in the pit either; a binding cap or floor loses the triangle and, because
    learning traders all call the legal limit, the lottery on top."""
    m = mk.Market([3.40, 3.10, 2.90, 2.70, 2.50, 2.30, 2.10, 1.90, 1.70, 1.50],
                  [1.20, 1.40, 1.60, 1.80, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00])

    def last(**kw):
        runs = [mk.double_auction(m, "zip", periods=6, seed=s, **kw)["periods"][-1] for s in range(24)]
        return {k: float(np.nanmedian([r[k] for r in runs])) for k in ("paid", "received", "efficiency", "n")}

    s, b = last(tax=0.4, tax_on="sell"), last(tax=0.4, tax_on="buy")
    assert abs(s["paid"] - b["paid"]) < 0.05 and abs(s["received"] - b["received"]) < 0.05
    assert s["n"] == b["n"] == 5 and abs(s["efficiency"] - 6.6 / 6.7) < 0.01
    cap = last(cap=2.0)
    assert cap["n"] == 5 and cap["efficiency"] < 0.9  # random rationing predicts 5.57 / 6.70 = 0.83
    floor = last(minimum=2.6)
    assert floor["n"] == 4 and floor["efficiency"] < 0.75  # 4.5 / 6.7 = 0.67
