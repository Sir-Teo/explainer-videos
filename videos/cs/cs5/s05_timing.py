from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load, wave


def box(w, h, text, color=CTRL, font_size=26):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class Timing(VoiceoverScene):
    def construct(self):
        self.card()
        self.windows()
        self.fmax()
        self.skew()

    def card(self):
        card = chapter_card(4, r"How fast can the clock go?", r"What sets the length of a clock cycle?", part=PART)
        with self.voiceover("Chapter four. How fast can the clock go?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def windows(self):
        head = label(r"Setup, \ hold, \ and clock-to-Q", font_size=38).to_edge(UP, buff=0.35)
        x0, dx = -5.0, 0.25
        clk = [0] * 10 + [1] * 14 + [0] * 16
        w_clk = wave(clk, x0=x0, y=1.3, dx=dx, color=CLOCK, name=r"\text{clk}", h=0.6)
        edge_x = x0 + dx * 10
        dline = DashedLine([edge_x, 2.2, 0], [edge_x, -2.2, 0], color=CLOCK, stroke_width=2)
        su = Rectangle(width=dx * 4, height=0.7, stroke_width=0, fill_color=NO, fill_opacity=0.35).move_to(
            [edge_x - dx * 2, 0.05, 0])
        ho = Rectangle(width=dx * 2, height=0.7, stroke_width=0, fill_color=NO, fill_opacity=0.35).move_to(
            [edge_x + dx, 0.05, 0])
        D = [0] * 3 + [1] * 30 + [0] * 7
        w_d = wave(D, x0=x0, y=-0.3, dx=dx, color=DATA, name="D", h=0.6)
        Q = [0] * 13 + [1] * 27
        w_q = wave(Q, x0=x0, y=-1.8, dx=dx, color=YES, name="Q", h=0.6)
        labs = VGroup(
            label(r"setup: \ steady \textit{before} the edge", font_size=22, color=NO).move_to([edge_x - 2.4, 0.75, 0]),
            label(r"hold: \ and just \textit{after}", font_size=22, color=NO).next_to(ho, DOWN, buff=0.15).shift(RIGHT * 1.2),
            BraceBetweenPoints([edge_x, -2.0, 0], [x0 + dx * 13, -2.0, 0], direction=DOWN, color=GREY_B),
        )
        tcq = MathTex(r"t_{cq}", font_size=26, color=GREY_A).next_to(labs[2], DOWN, buff=0.08)
        rules = VGroup(label(r"$t_{setup}$, \ $t_{hold}$: \ the window where $D$ must not move", font_size=26,
                             color=GREY_A),
                       label(r"$t_{cq}$: \ how long after the edge $Q$ shows the new value", font_size=26,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A flip-flop makes a promise, but only if it is treated well. <bookmark mark='a'/> Around each rising "
            "edge there is a small window. D must be steady for a short time before the edge, the setup time, and "
            "for a short time after it, the hold time. Inside the window, the flip-flop's master latch is in the "
            "middle of closing, and a change there is exactly the balanced push that can leave it on the saddle. "
            "<bookmark mark='b'/> And the flip-flop is not instant either: the new value appears at Q a little after "
            "the edge, the clock-to-Q delay. These three numbers, from the datasheet of every flip-flop, set the "
            "speed limit of a whole processor."
        ) as vo:
            self.play(FadeIn(head), Create(w_clk), Create(dline))
            vo.wait_until("a")
            self.play(Create(w_d), FadeIn(su), FadeIn(ho), FadeIn(labs[0]), FadeIn(labs[1]), FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(Create(w_q), FadeIn(labs[2]), FadeIn(tcq), FadeIn(rules[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fmax(self):
        head = label(r"The cycle has to hold the slowest path", font_size=36).to_edge(UP, buff=0.35)
        r1 = box(1.4, 1.0, r"\text{reg}", YES).move_to(LEFT * 4.6 + UP * 1.6)
        lg = box(3.2, 1.0, r"\text{logic}", CTRL).move_to(LEFT * 0.6 + UP * 1.6)
        r2 = box(1.4, 1.0, r"\text{reg}", YES).move_to(RIGHT * 3.4 + UP * 1.6)
        a1 = Arrow(r1.get_right(), lg.get_left(), buff=0.08, color=WIRE, stroke_width=3)
        a2 = Arrow(lg.get_right(), r2.get_left(), buff=0.08, color=WIRE, stroke_width=3)
        # the budget bar
        parts = [(r"t_{cq}", 0.9, GREY_B), (r"t_{logic}", 5.2, CTRL), (r"t_{setup}", 0.9, NO)]
        bar = VGroup()
        x = -4.6
        for t, w, c in parts:
            r = Rectangle(width=w, height=0.6, stroke_color=BG, stroke_width=1, fill_color=c, fill_opacity=0.75)
            r.move_to([x + w / 2, -0.2, 0])
            bar.add(VGroup(r, MathTex(t, font_size=28, color=WHITE).move_to(r)))
            x += w
        period = BraceBetweenPoints([-4.6, -0.6, 0], [x, -0.6, 0], direction=DOWN, color=CLOCK)
        pl = MathTex(r"T_{clk}", font_size=30, color=CLOCK).next_to(period, DOWN, buff=0.1)
        f = MathTex(r"f_{max} = \frac{1}{t_{cq} + t_{logic,\,max} + t_{setup}}", font_size=40, color=HEAD).move_to(
            DOWN * 2.2 + LEFT * 2.5)
        ex = VGroup(label(r"Pebble's ALU: \ 29 gate delays $\times$ 10 ps \ $=$ 290 ps", font_size=24, color=GREY_A),
                    label(r"$+$ 40 ps $t_{cq}$ $+$ 30 ps $t_{setup}$ \ $=$ 360 ps", font_size=24, color=GREY_A),
                    label(r"$\Rightarrow$ \ at most about 2.8 GHz", font_size=28, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 3.6 + DOWN * 2.1)
        with self.voiceover(
            "Now the clock. <bookmark mark='a'/> Between two registers sits some combinational logic. At a rising "
            "edge, the first register launches new values; they appear after the clock-to-Q delay, ripple through the "
            "logic, and must arrive at the second register at least a setup time before the next edge. "
            "<bookmark mark='b'/> So one clock period has to hold three things end to end: clock-to-Q, the slowest "
            "path through the logic, and the setup time. The fastest clock the circuit can take is one over their "
            "sum. <bookmark mark='c'/> Put Pebble's ALU between two registers: twenty-nine gate delays, at about ten "
            "picoseconds each, plus the flip-flops' own overheads, comes to three hundred and sixty picoseconds, a "
            "clock of at most about two point eight gigahertz. Every gate delay saved in Part 4 shows up here, and Part "
            "7 will cut the path into pieces to go faster still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(r1), FadeIn(lg), FadeIn(r2), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(period), FadeIn(pl), Write(f))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def skew(self):
        head = label(r"Clock skew, \ and the bug a slower clock cannot fix", font_size=34).to_edge(UP, buff=0.35)
        setup = MathTex(r"\text{setup: } \ t_{cq} + t_{logic,\,max} + t_{setup} \le T_{clk} + \delta", font_size=34,
                        color=GREY_A).move_to(UP * 2.2)
        hold = MathTex(r"\text{hold: } \ t_{cq} + t_{logic,\,min} \ge t_{hold} + \delta", font_size=34,
                       color=NO).next_to(setup, DOWN, buff=0.3)
        d = label(r"$\delta$: \ how much later the clock reaches the second register", font_size=24,
                  color=CLOCK).next_to(hold, DOWN, buff=0.3)
        pts = VGroup(
            label(r"a setup violation: \ slow the clock down, \ and it goes away", font_size=26, color=YES),
            label(r"a hold violation: \ $T_{clk}$ is not in the inequality, \ so no clock is slow enough", font_size=26,
                  color=NO),
            label(r"chip tools fix hold problems by \textit{adding} delay to short paths, \ and balance the clock tree "
                  r"\\ so that $\delta$ is a few picoseconds across a whole chip", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(DOWN, buff=0.3)
        sk = 2
        c1 = [0] * 6 + [1] * 8 + [0] * 8
        c2 = [0] * (6 + sk) + [1] * 8 + [0] * (8 - sk)
        w1 = wave(c1, x0=-2.6, y=-0.1, dx=0.3, h=0.4, color=CLOCK, name=r"\text{clk at reg 1}", font_size=22)
        w2 = wave(c2, x0=-2.6, y=-0.85, dx=0.3, h=0.4, color=CLOCK, name=r"\text{clk at reg 2}", font_size=22)
        e1, e2 = -2.6 + 0.3 * 6, -2.6 + 0.3 * (6 + sk)
        guide = VGroup(DashedLine([e1, 0.4, 0], [e1, -0.95, 0], color=GREY_C, stroke_width=1.5),
                       DashedLine([e2, 0.4, 0], [e2, -0.95, 0], color=GREY_C, stroke_width=1.5))
        br = BraceBetweenPoints([e1, -0.95, 0], [e2, -0.95, 0], direction=DOWN, color=CLOCK, buff=0.05)
        bl = MathTex(r"\delta", font_size=26, color=CLOCK).next_to(br, DOWN, buff=0.05)
        with self.voiceover(
            "One more effect, because a clock signal is a wire too. <bookmark mark='a'/> It reaches different "
            "registers at slightly different times; call the difference delta, the clock skew. A late clock at the "
            "second register gives the data more time to arrive, which helps the setup inequality. "
            "<bookmark mark='b'/> But it hurts the second one, the hold condition: the fastest path from the first "
            "register must not change the second register's input before that register has finished capturing its "
            "old value. <bookmark mark='c'/> Notice what is missing from that inequality: the clock period. A setup "
            "violation can always be cured by running the clock slower. A hold violation cannot; the chip is broken "
            "at any speed. So design tools insert extra delay into paths that are too fast, and engineers build "
            "balanced trees of wires that deliver the clock to billions of transistors within a few picoseconds of "
            "each other."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(w1), Create(w2), run_time=1.5)
            self.play(Create(guide), GrowFromCenter(br), FadeIn(bl))
            self.play(FadeIn(d), Write(setup))
            vo.wait_until("b")
            self.play(Write(hold))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4), run_time=2.4)
        self.wait(0.3)
        self.clear_scene()
