"""Helpers shared by the scenes of Part 60 ("Domain-Specific Hardware")."""

from __future__ import annotations

import math  # noqa: F401

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs31.common import BG, DATA, HEAD, KERN, LAM, NO, YES  # noqa: F401
from videos.cs.cs37.common import axes, trace  # noqa: F401
from videos.cs.cs40.common import code_block, module_box  # noqa: F401

from .compute import load  # noqa: F401

PART = 60


def tag_box(text: str, color=DATA, size=18, w=None, h=0.5):
    """A DOM node or a token drawn as a rounded box with monospace text."""
    t = mono(text, size=size, color=color)
    box = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.6, fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


def timeline_bar(x0: float, x1: float, y: float, color, h=0.32, scale=1.0, label_text=None, size=14):
    """A span of time on a horizontal timeline (x in scene units), optionally labelled inside."""
    r = Rectangle(width=max(0.02, (x1 - x0) * scale), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x0 * scale + (x1 - x0) * scale / 2, y, 0])
    if label_text:
        t = label(label_text, font_size=size, color=BLACK)
        if t.width < r.width - 0.05:
            t.move_to(r)
            return VGroup(r, t)
    return VGroup(r)


class SystolicView(VGroup):
    """An N x N output-stationary systolic grid drawn from a ``wave`` trace (``load("wave")["os"]``): each cell shows
    its running sum, with the operand pair it holds (a from the left in DATA blue, b from above in LAM purple); busy
    cells glow.  The waiting inputs are drawn as skewed queues: row i of A to the left, column j of B above.
    ``step(t)`` returns the animations that move the drawing to cycle t."""

    def __init__(self, wave: dict, size: float = 0.95, gap: float = 0.16, font_size: int = 22, queues: bool = True):
        super().__init__()
        self.wave, self.n, self.size, self.gap, self.fs = wave, wave["n"], size, gap, font_size
        self.queues_on = queues
        n = self.n
        self.boxes = VGroup(*[Square(size, stroke_color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1)
                              for _ in range(n * n)]).arrange_in_grid(n, n, buff=gap)
        self.add(self.boxes)
        self.acc = VGroup(*[self._acc(0, i, j) for i in range(n) for j in range(n)])
        self.ops = VGroup(*[self._ops(None, None, i, j) for i in range(n) for j in range(n)])
        self.add(self.acc, self.ops)
        self.qa, self.qb = self._queues(-1)
        if queues:
            self.add(self.qa, self.qb)

    def box(self, i, j):
        return self.boxes[i * self.n + j]

    def _acc(self, v, i, j):
        return label(rf"{v}", font_size=self.fs, color=WHITE if v else GREY_D).move_to(self.box(i, j)).shift(
            DOWN * 0.12 * self.size)

    def _ops(self, a, b, i, j):
        bx = self.box(i, j)
        ta = label(rf"{a or 0}", font_size=self.fs - 7, color=DATA).move_to(bx.get_corner(UL) + RIGHT * 0.2 * self.size
                                                                            + DOWN * 0.18 * self.size)
        tb = label(rf"{b or 0}", font_size=self.fs - 7, color=LAM).move_to(bx.get_corner(UR) + LEFT * 0.2 * self.size
                                                                           + DOWN * 0.18 * self.size)
        ta.set_opacity(0 if a is None else 1)
        tb.set_opacity(0 if b is None else 1)
        return VGroup(ta, tb)

    def _queues(self, t):
        """The inputs still waiting before cycle t+1: A[i][k] enters row i at cycle i + k; B[k][j] column j at j + k."""
        A, B, n = self.wave["A"], self.wave["B"], self.n
        step = self.size * 0.62
        qa, qb = VGroup(), VGroup()
        for i in range(n):
            left = self.box(i, 0).get_left()
            for k in range(n):
                d = i + k - t          # cycles until it enters
                q = label(rf"{A[i][k]}", font_size=self.fs - 6, color=DATA).move_to(left + LEFT * (0.1 + max(d, 1) * step))
                qa.add(q.set_opacity(1 if d >= 1 else 0))
        for j in range(n):
            top = self.box(0, j).get_top()
            for k in range(n):
                d = j + k - t
                q = label(rf"{B[k][j]}", font_size=self.fs - 6, color=LAM).move_to(top + UP * (0.05 + max(d, 1) * step * 0.45))
                qb.add(q.set_opacity(1 if d >= 1 else 0))
        return qa, qb

    def step(self, t):
        tr = self.wave["trace"][t]
        n = self.n
        anims = []
        for i in range(n):
            for j in range(n):
                busy = tr["k"][i][j] is not None
                idx = i * n + j
                anims.append(self.boxes[idx].animate.set_fill(HEAD if busy else BG, opacity=0.28 if busy else 1)
                             .set_stroke(HEAD if busy else GREY_B))
                anims.append(Transform(self.acc[idx], self._acc(tr["acc"][i][j], i, j)))
                anims.append(Transform(self.ops[idx], self._ops(tr["a"][i][j] if busy else None,
                                                                 tr["b"][i][j] if busy else None, i, j)))
        if self.queues_on:
            qa, qb = self._queues(t)
            anims += [Transform(self.qa, qa), Transform(self.qb, qb)]
        return anims


