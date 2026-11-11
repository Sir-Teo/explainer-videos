"""Precompute everything numerical in Part 26 of *Computer Science, Built* ("P versus NP").

    python -m videos.cs.cs26.compute              # everything missing
    python -m videos.cs.cs26.compute --force web

Results are cached in ``.cache/cs26/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/complexity.py`` (tested in tests/test_cs26_complexity.py).

Items:
    hook       finding against checking: a planted 3-colourable graph of 60 vertices, solved by CDCL and checked
    growth     n^2, n^3, 2^n and n! at a microsecond a step
    savitch    CANYIELD by midpoint recursion on paths: calls and depth against BFS's visited set
    tableau    Cook-Levin tableaux for a tiny NTM: variables and clauses against the time bound; a decoded run
    web        one 3-SAT formula through the reductions: independent set, clique, vertex cover, 3-colouring, subset sum
    phase      the random 3-SAT phase transition with our solver: P(satisfiable) and median conflicts by ratio
    solvers    DPLL against CDCL at the threshold, by n
    selfreduce a satisfying assignment found with yes/no questions only
    knapsack   pseudo-polynomial subset-sum DP against the number of digits; meet in the middle for comparison
    pratt      a Pratt certificate for 2^61 - 1, and a factoring certificate
    games      TQBF evaluation and generalized geography: positions evaluated
    famous     Schur numbers S(3) = 13 and S(4) = 44 by our solver; Pythagorean triples colourable up to n
    formulas   exact literal-leaf De Morgan formula sizes of all 256 three-input functions (parity needs 10)
    sudoku     the complete 729-variable encoding, model and checked solution of the exercise puzzle
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import math
import platform
import random
import statistics
import sys
import time
from pathlib import Path

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item
from explainer.cs.algo import complexity as X
from . import computational_references as R

SOURCE_FILES = tuple(Path(p) for p in (
    __file__, X.__file__, R.__file__, 'explainer/ai/cache.py', 'explainer/cache_lock.py', 'pyproject.toml'))


def source_signature():
    return {str(p.resolve().relative_to(Path.cwd())): R.digest(p.read_bytes()) for p in SOURCE_FILES}


def cache_current(name, path=None):
    try:
        data = json.loads((CACHE.path(name) if path is None else Path(path)).read_text())
        return (data.get('schema') == 2 and data.get('source_sha256') == source_signature()
                and all(Path(a['path']).is_file() and R.digest(Path(a['path']).read_bytes()) == a['sha256']
                        for a in data['artifacts']))
    except (OSError, ValueError, KeyError):
        return False


class ComplexityCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not cache_current(name):
            self.save(name, ITEMS[name]())
        return super().load(name)

    def main(self, items, doc=None):
        parser = argparse.ArgumentParser(description=doc)
        parser.add_argument('names', nargs='*', default=list(items))
        parser.add_argument('--force', action='store_true')
        args = parser.parse_args()
        if any(name not in items for name in args.names):
            parser.error('unknown producer')
        self.items = items
        for name in args.names:
            with cache_lock(self.path(name)):
                if not args.force and cache_current(name):
                    print('  cached ', name, flush=True)
                    continue
                start = time.monotonic()
                print('  compute', name, flush=True)
                self.save(name, items[name]())
                print('  done   ', name, f'{time.monotonic()-start:.3f}s', flush=True)


CACHE = ComplexityCache("cs26")
load = CACHE.load
_calls = None


def solve(n, clauses, *, proof=False, **options):
    """Retain every actual solver query and distinguish unknown from UNSAT."""
    clauses = [list(c) for c in clauses]
    start = time.perf_counter()
    model, stats = X.cdcl(n, clauses, **options)
    stats['teaching_seconds'] = time.perf_counter() - start
    row = dict(n=n, clauses=clauses, model=model, stats=stats, options=options)
    assert _calls is not None, 'solver calls must occur inside a provenance-wrapped producer'
    _calls.append(row)
    if model is not None:
        assert stats['status'] == 'sat' and R.model_satisfies(n, clauses, model)
    if stats['status'] != 'unknown':
        row['reference'] = R.reference_sat(n, clauses, stats['status'], proof=proof)
        if proof and stats['status'] == 'unsat':
            row['reference']['proof_check'] = R.check_rup(clauses, row['reference']['drup_proof'])
    else:
        row['reference'] = dict(status='not-classified', reason='teaching solver exhausted its explicit budget')
    return model, stats


def _producer(name, fn):
    @functools.wraps(fn)
    def run():
        global _calls
        assert _calls is None
        before = source_signature()
        start = time.monotonic_ns()
        _calls = []
        try:
            data = fn()
            calls = _calls
        except Exception as exc:
            R.artifact(f'{name}/failed-queries-{time.time_ns()}.json.gz',
                       dict(source_sha256=before, error=repr(exc), queries=_calls))
            raise
        finally:
            _calls = None
        assert source_signature() == before, 'numerical sources changed during computation'
        raw = R.artifact(f'{name}/full-solver-queries.json.gz', calls)
        artifacts = data.pop('artifacts', []) + [raw]
        data.update(schema=2, source_sha256=before, artifacts=artifacts,
                    elapsed_ns=time.monotonic_ns()-start, host=platform.platform(), python_version=sys.version,
                    solver_queries=len(calls), scope='Actual retained finite computation; host timings are not benchmark guarantees. Unknown is never a refutation.')
        return data
    return run

WEB = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, 2, 3]]


def compute_hook() -> dict:
    rng = random.Random(26)
    n, p = 60, 0.12
    col = [rng.randrange(3) for _ in range(n)]
    edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if col[u] != col[v] and rng.random() < p]
    V = list(range(n))
    nv, cl, var = X.coloring_cnf(V, edges, 3)
    t = time.perf_counter()
    model, st = solve(nv, cl)
    t_find = st['teaching_seconds']
    c = X.decode_coloring(V, model, var, 3)
    t = time.perf_counter()
    for _ in range(1000):
        ok = all(c[u] != c[v] for u, v in edges)
    t_check = (time.perf_counter() - t) / 1000
    assert ok and all(c[u] != c[v] for u, v in edges)
    brute_years = 3 ** n * t_check / (3600 * 24 * 365.25)
    return {"n": n, "edges": len(edges), "find_s": t_find, "check_s": t_check, "ok": ok,
            "conflicts": st["conflicts"], "decisions": st["decisions"], "brute_years": brute_years,
            "colouring": [c[v] for v in V], "planted_colouring": col, "edge_list": edges,
            "seed": 26, "edge_probability_between_different_planted_colours": p,
            "enumeration_scenario": '3^60 times mean valid-colouring check, not a measured search or lower bound'}


def compute_growth() -> dict:
    rows = []
    for n in (10, 20, 30, 40, 50, 60, 100):
        counts = dict(n2=n*n, n3=n*n*n, **{'2n': 1 << n, 'fact': math.prod(range(1, n+1))})
        assert counts['fact'] == math.factorial(n)
        rows.append({"n": n, **{k: v*1e-6 for k,v in counts.items()}, "exact_operation_counts": counts})
    return {"rows": rows, "age_universe_s": 13.8e9 * 365.25 * 24 * 3600}


def compute_savitch() -> dict:
    rows = []
    for n in (4, 8, 16):
        adj = {i: {i + 1} for i in range(n - 1)}
        adj[n - 1] = set()
        t = time.perf_counter()
        ok, calls, depth = X.savitch(adj, 0, n - 1, n)
        reference, layers = R.reachability(adj, 0, n-1, n)
        assert ok == reference
        rows.append({"n": n, "ok": ok, "calls": calls, "depth": depth, "bfs_memory": n,
                     "savitch_memory": depth * 3, "seconds": time.perf_counter() - t,
                     "adjacency": {str(v): sorted(us) for v,us in adj.items()}, "reference_layers": layers})
    return {"rows": rows, "memory_scope": 'Three illustrative configuration slots per depth; excludes stored input, iterators and interpreter overhead.'}


NTM = {"states": ["q", "a"], "start": "q", "accept": "a", "blank": "_", "alphabet": ["0", "1", "_"],
       "delta": {("q", "0"): [("q", "0", 1)], ("q", "1"): [("q", "1", 1), ("a", "1", 1)]}}


def compute_tableau() -> dict:
    rows, witnesses = [], []
    for k in range(2, 9):
        w = "0" * (k - 1) + "1"
        T = k + 2
        nv, cl, info = X.cook_levin(NTM, w, T)
        t = time.perf_counter()
        model, st = solve(nv, cl)
        tab = X.decode_tableau(model, info) if model is not None else None
        certificate = R.tableau_certificate(NTM, w, T, tab)
        assert certificate['accepted'] == (st['status'] == 'sat')
        witnesses.append(dict(word=w, T=T, decoded_tableau=tab, certificate=certificate,
                              cells=info['cells'], cols=info['cols']))
        rows.append({"n": k, "T": T, "vars": nv, "clauses": len(cl), "sat": model is not None,
                     "seconds": st['teaching_seconds']})
    w = "0010"
    nv, cl, info = X.cook_levin(NTM, w, 6)
    model, _ = solve(nv, cl)
    decoded = X.decode_tableau(model, info)
    witnesses.append(dict(word=w,T=6,decoded_tableau=decoded,certificate=R.tableau_certificate(NTM,w,6,decoded)))
    tab = [[c if isinstance(c, str) else c[0] + c[1] for c in row] for row in decoded]
    nv2, cl2, _ = X.cook_levin(NTM, "0000", 6)
    no, no_stats = solve(nv2, cl2)
    reject = R.tableau_certificate(NTM, '0000', 6)
    assert not reject['accepted'] and no_stats['status'] == 'unsat'
    witnesses.append(reject)
    machine = {k:v for k,v in NTM.items() if k != 'delta'}
    machine['delta'] = [[q,a,rules] for (q,a),rules in NTM['delta'].items()]
    return {"rows": rows, "w": w, "tableau": tab, "legal": info["legal"], "per_position": info["per_position"][:3],
            "rejects_0000": no is None, "vars": nv, "clauses": len(cl),
            "acceptance_scope": 'T rows encode T-1 transitions; absorbing acceptance is forced in the final row.',
            "artifacts": [R.artifact('tableau/full-traces.json.gz',dict(machine=machine,witnesses=witnesses))]}


def compute_web() -> dict:
    n, cl = 4, WEB
    model, _ = solve(n, cl)
    sols = [a for a in itertools.product([False, True], repeat=n) if X.check([False] + list(a), cl)]
    verts, edges, lit, k = X.sat_to_is(cl)
    S = X.is_from_model(cl, model)
    clique_edges = X.is_to_clique(verts, edges)
    C = X.is_to_vc(verts, S)
    assert len(S) == k and all(not (u in S and v in S) for u,v in edges)
    assert all(u in C or v in C for u,v in edges)
    assert all((u,v) in clique_edges or (v,u) in clique_edges for u,v in itertools.combinations(S,2))
    V3, E3 = X.sat_to_3col(n, cl)
    nv, ccl, var = X.coloring_cnf(V3, E3, 3)
    cm, _ = solve(nv, ccl)
    colour = X.decode_coloring(V3, cm, var, 3)
    assert all(colour[u] != colour[v] for u,v in E3)
    names = {colour["T"]: "T", colour["F"]: "F", colour["B"]: "B"}
    mapped = [False] + [colour[f"x{v}"] == colour["T"] for v in range(1, n + 1)]
    nums, target = X.sat_to_subset_sum(n, cl)
    chosen = X.subset_from_model(n, cl, model, nums)
    assert sum(nums[v] for v in chosen) == target
    projections = []
    for bits in itertools.product((False,True),repeat=n):
        expected = all(any(bits[abs(l)-1] == (l>0) for l in c) for c in cl)
        fixed = [[var('T',0)],[var('F',1)],[var('B',2)]]
        fixed += [[var(f'x{i}',0 if b else 1)] for i,b in enumerate(bits,1)]
        projected, stats = solve(nv,ccl+fixed)
        assert (stats['status']=='sat') == expected
        projections.append(dict(assignment=bits,formula_value=expected,coloring_status=stats['status']))
    # one unsatisfiable formula through the colouring, to show the other direction
    bad = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    V4, E4 = X.sat_to_3col(2, bad)
    nv4, c4, _ = X.coloring_cnf(V4, E4, 3)
    bm, bad_stats = solve(nv4, c4)
    assert bad_stats['status'] == 'unsat'
    full = dict(verts=verts,edges=edges,independent_set=S,clique_edges=clique_edges,cover=C,
                coloring_vertices=V3,coloring_edges=E3,coloring=colour,all_16_projected_assignments=projections,
                subset_numbers=nums,target=target,chosen=chosen,bad_formula=bad)
    return {"n": n, "clauses": cl, "model": model[1:], "solutions": len(sols),
            "is": {"verts": [list(v) for v in verts], "edges": [[list(a), list(b)] for a, b in edges],
                   "lits": [lit[v] for v in verts], "k": k, "chosen": [list(v) for v in S],
                   "clique_edges": len(clique_edges), "cover": len(C)},
            "col": {"vertices": len(V3), "edges": len(E3), "cnf_vars": nv, "cnf_clauses": len(ccl),
                    "colour": {v: names[c] for v, c in colour.items()}, "mapped": mapped[1:],
                    "mapped_ok": X.check(mapped, cl), "bad_colourable": bm is not None},
            "ss": {"nums": {k_: str(v).zfill(n + len(cl)) for k_, v in nums.items()}, "target": str(target),
                   "chosen": chosen, "sum": str(sum(nums[x] for x in chosen))},
            "artifacts": [R.artifact('web/full-witnesses.json.gz',full)]}


def compute_selfreduce() -> dict:
    """Find an assignment for WEB using only yes/no answers from the solver (n + 1 calls)."""
    n, cl = 4, [list(c) for c in WEB]
    calls = 1
    assert solve(n, cl)[1]['status'] == 'sat'
    steps, fixed = [], []
    for v in range(1, n + 1):
        trial = cl + [[v]] + [[u] if b else [-u] for u, b in fixed]
        calls += 1
        candidate, status = solve(n, trial)
        assert status['status'] != 'unknown'
        ok = status['status'] == 'sat'
        b = ok
        steps.append({"var": v, "value": True, "kept": ok, "queried_formula": trial,
                      "status": status['status'], "model": candidate})
        fixed.append((v, b))
    model = [False] + [b for _, b in fixed]
    assert X.check(model, cl)
    assert R.model_satisfies(n, cl, model)
    return {"steps": steps, "model": model[1:], "calls": calls, "original_formula": cl}


def compute_phase() -> dict:
    rng = random.Random(3)
    ratios = [3.0, 3.5, 3.8, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.7, 5.0, 5.5, 6.0]
    out = {}
    for n in (50, 100, 150):
        rows = []
        for r in ratios:
            m = round(r * n)
            sat, confl = 0, []
            trials = 40 if n < 150 else 20
            for _ in range(trials):
                model, st = solve(n, X.random_ksat(n, m, 3, rng))
                assert st['status'] in ('sat','unsat')
                sat += st['status'] == 'sat'
                confl.append(st["conflicts"])
            rows.append({"ratio": r, "actual_ratio": m/n, "m": m, "trials": trials,
                         "sat_count": sat, "unsat_count": trials-sat, "unknown_count": 0,
                         "p_sat": sat / trials, "wilson95": R.wilson(sat,trials),
                         "median_conflicts": statistics.median(confl), "all_conflict_counts": confl})
        out[str(n)] = rows
    return {"ratios": ratios, "by_n": out, "seed": 3,
            "scope": 'Independent random clauses use distinct variables and independent fair signs; finite samples and Wilson intervals do not establish an asymptotic threshold.'}


def compute_solvers() -> dict:
    rng = random.Random(9)
    rows, trials = [], []
    for n in (20, 30, 40, 50, 60):
        m = round(4.26 * n)
        dn, cd, dt, ct = [], [], [], []
        for _ in range(10):
            f = X.random_ksat(n, m, 3, rng)
            t = time.perf_counter()
            try:
                dmodel, nodes = X.dpll(n, f, max_nodes=3_000_000)
                dstatus = 'sat' if dmodel is not None else 'unsat'
            except RuntimeError:
                nodes = None
                dmodel, dstatus = None, 'unknown'
            dt.append(time.perf_counter() - t)
            t = time.perf_counter()
            cmodel, st = solve(n, f)
            ct.append(st['teaching_seconds'])
            assert dstatus == 'unknown' or dstatus == st['status']
            if dmodel is not None:
                assert R.model_satisfies(n,f,dmodel)
            trials.append(dict(n=n,formula=f,dpll_status=dstatus,dpll_model=dmodel,dpll_nodes=nodes,
                               dpll_seconds=dt[-1],cdcl_status=st['status'],cdcl_model=cmodel,
                               cdcl_seconds=ct[-1],cdcl_stats=st))
            dn.append(nodes)
            cd.append(st["decisions"] + st["conflicts"])
        resolved = [d for d in dn if d is not None]
        rows.append({"n": n, "dpll_nodes": statistics.median(resolved) if resolved else None,
                     "dpll_s": statistics.median(dt), "cdcl_steps": statistics.median(cd),
                     "cdcl_s": statistics.median(ct), "trials": 10,
                     "dpll_resolved": len(resolved), "dpll_unknown": 10-len(resolved)})
    return {"rows": rows, "seed": 9, "dpll_node_budget": 3_000_000,
            "work_unit_scope": 'DPLL recursive nodes and CDCL decisions plus conflicts are different work units; timings cover teaching algorithms only.',
            "artifacts": [R.artifact('solvers/full-comparison.json.gz',trials)]}


def compute_knapsack() -> dict:
    rng = random.Random(4)
    rows, artifacts = [], []
    n = 30
    for digits in (2, 3, 4, 5, 6):
        weights = [rng.randrange(10 ** (digits - 1), 10 ** digits) for _ in range(n)]
        target = sum(rng.sample(weights, n//2))
        mask = (1 << (target+1))-1
        start = time.perf_counter()
        reach, layers = 1, [1]
        for weight in weights:
            reach = (reach | (reach << weight)) & mask
            layers.append(reach)
        ok = bool((reach >> target) & 1)
        elapsed = time.perf_counter()-start
        remaining, chosen = target, []
        for i in range(n-1,-1,-1):
            if not (layers[i] >> remaining) & 1:
                chosen.append(i)
                remaining -= weights[i]
        assert ok and remaining == 0 and sum(weights[i] for i in chosen) == target
        reference = R.subset_witness(weights,target)
        assert reference is not None and reach.bit_length() <= target+1
        raw = R.artifact(f'knapsack/digits-{digits}-reachable-bits.bin.gz',reach.to_bytes((target+8)//8,'little'))
        artifacts.append(raw)
        rows.append(dict(digits=digits,W=target,dp_s=elapsed,found=ok,weights=weights,
                         witness_indices=chosen,reference_indices=reference,retained_bit_count=target+1,
                         reachable_sums=reach.bit_count(),reachable_bits_artifact=raw['path']))
    weights = [rng.randrange(10 ** 11,10 ** 12) for _ in range(n)]
    target = sum(rng.sample(weights,n//2))
    start = time.perf_counter()
    left = {}
    for bits in range(1 << 15):
        value = sum(weights[i] for i in range(15) if bits >> i & 1)
        left[value] = bits
    chosen = None
    scanned = 0
    for bits in range(1 << 15):
        scanned += 1
        value = sum(weights[15+i] for i in range(15) if bits >> i & 1)
        if target-value in left:
            left_bits = left[target-value]
            chosen = [i for i in range(15) if left_bits >> i & 1]
            chosen += [15+i for i in range(15) if bits >> i & 1]
            break
    elapsed = time.perf_counter()-start
    assert chosen is not None and sum(weights[i] for i in chosen) == target
    assert R.subset_witness(weights,target) is not None
    return dict(n=n,rows=rows,mitm_digits=12,mitm_s=elapsed,mitm_found=True,seed=4,
                mitm_weights=weights,mitm_target=target,mitm_witness_indices=chosen,
                mitm_left_subsets=1 << 15,mitm_right_subsets_scanned=scanned,artifacts=artifacts,
                scope='Dense bitset keeps sums 0..W inclusive; bit-parallel operations have limb costs. Meet-in-middle still pays integer bit costs. Single host runs are illustrative.')


def compute_pratt() -> dict:
    p = 2 ** 61 - 1
    cert = X.pratt(p)
    ok, checks = X.verify_pratt(cert)
    reference = R.pratt_certificate(cert)
    assert ok and checks == reference['nodes']

    def flat(c, d=0, out=None):
        out = [] if out is None else out
        out.append({"p": c["p"], "g": c.get("g"), "depth": d})
        for f in c.get("factors", []):
            flat(f, d + 1, out)
        return out

    N = 1000000007 * 998244353
    factor_certificates = [X.pratt(q) for q in (1000000007,998244353)]
    factor_checks = [R.pratt_certificate(c) for c in factor_certificates]
    assert all(X.verify_pratt(c)[0] for c in factor_certificates)
    return {"p": str(p), "ok": ok, "checks": checks, "tree": flat(cert), "factors_of_pm1": X._factor(p - 1),
            "N": str(N), "N_factors": [1000000007, 998244353], "reference": reference,
            "factor_threshold_language": 'N>=2, 1<=k<N: exists a divisor d with 2<=d<=k. Full prime factorization certifies both answers.',
            "artifacts": [R.artifact('pratt/full-certificates.json.gz',dict(prime=cert,N=N,
                           factor_certificates=factor_certificates,factor_checks=factor_checks))]}


def compute_games() -> dict:
    rng = random.Random(8)
    rows = []
    for n in (4, 8, 12, 16):
        quants = [("E" if i % 2 == 0 else "A", i + 1) for i in range(n)]
        f = X.random_ksat(n, 2 * n, 3, rng)
        val, nodes = X.tqbf(quants, f)
        independent, truth = R.quantified(quants,f)
        assert val == independent
        rows.append({"n": n, "value": val, "nodes": nodes, "full_tree": 2 ** (n + 1) - 1,
                     "quantifiers": quants, "clauses": f, "full_truth_table": truth, "reference_value": independent})
    adj = {0: [1, 2], 1: [3, 4], 2: [4, 5], 3: [6], 4: [6, 7], 5: [7], 6: [0, 8], 7: [8], 8: []}
    win, positions = X.geography(adj, 0)
    assert win == R.geography(adj,0)
    grng = random.Random(2)
    grows = []
    for nv in (8, 12, 16, 20):
        g = {v: [u for u in range(nv) if u != v and grng.random() < 0.25] for v in range(nv)}
        t = time.perf_counter()
        w2, pos = X.geography(g, 0)
        elapsed = time.perf_counter() - t
        assert w2 == R.geography(g,0)
        grows.append({"n": nv, "first_wins": w2, "positions": pos, "seconds": elapsed,
                      "adjacency": {str(v): us for v,us in g.items()}})
    return {"tqbf": rows, "geo": {"adj": {str(k): v for k, v in adj.items()}, "first_wins": win,
                                   "positions": positions}, "geo_random": grows,
            "winner_convention": 'Player 1 places start, player 2 moves next; first_wins names initial placer.',
            "memory_scope": 'Actual memoized geography may use exponential storage; full depth-first proof gives PSPACE membership.'}


def compute_famous() -> dict:
    out = {}
    for n, k in ((13, 3), (14, 3), (44, 4)):
        t = time.perf_counter()
        model, st = solve(*X.schur_cnf(n, k), proof=n == 14)
        out[f"schur_{n}_{k}"] = {"sat": model is not None, "conflicts": st["conflicts"],
                                 "status": st['status'], "seconds": st['teaching_seconds']}
        if model is not None:
            var = lambda i, c: (i - 1) * k + c + 1  # noqa: E731
            colouring = [next(c for c in range(k) if model[var(i, c)]) for i in range(1, n + 1)]
            assert all(not (colouring[x-1] == colouring[y-1] == colouring[x+y-1])
                       for x in range(1,n+1) for y in range(x,n+1-x))
            out[f'schur_{n}_colouring'] = colouring
    t = time.perf_counter()
    model, st = solve(*X.schur_cnf(45, 4), max_conflicts=30_000)
    out["schur_45_4"] = {"status": st["status"], "conflicts": st["conflicts"], "seconds": st['teaching_seconds'],
                            "conflict_budget": 30_000}
    py = []
    for n in (500, 1000, 2000, 3000):
        nv, cl = X.pythagorean_cnf(n)
        t = time.perf_counter()
        model, st = solve(nv, cl, max_conflicts=30_000)
        colours = model[1:] if model is not None else None
        if colours is not None:
            # Re-enumerate triples from integer squares, independently of the encoder.
            for c in range(1,n+1):
                for a in range(1,c):
                    square = c*c-a*a
                    b = math.isqrt(square)
                    if a <= b and b*b == square:
                        assert not (colours[a-1] == colours[b-1] == colours[c-1])
        py.append({"n": n, "triples": len(cl) // 2, "status": st["status"], "conflicts": st["conflicts"],
                   "seconds": st['teaching_seconds'], "conflict_budget": 30_000, "colouring": colours})
    out["pythagorean"] = py
    nv, large = X.pythagorean_cnf(7825)
    out["pythagorean_7825_triples"] = len(large) // 2
    triples = set(tuple(c) for c in large if c[0] > 0)
    independent = set()
    # Euclid's parametrization generates all primitive triples, then all multiples.
    for m in range(2,math.isqrt(7825)+1):
        for q in range(1,m):
            c = m*m+q*q
            if c > 7825 or (m-q)%2 == 0 or math.gcd(m,q) != 1:
                continue
            a,b = sorted((m*m-q*q,2*m*q))
            for k in range(1,7825//c+1):
                independent.add((k*a,k*b,k*c))
    assert triples == independent
    out['artifacts'] = [R.artifact('famous/7825-complete-encoding.json.gz',dict(n=nv,clauses=large,
                       triples=sorted(triples),scope='Encoding and triple count only; published 7825 UNSAT proof is not rerun here.'))]
    out['scope'] = 'Local finite colourings fully checked. Schur 14/3 native RUP proof checked. Schur 45/4 budget exhaustion is unknown. Published S(5) and 7825 results are separate primary-source claims.'
    return out


def compute_formulas() -> dict:
    """De Morgan formulas over x1..x3: leaves are literals, internal nodes AND / OR; size = number of leaves.
    L(f) by dynamic programming over sizes: a formula of size s splits into sizes a + (s - a)."""
    n = 3
    full = (1 << (1 << n)) - 1
    lits = []
    for i in range(n):
        t = 0
        for x in range(1 << n):
            if x >> i & 1:
                t |= 1 << x
        lits += [t, full ^ t]
    best = {}
    witnesses = {}
    by_size = {1: set(lits)}
    for i,f in enumerate(lits):
        best[f] = 1
        witnesses[f] = ['lit',(i//2+1) * (1 if i%2 == 0 else -1)]
    s = 1
    while len(best) < (1 << (1 << n)) and s < 12:
        s += 1
        new = {}
        for a in range(1, s // 2 + 1):
            A, B = by_size.get(a, ()), by_size.get(s - a, ())
            for f in A:
                for g in B:
                    for op,h in (('and',f & g), ('or',f | g)):
                        if h not in best:
                            new.setdefault(h,[op,witnesses[f],witnesses[g]])
        for h in new:
            best[h] = s
            witnesses[h] = new[h]
        by_size[s] = set(new)
    # constants: 0 and 1 count as x & ~x and x | ~x (size 2)
    hist = {}
    for f in range(1 << (1 << n)):
        hist.setdefault(best.get(f), 0)
        hist[best.get(f)] += 1
    parity = 0
    for x in range(1 << n):
        if bin(x).count("1") % 2:
            parity |= 1 << x
    majority = sum(1 << x for x in range(1 << n) if bin(x).count("1") >= 2)
    certificate = R.formula_certificate(best,witnesses,n)
    assert best[parity] == 10 and best[majority] == 5
    return {"n": n, "hist": {str(k): v for k, v in sorted(hist.items(), key=lambda kv: (kv[0] is None, kv[0]))},
            "parity": best.get(parity), "majority": best.get(majority), "max": max(best.values()),
            "functions": len(best), "certificate": certificate,
            "basis": 'Binary AND/OR trees, literal leaves counted; free input negation, no free constants. Fan-out-one formulas, not unrestricted circuits.',
            "artifacts": [R.artifact('formulas/all-256-minimal-witnesses.json.gz',
                           dict(minimal_sizes=best,witnesses=witnesses,certificate=certificate))]}


def compute_sudoku():
    """The 21-clue exercise puzzle; every constraint and decoded cell retained."""
    puzzle = ['800000000','003600000','070090200','050007000','000045700',
              '000100030','001000068','008500010','090000400']
    var = lambda r,c,v: 81*r+9*c+v
    groups = [[var(r,c,v) for v in range(1,10)] for r in range(9) for c in range(9)]
    groups += [[var(r,c,v) for c in range(9)] for r in range(9) for v in range(1,10)]
    groups += [[var(r,c,v) for r in range(9)] for c in range(9) for v in range(1,10)]
    groups += [[var(3*br+dr,3*bc+dc,v) for dr in range(3) for dc in range(3)]
               for br in range(3) for bc in range(3) for v in range(1,10)]
    clauses = []
    for group in groups:
        clauses.append(group)
        clauses.extend([-a,-b] for a,b in itertools.combinations(group,2))
    givens = [[var(r,c,int(value))] for r,row in enumerate(puzzle) for c,value in enumerate(row) if value != '0']
    clauses += givens
    assert len(givens) == 21 and len(clauses) == 12009
    model,stats = solve(729,clauses)
    assert stats['status'] == 'sat'
    grid = [[next(v for v in range(1,10) if model[var(r,c,v)]) for c in range(9)] for r in range(9)]
    expected = set(range(1,10))
    assert all(set(row) == expected for row in grid)
    assert all({grid[r][c] for r in range(9)} == expected for c in range(9))
    assert all({grid[3*br+dr][3*bc+dc] for dr in range(3) for dc in range(3)} == expected
               for br in range(3) for bc in range(3))
    assert all(value == '0' or grid[r][c] == int(value) for r,row in enumerate(puzzle) for c,value in enumerate(row))
    return dict(puzzle=puzzle,grid=grid,variables=729,clauses=len(clauses),givens=21,
                long_clauses=324,binary_clauses=11664,conflicts=stats['conflicts'],
                seconds=stats['teaching_seconds'],all_rows_columns_boxes_and_givens_checked=True)


ITEMS = {k[8:]: _producer(k[8:], v) for k, v in list(globals().items()) if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
