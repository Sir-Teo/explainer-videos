"""Real-time scheduling (Part 31, chapter 11): periodic tasks with implicit deadlines.

    ll_bound(n)                        Liu and Layland (1973): RMS meets every deadline if U <= n (2^(1/n) - 1)
    rta(tasks)                         the exact test for fixed priorities (Joseph and Pandya, 1986): worst-case
                                       response times R_i = C_i + sum_{j < i} ceil(R_i / T_j) C_j
    uunifast(n, U, rng)                random task utilizations summing to U (Bini and Buttazzo, 2005)
    schedule(tasks, policy, horizon)   the timeline under "rms" or "edf", and any missed deadlines
    pathfinder(inherit)                the 1997 priority inversion, as a three-task timeline

A task is (C, T): C ticks of work released every T ticks, due by the next release.
"""
from __future__ import annotations

import math
import random


def ll_bound(n: int) -> float:
    return n * (2 ** (1 / n) - 1)


def rta(tasks: list[tuple[int, int]]) -> list[float | None]:
    """Worst-case response time of each task under rate-monotonic priorities (shorter period first); None if it
    can exceed its period."""
    ts = sorted(tasks, key=lambda x: x[1])
    out = []
    for i, (C, T) in enumerate(ts):
        R = C
        while True:
            nr = C + sum(math.ceil(R / Tj) * Cj for Cj, Tj in ts[:i])
            if nr > T:
                out.append(None)
                break
            if nr == R:
                out.append(R)
                break
            R = nr
    return out


def uunifast(n: int, U: float, rng: random.Random) -> list[float]:
    us, s = [], U
    for i in range(1, n):
        nxt = s * rng.random() ** (1 / (n - i))
        us.append(s - nxt)
        s = nxt
    us.append(s)
    return us


def schedule(tasks: list[tuple[int, int]], policy: str = "rms", horizon: int | None = None) -> dict:
    """Tick-by-tick: each tick runs the released job with the highest priority (RMS: shortest period; EDF: earliest
    absolute deadline).  Returns the segments (start, end, task index), and the misses (task, deadline)."""
    H = horizon or math.lcm(*[T for _, T in tasks])
    jobs = []               # [task, remaining, deadline, release]
    seg, miss = [], []
    for t in range(H):
        for i, (C, T) in enumerate(tasks):
            if t % T == 0:
                jobs.append([i, C, t + T, t])
        for j in [j for j in jobs if j[2] <= t and j[1] > 0]:
            miss.append((j[0], j[2]))
            jobs.remove(j)
        live = [j for j in jobs if j[1] > 0]
        if live:
            if policy == "rms":
                j = min(live, key=lambda j: (tasks[j[0]][1], j[0]))
            else:
                j = min(live, key=lambda j: (j[2], j[0]))
            j[1] -= 1
            if seg and seg[-1][2] == j[0] and seg[-1][1] == t:
                seg[-1] = (seg[-1][0], t + 1, j[0])
            else:
                seg.append((t, t + 1, j[0]))
        jobs = [j for j in jobs if j[1] > 0]
    return {"segments": seg, "misses": miss, "horizon": H, "U": sum(C / T for C, T in tasks)}


def pathfinder(inherit: bool, horizon: int = 60) -> dict:
    """Mars Pathfinder, 1997, simplified: a low-priority meteorological task takes the information-bus mutex; the
    high-priority bus-management task arrives and waits for it; a medium-priority communications task, which needs
    no mutex, preempts the low task, so the high one waits behind a task of lower priority than itself.  A watchdog
    resets the system if the bus task has not finished by its deadline.  With priority inheritance, the low task
    runs at the high task's priority while it holds the mutex.

    Tasks: (name, priority, release, plan), where plan is a list of ("run", n) and ("lock"/"unlock",)."""
    tasks = [
        {"name": "meteo", "prio": 1, "release": 0, "plan": [("run", 2), ("lock",), ("run", 6), ("unlock",),
                                                            ("run", 2)]},
        {"name": "bus", "prio": 3, "release": 5, "plan": [("run", 1), ("lock",), ("run", 3), ("unlock",), ("run", 1)],
         "deadline": 25},
        {"name": "comms", "prio": 2, "release": 7, "plan": [("run", 30)]},
    ]
    for t in tasks:
        t["pc"], t["left"], t["done"] = 0, None, None
    owner = None
    seg = []
    blocked_at = None
    for now in range(horizon):
        ready = []
        for t in tasks:
            if t["release"] > now or t["done"] is not None:
                continue
            # execute zero-time steps
            while t["pc"] < len(t["plan"]) and t["plan"][t["pc"]][0] in ("lock", "unlock"):
                op = t["plan"][t["pc"]][0]
                if op == "lock":
                    if owner is None:
                        owner = t["name"]
                        t["pc"] += 1
                    elif owner != t["name"]:
                        break
                else:
                    owner = None
                    t["pc"] += 1
            if t["pc"] >= len(t["plan"]):
                t["done"] = now
                continue
            if t["plan"][t["pc"]][0] == "lock":
                if t["name"] == "bus" and blocked_at is None:
                    blocked_at = now
                continue        # waiting for the mutex
            ready.append(t)
        if not ready:
            continue

        def eff(t):
            p = t["prio"]
            if inherit and owner == t["name"]:
                waiting = [u["prio"] for u in tasks if u is not t and u["done"] is None and u["release"] <= now
                           and u["pc"] < len(u["plan"]) and u["plan"][u["pc"]][0] == "lock"]
                p = max([p] + waiting)
            return p
        run = max(ready, key=eff)
        if run["left"] is None:
            run["left"] = run["plan"][run["pc"]][1]
        run["left"] -= 1
        if seg and seg[-1][2] == run["name"] and seg[-1][1] == now:
            seg[-1] = (seg[-1][0], now + 1, run["name"])
        else:
            seg.append((now, now + 1, run["name"]))
        if run["left"] == 0:
            run["left"] = None
            run["pc"] += 1
            if run["pc"] >= len(run["plan"]):
                run["done"] = now + 1
    bus = next(t for t in tasks if t["name"] == "bus")
    return {"segments": seg, "bus_done": bus["done"], "deadline": bus["deadline"], "blocked_at": blocked_at,
            "reset": bus["done"] is None or bus["done"] > bus["deadline"]}
