"""The recorded wobble score is a second difference, not speed or jerk."""
import unittest
import numpy as np
from videos.ai.ai22.video import jerk_of

class WobbleUnits(unittest.TestCase):
    def test_constant_displacement_has_zero_wobble(self):
        clips=np.zeros((1,5,20,20))
        for t in range(5):clips[0,t,5,t]=1
        self.assertAlmostEqual(jerk_of(clips),0,places=8)

    def test_quadratic_path_measures_second_not_third_difference(self):
        clips=np.zeros((1,5,20,20))
        for t in range(5):clips[0,t,5,t*t]=1
        self.assertAlmostEqual(jerk_of(clips),2,places=8)
