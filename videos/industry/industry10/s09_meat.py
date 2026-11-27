from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Meat(VoiceoverScene):
    def construct(self):
        card(self, 8, "Meat", "Who turns grain into meat, and who holds the power in between?",
             "Chapter eight. Meat.", lit=("moat", "dollar"))
        self.feed()
        self.packers()
        self.prices()

    def feed(self):
        corn = VGroup(*[Circle(0.08, stroke_width=0, fill_color=CORN, fill_opacity=1) for _ in range(60)]).arrange_in_grid(
            rows=6, cols=10, buff=0.04).move_to([-5.2, 0.3, 0])
        meal = VGroup(*[Circle(0.08, stroke_width=0, fill_color="#B5915A", fill_opacity=1) for _ in range(24)]).arrange_in_grid(
            rows=3, cols=8, buff=0.04).next_to(corn, DOWN, buff=0.25)
        cl = VGroup(tx("corn", 15, CORN), tx("soybean meal", 15, "#B5915A")).arrange(DOWN, buff=0.75).next_to(corn, LEFT, buff=0.15)
        cl[1].align_to(meal, UP).shift(DOWN * 0.05)
        animals = VGroup(draw.cow(1.4), draw.pig(1.2), draw.chicken(0.8)).arrange(DOWN, buff=0.35).move_to([-0.4, 0.0, 0])
        al = VGroup(*[tx(n, 15, WHITE).next_to(a, RIGHT, buff=0.15) for n, a in zip(("cattle", "hogs", "chickens"), animals)])
        packer = draw.factory(1.6).move_to([3.4, 0.6, 0])
        pl = VGroup(tx("the packing plant", 17, WHITE, bold=True), tx("slaughter, cut, pack", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(packer, DOWN, buff=0.15)
        shop = draw.shop(1.4).move_to([6.0, -1.6, 0])
        arrows = VGroup(Arrow(corn.get_right(), animals.get_left() + UP * 0.6, buff=0.2, stroke_width=2.5, color=GREY_B, tip_length=0.12),
                        Arrow(animals.get_right() + RIGHT * 0.9, packer.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B,
                              tip_length=0.12),
                        Arrow(packer.get_bottom() + DOWN * 0.7, shop.get_top(), buff=0.15, stroke_width=2.5, color=GREY_B,
                              tip_length=0.12))
        src = source("the standard livestock chain; USDA ERS, Feed Grains Sector at a Glance", size=13)
        with self.voiceover(
            "Much of what farmers grow is never eaten by people directly. <bookmark mark='a'/> Most American corn that "
            "stays at home goes into animal feed or ethanol, and nearly all soybean meal is fed to animals. "
            "<bookmark mark='b'/> Cattle, hogs and chickens turn that grain into meat, eggs and milk, at a cost: an "
            "animal burns most of its feed simply to live and grow. <bookmark mark='c'/> Then the animals go to a "
            "packing plant, where they are slaughtered, cut and packed, <bookmark mark='d'/> and on to shops and "
            "restaurants. The packing plant is where this chain narrows."
        ) as vo:
            self.play(FadeIn(src), FadeIn(corn), FadeIn(meal), FadeIn(cl))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in animals], lag_ratio=0.3), FadeIn(al), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(packer), FadeIn(pl))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(shop))
        self.clear_scene()

    def packers(self):
        M = R["meat"]
        herds = []
        for k, share in enumerate((M["cr4_1980"], M["cr4"])):
            cows = VGroup(*[draw.cow(0.38) for _ in range(100)]).arrange_in_grid(rows=10, cols=10, buff=(0.06, 0.04))
            cows.move_to([-3.4 + 6.8 * k, -0.6, 0])
            for i, c in enumerate(cows):
                if i >= share:
                    c.set_opacity(0.25)
            herds.append(cows)
        labs = VGroup(VGroup(tx("1980", 22, WHITE, bold=True), tx(f"the four largest packers buy {M['cr4_1980']:.0f}%", 17, MEAT)
                             ).arrange(DOWN, buff=0.06).next_to(herds[0], UP, buff=0.2),
                      VGroup(tx("today", 22, WHITE, bold=True), tx(f"the four largest packers buy {M['cr4']:.0f}%", 17, MEAT)
                             ).arrange(DOWN, buff=0.06).next_to(herds[1], UP, buff=0.2))
        who = tx("Tyson, JBS, Cargill and National Beef", 18, WHITE, bold=True).to_edge(DOWN, buff=0.7)
        sub = tx("of the steers and heifers fed for beef in the US", 15, GREY_A).next_to(who, UP, buff=0.08)
        src = source("USDA ERS, Amber Waves (January 2024), from USDA's Packers and Stockyards data", size=13)
        with self.voiceover(
            "Take beef. <bookmark mark='a'/> In 1980, the four largest beef packers bought about "
            f"{M['cr4_1980']:.0f} percent of the young cattle fattened for slaughter in the United States. "
            f"<bookmark mark='b'/> Today, about {M['cr4']:.0f} percent, according to the Department of Agriculture. "
            "<bookmark mark='c'/> Four companies: Tyson, Brazil's JBS, Cargill, and National Beef. A cattle "
            "feeder in Kansas or Nebraska with animals ready for slaughter may have only two or three plants within "
            "trucking distance to sell to. Economists still argue about how much that costs cattle producers. But it "
            "means the farm's side of this market is many sellers facing very few buyers."
        ) as vo:
            self.play(FadeIn(src), FadeIn(herds[0]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(c, color=MEAT, scale_factor=1.15) for c in herds[0][:int(M["cr4_1980"])]],
                                  lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(herds[1]), FadeIn(labs[1]))
            self.play(LaggedStart(*[Indicate(c, color=MEAT, scale_factor=1.15) for c in herds[1][:int(M["cr4"])]],
                                  lag_ratio=0.01), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(sub), FadeIn(who))
        self.clear_scene()

    def prices(self):
        M = R["meat"]
        gb = M["ground_beef"]
        ms = sorted(gb)
        pa = viz.plot_axes([2000, 2027], [0, 8], x_length=5.6, y_length=3.4, xticks=[2000, 2010, 2020],
                           yticks=[2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13).move_to(
            [-3.4, -0.4, 0])
        ln = VMobject(stroke_color=MEAT, stroke_width=3).set_points_as_corners([pa.ax.c2p(mx(m), gb[m]) for m in ms])
        pk = max(ms, key=gb.get)
        pkd = VGroup(Dot(pa.ax.c2p(mx(pk), gb[pk]), color=WHITE, radius=0.06),
                     tx(f"{mlabel(pk)}: ${gb[pk]:.2f}", 15, WHITE, bold=True)).arrange(LEFT, buff=0.1)
        pkd.move_to(pa.ax.c2p(mx(pk), gb[pk]), aligned_edge=RIGHT).shift(UP * 0.25 + LEFT * 0.1)
        pt = tx("ground beef, a pound, average US retail price", 15, MEAT, bold=True).next_to(pa, UP, buff=0.12)
        tsn = {y: v for y, v in M["tsn"].items() if v[0] and v[1] is not None}
        ys = sorted(tsn)
        pb = viz.plot_axes([2011.4, 2026.6], [-2, 8], x_length=5.4, y_length=3.4, xticks=[2012, 2016, 2020, 2024],
                           yticks=[-2, 0, 2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}%", size=13).move_to(
            [3.6, -0.4, 0])
        z = Line(pb.ax.c2p(2011.4, 0), pb.ax.c2p(2026.6, 0), stroke_color=GREY_B, stroke_width=1.2)
        bars = VGroup()
        for y in ys:
            m = 100 * tsn[y][1] / tsn[y][0]
            p0, p1 = pb.ax.c2p(y, 0), pb.ax.c2p(y, m)
            bars.add(Rectangle(width=0.5, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=GREEN_C if m >= 0 else STATE,
                               fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        bt = tx("Tyson Foods: profit as a share of sales", 15, WHITE, bold=True).next_to(pb, UP, buff=0.12)
        src = source("BLS average price of ground beef via FRED; SEC EDGAR, Tyson Foods Forms 10-K (years to September)",
                     size=13)
        with self.voiceover(
            "And yet the packers are not simply rich. <bookmark mark='a'/> Beef in American shops has never been "
            f"dearer: a pound of ground beef cost about {gb[ms[0]]:.2f} dollars in 2000, and a record "
            f"{say_money(gb[pk])} in {mlabel(pk)}, as the national cattle herd shrank after years of drought and high "
            "costs. Ranchers selling cattle have had some of their best years. <bookmark mark='b'/> But look at Tyson, "
            "the biggest meat company in America. In 2021 and 2022 it kept about six cents of every dollar. Then its "
            "margins collapsed: chicken prices fell, and cattle became so scarce and expensive that beef stopped paying. "
            "In 2023 the whole company lost money. "
            "<bookmark mark='c'/> Since then it has kept about a cent on the dollar. Concentration gives the packers "
            "power over the price of cattle, but not over the number of cattle. When the animals run short, the "
            "squeeze runs the other way."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(pt))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            self.play(FadeIn(pkd))
            vo.wait_until("b")
            self.play(FadeIn(pb), Create(z), FadeIn(bt))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] > pb.ax.c2p(0, 0)[1] else UP) for b in bars[:-4]],
                                  lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] > pb.ax.c2p(0, 0)[1] else UP) for b in bars[-4:]],
                                  lag_ratio=0.2), run_time=1.5)
        self.clear_scene()
