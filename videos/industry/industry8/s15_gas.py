from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

HH, EU, ASIA = GAS, BRENT, PRICE


class Gas(VoiceoverScene):
    def construct(self):
        card(self, 13, "Gas, and the ships that made it global", "Why did gas cost eight times as much in Europe as in Texas?",
             "Chapter thirteen. Gas, and the ships that made it global.", lit=("unit", "change"))
        self.prices()
        self.chain()
        self.exports()

    def prices(self):
        G = R["gas"]
        ms = G["months"]
        pa = viz.plot_axes([2010, 2027], [0, 75], x_length=9.4, y_length=4.4, xticks=[2010, 2014, 2018, 2022, 2026],
                           yticks=[20, 40, 60], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=14)
        pa.move_to([0.3, -0.5, 0])

        def line(vals, col):
            return VMobject(stroke_color=col, stroke_width=3.5).set_points_as_corners(
                [pa.ax.c2p(mx(m), v) for m, v in zip(ms, vals) if v is not None])
        lh, le, la = line(G["hh"], HH), line(G["eu"], EU), line(G["asia"], ASIA)
        key_ = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.3, stroke_color=c, stroke_width=4), tx(n, 15, c)).arrange(RIGHT, buff=0.1)
                        for n, c in (("Henry Hub, Louisiana", HH), ("Europe", EU), ("Asia, LNG", ASIA))]).arrange(
            RIGHT, buff=0.5).next_to(pa, UP, buff=0.15)
        unit = tx("dollars per million British thermal units", 14, GREY_B).next_to(pa, DOWN, buff=0.1).align_to(pa, LEFT)
        pk = G["eu_peak"]
        lab = tx(f"{mlabel(pk)}: Europe ${G['eu_peak_val']:.0f}, Louisiana ${G['hh_at_peak']:.1f}", 18, WHITE, bold=True).next_to(
            pa.ax.c2p(mx(pk), G["eu_peak_val"]), LEFT, buff=0.2)
        src = source("FRED: Henry Hub spot (EIA); the IMF's global prices of natural gas, Europe, and of LNG, Asia; monthly",
                     size=13)
        with self.voiceover(
            "Natural gas comes out of the same rocks as oil, often from the same wells. But for most of its history "
            "it has had not one price but several. <bookmark mark='a'/> In Louisiana, at the pipeline hub called Henry "
            "Hub, gas has mostly cost a few dollars per million British thermal units. <bookmark mark='b'/> In Europe "
            "and in Asia it usually cost two or three times as much. <bookmark mark='c'/> And in 2022, after Russia "
            "invaded Ukraine and most of its pipeline gas to Europe stopped, Europe's price rose to "
            f"{G['eu_peak_val']:.0f} dollars, while in Louisiana it was {G['hh_at_peak']:.0f}. The same molecules, "
            "eight times the price. Why didn't traders just ship the cheap gas to the dear market?"
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(key_), FadeIn(unit))
            vo.wait_until("a")
            self.play(Create(lh), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(le), Create(la), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(lab))
        self.clear_scene()

    def chain(self):
        well = draw.derrick(1.2, color=GAS).move_to([-6.0, 0.4, 0])
        plant = VGroup(*[draw.tank(0.6, 0.8, color="#E8EAED") for _ in range(2)]).arrange(RIGHT, buff=0.1).move_to([-3.6, 0.0, 0])
        ship = VGroup(draw.tanker(2.2, color="#5B6372"),
                      *[Circle(radius=0.16, stroke_width=0, fill_color="#E8EAED", fill_opacity=1).move_to([x, 0.33, 0])
                        for x in (-0.6, -0.2, 0.2)]).move_to([0.2, -0.1, 0])
        regas = draw.tank(0.7, 0.4, color="#E8EAED").move_to([3.6, 0.0, 0])
        city = draw.skyline(1.6, seed=3).scale(0.8).move_to([5.8, 0.3, 0])
        steps = [well, plant, ship, regas, city]
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.12, stroke_width=3, color=GREY_C,
                                max_tip_length_to_length_ratio=0.2) for k in range(4)])
        labs = VGroup(tx("gas well", 15, GAS), tx("liquefaction: chilled", 15, WHITE), tx("to about -162 C", 15, WHITE),
                      tx("LNG carrier", 15, WHITE), tx("regasification", 15, WHITE), tx("homes, power, industry", 15, GREY_A))
        labs[0].next_to(well, DOWN, buff=0.2)
        VGroup(labs[1], labs[2]).arrange(DOWN, buff=0.03).next_to(plant, DOWN, buff=0.2)
        labs[3].next_to(ship, DOWN, buff=0.2)
        labs[4].next_to(regas, DOWN, buff=0.2)
        labs[5].next_to(city, DOWN, buff=0.2)
        shrink = tx("a six-hundredth of the volume", 18, PRICE, bold=True).next_to(plant, UP, buff=0.4)
        head = tx("Liquefied natural gas: a gas turned into a cargo", 24, WHITE, bold=True).to_edge(UP, buff=0.5)
        tag = estimate_tag("illustrative chain", corner=DR, size=14)
        with self.voiceover(
            "Because gas is hard to move. <bookmark mark='a'/> Oil is a liquid you can pour into any tanker. Gas fills "
            "pipes, and pipes stop at the coast. <bookmark mark='b'/> To cross an ocean it has to be cooled to about "
            "minus a hundred and sixty-two degrees, when it becomes a liquid, about six hundred times smaller. That "
            "takes a plant costing billions of dollars. <bookmark mark='c'/> Then special ships with insulated tanks, "
            "<bookmark mark='d'/> and at the other end a terminal to warm it back into gas. <bookmark mark='e'/> Each "
            "step costs money, so the gap between the cheap market and the dear one has to be wide enough to pay for "
            "the chain. Until enough plants and ships exist, the gap can stay open for years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(well), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(plant))
            vo.wait_until("b")
            self.play(FadeIn(labs[1:3]), FadeIn(shrink))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(ship, shift=RIGHT * 0.3), FadeIn(labs[3]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(regas), FadeIn(labs[4]))
            vo.wait_until("e")
            self.play(GrowArrow(arrows[3]), FadeIn(city), FadeIn(labs[5]))
        self.clear_scene()

    def exports(self):
        G = R["gas"]
        lng = G["lng"]
        ys = sorted(lng)
        pa = viz.plot_axes([2013.4, 2025.6], [0, 16], x_length=6.2, y_length=3.8, xticks=[2014, 2016, 2018, 2020, 2022, 2024],
                           yticks=[5, 10, 15], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}", size=13)
        pa.move_to([-3.0, -0.5, 0])
        bars = VGroup()
        for y in ys:
            v = lng[y] * 1000 / 365  # bcf a day
            p0, p1 = pa.ax.c2p(y - 0.35, 0), pa.ax.c2p(y + 0.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=HH,
                               fill_opacity=0.9).move_to((p0 + p1) / 2))
        ha = tx("US LNG exports, billion cubic feet a day", 17, HH, bold=True).next_to(pa, UP, buff=0.15)
        lab = tx(f"2025: {G['lng_bcfd_2025']:.1f}", 18, WHITE, bold=True).next_to(bars[-1], UP, buff=0.1)
        lngco = R["companies"]["LNG"]["revenue"]
        cy = [y for y in sorted(lngco) if y >= 2016]
        pb = viz.plot_axes([2015.4, 2025.6], [0, 36], x_length=4.6, y_length=3.0, xticks=[2016, 2020, 2024],
                           yticks=[10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=12)
        pb.move_to([3.9, -0.3, 0])
        lb = VMobject(stroke_color=PRICE, stroke_width=4).set_points_as_corners([pb.ax.c2p(y, lngco[y]) for y in cy])
        hb = tx("Cheniere Energy, revenue", 16, PRICE, bold=True).next_to(pb, UP, buff=0.12)
        src = source("EIA, liquefied US natural gas exports (annual); Cheniere Energy, Forms 10-K (SEC company facts)",
                     size=13)
        with self.voiceover(
            "America built that chain. <bookmark mark='a'/> Its first big export plant, on the Louisiana coast, "
            "shipped its first cargoes in 2016. <bookmark mark='b'/> By 2025 the country was exporting about "
            f"{G['lng_bcfd_2025']:.0f} billion cubic feet of liquefied gas a day; since 2023 it has been the world's "
            "largest exporter. "
            "<bookmark mark='c'/> Cheniere, the company that built that first plant, saw its revenue nearly double "
            f"in 2022, to {lngco[2022]:.0f} billion dollars, as Europe bid for every cargo. Shale gas from Texas and "
            "Pennsylvania now sets a floor under prices in Europe and Asia: the price of gas at Henry Hub, plus the "
            "cost of the chain. Gas is becoming, slowly, one market, the way oil already is."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(ha))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:4]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[4:]], lag_ratio=0.2), run_time=2.4)
            self.play(FadeIn(lab))
            vo.wait_until("c")
            self.play(FadeIn(pb), FadeIn(hb), Create(lb), run_time=2.0)
        self.clear_scene()
