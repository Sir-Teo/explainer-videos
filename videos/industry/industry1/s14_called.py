from __future__ import annotations

from explainer.industry.calls import calls
from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 15, "Called it?", "Who forecast this industry, and how did they do?",
             "Chapter fifteen. Called it?", lit=("change",))
        self.ballmer()
        self.ours()

    def ballmer(self):
        q = VGroup(T("“There’s no chance that the iPhone is going to get", 32, I.TEXT),
                   T("any significant market share. No chance.”", 32, I.TEXT),
                   T("Steve Ballmer, chief executive of Microsoft, April 2007", 22, I.DIM)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.8)
        H = R["history"]
        units = [(y, u) for y, u in zip(H["years"], H["units"]) if u is not None]
        pa = viz.plot_axes((2007.4, 2018.6), (0, 250), x_length=6.0, y_length=2.8, xticks=[2008, 2013, 2018],
                           yticks=[0, 100, 200], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}m", size=15,
                           ylabel="iPhones sold (Apple 10-K)").shift(LEFT * 3.2 + DOWN * 1.6)
        bars = viz.year_bars(pa, [y for y, _ in units], [u for _, u in units], I.BRAND, width=0.4)
        right = VGroup(VGroup(TB("about 1 in 5", 34, I.BRAND), T("Apple's share of phones shipped, 2025", 20, I.TEXT))
                       .arrange(DOWN, buff=0.05),
                       VGroup(TB(money_short(get("apple.iphone_sales.fy2026")), 34, I.PROFIT),
                              T("iPhone sales, fiscal 2026", 20, I.TEXT)).arrange(DOWN, buff=0.05),
                       VGroup(TB(f"{pct(get('share.apple.revenue.q2_2026'))} of the revenue", 30, I.ACCENT),
                              T("of the whole phone industry, Q2 2026 (Counterpoint)", 18, I.TEXT))
                       .arrange(DOWN, buff=0.05)).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 1.4)
        src = source("USA Today CEO Forum, April 2007, as quoted by MacRumors; Apple Form 10-K; IDC")
        with self.voiceover(
            "Every part of this series ends its story with a forecast, and what became of it. <bookmark mark='a'/> In "
            "April 2007, two months before the first iPhone went on sale, the head of Microsoft was asked about it. "
            "There's no chance, he said, that the iPhone is going to get any significant market share. No chance. "
            "<bookmark mark='b'/> Apple sold 11.6 million iPhones in its 2008 fiscal year and 231 million in 2015. "
            "<bookmark mark='c'/> And yet, in a sense, he was half right. Apple's share of phones shipped has stayed "
            "around one in five. What he missed is the subject of this whole part: a fifth of the phones can be half "
            "of the money, and most of the profit."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(pa), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), run_time=2.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.1) for x in right], lag_ratio=0.5), run_time=2.4)
        self.clear_scene()

    def ours(self):
        c = calls(1, ours=True)[0]
        box = RoundedRectangle(corner_radius=0.16, width=11.6, height=3.6, stroke_color=I.ACCENT, stroke_width=2,
                               fill_color=I.PANEL, fill_opacity=1)
        body = VGroup(TB("This series' call", 26, I.ACCENT), T(f"logged {c.made}", 18, I.DIM),
                      T("Smartphones shipped worldwide in 2026 will be", 30, I.TEXT),
                      TB("below 1.15 billion", 40, I.MONEY),
                      T("(2025: 1.26 billion)  ·  scored on IDC's first full-year count, due January 2027", 18, I.DIM)
                      ).arrange(DOWN, buff=0.16).move_to(box)
        why = T("Why: shipments fell 7% in the second quarter and about 20% in the third, and memory makers expect "
                "the shortage to last.", 19, I.DIM).next_to(box, DOWN, buff=0.35)
        if why.width > 12.4:
            why.scale_to_fit_width(12.4)
        with self.voiceover(
            "This series also makes its own forecasts, writes down the date, and scores them later. <bookmark "
            "mark='a'/> Here is the first. Logged on the twenty-third of November 2026: smartphones shipped "
            "worldwide in 2026 will number fewer than 1.15 billion, against 1.26 billion in 2025. <bookmark "
            "mark='b'/> The reasoning is in this part: shipments fell about 7 percent in the second quarter and "
            "about a fifth in the third, and the memory makers do not expect the shortage to end soon. It will be "
            "scored on IDC's first count for the year, due in January 2027."
        ) as vo:
            self.play(FadeIn(box), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1:], shift=UP * 0.1), run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.clear_scene()
