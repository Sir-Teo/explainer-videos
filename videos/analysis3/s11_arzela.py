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
        d = load("arzela")
        x, sample, pts = d["x"], d["sample"], d["pts"]
        thm = VGroup(label(r"\textbf{Rudin 7.25} \ $K$ compact, \ $f_n \in C(K)$ \ pointwise bounded and equicontinuous",
                           font_size=30),
                     label(r"$\Rightarrow$ \ uniformly bounded, \ and some subsequence converges uniformly", font_size=30,
                           color=C.COMPACT_SET)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        pm = ProofMap([r"converge on a countable dense set \ (the diagonal process)",
                       r"spread it to every point, uniformly \ (equicontinuity + compactness)"], font_size=22,
                      width=5.6, buff=0.4).next_to(thm, DOWN, buff=0.3)
        ax = plain_axes([0, 1, 0.25], [-0.4, 0.4, 0.2], 9.0, 3.2).move_to([0, -1.05, 0])
        assert np.abs(sample).max() < 0.4
        fan = VGroup(*[polyline(ax, x, s_, color=GREY_C, stroke_width=1.2).set_stroke(opacity=0.55) for s_ in sample])
        fl = label(r"a bounded, equicontinuous family: \ random functions with $|f| \le 1$, \ $|f'| \le 1$",
                   font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        # the dense set: the dyadic points of K = [0, 1] (with its ends), on the x-axis
        kpts = np.r_[0.0, np.sort(pts.astype(float)), 1.0]
        dense = VGroup(*[Dot(ax.c2p(float(p_), 0), radius=0.06, color=C.EPS).set_z_index(2) for p_ in kpts])
        dl = label(r"yellow: \ the dyadic points $0, \tfrac18, \tfrac14, \dots, 1$ \ (dense in $K$)", font_size=22,
                   color=C.EPS).next_to(fl, DOWN, buff=0.1)
        delta = 0.07
        # finitely many delta-neighbourhoods (p - delta, p + delta) cover K: the gaps between centres are < 2 delta
        assert kpts[0] - delta < 0 and kpts[-1] + delta > 1 and np.diff(kpts).max() < 2 * delta
        boxes = VGroup(*[Rectangle(width=ax.c2p(2 * delta, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 0.8)[1] - ax.c2p(0, 0)[1],
                                   stroke_width=0, fill_color=C.DELTA, fill_opacity=0.12).move_to(ax.c2p(float(p_), 0))
                         for p_ in kpts])
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: if a sequence of continuous functions on a compact set is pointwise "
            "bounded and equicontinuous, then it has a uniformly convergent subsequence. Here's such a family: random "
            "functions, all bounded by one, with slopes at most one. <bookmark mark='b'/> The proof has two steps. "
            "First, get convergence at countably many points, densely spread, by Cantor's diagonal trick. "
            "<bookmark mark='c'/> Then use equicontinuity, and compactness, to spread that convergence to every point, "
            "uniformly."
        ) as vo:
            self.play(FadeIn(thm[0]), Create(ax), LaggedStart(*[Create(f_) for f_ in fan], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(thm[1]), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(pm), *pm.light(0))
            self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dense], lag_ratio=0.2), FadeIn(dl), run_time=2.0)
            vo.wait_until("c")
            self.play(*pm.light(1))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.1), run_time=1.5)
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
        sv, blo, bw = d["surv_vals"], d["bin_lo"], d["bin_w"]
        assert np.all(np.diff(bw) < 0) and np.array_equal(surv[:rows_n, :cols_n], surv[:rows_n, :cols_n])
        x_s, L_s, half = 3.25, 2.4, 0.15  # each strip shows a window of values 0.3 wide around its row's bin
        plabs = VGroup()
        for i in range(rows_n):
            y_ = grid[i][0].get_y()
            c_ = blo[i] + bw[i] / 2
            V_ = lambda v, c_=c_: x_s + L_s * (v - (c_ - half)) / (2 * half)  # noqa: E731
            assert np.all(np.abs(sv[i] - c_) <= bw[i] / 2 + 1e-12)
            strip = VGroup(MathTex(rf"\text{{at }} p_{{{i + 1}}}", font_size=22, color=GREY_B).next_to(
                               [x_s, y_, 0], LEFT, buff=0.15),
                           Line([x_s, y_, 0], [x_s + L_s, y_, 0], color=GREY_D, stroke_width=1.5),
                           Rectangle(width=L_s * bw[i] / (2 * half), height=0.3, stroke_width=1.5, stroke_color=C.EPS,
                                     fill_color=C.EPS, fill_opacity=0.25).move_to([V_(c_), y_, 0]),
                           VGroup(*[Dot([V_(v), y_, 0], radius=0.035, color=WHITE) for v in sv[i]]))
            plabs.add(strip)
        strip_h = label(r"their values there: \ a bin $\tfrac14 (0.55)^{k}$ wide", font_size=22, color=GREY_B)
        strip_h.next_to(plabs[0][1], UP, buff=0.3)
        diag = VGroup(*[SurroundingRectangle(grid[i][i], color=C.EPS, buff=0.06, stroke_width=2.5) for i in range(rows_n)])
        side = VGroup(label(r"each row is a subsequence of the row above,", font_size=24),
                      label(r"chosen so the values at one more point converge", font_size=24),
                      label(r"the diagonal is a subsequence of every row", font_size=24, color=C.EPS),
                      label(r"(Rudin 7.23; \ Cantor's diagonal, put to work)", font_size=22, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        foot = label(r"actual indices, from 400{,}000 random 1-Lipschitz functions; \ `converges' = a shrinking bin",
                     font_size=20, color=GREY_B).to_corner(UR, buff=0.4)
        dl_ = NumberLine(x_range=[0, 1, 0.25], length=8.0, include_numbers=False).move_to([-1.0, 2.5, 0])
        dl_n = VGroup(*[MathTex(t_, font_size=22, color=GREY_B).next_to(dl_.n2p(v_), DOWN, buff=0.15)
                        for v_, t_ in ((0, "0"), (0.25, r"\tfrac14"), (0.5, r"\tfrac12"), (0.75, r"\tfrac34"), (1, "1"))])
        dyad = VGroup(*[VGroup(Dot(dl_.n2p(float(p_)), radius=0.07, color=C.EPS),
                               MathTex(rf"p_{{{k + 1}}}", font_size=22, color=C.EPS).next_to(dl_.n2p(float(p_)), UP,
                                                                                         buff=0.12))
                        for k, p_ in enumerate(pts)])
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
            self.play(FadeIn(foot), Create(dl_), FadeIn(dl_n))
            self.play(LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dyad], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(strip_h), run_time=0.4)
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
        pts = np.arange(0, 9) / 8
        delta = 0.09
        dots = VGroup(*[Dot([X(p), y0, 0], radius=0.06, color=C.EPS) for p in pts])
        # the neighbourhoods (p - delta, p + delta): 2 delta wide; neighbours overlap, so together they cover K = [0, 1]
        assert np.diff(pts).max() < 2 * delta and pts[0] - delta < 0 < 1 < pts[-1] + delta
        nb = VGroup(*[Rectangle(width=X(2 * delta) - X(0), height=0.5, stroke_width=1, stroke_color=C.DELTA,
                                stroke_opacity=0.6, fill_color=C.DELTA, fill_opacity=0.2).move_to([X(p), y0, 0])
                      for p in pts])
        xq = 0.43
        jp = int(np.argmin(np.abs(pts - xq)))
        assert pts[jp] == 0.375 and abs(xq - pts[jp]) < delta
        xd = Dot([X(xq), y0, 0], radius=0.07, color=WHITE)
        xl = MathTex(r"x", font_size=28).next_to(xd, DOWN, buff=0.12)
        pl = MathTex(r"p", font_size=28, color=C.EPS).next_to(dots[jp], DOWN, buff=0.12)
        rows = [
            MathTex(r"|f_i(x) - f_j(x)|", r"\le", r"|f_i(x) - f_i(p)| + |f_i(p) - f_j(p)| + |f_j(p) - f_j(x)|",
                    font_size=30),
            MathTex(r"|f_i(x) - f_j(x)|", r"<", r"\varepsilon + \varepsilon + \varepsilon", font_size=30),
        ]
        whys = [why(r"through a nearby point $p$ of the dense set"),
                why(r"equicontinuity, \ convergence at the finitely many $p$, \ equicontinuity")]
        step = ladder(self, rows, whys, keep=2, top=-1.0, buff=0.35, x=0.0, edge=6.5)
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
        assert np.abs(sample).max() < 0.33 and np.abs(G).max() < 0.33
        ax = plain_axes([0, 1, 0.25], [-0.33, 0.33, 0.33], 7.6, 4.6).move_to([-2.6, -0.7, 0])
        fan = VGroup(*[polyline(ax, x, s, color=GREY_C, stroke_width=1).set_stroke(opacity=0.5) for s in sample])
        head = VGroup(label(r"The proof, run: \ 400{,}000 random functions with $|f| \le 1$, \ $|f'| \le 1$", font_size=28),
                      label(r"(a sample of 60 in grey)", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.25)
        cols = [interpolate_color(ManimColor(GREY_B), ManimColor(C.APPROX), i / (len(G) - 1)) for i in range(len(G))]
        curves = [polyline(ax, x, G[i], color=cols[i], stroke_width=3) for i in range(len(G))]
        tab = VGroup(MathTex(r"k", r"\text{survivors}", r"\sup_{j > k} \|g_j - g_k\|", font_size=26, color=GREY_A))
        for k in range(len(gaps)):
            tab.add(MathTex(rf"{k + 1}", rf"{int(stages[k]):,}".replace(",", "{,}"), rf"{gaps[k]:.4f}", font_size=26,
                            color=cols[k]))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.6, -0.5, 0])
        regrid(tab, gap=0.35)
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
        ], font_size=22, width=13.2)
        tail = VGroup(label(r"Part 4: \ solutions of $y' = F(x, y)$ exist (Peano) \ $\cdot$ \ Part 7: \ Montel's theorem "
                            r"and the Riemann mapping theorem", font_size=24, color=C.EPS)).to_edge(DOWN, buff=0.4)
        card.next_to(tail, UP, buff=0.35)
        # above each column, the statement drawn.  Left: a bounded sequence in the plane, x_n = (cos n, sin 2.3n), and a
        # subsequence closing in on one of its limit points (Bolzano-Weierstrass)
        nn = np.arange(1, 4001)
        X2 = np.c_[np.cos(nn), np.sin(2.3 * nn)]
        Lp = np.array([0.35, -0.2])
        sub, r_ = [], 0.6
        for n_ in nn:
            dd = np.linalg.norm(X2[n_ - 1] - Lp)
            if dd < r_ and (not sub or n_ > sub[-1]):
                sub.append(int(n_))
                r_ = dd * 0.6
            if len(sub) == 7:
                break
        dsub = np.linalg.norm(X2[np.array(sub) - 1] - Lp, axis=1)
        assert len(sub) == 7 and np.all(np.diff(sub) > 0) and np.all(np.diff(dsub) < 0) and dsub[-1] < 0.01
        pc, ur = np.array([-3.3, 1.85, 0]), 1.15
        P2 = lambda q: pc + ur * np.array([q[0], q[1], 0])  # noqa: E731
        frameL = Square(side_length=2 * ur + 0.25, color=GREY_D, stroke_width=1.5).move_to(pc)
        cloud = VGroup(*[Dot(P2(q), radius=0.022, color=GREY_B) for q in X2[:300]])
        subd = VGroup(*[Dot(P2(X2[n_ - 1]), radius=0.06, color=C.SEQ) for n_ in sub])
        subp = VMobject(color=C.SEQ, stroke_width=2).set_points_as_corners([P2(X2[n_ - 1]) for n_ in sub])
        limd = Dot(P2(Lp), radius=0.07, color=WHITE).set_z_index(2)
        # right: the computed family (grey) and its diagonal subsequence converging uniformly (chapter's run)
        d = load("arzela")
        xa, G, sample = d["x"], d["G"], d["sample"]
        rax = plain_axes([0, 1, 0.5], [-0.33, 0.33, 0.33], 4.6, 2.5, axis_config={"include_ticks": False}).move_to(
            [3.3, 1.85, 0])
        fanR = VGroup(*[polyline(rax, xa, s_, color=GREY_C, stroke_width=1).set_stroke(opacity=0.4) for s_ in sample])
        colsR = [interpolate_color(ManimColor(GREY_B), ManimColor(C.APPROX), i / (len(G) - 1)) for i in range(len(G))]
        diagR = VGroup(*[polyline(rax, xa, G[i], color=colsR[i], stroke_width=2.2) for i in range(len(G))])
        assert frameL.get_top()[1] < 3.6 and rax.get_top()[1] < 3.6 and card.get_top()[1] < frameL.get_bottom()[1] - 0.2
        with self.voiceover(
            "So here's the dictionary entry. <bookmark mark='a'/> In R k, bounded sequences have convergent "
            "subsequences. In the space of continuous functions on a compact set, bounded sequences need one more "
            "property, equicontinuity, and then they too have uniformly convergent subsequences. "
            "<bookmark mark='b'/> This theorem will produce solutions of differential equations in Part 4 and "
            "conformal maps in Part 7."
        ) as vo:
            self.play(FadeIn(card.titles), Create(frameL), FadeIn(cloud), Create(rax), FadeIn(fanR))
            vo.wait_until("a")
            self.play(FadeIn(card.rows[0]), FadeIn(card.arrows[0]), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in subd],
                                                                                lag_ratio=0.2), run_time=1.4)
            self.play(FadeIn(card.rows[1]), FadeIn(card.arrows[1]), Create(subp), FadeIn(limd),
                      LaggedStart(*[Create(c_) for c_ in diagR], lag_ratio=0.15), run_time=1.6)
            for r_, a_ in zip(card.rows[2:], card.arrows[2:]):
                self.play(FadeIn(r_), FadeIn(a_), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(tail))
        self.wait(0.4)
        self.clear_scene()
