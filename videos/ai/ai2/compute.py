"""Precompute everything numerical in Part 2 of the AI series ("Thinking Machines: the symbolic era").

    nice -n 15 python -m videos.ai.ai2.compute             # everything missing (about half an hour on one core)
    nice -n 15 python -m videos.ai.ai2.compute --force sat3

Results are cached in ``.cache/ai2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every search, solver and
learner here runs on this machine, seeded. Numbers about historical systems (Deep Blue, MYCIN, ...) are the
published ones, cited on screen.

Items:
    tm         Turing machines: a binary incrementer step by step; the busy-beaver champions with 4 and 5 states
               run to their halts (107 and 47,176,870 steps), with space-time pictures
    puzzle8    the 8-puzzle: breadth-first search of all 181,440 states (how many at each distance); A* with no
               heuristic, misplaced tiles and Manhattan distance on 100 positions per solution length; one solution
    puzzle15   the 15-puzzle: IDA* with misplaced tiles, Manhattan distance and an additive 5-5-5 pattern database,
               on scrambled positions
    grid       Dijkstra, A*, weighted A* and greedy best-first on a grid with walls (the frontier, cell by cell);
               the circle and the ellipse that must contain what they expand; 200 random maps
    queens     steepest-ascent hill climbing on 8 queens, with and without sideways moves (10,000 starts)
    tsp        berlin52: nearest neighbour, 2-opt hill climbing, simulated annealing and a genetic algorithm, on equal
               budgets; one annealing run cooling, tour by tour
    ttt        tic-tac-toe's whole game tree: minimax against alpha-beta
    uniform    alpha-beta with perfect ordering on uniform trees against Knuth & Moore's count
    alphabeta  Connect Four, 1 to 9 moves deep: minimax, alpha-beta in random order, best-looking first, truly best
               first
    testset    Connect Four positions (14-28 stones) with every move scored by the perfect solver (Part 26's)
    samuel     a Samuel-style learner of a Connect Four evaluation, by self-play; its weights over training and its
               score against its programmer's hand-set weights
    resolution resolution refutations: a propositional one, a first-order one with unification, and the clause
               explosion of saturation against the set-of-support strategy
    sat3       random 3-SAT: the chance of being satisfiable and DPLL's work against the clause ratio, n = 25 ... 200
    cdcl       clause learning: one conflict analysed; DPLL against CDCL on adder equivalence; adders proved equal
               and a bug found; multiplier commutativity, where SAT solvers struggle
    sudoku     a Sudoku made here; AC-3 alone; backtracking plain, with forward checking, MRV, and MAC
    blocks     the blocks world: states counted; the Sussman anomaly; breadth-first against A* (h_max) and greedy
               search with the relaxed-plan heuristic (h_FF)
    rules      a small forward-chaining rule base (illustrative) and MYCIN's certainty-factor arithmetic
    eliza      our ELIZA on the conversation printed in Weizenbaum (1966), and on some new lines
    tail       the long tail of words in the thirty novels (Part 1's corpus) and in the scoreboard passage
"""

from __future__ import annotations

import json
import math
import re
import time
from collections import Counter

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai2")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


class Partial:
    """The finished pieces of a long compute item, saved as they come (``.cache/ai2/<name>.partial.json``), so a run
    that is killed resumes where it stopped. Pieces computed with other parameters are discarded; the file is
    removed when the item is saved."""

    def __init__(self, name: str, params):
        self.path = CACHE.dir / f"{name}.partial.json"
        self.params = json.loads(json.dumps(params, default=float))
        data = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.done = data.get("done", {}) if data.get("params") == self.params else {}
        if self.done:
            print(f"  resuming {name}: {len(self.done)} pieces done", flush=True)

    def __contains__(self, key: str) -> bool:
        return key in self.done

    def __getitem__(self, key: str):
        return self.done[key]

    def __setitem__(self, key: str, value) -> None:
        self.done[key] = json.loads(json.dumps(value, default=float))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"params": self.params, "done": self.done}, default=float))
        tmp.replace(self.path)

    def finish(self) -> None:
        self.path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Turing machines
