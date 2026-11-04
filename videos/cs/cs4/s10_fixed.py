from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, bit_cells, load


class Fixed(VoiceoverScene):
    def construct(self):
        self.card()
        self.qformat()
        self.money()
        self.range_()

    def card(self):
        card = chapter_card(9, r"Fixed point", r"How do integers hold fractions?", part=PART)
        with self.voiceover("Chapter nine. Fixed point."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def qformat(self):
        head = label(r"A binary point, \ in a fixed place", font_size=38).to_edge(UP, buff=0.35)
        bits = "01011010"
        cells = bit_cells(bits, cell=0.6, font_size=36).move_to(UP * 1.4)
        point = Dot(radius=0.07, color=HEAD).move_to((cells[3].get_right() + cells[4].get_left()) / 2 + DOWN * 0.28)
        w = VGroup(*[MathTex(t, font_size=24, color=GREY_B).next_to(cells[i], UP, buff=0.15)
                     for i, t in enumerate([r"8", r"4", r"2", r"1", r"\tfrac12", r"\tfrac14", r"\tfrac18", r"\tfrac1{16}"])])
        val = MathTex(r"0101.1010_2 = 4 + 1 + \tfrac12 + \tfrac18 = 5.625 = \tfrac{90}{16}", font_size=38,
                      color=YES).move_to(UP * 0.0)
        rules = VGroup(
            MathTex(r"Q4.4: \quad x = \frac{\text{an 8-bit integer}}{2^4}", font_size=34, color=CODE),
            label(r"add and subtract: \ exactly integer arithmetic", font_size=26, color=GREY_A),
            MathTex(r"\text{multiply: } \frac{A}{2^4} \cdot \frac{B}{2^4} = \frac{A B / 2^4}{2^4} \ \Rightarrow "
                    r"\text{ multiply the integers, shift right by } 4", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 1.9)
        with self.voiceover(
            "The integer hardware we have built can hold fractions, with one agreement. <bookmark mark='a'/> Decide "
            "that the binary point sits in a fixed place, say four bits from the right. The places to its left are "
            "worth eight, four, two and one; to its right, a half, a quarter, an eighth and a sixteenth. "
            "<bookmark mark='b'/> Then these eight bits mean five point six two five, which is the integer ninety "
            "divided by sixteen. <bookmark mark='c'/> This is fixed point, and its format is written Q four point four. "
            "Adding and subtracting are exactly the integer operations, on the same adder. Multiplying two such numbers "
            "multiplies their scale factors too, so multiply the integers and shift the result right by four. "
            "Nothing new is needed in the hardware."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(point), FadeIn(w))
            vo.wait_until("b")
            self.play(Write(val))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def money(self):
        head = label(r"Money is counted in cents", font_size=38).to_edge(UP, buff=0.35)
        left = VGroup(label(r"floating point", font_size=28, color=NO),
                      Text("0.10 + 0.20 == 0.30\n→ False", font="DejaVu Sans Mono", font_size=26, color=GREY_A),
                      Text("sum([0.10] * 10)\n→ 0.9999999999999999", font="DejaVu Sans Mono", font_size=26,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(LEFT * 3.4 + UP * 0.4)
        right = VGroup(label(r"integer cents", font_size=28, color=YES),
                       Text("10 + 20 == 30\n→ True", font="DejaVu Sans Mono", font_size=26, color=GREY_A),
                       Text("sum([10] * 10)\n→ 100", font="DejaVu Sans Mono", font_size=26, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.2 + UP * 0.4)
        why = label(r"a tenth has no finite binary expansion: \ $0.1 = 0.0\overline{0011}_2$", font_size=28,
                    color=HEAD).to_edge(DOWN, buff=1.1)
        rule = note(r"banks, payment systems and databases store money as integers \ (or decimal types), \ and fix "
                    r"the rounding rule in writing", font_size=22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Fixed point has one place where it is not optional: money. <bookmark mark='a'/> In floating point, ten "
            "cents plus twenty cents is not thirty cents, and ten dimes do not make a dollar; they make zero point nine "
            "nine nine, and so on. <bookmark mark='b'/> Counted as integers, in cents, every sum is exact. "
            "<bookmark mark='c'/> The root cause is that one tenth has no finite expansion in binary, just as one third "
            "has none in decimal: it is zero point zero, then zero zero one one, repeating forever, and any format "
            "with finitely many bits must round it. So financial software keeps money in integer cents, or in decimal "
            "types, and writes down exactly how and when to round."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(right, lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(why), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def range_(self):
        head = label(r"What fixed point cannot do: \ range", font_size=38).to_edge(UP, buff=0.35)
        ax = NumberLine(x_range=[-40, 40, 10], length=12.0, color=GREY_C).move_to(UP * 0.3)
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.n2p(k), DOWN, buff=0.15)
                         for k in range(-40, 41, 10)])
        things = [(-30.04, r"electron mass (kg)", INF), (-10, r"atom (m)", GREY_A), (0, r"1", GREY_A),
                  (30.3, r"the Sun (kg)", FUNC), (26.9, r"observable universe (m)", GREY_A)]
        marks = VGroup()
        for k, (x, t, c) in enumerate(things):
            y = 0.9 + 0.45 * (k % 2)
            marks.add(VGroup(Line(ax.n2p(x), ax.n2p(x) + UP * (y - 0.15), color=c, stroke_width=2),
                             label(t, font_size=20, color=c).move_to(ax.n2p(x) + UP * y)))
        q = (np.log10(2.0 ** -16), np.log10(2.0 ** 15))
        win = Rectangle(width=ax.n2p(q[1])[0] - ax.n2p(q[0])[0], height=0.5, stroke_color=NO, stroke_width=2.5,
                        fill_color=NO, fill_opacity=0.25).move_to((ax.n2p(q[0]) + ax.n2p(q[1])) / 2 + DOWN * 1.0)
        wl = label(r"Q16.16 \ (32 bits): \ $1.5 \times 10^{-5}$ to $3.3 \times 10^{4}$: \ 9 decades", font_size=24,
                   color=NO).next_to(win, DOWN, buff=0.2)
        fwin = Rectangle(width=ax.n2p(38.5)[0] - ax.n2p(-37.9)[0], height=0.5, stroke_color=YES, stroke_width=2.5,
                         fill_color=YES, fill_opacity=0.18).move_to((ax.n2p(-37.9) + ax.n2p(38.5)) / 2 + DOWN * 2.2)
        fl = label(r"a 32-bit float: \ $10^{-38}$ to $10^{38}$, \ with about 7 digits everywhere", font_size=24,
                   color=YES).next_to(fwin, DOWN, buff=0.2)
        with self.voiceover(
            "What fixed point cannot do is range. <bookmark mark='a'/> Science deals with numbers from the mass of an "
            "electron, about ten to the minus thirty kilograms, to the mass of the Sun, about ten to the thirty. "
            "<bookmark mark='b'/> A thirty-two-bit fixed-point number with sixteen bits on each side of the point "
            "covers nine decades, from about one sixty-thousandth to about thirty thousand, with the same absolute "
            "spacing everywhere: superb near thirty thousand and useless near zero. Classic Doom did its geometry in "
            "exactly this format, and signal processors and embedded chips still live in it. "
            "<bookmark mark='c'/> To cover all of science you would need two hundred bits. Instead, let the point "
            "float: store the digits and, separately, where the point goes. A thirty-two-bit floating-point number "
            "spans seventy-six decades with about seven significant digits at every scale. That is the next chapter."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(win), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(fwin), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()
