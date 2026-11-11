"""Precompute everything numerical in Part 24 of *Computer Science, Built* ("Algorithms in Practice").

    python -m videos.cs.cs24.compute              # everything missing
    python -m videos.cs.cs24.compute --force layouts

Results are cached in ``.cache/cs24/<name>.json``; scenes call ``load(name)``.  The instrument for the data
structures is ``explainer/cs/algo/practice.py`` (tested in tests/test_cs24_practice.py); everything that depends on
the machine is a C or C++ program below. Exact sources, compiler flags/version, binaries, disassembly and all native
clock reads are retained with each schema-2 payload. Displayed native summaries are minima of fixed repetitions,
with complete semantic checks outside timers; benchmark spread uses matched first versus later-median statistics.
Full-output buffers and the timestamp store are part of this revised measurement harness. This shared host is not a
controlled hardware-counter experiment; measured speedups do not identify their microarchitectural cause.

Items:
    hook      the same O(n) sum over an array and over a shuffled linked list
    prefix    prefix sums, difference arrays and an integral image, drawn
    fenwick   responsibility ranges and paths; nodes touched against n; four structures timed in C
    segtree   covering nodes of a range query; lazy range updates against touching every element
    rmq       a sparse table, LCA by Euler tour and by binary lifting, the Cartesian tree
    monotone  the sliding-window maximum's deque, next greater element, the largest rectangle
    search    binary search on the answer; galloping against binary search
    bits      popcount, Gray codes, submasks (3^n); bitset closure and bit-parallel LCS in C
    split     meet in the middle; square-root blocks; Mo's order
    layouts   sorted, branchless, Eytzinger and B-tree search layouts, timed from 1 K to 64 M keys
    simd      scalar against AVX2 word finding; unordered_map, linear probing and a Swiss-style table
    sorting   std::sort against LSD radix sort, from 16 to 16 M keys
    bench     run-to-run spread, the first run's warm-up, environment size, dead-code elimination
    job       the Job engineered natively against Part 17's open-addressing C: ledger row 10
    branches  a predictable and an unpredictable branch, and the branch-free version
    vector    three loops at -O1 and at -O3 -march=native
    topk      the top 20 of 16 M keys: sort, partial_sort, nth_element and a heap
    pairs     a worked example: brute force, two pointers, and a stress test
    frontier  a learned index over the corpus's word offsets; ski rental with predictions
"""

from __future__ import annotations

import json
import argparse
import functools
import hashlib
import os
import math
import random
import re
import statistics
import subprocess
import tempfile
import time
from collections import deque
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.algo import practice as P
from explainer.cache_lock import cache_lock, locked_item
from . import measurement_references as R

SOURCE_FILES = (Path(__file__), Path(P.__file__), Path(R.__file__),
                Path('videos/cs/cs17/compute.py'), Path('explainer/cs/pebble/programs.py'),
                Path('videos/cs/cs16/compute.py'))


def source_signature():
    return {str(p): R.file_hash(p) for p in SOURCE_FILES}


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    if not path.exists(): return False
    try: data = json.loads(path.read_text())
    except (ValueError,OSError): return False
    if name=='ledger':
        job=CACHE.path('job')
        return (cache_current('job',job) and data==json.loads(job.read_text()).get('ledger'))
    return isinstance(data,dict) and data.get('schema') == 2 and data.get('source_sha256') == source_signature()


class PracticeCache(Cache):
    @locked_item(lambda self,name:self.path(name))
    def load(self,name):
        if not cache_current(name,self.path(name)): self.save(name,ITEMS[name]())
        return super().load(name)

    def main(self,items,doc=None):
        parser=argparse.ArgumentParser(description=doc)
        parser.add_argument('names',nargs='*',default=list(items));parser.add_argument('--force',action='store_true')
        args=parser.parse_args();self.items=items
        if any(n not in items for n in args.names):parser.error('unknown producer')
        for name in args.names:
            with cache_lock(self.path(name)):
                if not args.force and cache_current(name):print('  cached ',name,flush=True);continue
                print('  compute',name,'...',flush=True);self.save(name,items[name]());print('  done   ',name,flush=True)


CACHE = PracticeCache('cs24')
load = CACHE.load
_AUDIT = None


def _native(d,exe,*args,env=None,text=True):
    return _AUDIT.run(d,exe,*args,env=env,text=text)


def _producer(name,fn):
    @functools.wraps(fn)
    def run():
        global _AUDIT
        assert _AUDIT is None
        sources=source_signature();root=CACHE.dir/'native'/(name+'-'+R.digest(sources)[:20])
        _AUDIT=R.NativeAudit(root)
        try:
            data=fn();checks=R.verify_illustrations(name,data,P)
            assert sources==source_signature()
            receipt=_AUDIT.receipt();receipt['decoded_intervals']=R.decode_timings(receipt)
            data.update(schema=2,source_sha256=sources,independent_checks=checks,native_audit=receipt)
            return data
        finally:_AUDIT=None
    return run


def _corpus() -> bytes:
    from videos.cs.cs16.compute import _full_text
    return _full_text()


def _build(d, name, code, cc="gcc", flags=("-O2",), libs=()):
    return _AUDIT.build(d,name,code,cc=cc,flags=flags,libs=libs)



def _run(d, exe, *args, env=None):
    return _native(d,exe,*args,env=env).stdout.split()



def _cpu():
    for ln in Path("/proc/cpuinfo").read_text().splitlines():
        if ln.startswith("model name"):
            return ln.split(":", 1)[1].strip()
    return "unknown"


def _measure(function,repeats=3):
    outputs=[];samples=[]
    for _ in range(repeats):
        start=time.perf_counter();output=function();samples.append(time.perf_counter()-start);outputs.append(output)
    hashes=[R.digest(out) for out in outputs];assert len(set(hashes))==1
    return outputs[0],min(samples),dict(samples_seconds=samples,statistic='minimum',output_sha256=hashes,validation='outside timed interval')


def compute_hook() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "hook", HOOK_C)
        for logn in range(10, 25, 2):
            k, arr, lst, ok = _run(d, exe, logn)
            assert ok == "1"
            rows.append({"logn": logn, "n": 1 << logn, "array_ns": float(arr), "list_ns": float(lst),
                         "ratio": float(lst) / float(arr)})
    return {"rows": rows, "cpu": _cpu(),
            "gcc": subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]}


def compute_prefix() -> dict:
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]
    S = P.prefix_sums(a)
    ups = [(2, 9, 3), (5, 12, 2), (0, 4, 1)]
    diff = [0] * 17
    for l, r, v in ups:
        diff[l] += v
        diff[r + 1] -= v
    rng = random.Random(3)
    img = [[rng.randint(0, 9) for _ in range(8)] for _ in range(6)]
    I = P.integral_image(img)
    box = (1, 2, 4, 6)
    return {"a": a, "S": S, "query": [3, 10], "query_sum": P.range_sum(S, 3, 10), "updates": ups, "diff": diff[:16],
            "after": P.diff_apply(16, ups), "img": img, "I": I, "box": box, "box_sum": P.box_sum(I, *box),
            "box_brute": sum(img[r][c] for r in range(box[0], box[2] + 1) for c in range(box[1], box[3] + 1))}


def compute_fenwick() -> dict:
    n = 16
    resp = {i: P.Fenwick.responsibility(i) for i in range(1, n + 1)}
    F = P.Fenwick(n)
    up = F.add(5, 1)
    F.prefix(13)
    q = F.last_path
    rng = random.Random(4)
    scale = []
    for k in range(4, 21, 2):
        m = 1 << k
        F = P.Fenwick(m)
        ops = 2000
        values=np.zeros(m+1,dtype=np.int64);trace=[]
        for _ in range(ops):
            if rng.random() < 0.5:
                i=rng.randint(1,m);F.add(i,1);values[i]+=1;trace.append(['add',i,1])
            else:
                i=rng.randint(1,m);answer=F.prefix(i);assert answer==int(values[:i+1].sum());trace.append(['prefix',i,answer])
        prefix=np.cumsum(values);indices=np.arange(1,m+1);lowbits=indices&-indices
        expected=prefix[indices]-prefix[indices-lowbits]
        assert np.array_equal(np.asarray(F.t[1:]),expected)
        scale.append({"k": k, "n": m, "touched": F.touched / ops,"validated_cells":m,"operation_sha256":R.digest(trace),"seed":4})
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "ranges", RANGES_C)
        observations=[_run(d,exe) for _ in range(3)]
        assert all(row[4:]==['1','1'] for row in observations)
        plain,prefix,fen,seg=[min(float(row[j]) for row in observations) for j in range(4)]
    timing = {"plain_ns": float(plain), "prefix_ns": float(prefix), "fenwick_ns": float(fen), "segtree_ns": float(seg),
              "n": 1 << 20, "plain_operations":1<<10,"prefix_operations":1<<10,"fenwick_operations":1<<20,"segtree_operations":1<<20}
    return {"n": n, "resp": {str(k): v for k, v in resp.items()}, "update_path": up, "query_path": q,
            "scale": scale, "timing": timing}


def compute_segtree() -> dict:
    a = [5, 8, 6, 3, 2, 7, 2, 6, 7, 1, 9, 4, 3, 5, 8, 1]
    T = P.SegTree(a, min, 10 ** 9)
    cov = []
    T.visits = 0
    val = T.query(3, 12, cov)
    rng = random.Random(5)
    rows = []
    for k in range(4, 17, 2):
        m = 1 << k
        L = P.LazySegTree([0] * m)
        L.visits = 0
        naive = 0
        ops = 500
        diff=[0]*(m+1);updates=[]
        for _ in range(ops):
            l = rng.randrange(m)
            r = rng.randrange(l, m)
            L.range_add(l, r, 1)
            naive += r - l + 1
            diff[l]+=1;diff[r+1]-=1;updates.append([l,r,1])
        touched=L.visits;expected=[];value=0
        for v in diff[:-1]:value+=v;expected.append(value)
        assert [L.range_sum(i,i) for i in range(m)]==expected
        rows.append({"k": k, "n": m, "lazy": touched / ops, "naive": naive / ops,"validated_final_elements":m,"updates_sha256":R.digest(updates),"seed":5})
    return {"a": a, "query": [3, 12], "min": val, "cover": cov, "visits": T.visits, "lazy": rows}


