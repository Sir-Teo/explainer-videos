"""Synthetic Connect Four rule checks, not AlphaZero training acceptance."""
import random
import unittest
import numpy as np
from videos.ai.ai26 import c4


def wins(grid, player):
    for r in range(6):
        for c in range(7):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = [(r + j*dr, c + j*dc) for j in range(4)]
                if all(0 <= y < 6 and 0 <= x < 7 and grid[y,x] == player for y,x in cells):
                    return True
    return False

class ConnectFourSynthetic(unittest.TestCase):
    def test_bitboards_match_independent_grid_during_legal_games(self):
        rng = random.Random(2626)
        for _ in range(150):
            board = c4.Board(); grid = np.zeros((6,7), np.int8)
            for turn in range(42):
                legal = [c for c in range(7) if grid[5,c] == 0]
                self.assertEqual(board.legal(), legal)
                player = 1 if turn % 2 == 0 else -1
                for c in legal:
                    row = next(r for r in range(6) if grid[r,c] == 0)
                    trial = grid.copy(); trial[row,c] = player
                    self.assertEqual(board.wins_with(c), wins(trial, player))
                    self.assertEqual(bool(c4.is_winning_move(np.int64(board.pos), np.int64(board.mask), c)),
                                     wins(trial, player))
                    p2, m2 = c4.play(np.int64(board.pos), np.int64(board.mask), c)
                    next_board = board.play(c)
                    self.assertEqual((int(p2), int(m2)), (next_board.pos, next_board.mask))
                if not legal: break
                c = rng.choice(legal); row = next(r for r in range(6) if grid[r,c] == 0)
                grid[row,c] = player; board = board.play(c)
                np.testing.assert_array_equal(board.grid(), grid)
                self.assertEqual(c4.last_mover_won(board), wins(grid, player))
                planes = board.planes(); self.assertEqual(int(planes.sum()), turn + 1)
                if wins(grid, player): break

if __name__ == '__main__':
    unittest.main()
