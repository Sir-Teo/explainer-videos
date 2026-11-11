"""CPU schedulers, simulated tick by tick (Part 31, chapters 7-10).

    jobs = [Job("A", 0, [100]), Job("B", 1, [10]), Job("C", 2, [10])]
    r = simulate(jobs, "fcfs")                      # or sjf, srtf, rr, mlfq, lottery, stride, cfs
    r.segments          # [(start, end, name)]: the Gantt chart
    r.metrics()         # per job: turnaround, response, waiting; and their means

A job is a list of bursts that alternate CPU and I/O, starting with CPU: ``[5, 20, 5]`` computes for 5 ticks,
waits 20 for its disk, computes 5 more.  Time is in ticks; one tick of CPU goes to one job (or to nobody).  A
``switch`` cost, in ticks, is charged whenever the CPU moves to a different job (drawn as ``"switch"``).

Policies, with their parameters:

* ``fcfs`` first come, first served; ``sjf`` shortest (next CPU burst) first; neither preempts.
* ``srtf`` shortest remaining time first: preempts whenever a shorter burst arrives.
* ``rr`` round robin with ``quantum``.
* ``mlfq``: Corbato's multi-level feedback queue as OSTEP states it: ``levels`` queues with ``quanta``; a job's
  ``allotment`` at a level used up moves it down; ``boost`` ticks put every job back at the top.  ``rule4a`` (the
  old rule) resets the allotment whenever a job gives up the CPU, which a job can game.
* ``lottery`` (Waldspurger and Weihl, 1994): each quantum goes to a random ticket; ``stride`` (1995): to the job with
  the smallest pass, which then advances by L / tickets.
* ``cfs`` (Linux 2007): the job with the least virtual runtime runs; vruntime grows by dt * 1024 / weight, the
  weight set by ``nice`` (1.25x per level); the slice is ``latency`` shared in proportion to weight, at least
  ``granularity``.  A job that wakes starts no lower than the smallest vruntime, less half a latency.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

# Linux's sched_prio_to_weight table (kernel/sched/core.c): nice -20 .. 19
NICE_WEIGHT = [88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916, 9548, 7620, 6100, 4904, 3906,
               3121, 2501, 1991, 1586, 1277, 1024, 820, 655, 526, 423, 335, 272, 215, 172, 137, 110, 87, 70, 56, 45,
               36, 29, 23, 18, 15]


def weight(nice: int) -> int:
    return NICE_WEIGHT[nice + 20]


@dataclass
class Job:
    name: str
    arrival: int
    bursts: list
    tickets: int = 100
    nice: int = 0
    # state during a run
    k: int = 0                  # which burst
    left: int = 0               # of the current burst
    first: int | None = None
    finish: int | None = None
    level: int = 0
    used: int = 0               # allotment used at this level
    pass_: float = 0.0
    vrt: float = 0.0
    ran: int = 0                # CPU ticks so far
    wake: int = 0


@dataclass
class Result:
    jobs: list
    segments: list
    switches: int
    end: int
    cpu: dict = field(default_factory=dict)   # name -> list of cumulative CPU ticks, one entry per tick
    levels: dict = field(default_factory=dict)

    def metrics(self) -> dict:
        out = {}
        for j in self.jobs:
            if j.finish is None:
                continue
            busy = sum(j.bursts[::2])
            io = sum(j.bursts[1::2])
            out[j.name] = {"turnaround": j.finish - j.arrival, "response": j.first - j.arrival,
                           "waiting": j.finish - j.arrival - busy - io, "finish": j.finish}
        if out:
            for m in ("turnaround", "response", "waiting"):
                out.setdefault("mean", {})[m] = sum(v[m] for v in out.values() if "finish" in v) / len(
                    [v for v in out.values() if "finish" in v])
        return out


def simulate(jobs: list[Job], policy: str = "fcfs", quantum: int = 10, switch: int = 0, horizon: int = 10 ** 7,
             levels: int = 3, quanta=(10, 20, 40), allotment=None, boost: int | None = None, rule4a: bool = False,
             seed: int = 1, L: int = 10_000, latency: int = 24, granularity: int = 3, track: bool = False) -> Result:
    import copy
    jobs = [copy.copy(j) for j in jobs]
    for j in jobs:
        j.bursts = list(j.bursts)
        j.k, j.left, j.first, j.finish, j.level, j.used, j.pass_, j.vrt, j.ran = 0, j.bursts[0], None, None, 0, 0, \
            0.0, 0.0, 0
    allot = list(allotment or quanta)
    rng = random.Random(seed)
    ready: list[Job] = []
    waiting: list[Job] = []          # in I/O, until j.wake
    pending = sorted(jobs, key=lambda j: j.arrival)
    t = 0
    cur: Job | None = None
    slice_used = 0
    last: Job | None = None
    seg: list = []
    switches = 0
    cpu = {j.name: [] for j in jobs} if track else {}
    lv = {j.name: [] for j in jobs} if track else {}
    done = 0

    def admit(j, waking=False):
        if policy == "stride":
            j.pass_ = max(j.pass_, min([x.pass_ for x in ready] + ([cur.pass_] if cur else []), default=0.0))
        if policy == "cfs":
            mv = min([x.vrt for x in ready] + ([cur.vrt] if cur else []), default=j.vrt)
            j.vrt = max(j.vrt, mv - latency / 2) if waking else max(j.vrt, mv)
        ready.append(j)

    def mark(name, a, b):
        if seg and seg[-1][2] == name and seg[-1][1] == a:
            seg[-1] = (seg[-1][0], b, name)
        else:
            seg.append((a, b, name))

    def cfs_slice(j):
        tot = sum(weight(x.nice) for x in ready) + weight(j.nice)
        return max(granularity, latency * weight(j.nice) / tot)

    while done < len(jobs) and t < horizon:
        while pending and pending[0].arrival <= t:
            admit(pending.pop(0))
        for j in [w for w in waiting if w.wake <= t]:
            waiting.remove(j)
            admit(j, waking=True)
        if boost and t > 0 and t % boost == 0:
            for j in ready + ([cur] if cur else []):
                j.level, j.used = 0, 0
        # preemption
        if cur is not None:
            pre = False
            if policy == "srtf" and ready and min(x.left for x in ready) < cur.left:
                pre = True
            elif policy in ("rr", "lottery", "stride") and slice_used >= quantum and ready:
                pre = True
            elif policy == "mlfq":
                pre = slice_used >= quanta[cur.level] or any(x.level < cur.level for x in ready)
            elif policy == "cfs" and ready and slice_used >= cfs_slice(cur) and min(x.vrt for x in ready) < cur.vrt:
                pre = True
            if pre:
                ready.append(cur)
                cur = None
        if cur is None and ready:
            if policy in ("fcfs", "rr"):
                cur = ready.pop(0)
            elif policy in ("sjf", "srtf"):
                cur = min(ready, key=lambda x: (x.left, x.arrival))
                ready.remove(cur)
            elif policy == "mlfq":
                top = min(x.level for x in ready)
                cur = next(x for x in ready if x.level == top)
                ready.remove(cur)
            elif policy == "lottery":
                tot = sum(x.tickets for x in ready)
                r = rng.randrange(tot)
                for x in ready:
                    r -= x.tickets
                    if r < 0:
                        cur = x
                        break
                ready.remove(cur)
            elif policy == "stride":
                cur = min(ready, key=lambda x: (x.pass_, x.name))
                ready.remove(cur)
            elif policy == "cfs":
                cur = min(ready, key=lambda x: (x.vrt, x.name))
                ready.remove(cur)
            else:
                raise ValueError(policy)
            slice_used = 0
            if policy == "stride":
                cur.pass_ += L / cur.tickets
            if last is not None and cur is not last:
                switches += 1
                if switch:
                    mark("switch", t, t + switch)
                    t += switch
            last = cur
            if cur.first is None:
                cur.first = t
        # run one tick
        if cur is not None:
            mark(cur.name, t, t + 1)
            cur.left -= 1
            cur.ran += 1
            slice_used += 1
            if policy == "cfs":
                cur.vrt += 1024 / weight(cur.nice)
            if policy == "mlfq":
                cur.used += 1
                if cur.used >= allot[cur.level]:
                    cur.level = min(cur.level + 1, levels - 1)
                    cur.used = 0
                    slice_used = quanta[cur.level] + 1   # at the end of its allotment: move on
            if cur.left == 0:
                cur.k += 1
                if cur.k >= len(cur.bursts):
                    cur.finish = t + 1
                    done += 1
                else:
                    cur.wake = t + 1 + cur.bursts[cur.k]
                    cur.k += 1
                    cur.left = cur.bursts[cur.k] if cur.k < len(cur.bursts) else 0
                    if cur.k >= len(cur.bursts):
                        cur.finish = cur.wake
                        done += 1
                    else:
                        if policy == "mlfq" and rule4a:
                            cur.used = 0
                        waiting.append(cur)
                cur = None
        if track:
            for j in jobs:
                cpu[j.name].append(j.ran)
                lv[j.name].append(j.level)
        t += 1
    return Result(jobs, seg, switches, t, cpu, lv)


# -- work stealing (chapter 10; callback to Part 10) ------------------------------------------------
def fork_join(depth: int, leaf: int, seed: int = 0):
    """A random binary fork-join tree: each node forks two children, then joins; leaves do ``leaf`` units of
    work (times a random factor 1-3).  Returns (T1, Tinf, tree)."""
    rng = random.Random(seed)

    def build(d):
        if d == 0:
            return ("leaf", leaf * rng.randint(1, 3))
        return ("fork", build(d - 1), build(d - 1))
    tree = build(depth)

    def work(n):
        return n[1] if n[0] == "leaf" else 1 + work(n[1]) + work(n[2])

    def span(n):
        return n[1] if n[0] == "leaf" else 1 + max(span(n[1]), span(n[2]))
    return work(tree), span(tree), tree


def work_stealing(tree, P: int, seed: int = 0, steal_cost: int = 1) -> dict:
    """Cilk-style work stealing (Blumofe and Leiserson, 1999): a worker that reaches a fork pushes the right child
    on the bottom of its own deque and goes on with the left; an idle worker steals the oldest task from the top of
    a random victim's deque, paying ``steal_cost``.  A fork costs one unit, a leaf its work; a fork is finished when
    both children are.  Returns the makespan, the steals and the steal attempts."""
    rng = random.Random(seed)

    def mk(n, parent):
        node = {"kind": n[0], "parent": parent, "pending": 2}
        node["cost"] = n[1] if n[0] == "leaf" else 1
        if n[0] == "fork":
            node["kids"] = (mk(n[1], node), mk(n[2], node))
        return node
    root = mk(tree, None)
    deques = [[] for _ in range(P)]
    cur = [None] * P
    cur[0] = [root, root["cost"]]
    t = steals = attempts = 0
    over = False
    while not over:
        for w in range(P):
            if cur[w] is None:
                if deques[w]:
                    n = deques[w].pop()
                    cur[w] = [n, n["cost"]]
                elif P > 1:
                    v = rng.randrange(P - 1)
                    v += v >= w
                    attempts += 1
                    if deques[v]:
                        n = deques[v].pop(0)
                        steals += 1
                        cur[w] = [n, n["cost"] + steal_cost]
                    continue
            if cur[w] is None:
                continue
            cur[w][1] -= 1
            if cur[w][1] > 0:
                continue
            n = cur[w][0]
            cur[w] = None
            if n["kind"] == "fork":
                left, right = n["kids"]
                deques[w].append(right)
                cur[w] = [left, left["cost"]]
                continue
            p = n["parent"]
            while True:
                if p is None:
                    over = True
                    break
                p["pending"] -= 1
                if p["pending"] > 0:
                    break
                p = p["parent"]
        t += 1
    return {"makespan": t, "steals": steals, "attempts": attempts}
