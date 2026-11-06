"""statkit.ppl: a tiny probabilistic programming language and the samplers behind it (Part 27 of *Statistics, Built*).

    from explainer.stats.kit import ppl as P
    m = P.Model({"mu": (1, "real"), "tau": (1, "positive"), "z": (8, "real")}, logp)   # logp(params) -> Tensor
    fit = P.sample(m, chains=4, iters=1000, warmup=1000, seed=1)                      # NUTS, adapted
    P.rhat(fit.draws["tau"][..., 0]), P.ess_bulk(fit.draws["tau"][..., 0])

A model is a log density written with *AI, Built*'s reverse-mode autodiff (``explainer.ai.autodiff.Tensor``):
parameters are declared with a size and a support ("real", "positive", "unit"), and the model maps them, through
the transform's Jacobian, to an unconstrained space where Hamiltonian Monte Carlo runs.  The samplers:

- ``leapfrog``, ``hmc`` (static path length), and ``nuts`` (Hoffman & Gelman 2014: the slice-sampling version with
  dual-averaging step-size adaptation and a windowed diagonal mass matrix, as in Stan), with divergences recorded;
- ``rwm``, a random-walk Metropolis sampler;
- ``advi``, mean-field Gaussian variational inference by stochastic gradient (Kucukelbir et al. 2017).

Diagnostics: rank-normalized split R-hat and bulk/tail ESS (Vehtari et al. 2021), and PSIS with its Pareto k-hat
(Vehtari et al. 2024).  Checked against closed-form posteriors in ``tests/test_stats_kit_ppl.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import special, stats

from explainer.ai.autodiff import Tensor, sigmoid

LOG2PI = float(np.log(2 * np.pi))


# ---------------------------------------------------------------------------------------------------------------
# Log densities on Tensors (constants kept, so that evidences and checks are exact)
# ---------------------------------------------------------------------------------------------------------------
def _t(x) -> Tensor:
    return x if isinstance(x, Tensor) else Tensor(np.asarray(x, float))


def softplus(x: Tensor) -> Tensor:
    """log(1 + e^x), stably, with derivative sigmoid(x)."""
    x = _t(x)
    return x._make(np.logaddexp(0.0, x.data), [(x, lambda g: g * special.expit(x.data))], "softplus")


def normal_lpdf(x, mu, sigma) -> Tensor:
    x, mu, sigma = _t(x), _t(mu), _t(sigma)
    z = (x - mu) / sigma
    return (z * z * -0.5 - sigma.log() - 0.5 * LOG2PI).sum()


def halfnormal_lpdf(x, s: float) -> Tensor:
    x = _t(x)
    return ((x / s) * (x / s) * -0.5 + float(np.log(2 / s) - 0.5 * LOG2PI)).sum()


def halfcauchy_lpdf(x, s: float) -> Tensor:
    x = _t(x)
    return ((x / s) * (x / s) + 1.0).log().__neg__().sum() + float(np.size(x.data) * np.log(2 / (np.pi * s)))


def exponential_lpdf(x, rate: float) -> Tensor:
    x = _t(x)
    return (x * -rate).sum() + float(np.size(x.data) * np.log(rate))


def bernoulli_logit_lpmf(y, eta) -> Tensor:
    eta = _t(eta)
    return (eta * np.asarray(y, float) - softplus(eta)).sum()


def poisson_log_lpmf(y, eta) -> Tensor:
    eta = _t(eta)
    y = np.asarray(y, float)
    return (eta * y - eta.exp()).sum() - float(np.sum(special.gammaln(y + 1)))


def binomial_logit_lpmf(k, n, eta) -> Tensor:
    eta = _t(eta)
    k, n = np.asarray(k, float), np.asarray(n, float)
    const = float(np.sum(special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)))
    return (eta * k - softplus(eta) * n).sum() + const


# ---------------------------------------------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------------------------------------------
class Model:
    """``params``: name -> (size, support) with support "real", "positive" (exp) or "unit" (logistic);
    ``logp(p)``: the log joint density of the constrained parameters (a dict of Tensors), as a Tensor."""

    def __init__(self, params: dict, logp):
        self.params = dict(params)
        self.logp = logp
        self.slices = {}
        k = 0
        for name, (size, support) in self.params.items():
            assert support in ("real", "positive", "unit"), support
            self.slices[name] = slice(k, k + size)
            k += size
        self.dim = k
        self.n_grad = 0

    def _unpack(self, base: Tensor):
        p, logj = {}, None
        for name, (size, support) in self.params.items():
            u = base[self.slices[name]]
            if support == "real":
                v, lj = u, None
            elif support == "positive":
                v, lj = u.exp(), u.sum()
            else:
                v = sigmoid(u)
                lj = (v.log() + (1.0 - v).log()).sum()
            p[name] = v
            if lj is not None:
                logj = lj if logj is None else logj + lj
        return p, logj

    def log_density(self, u) -> float:
        """The log density on the unconstrained scale (Jacobian included), without a gradient."""
        p, logj = self._unpack(Tensor(np.asarray(u, float)))
        lp = self.logp(p)
        return float(lp.data + (logj.data if logj is not None else 0.0))

    def logp_grad(self, u):
        self.n_grad += 1
        base = Tensor(np.asarray(u, float).copy(), requires_grad=True)
        p, logj = self._unpack(base)
        lp = self.logp(p)
        if logj is not None:
            lp = lp + logj
        lp.backward()
        return float(lp.data), base.grad.copy()

    def constrain(self, U) -> dict:
        """Constrained values for an array of unconstrained draws (..., dim)."""
        U = np.asarray(U, float)
        out = {}
        for name, (size, support) in self.params.items():
            u = U[..., self.slices[name]]
            out[name] = u if support == "real" else (np.exp(u) if support == "positive" else special.expit(u))
        return out


# ---------------------------------------------------------------------------------------------------------------
# Hamiltonian dynamics
# ---------------------------------------------------------------------------------------------------------------
def leapfrog(model: Model, q, p, g, eps: float, inv_m):
    """One leapfrog step with a diagonal inverse mass matrix; returns q, p, lp, grad at the new point."""
    p = p + 0.5 * eps * g
    q = q + eps * inv_m * p
    lp, g = model.logp_grad(q)
    p = p + 0.5 * eps * g
    return q, p, lp, g


def hmc(model: Model, q0, eps: float, L: int, n: int, rng: np.random.Generator, inv_m=None, record: bool = False):
    """Static HMC: L leapfrog steps of size eps per iteration; returns draws, acceptance and (optionally) paths."""
    inv_m = np.ones(model.dim) if inv_m is None else np.asarray(inv_m, float)
    q = np.asarray(q0, float)
    lp, g = model.logp_grad(q)
    draws, acc, paths = np.empty((n, model.dim)), np.zeros(n), []
    for i in range(n):
        p0 = rng.standard_normal(model.dim) / np.sqrt(inv_m)
        h0 = lp - 0.5 * np.sum(inv_m * p0 * p0)
        qn, pn, lpn, gn = q, p0, lp, g
        path = [q.copy()]
        for _ in range(L):
            qn, pn, lpn, gn = leapfrog(model, qn, pn, gn, eps, inv_m)
            path.append(qn.copy())
        h1 = lpn - 0.5 * np.sum(inv_m * pn * pn)
        if np.log(rng.random()) < h1 - h0:
            q, lp, g = qn, lpn, gn
            acc[i] = 1
        draws[i] = q
        if record:
            paths.append(np.array(path))
    return {"draws": draws, "accept": acc, "paths": paths}


def rwm(log_density, q0, scale, n: int, rng: np.random.Generator):
    """Random-walk Metropolis with N(0, diag(scale^2)) proposals; returns draws and acceptance indicators."""
    q = np.asarray(q0, float)
    scale = np.broadcast_to(np.asarray(scale, float), q.shape)
    lp = log_density(q)
    draws, acc = np.empty((n, q.size)), np.zeros(n)
    for i in range(n):
        prop = q + scale * rng.standard_normal(q.size)
        lq = log_density(prop)
        if np.log(rng.random()) < lq - lp:
            q, lp = prop, lq
            acc[i] = 1
        draws[i] = q
    return {"draws": draws, "accept": acc}


# ---------------------------------------------------------------------------------------------------------------
# NUTS (Hoffman & Gelman 2014, Algorithm 6) with Stan-style warmup
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class _Tree:
    q_minus: np.ndarray
    p_minus: np.ndarray
    g_minus: np.ndarray
    q_plus: np.ndarray
    p_plus: np.ndarray
    g_plus: np.ndarray
    q_prop: np.ndarray
    lp_prop: float
    g_prop: np.ndarray
    n: int
    s: bool
    alpha: float
    n_alpha: int
    divergent: bool
    path: list = field(default_factory=list)


def _no_u_turn(qm, qp, pm, pp, inv_m) -> bool:
    dq = qp - qm
    return bool(np.dot(dq, inv_m * pm) >= 0 and np.dot(dq, inv_m * pp) >= 0)


def _build(model, q, p, g, log_u, v, j, eps, h0, inv_m, rng, record, max_dh=1000.0) -> _Tree:
    if j == 0:
        q1, p1, lp1, g1 = leapfrog(model, q, p, g, v * eps, inv_m)
        h1 = lp1 - 0.5 * np.sum(inv_m * p1 * p1)
        if not np.isfinite(h1):
            h1 = -np.inf
        n1 = int(log_u <= h1)
        s1 = bool(log_u < max_dh + h1)
        a = float(min(1.0, np.exp(min(h1 - h0, 0.0)))) if np.isfinite(h1) else 0.0
        return _Tree(q1, p1, g1, q1, p1, g1, q1, lp1, g1, n1, s1, a, 1, not s1, [q1.copy()] if record else [])
    t = _build(model, q, p, g, log_u, v, j - 1, eps, h0, inv_m, rng, record, max_dh)
    if t.s:
        if v == -1:
            t2 = _build(model, t.q_minus, t.p_minus, t.g_minus, log_u, v, j - 1, eps, h0, inv_m, rng, record, max_dh)
            t.q_minus, t.p_minus, t.g_minus = t2.q_minus, t2.p_minus, t2.g_minus
        else:
            t2 = _build(model, t.q_plus, t.p_plus, t.g_plus, log_u, v, j - 1, eps, h0, inv_m, rng, record, max_dh)
            t.q_plus, t.p_plus, t.g_plus = t2.q_plus, t2.p_plus, t2.g_plus
        if t.n + t2.n > 0 and rng.random() < t2.n / (t.n + t2.n):
            t.q_prop, t.lp_prop, t.g_prop = t2.q_prop, t2.lp_prop, t2.g_prop
        t.alpha += t2.alpha
        t.n_alpha += t2.n_alpha
        t.divergent = t.divergent or t2.divergent
        t.s = t2.s and _no_u_turn(t.q_minus, t.q_plus, t.p_minus, t.p_plus, inv_m)
        t.n += t2.n
        if record:
            t.path = t.path + t2.path if v == 1 else t2.path[::-1] + t.path
    return t


def nuts_step(model, q, lp, g, eps, inv_m, rng, max_depth=10, record=False):
    p0 = rng.standard_normal(model.dim) / np.sqrt(inv_m)
    h0 = lp - 0.5 * np.sum(inv_m * p0 * p0)
    log_u = h0 + np.log(rng.random())
    qm = qp = q
    pm = pp = p0
    gm = gp = g
    q_new, lp_new, g_new = q, lp, g
    n, s, depth = 1, True, 0
    alpha, n_alpha, divergent = 0.0, 0, False
    path = [q.copy()] if record else []
    while s and depth < max_depth:
        v = 1 if rng.random() < 0.5 else -1
        if v == -1:
            t = _build(model, qm, pm, gm, log_u, v, depth, eps, h0, inv_m, rng, record)
            qm, pm, gm = t.q_minus, t.p_minus, t.g_minus
        else:
            t = _build(model, qp, pp, gp, log_u, v, depth, eps, h0, inv_m, rng, record)
            qp, pp, gp = t.q_plus, t.p_plus, t.g_plus
        if record:
            path = path + t.path if v == 1 else t.path[::-1] + path
        if t.s and rng.random() < min(1.0, t.n / n):
            q_new, lp_new, g_new = t.q_prop, t.lp_prop, t.g_prop
        n += t.n
        alpha += t.alpha
        n_alpha += t.n_alpha
        divergent = divergent or t.divergent
        s = t.s and _no_u_turn(qm, qp, pm, pp, inv_m)
        depth += 1
    return q_new, lp_new, g_new, {"accept": alpha / max(n_alpha, 1), "depth": depth, "n_leapfrog": n_alpha,
                                  "divergent": divergent, "path": path}


def _find_eps(model, q, lp, g, inv_m, rng):
    eps = 1.0
    p = rng.standard_normal(model.dim) / np.sqrt(inv_m)
    h0 = lp - 0.5 * np.sum(inv_m * p * p)
    _, p1, lp1, _ = leapfrog(model, q, p, g, eps, inv_m)
    h1 = lp1 - 0.5 * np.sum(inv_m * p1 * p1)
    a = 1 if (np.isfinite(h1) and h1 - h0 > np.log(0.5)) else -1
    for _ in range(50):
        _, p1, lp1, _ = leapfrog(model, q, p, g, eps, inv_m)
        h1 = lp1 - 0.5 * np.sum(inv_m * p1 * p1)
        if not np.isfinite(h1):
            h1 = -np.inf
        if a * (h1 - h0) <= -a * np.log(2):
            break
        eps *= 2.0 ** a
    return eps


@dataclass
class Fit:
    draws: dict  # name -> (chains, iters, size) constrained
    unconstrained: np.ndarray  # (chains, iters, dim)
    divergent: np.ndarray  # (chains, iters)
    depth: np.ndarray
    n_leapfrog: np.ndarray
    accept: np.ndarray
    step_size: np.ndarray  # per chain
    inv_metric: np.ndarray  # (chains, dim)
    n_grad: int
    warmup_divergent: np.ndarray = None


def nuts(model: Model, iters: int, warmup: int, rng: np.random.Generator, init=None, delta: float = 0.8,
         max_depth: int = 10, adapt_metric: bool = True):
    """One chain of NUTS with Stan's warmup: step-size dual averaging throughout, and a diagonal inverse metric
    estimated in doubling windows (75 initial, 25 doubling, 50 final iterations, scaled to the warmup length)."""
    q = rng.uniform(-2, 2, model.dim) if init is None else np.asarray(init, float)
    lp, g = model.logp_grad(q)
    inv_m = np.ones(model.dim)
    eps = _find_eps(model, q, lp, g, inv_m, rng)
    mu, hbar, log_eps_bar, gamma, t0, kappa = np.log(10 * eps), 0.0, 0.0, 0.05, 10.0, 0.75
    # windows
    if warmup >= 150 and adapt_metric:
        init_w, term_w = int(0.15 * warmup), int(0.1 * warmup)
        ends, w, start = [], max(25, int(0.05 * warmup)), init_w
        while start + w < warmup - term_w:
            nxt = start + w
            if nxt + 2 * w > warmup - term_w:
                nxt = warmup - term_w
            ends.append((start, nxt))
            start, w = nxt, 2 * w
    else:
        ends = []
    window_draws = []
    U = np.empty((iters, model.dim))
    info = {k: np.zeros(iters) for k in ("divergent", "depth", "n_leapfrog", "accept")}
    wdiv = np.zeros(max(warmup, 1))
    m_step = 0
    for it in range(warmup + iters):
        q, lp, g, st = nuts_step(model, q, lp, g, eps, inv_m, rng, max_depth)
        if it < warmup:
            wdiv[it] = st["divergent"]
            m_step += 1
            hbar = (1 - 1 / (m_step + t0)) * hbar + (delta - st["accept"]) / (m_step + t0)
            log_eps = mu - np.sqrt(m_step) / gamma * hbar
            eta = m_step ** (-kappa)
            log_eps_bar = eta * log_eps + (1 - eta) * log_eps_bar
            eps = float(np.exp(log_eps))
            for a, b in ends:
                if a <= it < b:
                    window_draws.append(q.copy())
                if it == b - 1 and window_draws:
                    W = np.array(window_draws)
                    n_w = len(W)
                    var = W.var(axis=0, ddof=1) if n_w > 1 else np.ones(model.dim)
                    inv_m = (n_w / (n_w + 5.0)) * var + 1e-3 * (5.0 / (n_w + 5.0))
                    window_draws = []
                    eps = _find_eps(model, q, lp, g, inv_m, rng)
                    mu, hbar, log_eps_bar, m_step = np.log(10 * eps), 0.0, 0.0, 0
            if it == warmup - 1:
                eps = float(np.exp(log_eps_bar))
        else:
            k = it - warmup
            U[k] = q
            for key in info:
                info[key][k] = st[key]
    return U, info, eps, inv_m, wdiv


def sample(model: Model, chains: int = 4, iters: int = 1000, warmup: int = 1000, seed: int = 0, inits=None, **kw) -> Fit:
    model.n_grad = 0
    ss = np.random.SeedSequence(seed)
    outs = []
    for c, child in enumerate(ss.spawn(chains)):
        rng = np.random.Generator(np.random.PCG64(child))
        outs.append(nuts(model, iters, warmup, rng, None if inits is None else inits[c], **kw))
    U = np.stack([o[0] for o in outs])
    draws = model.constrain(U)
    return Fit(draws, U, np.stack([o[1]["divergent"] for o in outs]).astype(bool), np.stack([o[1]["depth"] for o in outs]),
               np.stack([o[1]["n_leapfrog"] for o in outs]), np.stack([o[1]["accept"] for o in outs]),
               np.array([o[2] for o in outs]), np.stack([o[3] for o in outs]), model.n_grad,
               np.stack([o[4] for o in outs]).astype(bool))


# ---------------------------------------------------------------------------------------------------------------
# Diagnostics (Vehtari, Gelman, Simpson, Carpenter & Bürkner 2021)
# ---------------------------------------------------------------------------------------------------------------
def _split(x):
    x = np.atleast_2d(np.asarray(x, float))
    n = x.shape[1] // 2
    return np.concatenate([x[:, :n], x[:, -n:]], axis=0)


def _rhat_basic(x):
    m, n = x.shape
    B = n * x.mean(axis=1).var(ddof=1)
    W = x.var(axis=1, ddof=1).mean()
    var_plus = (n - 1) / n * W + B / n
    return float(np.sqrt(var_plus / W))


def _z_scale(x):
    r = stats.rankdata(x, method="average").reshape(x.shape)
    return stats.norm.ppf((r - 3 / 8) / (x.size + 1 / 4))


def rhat(x) -> float:
    """Rank-normalized split R-hat: the larger of the bulk and folded (tail) versions."""
    s = _split(x)
    bulk = _rhat_basic(_z_scale(s))
    tail = _rhat_basic(_z_scale(np.abs(s - np.median(s))))
    return max(bulk, tail)


def _ess_multi(x):
    m, n = x.shape
    xc = x - x.mean(axis=1, keepdims=True)
    f = np.fft.rfft(xc, 2 * n, axis=1)
    acov = np.fft.irfft(f * np.conj(f), axis=1)[:, :n] / n
    chain_var = acov[:, 0] * n / (n - 1)
    W = chain_var.mean()
    var_plus = W * (n - 1) / n + (x.mean(axis=1).var(ddof=1) if m > 1 else 0.0)
    rho = 1 - (W - acov.mean(axis=0)) / var_plus
    rho[0] = 1.0
    # Geyer's initial positive monotone sequence
    t, s, prev = 0, 0.0, np.inf
    while t + 1 < n:
        pair = rho[t] + rho[t + 1]
        if pair < 0:
            break
        pair = min(pair, prev)
        s += pair
        prev = pair
        t += 2
    tau = -1 + 2 * s
    return float(m * n / max(tau, 1.0 / np.log10(m * n)))


def ess_bulk(x) -> float:
    return _ess_multi(_z_scale(_split(x)))


def ess_tail(x) -> float:
    s = _split(x)
    q05, q95 = np.quantile(s, [0.05, 0.95])
    return min(_ess_multi((s <= q05).astype(float)), _ess_multi((s >= q95).astype(float)))


def ess_basic(x) -> float:
    return _ess_multi(_split(x))


# ---------------------------------------------------------------------------------------------------------------
# Importance sampling and PSIS
# ---------------------------------------------------------------------------------------------------------------
def _gpd_fit(x):
    """Zhang & Stephens (2009) estimate of the generalized Pareto (k, sigma) for exceedances x > 0, with the
    weakly informative prior adjustment of Vehtari et al."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    prior_bs, prior_k = 3, 10
    m = 30 + int(np.sqrt(n))
    bs = 1 - np.sqrt(m / (np.arange(1, m + 1) - 0.5))
    bs = bs / (prior_bs * x[int(n / 4 + 0.5) - 1]) + 1 / x[-1]
    ks = np.array([np.mean(np.log1p(-b * x)) for b in bs])
    L = n * (np.log(-bs / ks) - ks - 1)
    with np.errstate(over="ignore"):
        w = 1 / np.array([np.sum(np.exp(L - li)) for li in L])
    b = np.sum(bs * w)
    k = np.mean(np.log1p(-b * x))
    sigma = -k / b
    k = (n * k + prior_k * 0.5) / (n + prior_k)
    return k, sigma  # the generalized Pareto shape and scale