def compute_rmq() -> dict:
    a = [5, 8, 6, 3, 2, 7, 2, 6, 7, 1, 9, 4, 3, 5, 8, 1]
    st = P.SparseTable(a)
    l, r = 2, 12
    j = st.lg[r - l + 1]
    # a small tree for LCA
    parent = [-1, 0, 0, 1, 1, 2, 2, 3, 3, 5, 6, 6]
    kids = {}
    for v, p in enumerate(parent):
        if p >= 0:
            kids.setdefault(p, []).append(v)
    E = P.EulerLCA(kids, 0)
    B = P.BinaryLift([0] + parent[1:], 0)
    lca = E.lca(7, 4)
    B.steps = 0
    lca2 = B.lca(9, 11)
    steps = B.steps
    ct = P.cartesian_tree(a)
    return {"a": a, "table": st.t, "lg": st.lg, "query": [l, r], "j": j, "windows": [[l, l + (1 << j) - 1],
            [r - (1 << j) + 1, r]], "min": st.query(l, r), "argmin": st.argmin(l, r), "cells": st.cells(),
            "parent": parent, "euler": E.order, "depth": E.depth, "first": {str(k): v for k, v in E.first.items()},
            "lca_7_4": lca, "lca_9_11": lca2, "lift_steps": steps, "cartesian": ct}


def compute_monotone() -> dict:
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]
    k = 4
    out, tr, pops = P.sliding_max(a, k, trace=True)
    h = [2, 1, 5, 6, 4, 5, 3, 1, 2, 4, 3, 2]
    rect = P.largest_rectangle(h)
    rng = random.Random(6)
    scale = []
    for e in range(3, 18, 2):
        m = 1 << e
        b = [rng.randint(0, 10 ** 6) for _ in range(m)]
        dq, pp = deque(), 0
        for i, x in enumerate(b):
            while dq and b[dq[-1]] <= x:
                dq.pop()
                pp += 1
            dq.append(i)
            if dq[0] <= i - 64:
                dq.popleft()
                pp += 1
        scale.append({"n": m, "pops": pp, "per": pp / m})
    return {"a": a, "k": k, "max": out, "trace": tr, "pops": pops, "next_greater": P.next_greater(a), "h": h,
            "rect": list(rect), "rect_brute": P.largest_rectangle_brute(h), "scale": scale}


def compute_search() -> dict:
    w = [7, 2, 5, 10, 8, 4, 6, 3, 9, 1]
    days = 4
    calls_seen = []

    def ok(cap):
        d, load_ = 1, 0
        for x in w:
            if load_ + x > cap:
                d += 1
                load_ = 0
            load_ += x
        calls_seen.append((cap, d <= days))
        return d <= days
    cap, calls = P.binary_search_answer(max(w), sum(w), ok)
    pred = [{"cap": c, "ok": ok(c)} for c in range(max(w), sum(w) + 1)]
    a = list(range(0, 2 * 10 ** 6, 2))
    rows = []
    for d in (1, 4, 16, 64, 256, 1024, 4096, 65536, 10 ** 6 - 1):
        x = a[d]
        j, probes = P.galloping(a, x)
        assert j == d
        lo,hi,binary=0,len(a),0
        while lo<hi:
            mid=(lo+hi)//2;binary+=1
            if a[mid]<x:lo=mid+1
            else:hi=mid
        assert lo==j
        rows.append({"d": d, "gallop": probes, "binary": binary})
    return {"w": w, "days": days, "cap": cap, "calls": calls, "trace": calls_seen[:calls], "pred": pred,
            "gallop": rows, "n": len(a)}


def compute_bits() -> dict:
    tab = [{"i": i, "bin": format(i, "04b"), "pop": P.popcount(i), "low": P.lowbit(i) if i else 0,
            "gray": format(P.gray(i), "04b")} for i in range(16)]
    sub = [{"n": n, "pairs": sum(1 for m in range(1 << n) for _ in P.submasks(m)), "three": 3 ** n,
            "naive": 4 ** n} for n in range(2, 13, 2)]
    rows = []
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "bits", BITS_C)
        for n, m in ((1024, 10000), (2048, 20000)):
            observations=[_run(d,exe,n,m) for _ in range(3)]
            assert all(row[3]=='1' and row[6]==row[7] for row in observations)
            tp,tb,ones,agree,tl,tbp,l1,l2=observations[0]
            tp,tb,tl,tbp=[min(float(row[j]) for row in observations) for j in (0,1,4,5)]
            rows.append({"n": n, "m": m, "closure_plain": float(tp), "closure_bits": float(tb), "reach": int(ones),
                         "lcs_dp": float(tl), "lcs_bits": float(tbp), "lcs": int(l1)})
    return {"table": tab, "submasks": sub, "rows": rows}


