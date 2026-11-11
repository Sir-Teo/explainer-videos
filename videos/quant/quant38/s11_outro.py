from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, ETF_C, FAST_C, GOOD, HURDLE, MAKER_C, PART, SNIPE_C, SPREAD_C, load)

DESK = [('How should a maker account for profit?', 'marked wealth = execution edge + rebates + inventory gains; horizon edge is a separate marked view, so do not subtract the same adverse move twice'), ('Why skew quotes with inventory?', 'within the stated model, a long position increases bid distance and reduces ask distance; width and skew also depend on risk and boundary assumptions'), ('What do reach probabilities establish?', 'threshold reach frequencies and equivalent rates; feeding them into GLFT gives a model illustration, not queue-fill or executable-profit validation'), ('What does a pinned spread change?', 'a binding tick can move competition toward queue priority; actual rents and welfare also depend on fills, information, fees and capital'), ('What keeps an ETF near basket value?', 'creation and redemption under executable prices, costs and constraints; published NAV can be stale and need not be a hard arbitrage bound'), ('What does the sniping root prove?', 'under the simplified role assumptions, half-spread is independent of $N$; industry revenue, pure-sniper transfers and speed-investment welfare remain distinct')]

PROBLEMS = ['Chosen horizon: execution edge 0.5 tick, rebate 0.2, adverse taker-direction mid move +0.9. Compute marked edge; state why it is not an extra term in the inventory ledger.', 'AS approximation: $\\gamma=0.1$, $\\sigma^2(T-t)=4$ price units squared, $k=1.5$, $q=2$. Compute total spread and reservation shift.', 'One-second reach probabilities are 0.30 at 1 tick and 0.05 at 45 ticks. Convert to Poisson-equivalent rates and solve the two-point exponential $k$ and half-distance.', 'Slow and hindsight variants lose 20 ticks on 40{,}000 fills and 9 on 20{,}000. Compute total-loss gap; why is this not causal speed value?', 'Fixed-mid illustration: one-cent spread versus 0.3-cent unconstrained spread, no fees or adverse selection. Compute full-spread and per-side markup; distinguish allocation from identified profit.', 'ETF costs \\$80; executable basket gross \\$84 and selling cost 2\\% of gross. Compute redemption profit. Repeat if executable gross is \\$79 despite a published NAV of \\$84.', 'Profitable stale-quote race, uniform independent priority among $N$ equal-speed messages. Compute sniping probability for $N=5,10$, and pure-sniper aggregate profit as a share of industry profit.', '$\\lambda_I=10$, $\\lambda_J=2$: solve the role root for constant magnitude 3, then equal-probability magnitudes 1 and 5. Explain the equality using the positive-part function.', 'Uniform news phase, deterministic latency $\\delta=5\\,\\mu$s, batch $\\tau=50$ ms. Compute exposure fraction $u$, then $h_u/h_1$ with $\\lambda_I=10$, $\\lambda_J=2$. State the extra race assumptions.', 'Four-firm binary investment game: fixed prize $R$ shared by fast firms only; if none is fast all share equally. Cost $c$ per firm. Derive gains for 0--3 fast rivals and strict dominance threshold.', '(qual) For $N\\ge2$, positive arrival rates and integrable nonnegative jump magnitude $U$ with $\\Pr(U>0)>0$, prove a unique role root and its convex-order monotonicity. Distinguish industry revenue from pure-sniper transfers.', "(qual) Derive GLFT's CARA HJB, quote FOC and finite-inventory linear system. Give its long-horizon spectral solution and interior Gaussian approximation; distinguish their risk-neutral limits at fixed inventory cap."]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("maker"), load("fills"), load("glft"), load("deep"), load("bcs"))
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

    def recap(self, mk, f, g, dp, b):
        d = mk["days"]["2023-05-17"]
        items = [
            (r"full ledger: execution edge + rebates + inventory gains; markouts are a separate view", MAKER_C),
            (rf"Bitcoin at the touch: {d['slow']['pnl_per_fill']:+.0f} ticks a fill slow, "
             rf"{d['fast']['pnl_per_fill']:+.0f} fast, {d['fast, filtered']['pnl_per_fill']:+.1f} filtered", SNIPE_C),
            (r"the same-step move is one large negative component; later marks also matter", SNIPE_C),
            (rf"fill rates $A e^{{-k\delta}}$ with $1/k \approx {1 / f['k']:.0f}$ ticks; GLFT quotes far out", SPREAD_C),
            (r"far reach marks can be positive; queues, fees and inventory are omitted", GOOD),
            (r"a pinned spread turns price competition into a queue race", FAST_C),
        ]
        items2 = [
            (r"ETFs: creation and redemption keep the price in a cost band", ETF_C),
            (r"March 2020: bond ETF dislocations discussed from cited literature", BAD),
            (r"the sniping spread is independent of the number of firms", HURDLE),
            (r"a specified fixed-prize investment game has a prisoner's dilemma", FAST_C),
            (r"HFT profits: spread and rebates minus positioning; concentrated in the fastest", MAKER_C),
            (r"Rule 38: quote only what you can measure", QC.HOUSE),
            (rf"research: conditional role root; Bitcoin proxy spread {b['btc']['general_half']:.2f} tick", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 38 in thirteen lines")
        with self.voiceover(
            'Part thirty-eight, recapped. Marked wealth uses execution edge, rebates and inventory gains. A horizon mark is another view, not an additional loss in that ledger. Our coarse-grid touch replay loses, with different selected fills under hindsight and filtering. Reach probabilities produce equivalent rates, not queue fills. Model quotes and far reach marks are illustrations with omitted execution and inventory costs. Tick constraints change price and priority incentives.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 38 in thirteen lines")
        with self.voiceover(
            "ETF arbitrage depends on executable baskets, settlement and capital; the March twenty-twenty case is sourced literature. The initial March facility covered investment-grade bond ETFs; high-yield eligibility expanded in April. A unique role-indifference spread follows from the simplified equal-speed assumptions. Industry profit and pure-sniper transfers differ. A separate fixed-prize investment game can have a prisoner's dilemma. Rule thirty-eight is a proposed validation standard."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"keep one consistent profit ledger", r"what decides a maker's fate is the markout after its "
                          r"fills, which depends on speed, queue position and forecasts", width=12.4, font_size=19),
            desk_question(r"models fit to the right thing", r"reach probabilities alone do not establish queue execution or profitability; validate every "
                          r"modeled execution, mark and cost assumption", width=12.4, font_size=19),
            desk_question(r"market design sets the prize", r"tick size, matching rules and batch intervals decide whether "
                          r"firms compete on price or on speed, and who pays", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Gross execution revenue and horizon-consistent marked gains need one consistent ledger. <bookmark mark='b'/> Reach probabilities, quote-control models and executable profit are different objects requiring different validation. <bookmark mark='c'/> Tick, priority and batch rules change incentives, but a welfare conclusion needs explicit resource costs, information and participation assumptions."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        scope = wrapped_label(r"Model scopes: horizon edge; reach-rate inputs; interior GLFT approximation; executable ETF basket; equal-speed role root; separate uniform-phase batch heuristic.", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.25)
        self.add(scope)
        with self.voiceover(
            'The formulas with their scopes. Horizon edge uses execution edge and adverse markout once. The exponential rate is a model, fed here with reach proxies. GLFT is an interior approximation, with finite-inventory qualifications. The ETF band uses executable basket values. The sniping root is conditional on equal-speed role assumptions. The batch expression is a separate uniform-phase, fixed-latency exposure heuristic, not the output of the batch-flag simulation.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.5,
                                                run_time=8))
        self.wait(0.6)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 35's dealer models become a business with costs; Part 36's markout definitions and "
                          r"queue value become its P\&L; Part 37's executor is its customer", width=12.4, font_size=19),
            desk_question(r"sideways", r"Part 11's options maker and Part 12's surface are the same business in "
                          r"another product", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 39's automated market makers quote by formula; Part 41's crises are when "
                          r"makers step back; Part 42's learning agents take the maker's chair", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: Part thirty-five's dealer models become a business "
            "with costs; Part thirty-six's markouts become its profit and loss; Part thirty-seven's executor is its "
            "customer. <bookmark mark='b'/> Sideways: Part eleven's options maker is the same business in another "
            "product. <bookmark mark='c'/> Forwards: Part thirty-nine's automated makers quote by formula, Part "
            "forty-one's crises are when makers step back, and Part forty-two's learning agents take the maker's chair."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
            "Six desk questions. How should a maker account for profit? Keep a consistent marked-wealth ledger, and do not subtract a horizon mark twice. <bookmark mark='a'/> Why skew inventory? To change the arrival incentives within the chosen model. <bookmark mark='b'/> What do reach probabilities establish? Threshold frequencies, not actual queue fills or a validated optimal quote."
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
            "What does a pinned spread change? It can shift competition toward priority, while actual rents need further evidence. <bookmark mark='a'/> What keeps an ETF near basket value? Executable creation and redemption, subject to costs and constraints rather than a hard bound at a stale published NAV. <bookmark mark='b'/> What does the sniping root establish? A conditional role spread. Industry revenue, pure-sniper transfers and investment welfare are different quantities. Complete answers are in the notes."
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
                          r"same here because the positive-part payoff is affine on both supports; convex-order widening need not be strict, and the comparison depends on mass "
                          r"around the relevant kink", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "The random-jump pause. <bookmark mark='a'/> With investor rate ten, jump rate two and magnitude three, the root is half a tick. <bookmark mark='b'/> A one-or-five mixture has the same root because both magnitudes exceed half a tick. The positive-part function is linear on that support. Convex-order increases can leave the root unchanged; a strict widening needs additional excess mass at the relevant kink, not a generic statement about tails."
        ) as vo:
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        def page(lo,hi,title):
            head=label(title,font_size=32,color=QC.IDEA).to_edge(UP,buff=0.35)
            rows=VGroup(*[wrapped_label(str(i+1)+". "+PROBLEMS[i],12.0,27) for i in range(lo,hi)])
            rows.arrange(DOWN,aligned_edge=LEFT,buff=0.32)
            if rows.height>6.0:rows.scale_to_fit_height(6.0)
            rows.next_to(head,DOWN,buff=0.35)
            return head,rows
        with self.voiceover("Twelve problems with complete bilingual solutions. Six basic problems cover consistent edge accounting, the Avellaneda and Stoikov approximation, Poisson-equivalent rate conversion, selected replay losses, a fixed-mid tick markup and executable ETF redemption. <bookmark mark='a'/> Four advanced problems distinguish random priority and industry accounting, the random-jump root, batch exposure from a spread ratio, and strict dominance in an explicitly specified four-firm investment game. <bookmark mark='b'/> The two qualifying problems prove the integrable random-magnitude root and convex-order comparison, then derive the CARA HJB, quote first-order condition, finite-inventory linear system and spectral limit. The exact fixed-cap risk-neutral limit must be distinguished from the interior Gaussian approximation. All units and additional assumptions belong to the problems, not to claims of identified market profit.") as vo:
            head,rows=page(0,6,r"Basic problems 1--6")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(3)
            vo.wait_until("a")
            self.clear_scene()
            head,rows=page(6,10,r"Advanced problems 7--10")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(3)
            vo.wait_until("b")
            self.clear_scene()
            head,rows=page(10,12,r"Qualifying problems 11--12")
            self.play(FadeIn(head),FadeIn(rows))
            self.wait(6)
        self.wait(1)
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
             r"Binance's public archive; simulation; ETF literature and official term sheets"])
        with self.voiceover(
            'The cited textbooks and papers distinguish models from attributed institutional evidence. Our successful numerical originals use public Binance inputs and stipulated simulations. Chosen arithmetic is labeled separately. The ETF discussion uses the cited BIS study and official term sheets, with no newly verified price series. Exact audits, the rejected input and final review limitations are retained in the notes.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("mm",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 39, Crypto and DeFi", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House has a proposed framework for measuring quoting costs and testing model assumptions, not a completed live market-making business. <bookmark mark='a'/> Next, Part thirty-nine: crypto and decentralized finance, perpetual funding, curve-based liquidity and venue failures. The same distinctions between accounting, assumptions and identified evidence will matter there."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
