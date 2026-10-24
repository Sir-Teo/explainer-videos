"""Precompute everything numerical in Part 12 of the AI series ("The Mathematics of Scale").

    python -m videos.ai.ai12.compute              # everything missing (Part 1's books: .cache/ai1); about 3 CPU-hours
    python -m videos.ai.ai12.compute sweep        # one item;  --force to recompute

Results are cached in ``.cache/ai12/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every run is seeded and
single-threaded (``AI12_THREADS``, default 1: on a shared 4-core machine one thread per job ran fastest). The long
items save each finished piece as they go (``CACHE.partial``) and resume where they stopped; the scaling sweep also
keeps a small checkpoint of the run in progress (``.cache/ai12/sweep_*.ckpt.pt``). ``AI12_WORKERS`` (default 1) runs
the learning-rate sweeps in that many processes (``spawn``); the results do not depend on it.

The workhorse is Part 11's character model (``charlm.py``): 8 characters of context, scored in bits per character on
held-out text from Part 1's thirty novels. The small exact experiments are in ``toys.py``, grokking in ``grok.py``.

Items:
    nngp       a wide two-layer net at initialization: its output over many random starts tends to a Gaussian
    ntk        the same net trained by gradient descent at widths 30 ... 30,000: how far the weights and the tangent
               kernel move (about 1/sqrt(width)), and the trained net against its own linearization
    lazy       Part 11's character model, wider and wider, plain gradient descent with neural-tangent step sizes: how
               much its hidden features change in training
    rich       lazy against rich: a two-layer net learning (w*.x)^2 - 1 in 32 dimensions from 256 examples, in the
               neural-tangent and the mean-field (muP) parametrizations, three seeds, and kernel regression
    coord      muP's coordinate check: how much each layer's activations change in the first Adam steps, widths 64
               to 4,096, standard parametrization against muP
    mup        learning-rate sweeps at widths 64, 256 and 1,024, standard and muP, two seeds (resumable)
    depth      learning-rate sweeps of a deep residual character model at depths 2 to 32 with no depth scaling,
               depth-muP (1/sqrt L) and CompleteP (1/L), two seeds (resumable)
    batch      steps and characters to reach a loss at batch sizes 32 to 4,096 (McCandlish et al.'s trade-off), and
               the gradient noise scale measured along the way (resumable)
    sweep      the scaling sweep: 11 widths x training lengths 2^16 ... 2^24 characters, one run per width with a
               constant learning rate and a cool-down branch at each length (warmup-stable-decay); every endpoint
               scored on held-out text, after post-training quantization to 8 ... 3 bits, and on a checkable task
               (guess the next 8 characters); extra seeds at two widths (resumable; about an hour)
    chinchilla Chinchilla's three methods on the sweep (envelope, iso-FLOP parabolas, the fitted L(N, D)); the fit
               on the cheap half predicting the expensive half; counting parameters Kaplan's way
    repeat     data-constrained: 4.2 million characters of training drawn from 2^22 ... 2^14 distinct ones (1 to 256
               epochs), three seeds; the effective data, and Muennighoff et al.'s R* fitted
    moe        the character model's hidden layer split into 1 ... 32 experts (one used per character), two seeds
    precision  how much post-training quantization costs, against model size and training length (from sweep)
    quanta     the quanta model's multitask sparse parity: 32 subtasks of Zipfian frequency, widths 8 ... 512
    manifold   regression with N linear pieces on a manifold of dimension 1, 2, 4, 8: loss against N
    emerge     the checkable task across model sizes: per-character loss, per-character accuracy, exact match
    testtime   the checkable task with many tries: pass@k from each model's exact probabilities; the power law in
               k, its origin in the hardest problems, and trading model size for tries at equal inference compute
    grok       grokking on (a + b) mod 97: the replayed run (snapshots of the number vectors, their Fourier spectrum,
               the tangent kernel's distance from where it started), and weight decay swept over five values,
               three seeds each (resumable)
"""

from __future__ import annotations

import copy
import math
import os
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai12")
if os.environ.get("AI12_CACHE"):  # a scratch cache (e.g. a quick, shrunken run for checking layouts)
    from pathlib import Path

    CACHE.dir = Path(os.environ["AI12_CACHE"])
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _workers() -> int:
    return max(1, int(os.environ.get("AI12_WORKERS", 1)))


def _pmap(fn, jobs: list) -> list:
    """``fn(*job)`` for every job, in AI12_WORKERS processes (spawn: fork and torch don't mix on macOS)."""
    if _workers() == 1 or len(jobs) < 2:
        return [fn(*j) for j in jobs]
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(_workers(), mp_context=mp.get_context("spawn")) as ex:
        return list(ex.map(fn, *zip(*jobs)))


def _nearest(values, v) -> int:
    """The index of ``v`` in ``values`` (or of the nearest value, for a shrunken test run)."""
    values = list(values)
    return values.index(v) if v in values else int(np.argmin([abs(float(x) - v) for x in values]))


def loglog_slope(x, y, lo=None) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = np.isfinite(x) & np.isfinite(y) & (y > 0) & (x > 0) & (x >= (lo or -np.inf))
    if keep.sum() < 2:
        return float("nan")
    return float(np.polyfit(np.log(x[keep]), np.log(y[keep]), 1)[0])


# ---------------------------------------------------------------------------
# 1. Infinitely wide
# ---------------------------------------------------------------------------
def compute_nngp():
    from . import toys

    return toys.nngp()


NTK_WIDTHS = [30, 100, 300, 1000, 3000, 10000, 30000]


def compute_ntk():
    from . import toys

    rows = {k: [] for k in ("moved_hidden", "moved_out", "kernel_moved", "lin_gap", "train_mse")}
    show = None
    for n in NTK_WIDTHS:
        vals = {k: [] for k in rows}
        for seed in range(3):
            r = toys.train_ntk(n, seed, steps=3000, record=(0, 30, 100, 300, 1000, 2999))
            for k in rows:
                vals[k].append(r[k])
            if seed == 0 and n in (100, 10000):
                show = show or {}
                show[n] = r
        for k in rows:
            rows[k].append(vals[k])
        print(f"    width {n}: weights moved {np.mean(vals['moved_hidden']):.4f}, kernel moved "
              f"{np.mean(vals['kernel_moved']):.4f}, gap to linear {np.mean(vals['lin_gap']):.4f}", flush=True)
    out = {k: np.array(v) for k, v in rows.items()}  # widths x seeds
    W = np.array(NTK_WIDTHS, float)
    for k in ("moved_hidden", "kernel_moved", "lin_gap"):
        out[f"slope_{k}"] = loglog_slope(W, out[k].mean(1), lo=300)
    for n, r in show.items():
        out[f"f0_{n}"], out[f"fT_{n}"], out[f"flin_{n}"] = r["f0"], r["fT"], r["flin"]
        out[f"snap_steps"] = np.array(sorted(r["snaps"]))
        out[f"snaps_{n}"] = np.array([r["snaps"][t] for t in sorted(r["snaps"])])
    out["grid"] = show[10000]["grid"]
    out["X"], out["y"] = toys.NTK_X, toys.ntk_target(toys.NTK_X)
    out["widths"] = NTK_WIDTHS
    out["truth"] = toys.ntk_target(out["grid"])
    assert out["kernel_moved"][-1].mean() < out["kernel_moved"][2].mean()  # wider: the kernel moves less
    return out


