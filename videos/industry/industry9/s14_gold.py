from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

DENSITY = 19.32  # tonnes of gold per cubic metre


class Gold(VoiceoverScene):
    def construct(self):
        card(self, 12, "Gold", "Why is the oldest metal suddenly the most profitable?",
             "Chapter twelve. Gold.", lit=("dollar", "change"))
        self.cube()
        self.uses()
        self.newmont()

    def cube(self):
        t = get("usgs.au.mine")
        side = (t / DENSITY) ** (1 / 3)
        s = 0.62  # screen units per metre
        a = side * s
        front = Square(a, stroke_width=0, fill_color="#D4A017", fill_opacity=1)
        top = Polygon(front.get_corner(UL), front.get_corner(UR), front.get_corner(UR) + [0.45 * a, 0.35 * a, 0],
                      front.get_corner(UL) + [0.45 * a, 0.35 * a, 0], stroke_width=0, fill_color=GOLDC, fill_opacity=1)
        right = Polygon(front.get_corner(UR), front.get_corner(DR), front.get_corner(DR) + [0.45 * a, 0.35 * a, 0],
                        front.get_corner(UR) + [0.45 * a, 0.35 * a, 0], stroke_width=0, fill_color="#A87C10",
                        fill_opacity=1)
        cube = VGroup(right, top, front).move_to([-2.2, -0.2, 0])
        floor = Line([-7, cube.get_bottom()[1], 0], [7, cube.get_bottom()[1], 0], stroke_color=GREY_D, stroke_width=2)
        man = draw.person(1.75 * s, STONE).next_to(cube, RIGHT, buff=1.0).align_to(cube, DOWN)
        mh = tx("a person", 14, GREY_A).next_to(man, UP, buff=0.08)
        dim = VGroup(Line(front.get_corner(DL) + DOWN * 0.25, front.get_corner(DR) + DOWN * 0.25, stroke_color=WHITE,
                          stroke_width=1.5),
                     tx(f"{side:.1f} m", 16, WHITE).next_to(front, DOWN, buff=0.35))
        lab = VGroup(tx(f"{t:,.0f} tonnes", 30, GOLDC, bold=True), tx("of gold mined in 2025", 18, WHITE),
                     tx(f"a cube {side:.1f} metres on a side", 18, GREY_A)).arrange(DOWN, buff=0.08).move_to([4.2, 1.8, 0])
        price = VGroup(tx(f"${get('usgs.au.price'):,.0f} an ounce", 26, PRICE, bold=True),
                       tx("the 2025 average, a record", 16, GREY_A),
                       tx(f"so the cube is worth about ${t * 32150.7 * get('usgs.au.price') / 1e9:,.0f} billion", 18,
                          WHITE)).arrange(DOWN, buff=0.06).move_to([4.2, -1.6, 0])
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'gold'; gold weighs 19.32 tonnes a cubic "
                     "metre", size=13)
        with self.voiceover(
            "Gold is the strangest metal in this film, because almost none of it is used up. "
            f"<bookmark mark='a'/> The world's mines produced about {t:,.0f} tonnes of gold in 2025. Gold is so dense "
            f"that all of it would fit in a cube about {side:.1f} metres on a side, a little taller than three "
            "people standing on each other's shoulders. <bookmark mark='b'/> Yet at 2025's average price of "
            f"{get('usgs.au.price'):,.0f} dollars an ounce, a record, that cube was worth about "
            f"{t * 32150.7 * get('usgs.au.price') / 1e9:,.0f} billion dollars. Gold miners dig up far more value per "
            "tonne of metal than anyone in this film, and they do it from ore that often holds only a few grams of gold "
            "in a tonne of rock."
        ) as vo:
            self.play(FadeIn(src), Create(floor), FadeIn(man), FadeIn(mh))
            vo.wait_until("a")
            self.play(GrowFromEdge(cube, DOWN), run_time=1.5)
            self.play(FadeIn(dim), FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(price, shift=UP * 0.1))
        self.clear_scene()

    def uses(self):
        parts = [("jewellery", get("usgs.au.jewellery"), GOLDC), ("bars", get("usgs.au.bars"), "#E0A458"),
                 ("central banks and institutions", get("usgs.au.cb"), STATE), ("coins", get("usgs.au.coins"), "#C9D3E0"),
                 ("electronics", get("usgs.au.electronics"), "#7EC8F5")]
        parts.append(("other", 100 - sum(v for _, v, _ in parts), GREY_D))
        ring = VGroup()
        a0 = PI / 2
        for n, v, c in parts:
            ring.add(AnnularSector(inner_radius=1.0, outer_radius=1.75, angle=-TAU * v / 100, start_angle=a0,
                                   fill_color=c, fill_opacity=0.92, stroke_color=BACKGROUND, stroke_width=2))
            a0 -= TAU * v / 100
        ring.move_to([-3.4, -0.2, 0])
        labs = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1), tx(f"{n}: {v:.0f}%", 17, WHITE))
                        .arrange(RIGHT, buff=0.12) for n, v, c in parts]).arrange(DOWN, aligned_edge=LEFT, buff=0.18
                                                                                   ).move_to([2.2, 0.9, 0])
        ys = [2021, 2022, 2023, 2024, 2025]
        pa = viz.plot_axes([2020.4, 2025.6], [0, 3600], x_length=4.0, y_length=2.0, xticks=ys, yticks=[1000, 2000, 3000],
                           xfmt=lambda v: f"'{int(v) % 100:02d}", yfmt=lambda v: f"${v:,.0f}", size=12).move_to(
            [3.2, -2.1, 0])
        pr = viz.year_bars(pa, ys, [get(f"usgs.au.price.{y}") if y < 2025 else get("usgs.au.price") for y in ys], PRICE,
                           width=0.5)
        pt = tx("gold, dollars an ounce", 14, PRICE).next_to(pa, LEFT, buff=0.2)
        head = tx("Where the gold went, 2025 (excluding funds)", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'gold'", size=13)
        with self.voiceover(
            "So where does it go? <bookmark mark='a'/> About forty percent into jewellery, and a quarter into bars "
            "that people and investors simply store. <bookmark mark='b'/> And about a fifth to central banks and other "
            "institutions. Central banks have been buying gold in large amounts; many analysts think one reason is to "
            "hold reserves that no other government can freeze. <bookmark mark='c'/> With that buying, the price climbed from about eighteen "
            f"hundred dollars an ounce in 2021 and 2022 to {get('usgs.au.price'):,.0f} in 2025, thirty-eight percent "
            "up on the year before. Gold's price is not set by a cost curve or by factories' demand. It is set by "
            "fear, by interest rates, and by what people expect others to pay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(ring[0], scale=0.9), FadeIn(labs[0]))
            self.play(FadeIn(ring[1], scale=0.9), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(FadeIn(ring[2], scale=0.9), FadeIn(labs[2]), Indicate(labs[2], color=STATE))
            self.play(FadeIn(ring[3:], scale=0.9), FadeIn(labs[3:]))
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(pt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in pr], lag_ratio=0.25),
                      run_time=2.0)
        self.clear_scene()

    def newmont(self):
        G = R["gold"]
        yrs = list(range(2012, 2026))
        pa = viz.plot_axes([2011.4, 2025.6], [-4, 24], x_length=10.0, y_length=4.6, xticks=[2012, 2015, 2018, 2021, 2024],
                           yticks=[0, 5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn",
                           size=15).move_to([-0.3, -0.4, 0])
        zero = Line(pa.ax.c2p(2011.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.5)
        rev = VGroup()
        net = VGroup()
        for y in yrs:
            r_ = G["nem_revenue"][y]
            n_ = G["nem_net"][y]
            p0, p1 = pa.ax.c2p(y - 0.19, 0), pa.ax.c2p(y - 0.19, r_)
            rev.add(Rectangle(width=0.36, height=p1[1] - p0[1], stroke_width=0, fill_color=GOLDC, fill_opacity=0.85
                              ).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
            q0, q1 = pa.ax.c2p(y + 0.19, 0), pa.ax.c2p(y + 0.19, n_)
            net.add(Rectangle(width=0.36, height=max(abs(q1[1] - q0[1]), 0.01), stroke_width=0,
                              fill_color=GREEN_C if n_ > 0 else STATE, fill_opacity=0.9).move_to(
                [q0[0], (q0[1] + q1[1]) / 2, 0]))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=GOLDC, fill_opacity=1), tx("revenue", 15, WHITE)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=GREEN_C, fill_opacity=1), tx("net income", 15, WHITE)
                            ).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=STATE, fill_opacity=1), tx("loss", 15, WHITE)
                            ).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.4).next_to(pa, UP, buff=0.12)
        last = VGroup(tx(f"2025: revenue ${G['nem_revenue'][2025]:.1f}bn,", 17, GOLDC, bold=True),
                      tx(f"net income ${G['nem_net'][2025]:.1f}bn, a record", 17, GREEN_C, bold=True)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.04).next_to(pa.ax.c2p(2023.3, 20), LEFT, buff=0.2)
        head = tx("Newmont, the largest gold miner, US$ billion", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR, Newmont Corporation, Forms 10-K (company facts)", size=13)
        with self.voiceover(
            "For the gold miners, the price rise has been a bonanza. <bookmark mark='a'/> Here is Newmont, the "
            "biggest of them, since 2012. Through the 2010s, as gold fell and then drifted, its revenue shrank and it "
            "lost money in several years. <bookmark mark='b'/> It bought its rivals Goldcorp in 2019 and Newcrest in "
            "2023, and the costs of those deals and of lower-quality mines weighed on its profits. "
            f"<bookmark mark='c'/> Then the price took off. Newmont's revenue went from {G['nem_revenue'][2023]:.1f} "
            f"billion dollars in 2023 to {G['nem_revenue'][2025]:.1f} billion in 2025, and its net income to "
            f"{G['nem_net'][2025]:.1f} billion, a record. The mines did not change much. The ounces did not change "
            "much. The price did. And remember Grasberg, whose gold made its copper cost less than nothing: in this "
            "market a copper mine with gold in its ore has a second business inside it."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(head), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_, DOWN), GrowFromEdge(n_, DOWN if
                                                                                         G["nem_net"][y] > 0 else UP))
                                    for r_, n_, y in zip(rev[:7], net[:7], yrs[:7])], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_, DOWN), GrowFromEdge(n_, DOWN if
                                                                                         G["nem_net"][y] > 0 else UP))
                                    for r_, n_, y in zip(rev[7:12], net[7:12], yrs[7:12])], lag_ratio=0.15),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_, DOWN), GrowFromEdge(n_, DOWN if
                                                                                         G["nem_net"][y] > 0 else UP))
                                    for r_, n_, y in zip(rev[12:], net[12:], yrs[12:])], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(last, shift=LEFT * 0.1))
        self.clear_scene()
