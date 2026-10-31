"""Local search for Part 2: hill climbing on n queens, and three ways to attack a travelling-salesman tour.

* Steepest-ascent hill climbing on the 8-queens problem (one queen per column; a move shifts one queen within its
  column), with and without sideways moves, as in Russell & Norvig.
* berlin52, a TSPLIB instance (52 places in Berlin, after Groetschel; optimum 7,542, TSPLIB's solutions list):
  nearest-neighbour tours, 2-opt hill climbing from random tours, simulated annealing with 2-opt moves and the
  Metropolis rule (Kirkpatrick, Gelatt & Vecchi 1983), and a genetic algorithm with order crossover (Holland 1975;
  Davis 1985), all limited by actual candidate-cost evaluations (not equal CPU time).
"""

from __future__ import annotations

import numpy as np
from numba import njit

# ---------------------------------------------------------------------------
# n queens
# ---------------------------------------------------------------------------


@njit(cache=True)
def attacks(q):
    n = q.shape[0]
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            if q[i] == q[j] or abs(q[i] - q[j]) == j - i:
                h += 1
    return h


@njit(cache=True)
def climb_queens(q, max_sideways, seed, trace, boards):
    """Steepest descent on the number of attacking pairs. Returns (solved, steps, final h); ``trace`` gets h per
    step and ``boards`` the board after each step (as far as their lengths allow)."""
    np.random.seed(seed)
    n = q.shape[0]
    h = attacks(q)
    steps = 0
    side = 0
    if trace.shape[0] > 0:
        trace[0] = h
    if boards.shape[0] > 0:
        boards[0] = q
    while True:
        if h == 0:
            return True, steps, 0
        best = h + 1
        cand_c = np.empty(n * n, np.int64)
        cand_r = np.empty(n * n, np.int64)
        nc = 0
        for c in range(n):
            old = q[c]
            for r in range(n):
                if r == old:
                    continue
                q[c] = r
                v = attacks(q)
                if v < best:
                    best = v
                    nc = 0
                if v == best:
                    cand_c[nc] = c
                    cand_r[nc] = r
                    nc += 1
            q[c] = old
        if best > h or (best == h and side >= max_sideways):
            return False, steps, h
        if best == h:
            side += 1
        else:
            side = 0
        k = np.random.randint(nc)
        q[cand_c[k]] = cand_r[k]
        h = best
        steps += 1
        if steps < trace.shape[0]:
            trace[steps] = h
        if steps < boards.shape[0]:
            boards[steps] = q


# ---------------------------------------------------------------------------
# berlin52
# ---------------------------------------------------------------------------
BERLIN52 = np.array([
    (565, 575), (25, 185), (345, 750), (945, 685), (845, 655), (880, 660), (25, 230), (525, 1000), (580, 1175),
    (650, 1130), (1605, 620), (1220, 580), (1465, 200), (1530, 5), (845, 680), (725, 370), (145, 665), (415, 635),
    (510, 875), (560, 365), (300, 465), (520, 585), (480, 415), (835, 625), (975, 580), (1215, 245), (1320, 315),
    (1250, 400), (660, 180), (410, 250), (420, 555), (575, 665), (1150, 1160), (700, 580), (685, 595), (685, 610),
    (770, 610), (795, 645), (720, 635), (760, 650), (475, 960), (95, 260), (875, 920), (700, 500), (555, 815),
    (830, 485), (1170, 65), (830, 610), (605, 625), (595, 360), (1340, 725), (1740, 245)], float)
BERLIN52_OPT = 7542


def dist_matrix(P: np.ndarray) -> np.ndarray:
    """TSPLIB EUC_2D: Euclidean distance rounded to the nearest integer."""
    d = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1))
    return np.floor(d + 0.5).astype(np.int64)


@njit(cache=True)
def tour_len(t, D):
    s = 0
    n = t.shape[0]
    for i in range(n):
        s += D[t[i], t[(i + 1) % n]]
    return s


@njit(cache=True)
def nearest_neighbour(D, start):
    n = D.shape[0]
    used = np.zeros(n, np.bool_)
    t = np.empty(n, np.int64)
    t[0] = start
    used[start] = True
    for i in range(1, n):
        best, bj = 1 << 60, -1
        for j in range(n):
            if not used[j] and D[t[i - 1], j] < best:
                best, bj = D[t[i - 1], j], j
        t[i] = bj
        used[bj] = True
    return t


@njit(cache=True)
def two_opt_climb(t, D, budget):
    """Best-improvement 2-opt, capped at ``budget`` actual cost evaluations.

    The initial tour costs one evaluation; each valid neighbour delta costs one.
    Apply the best evaluated improvement even if the budget ends mid-sweep.
    Returns (length, evaluations), and mutates ``t`` to the best tour found.
    """
    if budget < 1:
        raise ValueError("a tour budget must include at least one initial evaluation")
    n = t.shape[0]
    looked = 1
    L = tour_len(t, D)
    while looked < budget:
        best, bi, bj = 0, -1, -1
        for i in range(n - 1):
            a, b = t[i], t[i + 1]
            for j in range(i + 2, n if i > 0 else n - 1):
                if looked >= budget:
                    break
                c, d = t[j], t[(j + 1) % n]
                delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
                looked += 1
                if delta < best:
                    best, bi, bj = delta, i, j
            if looked >= budget:
                break
        if bi < 0:
            break
        t[bi + 1: bj + 1] = t[bi + 1: bj + 1][::-1].copy()
        L += best
    return L, looked


