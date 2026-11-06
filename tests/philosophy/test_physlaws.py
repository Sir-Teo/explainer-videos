"""Tests for the Reasoner's laws, chance and the arrow of time (Part 24)."""

import math

from explainer.philosophy.reasoner import physlaws as L


def test_best_system_picks_the_true_degree():
    b = L.best_system()
    assert b["best_degree"] == 2
    totals = {r["degree"]: r["total"] for r in b["rows"]}
    assert totals[2] < totals[1] < totals[0]
    assert all(totals[d] > totals[2] for d in range(3, 8))


def test_undermining_futures():
    u = L.undermining(10, 5, 10)
    # only exactly five future heads keep the frequency at one half: C(10,5) / 2^10
    assert math.isclose(u["consistent_chance"], round(252 / 1024, 4))
    assert math.isclose(u["undermining_chance"] + u["consistent_chance"], 1.0, abs_tol=1e-4)
    assert sum(r["undermines"] for r in u["rows"]) == 10


def test_new_principle_converges():
    r = L.new_principle(3)
    assert math.isclose(r["rows"][0]["np"], 21 / 252, abs_tol=1e-5)
    nps = [x["np"] for x in r["rows"]]
    assert nps == sorted(nps) and abs(nps[-1] - 0.125) < 1e-3


def test_norton_dome_solves_newton_and_is_indeterministic():
    d = L.norton_dome()
    assert all(s["max_error"] < 1e-12 for s in d["solutions"])
    for c in d["finite_difference_check"]:
        assert math.isclose(c["rdd"], c["sqrt_r"], rel_tol=1e-3)
    assert not d["deterministic"]


def test_lorenz_lyapunov_and_horizons():
    lz = L.lorenz(t_max=30.0)
    assert 0.85 < lz["lyapunov"] < 0.96
    times = [h["time"] for h in lz["horizons"]]
    assert times == sorted(times)
    # each factor of 1000 in precision buys roughly ln(1000) / lambda more time
    gaps = [b - a for a, b in zip(times, times[1:])]
    assert all(4.0 < g < 11.0 for g in gaps)


def test_roulette_gives_one_half_for_any_smooth_spread():
    r = L.arbitrary_functions(samples=50000)
    assert all(abs(x["red"] - 0.5) < 0.02 for x in r["rows"])
    flips = sum(1 for a, b in zip(r["red_at_v"], r["red_at_v"][1:]) if a != b)
    assert flips > 10


def test_h_falls_loschmidt_reverses_and_rotors_recur():
    h = L.h_theorem(n=3000, steps=6)
    assert h["H"][-1] < h["H"][0] - 1.0 and math.isclose(h["energy"], 1.0, abs_tol=1e-9)
    g = L.free_gas()
    e = g["entropy"]
    assert e[0] == 0.0 and max(e) > 3.0 and e[-1] == e[0]
    r = L.recurrence(max_n=3, t_total=5000.0)
    gaps = [x["mean_gap"] for x in r["rows"]]
    assert gaps == sorted(gaps) and gaps[-1] > 10 * gaps[0]


def test_kac_ring_decays_recurs_and_reverses():
    k = L.kac_ring()
    assert k["returns"] and k["reverse_returns"]
    assert abs(k["delta"][100]) < 0.2
    # every ball has crossed every marker once at t = N: an odd number of markers turns them all black
    assert k["half_way"] == (-1.0 if k["markers"] % 2 else 1.0)
    s = L.kac_states()
    assert s["returns_at_2N"] and s["whites"][0] == s["N"]


def test_boltzmann_and_landauer():
    b = L.boltzmann(100)
    assert math.isclose(b["p_all_left_log10"], -30.1, abs_tol=0.01)
    assert b["fraction_within_10pct"] > 0.96
    drops = [f["entropy_drop"] for f in b["fluctuations"]]
    probs = [f["log10_p"] for f in b["fluctuations"]]
    assert drops == sorted(drops) and probs == sorted(probs, reverse=True)
    la = L.landauer()
    assert math.isclose(la["joules_per_bit"], 2.87e-21, rel_tol=1e-3)
    assert la["toffoli_bijective"] and 1.18 < la["and_lost_bits"] < 1.19
    sz = L.szilard()
    best = max(sz["rows"], key=lambda r: r["theory_kT"])
    assert best["x"] == 0.5 and math.isclose(best["theory_kT"], math.log(2), abs_tol=1e-4)
    assert all(abs(r["simulated_kT"] - r["theory_kT"]) < 0.02 for r in sz["rows"])
