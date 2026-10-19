"""Precompute everything numerical in Part 3 of the AI series ("Change").

    python -m videos.ai.ai3.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai3.compute --force train

Results are cached in ``.cache/ai3/<name>.json`` (+ ``.npz``).  The autodiff library the part builds is
``explainer/ai/autodiff.py``; this file checks it and trains with it.

Items:
    params    how many numbers GPT-2 small and Qwen3-4B have (read from their weight files' headers)
    tiny      the worked example: one input, one weight, one bias, a sigmoid and a squared error, forward and back
    check     the library's gradients against finite differences and against PyTorch, on a small network
    train     Part 1's letter-pair model, 729 scores trained by gradient descent with the library on the books
    valley    gradient descent, momentum and Newton's method on a long narrow valley
"""

from __future__ import annotations

import json
import math
import struct

import numpy as np

from explainer.ai.autodiff import Tensor, cross_entropy
from explainer.ai.cache import Cache

CACHE = Cache("ai3")
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


def compute_params():
    import torch
    from transformers import AutoModelForCausalLM

    gpt2 = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
    n_gpt2 = sum(p.numel() for p in gpt2.parameters())  # the tied input/output matrix counted once
    n_qwen = count_safetensors("Qwen/Qwen3-4B-Base")
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
    m, v = np.zeros((27, 27)), np.zeros((27, 27))  # Adam's running averages (Part 9)
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


ITEMS = {
    "params": compute_params,
    "tiny": compute_tiny,
    "check": compute_check,
    "train": compute_train,
    "valley": compute_valley,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
