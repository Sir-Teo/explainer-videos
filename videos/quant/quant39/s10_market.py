from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
from videos.quant.quant39.common import (
    BAD,
    GOOD,
    PART,
    PERP_C,
    SPOT_C,
    fit_right,
    load,
)


class Market(VoiceoverScene):
    def construct(self):
        e = load("etf")
        self.card()
        self.makarov()
        self.discovery()
        self.trust(e)
        self.gbtc(e)
        self.etfs(e)
        self.cross_section()
        self.firms()
        self.question()

    def card(self):
        c = chapter_card(9, r"Venues, funds and the cross-section", r"How integrated is a market that never closes?",
                         part=PART)
        with self.voiceover(
            "Chapter nine, and the answer to the pause: capital controls. An arbitrageur must buy in one country and "
            "sell in the other, and then move the money back; Korea's limits on moving won abroad, and on foreign "
            "accounts at its exchanges, made the second leg slow and costly. A market without a closing bell can still "
            "have borders."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def makarov(self):
        cards = VGroup(
            desk_question(r"within a country, small gaps", r"exchanges in the same currency stay close: moving coins and "
                          r"cash between them is easy", width=12.4, font_size=19),
            desk_question(r"across borders, large ones", r"Igor Makarov and Antoinette Schoar documented premiums in Korea "
                          r"that peaked above 40\% in early 2018, and smaller ones in Japan, for weeks", width=12.4,
                          font_size=19),
            desk_question(r"a common driver", r"the gaps rose together when buying pressure rose: arbitrage capital, "
                          r"not information, was the scarce input", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Makarov and Schoar: crypto arbitrage", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Igor Makarov and Antoinette Schoar's study of crypto arbitrage. <bookmark mark='a'/> Within a country, "
            "exchanges in the same currency stayed close, because coins and cash move easily between them. "
            "<bookmark mark='b'/> Across borders, gaps were large and lasting: premiums in Korea that peaked above forty "
            "percent in early twenty eighteen. <bookmark mark='c'/> And the gaps rose together when buying pressure rose. "
            "What was scarce was arbitrage capital that could cross the border, not information."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def discovery(self):
        rows = [cmath(r"\text{information share}", r":", r"\text{perpetual} \gg \text{spot}", font_size=38,
                      colors={r"\text{perpetual} \gg \text{spot}": PERP_C}),
                cmath(r"\text{pools}", r":", r"\text{follow, by arbitrage}", font_size=38),
                cmath(r"\text{weekends}", r":", r"\text{crypto moves, CME and ETFs are shut}", font_size=36)]
        whys = [why(r"Part 35's Hasbrouck information shares: Bitcoin's price is discovered mostly on the perpetual, "
                    r"where leverage is cheapest"),
                why(r"on-chain pools rarely lead: Chapter 3's arbitrageurs carry the price to them"),
                why(r"so the listed products price off a market that kept trading while they were closed: their Monday "
                    r"opens jump")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Where the price is made. <bookmark mark='a'/> Part thirty-five's information shares found Bitcoin's price "
            "discovered mostly on the perpetual, where leverage is cheapest. <bookmark mark='b'/> Pools on chain rarely "
            "lead; Chapter three's arbitrageurs carry the price to them. <bookmark mark='c'/> And on weekends crypto keeps "
            "trading while Chicago's futures and the funds are closed, so the listed products open on Monday wherever "
            "crypto went."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def trust(self, e):
        rows = [cmath(r"\text{GBTC, 2013--2024}", r":", r"\text{a trust: shares created, never redeemed}", font_size=34,
                      colors={r"\text{GBTC, 2013--2024}": SPOT_C}),
                cmath(r"\text{no redemption}", r"\Rightarrow", r"\text{no enforced redemption band}", font_size=38,
                      colors={r"\text{no enforced redemption band}": BAD}),
                cmath(r"\text{fee}", r"=", r"2\%\ \text{a year}", font_size=40)]
        whys = [why(r"Grayscale's Bitcoin trust traded over the counter; investors could buy shares but not hand them "
                    r"back for bitcoin"),
                why('no ordinary redemption mechanism tightly enforced a NAV arbitrage band; prices still reflected claims on the holdings and other constraints'),
                why(r"while holders paid the trust's fee on its full value")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Before the funds, a trust. <bookmark mark='a'/> Grayscale's Bitcoin trust created shares but never redeemed "
            "them. <bookmark mark='b'/> Without Part thirty-eight's creation and redemption, nothing tied its price to "
            "the bitcoin it held: it traded at premiums for years, and at a discount of close to half its value in "
            "twenty twenty-two, as reported. <bookmark mark='c'/> All the while its holders paid a fee of two percent a "
            "year on the full value."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def gbtc(self, e):
        gb = e["gbtc"]
        d = np.asarray(gb["d"], int)
        import datetime as dt
        days = [dt.datetime.strptime(str(int(v)), "%Y%m%d").date() for v in d]
        yr = np.array([v.year + (v-dt.date(v.year,1,1)).days / (dt.date(v.year+1,1,1)-dt.date(v.year,1,1)).days for v in days])
        r = np.asarray(gb["ratio"], float)
        g = axes([2022, 2025], [0.5, 2.0], x_length=7.6, y_length=4.0, xlabel=r"GBTC's price over Bitcoin's",
                 ylabel=r"end of 2022 = 1", xticks=[2022, 2023, 2024, 2025], yticks=[0.5, 1.0, 1.5, 2.0], font_size=16)
        g.move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, yr, r, SPOT_C, stroke_width=2.5)
        marks = VGroup(label(r"Aug 2023: the court rules for Grayscale", font_size=17, color=GREY_A),
                       label(r"10 Jan 2024: spot ETFs approved", font_size=17, color=GOOD))
        marks.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.4)
        fit_right(marks)
        with self.voiceover(
            f"Read exactly what was computed. GBTC's market close divided by Binance's Bitcoin daily close is normalized to one near the end of twenty twenty-two. <bookmark mark='a'/> The ratio rose during twenty twenty-three; the August court decision and January approval are dated context. <bookmark mark='b'/> Near January tenth, twenty twenty-four, the ratio is {100*gb['rise']:.0f} percent above that chosen base. This is not a measured NAV discount: the calculation omits bitcoin entitlement per share, fee erosion and synchronized valuation clocks. The labels do not identify the court decision's causal price effect. Conversion changed redemption access, while fees can change bitcoin per share over time."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
        self.wait(0.4)
        self.clear_scene()

    def etfs(self, e):
        ib = e["ibit"]
        rows = [cmath(r"\text{11 January 2024}", r":", '\\text{spot Bitcoin products begin trading}', font_size=34),
                cmath(r"\text{IBIT, first day}", r"\approx", rf"\${ib['first_day_bn']:.1f}\text{{bn proxy}}", font_size=38,
                      colors={r"\text{IBIT, first day}": GOOD}),
                cmath(r"\text{2024 average}", r"\approx", rf"\${ib['mean_bn']:.1f}\text{{bn/day proxy}}", font_size=38),
                cmath(r"\text{creation}", r":", '\\text{check current product creation terms}', font_size=36)]
        whys = [why('the SEC approval order is dated 10 January 2024; trading began subsequently and launch dates differ by product'),
                why('Yahoo daily close times share volume on the first observed day; a turnover proxy, not exact dollar volume or inflow'),
                why('mean daily close-times-volume proxy over the selected 2024 observations'),
                why('authorised participants face product-specific cash, settlement, custody, funding and eligibility terms')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"Spot Bitcoin exchange-traded products began United States trading in January twenty twenty-four after the January tenth approval order. <bookmark mark='a'/> Approval and first trading are different dates, and not every approved product launched together. <bookmark mark='b'/> For IBIT, daily volume times closing price is {ib['first_day_bn']:.1f} billion dollars on the first observed day. <bookmark mark='c'/> Its mean is {ib['mean_bn']:.1f} billion over the selected twenty twenty-four observations. This is a close-times-volume turnover proxy, not exact traded dollar value or fund inflow. <bookmark mark='d'/> Creation and redemption terms, cash funding, costs and current eligibility must be checked against actual product documents; listing approval is not investment approval."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def cross_section(self):
        cards = VGroup(
            desk_question(r"three factors", r"Liu, Tsyvinski and Wu found that a crypto market factor, a size factor and "
                          r"a momentum factor price the cross-section of coins", width=12.4, font_size=19),
            desk_question(r"not the stock factors", r"Liu and Tsyvinski found crypto returns barely exposed to equity, "
                          r"currency or commodity factors, and predicted by momentum and attention", width=12.4,
                          font_size=19),
            desk_question('validation discipline', 'predictive fit needs past-only selection, survivorship controls, net costs and independent validation; no prior strategy outcome is used as evidence for this desk', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Research on token returns. <bookmark mark='a'/> Liu, Tsyvinski and Wu study crypto market, size and momentum factors in their chosen samples; factor fit is an empirical result rather than a universal pricing law. <bookmark mark='b'/> Liu and Tsyvinski report distinctive exposures, momentum and attention relationships for their period. Market composition, survivorship, trading costs and subsequent structural change limit extrapolation. <bookmark mark='c'/> A predictive model from another part is not independent validation of this desk. We do not use sealed strategy outcomes here, and descriptive cross-sectional patterns do not establish implementable net alpha or justify an additional market trial."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        cards = VGroup(
            desk_question(r"trading firms in the record", r"the SEC found, in a settled order of December 2024, that "
                          r"Tai Mo Shan, a Jump Trading affiliate, bought UST in May 2021 in a way that misled investors "
                          r"about its peg; it agreed to pay about \$123 million without admitting or denying the findings", width=12.4,
                          font_size=18),
            desk_question(r"market makers for tokens", r"examine compensation, token options, inventory and conflicts; "
                          r"quoted volume alone does not establish independent executable liquidity",
                          width=12.4, font_size=18),
            desk_question(r"the exchange as everything", r"custody, execution, collateral and clearing can share one venue; "
                          r"map legal claims and operational dependencies before treating functions as diversified", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "Firms, from the public record. <bookmark mark='a'/> In a settled order of December twenty twenty-four, the "
            "SEC found that Tai Mo Shan, an affiliate of Jump Trading, had bought UST in May twenty twenty-one in a way "
            "that misled investors about the peg's mechanism; it agreed to pay about a hundred and twenty-three million dollars "
            "without admitting or denying the findings. <bookmark mark='b'/> For token market making, examine compensation, "
            "options, inventory and conflicts. Quoted volume alone does not establish independent executable liquidity. "
            "<bookmark mark='c'/> A venue can combine custody, execution, collateral and clearing. Map legal claims and "
            "operational dependencies before calling these functions diversified."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"the House opens a digital-assets desk to run Chapter 7's carry book and to provide liquidity in "
                       r"pools. Which three limits should its rule set before the first trade?")
        with self.voiceover(
            "Pause and predict. The House opens a digital-assets desk to run Chapter seven's carry book and to provide "
            "liquidity in pools. Which three limits should its rule set before the first trade?"
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
