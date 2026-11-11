"""RAID (Part 34): striping, mirroring and parity across disks, and the odds of losing data while rebuilding.

* :func:`layout`: where logical block b lives under RAID 0, 1, 4, 5 and 6 (data and parity disks, per stripe).
* :func:`xor_parity`, :func:`rebuild_one`: RAID 4/5's parity is the XOR of the stripe (Part 28's simplest code); any
  one lost disk is the XOR of the survivors.
* :func:`pq`, :func:`rebuild_two`: RAID 6 adds Q = sum of g^i D_i over GF(256), with g = 2 and Part 28's field
  (x^8 + x^4 + x^3 + x^2 + 1, the polynomial Linux's RAID 6 uses); any two lost disks can be solved for
  (Anvin, *The mathematics of RAID-6*).
* :func:`small_write_ios`: what a one-block write costs at each level.
* :func:`rebuild_risk`, :func:`mttdl`, :func:`simulate_mttdl`: a second failure, or an unreadable sector, during the
  hours a rebuild takes; mean time to data loss by formula and by simulation.
"""
from __future__ import annotations

import math
import random

from explainer.cs.algo.codes import gf_div, gf_mul, gf_pow


def layout(level: int, disks: int, stripes: int) -> list[list[str]]:
    """A grid [stripe][disk] of labels: "D3" for data block 3, "P"/"Q" for parity, "M3" for a mirror of block 3."""
    minimum = {0: 1, 1: 2, 4: 2, 5: 2, 6: 3}
    if level not in minimum or disks < minimum[level] or stripes < 0 or (level == 1 and disks % 2):
        raise ValueError("unsupported RAID level, disk count, or stripe count")
    grid = []
    b = 0
    for s in range(stripes):
        row = [""] * disks
        if level == 0:
            for d in range(disks):
                row[d] = f"D{b}"
                b += 1
        elif level == 1:
            row = [f"{'D' if d % 2 == 0 else 'M'}{b + d // 2}" for d in range(disks)]
            b += disks // 2
        elif level in (4, 5, 6):
            npar = 2 if level == 6 else 1
            if level == 4:
                par = [disks - 1]
            else:
                p = (disks - 1 - s) % disks          # rotating parity, left-symmetric
                par = [p] if level == 5 else [p, (p + 1) % disks]
            for d in range(disks):
                if d in par:
                    row[d] = "P" if d == par[0] else "Q"
            k = (par[-1] + 1) % disks if level != 4 else 0
            for _ in range(disks - npar):
                while row[k]:
                    k = (k + 1) % disks
                row[k] = f"D{b}"
                b += 1
        grid.append(row)
    return grid


def xor_parity(blocks: list[bytes]) -> bytes:
    out = bytearray(len(blocks[0]))
    for blk in blocks:
        for i, x in enumerate(blk):
            out[i] ^= x
    return bytes(out)


def rebuild_one(survivors: list[bytes]) -> bytes:
    """The lost block of a stripe is the XOR of every other block, parity included."""
    return xor_parity(survivors)


def pq(data: list[bytes]) -> tuple[bytes, bytes]:
    """RAID 6: P = XOR of D_i; Q = XOR of 2^i * D_i in GF(256)."""
    n = len(data[0])
    P = bytearray(n)
    Q = bytearray(n)
    for i, blk in enumerate(data):
        g = gf_pow(2, i)
        for j, x in enumerate(blk):
            P[j] ^= x
            Q[j] ^= gf_mul(g, x)
    return bytes(P), bytes(Q)


def rebuild_two(data: list[bytes | None], P: bytes, Q: bytes) -> list[bytes]:
    """Recover two missing data blocks (None) from the rest and P and Q.

    With x < y missing: P' = P + sum of the others = Dx + Dy, Q' = Q + sum of g^i D_i over the others
    = g^x Dx + g^y Dy, so Dx = (g^(y-x) P' + g^(-x) Q') / (g^(y-x) + 1) and Dy = P' + Dx."""
    miss = [i for i, b in enumerate(data) if b is None]
    assert len(miss) == 2
    x, y = miss
    n = len(P)
    Pp = bytearray(P)
    Qp = bytearray(Q)
    for i, blk in enumerate(data):
        if blk is None:
            continue
        g = gf_pow(2, i)
        for j, v in enumerate(blk):
            Pp[j] ^= v
            Qp[j] ^= gf_mul(g, v)
    gyx = gf_pow(2, y - x)
    ginvx = gf_div(1, gf_pow(2, x))
    den = gyx ^ 1
    Dx = bytes(gf_div(gf_mul(gyx, Pp[j]) ^ gf_mul(ginvx, Qp[j]), den) for j in range(n))
    Dy = bytes(Pp[j] ^ Dx[j] for j in range(n))
    out = list(data)
    out[x], out[y] = Dx, Dy
    return out


def small_write_ios(level: int) -> dict:
    """Disk operations for a one-block write: RAID 4/5 read the old data and parity and write both (P' = P + D +
    D'); RAID 6 does the same for Q too."""
    return {0: {"reads": 0, "writes": 1}, 1: {"reads": 0, "writes": 2}, 4: {"reads": 2, "writes": 2},
            5: {"reads": 2, "writes": 2}, 6: {"reads": 3, "writes": 3}}[level]


