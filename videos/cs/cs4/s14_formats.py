from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, load, sci

SIGN, EXP, FRAC = "#E5484D", "#4DABF7", "#69DB7C"


def layout_bar(e, m, unit=0.17, h=0.36):
    g = VGroup()
    for n, col in ((1, SIGN), (e, EXP), (m, FRAC)):
        if n:
            g.add(Rectangle(width=unit * n, height=h, stroke_color=BG, stroke_width=1, fill_color=col, fill_opacity=0.9))
    g.arrange(RIGHT, buff=0)
    return g


class Formats(WatchScene):
    def construct(self):
        self.card()
        self.ml()

    def card(self):
        self.chapter(13, r"Beyond IEEE", r"Why does machine learning want fewer bits?", lit=(2017, 2022), part=PART, said="Chapter thirteen. Beyond IEEE.")


    # ------------------------------------------------------------------
    def ml(self):
        self.ask(r"bfloat16 has 16 bits; float32 has 32. \\ Is bfloat16's range much smaller?", [r"yes",
                 r"no: the same range"], 1,
                 say="Google's bfloat16 uses half the bits of a single-precision float. Is its range much smaller?",
                 reveal="No. It keeps all eight exponent bits, and gives up precision instead.")
        d = load("floats")
        fm = {f["name"]: f for f in d["formats"]}
        head = label(r"Range over precision: \ bfloat16", font_size=38).to_edge(UP, buff=0.3)
        b32 = VGroup(label(r"binary32", font_size=26, color=GREY_A), layout_bar(8, 23, unit=0.2)).arrange(RIGHT, buff=0.3)
        b16 = VGroup(label(r"bfloat16", font_size=26, color=YES), layout_bar(8, 7, unit=0.2)).arrange(RIGHT, buff=0.3)
        h16 = VGroup(label(r"binary16", font_size=26, color=NO), layout_bar(5, 10, unit=0.2)).arrange(RIGHT, buff=0.3)
        bars = VGroup(b32, b16, h16).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 2.0 + UP * 1.4)
        for b in bars:
            b[1].align_to(bars[0][1], LEFT)
        same = label(r"bfloat16 shares float32's high-bit layout; \ conversion usually rounds", font_size=26,
                     color=YES).next_to(bars, DOWN, buff=0.4)
        pts = VGroup(
            label(r"bfloat16's wider exponent range reduces gradient underflow", font_size=24,
                  color=GREY_A),
            label(r"many models tolerate low precision; \ training still needs care", font_size=24, color=GREY_A),
            label(r"half the bits: \ twice the values per transfer; \ smaller multipliers",
                  font_size=24, color=HEAD),
            label(r"FP8 (2022): \ E4M3 for weights and activations, \ E5M2 for gradients", font_size=24, color=INF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Machine learning answered that question in an unusual way. <bookmark mark='a'/> Google Brain's bfloat16 "
            "shares the high-bit layout of a single-precision float: eight exponent bits and seven fraction bits. "
            "Conversion normally rounds, rather than just discarding the low bits. IEEE's half precision made the opposite choice, five exponent bits and ten of fraction. "
            "<bookmark mark='b'/> For many neural networks, bfloat16 is useful. Gradients span many decades, and its "
            "wide exponent range reduces underflow compared with binary16. Many models tolerate low precision, "
            "but not every quantity does; accumulation and training recipes still matter. <bookmark mark='c'/> Fewer bits also means more "
            "numbers per transfer from memory, which is usually the real bottleneck, and a significand multiplier's area grows roughly "
            "with the square of the fraction width. In 2022 the industry agreed on two eight-bit formats, one with "
            "more precision for weights and activations and one with more range for gradients. Part 17 of AI, Built "
            "trains a model in these formats and measures what they cost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars))
            vo.wait_until("a")
            self.play(Indicate(bars, scale_factor=1.02), FadeIn(same))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

