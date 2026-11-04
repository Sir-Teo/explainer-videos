from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, PART, WORD


class LLMs(VoiceoverScene):
    def construct(self):
        self.card()
        self.prompt()
        self.lopez()
        self.embeddings()
        self.statements()
        self.caveats()
        self.question()

    def card(self):
        c = chapter_card(10, r"LLMs read the news", r"What changes when the reader has read most of the internet?",
                         part=PART)
        with self.voiceover("Chapter ten. Every method so far learned its words from finance alone. Large language "
                            "models arrive having read most of the public internet. What changes when that is the reader?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def prompt(self):
        lines = [r"\textbf{Prompt.} Forget all your previous instructions. Pretend you are a financial expert. You are "
                 r"a financial expert with stock recommendation experience. Answer ``YES'' if good news, ``NO'' if bad "
                 r"news, or ``UNKNOWN'' if uncertain in the first line. Then elaborate with one short and concise "
                 r"sentence on the next line. Is this headline good or bad for the stock price of \emph{company name} in "
                 r"the short term?",
                 r"\textbf{Headline.} \emph{(one news headline about the company)}"]
        box = VGroup(*[wrapped_label(l_, 10.6, 21, GREY_A) for l_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        frame = SurroundingRectangle(box, buff=0.3, color=WORD, corner_radius=0.1)
        g = VGroup(frame, box).move_to(UP * 0.3)
        src = note(r"the prompt of Lopez-Lira and Tang (2023), as published", font_size=16, color=GREY_B).next_to(g, DOWN, buff=0.3)
        score = label(r"YES $\to +1$,\quad UNKNOWN $\to 0$,\quad NO $\to -1$: averaged by firm and day", font_size=24,
                      color=HURDLE).next_to(src, DOWN, buff=0.4)
        with self.voiceover(
            "Here is how the most cited paper did it. <bookmark mark='a'/> Pretend you are a financial expert with stock "
            "recommendation experience. Is this "
            "headline good or bad for the company's stock price in the short term? Answer yes, no or unknown, then one "
            "sentence of reasoning. <bookmark mark='b'/> Yes becomes plus one, no becomes minus one, and the scores "
            "are averaged by company and day. No training, no word lists, no labels: the model's general reading does "
            "the work."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(score))
        self.wait(0.4)
        self.clear_scene()

    def lopez(self):
        card = firm_card(r"Lopez-Lira and Tang (2023, revised)", r"`Can ChatGPT forecast stock price movements?': "
                         r"134{,}129 headlines about 4{,}106 U.S. stocks on the NYSE, NASDAQ and AMEX, October 2021 to "
                         r"December 2023, all after the model's training data ends (September 2021); GPT-4's answer "
                         r"against the next day's return",
                         numbers=((r"+", r"the scores predict next-day returns; long-short portfolios earn significant returns"),
                                  (r">", r"they outperform traditional sentiment methods"),
                                  (r"\times", r"GPT-1, GPT-2 and BERT show little forecasting ability; their strategies' "
                                              r"Sharpe ratios are all negative")),
                         source=r"arXiv 2304.07619 (first version April 2023, with ChatGPT)", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Alejandro Lopez-Lira and Yuehua Tang ran this on a hundred and thirty-four thousand headlines, all "
            "published after the model's training data ended. <bookmark mark='a'/> The scores predicted the next day's "
            "returns, and beat the traditional sentiment methods. <bookmark mark='b'/> The striking part was the "
            "comparison: GPT-1, GPT-2 and BERT showed little ability, and every strategy built on them lost money. "
            "Predictability appeared only in the large models, which the authors called an emerging capacity."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def embeddings(self):
        rows = [cmath(r"h_i", r"=", r"\text{LLM}(\text{article}_i) \in \mathbb R^{d}", font_size=34, colors={r"h_i": WORD}),
                cmath(r"r_{i,t+1}", r"=", r"\beta^\top h_i + \varepsilon,\quad \beta \text{ by ridge}", font_size=34,
                      colors={r"r_{i,t+1}": HURDLE}),
                cmath(r"\text{news}", r"\to", r"\text{returns in 16 markets, 13 languages}", font_size=30)]
        whys = [why(r"Chen, Kelly and Xiu (2022), `Expected returns and large language models': skip the prompt, take "
                    r"the model's internal representation of the whole article"),
                why(r"and learn, from returns, which directions of that representation predict; Part 27's ridge on "
                    r"a new kind of feature"),
                why(r"across global equity markets, LLM representations beat word-based models, and returns respond "
                    r"to news slowly")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A second way skips the prompt. <bookmark mark='a'/> Yifei Chen, Bryan Kelly and Dacheng Xiu feed each "
            "article through a language model and keep its internal representation, a long vector. "
            "<bookmark mark='b'/> Then they learn from returns which directions of that vector predict, with the ridge "
            "regression of Part twenty-seven. <bookmark mark='c'/> Across sixteen equity markets and thirteen "
            "languages, the representations beat word-based models, and prices respond to news slowly enough to trade."
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

    def statements(self):
        card = firm_card(r"Kim, Muhn and Nikolaev (2024)", r"`Financial statement analysis with large language models': "
                         r"GPT-4 Turbo is given standardised, anonymised balance sheets and income statements, no names, "
                         r"no narrative, and asked whether earnings will rise or fall next year",
                         numbers=((r"52\%", r"accuracy with a simple prompt"),
                                  (r"60\%", r"with a chain-of-thought prompt that walks through ratios as an analyst would"),
                                  (r">", r"above analysts' consensus and comparable to specialised models")),
                         source=r"arXiv 2407.17866", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "A third uses no text at all. <bookmark mark='a'/> Alex Kim, Maximilian Muhn and Valeri Nikolaev gave GPT-4 "
            "anonymised financial statements, just the numbers, with no company names, and asked whether next year's "
            "earnings would rise or fall. <bookmark mark='b'/> With a simple prompt it was right fifty-two percent of "
            "the time; walked through the ratios the way an analyst is taught, sixty percent, above the analysts' "
            "consensus. The model is not reading sentiment here. It is doing the analysis."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def caveats(self):
        cards = VGroup(
            desk_question(r"what was the model trained on?", r"a model that has read the internet up to 2023 may have "
                          r"read what happened after a 2019 headline. Every result above is only as good as its separation "
                          r"of training and testing in time: the next chapter", width=12.4, font_size=19),
            desk_question(r"what does it cost?", r"a query per headline, per firm, per day; and a model that changes "
                          r"under you when the vendor updates it, which breaks reproducibility", width=12.4, font_size=19),
            desk_question(r"who else is doing it?", r"a signal from a public model read by everyone is priced quickly: "
                          r"Chapter 14's arithmetic of crowding", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three questions every one of these results must answer. <bookmark mark='a'/> What was the model trained "
            "on? A model that has read the internet through 2023 may already know what followed a 2019 headline. "
            "<bookmark mark='b'/> What does it cost, and will the same query give the same answer next year, after "
            "the vendor updates the model? <bookmark mark='c'/> And who else is asking it? A signal anyone can buy "
            "from the same public model is priced quickly."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"BERT could not predict returns from headlines; ChatGPT could. Name two explanations other than "
                       r"`larger models understand news better'.")
        with self.voiceover(
            "Pause and predict. BERT could not predict returns from headlines; ChatGPT could. Name two explanations "
            "other than larger models understanding news better."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
