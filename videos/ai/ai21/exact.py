"""Part 21's exact experiments: everything that can be computed with the true score, no network (numpy only).

The data is Part 5's letters "AI" made into a smooth density: a mixture of K small Gaussians (k-means centres of the
letter points, each of width S0, equal weights).  Then everything a diffusion model is meant to learn is known in
closed form at every noise level: for x = a x0 + b n (x0 from the mixture, n standard normal) the density p(x), its
score, and the best guess of the clean point E[x0 | x] (``posterior``).  That makes it a test bench:

    forward     the DDPM forward chain (1,000 small steps, linear betas) against its closed form, one jump
    tweedie     Tweedie's formula: the posterior mean found by brute force (1D on a grid, 2D by Monte Carlo) against
                (x + sigma^2 score) / alpha; and the best denoiser's guesses at four noise levels
    sde         the reverse SDE and the probability-flow ODE (linear-beta VP), from the same noise: marginals at every
                time against direct samples, paths, and the ODE run there and back
    solvers     samplers with the exact denoiser: DDPM, Euler, DDIM, Heun (EDM), DPM-Solver-2, DPM-Solver++(2M); error
                against a reference solution and distance from the data, by number of network evaluations
    schedules   noise schedules: log-SNR curves, where training spends its noise levels, the linear schedule's terminal
                SNR, and time-step spacings for DDIM compared
    edmtargets  EDM's preconditioning on this data: the variance of each regression target, the error amplification,
                the irreducible loss at each noise level
    transport   optimal transport and flow matching: the exact marginal velocity field, its marginals checked against
                the interpolation at four times, path straightness, transport cost against the optimal (Hungarian)
                coupling, and the diffusion (trigonometric) interpolant's paths
"""

from __future__ import annotations

import math

import numpy as np

S0 = 0.06  # each mixture component's width
K = 400  # components


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def kmeans(P, k, seed, iters=40):
    """Lloyd's algorithm from a k-means++ start (seeded)."""
    g = rng(seed)
    C = [P[g.integers(len(P))]]
    d2 = ((P - C[0]) ** 2).sum(1)
    for _ in range(k - 1):
        C.append(P[g.choice(len(P), p=d2 / d2.sum())])
        d2 = np.minimum(d2, ((P - C[-1]) ** 2).sum(1))
    C = np.array(C)
    for _ in range(iters):
        lab = np.argmin(((P[:, None] - C[None]) ** 2).sum(-1), 1)
        for j in range(k):
            m = lab == j
            if m.any():
                C[j] = P[m].mean(0)
    return C


_CENTERS = None


def centers():
    global _CENTERS
    if _CENTERS is None:
        from videos.ai.ai21.compute import ai_points

        _CENTERS = kmeans(ai_points(n=8000, seed=0), K, seed=21)
    return _CENTERS


def sample(n, seed):
    """n points from the mixture."""
    g = rng(seed)
    C = centers()
    return C[g.integers(0, len(C), n)] + S0 * g.normal(size=(n, 2))


def posterior(x, a, b):
    """For x = a x0 + b n: E[x0 | x] and the score grad log p(x), exactly (the mixture's responsibilities)."""
    C = centers()
    x = np.asarray(x, float)
    v = a * a * S0 * S0 + b * b
    out_m = np.empty_like(x)
    for i in range(0, len(x), 4096):
        xs = x[i:i + 4096]
        d2 = (xs * xs).sum(1)[:, None] - 2 * a * xs @ C.T + (a * a) * (C * C).sum(1)[None]
        lw = -d2 / (2 * v)
        lw -= lw.max(1, keepdims=True)
        w = np.exp(lw)
        w /= w.sum(1, keepdims=True)
        out_m[i:i + 4096] = w @ C
    ex0 = out_m * (b * b / v) + x * (a * S0 * S0 / v)
    score = (a * out_m - x) / v
    return ex0, score


def density(G, a, b):
    """p(x) on points G, for x = a x0 + b n."""
    C = centers()
    v = a * a * S0 * S0 + b * b
    d2 = ((G[:, None, :] - a * C[None]) ** 2).sum(-1)
    return np.exp(-d2 / (2 * v)).mean(1) / (2 * np.pi * v)


def denoise_edm(x, s):
    """EDM's coordinates: x = x0 + s n.  The best denoiser D(x; s) = E[x0 | x]."""
    return posterior(x, 1.0, s)[0]


def sw(a, b, n_proj=128, seed=0):
    from videos.ai.ai21.compute import sw_distance

    return sw_distance(a, b, n_proj=n_proj, seed=seed)


