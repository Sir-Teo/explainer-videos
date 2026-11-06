"""Inside a JavaScript engine (Part 42): hidden classes (shapes) with transitions, inline caches at property-access
sites (uninitialized, monomorphic, polymorphic, megamorphic), and type feedback with deoptimization.  Costs are
counted operations, not times."""

from __future__ import annotations

import random


class Shape:
    """A hidden class: property name -> slot offset, plus transitions to the shapes made by adding one property."""
    _next = 0

    def __init__(self, props=()):
        self.props = dict((p, i) for i, p in enumerate(props))
        self.trans = {}
        Shape._next += 1
        self.id = Shape._next

    def add(self, name):
        if name not in self.trans:
            self.trans[name] = Shape(list(self.props) + [name])
        return self.trans[name]


class Obj:
    def __init__(self, root: Shape, **kw):
        self.shape = root
        self.slots = []
        for k, v in kw.items():
            self.shape = self.shape.add(k)
            self.slots.append(v)


class Site:
    """One property access site, say `p.x` in a loop.  Up to four shapes are cached (polymorphic); beyond that the
    site goes megamorphic and does a dictionary lookup every time."""

    def __init__(self, name, limit=4):
        self.name, self.limit = name, limit
        self.cache = []                # (shape id, offset)
        self.state = "uninitialized"
        self.ops = {"shape checks": 0, "dictionary lookups": 0, "misses": 0}

    def get(self, o: Obj):
        if self.state == "megamorphic":
            self.ops["dictionary lookups"] += 1
            return o.slots[o.shape.props[self.name]]
        for sid, off in self.cache:
            self.ops["shape checks"] += 1
            if sid == o.shape.id:
                return o.slots[off]
        self.ops["misses"] += 1
        self.ops["dictionary lookups"] += 1
        off = o.shape.props[self.name]
        if len(self.cache) < self.limit:
            self.cache.append((o.shape.id, off))
            self.state = "monomorphic" if len(self.cache) == 1 else "polymorphic"
        else:
            self.state = "megamorphic"
            self.cache = []
        return o.slots[off]


def ic_experiment(n=10_000, seed=0):
    """Sum p.x over n points whose objects were built with 1, 2, 4 or 8 different property orders."""
    rng = random.Random(seed)
    orders = [["x", "y"], ["y", "x"], ["x", "y", "z"], ["z", "x", "y"], ["x", "z", "y"], ["y", "z", "x"],
              ["z", "y", "x"], ["y", "x", "z"]]
    out = {}
    for k in (1, 2, 4, 8):
        root = Shape()
        objs = []
        for i in range(n):
            ordr = orders[rng.randrange(k)]
            objs.append(Obj(root, **{p: (i if p == "x" else 0) for p in ordr}))
        site = Site("x")
        total = sum(site.get(o) for o in objs)
        shapes = len({o.shape.id for o in objs})
        out[k] = {"shapes": shapes, "state": site.state, **site.ops, "sum_ok": total == n * (n - 1) // 2,
                  "per_access": (site.ops["shape checks"] + 10 * site.ops["dictionary lookups"]) / n}
    return out


def transition_tree():
    """The shapes created by two constructors that add the same properties in different orders."""
    root = Shape()
    a = Obj(root, x=1, y=2)
    b = Obj(root, x=3, y=4)
    c = Obj(root, y=5, x=6)
    edges = []

    def walk(s, path):
        for name, t in s.trans.items():
            edges.append((path, path + [name]))
            walk(t, path + [name])
    walk(root, [])
    return {"same_shape_ab": a.shape is b.shape, "same_shape_ac": a.shape is c.shape,
            "edges": [("." + ".".join(p) if p else "{}", "." + ".".join(q)) for p, q in edges]}


def deopt_trace(values):
    """Type feedback for `function add(a, b) { return a + b }`: after a few calls with small integers the optimizing
    tier compiles an integer-only version guarded by type checks; a string or an overflowing value fails a guard,
    deoptimizes back to the interpreter, and the feedback widens."""
    feedback = set()
    tier, calls, events = "interpreter", 0, []
    for n, (a, b) in enumerate(values, 1):
        kind = "string" if isinstance(a, str) or isinstance(b, str) else (
            "small int" if abs(a + b) < 2 ** 31 and isinstance(a, int) and isinstance(b, int) else "number")
        calls += 1
        if tier.startswith("optimized"):
            if kind not in feedback:
                events.append((n, f"guard failed on {kind}: deoptimize"))
                tier = "interpreter"
                calls = 0
        feedback.add(kind)
        if tier == "interpreter" and calls >= 3:
            tier = "optimized for " + " or ".join(sorted(feedback))
            events.append((n, tier))
    return events
