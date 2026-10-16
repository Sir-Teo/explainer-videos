from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis3.common import load, plain_axes, rects


def f(x):
    return 1.15 + 0.55 * np.sin(2.3 * x - 0.4) - 0.12 * x


def sup_inf(func, edges, k=400):
    M, m = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        t = np.linspace(a, b, k)
        v = func(t)
        M.append(v.max())
        m.append(v.min())
    return np.array(M), np.array(m)


class UpperLower(VoiceoverScene):
    def construct(self):
        self.card()
        self.sums()
        self.refine()
        self.criterion()
        self.square()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Upper and lower sums", r"What is the area under a graph?", lit=(1854,), part=3)
        with self.voiceover(
            "Chapter one. Riemann defined the integral in 1854, in the same paper where he studied Fourier series. We'll "
            "use the version that Darboux streamlined, which is the one Rudin uses: trap the area between two sums."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def _axes(self):
        ax = plain_axes([0, 3.2, 1], [0, 2.0, 0.5], 8.0, 4.0).move_to([-2.4, -1.1, 0])
        g = ax.plot(f, x_range=[0, 3.0, 0.01], color=C.FUNC, stroke_width=4)
        g.set_z_index(3)  # the graph stays on top of the translucent rectangles
        return ax, g

    def sums(self):
        ax, g = self._axes()
        self.ax, self.g = ax, g
        a, b = 0.0, 3.0
        edges = np.linspace(a, b, 7)
        M, m = sup_inf(f, edges)
        up = rects(ax, edges, M, C.UPPER_SUM, opacity=0.35)
        lo = rects(ax, edges, m, C.LOWER_SUM, opacity=0.6)
        ticks = VGroup(*[VGroup(Line(ax.c2p(e, 0) + DOWN * 0.08, ax.c2p(e, 0) + UP * 0.08, color=WHITE, stroke_width=2),
                                MathTex(rf"x_{{{i}}}", font_size=24).next_to(ax.c2p(e, 0), DOWN, buff=0.15))
                         for i, e in enumerate(edges)])
        dfn = VGroup(
            label(r"a \textbf{partition} $P$: \ $a = x_0 < x_1 < \cdots < x_n = b$", font_size=24),
            MathTex(r"M_i = \sup_{[x_{i-1}, x_i]} f, \qquad m_i = \inf_{[x_{i-1}, x_i]} f", font_size=30),
            MathTex(r"U(P, f) = \sum M_i\, \Delta x_i", font_size=32, color=C.UPPER_SUM),
            MathTex(r"L(P, f) = \sum m_i\, \Delta x_i", font_size=32, color=C.LOWER_SUM),
            label(r"Rudin 6.1", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        dfn[-1].align_to(dfn, RIGHT)
        dfn.move_to([6.5 - dfn.width / 2, 0.2, 0])
        assert dfn.get_left()[0] > 1.5
        area = ax.get_area(g, x_range=[0, 3.0], color=C.FUNC, opacity=0.25)
        head = label(r"Darboux: \ trap the area between two sums", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Take a bounded function on an interval, and ask for the area under its graph. <bookmark mark='p'/> Cut "
            "the interval into pieces with a partition: points x zero up to x n. <bookmark mark='u'/> On each piece, "
            "build a rectangle as tall as the function's supremum there: the red rectangles cover the area, and their "
            "total is the upper sum U. <bookmark mark='l'/> Build them as tall as the infimum instead, and the green "
            "rectangles fit under the graph: their total is the lower sum L. <bookmark mark='s'/> Whatever the area "
            "is, it must lie between L and U."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(g))
            self.play(FadeIn(area))
            vo.wait_until("p")
            self.play(FadeOut(area), FadeIn(ticks), FadeIn(dfn[0]))
            vo.wait_until("u")
            self.play(FadeIn(dfn[1]), LaggedStart(*[GrowFromEdge(r, DOWN) for r in up], lag_ratio=0.15), FadeIn(dfn[2]))
            vo.wait_until("l")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in lo], lag_ratio=0.15), FadeIn(dfn[3]), FadeIn(dfn[4]))
            vo.wait_until("s")
            self.play(Indicate(VGroup(dfn[2], dfn[3]), color=C.EPS, scale_factor=1.03))
        self.up, self.lo, self.ticks, self.dfn, self.edges, self.head = up, lo, ticks, dfn, edges, head

    # ------------------------------------------------------------------
    def refine(self):
        ax = self.ax
        edges = self.edges
        # add one point inside the third piece: its upper rectangle can only drop, its lower one only rise
        new_pt = 1.25
        e2 = np.sort(np.r_[edges, new_pt])
        M2, m2 = sup_inf(f, e2)
        up2 = rects(ax, e2, M2, C.UPPER_SUM, opacity=0.35)
        lo2 = rects(ax, e2, m2, C.LOWER_SUM, opacity=0.6)
        tick = VGroup(Line(ax.c2p(new_pt, 0) + DOWN * 0.08, ax.c2p(new_pt, 2.0), color=C.EPS, stroke_width=2.5),
                      MathTex(r"x^*", font_size=26, color=C.EPS).next_to(ax.c2p(new_pt, 0), DOWN, buff=0.15))
        M1, m1 = sup_inf(f, edges)
        U1, L1 = float(np.sum(M1 * np.diff(edges))), float(np.sum(m1 * np.diff(edges)))
        U2, L2 = float(np.sum(M2 * np.diff(e2))), float(np.sum(m2 * np.diff(e2)))
        assert U2 <= U1 + 1e-12 and L2 >= L1 - 1e-12 and U2 < U1
        rows = [
            MathTex(r"P \subset P^*", r"\Rightarrow", r"L(P) \le L(P^*) \le U(P^*) \le U(P)", font_size=32),
            MathTex(r"\underline{\int} f = \sup_P L(P, f)", r"\le", r"\inf_P U(P, f) = \overline{\int} f", font_size=32),
        ]
        whys = [why(r"refining only helps \ (Rudin 6.4)"), why(r"any lower sum $\le$ any upper sum (6.5)")]
        for r_, w in zip(rows, whys):
            w.next_to(r_, DOWN, buff=0.1)
        block = VGroup(*[VGroup(r_, w) for r_, w in zip(rows, whys)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        block.move_to([0, 2.55, 0])
        vals = VGroup(MathTex(rf"U = {U1:.3f} \to {U2:.3f}", font_size=32, color=C.UPPER_SUM),
                      MathTex(rf"L = {L1:.3f} \to {L2:.3f}", font_size=32, color=C.LOWER_SUM)).arrange(DOWN, buff=0.15)
        vals.move_to([4.4, 0.2, 0])
        eq = VGroup(label(r"$f$ is \textbf{integrable}", font_size=28, color=C.EPS),
                    label(r"when the two agree (Rudin 6.1)", font_size=28, color=C.EPS)).arrange(DOWN, buff=0.1)
        eq.next_to(vals, DOWN, buff=0.6)
        with self.voiceover(
            "Now refine the partition by adding a point. <bookmark mark='a'/> On the piece that gets cut, the supremum "
            "over each half is at most the supremum over the whole, so the upper sum can only go down, and by the "
            "same argument the lower sum can only go up. <bookmark mark='b'/> Comparing any two partitions through "
            "their common refinement shows that every lower sum is at most every upper sum. "
            "<bookmark mark='c'/> So the best lower bound, the supremum of all lower sums, sits below the best upper "
            "bound, the infimum of all upper sums. These are the lower and upper integrals, and when they're equal the "
            "function is called integrable, and that common value is its integral."
        ) as vo:
            self.play(FadeOut(self.dfn), FadeOut(self.head), FadeIn(block[0][0]))
            vo.wait_until("a")
            self.play(Create(tick))
            self.play(ReplacementTransform(self.up, up2), ReplacementTransform(self.lo, lo2), FadeIn(vals), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(block[0][1]))
            vo.wait_until("c")
            self.play(FadeIn(block[1]))
            self.play(FadeIn(eq))
        self.wait(0.3)
        self.up, self.lo = up2, lo2
        self.play(FadeOut(VGroup(block, vals, eq, tick)))

    # ------------------------------------------------------------------
    def criterion(self):
        ax = self.ax
        crit = VGroup(label(r"\textbf{Rudin 6.6} \ $f$ is integrable $\iff$ for every $\varepsilon > 0$ some $P$ has",
                            font_size=28),
                      MathTex(r"U(P, f) - L(P, f) < \varepsilon", font_size=36, color=C.EPS)).arrange(DOWN, buff=0.15)
        crit.to_edge(UP, buff=0.35)
        ns = (8, 16, 32, 64)
        gaps = []
        gap_groups = []
        for n in ns:
            e = np.linspace(0, 3.0, n + 1)
            M, m = sup_inf(f, e)
            gaps.append(float(np.sum((M - m) * np.diff(e))))
            slivers = VGroup()
            for a, b, hi, lo_ in zip(e[:-1], e[1:], M, m):
                p0, p1 = ax.c2p(a, lo_), ax.c2p(b, hi)
                slivers.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 1e-3), stroke_width=0,
                                      fill_color=C.EPS, fill_opacity=0.75).move_to((p0 + p1) / 2))
            gap_groups.append(slivers)
        assert all(a > b for a, b in zip(gaps, gaps[1:]))
        ratios = [gaps[k] / gaps[k - 1] for k in range(1, len(gaps))]
        assert all(0.45 < r_ < 0.55 for r_ in ratios)  # "doubling the pieces roughly halves the gap"
        tab = VGroup(MathTex(r"n", r"U - L", r"\text{ratio}", font_size=30, color=GREY_A))
        for k, (n, gp) in enumerate(zip(ns, gaps)):
            tab.add(MathTex(rf"{n}", rf"{gp:.4f}", rf"{ratios[k - 1]:.3f}" if k else r"\text{--}", font_size=30))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, -0.6, 0])
        regrid(tab, gap=0.5)
        tab[1][2].set_x(tab[2][2].get_x())
        with self.voiceover(
            "Here's the practical test. <bookmark mark='a'/> The difference between the upper and lower sums is the "
            "total area of these yellow slivers, the gaps between each red rectangle and its green one. "
            "<bookmark mark='b'/> The function is integrable exactly when those gaps can be made as small as you "
            "like: for every epsilon, some partition has U minus L below epsilon. <bookmark mark='c'/> For this "
            "function, doubling the number of pieces roughly halves the total gap."
        ) as vo:
            self.play(FadeIn(crit[0]))
            vo.wait_until("a")
            self.play(FadeOut(self.up), FadeOut(self.lo), FadeOut(self.ticks), FadeIn(gap_groups[0]), FadeIn(tab[0]),
                      FadeIn(tab[1].set_color(C.EPS)))
            vo.wait_until("b")
            self.play(FadeIn(crit[1]))
            vo.wait_until("c")
            for k in range(1, len(ns)):
                self.play(ReplacementTransform(gap_groups[k - 1], gap_groups[k]), tab[k].animate.set_color(WHITE),
                          FadeIn(tab[k + 1].set_color(C.EPS)), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def square(self):
        d = load("riemann")
        ns, U, L = d["ns"], d["U"], d["L"]
        ax = plain_axes([0, 1, 0.25], [0, 1, 0.25], 5.6, 5.0).move_to([-3.4, -0.4, 0])
        ax_n = VGroup(MathTex(r"0", font_size=24, color=GREY_B).next_to(ax.c2p(0, 0), DL, buff=0.08),
                      MathTex(r"1", font_size=24, color=GREY_B).next_to(ax.c2p(1, 0), DOWN, buff=0.12),
                      MathTex(r"1", font_size=24, color=GREY_B).next_to(ax.c2p(0, 1), LEFT, buff=0.12))
        g = ax.plot(lambda t: t * t, x_range=[0, 1, 0.005], color=C.FUNC, stroke_width=4)
        g.set_z_index(3)
        n = 8
        e = np.linspace(0, 1, n + 1)
        up = rects(ax, e, e[1:] ** 2, C.UPPER_SUM, opacity=0.35)
        lo = rects(ax, e, e[:-1] ** 2, C.LOWER_SUM, opacity=0.6)
        slivers = VGroup()
        for a, b in zip(e[:-1], e[1:]):
            p0, p1 = ax.c2p(a, a * a), ax.c2p(b, b * b)
            slivers.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=1, stroke_color=BACKGROUND,
                                  fill_color=C.EPS, fill_opacity=0.85).move_to((p0 + p1) / 2))
        # slide every sliver into one column over the last piece: width 1/n, total height f(1) - f(0) = 1
        targets = []
        for a, b in zip(e[:-1], e[1:]):
            p0, p1 = ax.c2p(1 - 1 / n, a * a), ax.c2p(1, b * b)
            targets.append((p0 + p1) / 2)
        head = MathTex(r"f(x) = x^2 \text{ on } [0, 1], \quad n \text{ equal pieces}", font_size=34).to_edge(UP, buff=0.3)
        tele = VGroup(MathTex(r"U - L = \sum_{i=1}^{n} \big(f(x_i) - f(x_{i-1})\big)\frac1n", font_size=32),
                      MathTex(r"= \frac{f(1) - f(0)}{n} = \frac1n", font_size=32, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.15)
        tele.move_to([3.4, 1.6, 0])
        rows = [(16, 3), (1024, 9), (16384, 13)]
        table = VGroup(MathTex(r"n", r"L", r"U", font_size=28, color=GREY_A))
        for nn, i in rows:
            assert ns[i] == nn and abs(U[i] - L[i] - 1 / nn) < 1e-12
            table.add(MathTex(rf"{fmt_int(nn)}", rf"{L[i]:.5f}", rf"{U[i]:.5f}", font_size=28))
        table[0][1].set_color(C.LOWER_SUM)
        table[0][2].set_color(C.UPPER_SUM)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, -1.2, 0])
        regrid(table, gap=0.5)
        third = MathTex(r"\int_0^1 x^2\,dx = \tfrac13", font_size=36, color=C.FUNC).next_to(table, DOWN, buff=0.35)
        with self.voiceover(
            "For an increasing function the gaps have a beautiful accounting. <bookmark mark='a'/> Take x squared with "
            "n equal pieces. Each yellow sliver is one piece wide and as tall as the function's rise across that piece. "
            "<bookmark mark='b'/> Slide them all over to the last piece and they stack into a single column, one n-th "
            "wide and as tall as the whole rise, from zero to one. So U minus L is exactly one over n. "
            "<bookmark mark='c'/> With sixteen thousand pieces, both sums agree with one third to four decimal "
            "places: the integral is one third."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ax_n), Create(g))
            vo.wait_until("a")
            self.play(FadeIn(up), FadeIn(lo))
            self.play(FadeIn(slivers), up.animate.set_opacity(0.08), lo.animate.set_opacity(0.15))
            vo.wait_until("b")
            self.play(*[s.animate.move_to(t) for s, t in zip(slivers, targets)], run_time=2.0)
            self.play(FadeIn(tele))
            vo.wait_until("c")
            self.play(FadeIn(table))
            self.play(FadeIn(third))
        self.wait(0.4)
        self.clear_scene()
