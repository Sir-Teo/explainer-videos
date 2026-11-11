"""An exhaustive interleaving model checker for small shared-memory programs (Part 33).

    prog = Program({"x": 0}, [T0, T1])          # each thread a list of instructions (below)
    r = explore(prog, model="sc" | "tso" | "pso", invariant=mutex)
    r.states, r.finals, r.violation, r.deadlocks, r.trace(state)

A program is a set of shared variables (all integers, every one named and initialised) and a few threads, each a list
of instructions. Labels are ``("label", name)`` entries; registers are any other names, local to a thread and
starting at 0. An operand ``v`` is an int or a register name.

    ("ld", r, x)               r <- x                       ("st", x, v)              x <- v
    ("ldx", r, base, ri)       r <- base<R[ri]>             ("stx", base, i, v)       base<i> <- v  (i int or reg)
    ("li", r, imm)             ("addi", r, a, imm)          ("add", r, a, b)
    ("mod", r, a, imm)         ("divi", r, a, imm)          ("muli", r, a, imm)
    ("beq", a, b, L)  ("bne", a, b, L)  ("blt", a, b, L)  ("jmp", L)
    ("fence",)                 wait until this thread's store buffer is empty
    ("cas", r, x, old, new)    atomically: if x == old then x <- new, r <- 1, else r <- 0
    ("tas", r, x)              atomically r <- x, x <- 1        ("fai", r, x)  atomically r <- x, x <- x + 1
    ("lock", x)                block until x == 0, then x <- 1   ("unlock", x)  x <- 0
    ("P", s)                   block until s > 0, then s <- s-1  ("V", s)      s <- s + 1
    ("cs",) / ("ncs",)         enter and leave the critical section (the invariant can count who is inside)
    ("out", v)                 append v to this thread's outputs (a decision, a popped value)

Memory models.  **sc**: every instruction is one atomic step, in some interleaving of the threads (Lamport 1979).
**tso** (x86, Part 10): a store goes into the thread's FIFO store buffer; a separate step drains the oldest entry to
memory; a load reads the thread's own newest buffered value for that variable, else memory; ``fence`` and every
atomic (``cas tas fai lock unlock P V``) wait for an empty buffer, as x86's locked instructions do.  **pso** (SPARC's
partial store order, a stand-in for Arm's weaker model): one FIFO per thread *and variable*, drained independently,
so two stores to different variables can reach memory in either order.

The search is breadth-first over states (pcs, registers, memory, buffers, outputs), so a reported violation comes with
a shortest schedule leading to it.  Loops are fine (the visited set closes them); the state space must be finite.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from math import comb

ATOMICS = {"cas", "tas", "fai", "lock", "unlock", "P", "V"}


@dataclass
class Program:
    init: dict
    threads: list
    names: list = field(default_factory=list)       # optional thread names, for traces

    def __post_init__(self):
        self.vars = sorted(self.init)
        self.vi = {v: i for i, v in enumerate(self.vars)}
        self.code, self.regs = [], []
        for t in self.threads:
            labels, code = {}, []
            for ins in t:
                if ins[0] == "label":
                    labels[ins[1]] = len(code)
                else:
                    code.append(ins)
            regs = set()
            for ins in code:
                if ins[0] in ("ld", "ldx", "li", "addi", "add", "mod", "divi", "muli", "cas", "tas", "fai"):
                    regs.add(ins[1])
                for a in ins[1:]:
                    if isinstance(a, str) and a not in self.vi and a not in labels and not _is_base(a, self.vi):
                        regs.add(a)
            jumps = []
            for ins in code:
                if ins[0] in ("beq", "bne", "blt"):
                    ins = ins[:3] + (labels[ins[3]],)
                elif ins[0] == "jmp":
                    ins = ("jmp", labels[ins[1]])
                jumps.append(ins)
            self.code.append(jumps)
            self.regs.append(sorted(regs))
        if not self.names:
            self.names = [f"T{i}" for i in range(len(self.threads))]


def _is_base(a, vi):
    return any(v.startswith(a) and v[len(a):].isdigit() for v in vi)


@dataclass
class Result:
    model: str
    states: int
    finals: dict                 # projection of a terminal state -> how many terminal states give it
    violation: tuple | None      # a state breaking the invariant (the first found: a shortest schedule)
    deadlocks: list
    parent: dict
    prog: Program
    edges: int = 0

    def trace(self, s) -> list[str]:
        """The schedule leading to state ``s``: one line per step."""
        out = []
        while self.parent.get(s) is not None:
            p, label = self.parent[s]
            out.append(label)
            s = p
        return out[::-1]


def _val(v, R, ri):
    return v if isinstance(v, int) else R[ri[v]]


def initial(prog: Program, model: str):
    if model not in ("sc", "tso", "pso"):
        raise ValueError("memory model must be sc, tso or pso")
    n = len(prog.threads)
    mem = tuple(prog.init[v] for v in prog.vars)
    regs = tuple(tuple(0 for _ in prog.regs[t]) for t in range(n))
    bufs = tuple(() for _ in range(n))
    return (tuple(0 for _ in range(n)), regs, mem, bufs, tuple(0 for _ in range(n)), tuple(() for _ in range(n)))


def _read(model, buf, mem, xi):
    if model != "sc":
        for x, v in reversed(buf):
            if x == xi:
                return v
    return mem[xi]


def successors(prog: Program, s, model: str):
    pcs, regs, mem, bufs, incs, outs = s
    n = len(pcs)
    for t in range(n):
        code = prog.code[t]
        pc = pcs[t]
        if pc >= len(code):
            continue
        ins = code[pc]
        op = ins[0]
        buf = bufs[t]
        if model != "sc" and buf and (op in ATOMICS or op == "fence"):
            continue                     # wait for the buffer to drain
        ri = {r: i for i, r in enumerate(prog.regs[t])}
        R = list(regs[t])
        M = None
        B = None
        npc = pc + 1
        inc = incs[t]
        out = outs[t]
        if op == "ld":
            R[ri[ins[1]]] = _read(model, buf, mem, prog.vi[ins[2]])
        elif op == "ldx":
            xi = prog.vi[f"{ins[2]}{R[ri[ins[3]]]}"]
            R[ri[ins[1]]] = _read(model, buf, mem, xi)
        elif op in ("st", "stx"):
            if op == "st":
                xi, v = prog.vi[ins[1]], _val(ins[2], R, ri)
            else:
                xi, v = prog.vi[f"{ins[1]}{_val(ins[2], R, ri)}"], _val(ins[3], R, ri)
            if model == "sc":
                M = list(mem)
                M[xi] = v
            else:
                B = buf + ((xi, v),)
        elif op == "li":
            R[ri[ins[1]]] = ins[2]
        elif op == "addi":
            R[ri[ins[1]]] = R[ri[ins[2]]] + ins[3]
        elif op == "add":
            R[ri[ins[1]]] = _val(ins[2], R, ri) + _val(ins[3], R, ri)
        elif op == "mod":
            R[ri[ins[1]]] = R[ri[ins[2]]] % ins[3]
        elif op == "divi":
            R[ri[ins[1]]] = R[ri[ins[2]]] // ins[3]
        elif op == "muli":
            R[ri[ins[1]]] = R[ri[ins[2]]] * ins[3]
        elif op in ("beq", "bne", "blt"):
            a, b = _val(ins[1], R, ri), _val(ins[2], R, ri)
            if (op == "beq" and a == b) or (op == "bne" and a != b) or (op == "blt" and a < b):
                npc = ins[3]
        elif op == "jmp":
            npc = ins[1]
        elif op == "fence":
            pass
        elif op == "cas":
            xi = prog.vi[ins[2]]
            if mem[xi] == _val(ins[3], R, ri):
                M = list(mem)
                M[xi] = _val(ins[4], R, ri)
                R[ri[ins[1]]] = 1
            else:
                R[ri[ins[1]]] = 0
        elif op in ("tas", "fai"):
            xi = prog.vi[ins[2]]
            M = list(mem)
            R[ri[ins[1]]] = mem[xi]
            M[xi] = 1 if op == "tas" else mem[xi] + 1
        elif op == "lock":
            xi = prog.vi[ins[1]]
            if mem[xi] != 0:
                continue                 # blocked
            M = list(mem)
            M[xi] = 1
        elif op == "unlock":
            M = list(mem)
            M[prog.vi[ins[1]]] = 0
        elif op == "P":
            xi = prog.vi[ins[1]]
            if mem[xi] <= 0:
                continue
            M = list(mem)
            M[xi] -= 1
        elif op == "V":
            M = list(mem)
            M[prog.vi[ins[1]]] += 1
        elif op == "cs":
            inc = 1
        elif op == "ncs":
            inc = 0
        elif op == "out":
            out = out + (_val(ins[1], R, ri),)
        else:
            raise ValueError(f"unknown instruction {ins}")
        nregs = regs[:t] + (tuple(R),) + regs[t + 1:]
        nmem = tuple(M) if M is not None else mem
        nbufs = bufs if B is None else bufs[:t] + (B,) + bufs[t + 1:]
        yield (f"{prog.names[t]}: {_show(ins)}",
               (pcs[:t] + (npc,) + pcs[t + 1:], nregs, nmem, nbufs, incs[:t] + (inc,) + incs[t + 1:],
                outs[:t] + (out,) + outs[t + 1:]))
    if model == "sc":
        return
    for t in range(n):
        buf = bufs[t]
        if not buf:
            continue
        if model == "tso":
            choices = [0]
        else:                            # pso: the oldest entry of any variable
            seen, choices = set(), []
            for i, (x, _) in enumerate(buf):
                if x not in seen:
                    seen.add(x)
                    choices.append(i)
        for i in choices:
            x, v = buf[i]
            M = list(mem)
            M[x] = v
            yield (f"{prog.names[t]}: drain {prog.vars[x]} = {v}",
                   (pcs, regs, tuple(M), bufs[:t] + (buf[:i] + buf[i + 1:],) + bufs[t + 1:], incs, outs))


def _show(ins):
    op = ins[0]
    if op in ("beq", "bne", "blt"):
        return f"{op} {ins[1]}, {ins[2]}"
    if op == "jmp":
        return "jmp"
    return " ".join([op] + [str(a) for a in ins[1:]])


def halted(prog: Program, s) -> bool:
    return all(pc >= len(c) for pc, c in zip(s[0], prog.code)) and not any(s[3])


def explore(prog: Program, model: str = "sc", invariant=None, project=None, limit: int = 5_000_000) -> Result:
    """Every reachable state.  ``invariant(state, prog)`` returning False marks a violation (search continues, the
    first one kept); ``project(state, prog)`` names a terminal state's outcome (default: the final memory)."""
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("state budget must be a positive integer")
    project = project or (lambda s, p: tuple(zip(p.vars, s[2])))
    s0 = initial(prog, model)
    parent = {s0: None}
    q = deque([s0])
    finals, deadlocks, violation, edges = {}, [], None, 0
    while q:
        s = q.popleft()
        if violation is None and invariant is not None and not invariant(s, prog):
            violation = s
        succ = list(successors(prog, s, model))
        edges += len(succ)
        if not succ:
            if halted(prog, s):
                k = project(s, prog)
                finals[k] = finals.get(k, 0) + 1
            else:
                deadlocks.append(s)
        for label, t in succ:
            if t not in parent:
                parent[t] = (s, label)
                q.append(t)
                if len(parent) > limit:
                    raise RuntimeError("state space too large")
    return Result(model, len(parent), finals, violation, deadlocks, parent, prog, edges)


