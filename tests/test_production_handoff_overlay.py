"""Portable Git/file preflight fixtures; no scenes, loaders or models are imported."""
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'docs/qa/evidence/production-handoff-parts1-3/verify_handoff.py'
spec = importlib.util.spec_from_file_location('production_handoff_preflight', HELPER)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)
sha = lambda raw: hashlib.sha256(raw).hexdigest()


class OverlayPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.meta = self.root / 'handoff'
        self.meta.mkdir()
        self.model = self.root / 'hf'
        self.cmd('init', '--quiet')
        self.write('.gitignore', b'.cache/\n')
        self.before = b'original scene\n'
        self.after = b'reviewed scene\n'
        self.write(preflight.SVD, self.before)
        self.write('explainer/unchanged.py', b'value = 1\n')
        self.write('README.md', b'original documentation\n')
        self.cmd('add', '.')
        self.commit('base fixture')
        self.base = self.cmd('rev-parse', 'HEAD').strip()
        self.cache = self.write('.cache/result.json', b'{"measured": 4}\n')
        self.external_data = self.write('.cache/extra.npy', b'fixture external numerical bytes')
        self.audio = self.write('.cache/real.wav', b'fixture audio hash bytes, not audio')
        self.source_before = self.row(preflight.SVD, self.before)
        self.source_after = self.row(preflight.SVD, self.after)
        source = {'commit': self.base, 'files': [self.source_before, self.row('explainer/unchanged.py', b'value = 1\n')]}
        self.json('reviewed-source-inventory.json', source)
        self.json('cache-inventory.json', {'files': [self.row('.cache/result.json', self.cache.read_bytes())]})
        self.evidence_path = 'docs/qa/evidence/ai3-svd-reveal-motion-regression/review.json'
        self.evidence_bytes = b'{"reviewed":true}\n'
        self.overlay = {'schema_version': 1, 'overlay_id': 'svd-reveal-v1', 'base_commit': self.base,
                        'reviewed_patch_commit': '7c47c11e3802390141c9551ac376ebe4ddf31e0e',
                        'source_replacement': {'before': self.source_before, 'after': self.source_after},
                        'optional_evidence_files': [self.row(self.evidence_path, self.evidence_bytes)]}
        self.version_expectations = {'torch': '2.15.0+cpu', 'transformers': '5.22.1', 'numpy': '2.5.4'}
        self.revision = '607a30d783dfa663caf39e06633721c8d4cfcd7e'
        self.snapshot = self.model / 'models--openai-community--gpt2/snapshots' / self.revision
        self.snapshot.mkdir(parents=True)
        model_files = []
        for filename, raw in [('config.json', b'{"fixture":true}'), ('model.safetensors', b'fixture weights hash bytes, never loaded')]:
            p = self.snapshot / filename
            p.write_bytes(raw)
            model_files.append({'snapshot_relative_path': str(p.relative_to(self.model)), 'bytes': len(raw), 'sha256': sha(raw)})
        self.ref = self.model / 'models--openai-community--gpt2/refs/main'
        self.ref.parent.mkdir()
        self.ref.write_text(self.revision + '\n')
        self.json('external-validation-dependencies.json', {
            'extra_repo_relative_files': [self.row('.cache/extra.npy', self.external_data.read_bytes())],
            'source_inputs': [self.row('explainer/unchanged.py', b'value = 1\n')],
            'required_observed_packages': self.version_expectations,
            'gpt2': {'files': model_files, 'revision': self.revision}})
        self.json('real-information-audio.json', {'blocks': [{'files': [self.row('.cache/real.wav', self.audio.read_bytes())]}]})
        self.json('overlays/svd-reveal-v1.json', self.overlay)
        self.known = {'svd-reveal-v1': ('overlays/svd-reveal-v1.json', sha((self.meta / 'overlays/svd-reveal-v1.json').read_bytes()))}
        for obj, name, value in [(preflight, 'D', self.meta), (preflight, 'BASE', self.base),
                                 (preflight, 'KNOWN_OVERLAYS', self.known)]:
            p = patch.object(obj, name, value)
            p.start()
            self.addCleanup(p.stop)
        p = patch.dict(os.environ, {'HF_HUB_CACHE': str(self.model)})
        p.start()
        self.addCleanup(p.stop)
        p = patch.object(preflight.importlib.metadata, 'version', side_effect=lambda name: self.version_expectations[name])
        p.start()
        self.addCleanup(p.stop)
        self.write(preflight.SVD, self.after)

    def cmd(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, text=True, stderr=subprocess.PIPE)

    def commit(self, message):
        self.cmd('-c', 'user.name=Cloud QA fixture', '-c', 'user.email=qa@example.invalid', 'commit', '--quiet', '-m', message)

    def write(self, path, raw):
        p = self.repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
        return p

    def json(self, path, value):
        p = self.meta / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value, indent=2) + '\n')

    def row(self, path, raw):
        blob = subprocess.check_output(['git', 'hash-object', '--stdin'], cwd=self.repo, input=raw).decode().strip()
        return {'path': path, 'bytes': len(raw), 'sha256': sha(raw), 'git_mode': '100644', 'git_blob': blob}

    def verify(self, **kwargs):
        return preflight.verify(self.repo, overlay_id='svd-reveal-v1', **kwargs)

    def assertRejected(self, result, text):
        self.assertTrue(result['errors'])
        self.assertTrue(any(text in item for item in result['errors']), result['errors'])

    def repin_fixture_manifest(self):
        self.json('overlays/svd-reveal-v1.json', self.overlay)
        self.known['svd-reveal-v1'] = ('overlays/svd-reveal-v1.json', sha((self.meta / 'overlays/svd-reveal-v1.json').read_bytes()))

    def test_good_overlay_at_base_worktree_preserves_all_checks(self):
        result = self.verify(strict_external=True, optional_audio=True)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['checked_files'], 8)
        self.assertEqual(self.cmd('rev-parse', 'HEAD').strip(), self.base)
        self.assertEqual(self.cache.read_bytes(), b'{"measured": 4}\n')

    def test_equivalent_source_only_commit_is_accepted(self):
        self.cmd('add', preflight.SVD)
        self.commit('equivalent source patch')
        self.assertEqual(self.verify()['errors'], [])

    def test_exact_optional_reviewed_evidence_is_accepted(self):
        self.write(self.evidence_path, self.evidence_bytes)
        self.cmd('add', preflight.SVD, self.evidence_path)
        self.commit('source plus reviewed evidence')
        self.assertEqual(self.verify()['errors'], [])

    def test_default_still_rejects_changed_scene(self):
        result = preflight.verify(self.repo)
        self.assertRejected(result, preflight.SVD)

    def test_unknown_overlay_is_rejected(self):
        self.assertRejected(preflight.verify(self.repo, overlay_id='not-reviewed'), 'Unknown reviewed overlay')

    def test_tampered_manifest_is_rejected(self):
        self.overlay['scope'] = 'allow all sources'
        self.json('overlays/svd-reveal-v1.json', self.overlay)
        self.assertRejected(self.verify(), 'manifest hash mismatch')

    def test_wrong_base_is_rejected_even_in_repinned_fixture(self):
        self.overlay['base_commit'] = '0' * 40
        self.repin_fixture_manifest()
        self.assertRejected(self.verify(), 'identity/base mismatch')

    def test_wrong_source_path_is_rejected_even_in_repinned_fixture(self):
        self.overlay['source_replacement']['after']['path'] = '../escape.py'
        self.repin_fixture_manifest()
        self.assertRejected(self.verify(), 'unreviewed path')

    def test_wrong_after_hash_is_rejected(self):
        self.write(preflight.SVD, b'unreviewed scene\n')
        self.assertRejected(self.verify(), 'exact reviewed SVD after bytes')

    def test_wrong_before_inventory_identity_is_rejected(self):
        p = self.meta / 'reviewed-source-inventory.json'
        d = json.loads(p.read_text())
        d['files'][0]['sha256'] = '0' * 64
        self.json(p.name, d)
        self.assertRejected(self.verify(), 'before identity mismatch')

    def test_unrelated_source_head_change_is_rejected(self):
        self.write('explainer/unchanged.py', b'value = 2\n')
        self.cmd('add', '.')
        self.commit('unrelated source and SVD')
        self.assertRejected(self.verify(), 'Overlay HEAD contains unrelated')

    def test_unrelated_documentation_head_change_is_rejected(self):
        self.write('README.md', b'unrelated HEAD docs\n')
        self.cmd('add', '.')
        self.commit('wrong base tree')
        self.assertRejected(self.verify(), 'Overlay HEAD contains unrelated')

    def test_unrelated_worktree_and_untracked_source_are_rejected(self):
        self.write('README.md', b'worktree drift\n')
        self.write('explainer/new_module.py', b'new = 1\n')
        result = self.verify()
        self.assertRejected(result, 'README.md')
        self.assertRejected(result, 'explainer/new_module.py')

    def test_unrelated_staged_change_hidden_by_worktree_is_rejected(self):
        self.write('README.md', b'staged drift\n')
        self.cmd('add', 'README.md')
        self.write('README.md', b'original documentation\n')
        self.assertRejected(self.verify(), 'Overlay index contains unrelated')

    def test_tampered_optional_evidence_is_rejected(self):
        self.write(self.evidence_path, b'{"reviewed":false}\n')
        self.assertRejected(self.verify(), 'worktree file missing/size/hash/type mismatch')

    def test_scene_executable_mode_drift_is_rejected(self):
        (self.repo / preflight.SVD).chmod(0o755)
        self.assertRejected(self.verify(), 'exact reviewed SVD after bytes')

    def test_exact_scene_bytes_through_symlink_are_rejected(self):
        source = self.repo / preflight.SVD
        source.unlink()
        target = self.root / 'external-scene.py'
        target.write_bytes(self.after)
        source.symlink_to(target)
        self.assertRejected(self.verify(), 'exact reviewed SVD after bytes')

    def test_missing_or_tampered_core_data_remains_failure(self):
        self.cache.unlink()
        self.assertRejected(self.verify(), '.cache/result.json: missing/size/hash mismatch')
        self.cache.write_bytes(b'{"measured": 5}\n')
        self.assertRejected(self.verify(), '.cache/result.json: missing/size/hash mismatch')

    def test_exact_version_tags_remain_required(self):
        with patch.object(preflight.importlib.metadata, 'version', return_value='2.15.0'):
            self.assertRejected(self.verify(strict_external=True), 'Package torch: expected exact 2.15.0+cpu')

    def test_missing_package_remains_failure(self):
        with patch.object(preflight.importlib.metadata, 'version', side_effect=preflight.importlib.metadata.PackageNotFoundError):
            self.assertRejected(self.verify(strict_external=True), 'found None; STOP, do not weaken current()')

    def test_strict_external_data_and_model_hashes_remain_required(self):
        self.external_data.write_bytes(b'changed')
        (self.snapshot / 'model.safetensors').unlink()
        result = self.verify(strict_external=True)
        self.assertRejected(result, '.cache/extra.npy: missing/size/hash mismatch')
        self.assertRejected(result, 'model.safetensors: missing/size/hash mismatch')

    def test_tampered_same_size_model_payload_remains_failure(self):
        model = self.snapshot / 'model.safetensors'
        payload = model.read_bytes()
        model.write_bytes(b'X' + payload[1:])
        self.assertRejected(self.verify(strict_external=True), 'model.safetensors: missing/size/hash mismatch')

    def test_missing_overlay_manifest_is_rejected(self):
        (self.meta / 'overlays/svd-reveal-v1.json').unlink()
        self.assertRejected(self.verify(), 'manifest unavailable/invalid')

    def test_model_revision_and_ambiguous_resolution_remain_failure(self):
        self.ref.write_text('wrong-revision\n')
        self.assertRejected(self.verify(strict_external=True), 'different revision')
        self.ref.unlink()
        (self.snapshot.parent / 'another-revision').mkdir()
        self.assertRejected(self.verify(strict_external=True), 'missing or ambiguous')

    def test_optional_audio_still_checked(self):
        self.audio.write_bytes(b'changed')
        self.assertRejected(self.verify(optional_audio=True), '.cache/real.wav: missing/size/hash mismatch')

    def test_unknown_or_boolean_schema_version_is_rejected(self):
        for version in [2, True, '1']:
            self.overlay['schema_version'] = version
            self.repin_fixture_manifest()
            self.assertRejected(self.verify(), 'schema_version must be exactly 1')

    def test_clean_base_is_not_falsely_accepted_as_applied_overlay(self):
        self.write(preflight.SVD, self.before)
        self.assertRejected(self.verify(), 'exact reviewed SVD after bytes')

    def install_polish_fixture(self):
        name = 'svd-production-polish-v2'
        overlay = json.loads(json.dumps(self.overlay))
        overlay['overlay_id'] = name
        raw = b'reviewed production margin and name wrapping\n'
        overlay['source_replacement']['after'] = self.row(preflight.SVD, raw)
        overlay['optional_evidence_files'] = []
        relative = 'overlays/' + name + '.json'
        self.json(relative, overlay)
        self.known[name] = (relative, sha((self.meta / relative).read_bytes()))
        self.write(preflight.SVD, raw)
        return name

    def test_polish_requires_its_own_exact_overlay_selection(self):
        name = self.install_polish_fixture()
        self.assertEqual(preflight.verify(self.repo, overlay_id=name,
                                         strict_external=True, optional_audio=True)['errors'], [])
        self.assertRejected(self.verify(), 'exact reviewed SVD after bytes')
        self.assertRejected(preflight.verify(self.repo), preflight.SVD)

    def test_polish_selection_rejects_old_reveal_source(self):
        name = self.install_polish_fixture()
        self.write(preflight.SVD, self.after)
        self.assertRejected(preflight.verify(self.repo, overlay_id=name), 'exact reviewed SVD after bytes')

    def test_polish_keeps_unrelated_source_and_cache_checks(self):
        name = self.install_polish_fixture()
        self.write('explainer/unchanged.py', b'unreviewed shared change\n')
        self.cache.write_bytes(b'changed data\n')
        result = preflight.verify(self.repo, overlay_id=name)
        self.assertRejected(result, 'explainer/unchanged.py')
        self.assertRejected(result, '.cache/result.json')


