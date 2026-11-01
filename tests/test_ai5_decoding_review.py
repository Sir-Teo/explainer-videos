"""Tiny actual-helper tests; no scenes, production loaders, networks or trained models."""
import ast
import json
import math
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import torch

from videos.ai.ai5 import decoding_contract as dc

ROOT = Path(__file__).resolve().parents[1]


def verdict(result, spoken):
    tree=ast.parse((ROOT/"videos/ai/ai5/s11_decoding.py").read_text())
    n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="comparison_verdict")
    env={};exec(compile(ast.Module([n],type_ignores=[]),"actual-scene-verdict","exec"),env)
    return env["comparison_verdict"](result,spoken)


def decoder_helpers():
    tree = ast.parse((ROOT / 'videos/ai/ai5/decoding.py').read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.Assign, ast.FunctionDef))]
    env = dict(math=math, np=np, Path=Path, contract=dc)
    exec(compile(ast.Module(nodes, type_ignores=[]), 'actual-decoding-helpers', 'exec'), env)
    return env


class Tokens:
    def __init__(self, texts): self.texts, self.calls = texts, []
    def __call__(self, text, **kw):
        assert kw == {'add_special_tokens': False}
        self.calls.append(text)
        return {'input_ids': self.texts[text]}


class Judge:
    def __init__(self, context=16, nonfinite=False):
        self.config = SimpleNamespace(n_positions=context)
        self.calls = []
        self.nonfinite = nonfinite
    def __call__(self, ids):
        self.calls.append(ids.tolist())
        p = torch.tensor([.2, .5, .3], dtype=torch.float64)
        z = p.log().repeat(1, ids.shape[1], 1)
        if self.nonfinite: z[:] = float('nan')
        return SimpleNamespace(logits=z)


class JudgeBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.fn = staticmethod(decoder_helpers()['judge'])

    def test_cross_boundary_merge_never_retokenizes_prompt(self):
        tok=Tokens({'a':[0], 'b':[1,2], 'ab':[2]}); model=Judge()
        out=self.fn(tok,model,['a'],['b'])
        self.assertEqual(tok.calls,['a','b'])
        self.assertEqual(model.calls,[[[0,1,2]]])
        self.assertAlmostEqual(out[0][0],-math.log(.5)-math.log(.3))
        self.assertEqual(out[0][1],1)

    def test_counts_true_unicode_continuation_not_decoded_tokens(self):
        out=self.fn(Tokens({'prompt':[0,1],'é🙂':[2]}),Judge(),['prompt'],['é🙂'])
        self.assertEqual(out[0][1],2)
        self.assertAlmostEqual(out[0][0],-math.log(.3))

    def test_empty_or_tokenless_examples_rejected_before_model(self):
        for a,b,pa,cb in [('', 'b',[],[1]),('a','',[0],[]),('a','b',[],[1]),('a','b',[0],[])]:
            model=Judge()
            with self.subTest(a=a,b=b,pa=pa,cb=cb), self.assertRaises(ValueError):
                self.fn(Tokens({a:pa,b:cb}),model,[a],[b])
            self.assertFalse(model.calls)

    def test_no_silent_truncation(self):
        model=Judge(context=3)
        with self.assertRaisesRegex(ValueError,'no continuation was truncated'):
            self.fn(Tokens({'a':[0,1],'b':[1,2]}),model,['a'],['b'])
        self.assertFalse(model.calls)

    def test_exact_context_boundary_and_cohort_size(self):
        out=self.fn(Tokens({'a':[0,1],'b':[2]}),Judge(context=3),['a'],['b'])
        self.assertAlmostEqual(out[0][0],-math.log(.3))
        with self.assertRaisesRegex(ValueError,'cohorts differ'):
            self.fn(Tokens({}),Judge(),['a'],[])

    def test_nonfinite_judge_rejected(self):
        with self.assertRaisesRegex(ValueError,'Nonfinite'):
            self.fn(Tokens({'a':[0],'b':[1]}),Judge(nonfinite=True),['a'],['b'])


class IdentityAndResumeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.hub=self.root/'hub'
        self.config=decoder_helpers()['configuration']()
        names=['.cache/novels/base.pt','.cache/novels/base.json','.cache/novels/tokenizer.json',
               '.cache/novels/train.npy','.cache/novels/valid.npy','.cache/ai1/train.txt','.cache/ai1/valid.txt',
               'videos/ai/ai5/decoding.py','videos/ai/ai5/decoding_contract.py','explainer/ai/novels.py','explainer/lm/pocket.py']
        for name in names:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('tiny fixture '+name)
        base=dict(steps=2929,diverged=False,run=dict(model=dict(d=256,layers=6,heads=8,seq=256,vocab=4096),tokens=24000000,batch=32))
        (self.root/'.cache/novels/base.json').write_text(json.dumps(base))
        snap=dc.snapshot_dir(self.hub);snap.mkdir(parents=True)
        for name in dc.GPT2_FILES:(snap/name).write_text('tiny pinned fixture '+name)

    def identity(self):
        with patch.object(dc,'version',return_value='test-version'):
            return dc.cache_identity(self.root,self.config,self.hub)

    def test_identity_changes_for_each_asset_configuration_runtime(self):
        original=self.identity()
        for name in ('.cache/novels/base.pt','.cache/novels/tokenizer.json','.cache/novels/valid.npy',
                     '.cache/ai1/valid.txt','videos/ai/ai5/decoding.py','explainer/lm/pocket.py'):
            p=self.root/name;raw=p.read_bytes();p.write_bytes(raw+b'changed')
            self.assertNotEqual(self.identity(),original,name);p.write_bytes(raw)
        p=dc.snapshot_dir(self.hub)/'model.safetensors';p.write_text('new weights')
        self.assertNotEqual(self.identity(),original)
        with patch.object(dc,'version',return_value='new-version'):
            self.assertNotEqual(dc.cache_identity(self.root,self.config,self.hub)['runtime'],original['runtime'])
        self.config['prompt_len']+=1
        self.assertNotEqual(self.identity()['config'],original['config'])

    def test_missing_file_and_incomplete_base_fail_without_rebuild(self):
        p=dc.snapshot_dir(self.hub)/'tokenizer.json';p.unlink()
        with self.assertRaisesRegex(FileNotFoundError,'prerequisite missing'): self.identity()
        p.write_text('replacement')
        b=self.root/'.cache/novels/base.json';value=json.loads(b.read_text());value['steps']=100;b.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError,'2929-step'):self.identity()

    def test_temperature_identity_does_not_need_novels(self):
        (self.root/'.cache/novels/base.pt').unlink()
        self.assertEqual(dc.judge_identity(self.hub)['revision'],dc.GPT2_REVISION)

    def test_selected_prompt_ids_and_text_both_bound(self):
        h=dc.prompt_identity([[1,2]],['abc'])
        self.assertNotEqual(h,dc.prompt_identity([[1,3]],['abc']))
        self.assertNotEqual(h,dc.prompt_identity([[1,2]],['abd']))

    def partial(self,data,contract):
        path=self.root/'decoding.partial.json';path.write_text(json.dumps(data))
        # Actual generic Partial only, no repository import / implicit loader.
        tree=ast.parse((ROOT/'explainer/ai/cache.py').read_text())
        node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Partial')
        env=dict(json=json,Path=Path);exec(compile(ast.Module([node],type_ignores=[]),'actual-partial', 'exec'),env)
        cache=SimpleNamespace(dir=self.root,partial=lambda name,params:env['Partial'](path,params))
        return dc.checked_partial(cache,contract,['temp0.5'],12),path

    @staticmethod
    def piece():return dict(nll=1.,rep=.1,div=.8,kept=3,nll_prompt=[1.]*12,examples=['text'],ex_prompt=['other'])

    def test_good_partial_reused_exactly(self):
        p,path=self.partial(dict(params={'version':3},done={'temp0.5':self.piece()}),{'version':3})
        self.assertEqual(p['temp0.5'],self.piece());self.assertTrue(path.exists())
        self.assertFalse(list(self.root.glob('*.stale-*')))

    def test_legacy_or_changed_identity_preserved_not_reused(self):
        for old in ({'v':2},{'version':3,'model':'OLD'}):
            data=dict(params=old,done={'temp0.5':self.piece()});raw=json.dumps(data).encode()
            p,path=self.partial(data,{'version':3,'model':'NEW'})
            self.assertNotIn('temp0.5',p);self.assertFalse(path.exists())
            self.assertTrue(any(q.read_bytes()==raw for q in self.root.glob('*.stale-*')))

    def test_nonfinite_missing_or_unknown_partial_preserved(self):
        for key,value in [('temp0.5',dict(self.piece(),nll=float('nan'))),('temp0.5',dict(self.piece(),nll_prompt=[1.])),('unknown',self.piece())]:
            p,path=self.partial(dict(params={'v':3},done={key:value}),{'v':3})
            self.assertNotIn(key,p);self.assertFalse(path.exists())


