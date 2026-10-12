from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import bump, load, plain_axes, polyline, trap


class Calculus(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.examples()
        self.sawtooth()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Calculus with distributions", r"How do you differentiate something that is not a function?",
                            lit=(1945,), part=9)
        with self.voiceover("Chapter three: differentiating distributions, by integrating by parts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        r1 = MathTex(r"\int f'\,\varphi", r"\;=\;", r"-\int f\,\varphi'", font_size=44)
        r2 = MathTex(r"\langle T', \varphi\rangle", r"\;=\;", r"-\langle T, \varphi'\rangle", font_size=44, color=C.EPS)
        VGroup(r1, r2).arrange(DOWN, buff=0.9).move_to([0, 0.6, 0])
        why1 = label(r"integration by parts: \ no boundary terms, \ because $\varphi$ vanishes near the edge", font_size=24,
                     color=GREY_A).next_to(r1, DOWN, buff=0.2)
        why2 = label(r"\textbf{FA 6.12} \ the definition: \ the derivative jumps onto the test function", font_size=24,
                     color=GREY_A).next_to(r2, DOWN, buff=0.2)
        notes = VGroup(
            label(r"every distribution has derivatives of every order, \ and $\partial_i\partial_j = \partial_j\partial_i$",
                  font_size=26),
            label(r"if $T_n \to T$ in $\mathcal D'$, \ then $T_n' \to T'$: \ differentiation commutes with every limit",
                  font_size=26, color=C.EPS),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        head = label(r"Move the derivative onto the test function", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> For a smooth function f, integration by parts moves the derivative onto the test "
            "function, with a minus sign, and no boundary terms, because phi vanishes near the edge. "
            "<bookmark mark='b'/> For a distribution, make that the definition: the derivative of T acts on phi as "
            "minus T acting on phi prime. <bookmark mark='c'/> Since phi can be differentiated forever, so can every "
            "distribution, and mixed partials always commute. And the swap of limits that cost so much in Part 3 is "
            "now free: if distributions converge, so do their derivatives."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Write(r1), FadeIn(why1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r1.copy(), r2), FadeIn(why2))
            self.play(Indicate(r2[2], color=C.DISTRIBUTION))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def examples(self):
        x = np.linspace(-2, 2, 2001)
        axes = [plain_axes([-2, 2, 1], [-1.4, 2.2, 1], 3.8, 2.6).move_to([-4.6 + 4.6 * k, 0.2, 0]) for k in range(3)]
        g1 = polyline(axes[0], x, np.abs(x), color=C.FUNC, stroke_width=3.5)
        g2 = VGroup(Line(axes[1].c2p(-2, -1), axes[1].c2p(0, -1), color=C.APPROX, stroke_width=3.5),
                    Line(axes[1].c2p(0, 1), axes[1].c2p(2, 1), color=C.APPROX, stroke_width=3.5))
        g3 = VGroup(Arrow(axes[2].c2p(0, 0), axes[2].c2p(0, 2.1), buff=0, color=C.DISTRIBUTION, stroke_width=6,
                          tip_length=0.2), Line(axes[2].c2p(-2, 0), axes[2].c2p(2, 0), color=C.DISTRIBUTION, stroke_width=2))
        t = VGroup(MathTex(r"|x|", font_size=28, color=C.FUNC).next_to(axes[0], UP, buff=0.05),
                   MathTex(r"|x|' = \operatorname{sign} x", font_size=28, color=C.APPROX).next_to(axes[1], UP, buff=0.05),
                   MathTex(r"(\operatorname{sign} x)' = 2\delta", font_size=28, color=C.DISTRIBUTION).next_to(axes[2], UP,
                                                                                                         buff=0.05))
        arrows = VGroup(Arrow([-2.55, 0.2, 0], [-2.05, 0.2, 0], buff=0, color=GREY_B, stroke_width=3),
                        Arrow([2.05, 0.2, 0], [2.55, 0.2, 0], buff=0, color=GREY_B, stroke_width=3))
        # checks: <H', phi> = phi(0) and <sign', phi> = 2 phi(0)
        xx = np.linspace(-3, 3, 600001)
        phi = bump((xx - 0.3) / 1.5) * (1 + 0.2 * xx)
        dphi = np.gradient(phi, xx)
        phi0 = float(bump(np.array([-0.3 / 1.5]))[0])
        H = -trap(dphi[xx >= 0], xx[xx >= 0])
        S = -trap(np.sign(xx) * dphi, xx)
        assert abs(H - phi0) < 1e-6 and abs(S - 2 * phi0) < 1e-5  # trapezoid error at the jump of sign
        rows = VGroup(
            MathTex(rf"\langle H', \varphi\rangle = -\int_0^\infty \varphi' = \varphi(0): \ \ {H:.6f} = {phi0:.6f}",
                    font_size=26),
            MathTex(rf"\langle (\operatorname{{sign}})', \varphi\rangle = -\int \operatorname{{sign}}\,\varphi' = 2\varphi(0): "
                    rf"\ \ {S:.5f}", font_size=26),
            MathTex(r"(\log|x|)' = \text{p.v.}\,\tfrac1x, \qquad (fT)' = f'T + fT' \ \ (f \in C^\infty)", font_size=26,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        head = label(r"Corners and jumps differentiate without trouble", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Now corners and jumps are no obstacle. The absolute value has derivative the sign "
            "function. <bookmark mark='b'/> The sign function jumps by two, so its derivative is two delta. "
            "<bookmark mark='c'/> Check it on a test function: minus the integral of the sign times phi prime is "
            "exactly twice phi of zero. The log of the absolute value has derivative the principal value of one over "
            "x, and the product rule survives for smooth multipliers."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(axes[0]), Create(g1), FadeIn(t[0]))
            self.play(GrowArrow(arrows[0]), Create(axes[1]), Create(g2), FadeIn(t[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), Create(axes[2]), FadeIn(g3), FadeIn(t[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[:2]))
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sawtooth(self):
        d = load("sawcomb")
        Ns, acts, target, errs = d["Ns"], d["acts"], float(d["target"]), d["errs"]
        ax = plain_axes([-7, 13, math.pi], [-2.0, 2.0, 1], 8.4, 2.0).move_to([-2.0, 1.6, 0])
        bx = plain_axes([-7, 13, math.pi], [-1.0, 3.6, 1], 8.4, 2.2).move_to([-2.0, -1.2, 0])
        segs = VGroup()
        for k in (-1, 0, 1):
            a, b = 2 * math.pi * k, 2 * math.pi * (k + 1)
            xs = np.linspace(max(a, -7) + 1e-3, min(b, 13) - 1e-3, 200)
            if len(xs) < 2 or xs[0] >= xs[-1]:
                continue
            segs.add(polyline(ax, xs, (math.pi - (xs - a)) / 2, color=C.FUNC, stroke_width=3))
        flat = Line(bx.c2p(-7, -0.5), bx.c2p(13, -0.5), color=C.APPROX, stroke_width=3)
        spikes = VGroup(*[Arrow(bx.c2p(2 * math.pi * k, -0.5), bx.c2p(2 * math.pi * k, 3.3), buff=0, color=C.DISTRIBUTION,
                                stroke_width=5, tip_length=0.18) for k in (-1, 0, 1, 2)])
        l1 = MathTex(r"f(x) = \tfrac{\pi - x}{2} \ \text{on } (0, 2\pi), \text{ periodic} = \sum_{n \ge 1}\frac{\sin nx}{n}",
                     font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.05)
        l2 = MathTex(r"f' = -\tfrac12 + \pi \sum_k \delta_{2\pi k} \ \ \text{in } \mathcal D'", font_size=26,
                     color=C.DISTRIBUTION).next_to(bx, DOWN, buff=0.1)
        tab = VGroup(MathTex(r"N", r"\quad \big|\langle \textstyle\sum_{n \le N} \cos nx, \varphi\rangle - \langle f', \varphi\rangle\big|",
                             font_size=22, color=GREY_A))
        for N, e in zip(Ns, errs):
            tab.add(MathTex(f"{int(N)}", rf"\quad {sci(float(e), 1)}", font_size=24, color=C.EPS))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.9, 0.6, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
        notes = VGroup(
            label(r"differentiate the series term by term:", font_size=22),
            MathTex(r"\sum_n \cos nx \ \text{ diverges at every } x,", font_size=24),
            label(r"but converges in $\mathcal D'$, \ to $f'$", font_size=22, color=C.EPS),
            label(r"Fourier was right, \ in the right space", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(tab, DOWN, buff=0.25)
        assert np.all(np.diff(errs) < 0) and errs[-1] < 1e-6
        head = label(r"The sawtooth, \ differentiated term by term", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the Fourier thread. The sawtooth is the sum of sine n x over n. Its "
            "derivative is minus a half between the jumps, and at each jump, up by pi, a spike: pi times delta. "
            "<bookmark mark='b'/> Now differentiate the series term by term: the sum of cos n x. At every point that "
            "series diverges. <bookmark mark='c'/> But test it against a smooth phi, and the partial sums converge, "
            "fast, to the action of the sawtooth's derivative. <bookmark mark='d'/> Term-by-term differentiation of "
            "a Fourier series, the move that started all of this, is simply correct, in the space of distributions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(segs), FadeIn(l1))
            self.play(Create(bx), Create(flat), LaggedStart(*[GrowArrow(s_) for s_ in spikes], lag_ratio=0.2), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(notes[:2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[2:]))
        self.wait(0.4)
        self.clear_scene()
