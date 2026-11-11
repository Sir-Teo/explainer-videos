"""Helpers shared by the scenes of Part 8 ("Out of Order")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, say, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401

from .compute import load  # noqa: F401

PART = 8

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
LIMIT = C.CS_LIMIT
INF = C.CS_INF
CLOCK = C.CS_CLOCK
HIST = C.HUMAN
BG = "#121722"

# the life of an instruction in the core
PHASES = (("fetch", GREY_D), ("wait", CTRL), ("execute", FUNC), ("done", DATA), ("commit", YES))
KIND_COLOR = {"load": INF, "store": INF, "branch": NO, "jump": HEAD, "alu": FUNC, "mul": CTRL, "div": CTRL}


# ---------------------------------------------------------------------------
# a recorded timeline: instructions down, cycles across, each bar coloured by what the instruction is doing
# ---------------------------------------------------------------------------
class OooChart(VGroup):
    """``timeline``: uops as recorded by compute (``t`` = fetched, renamed, issued, complete, committed).
    Each row: the instruction, then a bar for each phase (waiting in the issue queue, executing, complete but
    waiting to commit) and a mark at commit.  Squashed instructions are drawn grey and struck through.
    ``rows[i]``, ``bars[i]`` (a VGroup of the phases), ``commits[i]``; ``x(c)`` is the x of cycle c."""

    def __init__(self, timeline, cw=0.3, ch=0.32, label_width=2.6, label_size=14, max_rows=None, show_fetch=False,
                 c0=None, c1=None, heads_every=5):
        super().__init__()
        tl = timeline[:max_rows] if max_rows else timeline
        self.c0 = c0 if c0 is not None else min(u["t"][1] for u in tl if u["t"][1] >= 0)
        last = max(max(x for x in u["t"] if x >= 0) for u in tl)
        self.c1 = c1 if c1 is not None else last + 1
        self.cw, self.ch = cw, ch
        x0 = label_width / 2 + 0.2
        self.x0 = x0
        self.rows, self.bars, self.commits = [], [], []
        for i, u in enumerate(tl):
            y = -i * ch
            t = u["t"]
            sq = u["squashed"]
            lab = Text(u["text"], font="DejaVu Sans Mono", font_size=label_size, color=GREY_D if sq else CODE)
            if lab.width > label_width:
                lab.width = label_width
            lab.move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            if sq:
                lab.add(Line(lab.get_left(), lab.get_right(), color=NO, stroke_width=1.5))
            bars = VGroup()
            end = t[4] if t[4] >= 0 else max(x for x in t if x >= 0) + 1
            spans = []
            if show_fetch and t[0] >= 0 and t[1] >= 0:
                spans.append((t[0], t[1], GREY_D))
            if t[1] >= 0:
                spans.append((t[1], t[2] if t[2] >= 0 else (t[3] if t[3] >= 0 else end), CTRL))
            if t[2] >= 0:
                spans.append((t[2], t[3] if t[3] >= 0 else end, FUNC))
            if t[3] >= 0:
                spans.append((t[3], t[4] if t[4] >= 0 else t[3], DATA))
            for a, b, col in spans:
                a, b = max(a, self.c0), min(b, self.c1)
                if b <= a:
                    continue
                r = Rectangle(width=(b - a) * cw - 0.02, height=ch * 0.62, stroke_width=0,
                              fill_color=GREY_D if sq else col, fill_opacity=0.25 if sq else 0.75)
                r.move_to([self.x(a) + (b - a) * cw / 2 - cw / 2, y, 0])
                bars.add(r)
            mark = VectorizedPoint([self.x(max(t[3], self.c0)), y, 0])
            if t[4] >= 0 and self.c0 <= t[4] < self.c1:
                mark = Square(side_length=ch * 0.62, stroke_width=0, fill_color=YES, fill_opacity=1).move_to(
                    [self.x(t[4]), y, 0])
            self.rows.append(lab)
            self.bars.append(bars)
            self.commits.append(mark)
            self.add(lab, bars, mark)
        self.heads = VGroup()
        for c in range(self.c0, self.c1):
            if (c - self.c0) % heads_every == 0:
                self.heads.add(Text(str(c - self.c0), font_size=11, color=GREY_C).move_to([self.x(c), ch * 0.9, 0]))
        self.add(self.heads)
        self.n = len(tl)

    def x(self, c: float) -> float:
        return self.x0 + (c - self.c0) * self.cw + self.cw / 2

    def column_line(self, c, color=HEAD):
        top = self.heads.get_top()[1] if len(self.heads) else 0.3
        return DashedLine([self.x(c) - self.cw / 2, top, 0], [self.x(c) - self.cw / 2, -self.n * self.ch, 0],
                          color=color, stroke_width=2, dash_length=0.08)


def phase_legend(font_size=18, show_fetch=False):
    items = [(r"waiting for operands", CTRL), (r"executing", FUNC), (r"done, \ waiting to commit", DATA),
             (r"committed", YES)]
    if show_fetch:
        items.insert(0, (r"fetch and decode", GREY_D))
    g = VGroup()
    for t, c in items:
        g.add(VGroup(Square(side_length=0.2, stroke_width=0, fill_color=c, fill_opacity=0.8),
                     label(t, font_size=font_size, color=GREY_A)).arrange(RIGHT, buff=0.12))
    return g.arrange(RIGHT, buff=0.45)


# ---------------------------------------------------------------------------
# the reorder buffer as a ring
# ---------------------------------------------------------------------------
class RobRing(VGroup):
    """``n`` slots round a circle; ``slots[i]`` is slot i (an annular sector), ``fill(i, color)`` an animation that
    fills it, ``pointer(i, text, color)`` an arrow and its label pointing at slot i from outside."""

    def __init__(self, n=16, inner=1.3, outer=2.0, color=GREY_C):
        super().__init__()
        self.n, self.inner, self.outer = n, inner, outer
        self.slots = VGroup()
        for i in range(n):
            a = PI / 2 - TAU * i / n
            s = AnnularSector(inner_radius=inner, outer_radius=outer, angle=-TAU / n * 0.94, start_angle=a,
                              stroke_color=color, stroke_width=1.5, fill_color=BG, fill_opacity=1)
            self.slots.add(s)
        self.add(self.slots)

    def angle(self, i: float) -> float:
        return PI / 2 - TAU * (i + 0.47) / self.n

    def at(self, i: float, r: float) -> np.ndarray:
        a = self.angle(i)
        return self.get_center() + r * np.array([np.cos(a), np.sin(a), 0])

    def pointer(self, i, text, color=HEAD, font_size=20):
        tip = self.at(i, self.outer + 0.05)
        tail = self.at(i, self.outer + 0.65)
        arr = Arrow(tail, tip, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        lab = label(text, font_size=font_size, color=color).move_to(self.at(i, self.outer + 1.0))
        return VGroup(arr, lab)

    def tag(self, i, text, color=CODE, font_size=12):
        t = Text(text, font="DejaVu Sans Mono", font_size=font_size, color=color)
        if t.width > (self.outer - self.inner) * 0.95:
            t.width = (self.outer - self.inner) * 0.95
        return t.move_to(self.at(i, (self.inner + self.outer) / 2))


# ---------------------------------------------------------------------------
# a dataflow graph laid out by earliest start time
# ---------------------------------------------------------------------------
def dag_figure(d, dx=0.95, dy=0.62, font_size=13, times=None, critical_color=HEAD, skip=("jump",)):
    """Nodes from ``load("dataflow")``: column = start time (``times`` or the earliest), rows packed per column;
    instructions of the kinds in ``skip`` (jumps, which depend on nothing) are left out.  Returns a VGroup with
    ``.nodes`` (dict index -> node), ``.edges`` (dict (i, j) -> arrow), ``.critical`` (the arrows of the critical
    path, thicker), ``.edge_group``."""
    nodes = d["nodes"]
    times = times or d["asap"]
    shown = [i for i, n in enumerate(nodes) if n["kind"] not in skip]
    lanes: dict[int, int] = {}
    pos = {}
    for i in shown:
        t = times[i]
        k = lanes.get(t, 0)
        lanes[t] = k + 1
        pos[i] = (t, k)
    hmax = max(lanes.values())
    g = VGroup()
    g.nodes = {}
    ng = VGroup()
    for i in shown:
        t, k = pos[i]
        n = nodes[i]
        col = KIND_COLOR.get(n["kind"], FUNC)
        txt = Text(n["text"].split(" ")[0], font="DejaVu Sans Mono", font_size=font_size, color=WHITE)
        r = RoundedRectangle(width=max(0.78, txt.width + 0.16), height=0.42, corner_radius=0.08, stroke_color=col,
                             stroke_width=2, fill_color=col, fill_opacity=0.25)
        node = VGroup(r, txt.move_to(r)).move_to([t * dx, -(k - (hmax - 1) / 2) * dy, 0])
        g.nodes[i] = node
        ng.add(node)
    g.node_group = ng
    g.add(ng)
    g.edges = {}
    edge_group = VGroup()
    for a, b, _ in d["edges"]:
        if a not in g.nodes or b not in g.nodes:
            continue
        A, B = g.nodes[a], g.nodes[b]
        arr = Arrow(A.get_right(), B.get_left(), buff=0.04, stroke_width=2, color=GREY_B,
                    max_tip_length_to_length_ratio=0.15, tip_length=0.12)
        g.edges[(a, b)] = arr
        edge_group.add(arr)
    g.add_to_back(edge_group)
    g.edge_group = edge_group
    cp = d["critical"]
    g.critical = VGroup(*[g.edges[(a, b)].copy().set_color(critical_color).set_stroke(width=5)
                          for a, b in zip(cp, cp[1:]) if (a, b) in g.edges])
    g.add(g.critical)  # (so it moves with the graph; scenes add the parts they show one by one)
    g.critical_nodes = VGroup(*[g.nodes[i] for i in cp if i in g.nodes])
    return g


def slot_grid(d, starts, width, cw=0.62, ch=0.42, font_size=12):
    """A schedule as the machine sees it: ``width`` issue slots (rows) against cycles (columns), each instruction
    in its cycle's next free slot.  Returns a VGroup with ``.cells`` (dict index -> cell) and ``.frame``."""
    T = max(starts) + 1
    g = VGroup()
    frame = VGroup()
    for c in range(T):
        for w in range(width):
            frame.add(Rectangle(width=cw, height=ch, stroke_color=GREY_D, stroke_width=1).move_to(
                [c * cw, -w * ch, 0]))
    g.frame = frame
    g.add(frame)
    g.cells = {}
    used: dict[int, int] = {}
    for i, t in enumerate(starts):
        k = used.get(t, 0)
        used[t] = k + 1
        n = d["nodes"][i]
        col = KIND_COLOR.get(n["kind"], FUNC)
        r = Rectangle(width=cw * 0.92, height=ch * 0.84, stroke_width=0, fill_color=col, fill_opacity=0.55)
        txt = Text(n["text"].split(" ")[0], font="DejaVu Sans Mono", font_size=font_size, color=WHITE)
        if txt.width > cw * 0.85:
            txt.width = cw * 0.85
        cell = VGroup(r, txt.move_to(r)).move_to([t * cw, -k * ch, 0])
        g.cells[i] = cell
        g.add(cell)
    g.T = T
    return g


