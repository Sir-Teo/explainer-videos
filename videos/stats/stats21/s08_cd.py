from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class CoordinateDescent(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.staircase()
        self.rates()
        self.why_fast()
        self.stuck()

    def card(self):
        card = chapter_card(7, r"Coordinate descent", r"One variable at a time", part=PART)
        with self.voiceover("Chapter seven. Coordinate descent."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\beta_j", r"\leftarrow", r"\arg\min_{b} f(\beta_1, \dots, b, \dots, \beta_p)", font_size=30),
            cmath(r"\text{lasso}", r":", r"\beta_j \leftarrow S_\lambda\big(\tfrac1n X_j' r^{(j)}\big) / \big(\tfrac1n \|X_j\|^2\big)", font_size=30),
            cmath(r"S_\lambda(z)", r"=", r"\operatorname{sign}(z)\,(|z| - \lambda)_+", font_size=30),
            cmath(r"\text{converges}", r":", r"f = \text{smooth convex} + \textstyle\sum_j \text{convex}(\beta_j)", font_size=28),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"cycle through the coordinates"), why(r"$r^{(j)}$: \ the residual without $\beta_j$"),
                why(r"soft thresholding: \ chapter two's KKT"), why(r"Tseng (2001): \ a separable penalty")]
        intro = label('Optimize one coordinate while holding the others fixed', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Coordinate descent is the simplest idea of all: hold every variable fixed but one, "
            "minimize over that one exactly, and cycle. <bookmark mark='b'/> For the lasso each one-variable problem "
            "has a closed form: compute the correlation of predictor j with the residual that leaves it out, "
            "<bookmark mark='c'/> and soft-threshold it: shrink toward zero by lambda, and set it to zero if it "
            "doesn't get past. That's chapter two's KKT condition, solved one coordinate at a time. <bookmark "
            "mark='d'/> Paul Tseng proved in 2001 that this converges under regularity on the objective and "
            "coordinate minimizations, including separable penalties; the standard convex lasso with nonzero design "
            "columns and an attained optimum fits that framework."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def staircase(self):
        d = load("cd")
        b0s, b1s = d["b0s"], d["b1s"]
        A = axes([b0s[0], b0s[-1]], [b1s[0], b1s[-1]], x_length=5.8, y_length=5.8, xlabel=r"$\beta_1$", ylabel=r"$\beta_2$",
                 xticks=[-1, 0, 1, 2], yticks=[-1, 0, 1, 2], center=[-2.8, 0.0, 0], font_size=18)
        ax = A.ax
        fmin = d["fmin"]
        L = Landscape(ax, np.asarray(d["obj"]), (b0s[0], b0s[-1]), (b1s[0], b1s[-1]),
                      [fmin + v for v in (0.02, 0.1, 0.3, 0.7, 1.4, 2.5)], color=LEVEL, stroke_width=1.8)
        axes0 = VGroup(DashedLine(ax.c2p(0, b1s[0]), ax.c2p(0, b1s[-1]), color=GREY_D, stroke_width=1),
                       DashedLine(ax.c2p(b0s[0], 0), ax.c2p(b0s[-1], 0), color=GREY_D, stroke_width=1))
        cd = L.path(d["cd_path"][:14], color=PATH, radius=0.05)
        ist = L.path(d["ista_path"][:25], color=GRAD, radius=0.035, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"two predictors, \ correlation {d['corr']:.2f}; \ $\lambda = {d['lam']}$", font_size=22),
            label(r"contours: \ the lasso objective, \ kinked on the axes", font_size=22, color=LEVEL),
            label(r"gold: \ coordinate descent, \ a staircase", font_size=22, color=PATH),
            label(r"red: \ proximal gradient (chapter eight)", font_size=22, color=GRAD),
            label(rf"the answer: \ $({d['bhat'][0]:.2f}, \ {d['bhat'][1]:.2f})$", font_size=22, color=TRUE),
            label(r"correlated predictors: \ short steps, \ many of them", font_size=20, color=GREY_A),
        ), 4.6, 0.4, [4.3, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's a lasso with just two predictors, correlated point eight four, so its contours are "
            "tilted ellipses with corners where they cross the axes. <bookmark mark='b'/> Coordinate descent, in gold, moves "
            "only horizontally or vertically: minimize over beta one, then beta two, then beta one again. The path is a "
            "staircase down the valley. <bookmark mark='c'/> Because the predictors are correlated, the valley runs diagonally, "
            "and the steps are short; there are many of them. <bookmark mark='d'/> The proximal gradient method of the next "
            "chapter, in red, takes diagonal steps instead. <bookmark mark='e'/> Both reach the same answer: beta two is shrunk "
            "almost to zero, beta one carries the signal."
        ) as vo:
            self.play(FadeIn(A), Create(L.levels), FadeIn(axes0), FadeIn(rows[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cd[1][0]), FadeIn(rows[2]))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(p_)) for s_, p_ in zip(cd[0], cd[1][1:])], lag_ratio=0.5),
                      run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(ist[1][0]), FadeIn(rows[3]))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(p_)) for s_, p_ in zip(ist[0], ist[1][1:])], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.wait(1.0)
        self.clear_scene()

    def rates(self):
        d = load("cdcorr")["runs"]
        rho = [r["corr"] for r in d]
        sw = [np.log10(max(1, r["sweeps"])) for r in d]
        A = axes([0, 1], [0, 3], x_length=8.0, y_length=4.2, xlabel=r"correlation of the two predictors",
                 ylabel=r"sweeps to a gap of $10^{-8}$ (log scale)", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2, 3],
                 center=[-1.6, 0.3, 0], yfmt=lambda v: f"{10 ** v:,.0f}")
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(max(0, a), b), radius=0.08, color=PATH) for a, b in zip(rho, sw)])
        ln = polyline(ax, [max(0, a) for a in rho], sw, PATH, 3)
        labs = VGroup(*[label(str(r["sweeps"]), font_size=18, color=GREY_A).next_to(p, UP, buff=0.1) for r, p in zip(d, pts)])
        rows = fit_rows(VGroup(
            label(r"uncorrelated: \ 5 sweeps", font_size=22, color=HIT),
            label(r"correlation 0.99: \ 635 sweeps", font_size=22, color=RES),
            label(r"each coordinate step undoes part of the other's", font_size=22),
            label(r"roughly $\propto 1/(1 - \rho)$", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How much does correlation slow it down? Here are the sweeps needed to reach a duality gap of ten "
            "to the minus eight, for two predictors with increasing correlation. Uncorrelated, five sweeps. "
            "<bookmark mark='b'/> At a correlation of point nine nine, six hundred and thirty-five. <bookmark mark='c'/> When "
            "predictors move together, each one-coordinate step undoes part of the other's progress, and the staircase steps "
            "shrink. <bookmark mark='d'/> The count grows roughly like one over one minus the correlation."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.2), FadeIn(labs), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def why_fast(self):
        rows = fit_rows(VGroup(
            label(r"each update: \ one inner product, \ $O(n)$", font_size=24, color=PATH),
            label(r"warm starts: \ solve for a decreasing sequence of $\lambda$, \ each from the last", font_size=24, color=NEWT),
            label(r"active sets: \ cycle over the non-zero coefficients until they settle", font_size=24, color=TEAL),
            label(r"screening rules: \ discard predictors that must be zero", font_size=24, color=HIT),
            label(r"Friedman, \ Hastie \& Tibshirani (2010): \ \texttt{glmnet}, \ efficient regularization paths with warm starts and screening", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('Warm starts and sparse updates make regularization paths efficient', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Coordinate descent became the standard way to fit the lasso for reasons that compound. <bookmark "
            "mark='a'/> Each update costs one inner product. <bookmark mark='b'/> Warm starts: you want the whole "
            "path of solutions as lambda decreases, and each solution is an excellent starting point for the next. "
            "<bookmark mark='c'/> Active sets: most coefficients are zero, so cycle over the few that aren't until "
            "they settle, then check the rest. <bookmark mark='d'/> Screening rules can rule out predictors in "
            "advance. <bookmark mark='e'/> Jerome Friedman, Trevor Hastie and Rob Tibshirani built these into glmnet "
            "in 2010, and it computes an entire regularization path in a small multiple of the cost of an individual "
            "fit in favorable problems. The speed depends on sparsity, correlations, tolerances and the lambda path."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stuck(self):
        A = axes([-1.5, 1.5], [-1.5, 1.5], x_length=5.0, y_length=5.0, xlabel=r"$b_1$", ylabel=r"$b_2$", xticks=[-1, 0, 1],
                 yticks=[-1, 0, 1], center=[-3.0, 0.0, 0], font_size=18)
        ax = A.ax
        f = lambda X, Y: (X - 1) ** 2 + (Y - 1) ** 2 + 4 * np.abs(X - Y)  # noqa: E731
        L = Landscape(ax, f, (-1.5, 1.5), (-1.5, 1.5), [0.5, 1.5, 3, 5, 8], color=LEVEL, stroke_width=1.8)
        start = Dot(ax.c2p(-1, -1), radius=0.1, color=RES)
        best = Dot(ax.c2p(1, 1), radius=0.1, color=HIT)
        rows = fit_rows(VGroup(
            label(r"$f = (b_1 - 1)^2 + (b_2 - 1)^2 + 4|b_1 - b_2|$", font_size=24),
            label(r"from $(-1, -1)$: \ moving either coordinate alone goes uphill", font_size=22, color=RES),
            label(r"coordinate descent is stuck; \ the minimum is $(1, 1)$", font_size=22, color=HIT),
            label(r"the penalty couples coordinates: \ not separable", font_size=22, color=OBS),
            label(r"the fused lasso needs another method: \ chapter nine", font_size=22, color=GREY_A),
        ), 5.6, 0.45, [3.6, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But the separability condition matters. Here's a penalty on the difference between two "
            "coefficients, the kind the fused lasso uses, plus a pull toward the point one, one. <bookmark mark='b'/> Start at "
            "minus one, minus one, on the diagonal. Moving either coordinate alone opens a gap between them and pays the "
            "penalty, which outweighs the gain: every single-coordinate move goes uphill. <bookmark mark='c'/> Coordinate "
            "descent is stuck, though the minimum is at one, one, straight along the diagonal. <bookmark mark='d'/> The "
            "penalty couples the coordinates, so the theory doesn't apply. <bookmark mark='e'/> For the fused lasso we need "
            "a method that can split the problem differently: ADMM, in chapter nine."
        ) as vo:
            self.play(FadeIn(A), Create(L.levels), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(start, scale=1.5), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(best, scale=1.5), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()
