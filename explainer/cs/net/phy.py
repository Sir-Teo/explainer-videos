"""The physical layer (Part 36): Nyquist and Shannon, square QAM through additive white Gaussian noise, and the
speed of light in fibre.

    shannon(B, snr)                  bits per second a channel of bandwidth B (Hz) can carry at that SNR (linear)
    qam(M)                           the M points of square M-QAM, Gray-coded, unit average energy, with their bits
    qam_simulate(M, snr_db, n, rng)  symbol and bit error rates, measured, at Es/N0 = snr_db
    qam_ser(M, snr_db)               the textbook symbol error rate of square M-QAM, for comparison
    snr_needed(M, ber)               the Es/N0 at which M-QAM reaches a bit error rate, by bisection on the formula
    shannon_snr(bits_per_symbol)     the least SNR at which Shannon allows that many bits per symbol: 2^k - 1
"""
from __future__ import annotations

import math

import numpy as np

C_FIBRE = 2.04e8        # metres a second in silica fibre (refractive index about 1.47)
C_VACUUM = 2.998e8


def shannon(B: float, snr: float) -> float:
    return B * math.log2(1 + snr)


def db(x: float) -> float:
    return 10 * math.log10(x)


def undb(d: float) -> float:
    return 10 ** (d / 10)


def _gray(n: int) -> int:
    return n ^ (n >> 1)


def qam(M: int):
    """Square M-QAM: (points as complex numbers, bit labels as ints), Gray-coded on each axis, mean energy 1."""
    k = int(round(math.sqrt(M)))
    assert k * k == M and k & (k - 1) == 0, "square QAM with a power-of-two side"
    b = int(math.log2(k))
    levels = np.arange(-(k - 1), k, 2, dtype=float)               # -3, -1, 1, 3 for 16-QAM
    pts, labels = [], []
    for i in range(k):
        for q in range(k):
            pts.append(complex(levels[i], levels[q]))
            labels.append((_gray(i) << b) | _gray(q))
    pts = np.array(pts)
    pts /= math.sqrt(np.mean(np.abs(pts) ** 2))
    return pts, np.array(labels)


def qam_simulate(M: int, snr_db: float, n: int, rng: np.random.Generator) -> dict:
    """Send n random symbols at Es/N0 = snr_db; decide each by the nearest point. Returns the symbol and bit error
    rates and a few received points for drawing."""
    pts, labels = qam(M)
    bits = int(math.log2(M))
    tx = rng.integers(0, M, size=n)
    n0 = 1 / undb(snr_db)
    noise = rng.normal(0, math.sqrt(n0 / 2), size=n) + 1j * rng.normal(0, math.sqrt(n0 / 2), size=n)
    rx = pts[tx] + noise
    # nearest point on a square grid: decide each axis separately
    k = int(round(math.sqrt(M)))
    lv = np.sort(np.unique(pts.real))
    ii = np.clip(np.round((rx.real - lv[0]) / (lv[1] - lv[0])), 0, k - 1).astype(int)
    qq = np.clip(np.round((rx.imag - lv[0]) / (lv[1] - lv[0])), 0, k - 1).astype(int)
    dec = ii * k + qq
    ser = float(np.mean(dec != tx))
    diff = labels[dec] ^ labels[tx]
    bit_errors = sum(bin(int(x)).count("1") for x in diff[diff != 0])
    return {"M": M, "snr_db": snr_db, "n": n, "ser": ser, "ber": bit_errors / (n * bits),
            "sample": [(float(z.real), float(z.imag)) for z in rx[:400]],
            "sample_tx": [int(t) for t in tx[:400]]}


def Q(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2))


def qam_ser(M: int, snr_db: float) -> float:
    k = math.sqrt(M)
    p = 2 * (1 - 1 / k) * Q(math.sqrt(3 * undb(snr_db) / (M - 1)))
    return 1 - (1 - p) ** 2


def qam_ber(M: int, snr_db: float) -> float:
    """Gray coding: almost every symbol error flips one bit."""
    return qam_ser(M, snr_db) / math.log2(M)


def snr_needed(M: int, ber: float = 1e-6) -> float:
    lo, hi = -10.0, 60.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if qam_ber(M, mid) > ber:
            lo = mid
        else:
            hi = mid
    return hi


def shannon_snr(bits_per_symbol: float) -> float:
    """Least Es/N0 (linear) at which a complex channel carries this many bits a symbol: 2^k - 1."""
    return 2 ** bits_per_symbol - 1


def fibre_rtt(km: float) -> float:
    return 2 * km * 1000 / C_FIBRE


def bdp(rate_bps: float, rtt_s: float) -> float:
    """Bytes in flight needed to fill the pipe."""
    return rate_bps * rtt_s / 8
