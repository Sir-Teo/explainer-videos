"""Precompute everything numerical in Part 29 of the AI series ("Agents and Worlds").

    python -m videos.ai.ai29.compute              # everything missing
    python -m videos.ai.ai29.compute --force lane

Results are cached in ``.cache/ai29/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Everything is seeded and
runs on the CPU; the longest items (``dreamer``, ``klbal``) keep each seed as it finishes, so a killed run resumes.
Torch uses ``AI29_THREADS`` threads (default 2).  About an hour on a laptop.

Items:
    belief     a robot in a corridor of 40 cells with 4 doors, unsure where it is: it moves (sometimes slipping) and
               senses doors (sometimes wrongly); its belief, updated by Bayes' rule step by step (Part 7's forward
               algorithm), and how sure it ends up
    horizon    long tasks: the chance of finishing a task of n steps when each step succeeds with probability p, and
               the task length an agent finishes half the time, as p rises
    agent      a simulated agent loop (no language model, no network calls): tasks of n tool calls in a little
               warehouse, solved three ways (in its head; ReAct with tools, seeing tool errors; ReAct that also checks
               its work), with error rates we set; real traces, and success against n
    metr       METR's measured time horizons (Time Horizon 1.1, cited data), fitted here: the doubling time with a
               bootstrap, and the 80% horizons against a constant-hazard model
    lane       imitation learning on a windy lane: behaviour cloning against DAgger at equal numbers of expert
               labels, 8 seeds; the expected cost over T steps computed exactly, against the T^2 epsilon bound
    world      a small world model: frames of a ball bouncing in a box (16 x 16 pixels); an encoder to 8 numbers, a
               network that predicts the next 8 numbers, a decoder; its imagined future against the real one, and how
               its error grows with the horizon
    dreamer    a Dreamer-lite (RSSM world model from pixels, actor-critic trained only in imagination) on a 12 x 12
               game of catch, 3 seeds: learning curves, imagined against real futures, the policy's play
    klbal      the world model alone, with DreamerV3's balanced KL against a plain KL of the same total weight, 3 seeds
    symlog     regression of rewards of four games whose scales differ a thousandfold: squared error on the raw
               rewards against squared error after symlog
    detour     demonstrations that pass an obstacle on either side: a regression policy against a flow-matching policy
               (pi0's action expert in miniature), 5 seeds
    fast       FAST action tokens on smooth seven-joint motion: the cosine transform, rounding, byte-pair encoding;
               tokens per chunk against reconstruction error, and per-step binning (RT-2, OpenVLA) for comparison
    randomize  domain randomization on Part 26's cart-pole: a policy trained in one simulator against one trained in
               many, tested on a "real" cart-pole with a longer pole, a weaker motor, a delay and a noisy sensor
"""

from __future__ import annotations

import math
import os
from collections import Counter
from datetime import date

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai29")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _torch():
    import torch

    torch.set_num_threads(int(os.environ.get("AI29_THREADS", "2")))
    return torch


def _log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------------------
def compute_belief():
    n = 40
    doors = np.zeros(n, bool)
    doors[[3, 8, 19, 33]] = True  # unevenly spaced, so the pattern of doors tells places apart
    p_hit, p_false = 0.9, 0.05  # sees a door when at one / when not
    p_move = 0.8  # a step of +1 succeeds; otherwise it stays
    g = rng(2005)  # Thrun, Burgard & Fox, Probabilistic Robotics
    pos = 2
    belief = np.full(n, 1 / n)
    beliefs, poss, obs = [belief.copy()], [pos], []
    for t in range(40):
        # move right by one (circular corridor), with a chance of slipping
        pos = (pos + 1) % n if g.random() < p_move else pos
        belief = p_move * np.roll(belief, 1) + (1 - p_move) * belief  # predict
        z = (g.random() < p_hit) if doors[pos] else (g.random() < p_false)
        like = np.where(doors, p_hit if z else 1 - p_hit, p_false if z else 1 - p_false)
        belief = belief * like
        belief /= belief.sum()  # update: Bayes' rule
        beliefs.append(belief.copy())
        poss.append(pos)
        obs.append(bool(z))
    beliefs = np.array(beliefs)
    ent = -(beliefs * np.log2(np.maximum(beliefs, 1e-300))).sum(1)
    out = dict(n=n, doors=np.where(doors)[0], beliefs=beliefs, pos=np.array(poss), obs=np.array(obs), entropy=ent,
               p_hit=p_hit, p_false=p_false, p_move=p_move)
    assert beliefs[-1].argmax() in (poss[-1] - 1, poss[-1], poss[-1] + 1) and ent[-1] < 0.5 * ent[0]
    return out


# ---------------------------------------------------------------------------
def compute_horizon():
    ps = [0.9, 0.99, 0.999]
    ns = np.unique(np.round(np.logspace(0, 4, 200)).astype(int))
    out = dict(ps=ps, ns=ns)
    for p in ps:
        out[f"succ{p:g}"] = p ** ns.astype(float)
    pr = np.linspace(0.5, 0.9999, 400)
    out["p_range"] = pr
    out["half_len"] = np.log(0.5) / np.log(pr)  # p^n = 1/2
    assert abs(out["half_len"][-1] - math.log(0.5) / math.log(0.9999)) < 1e-6
    # sixty simulated runs of a 30-step task at 97% a step: the step at which each first goes wrong
    g = rng(30)
    fails = g.geometric(1 - 0.97, size=60)
    out["runs_fail"] = fails
    out["runs_ok"] = float((fails > 30).mean())
    assert abs(out["runs_ok"] - 0.97 ** 30) < 0.15
    return out


# ---------------------------------------------------------------------------
# A simulated agent loop
# ---------------------------------------------------------------------------
AGENT_RATES = dict(head=0.06, malformed=0.10, silent=0.02, catch=0.7)
ITEMS_W = ["bolt", "gear", "hinge", "lamp", "valve", "spring", "pulley", "clamp", "fuse", "cable", "drill", "rivet"]


