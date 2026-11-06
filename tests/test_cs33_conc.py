"""Part 33's instruments: the model checker, the linearizability checker, the lock simulator, Pebble's atomics and
PebbleOS threads."""
from __future__ import annotations

import random
import unittest

from explainer.cs.conc import lin as L
from explainer.cs.conc import locks as K
from explainer.cs.conc import mc as M
from explainer.cs.os import vmos as V
from explainer.cs.pebble.asm import assemble
from explainer.cs.pebble.emu import Machine


def final_c(r):
    return sorted(dict(f)["c"] for f in r.finals)


class ModelChecker(unittest.TestCase):
    def test_counter_schedules_match_the_multinomial(self):
        p = M.counter(2, 1)
        sch = M.schedules(p, project=lambda s, q: dict(zip(q.vars, s[2]))["c"])
        self.assertEqual(sum(sch.values()), M.interleavings([3, 3]))
        self.assertEqual(sch, {1: 18, 2: 2})

    def test_lost_updates_and_their_fixes(self):
        self.assertEqual(final_c(M.explore(M.counter(2, 2))), [2, 3, 4])
        self.assertEqual(final_c(M.explore(M.counter(2, 2, "fai"))), [4])
        self.assertEqual(final_c(M.explore(M.counter(2, 2, "lock"))), [4])

    def test_peterson_needs_its_fences(self):
        self.assertIsNone(M.explore(M.peterson(False, 2), "sc", M.mutex).violation)
        self.assertIsNotNone(M.explore(M.peterson(False, 1), "tso", M.mutex).violation)
        self.assertIsNone(M.explore(M.peterson(True, 2), "tso", M.mutex).violation)
        self.assertIsNotNone(M.explore(M.peterson(True, 2), "pso", M.mutex).violation)
        self.assertIsNone(M.explore(M.peterson("both", 2), "pso", M.mutex).violation)

    def test_naive_lock_fails_and_bakery_holds(self):
        self.assertIsNotNone(M.explore(M.naive_flags(1), "sc", M.mutex).violation)
        self.assertIsNone(M.explore(M.bakery(2, 2), "sc", M.mutex).violation)

    def test_litmus_outcomes(self):
        def sb(model, f):
            return sorted(M.explore(M.litmus_sb(f), model, project=lambda s, q: tuple(s[2][0:2])).finals)
        self.assertNotIn((0, 0), sb("sc", False))
        self.assertIn((0, 0), sb("tso", False))
        self.assertNotIn((0, 0), sb("tso", True))

        def mp(model):
            return sorted(M.explore(M.litmus_mp(False), model, project=lambda s, q: dict(zip(q.vars, s[2]))["r"]
                                    ).finals)
        self.assertEqual(mp("tso"), [42])
        self.assertEqual(mp("pso"), [0, 42])

    def test_philosophers_deadlock_unless_ordered(self):
        self.assertEqual(len(M.explore(M.philosophers(5)).deadlocks), 1)
        self.assertEqual(len(M.explore(M.philosophers(5, True)).deadlocks), 0)

    def test_consensus(self):
        def ok(p):
            return M.explore(p, invariant=M.agreement).violation is None
        self.assertTrue(ok(M.consensus_tas(2)))
        self.assertFalse(ok(M.consensus_tas(3)))
        self.assertTrue(ok(M.consensus_cas(3)))
        self.assertFalse(ok(M.consensus_registers(2)))

    def test_aba(self):
        def corrupt(tagged):
            T = 100 if tagged else None
            p = M.treiber_aba(tagged)

            def proj(s, q):
                popped = {v for o in s[5] for v in o if v > 0}
                pushed = {-v for o in s[5] for v in o if v < 0}
                return bool((popped - pushed) & set(M.stack_of(s, q, T)))
            return any(M.explore(p, project=proj).finals)
        self.assertTrue(corrupt(False))
        self.assertFalse(corrupt(True))


class Linearizability(unittest.TestCase):
    def test_hand_histories(self):
        Op = L.Op
        self.assertIsNone(L.check([Op(0, "write", 1, None, 0, 2), Op(1, "read", None, 1, 1, 3),
                                   Op(1, "read", None, 0, 4, 5)], "register"))
        self.assertIsNotNone(L.check([Op(0, "write", 1, None, 0, 2), Op(1, "read", None, 0, 1, 3)], "register"))

    def test_correct_objects_always_pass(self):
        rng = random.Random(3)
        for spec in ("queue", "stack", "register", "counter"):
            for _ in range(100):
                self.assertIsNotNone(L.check(L.random_history(spec, 3, 10, rng), spec))


class Locks(unittest.TestCase):
    def test_mutual_exclusion_and_scaling(self):
        tas = K.simulate("tas", 16, 120, cs=4, think=40)
        mcs = K.simulate("mcs", 16, 120, cs=4, think=40)
        self.assertGreater(tas["bus_per_acq"], 3 * mcs["bus_per_acq"])
        self.assertGreater(mcs["fair"], 0.8)


class Atomics(unittest.TestCase):
    def test_cas_and_amoadd(self):
        p = assemble("""
        li   t0, 4096
        li   t1, 5
        sw   t1, 0(t0)
        li   a0, 5
        li   a1, 9
        cas  a0, t0, a1
        li   a2, 5
        cas  a2, t0, a1
        li   a3, 3
        amoadd a4, t0, a3
        lw   a5, 0(t0)
        halt
""")
        m = Machine(image=p.image).run(100)
        R = m.regs
        self.assertEqual((R[3], R[5], R[7], R[8]), (5, 9, 9, 12))

    def test_threads_share_memory(self):
        from videos.cs.cs33.compute import TDATA, thread_src
        outs = {}
        for kind in ("race", "amoadd", "lock"):
            th = V.threads_vm("w", thread_src(kind, 1000, 2), 2, data=TDATA)
            m = V.boot_vm(th, quantum=500)
            m.run(20_000_000)
            outs[kind] = int(bytes(m.output).decode())
        self.assertLess(outs["race"], 2000)
        self.assertEqual(outs["amoadd"], 2000)
        self.assertEqual(outs["lock"], 2000)


if __name__ == "__main__":
    unittest.main()