def floor(n, reps=4):
    """The sliced Wasserstein distance between two independent samples of the data, of n points each."""
    return float(np.mean([sw(sample(n, 900 + 2 * r), sample(n, 901 + 2 * r)) for r in range(reps)]))


# ---------------------------------------------------------------------------
def compute_mix():
    """The test bench itself: the centres, a sample, the density landscape at six noise levels (cosine schedule)."""
    from videos.ai.ai21.compute import vp

    out = dict(centers=centers(), s0=S0, K=K, data=sample(4000, 1))
    lx, ly = np.linspace(-3, 3, 61), np.linspace(-2, 2, 41)
    LX, LY = np.meshgrid(lx, ly)
    G = np.stack([LX.ravel(), LY.ravel()], 1)
    out["land_x"], out["land_y"], out["land_ts"] = lx, ly, [1.0, 0.7, 0.5, 0.35, 0.22, 0.12]
    for t in out["land_ts"]:
        a, s = vp(t)
        out[f"land{t:g}"] = density(G, a, s).reshape(len(ly), len(lx))
    out["floor1500"] = floor(1500)
    out["floor2000"] = floor(2000)
    out["sigma_data"] = float(np.sqrt(out["data"].var(0).mean()))
    print(f"    {K} components; floor {out['floor2000']:.4f}; sigma_data {out['sigma_data']:.3f}", flush=True)
    return out


# ---------------------------------------------------------------------------
def ddpm_schedule(T=1000):
    beta = np.linspace(1e-4, 0.02, T)
    abar = np.cumprod(1 - beta)
    return beta, abar


