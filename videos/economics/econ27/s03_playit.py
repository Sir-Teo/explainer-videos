from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403

CHIP = ("#7EC8F5", "#C9A0FF")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ hoard or spend?", r"You hold three coupons. \ What do you do this week?",
             "Chapter two. Play it: hoard, or spend?", lit={1977: r"Sweeney and Sweeney"}, scale=("household",),
             horizon=("a week",))
        self.choose()
        self.reveal()

    def choose(self):
        P = load("coop_path")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        rows = VGroup(
            label(r"you are a couple in the Island's co-op", font_size=23, color=GREY_A),
            label(r"you hold 3 coupons", font_size=26, color=COUPON),
            label(rf"you would like {P['target']:.0f} in reserve before the busy season", font_size=24, color=SAVE),
            label(r"this week you could go out for an evening, \ or stay in and offer to sit", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(stage.box.get_top() + DOWN * 1.7)
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=28, color=c))
                         for c, t in zip(CHIP, (r"A: \ spend a coupon", r"B: \ hoard, \ and sit"))]).arrange(
            RIGHT, buff=0.6)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(rows, DOWN, buff=0.55)
        ring = countdown().next_to(chips, DOWN, buff=0.35)
        with self.voiceover(
            "Your turn. You are a couple in the Island's co-op. <bookmark mark='a'/> You hold three coupons. "
            f"<bookmark mark='b'/> You would like to have {P['target']:.0f} in reserve before the busy season, "
            "when you know you will want to go out more. <bookmark mark='c'/> This week you could spend a coupon on "
            "an evening out, or stay in and offer to sit for someone else, to build up your reserve. Spend, or "
            "hoard? Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(rows[0]))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("coop_path")
        rate = P["before"] / P["sitters_before"]
        rows = VGroup(
            label(r"for you, \ hoarding is sensible: \ you are short of your reserve", font_size=24, color=SAVE),
            label(r"but everyone in the co-op is short, \ so everyone chooses B", font_size=24, color=GREY_A),
            label(rf"each week, \ {100 * P['sitters_before']:.0f}\% of couples offer to sit, \ "
                  rf"but only {100 * P['goers_before']:.0f}\% go out", font_size=24, color=PRICE),
            label(rf"so an offer to sit finds a job only {100 * rate:.0f}\% of the time: \ hoarding is slow",
                  font_size=24, color=PRICE),
            label(r"what is wise for each couple is ruinous for the co-op: \ the fallacy of composition",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "There is no wrong answer for you alone. <bookmark mark='a'/> If you chose B, you were sensible: you "
            "are short of your reserve, and sitting is how you build it. <bookmark mark='b'/> But every couple in "
            "the co-op is short, so every couple chooses B. <bookmark mark='c'/> In Agora's co-op, each week about "
            f"{100 * P['sitters_before']:.0f} percent of couples offer to sit, and only "
            f"{100 * P['goers_before']:.0f} percent go out. <bookmark mark='d'/> So an offer to sit finds a job "
            f"only about {100 * rate:.0f} percent of the time, and nobody's reserve grows quickly, because the "
            "coupons are not there to be earned. <bookmark mark='e'/> What is wise for each couple is ruinous for "
            "the co-op as a whole. Economists call it the fallacy of composition, and it is the heart of this part."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
