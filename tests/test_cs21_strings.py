"""Part 21's instruments against brute force."""

from __future__ import annotations

import random
import unittest
import zlib

import numpy as np

from explainer.cs.algo import strings as S


def brute(text, pat):
    return [i for i in range(len(text) - len(pat) + 1) if text[i:i + len(pat)] == pat]


class Strings(unittest.TestCase):
    def setUp(self):
        rng = random.Random(21)
        self.texts = [bytes(rng.choice(b"ab") for _ in range(300)), bytes(rng.choice(b"acgt") for _ in range(500)),
                      b"abracadabra" * 20, b"a" * 200 + b"b"]
        self.pats = [b"ab", b"aab", b"abab", b"acg", b"abra", b"cadabra", b"a" * 10 + b"b", b"a" * 5, b"tttt"]

    def test_matchers(self):
        for t in self.texts:
            for p in self.pats:
                want = brute(t, p)
                self.assertEqual(S.naive(t, p)[0], want)
                self.assertEqual(S.naive_fast(t, p), S.naive(t, p))
                self.assertEqual(S.rabin_karp(t, p)[0], want)
                self.assertEqual(S.rabin_karp(t, p, mod=97)[0], want)        # spurious hits are filtered
                self.assertEqual(S.kmp(t, p)[0], want)
                self.assertLessEqual(S.kmp(t, p)[1], 2 * len(t))
                self.assertEqual(S.horspool(t, p)[0], want)
                self.assertEqual(S.boyer_moore(t, p)[0], want)

    def test_automaton(self):
        pat = b"abab"
        d = S.kmp_automaton(pat, b"ab")
        q, hits = 0, []
        for i, c in enumerate(b"abababbabab"):
            q = d[q][c]
            if q == len(pat):
                hits.append(i - 3)
        self.assertEqual(hits, brute(b"abababbabab", pat))

    def test_aho_corasick(self):
        pats = [b"he", b"she", b"his", b"hers", b"a", b"abra"]
        ac = S.AhoCorasick(pats)
        for t in self.texts + [b"ushers and his abra"]:
            hits, _ = ac.search(t)
            for p in pats:
                self.assertEqual(hits[p], len(brute(t, p)))

    def test_suffix_array_lcp_search(self):
        for t in self.texts + [b"banana$", b"mississippi\x00"]:
            sa = S.suffix_array(t)
            self.assertEqual(sa.tolist(), S.suffix_array_naive(t))
            lcp = S.lcp_kasai(t, sa)
            for i in range(1, len(t)):
                a, b = t[sa[i - 1]:], t[sa[i]:]
                k = 0
                while k < min(len(a), len(b)) and a[k] == b[k]:
                    k += 1
                self.assertEqual(lcp[i], k)
            for p in self.pats:
                lo, hi, _ = S.sa_search(t, sa, p)
                self.assertEqual(sorted(sa[lo:hi].tolist()), brute(t, p))

    def test_bwt_fm(self):
        rng = random.Random(3)
        for t in [b"banana\x00", b"abracadabra\x00", bytes(rng.choice(b"acgt") for _ in range(2000)) + b"\x00"]:
            sa = S.suffix_array(t)
            L = S.bwt_from_sa(t, sa)
            self.assertEqual(S.inverse_bwt(L), t)
            fm = S.FMIndex(t, sa, step=16, sa_step=8)
            for p in (b"a", b"an", b"ana", b"abra", b"acg", b"gtac", b"zz"):
                cnt, (lo, hi) = fm.count(p)
                self.assertEqual(cnt, len(brute(t, p)))
                self.assertEqual(sorted(fm.locate(r) for r in range(lo, hi)), brute(t, p))
        self.assertEqual(S.bwt_from_sa(b"banana\x00", S.suffix_array(b"banana\x00")), b"annb\x00aa")

    def test_compression(self):
        data = (b"it was the best of times, it was the worst of times, " * 30) + bytes(range(256))
        tok = S.lz77(data)
        self.assertEqual(S.lz77_decode(tok), data)
        sz = S.deflate_size(tok)
        self.assertLess(sz["bytes"], len(zlib.compress(data, 9)) * 1.6)
        codes, nd = S.lzw(data)
        self.assertEqual(nd, 256 + len(codes) - 1)
        r = S.RANS(data)
        enc = r.encode(data)
        self.assertEqual(r.decode(enc, len(data)), data)
        self.assertLess(len(enc) * 8, S.rans_size(data) * 1.05 + 64)
        mtf = S.move_to_front(b"aaabbbaaa")
        self.assertEqual(mtf.tolist(), [97, 0, 0, 98, 0, 0, 1, 0, 0])

    def test_alignment_and_diff(self):
        S_ = S.needleman_wunsch("GATTACA", "GCATGCU")
        self.assertEqual(S_[-1, -1], 0)
        best, end, start, _ = S.smith_waterman("xxxACGTACGTyyy", "zzACGTACGTzz")
        self.assertEqual(best, 16)
        rng = random.Random(9)
        for _ in range(40):
            a = [rng.choice("abc") for _ in range(rng.randint(0, 25))]
            b = [rng.choice("abc") for _ in range(rng.randint(0, 25))]
            D, ops, _, _ = S.myers(a, b)
            self.assertEqual(D, len(a) + len(b) - 2 * S.lcs_len(a, b))
            self.assertEqual([x for o, x in ops if o != "+"], a)
            self.assertEqual([x for o, x in ops if o != "-"], b)
            self.assertEqual(sum(o != "=" for o, _ in ops), D)
        anchors = S.patience_anchors(list("abcdxe"), list("xabcde"))
        self.assertTrue(all(a < b for (a, _), (b, _) in zip(anchors, anchors[1:])))

    def test_rolling_and_chunks(self):
        rng = np.random.default_rng(1)
        data = rng.integers(0, 256, 5000, dtype=np.uint8).tobytes()
        w = S.adler32_rolling(data, 64)
        for k in (0, 17, 4000):
            blk = data[k:k + 64]
            a = sum(blk) % 65536
            b = sum((64 - i) * x for i, x in enumerate(blk)) % 65536
            self.assertEqual(int(w[k]), (b << 16) | a)
        big = rng.integers(0, 256, 400_000, dtype=np.uint8).tobytes()
        cuts = S.cdc_chunks(big)
        edited = big[:200_000] + b"INSERTED" + big[200_000:]
        cuts2 = S.cdc_chunks(edited)
        h1, h2 = set(S.chunk_hashes(big, cuts)), set(S.chunk_hashes(edited, cuts2))
        self.assertGreaterEqual(len(h1 & h2), len(h1) - 3)

    def test_periodicity(self):
        self.assertEqual(S.manacher(b"xabacabay"), (1, 7))
        self.assertEqual(S.periods(b"abaababaab")[:3], [5, 8, 10])
        self.assertEqual(S.duval("banana"), ["b", "an", "an", "a"])
        f = S.duval("abracadabra")
        self.assertEqual("".join(f), "abracadabra")
        self.assertTrue(all(f[i] >= f[i + 1] for i in range(len(f) - 1)))


if __name__ == "__main__":
    unittest.main()
