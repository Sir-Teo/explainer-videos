from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, GOOD, HURDLE, MODEL_A, MODEL_B, PART, WORD


class LookAhead(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeline_()
        self.two_biases()
        self.glasserman()
        self.sarkar()
        self.chrono()
        self.question()

    def card(self):
        c = chapter_card(11, r"Look-ahead bias", r"How do you backtest a model that has read the future?", part=PART)
        with self.voiceover("Chapter eleven. Part one's first rule was point in time: a number used at time t may only "
                            "depend on data from before t. How do you keep that rule with a model that has read the future?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def timeline_(self):
        line = NumberLine(x_range=[2015, 2025, 1], length=12.0, include_numbers=True, font_size=22,
                          decimal_number_config={"num_decimal_places": 0, "group_with_commas": False}).shift(DOWN * 0.4)
        test = Rectangle(width=line.n2p(2020)[0] - line.n2p(2016)[0], height=0.6, stroke_width=0, fill_color=WORD,
                         fill_opacity=0.35).move_to([(line.n2p(2016)[0] + line.n2p(2020)[0]) / 2, 0.25, 0])
        train = Rectangle(width=line.n2p(2023.2)[0] - line.n2p(2015)[0], height=0.3, stroke_width=0, fill_color=BAD,
                          fill_opacity=0.5).move_to([(line.n2p(2015)[0] + line.n2p(2023.2)[0]) / 2, 1.1, 0])
        t1 = label(r"the backtest: 2016--2020 news", font_size=22, color=WORD).next_to(test, DOWN, buff=1.0)
        t2 = label(r"what the model read: the internet up to 2023", font_size=22, color=BAD).next_to(train, UP, buff=0.2)
        warn = wrapped_label(r"every headline in the backtest was followed by events the model may have read about: "
                             r"its `prediction' can be memory", 10.6, 22, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Picture the usual experiment. <bookmark mark='a'/> The backtest asks a model about news from 2016 to "
            "2020. <bookmark mark='b'/> But the model was trained on text up to 2023, which includes what happened "
            "after every one of those headlines: the earnings, the lawsuits, the share price. <bookmark mark='c'/> "
            "Its forecast can be memory. And unlike a leaked price in a backtest, you cannot find the leak by reading "
            "the code: it is somewhere in a trillion words of training data."
        ) as vo:
            self.play(Create(line))
            vo.wait_until("a")
            self.play(FadeIn(test), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(train), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    def two_biases(self):
        rows = [cmath(r"\hat r^{\,\text{backtest}}", r"=", r"\underbrace{r^{\,\text{skill}}}_{\text{reading}} + "
                      r"\underbrace{b^{\,\text{look-ahead}}}_{\text{memory}} - \underbrace{d}_{\text{distraction}}", font_size=30,
                      colors={r"\hat r^{\,\text{backtest}}": HURDLE}),
                cmath(r"\text{anonymise}", r":", r"\text{``Apple beats estimates''} \to \text{``Company X beats estimates''}",
                      font_size=28),
                cmath(r"\Delta", r"=", r"\hat r(\text{named}) - \hat r(\text{anonymised}) \approx b - d", font_size=32,
                      colors={r"\Delta": HURDLE})]
        whys = [why(r"what a backtest of an LLM measures: real skill, plus what it remembers about the outcome, minus what "
                    r"it gets wrong because it knows too much about the firm in general"),
                why(r"strip the company's identity from the text"),
                why(r"the difference between named and anonymised backtests estimates look-ahead minus distraction")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Paul Glasserman and Caden Lin separated two things a backtest of an LLM picks up. <bookmark mark='a'/> "
            "Skill, from reading the headline; plus look-ahead, from remembering what followed; minus distraction, "
            "errors that come from knowing too much about the firm in general. <bookmark mark='b'/> Their tool: "
            "anonymise the headline, so Apple beats estimates becomes company X beats estimates. "
            "<bookmark mark='c'/> The gap between the named and anonymised backtests measures look-ahead minus "
            "distraction."
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

    def glasserman(self):
        card = firm_card(r"Glasserman and Lin (2023)", r"`Assessing look-ahead bias in stock return predictions generated "
                         r"by GPT sentiment analysis': GPT-3.5 scores headlines with and without the firm's identifiers",
                         numbers=((r"\text{in sample}", r"anonymised headlines did better: distraction outweighed look-ahead, "
                                                       r"most of all for large companies"),
                                  (r"\text{out of sample}", r"look-ahead is not a concern; distraction can remain"),
                                  (r"\Rightarrow", r"anonymise, for backtests and in production")),
                         source=r"arXiv 2309.17322", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Their result was a surprise. <bookmark mark='a'/> In sample, the anonymised headlines did better: the "
            "model's general knowledge of famous companies hurt more than its memory helped, especially for the "
            "largest firms. <bookmark mark='b'/> Out of sample, look-ahead cannot exist, but distraction can. So: "
            "anonymise, both to backtest honestly and to trade."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def sarkar(self):
        rows = [cmath(r"H_0", r":", r"\text{the model's forecast of an unpredictable event is no better than chance}",
                      font_size=28, colors={r"H_0": HURDLE}),
                cmath(r"\text{reject}", r"\Rightarrow", r"\text{the model knows the outcome: look-ahead}", font_size=30,
                      colors={r"\text{reject}": BAD}),
                cmath(r"\text{fail to reject}", r"\not\Rightarrow", r"\text{no look-ahead}", font_size=30)]
        whys = [why(r"Sarkar and Vafa (2024): pick events that nothing before the cut-off could predict, such as who won "
                    r"an election given a candidate's biography, or which risk factors an earnings call implies"),
                why(r"if the model does better than chance, it must have read the answer"),
                why(r"the test is one-sided: it catches some leakage, never proves its absence")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Suproteem Sarkar and Keyon Vafa turned this into a statistical test. <bookmark mark='a'/> Choose events "
            "that nothing before a date could have predicted: who won an election, given only a candidate's "
            "biography. <bookmark mark='b'/> If the model beats chance, it has read the answer. They found exactly "
            "that, in elections and in earnings calls. <bookmark mark='c'/> But the test is one-sided. It can catch a "
            "leak; it can never prove there is none."
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

    def chrono(self):
        years = list(range(1999, 2025, 3))
        bars = VGroup()
        for k, y in enumerate(years):
            r = Rectangle(width=0.5 + 0.45 * k, height=0.32, stroke_width=0, fill_color=MODEL_A, fill_opacity=0.8)
            r.move_to([-5.2 + r.width / 2, 2.2 - 0.45 * k, 0])
            t = label(rf"model dated {y}", font_size=15, color=GREY_A).next_to(r, RIGHT, buff=0.2)
            bars.add(VGroup(r, t))
        card = firm_card(r"He, Lv, Manela and Wu (2025)", r"`Chronologically consistent large language models': ChronoBERT "
                         r"and ChronoGPT, a series of models each trained only on text available up to its date; "
                         r"weights released",
                         numbers=((r"\checkmark", r"competitive on language benchmarks with larger open models"),
                                  (r"\approx", r"real-time Sharpe ratios comparable to state-of-the-art models: the "
                                               r"look-ahead in those was modest")),
                         source=r"arXiv 2502.21206", kind=r"Paper file", width=6.4, font_size=19).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The clean answer is to build the models so that they cannot cheat. <bookmark mark='a'/> Songrun He, Linying "
            "Lv, Asaf Manela and Jimmy Wu trained a series of language models, each on text available only up to its "
            "own date: one model for one date, another for a later date, and so on. <bookmark mark='b'/> For any "
            "backtest date, use the "
            "model of that date. Their models compete with larger open models on standard benchmarks, and their "
            "real-time trading results come close to the leaky state of the art, which suggests the look-ahead in the "
            "famous results was modest. We can run the same experiment ourselves, in miniature."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(card))
        self.add(note(r"schematic: a model for each date, trained only on text before it", font_size=15,
                      color=GREY_B).to_edge(DOWN, buff=0.3))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a model anonymises `Apple' to `Company X' but keeps `the iPhone maker'. What has it fixed, and "
                       r"what not?")
        with self.voiceover(
            "Pause and predict. A backtest anonymises Apple to company X but keeps the phrase the iPhone maker. What "
            "has it fixed, and what not?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
