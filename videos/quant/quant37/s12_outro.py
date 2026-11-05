from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BAD, GOOD, IMPACT_C, KERNEL_C, PART, RL_C, SCHED_C, TWAP_C, load)

DESK = [
    (r"10\% of daily volume costs 30 bp. What does 40\% cost?",
     r"under the square-root law, $30\sqrt{4} = 60$ bp; a straight line would say 120"),
    (r"Why is impact concave?",
     r"liquidity is latent and its density grows linearly away from the price, so a buyer eats a triangle: "
     r"$Q \propto \Delta^2$"),
    (r"Order signs are predictable; why are prices not?",
     r"each trade's impact decays, at the rate $\beta = (1 - \gamma)/2$ that exactly offsets the memory of signs"),
    (r"What must an impact model satisfy?",
     r"a positive-definite decay kernel (no profitable round trips), and preferably convex and decreasing (no buying by "
     r"selling)"),
    (r"How does a risk-averse seller trade?",
     r"front-loaded: holdings follow $\sinh\kappa(T - t)$ with $\kappa = \sqrt{\lambda\sigma^2/\eta}$"),
    (r"The book recovers between trades. How should you trade?",
     r"equal blocks at the start and end, and the recovery rate between (Obizhaeva--Wang)"),
]

PROBLEMS = [
    r"Square root: 1\% of volume moves the price 10 bp. What do 4\% and 9\% do? What does a linear law say?",
    r"A latent book of slope $\mathcal L = 2$ per tick: the impact of buying 9 units at once.",
    r"Signs with $\gamma = 0.6$: the propagator exponent that keeps prices diffusive.",
    r"A box kernel $G = 1$ for $t < \tau$: construct a round trip with negative expected cost.",
    r"Almgren--Chriss with $\lambda\sigma^2/\eta = 0.01$ per minute$^2$: $\kappa$, and the share held after 20 minutes.",
    r"TWAP over an hour, 5{,}000 BTC, $\sigma = \$12$ a minute: the shortfall's standard deviation.",
    r"Obizhaeva--Wang, $\rho T = 2$, $X = 1$: blocks, rate and cost; and TWAP's cost.",
    r"A VWAP order of 1{,}000 BTC with 7.5\% of the volume in one hour: that hour's trades.",
    r"POV at 5\% against 20\% for an order of 2\% of daily volume: the times, the impact, the risk.",
    r"A signal worth 10 bp, $\sigma_{\text{day}} = 2\%$, $V = \$10$bn: the largest sensible order.",
    r"(qual) Prove that for a strictly positive-definite kernel the optimal schedule is unique and satisfies "
    r"$\int G(|t - s|)\,dX^*_s = \lambda$, and derive Obizhaeva--Wang's solution and cost.",
    r"(qual) Derive Almgren--Chriss's discrete schedule from the first-order conditions, show "
    r"$\cosh\kappa\tau = 1 + \lambda\sigma^2\tau^2/(2\tilde\eta)$, and find the limits $\lambda \to 0$ and $\lambda \to "
    r"\infty$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("aggregate"), load("latent"), load("propagator"), load("ac"), load("ow"), load("rl"),
                   load("research"))
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

    def recap(self, ag, lt, p, ac, ow, rl, rs):
        r = rl["res"]
        items = [
            (r"metaorders: impact rises concavely while they run, and about a third reverts", IMPACT_C),
            (rf"Bitcoin: a minute's move grows like signed volume to the power {ag['slope']:.2f}", IMPACT_C),
            (r"the square-root law: $I \approx Y\sigma\sqrt{Q/V}$, across markets", IMPACT_C),
            (rf"latent liquidity explains it; the simulated exponent falls from {lt['slope_small']:.1f} to "
             rf"{lt['slope_large']:.2f}", IMPACT_C),
            (rf"the propagator decays ($\beta = {p['beta']:.2f}$) to offset sign memory", KERNEL_C),
            (r"no dynamic arbitrage: positive-definite, preferably convex, kernels", KERNEL_C),
        ]
        items2 = [
            (r"Almgren--Chriss: front-load by urgency; risk dwarfs cost", SCHED_C),
            (r"linear temporary impact understates the cost the square root predicts", BAD),
            (rf"Obizhaeva--Wang: blocks of {100 * ow['closed']['block']:.1f}\% at each end for $\rho T = 10$", SCHED_C),
            (rf"a Q-learning executor: {r['Q-learning']['mean']:.1f} against TWAP's {r['TWAP']['mean']:.1f}", RL_C),
            (r"TWAP, VWAP, POV, IS; routing; TCA against the arrival price", TWAP_C),
            (r"Rule 37: price the trade before you make it", QC.HOUSE),
            (r"research: the optimal schedule under transient impact, unique, proved", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 37 in thirteen lines")
        with self.voiceover(
            "Part thirty-seven in thirteen lines. Metaorders push the price concavely while they run, and about a third "
            "of it reverts. On Bitcoin, a minute's move grows less than proportionally with signed volume. The "
            "square-root law holds across markets, and latent liquidity explains it. The propagator decays just fast "
            "enough to offset the memory of order signs. And impact models must forbid money machines."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 37 in thirteen lines")
        with self.voiceover(
            "Almgren and Chriss front-load by urgency, and their risk dwarfs their cost, though linear impact understates "
            "the cost. Obizhaeva and Wang trade blocks at the ends. A learned executor did not beat TWAP. The brokers' "
            "algorithms are these schedules, judged against the arrival price. And the research chapter proved the "
            "optimal schedule under transient impact."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"size first, schedule second", r"under the square root, how much is traded sets most of the "
                          r"cost; the best schedule saves a few percent of it", width=12.4, font_size=19),
            desk_question(r"models must be allowed", r"an impact model is a statement about free lunches; test it before "
                          r"you optimise against it", width=12.4, font_size=19),
            desk_question(r"judge learning against the plain answer", r"a learner that cannot beat TWAP in a simulator "
                          r"will not beat it in a market", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Size first, schedule second: under the square root, how much is traded "
            "sets most of the cost, and the best schedule saves a few percent of it. <bookmark mark='b'/> Impact models "
            "make claims about free lunches; test them before optimising against them. <bookmark mark='c'/> And judge "
            "learning against the plain answer: a learner that cannot beat TWAP in a simulator will not beat it in a "
            "market."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"I \approx Y\sigma\sqrt{Q/V}", font_size=34, color=IMPACT_C),
            MathTex(r"\Delta = \sqrt{2Q/\mathcal L}", font_size=34),
            MathTex(r"\beta = (1 - \gamma)/2", font_size=34, color=KERNEL_C),
            MathTex(r"\mathcal C = \tfrac12 \iint G(|t - s|)\,dX_s\,dX_t \ge 0", font_size=34),
            MathTex(r"x(t) = X\sinh\kappa(T - t)/\sinh\kappa T,\quad \kappa = \sqrt{\lambda\sigma^2/\eta}", font_size=34,
                    color=SCHED_C),
            MathTex(r"dX^* = \tfrac{X}{2 + \rho T}(\delta_0 + \rho\,dt + \delta_T),\quad \mathcal C^* = \tfrac{X^2}{q(2 + \rho T)}",
                    font_size=32, color=SCHED_C),
        ).arrange(DOWN, buff=0.32)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "The part on one card. The square-root law. The latent book's triangle. The propagator's balance with sign "
            "memory. The cost of a schedule under transient impact, never negative for an allowed kernel. Almgren and "
            "Chriss's hyperbolic sine. And Obizhaeva and Wang's blocks, with their cost."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.5,
                                                run_time=8))
        self.wait(0.6)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 31's costs and capacity now have their microstructure: the square root, "
                          r"its prefactor and its decay; Part 35's Kyle is the linear, permanent special case",
                          width=12.4, font_size=19),
            desk_question(r"sideways", r"Part 36's book supplied the simulator and the signals; Part 8's control and "
                          r"mean-field games supplied the mathematics", width=12.4, font_size=19),
            desk_question(r"forwards", r"the market maker of Part 38 earns what the executor pays, and Part 41's fire "
                          r"sales are metaorders that everyone sends at once", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: Part thirty-one's costs now have their "
            "microstructure, and Kyle's model of Part thirty-five is the linear, permanent special case. "
            "<bookmark mark='b'/> Sideways: Part thirty-six supplied the simulator and the signals, and Part eight the "
            "mathematics. <bookmark mark='c'/> Forwards: the market maker of Part thirty-eight earns what the executor "
            "pays, and the fire sales of Part forty-one are metaorders that everyone sends at once."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
            "Six desk questions. Ten percent of volume costs thirty basis points; forty percent? Sixty, by the square "
            "root. <bookmark mark='a'/> Why is impact concave? Latent liquidity in a V. <bookmark mark='b'/> Why are "
            "prices unpredictable when signs are? Impact decays."
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
            "What must an impact model satisfy? A positive-definite kernel. <bookmark mark='a'/> How does a risk-averse "
            "seller trade? Front-loaded. <bookmark mark='b'/> And when the book recovers? Blocks at the ends. Full "
            "solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        rt = 2.0
        blk = 1 / (2 + rt)
        rate = rt * blk
        cost = 1 / (2 + rt)
        twap = (1 / rt) * (1 - (1 - math.exp(-rt)) / rt)
        save = 100 * (1 - cost / twap)
        cards = VGroup(
            desk_question(r"Research: $\rho T = 2$", rf"blocks of $1/(2 + 2) = {blk:.2f}$ at each end, a rate of "
                          rf"{rate:.2f} between, cost {cost:.3f}; TWAP costs "
                          rf"$\frac12\left(1 - \frac{{1 - e^{{-2}}}}{{2}}\right) = {twap:.3f}$, "
                          rf"{100 * (1 - cost / twap):.0f}\% more", width=12.4, font_size=20),
        )
        with self.voiceover(
            f"The research chapter's pause, answered. Blocks of a quarter at each end, a rate of {rate:.1f} between, and "
            f"a cost of {cost:.2f}. TWAP costs {twap:.3f}: the optimum saves {save:.0f} percent."
        ):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: the square root; a latent book; the propagator's exponent; a money machine; Almgren "
            "and Chriss's urgency; TWAP's risk; Obizhaeva and Wang; a VWAP hour; participation; and sizing against an "
            "alpha. Then two qualifying-exam problems: the optimal schedule under transient impact, and Almgren and "
            "Chriss from first principles. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the market maker on the other side of the executor", [38]),
            (r"liquidity on decentralised exchanges, priced by a curve", [39]),
            (r"liquidity risk and fire sales in stress", [41]),
            (r"execution agents among other machines", [42]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-eight sits on the other side, as the market maker the executor trades "
            "with. Part thirty-nine meets liquidity priced by a curve. Part forty-one asks what happens to impact when "
            "everyone must sell at once. And Part forty-two puts executors among other machines."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bouchaud, Bonart, Donier and Gould, \textit{Trades, Quotes and Prices} (2018); Cartea, Jaimungal and "
             r"Penalva, \textit{Algorithmic and High-Frequency Trading} (2015); Guéant, \textit{The Financial Mathematics "
             r"of Market Liquidity} (2016); Lehalle and Laruelle, \textit{Market Microstructure in Practice} (2018)"],
            [r"Kraus and Stoll (1972); Loeb (1983); Perold (1988); Torre (1997); Bertsimas and Lo (1998); Almgren and "
             r"Chriss (2000); Konishi (2002); Almgren (2003); Bouchaud et al.\ (2004); Huberman and Stanzl (2004); "
             r"Almgren et al.\ (2005); Brunnermeier and Pedersen (2005); Nevmyvaka, Feng and Kearns (2006); Almgren and "
             r"Lorenz (2007); Moro et al.\ (2009); Gatheral (2010); Alfonsi, Fruth and Schied (2010)",
             r"Tóth et al.\ (2011); Alfonsi, Schied and Slynko (2012); Gatheral, Schied and Slynko (2012); Bershova and "
             r"Rakhlin (2013); Obizhaeva and Wang (2013); Donier and Bonart (2015); Donier, Bonart, Mastromatteo and "
             r"Bouchaud (2015); Zarinelli et al.\ (2015); Kyle and Obizhaeva (2016); Patzelt and Bouchaud (2018); "
             r"Cardaliaguet and Lehalle (2018); Bucci et al.\ (2019); Lehalle and Neuman (2019); Ning, Lin and Jaimungal "
             r"(2021). Data: Binance's public archive"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Kraus and Stoll's block trades to deep "
            "reinforcement learning. Every number on screen was computed by the House's code from Binance's public "
            "trade tape, best quotes and bars, or from simulation."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("execution",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 38, Market Making, ETFs and the Speed Race", font_size=30,
                    color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now price a trade before making it, schedule it, and measure what it cost. "
            "<bookmark mark='a'/> Next, Part thirty-eight: market making, exchange-traded funds and the speed race. The "
            "other side of every order in this part, and how it earns a living."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
