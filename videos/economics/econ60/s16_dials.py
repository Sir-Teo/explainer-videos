from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ60.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ pass-through and elasticities", r"How much of a cost change reaches the shelf, \ "
             r"and how sensitive is one product's demand?", "Chapter fourteen. The Dials: pass-through and "
             "elasticities.", scale=("firm", "market"), horizon=("a year",))
        self.passthrough()
        self.elasticity()

    def passthrough(self):
        dial = dials.DIALS["retail_passthrough"]
        head = status_head(dial, r"cost pass-through to retail prices \ (new)")
        frame, rows = dial_rows(dial, 0, 1.0, [0, 0.25, 0.5, 0.75, 1.0], r"share of a change in producers' prices "
                                r"that reaches retail prices", top=1.7, step=0.8, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens one Dial and returns to another. The new one is cost pass-through to retail prices. "
            f"<bookmark mark='a'/> American food, 2000 to 2019: {e[0].value:.2f} of a change in factory-gate prices "
            f"reached the grocer's shelf within a year. <bookmark mark='b'/> 2021 to 2023: about {e[1].value:.2f}, "
            "measured as the ratio of the two rises. <bookmark mark='c'/> And Staples' pass-through of a cost "
            f"change at one firm only, from Part fifty-nine: about {e[2].value:.2f}. <bookmark mark='d'/> The status "
            "is that it depends on the setting: on how much of the retail price is the retailer's own cost, and on "
            "whether rivals share the cost change. The same retailer passes on a shared shock far more than a "
            "private one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def elasticity(self):
        dial = dials.DIALS["product_elasticity"]
        head = status_head(dial, r"one product's own-price elasticity \ (Part 43's Dial)")
        frame, rows = dial_rows(dial, -5, 0, [-5, -4, -3, -2, -1, 0], r"percent change in sales for a 1\% price rise",
                                top=2.0, step=0.62, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second Dial is Part forty-three's: how sensitive one product's sales are to its own price. "
            "<bookmark mark='a'/> Its rows from cars and cereal show the range, and the warning that an estimate "
            "below one in magnitude means the method has failed. <bookmark mark='b'/> This part adds DellaVigna and "
            f"Gentzkow's stores: within the typical chain, from {e[-1].lo:.2f} to {e[-1].hi:.2f} between the tenth "
            "and ninetieth percentiles. <bookmark mark='c'/> A seventeen percent difference in the best prices, "
            "which the chains chose not to charge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:-1]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[-1]))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
