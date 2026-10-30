"""Precompute everything numerical in Part 4 of the AI series ("Change").

    python -m videos.ai.ai4.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai4.compute --force train

Results are cached in ``.cache/ai4/<name>.json`` (+ ``.npz``).  The autodiff library the part builds is
``explainer/ai/autodiff.py``; this file checks it and trains with it.

Items (all small, on the CPU; the whole part computes in a few minutes):
    params     how many numbers GPT-2 small and Qwen3-4B have (read from their weight files' headers)
    linapprox  the derivative as the best linear approximation: its error against the step; tangent planes;
               directional derivatives around a circle (Cauchy-Schwarz)
    jacobians  the Jacobians of a softmax, a layer norm and a matrix product, by formula and by the library
    modes      forward against reverse mode, counted (multiply-adds) and timed, on networks with n inputs, m outputs
    tiny       the worked example: one input, one weight, one bias, a sigmoid and a squared error, forward and back
    mlp2       backpropagation through a two-layer network by hand (dW = delta x^T) against the library and PyTorch
    check      the library's gradients against finite differences and against PyTorch, on a small network
    train      Part 1's letter-pair model, 729 scores trained by gradient descent with the library on the books
    grad0      that model's first gradient, by the formula q - p (Part 1) and by the library
    gdlr       full-batch gradient descent on that model at five step sizes; the Hessian's top eigenvalue tracked
    floats     number formats: their ranges, the gap between neighbours (ulp) across the range, rounding, overflow
    cancel     catastrophic cancellation, (1 - cos x) / x^2 in float32 and float64
    vcurve     gradient checking: the error of finite differences against the step, in float32 and float64
    checkpoint memory against recomputation in backpropagation through a deep chain (checkpoints every k layers)
    newton     Newton's method against gradient descent on an ill-conditioned logistic regression
    hessian    Hessian-vector products (Pearlmutter), checked; the Hessian spectrum of a small network as it trains
    valley     gradient descent, momentum and Newton's method on a long narrow valley
    quad       gradient descent on quadratics: the rate against the condition number; the stability edge; saddles
    lagrange   Lagrange multipliers: a constrained minimum on a circle; maximum entropy (a die); RL's closed form
    kkt        KKT and duality: a support vector machine solved as primal and dual; a non-convex duality gap
    deq        implicit differentiation of a fixed point (a tiny deep equilibrium model) against unrolling; trained
"""

from __future__ import annotations

import json
import math
import struct

import numpy as np

from explainer.ai.autodiff import Tensor, cross_entropy, sigmoid, tape
from explainer.ai.cache import Cache

CACHE = Cache("ai4")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def count_safetensors(repo: str) -> int:
    """Parameters in a Hugging Face model, from the safetensors headers alone (no weights loaded)."""
    import urllib.request

    from huggingface_hub import hf_hub_url, list_repo_files

    def read(url: str, a: int, b: int) -> bytes:  # bytes a..b-1 of the file: the weights themselves are never downloaded
        req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b - 1}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()

    total = 0
    for f in [f for f in list_repo_files(repo) if f.endswith(".safetensors")]:
        url = hf_hub_url(repo, f)
        n = struct.unpack("<Q", read(url, 0, 8))[0]
        head = json.loads(read(url, 8, 8 + n))
        for k, v in head.items():
            if k != "__metadata__":
                total += int(np.prod(v["shape"]))
    return total


PARAMS_READ = dict(gpt2=124_439_808, qwen3_4b=4_022_468_096)  # as read from the weight files on 23 October 2026


def compute_params():
    try:
        import torch
        from transformers import AutoModelForCausalLM

        gpt2 = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
        n_gpt2 = sum(p.numel() for p in gpt2.parameters())  # the tied input/output matrix counted once
        n_qwen = count_safetensors("Qwen/Qwen3-4B-Base")
    except Exception as e:  # offline: the counts as read from the same files when this part was made
        print(f"  params: weight files unreachable ({type(e).__name__}); using the counts read on 23 October 2026")
        n_gpt2, n_qwen = PARAMS_READ["gpt2"], PARAMS_READ["qwen3_4b"]
    assert n_gpt2 == 124_439_808 and 4.0e9 < n_qwen < 4.1e9
    return dict(gpt2=int(n_gpt2), qwen3_4b=int(n_qwen))


# ---------------------------------------------------------------------------
TINY = dict(x=2.0, w=-1.5, b=0.5, y=1.0)


def compute_tiny():
    x, y = TINY["x"], TINY["y"]
    w, b = Tensor(TINY["w"], True), Tensor(TINY["b"], True)
    u = w * x
    z = u + b
    a = (-z).exp().__radd__(1.0) ** -1  # the sigmoid, 1 / (1 + e^-z)
    e = a - y
    L = e * e
    L.backward()
    vals = dict(u=float(u.data), z=float(z.data), a=float(a.data), e=float(e.data), L=float(L.data))
    # the same gradients by hand, node by node, from the loss back
    dL_de = 2 * vals["e"]
    dL_da = dL_de
    dL_dz = dL_da * vals["a"] * (1 - vals["a"])
    grads = dict(e=dL_de, a=dL_da, z=dL_dz, u=dL_dz, b=dL_dz, w=dL_dz * x)
    assert abs(grads["w"] - float(w.grad)) < 1e-12 and abs(grads["b"] - float(b.grad)) < 1e-12
    return dict(inputs=TINY, values=vals, grads=grads)


# ---------------------------------------------------------------------------
def compute_check():
    import torch

    g = rng(0)
    X = g.normal(size=(64, 10))
    y = g.integers(0, 5, 64)
    W1, b1, W2 = g.normal(size=(10, 16)) * 0.4, g.normal(size=16) * 0.1, g.normal(size=(16, 5)) * 0.4

    def ours(W1, b1, W2):
        a, b, c = Tensor(W1, True), Tensor(b1, True), Tensor(W2, True)
        loss = cross_entropy((Tensor(X) @ a + b).tanh() @ c, y)
        loss.backward()
        return float(loss.data), [a.grad, b.grad, c.grad]

    L, grads = ours(W1, b1, W2)
    ts = [torch.tensor(v, requires_grad=True) for v in (W1, b1, W2)]
    tl = torch.nn.functional.cross_entropy(torch.tanh(torch.tensor(X) @ ts[0] + ts[1]) @ ts[2], torch.tensor(y))
    tl.backward()
    torch_diff = max(float(np.abs(gr - t.grad.numpy()).max()) for gr, t in zip(grads, ts))
    # finite differences, one number at a time, on 60 randomly chosen numbers
    fd_diff, eps, shown = 0.0, 1e-6, []
    params = [W1, b1, W2]
    for _ in range(60):
        k = int(g.integers(0, 3))
        idx = tuple(int(g.integers(0, s)) for s in params[k].shape)
        plus = [p.copy() for p in params]
        minus = [p.copy() for p in params]
        plus[k][idx] += eps
        minus[k][idx] -= eps
        fd = (ours(*plus)[0] - ours(*minus)[0]) / (2 * eps)
        fd_diff = max(fd_diff, abs(fd - grads[k][idx]))
        if len(shown) < 5:
            shown.append((float(grads[k][idx]), float(fd)))
    assert torch_diff < 1e-12 and fd_diff < 1e-8
    return dict(loss=L, torch_loss=float(tl.detach()), torch_diff=torch_diff, fd_diff=fd_diff, shown=shown,
                n_params=int(sum(p.size for p in params)))


# ---------------------------------------------------------------------------
def compute_train():
    """729 scores z[prev, next]; q(next | prev) = softmax(z[prev]); minimize the cross-entropy on the books."""
    from videos.ai.ai1 import compute as c1

    tr = c1.codes27(c1.text("train27"))
    va = c1.codes27(c1.text("valid27"))
    if not c1.path("bigram").exists():
        c1._save("bigram", c1.ITEMS["bigram"]())
    H_cond = float(c1.load("bigram")["H_cond"])
    g = rng(3)
    z = Tensor(np.zeros((27, 27)), requires_grad=True)
    m, v = np.zeros((27, 27)), np.zeros((27, 27))  # Adam's running averages (Part 11)
    lr, b1, b2, B = 0.05, 0.9, 0.999, 4096
    steps, curve, snaps = 1500, [], {}
    for t in range(1, steps + 1):
        i = g.integers(0, len(tr) - 1, B)
        loss = cross_entropy(z[tr[i]], tr[i + 1])
        z.grad[:] = 0
        loss.backward()
        m = b1 * m + (1 - b1) * z.grad
        v = b2 * v + (1 - b2) * z.grad ** 2
        z.data -= lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + 1e-8)
        if t % 25 == 0 or t == 1:
            curve.append((t, float(loss.data) / math.log(2)))
        if t in (1, 50, 200, 1500):
            snaps[str(t)] = z.data.copy()
    # held-out bits per letter, and the scores against the log of the counts
    lp = z.data - np.log(np.exp(z.data).sum(1, keepdims=True))
    bits_valid = float(-lp[va[:-1], va[1:]].mean() / math.log(2))
    bits_train = float(-lp[tr[:-1], tr[1:]].mean() / math.log(2))
    cond = np.asarray(c1.load("bigram")["cond"])
    logc = np.log(np.maximum(cond, 1e-9))
    mask = cond > 1e-4
    corr = float(np.corrcoef(lp[mask], logc[mask])[0, 1])
    assert abs(bits_train - H_cond) < 0.02, (bits_train, H_cond)
    assert corr > 0.97
    return dict(curve=np.array(curve), bits_train=bits_train, bits_valid=bits_valid, H_cond=H_cond, corr=corr,
                z_final=z.data, logp=lp, logcond=logc, snaps=np.stack([snaps[k] for k in ("1", "50", "200", "1500")]),
                steps=steps, batch=B, lr=lr)


