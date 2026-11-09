"""Part 5 (Memory and Time): latches, flip-flops, LFSRs and the register file of explainer/cs/pebble/seq.py, and the
state-machine computations of videos/cs/cs5/compute.py."""

from __future__ import annotations

import itertools
import math
import unittest

import numpy as np

from explainer.cs.pebble import seq as S


class Latches(unittest.TestCase):
    def test_sr_latch_sets_holds_resets(self):
        n = S.sr_latch()
        prog = [(0, 1)] * 4 + [(1, 1)] * 4 + [(1, 0)] * 4 + [(1, 1)] * 4
        h = n.run(lambda t: {"S_": prog[t][0], "R_": prog[t][1]}, len(prog), init={"Q": 0, "Qn": 1})
        self.assertEqual(h["Q"][7], 1)    # set, then held
        self.assertEqual(h["Q"][15], 0)   # reset, then held

    def test_symmetric_release_oscillates(self):
        n = S.sr_latch()
        prog = [(0, 0)] * 4 + [(1, 1)] * 10
        h = n.run(lambda t: {"S_": prog[t][0], "R_": prog[t][1]}, len(prog), init={"Q": 1, "Qn": 1})
        tail = h["Q"][6:]
        self.assertTrue(all(tail[i] != tail[i + 1] for i in range(len(tail) - 1)))

    def test_odd_ring_oscillates_with_period_2k(self):
        for k in (3, 5, 7):
            h = S.ring(k).run(lambda t: {}, 8 * k, init={f"x{i}": i % 2 for i in range(k)})["x0"]
            self.assertEqual(h[2 * k:4 * k], h[4 * k:6 * k])
            self.assertNotEqual(len(set(h[2 * k:4 * k])), 1)

    def test_flip_flop_samples_at_rising_edges(self):
        ms = S.master_slave()
        T = 72
        clk = [(t // 6) % 2 for t in range(T)]
        rng = np.random.default_rng(1)
        D, v = [], 0
        for t in range(T):
            if t % 12 == 2:  # change D well away from the rising edges (t = 6, 18, 30, ...)
                v = int(rng.integers(0, 2))
            D.append(v)
        h = ms.run(lambda t: {"D": D[t], "C": clk[t]}, T, init=S.MS_INIT)
        for edge in range(6, T - 6, 12):
            self.assertEqual(h["Q"][edge + 5], D[edge], edge)


class Clocked(unittest.TestCase):
    def test_counter_wraps(self):
        c = S.counter(4)
        c.reset(1)
        self.assertEqual([int(c.step({})["count"][0]) for _ in range(20)], [k % 16 for k in range(20)])

    def test_lfsr_period(self):
        l4 = S.lfsr((3, 2), 4)
        l4.reset(1)
        seen = [int(l4.step({})["r"][0]) for _ in range(15)]
        self.assertEqual(len(set(seen)), 15)
        self.assertNotIn(0, seen)

    def test_register_file_against_a_model(self):
        rf = S.register_file(8, 8)
        n = 200
        rf.reset(n)
        model = np.zeros((n, 8), dtype=np.int64)
        idx = np.arange(n)
        rng = np.random.default_rng(2)
        for _ in range(40):
            we, wa, wd = rng.integers(0, 2, n), rng.integers(0, 8, n), rng.integers(0, 256, n)
            ra, rb = rng.integers(0, 8, n), rng.integers(0, 8, n)
            out = rf.step({"we": we, "wa": wa, "wd": wd, "ra": ra, "rb": rb})
            self.assertTrue(np.array_equal(out["a"], model[idx, ra]))
            self.assertTrue(np.array_equal(out["b"], model[idx, rb]))
            m = (we == 1) & (wa != 0)
            model[idx[m], wa[m]] = wd[m]
        self.assertEqual(rf.flip_flops, 7 * 8)


class Theory(unittest.TestCase):
    def test_primitive_polynomial_counts(self):
        from videos.cs.cs5.compute import lfsr_period, totient
        for n in range(2, 9):
            maximal = sum(lfsr_period((1 << n) | (m << 1) | 1, n) == (1 << n) - 1 for m in range(1 << (n - 1)))
            self.assertEqual(maximal, totient((1 << n) - 1) // n)

    def test_minimization_of_the_mod6_machine(self):
        from videos.cs.cs5.compute import minimize
        delta = {(r, b): (2 * r + b) % 6 for r in range(6) for b in (0, 1)}
        rounds = minimize(list(range(6)), (0, 1), delta, {0, 3})
        final = rounds[-1]
        self.assertEqual(len(set(final.values())), 3)
        self.assertEqual(final[0], final[3])
        self.assertEqual(final[1], final[4])
        self.assertEqual(final[2], final[5])

    def test_fsm_synthesis_is_correct(self):
        from videos.cs.cs5.compute import encodings, synth
        for name, enc in encodings().items():
            self.assertTrue(synth(enc)["verified"], name)


class MitigationModel(unittest.TestCase):
    def test_refresh_frees_counter_for_another_row(self):
        from videos.cs.cs5.compute import misra_gries

        # Retaining the first row's zero counter lets it become negative and
        # permanently prevents the second row from being tracked.
        self.assertEqual(misra_gries([0, 0] + [1] * 20, 1, 2), {0: 2, 1: 2})

    def test_bounded_window_guarantee_on_every_short_stream(self):
        from videos.cs.cs5.compute import misra_gries

        # W=8, k=3, trigger=3: at most floor(8/4)=2 decrements.
        # Thus no row exceeds 3+2 activations before modeled mitigation.
        for stream in itertools.product(range(4), repeat=8):
            self.assertLessEqual(max(misra_gries(stream, 3, 3).values()), 5, stream)

    def test_annual_coin_bound_covers_all_run_endings(self):
        from videos.cs.cs5.compute import T_RC_S, compute_hammerdefence

        opportunities = math.ceil(365 * 24 * 3600 / T_RC_S)
        for row in compute_hammerdefence()["para"]:
            log_bound = math.log(opportunities) + row["t"] * math.log1p(-row["p"])
            self.assertLessEqual(log_bound, math.log(.01) + 1e-12, row)


if __name__ == "__main__":
    unittest.main()
