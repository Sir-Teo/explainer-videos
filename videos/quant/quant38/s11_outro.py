from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, ETF_C, FAST_C, GOOD, HURDLE, MAKER_C, PART, SNIPE_C, SPREAD_C, load)

DESK = [
    (r"Where does a market maker's profit come from?",
     r"half-spread plus rebate minus the markout after fills, plus or minus inventory; on Bitcoin at the touch, the markout "
     r"is forty times the half-spread"),
    (r"Why does a maker skew its quotes with inventory?",
     r"to make the next fills reduce it: GLFT's skew per unit is $\sqrt{\sigma^2\gamma(1 + \gamma/k)^{1 + k/\gamma}/(2Ak)}$"),
    (r"What does fill-rate data say about where to quote?",
     r"intensities that decay slowly with distance put the optimal quotes far out; on Bitcoin about 30 ticks"),
    (r"Why does a pinned spread create a speed race?",
     r"makers cannot undercut on price, so they compete for queue position, and position goes to the fastest"),
    (r"What keeps an ETF near its NAV, and when does it fail?",
     r"creation and redemption arbitrage, bounded by trading costs and balance sheet; it failed in March 2020 for bond "
     r"funds whose NAVs were stale and whose dealers were full"),
    (r"Why doesn't competition in speed narrow the spread?",
     r"the sniping half-spread $\lambda_J J/(\lambda_I + \lambda_J)$ does not depend on the number of firms; batch "
     r"auctions remove the prize"),
]

