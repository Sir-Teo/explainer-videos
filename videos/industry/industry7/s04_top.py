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
