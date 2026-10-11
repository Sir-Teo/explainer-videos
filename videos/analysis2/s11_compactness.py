from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from explainer.analysis.gameboard import largest_delta
from videos.analysis2.common import endpoint, load, plain_axes, polyline


class Compactness(VoiceoverScene):
    def construct(self):
        self.card()
        self.image()
        self.extremes()
        self.inverse()
        self.uniform()
        self.heine()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Continuity and compactness",
                            r"What does a continuous function gain on a compact set?", lit=(), part=2)
        with self.voiceover(
            "Chapter ten. On a compact set, continuous functions behave far better than they have to anywhere else. "
            "Three of the most used theorems in analysis come from one fact."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def image(self):
        ax = plain_axes([0, 4, 1], [-1.6, 1.6, 1], 6.4, 4.6, numbers=False).move_to([-2.0, -0.6, 0])
        f = lambda x: 0.9 * np.sin(1.7 * x) + 0.35 * np.cos(4.3 * x)  # noqa: E731
        a, b = 0.3, 3.7
        g = ax.plot(f, x_range=[a, b, 0.005], color=C.FUNC, stroke_width=4)
        xs = np.linspace(a, b, 20001)
        ys = f(xs)
        m, M = ys.min(), ys.max()
        dom = VGroup(Line(ax.c2p(a, -1.6) + DOWN * 0.25, ax.c2p(b, -1.6) + DOWN * 0.25, color=C.COMPACT_SET,
                          stroke_width=8),
                     endpoint(ax.c2p(a, -1.6) + DOWN * 0.25, True, C.COMPACT_SET),
                     endpoint(ax.c2p(b, -1.6) + DOWN * 0.25, True, C.COMPACT_SET))
        img = VGroup(Line(ax.c2p(0, m) + LEFT * 0.3, ax.c2p(0, M) + LEFT * 0.3, color=C.COMPACT_SET, stroke_width=8),
                     endpoint(ax.c2p(0, m) + LEFT * 0.3, True, C.COMPACT_SET),
                     endpoint(ax.c2p(0, M) + LEFT * 0.3, True, C.COMPACT_SET))
        dl = MathTex(r"[a, b]", font_size=30, color=C.COMPACT_SET).next_to(dom, DOWN, buff=0.15)
        il = MathTex(r"f([a, b])", font_size=30, color=C.COMPACT_SET).next_to(img, UP, buff=0.15)
        thm = label(r"\textbf{Rudin 4.14} \ A continuous image of a compact set is compact.", font_size=30)
        thm.to_edge(UP, buff=0.4)
        steps = VGroup(
            label(r"cover $f(X)$ by open sets $V_\alpha$", font_size=26),
            label(r"the preimages $f^{-1}(V_\alpha)$ are open (4.8) and cover $X$", font_size=26),
            label(r"$X$ compact: finitely many do", font_size=26),
            label(r"so finitely many $V_\alpha$ cover $f(X)$", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.4, 0])
        # an open cover of the image by overlapping intervals, and the preimage of one of them
        centers = np.linspace(m - 0.1, M + 0.1, 7)
        cov = VGroup()
        for i, c in enumerate(centers):
            h = (centers[1] - centers[0]) * 0.75
            x0 = ax.c2p(0, 0)[0] - 0.55 - 0.12 * (i % 2)
            cov.add(Line([x0, ax.c2p(0, c - h)[1], 0], [x0, ax.c2p(0, c + h)[1], 0], color=C.OPEN_SET, stroke_width=4))
        k = 4
        c, h = centers[k], (centers[1] - centers[0]) * 0.75
        inside = (ys > c - h) & (ys < c + h)
        pre = VGroup()
        start = None
        for i, v in enumerate(inside):
            if v and start is None:
                start = i
            if (not v or i == len(inside) - 1) and start is not None:
                pre.add(Line(ax.c2p(xs[start], -1.6) + DOWN * 0.55, ax.c2p(xs[i], -1.6) + DOWN * 0.55, color=C.OPEN_SET,
                             stroke_width=6))
                start = None
        with self.voiceover(
            "<bookmark mark='t'/> The fact: a continuous function maps compact sets to compact sets. "
            "<bookmark mark='a'/> Here the domain is a closed interval, and its image is the set of values on the "
            "vertical axis. <bookmark mark='b'/> Cover the image with open sets. <bookmark mark='c'/> Pull each one "
            "back: by continuity, the preimages are open, and together they cover the domain. <bookmark mark='d'/> The "
            "domain is compact, so finitely many of them already cover it, <bookmark mark='e'/> and then the matching "
            "finitely many open sets cover the image. Open covers, pulled back, are exactly what continuity and "
            "compactness were designed to share."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Create(ax), Create(g), FadeIn(dom), FadeIn(dl))
            self.play(FadeIn(img), FadeIn(il))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), LaggedStart(*[Create(x) for x in cov], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(cov[k].animate.set_color(C.EPS), FadeIn(steps[1]))
            self.play(LaggedStart(*[Create(p) for p in pre], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def extremes(self):
        thm = VGroup(label(r"\textbf{Rudin 4.16} \ A continuous real function on a compact set attains its maximum and "
                           r"minimum.", font_size=28),
                     label(r"(its image is compact: \ closed and bounded, \ so it contains its sup and inf)", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        ax = plain_axes([0, 4, 1], [-1.6, 1.6, 1], 6.0, 3.0, numbers=False).move_to([0, 0.6, 0])
        f = lambda x: 0.9 * np.sin(1.7 * x) + 0.35 * np.cos(4.3 * x)  # noqa: E731
        a, b = 0.3, 3.7
        g = ax.plot(f, x_range=[a, b, 0.005], color=C.FUNC, stroke_width=4)
        xs = np.linspace(a, b, 20001)
        ys = f(xs)
        pmax, pmin = Dot(ax.c2p(xs[ys.argmax()], ys.max()), radius=0.08, color=C.CONNECTED_SET), Dot(
            ax.c2p(xs[ys.argmin()], ys.min()), radius=0.08, color=C.CONNECTED_SET)
        lmax = label(r"max", font_size=24, color=C.CONNECTED_SET).next_to(pmax, UP, buff=0.1)
        lmin = label(r"min", font_size=24, color=C.CONNECTED_SET).next_to(pmin, DOWN, buff=0.1)

        def panel(x0, title, build):
            axp = plain_axes([0, 1.05, 1], [0, 1.6, 1], 3.2, 2.0, numbers=False).move_to([x0, -2.3, 0])
            t = label(title, font_size=22, color=C.PATHOLOGY).next_to(axp, UP, buff=0.12)
            return VGroup(axp, t, *build(axp))

        p1 = panel(-4.4, r"$\tfrac1x$ on $(0, 1]$: \ unbounded", lambda A: [
            A.plot(lambda x: 1 / x, x_range=[1 / 1.6, 1, 0.005], color=C.FUNC, stroke_width=3),
            Arrow(A.c2p(0.62, 1.45), A.c2p(0.55, 1.75), buff=0, color=C.FUNC, stroke_width=3, tip_length=0.12)])
        p2 = panel(0.0, r"$x$ on $(0, 1)$: \ no max", lambda A: [
            A.plot(lambda x: x, x_range=[0, 1], color=C.FUNC, stroke_width=3),
            endpoint(A.c2p(1, 1), False, C.FUNC), endpoint(A.c2p(0, 0), False, C.FUNC)])
        p3 = panel(4.4, r"a jump on $[0, 1]$: \ no max", lambda A: [
            A.plot(lambda x: x, x_range=[0, 1], color=C.FUNC, stroke_width=3),
            endpoint(A.c2p(1, 1), False, C.FUNC), Dot(A.c2p(1, 0.2), radius=0.06, color=C.FUNC)])
        with self.voiceover(
            "<bookmark mark='t'/> Consequence one: on a compact set, a continuous real function attains a largest and "
            "a smallest value. The image is compact, so closed and bounded, so it contains its supremum and infimum. "
            "<bookmark mark='m'/> Here they are. <bookmark mark='f'/> Drop any hypothesis and it fails. On the "
            "half-open interval, one over x is unbounded. On the open interval, x gets arbitrarily close to one but "
            "never reaches it. <bookmark mark='g'/> And on a closed interval, a single jump can remove the top."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm), Create(ax), Create(g))
            vo.wait_until("m")
            self.play(FadeIn(pmax), FadeIn(pmin), FadeIn(lmax), FadeIn(lmin))
            vo.wait_until("f")
            self.play(FadeIn(p1), FadeIn(p2))
            vo.wait_until("g")
            self.play(FadeIn(p3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inverse(self):
        thm = VGroup(label(r"\textbf{Rudin 4.17} \ A continuous bijection from a compact space has a continuous "
                           r"inverse.", font_size=28),
                     label(r"\textbf{Rudin 4.21} \ Without compactness: \ $t \mapsto (\cos t, \sin t)$ on $[0, 2\pi)$",
                           font_size=28, color=C.PATHOLOGY)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        y0 = -0.9
        X = lambda t: -6.2 + t * (4.6 / (2 * np.pi))  # noqa: E731
        seg = VGroup(Line([X(0), y0, 0], [X(2 * np.pi), y0, 0], color=C.FUNC, stroke_width=6),
                     endpoint([X(0), y0, 0], True, C.FUNC), endpoint([X(2 * np.pi), y0, 0], False, C.FUNC))
        tl = VGroup(MathTex(r"0", font_size=26).next_to([X(0), y0, 0], DOWN, buff=0.2),
                    MathTex(r"2\pi", font_size=26).next_to([X(2 * np.pi), y0, 0], DOWN, buff=0.2))
        o = np.array([3.6, y0, 0])
        R = 1.7
        circ = Circle(radius=R, color=C.FUNC, stroke_width=5).move_to(o)
        arrow = Arrow([-1.3, y0, 0], [1.4, y0, 0], buff=0, color=GREY_B, stroke_width=3)
        al = MathTex(r"t \mapsto e^{it}", font_size=30, color=GREY_B).next_to(arrow, UP, buff=0.1)
        p0 = Dot(o + R * RIGHT, radius=0.08, color=WHITE)
        ts_hi = [0.25, 0.15, 0.07]
        ts_lo = [2 * np.pi - 0.25, 2 * np.pi - 0.15, 2 * np.pi - 0.07]
        up = VGroup(*[Dot(o + R * np.array([np.cos(t), np.sin(t), 0]), radius=0.06, color=C.CONNECTED_SET) for t in ts_hi])
        dn = VGroup(*[Dot(o + R * np.array([np.cos(t), np.sin(t), 0]), radius=0.06, color=C.CLOSED_SET) for t in ts_lo])
        up_b = VGroup(*[Dot([X(t), y0, 0], radius=0.06, color=C.CONNECTED_SET) for t in ts_hi])
        dn_b = VGroup(*[Dot([X(t), y0, 0], radius=0.06, color=C.CLOSED_SET) for t in ts_lo])
        verdict = label(r"points close together on the circle go back to opposite ends: \ the inverse jumps at $(1, 0)$",
                        font_size=26, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='t'/> Consequence two: a continuous bijection from a compact space has a continuous "
            "inverse. Compactness is needed. <bookmark mark='a'/> Wrap the half-open interval from zero to two pi "
            "around the circle. It's continuous, one to one, and onto. <bookmark mark='b'/> But take points near the "
            "point one comma zero: those just above it come from near zero, <bookmark mark='c'/> and those just below "
            "come from near two pi. <bookmark mark='d'/> Close together on the circle, far apart on the line: the "
            "inverse is not continuous. The interval isn't compact, and that's the whole problem."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm[0]))
            vo.wait_until("a")
            self.play(FadeIn(thm[1]), FadeIn(seg), FadeIn(tl), GrowArrow(arrow), FadeIn(al), Create(circ), FadeIn(p0))
            vo.wait_until("b")
            self.play(FadeIn(up), FadeIn(up_b))
            vo.wait_until("c")
            self.play(FadeIn(dn), FadeIn(dn_b))
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uniform(self):
        d = load("deltas")
        dfn = VGroup(label(r"\textbf{Uniformly continuous} (Rudin 4.18): \ the same game, but $\delta$ must be chosen "
                           r"\emph{before} $x$", font_size=28),
                     MathTex(r"\forall \varepsilon > 0 \;\exists \delta > 0 \;\forall x, y:\; |x - y| < \delta "
                             r"\Rightarrow |f(x) - f(y)| < \varepsilon", font_size=32)).arrange(DOWN, buff=0.15)
        dfn.to_edge(UP, buff=0.3)
        ax = plain_axes([0, 1.05, 0.25], [0, 1.15, 0.5], 5.6, 4.0, numbers=True, font_size=18,
                        axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.3, -1.4, 0])
        f = np.sqrt
        graph = ax.plot(lambda x: np.sqrt(max(x, 0)), x_range=[0, 1.05, 0.002], color=C.FUNC, stroke_width=3)
        eps, dl = 0.25, 0.25**2
        aT = ValueTracker(0.9)
        board = FunctionBoard(ax, f, a=aT, eps=eps, delta=dl, domain=(0, 1.05))
        eb, db, pc = board.eps_band(), board.delta_band(), board.piece()
        tl = MathTex(r"\sqrt{x} \text{ on } [0, 1]:\ \delta = \varepsilon^2 \text{ works everywhere}", font_size=26,
                     color=C.CONNECTED_SET).next_to(ax, UP, buff=0.15)
        ax2 = plain_axes([0, 1.05, 0.25], [0, 12, 4], 5.6, 4.0, numbers=True, font_size=18,
                         axis_config={"decimal_number_config": {"num_decimal_places": 2}}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.4, -1.4, 0])
        g2 = ax2.plot(lambda x: 1 / x, x_range=[1 / 12, 1.05, 0.001], color=C.FUNC, stroke_width=3)
        e2 = 1.0
        bT = ValueTracker(0.9)
        d_fixed = largest_delta(lambda x: 1 / x, 0.9, 1 / 0.9, e2, 0.9, domain=(0, np.inf))
        board2 = FunctionBoard(ax2, lambda x: 1 / x, a=bT, eps=e2, delta=d_fixed, domain=(1e-6, 1.05))
        eb2, db2, pc2 = board2.eps_band(), board2.delta_band(), board2.piece()
        tl2 = MathTex(r"\tfrac1x \text{ on } (0, 1):\ \text{one } \delta \text{ fails near } 0", font_size=26,
                      color=C.PATHOLOGY).next_to(ax2, UP, buff=0.15)
        with self.voiceover(
            "Consequence three needs a stronger kind of continuity. <bookmark mark='d'/> In ordinary continuity, delta "
            "may depend on the point. Uniform continuity demands one delta that works at every point at once: the "
            "second player must answer before knowing where the game is played. <bookmark mark='a'/> Picture it as a "
            "box of fixed size sliding along the graph: <bookmark mark='b'/> the graph must leave through the sides, "
            "never the top or bottom. For the square root on zero to one, a box with delta equal to epsilon squared "
            "slides all the way to zero. <bookmark mark='c'/> For one over x on the open interval, any fixed box "
            "fails once it gets close enough to zero, where the graph is too steep."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(dfn))
            vo.wait_until("a")
            self.play(Create(ax), Create(graph), FadeIn(tl))
            self.play(FadeIn(eb), FadeIn(db), FadeIn(pc))
            vo.wait_until("b")
            self.play(aT.animate.set_value(0.0), run_time=3.5, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(ax2), Create(g2), FadeIn(tl2))
            self.play(FadeIn(eb2), FadeIn(db2), FadeIn(pc2))
            self.play(bT.animate.set_value(0.25), run_time=3.5, rate_func=linear)
        # sqrt: delta = eps^2 wins at every point of [0, 1]; 1/x: the fixed delta loses at x = 0.25
        x = np.linspace(0, 1, 2001)
        for h in np.linspace(-dl, dl, 21)[1:-1]:
            assert np.all(np.abs(np.sqrt(np.clip(x + h, 0, 1)) - np.sqrt(x)) < eps)
        assert largest_delta(lambda x: 1 / x, 0.25, 4.0, e2, 0.25, domain=(0, np.inf)) < d_fixed
        for m in (eb, db, pc, eb2, db2, pc2):
            m.clear_updaters()
        self.clear_scene()

        xs, d_inv = d["xs"], d["d_inv"]
        ax3 = plain_axes([0, 1.0, 0.25], [0, 0.1, 0.05], 8.0, 3.8, numbers=True, font_size=20,
                         axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([0, -1.0, 0])
        xx = np.linspace(0.02, 1.0, 400)
        exact = polyline(ax3, xx, xx - 1 / (1 / xx + 0.1), color=C.DELTA, stroke_width=3)
        pts = VGroup(*[Dot(ax3.c2p(x, dd), radius=0.07, color=WHITE) for x, dd in zip(xs, d_inv)])
        head = MathTex(r"\tfrac1x,\ \varepsilon = 0.1:\ \text{the largest } \delta \text{ at each } x", font_size=34)
        head.to_edge(UP, buff=0.5)
        f_l = MathTex(r"\delta(x) = x - \frac{1}{1/x + \varepsilon} \to 0", font_size=32, color=C.DELTA).move_to([-2.6, 1.75, 0])
        note_ = label(r"no single $\delta > 0$ is below all of them", font_size=28, color=C.PATHOLOGY).next_to(
            ax3, DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Here are the best deltas for one over x at a tolerance of a tenth, computed at seven "
            "points. <bookmark mark='b'/> They shrink to zero as x approaches zero, so no single positive delta works "
            "everywhere: one over x is continuous on the open interval, but not uniformly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax3), Create(exact), FadeIn(f_l))
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        assert np.allclose(d_inv, xs - 1 / (1 / xs + 0.1), rtol=1e-3, atol=1e-6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heine(self):
        thm = label(r"\textbf{Rudin 4.19} \ Continuous on a compact space $\Rightarrow$ uniformly continuous.",
                    font_size=30).to_edge(UP, buff=0.4)
        y0 = 0.4
        X = lambda v: -5.5 + v * 11.0  # noqa: E731
        line = Line([X(0) - 0.2, y0, 0], [X(1) + 0.2, y0, 0], color=GREY_C, stroke_width=2)
        eps = 0.25
        pts = np.r_[0.0, np.geomspace(0.004, 1.0, 24)]
        # for sqrt at p, the largest delta that works for eps/2 (computed), and the cover by half-width intervals
        deltas = np.array([largest_delta(np.sqrt, p, float(np.sqrt(p)), eps / 2, 1.0, domain=(0, 1.0 + 1e-9))
                           for p in pts])
        bars = VGroup()
        for i, (p, dd) in enumerate(zip(pts, deltas)):
            r = dd / 2
            yy = y0 - 0.25 - 0.14 * (i % 6)
            bars.add(Line([X(max(p - r, 0)), yy, 0], [X(min(p + r, 1)), yy, 0], color=C.OPEN_SET, stroke_width=4))
        # a finite subcover, chosen greedily from the left
        chosen, reach = [], 0.0
        order = np.argsort(pts)
        while reach < 1.0:
            cand = [i for i in order if pts[i] - deltas[i] / 2 <= reach + 1e-12]
            best = max(cand, key=lambda i: pts[i] + deltas[i] / 2)
            assert pts[best] + deltas[best] / 2 > reach, "the sample intervals must cover [0, 1]"
            chosen.append(best)
            reach = pts[best] + deltas[best] / 2
        dmin = min(deltas[i] / 2 for i in chosen)
        steps = VGroup(label(r"each point $p$ has its own $\delta_p$ (for $\varepsilon/2$)", font_size=26),
                       label(r"the intervals of half-width $\delta_p/2$ cover the space; \ finitely many suffice",
                             font_size=26),
                       label(r"$\delta = $ the smallest of those finitely many $\delta_p/2$, \ which is positive",
                             font_size=26, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        steps.to_edge(DOWN, buff=0.4)
        lbl = MathTex(r"\sqrt{x} \text{ on } [0, 1]", font_size=30, color=C.FUNC).next_to(line, UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='t'/> And now the theorem: on a compact space, continuous implies uniformly continuous. "
            "<bookmark mark='a'/> Each point has its own delta, for epsilon over two. <bookmark mark='b'/> The "
            "intervals of half those widths cover the space, so finitely many of them cover it. <bookmark mark='c'/> "
            "Take delta to be the smallest of those finitely many half-widths. A minimum of finitely many positive "
            "numbers is positive, and a short triangle-inequality argument shows this one delta works everywhere. With "
            "infinitely many, the infimum could be zero, which is exactly what happened to one over x."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm), Create(line), FadeIn(lbl))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), *[bars[i].animate.set_stroke(opacity=0.25) for i in range(len(bars))
                                          if i not in chosen])
            self.play(*[bars[i].animate.set_color(C.EPS).set_stroke(width=6) for i in chosen])
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        assert dmin > 0 and reach >= 1.0
        self.wait(0.5)
        self.clear_scene()
