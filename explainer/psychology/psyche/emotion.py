"""Psyche's emotion (Part 29): maps of affect, arousal attributed to a cause, appraisal, a fear circuit with two
roads, adaptation and forecasting, a world in which money and happiness relate in two ways at once, and Lorenz's
equations as the positivity ratio used them.

* :func:`classical_mds`: Torgerson's classical multidimensional scaling of a dissimilarity matrix; :func:`fit_scale`
  finds the direction in a configuration that best predicts an external rating (its multiple correlation), and
  :func:`procrustes` aligns one configuration to another by rotation, reflection and scale.
* :func:`pairs_map`: a simulated observer judges every pair of faces 'same feeling' or 'different', from their
  distance on a valence-arousal plane plus noise; the share of 'different' judgments is a dissimilarity, and MDS of
  it recovers the plane (the face-sorting interactive's analysis).
* :func:`attribution`: two factors as inference.  Arousal is observed; its cause is unknown (a drug, the situation,
  another person).  With an explanation already given (the informed condition), arousal is explained away and less
  of it is attributed to the situation.
* :func:`appraise`: an appraisal model.  A scenario is coded on six appraisal dimensions (pleasantness, certainty,
  agency of self, agency of others, control, novelty); each emotion is a prototype on those dimensions (directions
  after Smith and Ellsworth 1985, values illustrative); the label probabilities are a softmax of negative distance.
* :func:`two_roads`: LeDoux's two routes to the amygdala as leaky integrators: a fast thalamic route that responds to
  coarse shape, and a slower cortical route that identifies the object and excites or inhibits.  A stick and a
  snake both start a response; only the snake sustains it.  Without an amygdala nothing is triggered.
* :func:`adaptation` and :func:`forecast`: hedonic adaptation as exponential return to baseline; a forecaster who
  expects the impact to fade slowly overestimates the feeling a month on (the impact bias).
* :func:`income_world`: a simulated population where happiness rises with log income for most people, while a
  minority's unhappiness comes from sources money does not touch.  The mean rises steadily; the share who felt
  bad yesterday, and the 20th percentile, flatten: both published patterns from one world.
* :func:`lorenz`: the Lorenz system, integrated by fourth-order Runge-Kutta.

Nothing here imports manim.
"""

from __future__ import annotations

import numpy as np

__all__ = ["classical_mds", "fit_scale", "procrustes", "pairs_map", "FACES", "attribution", "APPRAISAL_DIMS",
           "PROTOTYPES", "appraise", "two_roads", "adaptation", "forecast", "income_world", "lorenz"]


# --------------------------------------------------------------------------------------------- maps
def classical_mds(D, k: int = 2) -> dict:
    """Torgerson scaling: double-centre the squared dissimilarities, take the top k eigenvectors.  Returns the
    configuration X (n x k), all eigenvalues (descending) and the share of positive variance in the first k."""
    D = np.asarray(D, float)
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    order = np.argsort(w)[::-1]
    w, V = w[order], V[:, order]
    X = V[:, :k] * np.sqrt(np.maximum(w[:k], 0))
    pos = w[w > 0].sum()
    return {"X": X, "eig": w, "share": float(w[:k].sum() / pos) if pos > 0 else 0.0}


def fit_scale(X, y) -> dict:
    """Regress a rating y on the configuration's coordinates: the unit direction of steepest increase, the
    multiple correlation R, and the fitted values."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    fit = A @ beta
    R = float(np.corrcoef(fit, y)[0, 1])
    d = beta[1:] / np.linalg.norm(beta[1:])
    return {"direction": d, "R": R, "fit": fit, "beta": beta}


def procrustes(X, Y) -> dict:
    """The rotation (or reflection) and scale that best map X onto Y (both centred).  Returns the mapped X and
    the correlation between the two sets of coordinates."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    Xc, Yc = X - X.mean(0), Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    scale = s.sum() / (Xc ** 2).sum()
    Z = scale * Xc @ R + Y.mean(0)
    r = float(np.corrcoef(Z.ravel(), Y.ravel())[0, 1])
    return {"Z": Z, "r": r, "R": R, "scale": float(scale)}


