from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import PART, RET, VOL, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        z = load("realized")
        dly = load("daily")
        self.title_card()
        self.river(z, dly)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The river under the noise")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part seven. Time series and volatility. Part one found that returns are nearly unpredictable, but their "
            "size is not. This part builds the models that forecast it, and puts them in a race."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def river(self, z, dly):
        t = np.asarray(z["t"])
        rv = np.asarray(z["rv"])
        td, r = np.asarray(dly["t"]), np.asarray(dly["r"])
        level = np.exp(np.asarray(z["kalman"])) * np.sqrt(365)
        g1 = axes([2017.6, 2021], [-0.3, 0.3], x_length=10.0, y_length=2.6, ylabel=r"Bitcoin's daily return",
                  xticks=[], yticks=[-0.2, 0, 0.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g2 = axes([2017.6, 2021], [0, 3.5], x_length=10.0, y_length=2.4, ylabel=r"Bitcoin's volatility, annualised",
                  xticks=[2018, 2019, 2020, 2021], xfmt=lambda u: f"{int(u)}", yticks=[0, 1, 2, 3], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        a1, a2 = g1.ax, g2.ax
        bars = VGroup(*[Line(a1.c2p(tt, 0), a1.c2p(tt, np.clip(v, -0.25, 0.25)), stroke_width=1.2, color=RET)
                        for tt, v in zip(td, r)])
        raw = curve(a2, t, np.clip(np.sqrt(rv * 365), 0, 3.5), RET, stroke_width=1.2).set_stroke(opacity=0.5)
        riv = curve(a2, t, np.clip(level, 0, 3.5), VOL, stroke_width=4)
        side = label(r"Kalman-filtered log volatility: signal-to-noise " + f"{z['kalman_snr']:.2f}", font_size=19,
                     color=VOL).next_to(g2, UP, buff=0.05).align_to(g2, RIGHT)
        src = real_data(r"Binance BTCUSDT one-minute candles, Aug.\ 2017 -- Dec.\ 2020; realized variance from 5-minute "
                        r"returns")
        with self.voiceover(
            "Here are three and a half years of Bitcoin, one bar a day: the day's return. Up or down is close to a coin "
            "toss. <bookmark mark='a'/> The size is not. Measure each "
            "day's volatility from its five-minute returns and it jumps around, but underneath there is something "
            "slower. <bookmark mark='b'/> Filter it, and you see a river: volatility rises and falls over weeks and "
            "months: quiet in early 2019, flooding in the crash of March 2020. You can't forecast the next "
            "day's direction, but you can forecast how big its move is likely to be, and every option price, risk "
            "limit and position size depends on doing it well."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.001, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(raw), run_time=2)
            vo.wait_until("b")
            self.play(Create(riv), FadeIn(side), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Stationarity, unit roots, spurious regression; cointegration on Bitcoin's spot and future",
            r"Hidden states: Hamilton's regimes and the Kalman filter",
            r"ARCH, GARCH, GJR and EGARCH on 94 years; the stock--bond correlation by DCC",
            r"Realized volatility done properly: noise, jumps, two-scale and kernel estimators",
            r"The race: GARCH against HAR against an LSTM and a transformer, out of sample",
            r"March 2020, and when the square-root-of-time rule is wrong",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Stationarity and unit roots, the regression that finds relationships between unrelated series, "
            "and cointegration, the relationship that is real. Hidden states: regimes and the Kalman filter. The "
            "GARCH family on ninety-four years of the market, and correlations that change. Realized volatility "
            "measured properly. Then a race between the classical models and two neural networks trained here, "
            "judged out of sample. And March 2020."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the volatility forecaster: the measures, the models and the scoring rules. "
            "<bookmark mark='a'/> When the volatility desk opens in Part ten, this is the engine it runs on."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
