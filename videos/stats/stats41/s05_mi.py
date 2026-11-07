from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class MultipleImputation(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.copies()
        self.rules()
        self.derive()
        self.proper()
        self.chained()
        self.air_results()
        self.draws()
        self.how_many()
        self.congenial()
        self.derived()
        self.board()

    def card(self):
        card = chapter_card(4, r"Multiple imputation", r"Fill the holes several times, \ and say how much they differ", lit=(1987,), part=PART)
        with self.voiceover("Chapter four. Multiple imputation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = fit_rows(VGroup(
            label(r"Rubin (1977, \ 1987): \ for the Census Bureau's public files", font_size=26, color=TAUC),
            label(r"the imputer knows the missing-data model; \ the analysts do not", font_size=26),
            label(r"so make $m$ completed data sets, \ each filled with plausible draws", font_size=26, color=IMPC),
            label(r"analyse each the usual way; \ combine by simple rules", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Rubin invented multiple imputation for public data files, such as the Census Bureau's. "
            "<bookmark mark='b'/> The agency that collects the data understands why values are missing; thousands of "
            "analysts who later use the file do not, and use ordinary software. <bookmark mark='c'/> So the agency makes "
            "several completed copies, each with the holes filled by random draws from a model, <bookmark mark='d'/> and "
            "each analyst runs the usual analysis on every copy and combines the results by simple rules."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def copies(self):
        d = load("mech")["grid"]
        G = MaskGrid(24, [r"age", r"sex", r"region", r"BMI", r"income"], cell_w=0.9, cell_h=0.18, center=[-3.6, 0.0, 0])
        miss = np.asarray(d["mar"], bool)
        rows = list(np.flatnonzero(miss))
        side = fit_rows(VGroup(
            label(r"dark: \ income missing \ (MAR)", font_size=22, color=GREY_A),
            label(r"gold: \ filled with a random draw", font_size=22, color=IMPC),
            label(r"$m$ copies: \ the draws differ", font_size=22, color=IMPC),
            label(r"the spread across copies \ is the uncertainty about the holes", font_size=22, color=MIC),
        ), 4.6, 0.42, [3.8, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The survey grid, with incomes missing at random. <bookmark mark='b'/> Fill each hole with "
            "a draw from its predictive distribution given the respondent's age, sex, region and BMI. <bookmark "
            "mark='c'/> Do it again, and again: each copy gets different draws. <bookmark mark='d'/> Where the copies "
            "disagree, we are uncertain about the missing values, and that uncertainty is what single imputation hides."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(G), *G.mark(4, miss), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*G.fill(4, rows), FadeIn(side[1]))
            vo.wait_until("c")
            cp = G.copies(5)
            self.play(FadeIn(cp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def rules(self):
        rows = [
            cmath(r"\bar Q", r"=", r"\tfrac1m \textstyle\sum_\ell \hat Q_\ell", font_size=32),
            cmath(r"W", r"=", r"\tfrac1m \textstyle\sum_\ell U_\ell, \ \ B = \tfrac{1}{m-1} \textstyle\sum_\ell (\hat Q_\ell - \bar Q)^2", font_size=30),
            cmath(r"T", r"=", r"W + \big(1 + \tfrac1m\big) B", font_size=34),
            cmath(r"\nu", r"=", r"(m - 1)\big(1 + \tfrac{W}{(1 + 1/m) B}\big)^2: \ \ \bar Q \pm t_\nu \sqrt T", font_size=30),
        ]
        rows[2][-1].set_color(MIC)
        whys = [why(r"average the estimates"), why(r"within and between"), why(r"Rubin's rules"), why(r"Barnard \& Rubin (1999) refine it")]
        with self.voiceover(
            "<bookmark mark='a'/> Rubin's rules. The combined estimate is the average of the m estimates. <bookmark "
            "mark='b'/> W is the average of their squared standard errors, the within-imputation variance; B is the "
            "variance of the estimates across copies, the between-imputation variance. <bookmark mark='c'/> The total "
            "variance is W plus B inflated by one plus one over m, for using finitely many copies. <bookmark mark='d'/> "
            "Intervals use a t distribution whose degrees of freedom grow as B shrinks relative to W, refined for small "
            "samples by John Barnard and Rubin in 1999."
        ) as vo:
            heading = label('Rubin combines within- and between-imputation uncertainty', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\text{Var}(Q \mid Y_{\text{obs}})", r"=", r"E[\text{Var}(Q \mid Y) \mid Y_{\text{obs}}] + \text{Var}[E(Q \mid Y) \mid Y_{\text{obs}}]", font_size=28),
            cmath(r"\phantom{V}", r"\approx", r"W + B", font_size=32),
            cmath(r"\text{finite } m", r":", r"\text{Var}(\bar Q) \text{ adds } B/m", font_size=30),
            cmath(r"\gamma", r"=", r"(1 + 1/m) B / T: \ \text{large-df relative variance share; finite-df FMI is adjusted}", font_size=30),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"the law of total variance"), why(r"Bayesian reading"), why(r"simulation error"), why(r"how much the holes cost")]
        with self.voiceover(
            "<bookmark mark='a'/> The rules come from the law of total variance, read in a Bayesian way: the "
            "posterior variance of a quantity given the observed data is the average of its variance if the data were"
            " complete, plus the variance, across the plausible completions, of its value. <bookmark mark='b'/> W "
            "estimates the first, B the second. <bookmark mark='c'/> With finitely many copies the average itself has"
            " simulation error, B over m. <bookmark mark='d'/> The share of the total variance due to the holes, is a"
            " large-degrees-of-freedom relative variance share. The reported finite-sample FMI also includes a "
            "degrees-of-freedom correction; it is often far smaller than the fraction of missing values."
        ) as vo:
            heading = label('Finite imputation counts add Monte Carlo variation', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proper(self):
        rows = [
            cmath(r"\text{improper}", r":", r"y^* = x^\top \hat\beta + \hat\sigma\, \varepsilon: \ \text{treats } \hat\beta \text{ as known}", font_size=30),
            cmath(r"\text{proper}", r":", r"\sigma^{*2} \sim \text{RSS}/\chi^2_{n-p}, \ \ \beta^* \sim N(\hat\beta, \sigma^{*2} (X^\top X)^{-1})", font_size=28),
            cmath(r"\phantom{p}", r"\;", r"y^* = x^\top \beta^* + \sigma^* \varepsilon", font_size=30),
            cmath(r"\text{or PMM}", r":", r"\text{borrow an observed value from a donor with a close prediction}", font_size=28),
        ]
        rows[1][-1].set_color(MIC)
        whys = [why(r"too little variance"), why(r"draw the parameters first"), why(r"then the value"), why(r"Little (1988)")]
        with self.voiceover(
            "<bookmark mark='a'/> The draws must be proper. Adding noise to the fitted regression treats its "
            "coefficients as known, and understates B. <bookmark mark='b'/> A proper imputation first draws the "
            "residual variance and the coefficients from their posterior, <bookmark mark='c'/> then draws the missing"
            " value from that regression. <bookmark mark='d'/> Predictive mean matching, popularized by Roderick "
            "Little, instead borrows an observed value from a donor whose prediction is close, so each imputation "
            "stays within the observed donor support. This does not guarantee that a value is plausible for every "
            "covariate pattern or that the joint model is correct: no negative incomes, no fractional children."
        ) as vo:
            heading = label('Proper draws include model-parameter uncertainty', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chained(self):
        rows = fit_rows(VGroup(
            label(r"many variables with holes: \ chained equations \ (van Buuren 2006; \ \texttt{mice})", font_size=26, color=TAUC),
            label(r"impute each in turn from all the others, \ with its own model: \ linear, \ logistic, \ PMM", font_size=26),
            label(r"cycle 10 to 20 times; \ start again for each of the $m$ copies", font_size=26, color=GREY_A),
            label(r"check convergence and compatibility; conditional models need not define one joint law", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With holes in many variables, Stef van Buuren's chained equations are the standard."
            " <bookmark mark='b'/> Impute each variable in turn from all the others, each with a model suited to it, "
            "a linear regression, a logistic, or predictive mean matching. <bookmark mark='c'/> Check mixing and "
            "convergence across chains rather than assuming a fixed number of sweeps suffices. This demonstration "
            "uses ten sweeps, and repeat from scratch for each copy. <bookmark mark='d'/> The conditional models need"
            " not fit together into any joint distribution, and incompatible conditionals can create inconsistent "
            "results or dependence on update order. Diagnostics and sensitivity to the imputation models matter."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def air_results(self):
        d = load("mice")
        rows = [[r"log ozone on:", r"complete cases \ (111 days)", r"MI, \ $m = 20$ \ (153 days)", r"FMI"]]
        for j in (1, 2, 3):
            rows.append([d["names"][j], f"{d['cc']['est'][j]:.4f} ({d['cc']['se'][j]:.4f})", f"{d['mi'][j]['est']:.4f} ({d['mi'][j]['se']:.4f})",
                         f"{d['mi'][j]['fmi']:.2f}"])
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.34, colors=[GREY_A, None, None, None]).move_to([0, 0.8, 0])
        for r in tab[1:]:
            r[1].set_color(CCC)
            r[2].set_color(MIC)
            r[3].set_color(TAUC)
        foot = fit_rows(VGroup(
            label(r"chained equations: \ PMM for ozone and sunlight, \ 10 sweeps, \ 20 copies", font_size=24, color=GREY_A),
            label(r"similar estimates, \ similar SEs: \ the extra 42 days help less than their number suggests", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> New York's ozone again, now regressing its log on sunlight, wind and temperature. "
            "<bookmark mark='b'/> Complete cases use a hundred and eleven days; twenty imputations by chained equations use "
            "all hundred and fifty-three. The estimates and standard errors are similar. <bookmark mark='c'/> The fractions "
            "of missing information, a fifth to a third, say why: the forty-two partly missing days carry less information "
            "than their number suggests, because their missing ozone is exactly the quantity being modelled."
        ) as vo:
            self.add(air_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[1:]])
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def draws(self):
        d = load("mice")
        q = np.asarray(d["temp_draws"], float)
        p = d["mi"][3]
        lo, hi = float(q.min() - 0.004), float(q.max() + 0.004)
        A = axes([0, 21], [lo, hi], x_length=7.4, y_length=4.0, xlabel=r"imputed data set $\ell$", ylabel=r"temperature coefficient",
                 xticks=[1, 5, 10, 15, 20], yticks=[round(lo, 3), round((lo + hi) / 2, 3), round(hi, 3)], xfmt=lambda v: f"{v:g}",
                 yfmt=lambda v: f"{v:.3f}", center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.08, color=IMPC) for i, v in enumerate(q)])
        mean = DashedLine(ax.c2p(0, p["est"]), ax.c2p(21, p["est"]), color=MIC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"gold: \ the 20 estimates $\hat Q_\ell$", font_size=22, color=IMPC),
            label(rf"green: \ $\bar Q = {p['est']:.4f}$", font_size=22, color=MIC),
            label(rf"$\sqrt{{W}} = {np.sqrt(p['W']):.4f}$, \ $\sqrt{{B}} = {np.sqrt(p['B']):.4f}$", font_size=22, color=TAUC),
            label(rf"$\sqrt{{T}} = {p['se']:.4f}$, \ $\nu = {p['df']:.0f}$", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The twenty estimates of the temperature coefficient, one per completed data set. <bookmark "
            "mark='b'/> Their average is the combined estimate. <bookmark mark='c'/> Their scatter, the square root of B, "
            "is about two thirds of the typical within-copy standard error, the square root of W; <bookmark mark='d'/> together they "
            "give the total standard error and the degrees of freedom of the t interval."
        ) as vo:
            self.add(air_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def congenial(self):
        rows = fit_rows(VGroup(
            label(r"congeniality \ (Meng 1994): \ the imputation model must contain the analysis", font_size=26, color=TAUC),
            label(r"impute without the outcome, \ and its relationships are diluted toward zero", font_size=26, color=MNC),
            label(r"analyse an interaction the imputer left out: \ it is attenuated", font_size=26, color=MNC),
            label(r"rule: \ impute with every variable in the analysis, \ the outcome included, \ and more", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One rule matters above all. Xiao-Li Meng called it congeniality: the imputation and"
            " analysis procedures must have compatible assumptions. Including the analysis variables is necessary "
            "practical advice, but not by itself a full congeniality theorem. <bookmark mark='b'/> Impute a covariate"
            " without using the outcome, and the imputed values carry no relation to the outcome, so the estimated "
            "association is diluted toward zero. <bookmark mark='c'/> Analyse an interaction the imputer ignored, and"
            " it is attenuated in the same way. <bookmark mark='d'/> So impute with every variable the analysis will "
            "use, including the outcome, and any others that predict the missing values or the missingness."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("single regression", "multiple imputation")
        text = (
            "<bookmark mark='a'/> The Board, in the same design as chapter two. Single regression imputation, analysed as "
            "if the filled values were real, gives ninety percent intervals that cover only about seventy percent of the "
            "time. <bookmark mark='b'/> Multiple imputation with ten proper copies and Rubin's rules keeps its promise."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])

    def how_many(self):
        rows = [
            cmath(r"\text{efficiency}", r"=", r"(1 + \gamma / m)^{-1}: \ m = 5, \gamma = 0.3 \text{ gives } 94\%", font_size=30),
            cmath(r"\text{but SEs and } p", r":", r"\text{need more copies to be stable}", font_size=30),
            cmath(r"\text{rule of thumb}", r":", r"m\approx1+\gamma^2/(2c^2),\quad c=\operatorname{MCSD}(\widehat{\rm SE})/{\rm SE}", font_size=28),
            cmath(r"\text{computers}", r":", r"\text{are cheap: \ use 20 to 100}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"Rubin's original answer"), why(r"the second moment"), why(r"large-sample SE-stability approximation; von Hippel (2020)"), why(r"no reason to skimp")]
        with self.voiceover(
            "<bookmark mark='a'/> How many copies? Rubin's answer was that a handful suffice: with five copies and "
            "thirty percent missing information, the estimate is ninety-four percent as efficient as with infinitely "
            "many. <bookmark mark='b'/> But standard errors and p-values need more copies to stop wobbling from one "
            "run to the next. <bookmark mark='c'/> A useful large-sample planning approximation is one plus gamma "
            "squared divided by twice the desired squared relative Monte Carlo standard deviation of the reported "
            "standard error, <bookmark mark='d'/> and since computing is cheap, twenty to a hundred copies are common"
            " starting points; high missing information or precise tail probabilities can require more."
        ) as vo:
            heading = label('Choose imputation counts for the required Monte Carlo stability', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derived(self):
        rows = fit_rows(VGroup(
            label(r"derived variables: \ BMI from height and weight, \ a squared term, \ an interaction", font_size=26, color=TAUC),
            label(r"impute, \ then transform: \ consistent, \ but may break the relationships", font_size=26, color=MNC),
            label(r"choose passive, direct-term or substantive-model-compatible imputation to suit the analysis", font_size=26, color=MIC),
            label(r"or impute separately by group, \ so interactions survive", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Derived variables need thought: a body mass index computed from height and weight, "
            "a squared term, an interaction. <bookmark mark='b'/> Imputing the ingredients and then computing the "
            "derived value keeps the arithmetic consistent, but can lose the relationships the analysis cares about. "
            "<bookmark mark='c'/> Treating a derived term as another imputed variable can help for some analyses, but"
            " may break deterministic identities. Passive imputation or substantive-model-compatible chained "
            "equations can preserve the required nonlinear and interaction structure. <bookmark mark='d'/> For "
            "interactions with a group, impute separately within each group, so that each group keeps its own "
            "relationships."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

