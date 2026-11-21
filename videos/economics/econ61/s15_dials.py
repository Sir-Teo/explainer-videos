from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ61.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ surge elasticities and the return on search ads", r"How sensitive are riders to "
             r"the surge, \ and do search ads pay?", "Chapter thirteen. The Dials: surge elasticities and the "
             "return on search ads.", scale=("person", "firm"), horizon=("a day", "a year"))
        self.surge()
        self.ads()
        self.reserve()

    def surge(self):
        dial = dials.DIALS["surge_elasticity"]
        head = status_head(dial, r"the elasticity of rides to the surge price \ (new)")
        frame, rows = dial_rows(dial, -1.0, 0, [-1.0, -0.75, -0.5, -0.25, 0], r"percent change in rides booked for a "
                                r"1\% higher fare", top=2.0, step=0.62, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens two Dials and returns to a third. The first: how much riders' bookings fall when the "
            "fare rises. <bookmark mark='a'/> Cohen and his co-authors, over the whole sample: minus "
            f"{abs(e[0].value):.2f}. <bookmark mark='b'/> In Los Angeles, minus {abs(e[1].value):.2f}, on weekend "
            f"days minus {abs(e[2].value):.2f}, on weekdays outside the rush hours minus {abs(e[3].value):.2f}. "
            f"<bookmark mark='c'/> The Island's riders, minus {abs(e[4].value):.2f}, planted to sit inside that "
            "range. <bookmark mark='d'/> The status: it depends on the setting, but every estimate is well below "
            "one in size. Demand for a ride on a busy night is inelastic, which is why surge clears the market "
            "mainly by bringing out drivers, and why riders keep so much surplus."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:4]], lag_ratio=0.4), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def ads(self):
        dial = dials.DIALS["search_ad_return"]
        head = status_head(dial, r"the return on search advertising \ (new)")
        frame, rows = dial_rows(dial, -2, 28, [0, 5, 10, 15, 20, 25], r"extra revenue per dollar, \ less the "
                                r"dollar", top=1.9, step=0.75, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second: the return on search advertising, in extra revenue per dollar, less the dollar. "
            f"<bookmark mark='a'/> eBay's experiment: minus {abs(e[0].value):.2f}, with an interval that stays "
            "below zero. <bookmark mark='b'/> The same data without the experiment: plus "
            f"{e[1].value:.1f}. <bookmark mark='c'/> The Island's experiment and its regression repeat the "
            "pattern, by construction: the truth was planted below zero. <bookmark mark='d'/> The status is "
            "contested, and for an unusual reason. The two kinds of estimate do not merely differ in size; they "
            "differ in sign. Ads that reach new customers can pay; ads shown to people already on their way to "
            "buy cannot, and only an experiment tells the two apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def reserve(self):
        dial = dials.DIALS["reserve_revenue"]
        head = status_head(dial, r"what a reserve price adds \ (Part 16's Dial)")
        frame, rows = dial_rows(dial, -0.06, 0.08, [-0.05, 0, 0.05], r"proportional change in revenue",
                                top=1.6, step=0.8, fmt="{:+.3f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "And the Dial from Part sixteen returns, with chapter six's auctions behind it: what a reserve price "
            "adds to an ad auction's revenue. <bookmark mark='a'/> Ostrovsky and Schwarz's experiment at Yahoo!, "
            f"at fixed search volumes: plus {100 * e[0].value:.1f} percent overall, <bookmark mark='b'/> minus "
            f"{abs(100 * e[1].value):.1f} percent on keywords searched fewer than ten times a day, and plus "
            f"{100 * e[2].value:.1f} percent on the busy ones. <bookmark mark='c'/> The theory's reserve raises "
            "revenue where bidders were many, and cost it where they were few, by driving some of them away: a "
            "lesson the static theory, which holds the bidders fixed, does not teach."
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
