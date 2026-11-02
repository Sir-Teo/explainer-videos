"""Area in the memory map represents actual token slots, including ragged allocations."""

import numpy as np
import pytest

from videos.ai.ai19.s06_paging import memory_map


@pytest.mark.parametrize("snapshot", [
    [(0, 5, 5, 0)],
    [(0, 5, 3, 0), (5, 11, 6, 1)],
    [(7, 24, 19, 3), (33, 7, 2, 4)],
    [(0, 16, 16, 0), (16, 16, 7, 1)],
])
def test_used_and_reserved_areas_match_token_counts(snapshot):
    cell, block = 0.15, 16
    picture = memory_map(snapshot, 64, block=block, cols=4, cell=cell)
    tokens = lambda opacity: sum(p.width * p.height for p in picture
                                 if np.isclose(p.get_fill_opacity(), opacity)) / (0.86 * cell) ** 2 * block
    assert tokens(0.9) == pytest.approx(sum(row[2] for row in snapshot))
    assert tokens(0.22) == pytest.approx(sum(row[1] - row[2] for row in snapshot))


def test_two_partial_allocations_in_one_cell_keep_both_owners():
    picture = memory_map([(0, 5, 5, 0), (5, 11, 11, 1)], 16, cols=1, cell=1)
    bright = [p for p in picture if np.isclose(p.get_fill_opacity(), 0.9)]
    assert len(bright) == 2
    assert bright[0].get_fill_color() != bright[1].get_fill_color()
    assert bright[0].get_right()[0] == pytest.approx(bright[1].get_left()[0])
