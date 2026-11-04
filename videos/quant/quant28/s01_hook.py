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
        parts = []
        for op, txt in h["diff"]:
            words = txt.split()
            if op == "=" and len(words) > 14:
                txt = " ".join(words[:6]) + " ... " + " ".join(words[-6:])
            parts.append((op, _tex(txt)))
        col = {"=": GREY_B, "-": BAD, "+": GOOD}
        chunks = VGroup()
        for op, txt in parts[:14]:
            t = (r"\sout{" + txt + "}") if op == "-" else txt
            chunks.add(wrapped_label(t, 12.4, 17, col[op]))
        chunks.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        if chunks.height > 5.6:
            chunks.scale_to_fit_height(5.6)
        chunks.to_edge(UP, buff=0.9)
        head = label(rf"the statement of {_date(h['date'])}, against the one before it ({_date(h['prev'])})",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        leg = VGroup(label(r"removed", font_size=17, color=BAD), label(r"added", font_size=17, color=GOOD),
                     label(r"unchanged", font_size=17, color=GREY_B)).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"On the {_date(h['date'])}, eight days before a scheduled meeting, the Federal Open Market Committee "
            "issued an unscheduled statement. <bookmark mark='a'/> Here it is, word by word, against the statement "
            "before it: in red what was removed, in green what was added. <bookmark mark='b'/> A cut of three quarters "
            "of a point instead of a quarter. A weakening of the economic outlook. Increasing downside risks to "
            "growth. A deepening housing contraction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.1) for c_ in chunks], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(*[Indicate(c_, color=GOOD, scale_factor=1.01) for (op, _), c_ in zip(parts, chunks) if op == "+"])
        self.wait(0.4)
        self.clear_scene()

    def moves(self, h):
        top = h["top"][:6]
        g = axes([-0.5, len(top) - 0.5], [-30, 30], x_length=8.4, y_length=4.2, xlabel=r"",
                 ylabel=r"two-year Treasury yield on the day, bp", xticks=[], yticks=[-30, -15, 0, 15, 30],
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
            "The bond market answered within minutes. <bookmark mark='a'/> By the close, the two-year Treasury yield "
            f"had fallen {abs(h['dy']):.0f} basis points, the largest move on any statement day from 1997 to 2020. "
            f"<bookmark mark='b'/> On a typical statement day it moves about {h['sd']:.0f}. The other big days cluster "
            "in the same crisis. Words, released at a known minute, moving one of the largest markets in the world: "
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
        I = QC.IDEA
        entries = [(1966, r"General Inquirer", I), (2007, r"Tetlock: media pessimism", I),
                   (2011, r"Loughran--McDonald", I), (2013, r"word2vec", I), (2017, r"the transformer", I),
                   (2018, r"BERT; HMP on the FOMC", I), (2019, r"SESTM", I), (2023, r"FinBERT; BloombergGPT; ChatGPT "
                                                                            r"reads headlines", I),
                   (2024, r"LLM agents; look-ahead tests", I), (2025, r"chronologically consistent LLMs", I)]
        strip = era_strip(entries, y0=1962, y1=2027, font_size=13).move_to(DOWN * 0.3)
        head = label(r"Machines learn to read the market's words", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 3), (3, 7), (7, 10)]
        with self.voiceover(
            "The tools are older than you might think. A psychologists' dictionary from the 1960s; Paul Tetlock's "
            "media pessimism in 2007; Loughran and McDonald's finance dictionary in 2011. <bookmark mark='a'/> Then "
            "the neural turn: word vectors in 2013, the transformer in 2017, BERT in 2018, the year a topic model also "
            "opened up the FOMC's transcripts; SESTM in 2019. <bookmark mark='b'/> And since 2023 the large language "
            "models: FinBERT, BloombergGPT, ChatGPT reading headlines, agents that trade, and the first models built so "
            "that they cannot read the future."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
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
            "with the moment its words became public, and a rule for what such a feature must survive."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
