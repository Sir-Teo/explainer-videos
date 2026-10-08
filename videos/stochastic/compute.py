"""Precompute every simulation shown in the stochastic-calculus video.

    python -m videos.stochastic.compute               # everything missing (~2 min on 4 cores)
    python -m videos.stochastic.compute hero qv       # specific items
    python -m videos.stochastic.compute --force       # recompute

Results are cached in ``.cache/stochastic/<name>.npz``; scenes call ``load(name)``
and never simulate anything themselves.  Nothing here is a cartoon: every path
is a seeded NumPy simulation (PCG64), every histogram is counted from simulated
samples, every PDE solution is a numerical solve, and every number the
narration quotes is computed here and, where theory predicts it, asserted
against that prediction.

Items:
    hero        "our path": one Brownian path on [0, 1] at 2^22 steps; its Riemann-type sums
                (left, right, midpoint), quadratic and total variation, Taylor terms of W^3
    others      five more paths: the hook's "missing half" on paths we didn't pick
    walk        coin-flip walks for the scaling triptych; 20,000 walks for the bell curve
    fan         200 Brownian paths and 20,000 samples of W at t = 1/4, 1/2, 1
    hook2d      a 2D Brownian particle (with a trail) and a cloud of 2,000 diffusing from a point
    qv          the quadratic variation Q_n of 4,000 fresh paths for n = 16, 256, 4096
    ito_mc      40,000 Ito integrals of W dW: mean 0, variance 1/2 (Ito isometry)
    coin        the +50% / -40% coin game, 10,000 players for 100 rounds
    gbm         geometric Brownian motion: Euler-Maruyama vs the naive and Ito solutions; a fan
    ou          the Ornstein-Uhlenbeck process: 3,000 particles relaxing to N(0, sigma^2 / 2 theta)
    heat        4,000 Brownian particles from a point (the heat kernel)
    well        3,000 particles in the double well V = (x^2 - 1)^2 and the Fokker-Planck solution
    exit        gambler's ruin: Brownian motion from x = 0.3 until it leaves (0, 1)
    disk        Kakutani: Brownian walkers solving Laplace's equation in a disk
    hedge       delta-hedging a call option at 4, 16, 64, 256 rebalances; the Black-Scholes price by Monte Carlo
    girsanov    reweighted paths and importance sampling of P(W_1 > 4)
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np
from scipy.special import erfc

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "stochastic"

HERO_LOG2 = 22  # 4,194,304 steps on [0, 1]
HERO_SEED = 174  # chosen so the path ends clearly above zero and stays on screen (see hero_ok)
HERO_LEVELS = [4, 8, 16, 32, 64, 256, 1024, 4096, 65536, 2**HERO_LOG2]

# The coin game and its continuous cousin
COIN_UP, COIN_DOWN, COIN_ROUNDS, COIN_PLAYERS = 1.5, 0.6, 100, 10_000
GBM_MU, GBM_SIGMA = 0.05, 0.45  # per round: the coin game's mean return and its standard deviation

# Ornstein-Uhlenbeck
OU_THETA, OU_SIGMA, OU_X0 = 1.0, 1.0, 2.0

# Double well
WELL_SIGMA = 0.8

# Black-Scholes
BS = dict(S0=100.0, K=100.0, r=0.05, sigma=0.2, T=1.0, mu=0.10)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def norm_cdf(x):
    return 0.5 * erfc(-np.asarray(x, float) / math.sqrt(2))


# ---------------------------------------------------------------------------
# The hero path
# ---------------------------------------------------------------------------
def brownian(seed: int, log2n: int) -> np.ndarray:
    n = 2**log2n
    dW = rng(seed).standard_normal(n) * math.sqrt(1.0 / n)
    return np.concatenate([[0.0], np.cumsum(dW)])


def hero_ok(W: np.ndarray) -> bool:
    """A path that makes a good on-screen example: it ends clearly above zero (so W^2/2 is visibly
    not the answer), stays on screen, and spends some time on both sides of zero."""
    return 0.9 < W[-1] < 1.3 and W.max() < 1.6 and W.min() < -0.25 and W.min() > -0.9


def pick_hero(max_seed=200) -> int:
    for s in range(max_seed):
        if hero_ok(brownian(s, 14)):  # coarse version; the fine path refines it
            W = brownian(s, HERO_LOG2)
            if hero_ok(W):
                return s
    raise RuntimeError("no hero seed")


def sums_at(W: np.ndarray, n: int) -> dict:
    """Riemann-type sums of W dW at n equal steps, and the variations."""
    N = len(W) - 1
    w = W[:: N // n]
    d = np.diff(w)
    return dict(
        left=float(np.sum(w[:-1] * d)),
        right=float(np.sum(w[1:] * d)),
        mid=float(np.sum(0.5 * (w[:-1] + w[1:]) * d)),
        qv=float(np.sum(d * d)),
        tv=float(np.sum(np.abs(d))),
        cube1=float(np.sum(3 * w[:-1] ** 2 * d)),
        cube2=float(np.sum(3 * w[:-1] * d * d)),
        cube3=float(np.sum(d**3)),
    )


def compute_hero():
    assert hero_ok(brownian(HERO_SEED, HERO_LOG2)), "HERO_SEED no longer qualifies: run pick_hero()"
    W = brownian(HERO_SEED, HERO_LOG2)
    rows = [sums_at(W, n) for n in HERO_LEVELS]
    out = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    WT = W[-1]
    # Exact identities at every level (algebra, not limits)
    assert np.allclose(out["left"], 0.5 * WT**2 - 0.5 * out["qv"])
    assert np.allclose(out["right"], 0.5 * WT**2 + 0.5 * out["qv"])
    assert np.allclose(out["mid"], 0.5 * WT**2)
    assert np.allclose(out["cube1"] + out["cube2"] + out["cube3"], WT**3)
    # Limits at the finest level: QV -> 1 (sd sqrt(2/N) = 0.0007), the cubic term -> 0
    assert abs(out["qv"][-1] - 1) < 0.003, out["qv"][-1]
    assert abs(out["cube3"][-1]) < 0.01
    # The target of the second Taylor term: 3 * int_0^1 W dt
    int_W = float(np.mean(0.5 * (W[:-1] + W[1:])))
    assert abs(out["cube2"][-1] - 3 * int_W) < 0.01
    # Secant slopes at the zoom point, h = 4^-k
    t_star = ZOOM_T
    i0 = int(round(t_star * (len(W) - 1)))
    hs = 4.0 ** -np.arange(1, 10)
    slopes = np.array([(W[i0 + int(h * (len(W) - 1))] - W[i0]) / h for h in hs])
    return dict(W=W, n=np.array(HERO_LEVELS), int_W=np.array([int_W]), hs=hs, slopes=slopes, **out)


ZOOM_T = 0.6125  # where the self-similarity zoom dives in


def compute_others():
    """The same left sum on five more paths: the gap to W^2/2 is always about one half."""
    rows = []
    for s in range(1001, 1006):
        W = brownian(s, 16)
        r = sums_at(W, 2**16)
        rows.append([W[-1], r["left"], 0.5 * W[-1] ** 2, 0.5 * W[-1] ** 2 - r["left"]])
    rows = np.array(rows)
    assert np.all(np.abs(rows[:, 3] - 0.5) < 0.02), rows[:, 3]
    paths = np.stack([brownian(s, 16)[::64] for s in range(1001, 1006)])
    return dict(rows=rows, paths=paths)


# ---------------------------------------------------------------------------
# Random walks and the fan of Brownian paths
# ---------------------------------------------------------------------------
WALK_NS = [16, 64, 256, 1024, 4096]


def compute_walk():
    g = rng(11)
    out = {}
    for n in WALK_NS:
        flips = g.integers(0, 2, n) * 2 - 1
        out[f"S{n}"] = np.concatenate([[0], np.cumsum(flips)]).astype(np.int32)
    # 20,000 walks of 64 steps: the endpoint S_64 / 8 approaches N(0, 1)
    n = 64
    ends = (g.integers(0, 2, (20_000, n)) * 2 - 1).sum(axis=1)
    out["ends64"] = ends.astype(np.int32)
    assert abs(ends.mean() / 8) < 0.03 and abs(ends.var() / 64 - 1) < 0.04
    # 120 of them drawn as paths
    out["paths64"] = np.concatenate([np.zeros((120, 1)), np.cumsum(g.integers(0, 2, (120, n)) * 2 - 1, axis=1)],
                                    axis=1).astype(np.int32)
    out["first16"] = (np.diff(out["S16"]) > 0).astype(np.int32)  # the coin flips themselves, H = 1
    return out


def compute_fan():
    g = rng(12)
    n = 512
    dW = g.standard_normal((200, n)) * math.sqrt(1 / n)
    paths = np.concatenate([np.zeros((200, 1)), np.cumsum(dW, axis=1)], axis=1)
    samples = {}
    m = 20_000
    a = g.standard_normal(m) * math.sqrt(0.25)
    b = a + g.standard_normal(m) * math.sqrt(0.25)
    c = b + g.standard_normal(m) * math.sqrt(0.5)
    for t, x in [(0.25, a), (0.5, b), (1.0, c)]:
        assert abs(x.var() / t - 1) < 0.04
        samples[f"t{int(t * 100)}"] = x
    # the share inside one and two standard deviations at t = 1
    inside1 = float(np.mean(np.abs(c) < 1))
    inside2 = float(np.mean(np.abs(c) < 2))
    assert abs(inside1 - 0.6827) < 0.01 and abs(inside2 - 0.9545) < 0.005
    return dict(paths=paths, inside=np.array([inside1, inside2]), **samples)


def compute_hook2d():
    g = rng(13)
    # One particle: 12 s at 30 fps, 8 substeps per frame
    frames, sub = 420, 8
    steps = g.standard_normal((frames * sub, 2)) * 0.055
    particle = np.concatenate([[[0, 0]], np.cumsum(steps, axis=0)])[::1]
    # A cloud of 2000 from the origin, diffusion constant chosen so it fills the frame in ~10 s
    n, frames_c = 2000, 300
    kicks = g.standard_normal((frames_c, n, 2)) * 0.12
    cloud = np.concatenate([np.zeros((1, n, 2)), np.cumsum(kicks, axis=0)]).astype(np.float32)
    # Einstein: mean squared displacement grows linearly, <r^2> = 2 * 2 D t (2 dims, var 0.12^2 per frame per axis)
    msd = (cloud**2).sum(axis=2).mean(axis=1)
    k = np.arange(frames_c + 1)
    assert np.allclose(msd[1:], 2 * 0.12**2 * k[1:], rtol=0.08)
    return dict(particle=particle, cloud=cloud, msd=msd)


# ---------------------------------------------------------------------------
# Quadratic variation and the Ito integral
# ---------------------------------------------------------------------------
def compute_qv():
    g = rng(21)
    out = {}
    for n in [16, 256, 4096]:
        q = np.empty(4000)
        for i in range(0, 4000, 500):
            d = g.standard_normal((500, n)) * math.sqrt(1 / n)
            q[i:i + 500] = (d * d).sum(axis=1)
        sd = q.std()
        assert abs(q.mean() - 1) < 3 * sd / math.sqrt(4000) + 1e-3
        assert abs(sd / math.sqrt(2 / n) - 1) < 0.06, (n, sd)
        out[f"q{n}"] = q
    return out


def compute_ito_mc():
    g = rng(31)
    m, n = 40_000, 1000
    ints = np.empty(m)
    WT = np.empty(m)
    qv = np.empty(m)
    for i in range(0, m, 1000):
        d = g.standard_normal((1000, n)) * math.sqrt(1 / n)
        W = np.concatenate([np.zeros((1000, 1)), np.cumsum(d, axis=1)], axis=1)
        ints[i:i + 1000] = (W[:, :-1] * d).sum(axis=1)
        WT[i:i + 1000] = W[:, -1]
        qv[i:i + 1000] = (d * d).sum(axis=1)
    assert np.allclose(ints, 0.5 * WT**2 - 0.5 * qv)
    mean, var = ints.mean(), ints.var()
    assert abs(mean) < 3 * math.sqrt(0.5 / m), mean  # E = 0
    assert abs(var - 0.5) < 0.02, var  # E[(int W dW)^2] = int_0^1 t dt = 1/2
    naive = 0.5 * WT**2
    assert abs(naive.mean() - 0.5) < 0.02  # the "ordinary calculus" answer has mean T/2, not 0
    return dict(ints=ints, WT=WT, stats=np.array([mean, var, naive.mean(), ints.min()]))


# ---------------------------------------------------------------------------
# Multiplicative noise
# ---------------------------------------------------------------------------
def compute_coin():
    g = rng(41)
    heads = g.integers(0, 2, (COIN_PLAYERS, COIN_ROUNDS)).astype(bool)
    logw = np.concatenate([np.zeros((COIN_PLAYERS, 1)),
                           np.cumsum(np.where(heads, math.log(COIN_UP), math.log(COIN_DOWN)), axis=1)], axis=1)
    pct = np.percentile(logw, [5, 25, 50, 75, 95], axis=0)
    sample_mean = np.log(np.exp(logw).mean(axis=0))
    t = np.arange(COIN_ROUNDS + 1)
    theory_mean = t * math.log(0.5 * (COIN_UP + COIN_DOWN))
    theory_median = t * 0.5 * math.log(COIN_UP * COIN_DOWN)
    lost = float(np.mean(logw[:, -1] < 0))
    # exact: lose money after 100 rounds iff heads <= 55
    from math import comb
    lost_exact = sum(comb(100, k) for k in range(56)) / 2**100
    assert abs(lost - lost_exact) < 0.01, (lost, lost_exact)
    assert abs(np.median(logw[:, -1]) - theory_median[-1]) < 0.75  # median of a discrete binomial
    return dict(paths=logw[:80], pct=pct, sample_mean=sample_mean, theory_mean=theory_mean,
                theory_median=theory_median, lost=np.array([lost, lost_exact]), final=logw[:, -1])


def compute_gbm():
    g = rng(42)
    mu, sig, T = GBM_MU, GBM_SIGMA, 100.0
    # One path, three answers, the same Brownian increments
    n = 1_000_000
    dt = T / n
    dW = g.standard_normal(n) * math.sqrt(dt)
    W = np.concatenate([[0], np.cumsum(dW)])
    em = np.concatenate([[1.0], np.cumprod(1 + mu * dt + sig * dW)])  # Euler-Maruyama: S += mu S dt + sig S dW
    t = np.linspace(0, T, n + 1)
    ito = np.exp((mu - 0.5 * sig**2) * t + sig * W)
    naive = np.exp(mu * t + sig * W)
    err = np.max(np.abs(np.log(em) - np.log(ito)))
    assert err < 0.05, err  # EM converges to Ito's solution...
    assert np.log(naive[-1]) - np.log(em[-1]) > 9  # ...and not to the naive one (off by sig^2/2 * T = 10.1)
    stride = 2000
    one = dict(t=t[::stride], em=np.log(em[::stride]), ito=np.log(ito[::stride]),
               naive=np.log(naive[::stride]), W=W[::stride])
    # A fan of 4000 exact GBM paths (on the log scale they are Brownian motion with drift)
    m, k = 4000, 400
    dW = g.standard_normal((m, k)) * math.sqrt(T / k)
    tt = np.linspace(0, T, k + 1)
    logS = (mu - 0.5 * sig**2) * tt + np.concatenate([np.zeros((m, 1)), np.cumsum(sig * dW, axis=1)], axis=1)
    below = float(np.mean(logS[:, -1] < 0))
    exact_below = float(norm_cdf(-(mu - 0.5 * sig**2) * T / (sig * math.sqrt(T))))
    assert abs(below - exact_below) < 0.025
    pct = np.percentile(logS, [5, 25, 50, 75, 95], axis=0)
    return dict(paths=logS[:100], tt=tt, pct=pct, below=np.array([below, exact_below]), final=logS[:, -1],
                **{f"one_{k_}": v for k_, v in one.items()})


# ---------------------------------------------------------------------------
# SDEs, Fokker-Planck, Feynman-Kac
# ---------------------------------------------------------------------------
def compute_ou():
    g = rng(51)
    th, sig, x0 = OU_THETA, OU_SIGMA, OU_X0
    m, T, fps_frames = 3000, 5.0, 300  # frames for animation: t = 0 .. 5
    sub = 20
    dt = T / (fps_frames * sub)
    X = np.full(m, x0)
    frames = [X.copy()]
    for _ in range(fps_frames):
        for _ in range(sub):
            X = X - th * X * dt + sig * math.sqrt(dt) * g.standard_normal(m)
        frames.append(X.copy())
    frames = np.array(frames, dtype=np.float32)
    ts = np.linspace(0, T, fps_frames + 1)
    mean_th = x0 * np.exp(-th * ts)
    var_th = sig**2 * (1 - np.exp(-2 * th * ts)) / (2 * th)
    for k in [15, 60, 240]:  # t = 0.25, 1, 4
        assert abs(frames[k].mean() - mean_th[k]) < 0.04
        assert abs(frames[k].var() / var_th[k] - 1) < 0.08
    return dict(frames=frames, ts=ts, mean=mean_th, var=var_th)


def compute_heat():
    g = rng(52)
    m, frames, T = 4000, 240, 1.0
    dW = g.standard_normal((frames, m)) * math.sqrt(T / frames)
    X = np.concatenate([np.zeros((1, m)), np.cumsum(dW, axis=0)]).astype(np.float32)
    assert abs(X[-1].var() - 1) < 0.06
    return dict(frames=X, ts=np.linspace(0, T, frames + 1))


def well_V(x):
    return (x * x - 1) ** 2


def well_drift(x):
    return -4 * x * (x * x - 1)


def compute_well():
    g = rng(53)
    sig = WELL_SIGMA
    m, T, frames, sub = 3000, 40.0, 720, 40
    dt = T / (frames * sub)
    X = -1 + 0.05 * g.standard_normal(m)
    out = [X.copy()]
    for _ in range(frames):
        for _ in range(sub):
            X = X + well_drift(X) * dt + sig * math.sqrt(dt) * g.standard_normal(m)
        out.append(X.copy())
    out = np.array(out, dtype=np.float32)
    # Fokker-Planck by finite volumes on [-2.2, 2.2]: p_t = -(mu p)_x + (sig^2/2) p_xx, zero-flux walls
    L, nx = 2.2, 440
    edges = np.linspace(-L, L, nx + 1)
    xc = 0.5 * (edges[:-1] + edges[1:])
    dx = edges[1] - edges[0]
    p = np.exp(-((xc + 1) ** 2) / (2 * 0.05**2))
    p /= p.sum() * dx
    D = 0.5 * sig**2
    mu_e = well_drift(edges[1:-1])
    dt_pde = 0.2 * dx * dx / D
    dt_pde = min(dt_pde, 0.4 * dx / np.abs(well_drift(edges)).max())
    steps = int(math.ceil(T / frames / dt_pde))
    dt_pde = T / frames / steps
    dens = [p.copy()]
    for _ in range(frames):
        for _ in range(steps):
            # flux at interior faces: upwinded advection + central diffusion
            adv = np.where(mu_e > 0, mu_e * p[:-1], mu_e * p[1:])
            dif = -D * (p[1:] - p[:-1]) / dx
            F = np.concatenate([[0.0], adv + dif, [0.0]])
            p = p - dt_pde / dx * (F[1:] - F[:-1])
        dens.append(p.copy())
    dens = np.array(dens, dtype=np.float32)
    boltz = np.exp(-2 * well_V(xc) / sig**2)
    boltz /= boltz.sum() * dx
    assert abs(dens[-1].sum() * dx - 1) < 1e-6
    assert 0.5 * np.abs(dens[-1] - boltz).sum() * dx < 0.03  # PDE relaxed to Boltzmann
    coarse = edges[::10]  # 44 bins: 3,000 particles in 440 bins would be mostly sampling noise
    hist, _ = np.histogram(out[-1], bins=coarse)
    b_coarse = boltz.reshape(-1, 10).sum(axis=1) * dx
    assert 0.5 * np.abs(hist / m - b_coarse).sum() < 0.06, 0.5 * np.abs(hist / m - b_coarse).sum()  # and so did the particles
    right = float(np.mean(out[-1] > 0))
    return dict(frames=out, ts=np.linspace(0, T, frames + 1), xc=xc, dens=dens, boltz=boltz,
                right=np.array([right]))


def compute_exit():
    """Brownian motion from x0 = 0.3, stopped when it leaves (0, 1)."""
    g = rng(61)
    x0, m, dt = 0.3, 4000, 1e-5
    X = np.full(m, x0)
    alive = np.ones(m, bool)
    tau = np.zeros(m)
    hit_top = np.zeros(m, bool)
    shown = 40
    trace = [X[:shown].copy()]
    t = 0.0
    while alive.any():
        X = np.where(alive, X + math.sqrt(dt) * g.standard_normal(m), X)
        t += dt
        out_top = alive & (X >= 1)
        out_bot = alive & (X <= 0)
        hit_top |= out_top
        tau[out_top | out_bot] = t
        alive &= ~(out_top | out_bot)
        if len(trace) < 300_000:
            trace.append(np.where(alive[:shown], X[:shown], np.clip(X[:shown], 0, 1)))
    trace = np.array(trace, dtype=np.float32)[::40]
    p_top = float(hit_top.mean())
    se = math.sqrt(0.3 * 0.7 / m)
    assert abs(p_top - x0) < 3 * se + 0.005, p_top  # u(x) = x solves u'' = 0
    assert abs(tau.mean() - x0 * (1 - x0)) < 0.01, tau.mean()  # E tau = x(1-x) solves u''/2 = -1
    return dict(trace=trace, tau=tau, hit_top=hit_top, dt=np.array([dt * 40]),
                stats=np.array([p_top, tau.mean(), x0, x0 * (1 - x0)]))


def disk_g(theta):
    """Boundary temperature on the unit circle: three hot arcs and three cold ones."""
    return (np.sin(3 * theta) > 0).astype(float)


def disk_exact(x, y):
    r2 = x * x + y * y
    r3 = r2**1.5
    th = np.arctan2(y, x)
    return 0.5 + np.arctan2(2 * r3 * np.sin(3 * th), 1 - r3 * r3) / np.pi


def walk_on_spheres(x, y, g, eps=1e-4):
    """Exit points of Brownian motion from the unit disk, sampled exactly by walk-on-spheres."""
    x, y = x.copy(), y.copy()
    while True:
        r = 1 - np.sqrt(x * x + y * y)
        live = r > eps
        if not live.any():
            break
        a = g.uniform(0, 2 * np.pi, live.sum())
        x[live] += r[live] * np.cos(a)
        y[live] += r[live] * np.sin(a)
    return np.arctan2(y, x)


def compute_disk():
    g = rng(62)
    z0 = np.array([0.32, 0.2])
    # 36 walkers drawn as paths (small Euler steps), each until it leaves the disk
    shown, dt = 36, 4e-5
    paths, ends = [], []
    for _ in range(shown):
        p = [z0.copy()]
        z = z0.copy()
        while z @ z < 1:
            z = z + math.sqrt(dt) * g.standard_normal(2)
            p.append(z.copy())
        z = z / math.sqrt(z @ z)
        p[-1] = z
        p = np.array(p)
        stride = max(1, len(p) // 2500)
        paths.append(np.concatenate([p[::stride], p[-1:]]))
        ends.append(math.atan2(z[1], z[0]))
    lens = [len(p) for p in paths]
    P = np.full((shown, max(lens), 2), np.nan, np.float32)
    for i, p in enumerate(paths):
        P[i, : len(p)] = p
    # Running average at z0 from 20,000 walkers (walk on spheres)
    m = 20_000
    th = walk_on_spheres(np.full(m, z0[0]), np.full(m, z0[1]), g)
    vals = disk_g(th)
    exact0 = float(disk_exact(z0[0], z0[1]))
    assert abs(vals.mean() - exact0) < 3 * math.sqrt(0.25 / m) + 0.002, (vals.mean(), exact0)
    # The whole field: Monte Carlo with 1, 4, 16, 64, 256 walkers per pixel
    n = 160
    xs = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(xs, -xs)
    inside = X**2 + Y**2 < 0.995
    px, py = X[inside], Y[inside]
    totals = np.zeros(px.size)
    fields, done = {}, 0
    for k in [1, 4, 16, 64, 256]:
        for _ in range(k - done):
            totals += disk_g(walk_on_spheres(px, py, g))
        done = k
        F = np.full(X.shape, np.nan)
        F[inside] = totals / k
        fields[f"mc{k}"] = F.astype(np.float32)
    E = np.full(X.shape, np.nan)
    E[inside] = disk_exact(px, py)
    err = np.nanmean(np.abs(fields["mc256"] - E))
    assert err < 0.03, err
    return dict(paths=P, lens=np.array(lens), ends=np.array(ends), z0=z0, run=vals.astype(np.float32),
                exact0=np.array([exact0]), exact=E.astype(np.float32), mc_err=np.array([err]), **fields)


# ---------------------------------------------------------------------------
# Black-Scholes and Girsanov
# ---------------------------------------------------------------------------
def bs_call(S, K, r, sigma, tau):
    S = np.asarray(S, float)
    tau = np.asarray(tau, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        sq = sigma * np.sqrt(tau)
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / sq
        d2 = d1 - sq
        v = S * norm_cdf(d1) - K * np.exp(-r * tau) * norm_cdf(d2)
        delta = norm_cdf(d1)
    payoff = np.maximum(S - K, 0)
    v = np.where(tau > 0, v, payoff)
    delta = np.where(tau > 0, delta, (S > K).astype(float))
    return v, delta


def compute_hedge():
    g = rng(71)
    S0, K, r, sig, T, mu = (BS[k] for k in ("S0", "K", "r", "sigma", "T", "mu"))
    price, _ = bs_call(S0, K, r, sig, T)
    price = float(price)
    # Monte Carlo under the risk-neutral measure: S_T = S0 exp((r - sig^2/2) T + sig sqrt(T) Z)
    Z = g.standard_normal(1_000_000)
    ST = S0 * np.exp((r - 0.5 * sig**2) * T + sig * math.sqrt(T) * Z)
    disc = math.exp(-r * T) * np.maximum(ST - K, 0)
    mc, mc_se = float(disc.mean()), float(disc.std() / math.sqrt(len(disc)))
    assert abs(mc - price) < 3 * mc_se, (mc, price)
    out = dict(price=np.array([price, mc, mc_se]))
    # Delta hedging under the REAL-world drift mu: sell the call for its price, hold Delta shares, bank the rest
    stds = []
    for n in [4, 16, 64, 256]:
        m = 5000
        dt = T / n
        S = np.full(m, S0)
        _, delta = bs_call(S, K, r, sig, T)
        cash = price - delta * S
        for k in range(1, n + 1):
            S = S * np.exp((mu - 0.5 * sig**2) * dt + sig * math.sqrt(dt) * g.standard_normal(m))
            cash = cash * math.exp(r * dt)
            if k < n:
                _, new = bs_call(S, K, r, sig, T - k * dt)
                cash -= (new - delta) * S
                delta = new
        pnl = cash + delta * S - np.maximum(S - K, 0)
        out[f"pnl{n}"] = pnl
        stds.append(pnl.std())
    stds = np.array(stds)
    ratios = stds[:-1] / stds[1:]
    assert np.all(np.abs(ratios - 2) < 0.35), ratios  # error ~ 1/sqrt(n)
    out["stds"] = stds
    # One showcase path, weekly rebalancing: option value vs the replicating portfolio
    n = 52
    dt = T / n
    S = [S0]
    for _ in range(n):
        S.append(S[-1] * math.exp((mu - 0.5 * sig**2) * dt + sig * math.sqrt(dt) * g.standard_normal()))
    S = np.array(S)
    ts = np.linspace(0, T, n + 1)
    V, D = bs_call(S, K, r, sig, T - ts)
    port = [price]
    cash = price - D[0] * S[0]
    for k in range(1, n + 1):
        cash *= math.exp(r * dt)
        port.append(cash + D[k - 1] * S[k])
        cash -= (D[k] - D[k - 1]) * S[k]
    out.update(path_S=S, path_t=ts, path_V=V, path_D=D, path_P=np.array(port))
    return out


def compute_girsanov():
    g = rng(81)
    m, n = 400, 256
    dW = g.standard_normal((m, n)) * math.sqrt(1 / n)
    paths = np.concatenate([np.zeros((m, 1)), np.cumsum(dW, axis=1)], axis=1)
    # Reweighting check with a big sample: E_Q[W_1] = theta under weights exp(theta W_1 - theta^2/2)
    big = g.standard_normal(200_000)
    for th in [0.5, 1.0, 1.5]:
        w = np.exp(th * big - 0.5 * th**2)
        assert abs(w.mean() - 1) < 0.02 and abs((w * big).mean() / w.mean() - th) < 0.03
    # Importance sampling for P(W_1 > 4)
    exact = float(norm_cdf(-4.0))
    plain = g.standard_normal(100_000)
    hits = int((plain > 4).sum())
    th = 4.0
    shifted = g.standard_normal(10_000) + th
    w = np.exp(-th * shifted + 0.5 * th**2) * (shifted > 4)
    est, se = float(w.mean()), float(w.std() / math.sqrt(len(w)))
    assert abs(est - exact) < 3 * se
    return dict(paths=paths, is_stats=np.array([exact, hits, hits / 100_000, est, se]))


ITEMS = {
    "hero": compute_hero,
    "others": compute_others,
    "walk": compute_walk,
    "fan": compute_fan,
    "hook2d": compute_hook2d,
    "qv": compute_qv,
    "ito_mc": compute_ito_mc,
    "coin": compute_coin,
    "gbm": compute_gbm,
    "ou": compute_ou,
    "heat": compute_heat,
    "well": compute_well,
    "exit": compute_exit,
    "disk": compute_disk,
    "hedge": compute_hedge,
    "girsanov": compute_girsanov,
}


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing '{name}'. Run: python -m videos.stochastic.compute {name}")
        with np.load(p, allow_pickle=False) as data:
            _loaded[name] = {k: data[k] for k in data.files}
    return _loaded[name]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  compute {name} ...", flush=True)
        out = ITEMS[name]()
        tmp = DATA_DIR / f"{name}.tmp.npz"
        np.savez_compressed(tmp, **out)
        tmp.replace(path(name))
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