def psis(log_w):
    """Pareto-smoothed importance weights (normalized) and the shape estimate k-hat: k-hat > 0.7 means the
    importance-sampling estimate is unreliable."""
    log_w = np.asarray(log_w, float)
    S = len(log_w)
    lw = log_w - log_w.max()
    M = int(min(S / 5, 3 * np.sqrt(S)))
    order = np.argsort(lw)
    tail = order[-M:]
    cutoff = lw[order[-M - 1]]
    exc = np.exp(lw[tail]) - np.exp(cutoff)
    if np.all(exc <= 0):
        k = -np.inf
    else:
        k, sigma = _gpd_fit(exc)
        if np.isfinite(k):
            p = (np.arange(1, M + 1) - 0.5) / M
            q = sigma / k * ((1 - p) ** (-k) - 1) if abs(k) > 1e-12 else -sigma * np.log1p(-p)
            sm = np.log(q + np.exp(cutoff))
            lw = lw.copy()
            lw[tail] = np.minimum(sm, 0.0)
    w = np.exp(lw - lw.max())
    return w / w.sum(), float(k)


def ess_is(w) -> float:
    """Kish's effective sample size of normalized importance weights."""
    w = np.asarray(w, float)
    w = w / w.sum()
    return float(1 / np.sum(w ** 2))


