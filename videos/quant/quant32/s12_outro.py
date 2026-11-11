from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import GOOD, PART, TREND_C

DESK = [
    (r"What does the quadratic trend identity establish?",
     r"for the stated reset linear rule, $P=(S^2-Q)/2$; no literal straddle replication or guaranteed crisis profit"),
    (r"Where can its expected profit come from?",
     r"stationary drift and lag covariances: $\mathbb E[P]=\binom n2\mu^2+\sum_k(n-k)\gamma_k$; costs still matter"),
    (r"Does inverse volatility always equalise risk contributions?",
     r"for two assets under the stated covariance convention; not for general multi-group Euler contributions"),
    (r"Does a volatility target guarantee realised risk?",
     r"no: exposure uses a lagged forecast and cap; forecast error and covariance changes alter risk"),
    (r"What is known from the two published series?",
     r"sample AQR style and Cboe PUT summaries, with provider construction and measurement conventions"),
    (r"What should an income fund disclose?",
     r"option and equity exposures, tail losses, event dates, collateral, funding, execution and fees"),
]

PROBLEMS = [
    r"Basic 1. Chosen stock/bond SDs 20\%/10\%, rho=0, weights 60/40: stocks' Euler risk fraction?",
    r"Basic 2. Same SDs, rho=-.2: inverse-vol weights, base SD and scale to target SD 10\%?",
    r"Basic 3. Four equal-vol styles each SR=.6: equal-weight SR at average rho=0 and .3?",
    r"Basic 4. Target SD 10\%, forecast 10\%, true conditional SD 20\%, cap 3: exposure and risk?",
    r"Basic 5. Fifty months at +1\%, then one at -30\%: arithmetic mean, skew sign and compound return?",
    r"Basic 6. Linear annual gross budget 10\%, 504 equally charged trade legs: break-even bp per leg?",
    r"Advanced 7. Independent increments with mean mu: derive E[P] for the reset linear rule.",
    r"Advanced 8. iid zero-mean Gaussian blocks, n=63: skew; then K=23 independent identical blocks' skew.",
    r"Advanced 9. With SE(SR) approx 1/sqrt(T), true annual SR=.3: years for signal / SE =2?",
    r"Advanced 10. Known $\sigma=.1$ or $.2$ equally likely, $\mu=\sigma^2$, $r=\mu+\sigma\epsilon$: "
    r"compare unconditional SR before/after x=.1/sigma; derive the conditional mean-variance optimum.",
    r"Qual 11. iid $N(0,1)$: prove $\mathbb E[Y^2]=\binom n2$, $\mathbb E[Y^3]=n(n-1)(n-2)$; derive exact chi-square law and weak limit.",
    r"Qual 12. Fixed lag filter $P_w=\sum_{s<t}w_{t-s}r_s r_t$: stationary mean, iid zero-mean variance; "
    r"derive the matched filter against specified zero-mean autocovariances using that variance reference.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        rows = VGroup(
            label(r"linear trend: exact path identity; drift and dependence determine its mean", font_size=25),
            label(r"volatility targeting: forecast, cap, financing and timing determine exposure", font_size=25),
            label(r"risk parity: covariance and risk-contribution definitions matter", font_size=25),
            label(r"carry: unchanged-price component, not a guaranteed premium", font_size=25),
            label(r"published styles and PUT: sample evidence with construction limits", font_size=25),
            label(r"calendar rules: exact accounting, costs and multiple testing", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        head = label(r"Part 32: what each claim needs", font_size=33).to_edge(UP)
        self.play(FadeIn(head), FadeIn(rows[0]))
        with self.voiceover(
            "Part thirty-two separates mechanism, mathematical identity and empirical evidence. "
            "The reset linear trend rule has an exact path identity; drift and dependence "
            "determine its mean, while Gaussian assumptions determine the stated finite-block "
            "distribution. <bookmark mark='a'/> A volatility target needs a forecast, and "
            "risk budgeting needs a covariance convention. Carry is an unchanged-price "
            "component rather than a guaranteed premium. <bookmark mark='b'/> The published "
            "style and put-writing series supply sample evidence under their construction "
            "and measurement conventions. Calendar accounting is exact only for its stated "
            "prices, and a trading claim must survive costs and selection. These conclusions "
            "do not establish an allocation verdict for an unmeasured strategy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=19) for q, a in DESK[:3]]
                       ).arrange(DOWN, buff=0.28)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Three desk questions first. Does the quadratic identity replicate a straddle? "
            "No: Q varies with the path, and the terminal quadratic differs from an "
            "absolute-value payoff. <bookmark mark='a'/> Is expected trend profit only "
            "autocorrelation? No: nonzero drift contributes n choose two times mu squared. "
            "<bookmark mark='b'/> Does inverse volatility always equalise risk contributions? "
            "It does in the stated two-asset construction, but general group covariance "
            "requires computing Euler contributions. Each answer starts by specifying the object."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=19) for q, a in DESK[3:]]
                       ).arrange(DOWN, buff=0.28)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Does a risk target guarantee realised risk? A lagged forecast, cap or "
            "covariance change can prevent that. <bookmark mark='a'/> What do the "
            "published series establish? Sample summaries with provider and measurement "
            "limitations, rather than an automatic forecast for a new fund. "
            "<bookmark mark='b'/> Finally, an income fund should disclose its equity and "
            "option exposures, dated tail losses, collateral, execution, financing and "
            "fees. A smooth average return leaves all those questions open."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=17)
        self.play(FadeIn(ps.head), FadeIn(ps.rows[0]))
        with self.voiceover(
            "Twelve problems have full English and Chinese solutions in the notes. "
            "Six basic calculations cover risk fractions, inverse-volatility scaling, "
            "style aggregation, forecast error, a put seller's returns and a linear "
            "cost budget. <bookmark mark='a'/> Four advanced problems treat independent "
            "drift, Gaussian skewness aggregation, an approximate Sharpe detection "
            "horizon and a two-state counterexample to automatic Sharpe improvement "
            "from volatility targeting. <bookmark mark='b'/> Two qualifying problems "
            "prove the Gaussian moments, distribution and limit, then derive a matched "
            "lag filter against a specified covariance alternative. The filter problem "
            "distinguishes a variance reference from the full alternative variance. "
            "These are chosen mathematical exercises, not additional strategy trials."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:10]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(ps.rows[10]), FadeIn(ps.rows[11]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"pairs, residuals and mean reversion", [33]),
            (r"the firm: fees, capacity and culture", [34]),
            (r"liquidity spirals and deleveraging", [41]),
            (r"the finale: evidence and selection across desks", [43]),
        ])
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where this returns. Part thirty-three considers pairs and residual mean "
            "reversion, whose dependence assumptions differ from trend. Part thirty-four "
            "examines the organisation, fees and capacity of the firm. Part forty-one "
            "returns to liquidity and deleveraging. The finale asks what the evidence "
            "supports after accounting for selection across the entire House. "
            "The shared lesson is to state the claim before judging its evidence."
        ):
            self.play(LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4))
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pedersen, \textit{Efficiently Inefficient} (2015); Ilmanen, \textit{Expected Returns} (2011); "
             r"Kakushadze--Serur, \textit{151 Trading Strategies} (2018); Clenow, \textit{Following the Trend} (2013)"],
            [r"Moskowitz--Ooi--Pedersen (2012); Hurst--Ooi--Pedersen (2017); Lemperiere et al. (2014); "
             r"Fung--Hsieh (2001); Potters--Bouchaud (2005); Moreira--Muir (2017); Cederburg et al. (2020)",
             r"Asness--Moskowitz--Pedersen (2013); Frazzini--Pedersen (2014); Koijen et al. (2018); "
             r"Israelov--Nielsen (2015); Garleanu et al. (2009); Lucca--Moench (2015); "
             r"Sullivan--Timmermann--White (2001). Published series: AQR, Cboe, Kenneth French."])
        self.play(FadeIn(card))
        with self.voiceover(
            "The reading guide maps the textbooks, classic papers and methodological "
            "limits to the chapters. The numerical evidence used here comes from the "
            "two published research-series calculations, alongside explicitly chosen "
            "mathematical inputs and analytic reference laws. The notes distinguish "
            "those sources, quotations from historical events and conclusions requiring "
            "further empirical work."
        ):
            self.wait(0.2)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("macro", "portfolio"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 33, Statistical Arbitrage", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(chart))
        with self.voiceover(
            "The House's macro desk now has a specification checklist: information "
            "timing, risk definitions, exposure, financing and the evidence required "
            "for each claim. A premium story remains a hypothesis until that evidence "
            "supports it. <bookmark mark='a'/> Next, statistical arbitrage: pairs, "
            "cointegration, residuals and the mathematics of trading mean reversion. "
            "The same discipline will decide whether a pattern is a model identity, "
            "a sample result or an attainable trading opportunity."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.clear_scene()
