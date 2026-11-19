"""Lab 19: the great escape: the Malthusian economy with a plague and an invention, England's labour demand curve,
the Black Death in England's data, growth rates over seven centuries, Engels's pause, the demographic transition,
Galor and Weil's education threshold, a toy unified growth economy, and spatial noise in persistence regressions."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import malthus as ml
from explainer.economics.island import truths

TITLE = "The great escape: Malthus, the Black Death and unified growth"
GOAL = ("Run a Malthusian economy and watch technology turn into people; fit England's labour demand curve and see it "
        "break after 1600; measure the Black Death and the slow growth of the Industrial Revolution; find the "
        "threshold at which parents start to educate; run a unified growth economy through three eras; and see how "
        "spatial correlation fakes significance.")
TASKS = [
    "The island: give it steady technological progress of 1% a year and no cap on population growth. Where does "
    "income per head settle, and why is it above subsistence but no longer rising? (Hint: ln y* = g / (lambda beta).)",
    "England's curve: fit 1270-1500 and 1500-1640 separately. Is the slope the same before and after the Black Death "
    "settles?",
    "Unified growth: double phi. How much earlier does the take-off come, and does the fertility peak move as much?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(19)

    t = T["malthus"]
    s = ml.simulate(t["years"], beta=t["beta"], lam=t["lam"], plague=t["plague"], invention=t["invention"])
    jump = s["y"][t["plague"][0]] / s["y"][t["plague"][0] - 1]
    assert abs(jump - (1 - t["plague"][1]) ** -t["beta"]) < 1e-9          # income jumps by the survivors' share
    lab.row("island: income jump after the plague; after the plough; people at the new steady state",
            f"x{jump:.3f}; x{s['y'][t['invention'][0]] / s['y'][t['invention'][0] - 1]:.3f}; {s['L_star']:.3f}")
    lab.row("island: half-life of a shock, ln 2 / (lambda beta)", f"{np.log(2) / (t['lam'] * t['beta']):.1f} years")

    m = data.millennium()
    e = T["elasticity"]
    before = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], *e["before"])
    after = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], *e["after"])
    assert before["slope"] < 0 < after["slope"]                            # Malthusian, then not
    lab.row("England 1270-1640: slope, HC1 s.e., Newey-West s.e., R2",
            f"{before['slope']:.3f}, {before['se_hc1']:.3f}, {before['se_nw']:.3f}, {before['r2']:.2f}")
    lab.row("England 1600-1800: slope", f"{after['slope']:+.3f}")

    i = {y: k for k, y in enumerate(m["year"])}
    lab.row("Black Death: population 1348 -> 1351 (thousands); real wage 1348 -> 1450",
            f"{m['population'][i[1348]]:,.0f} -> {m['population'][i[1351]]:,.0f}; "
            f"{m['real_wage'][i[1348]]:.1f} -> {m['real_wage'][i[1450]]:.1f}")
    for a, b in ((1270, 1650), (1650, 1800), (1800, 2016)):
        g = ml.cagr(m["gdppc"][i[a]], m["gdppc"][i[b]], b - a)
        lab.row(f"England's GDP per head growth {a}-{b}; doubling time", f"{100 * g:.2f}% a year; "
                f"{np.log(2) / np.log(1 + g):.0f} years")
    gp = ml.cagr(m["gdppc"][i[1780]], m["gdppc"][i[1840]], 60)
    gw = ml.cagr(m["real_wage"][i[1780]], m["real_wage"][i[1840]], 60)
    lab.row("Engels's pause, 1780-1840: output per head, real wages", f"{100 * gp:.2f}%, {100 * gw:.2f}% a year")

    se = data.longrun("children-born-per-woman", "Sweden")
    f = dict(zip(se["year"], se["value"]))
    lab.row("Sweden's fertility, 1891 and 1935", f"{f[1891]:.2f}, {f[1935]:.2f}")

    th = ml.threshold()
    assert abs(th - 0.5 ** 2 * 0.15 / 0.5) < 1e-3                         # rho^2 tau / (1 - rho)
    lab.row("education threshold (numerical; closed form rho^2 tau / (1 - rho))", f"{th:.4f}; {0.075:.4f}")

    u = ml.unified(**{"phi": T["unified"]["phi"], "generations": T["unified"]["generations"]})
    lab.row("unified economy: take-off year; fertility peak year and level",
            f"{u['takeoff_year']}; {u['peak_year']}, {u['peak_n']:.3f}")

    nz = ml.spatial_noise(n_sites=200, reps=200, seed=2019 + seed)
    lab.row("spatial noise: share 'significant' with no pattern; with smooth patterns",
            f"{nz['independent']['reject']:.2f}; {nz['smooth']['reject']:.2f}")

    lab.note = ("Technology buys people, not income: the island's income always returns to subsistence. England obeyed "
                "until about 1640, with wages falling about 0.9% for each 1% more people; the Black Death nearly "
                "tripled wages, and the population's recovery undid it. Growth reached 1% a year only after 1830, wages "
                "lagged output until 1840, and fertility fell once education paid. Unrelated smooth maps look related "
                "half the time.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    yr = np.array(m["year"])
    k = (yr >= 1270) & (yr <= 1860)
    ax[0].scatter(np.log(np.array(m["population"])[k]), np.log(np.array(m["real_wage"])[k]), s=4,
                  c=yr[k], cmap="viridis")
    ax[0].set(title="England, 1270-1860", xlabel="log population", ylabel="log real wage")
    rows = u["rows"]
    ax[1].plot([r["year"] for r in rows], [r["y"] for r in rows], color=labs.BLUE, label="income per head")
    ax[1].plot([r["year"] for r in rows], [r["n"] for r in rows], color=labs.ORANGE, label="children per adult")
    ax[1].set(title="A unified growth economy", xlabel="year")
    ax[1].legend()
    lab.fig = fig
    return lab
