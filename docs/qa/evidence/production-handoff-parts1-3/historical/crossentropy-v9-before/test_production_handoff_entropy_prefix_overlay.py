"""Seven-source controlled-rerender gate fixtures; no scene/producer/model imports."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_production_handoff_probability_dwell_overlay as previous

preflight=previous.preflight
ROOT=previous.ROOT
D=previous.D
sha=lambda b:hashlib.sha256(b).hexdigest()


class EntropyPrefixOverlayTests(unittest.TestCase):
    setUp=previous.NumericDwellOverlayPreparationTests.setUp
    cmd=previous.NumericDwellOverlayPreparationTests.cmd
    commit=previous.NumericDwellOverlayPreparationTests.commit
    write=previous.NumericDwellOverlayPreparationTests.write
    json=previous.NumericDwellOverlayPreparationTests.json
    row=previous.NumericDwellOverlayPreparationTests.row
    assertRejected=previous.NumericDwellOverlayPreparationTests.assertRejected
    repin_fixture_manifest=previous.NumericDwellOverlayPreparationTests.repin_fixture_manifest
    install_combined_fixture=previous.NumericDwellOverlayPreparationTests.install_combined_fixture
    repin_combined_fixture=previous.NumericDwellOverlayPreparationTests.repin_combined_fixture
    install_roadmap_fixture=previous.NumericDwellOverlayPreparationTests.install_roadmap_fixture
    repin_roadmap_fixture=previous.NumericDwellOverlayPreparationTests.repin_roadmap_fixture
    install_polish_fixture=previous.NumericDwellOverlayPreparationTests.install_polish_fixture
    install_probability_fixture=previous.NumericDwellOverlayPreparationTests.install_probability_fixture
    repin_probability_fixture=previous.NumericDwellOverlayPreparationTests.repin_probability_fixture
    install_surprise_fixture=previous.NumericDwellOverlayPreparationTests.install_surprise_fixture
    repin_surprise_fixture=previous.NumericDwellOverlayPreparationTests.repin_surprise_fixture
    install_dwell_fixture=previous.NumericDwellOverlayPreparationTests.install_dwell_fixture
    repin_dwell_fixture=previous.NumericDwellOverlayPreparationTests.repin_dwell_fixture

    def install_v8(self):
        self.install_dwell_fixture()
        for row in self.dwell['source_replacements']:
            path=row['before']['path'];self.write(path,self.cmd('show',self.base+':'+path).encode())
        self.entropy_before=b'original Entropy fixture\n';self.entropy_after=b'reviewed Entropy relative timing fixture\n'
        self.prefix_before=b'original Prefix fixture\n';self.prefix_after=b'reviewed Prefix relative timing fixture\n'
        for path,raw in [(preflight.ENTROPY,self.entropy_before),(preflight.PREFIX,self.prefix_before)]:self.write(path,raw)
        self.cmd('add',preflight.ENTROPY,preflight.PREFIX);self.commit('base with original Entropy and Prefix')
        self.base=self.cmd('rev-parse','HEAD').strip();p=patch.object(preflight,'BASE',self.base);p.start();self.addCleanup(p.stop)
        source=json.loads((self.meta/'reviewed-source-inventory.json').read_text());source['commit']=self.base
        source['files'] += [self.row(preflight.ENTROPY,self.entropy_before),self.row(preflight.PREFIX,self.prefix_before)]
        self.json('reviewed-source-inventory.json',source)
        for attr,repin in [('overlay',self.repin_fixture_manifest),('combined',self.repin_combined_fixture),
                            ('roadmap',self.repin_roadmap_fixture),('probability',self.repin_probability_fixture),
                            ('surprise',self.repin_surprise_fixture),('dwell',self.repin_dwell_fixture)]:
            getattr(self,attr)['base_commit']=self.base;repin()
        self.v8=copy.deepcopy(self.dwell);self.v8['overlay_id']=preflight.ENTROPY_PREFIX_OVERLAY
        self.v8['source_replacements'][3:3]=[
            {'before':self.row(preflight.ENTROPY,self.entropy_before),'after':self.row(preflight.ENTROPY,self.entropy_after)},
            {'before':self.row(preflight.PREFIX,self.prefix_before),'after':self.row(preflight.PREFIX,self.prefix_after)}]
        self.v8['production_acceptance']={'entropy_repaired_output_accepted':False,'prefix_repaired_output_accepted':False}
        self.repin_v8()
        after={preflight.HOOK:self.hook_after,preflight.PROBABILITY:self.dwell_after,
               preflight.SURPRISE:self.surprise_after,preflight.ENTROPY:self.entropy_after,
               preflight.PREFIX:self.prefix_after,preflight.SVD:self.combined_svd_after,preflight.OUTRO:self.outro_after}
        for path,raw in after.items():self.write(path,raw)
        return preflight.ENTROPY_PREFIX_OVERLAY

    def repin_v8(self):
        rel='overlays/'+preflight.ENTROPY_PREFIX_OVERLAY+'.json';self.json(rel,self.v8)
        self.known[preflight.ENTROPY_PREFIX_OVERLAY]=(rel,sha((self.meta/rel).read_bytes()))

    def test_exact_seven_sources_preserve_all_strict_checks(self):
        name=self.install_v8();result=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        self.assertEqual(result['errors'],[]);self.assertEqual(result['checked_files'],14)

    def test_source_only_seven_path_commit_is_accepted(self):
        name=self.install_v8();self.cmd('add',*[r['after']['path']for r in self.v8['source_replacements']]);self.commit('exact seven sources')
        self.assertEqual(preflight.verify(self.repo,overlay_id=name)['errors'],[])

    def test_all_prior_modes_and_default_reject_new_two_paths(self):
        self.install_v8();v2=self.install_polish_fixture()
        for mode in [None,'svd-reveal-v1',v2,preflight.COMBINED,preflight.ROADMAP,preflight.PROBABILITY_OVERLAY,
                     preflight.SURPRISE_OVERLAY,preflight.NUMERIC_DWELL_OVERLAY]:
            with self.subTest(mode=mode):
                result=preflight.verify(self.repo,overlay_id=mode)
                self.assertRejected(result,preflight.ENTROPY)

    def test_prior_v7_still_accepts_exact_five_after_new_two_reverted(self):
        self.install_v8();self.write(preflight.ENTROPY,self.entropy_before);self.write(preflight.PREFIX,self.prefix_before)
        self.assertEqual(preflight.verify(self.repo,overlay_id=preflight.NUMERIC_DWELL_OVERLAY)['errors'],[])
        self.assertRejected(preflight.verify(self.repo,overlay_id=preflight.ENTROPY_PREFIX_OVERLAY),preflight.ENTROPY)

    def test_every_replacement_is_exactly_required_with_structured_errors(self):
        name=self.install_v8()
        for row in self.v8['source_replacements']:
            path=row['after']['path'];good=(self.repo/path).read_bytes();self.write(path,self.cmd('show',self.base+':'+path).encode())
            with self.subTest(path=path):self.assertRejected(preflight.verify(self.repo,overlay_id=name),path)
            self.write(path,good)

    def test_bad_new_source_hashes_return_errors_not_keyerror(self):
        name=self.install_v8()
        for path,label in [(preflight.ENTROPY,'Part1 Entropy'),(preflight.PREFIX,'Part1 Prefix')]:
            original=(self.repo/path).read_bytes();self.write(path,original+b'# unreviewed\n')
            result=preflight.verify(self.repo,overlay_id=name);self.assertRejected(result,label);self.write(path,original)

    def test_huffman_and_untracked_producer_are_never_authorized_or_imported(self):
        name=self.install_v8();self.write('videos/ai/ai1/s06_huffman.py',b'raise RuntimeError("never import")\n')
        self.write('videos/ai/ai7/unreviewed.py',b'raise RuntimeError("never import")\n')
        result=preflight.verify(self.repo,overlay_id=name)
        for path in ['s06_huffman.py','ai7/unreviewed.py']:self.assertRejected(result,path)

    def test_manifest_hash_identity_and_unknown_overlay_fail(self):
        name=self.install_v8();self.assertRejected(preflight.verify(self.repo,overlay_id='guessed-v8'),'Unknown reviewed overlay')
        self.v8['production_acceptance']['entropy_repaired_output_accepted']=True;self.json('overlays/'+name+'.json',self.v8)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'manifest hash mismatch')
        self.v8['base_commit']='0'*40;self.repin_v8();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'identity/base mismatch')

    def test_schema_is_exact_integer_two(self):
        name=self.install_v8()
        for version in [1,True,'2',3]:
            self.v8['schema_version']=version;self.repin_v8()
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),'schema_version must be exactly 2')

    def test_source_path_order_and_no_optional_repository_extras(self):
        name=self.install_v8();original=copy.deepcopy(self.v8)
        self.v8['source_replacements'].reverse();self.repin_v8();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.v8=copy.deepcopy(original);self.v8['optional_evidence_files']=[self.row(self.evidence_path,self.evidence_bytes)]
        self.repin_v8();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')

    def test_unrelated_head_and_index_remain_rejected(self):
        name=self.install_v8();self.write('README.md',b'forbiddenHEAD\n');self.cmd('add','.');self.commit('forbidden later HEAD')
        self.write('explainer/unchanged.py',b'forbiddenindex\n');self.cmd('add','explainer/unchanged.py')
        result=preflight.verify(self.repo,overlay_id=name)
        self.assertRejected(result,'Overlay HEAD contains unrelated');self.assertRejected(result,'Overlay index contains unrelated')

    def test_data_runtime_model_and_audio_guards_are_unchanged(self):
        name=self.install_v8();self.cache.unlink();self.audio.write_bytes(b'wrongaudio');(self.snapshot/'model.safetensors').unlink()
        with patch.object(preflight.importlib.metadata,'version',return_value='wrong'):
            result=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        for text in ['.cache/result.json','.cache/real.wav','model.safetensors','Package torch:']:self.assertRejected(result,text)

    def test_source_symlinks_reject_for_both_new_paths(self):
        name=self.install_v8()
        for path in [preflight.ENTROPY,preflight.PREFIX]:
            p=self.repo/path;raw=p.read_bytes();target=self.root/(p.name+'.target');target.write_bytes(raw);p.unlink();p.symlink_to(target)
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),'type mismatch');p.unlink();p.write_bytes(raw)


class EntropyPrefixReviewedManifestTests(unittest.TestCase):
    def test_real_v8_exact_seven_and_source_only_clearance(self):
        errors=[];manifest=preflight.load_overlay(preflight.ENTROPY_PREFIX_OVERLAY,errors);self.assertEqual(errors,[])
        rows=preflight.source_replacements(manifest)
        self.assertEqual([r['after']['path']for r in rows],[preflight.HOOK,preflight.PROBABILITY,preflight.SURPRISE,
                        preflight.ENTROPY,preflight.PREFIX,preflight.SVD,preflight.OUTRO])
        self.assertEqual(manifest['base_commit'],'927fba668656a682b3e29a288de64130ddc680dd')
        self.assertEqual(manifest['optional_evidence_files'],[])
        self.assertEqual([r['after']['sha256']for r in rows],[
            '7230ac4c55882c65ba880133512bbb328a4239f919a1f993544a52e7d272dcf8',
            '5e856dd92a662a8a7f1bfc370e57e0c937722c5e2f9c35e99960e1cfd80724ea',
            '64567666d4e3d0d7ebed23a78f034d4aa1883b78acb2fb5cd89e6298d0855d55',
            '338c43429a0087d9cbba25e945bba2dfbad09fd40afeb2eef9f7ce68c62dcc49',
            '4592ba3674a83dca35bf52455367b32dc1ee8a53df93e27e5676f50387a7e7e8',
            '2c01a4a7b7acd7d51d05b3c8943b82337cb850776b309d552ba2719f12ead63b',
            'e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24'])
        self.assertFalse(manifest['production_acceptance']['entropy_repaired_output_observed'])
        self.assertFalse(manifest['production_acceptance']['entropy_repaired_output_accepted'])
        self.assertFalse(manifest['production_acceptance']['prefix_repaired_output_observed'])
        self.assertFalse(manifest['production_acceptance']['prefix_repaired_output_accepted'])
        for row in manifest['entropy_prefix_evidence_receipts']:
            raw=(ROOT/row['path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_prior_bytes_remain_exact_except_precisely_disclosed_v7_test_and_dispatch(self):
        history=D/'historical/entropy-prefix-v8-before';rows=json.loads((history/'preserved-pins.json').read_text())['files']
        allowed={'docs/qa/evidence/production-handoff-parts1-3/verify_handoff.py',
                 'docs/qa/evidence/production-handoff-parts1-3/README.md','docs/qa/production-handoff-parts1-3.md',
                 'tests/test_production_handoff_probability_dwell_overlay.py'}
        for row in rows:
            raw=(ROOT/row['historical_path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))
            if row['path'] not in allowed:
                raw=(ROOT/row['path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))
        self.assertEqual(preflight.NUMERIC_DWELL_OVERLAY,'part1-probability-numeric-dwell-surprise-roadmap-and-part3-v7')


if __name__=='__main__':unittest.main()
