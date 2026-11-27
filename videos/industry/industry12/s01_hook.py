from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.air()
        self.reaction()
        self.scale_()
        self.products()
        self.title()

    def air(self):
        H = R["hook"]
        where = VGroup(tx("Germany, 1908", 24, WHITE, bold=True),
                       tx(f"13 October {H['patent']:.0f}: Fritz Haber files a patent", 18, GREY_A),
                       tx("on the \"synthesis of ammonia from its elements\"", 18, GREY_A)).arrange(DOWN, buff=0.06,
                                                                                         aligned_edge=LEFT).to_corner(UL, buff=0.45)
        rng = np.random.default_rng(4)
        sky = VGroup()
        for k in range(26):
            m = draw.molecule("N2" if k % 5 else "H2", bond=0.3)
            m.move_to([rng.uniform(-5.5, 5.5), rng.uniform(-2.6, 1.6), 0]).rotate(rng.uniform(0, PI))
            sky.add(m)
        cap = VGroup(tx("Air is four fifths nitrogen.", 24, NITRO, bold=True),
                     tx("Every plant needs nitrogen, but almost none can take it from the air:", 18, GREY_A),
                     tx("the two atoms of N2 are held by one of the strongest bonds in chemistry.", 18, GREY_A)).arrange(
            DOWN, buff=0.08).to_edge(DOWN, buff=0.5)
        src = source("Erisman et al., Nature Geoscience 1 (2008); the Nobel Foundation", corner=DR, size=13)
        with self.voiceover(
            "On the thirteenth of October 1908, a German chemist named Fritz Haber filed a patent on, in his words, the "
            "synthesis of ammonia from its elements. <bookmark mark='a'/> The elements were in the air. Four fifths of "
            "the air we breathe is nitrogen, and nitrogen is what every crop is hungriest for. But almost no plant can "
            "take it from the air, because the two atoms of a nitrogen molecule are held together by one of the "
            "strongest bonds in chemistry. Farmers had to bring nitrogen to their fields, as manure or as mined "
            "nitrate."
        ) as vo:
            self.play(FadeIn(where), FadeIn(src), LaggedStart(*[FadeIn(m, scale=0.6) for m in sky], lag_ratio=0.04),
                      run_time=2.5)
            self.play(*[m.animate.shift(RIGHT * 0.3 + UP * 0.1 * ((k % 3) - 1)).rotate(0.4) for k, m in enumerate(sky)],
                      run_time=3.0)
            vo.wait_until("a")
            self.play(*[m.animate.shift(RIGHT * 0.3 + UP * 0.1 * ((k % 3) - 1)).rotate(0.4) for k, m in enumerate(sky)],
                      FadeIn(cap), run_time=2.5)
        self.clear_scene()

    def reaction(self):
        H = R["hook"]
        n2 = draw.molecule("N2", bond=0.55).move_to([-4.6, 0.4, 0])
        h2s = VGroup(*[draw.molecule("H2", bond=0.5).move_to([-2.4, 1.4 - 1.0 * k, 0]) for k in range(3)])
        plus = tx("+", 40, WHITE).move_to([-3.5, 0.4, 0])
        arrow = Arrow([-1.2, 0.4, 0], [0.8, 0.4, 0], buff=0, color=PRICE, stroke_width=5)
        cond = VGroup(tx("about 200 atmospheres,", 15, PRICE), tx("500 °C, an iron catalyst", 15, PRICE)).arrange(
            DOWN, buff=0.02).next_to(arrow, UP, buff=0.12)
        nh3 = VGroup(*[draw.molecule("NH3", bond=0.6).move_to([2.6, 1.3 - 1.9 * k, 0]) for k in range(2)])
        eq = tx("N2  +  3 H2  →  2 NH3", 34, WHITE, bold=True).to_edge(UP, buff=0.6)
        names = VGroup(tx("nitrogen, from the air", 15, NITRO).next_to(n2, DOWN, buff=0.4),
                       tx("hydrogen, from natural gas", 15, GREY_A).next_to(h2s, DOWN, buff=0.2),
                       tx("ammonia", 18, NITRO, bold=True).next_to(nh3, RIGHT, buff=0.3))
        bosch = VGroup(tx(f"Around {H['bosch_year']:.0f}: Carl Bosch makes it industrial at BASF,", 17, WHITE),
                       tx("in steel vessels that hold the pressure", 17, WHITE),
                       tx(f"Nobel Prizes: Haber {H['prize']:.0f}, Bosch {H['bosch']:.0f}", 16, GREY_A)).arrange(
            DOWN, buff=0.05).to_edge(DOWN, buff=0.45)
        tag = estimate_tag("conditions: typical of the process, not of any one plant", corner=DR, size=12)
        src = source("The Nobel Foundation, 'Fritz Haber - Facts' and 'Carl Bosch - Facts'", size=13)
        with self.voiceover(
            "Haber's trick was to force nitrogen to combine with hydrogen. <bookmark mark='a'/> One molecule of "
            "nitrogen and three of hydrogen, <bookmark mark='b'/> squeezed to hundreds of atmospheres and heated over an "
            "iron catalyst, <bookmark mark='c'/> become two molecules of ammonia, which plants can use. "
            "<bookmark mark='d'/> Haber did it on a laboratory bench. It took an engineer, Carl Bosch, at the chemical "
            f"company BASF, to build steel vessels that could hold the pressure at industrial scale, around "
            f"{H['bosch_year']:.0f}. Both won the Nobel Prize. In America today the hydrogen comes from natural gas, "
            "the dominant feedstock, as the US Geological Survey puts it."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(n2, shift=RIGHT * 0.3), FadeIn(plus), LaggedStart(*[FadeIn(h, shift=RIGHT * 0.3) for h in h2s],
                                                                              lag_ratio=0.2), FadeIn(names[:2]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(cond))
            self.play(VGroup(n2, h2s).animate.shift(RIGHT * 0.8).scale(0.9), run_time=1.0)
            vo.wait_until("c")
            self.play(ReplacementTransform(VGroup(n2, h2s, plus), nh3), FadeIn(names[2]), FadeOut(names[:2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(bosch, shift=UP * 0.1))
        self.clear_scene()

    def scale_(self):
        H = R["hook"]
        wn = H["world_n"]
        ys = sorted(y for y in wn if y >= 1950)
        pa = viz.plot_axes([1948, 2027], [0, 180], x_length=6.2, y_length=4.0, xticks=[1950, 1975, 2000, 2025],
                           yticks=[50, 100, 150], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}",
                           ylabel="world ammonia, million tonnes of nitrogen", size=13).move_to([-3.4, -0.3, 0])
        ln = VMobject(stroke_color=NITRO, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, wn[y] / 1e6) for y in ys])
        pop = H["pop"]
        py = sorted(y for y in pop if y >= 1900)
        pb = viz.plot_axes([1898, 2027], [0, 9], x_length=5.4, y_length=4.0, xticks=[1900, 1950, 2000],
                           yticks=[2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}bn",
                           ylabel="people on Earth", size=13).move_to([3.6, -0.3, 0])
        lp = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners([pb.ax.c2p(y, pop[y]) for y in py])
        m08 = VGroup(Dot(pb.ax.c2p(1908, H["pop1908"]), radius=0.06, color=PRICE),
                     tx(f"1908: {H['pop1908']:.1f}bn", 14, PRICE).next_to(pb.ax.c2p(1908, H["pop1908"]), UP, buff=0.1))
        mlast = tx(f"{H['pop_year']}: {H['pop_last']:.1f}bn", 15, WHITE, bold=True).next_to(
            pb.ax.c2p(H["pop_year"], H["pop_last"]), LEFT, buff=0.15)
        nl = VGroup(tx(f"1950: {H['n1950']:.1f}", 14, NITRO).next_to(pa.ax.c2p(1950, H["n1950"]), UP, buff=0.15),
                    tx(f"2025: {H['n2025']:.0f}", 16, NITRO, bold=True).next_to(pa.ax.c2p(2025, H["n2025"]), LEFT, buff=0.1))
        src = source("USGS, Data Series 140 and Mineral Commodity Summaries 2026 (ammonia); Our World in Data "
                     "(population; FAO nitrogen use per hectare)", size=13)
        with self.voiceover(
            f"<bookmark mark='a'/> In 1950 the world made about {H['n1950']:.0f} million tonnes of nitrogen in ammonia. "
            f"In 2025, about {H['n2025']:.0f} million. <bookmark mark='b'/> Over the same century the number of people "
            f"on Earth went from about {H['pop1908']:.1f} billion, when Haber filed his patent, to over eight billion. "
            f"And the world's farmers now spread about {H['n_ha'][max(H['n_ha'])]:.0f} kilograms of nitrogen on each "
            f"hectare of cropland, against about {H['n_ha'][min(H['n_ha'])]:.0f} in {min(H['n_ha'])}."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(nl), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pb), Create(lp), FadeIn(m08), run_time=3.0)
            self.play(FadeIn(mlast))
        self.clear_scene()

    def products(self):
        eth = draw.molecule("C2H6", bond=0.5).move_to([-5.2, 1.4, 0])
        ch4 = draw.molecule("CH4", bond=0.5).move_to([-5.2, -1.4, 0])
        c2h4 = draw.molecule("C2H4", bond=0.5).move_to([-2.0, 1.4, 0])
        nh3 = draw.molecule("NH3", bond=0.55).move_to([-2.0, -1.4, 0])
        ch = draw.chain(8, 0.32).move_to([1.6, 1.4, 0])
        goods = VGroup(draw.pellet_bag(0.7), draw.bottle(0.8, "#7EC8F5", 0.0), draw.carton(0.5), draw.paint_can(0.6)).arrange(
            RIGHT, buff=0.35).move_to([4.8, 1.4, 0])
        sack = draw.sack(0.9, label_="N").move_to([2.0, -1.4, 0])
        field = draw.field(2.4, 2, 6, "corn", 0.6).move_to([5.0, -1.4, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.2, color=GREY_B, stroke_width=2.5, tip_length=0.12)
                          for a, b in ((eth, c2h4), (c2h4, ch), (ch, goods), (ch4, nh3), (nh3, sack), (sack, field))])
        labs = VGroup(tx("ethane", 14, GAS).next_to(eth, DOWN, buff=0.12), tx("ethylene", 14, ETHYL).next_to(c2h4, DOWN, buff=0.12),
                      tx("polyethylene", 14, PLASTIC).next_to(ch, DOWN, buff=0.12),
                      tx("methane", 14, GAS).next_to(ch4, DOWN, buff=0.12), tx("ammonia", 14, NITRO).next_to(nh3, DOWN, buff=0.12),
                      tx("fertilizer", 14, FERT).next_to(sack, DOWN, buff=0.12))
        with self.voiceover(
            "Ammonia is one branch of a much bigger tree. <bookmark mark='a'/> The same natural gas gives up methane, "
            "which becomes the hydrogen for ammonia and fertilizer, <bookmark mark='b'/> and ethane, which becomes "
            "ethylene, which is strung together into polyethylene, one of the most common plastics: bags, bottles, "
            "films, the lining of a carton. <bookmark mark='c'/> From a few molecules of gas and oil, the chemical "
            "industry makes almost everything else: plastics, paints, fibres, fertilizers, detergents and medicines."
        ) as vo:
            self.play(FadeIn(eth), FadeIn(ch4), FadeIn(labs[0]), FadeIn(labs[3]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[3]), TransformFromCopy(ch4, nh3), FadeIn(labs[4]))
            self.play(GrowArrow(arrows[4]), FadeIn(sack), FadeIn(labs[5]), GrowArrow(arrows[5]), FadeIn(field))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), TransformFromCopy(eth, c2h4), FadeIn(labs[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(ch, shift=RIGHT * 0.2), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in goods], lag_ratio=0.2))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "It is one of the largest industries in the world, and one of the least seen. Industry, Built. Part twelve: "
            "chemicals. How does a molecule of gas become a thousand products, and where in the chain is the money?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
