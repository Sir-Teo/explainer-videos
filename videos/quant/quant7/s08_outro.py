from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load

DESK = [
    (r"Daily volatility is 1\%. What is it over a week, and over a year? When is $\sqrt{T}$ wrong?",
     r"$1\% \times \sqrt{5} \approx 2.2\%$ and $1\% \times \sqrt{252} \approx 15.9\%$, if returns are independent with "
     r"constant variance; wrong when volatility mean-reverts (use the GARCH term structure), when returns are "
     r"autocorrelated, and for quantiles of fat-tailed returns"),
    (r"You regress one price on another and get $t = 24$. What do you check first?",
     r"whether both have unit roots (ADF); if so, test the residual for one (Engle--Granger, critical value about "
     r"$-3.34$, not $-2.86$), or regress changes on changes"),
    (r"A new volatility model beats GARCH on mean squared error over a year that includes March 2020. Convinced?",
     r"no: one day can decide an MSE race; score with QLIKE, compare with a Diebold--Mariano test against HAR, and "
     r"check the result without the crisis weeks"),
]

PROBLEMS = [
    r"For GARCH(1,1), $\sigma^2_{t+1} = \omega + \alpha r_t^2 + \beta\sigma_t^2$, derive the $h$-step forecast "
    r"$\mathbb{E}_t[\sigma^2_{t+h}] = \bar\sigma^2 + (\alpha + \beta)^{h-1}(\sigma^2_{t+1} - \bar\sigma^2)$ and the "
    r"half-life of a shock.",
    r"Show that GARCH(1,1) implies ARMA(1,1) for $r_t^2$, and that its kurtosis exceeds 3 whenever $\alpha > 0$.",
    r"With prices observed with iid noise of variance $\eta^2$, show that $\mathbb{E}[RV_n] = \int\sigma^2 dt + "
    r"2n\eta^2$; explain how two-scale RV removes the bias.",
    r"Show that QLIKE, $L(\hat h, h) = h/\hat h - \log(h/\hat h) - 1$, is minimized in expectation at "
    r"$\hat h = \mathbb{E}[h]$, so that a noisy but unbiased proxy ranks forecasts correctly (Patton 2011).",
    r"Write the Kalman filter for a local-level model and show that its steady-state gain depends only on the "
    r"signal-to-noise ratio.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("spurious"), load("coint"), load("garch"), load("realized"), load("race"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, s, c, g, z, race):
        sc = race["scores"]
        best = min(race["names"], key=lambda k: sc[k]["qlike"])
        items = [
            (rf"unrelated random walks regressed on each other: $|t| > 2$ in {100 * s['rej_levels']:.0f}\% of pairs", BAD),
            (rf"Bitcoin's spot and perpetual are cointegrated; the basis has a half-life of {c['half_life_days']:.1f} days",
             GOOD),
            (r"volatility is a slow hidden state under noisy returns: regimes, Kalman, GARCH", VOL),
            (rf"94 years of US stocks: GARCH persistence {g['us']['garch']['persistence']:.3f}; bad news raises "
             r"volatility more than good (GJR)", FC),
            (r"the stock--bond correlation changed sign around 2000", ALT),
            (rf"Bitcoin's volatility, measured properly: {100 * z['vol_tsrv']:.0f}\%, of which jumps are "
             rf"{100 * z['jump_share']:.0f}\% of the variance", VOL),
            (rf"the race, out of sample in 2020: {best} first on QLIKE; the LSTM's edge over HAR was the logarithm, "
             r"not the network", GOOD),
            (r"$\sqrt{T}$ assumes volatility stands still; it mean-reverts", BAD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 7 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part seven in eight lines. Regress one wandering series on another and you will find a relationship "
            "almost every time. A real one, like Bitcoin's spot and its perpetual future, shows up as cointegration. "
            "Volatility is a slow hidden state under noisy returns. Ninety-four years of the American market give "
            "a GARCH with a persistence close to one, and bad news moves volatility more than good. The correlation "
            "between stocks and bonds changed sign around 2000. Measured properly, Bitcoin's volatility is about "
            "ninety percent a year, and a tenth of its variance comes from jumps. In an honest race over 2020, a "
            "neural network beat HAR, until HAR was fitted to the logarithm too; then four numbers fitted by least "
            "squares came first. And the "
            "square-root-of-time rule assumes volatility stands still. It doesn't."
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
            "Three desk questions. One percent a day is about two point two percent a week and sixteen a year, if "
            "volatility stays put; when it mean-reverts, use the term structure instead. <bookmark mark='a'/> A "
            "t-statistic of twenty-four between two prices: check first for unit roots, and test the residual with "
            "the right critical values. <bookmark mark='b'/> And a model that wins on squared error over a year with "
            "a crash in it may have won on one day. Score it with QLIKE, and test it against HAR. Full solutions are "
            "in the notes."
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
            "And five problems: GARCH's term structure and half-life, GARCH as an ARMA model for squared returns, the "
            "bias that noise adds to realized variance, why QLIKE ranks forecasts correctly, and the Kalman gain. "
            "Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GARCH, realized volatility and the term structure of volatility", [10, 11, 12]),
            (r"stochastic and rough volatility", [13, 14]),
            (r"cointegration and pairs trading", [33]),
            (r"regimes and the Kalman filter in macro and factor timing", [32]),
            (r"volatility forecasts in risk models and value at risk", [31, 40]),
        ])
        with self.voiceover(
            "Where this comes back. The volatility forecaster feeds the volatility desk from Part ten, where "
            "forecasts meet implied volatility, and its term structure becomes the surface of Part twelve. Stochastic "
            "and rough volatility, in Parts thirteen and fourteen, make the hidden state a model for prices. "
            "Cointegration becomes statistical arbitrage in Part thirty-three; regimes and the Kalman filter return "
            "in systematic macro; and volatility forecasts drive the risk models and value at risk of Parts "
            "thirty-one and forty."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Tsay, \textit{Analysis of Financial Time Series}, ch.\ 2--4, 10--11",
             r"Hamilton, \textit{Time Series Analysis}, ch.\ 13, 17--22",
             r"A\"it-Sahalia and Jacod, \textit{High-Frequency Financial Econometrics}, ch.\ 2, 6--7"],
            [r"Box and Jenkins (1970); Granger and Newbold (1974); Dickey and Fuller (1979); Engle and Granger (1987)",
             r"Hamilton (1989); Engle (1982); Bollerslev (1986); Nelson (1991); Glosten, Jagannathan and Runkle (1993)",
             r"Engle (2002); Andersen, Bollerslev, Diebold and Labys (2003); Barndorff-Nielsen and Shephard (2004)",
             r"Zhang, Mykland and A\"it-Sahalia (2005); Barndorff-Nielsen, Hansen, Lunde and Shephard (2008)",
             r"Hansen and Lunde (2005); Corsi (2009); Patton (2011); Bollerslev, Patton and Quaedvlieg (2016)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code from public data: Kenneth French's daily market returns, the St. Louis Fed's Treasury "
            "yields, and one-minute Bitcoin prices from Binance."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 8, Decisions and Control", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now forecast how much the market will move. <bookmark mark='a'/> Next, Part eight: "
            "decisions and control. Given a forecast, how much should you bet? Utility, dynamic programming, "
            "Merton's portfolio problem, and the Kelly criterion, with the controversy that still surrounds it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
