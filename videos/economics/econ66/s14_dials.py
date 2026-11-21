from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ66.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The Dials: \ who pays, \ and what a war costs", r"How much of a tariff reaches prices, \ and "
             r"how much does a tariff war cost?", "Chapter twelve. The Dials: who pays, and what a war costs.",
             scale=("nation", "world"), horizon=("a year", "a decade"))
        self.passthrough()
        self.war()

    def passthrough(self):
        dial = dials.DIALS["passthrough"]
        head = status_head(dial, r"pass-through \ (Parts 34 and 36, \ now 66)")
        frame, rows = dial_rows(dial, 0, 1.1, [0, 0.25, 0.5, 0.75, 1.0], r"share of a currency move or a tariff "
                                r"that reaches prices", top=2.4, step=0.72, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 16, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "Two Dials. The first is pass-through, first opened in Part thirty-four. <bookmark mark='a'/> For "
            "exchange rates, little of a currency move reaches American import prices when they are set in dollars, "
            "nearly all when they are set in the exporter's currency, and this film's own estimate is "
            f"{e[4].value:.2f} after a year. <bookmark mark='b'/> For the tariffs of 2018 and 2019, Amiti and her "
            "coauthors and Fajgelbaum and his found complete pass-through to the prices American buyers paid at "
            "the border. <bookmark mark='c'/> And for 2025, at the next stage, the shelf: about a fifth of the "
            "tariff had reached retail prices by September, in Cavallo and coauthors' daily data. <bookmark "
            "mark='d'/> The status: depends on the setting. At the border, tariffs are paid by American buyers; "
            "how much reaches consumers, and how fast, depends on margins, competition and time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[4]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def war(self):
        dial = dials.DIALS["trade_war_loss"]
        head = status_head(dial, r"the cost of a tariff war \ (new)")
        frame, rows = dial_rows(dial, 0, 3.5, [0, 1, 2, 3], r"percent of real income, \ Nash tariffs against "
                                r"cooperation", top=1.6, step=0.95, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second Dial is new: the cost of a tariff war, from cooperation to the tariffs each country would "
            f"choose alone. <bookmark mark='a'/> Ossa's model of the world economy: {e[0].value:.1f} percent of "
            "income on average, with lobbying pushing tariffs up. <bookmark mark='b'/> This film's two-bloc war: "
            f"{e[1].value:.2f} percent for the United States, {e[2].value:.2f} percent for the rest of the world. "
            "<bookmark mark='c'/> The status: depends on the setting. More trade, and more political pressure, "
            "make a war costlier. And in every model, the gain from a tariff lasts only while others do not answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
