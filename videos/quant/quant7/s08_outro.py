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
    (r"A GARCH fit gives $\alpha + \beta = 1$. Is the process stationary?",
     r"not covariance-stationary (the variance is infinite), but strictly stationary: Nelson (1990) needs only "
     r"$\mathbb{E}\ln(\alpha z^2 + \beta) < 0$, which Jensen gives whenever $\alpha + \beta \le 1$"),
]

PROBLEMS = [
    r"For GARCH(1,1), $\sigma^2_{t+1} = \omega + \alpha r_t^2 + \beta\sigma_t^2$, derive the $h$-step forecast "
    r"$\mathbb{E}_t[\sigma^2_{t+h}] = \bar\sigma^2 + (\alpha + \beta)^{h-1}(\sigma^2_{t+1} - \bar\sigma^2)$ and the "
    r"half-life of a shock.",
    r"Show that GARCH(1,1) implies ARMA(1,1) for $r_t^2$, and that its kurtosis exceeds 3 whenever $\alpha > 0$.",
    r"With prices observed with iid noise of variance $\eta^2$, show that $\mathbb{E}[RV_n] = \int\sigma^2 dt + "
    r"2n\eta^2$; minimise $4n^2\eta^4 + 2IQ/n$ to find Bandi and Russell's optimal $n^*$.",
    r"Show that QLIKE, $L(\hat h, h) = h/\hat h - \log(h/\hat h) - 1$, is minimized in expectation at "
    r"$\hat h = \mathbb{E}[h]$, so that a noisy but unbiased proxy ranks forecasts correctly (Patton 2011).",
    r"Write the Kalman filter for a local-level model and show that its steady-state gain depends only on the "
    r"signal-to-noise ratio.",
    r"For a random walk with $x_0 = 0$, show that $T(\hat\rho - 1) \Rightarrow \tfrac12(W(1)^2 - 1)/\int_0^1 W^2$, "
    r"and that $\Pr(W(1)^2 < 1) \approx 0.68$.",
    r"(qual) Nested models, squared loss, the extra slope zero: show $\mathbb E[e_2^2 - e_1^2] \approx \mathbb E[(\hat y_1 - "
    r"\hat y_2)^2] > 0$, so DM is centred below zero.",
    r"(qual) One extra regressor, recursive OLS from $R$: show the mean squared forecast gap over $P$ forecasts is about "
    r"$\sigma^2\ln(1 + P/R)/P$.",
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
        r2 = load("race2")
        sc = r2["scores"]
        best = min(r2["names"], key=lambda k: sc[k]["qlike"])
        f = load("foundation")
        items = [
            (r"size has a long memory and direction almost none: Ljung--Box on squares dwarfs returns", VOL),
            (rf"unrelated random walks regressed on each other: $|t| > 2$ in {100 * s['rej_levels']:.0f}\% of pairs; "
             r"the Dickey--Fuller distribution leans left", BAD),
            (rf"Bitcoin's spot and perpetual are cointegrated (basis half-life {c['half_life_days']:.1f} days); Treasury "
             r"yields share common trends", GOOD),
            (r"hidden states: Hamilton's jars and Kalman's bells; stochastic volatility by quasi-likelihood", ALT),
            (rf"94 years of US stocks: GARCH persistence {g['us']['garch']['persistence']:.3f}; fat tails, and bad news "
             r"counts more", FC),
            (r"the stock--bond correlation changed sign around 2000", ALT),
            (rf"Bitcoin's volatility measured properly: {100 * z['vol_tsrv']:.0f}\%; noise, jumps and roughness measured", VOL),
            (r"score with QLIKE: it ranks correctly against a noisy target", GOOD),
            (rf"the race: {best} first, log-HAR within noise; a toy foundation model and the literature agree the bar "
             r"is high", GOOD),
            (r"$\sqrt{T}$ assumes volatility stands still; it mean-reverts", BAD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 7 in ten lines", font_size=36).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.4)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        with self.voiceover(
            "Part seven in ten lines. Size has a long memory; direction has almost none. Wandering series fool "
            "regressions, and the random-walk test has its own lopsided distribution. Real ties are cointegration. "
            "Volatility is a slow hidden state. A century of the American market gives a GARCH with persistence near "
            "one, fat tails and asymmetry. The stock-bond correlation changed sign. Measured properly, volatility comes "
            "with noise, jumps and roughness. Scored "
            f"honestly, with QLIKE, the race went to {best}, within noise of log-HAR, and neither our toy foundation "
            "model nor the published ones clearly beat it. And the square-root-of-time rule assumes volatility "
            "stands still. It doesn't."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. One percent a day is about two point two a week and sixteen a year, if volatility stays put. <bookmark mark='a'/> A "
            "t-statistic of twenty-four between two prices: check first for unit roots, and test the residual with "
            "the right critical values. <bookmark mark='b'/> A model that wins on squared error over a year with "
            "a crash in it may have won on one day. Score it with QLIKE, and test it against HAR. <bookmark "
            "mark='c'/> And alpha plus beta equal to one: the variance is infinite, but the process is still strictly "
            "stationary, by Nelson's condition. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "And eight problems: GARCH's term structure and half-life, GARCH as an ARMA model for squared returns, the "
            "bias that noise adds to realized variance and the optimal sampling rate, why QLIKE ranks forecasts "
            "correctly, the Kalman gain, the Dickey-Fuller limit, and two at the level of a qualifying exam: why "
            "Diebold and Mariano's test leans towards the smaller nested model, and by how much. Solutions, in English "
            "and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GARCH, realized volatility and the term structure of volatility", [10, 11, 12]),
            (r"stochastic and rough volatility", [13, 14]),
            (r"cointegration and pairs trading; yield-curve factors", [33, 19]),
            (r"regimes and the Kalman filter in macro and factor timing", [32]),
            (r"volatility forecasts in risk models and value at risk", [31, 40]),
        ])
        with self.voiceover(
            "Where this comes back: the volatility desk and the surface from Part ten, stochastic and rough "
            "volatility in Parts thirteen and fourteen, pairs trading and yield factors, systematic macro, and the "
            "risk models and value at risk of Parts thirty-one and forty."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Tsay, \textit{Analysis of Financial Time Series}, ch.\ 1--5, 8, 10--11",
             r"Hamilton, \textit{Time Series Analysis}, ch.\ 3--5, 13, 15--22; Brockwell and Davis; Francq and Zakoian",
             r"A\"it-Sahalia and Jacod, \textit{High-Frequency Financial Econometrics}; Andersen et al.\ (2006), Handbook"],
            [r"Yule (1927); Kalman (1960); Box and Jenkins (1970); Granger and Newbold (1974); Ljung and Box (1978)",
             r"Dickey and Fuller (1979); Phillips (1986); Engle and Granger (1987); Johansen (1991); Murray (1994)",
             r"Engle (1982); Bollerslev (1986); Hamilton (1989); Nelson (1990, 1991); GJR (1993); Engle (2002)",
             r"ABDL (2003); BNS (2002, 2006); ZMA (2005); BNHLS (2008); Bandi and Russell (2008); Corsi (2009)",
             r"Hansen and Lunde (2005); Patton (2011); Hansen, Lunde and Nason (2011); BPQ (2016); GJR (2018)",
             r"Reisenhofer et al.\ (2022); Ansari et al.\ (2024); Das et al.\ (2024); Ekambaram et al.\ (2024); Brini (2026)",
             r"RiskMetrics TD (1996); Moskowitz, Ooi and Pedersen (2012); Harvey et al.\ (2018); Carr and Wu (2009)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code from public data: Kenneth French's daily market returns, the St. Louis Fed's Treasury "
            "yields and the VIX, and one-minute Bitcoin prices from Binance; the foundation-model comparison is "
            "quoted from the paper."
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
