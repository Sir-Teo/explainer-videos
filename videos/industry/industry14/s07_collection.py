from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

A_COL, B_COL = "#7BD88F", "#F2A65A"


class Collection(VoiceoverScene):
    def construct(self):
        card(self, 6, "The route", "Why does the second truck on a street lose money?",
             "Chapter six. The route.", lit=("make", "moat"))
        self.street()
        self.curve()
        self.money()

    def _street(self, n=12, y=0.6):
        road = Rectangle(width=13.6, height=0.7, stroke_width=0, fill_color="#2A2F38", fill_opacity=1).move_to([0, y - 0.55, 0])
        dash = DashedLine([-6.8, y - 0.55, 0], [6.8, y - 0.55, 0], stroke_color="#8B95A7", stroke_width=2, dash_length=0.15)
        houses = VGroup(*[draw.house(0.6, "#B9B2A3" if k % 2 else "#C9D3E0").move_to([-6.0 + 1.07 * k, y + 0.05, 0], aligned_edge=DOWN)
                          for k in range(n)])
        bins = VGroup(*[draw.wheelie_bin(0.38, A_COL, "#3D6B47").move_to(h.get_bottom() + RIGHT * 0.38 + DOWN * 0.02, aligned_edge=DOWN)
                        for h in houses])
        return road, dash, houses, bins

    def street(self):
        C = R["collection"]
        road, dash, houses, bins = self._street()
        lorry = draw.bin_lorry(1.3, A_COL).move_to([-7.6, 0.1, 0])
        clock = tx("one truck, the whole street", 22, WHITE, bold=True).to_edge(UP, buff=0.45)
        # second street, two haulers alternating
        road2, dash2, houses2, bins2 = self._street(y=-2.0)
        for k, b in enumerate(bins2):
            if k % 2:
                b.become(draw.wheelie_bin(0.38, B_COL, "#8A5A2B").move_to(b))
        l2a = draw.bin_lorry(1.3, A_COL).move_to([-7.6, -2.5, 0])
        l2b = draw.bin_lorry(1.3, B_COL).move_to([-7.6, -2.5, 0])
        lab1 = tx(f"about ${C['split']['1.0']['cost']:.2f} a stop", 18, A_COL, bold=True).next_to(road, DOWN, buff=0.12).shift(RIGHT * 4.5)
        lab2 = tx(f"about ${C['split']['0.5']['cost']:.2f} a stop, for each", 18, B_COL, bold=True).next_to(road2, DOWN, buff=0.12).shift(RIGHT * 4.3)
        head2 = tx("two haulers, alternate houses", 18, GREY_A).next_to(road2, UP, buff=1.2).to_edge(LEFT, buff=0.4)
        tag = estimate_tag("the Works' route: an illustration", corner=DR, size=12)

        with self.voiceover(
            "Now the other half: rubbish. Collection is a truck, a crew and a route. <bookmark mark='a'/> The truck "
            "costs much the same each day whether it stops at a hundred bins or a thousand. What it sells is stops, and "
            "the time between stops is wasted. <bookmark mark='b'/> On a street where one hauler has every house, the "
            "truck pulls up, tips a bin, rolls a few metres, tips the next. In the Works' version, that comes to about "
            f"${C['split']['1.0']['cost']:.2f} a stop. <bookmark mark='c'/> Now split the street between two haulers, "
            "taking alternate houses. Each truck still drives the whole street, but stops half as often. "
            f"<bookmark mark='d'/> Each pays about ${C['split']['0.5']['cost']:.2f} a stop: the same street, served twice, "
            "at a higher cost to everyone."
        ) as vo:
            self.play(FadeIn(road), FadeIn(dash), LaggedStart(*[FadeIn(h) for h in houses], lag_ratio=0.04), FadeIn(bins), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(clock), FadeIn(lorry))
            vo.wait_until("b")
            self.play(lorry.animate.move_to([7.4, 0.1, 0]), LaggedStart(*[Wiggle(b, scale_value=1.15) for b in bins], lag_ratio=0.15),
                      run_time=5.0, rate_func=linear)
            self.play(FadeIn(lab1))
            vo.wait_until("c")
            self.play(FadeIn(road2), FadeIn(dash2), FadeIn(houses2), FadeIn(bins2), FadeIn(head2))
            self.play(l2a.animate.move_to([7.4, -2.5, 0]),
                      LaggedStart(*[Wiggle(b, scale_value=1.15) for k, b in enumerate(bins2) if k % 2 == 0], lag_ratio=0.3),
                      run_time=4.0, rate_func=linear)
            self.play(l2b.animate.move_to([7.4, -2.5, 0]),
                      LaggedStart(*[Wiggle(b, scale_value=1.15) for k, b in enumerate(bins2) if k % 2 == 1], lag_ratio=0.3),
                      run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(lab2))
        self.clear_scene()

    def curve(self):
        C = R["collection"]
        pts = C["curve"]
        pa = viz.plot_axes([0.1, 1.0], [0, 2.6], x_length=6.6, y_length=4.2, xticks=[0.1, 0.25, 0.5, 0.75, 1.0], yticks=[0.5, 1.0, 1.5, 2.0, 2.5],
                           xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"${v:.2f}", ylabel="cost per stop", size=13).move_to([-3.2, -0.3, 0])
        xl = tx("share of the street's houses the hauler serves", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        ln = poly(pa, pts, PRICE, 4)
        price = DashedLine(pa.ax.c2p(0.1, C["price"]), pa.ax.c2p(1.0, C["price"]), stroke_color=GOOD, stroke_width=2, dash_length=0.08)
        price_l = tx(f"the price: ${C['price']:.2f} a stop", 15, GOOD, bold=True).next_to(pa.ax.c2p(1.0, C["price"]), UP, buff=0.08).align_to(price, RIGHT)
        rows = VGroup()
        for i, (k, n, lbl) in enumerate((("1.0", 1, "one hauler"), ("0.5", 2, "two haulers"), ("0.333", 3, "three haulers"))):
            p_ = C["split"][k]["profit"]
            y = 1.6 - 1.05 * i
            trucks = VGroup(*[draw.bin_lorry(0.55, [A_COL, B_COL, "#B58CFF"][j]) for j in range(n)]).arrange(RIGHT, buff=0.08)
            trucks.move_to([2.3, y, 0], aligned_edge=LEFT)
            txt = VGroup(tx(lbl, 16, WHITE, bold=True), tx(f"{'+' if p_ >= 0 else '-'}${abs(p_):,.0f} a day {'each' if n > 1 else ''}".strip(), 18,
                                                           GOOD if p_ > 0 else BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([4.6, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(trucks, txt))
        tag = estimate_tag("the Works' route: an illustration", corner=DR, size=12)
        with self.voiceover(
            "Draw the cost per stop against the hauler's share of the street. <bookmark mark='a'/> With every house, "
            f"about ${pts[-1][1]:.2f}. With half, about ${C['split']['0.5']['cost']:.2f}. With a tenth, more than two "
            f"dollars. <bookmark mark='b'/> Suppose the going price is ${C['price']:.2f} a stop. <bookmark mark='c'/> One "
            f"hauler with the whole street makes about ${C['split']['1.0']['profit']:,.0f} a day. Two haulers make about "
            f"${C['split']['0.5']['profit']:,.0f} each, much less than half as much between them. Three lose money. "
            "<bookmark mark='d'/> So the street tends to end up with one truck: either the town grants one hauler the "
            "whole district, or the haulers buy each other's customers until one is left. Density is the moat."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(price), FadeIn(price_l))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.1) for r_ in rows], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(rows[0], color=GOOD, scale_factor=1.05))
        self.clear_scene()

    def money(self):
        C = R["collection"]
        W = C["wm"]
        gr = C["garbage_real"]
        ppi = C["ppi"]
        pa = viz.plot_axes([1984, 2025], [0.8, 2.2], x_length=6.0, y_length=3.6, xticks=[1985, 1995, 2005, 2015, 2025], yticks=[1.0, 1.5, 2.0],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{v:.1f}", ylabel="price of rubbish collection, after inflation (1984 = 1)",
                           size=12).move_to([-3.4, 0.2, 0])
        ln = poly(pa, sorted(gr.items()), RECYCLE, 4)
        end = tx(f"x{gr[2025]:.2f}", 20, RECYCLE, bold=True).next_to(pa.ax.c2p(2025, gr[2025]), UP, buff=0.1)
        parts = [("commercial", W["commercial"]), ("industrial", W["industrial"]), ("homes", W["residential"]),
                 ("other collection", W["collection"] - W["commercial"] - W["industrial"] - W["residential"]),
                 ("landfill", W["landfill"]), ("transfer", W["transfer"]), ("recycling", W["recycling"]),
                 ("medical waste", W["health"]), ("energy and other", W["total"] - W["collection"] - W["landfill"] - W["transfer"] - W["recycling"] - W["health"])]
        cols = ["#5E9C6A", "#6FB07B", "#7BD88F", "#9FE3AE", LANDFILL, "#9AA3B2", "#5DA9E9", HAZ, "#5D6B82"]
        sc = 4.6 / W["total"]
        y = -1.9
        bar = VGroup()
        for (nm, v), col in zip(parts, cols):
            b = Rectangle(width=1.0, height=v * sc, stroke_color="#0E1117", stroke_width=1.5, fill_color=col, fill_opacity=0.95).move_to([2.6, y, 0], aligned_edge=DOWN)
            lab = tx(f"{nm} ${v:.1f}bn", 13, WHITE).next_to(b, RIGHT, buff=0.12)
            bar.add(VGroup(b, lab))
            y += v * sc
        bh = VGroup(tx(f"Waste Management, 2025: ${W['total']:.1f}bn", 17, WHITE, bold=True)).next_to(bar, UP, buff=0.15)
        esc = tx("its contracts: yearly price changes linked to the CPI, fuel or costs", 14, GREY_A).to_edge(DOWN, buff=0.7)
        src = source("BLS, CPI garbage and trash collection and all items; Waste Management, Form 10-K 2025 (net revenue by line of business)", size=13)
        with self.voiceover(
            "And the price? <bookmark mark='a'/> America's consumer price index for rubbish collection has doubled since "
            f"1984 after allowing for inflation: about {gr[2025]:.1f} times. <bookmark mark='b'/> Here is the biggest "
            f"hauler, Waste Management, with about ${W['total']:.0f} billion of revenue in 2025, after taking out what its "
            f"own trucks paid its own landfills. <bookmark mark='c'/> Collection is the bulk of it, about "
            f"${W['collection']:.0f} billion, from businesses, factories and homes. <bookmark mark='d'/> Its contracts with "
            "customers, it says, carry yearly price changes linked to the consumer price index, fuel or other costs. "
            "That is the steadiness: a price that follows costs up, on a route nobody else can serve as cheaply."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(VGroup(*[b_[0].copy().set_fill(opacity=0.15) for b_ in bar])))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            self.play(FadeIn(end))
            vo.wait_until("b")
            self.play(FadeIn(bh))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1])) for b_ in bar], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(esc, shift=UP * 0.1))
        self.clear_scene()
