from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Carbon(VoiceoverScene):
    def construct(self):
        card(self, 12, "The hardest carbon", "Why are steel and cement so hard to clean up, and who will pay?",
             "Chapter twelve. The hardest carbon.", lit=("make", "change"))
        self.scale_()
        self.chemistry()
        self.border()

    def scale_(self):
        Cb = R["carbon"]
        tot = Cb["total_co2"]
        W_ = 11.0
        bar = Rectangle(width=W_, height=0.8, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to([0, 0.6, 0])
        cem = Rectangle(width=W_ * Cb["cement_co2"] / tot, height=0.8, stroke_width=0, fill_color=CEMENT, fill_opacity=0.95
                        ).move_to(bar.get_left(), aligned_edge=LEFT)
        tl = VGroup(tx(f"All CO2 from fossil fuels and industry, {Cb['year']}: about {tot:.0f} billion tonnes", 17, WHITE, bold=True)
                    ).next_to(bar, UP, buff=0.2)
        cl = VGroup(tx(f"cement's chemistry alone: {Cb['cement_co2']:.2f} billion t", 16, CEMENT, bold=True),
                    tx(f"({100 * Cb['cement_share']:.1f}%, before the fuel its kilns burn)", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03).next_to(cem, DOWN, buff=0.2).align_to(bar, LEFT)
        st = VGroup(draw.blast_furnace(1.4), VGroup(tx("Steel, 2024", 19, ORE, bold=True),
                                                     tx(f"{Cb['steel_total']:.1f} billion tonnes of greenhouse gases", 16, WHITE),
                                                     tx(f"about {Cb['steel_share'][0]:.0f}-{Cb['steel_share'][1]:.0f}% of the "
                                                        "world's, by the industry's own count", 15, GREY_A),
                                                     tx(f"{Cb['steel_avg']:.2f} t for every tonne of steel", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04)).arrange(RIGHT, buff=0.4).move_to([-2.6, -2.2, 0])
        kiln = VGroup(draw.rotary_kiln(1.6), VGroup(tx("Cement", 19, CEMENT, bold=True),
                                                    tx("half a tonne of CO2 from the rock", 15, GREY_A),
                                                    tx("in every tonne of clinker", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.04)).arrange(
            RIGHT, buff=0.3).move_to([4.0, -2.2, 0])
        src = source("Global Carbon Budget (2025) via Our World in Data; World Steel Association, climate policy paper "
                     "(October 2025)", size=13)
        with self.voiceover(
            "Heavy materials have one more cost that does not show up in their price. <bookmark mark='a'/> The world "
            f"emits about {tot:.0f} billion tonnes of carbon dioxide a year from fossil fuels and industry. "
            "<bookmark mark='b'/> Cement's chemistry alone, the carbon dioxide driven out of limestone in the kiln, is "
            f"about {Cb['cement_co2']:.1f} billion of it, before counting the fuel. <bookmark mark='c'/> Steel, by the "
            f"industry's own count, emitted about {Cb['steel_total']:.1f} billion tonnes of greenhouse gases in 2024, "
            f"some {Cb['steel_share'][0]:.0f} to {Cb['steel_share'][1]:.0f} per cent of all the world's. These are two "
            "of the largest sources of emissions there are, and among the hardest to remove."
        ) as vo:
            self.play(FadeIn(src), GrowFromEdge(bar, LEFT), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(tl), Indicate(bar, color=GREY_B, scale_factor=1.02))
            vo.wait_until("b")
            self.play(GrowFromEdge(cem, LEFT), FadeIn(cl))
            self.play(FadeIn(kiln, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(st, shift=UP * 0.1))
        self.clear_scene()

    def chemistry(self):
        Cb = R["carbon"]
        h2 = Cb["h2"]
        top = VGroup(tx("Fe2O3  +  3 CO  →  2 Fe  +  3 CO2", 34, ORE, bold=True),
                     tx(f"carbon takes the oxygen: about {Cb['co2_chem']:.1f} t of CO2 per tonne of iron, from the chemistry", 15,
                        GREY_A)).arrange(DOWN, buff=0.06).move_to([0, 2.4, 0])
        bot = VGroup(tx("Fe2O3  +  3 H2  →  2 Fe  +  3 H2O", 34, SCRAP, bold=True),
                     tx(f"hydrogen takes it instead: about {Cb['h2_kg']:.0f} kg of hydrogen per tonne of iron, and water", 15,
                        GREY_A)).arrange(DOWN, buff=0.06).move_to([0, 1.0, 0])
        cost = VGroup(tx("Our arithmetic for that hydrogen:", 17, WHITE, bold=True),
                      tx(f"made by electrolysis, about {h2[2.0]['mwh']:.1f} MWh of electricity per tonne of iron", 15, GREY_A),
                      tx(f"at $2 a kg: ${h2[2.0]['cost']:.0f} a tonne;  at $5 a kg: ${h2[5.0]['cost']:.0f} a tonne", 17, PRICE,
                         bold=True),
                      tx(f"against a ton of steel selling for about ${R['tonne']['p25']:,.0f}", 15, GREY_A)).arrange(
            DOWN, buff=0.06).move_to([-3.2, -1.6, 0])
        cem = VGroup(tx("Cement has no such swap:", 17, WHITE, bold=True),
                     tx("the CO2 comes from the limestone itself.", 15, GREY_A),
                     tx("So: less clinker in each tonne, and capture.", 15, GREY_A),
                     tx(f"US blended cements, 2025: {Cb['blended']:.0f}% of shipments", 16, CEMENT, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.6, -1.6, 0])
        tag = estimate_tag("the chemistry and the hydrogen's cost: our arithmetic (mill.py)", corner=DR, size=13)
        src = source("USGS, Mineral Commodity Summaries 2026 (Cement)", size=13)
        with self.voiceover(
            "Why so hard? <bookmark mark='a'/> Because in a blast furnace the carbon is not just fuel. It is the "
            "chemistry. Iron ore is iron bound to oxygen, and carbon is what takes the oxygen away, leaving as carbon "
            f"dioxide: about {Cb['co2_chem']:.1f} tonnes for every tonne of iron, from the reaction alone. "
            "<bookmark mark='b'/> There is another molecule that can take the oxygen: hydrogen. Then what leaves is "
            f"water. It takes about {Cb['h2_kg']:.0f} kilograms of hydrogen per tonne of iron. <bookmark mark='c'/> Made "
            f"from water with electricity, that is nearly {h2[2.0]['mwh']:.0f} megawatt-hours, and at two to five dollars "
            f"a kilogram, between {h2[2.0]['cost']:.0f} and {h2[5.0]['cost']:.0f} dollars a tonne, on a product that "
            "sells for about a thousand. <bookmark mark='d'/> Cement has no such swap: the carbon dioxide comes from the "
            "limestone itself. The answers are to use less clinker in each tonne, which American cement makers have "
            f"done fast, {Cb['blended']:.0f} per cent of their shipments are now blended cements, and to capture what is "
            "left."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), Write(top[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(top[1]), run_time=1.0)
            vo.wait_until("b")
            self.play(Write(bot[0]), FadeIn(bot[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cost, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cem, shift=UP * 0.1))
        self.clear_scene()

    def border(self):
        Cb = R["carbon"]
        gate = VGroup(Rectangle(width=0.25, height=3.2, stroke_width=0, fill_color="#3E4553", fill_opacity=1).move_to([0, -0.2, 0]),
                      tx("EU border", 16, WHITE, bold=True).move_to([0, 1.7, 0]))
        goods = VGroup(draw.coil(0.35), draw.silo(0.8), draw.can(0.6), draw.sack(0.6, label_="N"), draw.pylon(0.7))
        goods.arrange(DOWN, buff=0.18).move_to([-5.0, -0.2, 0])
        names = VGroup(*[tx(n, 13, GREY_A).next_to(g, LEFT, buff=0.15) for n, g in
                         zip(("iron and steel", "cement", "aluminium", "fertilisers", "electricity"), goods)])
        meter = VGroup(RoundedRectangle(corner_radius=0.1, width=2.6, height=1.0, stroke_color=CARBON, stroke_width=3),
                       tx("pay for the CO2 inside", 15, CARBON, bold=True)).move_to([0, -2.85, 0])
        meter[1].move_to(meter[0])
        law = VGroup(tx("Regulation (EU) 2023/956: the carbon border adjustment", 17, WHITE, bold=True),
                     tx("reporting since 1 October 2023; importers' obligations from 1 January 2026", 15, GREY_A),
                     tx("for cement, iron and steel, aluminium, fertilisers, electricity and hydrogen", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([3.6, 1.9, 0])
        bill = VGroup(tx("And the bill for steel's own transition,", 16, WHITE, bold=True),
                      tx("in the industry's estimate:", 16, WHITE, bold=True),
                      tx(f"${Cb['capex']:.1f} trillion for new and adapted plants,", 16, PRICE, bold=True),
                      tx("plus $2.5-4 trillion in energy and infrastructure", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.05).move_to([3.8, -1.2, 0])
        src = source("Regulation (EU) 2023/956, Article 36 and Annex I; World Steel Association, climate policy paper "
                     "(October 2025)", size=13)
        with self.voiceover(
            "Who pays? <bookmark mark='a'/> Europe's answer is a price on carbon for its own plants, and, so that "
            "imports do not undercut them, a charge at the border. <bookmark mark='b'/> Under a 2023 regulation, "
            "importers of cement, iron and steel, aluminium, fertilisers, electricity and hydrogen have reported the "
            "carbon in their goods since October 2023, and from the first of January 2026 they must pay for it. "
            "<bookmark mark='c'/> And the bill for steel's own transition is enormous. The industry's association "
            f"estimates about {Cb['capex']:.1f} trillion dollars for new and rebuilt plants, and two and a half to four "
            "trillion more for the energy and infrastructure around them. For an industry that, as this film has "
            "shown, earns thin and unreliable profits, that is the hardest question of all."
        ) as vo:
            self.play(FadeIn(gate), FadeIn(goods), FadeIn(names), FadeIn(src))
            vo.wait_until("a")
            self.play(goods.animate.shift(RIGHT * 6.2), names.animate.shift(RIGHT * 3.0).set_opacity(0), run_time=2.5)
            self.play(FadeIn(meter, scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(law, shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(bill, shift=UP * 0.1))
        self.clear_scene()
