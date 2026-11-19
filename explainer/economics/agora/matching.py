"""Markets by design (Part 17): matching without prices, and mechanisms that ask people what they want.

**Matching.**  :func:`deferred_acceptance` (Gale and Shapley's algorithm, one-to-one or many-to-one, round by round,
with a log for drawing it), :func:`boston` (the immediate-acceptance rule many school districts used),
:func:`blocking_pairs` and :func:`all_stable` (every stable matching of a small market, by enumeration: the lattice),
:func:`outcomes_by_report` (what one participant gets for every list it could submit: a manipulation check),
:func:`top_trading_cycles` (Shapley and Scarf's housing market, with Gale's cycles), :func:`kidney_exchange` (the most
transplants from cycles of bounded length and chains started by altruistic donors, by exhaustive search on a small
pool).

**Mechanisms.**  :func:`pivotal` (Clarke's pivot rule for a public project: truthful, efficient, and not budget
balanced), :func:`bilateral_trade` (Myerson and Satterthwaite: the gains from trade between a buyer and a seller with
private values, under full efficiency, a posted price and the double auction's linear equilibrium),
:func:`assignment_game` (Shapley and Shubik: the efficient assignment and the core's buyer- and seller-optimal
prices).

**Evaluation.**  :func:`lottery_study` (a district that assigns seats by deferred acceptance with lottery tie-breaks:
offers are random only within applicant types, so a comparison that ignores the type is biased, and 2SLS with type
controls recovers the school's effect).

Plain numpy and scipy.
"""

from __future__ import annotations

from itertools import permutations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# deferred acceptance and the Boston rule

def deferred_acceptance(proposers: dict, receivers: dict, capacity: dict | None = None) -> dict:
    """Gale and Shapley's deferred acceptance, in rounds: every unmatched proposer applies to the best receiver that
    has not yet rejected it; each receiver holds its best applicants up to capacity (counting those already held) and
    rejects the rest.  Nothing is final until no one is rejected.  ``proposers``: name -> ranked list of receivers
    (a proposer may leave some off); ``receivers``: name -> ranked list of proposers (unlisted ones are unacceptable).
    Returns the match (proposer -> receiver or None), what each receiver holds, and a log of rounds."""
    capacity = capacity or {r: 1 for r in receivers}
    rank = {r: {p: i for i, p in enumerate(lst)} for r, lst in receivers.items()}
    nxt = {p: 0 for p in proposers}
    held = {r: [] for r in receivers}
    free = [p for p in proposers]
    log = []
    while True:
        applying = [p for p in free if nxt[p] < len(proposers[p])]
        if not applying:
            break
        props = {}
        for p in applying:
            r = proposers[p][nxt[p]]
            nxt[p] += 1
            props.setdefault(r, []).append(p)
        rejected = []
        for r, ps in props.items():
            pool = [q for q in held[r] + ps if q in rank[r]]
            rejected += [q for q in held[r] + ps if q not in rank[r]]
            pool.sort(key=lambda q: rank[r][q])
            held[r], out = pool[:capacity[r]], pool[capacity[r]:]
            rejected += out
        log.append({"proposals": [(p, r) for r, ps in props.items() for p in ps],
                    "held": {r: list(v) for r, v in held.items()}, "rejected": list(rejected)})
        free = [p for p in proposers if not any(p in v for v in held.values())]
    match = {p: next((r for r, v in held.items() if p in v), None) for p in proposers}
    return {"match": match, "held": held, "log": log, "rounds": len(log)}


def boston(students: dict, schools: dict, capacity: dict) -> dict:
    """The immediate-acceptance (Boston) rule: in round k every unassigned student applies to the k-th school on its
    list; each school admits its applicants by priority into the seats it still has, and admissions are final.
    Returns the assignment and a log of rounds."""
    rank = {s: {p: i for i, p in enumerate(lst)} for s, lst in schools.items()}
    left = dict(capacity)
    assigned = {p: None for p in students}
    log = []
    k = 0
    while any(assigned[p] is None and k < len(students[p]) for p in students):
        apps = {}
        for p in students:
            if assigned[p] is None and k < len(students[p]):
                apps.setdefault(students[p][k], []).append(p)
        admitted = []
        for s, ps in apps.items():
            ps = sorted([q for q in ps if q in rank[s]], key=lambda q: rank[s][q])
            take = ps[:left[s]]
            for q in take:
                assigned[q] = s
            left[s] -= len(take)
            admitted += [(q, s) for q in take]
        log.append({"round": k + 1, "applications": [(p, s) for s, ps in apps.items() for p in ps],
                    "admitted": admitted})
        k += 1
    return {"match": assigned, "log": log}


