from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ13.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how much does adverse selection cost?", r"Across insurance markets where it has "
             r"been measured, \ how large is the triangle?", "Chapter thirteen. The Dials: how much does adverse "
             "selection cost?", scale=("person", "market"), lit={2010: r"the cost measured"})
        self.dial()

    def dial(self):
        dial = dials.DIALS["selection_cost"]
        d = load("dial")
        head = status_head(dial, r"the welfare cost of adverse selection \ (new)")
        frame, rows = dial_rows(dial, 0.0, 10.0, [0, 2, 4, 6, 8, 10], r"percent of what is at stake \ (each "
                                r"study's own measure)", top=1.9, step=0.8, fmt="{:.1f}")
        x8 = -0.2 + 6.5 * d["hkk"]["handel_loss"] * 100 / 10
        hand = VGroup(DashedLine([x8, 2.35, 0], [x8, -0.15, 0], color=HOLD, stroke_width=2),
                      label(r"Handel: \ if inertia were cured", font_size=15, color=HOLD).move_to([x8, 2.55, 0]))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.2)
        extra = label(r"real, \ measurable, \ and in employer plans \ small: \ a few percent of what's at stake",
                      font_size=22, color=E.ACCENT).next_to(meaning, UP, buff=0.25)
        tag = published_tag(r"Einav, Finkelstein and Cullen (2010); \ Cutler and Reber (1998); \ Hackmann, Kolstad "
                            r"and Kowalski (2015); \ Handel (2013)", corner=UR, font_size=11)
        with self.voiceover(
            "This part opens a dial for what adverse selection costs. <bookmark mark='a'/> At Alcoa, Einav, Finkelstein "
            "and Cullen put it at about three percent of the surplus at stake. At Harvard, Cutler and Reber put it at "
            "two to four percent of what the university had been spending. In Massachusetts's individual market, "
            "Hackmann, Kolstad and Kowalski found that reducing selection with a mandate gained about four percent "
            "per person. <bookmark mark='b'/> Each study measures against its own yardstick, so the rows are not "
            "quite comparable; but they agree that the triangle is real, measurable, and in employer plans small. "
            "<bookmark mark='c'/> Handel's estimate, the dashed line, is what the cost would become if employees "
            "chose more actively: more than eight percent of premiums. So the dial depends on the setting. Selection "
            "costs little where inertia and employers' subsidies hold the pool together, and more where individuals "
            "shop freely, which is why the remedies of chapter eleven matter most in individual markets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(extra))
            vo.wait_until("c")
            self.play(FadeIn(hand), FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
