import numpy as np

from explainer.stats.kit import multi as M
from explainer.stats.viz import DistanceMap


def test_distance_map_parts_and_exact_rebuild():
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 10, (30, 2))
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    Y = M.classical_mds(D, 2)["X"]
    fit = M.procrustes(X, Y)["fitted"]
    assert np.max(np.abs(fit - X)) < 1e-8
    dm = DistanceMap(X, fit, width=6.0, height=4.0, edges=[(0, 1), (1, 2)], names=[str(i) for i in range(30)],
                     label_idx=[0, 5])
    assert len(dm.truth) == 30 and len(dm.rebuilt) == 30 and len(dm.residuals) == 30
    assert len(dm.roads) == 2 and len(dm.labels) == 2
    assert dm.width <= 6.0 + 0.5 and dm.height <= 4.0 + 0.5
    # every residual segment is (numerically) a point when the rebuild is exact
    assert max(r.get_length() for r in dm.residuals) < 1e-6
