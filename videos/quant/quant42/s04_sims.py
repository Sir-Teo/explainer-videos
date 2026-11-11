from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, load)


class Sims(VoiceoverScene):
    def construct(self):
        self.card()
        self.abides()
        self.realism()
        self.calibrate()
        self.gap()
        self.lucas()
        self.env()
        self.leaves_out()
        self.question()

    def card(self):
        c = chapter_card(3, r"Simulators", r"When does a strategy that works in a simulator work in a market?", part=PART)
        with self.voiceover(
            "Chapter three, and the answer to the pause: not necessarily, and often not. Matching the stylised facts "
            "says the simulator reproduces how prices move when nobody new arrives. A strategy needs something else: "
            "how the market responds to its own orders, and how the other traders adapt to it. Neither is in the "
            "historical data the simulator was fitted to."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def abides(self):
        rows = [cmath(r"\text{exchange}", r":", r"\text{a limit order book, matching by price and time}", font_size=36,
                      colors={r"\text{exchange}": SIM_C}),
                cmath(r"\text{agents}", r":", r"\text{noise, value, momentum, market makers, the strategy}", font_size=36,
                      colors={r"\text{agents}": LEARN_C}),
                cmath(r"\text{messages}", r":", r"\text{orders and fills, with latency, in event time}", font_size=36),
                cmath(r"\text{output}", r":", r"\text{a tape, and every agent's P\&L}", font_size=36)]
        whys = [why(r"ABIDES (Byrd, Hybinette and Balch 2020): an open-source discrete-event market simulator"),
                why(r"a population of background traders, each a simple rule, plus the agent under test"),
                why(r"each message travels with a delay, so speed matters as it does in Part 38"),
                why('a synthetic tape; comparisons with and without the strategy give counterfactuals conditional on the model')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What a modern market simulator is, taking ABIDES as the example. <bookmark mark='a'/> An exchange with a limit order book. <bookmark mark='b'/> Background traders and the strategy being tested. <bookmark mark='c'/> Orders and fills travel as messages with latency. <bookmark mark='d'/> It produces a tape and agent profits. Comparing runs with and without a strategy gives a counterfactual within the specified model. It does not by itself identify the strategy's causal effect in a real exchange."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def realism(self):
        cards = VGroup(
            desk_question(r"the stylised facts", r"fat tails, no linear predictability, clustered volatility, the shape "
                          r"of the spread and the depth: Chapter 1's checklist, at every horizon", width=12.4,
                          font_size=19),
            desk_question(r"the responses", r"the price impact of a metaorder (Part 37's square root) and how it "
                          r"decays: what a strategy actually experiences", width=12.4, font_size=19),
            desk_question(r"Vyetrenko et al. (2020)", r"proposed both kinds as realism metrics for order-book "
                          r"simulators, and found that matching the first does not guarantee the second", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How to judge a simulator. <bookmark mark='a'/> First, stylised facts: tails, clustering, spreads and depth across relevant horizons. <bookmark mark='b'/> Second, responses to interventions: order impact and its decay, including the approximate square-root regimes discussed in Part thirty-seven. They are empirical benchmarks, not universal laws. <bookmark mark='c'/> Vyetrenko and coauthors proposed both kinds of realism metrics. Matching unconditional statistics does not ensure realistic responses to a new strategy."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def calibrate(self):
        rows = [cmath(r"\hat\theta", r"=", r"\arg\min_\theta\ \bigl(m(\theta) - \hat m\bigr)^\top W \bigl(m(\theta) - \hat m\bigr)",
                      font_size=36, colors={r"\hat\theta": SIM_C}),
                cmath(r"m(\theta)", r":", r"\text{moments of simulated data}", font_size=38),
                cmath(r"\text{or}", r":", r"\text{learn the simulator: Part 36's queue model, generative books}", font_size=34)]
        whys = [why(r"the method of simulated moments: choose parameters so the simulator's statistics match the data's"),
                why(r"kurtosis, autocorrelations of $|r|$, spread, depth, impact: each a moment, each with a weight"),
                why('event-rate and generative models can fit book dynamics; responses outside observed policies require separate validation')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Fitting one to data. <bookmark mark='a'/> Simulated moments choose parameters to match selected statistics. <bookmark mark='b'/> Weights determine which discrepancies matter; matching them does not identify every behavioural mechanism. <bookmark mark='c'/> Event models or generative networks can also learn order-book dynamics. Their counterfactual validity under unfamiliar policies needs separate evidence; neither a close fit nor a behavioural story guarantees it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def gap(self):
        cards = VGroup(
            desk_question(r"artefacts", r"a learner finds whatever pays in the simulator, including its bugs and its "
                          r"simplifications: a too-patient noise trader is free money", width=12.4, font_size=19),
            desk_question(r"the counterfactual", r"historical data show how the market moved without you; how it moves "
                          r"with you is not identified from them, only assumed", width=12.4, font_size=19),
            desk_question(r"adaptation", r"real competitors learn back: a strategy that pays changes the population "
                          r"that made it pay, which a fixed simulator never does", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Three sources of the gap between simulation and reality", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "So the gap between simulation and reality has three sources. <bookmark mark='a'/> Artefacts: a learner "
            "finds whatever pays in the simulator, including its simplifications. A noise trader that is too patient "
            "is free money. <bookmark mark='b'/> The counterfactual: history shows how the market moved without you, "
            "and how it would move with you is assumed, not measured. <bookmark mark='c'/> And adaptation: real "
            "competitors learn back, so a strategy that pays changes the population that made it pay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lucas(self):
        cards = VGroup(
            desk_question(r"the Lucas critique (1976)", r"relations estimated under one policy break when the policy "
                          r"changes, because people respond to it; a simulator fitted to the past is such a relation",
                          width=12.4, font_size=19),
            desk_question(r"structural agents", 'objectives allow behaviour to be recomputed under new rules, conditional on assumptions about beliefs, constraints and adaptation', width=12.4,
                          font_size=19),
            desk_question(r"central banks use them", r"for example, the Bank of England's agent model of corporate bond "
                          r"funds and dealers, used to study fire sales under stress (Braun-Munzinger, Liu and Turrell "
                          r"2018)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "This is an old problem in economics. <bookmark mark='a'/> Lucas argued that estimated relations can change when policy changes because people respond. <bookmark mark='b'/> Agents with objectives let a researcher recompute behaviour under new rules, but their objectives, beliefs and adaptation still need justification. They do not automatically solve the identification problem. <bookmark mark='c'/> A historical example is the Bank of England model of bond funds and dealers used to examine fire-sale mechanisms under stress."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def env(self):
        rows = [cmath(r"v_{t+1}", r"=", r"v_t \pm 1\ \text{tick, with probability } 0.15", font_size=38,
                      colors={r"v_{t+1}": REAL_C}),
                cmath(r"\text{informed}", r":", r"\text{buy if } v > \text{ask},\ \text{sell if } v < \text{bid}", font_size=36,
                      colors={r"\text{informed}": BAD}),
                cmath(r"\text{noise}", r":", r"\text{trade with probability } \lambda e^{-k\,d}", font_size=38,
                      colors={r"\text{noise}": COMP_C}),
                cmath(r"\text{maker}", r":", r"\text{mid} \pm h - s\cdot\text{sign}(\text{inventory}),\ \text{mid moves with flow}",
                      font_size=32, colors={r"\text{maker}": LEARN_C})]
        whys = [why(r"the value moves a tick at a time; only the informed see it"),
                why('an informed trader observes current latent value and trades only at an immediately favourable quote'),
                why(r"noise traders trade less the further the quote is from the mid $d$: Part 38's fill law"),
                why(r"the maker chooses a half-spread $h$ and a skew $s$; reward: spread earned, inventory marked to "
                    r"$v$, less an inventory penalty")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The dealer simulator used here is deliberately small. <bookmark mark='a'/> A latent value moves by a tick; informed traders observe its current value, not its next innovation. <bookmark mark='b'/> They buy below that value or sell above it. <bookmark mark='c'/> Noise participation falls exponentially with quote distance. <bookmark mark='d'/> The maker chooses width and inventory skew. Its score is latent-value marked profit and loss less an inventory penalty, rather than cash profit alone. The value innovation occurs after the trading decision."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def leaves_out(self):
        cards = VGroup(
            desk_question(r"no order book", r"one maker, one quote on each side, no queue: Part 36's priorities and "
                          r"Part 38's speed race are absent", width=12.4, font_size=19),
            desk_question(r"fixed traders", r"the noise and informed traders never learn; a real informed trader "
                          r"would study the maker as the maker studies it", width=12.4, font_size=19),
            desk_question(r"why keep it this small", 'small enough to audit; results can depend on partial observation, learning choices and simulator assumptions', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this simulator leaves out. <bookmark mark='a'/> There is one maker, no order book, queue or speed race. <bookmark mark='b'/> The other traders do not learn. <bookmark mark='c'/> The maker observes only inventory and last trade, so different hidden value gaps share an observation. Failures can reflect this partial observation, the learning method, or model assumptions. A small simulator makes these mechanisms easier to audit; it does not make every failure the learner's fault."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a market maker learns its quotes by trial and error where 5\% of traders are informed, and is "
                       r"deployed where 30\% are. Does it lose money? Does it do worse than one trained there?")
        with self.voiceover(
            "Pause and predict. A market maker learns its quotes by trial and error in a market where five percent of "
            "traders are informed. It is then deployed where thirty percent are. Does it lose money? And does it do "
            "worse than one trained in the harder market?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
