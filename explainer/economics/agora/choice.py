"""Social choice and welfare (Part 18): voting rules on a profile, majority cycles, agendas, Arrow's axioms checked
on the rules, single-peaked preferences and the median voter, manipulation, and social welfare functions over a
distribution of incomes.

**Voting.**  A profile is a list of ``(count, ranking)`` with rankings as tuples of candidate names, best first.
:func:`plurality`, :func:`runoff` (the top two, then a majority vote), :func:`instant_runoff`, :func:`borda`,
:func:`pairwise` (every head-to-head count), :func:`condorcet_winner`, :func:`copeland`, :func:`all_rules`;
:func:`agenda_winner` (sequential pairwise votes in a fixed order) and :func:`agendas` (which order makes whom win);
:func:`majority_cycle` (Condorcet's three voters).

**Axioms.**  :func:`iia_violation` (a pair of profiles that agree on how everyone ranks two candidates but where a rule
ranks them differently: Borda fails independence of irrelevant alternatives), :func:`transitivity_violation`
(majority rule's cycle), :func:`geanakoplos_pivot` (Geanakoplos's first step, run on a dictatorship or a rule that
satisfies Pareto and independence: move a candidate from bottom to top one voter at a time and find the voter at whom
society's ranking flips).

**Ways out and around.**  :func:`single_peaked` (voters with peaks on a line: the median peak beats every
alternative), :func:`manipulations` (every voter who gains by misreporting under a rule: Gibbard and Satterthwaite).

**Welfare.**  :func:`welfare` (utilitarian, Rawlsian and Atkinson's family on a distribution of incomes, with the
equally-distributed equivalent and Atkinson's index), :func:`veil` (Harsanyi's and Rawls's choices behind the veil
between two societies), :func:`scitovsky` (a compensation test that passes both ways), :func:`liberal_paradox` (Sen's
two readers and one book).

Plain numpy.
"""

from __future__ import annotations

from itertools import permutations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# voting rules

def candidates(profile) -> list:
    return sorted(profile[0][1])


def plurality(profile) -> dict:
    """First-place votes; the most wins."""
    tally = {c: 0 for c in candidates(profile)}
    for n, r in profile:
        tally[r[0]] += n
    return {"tally": tally, "winner": max(tally, key=lambda c: (tally[c], c))}


def _restrict(profile, keep):
    return [(n, tuple(c for c in r if c in keep)) for n, r in profile]


def _majority(profile, a, b) -> int:
    """Voters who rank a above b."""
    return sum(n for n, r in profile if r.index(a) < r.index(b))


def runoff(profile) -> dict:
    """The top two by first-place votes meet in a second round."""
    p = plurality(profile)["tally"]
    a, b = sorted(p, key=lambda c: (-p[c], c))[:2]
    va, vb = _majority(profile, a, b), _majority(profile, b, a)
    return {"finalists": (a, b), "votes": (va, vb), "winner": a if va >= vb else b}


def instant_runoff(profile) -> dict:
    """Drop the candidate with the fewest first places, transfer those ballots, repeat until someone has a majority."""
    keep = set(candidates(profile))
    rounds = []
    total = sum(n for n, _ in profile)
    while True:
        t = plurality(_restrict(profile, keep))["tally"]
        rounds.append(dict(t))
        top = max(t, key=lambda c: (t[c], c))
        if t[top] * 2 > total or len(keep) == 1:
            return {"rounds": rounds, "winner": top}
        keep.discard(min(t, key=lambda c: (t[c], c)))


def borda(profile) -> dict:
    """With m candidates, a ballot gives m - 1 points to its first, m - 2 to its second, ... 0 to its last."""
    cs = candidates(profile)
    m = len(cs)
    pts = {c: 0 for c in cs}
    for n, r in profile:
        for k, c in enumerate(r):
            pts[c] += n * (m - 1 - k)
    return {"points": pts, "winner": max(pts, key=lambda c: (pts[c], c)),
            "ranking": sorted(cs, key=lambda c: (-pts[c], c))}


