"""The two 4-bit floating-point formats of current accelerators, bit by bit (Part 19's ``formats`` item).

    MXFP4  (OCP Microscaling spec, 2023; gpt-oss's expert weights): blocks of 32 numbers, each an FP4 E2M1 code
           (sign, 2 exponent bits, 1 mantissa bit), sharing one scale that is a power of two, stored as an 8-bit
           exponent E8M0: shared exponent = floor(log2(max |v|)) - 2, so the block's largest number lands in E2M1's
           top binade [4, 8); values above 6 there are clamped to 6.  4 + 8/32 = 4.25 bits a number.
    NVFP4  (NVIDIA Blackwell, 2025): blocks of 16 E2M1 codes sharing a scale stored as an FP8 E4M3 number (not just a
           power of two), and one FP32 scale per tensor that keeps the block scales inside E4M3's range.  4 + 8/16 =
           4.5 bits a number.

Every code is produced as bits and decoded back, so the emulation is exact, not an approximation of the format.
"""

from __future__ import annotations

import math

import numpy as np

E2M1 = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 6])  # magnitudes of the codes 000 ... 111 (sign separate)


def e2m1_code(v):
    """Round to the nearest E2M1 value (ties to the even code), clamp at 6: the 4-bit codes (sign << 3 | magnitude)."""
    v = np.asarray(v, np.float64)
    a = np.minimum(np.abs(v), 6.0)
    d = np.abs(a[..., None] - E2M1) + 1e-12 * (np.arange(8) % 2)  # a tie goes to the even code
    idx = d.argmin(-1)
    return ((np.signbit(v) & (idx > 0)).astype(int) << 3) | idx


def e2m1_value(code):
    code = np.asarray(code)
    return np.where(code & 8, -1.0, 1.0) * E2M1[code & 7]


def bits(code, n):
    return format(int(code), f"0{n}b")


def round_e4m3(x):
    """Positive x to FP8 E4M3 (bias 7, 3 mantissa bits, largest 448, subnormals below 2^-6), round to nearest."""
    x = np.minimum(np.asarray(x, np.float64), 448.0)
    e = np.floor(np.log2(np.maximum(x, 2.0 ** -9)))
    e = np.maximum(e, -6)
    step = 2.0 ** (e - 3)
    return np.minimum(np.round(x / step) * step, 448.0)


def e4m3_bits(x) -> str:
    """The 8 bits of a positive E4M3 number (already representable): 0 eeee mmm."""
    x = float(x)
    if x == 0:
        return "00000000"
    e = math.floor(math.log2(x))
    if e < -6:  # subnormal
        return "0" + "0000" + bits(round(x / 2.0 ** -9), 3)
    m = round((x / 2.0 ** e - 1) * 8)
    if m == 8:
        e, m = e + 1, 0
    return "0" + bits(e + 7, 4) + bits(m, 3)


def _blocks(W, g):
    """Rows of W cut into blocks of g (the last padded with zeros, which change no block's maximum)."""
    r, c = W.shape
    pad = (-c) % g
    Wp = np.concatenate([W, np.zeros((r, pad))], 1) if pad else W
    return Wp.reshape(-1, g), c, pad


def _unblocks(flat, r, c, pad):
    return flat.reshape(r, c + pad)[:, :c]


def mxfp4(W, detail=False):
    """Round every row of W in MXFP4 (blocks of 32 along the row); ``detail``: also the shared exponents and codes."""
    W = np.asarray(W, np.float64)
    flat, c, pad = _blocks(W, 32)
    amax = np.abs(flat).max(1, keepdims=True)
    sh = np.floor(np.log2(np.maximum(amax, 2.0 ** -126))) - 2  # E8M0: the shared exponent
    X = 2.0 ** sh
    codes = e2m1_code(flat / X)
    out = _unblocks(e2m1_value(codes) * X, W.shape[0], c, pad)
    if detail:
        return out, dict(shared_exp=sh[:, 0], codes=codes, clipped=(amax[:, 0] / X[:, 0]) > 6.0)
    return out


def nvfp4(W, detail=False):
    """Round W in NVFP4: blocks of 16 along rows, an E4M3 scale each, and one FP32 scale for the tensor."""
    W = np.asarray(W, np.float64)
    flat, c, pad = _blocks(W, 16)
    g = np.abs(W).max() / (6.0 * 448.0)  # the tensor scale: the largest block scale becomes 448
    amax = np.abs(flat).max(1, keepdims=True)
    s = round_e4m3(amax / 6.0 / g)
    s = np.where(s > 0, s, 1.0)
    codes = e2m1_code(flat / (s * g))
    out = _unblocks(e2m1_value(codes) * s * g, W.shape[0], c, pad)
    if detail:
        return out, dict(tensor_scale=g, block_scale=s[:, 0], codes=codes)
    return out


def int4_scaled(W, group, scale="fp16"):
    """4-bit integers (-8 ... 7) with one scale per ``group`` numbers along a row; the scale stored in FP16 (rounded
    to 11 significant bits) or in E4M3 with a tensor scale, as NVFP4 does (to compare the element formats alone)."""
    W = np.asarray(W, np.float64)
    flat, c, pad = _blocks(W, group)
    amax = np.abs(flat).max(1, keepdims=True)
    if scale == "e4m3":
        g = np.abs(W).max() / (7.0 * 448.0)
        s = round_e4m3(amax / 7.0 / g) * g
    else:
        s = amax / 7.0
        e = np.floor(np.log2(np.maximum(s, 1e-30)))
        s = np.round(s / 2.0 ** (e - 10)) * 2.0 ** (e - 10)
    s = np.where(s > 0, s, 1.0)
    return _unblocks(np.clip(np.round(flat / s), -8, 7) * s, W.shape[0], c, pad)


def block_picture(W_row32):
    """One block of 32 of our weights, encoded both ways, every bit kept for the picture."""
    v = np.asarray(W_row32, np.float64)
    mx, dm = mxfp4(v[None], detail=True)
    amax = np.abs(v).max()
    sh = int(dm["shared_exp"][0])
    out = dict(values=v, mx_shared_exp=sh, mx_scale_bits=bits(sh + 127, 8), mx_codes=[bits(c, 4) for c in dm["codes"][0]],
               mx_decoded=mx[0], mx_clipped=bool(dm["clipped"][0]), amax=amax)
    # NVFP4 on the first 16 (with this row's tensor scale taken from the whole layer by the caller)
    return out
