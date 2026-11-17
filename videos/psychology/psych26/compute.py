"""Precompute every number in Part 26 of *Psychology, Built* ("Judgment and Choice").

    python -m videos.psychology.psych26.compute            # everything missing (a few minutes; fetches data once)
    python -m videos.psychology.psych26.compute --force c13k

Results are cached in ``.cache/psych26/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.choice``, with Part 25's ``decide`` for the one-process account of "two
systems").  The data are choices13k (Peterson, Bourgin, Agrawal, Reichman and Griffiths 2021), fetched by
``explainer.psychology.opendata``.  Simulations use fixed seeds; where a part shows one run of many, it is the run
of median outcome, chosen by rule.  Money is in the units of each problem (dollars, or the data's points).

Items:
    framing      the disease problem valued by prospect theory in both frames; the published splits
    stpete       the St Petersburg game: expected value by cut-off, a long run of plays (the median of 101 runs),
                 Bernoulli's buying price against wealth
    allais       Kahneman and Tversky's Allais problems in the probability triangle with expected utility's
                 parallel indifference lines
    curves       the value and weighting functions: 1992 parameters
    fourfold     certainty equivalents for gains and losses at probabilities 0.01 to 0.99; Kahneman and
                 Tversky's 1979 problems valued
    c13k         choices13k's described problems: four models fitted, cross-validated, the fitted curves,
                 predictions against data; the feedback problems fitted separately
    bayes        the cab problem and the mammography problem in probabilities and in natural frequencies
    ttb          take-the-best, tallying and regression out of sample in two simulated worlds
    hothand      the streak statistic's expectation by exact enumeration (n = 4 in full, n = 3..20), and by
                 simulation at 100 shots
    time         exponential, hyperbolic and beta-delta discounting; the reversal of 100 sooner against 110 later
    experience   the chance a rare event is never seen; choices from seven draws against prospect theory's
    systems      a diffusion process with a start near the intuitive answer: answers by response-time quintile
    sampling     decision by sampling: value as rank among remembered credits and debits
    rational     anchoring as resource-rational adjustment: bias after k steps, the best k for two costs of time
    calibration  a judge calibrated to its world, asked questions drawn at random and questions chosen because the
                 cue misleads (Gigerenzer et al. 1991; Juslin 1994): proportion correct by stated confidence
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import choice as C

CACHE = Cache("psych26")
load = CACHE.load


def compute_framing() -> dict:
    f = C.framing()
    return {**{k: v for k, v in f.items() if isinstance(v, float)},
            "saved_choice": f["saved_choice"], "die_choice": f["die_choice"],
            # Tversky and Kahneman (1981), Problems 1 and 2
            "n_saved": 152, "saved_sure_pct": 72, "n_die": 155, "die_sure_pct": 22}


def compute_stpete() -> dict:
    cut = C.st_petersburg_ev(30)
    wealth = np.array([10, 100, 1_000, 10_000, 100_000, 1_000_000], float)
    price = np.array([C.st_petersburg_ce(w) for w in wealth])
    rng = np.random.default_rng(26)
    n = 100_000
    finals, runs = [], []
    for _ in range(101):
        k = rng.geometric(0.5, n)  # the toss of the first head
        avg = np.cumsum(2.0 ** k) / np.arange(1, n + 1)
        runs.append(avg)
        finals.append(avg[-1])
    med = runs[int(np.argsort(finals, kind="stable")[50])]
    marks = np.unique(np.round(np.logspace(0, 5, 200)).astype(int)) - 1
    return {"cut": cut, "wealth": wealth, "price": price, "plays": marks + 1, "avg": med[marks],
            "final_median": float(np.median(finals)), "log2_n": float(np.log2(n))}


def compute_allais() -> dict:
    out = (0.0, 2400.0, 2500.0)
    lots = {"A": C.lottery((0.33, 2500), (0.66, 2400), (0.01, 0)), "B": C.lottery((1.0, 2400)),
            "C": C.lottery((0.33, 2500), (0.67, 0)), "D": C.lottery((0.34, 2400), (0.66, 0))}
    pts = {k: C.triangle(L, out) for k, L in lots.items()}
    slope = C.eu_slope(0.0, 1.0, 1.5)  # an illustrative utility: u(0) = 0, u(2400) = 1, u(2500) = 1.5
    # prospect theory's verdicts on both pairs
    pt = {k: C.cpt(L) for k, L in lots.items()}
    return {"pts": {k: list(v) for k, v in pts.items()}, "slope": slope,
            "ev": {k: C.ev(L) for k, L in lots.items()}, "pt": pt,
            "pt_pair1": "B" if pt["B"] > pt["A"] else "A", "pt_pair2": "C" if pt["C"] > pt["D"] else "D",
            # Kahneman and Tversky (1979), Problems 1 and 2: N = 72 each
            "n": 72, "pct": {"A": 18, "B": 82, "C": 83, "D": 17}}


def compute_curves() -> dict:
    x = np.linspace(-100, 100, 401)
    p = np.linspace(0, 1, 201)
    return {"x": x, "v": C.value(x), "p": p, "w_gain": C.w_tk(p, 0.61), "w_loss": C.w_tk(p, 0.69),
            "w_prelec": C.w_prelec(p, 0.65), "lam": 2.25,
            "loss_100": float(-C.value(-100.0)), "gain_100": float(C.value(100.0)),
            "mixed_ce": float(C.ce(C.lottery((0.5, 100), (0.5, -100)))),
            # the gain that makes a 50-50 bet against losing 100 acceptable under the 1992 values
            "break_even": float(_break_even())}


def _break_even() -> float:
    from scipy.optimize import brentq
    return brentq(lambda g: C.cpt(C.lottery((0.5, g), (0.5, -100.0))), 100.0, 1000.0)


def compute_fourfold() -> dict:
    f = C.fourfold(probs=(0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99))
    cells = C.fourfold(probs=(0.05, 0.95))
    kt = {"P3": (C.lottery((0.8, 4000), (0.2, 0)), C.lottery((1.0, 3000))),
          "P4": (C.lottery((0.2, 4000), (0.8, 0)), C.lottery((0.25, 3000), (0.75, 0))),
          "P3neg": (C.lottery((0.8, -4000), (0.2, 0)), C.lottery((1.0, -3000)))}
    verdict = {k: "risky" if C.cpt(a) > C.cpt(b) else "other" for k, (a, b) in kt.items()}
    return {**f, "cell_p": cells["p"], "cell_gain": cells["gain_ce"], "cell_loss": cells["loss_ce"],
            "kt_verdict": verdict,
            # Kahneman and Tversky (1979): percent choosing the riskier option, and N
            "kt_pct": {"P3": 20, "P4": 65, "P3neg": 92}, "kt_n": {"P3": 95, "P4": 95, "P3neg": 95}}


def _c13k_sets():
    d = opendata.choices13k()
    unamb = ~d["amb"]
    desc = np.where(unamb & ~d["feedback"])[0]
    fb = np.where(unamb & d["feedback"])[0]
    return d, desc, fb


def compute_c13k() -> dict:
    d, desc, fb = _c13k_sets()
    A = C.pad([d["A"][i] for i in desc])
    B = C.pad([d["B"][i] for i in desc])
    y = d["b_rate"][desc]
    fits = {m: C.fit_model(m, A, B, y) for m in C.MODELS}
    cv = C.cv_models(A, B, y, k=10, seed=26)
    pred_cpt = C.predict("cpt", fits["cpt"]["theta"], A, B)
    pred_ev = C.predict("ev", fits["ev"]["theta"], A, B)
    pc = fits["cpt"]["params"]
    x = np.linspace(-100, 100, 401)
    p = np.linspace(0, 1, 201)
    # the feedback problems, fitted the same way
    Af = C.pad([d["A"][i] for i in fb])
    Bf = C.pad([d["B"][i] for i in fb])
    fit_fb = C.fit_model("cpt", Af, Bf, d["b_rate"][fb])
    # problems seen both without and with feedback: does feedback move choices of rare-outcome options?
    first = {}
    for i in desc:
        first[d["problem"][i]] = i
    pairs = []
    for i in fb:
        j = first.get(d["problem"][i])
        if j is not None:
            pairs.append((j, i))
    pairs = np.array(pairs)
    rare_dir = []
    for j, i in pairs:
        L = d["B"][j]
        L = L[L[:, 0] > 0]
        a = d["A"][j]
        a = a[a[:, 0] > 0]
        if len(a) != 1 or len(L) != 2 or L[:, 0].min() > 0.1:
            rare_dir.append(0)
            continue
        good = L[np.argmin(L[:, 0]), 1] > L[np.argmax(L[:, 0]), 1]
        rare_dir.append(1 if good else -1)
    rare_dir = np.array(rare_dir)
    delta = d["b_rate"][pairs[:, 1]] - d["b_rate"][pairs[:, 0]]
    return {"n_problems": int(len(desc)), "n_people_problems": int(d["n"][desc].sum()),
            "n_rows": int(len(d["b_rate"])), "n_unique": int(len(np.unique(d["problem"]))),
            "n_feedback": int(len(fb)), "var": float(y.var()),
            "mse": {m: f["mse"] for m, f in fits.items()}, "cv": cv,
            "r2": {m: 1 - f["mse"] / float(y.var()) for m, f in fits.items()},
            "params": {m: f["params"] for m, f in fits.items()},
            "y": y, "pred_cpt": pred_cpt, "pred_ev": pred_ev,
            "x": x, "v_fit": C.value(x, pc["alpha"], pc["alpha"], pc["lam"]), "v_92": C.value(x),
            "p": p, "w_fit_gain": C.w_tk(p, pc["gamma"]), "w_fit_loss": C.w_tk(p, pc["delta"]),
            "w_92_gain": C.w_tk(p, 0.61), "fb_params": fit_fb["params"], "fb_mse": fit_fb["mse"],
            "w_fb_gain": C.w_tk(p, fit_fb["params"]["gamma"]),
            "pairs": int(len(pairs)),
            "rare_good_n": int((rare_dir == 1).sum()), "rare_bad_n": int((rare_dir == -1).sum()),
            "rare_good_delta": float(delta[rare_dir == 1].mean()),
            "rare_bad_delta": float(delta[rare_dir == -1].mean()),
            "rare_good_rates": [float(d["b_rate"][pairs[rare_dir == 1, k]].mean()) for k in (0, 1)],
            "rare_bad_rates": [float(d["b_rate"][pairs[rare_dir == -1, k]].mean()) for k in (0, 1)]}


def compute_bayes() -> dict:
    cab = C.bayes(0.15, 0.8, 0.2)
    cab_nf = C.natural_frequencies(100, 0.15, 0.8, 0.2)
    mam = C.bayes(0.01, 0.8, 0.096)
    mam_nf = C.natural_frequencies(1000, 0.01, 0.8, 0.096)
    return {"cab": cab, "cab_nf": cab_nf, "mam": mam, "mam_nf": mam_nf,
            # Tversky and Kahneman (1982): the median answer to the cab problem
            "cab_median_answer": 0.80}


WORLDS = {"noncompensatory": ((8.0, 4.0, 2.0, 1.0, 0.5, 0.25), 3.0),
          "compensatory": ((1.0, 1.0, 1.0, 1.0, 1.0, 1.0), 2.0)}


def compute_ttb() -> dict:
    sizes = (8, 10, 12, 15, 20, 30, 40, 60, 80)
    out = {"train": np.array(sizes)}
    for name, (w, noise) in WORLDS.items():
        r = C.heuristics_cv(w, sizes, reps=300, noise=noise, seed=26)
        for k in ("ttb", "tally", "regression"):
            out[f"{name}_{k}"] = r[k]
            out[f"{name}_{k}_se"] = r[k + "_se"]
        out[f"{name}_weights"] = np.array(w)
    nc = out["noncompensatory_ttb"] - out["noncompensatory_regression"]
    out["ttb_wins_upto"] = int(np.array(sizes)[nc > 0].max()) if (nc > 0).any() else 0
    out["ttb_lead_small"] = float(nc[0])
    return out


def compute_hothand() -> dict:
    ex4 = C.streak_exact(4, 1)
    seqs, props = ex4["table"]
    ns = np.arange(3, 21)
    curve = np.array([C.streak_exact(int(n), 1)["expected"] for n in ns])
    sim = C.streak_sim(100, 3, 0.5, reps=200_000, seed=26)
    sim_k1 = C.streak_sim(100, 1, 0.5, reps=200_000, seed=27)
    return {"seqs": seqs, "props": props, "expected4": ex4["expected"], "ns": ns, "curve": curve,
            "e100_k3": sim["expected"], "e100_k1": sim_k1["expected"],
            "hist": np.histogram(sim["props"], bins=np.linspace(0, 1, 26))[0], "bins": np.linspace(0, 1, 26)}


def compute_time() -> dict:
    t = np.linspace(0, 52, 209)  # weeks
    k, gap, small, large = 0.05, 4.0, 100.0, 110.0
    delta = 0.97
    star = C.reversal_delay(small, large, gap, k)
    return {"t": t, "exp": C.discount(t, "exponential", delta=delta), "hyp": C.discount(t, k=k),
            "bd": C.discount(t, "beta_delta", beta=0.7, delta=0.995),
            "k": k, "gap": gap, "small": small, "large": large, "delta": delta, "star": star,
            "hyp_small": small * C.discount(t, k=k), "hyp_large": large * C.discount(t + gap, k=k),
            "exp_small": small * delta ** t, "exp_large": large * delta ** (t + gap)}


EXP_PROBLEMS = [("4 with .8, or 3", C.lottery((0.8, 4), (0.2, 0)), 3.0),
                ("32 with .1, or 3", C.lottery((0.1, 32), (0.9, 0)), 3.0),
                ("$-$3, or $-$32 with .1", C.lottery((0.1, -32), (0.9, 0)), -3.0),
                ("$-$3, or $-$4 with .8", C.lottery((0.8, -4), (0.2, 0)), -3.0)]


def compute_experience() -> dict:
    n = np.arange(1, 41)
    never = {p: C.p_never_seen(p, n) for p in (0.05, 0.1, 0.2)}
    desc, expr = [], []
    for name, L, sure in EXP_PROBLEMS:
        d = C.cpt(L) - C.cpt(C.lottery((1.0, sure)))
        desc.append(float(1 / (1 + np.exp(-1.0 * d))))
        expr.append(C.sample_choices(L, sure, 7, reps=40_000, seed=26))
    return {"n": n, "never_05": never[0.05], "never_10": never[0.1], "never_20": never[0.2],
            "names": [p[0] for p in EXP_PROBLEMS], "desc": np.array(desc), "expr": np.array(expr),
            "never7_10": float(C.p_never_seen(0.1, 7))}


def compute_systems() -> dict:
    from explainer.psychology.psyche import decide as D

    v, a, w, t0 = 0.8, 1.6, 0.25, 0.3  # start a quarter of the way up: near the intuitive answer (lower bound)
    rt, up = D.simulate(v, a, w, t0, n=40_000, seed=26, dt=0.001)
    ok = np.isfinite(rt)
    rt, up = rt[ok], up[ok]
    qs = np.quantile(rt, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
    bin_ = np.clip(np.searchsorted(qs, rt, "right") - 1, 0, 4)
    p_ref = np.array([up[bin_ == b].mean() for b in range(5)])
    mid = np.array([np.median(rt[bin_ == b]) for b in range(5)])
    return {"v": v, "a": a, "w": w, "t0": t0, "p_reflective": p_ref, "rt_mid": mid,
            "overall": float(up.mean()), "fast_intuitive": float(1 - p_ref[0]),
            "slow_reflective": float(p_ref[-1])}


def compute_sampling() -> dict:
    rng = np.random.default_rng(26)
    credits = np.exp(rng.normal(np.log(150.0), 1.1, 2_000))  # fewer, larger
    debits = np.exp(rng.normal(np.log(60.0), 1.1, 20_000))  # many, smaller
    x = np.linspace(0, 1000, 401)
    vg = C.dbs_value(x, credits)
    vl = -C.dbs_value(x, debits)
    at = 100.0
    return {"x": x, "v_gain": vg, "v_loss": vl, "at": at,
            "gain_at": float(C.dbs_value(at, credits)), "loss_at": float(C.dbs_value(at, debits)),
            "ratio_at": float(C.dbs_value(at, debits) / C.dbs_value(at, credits)),
            "ratio_amounts": np.array([20.0, 50.0, 100.0, 200.0, 500.0]),
            "ratios": np.array([C.dbs_value(a, debits) / C.dbs_value(a, credits) for a in (20.0, 50.0, 100.0, 200.0, 500.0)]),
            "n_credits": len(credits), "n_debits": len(debits),
            "hist_c": np.histogram(np.log10(credits), bins=np.linspace(0, 4, 33))[0],
            "hist_d": np.histogram(np.log10(debits), bins=np.linspace(0, 4, 33))[0],
            "hist_bins": np.linspace(0, 4, 33)}


def compute_rational() -> dict:
    """Lieder, Griffiths, Huys and Goodman's (2018) argument in its simplest form: an estimate starts at the anchor
    and each step of adjustment removes a share r of the remaining distance D; the error costs its square and each
    step costs c.  The best number of steps leaves a bias toward the anchor, larger when time is dearer."""
    D, r = 40.0, 0.12
    k = np.arange(0, 41)
    bias = D * (1 - r) ** k
    out = {"k": k, "bias": bias, "D": D, "r": r}
    for name, c in (("cheap", 2.0), ("dear", 20.0)):
        J = bias ** 2 + c * k
        kb = int(np.argmin(J))
        out[f"J_{name}"] = J
        out[f"c_{name}"] = c
        out[f"k_{name}"] = kb
        out[f"bias_{name}"] = float(bias[kb])
    return out


def compute_calibration() -> dict:
    """Juslin's (1994) argument as a simulation.  Each question comes with a cue whose validity v (the chance the
    cue's answer is right) is 0.55 to 0.95 in steps of 0.1; the judge answers with the cue and states v as its
    confidence, so over the world's questions it is calibrated by construction.  Random questions are drawn as
    they come; chosen questions keep every one on which the cue misleads but only three in five of those on which it
    is right, as an experimenter looking for questions that catch people out might."""
    rng = np.random.default_rng(1994)
    levels = np.round(np.arange(0.55, 1.0, 0.1), 2)
    n = 200_000
    v = rng.choice(levels, n)
    right = rng.random(n) < v
    keep = right & (rng.random(n) < 0.6) | ~right
    out = {"levels": levels}
    for name, mask in (("random", np.ones(n, bool)), ("chosen", keep)):
        out[f"acc_{name}"] = np.array([right[mask & (v == L)].mean() for L in levels])
        out[f"conf_{name}"] = float(v[mask].mean())
        out[f"hit_{name}"] = float(right[mask].mean())
        out[f"over_{name}"] = float(v[mask].mean() - right[mask].mean())
    return out


ITEMS = {"framing": compute_framing, "stpete": compute_stpete, "allais": compute_allais, "curves": compute_curves,
         "fourfold": compute_fourfold, "c13k": compute_c13k, "bayes": compute_bayes, "ttb": compute_ttb,
         "hothand": compute_hothand, "time": compute_time, "experience": compute_experience,
         "systems": compute_systems, "sampling": compute_sampling,
         "rational": compute_rational, "calibration": compute_calibration}


if __name__ == "__main__":
    CACHE.main(ITEMS)
