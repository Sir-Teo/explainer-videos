"""Synthetic geometry and split checks, not validation of original fonts or trained video models."""
import unittest
from unittest.mock import patch
import numpy as np
from videos.ai.ai22 import video

class SyntheticClips(unittest.TestCase):
    def test_bouncing_stays_in_bounds_and_reflects_at_walls(self):
        room = video.GL - video.S_LET
        for start, velocity in [((0, 0), (-1, -1)), ((room, room), (1, 1)), ((2, 3), (1, 0))]:
            path = video.physics(start, velocity, 60)
            self.assertEqual(path.shape, (60, 2))
            self.assertTrue(np.all(path >= 0))
            self.assertTrue(np.all(path <= room))
            self.assertTrue(np.all(np.abs(np.diff(path, axis=0)) <= 1))
        edge = video.physics((0, 0), (-1, -1), 2)
        np.testing.assert_array_equal(edge, [[0, 0], [1, 1]])

    def test_generated_clips_respect_mocked_font_split_and_seed(self):
        letters = np.stack([np.ones((video.S_LET, video.S_LET)) * x for x in (.25, .75)])
        labels = np.array([2, 7]); held = np.array([False, True])
        with patch.object(video, 'small_letters', return_value=(letters, labels, held)):
            train = video.make_clips(8, 5, seed=12, split='train')
            repeat = video.make_clips(8, 5, seed=12, split='train')
            test = video.make_clips(8, 5, seed=12, split='test')
        for a, b in zip(train, repeat): np.testing.assert_array_equal(a, b)
        self.assertTrue(np.all(train[1] == 2))
        self.assertTrue(np.all(test[1] == 7))
        self.assertEqual(train[0].shape, (8, 5, video.GL, video.GL))
        self.assertTrue(np.allclose(train[0].max(axis=(-1, -2)), .25))
        self.assertTrue(np.allclose(test[0].max(axis=(-1, -2)), .75))

    def test_centroid_for_point_is_in_pixel_coordinates(self):
        frames = np.zeros((2, video.GL, video.GL)); frames[0, 3, 4] = 1; frames[1, 7, 9] = 1
        np.testing.assert_allclose(video.centers(frames), [[3,4],[7,9]], atol=1e-8)

if __name__ == '__main__':
    unittest.main()
