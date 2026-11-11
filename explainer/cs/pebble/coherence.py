"""Cache coherence and memory consistency for Pebble's multicore (Part 10).

    sys = MESI(cores=4, sets=64, ways=4)
    sys.access(core, addr, write)     # returns the event: hit, or the bus transaction it caused
    sys.state(core, addr)             # 'M', 'E', 'S' or 'I'
    sys.stats                         # hits, misses, invalidations, write-backs, transfers between caches

    litmus_sb(model="sc" | "tso", trials=...)   # the store-buffering litmus test: how often both loads read 0

MESI is the snooping protocol of Papamarcos and Patel (1984): every line in every private cache is Modified (dirty,
only copy), Exclusive (clean, only copy), Shared (clean, maybe other copies) or Invalid.  A read miss asks the bus;
another cache holding the line Modified supplies it and both end Shared; with no other copy the reader gets it
Exclusive.  A write needs the only copy: a write to a Shared line broadcasts an invalidation first; a write to an
Exclusive line just becomes Modified, silently.  The checks in tests/test_cs10_parallel.py: at most one Modified or
Exclusive copy of any line; a Modified copy excludes every other copy; every read returns the last value written.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


class MESI:
    def __init__(self, cores: int = 4, sets: int = 64, ways: int = 4, line: int = 64):
        self.n, self.sets, self.ways, self.line = cores, sets, ways, line
        self.caches = [[dict() for _ in range(sets)] for _ in range(cores)]  # set -> {line: state}, insertion = LRU
        self.memory: dict[int, int] = {}  # line -> value (a version number standing for the data)
        self.data = [dict() for _ in range(cores)]  # core -> {line: value held in its cache}
        self.stats = {"hits": 0, "misses": 0, "invalidations": 0, "writebacks": 0, "transfers": 0, "bus": 0}
        self.log: list[tuple] = []

    def _set(self, ln: int) -> int:
        return ln % self.sets

    def state(self, core: int, addr: int) -> str:
        ln = addr // self.line
        return self.caches[core][self._set(ln)].get(ln, "I")

    def _touch(self, core: int, ln: int, st: str):
        s = self.caches[core][self._set(ln)]
        s.pop(ln, None)
        if len(s) >= self.ways:
            victim, vst = next(iter(s.items()))
            del s[victim]
            if vst == "M":
                self.memory[victim] = self.data[core][victim]
                self.stats["writebacks"] += 1
            self.data[core].pop(victim, None)
        s[ln] = st

    def access(self, core: int, addr: int, write: bool = False, value: int | None = None) -> str:
        """Perform one access; returns a short description of what happened.  ``value`` is written on a store (a
        stand-in for data, so the checker can follow the last value written)."""
        ln = addr // self.line
        st = self.state(core, ln * self.line)
        others = [c for c in range(self.n) if c != core and self.state(c, ln * self.line) != "I"]
        if not write:
            if st != "I":
                self.stats["hits"] += 1
                self._touch(core, ln, st)
                ev = "read hit"
            else:
                self.stats["misses"] += 1
                self.stats["bus"] += 1
                owner = [c for c in others if self.state(c, ln * self.line) == "M"]
                if owner:
                    o = owner[0]
                    self.memory[ln] = self.data[o][ln]  # the owner writes back as it supplies the line
                    self.stats["writebacks"] += 1
                    self.stats["transfers"] += 1
                    self._set_state(o, ln, "S")
                    self.data[core][ln] = self.data[o][ln]
                    self._touch(core, ln, "S")
                    ev = f"read miss: core {o} supplies its Modified line; both Shared"
                elif others:
                    for o in others:
                        if self.state(o, ln * self.line) == "E":
                            self._set_state(o, ln, "S")
                    self.data[core][ln] = self.memory.get(ln, 0)
                    self._touch(core, ln, "S")
                    ev = "read miss: others have it; Shared"
                else:
                    self.data[core][ln] = self.memory.get(ln, 0)
                    self._touch(core, ln, "E")
                    ev = "read miss: the only copy; Exclusive"
        else:
            if st in ("M", "E"):
                self.stats["hits"] += 1
                ev = "write hit" + (" (Exclusive becomes Modified, silently)" if st == "E" else "")
            else:
                self.stats["bus"] += 1
                if st == "S":
                    self.stats["hits"] += 1
                    ev = "write to a Shared line: invalidate the others"
                else:
                    self.stats["misses"] += 1
                    owner = [c for c in others if self.state(c, ln * self.line) == "M"]
                    if owner:
                        self.memory[ln] = self.data[owner[0]][ln]
                        self.stats["writebacks"] += 1
                        self.stats["transfers"] += 1
                    ev = "write miss: read for ownership" + (", invalidate the others" if others else "")
                for o in others:
                    self._set_state(o, ln, "I")
                    self.data[o].pop(ln, None)
                    self.stats["invalidations"] += 1
            self.data[core][ln] = value if value is not None else self.data[core].get(ln, self.memory.get(ln, 0))
            self._touch(core, ln, "M")
        self.log.append((core, ln, write, ev))
        return ev

    def _set_state(self, core: int, ln: int, st: str):
        s = self.caches[core][self._set(ln)]
        if st == "I":
            s.pop(ln, None)
        else:
            s[ln] = st

    def read_value(self, core: int, addr: int) -> int:
        """The value a load by ``core`` returns (after the coherence actions of ``access``)."""
        ln = addr // self.line
        return self.data[core].get(ln, self.memory.get(ln, 0))

    def check(self) -> None:
        """The single-writer, multiple-reader invariant."""
        lines = set()
        for c in range(self.n):
            for s in self.caches[c]:
                lines |= set(s)
        for ln in lines:
            sts = [self.state(c, ln * self.line) for c in range(self.n)]
            exclusive = sum(st in ("M", "E") for st in sts)
            assert exclusive <= 1, (ln, sts)
            if exclusive:
                assert sum(st != "I" for st in sts) == 1, (ln, sts)


# ---------------------------------------------------------------------------
# memory consistency: the store-buffering litmus test
# ---------------------------------------------------------------------------
@dataclass
class _Thread:
    prog: list  # ("st", var, val) or ("ld", var, reg)
    pc: int = 0
    buffer: list = field(default_factory=list)  # pending stores (TSO), oldest first
    regs: dict = field(default_factory=dict)


def litmus_sb(model: str = "tso", trials: int = 100_000, seed: int = 1, drain: float = 0.5) -> dict:
    """Thread 0: x = 1; r0 = y.   Thread 1: y = 1; r1 = x.   Under sequential consistency (Lamport 1979) some store
    comes first, so r0 = r1 = 0 is impossible.  Under TSO each core's stores wait in a FIFO store buffer, and its own
    loads read past them (or from them, for its own address): both loads can read 0.  Random interleavings; returns
    how often each outcome occurs."""
    rng = random.Random(seed)
    out: dict[tuple, int] = {}
    for _ in range(trials):
        mem = {"x": 0, "y": 0}
        th = [_Thread([("st", "x", 1), ("ld", "y", "r0")]), _Thread([("st", "y", 1), ("ld", "x", "r1")])]
        while any(t.pc < len(t.prog) or t.buffer for t in th):
            t = rng.choice([t for t in th if t.pc < len(t.prog) or t.buffer])
            if model == "tso" and t.buffer and (t.pc >= len(t.prog) or rng.random() < drain):
                var, val = t.buffer.pop(0)  # a store leaves the buffer for memory
                mem[var] = val
                continue
            op = t.prog[t.pc]
            t.pc += 1
            if op[0] == "st":
                if model == "tso":
                    t.buffer.append((op[1], op[2]))
                else:
                    mem[op[1]] = op[2]
            else:
                own = [v for var, v in t.buffer if var == op[1]]
                t.regs[op[2]] = own[-1] if own else mem[op[1]]
        key = (th[0].regs["r0"], th[1].regs["r1"])
        out[key] = out.get(key, 0) + 1
    return {f"r0={a}, r1={b}": n / trials for (a, b), n in sorted(out.items())}
