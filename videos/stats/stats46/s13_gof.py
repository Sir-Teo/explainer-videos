from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class GoodnessOfFit(VoiceoverScene):
    def construct(self):
        self.card()
        self.pearson()
        self.check()
        self.estimated()
        self.lilliefors()
        self.chart()
        self.durbin()
        self.board()

    def card(self):
        card = chapter_card(12, r"Goodness of fit, \ rigorously", r"Testing a whole distribution", lit=(1900, 1967), part=PART)
        with self.voiceover("Chapter twelve. Goodness of fit, rigorously: testing a whole distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pearson(self):
        rows = [
            cmath(r"(O_1, \ldots, O_k) \sim \text{Mult}(n, p)", r":", r"X^2 = \textstyle\sum_j (O_j - n p_j)^2 / (n p_j)", font_size=32),
            cmath(r"Z_j = \tfrac{O_j - n p_j}{\sqrt{n p_j}}", r"\Rightarrow", r"N(0, I - \sqrt p \sqrt p^\top)", font_size=32),
            cmath(r"I - \sqrt p \sqrt p^\top", r":", r"\text{a projection of rank } k - 1", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"X^2 = \|Z\|^2 \Rightarrow \chi^2_{k - 1}", font_size=36),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"Pearson (1900)"), why(r"the multivariate CLT"), why(r"one constraint: \ $\sum O_j = n$"), why(r"the squared length")]
        with self.voiceover(
            "<bookmark mark='a'/> Karl Pearson's statistic of 1900 adds up the squared differences between observed "
            "and expected counts, each divided by its expected count. <bookmark mark='b'/> The standardized "
            "differences are asymptotically normal, by the multivariate central limit theorem, for a fixed number of "
            "categories and fixed positive cell probabilities, with a covariance matrix equal to the identity minus "
            "the outer product of the square roots of the probabilities. <bookmark mark='c'/> That matrix is a "
            "projection, of rank k minus one, because the counts must add up to n. <bookmark mark='d'/> So Pearson's "
            "statistic, the squared length of a normal vector projected onto a k minus one dimensional space, tends "
            "to a chi-square with k minus one degrees of freedom."
        ) as vo:
            heading=label('Fixed positive multinomial probabilities give a projection CLT',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        d = load("gof")
        rows = [[r"quantile", r"50\%", r"90\%", r"95\%", r"99\%"],
                [r"$X^2$, \ simulated"] + [f"{v:.2f}" for v in d["x2_q"]],
                [r"$\chi^2_5$"] + [f"{v:.2f}" for v in d["chi2_q"]]]
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.35, colors=[GREY_A, UMPC, H0C]).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"a fair die, \ 60 rolls, \ six categories: \ 40,000 replications", font_size=24, color=GREY_A),
            label(rf"size of the nominal 5\% test: \ {100 * d['x2_size']:.1f}\%, \ with only 10 expected per cell", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Checked by simulation: sixty rolls of a fair die, six categories. <bookmark mark='b'/> The quantiles of Pearson's statistic sit on those of chi-square with five degrees of freedom, <bookmark mark='c'/> and the nominal five percent test rejects {100 * d['x2_size']:.1f} percent of the time, with only ten expected counts per cell. This example checks one balanced design; sparse cells, growing category counts, or fitted probabilities require separate conditions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated: 40,000 replications")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def estimated(self):
        rows = [
            cmath(r"p = p(\theta), \ \theta \in \mathbb R^q", r":", r"\text{estimate } \theta, \ \text{then compute } X^2", font_size=32),
            cmath(r"\hat\theta \text{ efficient grouped MLE; fixed positive cells}", r"\Rightarrow", r"\chi^2_{k - 1 - q}: \ \text{lose one df per parameter}", font_size=30),
            cmath(r"\hat\theta \text{ regular efficient ungrouped MLE}", r"\Rightarrow", r"\text{between } \chi^2_{k-1-q} \text{ and } \chi^2_{k-1}, \ \text{not } \chi^2", font_size=30),
            cmath(r"\text{the lesson}", r":", r"\text{estimating the null changes the null distribution}", font_size=32),
        ]
        rows[1][-1].set_color(UMPC)
        rows[2][-1].set_color(REJC)
        whys = [why(r"a composite null"), why(r"Fisher (1924)"), why(r"Chernoff \& Lehmann (1954)"), why(r"for every statistic")]
        with self.voiceover(
            "<bookmark mark='a'/> Usually the null is a family, not a single distribution: normal, with unknown mean "
            "and variance. We estimate the parameters and then compute the statistic. <bookmark mark='b'/> Fisher "
            "showed in 1924, against Pearson, that with efficient estimates from the grouped counts each estimated "
            "parameter costs one degree of freedom. <bookmark mark='c'/> But Chernoff and Lehmann showed in 1954 that"
            " under the regular fixed-bin model, efficient ungrouped maximum likelihood estimation generally gives a "
            "weighted chi-square limit: it lies between the chi-squares with k minus one minus q and k minus one "
            "degrees of freedom. <bookmark mark='d'/> Estimating the null changes the statistic's null distribution, "
            "a lesson that matters even more for the next test."
        ) as vo:
            heading=label('Fitting the null changes the goodness-of-fit reference law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lilliefors(self):
        d = load("gof")
        a, b = d["ks20"], d["ks100"]
        rows = [
            cmath(r"D_n", r"=", r"\sup_x |F_n(x) - \Phi((x - \bar x)/s)|", font_size=34),
            cmath(r"n = 20", r":", rf"\text{{KS table}} \ {a['crit_naive']:.3f}; \ \text{{correct}} \ {a['crit_lilliefors']:.3f}; \ \text{{size with the table}} \ {100 * a['size']:.2f}\%", font_size=28),
            cmath(r"n = 100", r":", rf"\text{{KS table}} \ {b['crit_naive']:.3f}; \ \text{{correct}} \ {b['crit_lilliefors']:.3f}; \ \text{{size}} \ {100 * b['size']:.2f}\%", font_size=28),
            cmath(r"\text{fitting brings } \Phi \text{ closer to } F_n", r"\Rightarrow", r"\text{much smaller } D_n: \ \text{the rejection threshold is too high: \ conservative test}", font_size=28),
        ]
        rows[3][-1].set_color(REJC)
        whys = [why(r"KS with estimated $\mu, \sigma$"), why(r"simulated, \ 5\%"), why(r"not a small-$n$ effect"), why(r"Lilliefors (1967)")]
        with self.voiceover(
            f"<bookmark mark='a'/> The Kolmogorov–Smirnov test of normality, with the mean and standard deviation estimated from the same data. <bookmark mark='b'/> With twenty observations the usual table's five percent critical value is {say(a['crit_naive'], 3)}; the estimated ninety-fifth percentile from forty thousand fresh normal simulations is {say(a['crit_lilliefors'], 3)}. Using the table, the simulated rejection count is extremely small; the displayed percentage has appreciable relative Monte Carlo uncertainty and is not an exact tail probability. <bookmark mark='c'/> With a hundred observations, the same: the ratio of the critical values does not improve with n. <bookmark mark='d'/> Fitting the parameters pulls the normal curve toward the data, so the distance is much smaller than for a fixed null. Hubert Lilliefors tabulated the correct values in 1967."
        ) as vo:
            heading=label('Refitting normal mean and SD needs a different KS threshold',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("gof")
        edges = np.linspace(0, 0.4, 41)
        A = axes([0, 0.4], [0, 16], x_length=7.4, y_length=4.4, xlabel=r"$D_{20}$ under the null, \ parameters estimated", ylabel=r"density",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 5, 10, 15], center=[-2.5, 0.2, 0])
        ax = A.ax
        h = hist_bars(ax, edges, np.asarray(d["D20_hist"]), color=H0C, opacity=0.75)
        c1 = DashedLine(ax.c2p(d["ks20"]["crit_lilliefors"], 0), ax.c2p(d["ks20"]["crit_lilliefors"], 15), color=UMPC, stroke_width=3)
        c2 = DashedLine(ax.c2p(d["ks20"]["crit_naive"], 0), ax.c2p(d["ks20"]["crit_naive"], 15), color=REJC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"blue: \ 40,000 values of $D_{20}$ \ with $\bar x$, $s$ estimated", font_size=22, color=H0C),
            label(rf"green: \ its 95th percentile, \ {d['ks20']['crit_lilliefors']:.3f}", font_size=22, color=UMPC),
            label(rf"red: \ the KS table's, \ {d['ks20']['crit_naive']:.3f}: \ almost never reached", font_size=22, color=REJC),
            label(r"fix: \ Lilliefors's table, \ or a parametric bootstrap", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The null distribution itself: forty thousand values of the statistic with twenty "
            "observations and the parameters estimated. <bookmark mark='b'/> In green, its correct ninety-fifth "
            "percentile. <bookmark mark='c'/> In red, the critical value from the standard table, out in the far tail, "
            "almost never reached. <bookmark mark='d'/> The fix is Lilliefors's table, or more generally a parametric "
            "bootstrap: simulate from the fitted model, refit, and recompute the statistic each time."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 40,000 normal samples")))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def durbin(self):
        rows = fit_rows(VGroup(
            label(r"why? \ \ $\sqrt n(F_n(x)-F(x))\Rightarrow B(F(x))$ for continuous $F$ \ (Part 44's Donsker)", font_size=26),
            label(r"with $\hat\theta$ plugged in: \ a different Gaussian process, \ estimator-dependent correction; \ efficient regular MLE gives a projection \ (Durbin 1973)", font_size=26, color=GREY_A),
            label(r"its law depends on the family, \ and sometimes on $\theta$: \ no universal table", font_size=26, color=REJC),
            label(r"Part 48: \ empirical processes, \ where this is proved", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The reason is a theorem about processes. for independent observations from a "
            "continuous distribution, the empirical CDF fluctuation tends to a Brownian bridge evaluated at the true "
            "CDF. The scaled Kolmogorov–Smirnov statistic tends to its supremum absolute value. <bookmark mark='b'/> "
            "With estimated parameters plugged in, James Durbin showed in 1973 that the limit is a different Gaussian"
            " process: a bridge with an estimator-dependent correction. For efficient estimators in a regular "
            "parametric model the correction has a projection interpretation; arbitrary estimators need their own "
            "influence-function calculation. <bookmark mark='c'/> Its law depends on the family, and sometimes on the"
            " parameter, so no universal table exists. <bookmark mark='d'/> Part forty-eight, on empirical processes,"
            " proves these limits."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("KS test", "pooled", "Welch", "Behrens")
        show_board(self, rows,
                   "<bookmark mark='a'/> Two sets of Board rows. The Kolmogorov–Smirnov test with the usual table and estimated "
                   "parameters: size essentially zero, conservative. <bookmark mark='b'/> And from the hook, Behrens and "
                   "Fisher's problem with a small, noisy first sample: the pooled t test rejects a true null thirty percent "
                   "of the time, broken; Welch's and Behrens–Fisher's tests stay near five percent, kept.",
                   [("a", [3]), ("b", [0, 1, 2])])
