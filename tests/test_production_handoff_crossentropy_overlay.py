"""Exact ten-source gate, without scene/model/provider/producer imports."""
import ast
import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_production_handoff_entropy_prefix_overlay as previous

preflight=previous.preflight
ROOT=previous.ROOT
D=previous.D
sha=lambda b:hashlib.sha256(b).hexdigest()


class CrossEntropyOverlayTests(unittest.TestCase):
    setUp=previous.EntropyPrefixOverlayTests.setUp
    cmd=previous.EntropyPrefixOverlayTests.cmd
    commit=previous.EntropyPrefixOverlayTests.commit
    write=previous.EntropyPrefixOverlayTests.write
    json=previous.EntropyPrefixOverlayTests.json
    row=previous.EntropyPrefixOverlayTests.row
    assertRejected=previous.EntropyPrefixOverlayTests.assertRejected
    repin_fixture_manifest=previous.EntropyPrefixOverlayTests.repin_fixture_manifest
    install_combined_fixture=previous.EntropyPrefixOverlayTests.install_combined_fixture
    repin_combined_fixture=previous.EntropyPrefixOverlayTests.repin_combined_fixture
    install_roadmap_fixture=previous.EntropyPrefixOverlayTests.install_roadmap_fixture
    repin_roadmap_fixture=previous.EntropyPrefixOverlayTests.repin_roadmap_fixture
    install_polish_fixture=previous.EntropyPrefixOverlayTests.install_polish_fixture
    install_probability_fixture=previous.EntropyPrefixOverlayTests.install_probability_fixture
    repin_probability_fixture=previous.EntropyPrefixOverlayTests.repin_probability_fixture
    install_surprise_fixture=previous.EntropyPrefixOverlayTests.install_surprise_fixture
    repin_surprise_fixture=previous.EntropyPrefixOverlayTests.repin_surprise_fixture
    install_dwell_fixture=previous.EntropyPrefixOverlayTests.install_dwell_fixture
    repin_dwell_fixture=previous.EntropyPrefixOverlayTests.repin_dwell_fixture
    install_v8=previous.EntropyPrefixOverlayTests.install_v8
    repin_v8=previous.EntropyPrefixOverlayTests.repin_v8

    def install_v9(self):
        self.install_v8()
        for row in self.v8['source_replacements']:
            path=row['before']['path'];self.write(path,self.cmd('show',self.base+':'+path).encode())
        self.ce_before=b'original CrossEntropy fixture\n'
        self.ce_after=b'reviewed CrossEntropy relative timing fixture\n'
        self.arithmetic_before=b'original Arithmetic fixture\n';self.arithmetic_after=b'reviewed Arithmetic relative timing fixture\n'
        self.zh_before=b'original Chinese narration fixture\n';self.zh_after=b'reviewed decoder bookmark-only Chinese fixture\n'
        for path,raw in [(preflight.CROSS_ENTROPY,self.ce_before),(preflight.ARITHMETIC,self.arithmetic_before),(preflight.AI1_ZH,self.zh_before)]:self.write(path,raw)
        self.cmd('add',preflight.CROSS_ENTROPY,preflight.ARITHMETIC,preflight.AI1_ZH);self.commit('base with original three added source paths')
        self.base=self.cmd('rev-parse','HEAD').strip()
        p=patch.object(preflight,'BASE',self.base);p.start();self.addCleanup(p.stop)
        source=json.loads((self.meta/'reviewed-source-inventory.json').read_text())
        source['commit']=self.base;source['files'].extend([self.row(preflight.CROSS_ENTROPY,self.ce_before),self.row(preflight.ARITHMETIC,self.arithmetic_before),self.row(preflight.AI1_ZH,self.zh_before)])
        self.json('reviewed-source-inventory.json',source)
        for attr,repin in [('overlay',self.repin_fixture_manifest),('combined',self.repin_combined_fixture),
                            ('roadmap',self.repin_roadmap_fixture),('probability',self.repin_probability_fixture),
                            ('surprise',self.repin_surprise_fixture),('dwell',self.repin_dwell_fixture),('v8',self.repin_v8)]:
            getattr(self,attr)['base_commit']=self.base;repin()
        self.v9=copy.deepcopy(self.v8);self.v9['overlay_id']=preflight.CROSS_ENTROPY_OVERLAY
        self.decoder_prefix_after=b'reviewed Prefix decoder cue visibility fixture\n'
        self.v9['source_replacements'][4]['after']=self.row(preflight.PREFIX,self.decoder_prefix_after)
        self.v9['source_replacements'].insert(5,{'before':self.row(preflight.CROSS_ENTROPY,self.ce_before),'after':self.row(preflight.CROSS_ENTROPY,self.ce_after)})
        self.v9['source_replacements'][6:6]=[{'before':self.row(preflight.ARITHMETIC,self.arithmetic_before),'after':self.row(preflight.ARITHMETIC,self.arithmetic_after)},{'before':self.row(preflight.AI1_ZH,self.zh_before),'after':self.row(preflight.AI1_ZH,self.zh_after)}]
        self.v9['production_acceptance']={'crossentropy_repaired_output_observed':False,'crossentropy_repaired_output_accepted':False}
        self.repin_v9()
        for row in self.v9['source_replacements']:
            path=row['after']['path']
            if path==preflight.CROSS_ENTROPY:raw=self.ce_after
            else:
                matches={preflight.HOOK:self.hook_after,preflight.PROBABILITY:self.dwell_after,preflight.SURPRISE:self.surprise_after,
                         preflight.ENTROPY:self.entropy_after,preflight.PREFIX:self.decoder_prefix_after,preflight.ARITHMETIC:self.arithmetic_after,preflight.AI1_ZH:self.zh_after,preflight.SVD:self.combined_svd_after,preflight.OUTRO:self.outro_after}
                raw=matches[path]
            self.write(path,raw)
        return preflight.CROSS_ENTROPY_OVERLAY

    def repin_v9(self):
        rel='overlays/'+preflight.CROSS_ENTROPY_OVERLAY+'.json';self.json(rel,self.v9)
        self.known[preflight.CROSS_ENTROPY_OVERLAY]=(rel,sha((self.meta/rel).read_bytes()))

    def test_exact_ten_sources_with_all_strict_inputs(self):
        name=self.install_v9();r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        self.assertEqual(r['errors'],[]);self.assertEqual(r['checked_files'],17)

    def test_exact_ten_source_only_commit_is_accepted(self):
        name=self.install_v9();self.cmd('add',*[r['after']['path']for r in self.v9['source_replacements']]);self.commit('exact ten sources')
        self.assertEqual(preflight.verify(self.repo,overlay_id=name)['errors'],[])

    def test_default_and_every_prior_mode_reject_crossentropy(self):
        self.install_v9();v2=self.install_polish_fixture()
        for mode in [None,'svd-reveal-v1',v2,preflight.COMBINED,preflight.ROADMAP,preflight.PROBABILITY_OVERLAY,
                     preflight.SURPRISE_OVERLAY,preflight.NUMERIC_DWELL_OVERLAY,preflight.ENTROPY_PREFIX_OVERLAY]:
            with self.subTest(mode=mode):self.assertRejected(preflight.verify(self.repo,overlay_id=mode),preflight.CROSS_ENTROPY)

    def test_v8_still_accepts_exact_seven_after_all_new_changes_reverted(self):
        self.install_v9();self.write(preflight.CROSS_ENTROPY,self.ce_before);self.write(preflight.PREFIX,self.prefix_after);self.write(preflight.ARITHMETIC,self.arithmetic_before);self.write(preflight.AI1_ZH,self.zh_before)
        self.assertEqual(preflight.verify(self.repo,overlay_id=preflight.ENTROPY_PREFIX_OVERLAY)['errors'],[])
        self.assertRejected(preflight.verify(self.repo,overlay_id=preflight.CROSS_ENTROPY_OVERLAY),'Part1 CrossEntropy')

    def test_v8_rejects_new_prefix_even_with_crossentropy_original(self):
        self.install_v9();self.write(preflight.CROSS_ENTROPY,self.ce_before)
        self.assertRejected(preflight.verify(self.repo,overlay_id=preflight.ENTROPY_PREFIX_OVERLAY),preflight.PREFIX)

    def test_prior_v8_and_v7_reject_new_zh_even_without_ce_arithmetic_changes(self):
        self.install_v9();self.write(preflight.CROSS_ENTROPY,self.ce_before);self.write(preflight.ARITHMETIC,self.arithmetic_before);self.write(preflight.PREFIX,self.prefix_after)
        for mode in (preflight.ENTROPY_PREFIX_OVERLAY,preflight.NUMERIC_DWELL_OVERLAY):
            self.assertRejected(preflight.verify(self.repo,overlay_id=mode),preflight.AI1_ZH)

    def test_each_replacement_remains_exactly_required(self):
        name=self.install_v9()
        for row in self.v9['source_replacements']:
            path=row['after']['path'];good=(self.repo/path).read_bytes();self.write(path,self.cmd('show',self.base+':'+path).encode())
            with self.subTest(path=path):self.assertRejected(preflight.verify(self.repo,overlay_id=name),path)
            self.write(path,good)

    def test_bad_added_sources_return_structured_errors_without_exception(self):
        name=self.install_v9()
        for path,label in [(preflight.CROSS_ENTROPY,'Part1 CrossEntropy'),(preflight.ARITHMETIC,'Part1 Arithmetic'),(preflight.AI1_ZH,'Part1 Chinese narration')]:
            good=(self.repo/path).read_bytes();self.write(path,good+b'# unreviewed\n')
            result=preflight.verify(self.repo,overlay_id=name)
            self.assertIsInstance(result['errors'],list);self.assertRejected(result,label);self.write(path,good)

    def test_extra_source_and_huffman_never_authorized_or_imported(self):
        name=self.install_v9();self.write('videos/ai/ai1/s06_huffman.py',b'raise RuntimeError("never execute")\n')
        self.write('videos/ai/ai7/unreviewed.py',b'raise RuntimeError("never execute")\n')
        result=preflight.verify(self.repo,overlay_id=name)
        for path in ('s06_huffman.py','ai7/unreviewed.py'):self.assertRejected(result,path)

    def test_manifest_exact_byte_pin_unknown_name_and_base_identity(self):
        name=self.install_v9();self.assertRejected(preflight.verify(self.repo,overlay_id='guessed-v9'),'Unknown reviewed overlay')
        self.v9['production_acceptance']['crossentropy_repaired_output_accepted']=True;self.json('overlays/'+name+'.json',self.v9)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'manifest hash mismatch')
        self.v9['base_commit']='0'*40;self.repin_v9();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'identity/base mismatch')

    def test_schema_path_order_and_extra_evidence_remain_strict(self):
        name=self.install_v9();original=copy.deepcopy(self.v9)
        for version in (1,True,'2',3):
            self.v9=copy.deepcopy(original);self.v9['schema_version']=version;self.repin_v9()
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),'schema_version must be exactly 2')
        self.v9=copy.deepcopy(original);self.v9['source_replacements'].reverse();self.repin_v9()
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.v9=copy.deepcopy(original);self.v9['optional_evidence_files']=[self.row(self.evidence_path,self.evidence_bytes)];self.repin_v9()
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')

    def test_unrelated_head_and_index_are_not_authorized(self):
        name=self.install_v9();self.write('README.md',b'unrelatedHEAD\n');self.cmd('add','.');self.commit('unrelatedHEAD')
        self.write('explainer/unchanged.py',b'unrelatedINDEX\n');self.cmd('add','explainer/unchanged.py')
        r=preflight.verify(self.repo,overlay_id=name)
        self.assertRejected(r,'Overlay HEAD contains unrelated');self.assertRejected(r,'Overlay index contains unrelated')

    def test_data_runtime_audio_and_model_guards_are_not_relaxed(self):
        name=self.install_v9();self.cache.unlink();self.audio.write_bytes(b'wrongaudio');(self.snapshot/'model.safetensors').unlink()
        with patch.object(preflight.importlib.metadata,'version',return_value='wrong'):
            r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        for text in ('.cache/result.json','.cache/real.wav','model.safetensors','Package torch:'):self.assertRejected(r,text)

    def test_ce_source_symlink_still_rejected(self):
        name=self.install_v9();p=self.repo/preflight.CROSS_ENTROPY;outside=self.root/'ce-target.py';outside.write_bytes(p.read_bytes());p.unlink();p.symlink_to(outside)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'type mismatch')


