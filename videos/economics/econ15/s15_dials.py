from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ15.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ do new roads fill?", r"When a city adds lanes, \ how much more driving follows?",
             "Chapter thirteen. The Dials: do new roads fill?", scale=("city",), lit={2011: r"Duranton and Turner"})
        self.dial()

    def dial(self):
        dial = dials.DIALS["road_traffic"]
        d = load("dial")["roads"]
        lo, hi, x0, x1 = 0.0, 1.5, -0.2, 6.3
        head = status_head(dial, r"traffic's response to roads \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5], r"elasticity of driving with "
                                r"respect to lane kilometres", top=1.6, step=0.9, fmt="{:.2f}")

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        one = VGroup(DashedLine([X(1.0), 2.1, 0], [X(1.0), 0.32, 0], color=GOOD, stroke_width=2),
                     label(r"one: \ every new lane fills", font_size=15, color=GOOD).move_to([X(1.0), 2.3, 0]))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.25)
        extra = label(r"the instruments: \ explorers' routes of the 1830s, \ railroads of 1898, \ the 1947 highway "
                      r"plan", font_size=20, color=GREY_B).next_to(meaning, UP, buff=0.25)
        tag = published_tag(r"Duranton and Turner, AER 101(6) (2011), Tables 3 and 5", corner=UR, font_size=12)
        with self.voiceover(
            "This part opens a dial for what new roads do to traffic. An elasticity of one would mean that a city "
            "with ten percent more lanes has ten percent more driving: every new lane fills. "
            "<bookmark mark='a'/> Gilles Duranton and Matthew Turner measured it across American cities from 1983 to "
            "2003. A plain comparison of cities gives nought point eight six. <bookmark mark='b'/> But roads are "
            "built where traffic is expected, so they also used three instruments for where highways ended up, "
            "chosen because they were drawn for other purposes, long before today's traffic: the routes of explorers "
            "in the 1830s, the railroads of 1898, and a 1947 plan for highways between cities. With them, the elasticity is about one. <bookmark mark='c'/> They called "
            "it the fundamental law of road congestion: building roads does not relieve congestion, because the new "
            "lanes fill, and more public transport did not reduce driving either. Settled within a range, for American "
            "cities. "
            "What does relieve congestion is a price, as Stockholm found. The dial returns in part thirty-seven, on "
            "cities."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(one))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(extra))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
