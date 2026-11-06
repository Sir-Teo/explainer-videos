from __future__ import annotations

from explainer.quant import *  # noqa: F403
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
            "Chapter five, and the answer to the pause: knowing what happened. A language model trained on text up "
            "to some date has read the news that followed every event before it, so a backtest on that history can "
            "measure its memory rather than its judgement. Part twenty-eight measured this look-ahead bias, and "
            "built small models trained only on text up to a date. This chapter asks what changes when such models "
            "become traders."
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
                why(r"a market whose events never happened cannot be remembered: a clean test of reasoning, and of how "
                    r"agents interact"),
                why(r"but what an agent does in a synthetic market is evidence about that market: the artefacts, the "
                    r"counterfactual and adaptation all still apply")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why simulators matter for language models in particular. <bookmark mark='a'/> On real history, a model may "
            "remember what followed. <bookmark mark='b'/> In a simulator, with synthetic news and synthetic outcomes, "
            "there is nothing to remember: a clean test of reasoning, and of how agents interact. "
            "<bookmark mark='c'/> But it is evidence about the simulator. Chapter three's gap applies to them as to "
            "anything else."
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
            desk_question(r"what they cost", r"one model per date, each smaller or older than the frontier; the test "
                          r"measures an older model's skill, not today's", width=12.4, font_size=19),
            desk_question(r"or wait", r"test only after a model's release, on events it cannot have read about: honest, "
                          r"and slow", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "There are two clean ways out. <bookmark mark='a'/> Chronologically consistent models, trained only on text "
            "published before each date, so a backtest at that date cannot remember what came next. Part twenty-eight "
            "built small ones. <bookmark mark='b'/> They cost a model per date, each behind the frontier, so the test "
            "measures an older model's skill. <bookmark mark='c'/> Or wait: test only on events after a model's "
            "release. Honest, and slow."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def shared(self):
        cards = VGroup(
            desk_question(r"few providers", r"many firms calling the same few foundation models is a concentration "
                          r"the Financial Stability Board flagged in 2024: a common supplier and a common point of failure",
                          width=12.4, font_size=19),
            desk_question(r"similar answers", r"the same model asked similar questions about the same news gives "
                          r"similar answers: correlated trades with no communication at all", width=12.4, font_size=19),
            desk_question(r"which is Chapter 7", r"a crowd that shares a model is a crowd that herds, and Chapter 2 "
                          r"says where such crowds spend their time", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And a risk that is new in scale. <bookmark mark='a'/> Many firms calling the same few foundation models is "
            "a concentration the Financial Stability Board flagged in twenty twenty-four: one supplier, one point of "
            "failure. <bookmark mark='b'/> The same model asked similar questions about the same news gives similar "
            "answers: correlated trades without any communication. <bookmark mark='c'/> A crowd that shares a model is "
            "a crowd that herds, and Chapter two says where such crowds spend their time."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def market_effects(self):
        cards = VGroup(
            desk_question(r"faster prices", r"machines that read every headline at once should move prices to news "
                          r"faster: more efficient on average", width=12.4, font_size=19),
            desk_question(r"correlated reactions", r"the same few models reading the same headline react the same way, "
                          r"at the same moment: Chapter 7's common share, at news time", width=12.4, font_size=19),
            desk_question(r"a new target", r"text written for machine readers, true or false, becomes a way to move "
                          r"prices; the defence is provenance, not a better model", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What language-model traders could do to a market", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What language-model traders could do to a market, in principle. <bookmark mark='a'/> Prices should absorb "
            "news faster, since machines read every headline at once. <bookmark mark='b'/> But the same few models "
            "reading the same headline react the same way at the same moment: Chapter seven's common share, at news "
            "time. <bookmark mark='c'/> And text written for machine readers, true or false, becomes a way to move "
            "prices. The defence there is knowing where text came from, not a better model."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def position(self):
        cards = VGroup(
            desk_question(r"what the House did not do", r"it ran no language model as a trader in this part: running "
                          r"downloaded model code was outside what this build was permitted, and a test without a "
                          r"clean cut-off would measure memory", width=12.4, font_size=19),
            desk_question(r"what it did", r"it built the bench: a simulator, a registry, a cost model and baselines "
                          r"(Chapters 3, 4 and Part 26), into which any agent can be placed", width=12.4, font_size=19),
            desk_question(r"what is known", r"no published, registered, out-of-sample test of a language-model trader "
                          r"at scale, net of costs, as far as this series could verify", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where the House stands. <bookmark mark='a'/> It ran no language model as a trader in this part. Running "
            "downloaded model code was outside what this build was permitted, and a test without a clean cut-off would "
            "measure memory anyway. <bookmark mark='b'/> It built the bench instead: a simulator, a registry, a cost "
            "model and baselines, into which any agent can be placed. <bookmark mark='c'/> And what is known: as far as "
            "this series could verify, no published, registered, out-of-sample test of a language-model trader at "
            "scale, net of costs."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
        self.wait(0.5)
        self.clear_scene()
