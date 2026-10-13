from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline
from videos.analysis3.compute import cos_series


class PowerSeries(VoiceoverScene):
    def construct(self):
        self.card()
        self.disk()
        self.abel()
        self.spiral()
        self.pi_section()
        self.fta()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(13, r"Power series, $\exp$, and the birth of $\pi$",
                            r"Where do the sine, the cosine and $\pi$ come from?", lit=(), part=3)
        with self.voiceover(
            "Chapter thirteen. Uniform convergence pays off first for power series. Rudin uses them to define the "
            "exponential function, and from it the sine, the cosine, and the number pi, without drawing a single "
            "triangle."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def disk(self):
        d = load("power")
        r, Ng, gerr = float(d["r"]), d["Ng"], d["gerr"]
        ax = plain_axes([-1, 1, 0.5], [0, 6, 1], 7.0, 4.6).move_to([-2.9, -0.75, 0])
        x = np.linspace(-1, 0.995, 1600)
        strip = Rectangle(width=ax.c2p(r, 0)[0] - ax.c2p(-r, 0)[0], height=ax.c2p(0, 6)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=C.COMPACT_SET, fill_opacity=0.10)
        strip.move_to(((ax.c2p(-r, 0) + ax.c2p(r, 6)) / 2))
        strip_l = MathTex(r"[-r, r], \ r = 0.8", font_size=24, color=C.COMPACT_SET).next_to(strip, DOWN, buff=0.12)
        target = runs(ax, x, 1 / (1 - x), WHITE, 3.5)
        parts = [runs(ax, x, sum(x**k for k in range(int(N) + 1)), C.APPROX, 3) for N in Ng]
        tlab = MathTex(r"\frac{1}{1 - x} = \sum_{n \ge 0} x^n", font_size=30).move_to(ax.c2p(-0.5, 4.3))
        head = VGroup(label(r"\textbf{Rudin 8.1} \ radius $R$ $\Rightarrow$ uniform convergence on $[-r, r]$ for "
                            r"every $r < R$", font_size=28),
                      ).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"N", r"\quad \sup_{[-r, r]} |f - s_N| = \frac{r^{N+1}}{1 - r}", font_size=26,
                             color=GREY_A))
        for N, e in zip(Ng, gerr):
            tab.add(MathTex(rf"{int(N)}", rf"\quad {e:.5f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([4.2, 0.9, 0])
        regrid(tab, gap=0.35)
        bad = label(r"on $(-1, 1)$: \ $\sup = \infty$ for every $N$", font_size=24, color=C.PATHOLOGY)
        bad.next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        cons = VGroup(MathTex(r"f'(x) = \sum n c_n x^{n-1} \ (\text{same radius})", font_size=28, color=C.EPS),
                      MathTex(r"f \in C^\infty, \quad c_k = \frac{f^{(k)}(0)}{k!}", font_size=28, color=C.EPS)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(bad, DOWN, buff=0.3).align_to(tab, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's theorem 8.1: a power series with radius of convergence R converges "
            "uniformly on every smaller closed interval. <bookmark mark='b'/> Here's the geometric series, whose sum is "
            "one over one minus x. On the interval up to 0.8, the largest error of the N-th partial sum is 0.8 to the "
            "N plus one, over 0.2, which goes to zero. <bookmark mark='c'/> On the whole open interval the convergence "
            "is never uniform: near one the sum is unbounded, and every partial sum is bounded. <bookmark mark='d'/> "
            "Uniform convergence on each smaller interval is all chapter seven needs. The sum is continuous, and it "
            "may be differentiated term by term, since the differentiated series has the same radius. Repeating, a "
            "power series is infinitely differentiable, and its coefficients are its Taylor coefficients."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(strip), FadeIn(strip_l))
            vo.wait_until("b")
            self.play(Create(target), FadeIn(tlab), Create(parts[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            cur = parts[0]
            for k in range(1, len(Ng)):
                self.play(ReplacementTransform(cur, parts[k]), FadeIn(tab[k + 1]), run_time=1.0)
                cur = parts[k]
            vo.wait_until("c")
            self.play(FadeIn(bad))
            vo.wait_until("d")
            self.play(FadeIn(cons[0]))
            self.play(FadeIn(cons[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def abel(self):
        d = load("power")
        xs, abel, alt = d["xs"], d["abel"], d["alt"]
        head = VGroup(label(r"\textbf{Rudin 8.2} \ (Abel, 1826)", font_size=30),
                      MathTex(r"\sum c_n \text{ converges} \;\Rightarrow\; \lim_{x \to 1^-} \sum c_n x^n = \sum c_n",
                              font_size=34, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 1, 0.25], [0, 0.8, 0.2], 6.2, 3.8).move_to([-3.3, -1.0, 0])
        x = np.linspace(0, 1, 801)
        g = polyline(ax, x, np.log1p(x), color=C.FUNC, stroke_width=3.5)
        ln2 = DashedLine(ax.c2p(0, math.log(2)), ax.c2p(1, math.log(2)), color=C.EPS, stroke_width=2)
        ln2_l = MathTex(r"\ln 2", font_size=26, color=C.EPS).next_to(ax.c2p(0, math.log(2)), LEFT, buff=0.1)
        fl = MathTex(r"f(x) = \sum_{n \ge 1} \frac{(-1)^{n+1}}{n} x^n = \ln(1 + x)", font_size=28, color=C.FUNC)
        fl.next_to(ax, UP, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(float(u), float(v)), radius=0.06, color=WHITE) for u, v in zip(xs, abel)])
        tab = VGroup(MathTex(r"x", r"\quad f(x) \ (\text{summed})", font_size=26, color=GREY_A))
        for u, v in zip(xs, abel):
            tab.add(MathTex(rf"{u:g}", rf"\quad {v:.6f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.95, -0.6, 0])
        regrid(tab, gap=0.35)
        # the series at x = 1 itself: alternating partial sums closing in on ln 2
        bx = plain_axes([0, 40, 10], [0.4, 1.05, 0.2], 3.6, 2.3).move_to([5.0, -0.95, 0])
        pts = VGroup(*[Dot(bx.c2p(k + 1, float(v)), radius=0.035, color=C.SEQ) for k, v in enumerate(alt)])
        bl = DashedLine(bx.c2p(0, math.log(2)), bx.c2p(40, math.log(2)), color=C.EPS, stroke_width=1.5)
        bt = MathTex(r"1 - \tfrac12 + \tfrac13 - \cdots", font_size=26, color=C.SEQ).next_to(bx, UP, buff=0.1)
        res = MathTex(r"1 - \tfrac12 + \tfrac13 - \tfrac14 + \cdots = \ln 2 = 0.693147\ldots", font_size=30,
                      color=C.EPS).to_edge(DOWN, buff=0.25)
        conv = label(r"the converse fails: \ $\sum (-1)^n x^n = \frac{1}{1 + x} \to \frac12$, \ but $1 - 1 + 1 - \cdots$ "
                     r"diverges", font_size=22, color=GREY_A).next_to(res, UP, buff=0.15)
        assert abs(abel[-1] - math.log(2)) < 1e-4 and np.all(np.diff(abel) > 0)
        with self.voiceover(
            "<bookmark mark='a'/> At the edge of the interval, uniform convergence can fail, and Abel's theorem fills "
            "the gap: if the series converges at x equal to one, then its sum there is the limit of the function as x "
            "approaches one from below. <bookmark mark='b'/> The series with coefficients plus and minus one over n "
            "sums to the logarithm of one plus x inside the interval. <bookmark mark='c'/> At x equal to one it "
            "becomes the alternating harmonic series, which converges by Part 2's alternating test, slowly. "
            "<bookmark mark='d'/> Abel's theorem identifies its sum: the logarithm of two. Summing the series at x "
            "closer and closer to one gives values marching up to it. <bookmark mark='e'/> The converse is false: "
            "one minus one plus one, and so on, has an Abel limit of one half but no sum. That kind of averaged sum "
            "comes back in Part 7, for Fourier series."
        ) as vo:
            self.play(Create(ax), Create(ln2), FadeIn(ln2_l))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(Create(g), FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bt), Create(bl), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(tab[0]))
            for k in range(len(xs)):
                self.play(FadeIn(dots[k], scale=1.5), FadeIn(tab[k + 1]), run_time=0.5)
            self.play(Write(res))
            vo.wait_until("e")
            self.play(FadeIn(conv))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spiral(self):
        d = load("power")
        o = np.array([-3.4, -1.25, 0])
        u = 1.3
        tT = ValueTracker(float(d["tt"]))
        K = 20

        def Z(w):
            return o + u * np.array([w.real, w.imag, 0])

        axes = VGroup(Line(Z(-1.4 + 0j), Z(1.6 + 0j), color=GREY_D, stroke_width=1.5),
                      Line(Z(-1.4j), Z(2.2j), color=GREY_D, stroke_width=1.5))
        circ = DashedVMobject(Circle(radius=u, color=GREY_B, stroke_width=2).move_to(o), num_dashes=48)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / (K - 1)) for k in range(K)]

        def spiral():
            t = tT.get_value()
            terms = np.array([(1j * t) ** k / math.factorial(k) for k in range(K)])
            heads = np.concatenate([[0], np.cumsum(terms)])
            g = VGroup()
            for k in range(K):
                a, b = Z(heads[k]), Z(heads[k + 1])
                if np.linalg.norm(b - a) > 0.02:
                    g.add(Arrow(a, b, buff=0, color=cols[k], stroke_width=4, tip_length=0.14,
                                max_tip_length_to_length_ratio=0.35))
            g.add(Dot(Z(heads[-1]), radius=0.08, color=C.EPS))
            return g

        sp = always_redraw(spiral)
        arc = always_redraw(lambda: Arc(radius=u, start_angle=0, angle=max(tT.get_value(), 1e-3), arc_center=o,
                                        color=C.EPS, stroke_width=4))
        land = always_redraw(lambda: Dot(Z(complex(np.cos(tT.get_value()), np.sin(tT.get_value()))), radius=0.09,
                                         color=C.EPS))
        tl = always_redraw(lambda: MathTex(rf"t = {tT.get_value():.2f}", font_size=28, color=C.EPS).move_to(
            o + np.array([-2.1, 2.75, 0])))
        heads = d["heads"]
        head = VGroup(label(r"\textbf{Rudin 8.6--8.7} \ one series makes $\exp$, $\cos$ and $\sin$", font_size=30),
                      MathTex(r"E(z) = \sum_{n \ge 0} \frac{z^n}{n!}, \qquad E(z)E(w) = E(z + w)", font_size=32)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        side = VGroup(
            label(r"$E(x) = e^x$ for real $x$; \ now put $z = it$:", font_size=24),
            label(r"each term is the last one turned $90^\circ$ and scaled by $t/n$", font_size=24, color=C.APPROX),
            MathTex(r"|E(it)|^2 = E(it)E(-it) = E(0) = 1", font_size=28),
            MathTex(r"\cos t := \operatorname{Re} E(it), \quad \sin t := \operatorname{Im} E(it)", font_size=28,
                    color=C.EPS),
            MathTex(rf"t = 2: \ {K} \text{{ terms land on }} ({heads[-1].real:.4f},\ {heads[-1].imag:.4f})",
                    font_size=26, color=GREY_A),
            MathTex(r"|\tfrac{d}{dt} E(it)| = |iE(it)| = 1: \text{ unit speed}", font_size=28, color=C.CONNECTED_SET),
            label(r"so the arc from $1$ to $E(it)$ has length $t$ \ (chapter 4)", font_size=24, color=GREY_A),
        )
        for r_ in side:
            if r_.width > 6.6:
                r_.width = 6.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, -0.85, 0])
        assert abs(heads[-1] - complex(math.cos(2.0), math.sin(2.0))) < 1e-9
        with self.voiceover(
            "<bookmark mark='a'/> Rudin defines E of z as the sum of z to the n over n factorial, for every complex z. "
            "Multiplying two such series, by Part 2's Cauchy product, gives the law E of z times E of w equals E of z "
            "plus w, and on the real line E is the exponential function. <bookmark mark='b'/> Now put in i times t. "
            "Each term is the previous one turned by a right angle and scaled by t over n, so the partial sums spiral "
            "inward. <bookmark mark='c'/> Where do they land? E of i t times E of minus i t is E of zero, which is "
            "one, so the landing point is always on the unit circle. Its coordinates are, by definition, the cosine "
            "and the sine of t. <bookmark mark='d'/> As t grows, the spiral's endpoint runs around the circle, and "
            "since the derivative of E of i t has length one, it runs at unit speed: by chapter four, the arc it has "
            "covered has length exactly t."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(axes), Create(circ))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(sp), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            sp.clear_updaters()
            self.play(FadeOut(sp), FadeIn(land))
            self.play(tT.animate.set_value(0.0), run_time=1.2)
            self.add(arc)
            self.play(FadeIn(side[5]), tT.animate.set_value(2 * np.pi - 0.05), run_time=6.0, rate_func=linear)
            self.play(FadeIn(side[6]))
        for m in (arc, tl, land):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pi_section(self):
        d = load("power")
        br, zero = d["brackets"], float(d["zero"])
        ax = plain_axes([0, 2.2, 0.5], [-1, 1.1, 0.5], 6.8, 3.4).move_to([-3.1, 0.35, 0])
        t = np.linspace(0, 2.2, 600)
        cg = polyline(ax, t, np.array([cos_series(v) for v in t]), color=C.FUNC, stroke_width=3.5)
        cl = MathTex(r"\cos t = 1 - \frac{t^2}{2!} + \frac{t^4}{4!} - \cdots", font_size=28, color=C.FUNC)
        cl.next_to(ax.c2p(1.0, 1.05), RIGHT, buff=0.1)
        p0 = Dot(ax.c2p(0, 1), radius=0.07, color=C.CONNECTED_SET)
        p2 = Dot(ax.c2p(2, cos_series(2.0)), radius=0.07, color=C.PATHOLOGY)
        l0 = MathTex(r"\cos 0 = 1", font_size=24, color=C.CONNECTED_SET).next_to(p0, RIGHT, buff=0.12).shift(DOWN * 0.2)
        l2 = MathTex(rf"\cos 2 = {cos_series(2.0):.4f} < 0", font_size=24, color=C.PATHOLOGY).next_to(p2, DOWN,
                                                                                                buff=0.12)
        # nested brackets under the axis
        y0 = ax.c2p(0, -1)[1] - 0.25
        bars = VGroup()
        for k in range(8):
            a, b = br[k]
            pa, pb = ax.c2p(a, 0)[0], ax.c2p(b, 0)[0]
            bars.add(Line([pa, y0 - 0.16 * k, 0], [pb, y0 - 0.16 * k, 0], color=C.COMPACT_SET, stroke_width=5))
        tab = VGroup(MathTex(r"k", r"\quad 2 \times \text{midpoint}", font_size=26, color=GREY_A))
        shown = [0, 1, 2, 3, 5, 10, 20, 30, 40, 59]
        for k in shown:
            a, b = br[k]
            m = a + b
            s = f"{m:.14f}"
            good = 0
            for ch1, ch2 in zip(s, f"{math.pi:.14f}"):
                if ch1 != ch2:
                    break
                good += 1
            tab.add(MathTex(rf"{k}", r"\quad " + s[:good], r"\," + s[good:] if good < len(s) else r"", font_size=26))
            tab[-1][1].set_color(C.EPS)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.3, 0.15, 0])
        head = VGroup(label(r"\textbf{Rudin 8.7} \ $\pi$ is defined: \ twice the first zero of $\cos$", font_size=30),
                      ).to_edge(UP, buff=0.3)
        out = VGroup(MathTex(r"\pi := 2x_0 = 3.14159265358979\ldots", font_size=32, color=C.EPS),
                     MathTex(r"E(i\pi/2) = i, \quad E(2\pi i) = 1, \quad E(z + 2\pi i) = E(z)", font_size=28),
                     ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.25)
        assert abs(2 * zero - math.pi) < 1e-12 and cos_series(2.0) < 0
        with self.voiceover(
            "<bookmark mark='a'/> Now pi. The cosine series starts at one, and at t equal to two it's already negative, "
            "since after the first few terms the series alternates with shrinking terms. <bookmark mark='b'/> By the "
            "intermediate value theorem the cosine has a first positive zero, and Rudin defines pi to be twice that "
            "zero. <bookmark mark='c'/> We can find it from the series alone, by bisection: halve the interval, keep "
            "the half where the sign changes, and repeat. Twice the midpoint gains a correct digit about every three "
            "steps. <bookmark mark='d'/> After sixty halvings, it agrees with pi to twelve decimal places. The rest "
            "follows from the addition law: E of i pi over two is i, E is periodic with period two pi i, and since "
            "the circle is traced at unit speed, pi is half its circumference. Not one triangle was needed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(cg), FadeIn(cl))
            self.play(FadeIn(p0), FadeIn(l0), FadeIn(p2), FadeIn(l2))
            vo.wait_until("b")
            self.play(Flash(Dot(ax.c2p(zero, 0)), color=C.EPS))
            vo.wait_until("c")
            self.play(FadeIn(tab[0]))
            for k in range(8):
                anims = [Create(bars[k])]
                if k in shown:
                    anims.append(FadeIn(tab[shown.index(k) + 1]))
                self.play(*anims, run_time=0.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[6:]], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(out[0]))
            self.play(FadeIn(out[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fta(self):
        d = load("power")
        P, z0, rad, th, img, roots = d["P"], complex(d["z0"]), float(d["rad"]), d["th"], d["img"], d["roots"]
        # left: the z-plane; right: the w = P(z) plane
        oz, uz = np.array([-3.6, -0.9, 0]), 1.25
        ow, uw = np.array([2.6, -0.9, 0]), 1.15

        def Zp(w):
            w = np.atleast_1d(w)
            return np.c_[oz[0] + uz * w.real, oz[1] + uz * w.imag, np.zeros(len(w))]

        def Wp(w):
            w = np.atleast_1d(w)
            return np.c_[ow[0] + uw * w.real, ow[1] + uw * w.imag, np.zeros(len(w))]

        zax = VGroup(Line(Zp(-2.3)[0], Zp(1.6)[0], color=GREY_D, stroke_width=1.5),
                     Line(Zp(-1.4j)[0], Zp(1.4j)[0], color=GREY_D, stroke_width=1.5))
        wax = VGroup(Line(Wp(-1.6)[0], Wp(2.4)[0], color=GREY_D, stroke_width=1.5),
                     Line(Wp(-1.6j)[0], Wp(1.6j)[0], color=GREY_D, stroke_width=1.5))
        zl = MathTex(r"z", font_size=30, color=GREY_A).next_to(Zp(1.6)[0], UP, buff=0.1)
        wl = MathTex(r"w = P(z)", font_size=30, color=GREY_A).next_to(Wp(2.4)[0], UP, buff=0.1)
        rts = VGroup(*[Dot(Zp(r_)[0], radius=0.06, color=C.CONNECTED_SET) for r_ in roots])
        Pz0 = complex(np.polyval(P, z0))
        zd = Dot(Zp(z0)[0], radius=0.07, color=C.FUNC)
        zc = Circle(radius=uz * rad, color=C.FUNC, stroke_width=2.5).move_to(Zp(z0)[0])
        wd = Dot(Wp(Pz0)[0], radius=0.07, color=C.FUNC)
        lvl = DashedVMobject(Circle(radius=uw * abs(Pz0), color=GREY_B, stroke_width=2).move_to(ow), num_dashes=50)
        lvl_l = MathTex(r"|w| = |P(z_0)|", font_size=22, color=GREY_B).next_to(Wp(-abs(Pz0) * 0.7 - 0.75j)[0], DL,
                                                                             buff=0.05)
        wimg = VMobject(color=C.APPROX, stroke_width=3).set_points_as_corners(Wp(img))
        k = int(np.argmin(np.abs(img)))
        wbest = Dot(Wp(img[k])[0], radius=0.07, color=C.EPS)
        zbest = Dot(Zp(z0 + rad * np.exp(1j * th[k]))[0], radius=0.07, color=C.EPS)
        # repeat the step: a descent that ends at a root
        path, z = [z0], z0
        for _ in range(40):
            Pv, dP = np.polyval(P, z), np.polyval(np.polyder(P), z)
            rho = min(0.25, 0.6 * abs(Pv) / max(abs(dP), 1e-9))
            cand = z + rho * np.exp(1j * th)
            z = cand[np.argmin(np.abs(np.polyval(P, cand)))]
            path.append(z)
            if abs(np.polyval(P, z)) < 1e-4:
                break
        path = np.array(path)
        assert abs(np.polyval(P, path[-1])) < 1e-3 and np.all(np.diff(np.abs(np.polyval(P, path))) < 0)
        zpath = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners(Zp(path))
        wpath = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners(Wp(np.polyval(P, path)))
        head = VGroup(label(r"\textbf{Rudin 8.8} \ every nonconstant polynomial has a complex root", font_size=30),
                      label(r"$P(z) = z^3 - 2z + 2$: \ $|P| \to \infty$, so $|P|$ has a smallest value, at some $z_0$",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        step = label(r"if $P(z_0) \ne 0$: \ a small circle around $z_0$ maps to a loop around $P(z_0)$, "
                     r"which dips closer to $0$", font_size=24, color=C.APPROX).to_edge(DOWN, buff=0.75)
        part7 = label(r"Part 7: \ the same fact in one line, from Liouville's theorem", font_size=22, color=GREY_B)
        part7.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> One more gift of these series: the fundamental theorem of algebra, Rudin 8.8. The "
            "size of a polynomial grows without bound far out, so it has a smallest value somewhere. "
            "<bookmark mark='b'/> Suppose that smallest value were not zero. Take a small circle around the point. "
            "Its image under P is a loop around P of z zero, <bookmark mark='c'/> and a loop around a point can't stay "
            "outside the circle through that point: part of it dips closer to zero. So the value wasn't the smallest "
            "after all. <bookmark mark='d'/> Repeat the step from the new point, and the values march down to zero, "
            "at a root. In Part 7 the same theorem will take one line."
        ) as vo:
            self.play(FadeIn(head[0]), Create(zax), Create(wax), FadeIn(zl), FadeIn(wl), FadeIn(zd), FadeIn(wd))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(lvl), FadeIn(lvl_l))
            vo.wait_until("b")
            self.play(Create(zc), Create(wimg), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(zbest, scale=1.5), FadeIn(wbest, scale=1.5), FadeIn(step))
            vo.wait_until("d")
            self.play(Create(zpath), Create(wpath), run_time=2.5)
            self.play(FadeIn(rts), FadeIn(part7))
        self.wait(0.4)
        self.clear_scene()
