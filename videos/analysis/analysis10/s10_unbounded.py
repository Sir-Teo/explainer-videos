from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis10.common import load, plain_axes, polyline, square_axes, trap


class Unbounded(VoiceoverScene):
    def construct(self):
        self.card()
        self.forced()
        self.symmetric()
        self.extensions()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Unbounded operators", r"Why must the operators of physics be unbounded?", lit=(1932,),
                            part=10)
        with self.voiceover("Chapter nine: unbounded operators, where the domain is part of the operator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forced(self):
        ax = plain_axes([0, 2 * math.pi, math.pi / 2], [-9, 9, 3], 6.2, 3.6).move_to([-3.2, -0.4, 0])
        x = np.linspace(0, 2 * math.pi, 1200)
        nT = ValueTracker(1)

        def pics():
            n = int(round(nT.get_value()))
            return VGroup(polyline(ax, x, np.sin(n * x), color=C.FUNC, stroke_width=3),
                          polyline(ax, x, n * np.cos(n * x), color=C.OPERATOR, stroke_width=2.5))

        pp = always_redraw(pics)
        rd = always_redraw(lambda: MathTex(rf"n = {int(round(nT.get_value()))}: \ \ \|f'\| / \|f\| = "
                                           rf"{int(round(nT.get_value()))}", font_size=28).next_to(ax, UP, buff=0.12))
        lg = VGroup(MathTex(r"f = \sin nx", font_size=24, color=C.FUNC), MathTex(r"f' = n\cos nx", font_size=24,
                                                                                 color=C.OPERATOR)).arrange(RIGHT, buff=0.5).next_to(ax, DOWN, buff=0.15)
        # the ratio, by quadrature
        for n in (1, 3, 8):
            r = math.sqrt(trap((n * np.cos(n * x)) ** 2, x) / trap(np.sin(n * x) ** 2, x))
            assert abs(r - n) < 1e-3
        rows = VGroup(
            label(r"$\frac{d}{dx}$ and multiplication by $x$ \ (on $L^2(\mathbb R)$) \ are not bounded", font_size=24),
            label(r"\textbf{Hellinger--Toeplitz} (Part 8): \ a symmetric operator defined", font_size=22),
            label(r"on all of $H$ is bounded", font_size=22),
            label(r"so they can only live on a dense \emph{domain} $\mathcal D(T) \subsetneq H$", font_size=24,
                  color=C.EPS),
            label(r"\textbf{FA 13.1--13.9} \ the graph $\{(x, Tx)\}$; \ closed operators; \ $T^*$ through graphs",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.3, 0])
        head = label(r"Derivatives are unbounded", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Momentum is a derivative, and derivatives are not bounded: sine n x has the same "
            "size for every n, but its derivative is n times bigger. <bookmark mark='b'/> And Part 8's "
            "Hellinger-Toeplitz theorem says a symmetric operator defined on all of Hilbert space is automatically "
            "bounded. <bookmark mark='c'/> So the operators of physics can't be defined everywhere. They come with "
            "a domain, a dense subspace, and the domain is part of the operator."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(pp), FadeIn(rd), FadeIn(lg), FadeIn(rows[0]))
            for n in (2, 3, 5, 8):
                self.play(nT.animate.set_value(n), run_time=0.8, rate_func=lambda t: 1.0 if t > 0.5 else 0.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        for m in (pp, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def symmetric(self):
        ax = plain_axes([0, 1, 0.5], [-1.4, 1.4, 1], 4.6, 2.2).move_to([-4.2, 1.0, 0])
        bx = plain_axes([0, 1, 0.5], [0, 3, 1], 4.6, 2.2).move_to([-4.2, -2.0, 0])
        x = np.linspace(0, 1, 400)
        bump = np.where((x > 0.05) & (x < 0.95), np.exp(-1 / np.clip(1 - ((x - 0.5) / 0.45) ** 2, 1e-9, None)) * 2.7, 0)
        g1 = polyline(ax, x, bump, color=C.TEST_FN, stroke_width=3)
        l1 = label(r"$\mathcal D(D) = C_c^\infty(0, 1)$: \ zero near both ends", font_size=20, color=C.TEST_FN).next_to(
            ax, UP, buff=0.05)
        g2 = VGroup(polyline(bx, x, np.exp(x), color=C.PATHOLOGY, stroke_width=3),
                    polyline(bx, x, np.exp(-x), color=C.APPROX, stroke_width=3))
        l2 = MathTex(r"D^*f = \pm i f: \ \ f = e^{\pm x}", font_size=22).next_to(bx, UP, buff=0.05)
        rows = VGroup(
            MathTex(r"D = i\frac{d}{dx}, \qquad \langle Df, g\rangle - \langle f, Dg\rangle = "
                    r"i\big(f(1)\overline{g(1)} - f(0)\overline{g(0)}\big)", font_size=26),
            label(r"on $C_c^\infty(0, 1)$ the boundary term vanishes: \ $D$ is \emph{symmetric}", font_size=22),
            label(r"but $D^*$ acts on everything with $f' \in L^2$: \ no boundary conditions at all", font_size=22),
            label(r"$D^* f = \pm i f$ has solutions $e^{\pm x}$: \ deficiency indices $(1, 1)$", font_size=22,
                  color=C.PATHOLOGY),
            label(r"symmetric $\ne$ self-adjoint: \ the distinction that matters", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.4, -0.3, 0])
        for r_ in rows:
            if r_.width > 8.4:
                r_.width = 8.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.4, -0.3, 0])
        assert np.allclose(np.gradient(np.exp(x), x)[5:-5], np.exp(x)[5:-5], rtol=1e-4)
        # D* f = i f' = +i f  gives f' = f (e^x);  = -i f  gives f' = -f (e^{-x})
        assert np.allclose(1j * np.gradient(np.exp(-x), x)[5:-5], -1j * np.exp(-x)[5:-5], rtol=1e-4)
        head = label(r"The museum: \ $i\,\frac{d}{dx}$ on an interval", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the cautionary example. Take i times the derivative on the interval from "
            "zero to one, defined on smooth functions that vanish near both ends. Integration by parts gives a "
            "boundary term, which vanishes, so the operator is symmetric. <bookmark mark='b'/> But its adjoint has no "
            "boundary conditions at all, so it's much bigger. The equations D star f equals plus or minus i f have "
            "solutions, e to the x and e to the minus x: one dimension each. <bookmark mark='c'/> Symmetric is not "
            "self-adjoint, and only self-adjoint operators get a spectral theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g1), FadeIn(l1), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(Create(bx), Create(g2), FadeIn(l2), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extensions(self):
        d = load("twisted")
        t0, t1, t2 = d["t0"], d["t1"], d["t2"]
        cx = square_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], 1.0).move_to([-4.6, 0.6, 0])
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(cx.c2p(0, 0))
        thT = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(cx.c2p(math.cos(thT.get_value()), math.sin(thT.get_value())), radius=0.09,
                                        color=C.EPS))
        cl = MathTex(r"f(1) = e^{i\theta} f(0)", font_size=24, color=C.EPS).next_to(cx, DOWN, buff=0.1)
        # the ladder of eigenvalues on a vertical axis
        lad = NumberLine(x_range=[-6 * math.pi, 6 * math.pi, 2 * math.pi], length=5.6,  # ticks at 2 pi n
                         rotation=PI / 2, include_numbers=False, color=GREY_C).move_to([-0.6, -0.25, 0])
        ladl = MathTex(r"\sigma", font_size=26, color=C.SPECTRUM).next_to(lad, UP, buff=0.1)

        def rungs():
            th = thT.get_value()
            g = VGroup()
            for n in range(-4, 5):
                v = 2 * math.pi * n - th
                if abs(v) <= 6 * math.pi + 1e-9:
                    g.add(Line(lad.n2p(v) + LEFT * 0.35, lad.n2p(v) + RIGHT * 0.35, color=C.SPECTRUM, stroke_width=5))
            return g

        rg = always_redraw(rungs)
        rd = VGroup(MathTex(r"\theta =", font_size=26), DecimalNumber(0, num_decimal_places=2, font_size=26)).arrange(
            RIGHT, buff=0.12).next_to(cx, UP, buff=0.1)
        rd[1].add_updater(lambda m: m.set_value(thT.get_value()))
        tab = VGroup(MathTex(r"\theta", r"\quad \text{computed eigenvalues near } 0", r"\quad 2\pi n - \theta",
                             font_size=22, color=GREY_A))
        for th, ev in ((0.0, t0), (math.pi / 2, t1), (math.pi, t2)):
            near = np.sort(ev[np.argsort(np.abs(ev))[:3]])
            ex = 2 * math.pi * np.round((near + th) / (2 * math.pi)) - th  # the ladder's nearest rung
            assert np.allclose(near, ex, atol=1e-4)
            tab.add(MathTex(f"{th:.3f}", r"\quad " + r",\ ".join(f"{{{v:.4f}}}" for v in near),
                            r"\quad " + r",\ ".join(f"{{{v:.4f}}}" for v in ex), font_size=20))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.9, 1.4, 0])
        regrid(tab, gap=0.35, max_width=6.6)
        for th, ev in ((0.0, t0), (math.pi / 2, t1), (math.pi, t2)):
            assert all(np.min(np.abs(ev - (2 * math.pi * n - th))) < 1e-4 for n in range(-3, 4))
        rows = VGroup(
            label(r"each $\theta$ gives a self-adjoint extension of $D$", font_size=22),
            label(r"its eigenfunctions $e^{-i\lambda x}$ need $e^{-i\lambda} = e^{i\theta}$:", font_size=22),
            MathTex(r"\sigma(D_\theta) = \{2\pi n - \theta : n \in \mathbb Z\}", font_size=30, color=C.SPECTRUM),
            label(r"the spectrum depends on the boundary condition: \ one physical", font_size=22, color=C.EPS),
            label(r"symbol, \ a circle of different operators", font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.35)
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(tab, DOWN, buff=0.35)
        head = label(r"A circle of self-adjoint extensions", font_size=34).to_edge(UP, buff=0.25)
        # the ladder stands between the circle and the text: vertical, clear of both, under the title
        assert lad.get_top()[1] > lad.get_bottom()[1] + 5 and lad.get_bottom()[1] > -3.6
        assert ladl.get_top()[1] < head.get_bottom()[1] - 0.1
        assert cx.get_right()[0] < lad.get_left()[0] - 0.35 - 0.2 and lad.get_right()[0] + 0.35 < rows.get_left()[0] - 0.2
        with self.voiceover(
            "<bookmark mark='a'/> To make it self-adjoint, impose a boundary condition: f at one equals e to the i "
            "theta times f at zero, one condition for each point on a circle. <bookmark mark='b'/> Each gives a "
            "self-adjoint operator, with eigenfunctions e to the minus i lambda x, and the condition forces lambda "
            "into the ladder two pi n minus theta. Computed numerically for three values of theta, the eigenvalues "
            "match to many digits. <bookmark mark='c'/> Now turn theta around the circle. The whole ladder slides "
            "down, and after a full turn it lands on itself. The same differential expression, a circle of "
            "different operators, each with its own spectrum."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(cx), Create(circ), FadeIn(dot), FadeIn(cl), FadeIn(rd), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lad), FadeIn(ladl), FadeIn(rg), FadeIn(rows[1:3]))
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("c")
            self.play(thT.animate.set_value(2 * math.pi), run_time=6.0, rate_func=linear)
            self.play(FadeIn(rows[3:]))
        for m in (dot, rg, rd[1]):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