class Warehouse:
    """The tools: ``shelf(k)`` lists the items on shelf k; ``price(item)`` gives an item's price; ``add(a, b)``.  A
    task: the total price of the items on some shelves.  Each item costs a lookup and an addition."""

    def __init__(self, g, shelves=12):
        self.shelf_items = {k: list(g.choice(ITEMS_W, size=int(g.integers(2, 5)), replace=False)) for k in range(1, shelves + 1)}
        self.prices = {it: int(g.integers(3, 60)) for it in ITEMS_W}

    def call(self, tool, arg):
        if tool == "shelf":
            if arg not in self.shelf_items:
                return None, f"error: no shelf {arg!r}"
            return self.shelf_items[arg], ", ".join(self.shelf_items[arg])
        if tool == "price":
            if arg not in self.prices:
                return None, f"error: unknown item {arg!r}"
            return self.prices[arg], str(self.prices[arg])
        if tool == "add":
            a, b = arg
            return a + b, str(a + b)
        return None, f"error: no tool {tool!r}"


def agent_episode(w, items, mode, g, rates=AGENT_RATES, trace=False):
    """Total the prices of ``items`` (n = len(items) steps: look up a price, add it).  ``mode``: 'head' (no tools:
    each step silently wrong with probability rates['head']), 'react' (each step a tool call: malformed with
    probability 'malformed', which the tool reports, so the agent retries; silently wrong, a real item but the wrong
    one, with probability 'silent'), 'check' (as react, then a second call re-reads the price and catches a silent
    slip with probability 'catch').  A budget of 3n + 4 calls.  Returns (right, calls, trace lines)."""
    total, true_total, calls, lines = 0, 0, 0, []
    budget = 3 * len(items) + 4
    say = lines.append if trace else (lambda s: None)
    for it in items:
        true_total += w.prices[it]
        if mode == "head":
            v = w.prices[it]
            if g.random() < rates["head"]:
                v += int(g.choice([-10, -1, 1, 10]))
                v = v if v > 0 else v + 20  # a wrong price, but a plausible one
            say(f"Thought: {it} costs {v}, so the total is {total + v}.")
            total += v
            calls += 1
            continue
        done = False
        while not done:
            if calls >= budget:
                say("Answer: out of steps.")
                return False, calls, lines
            calls += 1
            r = g.random()
            if r < rates["malformed"]:
                bad = it[:-1] if len(it) > 3 else it + "s"
                _, obs = w.call("price", bad)
                say(f'Action: price("{bad}")')
                say(f"Observation: {obs}")
                continue
            target = it
            if r < rates["malformed"] + rates["silent"]:
                target = str(g.choice([x for x in ITEMS_W if x != it]))
            v, obs = w.call("price", target)
            say(f'Action: price("{target}")')
            say(f"Observation: {obs}")
            if mode == "check" and target != it and calls < budget:
                calls += 1
                if g.random() < rates["catch"]:
                    say(f"Thought: that was {target}, not {it}. Again.")
                    continue
            total += v
            done = True
        say(f"Thought: the total so far is {total}.")
    say(f"Answer: {total}")
    return total == true_total, calls, lines


def compute_agent(tasks=3000, ns=(1, 2, 3, 5, 8, 12, 20, 30, 45, 60)):
    g = rng(2022)  # Yao et al., ReAct (2022)
    out = dict(ns=list(ns), rates=AGENT_RATES, tasks=tasks)
    for mode in ("head", "react", "check"):
        succ, cost = [], []
        for n in ns:
            ok, cs = 0, 0
            for _ in range(tasks):
                w = Warehouse(g)
                items = list(g.choice(ITEMS_W, size=n, replace=True))
                r, c, _ = agent_episode(w, items, mode, g)
                ok += r
                cs += c
            succ.append(ok / tasks)
            cost.append(cs / tasks)
        out[f"{mode}_succ"] = succ
        out[f"{mode}_calls"] = cost
        # the per-step reliability that p^n would need to match, fitted on log success
        s = np.array(succ)
        m = s > 0.02
        out[f"{mode}_p"] = float(np.exp(np.polyfit(np.array(ns)[m], np.log(s[m]), 1)[0]))
    # the per-step silent-error rate each mode works out to, in theory
    out["theory"] = dict(head=1 - AGENT_RATES["head"], react=1 - AGENT_RATES["silent"],
                         check=1 - AGENT_RATES["silent"] * (1 - AGENT_RATES["catch"]))
    # traces to show: one of each, three items, the same task
    tg = rng(7)
    w = Warehouse(tg)
    items = ["gear", "valve", "rivet"]
    traces = {}
    # for each mode, the first seed whose run shows what the mode is about: a silent slip in the head; a tool error
    # seen and retried; a slip caught by the check
    want = dict(head=lambda r, ls: not r, react=lambda r, ls: r and any("error" in x for x in ls),
                check=lambda r, ls: r and any("Again" in x for x in ls))
    for mode in ("head", "react", "check"):
        for seed in range(10_000):
            r, c, lines = agent_episode(w, items, mode, rng(seed), trace=True)
            if want[mode](r, lines):
                break
        traces[mode] = dict(right=bool(r), calls=c, lines=lines, seed=seed)
    out["traces"] = traces
    out["trace_items"] = items
    out["trace_prices"] = [w.prices[i] for i in items]
    return out


