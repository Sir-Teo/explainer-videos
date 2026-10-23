"""Helpers shared by the scenes of Part 1 ("The Guessing Game").

The series' instruments live in ``explainer/ai`` (chapter cards and the timeline strip, the series map, the
scoreboard, payoff and reference cards).  Here:

* letters: Shannon's 27 symbols drawn in a monospace face, the space shown as a faint ``␣``;
  :func:`letter_row` lays a string out as one Text whose ``[i]`` is its i-th letter;
* :func:`letter_bars`, a bar chart over the 27 symbols;
* :class:`ZoomLadder`, the chain rule drawn as nested intervals: each row is the previous row's chosen sliver,
  magnified to full width and split again by the next conditional probabilities (Chapter 1, and Chapter 6, where the
  same picture turns out to be an arithmetic coder);
* :func:`code_tree`, a prefix code drawn as a binary tree;
* :func:`surprise_color`, the colormap for -log2 p (dark = expected, bright = surprising).
"""

from __future__ import annotations


import math

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import ALPHA27, load  # noqa: F401

PART = 1
MONO = "DejaVu Sans Mono"
SPACE = "␣"  # ␣


def glyph(c: str) -> str:
    return SPACE if c == " " else c


def letter_row(s: str, font_size=30, color=WHITE, space_opacity=0.35) -> Text:
    """``s`` in the monospace face, one submobject per character (spaces drawn as faint ␣)."""
    t = Text(s.replace(" ", SPACE), font=MONO, font_size=font_size, color=color)
    assert len(t) == len(s), (s, len(t))
    for ch, m in zip(s, t):
        if ch == " ":
            m.set_opacity(space_opacity)
    return t


def letter(c: str, font_size=30, color=WHITE) -> Text:
    return letter_row(c, font_size=font_size, color=color, space_opacity=0.6)


def wrap_words(s: str, width: int) -> list[str]:
    """Break ``s`` into lines of at most ``width`` characters at spaces (each line keeps its trailing space, so the
    lines concatenate back to ``s``)."""
    lines, cur = [], ""
    for w in s.split(" "):
        piece = w + " "
        if len(cur) + len(w) > width and cur:
            lines.append(cur)
            cur = ""
        cur += piece
    if cur:
        lines.append(cur)
    lines[-1] = lines[-1][:-1] if lines[-1].endswith(" ") and not s.endswith(" ") else lines[-1]
    assert "".join(lines) == s
    return lines


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
_SURPRISE_STOPS = [(0.0, "#1C2433"), (1.5, "#2E4A78"), (3.5, "#8E4E9E"), (5.5, C.SURPRISE), (9.0, C.BITS)]


def surprise_color(bits: float) -> ManimColor:
    """-log2 p as a color: near 0 bits a dark slate (expected), then blue, violet, pink, and yellow (9+ bits)."""
    b = float(np.clip(bits, 0, _SURPRISE_STOPS[-1][0]))
    for (b0, c0), (b1, c1) in zip(_SURPRISE_STOPS, _SURPRISE_STOPS[1:]):
        if b <= b1:
            return interpolate_color(ManimColor(c0), ManimColor(c1), (b - b0) / (b1 - b0))
    return ManimColor(_SURPRISE_STOPS[-1][1])


def surprise_legend(width=4.0, height=0.18, vmax=9.0, font_size=18) -> VGroup:
    n = 60
    cells = VGroup(*[Rectangle(width=width / n, height=height, stroke_width=0, fill_opacity=1,
                               fill_color=surprise_color(vmax * (i + 0.5) / n)) for i in range(n)])
    cells.arrange(RIGHT, buff=0)
    ticks = VGroup()
    for b in (0, 3, 6, 9):
        x = cells.get_left()[0] + width * b / vmax
        ticks.add(MathTex(str(b), font_size=font_size, color=GREY_B).move_to([x, cells.get_bottom()[1] - 0.18, 0]))
    cap = label(r"bits of surprise", font_size=font_size, color=GREY_B).next_to(cells, UP, buff=0.1)
    return VGroup(cells, ticks, cap)


