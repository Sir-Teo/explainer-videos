from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        C = [c for c in R["capex"] if c["fy"] >= 2010]
        yrs = [c["fy"] for c in C]
        pa = viz.plot_axes((2009.4, 2026.6), (0, 200), x_length=10.6, y_length=4.6,
                           xticks=[2010, 2014, 2018, 2022, 2026], yticks=[0, 50, 100, 150, 200],
                           xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"${v:.0f}bn", size=16).shift(DOWN * 0.45)
        bars = viz.year_bars(pa, yrs, [c["capex"] for c in C], CO["msft"], width=0.62)
        pts = [(c["fy"], c["ocf"]) for c in C if c["ocf"]]
        line = VMobject(stroke_color=I.MONEY, stroke_width=3).set_points_as_corners([pa.ax.c2p(x, v) for x, v in pts])
        dots = VGroup(*[Dot(pa.ax.c2p(x, v), color=I.MONEY, radius=0.045) for x, v in pts])
        lb = VGroup(Square(0.22, fill_color=CO["msft"], fill_opacity=0.9, stroke_width=0),
                    T("spent on data centres, equipment and buildings", 18, CO["msft"])).arrange(RIGHT, buff=0.12)
        ll = VGroup(Line(LEFT * 0.12, RIGHT * 0.12, color=I.MONEY, stroke_width=4), T("cash from operations", 18,
                                                                                         I.MONEY)).arrange(RIGHT, buff=0.12)
        VGroup(lb, ll).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(pa.ax.c2p(2010.2, 180), aligned_edge=UL)
        first, last = C[0], C[-1]
        head = T("Intermission: Microsoft's capital spending by fiscal year", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = source("Microsoft Forms 10-K via SEC company facts (fiscal years to June; 2014-15 operating cash not "
                     "tagged)", size=13)
        with self.voiceover(
            "An intermission. For most of its history Microsoft was the model of a business that needs almost no "
            f"capital: in fiscal {first['fy']} it spent {say_bn(first['capex'])} on buildings and equipment. "
            "<bookmark mark='a'/> Then came the cloud, and the spending grew year after year. <bookmark mark='b'/> "
            f"And then artificial intelligence: {say_bn(last['capex'])} in fiscal {last['fy']}, about sixty times as "
            "much, and the company has said it will spend more in the year after. The gold line is the cash its "
            "business brings in. The gap between them has closed fast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            self.play(GrowFromEdge(bars[0], DOWN))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:13]], lag_ratio=0.15), FadeIn(lb),
                      run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[13:]], lag_ratio=0.3), run_time=2)
            self.play(Create(line), FadeIn(dots), FadeIn(ll), run_time=2)
        self.clear_scene()
        self.story()

    def story(self):
        so = VGroup(TB("The story so far", 34, I.ACCENT),
                    T("Every transaction is written twice, so the balance sheet always balances.", 24, I.TEXT),
                    T("The income statement says how much of each dollar of sales a company keeps.", 24, I.TEXT),
                    T("The balance sheet says what it owns, and whose money paid for it.", 24, I.TEXT),
                    T("The cash-flow statement says whether the profit turned into money.", 24, I.TEXT),
                    T("Next: speed, margin and borrowing, and whether a business earns its keep.", 21, I.DIM)
                    ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The story so far. Every transaction is written twice, so the balance sheet always balances. The income "
            "statement says how much of each dollar of sales a company keeps. The balance sheet says what it owns, "
            "and whose money paid for it. And the cash-flow statement says whether the profit turned into money. "
            "Next: how speed, margin and borrowing combine, and whether a business earns its keep."
        ):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in so], lag_ratio=0.5), run_time=5)
        self.clear_scene()
