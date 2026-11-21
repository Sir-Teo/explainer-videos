"""Lab 52: many agents: Gorman's transfer, Aiyagari's equilibrium and its supply curve, Huggett's bond market, the
wealth shares by model, a small Krusell and Smith, sequence-space Jacobians against brute force, a rate cut split by
fifth of wealth, multipliers, and Hopenhayn's industry at two entry costs."""

import time

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import hetero as H
from explainer.economics.island import truths

TITLE = "Many agents"
GOAL = ("Solve economies with a whole distribution of households (and of firms), check the answers two ways, and see "
        "which aggregate questions the distribution changes.")
TASKS = [
    "Raise the spread of wages from 0.4 to 0.6 in Aiyagari's economy. What happens to the interest rate and to "
    "capital?",
    "Give the HANK households eight quarters of liquid wealth instead of two. How do the direct share of a rate cut "
    "and the deficit-financed multiplier change?",
    "Triple Hopenhayn's entry cost. What happens to the price, to entry and to average productivity?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(52)
    A = T["aiyagari"]

    g = H.gorman_demand([20, 60, 120], [4, 6, 8], [0.9, 0.6, 0.3], 20.0, 2, 0)
    lab.row("Gorman: a transfer of 20 with slopes 0.9, 0.6, 0.3 changes spending by", f"{g['change']:.1f}")

    kw = dict(beta=A["beta"], gamma=A["gamma"], rho=A["rho"], sigma=A["sd"] * np.sqrt(1 - A["rho"] ** 2),
              n_e=A["n_e"], n_a=200, a_max=A["a_max"])
    t0 = time.perf_counter()
    res = H.aiyagari(**kw)
    lab.row("Aiyagari: r, rate of time preference, seconds",
            f"{100 * res['r']:.2f}%, {100 * res['rho_time']:.2f}%, {time.perf_counter() - t0:.1f}")
    assert 0 < res["r"] < res["rho_time"]
    lab.row("Aiyagari: capital against one household's",
            f"{res['K']:.2f} against {H.capital_demand(res['rho_time']):.2f}")
    lab.row("Aiyagari: Gini, top 1%, at the limit",
            f"{res['gini']:.3f}, {100 * res['top1']:.1f}%, {100 * res['at_limit']:.1f}%")
    sim = H.simulate(res, n=20000, T=300, seed=seed)
    lab.row("simulated Gini (20,000 households)", f"{H.gini(sim['wealth'], np.ones(len(sim['wealth']))):.3f}")
    curve = H.capital_supply(np.linspace(0.0, res["rho_time"] - 0.003, 8), **kw)

    hg = H.huggett_ct(**T["huggett"])
    lab.row("Huggett: the rate that clears the bond market (rho = 5%)", f"{100 * hg['r']:.2f}%")

    ks = H.krusell_smith(n_a=60, T=500, burn=60, max_rounds=40, tol=1e-5, inner_tol=1e-6)
    lab.row("Krusell and Smith (small): R-squared, Den Haan's largest error",
            f"{min(ks['r2']):.6f}, {ks['dh_max']:.2f}%")

    ss = H.hank_steady_state(2.0, n_a=200)
    t0 = time.perf_counter()
    jac = H.jacobians(ss, T=150)
    fake = time.perf_counter() - t0
    t0 = time.perf_counter()
    b = H.jacobian_column_brute(ss, "Z", 5, T=150)
    one = time.perf_counter() - t0
    err = float(np.max(np.abs(b["C"] - jac["J"][("C", "Z")][:, 5])))
    lab.row("fake news: all columns, seconds; brute force, one column", f"{fake:.2f}; {one:.2f}")
    lab.row("fake news against brute force: largest difference", f"{err:.1e}")
    assert err < 1e-3
    rc = H.hank_rate_cut(ss, jac)
    ra = H.ra_rate_cut(ss["r"], ss["B"], rc["dr"])
    lab.row("rate cut: direct share on impact, with many households and with one",
            f"{100 * rc['direct_share_impact']:.0f}%, {100 * ra['direct_share_impact']:.0f}%")
    tot = H.response(ss, rc["dr"], rc["dZ"])
    groups = H.by_wealth_group(ss, tot)
    lab.row("rate cut: rise in spending by fifth, poorest first",
            ", ".join(f"{x['pct']:.2f}%" for x in groups))
    for f in ("balanced", "deficit"):
        mult = H.hank_multiplier(ss, jac, financing=f)["multiplier"]
        lab.row(f"multiplier, {f}", f"{mult:.3f}")
        assert mult >= 1.0 - 1e-8

    F = T["hopenhayn"]
    for ce in F["c_e"]:
        h = H.hopenhayn(c_e=ce, c_f=F["c_f"], entrant_shift=F["entrant_shift"])
        lab.row(f"Hopenhayn, entry cost {ce:.0f}: price, entry rate, average productivity",
                f"{h['p']:.2f}, {100 * h['entry_rate']:.1f}%, {h['productivity']:.3f}")

    lab.note = ("Uninsured risk lowers the interest rate and raises capital; a simulated population agrees with the "
                "histogram; the mean is nearly enough to forecast capital; fake-news Jacobians match brute force at a "
                "fraction of the cost; with little liquid wealth most of a rate cut works through incomes and a "
                "deficit-financed multiplier exceeds one; entry barriers protect the unproductive.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot([c["supply"] for c in curve], [100 * c["r"] for c in curve], color=labs.BLUE, label="households")
    ax[0].plot([c["demand"] for c in curve], [100 * c["r"] for c in curve], color=labs.ORANGE, label="firms")
    ax[0].set(title="Aiyagari: the market for capital", xlabel="capital", ylabel="interest rate, %")
    ax[0].legend()
    q = np.arange(16)
    ax[1].plot(q, 100 * rc["dC"][:16], color="black", label="total")
    ax[1].plot(q, 100 * rc["direct"][:16], color=labs.BLUE, label="direct")
    ax[1].plot(q, 100 * rc["indirect"][:16], color=labs.ORANGE, label="indirect")
    ax[1].set(title="a rate cut, % of output", xlabel="quarter")
    ax[1].legend()
    lab.fig = fig
    return lab
