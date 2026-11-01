"""Small mathematical/branch references for Part7; no production cache or scene execution."""
import ast
import contextlib
import io
import math
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai7 import compute

SCENES = Path(__file__).resolve().parents[1] / 'videos/ai/ai7'


def scene_function(filename, name):
    tree = ast.parse((SCENES / filename).read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace = {'np': np}
    exec(compile(ast.Module(body=[function], type_ignores=[]), filename, 'exec'), namespace)
    return namespace[name]


class LatentSceneBranches(unittest.TestCase):
    def test_ppca_validation_comparisons_do_not_infer_signal(self):
        verdict = scene_function('s03_ppca.py', 'ppca_verdict')
        for score, full, word in [(-92.,-93.,'higher than'),(-94.,-93.,'lower than'),
                                  (-93.,-93.,'equal at the shown precision to'),
                                  (-93.+1e-9,-93.,'equal at the shown precision to')]:
            with self.subTest(score=score,full=full):
                text = verdict(2,score,full)
                self.assertIn(word,text)
                self.assertIn('not a fresh test',text)
                self.assertIn('does not identify',text)
                self.assertNotIn('mostly noise',text)
                self.assertNotIn('every direction carries',text)

    def test_kmeans_has_win_loss_and_displayed_tie(self):
        verdict = scene_function('s05_em.py', 'kmeans_verdict')
        for own, other, word in [(.98,.97,'higher than'),(.95,.97,'lower than'),
                                 (.97,.97,'equal at the shown precision to')]:
            with self.subTest(own=own):
                text = verdict(own,other)
                self.assertIn(word,text)
                self.assertIn('not a general ranking',text)

    def test_bound_replay_uses_only_completed_explicit_rounds(self):
        prefix = scene_function('s06_lda.py', 'bound_prefix')
        rounds = np.array([0,2,5])
        bounds = np.array([-10.,-8.,-7.])
        for current, expected in [(0,[0]),(1.999,[0]),(2,[0,2]),(5,[0,2,5])]:
            x,y=prefix(rounds,bounds,current)
            self.assertEqual(x.tolist(),expected)
            np.testing.assert_equal(y,bounds[:len(expected)])
        with self.assertRaises(ValueError):
            prefix(rounds,bounds[:-1],1)


class LatentNumericalReferences(unittest.TestCase):
    def test_covariance_floor_preserves_likelihood_at_constrained_optimum(self):
        points=np.array([[-.001,-.001],[-.001,.001],[.001,-.001],[.001,.001]])
        covariance=points.T@points/len(points)
        ll=float(compute.gauss_logpdf(points,0,covariance).mean())
        ridge_ll=float(compute.gauss_logpdf(points,0,covariance+1e-6*np.eye(2)).mean())
        self.assertLess(ridge_ll,ll-.19)
        floor=compute.covariance_mle(covariance)
        np.testing.assert_allclose(floor,covariance,rtol=0,atol=1e-20)
        self.assertAlmostEqual(float(compute.gauss_logpdf(points,0,floor).mean()),ll,places=12)

    def test_covariance_floor_rotates_with_scatter_and_only_changes_small_eigenvalue(self):
        angle=.4
        U=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
        scatter=U@np.diag([1e-9,.3])@U.T
        expected=U@np.diag([compute.GMM_MIN_VARIANCE,.3])@U.T
        np.testing.assert_allclose(compute.covariance_mle(scatter),expected,atol=1e-15)

    def test_baselines_cannot_credit_one_source_twice(self):
        S=np.array([[1.,-1.,1.,-1.],[1.,1.,-1.,-1.]])
        X=np.array([[1.,.2],[1.,.3]])@S
        R=np.corrcoef(X,S)[:2,2:]
        self.assertEqual(np.abs(R).argmax(1).tolist(),[0,0])
        result=compute.bijective_correlations(R)
        pairs=[np.abs(R)[[0,1],p]for p in ([0,1],[1,0])]
        expected=max(pairs,key=np.sum)
        np.testing.assert_allclose(result,expected)
        self.assertLess(result.min(),.3)

    def test_selected_variance_percentage_comes_from_training_covariance(self):
        base=np.vstack([np.eye(3),-np.eye(3)])*np.sqrt(3)
        train=base@np.linalg.cholesky(np.array([[1.,.8,0],[.8,1.,0],[0,0,1.]])).T
        valid=base@np.linalg.cholesky(np.array([[1.,.5,0],[.5,1.,0],[0,0,1.]])).T
        X=np.vstack([train,valid]); mask=np.array([False]*6+[True]*6)
        with patch.object(compute,'pages',return_value=(X,np.zeros(12),None,['the','not','and'])), \
             patch.object(compute.CACHE,'read_pages',return_value={'test':mask}), \
             patch('videos.ai.ai6.compute.load',side_effect=AssertionError('No legacy external cache reads in this test')):
            result=compute.compute_pca2()
        k=result['best_k']
        self.assertGreater(k,0)
        z=(train-train.mean(0))/train.std(0)
        values=np.linalg.eigvalsh(z.T@z/len(z))[::-1]
        expected=values[:k].sum()/values.sum()
        self.assertAlmostEqual(result['training_share_best'],expected,places=12)
        self.assertGreater(abs(result['share_best']-expected),.01)

    def test_one_topic_final_bound_is_scored_after_the_same_m_step(self):
        # K=1 makes q(z)=1 and q(theta) a point, so the bound is independently
        # sum(counts*log(beta))/N. Only a four-document synthetic corpus is used.
        counts=np.array([[8.,2.],[7.,3.],[1.,9.],[2.,8.]])
        di=np.repeat(np.arange(4),2); wi=np.tile(np.arange(2),4)
        corpus=(di,wi,counts.ravel(),['red','blue'],np.array([1,1,2,2]),
                [['red','blue']*5]*4,{'red':0,'blue':1},0)
        book=SimpleNamespace(BOOKS={1:'synthetic A',2:'synthetic B'})
        # The teaching producer's later two-topic exemplar assumes K>=2. Check
        # its exact numerical prefix, stopping before that unrelated selector.
        tree=ast.parse((SCENES/'compute.py').read_text())
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='compute_lda')
        stop=next(i for i,n in enumerate(function.body)if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name)and t.id=='theta'for t in n.targets))
        function.body=function.body[:stop]+ast.parse("return {'bounds': bounds, 'bound_rounds': list(range(LDA_ITERS+1))}").body
        ast.fix_missing_locations(function)
        ns=dict(compute.__dict__,LDA_K=1,LDA_ITERS=2,LDA_INNER=2,lda_corpus=lambda:corpus)
        exec(compile(ast.Module(body=[function],type_ignores=[]),'exact-LDA-prefix','exec'),ns)
        with contextlib.redirect_stdout(io.StringIO()):
            result=ns['compute_lda']()
        beta=counts.sum(0)+compute.LDA_ETA;beta/=beta.sum()
        expected=float(counts.sum(0)@np.log(beta)/counts.sum())
        self.assertEqual(result['bound_rounds'],[0,1,2])
        self.assertEqual(len(result['bounds']),3)
        self.assertAlmostEqual(result['bounds'][1],expected,places=12)
        self.assertAlmostEqual(result['bounds'][2],expected,places=12)


if __name__=='__main__':
    unittest.main()
