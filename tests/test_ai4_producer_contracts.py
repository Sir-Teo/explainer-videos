"""Small real-kernel/temp-cache/fake-HTTP checks; no production corpus, weights or training."""
from contextlib import contextmanager
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai4 import compute as c
from videos.ai.ai4 import contracts as k
from videos.ai.ai4.cache_contract import SchemaCache


class RangeTests(unittest.TestCase):
    def response(self, body=b"12345678", status=206, content_range="bytes 0-7/1000"):
        class Response(io.BytesIO):
            def __init__(self):
                super().__init__(body)
                self.status = status
                self.headers = {"Content-Range": content_range}
                self.requests = []
            def read(self, size=-1):
                self.requests.append(size)
                if size < 0:
                    raise AssertionError("unbounded response read")
                return super().read(size)
        return Response()

    def test_exact_range_bounded_by_requested_bytes_plus_one(self):
        response = self.response()
        self.assertEqual(k.read_range("https://example.test/model", 0, 8, opener=lambda *a, **kw: response), b"12345678")
        self.assertEqual(response.requests, [9])

    def test_ignored_range_is_closed_without_consuming_model(self):
        response = self.response(status=200)
        with self.assertRaisesRegex(ValueError, "honor"):
            k.read_range("https://example.test/model", 0, 8, opener=lambda *a, **kw: response)
        self.assertEqual(response.requests, [])

    def test_short_oversized_wrong_range_and_wrong_total_rejected(self):
        for kwargs in [dict(body=b"123"), dict(body=b"123456789"), dict(content_range="bytes 1-8/1000"), dict(content_range="bytes 0-7/7")]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                k.read_range("https://example.test/model", 0, 8, opener=lambda *a, **kw:self.response(**kwargs))

    def test_metadata_read_is_bounded(self):
        response = self.response(body=b"x"*20)
        with self.assertRaisesRegex(ValueError, "size limit"):
            k.bounded_json("https://example.test/config", limit=4, opener=lambda *a, **kw:response)
        self.assertEqual(response.requests, [5])

    def test_header_length_limit_stops_before_second_request(self):
        with patch.object(k, "bounded_json", return_value=({"model_type":"gpt2"}, "config")), \
                patch.object(k, "read_range", return_value=struct.pack("<Q", 9*1024*1024)) as read:
            with self.assertRaisesRegex(ValueError, "unsafe"):
                k.parameter_headers("gpt2")
        self.assertEqual(read.call_count, 1)

    def test_header_count_excludes_buffers_and_declared_tied_output(self):
        tensors = {"transformer.wte.weight":{"shape":[4,3]}, "lm_head.weight":{"shape":[4,3]},
                   "transformer.h.0.attn.bias":{"shape":[1,1,10,10]}, "transformer.h.0.attn.c_attn.bias":{"shape":[9]}}
        raw=json.dumps(tensors).encode()
        with patch.object(k, "bounded_json", return_value=({"model_type":"gpt2"},"config")), \
                patch.object(k, "read_range", side_effect=[struct.pack("<Q",len(raw)),raw]):
            count, provenance=k.parameter_headers("gpt2")
        self.assertEqual(count,21)
        self.assertEqual(len(provenance['excluded']),2)
        self.assertEqual(provenance['source'],'pinned-safetensors-headers')

    def test_each_model_fallback_is_independent_and_explicit(self):
        with patch.object(k, "parameter_headers", side_effect=[(13,dict(source='pinned-safetensors-headers')), OSError('offline')]):
            out=k.parameter_counts()
        self.assertEqual(out['gpt2'],13)
        self.assertEqual(out['qwen3_4b'],k.MODEL_HEADERS['qwen3_4b']['historical'])
        self.assertEqual(out['provenance']['gpt2']['source'],'pinned-safetensors-headers')
        self.assertEqual(out['provenance']['qwen3_4b']['source'],'historical-fallback')
        self.assertIn('offline',out['provenance']['qwen3_4b']['error'])


