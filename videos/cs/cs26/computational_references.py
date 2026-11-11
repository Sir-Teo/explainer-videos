"""Complete finite witnesses and independent checks for Part 26.

Native Glucose cross-checks SAT statuses; positive assignments are evaluated
literal by literal here. A retained proof is only called checked when the RUP
checker below has actually accepted it. Finite experiments are not asymptotic
complexity proofs. These helpers do not import the teaching instrument.
"""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path('.cache/cs26/artifacts')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def artifact(name, data):
    if not isinstance(data, bytes):
        data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    if name.endswith('.gz'):
        data = gzip.compress(data, mtime=0)
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_bytes(data)
    temp.replace(path)
    return dict(path=str(path), sha256=digest(data), bytes=len(data))


def model_satisfies(n, clauses, model):
    assert len(model) == n + 1 and all(type(v) is bool for v in model)
    assert all(all(type(l) is int and 1 <= abs(l) <= n for l in c) for c in clauses)
    return all(any(model[abs(l)] == (l > 0) for l in c) for c in clauses)


def reference_sat(n, clauses, status, proof=False):
    """Cross-check a resolved teaching-solver result with native Glucose 4.2."""
    import pysat
    from pysat.solvers import Glucose42
    assert status in ('sat', 'unsat')
    with Glucose42(bootstrap_with=clauses, with_proof=proof) as solver:
        sat = solver.solve()
        assert sat == (status == 'sat')
        row = dict(engine='Glucose 4.2 / python-sat', binding_version=pysat.__version__, status=status)
        if sat:
            values = set(solver.get_model())
            model = [False] + [v in values for v in range(1, n + 1)]
            assert model_satisfies(n, clauses, model)
            row['model'] = model
        elif proof:
            row['drup_proof'] = solver.get_proof()
            row['proof_scope'] = 'Retained native solver proof; no checker claim until explicitly checked.'
    return row


def check_rup(clauses, proof):
    """Check a deletion/RUP proof by unit propagation of each negated addition.

    This accepts the RUP subset of DRAT. Deletions are ignored: retaining
    already implied clauses is sound for RUP and avoids depending on the native
    logger's omission of bootstrap unit propagations. Every added clause must
    follow from the original clauses and earlier checked additions. A RAT-only
    addition is still rejected.
    """
    database = [frozenset(c) for c in clauses]
    assert all(all(type(l) is int and l != 0 for l in c) for c in database)
    additions = 0
    ignored_deletions = 0
    empty = False
    for line in proof:
        parts = line.split()
        if not parts:
            continue
        deletion = parts[0] == 'd'
        if deletion:
            parts = parts[1:]
        assert parts[-1] == '0'
        clause = frozenset(map(int, parts[:-1]))
        assert 0 not in clause, 'zero is a terminator, not a proof literal'
        if deletion:
            ignored_deletions += 1
            continue
        assignment = {-l for l in clause}
        conflict = any(-l in assignment for l in assignment)
        while not conflict:
            units = []
            for c in database:
                if c & assignment:
                    continue
                free = c - {-l for l in assignment}
                if not free:
                    conflict = True
                    break
                if len(free) == 1:
                    units.extend(free)
            if conflict or not units:
                break
            for lit in units:
                if -lit in assignment:
                    conflict = True
                    break
                assignment.add(lit)
        assert conflict, 'addition is not RUP'
        database.append(clause)
        additions += 1
        empty |= not clause
    assert empty, 'proof did not derive the empty clause'
    return dict(checked=True, additions=additions, ignored_deletions=ignored_deletions,
                checker='independent unit-propagation RUP checker retaining all implied clauses')


def successors(machine, row):
    heads = [i for i, c in enumerate(row) if isinstance(c, tuple)]
    assert len(heads) == 1
    i = heads[0]
    q, a = row[i]
    if q == machine['accept']:
        return [tuple(row)]
    out = []
    for q2, write, move in machine['delta'].get((q, a), []):
        j = i + move
        if not 1 <= j < len(row) - 1:
            continue
        result = list(row)
        result[i] = write
        result[j] = (q2, result[j])
        out.append(tuple(result))
    return out


def tableau_certificate(machine, word, time_rows, tableau=None):
    """Direct whole-configuration exploration, independent of local windows/CNF."""
    width = time_rows + 2
    start = ('#', (machine['start'], word[0] if word else machine['blank']),
             *word[1:], *([machine['blank']] * (width - max(len(word), 1))), '#')
    layers = [{start}]
    for _ in range(time_rows - 1):
        layers.append({nxt for row in layers[-1] for nxt in successors(machine, row)})
    accepted = any(any(isinstance(c, tuple) and c[0] == machine['accept'] for c in row) for row in layers[-1])
    if tableau is not None:
        assert len(tableau) == time_rows and tuple(tableau[0]) == start
        for row in tableau:
            assert len(row) == width + 2 and row[0] == row[-1] == '#'
            assert all(c != '#' for c in row[1:-1])
            assert sum(isinstance(c, tuple) for c in row) == 1
        assert all(tuple(b) in successors(machine, a) for a, b in zip(tableau, tableau[1:]))
        assert any(isinstance(c, tuple) and c[0] == machine['accept'] for c in tableau[-1])
        assert accepted
    return dict(word=word, rows=time_rows, transition_budget=time_rows-1, accepted=accepted,
                full_reachable_layers=[sorted(layer, key=repr) for layer in layers],
                decoded_trace_checked=tableau is not None)


