"""The event loop (Part 42), as the HTML standard describes it: one task from a task queue runs to completion, then
the whole microtask queue drains, then, if a frame is due, the rendering steps run (requestAnimationFrame callbacks,
style, layout, paint).  A tiny interpreter for programs written as nested steps, so that orderings can be computed
rather than asserted, and a frame timeline that shows a long task causing jank."""

from __future__ import annotations

from collections import deque

FRAME = 1000 / 60


class Loop:
    """Steps are tuples: ("log", s), ("timeout", ms, steps), ("promise", steps) (queue a microtask),
    ("raf", steps), ("async", steps) (call an async function), ("await",) (the rest of the function
    becomes a microtask), ("work", ms)."""

    def __init__(self):
        self.t = 0.0
        self.tasks = deque()            # (ready time, seq, steps, label)
        self.micro = deque()
        self.raf = []
        self.log = []
        self.timeline = []              # (start, end, kind, label)
        self.seq = 0

    def run_steps(self, steps):
        for k, st in enumerate(steps):
            op = st[0]
            if op == "log":
                self.log.append(st[1])
            elif op == "timeout":
                self.seq += 1
                self.tasks.append((self.t + st[1], self.seq, st[2], "setTimeout"))
            elif op == "promise":
                self.micro.append(st[1])
            elif op == "raf":
                self.raf.append(st[1])
            elif op == "work":
                self.t += st[1]
            elif op == "async":
                self.run_steps(st[1])          # an async function runs synchronously up to its first await
            elif op == "await":
                self.micro.append(list(steps[k + 1:]))
                return

    def drain(self):
        while self.micro:
            self.run_steps(self.micro.popleft())

    def run(self, script, until=200.0, render_every=FRAME):
        start = self.t
        self.run_steps(script)
        self.timeline.append((start, self.t, "task", "script"))
        self.drain()
        next_frame = render_every
        while self.t < until and (self.tasks or self.raf or self.micro):
            if self.t >= next_frame - 1e-9:
                cbs, self.raf = self.raf, []
                s = self.t
                for cb in cbs:
                    self.run_steps(cb)
                    self.drain()
                self.t += 1.0           # style, layout, paint
                self.timeline.append((s, self.t, "render", f"frame at {next_frame:.1f}"))
                while next_frame <= self.t:
                    next_frame += render_every
                continue
            ready = sorted((x for x in self.tasks if x[0] <= self.t), key=lambda x: (x[0], x[1]))
            if ready:
                task = ready[0]
                self.tasks.remove(task)
                s = self.t
                self.run_steps(task[2])
                self.timeline.append((s, self.t, "task", task[3]))
                self.drain()
            else:
                nxt = min([x[0] for x in self.tasks] + [next_frame])
                self.t = max(self.t, nxt)
        return self.log


def ordering_examples():
    """Classic orderings, computed."""
    ex = {}
    ex["basic"] = Loop().run([("log", "A"), ("timeout", 0, [("log", "B")]), ("promise", [("log", "C")]),
                              ("log", "D")])
    ex["nested"] = Loop().run([("timeout", 0, [("log", "t1"), ("promise", [("log", "p-in-t1")])]),
                               ("timeout", 0, [("log", "t2")]),
                               ("promise", [("log", "p1"), ("promise", [("log", "p2")])]), ("log", "sync")])
    ex["async"] = Loop().run([("log", "before call"), ("async", [("log", "f starts"), ("await",), ("log", "f resumes")]),
                              ("promise", [("log", "then")]), ("log", "after call")])
    ex["async2"] = Loop().run([("log", "script start"), ("timeout", 0, [("log", "timeout")]),
                               ("promise", [("log", "promise1"), ("promise", [("log", "promise2")])]),
                               ("raf", [("log", "raf")]), ("log", "script end")])
    return ex


def jank(long_task_ms: float = 120.0, frames: int = 16):
    """A page animating with requestAnimationFrame, and a click handler that does long_task_ms of work: which
    frames are delivered on time."""
    lp = Loop()
    selfref = [("work", 3.0), ("log", "frame")]
    selfref.append(("raf", selfref))      # a callback that re-registers itself, as an animation does
    lp.run([("raf", selfref), ("timeout", 40, [("log", "click"), ("work", long_task_ms)])],
           until=frames * FRAME)
    renders = [(s, e) for s, e, k, _ in lp.timeline if k == "render"]
    gaps = [b[0] - a[0] for a, b in zip(renders, renders[1:])]
    return {"timeline": lp.timeline, "renders": renders, "gaps": gaps,
            "dropped": sum(max(0, round(g / FRAME) - 1) for g in gaps)}


def chunked(total_ms: float = 120.0, chunk_ms: float = 8.0, frames: int = 16):
    """The same work split into chunks, each yielding back to the loop with setTimeout(0)."""
    lp = Loop()
    selfref = [("work", 3.0), ("log", "frame")]
    selfref.append(("raf", selfref))
    n = int(total_ms / chunk_ms)

    def chunk(k):
        st = [("work", chunk_ms)]
        if k + 1 < n:
            st.append(("timeout", 0, chunk(k + 1)))
        return st
    lp.run([("raf", selfref), ("timeout", 40, [("log", "click")] + chunk(0))], until=frames * FRAME)
    renders = [(s, e) for s, e, k, _ in lp.timeline if k == "render"]
    gaps = [b[0] - a[0] for a, b in zip(renders, renders[1:])]
    done = max(e for s, e, k, lab in lp.timeline if k == "task")
    return {"timeline": lp.timeline, "renders": renders, "gaps": gaps, "finish": done,
            "dropped": sum(max(0, round(g / FRAME) - 1) for g in gaps)}
