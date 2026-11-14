"""Reading a brain from outside: the measurement chain from neural events to a coloured map, and where it can
mislead (videos/psychology/SYLLABUS.md, Part 8).

**A tuning curve.**  :func:`tuning_curve` is a cell's mean rate against the orientation of a bar;
:func:`spike_counts` draws Poisson counts from it, which is what a recording gives.

**EEG.**  A scalp electrode sees the sum of many small current dipoles.  :func:`dipole_sum` shows why only
aligned, synchronous sources are visible: N aligned dipoles add to N, N randomly oriented ones to about the
square root of N.  :func:`lead_field` is a toy forward model (dipoles in a uniform conductor), and
:func:`silent_source` constructs a pattern of sources that no electrode can see, which is why the inverse
problem has no unique answer.

**Event-related potentials.**  :func:`erp_trials` adds a small fixed waveform to large ongoing noise;
averaging n trials leaves the waveform and shrinks the noise by the square root of n (:func:`erp_noise`).

**MRI.**  :func:`relaxation` gives the recovery and decay of the signal after a pulse; :func:`kspace` and
:func:`from_kspace` are the Fourier transform pair that turns measured spatial frequencies into an image.

**BOLD and the linear model.**  :func:`hrf` is the canonical haemodynamic response (a difference of two gamma
densities); :func:`bold` convolves events with it; :func:`design_matrix` and :func:`glm` fit a time series by
least squares and test a contrast.

**A synthetic brain.**  :class:`SyntheticBrain` is a slice of voxels with spatially smooth noise and regions
whose activity is known.  It is analysed with each rule for thresholding a map of t statistics
(:func:`threshold_map`: uncorrected, Bonferroni, false discovery rate, cluster extent), and
:func:`familywise_rates` counts how often each rule finds something in brains where nothing is there.
:func:`cluster_calibration` reproduces the mechanism of the 2016 "cluster failure" result: an extent threshold
calibrated on noise with Gaussian smoothness, applied to noise whose smoothness has a long tail.

**Circular analysis.**  :func:`voodoo` selects the voxels that correlate best with a behavioural score and
reports the correlation in the same data and in fresh data.

**Inference.**  :func:`reverse_inference` is Bayes' rule for "this region is active, so that process is
engaged"; :func:`r_ceiling` is the largest correlation two imperfectly reliable measures can show;
:func:`n_for_correlation` and :func:`small_study` say what a sample of 25 can and cannot detect.

Nothing here imports manim.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import ndimage, stats

# ---------------------------------------------------------------------------------------------------------------
# A neuron's tuning curve
# ---------------------------------------------------------------------------------------------------------------


def tuning_curve(theta_deg, pref: float = 45.0, width: float = 20.0, peak: float = 40.0, base: float = 2.0):
    """Mean firing rate (spikes a second) of an orientation-tuned cell to a bar at ``theta_deg``.  Orientation
    repeats every 180 degrees; ``width`` is the standard deviation of the tuning, in degrees."""
    d = (np.asarray(theta_deg, float) - pref + 90.0) % 180.0 - 90.0
    return base + (peak - base) * np.exp(-0.5 * (d / width) ** 2)


def spike_counts(theta_deg, trials: int = 10, window: float = 0.5, rng=None, **kw) -> np.ndarray:
    """Poisson spike counts in ``window`` seconds, ``trials`` times at each orientation: (orientations, trials)."""
    rng = rng or np.random.default_rng(0)
    rate = np.atleast_1d(tuning_curve(theta_deg, **kw))
    return rng.poisson(rate[:, None] * window, (len(rate), trials))


# ---------------------------------------------------------------------------------------------------------------
# EEG: what a scalp electrode can and cannot see
# ---------------------------------------------------------------------------------------------------------------


def dipole_sum(n: int, aligned: bool, repeats: int = 400, rng=None) -> float:
    """Mean size of the summed moment of ``n`` unit dipoles, all pointing one way or each in a random direction
    in the plane."""
    rng = rng or np.random.default_rng(0)
    if aligned:
        return float(n)
    a = rng.uniform(0, 2 * np.pi, (repeats, n))
    return float(np.hypot(np.cos(a).sum(axis=1), np.sin(a).sum(axis=1)).mean())


def electrodes(n: int = 9, radius: float = 1.0) -> np.ndarray:
    """``n`` electrodes over the upper half of a circular head: positions (n, 2)."""
    a = np.linspace(np.pi * 0.08, np.pi * 0.92, n)
    return radius * np.c_[np.cos(a), np.sin(a)]


def source_grid(n: int = 6, radius: float = 0.75) -> np.ndarray:
    """Candidate source positions on a grid inside the head: (m, 2)."""
    g = np.linspace(-radius, radius, n)
    xx, yy = np.meshgrid(g, g)
    keep = (xx ** 2 + yy ** 2 <= radius ** 2) & (yy > -0.2)
    return np.c_[xx[keep], yy[keep]]


def lead_field(elec: np.ndarray, src: np.ndarray) -> np.ndarray:
    """The potential at each electrode of a unit radial dipole at each source, in a uniform conductor:
    V = p . (r_e - r_s) / |r_e - r_s|^3.  A toy: a real head has a skull that smears the field further.
    Returns (electrodes, sources)."""
    d = elec[:, None, :] - src[None, :, :]
    dist = np.linalg.norm(d, axis=2)
    p = src / np.maximum(np.linalg.norm(src, axis=1, keepdims=True), 1e-9)  # radial orientation
    return (d * p[None, :, :]).sum(axis=2) / dist ** 3


def silent_source(L: np.ndarray, rng=None) -> np.ndarray:
    """A pattern of source strengths that produces no potential at any electrode: a unit vector of the lead
    field's null space (it exists whenever there are more sources than electrodes)."""
    rng = rng or np.random.default_rng(0)
    _, s, vt = np.linalg.svd(L)
    null = vt[len(s):]
    if not len(null):
        raise ValueError("no null space: as many electrodes as sources")
    v = null.T @ rng.standard_normal(len(null))
    return v / np.linalg.norm(v)