def pairwise(profile) -> dict:
    cs = candidates(profile)
    return {a: {b: _majority(profile, a, b) for b in cs if b != a} for a in cs}


def condorcet_winner(profile):
    """The candidate who beats every other head to head, or None."""
    pw = pairwise(profile)
    for a, row in pw.items():
        if all(v > pw[b][a] for b, v in row.items()):
            return a
    return None


def copeland(profile) -> dict:
    pw = pairwise(profile)
    score = {a: sum(1 for b, v in row.items() if v > pw[b][a]) for a, row in pw.items()}
    return {"score": score, "winner": max(score, key=lambda c: (score[c], c))}


def all_rules(profile) -> dict:
    return {"plurality": plurality(profile)["winner"], "runoff": runoff(profile)["winner"],
            "instant runoff": instant_runoff(profile)["winner"], "Borda": borda(profile)["winner"],
            "Condorcet": condorcet_winner(profile)}


def agenda_winner(profile, order) -> str:
    """Sequential pairwise voting: the first two meet, the winner meets the third, and so on."""
    champ = order[0]
    for c in order[1:]:
        champ = champ if _majority(profile, champ, c) >= _majority(profile, c, champ) else c
    return champ


def agendas(profile) -> dict:
    """For each candidate, the agendas (orders of votes) under which it wins."""
    out = {c: [] for c in candidates(profile)}
    for order in permutations(candidates(profile)):
        out[agenda_winner(profile, order)].append(order)
    return out


def majority_cycle() -> dict:
    """Condorcet's three voters: A > B > C, B > C > A, C > A > B.  Each pair is decided 2 to 1, in a circle."""
    prof = [(1, ("A", "B", "C")), (1, ("B", "C", "A")), (1, ("C", "A", "B"))]
    pw = pairwise(prof)
    return {"profile": prof, "pairwise": pw,
            "cycle": [("A", "B", pw["A"]["B"]), ("B", "C", pw["B"]["C"]), ("C", "A", pw["C"]["A"])],
            "agendas": {c: len(v) for c, v in agendas(prof).items()}}


# ---------------------------------------------------------------------------------------------------------------
# Arrow's axioms, checked

def iia_violation(profile, rule=None) -> dict:
    """Independence of irrelevant alternatives says society's ranking of a and b depends only on how each voter ranks
    a and b.  Search for a voter type and a reordering of the OTHER candidates in that type's ranking (leaving the
    a-b order alone) that flips Borda's ranking of a pair: a counterexample."""
    rule = rule or _borda_ranking
    base = rule(profile)
    cs = candidates(profile)
    for i, (n, r) in enumerate(profile):
        for perm in permutations(r):
            for a in cs:
                for b in cs:
                    if a >= b or (perm.index(a) < perm.index(b)) != (r.index(a) < r.index(b)):
                        continue
                    new = list(profile)
                    new[i] = (n, perm)
                    rk = rule(new)
                    if (base.index(a) < base.index(b)) != (rk.index(a) < rk.index(b)):
                        out = {"type": i, "before": r, "after": perm, "pair": (a, b), "ranking_before": base,
                               "ranking_after": rk}
                        if rule is _borda_ranking:
                            out["points_before"] = borda(profile)["points"]
                            out["points_after"] = borda(new)["points"]
                        return out
    return {}


def _borda_ranking(profile):
    return borda(profile)["ranking"]


def transitivity_violation(profile) -> list:
    """Majority rule's strict social preferences that form a cycle of length three, if any."""
    pw = pairwise(profile)
    cs = candidates(profile)
    out = []
    for a, b, c in permutations(cs, 3):
        if pw[a][b] > pw[b][a] and pw[b][c] > pw[c][b] and pw[c][a] > pw[a][c] and a == min(a, b, c):
            out.append((a, b, c))
    return out