# ---------------------------------------------------------------------------
# METR's time horizons (cited data), fitted here
# ---------------------------------------------------------------------------
# metr.org/assets/benchmark_results_1_1.yaml, METR-Horizon-v1.1 (retrieved 29 October 2026): model, release date,
# 50% horizon (minutes) with its 95% interval, 80% horizon (minutes), whether it was the frontier when released.
METR = [
    ("GPT-2", "2019-02-14", 0.054, 0.012, 0.137, 0.0128, True),
    ("GPT-3 (davinci-002)", "2020-05-28", 0.144, 0.089, 0.220, 0.0562, True),
    ("GPT-3.5 (instruct)", "2022-03-15", 0.599, 0.260, 1.123, 0.255, True),
    ("GPT-4", "2023-03-14", 3.99, 1.93, 8.00, 0.890, True),
    ("GPT-4 Turbo (1106)", "2023-11-06", 4.04, 1.87, 8.44, 0.783, True),
    ("Claude 3 Opus", "2024-03-04", 3.95, 1.71, 8.76, 0.639, False),
    ("GPT-4 Turbo", "2024-04-09", 3.73, 1.98, 6.74, 0.928, False),
    ("GPT-4o", "2024-05-13", 6.99, 4.00, 12.91, 1.267, True),
    ("Claude 3.5 Sonnet", "2024-06-20", 11.40, 5.49, 22.38, 1.672, True),
    ("o1-preview", "2024-09-12", 20.33, 11.72, 33.38, 4.421, True),
    ("Claude 3.5 Sonnet (new)", "2024-10-22", 20.52, 10.14, 40.82, 2.596, True),
    ("o1", "2024-12-05", 38.83, 21.16, 64.95, 7.090, True),
    ("Claude 3.7 Sonnet", "2025-02-24", 60.39, 33.01, 104.23, 12.09, True),
    ("o3", "2025-04-16", 119.73, 74.62, 190.94, 29.98, True),
    ("Claude 4 Opus", "2025-05-22", 100.37, 59.99, 163.45, 20.43, False),
    ("Claude 4.1 Opus", "2025-08-05", 100.47, 59.27, 159.45, 23.46, False),
    ("GPT-5", "2025-08-07", 203.01, 112.64, 405.55, 38.31, True),
    ("Gemini 3 Pro", "2025-11-18", 224.33, 139.57, 379.24, 54.14, True),
    ("GPT-5.1-Codex-Max", "2025-11-19", 223.71, 134.31, 396.21, 50.63, False),
    ("Claude Opus 4.5", "2025-11-24", 292.99, 161.72, 623.70, 49.43, True),
    ("GPT-5.2", "2025-12-11", 352.25, 198.07, 815.18, 66.00, True),
    ("Claude Opus 4.6", "2026-02-05", 718.81, 316.69, 3633.79, 69.87, True),
    ("GPT-5.3-Codex", "2026-02-05", 349.53, 194.91, 816.35, 54.74, False),
    ("Gemini 3.1 Pro", "2026-02-19", 384.15, 233.50, 694.75, 89.80, False),
    ("GPT-5.4", "2026-03-05", 341.74, 186.58, 768.78, 53.88, False),
    ("Claude Mythos Preview (early)", "2026-04-07", 1044.78, 508.88, 3304.26, 185.91, True),
]
METR_FIT = dict(from_2023=128.744, lo=104.428, hi=158.012, all_time=187.778)  # METR's own doubling times, days
RELIABLE = 16 * 60  # METR: measurements above 16 hours are unreliable with the current task suite


def years(d: str) -> float:
    y, m, dd = (int(x) for x in d.split("-"))
    return (date(y, m, dd) - date(2019, 1, 1)).days / 365.25


def compute_metr(boots=4000):
    rows = [dict(name=n, date=d, t=years(d), p50=p, lo=lo, hi=hi, p80=p8, sota=s) for n, d, p, lo, hi, p8, s in METR]
    t = np.array([r["t"] for r in rows])
    y50 = np.log2([r["p50"] for r in rows])
    y80 = np.log2([r["p80"] for r in rows])
    sota = np.array([r["sota"] for r in rows])
    ok = np.array([r["p50"] <= RELIABLE for r in rows])
    g = rng(2025)

    def fit(mask, y):
        A = np.stack([np.ones(mask.sum()), t[mask]], 1)
        return np.linalg.lstsq(A, y[mask], rcond=None)[0]

    def boot(mask, y):
        idx = np.flatnonzero(mask)
        out = []
        for _ in range(boots):
            k = g.choice(idx, len(idx), replace=True)
            if len(np.unique(t[k])) < 3:
                continue
            out.append(np.linalg.lstsq(np.stack([np.ones(len(k)), t[k]], 1), y[k], rcond=None)[0][1])
        return 365.25 / np.array(out)

    m23 = sota & ok & (t >= years("2023-01-01"))
    mall = sota & ok
    c23, call = fit(m23, y50), fit(mall, y50)
    d23 = boot(m23, y50)
    c80 = fit(m23, y80)
    ratio = np.array([r["p50"] / r["p80"] for r in rows])
    # a constant hazard (each minute of work fails with the same chance) predicts p50 / p80 = ln 2 / ln 1.25
    ch = math.log(2) / math.log(1.25)
    # the per-hour failure rate a constant hazard would give each frontier model: ln 2 / p50
    return dict(rows=rows, coef_2023=c23, coef_all=call, doubling_2023=365.25 / c23[1],
                doubling_ci=(float(np.percentile(d23, 2.5)), float(np.percentile(d23, 97.5))),
                doubling_all=365.25 / call[1], doubling_80=365.25 / c80[1], coef_80=c80, metr=METR_FIT,
                ratio=ratio, ratio_median=float(np.median(ratio)), ratio_hazard=ch, n_fit=int(m23.sum()),
                n_all=int(mall.sum()), reliable_min=RELIABLE, t2023=years("2023-01-01"))


# ---------------------------------------------------------------------------
# Imitation on a windy lane: behaviour cloning against DAgger
# ---------------------------------------------------------------------------
LANE = dict(D=10, wind=0.3, noise=0.2, demo_len=50)


class Lane:
    """A car's offset d from the centre of a lane (-D ... D, the verges at +-D).  Each step the driver steers left,
    straight or right (a = -1, 0, +1) and the wind pushes it one to the right with probability ``wind``:
    d' = clip(d + a + w).  The cost is 1 for every step with |d| >= 2, off the lane.  The expert knows d and steers
    back (a = -1 if d >= 0, else +1), so it never leaves the lane.  The learner sees d through a noisy camera: one
    cell off either way, with probability ``noise``."""

    def __init__(self, D=LANE["D"], wind=LANE["wind"], noise=LANE["noise"]):
        self.D, self.wind, self.noise = D, wind, noise
        self.offs = np.arange(-D, D + 1)
        self.S = len(self.offs)
        self.expert = np.where(self.offs >= 0, -1, 1)
        self.cost = (np.abs(self.offs) >= 2).astype(float)
        self.Pobs = np.zeros((self.S, self.S))  # P(o | d)
        for i, d in enumerate(self.offs):
            for nz, p in ((-1, noise / 2), (0, 1 - noise), (1, noise / 2)):
                self.Pobs[i, self.clip(d + nz) + D] += p

    def clip(self, x):
        return int(np.clip(x, -self.D, self.D))

    def chain(self, table=None):
        """P[d, d'] for a learner acting on what it sees (``table[o]``), or for the expert (``None``)."""
        D, S = self.D, self.S
        P = np.zeros((S, S))
        for i, d in enumerate(self.offs):
            acts = [(1.0, self.expert[i])] if table is None else [(self.Pobs[i, j], table[j]) for j in range(S)
                                                                 if self.Pobs[i, j] > 0]
            for po, a in acts:
                for w, pw in ((1, self.wind), (0, 1 - self.wind)):
                    P[i, self.clip(d + a + w) + D] += po * pw
        return P

    def run(self, table, T):
        """Exactly: the expected cumulative cost J(1..T) and the distribution of d at each step, from d = 0."""
        P = self.chain(table)
        p = np.zeros(self.S)
        p[self.D] = 1
        ps, per = [p], []
        for _ in range(T):
            p = p @ P
            ps.append(p)
            per.append(p @ self.cost)
        return np.cumsum(per), np.array(ps)

    def rollout(self, table, T, g):
        """A sampled drive from d = 0: (offsets, what the camera showed); ``table`` None drives the expert."""
        d, ds, os_ = 0, [], []
        for _ in range(T):
            o = self.clip(d + g.choice([-1, 0, 1], p=[self.noise / 2, 1 - self.noise, self.noise / 2]))
            ds.append(d)
            os_.append(o)
            a = self.expert[d + self.D] if table is None else table[o + self.D]
            d = self.clip(d + a + (1 if g.random() < self.wind else 0))
        return np.array(ds), np.array(os_)

    def eps(self, table, T):
        """The learner's error rate on the expert's own drives: E over the expert's states of P(table[o] != expert)."""
        _, ps = self.run(None, T)
        dstar = ps[:T].mean(0)
        wrong = (table[None, :] != self.expert[:, None]).astype(float)  # [d, o]
        return float((dstar[:, None] * self.Pobs * wrong).sum())