# Ten schematic faces on a valence-arousal plane (the interactive draws them from these two numbers)
FACES = {
    "excited": (0.7, 0.75), "happy": (0.9, 0.3), "content": (0.75, -0.45), "calm": (0.2, -0.8),
    "tired": (-0.35, -0.8), "sad": (-0.8, -0.4), "afraid": (-0.6, 0.85), "angry": (-0.85, 0.5),
    "surprised": (0.05, 0.95), "neutral": (0.0, 0.0),
}


def pairs_map(n_reps: int = 1, noise: float = 0.35, scale: float = 0.9, seed: int = 0) -> dict:
    """Every pair of the ten faces judged 'different' with probability logistic((distance - scale) / noise),
    ``n_reps`` times; MDS of the share of 'different' judgments, aligned to the true plane by Procrustes."""
    rng = np.random.default_rng(seed)
    names = list(FACES)
    P = np.array([FACES[k] for k in names], float)
    n = len(names)
    dist = np.linalg.norm(P[:, None] - P[None], axis=2)
    p_diff = 1 / (1 + np.exp(-(dist - scale) / noise))
    Dm = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            Dm[i, j] = Dm[j, i] = (rng.random(n_reps) < p_diff[i, j]).mean()
    m = classical_mds(Dm)
    pr = procrustes(m["X"], P)
    return {"names": names, "true": P, "D": Dm, "X": pr["Z"], "r": pr["r"], "share": m["share"]}


# --------------------------------------------------------------------------------------------- two factors
def attribution(arousal: float = 1.0, explanation: float = 0.0, prior_situation: float = 0.3,
                spread: float = 0.5) -> dict:
    """Arousal a is observed.  Its sources: the situation s (prior ``prior_situation``) and a known cause c of size
    ``explanation`` (an injection the person was told about).  a ~ N(s + c, spread^2), s >= 0 on a grid with an
    exponential prior.  Returns the posterior mean of s (arousal attributed to the situation, felt as emotion)."""
    s = np.linspace(0, 3, 601)
    prior = np.exp(-s / prior_situation)
    lik = np.exp(-0.5 * ((arousal - s - explanation) / spread) ** 2)
    post = prior * lik
    post /= post.sum()
    return {"mean": float((s * post).sum()), "grid": s, "posterior": post}


# --------------------------------------------------------------------------------------------- appraisal
APPRAISAL_DIMS = ("pleasant", "certain", "self caused", "others caused", "in control", "sudden")

# directions after Smith and Ellsworth (1985) and Scherer (2001); the values are illustrative, on -1 to 1
PROTOTYPES = {
    "joy": (0.9, 0.6, 0.0, 0.0, 0.4, 0.0),
    "pride": (0.8, 0.6, 0.9, -0.3, 0.6, 0.0),
    "hope": (0.5, -0.6, 0.0, 0.0, 0.0, 0.0),
    "relief": (0.6, 0.6, 0.0, 0.0, 0.0, 0.3),
    "anger": (-0.8, 0.6, -0.4, 0.9, 0.4, 0.3),
    "guilt": (-0.7, 0.5, 0.9, -0.4, 0.2, 0.0),
    "sadness": (-0.8, 0.6, -0.2, -0.2, -0.8, 0.0),
    "fear": (-0.8, -0.8, -0.2, 0.2, -0.6, 0.6),
    "surprise": (0.0, -0.6, 0.0, 0.0, -0.2, 1.0),
}


def appraise(code, beta: float = 3.0) -> dict:
    """Label probabilities for a scenario coded on :data:`APPRAISAL_DIMS`: softmax of -beta x distance to each
    prototype."""
    x = np.asarray(code, float)
    names = list(PROTOTYPES)
    P = np.array([PROTOTYPES[k] for k in names], float)
    d = np.linalg.norm(P - x, axis=1)
    z = np.exp(-beta * (d - d.min()))
    p = z / z.sum()
    order = np.argsort(p)[::-1]
    return {"labels": [names[i] for i in order], "p": p[order], "distance": d[order]}


