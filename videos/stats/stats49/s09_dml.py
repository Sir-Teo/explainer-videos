from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class DMLTheory(VoiceoverScene):
    def construct(self):
        self.card()
        self.orthogonality()
        self.conditions()
        self.chart()
        self.crossfit()
        self.practice()

    def card(self):
        card = chapter_card(8, r"DML theory", r"Orthogonality, \ cross-fitting, \ and the product rate", lit=(2018,), part=PART)
        with self.voiceover("Chapter eight. The theory of double machine learning: orthogonality, cross-fitting, and the product rate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def orthogonality(self):
        rows = [
            cmath(r"E\,\psi(W; \theta_0, \eta) = 0", r":", r"\text{an estimating function with nuisance } \eta", font_size=34),
            cmath(r"\partial_\eta\, E\,\psi(W; \theta_0, \eta_0)[\eta - \eta_0]", r"=", r"0 \ \ \text{for all directions}", font_size=32),
            cmath(r"\text{the efficient influence function}", r":", r"\text{always Neyman-orthogonal, \ by chapter 5}", font_size=32),
            cmath(r"\text{Part 48's footprint}", r"=", r"0: \ \text{first-order errors in } \hat\eta \text{ do not reach } \hat\theta", font_size=32),
        ]
        rows[1][-1].set_color(TANC)
        rows[3][-1].set_color(EFFC)
        whys = [why(r"Chernozhukov et al.\ (2018)"), why(r"Neyman (1959): \ orthogonality"), why(r"orthogonal to the nuisance tangent space"), why(r"why plug-in errors wash out")]
        with self.voiceover(
            "<bookmark mark='a'/> Victor Chernozhukov and colleagues' double machine learning, of 2018, starts from an "
            "estimating function that depends on a nuisance. <bookmark mark='b'/> It asks that the function be Neyman "
            "orthogonal: its expectation must not change to first order when the nuisance moves in any direction. Jerzy "
            "Neyman used the idea in 1959 for tests with nuisance parameters. <bookmark mark='c'/> The efficient influence "
            "function always has this property, because the efficient score is orthogonal to the nuisance tangent space. "
            "<bookmark mark='d'/> In Part forty-eight's language, the footprint is zero: first-order errors in the nuisance "
            "estimates never reach the estimate of theta."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def conditions(self):
        rows = [
            cmath(r"\sqrt n\,(\hat\theta - \theta_0)", r"=", r"\tfrac{1}{\sqrt n}\textstyle\sum \phi^*(W_i) + \sqrt n\, R_2 + \text{(empirical-process term)}", font_size=30),
            cmath(r"\sqrt n\, R_2", r"\lesssim", r"\sqrt n\, \|\hat e - e\|\, \|\hat\mu - \mu\| \to 0", font_size=34),
            cmath(r"\Leftarrow", r"\;", r"\|\hat e - e\| = o(n^{-a}), \ \|\hat\mu - \mu\| = o(n^{-b}), \ a + b \ge \tfrac12", font_size=32),
            cmath(r"\text{cross-fitting}", r":", r"\text{fit } \hat\eta \text{ on other folds: \ no Donsker condition}", font_size=32),
        ]
        rows[2][-1].set_color(EFFC)
        rows[3][-1].set_color(OSC)
        whys = [why(r"chapter 6's expansion"), why(r"chapter 7's product"), why(r"e.g.\ both $n^{-1/4}$"), why(r"sample splitting, \ Bickel (1982); \ Schick (1986)")]
        with self.voiceover(
            "<bookmark mark='a'/> Then chapter six's expansion has three parts: the efficient influence function's average, "
            "root n times the second-order remainder, and an empirical-process term. <bookmark mark='b'/> By chapter seven, "
            "the remainder is bounded by the product of the two nuisance errors. <bookmark mark='c'/> So it suffices that "
            "the product of the rates beats root n: if the propensity converges at n to the minus a and the outcome "
            "regression at n to the minus b, we need a plus b at least a half. Both at n to the minus a quarter is enough, "
            "far slower than root n, and within reach of forests, boosting and neural networks. <bookmark mark='d'/> The "
            "empirical-process term would need a Donsker condition on the nuisance estimators, which flexible machine "
            "learning violates. Cross-fitting removes the need: estimate the nuisances on other folds, so that, conditionally, "
            "the term is an average of independent mean-zero pieces."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("rates")
        ln = np.log10(d["ns"])
        A = axes([2.2, 4.4], [-1.3, 2.8], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}\, \sqrt n\,|\text{bias}|$",
                 xticks=[np.log10(250), 3, np.log10(4000), np.log10(16000)], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-1, 0, 1, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0.5_0.5": TANC, "0.25_0.25": OSC, "0.375_0.125": GRADC, "0.125_0.125": EFFC, "0.0_0.0": NUIC}
        lines = {}
        for k, c in cols.items():
            y = np.log10(np.maximum(np.abs(d["lines"][k]), 0.05))
            lines[k] = VGroup(polyline(ax, ln, y, c, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(ln, y)])
        side = fit_rows(VGroup(
            label(r"errors $n^{-a}$ (outcome) and $n^{-b}$ (propensity)", font_size=22),
            label(r"green: \ $a = b = \tfrac12$; \ teal: \ $\tfrac14, \tfrac14$; \ blue: \ $\tfrac38, \tfrac18$", font_size=22, color=OSC),
            label(r"$a + b = \tfrac12$ or more: \ flat: \ root-$n$ is safe", font_size=22, color=TANC),
            label(r"gold: \ $\tfrac18, \tfrac18$: \ grows like $n^{1/4}$", font_size=22, color=EFFC),
            label(r"red: \ errors that never shrink: \ like $\sqrt n$", font_size=22, color=NUIC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The product-rate condition, tested directly. Corrupt the outcome regressions by n to the "
            "minus a and the propensity by n to the minus b, in directions that do not cancel, and track root n times the "
            "one-step's bias. <bookmark mark='b'/> With a and b both a half, or both a quarter, or three eighths and one "
            "eighth, <bookmark mark='c'/> the lines are flat: whenever a plus b is a half or more, the bias is a bounded "
            "fraction of a standard error, and root n inference is safe. Notice that one nuisance can be quite poor if the "
            "other is good. <bookmark mark='d'/> With both at n to the minus an eighth, the scaled bias grows like n to the "
            "one quarter. <bookmark mark='e'/> And with errors that never shrink, it grows like root n: the estimator is "
            "inconsistent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated: \ 120--300 samples per point")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["0.5_0.5"]), Create(lines["0.25_0.25"]), Create(lines["0.375_0.125"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["0.125_0.125"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(lines["0.0_0.0"]), FadeIn(side[4]))
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"DML in practice:", font_size=28, color=GREY_A),
            label(r"$K = 5$ folds is typical; \ average the scores over all folds (DML2) \ rather than the estimates (DML1)", font_size=26, color=OSC),
            label(r"repeat the random split and take the median estimate: \ the split is a nuisance too", font_size=26, color=GRADC),
            label(r"choose learners by cross-validated prediction error \ \emph{for each nuisance separately}", font_size=26, color=TANC),
            label(r"clip or trim propensities, \ and report it: \ overlap is an assumption, \ not a tuning parameter", font_size=26, color=NUIC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice, a few conventions have settled. <bookmark mark='b'/> Five folds is typical, "
            "and the scores are pooled across folds before solving, which behaves better in small samples than averaging "
            "fold-wise estimates. <bookmark mark='c'/> The random split adds noise of its own, so repeat it several times "
            "and report the median. <bookmark mark='d'/> Choose each learner by its own cross-validated prediction error: "
            "the propensity and the outcome regressions are separate prediction problems. <bookmark mark='e'/> And if "
            "propensities must be clipped, say so: clipping changes the estimand, and poor overlap is an assumption that "
            "failed, not a parameter to tune."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def crossfit(self):
        d = load("rates")
        c = d["cf"]
        rows = [[r"5-NN nuisances, \ $n = 600$", r"bias", r"actual SD", r"reported SE", r"90\% coverage"],
                [r"fitted to all the data", f"{c['reuse']['bias']:+.3f}", f"{c['reuse']['sd']:.3f}", f"{c['reuse']['se']:.3f}", f"{100 * c['reuse']['cover']:.1f}\\%"],
                [r"cross-fitted, \ 2 folds", f"{c['cross']['bias']:+.3f}", f"{c['cross']['sd']:.3f}", f"{c['cross']['se']:.3f}", f"{100 * c['cross']['cover']:.1f}\\%"]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.45, colors=[GREY_B, NUIC, OSC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        foot = label(rf"the smooth world; \ {d['cf_reps']} samples", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"reusing the data shrinks the residuals \ (a 5-NN fit partly memorizes $Y$), \ so the SE is too small", font_size=24, color=NUIC).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Cross-fitting, tested. Five-nearest-neighbour outcome regressions, which partly memorize "
            f"the data. Fitted to all the data and evaluated on the same points, the residuals are too small, so the "
            f"reported standard error, {say(c['reuse']['se'], 3)}, understates the actual {say(c['reuse']['sd'], 3)}, and "
            f"ninety percent intervals cover {100 * c['reuse']['cover']:.0f} percent of the time. Cross-fitted on two folds, the "
            f"reported standard error matches the actual one, and coverage rises to {100 * c['cross']['cover']:.0f} percent; "
            f"what remains is a small smoothing bias from a crude learner. <bookmark mark='b'/> Cross-fitting costs nothing "
            f"asymptotically, and with flexible learners it is the difference between honest and dishonest standard errors."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()
