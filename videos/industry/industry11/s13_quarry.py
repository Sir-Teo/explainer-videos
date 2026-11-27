from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Quarry(VoiceoverScene):
    def construct(self):
        card(self, 11, "The quarry with a permit", "How does the cheapest material of all earn the steadiest profits?",
             "Chapter eleven. The quarry with a permit.", lit=("unit", "moat"))
        self.reach()
        self.price()
        self.vulcan()

    def reach(self):
        A = R["aggregates"]
        q = draw.quarry(1.8, 0.6).move_to([-3.4, -0.4, 0])
        rings = VGroup(*[Circle(radius=r_, stroke_color=PRICE, stroke_width=2, stroke_opacity=0.8 - 0.2 * k).move_to(q.get_center())
                         for k, r_ in enumerate((1.2, 2.0, 2.8))])
        rl = VGroup(*[tx(t_, 13, PRICE).next_to(rings[k].point_at_angle(0.35), RIGHT, buff=0.05) for k, t_ in
                      enumerate(("+25%", "+60%", "price doubled"))])
        trucks = VGroup(*[draw.truck(0.7, STONE).move_to(q.get_center()) for _ in range(5)])
        facts = VGroup(tx(f"US crushed stone, 2025: {A['tonnes'] / 1000:.1f} billion tonnes", 19, WHITE, bold=True),
                       tx(f"from {A['quarries']:,.0f} quarries; about ${A['price']:.2f} a tonne", 16, GREY_A),
                       tx(f"{A['aggregate']:.0f}% for roads, concrete and building; {A['to_cement']:.0f}% for cement", 16,
                          GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.0, 2.4, 0])
        vul = VGroup(tx("Vulcan Materials, 10-K 2025:", 16, STONE, bold=True),
                     tx(f"\"Approximately {A['vmc']['truck']:.0f}% of our total aggregates shipments are", 15, WHITE),
                     tx("delivered exclusively from the producing location", 15, WHITE),
                     tx("to the customer by truck.\"", 15, WHITE),
                     tx("\"... transportation costs can quickly exceed the cost", 15, WHITE),
                     tx("of the aggregates.\"", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.4, -1.2, 0])
        tag = estimate_tag("rings: illustrative, a $22 ton trucked at about 20 cents a ton-mile", corner=DR, size=12)
        src = source("USGS, Mineral Commodity Summaries 2026 (Stone, Crushed); Vulcan Materials, Form 10-K 2025", size=12)
        with self.voiceover(
            "The humblest heavy material is stone. <bookmark mark='a'/> America quarries about "
            f"{A['tonnes'] / 1000:.1f} billion tonnes of crushed stone a year, from {A['quarries']:,.0f} quarries, at "
            f"about {A['price']:.0f} dollars a tonne: the gravel under every road and inside every concrete slab. "
            "<bookmark mark='b'/> It is so heavy for its price that it barely travels. Vulcan Materials, the largest "
            "producer, says about eighty per cent of its stone goes straight from the quarry to the customer by truck, "
            "and that transport costs can quickly exceed the cost of the stone itself. <bookmark mark='c'/> Truck a "
            "load a few dozen miles and its price has risen by a quarter; a hundred miles or so, and it has doubled. "
            "Every quarry serves its own neighbourhood, and the nearest quarry to a growing city is worth a great deal."
        ) as vo:
            self.play(FadeIn(q), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(facts, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(vul))
            vo.wait_until("c")
            self.add(trucks)
            self.play(*[trucks[k].animate.move_to(q.get_center() + 2.6 * np.array([np.cos(a), np.sin(a), 0]))
                        for k, a in enumerate(np.linspace(0.6, 5.6, 5))],
                      LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.4), run_time=3.0)
            self.play(FadeIn(rl))
        self.clear_scene()

    def price(self):
        A = R["aggregates"]
        sr = A["stone_real"]
        ys = sorted(sr)
        pa = viz.plot_axes([1898, 2027], [0, 30], x_length=10.4, y_length=4.2, xticks=[1900, 1925, 1950, 1975, 2000, 2025],
                           yticks=[10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}",
                           ylabel="a tonne of crushed stone, in today's dollars", size=13).move_to([-0.4, -0.2, 0])
        y0 = [y for y in ys if y >= 1900]
        ln = VMobject(stroke_color=STONE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, sr[y]) for y in y0])
        lo = min((y for y in y0 if 1990 <= y <= 2010), key=lambda y: sr[y])
        mk = VGroup(Dot(pa.ax.c2p(lo, sr[lo]), radius=0.06, color=WHITE),
                    tx(f"{lo}: ${sr[lo]:.2f}", 14, WHITE).next_to(pa.ax.c2p(lo, sr[lo]), DOWN, buff=0.1))
        mk2 = VGroup(Dot(pa.ax.c2p(2025, sr[2025]), radius=0.06, color=PRICE),
                     tx(f"2025: ${sr[2025]:.2f}", 15, PRICE, bold=True).next_to(pa.ax.c2p(2025, sr[2025]), UP, buff=0.1))
        quote = VGroup(tx("\"Shortages in some urban and industrialized areas were anticipated to continue", 15, WHITE),
                       tx("to increase owing to local zoning regulations and land-development alternatives.\"", 15, WHITE),
                       tx("USGS, Mineral Commodity Summaries 2026", 13, GREY_A)).arrange(DOWN, buff=0.04).to_edge(DOWN, buff=0.5)
        src = source("USGS Data Series 140 (unit value in 1998 dollars, 1900-2021) and Mineral Commodity Summaries "
                     "(2022-2025), carried to today's dollars with the CPI (BLS)", size=12)
        since = max(y for y in ys if y < 2000 and sr[y] > sr[2025])
        top_y = max((y for y in ys if y < 1960), key=lambda y: sr[y])
        with self.voiceover(
            "Now watch what that does to the price. <bookmark mark='a'/> Here is a tonne of crushed stone, in today's "
            f"dollars, since 1900. It peaked around {top_y}, and then for some sixty years got cheaper, as quarries "
            f"mechanised, <bookmark mark='b'/> down to about {sr[lo]:.0f} dollars in {lo}. <bookmark mark='c'/> And then, "
            f"unlike steel, it climbed, year after year, to about {sr[2025]:.0f} dollars in 2025, the highest since "
            f"{since}. "
            "<bookmark mark='d'/> The government's own geologists give a reason: shortages near cities, because of "
            "zoning and because the land is worth more as houses. New quarries end up further away, and trucking makes "
            "the old ones near town ever more valuable. Nobody can open a rival quarry next door. The permit is the moat."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            k = y0.index(lo)
            l1 = VMobject(stroke_color=STONE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, sr[y]) for y in y0[:k + 1]])
            self.play(Create(l1), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(mk))
            vo.wait_until("c")
            self.play(Create(ln), run_time=2.0)
            self.remove(l1)
            self.play(FadeIn(mk2))
            vo.wait_until("d")
            self.play(FadeIn(quote, shift=UP * 0.1))
        self.clear_scene()

    def vulcan(self):
        A = R["aggregates"]
        v = A["vmc"]
        H = 4.2
        base = -2.4
        out = Rectangle(width=1.8, height=H, stroke_color=WHITE, stroke_width=2).move_to([-3.6, base, 0], aligned_edge=DOWN)
        gp = Rectangle(width=1.8, height=H * v["gp"] / v["price"], stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(
            [-3.6, base, 0], aligned_edge=DOWN)
        rest = Rectangle(width=1.8, height=H * (1 - v["gp"] / v["price"]), stroke_width=0, fill_color=STONE,
                         fill_opacity=0.6).next_to(gp, UP, buff=0)
        top = tx(f"${v['price']:.2f}", 26, WHITE, bold=True).next_to(out, UP, buff=0.08)
        l1 = VGroup(tx(f"${v['gp']:.2f}", 22, GOOD, bold=True), tx("gross profit", 14, GREY_A),
                    tx(f"(${v['cashgp']:.2f} before depreciation)", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).next_to(
            gp, RIGHT, buff=0.25)
        l2 = VGroup(tx("blasting, crushing, labour,", 14, GREY_A), tx("energy, depreciation", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03).next_to(rest, RIGHT, buff=0.25)
        head = VGroup(tx("A ton of Vulcan's stone, 2025", 20, WHITE, bold=True), tx("freight-adjusted price", 13, GREY_A)).arrange(
            DOWN, buff=0.03).next_to(top, UP, buff=0.15)
        res = VGroup(tx(f"{v['reserves']:.1f} billion tons", 30, STONE, bold=True), tx("of proven and probable reserves", 15, GREY_A),
                     tx(f"{v['shipments']:.0f} million tons shipped in 2025:", 15, GREY_A),
                     tx(f"about {v['years']:.0f} years' worth", 22, PRICE, bold=True)).arrange(DOWN, buff=0.06).move_to([3.4, 1.3, 0])
        mlm = VGroup(tx("Martin Marietta kept the stone", 17, WHITE, bold=True), tx("and sold or swapped its cement plants", 15,
                                                                                    GREY_A),
                     tx("(chapter eight)", 13, GREY_B)).arrange(DOWN, buff=0.04).move_to([3.4, -1.7, 0])
        src = source("Vulcan Materials, Form 10-K 2025 (tons are US short tons); Martin Marietta, Form 10-K 2025", size=13)
        with self.voiceover(
            f"Here is a ton of Vulcan's stone in 2025. <bookmark mark='a'/> It sold for about {v['price']:.0f} dollars, "
            f"after taking out the cost of delivery. <bookmark mark='b'/> Of that, {v['gp']:.2f} dollars was gross "
            "profit: about two fifths of the price, on a product that is, after all, broken rock. "
            f"<bookmark mark='c'/> And Vulcan reports {v['reserves']:.1f} billion tons of proven and probable reserves, "
            f"at its 2025 pace about {v['years']:.0f} years of selling, in quarries already permitted, near the cities "
            "that will need them. <bookmark mark='d'/> That is why Martin Marietta, which owned both, chose to keep the "
            "quarries and sell or swap away its cement plants. In heavy materials, the money is where something cannot "
            "be copied: here, a hole in the ground with a permit, close to town."
        ) as vo:
            self.play(FadeIn(src), FadeIn(draw.truck(1.4, STONE).move_to([-6.0, -2.0, 0])))
            vo.wait_until("a")
            self.play(Create(out), FadeIn(top), FadeIn(head))
            vo.wait_until("b")
            self.play(GrowFromEdge(gp, DOWN), FadeIn(rest), FadeIn(l1), FadeIn(l2), run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(res, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(mlm, shift=UP * 0.1))
        self.clear_scene()