# ---------------------------------------------------------------------------
VALLEY = np.array([[1.0, 0.0], [0.0, 25.0]])  # f(x, y) = (x^2 + 25 y^2) / 2: curvatures 1 and 25


def compute_valley():
    H = VALLEY

    def grad(p):
        return H @ p

    start = np.array([-4.5, 0.9])
    out = dict(H=H, start=start)
    for name, lr, mom in (("gd", 0.075, 0.0), ("momentum", 0.03, 0.8)):
        p, vel, path = start.copy(), np.zeros(2), [start.copy()]
        for _ in range(60):
            vel = mom * vel - lr * grad(p)
            p = p + vel
            path.append(p.copy())
        out[name] = np.array(path)
    out["newton"] = np.array([start, start - np.linalg.solve(H, grad(start))])
    assert np.allclose(out["newton"][-1], 0)
    f = [0.5 * q @ H @ q for q in out["gd"]]
    out["gd_f"] = np.array(f)
    out["gd_steps_to_1pct"] = int(np.argmax(np.array(f) < 0.01 * f[0]))
    return out


# ---------------------------------------------------------------------------
# Chapter 1-2: the derivative and the gradient as best linear approximations
# ---------------------------------------------------------------------------
def bowl(x, y):
    """The landscape of chapters 2 and 3: a tilted bowl with a ripple (illustrative)."""
    return 0.18 * x * x + 0.32 * y * y + 0.35 * np.sin(1.3 * x) * np.cos(0.9 * y) + 0.6


def bowl_grad(x, y):
    return np.array([0.36 * x + 0.455 * np.cos(1.3 * x) * np.cos(0.9 * y),
                     0.64 * y - 0.315 * np.sin(1.3 * x) * np.sin(0.9 * y)])


BOWL_P0 = (1.6, -1.4)  # the point where chapter 2 measures slopes


def compute_linapprox():
    p0 = 0.25
    f = lambda p: math.log2(1 / p)  # noqa: E731  Part 1's surprise
    d1, d2 = -1 / (p0 * math.log(2)), 1 / (p0 ** 2 * math.log(2))
    hs = np.logspace(-4, -0.8, 33)
    err = np.array([abs(f(p0 + h) - f(p0) - d1 * h) for h in hs])
    slope = float(np.polyfit(np.log10(hs[:15]), np.log10(err[:15]), 1)[0])
    # a worse line through the same point: slope off by 10%; its error shrinks only like h
    err_bad = np.array([abs(f(p0 + h) - f(p0) - 1.1 * d1 * h) for h in hs])
    slope_bad = float(np.polyfit(np.log10(hs[:15]), np.log10(err_bad[:15]), 1)[0])
    # the tangent plane of the bowl: the worst error at distance r, over 64 directions
    p = np.array(BOWL_P0)
    gr = bowl_grad(*p)
    rs = np.logspace(-3, 0, 25)
    th = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    U = np.c_[np.cos(th), np.sin(th)]
    perr = np.array([max(abs(bowl(*(p + r * u)) - bowl(*p) - r * gr @ u) for u in U) for r in rs])
    pslope = float(np.polyfit(np.log10(rs[:10]), np.log10(perr[:10]), 1)[0])
    # directional derivatives around the circle, by finite differences
    ang = np.linspace(-np.pi, np.pi, 721)
    h = 1e-6
    D = np.array([(bowl(*(p + h * np.array([math.cos(a), math.sin(a)]))) -
                   bowl(*(p - h * np.array([math.cos(a), math.sin(a)])))) / (2 * h) for a in ang])
    g_ang = math.atan2(gr[1], gr[0])
    best = float(ang[int(np.argmax(D))])
    assert abs((best - g_ang + np.pi) % (2 * np.pi) - np.pi) < 0.01 and abs(D.max() / np.linalg.norm(gr) - 1) < 1e-4
    return dict(p0=p0, d1=d1, d2=d2, hs=hs, err=err, slope=slope, err_bad=err_bad, slope_bad=slope_bad,
                ratio=float(err[0] / hs[0] ** 2), rs=rs, perr=perr, pslope=pslope, ang=ang, D=D, g_ang=g_ang,
                best_ang=best, gnorm=float(np.linalg.norm(gr)), dmax=float(D.max()), grad=gr)


# ---------------------------------------------------------------------------
# Chapter 4: Jacobians of real layers
# ---------------------------------------------------------------------------
def _softmax_t(t: Tensor) -> Tensor:
    e = (t - Tensor(t.data.max())).exp()
    return e * e.sum() ** -1


def _layernorm_t(t: Tensor, eps: float) -> Tensor:
    c = t - t.mean()
    return c * ((c * c).mean() + eps) ** -0.5


def _jacobian_by_library(fn, x):
    """Row i of the Jacobian is the gradient of output i: one backward pass per output."""
    rows = []
    for i in range(fn(Tensor(x)).data.size):
        xt = Tensor(x, requires_grad=True)
        fn(xt)[i].backward()
        rows.append(xt.grad.copy())
    return np.array(rows)


def compute_jacobians():
    g = rng(4)
    z = g.normal(size=5) * 1.2
    p = np.exp(z - z.max())
    p /= p.sum()
    J_sm = np.diag(p) - np.outer(p, p)
    J_sm_lib = _jacobian_by_library(_softmax_t, z)
    eig_sm = np.linalg.eigvalsh(J_sm)
    # layer norm with eps
    eps = 1e-5
    x = g.normal(size=6) * 1.5 + 0.7
    mu, var = x.mean(), x.var()
    sig = math.sqrt(var + eps)
    y = (x - mu) / sig
    n = len(x)
    J_ln = (np.eye(n) - np.ones((n, n)) / n - np.outer(y, y) / n) / sig
    J_ln_lib = _jacobian_by_library(lambda t: _layernorm_t(t, eps), x)
    eig_ln = np.linalg.eigvalsh((J_ln + J_ln.T) / 2)
    # a matrix product's vector-Jacobian products
    X, W, G = g.normal(size=(4, 3)), g.normal(size=(3, 2)), g.normal(size=(4, 2))
    Xt, Wt = Tensor(X, True), Tensor(W, True)
    ((Xt @ Wt) * Tensor(G)).sum().backward()
    dX, dW = G @ W.T, X.T @ G
    # the full Jacobian dY/dW of one GPT-2 MLP matrix over a 1,024-token context, against its VJP
    T, d = 1024, 768
    jac_entries = (T * 4 * d) * (d * 4 * d)
    vjp_flops = 2 * T * d * 4 * d
    out = dict(z=z, p=p, J_sm=J_sm, J_sm_lib=J_sm_lib, sm_diff=float(np.abs(J_sm - J_sm_lib).max()), eig_sm=eig_sm,
               sm_null=float(np.abs(J_sm @ np.ones(5)).max()),
               x=x, y=y, sigma=sig, eps=eps, J_ln=J_ln, J_ln_lib=J_ln_lib, ln_diff=float(np.abs(J_ln - J_ln_lib).max()),
               eig_ln=eig_ln, ln_null1=float(np.abs(J_ln @ np.ones(n)).max()), ln_nully=float(np.abs(J_ln @ y).max()),
               X=X, W=W, G=G, dX=dX, dW=dW, mm_diff=float(max(np.abs(Xt.grad - dX).max(), np.abs(Wt.grad - dW).max())),
               jac_entries=float(jac_entries), jac_bytes=float(jac_entries * 4), vjp_flops=float(vjp_flops), T=T, d=d)
    assert out["sm_diff"] < 1e-12 and out["ln_diff"] < 1e-10 and out["mm_diff"] < 1e-12
    return out


# ---------------------------------------------------------------------------
# Chapter 5: forward against reverse mode, counted
# ---------------------------------------------------------------------------
def _mlp(widths, seed):
    g = rng(seed)
    return [(g.normal(size=(b, a)) / math.sqrt(a), g.normal(size=b) * 0.1) for a, b in zip(widths, widths[1:])]


def _jvp_inputs(params, x, V):
    """Forward mode: carry the tangents V (n x k, one column per direction) along with the values.
    Returns the outputs, the pushed-forward tangents (m x k) and the multiply-adds spent on tangents."""
    h, T, madds = x, V, 0
    for l, (W, b) in enumerate(params):
        z = W @ h + b
        T = W @ T
        madds += W.size * T.shape[1]
        if l < len(params) - 1:
            h = np.tanh(z)
            T = (1 - h * h)[:, None] * T
            madds += h.size * T.shape[1]
        else:
            h = z
    return h, T, madds