# ---------------------------------------------------------------------------------------------------------------
# Variational inference
# ---------------------------------------------------------------------------------------------------------------
def advi(model: Model, steps: int, rng: np.random.Generator, lr: float = 0.05, samples: int = 4, init=None):
    """Mean-field Gaussian ADVI on the unconstrained space: q(u) = N(m, diag(e^{2 w})), maximizing the ELBO with the
    reparametrization gradient and Adam.  Returns m, w and the ELBO trace."""
    d = model.dim
    m = np.zeros(d) if init is None else np.asarray(init, float).copy()
    w = np.full(d, -1.0)
    am, vm, aw, vw = (np.zeros(d) for _ in range(4))
    b1, b2 = 0.9, 0.999
    elbo = []
    for t in range(1, steps + 1):
        gm, gw, e = np.zeros(d), np.zeros(d), 0.0
        for _ in range(samples):
            z = rng.standard_normal(d)
            u = m + np.exp(w) * z
            lp, g = model.logp_grad(u)
            gm += g
            gw += g * z * np.exp(w) + 1.0
            e += lp
        gm, gw = gm / samples, gw / samples
        elbo.append(e / samples + np.sum(w) + 0.5 * d * (1 + LOG2PI))
        for par, grad, a, v in ((m, gm, am, vm), (w, gw, aw, vw)):
            a[:] = b1 * a + (1 - b1) * grad
            v[:] = b2 * v + (1 - b2) * grad ** 2
            step = lr * (a / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + 1e-8)
            par += step
    return {"mean": m, "log_sd": w, "elbo": np.array(elbo)}


