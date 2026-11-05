"""The reference VM for the λ-core's bytecode (Part 15), with pluggable garbage collectors.

    prog = bytecode.job_program()
    vm = VM(prog, Cheney(semispace=20000), tape=text)
    vm.run()
    vm.output, vm.stats, vm.heap.log      # what it printed, what it did, one record per collection

Every collector manages the same word-addressed memory (``heap.mem``) and sees the same roots: the whole VM stack
(return addresses and saved frame pointers are tagged integers, so the stack can be scanned blindly) and the
globals.  An allocation first calls :meth:`reserve`, while its operands are still on the stack, so a collection that
moves objects updates them too; only then are the operands popped and the object written.

Collectors:

* :class:`Cheney` (1970): two semispaces; a breadth-first copy with a *scan* and a *free* pointer and no stack.
* :class:`MarkSweep` (McCarthy 1960): mark from the roots with an explicit stack, then sweep the whole heap onto
  free lists by size; objects never move.
* :class:`MarkCompact`: mark, then Lisp 2's three passes (compute new addresses, update pointers, slide).
* :class:`Generational` (Lieberman and Hewitt 1983, Ungar 1984): a nursery collected by copying its survivors
  into an old space, which is collected (by copying) only when it fills.  The λ-core never writes into an existing
  object, so no old object can point at a young one and the remembered set stays empty; :attr:`barrier_hits`
  counts the stores a write barrier would have had to check (zero).

Each collector keeps :attr:`log`: one dict per collection with the allocation clock (words allocated so far), the
live words found, and the words of work done (copied, marked, swept or slid).
"""
from __future__ import annotations

from collections import Counter

from explainer.cs.runtime.bytecode import CLOS, CONS, FWD, OP, OPS, PAIR, PAP, TRUE, FALSE, UNIT

for _name, _k in OP.items():
    globals()["_" + _name] = _k


class OutOfMemory(RuntimeError):
    pass


class VMError(RuntimeError):
    pass


def _ptr(v):
    return v != 0 and not v & 1


class Collector:
    name = "collector"

    def __init__(self):
        self.log: list[dict] = []
        self.clock = 0            # words allocated so far
        self.vm = None
        self.track_ages = False
        self.birth = None

    def roots(self):
        vm = self.vm
        return vm.stack, vm.sp, vm.globals

    def words_in_use(self) -> int:
        raise NotImplementedError


class Cheney(Collector):
    name = "copying (Cheney)"

    def __init__(self, semispace: int = 1 << 16, track_ages=False):
        super().__init__()
        self.S = semispace
        self.mem = [0] * (1 + 2 * semispace)
        self.base = 1
        self.free = 1
        self.limit = 1 + semispace
        self.track_ages = track_ages
        self.birth = [0] * len(self.mem) if track_ages else None
        self.lifetimes: list[int] = []   # per object, the age at which it was last seen alive (0: never)
        self.ids = [0] * len(self.mem) if track_ages else None
        self.seen: dict[int, int] = {}

    def reserve(self, n):
        if self.free + n > self.limit:
            self.collect()
            if self.free + n > self.limit:
                raise OutOfMemory(f"{self.free - self.base + n} words needed, semispace {self.S}")

    def alloc(self, hdr, fields):
        a = self.free
        mem = self.mem
        mem[a] = hdr
        n = len(fields)
        mem[a + 1:a + 1 + n] = fields
        self.free = a + 1 + n
        self.clock += 1 + n
        if self.track_ages:
            self.birth[a] = self.clock
            oid = len(self.lifetimes)
            self.lifetimes.append(0)
            self.ids[a] = oid
        return a

    def collect(self):
        mem = self.mem
        to = 1 + self.S if self.base == 1 else 1
        free = to
        lo, hi = self.base, self.base + self.S
        birth, ids, track = self.birth, self.ids, self.track_ages

        def forward(v):
            nonlocal free
            if v & 1 or v == 0:
                return v
            a = v >> 1
            h = mem[a]
            if h & 15 == FWD:
                return mem[a + 1]
            n = h >> 4
            mem[free:free + 1 + n] = mem[a:a + 1 + n]
            if track:
                birth[free] = birth[a]
                ids[free] = ids[a]
            mem[a] = FWD
            nv = free << 1
            mem[a + 1] = nv
            free += 1 + n
            return nv

        stack, sp, gl = self.roots()
        roots = 0
        for i in range(sp):
            v = stack[i]
            if _ptr(v):
                roots += 1
                stack[i] = forward(v)
        for i, v in enumerate(gl):
            if _ptr(v):
                roots += 1
                gl[i] = forward(v)
        scan = to
        while scan < free:
            n = mem[scan] >> 4
            for j in range(scan + 1, scan + 1 + n):
                v = mem[j]
                if v and not v & 1:
                    mem[j] = forward(v)
            scan += 1 + n
        live = free - to
        if track:
            p = to
            while p < free:
                age = self.clock - birth[p]
                oid = ids[p]
                if age > self.lifetimes[oid]:
                    self.lifetimes[oid] = age
                p += 1 + (mem[p] >> 4)
        self.log.append({"clock": self.clock, "live": live, "work": live, "roots": roots, "kind": "full"})
        self.base, self.free, self.limit = to, free, to + self.S

    def words_in_use(self):
        return self.free - self.base


