from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, load)


class LLM(VoiceoverScene):
    def construct(self):
        self.card()
        self.what()
        self.sim_bench()
        self.honest()
        self.cutoff()
        self.shared()
        self.market_effects()
        self.position()
        self.question()

    def card(self):
        c = chapter_card(5, r"Language models as traders", r"How would you know whether one can trade?", part=PART)
        with self.voiceover(
            'Chapter five. A language model may have encountered later news about historical test events during training. A training cutoff does not prove it read every event, but contamination can make apparent trading skill difficult to distinguish from recall. Part twenty-eight examined this timing problem with small chronologically consistent models. Here we discuss evaluation requirements; no language-model trader is executed in this part.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def what(self):
        cards = VGroup(
            desk_question(r"readers", r"models that score headlines or filings for a separate trading rule: Part 28's "
                          r"tone and sentiment, the commonest use", width=12.4, font_size=19),
            desk_question(r"planners", r"agents that read, reason in text and output an order, often several in a "
                          r"pipeline of analyst, trader and risk manager, as research prototypes describe them",
                          width=12.4, font_size=19),
            desk_question(r"populations", r"many such agents in one simulated market, to see what prices they make "
                          r"together, as recent working papers report", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three ways they are used, as the research describes them. <bookmark mark='a'/> As readers: a model scores "
            "news for a separate trading rule, Part twenty-eight's tone. <bookmark mark='b'/> As planners: an agent "
            "reads, reasons in text and outputs an order, sometimes as a pipeline of analyst, trader and risk manager. "
            "<bookmark mark='c'/> And as populations: many agents in one simulated market, to see what prices they make "
            "together."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def sim_bench(self):
        rows = [cmath(r"\text{history}", r":", r"\text{the model may remember what followed}", font_size=38,
                      colors={r"\text{history}": BAD}),
                cmath(r"\text{simulator}", r":", r"\text{synthetic news, synthetic outcomes}", font_size=38,
                      colors={r"\text{simulator}": SIM_C}),
                cmath(r"\text{but}", r":", r"\text{Chapter 3's gap, unchanged}", font_size=38, colors={r"\text{but}": HURDLE})]
        whys = [why(r"a backtest on dates inside the training data mixes skill with recall"),
                why('novel events reduce direct outcome recall; template contamination and simulator shortcuts can remain'),
                why(r"but what an agent does in a synthetic market is evidence about that market: the artefacts, the "
                    r"counterfactual and adaptation all still apply")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why simulators can help test language models. <bookmark mark='a'/> Historical outcomes may overlap training material. <bookmark mark='b'/> Newly generated events reduce direct outcome recall, but familiar templates, benchmark leakage and exploitable simulator rules can remain. Synthetic novelty alone is not a clean test of general reasoning. <bookmark mark='c'/> Results are evidence about that simulated environment. Transfer to real execution and unfamiliar market conditions requires separate validation."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def honest(self):
        rows = [cmath(r"\text{1. a cut-off}", r":", r"\text{training data that end before the test begins}", font_size=36,
                      colors={r"\text{1. a cut-off}": COMP_C}),
                cmath(r"\text{2. a record}", r":", r"\text{prompts, versions and every run, registered first}", font_size=36,
                      colors={r"\text{2. a record}": HURDLE}),
                cmath(r"\text{3. costs}", r":", r"\text{the House's cost model and Part 26's deflation}", font_size=36,
                      colors={r"\text{3. costs}": BAD}),
                cmath(r"\text{4. a baseline}", r":", r"\text{the simplest rule using the same inputs}", font_size=36)]
        whys = [why(r"Part 28's chronologically consistent models, or a test window after the model's release"),
                why(r"a model's output varies with the wording and the version: each try is a trial on the counter"),
                why(r"turnover costs and the number of configurations tried, as for any strategy"),
                why(r"a tone dictionary or a linear model on the same text: what the language model adds is the difference")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What an honest test would need. <bookmark mark='a'/> Training data that end before the test window "
            "begins. <bookmark mark='b'/> A registered record of prompts, versions and every run, because each "
            "rewording is another trial on the counter. <bookmark mark='c'/> Costs, and Part twenty-six's deflation "
            "for the number tried. <bookmark mark='d'/> And a baseline: the simplest rule using the same text. What the "
            "language model adds is the difference."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def cutoff(self):
        cards = VGroup(
            desk_question(r"chronologically consistent models", r"language models trained only on text published before "
                          r"each date, so a backtest at that date cannot remember the future: Part 28 built small ones",
                          width=12.4, font_size=19),
            desk_question(r"what they cost", 'one model frozen before the test window, or documented rolling vintages; older vintages measure their own capabilities', width=12.4, font_size=19),
            desk_question(r"or wait", r"test only after a model's release, on events it cannot have read about: honest, "
                          r"and slow", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two ways to improve timing discipline. <bookmark mark='a'/> Use a frozen model whose training information predates the whole test window, or use documented rolling vintages. A new model for every date is not required. <bookmark mark='b'/> Historical vintages test those older models and their recorded information sets. <bookmark mark='c'/> A prospective test after release also needs frozen prompts, data rules, model versions and a record of all trials. Release timing alone does not prevent adaptation to test outcomes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def shared(self):
        cards = VGroup(
            desk_question(r"few providers", r"many firms calling the same few foundation models is a concentration "
                          r"the Financial Stability Board flagged in 2024: a common supplier and a common point of failure",
                          width=12.4, font_size=19),
            desk_question(r"similar answers", 'shared models and inputs can correlate decisions; prompts, constraints and execution can preserve differences', width=12.4, font_size=19),
            desk_question(r"which is Chapter 7", 'Chapter 7 isolates a common-signal mechanism; sharing a model alone does not imply the Chapter 2 imitation law', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "A potential concentration risk. <bookmark mark='a'/> The Financial Stability Board's twenty twenty-four report discussed reliance on common AI providers. <bookmark mark='b'/> Shared models and inputs can correlate decisions, but prompts, constraints and execution can also make actions differ. <bookmark mark='c'/> Chapter seven isolates a common-signal mechanism. Sharing a model alone does not imply herding or the stationary distribution of Chapter two's particular imitation chain."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def market_effects(self):
        cards = VGroup(
            desk_question(r"faster prices", 'faster text processing may accelerate information incorporation; accuracy and execution still matter', width=12.4, font_size=19),
            desk_question(r"correlated reactions", 'shared inputs and rules can correlate order flow; heterogeneous constraints can reduce alignment', width=12.4, font_size=19),
            desk_question(r"a new target", 'misleading text creates manipulation risk; provenance, validation and trading controls are complementary safeguards', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What language-model traders could do to a market", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Possible market effects depend on deployment. <bookmark mark='a'/> Faster text processing can speed some information into prices, but errors and execution frictions remain. <bookmark mark='b'/> Similar inputs and decision rules can create correlated order flow; this is a risk mechanism, not a measured universal outcome. <bookmark mark='c'/> Misleading or malicious text can affect machine readers. Provenance, validation, access controls and risk limits all matter; no single defence eliminates that risk."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def position(self):
        cards = VGroup(
            desk_question(r"what the House did not do", 'no language-model trader is executed here; this part provides no direct evidence of its profitability', width=12.4, font_size=19),
            desk_question(r"what it did", 'the small dealer simulator and fixed baselines illustrate evaluation problems; a real trial needs prospective information and cost controls', width=12.4, font_size=19),
            desk_question(r"what is known", 'no claim about the current field-wide profitability of language-model traders follows from these simulations', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part establishes. <bookmark mark='a'/> It runs no language model as a trader, so it supplies no direct performance evidence about one. <bookmark mark='b'/> The small dealer simulator and fixed-rule baselines illustrate some evaluation problems. A real trial would additionally need a frozen information set, costs and complete prospective accounting of configurations. <bookmark mark='c'/> Results here cannot establish the current absence or presence of profitable language-model trading at scale. That is a separate empirical question."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two pricing algorithms learn by trial and error, never communicate, and set prices against each "
                       r"other again and again. Do they end up at competitive prices?")
        with self.voiceover(
            "Pause and predict. Two pricing algorithms learn by trial and error. They never communicate, and they set "
            "prices against each other again and again. Do they end up at competitive prices?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
