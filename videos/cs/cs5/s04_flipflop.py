from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import seq as S
from videos.cs.cs5.common import (fsm_block, BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, WIRE, YES, gate, load,
                                  nand_latch, wave)


def box(w, h, text, color=CTRL, font_size=26):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class FlipFlop(VoiceoverScene):
    def construct(self):
        self.card()
        self.d_latch()
        self.edge()
        self.registers()

    def card(self):
        card = chapter_card(3, r"Latches, flip-flops \ and the clock", r"How do many bits change at the same moment?",
                            part=PART)
        with self.voiceover("Chapter three. Latches, flip-flops and the clock."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def d_latch(self):
        head = label(r"The D latch: \ a door for one bit", font_size=38).to_edge(UP, buff=0.35)
        T = 40
        E = [1 if (4 <= t < 14) or (26 <= t < 32) else 0 for t in range(T)]
        D = [1 if (2 <= t < 8) or (11 <= t < 20) or (22 <= t < 28) or (35 <= t < 38) else 0 for t in range(T)]
        h = S.d_latch().run(lambda t: {"D": D[t], "E": E[t]}, T,
                            init={"Dn": 1, "S_": 1, "R_": 1, "Q": 0, "Qn": 1})
        dx = 0.27
        ws = VGroup(wave(E, x0=-5.0, y=-0.6, dx=dx, color=CLOCK, name="E"),
                    wave(D, x0=-5.0, y=-1.5, dx=dx, color=DATA, name="D"),
                    wave(h["Q"], x0=-5.0, y=-2.4, dx=dx, color=YES, name="Q"))
        shades = VGroup(*[Rectangle(width=dx * (b - a), height=2.6, stroke_width=0, fill_color=CLOCK, fill_opacity=0.08)
                          .move_to([-5.0 + dx * (a + b) / 2, -1.3, 0]) for a, b in ((4, 14), (26, 32))])
        blk = VGroup(
            box(2.2, 1.0, r"\text{SR latch}", CTRL).move_to(RIGHT * 2.6 + UP * 1.5),
            MathTex(r"\bar S = \overline{D \cdot E}, \qquad \bar R = \overline{\bar D \cdot E}", font_size=30,
                    color=CODE).move_to(RIGHT * 2.6 + UP * 0.4))
        notes = VGroup(label(r"$E = 1$: \ transparent, \ $Q$ follows $D$", font_size=26, color=CLOCK),
                       label(r"$E = 0$: \ closed, \ $Q$ holds", font_size=26, color=YES),
                       label(r"stable Boolean inputs: mutually exclusive requests", font_size=22, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to(LEFT * 3.0 + UP * 1.5)
        with self.voiceover(
            "An SR latch needs two inputs and has a forbidden one. Gate the data and its complement into the set "
            "and reset inputs. <bookmark mark='a'/> Feed the latch from a data input D and an enable E, so that "
            "set is D and E, and reset is not D and E. <bookmark mark='b'/> While the enable is one, the latch is "
            "transparent: Q follows D, a few gate delays behind. While the enable is zero, the door is shut, and "
            "Q holds whatever D was at the moment it closed, no matter what D does afterwards. For stable Boolean "
            "inputs, those set and reset requests are mutually exclusive. Real transitions still have gate "
            "delays, and data must meet setup and hold around closing. This is the D latch, simulated here gate "
            "by gate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blk))
            vo.wait_until("a")
            self.play(Indicate(blk, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(shades), LaggedStart(*[Create(w) for w in ws], lag_ratio=0.2), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        d = load("latch")["ms"]
        head = label(r"The edge-triggered flip-flop", font_size=38).to_edge(UP, buff=0.35)
        m1 = box(2.0, 1.0, r"\text{master}", DATA).move_to(LEFT * 2.0 + UP * 1.6)
        m2 = box(2.0, 1.0, r"\text{slave}", YES).move_to(RIGHT * 1.6 + UP * 1.6)
        arr = Arrow(m1.get_right(), m2.get_left(), buff=0.1, stroke_width=3, color=WIRE)
        din = Arrow(m1.get_left() + LEFT * 1.0, m1.get_left(), buff=0, stroke_width=3, color=WIRE)
        qout = Arrow(m2.get_right(), m2.get_right() + RIGHT * 1.0, buff=0, stroke_width=3, color=WIRE)
        lbl = VGroup(MathTex("D", font_size=30, color=DATA).next_to(din, LEFT, buff=0.1),
                     MathTex("Q", font_size=30, color=YES).next_to(qout, RIGHT, buff=0.1),
                     label(r"open while clock low", font_size=20, color=GREY_B).next_to(m1, DOWN, buff=0.12),
                     label(r"open while clock high", font_size=20, color=GREY_B).next_to(m2, DOWN, buff=0.12))
        n = len(d["C"])
        dx = 11.0 / n
        x0 = -5.2
        ws = VGroup(wave(d["C"], x0=x0, y=-0.4, dx=dx, color=CLOCK, name=r"\text{clk}"),
                    wave(d["D"], x0=x0, y=-1.3, dx=dx, color=DATA, name="D"),
                    wave(d["M"], x0=x0, y=-2.2, dx=dx, color=GREY_B, name="M"),
                    wave(d["Q"], x0=x0, y=-3.1, dx=dx, color=YES, name="Q"))
        edges = VGroup(*[DashedLine([x0 + dx * t, 0.25, 0], [x0 + dx * t, -3.2, 0], color=CLOCK, stroke_width=1.5)
                         for t in range(1, n) if d["C"][t] and not d["C"][t - 1]])
        cap = label(r"$Q$ takes the value $D$ had at the rising edge, \ and holds it for a whole cycle", font_size=26,
                    color=HEAD).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "A latch is transparent for as long as its enable is high, and that is a problem when its output "
            "feeds logic that feeds back into its input: the signal can race round the loop many times while the "
            "door is open. <bookmark mark='a'/> The cure is two latches in a row, enabled by opposite phases of a "
            "clock. While the clock is low, the first, the master, follows D, and the second, the slave, holds. "
            "When the clock rises, the master shuts, capturing D, and the slave opens, passing the captured value "
            "to Q. <bookmark mark='b'/> In the ideal opposite-phase model, the two are not transparent together. "
            "Real designs must control phase overlap and satisfy their timing constraints. Here it is, simulated: "
            "With data stable around the sampling edge, Q takes the captured value after the rising edge. "
            "<bookmark mark='c'/> This is the edge-triggered D flip-flop, and it turns continuous time into "
            "discrete steps."
        ) as vo:
            race = fsm_block(0.9).move_to(UP * 0.4)
            race[6].become(MathTex(r"\text{latch: open}", font_size=22, color=NO).move_to(race.reg))
            race.reg.set_stroke(NO)
            rl = label(r"while the door is open, \ a value can race round the loop many times", font_size=24,
                       color=NO).next_to(race, DOWN, buff=0.45)
            self.play(FadeIn(head), FadeIn(race))
            for k in range(6):
                dot = Dot(race.reg.get_right(), radius=0.08, color=NO)
                self.add(dot)
                self.play(MoveAlongPath(dot, race.loop.copy()), run_time=0.45, rate_func=linear)
                self.remove(dot)
                if k == 1:
                    self.add(rl)
            vo.wait_until("a")
            self.play(FadeOut(race), FadeOut(rl))
            self.play(FadeIn(m1), FadeIn(m2), GrowArrow(arr), GrowArrow(din), GrowArrow(qout), FadeIn(lbl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(w) for w in ws], lag_ratio=0.2), run_time=3.0)
            self.play(Create(edges))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def registers(self):
        head = label(r"Registers, \ and the synchronous picture", font_size=36).to_edge(UP, buff=0.35)
        ffs = VGroup(*[box(0.7, 0.8, r"D\ Q", YES, 22) for _ in range(8)]).arrange(RIGHT, buff=0.15).move_to(UP * 1.6)
        clk = Line(ffs.get_corner(DL) + DOWN * 0.3, ffs.get_corner(DR) + DOWN * 0.3, color=CLOCK, stroke_width=3)
        taps = VGroup(*[Line(f.get_bottom(), [f.get_x(), clk.get_y(), 0], color=CLOCK, stroke_width=2) for f in ffs])
        cl = MathTex(r"\text{clk}", font_size=26, color=CLOCK).next_to(clk, LEFT, buff=0.15)
        rl = label(r"an 8-bit register: \ eight flip-flops, \ one clock", font_size=26, color=GREY_A).next_to(clk, DOWN,
                                                                                                         buff=0.3)
        # the synchronous loop: registers -> logic -> registers
        reg = box(1.8, 1.0, r"\text{registers}", YES).move_to(LEFT * 3.0 + DOWN * 1.8)
        logic = box(3.0, 1.0, r"\text{combinational logic}", CTRL).move_to(RIGHT * 1.2 + DOWN * 1.8)
        a1 = Arrow(reg.get_right(), logic.get_left(), buff=0.1, color=WIRE, stroke_width=3)
        back = CurvedArrow(logic.get_bottom() + DOWN * 0.05, reg.get_bottom() + DOWN * 0.05, angle=-1.2, color=WIRE,
                           stroke_width=3)
        ins = Arrow(logic.get_top() + UP * 0.7, logic.get_top(), buff=0, color=DATA, stroke_width=3)
        il = label(r"inputs", font_size=22, color=DATA).next_to(ins, UP, buff=0.05)
        rule = label(r"next state $=$ logic(state, inputs), \ loaded at every rising edge", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Put flip-flops side by side on the same clock and you have a register. <bookmark mark='a'/> Eight "
            "flip-flops make an eight-bit register; each bit samples on the same rising edge and its output "
            "settles after its clock-to-Q delay. <bookmark mark='b'/> Now the shape of almost every digital "
            "system: registers hold the state; combinational logic, the circuits of Parts 3 and 4, computes the "
            "next state from the current state and the inputs; and at each clock edge the registers load it. "
            "Between edges the combinational outputs may glitch, but the values sampled by registers must settle "
            "for their setup and hold windows. Outputs used asynchronously need separate care. <bookmark "
            "mark='c'/> This series' hardware library simulates exactly this picture, one clock cycle at a time, "
            "and Pebble is built in it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ffs), Create(clk), Create(taps), FadeIn(cl), FadeIn(rl))
            vo.wait_until("a")
            self.play(Indicate(ffs, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(reg), FadeIn(logic), GrowArrow(a1), Create(back), GrowArrow(ins), FadeIn(il))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()
