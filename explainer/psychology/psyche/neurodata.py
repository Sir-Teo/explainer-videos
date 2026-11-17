"""Psyche's brain data (Part 49): the analysis chain on synthetic brains where the truth is known.

Group maps with subjects as a random sample; fixed against random effects; a multiverse of pipelines (smoothing,
thresholding, exclusions, covariates) asked the same yes-or-no questions; permutation (sign-flipping) inference for
clusters against a Gaussian-calibrated extent; head motion as a distance-dependent confound in connectivity, and
global-signal regression's anticorrelations; decoding with and without leakage; representational similarity
analysis with a noise ceiling; a ridge encoding model against the noise ceiling; ERP time windows chosen from the
data; a population of cosine-tuned neurons, the population vector and its low-dimensional manifold; a
brain-computer interface's information rate; and brain-behaviour correlations from 25 to 4,000 people.
numpy and scipy only; Part 8's synthetic brain and thresholds from ``imaging``.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy import ndimage, stats

from explainer.psychology.psyche import imaging as Im


# ----------------------------------------------------------------------------------------------------------------
# Group maps: subjects as a sample
# ----------------------------------------------------------------------------------------------------------------
def regions(size: int = 48) -> dict:
    """Five named discs, each the region of one hypothesis, with planted group effects (in within-subject noise
    SDs): from none to large."""
    return {"H1": (12, 14, 4.0, 0.0), "H2": (14, 33, 4.0, 0.25), "H3": (24, 24, 4.0, 0.45),
            "H4": (35, 14, 4.0, 0.7), "H5": (35, 33, 4.0, 1.1)}


def disc(size: int, r: float, c: float, rad: float) -> np.ndarray:
    y, x = np.mgrid[0:size, 0:size]
    return (y - r) ** 2 + (x - c) ** 2 <= rad ** 2


def subject_maps(n: int = 30, size: int = 48, regs=None, between: float = 0.6, fwhm: float = 4.0,
                 long_tail: float = 0.0, seed: int = 0) -> dict:
    """Each subject's contrast map: the planted group effect, plus that subject's own departure (smooth, SD
    ``between``), plus estimation noise (smooth, SD 1).  Returns maps (n, size, size), truth, the mask, region
    masks, and each subject's head motion (a nuisance, larger in some people)."""
    rng = np.random.default_rng(seed)
    regs = regions(size) if regs is None else regs
    brain = Im.SyntheticBrain(size, regions=(), fwhm=fwhm)
    truth = np.zeros((size, size))
    rmask = {}
    for k, (r, c, rad, amp) in regs.items():
        m = disc(size, r, c, rad) & brain.mask
        rmask[k] = m
        truth[m] = amp
    dev = between * Im.smooth_noise((n, size, size), fwhm * 2, rng)
    err = Im.smooth_noise((n, size, size), fwhm, rng, long_tail)
    motion = rng.gamma(2.0, 0.1, n)
    # motion adds an artefact at the brain's edge, scaled by each person's motion
    y, x = np.mgrid[0:size, 0:size]
    c0 = (size - 1) / 2
    rim = np.exp(-((np.hypot((x - c0) / (0.46 * size), (y - c0) / (0.48 * size)) - 1.0) / 0.08) ** 2)
    art = motion[:, None, None] * 4.0 * rim[None] * rng.choice([-1, 1], (n, 1, 1))
    maps = (truth[None] + dev + err + art) * brain.mask[None]
    return {"maps": maps, "truth": truth, "mask": brain.mask, "regions": rmask, "motion": motion,
            "age": rng.normal(30, 8, n)}


