"""Wireless (Part 36): fading, OFDM over a multipath channel, and MIMO capacity.

    rayleigh_ber(snr_db, n, rng)       BPSK through flat Rayleigh fading against the same SNR without fading
    ofdm(n_sub, cp, taps, snr_db, rng) one OFDM symbol: QPSK on n_sub subcarriers, an inverse FFT (Part 19), a
        cyclic prefix of cp samples, a multipath channel (taps), noise; then the FFT and a one-tap equaliser per
        subcarrier.  Returns the bit error rate with and without the prefix
    mimo_capacity(nt, nr, snr_db, trials, rng)  E log2 det(I + (snr/nt) H H*) for i.i.d. Rayleigh H
"""
from __future__ import annotations

import math

import numpy as np


def rayleigh_ber(snr_db: float, n: int, rng: np.random.Generator) -> dict:
    snr = 10 ** (snr_db / 10)
    bits = rng.integers(0, 2, n)
    x = 2.0 * bits - 1
    noise = rng.normal(0, math.sqrt(1 / (2 * snr)), n)
    awgn = np.mean(((x + noise) > 0) != bits)
    h = np.abs(rng.normal(0, math.sqrt(0.5), n) + 1j * rng.normal(0, math.sqrt(0.5), n))
    faded = np.mean(((h * x + noise) > 0) != bits)
    theory_awgn = 0.5 * math.erfc(math.sqrt(snr))
    theory_ray = 0.5 * (1 - math.sqrt(snr / (1 + snr)))
    return {"snr_db": snr_db, "awgn": float(awgn), "rayleigh": float(faded), "theory_awgn": theory_awgn,
            "theory_rayleigh": theory_ray}


def ofdm(n_sub: int, cp: int, taps: list[complex], snr_db: float, rng: np.random.Generator,
         symbols: int = 200) -> dict:
    taps = np.array(taps, dtype=complex)
    H = np.fft.fft(taps, n_sub)
    errs_cp = errs_nocp = total = 0
    for _ in range(symbols):
        bits = rng.integers(0, 2, 2 * n_sub)
        X = ((2 * bits[0::2] - 1) + 1j * (2 * bits[1::2] - 1)) / math.sqrt(2)
        x = np.fft.ifft(X) * math.sqrt(n_sub)
        prev = np.fft.ifft(((2 * rng.integers(0, 2, n_sub) - 1) + 1j * (2 * rng.integers(0, 2, n_sub) - 1))
                           / math.sqrt(2)) * math.sqrt(n_sub)
        sigma = math.sqrt(10 ** (-snr_db / 10) / 2)
        for use_cp in (True, False):
            g = cp if use_cp else 0
            tx = np.concatenate([prev, x[-g:], x]) if g else np.concatenate([prev, x])
            rx = np.convolve(tx, taps)[: len(tx)]
            rx = rx + sigma * (rng.normal(size=len(rx)) + 1j * rng.normal(size=len(rx)))
            y = rx[len(prev) + g: len(prev) + g + n_sub]
            Y = np.fft.fft(y) / math.sqrt(n_sub)
            Xh = Y / H
            dec = np.empty(2 * n_sub, dtype=int)
            dec[0::2] = Xh.real > 0
            dec[1::2] = Xh.imag > 0
            e = int(np.sum(dec != bits))
            if use_cp:
                errs_cp += e
            else:
                errs_nocp += e
        total += 2 * n_sub
    return {"n_sub": n_sub, "cp": cp, "taps": len(taps), "ber_cp": errs_cp / total, "ber_nocp": errs_nocp / total,
            "H": [abs(v) for v in H]}


def mimo_capacity(nt: int, nr: int, snr_db: float, trials: int, rng: np.random.Generator) -> float:
    snr = 10 ** (snr_db / 10)
    tot = 0.0
    for _ in range(trials):
        H = (rng.normal(size=(nr, nt)) + 1j * rng.normal(size=(nr, nt))) / math.sqrt(2)
        M = np.eye(nr) + (snr / nt) * H @ H.conj().T
        tot += math.log2(np.linalg.det(M).real)
    return tot / trials
