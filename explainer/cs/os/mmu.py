"""Pebble with an MMU (Part 32): page tables walked in hardware, cached in a TLB.

    m = VMMachine(image=kernel_image, mem_size=4 << 20)
    m.tlb_size = 16
    ... csrw ptbr, root           # translation on, in both modes, through the table at `root`

The design is RISC-V's Sv32, simplified:

* 4 KiB pages.  A virtual address is | L1 index: 10 | L2 index: 10 | offset: 12 |.
* ``ptbr`` (control register 9) holds the physical address of the root table; 0 means translation is off and the
  machine behaves exactly as Part 31's (physical addresses, bounds in user mode).
* A page-table entry is | physical page number: 20 | flags: 12 |, flags ``V`` valid, ``R``, ``W``, ``X``, ``U`` user,
  ``A`` accessed, ``D`` dirty.  An L1 entry with R or X set is a leaf: a 4 MiB **superpage**.  Otherwise it points to
  an L2 table.
* User mode may touch only ``U`` pages; kernel mode may touch any mapped page, so the kernel, mapped into every
  address space, can copy a process's buffers by their virtual addresses.  The device page is physical and kernel
  only.
* A missing or forbidden translation is a **page fault**: cause 12 (fetch), 13 (load) or 15 (store), with the
  virtual address in ``tval``.  The faulting instruction has not happened, so after the kernel fixes the mapping,
  ``eret`` runs it again.
* The hardware sets A on every access and D on every write, in the entry itself.
* The TLB is fully associative, ``tlb_size`` entries, least recently used out; writing ``ptbr`` flushes it.
  ``stats`` counts hits, misses, walks and the memory references the walks made.  With ``asid`` set, entries are
  tagged with the page table they came from and survive a switch (x86's PCID, RISC-V's ASID).
"""
from __future__ import annotations

from collections import OrderedDict

from explainer.cs.os.machine import MISALIGNED, OSMachine, Trap
from explainer.cs.pebble.emu import Machine
from explainer.cs.pebble.isa import IO_BASE, MASK

PTE_V, PTE_R, PTE_W, PTE_X, PTE_U, PTE_A, PTE_D = 1, 2, 4, 8, 16, 64, 128
PAGE_FETCH, PAGE_LOAD, PAGE_STORE = 12, 13, 15
PTBR = 9
PAGE = 4096
READ, WRITE, EXEC = 0, 1, 2
NEED = (PTE_R, PTE_W, PTE_X)
FAULT = (PAGE_LOAD, PAGE_STORE, PAGE_FETCH)


def pte(pa: int, flags: int) -> int:
    return ((pa >> 12) << 12) | flags


class VMMachine(OSMachine):
    def __post_init__(self):
        super().__post_init__()
        self.csr = [0] * 10
        self.tlb: OrderedDict = OrderedDict()
        self.tlb_size = 16
        self.stats = {"tlb_hits": 0, "tlb_misses": 0, "walks": 0, "walk_refs": 0, "flushes": 0, "mmu_faults": 0}
        self.asid = False          # True: TLB entries are tagged with their page table, and not flushed
        self._fmemo = (None, None, None, None)

    # -- the MMU ----------------------------------------------------------------------
    def _csr_written(self, i: int) -> None:
        if i == PTBR and not self.asid:
            self.tlb.clear()
            self.stats["flushes"] += 1

    @staticmethod
    def _ok(fl: int, kind: int, user: bool) -> bool:
        return bool(fl & NEED[kind]) and (not user or bool(fl & PTE_U))

    def walk(self, va: int) -> tuple[int, int, int, bool]:
        """(entry, its physical address, references made, superpage?) for va, without faulting."""
        root = self.csr[PTBR]
        a1 = root + ((va >> 22) << 2)
        e = self.word(a1)
        if e & PTE_V and not e & (PTE_R | PTE_X):
            a2 = ((e >> 12) << 12) + (((va >> 12) & 0x3FF) << 2)
            return self.word(a2), a2, 2, False
        return e, a1, 1, True

    def translate(self, va: int, kind: int) -> int:
        va &= MASK
        vpn = va >> 12
        key = (self.csr[PTBR], vpn) if self.asid else vpn
        user = self.mode == 0
        t = self.tlb.get(key)
        if t is not None:
            ppn, fl = t
            if self._ok(fl, kind, user) and (kind != WRITE or fl & PTE_D):
                self.tlb.move_to_end(key)
                self.stats["tlb_hits"] += 1
                return (ppn << 12) | (va & 0xFFF)
        self.stats["tlb_misses"] += 1
        self.stats["walks"] += 1
        e, addr, refs, big = self.walk(va)
        self.stats["walk_refs"] += refs
        if not e & PTE_V or not self._ok(e, kind, user):
            self.stats["mmu_faults"] += 1
            raise Trap(FAULT[kind], va)
        new = e | PTE_A | (PTE_D if kind == WRITE else 0)
        if new != e:
            self.mem[addr:addr + 4] = new.to_bytes(4, "little")
        ppn = ((e >> 12) | (vpn & 0x3FF)) if big else (e >> 12)
        self.tlb[key] = (ppn, new)
        self.tlb.move_to_end(key)
        if len(self.tlb) > self.tlb_size:
            self.tlb.popitem(last=False)
        return (ppn << 12) | (va & 0xFFF)

    # -- memory through the MMU ---------------------------------------------------------
    def _mapped(self, addr: int) -> bool:
        return bool(self.csr[PTBR]) and (self.mode == 0 or (addr & MASK) < IO_BASE)

    def load(self, addr, size, signed_=False):
        if self._mapped(addr):
            if size == 4 and addr & 3:
                raise Trap(MISALIGNED, addr & MASK)
            return Machine.load(self, self.translate(addr, READ), size, signed_)
        return super().load(addr, size, signed_)

    def store(self, addr, size, value):
        if self._mapped(addr):
            if size == 4 and addr & 3:
                raise Trap(MISALIGNED, addr & MASK)
            Machine.store(self, self.translate(addr, WRITE), size, value)
            return
        super().store(addr, size, value)

    def _decoded(self, pc: int):
        if self.csr[PTBR]:
            m = self._fmemo
            if m[0] == pc and m[1] == self.steps and m[2] == self.mode:
                pa = m[3]
            else:
                pa = self.translate(pc, EXEC)
                self._fmemo = (pc, self.steps, self.mode, pa)
            return OSMachine._decoded(self, pa)
        return super()._decoded(pc)