def advi_psis_khat(model: Model, fit: dict, n: int, rng: np.random.Generator) -> float:
    """Yao et al. (2018): PSIS k-hat of the variational approximation as a proposal for the posterior."""
    m, w = fit["mean"], fit["log_sd"]
    U = m + np.exp(w) * rng.standard_normal((n, model.dim))
    lq = np.sum(stats.norm.logpdf(U, m, np.exp(w)), axis=1)
    lp = np.array([model.log_density(u) for u in U])
    return psis(lp - lq)[1]


# ---------------------------------------------------------------------------------------------------------------
# Beyond HMC: Gibbs, SMC, particle filters, ABC, coupling from the past
# ---------------------------------------------------------------------------------------------------------------
def gibbs_probit(X, y, n: int, rng: np.random.Generator, beta0=None):
    """Albert & Chib (1993): y = 1{z > 0}, z ~ N(X beta, 1), flat prior on beta.  Alternate z | beta (truncated
    normals) and beta | z ~ N((X'X)^-1 X'z, (X'X)^-1)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    XtX_inv = np.linalg.inv(X.T @ X)
    L = np.linalg.cholesky(XtX_inv)
    beta = np.zeros(X.shape[1]) if beta0 is None else np.asarray(beta0, float)
    out = np.empty((n, X.shape[1]))
    for i in range(n):
        m = X @ beta
        lo = np.where(y == 1, -m, -np.inf)
        hi = np.where(y == 1, np.inf, -m)
        z = m + stats.truncnorm.rvs(lo, hi, random_state=rng)
        beta = XtX_inv @ (X.T @ z) + L @ rng.standard_normal(X.shape[1])
        out[i] = beta
    return out


def smc_tempering(sample_prior, log_lik, log_prior, n: int, rng: np.random.Generator, target_ess: float = 0.5,
                  mh_steps: int = 5):
    """Likelihood-tempered SMC (Del Moral, Doucet & Jasra 2006): particles move from the prior (phi = 0) to the
    posterior (phi = 1), the next temperature chosen so the ESS falls to ``target_ess`` n; resampled, then rejuvenated
    by random-walk Metropolis steps scaled by the particles' covariance.  Returns particles, the temperature path and
    the log evidence, sum_t log mean_i w_i."""
    x = np.asarray(sample_prior(n, rng), float)
    if x.ndim == 1:
        x = x[:, None]
    ll = np.array([log_lik(xi) for xi in x])
    lpr = np.array([log_prior(xi) for xi in x])
    phi, log_z, path = 0.0, 0.0, [0.0]
    while phi < 1:
        def ess_at(p):
            lw = (p - phi) * ll
            w = np.exp(lw - lw.max())
            return (w.sum() ** 2) / np.sum(w ** 2) / n
        if ess_at(1.0) >= target_ess:
            new = 1.0
        else:
            lo_, hi_ = phi, 1.0
            for _ in range(60):
                mid = 0.5 * (lo_ + hi_)
                lo_, hi_ = (mid, hi_) if ess_at(mid) > target_ess else (lo_, mid)
            new = lo_
        lw = (new - phi) * ll
        mx = lw.max()
        log_z += mx + np.log(np.mean(np.exp(lw - mx)))
        w = np.exp(lw - mx)
        w /= w.sum()
        idx = rng.choice(n, n, p=w)
        x, ll, lpr = x[idx], ll[idx], lpr[idx]
        phi = new
        path.append(phi)
        cov = np.atleast_2d(np.cov(x.T)) * (2.38 ** 2 / x.shape[1]) + 1e-12 * np.eye(x.shape[1])
        Lc = np.linalg.cholesky(cov)
        for _ in range(mh_steps):
            prop = x + rng.standard_normal(x.shape) @ Lc.T
            ll_p = np.array([log_lik(xi) for xi in prop])
            lpr_p = np.array([log_prior(xi) for xi in prop])
            acc = np.log(rng.random(n)) < phi * (ll_p - ll) + lpr_p - lpr
            x[acc], ll[acc], lpr[acc] = prop[acc], ll_p[acc], lpr_p[acc]
    return {"particles": x, "phi": np.array(path), "log_evidence": float(log_z)}


def particle_filter(y, n: int, q: float, r: float, rng: np.random.Generator, m0: float = 0.0, s0: float = 10.0):
    """The bootstrap particle filter (Gordon, Salmond & Smith 1993) for the local-level model x_t = x_{t-1} + N(0, q),
    y_t = x_t + N(0, r): filtered means, and an unbiased estimate of the likelihood (returned as its log)."""
    y = np.asarray(y, float)
    x = m0 + s0 * rng.standard_normal(n)
    means, ll = np.empty(len(y)), 0.0
    for t, yt in enumerate(y):
        if t > 0:
            x = x + np.sqrt(q) * rng.standard_normal(n)
        lw = stats.norm.logpdf(yt, x, np.sqrt(r))
        mx = lw.max()
        w = np.exp(lw - mx)
        ll += mx + np.log(w.mean())
        w /= w.sum()
        means[t] = np.sum(w * x)
        x = x[rng.choice(n, n, p=w)]
    return {"mean": means, "loglik": float(ll)}


def kalman_local_level(y, q: float, r: float, m0: float = 0.0, s0: float = 10.0):
    """The exact filter for the same model: filtered means and variances, and the log likelihood."""
    y = np.asarray(y, float)
    m, P_ = m0, s0 ** 2
    means, vars_, ll = np.empty(len(y)), np.empty(len(y)), 0.0
    for t, yt in enumerate(y):
        if t > 0:
            P_ = P_ + q
        S_ = P_ + r
        ll += stats.norm.logpdf(yt, m, np.sqrt(S_))
        K = P_ / S_
        m = m + K * (yt - m)
        P_ = (1 - K) * P_
        means[t], vars_[t] = m, P_
    return {"mean": means, "var": vars_, "loglik": float(ll)}


def abc_rejection(sample_prior, simulate, summary, s_obs, n: int, eps: float, rng: np.random.Generator):
    """Rejection ABC: keep prior draws whose simulated summary lands within eps of the observed one."""
    keep, tried = [], 0
    s_obs = np.atleast_1d(np.asarray(s_obs, float))
    while len(keep) < n:
        th = sample_prior(rng)
        s = np.atleast_1d(np.asarray(summary(simulate(th, rng)), float))
        tried += 1
        if np.max(np.abs(s - s_obs)) <= eps:
            keep.append(th)
    return {"draws": np.array(keep), "accept_rate": n / tried}


def cftp_ising(L: int, beta: float, rng: np.random.Generator, t_start: int = 1):
    """Propp & Wilson's (1996) coupling from the past for the Ising model on an L x L torus with heat-bath updates:
    run the all-plus and all-minus chains from time -T to 0 with the same random numbers, doubling T until they meet.
    The common state at time 0 is an exact draw.  Returns the state, the T used and the two chains' trajectories of
    the magnetization."""
    T = t_start
    us = []  # random numbers for times -1, -2, ...: reused as T grows, as the method requires
    sites = [(i, j) for i in range(L) for j in range(L)]

    def sweep(s, u):
        for k, (i, j) in enumerate(sites):
            h = s[(i + 1) % L, j] + s[(i - 1) % L, j] + s[i, (j + 1) % L] + s[i, (j - 1) % L]
            p_plus = 1 / (1 + np.exp(-2 * beta * h))
            s[i, j] = 1 if u[k] < p_plus else -1

    while True:
        while len(us) < T:
            us.append(rng.random(L * L))
        top, bot = np.ones((L, L), int), -np.ones((L, L), int)
        mags = []
        for t in range(T - 1, -1, -1):  # time -T ... -1, using us[t] for time -(t+1)
            sweep(top, us[t])
            sweep(bot, us[t])
            mags.append((top.mean(), bot.mean()))
        if np.array_equal(top, bot):
            return {"state": top, "T": T, "mags": np.array(mags)}
        T *= 2
