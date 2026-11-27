from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Plants(VoiceoverScene):
    def construct(self):
        card(self, 3, "Fixed cost against running cost", "Why would anyone build a plant that runs one hour in ten?",
             "Chapter three. Fixed cost against running cost.", lit=("make", "dollar"))
        self.two_costs()
        self.screening()
        self.use()

    def two_costs(self):
        P = R["plants"]
        T = P["techs"]
        order = [("nuclear", draw.cooling_tower(1.2) if hasattr(draw, "cooling_tower") else draw.factory(1.0), NUKE),
                 ("cc2", draw.gas_plant(1.0), GAS), ("ct_frame", draw.gas_plant(0.75), "#F28B82"),
                 ("wind", draw.wind_turbine(1.2), WIND), ("solar", draw.solar_panel(0.9), SUN)]
        cols = VGroup()
        for i, (k, ic, col) in enumerate(order):
            t = T[k]
            x = -5.2 + 2.6 * i
            ic.scale_to_fit_height(min(ic.height, 1.0)).move_to([x, 2.3, 0])
            nm = tx(t["name"], 15, col, bold=True).next_to(ic, DOWN, buff=0.1)
            fb = Rectangle(width=0.7, height=t["fixed"] / 800 * 2.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [x - 0.42, -2.6, 0], aligned_edge=DOWN)
            rb = Rectangle(width=0.7, height=max(t["running"] / 40 * 2.6, 0.02), stroke_color=col, stroke_width=2, fill_color=col,
                           fill_opacity=0.25).move_to([x + 0.42, -2.6, 0], aligned_edge=DOWN)
            fl = tx(f"${t['fixed']:,.0f}", 13, col, bold=True).next_to(fb, UP, buff=0.05)
            rl = tx(f"${t['running']:.0f}", 13, col).next_to(rb, UP, buff=0.05)
            sub = VGroup(tx("fixed", 11, GREY_B).next_to(fb, DOWN, buff=0.06), tx("running", 11, GREY_B).next_to(rb, DOWN, buff=0.06))
            cols.add(VGroup(ic, nm, fb, rb, fl, rl, sub))
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=GREY_B, fill_opacity=0.85),
                            tx("fixed: $ a kW of capacity a year, built and paid for", 14, GREY_A)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_B, fill_opacity=0.25),
                            tx("running: $ for each MWh it makes (fuel and upkeep)", 14, GREY_A)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.6).to_edge(DOWN, buff=0.45)
        tag = estimate_tag(f"EIA AEO2026 costs; capital at {100 * P['rate']:.0f}% a year; gas ${P['gas_price']:.2f}; nuclear fuel EIA 2025",
                           corner=UR, size=11)
        with self.voiceover(
            "Every kind of power plant has two kinds of cost. <bookmark mark='a'/> A fixed cost, paid every year whether "
            "it runs or not: the money borrowed to build it, and the staff who keep it ready. <bookmark mark='b'/> And a "
            "running cost, for each megawatt-hour it actually makes: mostly fuel. <bookmark mark='c'/> Here they are, "
            "from the government's own cost estimates. A nuclear plant: enormous fixed cost, about "
            f"{T['nuclear']['fixed']:,.0f} dollars a kilowatt a year, and almost nothing to run. <bookmark mark='d'/> A gas "
            f"plant: about a hundred dollars a kilowatt a year, but {T['cc2']['running']:.0f} to "
            f"{T['ct_frame']['running']:.0f} dollars of gas and upkeep for every megawatt-hour. <bookmark mark='e'/> Wind and "
            "solar: in between on fixed cost, and nothing at all to run, because the wind and the sun are free. Which "
            "one is cheapest depends entirely on how many hours you need it."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag), LaggedStart(*[FadeIn(c_[0]) for c_ in cols], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(c_[1]) for c_ in cols], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Indicate(key[0]))
            vo.wait_until("b")
            self.play(Indicate(key[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(cols[0][2], DOWN), GrowFromEdge(cols[0][3], DOWN), FadeIn(cols[0][4:]))
            self.add(*[c_[6] for c_ in cols[1:]])
            vo.wait_until("d")
            self.play(*[GrowFromEdge(c_[j], DOWN) for c_ in cols[1:3] for j in (2, 3)], *[FadeIn(c_[4:]) for c_ in cols[1:3]])
            vo.wait_until("e")
            self.play(*[GrowFromEdge(c_[j], DOWN) for c_ in cols[3:] for j in (2, 3)], *[FadeIn(c_[4:]) for c_ in cols[3:]])
        self.clear_scene()

    def screening(self):
        P = R["plants"]
        T = P["techs"]
        xs = [x for x in range(0, 101, 5)]
        pa = viz.plot_axes([0, 100], [0, 1200], x_length=8.6, y_length=4.6, xticks=[0, 25, 50, 75, 100],
                           yticks=[300, 600, 900, 1200], xfmt=lambda v: f"{int(v)}%", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="total cost, $ a kW a year", size=14).move_to([-1.6, -0.4, 0])
        xl = tx("share of the year's hours the plant runs (capacity factor)", 14, GREY_B).next_to(pa, DOWN, buff=0.08)
        lines = {}
        for k, col in (("ct_frame", "#F28B82"), ("cc2", GAS), ("nuclear", NUKE)):
            lines[k] = poly(pa, list(zip(xs, T[k]["curve"])), col, 4)
        labs = VGroup(tx("gas peaker", 15, "#F28B82", bold=True).next_to(pa.ax.c2p(100, T["ct_frame"]["curve"][-1]), RIGHT, buff=0.1),
                      tx("combined-cycle gas", 15, GAS, bold=True).next_to(pa.ax.c2p(100, T["cc2"]["curve"][-1]), RIGHT, buff=0.1).shift(DOWN * 0.15),
                      tx("nuclear", 15, NUKE, bold=True).next_to(pa.ax.c2p(100, T["nuclear"]["curve"][-1]), RIGHT, buff=0.1))
        notes = VGroup(tx("At 90% of the year, a new plant's power:", 15, GREY_A),
                       tx(f"combined-cycle gas: ${P['cc_mwh_90']:.0f} a MWh", 17, GAS, bold=True),
                       tx(f"nuclear: ${P['nuke_mwh_90']:.0f} a MWh", 17, NUKE, bold=True),
                       tx(f"nuclear wins only if gas costs", 15, GREY_A),
                       tx(f"more than about ${P['gas_even']:.0f} per million Btu", 15, GREY_A),
                       tx(f"(it cost power plants ${P['gas_price']:.2f} in 2025)", 13, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.75, 2.25, 0])
        head = tx("The screening curve: which plant is cheapest for how many hours?", 21, WHITE, bold=True).to_edge(UP, buff=0.3)
        tag = estimate_tag("the Works (power.py): EIA AEO2026 costs, 7% capital, 30-year gas and 40-year nuclear lives", corner=DR, size=11)
        with self.voiceover(
            "Engineers draw this as a screening curve. <bookmark mark='a'/> Across the bottom, how many hours of the "
            "year a plant runs. Up the side, what it costs in a year, fixed and running together. A plant that never "
            "runs costs only its fixed cost; every hour it runs adds its running cost. <bookmark mark='b'/> The peaker "
            "starts low and climbs steeply. <bookmark mark='c'/> The combined-cycle plant, on today's costs, is cheaper "
            "at almost any use. <bookmark mark='d'/> Nuclear starts very high and climbs slowly, but on these numbers "
            f"never catches up: run all year, a new combined-cycle plant makes power for about {P['cc_mwh_90']:.0f} "
            f"dollars a megawatt-hour and a new nuclear plant for about {P['nuke_mwh_90']:.0f}. "
            f"<bookmark mark='e'/> Nuclear wins only if gas costs more than about {P['gas_even']:.0f} dollars per million "
            "Btu, or carbon is priced, or the money to build it is far cheaper. That one comparison explains why "
            "America has built so many gas plants and so few reactors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(xl), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(lines["ct_frame"]), FadeIn(labs[0]), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(lines["cc2"]), FadeIn(labs[1]), run_time=1.8)
            vo.wait_until("d")
            self.play(Create(lines["nuclear"]), FadeIn(labs[2]), run_time=1.8)
            self.play(FadeIn(notes[:3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3:]))
        self.clear_scene()

    def use(self):
        P = R["plants"]
        cf = P["cf"]
        items = [("nuclear", "nuclear", NUKE), ("gas_cc", "combined-cycle gas", GAS), ("coal", "coal", COAL),
                 ("wind", "wind", WIND), ("hydro", "hydro", HYDRO), ("solar", "solar", SUN), ("gas_ct", "gas peakers", "#F28B82")]
        bars = VGroup()
        for i, (k, n, col) in enumerate(items):
            y = 2.2 - 0.68 * i
            v = cf[k]["cf"]
            b = Rectangle(width=8.0 * v, height=0.44, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-2.6, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(tx(n, 17, WHITE).next_to([-2.75, y, 0], LEFT, buff=0.0), b,
                            tx(f"{100 * v:.0f}%", 17, col, bold=True).next_to(b, RIGHT, buff=0.12),
                            tx(f"{cf[k]['gw']:.0f} GW", 13, GREY_B).move_to([6.3, y, 0])))
        head = tx("How much of the year America's plants actually ran, 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        gw = tx("capacity", 13, GREY_B).move_to([6.3, 2.7, 0])
        src = source("EIA, Electric Power Annual 2025, Tables 4.8.A and 4.8.B (capacity factors)", size=13)
        with self.voiceover(
            "And that is how the real fleet runs. <bookmark mark='a'/> America's nuclear plants ran "
            f"{100 * cf['nuclear']['cf']:.0f} per cent of the hours of 2025, flat out, because their fuel is nearly free "
            "once they are built. <bookmark mark='b'/> Combined-cycle gas plants, about "
            f"{100 * cf['gas_cc']['cf']:.0f} per cent; coal, about {100 * cf['coal']['cf']:.0f}. <bookmark mark='c'/> Wind "
            f"and solar run when the weather lets them: {100 * cf['wind']['cf']:.0f} and {100 * cf['solar']['cf']:.0f} per "
            "cent. <bookmark mark='d'/> And the peakers, "
            f"{cf['gas_ct']['gw']:.0f} gigawatts of them, ran {100 * cf['gas_ct']['cf']:.0f} per cent of the time. They "
            "exist for the top of the load duration curve: the few hundred hours a year when everything else is "
            "already running."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(gw), *[FadeIn(b_[0]) for b_ in bars])
            for m_, idx in zip("abcd", ((0,), (1, 2), (3, 4, 5), (6,))):
                vo.wait_until(m_)
                self.play(*[AnimationGroup(GrowFromEdge(bars[i][1], LEFT), FadeIn(bars[i][2]), FadeIn(bars[i][3])) for i in idx],
                          run_time=1.0)
        self.clear_scene()
