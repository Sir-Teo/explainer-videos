from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (MAKER_C, BAD, ETF_C, GOOD, HURDLE, PART, load)


class ETF(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanics()
        self.band()
        self.worked()
        self.who()
        self.in_kind()
        self.inav()
        self.march()
        self.discovery()
        self.fed()
        self.leveraged()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(5, r"Making markets in ETFs", r"What keeps a fund's price near the value of what it holds?",
                         part=PART)
        with self.voiceover("Chapter five, and the answer to the pause: an authorised participant could buy the cheap "
                            "ETF, redeem it for the bonds, and sell the bonds, if the bonds could really be sold at their "
                            "published value. In March twenty twenty, often they could not. Exchange-traded funds are "
                            "market making with a second exit."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        rows = [cmath(r"\text{creation}", r":", r"\text{basket of securities} \to \text{ETF shares}", font_size=36,
                      colors={r"\text{creation}": GOOD}),
                cmath(r"\text{redemption}", r":", r"\text{ETF shares} \to \text{basket}", font_size=36,
                      colors={r"\text{redemption}": BAD}),
                cmath(r"\text{NAV}", r"=", r"(\text{assets at marks}-\text{liabilities})/\text{shares}", font_size=40,
                      colors={r"\text{NAV}": ETF_C}),
                cmath(r"\text{secondary}", r":", r"\text{investors trade shares on an exchange}", font_size=34)]
        whys = [why(r"authorised participants, usually large dealers, deliver the basket to the fund and receive new "
                    r"shares in large blocks, called creation units"),
                why(r"or the reverse: return shares, receive the securities; in kind, so the fund need not sell"),
                why(r"the net asset value per share, published daily from the holdings' prices"),
                why(r"much share trading happens here, between investors and market makers, never touching the fund")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Creation and redemption mechanics. <bookmark mark='a'/> In an in-kind structure, an authorized participant delivers a specified basket for creation-unit shares. <bookmark mark='b'/> Redemption reverses that exchange, subject to the fund's terms; cash structures differ. <bookmark mark='c'/> NAV per share is marked assets minus liabilities, divided by shares outstanding. It is not necessarily an executable basket price. <bookmark mark='d'/> Secondary-market share trades between investors and market makers do not each trigger a primary transaction with the fund."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def band(self):
        rows = [cmath(r"P > \text{NAV} + c_{\text{create}}", r"\Rightarrow", r"\text{buy basket, create, sell shares}",
                      font_size=32),
                cmath(r"P < \text{NAV} - c_{\text{redeem}}", r"\Rightarrow", r"\text{buy shares, redeem, sell basket}",
                      font_size=32),
                cmath(r"|P - \text{NAV}|", r"\lesssim", r"c", font_size=40, colors={r"c": HURDLE})]
        whys = [why(r"a premium over executable basket value net of all creation costs can support arbitrage, under matched execution and settlement assumptions"),
                why(r"a discount to executable redemption proceeds can support the reverse trade; stale published NAV need not be realizable"),
                why(r"a shorthand band requires executable basket value, matched settlement and financing; published NAV may be stale; costs include "
                    r"fees and the participants' balance sheets: narrow for large stocks, wide for bonds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A conditional arbitrage band. <bookmark mark='a'/> If the ETF sale proceeds exceed the executable basket purchase cost plus creation, financing and settlement costs, a participant can create and sell. <bookmark mark='b'/> Reverse the transactions for redemption at a discount. <bookmark mark='c'/> The displayed NAV inequalities are a shorthand only when NAV approximates the executable basket. Stale marks, hedging error, trading restrictions and capital constraints prevent a hard bound around published NAV."
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

    def worked(self):
        p, nav, c = 80.0, 84.0, 0.02
        gain = nav * (1 - c) - p
        rows = [cmath(r"\text{buy shares}", r":", r"\$80.00", font_size=38),
                cmath(r"\text{redeem, sell bonds}", r":", rf"\$84.00 \times (1 - 0.02) = \${nav * (1 - c):.2f}", font_size=36),
                cmath(r"\text{profit}", r"=", rf"\${gain:.2f}\ \text{{a share}}", font_size=40, colors={r"\text{profit}": GOOD}),
                cmath(r"\text{if gross bonds fetch } 79", r"\Rightarrow", r"\text{loss }\$2.58", font_size=36, colors={r"\text{loss }\$2.58": BAD})]
        whys = [why(r"the pause's fund, at a discount of almost 5\%"),
                why(r"redeem in kind, then sell the bonds at their published value less a 2\% cost of trading them"),
                why(r"an arbitrage, on paper"),
                why(r"but if the published value is stale and the bonds really fetch \$79, the trade loses: the discount "
                    r"was the market's price for the bonds")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"A chosen executable-basket calculation. <bookmark mark='a'/> Buy a share for eighty dollars. <bookmark mark='b'/> Assume the delivered basket really sells for eighty-four gross, with a two-percent selling cost applied to that gross amount. <bookmark mark='c'/> Net proceeds are eighty-two dollars thirty-two, a profit of {gain:.2f} before other costs. <bookmark mark='d'/> If executable gross is only seventy-nine despite the published mark, the same cost leaves seventy-seven dollars forty-two, a loss of two dollars fifty-eight. The example illustrates why a marked NAV need not be an executable arbitrage."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def who(self):
        cards = VGroup(
            desk_question(r"two layers of makers", r"exchange market makers quote the shares all day and hedge with "
                          r"futures, the basket or related ETFs; participants submit primary transactions subject to fund terms, cutoffs and settlement", width=12.4,
                          font_size=19),
            desk_question(r"what the maker prices", r"a fair value for the basket in real time, often far more current "
                          r"than the published value, and the cost of the trip through creation or redemption",
                          width=12.4, font_size=19),
            desk_question(r"no obligation", r"participants may create and redeem; they are not required to, and in stress "
                          r"their balance sheets are what is scarce (Pan and Zeng)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Two connected roles. <bookmark mark='a'/> Exchange market makers quote ETF shares and may hedge with futures, baskets or related funds. Authorized participants submit primary-market creation or redemption transactions under fund terms, cutoffs and settlement procedures; execution is not simply one universal end-of-day event. <bookmark mark='b'/> A dealer estimates executable fair value and the cost of that route. <bookmark mark='c'/> Authorization usually does not oblige it to arbitrage every discount; capital constraints and basket risks can make a visible gap persist."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def in_kind(self):
        cards = VGroup(
            desk_question(r"in kind and taxes", r"in the US, redeeming in kind lets a fund hand low-cost-basis securities "
                          r"to participants instead of selling them, so fewer capital gains reach shareholders", width=12.4,
                          font_size=19),
            desk_question(r"custom baskets", r"since the SEC's 2019 ETF rule, funds may accept baskets that differ from "
                          r"their holdings, which helps bond funds whose exact bonds are hard to find", width=12.4,
                          font_size=19),
            desk_question(r"cash creations", r"some funds create and redeem in cash, so the fund itself trades the "
                          r"securities; the first US spot Bitcoin ETFs, approved in January 2024, were set up that way",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three details that matter. <bookmark mark='a'/> Redeeming in kind lets an American fund hand over "
            "low-cost-basis securities instead of selling them, so fewer capital gains reach shareholders. "
            "<bookmark mark='b'/> Since the SEC's twenty nineteen ETF rule, funds may accept custom baskets that differ "
            "from their holdings, which helps bond funds. <bookmark mark='c'/> And some funds create in cash, so the fund "
            "itself trades the securities; the first American spot Bitcoin funds, approved in January twenty twenty-four, "
            "were set up that way."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def inav(self):
        rows = [cmath(r"\text{iNAV}", r":", r"\text{an indicative value, published every 15 seconds}", font_size=34,
                      colors={r"\text{iNAV}": ETF_C}),
                cmath(r"\text{premium}", r"=", r"P / \text{NAV} - 1", font_size=40),
                cmath(r"\text{maker's fair value}", r":", r"\text{futures, correlated funds, the basket's live quotes}",
                      font_size=30, colors={r"\text{maker's fair value}": MAKER_C})]
        whys = [why(r"many exchanges publish an intraday indicative value of the basket, from the last prices of its "
                    r"holdings"),
                why(r"the daily premium or discount, against the official end-of-day NAV"),
                why(r"makers do not quote off the published values; they build their own fair value from the most liquid "
                    r"related prices, which is why they can quote a bond fund when the bonds are not trading")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How the price is watched. <bookmark mark='a'/> Many exchanges publish an indicative value of the basket "
            "every fifteen seconds, from its holdings' last prices. <bookmark mark='b'/> The premium is the price over "
            "the official value, minus one. <bookmark mark='c'/> But makers do not quote off published values. They build "
            "their own fair value from the most liquid related prices, futures and other funds, which is why they can "
            "quote a bond fund when the bonds themselves are not trading."
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

    def march(self):
        cards = VGroup(
            desk_question(r"March 2020: a literature case", r"bond ETF prices and evaluated NAVs diverged during market stress; Aramonte and Avalos (BIS, 2020) discuss price discovery and strained arbitrage", width=12.4, font_size=19),
            desk_question(r"two distinct measurements", r"price drawdown is a change over time; discount is price relative to contemporaneous NAV. A close-only price series cannot measure the latter", width=12.4, font_size=19),
            desk_question(r"what would identify the gap", r"time-matched executable basket quotes, NAV methodology, creation terms, funding and dealer constraints; daily price movements alone do not identify a policy effect", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("March twenty twenty as a literature case. <bookmark mark='a'/> BIS researchers documented bond ETF dislocations and the difficulty of arbitraging illiquid holdings during stress. <bookmark mark='b'/> A price drawdown and a discount to NAV are different quantities. A close-only series cannot measure the discount, and price response alone cannot identify an announcement's causal effect. <bookmark mark='c'/> A careful study needs synchronized NAV and executable basket information, funding, creation terms and a credible identification design. We use the cited case to explain mechanisms without a new numerical price chart.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(("a","b","c")):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k]))
        self.wait(0.4)
        self.clear_scene()

    def discovery(self):
        rows = [cmath(r"\text{NAV}", r":", r"\text{bond prices, many not traded that day}", font_size=36,
                      colors={r"\text{NAV}": ETF_C}),
                cmath(r"P_{\text{ETF}}", r":", r"\text{a live price, traded thousands of times}", font_size=36),
                cmath(r"\text{possible channels}", r":", r"\text{stale marks and constrained intermediation}", font_size=32,
                      colors={r"\text{discount}": HURDLE})]
        whys = [why(r"most corporate bonds trade rarely; the value is built from evaluated prices that lag the market"),
                why(r"the fund's shares trade continuously, so they carry the news first"),
                why(r"Haddad, Moreira and Muir (2021) and others: part of the discount was the ETF discovering prices the "
                    r"bonds had not yet shown; part was dealers unable to absorb more bonds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Interpreting a NAV gap. <bookmark mark='a'/> Evaluated prices for less frequently traded bonds can lag executable values, although infrequent trading does not make every mark stale. <bookmark mark='b'/> Liquid ETF shares can contribute price discovery, while also reflecting their own flow and risk premia. <bookmark mark='c'/> The cited March literature discusses valuation and constrained intermediation channels. Our illustrations do not estimate their separate contributions or show that a particular discount is an error."
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

    def fed(self):
        cards = VGroup(
            desk_question(r"23 March 2020", r"the announced SMCCF term sheet allowed investment-grade corporate-bond ETFs; this was not initial eligibility for high-yield ETFs", width=12.4, font_size=19),
            desk_question(r"9 April 2020", r"the expanded term sheet included high-yield corporate-bond ETFs, with most ETF holdings still directed toward investment-grade exposure", width=12.4, font_size=19),
            desk_question(r"announcement, purchases and causality", r"a backstop can affect expectations before purchases; separating this channel from concurrent policies and market news requires evidence beyond one price path", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover("Keep the chronology precise. <bookmark mark='a'/> The March twenty-third SMCCF term sheet initially specified investment-grade corporate-bond ETFs. <bookmark mark='b'/> The April ninth expansion included high-yield bond ETFs, while retaining a predominant investment-grade allocation. <bookmark mark='c'/> Announcement effects can precede purchases, but an observed recovery alone does not show that dealer balance sheets were restored by that announcement. The official term sheets establish eligibility dates; causal policy studies require additional evidence.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(("a","b","c")):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k]))
        self.wait(0.4)
        self.clear_scene()

    def leveraged(self):
        rows = [cmath(r"\text{target}", r":", r"L \times \text{the daily return}", font_size=38),
                cmath(r"\text{rebalance}", r"=", r"L(L - 1)\,r\,A_0", font_size=40, colors={r"\text{rebalance}": HURDLE}),
                cmath(r"L = 3,\ r = -5\%", r":", r"\text{sell exposure of }30\%\,A_0", font_size=34,
                      colors={r"\text{sell exposure of }30\%\,A_0": BAD})]
        whys = [why(r"leveraged and inverse ETFs promise a multiple of each day's return, so their exposure must be reset "
                    r"every day"),
                why(r"Cheng and Madhavan (2009): the trade needed at the close is $L(L - 1)$ times the day's return times "
                    r"beginning-of-day assets, ignoring flows, financing and tracking costs; for $L>1$ or $L<0$, the trade follows the move"),
                why(r"with no flows or financing costs, a triple-leveraged fund after a 5\% fall sells 30\% of starting assets in exposure: "
                    r"predictable, procyclical flow that market makers price")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Daily leverage resets. <bookmark mark='a'/> In a frictionless single-asset calculation, begin with assets A zero and exposure L times assets, with no subscriptions, financing or tracking costs. <bookmark mark='b'/> After underlying return r, new assets are A zero times one plus L r, while existing exposure is L A zero times one plus r. Their difference gives the required trade L times L minus one times r times A zero. <bookmark mark='c'/> For triple leverage and a five-percent fall, sell thirty percent of beginning-of-day assets in exposure. That is not thirty percent of the reduced ending assets. For leverage between zero and one, the directional statement reverses."
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
            desk_question(r"the band is a cost, not a law", r"premiums and discounts are bounded by what arbitrage costs; "
                          r"in stress the cost of balance sheet dominates", width=12.4, font_size=19),
            desk_question(r"the ETF may be the better price", r"for illiquid holdings, the fund's price can lead its NAV; "
                          r"a discount can be information, not a mistake", width=12.4, font_size=19),
            desk_question(r"liquidity on top of illiquidity", r"an ETF offers intraday liquidity on assets that have "
                          r"little; it works because makers warehouse the gap, and it strains when they cannot", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> The band is a cost, not a law: in stress the cost of balance sheet "
            "dominates. <bookmark mark='b'/> For illiquid holdings, the fund's price can be the better one, and a "
            "discount can be information. <bookmark mark='c'/> And an ETF offers liquidity on top of assets that have "
            "little. It works because market makers warehouse the gap, and it strains when they cannot."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label("public news moves Bitcoin's value by 10 ticks. A maker's stale quote can be cancelled, or picked off by any of four faster-or-equal rivals. With five equally fast firms, how often is it picked off?", 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. Public news moves Bitcoin's value by ten ticks. A maker's stale quote can be cancelled, "
            "or picked off by any of four rivals as fast as it is. With five equally fast firms, how often is it picked "
            "off?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
