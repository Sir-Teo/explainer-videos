import math
import random
import unittest
import zlib

from explainer.cs.algo import codes as C


class TestBinaryCodes(unittest.TestCase):
    def test_hamming74_corrects_every_single_error(self):
        for d in range(16):
            bits = [(d >> i) & 1 for i in range(4)]
            c = C.hamming74_encode(bits)
            self.assertEqual(C.hamming74_syndrome(c), 0)
            for e in range(7):
                c2 = list(c)
                c2[e] ^= 1
                self.assertEqual(C.hamming74_decode(c2), (bits, e + 1))

    def test_secded_detects_doubles(self):
        c = C.hamming74_encode([1, 0, 1, 1])
        c8 = c + [sum(c) % 2]
        self.assertEqual(C.secded_decode(c8)[1], "ok")
        one = list(c8)
        one[3] ^= 1
        self.assertEqual(C.secded_decode(one), ([1, 0, 1, 1], "corrected"))
        two = list(c8)
        two[1] ^= 1
        two[5] ^= 1
        self.assertEqual(C.secded_decode(two)[1], "double")

    def test_golay(self):
        w = C.codewords(C.golay23_generators())
        dist = C.weight_distribution(w, 23)
        self.assertEqual(C.min_distance(w), 7)
        self.assertEqual({i: a for i, a in enumerate(dist) if a},
                         {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288, 15: 506, 16: 253, 23: 1})
        # perfect: spheres of radius 3 tile the cube
        self.assertEqual(len(w) * sum(math.comb(23, i) for i in range(4)), 2 ** 23)

    def test_bounds_order(self):
        for d in (0.05, 0.1, 0.2, 0.3, 0.4):
            self.assertLessEqual(C.gv_bound(d), min(C.mrrw_bound(d), C.hamming_bound(d)) + 1e-12)
            self.assertLessEqual(C.hamming_bound(d), C.singleton_bound(d) + 1e-12)
        self.assertLess(C.mrrw_bound(0.35), C.hamming_bound(0.35))        # the LP bound wins for large distance
        self.assertGreater(C.mrrw_bound(0.05), C.hamming_bound(0.05))     # and Hamming's for small


class TestFieldsAndRS(unittest.TestCase):
    def test_zero_inverse_and_zero_parity(self):
        for inverse in (lambda: C.gf_inv(0), lambda: C.gf_pow(0, -1)):
            with self.assertRaises(ZeroDivisionError):
                inverse()
        self.assertEqual(C.rs_encode([1, 2, 3], 0), [1, 2, 3])
        self.assertEqual(C.rs_decode([1, 2, 3], 0), ([1, 2, 3], []))
        self.assertEqual(C.gp_divmod([7], [1, 2, 3]), ([], [7]))
        with self.assertRaises(ValueError):
            C.rs_decode(C.rs_encode([1, 2], 4), 4, [0, 0])

    def test_gf256(self):
        for a in range(1, 256):
            self.assertEqual(C.gf_mul(a, C.gf_inv(a)), 1)
            for b in (1, 2, 29, 200):
                self.assertEqual(C.gf_mul(a, b), C.gf_mul_slow(a, b))
        self.assertEqual(len({C.gf_pow(2, i) for i in range(255)}), 255)

    def test_rs_errors_and_erasures(self):
        rng = random.Random(5)
        msg = [rng.randrange(256) for _ in range(20)]
        cw = C.rs_encode(msg, 16)
        for ne, nf in ((8, 0), (0, 16), (4, 8), (7, 2)):
            for _ in range(20):
                bad = list(cw)
                pos = rng.sample(range(len(cw)), ne + nf)
                for p in pos:
                    bad[p] ^= rng.randrange(1, 256)
                self.assertEqual(C.rs_decode(bad, 16, erase_pos=pos[ne:])[0], cw)

    def test_evaluation_view(self):
        p, msg, xs = 97, [5, 3, 2], list(range(1, 10))
        y = C.rs_eval_encode(msg, xs, p)
        pts = list(zip(xs, y))
        self.assertEqual(C.lagrange_coeffs(pts[2:5], p), msg)
        y[0] = (y[0] + 1) % p
        y[4] = (y[4] + 50) % p
        y[7] = (y[7] + 9) % p
        dec, bad = C.berlekamp_welch(list(zip(xs, y)), 3, 3, p)
        self.assertEqual(dec, msg)
        self.assertEqual(bad, [1, 5, 8])

    def test_welch_reports_actual_errors_with_unused_budget(self):
        p, msg, xs = 97, [5, 3, 2], list(range(9))
        for errors in range(4):
            ys = C.rs_eval_encode(msg, xs, p)
            for i in range(errors):
                ys[i] = (ys[i] + 1) % p
            self.assertEqual(C.berlekamp_welch(list(zip(xs, ys)), 3, 3, p), (msg, xs[:errors]))
        with self.assertRaises(ValueError):
            C.berlekamp_welch([(0, 1), (97, 1), (2, 3)], 3, 0, p)


