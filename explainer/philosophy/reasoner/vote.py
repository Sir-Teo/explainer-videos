"""Social choice for Part 39 ("The Arithmetic of Democracy"): profiles and voting rules, Condorcet cycles and their
probability under impartial culture, May's theorem and Arrow's theorem by exhaustive search and SAT, manipulation,
single-peaked preferences, jury theorems, judgment aggregation, apportionment, and what preference learning
aggregates.

A profile is a list of ``(count, ranking)`` pairs; a ranking is a tuple of alternatives, best first.
"""

from __future__ import annotations

import itertools
import math
from collections import Counter

import numpy as np

from . import prop


# ---------------------------------------------------------------------------
# Profiles and pairwise majorities
# ---------------------------------------------------------------------------
def alternatives(profile) -> list:
    return sorted(set(profile[0][1]))


def pairwise(profile) -> dict:
    """N[(x, y)]: how many voters rank x above y."""
    alts = alternatives(profile)
    N = {(x, y): 0 for x in alts for y in alts if x != y}
    for c, r in profile:
        for i, x in enumerate(r):
            for y in r[i + 1:]:
                N[(x, y)] += c
    return N


def condorcet_winner(profile):
    alts = alternatives(profile)
    N = pairwise(profile)
    for x in alts:
        if all(N[(x, y)] > N[(y, x)] for y in alts if y != x):
            return x
    return None


def majority_cycle(profile) -> list | None:
    """A cycle x > y > z > x in the strict majority relation, if there is one (three alternatives suffice to find
    one whenever there is no Condorcet ordering among them)."""
    alts = alternatives(profile)
    N = pairwise(profile)
    for x, y, z in itertools.permutations(alts, 3):
        if N[(x, y)] > N[(y, x)] and N[(y, z)] > N[(z, y)] and N[(z, x)] > N[(x, z)]:
            return [x, y, z]
    return None


def _ranked(scores: dict, tie=None) -> list:
    tie = tie or sorted(scores)
    return sorted(scores, key=lambda a: (-scores[a], tie.index(a)))


def plurality(profile) -> dict:
    alts = alternatives(profile)
    s = {a: 0 for a in alts}
    for c, r in profile:
        s[r[0]] += c
    return {"scores": s, "winner": _ranked(s)[0]}


def borda(profile) -> dict:
    alts = alternatives(profile)
    m = len(alts)
    s = {a: 0 for a in alts}
    for c, r in profile:
        for i, a in enumerate(r):
            s[a] += c * (m - 1 - i)
    return {"scores": s, "winner": _ranked(s)[0]}


def runoff(profile) -> dict:
    """Plurality with a runoff between the top two."""
    p = plurality(profile)
    a, b = _ranked(p["scores"])[:2]
    N = pairwise(profile)
    return {"finalists": [a, b], "votes": [N[(a, b)], N[(b, a)]], "winner": a if N[(a, b)] >= N[(b, a)] else b}


def irv(profile) -> dict:
    """Instant runoff: repeatedly eliminate the alternative with the fewest first preferences."""
    left = alternatives(profile)
    rounds = []
    while True:
        s = {a: 0 for a in left}
        for c, r in profile:
            top = next(x for x in r if x in left)
            s[top] += c
        rounds.append(dict(s))
        total = sum(s.values())
        best = _ranked(s)[0]
        if 2 * s[best] > total or len(left) == 1:
            return {"rounds": rounds, "winner": best}
        worst = sorted(left, key=lambda a: (s[a], -left.index(a)))[0]
        left = [a for a in left if a != worst]


def copeland(profile) -> dict:
    alts = alternatives(profile)
    N = pairwise(profile)
    s = {a: sum(1 if N[(a, b)] > N[(b, a)] else 0.5 if N[(a, b)] == N[(b, a)] else 0 for b in alts if b != a)
         for a in alts}
    return {"scores": s, "winner": _ranked(s)[0]}


def kemeny(profile) -> dict:
    """The ranking that agrees with the most pairwise preferences (brute force over all orders)."""
    alts = alternatives(profile)
    N = pairwise(profile)
    best, best_s = None, -1
    for order in itertools.permutations(alts):
        s = sum(N[(order[i], order[j])] for i in range(len(order)) for j in range(i + 1, len(order)))
        if s > best_s:
            best, best_s = order, s
    return {"ranking": list(best), "agreements": best_s, "winner": best[0]}


