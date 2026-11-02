from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        z = load("realized")
        dly = load("daily")
        self.title_card()
        self.century(load("garch"))
        self.memory(load("acf_arma"))
        self.river(z, dly, load("kalman"))
        self.history()
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

    def century(self, g):
        t, a = np.asarray(g["t"]), np.asarray(g["absr_ann"])
        k = 4  # 20 trading days per bar
        n = len(t) // k
        tb = t[:n * k].reshape(n, k).mean(1)
        rms = np.sqrt((a[:n * k].reshape(n, k) ** 2).mean(1))
        gr = axes([1926, 2021], [0, 1.0], x_length=12.0, y_length=4.4, xticks=[1930, 1950, 1970, 1990, 2010],
                  xfmt=lambda u: f"{int(u)}", yticks=[0, 0.5, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  ylabel=r"size of the US market's daily moves, annualised (each bar: 20 trading days)",
                  font_size=16).move_to(DOWN * 0.3)
        ax = gr.ax
        hi = float(np.quantile(rms, 0.995))
        bars = VGroup()
        for x, v in zip(tb, rms):
            f = float(np.clip(v / 0.45, 0, 1))
            bars.add(Line(ax.c2p(x, 0), ax.c2p(x, min(v, 1.0)), stroke_width=2.2,
                          color=interpolate_color(ManimColor(GREY_D), ManimColor(BAD), f)))
        glow = curve(ax, t, np.clip(np.asarray(g["vol_ann"]), 0, 1.0), VOL, stroke_width=3)
        tags = VGroup(*[label(s, font_size=18, color=BAD).next_to(ax.c2p(x, min(y, 0.95)), UP, buff=0.08)
                        for s, x, y in ((r"1929--33", 1932, 0.72), (r"1987", 1987.8, 0.62), (r"2008", 2008.8, 0.66),
                                        (r"2020", 2020.2, 0.72))])
        src = real_data(r"Kenneth French's daily US market return, July 1926 -- December 2020 (" +
                        f"{g['n']:,}".replace(",", "{,}") + r" days)")
        q = pause_card(r"Tomorrow's sign: can you forecast it? Tomorrow's size?", width=6.8, font_size=24)
        q.to_corner(UR, buff=0.3)
        with self.voiceover(
            "Here is almost a century of the American stock market, every bar the size of its daily moves over a "
            "month. <bookmark mark='a'/> Big moves do not arrive alone. They come in clusters: the early nineteen "
            "thirties, 1987, 2008, March 2020. Benoit Mandelbrot saw it in cotton prices in 1963: large changes tend to "
            "be followed by large changes, of either sign. <bookmark mark='b'/> So, pause and predict. Can you "
            "forecast tomorrow's sign? And can you forecast tomorrow's size? <bookmark mark='c'/> The bright line is "
            "the slow, hidden quantity that the clusters suggest: volatility. This part is about seeing it, measuring "
            "it and forecasting it."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(src))
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.004, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_, shift=DOWN * 0.1) for x_ in tags], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(q), Create(glow), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    def memory(self, a):
        L = 100
        lags = np.arange(1, L + 1)
        r_, ab = np.asarray(a["acf"]["r"])[1:L + 1], np.asarray(a["acf"]["abs"])[1:L + 1]
        mk = lambda title: axes([0, L + 1], [-0.1, 0.4], x_length=5.6, y_length=3.6, xticks=[1, 25, 50, 100],  # noqa: E731
                                yticks=[0, 0.2, 0.4], xlabel=r"lag (trading days)", ylabel=title, font_size=16)
        g1, g2 = mk(r"autocorrelation of returns $r_t$"), mk(r"autocorrelation of sizes $|r_t|$")
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)

        def bars(g, v, col):
            ax = g.ax
            return VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, y), stroke_width=3, color=col) for x, y in zip(lags, v)])

        b1, b2 = bars(g1, r_, RET), bars(g2, ab, VOL)
        band_ = Rectangle(width=g1.ax.c2p(L + 1, 0)[0] - g1.ax.c2p(0, 0)[0],
                          height=g1.ax.c2p(0, 0.012)[1] - g1.ax.c2p(0, -0.012)[1], stroke_width=0, fill_color=GREY_B,
                          fill_opacity=0.25).move_to(g1.ax.c2p((L + 1) / 2, 0))
        lb = a["lb"]
        cap = VGroup(
            MathTex(rf"\rho_1(r) = {r_[0]:.2f},\quad \rho_{{100}}(r) = {r_[-1]:+.2f}", font_size=26, color=RET),
            MathTex(rf"\rho_1(|r|) = {ab[0]:.2f},\quad \rho_{{100}}(|r|) = {ab[-1]:.2f},\quad "
                    rf"\rho_{{250}}(|r|) = {a['acf']['abs'][250]:.2f}", font_size=26, color=VOL),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The data answer. Correlate each day's return with the return a lag earlier. <bookmark mark='a'/> The "
            f"bars sit almost on zero: at lag one, {r_[0]:.2f}, and nothing after. Direction has no memory worth "
            "trading. <bookmark mark='b'/> Now do the same with the size of the move, the absolute return. At lag "
            f"one the correlation is {ab[0]:.2f}, and it decays slowly: a hundred trading days later it is still "
            f"{ab[-1]:.2f}, and after a whole year it has not reached zero. Size has a long memory. That memory is "
            "what every model in this part exploits."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(band_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in b1], lag_ratio=0.03, run_time=2.5), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in b2], lag_ratio=0.03, run_time=3), FadeIn(cap[1]))
        self.wait(0.3)
        self.clear_scene()

    def river(self, z, dly, k):
        t = np.asarray(k["t"])
        y = np.exp(np.asarray(k["y"])) * np.sqrt(365)
        m = np.exp(np.asarray(k["m"])) * np.sqrt(365)
        td, r = np.asarray(dly["t"]), np.asarray(dly["r"])
        g1 = axes([2017.6, 2021], [-0.3, 0.3], x_length=10.0, y_length=2.4, ylabel=r"Bitcoin's daily return",
                  xticks=[], yticks=[-0.2, 0, 0.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g2 = axes([2017.6, 2021], [0, 3.5], x_length=10.0, y_length=2.6, ylabel=r"Bitcoin's volatility, annualised",
                  xticks=[2018, 2019, 2020, 2021], xfmt=lambda u: f"{int(u)}", yticks=[0, 1, 2, 3],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)
        a1, a2 = g1.ax, g2.ax
        bars = VGroup(*[Line(a1.c2p(tt, 0), a1.c2p(tt, np.clip(v, -0.25, 0.25)), stroke_width=1.2, color=RET)
                        for tt, v in zip(td, r)])
        dots = VGroup(*[Dot(a2.c2p(tt, min(v, 3.5)), radius=0.018, color=RET).set_opacity(0.55) for tt, v in zip(t, y)])
        tr = ValueTracker(0.0)
        riv = tracing(a2, t, np.clip(m, 0, 3.5), tr, VOL, stroke_width=4)
        side = label(r"Kalman-filtered log volatility: signal-to-noise " + f"{z['kalman_snr']:.2f}", font_size=19,
                     color=VOL).next_to(g2, UP, buff=0.05).align_to(g2, RIGHT)
        src = real_data(r"Binance BTCUSDT one-minute candles, Aug.\ 2017 -- Dec.\ 2020; realized variance from 5-minute "
                        r"returns")
        with self.voiceover(
            "The same holds in a market that never closes. Here are three and a half years of Bitcoin, one bar a "
            "day. <bookmark mark='a'/> Measure each day's volatility from its five-minute returns, one dot a day, "
            "and it jumps around. <bookmark mark='b'/> Now run a filter through it, day by day, that keeps a belief "
            "about the slow level and nudges it toward each new dot. A river appears: quiet in early 2019, flooding "
            "in March 2020. You can't forecast the next day's direction, but you can forecast how big its move is "
            "likely to be, and every option price, risk limit and position size depends on doing it well."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.001, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(g2), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=2.5))
            vo.wait_until("b")
            self.add(riv)
            self.play(FadeIn(side), tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(1.0) - 0.5, 3),
                      rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    def history(self):
        strip = timeline(lit=(1927, 1960, 1963, 1982, 1989, 1994, 2003, 2018)).move_to(UP * 2.3)
        cards = [
            (1927, r"Udny Yule", r"sunspots as an autoregression: the first AR model"),
            (1960, r"Rudolf Kalman", r"the filter: predict, observe, correct"),
            (1970, r"George Box, Gwilym Jenkins", r"identify, estimate, check: ARMA as a craft"),
            (1979, r"David Dickey, Wayne Fuller", r"a test for a unit root, with its own distribution"),
            (1982, r"Robert Engle", r"ARCH, on UK inflation: variance that responds to news"),
            (1986, r"Tim Bollerslev", r"GARCH: variance with memory"),
            (1987, r"Engle and Clive Granger", r"cointegration: wandering series tied together"),
            (1989, r"James Hamilton", r"hidden regimes, switching by a Markov chain"),
            (1994, r"J.P.\ Morgan", r"RiskMetrics: one exponential average, free to all"),
            (2003, r"ABDL; the Nobel", r"realized volatility from intraday data; Engle and Granger's prize"),
            (2009, r"Fulvio Corsi", r"HAR: a day, a week and a month"),
            (2018, r"Gatheral, Jaisson, Rosenbaum", r"volatility is rough"),
        ]
        grid = VGroup(*[history_card(y, w, s, color=QC.IDEA, width=3.15, font_size=16) for y, w, s in cards])
        grid.arrange_in_grid(rows=3, cols=4, buff=(0.18, 0.15))
        if grid.height > 4.9:
            grid.scale_to_fit_height(4.9)
        grid.next_to(strip, DOWN, buff=0.35)
        with self.voiceover(
            "How we got here. In 1927 Udny Yule modelled sunspot numbers as a series that remembers its own past: the "
            "first autoregression. In 1960 Rudolf Kalman published a filter for hidden states that guided Apollo. In "
            "1970 George Box and Gwilym Jenkins made model building a craft, and in 1979 David Dickey and Wayne "
            "Fuller showed how to test for a random walk. <bookmark mark='a'/> Then volatility: Robert Engle's ARCH in "
            "1982, built for British inflation; Tim Bollerslev's GARCH in 1986; Engle and Clive Granger's "
            "cointegration in 1987; James Hamilton's regimes in 1989. <bookmark mark='b'/> In 1994 J.P. Morgan gave "
            "away RiskMetrics, an exponential average that became the industry's default. Around 2000, intraday data "
            "turned volatility into something you measure, and in 2003 Engle and Granger shared the Nobel prize. "
            "<bookmark mark='c'/> HAR in 2009, rough volatility in 2018, and since 2024, foundation models that "
            "forecast any time series without training. Each of them gets a chapter."
        ) as vo:
            self.play(FadeIn(strip))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in grid[:4]], lag_ratio=0.5, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in grid[4:8]], lag_ratio=0.5, run_time=4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in grid[8:10]], lag_ratio=0.5, run_time=2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in grid[10:]], lag_ratio=0.5, run_time=2))
        self.wait(0.3)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Stationarity, ARMA and Box--Jenkins; unit roots and the Dickey--Fuller distribution; spurious regression",
            r"Cointegration: Engle--Granger and Johansen; hidden regimes and the Kalman filter",
            r"ARCH and GARCH by maximum likelihood; stationarity, fat tails and asymmetry; correlations that move (DCC)",
            r"Realized volatility, noise and jumps; HAR; is volatility rough?",
            r"Scoring forecasts honestly; networks trained here; the race; foundation models",
            r"March 2020; how risk vendors, CTAs and options desks forecast volatility",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            "The plan. Stationarity, ARMA models and unit roots, the regression that finds relationships between "
            "unrelated series, and cointegration, the relationship that is real. Hidden states: regimes and the "
            "Kalman filter. The GARCH family, derived and fitted, and correlations that change. Realized volatility "
            "measured properly, the HAR model and rough volatility. Then how to score a forecast, networks trained "
            "here, a race judged out of sample, and foundation models. And March 2020, and the industry."
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