def blocking_pairs(match: dict, prefs_a: dict, prefs_b: dict, capacity: dict | None = None) -> list:
    """Pairs (a, b) who both prefer each other to what the match gives them (b has a free seat, or holds someone it
    ranks below a).  ``match``: a -> b or None."""
    capacity = capacity or {b: 1 for b in prefs_b}
    holders = {b: [a for a, x in match.items() if x == b] for b in prefs_b}
    out = []
    for a, lst in prefs_a.items():
        cur = match.get(a)
        better = lst[:lst.index(cur)] if cur in lst else lst
        for b in better:
            if a not in prefs_b[b]:
                continue
            rb = prefs_b[b]
            if len(holders[b]) < capacity[b] or any(rb.index(a) < rb.index(h) for h in holders[b] if h in rb):
                out.append((a, b))
    return out


def all_stable(prefs_a: dict, prefs_b: dict) -> list:
    """Every stable one-to-one matching of a small, complete market (equal numbers, everyone acceptable), by
    enumeration.  Returned with each side's ranks, sorted from the a-side's best to its worst."""
    A, B = list(prefs_a), list(prefs_b)
    out = []
    for perm in permutations(B):
        m = dict(zip(A, perm))
        if not blocking_pairs(m, prefs_a, prefs_b):
            ra = sum(prefs_a[a].index(m[a]) for a in A)
            rb = sum(prefs_b[b].index(a) for a, b in m.items())
            out.append({"match": m, "rank_a": ra, "rank_b": rb})
    return sorted(out, key=lambda r: r["rank_a"])


def outcomes_by_report(who: str, students: dict, schools: dict, capacity: dict, rule: str = "boston") -> list:
    """What ``who`` is assigned for every ordering of its list, the others reporting truthfully, under the Boston
    rule or deferred acceptance (students proposing)."""
    out = []
    for perm in permutations(students[who]):
        rep = dict(students)
        rep[who] = list(perm)
        if rule == "boston":
            m = boston(rep, schools, capacity)["match"]
        else:
            m = deferred_acceptance(rep, schools, capacity)["match"]
        out.append({"report": list(perm), "gets": m[who], "match": m})
    return out


# ---------------------------------------------------------------------------------------------------------------
# top trading cycles and kidney exchange

def top_trading_cycles(prefs: dict) -> dict:
    """Shapley and Scarf's housing market, solved by Gale's top trading cycles: each agent owns its own house
    (named by the agent) and ranks houses; each points to the owner of its favourite remaining house; there is always
    a cycle; everyone in it gets the house they point at and leaves; repeat.  Returns the allocation and the cycles in
    the order they cleared."""
    left = set(prefs)
    alloc, cycles = {}, []
    while left:
        point = {a: next(h for h in prefs[a] if h in left) for a in left}
        a = next(iter(sorted(left)))
        seen = []
        while a not in seen:
            seen.append(a)
            a = point[a]
        cyc = seen[seen.index(a):]
        for x in cyc:
            alloc[x] = point[x]
        cycles.append([(x, point[x]) for x in cyc])
        left -= set(cyc)
    return {"alloc": alloc, "cycles": cycles}


def _cycles(compat: dict, k: int) -> list:
    nodes = sorted(compat)
    out = set()
    for start in nodes:
        stack = [(start, [start])]
        while stack:
            u, path = stack.pop()
            for v in compat[u]:
                if v == start and 2 <= len(path) <= k:
                    out.add(tuple(path))
                elif v not in path and v > start and len(path) < k and v in compat:
                    stack.append((v, path + [v]))
    return [list(c) for c in out]


