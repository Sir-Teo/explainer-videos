"""Synthetic four-source gate prep; no real candidate/model/data/producer imports."""
import ast
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import test_production_handoff_overlay as old

preflight = old.preflight
ROOT = old.ROOT
sha = old.sha


class ProbabilityOverlayPreparationTests(unittest.TestCase):
    # Reuse helper methods, not inherited test methods; original54 remain exact.
    setUp = old.OverlayPreflightTests.setUp
    cmd = old.OverlayPreflightTests.cmd
    commit = old.OverlayPreflightTests.commit
    write = old.OverlayPreflightTests.write
    json = old.OverlayPreflightTests.json
    row = old.OverlayPreflightTests.row
    verify = old.OverlayPreflightTests.verify
    assertRejected = old.OverlayPreflightTests.assertRejected
    repin_fixture_manifest = old.OverlayPreflightTests.repin_fixture_manifest
    install_combined_fixture = old.OverlayPreflightTests.install_combined_fixture
    repin_combined_fixture = old.OverlayPreflightTests.repin_combined_fixture
    install_roadmap_fixture = old.OverlayPreflightTests.install_roadmap_fixture
    repin_roadmap_fixture = old.OverlayPreflightTests.repin_roadmap_fixture
    install_polish_fixture = old.OverlayPreflightTests.install_polish_fixture

    def install_probability_fixture(self):
        self.install_roadmap_fixture()
        for path, before in [(preflight.SVD, self.before), (preflight.OUTRO, self.outro_before),
                             (preflight.HOOK, self.hook_before)]:
            self.write(path, before)
        self.prob_before = b'original probability fixture\n'
        self.prob_after = b'synthetic probability timing candidate fixture\n'
        self.write(preflight.PROBABILITY, self.prob_before)
        self.cmd('add', preflight.PROBABILITY); self.commit('base with original Probability')
        self.base = self.cmd('rev-parse', 'HEAD').strip()
        p = patch.object(preflight, 'BASE', self.base); p.start(); self.addCleanup(p.stop)
        source = json.loads((self.meta / 'reviewed-source-inventory.json').read_text())
        source['commit'] = self.base
        source['files'].append(self.row(preflight.PROBABILITY, self.prob_before))
        self.json('reviewed-source-inventory.json', source)
        self.overlay['base_commit'] = self.base; self.repin_fixture_manifest()
        self.combined['base_commit'] = self.base; self.repin_combined_fixture()
        self.roadmap['base_commit'] = self.base; self.repin_roadmap_fixture()
        self.probability = json.loads(json.dumps(self.roadmap))
        self.probability['overlay_id'] = preflight.PROBABILITY_OVERLAY
        self.probability['source_replacements'].insert(1, {
            'before': self.row(preflight.PROBABILITY, self.prob_before),
            'after': self.row(preflight.PROBABILITY, self.prob_after)})
        self.repin_probability_fixture()
        for path, after in [(preflight.HOOK,self.hook_after), (preflight.PROBABILITY,self.prob_after),
                            (preflight.SVD,self.combined_svd_after), (preflight.OUTRO,self.outro_after)]:
            self.write(path, after)
        return preflight.PROBABILITY_OVERLAY

    def repin_probability_fixture(self):
        rel = 'overlays/' + preflight.PROBABILITY_OVERLAY + '.json'
        self.json(rel, self.probability)
        self.known[preflight.PROBABILITY_OVERLAY] = (rel, sha((self.meta / rel).read_bytes()))

    def test_exact_four_sources_at_base_preserve_strict_dependencies(self):
        name = self.install_probability_fixture()
        r = preflight.verify(self.repo, overlay_id=name, strict_external=True, optional_audio=True)
        self.assertEqual(r['errors'], []); self.assertEqual(r['checked_files'], 11)

    def test_equivalent_four_source_commit_accepted(self):
        name = self.install_probability_fixture()
        self.cmd('add', preflight.HOOK, preflight.PROBABILITY, preflight.SVD, preflight.OUTRO)
        self.commit('exact synthetic four-source tree')
        self.assertEqual(preflight.verify(self.repo, overlay_id=name)['errors'], [])

    def test_every_replacement_required(self):
        name = self.install_probability_fixture()
        for row in self.probability['source_replacements']:
            with self.subTest(path=row['after']['path']):
                path=row['after']['path']; after=(self.repo/path).read_bytes()
                raw=self.cmd('show', self.base+':'+path).encode()
                self.write(path, raw)
                self.assertRejected(preflight.verify(self.repo, overlay_id=name), path)
                self.write(path, after)

    def test_default_and_v1_to_v4_do_not_expand(self):
        self.install_probability_fixture(); v2=self.install_polish_fixture()
        for name in [None,'svd-reveal-v1',v2,preflight.COMBINED,preflight.ROADMAP]:
            self.assertRejected(preflight.verify(self.repo, overlay_id=name), preflight.PROBABILITY)
        self.write(preflight.PROBABILITY,self.prob_before)
        self.assertEqual(preflight.verify(self.repo, overlay_id=preflight.ROADMAP)['errors'], [])

    def test_tamper_unknown_manifest_and_wrong_base_fail(self):
        name = self.install_probability_fixture()
        self.assertRejected(preflight.verify(self.repo,overlay_id='unreviewed-v5-alias'),'Unknown reviewed overlay')
        self.probability['scope']='tampered synthetic claim'
        self.json('overlays/'+name+'.json',self.probability)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'manifest hash mismatch')
        self.probability['base_commit']='0'*40;self.repin_probability_fixture()
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'identity/base mismatch')

    def test_no_fifth_source_swapped_path_or_extra_evidence(self):
        name=self.install_probability_fixture()
        original=json.loads(json.dumps(self.probability))
        self.probability['source_replacements'][1]['after']['path']='videos/ai/ai1/unreviewed.py'
        self.repin_probability_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.probability=json.loads(json.dumps(original));self.probability['source_replacements'].reverse()
        self.repin_probability_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.probability=json.loads(json.dumps(original));self.probability['source_replacements'].append({
            'before':self.row('explainer/unchanged.py',b'value = 1\n'),
            'after':self.row('explainer/unchanged.py',b'value = 2\n')})
        self.repin_probability_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.probability=json.loads(json.dumps(original));self.probability['optional_evidence_files']=[self.row(self.evidence_path,self.evidence_bytes)]
        self.repin_probability_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')

    def test_strict_schema_type(self):
        name=self.install_probability_fixture()
        for value in [1,True,'2',3]:
            self.probability['schema_version']=value;self.repin_probability_fixture()
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),'schema_version must be exactly 2')

    def test_unrelated_head_index_and_untracked_producer_fail(self):
        name=self.install_probability_fixture()
        self.write('README.md',b'unrelated branch\n');self.cmd('add','.');self.commit('forbidden later tree')
        self.write('explainer/unchanged.py',b'wrong source\n');self.cmd('add','explainer/unchanged.py')
        self.write('explainer/new_producer.py',b'raise AssertionError("never import")\n')
        r=preflight.verify(self.repo,overlay_id=name)
        for text in ['Overlay HEAD contains unrelated','Overlay index contains unrelated','new_producer.py']:
            self.assertRejected(r,text)

    def test_missing_or_tampered_data_runtime_model_audio_still_fail(self):
        name=self.install_probability_fixture();self.cache.unlink();self.audio.write_bytes(b'tampered')
        (self.snapshot/'model.safetensors').unlink()
        with patch.object(preflight.importlib.metadata,'version',return_value='wrong'):
            r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        for text in ['.cache/result.json','.cache/real.wav','Package torch:','model.safetensors']:
            self.assertRejected(r,text)