def lane_table(counts, S, D, seed):
    """The learner: for each camera reading, the expert's most common action there; readings it has never been
    shown keep an arbitrary action, fixed by the seed (as an untrained network's output is arbitrary but fixed)."""
    tab = rng(seed).integers(-1, 2, size=S)
    for o, c in counts.items():
        tab[o + D] = max(sorted(c), key=lambda a: c[a])
    return tab


def lane_add(counts, lane, ds, os_):
    for d, o in zip(ds, os_):
        c = counts.setdefault(int(o), Counter())
        c[int(lane.expert[d + lane.D])] += 1


def lane_learn(lane, method, N, seed, history=False):
    """``N`` expert labels.  BC: N / L demonstrations of L steps.  DAgger: the first L labels from a demonstration,
    then each round the learner drives L steps and the expert labels what it saw."""
    L = LANE["demo_len"]
    g = rng(seed)
    counts, hist = {}, []
    if method == "bc":
        for _ in range(N // L):
            lane_add(counts, lane, *lane.rollout(None, L, g))
            if history:
                hist.append(np.concatenate([lane_table(counts, lane.S, lane.D, 100 + seed), _seen(counts, lane)]))
        return lane_table(counts, lane.S, lane.D, 100 + seed), hist
    lane_add(counts, lane, *lane.rollout(None, L, g))
    tab = lane_table(counts, lane.S, lane.D, 100 + seed)
    drives = []
    if history:
        hist.append(np.concatenate([tab, _seen(counts, lane)]))
    for _ in range(N // L - 1):
        ds, os_ = lane.rollout(tab, L, g)
        drives.append(ds)
        lane_add(counts, lane, ds, os_)
        tab = lane_table(counts, lane.S, lane.D, 100 + seed)
        if history:
            hist.append(np.concatenate([tab, _seen(counts, lane)]))
    return tab, (hist, drives)


def _seen(counts, lane):
    m = np.zeros(lane.S, int)
    for o in counts:
        m[o + lane.D] = 1
    return m


def compute_lane(seeds=8, T=400, N=400, budgets=(50, 100, 200, 400, 800, 1600)):
    lane = Lane()
    Je, pse = lane.run(None, T)
    out = dict(params=LANE, T=T, N=N, seeds=seeds, offs=lane.offs, expert=lane.expert, J_expert=Je,
               budgets=list(budgets))
    for method in ("bc", "dagger"):
        Js, eps_, tabs = [], [], []
        for s in range(seeds):
            tab, _ = lane_learn(lane, method, N, s)
            J, _ = lane.run(tab, T)
            Js.append(J)
            eps_.append(lane.eps(tab, T))
            tabs.append(tab)
        out[f"{method}_J"] = np.array(Js)
        out[f"{method}_eps"] = np.array(eps_)
        out[f"{method}_tabs"] = np.array(tabs)
        # the cost at the end of the horizon against the label budget
        out[f"{method}_budget"] = np.array([[lane.run(lane_learn(lane, method, n, s)[0], T)[0][-1] for s in range(seeds)]
                                            for n in budgets])
    # the bound J(BC) <= J(expert) + T^2 eps holds for every horizon (Ross & Bagnell 2010): checked, every seed
    ts = np.arange(1, T + 1)
    for s in range(seeds):
        e = [lane.eps(out["bc_tabs"][s], int(t)) for t in (10, 50, 200)]
        for t, et in zip((10, 50, 200), e):
            assert out["bc_J"][s][t - 1] <= Je[t - 1] + t * t * et + 1e-9
    # how the cost grows with the horizon: the slope of log J against log T, over the first steps and over the run
    def slope(J, a, b):
        return float(np.polyfit(np.log(ts[a:b]), np.log(np.maximum(J[a:b], 1e-12)), 1)[0])

    for method in ("bc", "dagger"):
        Jm = out[f"{method}_J"].mean(0)
        out[f"{method}_slope_early"] = slope(Jm, 9, 60)
        out[f"{method}_slope_late"] = slope(Jm, 200, T)
    # the replays: BC's table as demonstrations accumulate, DAgger's round by round (seed 0), and DAgger's own drives
    _, out["bc_hist"] = (lambda r: (r[0], np.array(r[1])))(lane_learn(lane, "bc", N, 0, history=True))
    _, (hist, drives) = lane_learn(lane, "dagger", N, 0, history=True)
    out["dagger_hist"] = np.array(hist)
    out["dagger_drives"] = np.array(drives)
    out["dagger_hist_J"] = np.array([lane.run(t_[:lane.S], T)[0][-1] for t_ in hist])  # rows: table, then seen
    # sampled drives for the pictures: seed 0's learners and the expert, the same wind and camera for all three
    for name, tab in (("expert", None), ("bc", out["bc_tabs"][0]), ("dagger", out["dagger_tabs"][0])):
        out[f"drives_{name}"] = np.array([lane.rollout(tab, 120, rng(900 + k))[0] for k in range(12)])
    out["dist_bc"] = lane.run(out["bc_tabs"][0], T)[1][[25, 100, 400]]
    out["dist_dagger"] = lane.run(out["dagger_tabs"][0], T)[1][[25, 100, 400]]
    return out


# ---------------------------------------------------------------------------
def frames(g, n_seq, T, size=16):
    """Balls bouncing in a box: positions and velocities, drawn as soft dots."""
    seqs = np.zeros((n_seq, T, size, size))
    yy, xx = np.mgrid[0:size, 0:size]
    for s in range(n_seq):
        p = g.uniform(3, size - 3, 2)
        v = g.uniform(-1.2, 1.2, 2)
        for t in range(T):
            seqs[s, t] = np.exp(-((xx - p[0]) ** 2 + (yy - p[1]) ** 2) / (2 * 1.2 ** 2))
            p = p + v
            for d in range(2):
                if p[d] < 1.5 or p[d] > size - 2.5:
                    v[d] = -v[d]
                    p[d] = np.clip(p[d], 1.5, size - 2.5)
    return seqs


def compute_world():
    torch = _torch()
    import torch.nn as nn

    torch.manual_seed(2018)  # Ha & Schmidhuber, World Models
    g = rng(2018)
    S = 16
    data = torch.tensor(frames(g, 600, 24), dtype=torch.float32)
    Z = 8
    enc = nn.Sequential(nn.Linear(S * S, 256), nn.ReLU(), nn.Linear(256, Z))
    dec = nn.Sequential(nn.Linear(Z, 256), nn.ReLU(), nn.Linear(256, S * S))
    dyn = nn.Sequential(nn.Linear(2 * Z, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, Z))
    params = [*enc.parameters(), *dec.parameters(), *dyn.parameters()]
    opt = torch.optim.Adam(params, lr=1e-3)
    flat = data.reshape(600, 24, -1)
    probe = torch.tensor(frames(rng(7), 50, 40), dtype=torch.float32).reshape(50, 40, -1)[:1]
    checks, snaps, losses = [0, 100, 300, 800, 2000, 5000], [], []

    def dream(n=12):  # how it learns: from the probe clip's first two frames, imagine the next n
        with torch.no_grad():
            z = enc(probe[:, :2])
            z1, z2, out_ = z[:, 0], z[:, 1], []
            for _ in range(n):
                z3 = z2 + dyn(torch.cat([z1, z2], -1))
                out_.append(torch.sigmoid(dec(z3))[0].numpy().reshape(S, S))
                z1, z2 = z2, z3
        return np.array(out_)

    for step in range(5000):
        if step in checks:
            snaps.append(dream())
        i = torch.randint(0, 600, (64,))
        x = flat[i]  # (64, 24, 256)
        z = enc(x)
        rec = torch.sigmoid(dec(z))
        # dynamics: from two frames' codes, predict the next code (two frames give the velocity)
        zin = torch.cat([z[:, :-2], z[:, 1:-1]], -1)
        zp = z[:, 1:-1] + dyn(zin)
        pred = torch.sigmoid(dec(zp))
        loss = ((rec - x) ** 2).mean() + ((pred - x[:, 2:]) ** 2).mean() + 0.1 * ((zp - z[:, 2:].detach()) ** 2).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 25 == 0:
            losses.append((step, float(loss)))
    snaps.append(dream())
    test = torch.tensor(frames(rng(7), 50, 40), dtype=torch.float32).reshape(50, 40, -1)
    with torch.no_grad():
        z = enc(test[:, :2])
        z1, z2 = z[:, 0], z[:, 1]
        imag = []
        for t in range(38):  # imagine: feed its own predictions back in
            z3 = z2 + dyn(torch.cat([z1, z2], -1))
            imag.append(torch.sigmoid(dec(z3)))
            z1, z2 = z2, z3
        imag = torch.stack(imag, 1)
        real = test[:, 2:]
        err = ((imag - real) ** 2).mean((0, 2)).numpy()

        def centre(fr):
            w = fr.reshape(-1, S, S).numpy()
            yy, xx = np.mgrid[0:S, 0:S]
            m = w.sum((1, 2)) + 1e-9
            return np.stack([(w * xx).sum((1, 2)) / m, (w * yy).sum((1, 2)) / m], 1)

        pos_err = np.array([np.linalg.norm(centre(imag[:, t]) - centre(real[:, t]), axis=1).mean() for t in range(38)])
    out = dict(S=S, Z=Z, real=real[0, :24].numpy().reshape(-1, S, S), imag=imag[0, :24].numpy().reshape(-1, S, S),
               err=err, pos_err=pos_err, first=test[0, :2].numpy().reshape(-1, S, S),
               checks=checks, dreams=np.array(snaps), losses=np.array(losses), probe_real=test[0, 2:14].numpy().reshape(-1, S, S))
    print(f"    position error after 1, 5, 20 imagined steps: {pos_err[0]:.2f}, {pos_err[4]:.2f}, {pos_err[19]:.2f} pixels",
          flush=True)
    assert pos_err[0] < 1.5 and pos_err[19] > pos_err[0]
    return out


# ---------------------------------------------------------------------------
# Dreamer-lite
# ---------------------------------------------------------------------------
DREAMER = dict(iters=60, steps_per_iter=40, seeds=(0, 1, 2), snap_iters=(0, 5, 20, 60), horizon=15, eval_eps=6)


def _jsonable(d):
    if isinstance(d, dict):
        return {k: _jsonable(v) for k, v in d.items()}
    if isinstance(d, np.ndarray):
        return d.tolist()
    if isinstance(d, (np.floating, np.integer)):
        return d.item()
    return d


def compute_dreamer():
    _torch()
    from .dreamer import train

    part = CACHE.partial("dreamer", DREAMER)
    for s in DREAMER["seeds"]:
        if str(s) in part:
            continue
        _log(f"    Dreamer-lite, seed {s}")
        r = train(s, iters=DREAMER["iters"], steps_per_iter=DREAMER["steps_per_iter"], H=DREAMER["horizon"],
                  eval_eps=DREAMER["eval_eps"], snap_iters=DREAMER["snap_iters"], log=_log)
        part[str(s)] = _jsonable(r)
    runs = [part[str(s)] for s in DREAMER["seeds"]]
    curves = np.array([r["curve"] for r in runs])  # (seeds, points, 3): iteration, env steps, catch rate
    out = dict(params=DREAMER, curves=curves, open_err=np.array([r["open_err"] for r in runs]),
               kl=np.array([r["kl"] for r in runs]), snaps=runs[0]["snaps"],
               final=curves[:, -1, 2], random_rate=float(np.mean(curves[:, 0, 2])))
    # the random policy's catch rate, measured: the paddle wanders, the ball lands anywhere
    from .envs import Catch

    g = rng(99)
    env, hits = Catch(rng(98)), []
    for _ in range(40):
        env.reset()
        done = False
        while not done:
            _, r, done = env.step(int(g.integers(3)))
            if r != 0:
                hits.append(r > 0)
    out["random_catch"] = float(np.mean(hits))
    return out


KLBAL = dict(iters=40, steps_per_iter=40, seeds=(0, 1, 2), configs={"balanced": (0.5, 0.1), "plain": (0.3, 0.3)})


def compute_klbal():
    _torch()
    from .dreamer import train

    part = CACHE.partial("klbal", KLBAL)
    for name, (kd, kr) in KLBAL["configs"].items():
        for s in KLBAL["seeds"]:
            key = f"{name}_{s}"
            if key in part:
                continue
            _log(f"    world model only, {name} KL, seed {s}")
            r = train(100 + s, iters=KLBAL["iters"], steps_per_iter=KLBAL["steps_per_iter"], kl_dyn=kd, kl_rep=kr,
                      train_policy=False, snap_iters=(), eval_every=10 ** 6, log=None)
            part[key] = _jsonable(dict(open_err=r["open_err"], kl=r["kl"]))
    out = dict(params=KLBAL)
    for name in KLBAL["configs"]:
        out[f"{name}_err"] = np.array([part[f"{name}_{s}"]["open_err"] for s in KLBAL["seeds"]])
        out[f"{name}_kl"] = np.array([part[f"{name}_{s}"]["kl"] for s in KLBAL["seeds"]])
    return out


# ---------------------------------------------------------------------------
def compute_symlog(seeds=3, steps=3000):
    torch = _torch()
    scales = [1.0, 10.0, 100.0, 1000.0]
    out = dict(scales=scales, steps=steps)
    xs = np.linspace(0, 1, 64)
    for mode in ("raw", "symlog"):
        errs, curves = [], []
        for s in range(seeds):
            torch.manual_seed(s)
            g = rng(s)
            phase = g.uniform(0, 2 * np.pi, len(scales))

            def batch(n):
                k = g.integers(len(scales), size=n)
                x = g.random(n)
                y = np.array(scales)[k] * (np.sin(6 * x + phase[k]) + 1.2)
                f = np.concatenate([np.eye(len(scales))[k], np.stack([np.sin(np.pi * j * x) for j in range(1, 7)] +
                                                                     [np.cos(np.pi * j * x) for j in range(0, 7)], 1)], 1)
                return torch.tensor(f, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

            net = torch.nn.Sequential(torch.nn.Linear(len(scales) + 13, 64), torch.nn.SiLU(), torch.nn.Linear(64, 64),
                                      torch.nn.SiLU(), torch.nn.Linear(64, 1))
            opt = torch.optim.Adam(net.parameters(), lr=1e-3)
            gt = rng(1000 + s)
            fx, fy = batch(2000)
            curve = []
            for it in range(steps + 1):
                if it % 100 == 0:
                    with torch.no_grad():
                        p = net(fx)[:, 0]
                        p = torch.sign(p) * (torch.exp(p.abs()) - 1) if mode == "symlog" else p
                        rel = []
                        kk = fx[:, :len(scales)].argmax(1)
                        for j in range(len(scales)):
                            m = kk == j
                            rel.append(float(((p[m] - fy[m]).abs() / fy[m].abs()).mean()))
                    curve.append([it] + rel)
                if it == steps:
                    break
                f, y = batch(256)
                p = net(f)[:, 0]
                tgt = torch.sign(y) * torch.log1p(y.abs()) if mode == "symlog" else y
                loss = ((p - tgt) ** 2).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
            curves.append(curve)
            errs.append(curve[-1][1:])
            del gt
        out[f"{mode}_err"] = np.array(errs)  # (seeds, games): mean relative error at the end
        out[f"{mode}_curves"] = np.array(curves)
    out["xs"] = xs
    return out


# ---------------------------------------------------------------------------
# Regression against flow matching, on demonstrations with two ways round
# ---------------------------------------------------------------------------
DETOUR = dict(demos=400, chunk=20, steps=6000, seeds=5, snaps=(0, 300, 1500, 6000), flow_steps=10)


def detour_rollout(policy, starts, chunk, max_steps=60):
    """Closed loop: plan a chunk of ``chunk`` moves, carry them out, look again.  Returns paths and outcomes."""
    from .envs import GOAL, OBST

    paths, hit, reached = [], [], []
    for y0 in starts:
        p = np.array([-1.0, float(y0)])
        path = [p.copy()]
        h, r = False, False
        while len(path) <= max_steps and not (h or r):
            moves = policy(p)
            for m in moves.reshape(chunk, 2):
                p = p + m
                path.append(p.copy())
                if np.hypot(p[0] - OBST[0], p[1] - OBST[1]) < OBST[2]:
                    h = True
                    break
                if np.hypot(p[0] - GOAL[0], p[1] - GOAL[1]) < 0.15:
                    r = True
                    break
        paths.append(np.array(path))
        hit.append(h)
        reached.append(r)
    return paths, np.array(hit), np.array(reached)


def offsets_to_moves(off):
    """A chunk of positions relative to the current one, (2H,), as the H moves that reach them, (2H,)."""
    o = off.reshape(-1, 2)
    return np.diff(np.concatenate([np.zeros((1, 2)), o]), axis=0).reshape(-1)


def compute_detour():
    torch = _torch()
    from .envs import detour_demo

    P = DETOUR
    H = P["chunk"]
    g = rng(2024)  # Black et al., pi0 (2024)
    demos = [detour_demo(g) for _ in range(P["demos"])]
    X, Y = [], []
    for d in demos:
        # the chunk: the next H positions relative to the current one (so sampling noise does not accumulate)
        dd = np.concatenate([d, np.repeat(d[-1:], H, 0)])
        for t in range(len(d) - 1):
            X.append(d[t])
            Y.append((dd[t + 1:t + H + 1] - d[t]).reshape(-1))
    X, Y = torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(np.array(Y), dtype=torch.float32)
    sc = float(Y.abs().max())
    Yn = Y / sc
    out = dict(params=P, demos=np.array(demos[:40]), scale=sc)
    starts = rng(5).uniform(-0.25, 0.25, 60)
    out["n_starts"] = len(starts)
    show = np.linspace(-0.22, 0.22, 12)

    def net(i, o):
        return torch.nn.Sequential(torch.nn.Linear(i, 256), torch.nn.SiLU(), torch.nn.Linear(256, 256), torch.nn.SiLU(),
                                   torch.nn.Linear(256, o))

    for method in ("regress", "flow"):
        res = []
        for s in range(P["seeds"]):
            torch.manual_seed(s)
            gb = torch.Generator().manual_seed(s)
            f = net(2 + (2 * H + 1 if method == "flow" else 0), 2 * H)
            opt = torch.optim.Adam(f.parameters(), lr=1e-3)
            snaps = {}
            gs = torch.Generator().manual_seed(1000 + s)

            def policy(pos, f=f, gs=gs):
                with torch.no_grad():
                    o = torch.tensor(pos, dtype=torch.float32)[None]
                    if method == "regress":
                        return offsets_to_moves((f(o)[0] * sc).numpy())
                    a = torch.randn(1, 2 * H, generator=gs)  # noise at tau = 0, the chunk at tau = 1
                    n = P["flow_steps"]
                    for k in range(n):
                        tau = torch.full((1, 1), k / n)
                        a = a + f(torch.cat([o, a, tau], -1)) / n  # Euler steps along the learned velocity
                    return offsets_to_moves((a[0] * sc).numpy())

            for it in range(P["steps"] + 1):
                if it in P["snaps"]:
                    paths, hit, reached = detour_rollout(policy, show, H)
                    snaps[str(it)] = dict(paths=[p_.tolist() for p_ in paths], hit=hit.tolist(), reached=reached.tolist())
                if it == P["steps"]:
                    break
                i = torch.randint(0, len(X), (256,), generator=gb)
                o, a = X[i], Yn[i]
                if method == "regress":
                    loss = ((f(o) - a) ** 2).mean()
                else:
                    eps = torch.randn(a.shape, generator=gb)
                    tau = torch.rand(len(a), 1, generator=gb)
                    at = (1 - tau) * eps + tau * a
                    loss = ((f(torch.cat([o, at, tau], -1)) - (a - eps)) ** 2).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
            paths, hit, reached = detour_rollout(policy, starts, H)
            # which way round: the side of the obstacle where the path crosses its centre line
            side = np.array([p_[np.argmin(np.abs(p_[:, 0] - 0.0)), 1] for p_ in paths])
            above, below = (side > 0).astype(float), (side <= 0).astype(float)
            res.append(dict(hit=float(hit.mean()), reached=float(reached.mean()), above=float(above.mean()),
                            below=float(below.mean()), snaps=snaps))
        out[f"{method}_hit"] = np.array([r["hit"] for r in res])
        out[f"{method}_reached"] = np.array([r["reached"] for r in res])
        out[f"{method}_above"] = np.array([r["above"] for r in res])
        out[f"{method}_below"] = np.array([r["below"] for r in res])
        out[f"{method}_snaps"] = res[0]["snaps"]
    return out


# ---------------------------------------------------------------------------
# FAST: frequency-space action tokens
# ---------------------------------------------------------------------------
def bpe_train(seqs, merges):
    """Byte-pair encoding on sequences of symbols (tuples): the ``merges`` most frequent adjacent pairs, in order."""
    seqs = [list(s) for s in seqs]
    rules = []
    for _ in range(merges):
        cnt = Counter()
        for s in seqs:
            cnt.update(zip(s, s[1:]))
        if not cnt:
            break
        (a, b), c = cnt.most_common(1)[0]
        if c < 2:
            break
        new = (a, b)
        rules.append(new)
        for k, s in enumerate(seqs):
            i, o = 0, []
            while i < len(s):
                if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                    o.append(new)
                    i += 2
                else:
                    o.append(s[i])
                    i += 1
            seqs[k] = o
    return rules


def bpe_encode(s, rules):
    s = list(s)
    for a, b in rules:
        i, o = 0, []
        while i < len(s):
            if i + 1 < len(s) and s[i] == a and s[i + 1] == b:
                o.append((a, b))
                i += 2
            else:
                o.append(s[i])
                i += 1
        s = o
    return s


FAST = dict(n_train=600, n_test=300, gammas=(2, 5, 10, 20, 50, 100), merges=600, bins=256, show_gamma=10)


def compute_fast():
    from scipy.fft import dct, idct

    from .envs import arm_chunks

    P = FAST
    g = rng(2025)  # Pertsch et al., FAST (2025)
    ch = arm_chunks(P["n_train"] + P["n_test"], g)  # (n, 50, 7) radians
    n, H, J = ch.shape
    lo, hi = np.quantile(ch[:P["n_train"]], 0.01, axis=(0, 1)), np.quantile(ch[:P["n_train"]], 0.99, axis=(0, 1))
    norm = lambda a: 2 * (a - lo) / (hi - lo) - 1  # noqa: E731  (FAST: the 1st and 99th percentiles to [-1, 1])
    unnorm = lambda a: (a + 1) / 2 * (hi - lo) + lo  # noqa: E731
    tr, te = ch[:P["n_train"]], ch[P["n_train"]:]
    out = dict(params=P, H=H, J=J, example=te[0], lo=lo, hi=hi)
    # per-step binning: every joint, every step, one of 256 bins over its range (RT-2, OpenVLA)
    edges = np.linspace(-1, 1, P["bins"] + 1)
    centres = (edges[:-1] + edges[1:]) / 2
    q = np.clip(np.digitize(norm(te), edges) - 1, 0, P["bins"] - 1)
    rec = unnorm(centres[q])
    out["bin_tokens"] = H * J
    out["bin_rmse"] = float(np.sqrt(((rec - te) ** 2).mean()))
    qtr = np.clip(np.digitize(norm(tr), edges) - 1, 0, P["bins"] - 1)
    out["bin_repeat"] = float((qtr[:, 1:] == qtr[:, :-1]).mean())  # how often a token just repeats the last one
    out["bin_near"] = float((np.abs(qtr[:, 1:] - qtr[:, :-1]) <= 1).mean())

    def fast_ints(a, gam):
        c = dct(norm(a), axis=1, norm="ortho")  # (n, H, J): along time, for each joint
        return np.round(gam * c).astype(int)

    def flat(qc):  # low frequencies first: every joint's first coefficient, then every joint's second, ...
        return [tuple(r) for r in qc.reshape(len(qc), -1)]

    rows = []
    for gam in P["gammas"]:
        qtr_, qte = fast_ints(tr, gam), fast_ints(te, gam)
        rules = bpe_train([[int(v) for v in s] for s in flat(qtr_)], P["merges"])
        toks = [len(bpe_encode([int(v) for v in s], rules)) for s in flat(qte)]
        rec = unnorm(idct(qte / gam, axis=1, norm="ortho"))
        rows.append(dict(gamma=gam, nonzero=float((qte != 0).sum((1, 2)).mean()), tokens=float(np.mean(toks)),
                         rmse=float(np.sqrt(((rec - te) ** 2).mean())), vocab=len(set(np.unique(qtr_))) + len(rules)))
        _log(f"    FAST gamma {gam}: {rows[-1]['tokens']:.1f} tokens a chunk, rmse {rows[-1]['rmse']:.4f}")
    out["rows"] = rows
    # the example chunk's first joint: its coefficients and its rebuilt motion at the shown gamma
    gam = P["show_gamma"]
    c = dct(norm(te[:1]), axis=1, norm="ortho")[0, :, 0]
    out["ex_coef"] = c
    out["ex_q"] = np.round(gam * c)
    out["ex_rec"] = unnorm(idct(np.round(gam * dct(norm(te[:1]), axis=1, norm="ortho")) / gam, axis=1, norm="ortho"))[0]
    # the energy in each frequency, averaged over chunks and joints: smooth motion lives in the first few
    cc = dct(norm(tr), axis=1, norm="ortho")
    en = (cc ** 2).mean((0, 2))
    out["energy"] = en / en.sum()
    return out


# ---------------------------------------------------------------------------
# Domain randomization on the cart-pole
# ---------------------------------------------------------------------------
RAND = dict(iters=30, pop=48, elite=8, episodes=6, seeds=8, eval_eps=40,
            ranges=dict(l=(0.25, 1.0), mp=(0.05, 0.4), mc=(0.5, 2.0), F=(6.0, 14.0), delay=0.5, noise=(0.0, 1.0)),
            real=dict(l=0.85, mp=0.3, mc=1.6, F=7.0, delay=1, noise=0.7),
            grid_l=(0.2, 1.2), grid_F=(4.0, 15.0), grid_n=11)


def _fixed(par):
    def phys(n, g):
        return {k: np.full(n, v) for k, v in par.items()}

    return phys


def _randomized(n, g):
    R = RAND["ranges"]
    return dict(l=g.uniform(*R["l"], n), mp=g.uniform(*R["mp"], n), mc=g.uniform(*R["mc"], n), F=g.uniform(*R["F"], n),
                delay=(g.random(n) < R["delay"]).astype(int), noise=g.uniform(*R["noise"], n))


def compute_randomize():
    from .envs import NOMINAL, cartpole_returns

    P = RAND
    nominal, real = _fixed(NOMINAL), _fixed(P["real"])
    out = dict(params=P, nominal=NOMINAL)
    for method, phys in (("nominal", nominal), ("randomized", _randomized)):
        Ws, hist = [], []
        for s in range(P["seeds"]):
            g = rng(2017 + s)  # Tobin et al., domain randomization (2017)
            mu, sd = np.zeros(5), np.ones(5)
            h = []
            for it in range(P["iters"]):
                W = mu + sd * g.standard_normal((P["pop"], 5))
                R = cartpole_returns(W, phys, P["episodes"], g)
                el = W[np.argsort(-R)[:P["elite"]]]
                mu, sd = el.mean(0), el.std(0) + 0.02
                ge = rng(10_000 + it)
                h.append((it, float(R.mean()), float(cartpole_returns(mu[None], nominal, P["eval_eps"], ge)[0]),
                          float(cartpole_returns(mu[None], real, P["eval_eps"], ge)[0])))
            Ws.append(mu)
            hist.append(h)
        out[f"{method}_W"] = np.array(Ws)
        out[f"{method}_hist"] = np.array(hist)  # (seeds, iters, 4): iteration, training return, nominal, real
        ge = rng(77)
        out[f"{method}_nominal"] = np.array([cartpole_returns(w[None], nominal, 100, ge)[0] for w in Ws])
        out[f"{method}_real"] = np.array([cartpole_returns(w[None], real, 100, ge)[0] for w in Ws])
        # robustness map: pole length against motor force, with the real robot's delay and sensor noise
        Ls = np.linspace(*P["grid_l"], P["grid_n"])
        Fs = np.linspace(*P["grid_F"], P["grid_n"])
        maps = []
        for w in Ws:
            m = np.zeros((len(Ls), len(Fs)))
            for i, l_ in enumerate(Ls):
                par = dict(P["real"], l=float(l_))
                for j, f_ in enumerate(Fs):
                    par["F"] = float(f_)
                    m[i, j] = cartpole_returns(w[None], _fixed(par), 12, rng(500 + 31 * i + j))[0]
            maps.append(m)
        out[f"{method}_map"] = np.array(maps)
        _log(f"    {method}: nominal {out[f'{method}_nominal'].mean():.0f}, real {out[f'{method}_real'].mean():.0f}")
    # one episode on the "real" cart-pole for each method's seed-0 policy, for the picture
    from .envs import cartpole_trace

    for method in ("nominal", "randomized"):
        out[f"{method}_trace"] = cartpole_trace(out[f"{method}_W"][0], P["real"], rng(4))
    out["grid_l"] = np.linspace(*P["grid_l"], P["grid_n"])
    out["grid_F"] = np.linspace(*P["grid_F"], P["grid_n"])
    return out


ITEMS = {
    "belief": compute_belief,
    "horizon": compute_horizon,
    "agent": compute_agent,
    "metr": compute_metr,
    "lane": compute_lane,
    "world": compute_world,
    "symlog": compute_symlog,
    "detour": compute_detour,
    "fast": compute_fast,
    "randomize": compute_randomize,
    "dreamer": compute_dreamer,
    "klbal": compute_klbal,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
