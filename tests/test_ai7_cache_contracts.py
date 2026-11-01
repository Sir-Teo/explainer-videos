"""Temporary tiny artifacts only; no Part7 producer/model/data generation."""
from __future__ import annotations

import copy
import ast
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import time
import unittest
import zipfile
from unittest import mock

import numpy as np

from videos.ai.ai7 import contracts as C
from videos.ai.ai7.cache_contract import CacheValidationError, SchemaCache, canonical


def reparam():
    h=np.zeros(80,dtype=int);h[40]=2
    return dict(m=.5,true=-3.,score_mean=-3.,rep_mean=-3.,score_sd=2.,rep_sd=1.,ratio=4.,
                R=2,bins=np.linspace(-25,15,81),h_score=h,h_rep=h.copy())


def bayesopt():
    xs=np.array([.2,.8]);ys=np.array([2.,1.])
    return dict(order=5,valid_chars=20,grid=np.linspace(.05,.95,31),truth=np.ones(31),cand=np.linspace(.02,.98,400),
                xs=xs,ys=ys,best_D=.8,best_bits=1.,grid_best_D=.05,grid_best_bits=1.,gt_D=[.5]*6,gt_bits=1.1,
                evals=2,grid_evals=31,steps_x=[xs.tolist()],steps_y=[ys.tolist()],
                steps_mean=np.ones((1,400)),steps_sd=np.ones((1,400)),steps_ei=np.ones((1,400)),steps_next=[.4])


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='ai7-contract-test-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.cache=SchemaCache('ai7');self.cache.dir=self.root/'.cache/ai7';self.cache.repo_root=self.root
        self.env=mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'0',**{k:'1'for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')}})
        self.env.start();self.addCleanup(self.env.stop)
        # Tiny stand-in source bytes bind a fixture registry, not real numerical producers.
        paths=('videos/ai/ai7/compute.py','videos/ai/ai7/contracts.py','videos/ai/ai7/cache_contract.py',
               'videos/ai/ai7/infini.py','videos/ai/ai1/compute.py','videos/ai/ai5/compute.py',
               'videos/ai/ai6/compute.py','videos/ai/ai6/contracts.py','videos/ai/ai6/cache_contract.py',
               'explainer/ai/cache.py','explainer/cache_lock.py')
        for name in paths:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# fixture source\n')
        self.items={name:mock.Mock(side_effect=AssertionError('unexpected fixture producer'))for name in C.REQUIRED}
        self.items['reparam']=mock.Mock(side_effect=reparam)
        self.cache.bind(self.items)

    def texts(self):
        for name in ('train','valid','passage'):
            p=self.root/f'.cache/ai1/{name}.txt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('abcdefghijklmnopqrst')

    def publish_bayes(self):
        self.texts()
        def producer():
            for name in ('train','valid','passage'):self.cache.read_text(name)
            return bayesopt()
        self.items['bayesopt']=mock.Mock(side_effect=producer)
        self.cache.bind(self.items)
        return self.cache.load('bayesopt')

    def test_known_inventory_and_missing_status_is_pure(self):
        self.assertEqual(len(C.REQUIRED),24)
        self.assertEqual(self.cache.status('not-an-item')['status'],'unknown')
        self.assertFalse(self.cache.current('reparam'))
        self.assertFalse(self.cache.dir.exists())
        self.items['reparam'].assert_not_called()

    def test_cached_only_missing_never_imports_or_calls_producer(self):
        with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'1'}),mock.patch('importlib.import_module',side_effect=AssertionError('producer import')):
            with self.assertRaises(CacheValidationError):self.cache.load('reparam')
        self.assertFalse(self.cache.dir.exists());self.items['reparam'].assert_not_called()

    def test_publish_and_actual_load_preserve_numeric_api(self):
        out=self.cache.load('reparam');self.assertIsInstance(out['bins'],np.ndarray)
        self.assertTrue(self.cache.current('reparam'));self.assertEqual(self.items['reparam'].call_count,1)
        self.cache.load('reparam');self.assertEqual(self.items['reparam'].call_count,1)
        raw=json.loads(self.cache.path('reparam').read_text());self.assertEqual(raw['_cache']['observed_reads'],{})

    def test_mutated_returned_arrays_do_not_poison_later_validated_load(self):
        out=self.cache.load('reparam');out['bins'][0]=999.;out['ratio']=999.
        again=self.cache.load('reparam');self.assertEqual(again['bins'][0],-25.);self.assertEqual(again['ratio'],4.)
        self.assertEqual(self.items['reparam'].call_count,1)

    def test_metadata_free_legacy_is_preserved_before_replacement(self):
        self.cache.dir.mkdir(parents=True);p=self.cache.path('reparam');original=b'{"legacy": true}\n';p.write_bytes(original)
        self.assertEqual(self.cache.status('reparam')['status'],'legacy')
        self.cache.load('reparam')
        preserved=list((self.cache.dir/'preserved').glob('*/reparam.json'))
        self.assertEqual(len(preserved),1);self.assertEqual(preserved[0].read_bytes(),original)

    def test_cached_only_legacy_never_migrates_or_changes_bytes(self):
        self.cache.dir.mkdir(parents=True);p=self.cache.path('reparam');p.write_text('{"legacy":true}');before=p.read_bytes();before_stat=p.stat()
        with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'1'}):
            with self.assertRaises(CacheValidationError):self.cache.load('reparam')
        self.assertEqual(p.read_bytes(),before);self.assertEqual(p.stat().st_mtime_ns,before_stat.st_mtime_ns)
        self.assertEqual(list(self.cache.dir.iterdir()),[p]);self.items['reparam'].assert_not_called()

    def test_malformed_top_levels_and_metadata_fail_closed_without_writes(self):
        self.cache.dir.mkdir(parents=True);p=self.cache.path('reparam')
        for value in (None,[],5,'text',{'_cache':[]},{'_cache':True},{'_cache':{'schema_version':True}}):
            with self.subTest(value=value):
                p.write_text(json.dumps(value));before=p.read_bytes()
                with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'1'}):
                    self.assertFalse(self.cache.current('reparam'))
                    with self.assertRaises(CacheValidationError):self.cache.load('reparam')
                self.assertEqual(p.read_bytes(),before)
        self.assertFalse((self.cache.dir/'preserved').exists())

    def test_payload_tamper_is_stale_even_after_prior_load(self):
        self.cache.load('reparam');p=self.cache.path('reparam');d=json.loads(p.read_text());d['ratio']=8;p.write_text(json.dumps(d))
        self.assertFalse(self.cache.current('reparam'))
        with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'1'}):
            with self.assertRaises(CacheValidationError):self.cache.load('reparam')

    def test_npz_tamper_and_missing_arrays_are_rejected(self):
        self.cache.load('reparam');p=self.cache.path('reparam').with_suffix('.npz')
        np.savez(p,bins=np.linspace(-25,15,81),h_score=np.zeros(80),h_rep=np.zeros(80))
        self.assertFalse(self.cache.current('reparam'));p.unlink();self.assertFalse(self.cache.current('reparam'))

    def test_corrupt_npz_is_not_treated_as_cache_hit(self):
        self.cache.load('reparam');p=self.cache.path('reparam').with_suffix('.npz');p.write_bytes(b'PK\x03\x04broken')
        self.assertFalse(self.cache.current('reparam'))

    def test_member_crc_failure_cannot_be_blessed_by_updating_outer_hash(self):
        self.cache.load('reparam');p=self.cache.path('reparam').with_suffix('.npz')
        # Stored member corruption: keep the original ZIP CRC but change a data byte.
        with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_STORED)as z:
            import io
            for key,value in reparam().items():
                if isinstance(value,np.ndarray):
                    b=io.BytesIO();np.save(b,value);z.writestr(key+'.npy',b.getvalue())
        data=bytearray(p.read_bytes())
        with zipfile.ZipFile(p)as z:
            member=z.infolist()[0];offset=member.header_offset
            start=offset+30+len(member.filename.encode())+len(member.extra)
        data[start+150]^=1;p.write_bytes(data)
        marker=self.cache.path('reparam');raw=json.loads(marker.read_text())
        import hashlib
        raw['_cache']['arrays_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();marker.write_text(json.dumps(raw))
        self.assertFalse(self.cache.current('reparam'))

    def test_duplicate_json_key_is_not_silently_last_wins(self):
        self.cache.dir.mkdir(parents=True);p=self.cache.path('reparam');p.write_text('{"R":2,"R":3}')
        self.assertFalse(self.cache.current('reparam'))
        self.assertIn('Duplicate JSON key',self.cache.status('reparam')['reason'])

    def test_source_drift_rejects_old_loaded_producer(self):
        self.cache.load('reparam');(self.root/'videos/ai/ai7/compute.py').write_text('# changed producer\n')
        self.assertFalse(self.cache.current('reparam'))
        with self.assertRaises(CacheValidationError):self.cache.bind(self.items)

    def test_runtime_drift_rejects_completed_result(self):
        self.cache.load('reparam')
        with mock.patch.object(C,'runtime_identity',return_value={'different':'runtime'}):self.assertFalse(self.cache.current('reparam'))

    def test_normal_load_serializes_two_readers_to_one_fake_generation(self):
        calls=[];barrier=threading.Barrier(2);errors=[]
        def producer():calls.append(1);time.sleep(.02);return reparam()
        self.items['reparam']=producer;self.cache.bind(self.items)
        def run():
            try:barrier.wait();self.cache.load('reparam')
            except Exception as exc:errors.append(exc)
        threads=[threading.Thread(target=run)for _ in range(2)]
        for t in threads:t.start()
        for t in threads:t.join(2)
        self.assertFalse(any(t.is_alive()for t in threads));self.assertEqual(errors,[]);self.assertEqual(len(calls),1)

    def test_cli_existing_marker_must_be_current_not_merely_present(self):
        self.cache.dir.mkdir(parents=True);self.cache.path('reparam').write_text('null')
        with mock.patch.object(sys,'argv',['compute','reparam']):self.cache.main(self.items)
        self.assertTrue(self.cache.current('reparam'));self.items['reparam'].assert_called_once()

    def test_cli_cached_only_force_and_missing_do_not_write(self):
        with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'1'}):
            for flags in (['reparam'],['--force','reparam']):
                with mock.patch.object(sys,'argv',['compute']+flags),self.assertRaises(CacheValidationError):self.cache.main(self.items)
        self.assertFalse(self.cache.dir.exists());self.items['reparam'].assert_not_called()

    def test_cli_check_is_pure_and_returns_failure_for_missing(self):
        with mock.patch.object(sys,'argv',['compute','--check','reparam']),self.assertRaises(SystemExit)as got:self.cache.main(self.items)
        self.assertEqual(got.exception.code,1);self.assertFalse(self.cache.dir.exists())

    def test_failed_publication_leaves_absent_marker_and_preserved_old_bytes(self):
        self.cache.load('reparam');p=self.cache.path('reparam');old=p.read_bytes();replace=Path.replace
        def fail_marker(obj,target):
            if obj.name=='reparam.tmp.json':raise OSError('simulated marker commit interruption')
            return replace(obj,target)
        with mock.patch.object(Path,'replace',fail_marker),self.assertRaises(OSError):self.cache._produce('reparam',reparam,force=True)
        self.assertFalse(p.exists());self.assertTrue(any(q.read_bytes()==old for q in(self.cache.dir/'preserved').glob('*/reparam.json')))

    def test_prerequisite_miss_does_not_create_corpus_or_import_producer(self):
        with mock.patch('importlib.import_module',side_effect=AssertionError('producer import')):
            with self.assertRaises(CacheValidationError):self.cache.require_inputs('hmm')
            with self.assertRaises(CacheValidationError):self.cache.read_text('train')
        self.assertFalse((self.root/'.cache/ai1').exists())

    def test_fresh_text_reader_observes_changes_and_matches_normalizer(self):
        self.texts();p=self.root/'.cache/ai1/train.txt';p.write_text('CAFÉ!\r\nTree—two.')
        self.assertEqual(self.cache.read_text('train27'),'cafe treetwo')
        p.write_text('NEW actual bytes');self.assertEqual(self.cache.read_text('train'),'NEW actual bytes')

    def test_bayesopt_dependency_reads_are_observed_and_bound(self):
        self.publish_bayes();raw=json.loads(self.cache.path('bayesopt').read_text());meta=raw['_cache']
        self.assertEqual(set(meta['observed_reads']),{'ai1/train.txt','ai1/valid.txt','ai1/passage.txt'})
        self.assertTrue(self.cache.current('bayesopt'))
        (self.root/'.cache/ai1/valid.txt').write_text('a different validation corpus')
        self.assertFalse(self.cache.current('bayesopt'))

    def test_publication_rejects_prerequisites_only_preflighted_not_read(self):
        self.texts();self.items['bayesopt']=bayesopt;self.cache.bind(self.items)
        with self.assertRaisesRegex(CacheValidationError,'not read'):self.cache.load('bayesopt')
        self.assertFalse(self.cache.path('bayesopt').exists())

    def test_one_threads_read_cannot_attest_another_generations_consumption(self):
        self.texts();entered=threading.Event();read=threading.Event();errors=[]
        def no_read_hmm():
            entered.set();self.assertTrue(read.wait(2));b=np.full((2,27),1/27)
            return dict(A=np.full((2,2),.5),B=b,pi=np.full(2,.5),Bs=np.stack([b]*61),lls=np.zeros(61),
                        vowel_side=['a'],sentence='a',states=[0],n=20,post=np.full((2,27),.5))
        def reads_bayes():
            self.assertTrue(entered.wait(2))
            for name in ('train','valid','passage'):self.cache.read_text(name)
            read.set();return bayesopt()
        self.items.update(hmm=no_read_hmm,bayesopt=reads_bayes);self.cache.bind(self.items)
        def run(name):
            try:self.cache.load(name)
            except Exception as exc:errors.append((name,exc))
        threads=[threading.Thread(target=run,args=(name,))for name in ('hmm','bayesopt')]
        for t in threads:t.start()
        for t in threads:t.join(3)
        self.assertFalse(any(t.is_alive()for t in threads));self.assertEqual(len(errors),1)
        self.assertEqual(errors[0][0],'hmm');self.assertIsInstance(errors[0][1],CacheValidationError)
        self.assertIn('not read',str(errors[0][1]));self.assertTrue(self.cache.current('bayesopt'))
        self.assertFalse(self.cache.path('hmm').exists())

    def test_mid_generation_input_change_never_publishes(self):
        self.texts()
        def producer():
            for name in ('train','valid','passage'):self.cache.read_text(name)
            (self.root/'.cache/ai1/train.txt').write_text('changed during fake generation')
            return bayesopt()
        self.items['bayesopt']=producer;self.cache.bind(self.items)
        with self.assertRaises(CacheValidationError):self.cache.load('bayesopt')
        self.assertFalse(self.cache.path('bayesopt').exists())

    def test_undeclared_reader_fails_even_after_all_expected_reads(self):
        self.texts();self.cache.dir.mkdir(parents=True)
        (self.cache.dir.parent/'ai1/extra.txt').write_text('undeclared fixture')
        def producer():
            for name in ('train','valid','passage'):self.cache.read_text(name)
            self.cache._consume_text(self.cache.dir.parent/'ai1/extra.txt')
            return bayesopt()
        self.items['bayesopt']=producer;self.cache.bind(self.items)
        with self.assertRaisesRegex(CacheValidationError,'Undeclared dependency'):self.cache.load('bayesopt')
        self.assertFalse(self.cache.path('bayesopt').exists())

    def interrupted_partial(self,force=False,expected_reuse=None):
        self.texts() if not(self.root/'.cache/ai1/train.txt').exists()else None
        seen=[]
        def producer():
            for name in ('train','valid','passage'):self.cache.read_text(name)
            part=self.cache.partial('bayesopt',dict(order=5,valid=200000));seen.append('grid_0.5000'in part)
            part['grid_0.5000']=1.25
            raise InterruptedError('tiny interrupted fixture')
        with self.assertRaises(InterruptedError):self.cache._produce('bayesopt',producer,force=force)
        if expected_reuse is not None:self.assertEqual(seen,[expected_reuse])

    def test_partial_resumes_only_matching_lineage_and_valid_piece(self):
        self.interrupted_partial(expected_reuse=False);self.interrupted_partial(expected_reuse=True)
        d=json.loads((self.cache.dir/'bayesopt.partial.json').read_text())
        self.assertEqual(d['params']['configuration'],C.BAYESOPT);self.assertEqual(d['done_sha256'],canonical(d['done']))

    def test_force_partial_never_reuses_old_piece_and_preserves_bytes(self):
        self.interrupted_partial();p=self.cache.dir/'bayesopt.partial.json';old=p.read_bytes()
        self.interrupted_partial(force=True,expected_reuse=False)
        self.assertTrue(any(q.read_bytes()==old for q in(self.cache.dir/'preserved').glob('*/bayesopt.partial.json')))

    def test_partial_input_drift_and_checksum_tamper_reject_reuse(self):
        self.interrupted_partial();p=self.cache.dir/'bayesopt.partial.json'
        (self.root/'.cache/ai1/valid.txt').write_text('new corpus');self.interrupted_partial(expected_reuse=False)
        d=json.loads(p.read_text());d['done']['grid_0.5000']=9.;p.write_text(json.dumps(d));self.interrupted_partial(expected_reuse=False)

    def test_malformed_partial_top_levels_are_preserved_not_reused(self):
        self.texts();self.cache.dir.mkdir(parents=True)
        p=self.cache.dir/'bayesopt.partial.json'
        for value in (None,[],5,{'schema_version':True,'done':[]}):
            with self.subTest(value=value):
                p.write_text(json.dumps(value));old=p.read_bytes()
                self.interrupted_partial(expected_reuse=False)
                self.assertTrue(any(q.read_bytes()==old for q in(self.cache.dir/'preserved').glob('*/bayesopt.partial.json')))

    def test_partial_source_or_runtime_drift_invalidates_reuse(self):
        self.interrupted_partial()
        with mock.patch.object(C,'runtime_identity',return_value={'fixture':'new runtime'}):
            self.interrupted_partial(expected_reuse=False)
        # Restoring the earlier runtime also cannot reuse pieces generated in the other one.
        self.interrupted_partial(expected_reuse=False)

    def test_partial_nonfinite_invalid_key_and_outside_generation_rejected(self):
        with self.assertRaises(CacheValidationError):self.cache.partial('bayesopt',dict(order=5,valid=200000))
        self.texts()
        def producer():
            part=self.cache.partial('bayesopt',dict(order=5,valid=200000))
            for key,value in [('grid_0.5000',float('nan')),('grid_0.5000',True),('x_9.000000',1.),('bogus',1.)]:
                with self.assertRaises((ValueError,CacheValidationError)):part[key]=value
            raise InterruptedError()
        with self.assertRaises(InterruptedError):self.cache._produce('bayesopt',producer)

    def test_partial_parameters_cannot_silently_change_inside_generation(self):
        self.texts()
        def producer():
            self.cache.partial('bayesopt',dict(order=5,valid=200000))
            self.cache.partial('bayesopt',dict(order=4,valid=200000))
        with self.assertRaises(CacheValidationError):self.cache._produce('bayesopt',producer)

    def test_missing_or_stale_upstream_is_checked_before_hashing_pages(self):
        with mock.patch.object(self.cache,'_upstream_status',side_effect=CacheValidationError('upstream stale'))as status:
            with self.assertRaisesRegex(CacheValidationError,'upstream stale'):self.cache.require_inputs('pca')
        status.assert_called_once_with('ai6','pages');self.items['pca'].assert_not_called()

    def test_actual_local_dag_and_upstream_hash_change(self):
        folder=self.root/'.cache/ai6';folder.mkdir(parents=True)
        (folder/'pages.json').write_text(json.dumps({'vocab':[f'w{i}'for i in range(70)],'protocol':{'fixture':True}}))
        np.savez(folder/'pages.npz',X=np.zeros((4,70)),X2=np.zeros((4,2)),y=np.array([0,0,1,1]),
                 test=np.array([0,1,0,1],bool),book=np.array([1342,1342,1400,1400]))
        calls=[]
        def pca():
            pages=self.cache.read_pages();calls.append('pca')
            return dict(share=np.full(70,1/70),proj=np.zeros((4,3)),y=pages['y'],top={'0':[],'1':[]},split=.5,n=4,d=70)
        def gmm():
            pc=self.cache.load('pca');pages=self.cache.read_pages();calls.append('gmm')
            return dict(P=pc['proj'][:,:2],y=pages['y'],means=np.zeros((40,2,2)),
                        covs=np.tile(np.eye(2),(40,2,1,1)),w=np.full((40,2),.5),ll=np.zeros(40),
                        r=np.full((40,4),.5),agree=.5,covariance_floor=1e-6)
        self.items.update(pca=pca,gmm=gmm);self.cache.bind(self.items)
        # Only the external validator is replaced; real recursive local status/load/save executes.
        with mock.patch.object(self.cache,'_upstream_status'):
            self.cache.load('gmm');self.assertEqual(calls,['pca','gmm'])
            self.assertTrue(self.cache.current('pca'));self.assertTrue(self.cache.current('gmm'))
            p=folder/'pages.json';data=json.loads(p.read_text());data['protocol']['new']=True;p.write_text(json.dumps(data))
            self.assertFalse(self.cache.current('pca'));self.assertFalse(self.cache.current('gmm'))

    def test_known_external_reader_never_falls_back_to_part1_models(self):
        with mock.patch('importlib.import_module',side_effect=AssertionError('producer import')):
            with self.assertRaises(FileNotFoundError):self.cache.read_part1('scoreboard')
        self.assertFalse((self.root/'.cache/ai1').exists())