def compute_forward():
    """DDPM's forward chain, step by step, against its closed form q(x_t | x_0) = N(sqrt(abar) x_0, (1 - abar) I)."""
    beta, abar = ddpm_schedule()
    T = len(beta)
    n = 20000
    x0 = sample(n, 2)
    g = rng(2015)  # Sohl-Dickstein et al.
    x = x0.copy()
    keep = [0, 10, 25, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    checks = [50, 100, 250, 500, 1000]
    frames, rows = [x0[:600].copy()], []
    for t in range(1, T + 1):
        x = math.sqrt(1 - beta[t - 1]) * x + math.sqrt(beta[t - 1]) * g.normal(size=x.shape)
        if t in keep:
            frames.append(x[:600].copy())
        if t in checks:
            ab = abar[t - 1]
            one = math.sqrt(ab) * x0 + math.sqrt(1 - ab) * rng(77 + t).normal(size=x0.shape)  # one jump
            one2 = math.sqrt(ab) * x0 + math.sqrt(1 - ab) * rng(78 + t).normal(size=x0.shape)
            # regress the chain's x_t on x_0: the slope should be sqrt(abar), the leftover variance 1 - abar
            slope = float((x * x0).sum() / (x0 * x0).sum())
            resid = float(((x - slope * x0) ** 2).mean())
            rows.append(dict(t=t, abar=float(ab), slope=slope, slope_pred=math.sqrt(ab), resid=resid, resid_pred=1 - ab,
                             sw_chain=sw(x, one), sw_floor=sw(one2, one)))
    # the ELBO's weight on the noise-guessing error at each step (sigma_t^2 = beta_t): beta / (2 (1 - beta)(1 - abar))
    lam = beta / (2 * (1 - beta) * (1 - abar))
    out = dict(beta=beta, abar=abar, keep=keep, frames=np.array(frames), checks=rows, lam=lam, T=T,
               abar_T=float(abar[-1]), snr_T=float(abar[-1] / (1 - abar[-1])))
    for r in rows:
        print("    t={t}: slope {slope:.4f} (formula {slope_pred:.4f}); leftover {resid:.4f} ({resid_pred:.4f}); "
              "SW chain vs jump {sw_chain:.4f}, floor {sw_floor:.4f}".format(**r), flush=True)
    for r in rows:
        assert abs(r["slope"] - r["slope_pred"]) < 0.02 and abs(r["resid"] - r["resid_pred"]) < 0.03
    return out


# ---------------------------------------------------------------------------
def compute_tweedie():
    from videos.ai.ai21.compute import vp

    out = {}
    # 1D: two bumps; the posterior p(x0 | x_t) on a grid, its mean, and Tweedie's formula from the exact score
    w, mu, sd = np.array([0.35, 0.65]), np.array([-1.6, 1.1]), np.array([0.35, 0.45])
    x0 = np.linspace(-5, 5, 4001)
    p0 = sum(wi * np.exp(-(x0 - m) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi)) for wi, m, s in zip(w, mu, sd))
    out.update(w1=w, mu1=mu, sd1=sd, x0grid=x0[::20], p0=p0[::20])
    for t in (0.35, 0.65):
        a, s = vp(t)
        xs = np.linspace(-3.5, 3.5, 141)
        # the noised density and its score, in closed form (each bump widened)
        v = (a * sd) ** 2 + s * s
        comp = np.array([wi * np.exp(-(xs[:, None] - a * m) ** 2 / (2 * vi)) / np.sqrt(2 * np.pi * vi)
                         for wi, m, vi in zip(w, mu, v)])[:, :, 0]
        pt = comp.sum(0)
        score = (comp * ((a * mu)[:, None] - xs[None]) / v[:, None]).sum(0) / pt
        tweedie = (xs + s * s * score) / a
        # brute force: p(x0 | x) proportional to N(x; a x0, s^2) p0(x0), its mean by quadrature
        lik = np.exp(-(xs[:, None] - a * x0[None]) ** 2 / (2 * s * s)) * p0[None]
        post_mean = (lik * x0[None]).sum(1) / lik.sum(1)
        out[f"t{t:g}_xs"], out[f"t{t:g}_pt"], out[f"t{t:g}_score"] = xs, pt, score
        out[f"t{t:g}_tweedie"], out[f"t{t:g}_mean"] = tweedie, post_mean
        out[f"t{t:g}_maxdiff"] = float(np.abs(tweedie - post_mean).max())
        for xq in (-1.2, 0.2, 1.4):
            post = np.exp(-(xq - a * x0) ** 2 / (2 * s * s)) * p0
            post /= post.sum() * (x0[1] - x0[0])
            out[f"t{t:g}_post{xq:g}"] = post[::20]
        print(f"    1D t={t}: |Tweedie - posterior mean| at most {out[f't{t:g}_maxdiff']:.2e}", flush=True)
    # 2D: the posterior mean by Monte Carlo (weighting 50,000 data samples by how likely each makes x), against the
    # formula with the exact score
    data = sample(50_000, 3)
    rows = []
    for t in (0.2, 0.5, 0.8):
        a, s = vp(t)
        g = rng(int(1000 * t))
        q = a * sample(300, 4 + int(10 * t)) + s * g.normal(size=(300, 2))
        d2 = (q * q).sum(1)[:, None] - 2 * a * q @ data.T + a * a * (data * data).sum(1)[None]
        lw = -d2 / (2 * s * s)
        lw -= lw.max(1, keepdims=True)
        W = np.exp(lw)
        ess = W.sum(1) ** 2 / (W ** 2).sum(1)
        mc = (W @ data) / W.sum(1, keepdims=True)
        ex0, score = posterior(q, a, s)
        tw = (q + s * s * score) / a
        assert np.allclose(tw, ex0, atol=1e-8)  # the formula, algebraically
        err = np.linalg.norm(mc - tw, axis=1)
        rows.append(dict(t=t, mean_err=float(err.mean()), max_err=float(err.max()), ess=float(np.median(ess)),
                         spread=float(np.linalg.norm(tw - tw.mean(0), axis=1).mean())))
        out[f"q{t:g}"], out[f"mc{t:g}"], out[f"tw{t:g}"] = q[:120], mc[:120], tw[:120]
        print(f"    2D t={t}: Monte Carlo vs Tweedie, mean gap {err.mean():.4f} (median ESS {np.median(ess):.0f})",
              flush=True)
    out["mc_rows"] = rows
    # the best denoiser's guesses: E[x0 | x_t] for 600 noisy points at four noise levels (a blur at high noise)
    x0s = sample(600, 5)
    eps = rng(6).normal(size=x0s.shape)
    out["den_ts"] = [0.9, 0.6, 0.35, 0.15]
    for t in out["den_ts"]:
        a, s = vp(t)
        xt = a * x0s + s * eps
        out[f"den_xt{t:g}"], out[f"den_x0{t:g}"] = xt, posterior(xt, a, s)[0]
        # the guess's mean squared error, against the noise level: the irreducible part of the loss
        out[f"den_mse{t:g}"] = float(((out[f"den_x0{t:g}"] - x0s) ** 2).sum(1).mean())
    out["den_clean"] = x0s
    return out


# ---------------------------------------------------------------------------
def vp_linear(t, bmin=0.1, bmax=20.0):
    """Song et al.'s VP SDE: beta(t) linear; alpha(t) = exp(-1/2 int beta)."""
    B = bmin * t + 0.5 * (bmax - bmin) * t * t
    a = np.exp(-0.5 * B)
    return a, np.sqrt(1 - a * a), bmin + (bmax - bmin) * t


