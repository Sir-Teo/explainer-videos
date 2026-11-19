"""Precompute every number in Part 7 of *Economics, Built* ("Time and Risk").

    python -m videos.economics.econ7.compute            # everything missing (seconds)
    python -m videos.economics.econ7.compute --force rabin

Results are cached in ``.cache/econ7/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: real personal consumption expenditures, the PCE price index, the population and the
3-month Treasury bill rate, 1934-2025; the transcribed tables of Bernoulli, Samuelson, Allais, Ellsberg, Rabin,
Thaler, Holt and Laury, Hayden and Platt, Madrian and Shea, Thaler and Benartzi, Barsky et al., Post et al. and Mehra
and Prescott).  Models: Agora's time and risk (``agora.risk``), with the Island's Part 7 truths.  Every random draw
is seeded.

Items:
    stpete       the St Petersburg game: its terms, a million simulated games and their running average, Bernoulli's
                 and Cramer's prices by wealth, the median heuristic; the Called-it numbers
    fisher       Chidi's two seasons: the budget line, his choice and the Euler equation; saving against the interest
                 rate for three elasticities of substitution
    discount     present values at 3% and 10%; exponential, hyperbolic and quasi-hyperbolic discount functions
    triangle     the probability triangle on $0, $1M, $5M: Allais's four lotteries and expected utility's lines
    aversion     Ana's reef and open sea: certainty equivalents, risk premia, Arrow-Pratt's approximation; CARA
                 against CRRA as wealth grows
    insurance    Ana's boat: cover against its price; deductibles' implied risk aversion; the risky asset's share
    dominance    three nets: CDFs and their integrals; first- and second-order dominance
    paradoxes    fanning out (weighted utility) in the triangle; Ellsberg's urn under maxmin; prospect theory's curves
    rabin        Rabin's calibration for CRRA choosers, against his tables
    eis          the (gamma, psi) plane: expected utility's diagonal, Epstein-Zin, early resolution's premium
    present      Thaler's survey; reversals; Chidi's dry-season store under beta-delta: the plan, what happens, a
                 commitment
    measuring    Holt and Laury's menu and intervals; their table; the menu run on 400 islanders; the HRS thresholds
    robust       the venture under ambiguity: maxmin and Hansen-Sargent's multiplier preferences
    dial         the dials' rows: relative risk aversion and the EIS
    film         the intermission's data film: consumption growth against the real interest rate, 1935-2025
    melody       its data melody: the real Treasury bill rate, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import calls, data, dials, island, score
from explainer.economics.agora import risk as rk
from explainer.economics.data import tables

CACHE = Cache("econ7")
load = CACHE.load
TRUTH = island.truths(7)


# ---------------------------------------------------------------------------------------------------------------
# the St Petersburg game

def compute_stpete() -> dict:
    t = TRUTH["stpete"]
    first = t["first"]
    ks = np.arange(1, 11)
    prob, prize = 0.5 ** ks, first * 2.0 ** (ks - 1)
    rng = np.random.default_rng(t["seed"])
    tosses = rng.geometric(0.5, size=12)                      # the hook's first twelve games: tosses until heads
    games = rk.stpetersburg_play(t["games"], np.random.default_rng(t["seed"] + 1), first)
    run = np.cumsum(games) / np.arange(1, len(games) + 1)
    at = np.unique(np.round(np.logspace(0, np.log10(len(games)), 240)).astype(int))
    wgrid = np.logspace(1, 7, 61)
    prices = {u: [rk.stpetersburg_price(w, u, first=first) for w in wgrid] for u in ("log", "sqrt")}
    named = {f"{w:g}": {"log": rk.stpetersburg_price(w, "log", first=first),
                        "sqrt": rk.stpetersburg_price(w, "sqrt", first=first)} for w in t["wealths"]}
    hp = tables.HAYDEN_PLATT_2009.data
    trunc = [rk.stpetersburg_truncated_value(n, first) for n in hp["truncated"]["tosses"]]
    assert np.allclose(trunc, hp["truncated"]["ev"])           # the transcription agrees with the game's arithmetic
    med = {n: rk.stpetersburg_median_prize(n, first, reps=3000, seed=7) for n in (1, 10, 100, 1000)}
    # the call: Bernoulli's prices at $1,000 and $1M, against the median bids
    c = calls.CALLS["bernoulli_1738"]
    assert c.verdict == "partly right"
    assert 5.5 < named["1000"]["log"] < 6.5 and 10.5 < named["1e+06"]["log"] < 11.5
    assert hp["real"]["median_bid"] == 1.75 and hp["hypothetical"]["median_bid"] == 1.50
    return {"ks": ks, "prob": prob, "prize": prize, "tosses": tosses, "run_at": at, "run": run[at - 1],
            "max_prize": float(games.max()), "share_1": float((games == first).mean()),
            "share_le_4": float((games <= 4 * first).mean()), "wgrid": wgrid, "prices": prices, "named": named,
            "ce_log": rk.stpetersburg_ce_alone("log", first=first), "ce_sqrt": rk.stpetersburg_ce_alone("sqrt",
                                                                                                    first=first),
            "trunc_tosses": hp["truncated"]["tosses"], "trunc_ev": trunc,
            "trunc_log": [float(_truncated_price(1000.0, n, first)) for n in hp["truncated"]["tosses"]],
            "median_heuristic": {str(k): v for k, v in med.items()}, "games": t["games"]}


def _truncated_price(w: float, n: int, first: float) -> float:
    """Bernoulli's log price, at wealth w, for the game cut off after n tosses."""
    from scipy.optimize import brentq

    ks = np.arange(1, n + 1)
    pk = list(0.5 ** ks) + [0.5 ** n]
    prize = list(first * 2.0 ** (ks - 1)) + [first * 2.0 ** n]
    pk, prize = np.array(pk), np.array(prize)
    return brentq(lambda c: float(pk @ np.log(w - c + prize) - np.log(w)), 0.0, w * 0.5)


