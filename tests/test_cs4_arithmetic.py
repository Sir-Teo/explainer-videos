"""Part 4 (Arithmetic): the adders, multipliers and ALU of explainer/cs/pebble/blocks.py, and the SRT divider of
videos/cs/cs4/compute.py, checked against Python's integers."""

from __future__ import annotations

import unittest

import numpy as np

from explainer.cs.pebble import blocks as B
from explainer.cs.pebble.hdl import simulate


def grid(*widths):
    total = sum(widths)
    p = np.arange(1 << total, dtype=np.int64)
    out, sh = [], 0
    for w in widths:
        out.append((p >> sh) & ((1 << w) - 1))
        sh += w
    return out


class Adders(unittest.TestCase):
    def test_every_adder_exhaustive_at_8_bits(self):
        a, b, c = grid(8, 8, 1)
        designs = [B.ripple_adder(8), B.carry_skip_adder(8, 2), B.carry_select_adder(8), B.carry_select_adder(8, [2, 3, 3])]
        designs += [B.prefix_adder(8, k) for k in B.PREFIX]
        for d in designs:
            r = simulate(d, {"a": a, "b": b, "cin": c})
            got = r["s"].astype(np.int64) + (r["cout"].astype(np.int64) << 8)
            self.assertTrue(np.array_equal(got, a + b + c), d.name)

    def test_prefix_networks_cover_every_prefix(self):
        for n in (5, 8, 13, 16, 32):
            for kind in B.PREFIX:
                spans = [{i} for i in range(n)]
                for level in B.prefix_levels(n, kind):
                    new = [set(s) for s in spans]
                    for i, j in level:
                        self.assertEqual(max(spans[j]) + 1, min(spans[i]), (kind, n))  # adjacent blocks only
                        new[i] = spans[i] | spans[j]
                    spans = new
                self.assertEqual(spans, [set(range(i + 1)) for i in range(n)], (kind, n))

    def test_kogge_stone_size_and_depth(self):
        for k in range(1, 7):
            n = 2 ** k
            lv = B.prefix_levels(n, "kogge-stone")
            self.assertEqual(len(lv), k)
            self.assertEqual(sum(len(x) for x in lv), n * k - n + 1)

    def test_ripple_delay_is_2n_plus_1(self):
        for n in (4, 8, 16):
            c = B.ripple_adder(n)
            a = np.array([(1 << n) - 1])
            st = c.settle({"a": a, "b": np.array([0]), "cin": np.array([1])})
            self.assertEqual(int(st[0]), 2 * n + 1)

    def test_carry_skip_has_a_false_path(self):
        n = 32
        c = B.carry_skip_adder(n, 4)
        rng = np.random.default_rng(0)
        a = rng.integers(0, 1 << n, 3000)
        b = rng.integers(0, 1 << n, 3000)
        a[:n], b[:n] = (1 << n) - 1, 1 << np.arange(n)
        st = c.settle({"a": a, "b": b, "cin": np.zeros(3000, np.int64)})
        self.assertGreater(c.depth(), int(st.max()) + 30)
        self.assertLess(int(st.max()), B.ripple_adder(n).depth())


class Multipliers(unittest.TestCase):
    def test_exhaustive_at_6_bits(self):
        a, b = grid(6, 6)
        for c in (B.array_multiplier(6), B.tree_multiplier(6, "wallace"), B.tree_multiplier(6, "dadda")):
            r = simulate(c, {"a": a, "b": b})
            self.assertTrue(np.array_equal(r["p"].astype(np.int64), a * b), c.name)

    def test_tree_stages_are_logarithmic(self):
        self.assertEqual(B.tree_multiplier(8, "wallace").stages, 4)   # 8 -> 6 -> 4 -> 3 -> 2
        self.assertEqual(B.tree_multiplier(16, "dadda").stages, 6)

    def test_booth_digits(self):
        from videos.cs.cs4.compute import booth4
        for b in range(-128, 128):
            d = booth4(b & 0xFF, 8)
            self.assertTrue(all(-2 <= x <= 2 for x in d))
            self.assertEqual(sum(x * 4 ** i for i, x in enumerate(d)), b)


class Alu(unittest.TestCase):
    def test_8_bit_alu_exhaustive(self):
        a, b, op = grid(8, 8, 4)
        keep = op < len(B.ALU_OPS)
        a, b, op = a[keep], b[keep], op[keep]
        r = simulate(B.alu(8), {"a": a, "b": b, "op": op})
        self.assertTrue(np.array_equal(r["y"].astype(np.int64), B.alu_spec(a, b, op, 8)))

    def test_32_bit_alu_against_the_emulator(self):
        from explainer.cs.pebble.emu import sext
        rng = np.random.default_rng(1)
        V = 3000
        A = rng.integers(0, 1 << 32, V)
        Bv = rng.integers(0, 1 << 32, V)
        Bv[: V // 3] = rng.integers(0, 40, V // 3)
        OP = rng.integers(0, len(B.ALU_OPS), V)
        r = simulate(B.alu(32), {"a": A, "b": Bv, "op": OP})
        M = 0xFFFF_FFFF
        for x, y, o, got in zip(A.tolist(), Bv.tolist(), OP.tolist(), r["y"].tolist()):
            name = B.ALU_OPS[o]
            want = {"add": x + y, "sub": x - y, "and": x & y, "or": x | y, "xor": x ^ y, "sll": x << (y & 31),
                    "srl": x >> (y & 31), "sra": sext(x, 32) >> (y & 31), "slt": int(sext(x, 32) < sext(y, 32)),
                    "sltu": int(x < y)}[name] & M
            self.assertEqual(int(got), want, (name, x, y))


class Division(unittest.TestCase):
    def test_srt_table_and_divisions(self):
        from videos.cs.cs4.compute import SRT_F, srt_array, srt_divide, srt_table
        tab = srt_table()
        self.assertEqual(len(tab), 1056)
        T = srt_array(tab)
        rng = np.random.default_rng(2)
        X = rng.integers(1 << SRT_F, 1 << (SRT_F + 1), 20000)
        D = rng.integers(1 << SRT_F, 1 << (SRT_F + 1), 20000)
        Q, _ = srt_divide(X, D, T)
        q = 4 * Q / 4.0 ** 14
        self.assertLess(float(np.max(np.abs(q - X / D) / (X / D))), 4.0 ** -12)

    def test_restoring(self):
        from videos.cs.cs4.compute import restoring
        for x in range(256):
            for d in (1, 3, 7, 13, 200):
                bits = [s["q"] for s in restoring(x, d)]
                self.assertEqual(int("".join(map(str, bits)), 2), x // d)


if __name__ == "__main__":
    unittest.main()