# ---------------------------------------------------------------------------
# a grid of cells (for the scoreboard and Tomasulo's tables)
# ---------------------------------------------------------------------------
def grid_table(header, rows, widths, row_h=0.42, font_size=18, header_color=GREY_B, colors=None, mono_cols=(0,)):
    """``header``: column titles (Tex); ``rows``: lists of strings (Tex, or monospaced in ``mono_cols``).
    Returns a VGroup with ``.cells[r][c]`` (r = 0 is the header) and ``.rule``."""
    g = VGroup()
    g.cells = []
    xs = np.cumsum([0] + list(widths[:-1])) + np.array(widths) / 2
    for r, row in enumerate([header] + rows):
        line = []
        for c, txt in enumerate(row):
            if r > 0 and c in mono_cols:
                m = (Text(txt, font="DejaVu Sans Mono", font_size=font_size - 3, color=CODE) if txt.strip()
                     else VectorizedPoint())
            else:
                col = header_color if r == 0 else (colors[r - 1][c] if colors else WHITE)
                m = label(txt, font_size=font_size, color=col) if txt else VectorizedPoint()
            if m.width > widths[c] - 0.1:
                m.width = widths[c] - 0.1
            m.move_to([xs[c], -r * row_h, 0])
            if r > 0 and c in mono_cols:
                m.align_to([xs[c] - widths[c] / 2 + 0.05, 0, 0], LEFT)
            line.append(m)
            g.add(m)
        g.cells.append(line)
    g.rule = Line([0, -row_h / 2, 0], [sum(widths), -row_h / 2, 0], color=GREY_D, stroke_width=1.5)
    g.add(g.rule)
    return g