@njit(cache=True)
def anneal(t, D, T0, alpha, moves_per_T, n_temps, seed, snap_every, snaps, trace,
           budget=-1, evaluations=None):
    """Anneal with valid 2-opt cost evaluations, not no-op random draws.

    Initialization counts once. ``budget`` optionally caps total evaluations;
    the default permits ``moves_per_T * n_temps`` evaluated moves. Trace rows
    after exhaustion repeat the final state. Optional ``evaluations[0]`` records
    the actual count. This currency is not a wall-clock comparison with a GA.
    """
    if moves_per_T < 0 or n_temps < 0 or T0 <= 0:
        raise ValueError("invalid annealing schedule")
    if budget == -1:
        budget = 1 + moves_per_T * n_temps
    if budget < 1:
        raise ValueError("a tour budget must include at least one initial evaluation")
    np.random.seed(seed)
    n = t.shape[0]
    L = tour_len(t, D)
    looked = 1
    bestL = L
    best = t.copy()
    T = T0
    k = 0
    for it in range(n_temps):
        acc, done = 0, 0
        while done < moves_per_T and looked < budget and n >= 4:
            i = np.random.randint(n)
            j = np.random.randint(n)
            if i > j:
                i, j = j, i
            if j - i < 2 or (i == 0 and j == n - 1):
                continue
            a, b, c, d = t[i], t[i + 1], t[j], t[(j + 1) % n]
            delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
            done += 1
            looked += 1
            if delta <= 0 or np.random.random() < np.exp(-delta / T):
                t[i + 1: j + 1] = t[i + 1: j + 1][::-1].copy()
                L += delta
                acc += 1
                if L < bestL:
                    bestL = L
                    best[:] = t
        trace[it, 0] = T
        trace[it, 1] = L
        trace[it, 2] = bestL
        trace[it, 3] = acc / done if done else 0.0
        if snap_every > 0 and it % snap_every == 0 and k < snaps.shape[0]:
            snaps[k] = t
            k += 1
        T *= alpha
    if evaluations is not None:
        evaluations[0] = looked
    return bestL, best


@njit(cache=True)
def _ox(p1, p2, i, j):
    """Order crossover: p1's slice [i, j) kept in place, the rest filled in p2's order."""
    n = p1.shape[0]
    child = np.full(n, -1, np.int64)
    used = np.zeros(n, np.bool_)
    for k in range(i, j):
        child[k] = p1[k]
        used[p1[k]] = True
    pos = j % n
    for k in range(n):
        c = p2[(j + k) % n]
        if not used[c]:
            child[pos] = c
            used[c] = True
            pos = (pos + 1) % n
    return child


@njit(cache=True)
def genetic(D, pop_size, gens, p_mut, seed, best_per_gen, snaps, snap_gens,
            budget=-1, evaluations=None):
    """A plain genetic algorithm: tournament selection (size 3), order crossover, a 2-opt reversal as mutation,
    and the best tour always kept (elitism). Initialization is charged; copied
    elites reuse their stored score. A partial final generation keeps its best
    evaluated child. ``best_per_gen[0]`` is initialization; later entries include
    each generation's result, including the last one. Returns the best length."""
    if pop_size < 1 or gens < 0:
        raise ValueError("invalid population or generation count")
    if budget == -1:
        budget = pop_size + gens * max(pop_size - 1, 0)
    if budget < 1:
        raise ValueError("a tour budget must include initialization")
    pop_size = min(pop_size, budget)
    np.random.seed(seed)
    n = D.shape[0]
    pop = np.empty((pop_size, n), np.int64)
    fit = np.empty(pop_size, np.int64)
    for k in range(pop_size):
        pop[k] = np.random.permutation(n)
        fit[k] = tour_len(pop[k], D)
    looked = pop_size
    si = 0
    for g in range(gens + 1):
        e = np.argmin(fit)
        if g < best_per_gen.shape[0]:
            best_per_gen[g] = fit[e]
        if si < snap_gens.shape[0] and g == snap_gens[si]:
            snaps[si] = pop[e]
            si += 1
        if g == gens:
            break
        new = pop.copy()
        new_fit = fit.copy()
        new[0] = pop[e]
        new_fit[0] = fit[e]
        for k in range(1, pop_size):
            if looked >= budget:
                break
            par = np.empty((2, n), np.int64)
            for m in range(2):
                a = np.random.randint(pop_size)
                for _ in range(2):
                    b = np.random.randint(pop_size)
                    if fit[b] < fit[a]:
                        a = b
                par[m] = pop[a]
            i = np.random.randint(n)
            j = np.random.randint(n)
            if i > j:
                i, j = j, i
            child = _ox(par[0], par[1], i, j + 1)
            if np.random.random() < p_mut:
                i = np.random.randint(n)
                j = np.random.randint(n)
                if i > j:
                    i, j = j, i
                child[i:j + 1] = child[i:j + 1][::-1].copy()
            new[k] = child
            new_fit[k] = tour_len(child, D)
            looked += 1
        pop = new
        fit = new_fit
    if evaluations is not None:
        evaluations[0] = looked
    return fit.min()