# ---------------------------------------------------------------------------------------------------------------
# Fisher and discounting

def compute_fisher() -> dict:
    t = TRUTH["chidi"]
    y1, y2 = t["income"]
    r0, beta, gm = t["rate"], t["beta"], t["gamma"]
    f0 = rk.fisher(y1, y2, r0, beta, gm)
    hi = t["rates"][-2]                                        # the rate rises to 30%
    f1 = rk.fisher(y1, y2, hi, beta, gm)
    u0 = rk.crra(f0["c1"], gm) + beta * rk.crra(f0["c2"], gm)
    u1 = rk.crra(f1["c1"], gm) + beta * rk.crra(f1["c2"], gm)
    c1s = np.linspace(20, 200, 400)

    def ic(u):  # c2 on the indifference curve through utility u
        v = (u - rk.crra(c1s, gm)) / beta
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(v < 0, rk.crra_inv(v, gm), np.nan)

    # Hicks's split of the move from f0 to f1: compensate to the old curve at the new rate
    k = (beta * (1 + hi)) ** (1 / gm)
    # on the old curve with the new slope: c2 = k c1 and u0 = u(c1) + beta u(k c1)
    c1h = rk.crra_inv(u0 / (1 + beta * k ** (1 - gm)), gm)
    rates = np.linspace(0.0, 0.5, 51)
    sav = {f"{g:g}": [rk.fisher(y1, y2, r, beta, g)["saving"] for r in rates] for g in t["gammas"]}
    # many periods: log consumption growth against log(1 + r) has slope 1/gamma
    return {"y": (y1, y2), "r0": r0, "r1": hi, "beta": beta, "gamma": gm, "f0": f0, "f1": f1, "c1s": c1s,
            "ic0": ic(u0), "ic1": ic(u1), "hicks_c1": float(c1h), "hicks_c2": float(k * c1h), "rates": rates,
            "saving": sav, "gammas": t["gammas"], "growth0": f0["c2"] / f0["c1"], "growth1": f1["c2"] / f1["c1"],
            "euler_gap": f0["euler_gap"]}


