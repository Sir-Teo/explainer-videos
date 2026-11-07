"""Independent numerical checks for Part 23's revised demonstrations."""
import unittest
import numpy as np
from scipy import stats
from explainer.stats.kit import ols as O
from videos.stats.stats23 import compute as C


class Part23Polish(unittest.TestCase):
    def test_cluster_sufficient_statistics_match_explicit_refits(self):
        g = np.random.default_rng(103)
        groups = np.repeat(np.arange(8), [4, 7, 9, 5, 6, 3, 8, 10])
        X = O.design(g.normal(size=len(groups)), g.normal(size=len(groups)))
        y = X @ [1., 2., -.3] + g.normal(size=len(groups))
        for weights in ('webb', 'rademacher'):
            with self.subTest(weights=weights):
                out = C.wild_cluster_boot(X, y, groups, 1, 1.7, 99, weights, np.random.default_rng(4))
                # Deliberately use the full observation-level refitting algorithm.
                f = O.fit(X, y)
                er = O.fit(np.delete(X, 1, axis=1), y - 1.7 * X[:, 1]).resid
                base = y - er
                ref = []
                draws = np.random.default_rng(4)
                for _ in range(99):
                    w = draws.choice(O.WEBB if weights == 'webb' else [-1., 1.], 8)
                    ff = O.fit(X, base + w[groups] * er)
                    ref.append((ff.coef[1] - 1.7) / np.sqrt(O.cluster_cov(ff, groups)[1, 1]))
                np.testing.assert_allclose(out['t_boot'], ref, rtol=2e-11, atol=2e-11)
                self.assertEqual(out['p'], (1 + np.count_nonzero((np.abs(ref) >= abs(out['t'])) | np.isclose(np.abs(ref), abs(out['t']), rtol=1e-12, atol=1e-12))) / 100)
                self.assertGreater(out['p'], 0)

    def test_bootstrap_rejects_degenerate_design_and_invalid_weights(self):
        X = O.design(np.arange(8))
        for kwargs in ({'groups': np.zeros(8)}, {'groups': np.arange(8), 'weights': 'typo'},
                       {'groups': np.arange(8), 'R': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                C.wild_cluster_boot(X, np.arange(8) ** 2, j=1, **kwargs)
        with self.assertRaises(ValueError):
            C.wild_cluster_boot(np.ones((8, 2)), np.arange(8), np.arange(8), 1)

    def test_quantile_meat_uses_empirical_scores(self):
        g = np.random.default_rng(24)
        X = O.design(g.uniform(-2, 2, 800))
        y = X[:, 1] ** 2 + g.normal(size=len(X))
        b, tau = np.array([.5, .2]), .2
        r = y - X @ b
        q, z = stats.norm.ppf(tau), stats.norm.ppf(.975)
        hs = len(y) ** (-1/3) * z ** (2/3) * (1.5 * stats.norm.pdf(q)**2 / (2*q*q+1)) ** (1/3)
        h = (stats.norm.ppf(min(tau+hs,.999)) - stats.norm.ppf(max(tau-hs,.001))) * min(r.std(), stats.iqr(r)/1.34)
        bread = sum(np.outer(x,x) / (2*h) for x,e in zip(X,r) if abs(e)<=h)
        meat = sum(np.outer(x,x) * (tau-int(e<0))**2 for x,e in zip(X,r))
        inv = np.linalg.inv(bread)
        np.testing.assert_allclose(C.qreg_score_se(X,y,tau,b), np.sqrt(np.diag(inv@meat@inv)), rtol=1e-12)

    def test_reference_solves_rounded_ill_conditioned_inputs(self):
        g = np.random.default_rng(65)
        U = np.linalg.qr(g.normal(size=(20, 3)))[0]
        V = np.linalg.qr(g.normal(size=(3, 3)))[0]
        X = U @ np.diag([1, 1e-5, 1e-10]) @ V.T
        y = X @ np.ones(3) + 1e-3 * g.normal(size=20)
        ref = C.precise_least_squares(X,y)
        # This independent SVD answer is useful only at the attainable accuracy.
        np.testing.assert_allclose(np.linalg.lstsq(X,y,rcond=None)[0], ref, rtol=5e-6)
        self.assertGreater(np.linalg.norm(ref-np.ones(3)), 1e4)

    def test_clipping_preserves_crossings_and_missing_breaks(self):
        segments=C.clipped_segments([-2,2,3,4], [0,0,np.nan,0], [-1,1,-1,1])
        self.assertEqual(len(segments),1)
        np.testing.assert_allclose(segments[0],[[-1,0],[1,0]])

    def test_training_knots_remove_duplicate_and_boundary_quantiles(self):
        age = np.repeat([18., 30., 60., 85.], [20, 2, 2, 20])
        k = C.training_knots(age, 25)
        self.assertTrue(np.all(np.diff(k)>0))
        self.assertTrue(np.all((k>18)&(k<85)))
        self.assertEqual(len(C.training_knots(age,0)),0)

    def test_prais_winsten_agrees_when_stationary_and_records_constraint(self):
        X,y = C.trend_data(60,.8,np.random.default_rng(35))
        np.testing.assert_allclose(C.stationary_prais_winsten(X,y)['coef'], O.prais_winsten(X,y)['coef'], rtol=1e-12)
        g=np.random.default_rng(8)
        X=O.design(np.linspace(0,1,30))
        y=np.exp(np.linspace(0,5,30))+g.normal(0,.01,30)
        out=C.stationary_prais_winsten(X,y,rho_bound=.1)
        self.assertLessEqual(abs(out['rho']),.1)
        self.assertGreater(out['constrained_updates'],0)
        self.assertTrue(np.isfinite(out['coef']).all())

if __name__ == '__main__':
    unittest.main()
