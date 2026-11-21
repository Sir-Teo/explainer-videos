"""Agora's machines that learn (Part 64): prediction against judgement, the labels a decision hides, causal
estimation with machine learning, learned solutions and learning agents, measurement by classifier, and fairness.

* **The Island's bail courts** (:func:`courts`, :func:`policy_curves`, :func:`contraction`, :func:`cases`):
  defendants with records, a risk known to the simulation, judges of different leniency who also see something the
  records do not; a forest trained on the released predicts failure; the policy frontier against the judges', the
  contraction design that uses only observed outcomes (after Kleinberg, Lakkaraju, Leskovec, Ludwig and
  Mullainathan), and the selective-labels bias of a naive evaluation.
* **Prediction is not causation** (:func:`targeting`): a job programme for a fifth of the unemployed, targeted at
  the highest risk, at the largest effect, or at the effect a causal forest estimates from a trial.
* **Double machine learning** (:func:`dml_study`): the partially linear model with nonlinear confounding; OLS with
  linear controls, a plug-in machine-learning estimator, and cross-fitted residual-on-residual (Chernozhukov et al.).
* **Text as data** (:func:`text_measure`): the share of news about layoffs measured by a classifier, by a small
  hand-labelled sample, and by prediction-powered inference.
* **A learned solution** (:func:`euler_net`): the growth model's saving rule as a small neural network trained on
  Euler-equation errors with the series' own automatic differentiation, against Brock and Mirman's closed form.
* **Learning agents** (:func:`pricing_agents`): Part 44's Q-learning price setters, several sessions.
* **Fairness** (:func:`fairness`): a calibrated score for two groups with different base rates; error rates by group
  and Chouldechova's identity.

numpy and scipy only (with statkit's forests, causal forest and PPI, and ``explainer.ai.autodiff``).
"""

from __future__ import annotations

import numpy as np

from explainer.stats.kit import causal as KC
from explainer.stats.kit import conformal as CF
from explainer.stats.kit import ppi as PPI

FEATURES = ("age", "priors", "missed", "charge", "employed")
CHARGES = ("minor", "property", "drugs", "violent")


def _sigmoid(z):
    return 1 / (1 + np.exp(-z))


# ---------------------------------------------------------------------------------------------------------------
# the Island's bail courts


def defendants(n: int = 40000, seed: int = 64, signal: float = 0.45) -> dict:
    """The Island's arrested: age, prior arrests, past missed court dates, the charge, a job; a signal s that the
    judge sees in court and the records do not (demeanour, a family in the gallery); and the true chance of failing
    to appear if released, which depends nonlinearly on the records and a little on s."""
    rng = np.random.default_rng(seed)
    age = rng.integers(18, 61, n)
    lam = 0.4 + 2.2 * np.exp(-(age - 18) / 12)
    priors = rng.poisson(lam)
    missed = rng.binomial(np.minimum(priors, 6), 0.3)
    charge = rng.choice(4, n, p=[0.35, 0.30, 0.20, 0.15])
    employed = (rng.random(n) < 0.40 + 0.25 * (age > 25)).astype(int)
    s = rng.normal(0, 1, n)
    z = (-2.35 + 0.55 * np.log1p(priors) + 0.65 * np.minimum(missed, 3) + 0.55 * (age < 23)
         + 0.45 * (age < 23) * (priors >= 2) - 0.45 * employed + 0.25 * (charge == 2) - 0.25 * (charge == 3)
         + signal * s)
    p = _sigmoid(z)
    y = (rng.random(n) < p).astype(int)               # what each would do if released
    X = np.c_[age, priors, missed, charge, employed].astype(float)
    return {"X": X, "s": s, "p": p, "y": y}


