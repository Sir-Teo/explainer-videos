"""Prepared cache-only guard probes. Execute only in the released QA window.

No model construction, dataset API, explicit numerical inference, optimization,
migration or download. Package imports may transitively load pinned Torch/Manim.
Synthetic tiny native files never count as scientific acceptance evidence.
"""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from explainer.ai.cache import Cache
from videos.ai.ai20.sampling_cache import (
    SamplingCache, consumer_class, consumer_source_sha256)


class SamplingCacheGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cache = SamplingCache()
        self.cache.dir = Path(self.temp.name)

    def native(self, name='toys'):
        self.cache.save(name, {'synthetic_probe': True})

    def test_compute_main_class_uses_canonical_module_and_preserves_qualname(self):
        cls = type('Inline', (), {'__module__': '__main__'})
        compute_file = Path(__file__).resolve().parents[1] / 'videos/ai/ai20/compute.py'
        with patch.object(sys.modules['__main__'], '__file__', str(compute_file), create=True):
            self.assertEqual(consumer_class(cls()), 'videos.ai.ai20.compute.' + cls.__qualname__)

    def test_unrelated_main_class_is_not_canonicalized(self):
        cls = type('Inline', (), {'__module__': '__main__'})
        unrelated = self.cache.dir / 'compute.py'
        with patch.object(sys.modules['__main__'], '__file__', str(unrelated), create=True):
            self.assertEqual(consumer_class(cls()), '__main__.' + cls.__qualname__)

    def test_direct_native_read_never_calls_base_loader(self):
        self.native()
        with patch.object(Cache, 'load', side_effect=AssertionError('auto-loader reached')):
            self.assertEqual(self.cache.load('toys'), {'synthetic_probe': True})

    def test_invalid_native_does_not_invoke_base_loader(self):
        self.native()
        (self.cache.dir / 'toys.json').write_text('{}')
        with patch.object(Cache, 'load', side_effect=AssertionError('auto-loader reached')):
            with self.assertRaises(RuntimeError):
                self.cache.load('toys')

    def test_native_read_needs_no_raw_data_or_model_directory(self):
        self.native()
        self.assertFalse((self.cache.dir / 'models').exists())
        self.assertEqual(self.cache.load('toys'), {'synthetic_probe': True})

    def test_consumer_source_mismatch_fails(self):
        self.native()
        changed = dict(consumer_source_sha256(), **{'gendigits.py': '0' * 64})
        with patch('videos.ai.ai20.sampling_cache.consumer_source_sha256', return_value=changed):
            with self.assertRaises(RuntimeError):
                self.cache.load('toys')

    def test_classifier_dependency_precedes_producer(self):
        calls = []
        items = {'gan': lambda: calls.append('producer') or {}}
        with patch.object(sys, 'argv', ['compute', 'gan']):
            with self.assertRaises(RuntimeError):
                self.cache.main(items)
        self.assertEqual(calls, [])

    def test_no_names_explicit_cli_runs_all_in_order(self):
        calls = []
        def producer(name):
            def run():
                calls.append(name)
                return {'synthetic_probe': True}
            return run
        items = {name: producer(name) for name in ('toys', 'classifier', 'gan')}
        with patch.object(sys, 'argv', ['compute']):
            self.cache.main(items)
        self.assertEqual(calls, list(items))
        self.assertEqual(self.cache.load('gan'), {'synthetic_probe': True})

    def test_quick_partial_scale_mismatch_preserves_completed_record(self):
        self.cache.scale = .01
        part = self.cache.partial('cnf', {'v': 1, 'steps': 1500})
        part['s0'] = {'synthetic_done': True}
        path = self.cache.dir / 'cnf.partial.json'
        before = path.read_bytes()
        self.cache.scale = .05
        with self.assertRaises(RuntimeError):
            self.cache.partial('cnf', {'v': 1, 'steps': 1500})
        self.assertEqual(path.read_bytes(), before)

    def test_quick_partial_source_mismatch_preserves_completed_record(self):
        part = self.cache.partial('cnf', {'v': 1, 'steps': 1500})
        part['s0'] = {'synthetic_done': True}
        path = self.cache.dir / 'cnf.partial.json'
        before = path.read_bytes()
        changed = dict(consumer_source_sha256(), **{'compute.py': '0' * 64})
        with patch('videos.ai.ai20.sampling_cache.consumer_source_sha256', return_value=changed):
            with self.assertRaises(RuntimeError):
                self.cache.partial('cnf', {'v': 1, 'steps': 1500})
        self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
