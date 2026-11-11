"""BGP (Part 36): path-vector routing with business relationships, prefix hijacks and route-origin validation, and
policy disputes that never converge.

    tiered(rng, tier1, tier2, stubs)   a synthetic AS graph: a clique of tier-1 peers, tier-2 ASes buying transit
        from one or two tier-1s and peering among themselves, stub ASes buying from one or two tier-2s.
        rel[a][b] is "customer" (b is a's customer), "peer" or "provider"
    propagate(rel, announcements, rov=set(), roa={})   announcements: [(origin AS, prefix)]; every AS keeps, per
        prefix, its best route: customer routes over peer routes over provider routes (Gao and Rexford), then the
        shorter AS path, then the lower neighbour.  It exports customer routes to everyone and peer or provider
        routes only to customers.  ASes in ``rov`` drop routes that a ROA (prefix -> (allowed origin, max length))
        marks invalid.  Returns {AS: {prefix: path}}
    reach(routes, addr_prefixes) for each AS, which origin its traffic to an address goes to (longest match)
    spp(nodes, permitted, rounds)   the stable-paths problem (Griffin, Shepherd and Wilfong): each node ranks its
        permitted paths to node 0; run synchronous best-response and report whether it settles or cycles
"""
from __future__ import annotations

import random

from explainer.cs.net.ip import Prefix

PREF = {"customer": 3, "peer": 2, "provider": 1}


def tiered(rng: random.Random, tier1: int = 5, tier2: int = 20, stubs: int = 100, peer_p: float = 0.15):
    rel: dict = {}

    def link(a, b, kind):                    # kind: what b is to a
        rel.setdefault(a, {})[b] = kind
        rel.setdefault(b, {})[a] = {"customer": "provider", "provider": "customer", "peer": "peer"}[kind]
    T1 = list(range(1, tier1 + 1))
    T2 = list(range(100, 100 + tier2))
    ST = list(range(1000, 1000 + stubs))
    for i, a in enumerate(T1):
        for b in T1[i + 1:]:
            link(a, b, "peer")
    for a in T2:
        for p in rng.sample(T1, rng.choice((1, 2))):
            link(p, a, "customer")
    for i, a in enumerate(T2):
        for b in T2[i + 1:]:
            if rng.random() < peer_p:
                link(a, b, "peer")
    for s in ST:
        for p in rng.sample(T2, rng.choice((1, 1, 2))):
            link(p, s, "customer")
    return rel, {"tier1": T1, "tier2": T2, "stubs": ST}


def _better(a, b):
    """a, b: (pref, path) or None."""
    if b is None:
        return True
    if a[0] != b[0]:
        return a[0] > b[0]
    if len(a[1]) != len(b[1]):
        return len(a[1]) < len(b[1])
    return a[1] < b[1]


def _valid(origin: int, prefix: Prefix, roa: dict) -> bool:
    """Route-origin validation against ROAs: {covering Prefix: (asn, max length)}.  Valid if some ROA covering the
    prefix names this origin and allows this length; invalid if ROAs cover it but none match; unknown otherwise
    (treated as valid)."""
    covering = [(p, v) for p, v in roa.items() if p.len <= prefix.len and p.contains(prefix.net)]
    if not covering:
        return True
    return any(asn == origin and prefix.len <= ml for _, (asn, ml) in covering)


def propagate(rel: dict, announcements: list, rov: set = frozenset(), roa: dict | None = None,
              max_rounds: int = 100) -> dict:
    roa = roa or {}
    best: dict = {a: {} for a in rel}               # AS -> prefix -> (pref, path)
    for origin, prefix in announcements:
        best[origin][prefix] = (4, (origin,))
    rounds = 0
    for rounds in range(1, max_rounds + 1):
        changed = False
        offers = []
        for a in rel:
            for prefix, (pref, path) in best[a].items():
                for b, kind_b in rel[a].items():   # kind_b: what b is to a
                    if pref in (4, 3) or kind_b == "customer":     # own or customer routes go to all
                        if b in path:
                            continue
                        offers.append((b, prefix, path))
        new = {a: dict(v) for a, v in best.items()}
        for b, prefix, path in offers:
            if b in rov and not _valid(path[-1], prefix, roa):
                continue
            a = path[0]
            kind = rel[b][a]                         # what the sender is to b
            cand = (PREF[kind], (b,) + path)
            cur = new[b].get(prefix)
            if cur is not None and cur[0] == 4:
                continue
            if _better(cand, cur):
                new[b][prefix] = cand
        # withdraw routes whose next hop no longer has them (not needed for announce-only runs)
        if new != best:
            changed = True
        best = new
        if not changed:
            break
    return {"routes": {a: {p: path for p, (_, path) in v.items()} for a, v in best.items()}, "rounds": rounds}


def reach(routes: dict, addr: int) -> dict:
    """For each AS, the origin AS its traffic to ``addr`` reaches (longest matching prefix wins)."""
    out = {}
    for a, table in routes.items():
        match = [(p, path) for p, path in table.items() if p.contains(addr)]
        if not match:
            out[a] = None
            continue
        p, path = max(match, key=lambda m: m[0].len)
        out[a] = path[-1]
    return out


def spp(permitted: dict, rounds: int = 30) -> dict:
    """permitted: node -> list of paths (tuples ending at 0), best first.  Synchronous best response: each node
    picks its highest-ranked permitted path whose next hop currently uses exactly the rest of that path."""
    choice = {v: None for v in permitted}
    history = [dict(choice)]
    for r in range(rounds):
        new = {}
        for v, paths in permitted.items():
            pick = None
            for p in paths:
                nxt = p[1]
                rest = p[1:]
                if nxt == 0 or choice.get(nxt) == rest:
                    pick = p
                    break
            new[v] = pick
        history.append(dict(new))
        if new == choice:
            return {"stable": True, "rounds": r, "history": history, "choice": new}
        if any(h == new for h in history[:-1]):
            return {"stable": False, "cycle_at": r, "history": history}
        choice = new
    return {"stable": False, "history": history}


BAD_GADGET = {1: [(1, 2, 0), (1, 0)], 2: [(2, 3, 0), (2, 0)], 3: [(3, 1, 0), (3, 0)]}
GOOD_GADGET = {1: [(1, 2, 0), (1, 0)], 2: [(2, 0), (2, 3, 0)], 3: [(3, 1, 0), (3, 0)]}