class TestQrAndCrc(unittest.TestCase):
    def test_qr_round_trip_with_damage(self):
        rng = random.Random(3)
        M, info = C.qr_encode("CS BUILT PART 28", "Q")
        self.assertEqual(C.qr_decode(M)["text"], "CS BUILT PART 28")
        pos = info["positions"]
        hit = rng.sample(range(len(info["codewords"])), 11)          # 11 whole codewords wrong: the limit
        D = [row[:] for row in M]
        for k in hit:
            x, y = pos[8 * k]
            D[y][x] = not D[y][x]
        out = C.qr_decode(D)
        self.assertEqual(out["text"], "CS BUILT PART 28")
        self.assertEqual(sorted(out["errors"]), sorted(hit))

    def test_crc(self):
        for data in (b"", b"a", b"The quick brown fox", bytes(range(256))):
            self.assertEqual(C.crc32(data), zlib.crc32(data))
        bits = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1]
        r = C.crc_remainder(bits, [1, 0, 1, 1])
        # appending the remainder makes the message divisible
        full = bits + r
        reg = list(full)
        poly = [1, 0, 1, 1]
        for i in range(len(full) - 3):
            if reg[i]:
                for j, pb in enumerate(poly):
                    reg[i + j] ^= pb
        self.assertEqual(reg[-3:], [0, 0, 0])


class TestModern(unittest.TestCase):
    def test_bp_stops_on_valid_incorrect_codeword(self):
        # With this fixed channel sample, 11 is a valid but incorrect word of the
        # length-two repetition code. Parity permits stopping; truth cannot be used.
        trace, unsat = C.ldpc_bp_trace([(0, 0), (0, 1)], 1, 2, 0.49, random.Random(7), iters=4)
        self.assertEqual(trace, [2, 2])
        self.assertEqual(unsat, [0])
        self.assertEqual(C.ldpc_bp_bsc([(0, 0), (0, 1)], 1, 2, 0.49, 1, random.Random(7)), (1.0, 1.0))

    def test_polar_rejects_non_power_of_two_blocks(self):
        import numpy as np
        for n in (0, 3, 6):
            with self.assertRaises(ValueError):
                C.polar_encode([0] * n)
            with self.assertRaises(ValueError):
                C.polar_sc(np.ones(n), [False] * n)

    def test_viterbi_and_ldpc_and_polar(self):
        rng = random.Random(4)
        bits = [rng.randrange(2) for _ in range(100)]
        self.assertEqual(C.viterbi(C.conv_encode(bits)), bits)
        self.assertAlmostEqual(C.de_bec_threshold(3, 6), 0.4294, places=3)
        edges, m = C.gallager_ldpc(600, 3, 6, rng)
        self.assertEqual(C.ldpc_bp_bsc(edges, m, 600, 0.02, 5, rng), (0.0, 0.0))
        u = [rng.randrange(2) for _ in range(16)]
        x = C.polar_encode(u)
        import numpy as np
        uh, xh = C.polar_sc(np.array([4.0 if b == 0 else -4.0 for b in x]), [False] * 16)
        self.assertEqual((uh, xh), (u, x))
        z = C.polar_bhattacharyya(8, 0.5)
        self.assertAlmostEqual(sum(1 - zz for zz in z) / 256, 0.5, places=9)    # capacity is conserved

    def test_storage_and_local(self):
        rng = random.Random(6)
        disks = [[rng.randrange(256) for _ in range(8)] for _ in range(5)]
        P, Q = C.raid6_parity(disks)
        self.assertEqual(C.raid6_recover_two(disks, 0, 3, P, Q), (disks[0], disks[3]))
        self.assertGreaterEqual(C.lt_symbols_needed(200, rng), 200)
        w = C.hadamard_encode(0b101101, 6)
        self.assertEqual([C.hadamard_local_decode(w, 6, i, rng) for i in range(6)], [1, 0, 1, 1, 0, 1])


if __name__ == "__main__":
    unittest.main()
