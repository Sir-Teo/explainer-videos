from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Dispatch(VoiceoverScene):
    def construct(self):
        card(self, 4, "The merit order", "Which plants run, and who sets the price?", "Chapter four. The merit order.",
             lit=("make", "dollar"))
        self.day()
        self.order()
        self.gas()

    def day(self):
        D = R["dispatch"]
        mix = D["mix"]
        hrs = list(range(1, len(D["demand"]) + 1))
        pa = viz.plot_axes([1, 24], [0, 90000], x_length=9.2, y_length=4.6, xticks=[1, 6, 12, 18, 24],
                           yticks=[20000, 40000, 60000, 80000], xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"{v / 1000:.0f} GW",
                           ylabel="ERCOT's generation, hour by hour", size=14).move_to([-1.4, -0.4, 0])
        order = ["nuclear", "coal", "wind", "solar", "gas", "hydro", "other"]
        layers, below = [], [0.0] * len(hrs)
        for f in order:
            top = [b + mix[f][i] for i, b in enumerate(below)]
            layers.append(Polygon(*[pa.ax.c2p(h, t) for h, t in zip(hrs, top)], *[pa.ax.c2p(h, b) for h, b in zip(reversed(hrs), reversed(below))],
                                  stroke_width=0, fill_color=FUEL_COL[f], fill_opacity=0.88))
            below = top
        dem = poly(pa, list(zip(hrs, D["demand"])), WHITE, 2.5)
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=FUEL_COL[f], fill_opacity=0.9), tx(FUEL_NAME[f], 14, GREY_A)).arrange(
            RIGHT, buff=0.08) for f in reversed(order[:5])]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.0, 1.2, 0])
        import datetime as _dt
        d = _dt.date.fromisoformat(D["day"])
        head = tx(f"Texas, {d.day} {d.strftime('%B')} {d.year}: the year's peak day", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("EIA, Hourly Electric Grid Monitor (Form EIA-930), ERCOT, net generation by source", size=13)
        nums = VGroup(tx(f"gas at its peak: {max(mix['gas']) / 1000:.0f} GW", 15, GAS, bold=True),
                      tx(f"solar at its peak: {max(mix['solar']) / 1000:.0f} GW", 15, SUN, bold=True),
                      tx(f"wind at its peak: {max(mix['wind']) / 1000:.0f} GW", 15, WIND, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.0, -1.6, 0])
        with self.voiceover(
            "Here is how Texas met its busiest day of 2025, hour by hour. <bookmark mark='a'/> At the bottom, nuclear, "
            "flat all day: it is cheapest to keep running. <bookmark mark='b'/> Then coal, and wind, whatever the wind "
            "gives. <bookmark mark='c'/> Then solar, rising with the sun and gone by evening. <bookmark mark='d'/> And on "
            "top, gas, which fills whatever is left and follows demand up and down: it is the plant that answers. As the "
            f"sun set and demand peaked, gas was making about {max(mix['gas']) / 1000:.0f} gigawatts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src), Create(dem))
            vo.wait_until("a")
            self.play(FadeIn(layers[0]), FadeIn(key[4]))
            vo.wait_until("b")
            self.play(FadeIn(layers[1]), FadeIn(layers[2]), FadeIn(key[3]), FadeIn(key[2]))
            vo.wait_until("c")
            self.play(FadeIn(layers[3]), FadeIn(key[1]), FadeIn(nums[1]))
            vo.wait_until("d")
            self.play(FadeIn(layers[4]), FadeIn(layers[5]), FadeIn(layers[6]), FadeIn(key[0]), FadeIn(nums[0]), FadeIn(nums[2]))
        self.clear_scene()

    def order(self):
        D = R["dispatch"]
        fleet = D["fleet"]
        total = sum(mw for _, mw, _ in fleet)
        sc_x = 10.0 / total
        cols = [SUN, NUKE, COAL, GAS, "#C9732F", "#F28B82", OTHER]
        x0, base = -5.6, -2.6

        def ypos(c):
            return base + min(c, 160) / 160 * 4.6
        blocks, x = VGroup(), x0
        for (n, mw_, c), col in zip(fleet, cols):
            w = mw_ * sc_x
            b = Rectangle(width=w, height=max(ypos(c) - base, 0.12), stroke_color="#0E1117", stroke_width=1.5, fill_color=col,
                          fill_opacity=0.88).move_to([x, base, 0], aligned_edge=DL)
            lab = VGroup(tx(n, 12, WHITE, bold=True), tx(f"${c:.0f}", 12, col)).arrange(DOWN, buff=0.02).next_to(b, UP, buff=0.06)
            blocks.add(VGroup(b, lab))
            x += w
        axis = VGroup(Line([x0, base, 0], [x0 + 10.2, base, 0], stroke_color=GREY_C), Line([x0, base, 0], [x0, base + 4.8, 0], stroke_color=GREY_C))
        yl = tx("running cost, $ a MWh", 13, GREY_B).next_to([x0, base + 4.8, 0], UP, buff=0.05).align_to([x0, 0, 0], LEFT)
        xl = tx("capacity, cheapest first", 13, GREY_B).next_to([x0 + 5, base, 0], DOWN, buff=0.15)
        demand = ValueTracker(35000)

        def dline():
            xx = x0 + demand.get_value() * sc_x
            return DashedLine([xx, base - 0.1, 0], [xx, base + 4.9, 0], stroke_color=WHITE, stroke_width=2.5, dash_length=0.1)

        def price():
            from explainer.industry.works import power
            units = [power.Unit(n, mw_, c) for n, mw_, c in fleet]
            return power.dispatch(units, demand.get_value())["price"]
        dl = always_redraw(dline)
        pl = draw.memo_redraw(lambda: round(price(), 0), lambda k: tx("price: $9,000, the cap" if k >= 9000 else f"price: ${k:,.0f}", 22, PRICE, bold=True),
                              lambda m: m.move_to([4.0, 2.9, 0]))
        tag = estimate_tag("illustration: a Texas-sized fleet; running costs from the Works and EIA", corner=DR, size=12)
        with self.voiceover(
            "Why that order? <bookmark mark='a'/> Line up every plant from the cheapest to run to the dearest. That is the "
            "merit order. <bookmark mark='b'/> Now draw demand. Every plant to the left of the line runs; and in most "
            "markets, every one of them is paid the running cost of the last plant needed, the one on the margin. "
            "<bookmark mark='c'/> On a quiet night, wind and nuclear can be enough, and the price is low. "
            "<bookmark mark='d'/> On a normal day, the line falls on gas, and gas sets the price for everyone. "
            "<bookmark mark='e'/> On the hottest afternoon, the peakers run, and the price jumps. <bookmark mark='f'/> And "
            "when demand passes everything there is, no plant sets the price: it goes to the cap, and someone's "
            "lights go out. The cheap plants to the left earn the difference between their cost and the price: that "
            "is what pays back the nuclear plant's huge fixed cost."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(yl), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in blocks], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.add(dl, pl)
            vo.wait_until("c")
            self.play(demand.animate.set_value(36000), run_time=1.0)
            vo.wait_until("d")
            self.play(demand.animate.set_value(75000), run_time=2.0)
            vo.wait_until("e")
            self.play(demand.animate.set_value(100000), run_time=2.0)
            vo.wait_until("f")
            self.play(demand.animate.set_value(106000), run_time=1.5)
        self.remove(dl, pl)
        self.clear_scene()

    def gas(self):
        D = R["dispatch"]
        pr, gp = D["prices"], D["gas"]
        ys = sorted(gp)
        pts = [(gp[y], pr[y], str(y)) for y in ys if y != 2021] + [(3.62, D["price21x"], "2021 without the storm")]
        pa = viz.plot_axes([1.5, 5], [0, 60], x_length=7.6, y_length=4.4, xticks=[2, 3, 4, 5], yticks=[15, 30, 45, 60],
                           xfmt=lambda v: f"${v:.0f}", yfmt=lambda v: f"${v:.0f}", ylabel="ERCOT's average price, $ a MWh",
                           size=14).move_to([-2.2, -0.4, 0])
        xl = tx("natural gas, $ per million Btu", 14, GREY_B).next_to(pa, DOWN, buff=0.08)
        dots = VGroup()
        for gx, py, lab in pts:
            d_ = Dot(pa.ax.c2p(gx, py), radius=0.08, color=GAS)
            dots.add(VGroup(d_, tx(lab, 12, GREY_A).next_to(d_, LEFT if lab.startswith("2021") else RIGHT, buff=0.06)))
        fit = Line(pa.ax.c2p(1.6, D["icpt"] + D["slope"] * 1.6), pa.ax.c2p(4.9, D["icpt"] + D["slope"] * 4.9), stroke_color=PRICE,
                   stroke_width=2.5)
        notes = VGroup(tx(f"each $1 on gas adds about ${D['slope']:.1f}", 17, PRICE, bold=True),
                       tx("to a MWh of power", 17, PRICE, bold=True),
                       tx("'natural gas units are generally", 15, WHITE), tx("on the margin in ERCOT'", 15, WHITE),
                       tx("the market monitor, 2021", 13, GREY_B),
                       tx(f"2021 with the storm: ${pr[2021]:.0f}", 17, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(
            [4.4, 0.0, 0])
        src = source("Potomac Economics, State of the Market Report for ERCOT, 2021 (prices and gas, 2014-2021)", size=13)
        with self.voiceover(
            "Because gas is so often the plant on the margin, the price of power follows the price of gas. "
            "<bookmark mark='a'/> Each dot is a year in Texas: the average price of gas, and the average price of a "
            "megawatt-hour, from the market monitor's reports. <bookmark mark='b'/> They line up. Each extra dollar on a "
            f"million Btu of gas added about {D['slope']:.1f} dollars to a megawatt-hour, about what a gas plant burns "
            "to make one. In the monitor's words, natural gas units are generally on the margin. <bookmark mark='c'/> "
            f"Except 2021: with the storm, the year's average was {pr[2021]:.0f} dollars, more than six times the year "
            "before, almost entirely because of a few days in February."
        ) as vo:
            head = tx("Texas: the price of power against the price of gas", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
            self.add(head)
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(src), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(d_[0], color=GAS, scale_factor=1.5) for d_ in dots], run_time=1.2)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(notes[:5]))
            vo.wait_until("c")
            self.play(FadeIn(notes[5]))
        self.clear_scene()