class CrossEntropyReviewedManifestTests(unittest.TestCase):
    def test_real_v9_exact_ten_and_controlled_preflight_only(self):
        stale_errors=[];self.assertIsNone(preflight.load_overlay('part1-crossentropy-timing-and-part3-v9',stale_errors))
        self.assertTrue(any('Unknown reviewed overlay' in x for x in stale_errors))
        errors=[];v9=preflight.load_overlay(preflight.CROSS_ENTROPY_OVERLAY,errors)
        self.assertEqual(errors,[])
        old=preflight.load_overlay(preflight.ENTROPY_PREFIX_OVERLAY,errors);self.assertEqual(errors,[])
        rows=preflight.source_replacements(v9)
        self.assertEqual([r['after']['path']for r in rows],[preflight.HOOK,preflight.PROBABILITY,preflight.SURPRISE,
                         preflight.ENTROPY,preflight.PREFIX,preflight.CROSS_ENTROPY,preflight.ARITHMETIC,preflight.AI1_ZH,preflight.SVD,preflight.OUTRO])
        self.assertEqual([r for r in rows if r['after']['path']not in (preflight.CROSS_ENTROPY,preflight.PREFIX,preflight.ARITHMETIC,preflight.AI1_ZH)],
                         [r for r in old['source_replacements']if r['after']['path']!=preflight.PREFIX])
        self.assertEqual(rows[4]['before'],old['source_replacements'][4]['before'])
        self.assertNotEqual(rows[4]['after'],old['source_replacements'][4]['after'])
        self.assertEqual(old['source_replacements'][4]['after']['sha256'],'4592ba3674a83dca35bf52455367b32dc1ee8a53df93e27e5676f50387a7e7e8')
        self.assertEqual(rows[4]['after']['sha256'],'3a9c939d8c0b0ac97bfec9b978f86bbac6049497ccffa92b6485787e4f3fd01e')
        self.assertEqual(rows[6]['after']['sha256'],'bb35007c0827e7a53660c89efc6e917f2f45a744434256628550f3799ee947c9')
        self.assertEqual(rows[7]['before']['sha256'],'ff37869346cc68dbdc4208feaeed46bb95281bfe053888ebf929e01f744e9411')
        self.assertEqual(rows[7]['after']['sha256'],'959bea5c8d43d569158908b7d37a4678c2db1ce29c3c978cfb8b9f373d4093b7')
        self.assertEqual(rows[5]['before']['sha256'],'149412abb320476bf16ba2abb7c632d4f40b707274b576eb12c77b9265f9948f')
        self.assertEqual(rows[5]['after']['sha256'],'5d4a5d584d68b8167d63b5949c4a0d214f1271b9f201e1382f3e6b64f566d15f')
        self.assertEqual(v9['base_commit'],'927fba668656a682b3e29a288de64130ddc680dd')
        self.assertEqual(v9['optional_evidence_files'],[])
        self.assertFalse(v9['production_acceptance']['crossentropy_repaired_output_observed'])
        self.assertFalse(v9['production_acceptance']['crossentropy_repaired_output_accepted'])
        self.assertEqual(v9['crossentropy_alignment_gate']['status'],'OPEN: production-host reconciliation required')
        self.assertEqual(v9['crossentropy_alignment_gate']['matched_requests'],21)
        self.assertEqual(v9['crossentropy_alignment_gate']['supplied_requests'],22)
        for row in v9['crossentropy_evidence_receipts']:
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_guard_bodies_exact_with_only_three_diagnostic_label_additions(self):
        def bodies(path):
            return {n.name:n for n in ast.parse(path.read_text()).body
                    if isinstance(n,ast.FunctionDef)and n.name not in {'load_overlay','main'}}
        old=bodies(D/'historical/crossentropy-v9-before/verify_handoff.py')
        new=bodies(D/'verify_handoff.py')
        fn=new['overlay_tree_checks'];labels=[n for n in ast.walk(fn)if isinstance(n,ast.Assign)
            and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='label']
        self.assertEqual(len(labels),1);value=labels[0].value
        self.assertIsInstance(value,ast.Subscript);self.assertIsInstance(value.value,ast.Dict)
        self.assertEqual(ast.dump(value.slice),ast.dump(ast.parse("after['path']",mode='eval').body))
        pairs=list(zip(value.value.keys,value.value.values));self.assertEqual(len(pairs),10)
        additions=[(k,v)for k,v in pairs if isinstance(k,ast.Name)and k.id in {'CROSS_ENTROPY','ARITHMETIC','AI1_ZH'}]
        self.assertEqual([(k.id,ast.literal_eval(v))for k,v in additions],[('CROSS_ENTROPY','Part1 CrossEntropy'),('ARITHMETIC','Part1 Arithmetic'),('AI1_ZH','Part1 Chinese narration')])
        keep=[(k,v)for k,v in pairs if not(isinstance(k,ast.Name)and k.id in {'CROSS_ENTROPY','ARITHMETIC','AI1_ZH'})]
        value.value.keys=[k for k,v in keep];value.value.values=[v for k,v in keep]
        self.assertEqual({k:ast.dump(v)for k,v in old.items()},{k:ast.dump(v)for k,v in new.items()})

    def test_every_prior_artifact_preserved_except_exact_documented_dispatch_and_comparator(self):
        rows=json.loads((D/'historical/crossentropy-v9-before/preserved-pins.json').read_text())['files']
        allowed={'docs/qa/evidence/production-handoff-parts1-3/verify_handoff.py',
                 'tests/test_production_handoff_probability_dwell_overlay.py','tests/test_production_handoff_entropy_prefix_overlay.py'}
        for row in rows:
            saved=(ROOT/row['historical_path']).read_bytes()
            if row.get('historical_compression')=='gzip':saved=gzip.decompress(saved)
            self.assertEqual((len(saved),sha(saved)),(row['bytes'],row['sha256']))
            if row['path']not in allowed:
                raw=(ROOT/row['path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))


if __name__=='__main__':unittest.main()
