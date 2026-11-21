from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403

PLANT_COLS = {"hydro": "#7EC8F5", "nuclear": "#C9A0FF", "coal": "#9AA3B2", "gas A": "#7FD1B9", "gas B": "#7BD88F",
              "peakers": "#F2C14E", "oil": "#F25F5C"}


class Power(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Electricity markets", r"How is the price of power set, and how can it be gamed?",
             "Chapter thirteen. Electricity markets.", lit={2002: r"Borenstein, Bushnell and Wolak"},
             scale=("market",), horizon=("a day",))
        self.merit()
        self.day()
        self.withhold()
        self.california()

    def _stack(self, ax, P, held=0.0):
        g = VGroup()
        left = 0.0
        for nm, top, c in zip(P["name"], P["cum"], P["cost"]):
            w = top - left
            if nm == "gas B" and held:
                w = max(w - held, 0.0)
            if w > 0:
                p0, p1 = ax.ax.c2p(left, 0), ax.ax.c2p(left + w, c)
                g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.02), stroke_color=BLACK,
                                stroke_width=1.0, fill_color=PLANT_COLS[nm], fill_opacity=0.85).move_to((p0 + p1) / 2))
            left += w
        return g

    def merit(self):
        P = load("power")
        ax = plane([0, 46], [0, 170], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 40, 80, 120, 160], xlabel=r"gigawatts offered",
                   ylabel=r"cost of one more megawatt-hour, \ \$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        stack = self._stack(ax, P)
        key = VGroup(*[VGroup(Square(side_length=0.18, fill_color=PLANT_COLS[n], fill_opacity=0.85, stroke_width=0),
                              label(rf"{n}: \ \${c:.0f}", font_size=15, color=WHITE)).arrange(RIGHT, buff=0.12)
                       for n, c in zip(P["name"], P["cost"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        side = VGroup(key, label(r"the price is the cost \\ of the last plant \\ needed: \ every plant \\ is paid it",
                                 font_size=18, color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        side.to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Electricity is where much of the carbon is, and its markets have their own economics. <bookmark "
            "mark='a'/> The Island's power plants line up from cheapest to dearest to run, the merit order: hydro "
            "and nuclear, then coal, then two gas plants, then fast-starting peakers and oil. <bookmark mark='b'/> "
            "Demand for power at any moment barely responds to price, and the market price is set by the cost of "
            "the last plant needed to meet it. Every plant running is paid that price, so the cheap ones earn a "
            "margin that pays for building them. <bookmark mark='c'/> A carbon price shuffles this queue: it adds "
            "most to coal, less to gas, nothing to hydro or nuclear, and so it changes which plants run."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in stack], lag_ratio=0.3), FadeIn(key), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(stack[2], color=WHITE))
        self.clear_scene()

    def day(self):
        P = load("power")
        h = np.array(P["hours"])
        axL = plane([0, 23], [20, 37], center=LEFT * 3.4 + DOWN * 0.3, x_length=5.4, y_length=4.2,
                    xticks=[0, 6, 12, 18], yticks=[20, 25, 30, 35], xlabel=r"hour", ylabel=r"demand, \ GW",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        axR = plane([0, 23], [0, 60], center=RIGHT * 2.9 + DOWN * 0.3, x_length=5.4, y_length=4.2,
                    xticks=[0, 6, 12, 18], yticks=[0, 20, 40, 60], xlabel=r"hour", ylabel=r"price, \ \$ per MWh",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        dl = path(axL, h, P["load"], POWER, 3.0)
        steps = VMobject(stroke_color=METAL, stroke_width=3.0)
        pts = []
        for i in range(len(h)):
            pts += [axR.ax.c2p(h[i], P["price"][i]), axR.ax.c2p(min(h[i] + 1, 23), P["price"][i])]
        steps.set_points_as_corners(pts)
        foot = label(r"night: \ coal sets the price; \ day: \ gas A; \ the evening peak: \ gas B", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Over a day, <bookmark mark='a'/> demand on the Island swings from about twenty-two gigawatts at night "
            f"to {P['peak']:.0f} at the evening peak. <bookmark mark='b'/> The price follows the merit order: coal "
            "sets it at night, the first gas plant by day, the second at the evening peak. <bookmark mark='c'/> "
            "Prices that vary through the day are what make batteries and flexible demand pay: buy power at night, "
            "sell or save it at the peak."
        ) as vo:
            self.play(FadeIn(axL), FadeIn(axR), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(dl), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(steps), FadeIn(foot), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(steps, color=WHITE))
        self.clear_scene()

    def withhold(self):
        P = load("power")
        st = P["steps"]
        ax = plane([0, 46], [0, 260], center=LEFT * 2.2 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 50, 100, 150, 200, 250], xlabel=r"gigawatts offered",
                   ylabel=r"\$ per MWh", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        stack0 = self._stack(ax, P)
        stack1 = self._stack(ax, P, held=st[1]["held"] + 0.01)
        dem = vline(ax, P["peak"], 0, 260, WHITE)
        dem_l = label(rf"peak demand, \ {P['peak']:.0f} GW", font_size=15, color=WHITE).next_to(
            ax.ax.c2p(P["peak"], 255), LEFT, buff=0.1)
        side = VGroup(
            label(rf"Dynamo owns both \\ gas plants, \ {P['dynamo_cap']:.0f} GW", font_size=18, color=WHITE),
            label(rf"offer everything: \\ price \${st[0]['price']:.0f}, \ profit \\ {st[0]['profit']:.0f} thousand an "
                  r"hour", font_size=18, color=GREY_A),
            label(rf"hold back {st[1]['held']:.0f} GW: \\ the peakers set \\ \${st[1]['price']:.0f}; \ profit "
                  rf"{st[1]['profit']:.0f}", font_size=18, color=LOSS),
            label(rf"hold back {st[3]['held']:.0f} GW: \\ the cap, \ \${st[3]['price']:.0f}; \\ profit "
                  rf"{st[3]['profit']:.0f}", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the danger. <bookmark mark='a'/> One Island firm, Dynamo, owns both gas plants, "
            f"{P['dynamo_cap']:.0f} gigawatts. <bookmark mark='b'/> If it offers all of its capacity at the evening "
            f"peak, the price is {st[0]['price']:.0f} dollars, and Dynamo earns {st[0]['profit']:.0f} thousand "
            "dollars an hour. <bookmark mark='c'/> If it declares just "
            f"{st[1]['held']:.0f} gigawatts unavailable, the queue runs short of cheap plants, the peakers set the "
            f"price at {st[1]['price']:.0f} dollars, and Dynamo earns {st[1]['profit']:.0f} thousand an hour on what "
            f"it still sells, nearly thirty times as much. <bookmark mark='d'/> Holding back {st[3]['held']:.0f} "
            f"gigawatts drives the price to the market's cap of {st[3]['price']:.0f}. When demand is near capacity, "
            "even a firm with a modest share can make a fortune by producing less, and it is hard to prove a plant "
            "was not really broken."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(stack0), Create(dem), FadeIn(dem_l), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(VGroup(stack0[3], stack0[4]), color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Transform(stack0, stack1), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def california(self):
        T = tables.CALIFORNIA_2000.data
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"summer 1999", T["spend_1999"], GREY_B),
                                          (r"summer 2000", T["spend_2000"], LOSS))):
            y = 1.7 - 1.0 * i
            w = v / 9.5 * 7.0
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.0 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=20, color=col).next_to(np.array([-2.2, y, 0]), LEFT, buff=0.1), r,
                            label(rf"\${v:.2f} billion", font_size=20, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        split = VGroup()
        x = -2.0
        for nm, sh, col in ((r"costs", T["costs"], GREY_B), (r"competitive rents", T["rents"], METAL),
                            (r"market power", T["power"], LOSS)):
            w = sh / 100 * 7.0
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([x + w / 2, -0.6, 0]))
            split.add(VGroup(r, label(rf"{nm}: \ {sh}\%", font_size=16, color=col).next_to(r, DOWN, buff=0.12)))
            x += w
        split_l = label(r"the increase, \ split", font_size=20, color=WHITE).next_to(np.array([-2.2, -0.6, 0]), LEFT,
                                                                                      buff=0.1)
        head = label(r"California, \ June to October", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(rf"market power's share of all spending: \ {T['share_1998']}\% in 1998, \ {T['share_2000']}\% in "
                     r"2000", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.CALIFORNIA_2000.tag, corner=DR, font_size=11)
        with self.voiceover(
            "This happened. <bookmark mark='a'/> California opened its electricity market in 1998. From June to "
            f"October of 1999, wholesale power cost {T['spend_1999']:.2f} billion dollars; <bookmark mark='b'/> in "
            f"the same months of 2000, {T['spend_2000']:.2f} billion. <bookmark mark='c'/> Severin Borenstein, James "
            "Bushnell and Frank Wolak worked out what each plant would have offered in a competitive market. Of the "
            f"increase, {T['costs']} percent was higher costs of production, as gas prices rose, {T['rents']} "
            f"percent the rents any tight market pays, and {T['power']} percent market power. <bookmark mark='d'/> "
            f"Market power's share of all spending rose from {T['share_1998']} percent in 1998 to "
            f"{T['share_2000']} in 2000. The lesson for climate policy: markets for power need watching, and "
            "the transition to clean electricity will run through markets like this one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(split_l), LaggedStart(*[FadeIn(s_) for s_ in split], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
