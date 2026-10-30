"""Precompute everything numerical in Part 15 of the AI series ("Memory").

    python -m videos.ai.ai15.compute              # everything missing
    python -m videos.ai.ai15.compute --force mqar

Results are cached in ``.cache/ai15/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.

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

CACHE = Cache("ai15")
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



# ---------------------------------------------------------------------------
# Associative memory, from Hopfield to the matrix written and read
# ---------------------------------------------------------------------------
def compute_hopfield():
    """A Hopfield network (1982) of N = 100 binary neurons storing P random patterns by Hebb's outer-product rule; each
    pattern is cued with 10 of its 100 bits flipped and the network runs until nothing changes.  Recall: the share of
    cues that end exactly on their pattern, against P / N (the classical limit is about 0.138, Amit, Gutfreund &
    Sompolinsky 1985).  And one recall step by step (energy falling) for the picture."""
    g = rng(1982)
    N, trials, flips = 100, 16, 10
    Ps = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32]

    def settle(W, s, order_rng, sweeps=8, trace=None):
        s = s.copy()
        for _ in range(sweeps):
            changed = 0
            for i in order_rng.permutation(N):
                h = W[i] @ s
                new = 1.0 if h >= 0 else -1.0
                if new != s[i]:
                    s[i] = new
                    changed += 1
            if trace is not None:
                trace.append(s.copy())
            if not changed:
                break
        return s

    frac, overlap = [], []
    for P in Ps:
        ok, ov = 0, 0.0
        for _ in range(trials):
            X = np.where(g.normal(size=(P, N)) > 0, 1.0, -1.0)
            W = X.T @ X / N
            np.fill_diagonal(W, 0)
            p = int(g.integers(0, P))
            s = X[p].copy()
            s[g.choice(N, flips, replace=False)] *= -1
            out = settle(W, s, g)
            ok += int(np.array_equal(out, X[p]))
            ov += float(out @ X[p] / N)
        frac.append(ok / trials)
        overlap.append(ov / trials)
    # one recall, step by step: 5 patterns, a cue with 30 bits flipped, asynchronous updates in small groups
    P = 5
    X = np.where(g.normal(size=(P, N)) > 0, 1.0, -1.0)
    W = X.T @ X / N
    np.fill_diagonal(W, 0)
    s = X[0].copy()
    s[g.choice(N, 30, replace=False)] *= -1
    frames, energy = [s.copy()], [float(-0.5 * s @ W @ s)]
    for i in g.permutation(N):
        s[i] = 1.0 if W[i] @ s >= 0 else -1.0
        frames.append(s.copy())
        energy.append(float(-0.5 * s @ W @ s))
    frames = np.array(frames[::5] + [frames[-1]])
    assert np.array_equal(frames[-1], X[0])  # a light load: the cue falls back to its pattern
    assert all(b <= a + 1e-12 for a, b in zip(energy, energy[1:]))  # every asynchronous step lowers the energy
    return dict(N=N, flips=flips, trials=trials, Ps=Ps, frac=np.array(frac), overlap=np.array(overlap),
                ex_patterns=X, ex_frames=frames, ex_energy=np.array(energy[::5] + [energy[-1]]))


def compute_matrix_rw():
    """The memory matrix written and read, step by step (d = 8): four key-value pairs written, then the second key
    given a new value; after every write, the matrix and what each key reads back, for the adding rule (linear
    attention) and the delta rule (beta = 1)."""
    g = rng(1992)  # Schmidhuber's fast weights
    d = 8
    Qm, _ = np.linalg.qr(g.normal(size=(d, d)))
    keys = Qm[:4] + 0.1 * g.normal(size=(4, d))  # nearly at right angles, but not quite: a little crosstalk
    keys /= np.linalg.norm(keys, axis=1, keepdims=True)
    vals = g.normal(size=(5, d)) / math.sqrt(d) * 1.6
    seq = [(0, 0), (1, 1), (2, 2), (3, 3), (1, 4)]  # (key, value): the last write gives key 1 a new value
    out = dict(d=d, keys=keys, vals=vals, seq=np.array(seq))
    for rule in ("add", "delta"):
        S = np.zeros((d, d))
        Ss, reads, errs = [], [], []
        truth = {}
        for kk, vv in seq:
            k, v = keys[kk], vals[vv]
            S = S + np.outer(v, k) if rule == "add" else S + np.outer(v - S @ k, k)
            truth[kk] = v
            R = keys @ S.T  # what every key reads now
            Ss.append(S.copy())
            reads.append(R)
            errs.append([float(np.linalg.norm(R[j] - truth[j]) / np.linalg.norm(truth[j])) if j in truth else np.nan
                         for j in range(4)])
        out[f"S_{rule}"], out[f"read_{rule}"], out[f"err_{rule}"] = np.array(Ss), np.array(reads), np.array(errs)
    out["overlaps"] = keys @ keys.T
    assert out["err_delta"][-1][1] < 1e-12  # the delta rule's rewrite is exact for that key
    assert out["err_add"][-1][1] > 0.5  # adding answers with a mixture of the old and the new value
    return out


# ---------------------------------------------------------------------------
# The associative scan
# ---------------------------------------------------------------------------
def compute_scan():
    """h_t = a_t h_{t-1} + b_t computed by a parallel prefix scan: the pairs (a, b) combine by
    (a1, b1) * (a2, b2) = (a1 a2, a2 b1 + b2), which is associative, so log2 T rounds of combining (Hillis & Steele
    1986) or a work-efficient up-and-down sweep (Blelloch 1990) give every h_t; checked against the loop, with
    scalars and with 4 x 4 matrices (h_t = A_t h_{t-1} + B_t)."""
    g = rng(1990)
    T = 4096
    a, b = g.uniform(0.9, 1.0, T), g.normal(size=T)

    def loop(a, b):
        h, out = 0.0, np.empty(T)
        for t in range(T):
            h = a[t] * h + b[t]
            out[t] = h
        return out

    def hillis_steele(a, b):
        A, Bv = a.copy(), b.copy()
        k, rounds = 1, 0
        while k < len(A):
            A2, B2 = A.copy(), Bv.copy()
            A2[k:] = A[:-k] * A[k:]
            B2[k:] = A[k:] * Bv[:-k] + Bv[k:]
            A, Bv = A2, B2
            k *= 2
            rounds += 1
        return Bv, rounds

    def blelloch(a, b):  # exclusive up-sweep / down-sweep, then shifted to inclusive
        n = len(a)
        A, Bv = a.copy(), b.copy()
        ops, rounds = 0, 0
        d = 1
        while d < n:  # up-sweep: partial products in a tree
            idx = np.arange(2 * d - 1, n, 2 * d)
            Bv[idx] = A[idx] * Bv[idx - d] + Bv[idx]
            A[idx] = A[idx - d] * A[idx]
            ops += len(idx)
            rounds += 1
            d *= 2
        A[-1], Bv[-1] = 1.0, 0.0  # identity at the root
        d = n // 2
        while d >= 1:  # down-sweep
            idx = np.arange(2 * d - 1, n, 2 * d)
            la, lb = A[idx - d].copy(), Bv[idx - d].copy()
            A[idx - d], Bv[idx - d] = A[idx], Bv[idx]
            # right child = (parent prefix) * (left subtree)
            Bv[idx] = la * Bv[idx] + lb
            A[idx] = A[idx] * la
            ops += len(idx)
            rounds += 1
            d //= 2
        return a * Bv + b, ops, rounds  # exclusive prefix (A, Bv) then the element itself

    ref = loop(a, b)
    hs, r_hs = hillis_steele(a, b)
    bl, ops_bl, r_bl = blelloch(a, b)
    # matrices: h_t = A_t h_{t-1} + B_t, combine (A1, B1) * (A2, B2) = (A2 A1, A2 B1 + B2)
    Tm, n = 256, 4
    Am = 0.25 * g.normal(size=(Tm, n, n)) + 0.7 * np.eye(n)
    Bm = g.normal(size=(Tm, n))
    h, refm = np.zeros(n), []
    for t in range(Tm):
        h = Am[t] @ h + Bm[t]
        refm.append(h)
    refm = np.array(refm)
    AA, BB = Am.copy(), Bm.copy()
    k = 1
    while k < Tm:
        A2, B2 = AA.copy(), BB.copy()
        A2[k:] = AA[k:] @ AA[:-k]
        B2[k:] = np.einsum("tij,tj->ti", AA[k:], BB[:-k]) + BB[k:]
        AA, BB = A2, B2
        k *= 2
    out = dict(T=T, rounds_hs=r_hs, rounds_bl=r_bl, work_hs=int(T * r_hs - (T - 1)), work_bl=int(ops_bl),
               diff_hs=float(np.abs(hs - ref).max() / np.abs(ref).max()), diff_bl=float(np.abs(bl - ref).max() / np.abs(ref).max()),
               diff_mat=float(np.abs(BB - refm).max() / np.abs(refm).max()), Tm=Tm, n=n)
    # a small trace to draw: T = 8, which positions combine in each round of Hillis-Steele
    out["trace"] = [[(i - k, i) for i in range(k, 8)] for k in (1, 2, 4)]
    print(f"    scan: {r_hs} rounds (Hillis-Steele), {r_bl} (Blelloch, {ops_bl} combines for {T}); "
          f"largest relative difference {max(out['diff_hs'], out['diff_bl']):.1e}, matrices {out['diff_mat']:.1e}", flush=True)
    assert max(out["diff_hs"], out["diff_bl"], out["diff_mat"]) < 1e-9 and r_hs == 12
    return out


# ---------------------------------------------------------------------------
# HiPPO, ZOH and S4
# ---------------------------------------------------------------------------
def legs_matrices(N):
    n = np.arange(N)
    r = np.sqrt(2 * n + 1)
    A = np.tril(np.outer(r, r), -1) + np.diag(n + 1)
    return A, r.copy()


def legendre(N, x):
    """P_0 .. P_{N-1} at x in [-1, 1], by the three-term recurrence."""
    P = np.zeros((N, len(x)))
    P[0] = 1
    if N > 1:
        P[1] = x
    for n in range(1, N - 1):
        P[n + 1] = ((2 * n + 1) * x * P[n] - n * P[n - 1]) / (n + 1)
    return P


def compute_hippo():
    """HiPPO-LegS (Gu, Dao, Ermon, Rudra & Re 2020) memorizing a signal online: N numbers c(t), updated once per
    sample by the recurrence c_k = (I + A/2k)^-1 [(I - A/2k) c_{k-1} + B f_k / k] (the bilinear step of
    dc/dt = -A c / t + B f / t), hold the best degree-(N-1) polynomial fit to everything seen so far; reconstructed
    with Legendre polynomials and compared with the signal, for several N."""
    g = rng(2020)
    L = 2000
    s = np.linspace(0, 1, L)
    f = np.zeros(L)
    for j in range(1, 13):  # a smooth random signal
        f += g.normal() / j * np.sin(2 * np.pi * j * s + g.uniform(0, 2 * np.pi))
    f /= np.abs(f).max()
    Ns = [4, 8, 16, 32, 64]
    snaps_at = [250, 500, 1000, 1500, 2000]
    out = dict(L=L, f=f, Ns=Ns, snaps_at=snaps_at)
    for N in Ns:
        A, B = legs_matrices(N)
        I = np.eye(N)
        c = np.zeros(N)
        snaps = []
        for k in range(1, L + 1):
            c = np.linalg.solve(I + A / (2 * k), (I - A / (2 * k)) @ c + B * f[k - 1] / k)
            if k in snaps_at:
                x = np.linspace(-1, 1, k)
                rec = (c[:, None] * np.sqrt(2 * np.arange(N) + 1)[:, None] * legendre(N, x)).sum(0)
                snaps.append(rec)
        err = float(np.sqrt(np.mean((snaps[-1] - f) ** 2)) / np.sqrt(np.mean(f ** 2)))
        out[f"err_{N}"] = err
        if N in (8, 32):
            out[f"snaps_{N}"] = [np.asarray(x) for x in snaps]
        # the best possible degree-(N-1) fit, by least squares on the whole signal: what the memory should approach
        V = legendre(N, np.linspace(-1, 1, L)).T
        coef = np.linalg.lstsq(V, f, rcond=None)[0]
        out[f"best_{N}"] = float(np.sqrt(np.mean((V @ coef - f) ** 2)) / np.sqrt(np.mean(f ** 2)))
        print(f"    HiPPO-LegS N={N}: error {err:.3f} (best polynomial fit {out[f'best_{N}']:.3f})", flush=True)
    for k_ in ("snaps_8", "snaps_32"):
        out[k_] = np.concatenate(out[k_])  # ragged: lengths are snaps_at
    assert out["err_64"] < out["err_8"] and out["err_32"] < 1.5 * out["best_32"] + 0.02
    return out


def compute_zoh():
    """Discretizing h' = A h + B x for a step Delta with the input held constant over each step: the zero-order hold
    gives A_bar = e^{Delta A}, B_bar = A^{-1}(e^{Delta A} - I) B, exact for such inputs; Euler and the bilinear rule
    are approximations of order 1 and 2.  Checked against a fine Runge-Kutta solution of the ODE; and S4's view, the
    same SSM as a convolution with the kernel (C B_bar, C A_bar B_bar, C A_bar^2 B_bar, ...)."""
    from scipy.linalg import expm

    g = rng(2022)
    A = np.array([[-0.3, -2.0], [2.0, -0.3]])  # a damped oscillator: a memory that rings, then fades
    B = np.array([1.0, 0.0])
    Cv = np.array([0.0, 1.0])
    T_end = 12.0
    deltas = [0.4, 0.2, 0.1, 0.05, 0.025]
    xs = g.normal(size=int(round(T_end / deltas[-1])))  # one piecewise-constant input on the finest grid

    def u_at(t, delta):  # the same input signal, resampled on a grid of step delta (held over each step)
        k = min(int(t / delta), int(round(T_end / delta)) - 1)
        return xs[int(k * delta / deltas[-1])]

    def rk4(delta, sub=200):
        n = int(round(T_end / delta))
        h, hs = np.zeros(2), []
        for k in range(n):
            u = u_at(k * delta + 1e-12, delta)
            dt = delta / sub
            for _ in range(sub):
                f1 = A @ h + B * u
                f2 = A @ (h + dt / 2 * f1) + B * u
                f3 = A @ (h + dt / 2 * f2) + B * u
                f4 = A @ (h + dt * f3) + B * u
                h = h + dt / 6 * (f1 + 2 * f2 + 2 * f3 + f4)
            hs.append(h.copy())
        return np.array(hs)

    out = dict(deltas=deltas, A=A, B=B, C=Cv, T_end=T_end)
    I = np.eye(2)
    errs = {"euler": [], "bilinear": [], "zoh": []}
    for delta in deltas:
        n = int(round(T_end / delta))
        ref = rk4(delta)
        Ab_z = expm(delta * A)
        Bb_z = np.linalg.solve(A, (Ab_z - I) @ B)
        Ab_b = np.linalg.solve(I - delta / 2 * A, I + delta / 2 * A)
        Bb_b = np.linalg.solve(I - delta / 2 * A, delta * B)
        rules = {"euler": (I + delta * A, delta * B), "bilinear": (Ab_b, Bb_b), "zoh": (Ab_z, Bb_z)}
        for name, (Ab, Bb) in rules.items():
            h, hs = np.zeros(2), []
            for k in range(n):
                h = Ab @ h + Bb * u_at(k * delta + 1e-12, delta)
                hs.append(h.copy())
            errs[name].append(float(np.abs(np.array(hs) - ref).max() / np.abs(ref).max()))
            if delta == 0.2:
                out[f"y_{name}"] = np.array(hs) @ Cv
        if delta == 0.2:
            out["y_exact"] = ref @ Cv
            out["u_02"] = np.array([u_at(k * delta + 1e-12, delta) for k in range(n)])
    for k_, v in errs.items():
        out[f"err_{k_}"] = np.array(v)
    # S4: the recurrence as one long convolution
    delta, n = 0.1, 120
    Ab = expm(delta * A)
    Bb = np.linalg.solve(A, (Ab - I) @ B)
    K = np.array([Cv @ np.linalg.matrix_power(Ab, j) @ Bb for j in range(n)])
    u = g.normal(size=n)
    h, y_rec = np.zeros(2), []
    for k in range(n):
        h = Ab @ h + Bb * u[k]
        y_rec.append(Cv @ h)
    y_conv = np.array([np.dot(K[:k + 1][::-1], u[:k + 1]) for k in range(n)])
    out.update(kernel=K, conv_diff=float(np.abs(np.array(y_rec) - y_conv).max()))
    slope = lambda e: float(np.polyfit(np.log(deltas[-3:]), np.log(e[-3:]), 1)[0])  # noqa: E731
    out.update(slope_euler=slope(errs["euler"]), slope_bilinear=slope(errs["bilinear"]))
    print(f"    ZOH: largest error {max(errs['zoh']):.1e}; Euler order {out['slope_euler']:.2f}, bilinear "
          f"{out['slope_bilinear']:.2f}; convolution vs recurrence {out['conv_diff']:.1e}", flush=True)
    assert max(errs["zoh"]) < 1e-8 and out["conv_diff"] < 1e-10
    return out


# ---------------------------------------------------------------------------
# Test-time training and Titans, as a toy
# ---------------------------------------------------------------------------
def compute_ttt():
    """A memory that is a learner.  Each sequence has its own hidden rule v = f(k) (a random small tanh network, keys
    of 8 numbers); the model reads pairs (k, f(k)) one at a time and its memory takes one gradient step on each
    (test-time training).  Memories: a linear map (8 x 8: one step of gradient descent is the delta rule, TTT-Linear)
    and a two-layer network (8 -> 32 -> 8, TTT-MLP); error on fresh keys of the same rule as more pairs are read
    (32 sequences; each memory's step size chosen on 16 other sequences).  Then Titans' memory on a stream whose
    rule changes halfway: the surprise (the gradient's size) spikes at the change; momentum and a forgetting gate."""
    import torch

    torch.set_num_threads(1)
    d, H, n_read, n_test = 8, 32, 256, 128

    def teacher(gen):
        W1 = torch.randn(16, d, generator=gen) / math.sqrt(d) * 1.5
        W2 = torch.randn(d, 16, generator=gen) / math.sqrt(16)
        return lambda k: torch.tanh(k @ W1.T) @ W2.T

    def run(kind, lr, seed, momentum=0.0, forget=0.0, switch=None, trace=False):
        gen = torch.Generator().manual_seed(seed)
        f = teacher(gen)
        f2 = teacher(gen) if switch else None
        K = torch.randn(n_read, d, generator=gen)
        Kt = torch.randn(n_test, d, generator=gen)
        if kind == "linear":
            params = [torch.zeros(d, d, requires_grad=True)]
            fwd = lambda P, x: x @ P[0].T  # noqa: E731
        else:
            g2 = torch.Generator().manual_seed(10_000 + seed)
            params = [(torch.randn(H, d, generator=g2) / math.sqrt(d)).requires_grad_(),
                      torch.zeros(d, H, requires_grad=True)]
            fwd = lambda P, x: torch.tanh(x @ P[0].T) @ P[1].T  # noqa: E731
        mom = [torch.zeros_like(p) for p in params]
        errs, surprise = [], []
        for t in range(n_read):
            rule = f2 if (switch and t >= switch) else f
            k = K[t:t + 1]
            v = rule(k)
            loss = 0.5 * ((fwd(params, k) - v) ** 2).sum()
            grads = torch.autograd.grad(loss, params)
            surprise.append(float(sum(gg.norm() ** 2 for gg in grads).sqrt()))
            with torch.no_grad():
                for p, gg, m in zip(params, grads, mom):
                    m.mul_(momentum).add_(gg, alpha=-lr)  # Titans: surprise with momentum
                    p.mul_(1 - forget).add_(m)  # and a forgetting gate
            if trace or (t + 1) % 16 == 0:
                with torch.no_grad():
                    tgt = rule(Kt)
                    errs.append(float(((fwd(params, Kt) - tgt) ** 2).mean() / (tgt ** 2).mean()))
        return np.array(errs), np.array(surprise)

    lrs = {"linear": [0.05, 0.1, 0.2, 0.4], "mlp": [0.05, 0.1, 0.2, 0.4, 0.8]}
    best = {}
    for kind, grid in lrs.items():  # tune the step size on sequences 100..115
        scores = [np.mean([run(kind, lr, 100 + s)[0][-1] for s in range(16)]) for lr in grid]
        best[kind] = grid[int(np.argmin(scores))]
    out = dict(d=d, H=H, n_read=n_read, every=16, best_lr=best,
               params_linear=d * d, params_mlp=2 * d * H)
    for kind in lrs:
        E = np.array([run(kind, best[kind], s)[0] for s in range(32)])
        out[f"err_{kind}"] = E
        print(f"    TTT-{kind}: lr {best[kind]}, error after {n_read} pairs {np.median(E[:, -1]):.3f}", flush=True)
    # Titans on a stream whose rule changes at t = 128
    sw = n_read // 2
    for name, mo, fo in (("plain", 0.0, 0.0), ("titans", 0.6, 0.02)):
        E, S = zip(*[run("mlp", best["mlp"] * (1 - mo), 200 + s, momentum=mo, forget=fo, switch=sw, trace=True)
                     for s in range(16)])
        out[f"switch_err_{name}"], out[f"switch_surprise_{name}"] = np.array(E), np.array(S)
    out["switch"] = sw
    return out



# ---------------------------------------------------------------------------
# Recall: MQAR and RULER-style tests on small trained models (videos/ai/ai15/recall.py)
# ---------------------------------------------------------------------------
MQAR_GRID = dict(mixers=["softmax", "linear", "mamba2", "delta", "gdn", "hybrid"], dks=[2, 4, 8, 16],
                 seeds=[0, 1, 2], N=16, steps=1000, replay_dk=8)
RULER_GRID = dict(mixers=["softmax", "mamba2", "gdn", "hybrid"], seeds=[0, 1], T=128, steps=1500)


def _pool_run(fn, jobs: dict, part, workers: int = 2):
    """Run the jobs (key -> (callable, kwargs)) not yet in ``part`` in ``workers`` processes (spawn, one torch thread
    each), saving each result the moment it arrives."""
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor, as_completed

    todo = {k: kw for k, kw in jobs.items() if k not in part}
    if not todo:
        return
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(fn, **kw): k for k, kw in todo.items()}
        for f in as_completed(futs):
            k = futs[f]
            part[k] = f.result()
            r = part[k]
            print(f"    {k}: {r.get('acc', '')} ({r['seconds']:.0f}s)", flush=True)


def compute_mqar():
    """Multi-query associative recall (Arora et al., Zoology, 2023), N = 16 pairs: two-layer models with each memory
    (softmax attention; linear attention; a Mamba-2-style selective SSM; the delta rule; the gated delta rule; a
    hybrid, gated delta then attention), at four key sizes, three seeds each, equal steps (1,000) and equal
    parameters up to a few gates.  Recall on 1,024 fresh lists; the curve along training; and, for key size 8, which
    answers of one fixed list each model gets right at every evaluation (the replay)."""
    from videos.ai.ai15.recall import train_mqar

    G = MQAR_GRID
    part = CACHE.partial("mqar", G)
    jobs = {f"{m}_{dk}_{s}": dict(mixer=m, dk=dk, N=G["N"], seed=s, steps=G["steps"],
                                  replay=(s == 0 and dk == G["replay_dk"]))
            for dk in G["dks"] for m in G["mixers"] for s in G["seeds"]}
    _pool_run(train_mqar, jobs, part)
    out = dict(G)
    for m in G["mixers"]:
        out[f"acc_{m}"] = np.array([[part[f"{m}_{dk}_{s}"]["acc"] for s in G["seeds"]] for dk in G["dks"]])
        out[f"state_{m}"] = np.array([part[f"{m}_{dk}_0"]["state"] for dk in G["dks"]])
        out[f"params_{m}"] = int(part[f"{m}_{G['replay_dk']}_0"]["params"])
        out[f"curves_{m}"] = np.array([[np.asarray(part[f"{m}_{dk}_{s}"]["curve"])[:, 1] for s in G["seeds"]]
                                       for dk in G["dks"]])
        r = part[f"{m}_{G['replay_dk']}_0"]
        out[f"picks_{m}"] = np.array(r["picks"])
    out["curve_steps"] = np.asarray(part[f"softmax_{G['dks'][0]}_0"]["curve"])[:, 0]
    out["example"] = np.array(part[f"softmax_{G['replay_dk']}_0"]["example"])
    return out


def compute_ruler():
    """RULER-style tests (Hsieh et al. 2024) on small models trained at 128 tokens and tested at 128 to 1,024: one
    needle in filler; one needle among four (multi-key); a value passed along a chain of three names (variable
    tracking).  Softmax attention, a Mamba-2-style SSM, the gated delta rule and a hybrid; two seeds each."""
    from videos.ai.ai15.recall import train_ruler

    G = RULER_GRID
    part = CACHE.partial("ruler", G)
    jobs = {f"{m}_{s}": dict(mixer=m, seed=s, T=G["T"], steps=G["steps"]) for m in G["mixers"] for s in G["seeds"]}
    _pool_run(train_ruler, jobs, part)
    from videos.ai.ai15.recall import TASKS

    out = dict(G, tasks=list(TASKS), lengths=[128, 256, 512, 1024])
    for m in G["mixers"]:
        out[f"acc_{m}"] = np.array([[[part[f"{m}_{s}"]["acc"][f"{t}_{L}"] for L in out["lengths"]] for t in TASKS]
                                    for s in G["seeds"]])
        out[f"curve_{m}"] = np.array([np.asarray(part[f"{m}_{s}"]["curve"])[:, 1] for s in G["seeds"]])
        out[f"params_{m}"] = int(part[f"{m}_0"]["params"])
    out["curve_steps"] = np.asarray(part[f"{G['mixers'][0]}_0"]["curve"])[:, 0]
    return out



# ---------------------------------------------------------------------------
# A gated-delta hybrid language model on the novels, against a transformer (videos/ai/ai15/novels_lm.py)
# ---------------------------------------------------------------------------
LM_GRID = dict(runs=[("transformer", 0), ("hybrid", 0), ("transformer", 1), ("hybrid", 1), ("transformer", 2),
                     ("hybrid", 2)], steps=300)
COPY_GAPS = [16, 64, 128, 192, 384, 768]


def compute_lm():
    """Train the runs (resumable: a checkpoint every 100 steps), then measure each: bits per character on the
    scoreboard's passage (windows of 256, as Part 14), loss at each position of 1,024-token windows read in one go,
    and the copy test at growing distances."""
    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai15 import novels_lm as L

    import torch

    torch.set_num_threads(2)
    G = LM_GRID
    part = CACHE.partial("lm", G)
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    passage = c1.text("passage")
    _, va = N.token_arrays()
    for arch, seed in G["runs"]:
        key = f"{arch}_{seed}"
        if key in part:
            continue
        r = L.train(arch, seed, G["steps"], CACHE.dir)
        m = L.load_trained(arch, seed, CACHE.dir)
        r["bits"] = L.bits_per_char(m, passage)
        r["by_pos"] = L.loss_by_position(m, va).tolist()
        r["copy"] = L.copy_test(m, va, COPY_GAPS)
        print(f"    {key}: held-out {r['final_val']:.3f}, passage {r['bits']:.3f} bits/char, copy {r['copy']}", flush=True)
        part[key] = r
    out = dict(steps=G["steps"], gaps=COPY_GAPS, seq=L.SEQ, d=L.D, layers=L.LAYERS, archs=["transformer", "hybrid"],
               tokens=G["steps"] * L.BATCH * L.SEQ)
    for arch in ("transformer", "hybrid"):
        rs = [part[f"{a}_{s}"] for a, s in G["runs"] if a == arch]
        out[f"{arch}_bits"] = np.array([r["bits"] for r in rs])
        out[f"{arch}_val"] = np.array([r["final_val"] for r in rs])
        out[f"{arch}_params"] = int(rs[0]["params"])
        out[f"{arch}_curve"] = np.array([np.asarray(r["curve"])[:, 1] for r in rs])
        out[f"{arch}_snaps_val"] = np.array([[s_[1] for s_ in r["snaps"]] for r in rs])
        out[f"{arch}_samples"] = [s_[2] for s_ in rs[0]["snaps"]]
        out[f"{arch}_by_pos"] = np.array([r["by_pos"] for r in rs])
        out[f"{arch}_copy"] = np.array([[r["copy"][str(gp)] for gp in COPY_GAPS] for r in rs])
        out[f"{arch}_seconds"] = float(np.mean([r["seconds"] for r in rs]))
    rs0 = part[f"{G['runs'][0][0]}_0"]
    out["curve_steps"] = np.asarray(rs0["curve"])[:, 0]
    out["snap_steps"] = np.array([s_[0] for s_ in rs0["snaps"]])
    out["prompt"] = L.PROMPT
    return out


# ---------------------------------------------------------------------------
# The series' model with a smaller cache: sinks and heavy hitters (videos/ai/ai15/memory_lm.py)
# ---------------------------------------------------------------------------
STREAM_BUDGETS = [32, 64, 128]


def compute_sinks():
    """Where the series' model looks: each head's mean attention on the first token of 256-token windows of held-out
    text; then the scoreboard's passage (the first 2,000 tokens) read token by token with a cache of 32, 64 or 128
    tokens per head under three policies (window, four sinks plus a window, heavy hitters), and with everything kept
    (positions running past the 256 the model was trained on)."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai15 import memory_lm as M

    torch.set_num_threads(2)
    model = N.load_base()
    _, va = N.token_arrays()
    starts = np.linspace(0, len(va) - 300, 24).astype(int)
    win = torch.from_numpy(np.stack([va[s:s + 256] for s in starts]).astype(np.int64))
    first = M.attention_on_first(model, win)
    ids = N.encode(c1.text("passage"))[:2000]
    part = CACHE.partial("sinks", dict(budgets=STREAM_BUDGETS, n=len(ids), v=3))
    pols = ("window", "sinks", "h2o")
    runs = [("full", 0)] + [(p, b) for b in STREAM_BUDGETS for p in pols]
    if "full_0" not in part:
        part["full_0"] = M.stream_full(model, ids).tolist()
    for b in STREAM_BUDGETS:
        if f"h2o_{b}" not in part:
            res = M.stream(model, ids, list(pols), b)
            for p_, row in zip(pols, res):
                part[f"{p_}_{b}"] = row.tolist()
                print(f"    {p_}_{b}: {np.mean(row):.3f} nats a token", flush=True)
    # the reference: windows of 256 recomputed, each token with 128 to 256 tokens before it (Part 14's scoring)
    H, lp, _ = M.query_states(model, ids)
    ref = (-lp).numpy()
    chars = len(N.decode(ids))
    out = dict(first=first, uniform=float(np.mean(1.0 / np.arange(65, 257))), budgets=STREAM_BUDGETS, n=len(ids),
               chars=chars, ref=ref, seq=model.cfg.seq)
    for k in [f"{p}_{b}" for p, b in runs]:
        out[f"loss_{k}"] = np.array(part[k])
        out[f"bits_{k}"] = float(np.sum(part[k]) / math.log(2) / chars)
    out["bits_ref"] = float(ref.sum() / math.log(2) / chars)
    return out


# ---------------------------------------------------------------------------
# The kNN-LM on the novels
# ---------------------------------------------------------------------------
KNN = dict(k=64, window=256, keep=192, batch=24, fractions=[1 / 256, 1 / 64, 1 / 16, 1 / 4], tune_tokens=4000, seed=15)


def compute_knn():
    """Every token of the thirty novels as (the series' model's last hidden state, the next token): about 6.6 million
    pairs, of which a quarter (in a seeded random order) is used: about 1.6 million.  The memory is never stored
    whole: the stored states stream past the queries, each query keeping its 64 nearest (squared distance), with
    snapshots after 1/256, 1/64, 1/16 and 1/4 of the novels.  Queries: the scoreboard's passage, and held-out novel text to choose the mixing weight lambda and
    the temperature.  Resumable: the running nearest neighbours are checkpointed with the position in the order."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai15 import memory_lm as M

    torch.set_num_threads(2)
    P = KNN
    model = N.load_base()
    tr, va = N.token_arrays()
    passage = c1.text("passage")
    ids_p = N.encode(passage)
    ids_t = va[:P["tune_tokens"] + 1].astype(np.int64).tolist()
    Hp, lpp, yp = M.query_states(model, ids_p)
    Ht, lpt, yt = M.query_states(model, ids_t)
    Q = torch.cat([Hp, Ht])
    q2 = (Q ** 2).sum(-1, keepdim=True)
    nq, K = len(Q), P["k"]
    W, keep = P["window"], P["keep"]
    starts = np.arange(0, len(tr) - W - 1, keep)
    order = np.random.default_rng(P["seed"]).permutation(len(starts))
    n_all = len(order)
    order = order[:int(round(P["fractions"][-1] * n_all))]  # a quarter of the novels, in a seeded random order
    snaps_at = [int(round(f * n_all)) for f in P["fractions"]]
    ck = CACHE.dir / "knn.ckpt.npz"
    if ck.exists():
        z = np.load(ck)
        D, V, pos = torch.from_numpy(z["D"]), torch.from_numpy(z["V"]), int(z["pos"])
        snaps = {s_: (z[f"s{s_}D"], z[f"s{s_}V"]) for s_ in snaps_at if f"s{s_}D" in z.files}
        print(f"    resuming the kNN sweep at window {pos:,} of {len(order):,}", flush=True)
    else:
        D, V, pos, snaps = torch.full((nq, K), float("inf")), torch.zeros((nq, K), dtype=torch.long), 0, {}
    import time

    t0 = time.time()
    B = P["batch"]
    while pos < len(order):
        sel = order[pos:pos + B]
        x = torch.from_numpy(np.stack([tr[starts[i]:starts[i] + W + 1] for i in sel]).astype(np.int64))
        h, _ = M.hidden(model, x[:, :-1])
        keys = h[:, W - keep:].reshape(-1, h.shape[-1])
        vals = x[:, W - keep + 1:].reshape(-1)
        d = q2 - 2 * Q @ keys.T + (keys ** 2).sum(-1)[None]
        allD, allV = torch.cat([D, d], 1), torch.cat([V, vals[None].expand(nq, -1)], 1)
        D, ix = allD.topk(K, dim=1, largest=False)
        V = allV.gather(1, ix)
        pos += len(sel)
        for s_ in snaps_at:
            if s_ not in snaps and pos >= s_:
                snaps[s_] = (D.numpy().copy(), V.numpy().copy())
        if pos % (B * 40) == 0 or pos >= len(order):
            extra = {f"s{s_}D": a for s_, (a, b) in snaps.items()} | {f"s{s_}V": b for s_, (a, b) in snaps.items()}
            np.savez(str(ck) + ".tmp.npz", D=D.numpy(), V=V.numpy(), pos=pos, **extra)
            (CACHE.dir / "knn.ckpt.npz.tmp.npz").replace(ck)
            rate = (time.time() - t0) / max(pos, 1)
            print(f"    kNN sweep: {pos:,} of {len(order):,} windows ({rate * (len(order) - pos) / 60:.0f} min left)",
                  flush=True)
    npass = len(Hp)
    chars_p = len(passage)
    chars_t = len(N.decode(ids_t))
    out = dict(P, n_keys=int(len(order) * keep), n_all=int(n_all * keep), n_passage=npass, n_tune=len(Ht), chars=chars_p,
               base_bits=float(-lpp.sum() / math.log(2) / chars_p))
    lams = np.round(np.arange(0, 0.51, 0.05), 2)
    temps = [1.0, 2.0, 4.0, 8.0, 16.0]
    yall = torch.cat([yp, yt])
    for s_ in snaps_at:
        Ds, Vs = torch.from_numpy(snaps[s_][0]), torch.from_numpy(snaps[s_][1])
        best = None
        for T in temps:  # chosen on the held-out novel text, never on the passage
            pk = M.knn_prob(Ds, Vs, yall, T, K)
            pkt = pk[npass:]
            for lam in lams:
                bt = float(-torch.log(lam * pkt + (1 - lam) * lpt.exp()).sum() / math.log(2) / chars_t)
                if best is None or bt < best[0]:
                    best = (bt, T, float(lam))
        _, T, lam = best
        pk = M.knn_prob(Ds, Vs, yall, T, K)
        pkp = pk[:npass]
        curve = [float(-torch.log(l_ * pkp + (1 - l_) * lpp.exp()).sum() / math.log(2) / chars_p) for l_ in lams]
        frac = s_ / n_all
        out[f"snap_{s_}"] = dict(frac=frac, keys=int(s_ * keep), temp=T, lam=lam, tune_bits=best[0],
                                 bits=float(-torch.log(lam * pkp + (1 - lam) * lpp.exp()).sum() / math.log(2) / chars_p),
                                 lam_curve=curve)
        print(f"    kNN with {s_ * keep:,} stored: lambda {lam}, T {T}: {out[f'snap_{s_}']['bits']:.4f} bits/char "
              f"(model alone {out['base_bits']:.4f})", flush=True)
    out["snaps"] = snaps_at
    out["lams"] = lams
    full = snaps_at[-1]
    Ds, Vs = torch.from_numpy(snaps[full][0]), torch.from_numpy(snaps[full][1])
    sf = out[f"snap_{full}"]
    pk = M.knn_prob(Ds, Vs, yp, sf["temp"], K).numpy()
    p_lm = lpp.exp().numpy()
    mix = sf["lam"] * pk + (1 - sf["lam"]) * p_lm
    gain = np.log2(mix) - np.log2(p_lm)  # bits saved on each token of the passage
    out.update(gain=gain, p_knn=pk, p_lm=p_lm, passage_ids=np.array(ids_p[1:1 + npass]))
    # the tokens it helps most and hurts most, as text
    order_g = np.argsort(gain)
    out["best_tokens"] = [(N.decode([int(ids_p[i + 1])]), float(gain[i])) for i in order_g[::-1][:12]]
    out["worst_tokens"] = [(N.decode([int(ids_p[i + 1])]), float(gain[i])) for i in order_g[:12]]
    # one example query: the context, the true next token, and its nearest neighbours' next tokens
    j = int(order_g[::-1][0])
    out["example"] = dict(context=N.decode(ids_p[max(0, j - 12):j + 1]), target=N.decode([int(ids_p[j + 1])]),
                          neighbours=[N.decode([int(v)]) for v in Vs[j, :8]], p_lm=float(p_lm[j]), p_knn=float(pk[j]))
    ck.unlink(missing_ok=True)
    return out


def compute_selfcache():
    """The passage's own past as the memory (a continuous cache, Grave et al. 2017): each token's nearest earlier
    states in the same chapter, beyond the model's 256-token window too; mixed in as the kNN-LM is, with lambda and
    the temperature chosen on held-out novel text read the same way."""
    import torch

    from explainer.ai import novels as N
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai15 import memory_lm as M

    torch.set_num_threads(2)
    model = N.load_base()
    _, va = N.token_arrays()

    def run(ids, k=32):
        H, lp, y = M.query_states(model, ids)
        n = len(H)
        d = (H ** 2).sum(-1, keepdim=True) - 2 * H @ H.T + (H ** 2).sum(-1)[None]
        d = d.masked_fill(~torch.ones(n, n, dtype=torch.bool).tril(-1), float("inf"))  # only earlier tokens
        Dk, ix = d.topk(k, dim=1, largest=False)
        # the stored value of earlier token j is the token that followed it: y[j]
        return Dk, y[ix], y, lp

    passage = c1.text("passage")
    ids_p = N.encode(passage)
    tune = va[4000:10_000].astype(np.int64).tolist()
    Dp, Vp, yp, lpp = run(ids_p)
    Dt, Vt, yt, lpt = run(tune)
    chars_t = len(N.decode(tune))
    best = None
    for T in (1.0, 2.0, 4.0, 8.0, 16.0):
        pk = M.knn_prob(Dt.clamp_max(1e9), Vt, yt, T, 32)
        for lam in np.round(np.arange(0, 0.51, 0.05), 2):
            b = float(-torch.log(lam * pk + (1 - lam) * lpt.exp()).sum() / math.log(2) / chars_t)
            if best is None or b < best[0]:
                best = (b, T, float(lam))
    _, T, lam = best
    pk = M.knn_prob(Dp.clamp_max(1e9), Vp, yp, T, 32)
    mix = lam * pk + (1 - lam) * lpp.exp()
    chars = len(passage)
    gain = (torch.log2(mix) - torch.log2(lpp.exp())).numpy()
    return dict(temp=T, lam=lam, chars=chars, bits=float(-torch.log(mix).sum() / math.log(2) / chars),
                base_bits=float(-lpp.sum() / math.log(2) / chars), gain=gain)


ITEMS = {
    "kvcache": compute_kvcache,
    "linear": compute_linear,
    "capacity": compute_capacity,
    "ssm": compute_ssm,
    "delta": compute_delta,
    "mla": compute_mla,
    "hopfield": compute_hopfield,
    "matrix_rw": compute_matrix_rw,
    "scan": compute_scan,
    "hippo": compute_hippo,
    "zoh": compute_zoh,
    "ttt": compute_ttt,
    "mqar": compute_mqar,
    "ruler": compute_ruler,
    "lm": compute_lm,
    "sinks": compute_sinks,
    "knn": compute_knn,
    "selfcache": compute_selfcache,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
