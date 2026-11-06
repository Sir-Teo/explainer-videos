"""Consensus (Part 38): FLP's dichotomy explored exhaustively, synchronous consensus in f + 1 rounds, Ben-Or's
randomized consensus, and single-decree Paxos under loss and duelling proposers.

    explore(protocol, inputs, n, f)   every schedule of a tiny asynchronous protocol (message deliveries in any order,
        up to f crashes at any time): the set of decisions reachable (the configuration's valency), whether two
        processes can decide differently, and whether a run can leave a live process undecided for ever
    floodset(n, f, rounds)            synchronous crash consensus by flooding the set of values seen, checked against
        every crash pattern (who crashes in which round, and which of its last messages get through)
    ben_or(n, f, inputs, seed)        randomized binary consensus: rounds until every live process decides
    paxos(n_acceptors, proposers, loss, seed)  Paxos with several proposers: what was chosen, and whether two
        different values ever were
"""
from __future__ import annotations

import heapq
import itertools
import random
from functools import lru_cache


# ---- FLP on a tiny protocol ------------------------------------------------------------------------------------
def explore(protocol: str, inputs, f: int = 1):
    """protocol "wait-n-f": decide the majority (ties to 0) of the first n - f values received (own value
    included); "wait-all": wait for all n values.  Returns valency and the two failure modes."""
    n = len(inputs)
    need = n - f if protocol == "wait-n-f" else n

    start_msgs = tuple(sorted((s, d) for s in range(n) for d in range(n) if s != d))
    start_recv = tuple(frozenset({(i, inputs[i])}) for i in range(n))

    @lru_cache(maxsize=None)
    def go(recv, msgs, crashed, decided):
        decisions = set()
        disagree = False
        stuck = False
        live = [i for i in range(n) if i not in crashed]
        # decide whenever possible (deterministically, right away)
        recv, decided = list(recv), list(decided)
        for i in live:
            if decided[i] is None and len(recv[i]) >= need:
                vals = [v for _, v in sorted(recv[i])][:need] if protocol == "wait-all" else [v for _, v in recv[i]]
                ones = sum(vals)
                decided[i] = 1 if ones * 2 > len(vals) else 0
        recv, decided = tuple(recv), tuple(decided)
        ds = {d for d in decided if d is not None}
        decisions |= ds
        if len(ds) > 1:
            disagree = True
        moves = []
        for k, (s, d) in enumerate(msgs):
            if d in crashed:
                continue
            if decided[d] is not None:
                continue
            moves.append(("deliver", k))
        if len(crashed) < f:
            for i in live:
                moves.append(("crash", i))
        if not moves:
            if any(decided[i] is None for i in live):
                stuck = True
            return frozenset(decisions), disagree, stuck
        for mv in moves:
            if mv[0] == "deliver":
                s, d = msgs[mv[1]]
                nr = list(recv)
                nr[d] = recv[d] | {(s, inputs[s])}
                nm = msgs[:mv[1]] + msgs[mv[1] + 1:]
                r = go(tuple(nr), nm, crashed, decided)
            else:
                i = mv[1]
                # a crash loses the crashed process's undelivered messages (those delivered before it, in some
                # other schedule, model a crash part-way through sending)
                nm = tuple(m for m in msgs if m[0] != i)
                r = go(recv, nm, crashed | frozenset({i}), decided)
            decisions |= r[0]
            disagree = disagree or r[1]
            stuck = stuck or r[2]
        return frozenset(decisions), disagree, stuck

    dec, dis, st = go(start_recv, start_msgs, frozenset(), tuple([None] * n))
    return {"inputs": list(inputs), "valency": sorted(dec), "bivalent": len(dec) > 1, "can_disagree": dis,
            "can_block": st}


def flp_table(protocol: str, n: int = 3, f: int = 1):
    return [explore(protocol, inp, f) for inp in itertools.product((0, 1), repeat=n)]


