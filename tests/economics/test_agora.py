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


# ---------------------------------------------------------------------------
# Part 3: national accounts and index numbers
# ---------------------------------------------------------------------------
def test_island_accounts_agree_three_ways():
    from explainer.economics.agora.accounts import IOTable

    t = IOTable(**truths(3)["accounts"])
    t.check()
    g = t.gdp()
    assert g["output"] == g["income"] == g["expenditure"] == 740
    e = t.expenditure()
    saving = t.income()["wages"] + t.income()["profits"] + 10 - e["C"]   # households keep the council's transfer of 10
    assert saving == e["I"] + (e["X"] - e["M"])                          # S = I + NX: the boats were partly borrowed
    L = t.leontief()
    assert np.all(L >= -1e-12) and np.all(np.diag(L) >= 1)
    # Leontief: producing final demand needs exactly the gross output
    f = sum(t.final.values())
    assert np.allclose(L @ f, t.gross_output())
    va = t.value_added_in("X")
    assert 0 < va["share"] < 1


def test_inconsistent_accounts_are_refused():
    from explainer.economics.agora.accounts import IOTable

    a = dict(truths(3)["accounts"])
    a["wages"] = (161, 180, 70, 40)
    with pytest.raises(ValueError):
        IOTable(**a).check()


def test_index_numbers_bracket_the_true_cost_of_living():
    from explainer.economics.agora import indices as ix

    rng = np.random.default_rng(3)
    for _ in range(50):
        n = 4
        sh = rng.dirichlet(np.ones(n))
        p0, p1 = rng.uniform(0.5, 2, n), rng.uniform(0.5, 2, n)
        q0 = ix.cobb_douglas_demand(p0, 100, sh)
        q1 = ix.cobb_douglas_demand(p1, 130, sh)
        true = ix.cost_of_living(p0, p1, sh)
        assert ix.paasche(p0, p1, q1) <= true + 1e-12 <= ix.laspeyres(p0, p1, q0) + 2e-12
        assert abs(ix.tornqvist(p0, p1, q0, q1) - true) < 1e-12        # exact for Cobb-Douglas tastes
        assert ix.paasche(p0, p1, q1) <= ix.fisher(p0, p1, q0, q1) <= ix.laspeyres(p0, p1, q0)


def test_chained_fisher_does_not_drift():
    from explainer.economics.agora import indices as ix

    P = np.array([[1, 1, 1], [2, 1, 0.8], [1.3, 1.6, 1], [1, 1, 1]], float)
    sh = np.array([0.5, 0.3, 0.2])
    Q = np.array([ix.cobb_douglas_demand(p, 100, sh) for p in P])
    d = ix.chain_drift(P, Q)
    assert d["laspeyres"] > 1.01 and d["paasche"] < 0.99
    # Fisher is not exactly path-independent, but its drift is tiny next to Laspeyres's; Tornqvist is exact for
    # Cobb-Douglas tastes
    assert abs(d["fisher"] - 1) < 0.005 < d["laspeyres"] - 1 and abs(d["tornqvist"] - 1) < 1e-9


# --- Part 4: the Island's econometrician ---------------------------------------------------------------------------
def test_simultaneity_and_the_instrument():
    from explainer.economics import island
    from explainer.economics.agora import econometrician as em

    t = island.truths(4)["season"]
    big = dict(t, days=40000)
    s = em.fish_season(**big)
    var_u = t["feast"][1] ** 2 * t["feast"][0] * (1 - t["feast"][0]) + t["noise"][0] ** 2
    var_v = t["storm"][1] ** 2 * t["storm"][0] * (1 - t["storm"][0]) + t["noise"][1] ** 2
    plim = em.simultaneity_slope(t["b"], t["d"], var_u, var_v)
    assert abs(em.ols(s["q"], s["p"])["slope"] - plim) < 1.5          # least squares finds neither curve
    assert abs(em.wald(s["q"], s["p"], s["storm"])["estimate"] + t["b"]) < 2.0    # storms trace demand
    assert abs(em.wald(s["q"], s["p"], s["feast"])["estimate"] - t["d"]) < 2.0    # feasts trace supply
    w = em.wald(s["q"], s["p"], s["storm"])["estimate"]
    assert abs(em.iv(s["q"], s["p"], s["storm"])["estimate"] - w) < 1e-6         # one binary instrument: 2SLS = Wald


def test_omitted_ability_and_lucas():
    from explainer.economics import island
    from explainer.economics.agora import econometrician as em

    sc = dict(island.truths(4)["schooling"], n=60000)
    sc["return_"] = sc.pop("return")
    r = em.schooling_records(**sc)
    bias = em.ovb(sc["ability_on_wage"], np.cov(r["school"], r["ability"])[0, 1], r["school"].var())
    assert abs(em.ols(r["logw"], r["school"])["slope"] - (sc["return_"] + bias)) < 0.005
    assert abs(em.iv(r["logw"], r["school"], r["near"])["estimate"] - sc["return_"]) < 0.01
    L = em.lucas_islands(**island.truths(4)["lucas"])
    assert em.ols(L["y"][L["calm"]], L["pi"][L["calm"]])["slope"] > 0.5        # a tradeoff in calm years
    assert abs(L["y"][-10:].mean() - L["ystar"]) < 0.5                          # gone once it is exploited
    assert em.did(20.44, 21.03, 23.33, 21.17) == pytest.approx(2.75, abs=0.01)


def test_the_lottery_balances_what_nobody_sees():
    from explainer.economics import island
    from explainer.economics.agora import econometrician as em

    a = dict(island.truths(4)["apprentice"], n=200000)
    r = em.apprenticeship(**a)
    ch, lo = r["by_choice"], r["by_lottery"]
    assert ch["ability1"] < ch["ability0"] - 0.8                     # the choosers differ in what nobody sees
    assert ch["diff"] < 0 < a["effect"]                              # so the comparison gets even the sign wrong
    assert ch["diff"] == pytest.approx(a["effect"] + r["bias"], abs=0.005)    # the bias is ability's gap
    assert abs(lo["ability1"] - lo["ability0"]) < 0.02               # the lottery's groups are alike
    assert abs(lo["diff"] - a["effect"]) < 3 * lo["se"]


def test_spillovers_hide_from_a_trial_within_villages():
    from explainer.economics import island
    from explainer.economics.agora import econometrician as em

    t = dict(island.truths(4)["villages"], villages=2000)
    r = em.village_trial(**t)
    assert abs(r["within"] - t["direct"]) < 0.01                      # a trial inside villages finds the direct effect
    assert abs(r["spill_hat"] - t["spill"]) < 0.02                    # the shares reveal the spillover
    assert abs(r["total"] - (t["direct"] + t["spill"])) < 0.02        # and scaling up delivers much less