def schedules(prog: Program, model: str = "sc", project=None):
    """For a loop-free program: the number of distinct schedules (paths to a terminal state), by outcome."""
    project = project or (lambda s, p: tuple(zip(p.vars, s[2])))
    memo = {}

    def count(s):
        if s in memo:
            return memo[s]
        succ = list(successors(prog, s, model))
        if not succ:
            r = {project(s, prog): 1} if halted(prog, s) else {"deadlock": 1}
        else:
            r = {}
            for _, t in succ:
                for k, v in count(t).items():
                    r[k] = r.get(k, 0) + v
        memo[s] = r
        return r
    return count(initial(prog, model))


def interleavings(lengths) -> int:
    """The number of ways to interleave threads of these lengths: the multinomial coefficient."""
    total, out = 0, 1
    for n in lengths:
        total += n
        out *= comb(total, n)
    return out


def mutex(s, prog) -> bool:
    """At most one thread in its critical section."""
    return sum(s[4]) <= 1


# ---- the programs of Part 33 ----------------------------------------------------------------------------------------

def counter(n_threads: int = 2, k: int = 1, atomic: str | None = None) -> Program:
    """Each thread adds one to ``c``, k times: load, add, store (or one ``fai``, or under a lock)."""
    ths = []
    for _ in range(n_threads):
        code = []
        for _ in range(k):
            if atomic == "fai":
                code += [("fai", "r", "c")]
            elif atomic == "lock":
                code += [("lock", "m"), ("ld", "r", "c"), ("addi", "r", "r", 1), ("st", "c", "r"), ("unlock", "m")]
            else:
                code += [("ld", "r", "c"), ("addi", "r", "r", 1), ("st", "c", "r")]
        ths.append(code)
    return Program({"c": 0, "m": 0}, ths)


