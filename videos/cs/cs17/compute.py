"""Precompute everything numerical in Part 17 of *Computer Science, Built* ("Data Structures").

    python -m videos.cs.cs17.compute              # everything missing
    python -m videos.cs.cs17.compute --force probing

Results are cached in ``.cache/cs17/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/algo/ds.py`` (hash tables, trees, heaps, union-find, tries, each counting its work) and
``explainer/cs/algo/job2.py`` (the Job v2, a hash table in the Pebble language, with a fitted model of its
instruction count and a C program that counts the same events on all thirty novels); tested in
tests/test_cs17_ds.py.  Items that time code (``cache``, ``practice``) run on this machine.

Items:
    hook       the ledger so far; where the Job v1's time goes; what a dictionary must do
    birthday   collisions: the exact probability against 1 - exp(-n^2/2m); measured on the corpus vocabulary
    chaining   chain lengths against Poisson; universal hashing; a flooding attack on a fixed hash
    probing    linear probing against Knuth's formulas; clusters; double hashing; Robin Hood's variance
    cuckoo     cuckoo hashing's failure rate against load; kicks; FKS perfect hashing
    bst        random BSTs: depth 2 ln n, the quicksort bijection; sorted input
    balanced   AVL and left-leaning red-black heights; rotations; Fibonacci trees
    randomized treaps and skip lists
    splay      splay trees on sequential, uniform and skewed access sequences; the entropy bound
    btree      B-tree height against fan-out; nodes touched per search
    heaps      Dijkstra with binary, pairing and Fibonacci heaps: comparisons and decrease-keys
    unionfind  path lengths with and without rank and compression; Ackermann and log*
    tries      a trie of the corpus vocabulary; the radix tree; a fixed rank directory with a logical packed-bit estimate
    persist    path copying: nodes copied per version
    cache      lookups timed on this machine: sorted array, std::map, std::unordered_map, open addressing
    practice   the Job natively: Python's dict, C++'s unordered_map, an open-addressing table in C
    job        the Job v2 on Pebble, its instruction model, the corpus through Part 9's caches: ledger row 8
    frontier   uniform probing against the new open-addressing bounds; dynamic optimality; open problems
"""

from __future__ import annotations

import json
import math
import random
import hashlib
import sys
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import locked_item

SCHEMAS = {name: 2 for name in ('birthday', 'probing', 'heaps', 'tries', 'cache', 'practice', 'job', 'frontier')}


class DataStructureCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not cache_current(name, self.path(name)):
            self.save(name, ITEMS[name]())
        return super().load(name)


CACHE = DataStructureCache("cs17")


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    return name not in SCHEMAS or (path.exists() and json.loads(path.read_text()).get('schema') == SCHEMAS[name])


def load(name):
    return CACHE.load(name)
P61 = (1 << 61) - 1


def _full_text():
    from videos.cs.cs16.compute import _full_text as f
    return f()


def _vocab():
    from explainer.cs.pebble import programs as PR
    words = list(PR.job_words(_full_text()))
    return words, Counter(words)


def compute_hook() -> dict:
    led = json.loads((Cache("cs16").dir / "ledger.json").read_text())
    j16 = Cache("cs16").load("job")
    return {"ledger": led, "v1_seconds": led[-1]["seconds"],
            "v1_cmp": j16["features"]["sort_cmp"], "words": j16["features"]["words"], "distinct": j16["features"]["runs"]}


