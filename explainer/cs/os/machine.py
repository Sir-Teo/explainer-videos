"""Pebble with a kernel mode (Part 31): the hardware an operating system needs, and nothing more.

The base emulator (:mod:`explainer.cs.pebble.emu`) runs one program with the whole machine to itself.  This one adds
the privileged extension of :mod:`explainer.cs.pebble.isa`:

* a **mode bit**: the machine starts in kernel mode; ``eret`` drops to user mode;
* **control registers** (``csrr``/``csrw``, kernel only): ``status`` (bit 0 IE, interrupts enabled; bit 1 PIE and
  bit 2 PM, the IE and mode saved by the last trap), ``epc`` (where the trap happened), ``cause``, ``tval`` (the
  faulting address), ``tvec`` (where traps go), ``scratch``, ``timer``, and the bounds ``lo``/``hi``;
* **traps**: ``ecall``, an illegal or privileged instruction, a bad address, a misaligned access or a division by
  zero in user mode, and the timer, all do the same five things in one step: ``epc`` = pc, ``cause`` (and ``tval``)
  set, PIE = IE and IE = 0, PM = mode and mode = kernel, pc = ``tvec``.  ``eret`` undoes the last three;
* **protection**: in user mode every fetch, load and store must fall in [``lo``, ``hi``), and the device page is
  out of reach.  (Relocation and paging are Part 32's.)
* a **timer**: ``timer`` counts down once per instruction; reaching zero makes an interrupt pending, taken at once
  in user mode, or in kernel mode once IE is set.  Writing ``timer`` clears the pending interrupt.

A fault in kernel mode is a kernel panic: :class:`~explainer.cs.pebble.emu.MachineError`, as before.  Every trap is
recorded in ``events`` as (instruction count, cause, pc, mode), and so is every ``eret`` (cause 0, the pc it returns
to), and instructions are counted per mode (``usteps``,
``ksteps``): the measurements Part 31 draws.
"""
from __future__ import annotations

from explainer.cs.pebble.emu import Machine, MachineError, Step
from explainer.cs.pebble.isa import ALL_OPS, IO_BASE, MASK, decode

FETCH_FAULT, ILLEGAL, DIV_ZERO, MISALIGNED, LOAD_FAULT, STORE_FAULT, ECALL, TIMER = 1, 2, 3, 4, 5, 7, 8, 16
ERET = 0  # recorded in ``events`` too: the return to user mode, with the pc it returns to
CAUSES = {FETCH_FAULT: "fetch fault", ILLEGAL: "illegal instruction", DIV_ZERO: "division by zero",
          MISALIGNED: "misaligned access", LOAD_FAULT: "load fault", STORE_FAULT: "store fault", ECALL: "ecall",
          TIMER: "timer"}
STATUS, EPC, CAUSE, TVEC, SCRATCH, TIMER_CSR, TVAL, LO, HI = range(9)
IE, PIE, PM = 1, 2, 4


class Trap(Exception):
    def __init__(self, cause: int, tval: int = 0):
        super().__init__(CAUSES.get(cause, cause))
        self.cause, self.tval = cause, tval


