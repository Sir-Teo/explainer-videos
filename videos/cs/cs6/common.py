"""Helpers shared by the scenes of Part 6 ("The Stored-Program Computer")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.zh_text import verbatim
from explainer.cs.gates import WIRE, gate, junction, wire  # noqa: F401

from .compute import load  # noqa: F401

PART = 6

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

FIELD_COLORS = {"op": CTRL, "rd": YES, "rs1": DATA, "rs2": INF, "imm": HEAD, "0": GREY_D}


def code_text(text, **kwargs):
    with verbatim():
        return Text(text, font="DejaVu Sans Mono", **kwargs)


def fmt(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


def say(n) -> str:
    return f"{int(n):,}"


def sci(x: float, digits: int = 2) -> str:
    if x == 0:
        return "0"
    e = int(np.floor(np.log10(abs(x))))
    m = x / 10 ** e
    return rf"{m:.{digits - 1}f} \times 10^{{{e}}}"


def box(w, h, text, color=CTRL, font_size=22, fill=BG):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.2, fill_color=fill,
                         fill_opacity=1)
    parts = text.split(r"\\")
    if len(parts) > 1:
        t = VGroup(*[MathTex(x, font_size=font_size, color=color) for x in parts]).arrange(DOWN, buff=0.08).move_to(b)
    else:
        t = MathTex(text, font_size=font_size, color=color).move_to(b)
    if t.width > w - 0.12:
        t.width = w - 0.12
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def word_bits(word: int, fields, cell: float = 0.3, font_size: int = 20, labels: bool = True,
              show_value: bool = False) -> VGroup:
    """An instruction word as 32 cells, bit 31 on the left, each field in its colour with its name under it.
    ``fields`` is ``isa.fields(word)``: (name, high bit, low bit, value)."""
    cells = VGroup()
    owner = {}
    for name, hi, lo, _ in fields:
        for b in range(lo, hi + 1):
            owner[b] = name
    for k in range(32):
        b = 31 - k
        col = FIELD_COLORS.get(owner.get(b, "0"), GREY_C)
        sq = Rectangle(width=cell, height=cell * 1.35, stroke_color=col, stroke_width=1.4, fill_color=col,
                       fill_opacity=0.16)
        bit = MathTex(str((word >> b) & 1), font_size=font_size, color=col).move_to(sq)
        cells.add(VGroup(sq, bit))
    cells.arrange(RIGHT, buff=0.02)
    g = VGroup(cells)
    g.cells = cells
    g.braces = VGroup()
    g.names = VGroup()
    if labels:
        for name, hi, lo, val in fields:
            seg = VGroup(*[cells[31 - b] for b in range(lo, hi + 1)])
            col = FIELD_COLORS.get(name, GREY_C)
            br = Line(seg.get_corner(DL) + DOWN * 0.08, seg.get_corner(DR) + DOWN * 0.08, color=col, stroke_width=2)
            txt = name if not show_value else f"{name} = {val}"
            nm = MathTex(r"\text{" + txt + "}", font_size=font_size, color=col).next_to(br, DOWN, buff=0.08)
            if nm.width > seg.width + 0.1 and hi - lo < 6:
                nm.width = seg.width + 0.1
            g.braces.add(br)
            g.names.add(nm)
        g.add(g.braces, g.names)
    return g


def mux(h=1.0, w=0.42):
    """A multiplexer: a narrow box, its label running up it."""
    b = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=GREY_B, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    t = MathTex(r"\text{mux}", font_size=15, color=GREY_B).rotate(PI / 2).move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


# ---------------------------------------------------------------------------
# the single-cycle datapath
# ---------------------------------------------------------------------------
class Datapath(VGroup):
    """Pebble's single-cycle datapath: blocks and named wires.  ``lit(names)`` colours a set of wires (the ones an
    instruction uses); ``flow(names)`` sends a packet along them."""

    def __init__(self, scale: float = 1.0):
        super().__init__()
        B = {}
        B["pc"] = box(0.75, 1.0, r"\text{pc}", YES, 24).move_to([-6.15, 0.2, 0])
        B["imem"] = box(1.45, 1.7, r"\text{instruction}\\\text{memory}", DATA, 20).move_to([-4.5, 0.2, 0])
        B["ctrl"] = box(2.2, 0.5, r"\text{control}", CTRL, 24).move_to([-1.3, 1.62, 0])
        B["rf"] = box(1.6, 2.0, r"\text{registers}", YES, 22).move_to([-1.5, 0.0, 0])
        B["imm"] = box(1.5, 0.55, r"\text{immediate}", HEAD, 20).move_to([-1.5, -1.95, 0])
        B["mux_b"] = mux(1.0).move_to([0.45, -0.45, 0])
        B["alu"] = box(1.0, 1.7, r"\text{ALU}", FUNC, 26).move_to([1.55, 0.0, 0])
        B["dmem"] = box(1.45, 1.7, r"\text{data}\\\text{memory}", DATA, 20).move_to([3.55, -0.2, 0])
        B["mux_wb"] = mux(1.3).move_to([5.3, -0.1, 0])
        B["add4"] = box(0.8, 0.5, r"+4", COST, 22).move_to([-4.5, 2.45, 0])
        B["addt"] = box(0.9, 0.5, r"+", COST, 24).move_to([3.55, 2.45, 0])
        B["mux_pc"] = mux(1.0).move_to([5.3, 2.3, 0])
        self.blocks = B
        b = {k: v.box for k, v in B.items()}

        def pt(name, side, dy=0.0, dx=0.0):
            m = b[name]
            p = {"L": m.get_left(), "R": m.get_right(), "T": m.get_top(), "B": m.get_bottom()}[side]
            return p + np.array([dx, dy, 0])

        W = {}

        def path(name, *pts, color=WIRE):
            W[name] = VMobject(color=color, stroke_width=2.6).set_points_as_corners([np.array(p, float) for p in pts])

        path("pc_imem", pt("pc", "R"), pt("imem", "L", 0.0))
        path("pc_add4", pt("pc", "T"), [b["pc"].get_x(), 2.45, 0], pt("add4", "L"))
        path("instr_ctl", pt("imem", "R", 0.6), [-3.2, pt("imem", "R", 0.6)[1], 0], [-3.2, 1.62, 0], pt("ctrl", "L"))
        path("instr_rf", pt("imem", "R", 0.6), [-3.2, pt("imem", "R", 0.6)[1], 0], [-3.2, 0.5, 0], pt("rf", "L", 0.5))
        path("instr_imm", [-3.2, 0.5, 0], [-3.2, -1.95, 0], pt("imm", "L"))
        path("rf_a", pt("rf", "R", 0.5), pt("alu", "L", 0.5))
        path("rf_b", pt("rf", "R", -0.45), pt("mux_b", "L", 0.0))
        path("imm_b", pt("imm", "R"), [0.0, -1.95, 0], [0.0, -0.75, 0], pt("mux_b", "L", -0.3))
        path("mux_alu", pt("mux_b", "R"), pt("alu", "L", -0.45))
        path("alu_dmem", pt("alu", "R", 0.1), pt("dmem", "L", 0.3))
        path("alu_wb", [2.4, pt("alu", "R", 0.1)[1], 0], [2.4, -1.45, 0], [4.75, -1.45, 0], [4.75, -0.45, 0],
             pt("mux_wb", "L", -0.35))
        path("b_dmem", [0.15, pt("rf", "R", -0.45)[1], 0], [0.15, -1.25, 0], [2.65, -1.25, 0],
             [2.65, pt("dmem", "L", -0.5)[1], 0], pt("dmem", "L", -0.5))
        path("dmem_wb", pt("dmem", "R", 0.25), pt("mux_wb", "L", 0.25))
        path("wb_rf", pt("mux_wb", "R"), [5.85, pt("mux_wb", "R")[1], 0], [5.85, -2.6, 0], [-2.7, -2.6, 0],
             [-2.7, -0.6, 0], pt("rf", "L", -0.6))
        path("add4_pc", pt("add4", "R"), [2.75, 2.45, 0], [2.75, 2.0, 0], [4.9, 2.0, 0], pt("mux_pc", "L", -0.3))
        path("imm_t", [0.0, -1.95, 0], [0.0, 1.75, 0], [2.95, 1.75, 0], [2.95, 2.35, 0], pt("addt", "L", -0.1))
        path("pc_t", [b["pc"].get_x(), 2.45, 0], [b["pc"].get_x(), 3.05, 0], [3.25, 3.05, 0], pt("addt", "T"))
        path("t_pc", pt("addt", "R"), pt("mux_pc", "L", 0.15))
        path("alu_pc", [2.4, pt("alu", "R", 0.1)[1], 0], [2.4, 1.2, 0], [5.0, 1.2, 0], [5.0, 1.95, 0],
             pt("mux_pc", "L", -0.35))
        path("pc_next", pt("mux_pc", "R"), [5.95, pt("mux_pc", "R")[1], 0], [5.95, 3.4, 0], [-6.75, 3.4, 0],
             [-6.75, 0.2, 0], pt("pc", "L"))
        path("link_wb", [2.75, 2.0, 0], [2.75, 0.95, 0], [4.95, 0.95, 0], [4.95, 0.35, 0], pt("mux_wb", "L", 0.45))
        ctl = VGroup(*[DashedLine(pt("ctrl", "B", dx=dx), [x, y, 0], color=CTRL, stroke_width=1.4, dash_length=0.07)
                       for dx, x, y in ((-0.6, -1.9, 1.0), (0.3, 0.45, 0.05), (0.8, 1.55, 0.85),
                                        (1.05, 3.55, 0.65))])
        self.wires = W
        self.ctl = ctl
        self.dots = VGroup(*[junction(p, r=0.05) for p in ([-3.2, pt("imem", "R", 0.6)[1], 0], [-3.2, 0.5, 0],
                                                           [0.0, -1.95, 0], [2.4, pt("alu", "R", 0.1)[1], 0],
                                                           [0.15, pt("rf", "R", -0.45)[1], 0], [2.75, 2.0, 0],
                                                           [b["pc"].get_x(), 2.45, 0])])
        self.add(VGroup(*W.values()), ctl, self.dots, VGroup(*B.values()))
        self.scale(scale)

    def wires_of(self, names) -> VGroup:
        return VGroup(*[self.wires[n] for n in names])

    def lit(self, names, color=HEAD, width=5.0):
        self._lit = getattr(self, "_lit", set()) | set(names)
        return [self.wires[n].animate.set_stroke(color, width) for n in names]

    def unlit(self, names=None):
        names = list(names or getattr(self, "_lit", set()))
        self._lit = getattr(self, "_lit", set()) - set(names)
        return [self.wires[n].animate.set_stroke(WIRE, 2.6) for n in names] or [Wait(0.01)]

    def flow(self, scene, names, color=HEAD, run_time=1.4):
        dots = [Dot(self.wires[n].get_start(), radius=0.07, color=color) for n in names]
        scene.add(*dots)
        scene.play(*[MoveAlongPath(d, self.wires[n].copy()) for d, n in zip(dots, names)], run_time=run_time,
                   rate_func=linear)
        scene.remove(*dots)


# which wires each kind of instruction uses
USES = {
    "R": ["pc_imem", "instr_ctl", "instr_rf", "rf_a", "rf_b", "mux_alu", "alu_wb", "wb_rf", "pc_add4", "add4_pc",
          "pc_next"],
    "I": ["pc_imem", "instr_ctl", "instr_rf", "instr_imm", "rf_a", "imm_b", "mux_alu", "alu_wb", "wb_rf", "pc_add4",
          "add4_pc", "pc_next"],
    "load": ["pc_imem", "instr_ctl", "instr_rf", "instr_imm", "rf_a", "imm_b", "mux_alu", "alu_dmem", "dmem_wb",
             "wb_rf", "pc_add4", "add4_pc", "pc_next"],
    "store": ["pc_imem", "instr_ctl", "instr_rf", "instr_imm", "rf_a", "rf_b", "b_dmem", "imm_b", "mux_alu",
              "alu_dmem", "pc_add4", "add4_pc", "pc_next"],
    "branch": ["pc_imem", "instr_ctl", "instr_rf", "instr_imm", "rf_a", "rf_b", "mux_alu", "imm_t", "pc_t", "t_pc",
               "pc_add4", "add4_pc", "pc_next"],
    "jal": ["pc_imem", "instr_ctl", "instr_imm", "imm_t", "pc_t", "t_pc", "pc_add4", "link_wb", "wb_rf", "pc_next"],
}
