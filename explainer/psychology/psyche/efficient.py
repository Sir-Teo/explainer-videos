"""Psyche's efficient codes (Part 58): the mind's mechanisms derived from an optimization principle.

Dead-leaves images (occluding discs of random size and grey level, a standard synthetic model of natural-image
statistics: edges, occlusion and a roughly 1/f spectrum), whitening and Olshausen-Field sparse coding by ISTA with
dictionary learning; Laughlin's histogram-matching contrast code; efficient-coding biases (Wei and Stocker): Fisher
information proportional to the prior, and repulsion away from the prior's peak; Blahut-Arimoto rate-distortion
and the generalization gradient it implies (Sims); divisive normalization; a linear predictive-coding hierarchy with
error units; the variational free energy of a Gaussian model; the tilt after-effect from adaptation in a population
code; and resource-rational sampling ("one and done").  numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


# ----------------------------------------------------------------------------------------------------------------
# Images and sparse coding
# ----------------------------------------------------------------------------------------------------------------
def dead_leaves(size: int = 128, n_discs: int = 3000, rmin: float = 1.5, rmax: float = 40.0, alpha: float = 3.0,
                seed: int = 0) -> np.ndarray:
    """A dead-leaves image: discs dropped one on top of another, radius density proportional to r^-alpha between
    rmin and rmax, grey levels uniform; later discs occlude earlier ones."""
    rng = np.random.default_rng(seed)
    img = np.full((size, size), np.nan)
    yy, xx = np.mgrid[0:size, 0:size]
    u = rng.random(n_discs)
    a1 = 1 - alpha
    r = (rmin ** a1 + u * (rmax ** a1 - rmin ** a1)) ** (1 / a1)
    cx, cy = rng.uniform(-rmax, size + rmax, n_discs), rng.uniform(-rmax, size + rmax, n_discs)
    g = rng.random(n_discs)
    for k in range(n_discs):  # first disc dropped is on top: fill only empty pixels
        m = np.isnan(img) & ((xx - cx[k]) ** 2 + (yy - cy[k]) ** 2 <= r[k] ** 2)
        img[m] = g[k]
        if not np.isnan(img).any():
            break
    img[np.isnan(img)] = rng.random()
    return img


def patches(images, size: int = 8, n: int = 20000, seed: int = 0) -> np.ndarray:
    """Random size x size patches, each with its mean removed: an (n, size*size) array."""
    rng = np.random.default_rng(seed)
    out = np.empty((n, size * size))
    for i in range(n):
        im = images[rng.integers(len(images))]
        y, x = rng.integers(0, im.shape[0] - size, 2)
        p = im[y:y + size, x:x + size].ravel()
        out[i] = p - p.mean()
    return out


def zca(X: np.ndarray, eps: float = 1e-2) -> tuple:
    """ZCA whitening: rotate to principal components, scale each to unit variance (eps regularizes), rotate back.
    Returns the whitened data, the whitening matrix and the eigenvalues (the power spectrum of the patches)."""
    C = np.cov(X, rowvar=False)
    ev, E = np.linalg.eigh(C)
    W = E @ np.diag(1 / np.sqrt(ev + eps * ev.max())) @ E.T
    return X @ W, W, ev[::-1]


def sparse_code(X: np.ndarray, D: np.ndarray, lam: float = 0.1, iters: int = 60) -> np.ndarray:
    """ISTA for min_a ||x - D a||^2 / 2 + lam ||a||_1, for every row of X at once."""
    L = np.linalg.norm(D, 2) ** 2
    A = np.zeros((X.shape[0], D.shape[1]))
    for _ in range(iters):
        G = (A @ D.T - X) @ D
        Z = A - G / L
        A = np.sign(Z) * np.maximum(np.abs(Z) - lam / L, 0)
    return A


def learn_dictionary(X: np.ndarray, atoms: int = 64, lam: float = 0.4, epochs: int = 400, batch: int = 500,
                     lr: float = 1.0, seed: int = 0, snapshots=(), iters: int = 80) -> dict:
    """Olshausen and Field's sparse coding: alternate ISTA inference with a gradient step on the dictionary, columns
    renormalized to unit length.  The dictionary starts from high-contrast data patches and the step size decays
    linearly (to 5% of ``lr`` plus a floor), which avoids dead atoms.  Returns the dictionary (columns are basis
    functions), the reconstruction error and the fraction of zero coefficients over training; ``snapshots`` lists
    epochs at which a copy of the dictionary is kept (epoch 0 is the start)."""
    rng = np.random.default_rng(seed)
    norms = np.linalg.norm(X, axis=1)
    pool = np.where(norms > np.median(norms))[0]
    D = X[rng.choice(pool, atoms, replace=False)].T.copy()
    D /= np.linalg.norm(D, axis=0)
    err, sparsity, snaps = [], [], {}
    if 0 in snapshots:
        snaps[0] = D.copy()
    for e in range(epochs):
        xb = X[rng.integers(0, len(X), batch)]
        A = sparse_code(xb, D, lam, iters)
        R = xb - A @ D.T
        D += (lr * (1 - e / epochs) + 0.05) * R.T @ A / batch
        D /= np.maximum(np.linalg.norm(D, axis=0), 1e-9)
        err.append(float(np.mean(R ** 2) / np.mean(xb ** 2)))
        sparsity.append(float(np.mean(A == 0)))
        if e + 1 in snapshots:
            snaps[e + 1] = D.copy()
    return {"D": D, "err": np.array(err), "sparsity": np.array(sparsity), "snapshots": snaps}


def localization(D: np.ndarray, size: int = 8) -> dict:
    """How localized and oriented each basis function is: the share of its energy in its strongest 3x3 neighbourhood
    and the coherence of its gradient orientation (1 = a single orientation)."""
    loc, ori = [], []
    for k in range(D.shape[1]):
        f = D[:, k].reshape(size, size)
        e = f ** 2
        best = 0.0
        for y in range(size - 2):
            for x in range(size - 2):
                best = max(best, e[y:y + 3, x:x + 3].sum())
        loc.append(best / e.sum())
        gy, gx = np.gradient(f)
        jxx, jyy, jxy = (gx * gx).sum(), (gy * gy).sum(), (gx * gy).sum()
        ori.append(np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / max(jxx + jyy, 1e-12))
    return {"localization": np.array(loc), "orientedness": np.array(ori)}


# ----------------------------------------------------------------------------------------------------------------
# Efficient coding of a single variable
# ----------------------------------------------------------------------------------------------------------------
def laughlin(contrasts, levels: int = 20) -> dict:
    """Laughlin (1981): a neuron with limited response levels uses them all equally often if its response is the
    cumulative distribution of its inputs.  Returns the input grid, the histogram and the optimal response curve."""
    c = np.sort(np.asarray(contrasts, float))
    grid = np.linspace(c[0], c[-1], 200)
    cdf = np.searchsorted(c, grid) / len(c)
    hist, edges = np.histogram(c, bins=40, density=True)
    return {"grid": grid, "response": cdf, "hist": hist, "edges": edges, "levels": levels}


def efficient_bias(prior_kind: str = "cardinal", noise: float = 0.08, n_grid: int = 360) -> dict:
    """Wei and Stocker (2015): an encoder whose Fisher information follows the prior (sqrt J proportional to p)
    and a Bayesian decoder with the same prior.  Orientation on [0, 180).  The encoder adds noise in the warped
    space F(theta) = CDF of the prior; the decoder's posterior mean is computed numerically.  Returns the bias
    (estimate - truth): repulsive, away from the prior's peaks, rather than attractive."""
    th = np.linspace(0, 180, n_grid, endpoint=False)
    if prior_kind == "cardinal":
        p = 2 - np.abs(np.sin(np.deg2rad(2 * th)))  # peaks at 0 and 90
    else:
        p = np.ones_like(th)
    p = p / p.sum()
    F = np.cumsum(p)  # warp, 0..1
    bias = np.zeros(n_grid)
    for i in range(n_grid):
        m = F[i]
        # likelihood over theta of measurement m' ~ N(F(theta), noise) on the circle, averaged over m'
        ms = m + noise * np.linspace(-2.5, 2.5, 41)
        wm = stats.norm.pdf(np.linspace(-2.5, 2.5, 41))
        est = 0.0
        for mm, ww in zip(ms, wm):
            d = (mm - F + 0.5) % 1 - 0.5
            post = p * np.exp(-d ** 2 / (2 * noise ** 2))
            post /= post.sum()
            ang = np.angle(np.sum(post * np.exp(1j * np.deg2rad(2 * th)))) / 2
            est += ww * ((np.rad2deg(ang) - th[i] + 90) % 180 - 90)
        bias[i] = est / wm.sum()
    return {"theta": th, "prior": p * n_grid / 180, "bias": bias}


