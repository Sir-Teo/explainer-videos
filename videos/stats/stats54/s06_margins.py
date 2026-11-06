from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Margins(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.chart()
        self.margin_chart()
        self.bound()
        self.gradient()
        self.svm()
        self.compression()

    def card(self):
        card = chapter_card(5, r"Margins", r"Why boosting kept improving after it stopped making mistakes", lit=(1998,), part=PART)
        with self.voiceover("Chapter five. Margins: why boosting kept improving after it stopped making mistakes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def puzzle(self):
        rows = [
            cmath(r"\text{AdaBoost}", r":", r"f_T = \textstyle\sum_t \alpha_t h_t, \ \ h_t \text{ weak rules (stumps), \ reweighting mistakes}", font_size=30),
            cmath(r"\text{VC thinking}", r":", r"\text{more rounds} = \text{a bigger class} = \text{more overfitting}", font_size=32),
            cmath(r"\text{what happened}", r":", r"\text{test error kept falling after training error hit } 0", font_size=32),
            cmath(r"\text{the explanation}", r":", r"\text{margins } y f(x)/\textstyle\sum|\alpha_t| \text{ keep growing}", font_size=32),
        ]
        rows[2][-1].set_color(BADC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Freund \& Schapire (1997)"), why(r"the expectation"), why(r"Drucker \& Cortes; \ Breiman"), why(r"Schapire et al. (1998)")]
        with self.voiceover(
            "<bookmark mark='a'/> Yoav Freund and Robert Schapire's AdaBoost builds a classifier as a weighted vote of weak "
            "rules, such as single-split decision stumps, each round reweighting the examples the vote gets wrong. <bookmark "
            "mark='b'/> VC thinking predicts that more rounds mean a bigger class and more overfitting. <bookmark "
            "mark='c'/> What people saw instead, in the mid-nineteen-nineties, was test error that kept falling long after "
            "the training error reached zero. <bookmark mark='d'/> Schapire, Freund, Bartlett and Lee explained it in 1998: "
            "after the training error is zero, boosting keeps increasing the margins, the confidence of the vote on each "
            "training example."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("boosting")
        T = len(d["train"])
        t = np.arange(1, T + 1)
        lt = np.log10(t)
        A = axes([0, 2.7], [0, 0.16], x_length=7.4, y_length=4.4, xlabel=r"boosting rounds \ (log scale)", ylabel=r"error",
                 xticks=[0, 1, 2, np.log10(400)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.05, 0.1, 0.15], center=[-2.5, 0.2, 0])
        ax = A.ax
        ctr = polyline(ax, lt, d["train"], TRAINC, 4)
        cte = polyline(ax, lt, d["test"], TESTC, 4)
        z = d["zero_round"]
        zl = DashedLine(ax.c2p(np.log10(z), 0), ax.c2p(np.log10(z), 0.16), color=CLASSC, stroke_width=2.5)
        te = d["test"]
        side = fit_rows(VGroup(
            label(rf"Wisconsin breast cancer: \ {d['n_train']} training, \ {d['n_test']} test biopsies", font_size=22),
            label(r"AdaBoost with decision stumps, \ 400 rounds", font_size=22),
            label(rf"teal: \ training error, \ zero from round {z}", font_size=22, color=TRAINC),
            label(rf"blue: \ test error: \ {te[z - 1]:.3f} at round {z}, \ {te[-1]:.3f} at 400", font_size=22, color=TESTC),
            label(r"no overfitting, \ despite a growing class", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the Wisconsin breast cancer biopsies, {d['n_train']} for training and "
            f"{d['n_test']} for testing. <bookmark mark='b'/> AdaBoost with decision stumps on the thirty features, for four "
            f"hundred rounds. <bookmark mark='c'/> The training error, in teal, reaches zero at round {z}. <bookmark "
            f"mark='d'/> The test error, in blue, is {say(te[z - 1], 3)} at that point and {say(te[-1], 3)} after four "
            f"hundred rounds. <bookmark mark='e'/> Three hundred and eighty more stumps added to a vote that already fits "
            f"the training data perfectly, and the test error did not rise."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ctr), Create(zl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cte), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def margin_chart(self):
        d = load("boosting")
        A = axes([-0.5, 1.0], [0, 1.02], x_length=7.4, y_length=4.4, xlabel=r"normalized margin $y f(x)/\sum|\alpha_t|$", ylabel=r"fraction of training points $\le$",
                 xticks=[-0.4, 0, 0.4, 0.8], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"5": GREY_B, "50": CLASSC, "400": GOODC}
        cs = {}
        for k, c in cols.items():
            m = np.asarray(d["margins"][k])
            y = np.arange(1, len(m) + 1) / len(m)
            cs[k] = polyline(ax, np.clip(m, -0.5, 1.0), y, c, 4)
        mins = {k: min(v) for k, v in d["margins"].items()}
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.02), color=GREY_C, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the cumulative distribution of training margins", font_size=22),
            label(rf"grey: \ round 5, \ smallest {mins['5']:.2f}: \ some mistakes", font_size=22, color=GREY_B),
            label(rf"gold: \ round 50, \ smallest {mins['50']:.2f}", font_size=22, color=CLASSC),
            label(rf"green: \ round 400, \ smallest {mins['400']:.2f}", font_size=22, color=GOODC),
            label(r"the bottom moves right: \ the weakest votes firm up", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The margins themselves: the cumulative distribution of the normalized vote margin over "
            f"the training points. <bookmark mark='b'/> After five rounds, some margins are negative, mistakes, the smallest "
            f"{say(mins['5'], 2)}. <bookmark mark='c'/> After fifty, every point is correct, and the smallest margin is "
            f"{say(mins['50'], 2)}. <bookmark mark='d'/> After four hundred, {say(mins['400'], 2)}. <bookmark mark='e'/> The "
            f"bottom of the distribution moves to the right, even as the top comes in: boosting keeps working on the "
            f"examples it is least sure of, pushing their votes away from the decision boundary at the expense of the easy ones."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["5"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["50"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["400"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def compression(self):
        rows = [
            cmath(r"\text{sample compression}", r":", r"\hat h \text{ is determined by } s \text{ of the } n \text{ training points}", font_size=34),
            cmath(r"R(\hat h)", r"\le", r"\frac{1}{n - s}\Big(s\log n + \log\frac1\delta\Big) \ \ \text{if } \hat h \text{ fits the rest}", font_size=34),
            cmath(r"\text{SVM}", r":", r"s = \text{the number of support vectors}", font_size=36),
            cmath(r"\text{leave-one-out}", r":", r"E\,R \le E[\#\text{SV}]/n: \ \text{Vapnik's bound}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BOUNDC)
        whys = [why(r"Littlestone \& Warmuth (1986)"), why(r"a union bound over subsets"), why(r"the solution is sparse"), why(r"removing a non-SV changes nothing")]
        with self.voiceover(
            "<bookmark mark='a'/> The support vector machine also admits a bound with no capacity measure at all. A rule is a sample compression scheme of size s if it is determined by just s of the training points. <bookmark mark='b'/> Nick Littlestone and Manfred Warmuth showed in 1986 that if it also fits the other n minus s points, its risk is at most s log n plus log one over delta, over n minus s: a union bound over the ways of choosing the s points. <bookmark mark='c'/> For the SVM, s is the number of support vectors. <bookmark mark='d'/> And because deleting a point that is not a support vector leaves the solution unchanged, the leave-one-out error is at most the fraction of support vectors, Vapnik's bound on the expected risk."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bound(self):
        rows = [
            cmath(r"\text{for every } \gamma > 0", r":", r"P(yf(x) \le 0) \le P_n(yf(x) \le \gamma) + \frac{2}{\gamma}\mathfrak R_n(\mathcal H) + \sqrt{\tfrac{\log(1/\delta)}{2n}}", font_size=28),
            cmath(r"\mathfrak R_n(\mathrm{conv}\,\mathcal H)", r"=", r"\mathfrak R_n(\mathcal H): \ \text{voting adds no complexity}", font_size=32),
            cmath(r"\text{read}", r":", r"\text{large margins on the sample} \Rightarrow \text{small test error, \ whatever } T", font_size=32),
            cmath(r"\text{the caveat}", r":", r"\text{Breiman (1999): \ maximizing the minimum margin can hurt}", font_size=32),
        ]
        rows[0][-1].set_color(BOUNDC)
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"via contraction, \ $1/\gamma$-Lipschitz"), why(r"convex hulls"), why(r"no $T$ in the bound"), why(r"the whole distribution matters")]
        with self.voiceover(
            "<bookmark mark='a'/> The margin bound: for every margin level gamma, the test error is at most the fraction of "
            "training points with margin below gamma, plus two over gamma times the Rademacher complexity of the weak rules, "
            "plus a confidence term. The ramp loss that makes this work is one-over-gamma Lipschitz, so contraction applies. "
            "<bookmark mark='b'/> And the Rademacher complexity of a convex hull equals that of the class itself: voting "
            "adds no complexity, however many rounds are run. <bookmark mark='c'/> So large margins on the sample imply small "
            "test error, with no dependence on the number of rounds. <bookmark mark='d'/> Leo Breiman's caveat of 1999: an "
            "algorithm that maximizes the minimum margin can do worse than AdaBoost; the whole margin distribution matters."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gradient(self):
        rows = [
            cmath(r"\text{AdaBoost}", r"=", r"\text{coordinate descent on } \textstyle\sum_i e^{-y_i f(x_i)}", font_size=36),
            cmath(r"\text{its population minimizer}", r":", r"f^*(x) = \tfrac12\log\frac{\eta(x)}{1 - \eta(x)}: \ \text{half the log-odds}", font_size=32),
            cmath(r"\text{gradient boosting}", r":", r"\text{any loss: \ fit each new tree to the negative gradient}", font_size=34),
            cmath(r"\text{stopping}", r":", r"\text{shrinkage and early stopping control the complexity}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"Friedman, \ Hastie \& Tibshirani (2000)"), why(r"a statistical reading"), why(r"Friedman (2001)"), why(r"Part 34's practice")]
        with self.voiceover(
            "<bookmark mark='a'/> Statisticians read AdaBoost differently. Jerome Friedman, Trevor Hastie and Robert Tibshirani showed in 2000 that it is coordinate descent on the exponential loss, summed over the training set. <bookmark mark='b'/> The population minimizer of that loss is half the log-odds of the class probability, so boosting is fitting an additive logistic model. <bookmark mark='c'/> Friedman's gradient boosting of 2001 generalizes it to any loss, fitting each new tree to the negative gradient. <bookmark mark='d'/> And in practice its complexity is controlled by shrinkage and early stopping, a form of the stability of chapter seven."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def svm(self):
        rows = fit_rows(VGroup(
            label(r"the same idea, \ for support vector machines:", font_size=28, color=GREY_A),
            label(r"maximize the margin $\gamma$ subject to correct classification, \ $\|w\| \le 1$", font_size=26, color=CLASSC),
            label(r"generalization depends on $R^2/\gamma^2$, \ not on the dimension of the feature space", font_size=26, color=GOODC),
            label(r"so the kernel trick, \ with infinite-dimensional features, \ is safe", font_size=26, color=GOODC),
            label(r"Vapnik's insight: \ control capacity by the margin, \ not by the number of parameters", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same idea drives support vector machines. <bookmark mark='b'/> They choose the separating "
            "hyperplane with the largest margin. <bookmark mark='c'/> Their generalization depends on the ratio of the data's "
            "radius to the margin, squared, not on the dimension of the feature space. <bookmark mark='d'/> That is why the "
            "kernel trick, which maps the data into infinite-dimensional spaces, does not overfit. <bookmark mark='e'/> It was "
            "Vapnik's central insight: control capacity by the margin, not by counting parameters."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
