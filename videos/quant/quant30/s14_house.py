from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import portfolio as P
from videos.quant.quant30.common import BAD, GOOD, HRP_C, HURDLE, PART, SHRINK_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("michaud"), load("spectrum"), load("shrink"), load("rolling"), load("theory"), load("envelope"))
        self.lab()
        self.lab2()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(13, r"Rule 30: the optimizer", r"What must an optimized portfolio report before the House trades "
                         r"it?", part=PART)
        with self.voiceover("Chapter thirteen. The House's thirtieth rule: what an optimized portfolio must report about "
                            "itself before the House will trade it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, m, sp, sh, ro, th, env):
        import numpy as np
        pts = np.median(np.asarray(m["sims"]["60"]["pts"], float), axis=0)
        r120 = ro["res"]["120"]
        y19 = sp["years"]["2019"]
        lw = env["strats"]["lw_gmv_part30"]["row"]["holdout"]
        ew = env["strats"]["equal_weight_part30"]["row"]["holdout"]
        rows = [(r"5 years of data: promised and true volatility, a month", rf"{100 * pts[2]:.1f}\%\ \to\ {100 * pts[0]:.1f}\%",
                 BAD),
                (r"eigenvalues above the noise edge, 2019 (of 49)", rf"{y19['n_above']}", HURDLE),
                (r"sample GMV's true variance, 5 years, simulated", rf"{sh['sims']['60']['sample']['gmv']:.1f}\times\ \to\ "
                 rf"{sh['sims']['60']['nonlinear']['gmv']:.1f}\times\ \text{{shrunk}}", SHRINK_C),
                (r"1980--2020 Sharpe: 1/N, shrunk GMV, HRP", rf"{r120['1/N']['sharpe']:.2f},\ {r120['LW const-corr GMV']['sharpe']:.2f}"
                 rf",\ {r120['HRP']['sharpe']:.2f}", HRP_C),
                (r"true over reported variance, 10-year windows: data, theory", rf"{th['data'][2]['ratio']:.1f},\ "
                 rf"{th['data'][2]['theory']:.1f}", BAD),
                (r"2021--25: shrunk GMV and 1/N, Sharpe", rf"{lw['sharpe']:.2f},\ {ew['sharpe']:.2f}", GOOD),
                (r"the trial counter", comma(env["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.3]
        tab = VGroup()
        for j, (txt, v, col) in enumerate(rows):
            y = 2.3 - 0.65 * j
            tab.add(VGroup(label(txt, font_size=18, color=col).move_to([hx[0], y, 0]),
                           MathTex(v, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The portfolio desk's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"every number computed in this part from Kenneth French's industry portfolios; none is a "
                             r"forecast, and none is advice", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Optimizers fed with five years of estimates promised a fraction of the "
            "risk they delivered. Two eigenvalues of forty-nine stood above the noise. Shrinkage cut the sample "
            "portfolio's excess variance several times over. Over forty years the humble rules held their own, and the "
            "shrunk minimum-variance rule had the least risk. On real windows the risk illusion was even larger than the "
            "theory. And on the sealed years, one over N came first, by less than a standard error."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Shrinkage toward the identity", P.lw_identity, "X = np.asarray(R, float)", 12, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter four's estimator, as the House implements it, in twelve lines. Demean the returns. The target is the "
            "average variance times the identity. Its distance from the sample matrix, and the sample matrix's own noise, "
            "measured observation by observation, give the intensity, capped at one. No tuning, no cross-validation: the "
            "data choose how much to distrust themselves."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Long-only minimum variance, exactly", P._gmv_long_only, "for _ in range(max_iter):", 16,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And the long-only optimizer, which this part had to write for itself, because the general-purpose solver "
            "took seconds per portfolio. It is a primal active-set method: on the assets still free, jump toward the "
            "unconstrained optimum; if a weight would turn negative, stop at zero and fix it there; when the target is "
            "reached, release the fixed weight whose multiplier says it wants back in. It finishes in a few milliseconds "
            "and matches the general solver to the last digit."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("portfolio",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{sample\_cov}, \texttt{lw\_identity}, \texttt{lw\_constcorr}, \texttt{rmt\_clip}, \texttt{lw\_nonlinear}",
             r"covariance"),
            (r"\texttt{gmv}, \texttt{tangency}, \texttt{mean\_variance}, \texttt{frontier}", r"Markowitz"),
            (r"\texttt{black\_litterman}, \texttt{entropy\_pooling}", r"views"),
            (r"\texttt{erc}, \texttt{risk\_contributions}, \texttt{hrp}", r"risk-based"),
            (r"\texttt{min\_cvar}, \texttt{cvar\_of}", r"tails"),
            (r"\texttt{kelly}, \texttt{universal\_2}, \texttt{diversity\_weights}", r"growth"),
            (r"\texttt{gmv\_theory}, \texttt{gmv\_sim}", r"the risk illusion"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.0)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 30: an optimized portfolio enters the House only with its covariance shrunk or "
                             r"cleaned and the method recorded; with its risk reported both in sample and on data the "
                             r"weights did not see; with its gross exposure, turnover and largest weight stated; and "
                             r"compared, after costs, with 1/N and with a risk-based rule that needs no expected returns.",
                             12.4, 18, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Covariance estimators; Markowitz's rules; views; risk-based "
            "allocation; tails; growth; and the theory of the risk illusion. <bookmark mark='b'/> And the thirtieth rule. "
            "An optimized portfolio enters the House only with its covariance shrunk or cleaned, and the method recorded; "
            "with its risk reported both in sample and on data its weights did not see; with its gross exposure, turnover "
            "and largest weight stated; and compared, after costs, with one over N and with a risk-based rule that needs "
            "no expected returns at all."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["portfolio"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the backtest with a volatility of 4\%", r"ask for the window, the number of assets and the "
                          r"estimator; if it is the sample matrix with $K/T$ near one, the true risk is several times "
                          r"larger (the research chapter)", width=12.0, font_size=19),
            desk_question(r"the portfolio with 300\% gross exposure", r"a long-short book built from estimated means: "
                          r"check it against 1/N and a shrunk minimum-variance rule, after costs", width=12.0, font_size=19),
            desk_question(r"the risk-parity fund that lost in 2022", r"equal risk is not no risk: when bonds and stocks "
                          r"fall together, the correlations it assumed are gone (Part 41)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A backtest with a volatility of four percent: ask for the "
            "window, the number of assets and the estimator; with the sample matrix and nearly as many assets as "
            "observations, the true risk is several times larger. <bookmark mark='b'/> A portfolio with three hundred "
            "percent gross exposure: built from estimated means, it must beat one over N and a shrunk minimum-variance "
            "rule after costs. <bookmark mark='c'/> A risk-parity fund that lost in 2022: equal risk is not no risk, and "
            "when bonds and stocks fall together the correlations it relied on are gone."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