PROBLEMS = [
    r"A maker earns 0.5 tick a fill, a rebate of 0.2 tick, and its markout after a minute is $-0.9$ tick. Its edge.",
    r"Avellaneda--Stoikov: $\gamma = 0.1$, $\sigma^2 (T - t) = 4$, $k = 1.5$. The total spread and the reservation shift at $q = 2$.",
    r"Fill probability 0.3 per second at 1 tick and 0.05 at 45 ticks: $k$, under the exponential model.",
    r"A slow maker loses 20 ticks a fill on 40{,}000 fills; a fast one 9 on 20{,}000. The value of speed per day.",
    r"Tick 1 cent, natural spread 0.3 cent. Who earns the 0.7 cent, and how is it allocated?",
    r"An ETF at \$80 with a NAV of \$84; redemption costs 2\%. Arbitrage profit, and why it may not happen.",
    r"Five equally fast firms; a stale quote. The probability it is sniped; with ten firms?",
    r"$\lambda_I = 10$, $\lambda_J = 2$, $J = 3$: the sniping half-spread; jumps of 1 or 5 instead.",
    r"Batch interval 50 ms, latency 5 $\mu$s: the factor by which the sniping component shrinks.",
    r"A speed investment of $c$ per unit time gives a 1-ns edge. When is it dominant to invest, with $N = 4$?",
    r"(qual) Prove that in Budish--Cramton--Shim's model the equilibrium half-spread is unique, independent of $N$, and "
    r"equal to the root of $\lambda_I h = \lambda_J\,\mathbb E[(|J| - h)^+]$; show the sniping rents equal investors' costs.",
    r"(qual) Derive GLFT's asymptotic quotes from the HJB of the inventory-constrained maker with intensities $A e^{-k\delta}$, "
    r"and show that the half-spread tends to $1/k$ as $\gamma \to 0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("maker"), load("fills"), load("glft"), load("deep"), load("bcs"), load("etf"))
        self.lessons()
        self.formulas()
        self.connections()
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, mk, f, g, dp, b, e):
        d = mk["days"]["2023-05-17"]
        items = [
            (r"profit = half-spread + rebate $-$ markout $\pm$ inventory", MAKER_C),
            (rf"Bitcoin at the touch: {d['slow']['pnl_per_fill']:+.0f} ticks a fill slow, "
             rf"{d['fast']['pnl_per_fill']:+.0f} fast, {d['fast, filtered']['pnl_per_fill']:+.1f} filtered", SNIPE_C),
            (r"most of the loss arrives within a fill's own tenth of a second", SNIPE_C),
            (rf"fill rates $A e^{{-k\delta}}$ with $1/k \approx {1 / f['k']:.0f}$ ticks; GLFT quotes far out", SPREAD_C),
            (r"far quotes earn on the overshoot of sweeps (an upper bound)", GOOD),
            (r"a pinned spread turns price competition into a queue race", FAST_C),
        ]
        items2 = [
            (r"ETFs: creation and redemption keep the price in a cost band", ETF_C),
            (rf"March 2020: HYG {100 * e['HYG']['drawdown']:.0f}\%, discounts, stale NAVs, full dealers", BAD),
            (r"the sniping spread is independent of the number of firms", HURDLE),
            (r"speed is a prisoner's dilemma; batch auctions remove the prize", FAST_C),
            (r"HFT profits: spread and rebates minus positioning; concentrated in the fastest", MAKER_C),
            (r"Rule 38: quote only what you can measure", QC.HOUSE),
            (rf"research: the BCS equilibrium proved; Bitcoin's model spread {b['btc']['general_half']:.2f} tick", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 38 in thirteen lines")
        with self.voiceover(
            "Part thirty-eight in thirteen lines. A maker's profit is the half-spread and rebate, less the markout, plus "
            "or minus its inventory. On Bitcoin, quoting at the touch loses, slow or fast, and most of the loss arrives "
            "within a fill's own tenth of a second. Fill rates decay slowly with distance, so the optimal quotes sit far "
            "out, where the overshoot of sweeps pays. And a spread pinned at the tick turns price competition into a "
            "queue race."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 38 in thirteen lines")
        with self.voiceover(
            "ETF arbitrage keeps a fund's price within a cost band, until, as in March twenty twenty, the band is the "
            "cost of a balance sheet no one has. The sniping spread does not depend on how many firms race, so speed is "
            "a prisoner's dilemma, and batch auctions remove its prize. High-frequency profits are spread and rebates "
            "minus positioning, concentrated in the fastest. And the research chapter proved the sniping equilibrium."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the spread pays for almost nothing", r"what decides a maker's fate is the markout after its "
                          r"fills, which depends on speed, queue position and forecasts", width=12.4, font_size=19),
            desk_question(r"models fit to the right thing", r"a fill-rate model can be right about distance for the wrong "
                          r"reason; test it on markouts, not on fills", width=12.4, font_size=19),
            desk_question(r"market design sets the prize", r"tick size, matching rules and batch intervals decide whether "
                          r"firms compete on price or on speed, and who pays", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> The spread pays for almost nothing: a maker's fate is the markout after "
            "its fills, which depends on speed, queue position and forecasts. <bookmark mark='b'/> Models must be tested "
            "on the right thing: markouts, not fill rates. <bookmark mark='c'/> And market design sets the prize: tick "
            "size, matching rules and batch intervals decide whether firms compete on price or on speed, and who pays."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"\text{edge} = \tfrac s2 + r - \mathbb E[\text{markout}]", font_size=34, color=MAKER_C),
            MathTex(r"\lambda(\delta) = A e^{-k\delta},\quad \delta^* \approx 1/k", font_size=34, color=SPREAD_C),
            MathTex(r"\delta^{b,a}(q) \approx \tfrac1\gamma\log(1 + \tfrac\gamma k) \pm \tfrac{2q \pm 1}{2} c", font_size=34),
            MathTex(r"|P - \text{NAV}| \lesssim c_{\text{arbitrage}}", font_size=34, color=ETF_C),
            MathTex(r"\tfrac{s^*}{2} = \frac{\lambda_J J}{\lambda_I + \lambda_J}\quad (\text{independent of } N)", font_size=34,
                    color=HURDLE),
            MathTex(r"\tfrac{s^*_{\text{batch}}}{2} \approx \frac{\lambda_J J\,\delta/\tau}{\lambda_I + \lambda_J \delta/\tau}",
                    font_size=32, color=GOOD),
        ).arrange(DOWN, buff=0.32)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "The part on one card. The maker's edge. Fill rates and the base distance one over k. GLFT's quotes with "
            "their inventory skew. The ETF's arbitrage band. The sniping spread, independent of the number of firms. "
            "And its batch-auction version, shrunk by latency over the batch interval."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.5,
                                                run_time=8))
        self.wait(0.6)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 35's dealer models become a business with costs; Part 36's markouts and "
                          r"queue value become its P\&L; Part 37's executor is its customer", width=12.4, font_size=19),
            desk_question(r"sideways", r"Part 11's options maker and Part 12's surface are the same business in "
                          r"another product", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 39's automated market makers quote by formula; Part 41's crises are when "
                          r"makers step back; Part 42's learning agents take the maker's chair", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: Part thirty-five's dealer models become a business "
            "with costs; Part thirty-six's markouts become its profit and loss; Part thirty-seven's executor is its "
            "customer. <bookmark mark='b'/> Sideways: Part eleven's options maker is the same business in another "
            "product. <bookmark mark='c'/> Forwards: Part thirty-nine's automated makers quote by formula, Part "
            "forty-one's crises are when makers step back, and Part forty-two's learning agents take the maker's chair."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Where does a market maker's profit come from? The spread and rebate, less the markout. "
            "<bookmark mark='a'/> Why skew quotes with inventory? To make the next fills reduce it. "
            "<bookmark mark='b'/> Where should Bitcoin's quotes sit? About thirty ticks out."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "Why does a pinned spread create a speed race? Makers can only compete for position. "
            "<bookmark mark='a'/> What keeps an ETF near its value, and when does it fail? Arbitrage, until balance "
            "sheets are full. <bookmark mark='b'/> And why doesn't competition in speed narrow the spread? Because the "
            "sniping spread does not depend on the number of firms. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        h1 = 2 * 3 / (10 + 2)
        cards = VGroup(
            desk_question(r"Research: $\lambda_I = 10$, $\lambda_J = 2$, $J = 3$", rf"$h^* = 2 \times 3/(10 + 2) = "
                          rf"{h1:.1f}$ tick", width=12.4, font_size=20),
            desk_question(r"jumps of 1 or 5", r"$10h = 2 \times \frac12[(1 - h) + (5 - h)]$ for $h < 1$, so $h = 0.5$: the "
                          r"same, because both sizes exceed the half-spread; dispersion matters only when some jumps are "
                          r"smaller than it", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The research chapter's pause, answered. <bookmark mark='a'/> Two times three over twelve: half a tick. "
            "<bookmark mark='b'/> With jumps of one or five, the answer is the same, half a tick, because both sizes "
            "exceed the half-spread, so the excess is linear. Dispersion matters only when some jumps are smaller than "
            "the half-spread, which is where the tails come in."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: a maker's edge; Avellaneda and Stoikov's spread; k from fill probabilities; the value of "
            "speed; the rent in a pinned spread; ETF arbitrage; sniping probabilities; the sniping spread; batch "
            "auctions; and the speed investment. Then two qualifying-exam problems: the sniping equilibrium in full, and "
            "GLFT's quotes from the HJB. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"automated market makers: liquidity priced by a curve, not quotes", [39]),
            (r"liquidity that vanishes in stress, and who provides it then", [41]),
            (r"learning agents that quote, and markets made by machines", [42]),
            (r"whether anyone can beat the market, net of what makers earn", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-nine replaces quotes with a pricing curve: the automated market maker. "
            "Part forty-one asks who provides liquidity when it vanishes. Part forty-two puts learning agents in the "
            "maker's chair. And Part forty-three asks whether anyone beats the market after paying the makers."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Guéant, \textit{The Financial Mathematics of Market Liquidity} (2016); Cartea, Jaimungal and Penalva, "
             r"\textit{Algorithmic and High-Frequency Trading} (2015), ch.~10; Lehalle and Laruelle, \textit{Market "
             r"Microstructure in Practice} (2018); Gastineau, \textit{The Exchange-Traded Funds Manual} (2010)"],
            [r"Garman (1976); Ho and Stoll (1981); Glosten and Milgrom (1985); Avellaneda and Stoikov (2008); Menkveld "
             r"(2013); Guéant, Lehalle and Fernandez-Tapia (2013); Cartea, Jaimungal and Ricci (2014); Budish, Cramton and "
             r"Shim (2015); Dayri and Rosenbaum (2015); Menkveld and Zoican (2017)",
             r"Baron, Brogaard, Hagströmer and Kirilenko (2019); Pan and Zeng (2019); Baldauf and Mollner (2020); "
             r"Aramonte and Avalos (2020); Haddad, Moreira and Muir (2021); Aquilina, Budish and O'Neill (2022). Data: "
             r"Binance's public archive; Yahoo Finance"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Garman's inventory model to the races "
            "measured in London. Every number on screen was computed by the House's code from Binance's public best "
            "quotes and trades, Yahoo Finance's bars, or simulation."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("mm",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 39, Crypto and DeFi", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now knows what market making costs, at what speed, and where its rules must stop it. "
            "<bookmark mark='a'/> Next, Part thirty-nine: crypto and decentralised finance. Perpetual futures and their "
            "funding, exchanges without order books, and what happens when a venue fails."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
