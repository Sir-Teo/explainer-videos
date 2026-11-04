from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bit_cells


class Positional(VoiceoverScene):
    def construct(self):
        self.card()
        self.places()
        self.why_binary()
        self.convert()
        self.hexa()

    def card(self):
        card = chapter_card(1, r"Bits as numbers", r"Why do computers count in twos?", lit=(1679,), part=PART)
        with self.voiceover("Chapter one. Bits as numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def places(self):
        head = label(r"A digit's value depends on its place", font_size=38).to_edge(UP, buff=0.4)
        dec = MathTex(r"2026", r"=", r"2 \cdot 10^3", r"+", r"0 \cdot 10^2", r"+", r"2 \cdot 10^1", r"+",
                      r"6 \cdot 10^0", font_size=42, color=GREY_A).move_to(UP * 2.0)
        dec[0].set_color(DATA)
        x = 2026
        bits = format(x, "b")
        n = len(bits)
        cells = bit_cells(bits, cell=0.62, font_size=36).move_to(UP * 0.1)
        weights = VGroup(*[MathTex(rf"2^{{{n - 1 - i}}}", font_size=26, color=GREY_B).next_to(cells[i], UP, buff=0.15)
                           for i in range(n)])
        vals = VGroup(*[MathTex(str(2 ** (n - 1 - i)), font_size=22, color=HEAD).next_to(cells[i], DOWN, buff=0.15)
                        for i in range(n) if bits[i] == "1"])
        total = MathTex(r"1024 + 512 + 256 + 128 + 64 + 32 + 8 + 2 = 2026", font_size=36, color=YES).move_to(DOWN * 1.6)
        rule = MathTex(r"n \text{ bits: } 2^n \text{ values, } 0 \dots 2^n - 1; \qquad N \text{ needs } "
                       r"\lfloor \log_2 N \rfloor + 1 \text{ bits}", font_size=34, color=CODE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two thousand and twenty-six means two thousands, no hundreds, two tens and six ones. A digit's value "
            "depends on its place, and each place is worth ten times the one to its right. <bookmark mark='a'/> "
            "Nothing about this needs ten. In base two each place is worth twice the one to its right, and each digit "
            "is a zero or a one: a bit. <bookmark mark='b'/> Two thousand and twenty-six is eleven bits: the places "
            "worth one thousand and twenty-four, five hundred and twelve, and so on, wherever there is a one. "
            "<bookmark mark='c'/> Add those up, and you get the number back. <bookmark mark='d'/> With n bits there "
            "are two to the n patterns, so they can count from zero to two to the n minus one; and a number N needs "
            "about log base two of N bits. Gottfried Leibniz worked all of this out in 1679, and thought it so elegant "
            "that he saw creation in it: everything from one and nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dec))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(weights))
            vo.wait_until("b")
            self.play(LaggedStart(*[Indicate(cells[i], color=HEAD) for i in range(n) if bits[i] == "1"],
                                  lag_ratio=0.15), FadeIn(vals))
            vo.wait_until("c")
            self.play(Write(total))
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_binary(self):
        head = label(r"Why two? \ Noise", font_size=38).to_edge(UP, buff=0.4)
        rng = np.random.default_rng(2)

        def bar(levels, x, color):
            h = 4.4
            base = np.array([x, -2.3, 0])
            g = VGroup(Rectangle(width=1.0, height=h, stroke_color=GREY_C, stroke_width=1.5).move_to(base + UP * h / 2))
            for k in range(levels):
                y0 = base[1] + h * k / levels
                band = Rectangle(width=1.0, height=h / levels, stroke_width=0, fill_color=color,
                                 fill_opacity=0.12 + 0.5 * (k % 2)).move_to([x, y0 + h / levels / 2, 0])
                g.add(band)
            # noisy samples of each level
            pts = VGroup()
            for k in range(levels):
                mid = base[1] + h * (k + 0.5) / levels
                for _ in range(14):
                    pts.add(Dot([x + rng.uniform(-0.4, 0.4), mid + rng.normal(0, 0.16), 0], radius=0.03, color=WHITE))
            return g, pts

        b2, p2 = bar(2, -4.6, YES)
        b10, p10 = bar(10, 1.0, NO)
        l2 = label(r"2 levels: \ each band is $\tfrac12 V_{DD}$ wide", font_size=26, color=YES).next_to(b2, RIGHT, buff=0.3)
        l10 = label(r"10 levels: \ each band $\tfrac1{10} V_{DD}$", font_size=26, color=NO).next_to(b10, RIGHT, buff=0.3)
        foot = note(r"the same noise \ ($\sigma = 0.04\,V_{DD}$) \ on both: \ with ten levels, \ neighbours blur together",
                    font_size=22).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why two, and not ten? Because of noise. <bookmark mark='a'/> A wire's voltage is never exactly what it "
            "should be: neighbouring wires, heat and the supply all jiggle it. With two levels, a zero and a one, "
            "there is half the supply voltage between them, and Part 3's inverter snaps anything near a level back to "
            "it. <bookmark mark='b'/> With ten levels, each gets a tenth of the range, and the same jiggle carries a "
            "three into a four. Every gate would need ten thresholds, and each stage would add error rather than remove "
            "it. Two levels is the most robust choice there is, and it pays for itself many times over: we simply use "
            "more wires."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(b2), FadeIn(p2, lag_ratio=0.01), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(b10), FadeIn(p10, lag_ratio=0.01), FadeIn(l10), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convert(self):
        head = label(r"Decimal to binary: \ halve, \ and keep the remainders", font_size=36).to_edge(UP, buff=0.35)
        x = 2026
        rows = VGroup()
        while x:
            rows.add(VGroup(MathTex(rf"{x} \div 2 = {x // 2}", font_size=30, color=GREY_A),
                            MathTex(rf"\text{{r}}\ {x % 2}", font_size=30, color=YES if x % 2 else GREY_B)).arrange(
                RIGHT, buff=0.5))
            x //= 2
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(LEFT * 3.4 + DOWN * 0.35)
        for r in rows:
            r[1].set_x(rows[0][0].get_right()[0] + 0.9 + r[1].width / 2)
        arrow = Arrow(rows[-1][1].get_right() + RIGHT * 0.3, rows[0][1].get_right() + RIGHT * 0.3, buff=0,
                      color=HEAD, stroke_width=4)
        read = label(r"read the remainders \\ from the bottom up", font_size=26, color=HEAD).next_to(arrow, RIGHT,
                                                                                                    buff=0.25)
        result = MathTex(r"2026 = 11111101010_2", font_size=40, color=DATA).move_to(RIGHT * 3.5 + DOWN * 1.8)
        why = note(r"each remainder is the lowest bit; \\ halving shifts the rest down one place", font_size=22).next_to(
            result, DOWN, buff=0.3)
        with self.voiceover(
            "To go the other way, from a decimal number to its bits, keep halving. <bookmark mark='a'/> Two thousand "
            "and twenty-six is even, so its lowest bit is zero; half of it is one thousand and thirteen, which is odd, "
            "so the next bit is one; and so on down to zero. <bookmark mark='b'/> Reading the remainders from the "
            "bottom up gives the bits from the top down. <bookmark mark='c'/> It works because halving a binary number "
            "shifts every bit one place to the right, and the remainder is the bit that falls off the end. Every "
            "routine that prints a number, in any base, is this loop."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.25), run_time=3.5)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(read))
            vo.wait_until("c")
            self.play(Write(result), FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hexa(self):
        head = label(r"Hexadecimal: \ four bits per digit", font_size=38).to_edge(UP, buff=0.4)
        bits = "011111101010"
        cells = bit_cells(bits, cell=0.56, font_size=32).move_to(UP * 1.4)
        groups = VGroup(*[SurroundingRectangle(VGroup(*cells[4 * k:4 * k + 4]), buff=0.06, color=CTRL, corner_radius=0.05)
                          for k in range(3)])
        hexd = VGroup(*[MathTex(h, font_size=48, color=CTRL).next_to(groups[k], DOWN, buff=0.35)
                        for k, h in enumerate("7EA")])
        res = MathTex(r"2026 = \texttt{0x7EA} = 7 \cdot 16^2 + 14 \cdot 16 + 10", font_size=38, color=GREY_A).move_to(
            DOWN * 0.9)
        table = VGroup(*[VGroup(MathTex(format(v, "04b"), font_size=22, color=GREY_B),
                                MathTex(format(v, "X"), font_size=26, color=CTRL)).arrange(DOWN, buff=0.08)
                         for v in range(16)]).arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=1.0)
        uses = note(r"memory addresses, \ colours (\texttt{\#E5484D}), \ machine code: \ hex is binary, \ "
                    r"made readable", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Long strings of bits are hard for people to read, so we write them in base sixteen. <bookmark mark='a'/> "
            "Sixteen is two to the fourth, so every group of four bits, counted from the right, is exactly one "
            "hexadecimal digit, from zero to nine and then a to f for ten to fifteen. <bookmark mark='b'/> Two "
            "thousand and twenty-six is seven, e, a in hexadecimal. <bookmark mark='c'/> Converting is just regrouping "
            "the bits: no arithmetic at all. That is why memory addresses, colours on a web page and machine code are "
            "written in hex. Pebble's instructions in Part 6 will be too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(Create(groups), FadeIn(table))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in hexd], lag_ratio=0.3), Write(res))
            vo.wait_until("c")
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()
