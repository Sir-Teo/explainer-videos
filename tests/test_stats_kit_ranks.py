import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import ranks as R


def test_signed_rank_exact():
    g = np.random.Generator(np.random.PCG64(2))
    d = g.normal(0.5, 1, 12)
    r = R.wilcoxon_signed_rank(d)
    s = stats.wilcoxon(d, method="exact")
    assert r["p"] == pytest.approx(s.pvalue)
    assert R.signed_rank_null(10).sum() == pytest.approx(1.0)


def test_mann_whitney_exact_and_auc():
    g = np.random.Generator(np.random.PCG64(3))
    x, y = g.normal(1, 1, 7), g.normal(0, 1, 9)
    r = R.mann_whitney(x, y)
    s = stats.mannwhitneyu(x, y, method="exact")
    assert r["U"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue)
    assert R.mann_whitney_null(4, 5).sum() == pytest.approx(1.0)


def test_kw_spearman_kendall():
    g = np.random.Generator(np.random.PCG64(4))
    a, b, c = g.normal(0, 1, 6), g.normal(1, 1, 7), g.normal(2, 1, 5)
    assert R.kruskal_wallis(a, b, c)["H"] == pytest.approx(stats.kruskal(a, b, c).statistic)
    x, y = g.normal(size=20), g.normal(size=20)
    assert R.spearman(x, y) == pytest.approx(stats.spearmanr(x, y).statistic)
    assert R.kendall(x, y) == pytest.approx(stats.kendalltau(x, y).statistic)
