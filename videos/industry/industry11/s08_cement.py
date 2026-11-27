from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Cement(VoiceoverScene):
    def construct(self):
        card(self, 7, "Cement: a circle on the map", "Why is cement made almost everywhere, by a few companies in each place?",
             "Chapter seven. Cement: a circle on the map.", lit=("make", "moat"))
        self.kiln()
        self.world()
        self.circle()

    def kiln(self):
        C = R["cement"]
        k = draw.rotary_kiln(6.0).move_to([0.4, -0.6, 0])
        q = draw.pile(1.1, "#C9C2B0", 70, 8, "jagged").move_to([5.6, -2.3, 0])
        ql = VGroup(tx("limestone and clay", 15, CEMENT, bold=True), tx("from a quarry next door", 12, GREY_A)).arrange(
            DOWN, buff=0.02).next_to(q, DOWN, buff=0.05)
        tl = VGroup(tx("preheater tower", 15, WHITE, bold=True), tx("hot gases warm the raw meal", 12, GREY_A)).arrange(
            DOWN, buff=0.02).next_to(k.tower, UP, buff=0.1)
        kl = VGroup(tx("rotary kiln, about 1,450 °C", 16, MOLTEN, bold=True), tx("turning slowly, sloping down to the flame",
                                                                              12, GREY_A)).arrange(DOWN, buff=0.02).next_to(
            k.tube, UP, buff=0.35)
        cl = draw.pile(0.9, "#4A505C", 50, 9, "round").move_to([-5.2, -2.3, 0])
        cll = VGroup(tx("clinker", 16, STEELC, bold=True), tx("ground with a little gypsum: cement", 12, GREY_A)).arrange(
            DOWN, buff=0.02).next_to(cl, DOWN, buff=0.05)
        start, end = k.tube.get_right() + LEFT * 0.3, k.tube.get_left() + RIGHT * 0.3
        dots = VGroup(*[Dot(radius=0.06, color="#E8D7B8") for _ in range(10)])
        t = ValueTracker(0)

        def place(m):
            for i, d in enumerate(m):
                f = ((t.get_value() + i / len(m)) % 1.0)
                d.move_to(start + (end - start) * f + UP * 0.02 * np.sin(12 * f))
                d.set_color(interpolate_color(ManimColor("#E8D7B8"), ManimColor(MOLTEN), f))
        dots.add_updater(place)
        chem = VGroup(tx("CaCO3  →  CaO  +  CO2", 26, WHITE, bold=True),
                      tx("limestone  →  lime  +  carbon dioxide", 15, GREY_A),
                      tx(f"about {C['calcination']:.2f} t of CO2 from the rock itself in every tonne of clinker,", 15, CARBON),
                      tx("before any fuel is burned", 15, CARBON)).arrange(DOWN, buff=0.06).to_corner(UL, buff=0.45)
        tag = estimate_tag("the chemistry: our arithmetic, with clinker about 65% lime", corner=DR, size=13)
        with self.voiceover(
            "Cement is made in a simpler way than steel, but at a temperature just as fierce. <bookmark mark='a'/> "
            "Limestone and clay come from a quarry, usually right beside the plant, and are crushed into a powder. "
            "<bookmark mark='b'/> The powder falls down a tower, warmed by the hot gases coming up, <bookmark mark='c'/> "
            "and into the kiln: a steel tube lined with brick, as long as a football field, turning slowly and sloping "
            "down towards a flame at about fourteen hundred and fifty degrees. <bookmark mark='d'/> What comes out are "
            "grey nodules called clinker, which are ground with a little gypsum into cement. Mix cement with sand, "
            "gravel and water, and you have concrete. <bookmark mark='e'/> The chemistry has a catch. Heating limestone "
            "splits it into lime and carbon dioxide. About half a tonne of carbon dioxide comes out of the rock itself "
            "for every tonne of clinker, before a single tonne of fuel is burned."
        ) as vo:
            self.play(FadeIn(k), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=LEFT * 0.2), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(tl))
            vo.wait_until("c")
            self.add(dots)
            self.play(FadeIn(kl), t.animate.set_value(1.0), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(t.animate.set_value(2.0), FadeIn(cl, shift=LEFT * 0.2), FadeIn(cll), run_time=3.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(chem, shift=DOWN * 0.1), t.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        dots.clear_updaters()
        self.clear_scene()

    def world(self):
        C = R["cement"]
        vals = [("China", C["china"], CHINA), ("India", C["india"], "#F2C14E"), ("Viet Nam", C["vietnam"], REST),
                ("United States", C["us"], USA), ("rest of the world", C["world"] - C["china"] - C["india"] - C["vietnam"] - C["us"],
                                                  "#3E4553")]
        total = C["world"]
        x0, W_ = -6.0, 12.0
        segs = VGroup()
        x = x0
        for n, v, col in vals:
            w = W_ * v / total
            r_ = Rectangle(width=w, height=1.0, stroke_color="#0E1117", stroke_width=1.5, fill_color=col, fill_opacity=0.9
                           ).move_to([x + w / 2, 1.2, 0])
            lab = VGroup(tx(n, 15 if w > 1.2 else 13, WHITE, bold=True), tx(f"{v:,.0f}", 13, WHITE)).arrange(DOWN, buff=0.02)
            if lab.width > w - 0.05:
                lab.next_to(r_, DOWN, buff=0.15 + 0.55 * (len(segs) % 2))
                lab.shift(LEFT * 0.5 if len(segs) % 2 == 0 else RIGHT * 0.3)
                lab.add(Line(r_.get_bottom(), lab.get_top(), stroke_color=GREY_B, stroke_width=1))
            else:
                lab.move_to(r_)
            segs.add(VGroup(r_, lab))
            x += w
        head = tx(f"The world's cement, 2025: about {total / 1000:.1f} billion tonnes", 24, WHITE, bold=True).to_edge(UP, buff=0.5)
        us = VGroup(tx("In the United States, 2025", 19, USA, bold=True),
                    tx(f"{C['plants']:.0f} plants in 34 states; {C['us']:.0f} million tonnes made", 16, GREY_A),
                    tx(f"${C['price']:.0f} a tonne at the plant (${C['price21']:.0f} in 2021)", 16, PRICE),
                    tx(f"about {C['readymix']:.0f}% sold to ready-mix concrete makers", 16, GREY_A),
                    tx(f"{C['imports']:.0f} million tonnes imported, by sea", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.07).move_to([-2.6, -1.8, 0])
        silo = draw.silo(1.6).move_to([3.6, -1.7, 0])
        truck = draw.mixer_truck(2.0).next_to(silo, RIGHT, buff=0.3).align_to(silo, DOWN)
        src = source("USGS, Mineral Commodity Summaries 2026 (Cement)", size=13)
        with self.voiceover(
            f"The world made about {total / 1000:.1f} billion tonnes of cement in 2025. <bookmark mark='a'/> China, "
            f"{C['china'] / 1000:.1f} billion, nearly half; India, {C['india']:.0f} million; Viet Nam, a hundred million; "
            f"the United States, {C['us']:.0f} million. <bookmark mark='b'/> Unlike steel, almost every country makes "
            f"its own. America has {C['plants']:.0f} cement plants in thirty-four states. A tonne sold for about "
            f"{C['price']:.0f} dollars at the plant in 2025, up from {C['price21']:.0f} in 2021, and most of it went to "
            "companies that mix concrete and deliver it in those turning drums. <bookmark mark='c'/> Some comes in by "
            "ship, to coastal terminals. Almost none travels far by road. And that is the whole economics of cement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(segs[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in segs[1:]], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(us[:4], shift=UP * 0.1), FadeIn(silo), FadeIn(truck, shift=LEFT * 0.3))
            self.play(Rotate(truck.drum, angle=TAU, about_point=truck.drum.get_center()), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(us[4]))
        self.clear_scene()

    def circle(self):
        C = R["cement"]
        mk = C["market"]
        xs, cost, price = mk["x"], mk["cost"], mk["price"]
        pa0 = viz.plot_axes([0, 600], [80, 150], x_length=10.0, y_length=3.6, xticks=[150, 300, 450],
                            yticks=[100, 120, 140], xfmt=lambda v: f"{v - 150:.0f} km", yfmt=lambda v: f"${v:.0f}",
                            ylabel="cost of a tonne delivered", size=13).move_to([0, 0.3, 0])

        class _P:  # plot with plant A at 0 km, drawn 150 km in from the axis
            ax = type("A", (), {"c2p": staticmethod(lambda x, y: pa0.ax.c2p(x + 150, y))})
        pa = _P
        kA = draw.rotary_kiln(1.1).move_to(pa.ax.c2p(0, 80) + DOWN * 0.55)
        kB = draw.rotary_kiln(1.1).move_to(pa.ax.c2p(300, 80) + DOWN * 0.55)
        la, lb = tx("plant A", 14, ORE, bold=True).next_to(kA, DOWN, buff=0.05), tx("plant B", 14, SCRAP, bold=True).next_to(
            kB, DOWN, buff=0.05)
        haul = mk["haul"]
        ca = VMobject(stroke_color=ORE, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(x, 95 + haul * abs(x)) for x in xs if 95 + haul * abs(x) <= 150])
        cb = VMobject(stroke_color=SCRAP, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(x, 95 + haul * abs(x - 300)) for x in xs if 95 + haul * abs(x - 300) <= 150])
        lp = [pa.ax.c2p(x, min(p, 150)) for x, p in zip(xs, price)]
        lc = [pa.ax.c2p(x, c) for x, c in zip(xs, cost)]
        margin = Polygon(*lp, *reversed(lc), stroke_width=0, fill_color=PRICE, fill_opacity=0.3)
        pl = VMobject(stroke_color=PRICE, stroke_width=2.5).set_points_as_corners(lp)
        mlab = VGroup(tx("what each plant can charge", 14, PRICE, bold=True),
                      tx("(the rival's delivered cost)", 12, GREY_A)).arrange(DOWN, buff=0.02).move_to(pa.ax.c2p(0, 143))
        border = DashedLine(pa.ax.c2p(150, 80), pa.ax.c2p(150, 150), stroke_color=WHITE, stroke_width=1.5, dash_length=0.08)
        bl = tx("the border", 13, WHITE).next_to(border, UP, buff=0.05)
        eu = VGroup(tx(f"Trucking cement in Europe, 1989: about ECU {C['haul_eu']:.2f} a tonne-kilometre,", 15, WHITE),
                    tx(f"when a tonne sold for about ECU {C['price_uk']:.0f}: {C['radius_eu']:.0f} km of road added half "
                       "the price", 15, WHITE)).arrange(DOWN, buff=0.04).to_edge(DOWN, buff=0.55)
        conc = VGroup(tx("Four largest firms' share of US sales, 2022", 15, WHITE, bold=True),
                      tx(f"cement: {C['cr4_cement'][0]:.0f}% ({C['cr4_cement'][1]:.0f} firms)", 14, CEMENT),
                      tx(f"ready-mix concrete: {C['cr4_readymix'][0]:.0f}% ({C['cr4_readymix'][1]:,.0f} firms)", 14, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.35)
        tag = estimate_tag("the Works (mill.py): two plants, $95 a tonne at the gate, trucking 12 cents a tonne-km",
                           corner=DR, size=12)
        src = source("European Commission Decision 94/815/EC, recitals 9-10; US Census Bureau, 2022 Economic Census, "
                     "concentration", size=12)
        with self.voiceover(
            "Here is why. A tonne of cement is heavy and cheap, so trucking it eats the price quickly. "
            "<bookmark mark='a'/> In the European Commission's files, trucking cement in 1989 cost about seven "
            f"hundredths of an ECU, Europe's accounting unit, per tonne and kilometre, when a tonne sold for about "
            f"{C['price_uk']:.0f} ECU: five hundred kilometres of road added half the price. <bookmark mark='b'/> So "
            "picture two plants, three hundred kilometres apart. A tonne leaves each gate at the same cost, and costs "
            "more the further it is trucked. <bookmark mark='c'/> Each plant is the cheapest supplier in its own circle, "
            "out to the border halfway between them. <bookmark mark='d'/> And within its circle, a plant only has to "
            "beat its rival's delivered cost, which is highest right at its own gate. So the margin is fattest close to "
            "home, and vanishes at the border. Every cement plant is a small monopoly on a circle of map. "
            "<bookmark mark='e'/> Nationally, the four largest American cement firms sell about half the cement, and "
            "the four largest concrete firms just fifteen per cent of the concrete. But nobody buys concrete "
            "nationally. Locally, a builder may have two or three suppliers to choose from."
        ) as vo:
            self.play(FadeIn(pa0), FadeIn(kA), FadeIn(kB), FadeIn(la), FadeIn(lb), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(eu, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(Create(ca), Create(cb), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(border), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(margin), Create(pl), FadeIn(mlab), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeOut(eu), FadeIn(conc, shift=LEFT * 0.2))
        self.clear_scene()
