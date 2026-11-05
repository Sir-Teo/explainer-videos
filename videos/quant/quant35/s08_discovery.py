from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, FLOW_C, GOOD, HURDLE, PART, PRICE_C, fit_right, load

PERP_C = QC.DELTA
SPOT_C = QC.SPOT


class Discovery(VoiceoverScene):
    def construct(self):
        d = load("discovery")
        self.card()
        self.two()
        self.vecm()
        self.shares()
        self.results(d)
        self.bounds(d)
        self.nyse()
        self.lead(d)
        self.basis(d)
        self.question()

    def card(self):
        c = chapter_card(7, r"Price discovery across markets", r"When one asset trades in two places, where is its price "
                         r"found?", part=PART)
        with self.voiceover("Chapter seven. Bitcoin trades on a spot market and, five times as heavily, as a perpetual "
                            "future. Arbitrage ties the two prices together. But news has to arrive somewhere first. "
                            "Joel Hasbrouck's question: which market discovers the price?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def two(self):
        rows = [cmath(r"p^{\text{perp}}_t,\ p^{\text{spot}}_t", r"=", r"m_t + \text{noise}", font_size=34),
                cmath(r"m_t", r"=", r"m_{t-1} + \eta_t\ \ \text{(the efficient price)}", font_size=34,
                      colors={r"m_t": GOOD}),
                cmath(r"p^{\text{perp}} - p^{\text{spot}}", r"\sim", r"\text{stationary: the basis}", font_size=34)]
        whys = [why(r"both prices are the same efficient price plus market-specific frictions"),
                why(r"the efficient price is a random walk; its innovations are the news"),
                why(r"cointegrated, Part 33's word: arbitrage keeps the basis bounded, here funding on the perpetual")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> Both prices are one efficient price plus market-specific noise. "
            "<bookmark mark='b'/> The efficient price is a random walk; its innovations are the news. "
            "<bookmark mark='c'/> The difference, the basis, is stationary: the two are cointegrated, Part "
            "thirty-three's word, held together by arbitrage."
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

    def vecm(self):
        rows = [cmath(r"\Delta p_t", r"=", r"\alpha\,(p^{\text{perp}} - p^{\text{spot}})_{t-1} + \textstyle\sum_k "
                      r"\Gamma_k \Delta p_{t-k} + e_t", font_size=32),
                cmath(r"\alpha", r"=", r"(\alpha_{\text{perp}}, \alpha_{\text{spot}})", font_size=36),
                cmath(r"\psi", r"\propto", r"\alpha_\perp = (\alpha_{\text{spot}}, -\alpha_{\text{perp}})", font_size=34,
                      colors={r"\psi": GOOD})]
        whys = [why(r"the error-correction model of Part 33's baskets, for two prices"),
                why(r"how strongly each market moves to close the basis"),
                why(r"the market that does not adjust is the one the other follows: its weight in the common trend is the "
                    r"other's adjustment speed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The tool. <bookmark mark='a'/> Part thirty-three's error-correction model, for two prices. "
            "<bookmark mark='b'/> The loadings alpha say how strongly each market moves to close the basis. "
            "<bookmark mark='c'/> The market that does not adjust is the one the other follows, so each market's weight "
            "in the common trend is the other's speed of adjustment."
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

    def shares(self):
        rows = [cmath(r"\operatorname{Var}(\eta)", r"=", r"\psi\,\Omega\,\psi^\top", font_size=36),
                cmath(r"\text{IS}_j", r"=", r"\frac{([\psi F]_j)^2}{\psi\Omega\psi^\top},\quad FF^\top = \Omega",
                      font_size=34, colors={r"\text{IS}_j": GOOD}),
                cmath(r"\text{bounds}", r":", r"\text{the two orderings of the Cholesky factor } F", font_size=32)]
        whys = [why(r"the variance of the efficient price's innovation, from the residual covariance $\Omega$"),
                why(r"Hasbrouck (1995): each market's share of that variance, its information share"),
                why(r"when the two markets' shocks are correlated within the sampling interval, the attribution depends on "
                    r"the ordering, and the bounds widen")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Hasbrouck's information share. <bookmark mark='a'/> The variance of the efficient price's innovation comes "
            "from the residual covariance. <bookmark mark='b'/> Each market's share of it is its information share. "
            "<bookmark mark='c'/> But when the two markets' shocks are correlated within the sampling interval, the "
            "split depends on which is ordered first, and the answer is a range."
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

    def results(self, d):
        ms = d["months"]
        x = np.arange(len(ms))
        lo = np.array([m["perp_low"] for m in ms])
        hi = np.array([m["perp_high"] for m in ms])
        g = axes([0, len(ms) - 1], [0, 1], x_length=8.0, y_length=4.2, xlabel=r"2021--2024, by month",
                 ylabel=r"the perpetual's information share", xticks=[0, 12, 24, 36], yticks=[0, 0.5, 1],
                 xfmt=lambda v: str(2021 + int(v) // 12), font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(i, a), ax.c2p(i, b), color=PERP_C, stroke_width=4) for i, (a, b) in
                        enumerate(zip(lo, hi))])
        with self.voiceover(
            "The answer, month by month, from one-minute bars. <bookmark mark='a'/> Each bar is the range of the "
            f"perpetual's information share. On average it runs from near zero to near one: a width of {d['width']:.2f}. "
            "At one-minute sampling, the method cannot say which market leads."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, d):
        rows = [cmath(r"\operatorname{corr}(r^{\text{perp}}_t, r^{\text{spot}}_t)", r"=", rf"{d['corr0']:.3f}",
                      font_size=36, colors={r"\operatorname{corr}(r^{\text{perp}}_t, r^{\text{spot}}_t)": HURDLE}),
                cmath(r"\text{arbitrage}", r":", r"\text{milliseconds}\ \ll\ \text{one minute}", font_size=34),
                cmath(r"\text{finer data}", r"\Rightarrow", r"\text{narrower bounds}", font_size=34, colors={r"\text{finer data}": GOOD})]
        whys = [why(r"within the minute, the two returns are almost the same number: their shocks are simultaneous at this "
                    r"resolution"),
                why(r"arbitrageurs align the two books in milliseconds; a minute contains thousands of rounds of discovery"),
                why(r"studies with tick data find the futures market usually leads; the House would need trade-level data "
                    r"to say so here")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why. <bookmark mark='a'/> Within a minute, the two returns are almost the same number: a correlation of "
            f"{d['corr0']:.3f}. <bookmark mark='b'/> Arbitrageurs align the two books in milliseconds, and a minute "
            "contains thousands of rounds of discovery. <bookmark mark='c'/> So the method needs finer data, and studies "
            "with tick data generally find the futures market leading. A null result, honestly reported: the House's "
            "data are too coarse to answer the question."
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

    def nyse(self):
        cards = VGroup(
            desk_question(r"Hasbrouck (1995)", r"for the thirty Dow stocks trading on the NYSE and on regional exchanges, "
                          r"the NYSE's information share was above nine tenths: the home market discovered the price, the "
                          r"others followed", width=12.4, font_size=19),
            desk_question(r"why the method worked there", r"in 1993 quotes moved in seconds, not microseconds, so one-second "
                          r"data separated the markets; at today's speeds the same question needs nanosecond time stamps",
                          width=12.4, font_size=19),
            desk_question(r"futures and spot, generally", r"index futures usually lead the stocks; the cheaper, more "
                          r"levered market is where informed traders go first", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the method found when it was new. <bookmark mark='a'/> Joel Hasbrouck studied the thirty Dow stocks "
            "trading on the New York Stock Exchange and on regional exchanges, and found the NYSE's information share above "
            "nine tenths. <bookmark mark='b'/> It worked because quotes then moved in seconds; at today's speeds the same "
            "question needs nanosecond time stamps. <bookmark mark='c'/> And across many studies, index futures lead the "
            "stocks: informed traders go first to the cheaper, more levered market."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lead(self, d):
        hx = [-2.2, 2.4]
        head = VGroup(label(r"one-minute correlation", font_size=18, color=GREY_B), label(r"value", font_size=18,
                                                                                     color=GREY_B))
        dv = d["dollar_vol_min"]
        ratio = dv["perp"] / dv["spot"]
        tab = VGroup(head,
                     VGroup(label(r"perpetual last minute, spot this minute", font_size=19, color=PERP_C),
                            MathTex(f"{d['lead_perp']:+.3f}", font_size=26)),
                     VGroup(label(r"spot last minute, perpetual this minute", font_size=19, color=SPOT_C),
                            MathTex(f"{d['lead_spot']:+.3f}", font_size=26)),
                     VGroup(label(r"perpetual's dollar volume over spot's", font_size=19), MathTex(f"{ratio:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.8 * j, 0])
        with self.voiceover(
            "What one-minute data can still say. <bookmark mark='a'/> The perpetual's last minute predicts spot's next "
            f"minute with a correlation of {d['lead_perp']:+.3f}; the reverse is {d['lead_spot']:+.3f}. Tiny, but "
            f"asymmetric. <bookmark mark='b'/> And the perpetual trades {ratio:.1f} times spot's dollar volume. The "
            "residue of a lead lasting seconds points the same way: the derivative, where leverage is cheap and "
            "volume concentrates, moves first."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def basis(self, d):
        import numpy as np
        ms = d["months"]
        x = np.arange(len(ms))
        b = np.array([m["basis_bp"] for m in ms])
        lim = float(np.ceil(np.abs(b).max() / 5) * 5)
        g = axes([0, len(ms) - 1], [-lim, lim], x_length=8.0, y_length=4.0, xlabel=r"2021--2024, by month",
                 ylabel=r"perpetual less spot, bp", xticks=[0, 12, 24, 36], yticks=[-lim, 0, lim],
                 xfmt=lambda v: str(2021 + int(v) // 12), yfmt=lambda v: f"{v:.0f}", font_size=15)
        g.move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.12, height=max(1e-3, abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])),
                                  fill_color=GOOD if v > 0 else BAD, fill_opacity=0.8, stroke_width=0)
                        .move_to(ax.c2p(i, v / 2)) for i, v in enumerate(b)])
        hi_m, lo_m = ms[int(np.argmax(b))]["month"], ms[int(np.argmin(b))]["month"]
        with self.voiceover(
            "What holds the two prices together. <bookmark mark='a'/> A perpetual future never expires; instead, every "
            "eight hours longs pay shorts a funding rate when the perpetual trades above spot, and shorts pay longs when "
            "it trades below. The monthly average basis stays within a few basis points: largest in "
            f"{hi_m}, in the bull market, most negative in {lo_m}. Funding is the arbitrage, paid on a schedule; Part "
            "thirty-nine builds it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if v > 0 else UP) for b_, v in zip(bars, b)], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two markets: when the basis widens, market A closes 90\% of it and market B 10\%. Which has the "
                       r"larger information share, and roughly what is it?")
        with self.voiceover(
            "Pause and predict. Two markets: when the basis widens, market A closes ninety percent of it and market B "
            "ten. Which has the larger information share, and roughly what is it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
