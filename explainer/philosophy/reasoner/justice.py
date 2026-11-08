"""Justice, built (Part 38).

* The veil of ignorance: random societies of five classes chosen by maximin, by average utility, and by expected
  utility with constant relative risk aversion eta; maximin as the limit eta -> infinity (Harsanyi against Rawls).
* The difference principle on a frontier of incentive-driven inequality.
* Nozick's Wilt Chamberlain, run as a toy economy, with Gini before and after, and the Price List of his argument.
* Dworkin's auction as competitive equilibrium from equal incomes (Varian 1974), found by proportional response
  dynamics on a Fisher market, with envy-freeness checked.
* Sen's liberal paradox (1970): for every assignment of two decisive pairs, a profile on which Pareto and minimal
  liberalism make social preference cyclic, found by exhaustive search; Lady Chatterley's Lover.
* Fair division of a cake: cut and choose; Selfridge-Conway for three, run on piecewise-constant valuations, with
  envy-freeness checked; envy-free rent division that maximizes the least utility (Gal et al. 2016).
"""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------------------
# Behind the veil
# ---------------------------------------------------------------------------
def _crra(w, eta):
    w = np.asarray(w, float)
    if abs(eta - 1.0) < 1e-12:
        return np.log(w)
    return (w ** (1 - eta) - 1) / (1 - eta)


def veil(n: int = 200, classes: int = 5, seed: int = 1971, etas=None) -> dict:
    """Two hundred societies, five equally large classes each, incomes drawn so that larger totals tend to come with
    more inequality. A chooser behind the veil, equally likely to be anyone, picks by: maximin (Rawls); average
    (Harsanyi's risk-neutral expected utility); and expected CRRA utility for eta from 0 to 20. As eta grows, the
    choice moves from the average-maximizing society to the maximin one."""
    rng = np.random.default_rng(seed)
    base = rng.uniform(10, 30, n)
    spread = rng.uniform(0, 1, n)
    soc = []
    for b, s in zip(base, spread):
        shares = np.sort(rng.dirichlet(np.ones(classes) * (1 + 20 * (1 - s))))
        total = b * classes * (1 + 0.8 * s)
        soc.append(np.round(total * shares, 3) + 1.0)
    soc = np.array(soc)
    avg = soc.mean(axis=1)
    mn = soc.min(axis=1)
    i_avg, i_max = int(np.argmax(avg)), int(np.argmax(mn))
    etas = etas if etas is not None else [0, 0.5, 1, 2, 3, 5, 8, 12, 20]
    by_eta = []
    for e in etas:
        # compare expected utility without the additive constant, so that large eta stays distinguishable in floating
        # point: maximize mean(w^(1 - eta)) for eta < 1, mean(log w) at 1, and minimize mean(w^(1 - eta)) above 1
        if abs(e - 1) < 1e-12:
            k = int(np.argmax(np.log(soc).mean(axis=1)))
        elif e < 1:
            k = int(np.argmax((soc ** (1 - e)).mean(axis=1)))
        else:
            k = int(np.argmin((soc ** (1 - e)).mean(axis=1)))
        by_eta.append({"eta": e, "choice": k, "average": round(float(avg[k]), 3), "minimum": round(float(mn[k]), 3)})
    return {"n": n, "classes": classes, "societies": soc.round(3).tolist(), "avg_choice": i_avg,
            "maximin_choice": i_max, "avg": {"average": round(float(avg[i_avg]), 3), "minimum": round(float(mn[i_avg]), 3)},
            "maximin": {"average": round(float(avg[i_max]), 3), "minimum": round(float(mn[i_max]), 3)},
            "by_eta": by_eta, "points": [[round(float(a), 3), round(float(m), 3)] for a, m in zip(avg, mn)]}


def difference_principle() -> dict:
    """An economy in which allowing the more advantaged a larger share, as an incentive t, first raises and then
    lowers the prospects of the least advantaged: u_A = 5 + 3t, u_L = 5 + 2t - t^2, for t in [0, 3]. Strict equality
    picks t = 0; the difference principle the t that maximizes u_L; the utilitarian the t that maximizes the sum."""
    ts = np.linspace(0, 3, 301)
    uA, uL = 5 + 3 * ts, 5 + 2 * ts - ts ** 2
    pick = {"equality": 0, "difference": int(np.argmax(uL)), "utilitarian": int(np.argmax(uA + uL))}
    return {"t": [round(float(t), 3) for t in ts[::10]], "uA": [round(float(x), 3) for x in uA[::10]],
            "uL": [round(float(x), 3) for x in uL[::10]],
            "points": {k: {"t": round(float(ts[i]), 3), "uA": round(float(uA[i]), 3), "uL": round(float(uL[i]), 3)}
                       for k, i in pick.items()}}


