"""Control loops in the cloud (Part 45): a reconciler that drives actual state to desired state, level-triggered
against edge-triggered when events are lost; an autoscaler as a proportional controller with a delay; Erlang C for
the servers a queue needs; and an infrastructure plan as a diff applied in dependency order."""

from __future__ import annotations

import random


# ---------------------------------------------------------------- reconciliation

def reconcile(desired=5, steps=40, crash_at=(12, 25), lose_events=0.3, seed=0):
    """A deployment wants `desired` replicas.  Pods crash at the given steps.  An edge-triggered controller reacts
    only to 'pod died' events, some of which are lost; a level-triggered one compares desired with observed state
    every step and fixes the difference.  Returns both replica counts over time."""
    rng = random.Random(seed)
    out = {}
    for mode in ("edge", "level"):
        rng.seed(seed)
        running = 0
        series = []
        pending_events = []
        for t in range(steps):
            if t in crash_at:
                dead = min(running, 2)
                running -= dead
                pending_events += ["died"] * dead
            if mode == "level":
                diff = desired - running
                running += max(-1, min(1, diff))             # at most one start per step
            else:
                if t == 0:
                    running = desired
                delivered = [e for e in pending_events if rng.random() >= lose_events]
                running += len(delivered)
                pending_events = []
            series.append(running)
        out[mode] = series
    return {"desired": desired, "crash_at": list(crash_at), "series": out}


# ---------------------------------------------------------------- autoscaling

def autoscale(gain=0.5, delay=3, steps=80, target=0.6, seed=1, spike_at=10, base=40.0, spike=100.0):
    """Load (requests/s) jumps from base to spike at spike_at.  Each server handles 10 requests/s at 100%.  Every
    step the controller sets servers += gain * (utilization/target - 1) * servers, from a measurement `delay` steps
    old; new servers take a step to start."""
    rng = random.Random(seed)
    servers = base / 10 / target
    hist_util = []
    series = []
    for t in range(steps):
        load = (spike if t >= spike_at else base) * (1 + rng.gauss(0, 0.02))
        util = load / (10 * servers)
        hist_util.append(util)
        seen = hist_util[max(0, t - delay)]
        servers = min(200.0, max(1.0, servers + gain * (seen / target - 1) * servers))   # quota: 200
        series.append({"t": t, "load": load, "servers": servers, "util": util})
    tail = [s["servers"] for s in series[-20:]]
    return {"gain": gain, "delay": delay, "series": series, "settled": max(tail) - min(tail) < 0.05 * sum(tail) / 20,
            "peak_servers": max(s["servers"] for s in series), "final_servers": series[-1]["servers"],
            "ideal": spike / 10 / target}


def erlang_c(c: int, a: float) -> float:
    """Probability that an arriving request waits, with c servers and offered load a = lambda/mu erlangs."""
    if a >= c:
        return 1.0
    b = 1.0                                   # Erlang B by its stable recursion
    for k in range(1, c + 1):
        b = a * b / (k + a * b)
    return c * b / (c - a * (1 - b))


def servers_for(lam, mu, wait_target, p_target=0.2):
    """Fewest servers so that the mean wait is under wait_target, and the share waiting at all under p_target."""
    a = lam / mu
    c = max(1, int(a) + 1)
    while True:
        pw = erlang_c(c, a)
        w = pw / (c * mu - lam)
        if w <= wait_target and pw <= p_target:
            return {"servers": c, "load": a, "p_wait": pw, "mean_wait": w, "utilization": a / c}
        c += 1


def erlang_table():
    rows = []
    for lam in (10, 50, 100, 500, 1000):
        rows.append({"rate": lam, **servers_for(lam, 1.0, 0.05)})
    return rows


# ---------------------------------------------------------------- infrastructure as code

def plan(desired: dict, actual: dict):
    """Resources as name -> (kind, properties, dependencies).  The plan creates what is missing, updates what
    differs and destroys what is no longer wanted; creates and updates run in dependency order, destroys in
    reverse."""
    create = [n for n in desired if n not in actual]
    update = [n for n in desired if n in actual and desired[n][:2] != actual[n][:2]]
    destroy = [n for n in actual if n not in desired]
    def dependency_order(graph):
        order, seen, active = [], set(), set()

        def visit(n):
            if n in active:
                raise ValueError("resource dependencies contain a cycle")
            if n in seen:
                return
            active.add(n)
            for d in graph[n][2]:
                if d in graph:
                    visit(d)
            active.remove(n)
            seen.add(n)
            order.append(n)
        for n in graph:
            visit(n)
        return order

    order = dependency_order(desired)
    apply = [("create" if n in create else "update", n) for n in order if n in create or n in update]
    rev = [("destroy", n) for n in reversed(dependency_order(actual)) if n in destroy]
    return {"create": create, "update": update, "destroy": destroy, "steps": apply + rev}


def plan_example():
    actual = {"vpc": ("network", {"cidr": "10.0.0.0/16"}, []),
              "subnet": ("subnet", {"cidr": "10.0.1.0/24"}, ["vpc"]),
              "db": ("database", {"size": "small"}, ["subnet"]),
              "old-cache": ("cache", {"nodes": 2}, ["subnet"])}
    desired = {"vpc": ("network", {"cidr": "10.0.0.0/16"}, []),
               "subnet": ("subnet", {"cidr": "10.0.1.0/24"}, ["vpc"]),
               "db": ("database", {"size": "large"}, ["subnet"]),
               "queue": ("queue", {"fifo": True}, []),
               "service": ("container service", {"replicas": 4}, ["subnet", "db", "queue"])}
    return {"actual": {k: v[0] for k, v in actual.items()}, "desired": {k: v[0] for k, v in desired.items()},
            **plan(desired, actual)}
