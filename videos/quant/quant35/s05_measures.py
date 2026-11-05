from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (ASK_C, BAD, BID_C, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C, fit_right,
                                         illustration, load)


class Measures(VoiceoverScene):
    def construct(self):
        m = load("measures")
        self.card()
        self.roll()
        self.bounce()
        self.power()
        self.others()
        self.table(m)
        self.verdict(m)
        self.amihud_plot(m)
        self.decompose()
        self.question()

    def card(self):
        c = chapter_card(4, r"Measuring the spread from prices alone", r"Can a researcher with only daily closes tell how "
                         r"liquid a market is?", part=PART)
        with self.voiceover("Chapter four. Most historical data has no quotes, only prices and volumes. Microstructure "
                            "built estimators of liquidity from those alone. Here are three, tested where the truth is "
                            "known."):
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
        with self.voiceover(
            "Richard Roll's estimator, which Part thirty-three met as a warning. <bookmark mark='a'/> Trades print at "
            "the bid or the ask around an efficient price. <bookmark mark='b'/> The bounce makes successive price "
            "changes negatively correlated, by a quarter of the spread squared. <bookmark mark='c'/> So the spread is "
            "twice the root of minus the autocovariance: a spread from prices alone."
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
                cmath(r"\text{SPY}", r":", rf"\sigma = 1.2\%,\ s = 0.33\ \text{{bp}}\ \Rightarrow\ T \approx 10^{{{math.log10(T_days):.0f}}}"
                      r"\ \text{days}", font_size=30, colors={r"\text{SPY}": BAD})]
        whys = [why(r"the signal is a quarter of the spread squared; the noise in a sample autocovariance of $T$ daily "
                    r"changes is about the daily variance over $\sqrt T$"),
                why(r"to see the signal at two standard errors, the sample must be this long"),
                why(r"for the most liquid fund, about a trillion days, billions of years: the bounce is unmeasurable at "
                    r"this frequency, so the estimate is all noise and reversal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How hopeless is it? <bookmark mark='a'/> The signal is a quarter of the spread squared. The noise in a "
            "sample autocovariance is about the daily variance over the root of the sample length. "
            "<bookmark mark='b'/> So to see the spread at two standard errors you need a sample this long. "
            "<bookmark mark='c'/> For SPY, a daily volatility of one point two percent and a spread of a third of a basis "
            "point: about a trillion days, billions of years. Roll's estimator works when the spread is a meaningful "
            "fraction of the daily move, as it was for many stocks in the 1980s, and for small, illiquid securities "
            "today."
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
                cmath(r"\text{truth}", r":", r"\text{the quoted spread: one cent on the price}", font_size=32,
                      colors={r"\text{truth}": GOOD})]
        whys = [why(r"Corwin and Schultz (2012): a day's high is usually a buy at the ask, its low a sell at the bid; the "
                    r"range has a volatility part that grows with time and a spread part that does not"),
                why(r"Amihud (2002): the price move per dollar traded, a daily cousin of Kyle's lambda"),
                why(r"for the most traded US ETFs the quoted spread is one cent: a fraction of a basis point")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Two more. <bookmark mark='a'/> Shane Corwin and Paul Schultz read the spread from daily highs and lows: the "
            "high is usually a buy at the ask, the low a sell at the bid, and the range has a volatility part that grows "
            "with time and a spread part that does not. <bookmark mark='b'/> Yakov Amihud's illiquidity: the price move "
            "per dollar traded, a daily version of Kyle's lambda. <bookmark mark='c'/> And the truth to test them "
            "against: the most traded American funds are quoted one cent wide, a fraction of a basis point."
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

    def table(self, m):
        rows = m["etfs"]
        hx = [-4.6, -2.4, -0.2, 2.0, 4.6]
        head = VGroup(label(r"ETF", font_size=16, color=GREY_B), label(r"\$ volume a day", font_size=16, color=GREY_B),
                      label(r"Roll, bp", font_size=16, color=HURDLE), label(r"Corwin--Schultz, bp", font_size=16,
                                                                          color=PRICE_C),
                      label(r"Amihud, per \$bn", font_size=16, color=FLOW_C))
        tab = VGroup(head)
        for r in rows:
            dv = r["dollar_vol"]
            dvs = rf"{dv / 1e9:.1f}\text{{bn}}" if dv >= 1e9 else rf"{dv / 1e6:.0f}\text{{m}}"
            roll = r["roll_bp"]
            rs = f"{roll:.0f}" if np.isfinite(roll) else r"\text{n/a}"
            tab.add(VGroup(label(r["sym"], font_size=18), MathTex(dvs, font_size=22), MathTex(rs, font_size=22),
                           MathTex(f"{r['cs_bp']:.0f}", font_size=22), MathTex(f"{r['amihud']:.2g}", font_size=22)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.7 - 0.5 * j, 0])
        foot = wrapped_label(r"Yahoo Finance daily bars, 2015--2020; n/a where the autocovariance is positive and Roll's "
                             r"formula has no answer", 11.4, 15, GREY_A).to_edge(DOWN, buff=0.35)
        spy = rows[0]
        with self.voiceover(
            "Ten American funds, from the most traded to the least, 2015 to 2020. <bookmark mark='a'/> Roll's estimator "
            f"puts the spread of SPY, the most liquid fund in the world, at {spy['roll_bp']:.0f} basis points; its "
            "quoted spread is about a third of one. For two funds it has no answer at all. "
            "<bookmark mark='b'/> Corwin and Schultz do better, but still say "
            f"{spy['cs_bp']:.0f}. <bookmark mark='c'/> Amihud's measure, by contrast, ranks the funds almost exactly "
            "by how much they trade."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot), LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]],
                                                                 lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:]], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[4]) for r_ in tab[1:]], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self, m):
        tick = m["btc_tick_bp"]
        rows = [cmath(r"\text{daily Roll}", r"\approx", r"\text{daily reversal, not the bounce}", font_size=32,
                      colors={r"\text{daily Roll}": BAD}),
                cmath(r"\text{daily high--low}", r"\approx", r"\text{volatility, not the spread}", font_size=32,
                      colors={r"\text{daily high--low}": BAD}),
                cmath(r"\text{BTC, one minute}", r":", rf"\text{{tick}} = {tick:.4f}\ \text{{bp}};\ \text{{Roll: no answer}}",
                      font_size=30)]
        whys = [why(r"a one-cent bounce on a fund that moves a percent a day is lost in the noise; what remains is any daily "
                    r"mean reversion, which the formula reads as a spread"),
                why(r"the range's spread part is tiny next to its volatility part, so small errors in the model swamp it"),
                why(r"on Bitcoin's one-minute closes the autocovariance is positive: momentum within minutes hides a "
                    r"bounce of a fraction of a tick")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why they fail here. <bookmark mark='a'/> A one-cent bounce on a fund that moves a percent a day is lost in "
            "the noise; what Roll's formula measures instead is any daily mean reversion. <bookmark mark='b'/> The "
            "high-low range is mostly volatility, so small errors in its model swamp the spread. "
            "<bookmark mark='c'/> And on Bitcoin's minutes, with a tick of a few thousandths of a basis point, the "
            "autocovariance is positive and Roll has no answer at all. These estimators were built for the wide spreads "
            "of the 1980s, and for less liquid assets they still work; for today's most liquid markets, use quotes."
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

    def amihud_plot(self, m):
        rows = m["etfs"]
        x = np.log10([r["dollar_vol"] for r in rows])
        y = np.log10([max(r["amihud"], 1e-6) for r in rows])
        g = axes([6, 11], [-6, 1], x_length=7.0, y_length=4.4, xlabel=r"$\log_{10}$ daily dollar volume",
                 ylabel=r"$\log_{10}$ Amihud, per \$bn", xticks=[6, 7, 8, 9, 10, 11], yticks=[-6, -4, -2, 0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=FLOW_C) for a, b in zip(x, y)])
        labs = VGroup(*[label(r["sym"], font_size=14, color=GREY_A).next_to(d_, UR, buff=0.05) for d_, r in zip(dots, rows)])
        b1, b0 = np.polyfit(x, y, 1)
        fit = Line(ax.c2p(6, b0 + 6 * b1), ax.c2p(11, b0 + 11 * b1), color=HURDLE, stroke_width=2)
        rho = float(np.corrcoef(x, y)[0, 1])
        st = label(rf"slope {b1:.2f}, correlation {rho:.2f}", font_size=17, color=HURDLE).to_edge(RIGHT, buff=0.4)
        st.shift(UP * 1.8)
        fit_right(st)
        with self.voiceover(
            "Amihud's measure against volume, on logarithmic scales. <bookmark mark='a'/> A tight line, with a "
            f"correlation of {rho:.2f} and a slope near minus one: the price move per dollar falls almost one for one "
            "with the dollars traded. It works because it measures impact, which scales with size, rather than a spread "
            "too small to see. That is why it became the standard liquidity measure in asset-pricing research."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), FadeIn(labs))
            self.play(Create(fit), FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def decompose(self):
        rows = [cmath(r"\text{effective}", r"=", r"2\,q\,(p - m)", font_size=36, colors={r"\text{effective}": HURDLE}),
                cmath(r"\text{realised}", r"=", r"2\,q\,(p - m_{t+\Delta})", font_size=36, colors={r"\text{realised}": GOOD}),
                cmath(r"\text{impact}", r"=", r"\text{effective} - \text{realised} = 2\,q\,(m_{t+\Delta} - m)", font_size=32,
                      colors={r"\text{impact}": BAD})]
        whys = [why(r"what a trade actually paid against the midpoint at the time, with $q = +1$ for a buy: quotes do not "
                    r"need to be estimated when they are recorded"),
                why(r"what the liquidity provider kept, measured against the midpoint a few seconds or minutes later"),
                why(r"the difference is the price impact: the part of the spread that the provider lost to information, "
                    r"Glosten and Milgrom's adverse selection, measured")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "With quotes, the spread can be taken apart. <bookmark mark='a'/> The effective spread: what a trade paid "
            "against the midpoint at the time. <bookmark mark='b'/> The realised spread: what the liquidity provider "
            "kept, measured against the midpoint a little later. <bookmark mark='c'/> And their difference, the price "
            "impact: the part of the spread lost to information. It is Glosten and Milgrom's adverse selection, measured "
            "trade by trade, and the standard way regulators and brokers report execution quality."
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
        q = pause_card(r"a stock's daily price changes have autocovariance $-0.0004$ (dollars squared). What spread does "
                       r"Roll's estimator give, and when would you trust it?")
        with self.voiceover(
            "Pause and predict. A stock's daily price changes have an autocovariance of minus four ten-thousandths of a "
            "dollar squared. What spread does Roll's estimator give, and when would you trust it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
