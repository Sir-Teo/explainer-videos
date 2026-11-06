"""Tests for Part 60's instruments (explainer/cs/hw): every result against an independent computation."""

from __future__ import annotations

import os
import unittest
from collections import Counter

import numpy as np

from explainer.cs.hw import accel, roofline, systolic
from explainer.cs.pebble import tech
from explainer.cs.pebble.blocks import tree_multiplier
from explainer.cs.pebble.hdl import exhaustive, simulate, unpack
from explainer.cs.pebble.programs import job_reference, job_words

BOOKS = os.path.isdir(os.path.join(os.path.dirname(__file__), "..", ".cache", "ai1", "books"))

TEXT = ("It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want "
        "of a wife.  “My dear Mr. Bennet,” said his lady to him one day, “have you heard that "
        "Netherfield Park is let at last?”  Mr. Bennet replied that he had not.  BUT it is, x2y, café, "
        "Émile; it IS!").encode("utf-8")


# ---------------------------------------------------------------------------- systolic
class Cell(unittest.TestCase):
    def test_cell_exhaustive_small(self):
        # every input of a 3-bit x 3-bit + 6-bit cell, against integer arithmetic
        for kind in systolic.KINDS:
            c = systolic.mac_cell(3, 6, kind)
            vals = exhaustive(c)
            out = c.evaluate(vals)["acc_out"]
            n = 1 << 12
            got = sum(unpack(w, n) << i for i, w in enumerate(out))
            p = np.arange(n)
            a, b, acc = p & 7, (p >> 3) & 7, p >> 6
            self.assertTrue(np.array_equal(got, (acc + a * b) % 64), kind)

    def test_cell_random_full_width(self):
        self.assertEqual(systolic.cell_check()["correct"], {"tree": True, "array": True})

    def test_cell_stats(self):
        st = systolic.cell_stats()
        for kind, r in st["kinds"].items():
            c = systolic.mac_cell(8, 24, kind)
            self.assertEqual(r["gates"], sum(r["counts"].values()))
            self.assertEqual(r["gates"], c.size())
            self.assertEqual(r["depth"], c.depth())
            self.assertGreater(r["nand_gates"], r["gates"])
        self.assertLess(st["kinds"]["tree"]["depth"], st["kinds"]["array"]["depth"])
        self.assertEqual(st["flip_flops"]["output_stationary"], 8 + 8 + 24)


