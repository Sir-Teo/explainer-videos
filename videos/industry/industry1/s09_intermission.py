from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        H = R["history"]
        years, sales, units = H["years"], H["sales"], H["units"]
        pa = viz.plot_axes((2007.3, 2026.7), (0, 270), x_length=11.6, y_length=4.9,
                           xticks=[2008, 2011, 2014, 2017, 2020, 2023, 2026], yticks=[0, 50, 100, 150, 200, 250],
                           xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"${v:.0f}bn", size=17,
                           ylabel="iPhone net sales, by Apple's fiscal year").shift(DOWN * 0.35 + RIGHT * 0.3)
        bars = viz.year_bars(pa, years, sales, I.BRAND, width=0.46)
        head = T("Intermission: nineteen years of iPhone sales", 26, I.DIM).to_edge(UP, buff=0.4)
        src = source("Apple Form 10-K, fiscal 2010 to 2026 (latest restated figure for each year)")
        yr = TB("2008", 40, I.ACCENT).to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        val = T("", 24, I.TEXT)
        marks = {2008: "iPhone 3G", 2015: "iPhone 6: bigger screens", 2021: "iPhone 12 and 13: 5G",
                 2026: "a record: $254.1bn"}
        notes = VGroup()
        with self.voiceover(
            "An intermission. Here is what Apple has earned from iPhones in each fiscal year since the first full "
            "year of sales. <bookmark mark='a'/> From under 7 billion dollars in 2008 to 155 billion in 2015, the "
            "year the screens got bigger. <bookmark mark='b'/> Then five flat years, as the phone market stopped "
            "growing. <bookmark mark='c'/> Then 5G, and a new plateau around 200 billion. <bookmark mark='d'/> And "
            "in fiscal 2026, a record: 254 billion dollars, even as fewer phones were sold worldwide."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(yr))
            vo.wait_until("a")
            for i, (y, b) in enumerate(zip(years, bars)):
                anims = [GrowFromEdge(b, DOWN), Transform(yr, TB(str(y), 40, I.ACCENT).move_to(yr))]
                if y in marks:
                    n = T(marks[y], 16, I.TEXT).next_to(b, UP, buff=0.12)
                    if y == 2026:
                        n.shift(LEFT * 0.9)
                    if y == 2021:
                        n.shift(LEFT * 1.1 + UP * 0.15)
                    notes.add(n)
                    anims.append(FadeIn(n))
                self.play(*anims, run_time=0.45)
                if y == 2015:
                    vo.wait_until("b")
                if y == 2020:
                    vo.wait_until("c")
                if y == 2025:
                    vo.wait_until("d")
        self.wait(1.0)
        self.clear_scene()
        so = VGroup(TB("The story so far", 34, I.ACCENT),
                    T("A phone's price is a chain of other companies' revenues.", 28, I.TEXT),
                    T("Counted once, as value added, the chain adds up to the price.", 28, I.TEXT),
                    T("The links that are hardest to replace keep the most.", 28, I.TEXT),
                    T("Next: what the label says, and what happened in 2026.", 24, I.DIM)
                    ).arrange(DOWN, buff=0.32)
        with self.voiceover(
            "The story so far. A phone's price is a chain of other companies' revenues. Counted once, as value "
            "added, the chain adds up exactly to the price. And the links that are hardest to replace keep the "
            "most. Next: what the label on the phone says, and what happened in 2026."
        ):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in so], lag_ratio=0.5), run_time=4)
        self.clear_scene()
