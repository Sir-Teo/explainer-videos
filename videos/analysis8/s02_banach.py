from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import between, load, p_ball, plain_axes, polyline, square_axes


class Banach(VoiceoverScene):
    def construct(self):
        self.card()
        self.gallery()
        self.bounded()
        self.volterra()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Banach spaces and bounded operators", r"Which linear maps are continuous?", lit=(1932,),
                            part=8)
        with self.voiceover("Chapter one: complete normed spaces, named after Stefan Banach, and the maps between them."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gallery(self):
        icons = []
        names = [r"$\ell^1$", r"$\ell^2$", r"$\ell^\infty$", r"$C[0, 1]$, \ sup", r"$c_0$: \ $x_n \to 0$", r"$L^p(\mu)$"]
        notes_ = [r"$\sum |x_n|$", r"$(\sum |x_n|^2)^{1/2}$", r"$\sup |x_n|$", r"$\sup |f|$", r"$\sup |x_n|$",
                  r"$(\int |f|^p)^{1/p}$"]
        for k in range(6):
            ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 0.75).move_to([-4.6 + 4.6 * (k % 3), 1.1 - 3.0 * (k // 3), 0])
            ax.set_opacity(0.3)
            if k < 3:
                pic = p_ball(ax, (1.0, 2.0, np.inf)[k], C.DIST)
            elif k == 3:
                x = np.linspace(-1.2, 1.2, 200)
                pic = VGroup(between(ax, x, np.ones_like(x), -np.ones_like(x), C.EPS, 0.15),
                             polyline(ax, x, 0.8 * np.sin(3 * x) * np.exp(-x * x / 2), color=C.FUNC, stroke_width=3))
            elif k == 4:
                pic = VGroup(*[Line(ax.c2p(-1.1 + 0.2 * j, 0), ax.c2p(-1.1 + 0.2 * j, 1.1 * 0.8**j * (-1) ** j),
                                    color=C.SEQ, stroke_width=4) for j in range(12)])
            else:
                x = np.linspace(-1.2, 1.2, 200)
                y = np.exp(-4 * (x - 0.3) ** 2) - 0.5 * np.exp(-6 * (x + 0.5) ** 2)
                pic = VGroup(between(ax, x, np.abs(y), np.zeros_like(x), C.MEASURE, 0.35), polyline(ax, x, y, color=C.FUNC,
                                                                                                    stroke_width=3))
            t = label(names[k], font_size=26).next_to(ax, UP, buff=0.05)
            n_ = label(notes_[k], font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.05)
            icons.append(VGroup(ax, pic, t, n_))
        head = VGroup(label(r"\textbf{RCA 5.1--5.3} \ a Banach space: \ a vector space with a norm, \ complete", font_size=30),
                      label(r"the spaces of Parts 3, 5 and 6, \ now in one family", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> A Banach space is a vector space with a norm in which every Cauchy sequence "
            "converges. We've met many. <bookmark mark='b'/> The sequence spaces, with the sum, square-sum and "
            "supremum norms, whose unit balls we know as the diamond, the circle and the square. "
            "<bookmark mark='c'/> The continuous functions with the sup norm, from Part 3; the sequences that tend to "
            "zero; and the L p spaces of Part 6. Every theorem in this part holds for all of them at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in icons[:3]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in icons[3:]], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bounded(self):
        T = np.array([[1.3, 0.6], [0.2, 0.8]])
        s = np.linalg.svd(T, compute_uv=False)
        ax = square_axes([-2.0, 2.0, 1], [-2.0, 2.0, 1], 1.35).move_to([-3.8, -0.6, 0])
        ax.set_opacity(0.35)
        th = np.linspace(0, 2 * np.pi, 361)
        unit = VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners([ax.c2p(math.cos(a), math.sin(a)) for a in th])
        img_pts = np.c_[np.cos(th), np.sin(th)] @ T.T
        img = VMobject(color=C.OPERATOR, stroke_width=3.5, fill_color=C.OPERATOR, fill_opacity=0.15).set_points_as_corners(
            [ax.c2p(*p) for p in img_pts])
        big = DashedVMobject(Circle(radius=s[0] * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), color=C.EPS, stroke_width=2.5)
                             .move_to(ax.c2p(0, 0)), num_dashes=50)
        assert abs(np.linalg.norm(img_pts, axis=1).max() - s[0]) < 1e-3
        rows = VGroup(
            label(r"\textbf{RCA 5.4} \ for a linear $\Lambda: X \to Y$, \ equivalent:", font_size=26),
            label(r"(a) \ $\Lambda$ is bounded: \ $\|\Lambda x\| \le C\|x\|$", font_size=26),
            label(r"(b) \ $\Lambda$ is continuous", font_size=26),
            label(r"(c) \ $\Lambda$ is continuous at one point", font_size=26),
            MathTex(r"\|\Lambda\| = \sup_{\|x\| \le 1} \|\Lambda x\|", font_size=32, color=C.EPS),
            label(r"why: \ $\|\Lambda x - \Lambda y\| = \|\Lambda(x - y)\| \le C\|x - y\|$", font_size=22, color=GREY_A),
            label(r"$B(X, Y)$ with this norm is a Banach space whenever $Y$ is one", font_size=24, color=C.OPERATOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.1, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.1, -0.5, 0])
        lab = VGroup(MathTex(r"\|x\| \le 1", font_size=24, color=GREY_B).next_to(ax.c2p(0.5, -0.9), DOWN, buff=0.05),
                     MathTex(rf"\|T\| = {s[0]:.3f}", font_size=26, color=C.EPS).next_to(ax, UP, buff=0.05))
        head = label(r"For linear maps, \ continuous means bounded", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A linear map between normed spaces is continuous exactly when it's bounded: it "
            "stretches no vector by more than a fixed factor. And if it's continuous at one point, it's continuous "
            "everywhere, because linearity moves that point anywhere. <bookmark mark='b'/> The smallest such factor is "
            "the operator norm: the radius of the smallest ball containing the image of the unit ball. "
            "<bookmark mark='c'/> With this norm, the bounded operators themselves form a Banach space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:4]), Create(ax), Create(unit))
            vo.wait_until("b")
            self.play(TransformFromCopy(unit, img), run_time=1.5)
            self.play(Create(big), FadeIn(lab), FadeIn(rows[4:6]))
            vo.wait_until("c")
            self.play(FadeIn(rows[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def volterra(self):
        d = load("volterra")
        s, exact, nrm = d["s"], d["exact"], float(d["norm"])
        ax = plain_axes([0, 1, 0.25], [0, 1.5, 0.5], 5.4, 2.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.5, 0.55, 0])
        x = np.linspace(0, 1, 400)
        f = math.sqrt(2) * np.cos(math.pi * x / 2)
        Vf = math.sqrt(2) * (2 / math.pi) * np.sin(math.pi * x / 2)
        gf = polyline(ax, x, f, color=C.SEQ, stroke_width=3.5)
        gV = polyline(ax, x, Vf, color=C.OPERATOR, stroke_width=3.5)
        lf = MathTex(r"f = \sqrt2\cos\tfrac{\pi x}{2}, \ \|f\|_2 = 1", font_size=24, color=C.SEQ).next_to(ax.c2p(0.28, 1.45),
                                                                                                    RIGHT, buff=0.05)
        lV = MathTex(r"Vf = \tfrac{2}{\pi}\sqrt2\sin\tfrac{\pi x}{2}", font_size=24, color=C.OPERATOR).next_to(
            ax.c2p(0.55, 0.55), DOWN, buff=0.1)
        xx = np.linspace(0, 1, 100001)
        fx = math.sqrt(2) * np.cos(math.pi * xx / 2)
        cumf = np.concatenate([[0], np.cumsum((fx[1:] + fx[:-1]) / 2 * np.diff(xx))])
        assert np.abs(cumf - math.sqrt(2) * (2 / math.pi) * np.sin(math.pi * xx / 2)).max() < 1e-8
        bx = plain_axes([0.5, 8.5, 1], [0, 0.7, 0.2], 5.4, 1.9, numbers=True, font_size=18,
                        x_axis_config={"include_numbers": False},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.5, -2.75, 0])
        kl = VGroup(*[MathTex(str(k), font_size=18).next_to(bx.c2p(k, 0), DOWN, buff=0.1) for k in range(1, 9)],
                    MathTex("k", font_size=20, color=GREY_A).next_to(bx.c2p(8.5, 0), DOWN, buff=0.1).shift(RIGHT * 0.2))
        bars = VGroup(*[Rectangle(width=0.35, height=bx.c2p(0, v)[1] - bx.c2p(0, 0)[1], stroke_width=0, fill_color=C.OPERATOR,
                                  fill_opacity=0.85).move_to(bx.c2p(k + 1, v / 2)) for k, v in enumerate(s[:8])])
        ticks = VGroup(*[Line(bx.c2p(k + 1 - 0.3, 2 / ((2 * k + 1) * math.pi)), bx.c2p(k + 1 + 0.3, 2 / ((2 * k + 1) * math.pi)),
                              color=C.EPS, stroke_width=3) for k in range(8)])
        b_l = VGroup(label(r"singular values (bars)", font_size=20, color=GREY_A),
                     label(r"$\frac{2}{(2k - 1)\pi}$ (ticks)", font_size=20, color=C.EPS)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.08).next_to(bx.c2p(8.5, 0.62), DL, buff=0)
        rows = VGroup(
            MathTex(r"(Vf)(x) = \int_0^x f(t)\,dt \ \text{ on } L^2[0, 1]", font_size=30),
            MathTex(r"\|V\| = \frac{2}{\pi}", font_size=36, color=C.EPS),
            MathTex(rf"\text{{computed (2000 points): }} {nrm:.6f}", font_size=26),
            MathTex(rf"2/\pi = {2 / math.pi:.6f}", font_size=26, color=GREY_A),
            label(r"the extremal $f$ is a quarter cosine wave", font_size=24),
            label(r"the singular values fall to $0$: \ $V$ is \emph{compact} (ch.~11)", font_size=24, color=C.OPERATOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.3, -0.4, 0])
        assert abs(nrm - 2 / math.pi) < 1e-5 and np.allclose(s[:6], exact, atol=1e-4)
        head = label(r"The norm of an integral operator", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> An operator from analysis: integrate from zero to x. On L two of the unit interval, "
            "how much can it stretch a function? <bookmark mark='b'/> The answer is two over pi. The function stretched "
            "most is a quarter of a cosine wave: integrating it gives a quarter sine wave, two over pi times as long. "
            "<bookmark mark='c'/> A discretization with two thousand points agrees to six digits. "
            "<bookmark mark='d'/> The other singular values follow the same pattern, two over three pi, two over five "
            "pi, falling to zero. That makes this operator compact, which chapter eleven explains."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(ax))
            vo.wait_until("b")
            self.play(Create(gf), FadeIn(lf))
            self.play(TransformFromCopy(gf, gV), FadeIn(lV), FadeIn(rows[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(rows[2:5]))
            vo.wait_until("d")
            self.play(Create(bx), FadeIn(kl), FadeIn(b_l), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15),
                      run_time=2.0)
            self.play(FadeIn(ticks), FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
