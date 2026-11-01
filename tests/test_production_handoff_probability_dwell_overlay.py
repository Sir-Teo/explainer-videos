"""Strict numeric-dwell five-source gate; no scenes, producers or models imported."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
import test_production_handoff_surprise_overlay as previous

D=Path(__file__).resolve().parents[1]/'docs/qa/evidence/production-handoff-parts1-3'
ROOT=Path(__file__).resolve().parents[1]
preflight=previous.preflight
sha=lambda raw:hashlib.sha256(raw).hexdigest()

class NumericDwellOverlayPreparationTests(unittest.TestCase):
    setUp=previous.SurpriseOverlayTests.setUp
    cmd=previous.SurpriseOverlayTests.cmd
    commit=previous.SurpriseOverlayTests.commit
    write=previous.SurpriseOverlayTests.write
    json=previous.SurpriseOverlayTests.json
    row=previous.SurpriseOverlayTests.row
    verify=previous.SurpriseOverlayTests.verify
    assertRejected=previous.SurpriseOverlayTests.assertRejected
    repin_fixture_manifest=previous.SurpriseOverlayTests.repin_fixture_manifest
    install_combined_fixture=previous.SurpriseOverlayTests.install_combined_fixture
    repin_combined_fixture=previous.SurpriseOverlayTests.repin_combined_fixture
    install_roadmap_fixture=previous.SurpriseOverlayTests.install_roadmap_fixture
    repin_roadmap_fixture=previous.SurpriseOverlayTests.repin_roadmap_fixture
    install_polish_fixture=previous.SurpriseOverlayTests.install_polish_fixture
    install_probability_fixture=previous.SurpriseOverlayTests.install_probability_fixture
    repin_probability_fixture=previous.SurpriseOverlayTests.repin_probability_fixture
    install_surprise_fixture=previous.SurpriseOverlayTests.install_surprise_fixture
    repin_surprise_fixture=previous.SurpriseOverlayTests.repin_surprise_fixture

    def install_dwell_fixture(self):
        self.install_surprise_fixture()
        self.dwell_after=b'synthetic reviewed numeric result dwell source\n'
        self.dwell=json.loads(json.dumps(self.surprise));self.dwell['overlay_id']=preflight.NUMERIC_DWELL_OVERLAY
        self.dwell['source_replacements'][1]['after']=self.row(preflight.PROBABILITY,self.dwell_after)
        self.dwell['production_acceptance']={'probability_numeric_dwell_output_accepted':False}
        self.repin_dwell_fixture();self.write(preflight.PROBABILITY,self.dwell_after)
        return preflight.NUMERIC_DWELL_OVERLAY

    def repin_dwell_fixture(self):
        rel='overlays/'+preflight.NUMERIC_DWELL_OVERLAY+'.json';self.json(rel,self.dwell)
        self.known[preflight.NUMERIC_DWELL_OVERLAY]=(rel,sha((self.meta/rel).read_bytes()))

    def test_exact_five_sources_and_strict_inputs_accepted(self):
        name=self.install_dwell_fixture();r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        self.assertEqual(r['errors'],[]);self.assertEqual(r['checked_files'],12)

    def test_source_only_equivalent_commit_accepted(self):
        name=self.install_dwell_fixture();self.cmd('add',*[r['after']['path'] for r in self.dwell['source_replacements']]);self.commit('exact synthetic numeric dwell tree')
        self.assertEqual(preflight.verify(self.repo,overlay_id=name)['errors'],[])

    def test_default_and_every_old_mode_reject_new_probability(self):
        self.install_dwell_fixture();v2=self.install_polish_fixture()
        for name in [None,'svd-reveal-v1',v2,preflight.COMBINED,preflight.ROADMAP,preflight.PROBABILITY_OVERLAY,preflight.SURPRISE_OVERLAY]:
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),preflight.PROBABILITY)
        self.write(preflight.PROBABILITY,self.prob_after)
        self.assertEqual(preflight.verify(self.repo,overlay_id=preflight.SURPRISE_OVERLAY)['errors'],[])
        self.assertRejected(preflight.verify(self.repo,overlay_id=preflight.NUMERIC_DWELL_OVERLAY),preflight.PROBABILITY)

    def test_every_exact_source_replacement_remains_required(self):
        name=self.install_dwell_fixture()
        for row in self.dwell['source_replacements']:
            path=row['after']['path'];raw=(self.repo/path).read_bytes();self.write(path,self.cmd('show',self.base+':'+path).encode())
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),path);self.write(path,raw)

    def test_unknown_or_tampered_manifest_and_wrong_base_fail(self):
        name=self.install_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id='unreviewed-numeric-dwell'),'Unknown reviewed overlay')
        self.dwell['production_acceptance']['probability_numeric_dwell_output_accepted']=True;self.json('overlays/'+name+'.json',self.dwell)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'manifest hash mismatch')
        self.dwell['base_commit']='0'*40;self.repin_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'identity/base mismatch')

    def test_wrong_source_path_order_and_extra_repository_files_fail(self):
        name=self.install_dwell_fixture();original=json.loads(json.dumps(self.dwell))
        self.dwell['source_replacements'][1]['after']['path']='videos/ai/ai1/unreviewed.py';self.repin_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.dwell=json.loads(json.dumps(original));self.dwell['source_replacements'].reverse();self.repin_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.dwell=json.loads(json.dumps(original));self.dwell['optional_evidence_files']=[self.row(self.evidence_path,self.evidence_bytes)];self.repin_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')

    def test_strict_schema_types_do_not_broaden(self):
        name=self.install_dwell_fixture()
        for version in [1,True,'2',3]:
            self.dwell['schema_version']=version;self.repin_dwell_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'schema_version must be exactly 2')

    def test_unrelated_head_index_and_untracked_producer_rejected_without_execution(self):
        name=self.install_dwell_fixture();self.write('README.md',b'forbidden later-tree\n');self.cmd('add','.');self.commit('forbidden unrelated source')
        self.write('explainer/unchanged.py',b'forbidden index\n');self.cmd('add','explainer/unchanged.py');self.write('explainer/unreviewed_producer.py',b'raise RuntimeError("must never import")\n')
        r=preflight.verify(self.repo,overlay_id=name)
        for text in ['Overlay HEAD contains unrelated','Overlay index contains unrelated','unreviewed_producer.py']:self.assertRejected(r,text)

    def test_missing_tampered_data_runtime_model_audio_still_reject(self):
        name=self.install_dwell_fixture();self.cache.unlink();self.audio.write_bytes(b'wrong audio');(self.snapshot/'model.safetensors').unlink()
        with patch.object(preflight.importlib.metadata,'version',return_value='wrong'):
            r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        for text in ['.cache/result.json','.cache/real.wav','model.safetensors','Package torch:']:self.assertRejected(r,text)

    def test_existing_data_symlink_policy_can_reuse_readonly_frozen_bytes(self):
        name=self.install_dwell_fixture();source=self.root/'frozen-input.json';source.write_bytes(self.cache.read_bytes());before=(sha(source.read_bytes()),source.stat().st_mtime_ns,source.stat().st_ino)
        self.cache.unlink();self.cache.symlink_to(source)
        self.assertEqual(preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)['errors'],[])
        self.assertEqual((sha(source.read_bytes()),source.stat().st_mtime_ns,source.stat().st_ino),before)
        source.write_bytes(b'tampered reused input')
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'.cache/result.json')

    def test_source_symlinks_still_reject(self):
        name=self.install_dwell_fixture();source=self.root/'after.py';source.write_bytes(self.dwell_after)
        p=self.repo/preflight.PROBABILITY;p.unlink();p.symlink_to(source)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'type mismatch')

class NumericDwellReviewedManifestTests(unittest.TestCase):
    def test_real_v7_exact_five_sources_and_controlled_dwell_status(self):
        errors=[];m=preflight.load_overlay(preflight.NUMERIC_DWELL_OVERLAY,errors)
        self.assertEqual(errors,[])
        rows=preflight.source_replacements(m)
        self.assertEqual(m['base_commit'],'927fba668656a682b3e29a288de64130ddc680dd')
        self.assertEqual([r['after']['path'] for r in rows],
                         [preflight.HOOK,preflight.PROBABILITY,preflight.SURPRISE,preflight.SVD,preflight.OUTRO])
        self.assertEqual([r['after']['sha256'] for r in rows],[
            '7230ac4c55882c65ba880133512bbb328a4239f919a1f993544a52e7d272dcf8',
            '5e856dd92a662a8a7f1bfc370e57e0c937722c5e2f9c35e99960e1cfd80724ea',
            '64567666d4e3d0d7ebed23a78f034d4aa1883b78acb2fb5cd89e6298d0855d55',
            '2c01a4a7b7acd7d51d05b3c8943b82337cb850776b309d552ba2719f12ead63b',
            'e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24'])
        self.assertEqual(rows[1]['before']['sha256'],
                         'f7da930ffe84df3d9588e7ad1f668d65296ee6c70f0a2ca9dd016db398f31620')
        self.assertEqual(m['optional_evidence_files'],[])
        self.assertFalse(m['production_acceptance']['probability_numeric_dwell_output_observed'])
        self.assertFalse(m['production_acceptance']['probability_numeric_dwell_output_accepted'])
        self.assertEqual(m['numeric_dwell_source_review']['minimum_finished_numeric_hold_seconds'],1.5)
        for row in m['numeric_dwell_evidence_receipts']:
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_all_prior_overlays_tests_inventories_and_historical_helper_stay_exact(self):
        historical=D/'historical/probability-numeric-dwell-v7-before'
        rows=json.loads((historical/'preserved-pins.json').read_text())['files']
        replaceable={str((D/'verify_handoff.py').relative_to(ROOT)),
                     str((D/'README.md').relative_to(ROOT)),
                     'docs/qa/production-handoff-parts1-3.md'}
        for row in rows:
            if row['historical_path'] is not None:
                raw=(ROOT/row['historical_path']).read_bytes()
                self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))
            if row['path'] not in replaceable:
                raw=(ROOT/row['path']).read_bytes()
                self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_full_verify_and_other_guard_bodies_unchanged(self):
        old=D/'historical/probability-numeric-dwell-v7-before/verify_handoff.py'
        def bodies(path):
            nodes={n.name:n for n in ast.parse(path.read_text()).body
                   if isinstance(n,ast.FunctionDef) and n.name not in {'load_overlay','main'}}
            if path==D/'verify_handoff.py':
                # V8 adds diagnostic labels only. Require exactly these pairs
                # at the existing label lookup, then compare every guard AST.
                fn=nodes['overlay_tree_checks']
                labels=[n for n in ast.walk(fn) if isinstance(n,ast.Assign)
                        and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)
                        and n.targets[0].id=='label']
                self.assertEqual(len(labels),1)
                value=labels[0].value
                self.assertIsInstance(value,ast.Subscript)
                self.assertIsInstance(value.value,ast.Dict)
                self.assertEqual(ast.dump(value.slice,include_attributes=False),
                                 ast.dump(ast.parse("after['path']",mode='eval').body,include_attributes=False))
                mapping=value.value
                additions=[(k,v) for k,v in zip(mapping.keys,mapping.values)
                           if isinstance(k,ast.Name) and k.id in {'ENTROPY','PREFIX'}]
                self.assertEqual([(k.id,ast.dump(v,include_attributes=False)) for k,v in additions],
                                 [('ENTROPY',ast.dump(ast.Constant(value='Part1 Entropy'),include_attributes=False)),
                                  ('PREFIX',ast.dump(ast.Constant(value='Part1 Prefix'),include_attributes=False))])
                self.assertEqual(len(mapping.keys),7)
                keep=[(k,v) for k,v in zip(mapping.keys,mapping.values)
                      if not(isinstance(k,ast.Name) and k.id in {'ENTROPY','PREFIX'})]
                mapping.keys=[k for k,v in keep];mapping.values=[v for k,v in keep]
            return {name:ast.dump(n,include_attributes=False) for name,n in nodes.items()}
        self.assertEqual(bodies(old),bodies(D/'verify_handoff.py'))

if __name__=='__main__':unittest.main()
