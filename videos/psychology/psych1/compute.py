"""Precompute every number in Part 1 of *Psychology, Built* ("Kant's Wager").

    python -m videos.psychology.psych1.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych1.compute --force pool_study

Results are cached in ``.cache/psych1/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Historical numbers
come from the Archive (``explainer.psychology.archive``, each with its source), models from Psyche
(``explainer.psychology.psyche.chronometry``), simulated participants from the Pool (seed 1850); every random
choice here is seeded.

Items:
    helmholtz    the 1850 nerve lengths and delays and the speeds they give; the later measurements in people;
                 how long a signal takes over one metre of nerve at each speed
    donders      Donders' three means and two differences; Psyche's stage models for his three methods, with
                 their densities and 20,000 simulated reaction times each; the rival model with the same means
    insertion    the distributional test of pure insertion in two model worlds: one where a stage is inserted and
                 nothing else changes, one where preparing the response changes the other stages
    additive     additive factors: exact 2 x 2 mean tables when two factors act on different stages and when they
                 act on the same stage, and a simulated experiment of each with standard errors
    ebbinghaus   the retention table of 1885 with his own fitted curve on a fine grid
    rt_shape     the shape of a reaction-time distribution: Psyche's simple and choice RTs, an ex-Gaussian and a
                 normal fitted to the choice RTs, the log-likelihoods, and the published means of Woods et al.
    hick         Psyche's prediction for 1 to 10 alternatives, with the per-bit time set from Donders' two means
    pool_study   Donders' experiment on 300 people of the Pool at 20 and at 400 trials: estimated against true
                 b - c differences, their correlations, and the group mean against the two kinds of people
    devices      one Pool participant measured on three devices with different constant delays: the means move,
                 the differences do not
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.pool import Pool
from explainer.psychology.psyche import chronometry as ch

CACHE = Cache("psych1")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_helmholtz() -> dict:
    d = archive.HELMHOLTZ_1850.data
    (l0, l1), (t0, t1) = d["length_mm"], d["delay_s"]
    lo, hi = ch.conduction_speed(l0, t1), ch.conduction_speed(l1, t0)
    assert (round(lo), round(hi)) == tuple(round(v) for v in d["speed_frog"])
    later = [{"who": w, "year": y, "speed": s} for w, y, s in d["later"]]
    speeds = {"frog_lo": lo, "frog_hi": hi, "human_1850": d["speed_human_1850"]}
    return {
        "length_mm": [l0, l1], "delay_ms": [1000 * t0, 1000 * t1], "speed_lo": lo, "speed_hi": hi,
        "speed_mid": ch.conduction_speed((l0 + l1) / 2, (t0 + t1) / 2),
        "human_1850": d["speed_human_1850"], "brain_time_ms": 1000 * d["brain_time_s"], "later": later,
        "metre_ms": {k: 1000 / v for k, v in speeds.items()},  # ms to travel one metre of nerve
        "sound": 343.0,
    }


def compute_donders() -> dict:
    d = archive.DONDERS_1868.data
    a, b, c = d["a"], d["b"], d["c"]
    pure = ch.donders_models(a, c - a, b - c)
    rival = ch.prepared_models(a, b, c)
    for k, want in zip("abc", (a, b, c)):
        assert abs(pure[k].mean - want) < 1e-9 and abs(rival[k].mean - want) < 1e-9
    t = np.arange(120.0, 480.0, 1.0)
    g = rng(1868)
    samples = {k: pure[k].sample(20_000, g) for k in "abc"}
    sub = ch.subtraction(samples["a"], samples["b"], samples["c"])
    out = {
        "a": a, "b": b, "c": c, "discriminate": c - a, "choose": b - c, "alternatives": d["alternatives"],
        "t": t,
        "stages": {k: [[s.name, s.mean] for s in pure[k].stages] for k in "abc"},
        "rival_stages": {k: [[s.name, s.mean] for s in rival[k].stages] for k in "abc"},
        "sd": {k: pure[k].sd for k in "abc"},
        "sim_mean": {k: float(samples[k].mean()) for k in "abc"},
        "sim_subtraction": sub,
    }
    for k in "abc":
        out[f"pdf_{k}"] = pure[k].pdf(t)
        out[f"sample_{k}"] = samples[k][:400]
    return out


def compute_insertion() -> dict:
    """Two model worlds with the same mean difference between a short task and a long one."""
    g = rng(1969)
    M = ch.donders_models()
    n = 4000
    short, long_ = M["a"], M["c"]
    # the world where insertion fails: in the simple task the response is prepared in advance, which makes it
    # fast on average but adds anticipations (a much more variable response stage); the longer task has the
    # ordinary response stage, slower by the same amount on average as the inserted stage is short
    prepared_a = short.with_stage("respond", cv=0.42)
    worlds = {"inserted": (short, long_), "changed": (prepared_a, long_)}
    t = np.arange(100.0, 420.0, 1.0)
    out = {"n": n, "t": t}
    for name, (m_s, m_l) in worlds.items():
        xs, xl = m_s.sample(n, g), m_l.sample(n, g)
        test = ch.insertion_test(xs, xl, n_boot=1000, seed=7)
        out[name] = {"mean_short": float(xs.mean()), "mean_long": float(xl.mean()),
                     "var_short": float(xs.var()), "var_long": float(xl.var()),
                     "true_var_short": m_s.var, "true_var_long": m_l.var, **test}
        out[f"pdf_short_{name}"] = m_s.pdf(t)
        out[f"pdf_long_{name}"] = m_l.pdf(t)
    # the inserted stage's own density, for the convolution picture (a gamma with mean 36 and CV 0.6)
    stage = [s for s in long_.stages if s.name == "discriminate"][0]
    ts = np.arange(0.0, 160.0, 1.0)
    out["stage_t"] = ts
    out["stage_pdf"] = stats.gamma.pdf(ts, 1 / stage.cv ** 2, scale=stage.mean * stage.cv ** 2)
    out["stage_mean"], out["stage_var"] = stage.mean, stage.var
    assert out["inserted"]["z_var"] < 3 and out["changed"]["z_var"] > 3
    return out


def compute_additive() -> dict:
    """Two 2 x 2 experiments on Psyche's choice model.  In ``different`` the factors act on different stages (a
    degraded stimulus slows sensing; more alternatives slow choosing).  In ``same`` both act on the choice stage (an
    awkward mapping of stimuli to responses, and more alternatives)."""
    g = rng(1966)
    base = ch.donders_models()["b"]
    n = 300  # trials per cell of the simulated experiment
    designs = {"different": (("sense", 1.25, "stimulus quality"), ("choose", 1.8, "number of alternatives")),
               "same": (("choose", 1.5, "mapping"), ("choose", 1.8, "number of alternatives"))}
    out = {"n": n}
    for name, ((s1, f1_hard, n1), (s2, f2_hard, n2)) in designs.items():
        exact = ch.factorial_means(base, s1, f1_hard, s2, f2_hard)
        cells = np.empty((2, 2))
        ses = np.empty((2, 2))
        for i, f1 in enumerate((1.0, f1_hard)):
            for j, f2 in enumerate((1.0, f2_hard)):
                m = base
                stage_means = {s.name: s.mean for s in m.stages}
                m = m.with_stage(s1, mean=stage_means[s1] * f1)
                stage_means = {s.name: s.mean for s in m.stages}
                m = m.with_stage(s2, mean=stage_means[s2] * f2)
                x = m.sample(n, g)
                cells[i, j], ses[i, j] = x.mean(), x.std(ddof=1) / math.sqrt(n)
        out[name] = {"stages": [s1, s2], "factors": [n1, n2], "levels": [f1_hard, f2_hard],
                     "exact": exact.tolist(), "interaction": ch.interaction(exact),
                     "sim": cells.tolist(), "sim_se": ses.tolist(), "sim_interaction": ch.interaction(cells),
                     "sim_interaction_se": float(math.sqrt((ses ** 2).sum()))}
    assert abs(out["different"]["interaction"]) < 1e-9 and out["same"]["interaction"] > 10
    return out


def compute_ebbinghaus() -> dict:
    d = archive.EBBINGHAUS_1885.data
    minutes = np.asarray(d["minutes"])
    grid = np.logspace(math.log10(10), math.log10(60_000), 240)

    def formula(t):
        return 100 * d["k"] / (np.log10(t) ** d["c"] + d["k"])

    fitted = formula(minutes)
    assert np.abs(fitted - np.asarray(d["calculated"])).max() < 0.15
    return {"minutes": minutes, "hours": np.asarray(d["hours"]), "saving": np.asarray(d["saving"]),
            "pe": np.asarray(d["probable_error"]), "grid": grid, "curve": formula(grid), "fitted": fitted,
            "k": d["k"], "c": d["c"], "syllables": d["syllables_created"],
            "max_miss": float(np.abs(fitted - np.asarray(d["saving"])).max())}


def compute_rt_shape() -> dict:
    g = rng(1965)
    w = archive.WOODS_2015.data
    # Psyche's simple reaction: sensing and responding, with the published split of Woods et al.
    simple = ch.StageModel((ch.Stage("sense", w["detection_ms"], 0.12),
                            ch.Stage("respond", w["mean_corrected_ms"] - w["detection_ms"], 0.2)))
    choice = simple.insert(ch.Stage("discriminate", 40.0, 0.6), before="respond").insert(
        ch.Stage("choose", 110.0, 0.7), before="respond")
    n = 3000
    xs, xc = simple.sample(n, g), choice.sample(n, g)
    ex = ch.fit_exgauss(xc)
    mu, sd = float(xc.mean()), float(xc.std())
    ll_normal = float(stats.norm.logpdf(xc, mu, sd).sum())
    t = np.arange(100.0, 800.0, 2.0)
    edges = np.arange(100.0, 800.0, 20.0)
    skew = float(((xc - mu) ** 3).mean() / sd ** 3)
    assert ex["loglik"] > ll_normal and skew > 0.3
    return {"n": n, "t": t, "edges": edges,
            "hist_simple": np.histogram(xs, edges, density=True)[0],
            "hist_choice": np.histogram(xc, edges, density=True)[0],
            "pdf_simple": simple.pdf(t), "pdf_choice": choice.pdf(t),
            "exgauss": ex, "exgauss_pdf": ch.exgauss_pdf(t, ex["mu"], ex["sigma"], ex["tau"]),
            "normal": {"mu": mu, "sd": sd, "loglik": ll_normal}, "normal_pdf": stats.norm.pdf(t, mu, sd),
            "skew": skew, "mean_simple": float(xs.mean()), "mean_choice": mu,
            "median_choice": float(np.median(xc)),
            "woods": {k: w[k] for k in ("n", "mean_raw_ms", "mean_corrected_ms", "detection_ms",
                                         "age_slope_ms_per_year", "galton_ms")}}


def compute_hick() -> dict:
    d = archive.DONDERS_1868.data
    per_bit = (d["b"] - d["c"]) / math.log2(d["alternatives"])  # Donders' choice time, spread over log2(5) bits
    n = np.arange(1, 11)
    return {"n": n, "bits": np.log2(n), "per_bit": per_bit, "base": d["c"],
            "predicted": ch.hick(n, d["c"], per_bit), "donders_n": d["alternatives"], "donders_b": d["b"]}


def compute_pool_study() -> dict:
    pool = Pool()
    ids = pool.sample(300, seed=1)
    truth = pool.true_stage(ids)
    dec = pool.gonogo_decides[ids]
    out = {"n_people": len(ids), "truth_bc": truth["b_minus_c"], "decides": dec,
           "share_decides": float(dec.mean()),
           "true_choose_mean": float(truth["choose"].mean()),
           "true_bc_mean": float(truth["b_minus_c"].mean()),
           "true_bc_nondeciders": float(truth["b_minus_c"][~dec].mean())}
    for trials in (20, 400):
        tr = pool.run_rt(ids, trials, seed=trials)
        rt = {m: tr.rt[tr.condition == m].reshape(len(ids), -1).mean(axis=1) for m in "abc"}
        est = rt["b"] - rt["c"]
        # within each kind of person the true difference varies; the estimate's correlation with it
        r_all = float(np.corrcoef(est, truth["b_minus_c"])[0, 1])
        r_non = float(np.corrcoef(est[~dec], truth["b_minus_c"][~dec])[0, 1])
        out[f"est_{trials}"] = est
        out[f"stats_{trials}"] = {"r_all": r_all, "r_nondeciders": r_non, "mean": float(est.mean()),
                                  "se": float(est.std(ddof=1) / math.sqrt(len(ids))),
                                  "negative": float((est < 0).mean()),
                                  "mean_a": float(rt["a"].mean()), "mean_b": float(rt["b"].mean()),
                                  "mean_c": float(rt["c"].mean())}
    assert out["stats_400"]["r_nondeciders"] > out["stats_20"]["r_nondeciders"]
    return out


def compute_devices() -> dict:
    pool = Pool()
    i = int(pool.sample(1, seed=3)[0])
    models = pool.rt_models(i)
    g = rng(2020)
    a, b = models["a"].sample(200, g), models["b"].sample(200, g)
    lags = {"calibrated": 0.0, "laptop": 18.0, "phone": 60.0}  # illustrative constant delays, ms
    rows = [{"device": k, "lag": lag, "simple": float(a.mean() + lag), "choice": float(b.mean() + lag),
             "difference": float(b.mean() - a.mean())} for k, lag in lags.items()]
    w = archive.WOODS_2015.data
    return {"person": i, "rows": rows, "woods_raw": w["mean_raw_ms"], "woods_corrected": w["mean_corrected_ms"],
            "woods_delay": w["mean_raw_ms"] - w["mean_corrected_ms"], "galton": w["galton_ms"]}


ITEMS = {
    "helmholtz": compute_helmholtz,
    "donders": compute_donders,
    "insertion": compute_insertion,
    "additive": compute_additive,
    "ebbinghaus": compute_ebbinghaus,
    "rt_shape": compute_rt_shape,
    "hick": compute_hick,
    "pool_study": compute_pool_study,
    "devices": compute_devices,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