class MarkSweep(Collector):
    """Non-moving: free lists by size; a sweep visits every object, live or dead."""
    name = "mark–sweep"

    def __init__(self, heap: int = 1 << 17):
        super().__init__()
        self.H = heap
        self.mem = [0] * (1 + heap)
        self.top = 1                 # bump pointer into never-used memory
        self.freelists: dict[int, list] = {}
        self.marks = bytearray(1 + heap)
        self.in_use = 0

    def _take(self, n):
        fl = self.freelists.get(n)
        if fl:
            return fl.pop()
        if self.top + n <= 1 + self.H:
            a = self.top
            self.top += n
            return a
        return None

    def reserve(self, n):
        self._pending = self._take(n)
        if self._pending is None:
            self.collect()
            self._pending = self._take(n)
            if self._pending is None:
                raise OutOfMemory(f"no block of {n} words in a heap of {self.H}")

    def alloc(self, hdr, fields):
        a = self._pending
        mem = self.mem
        mem[a] = hdr
        n = len(fields)
        mem[a + 1:a + 1 + n] = fields
        self.clock += 1 + n
        self.in_use += 1 + n
        return a

    def mark(self):
        mem, marks = self.mem, self.marks
        stack, sp, gl = self.roots()
        todo = [v >> 1 for v in list(stack[:sp]) + list(gl) if _ptr(v)]
        live = 0
        while todo:
            a = todo.pop()
            if marks[a]:
                continue
            marks[a] = 1
            n = mem[a] >> 4
            live += 1 + n
            for j in range(a + 1, a + 1 + n):
                v = mem[j]
                if v and not v & 1 and not marks[v >> 1]:
                    todo.append(v >> 1)
        return live

    def collect(self):
        live = self.mark()
        mem, marks = self.mem, self.marks
        self.freelists = {}
        p, swept = 1, 0
        while p < self.top:
            h = mem[p]
            n = h >> 4
            size = 1 + n
            if marks[p]:
                marks[p] = 0
            else:
                mem[p] = (n << 4) | 0        # a free block keeps its size, kind 0
                self.freelists.setdefault(size, []).append(p)
            swept += 1
            p += size
        self.in_use = live
        frag = sum(len(v) * k for k, v in self.freelists.items())
        self.log.append({"clock": self.clock, "live": live, "work": live + swept, "kind": "full",
                         "free_blocks": sum(len(v) for v in self.freelists.values()), "free_words": frag})

    def words_in_use(self):
        return self.in_use


class MarkCompact(MarkSweep):
    """Mark, then slide every live object down (Lisp 2): allocation is a bump pointer again."""
    name = "mark–compact"

    def reserve(self, n):
        if self.top + n > 1 + self.H:
            self.collect()
            if self.top + n > 1 + self.H:
                raise OutOfMemory(f"{n} words needed in a heap of {self.H}")
        self._pending = self.top
        self.top += n

    def collect(self):
        live = self.mark()
        mem, marks = self.mem, self.marks
        new = {}
        p, dst = 1, 1
        while p < self.top:                      # pass 1: forwarding addresses
            size = 1 + (mem[p] >> 4)
            if marks[p]:
                new[p] = dst
                dst += size
            p += size

        def fw(v):
            return new[v >> 1] << 1 if v and not v & 1 else v
        stack, sp, gl = self.roots()             # pass 2: update every pointer
        for i in range(sp):
            stack[i] = fw(stack[i])
        for i in range(len(gl)):
            gl[i] = fw(gl[i])
        for a in new:
            n = mem[a] >> 4
            for j in range(a + 1, a + 1 + n):
                mem[j] = fw(mem[j])
        moved = 0
        for a, d in new.items():                 # pass 3: slide (in address order, so never overwrites)
            size = 1 + (mem[a] >> 4)
            if a != d:
                mem[d:d + size] = mem[a:a + size]
                moved += size
            marks[a] = 0
        self.top = dst
        self.in_use = live
        swept = len(new)
        self.log.append({"clock": self.clock, "live": live, "work": 2 * live + moved, "moved": moved, "kind": "full"})


