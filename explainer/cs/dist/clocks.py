"""Time without a shared clock (Part 38): Lamport clocks, vector clocks, NTP's offset, and Chandy-Lamport snapshots.

    tr = random_trace(n=3, events=12, seed=1)       # [(process, kind, peer, msg id)] kinds: local, send, recv
    L = lamport(tr); V = vector(tr)
    happened_before(tr) -> set of (e, f) pairs, by the transitive closure of program order and messages
    check_vector(tr): V[e] < V[f] iff e -> f, for every pair (the characterization theorem, tested)
    ntp(t0, t1, t2, t3) -> (offset, delay)
    Bank(n, seed).run(snapshot_at=...) : processes moving money over FIFO channels; a Chandy-Lamport snapshot of
        local balances and channel contents, whose total equals the money in the system (and an inconsistent cut
        taken naively, which does not)
"""
from __future__ import annotations

import heapq
import itertools
import random


def random_trace(n: int = 3, events: int = 12, seed: int = 0, p_send: float = 0.4):
    """A random execution: each step one process does a local event, sends to another, or receives a pending
    message.  Returns events [(proc, kind, peer, mid)] in a valid real-time order."""
    rng = random.Random(seed)
    tr, pending, mid = [], [], 0
    while len(tr) < events:
        if pending and rng.random() < 0.45:
            k = rng.randrange(len(pending))
            src, dst, m = pending.pop(k)
            tr.append((dst, "recv", src, m))
        else:
            p = rng.randrange(n)
            if rng.random() < p_send:
                q = rng.choice([x for x in range(n) if x != p])
                tr.append((p, "send", q, mid))
                pending.append((p, q, mid))
                mid += 1
            else:
                tr.append((p, "local", None, None))
    for src, dst, m in pending:                         # deliver what is left
        tr.append((dst, "recv", src, m))
    return tr


def lamport(tr):
    c = {}
    sent = {}
    out = []
    for p, kind, peer, m in tr:
        t = c.get(p, 0)
        if kind == "recv":
            t = max(t, sent[m])
        t += 1
        c[p] = t
        if kind == "send":
            sent[m] = t
        out.append(t)
    return out


def vector(tr, n=None):
    n = n or (max(p for p, *_ in tr) + 1)
    c = {p: [0] * n for p in range(n)}
    sent = {}
    out = []
    for p, kind, peer, m in tr:
        v = c[p]
        if kind == "recv":
            v = [max(a, b) for a, b in zip(v, sent[m])]
        v = list(v)
        v[p] += 1
        c[p] = v
        if kind == "send":
            sent[m] = list(v)
        out.append(tuple(v))
    return out


def happened_before(tr):
    n_ev = len(tr)
    edges = {i: set() for i in range(n_ev)}
    last = {}
    send_of = {}
    for i, (p, kind, peer, m) in enumerate(tr):
        if p in last:
            edges[last[p]].add(i)
        last[p] = i
        if kind == "send":
            send_of[m] = i
        elif kind == "recv":
            edges[send_of[m]].add(i)
    hb = set()
    for i in range(n_ev):
        stack, seen = list(edges[i]), set()
        while stack:
            j = stack.pop()
            if j in seen:
                continue
            seen.add(j)
            hb.add((i, j))
            stack.extend(edges[j])
    return hb


def vless(a, b):
    return all(x <= y for x, y in zip(a, b)) and a != b


def check_vector(tr):
    """True iff, for all pairs, V(e) < V(f) exactly when e happened before f; also Lamport's clock condition."""
    V, L, hb = vector(tr), lamport(tr), happened_before(tr)
    ok_v = all(vless(V[i], V[j]) == ((i, j) in hb) for i, j in itertools.permutations(range(len(tr)), 2))
    ok_l = all(L[i] < L[j] for i, j in hb)
    concurrent = sum(1 for i, j in itertools.combinations(range(len(tr)), 2) if (i, j) not in hb and (j, i) not in hb)
    lamport_misleads = sum(1 for i, j in itertools.combinations(range(len(tr)), 2)
                           if (i, j) not in hb and (j, i) not in hb and L[i] != L[j])
    return {"vector_characterizes": ok_v, "lamport_condition": ok_l, "pairs": len(tr) * (len(tr) - 1) // 2,
            "ordered": len(hb), "concurrent": concurrent, "lamport_orders_concurrent": lamport_misleads}


