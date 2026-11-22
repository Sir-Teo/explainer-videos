from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bit_cells


class Positional(WatchScene):
    def construct(self):
        self.card()
        self.places()
        self.convert()

    def card(self):
        self.chapter(1, r"Bits as numbers", r"Why do computers count in twos?", lit=(1679,), part=PART, said="Chapter one. Bits as numbers.")

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
        rule = MathTex(r"n \text{ bits: } 2^n \text{ values, } 0 \dots 2^n - 1; \qquad N>0 \text{ needs } "
                       r"\lfloor \log_2 N \rfloor + 1 \text{ bits}", font_size=34, color=CODE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two thousand and twenty-six means two thousands, no hundreds, two tens and six ones. A digit's value "
            "depends on its place, and each place is worth ten times the one to its right. <bookmark mark='a'/> "
            "Nothing about this needs ten. In base two each place is worth twice the one to its right, and each digit "
            "is a zero or a one: a bit. <bookmark mark='b'/> Two thousand and twenty-six is eleven bits: the places "
            "worth one thousand and twenty-four, five hundred and twelve, and so on, wherever there is a one. "
            "<bookmark mark='c'/> Add those up, and you get the number back. <bookmark mark='d'/> With n bits there "
            "are two to the n patterns, so they can count from zero to two to the n minus one; and a positive integer N needs "
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
    def convert(self):
        self.ask(r"2026 in binary: \\ how many bits?", [r"10", r"11", r"12"], 1,
                 say="How many bits does two thousand and twenty-six need?",
                 reveal="Eleven. It's less than two to the eleven, two thousand and forty-eight.")
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
            self.play(FadeIn(head), FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(Indicate(rows[:2], scale_factor=1.03), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows[2:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(read))
            vo.wait_until("c")
            self.play(Write(result), FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

