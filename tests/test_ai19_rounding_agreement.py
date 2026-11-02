"""Select a valid high-resolution suffix without assuming monotonic errors."""

from videos.ai.ai19.s09_rounding import agreement_suffix


def test_one_good_point_does_not_hide_later_disagreement():
    assert agreement_suffix([1.25, 1.01, 1.15, 1.02]) == 3


def test_no_good_suffix_reports_last_point_not_entire_range():
    assert agreement_suffix([1.25, 1.16, 1.15, 1.12]) == 3


def test_all_good_reports_whole_range():
    assert agreement_suffix([1.02, 0.99, 1.01]) == 0
