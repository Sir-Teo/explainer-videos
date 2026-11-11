"""Dependency resolution (Part 41): packages, versions and constraints encoded as SAT, solved with Part 26's CDCL;
the reduction from 3-SAT showing that choosing versions is NP-complete (Di Cosmo et al. 2006); and a diamond."""

from __future__ import annotations

import random
from itertools import combinations


class Universe:
    """``pkgs``: {name: {version: [(dep name, set of allowed versions), ...]}}."""

    def __init__(self, pkgs: dict):
        self.pkgs = pkgs
        self.var = {}
        for p, vs in pkgs.items():
            for v in vs:
                self.var[(p, v)] = len(self.var) + 1

    def encode(self, root: list):
        """Clauses: at most one version of each package; a chosen version implies, for each dependency, one of its
        allowed versions; the root requirements hold."""
        cl = []
        for p, vs in self.pkgs.items():
            for a, b in combinations(vs, 2):
                cl.append([-self.var[(p, a)], -self.var[(p, b)]])
            for v, deps in vs.items():
                for d, allowed in deps:
                    cl.append([-self.var[(p, v)]] + [self.var[(d, w)] for w in sorted(allowed) if (d, w) in self.var])
        for d, allowed in root:
            cl.append([self.var[(d, w)] for w in sorted(allowed) if (d, w) in self.var])
        return len(self.var), cl

    def solve(self, root: list, seed: int = 0):
        from explainer.cs.algo.complexity import cdcl
        n, cl = self.encode(root)
        model, stats = cdcl(n, cl, seed=seed)
        if model is None:
            return None, stats, len(cl)
        inv = {i: pv for pv, i in self.var.items()}
        chosen = {inv[i][0]: inv[i][1] for i in range(1, n + 1) if model[i]}
        return chosen, stats, len(cl)


def from_3sat(n: int, clauses):
    """Package X_i with versions 0 and 1 (the value of variable i); package C_j with one version per literal, which
    requires X_i at the value that makes that literal true; the root requires every C_j.  Installable iff the
    formula is satisfiable."""
    if n < 0 or any(not 1 <= abs(l) <= n for c in clauses for l in c):
        raise ValueError("SAT literals must name a variable from 1 through n")
    pkgs = {f"x{i}": {0: [], 1: []} for i in range(1, n + 1)}
    for j, c in enumerate(clauses, 1):
        pkgs[f"c{j}"] = {k: [(f"x{abs(l)}", {1 if l > 0 else 0})] for k, l in enumerate(c, 1)}
    root = [(f"c{j}", set(range(1, len(c) + 1))) for j, c in enumerate(clauses, 1)]
    return Universe(pkgs), root


def diamond():
    """app needs A and B; A 1.x needs C >= 2; B 1.0 needs C < 2, B 1.1 allows C 2."""
    pkgs = {"app": {1: [("A", {1}), ("B", {10, 11})]},
            "A": {1: [("C", {2, 3})]},
            "B": {10: [("C", {1})], 11: [("C", {1, 2})]},
            "C": {1: [], 2: [], 3: []}}
    return Universe(pkgs), [("app", {1})]


def hardness(ns=(20, 40, 60, 80, 100), ratio: float = 4.26, trials: int = 20, seed: int = 0):
    """Random 3-SAT at the threshold, written as package universes: solver conflicts against size."""
    from explainer.cs.algo.complexity import random_ksat
    rng = random.Random(seed)
    rows = []
    for n in ns:
        conf, sat = [], 0
        for t in range(trials):
            cls = random_ksat(n, int(ratio * n), 3, rng)
            u, root = from_3sat(n, cls)
            chosen, stats, _ = u.solve(root, seed=t)
            conf.append(stats["conflicts"])
            sat += chosen is not None
        conf.sort()
        rows.append({"vars": n, "packages": n + int(ratio * n), "median_conflicts": conf[len(conf) // 2],
                     "satisfiable": sat / trials})
    return rows


def check_assignment(clauses, chosen):
    vals = {int(p[1:]): v for p, v in chosen.items() if p.startswith("x")}
    return all(any(abs(l) in vals and (vals[abs(l)] == 1) == (l > 0) for l in c) for c in clauses)


def backtracking_trace(u: Universe, root: list):
    """A simple resolver as package managers explain it: take requirements in order, try the newest allowed version
    of each, and backtrack on conflict.  Returns the steps it took."""
    steps = []
    pkgs = u.pkgs

    def solve(todo, chosen):
        if not todo:
            return chosen
        (p, allowed), rest = todo[0], todo[1:]
        if p in chosen:
            if chosen[p] in allowed:
                return solve(rest, chosen)
            steps.append(("conflict", p, chosen[p], sorted(allowed)))
            return None
        for v in sorted((v for v in pkgs.get(p, {}) if v in allowed), reverse=True):
            steps.append(("try", p, v, None))
            got = solve(rest + list(pkgs[p][v]), {**chosen, p: v})
            if got is not None:
                return got
            steps.append(("undo", p, v, None))
        return None
    result = solve(list(root), {})
    return {"steps": steps, "result": result}