def compute_discount() -> dict:
    t = TRUTH["discount"]
    years = np.arange(0, t["years"] + 1)
    pv = {f"{r:g}": list(t["prize"] / (1 + r) ** years) for r in t["rates"]}
    tt = np.linspace(0, 30, 301)
    curves = {"exponential": rk.discount(tt, "exponential", rate=0.10),
              "hyperbolic": rk.discount(tt, "hyperbolic", a=1.0, b=1.0),
              "beta-delta": rk.discount(tt, "beta-delta", beta=0.7, delta=float(np.exp(-0.05)))}
    # time consistency: the ratio D(t + 1) / D(t), the price of waiting one more year, seen from today
    ratio = {k: list(np.array(rk.discount(np.arange(1, 21), k, rate=0.10, a=1.0, b=1.0, beta=0.7,
                                          delta=float(np.exp(-0.05)))) /
                     np.array(rk.discount(np.arange(0, 20), k, rate=0.10, a=1.0, b=1.0, beta=0.7,
                                          delta=float(np.exp(-0.05)))))
             for k in ("exponential", "hyperbolic", "beta-delta")}
    stream = np.full(11, 10.0)
    sp = {f"{r:g}": float((stream / (1 + r) ** np.arange(11)).sum()) for r in t["rates"]}
    return {"years": years, "pv": pv, "prize": t["prize"], "rates": t["rates"], "tt": tt, "curves": curves,
            "ratio": ratio, "stream_pv": sp, "samuelson": tables.SAMUELSON_1937.data}


# ---------------------------------------------------------------------------------------------------------------
# lotteries and the triangle

ALLAIS_PTS = {"1A": (0.0, 0.0), "1B": (0.01, 0.10), "2A": (0.89, 0.0), "2B": (0.90, 0.10)}


def _eu_lines(slope: float, n: int = 9):
    """Expected utility's indifference lines in the triangle (p_low across, p_high up): p_high = c + slope p_low,
    clipped to the triangle; a family of parallel segments."""
    out = []
    for c in np.linspace(-slope, 1.0, n + 2)[1:-1]:
        xs = np.linspace(0, 1, 401)
        ys = c + slope * xs
        ok = (ys >= 0) & (xs + ys <= 1)
        if ok.sum() > 2:
            out.append([(float(x), float(y)) for x, y in zip(xs[ok], ys[ok])])
    return out


def compute_triangle() -> dict:
    ev = {k: float(np.dot(*rk.ALLAIS[k])) for k in rk.ALLAIS}
    chord = (ALLAIS_PTS["1B"][1] - ALLAIS_PTS["1A"][1]) / (ALLAIS_PTS["1B"][0] - ALLAIS_PTS["1A"][0])
    fams = {}
    for um in (0.5, 0.9, 0.95):
        s = rk.eu_slope(0.0, um, 1.0)
        fams[f"{um:g}"] = {"slope": s, "lines": _eu_lines(s, 7), "picks": "A" if s > chord else "B"}
    return {"points": ALLAIS_PTS, "ev": ev, "chord": float(chord), "families": fams,
            "pairs": tables.ALLAIS_1953.data["pairs"], "kt": tables.ALLAIS_1953.data["kt_problem1_sure"]}


# ---------------------------------------------------------------------------------------------------------------
# risk aversion, insurance, the risky asset