def blahut_arimoto(n: int = 41, beta: float = 0.5, iters: int = 300) -> dict:
    """Rate-distortion by the Blahut-Arimoto algorithm for stimuli and responses on a line of n points with
    squared-error distortion: the channel p(response | stimulus) that minimizes rate + beta x distortion.  Sims
    (2018): its generalization gradient, how often a stimulus is confused with one at distance d, falls off
    roughly exponentially, as in Shepard's law."""
    x = np.arange(n, dtype=float)
    Dm = (x[:, None] - x[None, :]) ** 2
    q = np.full(n, 1 / n)
    for _ in range(iters):
        Pc = q[None, :] * np.exp(-beta * Dm)
        Pc /= Pc.sum(1, keepdims=True)
        q = Pc.mean(0)
    rate = float(np.sum(Pc / n * np.log2(np.maximum(Pc, 1e-300) / np.maximum(q[None, :], 1e-300))))
    dist = float(np.sum(Pc / n * Dm))
    mid = n // 2
    return {"channel": Pc, "rate": rate, "distortion": dist, "gradient": Pc[mid, mid:] / Pc[mid, mid],
            "distance": x[mid:] - x[mid]}


def generalization(betas=(0.05, 0.2, 0.8), n: int = 41) -> dict:
    """The generalization gradient at several costs of error: a cheap, low-rate code generalizes broadly."""
    out = {"distance": None, "gradients": [], "rates": []}
    for b in betas:
        r = blahut_arimoto(n=n, beta=b)
        out["distance"] = r["distance"]
        out["gradients"].append(r["gradient"])
        out["rates"].append(r["rate"])
    out["gradients"] = np.array(out["gradients"])
    out["rates"] = np.array(out["rates"])
    out["betas"] = np.array(betas)
    return out