def compute_split() -> dict:
    rng = random.Random(8)
    a = [rng.randint(1, 10 ** 6) for _ in range(20)]
    t = sum(rng.sample(a, 9))
    (fb,wb),tb,brute_timing=_measure(lambda:P.subset_sum_brute(a,t))
    (fm,wm),tm,mitm_timing=_measure(lambda:P.subset_sum_mitm(a,t))
    assert fb==fm
    n = 20000
    arr = [rng.randrange(2000) for _ in range(n)]
    qs = []
    for _ in range(20000):
        l = rng.randrange(n)
        qs.append((l, min(n - 1, l + rng.randrange(n // 2))))
    (ans,moves),tmo,mo_timing=_measure(lambda:P.mo_distinct(arr,qs))
    naive = sum(r - l + 1 for l, r in qs)
    check = R.mo_reference(arr,qs)
    assert check == ans
    S = P.SqrtDecomp(list(range(10000)))
    S.touched = 0
    S.query(137, 8641)
    return {"n": len(a), "target": t, "found": fb, "brute_sums": wb, "mitm_work": wm, "brute_s": tb, "mitm_s": tm,
            "timings":dict(brute=brute_timing,mitm=mitm_timing,mo=mo_timing),"subset_input":a,
            "n40_brute": 2 ** 40, "n40_mitm": 2 * 2 ** 20, "mo_n": n, "mo_q": len(qs), "mo_moves": moves,
            "mo_naive": naive, "mo_s": tmo,
            "mo_validation": dict(queries=len(qs),input_sha256=R.digest([arr,qs]),output_sha256=R.digest(ans),reference='offline last-occurrence sum-tree sweep',seed=8),
            "mitm_counter_scope": 'generated subset sums plus lower-bound calls; excludes sort/comparison/bit costs',  "sqrt_touched": S.touched, "sqrt_B": S.B}


def compute_layouts() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "layouts", LAYOUTS_C, flags=("-O2", "-march=native"))
        out = _native(d,exe).stdout.strip().splitlines()
    for ln in out:
        k, b, bl, e, bt, ok = ln.split()
        assert ok == "1"
        rows.append({"logn": int(k), "bytes": 4 << int(k), "branchy": float(b), "branchless": float(bl),
                     "eytzinger": float(e), "btree": float(bt)})
    return {"rows": rows, "queries": 1 << 20}


def compute_simd() -> dict:
    full = _corpus()
    out = {}
    with tempfile.TemporaryDirectory() as d:
        Path(d, "t").write_bytes(full)
        exe = _build(d, "tok", TOKEN_C, flags=("-O2", "-march=native"))
        sz, bs, bv, ws, ls, ok = _run(d, exe, "t")
        assert ok == "1"
        from explainer.cs.pebble import programs as PR
        words = PR.job_words(full)
        assert int(ws) == len(words) and int(ls) == sum(map(len, words))
        out["token"] = {"bytes": int(sz), "scalar_s": float(bs), "simd_s": float(bv), "words": int(ws),
                        "letters": int(ls)}
        exe = _build(d, "maps", MAPS_CPP, cc="g++", flags=("-O2", "-march=native"))
        for load_ in ("0.5", "0.875"):
            rows = []
            for ln in _native(d,exe,load_).stdout.strip().splitlines():
                v = ln.split()
                assert v[-1] == "1"
                k = int(v[0])
                rows.append({"logcap": k, "n": int((1 << k) * float(load_)), "umap_ins": float(v[1]),
                             "umap_get": float(v[2]), "linear_ins": float(v[3]), "linear_get": float(v[4]),
                             "swiss_ins": float(v[5]), "swiss_get": float(v[6]), "unordered_buckets":int(v[7]),"unique_keys":int(v[8]),"unordered_occupancy":int(v[8])/int(v[7])})
            out["load_" + load_] = rows
    return out


def compute_sorting() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "sorts", SORTS_CPP, cc="g++", flags=("-O2", "-march=native"))
        for ln in _native(d,exe).stdout.strip().splitlines():
            k, s, r, ok = ln.split()
            assert ok == "1"
            rows.append({"logn": int(k), "n": 1 << int(k), "std_sort": float(s), "radix": float(r)})
    cross = next(r["n"] for r in rows if r["radix"] < r["std_sort"])
    return {"rows": rows, "crossover": cross}


def compute_bench() -> dict:
    import os
    runs = []
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "bench", BENCH_C, libs=("-lm",))
        for _ in range(30):
            v = list(map(float, _run(d, exe, 0)[:6]))
            runs.append(v)
        dead, live = map(float, _run(d, exe, 1))
        pads = []
        order=[pad for pad in range(0,4097,256) for _ in range(5)]
        random.Random(2412).shuffle(order)
        raw={pad:[] for pad in range(0,4097,256)}
        for pad in order:
            env={"PATH":os.environ.get("PATH",""),"PAD":"x"*pad}
            observations=list(map(float,_run(d,exe,0,env=env)[:6]))
            raw[pad].append(observations)
        for pad,observations in raw.items():
            ts=sorted(statistics.median(row[1:]) for row in observations)
            pads.append(dict(pad=pad,median=ts[2],min=ts[0],max=ts[-1],runs=observations))
    x=(np.arange(1<<16)%97).astype(np.float32)/np.float32(97)
    expected=float((x*x[(np.arange(1<<16)*7)&((1<<16)-1)]).astype(np.float64).sum())*800*6
    for execution in _AUDIT.executions:
        if execution['args']==['0']:
            assert math.isclose(float(execution['stdout'].split()[6]),expected,rel_tol=3e-6)
    firsts = [r[0] for r in runs]
    warm = [statistics.median(r[1:]) for r in runs]
    return {"runs": runs, "first_mean": statistics.mean(firsts), "warm_mean": statistics.mean(warm),
            "warm_sd": statistics.stdev(warm), "warm_min": min(warm), "warm_max": max(warm),
            "dead_s": dead, "live_s": live, "pads": pads,
            "pad_execution_order": order,"warm_statistic":"median of later five observations", "causal_scope":"observed spread; shared host/ASLR not controlled",
            "pad_spread": max(p["median"] for p in pads) / min(p["median"] for p in pads)}


def compute_job() -> dict:
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs17.compute import JOB_OA_C
    full = _corpus()
    ref = PR.job_reference(full)
    from collections import Counter
    expected=Counter(PR.job_words(full))
    assert len(expected)<(1<<17)-1 and max(map(len,expected))<256
    assert sum(map(len,expected))<(1<<21) and max(expected.values())<(1<<32)
    out = {}
    with tempfile.TemporaryDirectory() as d:
        Path(d, "t").write_bytes(full)
        for name, code, flags in (("textbook", JOB_OA_C, ("-O2",)), ("engineered", JOB_ENG_C, ("-O2", "-march=native"))):
            exe = _build(d, name, R.job_code(name,code), flags=flags)
            ts = []
            for _ in range(7):
                r = _native(d,exe,"t",text=False,env=dict(os.environ,CS24_COUNTS_FILE=str(Path(d,"all-counts.txt"))))
                ts.append(float(r.stdout.split()[0]))
                assert r.stderr == ref, name
                actual={}
                for line in Path(d,'all-counts.txt').read_bytes().splitlines():
                    word,count=line.rsplit(b' ',1);assert word not in actual;actual[word]=int(count)
                assert actual==expected,(name,'complete word counts')
            out[name] = {"best": min(ts), "median": statistics.median(ts), "runs": ts,"all_count_entries_checked":len(expected),"full_counts_sha256":R.digest(sorted((w.decode(),c) for w,c in actual.items()))}
    led = json.loads((Cache("cs20").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 24]
    led.append({"part": 24, "label": r"engineered, \ this machine", "seconds": out["engineered"]["best"],
                "native": True, "textbook_native_seconds": out["textbook"]["best"], "cpu": _cpu()})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    row8 = next(r for r in led if r["part"] == 17)
    return {"bytes": len(full), "words": len(PR.job_words(full)), "distinct": len(set(PR.job_words(full))),
            "textbook": out["textbook"], "engineered": out["engineered"],
            "speedup": out["textbook"]["best"] / out["engineered"]["best"],
            "pebble_hash_s": row8["seconds"], "ledger": led, "report": ref.decode().splitlines(),
            "ns_per_byte": out["engineered"]["best"] * 1e9 / len(full)}


def _ski_predict(B,d,y,lam):
    """Discrete buy-at-start-of-day policy from Purohit et al. (2018), Algorithm2."""
    return R.ski_ratio(B,d,y,lam)



def compute_frontier() -> dict:
    full = _corpus()
    offs = np.array([m.start() for m in re.finditer(rb"[a-z]+", full.lower())], dtype=np.uint64)
    rows = []
    with tempfile.TemporaryDirectory() as d:
        offs.tofile(Path(d, "keys.bin"))
        exe = _build(d, "learned", LEARNED_C, libs=("-lm",))
        for eps in (4, 16, 64, 256, 1024):
            env=dict(os.environ,CS24_ARRAY_DIR=d)
            values=_run(d,exe,"keys.bin",eps,env=env)
            n,e,ns,tb,tl,ok,active,peak,struct_size,max_error,fallbacks,queries=values
            assert ok=="1"
            q=np.fromfile(Path(d,'queries.bin'),dtype=np.uint64)
            b=np.fromfile(Path(d,'binary.bin'),dtype=np.int64)
            l=np.fromfile(Path(d,'learned.bin'),dtype=np.int64)
            expected=np.searchsorted(offs,q,side='left')
            assert len(q)==int(queries) and np.array_equal(b,expected) and np.array_equal(l,expected)
            rows.append(dict(eps=int(e),segments=int(ns),binary_ns=float(tb),learned_ns=float(tl),
                             model_bytes=int(active),peak_requested_model_bytes=int(peak),struct_bytes=int(struct_size),
                             max_stored_key_error=float(max_error),fallbacks=int(fallbacks),queries=len(q),
                             queries_sha256=R.file_hash(Path(d,'queries.bin')),results_sha256=R.file_hash(Path(d,'learned.bin')),
                             independent_reference='NumPy searchsorted on every actual query'))
    B=10;rng=random.Random(24);ski=[]
    for lam in (0.1,0.3,0.6,1.0):
        _,_,early,late,consistency,worst=R.ski_parameters(B,lam)
        # For either forecast branch the maximum is attained at its buy day.
        witnesses=[dict(days=early,forecast=B,ratio=_ski_predict(B,early,B,lam)),
                   dict(days=late,forecast=0,ratio=_ski_predict(B,late,0,lam))]
        assert max(w['ratio'] for w in witnesses)==float(worst)
        for sigma in (0.0,0.5,1.0,2.0,4.0):
            trials=[]
            for _ in range(4000):
                dd=rng.randint(1,4*B);forecast=dd+sigma*B*rng.gauss(0,1)
                trials.append([dd,forecast,_ski_predict(B,dd,forecast,lam)])
            ratios=[row[2] for row in trials];assert max(ratios)<=float(worst)
            if not sigma:assert max(ratios)<=float(consistency)
            ski.append(dict(lam=lam,sigma=sigma,mean=statistics.mean(ratios),worst_case=float(worst),
                            consistency=float(consistency),robustness=float(worst),loose_consistency=1+lam,
                            loose_robustness=1+1/lam,early_buy_day=early,late_buy_day=late,witnesses=witnesses,
                            input_output_sha256=R.digest(trials),trials=trials,seed=24,
                            scope='discrete deterministic policy; Gaussian synthetic forecasts, not a trained model'))
    return dict(n=len(offs),rows=rows,key_bytes=len(offs)*8,key_sha256=hashlib.sha256(offs.tobytes()).hexdigest(),ski=ski,B=B,
                fit_scope='anchored greedy floating-point teaching fit; complete bracket check and full-search fallback; not optimal PGM',
                timing_scope='lookup only; model construction and independent checks outside timers; active and peak requested storage exclude keys/queries')


def compute_branches() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "branches", BRANCHES_C)
        rb, sb, rl, sl, ok = _run(d, exe)
        assert ok == "1"
    return {"random_branchy": float(rb), "sorted_branchy": float(sb), "random_branchless": float(rl),
            "sorted_branchless": float(sl), "n": 1 << 24}


def compute_vector() -> dict:
    out = {}
    with tempfile.TemporaryDirectory() as d:
        for name, flags in (("o1", ("-O1",)), ("o3", ("-O3", "-march=native"))):
            exe = _build(d, "vec_" + name, VECTOR_C, flags=flags)
            observations=[_run(d,exe) for _ in range(3)]
            assert all(row[3:]==observations[0][3:] for row in observations)
            v=[min(float(row[j]) for row in observations) for j in range(3)]+observations[0][3:]
            out[name] = {"saxpy": float(v[0]), "isum": float(v[1]), "prefix": float(v[2]), "check": v[3:]}
    assert out["o1"]["check"] == out["o3"]["check"]
    return out


def compute_topk() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "topk", TOPK_CPP, cc="g++")
        s, ps, ne, hp, ok = _run(d, exe)
        assert ok == "1"
    return {"n": 1 << 24, "k": 20, "sort": float(s), "partial_sort": float(ps), "nth_element": float(ne),
            "heap": float(hp)}


def _pairs_brute(a, T):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] + a[j] <= T)


def _pairs_fast(a, T):
    b = sorted(a)
    i, j, c = 0, len(b) - 1, 0
    while i < j:
        if b[i] + b[j] <= T:
            c += j - i
            i += 1
        else:
            j -= 1
    return c


def compute_pairs() -> dict:
    rng = random.Random(14)
    fails = 0
    tests = 2000
    stress=[]
    for _ in range(tests):
        n = rng.randint(0, 12)
        a = [rng.randint(-5, 5) for _ in range(n)]
        T = rng.randint(-8, 8)
        brute,fast=_pairs_brute(a,T),_pairs_fast(a,T);fails+=brute!=fast;stress.append([a,T,brute,fast])
    rows = []
    for n in (500, 1000, 2000, 4000):
        a = [rng.randint(0, 10 ** 6) for _ in range(n)]
        T = 10 ** 6
        x,tb,brute_timing=_measure(lambda:_pairs_brute(a,T))
        y,tf,fast_timing=_measure(lambda:_pairs_fast(a,T))
        assert x==y
        rows.append(dict(n=n,brute_s=tb,fast_s=tf,pairs=x,brute_timing=brute_timing,fast_timing=fast_timing,input_sha256=R.digest(a)))
    return {"tests": tests, "fails": fails, "rows": rows,"stress_fixtures":stress,"seed":14}