class CacheTests(unittest.TestCase):
    @contextmanager
    def cache(self):
        with tempfile.TemporaryDirectory() as td:
            cache=SchemaCache('ai4');cache.dir=Path(td)/'ai4';cache.items={'tiny':lambda:dict(value=4.,inputs={},values={},grads={})}
            yield cache

    def test_missing_and_legacy_validation_never_invokes_producer(self):
        with self.cache() as cache, patch.dict(cache.items, tiny=lambda:self.fail('producer invoked')):
            self.assertFalse(cache.current('tiny'))
            cache.path('tiny').write_text('{"legacy":true}')
            self.assertFalse(cache.current('tiny'))

    def test_malformed_top_level_is_stale_through_actual_cached_only_guard(self):
        from tools.qa_series import require_current_cache, StaleDataError
        with self.cache() as cache, patch.object(c,'CACHE',cache), \
                patch.object(cache,'_produce',side_effect=AssertionError('producer invoked')) as produce:
            for value in (None,0,False,'text',[],[1,2]):
                with self.subTest(value=value):
                    path=cache.path('tiny');path.parent.mkdir(parents=True,exist_ok=True)
                    raw=json.dumps(value);path.write_text(raw);before=path.stat().st_mtime_ns
                    with self.assertRaises(StaleDataError):require_current_cache(c,'ai4',path,'tiny')
                    self.assertEqual(path.read_text(),raw);self.assertEqual(path.stat().st_mtime_ns,before)
            self.assertFalse(cache.current('unknown-item'))
            produce.assert_not_called()

    def test_json_and_npz_tamper_fail_closed(self):
        with self.cache() as cache:
            cache.save('tiny',dict(x=np.array([1.,2]),value=3.,inputs={},values={},grads={}))
            self.assertTrue(cache.current('tiny'))
            data=json.loads(cache.path('tiny').read_text());data['value']=4
            cache.path('tiny').write_text(json.dumps(data));self.assertFalse(cache.current('tiny'))
            cache.save('tiny',dict(x=np.array([1.,2]),value=3.,inputs={},values={},grads={}))
            cache.path('tiny').with_suffix('.npz').write_bytes(b'badzip');self.assertFalse(cache.current('tiny'))

    def test_recipe_and_dependency_drift_refuse_old_cache(self):
        with self.cache() as cache:
            corpus=cache.dir.parent/'ai1';corpus.mkdir();(corpus/'train.txt').write_text('abc')
            cache.save('grad0',dict(grad=np.zeros((27,27)),diff=0,pairs=1,top=[]))
            self.assertTrue(cache.current('grad0'))
            (corpus/'train.txt').write_text('abd');self.assertFalse(cache.current('grad0'))
            cache.save('tiny',dict(value=1,inputs={},values={},grads={}))
            with patch.object(cache,'recipe',return_value={'changed':True}):
                self.assertFalse(cache.current('tiny'))

    def test_source_or_consumed_dependency_change_aborts_publication(self):
        with self.cache() as cache:
            def changed():
                (cache.dir.parent/'ai1/train.txt').write_text('mutated')
                return dict(value=1,inputs={},values={},grads={})
            corpus=cache.dir.parent/'ai1';corpus.mkdir();(corpus/'train.txt').write_text('original')
            with self.assertRaisesRegex(ValueError,'consumed corpus'):
                cache._produce('grad0',changed)
            self.assertFalse(cache.path('grad0').exists())
            with patch.object(cache,'recipe',side_effect=[dict(v=1),dict(v=2)]):
                with self.assertRaisesRegex(ValueError,'source changed'):
                    cache._produce('tiny',lambda:dict(value=1,inputs={},values={},grads={}))

    def test_load_and_cli_use_schema_with_item_lock(self):
        import sys
        from explainer.cache_lock import _local
        with self.cache() as cache:
            observations=[]
            def producer():
                observations.append(cache.path('tiny').resolve() in _local.held)
                return dict(value=7,inputs={},values={},grads={})
            cache.items={'tiny':producer}
            self.assertEqual(cache.load('tiny')['value'],7)
            self.assertEqual(observations,[True])
            cache.path('tiny').write_text('{}')
            with patch.object(sys,'argv',['compute','tiny']):cache.main(cache.items)
            self.assertEqual(observations,[True,True]);self.assertTrue(cache.current('tiny'))

    def test_concurrent_loads_publish_once_and_reuse_same_completed_item(self):
        from concurrent.futures import ThreadPoolExecutor
        import threading
        with self.cache() as cache:
            started,release=threading.Event(),threading.Event()
            calls=[]
            def producer():
                calls.append(1);started.set()
                if not release.wait(2):raise AssertionError('test release missing')
                return dict(value=7,inputs={},values={},grads={})
            cache.items={'tiny':producer}
            with ThreadPoolExecutor(max_workers=2) as pool:
                one=pool.submit(cache.load,'tiny');self.assertTrue(started.wait(2))
                two=pool.submit(cache.load,'tiny');release.set()
                self.assertEqual(one.result()['value'],7);self.assertEqual(two.result()['value'],7)
            self.assertEqual(len(calls),1);self.assertTrue(cache.current('tiny'))

    def test_dynamic_load_can_be_guarded_before_schema_upgrade(self):
        with patch.object(c.CACHE,'load',side_effect=FileNotFoundError('cached-only missing')), \
                patch.object(c.CACHE,'_produce') as produce:
            with self.assertRaises(FileNotFoundError):c.load('tiny')
            produce.assert_not_called()


