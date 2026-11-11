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
        rows = [cmath(r"\Delta W", r"=", r"\sum_i\varepsilon_i(p_i-M_i)+\sum_i r_i+\int I_{t-}\,dM_t", font_size=31),
                cmath(r"a_{i,h}", r"=", r"\varepsilon_i(M_{i+h}-M_i)", font_size=36, colors={r"a_{i,h}": SNIPE_C}),
                cmath(r"e_h", r"=", r"\mathbb E[\varepsilon_i(p_i-M_i)+r_i-a_{i,h}]", font_size=33, colors={r"e_h": SPREAD_C})]
        whys = [why(r"self-financing marked wealth; taker sign $\varepsilon_i$, maker inventory $I$, trade price $p_i$ and contemporaneous mid $M_i$; no other costs"),
                why(r"adverse markout in the taker direction over a specified horizon; it can be negative"),
                why(r"a separate marked edge per fill; near the touch the first term is half-spread. Do not subtract this markout again from the full inventory ledger")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover("The accounting first. <bookmark mark='a'/> Marked wealth is execution edge at each fill, plus rebates, plus gains on inventory as the mid moves. Epsilon is the taker's sign; the maker holds the opposite trade. This self-financing identity omits other costs. <bookmark mark='b'/> Separately, adverse markout is the subsequent mid move in the taker's direction at a specified horizon. <bookmark mark='c'/> Subtract that from the fill's execution edge to obtain a horizon-marked edge. This already includes that price move. Subtracting it again from the full inventory ledger would double-count it.") as vo:
            step(0)
            vo.wait_until("a")
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
        self.add(cards[0])
        with self.voiceover(
            "Three risks. <bookmark mark='a'/> Adverse selection: the taker knows something, either private information "
            "or just a faster read of public news. <bookmark mark='b'/> Inventory: every fill leaves a position whose "
            "price risk the maker carries until the other side arrives. <bookmark mark='c'/> And operations: a quoting "
            "engine that misbehaves for minutes can lose more than a year of spreads. Knight Capital, as reported, lost "
            "about four hundred and forty million dollars in under an hour in August twenty twelve."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
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
        whys = [why(r"a model-based spread decomposition (Stoll 1989; Huang and Stoll 1997), with identification assumptions about how prices "
                    r"move after trades"),
                why(r"the costs of being in business at all: exchange and clearing fees, servers, people, capital"),
                why(r"Ho and Stoll's term: paid for carrying a position whose price may move"),
                why(r"Glosten and Milgrom's term, and Budish, Cramton and Shim's: the part of each fill that is lost to the "
                    r"counterparty's knowledge or speed")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A model-based spread decomposition. <bookmark mark='a'/> Stoll, then Huang and Stoll, distinguish order processing, inventory and adverse selection under their respective identification assumptions. <bookmark mark='b'/> Processing includes fees, technology and capital. <bookmark mark='c'/> Inventory carries price risk until it is offset. <bookmark mark='d'/> Adverse selection concerns conditional losses to counterparties. A simple replay's loss does not separately identify those structural components."
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
                    r"know which; uninformed buys and sells have equal odds independent of value"),
                why(r"a buy is evidence for the high value: $P(V_H \mid \text{buy}) = (1 + \mu)/2$, so a competitive maker "
                    r"asks the value expected given a buy"),
                why(r"the whole spread is adverse selection: no fees, no inventory risk"),
                why(r"a fifth of takers informed, a range of ten: a spread of two"),
                why(r"zero profit: on average the half-spread on each fill pays the expected move to eventual value under the symmetric model")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.3, buff=0.32, edge=6.9)
        with self.voiceover(
            "Recall the symmetric Glosten and Milgrom example. <bookmark mark='a'/> Value is high or low with equal prior probabilities. A fraction mu knows value; uninformed traders buy and sell with equal odds, independently of value. <bookmark mark='b'/> Conditional on a buy, high value has probability one plus mu over two. A risk-neutral competitive dealer therefore asks the conditional expected value. <bookmark mark='c'/> Spread is mu times the value range, with no fees or inventory risk. <bookmark mark='d'/> A fifth informed and a range of ten give two. <bookmark mark='e'/> Against eventual value, the expected adverse move equals the half-spread. This theoretical balance does not identify which real Bitcoin maker breaks even."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def as_recap(self):
        rows = [cmath(r"r(q)", r"\approx", r"M - q\,\gamma\sigma^2 (T - t)", font_size=40, colors={r"r(q)": INV_C}),
                cmath(r"\delta^a + \delta^b", r"\approx", r"\gamma\sigma^2 (T - t) + \frac{2}{\gamma}\log\!\left(1 + "
                      r"\frac{\gamma}{k}\right)", font_size=32),
                cmath(r"\lambda(\delta)", r"=", r"A\,e^{-k\delta}", font_size=40, colors={r"\lambda(\delta)": SPREAD_C})]
        whys = [why(r"Avellaneda and Stoikov (2008), derived in Part 11: the reservation price falls with inventory $q$, "
                    r"by risk aversion times the variance still to be borne"),
                why(r"the total spread: a risk term, and a term from the trade-off between fill rate and margin"),
                why(r"the assumption that makes it solvable: quotes at distance $\delta$ from the mid are hit at a "
                    r"Poisson rate that decays exponentially; arrival drivers and Brownian price noise are independent, while controls adapt to the current state")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The familiar Avellaneda and Stoikov approximation. <bookmark mark='a'/> Take a driftless Brownian mid, constant-size trades and CARA utility. The reservation-price approximation falls with inventory times remaining price variance. <bookmark mark='b'/> Its approximate total spread combines risk and an arrival-rate term. <bookmark mark='c'/> The model assumes exponential conditional arrival rates with price noise independent of the arrival drivers. A tape reach fit alone does not test those assumptions, queue fills or the control problem."
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
                why(r"risk changes both the width at zero inventory and the inventory skew; other models add information and costs")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A restricted revenue calculation. <bookmark mark='a'/> Suppose an independently arriving unit fill earns delta and has rate A times exp minus k delta. Ignore adverse selection, fees and inventory. <bookmark mark='b'/> Differentiating delta times that rate gives delta equals one over k as the unique interior maximum for positive A and k. <bookmark mark='c'/> Risk aversion can widen even zero-inventory quotes as well as skew them. This baseline is not a universal optimal trading distance."
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
        whys = [why(r"Guéant, Lehalle and Fernandez-Tapia (2013): under the stated arrival model, a long horizon and an interior approximation, quote "
                    r"distances are approximately stationary; the base term tends to $1/k$ as risk aversion vanishes"),
                why(r"the ask is the mirror image: a long maker sells more cheaply and bids less"),
                why(r"the skew per unit of inventory: grows with volatility and risk aversion, falls with how often "
                    r"quotes are hit")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The GLFT closed-form approximation. <bookmark mark='a'/> With positive A, k, gamma, a Brownian reference price, unit trades and bounded inventory, a long-horizon spectral problem gives stationary quotes. Away from binding boundaries, a further Gaussian approximation gives these formulas. <bookmark mark='b'/> A long maker raises its bid distance and lowers its ask distance. <bookmark mark='c'/> Sigma is price per square root of time. Calibration to reach proxies does not validate the arrival model; the finite-inventory exact limit also differs from this interior approximation."
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
            desk_question(r"decimals and electronics", r"decimal prices and electronic books reshaped both models; "
                          r"spreads collapsed, and making markets became a contest of technology", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "How the business changed. <bookmark mark='a'/> The New York Stock Exchange historically assigned specialists with quoting obligations and privileged book information. <bookmark mark='b'/> Christie and Schultz documented avoidance of odd eighths on Nasdaq in 1994; investigations and settlements followed. <bookmark mark='c'/> Decimalization and electronic competition changed those institutions and narrowed many spreads. Specialist functions evolved rather than disappearing everywhere at once."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        self.add(cards[0])
        with self.voiceover(
            "Who does it today. <bookmark mark='a'/> In American stocks, wholesalers internalise most retail orders off "
            "exchange and pay brokers for the flow. <bookmark mark='b'/> Electronic market makers quote on exchanges in "
            "thousands of instruments at once; Virtu disclosed a single losing day in about twelve hundred, as Part "
            "thirty-four discussed. <bookmark mark='c'/> And some venues contract designated makers to quote within a "
            "maximum spread for a minimum share of the day, in return for rebates or priority."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def flow_types(self):
        cards = VGroup(
            desk_question(r"not all flow is equal", r"a maker's markout depends on who it trades with: retail orders are "
                          r"often less adversely selected on average; labels alone do not identify informed orders",
                          width=12.4, font_size=19),
            desk_question(r"segmentation", r"wholesalers pay brokers for retail orders precisely because their markouts "
                          r"are often more favorable; effects on lit spreads depend on routing and competition", width=12.4,
                          font_size=19),
            desk_question(r"measuring it", r"markouts by counterparty type, order size and time of day are the maker's "
                          r"most guarded statistics, and the basis of every pricing decision", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Order flow differs. <bookmark mark='a'/> Retail flow often has lower average adverse markout than professional arbitrage flow, but neither label proves that an individual order is informed. <bookmark mark='b'/> Segmentation can change the flow remaining on exchanges; its effect on lit spreads depends on competition and routing, rather than following mechanically from payment for order flow. <bookmark mark='c'/> Makers measure markouts by size, time and available counterparty classifications to estimate those differences."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        self.add(cards[0])
        with self.voiceover(
            "Real makers run many books at once. <bookmark mark='a'/> A maker in a thousand stocks hedges the common "
            "factor with index futures and keeps the stock-specific inventory small: Part thirty-one's risk model, at "
            "high frequency. <bookmark mark='b'/> An options maker quotes a whole volatility surface and hedges its "
            "Greeks, as in Part eleven. <bookmark mark='c'/> And in crypto the same Bitcoin trades on many venues, as "
            "spot and perpetual: makers quote on several and hedge on the cheapest."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label("a maker joins the best bid and offer of Bitcoin's perpetual and rejoins whenever the price moves. After the half tick of spread, what is its average profit per fill a minute later?", 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            'Pause and predict. In the specified coarse-grid maker replay, orders join behind displayed quantity, with assumed pro-rata cancellations and through-price fills. After execution price is marked to the mid one minute later, would a half-tick quoted spread alone imply positive mean profit? Predict the sign before viewing the measured conditional mark.'
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
