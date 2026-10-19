"""Helpers shared by the scenes of Part 26 ("Reinforcement Learning, from Bellman to AlphaZero")."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 26
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
AGENT = C.RL_POLICY  # the agent, its policy pi
ENV = GREY_B  # the environment
REWARD = C.REWARD  # rewards, wins
PENALTY = C.PENALTY  # penalties, losses
VALUE = C.BASELINE  # values V, Q; the critic
TDERR = C.ADVANTAGE  # the TD error delta, advantages
EXPLORE = C.ENTROPY  # exploration: bonuses, noise, randomness
SEARCH = C.BITS  # search: visit counts, the tree
PRIOR = C.MODEL_Q  # a network's prior P over moves
GAMMA_C = C.CONTEXT  # the discount gamma

COLORS = {r"\pi": AGENT, r"V": VALUE, r"Q": VALUE, r"r": REWARD, r"R": REWARD, r"\gamma": GAMMA_C,
          r"\delta": TDERR, r"A": TDERR, r"G": REWARD}


def curve(ax, xs, ys, color, stroke_width=3, smooth=False) -> VMobject:
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys) if np.isfinite(y)]
    m = VMobject(color=color, stroke_width=stroke_width)
    return m.set_points_smoothly(pts) if smooth else m.set_points_as_corners(pts)


def band(ax, xs, lo, hi, color, opacity=0.18) -> VMobject:
    """The region between two curves (a spread across seeds)."""
    top = [ax.c2p(x, y) for x, y in zip(xs, hi)]
    bot = [ax.c2p(x, y) for x, y in zip(xs, lo)][::-1]
    return Polygon(*top, *bot, stroke_width=0, fill_color=color, fill_opacity=opacity)


def axes(x_range, y_range, x_length=6.0, y_length=3.6, xlabel="", ylabel="", xticks=None, yticks=None,
         xfmt=None, yfmt=None, font_size=20, center=ORIGIN, log_x=False) -> VGroup:
    """Plain axes with a few tick labels and names; ``ax`` is the first element. ``log_x``: x_range in log10."""
    ax = CornerAxes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
    g = VGroup(ax)
    xfmt = xfmt or (lambda v: (f"10^{{{int(v)}}}" if log_x else f"{v:g}"))
    yfmt = yfmt or (lambda v: f"{v:g}")
    for v in (xticks if xticks is not None else []):
        g.add(MathTex(xfmt(v), font_size=font_size, color=GREY_B).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.12))
    for v in (yticks if yticks is not None else []):
        g.add(MathTex(yfmt(v), font_size=font_size, color=GREY_B).next_to(ax.c2p(x_range[0], v), LEFT, buff=0.12))
    if xlabel:
        xl = label(xlabel, font_size=font_size + 2, color=GREY_A)
        xl.next_to(ax, DOWN, buff=0.5 if xticks is not None else 0.2)
        g.add(xl)
        g.xlabel = xl
    if ylabel:
        yl = label(ylabel, font_size=font_size + 2, color=GREY_A).next_to(ax, UP, buff=0.18).align_to(ax, LEFT)
        g.add(yl)
        g.ylabel = yl
    g.ax = ax
    g.move_to(center)
    return g


def legend(items, font_size=20, buff=0.18) -> VGroup:
    """(color, text) rows with a short line swatch."""
    rows = VGroup()
    for col, txt in items:
        rows.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=col, stroke_width=5), label(txt, font_size=font_size, color=col))
                 .arrange(RIGHT, buff=0.15))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def chip(text: str, size=0.46, color=GREY_B, font_size=26, fill=0.12, width=None) -> VGroup:
    box = RoundedRectangle(width=width or size, height=size, corner_radius=0.08, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=fill)
    t = Text(text, font=MONO, font_size=font_size, color=WHITE).move_to(box)
    return VGroup(box, t)


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def loop_arrow(a: Mobject, b: Mobject, color=GREY_B, angle=-0.6, stroke_width=3) -> CurvedArrow:
    return CurvedArrow(a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05, angle=angle, color=color,
                       stroke_width=stroke_width, tip_length=0.18)


def tile_frame(caption, color, TW=3.0, TH=2.0):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color="#121722", fill_opacity=1)
    return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)


# ---------------------------------------------------------------------------
# Go, for AlphaGo's games: the board and stones
# ---------------------------------------------------------------------------
GO_WOOD = "#D9A85B"


def go_board(size=19, side=5.6, center=ORIGIN) -> VGroup:
    step = side / (size - 1)
    g = VGroup()
    wood = Square(side + step * 1.2, stroke_width=0, fill_color=GO_WOOD, fill_opacity=1)
    g.add(wood)
    lines = VGroup()
    for i in range(size):
        lines.add(Line([-side / 2, -side / 2 + i * step, 0], [side / 2, -side / 2 + i * step, 0], stroke_width=1,
                       color="#3B2A12"))
        lines.add(Line([-side / 2 + i * step, -side / 2, 0], [-side / 2 + i * step, side / 2, 0], stroke_width=1,
                       color="#3B2A12"))
    g.add(lines)
    for x in (3, 9, 15):
        for y in (3, 9, 15):
            g.add(Dot([-side / 2 + x * step, -side / 2 + y * step, 0], radius=step * 0.11, color="#3B2A12"))
    g.step, g.side = step, side
    g.move_to(center)
    g.origin = g[0].get_center() + np.array([-side / 2, side / 2, 0])  # the top-left intersection
    return g


def go_point(board, col: int, row_from_top: int):
    return board[0].get_center() + np.array([-board.side / 2 + col * board.step, board.side / 2 - row_from_top * board.step, 0])


def go_stone(board, col, row, black: bool, scale=0.92) -> Circle:
    r = board.step * 0.5 * scale
    return Circle(radius=r, stroke_width=1 if not black else 0, stroke_color="#555555",
                  fill_color="#111111" if black else "#F4F4F0", fill_opacity=1).move_to(go_point(board, col, row))
