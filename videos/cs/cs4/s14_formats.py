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


class Formats(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.ml()
        self.others()

    def card(self):
        card = chapter_card(13, r"Beyond IEEE", r"Why does machine learning want fewer bits?", lit=(2017, 2022), part=PART)
        with self.voiceover("Chapter thirteen. Beyond IEEE."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def table(self):
        d = load("floats")
        head = label(r"Six formats, \ one design", font_size=38).to_edge(UP, buff=0.3)
        rows = VGroup()
        hdr = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"format", r"sign, \ exponent, \ fraction",
                                                                      r"largest", r"$\varepsilon$", r"digits")])
        rows.add(hdr)
        for f in d["formats"]:
            rows.add(VGroup(label(f["name"], font_size=24, color=WHITE), layout_bar(f["e"], f["m"], unit=0.08),
                            MathTex(sci(f["max"]), font_size=26, color=GREY_A),
                            MathTex(rf"2^{{-{f['m']}}}", font_size=26, color=GREY_A),
                            MathTex(f"{f['digits']:.1f}", font_size=26, color=HEAD)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                x = [-6.5, -4.0, 2.2, 4.3, 6.0][j]
                if j == 1:
                    m.move_to([x, 2.1 - 0.62 * i, 0], aligned_edge=LEFT)
                else:
                    m.move_to([x, 2.1 - 0.62 * i, 0], aligned_edge=LEFT if j == 0 else ORIGIN)
        foot = note(r"each row: \ $(-1)^s\, 1.f \times 2^{e - \text{bias}}$, \ with subnormals, \ infinities and NaNs "
                    r"\ (FP8 E4M3 trades its infinities for range: \ largest 448)", font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The same design comes in many sizes. <bookmark mark='a'/> Double precision, sixty-four bits, with eleven "
            "bits of exponent and fifty-two of fraction, gives about sixteen decimal digits; scientific computing "
            "lives here. Single precision gives about seven. Half precision, sixteen bits, gives three digits and a "
            "largest value of only sixty-five thousand. <bookmark mark='b'/> Below it are formats invented in the last "
            "decade for machine learning: bfloat16, and two eight-bit formats, FP8, with barely one significant "
            "digit. Each row splits its bits between exponent, for range, and fraction, for precision, and the "
            "interesting question is which matters more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[1:4]], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[4:]], lag_ratio=0.35), FadeIn(foot),
                      run_time=2.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ml(self):
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

    # ------------------------------------------------------------------
    def others(self):
        head = label(r"Other ways to hold a real number", font_size=38).to_edge(UP, buff=0.35)
        iv = VGroup(label(r"interval arithmetic", font_size=28, color=INF),
                    MathTex(r"[a, b] + [c, d] = [\nabla(a + c),\ \Delta(b + d)]", font_size=30, color=CODE),
                    label(r"round the ends outward: \ the true value is guaranteed inside", font_size=22, color=GREY_A),
                    MathTex(r"x = [1, 2]: \quad x - x = [-1, 1] \ne 0", font_size=30, color=NO),
                    label(r"but each $x$ is treated as independent: \ the dependency problem", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 0.9).to_edge(LEFT, buff=0.5)
        po = VGroup(label(r"posits \ (Gustafson, 2017)", font_size=28, color=FUNC),
                    label(r"a variable-length regime for scale: \ more fraction bits near 1, \\ fewer far away \ (tapered "
                          r"precision)", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(
            RIGHT * 3.2 + UP * 1.5)
        po.to_edge(RIGHT, buff=0.5)
        bn = VGroup(label(r"bignums", font_size=28, color=YES),
                    label(r"integers as long as memory allows: \ Python's \texttt{int}, \ GMP", font_size=22,
                          color=GREY_A),
                    MathTex(r"2^{100} = 1267650600228229401496703205376", font_size=26, color=CODE),
                    label(r"schoolbook multiplication is $O(n^2)$; \ Karatsuba's $O(n^{1.585})$ is Part 19", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.6).to_edge(RIGHT, buff=0.5)
        foot = note(r"and exact rationals, \ decimal floating point (IEEE 754-2008) for money, \ and computer algebra",
                    font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There are other answers altogether. <bookmark mark='a'/> Interval arithmetic stores a lower and an upper "
            "bound, and uses IEEE's directed rounding modes to round each end outward, so the true value is guaranteed "
            "to lie inside. Its weakness is that it forgets where numbers came from: x minus x, for x between one and "
            "two, comes out as minus one to one, not zero. <bookmark mark='b'/> John Gustafson's posits, from 2017, "
            "use a variable-length regime to encode scale, spending more bits on precision near one and fewer far away. "
            "<bookmark mark='c'/> And when exactness matters more than speed, integers can simply grow, as Python's do: "
            "two to the hundred, all thirty-one digits of it. Multiplying such numbers the schoolbook way takes time "
            "proportional to the square of their length; a cleverer method, Karatsuba's, waits for Part 19."
        ) as vo:
            self.play(FadeIn(head), FadeIn(iv))
            vo.wait_until("a")
            self.play(Indicate(iv, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(po, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(bn, lag_ratio=0.2), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
