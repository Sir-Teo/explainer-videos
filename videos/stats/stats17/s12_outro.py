from __future__ import annotations

from videos.stats.stats17.common import *  # noqa: F403

PROBLEMS = [
    r"AR(1) with $\phi = 0.6$, \ $\mu = 0$: \ $\rho(2)$, \ $\mathrm{Var}(X_t)/\sigma^2$, \ and the 2-step forecast and its SE from $x_n = 5$.",
    r"Show that an MA(1) has $|\rho(1)| \le \tfrac12$, \ with equality only at $\theta = \pm 1$.",
    r"The effective sample size of the mean of 200 observations from an AR(1) with $\rho = 0.5$.",
    r"Is the AR(2) with $\phi_1 = 0.5$, \ $\phi_2 = 0.3$ stationary? \ Find its roots.",
    r"Yule--Walker for an AR(2), \ given $\hat\rho_1 = 0.7$ and $\hat\rho_2 = 0.5$.",
    r"Show that simple smoothing's weights sum to 1, \ and that the average age of the data they weight is $(1 - \alpha)/\alpha$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Yule: \ nonsense correlations", RES), (r"stationarity; \ the ACF and its bands", SERIES),
            (r"dependence shrinks $n$: \ HAC, \ blocks", OBS), (r"AR, \ MA, \ ARMA; \ $\psi$ weights", MODEL),
            (r"roots outside the unit circle", MODEL), (r"complex roots: \ pseudo-cycles; \ Slutsky", OBS),
            (r"ACF and PACF signatures", SERIES), (r"Box--Jenkins: \ identify, \ estimate, \ check", SERIES),
            (r"Yule--Walker, \ AIC, \ Ljung--Box", MODEL), (r"forecasts revert; \ intervals widen", FC),
            (r"trend, \ season, \ remainder", S.ALT), (r"exponential smoothing; \ Holt--Winters", FC),
            (r"spurious regression; \ difference first", RES), (r"combine forecasts", HIT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 17, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part seventeen in fourteen lines. <bookmark mark='a'/> Yule showed that series which merely drift correlate by "
            "nonsense. Stationarity makes a series' dependence stable, and the autocorrelation function, with Bartlett's "
            "bands, measures it. Dependence shrinks the effective sample size; HAC standard errors and block bootstraps "
            "partly repair the mean's interval. Autoregressions and moving averages build memory out of shocks, and the "
            "roots of a polynomial decide whether that memory fades. Complex roots make pseudo-cycles, and so, Slutsky "
            "showed, does averaging noise. The ACF and PACF are fingerprints; Box and Jenkins turned them into a cycle of "
            "identifying, estimating and checking, with Yule–Walker, AIC and Ljung–Box as tools. Forecasts return to the mean "
            "and their intervals widen. Trend and season can be taken apart, and exponential smoothing forecasts them. "
            "Regressions between wandering series are spurious unless differenced. And when unsure, combine forecasts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=32.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"cross-validation for time: \ rolling origins", [19]), (r"the Kalman filter and state space", [38]),
            (r"spectra, \ unit roots, \ cointegration, \ GARCH", [38]), (r"dependent data in space", [39]),
            (r"martingales and mixing", [44]), (r"anytime-valid monitoring of a stream", [58]),
            (r"forecasting with machine learning", [64]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 19's cross-validation must respect time, with rolling forecast "
            "origins. Part 38 takes time series in depth: the Kalman filter and state-space models, spectra, tests for unit "
            "roots, cointegration and volatility models. Part 39 meets dependence in space instead of time. Part 44 builds "
            "the probability of dependent sequences, martingales and mixing. Part 58 monitors a stream of data with "
            "guarantees at every moment. And Part 64 asks what machine learning has changed in forecasting."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> An AR one's moments and forecast; a bound "
            "on an MA one's autocorrelation; an effective sample size; stationarity from roots; the Yule–Walker equations; and "
            "the weights of exponential smoothing. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Box, G. Jenkins, G. Reinsel \& G. Ljung, \emph{Time Series Analysis: Forecasting and Control} (5th ed., 2015)",
             r"P. Brockwell \& R. Davis, \emph{Introduction to Time Series and Forecasting} (3rd ed., 2016)",
             r"R. Hyndman \& G. Athanasopoulos, \emph{Forecasting: Principles and Practice} (3rd ed., 2021)",
             r"R. Shumway \& D. Stoffer, \emph{Time Series Analysis and Its Applications} (4th ed., 2017)"],
            [r"G. U. Yule (1926, 1927); \ E. Slutsky (1927); \ G. Walker (1931); \ H. Wold (1938); \ M. Bartlett (1946)",
             r"J. Durbin \& G. Watson (1950); \ C. Holt (1957); \ P. Winters (1960); \ J. Muth (1960)",
             r"C. Granger \& P. Newbold (1974); \ G. Ljung \& G. Box (1978); \ P. Phillips (1986); \ W. Newey \& K. West (1987)",
             r"S. Makridakis \& M. Hibon (1979); \ S. Makridakis et al.\ (1982, 2000, 2020); \ J. Bates \& C. Granger (1969)"])
        with self.voiceover(
            "The books and papers this part follows: Box and Jenkins, now in its fifth edition; Brockwell and Davis; Hyndman "
            "and Athanasopoulos's free online text; Shumway and Stoffer; with the papers from Yule and Slutsky to Newey, West "
            "and the M-competitions."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=17, current=None)
        nxt = VGroup(label(r"Part 18", font_size=30, color=GREY_B), label(r"Who Did You Ask?", font_size=48),
                     label(r"how 1,000 people can speak for a nation, \ and 2.4 million can fail to", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Seventeen parts of sixty-five, the seventh of Stage II. <bookmark mark='a'/> We can now handle data that remember "
            "their past. <bookmark mark='b'/> But every part so far has trusted that the data were a fair sample of something. "
            "In 1936 the Literary Digest mailed ten million ballots, received two point four million back, and predicted "
            "that Alf Landon would beat Franklin Roosevelt. Roosevelt won forty-six of forty-eight states. Part 18: who did "
            "you ask?"
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(17)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