class PromptAndComparisonTests(unittest.TestCase):
    def test_footer_reports_mean_standard_error_not_passage_spread(self):
        tree=ast.parse((ROOT/'videos/ai/ai5/s11_decoding.py').read_text())
        assignment=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign)
                        and any(isinstance(t,ast.Name) and t.id=='mean_se' for t in n.targets))
        # Sample variance of 0,...,11 is13; doubling values quadruples variance.
        d={'settings':['first','second'],'first':{'nll_prompt':list(range(12))},
           'second':{'nll_prompt':[2*x for x in range(12)]}}
        actual=eval(compile(ast.Expression(assignment.value),'actual-setting-mean-se','eval'),
                    {'np':np,'math':math},{'d':d})
        expected=1.5*math.sqrt(13/12)
        self.assertAlmostEqual(actual,expected)
        self.assertNotAlmostEqual(actual,1.5*math.sqrt(13))
        caption=next(n.args[0] for n in ast.walk(tree) if isinstance(n,ast.Call)
                     and isinstance(n.func,ast.Name) and n.func.id=='note'
                     and n.args and 'standard error' in ast.unparse(n.args[0]))
        text=eval(compile(ast.Expression(caption),'actual-se-caption','eval'),{}, {'mean_se':actual})
        self.assertIn('mean standard error of setting means',text)
        self.assertIn('not passage SD or CI',text)
        self.assertIn('nats/character',text)
        self.assertNotIn(r'\pm',text)

    def test_topk_ties_keep_exact_budget_and_other_filters_normalize(self):
        fn=decoder_helpers()['filter_probs']
        p=torch.tensor([[.4,.2,.2,.2]],dtype=torch.float64)
        q=fn(p,'topk',2)
        self.assertEqual(int((q>0).sum()),2)
        self.assertAlmostEqual(float(q.sum()),1.)
        for kind,v in [('topp',.5),('minp',.75),('temp',1.)]:
            q=fn(p,kind,v)
            self.assertAlmostEqual(float(q.sum()),1.)
            self.assertTrue(torch.isfinite(q).all())

    def test_prompt_selection_terminates_insufficient_candidates(self):
        fn=decoder_helpers()['prompts']
        tok=SimpleNamespace(get_vocab_size=lambda:3,decode=lambda ids,**kw:'\n' if ids==[0] else 'x',token_to_id=lambda s:2)
        with self.assertRaisesRegex(ValueError,'too short'):fn(np.ones(10,dtype=np.uint16),tok)
        with self.assertRaisesRegex(ValueError,'Only 0 admissible'):fn(np.ones(1000,dtype=np.uint16),tok)

    def test_prompt_selection_reproducible_and_full_length(self):
        fn=decoder_helpers()['prompts']
        tok=SimpleNamespace(get_vocab_size=lambda:3,decode=lambda ids,**kw:'\n' if ids==[0] else 'x',token_to_id=lambda s:2)
        valid=np.ones(2000,dtype=np.uint16);valid[::100]=0
        a=fn(valid,tok);b=fn(valid,tok)
        np.testing.assert_array_equal(a,b);self.assertEqual(a.shape,(12,72))

    def test_sixteen_settings_and_unequal_greedy_cohort(self):
        c=decoder_helpers()['configuration']()
        self.assertEqual(len(c['settings']),16);self.assertEqual(c['greedy_samples'],1);self.assertEqual(c['samples'],8)
        self.assertEqual(12*(1+15*8)*40,58080)

    def test_partial_common_range_is_not_four_rule_winner(self):
        rows=[('a',dict(div=.8,nll=1.)),('a',dict(div=.9,nll=2.)),('b',dict(div=.4,nll=.5)),('b',dict(div=.5,nll=.6))]
        r=dc.comparison(rows,['a','b']);self.assertEqual(set(r['at']),{'a'})
        text=verdict(r,{'a':'A','b':'B'})
        self.assertIn('Only 1',text);self.assertIn('cannot establish a winner',text)

    def test_no_common_range_and_nonfinite_failures(self):
        r=dc.comparison([('a',dict(div=.2,nll=1.)),('a',dict(div=.3,nll=2.))],['a'])
        self.assertIn('no interpolation',verdict(r,{'a':'A'}))
        with self.assertRaises(ValueError):dc.comparison([('a',dict(div=.8,nll=float('nan')))],['a'])

    def test_actual_interpolation_and_verdict_branches(self):
        rows=[(k,dict(div=x,nll=y)) for k,ys in [('a',(1.,2.)),('b',(.5,1.))] for x,y in zip((.8,.9),ys)]
        r=dc.comparison(rows,['a','b']);self.assertAlmostEqual(r['at']['a'],1.5);self.assertEqual(r['best'],'b')
        self.assertIn('B has the lowest',verdict(r,{'a':'A','b':'B'}))
        self.assertIn('lowest surprise',dc.judge_verdict(.2,[.3,.4]))
        self.assertIn('ties',dc.judge_verdict(.3,[.3,.4]))
        self.assertIn('sampled setting',dc.judge_verdict(.5,[.3,.4]))
        with self.assertRaises(ValueError):dc.judge_verdict(float('nan'),[.2])


if __name__=='__main__':unittest.main()