def reachability(adj, source, target, steps):
    reachable = {source}
    layers = [sorted(reachable)]
    for _ in range(steps):
        reachable |= {u for v in reachable for u in adj[v]}
        layers.append(sorted(reachable))
    return target in reachable, layers


def quantified(quants, clauses):
    """Bottom-up full truth table, with no short-circuit evaluator."""
    variables = [v for _, v in quants]
    rows = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        values = dict(zip(variables, bits))
        rows.append(all(any(values[abs(l)] == (l > 0) for l in c) for c in clauses))
    original = list(rows)
    for q, _ in reversed(quants):
        rows = [(a or b) if q == 'E' else (a and b) for a, b in zip(rows[::2], rows[1::2])]
    return rows[0], original


def geography(adj, start):
    """Independent recursive set search; returns initial placer outcome."""
    def next_wins(v, remaining):
        return any(not next_wins(u, remaining - {u}) for u in adj[v] if u in remaining)
    return not next_wins(start, set(adj) - {start})


def wilson(successes, count):
    z = 1.959963984540054
    p = successes / count
    center = (p + z*z/(2*count)) / (1 + z*z/count)
    half = z * math.sqrt(p*(1-p)/count + z*z/(4*count*count)) / (1 + z*z/count)
    return [max(0., center-half), min(1., center+half)]


def subset_witness(weights, target):
    """Separate list-doubling meet-in-middle reference with explicit indices."""
    middle = len(weights)//2
    def sums(start, stop):
        out = [(0, ())]
        for i in range(start, stop):
            out += [(value+weights[i], indices+(i,)) for value,indices in out]
        return out
    left = dict(sums(0,middle))
    for value,indices in sums(middle,len(weights)):
        if target-value in left:
            witness = left[target-value] + indices
            assert sum(weights[i] for i in witness) == target
            return list(witness)
    return None


def pratt_certificate(cert):
    """Independent bottom-up Lucas criterion using gcd order witnesses."""
    nodes = []
    pending = [cert]
    while pending:
        node = pending.pop()
        nodes.append(node)
        pending.extend(node.get('factors', []))
    proven = {2}
    powers = 0
    for node in sorted(nodes,key=lambda c:c['p']):
        p = node['p']
        if p == 2:
            continue
        factors = [c['p'] for c in node['factors']]
        assert all(q in proven and 2 <= q < p for q in factors)
        remaining = p-1
        for q in factors:
            while remaining % q == 0:
                remaining //= q
        assert remaining == 1
        assert pow(node['g'],p-1,p) == 1
        for q in factors:
            assert math.gcd(pow(node['g'],(p-1)//q,p)-1,p) == 1
        powers += 1 + len(factors)
        proven.add(p)
    return dict(valid=True,nodes=len(nodes),modular_powers=powers,distinct_primes=sorted(proven))


def formula_certificate(best, witnesses, n=3):
    """Check every AST and the complete closure giving the lower bounds."""
    full = (1 << (1 << n)) - 1
    literals = {sum(((x >> i) & 1) << x for x in range(1 << n)) for i in range(n)}
    literals |= {full ^ v for v in tuple(literals)}
    def evaluate(node, bits):
        if node[0] == 'lit':
            return bits[abs(node[1])-1] == (node[1] > 0), 1
        a, left = evaluate(node[1], bits)
        b, right = evaluate(node[2], bits)
        return ((a and b) if node[0] == 'and' else (a or b)), left + right
    for mask, tree in witnesses.items():
        value = 0
        for x in range(1 << n):
            bit, size = evaluate(tree, [(x >> i) & 1 == 1 for i in range(n)])
            value |= int(bit) << x
        assert value == mask and size == best[mask]
    # A size-s binary tree splits at its root into positive sizes a + b=s.
    # Enumerating every pair of functions with smaller minimal sizes closes
    # the induction; replacing a nonminimal subtree cannot improve a minimum.
    layers = {1: set(literals)}
    reached = set(literals)
    for size in range(2, max(best.values()) + 1):
        now = set()
        for a in range(1, size):
            for left in layers.get(a, ()):
                for right in layers.get(size-a, ()):
                    now.update((left & right, left | right))
        now -= reached
        assert now == {mask for mask, minimum in best.items() if minimum == size}
        layers[size] = now
        reached |= now
    assert len(reached) == 1 << (1 << n)
    return dict(functions=len(reached), all_asts_evaluated=True, complete_minimality_closure=True,
                layers={str(k): sorted(v) for k, v in layers.items()})