def _vjp_inputs(params, x, U):
    """Reverse mode: a forward pass that keeps every layer's output, then the cotangents U (m x k, one column per
    output direction) pulled back to the input.  Returns U^T J transposed (n x k) and the multiply-adds spent."""
    hs, h = [], x
    for l, (W, b) in enumerate(params):
        z = W @ h + b
        h = np.tanh(z) if l < len(params) - 1 else z
        hs.append(h)
    G, madds = U, 0
    for l in range(len(params) - 1, -1, -1):
        W, _ = params[l]
        if l < len(params) - 1:
            G = (1 - hs[l] * hs[l])[:, None] * G
            madds += hs[l].size * G.shape[1]
        G = W.T @ G
        madds += W.size * G.shape[1]
    return G, madds


def _timeit(fn, reps):
    import time

    fn()
    t = time.perf_counter()
    for _ in range(reps):
        fn()
    return (time.perf_counter() - t) / reps


def compute_modes():
    sizes = [1, 4, 16, 64, 256]
    H = 64
    fwd, rev, t_fwd, t_rev, primal = (np.zeros((len(sizes), len(sizes))) for _ in range(5))
    agree = 0.0
    for i, n in enumerate(sizes):
        for j, m in enumerate(sizes):
            params = _mlp([n, H, H, m], seed=10 + i * 7 + j)
            x = rng(99).normal(size=n)
            primal[i, j] = sum(W.size for W, _ in params) + 2 * H
            _, Jf, cf = _jvp_inputs(params, x, np.eye(n))   # n directions in: J, column by column
            JrT, cr = _vjp_inputs(params, x, np.eye(m))     # m directions out: J, row by row
            agree = max(agree, float(np.abs(Jf - JrT.T).max()))
            fwd[i, j], rev[i, j] = cf, cr
            t_fwd[i, j] = _timeit(lambda: [_jvp_inputs(params, x, np.eye(n)[:, k:k + 1]) for k in range(n)], 3)
            t_rev[i, j] = _timeit(lambda: [_vjp_inputs(params, x, np.eye(m)[:, k:k + 1]) for k in range(m)], 3)
    # the same Jacobian once more, by the library: one backward pass per output
    params = _mlp([16, H, H, 4], seed=10 + 2 * 7 + 1)
    x = rng(99).normal(size=16)

    def lib_f(t):
        h = t
        for l, (W, b) in enumerate(params):
            z = Tensor(W) @ h + Tensor(b)
            h = z.tanh() if l < len(params) - 1 else z
        return h

    J_lib = _jacobian_by_library(lib_f, x)
    _, J_fwd, _ = _jvp_inputs(params, x, np.eye(16))
    lib_diff = float(np.abs(J_lib - J_fwd).max())
    assert agree < 1e-10 and lib_diff < 1e-10

    # a classifier's loss: P parameters in, one number out
    g = rng(21)
    B, din, dh, k = 32, 16, 32, 10
    X, y = g.normal(size=(B, din)), g.integers(0, k, B)
    W1, b1 = g.normal(size=(din, dh)) / 4, np.zeros(dh)
    W2, b2 = g.normal(size=(dh, k)) / math.sqrt(dh), np.zeros(k)
    P = W1.size + b1.size + W2.size + b2.size
    Y = np.eye(k)[y]

    def reverse():
        ts = [Tensor(v, requires_grad=True) for v in (W1, b1, W2, b2)]
        loss = cross_entropy((Tensor(X) @ ts[0] + ts[1]).tanh() @ ts[2] + ts[3], y)
        loss.backward()
        return np.concatenate([t.grad.ravel() for t in ts])

    def forward_mode():
        """P tangent directions, one per parameter, pushed through the network beside the values."""
        z1 = X @ W1 + b1
        h = np.tanh(z1)
        z2 = h @ W2 + b2
        q = np.exp(z2 - z2.max(1, keepdims=True))
        q /= q.sum(1, keepdims=True)
        out, madds = np.zeros(P), 0
        for idx in range(P):
            dW1, db1, dW2, db2 = np.zeros_like(W1), np.zeros_like(b1), np.zeros_like(W2), np.zeros_like(b2)
            flat = [dW1, db1, dW2, db2]
            off = idx
            for a in flat:
                if off < a.size:
                    a.flat[off] = 1.0
                    break
                off -= a.size
            dz1 = X @ dW1 + db1
            dhid = (1 - h * h) * dz1
            dz2 = dhid @ W2 + h @ dW2 + db2
            out[idx] = float(((q - Y) * dz2).sum() / B)
            madds += B * din * dh + B * dh + 2 * B * dh * k + B * k  # dense products: forward mode cannot skip zeros
        return out, madds

    g_rev = reverse()
    g_fwd, madds_fwd = forward_mode()
    madds_rev = 2 * (B * din * dh + B * dh * k) + B * dh  # the backward pass: two products per matrix, one tanh'
    madds_primal = B * din * dh + B * dh * k
    t_r = _timeit(reverse, 20)
    t_f = _timeit(forward_mode, 1)
    grad_diff = float(np.abs(g_rev - g_fwd).max())
    assert grad_diff < 1e-12
    return dict(sizes=sizes, H=H, fwd=fwd, rev=rev, primal=primal, t_fwd=t_fwd, t_rev=t_rev, agree=agree,
                lib_diff=lib_diff, P=int(P), B=B, madds_fwd=float(madds_fwd), madds_rev=float(madds_rev),
                madds_primal=float(madds_primal), t_param_fwd=t_f, t_param_rev=t_r, grad_diff=grad_diff,
                net=[din, dh, k])


# ---------------------------------------------------------------------------
# Chapter 6: backpropagation through a two-layer network, by hand
# ---------------------------------------------------------------------------
def compute_mlp2():
    import torch

    g = rng(6)
    B, d, h, k = 8, 4, 5, 3
    X, y = g.normal(size=(B, d)), g.integers(0, k, B)
    W1, b1 = g.normal(size=(h, d)) * 0.6, g.normal(size=h) * 0.1  # column convention: z1 = W1 x + b1
    W2, b2 = g.normal(size=(k, h)) * 0.6, g.normal(size=k) * 0.1
    Y = np.eye(k)[y]
    # by hand, one example at a time, then summed: delta = dL/dz, dW = delta x^T
    dW1, db1, dW2, db2 = np.zeros_like(W1), np.zeros_like(b1), np.zeros_like(W2), np.zeros_like(b2)
    per_example = []
    L = 0.0
    for n in range(B):
        x = X[n]
        z1 = W1 @ x + b1
        a1 = np.tanh(z1)
        z2 = W2 @ a1 + b2
        q = np.exp(z2 - z2.max())
        q /= q.sum()
        L += -math.log(q[y[n]]) / B
        d2 = (q - Y[n]) / B                 # softmax + cross-entropy: q - y (Part 1)
        d1 = (W2.T @ d2) * (1 - a1 * a1)    # back through W2, then through tanh
        dW2 += np.outer(d2, a1)
        db2 += d2
        dW1 += np.outer(d1, x)
        db1 += d1
        per_example.append(np.outer(d1, x) * B)
    # the library (row convention: parameters stored transposed)
    ts = [Tensor(v, requires_grad=True) for v in (W1.T, b1, W2.T, b2)]
    loss = cross_entropy((Tensor(X) @ ts[0] + ts[1]).tanh() @ ts[2] + ts[3], y)
    loss.backward()
    lib = [ts[0].grad.T, ts[1].grad, ts[2].grad.T, ts[3].grad]
    # PyTorch
    tt = [torch.tensor(v, requires_grad=True) for v in (W1, b1, W2, b2)]
    tl = torch.nn.functional.cross_entropy(torch.tanh(torch.tensor(X) @ tt[0].T + tt[1]) @ tt[2].T + tt[3],
                                           torch.tensor(y))
    tl.backward()
    hand = [dW1, db1, dW2, db2]
    d_lib = max(float(np.abs(a - b).max()) for a, b in zip(hand, lib))
    d_torch = max(float(np.abs(a - t.grad.numpy()).max()) for a, t in zip(hand, tt))
    sv_one = np.linalg.svd(per_example[0], compute_uv=False)
    sv_all = np.linalg.svd(dW1, compute_uv=False)
    assert d_lib < 1e-12 and d_torch < 1e-12 and abs(L - float(loss.data)) < 1e-12
    x0 = X[0]
    z1 = W1 @ x0 + b1
    a1 = np.tanh(z1)
    z2 = W2 @ a1 + b2
    q0 = np.exp(z2 - z2.max())
    q0 /= q0.sum()
    d2_0 = q0 - Y[0]
    d1_0 = (W2.T @ d2_0) * (1 - a1 * a1)
    return dict(B=B, dims=[d, h, k], loss=L, d_lib=d_lib, d_torch=d_torch, sv_one=sv_one, sv_all=sv_all,
                x0=x0, d1_0=d1_0, d2_0=d2_0, a1_0=a1, q0=q0, y0=int(y[0]), dW1_0=per_example[0], dW1=dW1, dW2=dW2,
                n_params=int(W1.size + b1.size + W2.size + b2.size))


# ---------------------------------------------------------------------------
# Chapter 7: the tape of the worked example
# ---------------------------------------------------------------------------
def compute_tape():
    x, y = TINY["x"], TINY["y"]
    w, b = Tensor(TINY["w"], True), Tensor(TINY["b"], True)
    z = w * x + b
    a = sigmoid(z)
    e = a - y
    L = e * e
    t = tape(L)
    L.backward()
    tiny = compute_tiny()
    assert abs(float(w.grad) - tiny["grads"]["w"]) < 1e-12
    # the same list for the two-layer network of chapter 6
    g = rng(6)
    X, yy = g.normal(size=(8, 4)), g.integers(0, 3, 8)
    ts = [Tensor(g.normal(size=s), requires_grad=True) for s in ((4, 5), (5,), (5, 3), (3,))]
    loss = cross_entropy((Tensor(X) @ ts[0] + ts[1]).tanh() @ ts[2] + ts[3], yy)
    t2 = tape(loss)
    return dict(tape=t, n_tape=len(t), tape2=[dict(op=e["op"], args=e["args"], shape=list(e["shape"])) for e in t2],
                n_tape2=len(t2), wgrad=float(w.grad))