# ---------------------------------------------------------------------------------------------------------------
# Event-related potentials
# ---------------------------------------------------------------------------------------------------------------


def erp_template(t_ms, kind: str = "n400") -> np.ndarray:
    """A schematic component, in microvolts, against time from the word's onset in ms."""
    t = np.asarray(t_ms, float)
    early = 1.5 * np.exp(-0.5 * ((t - 100) / 25) ** 2) - 2.0 * np.exp(-0.5 * ((t - 170) / 30) ** 2)
    if kind == "n400":
        return early - 5.0 * np.exp(-0.5 * ((t - 400) / 70) ** 2)
    if kind == "p300":
        return early + 8.0 * np.exp(-0.5 * ((t - 350) / 80) ** 2)
    if kind == "none":
        return early
    raise ValueError(kind)


def erp_trials(n: int, t_ms, kind: str = "n400", noise_sd: float = 20.0, smooth_ms: float = 40.0, rng=None):
    """``n`` single trials: the component plus ongoing EEG (smoothed noise of standard deviation ``noise_sd``
    microvolts).  Returns (n, len(t))."""
    rng = rng or np.random.default_rng(0)
    t = np.asarray(t_ms, float)
    dt = float(t[1] - t[0])
    noise = ndimage.gaussian_filter1d(rng.standard_normal((n, len(t))), smooth_ms / dt, axis=1, mode="wrap")
    noise *= noise_sd / noise.std()
    return erp_template(t, kind)[None, :] + noise


def erp_noise(noise_sd: float, n) -> np.ndarray:
    """The noise left in an average of ``n`` trials: sd / sqrt(n)."""
    return noise_sd / np.sqrt(np.asarray(n, float))


# ---------------------------------------------------------------------------------------------------------------
# MRI
# ---------------------------------------------------------------------------------------------------------------


def relaxation(t_ms, t1: float = 1000.0, t2: float = 80.0) -> dict:
    """After a 90-degree pulse: the recovery of the magnetization along the field, 1 - exp(-t/T1), and the
    decay of the signal across it, exp(-t/T2)."""
    t = np.asarray(t_ms, float)
    return {"recovery": 1 - np.exp(-t / t1), "decay": np.exp(-t / t2)}