def compute_aversion() -> dict:
    t = TRUTH["ana"]
    w = t["wealth"]
    sea = np.array(t["sea"]) + w
    reef = t["reef"] + w
    p = (0.5, 0.5)
    rows = []
    for g in t["gammas"]:
        ce = rk.certainty_equivalent(sea, p, gamma=g) if g > 0 else float(np.dot(sea, p))
        rows.append({"gamma": g, "ce": ce, "premium": float(np.dot(sea, p) - ce), "takes": "sea" if ce > reef else
                     "reef"})
    from scipy.optimize import brentq

    g_star = brentq(lambda g: rk.certainty_equivalent(sea, p, gamma=g) - reef, 0.05, 20)
    xs = np.linspace(30, 200, 300)
    u2 = rk.crra(xs, 2.0)
    # Arrow-Pratt in the small: premium ~ (1/2) (gamma / w) variance, for 50-50 bets of +-h around $120, with
    # Bernoulli's logarithm (for gamma = 2 and even bets the approximation happens to be exact)
    hs = np.linspace(2, 80, 40)
    exact = [120 - rk.certainty_equivalent([120 - h, 120 + h], p, gamma=1.0) for h in hs]
    approx = [0.5 * 1.0 / 120 * h ** 2 for h in hs]
    # CARA against CRRA: the premium for a 50-50 +-$20 bet as wealth grows
    ws = np.linspace(40, 400, 37)
    a = 2.0 / 120                                               # the same absolute aversion at $120
    cara = [x - rk.certainty_equivalent([x - 20, x + 20], p, a=a) for x in ws]
    crra = [x - rk.certainty_equivalent([x - 20, x + 20], p, gamma=2.0) for x in ws]
    return {"wealth": w, "sea": sea, "reef": reef, "rows": rows, "g_star": float(g_star), "xs": xs, "u2": u2,
            "hs": hs, "exact": exact, "approx": approx, "ws": ws, "cara": cara, "crra": crra,
            "ev_sea": float(np.dot(sea, p))}


def compute_insurance() -> dict:
    b = TRUTH["boat"]
    out = {"wealth": b["wealth"], "boat": b["boat"], "storm": b["storm"], "gamma": b["gamma"], "covers": {}}
    for ld in b["loadings"]:
        oc = rk.optimal_cover(b["wealth"], b["boat"], b["storm"], ld, b["gamma"])
        q, eu = oc["q"], oc["eu"]
        out["covers"][f"{ld:g}"] = {"cover": oc["cover"], "premium": oc["premium"], "q": q[::40], "eu": eu[::40]}
    # the most Ana would pay for full cover: wealth minus her certainty equivalent of the uninsured lottery
    ce = rk.certainty_equivalent([b["wealth"], b["wealth"] - b["boat"]], [1 - b["storm"], b["storm"]],
                                 gamma=b["gamma"])
    out["max_premium"] = float(b["wealth"] - ce)
    out["fair_premium"] = float(b["storm"] * b["boat"])
    d = TRUTH["deductible"]
    lo, hi = d["deductibles"]
    out["deductible"] = {"wealth": d["wealth"], "claim": d["claim"], "low": lo, "high": hi,
                         "saving": d["claim"] * (hi - lo),
                         "rows": [(x, rk.deductible_gamma(d["wealth"], d["claim"], lo, hi, x)) for x in d["extra"]]}
    v = TRUTH["venture"]
    R = np.array(v["outcomes"])
    mu, sd = float(R.mean() - 1), float(R.std())
    shares = np.linspace(0, 1.6, 161)
    out["venture"] = {"safe": v["safe"], "mu": mu, "sd": sd, "outcomes": R,
                      "merton": {f"{g:g}": rk.merton_share(mu, v["safe"], sd, g) for g in v["gammas"]},
                      "shares": shares,
                      "eu": {f"{g:g}": list(rk.portfolio_eu(shares, 100.0, v["safe"], R, [0.5, 0.5], g))
                             for g in (2.0, 4.0)}}
    for g in (2.0, 4.0):
        e = np.array(out["venture"]["eu"][f"{g:g}"])
        out["venture"][f"best_{g:g}"] = float(shares[int(np.argmax(e))])
    return out


# ---------------------------------------------------------------------------------------------------------------
# dominance and the paradoxes

def compute_dominance() -> dict:
    n = TRUTH["nets"]
    grid = np.linspace(-1, 13, 1401)

    def cdf(x, p):
        x, p = np.asarray(x, float), np.asarray(p, float)
        return np.array([p[x <= g].sum() for g in grid])

    out = {"grid": grid}
    for k, (x, p) in n.items():
        F = cdf(x, p)
        out[k] = {"x": x, "p": p, "F": F, "IF": np.cumsum(F) * (grid[1] - grid[0]), "mean": float(np.dot(x, p))}
    out["fosd"] = rk.fosd(*n["better"], *n["old"])
    out["sosd"] = rk.sosd(*n["old"], *n["spread"])
    out["fosd_spread"] = rk.fosd(*n["old"], *n["spread"]) or rk.fosd(*n["spread"], *n["old"])
    out["ce"] = {k: {f"{g:g}": rk.certainty_equivalent(np.array(x) + 10, p, gamma=g) - 10 for g in (0.5, 2.0, 5.0)}
                 for k, (x, p) in n.items()}
    return out