def ntp(t0, t1, t2, t3):
    """Client sends at t0 (its clock), server receives at t1 and replies at t2 (server clock), client receives at
    t3.  Offset θ = ((t1 - t0) + (t2 - t3)) / 2, round-trip delay δ = (t3 - t0) - (t2 - t1); θ is exact only if
    the two directions take equal time, and is off by half the asymmetry otherwise."""
    return ((t1 - t0) + (t2 - t3)) / 2, (t3 - t0) - (t2 - t1)


class Bank:
    """n processes, each with a balance, sending random amounts to each other over FIFO channels with random
    delays.  ``snapshot(at, initiator)`` runs Chandy and Lamport's algorithm: the initiator records its state and
    sends a marker on every channel; a process receiving its first marker records its state, marks that channel
    empty and sends markers on; until a marker arrives on a channel, money arriving on it is recorded as in
    transit."""

    def __init__(self, n: int = 4, money: int = 1000, seed: int = 0):
        self.n = n
        self.rng = random.Random(seed)
        self.bal = [money // n] * n
        self.total = money
        self.events: list = []
        self.k = 0
        self.chan_last = {}                            # (a, b) -> time of last delivery, to keep channels FIFO
        self.snap = None
        self.log = []

    def _push(self, t, kind, data):
        self.k += 1
        heapq.heappush(self.events, (t, self.k, kind, data))

    def _send(self, t, a, b, msg):
        d = self.rng.uniform(0.1, 1.0)
        at = max(t + d, self.chan_last.get((a, b), 0) + 1e-6)
        self.chan_last[(a, b)] = at
        self._push(at, "deliver", (a, b, msg))

    def _record(self, i, t):
        s = self.snap
        s["state"][i] = self.bal[i]
        s["recording"].update({(j, i) for j in range(self.n) if j != i})
        for j in range(self.n):
            if j != i:
                self._send(t, i, j, ("marker",))

    def run(self, until: float = 20.0, snapshot_at: float | None = 8.0, initiator: int = 0, rate: float = 3.0):
        for i in range(self.n):
            self._push(self.rng.expovariate(rate), "transfer", i)
        if snapshot_at is not None:
            self._push(snapshot_at, "snapshot", initiator)
            for i in range(self.n):                   # a naive survey: ask each process in turn, a second apart
                self._push(snapshot_at + i * 1.0, "peek", i)
        peeks = {}
        naive = None
        while self.events:
            t, _, kind, data = heapq.heappop(self.events)
            if t > until:
                break
            if kind == "transfer":
                i = data
                amt = self.rng.randint(1, max(1, self.bal[i] // 4)) if self.bal[i] > 0 else 0
                if amt:
                    j = self.rng.choice([x for x in range(self.n) if x != i])
                    self.bal[i] -= amt
                    self._send(t, i, j, ("money", amt))
                    self.log.append((t, i, j, amt))
                self._push(t + self.rng.expovariate(rate), "transfer", i)
            elif kind == "snapshot":
                self.snap = {"state": {}, "channels": {}, "recording": set(), "start": t}
                # a naive "snapshot": read every balance at slightly different moments, ignoring channels
                naive = {"balances": list(self.bal)}
                self._record(data, t)
            elif kind == "peek":
                peeks[data] = self.bal[data]
            elif kind == "deliver":
                a, b, msg = data
                if msg[0] == "money":
                    self.bal[b] += msg[1]
                    if self.snap and (a, b) in self.snap["recording"]:
                        self.snap["channels"][(a, b)] = self.snap["channels"].get((a, b), 0) + msg[1]
                elif msg[0] == "marker" and self.snap is not None:
                    if b not in self.snap["state"]:
                        self._record(b, t)
                    self.snap["recording"].discard((a, b))
                    if not self.snap["recording"] and len(self.snap["state"]) == self.n and "end" not in self.snap:
                        self.snap["end"] = t
        s = self.snap
        out = {"total": self.total}
        if s:
            recorded = sum(s["state"].values()) + sum(s["channels"].values())
            out.update({"states": dict(s["state"]), "channels": {f"{a}->{b}": v for (a, b), v in s["channels"].items()},
                        "recorded_total": recorded, "consistent": recorded == self.total,
                        "instant_total": sum(naive["balances"]), "survey": peeks,
                        "survey_total": sum(peeks.values()), "start": s["start"], "end": s.get("end")})
        return out


# ---------------------------------------------------------------- hybrid logical clocks (Part 39)

def hlc_trace(n: int = 4, events: int = 20000, eps_ms: float = 5.0, delay_ms=(0.2, 3.0), p_send: float = 0.5,
              seed: int = 0):
    """``n`` processes whose physical clocks are off by up to ``eps_ms`` (fixed offsets) exchange messages with
    random delays.  Three timestamps per event: the physical clock, a Lamport clock, and a hybrid logical clock
    (Kulkarni et al. 2014), a pair (l, c) where l tracks the largest physical time heard of and c breaks ties.
    Returns, for each, the fraction of messages whose receive is not stamped after its send, and how far the
    timestamp strays from true time."""
    import random as _r
    rng = _r.Random(seed)
    off = [rng.uniform(-eps_ms, eps_ms) for _ in range(n)]
    t = 0.0
    lam = [0] * n
    hl = [0.0] * n
    hc = [0] * n
    inflight: list = []
    stats = {"physical": [0, 0.0], "lamport": [0, 0.0], "hlc": [0, 0.0]}
    msgs = 0
    maxc = 0
    for _ in range(events):
        t += rng.expovariate(1.0) * 0.5
        i = rng.randrange(n)
        pt = t + off[i]
        due = [m for m in inflight if m[0] <= t and m[1] == i]
        if due:
            m = due[0]
            inflight.remove(m)
            _, _, spt, slam, sl, sc = m
            lam[i] = max(lam[i], slam) + 1
            lp = hl[i]
            hl[i] = max(lp, sl, pt)
            if hl[i] == lp and hl[i] == sl:
                hc[i] = max(hc[i], sc) + 1
            elif hl[i] == lp:
                hc[i] += 1
            elif hl[i] == sl:
                hc[i] = sc + 1
            else:
                hc[i] = 0
            msgs += 1
            if pt <= spt:
                stats["physical"][0] += 1
            if (hl[i], hc[i]) <= (sl, sc):
                stats["hlc"][0] += 1
            if lam[i] <= slam:
                stats["lamport"][0] += 1
        else:
            lam[i] += 1
            lp = hl[i]
            hl[i] = max(lp, pt)
            hc[i] = hc[i] + 1 if hl[i] == lp else 0
            if rng.random() < p_send:
                j = rng.randrange(n - 1)
                j = j + (j >= i)
                inflight.append((t + rng.uniform(*delay_ms), j, pt, lam[i], hl[i], hc[i]))
        maxc = max(maxc, hc[i])
        stats["physical"][1] = max(stats["physical"][1], abs(pt - t))
        stats["hlc"][1] = max(stats["hlc"][1], abs(hl[i] - t))
    out = {k: {"violations": v[0] / max(1, msgs), "max_drift_ms": v[1]} for k, v in stats.items()}
    out["lamport"]["max_drift_ms"] = None
    out["lamport"]["final_value"] = max(lam)
    return {"schemes": out, "messages": msgs, "max_c": maxc, "eps_ms": eps_ms, "true_end_ms": t}
