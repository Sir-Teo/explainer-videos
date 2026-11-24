from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Prices(VoiceoverScene):
    def construct(self):
        card(self, 8, "Price and quantity", "Can a market grow while its dollars shrink?",
             "Chapter eight. Price and quantity.", lit=("unit", "dollar", "change"))
        P = R["prices"]
        yrs = P["years"]
        c0, k0 = P["computers"][0], P["cars"][0]
        comp = [100 * v / c0 for v in P["computers"]]
        cars = [100 * v / k0 for v in P["cars"]]
        pa = viz.plot_axes([yrs[0] - 0.5, yrs[-1] + 0.5], [0, 140], x_length=8.6, y_length=4.2,
                           xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[25, 50, 75, 100, 125],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}", size=15)
        pa.move_to([1.2, -0.5, 0])
        lc = VMobject(stroke_color=UNITS, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in zip(yrs, comp)])
        lk = VMobject(stroke_color=GUESS, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in zip(yrs, cars)])
        tc = tx(f"computers: {100 * P['comp_fall']:.0f}%", 18, UNITS, bold=True).next_to(pa.ax.c2p(yrs[-1], comp[-1]), UP,
                                                                                       buff=0.15).shift(LEFT * 0.8)
        tk = tx(f"new cars: +{100 * P['car_rise']:.0f}%", 18, GUESS, bold=True).next_to(pa.ax.c2p(yrs[-1], cars[-1]), UP,
                                                                                     buff=0.12).shift(LEFT * 0.8)
        head = tx(f"consumer prices, {yrs[0]} = 100, adjusted for quality", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(
            pa, LEFT)
        pc = VGroup(RoundedRectangle(corner_radius=0.06, width=1.3, height=0.85, stroke_width=0, fill_color="#2E3645",
                                     fill_opacity=1),
                    RoundedRectangle(corner_radius=0.04, width=1.1, height=0.65, stroke_width=0, fill_color="#5DA9E9",
                                     fill_opacity=0.7),
                    Rectangle(width=1.5, height=0.08, stroke_width=0, fill_color="#8C929B", fill_opacity=1).shift(
                        DOWN * 0.5)).move_to([-5.4, 1.8, 0])
        coins = VGroup(*[draw.coin(0.13) for _ in range(5)]).arrange(RIGHT, buff=0.04).next_to(pc, DOWN, buff=0.3)
        src = source("BLS consumer price indexes via FRED: computers, peripherals and smart home assistants "
                     "(CUUR0000SEEE01); new vehicles (CUSR0000SETA01)", size=13)
        with self.voiceover(
            "A market in dollars is units times price, and both of them move. <bookmark mark='a'/> Here is what "
            "American consumers paid for computers since 2000, as the statistical office measures it, adjusting for "
            f"how much better each year's machine is. The price fell by {abs(100 * P['comp_fall']):.0f} percent. "
            "<bookmark mark='b'/> New cars, measured the same way, rose by about a quarter. "
            "<bookmark mark='c'/> So the same dollar figure means very different things in different markets. A "
            "computer market that is flat in dollars has grown enormously in what it delivers. Sizing a market is "
            "two forecasts, not one: how many, and at what price. The quantity is often the easier half, because "
            "people and their habits change slowly. The price is set by costs, competition and technology, by "
            "everything Parts 4 to 6 were about."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pc, shift=UP * 0.2), FadeIn(coins), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(lc), run_time=2.4)
            self.play(FadeIn(tc), coins[1:].animate.set_opacity(0.15))
            vo.wait_until("b")
            self.play(Create(lk), run_time=2.0)
            self.play(FadeIn(tk))
            vo.wait_until("c")
            self.play(Indicate(lc, color=WHITE), Indicate(lk, color=WHITE))
        self.clear_scene()
