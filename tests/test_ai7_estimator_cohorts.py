"""Tiny extracted estimator math only; never import Part7 producers or caches."""
import ast
import contextlib
import copy
import importlib.util
import io
import math
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'videos/ai/ai7/compute.py'
TREE = ast.parse(SOURCE.read_text())
NAMES = {'ngram_tables', 'kn_model', 'kn_bits', 'kn_probs', 'goodturing_cohort', 'continuation_examples'}
SCOPE = dict(np=np, math=math)
exec(compile(ast.Module([n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in NAMES], type_ignores=[]),
             'extracted-pure-ai7-estimators', 'exec'), SCOPE)
spec = importlib.util.spec_from_file_location('ai7_contracts_only', ROOT / 'videos/ai/ai7/contracts.py')
contracts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contracts)
TRAIN = np.array([0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,1], dtype=np.int64)
TEST = np.array([0,0,1,1,0,0,1,0], dtype=np.int64)


def comparison(valid, maximum=1, train=TRAIN):
    """Execute only the actual numerical body; no CACHE/read/producer is executed."""
    fn = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_kn')
    first = next(i for i,n in enumerate(fn.body) if isinstance(n, ast.If))
    last = next(i for i,n in enumerate(fn.body) if isinstance(n, ast.Assign)
                and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'raw')
    nodes = copy.deepcopy(fn.body[first:last])
    nodes.append(ast.Assign(targets=[ast.Name(id='result',ctx=ast.Store())], value=copy.deepcopy(fn.body[-1].value)))
    ns = dict(SCOPE, a=train, v=np.asarray(valid,dtype=np.int64), ps=TEST, K=2, MAXM=maximum,
              raw={'best_bits':2.,'rows':[{'test':2.}]})
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(ast.fix_missing_locations(ast.Module(nodes,type_ignores=[])), 'actual-kn-array-comparison-only', 'exec'), ns)
    return ns['result']


def words(frequent=False):
    a = [0]
    for r in range(1,9):
        a.extend([r,0] * r)
    if frequent:
        a.extend([8,9] * 1001)
    return np.array(a,dtype=np.int64)


def example(a,b,V):
    ka=np.unique(a[:-1]*V+a[1:]); kb=np.unique(b[:-1]*V+b[1:])
    return SCOPE['continuation_examples'](np.array(['w'+str(i) for i in range(V)]),a,b,ka,kb)