class NumericalTests(unittest.TestCase):
    def test_optional_blas_probe_cannot_break_real_benchmark_context(self):
        import builtins
        original=builtins.__import__
        def without_optional(name,*args,**kwargs):
            if name=='threadpoolctl':raise ImportError('optional package absent')
            return original(name,*args,**kwargs)
        with patch('builtins.__import__',side_effect=without_optional):report=k.benchmark_context()
        self.assertEqual(report['native_threadpools']['status'],'unavailable')
        self.assertIn('torch_threads',report)

    def test_timing_protocol_keeps_actual_repeat_spread_and_warmup(self):
        seen=[];before=len(c._TIMINGS)
        elapsed=c._timeit(lambda:seen.append(1),3)
        report=c._TIMINGS[before]
        self.assertEqual(len(seen),4)
        self.assertEqual(report['repeats'],3)
        self.assertEqual(len(report['seconds']),3)
        self.assertEqual(elapsed,np.mean(report['seconds']))

    def test_stopping_preserves_miss_and_success_on_last_permitted_update(self):
        a=k.stopping([2,1],.5,1,criterion='test')
        self.assertEqual((a['status'],a['first_hit_step']),('capped',None))
        b=k.stopping([2,.25],.5,1,criterion='test')
        self.assertEqual((b['status'],b['first_hit_step']),('converged',1))
        self.assertEqual(k.stopping([2,np.nan],.5,1,criterion='test')['status'],'nonfinite')

    def test_nonfinite_after_threshold_hit_preserves_hit_without_claiming_convergence(self):
        for values in ([2,.25,np.nan],[2,.25,np.inf],[2,.25,np.nan,.1]):
            with self.subTest(values=values):
                report=k.stopping(values,.5,len(values)-1,criterion='test')
                self.assertEqual(report['status'],'nonfinite')
                self.assertEqual(report['first_hit_step'],1)

    def test_fixed_point_last_iteration_convergence_and_censoring(self):
        _,a=k.fixed_point(np.zeros((1,1)),np.ones(1),max_iter=1)
        self.assertEqual(a['status'],'converged')
        _,b=k.fixed_point(np.array([[.9]]),np.array([.1]),tol=1e-15,max_iter=1)
        self.assertEqual(b['status'],'capped');self.assertGreater(b['residual'],b['tolerance'])

    def test_actual_quad_and_newton_controlled_caps_do_not_masquerade_as_success(self):
        out=c.compute_quad(descent_cap=1,escape_cap=0)
        self.assertTrue(all(x['status']=='capped' and x['first_hit_step'] is None for x in out['convergence']['escape']))
        self.assertEqual(out['esc'],[None]*12)
        out=c.compute_newton(gd_cap=0,newton_cap=0)
        self.assertEqual(out['convergence']['newton']['status'],'capped')
        self.assertIsNone(out['newton_steps']);self.assertFalse(out['reference']['stationary'])
        self.assertEqual(len(out['gd']),len(out['gd_path_steps']))

    def test_actual_newton_long_stride_keeps_final_error_and_iteration(self):
        # A negative synthetic stopping threshold disables early threshold hits;
        # only4001bounded iterations, rather than the200000default budget.
        out=c.compute_newton(gd_cap=4001,newton_cap=0,threshold=-1)
        self.assertEqual(out['gd_steps'],4001)
        self.assertEqual(out['gd_err_stride'],2)
        self.assertEqual(out['gd_err_steps'][-2:].tolist(),[4000,4001])
        self.assertEqual(len(out['gd_err']),len(out['gd_err_steps']))
        self.assertEqual(out['gd_path_steps'][-1],out['gd_err_steps'][-1])
        w=out['gd'][-1];X,y=out['X'],out['y']
        actual=float(np.logaddexp(0,-y*(X@w)).mean()+out['lam']/2*(w@w)-out['f_star'])
        self.assertAlmostEqual(out['gd_err'][-1],actual)

    def test_actual_optimizer_failure_survives_without_hoped_outcome_assertions(self):
        lag=c.compute_lagrange(solver_cap=1)
        self.assertFalse(lag['solvers']['dice']['success'])
        svm=c.compute_kkt(solver_cap=1,grid_x_count=41,grid_lambda_count=7)
        self.assertFalse(svm['solvers']['primal']['success'])
        self.assertFalse(svm['solvers']['dual']['success'])
        self.assertEqual(svm['grid']['x_count'],41)
        self.assertGreater(svm['residuals']['dual_equality'],0)

    def test_actual_tiny_train_reads_current_corpus_not_stale_part1_text_or_bigram(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td);(folder/'ai1').mkdir();(folder/'ai1/train.txt').write_text('abc abc abb ac ' * 10)
            (folder/'ai1/valid.txt').write_text('abc abb ')
            from videos.ai.ai1 import compute as c1
            with patch.object(c.CACHE,'dir',folder/'ai4'), patch.object(c1,'text',side_effect=AssertionError('memoized text used')), \
                    patch.object(c1,'load',side_effect=AssertionError('stale bigram used')):
                out=c.compute_train(steps=2,batch=8,snapshot_steps=(1,2))
            self.assertEqual(out['snap_steps'],[1,2])
            self.assertTrue(np.allclose(np.exp(out['snaps_logp']).sum(2),1))
            self.assertEqual(out['metrics']['curve_parameter_step'],'t-1')
            self.assertEqual(out['metrics']['snapshot_parameter_step'],'t')

    def test_actual_paired_precision_aggregate_markers_lie_on_plotted_curve(self):
        # Actual aggregation/selection, with a two-parameter deterministic loss.
        def net(dtype):
            return lambda x:float(np.exp(np.asarray(x,dtype=dtype)).sum()), np.exp, np.array([.2,.3])
        with patch.object(c,'_check_net',side_effect=net):out=c.compute_vcurve()
        self.assertTrue(np.allclose(np.linalg.norm(out['directions'],axis=1),1))
        for precision in ('fp32','fp64'):
            for method in ('central','forward'):
                marker=out['meas'][precision][method];i=np.flatnonzero(out['hs']==marker)[0]
                self.assertEqual(out[f'{method}_{precision}'][i],out['meas'][precision][method+'_err'])

    def test_actual_classifier_work_matches_executed_requested_gradient_pullbacks(self):
        import ast
        import copy
        source=ast.parse(Path(c.__file__).read_text())
        fn=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='compute_modes')
        start=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call)
                   and isinstance(n.value.func,ast.Name) and n.value.func.id=='rng' and isinstance(n.value.args[0],ast.Constant)
                   and n.value.args[0].value==21)
        tail=copy.deepcopy(fn.body[start:])
        dimensions=next(n for n in tail if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Tuple))
        dimensions.value=ast.Tuple(elts=[ast.Constant(v) for v in (2,3,4,2)],ctx=ast.Load())
        fixture=ast.FunctionDef(name='fixture',args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),
                               body=tail,decorator_list=[])
        ns=dict(vars(c));ns.update(sizes=[],H=4,fwd=[],rev=[],primal=[],t_fwd=[],t_rev=[],agree=0,lib_diff=0,timing_start=0,
                                  _timeit=lambda *a:0,benchmark_context=lambda:{})
        exec(compile(ast.fix_missing_locations(ast.Module(body=[fixture],type_ignores=[])),c.__file__,'exec'),ns)
        calls=[];original=c.Tensor._make
        def observed(tensor,data,parents,op):
            tracked=[]
            for parent,back in parents:
                cost=(parents[0][0].data.shape[0]*parents[0][0].data.shape[1]*parents[1][0].data.shape[1]) if op=='@' else (data.size if op=='tanh' else 0)
                def visit(g,back=back,cost=cost,op=op):
                    if cost:calls.append((op,cost))
                    return back(g)
                tracked.append((parent,visit))
            return original(tensor,data,tracked,op)
        with patch.object(c.Tensor,'_make',observed):out=ns['fixture']()
        self.assertEqual(sum(v for _,v in calls),out['madds_rev'])
        self.assertEqual(sum(op=='@' for op,v in calls),3)  # dW1, dH, dW2; no dX
        self.assertEqual(out['madds_fwd']/out['madds_rev'],out['P'])
        self.assertLess(out['grad_diff'],1e-12)

    def test_actual_deq_bounded_fixture_retains_all_capped_solve_counts(self):
        out=c.compute_deq(training_steps=0,solve_cap=1)
        self.assertEqual(out['parameter_count'],181)
        self.assertEqual(out['solves']['initial']['status'],'capped')
        self.assertEqual(out['solves']['training']['count'],48)
        for phase in ('training','fit'):
            report=out['solves'][phase]
            self.assertEqual(report['converged']+report['capped']+report['nonfinite'],report['count'])
            self.assertGreater(report['capped'],0)


if __name__=='__main__':unittest.main()
