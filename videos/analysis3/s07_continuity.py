from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline


def fl(x):
    return 0.9 + 0.5 * np.sin(1.7 * x) + 0.18 * np.cos(4.1 * x)


# f_n wiggles around f with amplitude A = eps/3; its troughs X0 and Y0 = X0 + 2 pi / 9 straddle f's maximum at equal
# heights, so the two vertical hops are a full band tall and the hop along f_n is short
A_N = 0.12
_t = np.linspace(0, 1.5, 150001)
X0 = float(_t[np.argmin(np.abs(fl(_t) - fl(_t + 2 * np.pi / 9)) + 10 * (_t < 0.6))])
Y0 = X0 + 2 * np.pi / 9
PHI = 1.5 * np.pi - 9 * X0


def fn(x):
    return fl(x) + A_N * np.sin(9 * x + PHI)


class UniformContinuity(VoiceoverScene):
    def construct(self):
        self.card()
        self.three_hops()
        self.dini()
        self.camera()
        self.peano()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Uniform limits, and the space $C(X)$", r"What survives a uniform limit?", lit=(), part=3)
        with self.voiceover(
            "Chapter six. Uniform convergence preserves continuity, and that turns the continuous functions into a "
            "space of their own, with distances, where Cauchy sequences converge."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def three_hops(self):
        ax = plain_axes([0, 3, 1], [0, 1.8, 0.5], 7.6, 4.8).move_to([-2.6, -0.8, 0])
        gf = ax.plot(fl, x_range=[0, 3, 0.005], color=WHITE, stroke_width=3)
        gn = ax.plot(fn, x_range=[0, 3, 0.005], color=C.FUNC, stroke_width=3.5)
        t = np.linspace(0, 3, 3000)
        band_r = float(np.abs(fn(t) - fl(t)).max())
        assert abs(band_r - A_N) < 1e-4
        top = [ax.c2p(a, b) for a, b in zip(t[::12], fl(t[::12]) + band_r)]
        bot = [ax.c2p(a, b) for a, b in zip(t[::-12], fl(t[::-12]) - band_r)]
        band = Polygon(*top, *bot, stroke_width=0, fill_color=C.EPS, fill_opacity=0.18)
        lf = MathTex(r"f", font_size=32).next_to(ax.c2p(3, fl(3)), RIGHT, buff=0.1)
        ln = MathTex(r"f_n", font_size=32, color=C.FUNC).next_to(ax.c2p(3, fn(3)), UR, buff=0.05)
        x0, y0 = X0, Y0
        # f_n lies a full band below f at x and at y: the hops (down at x, up at y) are a full band tall
        assert abs(fl(x0) - fn(x0) - band_r) < 1e-6 and abs(fl(y0) - fn(y0) - band_r) < 1e-6
        assert abs(fn(x0) - fn(y0)) < band_r / 10 and 0.6 < x0 < y0 < 2.4
        P = [ax.c2p(x0, fl(x0)), ax.c2p(x0, fn(x0)), ax.c2p(y0, fn(y0)), ax.c2p(y0, fl(y0))]
        dots = VGroup(Dot(P[0], radius=0.07, color=WHITE), Dot(P[1], radius=0.07, color=C.FUNC),
                      Dot(P[2], radius=0.07, color=C.FUNC), Dot(P[3], radius=0.07, color=WHITE))
        hops = VGroup(Arrow(P[0], P[1], buff=0.03, color=C.EPS, stroke_width=5, tip_length=0.12,
                            max_tip_length_to_length_ratio=0.45),
                      ax.plot(fn, x_range=[x0, y0, 0.002], color=C.DELTA, stroke_width=7),
                      Arrow(P[2], P[3], buff=0.03, color=C.EPS, stroke_width=5, tip_length=0.12,
                            max_tip_length_to_length_ratio=0.45))
        xl = VGroup(MathTex(r"x", font_size=28).next_to(ax.c2p(x0, 0), DOWN, buff=0.12),
                    MathTex(r"y", font_size=28).next_to(ax.c2p(y0, 0), DOWN, buff=0.12))
        rows = VGroup(
            label(r"\textbf{Rudin 7.12} \ uniform limits of continuous functions are continuous", font_size=28),
            MathTex(r"|f(x) - f(y)| \le", r"|f(x) - f_n(x)|", r"+", r"|f_n(x) - f_n(y)|", r"+", r"|f_n(y) - f(y)|",
                    font_size=30),
            MathTex(r"<", r"\tfrac{\varepsilon}{3}", r"+", r"\tfrac{\varepsilon}{3}", r"+", r"\tfrac{\varepsilon}{3}",
                    font_size=30),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.25)
        rows[1][1].set_color(C.EPS)
        rows[1][3].set_color(C.DELTA)
        rows[1][5].set_color(C.EPS)
        rows[2].next_to(rows[1], DOWN, buff=0.12).align_to(rows[1][1], LEFT)
        side = VGroup(label(r"uniform: \ one $n$ for both $x$ and $y$", font_size=24, color=C.EPS),
                      label(r"$f_n$ continuous: \ $y$ close to $x$", font_size=24, color=C.DELTA),
                      label(r"(the $\varepsilon/3$ trick)", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.15)
        side.move_to([4.6, -1.2, 0])
        with self.voiceover(
            "<bookmark mark='t'/> Suppose continuous functions f n converge uniformly to f. Why is f continuous? "
            "<bookmark mark='a'/> Pick n so large that f n lies within epsilon over three of f everywhere: the band. "
            "<bookmark mark='b'/> To compare f at x and at a nearby y, take three hops. Down from f of x to f n of x: "
            "less than epsilon over three, by uniform convergence. <bookmark mark='c'/> Along the graph of f n to f n "
            "of y: less than epsilon over three, because f n is continuous and y is close to x. "
            "<bookmark mark='d'/> Up to f of y: less than epsilon over three, by uniform convergence again, and "
            "crucially with the same n, because the convergence is uniform. Pointwise convergence would let the n "
            "needed at y be different, and the argument would collapse."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(rows[0]), Create(ax), Create(gf), FadeIn(lf))
            vo.wait_until("a")
            self.play(FadeIn(band), Create(gn), FadeIn(ln))
            vo.wait_until("b")
            self.play(FadeIn(dots[0]), FadeIn(xl), FadeIn(rows[1][0]))
            self.play(GrowArrow(hops[0]), FadeIn(dots[1]), FadeIn(rows[1][1]), FadeIn(rows[2][:2]))
            vo.wait_until("c")
            self.play(Create(hops[1]), FadeIn(dots[2]), FadeIn(rows[1][2:4]), FadeIn(rows[2][2:4]))
            vo.wait_until("d")
            self.play(GrowArrow(hops[2]), FadeIn(dots[3]), FadeIn(rows[1][4:]), FadeIn(rows[2][4:]))
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dini(self):
        d = load("dini")
        ns, err = d["ns"], d["err"]
        ax = plain_axes([0, 1, 0.25], [0.9, 2.8, 0.5], 6.0, 4.4).move_to([-3.2, -0.7, 0])
        x = np.linspace(0, 1, 400)
        ge = ax.plot(np.exp, x_range=[0, 1, 0.005], color=WHITE, stroke_width=3)
        cols = [interpolate_color(ManimColor(GREY_C), ManimColor(C.APPROX), i / (len(ns) - 1)) for i in range(len(ns))]
        curves = VGroup(*[polyline(ax, x, (1 + x / n) ** n, color=cols[i], stroke_width=2.5) for i, n in enumerate(ns)])
        n1l = MathTex(r"n = 1", font_size=24, color=cols[0]).next_to(ax.c2p(1, 2.0), RIGHT, buff=0.1)
        el = MathTex(r"e^x", font_size=30).next_to(ax.c2p(1, np.e), RIGHT, buff=0.1)
        head = VGroup(label(r"\textbf{Rudin 7.13} \ (Dini) \ $K$ compact, \ $f_n$ continuous and monotone in $n$, \ "
                            r"limit continuous", font_size=28),
                      label(r"$\Rightarrow$ the convergence is uniform", font_size=28, color=C.EPS)
                      ).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"f_n(x) = \left(1 + \tfrac{x}{n}\right)^n \nearrow e^x", font_size=30, color=C.APPROX))
        for i, (n, e) in enumerate(zip(ns, err)):
            if n in (1, 2, 4, 10, 20, 100):
                tab.add(MathTex(rf"n = {n}: \ \sup|e^x - f_n| = {e:.4f}", font_size=26, color=cols[i]))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -0.3, 0])
        warn = label(r"drop compactness and it fails: \ $x^n \searrow 0$ on $[0, 1)$, \ never uniformly", font_size=24,
                     color=C.PATHOLOGY).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Sometimes pointwise convergence upgrades itself to uniform for free. <bookmark mark='a'/> Dini's theorem: "
            "on a compact set, if continuous functions converge monotonically to a continuous limit, the convergence "
            "is uniform. <bookmark mark='b'/> Here one plus x over n, to the n, increases to e to the x on the interval "
            "from zero to one. The worst gap is at x equal to one, and it shrinks steadily. "
            "<bookmark mark='c'/> Compactness matters: x to the n decreases to zero on the half-open interval, and "
            "the convergence is not uniform."
        ) as vo:
            self.play(Create(ax), Create(ge), FadeIn(el))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(tab), FadeIn(n1l), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(warn))
        assert np.all(np.diff(err) < 0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def camera(self):
        d = load("cauchyc")
        x, ns, B, err, coords, lim = d["x"], d["ns"], d["B"], d["err"], d["coords"], d["lim"]
        lax = plain_axes([0, 1, 0.5], [0, 0.55, 0.25], 5.4, 3.8).move_to([-3.6, -0.7, 0])
        target = polyline(lax, x, np.abs(x - 0.5), color=WHITE, stroke_width=3)
        mapax = plain_axes([-0.15, 0.3, 0.15], [-0.05, 0.4, 0.15], 4.0, 4.0).move_to([3.5, -0.6, 0])
        cam = FunctionCamera(mapax, lambda c: (c[0], c[1]))
        u_l = MathTex(r"f(\tfrac12)", font_size=26, color=GREY_B).next_to(mapax, DOWN, buff=0.1)
        v_l = MathTex(r"f(0.4)", font_size=26, color=GREY_B).next_to(mapax, LEFT, buff=0.1)
        probes = VGroup(DashedLine(lax.c2p(0.5, 0), lax.c2p(0.5, 0.55), color=GREY_B, stroke_width=1.2),
                        DashedLine(lax.c2p(0.4, 0), lax.c2p(0.4, 0.55), color=GREY_B, stroke_width=1.2),
                        MathTex(r"\tfrac12", font_size=24, color=GREY_B).next_to(lax.c2p(0.5, 0.5), RIGHT, buff=0.08),
                        MathTex(r"0.4", font_size=22, color=GREY_B).next_to(lax.c2p(0.4, 0.5), LEFT, buff=0.08))
        lim_dot = Dot(mapax.c2p(*lim), radius=0.09, color=WHITE)
        head = VGroup(label(r"\textbf{Rudin 7.15} \ $C(X)$ with $d(f, g) = \sup |f - g|$ is a complete metric space",
                            font_size=28),
                      label(r"each function is one point; \ on the right, two of its coordinates", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        seq_l = label(r"Bernstein polynomials of $|x - \tfrac12|$", font_size=24, color=C.APPROX).next_to(lax, UP, buff=0.1)
        curves = [polyline(lax, x, B[i], color=C.APPROX, stroke_width=3) for i in range(len(ns))]
        jg = int(np.argmax(np.abs(B[0] - np.abs(x - 0.5))))
        gap = Line(lax.c2p(x[jg], abs(x[jg] - 0.5)), lax.c2p(x[jg], B[0][jg]), color=C.DIST, stroke_width=6)
        gap_l = MathTex(rf"d(f, g) = \sup|f - g| = {err[0]:.3f}", font_size=28, color=C.DIST).next_to(lax, DOWN,
                                                                                                buff=0.15)
        assert abs(abs(B[0][jg] - abs(x[jg] - 0.5)) - err[0]) < 1e-12
        dots = [Dot(mapax.c2p(*coords[i]), radius=0.06, color=C.APPROX) for i in range(len(ns))]
        path = VMobject(color=C.APPROX, stroke_width=1.5, stroke_opacity=0.6).set_points_as_corners(
            [mapax.c2p(*c) for c in coords])
        ks = (2, 4, 6)
        sqs = [cam.square(lim, float(err[k])) for k in ks]
        sq_ls = [MathTex(rf"\text{{half-width }} \|B_{{{int(ns[k])}}} - f\| = {err[k]:.3f}", font_size=24, color=C.EPS)
                 .next_to(mapax, UP, buff=0.1) for k in ks]
        concl = label(r"the limit is no polynomial, \ but it is in $C[0, 1]$: \ the space has no holes", font_size=26,
                      color=C.EPS).to_edge(DOWN, buff=0.35)
        for k in ks:
            assert np.all(np.abs(coords[k:] - lim).max(axis=1) <= err[k] + 1e-12)
        with self.voiceover(
            "<bookmark mark='a'/> Now a change of viewpoint. Measure the distance between two continuous functions on a "
            "compact set by their largest gap. Then the continuous functions form a metric space, and each function "
            "is a single point in it. <bookmark mark='b'/> On the right is a camera on that space: each function is "
            "plotted by two of its values, at one half and at 0.4. <bookmark mark='c'/> Here's a sequence of "
            "polynomials closing in on the absolute value of x minus a half: their sup distances shrink, so it's a "
            "Cauchy sequence, and on the camera the dots form a trail. <bookmark mark='d'/> Once a function is within "
            "r of the limit in the sup norm, its dot lies inside a square of half-width r, and every later dot does "
            "too. <bookmark mark='e'/> The limit has a corner, so it's not a polynomial: the polynomials have a hole "
            "here. But it is continuous, and that's the theorem: by the previous result, uniform limits of continuous "
            "functions are continuous, so this space is complete. It's our first Banach space, though the name will "
            "wait for Part 8."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(lax), Create(target))
            self.play(Create(curves[0]), FadeIn(seq_l))
            self.play(Create(gap), FadeIn(gap_l))
            vo.wait_until("b")
            self.play(FadeIn(head[1]), Create(mapax), FadeIn(u_l), FadeIn(v_l), FadeIn(lim_dot), Create(probes))
            vo.wait_until("c")
            self.play(FadeOut(gap), FadeOut(gap_l), FadeIn(dots[0]))
            cur = curves[0]
            for i in range(1, len(ns)):
                self.play(cur.animate.set_stroke(opacity=0.25, width=1.5), TransformFromCopy(dots[i - 1], dots[i]),
                          Create(curves[i]), run_time=0.8)
                cur = curves[i]
            self.play(Create(path))
            vo.wait_until("d")
            self.play(FadeIn(sqs[0]), FadeIn(sq_ls[0]))
            for j in range(1, len(ks)):
                self.play(ReplacementTransform(sqs[j - 1], sqs[j]), FadeTransform(sq_ls[j - 1], sq_ls[j]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def peano(self):
        d = load("peano")
        o = np.array([-3.4, -0.95, 0])
        S = 4.4
        frame = Square(side_length=S, color=GREY_C, stroke_width=2).move_to(o)
        curves = []
        for k in range(1, 5):
            xx, yy = d[f"x{k}"], d[f"y{k}"]
            step = max(1, len(xx) // 6000)
            pts = np.c_[o[0] - S / 2 + S * xx[::step], o[1] - S / 2 + S * yy[::step], np.zeros(len(xx[::step]))]
            m = VMobject(color=C.APPROX, stroke_width=2.0 if k < 3 else 1.2).set_points_as_corners(pts)
            curves.append(m)
        head = VGroup(label(r"A curve that fills a square \ (Rudin, Exercise 7.14; \ I.~J.~Schoenberg, 1938)",
                            font_size=28),
                      MathTex(r"\Phi(t) = \Big(\sum_{n \ge 1} \frac{f(3^{2n-1}t)}{2^n},\ \sum_{n \ge 1} \frac{f(3^{2n}t)}{2^n}\Big)",
                              font_size=32)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        side = VGroup(label(r"M-test with $M_n = 2^{-n}$: \ uniform, \ so $\Phi$ is continuous", font_size=24),
                      label(r"ternary digits of $t$ $\to$ binary digits of $x$ and $y$:", font_size=24),
                      label(r"every point of the square is hit \ (checked exactly)", font_size=24, color=C.EPS)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -1.0, 0])
        for r_ in side:
            if r_.width > 5.6:
                r_.width = 5.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -1.1, 0])
        nlab = [MathTex(rf"{k} \text{{ term{'s' if k > 1 else ''}}}", font_size=28, color=C.APPROX).next_to(frame, DOWN,
                                                                                                     buff=0.15)
                for k in range(1, 5)]
        card = museum_card(r"a space-filling curve", r"Peano 1890; \ this one Schoenberg 1938",
                           r"`a curve is one-dimensional'", r"Rudin, Exercise 7.14", width=4.4)
        card.to_edge(RIGHT, buff=0.4).set_y(1.15)
        with self.voiceover(
            "One more exhibit for the museum, from Rudin's exercises. <bookmark mark='a'/> Build a plane curve whose "
            "coordinates are series of copies of one continuous zigzag function, scaled by powers of three inside and "
            "halved outside. <bookmark mark='b'/> By the M-test both series converge uniformly, so the curve is "
            "continuous. <bookmark mark='c'/> But it passes through every point of the square: the ternary digits of "
            "the parameter become the binary digits of x and y. A continuous image of a segment can fill a square. "
            "Peano found the first such curve in 1890; this one is Schoenberg's."
        ) as vo:
            self.play(FadeIn(head[0]), Create(frame))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(curves[0]), FadeIn(nlab[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            for k in range(1, 4):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), FadeTransform(nlab[k - 1], nlab[k]), run_time=1.3)
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
            self.play(FadeIn(card, scale=0.95))
        self.wait(0.4)
        self.clear_scene()
