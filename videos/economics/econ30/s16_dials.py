from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ30.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ how often prices change", r"What share of prices changes in a month?",
             "Chapter fourteen. The Dials: how often prices change.",
             lit={2004: r"Bils and Klenow", 2008: r"Nakamura and Steinsson"}, scale=("firm",), horizon=("a month",))
        self.frequency()

    def frequency(self):
        dial = dials.DIALS["price_frequency"]
        head = status_head(dial, r"the frequency of price changes \ (new)")
        frame, rows = dial_rows(dial, 0.0, 0.3, [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3], r"share of prices changing in "
                                r"a month", top=2.0, step=0.68, fmt="{:.3f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Bils and Klenow (2004); \ Nakamura and Steinsson (2008); \ this film", corner=DR,
                            font_size=12)
        with self.voiceover(
            "This part's new dial is the frequency of price changes: the share of prices that change in a month. "
            "<bookmark mark='a'/> Bils and Klenow's median duration of four point three months corresponds to about "
            "a fifth of prices changing each month. <bookmark mark='b'/> Nakamura and Steinsson find much the same "
            "when sales count, about nineteen to twenty percent. <bookmark mark='c'/> Without sales, nine to twelve "
            "percent. <bookmark mark='d'/> And the Island's Calvo calibration, prices lasting nine months on "
            "average, means about thirteen percent. <bookmark mark='e'/> The status: settled within a range, "
            "between about one in ten and one in five. Which end belongs in a model depends on whether temporary "
            "sales matter for money, and the evidence says they matter less than their number suggests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
