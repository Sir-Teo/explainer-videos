"""Lab 34: the open economy: real exchange rates since 1870 and the half-life of deviations from purchasing power
parity, the Big Mac index and Balassa-Samuelson, Fama's regression and the carry trade, Meese and Rogoff's horse race
out of sample, Mundell-Fleming under fixed and floating rates, Dornbusch's overshooting, Krugman's speculative attack,
Obstfeld's self-fulfilling crises, and the pass-through of the dollar into American import prices."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import openecon
from explainer.economics.island import truths

TITLE = "The open economy: parity, the random walk and the trilemma"
GOAL = ("Measure how slowly real exchange rates return to parity over 150 years; test uncovered interest parity "
        "currency by currency and run the carry trade; check that no model beats the random walk out of sample; "
        "solve Mundell-Fleming, Dornbusch and Krugman's attack; and estimate how far the dollar's moves reach "
        "American import prices.")
TASKS = [
    "Half-life: estimate it country by country since 1973 (the 'by_country' output). Which currency returns fastest, "
    "and which slowest?",
    "Carry: hold one currency instead of two (k=1). Is the Sharpe ratio higher, and is the worst month worse?",
    "Pass-through: replace import prices excluding fuel (IREXFUELS) by all import prices (IR). What happens to the "
    "estimate, and why?",
]

USD_PER = {"GB": ("EXUSUK", False), "JP": ("EXJPUS", True), "CA": ("EXCAUS", True), "CH": ("EXSZUS", True),
           "AU": ("EXUSAL", False), "NZ": ("EXUSNZ", False)}


def monthly(key):
    d = data.fred(key)
    return {x[:7]: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def log_usd_per(c):
    if c == "DE":                       # marks per dollar to 1998, then dollars per euro at 1.95583 marks
        de, eu = monthly("EXGEUS"), monthly("EXUSEU")
        return {**{k: -np.log(v) for k, v in de.items() if k < "1999-01"},
                **{k: np.log(v / 1.95583) for k, v in eu.items()}}
    key, inv = USD_PER[c]
    return {k: (-np.log(v) if inv else np.log(v)) for k, v in monthly(key).items()}


def run(seed=0):
    lab = labs.Lab()
    T = truths(34)

    Rr = openecon.real_rates(data.jst())
    full, flt = openecon.ppp_halflife(Rr, 1870, 2020), openecon.ppp_halflife(Rr, 1973, 2020)
    lab.row("PPP: pooled AR(1) and half-life, 1870-2020 and 1973-2020",
            f"{full['rho']:.3f}, {full['halflife']:.1f} years; {flt['rho']:.3f}, {flt['halflife']:.1f} years")
    assert 2 < full["halflife"] < 8 and 1 < flt["halflife"] < full["halflife"]

    B = data.bigmac()
    last = max(B["date"])
    ok = [i for i, d in enumerate(B["date"]) if d == last and np.isfinite(B["GDP_bigmac"][i])
          and np.isfinite(B["USD_raw"][i]) and B["iso_a3"][i] != "USA"]
    bs = openecon.balassa_samuelson(np.log([B["GDP_bigmac"][i] for i in ok]), [B["USD_raw"][i] for i in ok])
    lab.row(f"Balassa-Samuelson in the Big Mac index ({last}): slope on log GDP per head; correlation; countries",
            f"{bs['slope']:.3f}; {bs['corr']:.2f}; {bs['n']}")
    assert bs["slope"] > 0

    i_us = monthly("IR3TIB01USM156N")
    cur = ("GB", "DE", "JP", "CH", "CA", "AU", "NZ")
    ls = {c: log_usd_per(c) for c in cur}
    rates = {c: monthly(f"IR3TIB01{c}M156N") for c in cur}
    betas = {c: openecon.fama(ls[c], i_us, rates[c], h=3) for c in cur}
    lab.row("Fama's slope by currency (uncovered parity says 1), with Newey-West SEs",
            ", ".join(f"{c} {b['beta']:+.2f} ({b['se']:.2f})" for c, b in betas.items()))
    assert sum(b["beta"] < 1 for b in betas.values()) >= 6

    C = openecon.carry(ls, rates, i_us)
    lab.row("the carry trade since 1985: mean a year; s.d.; Sharpe; skewness; worst month",
            f"{100 * C['mean']:.1f}%; {100 * C['sd']:.1f}%; {C['sharpe']:.2f}; {C['skew']:.2f}; "
            f"{C['worst'][0]} {100 * C['worst'][1]:.1f}%")
    assert C["mean"] > 0 and C["skew"] < 0

    eom = {}
    for c, (key, inv) in {"GB": ("DEXUSUK", False), "JP": ("DEXJPUS", True), "CA": ("DEXCAUS", True),
                          "CH": ("DEXSZUS", True)}.items():
        d = data.fred(key)
        last_of = {}
        for x, v in zip(d["date"], d["value"]):
            if np.isfinite(v) and x >= "1980-01":
                last_of[x[:7]] = v
        eom[c] = {k: (-np.log(v) if inv else np.log(v)) for k, v in last_of.items()}
    for h in (1, 12):
        H = openecon.horse_race(eom, {c: rates[c] for c in eom}, i_us, h)
        lab.row(f"Meese-Rogoff at {h} month(s): RMSE relative to the random walk (interest parity; AR(1))",
                f"{H['ratio']['interest parity']:.3f}; {H['ratio']['AR(1)']:.3f} ({H['n']} forecasts)")
        assert 0.95 < H["ratio"]["interest parity"] < 1.05

    mf = {(r, p): openecon.mundell_fleming(r, **{p: 1.0}) for r in ("floating", "fixed") for p in ("dg", "dm")}
    lab.row("Mundell-Fleming, output after a unit rise: fiscal and money, floating; fiscal and money, fixed",
            f"{mf['floating', 'dg']['y']:.1f}, {mf['floating', 'dm']['y']:.1f}; {mf['fixed', 'dg']['y']:.1f}, "
            f"{mf['fixed', 'dm']['y']:.1f}")
    assert mf["floating", "dg"]["y"] == 0 and mf["fixed", "dm"]["y"] == 0

    D = openecon.dornbusch(**T["dornbusch"])
    lab.row("Dornbusch: the currency's jump after 10% more money; the overshooting factor",
            f"{100 * D['jump']:.1f}%; {D['factor']:.2f}")
    assert abs(D["factor"] - (1 + 1 / (D["lam"] * D["theta"]))) < 1e-12

    K = openecon.krugman_attack(**T["krugman"])
    lab.row("Krugman: the attack; reserves would have run out; reserves lost in the attack",
            f"year {K['T_attack']:.0f}; year {K['T_exhaust']:.0f}; {K['jump_reserves']:.0f}")
    assert K["T_attack"] < K["T_exhaust"]

    P = T["playit"]
    O = openecon.obstfeld_regions(P["cost"], P["gamma"], P["delta"])
    both = [openecon.obstfeld_outcome(P["u_island"], e, P["cost"], P["gamma"], P["delta"]) for e in (False, True)]
    lab.row("Obstfeld: the band with two equilibria; the Island's outcome without and with an expected devaluation",
            f"({O['safe_below']:.2f}, {O['doomed_above']:.2f}); {both[0]}, {both[1]}")
    assert both == ["defend", "abandon"]

    ip, tw = monthly("IREXFUELS"), monthly("TWEXBMTH")
    ks = sorted(k for k in ip if k in tw and k <= "2019-12")
    pt = openecon.passthrough(np.diff(np.log([ip[k] for k in ks])), np.diff(np.log([tw[k] for k in ks])))
    lab.row("pass-through into US import prices ex fuel: on impact; after a year (share of the dollar's move)",
            f"{-pt['impact']:.2f}; {-pt['long_run']:.2f}")
    assert 0 < -pt["long_run"] < 1

    lab.note = ("Real exchange rates return to parity, but half a deviation lasts years; high-interest currencies tend "
                "to rise rather than fall, which pays the carry trade until it crashes; and out of sample neither "
                "interest parity nor the past beats 'no change'. Under a peg money cannot move output; under a float "
                "fiscal policy cannot. Sticky prices make currencies overshoot, attacks come before reserves run out, "
                "and in a middle zone a peg falls because it is expected to.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    y, q = Rr["GBR"]
    k = (y >= 1870) & (y <= 2020)
    ax[0].plot(y[k], q[k] - np.nanmean(q[k]), color=labs.BLUE)
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="Britain's real exchange rate against the dollar", xlabel="year", ylabel="log, demeaned")
    ax[1].plot(D["t"], 100 * np.array(D["s"]), color=labs.ORANGE, label="exchange rate")
    ax[1].plot(D["t"], 100 * np.array(D["p"]), color=labs.BLUE, label="price level")
    ax[1].axhline(100 * T["dornbusch"]["dm"], color="grey", ls="--", lw=0.8)
    ax[1].set(title="Overshooting after 10% more money", xlabel="years", ylabel="% from the old level")
    ax[1].legend()
    lab.fig = fig
    return lab