def compute_paradoxes() -> dict:
    f = TRUTH["fanning"]
    u, w = f["u"], f["w"]
    lines = []
    for k in np.linspace(0.08, 0.92, 9):
        (x0, y0), (x1, y1) = rk.weighted_utility_line(k, u, w)
        xs = np.linspace(0, 1, 401)
        ys = y0 + (y1 - y0) * xs
        ok = (ys >= 0) & (xs + ys <= 1)
        if ok.sum() > 2:
            lines.append([(float(a), float(b)) for a, b in zip(xs[ok], ys[ok])])
    V = {k: rk.weighted_utility_value(*v, u, w) for k, v in ALLAIS_PTS.items()}
    assert V["1A"] > V["1B"] and V["2B"] > V["2A"]
    # the slopes of the fanned lines at the two pairs
    def slope_at(pt):
        k = rk.weighted_utility_value(*pt, u, w)
        (x0, y0), (x1, y1) = rk.weighted_utility_line(k, u, w)
        return float(y1 - y0)

    e = rk.ellsberg_maxmin()
    xs = np.linspace(-100, 100, 401)
    ps = np.linspace(0, 1, 201)
    return {"lines": lines, "values": V, "slope_1": slope_at(ALLAIS_PTS["1A"]), "slope_2": slope_at(ALLAIS_PTS["2A"]),
            "u": u, "w": w, "ellsberg": e, "urn": tables.ELLSBERG_1961.data, "xs": xs, "value": rk.tk_value(xs),
            "ps": ps, "weight": rk.tk_weight(ps)}


def compute_rabin() -> dict:
    rows = []
    for w in (10_000.0, 100_000.0, 300_000.0, 1_000_000.0):
        rows.append({"wealth": w, "gamma": rk.crra_gamma_to_reject(100, 110, w)})
    w = 100_000.0
    g = rk.crra_gamma_to_reject(100, 110, w)
    losses = (400, 600, 800, 1000, 2000)
    crra_g = [rk.crra_largest_gain(L, w, g) for L in losses]
    tab = tables.RABIN_2000.data
    # an ordinary chooser: gamma 2 at $100,000 takes lose $100 / gain $110 (and is near indifferent to lose $100 /
    # gain $100.20)
    from scipy.optimize import brentq

    g2 = brentq(lambda G: rk._crra_gain(100, G, w, 2.0), 100.0, 200.0)
    return {"rows": rows, "wealth": w, "gamma": g, "losses": losses, "crra_largest": crra_g,
            "table1": tab["table1_g110"], "table1_101": tab["table1_g101"], "table2": tab["table2_g110"],
            "example": tab["example"], "example2": tab["example2"], "g2_breakeven": float(g2)}


# ---------------------------------------------------------------------------------------------------------------
# time meets risk; present bias

def compute_eis() -> dict:
    e = TRUTH["ez"]
    c0, c1 = e["c"]
    res = []
    for g, psi in e["calibrations"]:
        r = rk.ez_resolution(c0, c1, e["c2"], (0.5, 0.5), e["beta"], g, psi)
        res.append({"gamma": g, "psi": psi, **r})
    d1, d2 = dials.DIALS["risk_aversion"], dials.DIALS["eis"]
    return {"calibrations": res, "c2": e["c2"], "beta": e["beta"], "psi_grid": np.linspace(0.05, 2.5, 100),
            "mp": tables.MEHRA_PRESCOTT_1985.data, "barsky": tables.BARSKY_1997.data,
            "rra_rows": [(x.who, x.year, x.design, x.value) for x in d1.estimates],
            "eis_rows": [(x.who, x.year, x.design, x.value) for x in d2.estimates]}


