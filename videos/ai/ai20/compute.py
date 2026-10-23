"""Precompute everything numerical in Part 20 of the AI series ("Four Ways to Generate").

    python -m videos.ai.ai20.compute                 # everything missing (MNIST through Part 10's download)
    python -m videos.ai.ai20.compute --force gan2d

Results are cached in ``.cache/ai20/<name>.json`` (+ ``.npz``); trained weights in ``.cache/ai20/models/``; scenes
call ``load(name)``. Every model is trained here, on the CPU, one torch thread, seeded. The items made of several runs
save each run as it finishes (``CACHE.partial``), so a killed computation resumes. About two hours on a busy 4-core
machine, all told; the longest items are the digit models (``pixelcnn``, ``vae``, ``gan``, ``wgan``, ``flow``: three
seeds each, a few minutes a seed).

The 2D items (gen2d.py: two moons, a ring of eight Gaussians, a checkerboard):
    toys        the three densities: samples, exact density images, entropies (the best possible NLL)
    ar2d        the autoregressive model p(x1) p(x2 | x1) (mixtures of ten Gaussians): training replay, the
                conditional slices, samples; three seeds on the ring
    vae2d       a VAE with a 2D code: replay, samples, where the ring's points land in the code; three seeds on the ring
    collapse2d  posterior collapse: the same VAE with a factorized decoder and with an autoregressive one, KL over
                training, three seeds each
    gan2d       the ring: the minimax loss, the non-saturating loss and WGAN-GP, five seeds each (same networks, same
                generator steps), modes covered over training; seed 0 replayed (samples and the discriminator); the
                generator's gradient early on; moons and checkerboard, seed 0
    bilinear    the game min_x max_y xy: simultaneous, alternating, extragradient and optimistic gradient steps;
                Mescheder's Dirac-GAN with and without the R1 penalty
    jsw         Arjovsky's parallel lines: Jensen-Shannon (from a trained discriminator) and Wasserstein-1 (from a
                trained critic) against the offset theta, with the exact values
    flow2d      RealNVP, eight affine couplings: replay, the plane warped layer by layer, log-det checked against
                autograd; three seeds on the ring
    cnf         a continuous normalizing flow on the moons: exact divergence vs Hutchinson's estimator, three seeds
                each; particle paths; Hutchinson's variance (Gaussian vs Rademacher probes) against the formulas;
                exact vs estimated trace in 196 dimensions
    ebm2d       an energy-based model trained with Langevin chains: replay, Langevin from noise, long-run samples
    langevin    Langevin on an exactly known two-Gaussian mixture (weights 0.2 / 0.8): plain vs annealed over noise
                levels (Song & Ermon 2019)
    hopfield    Hopfield's network: capacity on random patterns (N = 196), digits recalled by Hebb's rule and by a
                modern (softmax) Hopfield network
    eval2d      every 2D family on the ring, three seeds: modes covered, precision and recall, the Frechet distance,
                NLL; a Gaussian blob with the ring's mean and covariance

The digit items (gendigits.py: MNIST at 14 x 14, 16 grey levels; every family on BUDGET training FLOPs):
    classifier  the judge: a small CNN (its 128-d penultimate layer gives the features); FID of real digits against
                the sample size, and against noise and blur
    pixelcnn    PixelCNN, three seeds: replay (test NLL, samples), receptive fields of the plain and two-stack
                layouts, one digit drawn pixel by pixel with its predictions
    vae         the VAE (16-d code), three seeds: the ELBO's two terms over training, samples, active units
    vae_map     a VAE with a 2-d code: the test digits' codes over training, the decoded grid
    beta        the beta-VAE sweep (beta = 0.25 ... 8, two seeds): rate, distortion, active units, samples
    collapse    a VAE whose decoder is a PixelCNN: KL over training, plain and with free bits
    gan         the non-saturating GAN, three seeds: replay, samples
    wgan        WGAN-GP, three seeds
    flow        RealNVP on the dequantized digits, three seeds
    rbm         restricted Boltzmann machines (16 hidden units, so log Z is summed exactly): CD-1, CD-10 and PCD, three
                seeds; a 100-unit RBM's filters and Gibbs chains
    vq          a VQ-VAE (49 codes from 32) and a small transformer over its codes: the two-stage recipe
    evaluate    the families side by side: FID, precision, recall, bits per pixel, sampling cost; the truncation
                trick and GAN inversion; nearest training digits (memorization)
"""

from __future__ import annotations

import math
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from explainer.ai.cache import Cache
from videos.ai.ai20 import gen2d as g2
from videos.ai.ai20 import gendigits as gd

CACHE = Cache("ai20")
if g2.SCALE != 1.0:  # a quick smoke test of every code path (AI20_SCALE=0.01): its own cache, never the real one
    CACHE.dir = CACHE.dir.parent / "ai20_quick"
load = CACHE.load
MODELS = CACHE.dir / "models"
SEEDS = (0, 1, 2)


def _threads():
    torch.set_num_threads(int(os.environ.get("AI20_THREADS", "1")))


