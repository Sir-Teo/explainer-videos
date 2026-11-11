from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, DOVE, GOOD, HAWK, HURDLE, PART, WORD, era_strip, load


def _date(d: int) -> str:
    import datetime as _dt
    return _dt.date(d // 10000, (d // 100) % 100, d % 100).strftime("%-d %B %Y")


def _tex(s: str) -> str:
    for a, b in (("\\", ""), ("%", r"\%"), ("$", r"\$"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("{", ""), ("}", "")):
        s = s.replace(a, b)
    return s


class Hook(VoiceoverScene):
    def construct(self):
        h = load("hook")
        self.title_card()
        self.diff(h)
        self.moves(h)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Text, LLMs and Alternative Data")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-eight. Text, language models and alternative data: how to turn words, and other things that "
            "are not prices, into numbers a model can use; what they are worth; and how easily they fool you."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def diff(self, h):
        old = h["prev_text"].split("\n")[0]
        new = h["text"].split("\n")[0]
        outlook = h["text"].split("\n")[1].split(". ")[0] + "."
        cards = VGroup(
            desk_question(r"Previous statement: 11 December 2007", _tex(old), width=12.0, font_size=25),
            desk_question(r"Unscheduled statement: 22 January 2008", _tex(new), width=12.0, font_size=25),
            desk_question(r"New outlook language (selected sentence)", _tex(outlook), width=12.0, font_size=24),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        if cards.height > 6.7:
            cards.scale_to_fit_height(6.7)
        foot = note(r"Selected policy and outlook excerpts; surrounding text omitted", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"On the {_date(h['date'])}, eight days before a scheduled meeting, the Federal Open Market Committee "
            "issued an unscheduled statement. <bookmark mark='a'/> Compare selected policy sentences with the statement "
            "before it. <bookmark mark='b'/> A cut of three quarters of a point instead of a quarter, and a lower target. "
            "The new outlook sentence points to weakening conditions and increasing downside risks to growth. "
            "Later paragraphs also discuss a deepening housing contraction; these excerpts do not show the full documents."
        ) as vo:
            self.play(FadeIn(cards[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()


    def moves(self, h):
        top = h["top"][:6]
        g = axes([-0.5, len(top) - 0.5], [-30, 30], x_length=8.4, y_length=4.2, xlabel=r"",
                 ylabel=r"prior-close to statement-day-close yield change, bp", xticks=[], yticks=[-30, -15, 0, 15, 30],
                 font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        bars, tags = VGroup(), VGroup()
        for k, (d, dy) in enumerate(top):
            b = Rectangle(width=0.7, height=abs(ax.c2p(0, dy)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                          fill_color=HAWK if dy > 0 else DOVE, fill_opacity=0.85)
            b.move_to([ax.c2p(k, 0)[0], (ax.c2p(0, 0)[1] + ax.c2p(0, dy)[1]) / 2, 0])
            bars.add(b)
            tags.add(label(_date(d), font_size=14, color=GREY_A).next_to(ax.c2p(k, -30), DOWN, buff=0.15))
        side = wrapped_label(rf"the six largest statement-day moves of 1997--2020, from {h['n']} statements; a typical "
                             rf"day moves {h['sd']:.0f} bp", 3.4, 16, GREY_A).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "This daily series measures a close-to-close association, not a minute-by-minute causal response. <bookmark mark='a'/> The two-year Treasury yield "
            f"had fallen {abs(h['dy']):.0f} basis points, the largest move on any statement day from 1997 to 2020. "
            f"<bookmark mark='b'/> On a typical statement day it moves about {h['sd']:.0f}. The other big days cluster "
            "in the same crisis. Other news and the policy decision share this daily window. Reading text and timing an executable trade are separate questions: "
            "can a machine read them as fast, and as well?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(tags))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], UP))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if top[k][1] > 0 else UP) for k, b in enumerate(bars[1:], 1)],
                                  lag_ratio=0.2), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        entries = [
            (r"Dictionaries", r"1966: General Inquirer. 2007: Tetlock's media pessimism. 2011: Loughran--McDonald."),
            (r"Neural models", r"2013: word2vec. 2017: transformer. 2018: BERT; HMP on FOMC transcripts. 2019: SESTM."),
            (r"Large models", r"2023: FinBERT study; BloombergGPT; LLM headline analysis. 2024: agents and leakage tests. 2025: chronological models."),
        ]
        cards = VGroup()
        for name, body in entries:
            if zh():
                # Keep adjacent English model names from becoming one oversized CJK-wrap token.
                from explainer.zh_text import translate
                body = translate(body).replace("。", "。 ").replace("；", "； ")
            cards.add(firm_card(name, body, kind=r"Historical sequence", width=4.0, font_size=23))
        cards.arrange(RIGHT, buff=0.32, aligned_edge=UP).move_to(DOWN * 0.2)
        head = label(r"Machines learn to read the market's words", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The tools are older than you might think. A psychologists' dictionary from the 1960s; Paul Tetlock's "
            "media pessimism in 2007; Loughran and McDonald's finance dictionary in 2011. <bookmark mark='a'/> Then "
            "the neural turn: word vectors in 2013, the transformer in 2017, BERT in 2018, the year a topic model also "
            "opened up the FOMC's transcripts; SESTM in 2019. <bookmark mark='b'/> And since 2023 the large language "
            "models: FinBERT, BloombergGPT, ChatGPT reading headlines, agents that trade, and the first models built so "
            "that they cannot read the future."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()


    def objectives(self):
        card = objectives_card([
            r"Words as numbers; dictionaries and why they misread; tone against the two-year yield",
            r"Forward guidance, readability, and what the committee publishes",
            r"Supervised words (SESTM), topics as eras, embeddings that learn \emph{easing}",
            r"Transformers, FinBERT and a pocket language model trained on the minutes",
            r"LLMs read the news; look-ahead bias, and a time-sliced experiment run here",
            r"Agents, alternative data and what crowding does to it; domain models",
            r"For the researcher: why screening finds the words, and how many documents it needs",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: words as numbers, dictionaries and why they misread; the bond market's reaction; forward "
            "guidance; supervised words, topics and embeddings, all on thirty years of the Fed's own documents; "
            "transformers, and a small language model of our own; what large language models can do with the news, "
            "and how they can cheat; agents and alternative data; and the theorem that says how many documents a "
            "word list needs."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk gets a reading room: tools to turn documents into features, each stamped "
            "with a required public-release clock, and a rule for what such a feature must survive. The original meeting-date fields alone do not supply that clock."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
