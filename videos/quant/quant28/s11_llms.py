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
        self.more_papers()
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
        card = firm_card(r"Lopez-Lira and Tang, version 6 (October 2025)",
                         r"159{,}137 firm-headline-date observations; 4{,}123 firms; October 2021--May 2024. "
                         r"Authors use GPT-4-0314 with a declared September 2021 training cutoff.",
                         numbers=((r"90\%", r"approximately: portfolio-day success on the initial reaction, which the authors call non-tradable"),
                                  (r"58\%,55\%", r"reported hit rates for subsequent overnight and intraday drift; different outcomes"),
                                  (r"20\text{ bp}", r"round-trip cost makes their drift portfolios unprofitable")),
                         source=r"arXiv 2304.07619v6; front matter: 30 October 2025", kind=r"Paper file", width=10.6,
                         font_size=21).move_to(ORIGIN)
        with self.voiceover(
            "Version matters. This is Lopez-Lira and Tang's sixth version, dated October 2025, with 159,137 firm-headline-date observations on 4,123 firms. "
            "<bookmark mark='a'/> Their roughly ninety-percent portfolio-day success refers to the initial reaction, which they explicitly call non-tradable. It is not headline classification accuracy. "
            "<bookmark mark='b'/> Subsequent drift has reported hit rates of fifty-eight and fifty-five percent, and gross Sharpe ratios of two point nine seven and two point six three. Twenty basis points of round-trip costs erase profitability. The authors declare a September 2021 cutoff for the fixed GPT-4 version; a declared cutoff alone does not independently audit its entire corpus. These are reported results, not replicated here."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card, color=QC.FIRM, scale_factor=1.01))
            vo.wait_until("b")
            self.wait(0.1)
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
            "languages, the authors report gains over word-based models and delayed price responses. Trading interpretation still depends on publication clocks, sample design and costs; that study is not reproduced here."
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
        card = firm_card(r"Withdrawn working paper: 20 February 2025",
                           r"Kim, Muhn and Nikolaev, Financial Statement Analysis with Large Language Models. "
                           r"The authors' version-3 notice reports data and analysis inconsistencies found by a co-author attempting replication. "
                           r"The working paper was temporarily withdrawn while the findings were reviewed.",
                           source=r"arXiv 2407.17866v3; author withdrawal notice", kind=r"Correction", width=10.6, font_size=23).move_to(ORIGIN)
        with self.voiceover(
            "Financial-statement analysis is a useful proposed task, but one prominent citation needs correction. "
            "<bookmark mark='a'/> Kim, Muhn and Nikolaev's working paper was withdrawn in February 2025. Their notice says a co-author found inconsistencies in the data and analyses while attempting replication. "
            "<bookmark mark='b'/> We therefore withhold its earlier accuracy and profitability claims. A plausible prompt and an appealing headline result are insufficient evidence. The task still needs reproducible data, a frozen model version, a clear comparison and an independent evaluation."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card, color=QC.LOSS, scale_factor=1.01))
        self.clear_scene()


    def more_papers(self):
        cards = VGroup(
            desk_question(r"Araci (2019)", r"the first FinBERT: BERT further trained on financial news and fine-tuned on the Financial PhraseBank's labelled sentences", width=12.4, font_size=19),
            desk_question(r"Hansen and Kazinnik (2023), `Can ChatGPT decipher Fedspeak?'", r"GPT models classify the stance of FOMC sentences, hawkish or dovish, close to human experts, and explain their reasons", width=12.4, font_size=19),
            desk_question(r"Cao, Jiang, Wang and Yang (2024)", r"an AI analyst built from public data beats most human analysts' price targets; analysts working with the machine beat both", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three more strands. <bookmark mark='a'/> Dogu Araci's FinBERT of 2019, the first, trained on financial news. "
            "<bookmark mark='b'/> Anne Lundgaard Hansen and Sophia Kazinnik asked whether ChatGPT can decipher Fedspeak; "
            "the larger models label the committee's sentences as hawkish or dovish close to human experts. "
            "<bookmark mark='c'/> And Sean Cao, Wei Jiang, Junbo Wang and Baozhong Yang built an artificial analyst from "
            "public data that beat most human analysts, while analysts working with it beat both."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(('a', 'b', 'c')):
                vo.wait_until(mk)
                if k > 0:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
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
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k > 0:
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