# --------------------------------------------------------------------------------------------------- native programs

HOOK_C = r'''

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
/* sum n numbers two ways: an array in order, and a linked list whose nodes sit in random order in memory */
typedef struct node { struct node *next; long val; } node;
int main(int argc, char **argv) {
  int logn = atoi(argv[1]); long n = 1L << logn;
  long *a = malloc(8 * n); node *pool = malloc(sizeof(node) * n); long *perm = malloc(8 * n);
  for (long i = 0; i < n; i++) { a[i] = i & 1023; perm[i] = i; }
  for (long i = n - 1; i > 0; i--) { long j = rnd() % (i + 1); long t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
  for (long i = 0; i < n; i++) { pool[perm[i]].val = a[i]; pool[perm[i]].next = i + 1 < n ? &pool[perm[i + 1]] : 0; }
  node *head = &pool[perm[0]];
  double ba = 1e9, bl = 1e9; long sa = 0, sl = 0;
  for (int rep = 0; rep < 5; rep++) {
    double t0 = now(); long s = 0; for (long i = 0; i < n; i++) s += a[i]; t0 = now() - t0; if (t0 < ba) ba = t0; sa = s;
    t0 = now(); s = 0; for (node *p = head; p; p = p->next) s += p->val; t0 = now() - t0; if (t0 < bl) bl = t0; sl = s;
    cs24_check(sa==(n/1024)*523776L && sl==(n/1024)*523776L,"every_trial_exact_sum",2);
  }
  cs24_check(sa == (n/1024)*523776L && sl == (n/1024)*523776L,"exact_sum_closed_form",2);
  printf("%d %.3f %.3f %d\n", logn, ba * 1e9 / n, bl * 1e9 / n, sa == sl);
  return 0;
}
'''

RANGES_C = r'''

/* Mixed point updates and prefix queries on n = 2^20 numbers: four structures, ns per operation. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
#define N (1 << 20)
static long a[N + 1], P[N + 2], F[N + 1], T[2 * N];
int main() {
  int Q = 1 << 20; int *op = malloc(4 * Q), *ix = malloc(4 * Q), *vv = malloc(4 * Q);
  for (int q = 0; q < Q; q++) { op[q] = rnd() & 1; ix[q] = rnd() % N + 1; vv[q] = rnd() % 100; }
  long *ans[4];for(int z=0;z<4;z++)ans[z]=calloc(Q,sizeof(long));
  double t; long s;
  /* plain array: update O(1), query O(n) -- only 2^10 operations, it is that slow */
  int Qs = 1 << 10; t = now(); s = 0;
  for (int q = 0; q < Qs; q++) { if (op[q]) a[ix[q]] += vv[q]; else { long x = 0; for (int i = 1; i <= ix[q]; i++) x += a[i]; s += x; ans[0][q]=x; } }
  double plain = (now() - t) / Qs; long sp = s; memset(a, 0, sizeof a);
  /* prefix array: query O(1), update O(n) */
  t = now(); s = 0;
  for (int q = 0; q < Qs; q++) { if (op[q]) { for (int i = ix[q]; i <= N; i++) P[i] += vv[q]; } else { s += P[ix[q]];ans[1][q]=P[ix[q]]; } }
  double prefix = (now() - t) / Qs; long spp = s;
  /* Fenwick */
  t = now(); s = 0;
  for (int q = 0; q < Q; q++) { if (op[q]) { for (int i = ix[q]; i <= N; i += i & -i) F[i] += vv[q]; } else { long x = 0; for (int i = ix[q]; i > 0; i -= i & -i) x += F[i]; s += x;ans[2][q]=x; } }
  double fen = (now() - t) / Q; long sf = s;
  /* bottom-up segment tree (leaves at N..2N-1), prefix query as the range [0, ix) */
  t = now(); s = 0;
  for (int q = 0; q < Q; q++) {
    if (op[q]) { int i = ix[q] - 1 + N; T[i] += vv[q]; for (i >>= 1; i; i >>= 1) T[i] = T[2 * i] + T[2 * i + 1]; }
    else { long x = 0; int l = N, r = ix[q] + N; while (l < r) { if (l & 1) x += T[l++]; if (r & 1) x += T[--r]; l >>= 1; r >>= 1; } s += x;ans[3][q]=x; }
  }
  double seg = (now() - t) / Q; long ss = s;
  long blocks[1024]={0};memset(a,0,sizeof a);
  for(int q=0;q<Q;q++){
    int i=ix[q];if(op[q]){a[i]+=vv[q];blocks[(i-1)/1024]+=vv[q];}
    else {long expected=0;int whole=i/1024;for(int b=0;b<whole;b++)expected+=blocks[b];for(int j=whole*1024+1;j<=i;j++)expected+=a[j];
      if(ans[2][q]!=expected||ans[3][q]!=expected||(q<Qs&&(ans[0][q]!=expected||ans[1][q]!=expected)))abort();}
  }
  cs24_check(1,"all_range_answers_sqrt_reference",2ULL*Q+2ULL*Qs);
  /* check: Fenwick and segment tree agree on all 2^20 operations; plain and prefix on the first 2^10 */
  printf("%.1f %.1f %.1f %.1f %d %d\n", plain * 1e9, prefix * 1e9, fen * 1e9, seg * 1e9, sf == ss, sp == spp);
  return 0;
}
'''

LAYOUTS_C = r'''

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <immintrin.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int cmpu(const void *a, const void *b) { unsigned x = *(const unsigned *)a, y = *(const unsigned *)b; return x < y ? -1 : x > y; }
/* lower bound: first index with a[i] >= x */
__attribute__((noinline, optimize("no-if-conversion","no-if-conversion2"))) static int lb_branchy(const unsigned *a, int n, unsigned x) {
  int lo = 0, hi = n;
  while (lo < hi) { int m = (lo + hi) >> 1; if (a[m] < x) lo = m + 1; else hi = m; }
  return lo;
}
__attribute__((noinline)) static int lb_branchless(const unsigned *a, int n, unsigned x) {
  const unsigned *base = a; int len = n;
  while (len > 1) { int half = len >> 1; base = (base[half - 1] < x) ? base + half : base; len -= half; }
  return (int)(base - a) + (*base < x);
}
static unsigned *eyt; static int eyn;
static int eyt_build(const unsigned *a, int i, int k) { if (k <= eyn) { i = eyt_build(a, i, 2 * k); eyt[k] = a[i++]; i = eyt_build(a, i, 2 * k + 1); } return i; }
__attribute__((noinline)) static int lb_eyt(unsigned x) {
  int k = 1;
  while (k <= eyn) { if(k<=eyn/16)__builtin_prefetch(eyt + k * 16); k = 2 * k + (eyt[k] < x); }
  k >>= __builtin_ffs(~k);
  return k; /* index in eyt (0 = none) */
}
/* B-tree layout (S-tree): nodes of B=16 keys, implicit, children (B+1)k + i + 1 */
#define B 16
static unsigned *bt; static int nblocks;
static int go(int k, int i) { return k * (B + 1) + i + 1; }
static void bt_build(const unsigned *a, int n, int k, int *t) {
  if (k < nblocks) { for (int i = 0; i < B; i++) { bt_build(a, n, go(k, i), t); bt[k * B + i] = (*t < n ? a[(*t)++] : 0xFFFFFFFFu); } bt_build(a, n, go(k, B), t); }
}
__attribute__((noinline)) static unsigned lb_btree(unsigned x) {
  int k = 0; unsigned res = 0xFFFFFFFFu;
  __m512i xv = _mm512_set1_epi32((int)(x ^ 0x80000000u));
  while (k < nblocks) {
    __m512i v = _mm512_xor_si512(_mm512_loadu_si512((const void *)(bt + k * B)), _mm512_set1_epi32((int)0x80000000u));
    unsigned mask = _mm512_cmpgt_epi32_mask(xv, v); /* keys < x */
    int i = __builtin_popcount(mask);
    if (i < B) res = bt[k * B + i];
    k = go(k, i);
  }
  return res;
}
int main(int argc, char **argv) {
  int Q = 1 << 20;
  unsigned *qs = malloc(4 * Q);
  for (int logn = 10; logn <= 26; logn += 2) {
    int n = 1 << logn;
    unsigned *a = malloc(4 * n);
    for (int i = 0; i < n; i++) a[i] = rnd();
    qsort(a, n, 4, cmpu);
    for (int i = 0; i < Q; i++) qs[i] = rnd();
    eyn = n; eyt = aligned_alloc(64, ((4UL*(n+1)+256+63)/64)*64); eyt_build(a, 0, 1);
    nblocks = (n + B - 1) / B; bt = aligned_alloc(64, 4 * nblocks * B); int t = 0; bt_build(a, n, 0, &t);
    unsigned *actual[4];for(int z=0;z<4;z++)actual[z]=malloc(4*Q);
    double best[4] = {1e9, 1e9, 1e9, 1e9}; unsigned long long chk[4] = {0};
    for (int rep = 0; rep < 3; rep++) {
      double t0; unsigned long long s;
      t0 = now(); s = 0; for (int i = 0; i < Q; i++) { int j = lb_branchy(a, n, qs[i]); s += (actual[0][i]=j < n ? a[j] : 0xFFFFFFFFu); } t0 = now() - t0; if (t0 < best[0]) best[0] = t0; chk[0] = s;
      t0 = now(); s = 0; for (int i = 0; i < Q; i++) { int j = lb_branchless(a, n, qs[i]); s += (actual[1][i]=j < n ? a[j] : 0xFFFFFFFFu); } t0 = now() - t0; if (t0 < best[1]) best[1] = t0; chk[1] = s;
      t0 = now(); s = 0; for (int i = 0; i < Q; i++) { int k = lb_eyt(qs[i]); s += (actual[2][i]=k ? eyt[k] : 0xFFFFFFFFu); } t0 = now() - t0; if (t0 < best[2]) best[2] = t0; chk[2] = s;
      t0 = now(); s = 0; for (int i = 0; i < Q; i++) { s += (actual[3][i]=lb_btree(qs[i])); } t0 = now() - t0; if (t0 < best[3]) best[3] = t0; chk[3] = s;
      for(int i=0;i<Q;i++){
        int j=lb_branchy(a,n,qs[i]);if((j&&a[j-1]>=qs[i])||(j<n&&a[j]<qs[i]))abort();
        unsigned expected=j<n?a[j]:0xFFFFFFFFu;for(int z=0;z<4;z++)if(actual[z][i]!=expected)abort();
      }
      cs24_check(1,"all_layout_lower_bound_values",4ULL*Q);
    }
    printf("%d %.2f %.2f %.2f %.2f %d\n", logn, best[0] * 1e9 / Q, best[1] * 1e9 / Q, best[2] * 1e9 / Q, best[3] * 1e9 / Q,
           chk[0] == chk[1] && chk[1] == chk[2] && chk[2] == chk[3]);
    free(a); free(eyt); free(bt);for(int z=0;z<4;z++)free(actual[z]);
  }
  return 0;
}
'''