class Systolic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.os = {n: systolic.output_stationary(n, trials=16, seed=n) for n in (2, 4, 8)}
        cls.ws = {n: systolic.weight_stationary(n, trials=16, seed=n) for n in (2, 4, 8)}

    def test_output_stationary_against_numpy(self):
        for n, r in self.os.items():
            A, B = np.array(r["A"]), np.array(r["B"])
            self.assertTrue(np.array_equal(np.array(r["C"]), A @ B))
            self.assertTrue(r["correct"])  # all 16 trials
            self.assertEqual(r["cycles"], 3 * n - 2)
            self.assertAlmostEqual(r["utilization"], n / (3 * n - 2))
            self.assertEqual(r["gates"], n * n * systolic.mac_cell().size())
            self.assertEqual(r["flip_flops"], n * n * 40)

    def test_output_stationary_wavefronts(self):
        r = systolic.output_stationary(4, trials=1, seed=3)
        A, B = np.array(r["A"]), np.array(r["B"])
        n = 4
        acc = np.zeros((n, n), np.int64)
        for row in r["trace"]:
            t = row["t"]
            for i in range(n):
                for j in range(n):
                    k = row["k"][i][j]
                    if 0 <= t - i - j < n:
                        self.assertEqual(k, t - i - j)
                        self.assertEqual(row["a"][i][j], A[i, k])
                        self.assertEqual(row["b"][i][j], B[k, j])
                        acc[i, j] += A[i, k] * B[k, j]
                    else:
                        self.assertIsNone(k)
                    self.assertEqual(row["acc"][i][j], acc[i, j])
        self.assertTrue(np.array_equal(acc, A @ B))

    def test_weight_stationary_against_numpy(self):
        for n, r in self.ws.items():
            X, W = np.array(r["X"]), np.array(r["W"])
            self.assertTrue(np.array_equal(np.array(r["Y"]), X @ W))
            self.assertTrue(r["correct"] and r["weights_loaded"])
            self.assertEqual(r["cycles"], n + n + 2 * n - 2)
            self.assertAlmostEqual(r["compute_utilization"], n / (3 * n - 2))
            self.assertAlmostEqual(r["utilization"], n ** 3 / (n * n * (4 * n - 2)))

    def test_weight_stationary_rectangular_stream(self):
        r = systolic.weight_stationary(3, m=7, trials=4, seed=5)
        self.assertTrue(np.array_equal(np.array(r["Y"]), np.array(r["X"]) @ np.array(r["W"])))
        self.assertTrue(r["correct"])
        self.assertEqual(r["compute_cycles"], 7 + 2 * 3 - 2)

    def test_compiled_engine_same_gates(self):
        a = systolic.output_stationary(2, trials=4, seed=9, engine="hdl")
        b = systolic.output_stationary(2, trials=4, seed=9, engine="fast")
        self.assertEqual(a["trace"], b["trace"])
        self.assertEqual(a["C"], b["C"])

    def test_model_matches_gate_level(self):
        for n in (2, 4, 8):
            g = self.os[n]
            m = systolic.dataflow_model(n, dataflow="os", A=g["A"], B=g["B"])
            self.assertTrue(np.array_equal(m["result"], np.array(g["C"])))
            self.assertEqual((m["cycles"], m["busy_cell_cycles"]), (g["cycles"], g["busy_cell_cycles"]))
            g = self.ws[n]
            m = systolic.dataflow_model(n, n, "ws", A=g["X"], B=g["W"])
            self.assertTrue(np.array_equal(m["result"], np.array(g["Y"])))
            self.assertEqual((m["cycles"], m["busy_cell_cycles"]), (g["cycles"], g["busy_cell_cycles"]))

    def test_scaling_closed_forms(self):
        for r in systolic.scaling((16, 64, 256)):
            self.assertTrue(r["correct"])
            self.assertAlmostEqual(r["utilization"], r["closed_form"])
            self.assertAlmostEqual(r["compute_utilization"], r["closed_form_compute"])
            n, m = r["n"], r["m"]
            self.assertEqual(r["cycles"], 3 * n - 2 if r["dataflow"] == "os" else m + 3 * n - 2)
            self.assertEqual(r["busy_cell_cycles"], r["macs"])

    def test_signed_model(self):
        rng = np.random.default_rng(4)
        X, W = rng.integers(-128, 128, (40, 16)), rng.integers(-128, 128, (16, 16))
        self.assertTrue(np.array_equal(systolic.dataflow_model(16, 40, "ws", A=X, B=W)["result"], X @ W))


class Quantization(unittest.TestCase):
    def test_quantize_bound(self):
        x = np.random.default_rng(0).standard_normal(1000)
        q, s = systolic.quantize(x)
        self.assertLessEqual(int(np.max(np.abs(q))), 127)
        self.assertLessEqual(float(np.max(np.abs(q * s - x))), s / 2 + 1e-12)

    def test_int8_matmul_independent(self):
        rng = np.random.default_rng(1)
        A, B = rng.standard_normal((50, 40)), rng.standard_normal((40, 30))
        got, _ = systolic.int8_matmul(A, B)
        sa, sb = np.abs(A).max() / 127, np.abs(B).max() / 127
        want = (np.round(A / sa) @ np.round(B / sb)) * sa * sb  # float64 arithmetic on the same integers
        self.assertTrue(np.allclose(got, want, rtol=1e-12, atol=1e-12))

    def test_quantized_matmul(self):
        r = systolic.quantized_matmul()
        self.assertLess(r["float32_rel_error"], 1e-5)
        self.assertLess(r["float32_rel_error"], r["float16_inputs_rel_error"])
        self.assertLess(r["float16_inputs_rel_error"], r["int8_rel_error"])
        # per-entry rounding error s/sqrt(12) on each factor, relative to unit-variance entries
        est = np.hypot(r["scale_a"], r["scale_b"]) / np.sqrt(12)
        self.assertLess(abs(r["int8_rel_error"] - est) / est, 0.25)
        self.assertTrue(r["systolic_int8_exact"])
        self.assertLess(r["max_abs_int32_acc"], 2 ** 31)

    def test_classifier(self):
        r = systolic.quantized_classifier()
        self.assertGreater(r["float32_accuracy"], 0.5)
        self.assertLess(abs(r["int8_accuracy"] - r["float32_accuracy"]), 0.01)
        self.assertGreater(r["agreement"], 0.98)

    def test_energy_area(self):
        e = systolic.energy_area()
        # the TPU paper: 65,536 MACs at 700 MHz is "92 TeraOps/second"; 6x energy and area for multiplies (int8 vs
        # fp16), 13x energy and 38x area for adds -- the paper's own statements of Horowitz's table
        self.assertAlmostEqual(e["tpu_peak_ops_computed"] / 1e12, 92, delta=0.5)
        self.assertEqual(256 * 256, e["tpu"]["macs"])
        r = e["ratios"]
        self.assertAlmostEqual(r["fp16_mult_over_int8_mult_energy"], 6, delta=0.6)
        self.assertAlmostEqual(r["fp16_mult_over_int8_mult_area"], 6, delta=0.6)
        self.assertAlmostEqual(r["fp16_add_over_int8_add_energy"], 13, delta=0.6)
        self.assertAlmostEqual(r["fp16_add_over_int8_add_area"], 38, delta=0.6)
        self.assertEqual(e["our_multipliers"][24]["gates"], tree_multiplier(24, "dadda").size())
        self.assertTrue(5 < e["our_gate_ratio_24_over_8"] < 12)  # about (24 / 8)^2