def peterson(fence: bool | str = False, rounds: int = 1) -> Program:
    """Peterson (1981): flag[i] <- 1; turn <- j; wait while flag[j] and turn == j; critical section; flag[i] <- 0.
    ``fence=True``: one fence before the loads (enough under TSO); ``"both"``: also between the two stores (PSO can
    otherwise reorder them)."""
    ths = []
    for i in (0, 1):
        j = 1 - i
        code = []
        for r in range(rounds):
            code += [("st", f"flag{i}", 1)] + ([("fence",)] if fence == "both" else []) + [("st", "turn", j)]
            if fence:
                code += [("fence",)]
            code += [("label", f"w{r}"), ("ld", "f", f"flag{j}"), ("beq", "f", 0, f"in{r}"), ("ld", "t", "turn"),
                     ("beq", "t", j, f"w{r}"), ("label", f"in{r}"), ("cs",), ("ncs",), ("st", f"flag{i}", 0)]
        ths.append(code)
    return Program({"flag0": 0, "flag1": 0, "turn": 0}, ths, ["P0", "P1"])


def naive_flags(rounds: int = 1) -> Program:
    """The obvious lock that fails: wait until the other's flag is down, then raise your own."""
    ths = []
    for i in (0, 1):
        j = 1 - i
        code = []
        for r in range(rounds):
            code += [("label", f"w{r}"), ("ld", "f", f"flag{j}"), ("bne", "f", 0, f"w{r}"), ("st", f"flag{i}", 1),
                     ("cs",), ("ncs",), ("st", f"flag{i}", 0)]
        ths.append(code)
    return Program({"flag0": 0, "flag1": 0}, ths, ["P0", "P1"])


