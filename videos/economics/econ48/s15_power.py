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

    def _stack(self, ax, names, cums, costs, held=0.0):
        """The merit order as bars keyed by plant name; ``held`` GW of Dynamo's are withdrawn, costliest first."""
        g = {}
        left = 0.0
        prev = 0.0
        rest = held
        cuts = {}
        for nm in sorted(("gas A", "gas B"), key=lambda n: -costs[names.index(n)]):
            cut = min(rest, cums[names.index(nm)] - (cums[names.index(nm) - 1] if names.index(nm) else 0.0))
            cuts[nm], rest = cut, rest - cut
        for nm, top, c in zip(names, cums, costs):
            w = top - prev - cuts.get(nm, 0.0)
            prev = top
            p0, p1 = ax.ax.c2p(left, 0), ax.ax.c2p(left + max(w, 1e-3), c)
            g[nm] = Rectangle(width=max(p1[0] - p0[0], 1e-3), height=max(p1[1] - p0[1], 0.02), stroke_color=BLACK,
                              stroke_width=1.0, fill_color=PLANT_COLS[nm],
                              fill_opacity=0.85 if w > 1e-6 else 0.0).move_to((p0 + p1) / 2)
            if w <= 1e-6:
                g[nm].set_stroke(opacity=0.0)
            left += max(w, 0.0)
        return g

    def _rents(self, ax, names, cums, costs, demand, price, owners=None, held=0.0):
        """Each running plant's margin over its cost, up to the price (only ``owners``' plants if given)."""
        g = VGroup()
        left = 0.0
        prev = 0.0
        rest = held
        cuts = {}
        for nm in sorted(("gas A", "gas B"), key=lambda n: -costs[names.index(n)]):
            cut = min(rest, cums[names.index(nm)] - (cums[names.index(nm) - 1] if names.index(nm) else 0.0))
            cuts[nm], rest = cut, rest - cut
        for nm, top, c in zip(names, cums, costs):
            w = top - prev - cuts.get(nm, 0.0)
            prev = top
            run = min(w, max(demand - left, 0.0))
            if run > 0 and price > c + 0.5 and (owners is None or nm in owners):
                p0, p1 = ax.ax.c2p(left, c), ax.ax.c2p(left + run, price)
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=WHITE, stroke_width=1.2,
                                fill_color=WHITE, fill_opacity=0.22).move_to((p0 + p1) / 2))
            left += w
        return g

    def merit(self):
        P = load("power")
        Tx = P["taxed"]
        ax = plane([0, 46], [0, 210], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 50, 100, 150, 200], xlabel=r"gigawatts offered",
                   ylabel=r"cost of one more megawatt-hour, \ \$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = self._stack(ax, P["name"], P["cum"], P["cost"])
        taxed = self._stack(ax, Tx["name"], Tx["cum"], Tx["cost"])
        stack = VGroup(*[bars[n] for n in P["name"]])
        key = VGroup(*[VGroup(Square(side_length=0.18, fill_color=PLANT_COLS[n], fill_opacity=0.85, stroke_width=0),
                              label(rf"{n}: \ \${c:.0f}", font_size=15, color=WHITE)).arrange(RIGHT, buff=0.12)
                       for n, c in zip(P["name"], P["cost"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        side = VGroup(key, label(r"the price is the cost \\ of the last plant \\ needed: \ every plant \\ is paid it",
                                 font_size=18, color=E.ACCENT),
                      label(rf"a carbon price of \\ \${P['carbon']:.0f} a tonne: \ coal \\ moves behind gas",
                            font_size=18, color=CO2)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.3)
        d0 = 33.0
        p0 = P["cost"][int(np.searchsorted(P["cum"], d0))]
        dem = vline(ax, d0, 0, 200, WHITE)
        dem_l = label(rf"demand, \ {d0:.0f} GW", font_size=15, color=WHITE).next_to(ax.ax.c2p(d0, 200), LEFT,
                                                                                     buff=0.1)
        pl = DashedLine(ax.ax.c2p(0, p0), ax.ax.c2p(46, p0), color=E.ACCENT, stroke_width=2.4, dash_length=0.1)
        pl_l = label(rf"price \${p0:.0f}", font_size=15, color=E.ACCENT).next_to(ax.ax.c2p(46, p0), UP, buff=0.08)
        rents = self._rents(ax, P["name"], P["cum"], P["cost"], d0, p0)
        pk = P["peak"]
        dem2 = vline(ax, pk, 0, 200, WHITE)
        dem2_l = label(rf"evening peak, \ {pk:.0f} GW", font_size=15, color=WHITE).next_to(ax.ax.c2p(pk, 200), LEFT,
                                                                                              buff=0.1)
        pl2 = DashedLine(ax.ax.c2p(0, Tx["peak_price"]), ax.ax.c2p(46, Tx["peak_price"]), color=E.ACCENT,
                         stroke_width=2.4, dash_length=0.1)
        pl2_l = label(rf"price \${Tx['peak_price']:.0f}", font_size=15, color=E.ACCENT).next_to(
            ax.ax.c2p(1.0, Tx["peak_price"]), UP, buff=0.06).align_to(ax.ax.c2p(1.0, Tx["peak_price"]), LEFT)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Electricity is where much of the carbon is, and its markets have their own economics. <bookmark "
            "mark='a'/> The Island's power plants line up from cheapest to dearest to run, the merit order: hydro "
            "and nuclear, then coal, then two gas plants, then fast-starting peakers and oil. <bookmark mark='b'/> "
            "Demand for power at any moment barely responds to price, and the market price is set by the cost of "
            "the last plant needed to meet it. <bookmark mark='c'/> Every plant running is paid that price, so the "
            "cheap ones earn a margin that pays for building them. <bookmark mark='d'/> A carbon price shuffles this "
            f"queue. At {P['carbon']:.0f} dollars a tonne it adds about fifty dollars a megawatt-hour to coal, which "
            "emits about a tonne for each, twenty to gas, and nothing to hydro or nuclear. <bookmark mark='e'/> Coal "
            "moves behind both gas plants, and at the evening peak the price rises to "
            f"{Tx['peak_price']:.0f} dollars: the tax changes which plants run, and every buyer pays it at the margin."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in stack], lag_ratio=0.3), FadeIn(key), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(dem), FadeIn(dem_l), run_time=1.0)
            self.play(Create(pl), FadeIn(pl_l), Indicate(bars["gas B"], color=WHITE), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rents], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeOut(rents), FadeOut(pl), FadeOut(pl_l), FadeOut(dem), FadeOut(dem_l), run_time=0.8)
            self.play(*[Transform(bars[n], taxed[n]) for n in P["name"]], run_time=3.0)
            self.play(Indicate(bars["coal"], color=WHITE), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[2]), Create(dem2), FadeIn(dem2_l), run_time=1.0)
            self.play(Create(pl2), FadeIn(pl2_l), Indicate(bars["coal"], color=WHITE), run_time=1.5)
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
        hr = ValueTracker(0.0)

        def _ld(x):
            return float(np.interp(x, h, P["load"]))

        def _pr(x):
            return float(P["price"][min(int(x), len(h) - 1)])

        dL = always_redraw(lambda: Dot(axL.ax.c2p(hr.get_value(), _ld(hr.get_value())), radius=0.08, color=WHITE))
        dR = always_redraw(lambda: Dot(axR.ax.c2p(hr.get_value(), _pr(hr.get_value())), radius=0.08, color=WHITE))
        read = always_redraw(lambda: label(rf"{int(hr.get_value()):02d}:00 \quad {_ld(hr.get_value()):.0f} GW "
                                           rf"\quad \${_pr(hr.get_value()):.0f}", font_size=20,
                                           color=WHITE).to_edge(UP, buff=0.5))
        lo, hi = int(np.argmin(P["price"])), int(np.argmax(P["price"]))
        buy = Rectangle(width=axR.ax.c2p(1, 0)[0] - axR.ax.c2p(0, 0)[0] + 0.02, height=3.9, stroke_width=0,
                        fill_color=GAIN, fill_opacity=0.18).move_to(axR.ax.c2p(lo + 0.5, 30))
        sell = Rectangle(width=axR.ax.c2p(1, 0)[0] - axR.ax.c2p(0, 0)[0] + 0.02, height=3.9, stroke_width=0,
                         fill_color=LOSS, fill_opacity=0.18).move_to(axR.ax.c2p(hi + 0.5, 30))
        bl = label(r"charge", font_size=15, color=GAIN).next_to(buy, UP, buff=0.05)
        sl = label(r"discharge", font_size=15, color=LOSS).next_to(sell, UP, buff=0.05)
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
            self.add(dL, dR, read)
            self.play(hr.animate.set_value(22.99), run_time=7.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(buy), FadeIn(sell), FadeIn(bl), FadeIn(sl), hr.animate.set_value(lo + 0.5), run_time=1.5)
            self.play(hr.animate.set_value(hi + 0.5), run_time=3.0)
        self.clear_scene()

    def withhold(self):
        P = load("power")
        st = P["steps"]
        nm, cu, co = P["name"], P["cum"], P["cost"]
        d = P["peak"]
        ax = plane([0, 46], [0, 260], center=LEFT * 2.2 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 50, 100, 150, 200, 250], xlabel=r"gigawatts offered",
                   ylabel=r"\$ per MWh", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = self._stack(ax, nm, cu, co)
        stack = VGroup(*[bars[n] for n in nm])
        dem = vline(ax, d, 0, 260, WHITE)
        dem_l = label(rf"peak demand, \ {d:.0f} GW", font_size=15, color=WHITE).next_to(ax.ax.c2p(d, 255), LEFT,
                                                                                         buff=0.1)
        cap = DashedLine(ax.ax.c2p(0, P["cap_price"]), ax.ax.c2p(46, P["cap_price"]), color=GREY_B, stroke_width=1.6,
                         dash_length=0.08)
        cap_l = label(r"price cap", font_size=14, color=GREY_B).next_to(ax.ax.c2p(46, P["cap_price"]), DOWN,
                                                                         buff=0.06).shift(LEFT * 0.3)

        def _price(p):
            ln = Line(ax.ax.c2p(0, p), ax.ax.c2p(d, p), color=E.ACCENT, stroke_width=2.6)
            tx = label(rf"price \${p:.0f}", font_size=15, color=E.ACCENT)
            return VGroup(ln, tx.next_to(ax.ax.c2p(1.0, p), UP, buff=0.06).align_to(ax.ax.c2p(1.0, p), LEFT))

        def _held(h):
            end = cu[nm.index("oil")]
            p0, p1 = ax.ax.c2p(end - h, 0), ax.ax.c2p(end, 48)
            r = DashedVMobject(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=GAIN,
                                         stroke_width=2.0).move_to((p0 + p1) / 2), num_dashes=40)
            return VGroup(r, label(rf"{h:.0f} GW \\ withheld", font_size=14, color=GAIN).next_to(r, UP, buff=0.08))

        prof = [self._rents(ax, nm, cu, co, d, s_["price"], owners=("gas A", "gas B"), held=s_["held"]) for s_ in st]
        prof = [p_.set_fill(GAIN, 0.35).set_stroke(GAIN, 1.6) for p_ in prof]
        side = VGroup(
            label(rf"Dynamo owns both \\ gas plants, \ {P['dynamo_cap']:.0f} GW", font_size=18, color=WHITE),
            label(rf"offer everything: \\ price \${st[0]['price']:.0f}, \ profit \\ {st[0]['profit']:.0f} thousand "
                  r"an hour", font_size=18, color=GREY_A),
            label(rf"hold back {st[1]['held']:.0f} GW: \\ the peakers set \\ \${st[1]['price']:.0f}; \ profit "
                  rf"{st[1]['profit']:.0f}", font_size=18, color=LOSS),
            label(rf"hold back {st[3]['held']:.0f} GW: \\ the cap, \ \${st[3]['price']:.0f}; \\ profit "
                  rf"{st[3]['profit']:.0f}", font_size=18, color=LOSS),
            label(r"green: \ Dynamo's \\ margin on what \\ it still sells", font_size=16, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        price = _price(st[0]["price"])
        held = None
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
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(stack), Create(dem), FadeIn(dem_l), Create(cap), FadeIn(cap_l),
                      run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(VGroup(bars["gas A"], bars["gas B"]), color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(price[0]), FadeIn(price[1]), FadeIn(prof[0]), FadeIn(side[4]))
            for k, mk in ((1, "c"), (3, "d")):
                vo.wait_until(mk)
                new = self._stack(ax, nm, cu, co, held=st[k]["held"] + 1e-6)
                nh = _held(st[k]["held"])
                self.play(*[Transform(bars[n], new[n]) for n in nm], FadeIn(nh) if held is None else
                          Transform(held, nh), run_time=2.0)
                if held is None:
                    held = nh
                self.play(Transform(price, _price(st[k]["price"])), Transform(prof[0], prof[k]),
                          FadeIn(side[{1: 2, 3: 3}[k]]), run_time=1.5)
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
            f"increase, <bookmark mark='c1'/> {T['costs']} percent was higher costs of production, as gas prices "
            f"rose, <bookmark mark='c2'/> {T['rents']} percent the rents any tight market pays, <bookmark mark='c3'/> "
            f"and {T['power']} percent market power. <bookmark mark='d'/> "
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
            self.play(FadeIn(split_l), Indicate(bars[1][1], color=WHITE, scale_factor=1.03), run_time=1.5)
            for mk, s_ in zip(("c1", "c2", "c3"), split):
                vo.wait_until(mk)
                self.play(GrowFromEdge(s_[0], LEFT), FadeIn(s_[1]), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(foot), Indicate(split[2], color=WHITE, scale_factor=1.05), run_time=1.5)
        self.clear_scene()