# ---------------------------------------------------------------------------
# Wilt Chamberlain
# ---------------------------------------------------------------------------
def gini(x) -> float:
    x = np.sort(np.asarray(x, float))
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


def wilt(n: int = 1000000, start: float = 1000.0, fee: float = 0.25, fans: float = 1.0) -> dict:
    """Nozick (1974): D1 gives each of a million people 1000 dollars; Wilt Chamberlain is one of them. Every fan puts a
    quarter in a box for Wilt each game they watch; one season of forty home games, every person a fan. D2 results,
    by voluntary transfers. Gini before and after, computed on the distribution (Wilt and everyone else)."""
    games = 40
    paid = n * fans * fee * games
    others = start - fee * games
    wilt_income = start + paid
    # Gini of n - 1 people at `others` and one person at wilt_income
    total = (n - 1) * others + wilt_income
    g = (wilt_income - others) * (n - 1) / (n * total)
    return {"n": n, "start": start, "fee": fee, "games": games, "wilt": wilt_income, "others": others,
            "gini_before": 0.0, "gini_after": round(g, 4), "share_of_wilt": round(wilt_income / total, 4)}


# ---------------------------------------------------------------------------
# Competitive equilibrium from equal incomes
# ---------------------------------------------------------------------------
SOCIETIES = {"A": [10, 10, 10, 10, 10], "B": [12, 14, 16, 20, 28], "C": [6, 12, 20, 40, 72]}


def three_societies(societies=None) -> dict:
    """Three five-person societies: their totals, least incomes and Gini coefficients, and which one each of three
    principles picks: the largest total, the best-off worst-off person, and the least inequality."""
    soc = societies or SOCIETIES
    out = {k: {"incomes": list(x), "total": float(sum(x)), "minimum": float(min(x)), "gini": round(gini(x), 3)}
           for k, x in soc.items()}
    return {"societies": out, "total": max(soc, key=lambda k: sum(soc[k])),
            "maximin": max(soc, key=lambda k: min(soc[k])), "equality": min(soc, key=lambda k: gini(soc[k]))}


def ceei(values=None, rounds: int = 3000) -> dict:
    """Varian (1974); Dworkin's auction (1981). Three agents with equal budgets of 1 and linear utilities over three
    divisible goods, one unit each. Proportional response dynamics (Zhang 2011) converge to the Fisher-market
    equilibrium, which maximizes the sum of log utilities (Eisenberg-Gale). Check market clearing, budgets and
    envy-freeness: no agent prefers another's bundle."""
    V = np.array(values if values is not None else [[6.0, 3.0, 1.0], [5.0, 4.0, 1.0], [2.0, 3.0, 5.0]])
    n, m = V.shape
    budget = np.ones(n)
    bids = np.outer(budget, np.ones(m)) / m
    for _ in range(rounds):
        prices = bids.sum(axis=0)
        alloc = bids / prices
        u = (V * alloc).sum(axis=1)
        bids = budget[:, None] * (V * alloc) / u[:, None]
    prices = bids.sum(axis=0)
    alloc = bids / prices
    u = (V * alloc).sum(axis=1)
    cross = V @ alloc.T                     # cross[i, j]: agent i's value for agent j's bundle
    envy = float(max(cross[i, j] - cross[i, i] for i in range(n) for j in range(n)))
    return {"values": V.tolist(), "prices": [round(float(p), 4) for p in prices],
            "alloc": [[round(float(x), 4) for x in row] for row in alloc], "utility": [round(float(x), 4) for x in u],
            "cross": [[round(float(x), 4) for x in row] for row in cross], "max_envy": round(envy, 6),
            "envy_free": envy <= 1e-6, "spent": [round(float(x), 4) for x in (alloc * prices).sum(axis=1)]}


# ---------------------------------------------------------------------------
# Sen's liberal paradox
# ---------------------------------------------------------------------------
ALTS = ("p", "l", "n")      # the prude reads; the lewd reads; no one reads


def _prefers(order, a, b):
    return order.index(a) < order.index(b)