def geanakoplos_pivot(n_voters: int = 5, rule: str = "dictator", dictator: int = 2) -> dict:
    """Geanakoplos's proof, step one: start with every voter ranking b last (so, by Pareto, society ranks b last),
    then move b to the top of voters' rankings one at a time.  For any rule satisfying Pareto and independence, at
    some voter society's ranking of b jumps from bottom to top: that voter is pivotal, and the proof goes on to show
    the pivotal voter is a dictator.  Here the rule is a dictatorship (of voter ``dictator``) or a Pareto-and-
    -unanimity rule; returns society's position for b after each move."""
    base = [("a", "c", "b") if k % 2 == 0 else ("c", "a", "b") for k in range(n_voters)]
    pos = []
    for k in range(n_voters + 1):
        prof = [("b",) + tuple(x for x in base[j] if x != "b") if j < k else base[j] for j in range(n_voters)]
        if rule == "dictator":
            social = prof[dictator]
        else:
            social = borda([(1, r) for r in prof])["ranking"]
        pos.append(social.index("b"))
    jump = next((k for k in range(1, len(pos)) if pos[k] == 0 and pos[k - 1] == 2), None)
    return {"positions": pos, "pivot": None if jump is None else jump - 1, "n": n_voters}


# ---------------------------------------------------------------------------------------------------------------
# single peaks and manipulation

def single_peaked(peaks, options=None) -> dict:
    """Voters with ideal points ``peaks`` on a line, who prefer options nearer their peak.  Returns the median peak,
    each option's head-to-head record, and the Condorcet winner (the option nearest the median, when the options
    include it)."""
    peaks = np.asarray(peaks, float)
    options = np.asarray(options if options is not None else np.unique(peaks), float)
    med = float(np.median(peaks))
    wins = {}
    for x in options:
        wins[float(x)] = sum(1 for y in options if y != x and np.sum(np.abs(peaks - x) < np.abs(peaks - y)) >
                             np.sum(np.abs(peaks - y) < np.abs(peaks - x)))
    cw = [x for x, w in wins.items() if w == len(options) - 1]
    return {"peaks": peaks.tolist(), "median": med, "wins": wins, "condorcet": cw[0] if cw else None,
            "mean": float(peaks.mean())}


def _relabel(profile, m):
    return [(n, tuple(m[c] for c in r)) for n, r in profile]


def robust_winner(fn, profile):
    """The winner under ``fn`` if it doesn't hang on a tie: the rules break ties by letter, so run the rule again with
    the letters' order reversed; None if the two runs disagree."""
    cs = candidates(profile)
    m = dict(zip(cs, reversed(cs)))
    w = fn(profile)
    return w if m[fn(_relabel(profile, m))] == w else None


def manipulations(profile, rule) -> list:
    """Every voter type whose members, all voting the same false ranking, would get a winner they all truly prefer to
    the honest one, the others voting honestly (Gibbard and Satterthwaite: every rule with three or more options that
    is not a dictatorship can be manipulated somewhere; here, by a bloc).  Only lies that win outright count, not those
    that make a tie broken by letter.  One lie per type: the one with the best result for it, the first found."""
    fn = {"plurality": lambda p: plurality(p)["winner"], "Borda": lambda p: borda(p)["winner"],
          "instant runoff": lambda p: instant_runoff(p)["winner"], "runoff": lambda p: runoff(p)["winner"]}[rule]
    honest = fn(profile)
    out = []
    for i, (n, r) in enumerate(profile):
        best = None
        for lie in permutations(r):
            if lie == r:
                continue
            new = list(profile)
            new[i] = (n, lie)
            w = robust_winner(fn, new)
            if w is None:
                continue
            if r.index(w) < r.index(honest) and (best is None or r.index(w) < r.index(best["new_winner"])):
                best = {"type": i, "count": n, "truth": r, "lie": lie, "honest_winner": honest, "new_winner": w}
        if best:
            out.append(best)
    return out


# ---------------------------------------------------------------------------------------------------------------
# welfare

