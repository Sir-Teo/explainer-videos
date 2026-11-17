"""Psyche's perception as inference: a percept is the best guess about a world the image underdetermines.

* **Bayes with Gaussians**: a prior and a likelihood combine into a posterior whose mean is a reliability-weighted
  average and whose variance is smaller than either; the general rule for any number of cues.
* **Cue combination** (Ernst and Banks 2002): an observer with a noisy visual and a noisy haptic estimate of height,
  run in two-interval discrimination; thresholds fitted for each cue alone, the optimal combination predicted from
  them, and checked against the combined condition; conflict trials reveal the weights.
* **The slow-motion prior** (Weiss, Simoncelli and Adelson 2002): speed estimates shrink toward zero more when
  contrast is low (the likelihood is broad); for edges, each gives only the velocity along its normal (the aperture
  problem), and the MAP velocity moves from the intersection of constraints toward a slower, rotated estimate as
  contrast falls.
* **Lightness**: a checkerboard under a soft shadow (two squares of equal luminance), and a retinex that keeps sharp
  edges and discards gentle gradients, recovering reflectances in which the shadowed square is the lighter.
* **Depth**: binocular disparity from geometry, and a random-dot stereogram whose square exists only in depth.
* **A small network**: one convolutional layer, global averaging and a linear readout, trained by gradient descent on
  shapes that each come with their own texture; tested on cue-conflict images it follows texture, as ImageNet-trained
  networks do (Geirhos et al. 2019); trained with textures shuffled across classes it learns more of the shape.

Nothing here imports manim.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats

Phi = stats.norm.cdf


# ============================================================================================ Bayes, Gaussians
def posterior(prior_mean: float, prior_sd: float, x, like_sd: float):
    """Posterior mean and sd for a Gaussian prior and one Gaussian measurement x (sd like_sd)."""
    wp, wl = 1 / prior_sd ** 2, 1 / like_sd ** 2
    mean = (wp * prior_mean + wl * np.asarray(x, float)) / (wp + wl)
    return mean, math.sqrt(1 / (wp + wl))


def combine(means, sds):
    """Optimal (maximum-likelihood) combination of independent Gaussian cues: weights proportional to 1/sd^2; the
    combined sd is 1/sqrt(sum 1/sd^2)."""
    m = np.asarray(means, float)
    w = 1 / np.asarray(sds, float) ** 2
    return float(np.sum(w * m) / w.sum()), float(1 / math.sqrt(w.sum())), w / w.sum()


# ======================================================================================== cue combination
def two_interval(sd: float, deltas, n: int, rng=None, standard: float = 55.0, weights=None, sds=None,
                 conflict: float = 0.0):
    """Two-interval height discrimination: the standard (``standard`` mm) and a comparison ``delta`` taller, each
    estimated with Gaussian noise ``sd``; the observer picks the one that seems taller.  Returns the share choosing the
    comparison at each delta.  With ``weights`` and ``sds`` (two cues), each estimate is the weighted average of a
    visual and a haptic estimate; ``conflict`` shifts the standard's visual height by +conflict/2 and its haptic
    height by -conflict/2 (the comparison has no conflict)."""
    rng = rng or np.random.default_rng(0)
    d = np.asarray(deltas, float)
    if weights is None:
        a = standard + rng.normal(0, sd, (n, len(d)))
        b = standard + d + rng.normal(0, sd, (n, len(d)))
    else:
        wv, wh = weights
        sv, sh = sds
        a = (wv * (standard + conflict / 2 + rng.normal(0, sv, (n, len(d))))
             + wh * (standard - conflict / 2 + rng.normal(0, sh, (n, len(d)))))
        b = (wv * (standard + d + rng.normal(0, sv, (n, len(d))))
             + wh * (standard + d + rng.normal(0, sh, (n, len(d)))))
    return (b > a).mean(axis=0)


def fit_cumulative(deltas, p, n: int) -> dict:
    """Maximum-likelihood cumulative Gaussian (no lapses) to choice proportions: the point of subjective equality and
    the spread; the single-cue sd is spread / sqrt 2 (two noisy intervals)."""
    d = np.asarray(deltas, float)
    k = np.round(np.asarray(p, float) * n)

    def nll(theta):
        mu, ls = theta
        q = np.clip(Phi((d - mu) / math.exp(ls)), 1e-9, 1 - 1e-9)
        return -float(np.sum(k * np.log(q) + (n - k) * np.log(1 - q)))

    r = optimize.minimize(nll, [0.0, math.log(max(np.std(d), 1e-3))], method="Nelder-Mead")
    mu, s = r.x[0], math.exp(r.x[1])
    return {"pse": float(mu), "spread": float(s), "sd": float(s / math.sqrt(2))}


# ========================================================================================= the motion prior
def speed_estimate(speed, contrast, prior_sd: float = 1.0, noise_at_full: float = 0.3):
    """Perceived speed under a zero-mean Gaussian prior on velocity: the likelihood sd is noise_at_full / contrast,
    so low-contrast motion is pulled further toward zero (Thompson's effect)."""
    like_sd = noise_at_full / np.asarray(contrast, float)
    shrink = prior_sd ** 2 / (prior_sd ** 2 + like_sd ** 2)
    return np.asarray(speed, float) * shrink


def edge_constraints(true_velocity, orientations_deg):
    """For edges at the given orientations, the unit normal (pointing along the motion's normal component) and the
    normal speed each edge reveals: the aperture problem's constraint lines."""
    v = np.asarray(true_velocity, float)
    out = []
    for th in orientations_deg:
        t = math.radians(th)
        n = np.array([-math.sin(t), math.cos(t)])
        s = float(n @ v)
        if s < 0:
            n, s = -n, -s
        out.append((n, s))
    return out


def map_velocity(constraints, like_sd: float, prior_sd: float = 1.0) -> np.ndarray:
    """MAP velocity from edge constraints (n . v = s, Gaussian noise like_sd) and a zero-mean Gaussian prior."""
    A = np.eye(2) / prior_sd ** 2
    b = np.zeros(2)
    for n, s in constraints:
        A += np.outer(n, n) / like_sd ** 2
        b += n * s / like_sd ** 2
    return np.linalg.solve(A, b)


def vector_average(constraints) -> np.ndarray:
    return np.mean([n * s for n, s in constraints], axis=0)


# ============================================================================================== lightness
def checker_shadow(n_checks: int = 6, cell: int = 24, light: float = 0.8, dark: float = 0.4, shadow: float = 0.5,
                   blur: float = 10.0):
    """A checkerboard (reflectances ``light`` and ``dark``) under uniform light with a soft-edged shadow over its
    right half-centre, chosen so a dark square outside (A) and a light square inside (B) send equal luminance
    (light * shadow = dark).  Returns luminance, reflectance, illumination and the centres (row, col) of A and B."""
    size = n_checks * cell
    yy, xx = np.mgrid[:size, :size]
    refl = np.where(((yy // cell) + (xx // cell)) % 2 == 0, light, dark).astype(float)
    # a shadow: an ellipse over the lower right, blurred
    cy, cx = size * 0.62, size * 0.66
    inside = ((yy - cy) / (size * 0.32)) ** 2 + ((xx - cx) / (size * 0.26)) ** 2 < 1.0
    sh = np.where(inside, shadow, 1.0)
    f = np.fft.fftfreq(size)
    k = np.exp(-2 * np.pi ** 2 * blur ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    illum = np.real(np.fft.ifft2(np.fft.fft2(sh) * k))
    # A: a dark square well outside the shadow; B: a light square at the shadow's centre
    def centre(r, c):
        return (int(r * cell + cell // 2), int(c * cell + cell // 2))
    a = next(centre(r, c) for r in range(1, n_checks) for c in range(0, 2) if (r + c) % 2 == 1)
    br, bc = int(cy // cell), int(cx // cell)
    if (br + bc) % 2 == 1:
        bc -= 1
    b = centre(br, bc)
    lum = refl * illum
    return {"luminance": lum, "reflectance": refl, "illumination": illum, "A": a, "B": b}


def retinex(luminance, threshold: float = 0.05) -> np.ndarray:
    """Horn's retinex: in log luminance, keep the gradients sharper than ``threshold`` (edges between surfaces), drop
    the gentle ones (changes of illumination), and reintegrate by solving Poisson's equation (periodic, by FFT).  The
    result is a reflectance estimate up to a constant, scaled so its maximum is 1."""
    L = np.log(np.asarray(luminance, float))
    gx = np.roll(L, -1, axis=1) - L
    gy = np.roll(L, -1, axis=0) - L
    gx = np.where(np.abs(gx) > threshold, gx, 0.0)
    gy = np.where(np.abs(gy) > threshold, gy, 0.0)
    div = gx - np.roll(gx, 1, axis=1) + gy - np.roll(gy, 1, axis=0)
    h, w = L.shape
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.fftfreq(w)[None, :]
    denom = (2 * np.cos(2 * np.pi * fx) - 2) + (2 * np.cos(2 * np.pi * fy) - 2)
    denom[0, 0] = 1.0
    R = np.fft.fft2(div) / denom
    R[0, 0] = 0.0
    r = np.real(np.fft.ifft2(R))
    r = np.exp(r - r.max())
    return r


# ================================================================================================== depth
def disparity_arcmin(distance_m: float, depth_m: float, ipd_m: float = 0.063) -> float:
    """Angular disparity between a point at ``distance_m`` and one ``depth_m`` further: ipd * depth / distance^2
    (small angles), in minutes of arc."""
    rad = ipd_m * depth_m / (distance_m * (distance_m + depth_m))
    return rad * 180 / math.pi * 60


def random_dot_stereogram(n: int = 160, square: int = 60, shift: int = 6, density: float = 0.5, seed: int = 0):
    """Julesz's stereogram: two random-dot images identical except that a central square is shifted sideways in one
    (the gap refilled with fresh dots).  Neither image alone shows a square."""
    rng = np.random.default_rng(seed)
    left = (rng.random((n, n)) < density).astype(float)
    right = left.copy()
    a, b = (n - square) // 2, (n + square) // 2
    right[a:b, a - shift:b - shift] = left[a:b, a:b]
    right[a:b, b - shift:b] = (rng.random((square, shift)) < density)
    return left, right


def perceived_size(angular_size_deg: float, perceived_distance: float) -> float:
    """Size-distance invariance: the size an object is seen to have is its angular size times its seen distance."""
    return 2 * perceived_distance * math.tan(math.radians(angular_size_deg) / 2)


# =========================================================================================== a small network
TEXTURES = ("stripes", "dots", "checks")
SHAPES = ("disc", "square", "triangle")


def _shape_mask(kind: str, n: int, rng) -> np.ndarray:
    yy, xx = np.mgrid[:n, :n] + 0.5
    s = rng.uniform(0.55, 0.8) * n / 2
    cy, cx = n / 2 + rng.uniform(-2, 2, 2)
    if kind == "disc":
        return ((yy - cy) ** 2 + (xx - cx) ** 2 < s * s).astype(float)
    if kind == "square":
        return ((np.abs(yy - cy) < s * 0.85) & (np.abs(xx - cx) < s * 0.85)).astype(float)
    # an upward triangle
    top, base = cy - s, cy + s * 0.8
    half = (yy - top) / (base - top) * s
    return ((yy > top) & (yy < base) & (np.abs(xx - cx) < half)).astype(float)


def _texture(kind: str, n: int, rng) -> np.ndarray:
    yy, xx = np.mgrid[:n, :n]
    ph = rng.integers(0, 4)
    if kind == "stripes":
        return (((xx + ph) // 2) % 2).astype(float)
    if kind == "dots":
        return ((((yy + ph) % 4) < 2) & (((xx + ph) % 4) < 2)).astype(float) * 0 + \
            (((yy + ph) % 4 == 1) & ((xx + ph) % 4 == 1)).astype(float)
    return ((((yy + ph) // 3) + ((xx + ph) // 3)) % 2).astype(float)


def shape_texture_images(m: int, n: int = 24, mode: str = "paired", seed: int = 0):
    """``m`` images of size n: a textured shape on a grey ground.  mode 'paired': each shape always carries its own
    texture (disc-stripes, square-dots, triangle-checks); 'shuffled': textures drawn at random; 'conflict': shape and
    texture deliberately mismatched.  Returns images, shape labels and texture labels."""
    rng = np.random.default_rng(seed)
    X = np.zeros((m, n, n))
    ys = rng.integers(0, 3, m)
    ts = ys.copy()
    if mode == "shuffled":
        ts = rng.integers(0, 3, m)
    elif mode == "conflict":
        ts = (ys + rng.integers(1, 3, m)) % 3
    for i in range(m):
        mask = _shape_mask(SHAPES[ys[i]], n, rng)
        tex = _texture(TEXTURES[ts[i]], n, rng)
        X[i] = 0.5 + mask * (0.45 * (2 * tex - 1) * 0.6 + 0.15) + rng.normal(0, 0.03, (n, n))
    return X, ys, ts


def _patches(X: np.ndarray, k: int) -> np.ndarray:
    m, n, _ = X.shape
    o = n - k + 1
    idx = np.lib.stride_tricks.sliding_window_view(X, (k, k), axis=(1, 2))  # m, o, o, k, k
    return idx.reshape(m, o * o, k * k)


class TinyConvNet:
    """One convolutional layer (``filters`` filters of size k), ReLU, global average pooling, and a linear readout to
    three classes, trained by full-batch gradient descent with softmax cross-entropy."""

    def __init__(self, filters: int = 8, k: int = 5, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.k = k
        self.W = rng.normal(0, 0.3, (k * k, filters))
        self.b = np.zeros(filters)
        self.V = rng.normal(0, 0.3, (filters, 3))
        self.c = np.zeros(3)

    def _forward(self, P):
        Z = P @ self.W + self.b  # m, positions, filters
        H = np.maximum(Z, 0)
        g = H.mean(axis=1)  # m, filters
        logits = g @ self.V + self.c
        return Z, H, g, logits

    def predict(self, X) -> np.ndarray:
        return self._forward(_patches(X, self.k))[3].argmax(axis=1)

    def fit(self, X, y, steps: int = 300, lr: float = 0.5, momentum: float = 0.9) -> list:
        P = _patches(X, self.k)
        m = len(y)
        Y = np.eye(3)[y]
        losses = []
        vel = [np.zeros_like(a) for a in (self.V, self.c, self.W, self.b)]
        for _ in range(steps):
            Z, H, g, logits = self._forward(P)
            logits = logits - logits.max(axis=1, keepdims=True)
            prob = np.exp(logits)
            prob /= prob.sum(axis=1, keepdims=True)
            losses.append(float(-np.mean(np.log(prob[np.arange(m), y] + 1e-12))))
            dlog = (prob - Y) / m
            dV, dc = g.T @ dlog, dlog.sum(axis=0)
            dg = dlog @ self.V.T  # m, filters
            dH = np.repeat(dg[:, None, :], H.shape[1], axis=1) / H.shape[1]
            dZ = dH * (Z > 0)
            dW = np.einsum("mpk,mpf->kf", P, dZ)
            db = dZ.sum(axis=(0, 1))
            for i, (param, grad) in enumerate(((self.V, dV), (self.c, dc), (self.W, dW), (self.b, db))):
                vel[i] = momentum * vel[i] - lr * grad
                param += vel[i]
        return losses


def texture_bias(net: TinyConvNet, m: int = 300, seed: int = 99) -> dict:
    """On cue-conflict images, the share of decisions that follow the texture (among those that follow either the
    shape or the texture)."""
    X, ys, ts = shape_texture_images(m, mode="conflict", seed=seed)
    pred = net.predict(X)
    shape_hits = int((pred == ys).sum())
    tex_hits = int((pred == ts).sum())
    return {"shape": shape_hits, "texture": tex_hits, "texture_share": tex_hits / max(shape_hits + tex_hits, 1)}
