from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline, square_axes


class OpenMapping(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.closed_graph()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Open mappings and closed graphs", r"When is the inverse of a bounded map bounded?", lit=(),
                            part=8)
        with self.voiceover("Chapter five: Baire's second and third children, the open mapping and closed graph "
                            "theorems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        d = load("openmap")
        T, s, r_in, img = d["T"], d["s"], float(d["r_in"]), d["img"]
        s2_min, s2_max = float(d["s2_min"]), float(d["s2_max"])
        ax = square_axes([-1.55, 1.55, 1], [-1.55, 1.55, 1], 1.3).move_to([-4.3, -0.55, 0])
        assert np.abs(img).max() < 1.5  # T(B) inside the drawn window
        ax.set_opacity(0.35)
        u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        unit = Circle(radius=u, color=GREY_B, stroke_width=2.5).move_to(ax.c2p(0, 0))
        ell = VMobject(color=C.OPERATOR, stroke_width=3.5, fill_color=C.OPERATOR, fill_opacity=0.15).set_points_as_corners(
            [ax.c2p(*p) for p in img])
        inner = Circle(radius=r_in * u, color=C.EPS, stroke_width=3).move_to(ax.c2p(0, 0))
        l_ = VGroup(MathTex(r"T(B)", font_size=26, color=C.OPERATOR).next_to(ax.c2p(1.2, 1.0), UR, buff=0.0),
                    MathTex(rf"\text{{yellow: radius }} 1/\|T^{{-1}}\| = {r_in:.3f}", font_size=24, color=C.EPS).next_to(
                        ax, DOWN, buff=0.12))
        pm = ProofMap([r"Baire: \ some $\overline{T(nB)}$ has interior", r"so $\overline{T(B)} \supset \delta B_Y$",
                       r"completeness: \ drop the bar \ (an iteration)"], font_size=20, width=3.6, buff=0.22,
                      direction=DOWN).move_to([0.3, -0.6, 0])
        rows = VGroup(
            label(r"$\ell^2$, \ 60 coordinates: \ $T = I + K$", font_size=22),
            MathTex(rf"\|T\| = {s2_max:.3f}, \ \ 1/\|T^{{-1}}\| = {s2_min:.3f}", font_size=24),
            label(r"50 random $y$ with $\|y\| < 0.99/\|T^{-1}\|$:", font_size=22, color=GREY_A),
            label(r"each is $Tx$ with $\|x\| \le 1$", font_size=22, color=C.EPS),
            label(r"\textbf{RCA 5.10} \ a bounded bijection", font_size=22),
            label(r"has a bounded inverse", font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([4.85, -0.6, 0])
        for r_ in rows:
            if r_.width > 3.4:
                r_.width = 3.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([4.85, -0.6, 0])
        assert rows.get_right()[0] < 6.6 and rows.get_left()[0] > pm.get_right()[0] + 0.3
        thm = VGroup(label(r"\textbf{RCA 5.9} \ (open mapping) \ $X, Y$ Banach, \ $T: X \to Y$ bounded, linear and onto:",
                           font_size=26),
                     MathTex(r"T(B_X) \supset \delta\, B_Y \ \text{ for some } \delta > 0", font_size=32, color=C.EPS)
                     ).arrange(DOWN, buff=0.1)
        head = label(r"The open mapping theorem", font_size=34).to_edge(UP, buff=0.3)
        thm.next_to(head, DOWN, buff=0.2)
        assert thm.get_bottom()[1] > max(ax.get_top()[1], l_[0].get_top()[1]) + 0.1
        with self.voiceover(
            "<bookmark mark='a'/> The open mapping theorem: a bounded linear map of one Banach space onto another "
            "sends the unit ball to a set that contains a ball. <bookmark mark='b'/> In the plane, the image of the "
            "disk is an ellipse, and the largest disk inside it has radius one over the norm of the inverse. "
            "<bookmark mark='c'/> In infinite dimensions that's a theorem. Baire says some multiple of the image is "
            "dense in a ball; completeness, through an iteration, removes the word dense. "
            "<bookmark mark='d'/> Checked on sixty coordinates of l two: fifty random targets inside the predicted "
            "ball are all hit from inside the unit ball. The consequence: a bounded bijection between Banach spaces "
            "has a bounded inverse, for free."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm), Create(ax), Create(unit))  # the unit ball under the statement
            vo.wait_until("b")
            self.play(TransformFromCopy(unit, ell), FadeIn(l_[0]), run_time=1.5)
            self.play(Create(inner), FadeIn(l_[1]))
            vo.wait_until("c")
            self.play(FadeIn(pm))
            for k in range(3):
                self.play(*pm.light(k), run_time=0.6)
            self.play(*pm.done())
            vo.wait_until("d")
            self.play(FadeIn(rows[:4]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed_graph(self):
        ax = plain_axes([0, 2 * math.pi, math.pi / 2], [-2.6, 2.6, 1], 5.6, 3.2).move_to([-3.4, -0.7, 0])
        x = np.linspace(0, 2 * math.pi, 1200)
        ns = (1, 2, 4)
        cols = [C.SEQ, C.APPROX, C.EPS]
        fs = [polyline(ax, x, np.sin(n * x) / math.sqrt(math.pi), color=c, stroke_width=2.5) for n, c in zip(ns, cols)]
        dfs = [DashedVMobject(polyline(ax, x, n * np.cos(n * x) / math.sqrt(math.pi), color=c, stroke_width=2.5),
                              num_dashes=60) for n, c in zip(ns, cols)]
        for n in ns:
            nf = math.sqrt(np.sum((np.sin(n * x[:-1]) / math.sqrt(math.pi)) ** 2) * (x[1] - x[0]))
            assert abs(nf - 1) < 1e-3
        assert max(n for n in ns) / math.sqrt(math.pi) < 2.6  # the tallest derivative fits the window
        key = MathTex(r"f_n = \frac{\sin nx}{\sqrt\pi}: \ \|f_n\|_2 = 1, \quad n = ", "1", r",\ ", "2", r",\ ", "4",
                      font_size=24)
        for i_, c_ in zip((1, 3, 5), cols):
            key[i_].set_color(c_)
        lab = VGroup(key.next_to(ax, UP, buff=0.05),
                     MathTex(r"\text{dashed: } f_n' = \frac{n\cos nx}{\sqrt\pi}: \ \|f_n'\|_2 = n", font_size=24).next_to(
                         ax, DOWN, buff=0.1))
        rows = VGroup(
            label(r"\textbf{FA 2.15} \ (closed graph) \ $T: X \to Y$ linear,", font_size=24),
            label(r"$X, Y$ Banach, \ graph closed in $X \times Y$ \ $\Rightarrow$ \ $T$ bounded", font_size=24, color=C.EPS),
            label(r"(open mapping applied to $x \mapsto (x, Tx)$)", font_size=22, color=GREY_A),
            label(r"\textbf{Hellinger--Toeplitz} \ a symmetric operator", font_size=24),
            label(r"defined on \emph{all} of a Hilbert space is bounded", font_size=24, color=C.EPS),
            label(r"$i\frac{d}{dx}$ is symmetric on $L^2$ (periodic $f$), \ and unbounded:", font_size=24),
            label(r"so it can only live on a domain: \ Part 10's unbounded operators", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.5, 0])
        # 'a': the graph of T in X x Y is closed: points (x_n, T x_n) on it converge to a point on it
        gx = square_axes([-3, 3, 1], [-2, 2, 1], 0.8).move_to(ax.get_center())
        gx.set_opacity(0.4)
        xs_ = 1.5 + 1.3 * (-0.72) ** np.arange(14)
        assert abs(xs_[-1] - 1.5) < 0.02
        gline = Line(gx.c2p(-3, -1.8), gx.c2p(3, 1.8), color=C.OPERATOR, stroke_width=3.5)
        gdots = VGroup(*[Dot(gx.c2p(v, 0.6 * v), radius=0.06, color=C.SEQ) for v in xs_])
        glim = Dot(gx.c2p(1.5, 0.9), radius=0.09, color=C.EPS)
        glab = VGroup(MathTex(r"\text{graph of } T = \{(x, Tx)\} \subset X \times Y", font_size=24, color=C.OPERATOR).next_to(
                          gx, UP, buff=0.08),
                      MathTex(r"(x_n, Tx_n) \to (x, y) \Rightarrow y = Tx", font_size=24, color=C.EPS).next_to(gx, DOWN, buff=0.1),
                      MathTex("X", font_size=22, color=GREY_B).next_to(gx.c2p(3, 0), DOWN, buff=0.08),
                      MathTex("Y", font_size=22, color=GREY_B).next_to(gx.c2p(0, 2), RIGHT, buff=0.1))
        glab[0].next_to(gx, UP, buff=0.3)
        assert glab[0].get_bottom()[1] > glab[3].get_top()[1] + 0.05
        gpic = VGroup(gx, gline, gdots, glim, glab)
        head = label(r"The closed graph theorem, \ and why derivatives need domains", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The closed graph theorem: a linear map between Banach spaces whose graph is closed is "
            "automatically bounded. It's the open mapping theorem applied to the graph. <bookmark mark='b'/> A "
            "striking corollary, due to Hellinger and Toeplitz: a symmetric operator defined on all of a Hilbert space "
            "is bounded. <bookmark mark='c'/> i times the derivative is symmetric on periodic functions, but sine n x "
            "over root pi has norm one while its derivative has norm n. So differentiation can't be defined on all of L "
            "two. It must live on a smaller domain, and that's why Part 10 needs unbounded operators."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:3]), Create(gx), Create(gline), FadeIn(glab[0]), FadeIn(glab[2:]))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in gdots], lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(glim, scale=2), FadeIn(glab[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("c")
            self.play(FadeOut(gpic), run_time=0.5)
            self.play(Create(ax), FadeIn(lab[0]))
            for k in range(3):
                self.play(Create(fs[k]), Create(dfs[k]), run_time=0.9)
            self.play(FadeIn(lab[1]), FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
