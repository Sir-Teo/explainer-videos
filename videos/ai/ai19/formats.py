"""Four-bit weights done properly, on Part 13's transformer (the ``formats`` item of Part 19).

    formats   the two 4-bit floating-point formats of current chips, exactly: MXFP4 (E2M1 numbers, one power-of-two
              scale per block of 32) and NVFP4 (E2M1, one FP8 E4M3 scale per block of 16, and one scale per tensor);
              against plain 4-bit integers per row. Then two tricks that make low precision work: GPTQ (round one
              input column at a time, and push each rounding error onto the columns not yet rounded, weighted by the
              inverse of the inputs' second moment) and a Hadamard rotation (spread the outliers before rounding).
              Bits per character on the passage for each, at 4 and 3 bits.
"""

from __future__ import annotations

import math

import numpy as np

E2M1 = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6])


def round_e2m1(v):
    """Round to the nearest E2M1 number (sign kept), values beyond 6 clipped."""
    mag = E2M1[np.abs(np.minimum(np.abs(v), 6.0)[..., None] - E2M1).argmin(-1)]
    return np.sign(v) * mag


def round_e4m3(x):
    """Round positive numbers to FP8 E4M3 (bias 7, 3 mantissa bits, largest 448, subnormals below 2^-6)."""
    x = np.minimum(np.asarray(x, float), 448.0)
    e = np.floor(np.log2(np.maximum(x, 2.0 ** -9)))
    e = np.maximum(e, -6)  # subnormal range shares the smallest exponent
    step = 2.0 ** (e - 3)
    return np.round(x / step) * step


def mxfp4(W):
    flat = W.reshape(-1, 32)
    amax = np.abs(flat).max(1, keepdims=True)
    X = 2.0 ** (np.floor(np.log2(np.maximum(amax, 1e-30))) - 2)  # E8M0: the shared exponent, 6 = 1.5 x 2^2
    return (round_e2m1(flat / X) * X).reshape(W.shape)


def nvfp4(W):
    flat = W.reshape(-1, 16)
    g = np.abs(W).max() / (6.0 * 448.0)  # the per-tensor FP32 scale, so block scales fit E4M3
    amax = np.abs(flat).max(1, keepdims=True)
    s = round_e4m3(amax / 6.0 / g) * g
    s = np.where(s > 0, s, 1.0)
    return (round_e2m1(flat / s) * s).reshape(W.shape)


def rtn(W, bits):
    """Round to nearest, symmetric, one scale per row."""
    qmax = 2 ** (bits - 1) - 1
    s = np.abs(W).max(1, keepdims=True) / qmax
    s = np.where(s > 0, s, 1.0)
    return np.clip(np.round(W / s), -qmax - 1, qmax) * s


def gptq(W, H, bits, damp=0.01):
    """GPTQ (Frantar et al., 2022) for y = W x with input second moment H = E[x x^T]: quantize column by column, and
    after each one, move its rounding error onto the columns still to come, along the rows of the Cholesky factor of
    H^-1 (the optimal brain surgeon update)."""
    W = W.astype(np.float64).copy()
    n = W.shape[1]
    qmax = 2 ** (bits - 1) - 1
    s = np.abs(W).max(1) / qmax  # the same per-row scales as round-to-nearest
    s = np.where(s > 0, s, 1.0)
    H = H + damp * np.mean(np.diag(H)) * np.eye(n)
    U = np.linalg.cholesky(np.linalg.inv(H)).T  # upper: H^-1 = U^T U
    Q = np.zeros_like(W)
    for j in range(n):
        w = W[:, j]
        q = np.clip(np.round(w / s), -qmax - 1, qmax) * s
        Q[:, j] = q
        err = (w - q) / U[j, j]
        W[:, j + 1:] -= np.outer(err, U[j, j + 1:])
    return Q


def hadamard(n):
    Hm = np.array([[1.0]])
    while Hm.shape[0] < n:
        Hm = np.block([[Hm, Hm], [Hm, -Hm]])
    return Hm / math.sqrt(n)