# ----------------------------------------------------------------------------------------------------------------
# Normalization, predictive coding, free energy
# ----------------------------------------------------------------------------------------------------------------
def normalization(contrast, mask: float = 0.0, n: float = 2.0, sigma: float = 0.15, rmax: float = 1.0):
    """Divisive normalization (Heeger; Carandini and Heeger 2012): R = rmax c^n / (sigma^n + c^n + m^n): the
    contrast response saturates, and a mask that drives the pool but not the cell suppresses it."""
    c = np.asarray(contrast, float)
    return rmax * c ** n / (sigma ** n + c ** n + mask ** n)


def predictive_coding(D: np.ndarray, x: np.ndarray, prior_mean: np.ndarray, prior_prec: float = 1.0,
                      steps: int = 80, lr: float = 0.1) -> dict:
    """A two-level linear predictive-coding loop (Rao and Ballard 1999): the cause r predicts the input as D r;
    error units carry e0 = x - D r (bottom-up) and e1 = r - prior (top-down); r descends the summed squared error.
    Returns the error-unit activity over the settling steps, and the final error."""
    r = prior_mean.copy()
    e0s, e1s = [], []
    for _ in range(steps):
        e0 = x - D @ r
        e1 = prior_prec * (r - prior_mean)
        r += lr * (D.T @ e0 - e1)
        e0s.append(float(np.linalg.norm(e0)))
        e1s.append(float(np.linalg.norm(e1)))
    return {"e0": np.array(e0s), "e1": np.array(e1s), "r": r}


