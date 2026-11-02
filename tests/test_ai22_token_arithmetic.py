"""Exact video accounting: a token grid must cover every input pixel and frame."""
import math
import unittest

from videos.ai.ai22.base import compute_video


class VideoTokenAccounting(unittest.TestCase):
    def test_boundary_patches_are_retained(self):
        rows={r['res']:r for r in compute_video()['rows'] if r['sec']==5}
        # Five seconds contain 80 frames: one alone, 20 later groups.
        self.assertEqual(rows['360p']['tokens'],21*23*40)
        self.assertEqual(rows['720p']['tokens'],21*45*80)
        self.assertEqual(rows['1080p']['tokens'],21*68*120)
        self.assertEqual(rows['360p']['padded_height'],368)
        self.assertEqual(rows['1080p']['padded_height'],1088)

    def test_all_grids_cover_the_clip_with_minimal_padding(self):
        dims={'360p':(640,360),'720p':(1280,720),'1080p':(1920,1080)}
        for row in compute_video()['rows']:
            width,height=dims[row['res']]
            self.assertLessEqual(width,row['padded_width'])
            self.assertLess(row['padded_width']-width,16)
            self.assertLessEqual(height,row['padded_height'])
            self.assertLess(row['padded_height']-height,16)
            # After the standalone first frame, every remaining frame is covered.
            self.assertGreaterEqual(1+4*(row['lat_t']-1),row['frames'])
            self.assertLess(1+4*(row['lat_t']-1)-row['frames'],4)
            self.assertEqual(row['tokens'],row['lat_t']*(row['padded_width']//16)*(row['padded_height']//16))