MAPS_CPP = r'''

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <unordered_map>
#include <vector>
#include <emmintrin.h>
using namespace std;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline uint64_t mix(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
struct Linear {  // open addressing, linear probing, keys != 0
  vector<uint64_t> k; vector<uint32_t> v; uint64_t mask;
  Linear(size_t cap) : k(cap, 0), v(cap), mask(cap - 1) {}
  void add(uint64_t key) { uint64_t i = mix(key) & mask; while (k[i] && k[i] != key) i = (i + 1) & mask; if (!k[i]) { k[i] = key; v[i] = 0; } v[i]++; }
  uint32_t get(uint64_t key) const { uint64_t i = mix(key) & mask; while (k[i]) { if (k[i] == key) return v[i]; i = (i + 1) & mask; } return 0; }
};
struct Swiss {  // groups of 16 control bytes: 0x80 empty, else the hash's low 7 bits; SSE2 compares a group at once
  vector<int8_t> ctrl; vector<uint64_t> k; vector<uint32_t> v; size_t ngroups;
  Swiss(size_t cap) : ctrl(cap, (int8_t)0x80), k(cap), v(cap), ngroups(cap / 16) {}
  void add(uint64_t key) {
    uint64_t h = mix(key); int8_t h2 = h & 0x7f; size_t g = (h >> 7) % ngroups;
    __m128i m = _mm_set1_epi8(h2), e = _mm_set1_epi8((char)0x80);
    for (;;) {
      __m128i c = _mm_loadu_si128((const __m128i *)&ctrl[g * 16]);
      unsigned hit = _mm_movemask_epi8(_mm_cmpeq_epi8(c, m));
      while (hit) { int j = __builtin_ctz(hit); if (k[g * 16 + j] == key) { v[g * 16 + j]++; return; } hit &= hit - 1; }
      unsigned emp = _mm_movemask_epi8(_mm_cmpeq_epi8(c, e));
      if (emp) { int j = __builtin_ctz(emp); ctrl[g * 16 + j] = h2; k[g * 16 + j] = key; v[g * 16 + j] = 1; return; }
      g = (g + 1) % ngroups;
    }
  }
  uint32_t get(uint64_t key) const {
    uint64_t h = mix(key); int8_t h2 = h & 0x7f; size_t g = (h >> 7) % ngroups;
    __m128i m = _mm_set1_epi8(h2), e = _mm_set1_epi8((char)0x80);
    for (;;) {
      __m128i c = _mm_loadu_si128((const __m128i *)&ctrl[g * 16]);
      unsigned hit = _mm_movemask_epi8(_mm_cmpeq_epi8(c, m));
      while (hit) { int j = __builtin_ctz(hit); if (k[g * 16 + j] == key) return v[g * 16 + j]; hit &= hit - 1; }
      if (_mm_movemask_epi8(_mm_cmpeq_epi8(c, e))) return 0;
      g = (g + 1) % ngroups;
    }
  }
};
int main(int argc, char **argv) {
  double load = atof(argv[1]);
  for (int logn = 10; logn <= 24; logn += 2) {
    size_t cap = 1u << logn; size_t n = (size_t)(cap * load); vector<uint64_t> keys(n), probe(n);
    for (auto &x : keys) x = rnd() | 1; for (size_t i = 0; i < n; i++) probe[i] = (i & 1) ? keys[rnd() % n] : (rnd() | 1);
    vector<uint64_t> sorted=keys;sort(sorted.begin(),sorted.end());vector<uint32_t> ref(n);
    for(size_t i=0;i<n;i++){auto p=equal_range(sorted.begin(),sorted.end(),probe[i]);ref[i]=p.second-p.first;}
    size_t buckets=0,unique=0;
    double best[3][2]; for (auto &r : best) r[0] = r[1] = 1e9; uint64_t chk[3] = {0, 0, 0};
    for (int rep = 0; rep < 3; rep++) {
      { double t0 = now(); unordered_map<uint64_t, uint32_t> m; m.reserve(n); for (auto x : keys) m[x]++; double t1 = now();
        uint64_t s = 0; for (auto x : probe) { auto it = m.find(x); if (it != m.end()) s += it->second; } double t2 = now();
        best[0][0] = min(best[0][0], t1 - t0); best[0][1] = min(best[0][1], t2 - t1); chk[0] = s;buckets=m.bucket_count();unique=m.size();
        for(size_t i=0;i<n;i++){auto p=m.find(probe[i]);if((p==m.end()?0:p->second)!=ref[i])abort();}
        for(size_t i=0;i<n;i++){auto p=equal_range(sorted.begin(),sorted.end(),keys[i]);if(m[keys[i]]!=p.second-p.first)abort();}
        cs24_check(1,"all_unordered_map_counts",2ULL*n); }
      { double t0 = now(); Linear m(cap); for (auto x : keys) m.add(x); double t1 = now();
        uint64_t s = 0; for (auto x : probe) s += m.get(x); double t2 = now();
        best[1][0] = min(best[1][0], t1 - t0); best[1][1] = min(best[1][1], t2 - t1); chk[1] = s;
        for(size_t i=0;i<n;i++)if(m.get(probe[i])!=ref[i])abort();
        for(size_t i=0;i<n;i++){auto p=equal_range(sorted.begin(),sorted.end(),keys[i]);if(m.get(keys[i])!=p.second-p.first)abort();}
        cs24_check(1,"all_linear_counts",2ULL*n); }
      { double t0 = now(); Swiss m(cap); for (auto x : keys) m.add(x); double t1 = now();
        uint64_t s = 0; for (auto x : probe) s += m.get(x); double t2 = now();
        best[2][0] = min(best[2][0], t1 - t0); best[2][1] = min(best[2][1], t2 - t1); chk[2] = s;
        for(size_t i=0;i<n;i++)if(m.get(probe[i])!=ref[i])abort();
        for(size_t i=0;i<n;i++){auto p=equal_range(sorted.begin(),sorted.end(),keys[i]);if(m.get(keys[i])!=p.second-p.first)abort();}
        cs24_check(1,"all_swiss_counts",2ULL*n); }
    }
    printf("%d", logn); for (int i = 0; i < 3; i++) printf(" %.2f %.2f", best[i][0] * 1e9 / n, best[i][1] * 1e9 / n);
    printf(" %zu %zu %d\n",buckets,unique,chk[0] == chk[1] && chk[1] == chk[2]);
  }
}
'''

SORTS_CPP = r'''

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static uint64_t rs = 88172645463325252ULL;
static uint32_t rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (uint32_t)(rs >> 13); }
static void radix(uint32_t *a, uint32_t *tmp, size_t n) {  // LSD, four passes of 8 bits
  for (int sh = 0; sh < 32; sh += 8) {
    size_t cnt[257] = {0};
    for (size_t i = 0; i < n; i++) cnt[((a[i] >> sh) & 255) + 1]++;
    for (int b = 0; b < 256; b++) cnt[b + 1] += cnt[b];
    for (size_t i = 0; i < n; i++) tmp[cnt[(a[i] >> sh) & 255]++] = a[i];
    swap(a, tmp);
  }
}
int main() {
  for (int logn = 4; logn <= 24; logn += 2) {
    size_t n = 1u << logn; size_t reps = max<size_t>(1, (1u << 24) / n);
    vector<uint32_t> src(n * reps), a(n * reps), b(n * reps), t(n);
    for (auto &x : src) x = rnd();
    double bs = 1e9, br = 1e9; bool ok = true;
    for (int rep = 0; rep < 3; rep++) {
      double t0 = now(); for (size_t r = 0; r < reps; r++) { memcpy(a.data()+r*n, &src[r * n], 4 * n); sort(a.begin()+r*n, a.begin()+(r+1)*n); } double t1 = now();
      for (size_t r = 0; r < reps; r++) { memcpy(b.data()+r*n, &src[r * n], 4 * n); radix(b.data()+r*n, t.data(), n); } double t2 = now();
      bs = min(bs, t1 - t0); br = min(br, t2 - t1); ok = ok && a == b;
      // Equality to the library sort for every batch plus sortedness/permutation certificate.
      for(size_t r=0;r<reps;r++)if(!is_sorted(b.begin()+r*n,b.begin()+(r+1)*n))abort();
      cs24_check(a==b,"all_sorted_batch_elements",n*reps);
    }
    printf("%d %.2f %.2f %d\n", logn, bs * 1e9 / (n * reps), br * 1e9 / (n * reps), ok);
  }
}
'''