# ---------------------------------------------------------------------------
# Bars over the 27 symbols
# ---------------------------------------------------------------------------
def letter_bars(p, order=None, width=12.0, height=3.2, pmax=None, color=C.TRUE_P, font_size=22, gap=0.18,
                labels=True, base=(0, -2.2)) -> VGroup:
    """Bars for a distribution over the 27 symbols (in ALPHA27 order, or ``order``: a list of symbol indices).
    Returns a VGroup with ``.bars`` (indexed by position) and ``.labels``; ``.idx`` maps position -> symbol."""
    p = np.asarray(p, float)
    order = list(range(27)) if order is None else list(order)
    pmax = pmax or p.max()
    slot = width / len(order)
    x0, y0 = base[0] - width / 2, base[1]
    bars, labs = VGroup(), VGroup()
    for k, i in enumerate(order):
        h = max(height * p[i] / pmax, 0.005)
        b = Rectangle(width=slot * (1 - gap), height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        b.move_to([x0 + (k + 0.5) * slot, y0 + h / 2, 0])
        bars.add(b)
        if labels:
            labs.add(letter(ALPHA27[i], font_size=font_size, color=GREY_A).move_to([x0 + (k + 0.5) * slot, y0 - 0.25, 0]))
    g = VGroup(bars, labs)
    g.bars, g.labels, g.idx, g.slot, g.x0, g.y0, g.height, g.pmax = bars, labs, order, slot, x0, y0, height, pmax
    return g


def bars_to(g: VGroup, p, pmax=None, color=None) -> list:
    """Animations that set the bars of ``g`` to the distribution ``p`` (same layout)."""
    pmax = pmax or g.pmax
    anims = []
    for k, i in enumerate(g.idx):
        h = max(g.height * float(p[i]) / pmax, 0.005)
        target = Rectangle(width=g.bars[k].width, height=h, stroke_width=0,
                           fill_color=color or g.bars[k].get_fill_color(), fill_opacity=0.9)
        target.move_to([g.bars[k].get_x(), g.y0 + h / 2, 0])
        anims.append(Transform(g.bars[k], target))
    return anims


# ---------------------------------------------------------------------------
# The zoom ladder: the chain rule as nested intervals
# ---------------------------------------------------------------------------
class ZoomLadder:
    """Rows of horizontal bars.  Row k shows one interval (the previous row's chosen sliver, magnified to the full
    width ``W``) split into 27 slivers in proportion to ``probs`` (in ALPHA27 order); the chosen sliver is filled
    green and joined to the next row by a funnel.  ``row(k)`` builds row k; :meth:`funnel` the connector."""

    def __init__(self, steps: list[dict], W=10.6, x=0.6, bar_h=0.42, font_size=22):
        self.steps, self.W, self.x, self.bar_h, self.fs = steps, W, x, bar_h, font_size

    def bounds(self, k: int, s: int) -> tuple[float, float]:
        probs = self.steps[k]["probs"]
        a = float(sum(probs[:s]))
        return a, a + float(probs[s])

    def row(self, k: int, y: float, chosen: bool = True, labels: bool = True) -> VGroup:
        st = self.steps[k]
        s = ALPHA27.index(st["symbol"])
        L = self.x - self.W / 2
        g = VGroup()
        cells = VGroup()
        cum = 0.0
        for j, pj in enumerate(st["probs"]):
            w = self.W * pj
            fill = C.INTERVAL if (chosen and j == s) else ("#26303E" if j % 2 == 0 else "#313C4C")
            r = Rectangle(width=max(w, 0.002), height=self.bar_h, stroke_width=0.6, stroke_color=BACKGROUND,
                          fill_color=fill, fill_opacity=1.0 if (chosen and j == s) else 0.95)
            r.move_to([L + (cum + pj / 2) * self.W, y, 0])
            cells.add(r)
            cum += pj
        g.add(cells)
        labs = VGroup()
        if labels:
            cum = 0.0
            for j, pj in enumerate(st["probs"]):
                w = self.W * pj
                if w > 0.2 or (chosen and j == s):
                    t = letter(ALPHA27[j], font_size=self.fs if w > 0.2 else self.fs - 4,
                               color=BLACK if (chosen and j == s) else GREY_A)
                    t.move_to([L + (cum + pj / 2) * self.W, y, 0])
                    if chosen and j == s and w < 0.2:  # a thin chosen sliver: its letter sits just above it
                        t.set_color(C.INTERVAL).next_to(cells[j], UP, buff=0.06)
                    labs.add(t)
                cum += pj
        g.add(labs)
        frame = Rectangle(width=self.W, height=self.bar_h, stroke_width=1.5, stroke_color=GREY_C).move_to([self.x, y, 0])
        g.add(frame)
        g.cells, g.labs, g.frame, g.s = cells, labs, frame, s
        return g

    def funnel(self, k: int, y_top: float, y_bot: float) -> VGroup:
        """Lines from the ends of row k's chosen sliver (at y_top) to the ends of row k+1 (at y_bot), and a faint fill."""
        s = ALPHA27.index(self.steps[k]["symbol"])
        a, b = self.bounds(k, s)
        L = self.x - self.W / 2
        p0 = np.array([L + a * self.W, y_top - self.bar_h / 2, 0])
        p1 = np.array([L + b * self.W, y_top - self.bar_h / 2, 0])
        q0 = np.array([L, y_bot + self.bar_h / 2, 0])
        q1 = np.array([L + self.W, y_bot + self.bar_h / 2, 0])
        fill = Polygon(p0, p1, q1, q0, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.10)
        lines = VGroup(Line(p0, q0, color=C.INTERVAL, stroke_width=1.5, stroke_opacity=0.7),
                       Line(p1, q1, color=C.INTERVAL, stroke_width=1.5, stroke_opacity=0.7))
        return VGroup(fill, lines)


# ---------------------------------------------------------------------------
# Code trees
# ---------------------------------------------------------------------------
def code_tree(codes: dict, x_range=(-6.4, 6.4), y_top=2.6, dy=0.55, leaf_font=22, order=None, dot_r=0.05,
              edge_width=2.5, show_bits=True) -> VGroup:
    """A prefix code {symbol: '0101'} drawn as a binary tree: the root at the top, a 0 branch to the left (BIT0) and a
    1 branch to the right (BIT1), leaves evenly spaced in code order.  Returns a VGroup with ``.edges`` (dict
    prefix -> Line), ``.nodes`` (prefix -> Dot), ``.leaves`` (symbol -> label) and ``.pos`` (prefix -> point)."""
    syms = sorted(codes, key=lambda s: codes[s]) if order is None else order
    n = len(syms)
    xs = np.linspace(x_range[0], x_range[1], n) if n > 1 else [0.0]
    pos = {}
    for s, x in zip(syms, xs):
        c = codes[s]
        pos[c] = np.array([x, y_top - dy * len(c), 0.0])
    # internal nodes: midpoint (in x) of their two children, from the deepest up
    prefixes = {c[:k] for c in codes.values() for k in range(len(max(codes.values(), key=len)) + 1) if k <= len(c)}
    for pre in sorted(prefixes, key=len, reverse=True):
        if pre in pos:
            continue
        kids = [pos[pre + b] for b in "01" if pre + b in pos]
        pos[pre] = np.array([np.mean([k[0] for k in kids]), y_top - dy * len(pre), 0.0])
    g = VGroup()
    edges, nodes, leaves, bits = {}, {}, {}, VGroup()
    for pre, p in pos.items():
        if pre == "":
            continue
        parent = pos[pre[:-1]]
        col = C.BIT0 if pre[-1] == "0" else C.BIT1
        e = Line(parent, p, color=col, stroke_width=edge_width)
        edges[pre] = e
        if show_bits and len(pre) <= 3:
            t = MathTex(pre[-1], font_size=18, color=col).move_to((parent + p) / 2 + (LEFT if pre[-1] == "0" else RIGHT) * 0.14)
            bits.add(t)
    for pre, p in pos.items():
        nodes[pre] = Dot(p, radius=dot_r, color=GREY_A)
    inv = {c: s for s, c in codes.items()}
    for c, s in inv.items():
        leaves[s] = letter(s, font_size=leaf_font, color=WHITE).next_to(pos[c], DOWN, buff=0.1)
    g.add(VGroup(*edges.values()), bits, VGroup(*nodes.values()), VGroup(*leaves.values()))
    g.edges, g.nodes, g.leaves, g.pos, g.bits = edges, nodes, leaves, pos, bits
    return g


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------
def polyline(ax: Axes, xs, ys, color=WHITE, stroke_width=3, **kw) -> VMobject:
    pts = np.array([ax.c2p(float(a), float(b)) for a, b in zip(xs, ys)])
    m = VMobject(color=color, stroke_width=stroke_width, **kw)
    m.set_points_as_corners(pts)
    return m


def plain_axes(x_range, y_range, x_length, y_length, **kw) -> Axes:
    cfg = {"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05, "stroke_width": 2}
    cfg.update(kw.pop("axis_config", {}))
    return Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length, tips=False,
                axis_config=cfg, **kw)


def valley_steps(eta: float, x0: float = -1.0, n: int = 5, width: float = 1.8, height: float = 1.1,
                 color=C.BITS) -> VGroup:
    """Gradient descent on the valley y = x^2, drawn small: the curve, and n steps x <- x - eta * 2x from x0, each a
    dot joined to the next by an arrow (a jargon-card picture: small steps downhill, or overshooting ones)."""
    sx, sy = width / 3.0, height / 2.25  # x in [-1.5, 1.5], y in [0, 2.25]
    curve = VMobject(stroke_color=GREY_B, stroke_width=2.5).set_points_smoothly(
        [np.array([x * sx, x * x * sy, 0]) for x in np.linspace(-1.5, 1.5, 31)])
    xs = [x0]
    for _ in range(n):
        xs.append(xs[-1] - eta * 2 * xs[-1])
    pts = [np.array([float(np.clip(x, -1.5, 1.5)) * sx, min(x * x, 2.25) * sy, 0]) for x in xs]
    dots = VGroup(*[Dot(p_, radius=0.065, color=color) for p_ in pts])
    dots[0].set_color(WHITE)
    arrows = VGroup(*[Arrow(a, b, buff=0.06, color=color, stroke_width=2.5, max_tip_length_to_length_ratio=0.3,
                            max_stroke_width_to_length_ratio=10) for a, b in zip(pts, pts[1:])
                      if np.linalg.norm(b - a) > 0.12])
    return VGroup(curve, arrows, dots)


def net_sketch(seed: int = 8) -> VGroup:
    """A neural network, drawn small: input -> table of numbers -> bend -> table of numbers -> scores.  The tables'
    cells are the adjustable numbers (lit by how large each is); the bend is a kinked curve (a jargon-card picture)."""
    rng = np.random.default_rng(seed)

    def table(rows, cols):
        return VGroup(*[Square(0.2, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.BITS,
                               fill_opacity=float(rng.uniform(0.15, 0.95))) for _ in range(rows * cols)]
                      ).arrange_in_grid(rows, cols, buff=0.03)

    inp = VGroup(*[Square(0.2, stroke_width=1, stroke_color=GREY_B, fill_color=C.TOKEN, fill_opacity=0.5)
                   for _ in range(4)]).arrange(DOWN, buff=0.03)
    t1, t2 = table(4, 5), table(5, 4)
    frame = Square(0.9, stroke_width=1.2, stroke_color=GREY_C)
    kink = VMobject(stroke_color=C.MLP, stroke_width=3.5).set_points_as_corners(
        [frame.get_left() + DOWN * 0.15, frame.get_center() + DOWN * 0.15, frame.get_corner(UR) + LEFT * 0.08])
    bend = VGroup(frame, kink)
    hs = [0.75, 0.3, 0.55, 0.15]
    out = VGroup(*[Rectangle(width=0.16, height=h, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.9)
                   for h in hs]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
    parts = VGroup(inp, t1, bend, t2, out).arrange(RIGHT, buff=0.55)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.35) for a, b in zip(parts, parts[1:])])
    names = [r"input", r"$\times$ a table", r"bend", r"$\times$ a table", r"scores"]
    labs = VGroup(*[label(t, font_size=20, color=GREY_A) for t in names])
    for lb, p_ in zip(labs, parts):
        lb.move_to([p_.get_x(), parts.get_bottom()[1] - 0.28, 0])
    return VGroup(parts, arrows, labs)


def tt(s: str) -> str:
    """A string of symbols for TeX: typewriter face, spaces as a visible space (␣)."""
    return r"\texttt{" + s.replace(" ", r"\textvisiblespace{}") + "}"


def area_slivers(p, W=11.0, x=0.0, y0=-2.4, scale=0.34, color=C.SURPRISE, opacity=0.8, order=None) -> VGroup:
    """Each symbol a rectangle of width W p(x) and height scale * log2(1/p(x)): total area = W * scale * H(p).
    The rectangles are laid out left to right in ``order`` (default: as given); ``g[i]`` is symbol i's."""
    order = list(range(len(p))) if order is None else list(order)
    rects, cum = {}, 0.0
    L = x - W / 2
    for i in order:
        pi = p[i]
        h = scale * (-math.log2(pi)) if pi > 0 else 0.0
        r = Rectangle(width=max(W * pi, 0.003), height=max(h, 0.003), stroke_width=0.8, stroke_color=BACKGROUND,
                      fill_color=color, fill_opacity=opacity)
        r.move_to([L + (cum + pi / 2) * W, y0 + h / 2, 0])
        rects[i] = r
        cum += pi
    return VGroup(*[rects[i] for i in range(len(p))])