def compute_present() -> dict:
    t = TRUTH["present"]
    th = tables.THALER_1981.data
    months = np.array(th["months"], float)
    eq = np.array(th["median_equivalent"], float)
    rates = np.log(eq / th["now"]) / (months / 12)             # continuous annual rates, as Frederick et al. report
    assert np.allclose(rates, th["annual_rate"], atol=0.01)
    b = rk.beta_delta_path(t["store"], t["weeks"], t["beta"], t["delta"])
    plan, naive = b["plan"], b["naive"]

    def U0(path):
        w = np.r_[1.0, t["beta"] * t["delta"] ** np.arange(1, t["weeks"])]
        return float(w @ np.log(path))

    # the self at week 0 would pay this share of the whole store to lock its plan in
    from scipy.optimize import brentq

    pay = brentq(lambda k: U0(plan * (1 - k)) - U0(naive), 0.0, 0.5)
    rev = {"exp": rk.reversal(100, 110, 1 / 365, 30 / 365, kind="exponential", rate=0.5),
           "bd": rk.reversal(100, 110, 1 / 365, 30 / 365, kind="beta-delta", beta=0.9, delta=0.96)}
    return {"thaler": th, "rates": rates, "plan": plan, "naive": naive, "exponential": b["exponential"],
            "store": t["store"], "weeks": t["weeks"], "beta": t["beta"], "u_plan": U0(plan), "u_naive": U0(naive),
            "commit_worth": float(pay), "reversal": rev}


# ---------------------------------------------------------------------------------------------------------------
# measuring it

def compute_measuring() -> dict:
    menu = rk.holt_laury_menu()
    rows = []
    for r in menu:
        pa = (r["p"], 1 - r["p"])
        rows.append({"k": r["k"], "p": r["p"], "ev_a": float(np.dot(r["A"], pa)), "ev_b": float(np.dot(r["B"], pa))})
    intervals = {n: rk.holt_laury_interval(n) for n in range(2, 10)}
    hl = tables.HOLT_LAURY_2005.data
    t = TRUTH["hl"]
    rng = np.random.default_rng(t["seed"])
    gam = rng.normal(t["gamma_mean"], t["gamma_sd"], t["people"])
    ch = rk.holt_laury_respond(gam, t["noise"], rng)
    n_safe = ch.sum(axis=1)
    back = rk.switches_back(ch)
    # each consistent respondent's interval midpoint, as a reader of the menu would score them
    mids = []
    for n in n_safe[~back]:
        lo, hi = intervals.get(int(n), (np.nan, np.nan))
        mids.append((lo + hi) / 2 if np.isfinite(lo) else np.nan)
    mids = np.array(mids)
    ok = np.isfinite(mids)
    tg = gam[~back][ok]
    exact = np.array([rk.safe_choices(g) for g in gam])         # what each would choose without noise
    hrs = {f"{c:.4f}": rk.hrs_threshold(c) for c in tables.BARSKY_1997.data["cuts"]}
    return {"menu": rows, "intervals": {str(k): v for k, v in intervals.items()}, "table": hl, "gammas": gam,
            "n_safe": n_safe, "exact_safe": exact, "switch_back": float(back.mean()),
            "mean_true": float(gam.mean()), "mean_scored": float(np.nanmean(mids)),
            "corr": float(np.corrcoef(tg, mids[ok])[0, 1]), "hist": np.bincount(n_safe, minlength=11),
            "hist_exact": np.bincount(exact, minlength=11), "hrs": hrs, "barsky": tables.BARSKY_1997.data,
            "noise": t["noise"], "people": t["people"]}