def welfare(incomes, epsilons=(0.0, 0.5, 1.0, 2.0, 5.0)) -> dict:
    """Social welfare from a distribution of incomes: utilitarian (the mean), Rawlsian (the minimum), and Atkinson's
    family with inequality aversion epsilon: the equally-distributed equivalent income
    y_e = (mean of y^(1 - e))^(1 / (1 - e)) (geometric mean at e = 1), and Atkinson's index 1 - y_e / mean."""
    y = np.asarray(incomes, float)
    mu = float(y.mean())
    out = {"mean": mu, "min": float(y.min()), "ede": {}, "atkinson": {}}
    for e in epsilons:
        if e == 1.0:
            ye = float(np.exp(np.mean(np.log(y))))
        else:
            ye = float(np.mean(y ** (1 - e)) ** (1 / (1 - e)))
        out["ede"][e] = ye
        out["atkinson"][e] = 1 - ye / mu
    return out


def veil(society_a, society_b, epsilons=(0.0, 1.0, 2.0, 5.0, 20.0)) -> dict:
    """Behind the veil, you will be a random member of society A or of society B.  Harsanyi: choose the higher
    expected utility (here, utility of income with constant relative risk aversion e); Rawls: choose the higher
    minimum.  Returns each choice; as e grows, Harsanyi's choice converges to Rawls's."""
    a, b = welfare(society_a, epsilons), welfare(society_b, epsilons)
    harsanyi = {e: "A" if a["ede"][e] >= b["ede"][e] else "B" for e in epsilons}
    return {"A": a, "B": b, "rawls": "A" if a["min"] >= b["min"] else "B", "harsanyi": harsanyi,
            "society_a": list(map(float, society_a)), "society_b": list(map(float, society_b))}


def scitovsky() -> dict:
    """Scitovsky's reversal.  Two islanders, two goods (fish and fruit), utility x*y.  In state 1, Ana has (6, 1) and Bo
    (1, 6), totals (7, 7); in state 2, Ana has (1, 4) and Bo (7, 3), totals (8, 7).  Kaldor's test asks whether the
    totals of the new state could be split so that nobody is worse off than in the old one and someone is better off.
    The function checks the test both ways and reports a split that passes each; here both moves pass."""
    def u(b):
        return b[0] * b[1]

    s1 = {"Ana": (6.0, 1.0), "Bo": (1.0, 6.0)}            # totals (7, 7)
    s2 = {"Ana": (1.0, 4.0), "Bo": (7.0, 3.0)}            # totals (8, 7)

    def kaldor(frm, to):
        """Can the totals of ``to`` be split so that both are at least as well off as in ``frm``, one strictly?"""
        tx = to["Ana"][0] + to["Bo"][0]
        ty = to["Ana"][1] + to["Bo"][1]
        ua, ub = u(frm["Ana"]), u(frm["Bo"])
        grid = np.linspace(0, 1, 401)
        for fx in grid:
            for fy in grid:
                a = (fx * tx, fy * ty)
                bb = (tx - a[0], ty - a[1])
                if u(a) >= ua and u(bb) >= ub and (u(a) > ua or u(bb) > ub):
                    return True, a, bb
        return False, None, None

    p12, a12, b12 = kaldor(s1, s2)
    p21, a21, b21 = kaldor(s2, s1)
    return {"s1": s1, "s2": s2, "utility_s1": {k: u(v) for k, v in s1.items()},
            "utility_s2": {k: u(v) for k, v in s2.items()}, "1_to_2": p12, "2_to_1": p21,
            "split_12": (a12, b12), "split_21": (a21, b21)}


def liberal_paradox() -> dict:
    """Sen's prude and lewd, and one copy of a scandalous book.  Options: the prude reads it (p), the lewd reads it
    (l), nobody does (n).  The prude ranks n > p > l; the lewd ranks p > l > n.  Liberalism gives each the say over
    their own reading: the prude decides n against p (so n beats p), the lewd decides l against n (so l beats n).
    Pareto: both prefer p to l (so p beats l).  A cycle: n > p > l > n."""
    prude, lewd = ("n", "p", "l"), ("p", "l", "n")
    return {"prude": prude, "lewd": lewd, "liberal": [("n", "p", "prude"), ("l", "n", "lewd")],
            "pareto": ("p", "l"), "cycle": ("n", "p", "l")}