def schulze(profile) -> dict:
    alts = alternatives(profile)
    N = pairwise(profile)
    P = {(x, y): (N[(x, y)] if N[(x, y)] > N[(y, x)] else 0) for x in alts for y in alts if x != y}
    for k in alts:
        for i in alts:
            for j in alts:
                if len({i, j, k}) == 3:
                    P[(i, j)] = max(P[(i, j)], min(P[(i, k)], P[(k, j)]))
    wins = {a: sum(P[(a, b)] > P[(b, a)] for b in alts if b != a) for a in alts}
    return {"strength": {f"{x}{y}": v for (x, y), v in P.items()}, "winner": _ranked(wins)[0]}


def sequential(profile, agenda) -> dict:
    """Pairwise majority votes along an agenda: the winner meets the next alternative."""
    N = pairwise(profile)
    cur = agenda[0]
    for a in agenda[1:]:
        cur = cur if N[(cur, a)] >= N[(a, cur)] else a
    return {"agenda": list(agenda), "winner": cur}


# Five rules, five winners: the 55-voter profile of the textbook literature (e.g. Hodge and Klima, *The Mathematics
# of Voting and Elections*, 2005).
FIFTY_FIVE = [(18, ("A", "D", "E", "C", "B")), (12, ("B", "E", "D", "C", "A")), (10, ("C", "B", "E", "D", "A")),
              (9, ("D", "C", "E", "B", "A")), (4, ("E", "B", "D", "C", "A")), (2, ("E", "C", "D", "B", "A"))]


def zoo(profile=None) -> dict:
    p = profile or FIFTY_FIVE
    N = pairwise(p)
    alts = alternatives(p)
    return {"profile": [[c, list(r)] for c, r in p], "voters": sum(c for c, _ in p),
            "plurality": plurality(p), "runoff": runoff(p), "irv": irv(p), "borda": borda(p),
            "condorcet": condorcet_winner(p), "copeland": copeland(p), "kemeny": kemeny(p), "schulze": schulze(p),
            "pairwise": {f"{x}{y}": N[(x, y)] for x in alts for y in alts if x != y}}


# ---------------------------------------------------------------------------
# Condorcet's paradox and its probability
# ---------------------------------------------------------------------------
def condorcet_paradox() -> dict:
    """Three voters with transitive rankings whose majority relation is a cycle (Condorcet, 1785)."""
    p = [(1, ("A", "B", "C")), (1, ("B", "C", "A")), (1, ("C", "A", "B"))]
    N = pairwise(p)
    return {"profile": [[c, list(r)] for c, r in p], "pairwise": {f"{x}{y}": N[(x, y)] for (x, y) in N},
            "cycle": majority_cycle(p), "winner": condorcet_winner(p)}


GUILBAUD = 0.25 - 3 / (2 * math.pi) * math.asin(1 / 3)     # the limit for three alternatives, n -> infinity


def paradox_exact(n: int) -> float:
    """Under impartial culture (every voter independently picks one of the 6 rankings of 3 alternatives uniformly),
    the exact probability that an odd number n of voters has no Condorcet winner: sum over all vote counts."""
    orders = list(itertools.permutations("ABC"))
    bad = 0.0
    for comp in _compositions(n, 6):
        prof = [(c, o) for c, o in zip(comp, orders) if c]
        if condorcet_winner(prof) is None:
            bad += math.exp(math.lgamma(n + 1) - sum(math.lgamma(c + 1) for c in comp) - n * math.log(6))
    return bad


def _compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for rest in _compositions(n - i, k - 1):
            yield (i,) + rest


def paradox_simulated(m: int, n: int = 101, trials: int = 20000, seed: int = 1785) -> float:
    """Impartial culture by simulation: the fraction of elections with m alternatives and n voters that have no
    Condorcet winner."""
    rng = np.random.default_rng(seed + m)
    ranks = np.argsort(rng.random((trials, n, m)), axis=2).argsort(axis=2)     # rank of each alternative, 0 = best
    beats = (ranks[:, :, :, None] < ranks[:, :, None, :]).sum(axis=1)         # trials x m x m
    wins = (2 * beats > n).sum(axis=2)
    return float((wins.max(axis=1) < m - 1).mean())


