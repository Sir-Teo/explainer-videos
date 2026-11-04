"""Helpers shared by the scenes of Part 2 ("Proof and Counting")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 2

# one meaning per colour, for the whole part (the series' palette, explainer/style.py)
DATA = C.CS_DATA  # objects being counted or reasoned about: tiles, numbers, elements
CTRL = C.CS_CONTROL  # moves, rules, steps of a proof
HEAD = C.CS_HEAD  # the current step, the thing being looked at
CODE = C.CS_CODE  # formulas and symbols as written
FUNC = C.CS_FUNC  # functions and maps between sets
COST = C.CS_COST  # counts, sizes
YES = C.CS_TRUE  # true, holds, the invariant kept
NO = C.CS_FALSE  # false, a contradiction, the forbidden
LIMIT = C.CS_LIMIT  # the impossible
INF = C.CS_INF  # the infinite
ADV = C.CS_ADVERSARY  # the skeptic, the opponent in a game
CLOCK = C.CS_CLOCK  # time, clocks, remainders
HIST = C.HUMAN  # people and dates


def fmt(n) -> str:
    """An integer with thousands separators, for TeX."""
    return f"{int(n):,}".replace(",", "{,}")


def say(n) -> str:
    """An integer with thousands separators, for narration."""
    return f"{int(n):,}"


def tile_board(board, cols: int, cell=0.7, font_size=30, hot=(), blank_color=None, tile_color="#1B2130",
               hot_color=None) -> VGroup:
    """A sliding-puzzle board: numbered tiles (0 is the blank).  ``board.tile[v]`` is the tile showing v."""
    hot_color = hot_color or HEAD
    g = VGroup()
    g.tile = {}
    rows = len(board) // cols
    frame = RoundedRectangle(width=cols * cell + 0.16, height=rows * cell + 0.16, corner_radius=0.1,
                             stroke_color=GREY_C, stroke_width=2, fill_color=BACKGROUND, fill_opacity=1)
    g.add(frame)
    for i, v in enumerate(board):
        r, c = divmod(i, cols)
        pos = np.array([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])
        if v == 0:
            continue
        sq = RoundedRectangle(width=cell * 0.92, height=cell * 0.92, corner_radius=0.07, stroke_color=GREY_B,
                              stroke_width=1.5, fill_color=tile_color, fill_opacity=1).move_to(pos)
        t = VGroup(sq, label(str(v), font_size=font_size, color=hot_color if v in hot else WHITE).move_to(pos))
        g.tile[v] = t
        g.add(t)
    g.frame = frame
    g.cell = cell
    g.cols = cols
    g.rows = rows
    return g


def cell_center(board_mob, i: int) -> np.ndarray:
    r, c = divmod(i, board_mob.cols)
    cell = board_mob.cell
    return board_mob.frame.get_center() + np.array([(c - (board_mob.cols - 1) / 2) * cell,
                                                    ((board_mob.rows - 1) / 2 - r) * cell, 0])


def grid_squares(rows: int, cols: int, cell=0.5, stroke=GREY_C, fill="#121722") -> VGroup:
    """An empty board of squares; ``g.sq[(r, c)]`` is the square at row r, column c."""
    g = VGroup()
    g.sq = {}
    for r in range(rows):
        for c in range(cols):
            s = Square(cell, stroke_color=stroke, stroke_width=1.2, fill_color=fill, fill_opacity=1)
            s.move_to([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])
            g.sq[(r, c)] = s
            g.add(s)
    g.cell = cell
    return g


def live_int(value=0, font_size=32, color=COST) -> Integer:
    """An Integer driven by ``.tracker``: animate the tracker, never the number itself."""
    n = Integer(value, font_size=font_size, color=color, group_with_commas=True)
    n.tracker = ValueTracker(value)
    n.add_updater(lambda m: m.set_value(round(m.tracker.get_value())))
    return n


def live_dec(value=0.0, places=3, font_size=32, color=COST) -> DecimalNumber:
    n = DecimalNumber(value, num_decimal_places=places, font_size=font_size, color=color)
    n.tracker = ValueTracker(value)
    n.add_updater(lambda m: m.set_value(m.tracker.get_value()))
    return n


def truth_table(header: list[str], rows: list[list], font_size=30, col_w=1.3, row_h=0.55, colors=None) -> VGroup:
    """A truth table: Tex headers, then rows of booleans shown as T and F in the true and false colours.
    ``t.cells[i][j]`` is row i, column j (row 0 is the header); ``t.rows[i]`` a data row."""
    t = VGroup()
    cells = []
    hdr = VGroup(*[MathTex(h, font_size=font_size, color=(colors or {}).get(j, GREY_A)) for j, h in enumerate(header)])
    for j, m in enumerate(hdr):
        m.move_to([j * col_w, 0, 0])
    cells.append(list(hdr))
    t.add(hdr)
    rule = Line([-col_w / 2, -row_h / 2, 0], [(len(header) - 0.5) * col_w, -row_h / 2, 0], color=GREY_D,
                stroke_width=1.5)
    t.add(rule)
    t.rows = VGroup()
    for i, r in enumerate(rows):
        rowm = VGroup()
        for j, v in enumerate(r):
            txt = ("T" if v else "F") if isinstance(v, bool) else str(v)
            m = MathTex(rf"\mathrm{{{txt}}}", font_size=font_size,
                        color=(YES if v else NO) if isinstance(v, bool) else WHITE)
            m.move_to([j * col_w, -(i + 1) * row_h, 0])
            rowm.add(m)
        cells.append(list(rowm))
        t.rows.add(rowm)
    t.add(t.rows)
    t.cells = cells
    t.rule = rule
    return t
