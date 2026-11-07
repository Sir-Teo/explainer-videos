from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


class Boosting(VoiceoverScene):
    def construct(self):
        self.card()
        self.adaboost()
        self.stagewise()
        self.gradient()
        self.picture()
        self.shrinkage()
        self.curves()
        self.exponential()
        self.lasso_link()
        self.modern()

    def card(self):
        card = chapter_card(3, r"Boosting", r"Stagewise additive modelling", lit=(2000,), part=PART)
        with self.voiceover("Chapter three. Boosting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def adaboost(self):
        rows = fit_rows(VGroup(
            label(r"Kearns \& Valiant (1988): \ can weak learners be combined into a strong one?", font_size=26),
            label(r"Schapire (1990): \ yes; \ Freund \& Schapire (1997): \ AdaBoost", font_size=26, color=BOOSTC),
            label(r"reweight the cases the last classifier got wrong; \ fit again; \ vote", font_size=26),
            label(r"Breiman: \ `the best off-the-shelf classifier in the world'", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Boosting came from computer science. In 1988 Michael Kearns and Leslie Valiant asked "
            "whether learners that are only slightly better than guessing could be combined into one that is arbitrarily "
            "accurate. <bookmark mark='b'/> Robert Schapire proved in 1990 that they could, and in 1997 Yoav Freund and "
            "Schapire published the algorithm that made it practical, AdaBoost. <bookmark mark='c'/> Fit a simple "
            "classifier, often a single split; increase the weights of the cases it got wrong; fit another; and so on, "
            "finally letting the classifiers vote with weights depending on their accuracy. <bookmark mark='d'/> It "
            "worked so well, and overfitted so little, that Breiman called it the best off-the-shelf classifier in the "
            "world. Nobody quite knew why it worked."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stagewise(self):
        rows = [
            cmath(r"F_M(x)", r"=", r"\textstyle\sum_{m=1}^M \beta_m\, h(x; \gamma_m)", font_size=32),
            cmath(r"\text{stage } m", r":", r"(\beta_m, \gamma_m) = \arg\min \textstyle\sum_i L\big(y_i, F_{m-1}(x_i) + \beta h(x_i; \gamma)\big)", font_size=26),
            cmath(r"L = e^{-yF}", r"\Rightarrow", r"\text{AdaBoost, \ exactly}", font_size=32),
            cmath(r"\text{earlier terms}", r":", r"\text{never revisited}", font_size=32),
        ]
        rows[2][-1].set_color(BOOSTC)
        whys = [why(r"an additive model in basis functions"), why(r"add one term, \ keep the rest"),
                why(r"Friedman, \ Hastie \& Tibshirani (2000)"), why(r"`stagewise', \ not `stepwise'")]
        with self.voiceover(
            "<bookmark mark='a'/> The explanation came from statisticians. In 2000 Jerome Friedman, Trevor Hastie and "
            "Robert Tibshirani showed that boosting fits an additive model, a sum of simple basis functions such as small "
            "trees. <bookmark mark='b'/> It fits it greedily, one term at a time: at stage m, choose the new term to "
            "minimize the loss of the current model plus that term, leaving all earlier terms alone. <bookmark mark='c'/> "
            "With the exponential loss, e to the minus y F, for labels plus or minus one, this forward stagewise procedure "
            "is exactly AdaBoost: the case weights are the exponential losses of the current model. <bookmark mark='d'/> "
            "Because earlier terms are never refitted, this is stagewise rather than stepwise, and that turns out to "
            "matter."
        ) as vo:
            intro=label('Stagewise fitting adds terms without refitting earlier coefficients',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gradient(self):
        rows = [
            cmath(r"r_{im}", r"=", r"-\dfrac{\partial L(y_i, F)}{\partial F}\Big|_{F = F_{m-1}(x_i)}", font_size=32),
            cmath(r"L = \tfrac12 (y - F)^2", r"\Rightarrow", r"r_{im} = y_i - F_{m-1}(x_i)", font_size=30),
            cmath(r"h_m", r"=", r"\text{a small tree fitted to the } r_{im}", font_size=32),
            cmath(r"F_m", r"=", r"F_{m-1} + \nu\, h_m, \ \ 0 < \nu \le 1", font_size=32),
        ]
        rows[3][-1].set_color(BOOSTC)
        whys = [why(r"steepest descent in function space"), why(r"the residuals"), why(r"Friedman (2001)"),
                why(r"$\nu$: \ shrinkage, \ the learning rate")]
        with self.voiceover(
            "<bookmark mark='a'/> Friedman then made it general, in his 2001 paper on gradient boosting. For any "
            "differentiable loss, compute the negative gradient of the loss at each training point, with respect to the "
            "current fitted value. <bookmark mark='b'/> For squared error that gradient is just the residual. <bookmark "
            "mark='c'/> Fit a small tree to these pseudo-residuals, <bookmark mark='d'/> and add it to the model, scaled "
            "by a learning rate nu. Boosting is steepest descent, not in a space of parameters, but in a space of "
            "functions, taking small steps each in the direction of a tree."
        ) as vo:
            intro=label('Gradient boosting fits trees to loss gradients',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("boost")
        x, y = np.asarray(d["stage_x"]), np.asarray(d["stage_y"])
        A = axes([0, 1], [-1, 11], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$y$", xticks=[0, 0.5, 1],
                 yticks=[0, 5, 10], center=[-2.0, 0.2, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=LABC) for a, b in zip(x[::2], y[::2])])
        stages = d["stages"]
        cur = polyline(ax, x, stages[0], BOOSTC, 3.5)
        side = fit_rows(VGroup(
            label(r"each stage: \ one split (a stump), \ $\nu = 0.3$", font_size=22),
            label(r"stage 1: \ a single step", font_size=22, color=BOOSTC),
            label(r"stages 2--12: \ each fits what is left", font_size=22, color=BOOSTC),
            label(r"a staircase approaching the curve", font_size=22, color=CALC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here it is in one dimension, with stumps, trees of a single split, and a learning rate "
            "of point three. <bookmark mark='b'/> The first stage puts one step into the constant fit, three tenths of the "
            "way towards the best split. <bookmark mark='c'/> Each further stage fits a stump to whatever is left over, and "
            "adds three tenths of it. <bookmark mark='d'/> After twelve stages the sum of twelve shrunken stumps is a staircase "
            "climbing towards the curve. No single term is a good model; their sum is."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(pts), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cur), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            for k in (1, 2, 3, 5, 7, 9, 11):
                new = polyline(ax, x, stages[k], BOOSTC, 3.5)
                self.play(Transform(cur, new), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def shrinkage(self):
        rows = [
            cmath(r"\nu = 1", r":", r"\text{each tree takes a full step}", font_size=32),
            cmath(r"\nu = 0.1", r":", r"\text{ten times as many trees, \ each a tenth}", font_size=32),
            cmath(r"\text{Friedman (2001)}", r":", r"\text{small }\nu\text{ often helps; tune both }\nu\text{ and }M", font_size=30),
            cmath(r"M", r":", r"\text{the regularization: \ stop early}", font_size=32),
        ]
        rows[2][-1].set_color(BOOSTC)
        whys = [why(r"greedy"), why(r"cautious"), why(r"an empirical regularity"), why(r"choose $M$ by validation")]
        with self.voiceover(
            "<bookmark mark='a'/> The learning rate turns out to matter a great deal. With nu equal to one, each tree"
            " takes its full step towards the residuals. <bookmark mark='b'/> With nu a tenth, each tree takes a "
            "tenth of a step, and many more trees are needed. <bookmark mark='c'/> Friedman found, and practitioners "
            "have confirmed ever since, that smaller steps often improve generalization when the number of stages is "
            "tuned appropriately; there is no universal ranking. <bookmark mark='d'/> The number of trees is then the"
            " main regularization: boosting keeps lowering the training error, and is stopped when the error on "
            "validation data stops falling."
        ) as vo:
            intro=label('Learning rate and stage count jointly control regularization',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("boost")
        b1, b01 = d["by_nu"]["1.0"], d["by_nu"]["0.1"]
        M = len(b01["test"])
        m = np.arange(1, M + 1)
        A = axes([0, M], [0, 25], x_length=7.4, y_length=4.4, xlabel=r"trees $M$", ylabel=r"mean squared error",
                 xticks=[0, 200, 400, 600], yticks=[0, 5, 10, 20], center=[-2.0, 0.2, 0])
        ax = A.ax
        sel = np.r_[np.arange(0, 60), np.arange(60, M, 5)]
        t1 = polyline(ax, m[sel], np.minimum(np.asarray(b1["test"])[sel], 25), MISSC, 3)
        r1 = polyline(ax, m[sel], np.minimum(np.asarray(b1["train"])[sel], 25), MISSC, 2, 0.45)
        t01 = polyline(ax, m[sel], np.minimum(np.asarray(b01["test"])[sel], 25), BOOSTC, 3.5)
        r01 = polyline(ax, m[sel], np.minimum(np.asarray(b01["train"])[sel], 25), BOOSTC, 2, 0.45)
        rf = DashedLine(ax.c2p(0, d["rf_mse"]), ax.c2p(M, d["rf_mse"]), color=TREEC, stroke_width=2)
        noise = DashedLine(ax.c2p(0, 1), ax.c2p(M, 1), color=GREY_B, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"Friedman 1, \ $n = 400$, \ trees of depth 2", font_size=22),
            label(rf"$\nu = 1$: \ best {b1['best']:.1f} at $M = {b1['best_m']}$, \ then worse", font_size=22, color=MISSC),
            label(rf"$\nu = 0.1$: \ {b01['best']:.2f} at $M = {M}$", font_size=22, color=BOOSTC),
            label(rf"a forest: \ {d['rf_mse']:.2f}; \ the noise: \ 1", font_size=22, color=TREEC),
            label(r"faint: \ training error", font_size=20, color=GREY_A),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On Friedman's function, with four hundred training points and trees of depth two, "
            "measured on three thousand test points. <bookmark mark='b'/> With nu equal to one, the test error falls "
            "fast, bottoms out at " + say(b1["best"], 1) + " after " + str(b1["best_m"]) + " trees, and then climbs, while "
            "the faint training error keeps falling: overfitting. <bookmark mark='c'/> With nu a tenth the error falls "
            "slowly but much further, to " + say(b01["best"], 1) + " after six hundred trees, and is still creeping down. "
            "<bookmark mark='d'/> For comparison, a random forest reaches " + say(d["rf_mse"], 1) + ", and the population Bayes risk cannot "
            "fall below the noise variance of one. These curve minima are test-set oracle diagnostics, not independently validated tuning results. On this smooth additive surface, slow boosting beats the forest by a wide "
            "margin."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), FadeIn(side[0]), Create(noise))
            vo.wait_until("b")
            self.play(Create(t1), Create(r1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(t01), Create(r01), FadeIn(side[2]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(Create(rf), FadeIn(side[3]))
        self.clear_scene()

    def exponential(self):
        rows = [
            cmath(r"F^\star(x)", r"=", r"\arg\min_F E\big[e^{-YF} \mid x\big]", font_size=32),
            cmath(r"", r"=", r"\tfrac12 \log \dfrac{P(Y = 1 \mid x)}{P(Y = -1 \mid x)}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{AdaBoost estimates half the log odds}", font_size=32),
            cmath(r"\text{a better loss}", r":", r"\log(1 + e^{-2yF}): \ \text{LogitBoost}", font_size=30),
        ]
        rows[1][-1].set_color(BOOSTC)
        whys = [why(r"the population minimizer"), why(r"set the derivative to zero"),
                why(r"a statistical estimand at last"), why(r"the binomial deviance; \ less weight on outliers")]
        with self.voiceover(
            "<bookmark mark='a'/> Friedman, Hastie and Tibshirani's view also said what AdaBoost estimates. Ask which "
            "function minimizes the expected exponential loss at each x. <bookmark mark='b'/> Setting the derivative to "
            "zero gives half the log odds of the class probabilities. <bookmark mark='c'/> So AdaBoost, invented with no "
            "probability model in sight, is estimating half the logit, the same estimand as logistic regression. "
            "<bookmark mark='d'/> That suggested a better loss: the binomial deviance, which gives the same minimizer but "
            "grows linearly rather than exponentially for badly misclassified points, and so is less thrown by mislabelled "
            "cases. They called it LogitBoost."
        ) as vo:
            intro=label('Expected exponential loss has a half-log-odds minimizer',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lasso_link(self):
        rows = fit_rows(VGroup(
            label(r"forward stagewise with tiny steps on the coefficients $\approx$ the lasso path", font_size=26, color=BOOSTC),
            label(r"Efron, \ Hastie, \ Johnstone \& Tibshirani (2004): \ Part 32's LARS", font_size=26, color=GREY_A),
            label(r"boosting $\approx$ an $L_1$-regularized fit in the space of all trees", font_size=26, color=CALC),
            label(r"Rosset, \ Zhu \& Hastie (2004): \ the margin-maximizing limit", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why should small steps help? A clue came from Part 32. Forward stagewise regression"
            " on the coefficients of a linear model, with infinitesimal steps, can follow the lasso path under "
            "additional design and coefficient-path conditions; the paths differ in general. <bookmark mark='b'/> "
            "Efron, Hastie, Johnstone and Tibshirani made that precise in their 2004 paper on least angle regression."
            " <bookmark mark='c'/> Boosting with a small learning rate is forward stagewise regression on a "
            "dictionary of all possible trees, so it behaves like an L one penalized fit in that enormous space, with"
            " the number of trees playing the role of the penalty. <bookmark mark='d'/> Saharon Rosset, Ji Zhu and "
            "Hastie showed that for classification its limit maximizes a margin, which goes a long way to explaining "
            "why it overfits so slowly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def modern(self):
        rows = fit_rows(VGroup(
            label(r"XGBoost (Chen \& Guestrin 2016), \ LightGBM, \ CatBoost: \ second-order steps, \ penalties, \ speed", font_size=26),
            label(r"subsampling each stage: \ Friedman's stochastic boosting (2002)", font_size=26, color=GREY_A),
            label(r"a boosted model is an estimator: \ bias, \ variance, \ a tuning parameter", font_size=26, color=BOOSTC),
            label(r"next: \ which error does validation actually estimate?", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Today's boosting libraries, XGBoost from Tianqi Chen and Carlos Guestrin in 2016, then "
            "LightGBM and CatBoost, add second-order steps using the Hessian of the loss, penalties on the leaf values, and "
            "very fast split-finding. <bookmark mark='b'/> They also fit each stage to a random subsample of the data, "
            "Friedman's stochastic gradient boosting of 2002, which helps in the same way that bagging does. <bookmark "
            "mark='c'/> Seen as statistics, a boosted model is an estimator like any other, with a bias, a variance, and a "
            "tuning parameter, the number of trees, chosen by validation. <bookmark mark='d'/> Which brings us to a "
            "question that sounds simple: when we validate, what error are we estimating?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
