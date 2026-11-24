from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Critical(VoiceoverScene):
    def construct(self):
        card(self, 11, "Critical minerals", "Why do governments now treat some metals like oil?",
             "Chapter eleven. Critical minerals.", lit=("moat", "change"))
        self.concentration()
        self.lithium()
        self.rare()

    def concentration(self):
        rows = [("cobalt", "Congo", get("usgs.co.congo") / 100, "#5DA9E9"),
                ("rare earths", "China", get("usgs.ree.china") / get("usgs.ree.world"), CHINA),
                ("nickel", "Indonesia", get("usgs.ni.indonesia") / 3900, "#7EC8F5"),
                ("iron ore", "Australia", get("usgs.fe.australia") / get("usgs.fe.world"), IRON),
                ("lithium", "Australia", get("usgs.li.australia") / get("usgs.li.world"), LITH),
                ("copper", "Chile", get("usgs.cu.mine.chl") / get("usgs.cu.mine"), COPPER)]
        W = 7.0
        bars = VGroup()
        for k, (metal, who, share, col) in enumerate(rows):
            y = 2.0 - 0.75 * k
            bg = Rectangle(width=W, height=0.48, stroke_color=GREY_D, stroke_width=1, fill_opacity=0).move_to(
                [0.9, y, 0])
            fg = Rectangle(width=W * share, height=0.48, stroke_width=0, fill_color=col, fill_opacity=0.85).align_to(
                bg, LEFT).set_y(y)
            name = tx(metal, 20, col, bold=True).next_to(bg, LEFT, buff=0.3)
            lab = tx(f"{who} {100 * share:.0f}%", 17, WHITE, bold=True).next_to(fg, RIGHT, buff=0.12)
            bars.add(VGroup(bg, fg, name, lab))
        half = DashedLine([0.9 - W / 2 + W / 2, 2.5, 0], [0.9, -2.0, 0], stroke_color=GREY_B, stroke_width=1.2)
        hl = tx("half the world", 14, GREY_B).next_to(half, UP, buff=0.05)
        head = tx("The largest producer's share of world mining, 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        conds = VGroup()
        for k, (t1, t2, ic) in enumerate([("modern life needs it", "wires, batteries, magnets, steel",
                                           draw.battery(0.8, LITH, 0.8)),
                                          ("nothing easily replaces it", "substitutes cost more or work worse",
                                           VGroup(Circle(0.35, stroke_color=STATE, stroke_width=4),
                                                  Line(LEFT * 0.25 + DOWN * 0.25, RIGHT * 0.25 + UP * 0.25,
                                                       stroke_color=STATE, stroke_width=4))),
                                          ("supply sits in a few places", "and could be cut off",
                                           VGroup(*[Dot(radius=0.12, color=CHINA) for _ in range(3)]).arrange(
                                               RIGHT, buff=0.08))]):
            box = RoundedRectangle(corner_radius=0.12, width=3.8, height=2.6, stroke_color=GREY_B, stroke_width=1.2,
                                   fill_color="#141A24", fill_opacity=1)
            inner = VGroup(ic, tx(t1, 19, WHITE, bold=True), tx(t2, 15, GREY_A)).arrange(DOWN, buff=0.18).move_to(box)
            conds.add(VGroup(box, inner))
        conds.arrange(RIGHT, buff=0.35).move_to([0, 0.1, 0])
        crit = VGroup(tx("Copper joined the US list of critical minerals", 17, WHITE),
                      tx("on 7 November 2025.", 17, COPPER, bold=True)).arrange(DOWN, buff=0.04).move_to([0.9, -2.75, 0])
        src = source("US Geological Survey, Mineral Commodity Summaries 2026 (cobalt, rare earths, nickel, iron ore, "
                     "lithium, copper)", size=13)
        with self.voiceover(
            "A mineral becomes critical when three things are true: modern life needs it, there is no easy substitute, "
            "and its supply is concentrated in a few places that could be cut off. <bookmark mark='a'/> Here is the "
            "third condition, measured. For each metal, the share of the world's mining done by its largest producer. "
            f"Congo mines about {100 * rows[0][2]:.0f} percent of the world's cobalt. China mines about "
            f"{100 * rows[1][2]:.0f} percent of the rare earths, and Indonesia about two-thirds of the nickel. "
            "<bookmark mark='b'/> Iron ore, lithium and copper are spread more widely, at least at the mine. But "
            "remember the refining: China refines almost half the world's copper, and much larger shares of lithium, "
            "cobalt and rare earths. <bookmark mark='c'/> On the seventh of November 2025, copper itself was added to "
            "the United States' official list of critical minerals. The metal of wires is now treated as a matter of "
            "national security."
        ) as vo:
            self.play(FadeIn(src))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in conds], lag_ratio=0.6), run_time=3.5)
            vo.wait_until("a")
            self.play(FadeOut(conds), FadeIn(head))
            self.play(Create(half), FadeIn(hl))
            for b in bars[:3]:
                self.play(FadeIn(b[0]), FadeIn(b[2]), GrowFromEdge(b[1], LEFT), FadeIn(b[3]), run_time=0.9)
            vo.wait_until("b")
            for b in bars[3:]:
                self.play(FadeIn(b[0]), FadeIn(b[2]), GrowFromEdge(b[1], LEFT), FadeIn(b[3]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(crit, shift=UP * 0.1))
        self.clear_scene()

    def lithium(self):
        L = R["lithium"]
        ys = [2021, 2022, 2023, 2024, 2025]
        pa = viz.plot_axes([2020.4, 2025.6], [0, 70000], x_length=4.8, y_length=3.6, xticks=ys,
                           yticks=[20000, 40000, 60000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v / 1000:.0f}k",
                           size=14).move_to([-4.0, 0.0, 0])
        pbars = viz.year_bars(pa, ys, [L["price"][y] for y in ys], LITH, width=0.55)
        plabs = VGroup(*[tx(f"${L['price'][y] / 1000:.1f}k", 13, WHITE).next_to(b, UP, buff=0.05)
                         for y, b in zip(ys, pbars)])
        pt = tx("lithium carbonate, a tonne (real)", 16, LITH).next_to(pa, UP, buff=0.12)
        yrs = list(range(2019, 2026))
        pb = viz.plot_axes([2018.4, 2025.6], [-2, 10], x_length=5.4, y_length=3.6, xticks=[2019, 2021, 2023, 2025],
                           yticks=[0, 4, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=14).move_to(
            [2.6, 0.0, 0])
        rev = viz.year_bars(pb, yrs, [L["alb_revenue"][y] for y in yrs], "#6F8FB8", width=0.36)
        for b in rev:
            b.shift(LEFT * 0.2)
        net = VGroup()
        for y in yrs:
            v = L["alb_net"][y]
            p0, p1 = pb.ax.c2p(y, 0), pb.ax.c2p(y, v)
            net.add(Rectangle(width=0.36, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                              fill_color=GREEN_C if v > 0 else STATE, fill_opacity=0.9).move_to(
                [p0[0] + 0.2, (p0[1] + p1[1]) / 2, 0]))
        zl = Line(pb.ax.c2p(2018.4, 0), pb.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.2)
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color="#6F8FB8", fill_opacity=1), tx("revenue", 14, WHITE)
                            ).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.18, stroke_width=0, fill_color=GREEN_C, fill_opacity=1), tx("profit", 14, WHITE)
                            ).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.18, stroke_width=0, fill_color=STATE, fill_opacity=1), tx("loss", 14, WHITE)
                            ).arrange(RIGHT, buff=0.08)).arrange(RIGHT, buff=0.3).next_to(pb, UP, buff=0.12)
        bt = tx("Albemarle, the largest US lithium producer", 16, WHITE, bold=True).next_to(key, UP, buff=0.1)
        supply = VGroup(tx("world lithium mining", 16, GREY_A),
                        tx(f"{get('usgs.li.world.2024') / 1000:.0f}k t in 2024, {get('usgs.li.world') / 1000:.0f}k t "
                           f"in 2025: +{100 * (get('usgs.li.world') / get('usgs.li.world.2024') - 1):.0f}%", 18, LITH,
                           bold=True)).arrange(DOWN, buff=0.05).move_to([-0.6, -2.7, 0])
        batt = VGroup(draw.battery(0.9, LITH, 0.88), tx(f"{get('usgs.li.batteries'):.0f}% of lithium", 15, WHITE),
                      tx("goes into batteries", 15, WHITE)).arrange(DOWN, buff=0.06).move_to([6.2, -2.4, 0])
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'lithium'; Albemarle, Forms 10-K (SEC)",
                     size=13)
        with self.voiceover(
            "Being critical does not make a metal a good business. Lithium shows why. "
            f"<bookmark mark='a'/> About {get('usgs.li.batteries'):.0f} percent of lithium now goes into batteries, "
            "and when electric car sales took off, battery makers scrambled for it. The price of battery-grade lithium "
            f"carbonate went from about {L['price'][2021] / 1000:.0f} thousand dollars a tonne in 2021 to "
            f"{L['price'][2022] / 1000:.0f} thousand in 2022. <bookmark mark='b'/> Albemarle, the biggest American "
            f"producer, nearly tripled its revenue, to {L['alb_revenue'][2023]:.1f} billion dollars in 2023. "
            "<bookmark mark='c'/> But unlike copper, lithium can be brought into production fast: from brines in "
            "Chile and Argentina, from hard-rock mines in Australia, China, Zimbabwe and Mali. Mines that had been "
            "planned in the boom all came at once. <bookmark mark='d'/> World lithium mining rose by "
            f"{100 * (get('usgs.li.world') / get('usgs.li.world.2024') - 1):.0f} percent in a single year, the price "
            f"collapsed to about {L['price'][2025] / 1000:.0f} thousand dollars, and Albemarle lost money in 2024 and "
            "again in 2025. A critical mineral is critical to its buyers. To its producers it is still a commodity, "
            "with a cost curve and a cycle."
        ) as vo:
            self.play(FadeIn(src), FadeIn(batt))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pt))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pbars[:2]], lag_ratio=0.3), FadeIn(plabs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(pb), Create(zl), FadeIn(key), FadeIn(bt))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_, DOWN), GrowFromEdge(n_, DOWN if
                                                                                         L["alb_net"][y] > 0 else UP))
                                    for r_, n_, y in zip(rev[:5], net[:5], yrs[:5])], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pbars[2:]], lag_ratio=0.3), FadeIn(plabs[2:]))
            vo.wait_until("d")
            self.play(FadeIn(supply, shift=UP * 0.1))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_, DOWN), GrowFromEdge(n_, DOWN if
                                                                                         L["alb_net"][y] > 0 else UP))
                                    for r_, n_, y in zip(rev[5:], net[5:], yrs[5:])], lag_ratio=0.3), run_time=1.5)
        self.clear_scene()

    def rare(self):
        ch, wd, us = get("usgs.ree.china"), get("usgs.ree.world"), get("usgs.ree.usa")
        ring = VGroup()
        a0 = PI / 2
        for share, col in [(ch / wd, CHINA), (us / wd, "#7EC8F5"), (1 - (ch + us) / wd, GREY_D)]:
            ring.add(AnnularSector(inner_radius=0.85, outer_radius=1.4, angle=-TAU * share, start_angle=a0,
                                   fill_color=col, fill_opacity=0.9, stroke_color=BACKGROUND, stroke_width=2))
            a0 -= TAU * share
        ring.move_to([-4.3, 0.5, 0])
        mid = VGroup(tx(f"{wd:.0f}k t", 20, WHITE, bold=True), tx("mined, 2025", 13, GREY_A)).arrange(DOWN, buff=0.03
                                                                                                    ).move_to(ring)
        rk = VGroup(tx(f"China {ch:.0f}k t ({100 * ch / wd:.0f}%)", 16, CHINA, bold=True),
                    tx(f"United States {us:.0f}k t", 16, "#7EC8F5"),
                    tx(f"US imports of rare-earth compounds and metals:", 14, GREY_A),
                    tx(f"{get('usgs.ree.import.china'):.0f}% from China (2021-24)", 14, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(ring, DOWN, buff=0.35)
        uses = VGroup(*[VGroup(Circle(0.32, stroke_color=GREY_B, stroke_width=1.5), tx(t, 13, WHITE)).arrange(
            DOWN, buff=0.06) for t in ("magnets", "wind turbines", "electric motors", "missiles")]).arrange(
            RIGHT, buff=0.35).move_to([2.6, 2.4, 0])
        uses[0][0].add(Rectangle(width=0.3, height=0.16, stroke_width=0, fill_color=CHINA, fill_opacity=1).move_to(
            uses[0][0]))
        uses[1][0].add(draw.wind_turbine(0.5).move_to(uses[1][0]))
        uses[2][0].add(Circle(0.14, stroke_color=COPPER, stroke_width=3).move_to(uses[2][0]))
        uses[3][0].add(Line(LEFT * 0.2 + DOWN * 0.1, RIGHT * 0.2 + UP * 0.1, stroke_color=GREY_A, stroke_width=4).move_to(
            uses[3][0]))
        tl = Line([0.0, -0.4, 0], [5.6, -0.4, 0], stroke_color=GREY_B, stroke_width=2)
        evs = [(0.4, "Apr 2025", "export controls on 7 rare earths", "(samarium, dysprosium, terbium...)"),
               (2.6, "Oct 2025", "5 more added", ""), (4.6, "Nov 2025", "October's controls", "suspended for a year")]
        marks = VGroup()
        for x, d, t1, t2 in evs:
            g = VGroup(Dot([x, -0.4, 0], color=CHINA, radius=0.08), tx(d, 15, CHINA, bold=True).move_to([x, -0.05, 0]),
                       VGroup(tx(t1, 13, WHITE), *([tx(t2, 13, GREY_A)] if t2 else [])).arrange(DOWN, buff=0.03).move_to(
                           [x, -0.95, 0]))
            marks.add(g)
        tt = tx("China's export controls, 2025", 17, WHITE, bold=True).next_to(tl, UP, buff=0.55).align_to(tl, LEFT)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'rare earths'", size=13)
        with self.voiceover(
            "The sharpest case is the rare earths: seventeen elements with odd names that make the strongest permanent "
            "magnets, the ones inside wind turbines, electric motors, hard drives and guided missiles. "
            f"<bookmark mark='a'/> They are not actually rare, but China mines about {100 * ch / wd:.0f} percent of "
            "them and dominates their separation and refining. The United States mines some, at Mountain Pass in "
            f"California, but {get('usgs.ree.import.china'):.0f} percent of its imports of rare-earth compounds and "
            "metals came from China. <bookmark mark='b'/> In April 2025, China put export controls on seven of them. "
            "<bookmark mark='c'/> In October it added five more. <bookmark mark='d'/> In November, it suspended the "
            "October controls for a year, while keeping April's. A single government, by licensing a few hundred "
            "thousand tonnes of oxide, could slow car factories on other continents. That is what makes a mineral "
            "critical: not its price, but who can turn off the tap."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(u_) for u_ in uses], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, scale=0.9) for s_ in ring], lag_ratio=0.3), FadeIn(mid), run_time=1.6)
            self.play(FadeIn(rk))
            self.play(Create(tl), FadeIn(tt))
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(marks[k], shift=UP * 0.1))
        self.clear_scene()
