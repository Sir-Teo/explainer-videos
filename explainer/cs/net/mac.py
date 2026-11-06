"""Sharing one channel (Part 36): ALOHA, slotted ALOHA, CSMA/CD with binary exponential backoff, and the hidden
terminal.

    aloha(G, frames, rng)          pure ALOHA: frames of length 1 start as a Poisson process of rate G; a frame
                                   succeeds if no other starts within one frame time either side.  S = G e^{-2G}
    slotted_aloha(G, slots, rng)   frames only at slot boundaries.  S = G e^{-G}
    csma_cd(n, a, frames, rng)     n saturated stations on a bus; a = propagation delay / frame time.  Contention in
                                   slots of 2a; binary exponential backoff after each collision (Metcalfe and Boggs)
    metcalfe_boggs(n, a)           the efficiency formula: 1 / (1 + a + 2a (1 - A) / A), A = (1 - 1/n)^(n-1)
    hidden_terminal(G, frames, rng, rts=False)  two senders that cannot hear each other, one receiver between them
"""
from __future__ import annotations

import math
import random


def aloha(G: float, frames: int, rng: random.Random) -> dict:
    t, starts = 0.0, []
    while len(starts) < frames:
        t += rng.expovariate(G)
        starts.append(t)
    ok = 0
    for i, s in enumerate(starts):
        prev_ok = i == 0 or s - starts[i - 1] >= 1
        next_ok = i == len(starts) - 1 or starts[i + 1] - s >= 1
        ok += prev_ok and next_ok
    T = starts[-1]
    return {"G": G, "S": ok / T, "formula": G * math.exp(-2 * G), "attempts": frames}


def slotted_aloha(G: float, slots: int, rng: random.Random) -> dict:
    ok = 0
    for _ in range(slots):
        # Poisson number of frames in the slot
        k, p, u = 0, math.exp(-G), rng.random()
        c = p
        while u > c:
            k += 1
            p *= G / k
            c += p
        ok += k == 1
    return {"G": G, "S": ok / slots, "formula": G * math.exp(-G)}


def csma_cd(n: int, a: float, frames: int, rng: random.Random, policy: str = "beb", cap: int = 10) -> dict:
    """Saturated stations.  Time in units of a frame; a contention slot lasts 2a (a collision is detected within the
    round trip).  A slot with exactly one transmitter wins the channel for 1 + a (the frame plus the last bit's
    propagation); with two or more it is a collision, and with none it is idle.

    policy "p": every station transmits in each slot with probability 1/n, the case Metcalfe and Boggs analysed.
    policy "beb": binary exponential backoff: after its k-th collision a station waits uniform [0, 2^min(k, cap) - 1]
    slots; counters run during idle and collision slots, and also tick once when a transmission ends, so that a
    station that has just sent does not capture the channel for ever."""
    backoff = [0] * n
    k = [0] * n
    t = 0.0
    sent = collisions = slots = 0
    while sent < frames:
        if policy == "p":
            ready = [i for i in range(n) if rng.random() < 1 / n]
        else:
            ready = [i for i in range(n) if backoff[i] == 0]
        if len(ready) == 1:
            i = ready[0]
            t += 1 + a
            sent += 1
            k[i] = 0
            for j in range(n):
                if j != i and backoff[j] > 0:
                    backoff[j] -= 1
            backoff[i] = rng.randrange(2) if policy == "beb" else 0
            continue
        t += 2 * a
        slots += 1
        for j in range(n):
            if j not in ready and backoff[j] > 0:
                backoff[j] -= 1
        if len(ready) > 1:
            collisions += 1
            for i in ready:
                k[i] += 1
                backoff[i] = rng.randrange(2 ** min(k[i], cap))
    return {"n": n, "a": a, "policy": policy, "efficiency": frames / t, "collisions": collisions,
            "contention_slots": slots, "formula": metcalfe_boggs(n, a)}


def metcalfe_boggs(n: int, a: float) -> float:
    """Each frame occupies 1 + a; between frames, contention slots of 2a until exactly one of n stations, each
    sending with probability 1/n, transmits: A = (1 - 1/n)^(n-1) per slot, so (1 - A)/A wasted slots on average."""
    A = (1 - 1 / n) ** (n - 1) if n > 1 else 1.0
    return 1 / (1 + a + 2 * a * (1 - A) / A)


def hidden_terminal(G: float, frames: int, rng: random.Random, rts: bool = False, rts_len: float = 0.05) -> dict:
    """Stations A and C each offer Poisson attempts at rate G/2 (frames of length 1) to B between them.  They
    cannot hear each other, so to each other they are ALOHA: a frame fails if the other station starts within one
    frame time either side.  With RTS/CTS only the short RTS (rts_len) is exposed; B's CTS, heard by both, then
    reserves the channel for the frame, and attempts during a reservation wait (they are not counted again)."""
    import bisect
    starts = {0: [], 1: []}
    for who in (0, 1):
        t = 0.0
        for _ in range(frames // 2):
            t += rng.expovariate(G / 2)
            starts[who].append(t)
    T = min(starts[0][-1], starts[1][-1])
    L = rts_len if rts else 1.0
    ev = sorted((s, w) for w in (0, 1) for s in starts[w] if s <= T)
    ok, busy_until = 0, -1.0
    for s, who in ev:
        if s < busy_until:
            continue
        other = starts[1 - who]
        j = bisect.bisect_left(other, s - L)
        clash = j < len(other) and other[j] < s + L and not (other[j] < busy_until)
        if not clash:
            ok += 1
            if rts:
                busy_until = s + rts_len + 1
    return {"G": G, "rts": rts, "S": ok / T, "aloha": G * math.exp(-G)}