# ---- synchronous: floodset in f + 1 rounds ---------------------------------------------------------------------
def floodset(n: int = 4, f: int = 1, rounds: int | None = None, inputs=None):
    """Exhaustively check FloodSet (decide min of the values seen) with every crash pattern of up to f processes:
    each crash happens in some round, after the process sends to some subset of the others.  Returns whether
    agreement always holds, and a counterexample if not."""
    rounds = rounds if rounds is not None else f + 1
    all_inputs = [inputs] if inputs else list(itertools.product((0, 1), repeat=n))
    counter = None
    checked = 0
    procs = range(n)
    # a crash event: (process, round, frozenset of receivers that still get its message that round)
    events = [(p, r, frozenset(rcv)) for p in procs for r in range(rounds)
              for k in range(n) for rcv in itertools.combinations([q for q in procs if q != p], k)]
    patterns = [()]
    for k in range(1, f + 1):
        for combo in itertools.combinations(events, k):
            if len({c[0] for c in combo}) == k:
                patterns.append(combo)
    for inp in all_inputs:
        for pat in patterns:
            checked += 1
            W = [{inp[i]} for i in procs]
            dead_at = {p: (r, rcv) for p, r, rcv in pat}
            alive = set(procs)
            for r in range(rounds):
                new = [set(w) for w in W]
                for p in procs:
                    if p not in alive:
                        continue
                    targets = [q for q in procs if q != p]
                    if p in dead_at and dead_at[p][0] == r:
                        targets = list(dead_at[p][1])
                    for q in targets:
                        new[q] |= W[p]
                for p, (rr, _) in dead_at.items():
                    if rr == r:
                        alive.discard(p)
                W = new
            ds = {min(W[p]) for p in alive}
            if len(ds) > 1 and counter is None:
                counter = {"inputs": list(inp), "crashes": [(p, r + 1, sorted(rcv)) for p, r, rcv in pat],
                           "decisions": {p: min(W[p]) for p in sorted(alive)}}
    return {"n": n, "f": f, "rounds": rounds, "patterns": len(patterns), "checked": checked,
            "agreement": counter is None, "counterexample": counter}


# ---- Ben-Or --------------------------------------------------------------------------------------------------
def ben_or(n: int = 5, f: int = 2, inputs=None, seed: int = 0, max_rounds: int = 1000):
    """Ben-Or (1983) for crash failures, n > 2f, simulated with random message delays: each phase every process
    waits for n - f reports; if more than n/2 report the same value it proposes it, else '?'; then waits for n - f
    proposals: decides v if more than f propose v, adopts v if at least one does, else flips a coin."""
    rng = random.Random(seed)
    x = list(inputs) if inputs is not None else [rng.randrange(2) for _ in range(n)]
    crashed = set(rng.sample(range(n), f))
    decided = {}
    rnd = 0
    while rnd < max_rounds:
        rnd += 1
        live = [i for i in range(n) if i not in crashed]
        # phase 1: each live process hears n - f reports, from a random subset (asynchrony)
        prop = {}
        for i in live:
            heard = rng.sample(live, n - f)
            vals = [x[j] for j in heard]
            c1 = vals.count(1)
            prop[i] = 1 if c1 * 2 > n else (0 if (len(vals) - c1) * 2 > n else None)
        for i in live:
            heard = rng.sample(live, n - f)
            ps = [prop[j] for j in heard if prop[j] is not None]
            if ps:
                v = ps[0]
                if sum(1 for p in ps if p == v) > f:
                    decided.setdefault(i, (v, rnd))
                x[i] = v
            else:
                x[i] = rng.randrange(2)
        if all(i in decided for i in live):
            vals = {v for v, _ in decided.values()}
            return {"rounds": max(r for _, r in decided.values()), "agreement": len(vals) == 1, "value": vals.pop()}
    return {"rounds": None, "agreement": True, "value": None}


