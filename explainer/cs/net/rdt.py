"""Reliable data transfer from scratch (Part 37): stop-and-wait (the alternating-bit protocol), Go-Back-N and
Selective Repeat, over a channel that loses, duplicates and reorders packets.

    run(protocol, n, window, seq_bits, channel, timeout)   send n packets; returns what the receiver delivered,
        in order, and counts (sent, retransmissions, time, utilization)
    utilization(L, R, rtt, window)   the textbook formula, min(1, W (L/R) / (RTT + L/R))

A channel: one-way propagation ``delay``, ``rate`` (packets a second, so a packet takes 1/rate to transmit),
``loss``, ``dup`` and ``reorder`` probabilities (a reordered packet is held back by an extra ``jitter``).
Sequence numbers are taken modulo 2^seq_bits, so a protocol with too few bits can be shown to fail: Selective
Repeat with a window larger than half the sequence space delivers duplicates as new data.
"""
from __future__ import annotations

import heapq
import random


class Channel:
    def __init__(self, delay=0.05, rate=1000.0, loss=0.0, dup=0.0, reorder=0.0, jitter=0.03, seed=0):
        self.delay, self.rate, self.loss, self.dup, self.reorder, self.jitter = delay, rate, loss, dup, reorder, jitter
        self.rng = random.Random(seed)

    def arrivals(self, t):
        """Arrival times of one packet sent at t (possibly none, possibly two)."""
        if self.rng.random() < self.loss:
            return []
        extra = self.jitter * self.rng.random() if self.rng.random() < self.reorder else 0.0
        out = [t + self.delay + extra]
        if self.rng.random() < self.dup:
            out.append(t + self.delay + self.jitter * self.rng.random())
        return out


def run(protocol: str, n: int, window: int = 1, seq_bits: int = 16, channel: Channel | None = None,
        timeout: float | None = None, ack_channel: Channel | None = None) -> dict:
    ch = channel or Channel()
    ack = ack_channel or Channel(ch.delay, ch.rate * 50, ch.loss, ch.dup, ch.reorder, ch.jitter, seed=ch.rng.random())
    S = 1 << seq_bits
    W = 1 if protocol == "stop-and-wait" else window
    T = timeout or (2 * ch.delay + 1 / ch.rate) * 1.5 + ch.jitter
    events = []
    seq = 0

    def push(t, kind, data):
        nonlocal seq
        seq += 1
        heapq.heappush(events, (t, seq, kind, data))

    # sender state
    base, nxt = 0, 0
    acked = [False] * n
    link_free = 0.0
    sent = retx = 0
    timers = {}
    # receiver state
    expected = 0
    buffer = {}
    delivered = []
    t = 0.0

    def transmit(i, now):
        nonlocal link_free, sent
        start = max(now, link_free)
        link_free = start + 1 / ch.rate
        sent += 1
        for a in ch.arrivals(link_free):
            push(a, "data", (i, i % S))
        key = 0 if protocol == "go-back-n" else i
        timers[key] = link_free + T
        push(link_free + T, "timeout", (key, link_free + T))

    while base < n:
        while nxt < n and nxt < base + W:
            transmit(nxt, t)
            nxt += 1
        if not events:
            break
        t, _, kind, data = heapq.heappop(events)
        if kind == "data":
            true_i, s = data
            if protocol in ("stop-and-wait", "go-back-n"):
                if s == expected % S:
                    delivered.append(true_i)
                    expected += 1
                for a in ack.arrivals(t):
                    push(a, "ack", (expected - 1) % S)          # cumulative: everything up to expected - 1
            else:   # selective repeat: buffer anything in the window; ACK each packet individually
                lo = expected
                off = (s - lo) % S
                if off < W:
                    idx = lo + off
                    if idx not in buffer and idx >= expected:
                        buffer[idx] = true_i
                    while expected in buffer:
                        delivered.append(buffer.pop(expected))
                        expected += 1
                for a in ack.arrivals(t):
                    push(a, "ack", s)
        elif kind == "ack":
            s = data
            if protocol in ("stop-and-wait", "go-back-n"):
                # the newest i in [base, nxt) with i % S == s
                cand = [i for i in range(base, nxt) if i % S == s]
                if cand:
                    i = cand[-1]
                    for k in range(base, i + 1):
                        acked[k] = True
                    base = i + 1
                    if protocol == "go-back-n" and base < nxt:
                        timers[0] = t + T
                        push(t + T, "timeout", (0, t + T))
                    else:
                        timers.pop(0, None)
            else:
                cand = [i for i in range(base, nxt) if i % S == s]
                for i in cand:
                    acked[i] = True
                    timers.pop(i, None)
                while base < n and acked[base]:
                    base += 1
        elif kind == "timeout":
            key, when = data
            if timers.get(key) != when:
                continue
            if protocol == "go-back-n":
                for i in range(base, nxt):
                    retx += 1
                    transmit(i, t)
            elif protocol == "stop-and-wait":
                if base < nxt:
                    retx += 1
                    transmit(base, t)
            else:
                if key < n and not acked[key]:
                    retx += 1
                    transmit(key, t)
    useful = n / ch.rate
    return {"protocol": protocol, "n": n, "window": W, "delivered": delivered, "correct": delivered == list(range(n)),
            "sent": sent, "retransmissions": retx, "time": t, "utilization": useful / t if t else 0.0}


def utilization(L_over_R: float, rtt: float, window: int = 1) -> float:
    return min(1.0, window * L_over_R / (rtt + L_over_R))
