from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


class CV(VoiceoverScene):
    def construct(self):
        self.card()
        self.targets()
        self.setup_()
        self.scatter()
        self.why_()
        self.intervals()
        self.nested_ladder()
        self.selection()
        self.board()
        self.lesson()

    def card(self):
        card = chapter_card(4, r"What cross-validation estimates", r"This model, or models like it?", lit=(1974,), part=PART)
        with self.voiceover("Chapter four. What cross-validation estimates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def targets(self):
        rows = [
            cmath(r"\mathrm{Err}_{XY}", r"=", r"E\big[L(Y, \hat f(X)) \mid \text{these training data}\big]", font_size=30),
            cmath(r"\mathrm{Err}", r"=", r"E\big[\mathrm{Err}_{XY}\big] \ \text{over training sets of size } n", font_size=30),
            cmath(r"\widehat{\mathrm{Err}}_{CV}", r"=", r"\tfrac1n \textstyle\sum_i L\big(y_i, \hat f^{-k(i)}(x_i)\big)", font_size=30),
            cmath(r"\text{which?}", r":", r"\text{we use it as if it were } \mathrm{Err}_{XY}", font_size=30),
        ]
        rows[3][-1].set_color(CALC)
        whys = [why(r"the error of the model we have"), why(r"the error of the procedure"),
                why(r"Stone (1974); \ Geisser (1975); \ Part 19"), why(r"`our model's error is \ldots'")]
        with self.voiceover(
            "<bookmark mark='a'/> There are two different errors we might want. The first is the error of the model we "
            "actually fitted, on these training data, when it meets new cases: Err X Y, a conditional error. <bookmark "
            "mark='b'/> The second is the average of that over all the training sets of the same size we might have "
            "drawn: Err, the error of the procedure. <bookmark mark='c'/> Cross-validation, from Part 19, holds out each "
            "fold in turn, fits on the rest, and averages the held-out losses. <bookmark mark='d'/> We almost always report "
            "it as if it estimated the first: our model's error rate is so much. Does it?"
        ) as vo:
            intro=label('A fitted model and a learning procedure have different risk targets',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def setup_(self):
        d = load("cv")
        rows = [
            cmath(r"y", r"=", r"X\beta + \varepsilon, \ \ n = 100, \ p = 20, \ \sigma = 1", font_size=30),
            cmath(r"\mathrm{Err}_{XY}", r"=", r"1 + \|\hat\beta - \beta\|^2", font_size=32),
            cmath(r"\mathrm{Err}", r"=", rf"1 + \tfrac{{p}}{{n - p - 1}} = {d['Err']:.3f}", font_size=32),
            cmath(r"\text{each data set}", r":", r"\text{10-fold CV, \ and the exact } \mathrm{Err}_{XY}", font_size=30),
        ]
        rows[1][-1].set_color(TRUEC)
        whys = [why(r"Gaussian $X$, \ least squares"), why(r"known exactly for each data set"),
                why(r"$E\,\mathrm{tr}(X'X)^{-1}$, \ inverse Wishart"), why(r"1,000 data sets")]
        with self.voiceover(
            "<bookmark mark='a'/> Stephen Bates, Trevor Hastie and Robert Tibshirani studied the question in 2024, and "
            "their cleanest example is ordinary least squares. A hundred observations, twenty standard normal predictors, "
            "noise of variance one. <bookmark mark='b'/> For a fitted coefficient vector, the error on a new case is exactly "
            "one plus the squared distance from beta hat to beta, so for each simulated data set we know its "
            "conditional error exactly. <bookmark mark='c'/> Its average over data sets is one plus p over n minus p minus "
            "one, about one point two five, from the inverse Wishart mean. <bookmark mark='d'/> On each of a thousand data "
            "sets, compute ten-fold cross-validation and the exact conditional error, and compare."
        ) as vo:
            intro=label('Gaussian least squares gives an independently known risk target',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scatter(self):
        d = load("cv")
        cv, ex = np.asarray(d["cv"]), np.asarray(d["err_xy"])
        A = axes([1.0, 1.6], [0.7, 2.1], x_length=6.0, y_length=4.6, xlabel=r"$\mathrm{Err}_{XY}$ \ (exact)",
                 ylabel=r"CV estimate", xticks=[1.1, 1.3, 1.5], yticks=[1.0, 1.5, 2.0], xfmt=lambda v: rf"{v:.1f}",
                 yfmt=lambda v: rf"{v:.1f}", center=[-2.6, 0.2, 0])
        ax = A.ax
        k = (ex >= 1.0) & (ex <= 1.6) & (cv >= 0.7) & (cv <= 2.1)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=PREDC, fill_opacity=0.7) for a, b in zip(ex[k], cv[k])])
        diag = DashedLine(ax.c2p(1.0, 1.0), ax.c2p(1.6, 1.6), color=GREY_B, stroke_width=2)
        errl = DashedLine(ax.c2p(d["Err"], 0.7), ax.c2p(d["Err"], 2.1), color=TRUEC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"correlation: \ {d['corr']:.2f}", font_size=22, color=CALC),
            label(rf"SD of $\mathrm{{Err}}_{{XY}}$: \ {d['sd_errxy']:.3f}", font_size=22, color=TRUEC),
            label(rf"SD of the CV estimate: \ {d['sd_cv']:.3f}", font_size=22, color=PREDC),
            label(rf"mean CV {d['mean_cv']:.3f} \ vs \ Err {d['Err']:.3f}", font_size=22),
            label(r"CV primarily tracks average error in this Gaussian OLS example", font_size=22, color=CALC),
        ), 4.6, 0.4, [4.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are three hundred of the thousand data sets: the exact conditional error across, "
            "the cross-validation estimate up. If cross-validation estimated the error of the model in hand, the points "
            "would lie along the diagonal. <bookmark mark='b'/> They form a shapeless cloud. The correlation between the "
            "estimate and the quantity we think it estimates is " + say(d["corr"]) + ": very little linear association in this experiment. <bookmark mark='c'/> "
            "The conditional error itself varies little from data set to data set, with a standard deviation of point oh "
            "nine; <bookmark mark='d'/> the estimate varies more than twice as much. Its average, one point two nine, is "
            "close to the average error, one point two five, slightly high because each fold trains on only ninety "
            "points. <bookmark mark='e'/> Bates, Hastie and Tibshirani's conclusion: cross-validation estimates Err, the "
            "error of the procedure averaged over training sets, and may be weakly informative about the error of the "
            "particular model we fitted."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.01), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]), Create(errl))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def why_(self):
        rows = fit_rows(VGroup(
            label(r"the CV estimate and $\mathrm{Err}_{XY}$ are computed from the same data", font_size=26),
            label(r"a data set that happens to fit well looks good in CV \ldots", font_size=26, color=PREDC),
            label(r"\ldots but its $\hat\beta$ was not closer to $\beta$ for that reason", font_size=26, color=MISSC),
            label(r"the same holds for the bootstrap, \ AIC, \ $C_p$ \ (Hastie et al. 2009, \S 7.12)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why should this be? Both quantities depend on the same training data, but on different "
            "features of it. <bookmark mark='b'/> A data set with small, well-behaved noise makes the held-out errors "
            "small, so cross-validation looks good. <bookmark mark='c'/> But beta hat is no closer to beta for that, so the "
            "model's real error is no smaller. The two are nearly independent. <bookmark mark='d'/> This is not special to "
            "cross-validation: Hastie, Tibshirani and Friedman's book had already shown that the bootstrap, A I C and "
            "Mallows' C p behave the same way. Estimating the error of the model in hand, rather than of the procedure, is "
            "simply very hard."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def intervals(self):
        d = load("cv")
        rows = [
            cmath(r"\widehat{\mathrm{se}}", r"=", r"\mathrm{sd}(e_1, \ldots, e_n)/\sqrt n", font_size=32),
            cmath(r"\text{interval}", r":", r"\widehat{\mathrm{Err}}_{CV} \pm 1.645\, \widehat{\mathrm{se}}", font_size=32),
            cmath(r"\text{covers } \mathrm{Err}", r":", rf"{100 * d['cover_err']:.1f}\% \ \text{{(nominal 90\%)}}", font_size=32),
            cmath(r"\mathrm{sd}(\widehat{\mathrm{Err}}_{CV}) / \overline{\widehat{\mathrm{se}}}", r"=", rf"{d['se_ratio']:.2f}", font_size=32),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"treats the $n$ held-out losses as independent"), why(r"the usual report"),
                why(r"1,000 data sets"), why(r"the folds share training data")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual standard error for a cross-validation estimate treats the n held-out losses as "
            "if they were independent: their standard deviation over root n. <bookmark mark='b'/> Plus or minus one point "
            "six four five of those gives a nominal ninety percent interval. <bookmark mark='c'/> Even for its proper "
            "target, the average error, it covers only " + say(100 * d["cover_err"], 1) + " percent of the time. "
            "<bookmark mark='d'/> The real standard deviation of the estimate is " + say(d["se_ratio"]) + " times the "
            "naive standard error, because training-size bias and dependence both matter. The held-out losses are correlated: every fold's model was trained on mostly "
            "the same points. Bates, Hastie and Tibshirani propose estimating the correction with a nested "
            "cross-validation."
        ) as vo:
            intro=label('Naive cross-validation intervals ignore dependence and training-size bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nested_ladder(self):
        outer = VGroup(*[Rectangle(width=1.9, height=0.55, stroke_color=GREY_B, stroke_width=2,
                                   fill_color=(CALC if k == 2 else PREDC), fill_opacity=0.35) for k in range(5)]).arrange(RIGHT, buff=0.08)
        outer.move_to([0, 1.6, 0])
        olab = label(r"outer folds: \ gold held out to \emph{assess}", font_size=22, color=CALC).next_to(outer, UP, buff=0.25)
        inner = VGroup(*[Rectangle(width=1.4, height=0.42, stroke_color=GREY_B, stroke_width=1.5,
                                   fill_color=(BANDC if k == 1 else PREDC), fill_opacity=0.45) for k in range(4)]).arrange(RIGHT, buff=0.06)
        inner.move_to([0, 0.0, 0])
        ilab = label(r"inner folds, \ within the blue: \ green held out to \emph{tune}", font_size=22, color=BANDC).next_to(inner, DOWN, buff=0.25)
        arrows = VGroup(Arrow(outer.get_bottom() + LEFT * 2, inner.get_top() + LEFT * 2.6, buff=0.1, color=GREY_B, stroke_width=2),
                        Arrow(outer.get_bottom() + RIGHT * 2, inner.get_top() + RIGHT * 2.6, buff=0.1, color=GREY_B, stroke_width=2))
        foot = fit_rows(VGroup(
            label(r"tuning and assessing with the same folds: \ optimistic", font_size=24, color=MISSC),
            label(r"Varma \& Simon (2006): \ selection inside CV, \ or the error is biased low", font_size=24, color=GREY_A),
        ), 12.4, 0.35, [0, -2.2, 0])
        intro=label("Tune inside each assessment split",font_size=34).to_edge(UP,buff=.35)
        self.add(intro)
        with self.voiceover(
            "<bookmark mark='a'/> Nested cross-validation has a second, older use. If cross-validation chooses a tuning "
            "parameter, such as a forest's m try or boosting's number of trees, then the minimum of the cross-validation "
            "curve is a biased, optimistic estimate of the chosen model's error: we picked the value that happened to look "
            "best. <bookmark mark='b'/> So split twice. The outer folds are held out only to assess. <bookmark mark='c'/> "
            "Within each outer training set, an inner cross-validation does all the tuning. <bookmark mark='d'/> Sudhir "
            "Varma and Richard Simon showed in 2006 how large the optimism from tuning on the assessment folds can be, "
            "following Christophe Ambroise and Geoffrey McLachlan's demonstration of 2002 that selecting genes outside the "
            "cross-validation loop can make random labels look predictable."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(outer), FadeIn(olab))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(inner), FadeIn(ilab))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def selection(self):
        rows = [
            cmath(r"\text{choose } \hat\lambda", r"=", r"\arg\min_\lambda \widehat{\mathrm{Err}}_{CV}(\lambda)", font_size=32),
            cmath(r"E\,\widehat{\mathrm{Err}}_{CV}(\hat\lambda)", r"\le", r"\min_\lambda E\,\widehat{\mathrm{Err}}_{CV}(\lambda)", font_size=30),
            cmath(r"\text{the gap}", r":", r"\text{grows with the number of candidates}", font_size=32),
            cmath(r"\text{remedy}", r":", r"\text{nested CV, \ or a fresh test set}", font_size=32),
        ]
        rows[1][-1].set_color(MISSC)
        whys = [why(r"the tuning step"), why(r"the minimum of noisy curves is low"), why(r"Part 33's winner's curse"),
                why(r"assess with data the choice never saw")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic of that optimism is Part 33's again. Choosing the tuning parameter that "
            "minimizes the cross-validation curve, <bookmark mark='b'/> the expected value of the minimum is at most the "
            "minimum of the expected values, because the minimum of noisy curves lands, on average, below every one of "
            "them. <bookmark mark='c'/> More competing noisy choices can increase this optimism; the amount depends on their joint errors: the winner's curse of a selected "
            "estimate. <bookmark mark='d'/> The remedy is to assess the whole procedure, tuning included, on data that "
            "the choice never saw."
        ) as vo:
            intro=label('Selecting the best noisy validation score creates optimism',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("CV interval")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board: the naive ninety percent interval from ten-fold cross-validation, as "
                   "an interval for the average prediction error of least squares with a hundred points and twenty "
                   "predictors. <bookmark mark='b'/> Broken: it covers about eighty-three percent of the time, because its "
                   "standard error ignores the correlation between folds.",
                   [("b", [0])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"cross-validation targets fold-training performance; \ full-fit conditional error is a different target", font_size=26, color=CALC),
            label(r"naive independent-loss errors can understate uncertainty", font_size=26, color=MISSC),
            label(r"tune inside, \ assess outside", font_size=26, color=TREEC),
            label(r"next: \ can a predicted probability be taken at its word?", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cross-validation targets average performance at the fold training size, and need "
            "not closely track the conditional error of the full-data fit. <bookmark mark='b'/> The naive "
            "independent-loss standard error undercovers in this example; cross-validation uncertainty depends on the"
            " learning problem. <bookmark mark='c'/> And any choice it makes must be assessed outside it. <bookmark "
            "mark='d'/> Next, a different kind of honesty: when a model says seventy percent, does it mean seventy "
            "percent?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
