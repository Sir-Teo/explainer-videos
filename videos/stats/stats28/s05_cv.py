from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class CV(VoiceoverScene):
    def construct(self):
        self.card()
        self.shortcuts()
        self.prostate_cv()
        self.press_prostate()
        self.what()
        self.kfold()
        self.picture()
        self.advice()

    def card(self):
        card = chapter_card(4, r"Cross-validation theory", r"What it estimates, \ and what it does not", lit=(1974,), part=PART)
        with self.voiceover("Chapter four. The theory of cross-validation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def shortcuts(self):
        d = load("cv")
        rows = [
            cmath(r"y_i - \hat y_{-i}", r"=", r"\dfrac{y_i - \hat y_i}{1 - h_{ii}}", font_size=32),
            cmath(r"\text{PRESS}", r"=", r"\tfrac1n \textstyle\sum_i \bigl(\tfrac{e_i}{1 - h_{ii}}\bigr)^2", font_size=30),
            cmath(r"\text{GCV}", r"=", r"\dfrac{\overline{\text{err}}}{(1 - \mathrm{tr}\,H/n)^2}", font_size=30),
            cmath(r"\text{both}", r":", rf"\text{{correlation }} {d['corr_press_gcv']:.3f} \text{{ across 400 data sets}}", font_size=30),
        ]
        rows[0][2].set_color(CVC)
        whys = [why(r"leave-one-out without refitting"), why(r"Allen (1974); \ Stone (1974)"), why(r"Craven \& Wahba (1979)"),
                why(r"$h_{ii}$ replaced by its average")]
        with self.voiceover(
            "<bookmark mark='a'/> Part 19 introduced cross-validation; here is its theory. For any linear smoother, "
            "leave-one-out needs no refitting: the left-out residual is the ordinary residual divided by one minus that "
            "point's leverage. <bookmark mark='b'/> Summing their squares gives PRESS, from David Allen and Mervyn Stone in "
            "1974. <bookmark mark='c'/> Replacing each leverage by the average gives generalized cross-validation, Peter "
            "Craven and Grace Wahba's: training error inflated by one minus the degrees of freedom over n, squared. "
            "<bookmark mark='d'/> Across four hundred regressions the two correlate at point nine nine."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def prostate_cv(self):
        d = load("prostate")
        m, s = np.asarray(d["cv_mean"]), np.asarray(d["cv_se"])
        sizes = np.arange(len(m))
        A = axes([-0.5, 8.5], [0, 1.8], x_length=7.4, y_length=4.2, xlabel=r"subset size", ylabel=r"10-fold CV error",
                 xticks=list(range(9)), yticks=[0, 0.5, 1, 1.5], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(k, a - b), ax.c2p(k, a + b), color=CVC, stroke_width=2.5) for k, (a, b) in enumerate(zip(m, s))])
        dots = VGroup(*[Dot(ax.c2p(k, a), radius=0.07, color=CVC) for k, a in enumerate(m)])
        best = d["picks"]["cv"]
        line = DashedLine(ax.c2p(-0.5, m[best] + s[best]), ax.c2p(8.5, m[best] + s[best]), color=PATH, stroke_width=2)
        one = d["picks"]["cv1se"]
        ring = Circle(radius=0.17, stroke_color=PATH, stroke_width=3).move_to(dots[one])
        rows = fit_rows(VGroup(
            label(r"the prostate training set: \ best subset of each size", font_size=22),
            label(rf"lowest CV error: \ size {best}", font_size=22, color=CVC),
            label(r"but sizes 2 and 4--8 are within one SE of it", font_size=22, color=GREY_A),
            label(rf"the one-SE rule: \ the smallest such: \ size {one}", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the prostate data, ten-fold cross-validation of the best subset of each size, with "
            "standard-error bars. <bookmark mark='b'/> The lowest CV error is at seven predictors, AIC's answer. "
            "<bookmark mark='c'/> But the curve is nearly flat from two predictors on: every size from two to eight except three is "
            "within one standard error of the best. <bookmark mark='d'/> Part 19's one-standard-error rule picks the smallest model "
            "within that band, two predictors, BIC's answer. Cross-validation's estimates are noisy, and the noise matters."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.1), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.1),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(dots[best].animate.scale(1.6), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ring), FadeIn(rows[3]))
        self.clear_scene()

    def what(self):
        rows = [
            cmath(r"\text{Err}_{XY}", r"=", r"E\bigl[L(Y, \hat f(X)) \mid \text{this training set}\bigr]", font_size=28),
            cmath(r"\text{Err}", r"=", r"E\,\text{Err}_{XY}: \ \text{averaged over training sets}", font_size=30),
            cmath(r"\text{CV}", r"\approx", r"\text{Err}, \ \text{not } \text{Err}_{XY}", font_size=32),
            cmath(r"\text{naive CV interval}", r":", r"\text{too narrow; \ nested CV fixes it}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the error of the model you actually fitted"), why(r"the error of the procedure"),
                why(r"Bates, Hastie \& Tibshirani (2024)"), why(r"the folds are not independent")]
        with self.voiceover(
            "<bookmark mark='a'/> But what does cross-validation estimate? Two different things could be meant: the error of "
            "the very model you fitted to your training set, <bookmark mark='b'/> or the error of the procedure, averaged over "
            "all the training sets you might have had. <bookmark mark='c'/> Stephen Bates, Trevor Hastie and Robert Tibshirani "
            "showed in 2024 that cross-validation estimates the second, not the first, even though the first is usually what "
            "people want. <bookmark mark='d'/> And the usual standard error across folds is too small, because the folds share "
            "data; their nested cross-validation fixes the interval."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("cv")
        cv, cond = np.asarray(d["cv10"]), np.asarray(d["cond"])
        A = axes([1.0, 2.2], [0.6, 2.6], x_length=5.6, y_length=4.6, xlabel=r"this fit's true error, \ $\text{Err}_{XY}$",
                 ylabel=r"its 10-fold CV estimate", xticks=[1.2, 1.6, 2.0], yticks=[1, 1.5, 2, 2.5], center=[-2.6, 0.2, 0])
        ax = A.ax
        m = (cond < 2.2) & (cv < 2.6) & (cv > 0.6)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=CVC, fill_opacity=0.7) for a, b in zip(cond[m], cv[m])])
        diag = DashedLine(ax.c2p(1.0, 1.0), ax.c2p(2.2, 2.2), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"400 regressions: \ $n = 50$, \ 10 predictors, \ 4 real", font_size=22),
            label(r"each dot: \ one training set", font_size=22, color=CVC),
            label(rf"correlation: \ {d['corr']:.2f}", font_size=22, color=RES),
            label(rf"but on average: \ CV {d['mean_cv']:.2f}, \ true {d['mean_cond']:.2f}", font_size=22, color=HIT),
        ), 4.6, 0.42, [4.0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> See it. Four hundred simulated regressions, fifty observations, ten predictors of which four "
            "matter. <bookmark mark='b'/> For each training set, its true error on new data against its ten-fold CV "
            "estimate. <bookmark mark='c'/> They are uncorrelated: minus point oh six. A training set that produced a bad fit "
            "is not one that cross-validation flags. <bookmark mark='d'/> Yet on average they agree, one point three two "
            "against one point three: cross-validation estimates the procedure's expected error well, and says almost nothing "
            "about this particular fit."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.003), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"5- or 10-fold: \ less variable than leave-one-out, \ slightly biased upwards", font_size=24),
            label(r"redo every data-driven step inside each fold \ (Part 19's selection bias)", font_size=24, color=RES),
            label(r"time series, \ groups: \ leave blocks out, \ not points", font_size=24, color=PATH),
            label(r"CV compares procedures; \ for one fit's error, \ use fresh data", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Practical rules. Five- or ten-fold cross-validation is less variable than leave-one-out, at "
            "the cost of a small upward bias. <bookmark mark='b'/> Every data-driven step, selection included, must be redone "
            "inside each fold, or the estimate is optimistic, Part 19's warning. <bookmark mark='c'/> With time series or "
            "grouped data, leave out whole blocks. <bookmark mark='d'/> And use cross-validation to compare procedures; to "
            "know one fitted model's error, there is no substitute for fresh data."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def kfold(self):
        rows = [
            cmath(r"\text{fit on}", r":", r"n(K - 1)/K \ \text{points}", font_size=30),
            cmath(r"\text{bias}", r":", r"\text{upward, \ largest for small } K", font_size=30),
            cmath(r"\text{variance}", r":", r"\text{LOO's } n \text{ fits are nearly identical}", font_size=30),
            cmath(r"K = 5 \text{ or } 10", r":", r"\text{the usual compromise}", font_size=30),
        ]
        rows[3][2].set_color(CVC)
        whys = [why(r"each fold's model sees less data"), why(r"a smaller training set predicts worse"),
                why(r"so their errors are highly correlated"), why(r"Breiman \& Spector (1992); \ Kohavi (1995)")]
        with self.voiceover(
            "<bookmark mark='a'/> How many folds? Each fold's model is fitted to a fraction K minus one over K of the data. "
            "<bookmark mark='b'/> A smaller training set predicts worse, so K-fold cross-validation is biased upwards, most for "
            "small K. <bookmark mark='c'/> Leave-one-out has almost no bias, but its n fitted models are nearly identical, so "
            "their errors are highly correlated and their average can be variable, especially for unstable procedures like "
            "subset selection. <bookmark mark='d'/> Leo Breiman and Philip Spector, and Ron Kohavi, found five or ten folds a "
            "good compromise, and that remains the default."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def press_prostate(self):
        from explainer.stats import museum
        from explainer.stats.kit import select as Se
        X, y, train, names = museum.prostate()
        Z = X[train]
        Z = (Z - Z.mean(0)) / Z.std(0)
        yt = y[train]
        n = len(yt)
        bs = Se.best_subset(Z, yt)
        pr, gc = [], []
        for b in bs:
            Xd = np.column_stack([np.ones(n), Z[:, b["subset"]]])
            pr.append(Se.press(Xd, yt))
            gc.append(Se.gcv(b["rss"], Xd.shape[1], n))
        cvm = np.asarray(load("prostate")["cv_mean"])
        A = axes([-0.5, 8.5], [0.4, 1.6], x_length=7.4, y_length=4.2, xlabel=r"subset size", ylabel=r"estimated prediction error",
                 xticks=list(range(9)), yticks=[0.5, 1, 1.5], center=[-2.0, 0.3, 0])
        ax = A.ax
        ks = np.arange(len(bs))
        lc = polyline(ax, ks, np.minimum(cvm, 1.6), CVC, 3)
        lp = polyline(ax, ks, np.minimum(pr, 1.6), PATH, 3)
        lg = DashedVMobject(polyline(ax, ks, np.minimum(gc, 1.6), BICC, 3), num_dashes=40)
        rows = fit_rows(VGroup(
            label(r"green: \ 10-fold CV \ (subsets re-chosen in each fold)", font_size=22, color=CVC),
            label(rf"gold: \ PRESS, \ exact LOO by the leverage formula: \ min at {int(np.argmin(pr))}", font_size=22, color=PATH),
            label(rf"purple dashed: \ GCV: \ min at {int(np.argmin(gc))}", font_size=22, color=BICC),
            label(r"smoother, \ and lower at 3--5: \ they never redo the search", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the same data, the shortcuts. Green is ten-fold cross-validation, with the best subset "
            "chosen again inside every fold. <bookmark mark='b'/> Gold is PRESS, exact leave-one-out for each fixed subset, "
            "computed from the leverages without a single refit. <bookmark mark='c'/> Purple is GCV, all but identical to "
            "PRESS. <bookmark mark='d'/> Both sit below the cross-validation curve, because they evaluate the subset that was "
            "chosen using all sixty-seven men; only the honest version repeats the search and pays for it."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lg), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
