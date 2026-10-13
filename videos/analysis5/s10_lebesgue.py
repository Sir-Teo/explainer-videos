from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import area_under, interval_band, load, plain_axes, polyline


class Lebesgue(VoiceoverScene):
    def construct(self):
        self.card()
        self.properties()
        self.criterion()
        self.improper()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Lebesgue measure, and Riemann revisited",
                            r"How does the new integral compare with the old one?", lit=(1854, 1902), part=5)
        with self.voiceover("Chapter nine: Lebesgue measure, and how the new integral compares with Riemann's."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def properties(self):
        head = VGroup(label(r"\textbf{RCA 2.19--2.20} \ Lebesgue measure on $\R^k$: \ the Riesz measure of the "
                            r"Riemann integral", font_size=28)).to_edge(UP, buff=0.35)
        # three small pictures: a box, a translated set, regularity (open above, compact below)
        o1, o2, o3 = np.array([-4.6, 0.3, 0]), np.array([0.0, 0.3, 0]), np.array([4.6, 0.3, 0])
        box = Rectangle(width=2.4, height=1.4, color=C.MEASURE, fill_opacity=0.3).move_to(o1)
        bl = MathTex(r"m(\text{box}) = \text{volume}", font_size=28, color=C.MEASURE).next_to(box, DOWN, buff=0.4)
        blob_pts = [o2 + 0.9 * np.array([math.cos(t) * (1 + 0.3 * math.sin(3 * t)), math.sin(t) * 0.8, 0])
                    for t in np.linspace(0, 2 * math.pi, 80)]
        blob = Polygon(*blob_pts, color=C.SEQ, fill_opacity=0.3).shift(LEFT * 0.7)
        blob2 = blob.copy().shift(RIGHT * 1.3 + UP * 0.4).set_color(C.APPROX)
        tl = MathTex(r"m(E + x) = m(E)", font_size=28, color=C.APPROX).next_to(VGroup(blob, blob2), DOWN, buff=0.4)
        Kc = Circle(radius=0.55, color=C.COMPACT_SET, fill_opacity=0.25).move_to(o3)
        Ec = Circle(radius=0.8, color=WHITE, stroke_width=2.5).move_to(o3)
        Vc = DashedVMobject(Circle(radius=1.05, color=C.OPEN_SET, stroke_width=2.5).move_to(o3), num_dashes=40)
        rl = MathTex(r"K \subset E \subset V, \ \ m(V \setminus K) < \varepsilon", font_size=28).next_to(Vc, DOWN,
                                                                                                    buff=0.4)
        names = VGroup(label(r"boxes get their volume", font_size=24, color=GREY_A).next_to(box, UP, buff=0.5),
                       label(r"translation invariant", font_size=24, color=GREY_A).next_to(VGroup(blob, blob2), UP,
                                                                                         buff=0.4),
                       label(r"regular", font_size=24, color=GREY_A).next_to(Vc, UP, buff=0.3))
        foot = label(r"and it is the \emph{only} translation-invariant Borel measure with $m([0,1]^k) = 1$",
                     font_size=26, color=C.EPS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Feed the Riemann integral into the Riesz machine and out comes Lebesgue measure. "
            "<bookmark mark='b'/> A box gets its volume. <bookmark mark='c'/> Sliding a set doesn't change its "
            "measure. <bookmark mark='d'/> Every measurable set is squeezed between a compact set inside and an open "
            "set outside, with as little room between them as you like. <bookmark mark='e'/> And these properties "
            "pin it down: it's the only translation-invariant measure that gives the unit cube measure one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(box), FadeIn(bl), FadeIn(names[0]))
            vo.wait_until("c")
            self.play(FadeIn(blob), FadeIn(names[1]))
            self.play(TransformFromCopy(blob, blob2), FadeIn(tl))
            vo.wait_until("d")
            self.play(FadeIn(Kc), Create(Ec), Create(Vc), FadeIn(rl), FadeIn(names[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def criterion(self):
        from videos.analysis3.compute import load as load3
        th = load3("thomae")
        head = VGroup(label(r"\textbf{Lebesgue's criterion} \ (\textit{Principles} 11.33):", font_size=30),
                      label(r"a bounded $f$ on $[a, b]$ is Riemann integrable $\iff$ it is continuous almost everywhere,",
                            font_size=28),
                      label(r"and then the two integrals agree", font_size=28, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        ax = plain_axes([0, 1, 0.25], [0, 0.55, 0.25], 5.6, 2.6).move_to([-3.5, -1.0, 0])
        rats = sorted({Fraction(p, q) for q in range(2, 41) for p in range(1, q)})
        th_dots = VGroup(*[Dot(ax.c2p(float(r), 1 / r.denominator), radius=0.025, color=C.FUNC) for r in rats])
        bx = plain_axes([0, 1, 0.25], [0, 1.15, 0.5], 5.6, 2.6).move_to([3.5, -1.0, 0])
        dir_dots = VGroup(*[Dot(bx.c2p(float(r), 1), radius=0.025, color=C.PATHOLOGY) for r in rats])
        dir_zero = Line(bx.c2p(0, 0), bx.c2p(1, 0), color=C.PATHOLOGY, stroke_width=4)
        cards = VGroup(
            VGroup(label(r"Thomae: \ discontinuous on $\mathbb Q$ (measure $0$)", font_size=22),
                   label(r"Riemann: \ yes, \ $\int = 0$ \ (Part 3: $U \to 0$)", font_size=22, color=C.CONNECTED_SET),
                   label(r"Lebesgue: \ yes, \ $\int = 0$", font_size=22, color=C.CONNECTED_SET)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.2),
            VGroup(label(r"Dirichlet: \ discontinuous everywhere", font_size=22),
                   label(r"Riemann: \ no \ ($U = 1$, $L = 0$)", font_size=22, color=C.PATHOLOGY),
                   label(r"Lebesgue: \ yes, \ $\int = 0$ \ (it is $0$ a.e.)", font_size=22, color=C.CONNECTED_SET)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bx, UP, buff=0.2),
        )
        u = th["U"]
        assert float(u[-1]) < 0.01
        with self.voiceover(
            "<bookmark mark='a'/> Which functions could Riemann integrate? Lebesgue answered exactly: a bounded "
            "function is Riemann integrable if and only if its points of discontinuity form a set of measure zero, "
            "and then the two integrals agree. <bookmark mark='b'/> Thomae's function is discontinuous at the "
            "rationals, a null set: Riemann can integrate it, and so can Lebesgue. <bookmark mark='c'/> Dirichlet's "
            "function is discontinuous everywhere: Riemann cannot. Lebesgue can, because it is zero almost "
            "everywhere. Every Riemann-integrable function is Lebesgue integrable, with the same integral."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(Create(ax), LaggedStart(*[FadeIn(d_) for d_ in th_dots], lag_ratio=0.003), run_time=2.0)
            self.play(FadeIn(cards[0]))
            vo.wait_until("c")
            self.play(Create(bx), Create(dir_zero), LaggedStart(*[FadeIn(d_) for d_ in dir_dots], lag_ratio=0.003),
                      run_time=2.0)
            self.play(FadeIn(cards[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def improper(self):
        d = load("improper")
        Ns, si, absint = d["Ns"], d["si"], d["absint"]
        ax = plain_axes([0, 30, 5], [-0.3, 1.05, 0.5], 9.0, 2.8).move_to([-1.0, 0.5, 0])
        x = np.linspace(1e-6, 30, 3000)
        y = np.sin(x) / x
        pos = area_under(ax, x, np.maximum(y, 0), C.CONNECTED_SET, 0.4)
        neg = area_under(ax, x, np.minimum(y, 0), C.PATHOLOGY, 0.4)
        g = polyline(ax, x, y, color=C.FUNC, stroke_width=3)
        head = label(r"One thing Riemann can do that Lebesgue will not: \ $\int_0^\infty \frac{\sin x}{x}\,dx$",
                     font_size=30).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"N", r"\quad \int_0^N \frac{\sin x}{x}", r"\quad \int_0^N \frac{|\sin x|}{x}",
                             font_size=28, color=GREY_A))
        for N, a, b in zip(Ns, si, absint):
            tab.add(MathTex(rf"{int(N)}", rf"\quad {a:.5f}", rf"\quad {b:.4f}", font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-1.6, -2.3, 0])
        regrid(tab)
        side = VGroup(label(r"$\to \pi/2$: \ an improper", font_size=24, color=C.CONNECTED_SET),
                      label(r"Riemann integral", font_size=24, color=C.CONNECTED_SET),
                      label(r"$\approx \tfrac2\pi \log N + 1.1$: \ no", font_size=24, color=C.PATHOLOGY),
                      label(r"Lebesgue integral", font_size=24, color=C.PATHOLOGY),
                      label(r"Lebesgue integrates $|f|$", font_size=24, color=GREY_A),
                      label(r"or nothing", font_size=24, color=GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.9, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One honest caveat. Sine x over x has an improper Riemann integral from zero to "
            "infinity: the positive and negative humps cancel more and more exactly, and the integral up to N "
            "converges to pi over two. <bookmark mark='b'/> But the humps' total area, without the cancellation, "
            "grows like the logarithm of N. <bookmark mark='c'/> A Lebesgue integral requires the absolute value to "
            "have a finite integral, so this function is not Lebesgue integrable. Conditionally convergent integrals "
            "are like conditionally convergent series in Part 2: useful, but fragile."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(pos), FadeIn(neg))
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_[:2]) for r_ in tab[1:]], lag_ratio=0.3))
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:]], lag_ratio=0.3))
            self.play(FadeIn(side[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