# ---------------------------------------------------------------------------- roofline
class Roofline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = roofline.kernels()
        cls.m = cls.k["machine"]

    def test_model(self):
        self.assertEqual(roofline.attainable(0.25, 100e9, 10e9), 2.5e9)
        self.assertEqual(roofline.attainable(50, 100e9, 10e9), 100e9)

    def test_machine(self):
        m = self.m
        self.assertGreater(m["peak_gflops"], 1)
        self.assertGreater(m["bandwidth_gbs"], 0.5)
        self.assertAlmostEqual(m["ridge_flops_per_byte"], m["peak_gflops"] / m["bandwidth_gbs"])
        self.assertEqual(m["peak_gflops"], max(r["gflops"] for r in m["peak"]["sizes"]))
        bw = m["bandwidth"]
        kinds = [bw[k] for k in ("copy_gbs", "add_gbs", "daxpy_gbs", "dot_gbs")]
        self.assertLess(max(kinds) / min(kinds), 4)
        self.assertTrue(bw["add_checked"])
        self.assertGreater(bw["array_mb"] * 2 ** 20, bw["llc_bytes"] or 0)

    def test_peak_against_part52(self):
        with roofline.blas_threads(1):
            g = roofline.speed.blas_levels((512,))[0]["gemm_gflops"]
        self.assertLess(g, 2.0 * self.m["peak_gflops"])
        self.assertGreater(g, self.m["peak_gflops"] / 4)

    def test_intensities(self):
        want = {"axpy": 2 / 24, "dot": 2 / 16, "matrix-vector": 2 / 8}
        for p in self.k["points"]:
            if p["kernel"] in want:
                self.assertAlmostEqual(p["intensity"], want[p["kernel"]])
            if p["kernel"] == "matrix-matrix":
                self.assertAlmostEqual(p["intensity"], p["size"] / 12)
            if p["kernel"] == "5-point stencil":
                self.assertAlmostEqual(p["intensity"], 0.25, delta=0.001)
            self.assertAlmostEqual(p["roof_gflops"], min(self.m["peak_gflops"], p["intensity"]
                                                         * self.m["bandwidth_gbs"]))
            self.assertAlmostEqual(p["gflops"], p["flops"] / p["seconds"] / 1e9)

    def test_points_under_roof(self):
        for p in self.k["points"]:
            if not p["in_cache"]:  # DRAM-sized: the roof binds, within a loaded machine's timing noise
                self.assertLess(p["fraction_of_roof"], 1.6, p["kernel"])
            if p["kernel"] == "matrix-matrix" and p["size"] >= 256:
                self.assertLess(p["fraction_of_roof"], 1.6)
        job = [p for p in self.k["points"] if p["kernel"].startswith("the Job")][0]
        self.assertLess(job["fraction_of_roof"], 0.05)  # far below: the interpreter, not the memory, limits it

    def test_job_point(self):
        j = self.k["job"]
        self.assertAlmostEqual(j["bytes_per_second"], j["bytes"] / j["seconds"])

    def test_stencil(self):
        u = np.random.default_rng(0).standard_normal((6, 7))
        out = roofline.stencil(u, np.zeros_like(u))
        for i in range(1, 5):
            for j in range(1, 6):
                self.assertAlmostEqual(out[i, j], (u[i - 1, j] + u[i + 1, j] + u[i, j - 1] + u[i, j + 1]) / 4)

    def test_energy(self):
        e = roofline.energy()
        E = {r["op"]: r["pj"] for r in e["table"]}
        self.assertAlmostEqual(e["dram_over_fp32_mult"][0], 1300 / 3.7)
        self.assertAlmostEqual(e["dram_over_int32_add"][1], 2600 / 0.1)
        self.assertLess(E["fp32 add"], E["fp32 multiply"])
        self.assertLess(E["8 KB SRAM read (64 bits)"], E["1 MB SRAM read (64 bits)"])


