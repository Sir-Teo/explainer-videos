"""IntervalRain colours each interval by whether it catches the truth, and counts."""

from explainer.stats import IntervalRain, S, axes


def test_hits_and_misses():
    A = axes([0, 10], [0, 10])
    r = IntervalRain(A.ax, truth=5.0)
    s1, ok1 = r._seg(4, 6, 0)
    s2, ok2 = r._seg(6, 8, 1)
    assert ok1 and not ok2
    assert s1.get_color().to_hex().lower() == str(S.KEPT).lower()
    assert s2.get_y() < s1.get_y()