class EstimatorCohorts(unittest.TestCase):
    def test_common_suffix_changes_real_ranking_without_changing_natural_api(self):
        tables=SCOPE['ngram_tables'](TRAIN,2,1)
        models=[SCOPE['kn_model'](tables,2,m)for m in range(2)]
        natural=[SCOPE['kn_bits'](model,TEST,2,m)for m,model in enumerate(models)]
        common=[SCOPE['kn_bits'](model,TEST,2,m,start=1)for m,model in enumerate(models)]
        np.testing.assert_allclose(natural,[.9671322027689284,1.0075845184273813],rtol=0,atol=1e-14)
        np.testing.assert_allclose(common,[1.0280698915412463,1.0075845184273813],rtol=0,atol=1e-14)
        self.assertEqual(int(np.argmin(natural)),0);self.assertEqual(int(np.argmin(common)),1)
        for m,model in enumerate(models):
            np.testing.assert_array_equal(SCOPE['kn_probs'](model,TEST,2,m,start=1),SCOPE['kn_probs'](model,TEST,2,m)[1-m:])

    def test_actual_comparison_schema_keeps_matched_natural_score_separate(self):
        d=comparison(np.ones(8,dtype=np.int64))
        self.assertEqual(d['best'],0)
        self.assertEqual({(r['start'],r['valid_count'],r['test_count'])for r in d['rows']},{(1,7,7)})
        self.assertAlmostEqual(d['comparison_best_bits'],1.0280698915412463)
        self.assertAlmostEqual(d['best_bits'],.9671322027689284)
        self.assertEqual(d['selected_same_order']['start'],0)
        self.assertEqual(d['selected_same_order']['test_count'],8)
        self.assertTrue(contracts.valid_structure('kn',d))
        for mutation in ['row_count','same_order_start','best_bits','common_best']:
            bad=copy.deepcopy(d)
            if mutation=='row_count':bad['rows'][0]['test_count']+=1
            elif mutation=='same_order_start':bad['selected_same_order']['start']=1
            elif mutation=='best_bits':bad['best_bits']=bad['comparison_best_bits']
            else:bad['comparison_best_bits']+=.1
            self.assertFalse(contracts.valid_structure('kn',bad),mutation)

    def test_nonempty_targets_and_history_requirements_fail_explicitly(self):
        model=SCOPE['kn_model'](SCOPE['ngram_tables'](TRAIN,2,1),2,1)
        for start in [0,8,-1,True,1.5]:
            with self.assertRaises(ValueError):SCOPE['kn_bits'](model,TEST,2,1,start=start)
        with self.assertRaises(ValueError):comparison(np.ones(1,dtype=np.int64))
        with self.assertRaises(ValueError):comparison(TEST,maximum=3,train=np.array([0,1],dtype=np.int64))
        with self.assertRaises(ValueError):SCOPE['kn_bits'](model,np.ones(1,dtype=np.int64),2,1)

    def test_goodturing_uses_bigram_trials_and_allows_zero_held_unseen(self):
        a=words();d,ka,kb=SCOPE['goodturing_cohort'](a,a,10)
        self.assertEqual(d['bigram_trials_a'],72);self.assertEqual(d['bigram_trials_b'],72)
        self.assertEqual(d['singleton_types'],2);self.assertAlmostEqual(d['p_unseen'],2/72)
        self.assertNotAlmostEqual(d['p_unseen'],2/73)
        self.assertEqual(d['rows'][0]['held'],0.)
        self.assertTrue(all(np.isfinite(r[k])for r in d['rows']for k in ['Nr','gt','held']))
        b=np.array([0,9,0,9],dtype=np.int64)
        other,_,_=SCOPE['goodturing_cohort'](a,b,10)
        self.assertEqual(other['bigram_trials_b'],3)
        self.assertGreater(other['rows'][0]['held'],0)

    def test_unsupported_raw_and_example_cohorts_never_make_nan_or_fake_contrast(self):
        a=words()
        for x,y,V in [(np.array([],dtype=int),a,10),(np.array([0]),a,10),
                      (np.array([0,0]),np.array([0,0]),1),(np.array([0,0,0,0,1]),a,10),
                      (np.array([0,0,1,1,0]),np.array([0,1]),2)]:
            with self.assertRaises(ValueError):SCOPE['goodturing_cohort'](x,y,V)
        with self.assertRaisesRegex(ValueError,'1000'):example(a,a,10)
        mono=np.array([0]*1100+[1],dtype=np.int64)
        with self.assertRaisesRegex(ValueError,'distinct'):example(mono,mono,2)
        tied=np.tile(np.array([0,1],dtype=np.int64),600)
        d=example(tied,tied,2)
        self.assertNotEqual(d['word'],d['other'])
        self.assertEqual(d['word_prev'],d['other_prev'])  # valid even without hoped-for improvement

    def test_goodturing_contract_binds_denominator_and_distinct_actual_examples(self):
        a=words(frequent=True);d,ka,kb=SCOPE['goodturing_cohort'](a,a,10)
        d.update(V=10,tokens=2*len(a),**example(a,a,10))
        self.assertTrue(contracts.valid_structure('goodturing',d))
        for key,value in [('p_unseen',d['singleton_types']/(d['bigram_trials_a']+1)),
                          ('bigram_trials_a',d['bigram_trials_a']+1),('other',d['word'])]:
            bad=copy.deepcopy(d);bad[key]=value
            self.assertFalse(contracts.valid_structure('goodturing',bad),key)


if __name__=='__main__':unittest.main()
