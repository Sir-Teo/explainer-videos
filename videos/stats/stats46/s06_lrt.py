from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class LRT(VoiceoverScene):
    def construct(self):
        self.card()
        self.wilks()
        self.check()
        self.chernoff()
        self.boundary()
        self.failures()

    def card(self):
        card = chapter_card(5, r"The likelihood ratio test", r"Wilks's theorem, \ and where it breaks", lit=(1938, 1954), part=PART)
        with self.voiceover("Chapter five. The likelihood ratio test: Wilks's theorem, and where it breaks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def wilks(self):
        rows = [
            cmath(r"\Lambda", r"=", r"\sup_{\Theta_0} L(\theta) \,/\, \sup_{\Theta} L(\theta)", font_size=36),
            cmath(r"\ell(\theta_0) - \ell(\hat\theta)", r"\approx", r"-\tfrac12 (\hat\theta - \theta_0)^\top I_n (\hat\theta - \theta_0)", font_size=32),
            cmath(r"\sqrt n(\hat\theta - \theta_0)", r"\Rightarrow", r"N(0, I^{-1}) \ \Rightarrow \ -2\log\Lambda \Rightarrow \chi^2_q", font_size=32),
            cmath(r"\text{needs}", r":", r"\theta_0 \text{ interior, \ smooth, \ identifiable; \ } q = \dim\Theta - \dim\Theta_0", font_size=30),
        ]
        rows[2][-1].set_color(UMPC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"a ratio of maxima"), why(r"Taylor at the MLE"), why(r"Wilks (1938)"), why(r"the conditions matter")]
        with self.voiceover(
            "<bookmark mark='a'/> When no optimal test exists, the likelihood ratio test is the general-purpose answer: "
            "the best likelihood under the null over the best likelihood overall. <bookmark mark='b'/> Expanding the "
            "log-likelihood around the maximum, the drop to the null value is half a quadratic form in the estimation "
            "error, weighted by the information. <bookmark mark='c'/> Since the scaled error is asymptotically normal with "
            "covariance the inverse information, minus twice the log ratio tends to a chi-square, with degrees of freedom "
            "equal to the number of constraints. That is Samuel Wilks's theorem of 1938. <bookmark mark='d'/> Every step "
            "used something: the true value must be interior, the model smooth and identifiable. Part forty-seven proves it "
            "properly; here we watch the conditions fail."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        d = load("lrt")
        q, c = d["wilks_q"], d["chi2_q"]
        rows = [[r"quantile", r"50\%", r"90\%", r"95\%", r"99\%"],
                [r"$-2\log\Lambda$, \ simulated"] + [f"{v:.2f}" for v in q],
                [r"$\chi^2_1$"] + [f"{v:.2f}" for v in c]]
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.35, colors=[GREY_A, UMPC, H0C]).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"Poisson rate, \ $n = 10$, \ $\lambda_0 = 2$: \ 40,000 data sets", font_size=24, color=GREY_A),
            label(rf"size of the nominal 5\% test: \ {100 * d['wilks_size']:.1f}\% \ (the counts are discrete)", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> First, a case where everything holds. Ten Poisson counts, testing a rate of two. "
            f"<bookmark mark='b'/> The simulated quantiles of minus twice the log ratio sit close to the chi-square with "
            f"one degree of freedom. <bookmark mark='c'/> The nominal five percent test rejects {100 * d['wilks_size']:.1f} "
            f"percent of the time; the difference comes from the discreteness of the counts, not from the theory."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated: 40,000 data sets")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def chernoff(self):
        rows = [
            cmath(r"Z \sim N(\mu, 1)", r",", r"\ H_0: \mu = 0 \ \ \text{vs} \ \ \mu > 0 \ \ (\Theta = [0, \infty))", font_size=32),
            cmath(r"\hat\mu", r"=", r"\max(0, Z) \ \Rightarrow \ -2\log\Lambda = \max(0, Z)^2", font_size=34),
            cmath(r"\text{under } H_0", r":", r"\tfrac12 \chi^2_0 + \tfrac12 \chi^2_1: \ \text{a point mass at 0, \ half the time}", font_size=30),
            cmath(r"5\% \text{ critical value}", r":", r"\chi^2_{1, 0.90} = 2.71, \ \text{not } 3.84", font_size=34),
        ]
        rows[2][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(UMPC)
        whys = [why(r"the null on the boundary"), why(r"the MLE sticks at 0"), why(r"Chernoff (1954)"), why(r"halve the p-value")]
        with self.voiceover(
            "<bookmark mark='a'/> Now put the null value on the edge of the parameter space: a normal mean that cannot be "
            "negative, tested at zero. <bookmark mark='b'/> The maximum likelihood estimate is Z when Z is positive and zero "
            "otherwise, so minus twice the log ratio is the positive part of Z, squared. <bookmark mark='c'/> Under the null "
            "that is zero half the time and a chi-square with one degree of freedom the other half: Herman Chernoff's "
            "mixture of 1954. <bookmark mark='d'/> The correct five percent critical value is the ninetieth percentile of "
            "chi-square one, two point seven one, not three point eight four."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def boundary(self):
        d = load("lrt")
        rows = fit_rows(VGroup(
            label(rf"simulated under $H_0$: \ $-2\log\Lambda = 0$ in {100 * d['zero_share']:.1f}\% of data sets", font_size=28),
            label(rf"with the $\chi^2_1$ critical value 3.84: \ size {100 * d['naive_size']:.1f}\% \ (conservative)", font_size=28, color=REJC),
            label(rf"with the mixture's 2.71: \ size {100 * d['chibar_size']:.1f}\%", font_size=28, color=UMPC),
            label(r"Self \& Liang (1987): \ $\bar\chi^2$ mixtures for boundaries in general", font_size=26, color=GREY_A),
            label(r"Part 25's variance components: \ testing $\tau^2 = 0$ is exactly this case", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Simulated, the statistic is exactly zero in half the data sets. <bookmark mark='b'/> "
            f"Using the chi-square critical value anyway gives a test of size {100 * d['naive_size']:.1f} percent: valid, "
            f"but conservative, wasting power. <bookmark mark='c'/> The mixture's critical value restores five percent. "
            f"<bookmark mark='d'/> Steven Self and Kung-Yee Liang worked out the general mixtures of chi-squares for "
            f"parameters on boundaries in 1987. <bookmark mark='e'/> The everyday case is Part twenty-five's test that a "
            f"variance component is zero, where the usual remedy is to halve the chi-square p-value."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def failures(self):
        rows = fit_rows(VGroup(
            label(r"when Wilks fails outright:", font_size=28, color=GREY_A),
            label(r"the number of mixture components: \ a parameter vanishes under $H_0$; \ $-2\log\Lambda \to \infty$ slowly (Hartigan 1985)", font_size=24, color=REJC),
            label(r"a change point, \ a threshold: \ the null leaves a parameter unidentified \ (Davies 1977)", font_size=24, color=REJC),
            label(r"many parameters: \ $q$ growing with $n$, \ the Bartlett correction and beyond \ (Part 59)", font_size=24, color=REJC),
            label(r"the remedies: \ parametric bootstrap of $\Lambda$, \ or a test built for the geometry", font_size=26, color=UMPC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And sometimes Wilks fails outright. <bookmark mark='b'/> Testing one mixture component "
            "against two: under the null, the second component's location is not identified, and the statistic grows "
            "without bound, slowly, as John Hartigan showed. <bookmark mark='c'/> Change points and thresholds have the same "
            "disease, studied by Robert Davies. <bookmark mark='d'/> And when the number of constraints grows with the sample "
            "size, the chi-square approximation drifts, the subject of Part fifty-nine. <bookmark mark='e'/> The practical "
            "remedies are to simulate the statistic's null distribution by a parametric bootstrap, or to build a test that "
            "respects the geometry of the problem."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
