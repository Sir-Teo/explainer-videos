from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, plain_axes, polyline, square_axes


class Contraction(VoiceoverScene):
    def construct(self):
        self.card()
        self.cobweb()
        self.proof()
        self.complete()
        self.newton()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"The contraction principle", r"When does iterating a map find a solution?", lit=(),
                            part=4)
        with self.voiceover("Chapter four: the contraction principle, the engine of this part."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cobweb(self):
        d = load("contraction")
        x, fix, errs, bound, c = d["x"], float(d["fix"]), d["errs"], d["bound"], float(d["c"])
        ax = square_axes([0, 1.1, 0.5], [0, 1.1, 0.5], 4.9, numbers=True, font_size=20,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.6, 0])
        t = np.linspace(0, 1.1, 300)
        cg = polyline(ax, t, np.cos(t), color=C.FUNC, stroke_width=3.5)
        dg = polyline(ax, t, t, color=GREY_B, stroke_width=2.5)
        cl = MathTex(r"y = \cos x", font_size=28, color=C.FUNC).move_to(ax.c2p(0.27, 0.78))  # under the curve, left of the web
        dl = MathTex(r"y = x", font_size=28, color=GREY_B).next_to(ax.c2p(0.3, 0.12), RIGHT, buff=0.05)  # below the diagonal
        web = VGroup()
        for k in range(9):
            a, b = x[k], x[k + 1]
            web.add(Line(ax.c2p(a, a if k else 0), ax.c2p(a, b), color=C.EPS, stroke_width=2.5))
            web.add(Line(ax.c2p(a, b), ax.c2p(b, b), color=C.EPS, stroke_width=2.5))
        fdot = Dot(ax.c2p(fix, fix), radius=0.08, color=WHITE)
        head = VGroup(label(r"Solve $\cos x = x$ by iterating: \ $x_{n+1} = \cos x_n$", font_size=30),
                      label(r"on $[0, 1]$, \ $|\cos' x| = |\sin x| \le \sin 1 = c$: \ every distance shrinks by $c$",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"n", r"x_n", r"|x_n - x^*|", r"\frac{c^n}{1 - c}|x_1 - x_0|",
                             font_size=26, color=GREY_A))
        for n in (0, 1, 2, 3, 5, 10, 20, 30):
            tab.add(MathTex(rf"{n}", rf"{x[n]:.6f}", rf"{sci(float(errs[n]), 2)}", rf"{sci(float(bound[n]), 2)}",
                            font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.5, -0.6, 0])
        x0 = tab.get_left()[0]
        cols_x = (0.0, 0.55, 2.0, 3.75)  # fixed column starts (scene units from the table's left edge)
        for row in tab:
            for j in range(4):
                row[j].set_x(x0 + cols_x[j] + row[j].width / 2)
        if tab.get_right()[0] > 6.85:  # keep the widest header inside the frame
            tab.shift((6.85 - tab.get_right()[0]) * RIGHT)
        fl = MathTex(rf"x^* = {fix:.10f}", font_size=30, color=C.EPS).next_to(tab, DOWN, buff=0.3)
        assert np.all(errs <= bound + 1e-15) and abs(c - math.sin(1)) < 1e-15
        with self.voiceover(
            "<bookmark mark='a'/> To solve cosine of x equals x, just iterate: start anywhere, apply the cosine, and "
            "apply it again. <bookmark mark='b'/> On the graph, bounce between the curve and the diagonal: the path "
            "spirals in on the crossing. <bookmark mark='c'/> Why it works: on this interval the cosine's slope is at "
            "most sine of one, about 0.84, so each application shrinks distances by that factor. The errors shrink "
            "geometrically, and the theorem we're about to prove even predicts a bound for them in advance, the last "
            "column. <bookmark mark='d'/> The solution is 0.7390851332, the only one there is."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(dg), FadeIn(dl))
            vo.wait_until("a")
            self.play(Create(cg), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(web), run_time=4.0, rate_func=linear)
            self.play(FadeIn(fdot, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(head[1]), FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        pm = ProofMap([r"steps shrink like $c^n$", r"so $(x_n)$ is Cauchy", r"$X$ complete: \ $x_n \to x$",
                       r"$\varphi(x) = x$; \ unique"], font_size=22, width=2.9, buff=0.28).to_edge(UP, buff=0.2)
        if pm.width > 13.2:
            pm.width = 13.2
        ax = square_axes([-2.6, 2.6, 1], [-2.0, 2.0, 1], 1.25).move_to([-3.4, -0.8, 0])
        ax.set_opacity(0)
        star = np.array([0.5, -0.2])
        c, th = 0.62, math.radians(48)
        R = c * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        pts = [np.array([-2.0, 1.4])]
        for _ in range(10):
            pts.append(star + R @ (pts[-1] - star))
        pts = np.array(pts)
        d10 = np.linalg.norm(pts[1] - pts[0])
        for n in range(len(pts)):
            assert np.linalg.norm(pts[n] - star) <= c**n / (1 - c) * d10 + 1e-12
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.07 if n < 6 else 0.05, color=C.SEQ) for n, p in enumerate(pts)])
        steps = VGroup(*[Line(ax.c2p(*pts[n]), ax.c2p(*pts[n + 1]), color=C.EPS, stroke_width=3) for n in range(10)])
        discs = [Circle(radius=1.25 * c**n / (1 - c) * d10, color=C.CONNECTED_SET, stroke_width=2).move_to(ax.c2p(*pts[n]))
                 .set_fill(C.CONNECTED_SET, 0.06) for n in range(6)]
        xl = MathTex(r"x_0", font_size=28).next_to(dots[0], UL, buff=0.05)
        fixd = Dot(ax.c2p(*star), radius=0.09, color=WHITE)
        rows = [
            MathTex(r"d(x_{n+1}, x_n)", r"\le", r"c^n\, d(x_1, x_0)", font_size=30),
            MathTex(r"d(x_m, x_n)", r"\le", r"\frac{c^n}{1 - c}\, d(x_1, x_0)", font_size=30),
            MathTex(r"\varphi(x)", r"=", r"\lim \varphi(x_n) = \lim x_{n+1} = x", font_size=30),
            MathTex(r"d(x, y)", r"=", r"d(\varphi x, \varphi y) \le c\, d(x, y) \;\Rightarrow\; x = y", font_size=30),
        ]
        whys = [why(r"$\varphi$ shrinks every distance by $c$"), why(r"triangle inequality: \ $\le (c^n + \dots + c^{m-1})\,d(x_1, x_0)$; \ Cauchy"),
                why(r"$\varphi$ is continuous"), why(r"uniqueness")]
        step = ladder(self, rows, whys, keep=4, top=2.2, buff=0.42, x=2.0, edge=6.95)
        head = label(r"\textbf{Rudin 9.23} \ $X$ complete, \ $d(\varphi x, \varphi y) \le c\, d(x, y)$ with $c < 1$ "
                     r"$\Rightarrow$ exactly one fixed point", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem, Rudin 9.23: on a complete metric space, a map that shrinks every "
            "distance by a factor c less than one has exactly one fixed point. Start anywhere and iterate. "
            "<bookmark mark='b'/> Each step is at most c times the one before, so the n-th step is at most c to the n "
            "times the first. <bookmark mark='c'/> Adding up the steps between the n-th point and any later one gives a "
            "geometric series: every later point lies in a disc of radius c to the n over one minus c times the first "
            "step. The discs shrink to nothing, so the sequence is Cauchy. <bookmark mark='d'/> The space is complete, "
            "so the points converge, and because the map is continuous, the limit is fixed. <bookmark mark='e'/> And "
            "two fixed points would have to be closer to each other than they are, so there's only one."
        ) as vo:
            self.play(FadeIn(pm), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(xl))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(d_)) for s_, d_ in zip(steps, dots[1:])],
                                  lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(*pm.light(0))
            step(0)
            vo.wait_until("c")
            self.play(*pm.light(1))
            step(1)
            self.play(FadeIn(discs[0]))
            for k in range(1, 6):
                self.play(ReplacementTransform(discs[k - 1], discs[k]), run_time=0.6)
            vo.wait_until("d")
            self.play(*pm.light(2))
            self.play(FadeIn(fixd, scale=2))
            self.play(*pm.light(3))
            step(2)
            vo.wait_until("e")
            step(3)
            self.play(*pm.done())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def complete(self):
        xs = [Fraction(1)]
        for _ in range(5):
            xs.append(xs[-1] / 2 + 1 / xs[-1])
        assert xs[1:4] == [Fraction(3, 2), Fraction(17, 12), Fraction(577, 408)]
        for a, b in zip(xs[1:], xs[2:]):  # a contraction with c = 1/2 on [1, 2]: |phi'(x)| = |1/2 - 1/x^2| <= 1/2
            assert abs(b - (a / 2 + 1 / a)) == 0
        nl = NumberLine(x_range=[1, 2, 0.25], length=11.0, include_numbers=True, font_size=22,
                        decimal_number_config={"num_decimal_places": 2}).move_to([0, 0.4, 0])
        dots = VGroup(*[Dot(nl.n2p(float(q)), radius=0.08, color=C.SEQ) for q in xs[:5]])
        labs = VGroup(*[MathTex(rf"\tfrac{{{q.numerator}}}{{{q.denominator}}}" if q.denominator > 1 else "1",
                                font_size=30, color=C.SEQ).next_to(dots[i], UP, buff=0.15 + 0.45 * (i % 2))
                        for i, q in enumerate(xs[:4])])
        hole = VGroup(Circle(radius=0.11, color=C.HOLE, stroke_width=3).move_to(nl.n2p(math.sqrt(2))),
                      MathTex(r"\sqrt 2 \notin \mathbb Q", font_size=30, color=C.HOLE).next_to(nl.n2p(math.sqrt(2)), DOWN,
                                                                                            buff=0.55))
        head = VGroup(label(r"Why completeness matters: \ $\varphi(x) = \frac x2 + \frac1x$ on $\mathbb Q \cap [1, 2]$",
                            font_size=30),
                      label(r"maps rationals to rationals, \ and $|\varphi'(x)| = |\tfrac12 - \tfrac1{x^2}| \le \tfrac12$:"
                            r" \ a contraction", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        out = VGroup(label(r"the iterates are Cauchy, \ but their limit would be $\sqrt 2$:", font_size=26),
                     label(r"no fixed point in $\mathbb Q$ \ (Part 1's hole, \ and Newton's method for $\sqrt 2$)",
                           font_size=26, color=C.HOLE)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> Completeness can't be dropped. The map x over two plus one over x sends rationals to "
            "rationals, and on the interval from one to two it shrinks distances by at least half. "
            "<bookmark mark='b'/> Iterate from one: three halves, seventeen twelfths, five hundred seventy-seven over "
            "four hundred eight. <bookmark mark='c'/> The iterates form a Cauchy sequence, but the point they close in "
            "on is the square root of two, the hole in the rationals from Part 1. Among the rationals, there is no "
            "fixed point at all."
        ) as vo:
            self.play(FadeIn(head[0]), Create(nl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            for i in range(4):
                self.play(FadeIn(dots[i], scale=1.5), FadeIn(labs[i]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(dots[4]), Create(hole[0]), FadeIn(hole[1]))
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def newton(self):
        d = load("contraction")
        xn, nerr = d["xn"], d["nerr"]
        ax = plain_axes([0.9, 2.1, 0.5], [0.9, 2.1, 0.5], 4.6, 4.6, numbers=True, font_size=20,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.7, 0])
        t = np.linspace(0.9, 2.1, 300)
        g = t / 2 + 1 / t
        gg = polyline(ax, t, g, color=C.FUNC, stroke_width=3.5)
        dg = polyline(ax, t, t, color=GREY_B, stroke_width=2.5)
        tang = DashedLine(ax.c2p(1.0, math.sqrt(2)), ax.c2p(1.85, math.sqrt(2)), color=C.EPS, stroke_width=2.5)
        head = VGroup(label(r"Newton's method is a contraction near a simple root", font_size=30),
                      MathTex(r"g(x) = x - \frac{f(x)}{f'(x)}, \qquad g'(x) = \frac{f(x) f''(x)}{f'(x)^2} = 0 "
                              r"\text{ at the root}", font_size=30)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        gl = MathTex(r"g(x) = \frac x2 + \frac1x \quad (f = x^2 - 2)", font_size=26, color=C.FUNC).next_to(ax, UP,
                                                                                                   buff=0.05)
        tab = VGroup(MathTex(r"n", r"\quad |x_n - \sqrt 2|", font_size=28, color=GREY_A))
        for n in range(5):
            tab.add(MathTex(rf"{n}", r"\quad " + (f"{nerr[n]:.4f}" if nerr[n] > 1e-3 else sci(float(nerr[n]), 1)),
                            font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([1.5, -0.6, 0])
        regrid(tab)
        side = VGroup(label(r"flat at the fixed point:", font_size=24),
                      label(r"near it, $c$ is as small as we like,", font_size=24),
                      label(r"so each step does better than the last:", font_size=24),
                      label(r"the error squares, \ the digits double", font_size=24, color=C.EPS),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, -0.7, 0])
        for r_ in side:
            if r_.width > 3.9:
                r_.width = 3.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([3.0, -0.7, 0], RIGHT, buff=0)
        assert nerr[4] < 1e-11
        with self.voiceover(
            "<bookmark mark='a'/> And Newton's method from the opening is a contraction too. Its step is the map g of "
            "x equals x minus f over f prime, and at a simple root its derivative is zero. <bookmark mark='b'/> For "
            "the square root of two, g is flat where it crosses the diagonal, so near the root it shrinks distances by "
            "a factor as small as we like. <bookmark mark='c'/> That's why Newton's method is so fast: each step "
            "contracts harder than the one before, the error squares, and the number of correct digits doubles."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(dg))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(Create(gg), FadeIn(gl))
            self.play(Create(tang))
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=2.5)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