def paradox_table(ns=(3, 5, 7, 9, 11, 15, 21, 31), ms=(3, 4, 5, 6, 7)) -> dict:
    return {"exact": [{"n": n, "p": round(paradox_exact(n), 5)} for n in ns], "limit": round(GUILBAUD, 5),
            "simulated": [{"m": m, "p": round(paradox_simulated(m), 4)} for m in ms]}


# ---------------------------------------------------------------------------
# May's theorem by exhaustive search
# ---------------------------------------------------------------------------
def may_theorem(n: int = 3) -> dict:
    """Two alternatives, n voters, each voting +1, 0 (indifferent) or -1. An anonymous rule depends only on the
    counts (n+, n0, n-). Enumerate every rule on the counts (3^k of them) and keep those that are neutral
    (f(-x) = -f(x)) and positively responsive (if f(x) >= 0 and some voter moves up, the result becomes +1).
    May (1952): only simple majority survives."""
    counts = [(a, b, n - a - b) for a in range(n + 1) for b in range(n + 1 - a)]         # (plus, zero, minus)
    idx = {c: i for i, c in enumerate(counts)}

    def flip(c):
        return (c[2], c[1], c[0])

    def ups(c):     # one voter moves up: - to 0, or 0 to +
        p, z, m = c
        out = []
        if m > 0:
            out.append((p, z + 1, m - 1))
        if z > 0:
            out.append((p + 1, z - 1, m))
        return out

    survivors, total = [], 0
    for f in itertools.product((-1, 0, 1), repeat=len(counts)):
        total += 1
        if any(f[idx[flip(c)]] != -f[idx[c]] for c in counts):
            continue
        if any(f[idx[c]] >= 0 and f[idx[u]] != 1 for c in counts for u in ups(c)):
            continue
        survivors.append(f)
    majority = tuple(int(np.sign(p - m)) for p, z, m in counts)
    return {"n": n, "profiles": len(counts), "rules": total, "survivors": len(survivors),
            "is_majority": survivors == [majority], "counts": [list(c) for c in counts], "rule": list(majority)}


# ---------------------------------------------------------------------------
# Arrow's theorem by SAT (after Tang and Lin, 2009)
# ---------------------------------------------------------------------------
ARROW_AXIOMS = ("ORDER", "PARETO", "IIA", "ND1", "ND2")


def arrow_cnf(axioms=ARROW_AXIOMS) -> dict:
    """Two voters, three alternatives a, b, c; a social welfare function maps each of the 36 profiles of strict
    rankings to a strict social ranking. Variable v(P, xy) says x is above y at profile P, for xy in ab, ac, bc
    (108 variables). Clause groups: ORDER (no cycle at any profile), PARETO (unanimous pairs are respected), IIA
    (the social ranking of x and y depends only on the voters' rankings of x and y), ND1 and ND2 (neither voter is
    a dictator). Returns the clauses of each group."""
    alts = "abc"
    orders = list(itertools.permutations(alts))
    profiles = list(itertools.product(orders, orders))
    pairs = [("a", "b"), ("a", "c"), ("b", "c")]
    var = {}
    for pi, _ in enumerate(profiles):
        for x, y in pairs:
            var[(pi, x + y)] = len(var) + 1

    def lit(pi, x, y):          # literal for "x above y" at profile pi
        return var[(pi, x + y)] if (x, y) in pairs else -var[(pi, y + x)]

    def above(order, x, y):
        return order.index(x) < order.index(y)

    groups = {k: [] for k in ARROW_AXIOMS}
    for pi, P in enumerate(profiles):
        ab, ac, bc = lit(pi, "a", "b"), lit(pi, "a", "c"), lit(pi, "b", "c")
        groups["ORDER"] += [frozenset({-ab, -bc, ac}), frozenset({ab, bc, -ac})]
        for x, y in itertools.permutations(alts, 2):
            if all(above(o, x, y) for o in P):
                groups["PARETO"].append(frozenset({lit(pi, x, y)}))
    for (pi, P), (qi, Q) in itertools.combinations(list(enumerate(profiles)), 2):
        for x, y in pairs:
            if all(above(o, x, y) == above(u, x, y) for o, u in zip(P, Q)):
                a, b = lit(pi, x, y), lit(qi, x, y)
                groups["IIA"] += [frozenset({-a, b}), frozenset({a, -b})]
    for i, key in ((0, "ND1"), (1, "ND2")):
        groups[key].append(frozenset(-lit(pi, x, y) if above(P[i], x, y) else lit(pi, x, y)
                                     for pi, P in enumerate(profiles) for x, y in pairs))
    return {"n_vars": len(var), "groups": {k: groups[k] for k in axioms}, "profiles": len(profiles)}


