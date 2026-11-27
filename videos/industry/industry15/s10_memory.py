from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

MEM = GROUP_COL["memory"]


class Memory(VoiceoverScene):
    def construct(self):
        card(self, 8, "Memory", "Why does the memory business swing from famine to feast?",
             "Chapter eight. Memory.", lit=("change", "dollar"))
        self.micron()
        self.market()
        self.spending()

    def micron(self):
        M = R["memory"]
        q = M["mu"]
        def xq(s):
            return int(s[:4]) + (int(s[5:7]) - 0.5) / 12
        pa = viz.plot_axes([2008.5, 2027], [-5, 56], x_length=10.0, y_length=4.6, xticks=[2010, 2013, 2016, 2019, 2022, 2026],
                           yticks=[0, 10, 20, 30, 40, 50], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="Micron, each quarter", size=13).move_to([-0.6, -0.5, 0])
        rev = VGroup()
        oi = VGroup()
        for s, r_, o in q:
            x = pa.ax.c2p(xq(s), 0)
            rev.add(Rectangle(width=0.08, height=max(pa.ax.c2p(0, r_)[1] - pa.ax.c2p(0, 0)[1], 0.01), stroke_width=0, fill_color=MEM, fill_opacity=0.55).move_to(x, aligned_edge=DOWN))
            h = pa.ax.c2p(0, abs(o))[1] - pa.ax.c2p(0, 0)[1]
            oi.add(Rectangle(width=0.08, height=max(h, 0.01), stroke_width=0, fill_color=GOOD if o >= 0 else BAD, fill_opacity=0.95).move_to(
                x, aligned_edge=DOWN if o >= 0 else UP).shift(RIGHT * 0.09))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=MEM, fill_opacity=0.55), tx("revenue", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color=GOOD, fill_opacity=0.95), tx("operating profit", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color=BAD, fill_opacity=0.95), tx("operating loss", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.4).move_to([-1.5, 2.75, 0])
        low = M["mu_low"]
        last = M["mu_last"]
        l1 = tx(f"early 2023: -${abs(low[2]):.1f}bn", 15, BAD, bold=True).next_to(pa.ax.c2p(xq(low[0]), low[2]), DOWN, buff=0.1).shift(LEFT * 0.4)
        l2 = VGroup(tx(f"quarter to September 2026:", 14, GREY_A), tx(f"${last[1]:.1f}bn revenue, ${last[2]:.1f}bn operating profit", 15, GOOD, bold=True)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.04).next_to(pa.ax.c2p(xq(last[0]), last[1]), LEFT, buff=0.2)
        src = source("SEC EDGAR: Micron Technology, Forms 10-Q and 10-K (three-month revenue and operating income), 2008-2026", size=13)
        with self.voiceover(
            "Memory chips are different. One maker's memory does much the same job as another's, so they sell close to "
            "a commodity, at whatever the market pays. <bookmark mark='a'/> Here is Micron, America's memory maker, "
            "quarter by quarter since 2008. <bookmark mark='b'/> In the bad years it loses money: "
            f"in early 2023 it lost about ${abs(low[2]):.1f} billion in a single quarter. <bookmark mark='c'/> And then "
            f"this: in the quarter to September 2026, ${last[1]:.0f} billion of revenue, and ${last[2]:.0f} billion of "
            "operating profit, eight dollars in every ten. The same factories, the same kind of product: only the price "
            "changed."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in rev], lag_ratio=0.01), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in oi], lag_ratio=0.01), run_time=2.5)
            self.play(FadeIn(l1))
            vo.wait_until("c")
            self.play(FadeIn(l2, shift=LEFT * 0.1))
        self.clear_scene()

    def market(self):
        M = R["memory"]["wsts"]
        order = [(2022, "2022"), (2023, "2023"), (2024, "2024"), (2025, "2025"), ("2026f", "2026, forecast")]
        sc = 4.4 / 850
        bars = VGroup()
        for i, (k, lab) in enumerate(order):
            v = M[k]
            b = Rectangle(width=1.0, height=v * sc, stroke_width=0, fill_color=MEM, fill_opacity=0.9 if k != "2026f" else 0.5).move_to(
                [-4.6 + 1.6 * i, -2.3, 0], aligned_edge=DOWN)
            if k == "2026f":
                b.set_stroke(MEM, 2)
            bars.add(VGroup(b, tx(f"${v:,.0f}bn", 16, WHITE, bold=True).next_to(b, UP, buff=0.08), tx(lab, 14, GREY_A).next_to(b, DOWN, buff=0.08)))
        head = tx("World sales of memory chips", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        side = VGroup(tx("WSTS, May 2026:", 15, GREY_A), tx("memory +250% in 2026,", 18, MEM, bold=True),
                      tx("driven by 'AI infrastructure,", 14, GREY_A), tx("high-bandwidth memory (HBM)'", 14, GREY_A),
                      tx("first half of 2026: +305%", 16, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 0.6, 0])
        src = source("World Semiconductor Trade Statistics: Fall 2023 and Autumn 2025 forecasts (2022-2024), Spring 2026 forecast "
                     "(2025, 2026), Q2 2026 release", size=13)
        with self.voiceover(
            "Across the whole industry: <bookmark mark='a'/> the world bought about "
            f"${M[2022]:.0f} billion of memory chips in 2022, and about ${M[2023]:.0f} billion in 2023, when prices "
            f"collapsed. <bookmark mark='b'/> Then ${M[2024]:.0f} billion, and ${M[2025]:.0f} billion in 2025. "
            "<bookmark mark='c'/> For 2026 the industry's own statisticians forecast more than "
            f"${M['2026f']:,.0f} billion, three and a half times as much, driven, they said, by AI infrastructure and the "
            "high-bandwidth memory that feeds AI chips. In the first half of 2026 memory sales were up 305 per cent. "
            "If every maker builds new factories in a boom like this, the factories open together, and that is how a "
            "famine starts: the cycle of Part six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[2]) for b_ in bars], FadeIn(ghost(*[b_[0] for b_ in bars])))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]), GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[4][0], DOWN), FadeIn(bars[4][1]), run_time=2.0)
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()

    def spending(self):
        M = R["memory"]["mu_capex"]
        ys = sorted(M)
        pa = viz.plot_axes([2009.4, 2026.6], [0, 34], x_length=9.0, y_length=4.4, xticks=[2010, 2014, 2018, 2022, 2026],
                           yticks=[10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="Micron: spent on fabs and tools, each fiscal year", size=13).move_to([-1.0, -0.4, 0])
        bars = VGroup()
        for y in ys:
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            rev, cap = M[y]
            bars.add(Rectangle(width=0.36, height=pa.ax.c2p(y, cap)[1] - y0, stroke_width=0, fill_color="#F2A65A", fill_opacity=0.9).move_to(
                [x0, y0, 0], aligned_edge=DOWN))
        notes = VGroup()
        for y, txt in ((2016, "a bust"), (2023, "a bust"), (2026, "a boom")):
            rev, cap = M[y]
            notes.add(tx(f"{y}: {100 * cap / rev:.0f}% of revenue", 14, PRICE if y == 2026 else GREY_A, bold=True).next_to(
                bars[ys.index(y)], UP, buff=0.12))
        notes[1].shift(UP * 0.75 + RIGHT * 0.2)
        r23, c23 = M[2023]
        r26, c26 = M[2026]
        src = source("SEC EDGAR: Micron Technology, Forms 10-K (purchases of property, plant and equipment; revenue), fiscal 2010-2026", size=13)
        with self.voiceover(
            "And through the swings, the spending does not stop. <bookmark mark='a'/> Here is what Micron spent on fabs and "
            "tools, year by year. <bookmark mark='b'/> In the bust of fiscal 2023 its revenue fell to about "
            f"${r23:.0f} billion, and it still spent about ${c23:.1f} billion, {100 * c23 / r23:.0f} cents of every dollar it "
            "took in: a memory maker that stops shrinking its cells falls behind. <bookmark mark='c'/> In fiscal 2026, with "
            f"prices soaring, it spent about ${c26:.0f} billion. That capacity will arrive whatever prices are by then, which "
            "is how a memory boom plants the seeds of the next bust."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(bars, opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(bars[ys.index(2023)], color=PRICE), FadeIn(notes[:2]))
            vo.wait_until("c")
            self.play(Indicate(bars[ys.index(2026)], color=PRICE), FadeIn(notes[2]))
        self.clear_scene()