def liberal_paradox() -> dict:
    """Two people, three alternatives. Minimal liberalism: person 1 is decisive over one pair, person 2 over another.
    The weak Pareto principle: if both prefer x to y, society does. For every choice of two distinct decisive pairs,
    search all 36 profiles of strict preferences for one on which these conditions alone force a cycle in social
    preference. Then Sen's own example: Lady Chatterley's Lover."""
    pairs = [frozenset(x) for x in itertools.combinations(ALTS, 2)]
    orders = list(itertools.permutations(ALTS))
    results = []
    for d1, d2 in itertools.permutations(pairs, 2):
        found = None
        for o1, o2 in itertools.product(orders, orders):
            strict = set()
            a, b = sorted(d1)
            strict.add((a, b) if _prefers(o1, a, b) else (b, a))
            a, b = sorted(d2)
            strict.add((a, b) if _prefers(o2, a, b) else (b, a))
            for x, y in itertools.permutations(ALTS, 2):
                if _prefers(o1, x, y) and _prefers(o2, x, y):
                    strict.add((x, y))
            # a cycle among three alternatives
            for x, y, z in itertools.permutations(ALTS, 3):
                if (x, y) in strict and (y, z) in strict and (z, x) in strict:
                    found = {"o1": list(o1), "o2": list(o2), "cycle": [x, y, z]}
                    break
            if found:
                break
        results.append({"d1": sorted(d1), "d2": sorted(d2), "profile": found})
    # Sen's example: the prude ranks n > p > l; the lewd p > l > n; the prude is decisive over {p, n}, the lewd over
    # {l, n}
    prude, lewd = ("n", "p", "l"), ("p", "l", "n")
    social = [("n", "p", "the prude's right: he prefers no one read it to his reading it"),
              ("l", "n", "the lewd's right: he prefers reading it to no one reading it"),
              ("p", "l", "Pareto: both prefer the prude reading to the lewd reading")]
    return {"pairs_checked": len(results), "all_cycle": all(r["profile"] for r in results), "results": results,
            "sen": {"prude": list(prude), "lewd": list(lewd), "social": social}}


# ---------------------------------------------------------------------------
# Cakes and rooms
# ---------------------------------------------------------------------------
def _value(density, a, b, grid):
    """The value of the piece [a, b] of the cake [0, 1] for a piecewise-constant density on `grid` intervals."""
    xs = np.linspace(0, 1, grid + 1)
    v = 0.0
    for k in range(grid):
        lo, hi = max(a, xs[k]), min(b, xs[k + 1])
        if hi > lo:
            v += density[k] * (hi - lo)
    return v


