"""Helpers shared by the scenes of Part 7 ("Pipelines")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import WIRE, gate, junction, wire  # noqa: F401
from videos.cs.cs6.common import box, fmt, mux, say, sci, word_bits  # noqa: F401

from .compute import load  # noqa: F401

PART = 7

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

STAGES = ("IF", "ID", "EX", "MEM", "WB")
STAGE_COLOR = {"IF": DATA, "ID": CTRL, "EX": FUNC, "MEM": INF, "WB": YES}


def mono(s, size=19, color=CODE):
    """One line of code. Text drops leading spaces from its bounding box, so an indented line is anchored by an
    invisible point where its first column would be, and listings aligned on the left keep their indentation."""
    t = Text(s.lstrip(" "), font="DejaVu Sans Mono", font_size=size, color=color)
    n = len(s) - len(s.lstrip(" "))
    if not n:
        return t
    cw = Text("0" * 20, font="DejaVu Sans Mono", font_size=size).width / 20
    return VGroup(VectorizedPoint(t.get_left() + LEFT * n * cw), t)


# ---------------------------------------------------------------------------
# the pipeline chart: instructions down, cycles across
# ---------------------------------------------------------------------------
class PipeChart(VGroup):
    """Built from a recorded chart (``load("charts")[name]``).  ``cells[(seq, cycle)]`` is the cell of an instruction
    in a cycle; ``rows[seq]`` its label; ``column(c)`` every cell of cycle c (to reveal the chart a cycle at a time);
    ``arrows`` the forwarding arrows; ``bubbles`` the stall cells."""

    def __init__(self, data, cycles=None, cw=0.44, ch=0.38, font_size=15, label_width=3.0, label_size=15,
                 max_rows=None):
        super().__init__()
        chart = data["chart"][:cycles] if cycles else data["chart"]
        info = data["seq"]
        order = sorted({int(r[s]) for r in chart for s in STAGES if r[s] is not None and info[str(r[s])]["text"] != "?"})
        if max_rows:
            order = order[:max_rows]
        rowof = {s: k for k, s in enumerate(order)}
        self.cells, self.rows, self.bubbles = {}, {}, VGroup()
        self._fwd: list[tuple[int, int, int, str]] = []
        self.columns: dict[int, VGroup] = {}
        x0 = label_width / 2 + 0.2
        seen: dict[tuple, int] = {}
        for c, r in enumerate(chart):
            col = VGroup()
            for st in STAGES:
                s = r[st]
                if s is None or s not in rowof:
                    continue
                y = -rowof[s] * ch
                again = seen.get((s, st)) is not None
                seen[(s, st)] = c
                flushed = info[str(s)]["flushed"]
                colr = GREY_D if flushed else STAGE_COLOR[st]
                sq = Rectangle(width=cw * 0.94, height=ch * 0.86, stroke_width=1, stroke_color=colr, fill_color=colr,
                               fill_opacity=0.12 if again else 0.32).move_to([x0 + c * cw, y, 0])
                t = Text(st, font_size=font_size, color=GREY_B if again else WHITE).move_to(sq)
                cell = VGroup(sq, t)
                self.cells[(s, c)] = cell
                col.add(cell)
            for ev in r["events"]:
                if ev[0] == "stall":
                    s = ev[1]
                    if s in rowof and (s, c) in self.cells:
                        self.bubbles.add(self.cells[(s, c)])
            self.columns[c] = col
            self.add(col)
        for s in order:
            it = info[str(s)]
            lab = Text(it["text"], font="DejaVu Sans Mono", font_size=label_size,
                       color=GREY_D if it["flushed"] else CODE)
            if lab.width > label_width:
                lab.width = label_width
            lab.move_to([x0 - cw / 2 - 0.15, -rowof[s] * ch, 0], aligned_edge=RIGHT)
            if it["flushed"]:
                lab.add(Line(lab.get_left(), lab.get_right(), color=NO, stroke_width=1.5))
            self.rows[s] = lab
            self.add(lab)
        heads = VGroup(*[Text(str(c + 1), font_size=12, color=GREY_C).move_to([x0 + c * cw, ch * 0.9, 0])
                         for c in range(len(chart))])
        self.heads = heads
        self.add(heads)
        for c, r in enumerate(chart):
            for ev in r["events"]:
                if ev[0] == "fwd" and (ev[1], c - 1) in self.cells and (ev[2], c) in self.cells:
                    self._fwd.append((ev[1], ev[2], c, ev[3]))
        self.rowof = rowof
        self.ncycles = len(chart)

    @property
    def arrows(self) -> VGroup:
        """The forwarding arrows, drawn from where the cells are now (so they follow the chart when it moves)."""
        g = VGroup()
        for src, dst, c, _ in self._fwd:
            a, b = self.cells[(src, c - 1)], self.cells[(dst, c)]
            g.add(CurvedArrow(a.get_corner(DR) + LEFT * 0.08, b.get_corner(UL) + RIGHT * 0.12 + DOWN * 0.05,
                              angle=0.6, color=HEAD, stroke_width=3, tip_length=0.12))
        return g


# ---------------------------------------------------------------------------
# the pipeline as five stages and four pipeline registers
# ---------------------------------------------------------------------------
class PipeFigure(VGroup):
    def __init__(self, width=12.0, stage_w=1.7, h=1.4, y=0.0):
        super().__init__()
        n = 5
        gap = (width - n * stage_w) / (n - 1)
        self.stage = {}
        self.reg = []
        x = -width / 2 + stage_w / 2
        for k, s in enumerate(STAGES):
            b = box(stage_w, h, rf"\text{{{s}}}", STAGE_COLOR[s], 30).move_to([x, y, 0])
            self.stage[s] = b
            self.add(b)
            if k < n - 1:
                r = Rectangle(width=0.16, height=h + 0.5, stroke_color=CLOCK, stroke_width=2, fill_color=CLOCK,
                              fill_opacity=0.35).move_to([x + stage_w / 2 + gap / 2, y, 0])
                self.reg.append(r)
                self.add(r)
            x += stage_w + gap
        names = ["IF/ID", "ID/EX", "EX/MEM", "MEM/WB"]
        self.reg_labels = VGroup(*[MathTex(rf"\text{{{nm}}}", font_size=16, color=CLOCK).next_to(r, DOWN, buff=0.08)
                                   for nm, r in zip(names, self.reg)])
        self.add(self.reg_labels)

    def token(self, stage, text, color=HEAD):
        b = self.stage[stage]
        t = Text(text, font="DejaVu Sans Mono", font_size=15, color=color)
        if t.width > b.box.width - 0.1:
            t.width = b.box.width - 0.1
        return t.move_to(b.box.get_bottom() + UP * 0.32)

    def forward_arcs(self):
        ex = self.stage["EX"].box
        a1 = CurvedArrow(self.reg[2].get_bottom() + DOWN * 0.1, ex.get_bottom() + LEFT * 0.4, angle=-PI / 1.6,
                         color=HEAD, stroke_width=3)
        a2 = CurvedArrow(self.reg[3].get_bottom() + DOWN * 0.1, ex.get_bottom() + LEFT * 0.1, angle=-PI / 1.6,
                         color=HEAD, stroke_width=3)
        return VGroup(a1, a2)


def laundry_strip(n=4, stage_names=("wash", "dry", "fold", "put away"), colors=None, w=1.0, h=0.5, pipelined=True):
    """Loads of laundry against time: one after another, or overlapped."""
    colors = colors or [DATA, HEAD, YES, FUNC]
    g = VGroup()
    for i in range(n):
        start = i if pipelined else i * len(stage_names)
        for k, (nm, c) in enumerate(zip(stage_names, colors)):
            r = Rectangle(width=w * 0.96, height=h * 0.85, stroke_width=0, fill_color=c, fill_opacity=0.6)
            r.move_to([(start + k) * w, -i * h, 0])
            t = Text(nm, font_size=12, color=WHITE)
            if t.width > r.width * 0.86:
                t.width = r.width * 0.86
            g.add(VGroup(r, t.move_to(r)))
    return g