def courts(n: int = 40000, judges: int = 50, seed: int = 64, trees: int = 80, signal: float = 0.45) -> dict:
    """Cases assigned at random to judges whose release rates run from 55% to 88%.  A judge ranks defendants by a
    risk index that overweights the charge, misreads youth and priors, uses the courtroom signal, and adds noise of
    its own, and releases the lowest-risk share.  Failures are seen only for the released.  A random forest is
    trained on half the released and scores everyone in the other half (the test set)."""
    rng = np.random.default_rng(seed + 1)
    D = defendants(n, seed, signal)
    X, s, p, y = D["X"], D["s"], D["p"], D["y"]
    judge = rng.integers(0, judges, n)
    rate = np.linspace(0.55, 0.88, judges)[rng.permutation(judges)]
    index = (0.35 * X[:, 1] + 0.30 * X[:, 2] + 0.55 * X[:, 3] - 0.20 * X[:, 4] + signal * s
             + rng.normal(0, 0.7, n))
    released = np.zeros(n, bool)
    for j in range(judges):
        idx = np.flatnonzero(judge == j)
        cut = np.quantile(index[idx], rate[j])
        released[idx] = index[idx] <= cut
    test = rng.random(n) < 0.5
    train = ~test & released
    forest = CF.Forest(X[train], y[train].astype(float), B=trees, min_leaf=40, rng=rng)
    risk = np.full(n, np.nan)
    risk[test] = forest.predict(X[test])
    return {"X": X, "s": s, "p": p, "y": y, "judge": judge, "rate": rate, "released": released, "test": test,
            "risk": risk, "n_train": int(train.sum())}