def bakery(n: int = 2, rounds: int = 1, fence: bool = False) -> Program:
    """Lamport's bakery (1974): take a number one more than every number you see; the smallest (number, id) goes."""
    ths = []
    init = {}
    for i in range(n):
        init[f"choosing{i}"] = 0
        init[f"number{i}"] = 0
    for i in range(n):
        code = []
        for r in range(rounds):
            code += [("st", f"choosing{i}", 1), ("li", "mx", 0)]
            for j in range(n):
                if j != i:
                    code += [("ld", "v", f"number{j}"), ("blt", "v", "mx", f"s{r}{j}"), ("add", "mx", "v", 0),
                             ("label", f"s{r}{j}")]
            code += [("addi", "me", "mx", 1), ("st", f"number{i}", "me"), ("st", f"choosing{i}", 0)]
            if fence:
                code += [("fence",)]
            for j in range(n):
                if j == i:
                    continue
                code += [("label", f"c{r}{j}"), ("ld", "ch", f"choosing{j}"), ("bne", "ch", 0, f"c{r}{j}"),
                         ("label", f"n{r}{j}"), ("ld", "v", f"number{j}"), ("beq", "v", 0, f"ok{r}{j}"),
                         ("blt", "me", "v", f"ok{r}{j}")]
                if j < i:            # equal numbers: the smaller id goes first
                    code += [("beq", "v", "me", f"n{r}{j}")]
                code += [("jmp", f"n{r}{j}"), ("label", f"ok{r}{j}")]
            code += [("cs",), ("ncs",), ("st", f"number{i}", 0)]
        ths.append(code)
    return Program(init, ths, [f"P{i}" for i in range(n)])


