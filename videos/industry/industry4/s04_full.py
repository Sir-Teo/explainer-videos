from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

ORDER = ("nuclear", "wind", "solar", "ct_frame", "cc2")
COL = dict(nuclear=TECH["nuclear"], wind=TECH["wind"], solar=TECH["solar"], ct_frame=TECH["gas_ct"], cc2=TECH["gas_cc"])
ICON = dict(nuclear="nuclear", wind="wind", solar="solar", ct_frame="gas_ct", cc2="gas_cc")
SHORT = dict(nuclear="nuclear", wind="wind", solar="solar", ct_frame="gas peaker", cc2="gas, combined cycle")
YMAX = 260


class Full(VoiceoverScene):
    def construct(self):
        card(self, 3, "How full?", "Why does a plant's cost depend on how often it runs?",
             "Chapter three. How full?", lit=("make", "dollar"))
        self.one_plant()
        self.five_plants()

    def one_plant(self):
        T_ = R["lcoe"]["techs"]["nuclear"]
        fixed, var = T_["fixed_kw_yr"], T_["variable"]
        u = ValueTracker(0.95)
        plant = draw.cooling_tower(2.2).move_to([-4.9, 1.45, 0])
        draw.puff(plant.steam, top=1.0, speed=0.3)
        name = tx("a new nuclear plant", 22, TECH["nuclear"]).next_to(plant, DOWN, buff=0.25)

        # the year as 365 days, lit for the share of the time the plant runs
        days = VGroup(*[Square(0.105, stroke_width=0, fill_color="#2A3446", fill_opacity=1) for _ in range(365)])
        days.arrange_in_grid(rows=13, buff=0.025).move_to([-4.9, -2.35, 0])

        def lit_days(m):
            k = int(round(365 * u.get_value()))
            for i, d in enumerate(m):
                d.set_fill(TECH["nuclear"] if i < k else "#2A3446")
        days.add_updater(lit_days)
        days_t = tx("days of the year it runs", 17, GREY_B).next_to(days, UP, buff=0.12)

        # the cost of a megawatt-hour, stacked: fixed on top of variable
        base = -2.9
        scale = 4.4 / 400  # inches per $/MWh; the bar is cut off above $400
        x0 = 1.0

        def fixed_mwh():
            return fixed * 1000 / (8760 * u.get_value())

        def stack_bar():
            v = Rectangle(width=1.5, height=var * scale, stroke_width=0, fill_color=VAR, fill_opacity=0.95)
            v.move_to([x0, base, 0], aligned_edge=DOWN)
            cut = fixed_mwh() + var > 400
            f = Rectangle(width=1.5, height=max(min(fixed_mwh(), 400 - var) * scale, 0.01), stroke_width=0,
                          fill_color=FIXED, fill_opacity=0.95)
            f.next_to(v, UP, buff=0)
            g = VGroup(v, f)
            if cut:  # a torn edge to show the bar goes on
                zz = VMobject(stroke_color="#0E1117", stroke_width=6).set_points_as_corners(
                    [f.get_corner(UL) + DOWN * 0.25 + RIGHT * (1.5 * i / 6) + DOWN * (0.12 if i % 2 else 0)
                     for i in range(7)])
                g.add(zz)
            return g
        bar = always_redraw(stack_bar)
        floor = Line([x0 - 1.2, base, 0], [x0 + 1.2, base, 0], stroke_color=GREY_B, stroke_width=2)
        total = draw.number(lambda: fixed_mwh() + var, 0, prefix="$", size=44, color=WHITE)
        total.add_updater(lambda m: m.next_to(bar, UP, buff=0.15), call_updater=True)
        unit = tx("per megawatt-hour", 18, GREY_B).move_to([x0, base - 0.35, 0])
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=FIXED, fill_opacity=1),
                            tx("the plant itself, spread over its output", 19, FIXED)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.22, stroke_width=0, fill_color=VAR, fill_opacity=1),
                            tx(f"fuel and running costs: ${var:.0f}", 19, VAR)).arrange(RIGHT, buff=0.15)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 2.4, 0])
        share = draw.number(lambda: 100 * u.get_value(), 0, suffix="%", size=40, color=TECH["nuclear"])
        share.move_to([4.3, 0.6, 0])
        share_t = tx("of the time running", 18, GREY_B).next_to(share, DOWN, buff=0.1)
        eq = MathTex(r"\frac{\text{cost per year}}{\text{hours run}}", font_size=40).move_to([4.4, -1.6, 0])
        tag = estimate_tag("EIA's AEO2026 costs; 7% over 30 years", corner=DR)
        with self.voiceover(
            "The cost of one more is only half of a plant's cost. The other half is the plant itself, and what you "
            "pay for it per unit depends on how much you use it. <bookmark mark='a'/> Take a new nuclear plant, with "
            "the costs the US Energy Information Administration assumes for one built today: eight thousand dollars "
            "of construction for every kilowatt of capacity. <bookmark mark='b'/> Pay that off over thirty years at "
            "seven percent, add the staff and upkeep, and each kilowatt costs about "
            f"{fixed:.0f} dollars a year whether it runs or not. The fuel and the running costs add only "
            f"{var:.0f} dollars a megawatt-hour. <bookmark mark='c'/> Run it flat out, as American reactors do, and "
            f"a megawatt-hour costs about {T_['per_mwh'][0.95]:.0f} dollars."
        ) as vo:
            self.play(FadeIn(plant), FadeIn(name), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(days), FadeIn(days_t), FadeIn(share), FadeIn(share_t))
            vo.wait_until("b")
            self.play(FadeIn(floor), FadeIn(bar), FadeIn(unit), FadeIn(key), Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(total))

        with self.voiceover(
            "Now run it less. <bookmark mark='a'/> At sixty percent of the time, the same yearly bill is spread over "
            f"fewer hours, and a megawatt-hour costs {T_['per_mwh'][0.6]:.0f} dollars. <bookmark mark='b'/> At a "
            f"quarter of the time, {T_['per_mwh'][0.25]:.0f}. At a tenth, nearly a thousand. Nothing about the plant "
            "changed. Only how full it was."
        ) as vo:
            vo.wait_until("a")
            self.play(u.animate.set_value(0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(u.animate.set_value(0.25), run_time=2.0)
            self.play(u.animate.set_value(0.1), run_time=2.0)
            self.wait(0.5)
            self.play(u.animate.set_value(0.95), run_time=2.5)
        days.clear_updaters()
        self.clear_scene()

    def five_plants(self):
        L = R["lcoe"]["techs"]
        ax = CornerAxes(x_range=[0, 1.0, 0.25], y_range=[0, YMAX, 50], x_length=7.6, y_length=5.0,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-1.2, -0.25, 0])
        xt = VGroup(*[tx(f"{int(100 * v)}%", 16, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                      for v in (0.25, 0.5, 0.75, 1.0)])
        yt = VGroup(*[tx(f"${v}", 16, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (50, 100, 150, 200, 250)])
        xl = tx("share of the year it runs", 19, GREY_B).next_to(ax, DOWN, buff=0.4)
        yl = tx("cost per megawatt-hour", 19, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)

        def cost(k, x):
            t = L[k]
            return t["fixed_kw_yr"] * 1000 / (8760 * x) + t["variable"]

        curves, labels, icons = {}, {}, {}
        for k in ORDER:
            t = L[k]
            x_lo = t["fixed_kw_yr"] * 1000 / (8760 * (YMAX - t["variable"]))
            curves[k] = ax.plot(lambda x, k=k: cost(k, x), x_range=[x_lo, 1.0, 0.005], color=COL[k], stroke_width=4)
            labels[k] = tx(SHORT[k], 18, COL[k])
            icons[k] = icon(ICON[k], 0.45)
        # labels at the right end, spread so they do not collide
        ends = sorted(ORDER, key=lambda k: cost(k, 1.0))
        y_end = {k: ax.c2p(1.0, cost(k, 1.0))[1] for k in ORDER}
        prev = -10
        for k in ends:
            y = max(y_end[k], prev + 0.42)
            prev = y
            VGroup(icons[k], labels[k]).arrange(RIGHT, buff=0.12).move_to([ax.c2p(1.0, 0)[0] + 1.55, y, 0])
        u = ValueTracker(0.95)

        def dot(k):
            def make():
                x = u.get_value()
                y = cost(k, x)
                if y > YMAX:
                    return Triangle(stroke_width=0, fill_color=COL[k], fill_opacity=0.9).scale(0.09).move_to(
                        ax.c2p(x, YMAX) + UP * 0.12)
                return glow_dot(ax.c2p(x, y), color=COL[k], radius=0.08)
            return always_redraw(make)
        dots = VGroup(*[dot(k) for k in ORDER])
        vline = always_redraw(lambda: DashedLine(ax.c2p(u.get_value(), 0), ax.c2p(u.get_value(), YMAX),
                                                 stroke_color=GREY_C, stroke_width=1.5))
        tag = estimate_tag("EIA's AEO2026 costs; 7% over 30 years; no subsidies, no grid costs", corner=DR)
        with self.voiceover(
            "Do the same for every kind of plant you could build, and you get a family of curves. "
            "<bookmark mark='a'/> Each falls as the plant runs more, because the yearly bill for the plant is spread "
            "over more hours. Each flattens out at its cost of one more megawatt-hour: nothing for wind and solar, "
            "whose fuel is free, and the price of gas for the gas plants. <bookmark mark='b'/> Run everything nearly "
            "all the time, and the cheapest are solar and wind, then combined-cycle gas, with nuclear dearest. "
            "<bookmark mark='c'/> Run everything a tenth of the time, and the order changes: the gas peaker, the "
            "cheapest machine to build, wins easily, and nuclear is off the top of the chart."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(curves[k]) for k in ORDER], lag_ratio=0.25), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(VGroup(icons[k], labels[k])) for k in ORDER], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(vline), FadeIn(dots))
            vo.wait_until("c")
            self.play(u.animate.set_value(0.1), run_time=4.0)

        rings = VGroup()
        tags = VGroup()
        for k in ORDER:
            x = L[k]["actual_cf"]
            p = ax.c2p(x, cost(k, x))
            rings.add(Circle(radius=0.14, stroke_color=COL[k], stroke_width=4).move_to(p))
            tags.add(tx(f"${L[k]['actual']:.0f}", 17, COL[k], bold=True).next_to(p, UR, buff=0.06))
        tags[ORDER.index("ct_frame")].next_to(rings[ORDER.index("ct_frame")], RIGHT, buff=0.08)
        tags[ORDER.index("solar")].next_to(rings[ORDER.index("solar")], DL, buff=0.04)
        with self.voiceover(
            "But most plants do not choose how full they are. <bookmark mark='a'/> The rings mark where each kind of "
            "plant actually ran in America in 2025. Wind turbines turned out about a third of what they could, solar "
            "panels about a quarter, because the wind drops and the sun sets. Reactors ran ninety-one percent of the "
            "time. Combined-cycle gas ran about sixty percent, and the peakers only fourteen. <bookmark mark='b'/> "
            "At those rates, a new combined-cycle plant's megawatt-hour costs about "
            f"{L['cc2']['actual']:.0f} dollars, wind's {L['wind']['actual']:.0f}, solar's "
            f"{L['solar']['actual']:.0f}, a reactor's {L['nuclear']['actual']:.0f} and a peaker's "
            f"{L['ct_frame']['actual']:.0f}. <bookmark mark='c'/> And yet power companies still build peakers, at "
            "the highest cost on this chart. The next chapters will say why: a peaker is not selling the average "
            "megawatt-hour. It sells the hours when nothing else is left."
        ) as vo:
            self.play(FadeOut(dots), FadeOut(vline))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(rings[ORDER.index("ct_frame")], color=COL["ct_frame"], scale_factor=1.6))
        rule = tx("The more a business has paid up front, the more it needs to run full.", 26, PRICE, bold=True)
        rule.to_edge(UP, buff=0.25)
        with self.voiceover(
            "This is the first rule of the cost curve. The more of a business's cost is paid up front, the more it "
            "needs to run full, and the more it will do to fill itself: cut prices, take the order below average "
            "cost, keep a reactor on through the night. That is true of reactors, of aircraft, of chip factories and "
            "of hotel rooms."
        ):
            self.play(FadeIn(rule, shift=DOWN * 0.1))
        self.clear_scene()