def policy_curves(C: dict, grid=None) -> dict:
    """On the test set, with the truth the simulation knows: failures per defendant if the algorithm detains the
    highest-risk share d, against the judges' own (detention rate, failure rate), overall and by leniency quintile.
    The headline: the algorithm's failures at the judges' detention rate, and the detention it needs to match the
    judges' failures."""
    t = C["test"]
    y, risk, rel = C["y"][t], C["risk"][t], C["released"][t]
    grid = np.linspace(0, 0.6, 61) if grid is None else np.asarray(grid)
    order = np.argsort(-risk)
    n = len(y)
    crime = []
    for d in grid:
        det = np.zeros(n, bool)
        det[order[:int(round(d * n))]] = True
        crime.append(float(y[~det].sum() / n))
    crime = np.array(crime)
    dj, cj = float(1 - rel.mean()), float(y[rel].sum() / n)
    alg_at_dj = float(np.interp(dj, grid, crime))
    d_at_cj = float(np.interp(-cj, -crime, grid))      # crime falls as detention rises
    jr = C["rate"][C["judge"][t]]
    q = np.quantile(jr, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
    quint = []
    for k in range(5):
        m = (jr >= q[k]) & (jr <= q[k + 1] if k == 4 else jr < q[k + 1])
        quint.append({"detain": float(1 - rel[m].mean()), "crime": float(y[m & rel].sum() / m.sum())})
    return {"grid": grid.tolist(), "crime": crime.tolist(), "judges": {"detain": dj, "crime": cj},
            "quintiles": quint, "alg_at_judges": alg_at_dj, "crime_cut": 1 - alg_at_dj / cj,
            "detain_at_judges_crime": d_at_cj, "detain_cut": 1 - d_at_cj / dj, "base": float(y.mean())}


def contraction(C: dict) -> dict:
    """Lakkaraju et al.'s contraction: take the most lenient fifth of judges; among the defendants they released,
    the algorithm detains more, highest predicted risk first, until it matches each stricter quintile's detention
    rate; its failure rate uses only outcomes that were observed.  Compared with the stricter judges' own failure
    rate, and with the truth.  Also the naive evaluation that fills in the detained defendants' outcomes with the
    algorithm's own predictions, which the courtroom signal makes too optimistic."""
    t = C["test"]
    jr = C["rate"][C["judge"][t]]
    y, risk, rel, p = C["y"][t], C["risk"][t], C["released"][t], C["p"][t]
    q = np.quantile(jr, [0.2, 0.4, 0.6, 0.8])
    lenient = jr >= q[3]
    n_l = lenient.sum()
    rows = []
    for k, lo, hi in ((0, None, q[0]), (1, q[0], q[1]), (2, q[1], q[2]), (3, q[2], q[3])):
        m = (jr < hi) & (jr >= lo if lo is not None else True)
        d_target = 1 - rel[m].mean()
        judge_crime = y[m & rel].sum() / m.sum()
        cand = np.flatnonzero(lenient & rel)
        extra = int(round(d_target * n_l)) - int((lenient & ~rel).sum())
        keep = np.ones(len(cand), bool)
        if extra > 0:
            keep[np.argsort(-risk[cand])[:extra]] = False
        alg_crime = y[cand[keep]].sum() / n_l
        rows.append({"detain": float(d_target), "judges": float(judge_crime), "algorithm": float(alg_crime)})
    # the naive evaluation at the judges' overall detention rate
    n = len(y)
    dj = 1 - rel.mean()
    det = np.zeros(n, bool)
    det[np.argsort(-risk)[:int(round(dj * n))]] = True
    filled = np.where(rel, y, risk)
    naive = float(filled[~det].sum() / n)
    truth = float(y[~det].sum() / n)
    # the released and the detained with the same record: the courtroom signal
    s = C["s"][t]
    return {"rows": rows, "naive": naive, "truth": truth, "s_released": float(s[rel].mean()),
            "s_detained": float(s[~rel].mean()), "p_detained": float(p[~rel].mean()),
            "risk_detained": float(np.nanmean(risk[~rel]))}


def cases(C: dict, targets=(0.05, 0.07, 0.09, 0.12, 0.15, 0.19, 0.24, 0.31, 0.39, 0.48), seed: int = 640) -> dict:
    """Ten test-set defendants whose predicted risks are near ``targets``, shuffled, for the Play-it: their records,
    the judge's decision, the algorithm's risk, the true chance of failing to appear (which the Island knows), and
    what each would have done if released."""
    rng = np.random.default_rng(seed)
    t = np.flatnonzero(C["test"])
    r = C["risk"][t]
    used, picks = set(), []
    for x in targets:
        for j in np.argsort(np.abs(r - x)):
            if t[j] not in used:
                used.add(t[j])
                picks.append(int(t[j]))
                break
    picks = rng.permutation(picks)
    rows = []
    for i in picks:
        a, pr, ms, ch, em = C["X"][i]
        rows.append({"age": int(a), "priors": int(pr), "missed": int(ms), "charge": CHARGES[int(ch)],
                     "employed": bool(em), "released": bool(C["released"][i]), "risk": float(C["risk"][i]),
                     "p": float(C["p"][i]), "y": int(C["y"][i])})
    return {"rows": rows}


def signal_sweep(signals=(0.0, 0.45, 0.9, 1.35, 1.8), n: int = 30000, seed: int = 64) -> dict:
    """How much the algorithm adds as the judges' courtroom signal grows more informative: for each strength (the
    signal's weight in both the true risk and the judges' index), the fall in failures at the judges' detention rate
    when cases are ranked by the forest, which sees only the records, and the fall in detention at their failure
    rate.  Negative values: the judges do better."""
    rows = []
    for w in signals:
        C = courts(n=n, seed=seed, signal=w, trees=50)
        P = policy_curves(C)
        rows.append({"signal": float(w), "crime_cut": float(P["crime_cut"]), "detain_cut": float(P["detain_cut"])})
    return {"rows": rows}


# ---------------------------------------------------------------------------------------------------------------
# prediction is not causation


def targeting(n: int = 20000, budget: float = 0.2, trial: int = 4000, seed: int = 64) -> dict:
    """A job programme for a fifth of the Island's unemployed.  Each person's chance of still being unemployed in a
    year without it, p0(x), and the programme's effect tau(x): largest for people in the middle of the risk range,
    small for those who would find work anyway and for those far from any job.  Unemployment averted per 100 people
    treated when the places go to the highest risk, to the largest true effect, to the largest effect a causal forest
    estimates from a randomized trial, or at random."""
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (n, 5))
    p0 = _sigmoid(-0.4 + 1.3 * X[:, 0] + 0.6 * X[:, 1] - 0.4 * X[:, 2])
    tau = 0.30 * np.exp(-((p0 - 0.5) / 0.25) ** 2) * (1 + 0.4 * np.tanh(X[:, 3]))
    k = int(budget * n)
    out = {}
    out["highest risk"] = float(tau[np.argsort(-p0)[:k]].mean())
    out["largest effect (truth)"] = float(tau[np.argsort(-tau)[:k]].mean())
    out["at random"] = float(tau.mean())
    # a randomized trial on a separate sample, and a causal forest
    Xt = rng.normal(0, 1, (trial, 5))
    p0t = _sigmoid(-0.4 + 1.3 * Xt[:, 0] + 0.6 * Xt[:, 1] - 0.4 * Xt[:, 2])
    taut = 0.30 * np.exp(-((p0t - 0.5) / 0.25) ** 2) * (1 + 0.4 * np.tanh(Xt[:, 3]))
    d = rng.random(trial) < 0.5
    yt = (rng.random(trial) < p0t - d * taut).astype(float)
    cf = KC.CausalForest(Xt, yt, d.astype(float), B=100, min_leaf=30, rng=rng)
    est = -cf.predict(X)
    out["largest effect (estimated)"] = float(tau[np.argsort(-est)[:k]].mean())
    shares = np.round(np.linspace(0.05, 0.6, 12), 3)
    curves = {"highest risk": np.argsort(-p0), "largest effect (estimated)": np.argsort(-est),
              "largest effect (truth)": np.argsort(-tau)}
    averted = {k: [float(tau[o[:int(b * n)]].sum() / n * 100) for b in shares] for k, o in curves.items()}
    averted["at random"] = [float(tau.mean() * b * 100) for b in shares]
    est_by = [float(est[(p0 >= a) & (p0 < b)].mean()) if ((p0 >= a) & (p0 < b)).any() else 0.0
              for a, b in zip(np.linspace(0, 1, 11)[:-1], np.linspace(0, 1, 11)[1:])]
    corr = float(np.corrcoef(p0, tau)[0, 1])
    bins = np.linspace(0, 1, 11)
    mid = (bins[:-1] + bins[1:]) / 2
    by = [float(tau[(p0 >= a) & (p0 < b)].mean()) if ((p0 >= a) & (p0 < b)).any() else 0.0
          for a, b in zip(bins[:-1], bins[1:])]
    return {"per100": {k_: 100 * v for k_, v in out.items()}, "corr": corr, "risk_bins": mid.tolist(),
            "effect_by_risk": by, "estimate_by_risk": est_by, "budget": budget, "trial": trial,
            "shares": shares.tolist(), "averted": averted}


