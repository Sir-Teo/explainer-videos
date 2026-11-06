"""Programmable data planes and their verification (Part 36's frontier).

    Pipeline: a P4-shaped switch: a parser that extracts header fields from bytes, a sequence of match-action
        tables (exact, ternary or longest-prefix keys; actions set fields, choose a port, drop, or count), and a
        deparser.  ``process(packet bytes) -> (port or None, new bytes, trace)``
    verify(fib, hosts)  data-plane verification in the spirit of header space analysis: for every destination
        prefix, follow every router's forwarding rule as a graph and report loops and black holes, without
        sending a packet
"""
from __future__ import annotations

from explainer.cs.net.ip import Prefix


class Pipeline:
    def __init__(self, header: list[tuple[str, int]]):
        self.header = header           # [(field, bytes)]
        self.tables: list = []
        self.counters: dict = {}

    def table(self, name: str, key: str, kind: str = "exact"):
        t = {"name": name, "key": key, "kind": kind, "rules": [], "default": ("noop",)}
        self.tables.append(t)
        return t

    def parse(self, data: bytes) -> dict:
        f, i = {}, 0
        for name, n in self.header:
            f[name] = int.from_bytes(data[i:i + n], "big")
            i += n
        f["_payload"] = data[i:]
        return f

    def deparse(self, f: dict) -> bytes:
        return b"".join(f[name].to_bytes(n, "big") for name, n in self.header) + f["_payload"]

    def _match(self, t, v):
        best = None
        for rule in t["rules"]:
            k, action = rule
            if t["kind"] == "exact" and k == v:
                return action
            if t["kind"] == "ternary" and (v & k[1]) == k[0]:
                return action
            if t["kind"] == "lpm" and k.contains(v) and (best is None or k.len > best[0].len):
                best = (k, action)
        if best:
            return best[1]
        return t["default"]

    def process(self, data: bytes):
        f = self.parse(data)
        port, trace = None, []
        for t in self.tables:
            act = self._match(t, f[t["key"]])
            trace.append((t["name"], act))
            op = act[0]
            if op == "drop":
                return None, None, trace
            if op == "forward":
                port = act[1]
            elif op == "set":
                f[act[1]] = act[2]
            elif op == "dec":
                f[act[1]] -= 1
                if f[act[1]] <= 0:
                    return None, None, trace + [("ttl", "expired")]
            elif op == "count":
                self.counters[act[1]] = self.counters.get(act[1], 0) + 1
        return port, self.deparse(f), trace


def verify(fib: dict, owners: dict) -> dict:
    """fib: router -> [(Prefix, next hop)]; owners: Prefix -> router that delivers it locally (next hop is a
    host).  For every prefix, from every router, follow next hops by longest-prefix match on that prefix's
    first address, and classify: delivered, loop, or black hole.  Exhaustive over prefixes, not packets."""
    def nh(r, p: Prefix):
        best, bl = None, -1
        for q, hop in fib.get(r, []):
            if q.len <= p.len and q.contains(p.net) and q.len > bl:
                best, bl = hop, q.len
        return best
    loops, holes = [], []
    for p, owner in owners.items():
        for r in fib:
            seen, x = [], r
            while True:
                if x == owner:
                    break
                if x in seen:
                    loops.append((p, seen[seen.index(x):] + [x]))
                    break
                seen.append(x)
                hop = nh(x, p)
                if hop is None or hop not in fib:
                    if hop is None:
                        holes.append((p, x))
                    break
                x = hop
    uniq_loops = {(repr(p), tuple(sorted(set(c)))) for p, c in loops}
    return {"checked": len(owners) * len(fib), "loops": sorted(uniq_loops), "black_holes": len(holes)}