# ---------------------------------------------------------------------------- the Job in hardware
class Stages(unittest.TestCase):
    def test_le_const(self):
        from explainer.cs.pebble.hdl import Circuit

        for K in range(32):
            c = Circuit()
            x = c.input("x", 5)
            c.output("y", accel.le_const(c, x, K))
            y = simulate(c, {"x": np.arange(32)})["y"]
            self.assertTrue(np.array_equal(y, (np.arange(32) <= K).astype(np.uint64)))

    def test_classify_every_byte(self):
        y = simulate(accel.classify_stage(), {"byte": np.arange(256)})
        for b in range(256):
            low = bytes([b]).lower()
            letter = b"a" <= low <= b"z"
            self.assertEqual(int(y["letter"][b]), int(letter), b)
            self.assertEqual(int(y["code"][b]), low[0] - 96 if letter else 0)

    def test_hash_stage(self):
        rng = np.random.default_rng(0)
        n = 2000
        h = rng.integers(0, 1 << 32, n, dtype=np.uint64)
        code = rng.integers(1, 27, n)
        letter = rng.integers(0, 2, n)
        inword = rng.integers(0, 2, n)
        y = simulate(accel.hash_stage(), {"h": h, "code": code, "letter": letter, "inword": inword})
        for i in range(n):
            hi, ci = int(h[i]), int(code[i])
            want = (33 * hi + ci) & 0xFFFFFFFF if letter[i] else accel.H0
            self.assertEqual(int(y["h_next"][i]), want)
            self.assertEqual(int(y["end"][i]), int(inword[i] and not letter[i]))
            self.assertEqual(int(y["hash_out"][i]), hi)

    def test_emit_and_count_stages(self):
        rng = np.random.default_rng(1)
        n = 2000
        h = rng.integers(0, 1 << 32, n, dtype=np.uint64)
        y = simulate(accel.emit_stage(12), {"end": np.ones(n, np.int64), "hash": h})
        self.assertEqual([int(v) for v in y["index"]], [accel.slot(int(v), 12) for v in h])
        tag = rng.integers(0, 1 << 32, n, dtype=np.uint64)
        rd_tag = np.where(rng.random(n) < 0.5, tag, rng.integers(0, 1 << 32, n, dtype=np.uint64))
        emit, valid = rng.integers(0, 2, n), rng.integers(0, 2, n)
        cnt, ovf = rng.integers(0, 1 << 23, n), rng.integers(0, 1 << 23, n)
        y = simulate(accel.count_stage(), {"emit": emit, "tag": tag, "rd_valid": valid, "rd_tag": rd_tag,
                                           "rd_count": cnt, "ovf": ovf})
        for i in range(n):
            hit = emit[i] and valid[i] and tag[i] == rd_tag[i]
            miss = emit[i] and valid[i] and tag[i] != rd_tag[i]
            claim = emit[i] and not valid[i]
            self.assertEqual(int(y["we"][i]), int(hit or claim))
            if hit or claim:
                self.assertEqual(int(y["wd_count"][i]), int(cnt[i]) + 1 if hit else 1)
            self.assertEqual(int(y["miss"][i]), int(miss))
            self.assertEqual(int(y["ovf_next"][i]), int(ovf[i]) + int(miss))

    def test_word_hash_is_djb2_on_letter_codes(self):
        h = 5381
        for ch in b"bennet":
            h = (h * 33 + ch - 96) % 2 ** 32
        self.assertEqual(accel.word_hash(b"bennet"), h)