# ---------------------------------------------------------------------------------------------------------------
# double machine learning


def _dml_data(n, rng, theta=1.0):
    X = rng.normal(0, 1, (n, 5))
    m = 0.8 * np.tanh(2 * X[:, 0]) + 0.5 * X[:, 1] * X[:, 2] + 0.3 * (X[:, 3] > 0)
    g = 1.5 * np.sin(2 * X[:, 0]) + 0.8 * X[:, 1] * X[:, 2] + 0.6 * (X[:, 3] > 0.5) + 0.3 * X[:, 4] ** 2
    d = m + rng.normal(0, 1, n)
    y = theta * d + g + rng.normal(0, 1, n)
    return X, d, y


def _boost_fit(Xtr, ytr, Xte):
    """Gradient boosting: 250 trees of depth 3, learning rate 0.1 (statkit's L2 boosting)."""
    return CF.l2_boost(Xtr, ytr, M=250, nu=0.1, depth=3, min_leaf=10, Xtest=Xte, ytest=np.zeros(len(Xte)))["pred"]


def dml_study(n: int = 1500, reps: int = 50, theta: float = 1.0, K: int = 3, seed: int = 64) -> dict:
    """Monte Carlo of the partially linear model y = theta d + g(X) + e, d = m(X) + v, with g and m nonlinear and
    sharing their first variables: OLS of y on d alone; OLS with the five controls entered linearly; a plug-in
    machine-learning estimator that partials boosting's g out of y but never m out of d; and cross-fitted double
    machine learning (residual on residual, K folds, gradient boosting).  Bias, spread, and the coverage of 90%
    intervals."""
    rng = np.random.default_rng(seed)
    est = {k: [] for k in ("no controls", "linear controls", "plug-in ML", "double ML")}
    cover = []
    for _ in range(reps):
        X, d, y = _dml_data(n, rng, theta)
        est["no controls"].append(float(np.polyfit(d, y, 1)[0]))
        Z = np.c_[np.ones(n), d, X]
        est["linear controls"].append(float(np.linalg.lstsq(Z, y, rcond=None)[0][1]))
        th = est["linear controls"][-1]
        half = rng.random(n) < 0.5
        for _ in range(2):
            ghat = np.zeros(n)
            ghat[~half] = _boost_fit(X[half], (y - th * d)[half], X[~half])
            ghat[half] = _boost_fit(X[~half], (y - th * d)[~half], X[half])
            th = float(np.sum(d * (y - ghat)) / np.sum(d * d))
        est["plug-in ML"].append(th)
        r = KC.dml_plr(y, d, X, _boost_fit, K=K, rng=rng, alpha=0.1)
        est["double ML"].append(r["est"])
        cover.append(bool(r["lo"] <= theta <= r["hi"]))
    out = {"theta": theta, "n": n, "reps": reps, "coverage": float(np.mean(cover)), "folds": K}
    for k, v in est.items():
        v = np.array(v)
        out[k] = {"mean": float(v.mean()), "sd": float(v.std()), "draws": v.tolist()}
    return out