class ProbabilityReviewedManifestTests(unittest.TestCase):
    def test_reviewed_v5_binds_four_exact_sources_and_new_diagnostic(self):
        errors=[];overlay=preflight.load_overlay(preflight.PROBABILITY_OVERLAY,errors)
        self.assertEqual(errors,[])
        self.assertEqual(overlay['base_commit'],'927fba668656a682b3e29a288de64130ddc680dd')
        replacements=preflight.source_replacements(overlay)
        self.assertEqual([r['after']['path'] for r in replacements],
                         [preflight.HOOK,preflight.PROBABILITY,preflight.SVD,preflight.OUTRO])
        self.assertEqual([r['after']['sha256'] for r in replacements],[
            '7230ac4c55882c65ba880133512bbb328a4239f919a1f993544a52e7d272dcf8',
            '50ff2a79121a6429eaf30950094d2157e6118d3b390e4544185f27cc44ecf0ed',
            '2c01a4a7b7acd7d51d05b3c8943b82337cb850776b309d552ba2719f12ead63b',
            'e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24'])
        self.assertEqual(replacements[1]['before']['sha256'],
                         'f7da930ffe84df3d9588e7ad1f668d65296ee6c70f0a2ca9dd016db398f31620')
        self.assertEqual(overlay['new_probability_diagnostic']['sha256'],
                         '7f773060879f7b8c4b83262fd37bc207e462c6fda9a4c35389697aeb5f8eee5e')
        self.assertFalse(overlay['production_acceptance']['part1_probability_repaired_output_observed'])
        self.assertFalse(overlay['production_acceptance']['part1_probability_repaired_output_accepted'])
        self.assertEqual(overlay['optional_evidence_files'],[])
        for row in overlay['evidence_receipts']:
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_v4_manifest_and_original_tests_are_byte_exact(self):
        self.assertEqual(sha((preflight.D/'overlays/part1-roadmap-and-part3-v4.json').read_bytes()),
                         'f3480355639457d5da3bcc1ee70f0833cd2ca26a22c7fb4169250d9b50472bf3')
        self.assertEqual(sha((ROOT/'tests/test_production_handoff_overlay.py').read_bytes()),
                         '3babfe70739a7146df1c4f84176ae80452722b770a4c22c0c83b8efdeecb2a69')

    def test_external_and_audio_guard_bodies_unchanged(self):
        def bodies(path):
            f=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='verify')
            return {n.test.id:ast.dump(n,include_attributes=False) for n in f.body
                    if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id in ['strict_external','optional_audio']}
        self.assertEqual(bodies(old.HELPER),bodies(preflight.D/'historical/probability-v5-before/verify_handoff.py'))

if __name__=='__main__':unittest.main()
