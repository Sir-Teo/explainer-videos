"""Replica-level instruments for Part 39: last-writer-wins against version vectors, Merkle-tree anti-entropy,
a sequence CRDT (RGA) against naive positional replay, and hot keys on hash partitions."""

from __future__ import annotations

import hashlib
import random


# ---------------------------------------------------------------- last writer wins, and what it loses

def lww_pairs(skews_ms=(0, 10, 50, 100, 250), delta_ms: float = 50.0, rate: float = 5.0, seconds: float = 2000.0,
              seed: int = 0):
    """Two leaders (regions A and B) accept writes to one key, each a Poisson stream of ``rate`` per second; a write
    reaches the other region ``delta_ms`` later.  B's clock runs ``skew`` ms ahead.  For every write, look at the
    latest earlier write from the *other* region: if it arrived first (gap > delta) the new write saw it, and
    last-writer-wins must keep the new one; if not, the two are concurrent.  Count, as fractions of all writes,
    concurrent pairs (silently resolved by LWW; reported as siblings by version vectors) and causal inversions
    (the newer write, which had seen the older, is discarded because the older carries a larger timestamp)."""
    rng = random.Random(seed)
    ev = []
    for reg in "AB":
        t = 0.0
        while True:
            t += rng.expovariate(rate) * 1000.0
            if t > seconds * 1000.0:
                break
            ev.append((t, reg))
    ev.sort()
    out = []
    for skew in skews_ms:
        conc = inv = cross = 0
        last = {"A": None, "B": None}
        for t, reg in ev:
            other = "B" if reg == "A" else "A"
            p = last[other]
            if p is not None and (last[reg] is None or p > last[reg]):
                cross += 1
                gap = t - p
                if gap <= delta_ms:
                    conc += 1
                else:
                    ts_new = t + (skew if reg == "B" else 0.0)
                    ts_old = p + (skew if other == "B" else 0.0)
                    if ts_new < ts_old:
                        inv += 1
            last[reg] = t
        n = len(ev)
        out.append({"skew_ms": skew, "writes": n, "concurrent": conc / n, "inversions": inv / n,
                    "lww_lost": (conc / 2 + inv) / n, "vv_lost": 0.0})
    return out


# ---------------------------------------------------------------- Merkle trees for anti-entropy

def _hh(b: bytes) -> bytes:
    return hashlib.blake2b(b, digest_size=16).digest()


def _tree(values: list[bytes], fanout: int, leaf: int):
    """Levels of hashes, leaves first: level 0 hashes ``leaf`` consecutive keys' values."""
    lv = [[_hh(b"".join(values[i:i + leaf])) for i in range(0, len(values), leaf)]]
    while len(lv[-1]) > 1:
        cur = lv[-1]
        lv.append([_hh(b"".join(cur[i:i + fanout])) for i in range(0, len(cur), fanout)])
    return lv


def merkle_sync(keys: int = 1 << 20, diffs=(0, 1, 10, 100, 1000, 10000), fanout: int = 16, leaf: int = 16,
                hash_bytes: int = 16, key_bytes: int = 8, seed: int = 0):
    """Two replicas of ``keys`` keys differ in ``d`` random keys.  Walk both Merkle trees from the root, exchanging
    only the children of nodes whose hashes differ; at the leaves, exchange the leaf's keys.  Against: send one hash
    per key.  Returns bytes and round trips for each d, and checks that every differing key was found."""
    if keys <= 0 or fanout < 2 or leaf <= 0 or any(not 0 <= d <= keys for d in diffs):
        raise ValueError("need positive keys/leaf size, fanout >= 2, and differences within the key count")
    rng = random.Random(seed)
    base = [i.to_bytes(8, "little") + rng.randbytes(8) for i in range(keys)]
    ta = _tree(base, fanout, leaf)
    out = []
    for d in diffs:
        idx = set(rng.sample(range(keys), d)) if d else set()
        other = list(base)
        for i in idx:
            other[i] = i.to_bytes(8, "little") + rng.randbytes(8)
        tb = _tree(other, fanout, leaf)
        top = len(ta) - 1
        frontier = [0]
        sent = hash_bytes
        rounds = 1
        level = top
        if ta[top][0] == tb[top][0]:
            frontier = []
        while frontier and level > 0:
            level -= 1
            nxt = []
            for j in frontier:
                kids = range(j * fanout, min((j + 1) * fanout, len(ta[level])))
                sent += hash_bytes * len(kids)
                nxt += [k for k in kids if ta[level][k] != tb[level][k]]
            frontier = nxt
            rounds += 1
        found = set()
        for j in frontier:
            lo, hi = j * leaf, min((j + 1) * leaf, keys)
            sent += (hi - lo) * (key_bytes + hash_bytes)
            found |= {i for i in range(lo, hi) if base[i] != other[i]}
        if frontier:
            rounds += 1
        out.append({"diffs": d, "merkle_bytes": sent, "rounds": rounds, "naive_bytes": keys * hash_bytes,
                    "found_all": found == idx})
    return {"rows": out, "keys": keys, "fanout": fanout, "leaf": leaf, "depth": len(ta)}