def _cut_for(density, a, target, grid, b_max=1.0):
    """The point x in [a, b_max] where the value of [a, x] reaches target, by bisection."""
    lo, hi = a, b_max
    for _ in range(60):
        mid = (lo + hi) / 2
        if _value(density, a, mid, grid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def selfridge_conway(dens=None) -> dict:
    """Three agents with piecewise-constant valuations of a cake [0, 1], each normalized to total 1 (Selfridge and
    Conway, c. 1960, as presented by Brams and Taylor, 1996). Agent 1 cuts three pieces of equal value to her. Agent 2
    trims her favourite down to tie with her second; the trimmings are set aside. Agent 3 chooses; agent 2 chooses,
    and must take the trimmed piece if agent 3 left it; agent 1 takes the rest. Then the trimmings: the one of agents
    2 and 3 who did not take the trimmed piece cuts them in three, and they choose in the order: the trimmed-piece
    taker, agent 1, the cutter. Check that no agent envies another."""
    grid = 10
    D = np.array(dens if dens is not None else [
        [3, 3, 1, 1, 0.5, 0.5, 0.5, 0.5, 0, 0],
        [0, 0.5, 0.5, 1, 1, 3, 3, 0.5, 0.5, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], float)
    D = D / D.sum(axis=1, keepdims=True) * grid           # each density integrates to 1
    val = lambda i, a, b: _value(D[i], a, b, grid)        # noqa: E731
    # stage 1: agent 1 cuts three equal pieces
    c1 = _cut_for(D[0], 0, 1 / 3, grid)
    c2 = _cut_for(D[0], c1, 1 / 3, grid)
    pieces = [[0.0, c1], [c1, c2], [c2, 1.0]]
    # agent 2 trims her favourite to equal her second
    v2 = [val(1, *p) for p in pieces]
    order = np.argsort(v2)[::-1]
    fav, second = int(order[0]), int(order[1])
    a, b = pieces[fav]
    # trim from the right: find x with value [a, x] = second's value
    x = _cut_for(D[1], a, v2[second], grid, b)
    trimmed = [a, x]
    trimmings = [x, b]
    work = [list(p) for p in pieces]
    work[fav] = trimmed
    # agent 3 chooses
    v3 = [val(2, *p) for p in work]
    pick3 = int(np.argmax(v3))
    # agent 2 chooses; must take the trimmed piece if available
    if pick3 != fav:
        pick2 = fav
    else:
        rest = [k for k in range(3) if k != pick3]
        pick2 = max(rest, key=lambda k: val(1, *work[k]))
    pick1 = [k for k in range(3) if k not in (pick3, pick2)][0]
    owner = {pick1: 0, pick2: 1, pick3: 2}
    # stage 2: the trimmings; T = taker of the trimmed piece, C = the other of agents 2 and 3
    T = owner[fav]
    C = 2 if T == 1 else 1
    ta, tb = trimmings
    total_t = val(C, ta, tb)
    d1 = _cut_for(D[C], ta, total_t / 3, grid, tb)
    d2 = _cut_for(D[C], d1, total_t / 3, grid, tb)
    tp = [[ta, d1], [d1, d2], [d2, tb]]
    left = [0, 1, 2]
    gets = {}
    for agent in (T, 0, C):
        k = max(left, key=lambda q: val(agent, *tp[q]))
        gets[agent] = k
        left.remove(k)
    bundles = {i: [] for i in range(3)}
    for k, i in owner.items():
        bundles[i].append(work[k])
    for i, k in gets.items():
        bundles[i].append(tp[k])
    worth = [[round(sum(val(i, *p) for p in bundles[j]), 4) for j in range(3)] for i in range(3)]
    envy_free = all(worth[i][i] >= worth[i][j] - 1e-6 for i in range(3) for j in range(3))
    return {"densities": D.round(4).tolist(), "first_cuts": [round(c1, 4), round(c2, 4)], "trim": round(x, 4),
            "fav_of_2": fav, "picks": {"3": pick3, "2": pick2, "1": pick1}, "trimmed_taker": T, "cutter": C,
            "trim_cuts": [round(d1, 4), round(d2, 4)], "bundles": {str(i): [[round(a, 4), round(b, 4)] for a, b in bs]
                                                                    for i, bs in bundles.items()},
            "worth": worth, "envy_free": envy_free}


def cut_and_choose(dens=None) -> dict:
    """Two agents: the first cuts the cake into two pieces she values equally; the second takes the one she prefers."""
    grid = 10
    D = np.array(dens if dens is not None else [[3, 3, 1, 1, 0.5, 0.5, 0.5, 0.5, 0, 0],
                                                [0, 0.5, 0.5, 1, 1, 3, 3, 0.5, 0.5, 0]], float)
    D = D / D.sum(axis=1, keepdims=True) * grid
    c = _cut_for(D[0], 0, 0.5, grid)
    left, right = _value(D[1], 0, c, grid), _value(D[1], c, 1, grid)
    chooser_takes = "left" if left >= right else "right"
    return {"cut": round(c, 4), "chooser_values": [round(left, 4), round(right, 4)], "chooser_takes": chooser_takes,
            "cutter_gets": 0.5, "chooser_gets": round(max(left, right), 4)}


def rent_division(values=None, rent: float = 3000.0) -> dict:
    """Gal, Mash, Procaccia and Zick (2016), as on Spliddit: three housemates value three rooms (each person's values
    sum to the rent). Assign rooms to maximize total value, then choose prices summing to the rent so that no one
    envies another's room-and-price, maximizing the least utility. A small linear program, solved by search over a
    fine grid of prices."""
    V = np.array(values if values is not None else [[1500.0, 1000.0, 500.0], [1300.0, 1100.0, 600.0],
                                                     [1200.0, 900.0, 900.0]])
    n = len(V)
    best_assign, best_val = None, -1
    for perm in itertools.permutations(range(n)):
        s = sum(V[i, perm[i]] for i in range(n))
        if s > best_val:
            best_assign, best_val = perm, s
    # prices p_room; utilities u_i = V[i, a_i] - p_{a_i}; envy-free: u_i >= V[i, r] - p_r for all r
    best, best_p = -1e18, None
    step = 5.0
    for p0 in np.arange(0, rent + step, step):
        for p1 in np.arange(0, rent - p0 + step, step):
            p2 = rent - p0 - p1
            if p2 < -1e-9:
                continue
            p = np.array([p0, p1, p2])
            u = np.array([V[i, best_assign[i]] - p[best_assign[i]] for i in range(n)])
            ok = all(u[i] >= V[i, r] - p[r] - 1e-9 for i in range(n) for r in range(n))
            if ok and u.min() > best + 1e-9:
                best, best_p = float(u.min()), p.copy()
    u = [float(V[i, best_assign[i]] - best_p[best_assign[i]]) for i in range(n)]
    return {"values": V.tolist(), "rent": rent, "assign": list(best_assign), "prices": [round(float(x), 2) for x in best_p],
            "utility": [round(x, 2) for x in u], "min_utility": round(best, 2), "total_value": best_val}


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------
STUDENT_PREFS = [[3, 2, 1, 0], [1, 0, 3, 2], [0, 1, 2, 3], [0, 2, 3, 1]]    # each student's ranking of schools
SCHOOL_PRIORITY = [[3, 2, 0, 1], [0, 3, 2, 1], [1, 2, 0, 3], [2, 1, 0, 3]]  # each school's ranking of students


def deferred_acceptance(prop_prefs, recv_prefs) -> dict:
    """Gale and Shapley (1962), in rounds: every unmatched proposer proposes to the best receiver not yet tried;
    each receiver holds the best proposal so far and rejects the rest. Returns the matching (proposer -> receiver)
    and, for each round, the proposals made and the proposals held."""
    n = len(prop_prefs)
    free, nxt, held, rounds = list(range(n)), [0] * n, {}, []
    while free:
        props = {}
        for p in free:
            r = prop_prefs[p][nxt[p]]
            nxt[p] += 1
            props.setdefault(r, []).append(p)
        new_free = []
        for r, ps in props.items():
            cands = ps + ([held[r]] if r in held else [])
            best = min(cands, key=lambda q: recv_prefs[r].index(q))
            new_free += [q for q in cands if q != best]
            held[r] = best
        rounds.append({"proposals": {str(r): sorted(ps) for r, ps in sorted(props.items())},
                       "held": [held.get(r) for r in range(n)]})
        free = sorted(new_free)
    match = [None] * n
    for r, p in held.items():
        match[p] = r
    return {"match": match, "rounds": rounds}


def is_stable(match, prop_prefs, recv_prefs) -> bool:
    """No blocking pair: no proposer and receiver who each prefer the other to their partner."""
    inv = {r: p for p, r in enumerate(match)}
    return not any(prop_prefs[p].index(r) < prop_prefs[p].index(match[p]) and
                   recv_prefs[r].index(p) < recv_prefs[r].index(inv[r])
                   for p in range(len(match)) for r in range(len(match)))


def stable_matching(student_prefs=None, school_priority=None) -> dict:
    """School choice with four students and four schools of one seat each. Run student-proposing and
    school-proposing deferred acceptance, enumerate all 24 matchings to find every stable one, and check the
    theorem: the student-proposing outcome is the best stable matching for every student, the school-proposing one
    the worst."""
    sp = student_prefs or STUDENT_PREFS
    cp = school_priority or SCHOOL_PRIORITY
    n = len(sp)
    stu = deferred_acceptance(sp, cp)
    sch = deferred_acceptance(cp, sp)
    sch_match = [None] * n
    for r, p in enumerate(sch["match"]):
        sch_match[p] = r
    stable = [list(m) for m in itertools.permutations(range(n)) if is_stable(m, sp, cp)]
    ranks = [[sp[p].index(m[p]) + 1 for p in range(n)] for m in stable]
    s_rank = [sp[p].index(stu["match"][p]) + 1 for p in range(n)]
    c_rank = [sp[p].index(sch_match[p]) + 1 for p in range(n)]
    student_optimal = all(s_rank[p] <= r[p] for r in ranks for p in range(n))
    school_pessimal = all(c_rank[p] >= r[p] for r in ranks for p in range(n))
    return {"student_prefs": sp, "school_priority": cp, "student_match": stu["match"], "rounds": stu["rounds"],
            "school_match": sch_match, "stable": stable, "stable_ranks": ranks, "matchings": math.factorial(n),
            "student_ranks": s_rank, "school_side_ranks": c_rank, "student_optimal": student_optimal,
            "worst_for_students": school_pessimal}
