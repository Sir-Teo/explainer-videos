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
        thm = VGroup(label(r"At a local maximum, \ $f'(x) = 0$", font_size=34),
                     label(r"from the left, \ $\dfrac{f(t) - f(x)}{t - x} \ge 0$;", font_size=28),
                     label(r"from the right, \ $\dfrac{f(t) - f(x)}{t - x} \le 0$.", font_size=28),
                     label(r"The limit is both: \ $0$.", font_size=28, color=C.EPS))
        thm[0].to_edge(UP, buff=0.3)
        ref = note(r"Rudin 5.8")
        VGroup(ref, *thm[1:]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, -0.3, 0])
        # secants from the top to t = x - 0.6 and t = x + 0.6, extended a little past both points
        sec, sec_l = VGroup(), VGroup()
        for dt, txt_, side in ((-0.6, r"\ge 0", LEFT), (0.6, r"\le 0", RIGHT)):
            t = xm + dt
            q = (f(t) - f(xm)) / (t - xm)
            assert (q > 0) if dt < 0 else (q < 0)
            lo_, hi_ = min(t, xm) - 0.25, max(t, xm) + 0.25
            sec.add(VGroup(Line(ax.c2p(lo_, f(xm) + q * (lo_ - xm)), ax.c2p(hi_, f(xm) + q * (hi_ - xm)), color=C.APPROX,
                                stroke_width=3), Dot(ax.c2p(t, f(t)), radius=0.06, color=C.APPROX)))
            sec_l.add(MathTex(r"\text{slope} " + txt_, font_size=26, color=C.APPROX).next_to(
                ax.c2p(t, f(t)), side + DOWN * 0.6, buff=0.15))
        with self.voiceover(
            "First, a lemma. <bookmark mark='a'/> At a local maximum the derivative is zero. <bookmark mark='b'/> "
            "Approaching from the left, f of t is at most f of x and t minus x is negative, so the difference quotients "
            "are at least zero; <bookmark mark='c'/> from the right they're at most zero. <bookmark mark='d'/> The "
            "limit has to be both."
        ) as vo:
            self.play(Create(ax), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(thm[0]), FadeIn(ref), FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(thm[1]), Create(sec[0]), FadeIn(sec_l[0]))
            vo.wait_until("c")
            self.play(FadeIn(thm[2]), Create(sec[1]), FadeIn(sec_l[1]))
            vo.wait_until("d")
            self.play(FadeIn(thm[3]), Create(tan))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shear(self):
        ax = plain_axes([0, 4.2, 1], [-1.5, 3.5, 1], 7.4, 5.0, numbers=False).move_to([-2.4, -0.75, 0])
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
        head = label(r"The mean value theorem", font_size=34).to_edge(UP, buff=0.3)
        thm = VGroup(MathTex(r"f(b) - f(a) = (b - a)\, f'(\xi)", font_size=32),
                     label(r"for some $\xi \in (a, b)$ \ (Rudin 5.10)", font_size=24, color=GREY_A)
                     ).arrange(DOWN, buff=0.12).move_to([4.3, 2.25, 0])

        def numbered(n, *lines, color=WHITE):
            num = label(rf"{n}.", font_size=24)
            body = VGroup(*[label(t_, font_size=24, color=color) for t_ in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08)
            body.next_to(num, RIGHT, buff=0.15, aligned_edge=UP)
            return VGroup(num, body)

        rows_ = [numbered(1, r"shear vertically: \ subtract the chord"),
                 numbered(2, r"now the ends are level; \ a continuous", r"function on $[a, b]$ has a max (4.16)"),
                 numbered(3, r"there the slope is $0$ \ (5.8)"),
                 numbered(4, r"shear back: \ slope $0$ becomes", r"the chord's slope")]
        rows_[3][1][1].set_color(C.EPS)
        steps_g = VGroup(*rows_).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, -0.3, 0])
        # the indexing the voiceover uses: 0, (1, 2), 3, (4, 5)
        steps = [rows_[0], rows_[1][0], rows_[1][1], rows_[2], rows_[3][0], rows_[3][1]]
        steps[1] = VGroup(rows_[1][0], rows_[1][1][0])
        steps[2] = rows_[1][1][1]
        steps[4] = VGroup(rows_[3][0], rows_[3][1][0])
        steps[5] = rows_[3][1][1]
        marks = VGroup(*[VGroup(Line(ax.c2p(v, 0) + DOWN * 0.08, ax.c2p(v, 0) + UP * 0.08, color=c_),
                                MathTex(t_, font_size=28, color=c_).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
                         for v, t_, c_ in ((a, r"a", GREY_B), (b, r"b", GREY_B))])
        xi_mark = VGroup(Line(ax.c2p(xi, 0) + DOWN * 0.08, ax.c2p(xi, 0) + UP * 0.08, color=C.EPS),
                         MathTex(r"\xi", font_size=28, color=C.EPS).next_to(ax.c2p(xi, 0), DOWN, buff=0.15))
        gen = label(r"Rudin 5.9, the general form: \ $[f(b) - f(a)]\, g'(\xi) = [g(b) - g(a)]\, f'(\xi)$", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.35)
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
            self.play(FadeIn(head), Create(ax), FadeIn(cv), FadeIn(ch), FadeIn(ends), FadeIn(marks))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            self.play(sT.animate.set_value(1.0), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(xi_dot), Create(tg), FadeIn(steps[3]), FadeIn(xi_mark))
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
        head = VGroup(label(r"\textbf{Rudin 5.11} \ On $(a, b)$:", font_size=32),
                      label(r"$f' \ge 0$ $\Rightarrow$ $f$ increasing; \quad $f' = 0$ $\Rightarrow$ $f$ constant; \quad "
                            r"$f' \le 0$ $\Rightarrow$ $f$ decreasing", font_size=28)).arrange(DOWN, buff=0.15)
        head.to_edge(UP, buff=0.3)
        # f' is positive, then zero on [2.5, 3.3], then negative, then positive; f is its integral
        def fp(x):
            x = np.asarray(x, float)
            return np.select([x < 2.5, x < 3.3, x < 4.9],
                             [1.2 * np.sin(np.pi * x / 2.5), 0.0 * x, -1.0 * np.sin(np.pi * (x - 3.3) / 1.6)],
                             0.9 * np.sin(np.pi * (x - 4.9) / 1.1))
        xs = np.linspace(0, 6.0, 3001)
        F = -1.0 + np.concatenate([[0.0], np.cumsum((fp(xs[1:]) + fp(xs[:-1])) / 2 * np.diff(xs))])
        f = lambda x: np.interp(x, xs, F)  # noqa: E731
        axf = plain_axes([0, 6.0, 1], [-1.3, 1.3, 1], 7.6, 2.5, numbers=False).move_to([-2.5, 0.75, 0])
        axd = plain_axes([0, 6.0, 1], [-1.3, 1.3, 1], 7.6, 1.9, numbers=False).move_to([-2.5, -2.05, 0])
        sign = np.select([xs < 2.5, xs <= 3.3, xs < 4.9], [1.0, 0.0, -1.0], 1.0)  # the sign of f', by construction
        assert np.all(np.sign(np.round(fp(xs), 9)) * sign >= 0)
        cols = {1.0: C.CONNECTED_SET, 0.0: C.EPS, -1.0: C.PATHOLOGY}
        f_plain = polyline(axf, xs, F, color=C.FUNC, stroke_width=4)
        d_plain = polyline(axd, xs, fp(xs), color=GREY_A, stroke_width=3)
        f_col, shade = VGroup(), VGroup()
        start = 0
        for i in range(1, len(xs) + 1):
            if i == len(xs) or sign[i] != sign[start]:
                seg = slice(start, min(i + 1, len(xs)))
                c = cols[float(sign[start])]
                f_col.add(polyline(axf, xs[seg], F[seg], color=c, stroke_width=5))
                if sign[start] != 0:
                    pts = [axd.c2p(xs[seg][0], 0)] + [axd.c2p(a, b) for a, b in zip(xs[seg], fp(xs[seg]))] + [
                        axd.c2p(xs[seg][-1], 0)]
                    shade.add(Polygon(*pts, stroke_width=0, fill_color=c, fill_opacity=0.35))
                start = i
        assert len(f_col) == 4
        fl = MathTex(r"f", font_size=30, color=C.FUNC).next_to(axf, LEFT, buff=0.15)
        dl = MathTex(r"f'", font_size=30, color=GREY_A).next_to(axd, LEFT, buff=0.15)
        keys = VGroup(label(r"$f' > 0$: \ $f$ rises", font_size=24, color=C.CONNECTED_SET),
                      label(r"$f' = 0$: \ $f$ is constant", font_size=24, color=C.EPS),
                      label(r"$f' < 0$: \ $f$ falls", font_size=24, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.15)
        keys.move_to([4.6, -1.9, 0])
        # the reason: a chord over [x1, x2] has the slope of the tangent at some xi between
        x1, x2 = 0.25, 1.6
        m = (f(x2) - f(x1)) / (x2 - x1)
        cand = xs[(xs > x1) & (xs < x2)]
        xi = float(cand[np.argmin(np.abs(fp(cand) - m))])
        assert abs(fp(xi) - m) < 1e-2 and m > 0
        chord = Line(axf.c2p(x1, f(x1)), axf.c2p(x2, f(x2)), color=C.APPROX, stroke_width=3)
        tng = Line(axf.c2p(xi - 0.5, f(xi) - 0.5 * m), axf.c2p(xi + 0.5, f(xi) + 0.5 * m), color=C.EPS, stroke_width=3)
        cd = VGroup(Dot(axf.c2p(x1, f(x1)), radius=0.06, color=C.APPROX), Dot(axf.c2p(x2, f(x2)), radius=0.06,
                                                                               color=C.APPROX),
                    Dot(axf.c2p(xi, f(xi)), radius=0.06, color=C.EPS))
        mvt = VGroup(MathTex(r"f(x_2) - f(x_1)", r"=", r"\underbrace{(x_2 - x_1)}_{> 0}", r"\,",
                             r"\underbrace{f'(\xi)}_{\ge 0}", font_size=32),
                     MathTex(r"\Rightarrow\ f(x_2) \ge f(x_1)", font_size=32, color=C.CONNECTED_SET)
                     ).arrange(DOWN, buff=0.25)
        mvt[0][0].set_color(C.APPROX)
        mvt.move_to([4.2, 0.9, 0])
        note = label(r"information about $f'$ becomes information about $f$", font_size=24, color=GREY_A)
        note.next_to(mvt, DOWN, buff=0.35).set_x(4.2)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem's main job is to turn facts about the derivative into facts about the "
            "function. <bookmark mark='b'/> If the derivative is never negative, then for any two points the difference "
            "f of x two minus f of x one is x two minus x one times some derivative, so it's never negative: f "
            "increases. <bookmark mark='c'/> A zero derivative means a constant function."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(axf), Create(axd), FadeIn(fl), FadeIn(dl))
            self.play(Create(f_plain), Create(d_plain), run_time=1.5)
            self.play(FadeIn(shade), ReplacementTransform(f_plain, f_col), FadeIn(head[1]), FadeIn(keys), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(cd[:2]))
            self.play(Create(tng), FadeIn(cd[2]), FadeIn(mvt[0]))
            self.play(FadeIn(mvt[1]), FadeIn(note))
            vo.wait_until("c")
            self.play(Indicate(f_col[1], color=C.EPS, scale_factor=1.0), Indicate(keys[1], color=C.EPS), run_time=1.2)
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
        sk = plain_axes([0, 1, 1], [0, 1, 1], 7.0, 3.4, numbers=False).move_to([0, -0.9, 0])
        gs = lambda t: 1.8 * (t - 0.45) ** 2 + 0.12  # noqa: E731
        gsk = sk.plot(gs, x_range=[0.05, 0.95, 0.01], color=C.FUNC, stroke_width=4)
        slopes = VGroup(*[Line(sk.c2p(max(t - 0.08, 0.0), gs(t) + (max(t - 0.08, 0.0) - t) * 3.6 * (t - 0.45)),
                               sk.c2p(min(t + 0.08, 1.0), gs(t) + (min(t + 0.08, 1.0) - t) * 3.6 * (t - 0.45)),
                               color=c, stroke_width=4) for t, c in ((0.05, C.PATHOLOGY), (0.95, C.CONNECTED_SET),
                                                                      (0.45, C.EPS))])
        sdots = VGroup(*[Dot(sk.c2p(t, gs(t)), radius=0.06, color=WHITE) for t in (0.05, 0.95, 0.45)])
        slabs = VGroup(MathTex(r"a", font_size=28).next_to(sk.c2p(0.05, 0), DOWN, buff=0.1),
                       MathTex(r"b", font_size=28).next_to(sk.c2p(0.95, 0), DOWN, buff=0.1),
                       MathTex(r"g'(a) < 0", font_size=24, color=C.PATHOLOGY).next_to(sk.c2p(0.05, gs(0.05)), LEFT,
                                                                                     buff=0.65),
                       MathTex(r"g'(b) > 0", font_size=24, color=C.CONNECTED_SET).next_to(sk.c2p(0.95, gs(0.95)),
                                                                                         RIGHT, buff=0.65),
                       MathTex(r"g'(x) = 0", font_size=24, color=C.EPS).next_to(sk.c2p(0.45, gs(0.45)), UP,
                                                                               buff=0.3),
                       MathTex(r"g(t) = f(t) - \lambda t", font_size=28, color=C.FUNC).move_to(sk.c2p(0.5, 0.95)))
        sketch = VGroup(sk, gsk, slopes, sdots, slabs)
        with self.voiceover(
            "<bookmark mark='t'/> Darboux noticed something surprising: a derivative always has the intermediate value "
            "property, continuous or not. <bookmark mark='p'/> To hit a value lambda, subtract lambda t from f: the "
            "result slopes down at a and up at b, so its minimum is inside, where its derivative is zero. "
            "<bookmark mark='a'/> Remember the museum piece: its derivative is discontinuous at zero, <bookmark mark='b'/> "
            "yet on every interval next to zero it takes every value between about minus one and one, again and again. "
            "<bookmark mark='c'/> So a derivative can never have a simple jump: if it's discontinuous, it's wildly so."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm), Create(sk), Create(gsk))
            vo.wait_until("p")
            self.play(FadeIn(pf), FadeIn(slabs[5]))
            self.play(Create(slopes[:2]), FadeIn(sdots[:2]), FadeIn(slabs[:4]))
            self.play(Create(slopes[2]), FadeIn(sdots[2]), FadeIn(slabs[4]))
            vo.wait_until("a")
            self.play(FadeOut(sketch), run_time=0.5)
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
        o = np.array([-4.6, -2.6, 0])
        sc = 2.9

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
        tangent = Line(tp - 0.25 * sc * np.array([1, slope, 0]) / np.hypot(1, slope),
                       tp + 0.5 * sc * np.array([1, slope, 0]) / np.hypot(1, slope), color=C.EPS, stroke_width=3)
        assert tangent.get_bottom()[1] > o[1] - 0.05  # the tangent stays above the g-axis
        xend = P(np.sin(x), 1 - np.cos(x))
        xl = MathTex(r"(g(x), f(x))", font_size=26, color=C.APPROX).next_to(xend, RIGHT, buff=0.15)
        xdot = Dot(xend, radius=0.06, color=C.APPROX)
        tl_ = MathTex(r"t", font_size=28, color=C.EPS).next_to(tp, DR, buff=0.08)
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
            self.play(Create(chord), FadeIn(xdot), FadeIn(xl), FadeIn(txt[0]))
            vo.wait_until("c")
            self.play(Create(tangent), FadeIn(Dot(tp, radius=0.07, color=C.EPS)), FadeIn(tl_), FadeIn(txt[1]))
            vo.wait_until("d")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        assert 0 < t < x and abs(np.tan(t) - slope) < 1e-9
        self.wait(0.5)
        self.clear_scene()
