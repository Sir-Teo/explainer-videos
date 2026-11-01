"""Portable five-source gate fixtures; no scene/producer/model imports."""
import ast
import json
import unittest
from unittest.mock import patch
import test_production_handoff_probability_overlay as previous

preflight=previous.preflight
ROOT=previous.ROOT
sha=previous.sha

class SurpriseOverlayTests(unittest.TestCase):
    setUp = previous.ProbabilityOverlayPreparationTests.setUp
    cmd = previous.ProbabilityOverlayPreparationTests.cmd
    commit = previous.ProbabilityOverlayPreparationTests.commit
    write = previous.ProbabilityOverlayPreparationTests.write
    json = previous.ProbabilityOverlayPreparationTests.json
    row = previous.ProbabilityOverlayPreparationTests.row
    verify = previous.ProbabilityOverlayPreparationTests.verify
    assertRejected = previous.ProbabilityOverlayPreparationTests.assertRejected
    repin_fixture_manifest = previous.ProbabilityOverlayPreparationTests.repin_fixture_manifest
    install_combined_fixture = previous.ProbabilityOverlayPreparationTests.install_combined_fixture
    repin_combined_fixture = previous.ProbabilityOverlayPreparationTests.repin_combined_fixture
    install_roadmap_fixture = previous.ProbabilityOverlayPreparationTests.install_roadmap_fixture
    repin_roadmap_fixture = previous.ProbabilityOverlayPreparationTests.repin_roadmap_fixture
    install_polish_fixture = previous.ProbabilityOverlayPreparationTests.install_polish_fixture
    install_probability_fixture = previous.ProbabilityOverlayPreparationTests.install_probability_fixture
    repin_probability_fixture = previous.ProbabilityOverlayPreparationTests.repin_probability_fixture

    def install_surprise_fixture(self):
        self.install_probability_fixture()
        for row in self.probability['source_replacements']:
            path=row['before']['path'];self.write(path,self.cmd('show',self.base+':'+path).encode())
        self.surprise_before=b'original Surprise timing fixture\n'
        self.surprise_after=b'reviewed five-source relative-cue fixture\n'
        self.write(preflight.SURPRISE,self.surprise_before);self.cmd('add',preflight.SURPRISE)
        self.commit('base with original Surprise');self.base=self.cmd('rev-parse','HEAD').strip()
        p=patch.object(preflight,'BASE',self.base);p.start();self.addCleanup(p.stop)
        source=json.loads((self.meta/'reviewed-source-inventory.json').read_text());source['commit']=self.base
        source['files'].append(self.row(preflight.SURPRISE,self.surprise_before));self.json('reviewed-source-inventory.json',source)
        self.overlay['base_commit']=self.base;self.repin_fixture_manifest()
        self.combined['base_commit']=self.base;self.repin_combined_fixture()
        self.roadmap['base_commit']=self.base;self.repin_roadmap_fixture()
        self.probability['base_commit']=self.base;self.repin_probability_fixture()
        self.surprise=json.loads(json.dumps(self.probability));self.surprise['overlay_id']=preflight.SURPRISE_OVERLAY
        self.surprise['source_replacements'].insert(2,{
            'before':self.row(preflight.SURPRISE,self.surprise_before),
            'after':self.row(preflight.SURPRISE,self.surprise_after)})
        self.surprise['production_acceptance']={'surprise_repaired_output_accepted':False}
        self.repin_surprise_fixture()
        for path,raw in [(preflight.HOOK,self.hook_after),(preflight.PROBABILITY,self.prob_after),
                         (preflight.SURPRISE,self.surprise_after),(preflight.SVD,self.combined_svd_after),
                         (preflight.OUTRO,self.outro_after)]:self.write(path,raw)
        return preflight.SURPRISE_OVERLAY

    def repin_surprise_fixture(self):
        rel='overlays/'+preflight.SURPRISE_OVERLAY+'.json';self.json(rel,self.surprise)
        self.known[preflight.SURPRISE_OVERLAY]=(rel,sha((self.meta/rel).read_bytes()))

    def test_exact_five_worktree_preserves_strict_dependencies(self):
        name=self.install_surprise_fixture()
        r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        self.assertEqual(r['errors'],[]);self.assertEqual(r['checked_files'],12)

    def test_exact_five_source_commit_accepted(self):
        name=self.install_surprise_fixture();self.cmd('add',*[r['after']['path'] for r in self.surprise['source_replacements']])
        self.commit('exact synthetic five-source tree');self.assertEqual(preflight.verify(self.repo,overlay_id=name)['errors'],[])

    def test_every_five_replacement_required(self):
        name=self.install_surprise_fixture()
        for row in self.surprise['source_replacements']:
            path=row['after']['path'];after=(self.repo/path).read_bytes()
            self.write(path,self.cmd('show',self.base+':'+path).encode())
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),path);self.write(path,after)

    def test_default_and_v1_to_v5_do_not_expand(self):
        self.install_surprise_fixture();v2=self.install_polish_fixture()
        for name in [None,'svd-reveal-v1',v2,preflight.COMBINED,preflight.ROADMAP,preflight.PROBABILITY_OVERLAY]:
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),preflight.SURPRISE)
        self.write(preflight.SURPRISE,self.surprise_before)
        self.assertEqual(preflight.verify(self.repo,overlay_id=preflight.PROBABILITY_OVERLAY)['errors'],[])

    def test_tamper_wrong_base_and_unknown_alias_fail(self):
        name=self.install_surprise_fixture()
        self.assertRejected(preflight.verify(self.repo,overlay_id='unreviewed-surprise-alias'),'Unknown reviewed overlay')
        self.surprise['production_acceptance']['surprise_repaired_output_accepted']=True
        self.json('overlays/'+name+'.json',self.surprise)
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'manifest hash mismatch')
        self.surprise['base_commit']='0'*40;self.repin_surprise_fixture()
        self.assertRejected(preflight.verify(self.repo,overlay_id=name),'identity/base mismatch')

    def test_no_sixth_source_reordered_path_or_extra_evidence(self):
        name=self.install_surprise_fixture();original=json.loads(json.dumps(self.surprise))
        self.surprise['source_replacements'][2]['after']['path']='videos/ai/ai1/unreviewed.py'
        self.repin_surprise_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.surprise=json.loads(json.dumps(original));self.surprise['source_replacements'].reverse()
        self.repin_surprise_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.surprise=json.loads(json.dumps(original));self.surprise['source_replacements'].append({
            'before':self.row('explainer/unchanged.py',b'value = 1\n'),
            'after':self.row('explainer/unchanged.py',b'value = 2\n')})
        self.repin_surprise_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')
        self.surprise=json.loads(json.dumps(original));self.surprise['optional_evidence_files']=[self.row(self.evidence_path,self.evidence_bytes)]
        self.repin_surprise_fixture();self.assertRejected(preflight.verify(self.repo,overlay_id=name),'unreviewed path')

    def test_strict_schema_types(self):
        name=self.install_surprise_fixture()
        for value in [1,True,'2',3]:
            self.surprise['schema_version']=value;self.repin_surprise_fixture()
            self.assertRejected(preflight.verify(self.repo,overlay_id=name),'schema_version must be exactly 2')

    def test_unrelated_head_index_and_untracked_producer_fail(self):
        name=self.install_surprise_fixture();self.write('README.md',b'unrelated tree\n');self.cmd('add','.')
        self.commit('forbidden later branch tree');self.write('explainer/unchanged.py',b'unreviewed\n');self.cmd('add','explainer/unchanged.py')
        self.write('explainer/new_producer.py',b'raise AssertionError("never import")\n');r=preflight.verify(self.repo,overlay_id=name)
        for text in ['Overlay HEAD contains unrelated','Overlay index contains unrelated','new_producer.py']:self.assertRejected(r,text)

    def test_cache_runtime_model_audio_checks_remain(self):
        name=self.install_surprise_fixture();self.cache.unlink();self.audio.write_bytes(b'wrong audio')
        (self.snapshot/'model.safetensors').unlink()
        with patch.object(preflight.importlib.metadata,'version',return_value='wrong'):
            r=preflight.verify(self.repo,overlay_id=name,strict_external=True,optional_audio=True)
        for text in ['.cache/result.json','.cache/real.wav','model.safetensors','Package torch:']:self.assertRejected(r,text)

