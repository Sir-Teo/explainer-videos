from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ57.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ forecast errors by horizon", r"How far ahead can the economy be read?",
             "Chapter thirteen. The Dials: forecast errors by horizon.", scale=("nation",), horizon=("a year",))
        self.dial()

    def dial(self):
        dial = dials.DIALS["gdp_forecast_rmse"]
        head = status_head(dial, r"error of forecasts of real GDP growth \ (new)")
        frame, rows = dial_rows(dial, 0, 4, [0, 1, 2, 3, 4], r"points of annual growth \ (root mean square)",
                                top=2.3, step=0.5, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens a new Dial: how far ahead the economy can be read. <bookmark mark='a'/> The "
            f"professional forecasters miss the current quarter's growth by {e[0].value:.2f} points, the next by "
            f"{e[1].value:.2f}, and a year ahead by {e[3].value:.2f}. <bookmark mark='b'/> The benchmark that takes "
            f"no skill, the last ten years' average, misses by {e[4].value:.2f}. <bookmark mark='c'/> The status "
            "is settled within a range: the present can be read, the next six months a little, and beyond that "
            "the forecast is mostly the average. For policy, that means what matters most is not the forecast "
            "but how quickly it is revised, which is the whole case for nowcasting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(1.0)
        self.clear_scene()
