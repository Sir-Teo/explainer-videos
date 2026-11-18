from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load


class Dram(WatchScene):
    def construct(self):
        self.card()
        self.cell()
        self.leak()

    def card(self):
        self.chapter(11, r"Dynamic memory", r"How do you store a bit in one transistor?", lit=(1966, 1970), part=PART, said="Chapter eleven. Dynamic memory.")

    # ------------------------------------------------------------------
    def cell(self):
        head = label(r"One transistor, \ one capacitor", font_size=38).to_edge(UP, buff=0.35)
        bl = Line([-3.0, 2.2, 0], [-3.0, -2.2, 0], color=DATA, stroke_width=3)
        wl = Line([-4.2, 1.2, 0], [0.6, 1.2, 0], color=HEAD, stroke_width=3)
        tr = Square(0.5, color=HEAD, stroke_width=2.5).move_to([-1.6, 0.4, 0])
        links = VGroup(Line([-3.0, 0.4, 0], tr.get_left(), color=WIRE, stroke_width=2.5),
                       Line(tr.get_top(), [-1.6, 1.2, 0], color=HEAD, stroke_width=2.5),
                       Line(tr.get_right(), [-0.4, 0.4, 0], color=WIRE, stroke_width=2.5),
                       Line([-0.4, 0.4, 0], [-0.4, -0.3, 0], color=WIRE, stroke_width=2.5))
        cap = VGroup(Line([-0.9, -0.3, 0], [0.1, -0.3, 0], color=YES, stroke_width=5),
                     Line([-0.9, -0.55, 0], [0.1, -0.55, 0], color=YES, stroke_width=5),
                     Line([-0.4, -0.55, 0], [-0.4, -1.1, 0], color=WIRE, stroke_width=2.5))
        gnd = VGroup(*[Line([-0.4 - w, -1.1 - 0.1 * k, 0], [-0.4 + w, -1.1 - 0.1 * k, 0], color=WIRE, stroke_width=2)
                       for k, w in enumerate((0.3, 0.2, 0.1))])
        labs = VGroup(MathTex(r"\text{bit line}", font_size=22, color=DATA).next_to(bl, DOWN, buff=0.1),
                      MathTex(r"\text{word line}", font_size=22, color=HEAD).next_to(wl, LEFT, buff=0.1),
                      MathTex(r"C_s", font_size=26, color=YES).next_to(cap, LEFT, buff=0.15).shift(DOWN * 0.1),
                      MathTex(r"C_b", font_size=26, color=DATA).next_to(bl, LEFT, buff=0.15).shift(DOWN * 1.2))
        charge = VGroup(*[MathTex("+", font_size=34, color=YES).move_to([-0.8 + 0.16 * k, -0.12, 0]) for k in range(7)])
        spread = [[-3.0 + (0.18 if k % 2 else -0.18), 1.7 - 0.6 * k, 0] for k in range(7)]
        formula = MathTex(r"\Delta V = \frac{V_{dd}}{2}\cdot\frac{C_s}{C_s + C_b}", r"\approx 0.6\,\text{V}\times"
                          r"\frac{10\ \text{fF}}{110\ \text{fF}}", r"\approx 55\ \text{mV}", font_size=32,
                          color=HEAD).to_edge(DOWN, buff=0.45).shift(RIGHT * 1.2)
        notes = VGroup(
            label(r"the bit is charge on a tiny capacitor \\ (about 10 femtofarads)", font_size=22, color=YES),
            label(r"reading connects it to the much larger bit line: \\ the voltage moves by a small fraction of a "
                  r"volt, \\ and the stored level is disturbed", font_size=22, color=NO),
            label(r"so every read is destructive: \\ the sense amplifier writes the value back", font_size=22,
                  color=HEAD),
            label(r"Dennard: 1T1C idea, 1966; \\ Intel 1103: early 3T cell, 1970", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 1.4 + UP * 0.4, aligned_edge=LEFT)
        with self.voiceover(
            "In 1966 Robert Dennard at IBM found a much smaller way to store a bit. <bookmark mark='a'/> One "
            "transistor, used as a switch, and one capacitor. The bit is the charge on the capacitor: charged is "
            "one, empty is zero. <bookmark mark='b'/> To read it, raise the word line and connect the capacitor "
            "to the bit line. But the bit line is far larger than the cell, so the charge spreads out and moves "
            "its voltage by only a small fraction of a volt. A sense amplifier detects that. <bookmark mark='c'/> "
            "Reading has redistributed the cell's charge and disturbed its stored level, so the sense amplifier "
            "restores it immediately. This is dynamic RAM. Intel's successful 1103 appeared in 1970, using an "
            "early three-transistor cell. The one-transistor, one-capacitor cell became the dominant dense design "
            "later, as semiconductor memory displaced core."
        ) as vo:
            self.play(FadeIn(head), Create(bl), Create(wl), FadeIn(tr), Create(links), FadeIn(cap), FadeIn(gnd), FadeIn(labs), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Indicate(cap, scale_factor=1.05))
            self.play(LaggedStart(*[FadeIn(c, scale=1.5) for c in charge], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(wl.animate.set_stroke(width=6), tr.animate.set_fill(HEAD, 0.5))
            self.play(*[c.animate.move_to(p).set_opacity(0.7) for c, p in zip(charge, spread)], FadeIn(notes[1]),
                      run_time=1.6)
            self.play(Write(formula[0]))
            self.play(FadeIn(formula[1:]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(*[c.animate.move_to([-0.8 + 0.16 * k, -0.12, 0]).set_opacity(1) for k, c in enumerate(charge)],
                      run_time=1.2)
            self.play(wl.animate.set_stroke(width=3), tr.animate.set_fill(BG, 0), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def leak(self):
        self.ask(r"How often must DRAM rewrite every cell?", [r"every hour", r"every 64 milliseconds", r"never"], 1,
                 say="A DRAM cell's charge leaks away. How often must every cell be refreshed?",
                 reveal="At least every sixty-four milliseconds.")
        d = load("dram")
        t = np.array(d["t"]) * 1000
        head = label(r"The charge leaks away", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 256, 64], y_range=[0, 1.05, 0.5], x_length=8.4, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 1.6 + DOWN * 0.3)
        xl = note(r"milliseconds", font_size=20).next_to(ax, DOWN, buff=0.35)
        yl = note(r"charge \ (fraction of full)", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        thr = DashedLine(ax.c2p(0, d["threshold"]), ax.c2p(256, d["threshold"]), color=NO, stroke_width=2)
        tl = label(r"read as 0 below here", font_size=22, color=NO).next_to(ax.c2p(256, d["threshold"]), RIGHT, buff=0.1)
        no = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, d["v_no"])])
        ref = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, d["v_ref"])])
        nl = label(r"left alone", font_size=22, color=GREY_B).next_to(ax.c2p(200, float(np.exp(-0.2 / d['tau']))),
                                                                    DOWN, buff=0.1)
        rl = label(r"model: refreshed every 64 ms", font_size=24, color=YES).next_to(ax.c2p(150, 1.0), UP, buff=0.1)
        side = VGroup(label('refresh: internal row sensing \\\\ and charge restoration', font_size=24, color=GREY_A),
                      label('cost depends on device, \\\\ temperature and workload', font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.5)
        with self.voiceover(
            "There is a second problem. <bookmark mark='a'/> A capacitor that small is not perfectly isolated, "
            "and its charge leaks away, in a fraction of a second for the weakest cells. Left alone, a one would "
            "slowly turn into a zero. <bookmark mark='b'/> So the memory refreshes itself: the controller "
            "schedules refresh commands, and the chip's internal circuits sense and restore each row, on a fixed "
            "schedule, using sixty-four milliseconds as a common normal-temperature example. The required "
            "interval depends on device and temperature, and the charge is topped up long before it falls below "
            "the threshold. That is why it is called dynamic: the bits survive only because they are constantly "
            "rewritten, with time and energy costs that depend on the device, temperature and workload."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(thr), FadeIn(tl), Create(no), FadeIn(nl))
            vo.wait_until("a")
            self.play(Indicate(no, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(ref), FadeIn(rl), run_time=2.5)
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