def throughput(level: int, n: int, S: float = 1.0, R: float = 1.0) -> dict:
    """OSTEP's table: sequential (S per disk) and random (R per disk) read and write throughput of n disks."""
    if level == 0:
        return {"seq_read": n * S, "seq_write": n * S, "rand_read": n * R, "rand_write": n * R, "capacity": n}
    if level == 1:
        return {"seq_read": n / 2 * S, "seq_write": n / 2 * S, "rand_read": n * R, "rand_write": n / 2 * R,
                "capacity": n / 2}
    if level == 4:
        return {"seq_read": (n - 1) * S, "seq_write": (n - 1) * S, "rand_read": (n - 1) * R, "rand_write": R / 2,
                "capacity": n - 1}
    if level == 5:
        return {"seq_read": (n - 1) * S, "seq_write": (n - 1) * S, "rand_read": n * R, "rand_write": n / 4 * R,
                "capacity": n - 1}
    if level == 6:
        return {"seq_read": (n - 2) * S, "seq_write": (n - 2) * S, "rand_read": n * R, "rand_write": n / 6 * R,
                "capacity": n - 2}
    raise ValueError(level)


def rebuild_hours(tb: float, mb_s: float) -> float:
    if not math.isfinite(tb) or tb < 0 or not math.isfinite(mb_s) or mb_s <= 0:
        raise ValueError("capacity must be nonnegative and rebuild bandwidth positive and finite")
    return tb * 1e12 / (mb_s * 1e6) / 3600


def rebuild_risk(n: int, tb: float, afr: float, rebuild_mb_s: float = 100.0, ure: float = 1e-15) -> dict:
    """While one of n disks is rebuilt (reading every survivor end to end): the chance another disk fails, and the
    chance some sector of the survivors cannot be read. Models independent Poisson errors at ``ure`` per bit,
    often a datasheet bound rather than a measured rate. ``p_loss`` is the union of these model events, not the
    probability that every byte of the array is lost; a bad sector may affect only one stripe."""
    if n < 2 or not math.isfinite(afr) or not 0 <= afr < 1 or not math.isfinite(ure) or ure < 0:
        raise ValueError("need at least two disks, AFR in [0, 1), and nonnegative finite URE rate")
    hours = rebuild_hours(tb, rebuild_mb_s)
    rate = -math.log1p(-afr) / 8766            # failures per disk-hour, from the annual failure rate
    fail_hazard = (n - 1) * rate * hours
    p_fail = -math.expm1(-fail_hazard)
    bits = (n - 1) * tb * 1e12 * 8
    ure_hazard = bits * ure
    p_ure = -math.expm1(-ure_hazard)
    return {"hours": hours, "p_second_failure": p_fail, "p_ure": p_ure, "bits_read": bits,
            "p_loss": -math.expm1(-(fail_hazard + ure_hazard))}


def _reliability_model(n: int, mttf: float, mttr: float, parity: int) -> None:
    if parity not in (1, 2) or n <= parity:
        raise ValueError("need one or two parity disks and at least one data disk")
    if not all(math.isfinite(t) and t > 0 for t in (mttf, mttr)):
        raise ValueError("MTTF and MTTR must be positive and finite")


def mttdl(n: int, mttf: float, mttr: float, parity: int = 1) -> float:
    """Mean time to data loss with independent exponential failures: RAID 5 MTTF^2 / (n (n-1) MTTR); RAID 6
    MTTF^3 / (n (n-1) (n-2) MTTR^2). Leading terms for fast, single-at-a-time repairs."""
    _reliability_model(n, mttf, mttr, parity)
    if parity == 1:
        return mttf ** 2 / (n * (n - 1) * mttr)
    return mttf ** 3 / (n * (n - 1) * (n - 2) * mttr ** 2)


def simulate_mttdl(n: int, mttf: float, mttr: float, parity: int = 1, trials: int = 2000, seed: int = 0) -> float:
    """Monte Carlo of the formula's model: each working disk fails at rate 1/mttf; one failed disk at a time is
    repaired, at rate 1/mttr; data is lost when more than ``parity`` are down at once."""
    _reliability_model(n, mttf, mttr, parity)
    if trials <= 0:
        raise ValueError("trials must be positive")
    rng = random.Random(seed)
    total = 0.0
    for _ in range(trials):
        t, k = 0.0, 0
        while k <= parity:
            fail = (n - k) / mttf
            fix = 1 / mttr if k else 0.0
            t += rng.expovariate(fail + fix)
            k += 1 if rng.random() < fail / (fail + fix) else -1
        total += t
    return total / trials


def mttdl_exact(n: int, mttf: float, mttr: float, parity: int = 1) -> float:
    """The same chain solved exactly: expected time from no failures to parity + 1 at once (the formula is its
    leading term when mttr << mttf / n)."""
    _reliability_model(n, mttf, mttr, parity)
    # d_k = T_k - T_{k+1}; the backward equations give
    # fail_k*d_k = 1 + repair*d_{k-1}. All terms are positive, avoiding
    # the near-singular transition matrix when failures are very rare.
    delta = mttf / n
    deltas = [delta]
    for k in range(1, parity + 1):
        delta = (1 + delta / mttr) * (mttf / (n - k))
        deltas.append(delta)
    return math.fsum(deltas)