class ReviewedManifestIdentityTests(unittest.TestCase):
    def test_polish_manifest_is_separate_and_binds_reviewed_scene(self):
        errors = []
        overlay = preflight.load_overlay('svd-production-polish-v2', errors)
        self.assertEqual(errors, [])
        self.assertEqual(overlay['base_commit'], '927fba668656a682b3e29a288de64130ddc680dd')
        self.assertEqual(overlay['reviewed_patch_commit'], 'd7a9b0acfb15ad9c371f14acae5d8acab2644d6f')
        self.assertEqual(overlay['source_replacement']['after']['sha256'],
                         '2c01a4a7b7acd7d51d05b3c8943b82337cb850776b309d552ba2719f12ead63b')
        self.assertEqual(overlay['optional_evidence_files'], [])

    def test_real_overlay_binds_exact_base_patch_and_scene(self):
        errors = []
        overlay = preflight.load_overlay('svd-reveal-v1', errors)
        self.assertEqual(errors, [])
        self.assertEqual(overlay['base_commit'], '927fba668656a682b3e29a288de64130ddc680dd')
        self.assertEqual(overlay['reviewed_patch_commit'], '7c47c11e3802390141c9551ac376ebe4ddf31e0e')
        self.assertEqual(overlay['source_replacement']['after']['sha256'], '291bba0e7c180750274e2117114cc22382f3b9b81880db0a499791b4b2e3e322')
        self.assertEqual(len(overlay['optional_evidence_files']), 103)


if __name__ == '__main__':
    unittest.main()