# ---------------------------------------------------------------------------
# 2. Lazy against rich
# ---------------------------------------------------------------------------
def compute_lazy():
    """Part 11's character model, wider and wider, trained by plain gradient descent with the neural-tangent step
    sizes (the hidden and output matrices' rates shrink like 1/width): how much its hidden features change."""
    import torch

    from . import charlm as L

    L.threads()
    tr_t, va_t, K = L.tensors()
    probe = L.windows(va_t, torch.arange(L.CTX, L.CTX + 2000))
    widths = [32, 64, 128, 256, 512, 1024, 2048]
    feat, moved, finals = [], [], []
    for w in widths:
        m = L.make_model(w, mup=False, seed=0)

        def features():
            with torch.no_grad():
                return m.hidden(probe)

        f0, w0 = features(), m.h2.weight.detach().clone()
        opt = torch.optim.SGD([dict(params=[*m.emb.parameters(), *m.h1.parameters()], lr=0.004),
                               dict(params=[*m.h2.parameters(), *m.out.parameters()], lr=0.5 * 64 / w)])
        st = L.Stream(7)
        for k in range(800):
            pos = st.batch(k)
            loss = torch.nn.functional.cross_entropy(m(L.windows(tr_t, pos)), tr_t[pos])
            opt.zero_grad()
            loss.backward()
            opt.step()
        finals.append(L.bits(m, va_t, 60_000))
        feat.append(float((features() - f0).norm() / f0.norm()))
        moved.append(float((m.h2.weight.detach() - w0).norm() / w0.norm()))
        print(f"    width {w}: features changed {feat[-1]:.4f}, hidden matrix moved {moved[-1]:.5f}, "
              f"held-out {finals[-1]:.3f} bits", flush=True)
    return dict(widths=widths, moved=np.array(feat), weights_moved=np.array(moved), finals=np.array(finals),
                slope=loglog_slope(widths, feat), slope_weights=loglog_slope(widths, moved))


def compute_rich():
    from . import toys

    toys_threads()
    out = {}
    for mode in ("ntk", "mf"):
        best = None
        for eta in (0.5, 2.0):  # each parametrization gets the better of two learning rates (on seed 0's test loss)
            r = toys.train_rich(mode, 0, eta=eta)
            if best is None or r["curve"][-1, 2] < best[1]:
                best = (eta, r["curve"][-1, 2])
        eta = best[0]
        runs = [toys.train_rich(mode, s, eta=eta) for s in range(3)]
        out[f"{mode}_eta"] = eta
        out[f"{mode}_curve"] = np.stack([r["curve"] for r in runs])  # seeds x checkpoints x (step, train, test, align)
        out[f"{mode}_units"] = runs[0]["units"]
        out[f"{mode}_moved"] = np.array([r["moved"] for r in runs])
        out[f"{mode}_test"] = np.array([r["curve"][-1, 2] for r in runs])
        out["var"] = runs[0]["var"]
        print(f"    {mode}: lr {eta}, test error {out[f'{mode}_test'].mean():.3f} (variance {out['var']:.3f}), "
              f"weights moved {out[f'{mode}_moved'].mean():.3f}", flush=True)
    out["kernel"] = np.array([toys.kernel_regression(s) for s in range(3)])
    print(f"    kernel regression: {out['kernel'].mean():.3f}", flush=True)
    out["width"], out["d"], out["n"] = 1024, toys.RICH_D, toys.RICH_N
    return out


def toys_threads():
    from . import charlm

    charlm.threads()


# ---------------------------------------------------------------------------
# 3. muP
# ---------------------------------------------------------------------------
COORD_WIDTHS = [64, 128, 256, 512, 1024, 2048, 4096]


def compute_coord():
    """Adam at one learning rate (0.01) for 4 steps on the same batches, at every width: the average size of each
    layer's change since initialization (std over the batch and the coordinates)."""
    import torch

    from . import charlm as L

    L.threads()
    tr_t, va_t, K = L.tensors()
    probe = L.windows(va_t, torch.arange(L.CTX, L.CTX + 1024))
    out = dict(widths=COORD_WIDTHS, steps=[1, 2, 3, 4], layers=["h1", "h2", "logits"])
    for mode in ("sp", "mup"):
        arr = np.zeros((len(COORD_WIDTHS), 4, 3))
        for i, w in enumerate(COORD_WIDTHS):
            m = L.make_model(w, mup=(mode == "mup"), seed=0)
            opt = L.adam(m, 1e-2)

            def acts():
                with torch.no_grad():
                    x = m.emb(probe).reshape(len(probe), -1)
                    a1 = torch.tanh(m.h1(x))
                    a2 = torch.tanh(m.h2(a1)) + a1
                    return a1, a2, m.out(a2) * m.mult

            a0 = acts()
            st = L.Stream(3)
            for t in range(4):
                for g in opt.param_groups:
                    g["lr"] = g["base_lr"]
                L.step_once(m, opt, st.batch(t), tr_t)
                a = acts()
                arr[i, t] = [float((x - y).std()) for x, y in zip(a, a0)]
            print(f"    {mode} width {w}: change after 4 steps " + " ".join(f"{v:.3g}" for v in arr[i, 3]), flush=True)
        out[mode] = arr
    out["slope_sp"] = loglog_slope(COORD_WIDTHS, out["sp"][:, 3, 2])
    out["slope_mup"] = loglog_slope(COORD_WIDTHS, out["mup"][:, 3, 2])
    return out


MUP_WIDTHS = [64, 256, 1024]
MUP_LRS = [float(10 ** x) for x in np.linspace(-4, -1, 11)]
MUP_STEPS = 600


def _mup_run(mode: str, w: int, lr: float, seed: int) -> float:
    from . import charlm as L

    L.threads()
    m = L.make_model(w, mup=(mode == "mup"), seed=seed)
    return L.train_run(m, lr, MUP_STEPS, L.Stream(seed))["final"]


def compute_mup():
    part = CACHE.partial("mup", dict(widths=MUP_WIDTHS, lrs=MUP_LRS, steps=MUP_STEPS, v=1))
    jobs = [(mode, w, lr, seed) for seed in (0, 1) for mode in ("sp", "mup") for w in MUP_WIDTHS for lr in MUP_LRS]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}_{j[2]:.3e}_{j[3]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_mup_run, chunk)):
            part[f"{j[0]}_{j[1]}_{j[2]:.3e}_{j[3]}"] = r
            print(f"    {j[0]} width {j[1]} lr {j[2]:.1e} seed {j[3]}: {r:.3f}", flush=True)
    out = dict(widths=MUP_WIDTHS, lrs=np.array(MUP_LRS), steps=MUP_STEPS)
    bests, best_loss = {}, {}
    for mode in ("sp", "mup"):
        for w in MUP_WIDTHS:
            v = np.array([[part[f"{mode}_{w}_{lr:.3e}_{s}"] for lr in MUP_LRS] for s in (0, 1)])
            out[f"{mode}{w}"] = v  # seeds x learning rates
        bests[mode] = [float(np.log10(MUP_LRS[int(np.nanargmin(np.nanmean(out[f'{mode}{w}'], 0)))])) for w in MUP_WIDTHS]
        best_loss[mode] = [float(np.nanmin(np.nanmean(out[f"{mode}{w}"], 0))) for w in MUP_WIDTHS]
    out["bests"], out["best_loss"] = bests, best_loss
    out["drift"] = {m: max(v) - min(v) for m, v in bests.items()}
    # the cost of tuning the small model and copying its rate: the big model's loss at the small model's best rate
    out["copy_loss"] = {}
    for mode in ("sp", "mup"):
        i_small = int(np.nanargmin(np.nanmean(out[f"{mode}{MUP_WIDTHS[0]}"], 0)))
        out["copy_loss"][mode] = float(np.nanmean(out[f"{mode}{MUP_WIDTHS[-1]}"], 0)[i_small])
    return out


