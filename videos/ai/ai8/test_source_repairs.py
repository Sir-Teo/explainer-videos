"""Synthetic source/guard checks. No scene, scientific producer or model imports."""
from __future__ import annotations

import ast
from contextlib import nullcontext
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
PART = ROOT / 'videos/ai/ai8'
BASE = '3cfc87e211ba1b56d133f9b8e57a8f739b4e10bb'


def tree(name, baseline=False):
    relative = 'videos/ai/ai8/' + name
    source = subprocess.check_output(['git', 'show', BASE + ':' + relative], cwd=ROOT, text=True) if baseline else (PART/name).read_text()
    return ast.parse(source)


def method(name, cls, function):
    owner = next(n for n in tree(name).body if isinstance(n, ast.ClassDef) and n.name == cls)
    return next(n for n in owner.body if isinstance(n, ast.FunctionDef) and n.name == function)


def wrapper():
    # This entry point deliberately imports standard-library modules only.
    spec = importlib.util.spec_from_file_location('ai8_qa_cached_test', PART/'qa_cached.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceRepairs(unittest.TestCase):
    def test_narration_bookmarks_and_timed_calls_remain_exact(self):
        for name in ['s01_hook.py', 's09_stability.py', 's12_maxmargin.py', 's17_shift.py']:
            with self.subTest(name=name):
                def signature(t):
                    spoken, waits, timing = [], [], []
                    for n in ast.walk(t):
                        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute):
                            continue
                        if n.func.attr == 'voiceover': spoken.append(ast.dump(n.args[0]))
                        if n.func.attr in ('wait_until', 'wait'): waits.append(ast.dump(n))
                        if n.func.attr == 'play': timing.append([ast.dump(k) for k in n.keywords])
                    return spoken, waits, timing
                self.assertEqual(signature(tree(name, True)), signature(tree(name)))

    def test_proof_has_visible_context_before_voiceover(self):
        m = method('s12_maxmargin.py', 'MaxMargin', 'why')
        before = m.body[:next(i for i,n in enumerate(m.body) if isinstance(n,ast.With))]
        added = [n.value.args[0].id for n in before if isinstance(n,ast.Expr)
                 and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute)
                 and n.value.func.attr=='add' and isinstance(n.value.args[0],ast.Name)]
        self.assertIn('head', added)
        self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
                             and n.func.attr in ('play','wait') for statement in before for n in ast.walk(statement)))

    def test_sensitivity_caveat_matches_producer_statistic_and_is_shown(self):
        m = method('s09_stability.py', 'Stability', 'stability')
        texts = [n.value for n in ast.walk(m) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        caveat = next(t for t in texts if t.startswith('Empirical illustration:'))
        for phrase in ['$60$ sampled swaps','largest prediction change','observed pages','then average',
                       'does not measure uniform loss stability']:
            self.assertIn(phrase,caveat)
        self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='FadeIn'
                            and isinstance(n.args[0],ast.Name) and n.args[0].id=='empirical' for n in ast.walk(m)))
        table = json.loads((PART/'text_zh_add.json').read_text())['strings']
        self.assertIn(caveat,table)
        self.assertIn('一致损失稳定性',table[caveat])

    def test_new_caption_keywords_match_actual_shared_helper_signature(self):
        shared=ast.parse((ROOT/'explainer/analysis/__init__.py').read_text())
        helper=next(n for n in shared.body if isinstance(n,ast.FunctionDef) and n.name=='wrapped_label')
        accepted={a.arg for a in helper.args.args+helper.args.kwonlyargs}
        calls=[n for n in ast.walk(method('s09_stability.py','Stability','stability'))
               if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='wrapped_label']
        self.assertTrue(calls)
        for call in calls:self.assertFalse({k.arg for k in call.keywords}-accepted)

    def test_both_density_functions_preserve_gaussian_ratio_under_same_affine_scale(self):
        m = method('s17_shift.py', 'Shift', 'picture')
        expressions = {}
        for n in m.body:
            if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('dtr','dte'):
                expressions[n.targets[0].id] = n.value.args[0]
        # Synthetic points and a standard-library normal PDF test the actual
        # source lambdas without importing the scene or reading experiment data.
        normal = SimpleNamespace(pdf=lambda x,mu,sd: math.exp(-.5*((x-mu)/sd)**2)/(sd*math.sqrt(2*math.pi)))
        params = {'mu_tr':.5,'sd_tr':.5,'mu_te':0.,'sd_te':.3}
        fs = {k:eval(compile(ast.Expression(v),'<source-density>','eval'),{'norm':normal,'s':params}) for k,v in expressions.items()}
        for x in [-.8,0.,.5,1.]:
            p,q=normal.pdf(x,.5,.5),normal.pdf(x,0.,.3)
            self.assertAlmostEqual((fs['dte'](x)+1.2)/(fs['dtr'](x)+1.2),q/p,places=10)
        self.assertAlmostEqual(fs['dtr'](.5),-1.2+.55*normal.pdf(.5,.5,.5))


