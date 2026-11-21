from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ59.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ pass-through and cartel overcharges", r"How much of a saving reaches buyers, "
             r"\ and how much does a cartel take?", "Chapter fourteen. The Dials: pass-through and cartel "
             "overcharges.", scale=("firm", "market"), horizon=("a year",))
        self.passthrough()
        self.overcharge()

    def passthrough(self):
        dial = dials.DIALS["merger_passthrough"]
        head = status_head(dial, r"pass-through of a merger's cost savings \ (new)")
        frame, rows = dial_rows(dial, 0, 100, [0, 20, 40, 60, 80, 100], r"\% of a cut in one firm's marginal cost "
                                r"that reaches its prices", top=1.7, step=0.75, fmt="{:.0f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens one Dial and returns to another. The new one is the pass-through of a merger's cost "
            f"savings. <bookmark mark='a'/> Staples' own history: about {e[0].lo:.0f} to {e[0].hi:.0f} percent of "
            "firm-specific cost changes reached its prices, the number the court set against the companies' "
            f"two-thirds. <bookmark mark='b'/> The Island's Alder, alone, passes on {e[1].value:.0f} percent of a "
            f"saving; <bookmark mark='c'/> merged with Birch, {e[2].value:.0f}. <bookmark mark='d'/> The status: it "
            "depends on the setting, on the curvature of demand and on how many of the firm's rivals share the "
            "saving. But the direction holds everywhere: a saving one firm enjoys alone is passed on less than one "
            "that the whole industry shares, and a merged firm passes on less than an independent one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def overcharge(self):
        dial = dials.DIALS["cartel_overcharge"]
        head = status_head(dial, r"cartel overcharges \ (Part 12's Dial)")
        frame, rows = dial_rows(dial, 0, 40, [0, 10, 20, 30, 40], r"\% by which a cartel's price exceeds the price "
                                r"without it", top=1.7, step=0.7, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second Dial is Part twelve's: how much cartels overcharge. <bookmark mark='a'/> John Connor's "
            f"collection of hundreds of published estimates has a median of about {e[0].value:.0f} percent. "
            "<bookmark mark='b'/> Marcel Boyer and Rachidi Kotchoni, correcting the same collection for the ways "
            f"estimates are made and published, put the median at about {e[1].value:.0f}. <bookmark mark='c'/> The "
            f"lysine cartel of the 1990s, about {e[2].value:.0f}. <bookmark mark='d'/> And the Island's cement "
            f"cartel, measured by this part's regression: {e[3].value:.1f}, against eighteen planted. <bookmark "
            "mark='e'/> The status stays contested. The low end and the high end imply very different fines, and "
            "whether the published estimates are biased upward is itself the argument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
