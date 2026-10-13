from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, square_axes, zcurve
from videos.analysis7.compute import contour


def F(z):
    return np.exp(z) * np.cos(2 * z) + z**3


class CauchyFormula(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.series()
        self.liouville()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Cauchy's formula and its miracles", r"How can the boundary know the inside?", lit=(1821,),
                            part=7)
        with self.voiceover("Chapter three: Cauchy's integral formula, the engine of the whole subject."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def formula(self):
        d = load("cauchy")
        a_pts, err = d["a"], float(d["err"])
        S = 4.8
        cx = square_axes([-1.2, 1.2, 0.5], [-1.2, 1.2, 0.5], S / 2.4).move_to([-3.5, -0.6, 0])
        img = cplot(cx, F, (-1.2, 1.2), (-1.2, 1.2))
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 0))
        circ = Circle(radius=cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0], color=WHITE, stroke_width=3).move_to(cx.c2p(0, 0))
        f_l = MathTex(r"f(z) = e^z \cos 2z + z^3", font_size=28).next_to(frame, UP, buff=0.1)
        tT = ValueTracker(0.0)

        def apos():
            t = tT.get_value()
            return 0.55 * np.exp(1j * t) * (0.6 + 0.4 * math.cos(3 * t))

        ad = always_redraw(lambda: Dot(cx.c2p(apos().real, apos().imag), radius=0.08, color=WHITE))

        def reads():
            a = apos()
            v = contour(lambda z: F(z) / (z - a), 0, 1.0, 1024)
            fa = F(np.array([a]))[0]
            return VGroup(
                MathTex(rf"a = {a.real:+.3f} {a.imag:+.3f}i", font_size=28),
                MathTex(rf"\tfrac{{1}}{{2\pi i}}\oint \tfrac{{f(z)}}{{z - a}}dz = {v.real:+.5f} {v.imag:+.5f}i", font_size=28,
                        color=C.EPS),
                MathTex(rf"f(a) = {fa.real:+.5f} {fa.imag:+.5f}i", font_size=28, color=C.EPS),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, 0.7, 0])

        rd = always_redraw(reads)
        dots = VGroup(*[Dot(cx.c2p(a.real, a.imag), radius=0.045, color=WHITE) for a in a_pts])
        thm = VGroup(
            label(r"\textbf{RCA 10.15} \ $f$ holomorphic on a convex $\Omega$, \ $\gamma$ a closed path in $\Omega$:",
                  font_size=24),
            MathTex(r"f(a)\,\mathrm{Ind}_\gamma(a) = \frac{1}{2\pi i}\oint_\gamma \frac{f(z)}{z - a}\,dz", font_size=34,
                    color=C.EPS),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        notes = VGroup(
            MathTex(rf"\text{{30 random points: largest error }} {sci(err, 1)}", font_size=26, color=GREY_A),
            label(r"at the center: \ $f(0) = \frac{1}{2\pi}\int_0^{2\pi} f(e^{i\theta})\,d\theta$, \ an average", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -1.5, 0])
        assert err < 1e-12
        with self.voiceover(
            "<bookmark mark='a'/> Cauchy's formula: for a holomorphic function, the value at any point inside a "
            "circle is an integral of the values on the circle. The boundary knows the inside. "
            "<bookmark mark='b'/> Move a point a around inside. The integral and the value agree, digit for digit. "
            "<bookmark mark='c'/> At thirty random points the largest disagreement is a rounding error. At the "
            "center the formula says the value is the average over the circle."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), FadeIn(img), Create(frame), FadeIn(f_l), Create(circ))
            vo.wait_until("b")
            self.play(FadeIn(ad), FadeIn(rd))
            self.play(tT.animate.set_value(2 * math.pi), run_time=6.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        for m in (ad, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def series(self):
        d = load("cauchy")
        fib = d["fib"]
        cx = square_axes([-2.0, 1.2, 0.5], [-1.4, 1.4, 0.5], 1.65).move_to([-3.6, -0.55, 0])
        img = cplot(cx, lambda Z: 1 / (1 - Z - Z * Z), (-2.0, 1.2), (-1.4, 1.4))
        frame = Rectangle(width=3.2 * 1.65, height=2.8 * 1.65, color=GREY_C, stroke_width=2).move_to(cx.c2p(-0.4, 0))
        R = (math.sqrt(5) - 1) / 2
        u = cx.c2p(1, 0)[0] - cx.c2p(0, 0)[0]
        c05 = Circle(radius=0.5 * u, color=WHITE, stroke_width=3).move_to(cx.c2p(0, 0))
        cR = DashedVMobject(Circle(radius=R * u, color=C.EPS, stroke_width=3).move_to(cx.c2p(0, 0)), num_dashes=40)
        poles = VGroup(*[Square(side_length=0.2, color=WHITE, stroke_width=2).move_to(cx.c2p(p, 0))
                         for p in (R, -1 - R)])
        f_l = MathTex(r"f(z) = \frac{1}{1 - z - z^2}", font_size=30).next_to(frame, UP, buff=0.1)
        F_ = [1, 1]
        while len(F_) < 16:
            F_.append(F_[-1] + F_[-2])
        assert np.allclose(fib, F_, atol=1e-9)
        coef = VGroup(
            MathTex(r"c_n = \frac{1}{2\pi i}\oint_{|z| = 1/2} \frac{f(z)}{z^{n+1}}\,dz", font_size=30),
            MathTex(r"= " + r",\ ".join(f"{v:.6f}" for v in fib[:5]) + r",\ \ldots", font_size=24, color=C.EPS),
            MathTex(r"= " + r",\ ".join(str(int(round(v))) for v in fib[:14]) + r",\ \ldots", font_size=26, color=C.EPS),
            label(r"Fibonacci! \ ($f = \sum F_{n+1} z^n$)", font_size=24, color=GREY_A),
            label(r"\textbf{RCA 10.16} \ holomorphic $\Rightarrow$ a power series in every disk inside $\Omega$:",
                  font_size=24),
            label(r"here it converges for $|z| < \frac{\sqrt5 - 1}{2} = 0.618$, \ the nearest pole", font_size=24,
                  color=C.EPS),
            label(r"so $f$ has derivatives of every order \ (and Morera: the converse)", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -0.5, 0])
        for r_ in coef:
            if r_.width > 6.4:
                r_.width = 6.4
        coef.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -0.5, 0])
        head = label(r"The first miracle: \ every holomorphic function is a power series", font_size=32).to_edge(UP,
                                                                                                          buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Expand the Cauchy kernel, one over z minus a, as a geometric series, and the "
            "formula turns into a power series. The coefficients are integrals over a circle. "
            "<bookmark mark='b'/> Try it on one over one minus z minus z squared, integrating over the circle of "
            "radius one half. <bookmark mark='c'/> The integrals come out as one, one, two, three, five, eight: the "
            "Fibonacci numbers. <bookmark mark='d'/> The series converges out to the nearest pole, at 0.618, the "
            "golden ratio's reciprocal. That's the first miracle: one complex derivative gives a convergent power "
            "series, and so derivatives of every order."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(coef[0]))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(frame), FadeIn(f_l), Create(c05), Create(poles))
            vo.wait_until("c")
            self.play(FadeIn(coef[1]))
            self.play(FadeIn(coef[2:4]))
            vo.wait_until("d")
            self.play(Create(cR), FadeIn(coef[4:6]))
            self.play(FadeIn(coef[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def liouville(self):
        d = load("cauchy")
        roots, rs, counts = d["roots"], d["rs"], d["counts"]
        p = np.poly1d([1, 0, -2, 0.3, 1.1, -0.4])
        ax = square_axes([-1.7, 1.7, 1], [-1.7, 1.7, 1], 1.3).move_to([-4.4, -0.75, 0])
        ax.set_opacity(0.35)
        rd = VGroup(*[Dot(ax.c2p(r.real, r.imag), radius=0.07, color=C.EPS) for r in roots])
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 4) for k in range(5)]
        u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        circs = [Circle(radius=r * u, color=c, stroke_width=2.5).move_to(ax.c2p(0, 0)) for r, c in zip(rs, cols)]
        bx = square_axes([-2.6, 2.6, 1], [-2.6, 2.6, 1], 0.62).move_to([0.2, -0.75, 0])
        bx.set_opacity(0.35)
        th = np.linspace(0, 2 * np.pi, 1500)
        imgs = []
        for r, c in zip(rs, cols):
            w = p(r * np.exp(1j * th))
            w = w / np.abs(w) ** 0.7  # compress the size, keep the angle
            imgs.append(zcurve(bx, w, c, 2.5))
        o = Dot(bx.c2p(0, 0), radius=0.07, color=WHITE)
        b_l = label(r"$p(\text{circle})$, \ size compressed", font_size=22, color=GREY_A).next_to(bx, UP, buff=0.1)
        tab = VGroup(MathTex(r"r", r"\quad \tfrac{1}{2\pi i}\oint \tfrac{p'}{p}", r"\quad \#\text{roots}", font_size=26,
                             color=GREY_A))
        for r, k in zip(rs, counts):
            tab.add(MathTex(f"{r}", rf"\quad {int(k)}", rf"\quad {int(np.sum(np.abs(roots) < r))}", font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 0.6, 0])
        regrid(tab, center=True)
        for i, row in enumerate(tab[1:]):
            row.set_color(cols[i])
        notes = VGroup(
            label(r"Cauchy: \ $|f^{(n)}(a)| \le n!\,M / R^n$", font_size=24),
            label(r"\textbf{10.23} \ Liouville: \ bounded entire $\Rightarrow$ constant", font_size=24, color=C.EPS),
            label(r"\textbf{10.25} \ no roots $\Rightarrow$ $1/p$ bounded entire:", font_size=24),
            label(r"so every $p$ has a root \ (Part 3's promise)", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -2.0, 0])
        for r_ in notes:
            if r_.width > 4.4:
                r_.width = 4.4
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.65, -2.0, 0])
        head = label(r"Counting roots with integrals: \ $p(z) = z^5 - 2z^3 + 0.3z^2 + 1.1z - 0.4$", font_size=30).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Cauchy's formula also bounds derivatives: on a circle of radius R where f is at "
            "most M, the n-th derivative is at most n factorial M over R to the n. A bounded function that's "
            "holomorphic on the whole plane can take R as large as it likes, so its derivative is zero: that's "
            "Liouville's theorem. <bookmark mark='b'/> If a polynomial had no roots, one over it would be bounded and "
            "entire, hence constant. So every polynomial has a root: the fundamental theorem of algebra, the promise "
            "from Part 3. <bookmark mark='c'/> The integral of p prime over p counts the roots inside a circle: it's "
            "the winding number of the image curve around zero. <bookmark mark='d'/> For five circles it counts "
            "zero, one, two, three and five roots, exactly the roots inside."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(notes[:2]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2:]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(rd), Create(bx), FadeIn(o), FadeIn(b_l), FadeIn(tab[0]))
            vo.wait_until("d")
            for k in range(len(rs)):
                self.play(Create(circs[k]), Create(imgs[k]), FadeIn(tab[k + 1]), run_time=1.1)
        self.wait(0.4)
        self.clear_scene()