# ---------------------------------------------------------------------------------------------------------------
# text as data


def text_measure(N: int = 20000, labelled: int = 400, share: float = 0.12, sens: float = 0.90, spec: float = 0.96,
                 reps: int = 500, seed: int = 64) -> dict:
    """The share of the Island's news articles about layoffs.  A classifier labels all N with sensitivity and
    specificity below one; a small random sample is labelled by hand.  The classifier's share, the hand-labelled
    sample's mean, and prediction-powered inference (the classifier's share corrected by its average error on the
    labelled sample), with the coverage of their 90% intervals over many corpora."""
    rng = np.random.default_rng(seed)
    res = {k: {"est": [], "cover": [], "width": []} for k in ("classifier", "hand-labelled", "prediction-powered")}
    for _ in range(reps):
        y = (rng.random(N) < share).astype(float)
        f = np.where(y == 1, rng.random(N) < sens, rng.random(N) > spec).astype(float)
        lab = rng.choice(N, labelled, replace=False)
        unl = np.setdiff1d(np.arange(N), lab)
        truth = y.mean()
        for k, r in (("classifier", PPI.naive_mean(f, alpha=0.1)), ("hand-labelled", PPI.classical_mean(y[lab],
                                                                                                         alpha=0.1)),
                     ("prediction-powered", PPI.ppi_mean(y[lab], f[lab], f[unl], alpha=0.1))):
            lo, hi = r["lo"], r["hi"]
            res[k]["est"].append(float(r["est"]))
            res[k]["cover"].append(bool(lo <= truth <= hi))
            res[k]["width"].append(float(hi - lo))
    out = {"share": share, "N": N, "labelled": labelled, "sens": sens, "spec": spec}
    for k, v in res.items():
        out[k] = {"mean": float(np.mean(v["est"])), "sd": float(np.std(v["est"])),
                  "coverage": float(np.mean(v["cover"])), "width": float(np.mean(v["width"])),
                  "draws": v["est"][:200]}
    return out


# ---------------------------------------------------------------------------------------------------------------
# a learned solution


def euler_net(alpha: float = 0.33, beta: float = 0.95, hidden: int = 12, steps: int = 3000, lr: float = 0.05,
              seed: int = 64) -> dict:
    """The deterministic growth model with log utility and full depreciation: output k^alpha is split between
    consumption and next year's capital, k' = s(k) k^alpha.  The saving rate s(k) is a one-hidden-layer network
    (tanh units, a sigmoid output) trained by gradient descent with the series' automatic differentiation to make the
    Euler equation 1/c = beta alpha k'^(alpha - 1)/c' hold on a grid of capital stocks.  Brock and Mirman's closed
    form: s = alpha beta, whatever k."""
    from explainer.ai.autodiff import Tensor, sigmoid

    rng = np.random.default_rng(seed)
    kss = (alpha * beta) ** (1 / (1 - alpha))
    grid = np.linspace(0.2 * kss, 2.5 * kss, 64)[:, None]
    x0 = (grid - kss) / kss
    W1 = Tensor(rng.normal(0, 0.8, (1, hidden)), requires_grad=True)
    b1 = Tensor(np.zeros((1, hidden)), requires_grad=True)
    W2 = Tensor(rng.normal(0, 0.3, (hidden, 1)), requires_grad=True)
    b2 = Tensor(np.zeros((1, 1)), requires_grad=True)
    params = (W1, b1, W2, b2)

    def srate(xn):
        return sigmoid(((Tensor(xn) @ W1 + b1).tanh()) @ W2 + b2)

    losses, snaps = [], []
    m_ = [np.zeros_like(p.data) for p in params]
    v_ = [np.zeros_like(p.data) for p in params]
    for it in range(steps):
        for p in params:
            p.grad = np.zeros_like(p.data)
        k = Tensor(grid)
        y = k ** alpha
        s = srate(x0)
        k1 = s * y
        c = y - k1
        x1 = (k1 - kss) / kss
        s1 = srate(x1.data)                    # next period's rule, held fixed within a step
        y1 = k1 ** alpha
        c1 = y1 - s1 * y1
        resid = (c * (k1 ** (alpha - 1)) * (beta * alpha)) / c1 - 1.0
        loss = (resid * resid).mean()
        loss.backward()
        for j, p in enumerate(params):          # Adam
            m_[j] = 0.9 * m_[j] + 0.1 * p.grad
            v_[j] = 0.999 * v_[j] + 0.001 * p.grad ** 2
            mh, vh = m_[j] / (1 - 0.9 ** (it + 1)), v_[j] / (1 - 0.999 ** (it + 1))
            p.data -= lr * mh / (np.sqrt(vh) + 1e-8)
        losses.append(float(loss.data))
        if it in (0, 50, 200, steps - 1):
            snaps.append({"step": it, "s": srate(x0).data.ravel().tolist()})
    s_final = srate(x0).data.ravel()
    return {"k": grid.ravel().tolist(), "kss": float(kss), "s": s_final.tolist(), "exact": alpha * beta,
            "loss": losses, "snaps": snaps, "max_err": float(np.max(np.abs(s_final - alpha * beta))),
            "alpha": alpha, "beta": beta}


