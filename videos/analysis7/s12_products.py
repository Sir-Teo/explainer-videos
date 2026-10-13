from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, square_axes, zcurve
from videos.analysis7.s11_harmonic import tour_tag


def sinprod(Z, N):
    P = np.pi * Z
    for n in range(1, N + 1):
        P = P * (1 - Z * Z / (n * n))
    return P


class ZerosProducts(VoiceoverScene):
    def construct(self):
        self.card()
        self.products()
        self.blaschke()
        self.continuation()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"A tour: products and continuation", r"Is a function determined by its zeros?", lit=(),
                            part=7)
        with self.voiceover("Chapter eleven, still on tour: functions built from their zeros, and functions continued "
                            "along paths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def products(self):
        d = load("products")
        Ns, errs = d["Ns"], d["errs"]
        cx = square_axes([-3.2, 3.2, 1], [-1.2, 1.2, 1], 1.0).move_to([-2.6, 1.2, 0])
        dx = square_axes([-3.2, 3.2, 1], [-1.2, 1.2, 1], 1.0).move_to([-2.6, -1.75, 0])
        exact = cplot(cx, lambda Z: np.sin(np.pi * Z), (-3.2, 3.2), (-1.2, 1.2))
        f1 = Rectangle(width=6.4, height=2.4, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        f2 = Rectangle(width=6.4, height=2.4, color=GREY_C, stroke_width=2).move_to(dx.c2p(0, 0))
        parts = [cplot(dx, lambda Z, N=N: sinprod(Z, N), (-3.2, 3.2), (-1.2, 1.2)) for N in (1, 2, 3, 10)]
        l1 = MathTex(r"\sin \pi z", font_size=28).next_to(f1, RIGHT, buff=0.15)
        lps = [MathTex(rf"\pi z \prod_{{n \le {N}}}\Big(1 - \frac{{z^2}}{{n^2}}\Big)", font_size=26).next_to(f2, RIGHT,
                                                                                                      buff=0.15)
               for N in (1, 2, 3, 10)]
        tab = VGroup(MathTex(r"N", r"\quad \text{rel. error on } |x| \le 3.2,\ |y| \le 1.2", font_size=22, color=GREY_A))
        for N, e in zip(Ns, errs):
            tab.add(MathTex(f"{N}", rf"\quad {sci(float(e), 2)}", font_size=24, color=C.EPS))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, -1.6, 0])
        regrid(tab)
        thm = label(r"\textbf{RCA 15.10} \ (Weierstrass) \ every entire function is a product over its zeros \ (with "
                    r"convergence factors)", font_size=22, color=C.EPS).to_edge(DOWN, buff=0.15)
        assert np.all(np.diff(np.log10(errs)) < -0.9)
        with self.voiceover(
            "<bookmark mark='a'/> A polynomial is a product over its roots. Euler guessed that sine of pi z should be "
            "one too, over the integers. <bookmark mark='b'/> Build the product one pair of zeros at a time: each "
            "factor plants two more dark points, and the picture fills in toward the sine. <bookmark mark='c'/> The "
            "error shrinks by a factor of ten for every factor of ten in the number of terms. "
            "<bookmark mark='d'/> Weierstrass proved that every entire function is such a product, once convergence "
            "factors are attached, and that any sequence of points going to infinity is the zero set of some entire "
            "function."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(exact), Create(f1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(parts[0]), Create(f2), FadeIn(lps[0]))
            for k in range(1, 4):
                self.play(FadeIn(parts[k]), FadeTransform(lps[k - 1], lps[k]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blaschke(self):
        d = load("products")
        ak, s = d["ak"], float(d["blaschke_sum"])

        def B(Z):
            out = np.ones_like(Z)
            for a in ak:
                out = out * (np.abs(a) / a) * (a - Z) / (1 - np.conj(a) * Z)
            return out

        S = 4.6
        cx = square_axes([-1.02, 1.02, 1], [-1.02, 1.02, 1], S / 2.04).move_to([-3.4, -0.6, 0])
        img = cplot(cx, B, (-1.02, 1.02), (-1.02, 1.02), px=800, mask=lambda Z: np.abs(Z) <= 1)
        unit = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=WHITE, stroke_width=2).move_to(cx.c2p(0, 0))
        zs = VGroup(*[Circle(radius=0.05, color=WHITE, stroke_width=1.5).move_to(cx.c2p(a.real, a.imag)) for a in ak[:12]])
        rows = VGroup(
            label(r"a bounded holomorphic function on the disk", font_size=24),
            label(r"with zeros $a_k = (1 - \frac{1}{(k + 1)^2})\, e^{ik}$:", font_size=24),
            MathTex(r"B(z) = \prod_k \frac{|a_k|}{a_k}\,\frac{a_k - z}{1 - \bar a_k z}", font_size=30),
            MathTex(rf"\sum_k (1 - |a_k|) = {s:.4f} < \infty", font_size=28, color=C.EPS),
            label(r"\textbf{RCA 15.21, 15.23} \ the zeros of a bounded $f \not\equiv 0$", font_size=22),
            label(r"on $D$ always satisfy $\sum (1 - |a_k|) < \infty$, \ and conversely", font_size=22),
            label(r"(Jensen's formula: \ zeros cost size)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        th = np.linspace(0, 2 * np.pi, 400)
        assert np.allclose(np.abs(B(np.exp(1j * th))), 1, atol=1e-9)  # each factor has size 1 on the circle
        head = label(r"How many zeros can a bounded function on the disk have?", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> In the disk, zeros can pile up toward the edge, but not too fast. Here's a Blaschke "
            "product, built from forty zeros spiraling outward. Each factor has size one on the circle, so the "
            "product stays bounded. <bookmark mark='b'/> What makes it converge is that the zeros approach the "
            "boundary quickly enough: the distances to the circle have a finite sum. For a bounded function, that's "
            "also necessary: by Jensen's formula, every zero costs size."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(img), Create(unit), FadeIn(zs), FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def continuation(self):
        ax = square_axes([-1.5, 1.5, 1], [-1.5, 1.5, 1], 1.4).move_to([-4.4, -0.7, 0])
        ax.set_opacity(0.35)
        t = np.linspace(0, 4 * np.pi, 800)
        z = (1 + 0.08 * t / (4 * np.pi)) * np.exp(1j * t)
        path = zcurve(ax, z, C.EPS, 3)
        o = Dot(ax.c2p(0, 0), radius=0.07, color=WHITE)
        bx = square_axes([0, 4 * np.pi, np.pi], [0, 4 * np.pi, np.pi], 0.32).move_to([0.6, -0.7, 0])
        arg = np.unwrap(np.angle(z))
        stair = VMobject(color=C.EPS, stroke_width=3.5).set_points_as_corners([bx.c2p(a, b) for a, b in zip(t, arg)])
        lv = VGroup(*[DashedLine(bx.c2p(0, 2 * np.pi * k), bx.c2p(4 * np.pi, 2 * np.pi * k), color=GREY_C, stroke_width=1.5)
                      for k in (1, 2)])
        lvl = VGroup(*[MathTex(rf"{k * 2}\pi" if k > 0 else "0", font_size=22).next_to(bx.c2p(0, 2 * np.pi * k), LEFT,
                                                                                      buff=0.1) for k in (0, 1, 2)])
        b_l = MathTex(r"\mathrm{Im}\log z \text{ along the path}", font_size=26, color=C.EPS).next_to(bx, UP, buff=0.1)
        assert abs(arg[-1] - arg[0] - 4 * np.pi) < 1e-9
        rows = VGroup(
            label(r"continue $\log z$ along a path \ (ch.~16):", font_size=22),
            label(r"each turn around $0$ adds $2\pi i$", font_size=22, color=C.EPS),
            label(r"monodromy: \ homotopic paths give the", font_size=22),
            label(r"same continuation \ (16.15)", font_size=22),
            label(r"Picard's little theorem: \ a nonconstant", font_size=22, color=C.PATHOLOGY),
            label(r"entire function misses at most", font_size=22, color=C.PATHOLOGY),
            label(r"one value \ ($e^z$ misses $0$)", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.1, -0.6, 0])
        for r_ in rows:
            if r_.width > 3.6:
                r_.width = 3.6
        head = label(r"Analytic continuation: \ the logarithm as a spiral staircase", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The identity theorem makes continuation unique along any path. Follow the logarithm "
            "around the origin twice. <bookmark mark='b'/> Its imaginary part, the angle, climbs without ever "
            "returning: two pi after one turn, four pi after two. The continued logarithm lives on a spiral "
            "staircase. <bookmark mark='c'/> The monodromy theorem says paths that can be deformed into each other "
            "give the same result, and the modular function proves Picard's little theorem: a nonconstant entire "
            "function takes every complex value, with at most one exception."
        ) as vo:
            self.add(tour_tag())
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(o), Create(bx), FadeIn(b_l), FadeIn(lv), FadeIn(lvl))
            vo.wait_until("b")
            self.play(Create(path), Create(stair), run_time=4.0, rate_func=linear)
            self.play(FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            self.play(FadeIn(rows[4:]))
        self.wait(0.4)
        self.clear_scene()
