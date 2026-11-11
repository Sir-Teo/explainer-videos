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
        self.add(c)
        with self.voiceover("Chapter seven. Bitcoin trades both as spot and as a perpetual future. Arbitrage and funding link their prices, but differences can persist. Hasbrouck's information shares describe how a specified cointegrated model attributes common-trend innovation variance. They require synchronized prices, a stable error-correction specification and residual assumptions; they are not a causal verdict about where every piece of news first appeared."):
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
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The maintained model. <bookmark mark='a'/> Each log price contains a common stochastic trend plus market-specific components. <bookmark mark='b'/> Specify integrated prices with a common innovation. <bookmark mark='c'/> Assume their difference is stationary over the estimation window, with the chosen cointegrating vector. Arbitrage is a motivation, not a proof of that statistical assumption. Time-varying funding, basis risk and regime changes can weaken the specification; no cointegration or stability test is supplied by these plots."
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
        self.add(rows[0], whys[0])
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
        self.add(rows[0], whys[0])
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
        self.add(g, bars[0])
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
                cmath(r"\text{within-bar adjustment}", r":", r"\text{unresolved by one-minute observations}", font_size=32),
                cmath(r"\text{finer data}", r"\Rightarrow", '\\text{potentially different attribution}', font_size=34, colors={r"\text{finer data}": GOOD})]
        whys = [why(r"within the minute, the two returns are almost the same number: their shocks are simultaneous at this "
                    r"resolution"),
                why('fast adjustment is a possible mechanism; these minute observations do not estimate a particular millisecond speed'),
                why(r"studies with tick data find the futures market usually leads; the House would need trade-level data "
                    r"to say so here")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Sampling limits the interpretation. <bookmark mark='a'/> The contemporaneous return correlation is {d['corr0']:.3f}; both prices can react within the same minute. <bookmark mark='b'/> Correlated residuals make Cholesky-order attribution ambiguous in this fitted model. Minute data do not establish a particular millisecond adjustment speed. <bookmark mark='c'/> Finer synchronized data may help, but do not guarantee narrow bounds or causal identification. The model, quote-versus-trade choice, clock quality and stability still matter. A wide range is an attribution limitation, not a proof that the markets have identical roles."""
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
                          r"others followed", width=12.4, font_size=25),
            desk_question(r"why the method worked there", 'the cited historical sampling and specification produced informative attribution; modern studies need appropriately synchronized data, without a universal timestamp threshold',
                          width=12.4, font_size=25),
            desk_question(r"futures and spot, generally", 'some cited settings find a leading futures contribution; turnover, leverage and cost are possible explanations, not universal causal identification', width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "An attributed historical application. <bookmark mark='a'/> Hasbrouck's study of Dow stocks and regional venues reported a dominant NYSE contribution in that setting. <bookmark mark='b'/> Historical results depend on the sample, quote records and econometric specification. Modern cross-venue studies need clocks and sampling suitable for their question; nanosecond labels alone do not guarantee synchronization or identification. <bookmark mark='c'/> Other studies often find an important futures role in particular markets. Lower transaction costs and leverage are possible explanations, not a universal causal conclusion from our Bitcoin turnover figures."
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
        self.add(tab[0], tab[1])
        with self.voiceover(
            f"""A descriptive lead-lag summary. <bookmark mark='a'/> The stored correlations are {d['lead_perp']:+.3f} for perpetual followed by spot and {d['lead_spot']:+.3f} for the reverse. The helper first filters non-one-minute increments, then lags the retained sequence. It does not ensure every adjacent retained pair is consecutive in calendar time, so gaps can compress the lag clock. <bookmark mark='b'/> Perpetual dollar turnover is {ratio:.1f} times spot turnover on matched timestamps. Neither turnover nor these small, untested correlations establishes causal price leadership or a profitable next-minute forecast."""
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
        self.add(g, bars[0])
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
        eq = MathTex('\\Delta p=\\alpha(p_A-p_B)_{-1}+\\cdots+e,\\quad\\alpha=(-0.9,0.1)', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('Derive normalized common-trend weights orthogonal to alpha. For information shares additionally stipulate equal independent innovation variances; distinguish the two shares.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover("Pause and predict. With adjustment loadings minus point nine and point one, find the normalized common-trend weights. Then assume equal independent innovation variances and derive B's information share. Why are the two numbers different?"):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
