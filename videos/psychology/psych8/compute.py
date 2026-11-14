"""Precompute every number in Part 8 of *Psychology, Built* ("Reading the Brain").

    python -m videos.psychology.psych8.compute            # everything missing (about a minute), into .cache/psych8/
    python -m videos.psychology.psych8.compute --force tests

Results are cached in ``.cache/psych8/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.imaging``); the published figures they are set beside come from the
Archive.  Every random choice is seeded.

Items:
    salmon     the chance that at least one of N tests passes at p < 0.001 when nothing is there
    tuning     an orientation-tuned model cell: its tuning curve, Poisson counts and three rasters
    eeg        aligned against randomly oriented dipoles; a toy lead field; a source no electrode can see
    erp        single trials and averages of a model N400; the noise left after n trials
    mri        relaxation curves; a phantom, its k-space, and the image from part of k-space
    bold       the haemodynamic response; events convolved with it; the test of linearity
    glm        one active and one silent voxel fitted with a design matrix
    tests      a synthetic brain thresholded by four rules; how often each rule finds something in null brains
    cluster    an extent threshold calibrated on Gaussian noise, applied to noise with a long-tailed autocorrelation
    voodoo     voxels selected by their correlation with a score: the correlation in the same data and in fresh data
    ceiling    the largest correlation two unreliable measures can show; three scatter plots, one of them impossible
    reverse    reverse inference by Bayes' rule, for several priors and two regions
    power      what a study of 25 people finds when the true correlation is small; the samples needed
    detector   a lie detector that is right nine times in ten, used where one person in ten is lying
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import imaging as I

CACHE = Cache("psych8")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_salmon() -> dict:
    n = np.unique(np.round(np.logspace(0, 5.2, 200)).astype(int))
    marks = np.array([1_000, 10_000, 100_000])
    return {"n": n, "chance": np.array([I.chance_of_any(int(k)) for k in n]), "marks": marks, "p": 0.001,
            "chance_at": np.array([I.chance_of_any(int(k)) for k in marks]), "expected_at": marks * 0.001}


def compute_tuning() -> dict:
    theta = np.arange(0, 180, 15.0)
    fine = np.linspace(0, 180, 181)
    counts = I.spike_counts(theta, trials=8, window=0.5, rng=rng(80))
    g = rng(81)
    rasters = {}
    for ang in (45.0, 75.0, 135.0):  # the preferred orientation, 30 degrees off, and the orthogonal one
        rate = float(I.tuning_curve(ang))
        rasters[f"raster_{int(ang)}"] = np.sort(g.uniform(0, 1.0, g.poisson(rate)))
        rasters[f"rate_{int(ang)}"] = rate
    return {"theta": theta, "fine": fine, "curve": I.tuning_curve(fine), "counts": counts,
            "mean_rate": counts.mean(axis=1) / 0.5, "sem_rate": counts.std(axis=1, ddof=1) / np.sqrt(8) / 0.5,
            "pref": 45.0, "peak": float(I.tuning_curve(45.0)), "orth": float(I.tuning_curve(135.0)), **rasters}


def compute_eeg() -> dict:
    n = np.array([10, 100, 1_000, 10_000, 100_000, 1_000_000])
    g = rng(82)
    rand = np.array([I.dipole_sum(int(k), False, repeats=40 if k > 10_000 else 300, rng=g) for k in n])
    elec, src = I.electrodes(9), I.source_grid(6)
    L = I.lead_field(elec, src)
    focal = np.zeros(len(src))
    k0 = int(np.argmin(np.hypot(src[:, 0] - 0.15, src[:, 1] - 0.45)))
    focal[k0] = 1.0
    silent = I.silent_source(L, rng=rng(83))
    other = focal + 2.5 * silent / np.abs(silent).max()
    return {"n": n, "aligned": n.astype(float), "random": rand, "ratio_million": float(n[-1] / rand[-1]),
            "electrodes": elec, "sources": src, "focal": focal, "other": other, "silent": silent,
            "scalp_focal": L @ focal, "scalp_other": L @ other, "max_difference": float(np.abs(L @ (other - focal)).max()),
            "n_sources": len(src), "n_electrodes": len(elec)}


def compute_erp() -> dict:
    t = np.arange(-100.0, 800.0, 4.0)
    odd = I.erp_trials(200, t, "n400", rng=rng(84))
    usual = I.erp_trials(200, t, "none", rng=rng(85))
    ns = np.array([1, 4, 10, 25, 50, 100, 200])
    g = rng(86)
    big = I.erp_trials(4000, t, "none", rng=g) - I.erp_template(t, "none")
    left = []
    for n in ns:  # the noise left in an average of n trials, over many averages
        idx = g.integers(0, len(big), (200, int(n)))
        left.append(float(np.sqrt((big[idx].mean(axis=1) ** 2).mean())))
    diff = odd.mean(axis=0) - usual.mean(axis=0)
    return {"t": t, "template": I.erp_template(t, "n400"), "plain": I.erp_template(t, "none"),
            "singles": odd[:3], "avg_10": odd[:10].mean(axis=0), "avg_50": odd[:50].mean(axis=0),
            "avg_200": odd.mean(axis=0), "usual_200": usual.mean(axis=0), "difference": diff,
            "peak_ms": float(t[np.argmin(diff)]), "peak_uv": float(diff.min()), "ns": ns, "left": np.array(left),
            "theory": I.erp_noise(20.0, ns), "noise_sd": 20.0, "component_uv": 5.0,
            "trials_for_1uv": int(np.ceil((20.0 / 1.0) ** 2))}


def compute_mri() -> dict:
    t = np.linspace(0, 3000, 301)
    t2 = np.linspace(0, 300, 301)
    grey, white = I.relaxation(t, 1300.0, 110.0), I.relaxation(t, 800.0, 80.0)
    im = I.phantom(64)
    k = I.kspace(im)
    keeps = np.array([1.0, 0.5, 0.25, 0.125])
    return {"t": t, "t2": t2, "grey_recovery": grey["recovery"], "white_recovery": white["recovery"],
            "grey_decay": I.relaxation(t2, 1300.0, 110.0)["decay"], "white_decay": I.relaxation(t2, 800.0, 80.0)["decay"],
            "image": im, "k_log": np.log1p(np.abs(k)), "keeps": keeps,
            "recon": np.array([I.from_kspace(k, float(f)) for f in keeps]),
            "error": np.array([float(np.abs(I.from_kspace(k, float(f)) - im).mean()) for f in keeps])}


def compute_bold() -> dict:
    t = np.linspace(0, 30, 301)
    h = I.hrf(t)
    tr, n = 1.0, 100
    onsets = np.array([8.0, 30.0, 32.0, 34.0, 70.0])
    scans = np.arange(n) * tr
    one, two = I.bold([10.0], n, tr), I.bold([16.0], n, tr)
    both = I.bold([10.0, 16.0], n, tr)
    return {"t": t, "hrf": h, "peak_s": float(t[np.argmax(h)]), "under_s": float(t[np.argmin(h)]),
            "under": float(h.min()), "back_s": float(t[np.argmax((t > 5) & (h < 0.02))]), "scans": scans, "onsets": onsets,
            "response": I.bold(onsets, n, tr), "one": one, "two": two, "both": both,
            "linear_error": float(np.abs(both - one - two).max()),
            "block": I.bold(np.arange(20.0, 100.0, 40.0), n, tr, duration=20.0), "block_on": np.arange(20.0, 100.0, 40.0)}


def compute_glm() -> dict:
    brain = I.SyntheticBrain(regions=((16, 15, 3.0, 0.20), (30, 33, 4.0, 0.16)))
    s = brain.scan(rng=rng(87))
    Y, X = s["Y"], s["X"]
    on, off = (16, 15), (24, 24)
    out = {"X": X, "scans": np.arange(len(X)) * 2.0, "df": s["df"]}
    for name, (r, c) in (("active", on), ("silent", off)):
        fit = I.glm(Y[:, r, c], X, [1, 0])
        out[f"{name}_y"], out[f"{name}_fit"] = Y[:, r, c], X @ fit["beta"][:, 0]
        out[f"{name}_beta"], out[f"{name}_t"] = float(fit["beta"][0, 0]), float(fit["t"][0])
        out[f"{name}_p"] = float(fit["p"][0])
    out["true_beta"] = 0.20
    return out


def compute_tests() -> dict:
    brain = I.SyntheticBrain(regions=((16, 15, 3.0, 0.20), (30, 33, 4.0, 0.16)))
    s = brain.scan(rng=rng(87))
    null_maps, mask = I.null_tmaps(1000, rng=rng(88))
    extent = I.cluster_extent(I.null_tmaps(1000, rng=rng(89))[0], mask, s["df"])
    out = {"t": s["t"], "truth": brain.truth, "mask": brain.mask, "voxels": int(brain.mask.sum()),
           "active": int(brain.active.sum()), "df": s["df"], "extent": extent}
    for rule in ("uncorrected", "bonferroni", "fdr", "cluster"):
        hit = I.threshold_map(s["t"], s["df"], brain.mask, rule, extent=extent)
        out[f"map_{rule}"] = hit
        out[f"hits_{rule}"], out[f"false_{rule}"] = int((hit & brain.active).sum()), int((hit & ~brain.active).sum())
    rates = I.familywise_rates(null_maps, mask, s["df"], extent)
    out.update({f"rate_{k}": v for k, v in rates.items()})
    # a null brain for the picture, chosen by rule: the first, in seed order, in which the uncorrected rule
    # declares at least one voxel
    for k, t in enumerate(null_maps):
        hit = I.threshold_map(t, s["df"], mask, "uncorrected")
        if hit.any():
            out["null_t"], out["null_hit"], out["null_index"], out["null_voxels"] = t, hit, k, int(hit.sum())
            break
    out["expected_false"] = out["voxels"] * 0.001
    out["chance_formula"] = I.chance_of_any(out["voxels"])
    return out


def compute_cluster() -> dict:
    g = rng(90)
    res = I.cluster_calibration(brains=1000, long_tail=0.5, rng=g)
    gauss = I.smooth_noise((300, 48, 48), 3.0, rng(91))
    tail = I.smooth_noise((300, 48, 48), 3.0, rng(92), long_tail=0.5)

    def acf(z, lags=16):
        # autocorrelation along a row, averaged over the maps
        return np.array([1.0] + [float((z[:, :, :-k] * z[:, :, k:]).mean()) for k in range(1, lags)])

    return {**res, "lags": np.arange(16), "acf_gauss": acf(gauss), "acf_tail": acf(tail),
            "example_gauss": gauss[0], "example_tail": tail[0], "nominal": 0.05,
            "inflation": res["long_tail"] / 0.05}


def compute_voodoo() -> dict:
    one = I.voodoo(subjects=16, voxels=10_000, threshold=0.7, rng=rng(93))
    best = int(np.argmax(one["r_all"]))
    g = rng(94)
    same, fresh, count = [], [], []
    for _ in range(200):
        v = I.voodoo(subjects=16, voxels=10_000, threshold=0.7, rng=g)
        if v["selected"]:
            same.append(v["r_same"]), fresh.append(v["r_fresh"]), count.append(v["selected"])
    sig = [I.voodoo(subjects=16, voxels=10_000, true_r=0.3, signal_share=0.02, threshold=0.7, rng=g) for _ in range(200)]
    edges = np.linspace(-1, 1, 41)
    # the best voxel of the first run, for the scatter: regenerate it from the same seed
    g2 = rng(93)
    score = g2.standard_normal(16)
    act = g2.standard_normal((16, 10_000))[:, best]
    return {"subjects": 16, "voxels": 10_000, "threshold": 0.7, "selected": one["selected"], "r_same": one["r_same"],
            "r_fresh": one["r_fresh"], "mean_same": float(np.mean(same)), "mean_fresh": float(np.mean(fresh)),
            "mean_selected": float(np.mean(count)), "edges": edges,
            "hist": np.histogram(one["r_all"], edges)[0] / len(one["r_all"]), "best_r": float(one["r_all"][best]),
            "score": score, "best_activation": act,
            "signal_same": float(np.nanmean([v["r_same"] for v in sig])),
            "signal_fresh": float(np.nanmean([v["r_fresh"] for v in sig])), "signal_true": 0.3,
            "p_threshold": float(1 - __import__("scipy.stats").stats.t.cdf(0.7 * np.sqrt(14) / np.sqrt(1 - 0.49), 14))}


def compute_ceiling() -> dict:
    rel = np.linspace(0.05, 1.0, 96)
    g = rng(95)

    def scatter(r, n=16):
        x = g.standard_normal(n)
        y = g.standard_normal(n)
        x, y = (x - x.mean()) / x.std(), (y - y.mean()) / y.std()
        y = y - (x @ y) / n * x  # the part of y orthogonal to x
        y = y / y.std()
        return x, r * x + np.sqrt(1 - r ** 2) * y  # a sample whose correlation is exactly r

    shown = np.array([0.45, 0.62, 0.88])
    pts = [scatter(float(r)) for r in shown]
    return {"rel": rel, "ceiling_08": np.sqrt(rel * 0.8), "brain": 0.5, "scale": 0.8,
            "ceiling": I.r_ceiling(0.5, 0.8), "ceiling_task": I.r_ceiling(0.4, 0.8), "shown": shown,
            "x": np.array([p[0] for p in pts]), "y": np.array([p[1] for p in pts]),
            "impossible": int(np.argmax(shown > I.r_ceiling(0.5, 0.8)))}


def compute_reverse() -> dict:
    priors = np.linspace(0.01, 0.99, 99)

    def post(prior, bf):
        return prior * bf / (prior * bf + 1 - prior)

    return {"priors": priors, "bf_weak": 2.3, "bf_strong": 10.0, "weak": post(priors, 2.3), "strong": post(priors, 10.0),
            "at_half": float(post(0.5, 2.3)), "at_fifth": float(post(0.2, 2.3)), "at_tenth": float(post(0.1, 2.3)),
            "strong_half": float(post(0.5, 10.0))}


def compute_power() -> dict:
    out = {"n": 25, "critical": I.r_critical(25)}
    edges = np.linspace(-0.8, 0.8, 65)
    for name, r in (("tiny", 0.01), ("small", 0.06), ("usual", 0.2)):
        s = I.small_study(r, 25, rng=rng(96))
        out[f"{name}_r"], out[f"{name}_power"], out[f"{name}_sig"] = r, s["power"], s["mean_sig_r"]
        out[f"{name}_wrong"], out[f"{name}_need"] = s["wrong_sign"], I.n_for_correlation(r)
        out[f"{name}_hist"] = np.histogram(s["r"], edges)[0] / len(s["r"])
    out["edges"] = edges
    ns = np.unique(np.round(np.logspace(1, 4.7, 60)).astype(int))
    out["ns"], out["half_width"] = ns, 1.96 / np.sqrt(ns - 3)  # the 95% interval of r near zero
    out["inflation_small"] = out["small_sig"] / 0.06
    return out


def compute_detector() -> dict:
    sens, spec = 0.9, 0.9
    base = np.linspace(0.01, 0.99, 99)
    ppv = sens * base / (sens * base + (1 - spec) * (1 - base))
    at = float(sens * 0.1 / (sens * 0.1 + (1 - spec) * 0.9))
    return {"sens": sens, "spec": spec, "base": base, "ppv": ppv, "at_tenth": at, "people": 1000,
            "liars": 100, "caught": 90, "false_alarms": 90}


ITEMS = {
    "salmon": compute_salmon,
    "tuning": compute_tuning,
    "eeg": compute_eeg,
    "erp": compute_erp,
    "mri": compute_mri,
    "bold": compute_bold,
    "glm": compute_glm,
    "tests": compute_tests,
    "cluster": compute_cluster,
    "voodoo": compute_voodoo,
    "ceiling": compute_ceiling,
    "reverse": compute_reverse,
    "power": compute_power,
    "detector": compute_detector,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
