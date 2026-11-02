"""Synthetic input-boundary and source-expression checks; no scientific outcomes or render acceptance."""
import ast
import hashlib
import importlib.util
import json
import io
import zipfile
from pathlib import Path
import re
import tempfile
import types
import unittest
from unittest import mock

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai10'
spec = importlib.util.spec_from_file_location('ai10_verified_inputs', PART / 'inputs.py')
inputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inputs)


def function(filename, name):
    return next(n for n in ast.walk(ast.parse((PART / filename).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


class CachedInputs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reader = inputs.SceneInputs(self.root)
        self.manifest = {'version': 1, 'inputs': {}}

    def file(self, name, raw):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return {'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}

    def save_manifest(self):
        path = self.root / '.cache/ai10/scene-inputs.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.manifest))

    def cache(self, data=None, path='.cache/ai10/example.json', **extra):
        entry = {'kind': 'canonical', 'json': self.file(path, json.dumps(data or {'value': 3}).encode()), **extra}
        self.manifest['inputs']['ai10/example'] = entry
        self.save_manifest()
        return entry

    def test_missing_manifest_does_not_generate_or_import_producers(self):
        with mock.patch('importlib.import_module', side_effect=AssertionError('producer import')):
            with self.assertRaises(FileNotFoundError):
                self.reader.load('ai10', 'example')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_missing_declared_input_does_not_generate(self):
        self.cache()
        path = self.root / '.cache/ai10/example.json'
        path.unlink()
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*'))
        with self.assertRaises(FileNotFoundError):
            self.reader.load('ai10', 'example')
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*')))

    def test_json_and_arrays_keep_values_and_intentional_missing_slots(self):
        entry = self.cache({'value': 3, 'evals': [[0, 7, float('nan')]]})
        array_path = self.root / '.cache/ai10/example.npz'
        np.savez_compressed(array_path, curve=np.array([[0, 7.25], [100, 3.25]], dtype=np.float32))
        entry['npz'] = {'path': '.cache/ai10/example.npz',
                        'sha256': hashlib.sha256(array_path.read_bytes()).hexdigest()}
        self.save_manifest()
        result = self.reader.load('ai10', 'example')
        self.assertEqual(result['value'], 3)
        self.assertTrue(np.isnan(result['evals'][0][2]))
        np.testing.assert_array_equal(result['curve'], [[0, 7.25], [100, 3.25]])
        self.assertEqual(result['curve'].dtype, np.float32)

    def test_checksum_change_is_rejected_even_with_restored_mtime(self):
        self.cache()
        path = self.root / '.cache/ai10/example.json'
        before = path.stat()
        path.write_bytes(path.read_bytes().replace(b'3', b'4'))
        import os
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.reader.load('ai10', 'example')

    def test_missing_array_and_changed_manifest_fail_closed(self):
        entry = self.cache()
        self.reader.load('ai10', 'example')
        entry['npz'] = {'path': '.cache/ai10/example.npz', 'sha256': '0' * 64}
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'manifest changed'):
            self.reader.load('ai10', 'example')
        with self.assertRaises(FileNotFoundError):
            inputs.SceneInputs(self.root).load('ai10', 'example')

    def test_alternate_path_requires_explicit_qualification(self):
        entry = self.cache(path='.cache/example-variant/example.json')
        with self.assertRaisesRegex(ValueError, 'alternate path'):
            self.reader.load('ai10', 'example')
        entry['kind'] = 'qualified'
        for invalid in [None, '', '  ', []]:
            entry['qualification'] = invalid
            self.save_manifest()
            with self.assertRaisesRegex(ValueError, 'qualification'):
                inputs.SceneInputs(self.root).load('ai10', 'example')
        entry['qualification'] = 'Synthetic alternate fixture; not a scientific outcome.'
        self.save_manifest()
        self.assertEqual(inputs.SceneInputs(self.root).load('ai10', 'example')['value'], 3)

    def array_fixture(self, raw):
        entry = self.cache()
        entry['npz'] = self.file('.cache/ai10/example.npz', raw)
        self.save_manifest()

    def test_array_header_cannot_request_unbounded_allocation(self):
        header = io.BytesIO()
        np.lib.format.write_array_header_1_0(header, {
            'descr': '<f8', 'fortran_order': False, 'shape': (1 << 40,)})
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('huge.npy', header.getvalue())
        self.array_fixture(archive.getvalue())
        with self.assertRaisesRegex(ValueError, 'shape exceeds'):
            self.reader.load('ai10', 'example')

    def test_decompressed_array_size_and_object_dtype_are_rejected(self):
        archive = io.BytesIO()
        np.savez_compressed(archive, values=np.zeros(128))
        self.array_fixture(archive.getvalue())
        with mock.patch.object(inputs, 'MAX_ARRAY_BYTES', 512):
            with self.assertRaisesRegex(ValueError, 'decompressed size'):
                self.reader.load('ai10', 'example')
        archive = io.BytesIO()
        np.savez_compressed(archive, values=np.array([{'not': 'a numeric array'}], dtype=object))
        self.array_fixture(archive.getvalue())
        with self.assertRaisesRegex(ValueError, 'numeric or text'):
            inputs.SceneInputs(self.root).load('ai10', 'example')

    def test_text_uses_verified_bytes_and_universal_newlines(self):
        self.manifest['inputs']['ai1/passage'] = {
            'kind': 'canonical', 'text': self.file('.cache/ai1/passage.txt', 'one\r\ntwo\rthree'.encode())}
        self.save_manifest()
        self.assertEqual(self.reader.text('ai1', 'passage'), 'one\ntwo\nthree')

    def test_escape_and_symlinks_are_rejected(self):
        entry = self.cache()
        entry.update(kind='qualified', qualification='Synthetic unsafe-path fixture')
        for unsafe in ['../escape.json', '.cache/../escape.json', str(self.root / 'escape.json')]:
            entry['json']['path'] = unsafe
            self.save_manifest()
            with self.assertRaises(ValueError):
                inputs.SceneInputs(self.root).load('ai10', 'example')
        target = self.root / '.cache/ai10/example.json'
        target.rename(target.with_suffix('.original'))
        target.symlink_to(target.with_suffix('.original'))
        entry['json']['path'] = '.cache/ai10/example.json'
        self.save_manifest()
        with self.assertRaises(ValueError):
            inputs.SceneInputs(self.root).load('ai10', 'example')

    def test_parent_swap_during_open_is_rejected(self):
        self.cache()
        import os
        real_open = os.open
        swapped = False
        def swap(name, flags, *args, **kwargs):
            nonlocal swapped
            if name == 'example.json' and not swapped:
                swapped = True
                original = self.root / '.cache/ai10'
                retained = self.root / '.cache/retained'
                original.rename(retained)
                original.symlink_to(retained, target_is_directory=True)
            return real_open(name, flags, *args, **kwargs)
        with mock.patch.object(inputs.os, 'open', side_effect=swap):
            with self.assertRaisesRegex(ValueError, 'directory changed'):
                self.reader.load('ai10', 'example')
        self.assertTrue(swapped)

    def test_invalid_identity_and_kind_are_rejected(self):
        entry = self.cache()
        entry['json']['sha256'] = 'not-a-digest'
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            self.reader.load('ai10', 'example')
        entry['kind'] = 'automatic'
        self.save_manifest()
        with self.assertRaises(ValueError):
            inputs.SceneInputs(self.root).load('ai10', 'example')


class SourceExpressions(unittest.TestCase):
    def test_character_replay_never_exposes_a_future_checkpoint(self):
        node = function('s14_charlstm.py', 'upto')
        class Trace:
            def __init__(self, **kwargs): self.points = []
            def set_points_as_corners(self, points): self.points = points; return self
        context = {'np': np, 'VMobject': Trace, 'LM_C': 'example',
                   'ev': np.array([[0, 7.25], [100, 3.25], [200, 2.5]]),
                   'A': types.SimpleNamespace(c2p=lambda x, y: np.array([x, y, 0]))}
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-replay-prefix', 'exec'), context)
        for clock, expected in [(0, [0, 0]), (50, [0, 0]), (100, [0, 100]), (150, [0, 100])]:
            context['t'] = types.SimpleNamespace(get_value=lambda: clock)
            self.assertEqual([p[0] for p in context['upto']().points], expected)
        replay = function('s14_charlstm.py', 'replay')
        top = next(n.value for n in replay.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'top' for t in n.targets))
        self.assertEqual(eval(compile(ast.Expression(top), 'actual-axis-range', 'eval'), context), 8)

    def test_small_beam_gain_retains_percentage_point_precision(self):
        node = function('s15_seq2seq.py', 'bottleneck')
        gain = next(n.value for n in node.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'bv' for t in n.targets))
        text = eval(compile(ast.Expression(gain), 'actual-beam-wording', 'eval'), {'gains': [0, 1 / 40, 0]})
        self.assertIn('2.5 percentage points', text)
        self.assertIn('seed-zero', text)

    def test_narration_keys_and_bookmarks_remain_consistent(self):
        lines = json.loads((PART / 'narration_zh.json').read_text())['lines']
        self.assertEqual(len(lines), 105)
        pattern = re.compile(r"<bookmark\s+mark=['\"]([^'\"]+)['\"]\s*/>")
        for key, row in lines.items():
            with self.subTest(key=key):
                self.assertEqual(hashlib.sha1(' '.join(row['en'].split()).encode()).hexdigest()[:12], key)
                self.assertEqual(pattern.findall(row['en']), pattern.findall(row['zh']))
                self.assertTrue(row['zh'].strip())

    def test_scene_input_entry_points_do_not_import_producers(self):
        for filename in ['common.py', 's14_charlstm.py', 'inputs.py']:
            tree = ast.parse((PART / filename).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    self.assertNotIn('compute', node.module or '')
                    self.assertTrue(all('compute' not in item.name for item in node.names))
                elif isinstance(node, ast.Import):
                    self.assertTrue(all('compute' not in item.name for item in node.names))


if __name__ == '__main__':
    unittest.main()