def tolist(x):
    """numpy (nested in dicts and lists) to plain JSON values, floats rounded to 6 significant digits."""
    if isinstance(x, dict):
        return {k: tolist(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [tolist(v) for v in x]
    if isinstance(x, np.ndarray):
        if x.dtype.kind in "iub":
            return x.tolist()
        return np.round(x.astype(np.float64), 6).tolist()
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, torch.Tensor):
        return tolist(x.detach().numpy())
    return x


def log(msg: str) -> None:
    print(f"    {time.strftime('%H:%M:%S')} {msg}", flush=True)


def save_model(m: nn.Module, name: str) -> None:
    MODELS.mkdir(parents=True, exist_ok=True)
    tmp = MODELS / f"{name}.tmp.pt"
    torch.save(m.state_dict(), tmp)
    tmp.replace(MODELS / f"{name}.pt")


def load_model(m: nn.Module, name: str, item: str) -> nn.Module:
    p = MODELS / f"{name}.pt"
    if not p.exists():  # the item's json without its weights (deleted by hand): train it again
        CACHE.save(item, CACHE.items[item]() if CACHE.items else ITEMS[item]())
    m.load_state_dict(torch.load(p))
    m.eval()
    return m


# ===========================================================================
# 2D
# ===========================================================================
def compute_toys():
    out = {}
    xs, P = g2.grid_points()
    for n in g2.NAMES:
        Xtr, Xte = g2.dataset(n)
        out[f"{n}_samples"] = Xtr[:2000]
        out[f"{n}_density"] = g2.density(n, P).reshape(g2.GRID, g2.GRID).astype(np.float32)
        out[f"{n}_entropy"] = g2.entropy(n)
    out.update(grid=xs, box=g2.BOX, ring_centers=g2.RING_C, ring_sigma=g2.RING_S, n_train=g2.N_TRAIN,
               n_test=g2.N_TEST, names=g2.NAMES)
    return out


def _samples(m, n=2000, seed=99):
    return m.sample(n, torch.Generator().manual_seed(seed)).numpy().astype(np.float32)


def compute_ar2d():
    _threads()
    out = {}
    for n in g2.NAMES:
        m, r = g2.train_ar(n, 0)
        out[f"{n}_curve"] = np.array(r["curve"])
        out[f"{n}_frames"] = np.array([f["dens"] for f in r["frames"]])
        out[f"{n}_frame_steps"] = [f["step"] for f in r["frames"]]
        out[f"{n}_s0"] = _samples(m)
        xs = np.linspace(-g2.BOX, g2.BOX, 241)
        out[f"{n}_x1"] = m.marginal1(xs).astype(np.float32)
        cuts = {"moons": [-1.6, 0.0, 1.6], "ring": [-2.0, 0.0, 1.41], "checker": [-1.5, -0.5, 0.5]}[n]
        out[f"{n}_cuts"] = cuts
        out[f"{n}_cond"] = np.array([m.conditional(c, xs) for c in cuts], np.float32)
        out["params"] = r["params"]
        log(f"ar2d {n}: test NLL {r['curve'][-1][1]:.3f}")
    out["xs"] = np.linspace(-g2.BOX, g2.BOX, 241)
    for s in SEEDS[1:]:
        m, r = g2.train_ar("ring", s, snaps=False)
        out[f"ring_s{s}"] = _samples(m)
        out[f"ring_nll_s{s}"] = r["curve"][-1][1]
    out["ring_nll_s0"] = float(out["ring_curve"][-1][1])
    return out


def compute_vae2d():
    _threads()
    out = {}
    for n in g2.NAMES:
        m, r = g2.train_vae(n, 0)
        out[f"{n}_curve"] = np.array(r["curve"])
        out[f"{n}_frames"] = np.array([f["dens"] for f in r["frames"]])
        out[f"{n}_frame_steps"] = [f["step"] for f in r["frames"]]
        out[f"{n}_s0"] = _samples(m)
        if n == "ring":  # where the data lands in the code, and where the code's grid lands in the data
            _, Xte = g2.dataset(n)
            with torch.no_grad():
                mu, _ = m.enc(torch.from_numpy(Xte[:1500])).chunk(2, -1)
                zs = np.linspace(-2.5, 2.5, 21)
                Z = torch.as_tensor(np.array([[a, b] for b in zs for a in zs]), dtype=torch.float32)
                dm, _ = m.decode(Z)
            out["ring_codes"] = mu.numpy()
            d = np.sqrt(((Xte[:1500, None, :] - g2.RING_C[None]) ** 2).sum(-1))
            out["ring_code_mode"] = d.argmin(1)
            out["ring_zgrid"] = zs
            out["ring_decoded"] = dm.numpy().reshape(21, 21, 2)
            with torch.no_grad():
                out["ring_nll_iw_s0"] = float(-m.log_prob(torch.from_numpy(Xte[:2000]), 128,
                                                          torch.Generator().manual_seed(5)).mean())
        out["params"] = r["params"]
        log(f"vae2d {n}: -ELBO {r['curve'][-1][1]:.3f}")
    _, Xte = g2.dataset("ring")
    for s in SEEDS[1:]:
        m, r = g2.train_vae("ring", s, snaps=False)
        out[f"ring_s{s}"] = _samples(m)
        with torch.no_grad():
            out[f"ring_nll_iw_s{s}"] = float(-m.log_prob(torch.from_numpy(Xte[:2000]), 128,
                                                          torch.Generator().manual_seed(5)).mean())
    return out


def compute_collapse2d():
    _threads()
    out = {}
    for ar in (False, True):
        tag = "ar" if ar else "fact"
        for s in SEEDS:
            r = g2.train_collapse(ar, s)
            out[f"{tag}_s{s}_curve"] = np.array(r["curve"])
            if s == 0:
                out[f"{tag}_codes"], out[f"{tag}_points"] = r["codes"], r["points"]
            out[f"{tag}_params"] = r["params"]
            log(f"collapse2d {tag} s{s}: KL {r['curve'][-1][3]:.3f}, -ELBO {r['curve'][-1][1]:.3f}")
    return out


def compute_gan2d():
    _threads()
    part = CACHE.partial("gan2d", dict(v=2, steps=6000))
    for loss in ("mm", "ns", "wgan"):
        for s in range(5):
            key = f"{loss}_s{s}"
            if key in part:
                continue
            t = time.time()
            G, r = g2.train_gan(loss, "ring", s, replay=(s == 0))
            part[key] = tolist(dict(curve=r["curve"], frames=r["frames"], final=r["final"], gnorm=r["gnorm"],
                                    params=r["params"]))
            log(f"gan2d {key}: modes {r['curve'][-1][1]}, quality {r['curve'][-1][2]:.2f} ({time.time() - t:.0f}s)")
    for loss in ("ns", "wgan"):
        for n in ("moons", "checker"):
            key = f"{loss}_{n}"
            if key not in part:
                G, r = g2.train_gan(loss, n, 0)
                part[key] = tolist(dict(final=r["final"]))
                log(f"gan2d {key}")
    out = {}
    for loss in ("mm", "ns", "wgan"):
        for s in range(5):
            p = part[f"{loss}_s{s}"]
            out[f"{loss}_s{s}_curve"] = np.array(p["curve"], float)
            out[f"ring_{loss}_s{s}"] = np.array(p["final"], np.float32)
            if s == 0:
                fr = p["frames"]
                out[f"{loss}_frame_steps"] = [f["step"] for f in fr]
                out[f"{loss}_frame_samples"] = np.array([f["samples"] for f in fr], np.float32)
                out[f"{loss}_frame_d"] = np.array([f["d"] for f in fr], np.float32)
                out[f"{loss}_frame_modes"] = [f["modes"] for f in fr]
                out[f"{loss}_frame_counts"] = [f["counts"] for f in fr]
                out[f"{loss}_gnorm"] = np.array(p["gnorm"], float)
        out["params"] = p["params"]
        out[f"{loss}_final_modes"] = [g2.modes(out[f"ring_{loss}_s{s}"])[0] for s in range(5)]
        out[f"{loss}_final_quality"] = [g2.modes(out[f"ring_{loss}_s{s}"])[1] for s in range(5)]
    for loss in ("ns", "wgan"):
        for n in ("moons", "checker"):
            out[f"{n}_{loss}_s0"] = np.array(part[f"{loss}_{n}"]["final"], np.float32)
    out["grid40"] = np.linspace(-g2.BOX, g2.BOX, 40)
    out["steps"], out["z_dim"], out["n_critic"] = 6000, g2.ZD, 5
    return out


def compute_gan2d_collapse():
    """The non-saturating GAN seed that ends with the fewest of the ring's modes, trained again (bit for bit the same
    run: the replay draws no random numbers) with its checkpoints recorded, to show collapse as it happens."""
    _threads()
    g = load("gan2d")
    fin = list(g["ns_final_modes"])
    seed = int(np.argmin(fin))
    G, r = g2.train_gan("ns", "ring", seed, replay=True)
    assert g2.modes(r["final"])[0] == fin[seed]  # the same run as in gan2d
    fr = r["frames"]
    return dict(seed=seed, n_seeds=len(fin), n_collapsed=int(sum(1 for m in fin if m < 8)), final_modes=fin,
                frame_steps=[f["step"] for f in fr], frame_samples=np.array([f["samples"] for f in fr], np.float32),
                frame_d=np.array([f["d"] for f in fr], np.float32), frame_modes=[f["modes"] for f in fr],
                frame_counts=[f["counts"] for f in fr])


def compute_bilinear():
    eta, T = 0.2, 60
    p0 = np.array([1.0, 0.0])

    def sim(p):
        x, y = p
        return np.array([x - eta * y, y + eta * x])

    def alt(p):
        x, y = p
        x = x - eta * y
        return np.array([x, y + eta * x])

    def extra(p):
        x, y = p
        xh, yh = x - eta * y, y + eta * x  # look ahead, then step with the look-ahead's gradient
        return np.array([x - eta * yh, y + eta * xh])

    prev = {"g": np.array([0.0, 1.0])}

    def opt(p, g_prev):
        x, y = p
        gx, gy = y, -x  # descent direction for x is -y; ascent for y is +x: g = (d/dx, -d/dy) of xy
        return np.array([x - eta * (2 * gx - g_prev[0]), y - eta * (2 * gy - g_prev[1])]), np.array([gx, gy])

    out = {"eta": eta, "steps": T}
    for name, step in (("sim", sim), ("alt", alt), ("extra", extra)):
        P = [p0]
        for _ in range(T):
            P.append(step(P[-1]))
        out[name] = np.array(P)
    P, gp = [p0], np.array([p0[1], -p0[0]])
    for _ in range(T):
        p, gp = opt(P[-1], gp)
        P.append(p)
    out["opt"] = np.array(P)
    out["sim_radius_theory"] = np.sqrt(1 + eta ** 2) ** np.arange(T + 1)
    for k in ("sim", "alt", "extra", "opt"):
        out[f"{k}_radius"] = np.linalg.norm(out[k], axis=1)
    assert np.allclose(out["sim_radius"], out["sim_radius_theory"])  # |1 + i eta|^t, exactly
    # the field itself, for the arrows: (dx/dt, dy/dt) = (-y, x)
    gs = np.linspace(-1.6, 1.6, 9)
    out["field_pts"] = np.array([[a, b] for a in gs for b in gs])
    out["field_vec"] = np.array([[-b, a] for a in gs for b in gs])
    # Mescheder, Geiger & Nowozin (2018): the Dirac-GAN. Data at 0, generator at theta, D(x) = psi x,
    # L = f(psi theta) + f(0), f(t) = -log(1 + e^{-t}); simultaneous steps, with and without R1 (gamma/2 psi^2)
    fp = lambda t: 1 / (1 + np.exp(t))  # f'(t)

    def dirac(gamma, alt_=False, h=0.1, n=300):
        th, ps = 1.0, 1.0
        P = [(th, ps)]
        for _ in range(n):
            d_th = -ps * fp(ps * th)  # the generator descends L: theta' = -dL/dtheta
            if alt_:
                th = th + h * d_th
            d_ps = th * fp(ps * th) - gamma * ps  # the discriminator ascends L - (gamma/2) psi^2
            th = th + h * d_th if not alt_ else th
            ps = ps + h * d_ps
            P.append((th, ps))
        return np.array(P)

    out["dirac_sim"] = dirac(0.0)
    out["dirac_alt"] = dirac(0.0, alt_=True)
    out["dirac_r1"] = dirac(1.0)
    out["dirac_gamma"], out["dirac_h"] = 1.0, 0.1
    out["fprime0"] = float(fp(0.0))
    return out


def compute_jsw():
    """P0: x = 0, y ~ U[0, 1]; P_theta: x = theta.  JS(P0, P_theta) = log 2 for theta != 0, W1 = |theta|."""
    _threads()
    thetas = np.round(np.linspace(-1.0, 1.0, 17), 4)
    js, w = [], []
    for i, th in enumerate(thetas):
        gen = g2.tseed(500 + i)

        def draw(n, t):
            return torch.stack([torch.full((n,), float(t)), torch.rand(n, generator=gen)], 1)

        Dn = g2.mlp(2, 1, 64, act=lambda: nn.LeakyReLU(0.2))
        o = torch.optim.Adam(Dn.parameters(), 2e-3)
        for _ in range(500):
            loss = F.softplus(-Dn(draw(256, 0.0))).mean() + F.softplus(Dn(draw(256, th))).mean()
            o.zero_grad()
            loss.backward()
            o.step()
        with torch.no_grad():
            V = -(F.softplus(-Dn(draw(20000, 0.0))).mean() + F.softplus(Dn(draw(20000, th))).mean())
        js.append(float((V + math.log(4)) / 2))  # V(D*) = 2 JS - log 4
        Cn = g2.mlp(2, 1, 64, act=lambda: nn.LeakyReLU(0.2))
        o = torch.optim.Adam(Cn.parameters(), 1e-3, betas=(0.5, 0.9))
        for _ in range(500):
            r, f = draw(256, 0.0), draw(256, th)
            loss = Cn(f).mean() - Cn(r).mean() + 10 * g2.grad_penalty(Cn, r, f, gen)
            o.zero_grad()
            loss.backward()
            o.step()
        with torch.no_grad():
            w.append(float(Cn(draw(20000, 0.0)).mean() - Cn(draw(20000, th)).mean()))
    return dict(thetas=thetas, js=np.array(js), w=np.array(w), js_exact=math.log(2), w_exact=np.abs(thetas))


def compute_flow2d():
    _threads()
    out = {}
    for n in g2.NAMES:
        m, r = g2.train_flow(n, 0)
        out[f"{n}_curve"] = np.array(r["curve"])
        out[f"{n}_frames"] = np.array([f["dens"] for f in r["frames"]])
        out[f"{n}_frame_steps"] = [f["step"] for f in r["frames"]]
        out[f"{n}_s0"] = _samples(m)
        # the warp: lines of the base plane and Gaussian points, through the inverse layers one by one
        ts = np.linspace(-2.5, 2.5, 121)
        lines = [np.c_[ts, np.full_like(ts, c)] for c in np.linspace(-2.5, 2.5, 11)] + \
                [np.c_[np.full_like(ts, c), ts] for c in np.linspace(-2.5, 2.5, 11)]
        L = torch.as_tensor(np.concatenate(lines), dtype=torch.float32)
        out[f"{n}_warp"] = np.array(m.generate_layers(L), np.float32).reshape(len(m.layers) + 1, 22, 121, 2)
        zpts = torch.randn(800, 2, generator=torch.Generator().manual_seed(7))
        out[f"{n}_warp_pts"] = np.array(m.generate_layers(zpts), np.float32)
        out[f"{n}_logdet_gap"] = g2.logdet_check(m, g2.dataset(n)[1][:20])
        assert out[f"{n}_logdet_gap"] < 1e-3  # the sum of the scales IS the log-determinant
        out["params"] = r["params"]
        log(f"flow2d {n}: test NLL {r['curve'][-1][1]:.3f}, logdet gap {out[f'{n}_logdet_gap']:.1e}")
    for s in SEEDS[1:]:
        m, r = g2.train_flow("ring", s, snaps=False)
        out[f"ring_s{s}"] = _samples(m)
        out[f"ring_nll_s{s}"] = r["curve"][-1][1]
    out["ring_nll_s0"] = float(out["ring_curve"][-1][1])
    out["n_layers"] = 8
    return out


def compute_cnf():
    _threads()
    part = CACHE.partial("cnf", dict(v=1, steps=1500))
    for hutch in (False, True):
        for s in SEEDS:
            key = f"{'hutch' if hutch else 'exact'}_s{s}"
            if key in part:
                continue
            t = time.time()
            f, r = g2.train_cnf(s, hutch)
            part[key] = tolist(dict(curve=r["curve"], train=r["train"], params=r["params"], secs=time.time() - t))
            if s == 0:
                save_model(f, f"cnf_{key}")
            log(f"cnf {key}: NLL {r['curve'][-1][1]:.3f} ({time.time() - t:.0f}s)")
    out = {k: np.array(v["curve"], float) for k, v in ((k, part[k]) for k in part.done)}
    out = {f"{k}_curve": v for k, v in out.items()}
    for k in part.done:
        out[f"{k}_train"] = np.array(part[k]["train"], float)
        out[f"{k}_secs"] = part[k]["secs"]
    out["params"] = part["exact_s0"]["params"]
    f = load_model(g2.ODEFunc(), "cnf_exact_s0", "cnf")
    z0 = torch.randn(1500, 2, generator=torch.Generator().manual_seed(11))
    out["paths"] = g2.cnf_paths(f, z0)
    xs, P = g2.grid_points(48)
    Pt = torch.as_tensor(P, dtype=torch.float32)
    dens = []
    for t0 in (0.0, 0.25, 0.5, 0.75, 1.0):
        if t0 == 0:
            lp = g2.normal_lp(Pt, torch.zeros_like(Pt), torch.zeros_like(Pt)).sum(-1)
        else:
            lp = g2.cnf_logp(f, Pt.clone(), max(2, int(round(8 * t0))), False, None, t0=t0, create_graph=False)
        dens.append(lp.detach().exp().numpy().reshape(48, 48))
    out["dens_t"] = np.array(dens, np.float32)
    out["dens_grid"] = xs
    # Hutchinson's variance at the trained field, t = 0.5: measured, and the formulas
    X = torch.from_numpy(g2.dataset("moons")[1][:400])
    with torch.enable_grad():
        Xg = X.clone().requires_grad_(True)
        o = f(Xg, 0.5)
        J = torch.stack([torch.autograd.grad(o[:, i].sum(), Xg, retain_graph=True)[0] for i in range(2)], 1)
    J = J.detach().numpy()  # (n, out i, in j)
    tr = np.trace(J, axis1=1, axis2=2)
    gen = np.random.default_rng(3)
    est = {}
    for kind in ("gauss", "rad"):
        e = gen.normal(size=(4000, 2)) if kind == "gauss" else gen.choice([-1.0, 1.0], size=(4000, 2))
        vals = np.einsum("ki,nij,kj->nk", e, J, e)  # (n points, 4000 probes)
        est[kind] = vals
    A = 0.5 * (J + J.transpose(0, 2, 1))
    fro = (A ** 2).sum((1, 2))
    diag = (np.diagonal(J, axis1=1, axis2=2) ** 2).sum(1)
    out["hv_gauss_measured"] = est["gauss"].var(1)
    out["hv_rad_measured"] = est["rad"].var(1)
    out["hv_gauss_theory"] = 2 * fro
    out["hv_rad_theory"] = 2 * (fro - diag)
    out["hv_mean_err"] = float(np.abs(est["gauss"].mean(1) - tr).max())
    out["hv_example"] = dict(tr=float(tr[0]), gauss=est["gauss"][0, :200], rad=est["rad"][0, :200])
    # in 196 dimensions: the exact trace costs 196 backward passes, Hutchinson's one
    torch.manual_seed(5)
    big = nn.Sequential(nn.Linear(gd.D, 256), nn.Tanh(), nn.Linear(256, gd.D))
    zb = torch.randn(64, gd.D, requires_grad=True)
    t = time.time()
    ob = big(zb)
    ex = sum(torch.autograd.grad(ob[:, i].sum(), zb, retain_graph=True)[0][:, i] for i in range(gd.D))
    t_exact = time.time() - t
    t = time.time()
    hs = []
    for k in range(50):
        e = (torch.randint(0, 2, zb.shape, generator=torch.Generator().manual_seed(k)).float() * 2 - 1)
        gg, = torch.autograd.grad((big(zb) * e).sum(), zb)
        hs.append((gg * e).sum(1))
    t_h = (time.time() - t) / 50
    hs = torch.stack(hs).detach().numpy()
    out["big_dim"] = gd.D
    out["big_exact"] = ex.detach().numpy()
    out["big_hutch_mean"] = hs.mean(0)
    out["big_hutch_sd"] = hs.std(0)
    out["big_time_ratio"] = float(t_exact / t_h)
    out["n_steps"] = 8
    return out


def compute_ebm2d():
    _threads()
    out = {}
    for n in g2.NAMES:
        t = time.time()
        E, r = g2.train_ebm(n, 0)
        out[f"{n}_curve"] = np.array(r["curve"])
        out[f"{n}_frames"] = np.array([f["dens"] for f in r["frames"]])
        out[f"{n}_frame_chains"] = np.array([f["chains"] for f in r["frames"]])
        out[f"{n}_frame_steps"] = [f["step"] for f in r["frames"]]
        gen = torch.Generator().manual_seed(21)
        x0 = (torch.rand(300, 2, generator=gen) * 2 - 1) * g2.BOX
        _, path = g2.langevin(E, x0, 240, 0.005, gen, keep_every=3)
        out[f"{n}_langevin"] = np.array([x0.numpy()] + path, np.float32)
        x0 = (torch.rand(2000, 2, generator=gen) * 2 - 1) * g2.BOX
        xs_, _ = g2.langevin(E, x0, 800, 0.005, gen)
        out[f"{n}_s0"] = xs_.numpy().astype(np.float32)
        xs, P = g2.grid_points()
        with torch.no_grad():
            out[f"{n}_energy"] = E(torch.as_tensor(P, dtype=torch.float32)).numpy().reshape(g2.GRID, g2.GRID)
            gq = np.linspace(-g2.BOX, g2.BOX, 15)
            Q_ = np.array([[a, b] for a in gq for b in gq])
        Qt = torch.as_tensor(Q_, dtype=torch.float32).requires_grad_(True)
        gq_, = torch.autograd.grad(E(Qt).sum(), Qt)
        out[f"{n}_score_pts"], out[f"{n}_score"] = Q_, -gq_.numpy()
        out["params"] = r["params"]
        if n == "ring":
            save_model(E, "ebm_ring_s0")
        log(f"ebm2d {n}: NLL {r['curve'][-1][1]:.3f} ({time.time() - t:.0f}s)")
    for s in SEEDS[1:]:
        E, r = g2.train_ebm("ring", s, snaps=False)
        gen = torch.Generator().manual_seed(21 + s)
        x0 = (torch.rand(2000, 2, generator=gen) * 2 - 1) * g2.BOX
        xs_, _ = g2.langevin(E, x0, 800, 0.005, gen)
        out[f"ring_s{s}"] = xs_.numpy().astype(np.float32)
        out[f"ring_nll_s{s}"] = r["curve"][-1][1]
    out["ring_nll_s0"] = float(out["ring_curve"][-1][1])
    out["k_steps"], out["eta"] = 40, 0.005
    return out


def compute_langevin():
    """Two Gaussians with weights 0.2 and 0.8, whose score is known exactly.  Langevin from uniform noise at one
    noise level, and annealed Langevin through ten (Song & Ermon 2019's toy, scaled to the screen)."""
    mus = np.array([[-1.6, -1.6], [1.6, 1.6]])
    w, sd = np.array([0.2, 0.8]), 0.35
    g = np.random.default_rng(0)

    def score(x, s2):
        d = x[:, None, :] - mus[None]
        lw = np.log(w)[None] - (d ** 2).sum(-1) / (2 * s2)
        r = np.exp(lw - lw.max(1, keepdims=True))
        r /= r.sum(1, keepdims=True)
        return -(r[:, :, None] * d).sum(1) / s2

    n = 2000
    x0 = g.uniform(-3, 3, size=(n, 2))
    x, path = x0.copy(), [x0[:300].copy()]
    eta = 0.004
    for k in range(1000):
        x = x + 0.5 * eta * score(x, sd ** 2) + math.sqrt(eta) * g.normal(size=x.shape)
        if k % 10 == 9:
            path.append(x[:300].copy())
    plain = x
    sig = np.geomspace(2.0, sd, 10)  # noise levels, largest first: the density blurred by N(0, s^2 - sd^2)
    x, apath = x0.copy(), [x0[:300].copy()]
    for s in sig:
        e = eta * (s / sd) ** 2
        for k in range(100):
            x = x + 0.5 * e * score(x, s ** 2) + math.sqrt(e) * g.normal(size=x.shape)
            if k % 10 == 9:
                apath.append(x[:300].copy())
    ann = x

    def share(X):  # the share of samples nearer the heavy mode
        return float((((X - mus[1]) ** 2).sum(1) < ((X - mus[0]) ** 2).sum(1)).mean())

    gs = np.linspace(-3, 3, 13)
    G_ = np.array([[a, b] for a in gs for b in gs])
    return dict(mus=mus, weights=w, sd=sd, plain=plain, annealed=ann, plain_path=np.array(path, np.float32),
                annealed_path=np.array(apath, np.float32), plain_heavy=share(plain), annealed_heavy=share(ann),
                start_heavy=share(x0), sigmas=sig, eta=eta, field_pts=G_, field=score(G_, sd ** 2),
                field_blur=score(G_, sig[0] ** 2))


def compute_hopfield():
    N = 196
    g = np.random.default_rng(0)

    def hebb(P):
        W = P.T @ P / P.shape[1]
        np.fill_diagonal(W, 0)
        return W

    def run(W, s, sweeps=10, rec=None):
        s = s.copy()
        for _ in range(sweeps):
            changed = False
            for i in g.permutation(len(s)):
                v = 1.0 if W[i] @ s >= 0 else -1.0
                if v != s[i]:
                    s[i], changed = v, True
                if rec is not None:
                    rec.append(s.copy())
            if not changed:
                break
        return s

    # capacity: P random patterns, each started 10% flipped; recalled if it comes back exactly
    Ps = list(range(2, 61, 2))
    frac, stable = [], []
    for P in Ps:
        ok, st = 0, 0
        trials = 6
        for t in range(trials):
            X = g.choice([-1.0, 1.0], size=(P, N))
            W = hebb(X)
            st += float((np.sign(X @ W) == X).mean())
            for k in range(min(P, 8)):
                cue = X[k] * np.where(g.random(N) < 0.1, -1, 1)
                ok += int(np.array_equal(run(W, cue, 6), X[k]))
        frac.append(ok / (trials * min(P, 8)))
        stable.append(st / trials)
    # digits: one per class, as +-1 pixels
    d = gd.digits()
    pick = [int(np.where(d["yte"] == c)[0][0]) for c in range(10)]
    Xd = gd.binarize(d["xte"][pick]) * 2 - 1
    overlap = Xd @ Xd.T / N
    recall = {"hebb": [], "modern": []}
    for P in range(1, 11):
        W = hebb(Xd[:P])
        oh, om = 0, 0
        for k in range(P):
            cue = Xd[k] * np.where(np.random.default_rng(k).random(N) < 0.25, -1, 1)
            oh += int((run(W, cue, 6) == Xd[k]).mean() > 0.97)
            # the modern (dense) Hopfield update: softmax(beta X s) X, one step (Ramsauer et al. 2020)
            a = 8.0 * (Xd[:P] @ cue) / N
            pz = np.exp(a - a.max())
            s_new = np.sign(pz / pz.sum() @ Xd[:P])
            om += int((s_new == Xd[k]).mean() > 0.97)
        recall["hebb"].append(oh / P)
        recall["modern"].append(om / P)
    # one recall, replayed: three digits stored, a 25%-flipped cue, every update
    W = hebb(Xd[:3])
    cue = Xd[1] * np.where(np.random.default_rng(42).random(N) < 0.25, -1, 1)
    rec = []
    fin = run(W, cue, 4, rec)
    frames = np.array([cue] + rec[::14] + [fin])
    energy = np.array([-0.5 * s @ W @ s for s in frames])
    # with five digits stored, the same cue lands in a mixture
    W5 = hebb(Xd[:6])
    mix = run(W5, Xd[1] * np.where(np.random.default_rng(42).random(N) < 0.25, -1, 1), 6)
    return dict(N=N, Ps=Ps, recall_random=frac, stable_random=stable, digits=Xd, overlap=overlap,
                recall_hebb=recall["hebb"], recall_modern=recall["modern"], frames=frames, energy=energy,
                final_overlap=float(fin @ Xd[1] / N), mixture=mix, mixture_overlap=(Xd[:6] @ mix / N),
                beta_modern=8.0, trials=6)


def compute_eval2d():
    """Every family on the ring, three seeds, judged the same way against 2,000 fresh points of the ring."""
    toys = load("toys")
    real = g2.ring(2000, g2.rng(31337))
    src = {"ar": ("ar2d", "ring_s{s}"), "vae": ("vae2d", "ring_s{s}"), "gan": ("gan2d", "ring_ns_s{s}"),
           "wgan": ("gan2d", "ring_wgan_s{s}"), "flow": ("flow2d", "ring_s{s}"), "ebm": ("ebm2d", "ring_s{s}")}
    out = {}
    for fam, (item, pat) in src.items():
        d = load(item)
        rows = []
        for s in SEEDS:
            S_ = np.asarray(d[pat.format(s=s)])
            nm, q, counts = g2.modes(S_)
            p, r = g2.prec_rec(real, S_)
            rows.append(dict(modes=nm, quality=q, precision=p, recall=r, fd=g2.frechet(real, S_), counts=counts))
        out[fam] = rows
        log(f"eval2d {fam}: modes {[r_['modes'] for r_ in rows]}, P {[round(r_['precision'], 2) for r_ in rows]}, "
            f"R {[round(r_['recall'], 2) for r_ in rows]}")
    nll = {"ar": [load("ar2d")[f"ring_nll_s{s}"] for s in SEEDS],
           "vae": [load("vae2d")[f"ring_nll_iw_s{s}"] for s in SEEDS],
           "flow": [load("flow2d")[f"ring_nll_s{s}"] for s in SEEDS],
           "ebm": [load("ebm2d")[f"ring_nll_s{s}"] for s in SEEDS]}
    # a single Gaussian with the ring's mean and covariance: the Frechet distance cannot tell it from the ring
    m, C = real.mean(0), np.cov(real, rowvar=False)
    blob = np.random.default_rng(8).multivariate_normal(m, C, 2000)
    p, r = g2.prec_rec(real, blob)
    nm, q, _ = g2.modes(blob)
    real2 = g2.ring(2000, g2.rng(4))
    p2, r2 = g2.prec_rec(real, real2)
    return dict(families=list(src), rows=out, nll=nll, entropy=toys["ring_entropy"], blob=blob,
                blob_fd=g2.frechet(real, blob), blob_precision=p, blob_recall=r, blob_modes=nm,
                real_fd=g2.frechet(real, real2), real_precision=p2, real_recall=r2, real=real)


# ===========================================================================
# Digits
# ===========================================================================
def compute_classifier():
    _threads()
    t = time.time()
    net, acc = gd.train_classifier(0)
    save_model(net, "classifier")
    J = gd.Judge(net)
    d = gd.digits()
    g = np.random.default_rng(0)
    ns = [100, 250, 500, 1000, 2000, 5000, 10000]
    fid_n = []
    for n in ns:
        vals = []
        for r in range(3):
            idx = g.choice(len(d["xtr"]), n, replace=False)
            m, S_ = gd.gauss_stats(net.features(d["xtr"][idx]))
            vals.append(gd.fid_from(m, S_, J.mu, J.S))
        fid_n.append(vals)
    base = d["xtr"][g.choice(len(d["xtr"]), 2000, replace=False)]
    xf = base.astype(np.float32) / 15
    noise_fid = []
    sigmas = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]
    for s in sigmas:
        q = gd.to_levels(np.clip(xf + s * g.normal(size=xf.shape), 0, 1))
        noise_fid.append(J(q))
    k = np.ones((3, 3)) / 9
    from scipy.signal import convolve2d

    blurred = gd.to_levels(np.array([convolve2d(x, k, mode="same") for x in xf]))
    blur = J(blurred)
    real = J(base)
    examples = dict(clean=base[:4], noisy=gd.to_levels(np.clip(xf[:4] + 0.2 * g.normal(size=xf[:4].shape), 0, 1)),
                    blurred=blurred[:4])
    log(f"classifier: test accuracy {acc:.4f} ({time.time() - t:.0f}s); real FID {real['fid']:.2f}")
    from videos.ai.ai10.data import mnist

    raw = mnist()["xte"][:4]  # the original 28 x 28 digits, for the picture of the downsampling
    half = raw.reshape(-1, gd.S, 2, gd.S, 2).astype(np.float32).mean((2, 4)) / 255
    return dict(accuracy=acc, params=g2.n_params(net), feature_dim=128, ns=ns, fid_n=np.array(fid_n),
                raw28=raw, half14=half, budget=gd.BUDGET,
                noise_sigmas=sigmas, noise=[dict(fid=r["fid"], precision=r["precision"], recall=r["recall"])
                                            for r in noise_fid],
                blur=dict(fid=blur["fid"], precision=blur["precision"], recall=blur["recall"]),
                real=dict(fid=real["fid"], precision=real["precision"], recall=real["recall"]),
                ex_clean=examples["clean"], ex_noisy=examples["noisy"], ex_blur=examples["blurred"],
                train_counts=np.bincount(d["ytr"], minlength=10), n_train=len(d["ytr"]), n_test=len(d["yte"]),
                grid=d["xte"][:64], grid_labels=d["yte"][:64])