# ---------------------------------------------------------------- a sequence CRDT: RGA

class Rga:
    """Replicated Growable Array (Roh et al. 2011).  Every element has a unique id (counter, replica); an insert names
    the id it goes after; among elements inserted after the same id, the larger id comes first.  Deletes leave a
    tombstone.  Operations commute once each insert's reference has arrived (causal delivery)."""

    def __init__(self, rid: int):
        self.rid, self.clock = rid, 0
        self.after: dict = {None: []}      # id -> children ids, sorted descending
        self.char: dict = {}
        self.dead: set = set()
        self.seen: set = set()

    def ids(self):
        out, stack = [], list(self.after[None])
        while stack:
            i = stack.pop(0)
            out.append(i)
            stack[0:0] = self.after.get(i, [])
        return out

    def text(self):
        return "".join(self.char[i] for i in self.ids() if i not in self.dead)

    def local_insert(self, pos: int, ch: str):
        vis = [i for i in self.ids() if i not in self.dead]
        ref = vis[pos - 1] if pos > 0 else None
        self.clock += 1
        op = ("ins", (self.clock, self.rid), ref, ch)
        self.apply(op)
        return op

    def local_delete(self, pos: int):
        vis = [i for i in self.ids() if i not in self.dead]
        op = ("del", vis[pos])
        self.apply(op)
        return op

    def ready(self, op) -> bool:
        return op[0] == "del" and op[1] in self.char or op[0] == "ins" and (op[2] is None or op[2] in self.char)

    def apply(self, op):
        if op[0] == "ins":
            _, i, ref, ch = op
            if i in self.char:
                return
            self.clock = max(self.clock, i[0])
            self.char[i] = ch
            self.after.setdefault(i, [])
            kids = self.after[ref]
            kids.append(i)
            kids.sort(reverse=True)
        else:
            self.dead.add(op[1])


class NaiveText:
    """Replays remote edits by position, as if no one else were typing."""

    def __init__(self):
        self.s = ""

    def local_insert(self, pos, ch):
        self.s = self.s[:pos] + ch + self.s[pos:]
        return ("ins", pos, ch)

    def local_delete(self, pos):
        self.s = self.s[:pos] + self.s[pos + 1:]
        return ("del", pos)

    def apply(self, op):
        if op[0] == "ins":
            pos = min(op[1], len(self.s))
            self.s = self.s[:pos] + op[2] + self.s[pos:]
        elif len(self.s):
            pos = min(op[1], len(self.s) - 1)
            self.s = self.s[:pos] + self.s[pos + 1:]

    def text(self):
        return self.s


def edit_session(kind: str, users: int = 3, ops: int = 30, seed: int = 0, start: str = "the cat sat"):
    """``users`` replicas start from ``start``; each makes local edits and the operations are delivered to the
    others in random (causally ready) order.  Returns whether all replicas end with the same text."""
    rng = random.Random(seed)
    if kind == "rga":
        reps = [Rga(r) for r in range(users)]
        init = []
        for k, ch in enumerate(start):
            init.append(reps[0].local_insert(k, ch))
        for r in reps[1:]:
            for op in init:
                r.apply(op)
        for r in reps:
            r.clock = max(r.clock, len(start))
    else:
        reps = [NaiveText() for _ in range(users)]
        for r in reps:
            r.s = start
    inbox = [[] for _ in range(users)]
    for _ in range(ops):
        u = rng.randrange(users)
        r = reps[u]
        n = len(r.text())
        if n and rng.random() < 0.3:
            op = r.local_delete(rng.randrange(n))
        else:
            op = r.local_insert(rng.randrange(n + 1), rng.choice("abcdefghijklmnopqrstuvwxyz"))
        for v in range(users):
            if v != u:
                inbox[v].append(op)
        if rng.random() < 0.4:
            v = rng.randrange(users)
            _deliver(reps[v], inbox[v], rng, kind, some=True)
    for v in range(users):
        _deliver(reps[v], inbox[v], rng, kind, some=False)
    texts = [r.text() for r in reps]
    return {"converged": len(set(texts)) == 1, "texts": texts}