def compute_birthday() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n in (10, 23, 40, 57, 70):
        e, a = D.birthday(n, 365)
        rows.append({"n": n, "exact": e, "approx": a})
    curve = [{"n": n, "p": D.birthday(n, 365)[0]} for n in range(0, 81, 2)]
    words, cnt = _vocab()
    vocab = sorted(cnt)
    # the Job v2's hash: polynomial mod a prime, then reduced to the table size; collisions among the vocabulary
    from explainer.cs.algo.job2 import P

    def h(w):
        x = 0
        for c in w:
            x = (33 * x + c) % P
        return x
    hs = [h(w) for w in vocab]
    full_counts = Counter(hs)
    full_coll = sum(c * (c - 1) // 2 for c in full_counts.values())
    m = 1 << 17
    slots = Counter(x % m for x in hs)
    n = len(vocab)
    return {"schema": SCHEMAS["birthday"], "rows": rows, "curve": curve, "distinct": n, "full_collisions": full_coll,
            "full_excess_keys": len(hs) - len(full_counts), "scope": "fixed polynomial hash observations; uniform independent hash expectation is a separate reference model",
            "expected_full": n * (n - 1) / (2 * P), "m": m, "slot_pairs": sum(c * (c - 1) // 2 for c in slots.values()),
            "expected_pairs": n * (n - 1) / (2 * m), "sqrt_m": math.sqrt(P)}


def compute_chaining() -> dict:
    from explainer.cs.algo import ds as D
    rng = random.Random(17)
    m, n = 10007, 10007
    keys = rng.sample(range(10 ** 12), n)
    lens = D.chain_lengths(keys, m, D.Universal(P61, m, rng))
    hist = Counter(lens)
    poisson = {k: m * math.exp(-1) / math.factorial(k) for k in range(0, 9)}
    # an attack on a fixed hash h(x) = x mod m: keys that are multiples of m all collide
    bad = [m * i for i in range(1, 2001)]
    fixed = D.chain_lengths(bad, m, lambda x: x % m)
    uni = D.chain_lengths(bad, m, D.Universal(P61, m, rng))
    # the universality bound, checked: over 2,000 random members, how often do two fixed keys collide?
    pair = (123456789, 987654321)
    coll = 0
    for _ in range(20000):
        h = D.Universal(10007, 100, rng)
        coll += h(pair[0] % 10007) == h(pair[1] % 10007)
    # cost of the attack: lookups of all keys, in probes, for the fixed and the universal hash
    def cost(lens_):
        return sum(L * (L + 1) // 2 for L in lens_)
    return {"m": m, "n": n, "hist": {str(k): hist.get(k, 0) for k in range(0, 9)}, "poisson": poisson,
            "max_chain": max(lens), "attack_n": len(bad), "attack_fixed_max": max(fixed),
            "attack_uni_max": max(uni), "attack_fixed_cost": cost(fixed), "attack_uni_cost": cost(uni),
            "pair_rate": coll / 20000, "bound": 1 / 100}


def compute_probing() -> dict:
    from explainer.cs.algo import ds as D
    rng = random.Random(17)
    m = 1 << 14
    rows = []
    for a in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95):
        n = int(a * m)
        keys = rng.sample(range(10 ** 12), n)
        miss_keys = rng.sample(range(10 ** 12, 2 * 10 ** 12), 3000)
        row = {"alpha": a}
        for name, cls in (("linear", D.LinearProbing), ("double", D.DoubleHashing)):
            t = cls(m, D.Universal(P61, m, rng), D.Universal(P61, m, rng))
            for k in keys:
                t.insert(k)
            hit_keys = rng.sample(keys, min(3000, n))      # uniformly over the keys, not the first inserted
            row[name + "_hit"] = sum(t.find(k) for k in hit_keys) / len(hit_keys)
            row[name + "_miss"] = sum(t.find(k) for k in miss_keys) / 3000
        # Controlled comparison: identical home addresses, key order and occupied slots.
        home = D.Universal(P61, m, rng)
        rh, t = D.RobinHood(m, home), D.LinearProbing(m, home)
        for k in keys:
            rh.insert(k)
            t.insert(k)
        d = rh.displacements()
        lp = [t.find(k) - 1 for k in keys]
        assert [x is not None for x in rh.t] == [x is not None for x in t.t]
        assert sum(d) == sum(lp)
        actual_alpha = n / m
        row.update({"n": n, "actual_alpha": actual_alpha, "same_home_hash": True,
                    "same_occupied_pattern": True, "displacement_sum": sum(d),
                    "robin_mean": 1 + sum(d) / len(d), "robin_var": float(np.var(d)), "robin_max": max(d),
                    "linear_var": float(np.var(lp)), "linear_max": max(lp), "linear_mean": 1 + sum(lp) / len(lp),
                    "knuth_hit": 0.5 * (1 + 1 / (1 - actual_alpha)),
                    "knuth_miss": 0.5 * (1 + 1 / (1 - actual_alpha) ** 2),
                    "uniform_hit": -math.log(1 - actual_alpha) / actual_alpha, "uniform_miss": 1 / (1 - actual_alpha)})
        rows.append(row)
        print(a, round(row["linear_miss"], 2), round(row["knuth_miss"], 2))
    # a picture of clustering: 64 slots, filled one key at a time to 70%
    snaps = []
    t = D.LinearProbing(64, D.Universal(P61, 64, rng))
    keys = rng.sample(range(10 ** 9), 45)
    for i, k in enumerate(keys, 1):
        t.insert(k)
        if i in (10, 20, 30, 45):
            snaps.append({"n": i, "slots": [x is not None for x in t.t], "clusters": sorted(t.clusters(), reverse=True)})
    return {"schema": SCHEMAS["probing"], "m": m, "rows": rows, "snaps": snaps, "scope": "finite seeded tables; Knuth/uniform formulas assume their respective random-hashing models; double hashing is not a uniform random permutation"}


def compute_cuckoo() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    m = 2000
    for load_ in (0.30, 0.35, 0.40, 0.45, 0.48, 0.50, 0.52, 0.55):
        fails, kicks, trials = 0, [], 40
        for tr in range(trials):
            rng = random.Random(1000 * tr + int(load_ * 100))
            c = D.Cuckoo(m, rng)
            ok = True
            for k in rng.sample(range(10 ** 12), int(2 * m * load_)):
                r = c.insert(k)
                if r is None:
                    ok = False
                    break
                kicks.append(r)
            fails += not ok
        rows.append({"load": load_, "fail": fails / trials, "mean_kicks": sum(kicks) / max(len(kicks), 1),
                     "max_kicks": max(kicks) if kicks else 0})
        print(rows[-1])
    rng = random.Random(5)
    f = [D.fks(rng.sample(range(10 ** 12), n), rng) for n in (1000, 10000, 100000)]
    return {"m": m, "rows": rows, "fks": f}


def compute_bst() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n in (100, 1000, 10000, 100000):
        depths, heights = [], []
        for r in range(5 if n < 100000 else 2):
            rng = random.Random(r)
            ks = list(range(n))
            rng.shuffle(ks)
            t = D.BST()
            for k in ks:
                t.insert(k)
            dd = t.depths()
            depths.append(sum(dd) / n)
            heights.append(max(dd))
        H = sum(1 / i for i in range(1, n + 1))
        rows.append({"n": n, "depth": sum(depths) / len(depths), "theory": 2 * (1 + 1 / n) * H - 4,
                     "height": sum(heights) / len(heights), "lg": math.log2(n), "ln": math.log(n),
                     "devroye": 4.311 * math.log(n) - 1.953 * math.log(math.log(n))})
        print(rows[-1])
    # the bijection: comparisons to build a BST from an order = quicksort's comparisons with the first pivot
    rng = random.Random(3)
    xs = [rng.random() for _ in range(2000)]
    t = D.BST()
    for x in xs:
        t.insert(x)
    def qs(v):
        """Quicksort with the first element as pivot and a stable two-way partition: comparisons."""
        total, stack = 0, [v]
        while stack:
            v = stack.pop()
            if len(v) <= 1:
                continue
            p = v[0]
            total += len(v) - 1
            stack.append([x for x in v[1:] if x < p])
            stack.append([x for x in v[1:] if x > p])
        return total
    q = qs(xs)
    # a small tree to draw
    small = [50, 30, 70, 20, 40, 60, 80, 35, 65, 45]
    sorted_t = D.BST()
    for k in range(1000):
        sorted_t.insert(k)
    return {"rows": rows, "build_cmp": t.cmp, "quick_cmp": q, "small": small, "sorted_height": sorted_t.height()}


def compute_balanced() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n in (1000, 10000, 100000):
        rng = random.Random(n)
        ks = list(range(n))
        rng.shuffle(ks)
        row = {"n": n, "lg": math.log2(n)}
        for name, cls in (("avl", D.AVL), ("llrb", D.LLRB)):
            for order, seq in (("random", ks), ("sorted", range(n))):
                t = cls()
                for k in seq:
                    t.insert(k)
                dd = t.depths()
                row[f"{name}_{order}_h"] = max(dd) + 1
                row[f"{name}_{order}_d"] = sum(dd) / n
                row[f"{name}_{order}_rot"] = t.rot / n
        rows.append(row)
        print(row)
    # Fibonacci trees: the fewest nodes an AVL tree of height h can have
    fib = [{"h": h, "min_nodes": _fib(h + 2) - 1, "bound": 1.4405 * math.log2(_fib(h + 2)) - 0.3277} for h in range(1, 16)]
    return {"rows": rows, "fib": fib}


def _fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def compute_randomized() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n in (1000, 10000, 100000):
        rng = random.Random(n)
        t = D.Treap(rng)
        for k in range(n):        # sorted input: a plain BST would be a path
            t.insert(k)
        dd = t.depths()
        sl = D.SkipList(random.Random(n + 1))
        ks = list(range(n))
        rng.shuffle(ks)
        for k in ks:
            sl.insert(k)
        q = [sl.search(rng.randrange(n)) for _ in range(3000)]
        lv = sl.levels()
        H = sum(1 / i for i in range(1, n + 1))
        rows.append({"n": n, "treap_depth": sum(dd) / n, "treap_height": max(dd), "bst_theory": 2 * (1 + 1 / n) * H - 4,
                     "skip_search": sum(q) / len(q), "skip_theory": 2 * math.log2(n), "skip_levels": max(lv),
                     "skip_pointers": sum(lv) / n})
        print(rows[-1])
    return {"rows": rows}


def compute_splay() -> dict:
    from explainer.cs.algo import ds as D
    n = 2000
    out = {}
    rng = random.Random(9)
    seqs = {
        "sequential": [k for _ in range(5) for k in range(n)],
        "uniform": [rng.randrange(n) for _ in range(5 * n)],
        "zipf": [min(int(rng.paretovariate(1.0)) - 1, n - 1) for _ in range(5 * n)],
        "hot ten": [rng.randrange(10) * 97 for _ in range(5 * n)],
    }
    for name, seq in seqs.items():
        s = D.Splay()
        ks = list(range(n))
        random.Random(1).shuffle(ks)
        for k in ks:
            s.insert(k)
        cost = [s.access(k) for k in seq]
        c = Counter(seq)
        m = len(seq)
        H = -sum(v / m * math.log2(v / m) for v in c.values())
        bal = D.AVL()
        for k in ks:
            bal.insert(k)
        bal_cost = sum(bal.search(k) for k in seq) / m
        out[name] = {"splay": sum(cost) / m, "entropy": H, "balanced": bal_cost, "distinct": len(c)}
        print(name, out[name])
    return {"n": n, "seqs": out, "lg": math.log2(n)}


def compute_btree() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    n = 200000
    ks = list(range(n))
    random.Random(4).shuffle(ks)
    for t_ in (2, 4, 16, 64, 256):
        b = D.BTree(t_)
        for k in ks:
            b.insert(k)
        rows.append({"t": t_, "height": b.height(), "nodes": b.nodes(), "log": math.log(n) / math.log(2 * t_)})
        print(rows[-1])
    # a billion keys on disk: 4 KB blocks of 8-byte keys and pointers
    fan = 4096 // 16
    return {"n": n, "rows": rows, "disk_fan": fan, "disk_height": math.ceil(math.log(1e9) / math.log(fan)),
            "bst_height": math.ceil(math.log2(1e9))}


def compute_heaps() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n, mdeg in ((2000, 5), (2000, 50), (20000, 5)):
        rng = random.Random(n + mdeg)
        adj = {i: [] for i in range(n)}
        for _ in range(n * mdeg // 2):
            a, b = rng.randrange(n), rng.randrange(n)
            w = rng.randrange(1, 1000)
            adj[a].append((b, w))
            adj[b].append((a, w))
        row = {"n": n, "m": n * mdeg // 2}
        ref = None
        for name, cls in (("binary", D.BinaryHeap), ("pairing", D.PairingHeap), ("fibonacci", D.FibHeap)):
            t0 = time.perf_counter()
            dist, h = D.dijkstra(adj, 0, cls)
            row[name] = h.cmp
            row[name + "_s"] = time.perf_counter() - t0
            ref = ref or dist
            assert dist == ref
        # decrease-keys performed
        dk = 0
        dist = {0: 0}
        done = set()
        import heapq
        pq = [(0, 0)]
        while pq:
            d, u = heapq.heappop(pq)
            if u in done:
                continue
            done.add(u)
            for v, w in adj[u]:
                if v not in done and (v not in dist or d + w < dist[v]):
                    dk += v in dist
                    dist[v] = d + w
                    heapq.heappush(pq, (d + w, v))
        assert ref == dist
        row["decrease"] = dk
        rows.append(row)
        print(row)
    return {"schema": SCHEMAS["heaps"], "rows": rows, "scope": "actual heap key comparisons on three graphs, independently checked with heapq; Python list operations do not realize theoretical pointer costs"}


def compute_unionfind() -> dict:
    from explainer.cs.algo import ds as D
    n = 20000
    rng = random.Random(2)
    pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(2 * n)]
    finds = [rng.randrange(n) for _ in range(2 * n)]
    rows = []
    for name, rank, comp in (("neither", False, False), ("rank", True, False), ("compression", False, True),
                             ("both", True, True)):
        uf = D.UnionFind(n, rank, comp)
        for a, b in pairs:
            uf.union(a, b)
        uf.steps = 0
        for x in finds:
            uf.find(x)
        rows.append({"name": name, "per_find": uf.steps / len(finds), "max_depth": uf.max_depth()})
        print(rows[-1])
    # the worst case for "neither": a chain, every node pointing to the next
    chain = D.UnionFind(10000, False, False)
    for i in range(1, 10000):
        chain.p[i - 1] = i
    ack = [{"m": m, "A(m,1)": D.ackermann(m, 1) if m < 4 else None} for m in range(5)]
    logstar = [{"n": s, "log*": D.log_star(v)} for s, v in (("2", 2), ("4", 4), ("16", 16), ("65,536", 65536))]
    logstar.append({"n": "2^65536", "log*": 1 + D.log_star(65536)})   # lg(2^65536) = 65536
    return {"n": n, "rows": rows, "chain_depth": chain.max_depth(), "ackermann": ack, "logstar": logstar}


def compute_tries() -> dict:
    from explainer.cs.algo import ds as D
    words, cnt = _vocab()
    vocab = sorted(cnt)
    t = D.Trie()
    for w in vocab:
        t.insert(w.decode())
    letters = sum(len(w) for w in vocab)
    # rank in O(1): a bit per node, the overhead of the directory
    rng = random.Random(1)
    bits = [rng.randrange(2) for _ in range(1 << 16)]
    rs = D.RankSelect(bits)
    prefix = [0]
    for b in bits:
        prefix.append(prefix[-1] + b)
    ok = all(rs.rank(i) == prefix[i] for i in range(len(bits) + 1))
    assert ok
    small = D.Trie()
    for w in ("the", "then", "there", "they", "this", "to", "tea", "ten"):
        small.insert(w)
    return {"schema": SCHEMAS["tries"], "distinct": len(vocab), "letters": letters, "trie_nodes": t.nodes, "radix_nodes": t.radix_nodes(),
            "rank_ok": ok, "rank_queries_checked": len(bits) + 1, "rank_bits": len(bits), "rank_overhead": rs.overhead_bits(),
            "scope": "fixed 512/64 rank directory; logical packed-bit estimate excludes Python objects; select not implemented; not an asymptotic o(n)-bit directory",
            "small_nodes": small.nodes, "small_radix": small.radix_nodes()}


def compute_persist() -> dict:
    from explainer.cs.algo import ds as D
    rows = []
    for n in (1000, 10000, 100000):
        rng = random.Random(n)
        ks = list(range(n))
        rng.shuffle(ks)
        p = D.PersistentBST()
        for k in ks:
            p.insert(k)
        ok = D.PersistentBST.contains(p.versions[n // 2], ks[0]) and not D.PersistentBST.contains(
            p.versions[n // 2], ks[-1])
        rows.append({"n": n, "copied_per_insert": p.copied / n, "ln": math.log(n), "ok": ok,
                     "full_copy": (n + 1) / 2})
        print(rows[-1])
    return {"rows": rows}


CACHE_CPP = r"""
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <unordered_map>
#include <vector>
using namespace std;
static double now(){return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count();}
static uint64_t checksum(const vector<uint32_t>& a){uint64_t h=14695981039346656037ULL;for(auto x:a){h^=x;h*=1099511628211ULL;}return h;}
int main(int argc,char**argv){
 if(argc!=2)return 2;char*end=nullptr;long n=strtol(argv[1],&end,10);if(*end||n<2||n>10000000)return 2;
 const long Q=2000000;mt19937_64 rng(7);vector<uint32_t>keys(n);for(auto&k:keys)k=(uint32_t)rng();keys[0]=12;keys[1]=13;
 vector<uint32_t>q(Q);for(auto&x:q)x=keys[rng()%n];q[0]=12;q[1]=13;
 // Last assignment wins identically for every container, including duplicate keys.
 unordered_map<uint32_t,uint32_t>reference;reference.reserve(n);for(long i=0;i<n;i++)reference[keys[i]]=(uint32_t)i;
 vector<uint32_t>expected(Q),out(Q);for(long i=0;i<Q;i++)expected[i]=reference.at(q[i]);uint64_t expected_hash=checksum(expected);
 vector<pair<uint32_t,uint32_t>>a; a.reserve(n);for(long i=0;i<n;i++)a.emplace_back(keys[i],i);sort(a.begin(),a.end());
 auto check=[&](){return out==expected&&checksum(out)==expected_hash;};
 double t=now();for(long i=0;i<Q;i++){auto it=upper_bound(a.begin(),a.end(),make_pair(q[i],numeric_limits<uint32_t>::max()));out[i]=prev(it)->second;}double ta=(now()-t)/Q;bool ca=check();
 map<uint32_t,uint32_t>m;for(long i=0;i<n;i++)m[keys[i]]=i;
 t=now();for(long i=0;i<Q;i++)out[i]=m.find(q[i])->second;double tm=(now()-t)/Q;bool cm=check();
 unordered_map<uint32_t,uint32_t>u;u.reserve(n);for(long i=0;i<n;i++)u[keys[i]]=i;
 t=now();for(long i=0;i<Q;i++)out[i]=u.find(q[i])->second;double tu=(now()-t)/Q;bool cu=check();
 size_t cap=1;while(cap<2*(size_t)n)cap<<=1;vector<uint32_t>ok(cap),ov(cap);vector<uint8_t>occupied(cap);
 for(long i=0;i<n;i++){uint32_t k=keys[i];size_t s=(k*2654435761u)&(cap-1);while(occupied[s]&&ok[s]!=k)s=(s+1)&(cap-1);occupied[s]=1;ok[s]=k;ov[s]=i;}
 t=now();for(long i=0;i<Q;i++){uint32_t k=q[i];size_t s=(k*2654435761u)&(cap-1);while(occupied[s]&&ok[s]!=k)s=(s+1)&(cap-1);if(!occupied[s])return 3;out[i]=ov[s];}double to=(now()-t)/Q;bool co=check();
 cout<<setprecision(17)<<"{\"n\":"<<n<<",\"unique\":"<<reference.size()<<",\"queries\":"<<Q<<",\"capacity\":"<<cap<<",\"load\":"<<(double)reference.size()/cap<<",\"checksum\":\""<<expected_hash<<"\",\"checks\":["<<ca<<","<<cm<<","<<cu<<","<<co<<"],\"nanoseconds\":["<<ta*1e9<<","<<tm*1e9<<","<<tu*1e9<<","<<to*1e9<<"]}\n";
 return !(ca&&cm&&cu&&co);
}
"""


def compute_cache() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as d:
        Path(d, "c.cpp").write_text(CACHE_CPP)
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", "c", "c.cpp"], cwd=d, check=True)
        for n in (1000, 100000, 1000000, 10000000):
            repeats = []
            for _ in range(3):
                r = json.loads(subprocess.run(["./c", str(n)], cwd=d, capture_output=True,
                                              text=True, check=True).stdout)
                assert r['n'] == n and r['checks'] == [1, 1, 1, 1]
                assert all(math.isfinite(t) and t > 0 for t in r['nanoseconds'])
                repeats.append(r)
            assert len({r['checksum'] for r in repeats}) == 1
            row = {k: repeats[0][k] for k in ('n', 'unique', 'capacity', 'load', 'queries', 'checksum')}
            row.update({name: min(r['nanoseconds'][i] for r in repeats)
                        for i, name in enumerate(('array', 'map', 'unordered', 'open'))})
            row['repeats'] = repeats
            rows.append(row)
            print(row)
    return dict(schema=SCHEMAS['cache'], rows=rows,
                gcc=subprocess.run(['g++', '--version'], capture_output=True, text=True, check=True).stdout.splitlines()[0],
                source_sha256=hashlib.sha256(CACHE_CPP.encode()).hexdigest(),
                protocol='2,000,000 seeded successful uint32 lookups; last assignment wins; keys 12/13 remain distinct; result-vector writes timed; build/query generation/full-vector verification excluded; minimum of three full-output-checked repeats; separate actual loads; one host')


JOB_CPP = r"""
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
using namespace std;
int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *f = fopen(argv[1], "rb"); if (!f || fseek(f, 0, SEEK_END)) return 2;
  long sz = ftell(f); if (sz < 0 || fseek(f, 0, SEEK_SET)) return 2;
  vector<unsigned char> t(sz); if (fread(t.data(), 1, sz, f) != (size_t)sz) return 1; fclose(f);
  auto t0 = chrono::steady_clock::now();
  unordered_map<string, pair<long, long>> m; m.reserve(1 << 17);
  string w; long ord = 0;
  for (long i = 0; i <= sz; i++) {
    int c = i < sz ? t[i] : -1;
    if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') w.push_back((char)c);
    else if (!w.empty()) { auto it = m.find(w); if (it == m.end()) m.emplace(w, make_pair(1L, ord++)); else it->second.first++; w.clear(); }
  }
  vector<tuple<long, long, string>> v; for (auto &e : m) v.emplace_back(-e.second.first, e.second.second, e.first);
  size_t shown = min<size_t>(20, v.size());
  partial_sort(v.begin(), v.begin() + shown, v.end());
  double s = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  for (size_t i = 0; i < shown; i++) fprintf(stderr, "%s %ld\n", get<2>(v[i]).c_str(), -get<0>(v[i]));
  printf("%g\n", s);
  return 0;
}
"""

JOB_OA_C = r"""
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct { uint32_t hash,start,len; uint64_t count; } Entry;
static double now(void){struct timespec ts;if(clock_gettime(CLOCK_MONOTONIC,&ts))exit(2);return ts.tv_sec+ts.tv_nsec*1e-9;}
static void* checked(void*p){if(!p)exit(2);return p;}
int main(int argc,char**argv){
 if(argc!=2)return 2;FILE*f=fopen(argv[1],"rb");if(!f)return 2;if(fseek(f,0,SEEK_END))return 2;long size=ftell(f);if(size<0||size>UINT32_MAX||fseek(f,0,SEEK_SET))return 2;
 size_t sz=(size_t)size;unsigned char*t=checked(malloc(sz+1));if(fread(t,1,sz,f)!=sz)return 2;fclose(f);
 double begin=now();size_t cap=64,allocated=16,ne=0,used=0,n=0;uint32_t*slot=checked(calloc(cap,sizeof(*slot)));Entry*entries=checked(malloc(allocated*sizeof(*entries)));unsigned char*pool=checked(malloc(sz+1)),*word=checked(malloc(sz+1));uint32_t h=2166136261u;
 for(size_t i=0;i<=sz;i++){
  int c=i<sz?t[i]:-1;if(c>='A'&&c<='Z')c+=32;
  if(c>='a'&&c<='z'){word[n++]=(unsigned char)c;h=(h^(uint32_t)c)*16777619u;continue;}
  if(!n)continue;size_t s=h&(cap-1);
  while(slot[s]){Entry*e=&entries[slot[s]-1];if(e->hash==h&&e->len==n&&!memcmp(pool+e->start,word,n)){e->count++;break;}s=(s+1)&(cap-1);}
  if(!slot[s]){
   if(ne==allocated){allocated*=2;entries=checked(realloc(entries,allocated*sizeof(*entries)));}
   if(used+n>sz||ne>=UINT32_MAX)return 3;entries[ne]=(Entry){h,(uint32_t)used,(uint32_t)n,1};memcpy(pool+used,word,n);used+=n;slot[s]=(uint32_t)++ne;
   if(2*ne>cap){cap*=2;free(slot);slot=checked(calloc(cap,sizeof(*slot)));for(size_t e=0;e<ne;e++){size_t q=entries[e].hash&(cap-1);while(slot[q])q=(q+1)&(cap-1);slot[q]=(uint32_t)(e+1);}}
  }
  n=0;h=2166136261u;
 }
 size_t selected[20],shown=0;uint64_t counts[20];for(size_t k=0;k<20;k++){uint64_t best=0;size_t at=0;for(size_t e=0;e<ne;e++)if(entries[e].count>best){best=entries[e].count;at=e;}if(!best)break;selected[shown]=at;counts[shown++]=best;entries[at].count=0;}
 double elapsed=now()-begin;
 for(size_t k=0;k<shown;k++){Entry*e=&entries[selected[k]];fwrite(pool+e->start,1,e->len,stderr);fprintf(stderr," %llu\n",(unsigned long long)counts[k]);}
 printf("%.17g\n",elapsed);free(word);free(pool);free(entries);free(slot);free(t);return 0;
}
"""


def compute_practice() -> dict:
    from explainer.cs.pebble import programs as PR
    full = _full_text()
    ref = PR.job_reference(full)
    py_repeats = []
    for _ in range(3):
        t0 = time.perf_counter()
        c = {}
        for w in PR.job_words(full):
            c[w] = c.get(w, 0) + 1
        top = sorted(c.items(), key=lambda kv: -kv[1])[:20]
        elapsed = time.perf_counter() - t0
        actual = b"".join(w + b" " + str(k).encode() + b"\n" for w, k in top)
        assert actual == ref
        py_repeats.append(elapsed)
    out = dict(schema=SCHEMAS['practice'], python=min(py_repeats), python_repeats=py_repeats)
    with tempfile.TemporaryDirectory() as d:
        Path(d, 't').write_bytes(full)
        Path(d, 'j.cpp').write_text(JOB_CPP)
        Path(d, 'o.c').write_text(JOB_OA_C)
        subprocess.run(['g++', '-O2', '-std=c++17', '-o', 'j', 'j.cpp'], cwd=d, check=True)
        subprocess.run(['gcc', '-O2', '-o', 'o', 'o.c'], cwd=d, check=True)
        for name, exe in (('unordered_map', './j'), ('open addressing', './o')):
            repeats = []
            for _ in range(5):
                r = subprocess.run([exe, 't'], cwd=d, capture_output=True, check=True)
                elapsed = float(r.stdout)
                assert math.isfinite(elapsed) and elapsed > 0 and r.stderr == ref
                repeats.append(elapsed)
            out[name] = min(repeats)
            out[name + '_repeats'] = repeats
            out[name + '_ok'] = True
    out.update(bytes=len(full), corpus_sha256=hashlib.sha256(full).hexdigest(),
               output_sha256=hashlib.sha256(ref).hexdigest(), python_version=sys.version.splitlines()[0],
               python_executable=sys.executable,
               gcc=subprocess.run(['gcc', '--version'], capture_output=True, text=True, check=True).stdout.splitlines()[0],
               cpp_sha256=hashlib.sha256(JOB_CPP.encode()).hexdigest(), c_sha256=hashlib.sha256(JOB_OA_C.encode()).hexdigest(),
               protocol='counting/allocation/top-20 selection timed; file input/output formatting/compiler startup excluded; ties by first occurrence; Python min of 3 and native min of 5, every complete output checked; one host; language/algorithm/container differ')
    print(out)
    return out


CACHE_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* The Job v2's data accesses over the whole corpus, through Part 9's hierarchy (LRU): L1 32 KB 8-way,
   L2 1 MB 16-way, L3 4 MB 16-way, 64-byte lines.  Arrays laid out one after another, sized for the corpus. */
#define P 16777213
typedef long long ll;
typedef struct { int sets, ways; unsigned long *tag; unsigned long *age; ll miss, acc; } C;
static unsigned long tick;
static C mk(int size, int ways) { C c; c.ways = ways; c.sets = size / 64 / ways; c.tag = calloc(c.sets * ways, 8);
  c.age = calloc(c.sets * ways, 8); c.miss = c.acc = 0; for (int i = 0; i < c.sets * ways; i++) c.tag[i] = ~0UL; return c; }
static int look(C *c, unsigned long line) {
  c->acc++; int s = line % c->sets; unsigned long *t = c->tag + s * c->ways, *a = c->age + s * c->ways; int v = 0;
  for (int w = 0; w < c->ways; w++) { if (t[w] == line) { a[w] = ++tick; return 1; } if (a[w] < a[v]) v = w; }
  c->miss++; t[v] = line; a[v] = ++tick; return 0;
}
static C L1, L2, L3;
static void acc(unsigned long addr) { unsigned long ln = addr / 64; if (!look(&L1, ln) && !look(&L2, ln)) look(&L3, ln); }
static unsigned long A_POOL, A_SLOT, A_START, A_LEN, A_HASH, A_COUNT;
static unsigned char *pool; static long used;
static int *slot, *estart, *elen, *ehash, *ecount; static long cap = 64, ne = 0;
static void place(long e) { acc(A_HASH + 4 * e); long i = ehash[e] % cap; acc(A_SLOT + 4 * i);
  while (slot[i]) { i++; if (i == cap) i = 0; acc(A_SLOT + 4 * i); } slot[i] = e + 1; }
static void count(int h, int n) {
  long i = h % cap; acc(A_SLOT + 4 * i);
  while (slot[i]) {
    int e = slot[i] - 1; acc(A_HASH + 4 * e);
    if (ehash[e] == h) { acc(A_LEN + 4 * e);
      if (elen[e] == n) { acc(A_START + 4 * e); int k = 0;
        while (k < n) { acc(A_POOL + estart[e] + k); acc(A_POOL + used + k); if (pool[estart[e] + k] != pool[used + k]) break; k++; }
        if (k == n) { acc(A_COUNT + 4 * e); ecount[e]++; return; } } }
    i++; if (i == cap) i = 0; acc(A_SLOT + 4 * i);
  }
  estart[ne] = used; elen[ne] = n; ehash[ne] = h; ecount[ne] = 1;
  acc(A_START + 4 * ne); acc(A_LEN + 4 * ne); acc(A_HASH + 4 * ne); acc(A_COUNT + 4 * ne); acc(A_SLOT + 4 * i);
  slot[i] = ne + 1; ne++; used += n;
  if (2 * ne > cap) { cap *= 2; memset(slot, 0, cap * 4); for (long s = 0; s < cap; s++) acc(A_SLOT + 4 * s);
    for (long e = 0; e < ne; e++) place(e); }
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *t = malloc(sz); if (fread(t, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  long ES = 1 << 17, SS = 1 << 18, PS = 1 << 20;
  pool = malloc(PS); slot = calloc(SS, 4); estart = malloc(4 * ES); elen = malloc(4 * ES); ehash = malloc(4 * ES); ecount = malloc(4 * ES);
  A_POOL = 1 << 16; A_SLOT = A_POOL + PS; A_START = A_SLOT + 4 * SS; A_LEN = A_START + 4 * ES; A_HASH = A_LEN + 4 * ES; A_COUNT = A_HASH + 4 * ES;
  L1 = mk(32 << 10, 8); L2 = mk(1 << 20, 16); L3 = mk(4 << 20, 16);
  int n = 0, h = 0;
  for (long i = 0; i < sz; i++) {
    int c = t[i]; if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') { pool[used + n] = c; acc(A_POOL + used + n); n++; h = (int)((33LL * h + c) % P); }
    else if (n > 0) { count(h, n); n = 0; h = 0; }
  }
  if (n > 0) count(h, n);
  for (int k = 0; k < 20; k++) for (long e = 0; e < ne; e++) acc(A_COUNT + 4 * e);
  printf("%lld %lld %lld %lld %ld\n", L1.acc, L1.miss, L2.miss, L3.miss, ne);
  return 0;
}
"""


def _passages(n=48, lo=60, hi=90000, seed=17):
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs6.compute import novels
    books = novels()
    keys = sorted(books)
    rng = np.random.default_rng(seed)
    out = []
    for L in np.geomspace(lo, hi, n).astype(int):
        b = books[keys[int(rng.integers(len(keys)))]]
        o = int(rng.integers(0, len(b) - L))
        out.append(PR.job_tape(b[o:o + L]))
    return out


def compute_job() -> dict:
    """Project full-corpus costs from checked samples of one corpus-sized image and a partial cache model."""
    from explainer.cs.algo import job2 as J
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs8.compute import core
    from videos.cs.cs9.compute import pebble_hierarchy
    full = _full_text()
    vocab = set(PR.job_words(full))
    unique_letters = sum(map(len, vocab))
    max_word = max(map(len, vocab), default=0)
    distinct_capacity = len(vocab) + 1
    slot_capacity = 1 << (2 * distinct_capacity - 1).bit_length()
    capacities = dict(letter_capacity=unique_letters + max_word + 1,
                      distinct_capacity=distinct_capacity, slot_capacity=slot_capacity)
    source = J.job_source(**capacities)
    c = J.compile_job(**capacities)
    memory_bytes = 1 << (len(c.program.image) + (1 << 20) - 1).bit_length()
    assert len(c.program.image) < memory_bytes < 2 ** 31
    tapes = _passages()
    samples = []
    emulator_samples = []
    for t in tapes:
        m = J.run(c, t, mem_size=memory_bytes)
        assert bytes(m.output) == PR.job_reference(t)
        features = J.features(t)
        native_features, native_out = J.features_native(t)
        assert native_features == features and native_out == bytes(m.output)
        samples.append((features, m.steps))
        emulator_samples.append(dict(bytes=len(t), steps=m.steps, features=features,
                                     tape_sha256=hashlib.sha256(t).hexdigest(),
                                     output_sha256=hashlib.sha256(bytes(m.output)).hexdigest()))
    held_idx = [i for i in range(len(samples)) if i % 4 == 2]
    train = [s for i, s in enumerate(samples) if i not in held_idx]
    model = J.fit(train)
    matrix = np.array([[1] + [f[k] for k in model['names'][1:]] for f, _ in train], dtype=float)
    singular = np.linalg.svd(matrix, compute_uv=False)
    model.update(rank=int(np.linalg.matrix_rank(matrix)), columns=matrix.shape[1],
                 singular_values=singular.tolist(), condition_number=float(singular[0] / singular[-1]),
                 decomposition_scope='correlated least-squares terms; nonunique category attribution, not measured causal costs')
    assert all(math.isfinite(v) for v in model['coef'])
    held = [{"bytes": samples[i][0]["bytes"], "steps": samples[i][1], "predicted": J.predict(model, samples[i][0])}
            for i in held_idx]
    held_err = max(abs(h["predicted"] - h["steps"]) / h["steps"] for h in held)
    full = _full_text()
    ff, out = J.features_native(full)
    assert out == PR.job_reference(full)
    instr = J.predict(model, ff)
    assert instr > 0 and math.isfinite(instr)
    # where the instructions go, from the model's own terms
    coef = dict(zip(model["names"], model["coef"]))
    parts = {
        "reading and hashing the text": sum(coef[k] * ff[k] for k in ("bytes", "capitals", "letters", "above_z", "between")),
        "probing the table": sum(coef[k] * ff[k] for k in ("words", "probes", "hash_eq", "len_eq", "found", "wraps",
                                                           "count_loops", "new")),
        "comparing letters": coef["k_steps"] * ff["k_steps"],
        "growing the table": sum(coef[k] * ff[k] for k in ("grows", "cleared", "placed", "place_probes", "place_wraps",
                                                           "place_loops")),
        "the report": sum(coef[k] * ff[k] for k in ("rep_iter", "rep_gt", "printed", "digits", "shown", "rep_stop")),
    }
    # IPC on the out-of-order core, on passages of 1-3 kB (as rows 3, 5 and 7 were priced)
    from videos.cs.cs13.compute import _tapes
    cyc = ins = 0
    ipc_samples = []
    for t in _tapes(6, 1200, 2600)[:3]:
        q = core(c.program.image, t, mem_size=memory_bytes)
        assert bytes(q.output) == PR.job_reference(t)
        cyc += q.cycles
        ins += q.committed
        ipc_samples.append(dict(bytes=len(t), cycles=q.cycles, committed=q.committed,
                                tape_sha256=hashlib.sha256(t).hexdigest(),
                                output_sha256=hashlib.sha256(bytes(q.output)).hexdigest()))
    ipc = ins / cyc
    # memory: the corpus run through Part 9's hierarchy
    lat = pebble_hierarchy()[1]      # cumulative cycles: L1, L2, L3, DRAM
    with tempfile.TemporaryDirectory() as d:
        Path(d, "m.c").write_text(CACHE_C)
        subprocess.run(["gcc", "-O2", "-o", "m", "m.c"], cwd=d, check=True)
        Path(d, "t").write_bytes(full)
        accs, m1, m2, m3, ne = map(int, subprocess.run(["./m", "t"], cwd=d, capture_output=True, text=True,
                                                       check=True).stdout.split())
    stall = m1 * (lat[1] - lat[0]) + m2 * (lat[2] - lat[1]) + m3 * (lat[3] - lat[2])
    led = json.loads((Cache("cs16").dir / "ledger.json").read_text())[:8]
    row7 = led[7]
    cycles = instr / ipc + stall
    seconds = cycles / (row7["clock_mhz"] * 1e6)
    led.append({"part": 17, "label": r"a hash table", "seconds": seconds, "cycles": cycles,
                "clock_mhz": row7["clock_mhz"], "instructions": instr, "ipc": ipc, "stall_cycles": stall,
                "memory_bytes": memory_bytes, "scope": "full native event counts + fitted instructions + sampled IPC + assumed cache trace; unexecuted additive projection"})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    probes_per_word = (ff["probes"] + ff["new"]) / ff["words"]
    return {"schema": SCHEMAS["job"], "model": model, "held": held, "held_err": held_err, "train_err": model["max_rel_err"],
            "n_train": len(train), "n_held": len(held), "n_features": len(model["names"]) - 1,
            "features": ff, "instructions": instr, "ipc": ipc, "parts": parts, "seconds": seconds, "ledger": led,
            "memory": {"accesses": accs, "L1_miss": m1, "L2_miss": m2, "L3_miss": m3, "latencies": lat,
                       "stall_cycles": stall, "stall_share": stall / cycles},
            "probes_per_word": probes_per_word, "final_cap": 64 * 2 ** ff["grows"],
            "speedup_vs_row7": row7["seconds"] / seconds, "speedup_vs_row5": led[5]["seconds"] / seconds,
            "speedup_vs_row4": led[4]["seconds"] / seconds, "hardware_gain": led[0]["seconds"] / led[4]["seconds"],
            "algorithm_gain": led[5]["seconds"] / seconds, "v1_instructions": row7["instructions"],
            "source": source.strip().splitlines(), "capacities": capacities, "memory_bytes": memory_bytes,
            "image_bytes": len(c.program.image), "image_sha256": hashlib.sha256(c.program.image).hexdigest(),
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(), "emulator_samples": emulator_samples,
            "ipc_samples": ipc_samples, "corpus_sha256": hashlib.sha256(full).hexdigest(),
            "corpus_output_sha256": hashlib.sha256(out).hexdigest(),
            "full_exceeds_training_max": [k for k in model['names'][1:] if ff[k] > max(f[k] for f, _ in train)],
            "scope": "48 finite emulator samples, 12 held out; full corpus event counts checked by native output; instructions/time not full execution; category shares nonunique; cache trace is partial assumed layout, not compiled execution; additive miss penalties may double count stalls and omit overlap"}


def compute_frontier() -> dict:
    from .measurements import uniform_probe_experiment
    return dict(schema=SCHEMAS['frontier'], **uniform_probe_experiment())


ITEMS = {
    "hook": compute_hook, "birthday": compute_birthday, "chaining": compute_chaining, "probing": compute_probing,
    "cuckoo": compute_cuckoo, "bst": compute_bst, "balanced": compute_balanced, "randomized": compute_randomized,
    "splay": compute_splay, "btree": compute_btree, "heaps": compute_heaps, "unionfind": compute_unionfind,
    "tries": compute_tries, "persist": compute_persist, "cache": compute_cache, "practice": compute_practice,
    "job": compute_job, "frontier": compute_frontier,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
