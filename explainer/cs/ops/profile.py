"""Profiling (Part 50): a sampling profiler of the Job running on our Pebble emulator.  Two views of one run.

* The guest: every ``interval`` instructions the profiler reads Pebble's program counter and maps it to the
  program's labels, grouped into functions by who calls whom, to give folded stacks and a flame graph (Gregg).
  An exact count of every instruction checks the sample: a share p measured from n samples has a binomial standard
  error sqrt(p (1 - p) / n).
* The host: a timer signal samples the Python stack of the emulator itself (where the emulator spends its time)."""

from __future__ import annotations

import math
import signal
from collections import Counter

FUNCS = {  # Pebble labels in JOB_V0, by the routine they belong to
    "main": ("read", "lower", "sep", "eof"),
    "word": ("word", "scan", "cmp", "found", "next", "insert"),
    "report": ("report", "rloop", "find", "fnext", "got", "pw", "pcount", "done"),
    "printnum": ("printnum", "pnext", "psub", "pdig", "pout", "pskip", "pend"),
}
STACK = {"main": ["main"], "word": ["main", "word"], "report": ["main", "report"],
         "printnum": ["main", "report", "printnum"]}


def _tape(chars: int) -> bytes:
    from explainer.cs.pebble.programs import job_tape
    from videos.cs.cs6.compute import novels
    text = next(iter(novels().values()))
    start = text.find("CHAPTER I")
    return job_tape(text[max(0, start):max(0, start) + chars])


def guest_profile(chars: int = 20_000, interval: int = 997) -> dict:
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble.emu import Machine
    from explainer.cs.pebble.programs import JOB_V0
    prog = assemble(JOB_V0)
    code_labels = {k: v for k, v in prog.labels.items() if any(k in v_ for v_ in FUNCS.values())}
    order = sorted(code_labels.items(), key=lambda kv: kv[1])
    owner = {lab: f for f, labs in FUNCS.items() for lab in labs}

    def block(pc):
        best = "start"
        for lab, a in order:
            if a <= pc:
                best = lab
            else:
                break
        return best

    exact, samples = Counter(), Counter()

    class Profiled(Machine):
        n = 0

        def step(self):
            pc = self.pc
            exact[pc] += 1
            Profiled.n += 1
            if Profiled.n % interval == 0:
                samples[pc] += 1
            Machine.step(self)

    tape = _tape(chars)
    m = Profiled(image=prog.image, tape=tape).run(200_000_000)
    cache = {}

    def stack(pc):
        if pc not in cache:
            b = block(pc)
            f = owner.get(b, "main")
            cache[pc] = ";".join(STACK[f] + [b])
        return cache[pc]

    folded, truth = Counter(), Counter()
    for pc, c in samples.items():
        folded[stack(pc)] += c
    for pc, c in exact.items():
        truth[stack(pc)] += c
    n, N = sum(folded.values()), sum(truth.values())
    rows = []
    for s in sorted(truth, key=lambda s: -truth[s]):
        p_true = truth[s] / N
        p_hat = folded.get(s, 0) / n
        se = math.sqrt(p_hat * (1 - p_hat) / n)
        se_true = math.sqrt(p_true * (1 - p_true) / n)
        rows.append({"stack": s, "true": p_true, "sampled": p_hat, "se": se, "z": (p_hat - p_true) / se_true})
    return {"folded": dict(folded), "exact": dict(truth), "samples": n, "instructions": N, "interval": interval,
            "bytes": len(tape), "rows": rows, "flame": flame(folded), "output": bytes(m.out).decode(errors="replace")
            if hasattr(m, "out") else None}


def flame(folded: dict) -> list[dict]:
    """Rectangles of a flame graph: each frame's width is its share of samples; children sit on their parent,
    sorted alphabetically (a flame graph's x axis is not time)."""
    total = sum(folded.values())
    tree = {}
    for s, c in folded.items():
        node = tree
        for fr in s.split(";"):
            node = node.setdefault(fr, {"_n": 0, "_k": {}})
            node["_n"] += c
            node = node["_k"]
    out = []

    def walk(level, x0, depth, path):
        x = x0
        for name in sorted(level):
            w = level[name]["_n"] / total
            out.append({"name": name, "x": x, "w": w, "depth": depth, "path": ";".join(path + [name])})
            walk(level[name]["_k"], x, depth + 1, path + [name])
            x += w

    walk(tree, 0.0, 0, [])
    return out


def host_profile(chars: int = 12_000, hz: int = 1000) -> dict:
    """Sample the Python stack of the emulator itself with a CPU-time timer signal."""
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble.emu import Machine
    from explainer.cs.pebble.programs import JOB_V0
    prog = assemble(JOB_V0)
    tape = _tape(chars)
    folded = Counter()

    def handler(sig, frame):
        names = []
        f = frame
        while f is not None:
            code = f.f_code
            if "pebble" in code.co_filename:
                names.append(getattr(code, "co_qualname", code.co_name))
            f = f.f_back
        if names:
            folded[";".join(reversed(names))] += 1

    old = signal.signal(signal.SIGPROF, handler)
    signal.setitimer(signal.ITIMER_PROF, 1 / hz, 1 / hz)
    try:
        Machine(image=prog.image, tape=tape).run(200_000_000)
    finally:
        signal.setitimer(signal.ITIMER_PROF, 0, 0)
        signal.signal(signal.SIGPROF, old)
    return {"folded": dict(folded), "samples": sum(folded.values()), "flame": flame(folded), "hz": hz}
