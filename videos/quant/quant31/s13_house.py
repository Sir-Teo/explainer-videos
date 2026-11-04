from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import BAD, COST_C, FAC_C, GOOD, GP_C, HURDLE, IC_C, PART, SPEC_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("law"), load("model"), load("vasicek"), load("costs"), load("gp"), load("attribution"),
                   load("envelope"))
        self.lab()
        self.lab2()
        self.lab3()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(12, r"Rule 31: the risk model", r"What must a strategy show about its risk, its costs and its "
                         r"trading before it gets capital?", part=PART)
        with self.voiceover("Chapter twelve. The House's thirty-first rule: what a strategy must show about its risk, its "
                            "costs and its trading before it is given capital."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, l, m, v, c, g, a, e):
        cur = {r["aum"]: r["sharpe"] for r in c["curve"]}
        r32 = g["rows"][-1]
        rows = [(r"IC 0.05, N = 500: IR per period, constant IC and IC sd 0.10",
                 rf"{[r for r in l['rows'] if r['N'] == 500 and r['ic_sd'] == 0][0]['sim']:.2f},\ "
                 rf"{[r for r in l['rows'] if r['N'] == 500 and r['ic_sd'] == 0.1][0]['sim']:.2f}", IC_C),
                (r"the coins' factor share of risk; bias statistic, equal-weighted", rf"{100 * m['fac_share']:.0f}\%,\ "
                 rf"{m['bias']['equal-weighted coins'][0]:.2f}", FAC_C),
                (r"next quarter's beta, MSE: raw and Vasicek", rf"{v['mse']['raw']:.3f}\ \to\ {v['mse']['shrunk']:.3f}",
                 SPEC_C),
                (r"calm-coin Sharpe: gross, \$100k, \$1m", rf"{c['gross_sharpe']:.2f},\ {cur[1e5]:.2f},\ {cur[1e6]:.2f}",
                 COST_C),
                (r"$\lambda = 32$: myopic and Garleanu--Pedersen Sharpe", rf"{r32['myopic']:.2f},\ {r32['gp']:.2f}", GP_C),
                (r"mined alpha: factor share of variance, specific Sharpe", rf"{100 * a['var_share_factor']:.0f}\%,\ "
                 rf"{a['sharpe_specific']:.2f}", HURDLE),
                (r"the registered rule, 2021--25 Sharpe", rf"{e['res']['gp']['sr_hold']:.2f}", BAD),
                (r"the trial counter", comma(e["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.4]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The risk desk's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"every number computed in this part from Binance's coins and Kenneth French's industries; "
                             r"none is a forecast, and none is advice", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A moving IC cut the information ratio by more than half. Most of a "
            "coin's risk is common, and the model's forecasts passed the bias test. Shrinking betas cut their error. "
            "Costs took a good signal's Sharpe ratio below zero at a million dollars. Garleanu and Pedersen's trader "
            "survived costs the myopic trader could not. The mined alpha was mostly a factor. And the registered rule "
            "failed on its sealed years, for a reason the House can now name."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"One day's factor returns", RM.factor_returns, "T, N, K = X.shape", 14, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter two's regression, as the House runs it. For each day, keep the assets with a return and a full set "
            "of exposures; weight them; solve the weighted normal equations with a whisper of ridge so a collinear day "
            "cannot break it; and keep the residuals, which become the specific returns. Fourteen lines carry the whole "
            "risk model."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"The trade rate and its check", RM.gp_trade_rate, "b = gamma", 3,
                         extra=((RM.riccati_scalar, "for _ in range(iters):", 15),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter five's trade rate, three lines, followed by the brute-force check the test suite runs against "
            "it: value iteration on the quadratic value function, until the coefficients stop changing. The House keeps "
            "both, because a closed form without a check is a claim."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"The guards Chapter 11 asked for", RM.floor_variance, "return np.maximum", 1,
                         extra=((RM.cap_positions, "x = np.asarray(x, float)", 5),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And the two guards the envelope asked for, added to the library after it was opened, and applied to every "
            "rule from now on. A floor under each forecast variance, set from the asset class. And position caps that "
            "do not consult the model at all: a share of the book, and a share of the asset's daily volume. Six lines "
            "that would have changed Chapter eleven, and that the House may not apply to Chapter eleven's sealed years."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("portfolio",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{standardise}, \texttt{factor\_returns}, \texttt{ewma\_cov}, \texttt{specific\_var}, "
             r"\texttt{portfolio\_risk}", r"the risk model"),
            (r"\texttt{vasicek}, \texttt{bias\_statistic}", r"shrinkage and tests"),
            (r"\texttt{fundamental\_ir}, \texttt{ir\_time\_varying}, \texttt{simulate\_ic\_strategy}", r"the law"),
            (r"\texttt{sqrt\_impact}, \texttt{gp\_trade\_rate}, \texttt{gp\_aim\_weight}, \texttt{riccati\_scalar}",
             r"costs and trading"),
            (r"\texttt{attribute}", r"attribution"),
            (r"\texttt{floor\_variance}, \texttt{cap\_positions}", r"guards"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 31: a strategy gets capital only with its risk forecast by the House's factor model "
                             r"and its bias statistic reported; its P\&L attributed to factors and specific return; its "
                             r"costs from the square-root law at its intended size, and its capacity stated; its trading "
                             r"rule dynamic, not myopic; and every forecast variance floored and every position capped by "
                             r"limits that do not depend on the model.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> The risk model; its shrinkage and its tests; the fundamental "
            "law with its corrections; costs and dynamic trading; attribution; and two guards. <bookmark mark='b'/> And "
            "the thirty-first rule. A strategy gets capital only with its risk forecast by the House's model and the "
            "model's bias statistic reported; its profit and loss attributed to factors and to specific return; its "
            "costs priced at its intended size, and its capacity stated; a trading rule that knows tomorrow comes; and "
            "every forecast variance floored, every position capped, by limits that do not depend on the model."
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
            desk_question(r"the pitch with an IR of 3", r"ask for the IC's standard deviation over time, not its mean: "
                          r"the research chapter turns the two into the information ratio, and breadth stops mattering "
                          r"beyond a point", width=12.0, font_size=19),
            desk_question(r"the market-neutral fund with 3\% volatility", r"ask whose risk model, and what the book "
                          r"would lose in a forced unwind of its crowded positions (Chapter 9)", width=12.0, font_size=19),
            desk_question(r"the daily strategy with a Sharpe of 2", r"ask for its turnover and the size it was costed "
                          r"at; at four ninths of its break-even size it keeps a third of its gross edge", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A pitch with an information ratio of three: ask for the "
            "standard deviation of the IC over time, which, as the research chapter shows, caps the information ratio "
            "however many assets there are. <bookmark mark='b'/> A market-neutral fund with three percent volatility: "
            "ask whose risk model, and what a forced unwind of its crowded positions would cost. "
            "<bookmark mark='c'/> A daily strategy with a Sharpe ratio of two: ask for its turnover, and the size it was "
            "costed at."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
