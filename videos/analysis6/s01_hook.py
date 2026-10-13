from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import between, load, p_ball, plain_axes, pnorm, polyline, square_axes, trap
from videos.analysis6.compute import ramp


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.balls()
        self.incomplete()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=5, highlight=6).scale(0.9)
        with self.voiceover(
            "Five rows of the ledger are filled. Part 5 built Lebesgue's integral. <bookmark mark='l'/> Part 6 uses "
            "it to measure distances between functions, and finds that one of those distances has the geometry of "
            "the plane: lengths, angles, and right triangles."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[5], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def balls(self):
        ax = square_axes([-1.3, 1.3, 1], [-1.3, 1.3, 1], 1.85).move_to([-4.3, -0.55, 0])
        pT = ValueTracker(1.0)

        def p_now():
            p = pT.get_value()
            return np.inf if p > 39 else p

        ball = always_redraw(lambda: p_ball(ax, p_now(), C.DIST))
        v = np.array([0.6, 0.8])
        arrow = Arrow(ax.c2p(0, 0), ax.c2p(*v), buff=0, color=WHITE, stroke_width=4, tip_length=0.18)
        v_l = MathTex(r"v = (0.6,\ 0.8)", font_size=26).next_to(ax.c2p(*v), UR, buff=0.05)

        def p_text():
            p = p_now()
            ps = r"\infty" if np.isinf(p) else f"{p:.1f}"
            return MathTex(rf"\{{|x|^p + |y|^p \le 1\}}, \ p = {ps}", font_size=28, color=C.DIST).next_to(ax, DOWN,
                                                                                                    buff=0.15)

        pl = always_redraw(p_text)
        vn = VGroup(*[MathTex(rf"\|v\|_{{{s}}} = {pnorm(v, p):.2f}".replace(".00", ""), font_size=26, color=C.DIST)
                      for s, p in (("1", 1), ("2", 2), (r"\infty", np.inf))]).arrange(RIGHT, buff=0.35)
        vn.next_to(pl, DOWN, buff=0.15)
        assert abs(pnorm(v, 1) - 1.4) < 1e-12 and abs(pnorm(v, 2) - 1) < 1e-12 and abs(pnorm(v, np.inf) - 0.8) < 1e-12

        fx = plain_axes([0, 1, 0.25], [0, 4.4, 1], 3.3, 3.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0.75, 0.15, 0])
        spike = VGroup(Line(fx.c2p(0, 4), fx.c2p(0.25, 4), color=C.APPROX, stroke_width=4),
                       Line(fx.c2p(0.25, 4), fx.c2p(0.25, 0), color=C.APPROX, stroke_width=2),
                       Line(fx.c2p(0.25, 0), fx.c2p(1, 0), color=C.APPROX, stroke_width=4))
        spike_a = Rectangle(width=fx.c2p(0.25, 0)[0] - fx.c2p(0, 0)[0], height=fx.c2p(0, 4)[1] - fx.c2p(0, 0)[1],
                            stroke_width=0, fill_color=C.APPROX, fill_opacity=0.25).move_to(fx.c2p(0.125, 2))
        flat = Line(fx.c2p(0, 1), fx.c2p(1, 1), color=C.SEQ, stroke_width=4)
        flat_a = Rectangle(width=fx.c2p(1, 0)[0] - fx.c2p(0, 0)[0], height=fx.c2p(0, 1)[1] - fx.c2p(0, 0)[1],
                           stroke_width=0, fill_color=C.SEQ, fill_opacity=0.2).move_to(fx.c2p(0.5, 0.5))
        sl = MathTex(r"f = 4 \cdot \mathbf 1_{[0, 1/4]}", font_size=26, color=C.APPROX).next_to(fx.c2p(0.25, 4), RIGHT,
                                                                                              buff=0.15)
        gl = MathTex(r"g = 1", font_size=26, color=C.SEQ).next_to(fx.c2p(1, 1), UP, buff=0.12).shift(LEFT * 0.3)
        # the three norms, exactly: area, energy, height
        x = np.linspace(0, 1, 400001)
        f, g = 4.0 * (x <= 0.25), np.ones_like(x)
        vals = {}
        for name, h in (("f", f), ("g", g)):
            l1 = float(np.mean(np.abs(h)))
            l2 = float(np.sqrt(np.mean(h**2)))
            vals[name] = (l1, l2, float(h.max()))
        assert np.allclose(vals["f"], (1, 2, 4), atol=1e-4) and np.allclose(vals["g"], (1, 1, 1))
        cols = (4.1, 5.35, 6.35)
        hdr = VGroup(MathTex(r"\text{norm}", font_size=24, color=GREY_A).move_to([cols[0], 1.3, 0]),
                     MathTex(r"f", font_size=28, color=C.APPROX).move_to([cols[1], 1.3, 0]),
                     MathTex(r"g", font_size=28, color=C.SEQ).move_to([cols[2], 1.3, 0]))
        names = (r"\int |h| \ \ (\text{area})", r"\big(\!\int |h|^2\big)^{1/2}", r"\sup |h| \ \ (\text{height})")
        tab = VGroup()
        for i, (nm, a, b) in enumerate(zip(names, (1, 2, 4), (1, 1, 1))):
            y = 0.55 - 0.72 * i
            row = VGroup(MathTex(nm, font_size=24).move_to([cols[0], y, 0]),
                         MathTex(str(a), font_size=30, color=C.APPROX).move_to([cols[1], y, 0]),
                         MathTex(str(b), font_size=30, color=C.SEQ).move_to([cols[2], y, 0]))
            tab.add(row)
        rule = Line([3.0, 0.95, 0], [6.8, 0.95, 0], color=GREY_C, stroke_width=1.5)
        out = VGroup(label(r"same area, \ twice the energy, \ four times the height:", font_size=26, color=C.EPS),
                     label(r"which distance is right?", font_size=26, color=C.EPS)).arrange(DOWN, buff=0.1).move_to(
            [3.7, -2.75, 0])
        head = label(r"How long is a vector? \ How big is a function?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> How long is a vector? In the plane we have a choice. Add the sizes of the "
            "coordinates, or take the square root of the sum of squares, or just the largest coordinate. "
            "<bookmark mark='b'/> The vectors of length one form a diamond, then a circle, then a square, and in "
            "between the p-norms, for every p from one to infinity. <bookmark mark='c'/> The same vector has three "
            "different lengths. <bookmark mark='d'/> Functions have the same choice. A tall spike and a flat line "
            "have the same area, but the spike has twice the energy and four times the height. "
            "<bookmark mark='e'/> So which distance between functions is the right one? Each answers a different "
            "question, and this part is about all of them, and about one that's special."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(FadeIn(ball), FadeIn(pl))
            vo.wait_until("b")
            self.play(pT.animate.set_value(2.0), run_time=2.5)
            self.play(pT.animate.set_value(6.0), run_time=1.5)
            self.play(pT.animate.set_value(40.0), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(v_l))
            self.play(LaggedStart(*[FadeIn(m) for m in vn], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(Create(fx))
            self.play(FadeIn(spike_a), Create(spike), FadeIn(sl), FadeIn(flat_a), Create(flat), FadeIn(gl))
            self.play(FadeIn(hdr), Create(rule))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in tab], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(out))
        for m in (ball, pl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def incomplete(self):
        d = load("ramps")
        ns, d1, left, right = d["ns"], d["d1"], d["left"], d["right"]
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 5.6, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.35, 0])
        x = np.linspace(0, 1, 2001)
        step = (x > 0.5).astype(float)
        step_g = VGroup(Line(ax.c2p(0, 0), ax.c2p(0.5, 0), color=WHITE, stroke_width=3),
                        Line(ax.c2p(0.5, 1), ax.c2p(1, 1), color=WHITE, stroke_width=3),
                        Dot(ax.c2p(0.5, 0), radius=0.05, color=WHITE),
                        Circle(radius=0.05, color=WHITE, stroke_width=2).move_to(ax.c2p(0.5, 1)))
        step_l = MathTex(r"\mathbf 1_{(1/2, 1]}", font_size=28).next_to(ax.c2p(1, 1), UP, buff=0.1)
        curves = [polyline(ax, x, ramp(x, n), color=C.SEQ, stroke_width=3.5) for n in ns]
        areas = [between(ax, x, ramp(x, n), step, C.MEASURE, 0.45) for n in ns]
        reads = [MathTex(rf"n = {n}: \ \ \|r_n - \mathbf 1\|_1 = \tfrac{{1}}{{4n}} = {v:.4f}", font_size=28,
                         color=C.MEASURE).next_to(ax, DOWN, buff=0.2) for n, v in zip(ns, d1)]
        rl = MathTex(r"r_n(x) = \text{clip}\big(n(x - \tfrac12) + \tfrac12,\ 0,\ 1\big)", font_size=26,
                     color=C.SEQ).next_to(ax, UP, buff=0.15)
        mapax = plain_axes([0, 0.14, 0.05], [0.36, 0.52, 0.05], 3.0, 3.0).move_to([3.6, 0.15, 0])
        u_l = MathTex(r"\int_0^{1/2} f", font_size=24, color=GREY_B).next_to(mapax, DOWN, buff=0.12)
        v_l = MathTex(r"\int_{1/2}^1 f", font_size=24, color=GREY_B).next_to(mapax, LEFT, buff=0.12)
        cam_h = label(r"the camera: \ each function is one point", font_size=24, color=GREY_A).next_to(mapax, UP,
                                                                                                    buff=0.15)
        dots = [Dot(mapax.c2p(a, b), radius=0.06, color=C.SEQ) for a, b in zip(left, right)]
        path = VMobject(color=C.SEQ, stroke_width=1.5, stroke_opacity=0.6).set_points_as_corners(
            [mapax.c2p(a, b) for a, b in zip(left, right)] + [mapax.c2p(0, 0.5)])
        target = VGroup(Line(mapax.c2p(0, 0.5) + UL * 0.09, mapax.c2p(0, 0.5) + DR * 0.09, color=C.PATHOLOGY,
                             stroke_width=4),
                        Line(mapax.c2p(0, 0.5) + DL * 0.09, mapax.c2p(0, 0.5) + UR * 0.09, color=C.PATHOLOGY,
                             stroke_width=4))
        t_l = label(r"only the step \ could be the limit", font_size=22, color=C.PATHOLOGY).next_to(
            mapax.c2p(0, 0.5), RIGHT, buff=0.2).shift(UP * 0.15)
        assert np.allclose(left, 1 / (8 * ns), rtol=1e-3) and np.allclose(right, 0.5 - 1 / (8 * ns), rtol=1e-3)
        side = VGroup(
            MathTex(r"\|r_n - r_m\|_1 = \tfrac{1}{4n} - \tfrac{1}{4m} \to 0 \quad (n < m)", font_size=28),
            label(r"Cauchy in $C[0, 1]$ with $\int |f - g|$, \ but no continuous limit:", font_size=24),
            label(r"a limit $g$ would have $\int |g - \mathbf 1_{(1/2, 1]}| = 0$, \ so $g = 0$ then $1$", font_size=24,
                  color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -2.75, 0])
        for r_ in side:
            if r_.width > 6.6:
                r_.width = 6.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -2.75, 0])
        # Cauchy, exactly: the ramps are nested on each side of 1/2
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                dij = trap(np.abs(ramp(x, ns[i]) - ramp(x, ns[j])), x)
                assert abs(dij - (1 / (4 * ns[i]) - 1 / (4 * ns[j]))) < 1e-5
        head = VGroup(label(r"The scandal: \ $C[0, 1]$ with the distance $\int_0^1 |f - g|$ has a hole", font_size=32),
                      label(r"its completion is $L^1[0, 1]$, \ Lebesgue's integrable functions \ (chapter 4)",
                            font_size=24, color=C.EPS)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the problem that forces Lebesgue's integral on us. Measure the distance "
            "between two continuous functions by the area between their graphs. <bookmark mark='b'/> Steeper and "
            "steeper ramps: the area between a ramp and the step is one over four n. <bookmark mark='c'/> The ramps "
            "get closer to each other too, so they form a Cauchy sequence. On the camera, each function is one point, "
            "plotted by its integrals over the two halves, and the points close in. <bookmark mark='d'/> But on what? "
            "A limit would have to be at area distance zero from the step: zero on the left half, one on the right. "
            "No continuous function does that. <bookmark mark='e'/> The continuous functions, under this distance, "
            "have a hole. Filling it takes exactly the functions Lebesgue's integral can handle, and that's the "
            "space L one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(ax), Create(step_g), FadeIn(step_l))
            vo.wait_until("b")
            self.play(FadeIn(rl), Create(curves[0]), FadeIn(areas[0]), FadeIn(reads[0]))
            for k in range(1, 3):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), ReplacementTransform(areas[k - 1], areas[k]),
                          FadeTransform(reads[k - 1], reads[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(Create(mapax), FadeIn(u_l), FadeIn(v_l), FadeIn(cam_h), FadeIn(dots[0]), FadeIn(dots[1]),
                      FadeIn(dots[2]))
            for k in range(3, len(ns)):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), ReplacementTransform(areas[k - 1], areas[k]),
                          FadeTransform(reads[k - 1], reads[k]), TransformFromCopy(dots[k - 1], dots[k]), run_time=0.8)
            self.play(Create(path), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(Create(target), FadeIn(t_l), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(head[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Convex functions and Jensen", r"Young, H\"older, Minkowski", r"The spaces $L^p$",
            r"$L^p$ is complete \ (Riesz--Fischer)", r"Inner products; \ the parallelogram law", r"The nearest point",
            r"Every functional is an inner product", r"Orthonormal bases, \ Bessel, Parseval",
            r"Fourier series in $L^2$, \ and Fej\'er", r"Complex measures", r"The Radon--Nikodym theorem",
            r"The dual of $L^p$", r"Differentiating measures", r"The fundamental theorem, for Lebesgue",
            r"Change of variables",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=26) for i, t in enumerate(chapters)])
        colL = VGroup(*items[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        colR = VGroup(*items[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        colL.move_to([-3.2, -0.55, 0])
        colR.move_to([3.3, -0.55, 0]).align_to(colL, UP)
        head = label(r"Part 6: \ $L^p$, Hilbert space and the geometry of functions", font_size=40).to_edge(UP, buff=0.4)
        sub = label(r"Rudin, \textit{Real and Complex Analysis}, chapters 3, 4, 6 and 7", font_size=26,
                    color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters three, four, six and seven of Rudin's Real and Complex Analysis. "
            "<bookmark mark='a'/> First the inequalities that make the p-norms into distances, and the theorem that "
            "the spaces are complete. <bookmark mark='b'/> Then the case p equals two, a Hilbert space, where we can "
            "project, find bases, and finally answer the Fourier question. <bookmark mark='c'/> Then measures that "
            "take signs and complex values, densities, dual spaces, and the fundamental theorem of calculus, "
            "rebuilt for Lebesgue's integral."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(4, 9)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(9, 15)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
