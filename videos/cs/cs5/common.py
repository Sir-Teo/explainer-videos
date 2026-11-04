"""Helpers shared by the scenes of Part 5 ("Memory and Time")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.gates import GATE_FILL, GATE_STROKE, ONE, WIRE, ZERO, gate, junction, wire  # noqa: F401

from .compute import load  # noqa: F401

PART = 5

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


def wave(values, x0=-5.0, y=0.0, dx=0.25, h=0.45, color=DATA, name="", font_size=26, stroke=3) -> VGroup:
    """A digital waveform: ``values`` are 0/1 per tick, drawn as a step line from x0 with height h."""
    pts = []
    for i, v in enumerate(values):
        yy = y + (h if v else 0)
        pts += [[x0 + dx * i, yy, 0], [x0 + dx * (i + 1), yy, 0]]
    line = VMobject(color=color, stroke_width=stroke).set_points_as_corners([np.array(p, float) for p in pts])
    g = VGroup(line)
    if name:
        g.add(MathTex(name, font_size=font_size, color=color).next_to([x0, y + h / 2, 0], LEFT, buff=0.25))
    g.line = line
    return g


def nand_latch(scale=1.0, labels=("\\bar S", "\\bar R")):
    """Two cross-coupled NAND gates, drawn: g.Q and g.Qn are the output pins, g.S and g.R the free inputs."""
    g1 = gate("NAND", size=0.9 * scale).move_to(UP * 0.8 * scale)
    g2 = gate("NAND", size=0.9 * scale).move_to(DOWN * 0.8 * scale)

    def cross(o, i, dy):
        pts = [o, o + RIGHT * 0.35 * scale, [o[0] + 0.35 * scale, dy, 0], [i[0] - 0.35 * scale, -dy, 0],
               [i[0] - 0.35 * scale, i[1], 0], i]
        return VMobject(color=WIRE, stroke_width=3).set_points_as_corners([np.asarray(p, float) for p in pts])

    w1 = cross(g1.out(), g2.inp[0](), 0.25 * scale)
    w2 = cross(g2.out(), g1.inp[1](), -0.25 * scale)
    s_in = Line(g1.inp[0]() + LEFT * 0.8 * scale, g1.inp[0](), color=WIRE, stroke_width=3)
    r_in = Line(g2.inp[1]() + LEFT * 0.8 * scale, g2.inp[1](), color=WIRE, stroke_width=3)
    q_out = Line(g1.out(), g1.out() + RIGHT * 0.9 * scale, color=WIRE, stroke_width=3)
    qn_out = Line(g2.out(), g2.out() + RIGHT * 0.9 * scale, color=WIRE, stroke_width=3)
    labs = VGroup(MathTex(labels[0], font_size=30, color=DATA).next_to(s_in, LEFT, buff=0.1),
                  MathTex(labels[1], font_size=30, color=DATA).next_to(r_in, LEFT, buff=0.1),
                  MathTex("Q", font_size=30, color=YES).next_to(q_out, RIGHT, buff=0.1),
                  MathTex("\\bar Q", font_size=30, color=YES).next_to(qn_out, RIGHT, buff=0.1))
    g = VGroup(g1, g2, w1, w2, s_in, r_in, q_out, qn_out, labs)
    g.g1, g.g2, g.w1, g.w2, g.s_in, g.r_in, g.q_out, g.qn_out, g.labs = g1, g2, w1, w2, s_in, r_in, q_out, qn_out, labs
    return g


def fsm_block(scale=1.0) -> VGroup:
    """The shape of every synchronous system: a state register, combinational logic, and the loop between them.

    Returns a VGroup with attributes reg, logic, loop (the path a token takes once round per tick), clk and labels.
    """
    s = scale
    reg = RoundedRectangle(width=1.5 * s, height=0.9 * s, corner_radius=0.08, stroke_color=YES, stroke_width=2.4,
                           fill_color=BG, fill_opacity=1).move_to(LEFT * 2.2 * s)
    rl = MathTex(r"\text{register}", font_size=24 * s, color=YES).move_to(reg)
    logic = Ellipse(width=2.8 * s, height=1.3 * s, stroke_color=CTRL, stroke_width=2.4, fill_color=BG,
                    fill_opacity=1).move_to(RIGHT * 1.4 * s)
    ll = VGroup(MathTex(r"\text{combinational}", font_size=22 * s, color=CTRL),
                MathTex(r"\text{logic}", font_size=22 * s, color=CTRL)).arrange(DOWN, buff=0.08).move_to(logic)
    fwd = Arrow(reg.get_right(), logic.get_left(), buff=0.05, color=WIRE, stroke_width=3)
    top = 1.1 * s
    back = VMobject(color=WIRE, stroke_width=3).set_points_as_corners([
        logic.get_right(), logic.get_right() + RIGHT * 0.5 * s, [logic.get_right()[0] + 0.5 * s, top, 0],
        [reg.get_left()[0] - 0.5 * s, top, 0], [reg.get_left()[0] - 0.5 * s, 0, 0], reg.get_left()])
    tip = Triangle(color=WIRE, fill_opacity=1, stroke_width=0).scale(0.08 * s).rotate(-PI / 2).move_to(
        reg.get_left() + LEFT * 0.08 * s)
    inp = Arrow(logic.get_bottom() + DOWN * 0.7 * s + LEFT * 0.5 * s, logic.get_bottom() + LEFT * 0.5 * s, buff=0.02,
                color=DATA, stroke_width=3)
    out = Arrow(logic.get_bottom() + RIGHT * 0.5 * s, logic.get_bottom() + DOWN * 0.7 * s + RIGHT * 0.5 * s, buff=0.02,
                color=YES, stroke_width=3)
    il = MathTex(r"\text{inputs}", font_size=20 * s, color=DATA).next_to(inp.get_start(), DOWN, buff=0.08)
    ol = MathTex(r"\text{outputs}", font_size=20 * s, color=YES).next_to(out.get_end(), DOWN, buff=0.08)
    clk = wave([0, 1, 0, 1, 0, 1, 0], x0=reg.get_left()[0] - 0.2 * s, y=reg.get_bottom()[1] - 0.95 * s, dx=0.25 * s,
               h=0.3 * s, color=CLOCK)
    cl = MathTex(r"\text{clk}", font_size=20 * s, color=CLOCK).next_to(clk, LEFT, buff=0.12)
    clw = DashedLine(clk.get_top() + RIGHT * 0.0, reg.get_bottom(), color=CLOCK, stroke_width=1.5).move_to(
        [reg.get_center()[0], (clk.get_top()[1] + reg.get_bottom()[1]) / 2, 0])
    loop = VMobject().set_points_as_corners([reg.get_right(), logic.get_left(), logic.get_right(),
                                            logic.get_right() + RIGHT * 0.5 * s,
                                            [logic.get_right()[0] + 0.5 * s, top, 0],
                                            [reg.get_left()[0] - 0.5 * s, top, 0],
                                            [reg.get_left()[0] - 0.5 * s, 0, 0], reg.get_left()])
    g = VGroup(back, tip, fwd, inp, out, reg, rl, logic, ll, il, ol, clw, clk, cl)
    g.reg, g.logic, g.loop, g.clk = reg, logic, loop, clk
    return g


def tick_tokens(scene, block, ticks=3, run_time=1.2):
    """Send a token once round the block's loop per clock tick, flashing the register at each edge."""
    for _ in range(ticks):
        dot = Dot(block.reg.get_right(), radius=0.08, color=HEAD)
        scene.add(dot)
        scene.play(MoveAlongPath(dot, block.loop.copy()), run_time=run_time, rate_func=linear)
        scene.play(Indicate(block.reg, color=HEAD, scale_factor=1.06), FadeOut(dot), run_time=0.35)