# ---------------------------------------------------------------------------------------------------------------
# learning agents


def pricing_agents(sessions: int = 8, beta: float = 2e-5, seed: int = 0) -> dict:
    """Part 44's two Q-learning price setters (Calvano, Calzolari, Denicolo and Pastorello's design) run for several
    sessions with a faster decline of exploration: the prices they settle on, and the profit gain (0 at the
    competitive Nash price, 1 at the monopoly price)."""
    from explainer.economics.agora import io

    rows = []
    for s in range(sessions):
        r = io.q_learning(beta=beta, max_iter=800_000, stable=50_000, seed=seed + s)
        rows.append({"prices": [float(x) for x in r["prices"]], "gain": float(r["gain"]),
                     "iterations": int(r["iterations"])})
    r0 = io.q_learning(beta=beta, max_iter=800_000, stable=50_000, seed=seed)
    return {"rows": rows, "nash": float(np.ravel(r0["nash"])[0]), "monopoly": float(np.ravel(r0["monopoly"])[0]),
            "mean_gain": float(np.mean([x["gain"] for x in rows]))}


# ---------------------------------------------------------------------------------------------------------------
# fairness


def fairness(n: int = 200000, threshold: float = 0.3, seed: int = 64) -> dict:
    """Two groups of the Island's defendants whose risks differ on average (group B's records reflect heavier
    policing of its neighbourhoods).  The score is each person's true risk, so it is perfectly calibrated within each
    group; detain above a threshold.  The false positive rate, false negative rate and positive predictive value by
    group, and Chouldechova's identity FPR = p/(1 - p) (1 - PPV)/PPV (1 - FNR), which forces unequal error rates when
    base rates differ and PPVs are equal-ish."""
    rng = np.random.default_rng(seed)
    out = {}
    for g, shift in (("A", -0.35), ("B", 0.35)):
        z = rng.normal(-1.0 + shift, 0.9, n)
        p = _sigmoid(z)
        y = rng.random(n) < p
        det = p > threshold
        fpr = float((det & ~y).sum() / (~y).sum())
        fnr = float((~det & y).sum() / y.sum())
        ppv = float((det & y).sum() / det.sum())
        base = float(y.mean())
        ident = base / (1 - base) * (1 - ppv) / ppv * (1 - fnr)
        bins = np.linspace(0, 1, 11)
        cal = [float(y[(p >= a) & (p < b)].mean()) if ((p >= a) & (p < b)).sum() > 50 else None
               for a, b in zip(bins[:-1], bins[1:])]
        out[g] = {"base": base, "fpr": fpr, "fnr": fnr, "ppv": ppv, "detained": float(det.mean()),
                  "identity": float(ident), "calibration": cal}
    out["threshold"] = threshold
    return out


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "annotations", "KC", "CF", "PPI")]
