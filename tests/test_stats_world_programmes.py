"""Distinct school and health interventions must not overwrite each other's truth."""
import numpy as np
import pytest
from explainer.stats.world import World


def test_school_programme_adds_twenty_points_to_each_treated_pupil():
    class WithoutTutoring(World):
        SCHOOL_PROGRAMME_EFFECT = 0.
    actual = World().schools
    baseline = WithoutTutoring().schools
    np.testing.assert_array_equal(actual['programme'],baseline['programme'])
    np.testing.assert_array_equal(actual['ses'],baseline['ses'])
    expected=20*actual['programme'][actual['school']]
    np.testing.assert_allclose(actual['score']-baseline['score'],expected,atol=2e-13)
    assert World.SCHOOL_PROGRAMME_EFFECT==pytest.approx(.2)


def test_health_programme_retains_its_separate_blood_pressure_effect():
    assert World.HEALTH_PROGRAMME_EFFECT==pytest.approx(-4.)
    assert 'PROGRAMME_EFFECT' not in World.__dict__