# ---------------------------------------------------------------------------
def compute_tm():
    from videos.ai.ai2 import machines as T

    inc = T.run_small(T.INCREMENT, ["_", 1, 0, 1, 1, "_"], 4)
    inc2 = T.run_small(T.INCREMENT, ["_", 1, 1, 1, "_"], 3)
    # Brady's 4-state champion: the whole run, cell by cell
    W, M, N = T._encode(T.parse(T.BB4))
    tape, head, st = {}, 0, 0
    rows, heads, states = [], [], []
    for _ in range(200):
        rows.append(dict(tape))
        heads.append(head)
        states.append(st)
        if st < 0:
            break
        b = tape.get(head, 0)
        tape[head] = int(W[st, b])
        head += int(M[st, b])
        st = int(N[st, b])
    lo = min(min(heads), min(min(r) if r else 0 for r in rows))
    hi = max(max(heads), max(max(r) if r else 0 for r in rows))
    st4 = np.array([[r.get(c, 0) for c in range(lo, hi + 1)] for r in rows], np.int8)
    bb4 = T.run_big(T.BB4)
    assert bb4["steps"] == 107 and bb4["ones"] == 13
    # Marxen and Buntrock's 5-state champion: 300 snapshots of the tape, each squeezed to 400 columns
    t0 = time.time()
    n_snaps = 300
    bb5 = T.run_big(T.BB5, n_snaps=n_snaps, snap_every=47_176_870 // n_snaps + 1, size=26_000)
    secs = time.time() - t0
    assert bb5["steps"] == 47_176_870 and bb5["ones"] == 4098  # the published values
    c0 = 26_000 // 2 + bb5["lo"] - 50
    c1 = 26_000 // 2 + bb5["hi"] + 50
    snaps = bb5["snaps"][:, c0:c1].astype(float)
    cols = 400
    edges = np.linspace(0, snaps.shape[1], cols + 1).astype(int)
    img = np.stack([snaps[:, a:b].mean(1) for a, b in zip(edges[:-1], edges[1:])], 1)
    return {"inc_tape": [[str(x) for x in h["tape"]] for h in inc], "inc_head": [h["head"] for h in inc],
            "inc_state": [h["state"] for h in inc], "inc2_final": [str(x) for x in inc2[-1]["tape"]],
            "inc_rules": [[s, str(b), str(w), m, n] for (s, b), (w, m, n) in T.INCREMENT.items()],
            "bb4_table": T.BB4, "bb4_steps": bb4["steps"], "bb4_ones": bb4["ones"], "bb4_st": st4,
            "bb4_heads": np.array(heads) - lo, "bb4_states": np.array(states),
            "bb5_table": T.BB5, "bb5_steps": bb5["steps"], "bb5_ones": bb5["ones"], "bb5_span": bb5["hi"] - bb5["lo"] + 1,
            "bb5_img": img, "bb5_heads": (bb5["heads"] - (bb5["lo"] - 50)) / (c1 - c0), "bb5_seconds": secs}


# ---------------------------------------------------------------------------
# Sliding-tile puzzles
# ---------------------------------------------------------------------------
def compute_puzzle8(per_depth=100, depths=tuple(range(2, 26, 2))):
    from videos.ai.ai2 import search as S

    dist = S.bfs8(S.GOAL8)
    reach = dist >= 0
    layers = np.bincount(dist[reach]).astype(int)
    g = rng(8)
    rows = {k: [] for k in ("h0", "h1", "h2")}
    for d in depths:
        idx = np.flatnonzero(dist == d)
        pick = g.choice(idx, size=min(per_depth, len(idx)), replace=False)
        res = {k: [] for k in rows}
        for r in pick:
            p = S.unrank9(int(r))
            for k, kind in (("h0", 0), ("h1", 1), ("h2", 2)):
                n, L = S.astar8(p, kind)
                assert L == d  # A* with an admissible heuristic is optimal
                res[k].append(n)
        for k in rows:
            rows[k].append(float(np.mean(res[k])))
    ebf = {k: [S.effective_branching(N, d) for N, d in zip(rows[k], depths)] for k in rows}
    # one position at distance 20 and a shortest solution, by walking down the distance table
    idx = np.flatnonzero(dist == 20)
    r = int(g.choice(idx))
    path = [S.unrank9(r).tolist()]
    while dist[r] > 0:
        p = S.unrank9(r)
        b = int(np.flatnonzero(p == 0)[0])
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            r2, c2 = b // 3 + dr, b % 3 + dc
            if 0 <= r2 < 3 and 0 <= c2 < 3:
                q = p.copy()
                j = r2 * 3 + c2
                q[b], q[j] = q[j], q[b]
                rq = int(S.rank9(q))
                if dist[rq] == dist[r] - 1:
                    r = rq
                    path.append(q.tolist())
                    break
    hardest = [S.unrank9(int(i)).tolist() for i in np.flatnonzero(dist == dist.max())]
    return {"layers": layers, "n_states": int(reach.sum()), "max_depth": int(dist.max()), "hardest": hardest,
            "depths": list(depths), "per_depth": per_depth, **{f"astar_{k}": rows[k] for k in rows},
            **{f"ebf_{k}": ebf[k] for k in ebf}, "path": path}


def compute_puzzle15(n_inst=30, seed=15):
    from videos.ai.ai2 import search as S

    t0 = time.time()
    pdbs = np.stack([S.build_pdb(gr) for gr in S.GROUPS])
    pdb_secs = time.time() - t0
    gpos = S.goal_pos15()
    g = rng(seed)
    rows = []
    walks = np.linspace(30, 120, n_inst).astype(int)
    caps = {"pdb": 10**9, "manhattan": 5 * 10**7, "misplaced": 10**7}
    for w in walks:
        b = S.scramble15(g, int(w))
        row = {"walk": int(w), "board": b.tolist()}
        for name, kind in (("pdb", 2), ("manhattan", 1), ("misplaced", 0)):
            t = time.time()
            n, L = S.ida15(b, kind, gpos, pdbs, S.GROUPS, caps[name])
            row[name] = int(n)
            row[name + "_len"] = int(L)
            row[name + "_secs"] = time.time() - t
        assert row["manhattan_len"] in (-1, row["pdb_len"]) and row["misplaced_len"] in (-1, row["pdb_len"])
        rows.append(row)
    # the heuristics at the goal's neighbourhood and on average over random positions: how much each one knows
    h_mean = {}
    perms = [g.permutation(16) for _ in range(2000)]
    for name, kind in (("misplaced", 0), ("manhattan", 1), ("pdb", 2)):
        vals = []
        for p in perms:
            pos = np.empty(16, np.int64)
            for i in range(16):
                pos[p[i]] = i
            vals.append(S._h15(pos, kind, gpos, pdbs, S.GROUPS))
        h_mean[name] = float(np.mean(vals))
    return {"rows": rows, "caps": caps, "pdb_secs": pdb_secs, "pdb_entries": int(16 ** 5), "h_mean": h_mean,
            "pdb_max": [int(p[p < 255].max()) for p in pdbs]}


# ---------------------------------------------------------------------------
# Shortest paths on a grid
# ---------------------------------------------------------------------------
def showcase_grid(H=64, W=64):
    """A square map: start in the middle, goal to the right, a wall between them; a few walls elsewhere."""
    free = np.ones((H, W), bool)
    free[24:41, 43] = False  # the wall between start and goal
    free[20:31, 20] = False  # behind the start
    free[12, 25:36] = False
    free[48, 30:42] = False
    free[50:58, 52] = False
    return free, (32, 31), (32, 55)


def compute_grid(n_maps=200):
    from videos.ai.ai2 import search as S

    free, (sr, sc), (gr, gc) = showcase_grid()
    H, W = free.shape
    out = {"free": free.astype(np.int8), "start": [sr, sc], "goal": [gr, gc]}
    methods = {"dijkstra": (1.0, 0.0), "astar": (1.0, 1.0), "wastar": (1.0, 2.0), "greedy": (0.0, 1.0)}
    for name, (wg, wh) in methods.items():
        n, cost, order, parent, gval = S.grid_search(free, sr, sc, gr, gc, wg, wh, S.MOVES)
        out[f"{name}_order"] = order.astype(np.int32)
        out[f"{name}_n"] = int(n)
        out[f"{name}_cost"] = float(cost)
        out[f"{name}_path"] = S.path_cells(parent, W, sr, sc, gr, gc)
    C = out["dijkstra_cost"]
    assert abs(out["astar_cost"] - C) < 1e-9  # A* with a consistent heuristic is optimal
    rr, cc = np.mgrid[0:H, 0:W]
    ds = np.hypot(rr - sr, cc - sc)
    dg = np.hypot(rr - gr, cc - gc)
    for name, inside in (("dijkstra", ds <= C + 1e-9), ("astar", ds + dg <= C + 1e-9)):
        exp = out[f"{name}_order"] >= 0
        out[f"{name}_inside"] = float((exp & inside).sum() / exp.sum())
        out[f"{name}_region"] = int((inside & free).sum())
    out["straight"] = float(np.hypot(gr - sr, gc - sc))
    # 200 random maps, start and goal far apart
    g = rng(21)
    batch = {k: [] for k in ("dijkstra_n", "astar_n", "wastar_n", "greedy_n", "astar_cost", "wastar_cost",
                             "greedy_cost", "dijkstra_cost")}
    done = 0
    while done < n_maps:
        f = S.random_grid(g, 48, 80)
        s = (int(g.integers(2, 46)), int(g.integers(1, 12)))
        t = (int(g.integers(2, 46)), int(g.integers(68, 79)))
        if not (f[s] and f[t]):
            continue
        res = {}
        for name, (wg, wh) in methods.items():
            n, cost, *_ = S.grid_search(f, s[0], s[1], t[0], t[1], wg, wh, S.MOVES)
            res[name] = (n, cost)
        if not np.isfinite(res["dijkstra"][1]):
            continue
        for name in methods:
            batch[f"{name}_n"].append(res[name][0])
            batch[f"{name}_cost"].append(res[name][1])
        done += 1
    for k, v in batch.items():
        out["batch_" + k] = np.array(v, float)
    ratio = np.array(batch["astar_n"]) / np.array(batch["dijkstra_n"])
    out["batch_ratio_median"] = float(np.median(ratio))
    out["batch_wastar_excess"] = float(np.max(np.array(batch["wastar_cost"]) / np.array(batch["dijkstra_cost"])) - 1)
    out["batch_greedy_excess_mean"] = float(np.mean(np.array(batch["greedy_cost"]) / np.array(batch["dijkstra_cost"]))
                                            - 1)
    assert np.allclose(batch["astar_cost"], batch["dijkstra_cost"])
    return out


# ---------------------------------------------------------------------------
# Local search
# ---------------------------------------------------------------------------
def compute_queens(n_starts=10_000):
    from videos.ai.ai2 import local as L

    g = rng(88)
    out = {}
    for name, side in (("plain", 0), ("sideways", 100)):
        ok, steps_ok, steps_fail = 0, [], []
        tr = np.zeros(0, np.int64)
        nob = np.zeros((0, 8), np.int64)
        for s in range(n_starts):
            q = g.integers(0, 8, 8).astype(np.int64)
            solved, steps, h = L.climb_queens(q, side, s, tr, nob)
            ok += solved
            (steps_ok if solved else steps_fail).append(steps)
        out[name] = {"success": ok / n_starts, "steps_ok": float(np.mean(steps_ok)) if steps_ok else 0.0,
                     "steps_fail": float(np.mean(steps_fail)) if steps_fail else 0.0}
        p = ok / n_starts
        # random restarts: expected climbs 1/p; expected steps (1/p - 1) failures + one success
        out[name]["restart_steps"] = (1 / p - 1) * out[name]["steps_fail"] + out[name]["steps_ok"]
    # one run that gets stuck, one that succeeds: the boards along the way
    runs = {}
    for want in (False, True):
        for s in range(1000):
            q = rng(1000 + s).integers(0, 8, 8).astype(np.int64)
            tr = np.zeros(64, np.int64)
            boards = np.zeros((64, 8), np.int64)
            solved, steps, h = L.climb_queens(q, 0, 5000 + s, tr, boards)
            if solved == want and steps >= 3:
                runs["solved" if want else "stuck"] = {"boards": boards[:steps + 1].tolist(),
                                                       "h": tr[:steps + 1].tolist()}
                break
    out["runs"] = runs
    out["n_starts"] = n_starts
    return out


def compute_tsp(seeds=5, budget=2_000_000):
    from videos.ai.ai2 import local as L

    P = L.BERLIN52
    D = L.dist_matrix(P)
    n = len(P)
    out = {"xy": P, "opt": L.BERLIN52_OPT, "budget": budget}
    nn = [L.tour_len(L.nearest_neighbour(D, s), D) for s in range(n)]
    out["nn_lengths"] = nn
    out["nn_best_tour"] = L.nearest_neighbour(D, int(np.argmin(nn))).tolist()
    # nearest neighbour polished by 2-opt
    polished = []
    for s in range(n):
        t = L.nearest_neighbour(D, s)
        polished.append(L.two_opt_climb(t, D, 10**9)[0])
    out["nn2opt_lengths"] = polished
    # 2-opt hill climbing from random tours: the local optima it lands in
    g = rng(52)
    climbs, looks = [], []
    first_tour, first_opt = None, None
    for k in range(200):
        t = g.permutation(n).astype(np.int64)
        t0 = t.copy()
        Lk, lk = L.two_opt_climb(t, D, 10**9)
        climbs.append(int(Lk))
        looks.append(int(lk))
        if first_tour is None:
            first_tour, first_opt = t0.tolist(), t.tolist()
    out["climb_lengths"] = climbs
    out["climb_looks_mean"] = float(np.mean(looks))
    out["climb_example"] = [first_tour, first_opt]
    # equal budgets: restarts of 2-opt, one annealing run, one GA run, per seed
    eq = {"restarts": [], "anneal": [], "ga": []}
    for s in range(seeds):
        gs = rng(500 + s)
        used, best = 0, 1 << 60
        while used < budget:
            t = gs.permutation(n).astype(np.int64)
            Lk, lk = L.two_opt_climb(t, D, budget - used)
            used += lk
            best = min(best, Lk)
        eq["restarts"].append(int(best))
        n_temps = 200
        snaps = np.zeros((1, n), np.int64)
        tr = np.zeros((n_temps, 4))
        t = gs.permutation(n).astype(np.int64)
        bl, _ = L.anneal(t, D, 300.0, 0.955, budget // n_temps, n_temps, 600 + s, 0, snaps, tr)
        eq["anneal"].append(int(bl))
        pop = 100
        gens = budget // pop
        bp = np.zeros(gens, np.int64)
        eq["ga"].append(int(L.genetic(D, pop, gens, 0.5, 700 + s, bp, np.zeros((1, n), np.int64),
                                      np.array([-1], np.int64))))
        if s == 0:
            out["ga_best_per_gen"] = bp
    out.update({f"eq_{k}": v for k, v in eq.items()})
    # the showcase annealing run: 60 snapshots as it cools
    n_temps, per = 240, 10_000
    snaps = np.zeros((60, n), np.int64)
    tr = np.zeros((n_temps, 4))
    t = rng(7).permutation(n).astype(np.int64)
    bl, best = L.anneal(t, D, 400.0, 0.97, per, n_temps, 7, 4, snaps, tr)
    out["sa_snaps"] = snaps
    out["sa_trace"] = tr
    out["sa_best"] = int(bl)
    out["sa_best_tour"] = best.tolist()
    out["sa_snap_every"] = 4
    out["sa_per_temp"] = per
    return out


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------
def compute_ttt():
    from videos.ai.ai2.play import ttt_counts

    return ttt_counts()


def compute_uniform():
    from videos.ai.ai2.play import uniform_counts

    return uniform_counts()


OPENINGS = [[3, 3, 2, 4], [3, 2, 3, 3, 4], [2, 3, 4, 3], [3, 3, 3, 2, 4, 4]]


def compute_alphabeta(max_depth=9, oracle_depth=8):
    from videos.ai.ai26 import c4
    from videos.ai.ai2.play import Oracle, c4_search

    depths = list(range(1, max_depth + 1))
    out = {"depths": depths, "openings": OPENINGS}
    for name, prune, order in (("minimax", False, 0), ("ab_random", True, 0), ("ab_ordered", True, 1)):
        rows = []
        for d in depths:
            tot = 0
            for i, seq in enumerate(OPENINGS):
                b = c4.Board.from_moves(seq)
                cnt = np.zeros(1, np.int64)
                c4_search(np.int64(b.pos), np.int64(b.mask), b.moves, d, -1e9, 1e9, prune, order, cnt, i + 1)
                tot += int(cnt[0])
            rows.append(tot / len(OPENINGS))
        out[name] = rows
    rows = []
    for d in range(1, oracle_depth + 1):
        tot = 0
        for seq in OPENINGS:
            b = c4.Board.from_moves(seq)
            O = Oracle()
            cnt = [0]
            O.search(b.pos, b.mask, b.moves, d, -1e9, 1e9, cnt)
            tot += cnt[0]
        rows.append(tot / len(OPENINGS))
    out["ab_perfect"] = rows
    # legal moves per position in these searches (the branching factor b), from the full minimax counts
    out["branching"] = float(np.mean([out["minimax"][k + 1] / out["minimax"][k] for k in range(3)]))
    return out


def compute_testset(n=300, seed=2):
    from videos.ai.ai26 import c4

    g = rng(seed)
    S = c4.Solver(23)
    hist, scores = [], []
    tries = 0
    while len(hist) < n:
        tries += 1
        stones = int(g.integers(14, 29))
        b = c4.Board()
        ok = True
        while b.moves < stones:
            legal = b.legal()
            win = [c for c in legal if b.wins_with(c)]
            opp = c4.Board(b.pos ^ b.mask, b.mask, b.moves)
            block = [c for c in legal if opp.wins_with(c)]
            c = win[0] if win else block[0] if block else int(legal[g.integers(len(legal))])
            nb = b.play(c)
            if c4.last_mover_won(nb) or nb.full():
                ok = False
                break
            b = nb
        if not ok:
            continue
        S.reset()
        sc = S.move_scores(b.pos, b.mask, b.moves)
        legal = ~np.isnan(sc)
        best = np.nanmax(sc)
        if (np.sign(sc[legal]) == np.sign(best)).all():
            continue  # every move keeps the result: nothing to test
        hist.append(list(b.history))
        scores.append(sc)
    return {"histories": hist, "scores": np.array(scores), "tries": tries}


def _right(scores_row, c) -> bool:
    return np.sign(scores_row[c]) == np.sign(np.nanmax(scores_row))


def compute_samuel(games=3000, every=250, depth=3, lr=0.003, decay=10**9, seeds=(0, 1, 2), n_eval=200):
    from videos.ai.ai26 import c4
    from videos.ai.ai2 import play as P

    t = load("testset")
    hist, scores = t["histories"], np.asarray(t["scores"])
    W = P.WINDOWS
    programmer = np.array([0.02, 0.1, 0.4, 0.05, 0.3])  # our own guess, set before any training
    zero = np.zeros(P.N_FEAT)
    ev_open = P.random_openings(rng(99), n_eval)

    def accuracy(w):
        ok = 0
        cnt = np.zeros(1, np.int64)
        for h, sc in zip(hist, scores):
            b = c4.Board.from_moves(h)
            _, c = P.negamax_w(np.int64(b.pos), np.int64(b.mask), b.moves, depth, -2.0, 2.0, w, W, cnt)
            ok += _right(sc, c)
        return ok / len(hist)

    out = {"features": P.FEATURES, "programmer": programmer, "depth": depth, "games": games, "every": every,
           "lr": lr, "decay": decay,
           "n_eval_games": 2 * n_eval, "acc_programmer": accuracy(programmer), "acc_zero": accuracy(zero),
           "programmer_vs_zero": P.match(programmer, zero, depth, ev_open)}
    runs = []
    for seed in seeds:
        g = rng(300 + seed)
        alpha = np.zeros(P.N_FEAT)
        beta = alpha.copy()
        log = []
        weights, ckpt, vs_prog, vs_zero, acc, deltas = [alpha.copy()], [0], [], [], [], []
        vs_prog.append(P.match(alpha, programmer, depth, ev_open))
        vs_zero.append(P.match(alpha, zero, depth, ev_open))
        acc.append(accuracy(alpha))
        handovers = 0
        for k in range(1, games + 1):
            op = P.random_openings(g, 1, plies=2 * int(g.integers(1, 3)))[0]
            alpha_first = k % 2 == 0
            lr_k = lr / (1 + k / decay)  # constant unless a decay is given
            if alpha_first:
                r = P.play_game(alpha, beta, depth, op, learn=(lr_k, log))
            else:
                # Alpha moves second: play with Beta as "A" and learn for Alpha through a swapped call
                r = -_play_second(P, alpha, beta, depth, op, lr_k, log)
            if r > 0:
                beta = alpha.copy()  # Samuel: when Alpha wins, Beta takes its scoring polynomial
                handovers += 1
            if k % 10 == 0:
                weights.append(alpha.copy())
            if k % every == 0:
                ckpt.append(k)
                vs_prog.append(P.match(alpha, programmer, depth, ev_open))
                vs_zero.append(P.match(alpha, zero, depth, ev_open))
                acc.append(accuracy(alpha))
                deltas.append(float(np.mean(np.abs(log[-500:]))))
        runs.append({"seed": seed, "weights": np.array(weights).tolist(), "ckpt": ckpt,
                     "vs_programmer": [float(x) for x in vs_prog], "vs_zero": [float(x) for x in vs_zero],
                     "accuracy": [float(x) for x in acc], "handovers": handovers, "delta": deltas})
    out["runs"] = runs
    return out


def _play_second(P, alpha, beta, depth, op, lr, log):
    """A game with Beta moving first after the opening and Alpha learning: returns +1 if Beta wins."""
    from videos.ai.ai26 import c4

    b = c4.Board.from_moves(op)
    b_turn = True
    prev = None
    cnt = np.zeros(1, np.int64)
    while True:
        if b.full():
            result = 0
            break
        w = beta if b_turn else alpha
        v, c = P.negamax_w(np.int64(b.pos), np.int64(b.mask), b.moves, depth, -2.0, 2.0, w, P.WINDOWS, cnt)
        if not b_turn:
            f = P.features(np.int64(b.pos), np.int64(b.mask), P.WINDOWS)
            if prev is not None:
                pv = math.tanh(float(np.dot(alpha, prev)))
                delta = max(-1.0, min(1.0, v)) - pv
                alpha += lr * delta * (1 - pv * pv) * prev
                log.append(delta)
            prev = f
        nb = b.play(int(c))
        if c4.last_mover_won(nb):
            result = 1 if b_turn else -1
            break
        b = nb
        b_turn = not b_turn
    if prev is not None:
        pv = math.tanh(float(np.dot(alpha, prev)))
        delta = -result - pv  # Alpha's result
        alpha += lr * delta * (1 - pv * pv) * prev
        log.append(delta)
    return result


# ---------------------------------------------------------------------------
# Logic
# ---------------------------------------------------------------------------
def compute_resolution():
    from videos.ai.ai2.logic import lit, refute

    L = lit
    # propositional (illustrative): rain or sprinkler wets the grass
    kb = [{L(False, "Rain"), L(True, "Wet")}, {L(False, "Sprinkler"), L(True, "Wet")},
          {L(True, "Rain"), L(True, "Sprinkler")}]
    prop = refute([frozenset(c) for c in kb], [frozenset({L(False, "Wet")})], strategy="support")
    # first order (illustrative): every parent's parent is a grandparent
    kb2 = [{L(False, "Parent", "x", "y"), L(False, "Parent", "y", "z"), L(True, "Grandparent", "x", "z")},
           {L(True, "Parent", "Anne", "Byron")}, {L(True, "Parent", "Byron", "Ada")}]
    fol = refute([frozenset(c) for c in kb2], [frozenset({L(False, "Grandparent", "Anne", "Ada")})],
                 strategy="support")
    # the explosion: a family of eight facts and three rules; saturation against the set of support
    people = ["Anne", "Byron", "Ada", "Ralph", "Clara", "Dora", "Ezra", "Flora"]
    facts = [("Parent", "Anne", "Byron"), ("Parent", "Byron", "Ada"), ("Parent", "Ada", "Ralph"),
             ("Parent", "Clara", "Dora"), ("Parent", "Dora", "Ezra"), ("Parent", "Ezra", "Flora"),
             ("Parent", "Byron", "Clara"), ("Parent", "Ralph", "Flora")]
    kb3 = [{L(False, "Parent", "x", "y"), L(True, "Ancestor", "x", "y")},
           {L(False, "Parent", "x", "y"), L(False, "Ancestor", "y", "z"), L(True, "Ancestor", "x", "z")},
           {L(False, "Ancestor", "x", "y"), L(False, "Ancestor", "y", "x")}] + \
          [{L(True, *f)} for f in facts]
    goal3 = [frozenset({L(False, "Ancestor", "Anne", "Flora")})]
    sat_ = refute([frozenset(c) for c in kb3], goal3, strategy="saturate", max_clauses=4000)
    sos = refute([frozenset(c) for c in kb3], goal3, strategy="support", max_clauses=4000)
    trim = lambda r: {"found": r["found"], "made": len(r["clauses"]), "levels": r["levels"],
                      "proof_len": len(r.get("proof", []))}
    return {"prop": prop, "fol": fol, "explode_saturate": trim(sat_), "explode_support": trim(sos),
            "people": people, "facts": facts}


def compute_sat3(ns=(25, 50, 100, 200), alphas=tuple(np.round(np.arange(3.0, 5.61, 0.1), 2)),
                 per=(400, 300, 200, 100)):
    from videos.ai.ai2.sat import random_3sat, solve_dpll

    out = {"ns": list(ns), "alphas": list(alphas), "per": list(per)}
    part = Partial("sat3", out)
    for n, k in zip(ns, per):
        g = rng(1000 + n)
        psat, med, mean, q90 = [], [], [], []
        for a in alphas:
            key = f"{n}/{a}"
            if key not in part:
                m = int(round(a * n))
                st, dec = [], []
                for _ in range(k):
                    cl = random_3sat(g, n, m)
                    s, d = solve_dpll(cl, n)
                    st.append(s)
                    dec.append(d)
                st, dec = np.array(st), np.array(dec, float)
                part[key] = {"psat": float((st == 1).mean()), "median": float(np.median(dec)),
                             "mean": float(dec.mean()), "q90": float(np.quantile(dec, 0.9)),
                             "rng": g.bit_generator.state}
            r = part[key]
            g.bit_generator.state = r["rng"]
            psat.append(r["psat"])
            med.append(r["median"])
            mean.append(r["mean"])
            q90.append(r["q90"])
        out[f"psat_{n}"] = psat
        out[f"median_{n}"] = med
        out[f"mean_{n}"] = mean
        out[f"q90_{n}"] = q90
        # where the chance crosses one half (linear interpolation)
        p = np.array(psat)
        j = int(np.argmax(p < 0.5))
        a0, a1 = alphas[j - 1], alphas[j]
        out[f"cross_{n}"] = float(a0 + (p[j - 1] - 0.5) / (p[j - 1] - p[j]) * (a1 - a0))
        # the width of the window: from 90% to 10% satisfiable
        def at(level):
            jj = int(np.argmax(p < level))
            return float(alphas[jj - 1] + (p[jj - 1] - level) / (p[jj - 1] - p[jj]) * (alphas[jj] - alphas[jj - 1]))
        out[f"width_{n}"] = at(0.1) - at(0.9)
        out[f"peak_{n}"] = float(alphas[int(np.argmax(med))])
    part.finish()
    return out


def compute_cdcl():
    from videos.ai.ai2 import sat as S

    out = {}
    # one conflict analysed, on a small formula (illustrative, after Marques-Silva & Sakallah's example)
    ex = [[1, 2], [1, 3, 7], [-2, -3, 4], [-4, 5, 8], [-4, 6, 9], [-5, -6]]
    c = S.CDCL(9, ex, record_first_conflict=True)
    # force the decisions of the textbook example: x7 = 0, x8 = 0, x9 = 0, then x1 = 0
    c.lim.append(len(c.trail))
    c._enqueue(-7, None)
    c.lim.append(len(c.trail))
    c._enqueue(-8, None)
    c.lim.append(len(c.trail))
    c._enqueue(-9, None)
    assert c._propagate() is None
    c.lim.append(len(c.trail))
    c._enqueue(-1, None)
    confl = c._propagate()
    assert confl is not None
    snap = c._snapshot(confl)
    learnt, bt, steps = c._analyze(confl)
    snap.update(learned=learnt, backjump=bt, clauses=ex)
    out["example"] = snap

    def adder_miter(w, bug=None):
        C = S.Circuit()
        A = [C.var() for _ in range(w)]
        B = [C.var() for _ in range(w)]
        s1 = C.ripple_adder(A, B)
        s2 = C.kogge_stone_adder(A, B, bug_at=bug)
        C.miter(s1, s2)
        return C, A, B, s1, s2

    def pad(clauses, n):
        F = n + 1
        k = max(len(cl) for cl in clauses)
        return np.array([list(cl) + [F] * (k - len(cl)) for cl in clauses] + [[-F] * k], np.int64), n + 1

    widths = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    part = Partial("cdcl", {"widths": widths, "big": [16, 32, 64], "mult": list(range(2, 9))})
    dp, cd = [], []
    for w in widths:
        if f"adder/{w}" not in part:
            C, *_ = adder_miter(w)
            arr, n = pad(C.clauses, C.n)
            st, dec = S.solve_dpll(arr, n)
            assert st == 0
            sv = S.CDCL(C.n, C.clauses)
            assert sv.solve() is False
            part[f"adder/{w}"] = [int(dec), sv.stats["conflicts"]]
        dp.append(part[f"adder/{w}"][0])
        cd.append(part[f"adder/{w}"][1])
    out.update(adder_widths=widths, adder_dpll=dp, adder_cdcl=cd)
    big = {}
    for w in (16, 32, 64):
        if f"big/{w}" not in part:
            C, *_ = adder_miter(w)
            t = time.time()
            sv = S.CDCL(C.n, C.clauses)
            r = sv.solve()
            assert r is False
            part[f"big/{w}"] = {"vars": C.n, "clauses": len(C.clauses), "conflicts": sv.stats["conflicts"],
                                "secs": time.time() - t}
        big[w] = part[f"big/{w}"]
    out["proved"] = big
    # the buggy adder: a counterexample, checked by evaluating both circuits
    w = 16
    C, A, B, s1, s2 = adder_miter(w, bug=6)
    sv = S.CDCL(C.n, C.clauses)
    assert sv.solve() is True
    a = [int(sv.model[v]) for v in A]
    b = [int(sv.model[v]) for v in B]
    o1 = [int(sv.model[v]) for v in s1]
    o2 = [int(sv.model[v]) for v in s2]
    assert o1 == S.eval_adder_bits(a, b) and o1 != o2
    out["bug"] = {"width": w, "bit": 6, "a": sum(x << i for i, x in enumerate(a)),
                  "b": sum(x << i for i, x in enumerate(b)), "right": sum(x << i for i, x in enumerate(o1)),
                  "wrong": sum(x << i for i, x in enumerate(o2)), "conflicts": sv.stats["conflicts"],
                  "vars": C.n, "clauses": len(C.clauses)}
    # multipliers: is a * b = b * a?  hard for clause learning
    mw, mc = [], []
    for w in range(2, 9):
        if f"mult/{w}" not in part:
            C = S.Circuit()
            A = [C.var() for _ in range(w)]
            B = [C.var() for _ in range(w)]
            C.miter(C.array_multiplier(A, B), C.array_multiplier(B, A))
            sv = S.CDCL(C.n, C.clauses)
            r = sv.solve(max_conflicts=200_000)
            assert r is not True
            part[f"mult/{w}"] = None if r is None else sv.stats["conflicts"]
        if part[f"mult/{w}"] is None:
            break
        mw.append(w)
        mc.append(part[f"mult/{w}"])
    out.update(mult_widths=mw, mult_conflicts=mc)
    part.finish()
    return out


# ---------------------------------------------------------------------------
# Constraints and plans
# ---------------------------------------------------------------------------
def compute_sudoku():
    from videos.ai.ai2 import csp

    g = rng(9)
    puzzle, solution = csp.make_puzzle(g, min_clues=23)
    assert csp.count_solutions(puzzle) == 1
    D = csp.domains_of(puzzle)
    log = []
    ok = csp.ac3(D, log)
    sizes_after = [len(d) for d in D]
    out = {"puzzle": puzzle, "solution": solution, "clues": sum(1 for x in puzzle if x), "ac3_log": log,
           "ac3_sizes": sizes_after, "ac3_solved": sum(1 for s in sizes_after if s == 1) - sum(1 for x in puzzle if x)}
    for kind in ("plain", "fc", "mrv", "mac"):
        n, ok, assign = csp.backtrack(puzzle, kind)
        assert ok and assign == solution
        out[f"nodes_{kind}"] = n
    out["values_total"] = 81 * 9
    return out


def compute_blocks(per_n=12):
    from videos.ai.ai2.plan import Blocks, random_towers, towers_count

    out = {"states": [], "towers": []}
    for n in range(1, 8):
        B = Blocks("ABCDEFGHIJ"[:n])
        out["states"].append(B.count_states(B.state([[i] for i in range(n)])))
        out["towers"].append(towers_count(n))
    # Sussman's anomaly: C on A, B on the table; goal A on B on C
    B = Blocks("ABC")
    s0 = B.state([[0, 2], [1]])  # A with C on it; B
    goal = B.goal([[2, 1, 0]])  # C at the bottom, then B, then A
    plan, exp = B.bfs(s0, goal)
    out["sussman_plan"] = [B.show(k) for k in plan]
    out["sussman_expanded"] = exp
    # the two goals one at a time (the 'linear' planner's trap): achieving on(A, B) first, then on(B, C)
    g1 = B.F("on", 0, 1)
    p1, _ = B.bfs(s0, g1)
    s1 = s0
    for k in p1:
        s1 = (s1 & ~B.actions[k][3]) | B.actions[k][2]
    p2, _ = B.bfs(s1, B.F("on", 1, 2))
    s2 = s1
    for k in p2:
        s2 = (s2 & ~B.actions[k][3]) | B.actions[k][2]
    # the other order: B on C first, then A on B
    h1 = B.F("on", 1, 2)
    q1, _ = B.bfs(s0, h1)
    t1 = s0
    for k in q1:
        t1 = (t1 & ~B.actions[k][3]) | B.actions[k][2]
    q2, _ = B.bfs(t1, B.F("on", 0, 1))
    t2 = t1
    for k in q2:
        t2 = (t2 & ~B.actions[k][3]) | B.actions[k][2]
    out["sussman_other_first"] = [B.show(k) for k in q1]
    out["sussman_other_second"] = [B.show(k) for k in q2]
    out["sussman_other_kept"] = bool(t2 & h1)
    out["sussman_first"] = [B.show(k) for k in p1]
    out["sussman_second"] = [B.show(k) for k in p2]
    out["sussman_first_kept"] = bool(s2 & g1)
    g = rng(71)
    rows = []
    for n in range(4, 11):
        B = Blocks("ABCDEFGHIJKL"[:n])
        for _ in range(per_n):
            s0 = B.state(random_towers(g, n))
            goal = B.goal(random_towers(g, n))
            row = {"n": n}
            if n <= 7:
                t = time.time()
                p, e = B.bfs(s0, goal)
                row.update(bfs=e, bfs_len=len(p) if p is not None else -1)
            if n <= 7:
                p, e = B.best_first(s0, goal, kind="max")
                row.update(hmax=e, hmax_len=len(p) if p is not None else -1)
            p, e = B.best_first(s0, goal, kind="ff", greedy=True)
            row.update(ff=e, ff_len=len(p) if p is not None else -1)
            if "bfs_len" in row:
                assert row["hmax_len"] == row["bfs_len"]
            rows.append(row)
    out["rows"] = rows
    return out


# ---------------------------------------------------------------------------
# Knowledge
# ---------------------------------------------------------------------------
RULES = [  # an illustrative rule base, in the manner of Winston's zoo-keeper
    ("R1", ["has hair"], "mammal"),
    ("R2", ["gives milk"], "mammal"),
    ("R3", ["has feathers"], "bird"),
    ("R4", ["mammal", "eats meat"], "carnivore"),
    ("R5", ["mammal", "has pointed teeth", "has claws"], "carnivore"),
    ("R6", ["carnivore", "tawny colour", "dark spots"], "cheetah"),
    ("R7", ["carnivore", "tawny colour", "black stripes"], "tiger"),
    ("R8", ["bird", "does not fly", "swims"], "penguin"),
]


def compute_rules():
    facts = ["has hair", "has pointed teeth", "has claws", "tawny colour", "dark spots"]
    known = list(facts)
    fired = []
    changed = True
    while changed:
        changed = False
        for name, ifs, then in RULES:
            if then not in known and all(c in known for c in ifs):
                known.append(then)
                fired.append(name)
                changed = True
    # MYCIN's certainty factors: two rules supporting the same conclusion with CF 0.6 and 0.5
    cf = [0.6, 0.5, 0.4]
    combined = []
    acc = 0.0
    for x in cf:
        acc = acc + x * (1 - acc)
        combined.append(acc)
    return {"rules": [list(r) for r in RULES], "facts": facts, "fired": fired, "derived": known[len(facts):],
            "cf": cf, "cf_combined": combined}


def compute_eliza():
    from videos.ai.ai2.eliza import WEIZENBAUM_1966, Eliza

    e = Eliza()
    convo = []
    for user, theirs in WEIZENBAUM_1966:
        ours = e.respond(user)
        convo.append({"user": user, "ours": ours, "1966": theirs, "same": ours == theirs})
    e = Eliza()
    new = ["I feel that nobody understands me.", "What is the capital of France?",
           "Can you prove that every even number is the sum of two primes?", "I am a computer program.",
           "Why can't I sleep?", "My dog died last week."]
    return {"convo": convo, "matches": sum(c["same"] for c in convo), "new": [[u, e.respond(u)] for u in new]}


def compute_tail():
    from videos.ai.ai1 import compute as ai1  # Part 1's corpus (it downloads and splits the novels if needed)

    word = re.compile(r"[a-z]+(?:'[a-z]+)?")
    train = word.findall(ai1.text("train").lower())
    valid = word.findall(ai1.text("valid").lower())
    passage = word.findall(ai1.text("passage").lower())
    cnt = Counter(train)
    freqs = np.array(sorted(cnt.values(), reverse=True), float)
    cum = np.cumsum(freqs) / freqs.sum()
    need = {str(q): int(np.searchsorted(cum, q) + 1) for q in (0.5, 0.9, 0.95, 0.99, 0.999)}
    once = int((freqs == 1).sum())
    # unseen words in fresh text, as the training text grows
    sizes = np.unique(np.round(np.geomspace(10_000, len(train), 24)).astype(int))
    unseen_valid, unseen_passage = [], []
    seen = set()
    last = 0
    for s in sizes:
        seen.update(train[last:s])
        last = s
        unseen_valid.append(float(np.mean([w not in seen for w in valid])))
        unseen_passage.append(float(np.mean([w not in seen for w in passage])))
    new_in_passage = sorted({w for w in passage if w not in cnt})
    k = np.unique(np.round(np.geomspace(1, len(freqs), 200)).astype(int))
    return {"n_tokens": len(train), "n_types": len(cnt), "need": need, "once": once,
            "coverage_k": k, "coverage": cum[k - 1], "sizes": sizes, "unseen_valid": unseen_valid,
            "unseen_passage": unseen_passage, "passage_tokens": len(passage), "passage_new": new_in_passage,
            "top": [w for w, _ in cnt.most_common(12)]}


ITEMS = {
    "tm": compute_tm,
    "puzzle8": compute_puzzle8,
    "puzzle15": compute_puzzle15,
    "grid": compute_grid,
    "queens": compute_queens,
    "tsp": compute_tsp,
    "ttt": compute_ttt,
    "uniform": compute_uniform,
    "alphabeta": compute_alphabeta,
    "testset": compute_testset,
    "samuel": compute_samuel,
    "resolution": compute_resolution,
    "sat3": compute_sat3,
    "cdcl": compute_cdcl,
    "sudoku": compute_sudoku,
    "blocks": compute_blocks,
    "rules": compute_rules,
    "eliza": compute_eliza,
    "tail": compute_tail,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
