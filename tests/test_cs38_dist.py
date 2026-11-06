"""Part 38's distributed-systems instruments: clocks and snapshots, consensus, Raft, Byzantine and Nakamoto."""
from __future__ import annotations

import unittest

from explainer.cs.dist import byzantine as B
from explainer.cs.dist import clocks as C
from explainer.cs.dist import consensus as K
from explainer.cs.dist.raft import Cluster, random_faults


class Clocks(unittest.TestCase):
    def test_vector_clocks_characterize_causality(self):
        for s in range(5):
            r = C.check_vector(C.random_trace(3, 14, seed=s))
            self.assertTrue(r["vector_characterizes"])
            self.assertTrue(r["lamport_condition"])

    def test_snapshot_conserves_money(self):
        for s in range(5):
            self.assertTrue(C.Bank(4, seed=s).run()["consistent"])

    def test_ntp(self):
        off, d = C.ntp(100.0, 105.0, 105.1, 100.3)
        self.assertAlmostEqual(off, 4.9)
        self.assertAlmostEqual(d, 0.2)


class Consensus(unittest.TestCase):
    def test_flp_dichotomy(self):
        a = K.flp_table("wait-n-f")
        b = K.flp_table("wait-all")
        self.assertTrue(any(r["bivalent"] for r in a))
        self.assertTrue(any(r["can_disagree"] for r in a))
        self.assertTrue(all(not r["can_disagree"] and r["can_block"] for r in b))

    def test_floodset_needs_f_plus_one_rounds(self):
        self.assertFalse(K.floodset(3, 1, 1)["agreement"])
        self.assertTrue(K.floodset(3, 1, 2)["agreement"])
        self.assertFalse(K.floodset(4, 2, 2)["agreement"])
        self.assertTrue(K.floodset(4, 2, 3)["agreement"])

    def test_paxos_and_ben_or_are_safe(self):
        self.assertTrue(all(K.paxos(5, 3, loss=0.1, seed=s)["safe"] for s in range(50)))
        self.assertTrue(all(K.ben_or(5, 2, seed=s)["agreement"] for s in range(50)))


class Raft(unittest.TestCase):
    def test_correct_raft_survives_faults(self):
        for s in range(60):
            c = Cluster(5, seed=s, loss=0.1, delay=(0.005, 0.08))
            random_faults(c, 6, rate=8)
            c.run(until=6, client_rate=40)
            self.assertEqual(c.violations, [], s)

    def test_checker_catches_bugs(self):
        caught = 0
        for s in range(60):
            c = Cluster(5, seed=s, loss=0.05, bug="no-log-check")
            random_faults(c, 8, rate=3)
            c.run(until=8)
            caught += bool(c.violations)
        self.assertGreater(caught, 30)


class Byzantine(unittest.TestCase):
    def test_three_generals_fail_four_succeed(self):
        self.assertFalse(B.om_exhaustive(3, 1, {1})["always_agree"])
        self.assertTrue(B.om_exhaustive(4, 1, {2})["always_agree"])
        self.assertTrue(B.om_exhaustive(4, 1, {0})["always_agree"])
        self.assertFalse(B.om_exhaustive(4, 1, {1, 2})["always_agree"])

    def test_double_spend(self):
        self.assertAlmostEqual(B.rosenfeld(0.1, 6), B.double_spend_mc(0.1, 6, 200000), delta=0.0002)
        self.assertLess(B.nakamoto_p(0.1, 6), B.rosenfeld(0.1, 6))

    def test_selfish_mining(self):
        r = B.selfish(0.25, 0.5, blocks=100000)
        self.assertAlmostEqual(r["simulated"], r["formula"], delta=0.01)


if __name__ == "__main__":
    unittest.main()
