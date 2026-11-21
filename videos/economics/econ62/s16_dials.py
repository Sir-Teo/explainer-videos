from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ62.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ management and CEO pay", r"How much does management add, \ and how much does "
             r"a chief executive gain when shareholders do?", "Chapter fourteen. The Dials: management and CEO pay.",
             scale=("firm",), horizon=("a year", "a decade"))
        self.management()
        self.pay()

    def management(self):
        dial = dials.DIALS["management_effect"]
        head = status_head(dial, r"what better management adds \ (new)")
        frame, rows = dial_rows(dial, 0, 0.3, [0, 0.1, 0.2, 0.3], r"proportional change in productivity", top=1.4,
                                step=0.9, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens two Dials. The first: how much basic management practices add to productivity. "
            f"<bookmark mark='a'/> The Mumbai experiment: {e[0].value:.2f}, a sixth, within a year. <bookmark "
            "mark='b'/> The Island's version, planted to match, with the spread its seventeen firms allow. "
            "<bookmark mark='c'/> The status is settled within a range, because the one large randomized test is "
            "backed by smaller trials elsewhere that find gains of the same sign, measured in other ways. The "
            "practices are cheap, which leaves the puzzle of chapter four: why firms had not adopted them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("ab"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def pay(self):
        dial = dials.DIALS["ceo_pay_performance"]
        head = status_head(dial, r"a CEO's wealth against the shareholders' \ (new)")
        frame, rows = dial_rows(dial, 0, 30, [0, 10, 20, 30], r"dollars per \$1,000 of shareholders' wealth"
                                .replace(",", "{,}"), top=1.7, step=0.8, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "The second: when shareholders gain a thousand dollars, how much does the chief executive gain? "
            f"<bookmark mark='a'/> Michael Jensen and Kevin Murphy, for 1974 to 1986: {e[0].value:.2f} dollars, "
            "counting pay, options, shares and the risk of being fired. They concluded that chief executives "
            "were paid like bureaucrats. <bookmark mark='b'/> Brian Hall and Jeffrey Liebman, for 1994, counting "
            f"the whole portfolio of stock and options: {e[1].value:.2f} dollars for the average chief executive, "
            f"<bookmark mark='c'/> and {e[2].value:.2f} for the median one. <bookmark mark='d'/> The status is "
            "contested: the answer depends on the years, on what is counted, and on whether the average or the "
            "typical executive is the question. Since the 1990s, holdings of stock and options, not salary, carry "
            "most of the incentive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
