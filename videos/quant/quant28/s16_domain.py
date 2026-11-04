from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, GOOD, HURDLE, PART, WORD, fit_right


class Domain(VoiceoverScene):
    def construct(self):
        self.card()
        self.bloomberg()
        self.tokens()
        self.general()
        self.desk()
        self.question()

    def card(self):
        c = chapter_card(15, r"Domain models and the text desk", r"Is a model trained on finance better at finance?",
                         part=PART)
        with self.voiceover("Chapter fifteen. If finance has its own vocabulary, as Loughran and McDonald showed, should "
                            "it have its own language model? And how does a trading firm actually use any of this?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bloomberg(self):
        card = firm_card(r"BloombergGPT (Wu et al., 2023)", r"Bloomberg trained a 50-billion-parameter language model on "
                         r"a corpus built from its own archives (FinPile: news, filings, press releases, web pages about "
                         r"finance, Bloomberg's own content) and general public data",
                         numbers=((r"363\text{bn}", r"tokens of financial text"), (r"345\text{bn}", r"tokens of general text"),
                                  (r"50\text{bn}", r"parameters"),
                                  (r"\checkmark", r"better than general models of similar size on financial tasks, without "
                                                  r"losing much on general ones")),
                         source=r"Wu et al., arXiv 2303.17564", kind=r"Firm file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "In March 2023 Bloomberg published BloombergGPT. <bookmark mark='a'/> Fifty billion parameters, trained on "
            "three hundred and sixty-three billion tokens of financial text from Bloomberg's own archives, news, "
            "filings and press releases among them, mixed with three hundred and forty-five billion tokens of general "
            "text. <bookmark mark='b'/> On financial benchmarks it beat general models of a similar size, without "
            "losing much on general tasks: the case for a domain model, made by the firm with the most financial text "
            "in the world."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def tokens(self):
        items = [(r"FinBERT (2023)", 4.9, WORD), (r"BloombergGPT: finance", 363.0, HURDLE),
                 (r"BloombergGPT: general", 345.0, GREY_B), (r"our minutes, 1996--2020", 1.3e-3 * 1.4, GOOD)]
        g = axes([-3.5, 3.5], [0, len(items)], x_length=8.0, y_length=3.6, xlabel=r"training tokens (billions, log scale)",
                 ylabel=r"", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[], xfmt=lambda v: f"10^{{{int(v)}}}",
                 font_size=15).move_to(RIGHT * 1.2 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for k, (nm, v, col) in enumerate(items):
            y = len(items) - k - 0.5
            b = Line(ax.c2p(-3.5, y), ax.c2p(np.log10(v), y), color=col, stroke_width=16)
            t = label(nm, font_size=17, color=col).next_to(ax.c2p(-3.5, y), LEFT, buff=0.2)
            bars.add(VGroup(b, t))
        foot = wrapped_label(r"FinBERT: 4.9 billion tokens of filings, earnings calls and analyst reports (Huang, Wang "
                             r"and Yang 2023). Our corpus: about 1.3 million words, roughly 1.8 million of our tokens. "
                             r"Frontier general models: trillions", 11.2, 17, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Put the sizes side by side, on a log scale. <bookmark mark='a'/> FinBERT, the finance-adapted BERT of "
            "Allen Huang, Hui Wang and Yi Yang, was trained on about five billion tokens of filings, calls and analyst "
            "reports. <bookmark mark='b'/> BloombergGPT, on seven hundred billion. The FOMC minutes we will train on "
            "ourselves in the next chapter are a million or two: a thousandth of FinBERT, a millionth of the frontier."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(bars[3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def general(self):
        card = firm_card(r"Li et al.\ (2023)", r"`Are ChatGPT and GPT-4 general-purpose solvers for financial text "
                         r"analytics?': the general models against domain-specific ones on standard financial tasks",
                         numbers=((r">", r"GPT-4 beats BloombergGPT on almost all the tasks tested, named-entity "
                                         r"recognition the exception"),
                                  (r"\checkmark", r"general models excel at numerical reasoning over financial text"),
                                  (r"<", r"they still trail fine-tuned specialists such as FinBERT on sentiment")),
                         source=r"EMNLP 2023, industry track; arXiv 2305.05862", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Within months the frontier moved. <bookmark mark='a'/> Testing ChatGPT and GPT-4 on the same kinds of "
            "financial tasks, Xianzhi Li and coauthors found GPT-4 ahead of BloombergGPT on almost all of them. "
            "<bookmark mark='b'/> General models were strongest at reasoning with the numbers in financial text, and "
            "still behind small fine-tuned specialists like FinBERT on sentiment. Scale and general reading beat a "
            "domain corpus; for narrow labelled tasks, a small specialist is still hard to beat."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        rows = VGroup()
        items = [(r"buy scored feeds", r"news analytics vendors (RavenPack and others) sell each story tagged with its "
                                       r"companies, relevance, novelty and a sentiment score, time-stamped to the millisecond"),
                 (r"build features", r"in-house teams turn filings, calls and news into features for the same models "
                                     r"as Part 27: a column among hundreds, rarely a strategy on its own"),
                 (r"read faster", r"language models summarise, extract and tag at the scale of every document, for "
                                  r"analysts and for the models downstream"),
                 (r"stamp the time", r"the hardest engineering is knowing exactly when each word became public, and "
                                     r"which model version read it")]
        for a, b in items:
            r_ = VGroup(label(a, font_size=24, color=WORD), wrapped_label(b, 8.6, 18, GREY_A)).arrange(RIGHT, buff=0.5,
                                                                                                       aligned_edge=UP)
            r_[0].set_width(min(r_[0].width, 3.0))
            rows.add(r_)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.1)
        head = label(r"the text desk, in practice", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "How do firms use text? <bookmark mark='a'/> Many buy it already scored: vendors such as RavenPack sell "
            "every story tagged with the companies it mentions, its relevance, its novelty and a sentiment score, "
            "time-stamped to the millisecond. <bookmark mark='b'/> Others build their own features from filings, calls "
            "and news, feeding the models of Part twenty-seven; text is usually one column among hundreds, rarely a "
            "strategy on its own. <bookmark mark='c'/> Language models now read everything for the analysts and "
            "tag it for the models. <bookmark mark='d'/> And the hardest engineering is unglamorous: knowing exactly "
            "when each word became public, and which version of which model read it."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a 50-billion-parameter domain model loses to a larger general model within months. When would "
                       r"you still train your own?")
        with self.voiceover(
            "Pause and predict. A fifty-billion-parameter domain model loses to a larger general model within months. "
            "When would you still train your own?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
