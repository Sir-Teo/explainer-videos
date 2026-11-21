from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ58.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the discount rate and cost overruns", r"How much do the future and a forecast "
             r"count?", "Chapter thirteen. The Dials: the discount rate and cost overruns.",
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.discount()
        self.overrun()

    def discount(self):
        dial = dials.DIALS["social_discount_rate"]
        head = status_head(dial, r"the social discount rate \ (new)")
        frame, rows = dial_rows(dial, 0, 10, [0, 2, 4, 6, 8, 10], r"real \% a year", top=2.45, step=0.47,
                                fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens two Dials. The first is the social discount rate. <bookmark mark='a'/> America's budget "
            f"office, in 2003, asked for {e[0].value:.0f} and {e[1].value:.0f} percent, and does again. <bookmark "
            f"mark='b'/> Britain's Treasury used {e[2].value:.1f} percent for a quarter of a century and has just "
            f"accepted {e[3].value:.0f}. <bookmark mark='c'/> The 2023 American revision chose {e[4].value:.0f}, and "
            f"two hundred experts surveyed by Moritz Drupp and coauthors averaged {e[5].value:.2f}, with a median of "
            f"two. <bookmark mark='d'/> The market's own real rate on ten-year inflation-protected bonds has "
            f"averaged {e[6].value:.2f} percent since 2003. <bookmark mark='e'/> The status is contested: the "
            "number is partly economics, the growth and the risk of the future, and partly ethics, how much later "
            "generations should count, and a bridge or a climate rule can pass or fail on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[6]))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def overrun(self):
        dial = dials.DIALS["cost_overrun"]
        head = status_head(dial, r"cost overruns of public works \ (new)")
        frame, rows = dial_rows(dial, 0, 50, [0, 10, 20, 30, 40, 50], r"\% over the cost forecast at the decision "
                                r"to build", top=1.9, step=0.62, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second Dial is how far public works overrun their budgets. <bookmark mark='a'/> In Flyvbjerg, Holm "
            f"and Buhl's projects, rail ran {e[0].value:.1f} percent over, bridges and tunnels {e[1].value:.1f}, "
            f"roads {e[2].value:.1f}, and all of them together about {e[3].value:.0f}. <bookmark mark='b'/> It "
            "depends on the setting: on the kind of project, the country and the decade, and on which projects keep "
            "good enough records to be counted. But the direction does not depend on the setting. An appraisal that "
            "takes the cost estimate at its word is biased towards building."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
