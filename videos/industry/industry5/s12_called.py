from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 16, "Called it?", "Was Buffett right about airlines, and what will last?",
             "Chapter sixteen. Called it?", lit=("change",))
        self.airlines()
        self.ours()

    def airlines(self):
        A = R["air"]
        yrs, roc, wacc = A["years"], A["roc"], A["wacc"]
        ax = CornerAxes(x_range=[2014.5, 2025.5, 1], y_range=[-0.25, 0.25, 0.05], x_length=9.6, y_length=4.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([0.4, -0.45, 0])
        zero = DashedLine(ax.c2p(2014.5, 0), ax.c2p(2025.5, 0), stroke_color=GREY_C, stroke_width=1.5)
        xt = VGroup(*[tx(f"{y}", 15, GREY_B).next_to(ax.c2p(y, -0.25), DOWN, buff=0.08) for y in (2015, 2018, 2021, 2025)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(2014.5, v), LEFT, buff=0.08)
                      for v in (-0.2, -0.1, 0.1, 0.2)])
        cost = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_as_corners([ax.c2p(y, w) for y, w in zip(yrs, wacc)])
        cost_t = tx("cost of capital", 16, WHITE).next_to(ax.c2p(2025, wacc[-1]), UP, buff=0.1).shift(LEFT * 0.4)
        bars = VGroup()
        for y, v in zip(yrs, roc):
            h = ax.c2p(y, v)[1] - ax.c2p(y, 0)[1]
            bars.add(Rectangle(width=0.55, height=max(abs(h), 0.01), stroke_width=0, fill_color=RET if v > 0 else COST_,
                               fill_opacity=0.85).move_to(ax.c2p(y, 0), aligned_edge=DOWN if v >= 0 else UP))
        quote = VGroup(tx("“Think airlines. Here a durable competitive advantage has proven elusive", 21, WHITE),
                       tx("ever since the days of the Wright Brothers.”   Buffett, 2008", 21, WHITE)).arrange(
            DOWN, buff=0.06).to_edge(UP, buff=0.3)
        avg = VGroup(tx(f"average, 2015-2025: {100 * A['avg_roc']:.1f}% earned", 20, GOLD, bold=True),
                     tx(f"against {100 * A['avg_wacc']:.1f}% for the capital", 20, GOLD)).arrange(DOWN, buff=0.06).move_to(
            ax.c2p(2022.6, -0.17))
        jet = draw.plane(0.8, windows=False).move_to(ax.c2p(2014.5, 0.2))
        src = source("Berkshire Hathaway letter for 2007; Damodaran, Excess Returns by industry (Air Transport), "
                     "2015-2025", size=13)
        with self.voiceover(
            "Every part ends by scoring forecasts. This one has Buffett's. <bookmark mark='a'/> In 2008 he wrote that "
            "a durable advantage had proven elusive in airlines ever since the Wright brothers. "
            "<bookmark mark='b'/> Then the American airlines merged into a few big ones, and for a few years they "
            "earned well: fourteen to nineteen percent on their capital from 2015 to 2019, more than twice what it "
            "cost. <bookmark mark='c'/> Then came the pandemic, and two years of heavy losses. "
            "<bookmark mark='d'/> Since then, about eight percent. <bookmark mark='e'/> Across the eleven years, "
            f"airlines earned {100 * A['avg_roc']:.1f} percent a year on their capital, against a cost of "
            f"{100 * A['avg_wacc']:.1f}: hardly more than the capital could have earned anywhere else. Fewer, bigger "
            "airlines helped for a while; the five forces did the rest. Buffett called it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(jet))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=DOWN * 0.1), Create(ax), FadeIn(xt), FadeIn(yt), Create(zero))
            self.play(Create(cost), FadeIn(cost_t))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:5]], lag_ratio=0.2),
                      jet.animate.move_to(ax.c2p(2019.3, 0.21)), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in bars[5:7]], lag_ratio=0.3),
                      jet.animate.move_to(ax.c2p(2021, -0.23)).rotate(-0.5), run_time=1.6)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[7:]], lag_ratio=0.2),
                      jet.animate.rotate(0.5).move_to(ax.c2p(2025.3, 0.12)), run_time=1.8)
            vo.wait_until("e")
            self.play(FadeIn(avg, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        B = R["base_rate"]
        head = tx("This part's call", 30, GOLD, bold=True).to_edge(UP, buff=0.35)
        claim = tx("At least seven of the ten American industries with the highest return on capital in 2025\n"
                   "will still be among the twenty highest in 2028.", 25, WHITE).next_to(head, DOWN, buff=0.3)
        prob = tx("Probability: 75%.  Scored on Damodaran's table for 2028, due January 2029.", 20, GREY_A).next_to(
            claim, DOWN, buff=0.2)
        top10 = VGroup(*[tx(f"{k + 1}. {n}", 17, RET) for k, n in enumerate(B["top10_2025"])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.6, -1.6, 0])
        top_t = tx("the top ten, 2025", 18, GREY_A, bold=True).next_to(top10, UP, buff=0.15).align_to(top10, LEFT)
        dots = VGroup()
        for k, (y0, y1, hits) in enumerate(B["windows"]):
            row = VGroup(tx(f"{y0} to {y1}", 16, GREY_B),
                         VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=RET if i < hits else "#2A3446",
                                         fill_opacity=1) for i in range(10)]).arrange(RIGHT, buff=0.05)).arrange(
                RIGHT, buff=0.25)
            dots.add(row)
        dots.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.3, -1.75, 0])
        dots_t = tx("of each year's top ten, how many were top twenty three years later", 16, GREY_A).next_to(
            dots, UP, buff=0.15)
        src = source("Damodaran, Excess Returns by industry, 2015-2025; this film's count", corner=DR, size=13)
        with self.voiceover(
            "And this part's own call, built on how sticky those returns have been. <bookmark mark='a'/> At least "
            "seven of the ten American industries with the highest return on capital in 2025 will still be among "
            "the twenty highest in 2028. <bookmark mark='b'/> Here is the top ten: tobacco, computers, general "
            "insurance, home centers, household products and the rest. <bookmark mark='c'/> In Damodaran's tables "
            "since 2015, seven or more of a year's top ten were still in the top twenty three years later in seven "
            "of eight cases. The one miss started in 2022, when a commodity boom briefly lifted steel, paper, coal "
            "and oil into the top ten; none of them had a moat, and all four fell back. We put it "
            "at seventy-five percent, a little below that record, because the record is short and the next shock "
            "is never the last one. It will be scored on his table for 2028, published in January 2029."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(claim), FadeIn(prob))
            vo.wait_until("b")
            self.play(FadeIn(top_t), LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.1) for t_ in top10], lag_ratio=0.1),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(dots_t), LaggedStart(*[FadeIn(r_, shift=LEFT * 0.1) for r_ in dots], lag_ratio=0.15),
                      run_time=2.0)
        self.clear_scene()