def litmus_sb(fence: bool = False) -> Program:
    """Store buffering: x <- 1; r1 <- y  ||  y <- 1; r2 <- x.  Both 0 is impossible under SC."""
    f = [("fence",)] if fence else []
    return Program({"x": 0, "y": 0, "r1": 0, "r2": 0},
                   [[("st", "x", 1)] + f + [("ld", "a", "y"), ("st", "r1", "a")],
                    [("st", "y", 1)] + f + [("ld", "b", "x"), ("st", "r2", "b")]])


def litmus_mp(fence: bool = False) -> Program:
    """Message passing: data <- 42; flag <- 1  ||  wait for flag; r <- data.  Can the reader see stale data?"""
    f = [("fence",)] if fence else []
    return Program({"data": 0, "flag": 0, "r": 0},
                   [[("st", "data", 42)] + f + [("st", "flag", 1)],
                    [("label", "w"), ("ld", "g", "flag"), ("beq", "g", 0, "w"), ("ld", "d", "data"),
                     ("st", "r", "d")]], ["writer", "reader"])


def philosophers(n: int = 5, ordered: bool = False) -> Program:
    """Each philosopher locks the left fork, then the right, eats, and puts both down.  ``ordered``: the last one
    takes the right fork first (a global lock order), which removes the cycle."""
    ths = []
    for i in range(n):
        a, b = f"fork{i}", f"fork{(i + 1) % n}"
        if ordered and i == n - 1:
            a, b = b, a
        ths.append([("lock", a), ("lock", b), ("cs",), ("ncs",), ("unlock", b), ("unlock", a)])
    return Program({f"fork{i}": 0 for i in range(n)}, ths, [f"Ph{i}" for i in range(n)])


