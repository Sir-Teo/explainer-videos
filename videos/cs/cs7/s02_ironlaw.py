from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load,
                                  mono)


class IronLaw(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.apply()
        self.myth()

    def card(self):
        card = chapter_card(1, r"The iron law", r"What does ``faster'' mean?", part=PART)
        with self.voiceover("Chapter one. The iron law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"Time, \ as a product of ratios", font_size=38).to_edge(UP, buff=0.35)
        eq1 = MathTex(r"\frac{\text{seconds}}{\text{program}}", r"=",
                      r"\frac{\text{instructions}}{\text{program}}", r"\times",
                      r"\frac{\text{cycles}}{\text{instruction}}", r"\times",
                      r"\frac{\text{seconds}}{\text{cycle}}", font_size=44).move_to(UP * 1.4)
        eq1[0].set_color(COST)
        eq1[2].set_color(CODE)
        eq1[4].set_color(YES)
        eq1[6].set_color(CLOCK)
        eq2 = MathTex(r"T", r"=", r"N", r"\times", r"\text{CPI}", r"\times", r"t_{\text{cycle}}", font_size=52).move_to(
            DOWN * 0.3)
        eq2[0].set_color(COST)
        eq2[2].set_color(CODE)
        eq2[4].set_color(YES)
        eq2[6].set_color(CLOCK)
        who = VGroup(
            label(r"$N$: \ the algorithm, \ the compiler, \ the instruction set", font_size=24, color=CODE),
            label(r"CPI: \ how the processor is organized \ (this part, \ and Parts 8--10)", font_size=24, color=YES),
            label(r"$t_{\text{cycle}}$: \ the circuits, \ and how the work is cut up", font_size=24, color=CLOCK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To make a computer faster we first need to say what faster means: less time to run a program. "
            "<bookmark mark='a'/> That time can be split into three ratios. The number of instructions the program "
            "executes. The average number of clock cycles each instruction takes. And the length of a cycle in "
            "seconds. Multiply them, and the instructions and the cycles cancel, leaving seconds per program. "
            "<bookmark mark='b'/> Architects write it as T equals N times CPI times the cycle time. The textbooks call it "
            "the processor performance equation; engineers call it the iron law. <bookmark mark='c'/> Its power is that the three "
            "factors belong to different people. N belongs to the algorithm, the compiler and the instruction set. "
            "CPI belongs to the organization of the processor. The cycle time belongs to the circuits, and to how the "
            "work of an instruction is divided up. Making one factor smaller often makes another larger, and the law "
            "keeps the accounts honest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq1), run_time=2.5)
            vo.wait_until("b")
            self.play(TransformMatchingTex(eq1.copy(), eq2), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w) for w in who], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def apply(self):
        il = load("ironlaw")
        st = load("stages")
        r1, r2 = il["rows"]["single"], il["rows"]["pipeline"]
        head = label(r"The Job's first chapter, \ two machines", font_size=36).to_edge(UP, buff=0.35)
        cols = [r"", r"$N$", r"CPI", r"$t_{\text{cycle}}$", r"$T$"]
        data = [
            (r"single cycle \ (Part 6)", fmt(r1["instructions"]), "1.00", rf"{r1['period_ps'] / 1000:.2f} ns",
             rf"{r1['seconds'] * 1e3:.2f} ms"),
            (r"five-stage pipeline", fmt(r2["instructions"]), rf"{r2['cpi']:.2f}", rf"{r2['period_ps'] / 1000:.2f} ns",
             rf"{r2['seconds'] * 1e3:.2f} ms"),
        ]
        xs = [-4.4, -1.4, 0.6, 2.4, 4.6]
        tab = VGroup()
        for i, row in enumerate([cols] + data):
            for j, t in enumerate(row):
                c = [GREY_B, CODE, YES, CLOCK, COST][j] if i == 0 else (GREY_A if j == 0 else [None, CODE, YES, CLOCK,
                                                                                               COST][j])
                m = label(t, font_size=26 if i else 24, color=c).move_to([xs[j], 1.6 - 0.75 * i, 0])
                tab.add(m)
        res = VGroup(
            label(rf"same $N$; \ CPI up from 1 to {r2['cpi']:.2f}; \ cycle {st['clock_ratio']:.2f} times shorter",
                  font_size=26, color=GREY_A),
            label(rf"net: \ {il['speedup']:.2f} times faster", font_size=32, color=HEAD),
            label(r"pipelining trades a little CPI for a lot of clock", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.4)
        with self.voiceover(
            "Here is the law applied to the machine of Part 6 and the one this part builds, both running the first "
            "chapter of Pride and Prejudice through the Job. <bookmark mark='a'/> The program is the same, so N is the "
            "same: eight hundred and twenty-seven thousand instructions. <bookmark mark='b'/> The single-cycle machine "
            "has a CPI of exactly one, and a cycle of two point six three nanoseconds. The pipeline's CPI rises to about "
            "one point two, because of the hazards this part is about, but its cycle shrinks to one point one three. "
            "<bookmark mark='c'/> Multiply out, and the pipeline is almost twice as fast. That is the whole bargain of "
            "pipelining: give up a little CPI to win a lot of clock."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[:5]), FadeIn(tab[5:7]), FadeIn(tab[10:12]))
            vo.wait_until("b")
            self.play(FadeIn(tab[7:10]))
            self.play(FadeIn(tab[12:15]))
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def myth(self):
        m = load("ironlaw")["myth"]
        a, b = m["subtract"], m["div"]
        head = label(r"The MIPS myth", font_size=38).to_edge(UP, buff=0.35)
        task = label(rf"print the numbers 1 to {fmt(load('ironlaw')['myth_numbers'])} in decimal", font_size=26,
                     color=GREY_A).next_to(head, DOWN, buff=0.3)
        cols = VGroup()
        for name, r, c in ((r"subtract powers of ten \\ (as the Job does)", a, DATA),
                           (r"divide by ten \\ (\texttt{div}, \texttt{rem})", b, FUNC)):
            items = VGroup(
                label(name, font_size=24, color=c),
                label(rf"{fmt(r['instructions'])} instructions", font_size=24, color=CODE),
                label(rf"CPI {r['cpi']:.2f}", font_size=24, color=YES),
                label(rf"{r['mips']:.0f} MIPS", font_size=30, color=HEAD),
                label(rf"{r['seconds'] * 1e3:.3f} ms", font_size=30, color=COST),
            ).arrange(DOWN, buff=0.22)
            cols.add(items)
        cols.arrange(RIGHT, buff=2.2).move_to(DOWN * 0.4)
        win = SurroundingRectangle(cols[1][4], buff=0.1, color=YES)
        lose = SurroundingRectangle(cols[0][3], buff=0.1, color=NO)
        moral = label(r"a higher MIPS rating \ and a slower program: \ only time is a measure of speed", font_size=24,
                      color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "For decades processors were sold by MIPS, millions of instructions per second, a number that leaves out "
            "the first factor of the law. Here is why that misleads. <bookmark mark='a'/> Two programs print the numbers "
            "from one to two thousand. One finds each digit by subtracting powers of ten, as the Job does. The other "
            "uses the divide instruction this part adds to Pebble. <bookmark mark='b'/> The subtracting program runs "
            "five times as many instructions, all of them simple, so it scores a splendid eight hundred MIPS. The "
            "dividing program runs few instructions, but each divide occupies the divider for sixteen cycles, so it "
            "scores barely two hundred and forty. <bookmark mark='c'/> And it finishes first. A program with fewer, "
            "slower instructions can beat one with many fast ones; only the time to run the program measures speed. "
            "Engineers took to calling MIPS a meaningless indicator of performance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(task), FadeIn(cols[0][0]), FadeIn(cols[1][0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in cols[0][1:4]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(x) for x in cols[1][1:4]], lag_ratio=0.3), run_time=2.4)
            self.play(Create(lose))
            vo.wait_until("c")
            self.play(FadeIn(cols[0][4]), FadeIn(cols[1][4]))
            self.play(Create(win), FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()