def one_sample_t(maps: np.ndarray, mask: np.ndarray, covariate=None) -> tuple:
    """Random effects: a one-sample t across subjects at each voxel (optionally with a centred covariate)."""
    n = maps.shape[0]
    Y = maps.reshape(n, -1)
    if covariate is None:
        X = np.ones((n, 1))
    else:
        X = np.column_stack([np.ones(n), np.asarray(covariate) - np.mean(covariate)])
    B, *_ = np.linalg.lstsq(X, Y, rcond=None)
    R = Y - X @ B
    df = n - X.shape[1]
    s2 = (R ** 2).sum(0) / df
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[0, 0])
    t = np.where(se > 0, B[0] / np.where(se > 0, se, 1), 0.0).reshape(maps.shape[1:])
    return np.where(mask, t, 0.0), df


def fixed_vs_random(n: int = 20, reps: int = 200, between: float = 1.0, within: float = 0.5, voxels: int = 500,
                    seed: int = 0) -> dict:
    """With no group effect but subjects whose effects differ (SD ``between`` at each voxel) and each subject's
    effect estimated with standard error ``within``: the share of null voxels below p < 0.001 when the test uses
    only the within-subject error (fixed effects) against the spread across subjects (random effects)."""
    rng = np.random.default_rng(seed)
    fx = rx = 0.0
    for r in range(reps):
        m = rng.normal(0, between, (n, voxels)) + rng.normal(0, within, (n, voxels))
        t_f = m.mean(0) / (within / np.sqrt(n))
        t_r = m.mean(0) / (m.std(0, ddof=1) / np.sqrt(n))
        fx += np.mean(2 * stats.norm.sf(np.abs(t_f)) < 0.001)
        rx += np.mean(2 * stats.t.sf(np.abs(t_r), n - 1) < 0.001)
    return {"fixed": fx / reps, "random": rx / reps, "nominal": 0.001, "between": between, "within": within}


# ----------------------------------------------------------------------------------------------------------------
# Thresholds: permutation inference
# ----------------------------------------------------------------------------------------------------------------
def sign_flip_null(maps: np.ndarray, mask: np.ndarray, perms: int = 500, primary_t: float = 3.4, seed: int = 0):
    """Nichols and Holmes's permutation test for a one-sample design: flip each subject's sign at random, recompute
    the t map, and keep the maximum t and the largest cluster above ``primary_t``.  Returns both null
    distributions."""
    rng = np.random.default_rng(seed)
    n = maps.shape[0]
    Y = maps.reshape(n, -1)[:, mask.ravel()]
    maxt, maxc = [], []
    full = np.zeros(mask.shape)
    for p in range(perms):
        s = rng.choice([-1.0, 1.0], n)
        Z = Y * s[:, None]
        m = Z.mean(0)
        sd = Z.std(0, ddof=1)
        t = m / (sd / np.sqrt(n))
        maxt.append(t.max())
        full[mask] = t
        _, sizes = Im.clusters(full > primary_t)
        maxc.append(sizes.max() if len(sizes) else 0)
    return np.array(maxt), np.array(maxc)


def cluster_fwe(n_sets: int = 120, n: int = 20, perms: int = 200, long_tail: float = 0.4, fwhm: float = 4.0,
                primary_p: float = 0.01, seed: int = 0) -> dict:
    """Null group studies whose noise has a long-tailed spatial autocorrelation.  An extent threshold calibrated
    on Gaussian-autocorrelated noise (the parametric assumption) against a sign-flipping permutation test of the
    largest cluster, run on each dataset: the share of datasets with any significant cluster (the familywise
    error)."""
    rng = np.random.default_rng(seed)
    size = 48
    df = n - 1
    tcrit = stats.t.isf(primary_p, df)
    brain = Im.SyntheticBrain(size, regions=(), fwhm=fwhm)
    mask = brain.mask

    def group(lt):
        e = Im.smooth_noise((n, size, size), fwhm, rng, lt)
        return e * mask[None]

    biggest = []
    for _ in range(200):
        t, _ = one_sample_t(group(0.0), mask)
        _, sizes = Im.clusters(t > tcrit)
        biggest.append(sizes.max() if len(sizes) else 0)
    extent = int(np.quantile(biggest, 0.95)) + 1
    par = perm = 0
    for k in range(n_sets):
        maps = group(long_tail)
        t, _ = one_sample_t(maps, mask)
        _, sizes = Im.clusters(t > tcrit)
        big = sizes.max() if len(sizes) else 0
        par += big >= extent
        _, null_c = sign_flip_null(maps, mask, perms, tcrit, seed=seed + 1000 + k)
        perm += big > np.quantile(null_c, 0.95)
    return {"extent": extent, "parametric": par / n_sets, "permutation": perm / n_sets, "primary_p": primary_p,
            "sets": n_sets}


