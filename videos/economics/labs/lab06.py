"""Lab 6: Slutsky's two effects, Giffen behaviour in an experiment, duality, integrability, Engel drift and welfare."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import demand as dm
from explainer.economics.island import truths

TITLE = "Demand: Slutsky, Giffen, duality and welfare"
GOAL = ("Split a price change into substitution and income effects two ways and check the Slutsky equation; find the "
        "subsistence household's three zones and its Giffen elasticity; run Jensen and Miller's voucher design on "
        "simulated households with the truth planted; check the duality identities on four demand systems; send "
        "compensated income round a loop of prices and compare it with Green's theorem; recover a planted CPI bias "
        "from drifting Engel curves; and compare consumer's surplus, CV and the exact deadweight loss of a tax.")
TASKS = [
    "Make the fish in the subsistence diet cheaper calories (900 calories each). What happens to the Giffen "
    "elasticity, and to the range of coconut prices where demand slopes up? Explain with r / (1 - r).",
    "In the voucher experiment, double the reporting error. How much does the 60-80% estimate fall, and why does "
    "error in the calorie share bias it toward zero? (Hint: misclassification.)",
    "Give the AIDS survey an asymmetric gamma (gamma_12 = 0.08, gamma_21 = 0.02, keeping rows and columns summing to "
    "zero) and fit it. Does the Wald test reject symmetry, and how large a survey does it need to?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(6)

    # Slutsky: Bo, fish $10 -> $6, both compensations, and the equation at a small change
    b = T["bo"]
    bo = dm.CobbDouglas((b["a"], 1 - b["a"]))
    p0, p1, m = np.array([b["fish"][0], b["coconut"]]), np.array([b["fish"][1], b["coconut"]]), b["income"]
    hk = dm.decompose(bo, 0, p0, p1, m, "hicks")
    sl = dm.decompose(bo, 0, p0, p1, m, "slutsky")
    lab.row("Bo, fish $10 -> $6: Hicks (substitution, income)", f"{hk['substitution']:+.3f}, {hk['income']:+.3f}")
    lab.row("Bo, fish $10 -> $6: Slutsky (substitution, income)", f"{sl['substitution']:+.3f}, {sl['income']:+.3f}")
    S = dm.slutsky_matrix(bo, p0, m)
    el = dm.elasticities(bo, p0, m)
    assert abs(el["marshall"][0, 0] - (el["hicks"][0, 0] - el["shares"][0] * el["income"][0])) < 1e-6
    assert abs(hk["total"] - sl["total"]) < 1e-12 and sl["substitution"] > hk["substitution"] > 0
    lab.row("Bo's Slutsky matrix: symmetric, negative semidefinite", f"asymmetry {dm.slutsky_report(S, p0)['asymmetry']:.1e}")

    # the subsistence diet: zones and the Giffen elasticity
    d = T["diet"]
    diet = dm.Diet(d["coconut_kcal"], d["fish_kcal"], d["need"], d["beta"], d["s0"])
    lo, hi = diet.zone_bounds(1.2, 2.0)
    eps = diet.elasticity(1.2, 2.0, 21.0)
    assert abs(eps - diet.giffen_elasticity(1.2, 2.0)) < 1e-6 and eps > 0
    lab.row("Play-it household at $1.20: zones by income, elasticity", f"deprived < ${lo:.2f} < subsistence < ${hi:.2f}; "
                                                                       f"{eps:+.3f}")

    # the voucher experiment, with the truth planted
    v = T["vouchers"]
    island_diet = dm.Diet(d["coconut_kcal"], d["fish_kcal"], d["need"], d["beta"], d["s0"], d["other_share"],
                          d["other_kcal"])
    ex = dm.voucher_experiment(island_diet, v["households"], v["villages"], v["cuts"], v["coconut"], v["fish"],
                               v["median"], v["sigma"], v["need_sd"], v["report_sd"], v["income_sd"], v["seed"] + seed)
    sh = ex["share0"]
    full = dm.fe_regression(ex["dS"], ex["dP"], ex["cell"], ex["hh"])
    mid = (sh >= 0.6) & (sh <= 0.8)
    mid_r = dm.fe_regression(ex["dS"][mid], ex["dP"][mid], ex["cell"][mid], ex["hh"][mid])
    lab.row("vouchers: all households, coconut shares 60-80%", f"{full['b']:+.2f} ({full['se']:.2f}), "
                                                               f"{mid_r['b']:+.2f} ({mid_r['se']:.2f}); planted "
                                                               f"{island_diet.giffen_elasticity(1.2, 2.0):+.2f}")
    assert mid_r["b"] > full["b"] and mid_r["b"] > 0

    # duality on four systems
    worst = 0.0
    for sys in (dm.CobbDouglas((0.5, 0.3, 0.2)), dm.CES((0.5, 0.3, 0.2), 0.5),
                dm.StoneGeary((0.3, 0.5, 0.2), (5.0, 2.0, 1.0)), dm.AIDS(alpha0=np.log(100.0))):
        worst = max(worst, max(dm.duality_errors(sys, np.array([2.0, 3.0, 1.5]), 100.0).values()))
    lab.row("duality identities, four systems: largest relative error", f"{worst:.1e}")
    assert worst < 1e-6

    # integrability: a loop of prices
    lp = T["loop"]
    path = dm.circle_path((0.0, 0.0), lp["radius"])
    gaps = {}
    for key in ("symmetric", "circular"):
        g = dm.AIDS(alpha=lp["alpha"], beta=(0.0, 0.0, 0.0), gamma=lp[key])
        gaps[key] = dm.loop_income(g.shares, path)[-1]
    ga = np.array(lp["circular"])
    green = (ga[1, 0] - ga[0, 1]) * np.pi * lp["radius"] ** 2
    lab.row("loop of radius 0.4: log income gap, symmetric / circular (Green)",
            f"{gaps['symmetric']:+.1e} / {gaps['circular']:+.4f} ({green:+.4f})")
    assert abs(gaps["symmetric"]) < 1e-9 and abs(gaps["circular"] - green) < 1e-4

    # Hamilton: drifting Engel curves read a planted CPI bias
    h = T["hamilton"]
    rng = np.random.default_rng(h["seed"] + seed)
    W, M, Y, R = [], [], [], []
    for t in h["years"]:
        lrel = rng.normal(0, h["food_price_sd"], h["regions"])[np.arange(h["households"]) % h["regions"]]
        ly = np.log(h["median"]) + h["growth"] * t + h["sigma"] * rng.standard_normal(h["households"])
        W.append(h["a"] + h["b"] * (ly - np.log(h["median"])) + h["g"] * lrel + rng.normal(0, h["noise"], len(ly)))
        M.append(np.exp(ly - h["bias"] * t) / h["median"])
        Y.append(np.full(len(ly), t))
        R.append(lrel)
    fit = dm.hamilton_drift(*map(np.concatenate, (W, M, Y, R)))
    per_year = np.polyfit(fit["years"], fit["cumulative_bias"], 1)[0]
    lab.row("Hamilton's method: CPI bias a year, planted / recovered", f"{h['bias']:.3f} / {per_year:.4f}")
    assert abs(per_year - h["bias"]) < 0.003

    # welfare: a coconut tax, Willig and Hausman
    tx = T["tax"]
    L = dm.LinearDemand(tx["alpha"], tx["delta"], tx["c"])
    r = L.tax(tx["price"], tx["taxes"][1], tx["income"])
    lab.row("60-cent tax: CS, CV, EV; deadweight loss Marshall / exact",
            f"{r['cs']:.3f}, {r['cv']:.3f}, {r['ev']:.3f}; {r['dwl_marshall']:.3f} / {r['dwl_exact']:.3f}")
    assert r["ev"] < r["cs"] < r["cv"] and r["dwl_marshall"] > r["dwl_exact"]

    lab.note = ("Slutsky's compensation is the more generous, so it books more of the move as substitution; the "
                "subsistence household's coconut demand slopes up exactly in its middle zone; the experiment recovers "
                "the Giffen households only when they are sorted by calorie share; every duality identity holds to "
                "numerical precision; an asymmetric Slutsky matrix leaves money on the table round a loop, as Green's "
                "theorem predicts; Engel curves recover the planted CPI bias; and Marshall's surplus is close to CV "
                "while his deadweight loss is not.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ps = np.linspace(0.45, 2.3, 300)
    s_ = [diet.staple(p, 2.0, 21.0) for p in ps]
    ax[0].plot(s_, ps, color=labs.ORANGE, lw=2.2)
    ax[0].set(title="The Play-it household's coconut demand ($21)", xlabel="coconuts a week",
              ylabel="price of a coconut ($)")
    grid = np.arange(0.40, 0.951, 0.025)
    loc = dm.local_elasticity(ex, grid, 0.10)
    ax[1].plot(grid, loc["b"], color=labs.BLUE, lw=2.2, label="estimated")
    ax[1].fill_between(grid, loc["lo"], loc["hi"], color=labs.BLUE, alpha=0.2)
    ax[1].axhline(0, color="grey", lw=1)
    ax[1].set(title="Price elasticity by calorie share (vouchers)", xlabel="share of calories from coconuts",
              ylabel="elasticity")
    ax[1].legend()
    lab.fig = fig
    return lab
