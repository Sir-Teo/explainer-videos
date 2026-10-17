"""Precompute everything numerical in Part 19 of the AI series ("Inference").

    python -m videos.ai.ai19.compute              # everything missing (Part 11's transformer, Part 6's counts)
    python -m videos.ai.ai19.compute --force quant

Results are cached in ``.cache/ai19/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    speculative  speculative decoding with Part 11's transformer as the target and a small counting model as the draft:
                 how often a drafted character is accepted, the characters per target run for drafts of 1 to 8, and a
                 check that the output distribution is exactly the target's
    quant        Part 11's transformer with its weights rounded to 8, 4 and 3 bits (per row, round to nearest), and to
                 FP4 (E2M1) with a scale per block of 32: bits per character on the passage, and the weight histogram
    flash        attention computed in tiles with an online softmax (FlashAttention's trick), against the plain formula;
                 the memory traffic of both for growing lengths
    roofline     this computer's own roofline: the speed of matrix products of growing size, and its memory bandwidth
    paging       a server's key-value memory for 200 requests of random lengths: reserved in one block per request at the
                 maximum length, against pages of 16 tokens (vLLM's paged attention); the share wasted
"""

from __future__ import annotations

import math
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai19")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_speculative():
    import torch

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    K = len(chars)
    tr, ps = data["train"].numpy(), data["passage"]
    # the draft: a counting model on the last 2 characters (lightly smoothed), built from the training text
    n = 2
    idx = tr[:-2] * K * K + tr[1:-1] * K + tr[2:]
    counts = np.bincount(idx, minlength=K ** 3).reshape(K, K, K).astype(np.float64) + 0.05
    draft_p = counts / counts.sum(-1, keepdims=True)

    def target_probs(ctx):
        with torch.no_grad():
            z = model(ctx[None, -c11.CTX:])[0]
            return torch.softmax(z, -1).numpy().astype(np.float64)

    g = rng(2023)  # Leviathan, Kalman & Matias; Chen et al., speculative decoding (2023)
    # acceptance: for real contexts from the passage, draft one character from q and accept with min(1, p/q)
    accept = []
    for s in g.integers(c11.CTX, len(ps) - 10, 300):
        ctx = ps[s - c11.CTX:s]
        p = target_probs(ctx)[-1]
        q = draft_p[tuple(ctx[-2:].numpy())]
        accept.append(float(np.minimum(p, q).sum()))  # the chance a drafted character is accepted
    alpha = float(np.mean(accept))
    ks = [1, 2, 3, 4, 6, 8]
    per_run = [(1 - alpha ** (k + 1)) / (1 - alpha) for k in ks]  # expected characters per target run (i.i.d. model)
    # exactness: sample the next character many times by the speculative rule, and compare with the target
    # a context where the big model hesitates (no character above 40%), so the comparison has something to show
    for _ in range(200):
        s0 = int(g.integers(c11.CTX, len(ps) - 10))
        ctx = ps[s0 - c11.CTX:s0]
        p = target_probs(ctx)[-1]
        if p.max() < 0.4 and np.sort(p)[-8:].sum() > 0.7:
            break
    q = draft_p[tuple(ctx[-2:].numpy())].astype(np.float64)
    q = q / q.sum()
    draws, N = np.zeros(K), 200_000
    x = g.choice(K, N, p=q)
    acc = g.random(N) < np.minimum(1, p[x] / q[x])
    resid = np.maximum(p - q, 0)
    resid /= resid.sum()
    y = np.where(acc, x, g.choice(K, N, p=resid))
    draws = np.bincount(y, minlength=K) / N
    tv = 0.5 * float(np.abs(draws - p).sum())
    top = np.argsort(-p)[:8]
    out = dict(alpha=alpha, ks=ks, per_run=per_run, accept=np.array(accept), tv=tv, N=N, p_top=p[top], q_top=q[top],
               emp_top=draws[top], top_chars=[chars[int(i)] for i in top], draft_order=n)
    print(f"    acceptance {alpha:.2f}; total variation of the speculative samples from the target {tv:.4f}", flush=True)
    assert tv < 0.01 and 0.2 < alpha < 0.95
    return out


# ---------------------------------------------------------------------------
FP4 = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6])  # E2M1's magnitudes


def quantize(W, mode):
    if mode == "fp32":
        return W
    if mode.startswith("int"):
        b = int(mode[3:])
        qmax = 2 ** (b - 1) - 1
        s = np.abs(W).max(1, keepdims=True) / qmax
        return np.clip(np.round(W / np.maximum(s, 1e-12)), -qmax - 1, qmax) * s
    # fp4 with a scale per block of 32
    flat = W.reshape(-1, 32)
    s = np.abs(flat).max(1, keepdims=True) / 6.0
    v = flat / np.maximum(s, 1e-12)
    mag = FP4[np.abs(np.abs(v)[..., None] - FP4).argmin(-1)]
    return (np.sign(v) * mag * s).reshape(W.shape)


