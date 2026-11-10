from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def ms(s):
    return f"{s * 1000:.1f} ms" if s < 1 else f"{s:.2f} s"


class Karatsuba(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.trick()
        self.tree()
        self.measured()

    def card(self):
        card = chapter_card(3, r"Three products instead of four", r"Is multiplication really $n^2$?", lit=(1960,),
                            extra=((1960, r"Karatsuba"), (1963, r"Toom")), part=PART)
        with self.voiceover("Chapter three. Three products instead of four."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def story(self):
        head = label(r"Moscow, \ 1960", font_size=36).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"Andrey Kolmogorov's seminar: \ \textit{multiplying two $n$-digit numbers needs about $n^2$ "
                  r"steps}", font_size=23, color=GREY_A),
            label(r"a conjecture: \ no faster way was known", font_size=22, color=GREY_A),
            label(r"within a week, \ Anatoly Karatsuba, \ 23, \ found $n^{1.585}$", font_size=24, color=YES),
            label(r"Kolmogorov wrote it up himself \ (Karatsuba and Ofman, \ 1962) \ and ended the seminar",
                  font_size=21, color=HEAD),
            label(r"the start of the theory of fast arithmetic", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.7)
        school_grid=VGroup(*[Square(.17,stroke_color=DATA,stroke_width=1,fill_color=DATA,fill_opacity=.45)
                             for _ in range(64)]).arrange_in_grid(rows=8,cols=8,buff=.025).move_to([0,-2.25,0])
        grid_caption=label("8 by 8 candidate coefficient products",font_size=19,color=DATA).next_to(school_grid,DOWN,buff=.16)
        with self.voiceover(
            "Karatsuba recalled a Moscow seminar in 1960, led by Andrey Kolmogorov. <bookmark mark='a'/> The "
            "challenge was whether multiplying n-digit integers really required quadratic work. <bookmark mark='b'/> "
            'The familiar school algorithm did; that did not establish a lower bound for every algorithm. <bookmark '
            "mark='c'/> Anatoly Karatsuba found a decomposition using three half-size products rather than four. "
            "<bookmark mark='d'/> The result appeared in a 1962 paper by Karatsuba and Yuri Ofman. <bookmark "
            "mark='e'/> Its lasting lesson is mathematical: a better algebraic identity can change the exponent, not "
            'merely tune a constant.'
        ) as vo:
            self.play(FadeIn(head),FadeIn(school_grid),FadeIn(grid_caption))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def trick(self):
        head = label(r"The trick", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"x = x_1 \cdot 10^m + x_0, \qquad y = y_1 \cdot 10^m + y_0", font_size=34),
            MathTex(r"xy = \underbrace{x_1 y_1}_{z_2}\,10^{2m} + (x_1 y_0 + x_0 y_1)\,10^m + \underbrace{x_0 y_0}_{z_0}",
                    font_size=34),
            MathTex(r"x_1 y_0 + x_0 y_1 = (x_1 + x_0)(y_1 + y_0) - z_2 - z_0", font_size=34, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        ex = VGroup(
            MathTex(r"1234 \times 5678:", font_size=30, color=HEAD),
            MathTex(r"z_2 = 12 \times 56 = 672, \quad z_0 = 34 \times 78 = 2652", font_size=30),
            MathTex(r"(12 + 34)(56 + 78) = 46 \times 134 = 6164, \quad 6164 - 672 - 2652 = 2840", font_size=30),
            MathTex(r"672\,0000 + 2840\,00 + 2652 = 7006652", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(eqs, DOWN, buff=0.5)
        split=VGroup(*[VGroup(RoundedRectangle(width=1.1,height=.62,corner_radius=.08,stroke_color=color,
                                  fill_color=color,fill_opacity=.35),mono(value,24,WHITE))
                            for value,color in zip(["12","34","56","78"],[DATA,DATA,YES,YES])])
        for obj,xpos in zip(split,[-2.5,-1.2,1.2,2.5]):obj.move_to([xpos,-2.4,0])
        split.add(MathTex(r"\times",font_size=32,color=HEAD).move_to([0,-2.4,0]))
        with self.voiceover(
            "Here is the trick. <bookmark mark='a'/> Split each number into a high half and a low half. <bookmark "
            "mark='b'/> The product needs four half-size products: high times high, low times low, and the two "
            "cross terms. <bookmark mark='c'/> But the two cross terms are only needed as a sum, and that sum is "
            "the product of the two half-sums, minus the two products we already have. Three multiplications "
            "instead of four, paid for with a few additions, which are cheap. <bookmark mark='d'/> For 1234 times "
            "5678: twelve times fifty-six, thirty-four times seventy-eight, and forty-six times one hundred and "
            "thirty-four, from which the middle term follows by subtraction. Three products give seven million "
            "and six thousand, six hundred and fifty-two."
        ) as vo:
            self.play(FadeIn(head),FadeIn(split))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.remove(split)
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.5), run_time=4)
        self.wait(0.3)
        self.clear_scene()

    def tree(self):
        head = label(r"Recursing", font_size=34).to_edge(UP, buff=0.3)
        levels = VGroup()
        for k in range(4):
            cnt = 3 ** k
            w = min(0.9, 11.0 / cnt - 0.08)
            row = VGroup(*[RoundedRectangle(width=w, height=0.42, corner_radius=0.06, stroke_color=DATA,
                                            stroke_width=1.5, fill_color=DATA, fill_opacity=0.25 + 0.1 * k)
                           for _ in range(cnt)]).arrange(RIGHT, buff=0.08)
            lab = label(rf"{cnt} product{'s' if cnt > 1 else ''} of size $n/{2 ** k}$" if k else r"1 product of size "
                        r"$n$", font_size=19, color=GREY_A)
            levels.add(VGroup(row, lab))
        for i, lv in enumerate(levels):
            lv[0].move_to([0, 1.9 - 1.05 * i, 0])
            lv[1].next_to(lv[0], RIGHT, buff=0.3) if i < 2 else lv[1].next_to(lv[0], DOWN, buff=0.12)
        eq = VGroup(
            MathTex(r"T(n) = 3\,T(n/2) + O(n)", font_size=34, color=YES),
            MathTex(r"3^{\lg n} = n^{\lg 3} = n^{1.585}", font_size=34, color=HEAD),
            label(r"four products would give $4^{\lg n} = n^2$: \ the saving compounds at every level", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The three-product decomposition recurses. <bookmark mark='a'/> One multiplication becomes three half-"
            'size problems, then nine quarter-size problems and twenty-seven eighth-size problems. <bookmark '
            "mark='b'/> For a power-of-two coefficient-array length, recursing to scalar leaves gives three to the "
            'log-base-two n leaves. Additions cost linear work at each node, yielding the n-to-log-base-two-three '
            'recurrence. Integer implementations also handle carries and the extra width of sums. <bookmark '
            "mark='c'/> The rectangular school model has n squared products. Our measured school loop skips zero left"
            ' digits, so the table distinguishes that model from its actual multiplication count.'
        ) as vo:
            self.play(FadeIn(head),FadeIn(levels))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(lv[0],color=HEAD) for lv in levels], lag_ratio=.25),run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(eq[0]), FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq[2]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("karatsuba")
        head = label(r"Timed, \ in Python, \ on this machine", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['school_products']:,}", f"{r['kara_products']:,}", ms(r["school_s"]),
                 ms(r["kara1_s"]), ms(r["kara32_s"])] for r in d["rows"] if r["n"] >= 64]
        tab = grid_table([r"digits", r"products, \ school", r"products, \ Karatsuba", r"school",
                          r"Karatsuba, \ pure", r"with a cutoff"], rows, widths=[1.5, 2.4, 2.4, 1.8, 2.0, 2.0],
                         row_h=0.42, font_size=18, colors=[[WHITE, NO, YES, NO, LAM, YES]] * len(rows)).next_to(
            head, DOWN, buff=0.4)
        last = d["rows"][-1]
        cross = next(r["n"] for r in d["rows"] if r["n"] > 32 and r["kara32_s"] < r["school_s"])
        pts = VGroup(
            label(rf"pure Karatsuba, \ down to single digits, \ is slower than school even at {words(last['n'])} "
                  r"digits: \ its additions and bookkeeping cost more than the products saved", font_size=20,
                  color=LAM),
            label(rf"switch to school below 32 digits: \ ahead from {cross} digits, \ "
                  rf"{last['school_s'] / last['kara32_s']:.1f}$\times$ faster at {words(last['n'])}", font_size=21,
                  color=YES),
            label(r"CPython does the same: \ Karatsuba above 70 machine digits of 30 bits, \ about 630 decimal "
                  r"digits", font_size=20, color=GREY_A),
            label(r"Toom--Cook \ (1963--66): \ five products of thirds, \ $n^{1.465}$; \ then the FFT \ (chapter 7)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            'These runs use preconverted decimal digit arrays and return coefficient convolutions. <bookmark '
            "mark='a'/> We carry and compare every timed result with Python's exact integer product after stopping "
            "the timer. The counters record actual scalar products, including the school's skipped zero rows. "
            "<bookmark mark='b'/> A cutoff of thirty-two reduces recursive overhead; the table shows the observed "
            "crossover on this host rather than a hardware-independent threshold. <bookmark mark='c'/> CPython "
            'similarly combines school multiplication and Karatsuba, but its machine-digit threshold is an '
            "implementation choice, not thirty-two decimal digits. <bookmark mark='d'/> Toom-Cook uses evaluation and"
            ' interpolation to reduce products further. The FFT takes that principle to many carefully chosen '
            'evaluation points.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
