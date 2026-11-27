from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 14, "Called it?", "Has China's steel demand finished falling?", "Chapter fourteen. Called it?",
             lit=("change",))
        self.theirs()
        self.ours()

    def theirs(self):
        C = R["called"]
        rows = [r_ for r_ in C["rows"] if r_["actual"] is not None]
        pa = viz.plot_axes([0, len(rows)], [-8.5, 1.5], x_length=7.4, y_length=4.4, xticks=[], yticks=[-8, -6, -4, -2, 0],
                           yfmt=lambda v: f"{v:+.0f}%" if v else "0%", ylabel="change in China's steel demand", size=13).move_to(
            [-2.4, -0.3, 0])
        zero = Line(pa.ax.c2p(0, 0), pa.ax.c2p(len(rows), 0), stroke_color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for i, r_ in enumerate(rows):
            f_, a_ = r_["forecast"], r_["actual"]
            fb = Rectangle(width=0.5, height=max(abs(pa.ax.c2p(0, f_)[1] - pa.ax.c2p(0, 0)[1]), 0.04), stroke_color=PRICE,
                           stroke_width=2, fill_color=PRICE, fill_opacity=0.35).move_to(pa.ax.c2p(i + 0.34, 0), aligned_edge=UP)
            ab = Rectangle(width=0.5, height=abs(pa.ax.c2p(0, a_)[1] - pa.ax.c2p(0, 0)[1]), stroke_width=0, fill_color=CHINA,
                           fill_opacity=0.9).move_to(pa.ax.c2p(i + 0.66, 0), aligned_edge=UP)
            lab = VGroup(tx(str(r_["year"]), 16, WHITE, bold=True), tx(f"forecast Oct {r_['made']}", 12, GREY_A)).arrange(
                DOWN, buff=0.02).next_to(pa.ax.c2p(i + 0.5, 1.5), DOWN, buff=0.05)
            fv = tx(f"{f_:+.1f}%" if f_ else "flat", 13, PRICE).next_to(fb, DOWN, buff=0.05)
            av = tx(f"{a_:+.1f}%", 14, CHINA, bold=True).next_to(ab, DOWN, buff=0.05)
            bars.add(VGroup(lab, fb, fv, ab, av))
        key = VGroup(VGroup(Square(0.2, stroke_color=PRICE, fill_color=PRICE, fill_opacity=0.35), tx("worldsteel's forecast, the "
                                                                                                    "October before", 14, PRICE)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=CHINA, fill_opacity=0.9), tx("what happened", 14, CHINA)
                            ).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.2, 1.6, 0])
        verdict = VGroup(tx("Too high, three years running.", 22, BAD, bold=True),
                         tx("Forecasters, including the steelmakers'", 15, GREY_A),
                         tx("own association, kept expecting the fall", 15, GREY_A),
                         tx("to end next year.", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.2, -1.0, 0])
        src = source("World Steel Association: Short Range Outlooks, October 2022-2025 and April 2026; World Steel in Figures "
                     "2026 (apparent steel use)", size=13)
        with self.voiceover(
            "Part eleven's forecast to test comes from the steel industry itself. <bookmark mark='a'/> Every October, the "
            "World Steel Association publishes its forecast of steel demand for the year ahead, country by country. "
            "Here are its forecasts for China. <bookmark mark='b'/> In October 2022, it expected China's demand in 2023 "
            "to be flat. It fell more than two per cent. <bookmark mark='c'/> In October 2023, flat again for 2024. It "
            "fell more than five per cent. <bookmark mark='d'/> In October 2024, a fall of one per cent in 2025. The "
            "association's own later report gives the official figure: a fall of seven per cent. <bookmark mark='e'/> "
            "Called it? No, three years running. Each time, the people who know the industry best expected China's "
            "property slump to bottom out within a year. Each time it went on."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b[0]) for b in bars], lag_ratio=0.2))
            for m, b in zip("bcd", bars):
                vo.wait_until(m)
                self.play(GrowFromEdge(b[1], UP), FadeIn(b[2]), run_time=0.7)
                self.play(GrowFromEdge(b[3], UP), FadeIn(b[4]), run_time=0.9)
            vo.wait_until("e")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("When worldsteel publishes China's steel demand", 18, WHITE),
                       tx("for 2026 (April 2027), it will show a fall", 18, WHITE),
                       tx(f"of more than {abs(C['f26']):.1f}%, the figure it forecast in October 2026.", 18, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked in April 2027", 14, GREY_A)).arrange(DOWN, buff=0.12).move_to([3.0, 0.6, 0])
        why = VGroup(tx("For:", 16, GOOD, bold=True),
                     tx("three years of forecasts that were too high;", 15, GREY_A),
                     tx(f"crude steel output down {abs(C['ytd']):.1f}% in Jan-Oct 2026", 15, GREY_A),
                     tx("Against:", 16, BAD, bold=True),
                     tx("exports and factories holding up; revisions", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.05).move_to([-3.8, 0.4, 0])
        ship = draw.ship(2.2).move_to([-3.8, -2.4, 0])
        src = source("World Steel Association, Short Range Outlook (12 October 2026) and 'October 2026 crude steel production' "
                     "(24 November 2026)", size=13)
        with self.voiceover(
            "Now our own forecast, written down so you can check it. <bookmark mark='a'/> In October 2026, worldsteel "
            f"forecast that China's steel demand would fall {abs(C['f26']):.0f} per cent in 2026. <bookmark mark='b'/> "
            "We think it will turn out to have fallen by more than that. Its forecasts have erred on the high side three "
            f"years running, and China's crude steel output in the first ten months of 2026 was {abs(C['ytd']):.1f} per "
            "cent below the year before. Against us: exports and factories have held up, and the figures get revised. "
            f"<bookmark mark='c'/> We give it {100 * C['prob']:.0f} per cent. We will check it against worldsteel's own "
            "report in April 2027, and report the answer, right or wrong."
        ) as vo:
            self.play(FadeIn(src), FadeIn(ship), FadeIn(card_[0]))
            vo.wait_until("a")
            self.play(FadeIn(card_[1:4], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(why, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(card_[4:], scale=1.1))
        self.clear_scene()
