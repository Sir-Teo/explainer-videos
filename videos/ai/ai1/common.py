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


import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import ALPHA27, load  # noqa: F401

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


def tt(s: str) -> str:
    """A string of symbols for TeX: typewriter face, spaces as a visible space (␣)."""
    return r"\texttt{" + s.replace(" ", r"\textvisiblespace{}") + "}"
