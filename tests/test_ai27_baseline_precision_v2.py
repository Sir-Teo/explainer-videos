"""Synthetic controls only: no original models, cached inputs or scientific acceptance."""
from __future__ import annotations
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import numpy as np
import torch
import torch.nn.functional as F
from videos.ai.ai27.baseline_precision_tools import StreamRun, prerequisites
from videos.ai.ai27.baseline_precision_validate import (KINDS, SOURCE_PATHS, digest, independent_topic,
                                                       safe_run, verify_run)
from videos.ai.ai27.baseline_precision import load_baseline_metrics

ROOT = Path(__file__).resolve().parents[1]


class Tiny(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.w = torch.nn.Parameter(torch.linspace(-.3, .4, 11))


def fake_recipe():
    """Execute the real function body with tiny, explicitly fake numerical dependencies."""
    text = (ROOT / 'videos/ai/ai27/compute.py').read_text()
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == 'compute_baselines')
    models, calls = [], []
    def model(name):
        out = Tiny(); models.append(out); return out
    def sample(pol, prompt, n, max_new, temperature, seed):
        calls.append((tuple(prompt), n, max_new, temperature, seed))
        g = np.random.default_rng(seed)
        return [g.integers(1, 20, size=3).tolist() for _ in range(n)]
    def lp(pol, examples):
        a = torch.tensor([[((sum(out) + j * out[j % len(out)]) % 17 - 8) / 11
                           for j in range(11)] for _, out in examples], dtype=torch.float32)
        return a @ pol.w
    p = SimpleNamespace(chat=lambda q: [3, 4, len(q)], sample=sample, seq_logprob=lp,
                        text_of=lambda ids: str(sum(ids)))
    ns = {'torch': torch, 'np': np, 'F': F, '_load_model': model, '_load_rm': lambda name: object(),
          'TOPICS': [f'q{i}' for i in range(30)], 'BASELINES': KINDS, 'SHIFT': 5., 'P': p,
          'line_q': lambda t: 'line ' + t,
          'rm_score': lambda rm, topic, texts: np.array([(int(t) % 23 - 8) / 13 for t in texts], dtype=np.float32)}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<synthetic compute_baselines>', 'exec'), ns)
    return ns['compute_baselines'], models, calls


def rng_reset():
    torch.manual_seed(17); np.random.seed(23); random.seed(31)


def rng_states():
    return torch.get_rng_state().clone(), np.random.get_state(), random.getstate()


class PrecisionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cache = Path(self.tmp.name)

    def capture(self, run_id='synthetic'):
        run = StreamRun(safe_run(self.cache, run_id), root=ROOT,
                        input_pins={'synthetic-control': {'sha256': '0' * 64, 'bytes': 1}},
                        run_kind='synthetic-control')
        fn, models, calls = fake_recipe()
        rng_reset(); original = fn(observer=run); candidate = run.finish(original)
        return run, original, candidate

    def test_default_and_capture_identical_rng_weights_sampling(self):
        fn, models, calls = fake_recipe()
        rng_reset(); a = fn(); first_calls = copy.deepcopy(calls); states = rng_states()
        original_weights = models[0].w.detach().clone()
        calls.clear(); collected = []
        def readonly(event):
            for array in (*event['G_r'], *event['G_1'], *event['rewards']):
                self.assertFalse(array.flags.writeable)
                with self.assertRaises(ValueError): array[0] = 0
            collected.append(event['topic'])
        rng_reset(); b = fn(observer=readonly); later = rng_states()
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(first_calls, calls); self.assertEqual(len(collected), 6)
        self.assertTrue(torch.equal(states[0], later[0])); self.assertEqual(states[2], later[2])
        for x, y in zip(states[1], later[1]): self.assertTrue(np.array_equal(x, y))
        self.assertTrue(torch.equal(original_weights, models[0].w)); self.assertTrue(torch.equal(original_weights, models[1].w))

    def test_stream_validates_and_preserves_default(self):
        run, original, candidate = self.capture()
        restored, binding = verify_run(run.path, root=ROOT, allow_synthetic=True)
        self.assertEqual(candidate, restored); self.assertEqual(binding['status'], 'passed')
        self.assertFalse(binding['later_raw_gradient_replay_available'])
        self.assertNotIn('original_gate_still_failed', binding)
        self.assertFalse(any(run.path.rglob('*.npy')))
        self.assertEqual(json.loads((run.path / 'baselines.json').read_text()), original)
        with self.assertRaises(ValueError): load_baseline_metrics(self.cache, run_id='synthetic')
        with self.assertRaises(ValueError): verify_run(run.path, root=ROOT)

    def test_missing_or_corrupt_receipt_fails(self):
        run, _, _ = self.capture(); p = run.path / 'topics/000.json'; old = p.read_text()
        p.write_text(old + ' ')
        with self.assertRaises(ValueError): verify_run(run.path, root=ROOT, allow_synthetic=True)
        p.unlink()
        with self.assertRaises((FileNotFoundError, ValueError)): verify_run(run.path, root=ROOT, allow_synthetic=True)

    def test_candidate_and_audit_hash_tamper_fails(self):
        for target in ['baselines_f64.json', 'baselines_f64.audit.json']:
            with self.subTest(target=target):
                run, _, _ = self.capture(target.replace('.', '_'))
                p = run.path / target; obj = json.loads(p.read_text()); obj['status'] = 'failed'; p.write_text(json.dumps(obj))
                with self.assertRaises(ValueError): verify_run(run.path, root=ROOT, allow_synthetic=True)

    def test_missing_audit_and_unknown_schema_fail(self):
        run, _, _ = self.capture(); (run.path / 'baselines_f64.audit.json').unlink()
        with self.assertRaises(FileNotFoundError): verify_run(run.path, root=ROOT, allow_synthetic=True)
        m = run.path / 'manifest.json'; data = json.loads(m.read_text()); data['schema_version'] = 99; m.write_text(json.dumps(data))
        with self.assertRaises(ValueError): verify_run(run.path, root=ROOT, allow_synthetic=True)

    def test_sources_are_bound(self):
        run, _, _ = self.capture(); m = run.path / 'manifest.json'; data = json.loads(m.read_text())
        data['sources'][SOURCE_PATHS[0]] = '0' * 64; m.write_text(json.dumps(data))
        with self.assertRaises(ValueError): verify_run(run.path, root=ROOT, allow_synthetic=True)

    def test_original_metadata_cannot_change(self):
        run, _, _ = self.capture(); p = run.path / 'baselines_f64.json'; data = json.loads(p.read_text()); data['shift'] = 9.; p.write_text(json.dumps(data))
        m = run.path / 'manifest.json'; manifest = json.loads(m.read_text()); manifest['artifacts']['baselines_f64.json'] = digest(p); m.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError): verify_run(run.path, root=ROOT, allow_synthetic=True, require_audit=False)

    def test_run_paths_and_overwrite_fail_closed(self):
        for name in ['', '..', '../x', 'a/b', '/tmp/x', 'a.b', 'x' * 65]:
            with self.subTest(name=name), self.assertRaises(ValueError): safe_run(self.cache, name)
        run, _, _ = self.capture()
        with self.assertRaises(FileExistsError): StreamRun(run.path, root=ROOT, input_pins={'synthetic': 1}, run_kind='synthetic-control')
        link = self.cache / 'baseline-runs/link'; link.symlink_to(run.path, target_is_directory=True)
        with self.assertRaises(ValueError): safe_run(self.cache, 'link')

    def test_no_implicit_v2_fallback_or_prerequisite_generation(self):
        with patch.dict(os.environ, {'AI27_BASELINE_RUN': 'missing'}):
            with self.assertRaises(FileNotFoundError): load_baseline_metrics(self.cache)
        with patch.dict(os.environ, {'AI27_BASELINE_RUN': ''}):
            with self.assertRaises(ValueError): load_baseline_metrics(self.cache)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(FileNotFoundError): load_baseline_metrics(self.cache)
        with self.assertRaises(FileNotFoundError): prerequisites(self.cache)

    def test_bad_provenance_and_metric_domains_are_rejected(self):
        from videos.ai.ai27.baseline_precision_validate import validate_live
        run, _, _ = self.capture()
        topic = json.loads((run.path / 'topics/000.json').read_text())
        for value in [float('inf'), -1.]:
            primary = copy.deepcopy(topic['primary'])
            primary['metrics']['none']['squares'][0] = value
            with self.assertRaises(ValueError): validate_live(primary, topic['independent'])
        primary = copy.deepcopy(topic['primary']); primary['metrics']['none']['pairs'][0] = 2.
        with self.assertRaises(ValueError): validate_live(primary, topic['independent'])
        path = run.path / 'manifest.json'; data = json.loads(path.read_text())
        data['run_kind'] = 'original-baseline'; path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'input provenance'):
            verify_run(run.path, root=ROOT, allow_synthetic=True, require_audit=False)

    def test_fp32_affine_before_promotion_and_zero_norm(self):
        from videos.ai.ai27.baseline_precision_tools import torch_metrics
        a = np.array([1e8, 1.0000001, -2.5, 0], dtype=np.float32)
        b = np.array([1e8, 1, 1, 0], dtype=np.float32)
        gr = (a, a.copy(), np.zeros_like(a)); g1 = (b, b.copy(), np.zeros_like(b))
        constants = {kind: [1.00000001, -3.25, 0.] for kind in KINDS}
        expected = a - np.float32(constants['none'][0]) * b
        early = a.astype(np.float64) - constants['none'][0] * b.astype(np.float64)
        self.assertFalse(np.array_equal(expected.astype(np.float64), early))
        primary = torch_metrics(gr, g1, constants)
        independent = independent_topic(gr, g1, constants, chunk=2)
        from videos.ai.ai27.baseline_precision_validate import validate_live
        validate_live(primary, independent)
        self.assertEqual(primary['affine_sha256']['none'][0], hashlib.sha256(expected.tobytes()).hexdigest())
        self.assertTrue(all(np.isfinite(independent['metrics'][kind]['pairs']).all() for kind in KINDS))


if __name__ == '__main__':
    unittest.main()
