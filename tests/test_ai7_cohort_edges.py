"""Cohort counts must describe the data actually used, including small inputs."""
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai7 import compute


class GaussianProcessCohort(unittest.TestCase):
    def test_learning_replay_caps_reported_page_counts_to_available_pages(self):
        data = dict(x=np.arange(3.), y=np.array([.2, -.1, .3]), xs=np.linspace(0, 3, 5),
                    ell=1., s2=.5, noise=.1, mu0=0.)
        with patch.object(compute, 'load', return_value=data):
            result = compute.compute_gpland()
        self.assertEqual(result['ns'], [min(n, 3) for n in compute.GP_NS])
        self.assertEqual(result['means'].shape, (len(compute.GP_NS), 5))
        self.assertTrue(np.all(np.diff(result['mean_sd']) <= 1e-12))
        final_mean, final_sd = compute.gp_post(data['x'], data['y'], data['xs'], 1., .5, .1)
        np.testing.assert_allclose(result['means'][-1], final_mean, atol=1e-14)
        np.testing.assert_allclose(result['sds'][-1], final_sd, atol=1e-14)


if __name__ == '__main__':
    unittest.main()