def compute_robust() -> dict:
    """The venture under ambiguity.  Maxmin: the chance of the good year is only known to lie in [0.5 - e, 0.5 + e];
    the share is chosen against the worst chance.  Multiplier (Hansen and Sargent): nature tilts the chances against
    the chooser, p* proportional to p exp(-u / theta); a smaller theta, a stronger fear of misspecification."""
    v = TRUTH["venture"]
    R = np.array(v["outcomes"])
    shares = np.linspace(0, 1.2, 241)
    w, r, g = 100.0, v["safe"], 2.0
    wealth = w * ((1 - shares)[:, None] * (1 + r) + shares[:, None] * R[None, :])
    U = rk.crra(wealth, g)
    eps = np.linspace(0, 0.2, 41)
    mm = []
    for e in eps:
        worst = np.minimum(U @ np.array([0.5 + e, 0.5 - e]), U @ np.array([0.5 - e, 0.5 + e]))
        mm.append(float(shares[int(np.argmax(worst))]))
    thetas = np.logspace(-3.4, -0.6, 41)
    hs = []
    for th in thetas:
        # the multiplier criterion: -theta log E[exp(-u / theta)]
        val = -th * np.log((np.exp(-(U - U.max()) / th) * 0.5).sum(axis=1)) + U.max()
        hs.append(float(shares[int(np.argmax(val))]))
    base = float(shares[int(np.argmax(U @ np.array([0.5, 0.5])))])
    return {"eps": eps, "maxmin": mm, "thetas": thetas, "multiplier": hs, "base": base, "gamma": g}


def compute_dial() -> dict:
    out = {}
    for key in ("risk_aversion", "eis"):
        dl = dials.DIALS[key]
        out[key] = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dl.estimates]
    return out


# ---------------------------------------------------------------------------------------------------------------
# the intermission: Hall's Euler equation, 1935-2025

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    """When the data film reaches the k-th year (0-based) of n."""
    return 1.5 + FILM_SECONDS * k / (n - 1)


def _euler_data():
    def ann(s):
        d = data.fred(s)
        return np.array([int(x[:4]) for x in d["date"]]), np.array(d["value"], float)

    yc, c = ann("PCECCA")
    yp, pop = ann("B230RC0A052NBEA")
    yd, P = ann("DPCERG3A086NBEA")
    d = data.fred("TB3MS")
    ym = np.array([int(x[:4]) for x in d["date"]])
    tb = np.array(d["value"], float)
    years = np.arange(1935, 2026)
    tba = np.array([tb[ym == y].mean() for y in years])

    def at(yy, v, ys):
        return np.array([v[yy == y][0] for y in ys])

    span = np.arange(1934, 2026)
    cp = at(yc, c, span) / at(yp, pop, span)
    g = np.diff(np.log(cp)) * 100                                  # growth of real consumption per head, %
    pi = np.diff(np.log(at(yd, P, span))) * 100                    # PCE inflation, %
    r = tba - pi                                                   # the ex post real bill rate, %
    return years, g, r, tba, pi


def compute_film() -> dict:
    years, g, r, tb, pi = _euler_data()
    n = len(years)
    Z = np.c_[r[:-2], g[:-2], tb[1:-1]]                            # instruments: the rate and growth two years
    full = rk.euler_regression(g[2:], r[2:], Z)                    # back, the nominal rate a year back
    post = years[2:] >= 1950
    late = rk.euler_regression(g[2:][post], r[2:][post], Z[post])
    return {"years": years, "growth": g, "rate": r, "tbill": tb, "inflation": pi,
            "times": [film_time(k, n) for k in range(n)], "full": full, "post1950": late,
            "named": {int(y): (float(r[i]), float(g[i])) for i, y in enumerate(years) if y in (1942, 1946, 1980,
                                                                                               2009, 2020, 2021)}}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    rate = np.array(f["rate"])
    times = f["times"]
    mel = score.data_melody(rate, MELODY_SECONDS, times=times, act=2, log=False, low=45, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "the real interest rate on Treasury bills, 1935-2025, as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ7").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "rate": rate, "seconds": MELODY_SECONDS}


ITEMS = {
    "stpete": compute_stpete,
    "fisher": compute_fisher,
    "discount": compute_discount,
    "triangle": compute_triangle,
    "aversion": compute_aversion,
    "insurance": compute_insurance,
    "dominance": compute_dominance,
    "paradoxes": compute_paradoxes,
    "rabin": compute_rabin,
    "eis": compute_eis,
    "present": compute_present,
    "measuring": compute_measuring,
    "robust": compute_robust,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
