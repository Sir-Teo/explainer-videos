"""Lab 51: computing economies: value and policy iteration on the growth model, grids and their steady states, the
endogenous grid method against value iteration, collocation by degree, perturbation, the zero bound by guess and
verify, and Smolyak's sparse grids."""

import time

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import solve as S
from explainer.economics.island import truths

TITLE = "Computing economies"
GOAL = ("Solve the growth model and a household with a borrowing limit several ways, measure each answer with "
        "Euler-equation errors, and see which methods are fast, which are accurate, and why.")
TASKS = [
    "Raise beta to 0.99. How many more rounds does value iteration need, and how many does policy iteration?",
    "Give the household no income risk (sigma = 0.0001). How much more does it consume at assets of 2?",
    "Find the smallest collocation degree whose worst Euler error is below 10^-6.",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(51)
    m = S.growth(**T["growth"])

    g = S.kgrid(m, 300)
    v = S.vfi(m, g, tol=1e-6)
    h = S.howard(m, g)
    lab.row("value iteration: rounds, seconds", f"{v['iters']}, {v['seconds']:.3f}")
    lab.row("policy iteration: rounds, seconds", f"{h['iters']}, {h['seconds']:.3f}")
    assert np.array_equal(v["j"], h["j"])
    cp = S.contraction_path(m, g, 60)
    lab.row("contraction ratio after 60 rounds (beta)", f"{cp['ratio'][-1]:.4f} ({m['beta']})")

    for n in T["grids"]:
        gg = S.kgrid(m, n)
        r = S.vfi(m, gg, tol=1e-8)
        steady = gg[np.argmin(np.abs(r["kprime"] - gg))] / m["kss"]
        ee = S.euler_errors(m, lambda k, gg=gg, r=r: S.resources(k, m) - np.interp(k, gg, r["kprime"]))["max"]
        lab.row(f"grid of {n}: steady state / true, worst Euler error", f"{steady:.4f}, 10^{ee:.2f}")

    hh = S.household(**T["household"])
    e = S.egm(hh)
    vh = S.household_vfi(hh)
    lab.row("household: endogenous grid (seconds, worst error)",
            f"{e['seconds']:.3f}, 10^{S.household_euler_errors(hh, e['c'])['max']:.2f}")
    lab.row("household: value iteration on the same grid",
            f"{vh['seconds']:.3f}, 10^{S.household_euler_errors(hh, vh['c'])['max']:.2f}")

    degs, errs = [], []
    for n in range(2, 12):
        c = S.collocation(m, n)
        degs.append(n - 1)
        errs.append(S.euler_errors(m, c["c"])["max"])
    lab.row("collocation: worst Euler error by degree 1..10", ", ".join(f"{x:.1f}" for x in errs))
    assert errs[-1] < errs[0] - 4

    t0 = time.perf_counter()
    p1, p2 = S.perturbation(m, 1), S.perturbation(m, 2)
    lab.row("perturbation: g1, g2 (seconds)", f"{p1['g1']:.4f}, {p2['g2']:.5f} ({time.perf_counter() - t0:.4f})")

    z = S.zlb_occbin(**T["zlb"])
    lab.row("zero bound: quarters at zero, guesses; output gap with and without the bound",
            f"{z['bound_quarters']}, {z['iters']}; {z['x'][0]:.2f}%, {z['x_free'][0]:.2f}%")

    lab.row("Smolyak level 2 against 5^d points, d = 2, 5, 10, 20",
            ", ".join(f"{S.smolyak_count(d, 2)} / {S.tensor_count(d, 2):.0e}" for d in (2, 5, 10, 20)))

    lab.note = ("Value iteration converges at the rate beta, and policy iteration in a handful of rounds; coarse "
                "grids bias the steady state; the endogenous grid method avoids root finding and beats value "
                "iteration on both time and accuracy; collocation's error falls geometrically with the degree; "
                "perturbation is exact at the steady state; the zero bound deepens the recession; sparse grids grow "
                "polynomially with the dimension.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].semilogy(np.arange(1, len(v["dist"]) + 1), v["dist"], color=labs.BLUE, label="value iteration")
    ax[0].set(title="change from the round before", xlabel="round")
    ax[0].legend()
    ax[1].plot(degs, errs, marker="o", color=labs.ORANGE)
    ax[1].set(title="collocation: worst Euler error (log10)", xlabel="degree")
    lab.fig = fig
    return lab