def arrow_sat() -> dict:
    """Solve the full encoding (unsatisfiable: Arrow's theorem for 2 voters and 3 alternatives), then every subset
    of the five axiom groups, to find the minimal unsatisfiable set and the minimal correction sets (the Price
    List)."""
    enc = arrow_cnf()
    groups = enc["groups"]
    sizes = {k: len(v) for k, v in groups.items()}
    model, stats = prop.cdcl([c for k in ARROW_AXIOMS for c in groups[k]], enc["n_vars"])
    sat = {}
    for r in range(len(ARROW_AXIOMS) + 1):
        for sub in itertools.combinations(ARROW_AXIOMS, r):
            m, _ = prop.cdcl([c for k in sub for c in groups[k]], enc["n_vars"])
            sat[sub] = m is not None
    unsat = [set(s) for s, ok in sat.items() if not ok]
    mus = [sorted(s) for s in unsat if not any(t < s for t in unsat)]
    mcs = []
    for r in range(1, len(ARROW_AXIOMS) + 1):
        for drop in itertools.combinations(ARROW_AXIOMS, r):
            rest = tuple(k for k in ARROW_AXIOMS if k not in drop)
            if sat[rest] and not any(set(d) < set(drop) for d in mcs):
                mcs.append(drop)
    return {"n_vars": enc["n_vars"], "profiles": enc["profiles"], "clauses": sizes,
            "total_clauses": sum(sizes.values()), "satisfiable": model is not None,
            "conflicts": stats["conflicts"], "decisions": stats["decisions"], "mus": mus,
            "mcs": [list(m) for m in mcs], "subsets_checked": len(sat)}


def arrow_models(axioms=("ORDER", "PARETO", "IIA"), limit: int = 50) -> dict:
    """Count the social welfare functions satisfying the given axiom groups, by blocking each model found. With
    ORDER, PARETO and IIA there are exactly two, and each is a dictatorship."""
    enc = arrow_cnf(axioms)
    cls = [c for k in axioms for c in enc["groups"][k]]
    full = arrow_cnf()
    models = []
    while len(models) < limit:
        m, _ = prop.cdcl(cls, enc["n_vars"])
        if m is None:
            break
        models.append(m)
        cls.append(frozenset(-v if m[v] else v for v in range(1, enc["n_vars"] + 1)))

    def satisfies(m, clauses):
        return all(any((l > 0) == m[abs(l)] for l in c) for c in clauses)

    dictators = [[i + 1 for i, k in enumerate(("ND1", "ND2")) if not satisfies(m, full["groups"][k])] for m in models]
    return {"axioms": list(axioms), "models": len(models), "dictator_of_each": dictators}


# ---------------------------------------------------------------------------
# Manipulation (Gibbard 1973; Satterthwaite 1975)
# ---------------------------------------------------------------------------
def _rule(name):
    return {"plurality": lambda p: plurality(p)["winner"], "borda": lambda p: borda(p)["winner"],
            "irv": lambda p: irv(p)["winner"], "copeland": lambda p: copeland(p)["winner"],
            "dictator": lambda p: p[0][1][0],
            "a_or_b": lambda p: "a" if pairwise(p)[("a", "b")] >= pairwise(p)[("b", "a")] else "b"}[name]


def manipulation(rules=("plurality", "borda", "irv", "copeland", "dictator", "a_or_b"), n: int = 3) -> dict:
    """Three voters, three alternatives, every profile of strict rankings (6^3 = 216), ties broken
    alphabetically. A profile is manipulable if some voter, by reporting a different ranking, gets an outcome she
    truly prefers. For each rule, count manipulable profiles and give the first example."""
    alts = "abc"
    orders = list(itertools.permutations(alts))
    out = {}
    for name in rules:
        f = _rule(name)
        bad, example = 0, None
        for P in itertools.product(orders, repeat=n):
            prof = [(1, o) for o in P]
            w = f(prof)
            found = None
            for i in range(n):
                for lie in orders:
                    if lie == P[i]:
                        continue
                    q = list(prof)
                    q[i] = (1, lie)
                    w2 = f(q)
                    if P[i].index(w2) < P[i].index(w):
                        found = {"profile": [list(o) for o in P], "voter": i + 1, "truth": list(P[i]),
                                 "lie": list(lie), "honest_winner": w, "new_winner": w2}
                        break
                if found:
                    break
            if found:
                bad += 1
                example = example or found
        out[name] = {"manipulable": bad, "of": len(orders) ** n, "example": example,
                     "range": sorted({f([(1, o) for o in P]) for P in itertools.product(orders, repeat=n)})}
    return out