BITS_C = r'''

/* Word-level parallelism: Warshall's transitive closure and the LCS length, plain against 64 bits per operation. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  int n = atoi(argv[1]), m = atoi(argv[2]);
  /* closure of a random graph with average out-degree 1.2 */
  unsigned char *R = calloc((size_t)n * n, 1); int W = (n + 63) / 64; uint64_t *B = calloc((size_t)n * W, 8);
  for (int i = 0; i < n; i++) { R[(size_t)i * n + i] = 1; B[(size_t)i * W + i / 64] |= 1ULL << (i % 64); }
  for (long e = 0; e < (long)(1.2 * n); e++) { int i = rnd() % n, j = rnd() % n; R[(size_t)i * n + j] = 1; B[(size_t)i * W + j / 64] |= 1ULL << (j % 64); }
  unsigned char *G=malloc((size_t)n*n);memcpy(G,R,(size_t)n*n);
  double t0 = now();
  for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) if (R[(size_t)i * n + k]) { unsigned char *ri = R + (size_t)i * n, *rk = R + (size_t)k * n; for (int j = 0; j < n; j++) ri[j] |= rk[j]; }
  double tp = now() - t0; t0 = now();
  for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) if (B[(size_t)i * W + k / 64] >> (k % 64) & 1) { uint64_t *bi = B + (size_t)i * W, *bk = B + (size_t)k * W; for (int j = 0; j < W; j++) bi[j] |= bk[j]; }
  double tb = now() - t0;
  long ones = 0, agree = 1;
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { int x = R[(size_t)i * n + j], y = B[(size_t)i * W + j / 64] >> (j % 64) & 1; ones += x; if (x != y) agree = 0; }
  int *queue=malloc(4*n);unsigned char *seen=malloc(n);
  for(int src=0;src<n;src++){
    memset(seen,0,n);int begin=0,end=1;queue[0]=src;seen[src]=1;
    while(begin<end){int v=queue[begin++];for(int w=0;w<n;w++)if(G[(size_t)v*n+w]&&!seen[w]){seen[w]=1;queue[end++]=w;}}
    for(int j=0;j<n;j++)if(R[(size_t)src*n+j]!=seen[j])abort();
  }
  cs24_check(agree,"all_closure_pairs_bfs",(unsigned long long)n*n);
  free(G);free(queue);free(seen);
  /* LCS of two random strings over ACGT, length m */
  char *a = malloc(m), *b = malloc(m); for (int i = 0; i < m; i++) { a[i] = "ACGT"[rnd() & 3]; b[i] = "ACGT"[rnd() & 3]; }
  int *prev = calloc(m + 1, 4), *cur = calloc(m + 1, 4);
  t0 = now();
  for (int i = 0; i < m; i++) { for (int j = 1; j <= m; j++) cur[j] = a[i] == b[j - 1] ? prev[j - 1] + 1 : (prev[j] > cur[j - 1] ? prev[j] : cur[j - 1]); int *t = prev; prev = cur; cur = t; }
  double tl = now() - t0; int lcs1 = prev[m];
  int MW = (m + 63) / 64; uint64_t *M[4]; for (int c = 0; c < 4; c++) M[c] = calloc(MW, 8);
  for (int j = 0; j < m; j++) { int c = b[j] == 'A' ? 0 : b[j] == 'C' ? 1 : b[j] == 'G' ? 2 : 3; M[c][j / 64] |= 1ULL << (j % 64); }
  uint64_t *V = malloc(8 * MW); for (int w = 0; w < MW; w++) V[w] = ~0ULL; if (m % 64) V[MW - 1] = (1ULL << (m % 64)) - 1;
  t0 = now();
  for (int i = 0; i < m; i++) {
    int c = a[i] == 'A' ? 0 : a[i] == 'C' ? 1 : a[i] == 'G' ? 2 : 3; uint64_t *Mc = M[c]; unsigned carry = 0;
    for (int w = 0; w < MW; w++) { uint64_t U = V[w] & Mc[w]; uint64_t s = V[w] + U; unsigned c1 = s < V[w]; uint64_t s2 = s + carry; c1 |= s2 < s; carry = c1; V[w] = s2 | (V[w] & ~Mc[w]); }
  }
  if (m % 64) V[MW - 1] &= (1ULL << (m % 64)) - 1;
  double tbp = now() - t0; int z = 0; for (int w = 0; w < MW; w++) z += __builtin_popcountll(V[w]);
  cs24_check(lcs1==m-z,"LCS_full_DP_reference",(unsigned long long)m*m);
  printf("%.4f %.4f %ld %ld %.4f %.4f %d %d\n", tp, tb, ones, agree, tl, tbp, lcs1, m - z);
  return 0;
}
'''

TOKEN_C = r'''

/* Finding the words of the corpus: one byte at a time, against 32 bytes per AVX2 instruction. Counts words and
   letters, lower-casing in place. */
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  long cap = (sz + 128) / 64 * 64 + 64;
  uint8_t *src = aligned_alloc(64, cap), *t = aligned_alloc(64, cap); if (fread(src, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  memset(src + sz, 0, cap - sz);
  uint8_t *scalar=malloc(cap);uint32_t *starts_actual=malloc(4*((sz+31)/32));
  double bs = 1e9, bv = 1e9; long ws = 0, ls = 0, wv = 0, lv = 0;
  for (int rep = 0; rep < 5; rep++) {
    memcpy(t, src, cap);
    double t0 = now(); long words = 0, letters = 0; int in = 0;
    for (long i = 0; i < sz; i++) { uint8_t c = t[i]; if (c >= 'A' && c <= 'Z') { c += 32; t[i] = c; }
      int l = c >= 'a' && c <= 'z'; letters += l; words += l & !in; in = l; }
    double t1 = now(); if (t1 - t0 < bs) bs = t1 - t0; ws = words; ls = letters;memcpy(scalar,t,cap);
    memcpy(t, src, cap);
    t0 = now(); words = 0; letters = 0; uint32_t prev = 0;
    const __m256i x20 = _mm256_set1_epi8(0x20), xa = _mm256_set1_epi8('a'), x25 = _mm256_set1_epi8(25);
    for (long i = 0; i < sz; i += 32) {
      __m256i v = _mm256_load_si256((const __m256i *)(t + i)), lo = _mm256_or_si256(v, x20), d = _mm256_sub_epi8(lo, xa);
      __m256i isl = _mm256_cmpeq_epi8(_mm256_min_epu8(d, x25), d);
      _mm256_store_si256((__m256i *)(t + i), _mm256_blendv_epi8(v, lo, isl));
      uint32_t L = (uint32_t)_mm256_movemask_epi8(isl); if (sz - i < 32) L &= (1u << (sz - i)) - 1;
      starts_actual[i/32]=L & ~((L << 1) | (prev >> 31));
      letters += __builtin_popcount(L); words += __builtin_popcount(starts_actual[i/32]); prev = L;
    }
    t1 = now(); if (t1 - t0 < bv) bv = t1 - t0; wv = words; lv = letters;
    if(memcmp(scalar,t,sz))abort();
    for(long i=0;i<sz;i+=32){uint32_t expected=0;for(int j=0;j<32&&i+j<sz;j++){long k=i+j;int letter=t[k]>='a'&&t[k]<='z';int before=k&&t[k-1]>='a'&&t[k-1]<='z';if(letter&&!before)expected|=1u<<j;}if(expected!=starts_actual[i/32])abort();}
    cs24_check(ws==wv&&ls==lv,"all_token_bytes_and_start_masks",sz+(sz+31)/32);
  }
  printf("%ld %.5f %.5f %ld %ld %d\n", sz, bs, bv, ws, ls, ws == wv && ls == lv);
  return 0;
}
'''

BENCH_C = r'''

/* Benchmarking honestly: one fixed loop, timed inside the process; and a loop the compiler can delete. */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
__attribute__((noinline)) static double work(const float *x, int n, int reps) {
  double s = 0; for (int r = 0; r < reps; r++) for (int i = 0; i < n; i++) s += x[i] * x[(i * 7) & (n - 1)];
  return s;
}
int main(int argc, char **argv) {
  int mode = atoi(argv[1]);
  if (mode == 0) {                 /* one timing of the fixed workload, cold: the first and the later repetitions */
    int n = 1 << 16; float *x = malloc(4 * n); for (int i = 0; i < n; i++) x[i] = (float)(i % 97) / 97.0f;
    double t[6]; double s = 0;
    for (int k = 0; k < 6; k++) { double t0 = now(); s += work(x, n, 800); t[k] = now() - t0; }
    printf("%.6f %.6f %.6f %.6f %.6f %.6f %g\n", t[0], t[1], t[2], t[3], t[4], t[5], s);
  } else {                         /* dead code: the sum is never used, so -O2 deletes the loop */
    int n = 100000000; double t0 = now(); unsigned long s = 0; for (int i = 1; i <= n; i++) s += (unsigned long)i * i % 7;
    double t1 = now(); volatile unsigned long sink; unsigned long s2 = 0; for (int i = 1; i <= n; i++) s2 += (unsigned long)i * i % 7; sink = s2;
    double t2 = now(); (void)sink;
    cs24_check(sink==200000001ULL,"exact_period7_kept_sum",1);
    printf("%.6f %.6f\n", t1 - t0, t2 - t1);
  }
  return 0;
}
'''

