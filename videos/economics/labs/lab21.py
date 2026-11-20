"""Lab 21: ideas and institutions: the price of light, Romer's balanced path and its scale effect, Aghion and Howitt's
research across step sizes, semi-endogenous growth, Hsieh and Klenow's misallocation on simulated plants, and settler
mortality as an instrument on Acemoglu, Johnson and Robinson's data."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import econometrician as em
from explainer.economics.agora import ge
from explainer.economics.agora import ideas as idx
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Growth II: ideas, ladders, misallocation and institutions"
GOAL = ("Measure the fall in the price of light; solve Romer's economy and see its scale effect; find where creative "
        "destruction brings too much research and where too little; watch idea growth settle in a semi-endogenous "
        "economy; measure misallocation on simulated plants; and estimate the effect of institutions on income with "
        "settler mortality as an instrument.")
TASKS = [
    "Romer: raise theta from 1 to 2. Why does growth fall, and what happens to the research share?",
    "Misallocation: make the wedges correlated with productivity (more productive plants taxed more). Is the loss "
    "larger or smaller than with independent wedges of the same spread?",
    "Settler mortality: add latitude as a control in both stages. What happens to the 2SLS estimate and the "
    "first-stage F?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(21)

    rows = tables.NORDHAUS_LIGHT.data["rows"]
    tallow = next(r[4] for r in rows if r[0] == "candle" and r[1] == "tallow" and r[2] == 1800)
    cfl = next(r[4] for r in rows if r[1] == "compact fluorescent")
    lab.row("hours of work per 1,000 lumen-hours: 1800 tallow candle; 1992 compact fluorescent; ratio",
            f"{tallow}; {cfl}; {tallow / cfl:,.0f}")

    r = T["romer"]
    kw = {k: r[k] for k in ("delta", "alpha", "rho", "theta")}
    b = idx.romer_bgp(L=r["L"], **kw)
    assert abs(b["g"] - kw["delta"] * b["L_A"]) < 1e-12
    lab.row("Romer: growth, research share, interest rate", f"{100 * b['g']:.2f}%, {100 * b['share_research']:.0f}%, "
            f"{100 * b['r']:.2f}%")
    lab.row("Romer: growth with twice the labour force", f"{100 * idx.romer_bgp(L=2 * r['L'], **kw)['g']:.2f}%")

    a = T["ah"]
    akw = {k: a[k] for k in ("lam", "alpha", "rho", "L")}
    for g in (1.2, 1.5, 2.5):
        x = idx.ah_research(gamma=g, **akw)
        lab.row(f"Aghion-Howitt, step {g}: market n, planner n*", f"{x['n_dec']:.3f}, {x['n_star']:.3f}"
                f"{'  (too much)' if x['too_much'] else ''}")

    s = T["semi"]
    se = idx.semi_endogenous(lam=s["lam"], phi=s["phi"], n=s["n"], theta=s["theta"], years=s["years"])
    lab.row("semi-endogenous: idea growth after 200 years; long-run lam n / (1 - phi)",
            f"{100 * se['gA'][-1]:.2f}%; {100 * se['long_run']:.2f}%")

    p = T["plants"]
    rng = np.random.default_rng(p["seed"] + seed)
    logA = rng.normal(0, p["sd_logA"], p["n"])
    for sd in p["sd_wedge"]:
        m = ge.misallocation(logA, rng.normal(0, sd, p["n"]), sigma=p["sigma"])
        lab.row(f"misallocation, wedge sd {sd}: output lost (direct; lognormal formula)",
                f"{100 * m['gain']:.0f}%; {100 * m['lognormal']:.0f}%")

    d = data.ajr()
    y, x_, z = np.array(d["GDP"]), np.array(d["Exprop"]), np.array(d["logMort"])
    iv = em.iv(y, x_, z)
    lab.row("AJR (64 countries): OLS; first stage; 2SLS (s.e.); first-stage F",
            f"{np.polyfit(x_, y, 1)[0]:.2f}; {np.polyfit(z, x_, 1)[0]:.2f}; {iv['estimate']:.2f} ({iv['se']:.2f}); "
            f"{iv['F']:.1f}")

    lab.note = ("Light became about 45,000 times cheaper in labour between 1800 and 1992. Romer's economy grows "
                "faster the bigger it is; creative destruction brings too much research when steps are small and too "
                "little when they are large; with ideas getting harder to find, growth settles at a rate set by the "
                "growth of researchers. Wedges that scatter revenue productivity cost output in proportion to their "
                "variance. Settler mortality, as an instrument, gives a larger effect of institutions than OLS.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    gs = np.exp(np.linspace(np.log(1.005), np.log(3), 120))
    ax[0].plot(gs, [idx.ah_research(gamma=g, **akw)["n_dec"] for g in gs], color=labs.BLUE, label="market")
    ax[0].plot(gs, [idx.ah_research(gamma=g, **akw)["n_star"] for g in gs], color=labs.ORANGE, label="planner")
    ax[0].set(title="Research on the quality ladder", xlabel="step size gamma", ylabel="research share", xscale="log")
    ax[0].legend()
    ax[1].scatter(z, x_, s=12, color=labs.BLUE)
    ax[1].set(title="Settler mortality and institutions", xlabel="log settler mortality",
              ylabel="protection against expropriation")
    lab.fig = fig
    return lab
