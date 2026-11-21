"""Lab 54: estimating models: a logit by maximum likelihood and the value of time, a railway forecast against a
nested-logit truth, GMM on the Euler equation with the J-test, indirect inference against the naive estimator, hidden
types and spurious habit, a subsidy experiment predicted from control villages, and Manski's bounds."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import estimate as E
from explainer.economics.island import truths
from explainer.stats.kit import quasi

TITLE = "Estimating models"
GOAL = ("Estimate the hidden parameters of the Island's models from the choices they produce, with standard errors and "
        "tests, and check the estimates against the truth that was planted.")
TASKS = [
    "Set the nest's lambda to 1 (no correlation between bus and rail). Is the logit's railway forecast now right?",
    "Give the subsidy a label effect of 0.3 instead of 0.6. Does the prediction still fail at the 5% level?",
    "Shorten the moving-average samples to 100 periods. Does indirect inference still beat the naive estimator?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(54)

    C = T["commuters"]
    d = E.simulate_commuters(C["n"], C["beta"], C["asc"], C["seed"])
    r = E.logit_ml(d["X"], d["y"])
    b, cov = r["b"], r["cov"]
    vot = 60 * b[0] / b[1]
    grad = np.array([60 / b[1], -60 * b[0] / b[1] ** 2])
    lab.row("logit: minute, dollar, bus constant (standard errors)",
            ", ".join(f"{x:.3f} ({s:.3f})" for x, s in zip(b, r["se"])))
    lab.row("value of an hour (planted $7.20)", f"${vot:.2f} ({np.sqrt(grad @ cov[:2, :2] @ grad):.2f})")
    assert np.all(np.abs(b - np.array(list(C["beta"]) + [C["asc"][1]])) < 3 * r["se"])

    rail = C["rail"]
    n = d["X"].shape[0]
    Xr = np.concatenate([d["X"], np.tile([[[rail["time"], rail["cost"]]]], (n, 1, 1))], axis=1)
    V = Xr @ np.array(C["beta"]) + np.array([C["asc"][0], C["asc"][1], rail["asc"]])[None, :]
    truth = E.nested_shares(V, [[0], [1, 2]], [1.0, C["nest_lambda"]]).mean(axis=0)
    Vh = Xr @ b[:2] + np.array([0.0, b[2], rail["asc"]])[None, :]
    fc = E.nested_shares(Vh, [[0], [1, 2]], [1.0, 1.0]).mean(axis=0)
    lab.row("railway: car, bus, rail, truth", ", ".join(f"{x:.3f}" for x in truth))
    lab.row("railway: car, bus, rail, the logit's forecast", ", ".join(f"{x:.3f}" for x in fc))

    G = T["euler"]
    data = E.euler_data(T=G["T"], beta=G["beta"], gamma=G["gamma"], seed=G["seed"])
    g = E.gmm(E.euler_moments(data), [0.95, 2.0])
    lab.row("GMM: beta, gamma (planted 0.97, 3)", f"{g['theta'][0]:.4f} ({g['se'][0]:.4f}), "
            f"{g['theta'][1]:.3f} ({g['se'][1]:.3f})")
    lab.row("Hansen's J, degrees of freedom, p", f"{g['J']:.2f}, {g['df']}, {g['p_J']:.3f}")

    M = T["ma1"]
    naive, ii = [], []
    for k in range(100):
        y = E.ma1_data(M["theta"], M["n"], 5400 + k + 1000 * seed)
        o = E.indirect_ma1(y, seed=9000 + k)
        naive.append(o["naive"])
        ii.append(o["theta"])
    rm = [float(np.sqrt(np.mean((np.array(a) - M["theta"]) ** 2))) for a in (naive, ii)]
    lab.row("MA(1), 100 samples: error of the naive and indirect-inference estimates", f"{rm[0]:.3f}, {rm[1]:.3f}")

    Ty = T["types"]
    rng = np.random.default_rng(Ty["seed"])
    P, nt = Ty["people"], Ty["T"] + 1
    low = rng.random(P) < Ty["share_low"]
    alpha = np.where(low, Ty["alpha"][0], Ty["alpha"][1])
    grp = np.repeat(np.arange(P), nt)
    x = rng.standard_normal(P * nt)
    yy = (rng.random(P * nt) < 1 / (1 + np.exp(-(alpha[grp] + Ty["b"] * x)))).astype(float)
    lag = np.roll(yy, 1)
    keep = np.tile(np.arange(nt) > 0, P)
    pooled = E.pooled_logit(np.column_stack([x[keep], lag[keep]]), yy[keep])
    mix = E.mixture_logit_em(np.column_stack([x[keep], lag[keep]]), yy[keep], Ty["T"], grp[keep])
    lab.row("habit (planted 0): one logit for everyone; two hidden types", f"{pooled['b'][2]:.2f}; {mix['b'][1]:.2f}")

    S = T["school"]
    for name, effect in (("a peso is a peso", 0.0), ("the label matters", S["label_effect"])):
        v = E.validate_subsidy(E.school_villages(S["villages"], S["per"], subsidy=S["subsidy"], label_effect=effect,
                                                 seed=S["seed"]))
        lab.row(f"validation ({name}): predicted, experimental (s.e.)",
                f"{v['predicted_effect']:.3f}, {v['experimental_effect']:.3f} ({v['experimental_se']:.3f})")

    dd = E.school_villages(S["villages"], S["per"], subsidy=S["subsidy"], seed=S["seed"])
    rg = np.random.default_rng(S["seed"] + 2)
    pm = np.where(dd["y"] > 0, 0.6 * S["missing"], 1.5 * S["missing"])
    rec = rg.random(len(dd["y"])) >= pm
    mb = quasi.manski(dd["y"], dd["treated"], rec, 0.0, 1.0)
    lab.row("Manski's bounds on the effect, no assumption", f"[{mb['lo']:.3f}, {mb['hi']:.3f}]")

    lab.note = ("A model of why people choose can be asked about worlds nobody has seen; likelihood, moments and "
                "simulation estimate it; hidden types masquerade as habits; an experiment the model never saw is the "
                "strongest test, and bounds say what the data allow before any assumption.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    bins = np.linspace(-0.1, 1.0, 23)
    ax[0].hist(naive, bins, color=labs.PURPLE, alpha=0.5, label="first autocorrelation")
    ax[0].hist(ii, bins, color=labs.ORANGE, alpha=0.6, label="indirect inference")
    ax[0].axvline(M["theta"], color="white")
    ax[0].set(title="estimates of theta in 100 samples", xlabel="theta")
    ax[0].legend()
    dv = (d["X"][:, 1] - d["X"][:, 0]) @ b[:2] + b[2]
    edges = np.quantile(dv, np.linspace(0, 1, 13))
    mids = [dv[(dv >= lo) & (dv <= hi)].mean() for lo, hi in zip(edges[:-1], edges[1:])]
    obs = [(d["y"][(dv >= lo) & (dv <= hi)] == 1).mean() for lo, hi in zip(edges[:-1], edges[1:])]
    zs = np.linspace(edges[0], edges[-1], 100)
    ax[1].plot(zs, 1 / (1 + np.exp(-zs)), color=labs.PURPLE, label="the fitted logit")
    ax[1].plot(mids, obs, "o", color=labs.GREEN, label="commuters, in twelve groups")
    ax[1].set(title="the logit's curve", xlabel="how much better the bus looks")
    ax[1].legend()
    lab.fig = fig
    return lab
