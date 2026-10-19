"""Boards and trees for the parts about search, games and reinforcement learning (Parts 2 and 26).

* :class:`GridView`, a gridworld: walls, special cells, a value heat map and the greedy policy's arrows;
* :class:`C4View`, a Connect Four board: stones dropped into columns, and bars over the columns (a policy, visit
  counts, the solver's verdicts);
* :class:`SearchTree`, a game tree laid out tidily (leaves evenly spaced, parents centred), its edges as thick as the
  visits they carry, so a search can be seen growing.
"""

from __future__ import annotations

import numpy as np

from explainer.analysis import label
from explainer.ai.viz import *  # noqa: F401,F403

FIRST, SECOND = "#F2C14E", "#E8505B"  # Connect Four: the first player's stones, the second's
BOARD_BLUE = "#1F4E9C"
VAL_NEG, VAL_ZERO, VAL_POS = "#E8505B", "#1A2130", "#3FBF8F"


def value_color(v: float, vmax: float = 1.0) -> ManimColor:
    """A diverging colour for a value: red below zero, dark at zero, green above."""
    t = float(np.clip(v / vmax, -1, 1))
    if t >= 0:
        return interpolate_color(ManimColor(VAL_ZERO), ManimColor(VAL_POS), t ** 0.8)
    return interpolate_color(ManimColor(VAL_ZERO), ManimColor(VAL_NEG), (-t) ** 0.8)


class GridView(VGroup):
    """A gridworld drawn from its layout strings ('.' free, '#' wall, 'G' goal, 'P' pit, 'S' start)."""

    def __init__(self, layout, cell=0.62, center=ORIGIN):
        super().__init__()
        self.layout, self.rows, self.cols, self.cell = layout, len(layout), len(layout[0]), cell
        self.squares = {}
        self.marks = VGroup()
        x0 = -(self.cols - 1) * cell / 2
        y0 = (self.rows - 1) * cell / 2
        self._origin = np.array([x0, y0, 0.0])
        for r in range(self.rows):
            for c in range(self.cols):
                ch = layout[r][c]
                sq = Square(cell, stroke_color=GREY_D, stroke_width=1.2,
                            fill_color="#3A4250" if ch == "#" else VAL_ZERO, fill_opacity=1)
                sq.move_to(self._origin + np.array([c * cell, -r * cell, 0.0]))
                self.squares[(r, c)] = sq
                self.add(sq)
                if ch in "GPS":
                    txt = {"G": r"$+1$", "P": r"$-1$", "S": r"start"}[ch]
                    col = {"G": VAL_POS, "P": VAL_NEG, "S": GREY_A}[ch]
                    m = label(txt, font_size=22 if ch != "S" else 16, color=col).move_to(sq)
                    self.marks.add(m)
        for (r, c), sq in self.squares.items():
            if layout[r][c] in "GP":
                sq.set_stroke(VAL_POS if layout[r][c] == "G" else VAL_NEG, width=3)
        self.add(self.marks)
        self.move_to(center)

    def center_of(self, r, c):
        return self.squares[(r, c)].get_center()

    def square(self, r, c) -> Square:
        return self.squares[(r, c)]

    def heat(self, cells, values, vmax=1.0) -> list:
        """Animations that colour each free cell by its value."""
        anims = []
        for (r, c), v in zip(cells, values):
            if self.layout[r][c] in "#":
                continue
            anims.append(self.squares[(r, c)].animate.set_fill(value_color(v, vmax), opacity=1))
        return anims

    def set_heat(self, cells, values, vmax=1.0):
        for (r, c), v in zip(cells, values):
            if self.layout[r][c] != "#":
                self.squares[(r, c)].set_fill(value_color(v, vmax), opacity=1)
        return self

    def arrows(self, cells, actions, skip=(), color=WHITE, scale=0.32) -> VGroup:
        """The policy: an arrow in each cell pointing along its action (0 up, 1 right, 2 down, 3 left)."""
        dirs = [UP, RIGHT, DOWN, LEFT]
        g = VGroup()
        for i, ((r, c), a) in enumerate(zip(cells, actions)):
            if i in skip or self.layout[r][c] in "#GP":
                g.add(VectorizedPoint(self.squares[(r, c)].get_center()))
                continue
            ctr = self.squares[(r, c)].get_center()
            d = dirs[int(a)] * self.cell * scale
            g.add(Arrow(ctr - d, ctr + d, buff=0, stroke_width=3, color=color, max_tip_length_to_length_ratio=0.45,
                        max_stroke_width_to_length_ratio=12))
        return g

    def numbers(self, cells, values, digits=2, font_size=14, color=WHITE) -> VGroup:
        g = VGroup()
        for (r, c), v in zip(cells, values):
            if self.layout[r][c] == "#":
                continue
            g.add(MathTex(f"{v:.{digits}f}".replace("-", "{-}"), font_size=font_size, color=color)
                  .move_to(self.squares[(r, c)]))
        return g


