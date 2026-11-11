from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, PCA_C, RP_C, SDF, TRUE, load

DESK = [
    (r"200 strategies, all noise. What is the expected best $t$-statistic?",
     r"about 2.8 (about 3.0 if losing strategies may be flipped into shorts), with a 5--95\% range of roughly 2.2 to 3.5: "
     r"the maximum of $n$ near-normal draws grows like $\sqrt{2\ln n}$"),
    (r"You report the best of 200, with $t = 2.9$. Its honest $p$-value?",
     '$1-\\Phi(2.9)^{200}\\approx0.31$ under independent standard-normal nulls; actual calibration needs the declared search family, null model and dependence'),
    (r"100 candidate signals; you will trade the ten best equally. Which error rate?",
     'choose a declared discovery-error objective; FDR controls an expectation under assumptions, not realised losses or portfolio safety'),
    (r"An anomaly: $t = 4$ equal-weighted, $t = 1.2$ value-weighted with NYSE breakpoints. Real? Trade it?",
     r"real in microcaps, perhaps; tradable at scale, probably not. Size it to the capacity of the stocks that carry it, "
     r"after costs, or leave it"),
    (r"A new paper: $t = 3.5$, 0.8\% a month. What do you plan for, from next year?",
     '0.3--0.4\\% is a sensitivity scenario only, not a calibrated forecast; selection, uncertainty and implementation matter'),
    (r"A new factor has $t = 5$ alone but an insignificant SDF loading after double selection. Hold it?",
     'nonrejection does not establish spanning or no value; inspect power, weak identification, covariance error and implementation'),
]