class OSMachine(Machine):
    def __post_init__(self):
        super().__post_init__()
        self.mode = 1
        self.csr = [0] * 9
        self.pending = False
        self.usteps = 0
        self.ksteps = 0
        self.events: list[tuple[int, int, int, int]] = []

    # -- protection -------------------------------------------------------------------
    def _check(self, addr: int, size: int, cause: int) -> None:
        a = addr & MASK
        if a >= IO_BASE or not (self.csr[LO] <= a and a + size <= self.csr[HI]):
            raise Trap(cause, a)

    def load(self, addr, size, signed_=False):
        if self.mode == 0:
            self._check(addr, size, LOAD_FAULT)
            if size == 4 and addr & 3:
                raise Trap(MISALIGNED, addr & MASK)
        return super().load(addr, size, signed_)

    def store(self, addr, size, value):
        if self.mode == 0:
            self._check(addr, size, STORE_FAULT)
            if size == 4 and addr & 3:
                raise Trap(MISALIGNED, addr & MASK)
        super().store(addr, size, value)

    def _decoded(self, pc: int):
        d = self._dec.get(pc)
        if d is None:
            if pc & 3 or pc + 4 > self.mem_size:
                raise MachineError(f"bad pc {pc:#x}")
            w = self.word(pc)
            if (w >> 26) & 0x3F not in ALL_OPS:
                raise MachineError(f"illegal instruction {w:#010x} at pc {pc:#x}")
            i = decode(w)
            d = (i.op, i.rd, i.rs1, i.rs2, i.imm, w)
            self._dec[pc] = d
        return d

    # -- traps ------------------------------------------------------------------------
    def trap(self, cause: int, tval: int = 0) -> None:
        c = self.csr
        if c[TVEC] == 0 or self.mode == 1:
            raise MachineError(f"kernel panic: {CAUSES.get(cause, cause)} at pc {self.pc:#x} (tval {tval:#x})")
        self.events.append((self.steps, cause, self.pc, self.mode))
        c[EPC], c[CAUSE], c[TVAL] = self.pc, cause, tval
        s = c[STATUS]
        c[STATUS] = (PIE if s & IE else 0) | (PM if self.mode else 0)
        self.mode = 1
        self.pc = c[TVEC]

    def interrupt(self) -> None:
        """The timer: taken whatever the mode (a kernel with IE set is interrupted too)."""
        c = self.csr
        self.events.append((self.steps, TIMER, self.pc, self.mode))
        c[EPC], c[CAUSE], c[TVAL] = self.pc, TIMER, 0
        s = c[STATUS]
        c[STATUS] = (PIE if s & IE else 0) | (PM if self.mode else 0)
        self.mode = 1
        self.pending = False
        self.pc = c[TVEC]

    # -- execution --------------------------------------------------------------------
    def step(self) -> None:
        if self.halted:
            return
        c = self.csr
        if c[TIMER_CSR]:
            c[TIMER_CSR] -= 1
            if not c[TIMER_CSR]:
                self.pending = True
        if self.pending and c[TVEC] and (self.mode == 0 or c[STATUS] & IE):
            self.interrupt()
        pc = self.pc
        user = self.mode == 0
        try:
            if user:
                if pc & 3 or not (c[LO] <= pc and pc + 4 <= c[HI]):
                    raise Trap(FETCH_FAULT, pc)
                try:
                    op, rd, rs1, rs2, imm, w = self._decoded(pc)
                except MachineError:
                    raise Trap(ILLEGAL, self.word(pc)) from None
            else:
                op, rd, rs1, rs2, imm, w = self._decoded(pc)
            if op in ("ecall", "eret", "csrr", "csrw") and self.trace and (user or op != "ecall"):
                self.log.append(Step(pc, w))
            if op == "ecall":
                if not c[TVEC]:
                    raise MachineError(f"ecall with no trap vector at pc {pc:#x}")
                self.steps += 1
                self.ksteps += not user
                self.usteps += user
                self.counts["ecall"] = self.counts.get("ecall", 0) + 1
                if user:
                    self.trap(ECALL)
                else:
                    raise MachineError(f"ecall in kernel mode at pc {pc:#x}")
                return
            if op in ("eret", "csrr", "csrw") or (op == "halt" and user):
                if user:
                    raise Trap(ILLEGAL, w)
                if op == "eret":
                    self.events.append((self.steps, ERET, c[EPC], 1))
                    s = c[STATUS]
                    self.mode = 1 if s & PM else 0
                    c[STATUS] = (IE if s & PIE else 0) | PIE
                    self.pc = c[EPC]
                elif op == "csrr":
                    if rd:
                        self.regs[rd] = c[imm] & MASK
                    self.pc = pc + 4
                else:
                    c[imm] = self.regs[rs1] & MASK
                    if imm == TIMER_CSR:
                        self.pending = False
                    self.pc = pc + 4
                self.steps += 1
                self.ksteps += 1
                self.counts[op] = self.counts.get(op, 0) + 1
                return
            before = self.steps
            super().step()
            if self.steps != before:
                if user:
                    self.usteps += 1
                else:
                    self.ksteps += 1
        except Trap as t:
            self.trap(t.cause, t.tval)
        except MachineError as e:
            if not user:
                raise
            msg = str(e)
            self.trap(DIV_ZERO if "division" in msg else MISALIGNED if "misaligned" in msg else
                      LOAD_FAULT if "load" in msg else STORE_FAULT if "store" in msg else ILLEGAL)
