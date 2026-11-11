from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, GOOD, HURDLE, KAL_C, PART, SPREAD_C, fit_right, load


class Kalman(VoiceoverScene):
    def construct(self):
        k = load("kalman")
        self.card()
        self.model()
        self.filter_()
        self.betas(k)
        self.spreads(k)
        self.window()
        self.trap(k)
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Hedge ratios that move", r"What if the tie between two prices changes over time?", part=PART)
        with self.voiceover("Chapter six. Cointegration assumes one fixed hedge ratio. Real relationships drift. The "
                            "Kalman filter of Part seven lets the hedge ratio move, and in doing so sets a trap."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"y_t", r"=", r"\alpha_t + \beta_t\, x_t + e_t,\quad e_t \sim N(0, r)", font_size=36),
                cmath(r"(\alpha_t, \beta_t)", r"=", r"(\alpha_{t-1}, \beta_{t-1}) + w_t,\quad w_t \sim N(0, qI)", font_size=34,
                      colors={r"(\alpha_t, \beta_t)": KAL_C}),
                cmath(r"q/r", r":", r"\text{how fast the hedge ratio is allowed to move}", font_size=32)]
        whys = [why(r"the regression of one log price on the other, with coefficients that change"),
                why(r"the coefficients follow random walks: the state of a linear Gaussian state-space model"),
                why(r"gain also depends on the loading vector, price units and state covariance; larger $q/r$ permits faster adaptation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> One log price is an intercept plus a hedge ratio times the other, plus "
            "noise. <bookmark mark='b'/> But the intercept and the hedge ratio are themselves random walks: a state "
            "that the filter tracks. <bookmark mark='c'/> One choice matters: the ratio of the state's noise to the "
            "observation's, which decides how fast the hedge ratio may move."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def filter_(self):
        rows = [cmath(r"P_{t|t-1}", r"=", r"P_{t-1} + qI", font_size=36),
                cmath(r"K_t", r"=", r"\frac{P_{t|t-1}h_t}{h_t^\top P_{t|t-1}h_t + r},\quad h_t = (1, x_t)", font_size=34),
                cmath(r"m_t", r"=", r"m_{t-1} + K_t\,(y_t - h_t^\top m_{t-1})", font_size=36, colors={r"m_t": KAL_C}),
                cmath(r"\text{spread}_t", r"=", r"y_t - h_t^\top m_{t-1}", font_size=34, colors={r"\text{spread}_t": SPREAD_C})]
        whys = [why(r"predict: the uncertainty about the coefficients grows by $q$ each day"),
                why(r"the gain: how much of today's surprise to believe"),
                why(r"update the coefficients toward today's observation"),
                why(r"the innovation uses the prior state and current $x_t$; it is observed at the close, not prior tradable wealth")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The filter predicts and then updates. <bookmark mark='a'/> The state covariance grows by q times the identity. <bookmark mark='b'/> The gain depends on the current loading vector and observation variance. <bookmark mark='c'/> Today's observed log prices update the coefficients. <bookmark mark='d'/> The innovation uses the prior state but today's x as well as today's y. It becomes available at the current close. Whether a subsequent holding earns a return requires explicit holdings and rebalancing; the innovation itself is not that wealth."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def betas(self, k):
        d = np.asarray(k["days"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        bk = np.asarray(k["beta_kalman"], float)
        br = np.asarray(k["beta_roll"], float)
        g = axes([x[0], x[-1]], [0, 3], x_length=8.0, y_length=4.2, xlabel=r"2018--2020",
                 ylabel=r"hedge ratio of ETH on BTC (log prices)", xticks=[2018, 2019, 2020, 2021], yticks=[0, 1, 2, 3],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        ok = np.isfinite(br)
        c1 = curve(ax, x[ok], np.clip(br[ok], 0, 3), GREY_B, stroke_width=2)
        c2 = curve(ax, x[20:], bk[20:], KAL_C, stroke_width=3)
        st = DashedLine(ax.c2p(x[0], k["beta_static"]), ax.c2p(x[-1], k["beta_static"]), color=HURDLE, stroke_width=2)
        leg = legend([(GREY_B, r"60-day rolling OLS"), (KAL_C, r"Kalman filter"), (HURDLE, r"one OLS on all three years")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.8)
        fit_right(leg)
        self.add(g, st, leg)
        with self.voiceover(
            "Bitcoin and ether, 2018 to 2020: two prices with an obvious common driver. <bookmark mark='a'/> One "
            f"regression on all three years gives a hedge ratio of {k['beta_static']:.2f}. <bookmark mark='b'/> A "
            "sixty-day rolling regression swings wildly, from near zero to almost three. <bookmark mark='c'/> The Kalman "
            "filter gives a smooth, slowly moving ratio between about two thirds and one. Which spread is the right one "
            "to trade?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(st))
            vo.wait_until("b")
            self.play(Create(c1), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(c2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def spreads(self, k):
        hx = [-3.4, 0.4, 3.6]
        head = VGroup(label(r"spread", font_size=18, color=GREY_B), label(r"ADF $t$", font_size=18, color=GREY_B),
                      label(r"half-life", font_size=18, color=GREY_B))
        tab = VGroup(head,
                     VGroup(label(r"fixed hedge ratio", font_size=20, color=HURDLE), MathTex(f"{k['adf_static']:.2f}",
                                                                                          font_size=28),
                            MathTex(rf"{k['hl_static']:.0f}\ \text{{days}}", font_size=28)),
                     VGroup(label(r"Kalman, one step ahead", font_size=20, color=KAL_C), MathTex(f"{k['adf_kalman']:.2f}",
                                                                                              font_size=28),
                            MathTex(rf"{k['hl_kalman']:.1f}\ \text{{days}}", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.9 * j, 0])
        foot = wrapped_label(r"ADF and AR(1) descriptive diagnostics; fixed residual critical values do not calibrate an adaptive innovation", 11.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.8)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"Descriptive diagnostics for two different constructions. <bookmark mark='a'/> The full-sample fixed ratio is retrospective. Its residual ADF statistic is {k['adf_static']:.2f}, and the fitted half-life {k['hl_static']:.0f} days. <bookmark mark='b'/> The adaptive innovation has statistic {k['adf_kalman']:.1f} and fitted half-life {k['hl_kalman']:.1f} days. Applying a fixed Engle-Granger reference to this generated adaptive series does not supply a calibrated cointegration test. A stationary-looking innovation is not proof of a stable fixed combination or profitable holdings."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def window(self):
        rows = [cmath(r"K_\infty", r"\approx", r"\sqrt{q/r}", font_size=38, colors={r"K_\infty": KAL_C}),
                cmath(r"m_t", r"\approx", r"(1 - K_\infty)\, m_{t-1} + K_\infty \cdot \text{today's estimate}", font_size=32),
                cmath(r"\text{scalar unit-loading memory}", r"\approx", r"1/\sqrt{q/r}\ \text{days}", font_size=34,
                      colors={r"\text{scalar unit-loading memory}": HURDLE})]
        whys = [why(r"scalar random-walk state, constant unit observation loading, small $q/r$: an illustrative steady-state limit"),
                why(r"so the filter is an exponentially weighted regression: it forgets the past at the rate of its gain"),
                why(r"in that scalar illustration, ratios $10^{-4}$ and $10^{-2}$ imply memory near 100 and 10 observations; not this two-state regression's universal window")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The square-root rule is a scalar illustration. <bookmark mark='a'/> For a random-walk state observed with constant unit loading and small q over r, the steady gain is approximately the square root of q over r. <bookmark mark='b'/> Its exponential memory length is approximately the reciprocal gain. <bookmark mark='c'/> That gives about one hundred or ten observations for ratios of one in ten thousand or one in one hundred. Our two-state intercept-and-beta regression instead has the changing loading vector one and the current log price. Price levels, units and covariance matter. Those scalar numbers are not its universal effective window."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def trap(self, k):
        rows = [cmath(r"\text{spread}_t", r"=", r"y_t - h_t^\top m_{t-1}", font_size=36,
                      colors={r"\text{spread}_t": SPREAD_C}),
                cmath(r"\text{a forecast error}", r"\approx", r"\text{white under a correctly specified filter}", font_size=32,
                      colors={r"\text{a forecast error}": BAD}),
                cmath(r"\text{reversion}", r"\neq", r"\text{profit}", font_size=36)]
        whys = [why(r"the Kalman spread is the filter's one-step forecast error"),
                why(r"a good filter's forecast errors are close to unpredictable noise: of course they look stationary, "
                    r"with a half-life near zero"),
                why(r"the spread reverts because the hedge ratio moves to absorb it, not because prices converge: betting "
                    r"on it bets on the filter's next correction, which already happened")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "It is a trap. <bookmark mark='a'/> The Kalman spread is the filter's forecast error. "
            "<bookmark mark='b'/> A good filter's forecast errors are close to white noise, so of course they test as "
            "stationary, with a half-life of about a day. <bookmark mark='c'/> The spread looks like it reverts because "
            "the hedge ratio moves to absorb every gap, not because the prices converge. A trade on it is a bet that "
            "the filter will correct itself, which it does by changing the ratio, not by moving the prices."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"use the filter for the ratio, not the test", r"a slowly moving hedge ratio is useful for "
                          r"sizing the hedge; its residual is not evidence of a pair", width=12.4, font_size=19),
            desk_question(r"test out of sample", r"trade the spread built from yesterday's ratio, on days the filter has "
                          r"not seen, and judge the profit, not the stationarity", width=12.4, font_size=19),
            desk_question(r"choose $q/r$ slowly", r"a slow filter keeps the spread's economics; a fast one manufactures "
                          r"reversion, and every choice of $q/r$ is a trial", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "So: <bookmark mark='a'/> use the filter to size the hedge, not to prove there is a pair. "
            "<bookmark mark='b'/> Test the spread out of sample, on its profit, not on its stationarity. "
            "<bookmark mark='c'/> And choose the speed slowly: a fast filter manufactures reversion, and every choice "
            "of its speed is a trial."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a filter's one-step forecast errors have an AR(1) slope of 0.3. Is the pair cointegrated?")
        working = MathTex('e_t=y_t-h_t^\\top m_{t-1},\\qquad s_t=y_t-\\beta x_t\\quad(\\beta\\ \\text{fixed})', font_size=32).move_to(UP * 0.8)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('AR(1) dependence in an adaptive innovation does not establish a stationary fixed combination of integrated prices or profitable holdings.', 11.7, 23).move_to(DOWN * 0.9)
        self.add(working, setup_note, q)
        with self.voiceover(
            "Pause and predict. A filter's one-step forecast errors have an autoregressive slope of point three. Is the "
            "pair cointegrated?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
