"""Coverage uncertainty must survive saving and reloading correlated-target simulations."""
import numpy as np
import pytest
from explainer.stats import board as B


def test_empirical_dataset_error_changes_the_reference_band():
    row=B.Row(26,"hierarchical","8 correlated targets per dataset","coverage",.95,.939,1000,mc_se=.004)
    assert row.se==.004
    assert row.verdict==B.KEPT
    assert B.verdict("coverage",.95,.939,8000)==B.BROKEN


def test_optional_error_survives_a_normal_board_round_trip(tmp_path,monkeypatch):
    monkeypatch.setattr(B,"REPO_ROOT",tmp_path)
    row=B.Row(26,"hierarchical","1000 independent datasets","coverage",.95,.9376,1000,mc_se=.0027)
    B.save_rows(26,[row])
    loaded=B.load_all(upto=26)
    assert len(loaded)==1
    assert loaded[0].se==row.se
    assert loaded[0].verdict==row.verdict==B.BROKEN


def test_legacy_rows_keep_the_independent_bernoulli_reference():
    row=B.Row(1,"interval","iid data","coverage",.95,.949,1000)
    assert row.se==pytest.approx(np.sqrt(.95*.05/1000))
    assert row.verdict==B.KEPT


@pytest.mark.parametrize("error",[-.1,np.nan,np.inf])
def test_invalid_error_is_not_displayed_as_a_calibration_band(error):
    row=B.Row(26,"method","setting","coverage",.95,.95,1000,mc_se=error)
    with pytest.raises(ValueError):_ = row.se
    with pytest.raises(ValueError):_ = row.verdict