def kspace(image: np.ndarray) -> np.ndarray:
    """What the scanner measures: the image's two-dimensional Fourier transform, centre of k-space in the
    middle."""
    return np.fft.fftshift(np.fft.fft2(image))


def from_kspace(k: np.ndarray, keep: float = 1.0) -> np.ndarray:
    """The image from k-space, using only the central ``keep`` share of spatial frequencies in each direction."""
    n0, n1 = k.shape
    mask = np.zeros(k.shape, bool)
    h0, h1 = max(1, int(round(n0 * keep / 2))), max(1, int(round(n1 * keep / 2)))
    mask[n0 // 2 - h0:n0 // 2 + h0, n1 // 2 - h1:n1 // 2 + h1] = True
    return np.abs(np.fft.ifft2(np.fft.ifftshift(np.where(mask, k, 0))))


def phantom(n: int = 64) -> np.ndarray:
    """A head-shaped test image: an ellipse with two ventricles and a small bright spot."""
    y, x = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    im = np.zeros((n, n))
    im[(x / 0.72) ** 2 + (y / 0.9) ** 2 <= 1] = 0.6
    im[(x / 0.62) ** 2 + (y / 0.8) ** 2 <= 1] = 0.85
    for cx in (-0.17, 0.17):
        im[((x - cx) / 0.09) ** 2 + ((y + 0.05) / 0.26) ** 2 <= 1] = 0.25
    im[(x - 0.3) ** 2 + (y - 0.4) ** 2 <= 0.006] = 1.0
    return im


# ---------------------------------------------------------------------------------------------------------------
# BOLD and the general linear model
# ---------------------------------------------------------------------------------------------------------------


def hrf(t, peak: float = 6.0, under: float = 16.0, ratio: float = 1 / 6) -> np.ndarray:
    """The canonical haemodynamic response at times ``t`` (s): a gamma density that peaks near 5 s minus a
    smaller, later one (the undershoot), scaled to a peak of 1."""
    t = np.asarray(t, float)
    h = stats.gamma.pdf(t, peak) - ratio * stats.gamma.pdf(t, under)
    tt = np.linspace(0, 32, 3201)
    top = (stats.gamma.pdf(tt, peak) - ratio * stats.gamma.pdf(tt, under)).max()
    return h / top


def bold(onsets, n_scans: int, tr: float = 2.0, duration: float = 0.0, dt: float = 0.1) -> np.ndarray:
    """The predicted BOLD time course, sampled every ``tr`` seconds: events at ``onsets`` (s), each lasting
    ``duration``, convolved with the haemodynamic response.  With ``duration`` 0 an event is a unit impulse, so
    one event's response is the haemodynamic response itself (peak 1); a sustained block's plateau is the
    response's area."""
    total = n_scans * tr
    grid = np.arange(0, total, dt)
    neural = np.zeros(len(grid))
    for o in np.atleast_1d(onsets):
        a = int(round(o / dt))
        if duration <= 0:
            if a < len(grid):
                neural[a] += 1.0 / dt
        else:
            neural[a:min(int(round((o + duration) / dt)), len(grid))] += 1.0
    kernel = hrf(np.arange(0, 32, dt)) * dt
    y = np.convolve(neural, kernel)[:len(grid)]
    return y[(np.arange(n_scans) * tr / dt).round().astype(int)]


def design_matrix(conditions: dict, n_scans: int, tr: float = 2.0, duration: float = 0.0) -> np.ndarray:
    """One column for each condition's predicted response, and a constant: (scans, conditions + 1)."""
    cols = [bold(on, n_scans, tr, duration) for on in conditions.values()]
    return np.c_[np.array(cols).T, np.ones(n_scans)]


def glm(Y: np.ndarray, X: np.ndarray, contrast) -> dict:
    """Least squares for every column of ``Y`` (scans, voxels) at once, and the t statistic of ``contrast``."""
    Y = np.asarray(Y, float)
    if Y.ndim == 1:
        Y = Y[:, None]
    c = np.asarray(contrast, float)
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ Y
    resid = Y - X @ beta
    df = X.shape[0] - np.linalg.matrix_rank(X)
    s2 = (resid ** 2).sum(axis=0) / df
    se = np.sqrt(s2 * (c @ xtx_inv @ c))
    t = (c @ beta) / se
    return {"beta": beta, "t": t, "df": int(df), "p": stats.t.sf(t, df), "effect": c @ beta}


# ---------------------------------------------------------------------------------------------------------------
# A synthetic brain, and the rules for thresholding its map
# ---------------------------------------------------------------------------------------------------------------


def smooth_noise(shape, fwhm: float, rng, long_tail: float = 0.0, long_fwhm: float | None = None) -> np.ndarray:
    """Spatially smooth noise with unit variance.  ``fwhm`` (voxels) sets a Gaussian autocorrelation; with
    ``long_tail`` a share of the variance comes from a much smoother field, which gives the autocorrelation the
    long tail real fMRI noise has."""
    def one(f):
        z = ndimage.gaussian_filter(rng.standard_normal(shape), [0] * (len(shape) - 2) + [f / 2.355] * 2,
                                    mode="wrap")
        return z / z.std()

    z = one(fwhm)
    if long_tail > 0:
        z = math.sqrt(1 - long_tail) * z + math.sqrt(long_tail) * one(long_fwhm or 4 * fwhm)
        z /= z.std()
    return z


class SyntheticBrain:
    """A slice of ``size`` x ``size`` voxels inside an elliptical mask.  ``regions`` is a list of
    (row, column, radius, amplitude): discs whose response to the task has the given size, in units of the
    noise's standard deviation.  Everything outside them responds with zero."""

    def __init__(self, size: int = 48, regions=((16, 15, 3.0, 0.9), (30, 33, 4.0, 0.7)), fwhm: float = 3.0,
                 long_tail: float = 0.0):
        self.size, self.fwhm, self.long_tail = size, fwhm, long_tail
        y, x = np.mgrid[0:size, 0:size]
        c = (size - 1) / 2
        self.mask = ((x - c) / (0.46 * size)) ** 2 + ((y - c) / (0.48 * size)) ** 2 <= 1
        self.truth = np.zeros((size, size))
        for r, cc, rad, amp in regions:
            self.truth[(y - r) ** 2 + (x - cc) ** 2 <= rad ** 2] = amp
        self.truth *= self.mask
        self.active = self.truth > 0

    def scan(self, n_scans: int = 120, tr: float = 2.0, period: float = 40.0, rng=None, null: bool = False) -> dict:
        """One run of a block design (task on for half of every ``period`` seconds): data (scans, size, size),
        the design matrix and the t map of the task regressor."""
        rng = rng or np.random.default_rng(0)
        onsets = np.arange(period / 2, n_scans * tr - period / 2 + 1e-9, period)
        X = design_matrix({"task": onsets}, n_scans, tr, duration=period / 2)
        noise = smooth_noise((n_scans, self.size, self.size), self.fwhm, rng, self.long_tail)
        signal = 0 if null else X[:, 0][:, None, None] * self.truth[None, :, :]
        Y = signal + noise
        fit = glm(Y.reshape(n_scans, -1), X, [1, 0])
        t = fit["t"].reshape(self.size, self.size)
        return {"Y": Y, "X": X, "t": np.where(self.mask, t, 0.0), "df": fit["df"], "onsets": onsets}


def clusters(above: np.ndarray):
    """Connected clusters (edge neighbours) of a boolean map: (labels, sizes)."""
    lab, n = ndimage.label(above)
    return lab, (np.bincount(lab.ravel())[1:] if n else np.array([], int))


def fdr_threshold(p: np.ndarray, q: float = 0.05) -> float:
    """Benjamini and Hochberg's rule: the largest p(k) with p(k) <= q k / m, or 0 if none."""
    ps = np.sort(np.asarray(p).ravel())
    ok = ps <= q * np.arange(1, len(ps) + 1) / len(ps)
    return float(ps[ok].max()) if ok.any() else 0.0


def threshold_map(t: np.ndarray, df: int, mask: np.ndarray, rule: str, alpha: float = 0.05, primary: float = 0.001,
                  extent: int = 0) -> np.ndarray:
    """The voxels a rule declares active.  ``rule``: "uncorrected" (p < ``primary`` at each voxel),
    "bonferroni" (p < alpha / voxels), "fdr" (false discovery rate ``alpha``), or "cluster" (p < ``primary``
    in a cluster of at least ``extent`` voxels)."""
    p = np.where(mask, stats.t.sf(t, df), 1.0)
    m = int(mask.sum())
    if rule == "uncorrected":
        return p < primary
    if rule == "bonferroni":
        return p < alpha / m
    if rule == "fdr":
        return p <= fdr_threshold(p[mask], alpha)
    if rule == "cluster":
        lab, sizes = clusters(p < primary)
        keep = np.flatnonzero(sizes >= extent) + 1
        return np.isin(lab, keep)
    raise ValueError(rule)


def null_tmaps(brains: int, size: int = 48, fwhm: float = 3.0, long_tail: float = 0.0, df: int = 118, rng=None):
    """t maps of brains in which nothing responds: smooth noise with a t distribution's tails, (brains, size,
    size), and the mask.  (A shortcut for scanning a null brain; the smoothness of the map is that of the
    noise.)"""
    rng = rng or np.random.default_rng(0)
    b = SyntheticBrain(size, regions=(), fwhm=fwhm, long_tail=long_tail)
    z = smooth_noise((brains, size, size), fwhm, rng, long_tail)
    chi = rng.chisquare(df, (brains, 1, 1)) / df
    return np.where(b.mask[None], z / np.sqrt(chi), 0.0), b.mask


def cluster_extent(tmaps: np.ndarray, mask: np.ndarray, df: int, primary: float = 0.001, alpha: float = 0.05) -> int:
    """The smallest cluster size that null maps exceed in fewer than ``alpha`` of brains: an extent threshold
    calibrated by simulation."""
    biggest = []
    for t in tmaps:
        _, sizes = clusters(np.where(mask, stats.t.sf(t, df), 1.0) < primary)
        biggest.append(sizes.max() if len(sizes) else 0)
    return int(np.quantile(biggest, 1 - alpha)) + 1


def familywise_rates(tmaps: np.ndarray, mask: np.ndarray, df: int, extent: int, alpha: float = 0.05,
                     primary: float = 0.001) -> dict:
    """For brains with nothing in them: the share in which each rule declares at least one voxel active, and
    the mean number of voxels the uncorrected rule declares."""
    out = {r: 0 for r in ("uncorrected", "bonferroni", "fdr", "cluster")}
    count = 0
    for t in tmaps:
        for r in out:
            hit = threshold_map(t, df, mask, r, alpha, primary, extent)
            out[r] += bool(hit.any())
            if r == "uncorrected":
                count += int(hit.sum())
    n = len(tmaps)
    return {**{r: v / n for r, v in out.items()}, "voxels": int(mask.sum()), "mean_uncorrected_voxels": count / n}


def cluster_calibration(brains: int = 400, fwhm: float = 3.0, long_tail: float = 0.35, df: int = 118,
                        primary: float = 0.01, rng=None) -> dict:
    """An extent threshold calibrated on noise with a Gaussian autocorrelation of width ``fwhm``, then applied
    to noise of the same local smoothness whose autocorrelation has a long tail.  Returns the extent and the
    familywise rate in each kind of noise."""
    rng = rng or np.random.default_rng(0)
    calib, mask = null_tmaps(brains, fwhm=fwhm, df=df, rng=rng)
    extent = cluster_extent(calib, mask, df, primary)
    fresh, _ = null_tmaps(brains, fwhm=fwhm, df=df, rng=rng)
    tail, _ = null_tmaps(brains, fwhm=fwhm, long_tail=long_tail, df=df, rng=rng)

    def rate(maps):
        return float(np.mean([threshold_map(t, df, mask, "cluster", primary=primary, extent=extent).any()
                              for t in maps]))

    return {"extent": extent, "gaussian": rate(fresh), "long_tail": rate(tail), "primary": primary}


def chance_of_any(voxels: int, p: float = 0.001) -> float:
    """The chance that at least one of ``voxels`` independent tests passes at level ``p`` when nothing is
    there."""
    return 1 - (1 - p) ** voxels


# ---------------------------------------------------------------------------------------------------------------
# Circular analysis
# ---------------------------------------------------------------------------------------------------------------


def voodoo(subjects: int = 16, voxels: int = 10000, true_r: float = 0.0, signal_share: float = 0.0,
           threshold: float = 0.6, rng=None) -> dict:
    """Each subject has a behavioural score and an activation in every voxel.  A share ``signal_share`` of
    voxels truly correlates ``true_r`` with the score; the rest do not.  Select the voxels whose correlation
    with the score exceeds ``threshold``, and report their mean correlation in the same data and in a second,
    independent set of scans of the same subjects."""
    rng = rng or np.random.default_rng(0)
    score = rng.standard_normal(subjects)
    n_sig = int(round(signal_share * voxels))

    def scans():
        a = rng.standard_normal((subjects, voxels))
        if n_sig:
            a[:, :n_sig] = true_r * score[:, None] + math.sqrt(1 - true_r ** 2) * a[:, :n_sig]
        return a

    def corr(a):
        z = (score - score.mean()) / score.std()
        return ((a - a.mean(axis=0)) / a.std(axis=0) * z[:, None]).mean(axis=0)

    r1, r2 = corr(scans()), corr(scans())
    chosen = r1 > threshold
    k = int(chosen.sum())
    return {"selected": k, "r_same": float(r1[chosen].mean()) if k else float("nan"),
            "r_fresh": float(r2[chosen].mean()) if k else float("nan"), "r_all": r1, "chosen": chosen,
            "score": score, "true_selected": int(chosen[:n_sig].sum())}


# ---------------------------------------------------------------------------------------------------------------
# Inference from a map
# ---------------------------------------------------------------------------------------------------------------


def reverse_inference(prior: float, p_active_given_process: float, p_active_given_not: float) -> dict:
    """P(process | region active) by Bayes' rule, and the factor by which the activation multiplies the odds."""
    num = p_active_given_process * prior
    post = num / (num + p_active_given_not * (1 - prior))
    return {"posterior": post, "bayes_factor": p_active_given_process / p_active_given_not}


def r_ceiling(reliability_x: float, reliability_y: float) -> float:
    """The largest correlation two measures can show if their true scores correlate perfectly."""
    return math.sqrt(reliability_x * reliability_y)


def r_critical(n: int, alpha: float = 0.05) -> float:
    """The smallest |r| that is significant (two-sided) in a sample of ``n``."""
    t = stats.t.ppf(1 - alpha / 2, n - 2)
    return float(t / math.sqrt(n - 2 + t ** 2))


def n_for_correlation(r: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """The sample needed to detect a true correlation ``r`` (Fisher's z approximation)."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return int(math.ceil((z / math.atanh(r)) ** 2 + 3))


def small_study(true_r: float, n: int = 25, studies: int = 20000, alpha: float = 0.05, rng=None) -> dict:
    """Many studies of ``n`` people of an association whose true size is ``true_r``: the share that reach
    significance, the mean |r| among those that do, and the share of those with the wrong sign."""
    rng = rng or np.random.default_rng(0)
    x = rng.standard_normal((studies, n))
    y = true_r * x + math.sqrt(1 - true_r ** 2) * rng.standard_normal((studies, n))
    xc, yc = x - x.mean(axis=1, keepdims=True), y - y.mean(axis=1, keepdims=True)
    r = (xc * yc).sum(axis=1) / np.sqrt((xc ** 2).sum(axis=1) * (yc ** 2).sum(axis=1))
    sig = np.abs(r) >= r_critical(n, alpha)
    return {"power": float(sig.mean()), "mean_sig_r": float(np.abs(r[sig]).mean()), "r": r,
            "wrong_sign": float((r[sig] * np.sign(true_r or 1) < 0).mean()), "critical": r_critical(n, alpha)}
