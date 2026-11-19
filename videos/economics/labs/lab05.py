"""Lab 5: demand from tastes, consistency from choices, power, kinks, and a value of time from a logit."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import consumer as cs
from explainer.economics.island import truths

TITLE = "What people want: demand, revealed preference and its power"
GOAL = ("Check CES demand against a search along the budget line and its homogeneity; test the Island's four "
        "choosers for GARP, rationalize the consistent ones with Afriat's linear programme and compute the others' "
        "efficiency; measure how the power of the test against random choice grows with the number of budgets; run "
        "GARP on America's spending since 1929; check the bunching window at the EITC's kink; and recover a value of "
        "time from simulated ferry choices, with its interval's coverage.")
TASKS = [
    "Give Bo a tremble four times as large. How often do his eleven choices now fail GARP, and what is his typical "
    "efficiency index? Compare with random choosers on the same lines.",
    "Replace the eleven Play-it lines by eleven lines that never cross (each a scaled copy of the first). What is the "
    "power of the test now, and why?",
    "In the ferry survey, let travellers' value of time differ (half value it at $10 an hour, half at $20). What does "
    "the logit estimate, and what does it mean?",
]


def _lines(T):
    L = np.array(T["budgets"]["lines"], float)
    return np.column_stack([60 / L[:, 0], 60 / L[:, 1]]), np.full(len(L), 60.0)


def run(seed=0):
    lab = labs.Lab()
    T = truths(5)
    rng = np.random.default_rng(500 + seed)

    # CES demand against search, and homogeneity of degree zero
    pref = cs.Preference("ces", a=0.4, sigma=0.6)
    x, y = pref.demand(2.0, 5.0, 100.0)
    xs = np.linspace(0, 50, 50001)
    best = cs.best_on_frontier(pref, xs, (100 - 2 * xs) / 5)
    assert abs(best["x"] - x) < 0.01
    assert np.allclose(pref.demand(2.0, 5.0, 100.0), pref.demand(4.0, 10.0, 200.0))
    lab.row("CES (a = 0.4, sigma = 0.6) at prices 2, 5 and $100", f"x = {x:.3f}, y = {y:.3f}; search x = {best['x']:.3f}")

    # the four choosers on the eleven lines
    P, m = _lines(T)
    spec = T["choosers"]
    res = {}
    for who in ("bo", "ana", "chidi", "dara"):
        s = spec[who]
        if s["kind"] == "random":
            X = cs.random_on_budgets(P, m, rng)
        else:
            pr = cs.Preference(s["kind"], a=s.get("a", 0.5), b=s.get("b", 1.0))
            X = np.array([pr.demand(px, py, mm) for (px, py), mm in zip(P, m)])
        sol = cs.afriat(P, X)
        res[who] = (cs.ccei(P, X), sol is not None)
        lab.row(f"{who}: Afriat's index, rationalizable?", f"{res[who][0]:.3f}, {'yes' if res[who][1] else 'no'}")
        assert res[who][1] == (res[who][0] >= 1.0)

    # power against random choice, by the number of random budgets
    powers = {}
    for n in (5, 11, 25, 50):
        Pn = rng.uniform(0.5, 3.0, (n, 2))
        powers[n] = cs.bronars(Pn, np.full(n, 30.0), reps=400, seed=seed + n)["power"]
    lab.row("power against random choice, 5 / 11 / 25 / 50 random budgets",
            " / ".join(f"{100 * powers[n]:.0f}%" for n in (5, 11, 25, 50)))
    b11 = cs.bronars(P, m, reps=1000, seed=seed + 1987)["power"]
    lab.row("power on the eleven Play-it lines", f"{100 * b11:.1f}%")
    assert powers[50] > powers[5] and b11 > 0.9

    # America as one consumer
    d = data.pce_by_type()
    v = cs.garp_violations(d["prices"], d["quantities"])
    lab.row("America 1929-2025, 15 goods: GARP violations", str(len(v)))

    # the EITC's first kink: the bunching window
    n = rng.uniform(4000, 14000, 40000)
    for e in (0.25, 1.0):
        z = cs.earnings_choice(n, e)
        share = np.mean(np.abs(z - 8580) < 5)
        window = (8580 - 8580 / 1.34 ** e) / 10000
        lab.row(f"EITC kink, elasticity {e:g}: share at the kink (window)", f"{100 * share:.1f}% ({100 * window:.1f}%)")
        assert abs(share - window) < 0.01

    # the ferry: the value of time and its interval's coverage
    f = T["ferry"]
    hits, ests = 0, []
    for k in range(200):
        r = np.random.default_rng(10_000 + k + seed)
        saves = r.choice(np.array(f["saves"], float), f["trips"])
        extra = r.uniform(0, f["max_extra"], f["trips"])
        vv = f["scale"] * (f["value_of_time"] / 60 * saves - extra)
        fast = (r.random(f["trips"]) < 1 / (1 + np.exp(-vv))).astype(float)
        Xd = np.column_stack([saves, extra])
        fit = cs.logit_fit(Xd, fast)
        a, bb = fit["b"]
        p = 1 / (1 + np.exp(-Xd @ fit["b"]))
        cov = np.linalg.inv((Xd * (p * (1 - p))[:, None]).T @ Xd)
        g = np.array([-1 / bb, a / bb ** 2]) * 60
        vot, se = -a / bb * 60, np.sqrt(g @ cov @ g)
        ests.append(vot)
        hits += abs(vot - f["value_of_time"]) <= 1.96 * se
    lab.row("value of time, 200 surveys: mean, 95% coverage", f"${np.mean(ests):.2f} an hour, {100 * hits / 200:.0f}%")
    assert abs(np.mean(ests) - f["value_of_time"]) < 0.3 and 0.9 < hits / 200 < 0.99
    lab.note = ("Demand found by the tangency matches a search; consistent choosers are rationalized by Afriat's "
                "programme exactly when they pass GARP; the test's power grows with the number of budgets; America's "
                "aggregate spending passes; the share at a kink matches the bunching window; and a logit recovers the "
                "value of time with honest intervals.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ns = [5, 11, 25, 50]
    ax[0].plot(ns, [100 * powers[k] for k in ns], "o-", color=labs.ORANGE, lw=2.2, label="random budgets")
    ax[0].axhline(100 * b11, color="#7BD88F", ls="--", label="the eleven Play-it lines")
    ax[0].set(title="Power against random choice", xlabel="number of budgets", ylabel="% of random choosers caught")
    ax[0].legend()
    ax[1].hist(ests, bins=25, color=labs.BLUE, alpha=0.85)
    ax[1].axvline(f["value_of_time"], color="#7BD88F", lw=2, label="planted $15")
    ax[1].set(title="The value of time, 200 ferry surveys", xlabel="$ an hour", ylabel="surveys")
    ax[1].legend()
    lab.fig = fig
    return lab