class Accelerator(unittest.TestCase):
    def _check(self, r, tape):
        ref = Counter(job_words(tape))
        self.assertTrue(r["hashes_match"] and r["tables_match_model"] and r["accounted"])
        self.assertEqual(r["words"], sum(ref.values()))
        self.assertEqual(r["distinct"], len(ref))
        self.assertEqual(r["lost_occurrences"], r["overflow"])

    def test_paragraph_exact(self):
        for lanes in (1, 3):
            r = accel.run(TEXT, lanes=lanes)
            self._check(r, TEXT)
            self.assertEqual(r["lost_occurrences"], 0)
            self.assertEqual(r["exact_words"], r["distinct"])
            self.assertTrue(r["top_exact"])
            self.assertEqual(r["top"].encode(), job_reference(TEXT))
            longest = max(len(p) for p in accel.split_lanes(TEXT, lanes))
            self.assertEqual(r["cycles"], longest + 1 + accel.LATENCY)

    def test_collisions_reported(self):
        r = accel.run(TEXT, lanes=1, k=3)  # an 8-entry table: most words collide
        self._check(r, TEXT)
        self.assertGreater(r["lost_occurrences"], 0)
        m = accel.table_model(job_words(TEXT), 3)
        self.assertEqual(r["overflow"], m["overflow"])
        self.assertEqual(r["occupied"], len(m["slots"]))

    def test_split_lanes(self):
        for L in (1, 2, 5, 9):
            ps = accel.split_lanes(TEXT, L)
            self.assertEqual(b"".join(ps), TEXT)
            self.assertEqual(sum((job_words(p) for p in ps), []), job_words(TEXT))

    @unittest.skipUnless(BOOKS, "the novels are not downloaded")
    def test_chapter_eight_lanes(self):
        tape = accel.short_text()
        r = accel.run(tape, lanes=8)
        self._check(r, tape)
        self.assertTrue(r["top_exact"])
        ref = Counter(job_words(tape))
        # the words a lane's table owns are counted exactly
        self.assertGreaterEqual(r["exact_words"], len(ref) - r["lost_occurrences"])

    def test_timing(self):
        tm = accel.timing()
        s = accel.unit()
        self.assertEqual(tm["gates"], s.c.size())
        self.assertEqual(tm["max_logic_depth"], s.c.depth())
        self.assertEqual(tm["flip_flops"], s.flip_flops)
        stage_ps = [r["mem_ps"] + r["depth"] * tech.GATE_PS for r in tm["stages"].values()]
        self.assertAlmostEqual(tm["period_ps"], max(stage_ps) + tech.FF_PS)
        self.assertAlmostEqual(tm["clock_mhz"], 1e6 / tm["period_ps"])
        self.assertEqual(tm["critical_stage"], "count")


@unittest.skipUnless(BOOKS, "the novels are not downloaded")
class Novels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = accel.job_on_novels()

    def test_bytes_and_time(self):
        from explainer.cs.pebble.programs import job_tape
        from videos.cs.cs6.compute import novels

        books = novels()
        total = sum(len(job_tape(t)) for t in books.values())
        self.assertEqual(self.job["bytes"], total)
        one = self.job["lanes"][0]
        self.assertEqual(one["cycles"], total + (len(books) - 1) + 1 + accel.LATENCY)
        self.assertAlmostEqual(one["seconds"], one["cycles"] / (self.job["clock_mhz"] * 1e6))
        for r in self.job["lanes"]:
            self.assertTrue(r["top_exact"] and r["accounted"])
            self.assertEqual(r["words"], self.job["lanes"][0]["words"])
        secs = [r["seconds"] for r in self.job["lanes"]]
        self.assertEqual(secs, sorted(secs, reverse=True))

    def test_ledger(self):
        row = accel.ledger_row(self.job)
        self.assertEqual(row["part"], 60)
        self.assertAlmostEqual(row["seconds"], self.job["lanes"][0]["seconds"])
        led = accel.ledger_with_row(row)
        self.assertEqual(led[-1], row)
        self.assertEqual([r["part"] for r in led[:-1]], [r["part"] for r in accel.ledger()])
        if os.path.exists(os.path.join(os.path.dirname(__file__), "..", ".cache", "cs55", "ledger.json")):
            self.assertEqual(len(led) - 1, 21)  # row 21


if __name__ == "__main__":
    unittest.main()
