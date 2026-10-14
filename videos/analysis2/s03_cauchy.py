from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import SQRT2, Window, load, plain_axes


class Cauchy(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.easy_half()
        self.hole()
        self.compact_complete()
        self.complete_spaces()
        self.monotone()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Cauchy sequences and completeness",
                            r"Can you tell that a sequence converges without knowing its limit?", lit=(1821,), part=2)
        with self.voiceover(
            "Chapter two. To check that a sequence converges, the definition makes you name the limit first. Cauchy "
            "found a test that doesn't."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        d = load("cauchy")
        s = d["s"]
        n_max = 40
        ax = plain_axes([0, n_max + 1, 5], [0.4, 1.05, 0.1], 11.0, 3.3, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-0.35, -1.75, 0])
        dots = VGroup(*[Dot(ax.c2p(k, s[k - 1]), radius=0.045, color=C.SEQ) for k in range(1, n_max + 1)])
        series = MathTex(r"s_n = 1 - \tfrac12 + \tfrac13 - \cdots \pm \tfrac1n", font_size=34, color=C.SEQ)
        series.move_to([3.6, 1.55, 0])
        q = label(r"It converges (to $\ln 2$). \ But how would we know, without knowing $\ln 2$?", font_size=30)
        q.to_edge(UP, buff=0.45)
        dfn = MathTex(r"\forall \varepsilon > 0", r"\;\exists N", r":\;", r"n, m \ge N", r"\Rightarrow",
                      r"d(p_n, p_m) < \varepsilon", font_size=40)
        dfn[0].set_color(C.EPS)
        dfn[1].set_color(C.DELTA)
        dfn_l = label(r"\textbf{Cauchy sequence} (Rudin 3.8):", font_size=30)
        dgrp = VGroup(dfn_l, dfn).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.45)
        nolim = label(r"no limit appears: \ only the terms, compared with each other", font_size=26, color=GREY_A)
        nolim.next_to(dgrp, DOWN, buff=0.15)
        with self.voiceover(
            "In the hook we used the fact that one minus a half plus a third, and so on, sums to the natural log of two. "
            "<bookmark mark='q'/> But suppose you didn't know that. How could you tell these partial sums converge at all? "
            "<bookmark mark='d'/> Cauchy's answer: call a sequence Cauchy if for every epsilon there's an N such that any "
            "two terms past N are within epsilon of each other. <bookmark mark='n'/> No limit appears anywhere: the "
            "terms are only compared with one another."
        ) as vo:
            self.play(Create(ax), FadeIn(series), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03))
            vo.wait_until("q")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeOut(q), Write(dgrp))
            vo.wait_until("n")
            self.play(FadeIn(nolim))

        Nv = ValueTracker(1)
        eps = ValueTracker(0.1)

        def tail_band():
            N = int(round(Nv.get_value()))
            lo, hi = sorted((s[N - 1], s[N]))
            dm = hi - lo
            # the tail's height against epsilon: red while it is too tall, green once it fits
            col = C.CONNECTED_SET if dm < eps.get_value() - 1e-12 else C.PATHOLOGY
            p0, p1 = ax.c2p(N - 0.4, lo), ax.c2p(n_max + 0.6, hi)
            band = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                             fill_opacity=0.22).move_to((p0 + p1) / 2)
            br = BraceBetweenPoints(ax.c2p(n_max + 0.8, hi), ax.c2p(n_max + 0.8, lo), direction=RIGHT, color=col)
            thr = DashedLine(ax.c2p(N - 0.4, 0.4), ax.c2p(N - 0.4, 1.05), color=C.DELTA, stroke_width=2.5)
            return VGroup(band, br, thr)

        def ruler():
            # a bar of length epsilon standing on the tail's floor, beside the brace
            N = int(round(Nv.get_value()))
            lo = min(s[N - 1], s[N])
            x = n_max + 2.4
            e = eps.get_value()
            return VGroup(Line(ax.c2p(x, lo), ax.c2p(x, lo + e), color=C.EPS, stroke_width=5),
                          Line(ax.c2p(x - 0.35, lo + e), ax.c2p(x + 0.35, lo + e), color=C.EPS, stroke_width=3),
                          Line(ax.c2p(x - 0.35, lo), ax.c2p(x + 0.35, lo), color=C.EPS, stroke_width=3),
                          MathTex(r"\varepsilon", font_size=30, color=C.EPS).next_to(ax.c2p(x, lo + e / 2), RIGHT,
                                                                                   buff=0.12))

        epsbar = always_redraw(ruler)

        band = always_redraw(tail_band)
        tail_def = MathTex(r"E_N = \{p_N, p_{N+1}, p_{N+2}, \ldots\}", font_size=34).move_to([-3.6, 1.55, 0])
        crit = label(r"Cauchy $\iff \operatorname{diam} E_N \to 0$ \ (Rudin 3.9)", font_size=28).next_to(tail_def, DOWN,
                                                                                                     buff=0.18)
        crit.align_to(tail_def, LEFT)

        def dlab(N):
            return MathTex(rf"\operatorname{{diam}} E_{{{N}}} = \tfrac{{1}}{{{N + 1}}}", font_size=32).move_to(
                [3.6, 0.85, 0])

        dl = dlab(1)
        eps_l = MathTex(r"\varepsilon = 0.1", font_size=32, color=C.EPS).next_to(dl, DOWN, buff=0.12).align_to(dl, LEFT)
        with self.voiceover(
            "Rudin repackages this with the tail of the sequence: <bookmark mark='e'/> E N, everything from the N-th "
            "term on. <bookmark mark='b'/> The sequence is Cauchy exactly when the diameter of the tail shrinks to zero. "
            "Here the terms alternate, and each step is smaller than the last, so the whole tail lies between s N and "
            "s N plus one, and its diameter is one over N plus one. <bookmark mark='g'/> Epsilon picks a tolerance, "
            "say a tenth; <bookmark mark='w'/> and the tail fits once N reaches 10. <bookmark mark='f'/> For "
            "one twentieth, N is 20. Convergence, checked without ever mentioning log two."
        ) as vo:
            vo.wait_until("e")
            self.play(FadeOut(nolim), FadeIn(tail_def))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(dl), FadeIn(crit))
            vo.wait_until("g")
            self.play(FadeIn(eps_l), FadeIn(epsbar))
            vo.wait_until("w")
            for N in range(2, 11):
                dl2 = dlab(N)
                self.play(Nv.animate.set_value(N), FadeTransform(dl, dl2), run_time=0.3)
                dl = dl2
            vo.wait_until("f")
            eps_l2 = MathTex(r"\varepsilon = 0.05", font_size=32, color=C.EPS).move_to(eps_l, LEFT)
            self.play(eps.animate.set_value(0.05), FadeTransform(eps_l, eps_l2), run_time=0.5)
            eps_l = eps_l2
            for N in range(11, 21):
                dl2 = dlab(N)
                self.play(Nv.animate.set_value(N), FadeTransform(dl, dl2), run_time=0.2)
                dl = dl2
        assert abs(d["diam"][9] - 1 / 11) < 1e-12 and d["diam"][8] >= 0.1 - 1e-12 and d["diam"][19] < 0.05
        self.wait(0.3)
        band.clear_updaters()
        epsbar.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def easy_half(self):
        head = label(r"\textbf{Rudin 3.11(a)} \ Every convergent sequence is Cauchy.", font_size=34).to_edge(UP, buff=0.3)
        rows = [MathTex(r"d(p_n, p_m)", r"\le", r"d(p_n, p) + d(p, p_m)", font_size=40),
                MathTex(r"d(p_n, p_m)", r"<", r"\tfrac{\varepsilon}{2} + \tfrac{\varepsilon}{2} = \varepsilon",
                        font_size=40)]
        whys = [why(r"triangle inequality, through the limit $p$"),
                why(r"once $n, m \ge N$, where $N$ answers $\tfrac{\varepsilon}{2}$ for $p_n \to p$")]
        step = ladder(self, rows, whys, keep=2, top=1.8, buff=0.55, x=0.2)
        conv = label(r"The converse, \emph{Cauchy $\Rightarrow$ convergent}, depends on the space.", font_size=32,
                     color=C.EPS).to_edge(DOWN, buff=0.4)
        # the picture: p, the band of radius eps/2 around it, and two late terms p_n, p_m inside the band
        yl, unit = -1.25, 1.0  # the line's height; screen units per unit of distance
        half = 1.9  # eps/2, in those units
        pv, pn, pm = 0.0, -1.25, 1.05
        assert abs(pn - pv) < half and abs(pm - pv) < half and abs(pm - pn) < 2 * half
        nl = Line([-5.6, yl, 0], [5.6, yl, 0], color=GREY_C, stroke_width=2)
        ball = Rectangle(width=2 * half * unit, height=0.5, stroke_width=0, fill_color=C.EPS, fill_opacity=0.18
                         ).move_to([pv, yl, 0])
        ball_e = VGroup(*[DashedLine([pv + sg * half, yl - 0.25, 0], [pv + sg * half, yl + 0.25, 0], color=C.EPS,
                                     stroke_width=2) for sg in (-1, 1)])
        ball_l = MathTex(r"\text{radius } \tfrac{\varepsilon}{2} \text{ around } p", font_size=26, color=C.EPS
                         ).next_to([pv + half, yl + 0.25, 0], UR, buff=0.1)
        pts = VGroup(Dot([pv, yl, 0], radius=0.08, color=WHITE), Dot([pn, yl, 0], radius=0.075, color=C.SEQ),
                     Dot([pm, yl, 0], radius=0.075, color=C.SEQ))
        pls = VGroup(MathTex(r"p", font_size=32).next_to(pts[0], DOWN, buff=0.2),
                     MathTex(r"p_n", font_size=32, color=C.SEQ).next_to(pts[1], DOWN, buff=0.2),
                     MathTex(r"p_m", font_size=32, color=C.SEQ).next_to(pts[2], DOWN, buff=0.2))
        arcs = VGroup(ArcBetweenPoints([pn, yl + 0.1, 0], [pv, yl + 0.1, 0], angle=-TAU / 5, color=C.EPS, stroke_width=3),
                      ArcBetweenPoints([pv, yl + 0.1, 0], [pm, yl + 0.1, 0], angle=-TAU / 5, color=C.EPS, stroke_width=3))
        arc_l = VGroup(*[MathTex(r"< \tfrac{\varepsilon}{2}", font_size=28, color=C.EPS).next_to(a_, UP, buff=0.08)
                         for a_ in arcs])
        br = BraceBetweenPoints([pn, yl - 0.65, 0], [pm, yl - 0.65, 0], direction=DOWN, color=WHITE)
        br_l = MathTex(r"d(p_n, p_m) < \varepsilon", font_size=30).next_to(br, DOWN, buff=0.1)
        with self.voiceover(
            "One direction is easy. <bookmark mark='h'/> If p n converges to p, then any two late terms are close to "
            "each other, <bookmark mark='a'/> because each is close to p: the triangle inequality, routed through the "
            "limit, <bookmark mark='b'/> with the epsilon over two trick. <bookmark mark='c'/> The converse is the "
            "interesting direction, and whether it holds depends on the space you're in."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(ball), FadeIn(ball_e), FadeIn(ball_l), FadeIn(pts),
                      FadeIn(pls))
            vo.wait_until("a")
            step(0)
            self.play(Create(arcs), FadeIn(arc_l))
            vo.wait_until("b")
            step(1)
            self.play(GrowFromCenter(br), FadeIn(br_l))
            vo.wait_until("c")
            self.play(FadeIn(conv))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hole(self):
        d = load("cauchy")
        num, den = [int(v) for v in d["num"]], [int(v) for v in d["den"]]
        vals = [p / q for p, q in zip(num, den)]
        K = 10  # the tails E_1 ... E_K
        win = Window(1.25, 1.1, y=-1.2)
        axis, labs = win.axis(), win.labels()
        dust = win.dust(height=0.75, target=1000)
        level = ValueTracker(0)

        def tail():
            k = int(round(level.get_value()))
            a, b = sorted((vals[k], vals[k + 1]))
            xa, xb = win.X(a), win.X(b)
            r = Rectangle(width=max(0.02, xb - xa), height=0.55, stroke_width=0, fill_color=C.EPS,
                          fill_opacity=0.25).move_to([(xa + xb) / 2, win.y + 0.3, 0])
            ends = VGroup(Line([xa, win.y - 0.1, 0], [xa, win.y + 0.7, 0], color=C.EPS, stroke_width=3),
                          Line([xb, win.y - 0.1, 0], [xb, win.y + 0.7, 0], color=C.EPS, stroke_width=3))
            return VGroup(r, ends)

        band = always_redraw(tail)
        def mark(v):
            return always_redraw(lambda: Dot(win.P(v, 0.3), radius=0.075, color=C.SEQ).set_opacity(
                1.0 if win.visible(v, 0.2) else 0.0))

        marks = VGroup(*[mark(v) for v in vals])
        hole = win.marker(SQRT2, color=C.HOLE, radius=0.11, dy=0.3, hollow=True)
        head = MathTex(r"1,\ \tfrac32,\ \tfrac75,\ \tfrac{17}{12},\ \tfrac{41}{29},\ \tfrac{99}{70},\ \ldots",
                       font_size=40, color=C.SEQ).to_edge(UP, buff=0.4)
        rule = label(r"$\dfrac{p}{q} \mapsto \dfrac{p + 2q}{p + q}$ \ (the convergents of $\sqrt2$; \ all rational)",
                     font_size=26, color=GREY_A).next_to(head, DOWN, buff=0.15)

        def info(k):
            g = VGroup(MathTex(rf"E_{{{k + 1}}} \text{{ lies between }} \tfrac{{{num[k]}}}{{{den[k]}}} \text{{ and }} "
                               rf"\tfrac{{{num[k + 1]}}}{{{den[k + 1]}}}", font_size=32),
                       MathTex(rf"\operatorname{{diam}} E_{{{k + 1}}} = \tfrac{{1}}{{{den[k]} \cdot {den[k + 1]}}}"
                               rf"\approx {sci(1 / (den[k] * den[k + 1]), 2)}", font_size=32, color=C.EPS))
            return g.arrange(DOWN, buff=0.15).move_to([0, 1.2, 0])

        inf = info(0)

        def wnd(k):
            a, b = sorted((vals[k], vals[k + 1]))
            return (a + b) / 2, 3.2 * (b - a)

        with self.voiceover(
            "Here's a space where it fails: the rational numbers. <bookmark mark='a'/> Start at one and repeatedly send "
            "p over q to p plus 2 q over p plus q. Every term is a fraction, alternating sides of root two. "
            "<bookmark mark='b'/> Each tail lies between two consecutive terms, and its diameter is one over the product "
            "of their denominators, so the sequence is Cauchy. <bookmark mark='z'/> Zoom in after it, keeping the tail "
            "the same size on screen."
        ) as vo:
            self.play(Create(axis), FadeIn(labs), FadeIn(dust))
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rule), LaggedStart(*[FadeIn(m) for m in marks[:5]], lag_ratio=0.25))
            self.add(*marks[5:])
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(inf), *win.zoom_to(*wnd(0)), run_time=1.2)
            vo.wait_until("z")
            for k in range(1, 4):
                nxt = info(k)
                self.play(level.animate.set_value(k), *win.zoom_to(*wnd(k)), FadeTransform(inf, nxt), run_time=1.2)
                inf = nxt
        with self.voiceover(
            "The tails shrink by a factor of nearly six each time. <bookmark mark='h'/> And they're closing in on a "
            "point that isn't there: root two, which Part 1 proved is not a fraction. In the rationals this sequence is "
            "Cauchy, and it has no limit."
        ) as vo:
            for k in range(4, K):
                nxt = info(k)
                self.play(level.animate.set_value(k), *win.zoom_to(*wnd(k)), FadeTransform(inf, nxt), run_time=0.8)
                inf = nxt
            vo.wait_until("h")
            hole.set_z_index(2)
            hole_l = MathTex(r"\sqrt2 \notin \mathbb{Q}", font_size=32, color=C.HOLE).move_to(win.P(SQRT2, 1.0))
            # the later terms (inside the last tail) step aside so the empty point itself shows
            for m in marks[K + 1:]:
                m.clear_updaters()
            self.play(FadeIn(hole, scale=1.6), FadeIn(hole_l), *[FadeOut(m) for m in marks[K + 1:]])
            self.play(Indicate(hole, color=C.HOLE, scale_factor=1.6))
        for i in range(K):
            assert abs(1 / (den[i] * den[i + 1]) - abs(vals[i] - vals[i + 1])) < 1e-15
        self.wait(0.3)
        for m in (axis, labs, dust, band, hole, *marks):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def compact_complete(self):
        d = load("cauchy")
        pts, hulls = d["pts"], d["hulls"]
        o = np.array([-3.4, -0.55, 0])
        sc = 0.78

        def P(xy):
            return o + sc * np.array([xy[0], xy[1], 0.0])

        dots = VGroup(*[Dot(P(p), radius=0.05 if i < 40 else 0.03, color=C.SEQ) for i, p in enumerate(pts)])

        def hull(N, color=C.COMPACT_SET):
            h = hulls[N]
            h = h[~np.isnan(h[:, 0])]
            return Polygon(*[P(p) for p in h], color=color, stroke_width=3, fill_color=color, fill_opacity=0.12)

        H = hull(0)
        thm = VGroup(label(r"\textbf{Rudin 3.11(b)} \ In a compact metric space,", font_size=30),
                     label(r"every Cauchy sequence converges.", font_size=30)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.12)
        thm.move_to([3.3, 2.7, 0])
        rows = VGroup(
            label(r"the closures $\overline{E_N}$ are compact and nested,", font_size=26),
            label(r"and $\operatorname{diam} \overline{E_N} = \operatorname{diam} E_N \to 0$ \ (3.10a)", font_size=26),
            label(r"so they share exactly one point $p$ \ (3.10b)", font_size=26),
            label(r"and $d(p, p_n) \le \operatorname{diam} \overline{E_N} \to 0$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(thm, DOWN, buff=0.4).align_to(thm, LEFT)
        for r in rows:
            r.set_color(GREY_A)
        pdot = Dot(P((0, 0)), radius=0.08, color=WHITE).set_z_index(3)
        plab = MathTex(r"p", font_size=34).move_to(P((1.1, -1.0)))
        plead = Line(plab.get_corner(UL) + 0.05 * (UL), pdot.get_center(), color=GREY_B, stroke_width=1.5, buff=0.1)
        plab = VGroup(plab, plead)
        note_h = label(r"(the yellow polygon: the convex hull of $E_N$, \ which has the same diameter)", font_size=22,
                       color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So when does Cauchy imply convergent? <bookmark mark='t'/> Rudin's first answer: in a compact space, "
            "always. Here's a Cauchy sequence in the plane, spiraling in. <bookmark mark='a'/> Draw its tail, and "
            "close it up. <bookmark mark='b'/> As N grows the closed tails are nested, each inside the last, they're "
            "compact, and their diameters go to zero. <bookmark mark='c'/> Nested compact sets with diameters shrinking "
            "to zero meet in exactly one point, and that point is the limit, <bookmark mark='d'/> because every term "
            "of the N-th tail is within the tail's diameter of it."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(H), FadeIn(rows[0]), FadeIn(note_h))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for N in range(1, 12):
                self.play(Transform(H, hull(N)), dots[N - 1].animate.set_opacity(0.25), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pdot), FadeIn(plab))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        assert np.all(np.diff(d["hdiam"]) < 0)

        allp = np.array([P(p) for p in pts])
        lo, hi = allp.min(0), allp.max(0)
        box = Rectangle(width=hi[0] - lo[0] + 0.5, height=hi[1] - lo[1] + 0.5, color=C.CLOSED_SET, stroke_width=3)
        box.move_to((lo + hi) / 2)
        rk = VGroup(label(r"\textbf{Rudin 3.11(c)} \ In $\R^k$, Cauchy $\Rightarrow$ convergent:", font_size=28),
                    label(r"a Cauchy sequence is bounded,", font_size=26, color=GREY_A),
                    label(r"so it lives in a closed box,", font_size=26, color=GREY_A),
                    label(r"which is compact (Heine--Borel).", font_size=26, color=GREY_A)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rk.next_to(rows, DOWN, buff=0.45).align_to(thm, LEFT)
        with self.voiceover(
            "<bookmark mark='a'/> And in R k, the same is true, with no compactness assumed. A Cauchy sequence is "
            "bounded: one tail has a finite diameter, and there are only finitely many terms before it. "
            "<bookmark mark='b'/> So the whole sequence sits in a closed box, and Part 1's Heine-Borel theorem says the "
            "box is compact. Part 1 pays off again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rk[0]), FadeIn(rk[1]))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(rk[2]))
            self.play(FadeIn(rk[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def complete_spaces(self):
        head = label(r"\textbf{Complete}: every Cauchy sequence converges", font_size=34).to_edge(UP, buff=0.3)
        ref = note(r"Rudin 3.12").next_to(head, DOWN, buff=0.1).align_to(head, RIGHT)
        Y, N_ = r"\checkmark", r"\times"
        data = [
            (r"$\R^k$", Y, r"3.11(c)"),
            (r"any compact metric space", Y, r"3.11(b)"),
            (r"a closed subset of a complete space", Y, r"limits stay inside"),
            (r"$\mathbb{Q}$", N_, r"the convergents of $\sqrt2$"),
            (r"$(0, 1]$", N_, r"$\tfrac1n \to 0$, which is not there"),
            (r"$C[a, b]$, sup distance", Y, r"Part 3"),
            (r"$L^2$, functions with $\int |f|^2 < \infty$", Y, r"Part 5 (Riesz--Fischer, 1907)"),
        ]
        rows = VGroup()
        for i, (sp, ok, why_) in enumerate(data):
            col = C.CONNECTED_SET if ok == Y else C.PATHOLOGY
            r = VGroup(label(sp, font_size=28), MathTex(ok, font_size=36, color=col),
                       label(why_, font_size=24, color=GREY_B))
            rows.add(r)
        xs = (-6.3, 0.3, 1.1)
        ys = [2.45 - 0.5 * i for i in range(5)] + [-0.25, -0.75]
        for r, y in zip(rows, ys):
            r[0].move_to([xs[0], y, 0], aligned_edge=LEFT)
            r[1].move_to([xs[1], y, 0])
            r[2].move_to([xs[2], y, 0], aligned_edge=LEFT)
        later = label(r"function spaces, later:", font_size=22, color=GREY_B).move_to([xs[0], 0.12, 0], aligned_edge=LEFT)
        sep = DashedLine([later.get_right()[0] + 0.2, 0.12, 0], [6.4, 0.12, 0], color=GREY_D, stroke_width=1.5)
        foot = VGroup(label(r"Banach and Hilbert spaces are \emph{required} to be complete.", font_size=28,
                            color=C.EPS),
                      label(r"Every metric space has a completion; completing $\mathbb{Q}$ is one way to build $\R$ "
                            r"(Cantor--M\'eray, Part 1).", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        foot.to_edge(DOWN, buff=0.35)

        # three small number lines: a Cauchy sequence in [0, 1] (complete), in Q, and in (0, 1] (not complete)
        def strip(x0, a, b, vals, target, title, closed):
            w = 3.6
            X = lambda v: x0 - w / 2 + (v - a) / (b - a) * w  # noqa: E731
            y = -1.95
            ln = Line([X(a), y, 0], [X(b), y, 0], color=GREY_C, stroke_width=2)
            ds = VGroup(*[Dot([X(v), y, 0], radius=0.045, color=C.SEQ) for v in vals])
            if closed:
                end = Dot([X(target), y, 0], radius=0.075, color=WHITE)
            else:
                end = Circle(radius=0.085, color=C.HOLE, stroke_width=3).move_to([X(target), y, 0])
                end.set_fill(BACKGROUND, opacity=1)
            end.set_z_index(2)
            ttl = label(title, font_size=24, color=GREY_A).move_to([x0, y + 0.5, 0])
            return VGroup(ln, ds, end, ttl), X, y

        inv = [1 / n for n in range(1, 21)]
        cf = [p_ / q_ for p_, q_ in zip(*[[int(v) for v in load("cauchy")[k]] for k in ("num", "den")])]
        assert abs(cf[-1] - SQRT2) < 1e-9 and all(abs(cf[i + 1] - SQRT2) < abs(cf[i] - SQRT2) for i in range(len(cf) - 1))
        s01, _, _ = strip(-4.3, 0.0, 1.0, inv, 0.0, r"in $[0, 1]$: \ $\tfrac1n \to 0$", True)
        sq, Xq, yq = strip(0.0, 0.9, 1.6, cf, SQRT2, r"in $\mathbb{Q}$: \ a hole at $\sqrt2$", False)
        s0, X0, y0_ = strip(4.3, 0.0, 1.0, inv, 0.0, r"in $(0, 1]$: \ a hole at $0$", False)
        fills = VGroup(Dot([Xq(SQRT2), yq, 0], radius=0.075, color=WHITE), Dot([X0(0.0), y0_, 0], radius=0.075,
                                                                                color=WHITE)).set_z_index(3)
        with self.voiceover(
            "A space where every Cauchy sequence converges is called complete. <bookmark mark='a'/> R k is complete, "
            "and so is every compact space, and every closed subset of a complete space. <bookmark mark='b'/> The "
            "rationals are not, and neither is the interval from zero to one with zero removed: one over n is Cauchy "
            "there, with nowhere to go. <bookmark mark='c'/> The function spaces of this series will be complete too, "
            "and proving it will be real work: continuous functions with the sup distance in Part 3, and square "
            "integrable functions in Part 5. <bookmark mark='d'/> Completeness is so useful that Banach and Hilbert "
            "spaces are defined to have it. And every metric space can be completed, by adding the missing limits: "
            "that's how Cantor and Méray built the reals from the rationals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ref))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3), FadeIn(s01[0]), FadeIn(s01[3]),
                      LaggedStart(*[FadeIn(x) for x in s01[1]], lag_ratio=0.05), FadeIn(s01[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(sq[0]), FadeIn(sq[3]), FadeIn(sq[2]),
                      LaggedStart(*[FadeIn(x) for x in sq[1]], lag_ratio=0.1))
            self.play(FadeIn(rows[4]), FadeIn(s0[0]), FadeIn(s0[3]), FadeIn(s0[2]),
                      LaggedStart(*[FadeIn(x) for x in s0[1]], lag_ratio=0.05))
            self.play(Indicate(sq[2], color=C.HOLE, scale_factor=1.8), Indicate(s0[2], color=C.HOLE, scale_factor=1.8))
            vo.wait_until("c")
            self.play(FadeIn(later), Create(sep), LaggedStart(*[FadeIn(r) for r in rows[5:]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            # completing: the missing limits are added
            self.play(FadeIn(foot[1]), FadeIn(fills, scale=1.5))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monotone(self):
        d = load("cauchy")
        e_seq = d["e_seq"]
        e_N = int(d["e_N"])
        n_max = 40
        ax = plain_axes([0, n_max + 1, 5], [1.75, 3.1, 0.25], 9.9, 3.2, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-1.0, -1.75, 0])
        assert ax.y_range[0] < e_seq[:n_max].min() and e_seq[:n_max].max() < math.e
        board = SequenceBoard(ax, e_seq[:n_max], L=math.e, eps=0.1, N=n_max, n_max=n_max)  # no dot judged yet
        dots = board.dots()
        thm = label(r"\textbf{Rudin 3.14} \ A monotone, bounded sequence converges: \ to its supremum.", font_size=30)
        thm.to_edge(UP, buff=0.45)
        ex = MathTex(r"s_n = \big(1 + \tfrac1n\big)^n", font_size=36, color=C.SEQ).move_to([-4.4, 2.45, 0])
        ex2 = label(r"increasing, and always below 3 \ (Rudin 3.30--3.31)", font_size=24, color=GREY_A)
        ex2.next_to(ex, DOWN, buff=0.12).align_to(ex, LEFT)
        ceil = ValueTracker(3.0)
        roof = always_redraw(lambda: VGroup(
            DashedLine(ax.c2p(0, ceil.get_value()), ax.c2p(n_max + 1, ceil.get_value()), color=C.EPS, stroke_width=2),
            MathTex(r"\text{upper bound}", font_size=24, color=C.EPS).next_to(ax.c2p(n_max + 1, ceil.get_value()), UP,
                                                                           buff=0.06).shift(LEFT * 1.0)))
        with self.voiceover(
            "There's one more way to know a sequence converges without knowing its limit, and it uses the "
            "least-upper-bound property directly. <bookmark mark='t'/> A monotone, bounded sequence converges, "
            "to its supremum. <bookmark mark='a'/> Take one plus one over n, to the n-th power: it increases, and it "
            "never reaches 3. <bookmark mark='b'/> Three is an upper bound, and so are smaller numbers, down to a least "
            "one."
        ) as vo:
            self.play(Create(ax), FadeIn(dots))
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(ex), FadeIn(ex2))
            vo.wait_until("b")
            self.play(FadeIn(roof))
            self.play(ceil.animate.set_value(math.e), run_time=2.0)
        roof.clear_updaters()
        sup_l = MathTex(r"s^* = \sup_n s_n", font_size=32).next_to(ax.c2p(n_max + 1, math.e), RIGHT, buff=0.15)
        band, thr = board.eps_band(), board.threshold()
        pf = VGroup(label(r"$s^* - \varepsilon$ is not an upper bound, \ so some $s_N > s^* - \varepsilon$;", font_size=26),
                    label(r"increasing: \ $s^* - \varepsilon < s_N \le s_n \le s^*$ \ for every $n \ge N$.", font_size=26)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 2.35, 0])
        nm = label(r"Chapter 5: \ $s^* = 1 + 1 + \tfrac12 + \tfrac16 + \cdots = e$", font_size=26, color=GREY_B)
        nm.next_to(pf, DOWN, buff=0.25).align_to(pf, LEFT)
        with self.voiceover(
            "<bookmark mark='s'/> Call the least upper bound s star. <bookmark mark='e'/> Given epsilon, s star minus "
            "epsilon is not an upper bound, so some term s N is above it; <bookmark mark='n'/> and since the sequence "
            "increases, every later term is trapped between s star minus epsilon and s star. For a tenth, every term "
            "from the thirteenth on is trapped. <bookmark mark='c'/> Chapter five identifies this supremum: it's the "
            "number e."
        ) as vo:
            vo.wait_until("s")
            self.play(ReplacementTransform(roof, VGroup(DashedLine(ax.c2p(0, math.e), ax.c2p(n_max + 1, math.e),
                                                                   color=WHITE, stroke_width=2), sup_l)))
            vo.wait_until("e")
            self.play(FadeIn(band), FadeIn(pf[0]))
            board.N.set_value(0)
            vo.wait_until("n")
            self.play(FadeIn(thr), board.N.animate.set_value(e_N), FadeIn(pf[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(nm))
        assert e_N == board.smallest_N(0.1) == 12, (e_N, board.smallest_N(0.1))
        moral = label(r"In $\mathbb{Q}$ it fails again: \ $1, 1.4, 1.41, 1.414, \ldots$ rises, is bounded, and has no "
                      r"rational supremum.", font_size=26, color=C.HOLE).move_to([0, 0.75, 0])
        with self.voiceover(
            "<bookmark mark='m'/> And in the rationals this fails too: the decimal truncations of root two increase, "
            "stay bounded, and have no rational supremum. Completeness, in either form, is exactly what the rationals "
            "lack."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(moral))
        self.wait(0.5)
        for m in (band, thr, dots):
            m.clear_updaters()
        self.clear_scene()
