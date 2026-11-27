from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Texas(VoiceoverScene):
    def construct(self):
        card(self, 6, "February 2021", "What happens when a market runs out of power?", "Chapter six. February 2021.",
             lit=("change", "state"))
        self.hours()
        self.fleet()
        self.why()
        self.cost()

    def hours(self):
        T = R["texas"]
        t, fc, dm = T["t"], T["forecast"], T["demand"]
        sel = [i for i, x in enumerate(t) if 8 <= x <= 22]
        pa = viz.plot_axes([8, 22], [0, 80000], x_length=10.0, y_length=4.4, xticks=[8, 10, 12, 14, 16, 18, 20, 22],
                           yticks=[20000, 40000, 60000, 80000], xfmt=lambda v: f"{int(v)} Feb", yfmt=lambda v: f"{v / 1000:.0f} GW",
                           ylabel="ERCOT, hour by hour", size=14).move_to([-0.3, -0.5, 0])
        lf = poly(pa, [(t[i], fc[i]) for i in sel if fc[i]], GREY_B, 2.5)
        ld = poly(pa, [(t[i], dm[i]) for i in sel if dm[i]], WHITE, 3.5)
        gap = Polygon(*[pa.ax.c2p(t[i], fc[i]) for i in sel if fc[i] and dm[i] and 14.9 <= t[i] <= 19],
                      *[pa.ax.c2p(t[i], dm[i]) for i in reversed(sel) if fc[i] and dm[i] and 14.9 <= t[i] <= 19],
                      stroke_width=0, fill_color=BAD, fill_opacity=0.4)
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=GREY_B, stroke_width=3), tx("demand ERCOT had forecast", 15, GREY_B)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=WHITE, stroke_width=4), tx("demand it actually served", 15, WHITE)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_width=0, fill_color=BAD, fill_opacity=0.5), tx("the gap: customers in the dark", 15, BAD)).arrange(RIGHT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.8, 2.4, 0])
        facts = VGroup(tx(f"rotating outages ordered: up to {T['shed']:,.0f} MW at the worst point,", 15, BAD),
                       tx("7:15 p.m., 15 February: the largest in US history", 15, BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.6, 2.5, 0])
        head = tx("Texas, February 2021", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("EIA, Hourly Electric Grid Monitor (EIA-930), ERCOT; FERC-NERC staff report (November 2021)", size=13)
        with self.voiceover(
            "In February 2021, a mass of Arctic air settled over Texas for a week. <bookmark mark='a'/> This is what ERCOT, "
            "which runs the grid for most of the state, expected its customers to use, hour by hour. As the cold set in, "
            "demand climbed towards a winter record. <bookmark mark='b'/> And this is what it could actually serve. In the "
            "early hours of Monday the fifteenth, the two lines split. Plants were tripping faster than operators could "
            "replace them, and to save the grid they ordered rolling outages. <bookmark mark='c'/> At the worst point, "
            f"{T['shed']:,.0f} megawatts of customers were cut off, the largest controlled outage in American history. "
            "The gap stayed open for three days."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lf), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ld), FadeIn(key[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(gap), FadeIn(key[2]), FadeIn(facts))
        self.clear_scene()

    def fleet(self):
        T = R["texas"]
        mix = T["mix"]
        i0 = 13 * 24 + 18          # 14 February, the hour ending 7 p.m.
        i1 = 14 * 24 + 19          # 15 February, the hour ending 8 p.m.
        fuels = [("gas", GAS), ("coal", COAL), ("wind", WIND), ("nuclear", NUKE)]
        bars = VGroup()
        for j, (f, col) in enumerate(fuels):
            a_, b_ = mix[f][i0], mix[f][i1]
            y = 1.6 - 1.0 * j
            ba = Rectangle(width=a_ / 50000 * 6.0, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.4).move_to([-2.2, y + 0.17, 0], aligned_edge=LEFT)
            bb = Rectangle(width=max(b_ / 50000 * 6.0, 0.02), height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([-2.2, y - 0.17, 0], aligned_edge=LEFT)
            lab = tx(FUEL_NAME[f], 17, col, bold=True).next_to([-2.35, y, 0], LEFT, buff=0.0)
            va = tx(f"{a_ / 1000:.1f} GW", 13, GREY_B).next_to(ba, RIGHT, buff=0.08)
            vb = tx(f"{b_ / 1000:.1f} GW", 14, col, bold=True).next_to(bb, RIGHT, buff=0.08)
            bars.add(VGroup(lab, ba, va, bb, vb))
        key = VGroup(tx("faint: Sunday 14 February, 7 p.m.", 15, GREY_B), tx("solid: Monday 15 February, 8 p.m.", 15, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, 2.6, 0])
        tot = tx(f"ERCOT averaged {T['unavail']:,.0f} MW of generation unavailable for over two days:", 15, GREY_A)
        tot2 = tx(f"nearly half its all-time winter peak of {T['winter_peak']:,.0f} MW", 15, GREY_A)
        totg = VGroup(tot, tot2).arrange(DOWN, buff=0.04).to_edge(DOWN, buff=0.6)
        src = source("EIA-930, ERCOT net generation by source; FERC-NERC staff report", size=13)
        with self.voiceover(
            "Where did the power go? Compare Sunday evening with Monday evening. <bookmark mark='a'/> Gas, the backbone, "
            f"fell by about {100 * (1 - mix['gas'][i1] / mix['gas'][i0]):.0f} per cent, as wells, pipelines and plants froze. "
            "<bookmark mark='b'/> Coal fell too, as instruments and lines at the plants froze. Wind, already low, fell "
            f"to almost nothing. <bookmark mark='c'/> Even nuclear output fell, by about "
            f"{100 * (1 - mix['nuclear'][i1] / mix['nuclear'][i0]):.0f} per cent. <bookmark mark='d'/> Over two days, the federal report found, "
            f"ERCOT averaged {T['unavail'] / 1000:.0f} gigawatts of generation that could not run: nearly half of its "
            "record winter demand."
        ) as vo:
            self.play(FadeIn(key), FadeIn(src), *[FadeIn(b_[0]) for b_ in bars],
                      *[AnimationGroup(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2])) for b_ in bars], run_time=1.5)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][3], LEFT), FadeIn(bars[0][4]))
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(bars[k][3], LEFT), FadeIn(bars[k][4])) for k in (1, 2)])
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3][3], LEFT), FadeIn(bars[3][4]))
            vo.wait_until("d")
            self.play(FadeIn(totg, shift=UP * 0.1))
        self.clear_scene()

    def why(self):
        T = R["texas"]
        causes = [("freezing", T["freezing"], WIND), ("fuel supply", T["fuel"], GAS), ("other causes", 100 - T["freezing"] - T["fuel"], OTHER)]
        ring = VGroup()
        start = PI / 2
        for name, v, col in causes:
            ang = -TAU * v / 100
            ring.add(AnnularSector(inner_radius=1.0, outer_radius=1.8, angle=ang, start_angle=start, fill_color=col, fill_opacity=0.9,
                                   stroke_color="#0E1117", stroke_width=2).move_arc_center_to([-3.4, -0.3, 0]))
            start += ang
        labs = VGroup(tx(f"freezing: {T['freezing']:.0f}%", 18, WIND, bold=True).move_to([-0.6, 1.4, 0]),
                      tx(f"fuel: {T['fuel']:.0f}%", 18, GAS, bold=True).move_to([-6.2, -1.6, 0]),
                      tx(f"other: {100 - T['freezing'] - T['fuel']:.0f}%", 16, GREY_B).move_to([-6.0, 1.6, 0]))
        center = VGroup(tx(f"{T['units']:,.0f}", 24, WHITE, bold=True), tx("units", 14, GREY_A)).arrange(DOWN, buff=0.04).move_to([-3.4, -0.3, 0])
        side = VGroup(tx("The units that failed:", 18, WHITE, bold=True),
                      tx(f"{T['gas_units']:.0f}% gas, 27% wind, 6% coal, 2% solar", 16, GREY_A),
                      tx("Natural gas supply: 87% of the fuel problems", 16, GAS),
                      tx("The fixes recommended after a 2011 cold snap", 16, GREY_A),
                      tx(f"were voluntary; over {get('nerc.not_adopted'):.0f}% of plant owners in the", 16, GREY_A),
                      tx("worst-hit regions had not adopted them", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, -0.3, 0])
        head = tx("Why plants failed, 8-20 February 2021", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("FERC-NERC staff report, 'The February 2021 Cold Weather Outages in Texas and the South Central United States'", size=13)
        with self.voiceover(
            f"The federal investigators counted {T['units']:,.0f} generating units that failed, were cut back, or could not "
            "start. <bookmark mark='a'/> The biggest cause was the cold itself: frozen pipes, valves and instruments. "
            "<bookmark mark='b'/> Next, fuel: mostly natural gas that never arrived, because the wells and gathering lines "
            "that feed the plants had frozen too. <bookmark mark='c'/> Every kind of plant failed, gas most of all, "
            "because there are most of them. And much of it had been seen before. After a cold snap in 2011, investigators "
            "had recommended winter fixes; they were voluntary, and over forty per cent of the plant owners in the "
            "worst-hit regions told the 2021 investigators they had not adopted them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(center))
            vo.wait_until("a")
            self.play(FadeIn(ring[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(FadeIn(ring[1]), FadeIn(labs[1]), FadeIn(ring[2]), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()

    def cost(self):
        T = R["texas"]
        people = VGroup(*[draw.person(0.35, GREY_B) for _ in range(45)]).arrange_in_grid(rows=3, buff=0.12).move_to([-3.2, 1.3, 0])
        pl = tx(f"{T['people']:.1f} million Texans lost power, some for four days", 18, WHITE, bold=True).next_to(people, DOWN, buff=0.2)
        dl = tx(f"at least {T['deaths']:.0f} people died, most in connection with the outages", 18, BAD, bold=True).next_to(pl, DOWN, buff=0.15)
        price = VGroup(tx("The price", 20, PRICE, bold=True),
                       tx(f"held at the ${T['voll']:,.0f} cap until 19 February,", 16, GREY_A),
                       tx("a day and a half after the outages ended", 16, GREY_A),
                       tx(f"the power sold in that week: worth ${T['value']:.0f} billion", 16, PRICE, bold=True),
                       tx(f"ERCOT's average price for 2021: ${T['price21']:.0f} a MWh,", 16, GREY_A),
                       tx(f"against ${T['price20']:.0f} in 2020", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 0.6, 0])
        lesson = tx("An energy-only market pays for scarcity; it does not, by itself, pay for winterizing.", 17, GOLD, bold=True).to_edge(
            DOWN, buff=0.6)
        src = source("FERC-NERC staff report (2021); Potomac Economics, 2021 State of the Market Report for ERCOT", size=13)
        with self.voiceover(
            f"The human cost: more than {T['people']:.1f} million people in Texas lost power, some for four days, in "
            f"freezing homes. <bookmark mark='a'/> At least {T['deaths']:.0f} people died, most of them in connection with "
            "the outages. <bookmark mark='b'/> And the market? The price sat at the cap, nine thousand dollars a "
            "megawatt-hour, and was held there until the nineteenth, a day and a half after the last outages were "
            f"ended. The market monitor valued the week's electricity at {T['value']:.0f} billion dollars. "
            "<bookmark mark='c'/> Texas runs what is called an energy-only market: plants are paid only for the power they "
            "sell, and the high prices of scarce hours are meant to pay for being ready. In February 2021 the prices were "
            "as high as they could go, and the plants still were not ready."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(p_, scale=0.6) for p_ in people], lag_ratio=0.02), FadeIn(pl), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(price, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
