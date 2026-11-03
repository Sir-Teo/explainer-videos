"""Synthetic numerical checks only; these do not validate Part 13 model activations."""
import math
import unittest
import numpy as np
from videos.ai.ai19 import attn

class AttentionSynthetic(unittest.TestCase):
    def test_tiled_matches_independent_row_reference(self):
        rng = np.random.default_rng(1907)
        for length, dim in [(1, 3), (7, 5), (16, 8), (19, 7)]:
            q, k, v = (rng.normal(size=(length, dim)) * scale for scale in (4, 4, 1))
            for causal in (False, True):
                ref = np.empty_like(q)
                for i in range(length):
                    scores = (k[:i+1] if causal else k) @ q[i] / math.sqrt(dim)
                    weights = np.exp(scores - scores.max())
                    weights /= weights.sum()
                    ref[i] = weights @ (v[:i+1] if causal else v)
                for br, bc in [(1, 1), (3, 4), (8, 3), (64, 64)]:
                    with self.subTest(length=length, dim=dim, causal=causal, br=br, bc=bc):
                        np.testing.assert_allclose(attn.flash_attention(q, k, v, br, bc, causal), ref,
                                                   atol=2e-12, rtol=2e-12)

    def test_split_decode_and_online_softmax(self):
        rng = np.random.default_rng(1919)
        q = rng.normal(size=7) * 4
        k, v = rng.normal(size=(17, 7)) * 4, rng.normal(size=(17, 7))
        scores = k @ q / math.sqrt(7)
        p = np.exp(scores - scores.max()); p /= p.sum()
        for tiles in (1, 3, 8, 17):
            _, actual = attn.online_softmax_trace(scores, tiles)
            np.testing.assert_allclose(actual, p, atol=1e-14, rtol=1e-14)
        for splits in (1, 2, 4, 8, 17):
            got, parts = attn.split_kv_decode(q, k, v, splits)
            self.assertEqual(len(parts), splits)
            np.testing.assert_allclose(got, p @ v, atol=1e-13, rtol=1e-13)

    def test_counted_io_matches_closed_form_with_partial_tiles(self):
        for n in (1, 31, 64, 127, 513):
            for d in (4, 16, 64):
                for m in (64, 256, 4096):
                    with self.subTest(n=n, d=d, m=m):
                        self.assertEqual(attn.io_flash_counted(n, d, m), attn.io_flash_formula(n, d, m))

if __name__ == '__main__':
    unittest.main()