# ---------------------------------------------------------------------------
# Chapter 9: the letter model's first gradient
# ---------------------------------------------------------------------------
def compute_grad0():
    from videos.ai.ai1 import compute as c1

    tr = c1.codes27(c1.text("train27"))[:300_001]
    N = np.zeros((27, 27))
    np.add.at(N, (tr[:-1], tr[1:]), 1)
    n_i = N.sum(1)
    phat = N / np.maximum(n_i, 1)[:, None]
    formula = (n_i / N.sum())[:, None] * (1 / 27 - phat)  # the share of pairs that start with i, times q - p-hat
    z = Tensor(np.zeros((27, 27)), requires_grad=True)
    cross_entropy(z[tr[:-1]], tr[1:]).backward()
    diff = float(np.abs(z.grad - formula).max())
    assert diff < 1e-12
    top = np.unravel_index(np.argsort(formula.ravel())[:3], formula.shape)
    return dict(grad=formula, diff=diff, pairs=int(len(tr) - 1), top=[(int(i), int(j)) for i, j in zip(*top)])


# ---------------------------------------------------------------------------
# Chapters 10-11: numbers in a computer
# ---------------------------------------------------------------------------
FORMATS = {  # name: (exponent bits, mantissa bits)
    "fp64": (11, 52), "fp32": (8, 23), "bf16": (8, 7), "fp16": (5, 10), "e5m2": (5, 2), "e4m3": (4, 3),
}


def _positive_values(name):
    """Every finite positive value of a format, in order, by enumerating its bit patterns."""
    import torch

    if name == "fp16":
        return np.arange(1, 0x7C00, dtype=np.uint16).view(np.float16).astype(np.float64)
    if name == "bf16":
        return torch.arange(1, 0x7F80, dtype=torch.int16).view(torch.bfloat16).double().numpy()
    if name == "e5m2":
        return torch.arange(1, 0x7C, dtype=torch.uint8).view(torch.float8_e5m2).double().numpy()
    if name == "e4m3":
        return torch.arange(1, 0x7F, dtype=torch.uint8).view(torch.float8_e4m3fn).double().numpy()
    raise KeyError(name)


def _round(v, name):
    import torch

    dt = dict(fp64=torch.float64, fp32=torch.float32, bf16=torch.bfloat16, fp16=torch.float16,
              e5m2=torch.float8_e5m2, e4m3=torch.float8_e4m3fn)[name]
    return torch.tensor(np.asarray(v, float), dtype=torch.float64).to(dt).double().numpy()


def compute_floats():
    import torch

    xs = np.logspace(-8, 6, 561)
    info, ulp = {}, {}
    for name, (e, m) in FORMATS.items():
        dt = dict(fp64=torch.float64, fp32=torch.float32, bf16=torch.bfloat16, fp16=torch.float16,
                  e5m2=torch.float8_e5m2, e4m3=torch.float8_e4m3fn)[name]
        fi = torch.finfo(dt)
        info[name] = dict(exp=e, man=m, bits=1 + e + m, eps=float(fi.eps), max=float(fi.max),
                          min_normal=float(fi.smallest_normal), digits=float(m * math.log10(2) + math.log10(2)))
        if name in ("fp64", "fp32"):
            npdt = np.float64 if name == "fp64" else np.float32
            u = np.array([float(np.spacing(npdt(x))) for x in xs])
            u[xs > fi.max] = np.nan
            ulp[name] = u
        else:
            vals = _positive_values(name)
            info[name]["min_sub"] = float(vals[0])
            info[name]["count"] = int(len(vals))
            idx = np.searchsorted(vals, xs, side="right") - 1
            u = np.full(len(xs), np.nan)
            ok = (idx >= 0) & (idx < len(vals) - 1)
            u[ok] = vals[idx[ok] + 1] - vals[idx[ok]]
            ulp[name] = u
    # rounding: what survives
    rounding = dict(
        bf16_1p=float(_round(1 + 2 ** -8, "bf16")), fp16_1p=float(_round(1 + 2 ** -8, "fp16")),
        bf16_257=float(_round(257, "bf16")), fp16_2049=float(_round(2049, "fp16")),
        fp32_2p24p1=float(np.float32(2 ** 24 + 1)), e4m3_pi=float(_round(math.pi, "e4m3")),
        bf16_pi=float(_round(math.pi, "bf16")), fp16_pi=float(_round(math.pi, "fp16")),
        fp32_pi=float(np.float32(math.pi)), fp32_tenth=float(np.float32(0.1)),
    )
    # accumulation: add 0.01 ten thousand times, rounding the running sum to the format each time
    steps, inc = 10_000, 0.01
    acc = {}
    for name in ("fp32", "fp16", "bf16"):
        dt = dict(fp32=torch.float32, fp16=torch.float16, bf16=torch.bfloat16)[name]
        s = torch.zeros((), dtype=dt)
        a = torch.tensor(inc, dtype=dt)
        traj = []
        for t in range(1, steps + 1):
            s = (s + a).to(dt)
            if t % 100 == 0:
                traj.append(float(s))
        acc[name] = np.array(traj)
    # bf16 numbers, an fp32 running sum (what a tensor core does)
    s32 = torch.zeros((), dtype=torch.float32)
    a16 = torch.tensor(inc, dtype=torch.bfloat16).float()
    traj = []
    for t in range(1, steps + 1):
        s32 = s32 + a16
        if t % 100 == 0:
            traj.append(float(s32))
    acc["bf16_fp32acc"] = np.array(traj)
    # the log-sum-exp trick: three logits, naive and shifted
    z = np.array([1000.0, 999.0, 998.0], dtype=np.float32)
    with np.errstate(over="ignore", invalid="ignore"):
        e_naive = np.exp(z)
        p_naive = e_naive / e_naive.sum()
    m = z.max()
    e_shift = np.exp(z - m)
    p_shift = e_shift / e_shift.sum()
    lse = float(m + np.log(e_shift.sum()))
    z16 = torch.tensor([12.0, 11.0, 10.0], dtype=torch.float16)
    e16 = torch.exp(z16)
    p16_shift = torch.softmax(z16.float(), 0)
    overflow_at = {n: math.log(info[n]["max"]) for n in info}
    return dict(info=info, xs=xs, **{f"ulp_{k}": v for k, v in ulp.items()}, rounding=rounding,
                acc_steps=steps, acc_inc=inc, **{f"acc_{k}": v for k, v in acc.items()},
                lse_z=z.astype(float), lse_naive_e=[str(v) for v in e_naive], lse_naive_p=[str(v) for v in p_naive],
                lse_p=p_shift.astype(float), lse=lse, fp16_e=[str(float(v)) for v in e16],
                fp16_shift_p=p16_shift.numpy().astype(float), overflow_at=overflow_at)


def compute_cancel():
    xs = np.logspace(-6, 0, 241)
    exact = np.array([2 * math.sin(x / 2) ** 2 / x ** 2 for x in xs])  # float64, no cancellation
    out = {"xs": xs, "exact": exact}
    for name, dt in (("fp32", np.float32), ("fp64", np.float64)):
        x = xs.astype(dt)
        naive = (dt(1) - np.cos(x)) / (x * x)
        stable = dt(2) * np.sin(x / dt(2)) ** 2 / (x * x)
        out[f"naive_{name}"] = np.abs(naive.astype(float) - exact) / exact
        out[f"stable_{name}"] = np.abs(stable.astype(float) - exact) / exact
    u32, u64 = 2.0 ** -24, 2.0 ** -53
    out["pred_fp32"] = u32 / (xs ** 2 / 2)  # rounding error of size u in 1 - cos x, relative to x^2/2
    out["pred_fp64"] = u64 / (xs ** 2 / 2)
    x0 = 1e-4
    out["x0"] = x0
    out["naive32_x0"] = float((np.float32(1) - np.cos(np.float32(x0))) / np.float32(x0) ** 2)
    out["stable32_x0"] = float(np.float32(2) * np.sin(np.float32(x0) / np.float32(2)) ** 2 / np.float32(x0) ** 2)
    out["cos32_x0"] = repr(float(np.cos(np.float32(x0))))
    # where float32's naive formula first goes wrong by 100% (the answer is all rounding)
    bad = out["naive_fp32"] >= 0.5
    out["x_dead32"] = float(xs[bad].max()) if bad.any() else 0.0
    return out


