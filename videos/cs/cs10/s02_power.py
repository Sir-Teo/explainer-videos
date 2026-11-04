from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, grid_table, load)


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.dennard()
        self.end()
        self.cores()
        self.dark()

    def card(self):
        card = chapter_card(1, r"The power wall", r"Why did the clock stop getting faster?", lit=(1974, 2005),
                            extra=((1974, r"Dennard scaling"), (2005, r"the first dual cores")), part=PART)
        with self.voiceover("Chapter one. The power wall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def formula(self):
        head = label(r"Where a chip's power goes", font_size=36).to_edge(UP, buff=0.35)
        eq = MathTex(r"P", r"\;=\;", r"\alpha", r"\,", r"C", r"\,", r"V^2", r"\,", r"f", r"\;+\;", r"V I_{\text{leak}}",
                     font_size=60).shift(UP * 1.2)
        parts = [(2, r"$\alpha$: \ the fraction of transistors switching each cycle", GREY_A),
                 (4, r"$C$: \ the capacitance each switch charges and discharges", DATA),
                 (6, r"$V$: \ the supply voltage, \ squared", NO),
                 (8, r"$f$: \ the clock frequency", CTRL),
                 (10, r"leakage: \ current that flows even when nothing switches", FUNC)]
        notes = VGroup(*[label(t, font_size=23, color=c) for _, t, c in parts]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.22)
        notes.next_to(eq, DOWN, buff=0.55)
        why = note(r"every switch moves charge $CV$ through a voltage $V$: \ energy $CV^2$ per cycle, \ $f$ cycles a "
                   r"second", font_size=19).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where does a chip's power go? Mostly into one formula. <bookmark mark='a'/> Each time a transistor "
            "switches, it charges or discharges a tiny capacitance C through the supply voltage V, and that costs "
            "energy C V squared. <bookmark mark='b'/> A fraction alpha of the transistors switch each cycle, "
            "<bookmark mark='c'/> and there are f cycles a second. So the dynamic power is alpha C V squared f. "
            "<bookmark mark='d'/> On top of that is leakage: transistors are not perfect switches, and some current "
            "flows through them even when they are off. Remember the V squared, and remember leakage; between them "
            "they stopped the clock."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]), Indicate(eq[4]), Indicate(eq[6]), FadeIn(why))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), Indicate(eq[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]), Indicate(eq[8]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]), Indicate(eq[10]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dennard(self):
        head = label(r"Dennard scaling \ (1974): \ shrink everything by $\kappa$", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"length, \ width, \ oxide", r"$1/\kappa$"], [r"voltage $V$", r"$1/\kappa$"],
                [r"capacitance $C$", r"$1/\kappa$"], [r"clock $f$", r"$\kappa$"],
                [r"power per transistor \ $CV^2f$", r"$1/\kappa^2$"], [r"transistors per area", r"$\kappa^2$"],
                [r"power per area", r"$1$"]]
        colors = [[GREY_A, GREY_A]] * 4 + [[GREY_A, YES], [GREY_A, DATA], [HEAD, HEAD]]
        t = grid_table([r"quantity", r"scales by"], rows, [5.0, 2.2], row_h=0.5, font_size=24, colors=colors,
                       mono_cols=()).move_to(LEFT * 1.6 + DOWN * 0.3)
        k = label(r"$\kappa \approx 1.4$ \ a generation: \ twice the transistors, \ 40\% faster, \ the same power "
                  r"per area", font_size=24, color=YES).to_edge(DOWN, buff=0.45)
        side = VGroup(label(r"Robert Dennard \\ and colleagues, \ IBM", font_size=22, color=GREY_B),
                      label(r"the free lunch: \\ every new chip faster, \\ at the same watts", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(t, RIGHT, buff=0.6)
        with self.voiceover(
            "In 1974 Robert Dennard and his colleagues at IBM worked out what happens when you shrink a transistor. "
            "Scale every dimension down by a factor kappa. <bookmark mark='a'/> Scale the voltage down by the same "
            "factor, so the electric fields inside stay the same. Then the capacitance falls by kappa too, and the "
            "transistor switches kappa times faster, so the clock can rise by kappa. <bookmark mark='b'/> Put those "
            "into the formula: the power of one transistor falls by kappa squared. <bookmark mark='c'/> But kappa "
            "squared as many fit in the same area. So the power per square millimetre stays exactly the same. "
            "<bookmark mark='d'/> With kappa about one point four each generation, every two years brought twice the "
            "transistors, running forty percent faster, for the same power. For thirty years, programs got faster "
            "without anyone changing them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t.cells[0][0]), FadeIn(t.cells[0][1]), FadeIn(t.rule), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in (1, 2, 3, 4)], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[5])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*t.cells[6])))
            self.play(FadeIn(VGroup(*t.cells[7])))
            vo.wait_until("d")
            self.play(FadeIn(k), FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def end(self):
        head = label(r"Why it ended", font_size=36).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 1.0, 0.25], y_range=[0, 9, 3], x_length=5.0, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.4)
        # subthreshold leakage: I ~ exp((Vgs - Vth) / (n kT/q)), about a decade per 100 mV at room temperature;
        # above the threshold the transistor is on (drawn flat, schematically)
        curve = ax.plot(lambda v: max(0.0, 9 + (v - 0.75) / 0.1) if v < 0.75 else 9.0, x_range=[0, 1.0],
                        color=FUNC, stroke_width=3)
        xl = label(r"gate voltage \ (V)", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"current \ (log)", font_size=18, color=GREY_B).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        vth = DashedLine(ax.c2p(0.75, 0), ax.c2p(0.75, 9), color=HEAD, stroke_width=2)
        vl = label(r"$V_{\text{th}}$", font_size=20, color=HEAD).next_to(vth, UP, buff=0.05)
        cap = note(r"below the threshold, \ current falls only tenfold \ per 60 to 100 mV \ (at room temperature)",
                   font_size=17).next_to(ax, DOWN, buff=0.6)
        pts = VGroup(
            label(r"to switch fast, \ $V$ must stay well above the threshold $V_{\text{th}}$", font_size=22,
                  color=GREY_A),
            label(r"lower $V_{\text{th}}$ \ $\to$ \ exponentially more leakage", font_size=22, color=FUNC),
            label(r"so from about 2005 \ $V$ stopped falling, \ near 1 volt", font_size=22, color=NO),
            label(r"then each generation: \ power per area $\times\,\kappa^2$ \ if the clock still rose", font_size=22,
                  color=NO),
            label(r"a chip can shed about 100 W: \ the clock had to stop", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.8).shift(UP * 0.3)
        with self.voiceover(
            "Why did it end? Because the voltage stopped falling. <bookmark mark='a'/> A transistor switches fast "
            "only if the supply voltage is well above its threshold voltage, the point where it turns on. So to lower "
            "V, you must lower the threshold too. <bookmark mark='b'/> But below its threshold a transistor is not "
            "quite off: the current through it falls only tenfold for every sixty to a hundred millivolts, a limit "
            "set by the thermal energy of electrons at room temperature. Lower the threshold, and leakage grows exponentially. "
            "<bookmark mark='c'/> By about 2005 supply voltages had settled near one volt, and they have barely moved "
            "since. <bookmark mark='d'/> With the voltage fixed, the formula turns against you: each generation packs "
            "twice the transistors into the same area, and if the clock still rose, the power per area would grow. "
            "<bookmark mark='e'/> A chip can only shed about a hundred watts of heat before it needs exotic cooling. "
            "So the clock stopped."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), Create(vth), FadeIn(vl), FadeIn(cap))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cores(self):
        head = label(r"Two slower cores \ beat one fast one", font_size=36).to_edge(UP, buff=0.35)
        eq = MathTex(r"f \propto V \quad\Longrightarrow\quad P \propto V^2 f \propto f^3", font_size=40,
                     color=HEAD).next_to(head, DOWN, buff=0.35)
        vals = [1.0, 1.0, 2 * 0.8 ** 3, 1.6]
        ch = bar_chart(vals, [r"one core \ power", r"one core \ speed", r"two at $0.8f$ \ power",
                              r"two at $0.8f$ \ speed"], [CTRL, YES, CTRL, YES], height=2.6, bar_w=1.0, gap=0.9,
                       font_size=20, fmt_=lambda v: f"{v:.2f}").move_to(DOWN * 0.7)
        punch = label(r"the same power, \ 60\% more work \ (if the work can be split)", font_size=26,
                      color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the industry turned the formula around. <bookmark mark='a'/> Within the range where a chip works, the "
            "highest clock it can run is roughly proportional to its voltage. So lowering both together cuts power "
            "with the cube of the clock. <bookmark mark='b'/> Take one core at full speed: one unit of power, one "
            "unit of work a second. <bookmark mark='c'/> Now two cores, each at eighty percent of the clock and "
            "voltage: each draws point eight cubed, about half the power, so the pair draws about the same as the one. "
            "But together they do one point six units of work. <bookmark mark='d'/> Sixty percent more, for the same "
            "watts, with one condition that changes everything: the work has to be divided between them. In 2005 "
            "both Intel and AMD shipped their first dual-core processors, and the rest of this part is about that "
            "condition."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ch[0]), *[GrowFromEdge(ch.bars[k], DOWN) for k in (0, 1)],
                      *[FadeIn(ch.vals[k]) for k in (0, 1)], *[FadeIn(ch.names[k]) for k in (0, 1)])
            vo.wait_until("c")
            self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in (2, 3)], *[FadeIn(ch.vals[k]) for k in (2, 3)],
                      *[FadeIn(ch.names[k]) for k in (2, 3)])
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dark(self):
        fr = load("frontier")["dark"]
        head = label(r"Dark silicon", font_size=36).to_edge(UP, buff=0.35)
        gens = fr["generations"]
        grids = VGroup()
        for g in (0, 2, 4, 6):
            n = 2 ** (g // 2 + 2)  # cells per side grows: transistors double each generation
            lit = fr["lit"][g]
            cells = VGroup()
            side = 2.0 / n
            on = int(round(lit * n * n))
            for k in range(n * n):
                cells.add(Square(side_length=side * 0.9, stroke_width=0,
                                 fill_color=YES if k < on else GREY_E, fill_opacity=0.9 if k < on else 0.6).move_to(
                    [(k % n) * side, -(k // n) * side, 0]))
            cap = label(rf"generation {g}: \ {100 * lit:.0f}\% lit", font_size=18, color=YES if lit > 0.4 else NO)
            grids.add(VGroup(cells, cap.next_to(cells, DOWN, buff=0.15)))
        grids.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        model = note(r"a toy model: \ twice the transistors each generation, \ energy per switch down only "
                     r"$1.4\times$, \ a fixed power budget", font_size=18).next_to(grids, DOWN, buff=0.35)
        cite = label(r"Esmaeilzadeh et al., \ 2011: \ at 8 nm, \ more than half of a chip must be dark at any moment",
                     font_size=22, color=HEAD).next_to(model, DOWN, buff=0.35)
        ans = label(r"the answer since: \ specialized circuits that are dark until needed \ (Part 60)", font_size=22,
                    color=DATA).next_to(cite, DOWN, buff=0.25)
        with self.voiceover(
            "And even more cores only postpone the problem. <bookmark mark='a'/> Each generation still doubles the "
            "transistors in the same area, but with the voltage stuck, the energy of one switch falls by only about "
            "forty percent. With a fixed power budget, the fraction of the chip that can switch at full speed shrinks "
            "every generation: half after two generations, a quarter after four, an eighth after six. The rest must "
            "stay dark. <bookmark "
            "mark='b'/> In 2011 Hadi Esmaeilzadeh and his colleagues estimated that at eight nanometres, more than "
            "half of a chip would have to be unpowered at any moment. <bookmark mark='c'/> The response has been "
            "specialization: chips full of circuits for one job each, video, encryption, matrix multiplication, which "
            "sit dark until their job comes. That is the story of Part 60. This part is about the general-purpose "
            "answer: many cores, and how to use them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grids], lag_ratio=0.5), FadeIn(model), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(cite))
            vo.wait_until("c")
            self.play(FadeIn(ans))
        self.wait(0.3)
        self.clear_scene()