def compute_formats():
    import torch

    from videos.ai.ai13 import compute as c11

    torch.set_num_threads(3)
    c11.load("tf")
    model, chars, enc, data = c11.load_tf()
    orig = {k: v.clone() for k, v in model.state_dict().items()}
    names = [k for k, v in orig.items() if v.dim() == 2 and "emb" not in k]
    # the inputs each linear layer sees, on 48 windows of the training text
    mods = dict(model.named_modules())
    acts = {}

    def hook(name):
        def f(_m, inp, _out):
            x = inp[0].detach().reshape(-1, inp[0].shape[-1]).double()
            acts[name] = acts.get(name, 0) + x.T @ x
            acts[name + "#n"] = acts.get(name + "#n", 0) + len(x)
        return f

    hs = [mods[k[:-len(".weight")]].register_forward_hook(hook(k)) for k in names]
    g = np.random.default_rng(7)
    starts = g.integers(0, len(data["train"]) - c11.CTX - 1, 48)
    with torch.no_grad():
        for i in range(0, 48, 16):
            model(torch.stack([data["train"][s:s + c11.CTX] for s in starts[i:i + 16]]))
    for h in hs:
        h.remove()
    Hs = {k: (acts[k] / acts[k + "#n"]).numpy() for k in names}

    def bits(fn):
        sd = {k: (torch.tensor(fn(k, v.numpy().astype(np.float64)), dtype=torch.float32) if k in names else v) for k, v in orig.items()}
        model.load_state_dict(sd)
        b = c11.tf_bits(model, data["passage"])
        model.load_state_dict(orig)
        return b

    def rotated(k, W, b):
        Hm = hadamard(W.shape[1])
        return rtn(W @ Hm.T, b) @ Hm  # round in the rotated basis, then rotate back

    out = dict(fp32=bits(lambda k, W: W))
    print(f"    fp32: {out['fp32']:.3f} bits/char", flush=True)
    jobs = {
        "int4": lambda k, W: rtn(W, 4), "mxfp4": lambda k, W: mxfp4(W), "nvfp4": lambda k, W: nvfp4(W),
        "gptq4": lambda k, W: gptq(W, Hs[k], 4), "had4": lambda k, W: rotated(k, W, 4),
        "int3": lambda k, W: rtn(W, 3), "gptq3": lambda k, W: gptq(W, Hs[k], 3), "had3": lambda k, W: rotated(k, W, 3),
    }
    for name, fn in jobs.items():
        out[name] = bits(fn)
        print(f"    {name}: {out[name]:.3f} bits/char", flush=True)
    # storage per weight, scales included (rows of 128 or 512 numbers for the integer formats)
    row = float(np.mean([orig[k].shape[1] for k in names]))
    out["bpw"] = dict(int4=4 + 32 / row, mxfp4=4 + 8 / 32, nvfp4=4 + 8 / 16, int3=3 + 32 / row)
    # how peaked one layer's rows are before and after the rotation: the largest weight over the typical one
    W = orig["blocks.1.f1.weight"].numpy().astype(np.float64)
    Wr = W @ hadamard(W.shape[1]).T
    crest = lambda M: float(np.mean(np.abs(M).max(1) / np.sqrt((M ** 2).mean(1))))  # noqa: E731
    out["crest"], out["crest_rot"] = crest(W), crest(Wr)
    out["row"], out["row_rot"] = W[0], Wr[0]
    # one real layer, at 3 bits: the output error on real inputs, rounded vs GPTQ (relative, via the second moment)
    k1 = "blocks.1.f1.weight"
    H1 = Hs[k1]

    def out_err(Q):
        E_ = W - Q
        return float(np.sqrt(np.trace(E_ @ H1 @ E_.T) / np.trace(W @ H1 @ W.T)))

    out["layer_err_rtn3"], out["layer_err_gptq3"] = out_err(rtn(W, 3)), out_err(gptq(W, H1, 3))
    out["layer_err_rtn4"], out["layer_err_gptq4"] = out_err(rtn(W, 4)), out_err(gptq(W, H1, 4))
    print(f"    one layer's output error at 3 bits: rounded {out['layer_err_rtn3']:.3f}, GPTQ {out['layer_err_gptq3']:.3f}", flush=True)
    # one block of 16 weights in NVFP4, step by step, for the picture
    blk = W[0, :16]
    gs = np.abs(W).max() / (6.0 * 448.0)
    s = round_e4m3(np.abs(blk).max() / 6.0 / gs) * gs
    out["block"], out["block_scale"], out["block_codes"] = blk, float(s), round_e2m1(blk / s)
    assert out["gptq3"] < out["int3"] and out["int3"] > out["int4"]
    return out
