from __future__ import annotations

from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline
from videos.analysis3.compute import rough


def phi(x):
    x = np.asarray(x, float)
    return np.abs(x - 2 * np.round(x / 2))


class Nowhere(VoiceoverScene):
    def construct(self):
        self.card()
        self.build()
        self.zoom()
        self.proof()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"A continuous function with no derivative", r"How rough can a continuous function be?",
                            lit=(1872,), part=3)
        with self.voiceover("Chapter eight: a function that is continuous everywhere and differentiable nowhere."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def build(self):
        head = VGroup(MathTex(r"f(x) = \sum_{n=0}^{\infty} \left(\tfrac34\right)^n \varphi(4^n x)", font_size=40),
                      label(r"$\varphi(x) = |x|$ on $[-1, 1]$, \ repeated with period $2$ \ (Rudin 7.18)", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        ax = plain_axes([0, 2, 0.5], [0, 4.2, 1], 7.2, 4.4).move_to([-2.9, -1.2, 0])
        x = np.linspace(0, 2, 8001)
        partial = [sum(0.75**k * phi(4.0**k * x) for k in range(n + 1)) for n in range(6)]
        term = [0.75**n * phi(4.0**n * x) for n in range(6)]
        cur = polyline(ax, x, partial[0], color=C.FUNC, stroke_width=3)
        teaser = polyline(ax, x, partial[5], color=C.FUNC, stroke_width=2).set_stroke(opacity=0.45)
        side = VGroup(MathTex(r"\text{term } n: \ \text{height } (\tfrac34)^n, \ \text{slope } \pm 3^n", font_size=30),
                      label(r"M-test with $M_n = (\tfrac34)^n$:", font_size=26, color=C.EPS),
                      label(r"uniform, \ so $f$ is continuous", font_size=26, color=C.EPS),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, 0.6, 0])
        nl = [MathTex(rf"\text{{terms up to }} n = {n}", font_size=28, color=C.FUNC).next_to(ax, DOWN, buff=0.15)
              for n in range(6)]
        with self.voiceover(
            "In 1872 Weierstrass showed the Berlin Academy such a function. Uniform convergence makes it easy to "
            "build; the hard part is the proof that it has no derivative, and Rudin's version of that proof is short. "
            "<bookmark mark='a'/> Rudin uses the zigzag phi: the distance to the nearest even integer. "
            "<bookmark mark='b'/> Add copies of it, the n-th one squeezed horizontally by four to the n and shrunk "
            "vertically by three quarters to the n. Each new term is smaller, but steeper: its slopes are plus or "
            "minus three to the n. <bookmark mark='c'/> The heights form a geometric series, so by the M-test the sum "
            "converges uniformly, and the limit is continuous. Every partial sum has corners; the limit, as we'll see, "
            "is all corners."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            self.play(Create(teaser), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(teaser), Create(cur), FadeIn(nl[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            for n in range(1, 6):
                tm_n = polyline(ax, x, term[n], color=C.APPROX, stroke_width=1.2)
                new = polyline(ax, x, partial[n], color=C.FUNC, stroke_width=3 if n < 4 else 2)
                self.play(FadeIn(tm_n), run_time=0.4)
                self.play(ReplacementTransform(cur, new), FadeOut(tm_n), FadeTransform(nl[n - 1], nl[n]), run_time=0.8)
                cur = new
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zoom(self):
        d = load("weier")
        x0 = float(d["x0"])
        S = 5.4
        box = Square(side_length=S, color=GREY_C, stroke_width=2).move_to([-2.6, -0.45, 0])
        c = box.get_center()
        widths = [0.5, 0.125, 0.03125, 0.0078125, 0.001953125]
        y0 = float(rough(np.array([x0]), 26)[0])

        def view(w):
            x = np.linspace(x0 - w, x0 + w, 4001)  # x0 itself is the middle sample
            y = rough(x, 26)
            assert abs(y[2000] - y0) < 1e-9
            mid, half = (y.max() + y.min()) / 2, (y.max() - y.min()) / 2 * 1.1
            X = c[0] + (x - x0) / w * S / 2
            Y = c[1] + (y - mid) / half * S / 2
            m = VMobject(color=C.FUNC, stroke_width=2.2).set_points_as_corners(np.c_[X, Y, np.zeros_like(X)])
            dot = Dot([c[0], c[1] + (y0 - mid) / half * S / 2, 0], radius=0.07, color=WHITE)
            return VGroup(m, dot)

        views = [view(w) for w in widths]
        labs = [MathTex(rf"\text{{window width }} 2 \times 4^{{-{k}}}" if k else r"\text{window width } 1", font_size=28,
                        color=GREY_A).next_to(box, DOWN, buff=0.15) for k in range(len(widths))]
        head = label(r"Zoom in at $x = 0.3$: \ new corners at every scale", font_size=32).to_edge(UP, buff=0.3)
        side = VGroup(label(r"each zoom by $4$ shrinks the", font_size=26),
                      label(r"vertical range by only about $3$:", font_size=26),
                      label(r"the graph never flattens into a line", font_size=26, color=C.PATHOLOGY),
                      label(r"(each view rescaled to fill the box)", font_size=22, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.7, 0.9, 0])
        brown = VGroup(label(r"the same roughness, met by chance:", font_size=24, color=GREY_A),
                       label(r"a Brownian path \ (the stochastic calculus video)", font_size=24, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.7, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Zoom in at a point. A differentiable function, under enough magnification, looks "
            "like a straight line: that's what a derivative is. <bookmark mark='b'/> This one never does. Every zoom "
            "by a factor of four shrinks the vertical range by only about three, and new corners keep appearing. "
            "<bookmark mark='c'/> Brownian motion, from the stochastic calculus video, has the same property, almost "
            "surely: nature produces these functions on its own."
        ) as vo:
            self.play(FadeIn(head), Create(box), FadeIn(views[0]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            cur, cl = views[0], labs[0]
            for k in range(1, len(widths)):
                self.play(ReplacementTransform(cur, views[k]), FadeTransform(cl, labs[k]), run_time=1.4)
                cur, cl = views[k], labs[k]
            self.play(FadeIn(side[2:]))
            vo.wait_until("c")
            self.play(FadeIn(brown))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        d = load("weier")
        x0, quot, dms = float(d["x0"]), d["quot"], d["dms"]
        m = 3
        dm = float(dms[m - 1])
        # exact contributions (3/4)^n [phi(4^n (x + d)) - phi(4^n x)] / d of each term, in rational arithmetic
        X, D = Fraction(3, 10), Fraction(dm).limit_denominator(10**6)
        assert abs(D) == Fraction(1, 2 * 4**m)

        def phi_q(y):
            return abs(y - 2 * ((y + 1) // 2))

        contrib = [Fraction(3, 4) ** n * (phi_q(4**n * (X + D)) - phi_q(4**n * X)) / D for n in range(m + 3)]
        assert all(c_ == 0 for c_ in contrib[m + 1:]) and abs(contrib[m]) == 3**m
        assert all(abs(contrib[n]) <= 3**n for n in range(m))
        total = sum(contrib)
        assert abs(float(total) - float(quot[m - 1])) < 1e-3 and abs(total) >= Fraction(3**m + 1, 2)
        head = label(r"Why there is no derivative at $x$: \ the difference quotients blow up", font_size=32).to_edge(
            UP, buff=0.3)
        rows = [
            MathTex(r"\delta_m = \pm \tfrac12 4^{-m}", font_size=32),
            MathTex(r"n > m: \ 4^n \delta_m \text{ is even} \Rightarrow \text{term } n \text{ unchanged}", font_size=30),
            MathTex(r"n = m: \ \text{no corner in between} \Rightarrow \text{slope } \pm 3^m", font_size=30, color=C.EPS),
            MathTex(r"n < m: \ |\text{slope}| \le 3^n, \ \text{total} \le \tfrac{3^m - 1}{2}", font_size=30),
            MathTex(r"\Big|\frac{f(x + \delta_m) - f(x)}{\delta_m}\Big| \ge 3^m - \frac{3^m - 1}{2} = \frac{3^m + 1}{2}",
                    font_size=32, color=C.PATHOLOGY),
        ]
        grp = VGroup(*rows)
        for r_ in grp:
            if r_.width > 5.9:
                r_.width = 5.9
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-3.75, -0.5, 0])
        # one small panel per term n = 0..m+2, over the step [x, x + delta_m] (shaded)
        a, b = (x0 - abs(dm), x0 + 2 * abs(dm)) if dm > 0 else (x0 - 2 * abs(dm), x0 + abs(dm))
        tt = np.linspace(a, b, 1500)
        panels = VGroup()
        PW, PH = 3.0, 0.5
        for n in range(m + 3):
            yv = 0.75**n * phi(4.0**n * tt)
            lo, hi = yv.min(), yv.max()
            if hi - lo < 1e-12:
                hi = lo + 1
            cy = 2.15 - 0.8 * n
            pax = Axes(x_range=[a, b, b - a], y_range=[lo - 0.08 * (hi - lo), hi + 0.08 * (hi - lo), hi - lo],
                       x_length=PW, y_length=PH, tips=False,
                       axis_config={"stroke_opacity": 0, "include_ticks": False}).move_to([2.35, cy, 0])
            frame = Rectangle(width=PW, height=PH + 0.12, stroke_color=GREY_D, stroke_width=1).move_to(pax)
            u0, u1 = min(x0, x0 + dm), max(x0, x0 + dm)
            shade = Rectangle(width=pax.c2p(u1, 0)[0] - pax.c2p(u0, 0)[0], height=PH + 0.12, stroke_width=0,
                              fill_color=C.EPS, fill_opacity=0.12).move_to([(pax.c2p(u0, 0)[0] + pax.c2p(u1, 0)[0]) / 2,
                                                                            cy, 0])
            col = C.EPS if n == m else (GREY_B if n > m else C.FUNC)
            g = polyline(pax, tt, yv, color=col, stroke_width=2)
            ya, yb = 0.75**n * phi(4.0**n * np.array([x0, x0 + dm]))
            pa, pb = pax.c2p(x0, ya), pax.c2p(x0 + dm, yb)
            chord = VGroup(Dot(pa, radius=0.045, color=WHITE), Dot(pb, radius=0.045, color=WHITE),
                           DashedLine(pa, pb, color=WHITE, stroke_width=1.5, dash_length=0.05))
            nlab = MathTex(rf"n = {n}", font_size=24, color=col).next_to(frame, LEFT, buff=0.15)
            cv = int(contrib[n])
            assert cv == contrib[n]
            clab = MathTex(rf"{cv:+d}" if cv else r"0", font_size=28, color=col).next_to(frame, RIGHT, buff=0.3)
            panels.add(VGroup(frame, shade, g, chord, nlab, clab))
        ph = label(rf"$m = {m}$: \ each term's share of the quotient", font_size=22, color=GREY_A).next_to(
            panels, UP, buff=0.15)
        sline = Line(panels[-1][5].get_left() + DOWN * 0.35 + LEFT * 0.1, panels[-1][5].get_right() + DOWN * 0.35
                     + RIGHT * 0.1, color=GREY_B, stroke_width=1.5)
        stot = MathTex(rf"{int(total):+d}", font_size=30, color=C.PATHOLOGY).next_to(sline, DOWN, buff=0.15)
        stot.align_to(panels[-1][5], RIGHT)
        sbound = MathTex(rf"|{{{int(total)}}}| \ge 27 - (1 + 3 + 9) = 14 = \tfrac{{3^3 + 1}}{{2}}", font_size=26,
                         color=C.PATHOLOGY).next_to(stot, LEFT, buff=0.4)
        tab = VGroup(MathTex(r"m", r"\quad \text{quotient at } x = 0.3", font_size=26, color=GREY_A))
        for mm in (1, 2, 3, 4, 6, 8, 10):
            q = float(quot[mm - 1])
            tab.add(MathTex(rf"{mm}", r"\quad {" + f"{q:,.0f}".replace(",", "{,}") + "}", font_size=26))
            assert abs(q) >= (3**mm + 1) / 2 - 1e-6
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, -0.3, 0])
        regrid(tab, gap=0.35)
        concl = label(r"$\to \infty$: \ no derivative at $x$; \ and $x$ was arbitrary", font_size=28,
                      color=C.PATHOLOGY).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "Here's Rudin's proof that there is no derivative at any x, carried out at x equal to 0.3. "
            "<bookmark mark='a'/> Step away from x by half of four to the minus m, choosing the sign so that the m-th "
            "zigzag has no corner in between. On the right, m is three, and each panel is one term over that step. "
            "<bookmark mark='b'/> Every later term repeats exactly over the step, because four to the n times the step "
            "is an even integer, the zigzag's period: those terms contribute nothing. <bookmark mark='c'/> The m-th "
            "term is a straight piece with slope three to the m, here twenty seven. <bookmark mark='d'/> The earlier "
            "terms have slopes at most three to the n, which add up to at most three to the m minus one, over two. "
            "<bookmark mark='e'/> So the difference quotient is at least three to the m plus one, over two, which grows "
            "without bound as the step shrinks. <bookmark mark='f'/> Computed for other m, the quotients are exactly "
            "as big as promised, and they never settle down. There is no derivative at x, and x was any point."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), FadeIn(ph),
                      LaggedStart(*[FadeIn(VGroup(p[0], p[1], p[2], p[4])) for p in panels], lag_ratio=0.15),
                      run_time=2.0)
            self.play(LaggedStart(*[FadeIn(p[3]) for p in panels], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), *[FadeIn(p[5]) for p in panels[m + 1:]])
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15), FadeIn(panels[m][5]), Indicate(panels[m][2], color=C.EPS))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), *[FadeIn(p[5]) for p in panels[:m]])
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.15), Create(sline), FadeIn(stot))
            self.play(FadeIn(sbound))
            vo.wait_until("f")
            self.play(FadeOut(VGroup(panels, ph, sline, stot, sbound)))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()
        card = museum_card(r"Weierstrass's function", r"Weierstrass, 1872; \ this form Rudin 7.18",
                           r"`continuous means differentiable, mostly'", r"Rudin 7.18; \ Part 8: most continuous "
                           r"functions are like this (Baire)")
        # beside the card, the exhibit itself: f on [0, 2], to 12 terms (12 more change it by at most 4 (3/4)^12 < 0.13)
        gx = plain_axes([0, 2, 0.5], [0, 4.2, 1], 6.0, 3.4).move_to([-3.4, -0.4, 0])
        xg = np.linspace(0, 2, 16001)
        fg = sum(0.75**k * phi(4.0**k * xg) for k in range(12))
        assert 4 * 0.75**12 < 0.13 and fg.max() < 4.2
        gg = polyline(gx, xg, fg, color=C.FUNC, stroke_width=1.6)
        gl_ = MathTex(r"f(x) = \sum_n \left(\tfrac34\right)^n \varphi(4^n x)", font_size=28, color=C.FUNC).next_to(
            gx, UP, buff=0.15)
        card.move_to([3.6, -0.4, 0])
        with self.voiceover(
            "Into the museum. And a teaser: in Part 8, Baire's theorem will show that in a precise sense most continuous "
            "functions are like this one, and the smooth ones are the rare exceptions."
        ):
            self.play(Create(gx), Create(gg), FadeIn(gl_), FadeIn(card, scale=0.95), run_time=2.0)
        self.wait(0.8)
        self.clear_scene()
