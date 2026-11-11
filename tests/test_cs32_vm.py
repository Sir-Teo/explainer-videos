"""Part 32's instruments: Pebble's MMU, paged PebbleOS, replacement policies, allocators and trap-and-emulate."""
from __future__ import annotations

import random
import unittest

from explainer.cs.os import kernel as K
from explainer.cs.os import paging as P
from explainer.cs.os import virt as Vt
from explainer.cs.os import vmos as V
from explainer.cs.os.mmu import PAGE_STORE, PTE_R, PTE_U, PTE_V, PTE_W, PTE_X, VMMachine, pte
from explainer.cs.os.machine import Trap
from videos.cs.cs32.compute import CELL, CODEWRITE, GROWER, KREAD, SAMEVA, WILD


class TestMMU(unittest.TestCase):
    def test_invalid_write_only_entries_and_superpage_alignment(self):
        for root_entry in (False, True):
            m, frame = self.machine()
            m.mode = 0
            addr = 0x10004 if root_entry else 0x11000
            m.mem[addr:addr + 4] = pte(frame, PTE_V | PTE_W | PTE_U).to_bytes(4, "little")
            with self.assertRaises(Trap) as cm:
                m.store(0x400000, 4, 1)
            self.assertEqual(cm.exception.cause, PAGE_STORE)
        m, frame = self.machine()
        m.mode = 0
        m.mem[0x10004:0x10008] = pte(frame, PTE_V | PTE_R | PTE_W | PTE_U).to_bytes(4, "little")
        with self.assertRaises(Trap):
            m.load(0x400000, 4)  # a 4 MiB superpage cannot start at physical 128 KiB

    def machine(self):
        m = VMMachine(image=b"", mem_size=1 << 20)
        root, l2, frame = 0x10000, 0x11000, 0x20000
        m.mem[root + 4:root + 8] = pte(l2, PTE_V).to_bytes(4, "little")            # VA 4 MiB .. 8 MiB
        m.mem[l2:l2 + 4] = pte(frame, PTE_V | PTE_R | PTE_U).to_bytes(4, "little")   # VA 0x400000: read-only
        m.mem[root:root + 4] = pte(0, PTE_V | PTE_R | PTE_W | PTE_X).to_bytes(4, "little")  # superpage, kernel
        m.csr[9] = root
        return m, frame

    def test_translate_and_tlb(self):
        m, frame = self.machine()
        m.mode = 0
        m.mem[frame + 8:frame + 12] = (1234).to_bytes(4, "little")
        self.assertEqual(m.load(0x400008, 4), 1234)
        self.assertEqual(m.load(0x400008, 4), 1234)
        self.assertEqual((m.stats["tlb_misses"], m.stats["tlb_hits"]), (1, 1))
        self.assertEqual(m.stats["walk_refs"], 2)
        with self.assertRaises(Trap) as cm:
            m.store(0x400008, 4, 1)
        self.assertEqual(cm.exception.cause, PAGE_STORE)
        with self.assertRaises(Trap):
            m.load(0x100, 4)                      # the kernel's superpage has no U bit

    def test_superpage_and_accessed(self):
        m, frame = self.machine()
        m.mode = 1
        m.mem[0x1234:0x1238] = (99).to_bytes(4, "little")
        self.assertEqual(m.load(0x1234, 4), 99)
        m.mode = 0
        m.load(0x400000, 4)
        self.assertTrue(m.word(0x11000) & 64)      # A set by the walk


class TestPagedOS(unittest.TestCase):
    def test_same_virtual_address(self):
        m = V.boot_vm([V.user_asm_vm("a", SAMEVA, data=CELL), V.user_asm_vm("b", SAMEVA, data=CELL)])
        m.run(1_000_000)
        self.assertEqual(sorted(bytes(m.output).split()), [b"1", b"2"])

    def test_faults(self):
        procs = [V.user_asm_vm("w", CODEWRITE), V.user_asm_vm("x", WILD), V.user_asm_vm("k", KREAD),
                 V.user_asm_vm("g", GROWER)]
        m = V.boot_vm(procs)
        m.run(5_000_000)
        r = V.report_vm(m)
        self.assertEqual([p["exit"] for p in r["procs"]], [-15, -13, -13, 0])
        self.assertEqual(r["page_faults"], 16)
        self.assertEqual(bytes(m.output), b"G\n")

    def test_pipeline(self):
        from explainer.cs.algo import job2 as J
        from explainer.cs.pebble import programs as PR
        from videos.cs.cs31.compute import TOK
        t = PR.job_tape("It was the best of times, it was the worst of times; it was THE age of wisdom. " * 40)
        m = V.boot_vm([V.user_vm("tok", TOK, stdout="pipe"), V.user_vm("job", J.JOB_HASH, stdin="pipe")], tape=t)
        m.run(50_000_000)
        self.assertEqual(bytes(m.output), PR.job_reference(t))


class TestReplacement(unittest.TestCase):
    def test_zero_frames_fault_on_every_reference(self):
        for policy in P.FAULTS:
            self.assertEqual(P.faults(iter([1, 1, 2, 1]), 0, policy), 4)
            self.assertEqual(P.faults([], 0, policy), 0)
        with self.assertRaises(ValueError):
            P.faults([1], -1, "lru")
        with self.assertRaises(ValueError):
            P.faults([1], 0, "unknown")

    def test_allocator_size_and_release_contracts(self):
        for size in (0, -1):
            with self.assertRaises(ValueError):
                P.Buddy(4).malloc(size)
        for size in (0, -1, 4097):
            with self.assertRaises(ValueError):
                P.Slab(size)
        s = P.Slab(2048)
        a, b = s.alloc(), s.alloc()
        self.assertEqual((a, b), (0, 0))
        s.release(a)
        s.release(b)
        with self.assertRaises(ValueError):
            s.release(a)

    def test_belady(self):
        s = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        self.assertEqual((P.faults(s, 3, "fifo"), P.faults(s, 4, "fifo")), (9, 10))
        self.assertEqual(P.faults(s, 3, "opt"), 7)

    def test_opt_is_optimal_and_lru_stack(self):
        rng = random.Random(1)
        t = [rng.randrange(12) for _ in range(400)]
        for k in (2, 4, 6, 8):
            o = P.faults(t, k, "opt")
            for pol in ("lru", "fifo", "clock", "2q", "arc", "lirs", "random"):
                self.assertLessEqual(o, P.faults(t, k, pol))
        self.assertEqual(P.lru_curve(t, [2, 4, 6, 8]), P.curve(t, [2, 4, 6, 8], "lru"))

    def test_buddy_coalesces(self):
        b = P.Buddy(6)
        xs = [b.malloc(n) for n in (1, 3, 8, 2, 5)]
        for x in xs:
            b.release(x)
        self.assertEqual(b.free_pages(), 64)
        self.assertEqual(b.largest_free(), 64)


class TestVirt(unittest.TestCase):
    def test_guest_identical(self):
        from videos.cs.cs31.compute import LETTERS
        src = LETTERS.format(spin=30, count=6)
        n = K.boot([K.user_asm("A", src, 0), K.user_asm("B", src, 1)], quantum=500)
        n.run(1_000_000)
        v = Vt.boot_virt([K.user_asm("A", src, 0), K.user_asm("B", src, 1)], quantum=500)
        v.run(1_000_000)
        self.assertEqual(bytes(n.output), bytes(v.output))
        self.assertEqual(n.steps, v.steps)
        self.assertGreater(v.exits["csr"], 0)


if __name__ == "__main__":
    unittest.main()
