from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

DIAG = {s: interpolate_color(ManimColor("#5DADEC"), ManimColor("#F28FB8"), (s - 2) / 10) for s in range(2, 13)}
FACTOR_COLS = {"s": GREY_A, "a": "#7BD88F", "b": "#B48EF0", "c": "#FF9F5A"}


class Generating(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.product()
        self.moments()
        self.sicherman()

    def card(self):
        card = chapter_card(13, r"Generating functions", r"A distribution as a polynomial", lit=(1738,), part=PART)
        with self.voiceover("Chapter thirteen. Generating functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        dfn = definition_card(r"Probability generating function", r"for $X$ with values $0, 1, 2, \dots$: \quad "
                              r"$G_X(s) = E\, s^X = \sum_k P(X = k)\, s^k$", color=EXACT, width=7.4, font_size=25)
        dfn.to_edge(UP, buff=0.45)
        g = MathTex(r"G_{\text{die}}(s)", r"=", r"\tfrac16\,(s + s^2 + s^3 + s^4 + s^5 + s^6)", font_size=42)
        g.move_to([0, 0.4, 0])
        faces_ = dice_row(range(1, 7), size=0.5, buff=0.55).next_to(g, DOWN, buff=0.6).shift(RIGHT * 0.9)
        note_ = label(r"the coefficient of $s^k$ \ is $P(X = k)$: \ the exponent is the value, \ the coefficient its "
                      r"chance", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.6)
        intro = label('A distribution as a power series', font_size=36)
        with self.voiceover(
            "Here's a device that turns probability into algebra, invented by de Moivre and made systematic by "
            "Laplace. <bookmark mark='a'/> For a variable that takes the values zero, one, two and so on, its "
            "probability generating function is the expectation of s to the X: a power series whose coefficient "
            "of s to the k is the probability that X equals k. <bookmark mark='b'/> For one die, it's a sixth of s "
            "plus s squared, up to s to the sixth. <bookmark mark='c'/> The exponents record the values and the "
            "coefficients record their chances. A distribution has become a polynomial."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(dfn, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(Write(g))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in faces_], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def product(self):
        d = load("pgf")
        rows = [
            cmath(r"G_{X+Y}(s)", r"=", r"E\, s^{X + Y}", r"=", r"E\, s^X\, s^Y", font_size=36),
            cmath(r"G_{X+Y}(s)", r"=", r"E\, s^X \cdot E\, s^Y", r"=", r"G_X(s)\, G_Y(s)", font_size=36),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"exponents add"), why(r"independent: \ $E(UV) = E U\, E V$")]
        cell = 0.74
        grid = VGroup()
        cells = {}
        origin = np.array([-5.4, 1.9, 0])
        for i in range(1, 7):
            for j in range(1, 7):
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1, fill_color=CELL, fill_opacity=1)
                sq.move_to(origin + np.array([(j - 1) * (cell + 0.04), -(i - 1) * (cell + 0.04), 0]))
                t = MathTex(rf"s^{{{i + j}}}", font_size=28, color=DIAG[i + j]).move_to(sq)
                cells[(i, j)] = VGroup(sq, t)
                grid.add(cells[(i, j)])
        top = VGroup(*[MathTex(rf"s^{j}", font_size=26, color=GREY_A).next_to(cells[(1, j)], UP, buff=0.12)
                       for j in range(1, 7)])
        side = VGroup(*[MathTex(rf"s^{i}", font_size=26, color=GREY_A).next_to(cells[(i, 1)], LEFT, buff=0.12)
                        for i in range(1, 7)])
        coeffs = d["two_counts"]
        poly = MathTex(r"\tfrac1{36}\big(", *[rf"{coeffs[k]}s^{{{k}}}" + (r"+" if k < 12 else "") for k in range(2, 13)],
                       r"\big)", font_size=30)
        for k, part in zip(range(2, 13), poly[1:-1]):
            part.set_color(DIAG[k])
        poly.to_edge(DOWN, buff=0.45)
        if poly.width > 13.2:
            poly.width = 13.2
        same = label(r"the two-dice grid again: \ each anti-diagonal one total", font_size=24, color=GREY_B)
        same.next_to(poly, UP, buff=0.25)
        intro = label('Sums become products', font_size=36)
        with self.voiceover(
            "Why bother? Because generating functions turn sums into products. <bookmark mark='a'/> The generating "
            "function of X plus Y is the expectation of s to the X times s to the Y. <bookmark mark='b'/> If X and Y "
            "are independent, the expectation of the product splits into the product of the expectations: the "
            "generating function of a sum is the product of the generating functions. <bookmark mark='c'/> Square "
            "the die's polynomial and watch what happens. Each term of one factor meets each term of the other: s to "
            "the i times s to the j is s to the i plus j. <bookmark mark='d'/> The terms with the same power lie on "
            "the anti-diagonals, and collecting them gives one, two, three, up to six, and back down: the "
            "distribution of the sum of two dice. It's the two-dice grid of chapter ten, in algebra. Adding "
            "independent variables convolves their distributions, and multiplying polynomials does exactly that."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=2.6, x=2.6, buff=0.55, edge=6.9)
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            step(0, transform=False)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(top), FadeIn(side))
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in grid], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("d")
            for s_ in range(2, 13):
                self.play(*[cells[(i, s_ - i)][0].animate.set_fill(DIAG[s_], opacity=0.35) for i in range(1, 7)
                            if 1 <= s_ - i <= 6], run_time=0.3)
            self.play(Write(poly), FadeIn(same))
        self.clear_scene()

    def moments(self):
        d = load("pgf")
        rows = [
            cmath(r"G'(1)", r"=", r"\sum_k k\, P(X = k)", r"=", r"E X", font_size=36),
            cmath(r"G''(1)", r"=", r"\sum_k k(k-1)\, P(X = k)", r"=", r"E\, X(X-1)", font_size=36),
            cmath(r"\mathrm{Var}\, X", r"=", r"G''(1) + G'(1) - G'(1)^2", font_size=36),
            cmath(r"\text{one die:}\ \ \mathrm{Var}", r"=", rf"{frac(d['g2'])} + {frac(d['mean'])} - "
                  rf"\left({frac(d['mean'])}\right)^2", r"=", rf"{frac(d['var'])}", font_size=36),
        ]
        rows[3][4].set_color(EXACT)
        whys = [why(r"differentiate, \ set $s = 1$"), why(r"twice"), why(r"$E X^2 = E X(X-1) + E X$"),
                why(r"chapter 12's answer, \ by calculus")]
        title = label(r"Moments by differentiation", font_size=36).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Generating functions also hand you the moments. <bookmark mark='a'/> Differentiate, then set s to one, "
            "and every term becomes k times the probability of k: the expectation. <bookmark mark='b'/> "
            "Differentiate twice and you get the expectation of X times X minus one. <bookmark mark='c'/> Combine "
            "them for the variance. <bookmark mark='d'/> For one die this gives thirty-five twelfths, the answer of "
            "the last chapter, now by calculus. Part 3 meets another transform, the "
            "moment generating function, and Part 6 uses its complex cousin, the characteristic function, to prove "
            "the central limit theorem."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=4, top=2.4, x=-0.8, buff=0.5)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def sicherman(self):
        d = load("pgf")
        fac = MathTex(r"G_{\text{die}}(s)", r"=", r"\tfrac16", r"\, s\,", r"(1 + s)", r"(1 + s + s^2)", r"(1 - s + s^2)",
                      font_size=36).to_edge(UP, buff=0.5)
        for part, key in zip(fac[3:], "sabc"):
            part.set_color(FACTOR_COLS[key])
        sq = MathTex(r"G_{\text{die}}(s)^2", r"=", r"\tfrac1{36}", r"\, s^2\,", r"(1 + s)^2", r"(1 + s + s^2)^2",
                     r"(1 - s + s^2)^2", font_size=36).next_to(fac, DOWN, buff=0.35)
        for part, key in zip(sq[3:], "sabc"):
            part.set_color(FACTOR_COLS[key])
        da = MathTex(r"\tfrac16\, s\,(1 + s)(1 + s + s^2)", r"=", r"\tfrac16(s + 2s^2 + 2s^3 + s^4)", font_size=32)
        db = MathTex(r"\tfrac16\, s\,(1 + s)(1 + s + s^2)(1 - s + s^2)^2", r"=", r"\tfrac16(s + s^3 + s^4 + s^5 + s^6 + s^8)",
                     font_size=32)
        VGroup(da, db).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(sq, DOWN, buff=0.5)
        for m in (da, db):
            if m.width > 13:
                m.width = 13
        die_a = dice_row(d["faces_a"] if "faces_a" in d else [1, 2, 2, 3, 3, 4], size=0.55)
        die_b = dice_row([1, 3, 4, 5, 6, 8], size=0.55)
        dd = VGroup(VGroup(label(r"die A", font_size=24, color=S.LIK), die_a).arrange(RIGHT, buff=0.3),
                    VGroup(label(r"die B", font_size=24, color=S.PRIOR), die_b).arrange(RIGHT, buff=0.3))
        dd.arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.45).shift(LEFT * 3.0)
        chk = code_block(["(A + B).p == (die + die).p   # True"], font_size=22).next_to(dd, RIGHT, buff=0.8)
        hc = label(r"George Sicherman; \ Martin Gardner's column, \ 1978", font_size=22, color=S.MUSEUM)
        hc.next_to(chk, DOWN, buff=0.2)
        intro = label('Different dice, the same sums', font_size=36)
        with self.voiceover(
            "Here's the most charming use of generating functions. Are ordinary dice the only pair whose totals have "
            "the usual distribution? <bookmark mark='a'/> Factor the die's polynomial over the integers: s, times one "
            "plus s, times one plus s plus s squared, times one minus s plus s squared. <bookmark mark='b'/> The "
            "pair's generating function is its square, every factor twice. <bookmark mark='c'/> Now deal the factors "
            "out differently. Each die must keep one factor of s, so no face shows zero, and its polynomial must "
            "add up to six at s equals one, so it has six faces. The only other way: give one die both copies of the "
            "last factor and the other die none. <bookmark mark='d'/> Expand, and read off the faces. One die is "
            "one, two, two, three, three, four. <bookmark mark='e'/> The other is one, three, four, five, six, "
            "eight. <bookmark mark='f'/> These are Sicherman's dice, popularized by Martin Gardner in 1978. Roll "
            "them together, and every total from two to twelve comes up with exactly the same probability as with "
            "ordinary dice. The engine agrees, outcome by outcome."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(fac))
            vo.wait_until("b")
            self.play(Write(sq))
            vo.wait_until("c")
            self.play(Indicate(sq[6], color=FACTOR_COLS["c"], scale_factor=1.15))
            vo.wait_until("d")
            self.play(Write(da))
            self.play(FadeIn(dd[0], shift=UP * 0.2))
            vo.wait_until("e")
            self.play(Write(db))
            self.play(FadeIn(dd[1], shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(chk), FadeIn(hc))
        self.clear_scene()
