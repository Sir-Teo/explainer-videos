from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ14.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how much do piece rates raise output?", r"Where pay follows output, \ how much "
             r"more output?", "Chapter thirteen. The Dials: how much do piece rates raise output?",
             scale=("person", "firm"), lit={2000: r"Lazear", 2004: r"Shearer", 2005: r"Bandiera et al."})
        self.dial()

    def dial(self):
        dial = dials.DIALS["piece_rate_response"]
        lo, hi, x0, x1 = 0.0, 60.0, -0.2, 6.3
        head = status_head(dial, r"output's response to piece rates \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [0, 10, 20, 30, 40, 50, 60], r"percent rise in output per worker",
                                top=1.9, step=0.8, fmt="{:.0f}")

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        half = 100 * tables.LAZEAR_2000.data["gain_published"] / 2
        inc = VGroup(Circle(radius=0.085, stroke_color=PAY, stroke_width=2.5).move_to([X(half), 1.9, 0]),
                     label(r"the same workers alone", font_size=14, color=PAY).move_to([X(half), 2.25, 0]))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.2)
        extra = label(r"a fifth to a half, \ where output is one person's and easy to count", font_size=23,
                      color=E.ACCENT).next_to(meaning, UP, buff=0.25)
        tag = published_tag(r"Lazear (2000); \ Shearer (2004); \ Bandiera, Barankay and Rasul (2005)", corner=UR,
                            font_size=12)
        with self.voiceover(
            "This part opens a dial for how much paying by output raises it. <bookmark mark='a'/> At Safelite, "
            "forty-four percent, of which about half, the hollow circle, came from the same workers working harder; "
            "the rest was who took the job. Shearer's tree planters, assigned at random, gave about twenty percent. "
            "Bandiera, Barankay and Rasul's fruit pickers gave at least fifty, but against pay relative to their "
            "friends, which had been holding them back. <bookmark mark='b'/> So the dial reads a fifth to a half, "
            "where output is one person's own and easy to count. <bookmark mark='c'/> It is settled within a range, "
            "and the range comes with conditions. These are jobs chosen because output could be measured. Where "
            "work is shared, or much of it can't be measured, chapters two, seven and twelve showed that the "
            "response can be smaller, or perverse. The dial returns in part thirty-eight, on personnel economics, "
            "with the field experiments that came after."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.6), run_time=2.5)
            self.play(FadeIn(inc))
            vo.wait_until("b")
            self.play(FadeIn(extra))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
