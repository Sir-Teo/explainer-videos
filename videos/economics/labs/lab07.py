"""Lab 7: Fisher's Euler equation, expected utility and its paradoxes, insurance, Rabin, present bias, measurement."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import risk as rk
from explainer.economics.island import truths

TITLE = "Time and risk: Euler, expected utility, Rabin and present bias"
GOAL = ("Price Bernoulli's game at different levels of wealth and against its truncations; solve Fisher's two periods "
        "and check the Euler equation; compute certainty equivalents and the demand for insurance and a risky asset; "
        "check that Allais's pairs differ by a common consequence and that fanning out produces the common pattern; "
        "calibrate Rabin's small bet for the power function; watch a present-biased self eat a store faster than "
        "planned; run Holt and Laury's menu on simulated respondents with the truth planted; and estimate Hall's "
        "Euler equation on a century of American data.")
TASKS = [
    "Bernoulli's game: at what wealth does his log price reach $20? Explain why each doubling of wealth adds about "
    "50 cents to the price (hint: the prize that matters is about as large as wealth).",
    "Holt and Laury's menu: raise the noise from $0.20 to $0.60. What happens to the share who switch back and to the "
    "scored mean gamma? Which is the more robust summary of a population, and why?",
    "Hall's regression: drop the war years 1942-1946 and re-estimate by OLS and by 2SLS. Which estimate moves more, "
    "and what does that say about using ex post real rates?",
]


def _euler_data():
    def ann(s):
        d = data.fred(s)
        return np.array([int(x[:4]) for x in d["date"]]), np.array(d["value"], float)

    yc, c = ann("PCECCA")
    yp, pop = ann("B230RC0A052NBEA")
    yd, P = ann("DPCERG3A086NBEA")
    d = data.fred("TB3MS")
    ym, tb = np.array([int(x[:4]) for x in d["date"]]), np.array(d["value"], float)
    years = np.arange(1935, 2026)
    tba = np.array([tb[ym == y].mean() for y in years])

    def at(yy, v, ys):
        return np.array([v[yy == y][0] for y in ys])

    span = np.arange(1934, 2026)
    g = np.diff(np.log(at(yc, c, span) / at(yp, pop, span))) * 100
    pi = np.diff(np.log(at(yd, P, span))) * 100
    return years, g, tba - pi, tba


def run(seed=0):
    lab = labs.Lab()
    T = truths(7)

    # Bernoulli's game: prices by wealth, and the truncated games
    first = T["stpete"]["first"]
    for w in T["stpete"]["wealths"]:
        lab.row(f"Bernoulli's log price at ${w:,.0f}", f"${rk.stpetersburg_price(w, 'log', first=first):.2f}")
    p1, p2 = rk.stpetersburg_price(1e3, first=first), rk.stpetersburg_price(2e3, first=first)
    assert 0.4 < p2 - p1 < 0.6                                             # half a dollar per doubling of wealth
    trunc = [rk.stpetersburg_truncated_value(n, first) for n in (3, 5, 8, 10, 15)]
    lab.row("truncated games (3, 5, 8, 10, 15 tosses): expected prize", ", ".join(f"${v:.2f}" for v in trunc))

    # Fisher: the Euler equation and the response of saving
    c = T["chidi"]
    f0 = rk.fisher(*c["income"], c["rate"], c["beta"], c["gamma"])
    f1 = rk.fisher(*c["income"], 0.30, c["beta"], c["gamma"])
    assert abs(f0["euler_gap"]) < 1e-12
    lab.row("Chidi at 10% and 30%: c1, c2, saving", f"({f0['c1']:.2f}, {f0['c2']:.2f}, {f0['saving']:.2f}) and "
                                                    f"({f1['c1']:.2f}, {f1['c2']:.2f}, {f1['saving']:.2f})")

    # certainty equivalents, insurance, the risky asset
    a = T["ana"]
    sea = np.array(a["sea"]) + a["wealth"]
    ce = {g: rk.certainty_equivalent(sea, (0.5, 0.5), gamma=g) for g in (1.0, 2.0, 4.0)}
    lab.row("the open sea's certainty equivalent, gamma 1 / 2 / 4", " / ".join(f"${v:.2f}" for v in ce.values()))
    assert abs(ce[2.0] - 90.0) < 1e-9
    b = T["boat"]
    covers = [rk.optimal_cover(b["wealth"], b["boat"], b["storm"], ld, b["gamma"])["cover"] for ld in b["loadings"]]
    lab.row("Ana's best cover at loadings 0, 20%, 50%", ", ".join(f"{100 * q:.1f}%" for q in covers))
    assert covers[0] == 1.0 and covers[0] > covers[1] > covers[2]
    v = T["venture"]
    R = np.array(v["outcomes"])
    lab.row("Merton's share, gamma 2 and 10", f"{rk.merton_share(R.mean() - 1, v['safe'], R.std(), 2):.2f}, "
                                              f"{rk.merton_share(R.mean() - 1, v['safe'], R.std(), 10):.2f}")

    # Allais: the common consequence, and fanning out
    ev = {k: float(np.dot(*rk.ALLAIS[k])) for k in rk.ALLAIS}
    assert abs((ev["1A"] - ev["1B"]) - (ev["2A"] - ev["2B"])) < 1e-6
    fz = T["fanning"]
    pts = {"1A": (0, 0), "1B": (0.01, 0.10), "2A": (0.89, 0), "2B": (0.90, 0.10)}
    V = {k: rk.weighted_utility_value(*p, fz["u"], fz["w"]) for k, p in pts.items()}
    lab.row("weighted utility: 1A vs 1B, 2A vs 2B", f"{V['1A']:.4f} > {V['1B']:.4f}; {V['2A']:.4f} < {V['2B']:.4f}")
    assert V["1A"] > V["1B"] and V["2B"] > V["2A"]

    # Rabin, for the power function
    g = rk.crra_gamma_to_reject(100, 110, 100_000)
    big = rk.crra_largest_gain(1000, 100_000, g)
    lab.row("gamma to refuse lose $100 / win $110 at $100,000; then lose $1,000 refused for gains up to",
            f"{g:.1f}; {'any sum' if not np.isfinite(big) else f'${big:,.0f}'}")
    assert not np.isfinite(big)

    # present bias: the store, and the value of commitment
    pr = T["present"]
    bd = rk.beta_delta_path(pr["store"], pr["weeks"], pr["beta"], pr["delta"])
    lab.row("Chidi's store: planned and eaten in the last week", f"{bd['plan'][-1]:.1f} and {bd['naive'][-1]:.1f}")
    assert bd["naive"][-1] < bd["plan"][-1]

    # Holt and Laury on simulated respondents
    h = T["hl"]
    rng = np.random.default_rng(h["seed"] + seed)
    gam = rng.normal(h["gamma_mean"], h["gamma_sd"], h["people"])
    ch = rk.holt_laury_respond(gam, h["noise"], rng)
    back = rk.switches_back(ch)
    brackets = {n: rk.holt_laury_interval(n) for n in range(2, 10)}
    mids = []
    for n in ch.sum(axis=1)[~back]:
        lo, hi = brackets.get(int(n), (np.nan, np.nan))
        mids.append((lo + hi) / 2)
    mids = np.array(mids)
    lab.row("Holt-Laury on 400 islanders: switch back, scored mean (planted)",
            f"{100 * back.mean():.1f}%, {np.nanmean(mids):.2f} ({gam.mean():.2f})")
    assert abs(np.nanmean(mids) - gam.mean()) < 0.1

    # Hall's Euler equation on FRED's data
    years, gr, r, tb = _euler_data()
    Z = np.c_[r[:-2], gr[:-2], tb[1:-1]]
    e = rk.euler_regression(gr[2:], r[2:], Z)
    lab.row("Hall's regression, 1937-2025: OLS, 2SLS (s.e.), first-stage F",
            f"{e['ols']:+.3f}, {e['iv']:+.3f} ({e['iv_se']:.3f}), {e['first_F']:.1f}")
    assert abs(e["iv"]) < 0.3

    lab.note = ("Bernoulli's price is small and grows by about half a dollar for every doubling of wealth; Chidi's "
                "saving barely responds to the interest rate because his EIS of one half makes the two effects "
                "cancel; a fair price buys full cover and any loading less; the Allais pairs differ only by a common "
                "consequence, and fanning out breaks the tie; a CRRA chooser who refuses a $100/$110 bet at $100,000 "
                "refuses to risk $1,000 for any gain; the present-biased store runs down; the menu recovers the "
                "planted mean despite noise; and in a century of data the instrumented EIS is close to zero.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ws = np.logspace(1, 7, 60)
    ax[0].semilogx(ws, [rk.stpetersburg_price(w, "log", first=first) for w in ws], color=labs.ORANGE, lw=2.2,
                   label="logarithm")
    ax[0].semilogx(ws, [rk.stpetersburg_price(w, "sqrt", first=first) for w in ws], color=labs.BLUE, lw=2.2,
                   label="square root")
    ax[0].axhline(1.75, color="grey", lw=1, ls="--")
    ax[0].set(title="Bernoulli's game: the price against wealth", xlabel="wealth ($)", ylabel="price ($)")
    ax[0].legend()
    ax[1].scatter(r, gr, s=14, color=labs.BLUE)
    xs = np.array([r.min(), r.max()])
    ax[1].plot(xs, e["ols_const"] + e["ols"] * xs, color=labs.ORANGE, lw=2, label="OLS")
    ax[1].set(title="Consumption growth against the real bill rate, 1935-2025", xlabel="real rate (%)",
              ylabel="growth per head (%)")
    ax[1].legend()
    lab.fig = fig
    return lab
