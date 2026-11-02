from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load

DESK = [
    (r"A strategy has a Sharpe ratio of 1 over 4 years. What is the standard error?",
     r"about 0.6: $\sqrt{(1 + SR^2/2)/T} = \sqrt{1.5/4} \approx 0.61$; the 95\% interval runs from about $-0.2$ to $2.2$"),
    (r"You tested 20 strategies and the best has $p = 0.03$. Is it significant?",
     r"no: with 20 tries, Bonferroni needs $p < 0.0025$; even ignoring correlation, the chance that one of 20 null "
     r"strategies reaches $p < 0.03$ is $1 - 0.97^{20} \approx 46\%$"),
    (r"You regress annual returns, sampled monthly, on a predictor over 40 years. How many observations do you have?",
     r"about 40, not 480: neighbouring annual returns share 11 of 12 months; use Newey--West or Hansen--Hodrick errors, "
     r"and still distrust $t \approx 2$"),
]

PROBLEMS = [
    r"For $h$-month sums of iid returns regressed on a slowly moving predictor, show that the naive standard "
    r"error understates the true one by roughly $\sqrt{h}$.",
    r"Starting from Kendall's bias $\mathbb{E}[\hat\rho - \rho] \approx -(1 + 3\rho)/T$, derive Stambaugh's bias in the "
    r"predictive slope. Evaluate it for $\rho = 0.91$, corr$(u, v) = -0.83$, $T = 149$.",
    r"Derive the standard error of a Sharpe ratio from iid normal returns by the delta method.",
    r"Show that Holm's procedure controls the family-wise error rate and rejects at least as much as Bonferroni.",
    r"For $k \ge 3$ means $x_i \sim N(\mu_i, 1)$, show that $(1 - (k - 2)/\|x\|^2)\,x$ has lower total squared error "
    r"than $x$ (James--Stein), and explain why shrinking toward the grand mean needs $k \ge 4$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.o = load("overlap")
        self.g = load("gmm")
        self.e = load("event")
        self.b = load("bootstrap")
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        o, g, e, b = self.o, self.g, self.e, self.b
        items = [
            (rf"overlapping returns: the dividend yield's naive $t$ of {o['est']['naive']['t']:.0f} is "
             rf"{o['est']['nw']['t']:.1f} with Newey--West", BAD),
            (rf"even corrected, a persistent predictor rejects a true null {100 * o['size']['nw']:.0f}\% of the time; "
             r"Stambaugh's bias inflates the slope", BAD),
            (rf"GMM: the consumption Euler equation is rejected ($p = {g['p_J']:.4f}$); risk aversion would need to be "
             rf"about {g['hj_gamma']:.0f}", EST),
            (rf"the turn of the month: {100 * e['1926-1986']['share_of_return']:.0f}\% of returns in 18\% of days, "
             rf"{100 * e['1987-2020']['share_of_return']:.0f}\% after publication", DATA_C),
            (r"panels: cluster by the common shock; Fama--MacBeth and pooled OLS answer different questions", ALT),
            (rf"the market's Sharpe ratio, {b['sr_a']:.2f}, has a standard error of {b['se_block']:.2f} after 94 years; "
             r"a Sharpe of 0.5 needs 16 years", EST),
            (r"shrinking 40 industry means to one number halved the forecast error; no industry alpha survives "
             r"multiple testing", GOOD),
            (r"causal questions need designs: instruments, differences, discontinuities, double ML", GOOD),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=c), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 6 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part six in eight lines. Overlapping returns turned a t-statistic of fifteen into one under three. Even "
            "corrected standard errors over-reject with a persistent predictor, and Stambaugh's bias inflates the "
            "slope. GMM rejects the consumption Euler equation, which would need a risk aversion in the hundreds. "
            "The turn of the month carried most of the market's return before it was published, and less after. "
            "In panels, cluster by the shock that is common, and know which question your estimator answers. After "
            "ninety-four years the market's Sharpe ratio is known only to within a quarter, and a good strategy "
            "needs sixteen years to prove itself. Shrinkage beat forty separate estimates, and no industry alpha "
            "survived multiple testing. And causal questions need designs, not just regressions."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A Sharpe ratio of one over four years has a standard error of about zero point "
            "six: the true value could be anywhere from below zero to above two. <bookmark mark='a'/> If you tested "
            "twenty strategies and the best has a p-value of three percent, it is not significant: nearly half the "
            "time, one of twenty worthless strategies would do as well. <bookmark mark='b'/> And forty years of "
            "annual returns sampled monthly are about forty observations, not four hundred and eighty. Full "
            "solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: the cost of overlap, Stambaugh's bias derived, the Sharpe ratio's standard error, "
            "Holm against Bonferroni, and the James-Stein estimator. Solutions, in English and Chinese, are in the "
            "notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GMM and the stochastic discount factor", [23]),
            (r"Fama--MacBeth, clustering and factors", [24, 25]),
            (r"multiple testing and the trial counter", [25, 26, 43]),
            (r"shrinkage and estimation error", [27, 30]),
            (r"double ML and causal machine learning", [27, 28]),
        ])
        with self.voiceover(
            "Where this comes back. GMM and the Euler equation become the stochastic discount factor of Part "
            "twenty-three. Fama-MacBeth and clustering are the workhorses of the factor parts, twenty-four and "
            "twenty-five, which also apply multiple testing to the factor zoo, as the backtesting part and the finale "
            "do to everything the House tries. Shrinkage returns in machine learning and in portfolio construction, "
            "and double machine learning in the parts on learning from returns and from text."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Campbell, Lo and MacKinlay, \textit{The Econometrics of Financial Markets}, ch.\ 3--4, 7",
             r"Cochrane, \textit{Asset Pricing}, part II; Hayashi, \textit{Econometrics}, ch.\ 3, 6",
             r"Bali, Engle and Murray, \textit{Empirical Asset Pricing: The Cross Section of Stock Returns}",
             r"Efron and Hastie, \textit{Computer Age Statistical Inference}, ch.\ 7, 15"],
            [r"Newey and West (1987); Hansen and Hodrick (1980); Stambaugh (1999); Hansen (1982); Hansen and Singleton (1982)",
             r"Mehra and Prescott (1985); MacKinlay (1997); Ariel (1987); Petersen (2009); Fama and MacBeth (1973)",
             r"Lo (2002); Politis and Romano (1994); James and Stein (1961); Benjamini and Hochberg (1995)",
             r"Moskowitz and Grinblatt (1999); Chernozhukov et al.\ (2018); Cameron, Gelbach and Miller (2011)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code from public data: Robert Shiller's century and a half of the market, Kenneth French's "
            "factors and industries, and consumption and prices from the St. Louis Fed."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 7, Time Series and Volatility", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now say how sure it is. <bookmark mark='a'/> Next, Part seven: time series and volatility. "
            "ARMA models, GARCH and its many children, and forecasts of volatility from the realized variance we "
            "measured in Part five."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
