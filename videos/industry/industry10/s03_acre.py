from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403

SHORT = {"Seed": "seed", "Fertilizer": "fertilizer", "Chemicals": "chemicals", "Custom services": "hired services",
         "Fuel, lube, and electricity": "fuel and power", "Repairs": "repairs", "Interest on operating capital": "interest",
         "Purchased irrigation water": "water", "Hired labor": "hired labour",
         "Opportunity cost of unpaid labor": "the family's own labour",
         "Capital recovery of machinery and equipment": "machinery", "Opportunity cost of land": "land",
         "Taxes and insurance": "taxes and insurance", "General farm overhead": "general overhead"}


class Acre(VoiceoverScene):
    def construct(self):
        card(self, 2, "An acre's arithmetic", "What does it cost to grow an acre of corn, and what is left?",
             "Chapter two. An acre's arithmetic.", lit=("unit", "dollar"))
        self.waterfall()
        self.residual()
        self.history()

    def waterfall(self):
        A = R["acre"]
        items = [(SHORT[k], v, COST) for k, v in A["operating"].items() if v >= 20]
        items = sorted(items, key=lambda q: -q[1])
        items += sorted([(SHORT[k], v, LAND if k == "Opportunity cost of land" else "#6F8FB8")
                         for k, v in A["overhead"].items() if v >= 20], key=lambda q: -q[1])
        small = A["cost"] - sum(v for _, v, _ in items)
        items.append(("everything else", small, GREY_B))
        top = A["revenue"]
        pa = viz.plot_axes([-0.7, len(items) + 1.7], [-200, 900], x_length=11.6, y_length=4.6, xticks=[],
                           yticks=[0, 200, 400, 600, 800], yfmt=lambda v: f"${v:g}", size=14).move_to([0.3, -0.55, 0])
        zero = Line(pa.ax.c2p(-0.7, 0), pa.ax.c2p(len(items) + 1.7, 0), stroke_color=GREY_B, stroke_width=1.2)
        bars = VGroup()
        rev = Rectangle(width=0.6, height=pa.ax.c2p(0, top)[1] - pa.ax.c2p(0, 0)[1], stroke_width=0, fill_color=CORN,
                        fill_opacity=0.9).move_to(pa.ax.c2p(0, 0), aligned_edge=DOWN)
        rl = VGroup(tx(f"${top:.0f}", 15, WHITE, bold=True).next_to(rev, UP, buff=0.06),
                    VGroup(tx("the crop", 13, CORN), tx(f"{A['yield_bu']:.0f} bu x ${A['price']:.2f}", 12, GREY_A)
                           ).arrange(DOWN, buff=0.02).next_to(pa.ax.c2p(0, -200), UP, buff=0.05))
        level = top
        for i, (name, v, col) in enumerate(items, start=1):
            y0, y1 = level, level - v
            b = Rectangle(width=0.6, height=pa.ax.c2p(0, y0)[1] - pa.ax.c2p(0, y1)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.9).move_to([pa.ax.c2p(i, 0)[0], (pa.ax.c2p(0, y0)[1] + pa.ax.c2p(0, y1)[1]) / 2, 0])
            lab = VGroup(tx(f"-{v:.0f}", 13, WHITE, bold=True), tx(name, 12, GREY_A)).arrange(
                DOWN, buff=0.02, aligned_edge=LEFT).next_to(b, RIGHT, buff=0.06)
            bars.add(VGroup(b, lab))
            level = y1
        other = top - sum(v for _, v, _ in items) - A["cost"] + A["cost"]
        net = A["revenue"] - A["cost"]
        nb = Rectangle(width=0.6, height=abs(pa.ax.c2p(0, net)[1] - pa.ax.c2p(0, 0)[1]), stroke_width=0, fill_color=STATE,
                       fill_opacity=0.9).move_to([pa.ax.c2p(len(items) + 1, 0)[0],
                                                  (pa.ax.c2p(0, 0)[1] + pa.ax.c2p(0, net)[1]) / 2, 0])
        nl = VGroup(tx(f"-${abs(net):.0f}", 16, STATE, bold=True).next_to(nb, DOWN, buff=0.06),
                    tx("what is left", 13, STATE).next_to(pa.ax.c2p(len(items) + 1, -200), UP, buff=0.05))
        del other
        head = tx(f"One acre of corn, {A['year']}: dollars", 24, WHITE, bold=True).to_edge(UP, buff=0.35)
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color=COST, fill_opacity=1), tx("operating costs", 14, WHITE)
                            ).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.18, stroke_width=0, fill_color="#6F8FB8", fill_opacity=1),
                            tx("machinery, labour, overhead", 14, WHITE)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.18, stroke_width=0, fill_color=LAND, fill_opacity=1), tx("land", 14, WHITE)
                            ).arrange(RIGHT, buff=0.08)).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.15)
        src = source(f"USDA ERS, commodity costs and returns, corn, {A['year']}, US total, per planted acre", size=13)
        with self.voiceover(
            "Now look inside one acre of that farm, with the Department of Agriculture's own accounts for corn in "
            f"{A['year']}. <bookmark mark='a'/> An acre grew about {A['yield_bu']:.0f} bushels, and at harvest a bushel "
            f"sold for {say_money(A['price'])}, so the crop was worth about {A['revenue']:.0f} dollars. "
            "<bookmark mark='b'/> Then the bills. Fertilizer, mostly nitrogen, is the biggest operating cost, about "
            f"{A['operating']['Fertilizer']:.0f} dollars an acre. Seed, much of it genetically engineered and patented, "
            f"about {A['operating']['Seed']:.0f}. Then chemicals, repairs, hired services and fuel. "
            "<bookmark mark='c'/> Then the costs of what the farmer owns: the machinery wearing out, about "
            f"{A['overhead']['Capital recovery of machinery and equipment']:.0f} dollars an acre, and the land itself, "
            f"valued at what it could be rented for, {A['land']:.0f}. Then the family's own work, taxes and overheads. "
            f"<bookmark mark='d'/> Add it all up, and the acre cost about {A['cost']:.0f} dollars to grow. It lost "
            f"{abs(net):.0f}."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(head), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(GrowFromEdge(rev, DOWN), FadeIn(rl))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], UP), FadeIn(b[1:])) for b in bars[:6]],
                                  lag_ratio=0.35), run_time=3.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], UP), FadeIn(b[1:])) for b in bars[6:]],
                                  lag_ratio=0.35), run_time=3.0)
            vo.wait_until("d")
            self.play(GrowFromEdge(nb, UP), FadeIn(nl))
            self.play(Indicate(nl[0], color=STATE, scale_factor=1.2))
        self.clear_scene()

    def residual(self):
        A = R["acre"]
        steps = [("the crop", A["revenue"]), ("after operating costs", A["net_op"]),
                 ("after the machinery", A["net_op"] - A["overhead"]["Capital recovery of machinery and equipment"]),
                 ("after the land's rent", A["net_op"] - A["overhead"]["Capital recovery of machinery and equipment"]
                  - A["land"]),
                 ("after the family's work and overheads", A["net"])]
        blocks = VGroup()
        for i, (lab, v) in enumerate(steps):
            h = abs(v) / 800 * 3.2
            b = Rectangle(width=1.6, height=max(h, 0.02), stroke_width=0, fill_color=CORN if v >= 0 else STATE,
                          fill_opacity=0.9)
            b.move_to([-5.2 + 2.6 * i, -0.6, 0], aligned_edge=DOWN if v >= 0 else UP)
            l1 = VGroup(*[tx(w, 15, GREY_A) for w in lab.split(" and ")]).arrange(DOWN, buff=0.02)
            lab_g = VGroup(tx(f"{'-' if v < 0 else ''}${abs(v):.0f}", 20, WHITE, bold=True), l1).arrange(DOWN, buff=0.06)
            lab_g.next_to(b, UP if v >= 0 else DOWN, buff=0.1)
            blocks.add(VGroup(b, lab_g))
        base = Line([-6.4, -0.6, 0], [6.4, -0.6, 0], stroke_color=GREY_B, stroke_width=1.2)
        arrows = VGroup(*[Arrow(blocks[i][0].get_right() + UP * 0.2, blocks[i + 1][0].get_left() + UP * 0.2, buff=0.1,
                                stroke_width=2, color=GREY_B, tip_length=0.12) for i in range(4)])
        be = VGroup(tx("Break-even price a bushel:", 19, WHITE, bold=True),
                    tx(f"${A['breakeven_op']:.2f} to cover the operating costs", 18, COST),
                    tx(f"${A['breakeven']:.2f} to cover everything", 18, STATE),
                    tx(f"the price was ${A['price']:.2f}", 18, CORN, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06
                                                                                        ).to_edge(UP, buff=0.4)
        src = source(f"USDA ERS, commodity costs and returns, corn, {A['year']}; computed, the Works (farm.py)", size=13)
        with self.voiceover(
            "So why plant at all? Follow the money in the order it is paid. <bookmark mark='a'/> The crop brings in "
            f"{A['revenue']:.0f} dollars. <bookmark mark='b'/> Seed, fertilizer and the other operating costs must be "
            f"paid in cash, and leave {A['net_op']:.0f}. <bookmark mark='c'/> The machinery is already bought; "
            "its wear is real but it is paid for. <bookmark mark='d'/> The land is the farmer's own, or rented on a "
            "contract that runs for the year. <bookmark mark='e'/> And the farmer's own time is paid last, with "
            f"whatever is left, which this year was less than nothing. <bookmark mark='f'/> A bushel needed "
            f"{say_money(A['breakeven_op'])} to cover the cash costs, and {say_money(A['breakeven'])} to cover everything. "
            f"It sold for {say_money(A['price'])}. So the farmer plants: every acre covers its cash costs and pays "
            "something towards the machinery and the land. It is Part four's cost curve again. In the short run, a "
            "producer keeps going as long as the price beats the cost of the next unit. The land, the machines and the "
            "family's labour are what absorb the bad years."
        ) as vo:
            self.play(Create(base), FadeIn(src))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                anims = [GrowFromEdge(blocks[k][0], DOWN if steps[k][1] >= 0 else UP), FadeIn(blocks[k][1])]
                if k:
                    anims.append(GrowArrow(arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(be, shift=DOWN * 0.1))
        self.clear_scene()

    def history(self):
        A = R["acre"]
        cols = {"corn": CORN, "soybeans": SOY, "wheat": WHEATC}
        pa = viz.plot_axes([1995.4, 2025.6], [-250, 250], x_length=10.6, y_length=4.4, xticks=[1996, 2000, 2005, 2010, 2015,
                                                                                                  2020, 2025],
                           yticks=[-200, -100, 0, 100, 200], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:+g}" if v else "$0",
                           ylabel="return over all costs, dollars an acre", size=14).move_to([-0.5, -0.45, 0])
        zero = Line(pa.ax.c2p(1995.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for j, crop in enumerate(cols):
            g = VGroup()
            for y, v in A["net_series"][crop].items():
                if v is None:
                    continue
                v = max(min(v, 249), -249)
                x = y + (j - 1) * 0.28
                p0, p1 = pa.ax.c2p(x, 0), pa.ax.c2p(x, v)
                g.add(Rectangle(width=0.26, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=cols[crop],
                                fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
            bars.add(g)
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=c, fill_opacity=1),
                              tx(f"{crop}: below zero in {A['losing_years'][crop]} of {A['n_years'][crop]} years", 15, WHITE)
                              ).arrange(RIGHT, buff=0.08) for crop, c in cols.items()]).arrange(RIGHT, buff=0.45).next_to(
            pa, UP, buff=0.15)
        head = tx("Thirty years of returns over all costs, per acre", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("USDA ERS, commodity costs and returns, US totals, 1996-2025 (values beyond $250 are clipped)", size=13)
        with self.voiceover(
            "And this is not a bad year. <bookmark mark='a'/> Here are thirty years of the same accounts for corn, "
            "soybeans and wheat. Count the bars below the line. <bookmark mark='b'/> By the Department of "
            f"Agriculture's full accounting, corn failed to cover all its costs in {A['losing_years']['corn']} of "
            f"{A['n_years']['corn']} years, soybeans in {A['losing_years']['soybeans']}, and wheat in "
            f"{A['losing_years']['wheat']} of {A['n_years']['wheat']}. <bookmark mark='c'/> The good years are the "
            "spikes: 2008, 2011 to 2013, 2021 and 2022, when droughts, biofuel mandates or wars sent prices up. A loss "
            "in these accounts does not mean the farm goes bust. It means the land and the family's work earned less "
            "than they could have earned elsewhere: the farm survives by paying its owners less than the market rate. "
            "That is the first clue to this part's question."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] > pa.ax.c2p(0, 0)[1] else UP)
                                    for g in bars for b in g], lag_ratio=0.01), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(key))
        self.clear_scene()
