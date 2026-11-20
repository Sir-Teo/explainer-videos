"""Lab 32: the treasury: the arithmetic of debt and the surplus that holds it steady, the spending multiplier in the
New Keynesian model with and without the zero bound, Ramey and Zubairy's local projections on US data since 1889, the
regional multiplier and its missing intercept, Reinhart and Rogoff's 90% line recounted, tax smoothing through a war,
Sargent and Wallace's unpleasant arithmetic, and sovereign default by value function iteration."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import fiscal
from explainer.economics.island import truths

TITLE = "The treasury: debt, multipliers and default"
GOAL = ("Find the primary surplus that holds debt steady for any r - g; compute the spending multiplier with the "
        "central bank leaning against it and at the zero bound; estimate multipliers on a century of US data by "
        "local projections; see why regional estimates miss the national multiplier; recount the 90% debt "
        "threshold; smooth taxes through a war; and solve a model in which a government chooses to default.")
TASKS = [
    "The zero bound: raise the persistence of spending from 0.5 to 0.7 and then 0.75. What happens to the multiplier, "
    "and why does the model stop having an answer?",
    "Local projections: change the slack threshold from 6.5% unemployment to 8%. Do the two states' multipliers move "
    "apart?",
    "Default: halve the output cost of default (ycost from 0.969 to 0.985). How do the default rate and the debt the "
    "country carries change?",
]

BINS = ((0, 30), (30, 60), (60, 90), (90, 1e9))


def run(seed=0):
    lab = labs.Lab()
    T = truths(32)

    B = T["budget"]
    for rg in (0.02, 0.0, -0.02):
        r = B["g"] + rg
        path = fiscal.debt_path(B["debt"], r, B["g"], -B["deficit"], B["years"])
        s = fiscal.stabilizing_surplus(B["debt"], r, B["g"])
        held = fiscal.debt_path(B["debt"], r, B["g"], s, B["years"])
        assert abs(held[-1] - B["debt"]) < 1e-9, "the stabilizing surplus must hold debt exactly steady"
        lab.row(f"r - g = {100 * rg:+.0f} points: debt after {B['years']} years with a 2% deficit; the stabilizing "
                f"surplus", f"{100 * path[-1]:.0f}% of output; {100 * s:+.2f}%")

    N = T["nk"]
    for rho in N["rhos"]:
        a = fiscal.nk_multiplier(rho, gamma=N["gamma"], gy=N["gy"])
        z = fiscal.nk_multiplier(rho, zlb=True, gamma=N["gamma"], gy=N["gy"])
        lab.row(f"the multiplier with spending persistence {rho:.1f}: Taylor's rule; the zero bound",
                f"{a['multiplier']:.2f}; " + (f"{z['multiplier']:.2f}" if z["bounded"] else "no bounded answer"))
    a5 = fiscal.nk_multiplier(0.5, gamma=N["gamma"], gy=N["gy"])["multiplier"]
    z5 = fiscal.nk_multiplier(0.5, zlb=True, gamma=N["gamma"], gy=N["gy"])["multiplier"]
    assert a5 < 1 < z5, "leaning against spending cuts the multiplier below one; the zero bound lifts it above"
    assert not fiscal.nk_multiplier(0.8, zlb=True, gamma=N["gamma"], gy=N["gy"])["bounded"]

    S = fiscal.rz_series(data.ramey_zubairy())
    news = fiscal.lp_multiplier(S, "news")
    bp = fiscal.lp_multiplier(S, "bp")
    slack = fiscal.lp_multiplier(S, "news", state="slack")
    lab.row("Ramey and Zubairy, 1889-2015: cumulative multiplier after 2 and 4 years, military news",
            f"{news['multiplier'][8]:.2f}, {news['multiplier'][16]:.2f}")
    lab.row("the same with Blanchard and Perotti's timing", f"{bp['multiplier'][8]:.2f}, {bp['multiplier'][16]:.2f}")
    lab.row("military news after 2 years: slack (unemployment of 6.5% or more), normal times",
            f"{slack['high'][8]:.2f}, {slack['low'][8]:.2f}")
    assert 0.3 < news["multiplier"][8] < 1.2 and 0.1 < bp["multiplier"][8] < 1.2

    G = fiscal.regions(**{**T["regions"], "seed": T["regions"]["seed"] + seed})
    lab.row("the currency union: year fixed effects; the national time series (truth 1.5 and 0.6)",
            f"{G['b_fe']:.2f}; {G['b_nat']:.2f}")
    assert abs(G["b_fe"] - G["m_local"]) < 0.3

    R = data.rr_hap()
    c, y = np.array(R["country"]), np.array(R["year"], int)
    d, g = np.array(R["debtgdp"], float), np.array(R["growth"], float)
    ok = np.isfinite(d) & np.isfinite(g) & ~((c == "Italy") & (y < 1951))
    pooled = [float(g[ok & (d > lo) & (d <= hi)].mean()) for lo, hi in BINS]
    lab.row("growth by public-debt band, every country-year counted once (0-30, 30-60, 60-90, above 90%)",
            ", ".join(f"{v:.1f}%" for v in pooled))
    assert pooled[3] > 1.0, "counted once, growth above the 90% line is not negative"

    W = T["war"]
    path = [W["normal"]] * W["before"] + [W["war"]] * W["length"] + [W["normal"]] * W["after"]
    X = fiscal.tax_smoothing(path, r=W["r"])
    assert abs(X["debt"][-1]) < 1e-9 and X["ratio"] > 1
    lab.row("tax smoothing through the war: the smooth rate; the peak debt; balanced-budget loss over smooth",
            f"{100 * X['tau_smooth']:.1f}%; {100 * max(X['debt']):.0f}% of output; {X['ratio']:.2f}")

    U = T["unpleasant"]
    P = fiscal.unpleasant(T_tight=U["T_tight"], years=U["years"], deficit=U["deficit"], b0=U["b0"], r=U["r"],
                          g=U["g"], base=U["base"], mu_tight=U["mu_tight"])
    assert P["mu_after_tight"] > P["mu_loose"], "tight money now means looser money later"
    lab.row("unpleasant arithmetic: money growth for good, loose from the start against tight for 12 years",
            f"{100 * P['mu_loose']:.1f}% against {100 * P['mu_after_tight']:.1f}%")
    F = T["ftpl"]
    lab.row("the fiscal theory: the price level with surpluses of 2 and of 1.5",
            f"{fiscal.ftpl_price_level(F['B'], F['surplus'], F['r']):.2f}, "
            f"{fiscal.ftpl_price_level(F['B'], F['surplus_low'], F['r']):.2f}")

    M = fiscal.arellano(nb=120)
    Sim = fiscal.arellano_simulate(M, T=8000, seed=seed)
    q = np.array(M["q"])
    lab.row("Arellano's model: iterations; defaults a year; the mean spread; mean debt (quarterly output)",
            f"{M['iterations']}; {100 * Sim['default_rate_annual']:.1f}%; {100 * Sim['mean_spread']:.1f} points; "
            f"{100 * Sim['mean_debt']:.0f}%")
    assert np.all(np.diff(q[len(q) // 2]) >= -1e-9), "more debt never sells at a higher price"
    assert 0 < Sim["default_rate_annual"] < 0.1

    lab.note = ("Debt grows at r - g on its own; the primary surplus is the one dial a treasury holds. In the model, "
                "a central bank that leans against spending holds the multiplier below one and the zero bound lifts "
                "it above, the more so the longer the spending lasts; a century of US data gives numbers between "
                "about 0.6 and 0.8, with little sign of a larger one in slack. Regions measure the relative "
                "multiplier, not the national one. Smoothing taxes through a war leaves the debt behind, which "
                "growth and inflation shrink. A tight central bank facing a deficit that will not move only delays "
                "the money it must print, and a government that may choose not to repay pays a spread for it.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    C = fiscal.nk_multiplier_curve(np.linspace(0.0, 0.72, 73), gamma=N["gamma"], gy=N["gy"])
    ax[0].plot(C["rho"], C["normal"], color=labs.BLUE, label="Taylor's rule")
    ax[0].plot(C["rho"], C["zlb"], color=labs.ORANGE, label="the zero bound")
    ax[0].axhline(1, color="grey", lw=0.8, ls="--")
    ax[0].set(title="The spending multiplier in the model", xlabel="persistence of spending", ylabel="dY/dG")
    ax[0].legend()
    ax[1].plot(news["h"], news["multiplier"], color=labs.BLUE, label="military news")
    ax[1].plot(bp["h"], bp["multiplier"], color=labs.ORANGE, label="Blanchard-Perotti")
    ax[1].axhline(1, color="grey", lw=0.8, ls="--")
    ax[1].set(title="US cumulative multipliers, 1889-2015", xlabel="quarters", ylabel="dY/dG")
    ax[1].legend()
    lab.fig = fig
    return lab
