from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (INV_C, PART, SNIPE_C, SPREAD_C)


class Business(VoiceoverScene):
    def construct(self):
        self.card()
        self.pnl()
        self.three_risks()
        self.components()
        self.gm_recall()
        self.as_recap()
        self.tradeoff()
        self.as_numbers()
        self.glft_formula()
        self.history_dealers()
        self.who()
        self.flow_types()
        self.books()
        self.question()

    def card(self):
        c = chapter_card(1, r"The maker's business", r"Where does a market maker's profit come from, and where does it "
                         r"go?", part=PART)
        with self.voiceover("Chapter one. A market maker posts prices at which it will buy and sell, and lets others "
                            "choose. Its profit is what remains after everyone who chose to trade with it has been paid "
                            "for knowing more, or for being faster."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pnl(self):
        rows = [cmath(r"\Pi", r"=", r"\underbrace{\textstyle\sum \tfrac{s}{2}}_{\text{spread}} + "
                      r"\underbrace{\textstyle\sum r}_{\text{rebates}} - \underbrace{\textstyle\sum \text{markout}}_{\text{adverse "
                      r"selection}} + \underbrace{\textstyle\int I\,dM}_{\text{inventory}}", font_size=30),
                cmath(r"\text{markout}_h", r"=", r"\varepsilon\,(M_{\text{fill}+h} - M_{\text{fill}})", font_size=36,
                      colors={r"\text{markout}_h": SNIPE_C}),
                cmath(r"\text{edge}", r"=", r"\tfrac{s}{2} + r - \mathbb E[\text{markout}]", font_size=38,
                      colors={r"\text{edge}": SPREAD_C})]
        whys = [why(r"half the spread on every fill, the venue's rebate for resting, minus the move against the maker after "
                    r"each fill, plus whatever the inventory gains or loses as the mid moves"),
                why(r"the adverse move after a fill, in the direction of the taker's trade (Part 36)"),
                why(r"the edge per fill: positive only if the taker's information is worth less than the spread and "
                    r"rebate")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The profit and loss. <bookmark mark='a'/> Half the spread on every fill, plus the venue's rebate for "
            "resting liquidity, minus the adverse selection, plus what the inventory gains or loses as the price moves. "
            "<bookmark mark='b'/> Adverse selection is measured by the markout: how far the mid moves in the taker's "
            "direction after the fill. <bookmark mark='c'/> So the edge per fill is the half-spread and rebate, less the "
            "expected markout. It is positive only if what the takers know is worth less than what they pay."
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

    def three_risks(self):
        cards = VGroup(
            desk_question(r"adverse selection", r"the taker knows something: Glosten and Milgrom's informed traders, or "
                          r"just a faster read of public news (the snipers of Chapter 6)", width=12.4, font_size=19),
            desk_question(r"inventory", r"every fill leaves a position; the maker carries its price risk until the "
                          r"other side arrives or it hedges, which Ho and Stoll priced into a skew", width=12.4,
                          font_size=19),
            desk_question(r"operations", r"a quoting engine that misbehaves for minutes can lose more than a year of "
                          r"spread: Knight Capital lost about \$440 million in under an hour in August 2012, as reported",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three risks. <bookmark mark='a'/> Adverse selection: the taker knows something, either private information "
            "or just a faster read of public news. <bookmark mark='b'/> Inventory: every fill leaves a position whose "
            "price risk the maker carries until the other side arrives. <bookmark mark='c'/> And operations: a quoting "
            "engine that misbehaves for minutes can lose more than a year of spreads. Knight Capital, as reported, lost "
            "about four hundred and forty million dollars in under an hour in August twenty twelve."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def components(self):
        rows = [cmath(r"s", r"=", r"\text{order processing} + \text{inventory} + \text{adverse selection}", font_size=34),
                cmath(r"\text{order processing}", r":", r"\text{fees, technology, capital}", font_size=34),
                cmath(r"\text{inventory}", r":", r"\text{the risk of holding until the other side comes}", font_size=32,
                      colors={r"\text{inventory}": INV_C}),
                cmath(r"\text{adverse selection}", r":", r"\text{what informed or faster takers win}", font_size=32,
                      colors={r"\text{adverse selection}": SNIPE_C})]
        whys = [why(r"the classic decomposition of a spread (Stoll 1989; Huang and Stoll 1997), estimated from how prices "
                    r"move after trades"),
                why(r"the costs of being in business at all: exchange and clearing fees, servers, people, capital"),
                why(r"Ho and Stoll's term: paid for carrying a position whose price may move"),
                why(r"Glosten and Milgrom's term, and Budish, Cramton and Shim's: the part of each fill that is lost to the "
                    r"counterparty's knowledge or speed")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What a spread pays for. <bookmark mark='a'/> The classic decomposition, by Hans Stoll and later Roger Huang "
            "and Stoll, has three parts. <bookmark mark='b'/> Order processing: fees, technology, capital. "
            "<bookmark mark='c'/> Inventory: the risk of holding a position until the other side arrives. "
            "<bookmark mark='d'/> And adverse selection: what informed or faster counterparties win. On Bitcoin's "
            "perpetual the third part is so large that the spread cannot cover it, as the next chapter shows."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def gm_recall(self):
        rows = [cmath(r"V", r"\in", r"\{V_L,\ V_H\},\ \text{each with probability } \tfrac12", font_size=34),
                cmath(r"\text{ask}", r"=", r"\mathbb E[V \mid \text{buy}] = \bar V + \mu\,\tfrac{V_H - V_L}{2}", font_size=34,
                      colors={r"\text{ask}": SPREAD_C}),
                cmath(r"s", r"=", r"\mu\,(V_H - V_L)", font_size=40, colors={r"s": SPREAD_C}),
                cmath(r"\mu = 0.2,\ V_H - V_L = 10", r"\Rightarrow", r"s = 2", font_size=34),
                cmath(r"\tfrac s2", r"=", r"\mathbb E[\text{markout}]", font_size=40, colors={r"\mathbb E[\text{markout}]": SNIPE_C})]
        whys = [why(r"Glosten and Milgrom (1985), met in Part 35: the value is high or low, and a fraction $\mu$ of takers "
                    r"know which"),
                why(r"a buy is evidence for the high value: $P(V_H \mid \text{buy}) = (1 + \mu)/2$, so a competitive maker "
                    r"asks the value expected given a buy"),
                why(r"the whole spread is adverse selection: no fees, no inventory risk"),
                why(r"a fifth of takers informed, a range of ten: a spread of two"),
                why(r"zero profit: on average the half-spread on each fill exactly pays the move that follows it")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Where adverse selection comes from, recalled from Part thirty-five. <bookmark mark='a'/> In Glosten and "
            "Milgrom's model the value is high or low with equal odds, and a fraction mu of takers know which. "
            "<bookmark mark='b'/> A buy is then evidence for the high value, so a competitive maker sets its ask at the "
            "value expected given a buy: the average, plus mu times half the range. <bookmark mark='c'/> The spread is "
            "mu times the range, all of it adverse selection. <bookmark mark='d'/> With a fifth of takers informed and a "
            "range of ten, a spread of two. <bookmark mark='e'/> And the maker earns nothing on average: the half-spread "
            "on each fill exactly pays the markout that follows. On Bitcoin's perpetual that balance is struck for the "
            "fastest makers at the front of the queue, not for a slow one at the back, which is why the next chapter's "
            "replay loses."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def as_recap(self):
        rows = [cmath(r"r(q)", r"=", r"M - q\,\gamma\sigma^2 (T - t)", font_size=40, colors={r"r(q)": INV_C}),
                cmath(r"\delta^a + \delta^b", r"=", r"\gamma\sigma^2 (T - t) + \frac{2}{\gamma}\log\!\left(1 + "
                      r"\frac{\gamma}{k}\right)", font_size=32),
                cmath(r"\lambda(\delta)", r"=", r"A\,e^{-k\delta}", font_size=40, colors={r"\lambda(\delta)": SPREAD_C})]
        whys = [why(r"Avellaneda and Stoikov (2008), derived in Part 11: the reservation price falls with inventory $q$, "
                    r"by risk aversion times the variance still to be borne"),
                why(r"the total spread: a risk term, and a term from the trade-off between fill rate and margin"),
                why(r"the assumption that makes it solvable: quotes at distance $\delta$ from the mid are hit at a "
                    r"Poisson rate that decays exponentially, independent of where the price goes next")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Part eleven derived the classic model. <bookmark mark='a'/> In Avellaneda and Stoikov's market maker, the "
            "reservation price falls with inventory, by risk aversion times the variance still to be borne. "
            "<bookmark mark='b'/> The total spread has a risk term and a term from the trade-off between how often "
            "quotes fill and how much each fill earns. <bookmark mark='c'/> And it rests on one assumption: a quote at "
            "distance delta is hit at a Poisson rate A e to the minus k delta, independent of where the price goes next. "
            "Chapter three tests that assumption on the tape."
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

    def tradeoff(self):
        rows = [cmath(r"\text{quote at } \delta", r":", r"\text{earn } \delta \text{ per fill, at rate } A e^{-k\delta}",
                      font_size=34),
                cmath(r"\max_\delta", r"\ ", r"\delta\,A e^{-k\delta} \Rightarrow \delta^* = 1/k", font_size=38,
                      colors={r"\delta\,A e^{-k\delta} \Rightarrow \delta^* = 1/k": SPREAD_C}),
                cmath(r"\text{risk aversion}", r"\Rightarrow", r"\text{adjust for inventory around } 1/k", font_size=34)]
        whys = [why(r"a wider quote earns more per fill and fills less often"),
                why(r"a risk-neutral maker with no inventory concerns maximises expected revenue per unit time: the first-"
                    r"order condition gives one over $k$"),
                why(r"everything else in the formulas is about inventory: how far to lean the quotes to get rid of it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The core trade-off in one line. <bookmark mark='a'/> A quote at distance delta earns delta per fill, and "
            "fills at a rate that falls with delta. <bookmark mark='b'/> Maximise revenue per unit time and the answer is "
            "delta equals one over k: the base term of every formula. <bookmark mark='c'/> Everything else is about "
            "inventory: how far to lean the quotes to get rid of what has been bought."
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

    def as_numbers(self):
        import math
        g, var, k, q = 0.1, 4.0, 1.5, 2
        total = g * var + (2 / g) * math.log(1 + g / k)
        shift = q * g * var
        rows = [cmath(r"\gamma = 0.1,\ \sigma^2(T - t) = 4,\ k = 1.5", r"\ ", r"", font_size=34),
                cmath(r"\delta^a + \delta^b", r"=", rf"0.4 + 20\log(1.0667) = {total:.2f}", font_size=36,
                      colors={r"\delta^a + \delta^b": SPREAD_C}),
                cmath(r"r(2)", r"=", rf"M - 2 \times 0.1 \times 4 = M - {shift:.1f}", font_size=38, colors={r"r(2)": INV_C})]
        whys = [why(r"an illustrative maker: risk aversion, the variance still to bear, and the fill decay"),
                why(r"the total spread is mostly the fill-rate term, almost $2/k$; risk adds only 0.4"),
                why(r"holding two units, the maker centres its quotes 0.8 below the mid, to sell more and buy less")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "In numbers. <bookmark mark='a'/> An illustrative maker: risk aversion a tenth, variance still to bear of four, "
            "and a fill decay of one and a half. <bookmark mark='b'/> The total spread is "
            f"{total:.2f}, mostly the fill-rate term, close to two over k; the risk term adds only 0.4. "
            "<bookmark mark='c'/> Holding two units, it centres its quotes 0.8 below the mid, to sell more and buy less."
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

    def glft_formula(self):
        rows = [cmath(r"\delta^{b}(q)", r"\approx", r"\frac1\gamma\log\!\left(1 + \frac\gamma k\right) + \frac{2q + 1}{2}\,c",
                      font_size=34),
                cmath(r"\delta^{a}(q)", r"\approx", r"\frac1\gamma\log\!\left(1 + \frac\gamma k\right) - \frac{2q - 1}{2}\,c",
                      font_size=34),
                cmath(r"c", r"=", r"\sqrt{\frac{\sigma^2\gamma}{2Ak}\left(1 + \frac\gamma k\right)^{1 + k/\gamma}}",
                      font_size=36, colors={r"c": INV_C})]
        whys = [why(r"Guéant, Lehalle and Fernandez-Tapia (2013): over a long horizon with inventory limits, the optimal "
                    r"distances become stationary; for small risk aversion, the first term tends to $1/k$"),
                why(r"the ask is the mirror image: a long maker sells more cheaply and bids less"),
                why(r"the skew per unit of inventory: grows with volatility and risk aversion, falls with how often "
                    r"quotes are hit")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And its practical form. <bookmark mark='a'/> Guéant, Lehalle and Fernandez-Tapia showed that over a long "
            "horizon with inventory limits, the optimal distances become stationary: a base distance, close to one over "
            "k when risk aversion is small, plus a skew proportional to inventory. <bookmark mark='b'/> The ask mirrors "
            "the bid: a long maker sells more cheaply and bids less. <bookmark mark='c'/> And the skew per unit grows "
            "with volatility and risk aversion and falls with the fill rate. Everything in it can be estimated from a "
            "tape."
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

    def history_dealers(self):
        cards = VGroup(
            desk_question(r"specialists", r"the NYSE once gave each stock one specialist, with privileged information "
                          r"about the book and an obligation to keep the market fair and orderly", width=12.4, font_size=19),
            desk_question(r"odd eighths", r"Christie and Schultz (1994) found Nasdaq dealers almost never quoted odd "
                          r"eighths of a dollar, keeping spreads at a quarter; investigations and a settlement followed",
                          width=12.4, font_size=19),
            desk_question(r"decimals and electronics", r"decimal prices in 2001 and electronic books ended both models; "
                          r"spreads collapsed, and making markets became a contest of technology", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How we got here. <bookmark mark='a'/> The New York Stock Exchange once gave each stock a single specialist, "
            "with privileged sight of the book and an obligation to keep the market orderly. <bookmark mark='b'/> On "
            "Nasdaq, William Christie and Paul Schultz found in 1994 that dealers almost never quoted odd eighths of a "
            "dollar, which kept spreads at a quarter; investigations and a large settlement followed. "
            "<bookmark mark='c'/> Decimal prices in two thousand and one and electronic books ended both models: spreads "
            "collapsed, and making markets became a contest of technology."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def who(self):
        cards = VGroup(
            desk_question(r"wholesalers", r"in US equities, a few firms internalise most retail orders off exchange, "
                          r"paying brokers for the flow (Part 35)", width=12.4, font_size=19),
            desk_question(r"electronic market makers", r"proprietary firms quoting on exchanges in thousands of "
                          r"instruments at once; Virtu disclosed one losing day in about 1,200 (Part 34)", width=12.4,
                          font_size=19),
            desk_question(r"designated makers and specialists", r"some venues contract makers to quote within a maximum "
                          r"spread for a minimum share of the day, in exchange for rebates or priority", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who does it today. <bookmark mark='a'/> In American stocks, wholesalers internalise most retail orders off "
            "exchange and pay brokers for the flow. <bookmark mark='b'/> Electronic market makers quote on exchanges in "
            "thousands of instruments at once; Virtu disclosed a single losing day in about twelve hundred, as Part "
            "thirty-four discussed. <bookmark mark='c'/> And some venues contract designated makers to quote within a "
            "maximum spread for a minimum share of the day, in return for rebates or priority."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def flow_types(self):
        cards = VGroup(
            desk_question(r"not all flow is equal", r"a maker's markout depends on who it trades with: retail orders are "
                          r"small and rarely informed; a fast arbitrageur's orders are informed by construction",
                          width=12.4, font_size=19),
            desk_question(r"segmentation", r"wholesalers pay brokers for retail orders precisely because their markouts "
                          r"are good; exchanges get the rest, which is why lit spreads must be wider", width=12.4,
                          font_size=19),
            desk_question(r"measuring it", r"markouts by counterparty type, order size and time of day are the maker's "
                          r"most guarded statistics, and the basis of every pricing decision", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Not all flow is equal. <bookmark mark='a'/> A maker's markout depends on who it trades with: retail orders "
            "are small and rarely informed, while a fast arbitrageur's orders are informed by construction. "
            "<bookmark mark='b'/> That is why wholesalers pay brokers for retail orders, and why the flow left on "
            "exchanges forces wider lit spreads. <bookmark mark='c'/> Markouts by counterparty, size and time of day are "
            "a maker's most guarded statistics."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def books(self):
        cards = VGroup(
            desk_question(r"many books, one risk", r"a maker in a thousand stocks hedges the common factor with index "
                          r"futures and keeps the idiosyncratic inventory small: Part 31's risk model, at high frequency",
                          width=12.4, font_size=19),
            desk_question(r"options", r"an options maker quotes a whole volatility surface and hedges delta, then vega "
                          r"(Part 11); the quote is the surface, the inventory is the Greeks", width=12.4, font_size=19),
            desk_question(r"across venues", r"the same Bitcoin trades on many exchanges and as spot and perpetual; makers "
                          r"quote on several and hedge on the cheapest", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Real makers run many books at once. <bookmark mark='a'/> A maker in a thousand stocks hedges the common "
            "factor with index futures and keeps the stock-specific inventory small: Part thirty-one's risk model, at "
            "high frequency. <bookmark mark='b'/> An options maker quotes a whole volatility surface and hedges its "
            "Greeks, as in Part eleven. <bookmark mark='c'/> And in crypto the same Bitcoin trades on many venues, as "
            "spot and perpetual: makers quote on several and hedge on the cheapest."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a maker joins the best bid and offer of Bitcoin's perpetual and rejoins whenever the price moves. "
                       r"After the half tick of spread, what is its average profit per fill a minute later?")
        with self.voiceover(
            "Pause and predict. A maker joins the best bid and offer of Bitcoin's perpetual, and rejoins whenever the "
            "price moves. After its half tick of spread, what is its average profit per fill, a minute later?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