class C4View(VGroup):
    """A Connect Four board: 7 columns, 6 rows, row 0 at the bottom. Stones are added by :meth:`drop`."""

    def __init__(self, cell=0.6, center=ORIGIN):
        super().__init__()
        self.cell = cell
        W, H = 7, 6
        self.frame = RoundedRectangle(width=W * cell + 0.3, height=H * cell + 0.3, corner_radius=0.12,
                                      stroke_width=0, fill_color=BOARD_BLUE, fill_opacity=1)
        self.holes = VGroup(*[Circle(radius=cell * 0.38, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1)
                              .move_to(self._xy(r, c)) for r in range(H) for c in range(W)])
        self.stones = VGroup()
        self.stone_at = {}
        self.add(self.frame, self.holes, self.stones)
        self.move_to(center)

    def _xy(self, r, c):
        return self.frame.get_center() + np.array([(c - 3) * self.cell, (r - 2.5) * self.cell, 0.0])

    def cell_center(self, r, c):
        return self._xy(r, c)

    def col_x(self, c) -> float:
        return float(self._xy(0, c)[0])

    def stone(self, r, c, player: int) -> Circle:
        return Circle(radius=self.cell * 0.36, stroke_width=0, fill_color=FIRST if player == 1 else SECOND,
                      fill_opacity=1).move_to(self._xy(r, c))

    def set_grid(self, grid):
        """Place stones from a 6 x 7 array (+1 first player, -1 second, 0 empty), row 0 at the bottom."""
        self.stones.remove(*self.stones.submobjects)
        self.stone_at = {}
        for r in range(6):
            for c in range(7):
                if grid[r][c]:
                    s = self.stone(r, c, 1 if grid[r][c] > 0 else -1)
                    self.stones.add(s)
                    self.stone_at[(r, c)] = s
        return self

    def height(self, c) -> int:
        return sum(1 for (r, cc) in self.stone_at if cc == c)

    def drop(self, c, player: int, run_time=0.45) -> Animation:
        """The animation of a stone falling into column c (and its bookkeeping)."""
        r = self.height(c)
        s = self.stone(r, c, player)
        top = self._xy(6.6, c)
        s.move_to(top)
        self.stones.add(s)
        self.stone_at[(r, c)] = s
        return s.animate(run_time=run_time, rate_func=rate_functions.ease_in_quad).move_to(self._xy(r, c))

    def play_moves(self, moves, first_player=1):
        """Place a sequence of moves at once (column numbers), alternating players."""
        p = first_player
        for c in moves:
            r = self.height(c)
            s = self.stone(r, c, p)
            self.stones.add(s)
            self.stone_at[(r, c)] = s
            p = -p
        return self

    def bars(self, values, color=C.BITS, height=1.4, vmax=None, gap=0.12, show=None) -> VGroup:
        """Bars over the columns (a probability per column, visit shares...), on a baseline just above the board."""
        values = np.nan_to_num(np.asarray(values, float))
        vmax = vmax or max(values.max(), 1e-9)
        base = self.frame.get_top()[1] + gap
        g = VGroup()
        for c, v in enumerate(values):
            h = max(height * v / vmax, 0.01)
            g.add(Rectangle(width=self.cell * 0.62, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
                  .move_to([self.col_x(c), base + h / 2, 0]))
        return g

    def column_marks(self, ok, font_size=26) -> VGroup:
        """A tick or cross under each column (True / False / None for a full column)."""
        g = VGroup()
        y = self.frame.get_bottom()[1] - 0.28
        for c, v in enumerate(ok):
            if v is None:
                g.add(VectorizedPoint([self.col_x(c), y, 0]))
                continue
            g.add(MathTex(r"\checkmark" if v else r"\times", font_size=font_size,
                          color=VAL_POS if v else VAL_NEG).move_to([self.col_x(c), y, 0]))
        return g


class SearchTree(VGroup):
    """A tree laid out with leaves evenly spaced and each parent over the middle of its children.

    ``tree`` is nested: ``{"children": [subtree, ...], ...}`` (any other keys are kept on ``node_data``).  Nodes are
    numbered in breadth-first order; ``self.nodes[i]``, ``self.edges[i]`` (the edge into node i, None for the
    root), ``self.depth[i]``, ``self.parent[i]``."""

    def __init__(self, tree, width=12.0, level_height=1.3, radius=0.12, node_color=GREY_B, edge_color=GREY_C,
                 edge_width=None, center=ORIGIN, max_edge=10.0):
        super().__init__()
        order, parent, depth, data = [], {}, {}, {}
        queue = [(tree, None, 0)]
        kids: dict[int, list[int]] = {}
        while queue:
            t, p, d = queue.pop(0)
            i = len(order)
            order.append(t)
            parent[i], depth[i], data[i] = p, d, t
            kids[i] = []
            if p is not None:
                kids[p].append(i)
            for ch in t.get("children", []):
                queue.append((ch, i, d + 1))
        n = len(order)
        # leaves get consecutive slots (depth-first order), parents the mean of their children
        x = np.zeros(n)
        slot = [0]

        def place(i):
            if not kids[i]:
                x[i] = slot[0]
                slot[0] += 1
            else:
                for k in kids[i]:
                    place(k)
                x[i] = np.mean([x[k] for k in kids[i]])

        place(0)
        span = max(slot[0] - 1, 1)
        x = (x / span - 0.5) * width
        self.parent, self.depth, self.node_data, self.kids = parent, depth, data, kids
        self.pos = [np.array([x[i], -depth[i] * level_height, 0.0]) for i in range(n)]
        self.nodes = VGroup(*[Dot(self.pos[i], radius=radius, color=data[i].get("color", node_color)) for i in range(n)])
        self.edges = [None] * n
        ew = edge_width or (lambda d: 2.0)
        edge_group = VGroup()
        for i in range(1, n):
            w = min(ew(data[i]), max_edge)
            e = Line(self.pos[parent[i]], self.pos[i], stroke_width=w, color=data[i].get("edge_color", edge_color),
                     buff=radius)
            self.edges[i] = e
            edge_group.add(e)
        self.edge_group = edge_group
        self.add(edge_group, self.nodes)
        self.move_to(center)
        self.pos = [m.get_center() for m in self.nodes]

    def path_to(self, i) -> list[int]:
        out = [i]
        while self.parent[out[-1]] is not None:
            out.append(self.parent[out[-1]])
        return out[::-1]

    def subtree(self, i) -> list[int]:
        out, stack = [], [i]
        while stack:
            j = stack.pop()
            out.append(j)
            stack.extend(self.kids[j])
        return out