# ---------------------------------------------------------------------------
# Single-peaked preferences (Black, 1948)
# ---------------------------------------------------------------------------
def single_peaked_orders(axis) -> list:
    """All rankings single-peaked on the left-right axis: built outward from a peak, each next alternative the
    nearer unranked neighbour on the left or the right."""
    m = len(axis)
    out = []
    for peak in range(m):
        def grow(lo, hi, acc):
            if lo == 0 and hi == m - 1:
                out.append(tuple(axis[i] for i in acc))
                return
            if lo > 0:
                grow(lo - 1, hi, acc + [lo - 1])
            if hi < m - 1:
                grow(lo, hi + 1, acc + [hi + 1])
        grow(peak, peak, [peak])
    return out


def black(axis=("L", "CL", "C", "CR", "R"), n: int = 3, samples: int = 100000, seed: int = 1948) -> dict:
    """Every profile of n = 3 single-peaked voters on a five-point axis (16^3 = 4096): the majority relation has a
    Condorcet winner, and it is the median voter's peak. Compare random unrestricted profiles."""
    sp = single_peaked_orders(list(axis))
    ok_winner, median_ok = 0, 0
    for P in itertools.product(sp, repeat=n):
        prof = [(1, o) for o in P]
        w = condorcet_winner(prof)
        if w is not None:
            ok_winner += 1
            peaks = sorted(axis.index(o[0]) for o in P)
            median_ok += (axis.index(w) == peaks[n // 2])
    rng = np.random.default_rng(seed)
    allo = list(itertools.permutations(axis))
    none = 0
    for _ in range(samples // 10):
        P = [allo[i] for i in rng.integers(0, len(allo), n)]
        none += condorcet_winner([(1, o) for o in P]) is None
    return {"axis": list(axis), "single_peaked": len(sp), "all_orders": len(allo), "profiles": len(sp) ** n,
            "with_winner": ok_winner, "winner_is_median": median_ok,
            "random_no_winner": round(none / (samples // 10), 4), "random_samples": samples // 10}


# ---------------------------------------------------------------------------
# Juries (Condorcet 1785; Ladha 1992; Dietrich and Spiekermann 2013)
# ---------------------------------------------------------------------------
def _majority_right(n: int, q: float) -> float:
    return float(sum(math.comb(n, k) * q ** k * (1 - q) ** (n - k) for k in range(n // 2 + 1, n + 1)))


def jury(ps=(0.55, 0.6), ns=tuple(range(1, 202, 2)), leader_p: float = 0.6, follow: float = 0.3) -> dict:
    """P(the majority of n independent voters is right), each right with probability p. Then voters who, with
    probability ``follow``, copy an opinion leader who is right with probability ``leader_p``: conditional on the
    leader, voters are independent and right with q1 = follow + (1 - follow) p or q0 = (1 - follow) p, so the
    majority's accuracy tends to leader_p, not to 1."""
    indep = {str(p): [round(_majority_right(n, p), 4) for n in ns] for p in ps}
    q1 = follow + (1 - follow) * leader_p
    q0 = (1 - follow) * leader_p
    corr = [round(leader_p * _majority_right(n, q1) + (1 - leader_p) * _majority_right(n, q0), 4) for n in ns]
    return {"ns": list(ns), "independent": indep, "correlated": corr, "leader_p": leader_p, "follow": follow,
            "q1": round(q1, 3), "q0": round(q0, 3)}


# ---------------------------------------------------------------------------
# Diversity and ability (Hong and Page 2004), rebuilt
# ---------------------------------------------------------------------------
def _climb(values, starts, heuristic):
    """Each agent tries its step sizes in order from the current point and moves whenever the value is higher,
    until no step helps. Vectorized over starting points."""
    n = len(values)
    pos = starts.copy()
    while True:
        moved = np.zeros(len(pos), bool)
        for k in heuristic:
            cand = (pos + k) % n
            better = values[cand] > values[pos]
            pos = np.where(better, cand, pos)
            moved |= better
        if not moved.any():
            return pos


def _team(values, starts, team):
    pos = starts.copy()
    while True:
        old = pos.copy()
        for h in team:
            pos = _climb(values, pos, h)
        if (pos == old).all():
            return pos


def hong_page(n: int = 2000, steps: int = 12, k: int = 3, team_size: int = 10, seed: int = 2004,
              smooth: int = 0) -> dict:
    """A ring of n points with random values in [0, 100] (smoothed by a moving average of width ``smooth`` if
    given). An agent is an ordered triple of distinct step sizes from 1 to 12 (1320 agents); its ability is the mean
    value it reaches from every starting point. Compare the team of the ten best agents with a team of ten drawn
    at random, working in relay."""
    rng = np.random.default_rng(seed)
    values = rng.uniform(0, 100, n)
    if smooth:
        kern = np.ones(smooth) / smooth
        values = np.convolve(np.concatenate([values, values[:smooth - 1]]), kern, mode="valid")[:n]
    starts = np.arange(n)
    agents = list(itertools.permutations(range(1, steps + 1), k))
    ability = np.array([values[_climb(values, starts, h)].mean() for h in agents])
    order = np.argsort(-ability)
    best = [agents[i] for i in order[:team_size]]
    rand_idx = rng.choice(len(agents), team_size, replace=False)
    rand = [agents[i] for i in rand_idx]
    best_team = float(values[_team(values, starts, best)].mean())
    rand_team = float(values[_team(values, starts, rand)].mean())
    distinct = lambda team: len({s for h in team for s in h})     # noqa: E731
    return {"agents": len(agents), "best_agent": round(float(ability[order[0]]), 2),
            "median_agent": round(float(np.median(ability)), 2), "best_team": round(best_team, 2),
            "random_team": round(rand_team, 2), "best_members": [list(h) for h in best],
            "random_members": [list(h) for h in rand], "best_distinct_steps": distinct(best),
            "random_distinct_steps": distinct(rand), "smooth": smooth}


# ---------------------------------------------------------------------------
# Judgment aggregation (Kornhauser and Sager 1986; Pettit 2001; List and Pettit 2002)
# ---------------------------------------------------------------------------
JUDGES = [("judge 1", (1, 1)), ("judge 2", (1, 0)), ("judge 3", (0, 1))]     # (p, q): breach, and damage


def doctrinal() -> dict:
    """Three judges; liability (r) holds iff a valid contract was breached (p) and damage resulted (q). Majorities
    on p and on q say yes, the majority on r says no: premise-based and conclusion-based procedures disagree."""
    rows = [{"judge": j, "p": p, "q": q, "r": int(p and q)} for j, (p, q) in JUDGES]
    maj = {k: int(sum(r[k] for r in rows) * 2 > len(rows)) for k in ("p", "q", "r")}
    return {"rows": rows, "majority": maj, "premise_based": int(maj["p"] and maj["q"]), "conclusion_based": maj["r"],
            "majority_consistent": maj["r"] == int(maj["p"] and maj["q"])}


def list_pettit(n: int = 3) -> dict:
    """The agenda p, q, p and q, with negations. Each judge holds one of the four consistent, complete judgment
    sets. An anonymous, systematic rule accepts a proposition iff g(k) = 1, where k is how many judges accept it;
    the same g for every proposition, and for negations g(n - k) = 1 - g(k) (completeness). Enumerate every such g
    and every profile (4^n): none always yields a consistent collective set (List and Pettit, 2002)."""
    types = [(p, q) for p in (1, 0) for q in (1, 0)]
    gs = []
    for g in itertools.product((0, 1), repeat=n + 1):
        if all(g[n - k] == 1 - g[k] for k in range(n + 1)):
            gs.append(g)
    out = []
    for g in gs:
        fail = None
        for P in itertools.product(types, repeat=n):
            kp = sum(t[0] for t in P)
            kq = sum(t[1] for t in P)
            kr = sum(t[0] and t[1] for t in P)
            cp, cq, cr = g[kp], g[kq], g[kr]
            if cr != (cp and cq):
                fail = {"profile": [list(t) for t in P], "collective": [cp, cq, cr]}
                break
        out.append({"g": list(g), "consistent_always": fail is None, "counterexample": fail})
    return {"n": n, "rules": out, "any_ok": any(r["consistent_always"] for r in out)}


# ---------------------------------------------------------------------------
# Apportionment (Hamilton; Jefferson; Webster; Balinski and Young 1982)
# ---------------------------------------------------------------------------
def hamilton(pops, seats):
    total = sum(pops)
    q = [p * seats / total for p in pops]
    a = [math.floor(x) for x in q]
    left = seats - sum(a)
    for i in sorted(range(len(pops)), key=lambda i: -(q[i] - a[i]))[:left]:
        a[i] += 1
    return a, q


def divisor(pops, seats, rnd):
    """A divisor method: find d with sum(round(p / d)) = seats, rounding by ``rnd``."""
    lo, hi = 1e-9, sum(pops)
    for _ in range(200):
        d = (lo + hi) / 2
        s = sum(rnd(p / d) for p in pops)
        if s > seats:
            lo = d
        elif s < seats:
            hi = d
        else:
            return [rnd(p / d) for p in pops], d
    raise ValueError("no divisor")


def alabama(pops=(20, 16, 7), seats=(9, 10)) -> dict:
    """A toy Alabama paradox: with Hamilton's largest remainders, the small state loses a seat when the house
    grows. Webster's divisor method (round to nearest) does not suffer it."""
    ham = [hamilton(list(pops), s) for s in seats]
    web = [divisor(list(pops), s, lambda x: int(math.floor(x + 0.5)))[0] for s in seats]
    return {"pops": list(pops), "seats": list(seats), "quotas": [[round(x, 3) for x in q] for _, q in ham],
            "hamilton": [a for a, _ in ham], "webster": web}


def quota_violation(trials: int = 20000, seed: int = 1982) -> dict:
    """Balinski and Young: divisor methods avoid the Alabama and population paradoxes but can violate quota. Search
    random four-state problems for a Jefferson (round down) apportionment outside floor/ceiling of the quota."""
    rng = np.random.default_rng(seed)
    for _ in range(trials):
        pops = sorted(rng.integers(100, 2000, 4).tolist(), reverse=True)
        seats = int(rng.integers(10, 30))
        try:
            a, d = divisor(pops, seats, math.floor)
        except ValueError:
            continue
        q = [p * seats / sum(pops) for p in pops]
        bad = [i for i in range(4) if a[i] > math.ceil(q[i]) or a[i] < math.floor(q[i])]
        if bad:
            return {"pops": pops, "seats": seats, "quota": [round(x, 3) for x in q], "jefferson": a,
                    "hamilton": hamilton(pops, seats)[0], "violated": bad}
    return {}


# ---------------------------------------------------------------------------
# What preference learning aggregates (Siththaranjan, Laidlaw and Hadfield-Menell, 2023)
# ---------------------------------------------------------------------------
def bradley_terry(groups=((0.6, ("x", "y", "z")), (0.4, ("y", "z", "x"))), noise: float = 0.1,
                  iters: int = 20000, lr: float = 0.5) -> dict:
    """Annotators from hidden groups compare responses; each comparison is made by a random annotator, who picks
    her preferred response with probability 1 - noise. Fit Bradley-Terry scores s by maximum likelihood on the
    infinite-data comparison probabilities, and compare with the majority (Condorcet) and Borda rankings: the
    fitted scores order the responses as Borda does."""
    alts = sorted(groups[0][1])
    P = {}
    for x, y in itertools.permutations(alts, 2):
        P[(x, y)] = sum(w * ((1 - noise) if r.index(x) < r.index(y) else noise) for w, r in groups)
    s = {a: 0.0 for a in alts}
    for _ in range(iters):
        grad = {a: 0.0 for a in alts}
        for x, y in itertools.permutations(alts, 2):
            pr = 1 / (1 + math.exp(-(s[x] - s[y])))
            grad[x] += P[(x, y)] * (1 - pr)
            grad[y] -= P[(x, y)] * (1 - pr)
        for a in alts:
            s[a] += lr * grad[a]
        mean = sum(s.values()) / len(s)
        s = {a: v - mean for a, v in s.items()}
    borda_s = {a: sum(P[(a, b)] for b in alts if b != a) for a in alts}
    maj = {a: sum(P[(a, b)] > 0.5 for b in alts if b != a) for a in alts}
    cw = next((a for a in alts if maj[a] == len(alts) - 1), None)
    return {"groups": [[w, list(r)] for w, r in groups], "noise": noise,
            "P": {f"{x}{y}": round(v, 3) for (x, y), v in P.items()}, "bt": {a: round(v, 3) for a, v in s.items()},
            "bt_order": _ranked(s), "borda": {a: round(v, 3) for a, v in borda_s.items()},
            "borda_order": _ranked(borda_s), "condorcet_winner": cw}


def agendas(profile=None) -> dict:
    """Sequential pairwise voting on the Condorcet cycle: each agenda elects a different winner, so whoever sets
    the agenda chooses the outcome."""
    p = profile or [(1, ("A", "B", "C")), (1, ("B", "C", "A")), (1, ("C", "A", "B"))]
    out = []
    for first in itertools.combinations(alternatives(p), 2):
        last = [a for a in alternatives(p) if a not in first][0]
        ag = list(first) + [last]
        out.append(sequential(p, ag))
    return {"results": out, "winners": sorted({r["winner"] for r in out})}


def hong_page_runs(seeds=range(2004, 2009)) -> dict:
    runs = []
    for s in seeds:
        for smooth in (0, 25):
            h = hong_page(seed=s, smooth=smooth)
            runs.append({"seed": s, "smooth": smooth, "best_team": h["best_team"], "random_team": h["random_team"]})
    return {"runs": runs, "first": hong_page(seed=2004), "first_smooth": hong_page(seed=2004, smooth=25)}


def borda_iia(profile=None, drop: str = "C") -> dict:
    """Independence of irrelevant alternatives fails for the Borda count: on the 55-voter profile, D beats E with
    every candidate present; withdraw the also-ran C and E beats D, though no voter changed their mind about D and
    E."""
    p = profile or FIFTY_FIVE
    q = [(c, tuple(x for x in r if x != drop)) for c, r in p]
    before, after = borda(p), borda(q)
    N = pairwise(p)
    return {"drop": drop, "before": before["scores"], "after": after["scores"], "winner_before": before["winner"],
            "winner_after": after["winner"], "DE": [N[("D", "E")], N[("E", "D")]]}


def quadratic(values=(10.0, 10.0, 10.0, -50.0)) -> dict:
    """Quadratic voting (Lalley and Weyl, 2018): v votes cost v^2. A voter who gains u if the measure passes buys
    v = u / 2 votes (maximizing u v - v^2), so the votes cast are proportional to the stakes and the outcome
    follows the sum of values. One person, one vote follows the count instead."""
    votes = [u / 2 for u in values]
    return {"values": list(values), "votes": votes, "costs": [v * v for v in votes],
            "majority": "pass" if sum(1 for u in values if u > 0) > sum(1 for u in values if u < 0) else "fail",
            "qv_total": sum(votes), "qv": "pass" if sum(votes) > 0 else "fail", "net_value": sum(values)}


def _no_ties(profile) -> bool:
    """No ties in any instant-runoff round, and an odd electorate."""
    return all(len(set(r.values())) == len(r) for r in irv(profile)["rounds"]) and \
        sum(c for c, _ in profile) % 2 == 1


def irv_monotonicity(max_voters: int = 25) -> dict:
    """Search profiles of up to ``max_voters`` voters over three candidates for a failure of monotonicity in
    instant runoff: the winner W wins; some voters who ranked another candidate first move W to the top of their
    ballot (changing nothing else about W's rivals' order); and W now loses. No ties anywhere; smallest electorate
    first."""
    orders = list(itertools.permutations("ABC"))
    for n in range(3, max_voters + 1):
        for comp in _compositions(n, 6):
            prof = [(c, o) for c, o in zip(comp, orders) if c]
            if not _no_ties(prof):
                continue
            w = irv(prof)["winner"]
            for i, o in enumerate(orders):
                if comp[i] == 0 or o[0] == w:
                    continue
                new_o = (w,) + tuple(x for x in o if x != w)
                j = orders.index(new_o)
                for k in range(1, comp[i] + 1):
                    c2 = list(comp)
                    c2[i] -= k
                    c2[j] += k
                    prof2 = [(c, oo) for c, oo in zip(c2, orders) if c]
                    w2 = irv(prof2)["winner"]
                    if w2 != w and _no_ties(prof2):
                        return {"n": n, "before": [[c, list(oo)] for c, oo in prof], "after": [[c, list(oo)] for c, oo in prof2],
                                "moved": k, "from": list(o), "to": list(new_o), "winner_before": w, "winner_after": w2,
                                "rounds_before": irv(prof)["rounds"], "rounds_after": irv(prof2)["rounds"]}
    return {}
