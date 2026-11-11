"""Precompute everything numerical in Part 27 of *Computer Science, Built* ("Proofs and Randomness").

    python -m videos.cs.cs27.compute              # everything missing
    python -m videos.cs.cs27.compute --force zk

Results are cached in ``.cache/cs27/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/proofs.py`` (tested in tests/test_cs27_proofs.py).

Items:
    amplify    majority-vote error against repetitions; Adleman's union bound in numbers
    equality   fingerprints: bits sent and the measured error, against n deterministic bits
    switching  random restrictions of a random 3-DNF: decision-tree depth against the switching-lemma bound
    gni        the graph non-isomorphism protocol: an honest prover always wins, a bluffer half the time
    sumcheck   an honest transcript for #SAT, and a cheating prover's survival against the bound
    zk         zero-knowledge 3-colouring: a cheater's survival by round; real against simulated transcripts
    blr        the linearity test's rejection probability against the distance from linear
    maxsat     random assignments against local search on MAX-3SAT
    vc         FPT vertex cover: search-tree nodes and Buss's kernel against brute force
    permanent  Ryser's permanent against Bareiss's determinant: time by n
    finegrained orthogonal vectors and 3SUM: quadratic time measured
    planted    planted clique in G(n, 1/2): how often the degree heuristic recovers it, by clique size
    oneway     multiplying two primes against factoring the product with Pollard's rho, by size
    unique     unique games with a planted labelling and an eps fraction of corrupted edges: propagation's value
    pit        Schwartz--Zippel on the Vandermonde identity: a true identity always passes, a false one rarely
    williams   Williams' reduction: random 3-SAT on 24 variables as orthogonal vectors, against the CDCL answer
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import platform
import sys
from pathlib import Path
import math
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item
from . import computational_references as R
from explainer.cs.algo import proofs as P
from explainer.cs.algo import complexity as X

SOURCE_FILES=tuple(Path(p) for p in (__file__,P.__file__,X.__file__,R.__file__,
    str(Path(__file__).with_name('reference_native.cpp')),'explainer/ai/cache.py','explainer/cache_lock.py','pyproject.toml'))
def source_signature():
    return {str(p.resolve().relative_to(Path.cwd())):R.digest(p.read_bytes()) for p in SOURCE_FILES}
def cache_current(name,path=None):
    try:
        d=json.loads((CACHE.path(name) if path is None else Path(path)).read_text())
        return d.get('schema')==2 and d.get('source_sha256')==source_signature() and all(
            Path(a['path']).is_file() and R.digest(Path(a['path']).read_bytes())==a['sha256'] for a in d['artifacts'])
    except (OSError,ValueError,KeyError):return False
class ProofCache(Cache):
    @locked_item(lambda self,name:self.path(name))
    def load(self,name):
        if not cache_current(name): self.save(name,ITEMS[name]())
        return super().load(name)
    def main(self,items,doc=None):
        parser=argparse.ArgumentParser(description=doc);parser.add_argument('names',nargs='*',default=list(items));parser.add_argument('--force',action='store_true');a=parser.parse_args()
        if any(n not in items for n in a.names):parser.error('unknown producer')
        for name in a.names:
            with cache_lock(self.path(name)):
                if not a.force and cache_current(name):print('  cached',name,flush=True);continue
                start=time.monotonic();print('  compute',name,flush=True)
                self.save(name,items[name]());print('  done',name,f'{time.monotonic()-start:.3f}s',flush=True)
CACHE=ProofCache('cs27')
load=CACHE.load
CURRENT=None

def _producer(name,fn):
    @functools.wraps(fn)
    def run():
        global CURRENT
        assert CURRENT is None
        before=source_signature();started=time.time_ns()
        with R.Recorder(P,X) as recorder:
            CURRENT=recorder
            try:data=fn()
            finally:CURRENT=None
        evidence=recorder.evidence()
        if '_evidence' in data:evidence['producer_witnesses']=data.pop('_evidence')
        # Original wall-clock spans include logging overhead; display only the
        # recorded teaching-call intervals, never serialization or validation.
        if name=='pit':
            for row in data['rows']:
                times=[c['elapsed_ns']/1e9 for c in evidence['calls'] if c['fn']=='P.vandermonde_test'
                       and evidence['objects'][c['input']]['args'][1]==row['p']
                       and not evidence['objects'][c['input']]['kwargs'].get('wrong',False)]
                row['seconds']=statistics.mean(times);row['raw_seconds']=times
        if name=='williams':
            for row,build,search in zip(data['rows'],recorder.times('P.sat_to_ov'),recorder.times('P.ov_brute')):
                row['build_s']=build;row['ov_s']=search
        raw=R.artifact(f'{name}-{started}-raw.json.gz',evidence)
        try:
            check=R.validate_recording(name,evidence)
        except BaseException as exc:
            evidence['validation_failure']=dict(type=type(exc).__name__,message=str(exc))
            R.artifact(f'{name}-{started}-failed-check.json.gz',evidence)
            raise
        saved=R.artifact(f'{name}-{started}-checked.json.gz',evidence)
        assert before==source_signature()
        data.update(schema=2,item=name,source_sha256=before,artifacts=[raw,saved],validation=check,
                    provenance=dict(started_utc_ns=started,finished_utc_ns=time.time_ns(),python=sys.version,
                        platform=platform.platform(),rng='seeded random.Random, noncryptographic teaching experiments',
                        timing='Teaching call intervals; full serialization and independent checks excluded. Host-specific finite measurements.'))
        return data
    return run

WEB = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, 2, 3]]


def compute_amplify() -> dict:
    rows = []
    for k in (1, 3, 5, 11, 21, 51, 101, 201):
        rows.append({"k": k, "error": P.binom_tail(k, 1 / 3, k // 2 + 1)})
    adl = []
    for n in (10, 20, 50, 100):
        k = 1
        while P.binom_tail(k, 1 / 3, k // 2 + 1) >= 2.0 ** -(n + 1):
            k += 2
        adl.append({"n": n, "runs": k, "error": P.binom_tail(k, 1 / 3, k // 2 + 1),
                    "union": 2.0 ** n * P.binom_tail(k, 1 / 3, k // 2 + 1)})
    return {"rows": rows, "adleman": adl}


def compute_equality() -> dict:
    rng = random.Random(1)
    n = 1000
    q = P.next_prime(n * n)
    x = [rng.randrange(2) for _ in range(n)]
    y = x[:]
    y[rng.randrange(n)] ^= 1
    trials = 20000
    wrong = sum(P.fingerprint_eq(x, y, q, rng)[0] for _ in range(trials))
    small_q = P.next_prime(2 * n)
    wrong_small = sum(P.fingerprint_eq(x, y, small_q, rng)[0] for _ in range(trials))
    rows = []
    for e in (3, 6, 9, 12):
        nn = 10 ** e
        bits = 2 * (2 * math.ceil(math.log2(nn)) + 1)
        rows.append({"n": nn, "det_bits": nn, "rand_bits": bits})
    return {"n": n, "q": q, "trials": trials, "wrong": wrong, "bound": n / q, "small_q": small_q,
            "wrong_small": wrong_small, "bound_small": n / small_q, "rows": rows}


def compute_switching() -> dict:
    rng = random.Random(2)
    n, terms, width = 14, 20, 3
    f = P.dnf_random(n, terms, width, rng)
    rows = []
    for p in (0.02, 0.04, 0.066, 0.1, 0.2):
        hist = {}
        trials = 1500
        for _ in range(trials):
            rho = P.random_restriction(n, p, rng)
            g = P.restrict(f, rho)
            free = [v for v in range(n) if v not in rho]
            d = P.dt_depth(P.truth_table(g, free), len(free))
            hist[d] = hist.get(d, 0) + 1
        ge = {s: sum(c for d, c in hist.items() if d >= s) / trials for s in (1, 2, 3)}
        rows.append({"p": p, "hist": {str(k): v for k, v in sorted(hist.items())}, "ge": ge,
                     "bound": {s: min(1.0, (5 * p * width) ** s) for s in (1, 2, 3)}})
    # one restriction to draw
    rho = P.random_restriction(n, 0.2, random.Random(11))
    g = P.restrict(f, rho)
    ex = {"rho": {str(k): v for k, v in rho.items()},
          "after": [[[v, b] for v, b in t] for t in g] if isinstance(g, list) else g}
    return {"n": n, "terms": terms, "width": width, "dnf": [[[v, b] for v, b in t] for t in f], "rows": rows,
            "example": ex}


def compute_gni() -> dict:
    rng = random.Random(3)
    G0 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]                   # a 5-cycle
    G1 = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]                   # a triangle with a tail
    G2 = [(0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]                   # another 5-cycle
    honest = [P.gni_round(G0, G1, 5, rng) for _ in range(200)]
    bluff = [P.gni_round(G0, G2, 5, rng) for _ in range(2000)]
    rate = sum(a == b for b, a in bluff) / len(bluff)
    return {"G0": G0, "G1": G1, "G2": G2, "honest_rate": sum(a == b for b, a in honest) / len(honest),
            "bluff_rate": rate, "after_k": [{"k": k, "survive": 0.5 ** k} for k in (1, 5, 10, 20)]}


def compute_sumcheck() -> dict:
    rng = random.Random(4)
    n, p = 4, 97
    true = P.count_sat(WEB, n)
    ok, _, log = P.sumcheck(WEB, n, p, true, rng)
    trials = 3000
    surv = sum(P.sumcheck(WEB, n, p, true + 1, rng, cheat=True)[0] for _ in range(trials)) / trials
    deg = len(WEB)
    bound = 1 - (1 - deg / p) ** n
    big = P.next_prime(10 ** 6)
    surv_big = sum(P.sumcheck(WEB, n, big, true + 1, rng, cheat=True)[0] for _ in range(300)) / 300
    return {"n": n, "p": p, "clauses": WEB, "true": true, "honest_ok": ok, "log": log, "trials": trials,
            "cheat_survive": surv, "bound": bound, "big_p": big, "cheat_survive_big": surv_big,
            "big_bound": 1 - (1 - deg / big) ** n}


def compute_zk() -> dict:
    rng = random.Random(5)
    # the Petersen graph is 3-colourable
    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    spokes = [(i, 5 + i) for i in range(5)]
    edges = outer + inner + spokes
    V = list(range(10))
    nv, cl, var = X.coloring_cnf(V, edges, 3)
    model, _ = X.cdcl(nv, cl)
    col = [next(c for c in range(3) if model[var(v, c)]) for v in V]
    m = len(edges)
    bad = col[:]
    u, v = edges[0]
    bad[v] = bad[u]
    nbad = sum(1 for a, b in edges if bad[a] == bad[b])
    trials = 2000
    caught_at = [P.zk_colouring(10, edges, bad, 200, rng)[0] for _ in range(trials)]
    surv = []
    for k in (1, 5, 10, 20, 50, 100):
        emp = sum(1 for c in caught_at if c is None or c > k) / trials
        surv.append({"k": k, "empirical": emp, "theory": (1 - nbad / m) ** k})
    _, real = P.zk_colouring(10, edges, col, 6000, rng)
    sim = P.zk_simulate(6000, rng)
    pairs = [(a, b) for a in range(3) for b in range(3) if a != b]
    dist = {"real": [sum(1 for r in real if r == pr) / len(real) for pr in pairs],
            "sim": [sum(1 for r in sim if r == pr) / len(sim) for pr in pairs], "pairs": pairs}
    return {"edges": edges, "colouring": col, "bad": bad, "m": m, "bad_edges": nbad, "survive": surv,
            "dist": dist, "rounds_for_1e9": math.ceil(math.log(1e-9) / math.log(1 - 1 / m))}


def compute_blr() -> dict:
    rng = random.Random(6)
    n = 8
    N = 1 << n
    a = 0b10110101
    lin = [bin(a & x).count("1") & 1 for x in range(N)]
    rows = []
    for t in (0, 4, 8, 16, 32, 48, 64, 96, 128):
        for _ in range(2 if t else 1):
            f = lin[:]
            for x in rng.sample(range(N), t):
                f[x] ^= 1
            d = P.distance_to_linear(f, n)
            rows.append({"flipped": t, "distance": d, "reject": P.blr_rejection(f, n)})
    return {"n": n, "rows": rows}


def compute_maxsat() -> dict:
    rng=random.Random(7);rows=[];witnesses=[]
    for ratio in (4.0,5.0,6.0,8.0):
        n=100;m=int(ratio*n);rnd=[];ws=[]
        for trial in range(5):
            cl=X.random_ksat(n,m,3,rng);assignments=[]
            for _ in range(20):
                a=[False]+[rng.random()<0.5 for _ in range(n)]
                count=sum(any(a[abs(l)]==(l>0) for l in c) for c in cl)
                assignments.append(dict(model=a,satisfied=count));rnd.append(count/m)
            best,model=P.walksat(n,cl,rng,flips=4000);ws.append(best/m)
            witnesses.append(dict(ratio=ratio,trial=trial,n=n,clauses=cl,random_assignments=assignments,walksat_model=model,walksat_satisfied=best))
        rows.append(dict(ratio=ratio,random=statistics.mean(rnd),walksat=statistics.mean(ws)))
    return dict(rows=rows,_evidence=witnesses)


def compute_vc() -> dict:
    rng=random.Random(8);rows=[];witnesses=[];n=40
    for k in (4,6,8,10,12):
        planted=rng.sample(range(n),k);others=[v for v in range(n) if v not in planted];edges=set()
        for v in others:
            for u in rng.sample(planted,min(2,k)):edges.add(tuple(sorted((u,v))))
        for u,w in itertools.combinations(planted,2):
            if rng.random()<0.3:edges.add(tuple(sorted((u,w))))
        edges=sorted(edges);covers=[];seconds=[];counts=[]
        for _ in range(30):
            c,nodes=P.vc_branch(edges,k);covers.append(c);counts.append(nodes);seconds.append(CURRENT.times('P.vc_branch')[-1])
        assert len(set(counts))==1
        ker=P.buss_kernel(edges,k)
        rows.append(dict(k=k,edges=len(edges),found=c is not None,nodes=nodes,bound=2**(k+1)-1,seconds=statistics.median(seconds),raw_seconds=seconds,brute_subsets=math.comb(n,k),kernel_edges=len(ker[1]) if ker else None,forced=len(ker[0]) if ker else None))
        witnesses.append(dict(n=n,k=k,edges=edges,planted_cover=planted,covers=covers,kernel=ker))
    return dict(n=n,rows=rows,_evidence=witnesses)


def compute_permanent() -> dict:
    rng=random.Random(9);rows=[];big=[]
    for n in (8,10,12,14,16,18,20):
        A=[[rng.randrange(2) for _ in range(n)] for _ in range(n)];perms=[];dets=[];pt=[];dt=[]
        for _ in range(30):
            perms.append(P.permanent_ryser(A));pt.append(CURRENT.times('P.permanent_ryser')[-1])
            dets.append(P.det_bareiss(A));dt.append(CURRENT.times('P.det_bareiss')[-1])
        assert len(set(perms))==len(set(dets))==1
        rows.append(dict(n=n,perm=perms[0],perm_s=statistics.median(pt),det=dets[0],det_s=statistics.median(dt),perm_raw_seconds=pt,det_raw_seconds=dt))
    for n in (50,100,200):
        A=[[rng.randrange(2) for _ in range(n)] for _ in range(n)];dets=[];dt=[]
        for _ in range(30):dets.append(P.det_bareiss(A));dt.append(CURRENT.times('P.det_bareiss')[-1])
        assert len(set(dets))==1
        big.append(dict(n=n,det=dets[0],det_s=statistics.median(dt),raw_seconds=dt))
    return dict(rows=rows,det_big=big)


def compute_finegrained() -> dict:
    rng=random.Random(10);ov=[];ts=[]
    for n in (500,1000,2000,4000):
        A=[rng.getrandbits(64)|(1<<63) for _ in range(n)];B=[rng.getrandbits(64)|(1<<63) for _ in range(n)]
        xs=[rng.randrange(-10**9,10**9)|1 for _ in range(n)];ot=[];tt=[]
        for _ in range(30):
            answer=P.ov_brute(A,B);ot.append(CURRENT.times('P.ov_brute')[-1]);assert not answer
            triple=P.three_sum(xs);tt.append(CURRENT.times('P.three_sum')[-1]);assert triple is None
        ov.append(dict(n=n,seconds=statistics.median(ot),raw_seconds=ot,answer=False,negative_certificate='all vectors share bit 63'))
        ts.append(dict(n=n,seconds=statistics.median(tt),raw_seconds=tt,found=False,negative_certificate='sum of three odd integers is odd, hence nonzero'))
    return dict(ov=ov,three_sum=ts)


def compute_planted() -> dict:
    n, trials = 1000, 20
    rows = []
    for k in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120):
        ok = 0
        for s in range(trials):
            adj, S = P.planted_clique(n, k, random.Random(1000 * k + s))
            ok += P.degree_recover(adj, k) == S
        rows.append({"k": k, "rate": ok / trials})
    return {"n": n, "trials": trials, "rows": rows, "sqrt_nlogn": math.sqrt(n * math.log(n)),
            "two_log": 2 * math.log2(n)}


def compute_oneway() -> dict:
    rows=[];witnesses=[]
    for bits in (24,32,40,48,56,64,72,80):
        mul=[];fac=[];steps=[];actual_bits=[]
        for seed in range(5):
            rng=random.Random(100*bits+seed)
            p=P.next_prime(rng.getrandbits(bits//2)|(1<<(bits//2-1)));q=P.next_prime(rng.getrandbits(bits//2)|(1<<(bits//2-1)))
            start=time.perf_counter_ns()
            for _ in range(1000):N=p*q
            multiplication_ns=time.perf_counter_ns()-start;mul.append(multiplication_ns/1e12)
            factor,count=P.pollard_rho(N,random.Random(seed));fac.append(CURRENT.times('P.pollard_rho')[-1]);steps.append(count);actual_bits.append(N.bit_length())
            assert factor is not None and 1<factor<N and N%factor==0
            witnesses.append(dict(requested_bits=bits,seed=seed,p=p,q=q,N=N,actual_bits=N.bit_length(),factor=factor,steps=count,multiplication_batch_ns=multiplication_ns,batch_operations=1000,factor_seconds=fac[-1]))
        rows.append(dict(bits=bits,actual_bits=actual_bits,mul_s=statistics.median(mul),factor_s=statistics.median(fac),steps=statistics.median(steps),mul_raw_seconds=mul,factor_raw_seconds=fac,raw_steps=steps))
    return dict(rows=rows,_evidence=witnesses)


def compute_unique() -> dict:
    n, m, k = 3000, 9000, 7
    rows = []
    for eps in (0.0, 0.01, 0.03, 0.05, 0.1, 0.2):
        edges, planted = P.ug_instance(n, m, k, eps, random.Random(5))
        roots = random.Random(1).sample(range(n), 10)
        best = max(P.ug_value(edges, P.ug_propagate(n, edges, k, r), k) for r in roots)
        random_values=[]
        for seed in range(5):
            trial_rng=random.Random(seed)
            labels=[trial_rng.randrange(k) for _ in range(n)]
            random_values.append(P.ug_value(edges,labels,k))
        rnd=statistics.mean(random_values)
        rows.append({"eps": eps, "planted": P.ug_value(edges, planted, k), "propagate": best, "random": rnd})
    return {"n": n, "m": m, "k": k, "rows": rows}


def compute_williams() -> dict:
    n, m = 24, 101
    rows = []
    for s in range(6):
        cl = X.random_ksat(n, m, 3, random.Random(700 + s))
        t = time.perf_counter()
        A, B = P.sat_to_ov(cl, n)
        tb = time.perf_counter() - t
        t = time.perf_counter()
        ov = P.ov_brute(A, B)
        to = time.perf_counter() - t
        model, st = X.cdcl(n, cl)
        rows.append({"seed": 700 + s, "build_s": tb, "ov_s": to, "ov": ov, "sat": model is not None,
                     "conflicts": st.get("conflicts")})
    return {"n": n, "m": m, "N": 1 << (n // 2), "rows": rows}


def compute_pit() -> dict:
    n, trials = 10, 5000
    rows = []
    for p in (101, 1009, 10007, 1000003):
        rng = random.Random(p)
        t = time.perf_counter()
        good = sum(P.vandermonde_test([rng.randrange(p) for _ in range(n)], p) for _ in range(trials))
        dt = (time.perf_counter() - t) / trials
        bad = sum(P.vandermonde_test([rng.randrange(p) for _ in range(n)], p, wrong=True) for _ in range(trials))
        rows.append({"p": p, "true_pass": good / trials, "false_pass": bad / trials, "bound": n * (n - 1) / 2 / p,
                     "seconds": dt})
    return {"n": n, "trials": trials, "terms": math.factorial(n), "degree": n * (n - 1) // 2, "rows": rows}


def _fs_challenge(statement,history,p):
    import hashlib
    payload=b'CS27-SUMCHECK-FS-TEACHING-v1\0'+json.dumps(dict(statement=statement,history=history),sort_keys=True,separators=(',',':')).encode()
    limit=(1<<256)//p*p
    for counter in itertools.count():
        raw=hashlib.sha256(payload+counter.to_bytes(8,'big')).digest();value=int.from_bytes(raw,'big')
        if value<limit:return value%p,dict(counter=counter,digest=raw.hex())

def _fs_verify(statement,proof):
    try:
        n=statement['n'];p=statement['p'];clauses=statement['clauses'];cur=statement['claim']%p;history=[];prefix=[]
        if n!=20 or not P.is_prime(p) or statement['degree_bound']!=1 or len(proof)!=n:return False
        if any(sum(abs(l)==v for c in clauses for l in c)>1 for v in range(1,n+1)):return False
        for message in proof:
            if len(message)!=2 or any(type(v) is not int or not 0<=v<p for v in message):return False
            if sum(message)%p!=cur:return False
            history.append(dict(message=message))
            r,_=_fs_challenge(statement,history,p);cur=(message[0]+r*(message[1]-message[0]))%p
            history[-1]['challenge']=r;prefix.append(r)
        return cur==P.arith_eval(clauses,prefix,p)
    except (ValueError,TypeError,KeyError,IndexError):return False

def compute_fiat_shamir() -> dict:
    import copy
    n=20;p=(1<<61)-1;clauses=[[i,i+1] for i in range(1,n+1,2)]
    statement=dict(n=n,p=p,clauses=clauses,claim=3**10,degree_bound=1)
    def suffix_sum(prefix):
        # This intentionally structured example factors over ten disjoint pairs.
        product=1
        for a,b in clauses:
            if b<=len(prefix):value=prefix[a-1]+prefix[b-1]-prefix[a-1]*prefix[b-1]
            elif a<=len(prefix):value=1+prefix[a-1]
            else:value=3
            product=product*value%p
        return product
    prefix=[];proof=[];history=[];rounds=[];cur=statement['claim']
    for i in range(n):
        message=[suffix_sum(prefix+[v]) for v in (0,1)];assert sum(message)%p==cur
        history.append(dict(message=message));r,hash_record=_fs_challenge(statement,history,p)
        cur=(message[0]+r*(message[1]-message[0]))%p;history[-1]['challenge']=r;prefix.append(r);proof.append(message)
        rounds.append(dict(round=i+1,message=message,r=r,next=cur,hash=hash_record))
    cases=[]
    def test(label,st,pr):cases.append(dict(label=label,statement=st,proof=pr,accepted=_fs_verify(st,pr)))
    test('honest structured 20-variable instance',copy.deepcopy(statement),copy.deepcopy(proof))
    st=copy.deepcopy(statement);st['claim']+=1;test('altered count claim',st,copy.deepcopy(proof))
    pr=copy.deepcopy(proof);pr[0][0]=(pr[0][0]+1)%p;test('altered message',copy.deepcopy(statement),pr)
    st=copy.deepcopy(statement);st['clauses'][0][0]*=-1;test('altered statement formula',st,copy.deepcopy(proof))
    test('truncated proof',copy.deepcopy(statement),copy.deepcopy(proof[:-1]))
    pr=copy.deepcopy(proof);pr[0].append(0);test('oversized degree message',copy.deepcopy(statement),pr)
    assert cases[0]['accepted'] and not any(c['accepted'] for c in cases[1:])
    return dict(n=n,clauses=10,true=3**10,p=p,rounds=n,scope='A structured factorable teaching example with transcript-bound hash challenges and six actual mutation checks. No generic Fiat-Shamir security theorem, succinctness claim or deployed proof system.',_evidence=dict(statement=statement,proof=proof,rounds=rounds,cases=cases,challenge_domain='CS27-SUMCHECK-FS-TEACHING-v1 with NUL terminator; canonical JSON; SHA-256 rejection sampling'))

def compute_blr_minima() -> dict:
    records=[];best={};N=16
    for mask in range(1<<N):
        table=[mask>>x&1 for x in range(N)];spectrum=R.fourier(table,4)
        distance=(N-max(spectrum))//2;bad=(N**3-sum(c**3 for c in spectrum))//(2*N)
        records.append([mask,distance,bad])
        if distance not in best or bad<best[distance]['bad_pairs']:
            best[distance]=dict(distance_numerator=distance,distance=distance/N,bad_pairs=bad,rejection=bad/N**2,witness=mask)
    return dict(n=4,functions=len(records),rows=[best[k] for k in sorted(best)],_evidence=dict(records=records,rows=[best[k] for k in sorted(best)]))

ITEMS = {k[8:]: _producer(k[8:],v) for k,v in list(globals().items()) if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