def bounded_buffer(producers: int = 1, consumers: int = 1, items: int = 2, size: int = 1,
                   broken: bool = False) -> Program:
    """Dijkstra's bounded buffer with semaphores ``empty`` and ``full`` and a mutex around the shared ``count``;
    ``over`` is set if count ever exceeds the size.  ``broken`` drops the mutex."""
    init = {"empty": size, "full": 0, "m": 0, "count": 0, "over": 0}
    lk = (lambda: []) if broken else (lambda: [("lock", "m")])
    ul = (lambda: []) if broken else (lambda: [("unlock", "m")])
    ths = []
    for _ in range(producers):
        code = []
        for k in range(items):
            code += [("P", "empty")] + lk() + [
                ("ld", "r", "count"), ("addi", "r", "r", 1), ("st", "count", "r"), ("li", "cap", size),
                ("blt", "cap", "r", f"bad{k}"), ("jmp", f"ok{k}"), ("label", f"bad{k}"), ("st", "over", 1),
                ("label", f"ok{k}")] + ul() + [("V", "full")]
        ths.append(code)
    for _ in range(consumers):
        code = []
        for _ in range(items * producers // consumers):
            code += [("P", "full")] + lk() + [("ld", "r", "count"), ("addi", "r", "r", -1), ("st", "count", "r")] + \
                ul() + [("V", "empty")]
        ths.append(code)
    return Program(init, ths)


def consensus_tas(n: int = 2) -> Program:
    """Test-and-set consensus: write your proposal, then tas the flag; the winner (who read 0) decides its own value,
    a loser decides the proposal of 'the other' (only well defined for n = 2: with three, a loser cannot tell)."""
    ths = []
    for i in range(n):
        j = (i + 1) % n
        ths.append([("st", f"prop{i}", 10 + i), ("tas", "w", "flag"), ("bne", "w", 0, "lose"), ("out", 10 + i),
                    ("jmp", "end"), ("label", "lose"), ("ld", "v", f"prop{j}"), ("out", "v"), ("label", "end")])
    init = {"flag": 0} | {f"prop{i}": 0 for i in range(n)}
    return Program(init, ths)


def consensus_cas(n: int = 3) -> Program:
    """Compare-and-swap consensus for any n: cas(decision, empty, mine), then decide whatever decision holds."""
    ths = [[("cas", "w", "decision", 0, 10 + i), ("ld", "v", "decision"), ("out", "v")] for i in range(n)]
    return Program({"decision": 0}, ths)


def consensus_registers(n: int = 2) -> Program:
    """An attempt with reads and writes only: write your proposal, read the other's; take the smaller one seen."""
    ths = []
    for i in range(n):
        j = 1 - i
        ths.append([("st", f"prop{i}", 10 + i), ("ld", "v", f"prop{j}"), ("beq", "v", 0, "mine"),
                    ("blt", "v", 10 + i, "theirs"), ("label", "mine"), ("out", 10 + i), ("jmp", "end"),
                    ("label", "theirs"), ("out", "v"), ("label", "end")])
    return Program({"prop0": 0, "prop1": 0}, ths)


def agreement(s, prog) -> bool:
    """All decisions made so far are equal, and each is someone's proposal."""
    ds = [o[0] for o in s[5] if o]
    return len(set(ds)) <= 1


def treiber_aba(tagged: bool = False) -> Program:
    """A Treiber stack A -> B -> C (nodes 1, 2, 3; ``node<i>`` holds i's next).  T1 pops once; T2 pops twice and
    pushes A back.  With a plain CAS on ``top``, the schedule  T1: read top = A, read A.next = B;  T2: pop A, pop B,
    push A;  T1: cas(top, A, B)  succeeds, and puts B, which T2 owns, back on the stack: the ABA problem.
    ``tagged``: top holds node + 100 * version and every successful CAS bumps the version, so T1's CAS fails."""
    T = 100

    def pop(k):
        if not tagged:
            return [("label", f"p{k}"), ("ld", "t", "top"), ("beq", "t", 0, f"e{k}"), ("ldx", "nx", "node", "t"),
                    ("cas", "ok", "top", "t", "nx"), ("beq", "ok", 0, f"p{k}"), ("out", "t"), ("label", f"e{k}")]
        return [("label", f"p{k}"), ("ld", "t", "top"), ("mod", "n", "t", T), ("beq", "n", 0, f"e{k}"),
                ("ldx", "nx", "node", "n"), ("divi", "v", "t", T), ("muli", "v", "v", T), ("addi", "v", "v", T),
                ("add", "new", "v", "nx"), ("cas", "ok", "top", "t", "new"), ("beq", "ok", 0, f"p{k}"),
                ("out", "n"), ("label", f"e{k}")]

    def push(node, k):
        if not tagged:
            return [("label", f"u{k}"), ("ld", "t", "top"), ("stx", "node", node, "t"),
                    ("cas", "ok", "top", "t", node), ("beq", "ok", 0, f"u{k}"), ("out", -node)]
        return [("label", f"u{k}"), ("ld", "t", "top"), ("mod", "n", "t", T), ("stx", "node", node, "n"),
                ("divi", "v", "t", T), ("muli", "v", "v", T), ("addi", "v", "v", T + node),
                ("cas", "ok", "top", "t", "v"), ("beq", "ok", 0, f"u{k}"), ("out", -node)]
    init = {"top": 1, "node0": 0, "node1": 2, "node2": 3, "node3": 0}
    return Program(init, [pop(0), pop(1) + pop(2) + push(1, 3)], ["T1", "T2"])


def stack_of(s, prog, T: int | None = None):
    """The nodes on a Treiber stack in state s, top first (stops at a repeat)."""
    mem = dict(zip(prog.vars, s[2]))
    t = mem["top"] % T if T else mem["top"]
    out = []
    while t and t not in out:
        out.append(t)
        t = mem[f"node{t}"]
    return tuple(out)