DEPTHS = [2, 4, 8, 16, 32]
ALPHAS = [0.0, 0.5, 1.0]
DEPTH_LRS = [float(10 ** x) for x in np.linspace(-3.5, -1.0, 9)]
DEPTH_W, DEPTH_STEPS = 64, 400


def _depth_run(depth: int, alpha: float, lr: float, seed: int) -> float:
    from . import charlm as L

    L.threads()
    m = L.make_deep(DEPTH_W, depth, alpha, seed=seed)
    return L.train_run(m, lr, DEPTH_STEPS, L.Stream(seed))["final"]


def compute_depth():
    part = CACHE.partial("depth", dict(depths=DEPTHS, alphas=ALPHAS, lrs=DEPTH_LRS, w=DEPTH_W, steps=DEPTH_STEPS, v=1))
    jobs = [(d, a, lr, s) for s in (0, 1) for a in ALPHAS for d in DEPTHS for lr in DEPTH_LRS]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}_{j[2]:.3e}_{j[3]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_depth_run, chunk)):
            part[f"{j[0]}_{j[1]}_{j[2]:.3e}_{j[3]}"] = r
            print(f"    depth {j[0]} alpha {j[1]} lr {j[2]:.1e} seed {j[3]}: {r:.3f}", flush=True)
    out = dict(depths=DEPTHS, alphas=ALPHAS, lrs=np.array(DEPTH_LRS), width=DEPTH_W, steps=DEPTH_STEPS)
    bests, best_loss = {}, {}
    for a in ALPHAS:
        for d in DEPTHS:
            out[f"a{a}_d{d}"] = np.array([[part[f"{d}_{a}_{lr:.3e}_{s}"] for lr in DEPTH_LRS] for s in (0, 1)])
        bests[str(a)] = [float(np.log10(DEPTH_LRS[int(np.nanargmin(np.nanmean(out[f'a{a}_d{d}'], 0)))])) for d in DEPTHS]
        best_loss[str(a)] = [float(np.nanmin(np.nanmean(out[f"a{a}_d{d}"], 0))) for d in DEPTHS]
    out["bests"], out["best_loss"] = bests, best_loss
    out["drift"] = {a: max(v) - min(v) for a, v in bests.items()}
    out["copy_loss"] = {}
    for a in ALPHAS:
        i0 = int(np.nanargmin(np.nanmean(out[f"a{a}_d{DEPTHS[0]}"], 0)))
        out["copy_loss"][str(a)] = float(np.nanmean(out[f"a{a}_d{DEPTHS[-1]}"], 0)[i0])
    return out


# ---------------------------------------------------------------------------
# 4. How big a batch?
# ---------------------------------------------------------------------------
BATCHES = [32, 64, 128, 256, 512, 1024, 2048, 4096]
BATCH_W, BATCH_LR, BATCH_CHARS = 128, 4e-3, 2 ** 23
BATCH_LEVELS = [3.4, 3.0, 2.8]


