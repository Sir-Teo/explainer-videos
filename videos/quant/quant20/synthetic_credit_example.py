"""Fixed synthetic classification lesson; no market labels, trials or envelopes.

All sample sizes, seeds, the data-generating law and learner settings were fixed
before this example was run. Independent samples illustrate selection and
assessment under one stationary invented population, not calendar forecasting.
Run: python -m videos.quant.quant20.synthetic_credit_example synthetic_credit_example
"""
from __future__ import annotations

import numpy as np
from scipy.special import expit
from explainer.ai.cache import Cache
from explainer.quant.house import credit as CR
from explainer.quant.house import termstructure as TS

CACHE = Cache("quant20")
FEATURES = ["WC/TA", "RE/TA", "EBIT/TA", "ME/TL", "Sales/TA", "NI/TA", "TL/TA",
            "Cash/TA", "CFO/TA", "logTA", "logME", "Int/TA"]
SAMPLES = {"fit": (8000, 202001), "selection": (4000, 202002), "evaluation": (6000, 202003)}


def population(n, seed):
    """Invented one-period binary events; ratios obey ME = TA*(TL/TA)*(ME/TL)."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n, 11))
    lev = 1.5 * expit(z[:, 0])
    profit = .08 + .1 * z[:, 1] - .06 * (lev - .75)
    wc = .1 + .2 * z[:, 2] - .15 * (lev - .75)
    re = .12 + .25 * z[:, 3] - .18 * (lev - .75)
    cushion = np.exp(.25 + .8 * z[:, 4] - .8 * (lev - .75))
    sales = np.exp(.3 + .5 * z[:, 5])
    ni = profit - .02 + .04 * z[:, 6]
    cash = .02 + .2 * expit(.6 * z[:, 7])
    cfo = profit + .06 * z[:, 8]
    log_ta = 20 + 1.5 * z[:, 9]
    log_me = log_ta + np.log(lev) + np.log(cushion)
    interest = .02 * lev + .01 * np.exp(.4 * z[:, 10])
    X = np.column_stack([wc, re, profit, cushion, sales, ni, lev, cash, cfo, log_ta, log_me, interest])
    eta = (-4.2 + 1.4 * (lev - .75) / .3 - (profit - .08) / .1 - .7 * np.log(cushion)
           + 1.6 * np.maximum((lev - .9) / .3, 0) * np.maximum((.06 - profit) / .1, 0))
    p = expit(eta)
    return X, rng.binomial(1, p), p


def fit_preprocessor(X):
    lo, hi = np.percentile(X, [1, 99], axis=0)
    Z = np.clip(X, lo, hi)
    return {"lo": lo, "hi": hi, "mean": Z.mean(0), "sd": Z.std(0)}


def transform(X, prep):
    return (np.clip(X, prep["lo"], prep["hi"]) - prep["mean"]) / prep["sd"]


def tied_roc(y, score):
    """Move every tied score together; trapezoidal area agrees with rank AUC."""
    y, score = np.asarray(y, bool), np.asarray(score, float)
    order = np.argsort(-score, kind="stable")
    ys, s = y[order], score[order]
    ends = np.r_[np.flatnonzero(s[:-1] != s[1:]), len(s) - 1]
    return np.r_[0, np.cumsum(~ys)[ends] / (~y).sum()], np.r_[0, np.cumsum(ys)[ends] / y.sum()]


def grouped_rates(x, y):
    groups = np.array_split(np.argsort(x, kind="stable"), 10)
    return {"rate": [float(y[g].mean()) for g in groups], "events": [int(y[g].sum()) for g in groups],
            "n": [len(g) for g in groups]}


def _json(x):
    if isinstance(x, dict): return {k: _json(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [_json(v) for v in x]
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, np.generic): return x.item()
    return x


def compute_example():
    xf, yf, _ = population(*SAMPLES["fit"])
    xs, ys, _ = population(*SAMPLES["selection"])
    prep = fit_preprocessor(xf)
    zf, zs = transform(xf, prep), transform(xs, prep)
    beta = CR.logit_fit(zf, yf, l2=1e-3)
    five = CR.logit_fit(zf[:, :5], yf, l2=1e-3)
    trees = CR.GBM(n_trees=240, depth=3, lr=.05, min_leaf=30, subsample=.8, seed=0)
    trees.fit(zf, yf, zs, ys, early_stop=30)
    # The evaluation sample is generated only after preprocessing and learner selection.
    xe, ye, oracle = population(*SAMPLES["evaluation"])
    ze = transform(xe, prep)
    results = {}
    eval_predictions = None
    for name, X, Z, y in [("fit", xf, zf, yf), ("selection", xs, zs, ys), ("evaluation", xe, ze, ye)]:
        pred = {"altman": -CR.altman_z(X[:, :5]), "logit": CR.logit_predict(beta, Z),
                "gbm": trees.predict_proba(Z), "five_ratio_logit": CR.logit_predict(five, Z[:, :5])}
        results[name] = {"n": len(y), "events": int(y.sum()), "rate": float(y.mean()),
                         "auc": {k: CR.auc(y, p) for k, p in pred.items()},
                         "brier": {k: CR.brier(y, pred[k]) for k in ("logit", "gbm")}}
        results[name]["brier"]["fit_base"] = CR.brier(y, np.full(len(y), yf.mean()))
        if name == "evaluation": eval_predictions = pred
    pred = eval_predictions
    groups = np.array_split(np.argsort(pred["gbm"], kind="stable"), 10)
    calibration = {"pred": [float(pred["gbm"][g].mean()) for g in groups],
                   "real": [float(ye[g].mean()) for g in groups], "n": [len(g) for g in groups],
                   "events": [int(ye[g].sum()) for g in groups]}
    z = CR.altman_z(xe[:, :5]); masks = [z < 1.81, (z >= 1.81) & (z < 2.99), z >= 2.99]
    zones = {"rate": [float(ye[g].mean()) for g in masks], "n": [int(g.sum()) for g in masks],
             "events": [int(ye[g].sum()) for g in masks]}
    q = np.linspace(.05, .95, 19)
    lev, cushion = np.quantile(xf[:, 6], q), np.quantile(xf[:, 3], q)
    raw = np.tile(np.median(xf, axis=0), (19 * 19, 1))
    raw[:, 6], raw[:, 3] = np.repeat(lev, 19), np.tile(cushion, 19)
    raw[:, 10] = raw[:, 9] + np.log(raw[:, 6]) + np.log(raw[:, 3])
    return _json({"scope": "Fixed synthetic one-period binary-event population; no real issuer forecasts or market validation",
                  "samples": SAMPLES, "features": FEATURES, "preprocessing": prep,
                  "results": results, "roc": {k: tied_roc(ye, pred[k]) for k in ("altman", "logit", "gbm")},
                  "calibration": calibration, "zones": zones, "five_ratio_beta": five[1:],
                  "logit_beta": beta, "gbm_importance": trees.importance(len(FEATURES)), "selected_trees": len(trees.trees),
                  "top_decile_capture": float(ye[groups[-1]].sum() / ye.sum()),
                  "sorts": {"base": float(yf.mean()), "leverage": grouped_rates(xf[:, 6], yf),
                            "profit": grouped_rates(xf[:, 2], yf), "altman": grouped_rates(CR.altman_z(xf[:, :5]), yf)},
                  "slice": {"q": q, "lev": lev, "cushion": cushion,
                            "gbm": trees.predict_proba(transform(raw, prep)).reshape(19, 19)},
                  "oracle_brier": CR.brier(ye, oracle)})


def rmv_curves():
    """Exact deterministic-rate CIR recovery-of-market-value discount factors.

    E[exp(-a*integral(lambda))] follows CIR with (lambda0,theta,sigma)
    scaled to (a*lambda0,a*theta,sqrt(a)*sigma); a = 1-R.
    """
    T = np.linspace(.25, 10, 40); k, theta, sigma, R = .5, .02, .1, .4
    a = 1 - R
    curves = {}
    for name, level in (("calm", .005), ("long run", .02), ("stressed", .08)):
        Q = TS.cir_zcb(level, k, theta, sigma, T)
        D = TS.cir_zcb(a * level, k, a * theta, np.sqrt(a) * sigma, T)
        curves[name] = {"l0": level, "Q": Q, "spread_bp": -np.log(D) / T * 1e4,
                        "legacy_approx_bp": -a * np.log(Q) / T * 1e4}
    return _json({"T": T, "curves": curves, "kappa": k, "theta": theta, "sigma": sigma, "R": R,
                  "scope": "Exact CIR RMV pricing example; original compute_cox unchanged"})


if __name__ == "__main__":
    CACHE.main({"synthetic_credit_example": compute_example, "rmv_credit_example": rmv_curves}, __doc__)