class SurpriseReviewedManifestTests(unittest.TestCase):
    def test_real_v6_exact_five_sources_and_controlled_status(self):
        errors=[];m=preflight.load_overlay(preflight.SURPRISE_OVERLAY,errors);self.assertEqual(errors,[])
        rows=preflight.source_replacements(m)
        self.assertEqual([r['after']['path'] for r in rows],[preflight.HOOK,preflight.PROBABILITY,preflight.SURPRISE,preflight.SVD,preflight.OUTRO])
        self.assertEqual([r['after']['sha256'] for r in rows],[
            '7230ac4c55882c65ba880133512bbb328a4239f919a1f993544a52e7d272dcf8',
            '50ff2a79121a6429eaf30950094d2157e6118d3b390e4544185f27cc44ecf0ed',
            '64567666d4e3d0d7ebed23a78f034d4aa1883b78acb2fb5cd89e6298d0855d55',
            '2c01a4a7b7acd7d51d05b3c8943b82337cb850776b309d552ba2719f12ead63b',
            'e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24'])
        self.assertEqual(rows[2]['before']['sha256'],'5adfb85e1094e56f8d81484fc2b04af0e8efbc3c3aab88d4fe8bb3a6c0eea3e8')
        self.assertFalse(m['production_acceptance']['surprise_repaired_output_accepted'])
        self.assertFalse(m['production_acceptance']['surprise_repaired_output_observed'])
        self.assertEqual(m['optional_evidence_files'],[])
        for row in m['evidence_receipts']:
            raw=(ROOT/row['path']).read_bytes();self.assertEqual((len(raw),sha(raw)),(row['bytes'],row['sha256']))

    def test_published_v5_and_original_test_files_unchanged(self):
        self.assertEqual(sha((preflight.D/'overlays/part1-probability-roadmap-and-part3-v5.json').read_bytes()),
                         '6bc668f43c97b0d9867b2ab323c2d337599a5c4417c9fb5eb01644d7e9a7dbce')
        self.assertEqual(sha((ROOT/'tests/test_production_handoff_overlay.py').read_bytes()),
                         '3babfe70739a7146df1c4f84176ae80452722b770a4c22c0c83b8efdeecb2a69')
        self.assertEqual(sha((ROOT/'tests/test_production_handoff_probability_overlay.py').read_bytes()),
                         'dbb041ef929150098126b49f3df048fafec4a5edbc36f52c0543f388543f8a44')

    def test_external_and_audio_AST_unchanged(self):
        def bodies(path):
            f=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='verify')
            return {n.test.id:ast.dump(n,include_attributes=False) for n in f.body if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id in ['strict_external','optional_audio']}
        self.assertEqual(bodies(previous.old.HELPER),bodies(preflight.D/'historical/surprise-v6-before/verify_handoff.py'))

if __name__=='__main__':unittest.main()