def _batch_run(B: int, f: float, seed: int = 0) -> dict:
    """Constant learning rate lr(B) = f x BATCH_LR x sqrt(B / 256) (Adam's square-root rule); held-out bits every
    so often, until BATCH_CHARS characters or the lowest level is reached."""
    from . import charlm as L

    L.threads()
    tr_t, va_t, _ = L.tensors()
    m = L.make_model(BATCH_W, mup=True, seed=seed)
    lr = f * BATCH_LR * math.sqrt(B / 256)
    opt = L.adam(m, lr)
    st = L.Stream(seed)
    steps = min(BATCH_CHARS // B, 60_000)
    every = max(10, min(200, steps // 150))
    curve = []
    for s in range(steps):
        L.set_lr(opt, min(1.0, (s + 1) / L.WARMUP))
        if not math.isfinite(L.step_once(m, opt, st.batch(s, B), tr_t)):
            break
        if (s + 1) % every == 0:
            b = L.bits(m, va_t, 10_000)
            curve.append((s + 1, b))
            if b < BATCH_LEVELS[-1] - 0.02:
                break
    return dict(curve=curve, lr=lr)


def noise_scale(model, B_small=64, B_big=4096, reps=16, seed=0) -> float:
    """McCandlish et al.'s simple noise scale B = tr(Sigma) / |G|^2, from gradient norms at two batch sizes
    (their unbiased estimators, Appendix A)."""
    import torch

    from . import charlm as L

    tr_t, _, _ = L.tensors()
    g = rng(900 + seed)

    def grad_sq(B):
        pos = torch.from_numpy(g.integers(L.CTX, len(tr_t), B))
        loss = torch.nn.functional.cross_entropy(model(L.windows(tr_t, pos)), tr_t[pos])
        gr = torch.autograd.grad(loss, [p for p in model.parameters()])
        return float(sum((x ** 2).sum() for x in gr))

    gs = np.mean([grad_sq(B_small) for _ in range(reps)])
    gb = np.mean([grad_sq(B_big) for _ in range(max(2, reps // 8))])
    G2 = (B_big * gb - B_small * gs) / (B_big - B_small)
    S = (gs - gb) / (1 / B_small - 1 / B_big)
    return float(S / G2)


def compute_batch():
    part = CACHE.partial("batch", dict(b=BATCHES, w=BATCH_W, lr=BATCH_LR, chars=BATCH_CHARS, lv=BATCH_LEVELS, v=1))
    jobs = [(B, f) for B in BATCHES for f in (0.5, 1.0, 2.0)]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_batch_run, chunk)):
            part[f"{j[0]}_{j[1]}"] = r
            print(f"    batch {j[0]} x{j[1]}: {len(r['curve'])} evals, last {r['curve'][-1] if r['curve'] else None}",
                  flush=True)
    out = dict(batches=BATCHES, levels=BATCH_LEVELS, width=BATCH_W)
    S = np.full((len(BATCH_LEVELS), len(BATCHES)), np.nan)
    for j, B in enumerate(BATCHES):
        for f in (0.5, 1.0, 2.0):
            c = np.array(part[f"{B}_{f}"]["curve"])
            out[f"curve_{B}_{f}"] = c
            for i, lv in enumerate(BATCH_LEVELS):  # steps to reach the level: the best of the three rates
                if len(c) and (c[:, 1] <= lv).any():
                    k = int(np.argmax(c[:, 1] <= lv))
                    s = c[k, 0] if k == 0 else np.interp(lv, [c[k, 1], c[k - 1, 1]], [c[k, 0], c[k - 1, 0]])
                    S[i, j] = np.nanmin([S[i, j], s])
    out["S"] = S
    out["E"] = S * np.array(BATCHES)[None]
    # (S/Smin - 1)(E/Emin - 1) = 1, i.e. S = Smin (1 + Bcrit / B): a straight line in 1/B
    fits = []
    for i in range(len(BATCH_LEVELS)):
        ok = np.isfinite(S[i])
        b = np.array(BATCHES)[ok]
        A = np.stack([np.ones(ok.sum()), 1 / b], 1)
        (smin, sb), *_ = np.linalg.lstsq(A, S[i][ok], rcond=None)
        fits.append((float(smin), float(sb / smin)))
    out["Smin"] = [f[0] for f in fits]
    out["Bcrit"] = [f[1] for f in fits]
    # the noise scale, measured on a batch-256 run as its loss crosses each level
    if "noise" not in part:
        from . import charlm as L

        L.threads()
        tr_t, va_t, _ = L.tensors()
        m = L.make_model(BATCH_W, mup=True, seed=0)
        opt = L.adam(m, BATCH_LR)
        st = L.Stream(0)
        noise, i = [], 0
        for s in range(BATCH_CHARS // 256):
            L.set_lr(opt, min(1.0, (s + 1) / L.WARMUP))
            L.step_once(m, opt, st.batch(s), tr_t)
            if (s + 1) % 50 == 0 and L.bits(m, va_t, 10_000) <= BATCH_LEVELS[i]:
                noise.append(noise_scale(m, seed=i))
                print(f"    noise scale at {BATCH_LEVELS[i]} bits: {noise[-1]:.0f}", flush=True)
                i += 1
                if i == len(BATCH_LEVELS):
                    break
        part["noise"] = noise + [float("nan")] * (len(BATCH_LEVELS) - len(noise))
    out["noise"] = np.array(part["noise"])
    return out


# ---------------------------------------------------------------------------
# 5. The scaling sweep
# ---------------------------------------------------------------------------
SWEEP_WIDTHS = [16, 32, 64, 96, 128, 192, 256, 384, 512, 768, 1024]
SWEEP_KS = list(range(16, 25))  # training lengths 2^16 ... 2^24 characters
SWEEP_KMAX = {768: 22, 1024: 21}  # the widest models stop at about 2 x 10^13 operations
SWEEP_EXTRA = [(64, 1), (64, 2), (256, 1), (256, 2)]  # (width, seed) repeats, up to 2^22 characters
PTQ_BITS = [8, 6, 5, 4, 3]
SWEEP_LRS = [1e-3, 2e-3, 4e-3, 8e-3, 1.6e-2]


def _sweep_lr() -> float:
    """The one learning rate of the sweep: the best of five at the base width (64) on 2^21 characters. muP carries it
    to every other width (chapter 4)."""
    part = CACHE.partial("sweep_lr", dict(lrs=SWEEP_LRS, v=1))
    from . import charlm as L

    for lr in SWEEP_LRS:
        if f"{lr:g}" not in part:
            L.threads()
            r = L.train_run(L.make_model(64, mup=True, seed=0), lr, 2 ** 21 // L.BATCH, L.Stream(0))["final"]
            part[f"{lr:g}"] = r
            print(f"    sweep learning rate {lr:g}: {r:.4f} bits", flush=True)
    res = {lr: part[f"{lr:g}"] for lr in SWEEP_LRS}
    return min(res, key=lambda k: res[k]), res


def _evaluate(m) -> dict:
    from . import charlm as L

    out = dict(bits=L.bits(m), fp30=L.bits(m, n=30_000))
    out["ptq"] = [L.quantized_bits(m, b) for b in PTQ_BITS]
    out.update(L.task_scores(m))
    return out


def _sweep_width(w: int, seed: int, kmax: int, lr: float, part) -> None:
    """One width: a constant-rate trunk, and at 0.8 x 2^k characters a branch that decays the rate to zero by 2^k
    (so each endpoint is exactly a warmup-stable-decay run of 2^k characters). Resumable at every branch."""
    import torch

    from . import charlm as L

    L.threads()
    tr_t, va_t, _ = L.tensors()
    ks = [k for k in SWEEP_KS if k <= kmax]
    keys = {k: f"s{seed}_w{w}_k{k}" for k in ks}
    if all(v in part for v in keys.values()) and f"curve_s{seed}_w{w}" in part:
        return
    parts_dir = CACHE.dir / "sweep_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    ckpt = CACHE.dir / f"sweep_s{seed}_w{w}.ckpt.pt"
    m = L.make_model(w, mup=True, seed=seed)
    opt = L.adam(m, lr)
    st = L.Stream(seed)
    forks = {int(round((1 - L.COOL) * 2 ** k / L.BATCH)): k for k in ks}
    last = max(forks)
    curve_at = sorted({int(round(2 ** (e / 4))) for e in range(16, 4 * int(math.log2(last)) + 1)} | {last})
    start, curve = 0, []
    if ckpt.exists():
        z = torch.load(ckpt, weights_only=False)
        m.load_state_dict(z["model"])
        opt.load_state_dict(z["opt"])
        start, curve = z["step"], z["curve"]
        print(f"    width {w} seed {seed}: resuming at step {start}", flush=True)
    t0 = time.time()
    for s in range(start, last + 1):
        if s in forks and keys[forks[s]] not in part:
            k = forks[s]
            S = 2 ** k // L.BATCH
            ms, os_ = copy.deepcopy(m.state_dict()), copy.deepcopy(opt.state_dict())
            tb = time.time()
            for t in range(s, S):
                L.set_lr(opt, L.lr_factor(t, S, decay_from=s))
                L.step_once(m, opt, st.batch(t), tr_t)
            ev = _evaluate(m)
            np.savez_compressed(parts_dir / f"{keys[k]}.npz", logp=ev.pop("logp").astype(np.float16), top=ev.pop("top"),
                                greedy=ev.pop("greedy"))
            ev.update(secs=time.time() - tb, n_params=L.n_params(m))
            part[keys[k]] = ev
            print(f"    width {w} seed {seed}, 2^{k} characters: {ev['bits']:.4f} bits "
                  f"(4-bit {ev['ptq'][3]:.3f}) [{time.time() - t0:.0f}s]", flush=True)
            m.load_state_dict(ms)
            opt.load_state_dict(os_)
            torch.save(dict(model=m.state_dict(), opt=opt.state_dict(), step=s, curve=curve), ckpt)
        if s == last:
            break
        L.set_lr(opt, min(1.0, (s + 1) / L.WARMUP))
        L.step_once(m, opt, st.batch(s), tr_t)
        if s + 1 in curve_at:
            curve.append((s + 1, L.bits(m, va_t, 20_000)))
    part[f"curve_s{seed}_w{w}"] = dict(curve=curve, secs=time.time() - t0)
    ckpt.unlink(missing_ok=True)


def compute_sweep():
    from . import charlm as L

    lr, lr_trials = _sweep_lr()
    part = CACHE.partial("sweep", dict(widths=SWEEP_WIDTHS, ks=SWEEP_KS, kmax=SWEEP_KMAX, extra=SWEEP_EXTRA, lr=lr,
                                       ptq=PTQ_BITS, v=1))
    runs = [(w, 0, SWEEP_KMAX.get(w, 24)) for w in SWEEP_WIDTHS] + [(w, s, 22) for w, s in SWEEP_EXTRA]
    for w, seed, kmax in runs:
        _sweep_width(w, seed, kmax, lr, part)
    nW, nK = len(SWEEP_WIDTHS), len(SWEEP_KS)
    out = dict(widths=SWEEP_WIDTHS, ks=SWEEP_KS, D=np.array([2.0 ** k for k in SWEEP_KS]), lr=lr,
               lr_trials={f"{k:g}": v for k, v in lr_trials.items()}, ptq_bits=PTQ_BITS, batch=L.BATCH,
               task_n=L.TASK_N, task_len=L.TASK_LEN, extra=SWEEP_EXTRA)
    bits = np.full((nW, nK), np.nan)
    fp30 = np.full((nW, nK), np.nan)
    ptq = np.full((nW, nK, len(PTQ_BITS)), np.nan)
    logp = np.full((nW, nK, L.TASK_N, L.TASK_LEN), np.nan, np.float32)
    top = np.zeros((nW, nK, L.TASK_N, L.TASK_LEN), bool)
    greedy = np.zeros((nW, nK, L.TASK_N, L.TASK_LEN), bool)
    secs = 0.0
    N = []
    for i, w in enumerate(SWEEP_WIDTHS):
        for j, k in enumerate(SWEEP_KS):
            key = f"s0_w{w}_k{k}"
            if key not in part:
                continue
            e = part[key]
            bits[i, j], fp30[i, j], ptq[i, j] = e["bits"], e["fp30"], e["ptq"]
            z = np.load(CACHE.dir / "sweep_parts" / f"{key}.npz")
            logp[i, j], top[i, j], greedy[i, j] = z["logp"], z["top"], z["greedy"]
        N.append(part[f"s0_w{w}_k16"]["n_params"])
        c = part[f"curve_s0_w{w}"]
        out[f"curve{w}"] = np.array(c["curve"])
        secs += c["secs"]
    out.update(N=np.array(N, float), bits=bits, fp30=fp30, ptq=ptq, logp=logp, top=top, greedy=greedy)
    for w, s in SWEEP_EXTRA:
        out[f"seed{s}_w{w}"] = np.array([part[f"s{s}_w{w}_k{k}"]["bits"] if k <= 22 else np.nan for k in SWEEP_KS])
        secs += part[f"curve_s{s}_w{w}"]["secs"]
    out["secs"] = secs
    out["flops"] = 6 * out["N"][:, None] * out["D"][None]
    return out


# ---------------------------------------------------------------------------
# 6. Chinchilla's three methods, on the sweep
# ---------------------------------------------------------------------------
def fit_lnd(N, D, L, inits=None, delta=1e-3):
    """Chinchilla's approach 3: L(N, D) = E + A/N^alpha + B/D^beta, fitted by minimizing a Huber loss on log L with
    L-BFGS from a grid of starting points (Hoffmann et al. 2022, appendix D.2). Returns (E, A, alpha, B, beta)."""
    from scipy.optimize import minimize
    from scipy.special import logsumexp

    lN, lD, lL = np.log(N), np.log(D), np.log(L)

    def huber(r):
        a = np.abs(r)
        return np.where(a <= delta, 0.5 * r * r, delta * (a - 0.5 * delta))

    def obj(p):
        a, b, e, al, be = p
        pred = logsumexp(np.stack([a - al * lN, b - be * lD, np.full_like(lN, e)]), axis=0)
        return huber(pred - lL).sum()

    best = None
    grid = inits or [(a, b, e, al, be) for a in (0, 5, 10) for b in (0, 5, 10) for e in (-0.5, 0.5, 1.0)
                     for al in (0.2, 0.5, 0.8) for be in (0.2, 0.5, 0.8)]
    for p0 in grid:
        r = minimize(obj, p0, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    a, b, e, al, be = best.x
    return float(math.exp(e)), float(math.exp(a)), float(al), float(math.exp(b)), float(be)


def lnd(p, N, D):
    E, A, al, B, be = p
    return E + A * np.asarray(N, float) ** -al + B * np.asarray(D, float) ** -be


def optimum(p, C):
    """argmin over N of L(N, C/6N): N_opt = G (C/6)^(beta/(alpha+beta)), G = (alpha A / beta B)^(1/(alpha+beta))."""
    E, A, al, B, be = p
    G = (al * A / (be * B)) ** (1 / (al + be))
    Nopt = G * (np.asarray(C, float) / 6) ** (be / (al + be))
    return Nopt, np.asarray(C, float) / 6 / Nopt


BUDGETS = [1e11, 3e11, 1e12, 3e12, 1e13]
FIT_KMIN, FIT_WMIN = 19, 64  # the runs Chinchilla's formula is fitted to
EXTRAP_CUT = 3e12


def power_floor(x, y):
    """y = E + A x^-a, fitted by least squares on a grid of exponents (E and A are linear given a)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    best = None
    for a in np.linspace(0.02, 1.5, 740):
        M = np.stack([np.ones_like(x), x ** -a], 1)
        (E, A), *_ = np.linalg.lstsq(M, y, rcond=None)
        if A <= 0:
            continue
        r = float(np.sum((M @ np.array([E, A]) - y) ** 2))
        if best is None or r < best[0]:
            best = (r, float(E), float(A), float(a))
    return dict(E=best[1], A=best[2], a=best[3], rms=float(math.sqrt(best[0] / len(x))))


def isoflop_points(s, C, N=None):
    """For one budget, each width's loss at D = C/(6N), read off its cooled endpoints (linear in log D between the
    two nearest lengths; only inside the measured range)."""
    N = s["N"] if N is None else N
    lD = np.log2(s["D"])
    pts = []
    for i in range(len(N)):
        d = math.log2(C / 6 / N[i])
        row = s["bits"][i]
        ok = np.isfinite(row)
        if ok.sum() < 2 or d < lD[ok].min() or d > lD[ok].max():
            continue
        pts.append((N[i], C / 6 / N[i], float(np.interp(d, lD[ok], row[ok]))))
    return np.array(pts)


def parabola_min(pts):
    """The vertex of a parabola in log N through the lowest point and its neighbours (Chinchilla's approach 2)."""
    if len(pts) < 3:
        return float("nan"), float("nan")
    lN, Lv = np.log10(pts[:, 0]), pts[:, 2]
    i = int(np.argmin(Lv))
    sl = slice(max(0, i - 2), min(len(Lv), i + 3))
    a2, a1, a0 = np.polyfit(lN[sl], Lv[sl], 2)
    if a2 <= 0:
        return float(10 ** lN[i]), float(Lv[i])
    x = -a1 / (2 * a2)
    return float(10 ** x), float(np.polyval([a2, a1, a0], x))


def compute_chinchilla():
    s = load("sweep")
    N, D, Lb = np.asarray(s["N"]), np.asarray(s["D"]), np.asarray(s["bits"])
    widths = list(s["widths"])
    # the fits use runs of at least 2^19 characters (256 optimizer steps: shorter ones are mostly warmup) and widths
    # of 64 and up (the two narrowest are mostly embedding and output layer)
    use = np.isfinite(Lb) & (D[None] >= 2 ** FIT_KMIN) & (np.array(widths)[:, None] >= FIT_WMIN)
    if use.sum() < 12:  # a test-sized sweep
        use = np.isfinite(Lb) & (D[None] >= 2 ** 17)
    ii, jj = np.where(use)
    Np, Dp, Lp = N[ii], D[jj], Lb[ii, jj]
    p = fit_lnd(Np, Dp, Lp)
    E, A, al, B, be = p
    rms = float(np.sqrt(np.mean((lnd(p, Np, Dp) - Lp) ** 2)))
    a3 = be / (al + be)
    out = dict(E=E, A=A, alpha=al, B=B, beta=be, a3=a3, rms=rms, n_points=int(len(Lp)), budgets=BUDGETS,
               fit_kmin=FIT_KMIN, fit_wmin=FIT_WMIN, fit_N=Np, fit_D=Dp, fit_L=Lp)
    # bootstrap: the spread of the exponent a
    g = rng(2024)
    boot = []
    for _ in range(100):
        k = g.integers(0, len(Lp), len(Lp))
        q = fit_lnd(Np[k], Dp[k], Lp[k], inits=[(math.log(A), math.log(B), math.log(E), al, be)])
        boot.append(q[4] / (q[2] + q[4]))
    out["a3_lo"], out["a3_hi"] = float(np.percentile(boot, 10)), float(np.percentile(boot, 90))
    # approach 2: iso-FLOP valleys
    nopt2, lopt2 = [], []
    for C in BUDGETS:
        pts = isoflop_points(s, C)
        out[f"iso{C:.0e}"] = pts
        n_, l_ = parabola_min(pts)
        nopt2.append(n_)
        lopt2.append(l_)
    out["nopt2"], out["lopt2"] = np.array(nopt2), np.array(lopt2)
    ok2 = np.isfinite(out["nopt2"])
    out["a2"] = loglog_slope(np.array(BUDGETS)[ok2], out["nopt2"][ok2])
    out["tpp2"] = [C / 6 / n / n for C, n in zip(BUDGETS, nopt2)]
    # approach 1: the envelope of all endpoints by compute; the width that is lowest at each compute
    Cs = np.geomspace(3e10, 3e13, 25)
    env_n, env_l = [], []
    for C in Cs:
        pts = isoflop_points(s, C)
        if len(pts) < 3:
            env_n.append(np.nan)
            env_l.append(np.nan)
            continue
        i = int(np.argmin(pts[:, 2]))
        env_n.append(pts[i, 0])
        env_l.append(pts[i, 2])
    env_n, env_l = np.array(env_n), np.array(env_l)
    ok = np.isfinite(env_n)
    out["env_C"], out["env_N"], out["env_L"] = Cs, env_n, env_l
    out["a1"] = loglog_slope(Cs[ok], env_n[ok])
    out["env_slope"] = loglog_slope(Cs[ok], env_l[ok] - E)  # the frontier: L - E ~ C^slope
    # one variable at a time, Kaplan's way: L(N) at the longest training, L(D) for the widest model trained that long
    jmax = len(D) - 1
    colN = np.isfinite(Lb[:, jmax])
    out["LN_N"], out["LN_L"] = N[colN], Lb[colN, jmax]
    out["LN_fit"] = power_floor(N[colN], Lb[colN, jmax])
    iw = int(np.where(colN)[0].max())
    rowD = np.isfinite(Lb[iw]) & (D >= 2 ** 17)
    out["LD_w"], out["LD_D"], out["LD_L"] = widths[iw], D[rowD], Lb[iw, rowD]
    out["LD_fit"] = power_floor(D[rowD], Lb[iw, rowD])
    # the fitted law's optimum per budget
    n3, d3 = optimum(p, np.array(BUDGETS))
    out["nopt3"], out["dopt3"] = n3, d3
    out["tpp3"] = float(np.mean(d3 / n3))
    out["lopt3"] = lnd(p, n3, d3)
    # Kaplan's way: counting only the parameters outside the embedding and the output layer
    K = 167
    Nne = np.array([w * w + 130 * w for w in widths], float)  # h1 (128 x w + w) and h2 (w x w + w)
    out["N_nonemb"] = Nne
    nk = []
    for C in BUDGETS:
        pts = isoflop_points(s, C)  # the same runs, the same budgets in operations
        n_, _ = parabola_min(pts)
        nk.append(math.exp(np.interp(math.log(n_), np.log(N), np.log(Nne))) if np.isfinite(n_) else float("nan"))
    out["nopt_kaplan"] = np.array(nk)
    out["a_kaplan_count"] = loglog_slope(np.array(BUDGETS)[ok2], out["nopt_kaplan"][ok2])
    out["emb_share"] = [float(1 - a / b) for a, b in zip(Nne, N)]
    # extrapolation: fit only the runs that cost at most 3 x 10^12 operations (about half of them), predict the rest
    cut = EXTRAP_CUT if (6 * Np * Dp > EXTRAP_CUT).sum() >= 5 else float(np.median(6 * Np * Dp))  # (median: a test run)
    cheap = 6 * Np * Dp <= cut
    out["extrap_cut"] = cut
    out["extrap_ratio"] = float(np.max(6 * Np * Dp) / cut)
    pc = fit_lnd(Np[cheap], Dp[cheap], Lp[cheap])
    pred = lnd(pc, Np[~cheap], Dp[~cheap])
    out["cheap"] = dict(E=pc[0], A=pc[1], alpha=pc[2], B=pc[3], beta=pc[4], n=int(cheap.sum()))
    out["extrap_err"] = float(np.mean(np.abs(pred - Lp[~cheap])))
    out["extrap_max"] = float(np.max(np.abs(pred - Lp[~cheap])))
    out["extrap_n"] = int((~cheap).sum())
    out["extrap_pts"] = np.stack([Np[~cheap], Dp[~cheap], Lp[~cheap], pred], 1)
    out["extrap_bias"] = float(np.mean(pred - Lp[~cheap]))
    nC, dC = optimum(pc, 1e13)
    out["extrap_opt"] = dict(N=float(nC), D=float(dC), pred=float(lnd(pc, nC, dC)), meas=float(np.array(lopt2)[ok2][-1]))
    # over-training priced by the fit: a model k times the optimal size reaching the optimum's loss (at 10^12
    # operations, where the sweep also has smaller models trained long enough to check it)
    C0 = 1e12
    n0, d0 = optimum(p, C0)
    L0 = float(lnd(p, n0, d0))
    kmin = float((A / (L0 - E)) ** (1 / al) / n0)
    ks = np.linspace(max(kmin * 1.02, 0.15), 1.0, 60)
    cost = []
    for k in ks:
        r = L0 - E - A * (k * n0) ** -al
        cost.append(6 * k * n0 * (B / r) ** (1 / be) / C0)
    out.update(ot_k=ks, ot_cost=np.array(cost), ot_kmin=kmin, ot_N0=float(n0), ot_D0=float(d0), ot_L0=L0, ot_C=C0)
    # with inference: minimize 6 N D + 2 N T over (N, D) on the level set L(N, D) = L0, for T inference characters
    Ts = np.geomspace(1e5, 1e11, 61)
    best_tpp, best_N, total_saving = [], [], []
    for T in Ts:
        Ngrid = np.geomspace(kmin * n0 * 1.001, n0 * 1.5, 400)
        r = L0 - E - A * Ngrid ** -al
        ok_ = r > 0
        Dg = (B / r[ok_]) ** (1 / be)
        tot = 6 * Ngrid[ok_] * Dg + 2 * Ngrid[ok_] * T
        i = int(np.argmin(tot))
        best_tpp.append(Dg[i] / Ngrid[ok_][i])
        best_N.append(Ngrid[ok_][i] / n0)
        total_saving.append(1 - tot[i] / (6 * n0 * d0 + 2 * n0 * T))
    out.update(inf_T=Ts, inf_tpp=np.array(best_tpp), inf_N=np.array(best_N), inf_saving=np.array(total_saving))
    # measured: endpoints of the sweep that land within 0.01 bits of the 10^12 optimum, smaller and longer-trained
    C1 = 1e12
    lo = float(np.interp(math.log(C1), np.log(np.array(BUDGETS)[ok2]), np.array(lopt2)[ok2]))
    match = []
    for i in range(len(N)):
        row = Lb[i]
        ok_ = np.isfinite(row)
        if ok_.sum() < 2 or row[ok_].min() > lo:
            continue
        lD = np.log2(D[ok_])
        r_ = row[ok_]
        j = int(np.argmax(r_ <= lo))
        if j == 0:
            continue
        dd = 2 ** np.interp(lo, [r_[j], r_[j - 1]], [lD[j], lD[j - 1]])
        match.append((N[i], dd, 6 * N[i] * dd / C1))
    out["matched"] = np.array(match)
    out["matched_L"] = lo
    return out


# ---------------------------------------------------------------------------
# 7. When the data runs out
# ---------------------------------------------------------------------------
REPEAT_W, REPEAT_K = 128, 22
REPEAT_UNIQUE = [22, 20, 18, 16, 14]  # 2^u distinct characters: 1, 4, 16, 64, 256 epochs


def _repeat_run(u: int, seed: int) -> dict:
    from . import charlm as L

    L.threads()
    S = 2 ** REPEAT_K // L.BATCH
    m = L.make_model(REPEAT_W, mup=True, seed=seed)
    lr = load("sweep")["lr"]
    at = set(np.unique(np.geomspace(64, S, 24).astype(int)))
    r = L.train_run(m, float(lr), S, L.Stream(seed, subset=2 ** u), eval_at=at)
    return dict(final=r["final"], curve=r["curve"])


def compute_repeat():
    s = load("sweep")
    part = CACHE.partial("repeat", dict(w=REPEAT_W, k=REPEAT_K, u=REPEAT_UNIQUE, lr=float(s["lr"]), v=1))
    jobs = [(u, seed) for seed in (0, 1, 2) for u in REPEAT_UNIQUE]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_repeat_run, chunk)):
            part[f"{j[0]}_{j[1]}"] = r
            print(f"    2^{j[0]} distinct, seed {j[1]}: {r['final']:.4f} bits", flush=True)
    out = dict(width=REPEAT_W, total=2 ** REPEAT_K, unique=[2 ** u for u in REPEAT_UNIQUE],
               epochs=[2 ** (REPEAT_K - u) for u in REPEAT_UNIQUE])
    fin = np.array([[part[f"{u}_{sd}"]["final"] for sd in (0, 1, 2)] for u in REPEAT_UNIQUE])
    out["final"] = fin
    for u in REPEAT_UNIQUE:
        out[f"curve{u}"] = np.array(part[f"{u}_0"]["curve"])
    # fresh data at the same width, from the sweep: L(D) for one pass over D distinct characters
    i = _nearest(s["widths"], REPEAT_W)
    fresh = np.asarray(s["bits"])[i]
    lD = np.log2(np.asarray(s["D"]))
    out["fresh"], out["fresh_D"] = fresh, np.asarray(s["D"])
    # the effective data of each repeated run: the fresh D that gives its loss
    eff = []
    okf = np.isfinite(fresh)
    order = np.argsort(fresh[okf])  # ascending loss (descending D), as np.interp needs
    for row in fin.mean(1):
        if row <= np.nanmin(fresh):  # as good as the longest fresh run, or better
            eff.append(2.0 ** lD[okf][order][0])
        elif row > np.nanmax(fresh):  # worse than the shortest fresh run: off the curve
            eff.append(float("nan"))
        else:
            eff.append(float(2 ** np.interp(row, fresh[okf][order], lD[okf][order])))
    eff = np.array(eff)
    out["effective"] = eff
    # Muennighoff et al.: D' = U + U R* (1 - exp(-R/R*)), R = epochs - 1; fit R* to the runs on the fresh curve
    U = np.array(out["unique"], float)
    R = np.array(out["epochs"], float) - 1
    rs = np.geomspace(0.3, 300, 2000)
    errs = [np.nansum((np.log(U + U * r * (1 - np.exp(-R / r))) - np.log(eff)) ** 2) for r in rs]
    out["Rstar"] = float(rs[int(np.argmin(errs))])
    out["Rstar_paper"] = 15.387756
    return out


# ---------------------------------------------------------------------------
# 8. Experts and bits
# ---------------------------------------------------------------------------
MOE_E = [1, 2, 4, 8, 16, 32]
MOE_W, MOE_K = 128, 21


def _moe_run(E: int, seed: int) -> dict:
    from . import charlm as L

    L.threads()
    m = L.make_model(MOE_W, mup=True, experts=E, seed=seed)
    lr = float(load("sweep")["lr"])
    r = L.train_run(m, lr, 2 ** MOE_K // L.BATCH, L.Stream(seed))
    load_ = m.load.numpy().tolist() if E > 1 else [1.0]
    return dict(final=r["final"], total=L.n_params(m), active=L.active_params(m), load=load_)


def compute_moe():
    s = load("sweep")
    part = CACHE.partial("moe", dict(E=MOE_E, w=MOE_W, k=MOE_K, lr=float(s["lr"]), v=1))
    jobs = [(E, seed) for seed in (0, 1) for E in MOE_E]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_moe_run, chunk)):
            part[f"{j[0]}_{j[1]}"] = r
            print(f"    {j[0]} experts, seed {j[1]}: {r['final']:.4f} bits ({r['total']} parameters)", flush=True)
    out = dict(E=MOE_E, width=MOE_W, chars=2 ** MOE_K)
    out["final"] = np.array([[part[f"{E}_{sd}"]["final"] for sd in (0, 1)] for E in MOE_E])
    out["total"] = np.array([part[f"{E}_0"]["total"] for E in MOE_E], float)
    out["active"] = np.array([part[f"{E}_0"]["active"] for E in MOE_E], float)
    # dense models at the same training length, from the sweep: the dense size that matches each mixture's loss
    j = _nearest(s["ks"], MOE_K)
    dense = np.asarray(s["bits"])[:, j]
    Nd = np.asarray(s["N"])
    out["dense_N"], out["dense_L"] = Nd, dense
    order = np.argsort(dense)[::-1]
    eff = [float(np.exp(np.interp(v, dense[order], np.log(Nd[order])))) for v in out["final"].mean(1)]
    out["effective_N"] = np.array(eff)
    out["slope"] = loglog_slope(np.array(MOE_E[1:]), out["final"].mean(1)[1:] - float(load("chinchilla")["E"]))
    return out


def compute_precision():
    s = load("sweep")
    ptq, fp = np.asarray(s["ptq"]), np.asarray(s["fp30"])
    delta = ptq - fp[..., None]  # widths x lengths x bits
    N, D = np.asarray(s["N"]), np.asarray(s["D"])
    out = dict(bits=s["ptq_bits"], delta=delta, N=N, D=D, widths=s["widths"])
    # Kumar et al.'s form: delta = C (D^gD / N^gN) exp(-P / gpost), fitted on log delta where delta > 0.002 bits
    rows = []
    for i in range(len(N)):
        for j in range(len(D)):
            for b, P in enumerate(s["ptq_bits"]):
                v = delta[i, j, b]
                if np.isfinite(v) and v > 0.002 and D[j] >= 2 ** 17:
                    rows.append((math.log(N[i]), math.log(D[j]), P, math.log(v)))
    R = np.array(rows)
    A = np.stack([np.ones(len(R)), R[:, 1], -R[:, 0], -R[:, 2]], 1)
    coef, *_ = np.linalg.lstsq(A, R[:, 3], rcond=None)
    out.update(logC=float(coef[0]), gD=float(coef[1]), gN=float(coef[2]), gpost=float(1 / coef[3]), n_fit=len(R))
    # at fixed width (256), how the 4-bit penalty grows with training length
    i = _nearest(s["widths"], 256)
    out["d4_w256"] = delta[i, :, PTQ_BITS.index(4)]
    out["post4_w256"] = ptq[i, :, PTQ_BITS.index(4)]
    out["fp_w256"] = fp[i]
    return out


# ---------------------------------------------------------------------------
# 9. Why power laws
# ---------------------------------------------------------------------------
QUANTA_W = [8, 16, 32, 64, 128, 256, 512]


def _quanta_run(w: int, seed: int) -> dict:
    from . import charlm, toys

    charlm.threads()
    r = toys.train_quanta(w, seed, steps=20000, lr=3e-3)
    return dict(steps=r["steps"].tolist(), per_task=r["per_task"].tolist(), n_params=r["n_params"])


def compute_quanta():
    from . import toys

    part = CACHE.partial("quanta", dict(w=QUANTA_W, tasks=toys.QT_TASKS, bits=toys.QT_BITS, a=toys.QT_ALPHA, v=1))
    jobs = [(w, s) for s in (0, 1) for w in QUANTA_W]
    todo = [j for j in jobs if f"{j[0]}_{j[1]}" not in part]
    for i in range(0, len(todo), max(1, _workers())):
        chunk = todo[i:i + max(1, _workers())]
        for j, r in zip(chunk, _pmap(_quanta_run, chunk)):
            part[f"{j[0]}_{j[1]}"] = r
            pt = np.array(r["per_task"])
            print(f"    width {j[0]} seed {j[1]}: {(pt[-1] < 0.1).sum()} subtasks learned", flush=True)
    S, p = toys.quanta_tasks()
    out = dict(widths=QUANTA_W, p=p, tasks=toys.QT_TASKS, bits=toys.QT_BITS, k=toys.QT_K, alpha=toys.QT_ALPHA)
    out["steps"] = np.array(part[f"{QUANTA_W[0]}_0"]["steps"])
    per = np.array([[part[f"{w}_{s}"]["per_task"] for s in (0, 1)] for w in QUANTA_W])  # W x seeds x T x tasks
    out["per_task"] = per
    out["mean"] = (per * p).sum(-1)  # W x seeds x T: the test loss averaged over the Zipfian task mix
    out["n_params"] = np.array([part[f"{w}_0"]["n_params"] for w in QUANTA_W], float)
    out["learned"] = (per[:, :, -1] < 0.1).sum(-1)
    fin = out["mean"][:, :, -1].mean(1)
    out["slope_N"] = loglog_slope(out["n_params"], fin)
    # the theory: n quanta learned leaves the loss sum_{k > n} p_k (one bit each), ~ n^-alpha
    out["theory"] = np.array([p[n:].sum() for n in range(toys.QT_TASKS + 1)])
    return out


MANIFOLD_D = [1, 2, 4, 8]
MANIFOLD_N = [2 ** k for k in range(4, 18)]


def compute_manifold():
    from . import toys

    out = dict(dims=MANIFOLD_D, pieces=MANIFOLD_N)
    for d in MANIFOLD_D:
        e = np.array([[toys.manifold_error(d, n, seed=s) for n in MANIFOLD_N] for s in range(2)])
        out[f"err{d}"] = e
        out[f"slope{d}"] = loglog_slope(np.array(MANIFOLD_N[-6:], float), e.mean(0)[-6:])
        print(f"    d = {d}: slope {out[f'slope{d}']:.2f} (theory {-4 / d:.2f})", flush=True)
    return out


# ---------------------------------------------------------------------------
# 10. Emergence, and many tries
# ---------------------------------------------------------------------------
def compute_emerge():
    s = load("sweep")
    j = _nearest(s["ks"], 22)  # every width at the same training length, 2^22 characters (those trained that long)
    have = np.isfinite(np.asarray(s["bits"], float)[:, j])
    lp, top, gr = (np.asarray(s["logp"], float)[have, j], np.asarray(s["top"])[have, j], np.asarray(s["greedy"])[have, j])
    N = np.asarray(s["N"])[have]
    out = dict(N=N, chars=2 ** 22, task_n=int(s["task_n"]), lens=list(range(1, int(s["task_len"]) + 1)))
    out["char_loss"] = -lp.mean((1, 2)) / math.log(2)  # bits per character on the task, teacher-forced
    out["char_acc"] = top.mean((1, 2))
    out["exact"] = gr.mean(1)  # widths x lengths: greedy decoding writes all L characters right
    out["prefix"] = gr.sum(2).mean(1)  # how many characters of the 8 are right before the first mistake
    out["sample_exact"] = np.exp(np.cumsum(lp, axis=2)).mean(1)  # sampling at temperature 1: P(all L right)
    # the "mirage" arithmetic: exact match of L characters if every character were right independently with p
    out["indep"] = out["char_acc"][:, None] ** np.array(out["lens"])[None]
    # sharpness: the share of the whole rise (smallest to largest model) made in the top third of the size range
    lN = np.log(N)
    top3 = lN >= lN.min() + 2 / 3 * (lN.max() - lN.min())
    i_top = int(np.argmax(top3))

    def share(v):
        return float((v[-1] - v[i_top - 1]) / (v[-1] - v[0])) if v[-1] != v[0] else float("nan")

    out["share_acc"] = share(out["char_acc"])
    out["share_exact8"] = share(out["exact"][:, -1])
    out["share_exact4"] = share(out["exact"][:, 3])
    return out


TT_LEN = 6
TT_K = np.unique(np.round(np.geomspace(1, 1e5, 61)).astype(int))


def compute_testtime():
    s = load("sweep")
    j = _nearest(s["ks"], 22)
    have = np.isfinite(np.asarray(s["bits"], float)[:, j])
    lp = np.asarray(s["logp"], float)[have, j, :, :TT_LEN].sum(-1)  # widths x problems: log P(a sample is exactly right)
    p = np.exp(lp)
    N = np.asarray(s["N"])[have]
    ks = TT_K.astype(float)
    cov = np.stack([1 - np.mean(np.exp(ks[:, None] * np.log1p(-np.minimum(pi, 1 - 1e-12))[None]), axis=1) for pi in p])
    out = dict(N=N, k=ks, length=TT_LEN, coverage=cov, p1=p.mean(1), task_n=p.shape[1])
    # -log pass@k ~ A k^-b at large k; and the left tail of the per-problem success rates
    b, A = [], []
    for i in range(len(N)):
        y = -np.log(cov[i])
        sel = (ks >= 30) & (y > 1e-4)
        if sel.sum() >= 4:
            c = np.polyfit(np.log(ks[sel]), np.log(y[sel]), 1)
            b.append(-float(c[0]))
            A.append(float(np.exp(c[1])))
        else:
            b.append(float("nan"))
            A.append(float("nan"))
    out["b"], out["A"] = np.array(b), np.array(A)
    # the tail: the share of problems with success rate below x, ~ x^b for small x (Schaeffer et al. 2025)
    xs = np.geomspace(1e-7, 1e-1, 25)
    out["tail_x"] = xs
    out["tail"] = np.array([[float((pi < x).mean()) for x in xs] for pi in p])
    tb = []
    for i in range(len(N)):
        sel = (out["tail"][i] > 0.02) & (out["tail"][i] < 0.5)
        tb.append(loglog_slope(xs[sel], out["tail"][i][sel]) if sel.sum() >= 3 else float("nan"))
    out["tail_b"] = np.array(tb)
    out["logp"] = lp
    # equal inference compute: each try costs 2 N operations per character; the best width per budget
    F = np.geomspace(1e6, 1e12, 25)
    best_i, best_cov = [], []
    for f in F:
        cv = []
        for i in range(len(N)):
            k = f / (2 * N[i] * TT_LEN)
            cv.append(np.interp(math.log(max(k, 1e-9)), np.log(ks), cov[i]) if k >= 1 else np.nan)
        cv = np.array(cv)
        best_i.append(int(np.nanargmax(cv)) if np.isfinite(cv).any() else -1)
        best_cov.append(float(np.nanmax(cv)) if np.isfinite(cv).any() else float("nan"))
    out["F"], out["F_best"], out["F_cov"] = F, np.array(best_i), np.array(best_cov)
    # how many tries a small model needs to match the biggest model's single try
    big = float(cov[-1, 0])
    need = []
    for i in range(len(N)):
        c = cov[i]
        need.append(float(np.exp(np.interp(big, c, np.log(ks)))) if c.max() >= big else float("nan"))
    out["tries_to_match"] = np.array(need)
    return out


# ---------------------------------------------------------------------------
# 11. Grokking
# ---------------------------------------------------------------------------
def compute_grok():
    from . import grok

    return grok.compute(CACHE)


ITEMS = {
    "nngp": compute_nngp,
    "ntk": compute_ntk,
    "lazy": compute_lazy,
    "rich": compute_rich,
    "coord": compute_coord,
    "mup": compute_mup,
    "depth": compute_depth,
    "batch": compute_batch,
    "sweep": compute_sweep,
    "chinchilla": compute_chinchilla,
    "repeat": compute_repeat,
    "moe": compute_moe,
    "precision": compute_precision,
    "quanta": compute_quanta,
    "manifold": compute_manifold,
    "emerge": compute_emerge,
    "testtime": compute_testtime,
    "grok": compute_grok,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
