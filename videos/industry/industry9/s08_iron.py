from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Iron(VoiceoverScene):
    def construct(self):
        card(self, 7, "Iron ore: three companies, one customer", "How did the world's biggest metal market get its price?",
             "Chapter seven. Iron ore: three companies, one customer.", lit=("moat", "dollar"))
        self.where()
        self.calendar()
        self.history()

    def where(self):
        wm = draw.world_map(12.4).move_to([0, 0.1, 0])
        prod = [("Australia", 122, -23, get("usgs.fe.australia")), ("Brazil", -45, -12, get("usgs.fe.brazil")),
                ("India", 79, 22, get("usgs.fe.india")), ("China", 112, 36, get("usgs.fe.china"))]
        bub = VGroup()
        labs = VGroup()
        for name, lo, la, v in prod:
            c = Circle(0.045 * np.sqrt(v / 10), stroke_color=IRON, stroke_width=2, fill_color=IRON,
                       fill_opacity=0.6).move_to(wm.p(lo, la))
            bub.add(c)
            labs.add(VGroup(tx(name, 15, WHITE, bold=True), tx(f"{v:,.0f} Mt", 14, IRON)).arrange(DOWN, buff=0.02
                                                                                                 ).next_to(c, LEFT if lo < 0 else DOWN, buff=0.08))
        tianjin = wm.p(117.7, 39.0)
        port = VGroup(Dot(tianjin, color=PRICE, radius=0.07), tx("Tianjin", 14, PRICE, bold=True).next_to(
            tianjin, UP, buff=0.08))
        ships = VGroup(*[draw.ship(0.5, boxes=0) for _ in range(2)])
        lanes = [VMobject().set_points_smoothly([wm.p(116, -21), wm.p(112, -5), wm.p(120, 18), wm.p(118, 36)]),
                 VMobject().set_points_smoothly([wm.p(-38, -21), wm.p(20, -38), wm.p(80, -8), wm.p(110, 5),
                                                 wm.p(118, 36)])]
        for l_ in lanes:
            l_.set_stroke(GREY_B, 1.5, opacity=0.6)
        for sh, l_ in zip(ships, lanes):
            sh.move_to(l_.get_start())
        world = VGroup(tx(f"world: {get('usgs.fe.world') / 1000:.1f} billion tonnes of iron ore a year", 19, IRON,
                          bold=True),
                       tx(f"Australia and Brazil: {100 * (get('usgs.fe.australia') + get('usgs.fe.brazil')) / get('usgs.fe.world'):.0f}%",
                          17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_corner(DL, buff=0.55)
        price = VGroup(tx("the world price is quoted here:", 15, GREY_A),
                       tx(f"62% iron fines, delivered to Tianjin, 2025: ${get('usgs.fe.price'):.0f} a tonne", 17, PRICE,
                          bold=True)).arrange(DOWN, aligned_edge=RIGHT, buff=0.04).to_corner(DR, buff=0.55)
        head = tx("Iron ore, 2025", 24, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'iron ore' (usable ore); routes illustrative",
                     corner=UL, size=13).shift(DOWN * 0.3)
        with self.voiceover(
            "Copper is the metal of wires. Iron is the metal of everything else: steel for buildings, bridges, ships "
            "and cars. And iron ore is mined on a scale nothing else matches. <bookmark mark='a'/> The world produced "
            f"about {get('usgs.fe.world') / 1000:.1f} billion tonnes of usable iron ore in 2025. Australia alone "
            f"produced {get('usgs.fe.australia'):,.0f} million tonnes, most of it from the Pilbara in the north-west; "
            f"Brazil {get('usgs.fe.brazil'):,.0f}, then India and China. <bookmark mark='b'/> Most of Australia's and "
            "Brazil's ore goes by sea to the steel mills of Asia, and above all to China, which makes more steel than "
            "the rest of the world combined. Three companies, Rio Tinto and BHP in Australia and Vale in Brazil, are the "
            "biggest sellers. <bookmark mark='c'/> You can see who the customer is from where the price is quoted. The "
            "standard price of iron ore is the price of a tonne of fines, sixty-two percent iron, delivered to a port "
            f"in northern China: about {get('usgs.fe.price'):.0f} dollars a tonne in 2025."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(b_) for b_ in bub], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.3), FadeIn(world), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lanes[0]), Create(lanes[1]), run_time=1.5)
            self.play(MoveAlongPath(ships[0], lanes[0]), MoveAlongPath(ships[1], lanes[1]), run_time=5.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(port, scale=1.5), FadeIn(price), Flash(tianjin, color=PRICE))
        self.clear_scene()

    def calendar(self):
        P = R["prices"]
        ms = P["months"]
        fe = P["nominal"]["PIORECRUSDM"]
        y03 = [fe[ms.index(f"2003-{m:02d}")] for m in range(1, 13)]
        y24 = [fe[ms.index(f"2024-{m:02d}")] for m in range(1, 13)]
        mon = "JFMAMJJASOND"

        def panel(vals, title, col, top):
            box = RoundedRectangle(corner_radius=0.12, width=5.6, height=4.2, stroke_color=GREY_B, stroke_width=1.2,
                                   fill_color="#141A24", fill_opacity=1)
            bars = VGroup()
            for k, v in enumerate(vals):
                h = 2.6 * v / top
                bars.add(VGroup(Rectangle(width=0.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9),
                                tx(mon[k], 13, GREY_B)))
            for k, b in enumerate(bars):
                b[0].move_to([-2.4 + 0.44 * k, -1.4 + b[0].height / 2, 0])
                b[1].move_to([-2.4 + 0.44 * k, -1.62, 0])
            t = tx(title, 19, WHITE, bold=True).move_to([0, 1.75, 0])
            g = VGroup(box, bars, t)
            bars.shift(RIGHT * 0.0)
            return g
        a = panel(y03, f"2003: one price, all year (${y03[0]:.2f})", IRON, 140).move_to([-3.4, -0.2, 0])
        b = panel(y24, "2024: a new price every month", IRON, 140).move_to([3.4, -0.2, 0])
        b_rng = tx(f"from ${min(y24):.0f} to ${max(y24):.0f}", 16, GREY_A).next_to(b[2], DOWN, buff=0.1)
        a_note = tx("set once a year, by negotiation", 16, GREY_A).next_to(a[2], DOWN, buff=0.1)
        head = tx("Iron ore's price, month by month, dollars a tonne", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("IMF primary commodity prices via FRED (PIORECRUSDM); Vale, 'Vale on iron ore pricing', 1 April 2010",
                     size=13)
        with self.voiceover(
            "That daily, delivered-to-China price is new. <bookmark mark='a'/> For about forty years, until the late "
            "2000s, iron ore had one price a year. The big miners and the big steelmakers negotiated a benchmark "
            "each year, and everyone else followed it. Look at 2003: the same price in every month, "
            f"{y03[0]:.2f} dollars a tonne. <bookmark mark='b'/> Then China's steel industry grew so fast that much of "
            "its ore was bought on the spot market, at prices far above the benchmark, and the miners wanted those "
            "prices too. On the first of April 2010, Vale announced that almost all its customers, ninety-seven percent "
            "of them, had agreed to prices tied to the spot market and changed every quarter. The annual benchmark was "
            "finished. <bookmark mark='c'/> Now look at 2024: a different price every month, from "
            f"{min(y24):.0f} to {max(y24):.0f} dollars. The risk that used to be negotiated away once a year is now "
            "carried by both sides, every day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(a[0]), FadeIn(a[2]), FadeIn(a_note))
            self.play(LaggedStart(*[GrowFromEdge(x[0], DOWN) for x in a[1]], lag_ratio=0.08), FadeIn(
                VGroup(*[x[1] for x in a[1]])), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(b[0]), FadeIn(b[2]), FadeIn(b_rng))
            self.play(LaggedStart(*[GrowFromEdge(x[0], DOWN) for x in b[1]], lag_ratio=0.08), FadeIn(
                VGroup(*[x[1] for x in b[1]])), run_time=1.6)
        self.clear_scene()

    def history(self):
        P = R["prices"]
        I_ = R["iron"]
        ms = P["months"]
        fe = P["nominal"]["PIORECRUSDM"]
        xs = [mx(m) for m in ms]
        pa = viz.plot_axes([1992, 2027], [0, 240], x_length=10.6, y_length=4.6, xticks=[1995, 2000, 2005, 2010, 2015,
                                                                                         2020, 2025],
                           yticks=[50, 100, 150, 200], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=15
                           ).move_to([0, -0.4, 0])
        line = VMobject(stroke_color=IRON, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(x, v) for x, v in zip(xs, fe) if v is not None])
        band = Rectangle(width=pa.ax.c2p(2008, 0)[0] - pa.ax.c2p(1992, 0)[0], height=4.6, stroke_width=0,
                         fill_color=GREY_B, fill_opacity=0.08).move_to(
            [(pa.ax.c2p(2008, 0)[0] + pa.ax.c2p(1992, 0)[0]) / 2, pa.ax.c2p(0, 120)[1], 0])
        bl = tx("the benchmark years:\none price a year", 16, GREY_A).move_to(pa.ax.c2p(2000, 150))
        vale = DashedLine(pa.ax.c2p(2010.25, 0), pa.ax.c2p(2010.25, 230), stroke_color=GREY_B, stroke_width=1.5)
        vl = VGroup(tx("April 2010:", 14, GREY_A), tx("Vale moves to", 14, GREY_A), tx("quarterly prices", 14, GREY_A)
                    ).arrange(DOWN, aligned_edge=RIGHT, buff=0.03).next_to(pa.ax.c2p(2010.25, 215), LEFT, buff=0.1)
        pk = Dot(pa.ax.c2p(mx(I_["peak"]), I_["peak_val"]), color=WHITE, radius=0.07)
        pkl = tx(f"{mlabel(I_['peak'])}: ${I_['peak_val']:.0f}", 16, WHITE, bold=True).next_to(pk, UP, buff=0.1)
        p03 = Dot(pa.ax.c2p(2003.5, I_["p2003"]), color=WHITE, radius=0.07)
        p03l = tx(f"2003: ${I_['p2003']:.0f}", 16, WHITE, bold=True).next_to(p03, UP, buff=0.1)
        last = Dot(pa.ax.c2p(xs[-1], fe[-1]), color=PRICE, radius=0.07)
        lastl = tx(f"{mlabel(ms[-1])}: ${fe[-1]:.0f}", 16, PRICE, bold=True).next_to(last, DOWN, buff=0.12)
        head = tx("Iron ore, dollars a tonne, 1992-2026", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("IMF primary commodity prices via FRED (PIORECRUSDM), nominal dollars", size=13)
        with self.voiceover(
            "Here is the whole story in one line. <bookmark mark='a'/> Through the 1990s, iron ore cost about "
            "twelve to fifteen dollars a tonne, and the benchmark barely moved. <bookmark mark='b'/> Then China's "
            "boom. From fourteen dollars in 2003 the price rose more than tenfold in eight years. "
            "<bookmark mark='c'/> After 2010 it moved every month, falling to the fifties in 2015 and 2016, then "
            f"soaring to a peak of {I_['peak_val']:.0f} dollars in June 2021. <bookmark mark='d'/> It is now about "
            f"{fe[-1]:.0f}. For the miners of the Pilbara, whose ore is among the cheapest in the world to dig and "
            "ship, even that is a very good price. Iron ore has been the richest business in mining for twenty years, "
            "and almost all of that wealth came from one customer."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(band), FadeIn(bl))
            vo.wait_until("a")
            n03 = ms.index("2004-01")
            part1 = VMobject(stroke_color=IRON, stroke_width=3).set_points_as_corners(
                [pa.ax.c2p(x, v) for x, v in zip(xs[:n03], fe[:n03])])
            self.play(Create(part1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(p03, scale=2), FadeIn(p03l))
            n11 = ms.index("2011-06")
            part2 = VMobject(stroke_color=IRON, stroke_width=3).set_points_as_corners(
                [pa.ax.c2p(x, v) for x, v in zip(xs[n03 - 1:n11], fe[n03 - 1:n11])])
            self.play(Create(part2), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(vale), FadeIn(vl))
            n21 = ms.index("2021-07")
            part3 = VMobject(stroke_color=IRON, stroke_width=3).set_points_as_corners(
                [pa.ax.c2p(x, v) for x, v in zip(xs[n11 - 1:n21], fe[n11 - 1:n21])])
            self.play(Create(part3), run_time=3.0)
            self.play(FadeIn(pk, scale=2), FadeIn(pkl))
            vo.wait_until("d")
            part4 = VMobject(stroke_color=IRON, stroke_width=3).set_points_as_corners(
                [pa.ax.c2p(x, v) for x, v in zip(xs[n21 - 1:], fe[n21 - 1:])])
            self.play(Create(part4), run_time=2.0)
            self.play(FadeIn(last, scale=2), FadeIn(lastl))
        self.clear_scene()
