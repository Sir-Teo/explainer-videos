"""Trap and emulate (Part 32, chapter 12): Part 31's PebbleOS, unmodified, as a guest in user mode.

    m = VirtMachine(image=kernel.image, tape=..., mem_size=...)   # then load the processes, as kernel.boot does
    m.run(); m.exits                                             # what the hypervisor had to do, by kind

Popek and Goldberg (1974): a machine can be virtualized by trap-and-emulate if every **sensitive** instruction (one
that reads or changes the machine's mode, its control state or its devices) is **privileged** (traps in user mode).
Pebble's are: ``csrr``, ``csrw``, ``eret`` and ``halt`` trap in user mode, and so does any touch of the device page.
So the hypervisor runs the guest kernel in user mode too, and keeps the guest's view of the machine itself:

* ``vmode`` (the mode the guest believes it is in) and ``vcsr`` (its control registers);
* a trap from the guest **kernel** is an instruction to emulate: a control-register read or write, an ``eret``
  (which switches the real bounds to the guest process's), a ``halt``, or a load or store to a device;
* a trap from a guest **process** (a system call, a fault, the timer) is *reflected*: the hypervisor does to the
  virtual state what the hardware would have done (save the pc, set the cause, enter "kernel mode") and jumps to the
  guest kernel's trap vector;
* the guest's timer is the real timer; if it fires while the guest kernel has interrupts off, it is held until the
  guest returns to a process.

Every emulated instruction counts as one guest instruction, so the guest executes exactly the instructions it would
natively; ``exits`` counts the trips into the hypervisor.
"""
from __future__ import annotations

from explainer.cs.os.machine import (CAUSE, ECALL, EPC, ERET, HI, IE, ILLEGAL, LO, LOAD_FAULT, PIE, PM, STATUS,
                                     STORE_FAULT, TIMER, TIMER_CSR, TVAL, TVEC, OSMachine)
from explainer.cs.pebble.emu import Machine, MachineError
from explainer.cs.pebble.isa import IO_BASE, MASK, decode, sext


class VirtMachine(OSMachine):
    def __post_init__(self):
        super().__post_init__()
        self.mode = 0                  # really: always user mode
        self.vmode = 1                 # what the guest believes
        self.vcsr = [0] * 9
        self.vpending = False
        self.csr[TVEC] = 1             # the hypervisor's own entry (any non-zero: it is Python)
        self.csr[LO], self.csr[HI] = 0, self.mem_size
        self.exits = {"csr": 0, "eret": 0, "halt": 0, "device": 0, "ecall": 0, "timer": 0, "fault": 0}

    def _bounds(self):
        c = self.csr
        if self.vmode:
            c[LO], c[HI] = 0, self.mem_size
        else:
            c[LO], c[HI] = self.vcsr[LO], self.vcsr[HI]

    def reflect(self, cause: int, tval: int = 0) -> None:
        """Deliver a trap to the guest kernel, as Pebble's hardware would."""
        v = self.vcsr
        self.events.append((self.steps, cause, self.pc, self.vmode))
        v[EPC], v[CAUSE], v[TVAL] = self.pc, cause, tval
        s = v[STATUS]
        v[STATUS] = (PIE if s & IE else 0) | (PM if self.vmode else 0)
        self.vmode = 1
        self.pc = v[TVEC]
        self._bounds()

    def interrupt(self) -> None:
        self.pending = False
        if self.vmode == 0 or self.vcsr[STATUS] & IE:
            self.exits["timer"] += 1
            self.reflect(TIMER)
        else:
            self.vpending = True

    def trap(self, cause: int, tval: int = 0) -> None:
        if self.vmode == 0:
            self.exits["ecall" if cause == ECALL else "fault"] += 1
            self.reflect(cause, tval)
            return
        pc = self.pc
        w = self.word(pc)
        i = decode(w)
        R = self.regs
        if cause == ILLEGAL and i.op in ("csrr", "csrw", "eret", "halt"):
            v = self.vcsr
            if i.op == "csrr":
                if i.rd:
                    R[i.rd] = v[i.imm] & MASK
                self.pc = pc + 4
                self.exits["csr"] += 1
            elif i.op == "csrw":
                val = R[i.rs1] & MASK
                v[i.imm] = val
                if i.imm == TIMER_CSR:
                    self.csr[TIMER_CSR] = val
                    self.pending = self.vpending = False
                self.pc = pc + 4
                self.exits["csr"] += 1
            elif i.op == "eret":
                self.exits["eret"] += 1
                self.events.append((self.steps, ERET, v[EPC], 1))
                s = v[STATUS]
                self.vmode = 1 if s & PM else 0
                v[STATUS] = (IE if s & PIE else 0) | PIE
                self.pc = v[EPC]
                self._bounds()
            else:
                self.exits["halt"] += 1
                self.halted = True
            self.steps += 1
            self.ksteps += 1
            if i.op == "eret" and self.vmode == 0 and self.vpending:
                self.vpending = False
                self.exits["timer"] += 1
                self.reflect(TIMER)
            return
        if cause in (LOAD_FAULT, STORE_FAULT) and tval >= IO_BASE:
            addr = (R[i.rs1] + i.imm) & MASK
            if i.op in ("lw", "lb", "lbu"):
                val = Machine.load(self, addr, 4 if i.op == "lw" else 1, signed_=i.op == "lb")
                if i.rd:
                    R[i.rd] = val & MASK
            else:
                Machine.store(self, addr, 4 if i.op == "sw" else 1, R[i.rs2])
            self.pc = pc + 4
            self.steps += 1
            self.ksteps += 1
            self.exits["device"] += 1
            return
        raise MachineError(f"guest kernel panic: cause {cause} at pc {pc:#x} (tval {tval:#x})")


def boot_virt(procs, tape: bytes = b"", quantum: int | None = None) -> VirtMachine:
    """Part 31's kernel and processes, exactly as kernel.boot builds them, on the hypervisor."""
    from explainer.cs.os import kernel as K
    from explainer.cs.pebble.asm import assemble
    k = assemble(K.kernel_source(procs, quantum or K.QUANTUM))
    m = VirtMachine(image=k.image, tape=tape, mem_size=K.MEM)
    for p in procs:
        m.mem[p.lo:p.lo + len(p.image)] = p.image
    m.kernel, m.procs = k, procs
    return m


del sext