# ---- spoken numbers and a log-log plot, shared by the TPU, GPU and memory chapters

def say_int(n: int) -> str:
    """An integer below a million as a speaker says it (British: 'one hundred and five')."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return _ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + say_int(rest))
    rest = n % 1000
    return say_int(n // 1000) + " thousand" + ("" if rest == 0 else (" and " if rest < 100 else " ") + say_int(rest))


def say_dec(x: float, digits: int = 1) -> str:
    """x with ``digits`` decimals, spoken digit by digit after the point."""
    s = f"{x:.{digits}f}"
    whole, frac = s.split(".")
    return say_int(int(whole)) + " point " + " ".join(_ONES[int(c)] for c in frac)


FRACTION = {8: "an eighth", 9: "a ninth", 10: "a tenth", 11: "an eleventh", 12: "a twelfth", 16: "a sixteenth",
            17: "a seventeenth", 18: "an eighteenth", 19: "a nineteenth", 20: "a twentieth"}


def commas(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


class LogPlot(VGroup):
    """Log-log axes: x from 10^x0 to 10^x1, y from 10^y0 to 10^y1, with power-of-ten tick labels."""

    def __init__(self, x0, x1, y0, y1, xlab, ylab, x_length=6.4, y_length=4.2, yfmt=None):
        super().__init__()
        self.x0, self.y0 = x0, y0
        self.ax = Axes(x_range=[0, x1 - x0, 1], y_range=[0, y1 - y0, 1], x_length=x_length, y_length=y_length,
                       tips=False, axis_config={"color": GREY_D, "include_ticks": False})
        lx = VGroup(*[label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(self.c2p(p, y0), DOWN, buff=0.12)
                      for p in range(x0, x1 + 1)])
        ly = VGroup(*[label(yfmt(p) if yfmt else rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(
            self.c2p(x0, p), LEFT, buff=0.12) for p in range(y0, y1 + 1)])
        xl = label(xlab, font_size=18, color=GREY_A).next_to(lx, DOWN, buff=0.12)
        yl = label(ylab, font_size=18, color=GREY_A).next_to(self.ax, UP, buff=0.12).align_to(self.ax, LEFT)
        self.add(self.ax, lx, ly, xl, yl)

    def c2p(self, u, v):
        return self.ax.c2p(u - self.x0, v - self.y0)

    def roof(self, peak, bw, color, width=4):
        """The roof min(peak, I bw) in log units: peak in ops/s, bw in bytes/s."""
        x0, x1 = self.x0, self.x0 + self.ax.x_range[1]
        lr = math.log10(peak / bw)
        pts = [self.c2p(x0, x0 + math.log10(bw)), self.c2p(lr, math.log10(peak)), self.c2p(x1, math.log10(peak))]
        return VMobject(color=color, stroke_width=width).set_points_as_corners(pts)