def kidney_exchange(compat: dict, max_cycle: int = 3, altruists: dict | None = None, max_chain: int = 4) -> dict:
    """The most transplants in a small pool.  ``compat``: pair -> set of pairs whose patient can take that pair's
    donor's kidney; ``altruists``: donor -> set of pairs it can give to (a chain starts there and passes along pairs,
    its last donor giving later or to the waiting list).  Searches disjoint sets of cycles (length 2..max_cycle) and
    chains (up to max_chain pairs) exhaustively.  Returns the best set, the transplant count, and the counts allowed
    by pairs only (k = 2), cycles up to max_cycle, and cycles with chains."""
    altruists = altruists or {}
    cyc2 = _cycles(compat, 2)
    cyck = _cycles(compat, max_cycle)
    chains = []
    for d, first in altruists.items():
        stack = [[p] for p in sorted(first)]
        while stack:
            path = stack.pop()
            chains.append({"donor": d, "path": path})
            if len(path) < max_chain:
                for v in sorted(compat.get(path[-1], ())):
                    if v not in path:
                        stack.append(path + [v])

    def best(items, used_d=frozenset()):
        items = sorted(items, key=lambda it: -it["n"])
        best_set, best_n = [], 0

        def rec(i, used, chosen, n, donors):
            nonlocal best_set, best_n
            if n > best_n:
                best_set, best_n = list(chosen), n
            if i >= len(items) or n + sum(it["n"] for it in items[i:]) <= best_n:
                return
            it = items[i]
            if not (set(it["pairs"]) & used) and it.get("donor") not in donors:
                rec(i + 1, used | set(it["pairs"]), chosen + [it], n + it["n"],
                    donors | ({it["donor"]} if it.get("donor") else set()))
            rec(i + 1, used, chosen, n, donors)

        rec(0, set(), [], 0, set(used_d))
        return best_set, best_n

    def as_items(cs):
        return [{"kind": "cycle", "pairs": c, "n": len(c)} for c in cs]

    chain_items = [{"kind": "chain", "pairs": ch["path"], "n": len(ch["path"]), "donor": ch["donor"]} for ch in chains]
    s2, n2 = best(as_items(cyc2))
    sk, nk = best(as_items(cyck))
    sc, nc = best(as_items(cyck) + chain_items)
    return {"pairs_only": n2, "cycles": nk, "with_chains": nc, "best": sc, "best_pairs_only": s2,
            "best_cycles": sk, "n_pairs": len(compat), "two_cycles": cyc2, "k_cycles": cyck}


# ---------------------------------------------------------------------------------------------------------------
# mechanisms with money

def pivotal(values, cost: float) -> dict:
    """Clarke's pivot mechanism for a public project costing ``cost``, shared equally: each reports a value; build
    if the reported net values (value less the equal share) sum to at least zero; a person whose report flips the
    decision pays the net loss it imposes on the others.  Truth is dominant, the decision efficient, and the taxes
    cannot be handed back without spoiling the incentives: the budget does not balance."""
    v = np.asarray(values, float)
    n = len(v)
    u = v - cost / n
    build = bool(u.sum() >= 0)
    tax = np.zeros(n)
    for i in range(n):
        others = u.sum() - u[i]
        if (others >= 0) != build:
            tax[i] = abs(others)
    return {"values": v.tolist(), "net": u.tolist(), "build": build, "tax": tax.tolist(), "surplus": float(tax.sum()),
            "pivotal": [i for i in range(n) if tax[i] > 0], "share": cost / n}


def bilateral_trade(draws: int = 200000, seed: int = 1983) -> dict:
    """A buyer values a good at v and its owner at c, both uniform on [0, 1] and private.  Full efficiency would
    trade whenever v > c, for expected gains of 1/6; Myerson and Satterthwaite (1983) show no voluntary, budget-
    balanced mechanism with truthful reports can.  A posted price of 1/2 gets 1/8; the double auction's linear
    equilibrium (Chatterjee and Samuelson), trading when v >= c + 1/4, gets 9/64, the most any such mechanism can.
    Returns the closed forms and a simulation check."""
    rng = np.random.default_rng(seed)
    v, c = rng.uniform(0, 1, draws), rng.uniform(0, 1, draws)
    gain = v - c
    sim = {"efficient": float(np.mean(np.where(v > c, gain, 0))),
           "posted": float(np.mean(np.where((c <= 0.5) & (v >= 0.5), gain, 0))),
           "double": float(np.mean(np.where(v >= c + 0.25, gain, 0)))}
    exact = {"efficient": 1 / 6, "posted": 1 / 8, "double": 9 / 64}
    p_trade = {"efficient": 0.5, "posted": 0.25, "double": 0.5 * 0.75 ** 2}
    return {"exact": exact, "sim": sim, "p_trade": p_trade,
            "share": {k: exact[k] / exact["efficient"] for k in exact}}


