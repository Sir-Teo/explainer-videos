from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Sins(VoiceoverScene):
    def construct(self):
        self.card()
        self.complete_cases()
        self.cc_numbers()
        self.when_ok()
        self.indicator()
        self.available()
        self.mean_imputation()
        self.outcome_vs_covariate()
        self.locf_story()
        self.locf_plot()
        self.locf_table()
        self.board()

    def card(self):
        card = chapter_card(2, r"The easy methods' sins", r"Complete cases, \ the mean, \ the last value", lit=(1976,), part=PART)
        with self.voiceover("Chapter two. The easy methods' sins."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def complete_cases(self):
        rows = [
            cmath(r"\text{complete cases}", r":", r"\text{drop every row with a hole}", font_size=32),
            cmath(r"\text{MCAR}", r":", r"\text{unbiased, \ but wasteful}", font_size=32),
            cmath(r"\text{MAR}", r":", r"\text{the complete-case marginal mean can be biased under selection}", font_size=30),
            cmath(r"\text{many variables}", r":", r"\text{independent holes: }10\text{ columns, }5\%\text{ each: }0.95^{10}\approx60\%", font_size=28),
        ]
        rows[2][-1].set_color(CCC)
        whys = [why(r"the software default"), why(r"a smaller random sample"), why(r"a selected sample"), why(r"the holes compound")]
        with self.voiceover(
            "<bookmark mark='a'/> The default in most software is to drop every row with a hole. <bookmark mark='b'/>"
            " If the data are missing completely at random, what remains is a smaller random sample: unbiased, but "
            "wasteful. <bookmark mark='c'/> Under missing at random, the remaining rows are a selected sample, and "
            "the unadjusted marginal mean can be biased when the selection depends on something that predicts the "
            "outcome. <bookmark mark='d'/> And the waste compounds: if the missingness indicators across ten "
            "variables are independent and each variable is five percent missing, only sixty percent of the rows "
            "survive."
        ) as vo:
            heading = label('Complete-case validity depends on the estimand and model', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cc_numbers(self):
        d = load("mech")
        t = d["truth"]
        A = axes([10.3, 10.7], [0, 4], x_length=8.0, y_length=3.8, xlabel=r"mean log income", ylabel=r"",
                 xticks=[10.3, 10.4, 10.5, 10.6, 10.7], yticks=[], xfmt=lambda v: f"{v:.1f}", center=[0.8, 0.2, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(t, 0), ax.c2p(t, 4), color=TRUEC, stroke_width=2.5)
        marks = VGroup()
        for k, (key, name, col) in enumerate((("mcar", r"MCAR", OBSV), ("mar", r"MAR", MIC), ("mnar", r"MNAR", MNC))):
            yv = 3.2 - k * 1.1
            c, se = d[key]["cc"], d[key]["cc_se"]
            marks.add(VGroup(Line(ax.c2p(c - 1.645 * se, yv), ax.c2p(c + 1.645 * se, yv), color=CCC, stroke_width=5),
                             Dot(ax.c2p(c, yv), radius=0.09, color=CCC),
                             label(name + r": \ complete cases", font_size=22, color=col).next_to(ax.c2p(10.3, yv), LEFT, buff=0.2)))
        foot = label(r"gold: \ the true mean of all 2,000; \ red: \ the complete-case mean and 90\% interval", font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World's survey, the true mean log income of all two thousand, in gold. <bookmark "
            "mark='b'/> Under the coin, the complete cases are fine. <bookmark mark='c'/> Under missing at random, they are "
            "a little high, because the young, who earn less, answered less; here age predicts income only weakly, so the "
            "bias is small. <bookmark mark='d'/> Under missing not at random, the complete cases are far too low, and their "
            "interval is confident and wrong."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth), FadeIn(foot))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(marks[k]))
        self.clear_scene()

    def when_ok(self):
        rows = [
            cmath(r"\text{regression of } Y \text{ on } X", r":", r"\text{correct conditional model and selection on }X\text{ only; adequate support}", font_size=28),
            cmath(r"\text{because}", r":", r"f(y \mid x, R = 1) = f(y \mid x)", font_size=32),
            cmath(r"\text{but not}", r":", r"\text{if } R \text{ depends on } Y \text{, even given } X", font_size=30),
            cmath(r"\text{and the mean}", r":", r"E(Y) \text{can differ because the selected }X\text{ mix changes}", font_size=30),
        ]
        rows[1][-1].set_color(MIC)
        whys = [why(r"a useful exception"), why(r"selection on the regressor"), why(r"selection on the outcome"), why(r"chapter 4's Board")]
        with self.voiceover(
            "<bookmark mark='a'/> There is a useful exception. If missingness depends only on the covariates of a "
            "regression, a correctly specified conditional regression can still be estimated from complete cases, "
            "provided selection leaves adequate covariate support, <bookmark mark='b'/> because, given x, being "
            "observed tells us nothing more about y. <bookmark mark='c'/> That fails if missingness depends on the "
            "outcome itself. <bookmark mark='d'/> And even when the regression is fine, the complete-case marginal "
            "mean of y need not be, because the complete cases have the wrong mix of x. The Board tests both."
        ) as vo:
            heading = label('Selection on covariates preserves a correct conditional model', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mean_imputation(self):
        d = load("sins")
        t = d["tab"]
        rows = [[r"log income, \ 30\% MCAR", r"mean", r"SD", r"correlation with age"],
                [r"the truth \ (all 2,000)", f"{t['truth']['mean']:.3f}", f"{t['truth']['sd']:.3f}", f"{t['truth']['corr']:.3f}"],
                [r"complete cases", f"{t['cc']['mean']:.3f}", f"{t['cc']['sd']:.3f}", f"{t['cc']['corr']:.3f}"],
                [r"fill with the mean", f"{t['mean_imp']['mean']:.3f}", f"{t['mean_imp']['sd']:.3f}", f"{t['mean_imp']['corr']:.3f}"],
                [r"fill with a regression prediction", f"{t['reg_imp']['mean']:.3f}", f"{t['reg_imp']['sd']:.3f}", f"{t['reg_imp']['corr']:.3f}"],
                [r"fill with a prediction plus noise", f"{t['proper']['mean']:.3f}", f"{t['proper']['sd']:.3f}", f"{t['proper']['corr']:.3f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_A, TRUEC, CCC, MNC, MNC, MIC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"mean imputation shrinks the spread by a sixth and the correlation toward zero", font_size=24, color=MNC),
            label(r"regression imputation keeps the mean but invents certainty: \ the filled values lie on a line", font_size=24, color=MNC),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Filling the holes is tempting. With incomes missing completely at random, <bookmark"
            " mark='b'/> filling them with the observed mean leaves the mean right, but shrinks the standard "
            "deviation by a sixth and pulls the correlation with age toward zero. <bookmark mark='c'/> Filling with a"
            " regression prediction is better, but every filled value lies exactly on the regression line, so the "
            "spread is too small and the correlation too strong. <bookmark mark='d'/> Stochastic draws under a "
            "suitable model can restore the missing residual variation in distribution; one draw need not reproduce "
            "either statistic exactly. That is the first step toward multiple imputation; the second, chapter four, "
            "is admitting that we do not know the regression either."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]))
        self.clear_scene()

    def locf_story(self):
        rows = fit_rows(VGroup(
            label(r"last observation carried forward: \ a dropout's last value stands for every later visit", font_size=26, color=MNC),
            label(r"assumes the disease stops changing the day the patient leaves", font_size=26),
            label(r"long the default in drug trials; \ criticized by the National Research Council \ (2010)", font_size=26, color=GREY_A),
            label(r"a seeded trial: \ symptoms worsen 2 points a month on placebo, \ 1 on the drug; \ the worse drop out", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In clinical trials the classic shortcut was to carry a dropout's last observation forward "
            "to every later visit. <bookmark mark='b'/> It assumes the disease stops changing on the day the patient leaves. "
            "<bookmark mark='c'/> It was the default for decades, until a 2010 report of the US National Research Council "
            "on missing data in trials argued against it. <bookmark mark='d'/> A seeded trial: symptom scores worsen by two "
            "points a month on placebo and one on the drug, and patients whose symptoms are worse are likelier to drop out."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def locf_plot(self):
        d = load("sins")["locf"]["means"]
        A = axes([0, 5], [18, 32], x_length=7.4, y_length=4.2, xlabel=r"month", ylabel=r"mean symptom score",
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[20, 25, 30], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        t = np.arange(6)
        lines = {}
        for key, sty in (("true", 3.5), ("locf", 2.5)):
            for arm, col in ((0, CCC), (1, MIC)):
                lines[(key, arm)] = polyline(ax, t, np.asarray(d[key][arm], float), col, sty, 1.0 if key == "true" else 0.6)
        dashed = VGroup(*[DashedVMobject(lines[("locf", a)], num_dashes=20) for a in (0, 1)])
        side = fit_rows(VGroup(
            label(r"red: \ placebo; \ green: \ drug", font_size=22),
            label(r"solid: \ everyone, \ as the World knows", font_size=22, color=GREY_A),
            label(r"dashed: \ with dropouts' last values carried forward", font_size=22, color=MNC),
            label(r"LOCF flattens the placebo curve most", font_size=22, color=MNC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The true average scores, for everyone, rise steadily in both arms, faster on placebo. "
            "<bookmark mark='b'/> With the last observations carried forward, both curves flatten, because each dropout is "
            "frozen at an earlier, better score. <bookmark mark='c'/> Placebo patients drop out more, so its curve is "
            "flattened more, and the gap between the arms, the treatment effect, shrinks."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(lines[("true", 0)]), Create(lines[("true", 1)]), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(dashed), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def locf_table(self):
        d = load("sins")["locf"]
        rows = [[r"drug $-$ placebo at month 5", r"estimate"],
                [r"the truth \ (everyone)", f"{d['true']:.2f}"],
                [r"LOCF", f"{d['locf']:.2f}"],
                [r"completers only", f"{d['cc']:.2f}"],
                [r"MAR imputation, \ month by month", f"{d['mi']:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.4, row_buff=0.34, colors=[GREY_A, TRUEC, MNC, CCC, MIC]).move_to([0, 0.8, 0])
        foot = label(rf"completed the trial: \ {100 * d['completed'][0]:.0f}\% on placebo, \ {100 * d['completed'][1]:.0f}\% on the drug",
                     font_size=24, color=GREY_A).move_to([0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The treatment effect at month five. <bookmark mark='b'/> The truth is " + say(d["true"], 2)
            + " points. <bookmark mark='c'/> Carrying values forward understates it, at " + say(d["locf"], 2) + ". "
            "<bookmark mark='d'/> Here the completers alone happen to land near the truth, and an imputation that assumes "
            "dropouts would have continued like similar patients who stayed recovers it too. LOCF is neither conservative "
            "nor safe: its bias can go either way, depending on how dropout and disease interact."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.clear_scene()

    def board(self):
        rows = board_rows("complete-case")
        text = (
            "<bookmark mark='a'/> The Coverage Board. A seeded design in which forty percent of outcomes are missing at "
            "random given a covariate. The complete-case mean's ninety percent interval is broken: the rows that survive "
            "have the wrong mix of x. <bookmark mark='b'/> But the complete-case regression slope keeps its promise, "
            "because missingness depends on the regressor alone. Whether complete cases are safe depends on the question, "
            "not just the data."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])

    def indicator(self):
        rows = fit_rows(VGroup(
            label(r"the missing-indicator method: \ fill with 0, \ add a dummy for missing", font_size=26, color=MNC),
            label(r"can bias covariate coefficients even under MCAR \ (Greenland \& Finkle 1995)", font_size=26, color=MNC),
            label(r"baseline trial adjustment can preserve treatment contrasts; use appropriate model and SEs", font_size=26, color=MIC),
            label(r"a reminder: \ whether a method works depends on the design", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Another shortcut fills a missing covariate with zero and adds an indicator for "
            "having been missing. <bookmark mark='b'/> Sander Greenland and William Finkle showed in 1995 that it can"
            " bias covariate coefficients even when the data are missing completely at random, because the filled "
            "zeros distort the covariate's relation to everything else. <bookmark mark='c'/> There is one honest use:"
            " for baseline covariates in a randomized trial, where randomization protects the treatment comparison. "
            "<bookmark mark='d'/> Whether a method is safe depends on the design, not only on the data."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()


    def available(self):
        rows = [
            cmath(r"\text{available cases}", r":", r"\text{each mean, \ variance, \ covariance from whatever pairs exist}", font_size=28),
            cmath(r"\text{uses more data}", r":", r"\text{than complete cases}", font_size=30),
            cmath(r"\text{but}", r":", r"\text{the covariance matrix need not be positive definite}", font_size=30),
            cmath(r"\text{and}", r":", r"\text{each entry comes from a different subsample}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"pairwise deletion"), why(r"more information"), why(r"impossible correlations"), why(r"possible covariance incoherence")]
        with self.voiceover(
            "<bookmark mark='a'/> Available-case analysis computes each mean, variance and covariance from whatever "
            "rows have the variables it needs. <bookmark mark='b'/> It uses more of the data than complete cases. "
            "<bookmark mark='c'/> But the resulting covariance matrix need not be positive definite: its entries can "
            "form an indefinite matrix even though individually computed pairwise correlations stay between minus one"
            " and one; regressions built on it can be nonsense. <bookmark mark='d'/> Each entry describes a different"
            " subsample, so the assembled entries can be incoherent as one covariance matrix. Under MCAR they can "
            "still be consistent, so incoherence is a finite-sample possibility rather than a universal failure."
        ) as vo:
            heading = label('Pairwise estimates can form an incoherent covariance matrix', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def outcome_vs_covariate(self):
        rows = fit_rows(VGroup(
            label(r"missing outcomes and missing covariates are different problems", font_size=26, color=TAUC),
            label(r"correct conditional outcome likelihood: missing outcomes add no information without auxiliaries", font_size=26, color=MIC),
            label(r"covariates missing: \ complete cases waste the outcome information of every incomplete row", font_size=26, color=MNC),
            label(r"imputation helps most when covariates, \ not outcomes, \ have the holes", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Where the holes are matters as much as why. <bookmark mark='b'/> If only the "
            "outcome is missing, and at random given the covariates, under a correctly specified conditional outcome "
            "model, with no additional auxiliary information, complete cases already provide its likelihood "
            "information: imputing from that same model creates no new information. Auxiliary measurements and "
            "different estimands can change the comparison. <bookmark mark='c'/> If covariates are missing, dropping "
            "those rows throws away their outcomes and their other covariates, which carry real information. "
            "<bookmark mark='d'/> This is one reason imputation can be especially helpful when the holes are in the "
            "covariates."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

