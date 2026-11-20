"""Lab 43: measuring market power: concentration and margins under Cournot, a merger simulated with nested logit,
plain logit and Berry, Levinsohn and Pakes's random-coefficient estimator on a simulated car market and plain logit on
their real data, Nevo's conduct test, production functions by OLS and Ackerberg, Caves and Frazer, markups from
production data, and Bresnahan and Reiss's entry thresholds."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import io
from explainer.economics.island import truths

TITLE = "Measuring market power"
GOAL = ("Show why concentration and margins correlate without collusion; simulate two mergers and see diversion beat "
        "market share; estimate demand by OLS, IV and BLP where the truth is known, and by logit on real cars; test "
        "conduct as Nevo did; estimate a production function and read markups from it; and recover entry "
        "thresholds from towns.")
TASKS = [
    "The merger game: lower the nesting parameter from 0.6 to 0.2. Which merger now raises prices more, and what "
    "happens to the diversion between the bran twins?",
    "Cars: drop the cost shifter from the instruments and keep only the crowding measures. What happens to the "
    "first-stage F and to the IV logit's alpha?",
    "Production: make labour less tied to productivity (sd_lerr from 0.3 to 0.8). How do the OLS and ACF "
    "estimates move, and what does that do to the markup from production data?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(43)

    S = io.scp(**{**T["scp"], "seed": T["scp"]["seed"] + seed})
    lab.row("300 Cournot industries: correlation of the Herfindahl index with the margin; within, share with margin",
            f"{S['corr']:.2f}; {S['within_corr']:.2f}")
    assert S["corr"] > 0.5

    P = T["playit"]
    q, mc, nests = np.array(P["quality"]), np.array(P["mc"]), np.array(P["nests"])

    def shares(p):
        return io.nested_shares(q - P["alpha"] * np.asarray(p, float), nests, P["sigma"])
    owner = np.arange(5)
    p0 = io.bertrand(shares, mc, owner)
    rx = io.merger(shares, p0, owner, list(P["x"]))
    ry = io.merger(shares, p0, owner, list(P["y"]))
    dx, dy = np.array(rx["dp"]), np.array(ry["dp"])
    lab.row("merger X (the bran twins): their price rise; rise in the Herfindahl index",
            f"{100 * dx[list(P['x'])].mean():.1f}%; {rx['dhhi']:.0f}")
    lab.row("merger Y (the two largest): their price rise; rise in the Herfindahl index",
            f"{100 * dy[list(P['y'])].mean():.1f}%; {ry['dhhi']:.0f}")
    assert dx[list(P["x"])].mean() > dy[list(P["y"])].mean() and rx["dhhi"] < ry["dhhi"]

    C = T["cars"]
    cars = io.island_cars(T=C["T"], firms=C["firms"], per_firm=C["per_firm"], alpha=C["alpha"], sigma=C["sigma"],
                          seed=C["seed"] + seed)
    n = len(cars["t"])
    out = np.zeros(n)
    for m in np.unique(cars["t"]):
        idx = cars["t"] == m
        out[idx] = 1 - cars["share"][idx].sum()
    X = np.column_stack([cars["size"], cars["power"]])
    Zd = io.diff_instruments(cars["t"], X)
    Z = np.column_stack([cars["w"], Zd, Zd ** 2 / 100, cars["w"] ** 2])
    ols = io.logit_ols(cars["share"], out, cars["price"], X)
    iv = io.logit_iv(cars["share"], out, cars["price"], X, Z)
    b = io.blp(cars["share"], cars["t"], cars["price"], X, Z, cars["nu"], bounds=(0.0, 0.6))
    lab.row("the Island's cars: alpha by OLS logit, IV logit (first-stage F), BLP; the truth",
            f"{ols['alpha']:.2f}, {iv['alpha']:.2f} ({iv['F']:.0f}), {b['alpha']:.2f}; {C['alpha']}")
    assert ols["alpha"] < iv["alpha"]

    d = {k: np.asarray(v) for k, v in data.blp_cars().items()}
    Xr = np.column_stack([d["hpwt"], d["air"], d["mpg"], d["space"]])
    Zr = io.blp_instruments(d["year"], d["firm"], Xr)
    for nm, r in (("OLS", io.logit_ols(d["share"], d["outshr"], d["price"], Xr)),
                  ("IV", io.logit_iv(d["share"], d["outshr"], d["price"], Xr, Zr))):
        e = io.own_elasticities_logit(r["alpha"], d["price"], d["share"])
        lab.row(f"BLP's 2,217 cars, plain logit by {nm}: alpha; models with inelastic demand",
                f"{r['alpha']:.4f}; {int(np.sum(np.abs(e) < 1)):,}")

    Ce = T["cereal"]
    rng = np.random.default_rng(Ce["seed"])
    J = len(Ce["owner"])
    base = rng.normal(Ce["base_mean"], Ce["base_sd"], J)
    mcc = np.exp(rng.normal(np.log(Ce["mc_median"]), Ce["mc_sd"], J))
    nu = np.random.default_rng(Ce["seed"] + 1).standard_normal(Ce["ns"])
    mk = io.RCMarket(base, Ce["alpha"], Ce["sigma"], nu)
    own = np.array(Ce["owner"])
    pc = mk.bertrand(mcc, own)
    im = io.implied_margins(mk.shares, pc, {"single": np.arange(J), "actual": own, "joint": np.zeros(J, int)})
    w = mk.shares(pc) / mk.shares(pc).sum()
    av = {k: float(np.sum(w * np.array(v))) for k, v in im.items()}
    true = float(np.sum(w * (pc - mcc) / pc))
    lab.row("Nevo's test on the Island's aisle: implied margins, single-product, real owners, cartel; the truth",
            f"{100 * av['single']:.0f}%, {100 * av['actual']:.0f}%, {100 * av['joint']:.0f}%; {100 * true:.0f}%")
    assert abs(av["actual"] - true) < 1e-6

    Pl = io.island_plants(**T["plants"])
    A = io.acf(Pl)
    lab.row("plants: labour and capital elasticities by OLS, by ACF; the truth",
            f"({A['ols']['bl']:.2f}, {A['ols']['bk']:.2f}), ({A['acf']['bl']:.2f}, {A['acf']['bk']:.2f}); "
            f"({T['plants']['bl']}, {T['plants']['bk']})")
    assert abs(A["acf"]["bl"] - T["plants"]["bl"]) < abs(A["ols"]["bl"] - T["plants"]["bl"])
    mu = T["dlw"]["median"] * np.exp(T["dlw"]["sd"] * np.random.default_rng(T["dlw"]["seed"]).standard_normal(2000))
    share = T["plants"]["bl"] / mu
    lab.row("markups from production data (median): with ACF's elasticity, with OLS's; the planted median",
            f"{np.median(A['acf']['bl'] / share):.2f}, {np.median(A['ols']['bl'] / share):.2f}; {T['dlw']['median']}")

    Tw = T["towns"]
    towns = io.island_towns(n=Tw["n"], F=Tw["F"], sd=Tw["sd"], seed=Tw["seed"] + seed, margins=Tw["margins"])
    est = io.ordered_thresholds(towns["pop"], towns["n"], n_max=len(Tw["margins"]))
    th = np.array(towns["thresholds"]) / np.arange(1, len(Tw["margins"]) + 1)
    lab.row("entry: ratios of per-firm thresholds, estimated; the truth",
            ", ".join(f"{x:.2f}" for x in est["ratio"]) + "; " + ", ".join(f"{x:.2f}" for x in th[1:] / th[:-1]))

    lab.note = ("Concentration and margins move together when costs differ, whatever the conduct. A merger's harm "
                "follows diversion between the merging products, not their size. Plain logit misreads demand even "
                "with good instruments, and random coefficients recover it. Markups follow from demand and ownership, "
                "or from a production function whose elasticity must be estimated with care.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].scatter(S["hhi"], S["pcm"], s=8, color=labs.BLUE)
    ax[0].set(title="300 Cournot industries", xlabel="Herfindahl index", ylabel="price-cost margin")
    xs = np.arange(1, len(est["ratio"]) + 1)
    ax[1].plot(xs, est["ratio"], "o-", color=labs.ORANGE, label="estimated")
    ax[1].plot(xs, th[1:] / th[:-1], "s--", color="grey", label="truth")
    ax[1].axhline(1.0, color="grey", lw=0.8)
    ax[1].set(title="entry thresholds", xlabel="entrant (2nd, 3rd, ...)", ylabel="ratio of per-firm thresholds")
    ax[1].legend()
    lab.fig = fig
    return lab