JOB_ENG_C = r'''

/* The Job, engineered: an AVX2 tokenizer that classifies 32 bytes at a time, and a Swiss-table-style map whose
   16-byte groups of control bytes are searched with one SSE2 compare. */
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
#define CAP (1 << 17)            /* slots: 8,192 groups of 16 */
#define NG (CAP / 16)
typedef struct { uint64_t key8; uint32_t cnt; uint32_t info; } Slot;   /* info = length << 24 | entry */
static int8_t ctrl[CAP] __attribute__((aligned(64)));
static Slot slots[CAP] __attribute__((aligned(64)));
static uint32_t *es; static uint8_t *pool; static long used, ne;
static inline uint64_t mix(uint64_t h) { h ^= h >> 31; h *= 0x9E3779B97F4A7C15ULL; h ^= h >> 29; return h; }
static inline void count(const uint8_t *w, int n) {
  if(n<=0||n>255)abort();
  /* the first 8 letters as one word (the text is padded, so reading past the word is safe) */
  uint64_t k8; memcpy(&k8, w, 8); if (n < 8) k8 &= (~0ULL) >> (8 * (8 - n));
  uint64_t h = mix(k8 * 0xff51afd7ed558ccdULL + (uint64_t)n);
  if (n > 8) for (int i = 8; i < n; i += 8) { uint64_t x; memcpy(&x, w + i, 8); if (n - i < 8) x &= (~0ULL) >> (8 * (8 - (n - i))); h = mix(h ^ x); }
  int8_t h2 = (int8_t)(h >> 57);           /* 7 bits */
  uint32_t g = (uint32_t)h & (NG - 1);
  __m128i m = _mm_set1_epi8(h2), e = _mm_set1_epi8((char)0x80);
  for (;;) {
    __m128i c = _mm_load_si128((const __m128i *)&ctrl[g * 16]);
    unsigned hit = _mm_movemask_epi8(_mm_cmpeq_epi8(c, m));
    while (hit) {
      int j = __builtin_ctz(hit); Slot *s = &slots[g * 16 + j];
      if (s->key8 == k8 && (int)(s->info >> 24) == n && (n <= 8 || !memcmp(pool + es[s->info & 0xFFFFFF] + 8, w + 8, n - 8))) {
        s->cnt++; return; }
      hit &= hit - 1;
    }
    unsigned emp = _mm_movemask_epi8(_mm_cmpeq_epi8(c, e));
    if (emp) {
      int j = __builtin_ctz(emp); Slot *s = &slots[g * 16 + j];
      ctrl[g * 16 + j] = h2; s->key8 = k8; s->cnt = 1; s->info = (uint32_t)n << 24 | (uint32_t)ne;
      if(ne>=CAP-1||used+n>(1<<21))abort();
      es[ne] = used; memcpy(pool + used, w, n); used += n; ne++; return;
    }
    g = (g + 1) & (NG - 1);
  }
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  uint8_t *t = aligned_alloc(64, (sz + 128) / 64 * 64 + 64); if (fread(t, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  memset(t + sz, 0, (sz + 128) / 64 * 64 + 64 - sz);
  double t0 = now();
  memset(ctrl, 0x80, sizeof ctrl);
  es = malloc(4 << 17); pool = malloc(1 << 21);
  /* lower-case in place, 32 bytes at a time, and find letters: (c | 0x20) - 'a' < 26 */
  const __m256i x20 = _mm256_set1_epi8(0x20), xa = _mm256_set1_epi8('a'), x25 = _mm256_set1_epi8(25);
  long nwords = 0; long start = -1; uint32_t prev = 0;
  for (long i = 0; i < sz; i += 32) {
    __m256i v = _mm256_load_si256((const __m256i *)(t + i));
    __m256i lo = _mm256_or_si256(v, x20);
    __m256i d = _mm256_sub_epi8(lo, xa);
    __m256i isl = _mm256_cmpeq_epi8(_mm256_min_epu8(d, x25), d);   /* d <= 25, unsigned */
    _mm256_store_si256((__m256i *)(t + i), _mm256_blendv_epi8(v, lo, isl));
    uint32_t L = (uint32_t)_mm256_movemask_epi8(isl);
    if (i + 32 > sz) L &= (sz - i) >= 32 ? ~0u : ((1u << (sz - i)) - 1);
    /* word starts: a letter whose predecessor is not; word ends: a non-letter whose predecessor is a letter */
    uint32_t starts = L & ~((L << 1) | (prev >> 31));
    uint32_t ends = ~L & ((L << 1) | (prev >> 31));
    while (starts | ends) {
      int a = starts ? __builtin_ctz(starts) : 32, b = ends ? __builtin_ctz(ends) : 32;
      if (b < a) { count(t + start, (int)(i + b - start)); nwords++; ends &= ends - 1; start = -1; }
      else { start = i + a; starts &= starts - 1; }
    }
    prev = L;
  }
  if (start >= 0) { count(t + start, (int)(sz - start)); nwords++; }
  /* the top 20, ties by first appearance (entries are numbered in order of first appearance) */
  uint32_t *cnt = calloc(ne, 4); uint8_t *el = malloc(ne);
  for (long i = 0; i < CAP; i++) if (ctrl[i] != (int8_t)0x80) { cnt[slots[i].info & 0xFFFFFF] = slots[i].cnt; el[slots[i].info & 0xFFFFFF] = slots[i].info >> 24; }
  int shown=ne<20?(int)ne:20;int top[20]; uint32_t topc[20];
  for (int k = 0; k < shown; k++) { long best = -1, at = 0; for (long e = 0; e < ne; e++) if ((long)cnt[e] > best) { best = cnt[e]; at = e; }
    top[k] = at; topc[k] = cnt[at]; cnt[at] = 0; }
  double s = now() - t0;
  for (int k = 0; k < shown; k++) { fwrite(pool + es[top[k]], 1, el[top[k]], stderr); fprintf(stderr, " %u\n", topc[k]); }
  printf("%g %ld %ld\n", s, nwords, ne);
  return 0;
}
'''

LEARNED_C = r'''

/* Anchored greedy teaching fit, not the optimal PGM segmentation algorithm.
   Full lower-bound brackets are certified; any invalid predicted bracket falls
   back to a full search. This also covers floating-point fitting roundoff. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <limits.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static uint64_t rs=88172645463325252ULL;
static uint64_t rnd() { rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs; }
typedef struct { uint64_t k0; double slope; long p0,len; } Seg;
static long lb(const uint64_t *a,long lo,long hi,uint64_t x) { while(lo<hi){long m=lo+(hi-lo)/2;if(a[m]<x)lo=m+1;else hi=m;}return lo; }
static long ub(const uint64_t *a,long n,uint64_t x) { long lo=0,hi=n;while(lo<hi){long m=lo+(hi-lo)/2;if(a[m]<=x)lo=m+1;else hi=m;}return lo; }
static int bracket(const uint64_t *a,long n,long p,uint64_t q) { return p>=0&&p<=n&&(p==0||a[p-1]<q)&&(p==n||a[p]>=q); }
static long lookup(const uint64_t *a,long n,const Seg *s,const uint64_t *sk,long ns,int eps,uint64_t x,long *fallback) {
 if(!n||x<=a[0])return 0;if(x>a[n-1])return n;
 long g=ub(sk,ns,x)-1;if(g<0)g=0;
 long double pred=(long double)s[g].p0+(long double)s[g].slope*(long double)(x-s[g].k0);
 long p=!isfinite(pred)?s[g].p0:pred<=0?0:pred>=n?n:(long)pred;
 long lo=p>eps+1?p-eps-1:0,hi=p<n-eps-2?p+eps+2:n;
 if((lo>0&&a[lo-1]>=x)||(hi<n&&a[hi]<x)){(*fallback)++;return lb(a,0,n,x);}
 return lb(a,lo,hi,x);
}
static uint64_t *read_keys(const char *path,long *n) {
 FILE *f=fopen(path,"rb");if(!f)return NULL;if(fseek(f,0,SEEK_END))exit(2);long bytes=ftell(f);if(bytes<0||bytes%8)exit(2);*n=bytes/8;rewind(f);
 uint64_t *a=malloc(bytes?bytes:8);if(!a||fread(a,8,*n,f)!=(size_t)*n)exit(2);fclose(f);return a;
}
static void save(const char *name,const void *data,size_t bytes) {
 const char *dir=getenv("CS24_ARRAY_DIR");if(!dir)return;char path[4096];snprintf(path,sizeof path,"%s/%s",dir,name);FILE *f=fopen(path,"wb");if(!f||fwrite(data,1,bytes,f)!=bytes||fclose(f))exit(2);
}
int main(int argc,char **argv) {
 if(argc<3)return 2;long n;uint64_t *a=read_keys(argv[1],&n);if(!a)return 2;
 char *end;long ep=strtol(argv[2],&end,10);if(*end||ep<1||ep>INT_MAX/4)return 2;int eps=(int)ep;
 for(long i=1;i<n;i++)if(a[i]<=a[i-1])return 2;
 Seg *s=malloc(sizeof(Seg)*(n?n:1));if(!s)return 2;long ns=0;
 for(long i=0;i<n;) {
  long double lo=-INFINITY,hi=INFINITY;long j=i+1;
  for(;j<n;j++) {
   long double dx=(long double)(a[j]-a[i]),l=(j-i-(long double)eps)/dx,h=(j-i+(long double)eps)/dx;
   long double nl=fmaxl(lo,l),nh=fminl(hi,h);if(nl>nh)break;lo=nl;hi=nh;
  }
  s[ns]=(Seg){a[i],isfinite(lo)&&isfinite(hi)?(double)((lo+hi)/2):0,i,j-i};ns++;i=j;
 }
 size_t peak=(size_t)(n?n:1)*sizeof(Seg);
 size_t active=(size_t)(ns?ns:1)*sizeof(Seg)+(size_t)(ns?ns:1)*8;if(active>peak)peak=active;
 Seg *small=realloc(s,sizeof(Seg)*(ns?ns:1));if(!small)return 2;s=small;
 uint64_t *sk=malloc(8*(ns?ns:1));if(!sk)return 2;long double max_error=0;
 for(long g=0;g<ns;g++){
  sk[g]=s[g].k0;
  for(long j=s[g].p0;j<s[g].p0+s[g].len;j++){
   long double pred=s[g].p0+(long double)s[g].slope*(long double)(a[j]-s[g].k0);
   max_error=fmaxl(max_error,fabsl(pred-j));
  }
 }
 cs24_check(1,"stored_key_errors_evaluated",n);
 long Q=n?(1<<21):2;uint64_t *q;
 if(argc>3){q=read_keys(argv[3],&Q);if(!q)return 2;}
 else {q=malloc(8*Q);if(!q)return 2;for(long k=0;k<Q;k++){if(!n)q[k]=k?UINT64_MAX:0;else{uint64_t key=a[rnd()%n];q[k]=key==UINT64_MAX?key:key+(rnd()&1);}}}
 long *rb=malloc(sizeof(long)*(Q?Q:1)),*rl=malloc(sizeof(long)*(Q?Q:1));if(!rb||!rl)return 2;
 double best_b=1e9,best_l=1e9;long fallbacks=0;
 for(int rep=0;rep<3;rep++) {
  double t=now();for(long k=0;k<Q;k++)rb[k]=lb(a,0,n,q[k]);double tb=now()-t;
  long fallback=0;t=now();for(long k=0;k<Q;k++)rl[k]=lookup(a,n,s,sk,ns,eps,q[k],&fallback);double tl=now()-t;
  best_b=fmin(best_b,tb);best_l=fmin(best_l,tl);fallbacks=fallback;
  for(long k=0;k<Q;k++)if(!bracket(a,n,rb[k],q[k])||!bracket(a,n,rl[k],q[k]))return 3;
  cs24_check(1,"complete_lower_bound_certificates",2*(unsigned long long)Q);
 }
 save("queries.bin",q,8*Q);save("binary.bin",rb,sizeof(long)*Q);save("learned.bin",rl,sizeof(long)*Q);
 printf("%ld %d %ld %.3f %.3f 1 %zu %zu %zu %.12Lg %ld %ld\n",n,eps,ns,best_b*1e9/(Q?Q:1),best_l*1e9/(Q?Q:1),(size_t)ns*(sizeof(Seg)+8),peak,sizeof(Seg),max_error,fallbacks,Q);
 free(a);free(s);free(sk);free(q);free(rb);free(rl);return 0;
}
'''

