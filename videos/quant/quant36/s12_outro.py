from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, HURDLE, MICRO_C, NET_C, OFI_C, PART, SIM_C, load)

DESK = [
    (r"What is order-flow imbalance, and why does it beat signed trades?",
     r"the net change in the best queues from adds, cancels and trades; limit orders carry as much information as "
     r"trades, and the response to OFI is close to linear"),
    (r"Why does a queue imbalance predict the next tick?",
     r"with a one-tick spread the price moves when a best queue empties, and the shorter queue tends to empty first"),
    (r"What is the microprice, and when can you trust it?",
     'a centered state adjustment under explicit Markov-additive, integrability and mixing assumptions; validate its clock, support and horizon'),
    (r"Why is the weighted mid not a fair price?",
     'a path illustration is insufficient; the weighted formula generally fails the model-specific martingale equation'),
    (r"Why is a fill at the back of the queue bad news?",
     'fill selection can be adverse under the replay assumptions; this is not a universal fill or informed-trading claim'),
    (r"How would you score an order-book simulator?",
     r"on stylised facts out of sample: move rate, burstiness, sign memory, fat tails, queue sizes, and its reaction to "
     r"the user's own orders"),
]

PROBLEMS = [
    r"A queue of 5 BTC ahead; trades 0.2 BTC/s, cancels 0.1 BTC/s from ahead. Time to the front, and to fill 1 BTC.",
    r"Queues of 9 and 3: the up-tick probability under Cont--de Larrard and under ``probability = imbalance''.",
    r"Hawkes: background 2/s, branching 0.68, then 0.95. Mean rates; the share of events that are endogenous.",
    r"Signs with ACF $\propto \ell^{-0.85}$: why the variance of the sum of $n$ signs grows faster than $n$.",
    r"OFI of $+12$ BTC against queues of 8 BTC, tick \$0.10: the mid move under the stylised model.",
    'Bid \\$100.00 for 500 shares; ask \\$100.01 for 100: mid, weighted mid, and expected next mid under independent, equal-variance, driftless Brownian queues and half-tick mid moves.',
    r"80 of 100 nonzero signs correct; gross gain 1.5 ticks, round-trip spread 1, fees 3 per side. Compute net and state limits.",
    r"Queues $(1,1)$ and $(10,10)$ share imbalance $1/2$. Remove one bid unit with probability 0.2: test Markov sufficiency.",
    'Fill probability 0.82; signed 1-s markout $-14.7$ ticks includes entry spread; unfilled value zero. Compute gross contribution per submission and state omissions.',
    r"Can cancellation on a state signal be guaranteed to improve markout? Give a numerical counterexample and a valid evaluation design.",
    '(qual) Under finite-state H1--H3 and integrable first-move rewards, prove convergence, the centered inverse formula, and uniqueness up to a constant fixed by mirror antisymmetry.',
    '(qual) Two mirror states: $B=\\bigl(\\begin{smallmatrix}p&1-p\\\\1-p&p\\end{smallmatrix}\\bigr)$, $0<p<1$, reward $g^1=(2q-1)(1,-1)$ ticks. Solve centered $g$; compare fixed $q>1/2$, $p\\to1$ with $q=1/2$.',
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("book"), load("micro"), load("memory"), load("ofi"), load("deep"), load("qr"), load("queue"),
                   load("research"))
        self.lessons()
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

    def recap(self, bk, m, me, o, d, q, z, r):
        r10 = float(np.mean([x["r2"] for x in o["fits"]["10 s"]]))
        items = [
            (r"the book: price-time priority, one-tick spreads, queues that refill", GREY_A),
            (rf"queue imbalance moves P(up) from {100 * m['p_up'][0]:.0f}\% to {100 * m['p_up'][-1]:.0f}\%; "
             r"Cont--de Larrard is too steep", MICRO_C),
            (f"Hawkes model (branching {me['hawkes']['branching']:.2f}); signs remember ($\\ell^{{-{me['gamma']:.2f}}}$)", HURDLE),
            (f"OFI explains {100 * r10:.0f}\\% of 10-s mid changes; descriptive slope versus depth$^{{{o['depth_slope']:.2f}}}$",
             OFI_C),
            ('weighted mid needs a model check; centered microprice has explicit martingale hypotheses', MICRO_C),
            (rf"on Bitcoin the microprice leans {abs(m['g'][9] / m['tick']):.0f} ticks and overshoots; a table of mean "
             r"moves works", BAD),
        ]
        items2 = [
            (r"DeepLOB, universal features, LOBCAST: the benchmark gains shrink on new data", NET_C),
            (rf"our network: {100 * d['1 s']['network']['test_acc']:.0f}\% against a linear "
             rf"{100 * d['1 s']['linear']['test_acc']:.0f}\% on unseen days", NET_C),
            (rf"a queue-reactive simulator: one fact right, four wrong (kurtosis {q['model']['kurt_10s']:.1f} against "
             rf"{q['data_train']['kurt_10s']:.0f})", SIM_C),
            (f"back-of-queue fills: {z['back']['markout']['1 s']:+.0f} ticks after a second; front/back gross functionals use different filled sets", BAD),
            ('a resting quote has option-like stale-price risk in specified models', HURDLE),
            (r"Rule 36: score the book against the spread", QC.HOUSE),
            (f"research: the microprice theorem; coarse simulator states are approximate; Bitcoin coefficient peaks at {max(r['btc']['beta']):.2f}", GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 36 in thirteen lines")
        with self.voiceover(
            "The first six conclusions. Displayed queues describe a venue's best prices under its matching rules. Imbalance is associated with the next-move sign. A fitted Hawkes model represents clustering but does not identify causal trader reactions, and finite-window sign correlations need cautious extrapolation. Same-interval OFI is descriptive. The state-adjusted martingale theorem has explicit centering, mixing and integrability assumptions. On these Bitcoin dates the fitted many-move adjustment overshoots, while horizon-specific tables offer modest held-out error reductions."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 36 in thirteen lines")
        with self.voiceover(
            'The remaining conclusions. This short network comparison does not beat the linear sign baseline, and its accuracy excludes flat targets. The simulator matches some summaries and misses others; full-state Markovity need not survive bucketing. The fill replay has adverse signed averages under explicit queue assumptions, without net-profit or causal priority-value certification. Proposed Rule thirty-six asks for baselines, costs and simulator response checks. The theorem is a model result; numerical and conditional diagnostics must be interpreted separately.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"check the hypotheses, not only the proof", 'the centered theorem requires stated model assumptions; finite conditional diagnostics do not certify exact market Markovity', width=12.4, font_size=19),
            desk_question(r"baselines first", r"the imbalance alone, a linear rule and a table of mean moves did as well "
                          r"as or better than the network and the theory; every claim was scored against them",
                          width=12.4, font_size=19),
            desk_question(r"measure in the units you pay", r"ticks against a one-tick spread, markouts per fill: a "
                          r"high accuracy, a high fill rate or a converging series can all be worth nothing",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three research habits. <bookmark mark='a'/> State and examine the model hypotheses separately from a proof: centering, support, mixing and the observation clock all matter. Conditional diagnostics can reveal omitted history without certifying full Markovity. <bookmark mark='b'/> Preserve simple baselines and the exact target definition; a linear direction score, a horizon table and a many-move state correction answer different questions. <bookmark mark='c'/> Report both gross diagnostics and executable costs, fill selection and inventory consequences. A high accuracy, high fill rate or convergent matrix series is not by itself a profitable strategy."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
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
            "Six desk questions. What is order-flow imbalance? The net change of the best queues, from every kind of "
            "event. <bookmark mark='a'/> Why does queue imbalance predict the next tick? The short queue empties first. "
            "<bookmark mark='b'/> What is the microprice, and when can you trust it? On large-tick books, and after "
            "testing."
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
            "Why is the weighted mid not a fair price? Its changes are predictable. <bookmark mark='a'/> Why is a fill "
            "at the back of the queue bad news? It comes just before the price goes through. <bookmark mark='b'/> And "
            "how would you score a simulator? On stylised facts, out of sample, and on how it reacts to your own "
            "orders. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        def answer_block(title, formula, explanation):
            head = label(title, font_size=24, color=QC.IDEA)
            equation = MathTex(formula, font_size=34)
            if equation.width > 12.2:
                equation.scale_to_fit_width(12.2)
            note = wrapped_label(explanation, 12.2, 18, GREY_A)
            return VGroup(head, equation, note).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cards = VGroup(*[answer_block(t, f, n) for t, f, n in [('Book: deterministic fluid queue', 't_{\\rm front}=5/0.3=16.67\\ \\mathrm{s},\\quad t_{\\rm fill}=16.67+5=21.67\\ \\mathrm{s}', 'Only aggressive trades execute the submitted order.'), ('Queues: Brownian probability versus imbalance', '1-\\frac2\\pi\\arctan(1/3)=0.7952,\\qquad I=9/12=0.75', 'Proportional queue rescaling preserves probabilities, not the time distribution.'), ('Events: stationary Hawkes cluster arithmetic', '\\mathbb E[N]=3.125,20;\\qquad\\bar\\lambda=6.25,40\\ \\mathrm{s}^{-1}', 'At branching one, the positive stationary mean is not finite.'), ('OFI: the stipulated constant-depth relation', '\\Delta m=0.10(12)/16=\\$0.075=0.75\\ \\mathrm{tick}', 'Double depth gives half the stipulated response; not causal identification.'), ('Microprice: errors on identical observations', '\\mathrm{MSE}_{\\rm mid}:\\mathrm{MSE}_{\\rm micro}:\\mathrm{MSE}_{h}=100:500:95', 'The increases/reductions are 400 percent worse and 5 percent better.')]]).arrange(DOWN, buff=0.20)
        assert cards.height < 7.2, "Arithmetic answer blocks need larger-page staging"
        with self.voiceover("The first five quantitative pauses. The fluid queue takes sixteen point six seven seconds to reach the front and five more to fill, twenty-one point six seven in total. The Brownian up probability is point seven nine five two, versus imbalance point seven five, with unchanged probabilities after proportional rescaling. Hawkes family sizes are three point one two five and twenty, giving rates six point two five and forty per second under stationarity. The stipulated OFI relation gives seven and a half cents, or three-quarters of a tick, halved by twice the depth. Normalized errors are one hundred, five hundred and ninety-five: four hundred percent worse is not five hundred percent worse."):
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.5, run_time=5))
        self.wait(0.5)
        self.clear_scene()
        cards = VGroup(*[answer_block(t, f, n) for t, f, n in [('Deep: conditional accuracy and specified costs', '80/100=80\\%,\\qquad G_{\\rm net}=1.5-1-2(3)=-5.5\\ \\mathrm{ticks}', 'Flat targets excluded; immediate entry and exit are stipulated.'), ('Simulator: equal imbalance, unequal move law', 'I=\\tfrac12:\\quad p_{\\downarrow}(1,1)=0.2,\\quad p_{\\downarrow}(10,10)=0', 'The full-state projection need not be Markov additive.'), ('Replay: a contribution per submission', '0.8(-2+0.1)=-1.52\\ \\mathrm{ticks/submission}', 'Entry spread is already included; unfilled value is assigned zero.'), ('Proposed Rule 36: cost budget', 'G_{\\rm break\\ even}=0.5+0.5+3+3=7\\ \\mathrm{ticks}', 'A stipulated gross gain of 1.5 ticks is 5.5 ticks short.'), ('Research: centered two-state adjustment', 'g_H=\\frac{2q-1}{2(1-p)}=1\\ \\mathrm{tick}\\quad(p=q=3/4)', 'For fixed q above one half, the lean diverges as p tends to one.')]]).arrange(DOWN, buff=0.20)
        assert cards.height < 7.2, "Arithmetic answer blocks need larger-page staging"
        with self.voiceover("The remaining five. Eighty-percent conditional sign accuracy can coexist with minus five and a half ticks after the stipulated immediate round-trip costs. Two full queue states with equal imbalance have different depletion probabilities, so the projection can lose the Markov property. The replay contribution including rebate is minus one point five two ticks per submission, with entry spread already counted. The proposed cost budget needs seven gross ticks to break even. Finally, the antisymmetric two-state reward is an eigenvector with eigenvalue two p minus one; summing its geometric series gives one tick at p and q equal to three-quarters. With q fixed above one half, the adjustment diverges as persistence approaches one; at one, irreducibility and the centered-limit argument fail."):
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.5, run_time=5))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            'Twelve fully worked problems, with six basic, four advanced and two qualifying problems. The first six cover deterministic queue time, diffusion depletion probability, stationary Hawkes arithmetic, sign-sum variance, stipulated OFI impact and the interview midpoint. The advanced set covers conditional accuracy and net costs, loss of Markov sufficiency after projection, partial replay accounting and a counterexample to guaranteed cancellation benefits. The qualifying set proves the centered finite-chain microprice theorem and solves the symmetric two-state model, including its boundary cases. Complete English and Chinese solutions are in the notes.'
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"impact and the optimal schedule of a large order", [37]),
            (r"market making with the microprice, inventory and queue position", [38]),
            (r"the order book of a decentralised exchange: the automated market maker", [39]),
            (r"simulators and learning agents in markets", [42]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty-seven measures the impact of large orders and schedules them. Part "
            "thirty-eight makes markets with the microprice, inventory and queue position. Part thirty-nine meets a book "
            "with no queues at all, the automated market maker. And Part forty-two puts learning agents into "
            "simulated markets like this one."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bouchaud, Bonart, Donier and Gould, \textit{Trades, Quotes and Prices} (2018)",
             r"Cartea, Jaimungal and Penalva, \textit{Algorithmic and High-Frequency Trading} (2015)",
             r"Abergel et al., \textit{Limit Order Books} (2016)",
             r"Gould et al., ``Limit order books'' (2013)"],
            [r"Lillo and Farmer (2004); Cont, Stoikov and Talreja (2010); Avellaneda, Reed and Stoikov (2011); Cont and "
             r"de Larrard (2013); Hardiman, Bercot and Bouchaud (2013); Cont, Kukanov and Stoikov (2014); Huang, Lehalle "
             r"and Rosenbaum (2015); Gould and Bonart (2016); Moallemi and Yuan (2017); Stoikov (2018); Xu, Gould and "
             r"Howison (2018)",
             r"Copeland and Galai (1983); Ntakaris et al.\ (2018); Sirignano and Cont (2019); Zhang, Zohren and Roberts "
             r"(2019); Byrd, Hybinette and Balch (2020); Vyetrenko et al.\ (2020); Coletta et al.\ (2021); Kolm, Turiel "
             r"and Westray (2023); Nagy et al.\ (2023); Prata et al.\ (2024). Data: Binance's public archive"])
        with self.voiceover(
            'The principal textbooks and papers behind this part are listed separately so each title remains readable. The displayed measurements come from the nine restored original computations on frozen public archives or their stipulated simulations. Chosen arithmetic examples are labeled as such. No new market trial, sealed strategy outcome or deployment approval is part of this visual review.'
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data", "research"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 37, Market Impact and Execution", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now read the book: its queues, its flow, its fair price where one exists, and the cost of "
            "waiting in line. <bookmark mark='a'/> Next, Part thirty-seven: market impact and execution. How much a "
            "large order moves the price, why the cost grows like a square root, and how to schedule a trade so that it "
            "costs the least."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
