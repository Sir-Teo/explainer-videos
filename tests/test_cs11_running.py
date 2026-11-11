"""Part 11's instruments: allocators, the Job in four linked files, the stack smash and its defences."""

import random
import unittest

from explainer.cs.pebble import heap as H
from explainer.cs.pebble import jobv1, smash
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.link import load


def random_events(n=3000, seed=1):
    rng = random.Random(seed)
    live, ev, nid = [], [], 0
    for _ in range(n):
        if live and rng.random() < 0.45:
            ev.append(("f", live.pop(rng.randrange(len(live)))))
        else:
            ev.append(("a", nid, rng.choice([8, 16, 24, 40, 100, 300, 1000, 5000])))
            live.append(nid)
            nid += 1
    return ev


class TestAllocators(unittest.TestCase):
    def test_no_overlap(self):
        """Live blocks never overlap, every block is big enough, and the heap covers them all."""
        ev = random_events()
        for A in (H.FirstFit, H.NextFit, H.BestFit, H.Segregated):
            a = A()
            where, size = {}, {}
            for e in ev:
                if e[0] == "a":
                    addr = a.malloc(e[2])
                    where[e[1]] = addr
                    size[e[1]] = a.used[addr]
                    self.assertGreaterEqual(a.used[addr], e[2] + H.HEADER)
                else:
                    a.free(where.pop(e[1]))
                    size.pop(e[1])
                spans = sorted((where[i], where[i] + size[i]) for i in where)
                for (s1, e1), (s2, _) in zip(spans, spans[1:]):
                    self.assertLessEqual(e1, s2, A.name)
                if spans:
                    self.assertLessEqual(spans[-1][1], a.top)
            # free blocks never touch (they would have been coalesced)
            for x, y in zip(a.addrs, a.addrs[1:]):
                self.assertLess(x + a.size[x], y)

    def test_buddy(self):
        b = H.Buddy()
        addrs = [b.malloc(n) for n in (10, 100, 1000, 10, 3000)]
        for a in addrs:
            k = b.used[a]
            self.assertEqual(a % (1 << k), 0)  # aligned to its size
        for a in addrs:
            b.free_(a)
        self.assertFalse(b.used)

    def test_fragmentation_at_least_one(self):
        ev = random_events(2000, seed=5)
        for A in (H.FirstFit, H.BestFit, H.Buddy):
            self.assertGreaterEqual(H.simulate(ev, A()).fragmentation, 1.0)


class TestJob(unittest.TestCase):
    def test_same_as_v0(self):
        objs, exe = jobv1.build()
        text = ("It is a truth universally acknowledged, that a single man in possession of a good fortune, "
                "must be in want of a wife. The the THE a A an.")
        tape = P.job_tape(text)
        m = load(exe, tape=tape)
        m.run()
        self.assertEqual(bytes(m.output), P.job_reference(tape))


class TestSmash(unittest.TestCase):
    def test_attack_and_defences(self):
        exe = smash.build()
        self.assertEqual(smash.run(exe, b"Ada\n")["output"], "hello, Ada\nbye\n")
        tape = smash.exploit(exe)
        self.assertTrue(smash.run(exe, tape)["output"].endswith("pwned"))
        exe_c = smash.build(canary=True)
        self.assertIn("smashing detected", smash.run(exe_c, smash.exploit(exe_c))["output"])
        self.assertIn("no-execute", smash.run(exe, tape, nx=True)["fault"])


if __name__ == "__main__":
    unittest.main()