class ShapeTests(unittest.TestCase):
    def test_hmm_histories_require_aligned_initial_and_final_round(self):
        b=np.full((2,27),1/27);d=dict(A=np.full((2,2),.5),B=b,pi=np.full(2,.5),
            Bs=np.stack([b]*61),lls=np.zeros(61),vowel_side=['a'],sentence='a',states=[0],n=10,post=np.full((2,27),.5))
        self.assertTrue(C.valid_structure('hmm',d));d['lls']=np.zeros(60);self.assertFalse(C.valid_structure('hmm',d))

    def test_ibm_histories_align_and_probability_rows_normalize(self):
        d={k:[]for k in C.REQUIRED['ibm1'].split()};d.update(F=['a'],E=['b'],t=np.ones((31,2,1)),lls=np.zeros(31),
            align=np.full((31,1,2),.5),example=['a','b'],n_train=1,
            bleu_gloss={'bleu':1.,'p':[1.]*4},bleu_rule={'bleu':1.,'p':[1.]*4})
        self.assertTrue(C.valid_structure('ibm1',d));d['lls']=np.zeros(30);self.assertFalse(C.valid_structure('ibm1',d))

    def test_expected_invalid_extrapolation_is_a_paired_nan_gap_not_infinity(self):
        d=dict(ts=np.linspace(-.5,1.6,85),i0=20,i1=60,rounds=[0,1,2,4],ll=np.ones((4,85)),bound=np.ones((4,85)))
        d['ll'][:,0]=np.nan;d['bound'][:,0]=np.nan;self.assertTrue(C.valid_structure('embound',d))
        d['bound'][0,0]=0;self.assertFalse(C.valid_structure('embound',d));d['bound'][0,0]=np.inf;self.assertFalse(C.valid_structure('embound',d))

    def test_bayesopt_prefix_shapes_and_observed_best_are_consistent(self):
        d=bayesopt();self.assertTrue(C.valid_structure('bayesopt',d));d['steps_y']=[[1.,2.]];self.assertFalse(C.valid_structure('bayesopt',d))

    def test_histogram_counts_are_counts_not_a_finiteness_only_check(self):
        d=reparam();self.assertTrue(C.valid_structure('reparam',d));d['h_score'][0]=1;self.assertFalse(C.valid_structure('reparam',d))

    def test_preferred_success_is_not_a_reparam_schema_condition(self):
        d=reparam();d['ratio']=.5;self.assertTrue(C.valid_structure('reparam',d))

    def test_infini_empty_long_cohort_is_unavailable_not_zero_or_nan(self):
        d={k:[]for k in C.REQUIRED['infini'].split()}
        d.update(K=3,n=20,M=0,types=[3],discounts=[.5],L=np.array([0,1,2]),hist=np.r_[np.ones(3),np.zeros(38)],
                 lam=np.zeros((7,2)),mix_bits=1.,kn_bits=2.,gain=1.,acc=.5,zero=0.,sparse=0.,
                 acc_long=None,long_count=0,share_long=0.)
        self.assertTrue(C.valid_structure('infini',d))
        for wrong in [0.,float('nan'),.5]:
            d['acc_long']=wrong;self.assertFalse(C.valid_structure('infini',d))
        d['L']=np.array([0,10,2]);d['hist']=np.bincount(d['L'],minlength=41);d['long_count']=1;d['acc_long']=.5
        self.assertTrue(C.valid_structure('infini',d));d['long_count']=0;self.assertFalse(C.valid_structure('infini',d))

    def test_public_normalizer_has_shannon_alphabet_and_real_accents(self):
        self.assertEqual(C.to27('Café 42, naïve!'),'cafe naive')


