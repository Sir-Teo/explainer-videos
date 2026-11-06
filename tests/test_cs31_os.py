"""Part 31's instruments: Pebble's kernel mode, PebbleOS, the schedulers, queues and real-time tests."""
from __future__ import annotations

import itertools
import random
import unittest

from explainer.cs.os import kernel as K
from explainer.cs.os import queueing as Q
from explainer.cs.os import rt
from explainer.cs.os.machine import ILLEGAL, STORE_FAULT, TIMER, OSMachine
from explainer.cs.os.sched import Job, simulate
from explainer.cs.pebble.asm import assemble
from explainer.cs.pebble.emu import Machine, MachineError

PRINT = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a5, 3
        ecall
        addi a0, a0, 48
        call __putc
        li   a0, 10
        call __putc
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
"""


class TestMachine(unittest.TestCase):
    def test_base_machine_rejects_privileged(self):
        with self.assertRaises(MachineError):
            Machine(image=assemble("ecall\nhalt\n").image).run(10)

    def test_trap_and_eret(self):
        # kernel: set tvec, drop to user at `u`; user executes halt (illegal) -> trap handler halts
        src = """
        la   t0, handler
        csrw tvec, t0
        la   t0, u
        csrw epc, t0
        li   t0, 0x100
        csrw lo, t0
        li   t0, 0x200
        csrw hi, t0
        li   t0, 2
        csrw status, t0
        eret
handler: csrr a0, cause
        csrr a1, epc
        halt
        .org 0x100
u:      addi a2, zero, 5
        halt
"""
        m = OSMachine(image=assemble(src).image)
        m.run(100)
        self.assertEqual(m.regs[3], ILLEGAL)
        self.assertEqual(m.regs[4], 0x104)
        self.assertEqual(m.regs[5], 5)
        self.assertEqual(m.mode, 1)

    def test_bounds_and_timer(self):
        src = """
        la   t0, handler
        csrw tvec, t0
        la   t0, u
        csrw epc, t0
        li   t0, 0x100
        csrw lo, t0
        li   t0, 0x200
        csrw hi, t0
        li   t0, {timer}
        csrw timer, t0
        li   t0, 2
        csrw status, t0
        eret
handler: csrr a0, cause
        csrr a1, tval
        halt
        .org 0x100
u:      addi a2, a2, 1
        li   t0, 0x40
        sw   a2, 0(t0)
        halt
"""
        m = OSMachine(image=assemble(src.format(timer=1000)).image)
        m.run(100)
        self.assertEqual((m.regs[3], m.regs[4]), (STORE_FAULT, 0x40))
        m = OSMachine(image=assemble(src.format(timer=6)).image)
        m.run(100)
        self.assertEqual(m.regs[3], TIMER)


class TestKernel(unittest.TestCase):
    def test_two_processes(self):
        m = K.boot([K.user_asm("a", PRINT, 0), K.user_asm("b", PRINT, 1)])
        m.run(100_000)
        self.assertEqual(bytes(m.output), b"1\n2\n")
        self.assertTrue(m.halted)
        self.assertEqual([p["state"] for p in K.pcbs(m)], ["exited", "exited"])

    def test_faults_kill_only_the_offender(self):
        bad = "main:   li t0, 0x100\n        sw t0, 0(t0)\n        ret\n"
        m = K.boot([K.user_asm("bad", bad, 0), K.user_asm("good", PRINT, 1)])
        m.run(100_000)
        self.assertEqual(bytes(m.output), b"2\n")
        self.assertEqual(K.pcbs(m)[0]["exit"], -STORE_FAULT)

    def test_kernel_checks_user_pointers(self):
        src = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a0, 1
        li   a1, 0x100          # the kernel's memory, not ours
        li   a2, 4
        li   a5, 2
        ecall                   # write: refused
        mv   s0, a0
        addi a0, a0, 50         # '1' if it returned -1
        call __putc
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
"""
        m = K.boot([K.user_asm("p", src, 0)])
        m.run(100_000)
        self.assertEqual(bytes(m.output), b"1")

    def test_pipeline_matches_the_job(self):
        from explainer.cs.algo import job2 as J
        from explainer.cs.pebble import programs as PR
        from videos.cs.cs31.compute import TOK
        t = PR.job_tape("It was the best of times, it was the worst of times; it was THE age of wisdom. " * 60)
        m = K.boot([K.user("tok", TOK, 0, stdout="pipe"), K.user("job", J.JOB_HASH, 1, stdin="pipe")], tape=t,
                   quantum=3000)
        m.run(50_000_000)
        self.assertEqual(bytes(m.output), PR.job_reference(t))
        a = K.attribute(m)
        self.assertEqual(sum(a["user"].values()) + a["kernel"], m.steps)
        self.assertGreater(K.report(m)["switches"], 10)


class TestSched(unittest.TestCase):
    def test_sjf_is_optimal(self):
        rng = random.Random(3)
        for _ in range(20):
            bursts = [rng.randint(1, 30) for _ in range(5)]
            jobs = [Job(str(i), 0, [b]) for i, b in enumerate(bursts)]
            sjf = simulate(jobs, "sjf").metrics()["mean"]["turnaround"]
            best = min(sum(sum(p[:k + 1]) for k in range(5)) / 5 for p in itertools.permutations(bursts))
            self.assertAlmostEqual(sjf, best)

    def test_stride_is_exact(self):
        J = [Job("a", 0, [10 ** 5], tickets=300), Job("b", 0, [10 ** 5], tickets=100)]
        r = simulate(J, "stride", quantum=10, horizon=4000, track=True)
        self.assertEqual(r.cpu["a"][3999], 3000)


class TestQueues(unittest.TestCase):
    def test_mm1_and_pk(self):
        r = Q.mg1(0.5, Q.expo(1.0), n=100_000, seed=2)
        self.assertAlmostEqual(r["mean"], 2.0, delta=0.1)
        r = Q.mg1(0.8, Q.det(1.0), n=100_000, seed=2)
        self.assertAlmostEqual(r["mean"], Q.pk(0.8, 1.0, 1.0), delta=0.15)
        self.assertAlmostEqual(r["L"], r["lam_hat"] * r["W_all"], delta=0.05 * r["L"])

    def test_srpt_beats_fcfs(self):
        f = Q.mg1(0.8, Q.expo(1.0), n=30_000, seed=4)["mean"]
        s = Q.mg1(0.8, Q.expo(1.0), n=30_000, seed=4, discipline="srpt")["mean"]
        self.assertLess(s, f)


class TestRealTime(unittest.TestCase):
    def test_bounds(self):
        self.assertAlmostEqual(rt.ll_bound(2), 0.8284, places=4)
        self.assertEqual(rt.rta([(1, 4), (2, 6), (3, 12)]), [1, 3, 10])

    def test_edf_meets_every_deadline_up_to_one(self):
        rng = random.Random(5)
        for _ in range(30):
            Ts = [rng.choice([4, 5, 6, 8, 10]) for _ in range(3)]
            us = rt.uunifast(3, 0.95, rng)
            tasks = [(max(1, int(u * T)), T) for u, T in zip(us, Ts)]
            if sum(c / t for c, t in tasks) <= 1:
                self.assertEqual(rt.schedule(tasks, "edf")["misses"], [])

    def test_priority_inheritance(self):
        self.assertTrue(rt.pathfinder(False)["reset"])
        self.assertFalse(rt.pathfinder(True)["reset"])


if __name__ == "__main__":
    unittest.main()