# ----------------------------------------------------------------------------------------------------------------
# The multiverse
# ----------------------------------------------------------------------------------------------------------------
PIPELINE = {
    "smoothing": (0.0, 4.0, 8.0),
    "threshold": ("p<0.001", "p<0.005, 10 voxels", "FDR 5%", "cluster p<0.01", "cluster p<0.001", "permutation"),
    "exclusion": ("none", "high motion"),
    "covariate": ("none", "age"),
}


def run_pipeline(data: dict, smoothing: float, threshold: str, exclusion: str, covariate: str,
                 extents: dict, perm_cache: dict) -> np.ndarray:
    """One path through the garden: returns the thresholded map."""
    maps, mask = data["maps"], data["mask"]
    keep = np.ones(len(maps), bool)
    if exclusion == "high motion":
        keep = data["motion"] < np.quantile(data["motion"], 0.8)
    m = maps[keep]
    if smoothing > 0:
        m = ndimage.gaussian_filter(m, [0, smoothing / 2.355, smoothing / 2.355]) * mask[None]
    cov = data["age"][keep] if covariate == "age" else None
    t, df = one_sample_t(m, mask, cov)
    p = np.where(mask, stats.t.sf(t, df), 1.0)
    if threshold == "p<0.001":
        return p < 0.001
    if threshold == "p<0.005, 10 voxels":
        lab, sizes = Im.clusters(p < 0.005)
        return np.isin(lab, np.flatnonzero(sizes >= 10) + 1)
    if threshold == "FDR 5%":
        return p <= Im.fdr_threshold(p[mask], 0.05)
    if threshold.startswith("cluster"):
        prim = 0.01 if "0.01" in threshold else 0.001
        lab, sizes = Im.clusters(p < prim)
        return np.isin(lab, np.flatnonzero(sizes >= extents[(prim, smoothing)]) + 1)
    if threshold == "permutation":
        key = (smoothing, exclusion, covariate)
        if key not in perm_cache:
            mt, _ = sign_flip_null(m, mask, 300, 99.0, seed=11)
            perm_cache[key] = np.quantile(mt, 0.95)
        return t > perm_cache[key]
    raise ValueError(threshold)


def gaussian_extents(n: int, size: int = 48, fwhm: float = 4.0, sims: int = 150, seed: int = 0) -> dict:
    """Cluster-extent thresholds for each primary threshold and smoothing, calibrated on Gaussian noise of the
    data's raw smoothness (the usual parametric shortcut)."""
    rng = np.random.default_rng(seed)
    mask = Im.SyntheticBrain(size, regions=(), fwhm=fwhm).mask
    out = {}
    for sm in PIPELINE["smoothing"]:
        big = {0.01: [], 0.001: []}
        for _ in range(sims):
            e = Im.smooth_noise((n, size, size), fwhm, rng) * mask[None]
            if sm > 0:
                e = ndimage.gaussian_filter(e, [0, sm / 2.355, sm / 2.355]) * mask[None]
            t, df = one_sample_t(e, mask)
            p = np.where(mask, stats.t.sf(t, df), 1.0)
            for prim in big:
                _, sizes = Im.clusters(p < prim)
                big[prim].append(sizes.max() if len(sizes) else 0)
        for prim in big:
            out[(prim, sm)] = int(np.quantile(big[prim], 0.95)) + 1
    return out


