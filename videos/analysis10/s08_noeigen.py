from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes, polyline, trap


class NoEigenvectors(VoiceoverScene):
    def construct(self):
        self.card()
        self.multiplication()
        self.approximate()
        self.born()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"A spectrum with no eigenvectors", r"What can ``diagonalize'' mean with nothing to "
                                                                    r"diagonalize?", lit=(), part=10)
        with self.voiceover("Chapter seven: an operator with a whole interval of spectrum and not one eigenvector."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def multiplication(self):
        ax = plain_axes([0, 1, 0.25], [-1.6, 1.6, 0.5], 5.8, 3.0, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, 0.4, 0])
        x = np.linspace(0, 1, 801)
        f = np.sin(7 * x) * np.exp(-x) + 0.6 * np.cos(3 * x)
        g1 = polyline(ax, x, f, color=C.FUNC, stroke_width=3.5)
        g2 = polyline(ax, x, x * f, color=C.OPERATOR, stroke_width=3.5)
        l1 = MathTex(r"f", font_size=26, color=C.FUNC).next_to(ax.c2p(0.05, f[40]), UP, buff=0.1)
        l2 = MathTex(r"Mf = xf", font_size=26, color=C.OPERATOR).next_to(ax.c2p(0.9, x[720] * f[720]), DOWN, buff=0.15)
        lam = 0.6
        inv = np.where(np.abs(x - lam) > 0.004, 1 / (x - lam), np.nan)
        bx = plain_axes([0, 1, 0.25], [-40, 40, 20], 5.8, 2.0).move_to([-3.4, -2.4, 0])
        gi = runs(bx, x, np.nan_to_num(inv, nan=1e9), C.PATHOLOGY, 3)
        il = MathTex(r"\tfrac{1}{x - 0.6}: \text{ unbounded}", font_size=24, color=C.PATHOLOGY).next_to(bx, RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(r"(Mf)(x) = x\,f(x) \ \text{ on } L^2[0, 1]", font_size=30, color=C.OPERATOR),
            label(r"self-adjoint: \ $\langle Mf, g\rangle = \int x f \bar g = \langle f, Mg\rangle$", font_size=22),
            label(r"$(M - \lambda)^{-1}$ is multiplication by $\frac{1}{x - \lambda}$:", font_size=22),
            label(r"bounded exactly when $\lambda \notin [0, 1]$, \ so", font_size=22),
            MathTex(r"\sigma(M) = [0, 1]", font_size=34, color=C.SPECTRUM),
            label(r"but $(x - \lambda)f(x) = 0$ a.e. \ forces $f = 0$ a.e.:", font_size=22),
            label(r"no eigenvalues, \ no eigenvectors", font_size=24, color=C.PATHOLOGY),
            label(r"it is quantum mechanics' position operator", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.2, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        head = label(r"Multiplication by $x$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Multiply every function by x. That's a bounded self-adjoint operator on L two of "
            "zero to one, and it's quantum mechanics' position operator. <bookmark mark='b'/> Its resolvent is "
            "multiplication by one over x minus lambda, which is bounded exactly when lambda is outside the "
            "interval. So the spectrum is the whole interval from zero to one. <bookmark mark='c'/> But it has no "
            "eigenvectors: x minus lambda times f vanishing almost everywhere forces f itself to vanish almost "
            "everywhere. A full interval of spectrum, and nothing to diagonalize."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g1), FadeIn(l1), FadeIn(rows[:2]))
            self.play(TransformFromCopy(g1, g2), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]), Create(bx), Create(gi), FadeIn(il))
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5:7]))
            self.play(FadeIn(rows[7]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def approximate(self):
        d = load("multop")
        ws, ratios, c = d["ws"], d["ratios"], float(d["c"])
        lam = 0.4
        ax = plain_axes([0, 1, 0.25], [0, 11, 5], 6.2, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.4, 0])
        x = np.linspace(0, 1, 4001)
        wT = ValueTracker(0.2)

        def bumpf():
            w_ = wT.get_value()
            psi = np.where(np.abs(x - lam) < w_, np.cos(math.pi * (x - lam) / (2 * w_)), 0.0)
            psi /= math.sqrt(trap(psi**2, x))
            return polyline(ax, x, np.minimum(psi, 11), color=C.FUNC, stroke_width=3.5)

        g = always_redraw(bumpf)
        rd = always_redraw(lambda: MathTex(
            rf"w = {wT.get_value():.4f}: \ \ \frac{{\|(M - 0.4)\psi\|}}{{\|\psi\|}} = {c * wT.get_value():.5f}", font_size=28,
            color=C.EPS).next_to(ax, UP, buff=0.12))
        mark = DashedLine(ax.c2p(lam, 0), ax.c2p(lam, 11), color=C.SPECTRUM, stroke_width=2)
        ml = MathTex(r"\lambda = 0.4", font_size=22, color=C.SPECTRUM).next_to(ax.c2p(lam, 0), DOWN, buff=0.35)
        tab = VGroup(MathTex(r"w", r"\quad \text{ratio (quadrature)}", font_size=22, color=GREY_A))
        for w_, r_ in zip(ws, ratios):
            tab.add(MathTex(f"{w_:g}", rf"\quad {r_:.6f}", font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([3.4, 1.0, 0])
        regrid(tab)
        assert np.allclose(ratios, c * ws, rtol=1e-4)
        rows = VGroup(
            MathTex(r"= w\sqrt{\tfrac13 - \tfrac{2}{\pi^2}} \to 0", font_size=28, color=C.EPS),
            label(r"approximate eigenvectors: \ $\lambda$ is in the spectrum", font_size=24),
            label(r"because $M - \lambda$ has no bounded inverse,", font_size=22, color=GREY_A),
            label(r"not because anything is mapped to $\lambda$ times itself", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.3)
        head = label(r"Almost eigenvectors", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> What makes 0.4 part of the spectrum, then? Take a bump centered at 0.4 and squeeze "
            "it. <bookmark mark='b'/> M minus 0.4 makes it small relative to its size, by a factor proportional to "
            "the width, so the ratio goes to zero. <bookmark mark='c'/> These are approximate eigenvectors: they "
            "show that M minus lambda can't have a bounded inverse, even though nothing is ever mapped exactly to "
            "lambda times itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(mark), FadeIn(ml), FadeIn(g), FadeIn(rd))
            vo.wait_until("b")
            self.play(wT.animate.set_value(0.00625), run_time=4.0, rate_func=lambda t: t**0.5)
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2), FadeIn(rows[0]),
                      run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]))
        for m in (g, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def born(self):
        d = load("multop")
        xs, dens, mean = d["xs"], d["dens"], float(d["mean"])
        ax = plain_axes([0, 1, 0.25], [0, 15, 5], 6.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, -0.3, 0])
        area = Polygon(*([ax.c2p(a, y) for a, y in zip(xs, dens)] + [ax.c2p(1, 0), ax.c2p(0, 0)]), stroke_width=0,
                       fill_color=C.MEASURE, fill_opacity=0.45)
        curve = polyline(ax, xs, dens, color=C.MEASURE, stroke_width=3)
        om = (0.5, 0.7)
        m = (xs >= om[0]) & (xs <= om[1])
        prob = trap(dens[m], xs[m])
        band = Rectangle(width=ax.c2p(om[1], 0)[0] - ax.c2p(om[0], 0)[0], height=ax.c2p(0, 15)[1] - ax.c2p(0, 0)[1],
                         stroke_color=C.EPS, stroke_width=2, fill_color=C.EPS, fill_opacity=0.08).move_to(
            ax.c2p(0.6, 7.5))
        bl = MathTex(r"\omega = [0.5, 0.7]", font_size=22, color=C.EPS).next_to(band, UP, buff=0.05)
        total = trap(dens, xs)
        assert abs(total - 1) < 1e-3 and 0 < prob < 1
        rows = VGroup(
            label(r"``diagonalizing'' $M$ means: \ $f(M)$ is multiplication by $f$", font_size=22),
            label(r"a state $\psi$ has a \emph{spectral measure} on $\sigma(M) = [0, 1]$:", font_size=22),
            MathTex(r"\mu_\psi(\omega) = \langle \mathbf 1_\omega(M)\psi, \psi\rangle = \int_\omega |\psi(x)|^2\,dx",
                    font_size=26, color=C.MEASURE),
            MathTex(rf"\mu_\psi([0, 1]) = {total:.4f}, \quad \mu_\psi([0.5, 0.7]) = {prob:.4f}", font_size=24),
            MathTex(rf"\langle M\psi, \psi\rangle = \int x\,d\mu_\psi = {mean:.4f}", font_size=24),
            label(r"the Born rule: \ the probability that position lies in $\omega$", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        head = label(r"Diagonalized, \ without eigenvectors", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> So what can diagonalizing mean here? M is already diagonal, in a continuous "
            "sense: any function of M is just multiplication by that function. <bookmark mark='b'/> And each state "
            "psi spreads a unit of mass over the spectrum: the measure of a set omega is the integral of psi "
            "squared over omega. <bookmark mark='c'/> That's the Born rule: the probability that the particle's "
            "position lies in omega. The total is one, and the average of x is the expected position. "
            "<bookmark mark='d'/> The spectral theorem will say every self-adjoint operator looks like this."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(area), Create(curve), FadeIn(rows[1:3]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(band), FadeIn(bl), FadeIn(rows[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