def assignment_game(values) -> dict:
    """Shapley and Shubik's assignment game: ``values[i][j]`` is what buyer i and seller j create together.  Finds
    the efficient assignment and, by linear programming, the core's two extreme price vectors: buyer-optimal (lowest
    seller payoffs) and seller-optimal.  Every core allocation splits each matched pair's surplus with no pair able
    to do better apart."""
    from scipy.optimize import linprog

    a = np.asarray(values, float)
    nb, ns = a.shape
    best, best_v = None, -1.0
    for perm in permutations(range(ns), nb):
        tot = sum(a[i, perm[i]] for i in range(nb))
        if tot > best_v:
            best, best_v = perm, tot
    A_ub, b_ub = [], []
    for i in range(nb):
        for j in range(ns):
            row = np.zeros(nb + ns)
            row[i], row[nb + j] = -1, -1
            A_ub.append(row)
            b_ub.append(-a[i, j])
    A_eq = [np.ones(nb + ns)]
    b_eq = [best_v]
    bounds = [(0, None)] * (nb + ns)
    sell = linprog(np.r_[np.zeros(nb), -np.ones(ns)], A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    buy = linprog(np.r_[-np.ones(nb), np.zeros(ns)], A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    return {"assign": [int(j) for j in best], "total": float(best_v),
            "seller_optimal": {"buyers": sell.x[:nb].tolist(), "sellers": sell.x[nb:].tolist()},
            "buyer_optimal": {"buyers": buy.x[:nb].tolist(), "sellers": buy.x[nb:].tolist()}}


# ---------------------------------------------------------------------------------------------------------------
# what a lottery reveals

def lottery_study(students: int = 4000, effect: float = 0.4, seats: int = 600, seed: int = 2017,
                  sibling_share: float = 0.25, always_takers: float = 0.3) -> dict:
    """A district with one oversubscribed school.  Students have a latent achievement a ~ N(0, 1).  Applying is more
    common among stronger students; some applicants have a sibling priority, which is more common among weaker ones
    (an applicant type).  Seats go by deferred acceptance with a single lottery: siblings first, then lottery order.
    Some applicants who get no offer enrol anyway later (always-takers).  Scores: a + effect x attend + noise.

    Returns the true effect and four estimates: attenders against everyone else (OLS), offered against not offered
    with no controls (a 2SLS that ignores types), and 2SLS controlling for the type (the offer is random within it),
    plus the first stage and each type's offer rate."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0, 1, students)
    apply_ = rng.uniform(size=students) < 1 / (1 + np.exp(-(0.8 * a - 0.2)))
    sib = apply_ & (rng.uniform(size=students) < sibling_share * (1 - 0.5 * np.tanh(a)))
    lot = rng.uniform(size=students)
    order = np.lexsort((lot, ~sib))                       # siblings first, then lottery
    order = [i for i in order if apply_[i]]
    offer = np.zeros(students, bool)
    offer[order[:seats]] = True
    late = apply_ & ~offer & (rng.uniform(size=students) < always_takers)
    attend = offer | late
    y = a + effect * attend + rng.normal(0, 0.5, students)
    ap = np.where(apply_)[0]

    def ols(Y, X):
        X = np.column_stack([np.ones(len(Y)), X])
        return np.linalg.lstsq(X, Y, rcond=None)[0]

    naive = ols(y, attend.astype(float))[1]
    yA, dA, zA, tA = y[ap], attend[ap].astype(float), offer[ap].astype(float), sib[ap].astype(float)
    fs0 = ols(dA, zA)[1]
    rf0 = ols(yA, zA)[1]
    fs1 = ols(dA, np.column_stack([zA, tA]))[1]
    rf1 = ols(yA, np.column_stack([zA, tA]))[1]
    rate = {"siblings": float(offer[ap][sib[ap]].mean()) if sib[ap].any() else float("nan"),
            "others": float(offer[ap][~sib[ap]].mean())}
    return {"effect": effect, "ols_everyone": float(naive), "iv_no_controls": float(rf0 / fs0),
            "iv_type_controls": float(rf1 / fs1), "first_stage": float(fs1), "offer_rate": rate,
            "applicants": int(apply_.sum()), "seats": seats, "siblings": int(sib.sum()),
            "mean_a": {"applicants": float(a[ap].mean()), "others": float(a[~apply_].mean()),
                       "siblings": float(a[ap][sib[ap]].mean()), "lottery": float(a[ap][~sib[ap]].mean())}}
