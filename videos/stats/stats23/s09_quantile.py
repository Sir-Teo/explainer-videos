from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403

QCOL = [BLUE, TEAL, PATH, GLS_C, RED]


class Quantile(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.fan()
        self.asymptotics()
        self.ses()
        self.qte()
        self.engel()
        self.properties()

    def card(self):
        card = chapter_card(8, r"Quantile regression", r"Not just the mean", lit=(1978,), part=PART)
        with self.voiceover("Chapter eight. Quantile regression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\rho_\tau(r)", r"=", r"r\,(\tau - [r < 0])", font_size=30),
            cmath(r"F^{-1}(\tau)", r"\in", r"\arg\min_q E\,\rho_\tau(Y-q)", font_size=30),
            cmath(r"\hat\beta(\tau)", r"=", r"\arg\min_b \textstyle\sum_i \rho_\tau(y_i - x_i^\top b)", font_size=30),
            cmath(r"\text{computed}", r":", r"\text{a linear program (Part 21)}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"the check loss: \ a tilted absolute value"), why(r"minimizing it finds the $\tau$ quantile"),
                why(r"Koenker \& Bassett (1978)"), why(r"linear-programming solver; \ numerical tolerance")]
        intro = label('Quantile regression minimizes the tilted absolute loss', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Least squares models the mean. Roger Koenker and Gilbert Bassett showed in 1978 how"
            " to model any quantile. The check loss is a tilted absolute value: residuals above the line cost tau "
            "each, below it one minus tau. <bookmark mark='b'/> The minimizers of expected check loss are tau "
            "quantiles; ties can make the minimizer nonunique, just as the mean minimizes squared error and the "
            "median absolute error. <bookmark mark='c'/> So minimize the check loss over regression lines: the tau-th"
            " regression quantile. <bookmark mark='d'/> It's a linear program, Part 21's chapter four, and solved "
            "numerically to a solver tolerance."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fan(self):
        d = load("qreg")
        age, inc = np.asarray(d["age"]), np.asarray(d["inc"])
        A = axes([25, 64], [0, 150], x_length=8.0, y_length=4.6, xlabel=r"age", ylabel=r"income, \ thousands",
                 xticks=[25, 35, 45, 55, 64], yticks=[0, 50, 100, 150], center=[-1.6, 0.3, 0])
        ax = A.ax
        keep = inc < 150
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=GREY_B, fill_opacity=0.5) for a, b in zip(age[keep], inc[keep])])
        lines = VGroup()
        for f, c in zip(d["fits"], QCOL):
            a, b = f["b"]
            lines.add(Line(ax.c2p(25, a + 25 * b), ax.c2p(64, a + 64 * b), color=c, stroke_width=3.5))
        oa, ob = d["ols"]
        ols = DashedLine(ax.c2p(25, oa + 25 * ob), ax.c2p(64, oa + 64 * ob), color=WHITE, stroke_width=2.5)
        fs = d["fits"]
        rows = fit_rows(VGroup(
            label(r"1,000 fitted; 500 shown, \ ages 25--64", font_size=22),
            *[label(rf"$\tau = {f['tau']}$: \ {f['b'][1]:.2f}k a year", font_size=22, color=c) for f, c in zip(fs, QCOL)],
            label(rf"dashed: \ OLS, \ {ob:.2f}k", font_size=22, color=GREY_A),
        ), 3.45, 0.36, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A thousand of the World's working-age adults, income against age. <bookmark mark='b'/> "
            "The tenth percentile rises two hundred and twenty a year. <bookmark mark='c'/> The median rises four hundred "
            "and seventy. <bookmark mark='d'/> The ninetieth percentile rises eleven hundred. The lines fan out: incomes "
            "spread as people age, so a single slope for the mean, point four one, describes nobody in particular. "
            "<bookmark mark='e'/> Least squares, dashed, also sits above the median, pulled up by the long right tail."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(rows[1]), Create(lines[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Create(lines[3]), FadeIn(rows[4]), Create(lines[4]), FadeIn(rows[5]))
            vo.wait_until("e")
            self.play(Create(ols), FadeIn(rows[6]))
        self.clear_scene()

    def asymptotics(self):
        rows = [
            cmath(r"\sqrt n(\hat\beta(\tau) - \beta(\tau))", r"\to", r"N\big(0,\ D^{-1}BD^{-1}\big)", font_size=30),
            cmath(r"B,\ D", r"=", r"E[xx^\top(\tau-[e<0])^2],\ E[f_{Y\mid x}(x^\top\beta\mid x)xx^\top]", font_size=27),
            cmath(r"f", r":", r"\text{density at the line; sparsity } = 1/f", font_size=30),
            cmath(r"\hat D", r"=", r"\dfrac1n\textstyle\sum_i \dfrac{[|e_i| \le h]}{2h} x_i x_i^\top", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"another sandwich"), why(r"the curvature of the expected check loss"),
                why(r"few data near the quantile: \ an imprecise quantile"), why(r"Powell's kernel estimate (1991)")]
        intro = label('Quantile-regression uncertainty uses density bread and score meat', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Under iid sampling, finite score moments and a nonsingular density-weighted design,"
            " a quantile-regression line has an asymptotic sandwich covariance. <bookmark mark='b'/> The bread D "
            "weights each predictor outer product by the conditional density at the fitted line. The meat B is the "
            "expected outer product of the quantile score. If the conditional quantile really is linear, B simplifies"
            " to tau times one minus tau times E x x transpose. <bookmark mark='c'/> Sparsity means the inverse of "
            "the density at the quantile: fewer data near the line means greater uncertainty. <bookmark mark='d'/> "
            "Estimate D by a sample average of kernel-weighted predictor products. Our World example uses empirical "
            "score meat because the conditional quantile need not be exactly linear; pairs resampling provides a "
            "second approximation."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ses(self):
        d = load("qreg")
        hdr = [r"$\tau$", r"\textbf{slope}", r"\textbf{sandwich SE}", r"\textbf{bootstrap SE}"]
        body = [[f"{f['tau']}", f"{f['b'][1]:.3f}", f"{f['se'][1]:.3f}", f"{f['boot_se']:.3f}"] for f in d["fits"]]
        body.append([r"OLS", f"{d['ols'][1]:.3f}", f"{d['ols_se'][1]:.3f} (HC3)", ""])
        t = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_A] + QCOL + [GREY_B])
        t.move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(r"empirical-score sandwich; \ 100 pairs-bootstrap refits", font_size=24, color=HIT),
            label(r"upper-quantile slopes are less precise in this sample", font_size=24, color=RES),
        ), 12.0, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The standard errors, two ways: a kernel-bread, empirical-score sandwich, and one "
            "hundred pairs-bootstrap refits at each quantile. Differences include density estimation, finite-sample "
            "effects and substantial Monte Carlo uncertainty from only a hundred bootstrap draws. <bookmark "
            "mark='b'/> In this example the upper-quantile slope is much less precise. The median slope has a smaller"
            " estimated standard error than the mean slope; this comparison is a feature of these data, not a "
            "universal ranking."
        ) as vo:
            self.add(simulated_tag())
            self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def qte(self):
        rows = [
            cmath(r"y", r"=", r"x^\top\beta + (x^\top\gamma)\varepsilon,\ x^\top\gamma>0", font_size=30),
            cmath(r"Q_\tau(y \mid x)", r"=", r"x^\top\big(\beta + \gamma\, F_\varepsilon^{-1}(\tau)\big)", font_size=30),
            cmath(r"\text{a treatment}", r":", r"\beta_d(\tau):\ \text{conditional quantile contrast}", font_size=30),
            cmath(r"\text{caution}", r":", r"\text{not the effect on the person at that quantile}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"independent mean-zero error; \ positive scale"), why(r"linear quantiles, \ slopes that change with $\tau$: \ the fan"),
                why(r"causal only with identification assumptions"), why(r"people can change rank: \ Part 35")]
        intro = label('Conditional quantile contrasts require assumptions for a causal reading', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> A location–scale model has a linear mean and a positive linear scale, with an "
            "independent mean-zero error of fixed distribution. <bookmark mark='b'/> Its conditional quantiles are "
            "linear; their slopes change with tau in the direction set by the scale coefficients, increasing only "
            "where those coefficients are positive. <bookmark mark='c'/> A treatment coefficient describes a "
            "conditional quantile contrast under the fitted model. A causal interpretation additionally needs "
            "identification, such as randomization or adequate confounding control. It is not automatically the "
            "marginal quantile treatment effect. <bookmark mark='d'/> Nor is a contrast between distributional "
            "quantiles the effect on the person who started at that rank: treatment can reshuffle ranks. Part 35 "
            "makes this distinction precise."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def engel(self):
        rows = [
            cmath(r"\text{Engel (1857)}", r":", r"\text{235 Belgian households: \ food against income}", font_size=28),
            cmath(r"\text{slopes}", r":", r"0.40 \ (\tau = 0.1) \ \text{to} \ 0.69 \ (\tau = 0.9)", font_size=30),
            cmath(r"\text{Engel's law}", r":", r"\text{the food share falls as income rises}", font_size=30),
            cmath(r"\text{the fan}", r":", r"\text{a wider conditional range of food spending}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"Part 21's linear programs"), why(r"positive fitted intercepts"), why(r"$a>0$: \ $a/x+b$ decreases with $x$"),
                why(r"heteroskedasticity, \ read as substance")]
        intro = label('Positive fitted intercepts imply declining food shares', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Part 21 fitted quantile regressions to Ernst Engel's 1857 survey of two hundred and"
            " thirty-five Belgian households. <bookmark mark='b'/> The slopes of food spending on income ran from "
            "point four at the tenth percentile to point six nine at the ninetieth. <bookmark mark='c'/> The fitted "
            "intercepts are positive. A fitted food-spending quantile a plus b times income therefore has food share "
            "a over income plus b, which falls with income. A slope below one alone would not establish this. "
            "<bookmark mark='d'/> The fitted fan shows a wider conditional range of food spending at higher incomes, "
            "not which foods households eat. What chapter four treated as nuisance heteroskedasticity, quantile "
            "regression reads as substance."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def properties(self):
        rows = [
            cmath(r"\text{equivariance}", r":", r"Q_\tau(g(y) \mid x) = g(Q_\tau(y \mid x)), \ g \text{ increasing}", font_size=28),
            cmath(r"\text{robust}", r":", r"\text{bounded residual score; leverage still matters}", font_size=30),
            cmath(r"\text{crossing}", r":", r"\text{fitted quantiles can cross: \ rearrange}", font_size=30),
            cmath(r"\text{uses}", r":", r"\text{growth charts, \ value at risk, \ inequality}", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"population equivariance; \ parametric refits can differ"), why(r"only the sign of a residual matters"),
                why(r"Chernozhukov, \ Fern\'andez-Val \& Galichon (2010)"), why(r"the whole distribution, \ not one number")]
        intro = label('Population quantile properties do not all transfer to parametric refits', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Population quantiles commute with strictly increasing transformations. "
            "Exponentiating a correctly specified log-quantile model gives an income quantile, but refitting a "
            "parametric linear model after a nonlinear transformation need not give the same fitted values. <bookmark"
            " mark='b'/> The vertical residual score is bounded and depends on its sign; moving an inactive point "
            "without changing the relevant signs can leave the optimum unchanged. High-leverage predictors can still "
            "be influential. <bookmark mark='c'/> Lines fitted separately can cross where data are thin, which is "
            "impossible for true quantiles; sorting the fitted values fixes that. <bookmark mark='d'/> Quantile "
            "regression is how paediatric growth charts, financial value at risk and studies of inequality are built:"
            " they all care about the whole distribution, not its centre."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