class ReaderIntegrationTests(unittest.TestCase):
    def functions(self,*names):
        path=Path(__file__).resolve().parents[1]/'videos/ai/ai7/compute.py'
        tree=ast.parse(path.read_text())
        return [n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names]

    def test_actual_entrypoints_follow_later_instance_guard_and_pages_reader(self):
        cache=mock.Mock();cache.load.return_value={'guarded':True};cache.current.return_value=False
        cache.read_pages.return_value={'X':[[1.,2.]],'y':[1],'book':[1400],'vocab':['the','not']}
        namespace={'CACHE':cache,'np':np}
        exec(compile(ast.Module(body=self.functions('load','cache_current','pages'),type_ignores=[]),'actual Part7 entrypoint AST','exec'),namespace)
        self.assertEqual(namespace['load']('kn'),{'guarded':True});cache.load.assert_called_once_with('kn')
        self.assertFalse(namespace['cache_current']('gp'));cache.current.assert_called_once_with('gp')
        cache.load=lambda name:{'later_guard':name};self.assertEqual(namespace['load']('kn'),{'later_guard':'kn'})
        x,y,book,vocab=namespace['pages']();self.assertEqual(x.shape,(1,2));self.assertEqual(vocab,['the','not'])
        cache.read_pages.assert_called_once()

    def test_actual_character_codec_uses_fresh_three_input_reads(self):
        cache=mock.Mock();cache.read_text.side_effect=lambda key:{'train':'aba','valid':'abc','passage':'cab'}[key]
        namespace={'CACHE':cache,'np':np,'ai1':lambda:object()}
        exec(compile(ast.Module(body=self.functions('chars_codec'),type_ignores=[]),'actual Part7 codec AST','exec'),namespace)
        chars,encode,train,valid,passage=namespace['chars_codec']()
        self.assertEqual(chars,['a','b','c']);np.testing.assert_array_equal(encode('ca'),[2,0])
        self.assertEqual([x.args for x in cache.read_text.call_args_list],[('train',),('valid',),('passage',)])

    def test_actual_producers_have_no_unprotected_upstream_data_calls(self):
        path=Path(__file__).resolve().parents[1]/'videos/ai/ai7/compute.py';tree=ast.parse(path.read_text())
        forbidden=[]
        for n in ast.walk(tree):
            if (isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)
                    and n.func.value.id in ('c1','c5','c6')and n.func.attr in ('load','text')):forbidden.append(n.lineno)
        self.assertEqual(forbidden,[],'Part7 must not silently compute upstream or consume memoized text')


if __name__=='__main__':unittest.main()
