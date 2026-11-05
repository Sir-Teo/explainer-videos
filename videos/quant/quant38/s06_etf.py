from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (MAKER_C, BAD, ETF_C, GOOD, HURDLE, PART, load)


class ETF(VoiceoverScene):
    def construct(self):
        e = load("etf")
        self.card()
        self.mechanics()
        self.band()
        self.worked()
        self.who()
        self.in_kind()
        self.inav()
        self.march(e)
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
                cmath(r"\text{NAV}", r"=", r"\textstyle\sum_i w_i\,p_i - \text{costs}", font_size=40,
                      colors={r"\text{NAV}": ETF_C}),
                cmath(r"\text{secondary}", r":", r"\text{investors trade shares on an exchange}", font_size=34)]
        whys = [why(r"authorised participants, usually large dealers, deliver the basket to the fund and receive new "
                    r"shares in large blocks, called creation units"),
                why(r"or the reverse: return shares, receive the securities; in kind, so the fund need not sell"),
                why(r"the net asset value per share, published daily from the holdings' prices"),
                why(r"almost all trading happens here, between investors and market makers, never touching the fund")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How an ETF works. <bookmark mark='a'/> Authorised participants, usually large dealers, deliver a basket of "
            "securities to the fund and receive new shares in large blocks. <bookmark mark='b'/> Or the reverse: they "
            "return shares and receive the securities, in kind, so the fund never has to sell. "
            "<bookmark mark='c'/> The net asset value is computed each day from the holdings' prices. "
            "<bookmark mark='d'/> And almost all trading happens on the exchange, between investors and market makers, "
            "without touching the fund at all."
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
        whys = [why(r"a premium larger than the cost of creating is an arbitrage: new shares appear and the premium closes"),
                why(r"a discount larger than the cost of redeeming closes the same way, shares disappearing"),
                why(r"so the price stays within a band around the value, set by trading costs in the underlying securities, "
                    r"fees and the participants' balance sheets: narrow for large stocks, wide for bonds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The arbitrage band. <bookmark mark='a'/> If the price rises above the value by more than the cost of "
            "creating, a participant buys the basket, creates shares and sells them. <bookmark mark='b'/> If it falls "
            "below by more than the cost of redeeming, it buys shares, redeems them and sells the basket. "
            "<bookmark mark='c'/> So the price stays in a band around the value, as wide as the cost of trading the "
            "underlying securities and using the dealer's balance sheet: narrow for large stocks, wide for bonds."
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
                cmath(r"\text{if bonds fetch } 79", r"\Rightarrow", r"\text{a loss}", font_size=36, colors={r"\text{a loss}": BAD})]
        whys = [why(r"the pause's fund, at a discount of almost 5\%"),
                why(r"redeem in kind, then sell the bonds at their published value less a 2\% cost of trading them"),
                why(r"an arbitrage, on paper"),
                why(r"but if the published value is stale and the bonds really fetch \$79, the trade loses: the discount "
                    r"was the market's price for the bonds")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The pause's arbitrage, worked through. <bookmark mark='a'/> Buy the shares at eighty dollars. "
            "<bookmark mark='b'/> Redeem them for bonds, and sell the bonds at their published value less a two percent "
            f"cost. <bookmark mark='c'/> A profit of {gain:.2f} dollars a share, on paper. <bookmark mark='d'/> But if the "
            "published value is stale and the bonds really fetch seventy-nine, the trade loses. The discount was the "
            "market's price for the bonds."
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
                          r"futures, the basket or related ETFs; participants create and redeem at the end", width=12.4,
                          font_size=19),
            desk_question(r"what the maker prices", r"a fair value for the basket in real time, often far more current "
                          r"than the published value, and the cost of the trip through creation or redemption",
                          width=12.4, font_size=19),
            desk_question(r"no obligation", r"participants may create and redeem; they are not required to, and in stress "
                          r"their balance sheets are what is scarce (Pan and Zeng)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two layers of makers. <bookmark mark='a'/> Exchange market makers quote the shares all day and hedge with "
            "futures, the basket or related funds; participants create and redeem at the end of the day. "
            "<bookmark mark='b'/> What they price is a fair value of the basket in real time, often far more current "
            "than the published one. <bookmark mark='c'/> And participants are not obliged to act. Kevin Pan and Yao Zeng "
            "showed that when their balance sheets are scarce, the band widens."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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

    def march(self, e):
        h = e["HYG"]
        t = h["t"]
        c = np.asarray(h["close"], float)
        v = np.asarray(h["vol_x"], float)
        x = np.arange(len(c))
        lo, hi = float(np.floor(c.min() / 5) * 5), float(np.ceil(c.max() / 5) * 5)
        g = axes([0, len(c) - 1], [lo, hi], x_length=8.4, y_length=3.0, xlabel=r"", ylabel=r"HYG, \$",
                 xticks=[], yticks=[lo, hi], yfmt=lambda v_: f"{v_:.0f}", font_size=14).move_to(UP * 1.3)
        g2 = axes([0, len(c) - 1], [0, float(np.ceil(v.max()))], x_length=8.4, y_length=2.0, xlabel=r"January to April 2020",
                  ylabel=r"volume $\times$ 2019", xticks=[], yticks=[0, float(np.ceil(v.max()))],
                  yfmt=lambda v_: f"{v_:.0f}", font_size=14).move_to(DOWN * 1.8)
        cp = curve(g.ax, x, c, ETF_C, stroke_width=3)
        bars = VGroup(*[Rectangle(width=0.06, height=max(1e-3, abs(g2.ax.c2p(0, y)[1] - g2.ax.c2p(0, 0)[1])),
                                  fill_color=HURDLE, fill_opacity=0.8, stroke_width=0).move_to(g2.ax.c2p(i, y / 2))
                        for i, y in enumerate(v)])
        k = t.index(h["trough_date"])
        mark = DashedLine(g.ax.c2p(k, lo), g.ax.c2p(k, hi), color=GREY_B, stroke_width=1.5)
        with self.voiceover(
            "March twenty twenty, in the largest high-yield bond fund, HYG. <bookmark mark='a'/> From its January high "
            f"to the twenty-third of March the price fell {100 * abs(h['drawdown']):.0f} percent, <bookmark mark='b'/> "
            f"and daily volume reached {h['max_vol_x']:.0f} times its median of twenty nineteen. As BIS economists and "
            "others reported, the largest bond funds traded at discounts of several percent to their published values, "
            "the widest in their histories."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(cp), Create(mark), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.01))
        self.wait(0.4)
        self.clear_scene()

    def discovery(self):
        rows = [cmath(r"\text{NAV}", r":", r"\text{bond prices, many not traded that day}", font_size=36,
                      colors={r"\text{NAV}": ETF_C}),
                cmath(r"P_{\text{ETF}}", r":", r"\text{a live price, traded thousands of times}", font_size=36),
                cmath(r"\text{discount}", r"=", r"\text{partly stale NAV, partly scarce balance sheets}", font_size=32,
                      colors={r"\text{discount}": HURDLE})]
        whys = [why(r"most corporate bonds trade rarely; the value is built from evaluated prices that lag the market"),
                why(r"the fund's shares trade continuously, so they carry the news first"),
                why(r"Haddad, Moreira and Muir (2021) and others: part of the discount was the ETF discovering prices the "
                    r"bonds had not yet shown; part was dealers unable to absorb more bonds")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Was the fund wrong, or the value? <bookmark mark='a'/> Most corporate bonds trade rarely, so the published "
            "value is built from evaluated prices that lag the market. <bookmark mark='b'/> The fund's shares trade "
            "continuously, and carry the news first. <bookmark mark='c'/> So part of the discount was the fund "
            "discovering prices the bonds had not yet shown, and part was dealers whose balance sheets could take no "
            "more bonds: the arbitrage that closes the band needs someone to buy the basket."
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
            desk_question(r"23 March 2020", r"the Federal Reserve announced it would buy corporate bonds, and corporate "
                          r"bond ETFs, through a new facility; HYG's low of the episode was that day", width=12.4,
                          font_size=19),
            desk_question(r"the announcement did the work", r"discounts closed and prices rose well before the facility "
                          r"bought much: the backstop restored dealers' willingness to hold inventory", width=12.4,
                          font_size=19),
            desk_question(r"a market maker of last resort", r"a central bank buying ETFs is, in effect, a balance sheet "
                          r"for the arbitrage when private ones are full (Part 41)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The turn. <bookmark mark='a'/> On the twenty-third of March the Federal Reserve announced it would buy "
            "corporate bonds, including corporate-bond ETFs, through a new facility; that was the fund's low. "
            "<bookmark mark='b'/> Discounts closed and prices rose well before the facility bought much: the "
            "announcement restored dealers' willingness to hold inventory. <bookmark mark='c'/> A central bank buying "
            "ETFs is, in effect, a balance sheet for the arbitrage when the private ones are full, a theme Part "
            "forty-one returns to."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def leveraged(self):
        rows = [cmath(r"\text{target}", r":", r"L \times \text{the daily return}", font_size=38),
                cmath(r"\text{rebalance}", r"=", r"L(L - 1)\,r\,\text{AUM}", font_size=40, colors={r"\text{rebalance}": HURDLE}),
                cmath(r"L = 3,\ r = -5\%", r":", r"\text{sell } 30\%\ \text{of AUM at the close}", font_size=34,
                      colors={r"\text{sell } 30\%\ \text{of AUM at the close}": BAD})]
        whys = [why(r"leveraged and inverse ETFs promise a multiple of each day's return, so their exposure must be reset "
                    r"every day"),
                why(r"Cheng and Madhavan (2009): the trade needed at the close is $L(L - 1)$ times the day's return times "
                    r"assets, in the direction of the move, for both leveraged and inverse funds"),
                why(r"a triple-leveraged fund after a 5\% fall must sell 30\% of its assets' worth of exposure: "
                    r"predictable, procyclical flow that market makers price")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A special case: leveraged and inverse funds. <bookmark mark='a'/> They promise a multiple of each day's "
            "return, so their exposure must be reset every day. <bookmark mark='b'/> Minder Cheng and Ananth Madhavan "
            "showed the trade at the close is L times L minus one, times the day's return, times assets, always in the "
            "direction of the move. <bookmark mark='c'/> A triple-leveraged fund after a five percent fall must sell "
            "thirty percent of its assets' worth of exposure: predictable, procyclical flow that market makers see "
            "coming."
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
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> The band is a cost, not a law: in stress the cost of balance sheet "
            "dominates. <bookmark mark='b'/> For illiquid holdings, the fund's price can be the better one, and a "
            "discount can be information. <bookmark mark='c'/> And an ETF offers liquidity on top of assets that have "
            "little. It works because market makers warehouse the gap, and it strains when they cannot."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"public news moves Bitcoin's value by 10 ticks. A maker's stale quote can be cancelled, or picked "
                       r"off by any of four faster-or-equal rivals. With five equally fast firms, how often is it picked "
                       r"off?")
        with self.voiceover(
            "Pause and predict. Public news moves Bitcoin's value by ten ticks. A maker's stale quote can be cancelled, "
            "or picked off by any of four rivals as fast as it is. With five equally fast firms, how often is it picked "
            "off?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
