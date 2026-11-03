"""Check the illustrated CTC lattice against exhaustive path enumeration."""
import itertools
import unittest

import numpy as np

from videos.ai.ai23.audio import ALPHA, ctc_lattice


def collapse(path):
    out = []
    prev = None
    for c in path:
        if c != prev and c != 0:
            out.append(ALPHA[c])
        prev = c
    return ''.join(out)


class CTCLatticeContracts(unittest.TestCase):
    def test_exhaustive_marginals_posteriors_and_best_path(self):
        rng = np.random.default_rng(23)
        symbols = [0, ALPHA.index('a'), ALPHA.index('b')]
        # Repeated labels need a blank; distinct labels can skip one.
        for text in ['a', 'ab', 'aa', 'aba']:
            for frames in range(2, 7):
                raw = rng.uniform(.05, 1, size=(frames, len(symbols)))
                probs = raw / raw.sum(axis=1, keepdims=True)
                lp = np.full((frames, len(ALPHA)), -1000.)
                lp[:, symbols] = np.log(probs)
                candidates = []
                for path in itertools.product(symbols, repeat=frames):
                    if collapse(path) == text:
                        p = np.prod([probs[t, symbols.index(c)] for t, c in enumerate(path)])
                        candidates.append((path, p))
                if not candidates:
                    continue
                la, gamma, best, total, ext = ctc_lattice(lp, text)
                expected = sum(p for _, p in candidates)
                self.assertAlmostEqual(np.exp(total), expected, places=12, msg=(text, frames))
                np.testing.assert_allclose(gamma.sum(axis=1), 1., atol=1e-12)
                for t in range(frames):
                    for c in symbols:
                        expected_occ = sum(p for path, p in candidates if path[t] == c) / expected
                        actual_occ = sum(gamma[t, s] for s, x in enumerate(ext) if x == c)
                        self.assertAlmostEqual(actual_occ, expected_occ, places=12, msg=(text, frames, t, c))
                path = tuple(ext[s] for s in best)
                self.assertEqual(collapse(path), text)
                best_p = np.prod([probs[t, symbols.index(c)] for t, c in enumerate(path)])
                self.assertAlmostEqual(best_p, max(p for _, p in candidates), places=12)

    def test_groupnorm_couples_distant_frames(self):
        try:
            import torch
        except ImportError:
            self.skipTest("PyTorch is unavailable")
        from videos.ai.ai23.audio import ctc_net
        torch.manual_seed(23)
        model = ctc_net(width=4).eval()
        x = torch.randn(1, 40, 240)
        changed = x.clone()
        changed[:, :, 200:] += 5
        # Frame 0 is outside the changed input's convolutional receptive field.
        # GroupNorm still shares statistics over the whole time dimension.
        with torch.no_grad():
            delta = (model(x)[:, 0] - model(changed)[:, 0]).abs().max().item()
        self.assertGreater(delta, 1e-5)


if __name__ == '__main__':
    unittest.main()
