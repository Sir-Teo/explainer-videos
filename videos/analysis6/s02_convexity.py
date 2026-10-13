from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import load, plain_axes, polyline


class Convexity(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.jensen()
        self.amgm()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Convex functions and Jensen's inequality",
                            r"What does averaging do to a convex function?", lit=(), part=6)
        with self.voiceover("Chapter one: convex functions, and the one inequality behind all the others."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        d = load("jensen")
        a, b = float(d["a"]), float(d["b"])
        ax = plain_axes([-1.6, 2.0, 0.5], [0, 5.4, 1], 6.0, 4.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.0, -0.6, 0])
        x = np.linspace(-1.6, 1.69, 600)
        graph = polyline(ax, x, np.exp(x), color=C.FUNC, stroke_width=4)
        g_l = MathTex(r"\varphi(x) = e^x", font_size=30, color=C.FUNC).next_to(ax.c2p(1.69, math.exp(1.69)), LEFT,
                                                                           buff=0.2)
        A, B = ax.c2p(a, math.exp(a)), ax.c2p(b, math.exp(b))
        chord = Line(A, B, color=C.EPS, stroke_width=3)
        ends = VGroup(Dot(A, radius=0.06, color=C.EPS), Dot(B, radius=0.06, color=C.EPS))
        tT = ValueTracker(0.2)

        def gap():
            t = tT.get_value()
            xm = (1 - t) * a + t * b
            top = (1 - t) * math.exp(a) + t * math.exp(b)
            bot = math.exp(xm)
            return VGroup(Line(ax.c2p(xm, bot), ax.c2p(xm, top), color=C.PATHOLOGY, stroke_width=5),
                          Dot(ax.c2p(xm, top), radius=0.06, color=C.EPS), Dot(ax.c2p(xm, bot), radius=0.06,
                                                                              color=C.FUNC))

        gp = always_redraw(gap)

        def gap_text():
            t = tT.get_value()
            g = (1 - t) * math.exp(a) + t * math.exp(b) - math.exp((1 - t) * a + t * b)
            return MathTex(rf"t = {t:.2f}: \ \text{{chord}} - \text{{graph}} = {g:.3f} \ge 0", font_size=28,
                           color=C.PATHOLOGY).next_to(ax, DOWN, buff=0.2)

        gt = always_redraw(gap_text)
        for t in np.linspace(0, 1, 101):
            assert (1 - t) * math.exp(a) + t * math.exp(b) >= math.exp((1 - t) * a + t * b) - 1e-12
        defn = VGroup(label(r"\textbf{RCA 3.1} \ $\varphi$ is convex on $(a, b)$ when", font_size=28),
                      MathTex(r"\varphi\big((1 - t)x + ty\big) \le (1 - t)\varphi(x) + t\,\varphi(y)", font_size=32,
                              color=C.EPS),
                      label(r"for all $x, y$ and $0 \le t \le 1$: \ chords lie above the graph", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        # slopes of chords increase (RCA 3.2): s < t < u
        s_, t_, u_ = -1.0, 0.3, 1.4
        P = [np.array([z, math.exp(z)]) for z in (s_, t_, u_)]
        sl = [(P[1][1] - P[0][1]) / (t_ - s_), (P[2][1] - P[0][1]) / (u_ - s_), (P[2][1] - P[1][1]) / (u_ - t_)]
        assert sl[0] <= sl[1] <= sl[2]
        chords = VGroup(Line(ax.c2p(*P[0]), ax.c2p(*P[1]), color=C.CONNECTED_SET, stroke_width=3),
                        Line(ax.c2p(*P[0]), ax.c2p(*P[2]), color=C.APPROX, stroke_width=3),
                        Line(ax.c2p(*P[1]), ax.c2p(*P[2]), color=C.CLOSED_SET, stroke_width=3))
        pdots = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=WHITE) for p in P])
        slopes = VGroup(
            label(r"\textbf{RCA 3.2} \ slopes of chords increase:", font_size=24),
            MathTex(rf"{sl[0]:.3f}", r"\ \le\ ", rf"{sl[1]:.3f}", r"\ \le\ ", rf"{sl[2]:.3f}", font_size=32),
            label(r"so a convex $\varphi$ is continuous on an open interval:", font_size=22, color=GREY_A),
            label(r"its graph is pinned between two chords at every point", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.95, -1.1, 0])
        for i, c in zip((0, 2, 4), (C.CONNECTED_SET, C.APPROX, C.CLOSED_SET)):
            slopes[1][i].set_color(c)
        with self.voiceover(
            "<bookmark mark='a'/> A function is convex if every chord lies above its graph: at each point between x "
            "and y, the straight line is at least as high as the function. <bookmark mark='b'/> Here's the "
            "exponential. Slide along the chord, and the red gap between chord and graph never goes negative. "
            "<bookmark mark='c'/> An equivalent form: take three points. The slopes of the three chords increase, "
            "from left to right. <bookmark mark='d'/> So at every point the graph is pinned between two chords, and "
            "a convex function on an open interval is automatically continuous."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(defn), Create(ax), Create(graph), FadeIn(g_l))
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(ends))
            self.play(FadeIn(gp), FadeIn(gt))
            self.play(tT.animate.set_value(0.85), run_time=3.0)
            self.play(tT.animate.set_value(0.5), run_time=1.5)
            vo.wait_until("c")
            for m in (gp, gt):
                m.clear_updaters()
            self.play(FadeOut(gp), FadeOut(gt), FadeOut(chord), FadeOut(ends))
            self.play(FadeIn(pdots), Create(chords), FadeIn(slopes[:2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(slopes[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jensen(self):
        d = load("jensen")
        worst = float(d["worst"])
        ax = plain_axes([-1.4, 1.8, 0.5], [0, 6.2, 1], 6.0, 4.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.0, -0.75, 0])
        x = np.linspace(-1.4, 1.8, 600)
        graph = polyline(ax, x, np.exp(x), color=C.FUNC, stroke_width=4)
        xs = np.array([-1.1, -0.4, 0.3, 1.0, 1.65])
        W = np.array([[0.2, 0.2, 0.2, 0.2, 0.2], [0.55, 0.25, 0.1, 0.05, 0.05], [0.05, 0.05, 0.1, 0.2, 0.6],
                      [0.4, 0.02, 0.02, 0.02, 0.54], [0.1, 0.3, 0.45, 0.1, 0.05]])
        wT = ValueTracker(0.0)

        def weights():
            s = wT.get_value()
            i = min(int(s), len(W) - 2)
            f = s - i
            return (1 - f) * W[i] + f * W[i + 1]

        hull = Polygon(*[ax.c2p(z, math.exp(z)) for z in xs], stroke_color=GREY_C, stroke_width=1.5,
                       fill_color=GREY_C, fill_opacity=0.12)

        def scene_pts():
            w = weights()
            g = VGroup()
            for z, wi in zip(xs, w):
                g.add(Dot(ax.c2p(z, math.exp(z)), radius=0.04 + 0.22 * math.sqrt(wi), color=C.MEASURE,
                          fill_opacity=0.85))
                g.add(Line(ax.c2p(z, 0), ax.c2p(z, 0.0) + UP * (1.6 * wi), color=C.MEASURE, stroke_width=8))
            mx, my = float(w @ xs), float(w @ np.exp(xs))
            g.add(Line(ax.c2p(mx, math.exp(mx)), ax.c2p(mx, my), color=C.PATHOLOGY, stroke_width=4))
            g.add(Dot(ax.c2p(mx, my), radius=0.08, color=C.EPS))
            g.add(Dot(ax.c2p(mx, math.exp(mx)), radius=0.07, color=C.DELTA))
            return g

        pts = always_redraw(scene_pts)

        # the readout: fixed labels with DecimalNumbers (re-typesetting whole formulas every frame is slow and
        # fills memory)
        def lr():
            w = weights()
            return math.exp(float(w @ xs)), float(w @ np.exp(xs))

        n_l = DecimalNumber(lr()[0], num_decimal_places=3, font_size=30, color=C.DELTA)
        n_r = DecimalNumber(lr()[1], num_decimal_places=3, font_size=30, color=C.EPS)
        n_w = [DecimalNumber(v, num_decimal_places=2, font_size=24, color=C.MEASURE) for v in weights()]
        wrow = VGroup(MathTex(r"w = (", font_size=24, color=C.MEASURE))
        for i, d_ in enumerate(n_w):
            wrow.add(d_)
            wrow.add(MathTex(r"," if i < len(n_w) - 1 else r")", font_size=24, color=C.MEASURE))
        wrow.arrange(RIGHT, buff=0.05)
        for k_ in range(2, len(wrow) - 1, 2):  # commas hang just below the digits' baseline
            wrow[k_].align_to(wrow[1], DOWN).shift(DOWN * 0.05)
        wrow[-1].set_y(wrow[0].get_y())  # the closing bracket matches the opening one
        ro = VGroup(
            VGroup(MathTex(r"\varphi\Big(\sum w_i x_i\Big) =", font_size=30, color=C.DELTA), n_l).arrange(RIGHT, buff=0.15),
            VGroup(MathTex(r"\sum w_i\, \varphi(x_i) =", font_size=30, color=C.EPS), n_r).arrange(RIGHT, buff=0.15),
            wrow,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, 1.05, 0])
        n_l.add_updater(lambda m: m.set_value(lr()[0]))
        n_r.add_updater(lambda m: m.set_value(lr()[1]))
        for i, d_ in enumerate(n_w):
            d_.add_updater(lambda m, i=i: m.set_value(weights()[i]))
        for row in W:
            assert math.exp(row @ xs) <= row @ np.exp(xs)
        thm = VGroup(
            label(r"\textbf{RCA 3.3} \ (Jensen, 1906) \ $\mu(\Omega) = 1$, \ $f \in L^1(\mu)$, \ $\varphi$ convex:",
                  font_size=24),
            MathTex(r"\varphi\Big(\int_\Omega f\,d\mu\Big) \le \int_\Omega \varphi \circ f\,d\mu", font_size=36,
                    color=C.EPS),
            label(r"proof: \ a line under $\varphi$ touching at $\int f$, \ integrated", font_size=22, color=GREY_A),
            MathTex(rf"10^4 \text{{ random weightings: smallest gap }} {sci(worst, 1)} \ge 0", font_size=24,
                    color=GREY_A),
        )
        for r_ in thm:
            if r_.width > 6.3:
                r_.width = 6.3
        thm.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to([0.55, -1.55, 0], RIGHT, buff=0)
        head = label(r"Weights on a convex curve: \ the center of mass lies above the curve", font_size=32).to_edge(
            UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Now put weights on several points of the curve, orange, adding up to one. Their "
            "center of mass is the yellow dot. <bookmark mark='b'/> It sits inside the shaded hull of the points, "
            "and so above the curve: the function of the average is at most the average of the function. "
            "<bookmark mark='c'/> Shift the weights around and the inequality holds every time. "
            "<bookmark mark='d'/> That's Jensen's inequality, and with a probability measure it reads: phi of the "
            "integral of f is at most the integral of phi of f. The proof is one picture: a straight line below phi, "
            "touching it at the average, integrated."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(graph))
            vo.wait_until("a")
            self.play(FadeIn(hull), FadeIn(pts))
            vo.wait_until("b")
            self.play(FadeIn(ro))
            vo.wait_until("c")
            for k in range(1, len(W)):
                self.play(wT.animate.set_value(float(k)), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(thm[:2]))
            self.play(FadeIn(thm[2:]))
        for m in (pts, n_l, n_r, *n_w):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def amgm(self):
        a = np.array([1.0, 8.0, 27.0])
        L = np.log(a)
        ax = plain_axes([0, 3.5, 0.5], [0, 29, 4], 5.6, 4.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.6, 0])
        x = np.linspace(0, 3.36, 400)
        graph = polyline(ax, x, np.exp(x), color=C.FUNC, stroke_width=4)
        pts = VGroup(*[Dot(ax.c2p(z, v), radius=0.08, color=C.MEASURE) for z, v in zip(L, a)])
        plabels = VGroup(*[MathTex(rf"(\log {int(v)},\ {int(v)})", font_size=22, color=C.MEASURE).next_to(
            ax.c2p(z, v), (UR, RIGHT, LEFT)[i], buff=0.15) for i, (z, v) in enumerate(zip(L, a))])  # (log 1, 1) above the axis
        tri = Polygon(*[ax.c2p(z, v) for z, v in zip(L, a)], stroke_color=GREY_C, stroke_width=1.5,
                      fill_color=GREY_C, fill_opacity=0.12)
        mx, am = float(L.mean()), float(a.mean())
        gm = math.exp(mx)
        assert abs(gm - 6.0) < 1e-12 and abs(am - 12.0) < 1e-12
        top, bot = Dot(ax.c2p(mx, am), radius=0.09, color=C.EPS), Dot(ax.c2p(mx, gm), radius=0.08, color=C.DELTA)
        gap = Line(ax.c2p(mx, gm), ax.c2p(mx, am), color=C.PATHOLOGY, stroke_width=5)
        tl = MathTex(r"\tfrac{1 + 8 + 27}{3} = 12", font_size=28, color=C.EPS).next_to(top, LEFT, buff=0.2)
        bl = MathTex(r"(1 \cdot 8 \cdot 27)^{1/3} = 6", font_size=28, color=C.DELTA).next_to(bot, RIGHT, buff=0.2).shift(
            DOWN * 0.25)
        side = VGroup(
            label(r"$\varphi = \exp$, \ $x_i = \log a_i$, \ equal weights:", font_size=26),
            MathTex(r"(a_1 a_2 \cdots a_n)^{1/n} \le \frac{a_1 + a_2 + \cdots + a_n}{n}", font_size=32, color=C.EPS),
            label(r"geometric mean $\le$ arithmetic mean", font_size=24, color=GREY_A),
            label(r"with weights $\frac1p$ and $\frac1q$, \ $\frac1p + \frac1q = 1$:", font_size=26),
            MathTex(r"e^{\frac sp + \frac tq} \le \frac{e^s}{p} + \frac{e^t}{q}", font_size=32, color=C.EPS),
            label(r"next chapter: \ this one line is H\"older's inequality", font_size=24, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([3.4, -0.55, 0])
        side[3:].shift(DOWN * 0.2)
        rng = np.random.default_rng(11)
        v = rng.uniform(0.05, 20, (10000, 5))
        assert np.all(np.prod(v, axis=1) ** (1 / 5) <= v.mean(axis=1) + 1e-12)
        head = label(r"A corollary: \ the AM--GM inequality", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> One corollary you know. Put the points log one, log eight and log twenty-seven on the "
            "exponential curve, with equal weights. <bookmark mark='b'/> The center of mass is at height twelve, the "
            "average of one, eight and twenty-seven. The curve below it is at height six, the cube root of their "
            "product. <bookmark mark='c'/> The geometric mean is at most the arithmetic mean, for any positive "
            "numbers. <bookmark mark='d'/> With unequal weights, one over p and one over q, the same line says: e to "
            "the s over p plus t over q is at most e to the s over p, plus e to the t over q. That single line is "
            "the engine of the next chapter."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(graph))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(plabels), FadeIn(tri))
            vo.wait_until("b")
            self.play(FadeIn(top), FadeIn(tl))
            self.play(Create(gap), FadeIn(bot), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(side[:3]))
            vo.wait_until("d")
            self.play(FadeIn(side[3:5]))
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()
