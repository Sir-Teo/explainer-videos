"""Pinned public METR facts and deterministic fits; no training or render acceptance."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from test_ai29_independent_science import c, real_cache_class

FIXTURE = json.loads((Path(__file__).parent / 'fixtures/ai29_metr_20261103.json').read_text())


class MetrPrecision(unittest.TestCase):
    def test_all_26_published_rows_and_provenance(self):
        self.assertEqual([list(row) for row in c.METR], FIXTURE['rows'])
        self.assertEqual(c.METR_PROVENANCE, FIXTURE['provenance'])
        self.assertEqual(len(c.METR), 26)
        self.assertEqual(c.RELIABLE, 960)
        for name, date, p50, lo, hi, p80, frontier in c.METR:
            self.assertTrue(np.isfinite([p50, lo, hi, p80]).all())
            self.assertTrue(0 < lo <= p50 <= hi)
            self.assertTrue(0 < p80 <= p50)
        self.assertEqual([r[3:5] for r in c.METR[:3]],
                         [(0.009994, 0.141825), (0.093319, 0.221209), (0.255148, 1.115905)])

    def test_fit_independent_centered_covariance_and_seed(self):
        a, b = c.compute_metr(boots=64), c.compute_metr(boots=64)
        self.assertEqual(a['doubling_ci'], b['doubling_ci'])
        self.assertEqual(a['n_fit'], 14)
        self.assertEqual(a['n_all'], 17)
        self.assertEqual([r['benchmark'] for r in a['rows']],
                         ['METR-Horizon-v1.0'] * 3 + ['METR-Horizon-v1.1'] * 23)
        for field, since2023, metric, expected in [
            ('doubling_2023', True, 'p50', 128.74380265078),
            ('doubling_all', False, 'p50', 187.77754378812733),
            ('doubling_80', True, 'p80', 133.4053133040359),
        ]:
            rows = [r for r in a['rows'] if r['sota'] and r['p50'] <= 960
                    and (not since2023 or r['date'] >= '2023-01-01')]
            x = np.array([r['t'] for r in rows]); y = np.log2([r[metric] for r in rows])
            slope = np.dot(x-x.mean(), y-y.mean()) / np.dot(x-x.mean(), x-x.mean())
            self.assertAlmostEqual(a[field], 365.25/slope, places=10)
            self.assertAlmostEqual(a[field], expected, places=10)
        self.assertTrue(np.isfinite(a['doubling_ci']).all())
        self.assertLess(a['doubling_ci'][0], a['doubling_ci'][1])

    def test_real_cache_rejects_legacy_and_npz_shadowing(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = real_cache_class()('ai29'); cache.dir = Path(directory)
            cache.items = {'metr': lambda: self.fail('implicit compute')}
            with patch.object(c, 'CACHE', cache):
                path = cache.path('metr')
                for metadata in ({'rows': []}, {'recipe_version': 'old'},
                                 {'recipe_version': c.RECIPE_VERSIONS['metr']}):
                    path.write_text(json.dumps(metadata))
                    with self.assertRaises(ValueError):
                        c.load('metr')
                metadata = {'recipe_version': c.RECIPE_VERSIONS['metr'],
                            'provenance': c.METR_PROVENANCE}
                path.write_text(json.dumps(metadata))
                np.savez(path.with_suffix('.npz'), coef_2023=np.array([1., 2.]))
                self.assertEqual(c.load('metr')['provenance'], c.METR_PROVENANCE)
                for key in ('recipe_version', 'provenance'):
                    np.savez(path.with_suffix('.npz'), **{key: np.array('wrong')})
                    with self.assertRaisesRegex(ValueError, 'NPZ shadows'):
                        c.load('metr')
                path.with_suffix('.npz').unlink(); path.unlink()
                with self.assertRaises(FileNotFoundError):
                    c.load('metr')

    def test_only_metr_adds_new_protocol(self):
        expected = {name: 'independent-20261103-v1'
                    for name in ('agent', 'lane', 'dreamer', 'klbal', 'detour', 'fast')}
        expected['metr'] = 'metr-th1.1-20261103-aae31902b051-v1'
        self.assertEqual(c.RECIPE_VERSIONS, expected)
        self.assertEqual(c.ITEMS['metr'].__name__, 'run')


if __name__ == '__main__':
    unittest.main()