def compute_quant():
    import torch

    from videos.ai.ai11 import compute as c11

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    orig = {k: v.clone() for k, v in model.state_dict().items()}
    modes = ["fp32", "int8", "int4", "int3", "fp4"]
    out = dict(modes=modes)
    W0 = orig["blocks.1.f1.weight"].numpy()
    out["hist_w"] = np.histogram(W0.ravel(), bins=80)[0]
    out["hist_edges"] = np.histogram(W0.ravel(), bins=80)[1]
    for mode in modes:
        sd = {k: (torch.tensor(quantize(v.numpy(), mode), dtype=torch.float32) if v.dim() == 2 and "emb" not in k else v)
              for k, v in orig.items()}
        model.load_state_dict(sd)
        out[f"bits_{mode}"] = c11.tf_bits(model, data["passage"])
        out[f"row_{mode}"] = quantize(W0, mode)[0][:64]
        print(f"    {mode}: {out[f'bits_{mode}']:.3f} bits/char", flush=True)
    model.load_state_dict(orig)
    out["n_params"] = int(sum(v.numel() for v in orig.values()))
    assert out["bits_int8"] - out["bits_fp32"] < 0.02 and out["bits_int3"] > out["bits_int4"]
    return out


# ---------------------------------------------------------------------------
def compute_flash():
    g = rng(2022)  # Dao et al., FlashAttention
    T, d, Bt = 512, 64, 64
    Q, Kk, V = (g.normal(size=(T, d)) for _ in range(3))
    S = Q @ Kk.T / math.sqrt(d)
    P = np.exp(S - S.max(1, keepdims=True))
    ref = (P / P.sum(1, keepdims=True)) @ V
    out_ = np.zeros((T, d))
    for i in range(0, T, Bt):  # one block of queries at a time
        m = np.full(Bt, -np.inf)
        l_ = np.zeros(Bt)
        acc = np.zeros((Bt, d))
        for j in range(0, T, Bt):  # stream the keys and values through, block by block
            s = Q[i:i + Bt] @ Kk[j:j + Bt].T / math.sqrt(d)
            m_new = np.maximum(m, s.max(1))
            scale = np.exp(m - m_new)
            p = np.exp(s - m_new[:, None])
            l_ = l_ * scale + p.sum(1)
            acc = acc * scale[:, None] + p @ V[j:j + Bt]
            m = m_new
        out_[i:i + Bt] = acc / l_[:, None]
    dev = float(np.abs(out_ - ref).max())
    Ts = np.array([1024, 4096, 16384, 65536, 131072])
    # memory for one head (fp16): the plain way stores the T x T table of scores; the tiled way only Q, K, V and the output
    plain = 2.0 * (4 * Ts * d + Ts * Ts)
    tiled = 2.0 * (4 * Ts * d)
    out = dict(dev=dev, T=T, d=d, Bt=Bt, Ts=Ts, plain=plain, tiled=tiled)
    assert dev < 1e-10
    return out


# ---------------------------------------------------------------------------
def compute_roofline():
    import torch

    torch.set_num_threads(4)
    sizes = [64, 128, 256, 512, 1024, 2048]
    gflops, intensity = [], []
    for n in sizes:
        a, b = torch.randn(n, n), torch.randn(n, n)
        reps = max(3, int(2e9 / (2 * n ** 3)))
        a @ b
        t = time.perf_counter()
        for _ in range(reps):
            a @ b
        dt = (time.perf_counter() - t) / reps
        gflops.append(2 * n ** 3 / dt / 1e9)
        intensity.append(2 * n ** 3 / (3 * 4 * n * n))  # flops per byte, each matrix moved once
    x = torch.randn(64 * 1024 * 1024 // 4)
    y = torch.empty_like(x)
    y.copy_(x)  # touch both buffers first, so the timing is the copying alone
    t = time.perf_counter()
    for _ in range(10):
        y.copy_(x)
    bw = 10 * 2 * x.numel() * 4 / (time.perf_counter() - t) / 1e9  # read and write
    out = dict(sizes=sizes, gflops=gflops, intensity=intensity, bandwidth=bw, peak=max(gflops), threads=4)
    print(f"    matmul up to {max(gflops):.0f} GFLOP/s; memory {bw:.1f} GB/s", flush=True)
    assert gflops[-1] > gflops[0]
    return out


# ---------------------------------------------------------------------------
def compute_paging():
    g = rng(2023)  # Kwon et al., vLLM
    n, max_len, page = 200, 4096, 16
    lens = np.minimum(np.round(g.lognormal(6.3, 1.0, n)).astype(int) + 20, max_len)
    reserved = n * max_len
    paged = int(np.sum(np.ceil(lens / page) * page))
    used = int(lens.sum())
    out = dict(n=n, max_len=max_len, page=page, lens=lens, used=used, reserved=reserved, paged=paged,
               waste_reserved=1 - used / reserved, waste_paged=1 - used / paged)
    assert out["waste_paged"] < 0.05 < out["waste_reserved"]
    return out


ITEMS = {
    "speculative": compute_speculative,
    "quant": compute_quant,
    "flash": compute_flash,
    "roofline": compute_roofline,
    "paging": compute_paging,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