PROBLEMS = [
    r"Show that $\Pr(\max_{i \le n} Z_i \le c) = \Phi(c)^n$ for independent standard normals, and that the median "
    r"maximum solves $\Phi(c) = 2^{-1/n}$. Find it for $n = 200$.",
    r"Bonferroni for $m = 212$ two-sided tests at 5\%: find the $p$ and $|t|$ hurdles.",
    r"$p$-values 0.001, 0.008, 0.012, 0.03, 0.2 ($m = 5$, 5\%). How many rejections by Bonferroni, Holm, and "
    r"Benjamini--Hochberg?",
    r"Empirical Bayes: the zoo's $t$'s have mean 4 and variance 6. Shrink $t = 7$.",
    r"Show that $(\Sigma + \gamma I)^{-1}\mu = \sum_k \frac{\lambda_k}{\lambda_k + \gamma}\frac{q_k^\top\mu}{\lambda_k}q_k$.",
    r"Two principal components with variances 0.01 and 0.0001 and projected means 0.002 each. Find the unshrunk and "
    r"the $\gamma = 0.001$ loadings. Which direction does shrinkage distrust?",
    r"Show that RP-PCA with $\gamma = -1$ is PCA of the (biased) sample covariance.",
    'In a classical EIV illustration with independent additive beta error, true-beta variance 0.01 and error variance 0.04: find the attenuation factor. Why is this not a general two-pass identity?',
    r"Model A's factors reach $SR^2 = 0.5$ a year, model B's 0.8. Which is better by Barillas--Shanken, and why are no "
    r"test assets needed?",
    'A miner tries 29{,}000 hypotheses with standard-normal null statistics. Find expected counts with $|Z|>2$ and $|Z|>3$. Do these expectations require independent tests?',
    "(qual) For independent $p$-values with exactly uniform true-null distributions, prove that Benjamini--Hochberg at level $q$ has $\\mathrm{FDR} = \\pi_0 q$ exactly. Hint: $V/R = \\sum_{i \\in H_0} 1\\{p_i \\le qR/m\\}/R$; condition on the other $p$'s.",
    '(qual) Show the UNTRUNCATED Storey estimator satisfies $\\mathbb E\\hat\\pi_0(\\lambda)\\ge\\pi_0$ for uniform null p-values; explain why clipping at one can change this. Then, in the two-group model, show that the tail-area rate $\\pi_0\\bar\\Phi(z)/\\bar F(z)$ equals $\\mathbb E[\\operatorname{lfdr}(Z) \\mid Z \\ge z]$.',
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("noise"), load("zoo"), load("mtest"), load("shrink"), load("kns"), load("pca"), load("fgx"),
                   load("models"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, n, z, m, s, k, p, f, mo):
        items = [
            (r"Noise maxima grow with the search count; normal asymptotics are approximations", NOISE),
            (rf"{z['n']} published predictors; a selected collection, not the full search family", HURDLE),
            (rf"Post-publication counts: raw {m['post']['raw']}, BH {m['post']['bh']}, Bonferroni {m['post']['bonferroni']}; validity conditional", BAD),
            (r"Replication depends on construction, universe, data vintage and sample", GOOD),
            (rf"Distinct diagnostics: EB slope {s['eb']['shrink']:.2f}; mean-return ratio {s['ratio']:.2f}", SDF),
            (r"Published mining comparisons do not identify a universal future retention rate", NOISE),
            (r"Ridge CV uses future folds; full-window tuning is not independent split validation", SDF),
        ]
        items2 = [
            (rf"Simplified DS: {f['sig_ds']} of {f['n_new']} nominal loading t crossings; heuristic inference", TRUE),
            (r"Weak factor loadings threaten identification and two-pass inference", BAD),
            (r"PCA/RP-PCA split uses a complete-history universe selected through 2023", RP_C),
            (r"IPCA models conditional betas; characteristics are not literally covariances", PCA_C),
            (rf"{mo['n_models']} candidate models; selected later-window leaders require fresh evidence", GOOD),
            (r"Registration and short-sample precision; sealed experiment unopened", SDF),
            (r"Rule 25: count, calibrate, disclose selection, shrink conditionally", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 25 in fourteen lines")
        with self.voiceover("Fourteen lessons. Search changes the distribution of the best result. Error-control procedures need valid null p-values and their stated dependence conditions. Published predictors are a selected universe, and modern reconstructions are not historical vintages. Replication depends on construction. The empirical-Bayes slope and observed return-retention ratio are different diagnostics, not a causal decomposition. Published mining comparisons do not deliver a universal forecast. The saved shrinkage cross-validation uses future folds and evaluation-window information, so the split is retrospective."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6, run_time=15))
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 25 in fourteen lines")
        with self.voiceover("The simplified double-selection t values are heuristic, and nonrejection does not prove exact spanning. Weak factor exposures undermine identification. PCA comparisons inherit complete-history and publication selection. IPCA models conditional betas rather than making characteristics literally equal to covariances. Traded-factor model comparison is conditional mean-variance geometry; choosing a later-window winner uses that window. Registration cannot make previously examined history fresh, and three years gives little precision. The sealed experiment remains unopened. Count choices, state assumptions, disclose inherited selection, and shrink conditionally."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6, run_time=15))
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=22) for q, a in qs]).arrange(DOWN, buff=0.25)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. The expected maximum depends on the declared noise model, horizon and search count. <bookmark mark='a'/> The standard-normal independent maximum gives a selected p-value near three tenths for a best t of two point nine among two hundred; unknown search and dependence change calibration. <bookmark mark='b'/> FDR controls an expected false-rejection fraction under assumptions. It does not cap realised false discoveries, portfolio loss, common exposures or funding risk."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "A microcap result needs uncertainty, liquidity and cost analysis before it is an implementable premium. <bookmark mark='a'/> Retaining one third to one half of a published return can be a sensitivity scenario, not a universal calibrated forecast. <bookmark mark='b'/> An insignificant simplified SDF loading does not prove exact spanning or no incremental value. Assess power, identification, estimation error and implementation. All six worked answers remain in the bilingual notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        def page(start, end):
            ps = problem_set(PROBLEMS[start:end], font_size=22)
            for number, row in enumerate(ps.rows, start + 1):
                old_number = row[0]
                new_number = label(rf"{number}.", font_size=22, color=old_number.get_color())
                new_number.match_height(old_number).move_to(old_number).align_to(old_number, RIGHT)
                old_number.become(new_number)
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=3))
            self.wait(2)
        with self.voiceover("The first six problems: normal maxima, Bonferroni under normal null calibration, three corrections by hand, the conditional normal-normal posterior, ridge in principal components, and two numerical directions. State positive eigenvalues and the assumed units."):
            page(0, 6)
        self.clear_scene()
        with self.voiceover("Problems seven through ten: the centered covariance convention in RP-PCA, classical independent errors-in-variables attenuation, conditional traded-factor mean-variance comparison, and expected noise discoveries. The attenuation formula is not a general two-pass identity; expected counts do not require independent tests when marginal probabilities are fixed."):
            page(6, 10)
        self.clear_scene()
        with self.voiceover("Two qualifying problems: prove exact BH false-discovery equality for independent tests with uniform true-null p-values. Then prove the expectation bound for the untruncated Storey estimator and the conditional two-group tail-area identity. Clipping changes the first claim. All twelve worked solutions are retained in English and Chinese."):
            page(10, 12)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the trial counter in every backtest; the deflated Sharpe ratio", [26]),
            (r"characteristics into machine-learned SDFs and expected returns", [27]),
            (r"alpha miners that try millions of signals, deflated by the count", [29]),
            (r"the SDF's weights as a portfolio, with costs and constraints", [30]),
            (r"the finale: every row deflated by the series' full count", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-six puts the trial counter into every backtest and turns it into a "
            "deflated Sharpe ratio. Part twenty-seven feeds the characteristics to machine-learned discount factors. "
            "Part twenty-nine's alpha miners try millions of signals and are deflated by the count. Part thirty turns "
            "the discount factor's weights into a portfolio with costs and constraints. And the finale deflates every "
            "row by the series' full count."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kelly and Xiu, \textit{Financial Machine Learning}; Bali, Engle and Murray, \textit{Empirical Asset Pricing}; "
             r"Efron, \textit{Large-Scale Inference}; Cochrane, \textit{Asset Pricing}"],
            [r"Holm (1979); Benjamini and Hochberg (1995); Kan and Zhang (1999); White (2000); Romano and Wolf (2005); "
             r"Kleibergen (2009); Lewellen, Nagel and Shanken (2010); Cochrane (2011); Belloni, Chernozhukov and Hansen "
             r"(2014); Harvey, Liu and Zhu (2016); McLean and Pontiff (2016); Harvey (2017); Yan and Zheng (2017); Barillas "
             r"and Shanken (2017, 2018)",
             r"Kelly, Pruitt and Su (2019); Kozak, Nagel and Santosh (2020); Feng, Giglio and Xiu (2020); Hou, Xue and Zhang "
             r"(2020); Lettau and Pelger (2020); Chen and Zimmermann (2020, 2022); Harvey and Liu (2020); Giglio and Xiu "
             r"(2021); Jensen, Kelly and Pedersen (2023); Bryzgalova, Huang and Julliard (2023); Chen, Lopez-Lira and "
             r"Zimmermann (working paper); Giglio, Xiu and Zhang (test assets and weak factors). Data: Open Source Asset "
             r"Pricing 2024.10; Kenneth French; global-q.org"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Holm's step-down test to the replication "
            "debate. Every number on screen was computed by the House's code from public data, with simulations "
            "labelled as such. The predictors' returns are Chen and Zimmermann's open-source release, which anyone can "
            "download and check against these numbers."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 26, Backtesting Without Fooling Yourself", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The research desk now has a factor library, a conditional discount-factor model and its local trial ledger. Search makes the best result optimistic, and published histories inherit selection. Shrinkage is a disciplined conditional estimate, not a guarantee that a portfolio is feasible or a predictor is real. <bookmark mark='a'/> Next, Part twenty-six examines backtesting choices, planted errors, costs, funding, borrow and the assumptions behind a deflated Sharpe ratio."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