class CachedOnlyHarness(unittest.TestCase):
    def test_cli_always_propagates_both_guards_and_silent_backend(self):
        module = wrapper()
        with mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'0','EXPLAINER_TTS':'kokoro'}), \
             mock.patch.object(module.subprocess,'run',return_value=SimpleNamespace(returncode=17)) as run:
            self.assertEqual(module.main(['--only','Hook','--lang','en']),17)
        command = run.call_args.args[0];env=run.call_args.kwargs['env']
        self.assertIn('--cached-only',command)
        self.assertEqual(command[2],'ai8')
        self.assertEqual(env['EXPLAINER_CACHED_ONLY'],'1')
        self.assertEqual(env['EXPLAINER_TTS'],'silent')
        self.assertTrue(all(env[k]=='1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']))

    def test_missing_explicit_scope_or_unknown_passthrough_never_launches(self):
        module=wrapper()
        for argv in [['--lang','en'],['--only','Hook','--lang','en','--force'],
                     ['--only','Hook','--lang','en','--timeout','0']]:
            with self.subTest(argv=argv),mock.patch.object(module.subprocess,'run') as run:
                with self.assertRaises(SystemExit):module.main(argv)
                run.assert_not_called()

    def test_upstream_actual_schema_loader_fails_before_import_produce_lock_or_write(self):
        # Compile only the real guard and SchemaCache.load method, with tiny
        # cache-state stubs. No project module or scientific producer is imported.
        src=ast.parse((ROOT/'videos/ai/ai6/cache_contract.py').read_text())
        guard=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='cached_only')
        owner=next(n for n in src.body if isinstance(n,ast.ClassDef) and n.name=='SchemaCache')
        load=next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='load')
        error=type('CacheValidationError',(ValueError,),{})
        lock=mock.Mock(side_effect=AssertionError('cache lock/write boundary reached'))
        imports=mock.Mock(side_effect=AssertionError('producer import reached'))
        base=type('SyntheticBase',(),{'load':lambda self,name: {'synthetic_current':True}})
        namespace={'os':os,'REQUIRED':{'pages'},'CacheValidationError':error,'cache_lock':lock,
                   'importlib':SimpleNamespace(import_module=imports),'SyntheticBase':base}
        node=ast.ClassDef(name='SchemaCache',bases=[ast.Name(id='SyntheticBase',ctx=ast.Load())],keywords=[],body=[load],decorator_list=[])
        exec(compile(ast.fix_missing_locations(ast.Module(body=[guard,node],type_ignores=[])),'<actual-ai6-loader>','exec'),namespace)
        module=wrapper()
        with tempfile.TemporaryDirectory(prefix='ai8-synthetic-cache-') as temp:
            marker=Path(temp)/'pages.json';marker.write_text('{"synthetic":"untouched"}\n');before=marker.read_bytes()
            for state in ['missing','legacy','stale','malformed']:
                cache=namespace['SchemaCache']();cache.status=lambda name,state=state: {'status':state,'reason':'synthetic fixture'}
                cache._produce=mock.Mock(side_effect=AssertionError('producer reached'))
                def child(command,**kw):
                    self.assertIn('--cached-only',command)
                    with mock.patch.dict(os.environ,kw['env']):
                        with self.assertRaisesRegex(error,state):cache.load('pages')
                    return SimpleNamespace(returncode=1)
                with self.subTest(state=state),mock.patch.dict(os.environ,{'EXPLAINER_CACHED_ONLY':'0'}), \
                     mock.patch.object(module.subprocess,'run',side_effect=child):
                    self.assertEqual(module.main(['--only','RandomLabels','--lang','en']),1)
                cache._produce.assert_not_called();imports.assert_not_called();lock.assert_not_called()
                self.assertEqual(marker.read_bytes(),before);self.assertEqual(list(Path(temp).iterdir()),[marker])


if __name__=='__main__':unittest.main()
