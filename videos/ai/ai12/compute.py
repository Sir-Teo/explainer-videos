"""Precompute everything numerical in Part 12 of the AI series ("Memory").

    python -m videos.ai.ai12.compute              # everything missing
    python -m videos.ai.ai12.compute --force mqar

Results are cached in ``.cache/ai12/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

Items:
    kvcache    the memory a model keeps per token of context, from published configurations: Llama 3.1 70B (grouped
               queries), the same with one key and value per query head, DeepSeek-V3 (multi-head latent attention, and
               its full-attention equivalent), Qwen3-Next-80B-A3B (one attention layer in four; the rest Gated
               DeltaNet, with a fixed-size state); the totals at contexts from 1,000 to a million tokens
    linear     causal linear attention computed two ways, as a masked matrix product and as a recurrence on a d x d
               state, agreeing to rounding error; the operation counts of softmax attention and of the recurrence
    capacity   a d x d matrix as an associative memory (d = 64), written by the additive rule (linear attention), the
               decaying rule (Mamba-2, RetNet) and the delta rule (DeltaNet): N random key-value pairs read back with
               their keys, as N grows and by age; and a changing world, 16 keys rewritten 256 times, read for their
               latest values
    ssm        a diagonal state-space model's memory: impulse responses for several step sizes, and a selective one
               (step size set by the input) holding a marked value through a stretch of noise
    mla        multi-head latent attention's folding trick, checked with random weights: without positions, the score
               computed from unpacked keys and from the latent with the key matrix folded into the query agree; with
               rotary positions applied to the unpacked keys they don't; with DeepSeek's decoupled rotary key (a small
               shared key that carries the positions, cached next to the latent) they agree again
    delta      the delta rule up close: the update as a rank-one change of a linear map (a 2 x 2 example, with beta
               1/2, 1 and 2); the gated delta rule run step by step and chunk by chunk (the WY form of a product of
               (I - beta k k^T), one triangular solve per chunk), agreeing to rounding error; the decaying rule as
               masked attention, (L o QK^T)V, with its semiseparable mask (Mamba-2's state-space duality)
    mqar       multi-query associative recall (Arora et al., Zoology): tiny one-layer models with softmax attention,
               linear attention and the delta rule (keys of 16 numbers), trained to answer "what value went with this
               key?" after N pairs; accuracy as N grows past the key size
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai12")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# published configurations (Hugging Face config.json of each model; bf16, 2 bytes a number)
CONFIGS = {
    "llama70": dict(name="Llama 3.1 70B", layers=80, q_heads=64, kv_heads=8, head_dim=128),
    "deepseek": dict(name="DeepSeek-V3", layers=61, q_heads=128, kv_lora_rank=512, rope_dim=64, nope_dim=128, v_dim=128),
    "qwen3next": dict(name="Qwen3-Next-80B-A3B", layers=48, attn_every=4, q_heads=16, kv_heads=2, head_dim=256,
                      lin_v_heads=32, lin_k_heads=16, lin_k_dim=128, lin_v_dim=128),
}


def compute_kvcache():
    B = 2  # bytes per number
    L = CONFIGS["llama70"]
    llama = 2 * L["layers"] * L["kv_heads"] * L["head_dim"] * B
    llama_mha = 2 * L["layers"] * L["q_heads"] * L["head_dim"] * B
    D = CONFIGS["deepseek"]
    mla = D["layers"] * (D["kv_lora_rank"] + D["rope_dim"]) * B
    mla_full = D["layers"] * D["q_heads"] * ((D["nope_dim"] + D["rope_dim"]) + D["v_dim"]) * B
    Q = CONFIGS["qwen3next"]
    n_attn = Q["layers"] // Q["attn_every"]
    qwen_tok = 2 * n_attn * Q["kv_heads"] * Q["head_dim"] * B
    qwen_state = (Q["layers"] - n_attn) * Q["lin_v_heads"] * Q["lin_k_dim"] * Q["lin_v_dim"] * B  # fixed, any length
    ctx = np.array([1e3, 4e3, 16e3, 64e3, 128e3, 256e3, 1e6])
    out = dict(per_token=dict(llama=llama, llama_mha=llama_mha, mla=mla, mla_full=mla_full, qwen=qwen_tok),
               qwen_state=qwen_state, n_attn=n_attn, ctx=ctx, configs=CONFIGS)
    for k, v in out["per_token"].items():
        out[f"total_{k}"] = ctx * v + (qwen_state if k == "qwen" else 0)
    assert llama == 327_680 and mla == 70_272  # 320 KiB and about 69 KiB a token
    assert mla_full / mla > 50
    return out


# ---------------------------------------------------------------------------
def compute_linear():
    g = rng(2020)  # Katharopoulos et al., Transformers are RNNs
    T, d = 200, 16
    q, k, v = (g.normal(size=(T, d)) for _ in range(3))

    def phi(x):  # elu + 1: positive features
        return np.where(x > 0, x + 1, np.exp(x))

    fq, fk = phi(q), phi(k)
    A = np.tril(fq @ fk.T)
    par = (A @ v) / A.sum(1, keepdims=True)
    S, z = np.zeros((d, d)), np.zeros(d)
    rec = np.zeros((T, d))
    for t in range(T):
        S += np.outer(fk[t], v[t])
        z += fk[t]
        rec[t] = (fq[t] @ S) / (fq[t] @ z)
    dev = float(np.abs(par - rec).max())
    assert dev < 1e-10
    Ts = np.array([1e3, 4e3, 16e3, 64e3, 256e3, 1e6])
    dm = 128
    return dict(dev=dev, T=T, d=d, Ts=Ts, softmax_ops=2 * Ts * Ts / 2 * dm, linear_ops=2 * Ts * dm * dm,
                state=dm * dm)


# ---------------------------------------------------------------------------
def compute_capacity():
    g = rng(1960)  # Widrow & Hoff, 1960: the delta rule
    d, trials = 64, 40

    def write(S, k, v, rule, alpha=0.97):
        if rule == "add":
            return S + np.outer(v, k)
        if rule == "decay":
            return alpha * S + np.outer(v, k)
        return S + np.outer(v - S @ k, k)  # delta: replace what the key reads now with the new value

    def unit(n):
        K = g.normal(size=(n, d))
        return K / np.linalg.norm(K, axis=1, keepdims=True)

    # 1. N different keys, each written once, then all read back
    Ns = [4, 8, 16, 24, 32, 48, 64, 96, 128, 192, 256]

    def once(N, rule):
        errs = np.zeros(N)
        for _ in range(trials):
            K, Vv = unit(N), g.normal(size=(N, d)) / math.sqrt(d)
            S = np.zeros((d, d))
            for i in range(N):
                S = write(S, K[i], Vv[i], rule)
            errs += np.linalg.norm(K @ S.T - Vv, axis=1) ** 2 / np.linalg.norm(Vv, axis=1) ** 2
        return errs / trials  # relative squared error per pair, oldest first

    out = dict(d=d, Ns=Ns)
    for rule in ("add", "decay", "delta"):
        out[f"err_{rule}"] = np.array([once(N, rule).mean() for N in Ns])
        out[f"age_{rule}"] = once(128, rule)[::-1]  # by age: newest first
    # 2. a changing world: 16 keys, 256 writes, each a new value for a random one of them; read the latest values
    M, W = 16, 256
    upd = {r: [] for r in ("add", "decay", "delta")}
    for _ in range(trials):
        K = unit(M)
        latest = np.zeros((M, d))
        seq = g.integers(0, M, W)
        vals = g.normal(size=(W, d)) / math.sqrt(d)
        Ss = {r: np.zeros((d, d)) for r in upd}
        for t, j in enumerate(seq):
            latest[j] = vals[t]
            for r in upd:
                Ss[r] = write(Ss[r], K[j], vals[t], r)
        seen = np.isin(np.arange(M), seq)
        for r in upd:
            R = K @ Ss[r].T
            upd[r].append(float((np.linalg.norm(R - latest, axis=1) ** 2 / np.linalg.norm(latest, axis=1).clip(1e-9) ** 2)[seen].mean()))
    out.update(M=M, W=W, **{f"update_{r}": float(np.mean(v)) for r, v in upd.items()})
    a = out["err_add"]
    assert abs(a[Ns.index(64)] - 63 / 64) < 0.2  # adding: the crosstalk grows like (N - 1) / d
    assert out["update_delta"] < 0.1 * out["update_add"] and out["update_delta"] < out["update_decay"]
    return out


# ---------------------------------------------------------------------------
def compute_ssm():
    t = np.arange(0, 120)
    deltas = [0.02, 0.08, 0.3]
    lam = 1.0
    imp = {f"{dt:g}": np.exp(-lam * dt * t) for dt in deltas}
    # a selective SSM, one channel: h_t = exp(-dt_t) h_{t-1} + (1 - exp(-dt_t)) u_t, dt_t large on marked inputs
    g = rng(2023)  # Gu & Dao, Mamba
    T = 120
    u = g.normal(size=T) * 0.6
    mark = np.zeros(T, bool)
    mark[[15, 70]] = True
    u[15], u[70] = 2.2, -1.8
    out = {}
    for name, dt in (("fixed", np.full(T, 0.08)), ("selective", np.where(mark, 6.0, 0.0005))):
        h, hs = 0.0, []
        for i in range(T):
            a = math.exp(-dt[i])
            h = a * h + (1 - a) * u[i]
            hs.append(h)
        out[name] = np.array(hs)
    assert abs(out["selective"][69] - u[15]) < 0.15 and abs(out["selective"][-1] - u[70]) < 0.15
    assert abs(out["fixed"][69]) < 0.5 * abs(u[15])  # a fixed step size has let it fade into the noise
    return dict(t=t, deltas=deltas, u=u, mark=np.where(mark)[0], **{f"imp{k}": v for k, v in imp.items()}, **out)


# ---------------------------------------------------------------------------
def compute_mqar():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    torch.set_num_threads(2)
    NK, NV, D = 64, 64, 64
    DK = 16  # the memory's key size: lists longer than this overflow a fixed state
    VOC = NK + NV

    def batch(g, n, N):
        keys = np.stack([g.permutation(NK)[:N] for _ in range(n)])
        vals = g.integers(0, NV, (n, N)) + NK
        order = np.stack([g.permutation(N) for _ in range(n)])
        pairs = np.stack([keys, vals], 2).reshape(n, 2 * N)
        qk = np.take_along_axis(keys, order, 1)
        ans = np.take_along_axis(vals, order, 1)
        x = np.concatenate([pairs, qk], 1)
        y = np.full(x.shape, -100)
        y[:, 2 * N:] = ans
        return torch.tensor(x), torch.tensor(y)

    class Model(nn.Module):
        def __init__(self, mixer):
            super().__init__()
            self.mixer = mixer
            self.emb = nn.Embedding(VOC, D)
            self.conv = nn.Parameter(torch.randn(2, D) * 0.3)  # a short convolution: each token sees the one before
            self.qkv = nn.Linear(D, 2 * DK + D, bias=False)
            self.beta = nn.Linear(D, 1)
            self.o = nn.Linear(D, D, bias=False)
            self.n = nn.LayerNorm(D)
            self.out = nn.Linear(D, VOC)

        def forward(self, x):
            e = self.emb(x)
            h = e * self.conv[0] + F.pad(e, (0, 0, 1, 0))[:, :-1] * self.conv[1]
            q, k, v = self.qkv(h).split([DK, DK, D], -1)
            T = x.shape[1]
            if self.mixer == "softmax":
                a = F.scaled_dot_product_attention(q[:, None], k[:, None], v[:, None], is_causal=True)[:, 0]
            elif self.mixer == "linear":
                fq, fk = F.elu(q) + 1, F.elu(k) + 1
                A = (fq @ fk.transpose(1, 2)).tril()
                a = (A @ v) / (A.sum(-1, keepdim=True) + 1e-6)
            else:  # delta rule
                q, k = F.normalize(q, dim=-1), F.normalize(k, dim=-1)
                b = torch.sigmoid(self.beta(h))
                S = torch.zeros(x.shape[0], D, DK)
                outs = []
                for t in range(T):
                    kt, vt = k[:, t], v[:, t]
                    pred = torch.einsum("bij,bj->bi", S, kt)
                    S = S + b[:, t, :, None] * torch.einsum("bi,bj->bij", vt - pred, kt)
                    outs.append(torch.einsum("bij,bj->bi", S, q[:, t]))
                a = torch.stack(outs, 1)
            return self.out(self.n(h + self.o(a)))

    Ns = [8, 16, 32, 48]
    out = dict(Ns=Ns, d=DK)
    for mixer in ("softmax", "linear", "delta"):
        accs = []
        for N in Ns:
            torch.manual_seed(2023)  # Arora et al., Zoology
            m = Model(mixer)
            opt = torch.optim.AdamW(m.parameters(), lr=3e-3, weight_decay=0.01)
            g = rng(N)
            steps = 1500
            sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-3, total_steps=steps, pct_start=0.1)
            xe, ye = batch(rng(20_000 + N), 128, N)
            curve = []
            for step in range(steps + 1):
                if step % 100 == 0:  # how it learns: recall on a fixed batch, along the way
                    with torch.no_grad():
                        pe, mk = m(xe).argmax(-1), ye >= 0
                        curve.append((step, float((pe[mk] == ye[mk]).float().mean())))
                if step == steps:
                    break
                x, y = batch(g, 64, N)
                loss = F.cross_entropy(m(x).reshape(-1, VOC), y.reshape(-1), ignore_index=-100)
                opt.zero_grad()
                loss.backward()
                opt.step()
                sched.step()
            with torch.no_grad():
                x, y = batch(rng(10_000 + N), 512, N)
                p = m(x).argmax(-1)
                mk = y >= 0
                accs.append(float((p[mk] == y[mk]).float().mean()))
            print(f"    {mixer} N={N}: recall {accs[-1]:.1%}", flush=True)
            out[f"curve_{mixer}_{N}"] = np.array(curve)
        out[mixer] = np.array(accs)
    assert out["softmax"].min() > 0.9
    assert out["linear"][-1] < 0.9  # the adding memory overflows
    return out


# ---------------------------------------------------------------------------
def compute_mla():
    g = rng(2024)  # DeepSeek-V2 (2024)
    d, dc, dh, dr, n = 64, 16, 8, 4, 12  # model width, latent, head size, rotary size, tokens

    def rope(x, pos, dim):
        th = 10000.0 ** (-np.arange(dim // 2) * 2 / dim)
        a = pos * th
        x1, x2 = x[: dim // 2], x[dim // 2:]
        return np.concatenate([x1 * np.cos(a) - x2 * np.sin(a), x1 * np.sin(a) + x2 * np.cos(a)])

    H = g.normal(size=(n, d))
    W_dkv, W_uk, W_q = g.normal(size=(dc, d)) / 8, g.normal(size=(dh, dc)) / 4, g.normal(size=(dh, d)) / 8
    C = H @ W_dkv.T  # the cached latents
    m = n - 1  # the query's position
    q = W_q @ H[m]
    W_fold = W_uk.T @ q  # the key matrix folded into the query, once
    out = {}
    # 1. no positions: score = q . (W_uk c) = (W_uk^T q) . c
    explicit = np.array([q @ (W_uk @ C[j]) for j in range(n)])
    folded = C @ W_fold
    out["diff_plain"] = float(np.abs(explicit - folded).max())
    # 2. rotary positions on the unpacked keys and the query: R_m q . R_j W_uk c = q . R_{j-m} W_uk c; the rotation sits
    #    between the query and W_uk, different for every pair, so no single folded matrix exists
    explicit_r = np.array([rope(q, m, dh) @ rope(W_uk @ C[j], j, dh) for j in range(n)])
    out["diff_rope_folded"] = float(np.abs(explicit_r - folded).max())  # what the folded shortcut would give: wrong
    out["rel_rope_folded"] = out["diff_rope_folded"] / float(np.abs(explicit_r).max())
    # 3. decoupled: content part without positions (folded) + a small shared rotary key computed from the token
    W_kr, W_qr = g.normal(size=(dr, d)) / 8, g.normal(size=(dr, d)) / 8
    Kr = np.array([rope(W_kr @ H[j], j, dr) for j in range(n)])  # cached next to the latent: dc + dr numbers a token
    qr = rope(W_qr @ H[m], m, dr)
    explicit_d = np.array([q @ (W_uk @ C[j]) + qr @ Kr[j] for j in range(n)])
    folded_d = C @ W_fold + Kr @ qr
    out["diff_decoupled"] = float(np.abs(explicit_d - folded_d).max())
    print(f"    no positions: {out['diff_plain']:.1e}; rotary on unpacked keys, folded anyway: off by "
          f"{100 * out['rel_rope_folded']:.0f}%; decoupled rotary key: {out['diff_decoupled']:.1e}", flush=True)
    assert out["diff_plain"] < 1e-12 and out["diff_decoupled"] < 1e-12 and out["rel_rope_folded"] > 0.05
    return out


# ---------------------------------------------------------------------------
def compute_delta():
    import time

    from scipy.linalg import solve_triangular

    g = rng(2024)  # Yang et al., Parallelizing Linear Transformers with the Delta Rule over Sequence Length (2024)
    # 1. the update on a 2 x 2 memory: S <- S (I - beta k k^T) + beta v k^T moves S's answer for k towards v, and
    #    leaves its answer for every direction at right angles to k alone
    S0 = np.array([[0.9, 0.3], [-0.2, 0.7]])
    th = np.deg2rad(30.0)
    k2 = np.array([np.cos(th), np.sin(th)])
    v2 = np.array([-0.3, 0.8])
    geo = {}
    for b in (0.5, 1.0, 2.0):
        S1 = S0 @ (np.eye(2) - b * np.outer(k2, k2)) + b * np.outer(v2, k2)
        geo[f"S{b:g}"] = S1
        perp = np.array([-k2[1], k2[0]])
        assert np.allclose(S1 @ perp, S0 @ perp)  # nothing changes at right angles to the key
        assert np.allclose(S1 @ k2, (1 - b) * S0 @ k2 + b * v2)
    # 2. the gated delta rule, step by step and chunk by chunk
    T, d, Cn = 2048, 64, 64

    def unit(x):
        return x / np.linalg.norm(x, axis=1, keepdims=True)

    Kx, Qx, Vx = unit(g.normal(size=(T, d))), unit(g.normal(size=(T, d))), g.normal(size=(T, d))
    beta = 1 / (1 + np.exp(-g.normal(size=T)))
    alpha = np.exp(-np.exp(g.normal(-3.0, 1.0, size=T)))  # decays near one, as a gate would learn

    def recurrent(gated):
        S = np.zeros((d, d))  # S @ k is the memory's answer for key k
        O = np.empty((T, d))
        for t in range(T):
            a = alpha[t] if gated else 1.0
            S = a * S
            S = S - beta[t] * np.outer(S @ Kx[t] - Vx[t], Kx[t])
            O[t] = S @ Qx[t]
        return O, S

    def chunked(gated):
        S = np.zeros((d, d))
        O = np.empty((T, d))
        for c0 in range(0, T, Cn):
            k, q, v, b = Kx[c0:c0 + Cn], Qx[c0:c0 + Cn], Vx[c0:c0 + Cn], beta[c0:c0 + Cn]
            la = np.log(alpha[c0:c0 + Cn]) if gated else np.zeros(Cn)
            G = np.exp(np.cumsum(la))  # decay from the chunk's start to each step
            D = np.exp(np.cumsum(la)[:, None] - np.cumsum(la)[None, :])  # decay from step j to step i
            # WY / UT transform: one triangular solve gives the chunk's product of (I - beta k k^T), decays included
            A = np.tril(D * (k @ k.T), -1) * b[:, None]
            M = np.eye(len(b)) + A
            W = solve_triangular(M, (b * G)[:, None] * k, lower=True)
            U = solve_triangular(M, b[:, None] * v, lower=True)
            Un = U - W @ S.T  # each step's correction, after what the chunk's starting state already says
            O[c0:c0 + Cn] = G[:, None] * (q @ S.T) + (np.tril(D * (q @ k.T))) @ Un
            S = G[-1] * S + (Un * D[-1][:, None]).T @ k
        return O, S

    out = dict(geo_S0=S0, geo_k=k2, geo_v=v2, **{f"geo_{n}": m for n, m in geo.items()}, T=T, d=d, chunk=Cn)
    for gated in (False, True):
        t0 = time.perf_counter()
        Or, Sr = recurrent(gated)
        t1 = time.perf_counter()
        Oc, Sc = chunked(gated)
        t2 = time.perf_counter()
        tag = "gated" if gated else "plain"
        out[f"diff_{tag}"] = float(max(np.abs(Or - Oc).max(), np.abs(Sr - Sc).max()))
        out[f"t_rec_{tag}"], out[f"t_chunk_{tag}"] = t1 - t0, t2 - t1
        print(f"    {tag} delta rule: step by step {t1 - t0:.3f}s, by chunks {t2 - t1:.3f}s; largest difference "
              f"{out[f'diff_{tag}']:.1e}", flush=True)
        assert out[f"diff_{tag}"] < 1e-9
    # 3. the decaying rule as masked attention: O = (L o Q K^T) V, L[i, j] = a_{j+1} ... a_i for j <= i
    n = 32
    a = np.exp(-np.exp(g.normal(-2.0, 0.8, size=n)))
    a[[9, 22]] = 0.05  # two moments where the gate forgets almost everything
    cs = np.cumsum(np.log(a))
    L = np.tril(np.exp(cs[:, None] - cs[None, :]))
    q, k, v = Qx[:n], Kx[:n], Vx[:n]
    S = np.zeros((d, d))
    Orec = np.empty((n, d))
    for t in range(n):
        S = a[t] * S + np.outer(v[t], k[t])
        Orec[t] = S @ q[t]
    Omask = (L * (q @ k.T)) @ v
    out["ssd_L"], out["ssd_a"] = L, a
    out["ssd_diff"] = float(np.abs(Orec - Omask).max())
    # every block below the diagonal has rank one (the mask is 1-semiseparable)
    blk = L[16:, :16]
    sv = np.linalg.svd(blk, compute_uv=False)
    out["ssd_rank_ratio"] = float(sv[1] / sv[0])
    print(f"    masked form vs recurrence: {out['ssd_diff']:.1e}; a lower block's 2nd/1st singular value "
          f"{out['ssd_rank_ratio']:.1e}", flush=True)
    assert out["ssd_diff"] < 1e-9 and out["ssd_rank_ratio"] < 1e-9
    return out


ITEMS = {
    "kvcache": compute_kvcache,
    "linear": compute_linear,
    "capacity": compute_capacity,
    "ssm": compute_ssm,
    "mqar": compute_mqar,
    "delta": compute_delta,
    "mla": compute_mla,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