# --------------------------------------------------------------------------------------------- fear
def two_roads(obj: str = "snake", amygdala: bool = True, T: float = 0.6, dt: float = 0.001,
              thalamic_delay: float = 0.015, cortical_delay: float = 0.06, tau: float = 0.02) -> dict:
    """Amygdala activity after a long curved object appears at t = 0.  The thalamic route (after
    ``thalamic_delay``) drives with the coarse shape, the same for stick and snake; the cortical route (after
    ``cortical_delay``) identifies it, adding drive for a snake and inhibition for a stick.  Leaky integration with
    time constant ``tau``; the defensive response (freezing, a startle, a racing heart) follows the activity.
    The timings are illustrative."""
    n = int(T / dt)
    t = np.arange(n) * dt
    coarse = (t >= thalamic_delay) * 0.6
    ident = (t >= cortical_delay) * (0.8 if obj == "snake" else -0.9)
    drive = np.maximum(coarse + ident, 0.0) if amygdala else np.zeros(n)
    a = np.zeros(n)
    for i in range(1, n):
        a[i] = a[i - 1] + dt / tau * (-a[i - 1] + drive[i])
    return {"t": t, "a": a, "peak_early": float(a[t < cortical_delay].max()), "late": float(a[-1])}


# --------------------------------------------------------------------------------------------- forecasting
def adaptation(t, impact: float, tau: float, baseline: float = 0.0):
    """Feeling over time after an event: baseline + impact exp(-t / tau)."""
    return baseline + impact * np.exp(-np.asarray(t, float) / tau)


def forecast(impact: float = 3.0, tau_actual: float = 20.0, tau_predicted: float = 150.0, at: float = 60.0,
             days: int = 365) -> dict:
    """A forecaster who expects the event's impact to fade with time constant ``tau_predicted`` days, while it
    actually fades with ``tau_actual``.  Returns both curves and the gap at ``at`` days."""
    t = np.arange(days + 1, dtype=float)
    act, pred = adaptation(t, impact, tau_actual), adaptation(t, impact, tau_predicted)
    k = int(at)
    return {"t": t, "actual": act, "predicted": pred, "at": float(at), "actual_at": float(act[k]),
            "predicted_at": float(pred[k])}


# --------------------------------------------------------------------------------------------- money
def income_world(n: int = 200_000, seed: int = 0, slope: float = 0.35, share_unhappy: float = 0.2,
                 sd: float = 0.6) -> dict:
    """Log income ~ N(log 60k, 0.7).  For most people momentary happiness = slope x log2(income / 60k) + noise; a
    minority (``share_unhappy``) carry an extra, money-resistant burden: their happiness rises with income only up
    to about 100,000 a year.  Returns income bins with the mean happiness, the 20th percentile, and the share who
    'felt bad yesterday' (happiness below -1)."""
    rng = np.random.default_rng(seed)
    inc = np.exp(np.log(60_000) + 0.7 * rng.standard_normal(n))
    x = np.log2(inc / 60_000)
    h = slope * x + sd * rng.standard_normal(n)
    unhappy = rng.random(n) < share_unhappy
    x100 = np.log2(100_000 / 60_000)  # above about 100,000 money no longer helps this group
    h = np.where(unhappy, slope * np.minimum(x, x100) - 1.8 + sd * rng.standard_normal(n), h)
    edges = np.array([15, 25, 35, 50, 70, 100, 140, 200, 300, 500]) * 1000.0
    mid, mean, p20, p10, bad = [], [], [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (inc >= lo) & (inc < hi)
        mid.append(np.sqrt(lo * hi))
        mean.append(h[m].mean())
        p20.append(np.percentile(h[m], 20))
        p10.append(np.percentile(h[m], 10))
        bad.append((h[m] < -1.0).mean())
    return {"income": np.array(mid), "mean": np.array(mean), "p20": np.array(p20), "p10": np.array(p10),
            "bad": np.array(bad)}


# --------------------------------------------------------------------------------------------- Lorenz
def lorenz(T: float = 40.0, dt: float = 0.01, sigma: float = 10.0, rho: float = 28.0, beta: float = 8 / 3,
           x0=(1.0, 1.0, 1.0)) -> np.ndarray:
    """The Lorenz system dx = sigma (y - x), dy = x (rho - z) - y, dz = x y - beta z, by RK4."""
    def f(v):
        x, y, z = v
        return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])
    n = int(T / dt)
    out = np.empty((n, 3))
    v = np.array(x0, float)
    for i in range(n):
        k1 = f(v)
        k2 = f(v + dt / 2 * k1)
        k3 = f(v + dt / 2 * k2)
        k4 = f(v + dt * k3)
        v = v + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[i] = v
    return out
