from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#F25F5C")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ the minister's budget", r"What primary balance holds the Island's debt steady?",
             "Chapter two. Play it: the minister's budget.", lit={2010: r"the consolidations"}, scale=("nation",),
             horizon=("a year",))
        self.desk()
        self.choose()
        self.reveal()

    def desk(self):
        P = load("playit")
        board = VGroup(
            label(r"you are the Island's finance minister", font_size=28, color=E.ACCENT),
            label(rf"debt: \ {100 * P['debt']:.0f}\% of GDP", font_size=25, color=DEBT),
            label(rf"interest rate: \ {100 * P['r']:.0f}\%; \ growth: \ {100 * P['g']:.0f}\%", font_size=25,
                  color=RATE),
            label(rf"this year: \ a primary deficit of {100 * P['deficit']:.0f}\% of GDP", font_size=25, color=TAX),
            label(r"your goal: \ stop the debt ratio rising", font_size=25, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. You are the Island's finance minister. <bookmark mark='a'/> The government owes a full year "
            f"of the Island's output. <bookmark mark='b'/> It pays {100 * P['r']:.0f} percent interest, and the "
            f"economy grows {100 * P['g']:.0f} percent a year. <bookmark mark='c'/> This year, spending other than "
            f"interest exceeds taxes by {100 * P['deficit']:.0f} percent of GDP. <bookmark mark='d'/> You want to "
            "stop the debt ratio from rising, and no more than that."
        ) as vo:
            self.play(FadeIn(board[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", board[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def _chips(self):
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.9, height=0.95, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=22, color=c))
                         for c, t in zip(CHIP, (r"A: \ a surplus of about 1\%", r"B: \ a balanced primary budget",
                                                r"C: \ a deficit of 1\% is enough"))]).arrange(RIGHT, buff=0.35)
        for ch in chips:
            ch[1].move_to(ch[0])
        return chips

    def choose(self):
        rows = VGroup(
            label(r"what primary balance holds debt at 100\% of GDP?", font_size=27, color=E.ACCENT),
            label(r"(interest 3\%, \ growth 2\%)", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.35).move_to(UP * 1.6)
        chips = self._chips().move_to(DOWN * 0.8)
        ring = countdown().scale(0.7).next_to(chips, DOWN, buff=0.4)
        with self.voiceover(
            "What primary balance holds the debt at a hundred percent of GDP? <bookmark mark='a'/> A surplus of "
            "about one percent of GDP; a balanced primary budget; or is a deficit of one percent enough? Pause, and "
            "choose."
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        chips = self._chips().move_to(UP * 2.4)
        rows = VGroup(
            MathTex(rf"s^{{*}} = \frac{{r - g}}{{1 + g}}\, b = \frac{{0.03 - 0.02}}{{1.02}} \times 1 = "
                    rf"{100 * P['stabilizing']:.2f}\%", font_size=36, color=TAX),
            label(rf"A: \ from a deficit of {100 * P['deficit']:.0f}\% to a surplus of about 1\%: \ a swing of "
                  rf"{100 * P['swing']:.1f}\% of GDP", font_size=23, color=CHIP[0]),
            label(rf"with a multiplier of 0.5, \ output falls about {100 * P['loss_m05']:.1f}\%; \ with 1.5, \ "
                  rf"about {100 * P['loss_m15']:.1f}\%", font_size=23, color=OUTPUT),
            label(r"and a smaller economy makes the same debt a larger ratio", font_size=23, color=HOLD),
            label(r"how big is the multiplier? \ the rest of the part", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.36).next_to(chips, DOWN, buff=0.55)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "<bookmark mark='a'/> Interest is a point above growth, so with debt equal to output the government "
            f"needs a primary surplus of {100 * P['stabilizing']:.2f} percent of GDP: answer A. "
            f"<bookmark mark='b'/> From a deficit of two percent, that is a swing of {100 * P['swing']:.1f} percent "
            "of GDP in spending cuts or tax rises. <bookmark mark='c'/> If each dollar of austerity costs half a "
            f"dollar of output, output falls about {100 * P['loss_m05']:.1f} percent; if it costs one and a half, "
            f"about {100 * P['loss_m15']:.1f}. <bookmark mark='d'/> And a smaller economy makes the same debt a "
            "larger share of it, so with a large multiplier, austerity can raise the debt ratio before it lowers "
            "it. <bookmark mark='e'/> Everything turns on the size of the multiplier, which is what the rest of "
            "this part is about."
        ) as vo:
            self.play(FadeIn(chips), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(chips[0], color=WHITE))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
