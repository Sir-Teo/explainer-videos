"""Games and the social contract, built (Part 34).

* Nash equilibria of bimatrix games by support enumeration; best-response correspondences for 2x2 games.
* The commons as a Cournot game: equilibrium against optimum as the number of herders grows; a public goods game with
  and without graduated sanctions (Ostrom).
* The stag hunt: basins, risk dominance and stochastic stability (Kandori, Mailath and Rob 1993).
* The centipede: backward induction, and logit quantal response (McKelvey and Palfrey 1998).
* Correlated equilibrium (Aumann 1974) by linear programming, on chicken.
* The shadow of the future: every deterministic memory-one strategy against grim and tit for tat, by discount factor;
  the folk theorem, with the patience each cyclic plan needs to be a subgame-perfect equilibrium under grim trigger.
* The iterated prisoner's dilemma: a strategy zoo with noise; Axelrod's ecological tournament; memory-one strategies
  as Markov chains; Press and Dyson's zero-determinant strategies; evolution in a finite population with rare
  mutations (Imhof, Fudenberg and Nowak 2005).
* Skyrms's Nash demand game: basins of fair division on the simplex.
* Bargaining: Nash, Kalai-Smorodinsky, Rubinstein.
* The Shapley value by permutations; Harsanyi dividends; SHAP on a tiny model.
* Auctions: second-price truthfulness, first-price shading, revenue equivalence, Myerson's reserve; GSP against VCG.
* Gale and Shapley's deferred acceptance: stability, proposer-optimality, strategy-proofness for proposers.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

PD = {"T": 5, "R": 3, "P": 1, "S": 0}


# ---------------------------------------------------------------------------
# Nash equilibria by support enumeration
# ---------------------------------------------------------------------------
def nash_equilibria(A, B, tol: float = 1e-9) -> list[dict]:
    """All Nash equilibria of a nondegenerate bimatrix game (row payoffs A, column payoffs B), by enumerating equal-size
    supports, solving the indifference conditions, and keeping the solutions that are probability vectors with no
    profitable deviation."""
    A, B = np.asarray(A, float), np.asarray(B, float)
    m, n = A.shape
    out = []
    for k in range(1, min(m, n) + 1):
        for I in itertools.combinations(range(m), k):
            for J in itertools.combinations(range(n), k):
                # column mix y on J makes row indifferent over I; row mix x on I makes column indifferent over J
                def solve(M, rows, cols):
                    # unknowns: probabilities on cols (k) and the value v; equations: M[rows, cols] y - v = 0, sum y = 1
                    kk = len(cols)
                    lhs = np.zeros((kk + 1, kk + 1))
                    rhs = np.zeros(kk + 1)
                    lhs[:kk, :kk] = M[np.ix_(rows, cols)]
                    lhs[:kk, kk] = -1
                    lhs[kk, :kk] = 1
                    rhs[kk] = 1
                    try:
                        sol = np.linalg.solve(lhs, rhs)
                    except np.linalg.LinAlgError:
                        return None
                    return sol[:kk], sol[kk]
                r1 = solve(A, list(I), list(J))
                r2 = solve(B.T, list(J), list(I))
                if r1 is None or r2 is None:
                    continue
                yJ, vA = r1
                xI, vB = r2
                if (yJ < -tol).any() or (xI < -tol).any():
                    continue
                x = np.zeros(m)
                y = np.zeros(n)
                x[list(I)] = xI
                y[list(J)] = yJ
                if (A @ y > vA + tol).any() or (x @ B > vB + tol).any():
                    continue
                eq = {"row": [round(float(v), 4) for v in x], "col": [round(float(v), 4) for v in y],
                      "payoff": [round(float(x @ A @ y), 4), round(float(x @ B @ y), 4)]}
                if eq not in out:
                    out.append(eq)
    return out


GAMES = {
    "prisoner's dilemma": ([[3, 0], [5, 1]], [[3, 5], [0, 1]], ["cooperate", "defect"]),
    "matching pennies": ([[1, -1], [-1, 1]], [[-1, 1], [1, -1]], ["heads", "tails"]),
    "battle of the sexes": ([[2, 0], [0, 1]], [[1, 0], [0, 2]], ["opera", "football"]),
    "stag hunt": ([[4, 0], [3, 3]], [[4, 3], [0, 3]], ["stag", "hare"]),
    "chicken": ([[0, 7], [2, 6]], [[0, 2], [7, 6]], ["dare", "swerve"]),
}


def equilibria_table() -> dict:
    out = {}
    for name, (A, B, acts) in GAMES.items():
        out[name] = {"acts": acts, "A": A, "B": B, "equilibria": nash_equilibria(A, B)}
    return out


def best_responses(name: str = "battle of the sexes", n: int = 201) -> dict:
    """For a 2x2 game, the row player's best response to the column's probability q of the first act, and the column's
    to the row's p: step correspondences, vertical at the indifference point. Their crossings are the equilibria
    (Kakutani's theorem guarantees one in general)."""
    A, B, acts = GAMES[name]
    A, B = np.asarray(A, float), np.asarray(B, float)
    # row indifferent when q A00 + (1-q) A01 = q A10 + (1-q) A11
    q_star = (A[1, 1] - A[0, 1]) / (A[0, 0] - A[0, 1] - A[1, 0] + A[1, 1])
    p_star = (B[1, 1] - B[1, 0]) / (B[0, 0] - B[1, 0] - B[0, 1] + B[1, 1])
    row_high = A[0, 0] - A[1, 0] > 0      # does the row prefer act 0 when q = 1?
    col_high = B[0, 0] - B[0, 1] > 0
    return {"q_star": round(float(q_star), 4), "p_star": round(float(p_star), 4), "row_first_when_q_high": bool(row_high),
            "col_first_when_p_high": bool(col_high), "equilibria": nash_equilibria(A, B), "acts": acts}


# ---------------------------------------------------------------------------
# The commons
# ---------------------------------------------------------------------------
def commons(a: float = 110.0, c: float = 10.0, ns=(1, 2, 3, 5, 10, 20, 50, 100)) -> dict:
    """Hardin (1968) as a Cournot game: n herders each graze x_i cows; each cow is worth a - X (X the total) and costs
    c. Each herder's best response gives the symmetric equilibrium x = (a - c)/(n + 1); the total (a - c) n/(n + 1)
    approaches the point where the pasture is worth nothing, while the welfare-maximizing total is (a - c)/2."""
    rows = []
    best_total = (a - c) / 2
    best_welfare = best_total * (a - best_total - c)
    for n in ns:
        x = (a - c) / (n + 1)
        X = n * x
        w = X * (a - X - c)
        rows.append({"n": n, "each": round(x, 3), "total": round(X, 3), "welfare": round(w, 2),
                     "share_of_best": round(w / best_welfare, 4)})
    return {"a": a, "c": c, "best_total": best_total, "best_welfare": best_welfare, "rows": rows}


def public_goods(n: int = 4, r: float = 1.6, rounds: int = 30, fine: float = 1.5, monitor: float = 0.1,
                 agents: int = 400, seed: int = 1990) -> dict:
    """A public goods game: each of n players keeps or contributes a unit, the pot is multiplied by r and shared. A
    contribution returns r/n = 0.4 to its giver, so keeping is dominant. Players adjust by imitation with noise (they
    copy a better-earning group member). Without sanctions contributions collapse; with Ostrom's monitored, graduated
    sanctions (a fine on each shortfall, paid for by a small monitoring cost) they stay high."""
    rng = np.random.default_rng(seed)

    def run(sanction: bool):
        groups = agents // n
        contrib = rng.random((groups, n)) < 0.6
        series = []
        for _ in range(rounds):
            series.append(round(float(contrib.mean()), 4))
            pot = contrib.sum(axis=1, keepdims=True) * r / n
            pay = pot + (~contrib) * 1.0
            if sanction:
                pay = pay - (~contrib) * fine - monitor
            # each player copies a random group member if that member earned more (with probability by the gap)
            new = contrib.copy()
            for g in range(groups):
                for i in range(n):
                    j = rng.integers(n)
                    if pay[g, j] > pay[g, i] and rng.random() < min(1.0, (pay[g, j] - pay[g, i])):
                        new[g, i] = contrib[g, j]
                    if rng.random() < 0.02:
                        new[g, i] = not new[g, i]
            contrib = new
        return series
    return {"n": n, "r": r, "return_per_unit": round(r / n, 3), "fine": fine, "monitor": monitor,
            "free": run(False), "sanctioned": run(True)}


# ---------------------------------------------------------------------------
# The stag hunt
# ---------------------------------------------------------------------------
def stag_hunt(N: int = 10, eps_values=(0.1, 0.05, 0.02), periods: int = 1000000, seed: int = 1993) -> dict:
    """Rousseau's stag hunt (stag/stag 4, stag/hare 0, hare 3 whatever the other does). Stag is payoff dominant; hare
    is risk dominant (3 + 3 > 4 + 0): stag is a best response only if at least 3/4 of others hunt stag. Kandori, Mailath
    and Rob (1993): a population of N that best-responds, with each agent mutating with probability eps, spends almost
    all its time at all-hare as eps shrinks."""
    rng = np.random.default_rng(seed)
    out = []
    for eps in eps_values:
        k = N            # number of stag hunters; start all stag
        time_hare = 0
        for _ in range(periods):
            # best response of each agent given the others (approximately the population share)
            frac = k / N
            br_stag = 4 * frac > 3
            target = N if br_stag else 0
            mutants = rng.random(N) < eps
            k = int(((~mutants) & np.array([target > 0] * N)).sum() + (mutants & (rng.random(N) < 0.5)).sum())
            time_hare += k < N / 2
        out.append({"eps": eps, "share_time_hare": round(time_hare / periods, 4)})
    return {"threshold": 0.75, "basin_stag": 0.25, "basin_hare": 0.75, "N": N, "runs": out}


# ---------------------------------------------------------------------------
# The centipede and quantal response
# ---------------------------------------------------------------------------
def centipede(nodes: int = 6, lambdas=(0.0, 0.5, 1.0, 2.0, 5.0, 20.0)) -> dict:
    """A centipede of `nodes` moves: at node k the mover may take (getting the larger part of the pot) or pass (the
    pot doubles). Pot at node k is 2^(k+2) split 0.8/0.2; if the last mover passes, the doubled pot goes 0.8/0.2 to the
    other. Backward induction: take at once. A noisy best response solved backward, in the spirit of McKelvey and
    Palfrey's logit quantal response (1998): each mover takes with probability 1/(1 + exp(-lambda g)), g the relative
    gain from taking. With moderate lambda players pass early and take late, the pattern of experiments."""
    def payoffs_take(k):
        pot = 2 ** (k + 2)
        big, small = 0.8 * pot, 0.2 * pot
        mover = k % 2
        return (big, small) if mover == 0 else (small, big)
    final_pot = 2 ** (nodes + 2)
    last = (nodes - 1) % 2                       # if the last mover passes, the other gets the larger part
    end = (0.8 * final_pot, 0.2 * final_pot) if last == 1 else (0.2 * final_pot, 0.8 * final_pot)
    rows = []
    for lam in lambdas:
        cont = end
        probs = []
        for k in reversed(range(nodes)):
            mover = k % 2
            take = payoffs_take(k)
            vt, vp = take[mover], cont[mover]
            if lam == float("inf"):
                pt = 1.0 if vt >= vp else 0.0
            else:
                z = lam * (vt - vp) / max(abs(vt), abs(vp), 1.0)
                pt = 1 / (1 + math.exp(-z))
            probs.append(pt)
            cont = tuple(pt * take[i] + (1 - pt) * cont[i] for i in range(2))
        probs = list(reversed(probs))
        reach, dist = 1.0, []
        for pt in probs:
            dist.append(round(reach * pt, 4))
            reach *= 1 - pt
        rows.append({"lambda": lam, "p_take": [round(p, 4) for p in probs], "ends_at": dist + [round(reach, 4)]})
    bi = []
    cont = end
    for k in reversed(range(nodes)):
        mover = k % 2
        take = payoffs_take(k)
        t = take[mover] >= cont[mover]
        bi.append(t)
        cont = take if t else cont
    return {"nodes": nodes, "take_payoffs": [list(payoffs_take(k)) for k in range(nodes)], "end": list(end),
            "backward_takes_everywhere": all(bi), "spe_payoff": list(payoffs_take(0)), "qre": rows}


# ---------------------------------------------------------------------------
# Correlated equilibrium
# ---------------------------------------------------------------------------
def correlated_chicken() -> dict:
    """Aumann (1974) on chicken (dare/dare 0, dare/swerve 7 and 2, swerve/swerve 6): the Nash equilibria give (7, 2),
    (2, 7) and, mixed, 14/3 each. A correlation device (a traffic light) recommending each cell with some probability is
    a correlated equilibrium if no one gains by disobeying; the set is a polytope, and the welfare-maximizing point,
    found by linear programming, gives 5.25 each."""
    from scipy.optimize import linprog
    A, B, acts = GAMES["chicken"]
    A, B = np.asarray(A, float), np.asarray(B, float)
    # variables: p00 p01 p10 p11 (row act, col act); obedience constraints
    cons, rhs = [], []
    for i in range(2):
        for i2 in range(2):
            if i2 == i:
                continue
            row = np.zeros(4)
            for j in range(2):
                row[2 * i + j] = -(A[i, j] - A[i2, j])
            cons.append(row)
            rhs.append(0)
    for j in range(2):
        for j2 in range(2):
            if j2 == j:
                continue
            row = np.zeros(4)
            for i in range(2):
                row[2 * i + j] = -(B[i, j] - B[i, j2])
            cons.append(row)
            rhs.append(0)
    c = -(A.flatten() + B.flatten())
    res = linprog(c, A_ub=np.array(cons), b_ub=np.array(rhs), A_eq=[np.ones(4)], b_eq=[1], bounds=[(0, 1)] * 4)
    p = res.x
    uniform = np.array([0, 1 / 3, 1 / 3, 1 / 3])
    return {"acts": acts, "best": [round(float(v), 4) for v in p],
            "best_payoff": [round(float(p @ A.flatten()), 4), round(float(p @ B.flatten()), 4)],
            "uniform_payoff": [round(float(uniform @ A.flatten()), 4), round(float(uniform @ B.flatten()), 4)],
            "nash": nash_equilibria(A, B)}


# ---------------------------------------------------------------------------
# The iterated prisoner's dilemma
# ---------------------------------------------------------------------------
def _pd_pay(a, b):
    T, R, P, S = PD["T"], PD["R"], PD["P"], PD["S"]
    return {("C", "C"): (R, R), ("C", "D"): (S, T), ("D", "C"): (T, S), ("D", "D"): (P, P)}[(a, b)]


# ---------------------------------------------------------------------------
# The shadow of the future: repeated games and the folk theorem
# ---------------------------------------------------------------------------
_OUT = [("C", "C"), ("C", "D"), ("D", "C"), ("D", "D")]


def _memory_one_strategies():
    """All 32 deterministic memory-one strategies: a first move, then a move after each (my last, their last)."""
    for first in "CD":
        for resp in itertools.product("CD", repeat=4):
            yield first + "".join(resp), first, dict(zip(_OUT, resp))


def _play_value(first, resp, opponent: str, delta: float, rounds: int = 4000) -> float:
    """Normalized discounted payoff (1 - delta) sum delta^t u_t of a memory-one strategy against grim or tit for tat."""
    me, triggered, last = first, False, None
    total, w = 0.0, 1.0
    for t in range(rounds):
        if opponent == "grim":
            them = "D" if triggered else "C"
        else:
            them = "C" if last is None else last[0]
        total += w * _pd_pay(me, them)[0]
        w *= delta
        if w < 1e-15:
            break
        if me == "D":
            triggered = True
        last = (me, them)
        me = resp[last]
    return (1 - delta) * total


def shadow(deltas=None) -> dict:
    """Against grim and against tit for tat, the best of all 32 deterministic memory-one strategies at each discount
    factor delta, and the smallest delta at which cooperating for ever is a best response. With (T, R, P, S) =
    (5, 3, 1, 0): (T - R)/(T - P) = 1/2 against grim, and max of that and (T - R)/(R - S) = 2/3 against tit for tat,
    where the best deviation alternates D, C, D, C."""
    T, R, P, S = PD["T"], PD["R"], PD["P"], PD["S"]
    if deltas is None:
        deltas = np.round(np.arange(0.0, 0.951, 0.01), 2)
    strategies = list(_memory_one_strategies())
    out = {"deltas": [float(d) for d in deltas]}
    for opp in ("grim", "tft"):
        best, arg = [], []
        for d in deltas:
            vals = [(_play_value(f, r, opp, float(d)), name) for name, f, r in strategies]
            v, name = max(vals, key=lambda x: (round(x[0], 9), x[1] == "CCCCC"))
            best.append(round(v, 6))
            arg.append(name)
        coop_best = [abs(b - R) < 1e-6 for b in best]
        # first delta from which cooperation stays a best response
        k = next(i for i in range(len(deltas)) if all(coop_best[i:]))
        out[opp] = {"best": best, "argbest": arg, "threshold_grid": float(deltas[k])}
    out["grim"]["threshold"] = (T - R) / (T - P)
    out["tft"]["threshold"] = max((T - R) / (T - P), (T - R) / (R - S))
    out["curves"] = {"cooperate": [float(R)] * len(deltas),
                     "always_defect": [round((1 - d) * T + d * P, 6) for d in deltas],
                     "alternate": [round((T + d * S) / (1 + d), 6) for d in deltas]}
    return out


def _canonical_rotation(seq):
    return min(tuple(seq[i:] + seq[:i]) for i in range(len(seq)))


def folk_theorem(max_len: int = 7, grid: int = 999) -> dict:
    """The folk theorem on the prisoner's dilemma (Friedman 1971; Fudenberg and Maskin 1986). A plan is a cycle of
    outcomes, repeated for ever; any deviation is punished by mutual defection for ever (Nash reversion, itself an
    equilibrium). For each cyclic plan of length at most max_len, find the smallest discount factor from which no
    player at any point of the cycle gains by deviating; then, for each average payoff pair, the most patient-friendly
    plan that reaches it. Feasible and strictly individually rational points all appear; the needed patience rises
    toward 1 near the minmax boundary."""
    pay = {o: _pd_pay(*o) for o in _OUT}
    ds = np.linspace(0.001, 0.999, grid)
    best: dict = {}
    seen = set()
    for L in range(1, max_len + 1):
        for comp in itertools.product(range(L + 1), repeat=4):
            if sum(comp) != L:
                continue
            avg = tuple(round(sum(c * pay[o][i] for c, o in zip(comp, _OUT)) / L, 6) for i in range(2))
            if not (avg[0] > 1 + 1e-9 and avg[1] > 1 + 1e-9):
                continue
            items = [o for c, o in zip(comp, _OUT) for _ in range(c)]
            for perm in set(itertools.permutations(items)):
                key = _canonical_rotation(list(perm))
                if key in seen:
                    continue
                seen.add(key)
                u = np.array([[pay[o][i] for o in key] for i in range(2)], dtype=float)   # 2 x L
                # V_i(k) = (1 - d) sum_j d^j u_i(k + j) / (1 - d^L)
                powers = ds[:, None] ** np.arange(L)[None, :]                             # G x L
                ok = np.ones(len(ds), dtype=bool)
                for i in range(2):
                    for k in range(L):
                        seq = np.roll(u[i], -k)
                        V = (1 - ds) * (powers @ seq) / (1 - ds ** L)
                        a = list(key[k])
                        a[i] = "D" if a[i] == "C" else "C"
                        dev = pay[tuple(a)][i]
                        ok &= V >= (1 - ds) * dev + ds * PD["P"] - 1e-12
                if not ok[-1]:
                    continue
                bad = np.where(~ok)[0]
                need = float(ds[bad[-1] + 1]) if len(bad) else float(ds[0])
                if avg not in best or need < best[avg]["delta"]:
                    best[avg] = {"delta": round(need, 3), "plan": ["".join(o) for o in key]}
    pts = sorted(({"u": list(k), **v} for k, v in best.items()), key=lambda r: (r["u"][0], r["u"][1]))
    return {"points": pts, "n_points": len(pts), "max_len": max_len,
            "ir_polygon": [[1, 1], [1, 13 / 3], [3, 3], [13 / 3, 1]],
            "feasible_polygon": [[1, 1], [0, 5], [3, 3], [5, 0]]}


def _zoo(rng):
    def allc(my, th):
        return "C"

    def alld(my, th):
        return "D"

    def tft(my, th):
        return th[-1] if th else "C"

    def gtft(my, th):
        if not th or th[-1] == "C":
            return "C"
        return "C" if rng.random() < 1 / 3 else "D"

    def grim(my, th):
        return "D" if "D" in th else "C"

    def wsls(my, th):
        if not my:
            return "C"
        return my[-1] if _pd_pay(my[-1], th[-1])[0] >= 3 else ("D" if my[-1] == "C" else "C")

    def tf2t(my, th):
        return "D" if th[-2:] == ["D", "D"] else "C"

    def joss(my, th):
        m = tft(my, th)
        return "D" if (m == "C" and rng.random() < 0.1) else m

    def rand(my, th):
        return "C" if rng.random() < 0.5 else "D"
    return {"tit for tat": tft, "generous tit for tat": gtft, "win-stay lose-shift": wsls, "grim": grim,
            "tit for two tats": tf2t, "Joss": joss, "random": rand, "always cooperate": allc, "always defect": alld}


def tournament(noises=(0.0, 0.05), rounds: int = 200, reps: int = 20, seed: int = 1980) -> dict:
    """Axelrod's round robin (each pair, and each strategy against its twin) with implementation noise: each intended
    move is flipped with probability `noise`. Mean payoff per round, averaged over `reps` repetitions with a fixed
    seed."""
    out = {}
    for noise in noises:
        rng = np.random.default_rng(seed)
        zoo = _zoo(rng)
        names = list(zoo)
        score = {n: 0.0 for n in names}
        count = {n: 0 for n in names}
        matrix = {a: {b: 0.0 for b in names} for a in names}
        for _ in range(reps):
            for i, a in enumerate(names):
                for b in names[i:]:
                    ha, hb, sa, sb = [], [], 0, 0
                    for _r in range(rounds):
                        ma, mb = zoo[a](ha, hb), zoo[b](hb, ha)
                        if rng.random() < noise:
                            ma = "D" if ma == "C" else "C"
                        if rng.random() < noise:
                            mb = "D" if mb == "C" else "C"
                        pa, pb = _pd_pay(ma, mb)
                        sa += pa
                        sb += pb
                        ha.append(ma)
                        hb.append(mb)
                    matrix[a][b] += sa / rounds / reps
                    if b != a:
                        matrix[b][a] += sb / rounds / reps
        for a in names:
            score[a] = sum(matrix[a].values()) / len(names)
        order = sorted(names, key=lambda n: -score[n])
        out[str(noise)] = {"ranking": [[n, round(score[n], 3)] for n in order],
                           "matrix": {a: {b: round(v, 3) for b, v in row.items()} for a, row in matrix.items()}}
    return {"rounds": rounds, "reps": reps, "by_noise": out}


def ecological(matrix: dict, generations: int = 60) -> dict:
    """Axelrod's ecological simulation: each strategy's share next generation is proportional to its share times its
    average score against the current population."""
    names = list(matrix)
    M = np.array([[matrix[a][b] for b in names] for a in names])
    x = np.ones(len(names)) / len(names)
    hist = [x.round(4).tolist()]
    for _ in range(generations):
        f = M @ x
        x = x * f / (x @ f)
        hist.append(x.round(4).tolist())
    return {"names": names, "shares": hist}


# ---------------------------------------------------------------------------
# Memory-one strategies and zero-determinant strategies
# ---------------------------------------------------------------------------
def stationary(p, q, eps: float = 1e-9) -> np.ndarray:
    """Stationary distribution over (CC, CD, DC, DD), from X's view, when X plays memory-one p and Y plays q (both
    conditioned on the previous outcome from their own view). A tiny error keeps the chain ergodic."""
    p = np.clip(np.asarray(p, float), eps, 1 - eps)
    q = np.clip(np.asarray(q, float), eps, 1 - eps)
    qy = q[[0, 2, 1, 3]]                 # Y sees CD as DC
    M = np.zeros((4, 4))
    for s in range(4):
        px, py = p[s], qy[s]
        M[s] = [px * py, px * (1 - py), (1 - px) * py, (1 - px) * (1 - py)]
    w, v = np.linalg.eig(M.T)
    k = np.argmin(abs(w - 1))
    pi = np.real(v[:, k])
    return pi / pi.sum()


def payoffs_memory_one(p, q) -> tuple[float, float]:
    pi = stationary(p, q)
    T, R, P, S = PD["T"], PD["R"], PD["P"], PD["S"]
    return float(pi @ [R, S, T, P]), float(pi @ [R, T, S, P])


def zero_determinant(n_opponents: int = 2000, seed: int = 2012) -> dict:
    """Press and Dyson (2012). With (T, R, P, S) = (5, 3, 1, 0), the extortionate strategy p = (11/13, 1/2, 7/26, 0)
    enforces s_X - P = 3 (s_Y - P) against every opponent, whatever it does; the equalizer (2/3, 0, 2/3, 1/3) fixes
    the opponent's score at 2. Checked against random memory-one opponents. Head to head the extortioner never loses;
    against itself it gets only P."""
    rng = np.random.default_rng(seed)
    ext = [11 / 13, 1 / 2, 7 / 26, 0.0]
    eq = [2 / 3, 0.0, 2 / 3, 1 / 3]
    ratios, eqs = [], []
    for _ in range(n_opponents):
        q = rng.random(4)
        sx, sy = payoffs_memory_one(ext, q)
        if abs(sy - 1) > 1e-3:
            ratios.append((sx - 1) / (sy - 1))
        eqs.append(payoffs_memory_one(eq, q)[1])
    named = {"tit for tat": [1, 0, 1, 0], "win-stay lose-shift": [1, 0, 0, 1], "always cooperate": [1, 1, 1, 1],
             "always defect": [0, 0, 0, 0], "generous tit for tat": [1, 1 / 3, 1, 1 / 3]}
    head = {}
    for nm, q in named.items():
        sx, sy = payoffs_memory_one(ext, q)
        head[nm] = [round(sx, 4), round(sy, 4)]
    self_x = payoffs_memory_one(ext, ext)[0]
    return {"extortioner": [round(v, 4) for v in ext], "equalizer": [round(v, 4) for v in eq],
            "ratio_min": round(min(ratios), 6), "ratio_max": round(max(ratios), 6),
            "equalized_min": round(min(eqs), 6), "equalized_max": round(max(eqs), 6), "head_to_head": head,
            "against_itself": round(self_x, 4), "opponents": n_opponents}


def evolution_rare_mutation(N: int = 50, w: float = 1.0, noise: float = 0.01, steps: int = 3000,
                            seed: int = 2005) -> dict:
    """Imhof, Fudenberg and Nowak (2005): a finite population of N, a Moran process with selection intensity w, and rare
    mutations, so the population is almost always monomorphic and moves between strategies by fixations. Strategies:
    always defect, always cooperate, tit for tat, win-stay lose-shift, generous tit for tat, the extortioner, with
    implementation noise. The embedded chain's stationary distribution says where the population spends its time; a
    sampled path shows cooperation rise and collapse."""
    strat = {"always defect": [0, 0, 0, 0], "always cooperate": [1, 1, 1, 1], "tit for tat": [1, 0, 1, 0],
             "win-stay lose-shift": [1, 0, 0, 1], "generous tit for tat": [1, 1 / 3, 1, 1 / 3],
             "extortioner": [11 / 13, 1 / 2, 7 / 26, 0.0]}
    names = list(strat)
    k = len(names)

    def noisy(p):
        return [(1 - noise) * v + noise * (1 - v) for v in p]
    pay = np.zeros((k, k))
    coop = np.zeros((k, k))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            pi = stationary(noisy(strat[a]), noisy(strat[b]))
            pay[i, j] = pi @ [3, 0, 5, 1]
            coop[i, j] = pi[0] + pi[1]

    def fix(i, j):
        # probability that one j-mutant takes over a population of i
        ratios = []
        for m in range(1, N):
            fj = (pay[j, j] * (m - 1) + pay[j, i] * (N - m)) / (N - 1)
            fi = (pay[i, j] * m + pay[i, i] * (N - m - 1)) / (N - 1)
            ratios.append(math.exp(-w * (fj - fi)))
        s, prod = 1.0, 1.0
        for r in ratios:
            prod *= r
            s += prod
        return 1 / s
    T = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i != j:
                T[i, j] = fix(i, j) / (k - 1)
        T[i, i] = 1 - T[i].sum()
    wv, v = np.linalg.eig(T.T)
    st = np.real(v[:, np.argmin(abs(wv - 1))])
    st = st / st.sum()
    rng = np.random.default_rng(seed)
    path, cur = [], 0
    for _ in range(steps):
        path.append(cur)
        cur = int(rng.choice(k, p=T[cur]))
    runs = []
    for x in path:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    return {"names": names, "N": N, "w": w, "noise": noise, "stationary": [round(float(x), 4) for x in st],
            "coop_self": [round(float(coop[i, i]), 4) for i in range(k)],
            "avg_cooperation": round(float(sum(st[i] * coop[i, i] for i in range(k))), 4),
            "runs": runs, "steps": steps,
            "fixation_from_alld": {names[j]: round(fix(0, j), 6) for j in range(1, k)}}


# ---------------------------------------------------------------------------
# Skyrms: the Nash demand game
# ---------------------------------------------------------------------------
def nash_demand(grid: int = 60, steps: int = 4000, dt: float = 0.05, assort: float = 0.0) -> dict:
    """Divide the cake: each of two players demands 1/3, 1/2 or 2/3, and gets it if the demands are compatible (sum at
    most 1), nothing otherwise. Under the replicator dynamics a population converges either to everyone demanding a
    half, or to a polymorphism of 1/3 and 2/3 demanders (Skyrms 1996): fair division has the larger basin, but not the
    whole simplex. Every interior grid point of the simplex is run to its end."""
    d = [1 / 3, 1 / 2, 2 / 3]
    A = np.array([[a if a + b <= 1 + 1e-9 else 0 for b in d] for a in d])
    starts = np.array([[i, j, grid - i - j] for i in range(1, grid) for j in range(1, grid - i)], float) / grid
    X = starts.copy()
    for _ in range(steps):
        # with assortment e, a demander meets its own type with probability e (Skyrms's correlated encounters)
        F = (1 - assort) * (X @ A.T) + assort * np.diag(A)[None, :]
        avg = (X * F).sum(axis=1, keepdims=True)
        X = np.clip(X + dt * X * (F - avg), 0, None)
        X /= X.sum(axis=1, keepdims=True)
    ends = np.where(X[:, 1] > 0.99, "fair", np.where(X[:, 1] < 0.01, "polymorphic", "other"))
    fair, poly, other = int((ends == "fair").sum()), int((ends == "polymorphic").sum()), int((ends == "other").sum())
    pts = [[round(float(a), 4), round(float(b), 4), str(e)] for (a, b, _c), e in zip(starts, ends)]
    total = fair + poly + other
    return {"demands": ["1/3", "1/2", "2/3"], "payoff": A.round(4).tolist(), "fair": fair, "polymorphic": poly,
            "other": other, "fair_share": round(fair / total, 4), "points": pts, "grid": grid, "assort": assort}


def nash_demand_assort(es=(0.0, 0.1, 0.2, 0.3)) -> dict:
    return {"rows": [{"assort": e, "fair_share": nash_demand(grid=40, assort=e)["fair_share"]} for e in es]}


# ---------------------------------------------------------------------------
# Bargaining
# ---------------------------------------------------------------------------
def bargaining(deltas=(0.5, 0.8, 0.9, 0.95, 0.99)) -> dict:
    """Split a dollar; player 1's utility is her share x, player 2 is risk averse with utility sqrt(1 - x). Nash (1950):
    maximize the product of gains, x sqrt(1 - x): x = 2/3. Kalai and Smorodinsky (1975): equal shares of the ideal
    gains, x = sqrt(1 - x): x = 0.618. Rubinstein (1982), alternating offers with a common discount delta (linear
    utilities): the first mover gets 1/(1 + delta), which tends to the Nash split 1/2 as delta tends to 1."""
    xs = np.linspace(0, 1, 100001)
    nash_x = float(xs[np.argmax(xs * np.sqrt(1 - xs))])
    ks_x = (math.sqrt(5) - 1) / 2
    frontier = [[round(float(x), 4), round(float(math.sqrt(1 - x)), 4)] for x in np.linspace(0, 1, 51)]
    rub = [{"delta": dlt, "first": round(1 / (1 + dlt), 4)} for dlt in deltas]
    return {"nash_x": round(nash_x, 4), "nash_u2": round(math.sqrt(1 - nash_x), 4), "ks_x": round(ks_x, 4),
            "ks_u2": round(math.sqrt(1 - ks_x), 4), "frontier": frontier, "rubinstein": rub}


# ---------------------------------------------------------------------------
# The Shapley value
# ---------------------------------------------------------------------------
def shapley(players, v) -> dict:
    """Average marginal contribution over all orders of arrival."""
    phi = {p: 0.0 for p in players}
    orders = list(itertools.permutations(players))
    for order in orders:
        s = frozenset()
        for p in order:
            phi[p] += v(s | {p}) - v(s)
            s = s | {p}
    return {p: phi[p] / len(orders) for p in players}


def shapley_examples() -> dict:
    """The glove game (one left glove, two right; a pair is worth 1): Shapley (2/3, 1/6, 1/6), while the core gives the
    scarce left glove everything. Harsanyi dividends of a three-player game, whose equal split recovers the Shapley
    value (the uniqueness proof's basis of unanimity games). SHAP (Lundberg and Lee 2017) on the model
    f = x1 + 2 x2 x3 at x = (1, 1, 1) with baseline 0."""
    def glove(s):
        return float(min(len(s & {"L"}), len(s & {"R1", "R2"})))
    g = shapley(["L", "R1", "R2"], glove)
    # core of the glove game: the only allocation with no blocking coalition gives L everything
    core = []
    for a in np.linspace(0, 1, 101):
        for b in np.linspace(0, 1 - a, int(round((1 - a) * 100)) + 1):
            c = 1 - a - b
            alloc = {"L": a, "R1": b, "R2": c}
            ok = all(sum(alloc[p] for p in S) >= glove(frozenset(S)) - 1e-9
                     for r in range(1, 4) for S in itertools.combinations(["L", "R1", "R2"], r))
            if ok:
                core.append([round(a, 3), round(b, 3), round(c, 3)])

    def model(x):
        return x[0] + 2 * x[1] * x[2]
    x, base = (1.0, 1.0, 1.0), (0.0, 0.0, 0.0)

    def v_model(s):
        z = [x[i] if f"x{i + 1}" in s else base[i] for i in range(3)]
        return model(z)
    shap = shapley(["x1", "x2", "x3"], v_model)
    # dividends of v_model: d(S) = sum over T subset S of (-1)^{|S|-|T|} v(T)
    players = ["x1", "x2", "x3"]
    div = {}
    for r in range(1, 4):
        for S in itertools.combinations(players, r):
            div["".join(p[1] for p in S)] = sum((-1) ** (len(S) - len(T)) * v_model(frozenset(T))
                                                for k in range(len(S) + 1) for T in itertools.combinations(S, k))
    return {"glove": {k: round(v, 4) for k, v in g.items()}, "glove_core": core,
            "shap": {k: round(v, 4) for k, v in shap.items()}, "model_value": model(x),
            "dividends": {k: round(v, 4) for k, v in div.items() if abs(v) > 1e-12}}


# ---------------------------------------------------------------------------
# Auctions
# ---------------------------------------------------------------------------
def auctions(n_sims: int = 400000, seed: int = 1961) -> dict:
    """Two bidders with values uniform on [0, 1]. Second price (Vickrey 1961): for a bidder with value 0.6, expected
    utility as a function of her bid peaks at the truth. First price: the equilibrium bid is v/2. Both raise expected
    revenue 1/3 (revenue equivalence). Myerson (1981): a reserve price of 1/2 raises it to 5/12."""
    rng = np.random.default_rng(seed)
    v = rng.random((n_sims, 2))
    other = rng.random(n_sims)
    bids = np.linspace(0, 1, 41)
    v0 = 0.6
    u2 = [round(float(np.mean(np.where(b > other, v0 - other, 0.0))), 4) for b in bids]
    u1 = [round(float(np.mean(np.where(b > other / 2, v0 - b, 0.0))), 4) for b in bids]
    second = float(np.mean(v.min(axis=1)))
    first = float(np.mean(v.max(axis=1) / 2))
    hi, lo = v.max(axis=1), v.min(axis=1)
    reserve = 0.5
    rev_res = np.where(hi < reserve, 0.0, np.maximum(lo, reserve))
    return {"bids": [round(float(b), 3) for b in bids], "value": v0, "u_second": u2, "u_first": u1,
            "best_bid_second": float(bids[int(np.argmax(u2))]), "best_bid_first": float(bids[int(np.argmax(u1))]),
            "revenue_second": round(second, 4), "revenue_first": round(first, 4),
            "revenue_reserve": round(float(np.mean(rev_res)), 4), "theory": [round(1 / 3, 4), round(5 / 12, 4)]}


def gsp_vcg(values=(10.0, 8.0, 5.0, 2.0), ctr=(0.3, 0.2, 0.1)) -> dict:
    """Sponsored-search slots with click rates ctr, bidders with values per click. VCG charges each winner the
    externality it imposes. The generalized second price auction charges each winner the next bid per click; bidding
    truthfully in GSP is not an equilibrium. Edelman, Ostrovsky and Schwarz (2007): its locally envy-free equilibrium
    raises exactly the VCG revenue."""
    v = list(values)
    k = len(ctr)
    vcg = []
    for i in range(k):
        # externality of the winner of slot i on those below
        pay = sum((ctr[j - 1] - ctr[j] if j < k else ctr[j - 1]) * v[j] for j in range(i + 1, k + 1))
        vcg.append(round(pay, 4))
    gsp_truthful = [round(ctr[i] * v[i + 1], 4) for i in range(k)]
    # does the top bidder gain by shading to win slot 2 under truthful GSP by others?
    top_slot1 = ctr[0] * (v[0] - v[1])
    top_slot2 = ctr[1] * (v[0] - v[2])
    # EOS equilibrium bids: b_{i} for slot i-1 ... revenue equals VCG
    return {"values": v, "ctr": list(ctr), "vcg_payments": vcg, "vcg_revenue": round(sum(vcg), 4),
            "gsp_truthful_payments": gsp_truthful, "gsp_truthful_revenue": round(sum(gsp_truthful), 4),
            "top_utility_slot1": round(top_slot1, 4), "top_utility_slot2": round(top_slot2, 4)}


# ---------------------------------------------------------------------------
# Deferred acceptance
# ---------------------------------------------------------------------------
def deferred_acceptance(prop_prefs: dict, recv_prefs: dict) -> tuple[dict, list]:
    free = list(prop_prefs)
    nxt = {p: 0 for p in prop_prefs}
    held = {}
    log = []
    rank = {r: {p: i for i, p in enumerate(pr)} for r, pr in recv_prefs.items()}
    while free:
        p = free.pop(0)
        if nxt[p] >= len(prop_prefs[p]):
            continue
        r = prop_prefs[p][nxt[p]]
        nxt[p] += 1
        cur = held.get(r)
        if cur is None:
            held[r] = p
            log.append([p, r, "held"])
        elif rank[r][p] < rank[r][cur]:
            held[r] = p
            free.append(cur)
            log.append([p, r, f"held, {cur} rejected"])
        else:
            free.append(p)
            log.append([p, r, "rejected"])
    return {p: r for r, p in held.items()}, log


def blocking_pairs(match: dict, prop_prefs: dict, recv_prefs: dict) -> list:
    inv = {r: p for p, r in match.items()}
    out = []
    for p, prefs in prop_prefs.items():
        for r in prefs:
            if r == match.get(p):
                break
            cur = inv.get(r)
            if cur is None or recv_prefs[r].index(p) < recv_prefs[r].index(cur):
                out.append([p, r])
    return out


def gale_shapley(n: int = 5, seed: int = 2083) -> dict:
    """Gale and Shapley (1962): students propose to schools in order of preference; each school holds its best offer so
    far and rejects the rest. The result is stable (no student and school both prefer each other to their match),
    proposer-optimal (every student does at least as well as in any stable matching), and no student can gain by
    misreporting (checked over all 120 orderings for each student). A school can sometimes gain by misreporting."""
    rng = np.random.default_rng(seed)
    P = [f"s{i + 1}" for i in range(n)]
    R = [chr(ord("A") + i) for i in range(n)]
    pp = {p: [str(x) for x in rng.permutation(R)] for p in P}
    rp = {r: [str(x) for x in rng.permutation(P)] for r in R}
    match, log = deferred_acceptance(pp, rp)
    stable = blocking_pairs(match, pp, rp) == []
    # all stable matchings by brute force
    stables = []
    for perm in itertools.permutations(R):
        m = dict(zip(P, perm))
        if not blocking_pairs(m, pp, rp):
            stables.append(m)
    proposer_optimal = all(all(pp[p].index(match[p]) <= pp[p].index(m[p]) for p in P) for m in stables)
    gains = 0
    for p in P:
        for lie in itertools.permutations(R):
            alt = dict(pp)
            alt[p] = list(lie)
            m2, _ = deferred_acceptance(alt, rp)
            gains += pp[p].index(m2[p]) < pp[p].index(match[p])
    # can some school gain by truncating or reordering? search all orderings for each school
    school_gain = None
    for r in R:
        for lie in itertools.permutations(P):
            alt = dict(rp)
            alt[r] = list(lie)
            m2, _ = deferred_acceptance(pp, alt)
            inv2 = {s: p for p, s in m2.items()}
            inv = {s: p for p, s in match.items()}
            if rp[r].index(inv2[r]) < rp[r].index(inv[r]):
                school_gain = {"school": r, "truth": inv[r], "lie_gets": inv2[r]}
                break
        if school_gain:
            break
    school_side, _ = deferred_acceptance(rp, pp)          # schools propose: the school-optimal stable matching
    school_opt = {p: r for r, p in school_side.items()}
    return {"students": pp, "schools": rp, "match": match, "log": log, "stable": stable,
            "n_stable": len(stables), "proposer_optimal": proposer_optimal, "student_gains_by_lying": gains,
            "school_gain": school_gain, "school_optimal": school_opt,
            "student_ranks": {p: [pp[p].index(match[p]) + 1, pp[p].index(school_opt[p]) + 1] for p in P}}