class Generational(Collector):
    """A nursery collected by copying survivors straight into the old space; the old space is itself a pair of
    semispaces collected by Cheney when it fills."""
    name = "generational"

    def __init__(self, nursery: int = 4096, old: int = 1 << 16):
        super().__init__()
        self.N, self.O = nursery, old
        # [1, 1+N) nursery; then two old semispaces
        self.mem = [0] * (1 + nursery + 2 * old)
        self.nfree = 1
        self.obase = 1 + nursery
        self.ofree = self.obase
        self.barrier_hits = 0
        self.promoted = 0

    def reserve(self, n):
        if self.nfree + n > 1 + self.N:
            self.minor()
            if self.nfree + n > 1 + self.N:
                raise OutOfMemory("object larger than the nursery")

    def alloc(self, hdr, fields):
        a = self.nfree
        mem = self.mem
        mem[a] = hdr
        n = len(fields)
        mem[a + 1:a + 1 + n] = fields
        self.nfree = a + 1 + n
        self.clock += 1 + n
        return a

    def _copy_into(self, in_from, dst_free, dst_limit, scan_start):
        """Cheney from the region in_from(a) into [dst_free, ...); returns the new free pointer."""
        mem = self.mem
        free = dst_free

        def forward(v):
            nonlocal free
            if v & 1 or v == 0:
                return v
            a = v >> 1
            if not in_from(a):
                return v
            h = mem[a]
            if h & 15 == FWD:
                return mem[a + 1]
            n = h >> 4
            if free + 1 + n > dst_limit:
                raise OutOfMemory("old space full during promotion")
            mem[free:free + 1 + n] = mem[a:a + 1 + n]
            mem[a] = FWD
            nv = free << 1
            mem[a + 1] = nv
            free += 1 + n
            return nv
        stack, sp, gl = self.roots()
        for i in range(sp):
            v = stack[i]
            if _ptr(v):
                stack[i] = forward(v)
        for i, v in enumerate(gl):
            if _ptr(v):
                gl[i] = forward(v)
        scan = scan_start
        while scan < free:
            n = mem[scan] >> 4
            for j in range(scan + 1, scan + 1 + n):
                v = mem[j]
                if v and not v & 1:
                    mem[j] = forward(v)
            scan += 1 + n
        return free

    def minor(self):
        limit = self.obase + self.O
        if self.ofree + self.N > limit:          # might not fit: collect the old space first
            self.major()
            limit = self.obase + self.O
        start = self.ofree
        nlim = 1 + self.N
        self.ofree = self._copy_into(lambda a: a < nlim, self.ofree, limit, start)
        moved = self.ofree - start
        self.promoted += moved
        self.nfree = 1
        self.log.append({"clock": self.clock, "live": moved, "work": moved, "kind": "minor"})

    def major(self):
        """Copy the nursery's and the old space's live objects into the other old semispace."""
        other = 1 + self.N + self.O if self.obase == 1 + self.N else 1 + self.N
        lo, hi = self.obase, self.obase + self.O
        nlim = 1 + self.N
        start = other
        free = self._copy_into(lambda a: a < nlim or lo <= a < hi, other, other + self.O, start)
        self.obase, self.ofree = other, free
        self.nfree = 1
        self.log.append({"clock": self.clock, "live": free - start, "work": free - start, "kind": "major"})

    def words_in_use(self):
        return (self.nfree - 1) + (self.ofree - self.obase)


