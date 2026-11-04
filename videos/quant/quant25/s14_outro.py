from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, PCA_C, RP_C, SDF, TRUE, load

DESK = [
    (r"200 strategies, all noise. What is the expected best $t$-statistic?",
     r"about 2.8 (about 3.0 if losing strategies may be flipped into shorts), with a 5--95\% range of roughly 2.2 to 3.5: "
     r"the maximum of $n$ near-normal draws grows like $\sqrt{2\ln n}$"),
    (r"You report the best of 200, with $t = 2.9$. Its honest $p$-value?",
     r"$1 - \Phi(2.9)^{200} \approx 0.31$ if the 200 are independent: nothing. Computing it needs the number of tries and "
     r"their dependence, which only the researcher knows"),
    (r"100 candidate signals; you will trade the ten best equally. Which error rate?",
     r"the false discovery rate, at perhaps 10\%: a dud among ten dilutes the book rather than ruining it. FWER is for "
     r"single claims"),
    (r"An anomaly: $t = 4$ equal-weighted, $t = 1.2$ value-weighted with NYSE breakpoints. Real? Trade it?",
     r"real in microcaps, perhaps; tradable at scale, probably not. Size it to the capacity of the stocks that carry it, "
     r"after costs, or leave it"),
    (r"A new paper: $t = 3.5$, 0.8\% a month. What do you plan for, from next year?",
     r"a third to a half: 0.3--0.4\% a month before costs, the post-publication record of the zoo"),
    (r"A new factor has $t = 5$ alone but an insignificant SDF loading after double selection. Hold it?",
     r"only as a cheaper or better-implemented way to hold the factors that span it; it adds no new premium"),
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
    r"A weak factor: true betas have variance 0.01 across assets, estimation noise 0.04. By what factor is the "
    r"two-pass premium attenuated?",
    r"Model A's factors reach $SR^2 = 0.5$ a year, model B's 0.8. Which is better by Barillas--Shanken, and why are no "
    r"test assets needed?",
    r"A data miner tries 29{,}000 signals with no true premium. How many clear $|t| > 2$ by chance? $|t| > 3$?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("noise"), load("zoo"), load("mtest"), load("shrink"), load("kns"), load("pca"), load("fgx"),
                   load("models"), load("envelope"))
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

    def recap(self, n, z, m, s, k, p, f, mo, e):
        items = [
            (rf"200 noise strategies: best $t \approx {n['rows'][6]['mean']:.1f}$; the best of $n$ grows like "
             r"$\sqrt{2 \ln n}$", NOISE),
            (rf"{z['n']} predictors by 2016; the Bonferroni hurdle {z['hurdle'][-1]:.2f}; Harvey--Liu--Zhu: $t > 3$", HURDLE),
            (rf"after publication: {m['post']['raw']} significant, {m['post']['bh']} by FDR, {m['post']['bonferroni']} by "
             r"Bonferroni", BAD),
            (r"replication: 65\% fail (Hou--Xue--Zhang), most replicate (Jensen--Kelly--Pedersen); construction decides",
             GOOD),
            (rf"decay: noise alone keeps {100 * s['eb']['shrink']:.0f}\%, the record {100 * s['ratio']:.0f}\%", SDF),
            (r"mined signals do as well as published ones: about half survives in both", NOISE),
            (rf"shrinkage SDF: cross-validated $R^2$ peaks at $\kappa \approx {k['best_kappa']:.1f}$; optimised "
             r"portfolios give back the most", SDF),
        ]
        items2 = [
            (rf"double selection: {f['sig_ds']} of {f['n_new']} new factors add to the zoo", TRUE),
            (r"weak factors: two-pass premia not identified; three-pass via PCA", BAD),
            (rf"RP-PCA beats PCA out of sample: K = 5, Sharpe {p['rp'][4]['sr_out']:.1f} against {p['pca'][4]['sr_out']:.1f}",
             RP_C),
            (r"IPCA: betas from characteristics; characteristics are covariances", PCA_C),
            (rf"models ranked by $SR^2$: rank correlation {mo['rank_corr']:.2f} in to out; average, do not crown", GOOD),
            (rf"the SDF opened: Sharpe {e['rows']['kns_sdf_part25']['holdout']['sharpe']:.1f} in 2021--23, on paper; "
             rf"counter {e['trials']}", SDF),
            (r"Rule 25: the count, the hurdle, the library, the shrinkage, the discount", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 25 in fourteen lines")
        with self.voiceover(
            "Part twenty-five in fourteen lines. Two hundred noise strategies produce a best t-statistic near three, "
            "because the best of many grows with the square root of the log of the number. The zoo passed two hundred "
            "predictors, and its own Bonferroni hurdle rose to three point seven; Harvey, Liu and Zhu asked for three. "
            "After publication, a quarter of the predictors are significant one by one, an eighth survive the false "
            "discovery rate, and seven survive Bonferroni. Whether the zoo replicates depends on how it is rebuilt. "
            "Noise alone would leave predictors most of their strength; the record left a bit over a third. Mined "
            "signals held up as well as published ones. And the shrinkage discount factor fits best out of sample at "
            "moderate shrinkage."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 25 in fourteen lines")
        with self.voiceover(
            "Double selection finds that most new factors add nothing to the zoo. Weak factors have premia the "
            "two-pass regression cannot identify. Risk-premium PCA finds the directions that pay, and plain PCA does "
            "not. Instrumented PCA lets betas move with characteristics. Models are best compared by the Sharpe ratio "
            "their factors reach, and the near-ties at the top are best averaged. The shrinkage discount factor kept "
            "most of its paper performance on three unseen years. And the House's rule: count, clear the hurdle the "
            "count implies, test against the library, shrink, and discount what is published."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a, width=12.4, font_size=22) for q, a in qs]).arrange(DOWN, buff=0.25)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Two hundred noise strategies: expect a best t of about two point eight, or three if "
            "losers may be flipped. <bookmark mark='a'/> Report the best of two hundred at two point nine, and its "
            "honest p-value is about three tenths. <bookmark mark='b'/> Trading the ten best of a hundred signals calls "
            "for the false discovery rate: a dud among ten dilutes rather than ruins."
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
            "An anomaly that lives in equal-weighted microcaps may be real and still untradable at scale. "
            "<bookmark mark='a'/> A new paper's eight tenths of a percent a month should be planned at a third to a "
            "half of that. <bookmark mark='b'/> And a factor spanned by the library is worth holding only as a cheaper "
            "way to hold what spans it. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "And ten problems: the distribution of the best of n; Bonferroni for the zoo; three procedures on five "
            "p-values; empirical-Bayes shrinkage; ridge in principal components, and which direction it distrusts; "
            "RP-PCA's special case; the attenuation of a weak factor; Barillas and Shanken's comparison; and what a "
            "data miner finds by chance. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
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
            "labelled as such."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 26, Backtesting Without Fooling Yourself", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The research desk has a factor library, a discount-factor model and a count of its own trials. "
            "<bookmark mark='a'/> Next, Part twenty-six: backtesting without fooling yourself. Every way a backtest "
            "lies, each with a planted error to find; costs, funding and borrow; and the deflated Sharpe ratio."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
