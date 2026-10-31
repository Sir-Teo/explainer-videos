"""Temporary, deterministic cache fixtures; no production models or computation."""
from concurrent.futures import ThreadPoolExecutor
import copy
import json
from pathlib import Path
import tempfile
import threading
import sys
import unittest
from unittest.mock import Mock, patch

import numpy as np

from explainer.cache_lock import cache_lock
from tools import attest_ai3_cache, qa_series
from videos.ai.ai3 import cache_integrity as integrity
from videos.ai.ai3 import compute

SOURCE = Path(compute.__file__)
ROOT = SOURCE.parents[3]


def fixtures(name):
    if name == "einsum":
        return dict(shapes=[1000,20,1000,20],macs_left=40000000,macs_right=800000,
                    path=[[1,2],[0,1]],heads=12,n=1024,dh=64,macs_scores=12*1024**2*64,
                    macs_values=12*1024**2*64,macs_proj=4*1024*768**2),{}
    if name == "project":
        return dict(rows=[dict(n=n,kappa=1.,cgs=0.,mgs=0.,householder=0.,err_normal=0.,err_qr=0.) for n in range(2,15)],eps=np.finfo(float).eps),{}
    if name == "letters":
        return dict(total=np.sqrt(26),ca_share=.5,ca_left5=list('aeiou'),ca_vowels_left=1),dict(
            M=np.eye(26),S=np.ones(26),U=np.eye(26),Vt=np.eye(26),recon=np.zeros((26,26,26)),
            err=np.sqrt(np.arange(25,-1,-1)),ca_s=np.ones(5),ca_row=np.zeros(26),ca_col=np.zeros(26))
    if name == "power":
        return {key:dict(lam=[2.]+[1.]*7,ratio=.5,sin=[.5]*(steps+1),rq=[2.]*(steps+1),
                         pred_tan=[.5]*(steps+1),rq_err=[0.]*(steps+1),rate_measured=.5)
                for key,steps in (('gpt2',60),('letters',30))},{}
    if name == "image":
        ranks=[1,2,4,8,16,32,64];S=np.zeros(180);S[0]=1
        return dict(ranks=ranks,err=[0.]*7,tail=[0.]*7,total=1.,shape=[180,288],
                    storage=[k*469 for k in ranks],pixels=180*288,energy=[1.]*7),dict(
                    img=np.zeros((180,288),np.uint8),recon=np.zeros((7,180,288),np.uint8),S=S)
    if name == "depth":
        d=dict(n=256,layers=40,gains=[.8,1.,1.2]);a={}
        for g in d['gains']:d.update({f'sigma{g}':1.,f'rate{g}':1.});a[f'len{g}']=np.ones(41)
        return d,a
    if name == "galorectl":
        runs={}
        for lr,seed in ((.001,0),(.003,0),(.01,0),(.001,1),(.001,2)):
            runs[f'adamsplit_{lr:g}_{seed}']=dict(method='adamsplit',lr=lr,seed=seed,curve=[1.]*120,
                val=lr,dW={str(k):dict(stable=1.,eff=1.,rank=128) for k in range(10)},weights=5,opt_numbers=10)
        return dict(runs=runs,best_lr=.001),{}
    if name == "highdim":
        dims=[2,3,10,100,768];vd=[2,3,5,10,20,50,100,200,500,768,1000,2000,4096]
        d=dict(dims=dims,var_dims=vd,cos_var=[.1]*13,norm_sd=[.1]*13,shell={str(x):1-.99**x for x in dims},n_dirs=10000,worst_cos=.5,worst_angle=float(np.degrees(np.arccos(.5))))
        a={}
        for x in dims:d[f'angle_sd{x}']=1.;a[f'angles{x}']=np.full(36,0,dtype=int);a[f'angles{x}'][0]=20000;a[f'norms{x}']=np.full(40,0,dtype=int)
        return d,a
    raise AssertionError(name)


def write_fixture(cache,name):
    data,arrays=fixtures(name);cache.mkdir(parents=True,exist_ok=True)
    (cache/f'{name}.json').write_text(json.dumps(data))
    if arrays:np.savez_compressed(cache/f'{name}.npz',**arrays)
    return data,arrays


class CacheIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.cache=Path(self.tmp.name)/'ai3'
        self.real_dependencies = integrity.dependencies
        self.deps=patch.object(integrity,'dependencies',return_value={'fixture':'original'});self.deps.start();self.addCleanup(self.deps.stop)

    def publish(self,name='einsum'):
        write_fixture(self.cache,name)
        with cache_lock(self.cache/f'{name}.json'):
            return integrity.publish(name,self.cache,ROOT,SOURCE,origin='producer-save')

    def current(self,name='einsum'):
        return integrity.current(name,self.cache,ROOT,SOURCE)

    def test_all_eight_real_sized_contracts_accept_complete_fixtures(self):
        for name in sorted(integrity.ITEMS):
            with self.subTest(name=name):
                record=self.publish(name)
                self.assertEqual(record['origin'],'producer-save');self.assertTrue(self.current(name))

    def test_missing_legacy_sidecar_is_stale_and_never_auto_created(self):
        write_fixture(self.cache,'einsum')
        self.assertFalse(self.current());self.assertFalse(integrity.sidecar_path(self.cache,'einsum').exists())

    def test_json_byte_tamper_is_stale_even_with_unchanged_values(self):
        self.publish();p=self.cache/'einsum.json';p.write_text(p.read_text()+' ')
        self.assertFalse(self.current())

    def test_json_malformed_nondict_and_nonfinite_are_stale(self):
        self.publish();p=self.cache/'einsum.json'
        for value in ('{','[]','null','{"value":NaN}'):
            with self.subTest(value=value):p.write_text(value);self.assertFalse(self.current())

    def test_non_object_sidecars_are_stale_in_cached_only_qa(self):
        self.publish()
        side = integrity.sidecar_path(self.cache, 'einsum')
        payload = self.cache / 'einsum.json'
        before = payload.read_bytes(), payload.stat().st_mtime_ns
        cache = compute.SchemaCache('ai3')
        cache.dir = self.cache
        producer = Mock(side_effect=AssertionError('unexpected producer'))
        cache.items = {'einsum': producer}
        with patch.object(compute, 'CACHE', cache):
            for value in ([], None, ['nonempty'], 'invalid', 1, True):
                with self.subTest(value=value):
                    side.write_text(json.dumps(value))
                    with self.assertRaises(qa_series.StaleDataError):
                        qa_series.require_current_cache(compute, 'ai3', payload, 'einsum')
                    self.assertEqual(json.loads(side.read_text()), value)
        producer.assert_not_called()
        self.assertEqual(before, (payload.read_bytes(), payload.stat().st_mtime_ns))

    def test_non_object_legacy_evidence_is_stale(self):
        record = self.publish()
        side = integrity.sidecar_path(self.cache, 'einsum')
        record['origin'] = 'postproduction-attestation'
        for value in ([], None, ['nonempty'], 'invalid', 1, True):
            with self.subTest(value=value):
                record['evidence'] = value
                side.write_text(json.dumps(record))
                self.assertFalse(self.current())

    def test_npz_truncated_shape_changed_or_object_are_stale(self):
        for mode in ('truncated','shape','object','missing'):
            with self.subTest(mode=mode):
                self.publish('depth');p=self.cache/'depth.npz'
                if mode=='truncated':p.write_bytes(b'PK\x03\x04broken')
                elif mode=='missing':p.unlink()
                else:
                    _,a=fixtures('depth');a['len0.8']=np.ones(40) if mode=='shape' else np.array([object()]*41)
                    np.savez_compressed(p,**a)
                self.assertFalse(self.current('depth'))

    def test_structure_rejects_self_consistent_hash_of_wrong_curve_length(self):
        self.publish('galorectl');p=self.cache/'galorectl.json';v=json.loads(p.read_text());next(iter(v['runs'].values()))['curve']=[1.]*600;p.write_text(json.dumps(v))
        side=integrity.sidecar_path(self.cache,'galorectl');m=json.loads(side.read_text());m['artifacts']['json_sha256']=integrity.digest(p);side.write_text(json.dumps(m))
        self.assertFalse(self.current('galorectl'))

    def test_recipe_and_dependency_drift_fail_closed(self):
        self.publish()
        with patch.object(integrity,'recipe',return_value={'drift':1}):self.assertFalse(self.current())
        with patch.object(integrity,'dependencies',return_value={'fixture':'changed'}):self.assertFalse(self.current())

    def test_power_rejects_transitively_stale_letters_without_payload_changes(self):
        bigram = self.cache.parent / 'ai1' / 'bigram.json'
        bigram.parent.mkdir(parents=True)
        bigram.write_text('{"fixture":1}')
        model = Path(self.tmp.name) / 'model.safetensors'
        config = model.with_name('config.json')
        model.write_bytes(b'local test weights')
        config.write_text('{}')
        with patch.object(integrity, 'dependencies', side_effect=self.real_dependencies), \
                patch.object(integrity, '_gpt2_files', return_value={'config': config, 'weights': model}):
            self.publish('letters')
            self.publish('power')
            self.assertTrue(self.current('power'))
            before = {p: (p.read_bytes(), p.stat().st_mtime_ns)
                      for p in self.cache.glob('*') if p.is_file() and p.suffix in ('.json', '.npz')}
            # Only the upstream bigram changes; direct power dependencies are identical.
            bigram.write_text('{"fixture":2}')
            self.assertFalse(self.current('letters'))
            self.assertFalse(self.current('power'))
            self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before})

    def test_recipe_tracks_algorithm_and_constants_not_validator_only_edits(self):
        p=Path(self.tmp.name)/'compute.py';p.write_bytes(SOURCE.read_bytes())
        before={n:integrity.recipe(n,p) for n in integrity.ITEMS}
        p.write_text(p.read_text().replace('Semantic revisions and corpus lineage','Validator-only documentation'))
        self.assertEqual(before,{n:integrity.recipe(n,p) for n in integrity.ITEMS})
        p.write_text(p.read_text().replace('g = rng(17)','g = rng(18)'))
        self.assertNotEqual(before['einsum'],integrity.recipe('einsum',p))
        self.assertEqual(before['depth'],integrity.recipe('depth',p))

    def test_origin_and_expected_legacy_hash_are_required(self):
        write_fixture(self.cache,'einsum')
        with self.assertRaises(integrity.IntegrityError):integrity.publish('einsum',self.cache,ROOT,SOURCE,origin='postproduction-attestation')
        with self.assertRaises(integrity.IntegrityError):integrity.publish('einsum',self.cache,ROOT,SOURCE,origin='postproduction-attestation',evidence={'original_producer_sha256':integrity.ORIGINAL_PRODUCER,'expected_artifacts':{}})
        self.assertFalse(integrity.sidecar_path(self.cache,'einsum').exists())

    def test_future_save_origin_and_existing_nine_recipe_values_stable(self):
        cache=compute.SchemaCache('ai3');cache.dir=self.cache
        before={n:compute.digest_json(compute.item_recipe(n)) for n in compute.CACHE_SCHEMAS}
        data,_=fixtures('einsum');cache.save('einsum',data)
        # Hookup is activated only after migration; this test then exercises actual save.
        record=json.loads(integrity.sidecar_path(self.cache,'einsum').read_text())
        self.assertEqual(record['origin'],'producer-save');self.assertIsNone(record['evidence'])
        self.assertTrue(cache.current('einsum'))
        self.assertEqual(before,{n:compute.digest_json(compute.item_recipe(n)) for n in compute.CACHE_SCHEMAS})

    def test_normal_loader_and_cli_record_before_after_stability(self):
        for entry in ('load', 'cli'):
            with self.subTest(entry=entry):
                cache=compute.SchemaCache('ai3');cache.dir=Path(self.tmp.name)/entry
                data,_=fixtures('einsum');producer=Mock(return_value=data);cache.items={'einsum':producer}
                if entry=='load':cache.load('einsum')
                else:
                    with patch.object(sys,'argv',['compute','einsum']):cache.main(cache.items)
                producer.assert_called_once()
                record=json.loads(integrity.sidecar_path(cache.dir,'einsum').read_text())
                self.assertEqual(record['generation_observation']['status'],'complete-before-observation')
                self.assertEqual(record['generation_observation']['dependencies_before'],record['dependencies_observed_now'])

    def test_changed_dependencies_during_generation_cannot_publish_current_item(self):
        cache=compute.SchemaCache('ai3');cache.dir=self.cache
        data,_=fixtures('einsum');producer=Mock(return_value=data);cache.items={'einsum':producer}
        with patch.object(integrity,'dependencies',side_effect=[{'input':'before'},{'input':'after'}]):
            with self.assertRaisesRegex(integrity.IntegrityError,'changed during generation'):cache.load('einsum')
        producer.assert_called_once();self.assertFalse(cache.current('einsum'))
        self.assertFalse(integrity.sidecar_path(self.cache,'einsum').exists())

    def test_fresh_prerequisite_creation_discloses_incomplete_before_observation(self):
        cache=compute.SchemaCache('ai3');cache.dir=self.cache
        data,_=fixtures('einsum');cache.items={'einsum':lambda:data}
        with patch.object(integrity,'dependencies',side_effect=[integrity.IntegrityError('missing input'),{'created':'hash'}]):
            cache.load('einsum')
        record=json.loads(integrity.sidecar_path(self.cache,'einsum').read_text())
        self.assertEqual(record['generation_observation']['status'],'incomplete-before-observation')
        self.assertIsNone(record['generation_observation']['dependencies_before'])
        self.assertEqual(record['dependencies_observed_now'],{'created':'hash'})

    def test_invalid_future_save_removes_old_attestation_completion(self):
        self.publish();cache=compute.SchemaCache('ai3');cache.dir=self.cache
        data,_=fixtures('einsum');data['macs_left']=1
        with self.assertRaises(integrity.IntegrityError):cache.save('einsum',data)
        self.assertFalse(cache.current('einsum'))
        self.assertFalse(integrity.sidecar_path(self.cache,'einsum').exists())

    def test_actual_cached_only_guard_stops_all_eight_without_producer_calls(self):
        cache=compute.SchemaCache('ai3');cache.dir=self.cache;producer=Mock(side_effect=AssertionError('unexpected producer'))
        cache.items={n:producer for n in integrity.ITEMS}
        with patch.object(compute,'CACHE',cache):
            for name in integrity.ITEMS:
                write_fixture(self.cache,name)
                with self.subTest(name=name),self.assertRaises(qa_series.StaleDataError):
                    qa_series.require_current_cache(compute,'ai3',cache.path(name),name)
            producer.assert_not_called()

    def test_current_waits_for_same_item_lock_and_sees_complete_publication(self):
        self.publish();started=threading.Event();done=threading.Event()
        def inspect():started.set();result=self.current();done.set();return result
        with ThreadPoolExecutor(max_workers=1) as pool:
            with cache_lock(self.cache/'einsum.json'):
                future=pool.submit(inspect);self.assertTrue(started.wait(2));self.assertFalse(done.wait(.05))
            self.assertTrue(future.result(timeout=3))

    def test_failed_atomic_sidecar_replace_leaves_payload_and_no_temp(self):
        write_fixture(self.cache,'einsum');p=self.cache/'einsum.json';before=p.read_bytes(),p.stat().st_mtime_ns
        with patch.object(Path,'replace',side_effect=OSError('interrupted publication')):
            with self.assertRaises(OSError):integrity.publish('einsum',self.cache,ROOT,SOURCE,origin='producer-save')
        self.assertEqual(before,(p.read_bytes(),p.stat().st_mtime_ns));self.assertFalse(self.current())
        self.assertFalse(list((self.cache/'_integrity').glob('*.tmp.json')))

    def test_explicit_migration_checks_expected_hash_and_preserves_payload(self):
        root=Path(self.tmp.name)/'root';src=root/'videos/ai/ai3/compute.py';src.parent.mkdir(parents=True);src.write_bytes(SOURCE.read_bytes())
        write_fixture(self.cache,'einsum');pair=integrity.inspect_payload('einsum',self.cache)
        expected=Path(self.tmp.name)/'expected.json';completion=Path(self.tmp.name)/'completion.json';log=Path(self.tmp.name)/'run.log'
        original=integrity.digest(src)
        expected.write_text(json.dumps({'producer_sha256':original,'items':{'einsum':pair}}))
        completion.write_text(json.dumps({'producer_sha256':original,'cache_json_sha256':{'einsum':pair['json_sha256']}}))
        log.write_text('  compute einsum ...\n  done    einsum in 0s\n')
        with patch.object(integrity,'ITEMS',frozenset(['einsum'])),patch.object(integrity,'ORIGINAL_PRODUCER',original):
            r=attest_ai3_cache.attest(self.cache,root,src,completion,expected,log,log)
            self.assertTrue(r['payload_bytes_sizes_mtimes_unchanged'])
            self.assertEqual(json.loads(integrity.sidecar_path(self.cache,'einsum').read_text())['origin'],'postproduction-attestation')
            p=self.cache/'einsum.json';p.write_text(p.read_text()+' ')
            with self.assertRaises(integrity.IntegrityError):attest_ai3_cache.attest(self.cache,root,src,completion,expected,log,log)

    def test_migration_preflights_all_items_before_any_sidecar_publication(self):
        root=Path(self.tmp.name)/'root';src=root/'videos/ai/ai3/compute.py';src.parent.mkdir(parents=True);src.write_bytes(SOURCE.read_bytes())
        for name in ('depth','einsum'):write_fixture(self.cache,name)
        pairs={n:integrity.inspect_payload(n,self.cache) for n in ('depth','einsum')}
        original=integrity.digest(src);completion=Path(self.tmp.name)/'completion.json';expected=Path(self.tmp.name)/'expected.json';log=Path(self.tmp.name)/'run.log'
        completion.write_text(json.dumps({'producer_sha256':original,'cache_json_sha256':{n:p['json_sha256'] for n,p in pairs.items()}}))
        pairs['einsum']['json_sha256']='wrong'
        expected.write_text(json.dumps({'producer_sha256':original,'items':pairs}))
        log.write_text('  compute depth ...\n  done    depth in 0s\n  compute einsum ...\n  done    einsum in 0s\n')
        with patch.object(integrity,'ITEMS',frozenset(['depth','einsum'])),patch.object(integrity,'ORIGINAL_PRODUCER',original):
            with self.assertRaises(integrity.IntegrityError):attest_ai3_cache.attest(self.cache,root,src,completion,expected,log,log)
        self.assertFalse(integrity.sidecar_path(self.cache,'depth').exists())
        self.assertFalse(integrity.sidecar_path(self.cache,'einsum').exists())


if __name__=='__main__':unittest.main()
