from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, plain_axes, polyline


class MeanValue(VoiceoverScene):
    def construct(self):
        self.card()
        self.extremum()
        self.shear()
        self.monotone()
        self.darboux()
        self.lhopital()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(13, r"Mean value theorems", r"If you averaged 60 miles an hour, were you ever doing exactly "
                            r"60?", lit=(), part=2)
        with self.voiceover(
            "Chapter thirteen. If a trip averaged sixty miles an hour, at some instant the speedometer read exactly "
            "sixty. That's the mean value theorem, and its proof runs on compactness."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def extremum(self):
        ax = plain_axes([0, 4, 1], [-1, 3, 1], 6.4, 4.4, numbers=False).move_to([-3.0, -0.8, 0])
        f = lambda x: 1.2 + 1.3 * np.sin(1.2 * x) - 0.15 * x  # noqa: E731
        g = ax.plot(f, x_range=[0, 4, 0.01], color=C.FUNC, stroke_width=4)
        xm = brentq(lambda x: 1.56 * np.cos(1.2 * x) - 0.15, 0.5, 2.0)
        top = Dot(ax.c2p(xm, f(xm)), radius=0.08, color=C.EPS)
        tan = Line(ax.c2p(xm - 1.0, f(xm)), ax.c2p(xm + 1.0, f(xm)), color=C.EPS, stroke_width=3)
        thm = VGroup(label(r"\textbf{Rudin 5.8} \ At a local maximum, \ $f'(x) = 0$:", font_size=30),
                     label(r"from the left, \ $\dfrac{f(t) - f(x)}{t - x} \ge 0$;", font_size=28),
                     label(r"from the right, \ $\dfrac{f(t) - f(x)}{t - x} \le 0$.", font_size=28),
                     label(r"The limit is both: \ $0$.", font_size=28, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.2)
        thm.move_to([3.5, 0.2, 0])
        with self.voiceover(
            "First, a lemma. <bookmark mark='a'/> At a local maximum the derivative is zero. <bookmark mark='b'/> "
            "Approaching from the left, f of t is at most f of x and t minus x is negative, so the difference quotients "
            "are at least zero; <bookmark mark='c'/> from the right they're at most zero. <bookmark mark='d'/> The "
            "limit has to be both."
        ) as vo:
            self.play(Create(ax), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(thm[0]), FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(thm[1]))
            vo.wait_until("c")
            self.play(FadeIn(thm[2]))
            vo.wait_until("d")
            self.play(FadeIn(thm[3]), Create(tan))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shear(self):
        ax = plain_axes([0, 4.2, 1], [-1.5, 3.5, 1], 8.0, 5.0, numbers=False).move_to([-1.9, -0.75, 0])
        f = lambda x: 0.4 + 0.55 * x + 0.8 * np.sin(1.7 * x) + 0.15 * np.cos(4 * x)  # noqa: E731
        fp = lambda x: 0.55 + 1.36 * np.cos(1.7 * x) - 0.6 * np.sin(4 * x)  # noqa: E731
        a, b = 0.3, 3.9
        m = (f(b) - f(a)) / (b - a)
        L = lambda x: f(a) + m * (x - a)  # noqa: E731
        sT = ValueTracker(0.0)  # 0: the graph of f; 1: the sheared graph f - (chord - f(a))

        def curve():
            s = sT.get_value()
            x = np.linspace(a, b, 500)
            y = f(x) - s * (L(x) - f(a))
            return polyline(ax, x, y, color=C.FUNC, stroke_width=4)

        def chord():
            s = sT.get_value()
            return Line(ax.c2p(a, f(a)), ax.c2p(b, f(b) - s * (f(b) - f(a))), color=C.APPROX, stroke_width=3)

        cv, ch = always_redraw(curve), always_redraw(chord)
        ends = always_redraw(lambda: VGroup(Dot(ax.c2p(a, f(a)), radius=0.07, color=C.APPROX),
                                            Dot(ax.c2p(b, f(b) - sT.get_value() * (f(b) - f(a))), radius=0.07,
                                                color=C.APPROX)))
        xs = np.linspace(a, b, 40001)
        h = f(xs) - (L(xs) - f(a))
        i_max = int(np.argmax(h))
        xi = brentq(lambda x: fp(x) - m, xs[max(i_max - 400, 0)], xs[min(i_max + 400, len(xs) - 1)])

        def tangent():
            s = sT.get_value()
            yv = f(xi) - s * (L(xi) - f(a))
            slope = m * (1 - s)
            return Line(ax.c2p(xi - 1.1, yv - 1.1 * slope), ax.c2p(xi + 1.1, yv + 1.1 * slope), color=C.EPS,
                        stroke_width=3.5)

        tg = always_redraw(tangent)
        xi_dot = always_redraw(lambda: Dot(ax.c2p(xi, f(xi) - sT.get_value() * (L(xi) - f(a))), radius=0.08,
                                           color=C.EPS))
        thm = VGroup(label(r"\textbf{Rudin 5.10} \ (mean value theorem)", font_size=28),
                     MathTex(r"f(b) - f(a) = (b - a)\, f'(\xi)", font_size=32),
                     label(r"for some $\xi \in (a, b)$", font_size=26)).arrange(DOWN, buff=0.12).move_to([4.6, 2.4, 0])
        steps = VGroup(
            label(r"1. \ shear vertically: \ subtract the chord", font_size=24),
            label(r"2. \ now the ends are level; \ a continuous", font_size=24),
            label(r"\phantom{2. \ }function on $[a, b]$ has a max (4.16)", font_size=24),
            label(r"3. \ there the slope is $0$ \ (5.8)", font_size=24),
            label(r"4. \ shear back: \ slope $0$ becomes", font_size=24),
            label(r"\phantom{4. \ }the chord's slope", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -0.3, 0])
        gen = label(r"Rudin 5.9, the general form: \ $[f(b) - f(a)]\, g'(\xi) = [g(b) - g(a)]\, f'(\xi)$", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: the chord from a to b has the same slope as the tangent at some point "
            "in between. <bookmark mark='b'/> Here's a proof you can watch. Subtract the chord from the function: a "
            "vertical shear, not a rotation, so vertical lines stay vertical. <bookmark mark='c'/> Now the two ends "
            "are level. The sheared function is continuous on a compact interval, so it has a maximum, and since the "
            "ends are level, we can take it in the interior. <bookmark mark='d'/> There, the slope is zero. "
            "<bookmark mark='e'/> Shear back: slopes all increase by the chord's slope, so the horizontal tangent "
            "becomes a tangent parallel to the chord. <bookmark mark='f'/> Rudin proves a version with two functions, "
            "which we'll need for L'Hôpital's rule."
        ) as vo:
            self.play(Create(ax), FadeIn(cv), FadeIn(ch), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            self.play(sT.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(xi_dot), Create(tg), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]), FadeIn(steps[5]))
            self.play(sT.animate.set_value(0.0), run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(gen))
        assert a < xi < b and abs(fp(xi) - m) < 1e-9
        for mob in (cv, ch, ends, tg, xi_dot):
            mob.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def monotone(self):
        rows = VGroup(
            label(r"\textbf{Rudin 5.11} \ On $(a, b)$:", font_size=32),
            label(r"$f' \ge 0$ $\Rightarrow$ $f$ increasing; \quad $f' = 0$ $\Rightarrow$ $f$ constant; \quad "
                  r"$f' \le 0$ $\Rightarrow$ $f$ decreasing", font_size=30),
            MathTex(r"f(x_2) - f(x_1) = (x_2 - x_1)\, f'(\xi)", font_size=36),
            label(r"the mean value theorem turns information about $f'$ into information about $f$", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem's main job is to turn facts about the derivative into facts about the "
            "function. If the derivative is never negative, then for any two points the difference f of x two minus f "
            "of x one is x two minus x one times some derivative, so it's never negative: f increases. A zero "
            "derivative means a constant function."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def darboux(self):
        thm = VGroup(label(r"\textbf{Rudin 5.12} \ (Darboux) \ Derivatives have the intermediate value property:",
                           font_size=28),
                     label(r"$f'(a) < \lambda < f'(b)$ $\Rightarrow$ $f'(x) = \lambda$ for some $x \in (a, b)$, \ "
                           r"even if $f'$ is not continuous", font_size=26)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        pf = label(r"proof: \ $g(t) = f(t) - \lambda t$ has $g'(a) < 0 < g'(b)$, \ so its minimum on $[a, b]$ is "
                   r"interior, \ where $g' = 0$", font_size=24, color=GREY_A).next_to(thm, DOWN, buff=0.2)
        ax = plain_axes([0, 0.1, 0.05], [-1.4, 1.4, 1], 10.0, 3.6, numbers=False).move_to([0, -1.5, 0])
        u = np.linspace(10, 600, 60000)
        x = 1 / u
        y = 2 * x * np.sin(1 / x) - np.cos(1 / x)
        g = polyline(ax, x, y, color=C.PATHOLOGY, stroke_width=1.5)
        lab = MathTex(r"f'(x) = 2x\sin\tfrac1x - \cos\tfrac1x \text{ on } (0, 0.1)", font_size=28,
                      color=C.PATHOLOGY).next_to(ax, UP, buff=0.12).align_to(ax, RIGHT)
        lev = ValueTracker(0.7)
        lline = always_redraw(lambda: DashedLine(ax.c2p(0, lev.get_value()), ax.c2p(0.1, lev.get_value()), color=C.EPS,
                                                 stroke_width=2))
        lt = always_redraw(lambda: MathTex(r"\lambda", font_size=30, color=C.EPS).next_to(ax.c2p(0, lev.get_value()),
                                                                                          LEFT, buff=0.12))
        cor = label(r"so a derivative cannot jump: \ its discontinuities are all of the second kind", font_size=26,
                    color=C.EPS).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='t'/> Darboux noticed something surprising: a derivative always has the intermediate value "
            "property, continuous or not. <bookmark mark='p'/> To hit a value lambda, subtract lambda t from f: the "
            "result slopes down at a and up at b, so its minimum is inside, where its derivative is zero. "
            "<bookmark mark='a'/> Remember the museum piece: its derivative is discontinuous at zero, <bookmark mark='b'/> "
            "yet on every interval next to zero it takes every value between about minus one and one, again and again. "
            "<bookmark mark='c'/> So a derivative can never have a simple jump: if it's discontinuous, it's wildly so."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("p")
            self.play(FadeIn(pf))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(lab), Create(g), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(lline), FadeIn(lt))
            self.play(lev.animate.set_value(-0.8), run_time=2.0)
            self.play(lev.animate.set_value(0.2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(cor))
        load("wiggle")  # asserts f' - c changes sign on (0, 0.02) for every c in [-0.9, 0.9]
        for m in (lline, lt):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def lhopital(self):
        thm = VGroup(label(r"\textbf{L'H\^opital's rule} (Rudin 5.13)", font_size=30),
                     label(r"$f, g \to 0$ as $x \to a$, \ $g' \ne 0$, \ $\dfrac{f'}{g'} \to A$ \ $\Rightarrow$ \ "
                           r"$\dfrac{f}{g} \to A$", font_size=28)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        o = np.array([-3.8, -2.6, 0])
        sc = 2.6

        def P(gx, fx):
            return o + sc * np.array([gx, fx, 0])

        tt = np.linspace(0.0, 1.6, 400)
        G, F = np.sin(tt), 1 - np.cos(tt)  # the curve t -> (g(t), f(t)) leaves the origin
        axes = VGroup(Arrow(P(0, 0), P(1.15, 0), buff=0, color=GREY_C, stroke_width=2, tip_length=0.12),
                      Arrow(P(0, 0), P(0, 1.15), buff=0, color=GREY_C, stroke_width=2, tip_length=0.12))
        al = VGroup(MathTex(r"g", font_size=28).next_to(P(1.15, 0), RIGHT, buff=0.1),
                    MathTex(r"f", font_size=28).next_to(P(0, 1.15), UP, buff=0.1))
        curve = VMobject(color=C.FUNC, stroke_width=4)
        curve.set_points_as_corners([P(gg, ff) for gg, ff in zip(G, F)])
        x = 1.3
        chord = Line(P(0, 0), P(np.sin(x), 1 - np.cos(x)), color=C.APPROX, stroke_width=3)
        slope = (1 - np.cos(x)) / np.sin(x)
        t = brentq(lambda s: np.sin(s) / np.cos(s) - slope, 1e-6, x)  # f'/g' = tan t equals the chord's slope
        tp = P(np.sin(t), 1 - np.cos(t))
        tangent = Line(tp - 0.9 * sc * np.array([1, slope, 0]) / np.hypot(1, slope),
                       tp + 0.9 * sc * np.array([1, slope, 0]) / np.hypot(1, slope), color=C.EPS, stroke_width=3)
        txt = VGroup(label(r"$\dfrac{f(x)}{g(x)}$ = slope of the chord from the origin", font_size=26, color=C.APPROX),
                     label(r"$\dfrac{f'(t)}{g'(t)}$ = slope of the curve at $t$", font_size=26, color=C.EPS),
                     label(r"5.9: \ some $t \in (a, x)$ has the chord's slope,", font_size=26),
                     label(r"so if tangent slopes $\to A$, \ chord slopes do too", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Finally L'Hôpital's rule, which follows from the two-function mean value theorem. <bookmark mark='a'/> "
            "Draw the curve whose coordinates are g of x and f of x; it starts at the origin, because both go to zero. "
            "<bookmark mark='b'/> The ratio f over g is the slope of the chord from the origin. <bookmark mark='c'/> "
            "The ratio of derivatives is the slope of the curve itself. <bookmark mark='d'/> The generalized mean value "
            "theorem says some point of the curve between has a tangent parallel to the chord. So if the tangent slopes "
            "approach A, the chord slopes are dragged along."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Create(axes), FadeIn(al), Create(curve))
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(Create(tangent), FadeIn(Dot(tp, radius=0.07, color=C.EPS)), FadeIn(txt[1]))
            vo.wait_until("d")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        assert 0 < t < x and abs(np.tan(t) - slope) < 1e-9
        self.wait(0.5)
        self.clear_scene()