def _check_net(dtype):
    """Chapter 7's 256-number network as a plain function of its parameters, in a chosen precision."""
    g = rng(0)
    X = g.normal(size=(64, 10))
    y = g.integers(0, 5, 64)
    W1, b1, W2 = g.normal(size=(10, 16)) * 0.4, g.normal(size=16) * 0.1, g.normal(size=(16, 5)) * 0.4
    theta = np.concatenate([W1.ravel(), b1, W2.ravel()])
    Xd = X.astype(dtype)

    def f(th):
        th = np.asarray(th, dtype=dtype)
        a, b, c = th[:160].reshape(10, 16), th[160:176], th[176:].reshape(16, 5)
        z = np.tanh(Xd @ a + b) @ c
        m = z.max(1, keepdims=True)
        lse = m[:, 0] + np.log(np.exp(z - m).sum(1))
        return float((lse - z[np.arange(64), y]).mean(dtype=dtype))

    def grad(th):
        a, b, c = (Tensor(v, requires_grad=True) for v in (th[:160].reshape(10, 16), th[160:176], th[176:].reshape(16, 5)))
        cross_entropy((Tensor(X) @ a + b).tanh() @ c, y).backward()
        return np.concatenate([a.grad.ravel(), b.grad, c.grad.ravel()])

    return f, grad, theta


def compute_vcurve():
    hs = np.logspace(-13, 0, 66)
    g = rng(17)
    f64, grad, theta = _check_net(np.float64)
    f32, _, _ = _check_net(np.float32)
    gr = grad(theta)
    ndir = 8
    out = dict(hs=hs, ndir=ndir)
    pred, meas = {}, {}
    for name, f, u in (("fp64", f64, 2.0 ** -53), ("fp32", f32, 2.0 ** -24)):
        C, F = [], []
        ph_c, ph_f, mh_c, mh_f = [], [], [], []
        for k in range(ndir):
            v = g.normal(size=theta.size)
            v /= np.linalg.norm(v)
            exact = float(gr @ v)
            ce = np.array([abs((f(theta + h * v) - f(theta - h * v)) / (2 * h) - exact) for h in hs])
            fe = np.array([abs((f(theta + h * v) - f(theta)) / h - exact) for h in hs])
            C.append(ce)
            F.append(fe)
            # the curvature terms along v, in float64 with a step large enough to be safe
            hh = 1e-2
            f0 = f64(theta)
            d2 = (f64(theta + hh * v) - 2 * f0 + f64(theta - hh * v)) / hh ** 2
            d3 = (f64(theta + 2 * hh * v) - 2 * f64(theta + hh * v) + 2 * f64(theta - hh * v)
                  - f64(theta - 2 * hh * v)) / (2 * hh ** 3)
            ph_c.append((3 * u * abs(f0) / abs(d3)) ** (1 / 3))
            ph_f.append(2 * math.sqrt(u * abs(f0) / abs(d2)))
            mh_c.append(float(hs[int(np.argmin(ce))]))
            mh_f.append(float(hs[int(np.argmin(fe))]))
        out[f"central_{name}"] = np.median(np.array(C), 0)
        out[f"forward_{name}"] = np.median(np.array(F), 0)
        out[f"central_{name}_all"] = np.array(C)
        pred[name] = dict(central=float(np.median(ph_c)), forward=float(np.median(ph_f)))
        meas[name] = dict(central=float(np.median(mh_c)), forward=float(np.median(mh_f)),
                          central_err=float(out[f"central_{name}"].min()), forward_err=float(out[f"forward_{name}"].min()))
        # slopes on the two sides of the V (central): +2 on the right (truncation), -1 on the left (roundoff)
        c = out[f"central_{name}"]
        hc = meas[name]["central"]
        right = (hs > hc * 30) & (hs < 0.1)
        left = (hs < hc / 3) & (hs > hc / 1000) & (c < 0.3 * c[0]) & (c > 0)
        out[f"slope_right_{name}"] = float(np.polyfit(np.log10(hs[right]), np.log10(c[right]), 1)[0]) if right.sum() > 2 else float("nan")
        out[f"slope_left_{name}"] = float(np.polyfit(np.log10(hs[left]), np.log10(c[left]), 1)[0]) if left.sum() > 2 else float("nan")
    out["pred"], out["meas"] = pred, meas
    out["at_1e-6_fp64"] = float(np.interp(-6, np.log10(hs), np.log10(out["central_fp64"])))
    out["loss"] = f64(theta)
    return out


# ---------------------------------------------------------------------------
# Chapter 12: checkpointing
# ---------------------------------------------------------------------------
class _Chain:
    """h_{k+1} = tanh(W_k h_k), k = 0..n-1; loss = |h_n|^2 / 2.  Counts layer evaluations and the activations held."""

    def __init__(self, n, w=16, seed=12):
        g = rng(seed)
        self.n, self.W = n, g.normal(size=(n, w, w)) * (1.1 / math.sqrt(w))
        self.x0 = g.normal(size=w)
        self.evals = 0
        self.held = 0
        self.peak = 0

    def f(self, k, h):
        self.evals += 1
        return np.tanh(self.W[k] @ h)

    def hold(self, k=1):
        self.held += k
        self.peak = max(self.peak, self.held)

    def drop(self, k=1):
        self.held -= k

    def back(self, k, h_out, g):
        gz = g * (1 - h_out * h_out)
        return self.W[k].T @ gz

    def run(self, every):
        """Backpropagation keeping a checkpoint every ``every`` layers (``every`` = 1: keep everything; ``every`` = n:
        keep only the input and the output, recomputing the rest once).  Returns dL/dx0."""
        n = self.n
        self.evals = self.held = self.peak = 0
        cps = {0: self.x0}
        self.hold()
        h = self.x0
        for k in range(n):
            h = self.f(k, h)
            if (k + 1) % every == 0 or k + 1 == n:
                cps[k + 1] = h
                self.hold()
        g = h.copy()  # dL/dh_n for L = |h_n|^2 / 2
        for s in sorted((c for c in cps if c < n), reverse=True):
            end = min(s + every, n)
            seg = {s: cps[s], end: cps[end]}
            hh = cps[s]
            for k in range(s, end - 1):  # recompute the inside of the segment from its checkpoint
                hh = self.f(k, hh)
                seg[k + 1] = hh
                self.hold()
            for k in range(end - 1, s - 1, -1):
                g = self.back(k, seg[k + 1], g)
                self.drop()  # h_{k+1} (a recomputed one, or the checkpoint at the segment's end) is done with
        self.drop()  # the input
        assert self.held == 0
        return g

    def run_none(self):
        """Keep nothing but the input: recompute every layer's input from the start when the backward pass needs it."""
        n = self.n
        self.evals = self.held = self.peak = 0
        self.hold()
        h = self.x0
        for k in range(n):
            h = self.f(k, h)
        g = h.copy()
        self.hold()
        for k in range(n - 1, -1, -1):
            hh = self.x0
            for j in range(k + 1):
                hh = self.f(j, hh)
            self.hold()
            g = self.back(k, hh, g)
            self.drop()
        self.drop(2)
        return g