def compute_sde():
    """The reverse SDE and the probability-flow ODE on the VP SDE, with the exact score, from the same noise."""
    n = 2000
    T0, T1 = 1.0, 1e-3
    N_sde, N_ode = 1000, 400
    g = rng(2021)  # Song et al., score-based SDEs
    z = g.normal(size=(n, 2))
    snap_t = [1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05, T1]

    def drift(x, t, k):  # f x - k g^2 score, k = 1 (SDE) or 1/2 (ODE)
        a, s, b = vp_linear(t)
        return -0.5 * b * x - k * b * posterior(x, a, s)[1]

    def run(kind):
        N = N_sde if kind == "sde" else N_ode
        ts = np.linspace(T0, T1, N + 1)
        at = {int(np.argmin(np.abs(ts - st))): st for st in snap_t}  # grid index -> snapshot time
        x = z.copy()
        snaps, paths = {T0: z.copy()}, [x[:40].copy()]
        gg = rng(5)
        for i in range(N):
            t, tn = ts[i], ts[i + 1]
            dt = tn - t  # negative
            if kind == "sde":
                x = x + drift(x, t, 1.0) * dt + math.sqrt(vp_linear(t)[2] * (-dt)) * gg.normal(size=x.shape)
            else:  # Heun
                d1 = drift(x, t, 0.5)
                xe = x + d1 * dt
                x = x + 0.5 * (d1 + drift(xe, tn, 0.5)) * dt
            if i + 1 in at:
                snaps[at[i + 1]] = x.copy()
            if (i + 1) % (N // 50) == 0:
                paths.append(x[:40].copy())
        return x, snaps, np.array(paths)

    out = dict(snap_t=snap_t, n=n)
    for kind in ("sde", "ode"):
        x, snaps, paths = run(kind)
        out[f"{kind}_final"], out[f"{kind}_paths"] = x[:1500], paths
        out[f"{kind}_snaps"] = np.array([snaps[t][:600] for t in snap_t])
        out[f"{kind}_sw"] = [sw(snaps[t], direct(t, n, 30 + k)) for k, t in enumerate(snap_t)]
    out["floor_sw"] = [sw(direct(t, n, 60 + k), direct(t, n, 90 + k)) for k, t in enumerate(snap_t)]
    out["sde_ode_sw"] = [sw(np.asarray(out["sde_snaps"])[k], np.asarray(out["ode_snaps"])[k]) for k in range(len(snap_t))]
    # the ODE both ways: data to noise, then back
    x0 = sample(600, 8)
    ts = np.linspace(T1, T0, N_ode + 1)
    x = x0.copy()
    for i in range(N_ode):
        t, tn = ts[i], ts[i + 1]
        dt = tn - t
        d1 = drift(x, t, 0.5)
        xe = x + d1 * dt
        x = x + 0.5 * (d1 + drift(xe, tn, 0.5)) * dt
    enc = x.copy()
    for i in range(N_ode):
        t, tn = ts[::-1][i], ts[::-1][i + 1]
        dt = tn - t
        d1 = drift(x, t, 0.5)
        xe = x + d1 * dt
        x = x + 0.5 * (d1 + drift(xe, tn, 0.5)) * dt
    out["roundtrip_err"] = float(np.linalg.norm(x - x0, axis=1).mean())
    out["roundtrip_enc"], out["roundtrip_x0"] = enc[:300], x0[:300]
    # each path's length: the SDE's wander against the ODE's glide (same start, 50 recorded steps)
    for kind in ("sde", "ode"):
        P = np.asarray(out[f"{kind}_paths"])
        out[f"{kind}_len"] = float(np.linalg.norm(np.diff(P, axis=0), axis=-1).sum(0).mean())
    print("    SDE marginals vs direct: " + " ".join(f"{v:.3f}" for v in out["sde_sw"]), flush=True)
    print("    ODE marginals vs direct: " + " ".join(f"{v:.3f}" for v in out["ode_sw"]), flush=True)
    print("    floor:                   " + " ".join(f"{v:.3f}" for v in out["floor_sw"]), flush=True)
    print(f"    ODE there and back: mean error {out['roundtrip_err']:.2e}", flush=True)
    return out


def direct(t, n, seed):
    """Samples of the noised data at time t of the linear VP SDE, drawn directly."""
    a, s, _ = vp_linear(t)
    return a * sample(n, seed) + s * rng(seed + 500).normal(size=(n, 2))


# ---------------------------------------------------------------------------
# Samplers in EDM's coordinates: x = x0 + s n, s from SMAX down to SMIN.  The VP state is x / sqrt(1 + s^2).
SMAX, SMIN = 80.0, 0.002


def sigmas(kind, n):
    """n + 1 noise levels from SMAX to SMIN."""
    i = np.arange(n + 1) / n
    if kind == "edm":  # Karras et al.: rho = 7
        r = 7.0
        return (SMAX ** (1 / r) + i * (SMIN ** (1 / r) - SMAX ** (1 / r))) ** r
    if kind == "logsnr":  # uniform in log sigma (= uniform in log-SNR)
        return np.exp(np.log(SMAX) + i * (np.log(SMIN) - np.log(SMAX)))
    if kind == "time":  # uniform in t of the cosine schedule, sigma = tan(pi t / 2)
        t0, t1 = 2 / np.pi * np.arctan(SMAX), 2 / np.pi * np.arctan(SMIN)
        return np.tan(np.pi / 2 * (t0 + i * (t1 - t0)))
    if kind == "ddpm":  # DDPM's linear-beta steps: uniform in its step index, within [SMIN, SMAX]
        beta, abar = ddpm_schedule()
        s_all = np.sqrt((1 - abar) / abar)
        lo, hi = np.searchsorted(s_all, SMIN), min(np.searchsorted(s_all, SMAX), len(s_all) - 1)
        idx = np.round(hi + i * (lo - hi)).astype(int)
        s = s_all[idx]
        s[0], s[-1] = min(SMAX, s_all[hi]), SMIN
        return s
    raise ValueError(kind)


def solve(D, z, kind, n, spacing="edm", seed=0):
    """Sample with denoiser D(x, s) from x = SMAX z.  Returns (x at SMIN, network evaluations)."""
    s = sigmas(spacing, n)
    x = SMAX * z if kind != "euler_vp" else z.copy()
    nfe = 0
    if kind in ("ddim", "euler_s"):  # Euler in s on dx/ds = (x - D)/s: the same as DDIM, and as DPM-Solver-1
        for i in range(n):
            d = D(x, s[i])
            nfe += 1
            x = (s[i + 1] / s[i]) * x + (1 - s[i + 1] / s[i]) * d
        return x, nfe
    if kind == "heun":  # EDM's Algorithm 1 (deterministic)
        for i in range(n):
            d = D(x, s[i])
            nfe += 1
            k1 = (x - d) / s[i]
            xe = x + (s[i + 1] - s[i]) * k1
            if i < n - 1 or s[i + 1] > 0:
                d2 = D(xe, s[i + 1])
                nfe += 1
                x = x + (s[i + 1] - s[i]) * 0.5 * (k1 + (xe - d2) / s[i + 1])
            else:
                x = xe
        return x, nfe
    if kind == "dpm2":  # DPM-Solver-2 (singlestep, data prediction): a half step in log-SNR, then the full step
        for i in range(n):
            d = D(x, s[i])
            sm = math.sqrt(s[i] * s[i + 1])  # the midpoint in lambda = -log s
            xm = (sm / s[i]) * x + (1 - sm / s[i]) * d
            dm = D(xm, sm)
            nfe += 2
            x = (s[i + 1] / s[i]) * x + (1 - s[i + 1] / s[i]) * dm
        return x, nfe
    if kind == "dpmpp2m":  # DPM-Solver++(2M): multistep, one evaluation a step
        prev = None
        for i in range(n):
            d = D(x, s[i])
            nfe += 1
            h = math.log(s[i] / s[i + 1])
            if prev is None:
                de = d
            else:
                r = prev[1] / h
                de = (1 + 1 / (2 * r)) * d - (1 / (2 * r)) * prev[0]
            x = (s[i + 1] / s[i]) * x + (1 - s[i + 1] / s[i]) * de
            prev = (d, h)
        return x, nfe
    if kind == "euler_vp":  # Euler in t on the VP probability-flow ODE (cosine schedule): the naive discretization
        t = 2 / np.pi * np.arctan(s)
        for i in range(n):
            a, sg = math.cos(np.pi * t[i] / 2), math.sin(np.pi * t[i] / 2)
            d = D(x / a, sg / a)
            nfe += 1
            score = (a * d - x) / (sg * sg)
            f, g2 = -np.pi / 2 * math.tan(np.pi * t[i] / 2), np.pi * math.tan(np.pi * t[i] / 2)
            x = x + (t[i + 1] - t[i]) * (f * x - 0.5 * g2 * score)
        a = math.cos(np.pi * t[-1] / 2)
        return x / a, nfe
    if kind == "ddpm":  # ancestral sampling (stochastic): the posterior q(x_{t-1} | x_t, x0 = D)
        g = rng(seed)
        for i in range(n):
            d = D(x, s[i])
            nfe += 1
            s2, sn2 = s[i] ** 2, s[i + 1] ** 2
            mean = (sn2 / s2) * x + (1 - sn2 / s2) * d
            var = sn2 * (s2 - sn2) / s2
            x = mean + (math.sqrt(var) * g.normal(size=x.shape) if i < n - 1 else 0)
        return x, nfe
    raise ValueError(kind)


SOLVERS = [("euler_vp", "time"), ("ddim", "edm"), ("heun", "edm"), ("dpm2", "edm"), ("dpmpp2m", "edm"), ("ddpm", "edm")]
NFES = [4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128]


def solver_sweep(D, z, ref, data_ref, label=""):
    """Every solver at budgets of about NFES network evaluations: the error against the reference solution (the
    deterministic ones) and the distance from the data (all of them)."""
    out = {}
    for kind, spacing in SOLVERS:
        rows = []
        for budget in NFES:
            if kind in ("heun",):
                n = max(1, (budget + 1) // 2)
            elif kind == "dpm2":
                n = max(1, budget // 2)
            else:
                n = budget
            x, nfe = solve(D, z, kind, n, spacing, seed=budget)
            rows.append(dict(nfe=nfe, err=float(np.linalg.norm(x - ref, axis=1).mean()), sw=sw(x, data_ref)))
        out[kind] = rows
        print(f"    {label}{kind:9s} " + " ".join(f"{r['nfe']}:{r['err']:.3f}/{r['sw']:.3f}" for r in rows), flush=True)
    return out


def compute_solvers():
    n = 2000
    z = rng(2022).normal(size=(n, 2))  # Karras et al.; Lu et al.
    ref, _ = solve(denoise_edm, z, "dpm2", 1024, "edm")
    ref2, _ = solve(denoise_edm, z, "heun", 1024, "edm")
    out = dict(ref_gap=float(np.linalg.norm(ref - ref2, axis=1).mean()), nfes=NFES, solvers=[k for k, _ in SOLVERS])
    data_ref = sample(n, 11)
    out["ref_sw"] = sw(ref, data_ref)
    out["floor"] = sw(sample(n, 12), data_ref)
    out.update(solver_sweep(denoise_edm, z, ref, data_ref))
    # the time steps of each, for the picture: the first 12 noise levels of each spacing at 12 steps
    for sp in ("edm", "logsnr", "time", "ddpm"):
        out[f"steps_{sp}"] = sigmas(sp, 12)
    # one sampler's points after 6, 12 and 24 evaluations (for the picture): DDIM, Heun, DPM-Solver++(2M)
    for kind in ("ddim", "heun", "dpmpp2m", "euler_vp"):
        for budget in (6, 12, 24):
            n_ = (budget + 1) // 2 if kind == "heun" else budget
            out[f"pic_{kind}{budget}"] = solve(denoise_edm, z[:600], kind, n_, "time" if kind == "euler_vp" else "edm")[0]
    out["pic_ref"] = ref[:600]
    print(f"    reference: two solvers at 1,024 steps differ by {out['ref_gap']:.1e}; its distance from the data "
          f"{out['ref_sw']:.4f}, floor {out['floor']:.4f}", flush=True)
    return out


# ---------------------------------------------------------------------------
def compute_schedules():
    out = {}
    t = np.linspace(0.0005, 0.9995, 400)
    beta, abar = ddpm_schedule()
    ti = np.arange(1, 1001) / 1000
    out["t"] = t
    out["logsnr_ddpm"] = np.interp(t, ti, np.log(abar / (1 - abar)))
    sc = 0.008
    f = np.cos((t + sc) / (1 + sc) * np.pi / 2) ** 2 / math.cos(sc / (1 + sc) * np.pi / 2) ** 2
    out["logsnr_cosine"] = np.log(f / (1 - f))
    out["logsnr_trig"] = 2 * np.log(1 / np.tan(np.pi * t / 2))  # ours: alpha = cos, sigma = sin
    a, s_, _ = vp_linear(t)
    out["logsnr_vpsde"] = np.log(a * a / (s_ * s_))
    out["logsnr_fm"] = 2 * np.log((1 - t) / t)  # flow matching's straight line, in diffusion time (t = 1: noise)
    # where training spends its noise levels: the density of log-SNR when t is uniform (and EDM's log-normal sigma)
    bins = np.linspace(-14, 14, 57)
    tt = rng(3).uniform(0, 1, 400_000)
    tt = np.clip(tt, 1e-4, 1 - 1e-4)
    dens = {}
    dens["ddpm"] = np.log(abar / (1 - abar))[rng(4).integers(0, 1000, 400_000)]
    dens["trig"] = 2 * np.log(1 / np.tan(np.pi * tt / 2))
    dens["fm"] = 2 * np.log((1 - tt) / tt)
    sd =float(np.sqrt(sample(20000, 13).var(0).mean()))
    ln_s = rng(5).normal(-1.2 + math.log(sd / 0.5), 1.2, 400_000)  # EDM's P_mean, P_std, rescaled to our data
    dens["edm"] = -2 * ln_s
    out["bins"] = bins
    for k, v in dens.items():
        h, _ = np.histogram(v, bins)
        out[f"dens_{k}"] = h / h.sum() / (bins[1] - bins[0])
    out["abar_T"], out["snr_T"] = float(abar[-1]), float(abar[-1] / (1 - abar[-1]))
    out["logsnr_T"] = float(np.log(abar[-1] / (1 - abar[-1])))
    # DDIM with four spacings of the same 3 to 128 steps, exact denoiser: error against the reference
    n = 2000
    z = rng(2022).normal(size=(n, 2))
    ref, _ = solve(denoise_edm, z, "dpm2", 1024, "edm")
    out["spacings"] = ["time", "ddpm", "logsnr", "edm"]
    out["steps"] = [4, 6, 8, 12, 16, 24, 32, 48, 64, 128]
    for sp in out["spacings"]:
        out[f"err_{sp}"] = [float(np.linalg.norm(solve(denoise_edm, z, "ddim", k, sp)[0] - ref, axis=1).mean())
                            for k in out["steps"]]
        print(f"    DDIM, {sp:6s} spacing: " + " ".join(f"{e:.3f}" for e in out[f"err_{sp}"]), flush=True)
    out["sigma_data"] = sd
    return out


# ---------------------------------------------------------------------------
def compute_edmtargets():
    """For x = x0 + s n on our data: how big each regression target is, and how much the network's error is
    magnified in the denoised guess, for predicting x0, predicting the noise, and EDM's mixed target F."""
    x0 = sample(20000, 14)
    n = rng(15).normal(size=x0.shape)
    sd = float(np.sqrt(x0.var(0).mean()))
    ss = np.exp(np.linspace(np.log(0.002), np.log(80), 40))
    rows = dict(s=ss, sd=sd)
    keys = ("in_raw", "in_edm", "tgt_x0", "tgt_eps", "tgt_F", "amp_x0", "amp_eps", "amp_F", "irreducible")
    for k in keys:
        rows[k] = []
    for s in ss:
        x = x0 + s * n
        c_skip = sd * sd / (s * s + sd * sd)
        c_out = s * sd / math.sqrt(s * s + sd * sd)
        c_in = 1 / math.sqrt(s * s + sd * sd)
        F = (x0 - c_skip * x) / c_out
        Dst = denoise_edm(x[:4000], s)
        rows["in_raw"].append(float(x.std(0).mean()))
        rows["in_edm"].append(float((c_in * x).std(0).mean()))
        rows["tgt_x0"].append(float(x0.std(0).mean()))
        rows["tgt_eps"].append(float(n.std(0).mean()))
        rows["tgt_F"].append(float(F.std(0).mean()))
        rows["amp_x0"].append(1.0)  # an error e in the predicted x0 is an error e in D
        rows["amp_eps"].append(float(s))  # D = x - s eps: an error e in eps is s e in D
        rows["amp_F"].append(float(c_out))  # D = c_skip x + c_out F
        rows["irreducible"].append(float(((Dst - x0[:4000]) ** 2).mean()))  # the best possible loss on D, per number
    print(f"    sigma_data {sd:.3f}; F's spread from {min(rows['tgt_F']):.3f} to {max(rows['tgt_F']):.3f}", flush=True)
    return rows


# ---------------------------------------------------------------------------
def fm_velocity(x, tau):
    """Flow matching's marginal velocity for the straight path x = (1 - tau) z + tau x1 (z: noise, x1: data):
    v = E[x1 - z | x] = (E[x1 | x] - x) / (1 - tau)."""
    x1hat = posterior(x, tau, 1 - tau)[0]
    return (x1hat - x) / (1 - tau)


def trig_velocity(x, tau):
    """The diffusion path as an interpolant: x = cos(pi tau / 2) z + sin(pi tau / 2) x1 (tau = 1 - t)."""
    c, s = math.cos(np.pi * tau / 2), math.sin(np.pi * tau / 2)
    x1hat = posterior(x, s, c)[0]
    zhat = (x - s * x1hat) / c
    return np.pi / 2 * (c * x1hat - s * zhat)


def integrate(vel, z, n=400, tau_end=1 - 1e-4, keep_every=10):
    """RK4 from tau = 0 to tau_end; the path every keep_every steps; the kinetic energy int E|v|^2 dtau."""
    taus = np.linspace(0, tau_end, n + 1)
    x = z.copy()
    path, energy = [x.copy()], 0.0
    for i in range(n):
        t, h = taus[i], taus[i + 1] - taus[i]
        k1 = vel(x, t)
        k2 = vel(x + 0.5 * h * k1, t + 0.5 * h)
        k3 = vel(x + 0.5 * h * k2, t + 0.5 * h)
        k4 = vel(x + h * k3, t + h)
        energy += h * float(((k1 ** 2).sum(1).mean() + 2 * (k2 ** 2).sum(1).mean() + 2 * (k3 ** 2).sum(1).mean()
                             + (k4 ** 2).sum(1).mean()) / 6)
        x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if (i + 1) % keep_every == 0:
            path.append(x.copy())
    return x, np.array(path), energy


def straightness(P):
    seg = np.linalg.norm(np.diff(P, axis=0), axis=-1).sum(0)
    return float((np.linalg.norm(P[-1] - P[0], axis=-1) / np.maximum(seg, 1e-9)).mean())


def compute_transport():
    from scipy.optimize import linear_sum_assignment

    n = 1500
    z = rng(1781).normal(size=(n, 2))  # Monge, 1781
    out = dict(n=n)
    x_fm, P_fm, A_fm = integrate(fm_velocity, z)
    x_tr, P_tr, A_tr = integrate(trig_velocity, z)
    out["fm_paths"], out["trig_paths"] = P_fm[:, :300], P_tr[:, :300]
    out["straight_fm"], out["straight_trig"] = straightness(P_fm), straightness(P_tr)
    out["action_fm"], out["action_trig"] = A_fm, A_tr
    out["cost_fm"] = float(((x_fm - z) ** 2).sum(1).mean())
    out["cost_trig"] = float(((x_tr - z) ** 2).sum(1).mean())
    data = sample(n, 21)
    out["cost_indep"] = float(((data - z) ** 2).sum(1).mean())
    # the optimal coupling between these n noise points and n data points (the Hungarian algorithm)
    Cm = ((z[:, None] - data[None]) ** 2).sum(-1)
    r, c = linear_sum_assignment(Cm)
    out["cost_ot"] = float(Cm[r, c].mean())
    out["ot_z"], out["ot_x"] = z[r][:300], data[c][:300]
    # and between the noise and where the flow takes it: the flow's own map, re-paired optimally
    Cm2 = ((z[:, None] - x_fm[None]) ** 2).sum(-1)
    r2, c2 = linear_sum_assignment(Cm2)
    out["cost_ot_fm"] = float(Cm2[r2, c2].mean())
    out["sw_fm_end"], out["sw_trig_end"] = sw(x_fm, data), sw(x_tr, data)
    # the marginal-field theorem: following E[x1 - z | x] keeps the particles distributed exactly as the
    # interpolation (1 - tau) z + tau x1 of independent pairs, at every tau
    taus = [0.25, 0.5, 0.75, 1.0]
    rows = []
    for k, tau in enumerate(taus):
        idx = int(round(tau * (len(P_fm) - 1)))
        tau_ = min(tau, 1 - 1e-4)
        d1 = (1 - tau_) * rng(40 + k).normal(size=(n, 2)) + tau_ * sample(n, 50 + k)
        d2 = (1 - tau_) * rng(60 + k).normal(size=(n, 2)) + tau_ * sample(n, 70 + k)
        rows.append(dict(tau=tau, sw_flow=sw(P_fm[idx], d1), sw_floor=sw(d2, d1)))
        out[f"direct{tau:g}"] = d1[:600]
        out[f"flow{tau:g}"] = P_fm[idx][:600]
    out["marginal_rows"] = rows
    # the conditional paths: straight, and crossing (40 random noise-data pairs)
    out["cond_z"], out["cond_x"] = z[:40], sample(40, 22)
    # the field itself at four times, on a grid
    gx, gy = np.meshgrid(np.linspace(-3, 3, 25), np.linspace(-2, 2, 17))
    G = np.stack([gx.ravel(), gy.ravel()], 1)
    out["grid"] = G
    out["field_taus"] = [0.2, 0.5, 0.8, 0.95]
    for tau in out["field_taus"]:
        out[f"field{tau:g}"] = fm_velocity(G, tau)
    print(f"    straightness: flow matching {out['straight_fm']:.3f}, diffusion path {out['straight_trig']:.3f}", flush=True)
    print(f"    cost: independent pairs {out['cost_indep']:.3f}; flow {out['cost_fm']:.3f} (action {A_fm:.3f}); "
          f"diffusion ODE {out['cost_trig']:.3f} (action {A_tr:.3f}); optimal {out['cost_ot']:.3f}", flush=True)
    for r_ in rows:
        print("    tau={tau}: flow vs interpolation {sw_flow:.4f}, floor {sw_floor:.4f}".format(**r_), flush=True)
    return out