_JUDGE: list = []


def judge() -> gd.Judge:
    if not _JUDGE:
        load("classifier")
        _JUDGE.append(gd.Judge(load_model(gd.Classifier(), "classifier", "classifier")))
    return _JUDGE[0]


def _bud(flops_step: float, budget: float = gd.BUDGET) -> int:
    return max(50, int(budget / flops_step))


def _sched(opt, steps):
    return torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 * (1 + math.cos(math.pi * min(s, steps) / steps)))


def train_pixelcnn(seed: int, replay: bool):
    gen = g2.tseed(seed)
    d = gd.digits()
    net = gd.PixelCNN()
    opt = torch.optim.Adam(net.parameters(), 2e-3)
    bs = 64
    it = gd.batches(d["xtr"], bs, g2.rng(seed))
    xb = next(it)

    def step():
        loss = gd.ar_nll(net, xb).mean() / gd.D
        opt.zero_grad()
        loss.backward()

    fl = gd.step_flops(step)
    opt.zero_grad()
    steps = _bud(fl)
    sched = _sched(opt, steps)
    marks = gd.checkpoints(steps, 11)
    curve, snaps, train = [], [], []
    te = d["xte"][:1000]
    t0 = time.time()
    run = 0.0
    for s in range(steps + 1):
        if s in marks:
            net.eval()
            with torch.no_grad():
                bpp = float(gd.ar_nll(net, te).mean()) / (gd.D * math.log(2))
            curve.append((s, s * bs, bpp))
            if replay:
                snaps.append(gd.ar_sample(net, 16, torch.Generator().manual_seed(1234)))
            net.train()
        if s == steps:
            break
        loss = gd.ar_nll(net, next(it)).mean() / gd.D
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        run = 0.98 * run + 0.02 * float(loss) if s else float(loss)
        if s % 20 == 0:
            train.append((s, run / math.log(2)))
    secs = time.time() - t0
    net.eval()
    with torch.no_grad():
        bpp = float(torch.cat([gd.ar_nll(net, d["xte"][a:a + 1000]) for a in range(0, 10000, 1000)]).mean()) / (
            gd.D * math.log(2))
    t = time.time()
    samples = np.concatenate([gd.ar_sample(net, gd.N_GEN // 4, torch.Generator().manual_seed(77 + k))
                              for k in range(4)])
    sample_secs = (time.time() - t) / len(samples)
    res = dict(curve=curve, train=train, bpp=bpp, step_flops=fl, steps=steps, batch=bs, examples=steps * bs,
               params=g2.n_params(net), secs=secs, sample_secs=sample_secs, nfe=gd.D, show=samples[:64],
               judge=judge()(samples))
    if replay:
        res["snaps"] = np.array(snaps)
        q, probs = gd.ar_sample(net, 1, torch.Generator().manual_seed(2024), trace=True)
        res["trace_image"], res["trace_probs"] = q[0], probs
    save_model(net, f"pixelcnn_s{seed}")
    return res


def compute_pixelcnn():
    _threads()
    part = CACHE.partial("pixelcnn", dict(v=1, budget=gd.BUDGET))
    for s in SEEDS:
        if f"s{s}" not in part:
            t = time.time()
            part[f"s{s}"] = tolist(train_pixelcnn(s, replay=(s == 0)))
            log(f"pixelcnn s{s}: {part[f's{s}']['bpp']:.3f} bits/pixel, FID {part[f's{s}']['judge']['fid']:.2f} "
                f"({time.time() - t:.0f}s)")
    out = _collect(part)
    torch.manual_seed(0)
    out["rf_plain"] = gd.receptive_field(gd.PlainPixelCNN())
    out["rf_two"] = gd.receptive_field(gd.PixelCNN())
    return out


def _collect(part) -> dict:
    out = {}
    for s in SEEDS:
        p = part[f"s{s}"]
        for k, v in p.items():
            out[f"s{s}_{k}"] = np.asarray(v) if isinstance(v, list) and k in ("curve", "train", "snaps", "show",
                                                                            "trace_image", "trace_probs", "kl_dims",
                                                                            "recon", "recon_src", "snap_recs",
                                                                            "activity", "show_cold") else v
    return out


def train_vae(seed: int, replay: bool, zdim=16, beta=1.0, budget=gd.BUDGET, tag="vae"):
    gen = g2.tseed(seed)
    d = gd.digits()
    m = gd.VAE(zdim)
    opt = torch.optim.Adam(m.parameters(), 1e-3)
    bs = 128
    it = gd.batches(d["xtr"], bs, g2.rng(seed))
    xb = next(it)

    def step():
        l, _, _, _ = m.terms(xb, gen, beta)
        opt.zero_grad()
        l.mean().backward()

    fl = gd.step_flops(step)
    opt.zero_grad()
    steps = _bud(fl, budget)
    sched = _sched(opt, steps)
    marks = gd.checkpoints(steps, 12)
    te = d["xte"][:2000]
    zfix = torch.randn(16, zdim, generator=torch.Generator().manual_seed(1234))
    curve, snaps, recs = [], [], []
    t0 = time.time()
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                l, r, k, _ = m.terms(te, gen, 1.0)
            curve.append((s, s * bs, float(l.mean()), float(r.mean()), float(k.mean())))
            if replay:
                snaps.append(m.sample(16, gen, zfix))
                with torch.no_grad():
                    mu, _ = m.encode(gd.as_float(te[:8]))
                    recs.append(gd.to_levels(m.decode(mu)[0].numpy()))
        if s == steps:
            break
        l, _, _, _ = m.terms(next(it), gen, beta)
        opt.zero_grad()
        l.mean().backward()
        opt.step()
        sched.step()
    secs = time.time() - t0
    with torch.no_grad():
        l, r, k, kd = m.terms(d["xte"], gen, 1.0)
        mu, _ = m.encode(gd.as_float(d["xte"]))
        au = mu.var(0).numpy()  # Burda et al.'s activity: a unit is active if its code mean varies with x
        rec = m.decode(mu[:8])[0].numpy()
    lg2 = gd.D * math.log(2)
    res = dict(curve=curve, elbo_bpp=float(l.mean()) / lg2, rec_nats=float(r.mean()), kl_nats=float(k.mean()),
               kl_dims=kd.mean(0).numpy(), activity=au, active=int((au > 0.01).sum()), step_flops=fl, steps=steps,
               batch=bs, examples=steps * bs, params=g2.n_params(m), secs=secs, beta=beta,
               recon=gd.to_levels(rec), recon_src=d["xte"][:8])
    if replay:
        res["snaps"], res["snap_recs"] = np.array(snaps), np.array(recs)
    return m, res


def compute_vae():
    _threads()
    part = CACHE.partial("vae", dict(v=1, budget=gd.BUDGET))
    for s in SEEDS:
        if f"s{s}" in part:
            continue
        t = time.time()
        m, res = train_vae(s, replay=(s == 0))
        gen = torch.Generator().manual_seed(77)
        samples = m.sample(gd.N_GEN, gen)
        res["iwae_bpp"] = float(-m.iwae(gd.digits()["xte"][:1000], gen).mean()) / (gd.D * math.log(2))
        res["judge"], res["show"], res["nfe"] = judge()(samples), samples[:64], 1
        t1 = time.time()
        m.sample(gd.N_GEN, gen)
        res["sample_secs"] = (time.time() - t1) / gd.N_GEN
        save_model(m, f"vae_s{s}")
        part[f"s{s}"] = tolist(res)
        log(f"vae s{s}: ELBO {res['elbo_bpp']:.3f} bpp, IWAE {res['iwae_bpp']:.3f}, KL {res['kl_nats']:.1f}, "
            f"active {res['active']}, FID {res['judge']['fid']:.2f} ({time.time() - t:.0f}s)")
    return _collect(part)


def compute_vae_map():
    _threads()
    gen = g2.tseed(0)
    d = gd.digits()
    m = gd.VAE(2)
    opt = torch.optim.Adam(m.parameters(), 1e-3)
    bs = 128
    steps = g2.scaled(6000)
    sched = _sched(opt, steps)
    it = gd.batches(d["xtr"], bs, g2.rng(0))
    marks = gd.checkpoints(steps, 10)
    te, lab = d["xte"][:2000], d["yte"][:2000]
    codes, curve = [], []
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                mu, _ = m.encode(gd.as_float(te))
                l, r, k, _ = m.terms(te, gen)
            codes.append(mu.numpy())
            curve.append((s, float(l.mean()), float(r.mean()), float(k.mean())))
        if s == steps:
            break
        l, _, _, _ = m.terms(next(it), gen)
        opt.zero_grad()
        l.mean().backward()
        opt.step()
        sched.step()
    from scipy.stats import norm

    u = norm.ppf(np.linspace(0.04, 0.96, 15))
    Z = torch.as_tensor(np.array([[a, b] for b in u[::-1] for a in u]), dtype=torch.float32)
    with torch.no_grad():
        grid = gd.to_levels(m.decode(Z)[0].numpy())
    return dict(codes=np.array(codes, np.float32), labels=lab, steps=[c for c in marks], curve=np.array(curve),
                grid=grid.reshape(15, 15, gd.S, gd.S), grid_z=u)


def compute_beta():
    _threads()
    betas = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    part = CACHE.partial("beta", dict(v=1, budget=gd.BUDGET / 4, betas=betas))
    for b in betas:
        for s in (0, 1):
            key = f"b{b}_s{s}"
            if key in part:
                continue
            m, res = train_vae(10 + s, replay=False, beta=b, budget=gd.BUDGET / 4)
            gen = torch.Generator().manual_seed(77)
            res["show"] = m.sample(16, gen)
            part[key] = tolist({k: res[k] for k in ("rec_nats", "kl_nats", "elbo_bpp", "active", "kl_dims", "show",
                                                    "recon", "steps", "examples")})
            log(f"beta {key}: rate {res['kl_nats']:.1f}, distortion {res['rec_nats']:.1f}, active {res['active']}")
    out = dict(betas=betas)
    for k in ("rec_nats", "kl_nats", "elbo_bpp", "active"):
        out[k] = np.array([[part[f"b{b}_s{s}"][k] for s in (0, 1)] for b in betas])
    out["show"] = np.array([part[f"b{b}_s0"]["show"] for b in betas])
    out["recon"] = np.array([part[f"b{b}_s0"]["recon"] for b in betas])
    out["kl_dims"] = np.array([part[f"b{b}_s0"]["kl_dims"] for b in betas])
    out["recon_src"] = gd.digits()["xte"][:8]
    out["steps"] = part[f"b{betas[0]}_s0"]["steps"]
    return out


class PixelVAE(nn.Module):
    """A VAE whose decoder is a PixelCNN conditioned on the code: strong enough to ignore it."""

    def __init__(self, zdim=16, h=512):
        super().__init__()
        self.zdim = zdim
        self.enc = nn.Sequential(nn.Linear(gd.D, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(), nn.Linear(h, 2 * zdim))
        self.dec = gd.PixelCNN(zdim=zdim)

    def terms(self, q, gen, free_bits=0.0):
        qt = torch.as_tensor(np.asarray(q), dtype=torch.long)
        mu, lv = self.enc(qt.reshape(len(q), -1).float() / (gd.Q - 1)).chunk(2, -1)
        lv = lv.clamp(-12, 6)
        z = mu + (0.5 * lv).exp() * torch.randn(mu.shape, generator=gen)
        rec = gd.ar_nll(self.dec, q, z)
        kld = 0.5 * (mu ** 2 + lv.exp() - lv - 1)
        kl = kld.sum(1)
        obj = rec + (torch.clamp(kld.mean(0), min=free_bits).sum() if free_bits else kl)
        return obj, rec, kl


def compute_collapse():
    _threads()
    part = CACHE.partial("collapse", dict(v=1, budget=gd.BUDGET / 2))
    d = gd.digits()
    for tag, fb in (("plain", 0.0), ("free", 0.25)):
        if tag in part:
            continue
        gen = g2.tseed(0)
        m = PixelVAE()
        opt = torch.optim.Adam(m.parameters(), 2e-3)
        bs = 64
        it = gd.batches(d["xtr"], bs, g2.rng(0))
        xb = next(it)

        def step():
            o, _, _ = m.terms(xb, gen, fb)
            opt.zero_grad()
            o.mean().backward()

        fl = gd.step_flops(step)
        opt.zero_grad()
        steps = _bud(fl, gd.BUDGET / 2)
        sched = _sched(opt, steps)
        marks = sorted(set(np.linspace(0, steps, 25).astype(int)))
        te = d["xte"][:500]
        curve = []
        t = time.time()
        for s in range(steps + 1):
            if s in marks:
                with torch.no_grad():
                    _, r, k = m.terms(te, gen)
                curve.append((s, s * bs, float(r.mean()), float(k.mean())))
            if s == steps:
                break
            o, _, _ = m.terms(next(it), gen, fb)
            opt.zero_grad()
            o.mean().backward()
            opt.step()
            sched.step()
        with torch.no_grad():  # does the code matter? the same code for every row, different codes across rows
            mu, _ = m.enc(gd.as_float(d["xte"][:4]).reshape(4, -1)).chunk(2, -1)
            z = mu.repeat_interleave(4, 0)
        same_z = gd.ar_sample(m.dec, 16, torch.Generator().manual_seed(3), z=z)
        # does a decoded digit keep its source's identity? the judge's classes against the source labels
        agree = float((judge().net.classes(same_z) == np.repeat(d["yte"][:4], 4)).mean())
        part[tag] = tolist(dict(curve=curve, free_bits=fb, steps=steps, step_flops=fl, same_z=same_z,
                                src=d["xte"][:4], src_labels=d["yte"][:4], agree=agree, secs=time.time() - t))
        log(f"collapse {tag}: KL {curve[-1][3]:.2f} nats, reconstruction {curve[-1][2]:.1f} ({time.time() - t:.0f}s)")
    out = {}
    for tag in ("plain", "free"):
        for k, v in part[tag].items():
            out[f"{tag}_{k}"] = np.asarray(v) if isinstance(v, list) else v
    return out


def train_gan(seed: int, replay: bool, wgan: bool):
    gen = g2.tseed(seed)
    d = gd.digits()
    G, Dn = gd.gan_nets()
    if wgan:
        oG = torch.optim.Adam(G.parameters(), 1e-4, betas=(0.5, 0.9))
        oD = torch.optim.Adam(Dn.parameters(), 1e-4, betas=(0.5, 0.9))
        n_critic, lam = 5, 10.0
    else:
        oG = torch.optim.Adam(G.parameters(), 2e-4, betas=(0.5, 0.999))
        oD = torch.optim.Adam(Dn.parameters(), 2e-4, betas=(0.5, 0.999))
        n_critic, lam = 1, 0.0
    bs = 128
    it = gd.batches(d["xtr"], bs, g2.rng(seed))

    def gstep():
        for _ in range(n_critic):
            real = gd.dequant(next(it), gen)
            fake = G(torch.randn(bs, gd.ZG, generator=gen)).detach()
            if wgan:
                lD = Dn(fake).mean() - Dn(real).mean() + lam * g2.grad_penalty(Dn, real, fake, gen)
            else:
                lD = F.softplus(-Dn(real)).mean() + F.softplus(Dn(fake)).mean()
            oD.zero_grad()
            lD.backward()
            oD.step()
        out = Dn(G(torch.randn(bs, gd.ZG, generator=gen)))
        lG = -out.mean() if wgan else F.softplus(-out).mean()
        oG.zero_grad()
        lG.backward()
        oG.step()
        return float(lD), float(lG)

    sd_G, sd_D = {k: v.clone() for k, v in G.state_dict().items()}, {k: v.clone() for k, v in Dn.state_dict().items()}
    fl = gd.step_flops(gstep)
    G.load_state_dict(sd_G)
    Dn.load_state_dict(sd_D)
    oG = type(oG)(G.parameters(), **{k: oG.defaults[k] for k in ("lr", "betas")})
    oD = type(oD)(Dn.parameters(), **{k: oD.defaults[k] for k in ("lr", "betas")})
    steps = _bud(fl)
    marks = gd.checkpoints(steps, 12)
    zfix = torch.randn(16, gd.ZG, generator=torch.Generator().manual_seed(1234))
    snaps, losses = [], []
    t0 = time.time()
    for s in range(steps + 1):
        if s in marks and replay:
            with torch.no_grad():
                snaps.append(gd.to_levels(G(zfix).numpy()))
        if s == steps:
            break
        lD, lG = gstep()
        if s % 25 == 0:
            losses.append((s, lD, lG))
    secs = time.time() - t0
    with torch.no_grad():
        samples = gd.to_levels(G(torch.randn(gd.N_GEN, gd.ZG, generator=torch.Generator().manual_seed(77))).numpy())
        t = time.time()
        G(torch.randn(gd.N_GEN, gd.ZG))
        sample_secs = (time.time() - t) / gd.N_GEN
    res = dict(losses=losses, step_flops=fl, steps=steps, batch=bs, examples=steps * bs * n_critic,
               params=g2.n_params(G) + g2.n_params(Dn), params_G=g2.n_params(G), secs=secs, sample_secs=sample_secs,
               nfe=1, show=samples[:64], judge=judge()(samples), marks=marks, n_critic=n_critic)
    if replay:
        res["snaps"] = np.array(snaps)
    save_model(G, f"{'wgan' if wgan else 'gan'}_G_s{seed}")
    return res


def _gan_item(wgan: bool):
    _threads()
    name = "wgan" if wgan else "gan"
    part = CACHE.partial(name, dict(v=1, budget=gd.BUDGET))
    for s in SEEDS:
        if f"s{s}" not in part:
            t = time.time()
            part[f"s{s}"] = tolist(train_gan(s, s == 0, wgan))
            j = part[f"s{s}"]["judge"]
            log(f"{name} s{s}: {part[f's{s}']['steps']} steps, FID {j['fid']:.2f}, P {j['precision']:.2f}, "
                f"R {j['recall']:.2f} ({time.time() - t:.0f}s)")
    out = _collect(part)
    for s in SEEDS:
        out[f"s{s}_losses"] = np.asarray(part[f"s{s}"]["losses"])
    return out


def compute_gan():
    return _gan_item(False)


def compute_wgan():
    return _gan_item(True)


def train_flow(seed: int, replay: bool):
    gen = g2.tseed(seed)
    d = gd.digits()
    m = gd.RealNVP()
    opt = torch.optim.Adam(m.parameters(), 1e-3)
    bs = 128
    it = gd.batches(d["xtr"], bs, g2.rng(seed))
    xb = next(it)

    def step():
        l = m.bits(xb, gen).mean()
        opt.zero_grad()
        l.backward()

    fl = gd.step_flops(step)
    opt.zero_grad()
    steps = _bud(fl)
    sched = _sched(opt, steps)
    marks = gd.checkpoints(steps, 12)
    te = d["xte"][:2000]
    curve, snaps = [], []
    t0 = time.time()
    for s in range(steps + 1):
        if s in marks:
            with torch.no_grad():
                curve.append((s, s * bs, float(m.bits(te, gen).mean())))
            if replay:
                snaps.append(m.sample(16, torch.Generator().manual_seed(1234)))
        if s == steps:
            break
        l = m.bits(next(it), gen).mean()
        opt.zero_grad()
        l.backward()
        nn.utils.clip_grad_norm_(m.parameters(), 50.0)
        opt.step()
        sched.step()
    secs = time.time() - t0
    with torch.no_grad():
        bpp = float(torch.cat([m.bits(d["xte"][a:a + 2000], gen) for a in range(0, 10000, 2000)]).mean())
    samples = m.sample(gd.N_GEN, torch.Generator().manual_seed(77))
    t = time.time()
    m.sample(gd.N_GEN, torch.Generator().manual_seed(78))
    res = dict(curve=curve, bpp=bpp, step_flops=fl, steps=steps, batch=bs, examples=steps * bs,
               params=g2.n_params(m), secs=secs, sample_secs=(time.time() - t) / gd.N_GEN, nfe=1, show=samples[:64],
               show_cold=m.sample(64, torch.Generator().manual_seed(77), temp=0.7), judge=judge()(samples))
    if replay:
        res["snaps"] = np.array(snaps)
    save_model(m, f"flow_s{seed}")
    return res


def compute_flow():
    _threads()
    part = CACHE.partial("flow", dict(v=1, budget=gd.BUDGET))
    for s in SEEDS:
        if f"s{s}" not in part:
            t = time.time()
            part[f"s{s}"] = tolist(train_flow(s, s == 0))
            p = part[f"s{s}"]
            log(f"flow s{s}: {p['bpp']:.3f} bits/pixel, FID {p['judge']['fid']:.2f} ({time.time() - t:.0f}s)")
    out = _collect(part)
    for s in SEEDS:
        out[f"s{s}_show_cold"] = np.asarray(part[f"s{s}"]["show_cold"])
    return out


def compute_rbm():
    _threads()
    part = CACHE.partial("rbm", dict(v=1, nh=16))
    for meth in ("cd1", "cd10", "pcd"):
        for s in SEEDS:
            key = f"{meth}_s{s}"
            if key in part:
                continue
            t = time.time()
            m, r = gd.train_rbm(meth, s)
            res = dict(curve=r["curve"], test_ll=r["test_ll"], steps=r["steps"])
            if s == 0:
                gen = torch.Generator().manual_seed(5)
                res["W"] = m.W.T.numpy()
                res["exact"] = m.exact_sample(16, gen).numpy()
                v = torch.bernoulli(torch.full((16, gd.D), 0.5), generator=gen)
                chain = [v.numpy().copy()]
                for k in (1, 9, 90, 900):
                    v = m.gibbs(v, k, gen)
                    chain.append(m.pv(torch.bernoulli(m.ph(v), generator=gen)).numpy())
                res["chain"] = chain
            part[key] = tolist(res)
            log(f"rbm {key}: exact test log-likelihood {r['test_ll']:.2f} nats ({time.time() - t:.0f}s)")
    if "big" not in part:  # a bigger machine, for its filters and its dreams
        t = time.time()
        m, r = gd.train_rbm("pcd", 0, nh=100, epochs=6, exact=False)
        gen = torch.Generator().manual_seed(6)
        v = torch.bernoulli(torch.full((16, gd.D), 0.5), generator=gen)
        chain = [v.numpy().copy()]
        for k in (1, 9, 90, 900):
            v = m.gibbs(v, k, gen)
            chain.append(m.pv(torch.bernoulli(m.ph(v), generator=gen)).numpy())
        part["big"] = tolist(dict(W=m.W.T.numpy(), chain=chain))
        log(f"rbm big ({time.time() - t:.0f}s)")
    out = {}
    for k in part.done:
        for kk, v in part[k].items():
            out[f"{k}_{kk}"] = np.asarray(v) if isinstance(v, list) else v
    out["nh"], out["nv"] = 16, gd.D
    d = gd.digits()
    out["binary_examples"] = gd.binarize(d["xte"][:16])
    return out


def compute_vq():
    _threads()
    gen = g2.tseed(0)
    d = gd.digits()
    vq = gd.VQVAE()
    opt = torch.optim.Adam(vq.parameters(), 1e-3)
    bs = 128
    steps = g2.scaled(3 * len(d["xtr"]) // bs)
    sched = _sched(opt, steps)
    it = gd.batches(d["xtr"], bs, g2.rng(0))
    t = time.time()
    curve = []
    for s in range(steps):
        l, rec, idx = vq.loss(next(it))
        opt.zero_grad()
        l.backward()
        opt.step()
        sched.step()
        if s % 100 == 0:
            curve.append((s, float(rec)))
        if s % 500 == 0 and s:  # revive codes nobody uses (a common fix for codebook collapse)
            with torch.no_grad():
                e = vq.enc(gd.as_float(next(it))).permute(0, 2, 3, 1).reshape(-1, vq.code.shape[1])
                used = torch.bincount(vq.quantize(vq.enc(gd.as_float(d["xte"][:500])))[1].ravel(), minlength=vq.K)
                dead = torch.where(used == 0)[0]
                if len(dead):
                    vq.code.data[dead] = e[torch.randint(0, len(e), (len(dead),), generator=gen)]
    vq_secs = time.time() - t
    with torch.no_grad():
        codes_tr = torch.cat([vq.quantize(vq.enc(gd.as_float(d["xtr"][a:a + 2000])))[1]
                              for a in range(0, len(d["xtr"]), 2000)]).reshape(-1, 49)
        codes_te = vq.quantize(vq.enc(gd.as_float(d["xte"][:2000])))[1].reshape(-1, 49)
        m, ls = vq.decode_codes(codes_te[:8].reshape(-1, 7, 7))
        recon = gd.to_levels(m.numpy())
        _, rec_te, _ = vq.loss(d["xte"][:2000])
    usage = np.bincount(codes_tr.numpy().ravel(), minlength=vq.K) / codes_tr.numel()
    perplexity = float(np.exp(-(usage[usage > 0] * np.log(usage[usage > 0])).sum()))
    prior = gd.CodePrior()
    opt = torch.optim.Adam(prior.parameters(), 1e-3)
    pst = g2.scaled(4 * len(codes_tr) // 256)
    sched = _sched(opt, pst)
    g = np.random.default_rng(0)
    pcurve = []
    t = time.time()
    for s in range(pst):
        j = torch.as_tensor(g.integers(0, len(codes_tr), 256))
        c = codes_tr[j]
        loss = F.cross_entropy(prior(c).reshape(-1, vq.K), c.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if s % 50 == 0:
            pcurve.append((s, float(loss)))
    prior_secs = time.time() - t
    with torch.no_grad():
        te_nll = float(F.cross_entropy(prior(codes_te).reshape(-1, vq.K), codes_te.reshape(-1))) * 49
    gen2 = torch.Generator().manual_seed(77)
    cs = torch.cat([prior.sample(gd.N_GEN // 4, gen2) for _ in range(4)])
    with torch.no_grad():
        samples = gd.to_levels(vq.decode_codes(cs.reshape(-1, 7, 7))[0].numpy())
    log(f"vq: perplexity {perplexity:.1f} of {vq.K}, prior {te_nll:.1f} nats per digit ({vq_secs + prior_secs:.0f}s)")
    return dict(curve=np.array(curve), recon=recon, src=d["xte"][:8], codes=codes_te[:8].numpy().reshape(8, 7, 7),
                usage=usage, perplexity=perplexity, K=vq.K, grid=7, rec_nats=float(rec_te),
                prior_curve=np.array(pcurve), prior_nll=te_nll, prior_bits=te_nll / math.log(2),
                show=samples[:64], judge=judge()(samples), codebook_bits=49 * math.log2(vq.K),
                params_vq=g2.n_params(vq), params_prior=g2.n_params(prior), sample_codes=cs[:8].numpy().reshape(8, 7, 7))


def compute_evaluate():
    _threads()
    J = judge()
    d = gd.digits()
    fams = {"pixelcnn": load("pixelcnn"), "vae": load("vae"), "gan": load("gan"), "wgan": load("wgan"),
            "flow": load("flow")}
    table = {}
    for f, r in fams.items():
        rows = []
        for s in SEEDS:
            j = r[f"s{s}_judge"]
            rows.append(dict(fid=j["fid"], precision=j["precision"], recall=j["recall"], classes=j["classes"],
                             bpp=r.get(f"s{s}_bpp", r.get(f"s{s}_iwae_bpp")), params=r[f"s{s}_params"],
                             steps=r[f"s{s}_steps"], examples=r[f"s{s}_examples"], flops=r[f"s{s}_step_flops"] *
                             r[f"s{s}_steps"], secs=r[f"s{s}_secs"], nfe=r[f"s{s}_nfe"],
                             sample_secs=r[f"s{s}_sample_secs"]))
        table[f] = rows
    # the truncation trick on the GAN (seed 0): sample z from a narrower distribution
    G, _ = gd.gan_nets()
    G = load_model(G, "gan_G_s0", "gan")
    trunc = []
    gen = torch.Generator().manual_seed(123)
    ts = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 0.0]  # 0: no truncation
    for t in ts:
        z = torch.randn(gd.N_GEN, gd.ZG, generator=gen)
        if t:
            bad = z.abs() > t
            while bad.any():
                z[bad] = torch.randn(int(bad.sum()), generator=gen)
                bad = z.abs() > t
        with torch.no_grad():
            q = gd.to_levels(G(z).numpy())
        j = J(q)
        trunc.append(dict(t=t, fid=j["fid"], precision=j["precision"], recall=j["recall"], show=q[:8].tolist()))
        log(f"truncation {t}: FID {j['fid']:.2f}, P {j['precision']:.2f}, R {j['recall']:.2f}")
    # GAN inversion: find z with G(z) close to a real digit the generator never saw
    targets = d["xte"][[3, 2, 1, 18, 4, 8, 11, 0]]
    X = gd.as_float(targets).reshape(8, -1)
    best, rec_steps = None, [0, 5, 20, 60, 150, 400]
    traj = []
    for start in range(4):
        z = torch.randn(8, gd.ZG, generator=torch.Generator().manual_seed(600 + start)).requires_grad_(True)
        o = torch.optim.Adam([z], 0.05)
        frames = []
        for s in range(401):
            with torch.no_grad():
                if s in rec_steps:
                    frames.append(gd.to_levels(G(z).numpy()))
            loss = ((G(z) - X) ** 2).sum(1) + 1e-3 * (z ** 2).sum(1)
            if s == 400:
                break
            o.zero_grad()
            loss.sum().backward()
            o.step()
        with torch.no_grad():
            err = ((G(z) - X) ** 2).mean(1)
        traj.append((err.numpy(), frames, z.detach().clone()))
    err_all = np.array([t_[0] for t_ in traj])  # (starts, 8)
    pick = err_all.argmin(0)
    inv_frames = np.array([[traj[pick[i]][1][k][i] for i in range(8)] for k in range(len(rec_steps))])
    zbest = torch.stack([traj[pick[i]][2][i] for i in range(8)])
    inv_err = err_all.min(0)
    vae = load_model(gd.VAE(16), "vae_s0", "vae")
    with torch.no_grad():
        mu, _ = vae.encode(gd.as_float(targets))
        vrec = vae.decode(mu)[0]
        vae_err = ((vrec - X) ** 2).mean(1).numpy()
        lerp = torch.stack([(1 - a) * zbest[0] + a * zbest[1] for a in np.linspace(0, 1, 9)])
        interp = gd.to_levels(G(lerp).numpy())
    # memorization: how close is each generated digit to its nearest training digit, against real test digits
    tr = d["xtr"].reshape(len(d["xtr"]), -1).astype(np.float32) / 15

    def nn_dist(q):
        A = np.asarray(q).reshape(len(q), -1).astype(np.float32) / 15
        best_ = np.full(len(A), np.inf)
        arg = np.zeros(len(A), int)
        for a in range(0, len(tr), 10000):
            dd = gd.sqd(A, tr[a:a + 10000])
            m_ = dd.min(1)
            upd = m_ < best_
            arg[upd] = dd.argmin(1)[upd] + a
            best_ = np.minimum(best_, m_)
        return np.sqrt(best_ / A.shape[1]), arg

    mem = {}
    for f, r in fams.items():
        dist, arg = nn_dist(r["s0_show"])
        mem[f] = dict(dist=dist, nearest=d["xtr"][arg[:8]])
    dist, _ = nn_dist(d["xte"][:64])
    mem["real"] = dict(dist=dist)
    out = dict(families=list(fams), table=table, trunc=trunc, trunc_t=ts, inv_targets=targets, inv_steps=rec_steps,
               inv_frames=inv_frames, inv_err=inv_err, vae_err=vae_err, vae_recon=gd.to_levels(vrec.numpy()),
               interp=interp, real_floor=load("classifier")["real"], vq=load("vq")["judge"])
    for f in mem:
        out[f"mem_{f}_dist"] = mem[f]["dist"]
        if "nearest" in mem[f]:
            out[f"mem_{f}_nearest"] = mem[f]["nearest"]
    return out


def _item(fn):
    """Top-level numpy arrays go to the item's .npz; anything nested (dicts, lists of arrays) becomes plain JSON."""
    def run():
        out = fn()
        return {k: (v if isinstance(v, np.ndarray) else tolist(v)) for k, v in out.items()}
    run.__name__ = fn.__name__
    return run


ITEMS = {
    "toys": compute_toys,
    "bilinear": compute_bilinear,
    "jsw": compute_jsw,
    "langevin": compute_langevin,
    "hopfield": compute_hopfield,
    "ar2d": compute_ar2d,
    "vae2d": compute_vae2d,
    "collapse2d": compute_collapse2d,
    "flow2d": compute_flow2d,
    "gan2d": compute_gan2d,
    "gan2d_collapse": compute_gan2d_collapse,
    "ebm2d": compute_ebm2d,
    "cnf": compute_cnf,
    "eval2d": compute_eval2d,
    "classifier": compute_classifier,
    "rbm": compute_rbm,
    "vae_map": compute_vae_map,
    "vae": compute_vae,
    "gan": compute_gan,
    "flow": compute_flow,
    "pixelcnn": compute_pixelcnn,
    "wgan": compute_wgan,
    "beta": compute_beta,
    "collapse": compute_collapse,
    "vq": compute_vq,
    "evaluate": compute_evaluate,
}
ITEMS = {k: _item(v) for k, v in ITEMS.items()}

if __name__ == "__main__":
    _threads()
    CACHE.main(ITEMS, __doc__)