def compute_checkpoint():
    import time

    n = 256
    ref = _Chain(n).run(1)
    ks = list(range(1, n + 1))
    peak, evals, worst = [], [], 0.0
    for k in ks:
        c = _Chain(n)
        gk = c.run(k)
        worst = max(worst, float(np.abs(gk - ref).max()))
        peak.append(c.peak)
        evals.append(c.evals)
    peak, evals = np.array(peak), np.array(evals)
    kbest = int(ks[int(np.argmin(peak))])
    kset = [k for k, pk in zip(ks, peak) if pk == peak.min()]
    # the best interval for longer chains
    ns = [16, 64, 256, 1024, 4096]
    best_k, best_peak = [], []
    for nn in ns:
        cands = sorted({max(1, int(round(math.sqrt(nn) * f))) for f in (0.5, 0.71, 0.85, 1.0, 1.2, 1.41, 2.0)}
                       | set(range(max(1, int(math.sqrt(nn)) - 3), int(math.sqrt(nn)) + 4)))
        res = []
        for k in cands:
            c = _Chain(nn, seed=13)
            c.run(k)
            res.append((c.peak, k))
        pk = min(res)[0]
        ties = [k for p_, k in res if p_ == pk]
        best_k.append(ties[len(ties) // 2])
        best_peak.append(pk)
    # time: everything kept against sqrt(n) checkpoints, on a longer, wider chain
    big = _Chain(1024, w=64, seed=14)
    t_all = _timeit(lambda: big.run(1), 3)
    t_ck = _timeit(lambda: big.run(32), 3)
    c = _Chain(n)
    g_none = c.run_none()
    none_peak, none_evals = c.peak, c.evals
    worst = max(worst, float(np.abs(g_none - ref).max()))
    assert worst < 1e-12
    return dict(n=n, ks=np.array(ks), peak=peak, evals=evals, kbest=kbest, klo=int(min(kset)), khi=int(max(kset)), worst=worst, ns=ns, best_k=best_k,
                best_peak=best_peak, t_all=t_all, t_ck=t_ck, store_all_peak=int(peak[0]), store_all_evals=int(evals[0]),
                none_peak=int(none_peak), none_evals=int(none_evals))


# ---------------------------------------------------------------------------
# Chapter 13: Newton against gradient descent
# ---------------------------------------------------------------------------
def compute_newton():
    g = rng(31)
    N = 400
    u = g.normal(size=N)
    X = np.c_[u, 0.95 * u + 0.06 * g.normal(size=N)]  # two strongly correlated features
    w_true = np.array([1.5, -1.0])
    y = np.where(g.random(N) < 1 / (1 + np.exp(-X @ w_true * 2.0)), 1.0, -1.0)
    lam = 1e-3

    def f(w):
        return float(np.logaddexp(0, -y * (X @ w)).mean() + lam / 2 * w @ w)

    def grad(w):
        s = 1 / (1 + np.exp(y * (X @ w)))
        return -(X * (y * s)[:, None]).mean(0) + lam * w

    def hess(w):
        p = 1 / (1 + np.exp(-(X @ w)))
        return (X * (p * (1 - p))[:, None]).T @ X / N + lam * np.eye(2)

    w = np.zeros(2)
    newton = [w.copy()]
    for _ in range(12):
        w = w - np.linalg.solve(hess(w), grad(w))
        newton.append(w.copy())
    w_star = w
    f_star = f(w_star)
    H = hess(w_star)
    ev = np.linalg.eigvalsh(H)
    L = np.linalg.eigvalsh(X.T @ X / N).max() / 4 + lam  # the curvature is never more than this
    eta = 1 / L
    w = np.zeros(2)
    gd = [w.copy()]
    gd_err = [f(w) - f_star]
    for t in range(200_000):
        w = w - eta * grad(w)
        if t < 3000 or t % 50 == 0:
            gd.append(w.copy())
        gd_err.append(f(w) - f_star)
        if gd_err[-1] < 1e-10:
            break
    gd_steps = len(gd_err) - 1
    newton_err = [max(f(q) - f_star, 1e-17) for q in newton]
    newton_steps = int(next(i for i, e in enumerate(newton_err) if e < 1e-10))
    gnorm = [float(np.linalg.norm(grad(q))) for q in newton]
    return dict(X=X, y=y, lam=lam, w_star=w_star, f_star=f_star, eig=ev, kappa=float(ev[1] / ev[0]), eta=eta,
                newton=np.array(newton), newton_err=np.array(newton_err), newton_steps=newton_steps,
                newton_gnorm=np.array(gnorm), gd=np.array(gd), gd_err=np.array(gd_err[::max(1, len(gd_err) // 2000)]),
                gd_err_stride=max(1, len(gd_err) // 2000), gd_steps=gd_steps,
                gd_err_full_first=np.array(gd_err[:200]))


# ---------------------------------------------------------------------------
# Chapter 14: Hessian-vector products, and the Hessian of a small network as it trains
# ---------------------------------------------------------------------------
def _spirals(n_per=100, seed=41):
    g = rng(seed)
    X, y = [], []
    for c in range(3):
        r = np.linspace(0.15, 1.0, n_per)
        t = c * 2 * np.pi / 3 + r * 3.2 + g.normal(size=n_per) * 0.18
        X.append(np.c_[r * np.cos(t), r * np.sin(t)])
        y.append(np.full(n_per, c))
    return np.concatenate(X), np.concatenate(y)


def compute_hessian():
    import time

    import torch

    torch.set_num_threads(1)
    torch.manual_seed(0)
    X, y = _spirals()
    Xt, yt = torch.tensor(X), torch.tensor(y)
    sizes = [2, 16, 16, 3]
    shapes = [(b, a) for a, b in zip(sizes, sizes[1:])]
    g = rng(42)
    parts = []
    for o, i in shapes:
        parts += [g.normal(size=(o, i)) * math.sqrt(1.0 / i), np.zeros(o)]
    theta0 = np.concatenate([p.ravel() for p in parts])
    P = theta0.size

    def unflat(th):
        out, k = [], 0
        for o, i in shapes:
            out.append(th[k:k + o * i].reshape(o, i))
            k += o * i
            out.append(th[k:k + o])
            k += o
        return out

    def loss_fn(th, Xb=Xt, yb=yt):
        ps = unflat(th)
        h = Xb
        for l in range(len(shapes)):
            h = h @ ps[2 * l].T + ps[2 * l + 1]
            if l < len(shapes) - 1:
                h = torch.tanh(h)
        return torch.nn.functional.cross_entropy(h, yb)

    def logits(th, Xb):
        ps = unflat(th)
        h = Xb
        for l in range(len(shapes)):
            h = h @ ps[2 * l].T + ps[2 * l + 1]
            if l < len(shapes) - 1:
                h = torch.tanh(h)
        return h

    xs = np.linspace(-1.25, 1.25, 56)
    grid = torch.tensor(np.stack(np.meshgrid(xs, xs), -1).reshape(-1, 2))
    th = torch.tensor(theta0, requires_grad=True)
    opt = torch.optim.Adam([th], lr=0.01)
    steps = 3000
    keep = [0, 30, 100, 300, 1000, 3000]
    curve, snaps = [], []
    for t in range(steps + 1):
        loss = loss_fn(th)
        if t % 10 == 0:
            curve.append((t, float(loss)))
        if t in keep:
            with torch.no_grad():
                acc = float((logits(th, Xt).argmax(1) == yt).double().mean())
                region = logits(th, grid).softmax(1).numpy()
            Hm = torch.autograd.functional.hessian(lambda v: loss_fn(v), th.detach())
            ev = np.linalg.eigvalsh(Hm.numpy())
            snaps.append(dict(t=t, loss=float(loss), acc=acc, eig=ev, region=region, theta=th.detach().numpy().copy()))
        if t == steps:
            break
        opt.zero_grad()
        loss.backward()
        opt.step()
    # Pearlmutter's trick at the trained parameters: Hv = d/dt grad(theta + t v), by differentiating the gradient
    thf = torch.tensor(snaps[-1]["theta"], requires_grad=True)
    v = torch.tensor(rng(43).normal(size=P))
    v = v / v.norm()

    def hvp(vec):
        gr = torch.autograd.grad(loss_fn(thf), thf, create_graph=True)[0]
        return torch.autograd.grad(gr @ vec, thf)[0]

    def gradient(t_):
        t_ = t_.detach().requires_grad_(True)
        return torch.autograd.grad(loss_fn(t_), t_)[0]

    Hv = hvp(v)
    Hfull = torch.autograd.functional.hessian(lambda q: loss_fn(q), thf.detach())
    hv_full_diff = float((Hv - Hfull @ v).abs().max())
    hs = np.logspace(-10, -1, 37)
    fd_err = []
    for h in hs:
        fd = (gradient(thf + h * v) - gradient(thf - h * v)) / (2 * h)
        fd_err.append(float((fd - Hv).norm() / Hv.norm()))
    fd_err = np.array(fd_err)
    reps = 200
    t0 = time.perf_counter()
    for _ in range(reps):
        gradient(thf)
    t_grad = (time.perf_counter() - t0) / reps
    t0 = time.perf_counter()
    for _ in range(reps):
        hvp(v)
    t_hvp = (time.perf_counter() - t0) / reps
    # the largest eigenvalue from Hessian-vector products alone (power iteration), against the full spectrum
    q = torch.tensor(rng(44).normal(size=P))
    q = q / q.norm()
    lam_est = []
    for _ in range(300):
        w = hvp(q)
        lam_est.append(float(q @ w))
        q = w / w.norm()
    ev_last = snaps[-1]["eig"]
    top = float(np.abs(ev_last).max())
    assert hv_full_diff < 1e-10
    out = dict(P=int(P), sizes=sizes, steps=steps, keep=keep, curve=np.array(curve), X=X, y=y, grid_xs=xs,
               hv_full_diff=hv_full_diff, hs=hs, fd_err=fd_err, fd_best_h=float(hs[int(np.argmin(fd_err))]),
               fd_best=float(fd_err.min()), t_grad=t_grad, t_hvp=t_hvp, lam_est=np.array(lam_est),
               lam_top=float(ev_last.max()), lam_power=float(lam_est[-1]))
    for k, s in enumerate(snaps):
        for key in ("loss", "acc"):
            out[f"{key}{k}"] = s[key]
        out[f"eig{k}"] = s["eig"]
        out[f"region{k}"] = s["region"]
        e_ = s["eig"]
        out[f"top{k}"] = float(e_.max())
        out[f"nout{k}"] = int((e_ > 0.1 * e_.max()).sum())
        out[f"flat{k}"] = float((np.abs(e_) < 0.01 * e_.max()).mean())
        out[f"nneg{k}"] = int((e_ < -0.01 * e_.max()).sum())
    # summary of the trained spectrum
    lam = ev_last
    out["n_outliers"] = int((lam > 0.1 * lam.max()).sum())
    out["frac_flat"] = float((np.abs(lam) < 1e-3 * lam.max()).mean())
    out["n_neg"] = int((lam < -1e-4 * lam.max()).sum())
    out["lam_min"] = float(lam.min())
    out["n_outliers0"] = int((snaps[0]["eig"] > 0.1 * snaps[0]["eig"].max()).sum())
    return out


# ---------------------------------------------------------------------------
# Chapter 15: gradient descent on quadratics; saddles
# ---------------------------------------------------------------------------
def compute_quad():
    kappas = [1, 2, 4, 10, 25, 100, 400, 1000]
    rate_opt, rate_opt_pred, rate_L, rate_L_pred, steps_opt, steps_L = [], [], [], [], [], []
    for k in kappas:
        lam = np.array([1.0, float(k)])
        for eta, rr, pr, st in ((2 / (1 + k), rate_opt, rate_opt_pred, steps_opt), (1 / k, rate_L, rate_L_pred, steps_L)):
            x = np.array([1.0, 1.0])
            errs = [np.linalg.norm(x)]
            for _ in range(20000):
                x = x - eta * lam * x
                errs.append(np.linalg.norm(x))
                if errs[-1] < 1e-6 * errs[0] or errs[-1] == 0:
                    break
            errs = np.array(errs)
            st.append(len(errs) - 1)
            tail = errs[errs > 1e-300]
            rr.append(float((tail[-1] / tail[len(tail) // 2]) ** (1 / max(1, len(tail) - 1 - len(tail) // 2)))
                      if len(tail) > 4 else 0.0)
            pr.append(float(max(abs(1 - eta * lam[0]), abs(1 - eta * lam[1]))))
    # the stability edge on the valley of curvatures 1 and 25
    lam = np.array([1.0, 25.0])
    etas = np.linspace(0.004, 0.1, 49)
    final = []
    for eta in etas:
        x = np.array([-4.5, 0.9])
        for _ in range(100):
            x = x - eta * lam * x
        final.append(float(np.linalg.norm(x)))
    # a saddle: f = x^2/2 - y^2/2 + y^4/4, minima at y = +-1
    eta = 0.1

    def sgrad(p):
        return np.array([p[0], -p[1] + p[1] ** 3])

    def sf(p):
        return 0.5 * p[0] ** 2 - 0.5 * p[1] ** 2 + 0.25 * p[1] ** 4

    y0s = [10.0 ** -e for e in range(1, 13)]
    esc, pred = [], []
    paths = {}
    for y0 in y0s:
        p = np.array([1.5, y0])
        path = [p.copy()]
        for t in range(1, 5000):
            p = p - eta * sgrad(p)
            path.append(p.copy())
            if abs(p[1]) > 0.5:
                break
        esc.append(t)
        pred.append(math.log(0.5 / y0) / math.log(1 + eta))
        if y0 in (1e-2, 1e-6, 1e-10):
            paths[f"{y0:.0e}"] = np.array(path)
    p = np.array([1.5, 0.0])
    on = [p.copy()]
    for t in range(300):
        p = p - eta * sgrad(p)
        on.append(p.copy())
    stuck_grad = float(np.linalg.norm(sgrad(p)))
    # the loss along an escape from y0 = 1e-8: the plateau
    p = np.array([1.5, 1e-8])
    loss_plateau = []
    for t in range(400):
        loss_plateau.append(sf(p))
        p = p - eta * sgrad(p)
    return dict(kappas=kappas, rate_opt=rate_opt, rate_opt_pred=rate_opt_pred, rate_L=rate_L, rate_L_pred=rate_L_pred,
                steps_opt=steps_opt, steps_L=steps_L, etas=etas, final=np.array(final), y0s=y0s, esc=esc, esc_pred=pred,
                stuck=np.array(on), stuck_grad=stuck_grad, stuck_point=on[-1], loss_plateau=np.array(loss_plateau),
                **{f"path_{k}": v for k, v in paths.items()})


# ---------------------------------------------------------------------------
# Chapter 16: Lagrange multipliers
# ---------------------------------------------------------------------------
LAG_A, LAG_C = np.array([0.6, 1.4]), np.array([1.6, 0.9])  # f(x, y) = 0.6 (x - 1.6)^2 + 1.4 (y - 0.9)^2


def lag_f(x, y):
    return LAG_A[0] * (x - LAG_C[0]) ** 2 + LAG_A[1] * (y - LAG_C[1]) ** 2


def compute_lagrange():
    from scipy.optimize import brentq, minimize, minimize_scalar

    th = np.linspace(-np.pi, np.pi, 1441)
    fv = lag_f(np.cos(th), np.sin(th))
    r = minimize_scalar(lambda t: lag_f(math.cos(t), math.sin(t)), bracket=(th[np.argmin(fv)] - 0.01, th[np.argmin(fv)] + 0.01))
    t_star = float(r.x)
    xs = np.array([math.cos(t_star), math.sin(t_star)])
    gf = 2 * LAG_A * (xs - LAG_C)
    gg = 2 * xs
    lam = float(-(gf @ gg) / (gg @ gg))
    resid = float(np.linalg.norm(gf + lam * gg))
    # the part of grad f along the circle (zero only where the two gradients are parallel)
    tang = np.array([(2 * LAG_A * (np.array([math.cos(t), math.sin(t)]) - LAG_C)) @ np.array([-math.sin(t), math.cos(t)])
                     for t in th])
    # maximum entropy for a die whose average is 4.5
    faces = np.arange(1, 7)

    def boltz(b):
        w = np.exp(b * faces)
        return w / w.sum()

    beta = brentq(lambda b: boltz(b) @ faces - 4.5, -5, 5)
    p_star = boltz(beta)
    cons = [dict(type="eq", fun=lambda p: p.sum() - 1), dict(type="eq", fun=lambda p: p @ faces - 4.5)]
    res = minimize(lambda p: float(np.sum(p * np.log(np.maximum(p, 1e-300)))), np.full(6, 1 / 6), constraints=cons,
                   bounds=[(1e-12, 1)] * 6, method="SLSQP", options=dict(ftol=1e-14, maxiter=500))
    dice_diff = float(np.abs(res.x - p_star).max())
    H = float(-(p_star * np.log2(p_star)).sum())
    # reinforcement learning's closed form: maximize E[r] - beta KL(pi || pi_ref)
    g = rng(51)
    pref = g.dirichlet(np.ones(6) * 2)
    rew = g.normal(size=6)
    kb = 0.5
    pi_star = pref * np.exp(rew / kb)
    pi_star /= pi_star.sum()
    res2 = minimize(lambda p: -float(p @ rew - kb * np.sum(p * np.log(np.maximum(p, 1e-300) / pref))), np.full(6, 1 / 6),
                    constraints=[dict(type="eq", fun=lambda p: p.sum() - 1)], bounds=[(1e-12, 1)] * 6, method="SLSQP",
                    options=dict(ftol=1e-14, maxiter=500))
    rl_diff = float(np.abs(res2.x - pi_star).max())
    assert resid < 1e-6 and dice_diff < 1e-4 and rl_diff < 1e-4
    return dict(th=th, fv=fv, tang=tang, t_star=t_star, x_star=xs, grad_f=gf, grad_g=gg, lam=lam, resid=resid,
                f_star=float(lag_f(*xs)), A=LAG_A, C=LAG_C, beta=float(beta), p_dice=p_star, dice_diff=dice_diff, H_dice=H,
                pref=pref, rew=rew, kl_beta=kb, pi_star=pi_star, rl_diff=rl_diff)


# ---------------------------------------------------------------------------
# Chapter 17: KKT and duality
# ---------------------------------------------------------------------------
def compute_kkt():
    from scipy.optimize import minimize

    g = rng(61)
    n = 10
    A = g.normal(size=(n, 2)) * 0.55 + np.array([1.1, 0.9])
    Bm = g.normal(size=(n, 2)) * 0.55 - np.array([1.1, 0.7])
    X = np.r_[A, Bm]
    y = np.r_[np.ones(n), -np.ones(n)]
    # the primal: smallest w with every point at least 1 / |w| from the line
    cons = [dict(type="ineq", fun=lambda v, i=i: y[i] * (X[i] @ v[:2] + v[2]) - 1) for i in range(2 * n)]
    pr = minimize(lambda v: 0.5 * v[:2] @ v[:2], np.array([1.0, 1.0, 0.0]), constraints=cons, method="SLSQP",
                  options=dict(ftol=1e-15, maxiter=1000))
    w, b = pr.x[:2], pr.x[2]
    p_star = float(0.5 * w @ w)
    # the dual: one multiplier per point
    K = (X @ X.T) * np.outer(y, y)
    du = minimize(lambda a: -(a.sum() - 0.5 * a @ K @ a), np.full(2 * n, 0.1), jac=lambda a: -(1 - K @ a),
                  constraints=[dict(type="eq", fun=lambda a: a @ y)], bounds=[(0, None)] * (2 * n), method="SLSQP",
                  options=dict(ftol=1e-15, maxiter=1000))
    alpha = du.x
    d_star = float(alpha.sum() - 0.5 * alpha @ K @ alpha)
    w_dual = (alpha * y) @ X
    sv = np.where(alpha > 1e-6 * alpha.max())[0]
    margins = y * (X @ w + b)
    slack = float(np.abs(alpha * (margins - 1)).max())
    # a convex toy for the picture: minimize x^2 subject to x >= 1; its dual function
    lams = np.linspace(0, 4, 81)
    toy_dual = lams - lams ** 2 / 4
    # a non-convex one: x^4 - 3x^2 + x subject to x >= 0.5
    xs = np.linspace(-2.2, 2.2, 440_001)
    F = xs ** 4 - 3 * xs ** 2 + xs
    G = 0.5 - xs
    nc_p = float(F[G <= 0].min())
    nc_x = float(xs[G <= 0][np.argmin(F[G <= 0])])
    nl = np.linspace(0, 6, 601)
    nc_dual = np.array([float((F + l * G).min()) for l in nl])
    nc_d = float(nc_dual.max())
    assert abs(p_star - d_star) < 1e-6 and np.abs(w - w_dual).max() < 1e-4 and nc_p - nc_d > 0.1
    return dict(X=X, y=y, w=w, b=float(b), p_star=p_star, d_star=d_star, gap=float(p_star - d_star), alpha=alpha,
                sv=sv.tolist(), margins=margins, slack=slack, w_dual=w_dual, width=float(2 / np.linalg.norm(w)),
                lams=lams, toy_dual=toy_dual, nc_p=nc_p, nc_x=nc_x, nc_d=nc_d, nc_lam=float(nl[np.argmax(nc_dual)]),
                nc_l=nl, nc_dual=nc_dual, nc_gap=float(nc_p - nc_d))


# ---------------------------------------------------------------------------
# Chapter 18: implicit differentiation of a fixed point
# ---------------------------------------------------------------------------
def _deq_solve(W, u, tol=1e-12, max_iter=2000):
    z = np.zeros(len(u))
    for k in range(max_iter):
        z2 = np.tanh(W @ z + u)
        if np.abs(z2 - z).max() < tol:
            return z2, k + 1
        z = z2
    return z, max_iter


def _spectral_clip(W, c=0.9):
    s = np.linalg.norm(W, 2)
    return W * (c / s) if s > c else W


def _unrolled_grad(W, u, v, K):
    """dL/dW for L = v . z_K, z_{k+1} = tanh(W z_k + u), z_0 = 0, by the library through all K steps.  The state is
    a row (1 x d) times W^T: the library's matrix product differentiates both factors for 2-D arrays."""
    WT = Tensor(W.T.copy(), requires_grad=True)
    zt = Tensor(np.zeros((1, len(u))))
    for _ in range(K):
        zt = (zt @ WT + Tensor(u[None])).tanh()
    (zt * Tensor(v[None])).sum().backward()
    return WT.grad.T


def compute_deq():
    g = rng(71)
    d = 8
    W = _spectral_clip(g.normal(size=(d, d)) / math.sqrt(d), 0.8)
    U, b, v = g.normal(size=d), g.normal(size=d) * 0.3, g.normal(size=d)
    x = 0.7
    u = U * x + b
    z, iters = _deq_solve(W, u)
    # implicit: dL/dW for L = v . z*, from (I - J)^T a = v, J = diag(1 - z^2) W
    D = 1 - z * z
    J = D[:, None] * W
    a = np.linalg.solve((np.eye(d) - J).T, v)
    gW_imp = np.outer(a * D, z)
    rho = float(np.abs(np.linalg.eigvals(J)).max())
    # unrolled: K steps from z = 0, differentiated by the library
    Ks = list(range(1, 61))
    errs = []
    for K in Ks:
        errs.append(float(np.abs(_unrolled_grad(W, u, v, K) - gW_imp).max() / np.abs(gW_imp).max()))
    errs = np.array(errs)
    ok = errs > 1e-14
    slope = float(np.polyfit(np.array(Ks)[ok][5:40], np.log(errs[ok][5:40]), 1)[0]) if ok.sum() > 40 else float("nan")
    # train a tiny DEQ to fit a curve, with implicit gradients only; W kept a contraction (spectral norm <= 0.9)
    xs = np.linspace(-2, 2, 48)
    ys = np.sin(1.6 * xs) * 0.8 + 0.25 * xs
    d = 12
    g = rng(72)
    p = dict(W=g.normal(size=(d, d)) * 0.2 / math.sqrt(d), U=g.normal(size=d), b=g.normal(size=d) * 0.5,
             v=g.normal(size=d) * 0.3, c=np.zeros(1))
    m = {k: np.zeros_like(val) for k, val in p.items()}
    s2 = {k: np.zeros_like(val) for k, val in p.items()}
    lr, steps = 0.03, 800
    keep = [0, 25, 75, 200, 400, 800]
    fits, curve, iters_curve = {}, [], []
    gx = np.linspace(-2.2, 2.2, 90)
    for t in range(steps + 1):
        grads = {k: np.zeros_like(val) for k, val in p.items()}
        L, its = 0.0, 0
        for xi, yi in zip(xs, ys):
            uu = p["U"] * xi + p["b"]
            zs, k_ = _deq_solve(p["W"], uu, tol=1e-10)
            its += k_
            out = p["v"] @ zs + p["c"][0]
            e = out - yi
            L += e * e / len(xs)
            gout = 2 * e / len(xs)
            Dz = 1 - zs * zs
            aa = np.linalg.solve((np.eye(d) - Dz[:, None] * p["W"]).T, gout * p["v"])  # dL/dz*, through the fixed point
            gz = aa * Dz
            grads["W"] += np.outer(gz, zs)
            grads["U"] += gz * xi
            grads["b"] += gz
            grads["v"] += gout * zs
            grads["c"] += gout
        if t % 5 == 0:
            curve.append((t, L))
            iters_curve.append((t, its / len(xs)))
        if t in keep:
            fits[t] = np.array([p["v"] @ _deq_solve(p["W"], p["U"] * xx + p["b"], tol=1e-10)[0] + p["c"][0] for xx in gx])
        if t == steps:
            break
        for k in p:  # Adam (Part 11)
            m[k] = 0.9 * m[k] + 0.1 * grads[k]
            s2[k] = 0.999 * s2[k] + 0.001 * grads[k] ** 2
            p[k] = p[k] - lr * (m[k] / (1 - 0.9 ** (t + 1))) / (np.sqrt(s2[k] / (1 - 0.999 ** (t + 1))) + 1e-8)
        p["W"] = _spectral_clip(p["W"], 0.9)
    # at the end, the implicit gradient against 60 unrolled steps for one input
    uu = p["U"] * 0.5 + p["b"]
    zs, _ = _deq_solve(p["W"], uu)
    Dz = 1 - zs * zs
    aa = np.linalg.solve((np.eye(d) - Dz[:, None] * p["W"]).T, p["v"])
    g_imp = np.outer(aa * Dz, zs)
    end_diff = float(np.abs(_unrolled_grad(p["W"], uu, p["v"], 200) - g_imp).max() / np.abs(g_imp).max())
    return dict(iters=iters, rho=rho, Ks=np.array(Ks), errs=errs, slope=slope, rate=float(math.exp(slope)),
                xs=xs, ys=ys, gx=gx, keep=keep, fits=np.stack([fits[k] for k in keep]), curve=np.array(curve),
                iters_curve=np.array(iters_curve), lr=lr, steps=steps, end_diff=end_diff, d=d,
                final_loss=float(curve[-1][1]), first_loss=float(curve[0][1]))


# ---------------------------------------------------------------------------
# Chapter 8: how large a step plain gradient descent can take on the letter model
# ---------------------------------------------------------------------------
def compute_gdlr():
    """Full-batch gradient descent on Part 1's 729 scores (the gradient from the pair counts, exactly), at five step
    sizes, with the Hessian's largest eigenvalue tracked: it starts at max_i w_i / 27 and grows as the model learns."""
    from videos.ai.ai1 import compute as c1

    tr = c1.codes27(c1.text("train27"))
    N = np.zeros((27, 27))
    np.add.at(N, (tr[:-1], tr[1:]), 1)
    n = N.sum(1)
    Ntot = N.sum()
    w = n / Ntot
    ph = N / np.maximum(n, 1)[:, None]
    H_cond = float(-(N * np.log2(np.maximum(ph, 1e-300))).sum() / Ntot)

    def top(q):
        return float(max(w[i] * np.linalg.eigvalsh(np.diag(q[i]) - np.outer(q[i], q[i]))[-1] for i in range(27)))

    lam0 = float(w.max() / 27)
    lam_star = top(ph)
    fracs = [0.01, 0.1, 0.2, 0.3, 0.5]
    steps = 3000
    out = dict(lam0=lam0, eta0=2 / lam0, lam_star=lam_star, eta_star=2 / lam_star, H_cond=H_cond, steps=steps)
    etas, last_mean, last_spread, monotone = [], [], [], []
    for k, f in enumerate(fracs):
        eta = f * 2 / lam0
        z = np.zeros((27, 27))
        bits, lam = [], []
        for t in range(steps + 1):
            q = np.exp(z - z.max(1, keepdims=True))
            q /= q.sum(1, keepdims=True)
            bits.append(float(-(N * np.log(np.maximum(q, 1e-300))).sum() / Ntot / math.log(2)))
            if t % 25 == 0:
                lam.append(top(q))
            z -= eta * w[:, None] * (q - ph)
        bits = np.array(bits)
        out[f"bitcurve{k}"] = bits[::10]
        out[f"lamcurve{k}"] = np.array(lam)
        etas.append(eta)
        last_mean.append(float(bits[-500:].mean()))
        last_spread.append(float(bits[-500:].max() - bits[-500:].min()))
        monotone.append(bool((np.diff(bits[-500:]) <= 1e-12).all()))
    out.update(etas=etas, last_mean=last_mean, last_spread=last_spread, monotone=monotone)
    return out


ITEMS = {
    "params": compute_params,
    "linapprox": compute_linapprox,
    "jacobians": compute_jacobians,
    "modes": compute_modes,
    "tiny": compute_tiny,
    "mlp2": compute_mlp2,
    "tape": compute_tape,
    "check": compute_check,
    "train": compute_train,
    "grad0": compute_grad0,
    "gdlr": compute_gdlr,
    "floats": compute_floats,
    "cancel": compute_cancel,
    "vcurve": compute_vcurve,
    "checkpoint": compute_checkpoint,
    "newton": compute_newton,
    "hessian": compute_hessian,
    "valley": compute_valley,
    "quad": compute_quad,
    "lagrange": compute_lagrange,
    "kkt": compute_kkt,
    "deq": compute_deq,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
