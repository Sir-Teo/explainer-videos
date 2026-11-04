from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import (BAD, BOND_C, CARRY_C, GOOD, HURDLE, PART, SIXTY_C, SPY_C, TREND_C, fit_right,
                                         load)

GCOL = {"equities": QC.SPOT, "bonds": QC.DELTA, "credit": QC.OPTION, "commodities": QC.P, "currencies": QC.REALIZED}


class Trend(VoiceoverScene):
    def construct(self):
        p, t = load("panel"), load("trend")
        self.card()
        self.panel(p)
        self.rule()
        self.curves(t)
        self.configs(t)
        self.classes(t)
        self.horizons()
        self.century(t)
        self.firms()
        self.business()
        self.question()

    def card(self):
        c = chapter_card(1, r"Trend following", r"Can a rule that only looks at past prices earn a premium?", part=PART)
        with self.voiceover("Chapter one. Trend following is the oldest systematic strategy, and the simplest: buy what "
                            "has been rising, sell what has been falling, in every market you can trade."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def panel(self, p):
        rows = VGroup()
        for g, syms in p["classes"].items():
            txt = r",\ ".join(syms)
            sr = np.mean([p["rows"][s]["sharpe"] for s in syms])
            rows.add(VGroup(label(g, font_size=24, color=GCOL[g]), label(r"\texttt{" + txt.replace(r",\ ", ", ") + "}",
                                                                           font_size=18, color=GREY_A),
                            MathTex(rf"\overline{{SR}} = {sr:+.2f}", font_size=24, color=GCOL[g])))
        for j, r_ in enumerate(rows):
            r_[0].move_to([-5.0, 2.0 - 0.85 * j, 0], aligned_edge=LEFT)
            r_[1].move_to([-2.4, 2.0 - 0.85 * j, 0], aligned_edge=LEFT)
            r_[2].move_to([4.4, 2.0 - 0.85 * j, 0], aligned_edge=LEFT)
        head = label(r"The House's macro panel: 23 funds, five asset classes", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(rf"US-listed ETFs, dividend-adjusted daily closes, excess of 3-month T-bills; research years "
                             rf"2006--2020 ({p['n_days']:,} days), 2021--2025 sealed; $\overline{{SR}}$: the class's average "
                             r"Sharpe ratio of simply holding each fund", 11.8, 16, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The House's panel. <bookmark mark='a'/> Twenty-three exchange-traded funds that stand in for the futures a "
            "macro fund trades: equity indices at home and abroad, Treasuries of three kinds, corporate credit, "
            "commodities from gold to natural gas, and seven currencies. Daily returns over Treasury bills, from 2006, "
            "with 2021 to 2025 sealed. <bookmark mark='b'/> Simply holding them was a mixed experience: stocks, bonds "
            "and credit paid; most commodities and currencies did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in rows], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def rule(self):
        rows = [cmath(r"s_{i,t}", r"=", r"\operatorname{sign}\big(r_{i,\,t-252\to t}\big)", font_size=38,
                      colors={r"s_{i,t}": TREND_C}),
                cmath(r"x_{i,t}", r"=", r"s_{i,t}\cdot\frac{40\%}{\hat\sigma_{i,t}}", font_size=38),
                cmath(r"r^{\text{TSMOM}}_{t+1}", r"=", r"\frac1{N_t}\textstyle\sum_i x_{i,t}\, r_{i,t+1}", font_size=36),
                cmath(r"\text{scale}", r":", r"\text{the whole book to } 10\%\ \text{a year, ex ante}", font_size=32)]
        whys = [why(r"each market long if its own excess return over the past year was positive, short if negative: "
                    r"time-series momentum (Moskowitz, Ooi and Pedersen 2012), not cross-sectional"),
                why(r"sized so each position would have 40\% annual volatility, from an exponentially weighted volatility "
                    r"with a 60-day centre of mass: a calm currency gets a large position, natural gas a small one"),
                why(r"an equal risk budget for every market with a signal, rebalanced at each month end"),
                why(r"so the book can be compared with others at the same risk")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The rule, as Tobias Moskowitz, Yao Hua Ooi and Lasse Pedersen wrote it down in 2012. <bookmark mark='a'/> "
            "Each market is long if its own excess return over the past year was positive, short if negative. Not "
            "which market did best, as in Part twenty-four's momentum, but whether each did well against cash: "
            "time-series momentum. <bookmark mark='b'/> Each position is sized to the same risk, forty percent a year "
            "on its own, so a calm currency gets a large position and natural gas a small one. "
            "<bookmark mark='c'/> Every market gets an equal risk budget, rebalanced monthly. <bookmark mark='d'/> And "
            "the whole book is scaled to ten percent volatility, so it can be compared with anything else."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def curves(self, t):
        md = np.asarray(t["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        ys = {k: 100 * np.asarray(v, float) for k, v in t["cum"].items()}
        lo = float(np.floor(min(y.min() for y in ys.values()) / 50) * 50)
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 50) * 50)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"2007--2020, the research years",
                 ylabel=r"cumulative excess return, \%", xticks=[2008, 2012, 2016, 2020], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        cols = {"trend": TREND_C, "spy": SPY_C, "6040": SIXTY_C}
        names = {"trend": r"trend, at 10\% volatility", "spy": r"US stocks (SPY)", "6040": r"60/40"}
        lines = VGroup(*[curve(ax, x, ys[k], cols[k], stroke_width=3) for k in ("spy", "6040", "trend")])
        leg = legend([(cols[k], names[k]) for k in ("trend", "spy", "6040")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 1.6)
        fit_right(leg)
        m, s, sx = t["main"], t["spy"], t["sixty"]
        st = VGroup(label(rf"Sharpe: trend {m['sharpe']:.2f}, SPY {s['sharpe']:.2f}, 60/40 {sx['sharpe']:.2f}",
                          font_size=16, color=GREY_A),
                    label(rf"correlation of trend with SPY: {t['corr_spy']:+.2f} (monthly)", font_size=16, color=GREY_A),
                    label(rf"worst drawdown: trend {100 * m['maxdd']:.0f}\%, SPY {100 * s['maxdd']:.0f}\%", font_size=16,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        st.next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(st)
        with self.voiceover(
            "Over the research years. <bookmark mark='a'/> Stocks rose most, at twice the risk. The trend book rose "
            "in 2008 while everything else fell, then went sideways for most of the decade after. "
            f"<bookmark mark='b'/> Its Sharpe ratio was {m['sharpe']:.2f}, about the same as the stock market's "
            f"{s['sharpe']:.2f}, and below sixty-forty's {sx['sharpe']:.2f}, a period kind to balanced portfolios. But its "
            f"correlation with stocks was {t['corr_spy']:+.2f}: an equally good return stream that moves independently "
            "of the market. That independence is what a trend fund sells."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def configs(self, t):
        cf = t["configs"]
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(label(r"lookback", font_size=18, color=GREY_B), label(r"sign of the return", font_size=18,
                                                                          color=TREND_C),
                      label(r"return over its volatility", font_size=18, color=TREND_C))
        tab = VGroup(head)
        for lb, nm in ((21, r"1 month"), (63, r"3 months"), (252, r"12 months")):
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{cf[f'{lb}/sign']['sharpe']:.2f}", font_size=28),
                           MathTex(f"{cf[f'{lb}/linear']['sharpe']:.2f}", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(rf"Sharpe ratios 2007--2020, each book scaled to 10\% volatility; these {t['n_trials']} "
                             r"configurations are the trials charged to the registered rule (Chapter 9)", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How sensitive is it to the choices? <bookmark mark='a'/> Three lookbacks and two ways to size the signal. "
            "<bookmark mark='b'/> A one-month trend barely worked here. Three months and twelve months did, and the "
            "plain sign did as well as the more refined size. <bookmark mark='c'/> Six configurations, and all six are "
            "trials: the twelve-month sign rule is the one registered, and the counter will be charged for the other "
            "five."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[0]) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[1:])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def classes(self, t):
        gr = t["groups"]
        keys = list(gr)
        mx = max(abs(gr[k]["sharpe"]) for k in keys)
        bars = VGroup()
        for j, k in enumerate(keys):
            v = gr[k]["sharpe"]
            r = Rectangle(width=max(abs(v) * 6.0 / mx, 0.03), height=0.5, fill_color=GCOL[k], fill_opacity=0.85,
                          stroke_width=0).move_to([-1.0, 1.8 - 0.9 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(k, font_size=22, color=GCOL[k]).next_to(r, LEFT, buff=0.3).align_to([-1.3, 0, 0], RIGHT),
                            r, MathTex(f"{v:.2f}", font_size=26).next_to(r, RIGHT, buff=0.2)))
        head = label(r"Trend within each asset class, Sharpe ratio, 2007--2020", font_size=28).to_edge(UP, buff=0.5)
        foot = wrapped_label(rf"the whole book: {t['main']['sharpe']:.2f}; each class's book on its own, scaled to 10\%",
                             11.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        cu = gr["currencies"]["sharpe"]
        with self.voiceover(
            "By asset class. <bookmark mark='a'/> Credit and commodities trended most; equities and bonds less; "
            f"currencies, a Sharpe ratio of {cu:.2f}, not at all in these years. <bookmark mark='b'/> The whole is better "
            "than most of its parts, because the classes' trends are weakly related: breadth, in Part thirty-one's "
            "sense, comes from markets that trend at different times."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def century(self, t):
        a = t["aqr"]
        cards = VGroup(
            desk_question(r"a century of evidence", r"Hurst, Ooi and Pedersen (2017) rebuilt time-series momentum on "
                          r"67 markets back to 1880 and found it consistently profitable decade after decade, through "
                          r"wars, depressions and inflations", width=12.4, font_size=19),
            desk_question(r"AQR's published series", rf"time-series momentum across 58 futures and forwards, as "
                          rf"published from {a['first'] // 100}: a Sharpe ratio of {a['sharpe']:.2f} through 2020, "
                          r"before fees and costs", width=12.4, font_size=19),
            desk_question(r"why the House's is lower", r"23 funds instead of 58 futures markets: less breadth, "
                          r"currencies that did not trend, and a period, 2009--2020, that was hard for every trend "
                          r"follower", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Is fourteen years enough? <bookmark mark='a'/> Brian Hurst, Ooi and Pedersen rebuilt the strategy on "
            "sixty-seven markets back to 1880, and found it profitable decade after decade, through wars, depressions "
            f"and inflations. <bookmark mark='b'/> AQR's published series, across fifty-eight futures markets from 1985, "
            f"has a Sharpe ratio of {a['sharpe']:.2f} through 2020, before fees and costs. <bookmark mark='c'/> The "
            "House's is lower: fewer markets, currencies that did not trend, and a decade after 2008 that was hard for "
            "every trend follower."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        cards = VGroup(
            firm_card(r"AHL and Man", r"founded in 1987 by Michael Adam, David Harding and Martin Lueck to trade futures "
                      r"trends systematically; bought by the Man Group, whose Man AHL is one of the largest managed-futures "
                      r"businesses", source=r"Man Group annual reports", width=6.2, font_size=20),
            firm_card(r"Winton", r"founded by David Harding in 1997 after AHL; for years among the largest trend "
                      r"followers, it later moved away from pure trend following toward other systematic signals, as reported",
                      source=r"company statements; press reports", width=6.2, font_size=20),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        with self.voiceover(
            "The firm files. <bookmark mark='a'/> AHL was founded in 1987 by Michael Adam, David Harding and Martin Lueck "
            "to trade futures trends by rule, and became part of the Man Group, where Man AHL is one of the largest "
            "managed-futures businesses. <bookmark mark='b'/> Harding left to found Winton in 1997; for years among the "
            "largest trend followers, it later moved away from pure trend toward other systematic signals, after the "
            "long, flat decade that followed 2008."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
        self.wait(0.4)
        self.clear_scene()


    def business(self):
        cards = VGroup(
            desk_question(r"the instruments", r"futures and forwards on a hundred or more markets: cheap to trade, easy to "
                          r"short, and margined, so a 10\% volatility book needs only a fraction of its notional in cash",
                          width=12.4, font_size=19),
            desk_question(r"the costs", r"a twelve-month signal turns over a few times a year per market; the roll of "
                          r"each futures contract adds trades of its own; both are small next to the fees", width=12.4,
                          font_size=19),
            desk_question(r"the fees", r"historically a 2\% management fee and 20\% of profits; on a book earning a "
                          r"Sharpe ratio of 0.5 at 10\% volatility, that is most of the excess return, which is why "
                          r"cheaper versions following the same rules now compete", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How a trend fund actually runs. <bookmark mark='a'/> It trades futures and forwards on a hundred or more "
            "markets: cheap to trade, easy to short, and margined, so the cash mostly sits in Treasury bills. "
            "<bookmark mark='b'/> A twelve-month signal turns over only a few times a year in each market; the rolls of "
            "the futures add trades of their own. <bookmark mark='c'/> And the fees were large: historically two percent "
            "of assets and twenty percent of profits. On a book earning five percent over bills, that is most of it, "
            "which is why cheaper funds that follow the same rules now compete for the same investors."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def horizons(self):
        cards = VGroup(
            desk_question(r"fast trends", r"weeks: respond quickly to a new crisis, but turn over often and are whipsawed "
                          r"by noise; Chapter 1's one-month signal barely paid", width=12.4, font_size=19),
            desk_question(r"slow trends", r"a year: cheap to trade and robust, but late to turn; they caught 2008 and miss "
                          r"crashes of days", width=12.4, font_size=19),
            desk_question(r"two centuries", r"Lemp\'eri\`ere and coauthors at Capital Fund Management (2014) traced trend "
                          r"profits across horizons and asset classes back to 1800, as a persistent anomaly", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Horizon is the main design choice. <bookmark mark='a'/> Fast trends, over weeks, turn quickly when a new "
            "crisis starts, but trade often and are whipsawed by noise; here the one-month signal barely paid. "
            "<bookmark mark='b'/> Slow trends, over a year, are cheap and robust but late to turn. Most funds blend "
            "several speeds. <bookmark mark='c'/> And the evidence is long: Yves Lemperiere and coauthors at Capital Fund "
            "Management traced trend profits across horizons and asset classes back to 1800."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a trend book holds 23 markets, each with 40\% volatility on its own, and has 10\% volatility in "
                       r"total. Are its positions correlated, uncorrelated, or offsetting?")
        with self.voiceover(
            "Pause and predict. A trend book holds twenty-three markets, each sized to forty percent volatility on its "
            "own, and the whole has ten percent. Are its positions correlated, uncorrelated, or offsetting?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
