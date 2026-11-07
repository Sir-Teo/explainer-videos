from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Computing(VoiceoverScene):
    def construct(self):
        self.card()
        self.cd()
        self.tricks()
        self.lars_idea()
        self.lars_lasso()
        self.path()
        self.order()
        self.ols_end()

    def card(self):
        card = chapter_card(5, r"Computing the path", r"Coordinate descent and least angle regression", lit=(2004,), part=PART)
        with self.voiceover("Chapter five. Computing the lasso."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cd(self):
        rows = [
            cmath(r"r^{(j)}", r"=", r"y - \textstyle\sum_{k \ne j} x_k \beta_k", font_size=32),
            cmath(r"\beta_j", r"\leftarrow", r"S_\lambda\big(\tfrac1n x_j^\top r^{(j)}\big) \big/ \tfrac1n \|x_j\|^2", font_size=30),
            cmath(r"\text{cost}", r":", r"O(n) \text{ per update, \ keeping the residual current}", font_size=30),
            cmath(r"\text{converges}", r":", r"\text{the objective is convex and separable in its penalty}", font_size=28),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"the partial residual"), why(r"one soft threshold"), why(r"cheap"), why(r"Tseng (2001); \ Part 21")]
        with self.voiceover(
            "<bookmark mark='a'/> Part 21's coordinate descent is the method of choice. Hold every coefficient but one fixed "
            "and form the partial residual. <bookmark mark='b'/> The best value of the free coefficient is the soft threshold "
            "of its correlation with that residual: the orthonormal formula, one coordinate at a time. "
            "<bookmark mark='c'/> Each update costs order n if the residual is kept current. <bookmark mark='d'/> And it "
            "converges to the minimum because the non-smooth part of the objective is separable across coordinates, a "
            "theorem of Paul Tseng."
        ) as vo:
            intro=label('Coordinate updates soft-threshold a partial-residual inner product',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tricks(self):
        rows = fit_rows(VGroup(
            label(r"warm starts: \ solve for a decreasing grid of $\lambda$, \ each from the last", font_size=26, color=LASSO),
            label(r"active sets: \ sweep only the nonzero coefficients until they settle", font_size=26, color=LASSO),
            label(r"strong rules: \ discard $j$ if $|x_j^\top r|/n < 2\lambda - \lambda_{\text{prev}}$, \ then check KKT", font_size=26, color=LASSO),
            label(r"glmnet (Friedman, \ Hastie \& Tibshirani 2010): \ fast paths in many examples; no universal timing ratio", font_size=26, color=SPIKE),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three tricks make it fast. Warm starts: solve for a decreasing grid of lambdas, "
            "starting each from the previous solution, which is already close. <bookmark mark='b'/> Active sets: once"
            " the nonzero coefficients settle, sweep only those, and check the rest occasionally. <bookmark "
            "mark='c'/> Strong rules: discard in advance any variable using a strong-rule heuristic based on its "
            "previous residual inner product, then check every discarded variable against KKT and restore any "
            "violations. <bookmark mark='d'/> Together, in Friedman, Hastie and Tibshirani's glmnet, they can make "
            "full paths fast on favorable problems; the cost depends on dimensions, conditioning, sparsity and the "
            "convergence tolerance."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lars_idea(self):
        rows = [
            cmath(r"\text{start}", r":", r"\beta = 0; \ \text{find the } x_j \text{ most correlated with } y", font_size=30),
            cmath(r"\text{move}", r":", r"\text{along } x_j \text{ until another } x_k \text{ is equally correlated with the residual}", font_size=26),
            cmath(r"\text{then}", r":", r"\text{move along the equiangular direction of the active set}", font_size=28),
            cmath(r"u_A", r"=", r"X_A w_A, \ \ X_A^\top u_A = A_A \mathbf 1", font_size=32),
        ]
        rows[3][-1].set_color(LASSO)
        whys = [why(r"forward, \ but cautious"), why(r"a step, \ not a full fit"), why(r"keep all active correlations tied"),
                why(r"equal angles with every active variable")]
        with self.voiceover(
            "<bookmark mark='a'/> The path itself can be computed exactly. Efron, Hastie, Johnstone and Tibshirani's "
            "least angle regression of 2004 starts at zero and finds the variable most correlated with the outcome. "
            "<bookmark mark='b'/> Rather than fitting it fully, it moves the fit along that variable only until a "
            "second variable has just as large a correlation with the residual. <bookmark mark='c'/> Then it moves "
            "along the direction that keeps the two correlations tied, decreasing together. <bookmark mark='d'/> In "
            "general that is the equiangular vector of the active set, making equal angles with the signed, "
            "standardized active columns. When a third variable catches up, it joins, and so on."
        ) as vo:
            intro=label('LARS follows an equiangular direction among signed active columns',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lars_lasso(self):
        rows = [
            cmath(r"\text{KKT}", r":", r"\text{active correlations all equal } \lambda, \ \text{with signs } \mathrm{sign}(\beta_j)", font_size=28),
            cmath(r"\text{LARS}", r":", r"\text{keeps them tied \ and decreasing}", font_size=30),
            cmath(r"\text{lasso modification}", r":", r"\text{if a } \beta_j \text{ hits zero, \ drop it}", font_size=30),
            cmath(r"\text{result}", r":", r"\text{the exact lasso path: \ piecewise linear in } \lambda", font_size=30),
        ]
        rows[3][-1].set_color(LASSO)
        whys = [why(r"chapter four"), why(r"the same structure"), why(r"or the sign condition fails"),
                why(r"knots where the active set changes")]
        with self.voiceover(
            "<bookmark mark='a'/> Why does this have anything to do with the lasso? The lasso's optimality conditions say the "
            "active correlations are all equal to lambda, with the signs of their coefficients. <bookmark mark='b'/> "
            "LARS keeps exactly those correlations tied as they decrease. <bookmark mark='c'/> The only difference: a lasso "
            "coefficient cannot cross zero while its variable stays active, because its sign would contradict its "
            "correlation. So when a coefficient hits zero, drop that variable. <bookmark mark='d'/> With that one "
            "modification LARS traces the entire lasso path exactly. It is piecewise linear in lambda, with a knot wherever "
            "a variable enters or leaves."
        ) as vo:
            intro=label('Dropping a zero-crossing coefficient enforces lasso sign conditions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def path(self):
        d = load("lars")
        s, B, nm = np.asarray(d["s"]), np.asarray(d["coefs"]), d["names"]
        A = axes([0, 1.05], [-850, 820], x_length=6.6, y_length=5.0, xlabel=r"$\|\hat\beta\|_1 / \|\hat\beta_{\text{OLS}}\|_1$",
                 ylabel=r"coefficient (unit-norm columns)", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-800, -400, 0, 400, 800],
                 center=[-2.9, 0.1, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, s, B[:, j], PATHC[j], 2.8) for j in range(10)])
        knots = VGroup(*[DashedLine(ax.c2p(v, -850), ax.c2p(v, 820), color=GREY_D, stroke_width=1) for v in s[1:-1]])
        tags = VGroup(*[label(nm[j], font_size=15, color=PATHC[j]).next_to(ax.c2p(1.0, B[-1, j]), RIGHT, buff=0.06)
                        for j in range(10)])
        # declutter the right-hand labels
        ys = sorted(range(10), key=lambda j: B[-1, j])
        for a, b in zip(ys, ys[1:]):
            if tags[b].get_bottom()[1] < tags[a].get_top()[1] + 0.02:
                tags[b].shift(UP * (tags[a].get_top()[1] + 0.02 - tags[b].get_bottom()[1]))
        rows = fit_rows(VGroup(
            label(r"the lasso path, \ by LARS", font_size=22),
            label(rf"{len(s) - 2} knots, \ dashed", font_size=22, color=GREY_A),
            label(r"piecewise linear between knots", font_size=22, color=LASSO),
        ), 3.2, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The whole lasso path for the diabetes data, with each variable's coefficient against the "
            "fraction of the least-squares coefficients' total size that the budget allows. <bookmark mark='b'/> Eleven "
            "knots, dashed, where a variable enters or leaves. <bookmark mark='c'/> Between knots every coefficient moves in "
            "a straight line. At the far right the budget no longer binds and the lasso is least squares."
        ) as vo:
            self.add(diabetes_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(rows[0]), run_time=3.0)
            self.play(FadeIn(tags))
            vo.wait_until("b")
            self.play(Create(knots), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def order(self):
        d = load("lars")
        nm, acts, s = d["names"], d["actions"], np.asarray(d["s"])
        cells = []
        for k, a in enumerate(acts[:-1]):
            j = int(a[1:])
            verb = r"enters" if a[0] == "+" else r"\textbf{leaves}"
            cells.append([rf"{k + 1}", rf"{nm[j]}", verb, f"{s[k]:.3f}"])
        hdr = [r"\textbf{step}", r"\textbf{variable}", r"", r"\textbf{at $s$}"]
        tb = table_rows([hdr] + cells, font_size=21, col_buff=0.7, row_buff=0.14, colors=[GREY_A] + [None] * len(cells))
        for i, a in enumerate(acts[:-1]):
            tb[i + 1].set_color(PATHC[int(a[1:])])
            if a[0] == "-":
                tb[i + 1].set_color(RES)
        tb.move_to([-2.6, 0.0, 0])
        rows = fit_rows(VGroup(
            label(r"BMI, \ then log triglycerides, \ then blood pressure", font_size=22),
            label(r"HDL enters fourth, \ leaves at $s = 0.81$, \ and returns", font_size=22, color=RES),
            label(r"pure LARS keeps it: \ the only difference between the two paths", font_size=22, color=GREY_A),
            label(r"as in Efron et al.'s Figure 1", font_size=22, color=SPIKE),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The order of events. Body-mass index enters first, then log triglycerides, then blood "
            "pressure: the strongest predictors of progression. <bookmark mark='b'/> HDL cholesterol enters fourth, and then, "
            "late in the path, its coefficient shrinks back to zero and it leaves, before returning one knot later. "
            "<bookmark mark='c'/> Pure least angle regression, without the lasso modification, keeps HDL throughout; that "
            "drop is the only difference between the two paths on these data. <bookmark mark='d'/> All of this reproduces "
            "the first figure of the 2004 paper."
        ) as vo:
            self.add(diabetes_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:4]], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[4:]], lag_ratio=0.2), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ols_end(self):
        rows = [
            cmath(r"\text{LARS}", r":", r"p \text{ steps, \ the cost of one least-squares fit}", font_size=30),
            cmath(r"\text{lasso path}", r":", r"\text{a few more steps for drops}", font_size=30),
            cmath(r"\text{forward stagewise}", r":", r"\text{tiny steps, \ also a LARS variant}", font_size=30),
            cmath(r"\text{in practice}", r":", r"\text{coordinate descent on a grid: \ simpler, \ any GLM}", font_size=28),
        ]
        rows[3][-1].set_color(LASSO)
        whys = [why(r"Efron et al. (2004)"), why(r"here: \ 12 steps for 10 variables"),
                why(r"boosting's cousin, \ Part 34"), why(r"glmnet")]
        with self.voiceover(
            "<bookmark mark='a'/> LARS needs only p steps for its pure form, about the cost of one least-squares fit."
            " <bookmark mark='b'/> The lasso path can take additional drop and re-entry steps, twelve steps for these"
            " ten variables; in general it can be much longer. <bookmark mark='c'/> A third variant, forward "
            "stagewise regression, takes tiny steps along the most correlated variable and turns out to be closely "
            "related to boosting, which Part 34 explains. <bookmark mark='d'/> In practice, coordinate descent on a "
            "grid of lambdas is simpler and extends to logistic, Poisson and Cox models, which LARS does not. Both "
            "give the same answer where both apply."
        ) as vo:
            intro=label('Path complexity depends on design and drop events',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
