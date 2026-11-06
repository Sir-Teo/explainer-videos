"""Process instruments for Part 40: Brooks' law as a simulation, Monte Carlo schedules with heavy-tailed tasks,
and work in progress as a queue (Little's law)."""

from __future__ import annotations

import math
import random

import numpy as np


# ---------------------------------------------------------------- Brooks' law

def brooks(work: float = 120.0, team: int = 6, add_at: float | None = None, add: int = 0, ramp: float = 6.0,
           mentor: float = 0.5, channel_cost: float = 0.02, dt: float = 0.05):
    """A project of ``work`` person-months.  Each person's output is 1 per month less ``channel_cost`` for each other
    person they must coordinate with (the n(n - 1)/2 channels, shared out).  Newcomers produce nothing at first and
    reach full speed linearly over ``ramp`` months; while ramping, each takes ``mentor`` of an experienced
    person's time.  Returns the finishing month."""
    t, done = 0.0, 0.0
    hires: list = []
    while done < work and t < 600:
        if add_at is not None and add and t >= add_at and not hires:
            hires = [t] * add
        n = team + len(hires)
        eff_each = max(0.0, 1.0 - channel_cost * (n - 1))
        out = team * eff_each
        for h in hires:
            frac = min(1.0, (t - h) / ramp) if ramp else 1.0
            out += eff_each * frac
            if frac < 1.0:
                out -= mentor * eff_each
        done += max(0.0, out) * dt
        t += dt
    return t


def brooks_table(work: float = 120.0, team: int = 6, add: int = 4):
    """Finishing month when ``add`` people join at month m, for a range of m; and the finishing month for teams of
    different sizes from the start."""
    base = brooks(work, team)
    late = [{"add_at": m, "finish": brooks(work, team, add_at=m, add=add)} for m in (2, 6, 10, 14, 16, 18, 20)]
    early = [{"team": n, "finish": brooks(work, n)} for n in (2, 4, 6, 8, 12, 16, 24, 32, 40)]
    return {"base": base, "late": late, "from_start": early, "work": work, "team": team, "add": add, "ramp": 6.0,
            "plan": work / team}


# ---------------------------------------------------------------- estimation

def schedule(tasks: int = 20, median: float = 5.0, sigma: float = 0.6, parallel: int = 1, trials: int = 100_000,
             seed: int = 0):
    """``tasks`` tasks with lognormal durations (median ``median`` days), done in ``parallel`` equal streams that
    must all finish.  The plan adds up medians; returns the plan, P50, P80, P95 and the chance of meeting the
    plan."""
    rng = np.random.default_rng(seed)
    d = median * np.exp(rng.normal(0, sigma, size=(trials, tasks)))
    per = tasks // parallel
    streams = d[:, :per * parallel].reshape(trials, parallel, per).sum(axis=2)
    total = streams.max(axis=1)
    plan = median * per
    q = np.percentile(total, [50, 80, 95])
    return {"tasks": tasks, "parallel": parallel, "plan": plan, "p50": float(q[0]), "p80": float(q[1]),
            "p95": float(q[2]), "on_time": float((total <= plan).mean()), "mean_task": float(d.mean()),
            "sigma": sigma}


def estimation_table():
    rows = [schedule(sigma=s) for s in (0.3, 0.6, 1.0)]
    par = [schedule(sigma=0.6, parallel=p) for p in (1, 2, 4)]
    return {"serial": rows, "parallel": par}


# ---------------------------------------------------------------- work in progress

