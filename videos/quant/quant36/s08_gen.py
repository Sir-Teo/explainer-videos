from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (BAD, GOOD, PART, SIM_C, fit_right, load)


class Gen(VoiceoverScene):
    def construct(self):
        q = load("qr")
        self.card()
        self.why_sim()
        self.literature()
        self.zero_intelligence()
        self.rates(q)
        self.path(q)
        self.scorecard(q)
        self.diagnosis(q)
        self.realism()
        self.question()

    def card(self):
        c = chapter_card(7, r"A book of our own", r"Can a model generate an order book that behaves like the real one?",
                         part=PART)
        with self.voiceover('Chapter seven. A forecast estimates a future statistic; a simulator must generate whole paths and respond to modeled actions. The previous cost calculation also showed that a direction score cannot certify profitable execution. We now examine a particular queue simulator and the behaviors it can and cannot reproduce under its assumptions.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_sim(self):
        cards = VGroup(
            desk_question(r"replay is not enough", 'a negligible-order replay can approximate queue fills and adverse selection; the historical market cannot react to the added order', width=12.4,
                          font_size=19),
            desk_question(r"what a simulator is for", r"testing execution and market-making algorithms, stress "
                          r"scenarios that never happened, and training reinforcement learners (Part 8) without "
                          r"trading real money", width=12.4, font_size=19),
            desk_question(r"the risk", r"an algorithm tuned on a simulator learns the simulator: any fact it gets wrong "
                          r"becomes a profit that does not exist", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why simulate, and what replay can do. <bookmark mark='a'/> Historical replay can approximate queueing and adverse selection for a negligible order, as our later exercise does. Its central limitation is that the historical market cannot react to the added order. <bookmark mark='b'/> A responsive simulator can study counterfactual actions and stresses under its own assumptions. <bookmark mark='c'/> A policy tuned to that simulator can exploit its errors. Validation must cover both ordinary stylised facts and the response to interventions; neither is guaranteed by a visually plausible price path."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def literature(self):
        cards = VGroup(
            desk_question(r"queue-reactive and Hawkes models", r"Huang, Lehalle and Rosenbaum (2015); Hawkes-driven "
                          r"books: rates estimated from data, interpretable, fast", width=12.4, font_size=18),
            desk_question(r"agent-based markets", r"ABIDES (Byrd, Hybinette and Balch, 2020): many simulated traders "
                          r"with strategies, meeting in a matching engine", width=12.4, font_size=18),
            desk_question(r"deep generative books", r"Coletta et al. (2021), a conditional GAN of order flow; Nagy et "
                          r"al. (2023), a token-by-token generator of every message, in the manner of a language model",
                          width=12.4, font_size=18),
            desk_question(r"realism metrics", r"Vyetrenko et al. (2020): score a simulator on a list of stylised facts "
                          r"of real books, not on its likelihood", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.2)
        with self.voiceover(
            "Four families. <bookmark mark='a'/> Statistical models, the queue-reactive model and Hawkes-driven books: "
            "rates read from data, interpretable and fast. <bookmark mark='b'/> Agent-based markets such as ABIDES, "
            "where simulated traders with strategies meet in a matching engine. <bookmark mark='c'/> Deep generative "
            "books: a conditional adversarial network of order flow, and Peer Nagy and colleagues' generator, which "
            "writes the message stream token by token, the way a language model writes text. <bookmark mark='d'/> And "
            "how to judge any of them: Svitlana Vyetrenko and colleagues proposed scoring a simulator on a list of the "
            "real book's stylised facts. We do that next."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def zero_intelligence(self):
        rows = [cmath(r"\text{orders}", r"\sim", r"\text{Poisson, at random prices}", font_size=38),
                cmath(r"\text{spread}", r"\sim", '\\frac{\\mu}{\\alpha}\\,f\\!\\left(\\frac{\\delta\\,\\sigma}{\\mu}\\right)',
                      font_size=36, colors={r"\text{spread}": SIM_C}),
                cmath(r"\text{lesson}", r":", '\\text{mechanics constrain spreads}', font_size=30)]
        whys = [why(r"Smith, Farmer, Gillemot and Krishnamurthy (2003): limit orders, market orders and cancellations "
                    r"arrive at random, with no intelligence at all"),
                why('$\\mu$: volume/time; $\\alpha$: volume/(price time); $\\delta$: inverse time; $\\sigma$: order size. Thus $\\mu/\\alpha$ is a price and $\\delta\\sigma/\\mu$ is dimensionless'),
                why('Farmer, Patelli and Zovko (2005) report cross-stock spread evidence for their model; dimensional analysis alone does not fix the function or identify residual causes')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A specified zero-intelligence baseline. <bookmark mark='a'/> Orders arrive and cancel under exogenous Poisson assumptions, without strategic decision rules. Define mu as market-order volume per time, alpha as limit-order volume per price per time, delta as cancellation rate per resting order and sigma as individual order size. <bookmark mark='b'/> Mu over alpha has price units; delta times sigma over mu is dimensionless. The continuum model therefore permits the displayed spread scale times an unspecified dimensionless function, with convention-dependent constants absorbed into it. Dimensional analysis does not determine that function or cover arbitrary finite-tick and placement rules. <bookmark mark='c'/> Farmer, Patelli and Zovko report supporting cross-stock spread evidence in their setting. Residual discrepancies do not separately identify strategy or information."
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

    def rates(self, q):
        pu = 10 * np.asarray(q["p_up"], float)
        pd = 10 * np.asarray(q["p_dn"], float)
        n = 16
        xs = np.arange(1, n)
        top = float(np.ceil(max(pu[1:n].max(), pd[1:n].max()) * 2) / 2)
        g = axes([0, n], [0, top], x_length=6.4, y_length=4.4, xlabel=rf"best queue size, units of {q['unit']:.1f} BTC",
                 ylabel=r"events per second", xticks=[0, 5, 10, 15], yticks=[0, top / 2, top], yfmt=lambda v: f"{v:.1f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        cu = curve(ax, xs, pu[1:n], GOOD, stroke_width=3)
        cd = curve(ax, xs, pd[1:n], BAD, stroke_width=3)
        leg = legend([(GOOD, 'net queue-size growth'), (BAD, 'net queue-size shrinkage')],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        rf = np.asarray(q["refill"], float)
        k_med = int(np.searchsorted(np.cumsum(rf), 0.5)) + 1
        p1 = rf[0]
        with self.voiceover(
            f"""Our simplified queue model uses a chosen size unit of {q['unit']:.1f} bitcoin: one quarter of the median displayed size, not an estimate of typical individual order size. <bookmark mark='a'/> At each discretized queue size, count net upward and downward size changes per grid step. The plotted rates are their nominal per-second conversion. <bookmark mark='b'/> This discards message type, multi-unit jumps and within-step activity. The empirical refill distribution puts {100 * p1:.0f} percent at one unit, with median {k_med}. Matching these summaries does not reproduce the full original message process."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cu))
            vo.wait_until("b")
            self.play(Create(cd))
        self.wait(0.4)
        self.clear_scene()

    def path(self, q):
        m = np.asarray(q["sim_mid"], float) / 2 * 0.1
        m = m - m[0]
        t = np.arange(len(m)) / 60
        lo, hi = float(np.floor(m.min())), float(np.ceil(m.max()))
        if hi - lo < 1:
            hi = lo + 1
        g = axes([0, t[-1]], [lo, hi], x_length=9.6, y_length=4.2, xlabel=r"minutes", ylabel=r"simulated mid, \$",
                 xticks=[0, 20, 40, 60], yticks=[lo, hi], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(DOWN * 0.2)
        c_ = curve(g.ax, t, m, SIM_C, stroke_width=2)
        with self.voiceover(
            "An hour of the simulated mid, from the fitted rates alone. <bookmark mark='a'/> It wanders like a price, "
            f"one half-tick at a time, ending {abs(m[-1]):.2f} dollars from where it began. It looks plausible. The "
            "question is whether it is plausible in the ways that matter."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c_), run_time=4)
        self.wait(0.4)
        self.clear_scene()

    def scorecard(self, q):
        tr, te, mo = q["data_train"], q["data_test"], q["model"]
        facts = [("moves_per_min", r"mid moves per minute", "{:.1f}"), ("gap_cv", r"burstiness of moves (Poisson = 1)",
                                                                       "{:.2f}"),
                 ("move_ac1", r"same-direction pairs (sign autocorrelation)", "{:.2f}"),
                 ("kurt_10s", r"fat tails (kurtosis of 10-s changes)", "{:.1f}"),
                 ("queue_med", r"median best queue, units", "{:.1f}")]
        hx = [-3.6, 1.2, 3.2, 5.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"stylised fact", r"17 May", r"20 May",
                                                                         r"simulator")])
        tab = VGroup(head)
        for k, name, fmt in facts:
            tab.add(VGroup(label(name, font_size=17), MathTex(fmt.format(tr[k]), font_size=24),
                           MathTex(fmt.format(te[k]), font_size=24), MathTex(fmt.format(mo[k]), font_size=24,
                                                                             color=SIM_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                if i == 0:
                    cell.move_to([hx[0], 2.3 - 0.75 * j, 0], aligned_edge=LEFT).shift(LEFT * 2.0)
                else:
                    cell.move_to([hx[i], 2.3 - 0.75 * j, 0])
        foot = wrapped_label(r"fitted on 17 May; 20 May is a weekend day the simulator never saw", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"""A scorecard of particular summary statistics. <bookmark mark='a'/> The simulated median queue is about {mo['queue_med']:.0f} chosen units. <bookmark mark='b'/> The model has {mo['moves_per_min']:.1f} mid moves per minute against {tr['moves_per_min']:.0f} in the training day. Inter-move waiting-time coefficient of variation is {mo['gap_cv']:.1f} against {tr['gap_cv']:.1f}; a Poisson event clock has coefficient one, but this ratio is not a general burstiness multiplier. Move-sign lag-one correlation has magnitude {abs(mo['move_ac1']):.2f}, versus signed data value {tr['move_ac1']:.2f}. Ten-second kurtosis is {mo['kurt_10s']:.1f} versus {tr['kurt_10s']:.0f}. These discrepancies reject several practical uses of this particular baseline, without proving that every Markov model has thin tails."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[5]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:5]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def diagnosis(self, q):
        rows = [cmath('\\text{this queue-only baseline}', r"\Rightarrow", '\\text{omitted history and intensity state}', font_size=36,
                      colors={'\\text{omitted history and intensity state}': BAD}),
                cmath(r"\pm 1\ \text{unit per step}", r"\Rightarrow", r"\text{no sweeps}", font_size=36,
                      colors={r"\text{no sweeps}": BAD}),
                cmath(r"\text{fix}", r":", r"\text{Hawkes rates, marks, the spread as a state}", font_size=32,
                      colors={r"\text{fix}": GOOD})]
        whys = [why('this implementation omits recent-flow and intensity states; Markov processes can still have serial dependence, clustering and heavy tails'),
                why(r"in the data one market order can take a whole queue in a single step; here a queue empties one "
                    r"unit at a time, so the price moves too rarely"),
                why(r"let rates depend on recent events, let an event remove many units, and model the spread opening "
                    r"and closing: each fix is a line on the scorecard")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Diagnose this implementation, not all Markov models. <bookmark mark='a'/> Current full queues determine its transition probabilities. A Markov state can still produce serial dependence; including exponential-Hawkes intensity would also give finite-dimensional self-excitation. Our state omits those intensity and history variables. <bookmark mark='b'/> One-unit steps and a chosen refill rule restrict depletion and price dynamics relative to multi-unit real events. <bookmark mark='c'/> History variables, jump sizes and spread states are candidate model extensions, whose benefits require new validation. None is fitted here, and an enlarged state is not automatically sufficient."
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

    def realism(self):
        cards = VGroup(
            desk_question(r"match the facts, not just the likelihood", r"a model can fit each step well and still miss "
                          r"the clustering of a day", width=12.4, font_size=19),
            desk_question(r"react to the agent", r"the test that matters for execution: when an algorithm trades, does "
                          r"the simulated price respond as much as a real one would (Part 37's impact)?", width=12.4,
                          font_size=19),
            desk_question(r"test out of sample", r"a different day, a different regime: the weekend's slower book is "
                          r"in the scorecard for that reason", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three rules for anyone who builds a market simulator. <bookmark mark='a'/> Match the facts, not only the "
            "likelihood: a model can fit each step and still miss the shape of a day. <bookmark mark='b'/> Check that "
            "it reacts: when an algorithm trades in it, the simulated price must respond as a real one would, which is "
            "Part thirty-seven's subject. <bookmark mark='c'/> And test out of sample, on another day and another "
            "regime."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('Does a Markov state stay Markov after bucketing?', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('(q^b,q^a)=(1,1)\\ \\text{or}\\ (10,10),\\quad I=\\tfrac12,\\quad\\Pr(\\text{remove one bid unit})=0.2', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Otherwise nothing happens. Bid depletion moves the mid down half a tick; the large queue cannot deplete in one step.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Compare next-step move probabilities from these identical imbalance buckets. Is I alone sufficient?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('Consider a full-state Markov chain with queue sizes one and one, or ten and ten. Both have imbalance one half. The next step removes one bid unit with probability point two and otherwise does nothing. Bid depletion moves the mid down half a tick. Compare the next-step price-move probability from the two states. Explain why projection onto imbalance alone need not remain Markov.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
