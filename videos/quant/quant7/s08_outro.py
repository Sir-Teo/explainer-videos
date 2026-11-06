from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load

DESK = [
    (r"Daily volatility is 1\%. What is it over a week, and over a year? When is $\sqrt{T}$ wrong?",
     r"$1\% \times \sqrt{5} \approx 2.2\%$ and $1\% \times \sqrt{252} \approx 15.9\%$, if returns are independent with "
     r"constant variance; wrong when volatility mean-reverts (use the GARCH term structure), when returns are "
     r"autocorrelated, and for quantiles of fat-tailed returns"),
    (r"You regress one price on another and get $t = 24$. What do you check first?",
     'assess I(1) as a working model: non-rejection is not proof; EG residual tests need their own critical values (about $-3.34$ for two variables, a constant and no trend)'),
    (r"A new volatility model beats GARCH on mean squared error over a year that includes March 2020. Convinced?",
     'a crash day can dominate MSE; compare simple benchmarks with suitable loss, nesting-aware inference and fresh validation'),
    (r"A GARCH fit gives $\alpha + \beta = 1$. Is the process stationary?",
     'positive $\\omega$ and $\\alpha+\\beta=1$ preclude finite stationary variance; strict Jensen needs $\\alpha>0$, nonconstant squared iid shocks and log integrability'),
]

PROBLEMS = [
    r"For GARCH(1,1), $\sigma^2_{t+1} = \omega + \alpha r_t^2 + \beta\sigma_t^2$, derive the $h$-step forecast "
    r"$\mathbb{E}_t[\sigma^2_{t+h}] = \bar\sigma^2 + (\alpha + \beta)^{h-1}(\sigma^2_{t+1} - \bar\sigma^2)$ and the "
    r"half-life of a shock.",
    'Derive the squared-return ARMA identity and the Gaussian GARCH fourth-moment condition; when finite, derive its kurtosis.',
    'Under continuous prices and independent iid price noise, derive the $2n\\eta^2$ bias and minimize the illustrative MSE $4n^2\\eta^4+2IQ/n$.',
    'With positive conditionally unbiased proxies, measurable forecasts and finite losses, derive the QLIKE target $\\hat h=E[h\\mid\\mathcal F]$ and ranking robustness.',
    r"Write the Kalman filter for a local-level model and show that its steady-state gain depends only on the "
    r"signal-to-noise ratio.",
    'For a random walk fitted with a constant and no trend, derive the coefficient and DF $t$ limits using $W_\\mu=W-\\int_0^1 W$ and $A=\\frac12(W(1)^2-1)-W(1)\\int_0^1W$.',
    '(qual) Under the stated nested-model orthogonality approximation, show $\\mathbb E[e_2^2-e_1^2]\\approx\\mathbb E[(\\hat y_1-\\hat y_2)^2]>0$ and explain the DM bias.',
    '(qual) In the idealized one-regressor case, derive the mean squared forecast-gap approximation $\\sigma^2\\ln(1+P/R)/P$.',
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
            ('magnitudes show stronger persistence; low return autocorrelation does not prove unpredictability', VOL),
            (rf"unrelated random walks regressed on each other: $|t| > 2$ in {100 * s['rej_levels']:.0f}\% of pairs; "
             r"the Dickey--Fuller distribution leans left", BAD),
            (rf"working I(1) model: EG rejects a residual unit root (basis half-life {c['half_life_days']:.1f} days); Treasury "
             r"yield-rank conclusions depend on specification", GOOD),
            (r"hidden states: Hamilton's jars and Kalman's bells; stochastic volatility by quasi-likelihood", ALT),
            (rf"94 years of US stocks: GARCH persistence {g['us']['garch']['persistence']:.3f}; fat tails, and bad news "
             r"counts more", FC),
            (r"the stock--bond correlation changed sign around 2000", ALT),
            (rf"Bitcoin's noise-corrected average volatility: {100 * z['vol_tsrv']:.0f}\%; noisy proxies, jumps and rough scaling require interpretation", VOL),
            ('QLIKE ranking robustness needs positive conditionally unbiased proxies and finite expectations', GOOD),
            (rf"the race: {best} first in this reused sample; log-HAR remains a useful benchmark; published rankings depend on model and horizon", GOOD),
            ('the constant-variance $\\sqrt{T}$ rule omits mean reversion and autocovariances', BAD),
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
            f"""Part seven in ten lines. Magnitudes have strong persistence; low return autocorrelation does not prove unpredictability. Unit-root inference depends on deterministic terms. Cointegration concerns stationary combinations. Hidden-state models and GARCH describe volatility differently. Correlations move. Realized measures contain noise and jumps; proxy roughness needs interpretation. In this reused 2020 comparison {best} leads QLIKE, without clear evidence over log-HAR. Published foundation results depend on model and horizon. Variance aggregation needs covariance and horizon assumptions."""
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
            """Four desk questions. One percent daily scales to about two point two over five trading days and sixteen over 252, under constant variance and zero autocovariances. <bookmark mark='a'/> A t-statistic between prices: check integration and use appropriate residual-test critical values. <bookmark mark='b'/> A crash can dominate a squared-error ranking. Compare sensible benchmarks with appropriate loss and inference. <bookmark mark='c'/> At alpha plus beta one, positive omega gives no finite unconditional variance; strict stationarity needs Nelson's log condition. Strict Jensen needs positive alpha and nonconstant squared shocks. Solutions are in the notes."""
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
            """The textbook chapters this part covers, and the papers it draws on. Empirical examples use the series' own code and public data: French's market returns, FRED yields and VIX, and Binance prices. Simulations have fixed seeds. The published foundation-model comparison is explicitly quoted from the paper."""
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
