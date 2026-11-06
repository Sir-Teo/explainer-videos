"""The link layer (Part 36): framing by bit stuffing, Ethernet frames with their CRC-32, and how often CRC-32 misses
an error.

    stuff(bits) / unstuff(bits)       HDLC bit stuffing: a 0 after every five 1s, so the flag 01111110 cannot occur
    frame(bits) / deframe(stream)     flag, stuffed payload, flag
    ethernet(dst, src, ethertype, payload) -> bytes, with the FCS (CRC-32, as zlib computes it)
    fcs_ok(frame)                     whether the last four bytes are the CRC-32 of the rest
    crc_trial(kind, n, rng)           corrupt n frames (single bits, two bits, bursts up to 32, or random noise) and
                                      count how many the CRC fails to catch
"""
from __future__ import annotations

import random

from explainer.cs.algo.codes import crc32

FLAG = [0, 1, 1, 1, 1, 1, 1, 0]


def stuff(bits: list[int]) -> list[int]:
    out, run = [], 0
    for b in bits:
        out.append(b)
        run = run + 1 if b else 0
        if run == 5:
            out.append(0)
            run = 0
    return out


def unstuff(bits: list[int]) -> list[int]:
    out, run, skip = [], 0, False
    for b in bits:
        if skip:
            assert b == 0, "a stuffed bit must be 0"
            skip = False
            run = 0
            continue
        out.append(b)
        run = run + 1 if b else 0
        if run == 5:
            skip = True
    return out


def frame(bits: list[int]) -> list[int]:
    return FLAG + stuff(bits) + FLAG


def deframe(stream: list[int]) -> list[list[int]]:
    """Split a bit stream at flags and unstuff each frame."""
    s = "".join(map(str, stream))
    f = "".join(map(str, FLAG))
    parts = s.split(f)
    return [unstuff([int(c) for c in p]) for p in parts if p]


def to_bits(data: bytes) -> list[int]:
    return [(byte >> (7 - i)) & 1 for byte in data for i in range(8)]


def mac(s: str) -> bytes:
    return bytes(int(x, 16) for x in s.split(":"))


def ethernet(dst: str, src: str, ethertype: int, payload: bytes) -> bytes:
    body = mac(dst) + mac(src) + ethertype.to_bytes(2, "big") + payload.ljust(46, b"\0")
    return body + crc32(body).to_bytes(4, "little")


def fcs_ok(fr: bytes) -> bool:
    return crc32(fr[:-4]).to_bytes(4, "little") == fr[-4:]


def crc_trial(kind: str, n: int, rng: random.Random, length: int = 64) -> dict:
    missed = 0
    base = bytes(rng.randrange(256) for _ in range(length))
    good = base + crc32(base).to_bytes(4, "little")
    nbits = len(good) * 8
    for _ in range(n):
        b = bytearray(good)
        if kind == "single":
            flips = [rng.randrange(nbits)]
        elif kind == "double":
            flips = rng.sample(range(nbits), 2)
        elif kind == "burst":
            L = rng.randint(2, 32)
            start = rng.randrange(nbits - L)
            inner = [start + i for i in range(1, L - 1) if rng.random() < 0.5]
            flips = [start, start + L - 1] + inner
        elif kind == "random":
            flips = [i for i in range(nbits) if rng.random() < 0.5]
        else:
            raise ValueError(kind)
        for f in flips:
            b[f // 8] ^= 0x80 >> (f % 8)
        if bytes(b) != good and fcs_ok(bytes(b)):
            missed += 1
    return {"kind": kind, "frames": n, "missed": missed}
