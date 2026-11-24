from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Top(VoiceoverScene):
    def construct(self):
        card(self, 3, "Top-down: the census", "What do the statistical offices count, and when do they tell you?",
             "Chapter three. Top-down: the census.", lit=("unit",))
        C = R["census"]
        yrs, ship, real = C["years"], C["shipments"], C["real"]
        pa = viz.plot_axes([2011.5, 2024.5], [0, 10], x_length=8.4, y_length=3.8, xticks=[2012, 2015, 2018, 2021, 2024],
                           yticks=[2.5, 5, 7.5, 10], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([1.4, -0.5, 0])
        bars = viz.year_bars(pa, yrs, ship, FACTORY, width=0.5)
        rl = VMobject(stroke_color=GOLD, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(y, v) for y, v in zip(yrs, real)])
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=FACTORY, fill_opacity=1),
                            tx("shipments, dollars of each year", 16, FACTORY)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, stroke_color=GOLD, stroke_width=3),
                            tx(f"at {yrs[0]} prices (deflated by the producer price index)", 16, GOLD)).arrange(
                         RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(pa, UP, buff=0.15).align_to(
            pa, LEFT)
        forms = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.55, height=0.72, stroke_width=0,
                                          fill_color="#E8E4DA", fill_opacity=1).shift(RIGHT * 0.08 * k + UP * 0.06 * k)
                         for k in range(5)]).move_to([-5.4, 1.4, 0])
        fl = VGroup(tx("Economic Census: every 5 years", 16, GREY_A), tx("annual survey in between", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).next_to(forms, DOWN, buff=0.2)
        lag = VGroup(tx("the 2022 census's", 16, GREY_B), tx("concentration tables:", 16, GREY_B),
                     tx("released April 2025", 18, "#E8554E", bold=True)).arrange(DOWN, buff=0.04).move_to([-5.3, -1.8, 0])
        src = source("US Census Bureau: Annual Integrated Economic Survey (via FRED, AIES312112RCTUS); BLS producer "
                     "price index for bottled water (PCU312112312112)", size=13)
        i20, i24 = yrs.index(2020), yrs.index(2024)
        with self.voiceover(
            "The top-down way starts with what governments count. <bookmark mark='a'/> Every five years America "
            "takes an Economic Census, of every business with employees, and in between the Census Bureau surveys "
            "a sample of companies every year, asking what each of their plants shipped. "
            f"<bookmark mark='b'/> Here is the answer since {yrs[0]}: from {ship[0]:.1f} billion dollars to "
            f"{ship[-1]:.1f} billion in {yrs[-1]}, made by about {C['employees']:,.0f} people. <bookmark mark='c'/> "
            "But some of that rise is only prices. Producer prices for bottled water rose by about a third between "
            f"2020 and 2023. Take out the price rises and the gold line is what was really shipped, at {yrs[0]} "
            "prices: much flatter. <bookmark mark='d'/> Top-down numbers are careful, consistent from year to year, "
            "and late. The concentration tables from the 2022 census, which Part 5 used, came out in April 2025. "
            "And they are only as good as the definitions behind them, which, as the last chapter showed, may not "
            "be the ones your question needs."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(f_, shift=UP * 0.1) for f_ in forms], lag_ratio=0.15),
                      FadeIn(pa), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(fl), Indicate(forms, color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeIn(key[0]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08),
                      run_time=2.2)
            vo.wait_until("c")
            self.play(FadeIn(key[1]), Create(rl), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(lag, shift=UP * 0.1))
        self.clear_scene()
        self.primary()

    def primary(self):
        """The census files plants, not products: each plant under what it mainly makes."""
        def plant(x, col, mix, name, filed):
            f = draw.factory(2.2, color=col).move_to([x, 1.3, 0])
            pie = VGroup()
            a0 = PI / 2
            for share, c_ in mix:
                pie.add(AnnularSector(inner_radius=0, outer_radius=0.62, angle=-TAU * share, start_angle=a0,
                                      fill_color=c_, fill_opacity=0.95, stroke_color="#0E1117", stroke_width=2))
                a0 -= TAU * share
            pie.move_to([x, -0.6, 0])
            lab = tx(name, 18, WHITE, bold=True).next_to(f, UP, buff=0.12)
            fl = VGroup(tx("filed as:", 15, GREY_B), tx(filed, 18, GOLD, bold=True)).arrange(DOWN, buff=0.04).next_to(
                pie, DOWN, buff=0.25)
            return VGroup(f, lab, pie, fl)
        BEER, H2O, TEA = "#E0A43A", WATER, "#9C6B3F"
        a_ = plant(-3.3, "#C9A26B", [(0.7, BEER), (0.3, H2O)], "a brewery", "brewery: all of it")
        b_ = plant(3.3, "#8FB8DE", [(0.8, H2O), (0.2, TEA)], "a water plant", "bottled water: all of it")
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c_, fill_opacity=1), tx(n_, 15, GREY_A)).arrange(
            RIGHT, buff=0.08) for n_, c_ in (("beer", BEER), ("water", H2O), ("iced tea", TEA))]).arrange(
            RIGHT, buff=0.4).to_edge(DOWN, buff=0.85)
        miss = tx("its water is not in bottled water's total", 16, "#E8554E").next_to(a_, DOWN, buff=0.15)
        extra = tx("its tea is", 16, "#E8554E").next_to(b_, DOWN, buff=0.15)
        tag = estimate_tag("illustrative plants and shares", corner=DR, size=14)
        src = source("US Census Bureau, NAICS classification of establishments by primary activity", size=13)
        with self.voiceover(
            "Chapter 2 said the census files each plant under what it mainly makes. Here is what that does. "
            "<bookmark mark='a'/> The census counts plants, not products. A brewery that also bottles some water is a brewery, and all of its water is counted as "
            "brewery shipments. <bookmark mark='b'/> A water plant that also makes some iced tea is a water plant, "
            "and its tea is counted as water. <bookmark mark='c'/> So an industry's total is the output of the plants "
            "filed under it, not the market for the product in its name. The two errors partly cancel, by an amount "
            "nobody can see in the totals. Every five years, the Economic Census also reports shipments product by "
            "product, which is closer to a market; in the years between, you have the plants."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), FadeIn(key), FadeIn(a_[0], shift=UP * 0.2), FadeIn(a_[1]))
            vo.wait_until("a")
            self.play(*[DrawBorderThenFill(w) for w in a_[2]], FadeIn(a_[3]))
            self.play(FadeIn(miss), Indicate(a_[2][1], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(b_[0], shift=UP * 0.2), FadeIn(b_[1]))
            self.play(*[DrawBorderThenFill(w) for w in b_[2]], FadeIn(b_[3]))
            self.play(FadeIn(extra), Indicate(b_[2][1], color=WHITE))
            vo.wait_until("c")
            self.play(Circumscribe(VGroup(a_[2], b_[2]), color=GOLD, time_width=0.8))
        self.clear_scene()
