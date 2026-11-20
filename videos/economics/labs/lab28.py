"""Lab 28: inflation and expectations: Phillips's curve, acceleration at the natural rate, adaptive forecasts of
American inflation, Lucas's islands, the Lucas critique, Barro and Gordon's inflation bias with Rogoff's conservative
banker, the sacrifice ratio of 1980-85, and the flattening of the Phillips curve."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import expectations as ex
from explainer.economics.island import truths

TITLE = "Inflation and expectations: why the trade-off is temporary"
GOAL = ("Draw Phillips's curve; hold unemployment below its natural rate and watch inflation accelerate; forecast "
        "American inflation adaptively and score the rule; solve Lucas's signal extraction and the Lucas critique; "
        "find the inflation bias and the best conservative banker; and measure the sacrifice ratio and the slope of "
        "the Phillips curve on FRED's data.")
TASKS = [
    "Acceleration: let expectations adapt with lambda = 0.1. How long before inflation reaches 6%?",
    "Rogoff: double the variance of supply shocks. Does the best banker care more or less about output, and why?",
    "The slope: re-estimate the Phillips curve on 2020-2025 only. What does the surge do to it?",
]


def _annual_infl(key):
    d = data.fred(key)
    a: dict = {}
    for x, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            a.setdefault(int(x[:4]), []).append(v)
    m = {y: np.mean(v) for y, v in a.items() if len(v) >= 11}
    return {y: 100 * (m[y] / m[y - 1] - 1) for y in m if y - 1 in m}


def run(seed=0):
    lab = labs.Lab()
    T = truths(28)

    lab.row("Phillips (1958): wage growth at 2.5%, 5.5% and 8% unemployment",
            ", ".join(f"{w:.2f}%" for w in ex.phillips1958([2.5, 5.5, 8.0])))

    A = T["accelerate"]
    fast = ex.accelerate(A["years"], A["ustar"], A["u_target"], A["beta"], A["lam"], A["pi0"])
    slow = ex.accelerate(A["years"], A["ustar"], A["u_target"], A["beta"], A["lam_slow"], A["pi0"])
    assert fast["pi"][-1] > slow["pi"][-1] > A["pi0"]
    lab.row("u held a point below u*: inflation after 15 years, fast and slow learners",
            f"{fast['pi'][-1]:.1f}%, {slow['pi'][-1]:.1f}%")

    inf = _annual_infl("CPIAUCSL")
    yrs = [y for y in range(1960, 2026) if y in inf]
    x = [inf[y] for y in yrs]
    for lam in T["adaptive"]["lams"]:
        f = ex.adaptive_forecasts(x, lam)
        lab.row(f"adaptive forecasts of US inflation, lambda = {lam}: RMSE", f"{f['rmse']:.2f} points")

    I = T["islands"]
    calm = ex.lucas_islands(I["sigma_z"], I["sigma_m_calm"], I["b"], I["n_islands"], I["years"], I["seed"] + seed)
    wild = ex.lucas_islands(I["sigma_z"], I["sigma_m_wild"], I["b"], I["n_islands"], I["years"], I["seed"] + seed)
    assert calm["slope"] > wild["slope"]
    lab.row("Lucas's islands: output's response to money, calm and wild", f"{calm['slope']:.2f}, {wild['slope']:.2f}")

    C = ex.critique(**{**T["critique"], "seed": T["critique"]["seed"] + seed})
    assert C["predicted"] - C["actual"] > 5
    lab.row("the critique: fitted slope; predicted and actual output under the new rule",
            f"{C['slope']:.2f}; {C['predicted']:.1f} and {C['actual']:.1f}")

    B = T["bg"]
    g = ex.barro_gordon(B["lam"], B["k"], B["b"])
    r = ex.conservative_banker(B["lam"], B["k"], B["sigma"], B["b"])
    lab.row("Barro-Gordon: discretionary inflation; loss under discretion and the rule",
            f"{g['pi_discretion']:.1f}%; {g['loss_discretion']:.2f} and {g['loss_rule']:.2f}")
    lab.row("Rogoff: the best banker's weight on output, and society's loss",
            f"{r['best']:.2f}, {r['best_loss']:.2f} (vs {r['loss_at_lam']:.2f} at society's weight)")

    core = _annual_infl("CPILFESL")
    gdp = dict(zip(data.fred("GDPC1")["date"], data.fred("GDPC1")["value"]))
    pot = dict(zip(data.fred("GDPPOT")["date"], data.fred("GDPPOT")["value"]))
    gaps = [100 * (gdp[d] / pot[d] - 1) / 4 for d in sorted(gdp) if "1980-01-01" <= d <= "1985-10-01" and d in pot]
    s = ex.sacrifice_ratio(gaps, core[1980], core[1985])
    lab.row("the Volcker disinflation, 1980-85: point-years lost; points of disinflation; ratio",
            f"{s['lost']:.1f}; {s['fall']:.1f}; {s['ratio']:.2f}")

    un = data.fred("UNRATE")
    ua: dict = {}
    for d, v in zip(un["date"], un["value"]):
        if np.isfinite(v):
            ua.setdefault(int(d[:4]), []).append(v)
    ua = {y: np.mean(v) for y, v in ua.items()}
    nr = data.fred("NROU")
    na: dict = {}
    for d, v in zip(nr["date"], nr["value"]):
        na.setdefault(int(d[:4]), []).append(v)
    na = {y: np.mean(v) for y, v in na.items()}
    for a, b in ((1960, 1983), (2000, 2019)):
        ys = [y for y in range(a, b + 1) if y in core and y - 1 in core and y in ua and y in na]
        slope = np.polyfit([ua[y] - na[y] for y in ys], [core[y] - core[y - 1] for y in ys], 1)[0]
        lab.row(f"the Phillips curve's slope, {a}-{b}", f"{slope:.3f}")

    lab.note = ("Unemployment below its natural rate needs inflation above what people expect, so holding it there "
                "makes inflation accelerate. Looking back makes errors that run one way for years. When money is "
                "volatile, producers read price rises as inflation and output barely responds; a trade-off fitted "
                "under one rule vanishes under another. Without commitment a central bank inflates for nothing; a "
                "moderately conservative banker does better. America's disinflation cost about two point-years of "
                "output per point, and the curve has been much flatter since.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    u = np.linspace(1, 11, 200)
    ax[0].plot(u, ex.phillips1958(u), color=labs.BLUE)
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="Phillips (1958)", xlabel="unemployment, %", ylabel="wage growth, %", ylim=(-2, 10))
    ax[1].plot(range(1, A["years"] + 1), fast["pi"], color=labs.ORANGE, label="last year's inflation")
    ax[1].plot(range(1, A["years"] + 1), slow["pi"], color=labs.BLUE, label="slow learning")
    ax[1].set(title="Holding u below u*", xlabel="year", ylabel="inflation, %")
    ax[1].legend()
    lab.fig = fig
    return lab