BRANCHES_C = r'''

/* Branch prediction: sum the elements >= 128 of 2^24 random bytes, shuffled and sorted, with a branch and without. */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
static unsigned long long rs = 88172645463325252ULL;
static unsigned rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
__attribute__((noinline, optimize("no-if-conversion", "no-if-conversion2", "no-tree-vectorize")))
static long branchy(const int *a, int n) { long s = 0; for (int i = 0; i < n; i++) if (a[i] >= 128) s += a[i]; return s; }
__attribute__((noinline, optimize("no-tree-vectorize")))
static long branchless(const int *a, int n) { long s = 0; for (int i = 0; i < n; i++) { int m = -(a[i] >= 128); s += a[i] & m; } return s; }
int main() {
  int n = 1 << 24; int *a = malloc(4 * n), *b = malloc(4 * n);
  for (int i = 0; i < n; i++) a[i] = b[i] = rnd() & 255;
  qsort(b, n, 4, cmpi);
  double r[4] = {1e9, 1e9, 1e9, 1e9}; long s[4];
  for (int rep = 0; rep < 5; rep++) {
    double t = now(); s[0] = branchy(a, n); t = now() - t; if (t < r[0]) r[0] = t;
    t = now(); s[1] = branchy(b, n); t = now() - t; if (t < r[1]) r[1] = t;
    t = now(); s[2] = branchless(a, n); t = now() - t; if (t < r[2]) r[2] = t;
    t = now(); s[3] = branchless(b, n); t = now() - t; if (t < r[3]) r[3] = t;
    // A separate weighted histogram certifies all four actual outputs before overwrite.
    unsigned long counts_rep[256]={0};for(int i=0;i<n;i++)counts_rep[a[i]]++;
    long expected_rep=0;for(int v=128;v<256;v++)expected_rep+=(long)counts_rep[v]*v;
    cs24_check(s[0]==expected_rep&&s[1]==expected_rep&&s[2]==expected_rep&&s[3]==expected_rep,"every_trial_histogram_sum",4);
  }
  long expected=0;unsigned long counts[256]={0};for(int i=0;i<n;i++)counts[a[i]]++;
  for(int v=128;v<256;v++)expected+=(long)counts[v]*v;
  cs24_check(s[0]==expected&&s[1]==expected&&s[2]==expected&&s[3]==expected,"histogram_weighted_sum",4);
  printf("%.3f %.3f %.3f %.3f %d\n", r[0] * 1e9 / n, r[1] * 1e9 / n, r[2] * 1e9 / n, r[3] * 1e9 / n,
         s[0] == s[1] && s[1] == s[2] && s[2] == s[3]);
  return 0;
}
'''

VECTOR_C = r'''

/* Auto-vectorization: the same loops at -O1 (scalar) and at -O3 -march=native (vectorized), checked equal. */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static double now() { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }
__attribute__((noinline)) void saxpy(float *restrict y, const float *restrict x, float a, int n) { for (int i = 0; i < n; i++) y[i] = a * x[i] + y[i]; }
__attribute__((noinline)) long isum(const int *x, int n) { long s = 0; for (int i = 0; i < n; i++) s += x[i]; return s; }
__attribute__((noinline)) void prefix(int *x, int n) { for (int i = 1; i < n; i++) x[i] += x[i - 1]; }
int main() {
  int n = 1 << 16, reps = 4000; float *x = malloc(4 * n), *y = malloc(4 * n); int *v = malloc(4 * n), *w = malloc(4 * n);
  for (int i = 0; i < n; i++) { x[i] = (i % 13) * 0.25f; y[i] = 1.0f; v[i] = i % 97; }
  double t = now(); for (int r = 0; r < reps; r++) saxpy(y, x, 1e-4f, n); double ts = (now() - t) / reps / n;
  t = now(); long s = 0; for (int r = 0; r < reps; r++) { __asm__ volatile("" ::: "memory"); s += isum(v, n); } double ti = (now() - t) / reps / n;
  t = now(); for (int r = 0; r < reps / 10; r++) { for (int i = 0; i < n; i++) w[i] = v[i]; prefix(w, n); } double tp = (now() - t) / (reps / 10) / n;
  long expected_sum=0;int cumulative=0;
  for(int i=0;i<n;i++){
    float expected=1.0f;for(int r=0;r<reps;r++)expected=1e-4f*x[i]+expected;
    if(y[i]!=expected)abort();expected_sum+=i%97;cumulative+=i%97;if(w[i]!=cumulative)abort();
  }
  cs24_check(s==expected_sum*reps,"all_vector_elements_and_reductions",2ULL*n+1);
  double cs = 0; for (int i = 0; i < n; i++) cs += y[i];
  printf("%.4f %.4f %.4f %.6f %ld %d\n", ts * 1e9, ti * 1e9, tp * 1e9, cs, s, w[n - 1]);
  return 0;
}
'''

TOPK_CPP = r'''

// The top 20 of 2^24 random keys, four ways: full sort, partial_sort, nth_element then sort, and a 20-element heap.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <queue>
#include <vector>
using namespace std;
static double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
static uint64_t rs = 88172645463325252ULL;
static uint32_t rnd() { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (uint32_t)(rs >> 13); }
int main() {
  size_t n = 1u << 24; int k = 20; vector<uint32_t> src(n); for (auto &x : src) x = rnd();
  vector<uint32_t> reference;
  for(auto x:src){auto at=lower_bound(reference.begin(),reference.end(),x,greater<uint32_t>());reference.insert(at,x);if((int)reference.size()>k)reference.pop_back();}
  double best[4] = {1e9, 1e9, 1e9, 1e9}; vector<uint32_t> out[4];
  for (int rep = 0; rep < 3; rep++) {
    vector<uint32_t> a = src; double t = now(); sort(a.begin(), a.end(), greater<uint32_t>()); out[0].assign(a.begin(), a.begin() + k); best[0] = min(best[0], now() - t);
    a = src; t = now(); partial_sort(a.begin(), a.begin() + k, a.end(), greater<uint32_t>()); out[1].assign(a.begin(), a.begin() + k); best[1] = min(best[1], now() - t);
    a = src; t = now(); nth_element(a.begin(), a.begin() + k, a.end(), greater<uint32_t>()); sort(a.begin(), a.begin() + k, greater<uint32_t>()); out[2].assign(a.begin(), a.begin() + k); best[2] = min(best[2], now() - t);
    t = now(); priority_queue<uint32_t, vector<uint32_t>, greater<uint32_t>> h;
    for (auto x : src) { if ((int)h.size() < k) h.push(x); else if (x > h.top()) { h.pop(); h.push(x); } }
    vector<uint32_t> o; while (!h.empty()) { o.push_back(h.top()); h.pop(); } reverse(o.begin(), o.end()); out[3] = o; best[3] = min(best[3], now() - t);
    for(int z=0;z<4;z++)cs24_check(out[z]==reference,"complete_top20_insertion_reference",k);
  }
  printf("%.4f %.4f %.4f %.4f %d\n", best[0], best[1], best[2], best[3], out[0] == out[1] && out[1] == out[2] && out[2] == out[3]);
}
'''


ITEMS = {k[8:]: _producer(k[8:],v) for k, v in list(globals().items()) if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