class VM:
    def __init__(self, prog, heap: Collector, tape: bytes = b"", stack_size: int = 1 << 18, tco: bool = True,
                 count_rc: bool = False):
        self.prog = prog
        self.heap = heap
        heap.vm = self
        self.tape = tape
        self.tpos = 0
        self.output = bytearray()
        self.stack = [0] * stack_size
        self.sp = 0
        self.globals = [0] * len(prog.globals)
        self.tco = tco
        self.stats = Counter()
        self.max_sp = 0
        self.count_rc = count_rc

    def _eq(self, a, b):
        mem = self.heap.mem
        while True:
            if a == b:
                return True
            if not (_ptr(a) and _ptr(b)):
                return False
            pa, pb = a >> 1, b >> 1
            ha, hb = mem[pa], mem[pb]
            if ha != hb:
                return False
            n = ha >> 4
            for j in range(1, n):
                if not self._eq(mem[pa + j], mem[pb + j]):
                    return False
            a, b = mem[pa + n], mem[pb + n]       # the last field (a list's tail) iteratively

    def _unfit(self, f, n):
        mem = self.heap.mem
        fa = f >> 1
        return mem[fa] & 15 == PAP or self.prog.fns[mem[fa + 1] >> 1].arity != n

    def run(self, max_ops: int = 10 ** 9):
        prog, heap = self.prog, self.heap
        code = prog.code
        fns = prog.fns
        stack, gl = self.stack, self.globals
        st = self.stats
        ops = Counter()
        pc = prog.main.entry
        bp = 0
        sp = prog.main.nlocals
        for i in range(sp):
            stack[i] = 1
        mem = heap.mem
        n_ops = 0
        max_sp = 0
        tco = self.tco
        rc = self.count_rc
        rc_stack = rc_heap = 0
        while True:
            op, arg = code[pc]
            pc += 1
            ops[op] += 1
            n_ops += 1
            if op == _LOCAL:
                v = stack[bp + arg]
                stack[sp] = v
                sp += 1
                if rc and v and not v & 1:
                    rc_stack += 1
            elif op == _SETLOCAL:
                sp -= 1
                stack[bp + arg] = stack[sp]
            elif op == _CONST:
                stack[sp] = arg
                sp += 1
            elif op == _FREE:
                v = mem[(stack[bp - 1] >> 1) + 2 + arg]
                stack[sp] = v
                sp += 1
                if rc and v and not v & 1:
                    rc_stack += 1
            elif op == _GLOBAL:
                v = gl[arg]
                stack[sp] = v
                sp += 1
                if rc and v and not v & 1:
                    rc_stack += 1
            elif op == _JF:
                sp -= 1
                if stack[sp] == FALSE:
                    pc = arg
            elif op == _JMP:
                pc = arg
            elif op == _JNIL:
                sp -= 1
                if stack[sp] == 0:
                    pc = arg
            elif op == _HEAD:
                stack[sp - 1] = mem[(stack[sp - 1] >> 1) + 1]
            elif op == _TAIL:
                stack[sp - 1] = mem[(stack[sp - 1] >> 1) + 2]
            elif op == _FST:
                stack[sp - 1] = mem[(stack[sp - 1] >> 1) + 1]
            elif op == _SND:
                stack[sp - 1] = mem[(stack[sp - 1] >> 1) + 2]
            elif op in (_CONS, _PAIR):
                self.sp = sp
                heap.reserve(3)
                mem = heap.mem
                a = heap.alloc((2 << 4) | (CONS if op == _CONS else PAIR), (stack[sp - 2], stack[sp - 1]))
                sp -= 2
                stack[sp] = a << 1
                sp += 1
                if rc:
                    rc_heap += sum(1 for v in mem[a + 1:a + 3] if v and not v & 1)
            elif op == _ADD:
                sp -= 1
                stack[sp - 1] = stack[sp - 1] + stack[sp] - 1
            elif op == _SUB:
                sp -= 1
                stack[sp - 1] = stack[sp - 1] - stack[sp] + 1
            elif op == _MUL:
                sp -= 1
                stack[sp - 1] = 2 * ((stack[sp - 1] >> 1) * (stack[sp] >> 1)) + 1
            elif op == _DIV or op == _MOD:
                sp -= 1
                x, y = stack[sp - 1] >> 1, stack[sp] >> 1
                q = abs(x) // abs(y) * (1 if (x >= 0) == (y >= 0) else -1)
                stack[sp - 1] = 2 * (q if op == _DIV else x - y * q) + 1
            elif op == _EQ or op == _NE:
                sp -= 1
                r = self._eq(stack[sp - 1], stack[sp])
                stack[sp - 1] = TRUE if r == (op == _EQ) else FALSE
            elif op == _LT:
                sp -= 1
                stack[sp - 1] = TRUE if stack[sp - 1] < stack[sp] else FALSE
            elif op == _LE:
                sp -= 1
                stack[sp - 1] = TRUE if stack[sp - 1] <= stack[sp] else FALSE
            elif op == _GT:
                sp -= 1
                stack[sp - 1] = TRUE if stack[sp - 1] > stack[sp] else FALSE
            elif op == _GE:
                sp -= 1
                stack[sp - 1] = TRUE if stack[sp - 1] >= stack[sp] else FALSE
            elif op == _NOT:
                stack[sp - 1] = TRUE if stack[sp - 1] == FALSE else FALSE
            elif op == _CALL or (op == _TAILCALL and (not tco or self._unfit(stack[sp - (arg & 0xFF) - 1], arg & 0xFF))):
                n = arg & 0xFF
                f = stack[sp - n - 1]
                fa = f >> 1
                h = mem[fa]
                if h & 15 == PAP:
                    # spread the partial application's arguments under the new ones
                    k = (h >> 4) - 1
                    clo = mem[fa + 1]
                    extra = mem[fa + 2:fa + 2 + k]
                    args = stack[sp - n:sp]
                    sp -= n + 1
                    stack[sp] = clo
                    stack[sp + 1:sp + 1 + k] = extra
                    stack[sp + 1 + k:sp + 1 + k + n] = args
                    sp += 1 + k + n
                    n += k
                    f = clo
                    fa = f >> 1
                    st["pap_calls"] += 1
                fn = fns[mem[fa + 1] >> 1]
                if fn.arity > n:
                    self.sp = sp
                    heap.reserve(2 + n)
                    mem = heap.mem
                    a = heap.alloc(((1 + n) << 4) | PAP, tuple(stack[sp - n - 1:sp]))
                    sp -= n + 1
                    stack[sp] = a << 1
                    sp += 1
                    st["paps"] += 1
                    continue
                if fn.arity < n:
                    raise VMError("over-application at run time")
                nbp = sp - n
                for i in range(fn.nlocals - n):
                    stack[sp + i] = 1
                sp = nbp + fn.nlocals
                stack[sp] = 2 * bp + 1
                stack[sp + 1] = 2 * pc + 1
                sp += 2
                bp = nbp
                pc = fn.entry
                st["calls"] += 1
                if sp > max_sp:
                    max_sp = sp
            elif op == _TAILCALL:
                n = arg & 0xFF
                cur_nl = arg >> 8
                f = stack[sp - n - 1]
                fa = f >> 1
                fn = fns[mem[fa + 1] >> 1]
                saved_bp, ret = stack[bp + cur_nl], stack[bp + cur_nl + 1]
                stack[bp - 1:bp + n] = stack[sp - n - 1:sp]
                sp = bp + n
                for i in range(fn.nlocals - n):
                    stack[sp + i] = 1
                sp = bp + fn.nlocals
                stack[sp] = saved_bp
                stack[sp + 1] = ret
                sp += 2
                pc = fn.entry
                st["tailcalls"] += 1
            elif op == _RET:
                v = stack[sp - 1]
                saved_bp, ret = stack[bp + arg], stack[bp + arg + 1]
                sp = bp - 1
                stack[sp] = v
                sp += 1
                bp = saved_bp >> 1
                pc = ret >> 1
            elif op == _CLOSURE:
                idx, nf = arg & 0xFFFF, arg >> 16
                self.sp = sp
                heap.reserve(2 + nf)
                mem = heap.mem
                a = heap.alloc(((1 + nf) << 4) | CLOS, (2 * idx + 1,) + tuple(stack[sp - nf:sp]))
                sp -= nf
                stack[sp] = a << 1
                sp += 1
                st["closures"] += 1
            elif op == _SELF:
                stack[sp] = stack[bp - 1]
                sp += 1
            elif op == _SETGLOBAL:
                sp -= 1
                gl[arg] = stack[sp]
            elif op == _POP:
                sp -= 1
            elif op == _GETC:
                if self.tpos < len(self.tape):
                    c = self.tape[self.tpos]
                    self.tpos += 1
                else:
                    c = -1
                stack[sp] = 2 * c + 1
                sp += 1
            elif op == _PUTC:
                self.output.append((stack[sp - 1] >> 1) & 255)
                stack[sp - 1] = UNIT
            elif op == _HALT:
                break
            else:
                raise VMError(f"bad opcode {op} at {pc - 1}")
            if n_ops >= max_ops:
                raise VMError("too many steps")
        self.sp = sp
        self.max_sp = max(max_sp, self.max_sp)
        st["ops"] = n_ops
        st["max_stack"] = max_sp
        if rc:
            st["rc_stack"] = rc_stack
            st["rc_heap"] = rc_heap
        self.ops = {OPS[k]: v for k, v in ops.items()}
        return self
