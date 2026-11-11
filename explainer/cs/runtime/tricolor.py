"""Incremental marking with the tri-color abstraction (Dijkstra, Lamport, Martin, Scholten and Steffens 1978), under a
mutator that keeps running (Part 15, chapter 11).

White objects have not been reached; gray ones have been reached but not scanned; black ones are reached and
scanned.  The invariant that makes incremental marking correct is the *strong tri-color invariant*: no black object
points at a white one.  A mutator that stores a pointer to a white object into a black one, and then deletes the
other path to it, hides the object from the marker, which frees it while it is still in use.

* ``barrier=None``: no barrier.  The marker can lose live objects.
* ``"dijkstra"`` (incremental update, an *insertion* barrier): storing a pointer to a white object shades it gray.
  The mutator's registers are not barriered, so they are rescanned when the marker runs dry.
* ``"yuasa"`` (snapshot at the beginning, a *deletion* barrier, Yuasa 1990): overwriting a pointer shades the old
  target gray, so everything reachable when marking began is marked; new objects are allocated black.  It never
  loses an object, and keeps more floating garbage.

:func:`trial` runs one random collection cycle; :func:`experiment` counts, over many trials, how often a live object
would have been freed and how much garbage survived.  :func:`scripted` is the four-move story the scene animates.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

WHITE, GRAY, BLACK = 0, 1, 2


@dataclass
class Heap:
    fields: list                       # per object, a list of 2 targets (or None)
    color: list
    regs: list                         # the mutator's registers: object ids or None
    gray: list = field(default_factory=list)
    shaded_by_barrier: int = 0

    def shade(self, o):
        if o is not None and self.color[o] == WHITE:
            self.color[o] = GRAY
            self.gray.append(o)

    def reachable(self):
        seen, todo = set(), [r for r in self.regs if r is not None]
        while todo:
            o = todo.pop()
            if o in seen:
                continue
            seen.add(o)
            todo += [c for c in self.fields[o] if c is not None]
        return seen

    def mark_step(self, k=1):
        for _ in range(k):
            if not self.gray:
                return False
            o = self.gray.pop()
            for c in self.fields[o]:
                self.shade(c)
            self.color[o] = BLACK
        return True


def random_heap(n, rng, nregs=3):
    fields = [[None, None] for _ in range(n)]
    for o in range(n):
        for j in range(2):
            if rng.random() < 0.7:
                fields[o][j] = rng.randrange(n)
    regs = [rng.randrange(n) for _ in range(nregs)]
    return Heap(fields=fields, color=[WHITE] * n, regs=regs)


def write(h: Heap, src, j, dst, barrier):
    old = h.fields[src][j]
    if barrier == "dijkstra" and dst is not None and h.color[src] == BLACK and h.color[dst] == WHITE:
        h.shade(dst)
        h.shaded_by_barrier += 1
    if barrier == "yuasa" and old is not None and h.color[old] == WHITE:
        h.shade(old)
        h.shaded_by_barrier += 1
    h.fields[src][j] = dst


def trial(seed, barrier=None, n=40, mut_per_step=3, p_alloc=0.1):
    rng = random.Random(seed)
    h = random_heap(n, rng)
    for r in h.regs:                    # the roots, shaded when the cycle starts
        h.shade(r)
    allocated = 0
    rescans = 0
    while True:
        for _ in range(mut_per_step):
            live = [r for r in h.regs if r is not None]
            if not live:
                break
            a = rng.choice(live)
            op = rng.random()
            i = rng.randrange(len(h.regs))
            if op < 0.35:                             # load a field into a register
                h.regs[i] = h.fields[a][rng.randrange(2)]
            elif op < 0.7:                            # store a register into a field
                write(h, a, rng.randrange(2), h.regs[i], barrier)
            elif op < 0.85:                           # delete a field
                write(h, a, rng.randrange(2), None, barrier)
            elif op < 0.85 + p_alloc:                 # allocate
                h.fields.append([None, None])
                h.color.append(BLACK if barrier else WHITE)
                h.regs[i] = len(h.fields) - 1
                allocated += 1
        if not h.mark_step(2):
            if barrier == "dijkstra":
                # registers are not barriered: rescan them, and finish if nothing new turned up
                for r in h.regs:
                    h.shade(r)
                rescans += 1
                if h.gray:
                    continue
            break
    live = h.reachable()
    lost = [o for o in live if h.color[o] == WHITE]
    floating = [o for o in range(len(h.fields)) if h.color[o] != WHITE and o not in live]
    return {"lost": len(lost), "floating": len(floating), "live": len(live), "barrier_shades": h.shaded_by_barrier,
            "allocated": allocated, "rescans": rescans}


def experiment(trials=2000, **kw):
    out = {}
    for b in (None, "dijkstra", "yuasa"):
        rs = [trial(s, barrier=b, **kw) for s in range(trials)]
        out[b or "none"] = {
            "trials": trials,
            "cycles_losing": sum(1 for r in rs if r["lost"]),
            "objects_lost": sum(r["lost"] for r in rs),
            "floating": sum(r["floating"] for r in rs) / trials,
            "live": sum(r["live"] for r in rs) / trials,
            "barrier_shades": sum(r["barrier_shades"] for r in rs) / trials,
        }
    return out


def scripted():
    """The textbook loss, move by move: roots R → A (black), A → B (gray), B → C (white).  The mutator copies the
    pointer to C into A, then deletes B → C.  Returns the frames: (description, colors, edges)."""
    names = ["R", "A", "B", "C"]
    edges = {("R", "A"), ("A", "B"), ("B", "C")}
    col = {"R": BLACK, "A": BLACK, "B": GRAY, "C": WHITE}
    frames = [("marking in progress: A scanned, B not yet", dict(col), set(edges))]
    edges.add(("A", "C"))
    frames.append(("the mutator stores B's pointer to C into A", dict(col), set(edges)))
    edges.discard(("B", "C"))
    frames.append(("then deletes B's pointer to C", dict(col), set(edges)))
    col["B"] = BLACK
    frames.append(("the marker scans B and finds nothing: C stays white and is freed, yet A still points at it",
                   dict(col), set(edges)))
    return names, frames