def kanban(wip_limit: int | None, workers: int = 4, arrivals_per_day: float = 0.8, days: int = 4000,
           switch_cost: float = 0.05, seed: int = 0):
    """Items arrive at random and are worked on by ``workers`` people.  Without a limit, everything started is in
    progress at once and each person splits their time across their items, paying ``switch_cost`` of a day per
    extra item they juggle; with a limit, new items wait in a backlog until a slot frees.  Each item needs an
    exponential amount of work (mean 4 person-days).  Returns throughput, mean items in progress (L), mean lead
    time from start (W) and Little's L / throughput."""
    rng = random.Random(seed)
    backlog = []
    active = []           # [remaining work, start day]
    done = []
    L_sum = 0.0
    for day in range(days):
        k = np.random.default_rng(seed + day).poisson(arrivals_per_day)
        for _ in range(int(k)):
            backlog.append(day)
        while backlog and (wip_limit is None or len(active) < wip_limit):
            arrived = backlog.pop(0)
            active.append([rng.expovariate(1 / 4.0), day, arrived])
        L_sum += len(active)
        if active:
            per_person = len(active) / workers
            eff = max(0.1, 1.0 - switch_cost * max(0.0, per_person - 1))
            share = workers * eff / len(active)
            for a in active:
                a[0] -= share
            fin = [a for a in active if a[0] <= 0]
            for a in fin:
                done.append((day + 1 - a[1], day + 1 - a[2]))
                active.remove(a)
    warm = len(done) // 5
    cycle = float(np.mean([c for c, _ in done[warm:]])) if done else float("nan")
    lead = float(np.mean([w for _, w in done[warm:]])) if done else float("nan")
    thr = len(done) / days
    L = L_sum / days
    return {"wip_limit": wip_limit, "throughput": thr, "wip": L, "cycle_time": cycle, "lead_time": lead,
            "little": L / thr if thr else None,
            "backlog_end": len(backlog)}


def channels(n: int) -> int:
    return n * (n - 1) // 2


def kanban_table():
    return [kanban(w) for w in (None, 16, 8, 6, 4)]


_ = math


# ---------------------------------------------------------------- technical debt, as a model

def debt(weeks: int = 104, refactor: float = 0.0, growth: float = 0.03, payoff: float = 2.0, base: float = 10.0):
    """A team ships ``base`` points a week when the code is clean.  Every point shipped without care adds
    ``growth`` units of debt; each unit of debt slows all work by a factor 1 / (1 + debt / 100) (interest).  A
    fraction ``refactor`` of the time goes to paying debt back, ``payoff`` units per unit of time.  Returns
    cumulative features delivered and the debt over time.  This is a model of Cunningham's metaphor, not data."""
    d, total = 0.0, 0.0
    out = []
    for w in range(weeks):
        speed = base / (1 + d / 100.0)
        feat = speed * (1 - refactor)
        total += feat
        d = max(0.0, d + growth * feat * 10 - payoff * refactor * 10)
        out.append({"week": w + 1, "delivered": total, "debt": d, "speed": speed})
    return out


def debt_table():
    return {str(r): debt(refactor=r) for r in (0.0, 0.1, 0.2, 0.3)}


# ---------------------------------------------------------------- integration frequency

def merge_conflicts(devs: int = 10, files: int = 400, edits_per_day: float = 6.0, days: int = 120,
                    intervals_h=(1, 4, 24, 72, 168, 336), zipf_s: float = 1.0, regions: int = 25, seed: int = 0):
    """``devs`` people edit files (popularity Zipf(s): some files are hot) at ``edits_per_day`` each, on branches
    they merge back every ``interval`` hours.  Each edit changes one of ``regions`` regions of its file.  A merge
    conflicts if another branch merged since this one was started changed one of the same regions.  Returns the share of merges that conflict and the mean files in
    conflict, against the interval."""
    rng = np.random.default_rng(seed)
    w = 1.0 / np.arange(1, files + 1) ** zipf_s
    w /= w.sum()
    out = []
    for iv in intervals_h:
        hours = days * 24
        log = []                 # (merge time, set of files)
        merges = conflicts = 0
        nfiles = 0
        starts = rng.uniform(0, iv, size=devs)
        for d in range(devs):
            t = starts[d]
            while t < hours:
                end = t + iv
                k = rng.poisson(edits_per_day * iv / 24.0)
                touched = set(zip(rng.choice(files, size=k, p=w).tolist(),
                                  rng.integers(0, regions, size=k).tolist())) if k else set()
                log.append((end, t, touched, d))
                t = end
        log.sort()
        merged: list = []
        for end, start, touched, d in log:
            if not touched:
                continue
            merges += 1
            clash = set()
            for mt, mf, md in reversed(merged):
                if mt <= start:
                    break
                if md != d:
                    clash |= (mf & touched)
            if clash:
                conflicts += 1
                nfiles += len(clash)
            merged.append((end, touched, d))
        out.append({"interval_h": iv, "merges": merges, "conflict_share": conflicts / merges if merges else 0.0,
                    "hunks_per_conflict": nfiles / conflicts if conflicts else 0.0,
                    "hunks_per_merge": nfiles / merges if merges else 0.0})
    return {"rows": out, "devs": devs, "files": files, "edits_per_day": edits_per_day}