def _deliver(rep, box, rng, kind, some):
    k = rng.randrange(1, len(box) + 1) if (some and box) else len(box)
    for _ in range(k):
        if not box:
            break
        cand = [j for j, op in enumerate(box) if kind != "rga" or rep.ready(op)]
        j = rng.choice(cand)
        rep.apply(box.pop(j))


def rga_demo():
    """Two people edit "the cat sat" at once: one types "fat " before "cat", the other replaces "sat" by "ran".
    Both replicas receive the other's edits afterwards; RGA and positional replay compared."""
    out = {}
    for kind in ("rga", "naive"):
        if kind == "rga":
            a, b = Rga(1), Rga(2)
            init = [a.local_insert(k, ch) for k, ch in enumerate("the cat sat")]
            for op in init:
                b.apply(op)
            b.clock = a.clock
        else:
            a, b = NaiveText(), NaiveText()
            a.s = b.s = "the cat sat"
        oa = [a.local_insert(4 + k, ch) for k, ch in enumerate("fat ")]
        ob = [b.local_delete(8) for _ in range(3)]
        ob += [b.local_insert(8 + k, ch) for k, ch in enumerate("ran")]
        mid = {"a": a.text(), "b": b.text()}
        for op in ob:
            a.apply(op)
        for op in oa:
            b.apply(op)
        out[kind] = {"a_local": mid["a"], "b_local": mid["b"], "a": a.text(), "b": b.text()}
    return out


# ---------------------------------------------------------------- hot keys

def hot_shards(shards: int = 100, keys: int = 1_000_000, requests: int = 2_000_000, zipf_s=(0.0, 0.8, 1.0, 1.2),
               salt_top: int = 10, salt_ways: int = 20, seed: int = 0):
    """Requests choose keys with Zipf(s) popularity (s = 0 is uniform); keys are hashed to shards.  The busiest
    shard's load against the mean, and the share of the single hottest key; then the same with the ``salt_top``
    hottest keys each split ``salt_ways`` ways (a random suffix per request, merged on read)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    home = rng.integers(0, shards, size=keys)
    out = []
    for s in zipf_s:
        w = 1.0 / np.arange(1, keys + 1) ** s
        w /= w.sum()
        cnt = rng.multinomial(requests, w)
        load = np.bincount(home, weights=cnt, minlength=shards)
        row = {"s": s, "top_key_share": float(w[0]), "max_over_mean": float(load.max() / load.mean())}
        load2 = load.copy()
        for k in range(salt_top):
            load2[home[k]] -= cnt[k]
            parts = rng.multinomial(cnt[k], [1 / salt_ways] * salt_ways)
            dest = rng.integers(0, shards, size=salt_ways)
            np.add.at(load2, dest, parts)
        row["salted_max_over_mean"] = float(load2.max() / load2.mean())
        out.append(row)
    return {"rows": out, "shards": shards, "keys": keys, "salt_top": salt_top, "salt_ways": salt_ways}


def rga_overhead(edits: int = 20000, p_delete: float = 0.45, checkpoints=(1000, 5000, 10000, 20000), seed: int = 0,
                 id_bytes: int = 12):
    """One RGA document edited ``edits`` times (inserts at random places, a fraction of deletions).  At each
    checkpoint: visible characters, tombstones kept, and metadata bytes per visible character (each element keeps
    its id and its reference's id, ``id_bytes`` each) against one byte per character for plain text."""
    rng = random.Random(seed)
    r = Rga(1)
    out = []
    vis = 0
    for e in range(1, edits + 1):
        if vis and rng.random() < p_delete:
            r.local_delete(rng.randrange(vis))
            vis -= 1
        else:
            r.local_insert(rng.randrange(vis + 1), "x")
            vis += 1
        if e in checkpoints:
            total = len(r.char)
            out.append({"edits": e, "visible": vis, "tombstones": total - vis,
                        "bytes_per_char": total * (2 * id_bytes + 1) / max(1, vis)})
    return out
