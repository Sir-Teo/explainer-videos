from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Prices(VoiceoverScene):
    def construct(self):
        card(self, 8, "Price and quantity", "Can a market grow while its dollars shrink?",
             "Chapter eight. Price and quantity.", lit=("unit", "dollar", "change"))
        self.area()
        self.chart()
        self.split()

    def area(self):
        """Dollars are an area: units along the bottom, price up the side."""
        u, p = ValueTracker(3.0), ValueTracker(2.0)
        corner = np.array([-5.6, -2.6, 0])

        def rect():
            return Rectangle(width=u.get_value(), height=p.get_value(), stroke_color=WHITE, stroke_width=2,
                             fill_color=GOLD, fill_opacity=0.35).move_to(corner, aligned_edge=DL)
        box = always_redraw(rect)
        w_lab = draw.memo_redraw(lambda: "units sold", lambda s: tx(s, 20, UNITS, bold=True),
                            lambda m: m.next_to(corner + [u.get_value() / 2, 0, 0], DOWN, buff=0.2))
        h_lab = draw.memo_redraw(lambda: "price", lambda s: tx(s, 20, GUESS, bold=True).rotate(PI / 2),
                            lambda m: m.next_to(corner + [0, p.get_value() / 2, 0], LEFT, buff=0.2))
        area = draw.number(lambda: 100 * u.get_value() * p.get_value() / 6.0, decimals=0, prefix="$", size=30,
                           color=GOLD)
        area.add_updater(lambda m: m.move_to(corner + [u.get_value() / 2, p.get_value() / 2, 0]))
        eq = MathTex(r"\text{dollars} = \text{units} \times \text{price}", font_size=40).move_to([3.2, 2.2, 0])
        lg = MathTex(r"\%\,\Delta\,\text{dollars} \approx \%\,\Delta\,\text{units} + \%\,\Delta\,\text{price}",
                     font_size=32, color=GREY_A).next_to(eq, DOWN, buff=0.35)
        tag = estimate_tag("illustrative: dollars start at 100", corner=DR, size=14)
        with self.voiceover(
            "A market measured in dollars is an area. <bookmark mark='a'/> Along the bottom, the number of units "
            "sold; up the side, the price of each. The dollars are the rectangle. Call it a hundred. "
            "<bookmark mark='b'/> Now let twice as many units be sold. <bookmark mark='c'/> And let the price halve. "
            "The rectangle changes shape completely, and its area, the market in dollars, is exactly where it "
            "started. <bookmark mark='d'/> So a market that is flat in dollars may be booming in units, or "
            "shrinking, and you cannot tell which from the dollars alone. To a first approximation, the growth in "
            "dollars is the growth in units plus the growth in price."
        ) as vo:
            self.play(FadeIn(tag), Write(eq))
            self.add(box, w_lab, h_lab)
            vo.wait_until("a")
            self.play(FadeIn(area))
            vo.wait_until("b")
            self.play(u.animate.set_value(6.0), run_time=2.0)
            vo.wait_until("c")
            self.play(p.animate.set_value(1.0), run_time=2.0)
            self.play(Indicate(area, color=WHITE))
            vo.wait_until("d")
            self.play(Write(lg))
        for m in (box, w_lab, h_lab, area):
            m.clear_updaters()
        self.clear_scene()

    def chart(self):
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
        ct = tx("what $100 of 2000's computing costs", 14, GREY_B).next_to(coins, DOWN, buff=0.12)
        src = source("BLS consumer price indexes via FRED: computers, peripherals and smart home assistants "
                     "(CUUR0000SEEE01); new vehicles (CUSR0000SETA01)", size=13)
        with self.voiceover(
            "Both halves move, and in some markets they move fast. <bookmark mark='a'/> Here is what American "
            "consumers paid for computers since 2000, as the Bureau of Labor Statistics measures it. The statisticians "
            "adjust for quality: a laptop that is twice as fast for the same price counts as a price cut. Measured "
            f"that way, the price fell by {abs(100 * P['comp_fall']):.0f} percent. What cost a hundred dollars in "
            f"2000 costs about {100 * (1 + P['comp_fall']):.0f} now. <bookmark mark='b'/> New cars, measured the same "
            "way, rose by about a quarter, less than prices in general. <bookmark mark='c'/> So the same dollar "
            "figure means very different things in different markets. A computer market that is flat in dollars has "
            "grown enormously in what it delivers. Sizing a market is two forecasts, not one: how many, and at what "
            "price. The quantity is often the easier half, because people and their habits change slowly. The price "
            "is set by costs, competition and technology: everything Parts 4 to 6 were about."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pc, shift=UP * 0.2), FadeIn(coins), FadeIn(ct), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(lc), run_time=2.4)
            self.play(FadeIn(tc), coins[1:].animate.set_opacity(0.15))
            vo.wait_until("b")
            self.play(Create(lk), run_time=2.0)
            self.play(FadeIn(tk))
            vo.wait_until("c")
            self.play(Indicate(lc, color=WHITE), Indicate(lk, color=WHITE))
        self.clear_scene()

    def split(self):
        C = R["census"]
        yrs, ship, real = C["years"], C["shipments"], C["real"]
        y0, y1 = yrs[0], yrs[-1]
        dol = ship[-1] / ship[0] - 1
        qty = real[-1] / real[0] - 1
        pri = (1 + dol) / (1 + qty) - 1
        corner = np.array([-5.2, -2.6, 0])
        s = 2.2
        r0 = Rectangle(width=s * 1.0, height=s * 1.0, stroke_color=GREY_B, stroke_width=2, fill_opacity=0).move_to(
            corner, aligned_edge=DL)
        r1 = Rectangle(width=s * (1 + qty), height=s * (1 + pri), stroke_color=WHITE, stroke_width=2, fill_color=GOLD,
                       fill_opacity=0.35).move_to(corner, aligned_edge=DL)
        l0 = tx(f"{y0}: ${ship[0]:.1f}bn", 18, GREY_B).move_to(r0)
        l1 = tx(f"{y1}: ${ship[-1]:.1f}bn", 18, GOLD, bold=True).next_to(r1, UP, buff=0.12).align_to(r1, RIGHT)
        wq = tx(f"units +{100 * qty:.0f}%", 18, UNITS, bold=True).next_to(r1, DOWN, buff=0.15)
        hp = tx(f"price +{100 * pri:.0f}%", 18, GUESS, bold=True).rotate(PI / 2).next_to(r1, LEFT, buff=0.15)
        bars = VGroup()
        for k, (lab, v, col) in enumerate((("dollars", dol, GOLD), ("price", pri, GUESS), ("quantity", qty, UNITS))):
            b = Rectangle(width=max(v, 0.005) * 14, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.9)
            t_ = tx(lab, 20, col, bold=True)
            n_ = tx(f"+{100 * v:.0f}%", 20, WHITE, bold=True)
            bars.add(VGroup(t_, b, n_))
        for k, g in enumerate(bars):
            g[0].move_to([1.2, 1.0 - 0.95 * k, 0], aligned_edge=RIGHT)
            g[1].next_to(g[0], RIGHT, buff=0.3).align_to([1.5, 0, 0], LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.2)
        head = tx(f"US bottled water at the factory gate, {y0} to {y1}", 22, WHITE, bold=True).to_edge(UP, buff=0.5)
        eqn = MathTex(rf"1.{100 * dol:02.0f} \approx 1.{100 * pri:02.0f} \times 1.{100 * qty:02.0f}", font_size=34,
                      color=GREY_A).next_to(bars, DOWN, buff=0.45)
        src = source("Census Bureau (AIES) shipments and BLS producer price index for bottled water, via FRED; this "
                     "film's division", size=13)
        with self.voiceover(
            "Now split a real market this way. <bookmark mark='a'/> American bottled-water plants shipped "
            f"{ship[0]:.1f} billion dollars of water in {y0}, and {ship[-1]:.1f} billion in {y1}. "
            f"<bookmark mark='b'/> Dollars up by {100 * dol:.0f} percent. <bookmark mark='c'/> The producer price index "
            f"for bottled water rose by {100 * pri:.0f} percent over the same years, most of it in the burst of "
            "inflation after 2021; before that, the price had been falling. <bookmark mark='d'/> Divide the one by "
            f"the other, and the quantity, the water itself, grew by only about {100 * qty:.0f} percent in twelve "
            "years. This is the gold line of Chapter 3, read as a rectangle: most of the market's growth in dollars "
            "was price. <bookmark mark='e'/> Whenever a company or a report tells you a market grew, ask the next "
            "question. Grew in what: in dollars of each year, in dollars of one year, or in things?"
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(r0), FadeIn(l0))
            self.play(TransformFromCopy(r0, r1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]), FadeIn(hp))
            vo.wait_until("d")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]), FadeIn(wq))
            self.play(Write(eqn))
            vo.wait_until("e")
            self.play(Indicate(bars[2], color=WHITE))
        self.clear_scene()
