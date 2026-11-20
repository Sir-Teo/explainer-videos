"""Lab 40: inequality and mobility: the measures with bootstrap standard errors on the Island, a century of top
shares and the Pareto exponent they imply, random growth's tail from simulation and from the Kolmogorov forward
equation, the speed of transitions with and without high-growth types, the tail of wealth against r - g, Kuznets's
dual economy, the intergenerational elasticity attenuated by one year of income, the Gatsby curve's mechanism, and
Opportunity Insights' rank-rank slope, transition matrix and absolute mobility."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import distribution as D
from explainer.economics.island import truths

TITLE = "Inequality and mobility"
GOAL = ("Measure inequality on a sample with standard errors; read the Pareto exponent off top shares; derive a "
        "Pareto tail from random growth and check it by simulation; see why pure random growth moves too slowly; "
        "attenuate and correct the intergenerational elasticity; and recompute America's mobility from the "
        "published tables.")
TASKS = [
    "Random growth: double the average career length. By how much does the tail exponent fall, and the top 1% "
    "share rise? Check the formula against the simulation.",
    "Attenuation: with five years of parents' income, how large must the transitory spread be for the estimate to "
    "fall below 0.3 when the truth is 0.45?",
    "Ranks: from the transition matrix, compute the chance that a child of the top fifth falls to the bottom fifth. "
    "How does it compare with the chance of the reverse journey?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(40)

    Ts = T["sample"]
    x = D.simulate_growth(Ts["n"], Ts["years"], Ts["nu"], Ts["sigma"], Ts["delta"], seed=Ts["seed"] + seed)
    M = D.measures(x, B=200, seed=seed)
    lab.row("the Island's 2,000 incomes: Gini (s.e.), top 10%, top 1%",
            f"{M['gini']['value']:.3f} ({M['gini']['se']:.3f}), {100 * M['top10']['value']:.1f}%, "
            f"{100 * M['top1']['value']:.1f}%")
    lab.row("Atkinson's index for epsilon 0.5, 1, 2",
            ", ".join(f"{M[k]['value']:.3f}" for k in ("atk05", "atk1", "atk2")))
    assert M["atk05"]["value"] < M["atk1"]["value"] < M["atk2"]["value"]

    S = data.saez()
    k70, k22 = S["year"].index(1970), S["year"].index(2022)
    a70 = D.pareto_alpha(S["top1"][k70], S["top01"][k70], 0.01, 0.001)
    a22 = D.pareto_alpha(S["top1"][k22], S["top01"][k22], 0.01, 0.001)
    lab.row("America's top 1% share 1970, 2022; Pareto exponent from the top 1% and 0.1%",
            f"{S['top1'][k70]:.1f}%, {S['top1'][k22]:.1f}%; {a70:.2f} -> {a22:.2f}")
    assert a22 < a70

    G = T["growth"]
    sim = D.simulate_growth(20000, 300, G["nu"], G["sigma1"], G["delta"], seed=G["seed"] + seed)
    z = D.zeta(G["nu"], G["sigma1"], G["delta"])
    K = D.KFE(G["nu"], G["sigma1"], G["delta"], y_lo=G["floor"])
    p = K.stationary()
    lab.row("random growth: zeta (theory), Hill's estimate from 20,000 careers, top 1% share (KFE, simulation)",
            f"{z:.3f}, {D.hill(sim, 200):.3f}, {100 * K.top_share(p, 0.01):.1f}%, {100 * D.top_share(sim, 0.01):.1f}%")
    assert abs(D.hill(sim, 200) - z) < 0.3

    K0 = D.KFE(G["nu"], G["sigma0"], G["delta"], y_lo=G["floor"])
    pure = K.path(K0.stationary(), 60, dt=0.5)
    Ty = T["types"]
    Ka = D.KFE(Ty["nu_l"], Ty["sigma"], G["delta"], nu_h=Ty["nu_h0"], psi=Ty["psi"], q_h=Ty["q_h"], y_lo=G["floor"])
    Kb = D.KFE(Ty["nu_l"], Ty["sigma"], G["delta"], nu_h=Ty["nu_h1"], psi=Ty["psi"], q_h=Ty["q_h"], y_lo=G["floor"])
    types = Kb.path(Ka.stationary(), 60, dt=0.5)
    hp = D.half_life(pure["t"], np.log(pure[0.01]), np.log(K.top_share(p, 0.01)))
    ht = D.half_life(types["t"], np.log(types[0.01]), np.log(Kb.top_share(Kb.stationary(), 0.01)))
    lab.row("half-life of the top 1% share's move: pure random growth, high-growth types (years)",
            f"{hp:.1f}, {ht:.1f}")
    assert ht < hp

    W = T["wealth"]
    lab.row("wealth's tail exponent at r - g = 0, 2%, 3%",
            ", ".join(f"{D.wealth_zeta(r, W['c'], W['sigma'], W['delta']):.2f}" for r in (0.0, 0.02, 0.03)))

    Kz = T["kuznets"]
    kz = D.kuznets(np.linspace(0, 1, 21), Kz["gap"], Kz["sd_a"], Kz["sd_m"], 20000, Kz["seed"] + seed)
    kk = int(np.argmax(kz["gini"]))
    lab.row("Kuznets: Gini with no one, half and everyone in the modern sector",
            f"{kz['gini'][0]:.3f}, {kz['gini'][kk]:.3f} (at {100 * kz['share'][kk]:.0f}%), {kz['gini'][-1]:.3f}")

    Tg = T["generations"]
    g = D.generations(Tg["n"], Tg["beta"], Tg["sd_perm"], Tg["sd_trans"], Tg["years"], Tg["seed"] + seed)
    b1 = D.ige(g["child"], g["parent_years"][:, 0])[0]
    b15 = D.ige(g["child"], g["parent_years"].mean(axis=1))[0]
    lab.row("the elasticity: one year, fifteen years, the formula's one-year value, planted",
            f"{b1:.3f}, {b15:.3f}, {Tg['beta'] * D.attenuation(1, Tg['sd_perm'], Tg['sd_trans']):.3f}, "
            f"{Tg['beta']:.2f}")
    assert b1 < b15 < Tg["beta"] + 0.05

    Tt = T["gatsby"]
    gb = D.gatsby(Tt["returns"], Tt["lam"], Tt["sd_h"], Tt["sd_u"], 10000, Tt["seed"] + seed)
    lab.row("the Gatsby mechanism: Gini and elasticity at the lowest and highest return to skill",
            f"{gb['gini'][0]:.3f}, {gb['ige'][0]:.3f}; {gb['gini'][-1]:.3f}, {gb['ige'][-1]:.3f}")

    N = data.opportunity("national")
    r = np.array(N["kid_rank"])
    slope = np.polyfit((np.arange(1, 101) - 0.5) / 100, r, 1)[0]
    Q = np.array([[np.mean(N[f"q{j}"][20 * i: 20 * i + 20]) for j in range(1, 6)] for i in range(5)])
    A = data.opportunity("absmob")
    lab.row("rank-rank slope; bottom fifth to top fifth; absolute mobility 1940, 1984",
            f"{slope:.3f}; {100 * Q[0, 4]:.1f}%; {100 * A['mean'][0]:.0f}%, {100 * A['mean'][-1]:.0f}%")
    assert abs(slope - 0.341) < 0.005

    lab.note = ("Every measure watches a different part of the distribution; the top is measured least precisely. "
                "Random growth with turnover gives Pareto's tail, but moves it too slowly unless a few incomes grow "
                "fast. One year of parents' income makes families look more mobile than they are. In America a "
                "child's rank rises about a third of a percentile for each percentile of the parents', and half of "
                "children born in 1984 out-earn their parents.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    gx, gs = D.ccdf(sim, 80)
    ax[0].loglog(gx, gs, ".", color=labs.BLUE, label="simulated")
    ax[0].loglog(gx, gs[0] * (gx / gx[0]) ** (-z), color=labs.ORANGE, label=f"slope -{z:.2f}")
    ax[0].set(title="random growth's tail", xlabel="income (start = 1)", ylabel="share above")
    ax[0].legend()
    ax[1].plot(pure["t"], 100 * np.array(pure[0.01]), color="grey", label="pure random growth")
    ax[1].plot(types["t"], 100 * np.array(types[0.01]), color=labs.ORANGE, label="high-growth types")
    ax[1].set(title="top 1% share after the change", xlabel="years", ylabel="%")
    ax[1].legend()
    lab.fig = fig
    return lab
