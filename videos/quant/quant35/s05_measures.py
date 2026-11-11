from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (ASK_C, BAD, BID_C, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C, fit_right,
                                         illustration, load)


class Measures(VoiceoverScene):
    def construct(self):
        self.card()
        self.roll()
        self.bounce()
        self.power()
        self.others()
        self.unavailable()
        self.decompose()
        self.question()

    def card(self):
        c = chapter_card(4, r"Measuring the spread from prices alone", r"Can a researcher with only daily closes tell how "
                         r"liquid a market is?", part=PART)
        self.add(c)
        with self.voiceover('Chapter four. Researchers often have daily prices and volume but no historical quotes. Roll, Corwin and Schultz, and Amihud propose different liquidity proxies. We derive their assumptions. The planned ten-fund comparison is unavailable: its unchanged original stopped when the SPY source failed the frozen checksum. We neither refresh the source nor replace the comparison with a new backtest.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def roll(self):
        rows = [cmath(r"p_t", r"=", r"m_t + \tfrac{s}{2}\, q_t,\quad q_t = \pm 1 \text{ independent}", font_size=34),
                cmath(r"\operatorname{Cov}(\Delta p_t, \Delta p_{t-1})", r"=", r"-\tfrac{s^2}{4}", font_size=36),
                cmath(r"\hat s", r"=", r"2\sqrt{-\widehat{\operatorname{Cov}}}", font_size=38, colors={r"\hat s": HURDLE})]
        whys = [why(r"Roll (1984), seen in Part 33: trades print at the bid or the ask around an efficient price that is a "
                    r"random walk"),
                why(r"the bounce makes successive price changes negatively correlated, by a quarter of the spread "
                    r"squared"),
                why(r"so the spread can be read off the autocovariance of prices, with no quotes at all")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Roll's identity requires a model. <bookmark mark='a'/> Let efficient-price increments be iid, with constant full spread s and independent equiprobable trade signs, independent of those increments. <bookmark mark='b'/> Bid-ask bounce then gives lag-one covariance minus s squared over four. <bookmark mark='c'/> Negative sample covariance yields twice its negative square root, in the units of the input prices. Nonnegative covariance makes this formula undefined; it does not prove the economic spread is zero. Serial price dynamics or correlated signs can break the identity."
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

    def bounce(self):
        rng = np.random.default_rng(35)
        T = 60
        m = np.cumsum(0.3 * rng.standard_normal(T)) + 100
        q = np.where(rng.random(T) < 0.5, 1, -1)
        p = m + 0.5 * q
        g = axes([0, T], [float(np.floor(p.min())) - 1, float(np.ceil(p.max())) + 1], x_length=8.0, y_length=4.2,
                 xlabel=r"trades", ylabel=r"price", xticks=[0, 30, 60], yticks=[], font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, np.arange(T), m, PRICE_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(i, p[i]), radius=0.05, color=ASK_C if q[i] > 0 else BID_C) for i in range(T)])
        ill = illustration(r"illustration: a spread of 1 around a random walk")
        leg = legend([(PRICE_C, r"the efficient price"), (ASK_C, r"trades at the ask"), (BID_C, r"trades at the bid")],
                     font_size=16).to_corner(UR, buff=0.4)
        self.add(g, c1, dots[0], leg, ill)
        with self.voiceover(
            "What the estimator sees. <bookmark mark='a'/> The efficient price wanders. <bookmark mark='b'/> Trades "
            "land half a spread above it or below it, at random, so the printed price zig-zags: up, then down, more "
            "often than a random walk would. That zig-zag is the spread."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ill), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.03))
        self.wait(0.4)
        self.clear_scene()

    def power(self):
        import math
        sigma, s = 0.012, 0.0033e-2 * 1.0
        ratio = (s * s / 4) / (sigma * sigma)
        T_days = (2 / ratio) ** 2
        rows = [cmath(r"\operatorname{Cov}", r"=", r"-\tfrac{s^2}{4},\quad \operatorname{se}(\widehat{\operatorname{Cov}})"
                      r"\approx \frac{\sigma^2}{\sqrt T}", font_size=32),
                cmath(r"T", r">", r"\Big(\frac{8\sigma^2}{s^2}\Big)^2\ \ \text{for two standard errors}", font_size=34),
                cmath('\\text{chosen scenario}', r":", rf"\sigma = 1.2\%,\ s = 0.33\ \text{{bp}}\ \Rightarrow\ T \approx 10^{{{math.log10(T_days):.0f}}}"
                      r"\ \text{days}", font_size=30, colors={'\\text{chosen scenario}': BAD})]
        whys = [why(r"the signal is a quarter of the spread squared; the noise in a sample autocovariance of $T$ daily "
                    r"changes is about the daily variance over $\sqrt T$"),
                why(r"to see the signal at two standard errors, the sample must be this long"),
                why('chosen daily volatility 1.2\\% and full spread 0.33 bp give an order-of-magnitude requirement near a trillion observations; this is a model-based heuristic, not an empirical power study')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "A chosen scale calculation. <bookmark mark='a'/> In the simple iid small-bounce approximation, sample autocovariance has standard error of order daily variance divided by the square root of sample length. <bookmark mark='b'/> Two standard errors give the displayed requirement, proportional to volatility to the fourth power divided by spread to the fourth. <bookmark mark='c'/> Stipulate daily volatility one point two percent and full spread point three three basis points. The resulting order is a trillion daily observations. This is a heuristic illustrating weak signal at this frequency, not a calibrated finite-sample power result or a measured SPY quote."
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

    def others(self):
        rows = [cmath(r"\text{Corwin--Schultz}", r":", r"\text{high-low ranges over one and two days}", font_size=32,
                      colors={r"\text{Corwin--Schultz}": PRICE_C}),
                cmath(r"\text{ILLIQ}", r"=", r"\mathbb E\Big[\frac{|r_t|}{\$\text{volume}_t}\Big]", font_size=38,
                      colors={r"\text{ILLIQ}": FLOW_C}),
                cmath(r"\text{direct quotes}", r":", r"\text{tick}\ne\text{quoted spread}\ne\text{effective spread}", font_size=32, colors={r"\text{direct quotes}": GOOD})]
        whys = [why(r"Corwin and Schultz (2012): a day's high is usually a buy at the ask, its low a sell at the bid; the "
                    r"range has a volatility part that grows with time and a spread part that does not"),
                why(r"Amihud (2002): the price move per dollar traded, a daily cousin of Kyle's lambda"),
                why('a one-cent tick is a price increment; it neither guarantees a one-tick spread nor supplies historical realized execution costs')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Three distinct objects. <bookmark mark='a'/> Corwin and Schultz use one- and two-day high-low ranges to separate spread and volatility under their model. Our original clips negative spread estimates at zero; that convention can affect bias. <bookmark mark='b'/> Amihud averages absolute return divided by dollar volume. Its units are return per dollar, and its denominator mechanically links it to volume. It is not a signed-flow structural-impact estimate. <bookmark mark='c'/> Direct quote data allow different measurements, but minimum tick, quoted spread and effective spread must remain distinct. Daily OHLC data alone do not provide their ground truth."
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







    def unavailable(self):
        card = desk_question(r"The planned empirical comparison is unavailable", r"The unchanged original stopped at the frozen SPY daily-bar checksum, 2015--2020. No ten-ETF table, Bitcoin Roll result or Amihud scatter was produced by this attempt. No retry, refresh or replacement historical test.", width=12.4, font_size=25)
        self.add(card)
        with self.voiceover("The empirical boundary matters. Yahoo's extracted SPY bars for 2015 to 2020 differ from the recorded checksum. That key was rejected once, and the original stopped before producing its output. We therefore omit the ten-fund table, Bitcoin Roll result and cross-fund scatter. The mathematical examples remain explicit illustrations. An old reported spread is not a current verified result, and a minimum tick is not an observed effective spread."):
            self.play(FadeIn(card))
        self.clear_scene()

    def decompose(self):
        rows = [cmath(r"\text{effective}", r"=", r"2\,q\,(p - m)", font_size=36, colors={r"\text{effective}": HURDLE}),
                cmath(r"\text{realised}", r"=", r"2\,q\,(p - m_{t+\Delta})", font_size=36, colors={r"\text{realised}": GOOD}),
                cmath(r"\text{impact}", r"=", r"\text{effective} - \text{realised} = 2\,q\,(m_{t+\Delta} - m)", font_size=32,
                      colors={r"\text{impact}": BAD})]
        whys = [why(r"what a trade actually paid against the midpoint at the time, with $q = +1$ for a buy: quotes do not "
                    r"need to be estimated when they are recorded"),
                why(r"what the liquidity provider kept, measured against the midpoint a few seconds or minutes later"),
                why('the difference is a signed midpoint change over the selected horizon; news, transitory dynamics and selection also contribute, so it does not identify private information alone')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "With trade and quote records, define the decomposition. <bookmark mark='a'/> The effective spread is twice the trade-side-signed execution-price difference from the initial midpoint. <bookmark mark='b'/> Replace that midpoint by a specified later midpoint to obtain the realized spread. <bookmark mark='c'/> The difference equals twice the signed midpoint change. This is an accounting identity. Its interpretation depends on horizon, timestamp alignment and selection; it does not by itself identify private information or causality. The factor two expresses a full-spread equivalent rather than one-way cost."
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

    def question(self):
        eq = MathTex('\\widehat{\\operatorname{Cov}}(\\Delta p_t,\\Delta p_{t-1})=-0.0004\\ \\mathrm{dollar}^2', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('Use the Roll identity under constant spread, iid trade signs and independent efficient-price innovations. State why other serial dynamics can invalidate the interpretation.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. A sample lag-one covariance is minus point zero zero zero four dollars squared. Compute the Roll full-spread estimate, check its units and state the assumptions required to interpret it economically.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
