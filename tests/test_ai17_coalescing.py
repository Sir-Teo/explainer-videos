"""Synthetic address patterns validate the actual diagram's transaction units."""
import unittest

from videos.ai.ai17.coalescing import sectors_touched


class Coalescing(unittest.TestCase):
    def test_adjacent_aligned_floats_use_four_sectors(self):
        self.assertEqual(sectors_touched(range(0, 128, 4)), [0, 1, 2, 3])

    def test_misalignment_costs_an_extra_sector(self):
        self.assertEqual(sectors_touched(range(4, 132, 4)), [0, 1, 2, 3, 4])

    def test_strided_float_loads_use_thirty_two_sectors(self):
        self.assertEqual(len(sectors_touched([32 * k for k in range(32)])), 32)

    def test_word_order_and_broadcast_do_not_add_transactions(self):
        self.assertEqual(sectors_touched(reversed(range(0, 128, 4))), [0, 1, 2, 3])
        self.assertEqual(sectors_touched([0] * 32), [0])

    def test_word_crossing_a_boundary_touches_both_sectors(self):
        self.assertEqual(sectors_touched([30]), [0, 1])

    def test_invalid_addresses_and_sizes_fail(self):
        for addresses, size in [([-1], 4), ([1.5], 4), ([0], 0), ([0], 4.5), ([0], True)]:
            with self.assertRaises(ValueError):
                sectors_touched(addresses, word_bytes=size)
        for size in (0, -1, 32.0, True):
            with self.assertRaises(ValueError):
                sectors_touched([0], sector_bytes=size)


if __name__ == "__main__":
    unittest.main()
