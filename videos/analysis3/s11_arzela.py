from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline


class ArzelaAscoli(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.diagonal()
        self.spread()
        self.run()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Arzel\`a--Ascoli: compactness in $C(X)$",
                            r"When does a sequence of functions have a convergent subsequence?", lit=(), part=3)
        with self.voiceover(
            "Chapter ten: the theorem of Arzelà and Ascoli, the compactness theorem for spaces of functions, and one of "
            "the most used theorems in analysis."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def statement(self):
        thm = VGroup(label(r"\textbf{Rudin 7.25} \ $K$ compact, \ $f_n \in C(K)$ \ pointwise bounded and equicontinuous",
                           font_size=30),
                     label(r"$\Rightarrow$ \ uniformly bounded, \ and some subsequence converges uniformly", font_size=30,
                           color=C.COMPACT_SET)).arrange(DOWN, buff=0.15).move_to([0, 1.4, 0])
        pm = VGroup()
        steps = [r"1. converge on a countable dense set \ (the diagonal process)",
                 r"2. equicontinuity spreads it to every point, \ uniformly",
                 r"(compactness of $K$: \ finitely many points suffice)"]
        for i, t in enumerate(steps):
            pm.add(label(t, font_size=26, color=GREY_A if i == 2 else WHITE))
        pm.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(thm, DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: if a sequence of continuous functions on a compact set is pointwise "
            "bounded and equicontinuous, then it has a uniformly convergent subsequence. <bookmark mark='b'/> The "
            "proof has two steps. First, get convergence at countably many points, densely spread, by Cantor's "
            "diagonal trick. <bookmark mark='c'/> Then use equicontinuity, and compactness, to spread that convergence "
            "to every point, uniformly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(pm[0]))
            vo.wait_until("c")
            self.play(FadeIn(pm[1]), FadeIn(pm[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagonal(self):
        d = load("arzela")
        surv, pts = d["survivors"], d["pts"]
        rows_n = 6
        cols_n = 7
        cs_x, cs_y = 0.95, 0.62
        o = np.array([-4.6, 1.5, 0])
        grid = VGroup()
        for i in range(rows_n):
            row = VGroup()
            for j in range(cols_n):
                v = int(surv[i][j])
                t = MathTex(rf"f_{{{v}}}", font_size=26, color=C.FUNC if i == j else WHITE)
                t.move_to(o + np.array([j * cs_x, -i * cs_y, 0]))
                row.add(t)
            row.add(MathTex(r"\cdots", font_size=26).move_to(o + np.array([cols_n * cs_x, -i * cs_y, 0])))
            grid.add(row)
        rlabs = VGroup(*[MathTex(rf"S_{{{i + 1}}}:", font_size=26, color=GREY_B).next_to(grid[i][0], LEFT, buff=0.35)
                         for i in range(rows_n)])
        plabs = VGroup(*[MathTex(rf"\text{{converges at }} x = {p:g}" if i < 3 else rf"x = {p:g}", font_size=22,
                                 color=GREY_B).next_to(grid[i][-1], RIGHT, buff=0.3) for i, p in enumerate(pts[:rows_n])])
        diag = VGroup(*[SurroundingRectangle(grid[i][i], color=C.EPS, buff=0.06, stroke_width=2.5) for i in range(rows_n)])
        side = VGroup(label(r"each row is a subsequence of the row above,", font_size=24),
                      label(r"chosen so the values at one more point converge", font_size=24),
                      label(r"the diagonal is a subsequence of every row", font_size=24, color=C.EPS),
                      label(r"(Rudin 7.23; \ Cantor's diagonal, put to work)", font_size=22, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        foot = label(r"actual indices, from 400{,}000 random 1-Lipschitz functions; \ `converges' = a shrinking bin",
                     font_size=20, color=GREY_B).to_corner(UR, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Step one. List the rational points, or any countable dense set: here, the dyadic "
            "points one half, one quarter, three quarters, and so on. <bookmark mark='b'/> The values at the first "
            "point are bounded, so by Bolzano–Weierstrass some subsequence converges there: that's the first row. "
            "From it, extract a further subsequence that converges at the second point as well: the second row. And "
            "so on, each row inside the one above. <bookmark mark='c'/> Now take the diagonal: the first function of "
            "the first row, the second of the second, and so on. From the n-th place on, the diagonal is a "
            "subsequence of the n-th row, so it converges at every one of the points. These are actual indices from "
            "a computed family."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(foot))
            vo.wait_until("b")
            for i in range(rows_n):
                self.play(FadeIn(rlabs[i]), LaggedStart(*[FadeIn(t) for t in grid[i]], lag_ratio=0.05), FadeIn(plabs[i]),
                          run_time=0.7)
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(r_) for r_ in diag], lag_ratio=0.25), FadeIn(side[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spread(self):
        y0 = 0.2
        X = lambda v: -5.5 + 11 * v  # noqa: E731
        line = Line([X(0), y0, 0], [X(1), y0, 0], color=GREY_C, stroke_width=2)
        pts = np.arange(1, 8) / 8
        delta = 0.09
        dots = VGroup(*[Dot([X(p), y0, 0], radius=0.06, color=C.EPS) for p in pts])
        nb = VGroup(*[Rectangle(width=X(delta) - X(0), height=0.5, stroke_width=0, fill_color=C.DELTA,
                                fill_opacity=0.25).move_to([X(p), y0, 0]) for p in np.r_[0, pts, 1]])
        xq = 0.43
        xd = Dot([X(xq), y0, 0], radius=0.07, color=WHITE)
        xl = MathTex(r"x", font_size=28).next_to(xd, DOWN, buff=0.12)
        pl = MathTex(r"p", font_size=28, color=C.EPS).next_to(dots[2], DOWN, buff=0.12)
        rows = [
            MathTex(r"|f_i(x) - f_j(x)|", r"\le", r"|f_i(x) - f_i(p)| + |f_i(p) - f_j(p)| + |f_j(p) - f_j(x)|",
                    font_size=30),
            MathTex(r"|f_i(x) - f_j(x)|", r"<", r"\varepsilon + \varepsilon + \varepsilon", font_size=30),
        ]
        whys = [why(r"through a nearby point $p$ of the dense set"),
                why(r"equicontinuity, \ convergence at the finitely many $p$, \ equicontinuity")]
        step = ladder(self, rows, whys, keep=2, top=-1.0, buff=0.35, x=-0.6)
        head = VGroup(label(r"Step 2: \ from the dense set to every point", font_size=32),
                      label(r"$K$ compact: \ finitely many $\delta$-neighbourhoods of dense points cover it", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Step two. Fix epsilon, and take the delta that equicontinuity provides for the whole "
            "family. <bookmark mark='b'/> Because the set is compact, finitely many of the dense points have delta "
            "neighborhoods covering all of it. <bookmark mark='c'/> Along the diagonal sequence, the values converge at "
            "those finitely many points, so past some index they're Cauchy at all of them at once. "
            "<bookmark mark='d'/> Now any x is within delta of one of them, p, and the triangle inequality through p "
            "gives three epsilons, at every x, for the same indices. The diagonal sequence is uniformly Cauchy, and "
            "since C of K is complete, it converges uniformly."
        ) as vo:
            self.play(FadeIn(head[0]), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(nb), FadeIn(head[1]))
            vo.wait_until("c")
            self.play(Indicate(dots, color=C.EPS, scale_factor=1.3))
            vo.wait_until("d")
            self.play(FadeIn(xd), FadeIn(xl), FadeIn(pl))
            step(0)
            step(1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run(self):
        d = load("arzela")
        x, G, gaps, sample, stages = d["x"], d["G"], d["gaps"], d["sample"], d["stages"]
        ax = plain_axes([0, 1, 0.25], [-0.6, 0.6, 0.3], 7.6, 4.6).move_to([-2.6, -0.7, 0])
        fan = VGroup(*[polyline(ax, x, s, color=GREY_C, stroke_width=1).set_stroke(opacity=0.5) for s in sample])
        head = VGroup(label(r"The proof, run: \ 400{,}000 random functions with $|f| \le 1$, \ $|f'| \le 1$", font_size=28),
                      label(r"(a sample of 60 in grey)", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), i / (len(G) - 1)) for i in range(len(G))]
        curves = [polyline(ax, x, G[i], color=cols[i], stroke_width=3) for i in range(len(G))]
        tab = VGroup(MathTex(r"k", r"\quad \text{survivors}", r"\quad \sup_{j > k} \|g_j - g_k\|", font_size=26,
                             color=GREY_A))
        for k in range(len(gaps)):
            tab.add(MathTex(rf"{k + 1}", rf"\quad {int(stages[k]):,}".replace(",", "{,}"), rf"\quad {gaps[k]:.4f}",
                            font_size=26))
        tab.arrange(DOWN, aligned_edge=RIGHT, buff=0.14).move_to([4.6, -0.5, 0])
        assert np.all(np.diff(gaps) < 0)
        with self.voiceover(
            "<bookmark mark='a'/> Here's the proof run on a computer. Four hundred thousand random functions, each "
            "bounded by one with slope at most one: a uniformly bounded, equicontinuous family. "
            "<bookmark mark='b'/> The diagonal process keeps, at each stage, the functions whose value at the next "
            "dyadic point falls in the most crowded small bin, a finite stand-in for converging there. "
            "<bookmark mark='c'/> The diagonal functions close in on each other: the largest gap to any later one "
            "falls from about a fifth to under three hundredths, uniformly in x."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(fan))
            vo.wait_until("a")
            self.play(fan.animate.set_stroke(opacity=0.25))
            vo.wait_until("b")
            self.play(FadeIn(tab[0]))
            for i, cv in enumerate(curves[:-1]):
                self.play(Create(cv), FadeIn(tab[i + 1]), run_time=0.7)
            vo.wait_until("c")
            self.play(Create(curves[-1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        card = dictionary_card(r"in $\R^k$", r"in $C(K)$, \ $K$ compact", [
            (r"bounded sequences", r"bounded \emph{and equicontinuous} sequences"),
            (r"have convergent subsequences", r"have uniformly convergent subsequences"),
            (r"Bolzano--Weierstrass (2.42)", r"Arzel\`a--Ascoli (7.25)"),
            (r"compact $\iff$ closed and bounded", r"compact $\iff$ closed, bounded, equicontinuous"),
        ], font_size=26, width=13.2).shift(UP * 0.4)
        tail = VGroup(label(r"Part 4: \ solutions of $y' = F(x, y)$ exist (Peano) \ $\cdot$ \ Part 7: \ Montel's theorem "
                            r"and the Riemann mapping theorem", font_size=24, color=C.EPS)).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So here's the dictionary entry. <bookmark mark='a'/> In R k, bounded sequences have convergent "
            "subsequences. In the space of continuous functions on a compact set, bounded sequences need one more "
            "property, equicontinuity, and then they too have uniformly convergent subsequences. "
            "<bookmark mark='b'/> This theorem will produce solutions of differential equations in Part 4 and "
            "conformal maps in Part 7."
        ) as vo:
            self.play(FadeIn(card.titles))
            vo.wait_until("a")
            for r_, a_ in zip(card.rows, card.arrows):
                self.play(FadeIn(r_), FadeIn(a_), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(tail))
        self.wait(0.4)
        self.clear_scene()