def free_energy_gaussian(x: float = 2.0, prior_sd: float = 1.0, noise_sd: float = 0.5, mus=None) -> dict:
    """The variational free energy of a one-dimensional Gaussian model, z ~ N(0, prior_sd^2), x | z ~ N(z,
    noise_sd^2), with q(z) = N(mu, s^2) at the posterior s: F(mu) = E_q[log q - log p(x, z)] = KL(q || p(z|x)) -
    log p(x).  Minimizing F over q gives the exact posterior and F = -log p(x) (surprise).  Returns F over mu, the
    posterior mean and the surprise."""
    mus = np.linspace(-1, 3, 201) if mus is None else np.asarray(mus, float)
    post_var = 1 / (1 / prior_sd ** 2 + 1 / noise_sd ** 2)
    post_mu = post_var * x / noise_sd ** 2
    s2 = post_var
    surprise = -stats.norm.logpdf(x, 0, np.sqrt(prior_sd ** 2 + noise_sd ** 2))
    kl = 0.5 * ((s2 + (mus - post_mu) ** 2) / post_var - 1 + np.log(post_var / s2))
    return {"mu": mus, "F": kl + surprise, "post_mu": float(post_mu), "surprise": float(surprise)}


# ----------------------------------------------------------------------------------------------------------------
# Adaptation, resource rationality
# ----------------------------------------------------------------------------------------------------------------
def tilt_aftereffect(adapter: float = 0.0, tests=None, n_units: int = 72, width: float = 20.0, gain_loss: float = 0.5,
                     adapt_width: float = 20.0) -> dict:
    """A population of orientation-tuned units; adaptation lowers the gain of units tuned near the adapter.  A test
    orientation is decoded by a population vector that assumes the unadapted gains, so it is pushed away from the
    adapter: the tilt after-effect, largest about 10 to 20 degrees from the adapter."""
    tests = np.linspace(-45, 45, 37) if tests is None else np.asarray(tests, float)
    pref = np.linspace(-90, 90, n_units, endpoint=False)

    def tuning(theta):
        d = (theta - pref + 90) % 180 - 90
        return np.exp(-d ** 2 / (2 * width ** 2))

    da = (adapter - pref + 90) % 180 - 90
    gain = 1 - gain_loss * np.exp(-da ** 2 / (2 * adapt_width ** 2))
    shift = []
    for t in tests:
        r = gain * tuning(t)
        ang = np.angle(np.sum(r * np.exp(1j * np.deg2rad(2 * pref)))) / 2
        shift.append((np.rad2deg(ang) - t + 90) % 180 - 90)
    return {"tests": tests, "shift": np.array(shift)}


def samples_value(ks=(1, 2, 3, 5, 10, 20, 50), p_correct_evidence: float = 0.65, cost_per_sample: float = 0.02,
                  time_value: float = 0.0) -> dict:
    """Vul, Goodman, Griffiths and Tenenbaum's "one and done": a decision made by drawing k samples from the
    posterior and taking the majority.  Accuracy rises with k, but if each sample costs time, the reward rate peaks
    at very few samples."""
    ks = np.asarray(ks)
    acc = []
    for k in ks:
        j = np.arange(k + 1)
        pk = stats.binom.pmf(j, k, p_correct_evidence)
        a = pk[j > k / 2].sum() + 0.5 * pk[j == k / 2].sum()
        acc.append(a)
    acc = np.array(acc)
    rate = acc / (1 + cost_per_sample * ks * 50)  # decisions per unit time, each sample costing time
    return {"k": ks, "accuracy": acc, "reward_rate": rate, "best_k": int(ks[np.argmax(rate)])}
