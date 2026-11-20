from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ28.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ the slope, \ and the sacrifice ratio", r"How much inflation does slack remove, "
             r"\ and what does a point of disinflation cost?", "Chapter fourteen. The Dials: the slope, and the "
             "sacrifice ratio.", lit={1958: r"Phillips", 1994: r"Ball"}, scale=("nation",), horizon=("years",))
        self.slope()
        self.sacrifice()

    def slope(self):
        dial = dials.DIALS["phillips_slope"]
        head = status_head(dial, r"the slope of the Phillips curve \ (new)")
        frame, rows = dial_rows(dial, -2.0, 0.0, [-2.0, -1.5, -1.0, -0.5, 0.0], r"points of inflation per point of "
                                r"unemployment", top=2.0, step=0.68, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Phillips (1958); \ Samuelson and Solow (1960); \ this film", corner=DR, font_size=12)
        with self.voiceover(
            "Two new dials. The first is the slope of the Phillips curve. <bookmark mark='a'/> Phillips's own wage "
            "curve, at three percent unemployment, has a slope of about minus one: a point less unemployment, a "
            "point more wage growth. <bookmark mark='b'/> Samuelson and Solow's menu for America implies about minus "
            "one point eight. <bookmark mark='c'/> This film's regressions, of the change in core inflation on "
            "unemployment against its natural rate, give minus point six five for 1960 to 1983, "
            "<bookmark mark='d'/> minus point one eight for 1984 to 1999, <bookmark mark='e'/> and minus point "
            "zero seven since 2000. <bookmark mark='f'/> The status: contested. Some of the flattening is real, and "
            "some of it is anchored expectations and good policy hiding the curve, and estimates across states "
            "suggest it was never as steep as the aggregate data made it look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def sacrifice(self):
        dial = dials.DIALS["sacrifice"]
        head = status_head(dial, r"the sacrifice ratio \ (new)")
        frame, rows = dial_rows(dial, 0.0, 4.0, [0, 1, 2, 3, 4], r"point-years of output per point of disinflation",
                                top=1.6, step=0.8, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Ball (1994); \ Mankiw (1991); \ this film", corner=DR, font_size=12)
        V = load("volcker")
        with self.voiceover(
            "The second: the sacrifice ratio, the output lost for each point of inflation removed. "
            "<bookmark mark='a'/> Laurence Ball's estimate for America's disinflation of 1979 to 1983 is about one "
            "point eight. <bookmark mark='b'/> Gregory Mankiw's textbook calculation, turning the extra unemployment "
            "into output with Okun's law, gives about two point eight. <bookmark mark='c'/> This film's, against the "
            f"Budget Office's potential, about {V['sac_ratio']:.1f}. <bookmark mark='d'/> Contested, because each "
            "number depends on what you call trend output and trend inflation, and statistical estimates are so "
            "imprecise that their intervals include zero. The rough consensus: about two years' worth of a point "
            "of output per point, less if the cure is fast and believed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