# ---- Paxos ---------------------------------------------------------------------------------------------------
def paxos(n: int = 5, proposers: int = 2, loss: float = 0.1, seed: int = 0, until: float = 5.0,
          backoff: bool = True, retry: float = 0.1, delay=(0.005, 0.03)):
    """Single-decree Paxos.  Each proposer p picks ballots p, p + P, p + 2P, ...; phase 1 (prepare / promise) and
    phase 2 (accept / accepted) as in "Paxos Made Simple"; a value is chosen when a majority of acceptors accept
    the same ballot.  Proposers retry after a timeout, with random backoff if ``backoff``.  Returns the chosen
    value(s), the ballots used and the message count."""
    rng = random.Random(seed)
    P = proposers
    promised = [-1] * n
    accepted = [None] * n                     # (ballot, value)
    events, k = [], 0
    chosen = {}
    accepted_by = {}
    msgs = 0
    state = {p: {"ballot": p - P, "phase": 0, "promises": {}, "acks": set(), "value": f"v{p}"} for p in range(P)}

    def push(t, kind, data):
        nonlocal k
        k += 1
        heapq.heappush(events, (t, k, kind, data))

    def send(t, kind, data):
        nonlocal msgs
        msgs += 1
        if rng.random() >= loss:
            push(t + rng.uniform(*delay), kind, data)

    def start(p, t):
        s = state[p]
        s["ballot"] += P
        s["phase"], s["promises"], s["acks"] = 1, {}, set()
        for a in range(n):
            send(t, "prepare", (p, a, s["ballot"]))
        arm(p, t)

    def arm(p, t):
        s = state[p]
        s["token"] = s.get("token", 0) + 1                  # each phase gets its own deadline
        push(t + retry + (rng.uniform(0, 2 * retry) if backoff else 0.0), "retry", (p, s["token"]))

    for p in range(P):
        push(rng.uniform(0, 0.01), "start", p)
    attempts = 0
    while events:
        t, _, kind, data = heapq.heappop(events)
        if t > until:
            break
        if kind == "start":
            attempts += 1
            start(data, t)
        elif kind == "retry":
            p, tok = data
            if state[p].get("token") == tok and not chosen:
                attempts += 1
                start(p, t)
        elif kind == "prepare":
            p, a, b = data
            if b > promised[a]:
                promised[a] = b
                send(t, "promise", (p, a, b, accepted[a]))
            else:
                send(t, "nack", (p, a, b, promised[a]))
        elif kind == "promise":
            p, a, b, acc = data
            s = state[p]
            if s["ballot"] == b and s["phase"] == 1:
                s["promises"][a] = acc
                if len(s["promises"]) > n // 2:
                    prior = [x for x in s["promises"].values() if x is not None]
                    if prior:
                        s["value"] = max(prior)[1]           # the value of the highest ballot already accepted
                    s["phase"] = 2
                    arm(p, t)
                    for a2 in range(n):
                        send(t, "accept", (p, a2, b, s["value"]))
        elif kind == "accept":
            p, a, b, v = data
            if b >= promised[a]:
                promised[a] = b
                accepted[a] = (b, v)
                accepted_by.setdefault((b, v), set()).add(a)
                if len(accepted_by[(b, v)]) > n // 2:
                    chosen.setdefault(v, (b, t))
                send(t, "accepted", (p, a, b))
            else:
                send(t, "nack", (p, a, b, promised[a]))
        elif kind == "nack":
            p, a, b, higher = data
            s = state[p]
            if s["ballot"] == b and not chosen and s.get("nacked") != b:
                s["nacked"] = b                                  # pre-empted: try again above the rival's ballot
                while s["ballot"] + P <= higher:
                    s["ballot"] += P
                wait = rng.uniform(0, 4 * retry) if backoff else 0.0
                s["token"] = s.get("token", 0) + 1
                push(t + wait, "restart", (p, s["token"]))
        elif kind == "restart":
            p, tok = data
            if state[p].get("token") == tok and not chosen:
                attempts += 1
                start(p, t)
    return {"chosen": {v: {"ballot": b, "time": round(tt, 4)} for v, (b, tt) in chosen.items()},
            "safe": len(chosen) <= 1, "messages": msgs, "attempts": attempts,
            "first": min((tt for _, (b, tt) in chosen.items()), default=None)}


_ = itertools