def multiverse(n: int = 30, seed: int = 0) -> dict:
    """Every path (3 x 6 x 2 x 2 = 72) on one dataset; for each of five regional hypotheses, whether the path
    reports any significant voxel in the region.  Returns the yes/no table (paths x hypotheses), the share of
    paths saying yes, and how many distinct thresholded maps the paths produce."""
    data = subject_maps(n=n, long_tail=0.3, seed=seed)
    extents = gaussian_extents(n, seed=seed + 1)
    cache = {}
    paths = list(itertools.product(*PIPELINE.values()))
    yes = np.zeros((len(paths), len(data["regions"])), bool)
    maps = []
    for i, path in enumerate(paths):
        th = run_pipeline(data, *path, extents=extents, perm_cache=cache)
        maps.append(th)
        for j, k in enumerate(data["regions"]):
            yes[i, j] = bool((th & data["regions"][k]).any())
    distinct = len({m.tobytes() for m in maps})
    return {"paths": [" / ".join(str(v) for v in p) for p in paths], "yes": yes, "share": yes.mean(0),
            "hypotheses": list(data["regions"]), "effects": [v[3] for v in regions().values()],
            "distinct_maps": distinct, "n_paths": len(paths)}


# ----------------------------------------------------------------------------------------------------------------
# Motion and connectivity
# ----------------------------------------------------------------------------------------------------------------
def motion_connectivity(n_people: int = 80, n_regions: int = 60, T: int = 300, seed: int = 0) -> dict:
    """Regions scattered over a 2-D brain with the same true connectivity in every person.  Brief head movements
    add a shared artefact that is stronger between nearby regions (Power and colleagues, 2012).  Half the people
    move more.  Returns the high-minus-low group difference in correlation against distance, before and after
    censoring the moving scans, and the true difference (zero)."""
    rng = np.random.default_rng(seed)
    pos = rng.uniform(0, 1, (n_regions, 2))
    D = np.hypot(*(pos[:, None, :] - pos[None, :, :]).transpose(2, 0, 1))
    net = rng.integers(0, 3, n_regions)
    L = (net[:, None] == np.arange(3)[None, :]).astype(float) * 0.7
    iu = np.triu_indices(n_regions, 1)

    def person(high):
        z = rng.normal(size=(T, 3)) @ L.T + rng.normal(size=(T, n_regions))
        spikes = rng.random(T) < (0.12 if high else 0.03)
        centre = rng.uniform(0, 1, (T, 2))
        amp = rng.normal(0, 3.0, T) * spikes
        dist_c = np.hypot(pos[None, :, 0] - centre[:, 0:1], pos[None, :, 1] - centre[:, 1:2])
        art = amp[:, None] * np.exp(-dist_c ** 2 / 0.08)
        x = z + art
        r_all = np.corrcoef(x.T)[iu]
        r_cens = np.corrcoef(x[~spikes].T)[iu]
        return r_all, r_cens

    hi = [person(True) for _ in range(n_people // 2)]
    lo = [person(False) for _ in range(n_people // 2)]
    d_all = np.mean([h[0] for h in hi], 0) - np.mean([l[0] for l in lo], 0)
    d_cen = np.mean([h[1] for h in hi], 0) - np.mean([l[1] for l in lo], 0)
    d = D[iu]
    bins = np.linspace(0, 1.0, 9)
    mid = (bins[:-1] + bins[1:]) / 2
    idx = np.digitize(d, bins) - 1
    ok = [k for k in range(len(mid)) if np.any(idx == k)]
    return {"dist": mid[ok], "diff_raw": np.array([d_all[idx == k].mean() for k in ok]),
            "diff_censored": np.array([d_cen[idx == k].mean() for k in ok]),
            "slope_raw": float(np.polyfit(d, d_all, 1)[0]), "slope_censored": float(np.polyfit(d, d_cen, 1)[0])}


def global_signal(n_regions: int = 40, T: int = 600, seed: int = 0) -> dict:
    """Two networks, each driven by its own signal, plus a global signal shared by all; no true anticorrelation.
    Regressing out the global mean leaves the between-network correlations negative (Murphy and colleagues,
    2009).  Returns mean within- and between-network correlations before and after."""
    rng = np.random.default_rng(seed)
    half = n_regions // 2
    a, b, g = rng.normal(size=(3, T))
    X = np.empty((T, n_regions))
    X[:, :half] = 0.8 * a[:, None] + 0.5 * g[:, None] + rng.normal(size=(T, half))
    X[:, half:] = 0.8 * b[:, None] + 0.5 * g[:, None] + rng.normal(size=(T, n_regions - half))
    gs = X.mean(1)
    beta = (gs @ (X - X.mean(0))) / (gs @ (gs - gs.mean()))
    Xr = X - np.outer(gs - gs.mean(), beta)

    def summ(M):
        R = np.corrcoef(M.T)
        w = np.concatenate([R[:half, :half][np.triu_indices(half, 1)],
                            R[half:, half:][np.triu_indices(n_regions - half, 1)]])
        return float(w.mean()), float(R[:half, half:].mean()), R

    w0, b0, R0 = summ(X)
    w1, b1, R1 = summ(Xr)
    return {"within_raw": w0, "between_raw": b0, "within_gsr": w1, "between_gsr": b1, "R_raw": R0, "R_gsr": R1}


# ----------------------------------------------------------------------------------------------------------------
# Patterns: decoding, RSA, encoding
# ----------------------------------------------------------------------------------------------------------------
def _centroid_cv(X, y, folds: int, select: int | None, inside: bool, rng) -> float:
    """Cross-validated accuracy of a nearest-centroid (correlation) classifier, with optional selection of the
    ``select`` voxels with the largest two-sample t, either inside each training fold or once on all data."""
    n = len(y)
    order = rng.permutation(n)
    fold = np.empty(n, int)
    fold[order] = np.arange(n) % folds

    def top(Xs, ys):
        t = stats.ttest_ind(Xs[ys == 1], Xs[ys == 0]).statistic
        return np.argsort(-np.abs(t))[:select]

    keep_all = top(X, y) if (select and not inside) else None
    correct = 0
    for f in range(folds):
        tr, te = fold != f, fold == f
        cols = keep_all if keep_all is not None else (top(X[tr], y[tr]) if select else slice(None))
        A, B = X[tr][:, cols], X[te][:, cols]
        c0, c1 = A[y[tr] == 0].mean(0), A[y[tr] == 1].mean(0)
        d0 = ((B - c0) ** 2).sum(1)
        d1 = ((B - c1) ** 2).sum(1)
        correct += np.sum((d1 < d0).astype(int) == y[te])
    return correct / n


def decoding(trials: int = 40, voxels: int = 1000, signal: float = 0.0, reps: int = 100, select: int = 50,
             seed: int = 0) -> dict:
    """Two categories, ``trials`` each, ``voxels`` with a per-voxel difference of ``signal`` SDs in a tenth of
    them.  Cross-validated accuracy: all voxels; voxels selected inside each fold; voxels selected on all the data
    first (the leak).  Mean over ``reps`` datasets."""
    rng = np.random.default_rng(seed)
    out = {"all": [], "nested": [], "leaky": []}
    y = np.repeat([0, 1], trials)
    for r in range(reps):
        X = rng.normal(size=(2 * trials, voxels))
        X[y == 1, : voxels // 10] += signal
        out["all"].append(_centroid_cv(X, y, 5, None, True, rng))
        out["nested"].append(_centroid_cv(X, y, 5, select, True, rng))
        out["leaky"].append(_centroid_cv(X, y, 5, select, False, rng))
    return {k: float(np.mean(v)) for k, v in out.items()} | {"signal": signal}


def rdm(P: np.ndarray) -> np.ndarray:
    """Representational dissimilarity: 1 - Pearson correlation between the patterns of each pair of stimuli."""
    return 1 - np.corrcoef(P)


def rsa(n_subj: int = 12, n_cat: int = 4, per_cat: int = 6, voxels: int = 200, noise: float = 1.5,
        seed: int = 0) -> dict:
    """Twenty-four stimuli in four categories, each with a visual feature (say, size) that cuts across category.
    A region's patterns are driven mostly by category, a little by size, plus noise.  Spearman correlations of
    each subject's RDM with a category model and a size model, and the noise ceiling (lower: each subject against
    the others' mean; upper: against the mean including themselves)."""
    rng = np.random.default_rng(seed)
    n = n_cat * per_cat
    cat = np.repeat(np.arange(n_cat), per_cat)
    size = np.tile(np.linspace(-1, 1, per_cat), n_cat)
    C = rng.normal(size=(n_cat, voxels))
    S = rng.normal(size=voxels)
    iu = np.triu_indices(n, 1)
    model_cat = (cat[:, None] != cat[None, :]).astype(float)[iu]
    model_size = np.abs(size[:, None] - size[None, :])[iu]
    subj = []
    for s in range(n_subj):
        P = C[cat] + 0.8 * np.outer(size, S) + noise * rng.normal(size=(n, voxels))
        subj.append(rdm(P)[iu])
    subj = np.array(subj)
    r_cat = [stats.spearmanr(x, model_cat)[0] for x in subj]
    r_size = [stats.spearmanr(x, model_size)[0] for x in subj]
    grand = subj.mean(0)
    upper = np.mean([stats.spearmanr(x, grand)[0] for x in subj])
    lower = np.mean([stats.spearmanr(subj[i], np.delete(subj, i, 0).mean(0))[0] for i in range(n_subj)])
    full = np.full((n, n), np.nan)
    full[iu] = grand
    full.T[iu] = grand
    np.fill_diagonal(full, 0)
    return {"r_category": float(np.mean(r_cat)), "r_size": float(np.mean(r_size)), "ceiling_low": float(lower),
            "ceiling_high": float(upper), "grand": full, "cat": cat, "size": size}


def encoding(n_train: int = 300, n_test: int = 60, features: int = 40, voxels: int = 300, reps_test: int = 2,
             noise: float = 2.0, seed: int = 0) -> dict:
    """Stimuli described by ``features``; each voxel responds to a weighted sum of them, plus noise.  A ridge
    model (penalty chosen by cross-validation on the training set) predicts held-out stimuli.  The test set is
    shown twice, so each voxel's noise ceiling is the correlation between the two repeats (Spearman-Brown to
    their mean).  Returns per-voxel prediction r and ceiling."""
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(features, voxels)) * (rng.random(voxels) < 0.7)
    Ftr = rng.normal(size=(n_train, features))
    Fte = rng.normal(size=(n_test, features))
    Ytr = Ftr @ W / np.sqrt(features) + noise * rng.normal(size=(n_train, voxels)) / np.sqrt(features) * 3
    sig_te = Fte @ W / np.sqrt(features)
    reps = [sig_te + noise * rng.normal(size=sig_te.shape) / np.sqrt(features) * 3 for _ in range(reps_test)]
    Yte = np.mean(reps, 0)

    def ridge(F, Y, lam):
        return np.linalg.solve(F.T @ F + lam * np.eye(F.shape[1]), F.T @ Y)

    lams = [0.1, 1, 10, 100, 1000]
    k = n_train // 5
    scores = []
    for lam in lams:
        sc = 0.0
        for f in range(5):
            te = slice(f * k, (f + 1) * k)
            tr = np.ones(n_train, bool)
            tr[te] = False
            B = ridge(Ftr[tr], Ytr[tr], lam)
            P = Ftr[te] @ B
            sc += np.mean([np.corrcoef(P[:, v], Ytr[te][:, v])[0, 1] for v in range(voxels)])
        scores.append(sc)
    lam = lams[int(np.argmax(scores))]
    B = ridge(Ftr, Ytr, lam)
    P = Fte @ B

    def colr(a, b):
        a = a - a.mean(0)
        b = b - b.mean(0)
        return (a * b).sum(0) / np.sqrt((a ** 2).sum(0) * (b ** 2).sum(0))

    r = colr(P, Yte)
    split = colr(reps[0], reps[1])
    ceiling = np.sqrt(np.clip(2 * split / (1 + split), 0, 1))
    return {"r": r, "ceiling": ceiling, "lambda": lam, "responsive": (np.abs(W).sum(0) > 0)}


# ----------------------------------------------------------------------------------------------------------------
# EEG: windows chosen by the data
# ----------------------------------------------------------------------------------------------------------------
def erp_windows(n_subj: int = 24, reps: int = 1000, width: int = 10, seed: int = 0) -> dict:
    """Two conditions with no difference; each subject's difference wave is smooth noise over 100 time points.
    Test a window fixed in advance, the window around the peak of the grand-average difference (double dipping),
    and the window around the peak of the conditions' average (an orthogonal localizer).  False-positive rates at
    5%."""
    rng = np.random.default_rng(seed)
    a_priori = dip = ortho = 0
    t = np.arange(100)
    comp = np.exp(-((t - 55) / 12) ** 2) * 2.0  # both conditions share this component
    for r in range(reps):
        e1 = ndimage.gaussian_filter1d(rng.normal(size=(n_subj, 100)), 4, axis=1) * 3
        e2 = ndimage.gaussian_filter1d(rng.normal(size=(n_subj, 100)), 4, axis=1) * 3
        c1, c2 = comp + e1, comp + e2
        diff = c1 - c2

        def test(lo):
            v = diff[:, lo:lo + width].mean(1)
            return stats.ttest_1samp(v, 0).pvalue < 0.05

        a_priori += test(50)
        pk = int(np.argmax(np.abs(diff.mean(0))[width // 2:100 - width // 2]))
        dip += test(min(pk, 100 - width))
        pk2 = int(np.argmax((c1 + c2).mean(0)[width // 2:100 - width // 2]))
        ortho += test(min(pk2, 100 - width))
    return {"a_priori": a_priori / reps, "double_dip": dip / reps, "orthogonal": ortho / reps}


# ----------------------------------------------------------------------------------------------------------------
# Populations of neurons
# ----------------------------------------------------------------------------------------------------------------
def cosine_population(n: int, seed: int = 0) -> dict:
    """``n`` neurons with cosine tuning to movement direction (Georgopoulos and colleagues, 1982): rate = b + m
    cos(theta - pref), Poisson spikes in a short window."""
    rng = np.random.default_rng(seed)
    base = rng.uniform(10, 30, n)
    return {"pref": rng.uniform(0, 2 * np.pi, n), "base": base, "mod": base * rng.uniform(0.3, 0.9, n)}


def population_vector_error(ns=(4, 8, 16, 32, 64, 128, 256), trials: int = 400, window: float = 0.2,
                            seed: int = 0) -> dict:
    """Mean absolute error (degrees) of the population vector, sum over neurons of (rate - base) times the
    preferred direction, as the number of recorded neurons grows."""
    rng = np.random.default_rng(seed)
    err = []
    for n in ns:
        pop = cosine_population(int(n), seed=seed + int(n))
        th = rng.uniform(0, 2 * np.pi, trials)
        lam = (pop["base"][None] + pop["mod"][None] * np.cos(th[:, None] - pop["pref"][None])) * window
        k = rng.poisson(lam) / window
        w = (k - pop["base"][None]) / pop["mod"][None]
        vx = (w * np.cos(pop["pref"][None])).sum(1)
        vy = (w * np.sin(pop["pref"][None])).sum(1)
        est = np.arctan2(vy, vx)
        d = np.angle(np.exp(1j * (est - th)))
        err.append(np.degrees(np.mean(np.abs(d))))
    return {"n": np.array(ns), "error_deg": np.array(err)}


def manifold(n: int = 100, T: int = 400, seed: int = 0) -> dict:
    """A hundred neurons during slow, continuous reaching: smoothed rates, and the share of variance in the first
    principal components.  Cosine tuning puts the signal on a two-dimensional manifold (plus noise)."""
    rng = np.random.default_rng(seed)
    pop = cosine_population(n, seed)
    th = np.cumsum(rng.normal(0, 0.15, T))
    lam = (pop["base"][None] + pop["mod"][None] * np.cos(th[:, None] - pop["pref"][None])) * 0.5
    k = rng.poisson(lam).astype(float)
    k = ndimage.gaussian_filter1d(k, 2, axis=0)
    X = k - k.mean(0)
    s = np.linalg.svd(X, compute_uv=False) ** 2
    U, _, Vt = np.linalg.svd(X, full_matrices=False)
    return {"var_share": s / s.sum(), "pcs": U[:, :2] * np.sqrt(s[:2]), "theta": th}


def wolpaw_itr(n_targets: int, accuracy: float, seconds_per_selection: float) -> float:
    """Bits per minute: B = log2 N + P log2 P + (1 - P) log2((1 - P)/(N - 1)), times selections per minute."""
    N, P = n_targets, accuracy
    b = np.log2(N)
    if 0 < P < 1:
        b += P * np.log2(P) + (1 - P) * np.log2((1 - P) / (N - 1))
    elif P == 0:
        return 0.0
    return float(b * 60 / seconds_per_selection)


# ----------------------------------------------------------------------------------------------------------------
# Brain-behaviour correlations: how many people?
# ----------------------------------------------------------------------------------------------------------------
def bwas(true_r: float = 0.1, ns=(25, 100, 500, 2000, 4000), studies: int = 4000, seed: int = 0) -> dict:
    """Correlations between one brain measure and one behaviour in samples of each size: the spread of r, the
    share significant, the mean |r| among significant results (what gets reported), and the chance that a
    significant result replicates in a new sample of the same size."""
    rng = np.random.default_rng(seed)
    out = {"n": np.array(ns), "sd": [], "power": [], "reported": [], "replicate": [], "lo": [], "hi": []}
    for n in ns:
        z = np.arctanh(true_r) + rng.normal(0, 1 / np.sqrt(n - 3), studies)
        r = np.tanh(z)
        crit = np.tanh(stats.norm.isf(0.025) / np.sqrt(n - 3))
        sig = np.abs(r) > crit
        z2 = np.arctanh(true_r) + rng.normal(0, 1 / np.sqrt(n - 3), studies)
        r2 = np.tanh(z2)
        rep = (np.abs(r2) > crit) & (np.sign(r2) == np.sign(r))
        out["sd"].append(r.std())
        out["power"].append(sig.mean())
        out["reported"].append(np.abs(r[sig]).mean() if sig.any() else np.nan)
        out["replicate"].append(rep[sig].mean() if sig.any() else np.nan)
        out["lo"].append(np.quantile(r, 0.025))
        out["hi"].append(np.quantile(r, 0.975))
    return {k: (np.array(v) if isinstance(v, list) else v) for k, v in out.items()} | {"true_r": true_r}


def attenuated(true_r: float, rel_brain: float, rel_behaviour: float) -> float:
    """Spearman's attenuation: the expected observed correlation."""
    return float(true_r * np.sqrt(rel_brain * rel_behaviour))
