from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403


def heatmap(M, size=0.11, pos_color=None, neg_color=None) -> VGroup:
    pos_color = pos_color or FIT
    neg_color = neg_color or RES
    vmax = np.abs(M).max()
    g = VGroup()
    n, m = M.shape
    for i in range(n):
        for j in range(m):
            v = M[i, j] / vmax
            col = interpolate_color(ManimColor("#121722"), ManimColor(pos_color if v >= 0 else neg_color), min(1, abs(v) ** 0.6))
            g.add(Square(side_length=size, stroke_width=0, fill_color=col, fill_opacity=1)
                  .move_to([j * size, -i * size, 0]))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.fit()
        self.matrix()
        self.eigen()
        self.dof()
        self.objectives()

    def fit(self):
        d = load("hat")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        b0, b1 = d["beta"]
        A = axes([150, 190], [140, 200], x_length=6.6, y_length=4.6, xlabel=r"mid-parent height (cm)",
                 ylabel=r"child's height (cm)", xticks=[150, 160, 170, 180, 190], yticks=[150, 170, 190],
                 center=[-3.0, -0.4, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=DATA) for a, b in zip(x, y)])
        line = Line(ax.c2p(150, b0 + b1 * 150), ax.c2p(190, b0 + b1 * 190), color=FIT, stroke_width=3)
        fits = VGroup(*[Dot(ax.c2p(a, b0 + b1 * a), radius=0.04, color=FIT) for a in x])
        f = MathTex(r"\hat{\mathbf y}", r"=", r"X\hat\beta", r"=", r"X (X^\top X)^{-1} X^\top", r"\mathbf y", font_size=40)
        f.move_to([3.6, 1.6, 0])
        f[0].set_color(FIT)
        f[5].set_color(DATA)
        hb = Brace(f[4], DOWN, color=S.ACCENT)
        hl = MathTex(r"H", r"\text{, the hat matrix}", font_size=34, color=S.ACCENT).next_to(hb, DOWN, buff=0.12)
        why_ = label(r"it puts the hat on $\mathbf y$", font_size=24, color=GREY_B).next_to(hl, DOWN, buff=0.2)
        tag = simulated_tag(r"simulated: 40 of the World's families")
        with self.voiceover(
            "Here's a matrix you'll meet in almost every part of this series. <bookmark mark='a'/> Forty of the "
            "World's families: the parents' average height across, the child's height up. <bookmark mark='b'/> "
            "Fit a straight line by least squares, which Part 12 will derive; each child gets a fitted value on the "
            "line. <bookmark mark='c'/> Stack the forty heights into a vector y. The fitted values are X times the "
            "fitted coefficients, and the coefficients turn out to be X transpose X inverse, X transpose, y. "
            "<bookmark mark='d'/> So the fitted values are one matrix times the data. Statisticians call it the hat "
            "matrix, H, because it puts the hat on y."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A), LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(ft) for ft in fits], lag_ratio=0.02))
            vo.wait_until("c")
            self.play(Write(f))
            vo.wait_until("d")
            self.play(GrowFromCenter(hb), FadeIn(hl), FadeIn(why_))
        self.clear_scene()

    def matrix(self):
        d = load("hat")
        x = np.asarray(d["x"])
        order = np.argsort(x)
        X = np.column_stack([np.ones(len(x)), x[order]])
        H = X @ np.linalg.solve(X.T @ X, X.T)
        hm = heatmap(H, size=0.13).move_to([-3.2, -0.2, 0])
        cap = label(r"$H$: \ $40 \times 40$, \ families sorted by mid-parent height", font_size=24, color=GREY_A)
        cap.next_to(hm, UP, buff=0.25)
        props = VGroup(
            MathTex(r"H^\top = H", font_size=36),
            MathTex(r"H^2 = H", font_size=36),
            label(r"symmetric, \ and \emph{idempotent}: \ apply it twice, nothing changes", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, 1.0, 0])
        lev = label(r"blue: positive weights; \ red: negative; \ each fitted value borrows from every child", font_size=22,
                    color=GREY_B).move_to([3.4, -1.4, 0])
        if lev.width > 6.0:
            lev.width = 6.0
        with self.voiceover(
            "Here's H for the forty families, sorted by the parents' height. <bookmark mark='a'/> Each row says how "
            "a fitted value is built from all forty observed heights: families with similar parents get positive "
            "weight, the far end negative. <bookmark mark='b'/> H has two properties that define it. It's "
            "symmetric, and it's idempotent: H times H is H. Fitting the fitted values changes nothing, because "
            "they're already on the line."
        ) as vo:
            self.play(FadeIn(hm, lag_ratio=0.0005), FadeIn(cap), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(lev))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in props], lag_ratio=0.4))
        self.clear_scene()

    def eigen(self):
        d = load("hat")
        ev = np.asarray(d["eig"])
        A = axes([0, 41], [0, 1.15], x_length=8.4, y_length=3.6, xlabel=r"the 40 eigenvalues of $H$, largest first",
                 yticks=[0, 1], center=[-1.4, -0.6, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.14, height=max(ax.c2p(0, max(v, 0.004))[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=EIG if v > 0.5 else GREY_C, fill_opacity=0.9).move_to(ax.c2p(i + 1, max(v, 0.004) / 2))
                        for i, v in enumerate(ev)])
        rows = [
            cmath(r"H\mathbf v = \lambda \mathbf v", r"\ \Rightarrow\ ", r"H^2 \mathbf v = \lambda^2 \mathbf v", font_size=34),
            cmath(r"\lambda^2 = \lambda", r"\ \Rightarrow\ ", r"\lambda \in \{0, 1\}", font_size=36),
            cmath(r"\operatorname{tr} H", r"=", r"\#\{\lambda = 1\}", r"=", rf"{d['trace']:.0f}", font_size=36),
        ]
        rows[1][2].set_color(EIG)
        rows[2][4].set_color(EIG)
        whys = [why(r"apply $H$ twice"), why(r"$H^2 = H$"), why(r"the trace sums the eigenvalues")]
        with self.voiceover(
            "And idempotence forces something remarkable. <bookmark mark='a'/> If v is an eigenvector of H, with "
            "eigenvalue lambda, then H squared times v is lambda squared times v. <bookmark mark='b'/> But H "
            "squared is H, so lambda squared equals lambda: every eigenvalue is zero or one. <bookmark mark='c'/> "
            "Here are all forty. Two ones, one for each column of X, and thirty-eight zeros. <bookmark mark='d'/> "
            "The trace, the sum of the eigenvalues, counts the ones: two, the number of parameters."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.42)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("d")
            step(2, transform=False)
        self.clear_scene()

    def dof(self):
        d = load("hat")
        rss = np.asarray(d["rss"])
        n, p = d["n"], d["p"]
        A = axes([10, 70], [0, 0.06], x_length=7.4, y_length=3.8, xlabel=r"$\mathrm{RSS} / \sigma^2$ \ in 2,000 simulated "
                 r"data sets", xticks=[10, 20, 30, 38, 50, 60, 70], center=[-2.2, -0.8, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        ed = np.linspace(10, 70, 46)
        h = hist_bars(ax, ed, np.histogram(rss, ed)[0] / (len(rss) * np.diff(ed)), color=SIM)
        ml = Line(ax.c2p(n - p, 0), ax.c2p(n - p, 0.06), color=EXACT, stroke_width=3)
        rows = VGroup(
            MathTex(r"\mathbf r = (I - H)\mathbf y", r",\quad \operatorname{tr}(I - H) = n - p = 38", font_size=30),
            MathTex(rf"E\,\mathrm{{RSS}} = (n - p)\,\sigma^2", rf"\quad \text{{simulated: }} {d['rss_mean']:.2f}\,\sigma^2",
                    font_size=30),
            MathTex(rf"\frac{{\mathrm{{RSS}}}}{{n}} \text{{ averages }} {d['rss_naive']:.3f}\,\sigma^2", r",\quad",
                    rf"\frac{{\mathrm{{RSS}}}}{{n - p}} \text{{ averages }} {d['rss_unbiased']:.3f}\,\sigma^2", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.45)
        rows[0][0].set_color(RES)
        rows[1][1].set_color(SIM)
        rows[2][2].set_color(EXACT)
        take = label(r"degrees of freedom $=$ the number of eigenvalues equal to $1$", font_size=28, color=S.ACCENT)
        take.move_to([3.6, -1.6, 0])
        if take.width > 6.2:
            take.width = 6.2
        with self.voiceover(
            "Why should anyone care? <bookmark mark='a'/> The residuals are I minus H, times y, and I minus H is "
            "also a projection, with thirty-eight eigenvalues equal to one. <bookmark mark='b'/> Simulate two "
            "thousand data sets with the same parents and noise of known variance sigma squared, and measure the "
            f"residual sum of squares each time. It averages {d['rss_mean']:.1f} sigma squared: n minus p, not n. "
            "<bookmark mark='c'/> So dividing the residual sum of squares by n underestimates the noise; dividing "
            "by n minus p is exactly right. <bookmark mark='d'/> That's what degrees of freedom are: the number of "
            "eigenvalues equal to one in the projection the residuals live in. One fact about one matrix, and out "
            "of it come the n minus one of the sample variance, the chi-squared distributions, regression and the "
            "analysis of variance."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(h), Create(ml), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 4", font_size=34, color=GREY_B), label(r"Matrices for Statistics", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"data as vectors; \ projections, Gram--Schmidt and QR; \ the trace and its tricks",
            r"the spectral theorem, quadratic forms and ellipses; \ positive semidefinite matrices and Cholesky",
            r"the singular value decomposition and low-rank approximation; \ the pseudoinverse",
            r"block matrices, Schur complements and Woodbury; \ Kronecker products and vec",
            r"matrix calculus and the Gaussian MLE; \ quadratic forms that are $\chi^2$; \ conditioning and floating point",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ a first course in linear algebra, \ or \emph{AI, Built} Part 3").to_corner(DL, buff=0.3)
        built = label(r"Built in this part: \ a projection lab, \ $\mathbb R^3$ you can turn", font_size=28, color=S.ACCENT)
        built.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part is the toolkit. <bookmark mark='a'/> Part four: matrices for statistics. <bookmark mark='b'/> "
            "Data as vectors, and projections; the trace; the spectral theorem and the ellipses of quadratic "
            "forms; positive semidefinite matrices; the singular value decomposition; generalized inverses; block "
            "matrices and the Woodbury identity; Kronecker products; matrix calculus; the quadratic forms that are "
            "chi-squared; and, at the end, what floating-point arithmetic does to all of it. "
            "<bookmark mark='c'/> Along the way we'll use a projection lab: three-dimensional space you can turn, "
            "where every projection can be seen. Most of the formulas of the next sixty parts are written in this "
            "language, from the standard errors of regression to the eigenvalues of random matrices, so it's worth "
            "learning to read it fluently. We'll prove what we use, check every identity numerically, and keep the "
            "statistics in view: every chapter ends with what the tool is for."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("c")
            self.play(obj.animate.shift(UP * 0.4), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
