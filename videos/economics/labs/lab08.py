"""Lab 8: technology, costs, supply, the industry, survival, and the boundary of the firm."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import firm as fm
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "The firm: technology, costs, supply and boundaries"
GOAL = ("Refit Cobb and Douglas's 1928 regression on their data and watch it break; find the boatyard's least-cost "
        "inputs and check Shephard's lemma; derive short-run cost curves, the shut-down and break-even prices and "
        "supply; check Hotelling's lemma and Le Chatelier's principle; find a free-entry equilibrium with identical "
        "and with different firms; run Alchian's survival of rule-of-thumb firms; and compute the investment lost "
        "to hold-up and the best owner in Grossman-Hart-Moore.")
TASKS = [
    "Cobb and Douglas: drop the years 1921-22 and refit with constant returns imposed. How much does capital's "
    "exponent move, and what does that say about a regression on 24 trending observations?",
    "The industry: raise demand to Q = 600 - 0.2p. How many identical yards are there in the long run, and what "
    "happens to the price? Then do it with heterogeneous fixed costs: who gains?",
    "Survival: make demand more elastic (-5 instead of -3). What is the new optimal markup, and how fast does "
    "selection find it? What happens if newcomers copy at random instead of in proportion to profit?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(8)

    # Cobb and Douglas, refitted
    d = tables.COBB_DOUGLAS_1928.data
    Y, L, K = (np.array(d[k], float) for k in ("output", "labour", "capital"))
    crs = fm.fit_cobb_douglas(Y, K, L, "crs")
    un = fm.fit_cobb_douglas(Y, K, L, "unrestricted")
    tr = fm.fit_cobb_douglas(Y, K, L, "trend", years=list(d["years"]))
    lab.row("Cobb-Douglas with constant returns: labour, capital, A", f"{crs['labour']:.3f}, {crs['capital']:.3f}, "
                                                                     f"{np.exp(crs['const']):.3f}")
    lab.row("unrestricted: labour, capital", f"{un['labour']:.3f}, {un['capital']:.3f}")
    lab.row("with a time trend: labour, capital, trend", f"{tr['labour']:.3f}, {tr['capital']:+.3f}, {tr['trend']:.4f}")
    assert tr["capital"] < 0 < crs["capital"]

    # the yard: least cost and Shephard
    y = T["yard"]
    yard = fm.CobbDouglas(y["A"], y["a"], y["b"])
    Kc, Lc = yard.demand(y["wage"], y["rent"], 8.0)
    errs = fm.shephard_errors(yard, y["wage"], y["rent"], 8.0)
    lab.row("8 boats at least cost: slipways, shipwrights, cost", f"{Kc:.2f}, {Lc:.2f}, ${yard.cost(y['wage'], y['rent'], 8.0):,.2f}")
    assert max(errs.values()) < 1e-6
    assert abs(yard.trs(Kc, Lc) - y["wage"] / y["rent"]) < 1e-6

    # short-run curves, the boatyard game
    sr = fm.ShortRun(yard, y["slipways"], y["wage"], y["rent"])
    qs = np.linspace(0.5, 16, 2000)
    q_min = qs[np.argmin(sr.atc(qs))]
    assert abs(sr.mc(q_min) - sr.atc(q_min)) / sr.atc(q_min) < 0.01
    h = fm.hire(y["price"], y["wage"], yard, y["slipways"])
    lab.row("short run, 4 slipways: bottom of average cost; shipwrights hired at $1,200 a boat",
            f"{q_min:.2f} boats at ${float(sr.atc(q_min)):,.0f}; {h['hired']}")

    # supply, Hotelling, Le Chatelier
    hot = fm.hotelling_errors(yard, y["price"], y["wage"], y["rent"])
    lc = fm.le_chatelier(yard)
    lab.row("supply elasticities, short run / long run; Hotelling error", f"{lc['short']:.1f} / {lc['long']:.1f}; "
                                                                          f"{max(hot.values()):.1e}")
    assert lc["long"] > lc["short"] and max(hot.values()) < 1e-6

    # the industry
    ind = T["industry"]
    u = fm.UCost(ind["F"], ind["c"], ind["d"])
    same = fm.industry(*ind["demand"], ind["F"], ind["c"], ind["d"])
    het = fm.industry(*ind["demand"], None, ind["c"], ind["d"], fixed_costs=np.linspace(*ind["fixed_range"],
                                                                                         ind["entrants"]))
    lab.row("break-even and shut-down prices", f"${u.breakeven:,.2f} and ${u.shutdown:,.2f}")
    lab.row("free entry, identical yards: price, yards", f"${same['price']:,.2f}, {same['firms']:.1f}")
    lab.row("free entry, different yards: price, yards, rents", f"${het['price']:,.2f}, {het['firms']}, "
                                                                f"${het['rents']:,.0f}")
    assert het["rents"] > 0

    # survival
    sel = T["selection"]
    out = fm.selection(sel["yards"], sel["months"], sel["elasticity"], sel["noise"], sel["mutation"],
                       sel["seed"] + seed)
    M = out["markups"]
    lab.row("survival: median markup at the start and after ten years (optimum)",
            f"{np.median(M[0]):.3f}, {np.median(M[-1]):.3f} ({out['best']:.2f})")

    # the boundary of the firm
    hu = fm.hold_up(T["holdup"]["V"], T["holdup"]["theta"])
    g = T["ghm"]
    gh = fm.ghm(g["va"], g["vb"], g["outside"], g["outside"])
    lab.row("hold-up: investment together / apart; surplus lost", f"{hu['first_best']:.0f} / {hu['held_up']:.0f}; "
                                                                  f"{hu['loss']:.0f}")
    lab.row("Grossman-Hart-Moore: the best owner, and its surplus (first best)",
            f"{gh['best']}, {gh[gh['best']]['surplus']:.3f} ({gh['first best']['surplus']:.3f})")
    assert gh["best"] == "A owns"

    lab.note = ("Cobb and Douglas's numbers reproduce their 1928 formula and break with a time trend; at least cost "
                "the rate of substitution equals the price ratio and Shephard's lemma holds; marginal cost cuts "
                "average cost at its bottom; the long run is more elastic than the short; free entry drives the "
                "price to the bottom of average cost, and with different costs leaves rents to the cheapest yards; "
                "survival moves rule-of-thumb markups toward the optimum; hold-up costs a quarter of the surplus "
                "here, and ownership belongs with the party whose investment matters most.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    yrs = np.array(d["years"])
    for v, c, nm in ((K, labs.ORANGE, "capital"), (L, labs.BLUE, "labour"), (Y, "goldenrod", "output")):
        ax[0].semilogy(yrs, v, color=c, lw=2, label=nm)
    ax[0].semilogy(yrs, np.exp(crs["fitted"]) * L, color="grey", lw=1.5, ls="--", label="1.01 L^0.75 K^0.25")
    ax[0].set(title="Cobb and Douglas's data, 1899-1922", xlabel="year", ylabel="index (1899 = 100)")
    ax[0].legend(fontsize=8)
    pct = np.percentile(M, [10, 50, 90], axis=1)
    ax[1].fill_between(np.arange(M.shape[0]), pct[0], pct[2], color=labs.BLUE, alpha=0.2)
    ax[1].plot(pct[1], color=labs.BLUE, lw=2)
    ax[1].axhline(out["best"], color=labs.ORANGE, lw=1.5, ls="--")
    ax[1].set(title="Rule-of-thumb markups under selection", xlabel="month", ylabel="markup over cost")
    lab.fig = fig
    return lab