def bar_chart(values, names, colors, height=3.0, bar_w=0.7, gap=0.45, vmax=None, fmt_=lambda v: f"{v:.2f}",
              font_size=18, log=False):
    """Vertical bars with their values on top and names below."""
    vmax = vmax or max(values)
    g = VGroup()
    g.bars, g.vals, g.names = VGroup(), VGroup(), VGroup()
    for k, (v, nm, c) in enumerate(zip(values, names, colors)):
        h = height * ((np.log10(max(v, 1)) / np.log10(vmax)) if log else v / vmax)
        h = max(h, 0.02)
        b = Rectangle(width=bar_w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
        b.move_to([k * (bar_w + gap), h / 2, 0])
        t = label(fmt_(v), font_size=font_size, color=c).next_to(b, UP, buff=0.08)
        n = label(nm, font_size=font_size - 2, color=GREY_A).next_to([k * (bar_w + gap), 0, 0], DOWN, buff=0.15)
        if n.width > bar_w + gap - 0.05:
            n.width = bar_w + gap - 0.05
        g.bars.add(b)
        g.vals.add(t)
        g.names.add(n)
    base = Line([-bar_w, 0, 0], [(len(values) - 1) * (bar_w + gap) + bar_w, 0, 0], color=GREY_C, stroke_width=1.5)
    g.add(base, g.bars, g.vals, g.names)
    return g
