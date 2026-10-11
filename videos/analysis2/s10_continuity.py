from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import endpoint, load, plain_axes, polyline


class Continuity(VoiceoverScene):
    def construct(self):
        self.card()
        self.limits()
        self.board()
        self.sequences()
        self.preimages()
        self.algebra()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Continuity", r"What does it mean for a function to have no jumps?", lit=(1817, 1821),
                            part=2)
        with self.voiceover(
            "Chapter nine. Bolzano in 1817 and Cauchy in 1821 turned no jumps into a definition, using the same game "
            "we've been playing with sequences."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def limits(self):
        ax = plain_axes([0, 4.2, 1], [0, 12, 2], 6.4, 4.6, numbers=True, font_size=20).move_to([-3.2, -0.9, 0])
        f = lambda x: x * x  # noqa: E731
        g1 = ax.plot(f, x_range=[0, 2.97], color=C.FUNC, stroke_width=4)
        g2 = ax.plot(f, x_range=[3.03, 3.45], color=C.FUNC, stroke_width=4)
        hole = Circle(radius=0.07, color=C.FUNC, stroke_width=3).set_fill(BACKGROUND, 1).move_to(ax.c2p(3, 9))
        odd = Dot(ax.c2p(3, 4), radius=0.07, color=C.PATHOLOGY)
        odd_l = MathTex(r"f(3) = 4", font_size=28, color=C.PATHOLOGY).next_to(odd, RIGHT, buff=0.12)
        dfn = VGroup(label(r"\textbf{Limit of a function} (Rudin 4.1)", font_size=30),
                     MathTex(r"\lim_{x \to p} f(x) = q", font_size=36),
                     MathTex(r"\forall \varepsilon > 0 \;\exists \delta > 0:", font_size=32),
                     MathTex(r"0 < |x - p| < \delta \Rightarrow |f(x) - q| < \varepsilon", font_size=32),
                     ).arrange(DOWN, buff=0.18).move_to([3.4, 1.5, 0])
        dfn[2][0][0:4].set_color(C.EPS)
        dfn[2][0][4:8].set_color(C.DELTA)
        nb = label(r"$0 < |x - p|$: \ the value at $p$ itself is ignored", font_size=26, color=C.EPS).next_to(dfn, DOWN,
                                                                                                        buff=0.3)
        here = MathTex(r"\lim_{x \to 3} f(x) = 9 \ne f(3)", font_size=32).next_to(nb, DOWN, buff=0.3)
        cont = VGroup(label(r"\textbf{Continuous at $p$} (Rudin 4.5):", font_size=28),
                      MathTex(r"\lim_{x \to p} f(x) = f(p)", font_size=34, color=C.CONNECTED_SET)).arrange(DOWN, buff=0.1)
        cont.next_to(here, DOWN, buff=0.35)
        with self.voiceover(
            "First, limits of functions. <bookmark mark='a'/> Here's x squared, except that someone has moved the "
            "value at 3 down to 4. <bookmark mark='d'/> The limit of f at p is q if for every epsilon there's a delta "
            "such that every x within delta of p, other than p itself, has f of x within epsilon of q. "
            "<bookmark mark='n'/> The value at p is deliberately ignored, <bookmark mark='h'/> so here the limit at 3 "
            "is nine, whatever f of 3 says. <bookmark mark='c'/> And f is continuous at p when the limit exists and "
            "equals the actual value. This f is not continuous at 3."
        ) as vo:
            self.play(Create(ax))
            vo.wait_until("a")
            self.play(Create(g1), Create(g2), FadeIn(hole), FadeIn(odd), FadeIn(odd_l))
            vo.wait_until("d")
            self.play(FadeIn(dfn))
            vo.wait_until("n")
            self.play(FadeIn(nb))
            vo.wait_until("h")
            self.play(FadeIn(here), Indicate(hole, color=C.EPS, scale_factor=2))
            vo.wait_until("c")
            self.play(FadeIn(cont))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        d = load("deltas")
        ax = plain_axes([2.0, 4.0, 0.5], [4, 16, 2], 9.0, 5.0, numbers=True, font_size=20,
                        axis_config={"decimal_number_config": {"num_decimal_places": 1}}, y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-1.3, -0.75, 0])
        f = lambda x: x * x  # noqa: E731
        graph = ax.plot(f, x_range=[2.0, 4.0], color=C.FUNC, stroke_width=3)
        board = FunctionBoard(ax, f, a=3.0, eps=1.0, delta=0.4)
        eb, db, pc, pm = board.eps_band(), board.delta_band(), board.piece(), board.point_marks()
        head = MathTex(r"f(x) = x^2 \text{ at } 3:", r"\quad |x - 3| < \delta \Rightarrow |x^2 - 9| < \varepsilon",
                       font_size=34).to_edge(UP, buff=0.3)

        def readout(e, dl):
            return VGroup(MathTex(rf"\varepsilon = {e:g}", font_size=32, color=C.EPS),
                          MathTex(rf"\delta = {dl:.4f}", font_size=32, color=C.DELTA)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.12).move_to(
                [5.0, 1.2, 0])

        ro = readout(1.0, 0.4)
        with self.voiceover(
            "Continuity as a game. <bookmark mark='a'/> Take x squared at 3. The first player, epsilon, draws a band "
            "around the value 9. <bookmark mark='b'/> The second player answers with a strip around 3, of half-width "
            "delta. They win if the graph over the strip stays inside the band: green where it does, red where it "
            "escapes. <bookmark mark='c'/> A strip too wide loses at the edges. <bookmark mark='d'/> The best answer is "
            "the widest strip that works."
        ) as vo:
            self.play(Create(ax), Create(graph), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eb), FadeIn(pm))
            vo.wait_until("b")
            self.play(FadeIn(db), FadeIn(pc), FadeIn(ro))
            vo.wait_until("c")
            self.play(board.delta.animate.set_value(0.55), Transform(ro, readout(1.0, 0.55)), run_time=1.2)
            vo.wait_until("d")
            best = board.largest_delta(1.0)
            self.play(board.delta.animate.set_value(best), Transform(ro, readout(1.0, best)), run_time=1.2)
        deltas = []
        with self.voiceover(
            "<bookmark mark='a'/> Tighten epsilon to a half: the strip must narrow. <bookmark mark='b'/> At a tenth, "
            "the widest strip has half-width 0.0166. The right edge binds, because the parabola is steeper there: delta "
            "is the square root of 9.1, minus 3. <bookmark mark='c'/> Whatever epsilon you pick, some delta answers it. "
            "That's continuity at 3."
        ) as vo:
            for mk, e in (("a", 0.5), ("b", 0.1)):
                vo.wait_until(mk)
                self.play(board.eps.animate.set_value(e), run_time=1.0)
                best = board.largest_delta(1.0)
                deltas.append(best)
                self.play(board.delta.animate.set_value(best), Transform(ro, readout(e, best)), run_time=1.0)
            vo.wait_until("c")
            formula = MathTex(r"\delta = \sqrt{9 + \varepsilon} - 3", font_size=32, color=C.DELTA).next_to(ro, DOWN,
                                                                                                        buff=0.35)
            self.play(FadeIn(formula))
        assert abs(deltas[1] - float(d["d_sq"])) < 1e-4 and abs(deltas[1] - (np.sqrt(9.1) - 3)) < 1e-4
        assert abs(deltas[0] - (np.sqrt(9.5) - 3)) < 1e-4
        self.wait(0.3)
        for m in (eb, db, pc, pm):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def sequences(self):
        thm = VGroup(label(r"\textbf{Rudin 4.2 and 4.6} \ $f$ is continuous at $p$ $\iff$", font_size=32),
                     label(r"$f(p_n) \to f(p)$ for every sequence $p_n \to p$", font_size=32)).arrange(DOWN, buff=0.15)
        thm.to_edge(UP, buff=0.5)
        ax = plain_axes([-1.5, 1.5, 0.5], [-1.4, 1.4, 1], 7.5, 4.2, numbers=False).move_to([0, -1.1, 0])
        u = np.linspace(1 / 1.5, 260, 40000)  # sample in 1/x, so every oscillation gets the same number of points
        g = polyline(ax, -1 / u, -np.sin(u), color=C.FUNC, stroke_width=2.5)
        g2 = polyline(ax, 1 / u, np.sin(u), color=C.FUNC, stroke_width=2.5)
        lab = MathTex(r"\sin\tfrac1x", font_size=32, color=C.FUNC).next_to(ax.c2p(1.0, np.sin(1.0)), UR, buff=0.1)
        n = np.arange(1, 9)
        xa = 1 / (np.pi / 2 + 2 * np.pi * n)
        xb = 1 / (3 * np.pi / 2 + 2 * np.pi * n)
        da = VGroup(*[Dot(ax.c2p(x, 1), radius=0.05, color=C.CONNECTED_SET) for x in xa])
        dbb = VGroup(*[Dot(ax.c2p(x, -1), radius=0.05, color=C.PATHOLOGY) for x in xb])
        la = MathTex(r"p_n = \tfrac{1}{\pi/2 + 2\pi n}:\ f(p_n) = 1", font_size=26, color=C.CONNECTED_SET)
        lb = MathTex(r"p_n' = \tfrac{1}{3\pi/2 + 2\pi n}:\ f(p_n') = -1", font_size=26, color=C.PATHOLOGY)
        VGroup(la, lb).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.0, 1.0, 0])
        verdict = label(r"two sequences $\to 0$ with different limits of $f$: \ no limit at $0$, however $f(0)$ is "
                        r"defined", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='t'/> Limits and continuity can also be tested with sequences: f is continuous at p "
            "exactly when f carries every sequence converging to p to a sequence converging to f of p. This is handy for "
            "showing a limit fails. <bookmark mark='a'/> Sine of one over x oscillates faster and faster near zero. "
            "<bookmark mark='b'/> Along one sequence approaching zero it's always one; <bookmark mark='c'/> along "
            "another, always minus one. <bookmark mark='d'/> So it has no limit at zero, and no choice of a value at "
            "zero makes it continuous there."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(Create(ax), Create(g), Create(g2), FadeIn(lab), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in da], lag_ratio=0.1), FadeIn(la))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in dbb], lag_ratio=0.1), FadeIn(lb))
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preimages(self):
        thm = VGroup(label(r"\textbf{Rudin 4.8} \ $f$ is continuous $\iff$ $f^{-1}(V)$ is open for every open $V$",
                           font_size=30),
                     label(r"(no epsilons: \ only open sets)", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12)
        thm.to_edge(UP, buff=0.35)
        ax = plain_axes([0, 6.3, 1], [-1.6, 1.6, 1], 7.6, 4.4, numbers=False).move_to([-2.2, -0.9, 0])
        f = lambda x: np.sin(1.6 * x) * 0.8 + 0.25 * np.sin(4.1 * x)  # noqa: E731
        graph = ax.plot(f, x_range=[0, 6.3, 0.005], color=C.FUNC, stroke_width=3.5)
        lo, hi = 0.3, 0.75
        vbar = Line(ax.c2p(0, lo), ax.c2p(0, hi), color=C.OPEN_SET, stroke_width=10).shift(LEFT * 0.25)
        vends = VGroup(endpoint(ax.c2p(0, lo) + LEFT * 0.25, False, C.OPEN_SET),
                       endpoint(ax.c2p(0, hi) + LEFT * 0.25, False, C.OPEN_SET))
        vl = MathTex(r"V", font_size=32, color=C.OPEN_SET).next_to(vbar, LEFT, buff=0.15)
        band = Rectangle(width=ax.c2p(6.3, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, hi)[1] - ax.c2p(0, lo)[1],
                         stroke_width=0, fill_color=C.OPEN_SET, fill_opacity=0.12)
        band.move_to((ax.c2p(0, lo) + ax.c2p(6.3, hi)) / 2)
        xs = np.linspace(0, 6.3, 20001)
        ys = f(xs)
        inside = (ys > lo) & (ys < hi)
        runs = []
        start = None
        for i, v in enumerate(inside):
            if v and start is None:
                start = i
            if (not v or i == len(inside) - 1) and start is not None:
                runs.append((xs[start], xs[i]))
                start = None
        y_dom = ax.c2p(0, -1.6)[1] - 0.25
        pre = VGroup()
        for a, b in runs:
            pre.add(VGroup(Line([ax.c2p(a, 0)[0], y_dom, 0], [ax.c2p(b, 0)[0], y_dom, 0], color=C.OPEN_SET,
                                stroke_width=10),
                           endpoint([ax.c2p(a, 0)[0], y_dom, 0], False, C.OPEN_SET),
                           endpoint([ax.c2p(b, 0)[0], y_dom, 0], False, C.OPEN_SET)))
        drops = VGroup(*[DashedLine(ax.c2p(a, f(a)), [ax.c2p(a, 0)[0], y_dom, 0], color=C.OPEN_SET, stroke_width=1.2)
                         for a, b in runs] + [DashedLine(ax.c2p(b, f(b)), [ax.c2p(b, 0)[0], y_dom, 0], color=C.OPEN_SET,
                                                         stroke_width=1.2) for a, b in runs])
        pl = MathTex(r"f^{-1}(V)", font_size=30, color=C.OPEN_SET).next_to([ax.c2p(6.3, 0)[0], y_dom, 0], RIGHT,
                                                                           buff=0.2)
        # a jump: the preimage of a small open interval around the value at the jump is not open
        ax2 = plain_axes([0, 2, 1], [0, 2, 1], 3.6, 3.2, numbers=False).move_to([4.6, -0.6, 0])
        s1 = Line(ax2.c2p(0, 0.6), ax2.c2p(1, 0.6), color=C.FUNC, stroke_width=4)
        s2 = Line(ax2.c2p(1, 1.4), ax2.c2p(2, 1.4), color=C.FUNC, stroke_width=4)
        e1 = endpoint(ax2.c2p(1, 0.6), False, C.FUNC)
        e2 = endpoint(ax2.c2p(1, 1.4), True, C.FUNC)
        v2 = VGroup(Line(ax2.c2p(0, 1.2) + LEFT * 0.2, ax2.c2p(0, 1.6) + LEFT * 0.2, color=C.OPEN_SET, stroke_width=8),
                    endpoint(ax2.c2p(0, 1.2) + LEFT * 0.2, False, C.OPEN_SET),
                    endpoint(ax2.c2p(0, 1.6) + LEFT * 0.2, False, C.OPEN_SET))
        y2 = ax2.c2p(0, 0)[1] - 0.25
        p2 = VGroup(Line([ax2.c2p(1, 0)[0], y2, 0], [ax2.c2p(2, 0)[0], y2, 0], color=C.PATHOLOGY, stroke_width=8),
                    endpoint([ax2.c2p(1, 0)[0], y2, 0], True, C.PATHOLOGY))
        p2l = label(r"contains $1$, but no interval around $1$: \ not open", font_size=22, color=C.PATHOLOGY).next_to(
            p2, DOWN, buff=0.15)
        with self.voiceover(
            "Now the reformulation that changed mathematics. <bookmark mark='t'/> A function is continuous exactly "
            "when the preimage of every open set is open. <bookmark mark='a'/> Pick an open interval V of values. "
            "<bookmark mark='b'/> The points whose values land in V form a union of open intervals: each is open "
            "because, by continuity, a point whose value is strictly inside V has neighbors whose values are too. "
            "<bookmark mark='c'/> A jump breaks this. Here a small open interval around the value at the jump pulls "
            "back to an interval that includes its left endpoint: not open."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            self.play(Create(ax), Create(graph))
            vo.wait_until("a")
            self.play(FadeIn(vbar), FadeIn(vends), FadeIn(vl), FadeIn(band))
            vo.wait_until("b")
            self.play(Create(drops), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p) for p in pre], lag_ratio=0.2), FadeIn(pl))
            vo.wait_until("c")
            self.play(Create(ax2), Create(s1), Create(s2), FadeIn(e1), FadeIn(e2))
            self.play(FadeIn(v2), FadeIn(p2), FadeIn(p2l))
        assert len(runs) >= 3
        why_ = label(r"Topology's definition: \ it survives in spaces with no distance at all (Part 8).", font_size=28,
                     color=C.EPS).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='w'/> This version never mentions a distance, only which sets are open. That's why it "
            "became the definition of continuity in topology, and in Part 8 we'll need it in spaces where no distance "
            "describes the convergence we care about."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        rows = VGroup(
            label(r"\textbf{Rudin 4.7} \ compositions of continuous functions are continuous:", font_size=30),
            MathTex(r"(g \circ f)^{-1}(V) = f^{-1}\big(g^{-1}(V)\big)", font_size=36),
            label(r"\textbf{Rudin 4.9} \ sums, products, and quotients (where defined) too: \ the $\varepsilon/2$ trick "
                  r"again", font_size=30),
            label(r"so every polynomial and every rational function is continuous", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "The open-set version makes some proofs one line. <bookmark mark='a'/> A composition of continuous functions "
            "is continuous, because the preimage under g of f is the preimage under f of the preimage under g. "
            "<bookmark mark='b'/> Sums and products are continuous by the epsilon over two trick, so polynomials and "
            "rational functions are continuous wherever they're defined."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.5)
        self.clear_scene()
