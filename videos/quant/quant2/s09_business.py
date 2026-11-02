from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, GAIN, LOSS, PART, TRADE, load, real_data

ROLES = [(r"quant researcher", r"finds and tests signals and models"),
         (r"quant trader", r"runs strategies, sizes risk, decides when to stop"),
         (r"quant developer", r"builds the data, the backtester, the trading systems"),
         (r"risk quant", r"models what can go wrong, sets limits"),
         (r"strat / desk quant", r"prices and hedges for a bank's trading desk"),
         (r"structurer", r"designs products for clients (Part 15)")]


class Business(VoiceoverScene):
    def construct(self):
        fe = load("fees")
        self.card()
        self.sides()
        self.fees(fe)
        self.industry()

    def card(self):
        c = chapter_card(8, r"Who earns what", r"How does each player get paid?", lit=(1982, 1990, 2000), part=PART)
        with self.voiceover("Chapter eight. Who earns what."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sides(self):
        sell = definition_card(r"Sell side", r"Banks and dealers: make markets, earn spreads and fees, structure "
                               r"products, lend to the buy side. Flow desks trade for clients' volume; exotics desks "
                               r"for margin on complex products. Agency: act for a client; principal: trade against "
                               r"them.", width=5.9, color=TRADE, font_size=21)
        buy = definition_card(r"Buy side", r"Asset managers, pension funds, insurers, hedge funds: invest money, "
                              r"for themselves or for clients, and pay the sell side to trade. Earn a fee on assets, "
                              r"and, for hedge funds, a share of profits.", width=5.9, color=QC.IDEA, font_size=21)
        pair = VGroup(sell, buy).arrange(RIGHT, buff=0.4, aligned_edge=UP).shift(UP * 1.2)
        prop = wrapped_label(r"and between them: proprietary traders and market makers, who trade only their own "
                             r"money; and retail brokers, many of which charge no commission and are paid by "
                             r"wholesalers for their customers' orders", 11.6, 23, GREY_A).next_to(pair, DOWN, buff=0.6)
        with self.voiceover(
            "The industry divides in two. The sell side, banks and dealers, makes markets, earns spreads and fees, "
            "designs products and lends to everyone else. Its flow desks live on clients' volume; its exotics "
            "desks on the margin built into complex products. <bookmark mark='a'/> The buy side invests money: "
            "asset managers, pension funds, insurers, hedge funds. It pays the sell side to trade, and charges its "
            "own clients a fee on assets, plus, for hedge funds, a share of the profits. <bookmark mark='b'/> "
            "Between them sit firms that trade only their own money, proprietary traders and market makers, and "
            "retail brokers that charge no commission because wholesalers pay them for their customers' orders."
        ) as vo:
            self.play(FadeIn(sell, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(buy, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(prop))
        self.wait(0.4)
        self.clear_scene()

    def fees(self, fe):
        ys = np.asarray(fe["years"], float)
        wg, wn = np.asarray(fe["wealth_gross"]), np.asarray(fe["wealth_net"])
        g = axes([1926, 2021], [0, 4.2], x_length=7.4, y_length=4.4, ylabel=r"\$1 invested in 1927 (log scale)",
                 xticks=[1930, 1960, 1990, 2020], yticks=[0, 1, 2, 3, 4], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: rf"\${10 ** v:,.0f}".replace(",", "{,}"), font_size=18).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        lg = curve(ax, ys, np.log10(wg), TRADE, stroke_width=3)
        ln = curve(ax, ys, np.log10(wn), LOSS, stroke_width=3)
        leg = legend([(TRADE, r"the market, no fees"), (LOSS, r"the same, after 2\% and 20\% (high-water mark)")],
                     font_size=21).to_edge(RIGHT, buff=0.35).shift(UP * 2.2)
        res = VGroup(
            MathTex(rf"\${fe['final_gross']:,.0f}\ \to\ \${fe['final_net']:,.0f}".replace(",", "{,}"), font_size=36),
            MathTex(rf"{100 * fe['geo_gross']:.1f}\%\ \to\ {100 * fe['geo_net']:.1f}\%\ \text{{a year}}", font_size=32),
            MathTex(rf"\text{{the investor keeps}}\ {100 * fe['share_kept']:.1f}\%\ \text{{of the profit}}", font_size=30,
                    color=LOSS),
            MathTex(rf"\text{{a 1\% fee instead:}}\ \${fe['final_1pct']:,.0f}".replace(",", "{,}"), font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        src = real_data(r"calendar-year returns of the US market, 1927--2020 (Ken French), as a fund's gross returns; "
                        r"fees charged yearly")
        with self.voiceover(
            "Fees compound, just like returns. Take the American market's calendar years from 1927 to 2020 as a "
            "fund's returns before fees. A dollar becomes "
            f"{fe['final_gross']:,.0f} dollars. <bookmark mark='a'/> Now charge the classic hedge-fund fee: two "
            "percent of assets every year, and twenty percent of any gain above the fund's previous peak, the "
            f"high-water mark. The same dollar becomes {fe['final_net']:,.0f}. <bookmark mark='b'/> Growth falls from "
            f"{100 * fe['geo_gross']:.1f} percent a year to {100 * fe['geo_net']:.1f}, and the investor keeps "
            f"{100 * fe['share_kept']:.1f} percent of the profit. Even a plain one percent fee leaves "
            f"{fe['final_1pct']:,.0f}. <bookmark mark='c'/> A manager who charges that much must earn a lot more than "
            "the market just to break even with an index fund, which is why fees, like costs, are charged in every "
            "Track Record result of this series."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lg), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(leg[1]), run_time=2)
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]), FadeIn(res[2]))
            self.play(FadeIn(res[3]))
            vo.wait_until("c")
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    def industry(self):
        strat = VGroup(
            label(r"Where quants work", font_size=30, color=QC.IDEA),
            label(r"systematic equity: factors and signals across thousands of stocks (Parts 24--31)", font_size=22),
            label(r"trend followers (CTAs) and macro: futures across every asset class (Part 32)", font_size=22),
            label(r"statistical arbitrage: short-horizon relative value (Part 33)", font_size=22),
            label(r"high-frequency market making and options market making (Parts 11, 38)", font_size=22),
            label(r"multi-strategy platforms: many teams, one risk budget (Part 34)", font_size=22),
            label(r"bank desks: pricing, hedging, structuring, XVA (Parts 10--21)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(LEFT, buff=0.5).shift(UP * 0.6)
        roles = VGroup(label(r"The roles", font_size=30, color=QC.HOUSE))
        for r_, what in ROLES:
            roles.add(VGroup(label(r_, font_size=23, color=QC.HOUSE), label(what, font_size=19, color=GREY_A))
                      .arrange(DOWN, aligned_edge=LEFT, buff=0.04))
        roles.arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        room = roles.get_left()[0] - 0.4 - (-7.1 + 0.5)
        if strat.width > room:
            strat.scale_to_fit_width(room).to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Where do quants work? In systematic equity, ranking thousands of stocks on signals; in trend-following "
            "and macro funds trading futures across every asset; in statistical arbitrage; in high-frequency and "
            "options market making; at multi-strategy platforms; and on banks' pricing and hedging desks. Each of "
            "these has its parts later in the series. <bookmark mark='a'/> And the jobs: the researcher who finds "
            "and tests ideas, the trader who runs them and decides when to stop, the developer who builds the "
            "systems, the risk quant who asks what can go wrong, the desk quant who prices and hedges for a bank, "
            "and the structurer who designs products. The House will need all of them."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in strat], lag_ratio=0.3, run_time=5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in roles], lag_ratio=0.3, run_time=4))
        self.wait(0.4)
        self.clear_scene()
