from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Harm(VoiceoverScene):
    def construct(self):
        card(self, 11, "The state and harm", "Who pays when a chemical hurts people, and when?",
             "Chapter eleven. The state and harm.", lit=("state",))
        self.bhopal()
        self.pfas()
        self.drops()
        self.bill()

    def bhopal(self):
        H = R["harm"]
        sky = draw.skyline(12.0) if hasattr(draw, "skyline") else VGroup()
        sky.move_to([1.6, -2.2, 0]).set_opacity(0.6)
        plant = VGroup(draw.factory(1.6), draw.tank(0.9) if hasattr(draw, "tank") else VGroup()).arrange(RIGHT, buff=0.2,
                                                                                                          aligned_edge=DOWN)
        plant.move_to([-5.0, -2.0, 0])
        moon = draw.moon(0.4).move_to([5.6, 2.8, 0]) if hasattr(draw, "moon") else VGroup()
        cloud = VGroup(*[Circle(0.5 + 0.1 * (k % 3), stroke_width=0, fill_color="#C9D3A0", fill_opacity=0.22).move_to(
            [-4.6 + 0.9 * k, -1.2 + 0.25 * np.sin(k), 0]) for k in range(12)])
        date = tx("Bhopal, India: midnight, 2 December 1984", 24, WHITE, bold=True).to_edge(UP, buff=0.5)
        facts = VGroup(tx("Union Carbide's pesticide plant leaks methyl isocyanate gas", 17, GREY_A),
                       tx(f"{H['deaths']:,.0f} people killed at once, by the count before the Supreme Court of India", 19, BAD, bold=True),
                       tx("30,000 to 40,000 seriously injured", 17, GREY_A),
                       tx(f"the settlement, 1989: ${H['settlement']:.0f} million", 19, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([0.6, 1.2, 0])
        src = source("Supreme Court of India, Union Carbide Corporation v. Union of India, judgment of 4 May 1989", size=13)
        with self.voiceover(
            "Chemistry has a dark side. "
            "<bookmark mark='a'/> At midnight on the second of December 1984, gas escaped from Union Carbide's plant in "
            "Bhopal, in India: methyl isocyanate, used to make pesticides, which the Supreme Court of India called a "
            "lethal toxic poison. <bookmark mark='b'/> It drifted over the sleeping city. <bookmark mark='c'/> By the "
            f"count before the court, {H['deaths']:,.0f} people died at once, and thirty to forty thousand were seriously "
            "injured; the court itself spoke of tens of thousands left impaired. <bookmark mark='d'/> In 1989 the court "
            f"ordered Union Carbide to pay {H['settlement']:.0f} million dollars to settle the claims."
        ) as vo:
            self.play(FadeIn(sky), FadeIn(plant), FadeIn(moon), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(date), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_, scale=0.3) for c_ in cloud], lag_ratio=0.15), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(facts[1:3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(facts[3], shift=UP * 0.1))
        self.clear_scene()

    def pfas(self):
        H = R["harm"]
        chainc = VGroup()
        for k in range(8):
            c = Circle(0.2, stroke_width=0, fill_color=ATOMC, fill_opacity=1).move_to([-3.0 + 0.6 * k, 1.6 + (0.12 if k % 2 else -0.12), 0])
            chainc.add(c)
            for s_ in (1, -1):
                f_ = Circle(0.15, stroke_width=0, fill_color=GOOD, fill_opacity=1).move_to(c.get_center() + np.array([0, 0.48 * s_, 0]))
                chainc.add(Line(c.get_center(), f_.get_center(), stroke_color="#C9D3E0", stroke_width=2), f_)
        bonds = VGroup(*[Line([-3.0 + 0.6 * k, 1.6 + (0.12 if k % 2 else -0.12), 0], [-2.4 + 0.6 * k, 1.6 + (-0.12 if k % 2 else 0.12), 0],
                              stroke_color="#C9D3E0", stroke_width=3) for k in range(7)])
        cl = VGroup(tx("PFAS: chains of carbon wrapped in fluorine", 18, GOOD, bold=True),
                    tx("among the strongest bonds in chemistry, so they hardly break down", 15, GREY_A)).arrange(
            DOWN, buff=0.06).next_to(chainc, DOWN, buff=0.3)
        uses = VGroup(tx("non-stick and stain-proof coatings, waterproof fabrics,", 16, WHITE),
                      tx("and firefighting foam", 16, WHITE)).arrange(DOWN, buff=0.04).move_to([0, -1.6, 0])
        nick = tx("'forever chemicals'", 22, GOLD, bold=True).next_to(uses, DOWN, buff=0.35)
        with self.voiceover(
            "The other kind of harm is slow. <bookmark mark='a'/> PFAS are a large family of chemicals built on "
            "chains of carbon atoms wrapped in fluorine. The bond between carbon and fluorine is among the strongest in "
            "chemistry, which is what makes them useful <bookmark mark='b'/> in non-stick and stain-proof coatings, "
            "waterproof fabrics and firefighting foam. <bookmark mark='c'/> It is also why they barely break down. "
            "They have spread into water supplies, and they have earned a nickname: forever chemicals."
        ) as vo:
            self.play(Create(bonds), LaggedStart(*[FadeIn(m) for m in chainc], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(cl), Indicate(VGroup(bonds, chainc), color=GOOD, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(uses, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(nick, scale=1.2))
        del H
        self.clear_scene()

    def drops(self):
        H = R["harm"]
        mcl = H["mcl"]
        drop_ml, pool_m3 = 0.05, 2500.0
        pools_n = 4 * drop_ml / (mcl * 1e-12) / 1e6 / pool_m3
        n = int(round(pools_n))
        pools = VGroup(*[RoundedRectangle(corner_radius=0.05, width=1.0, height=0.5, stroke_color=GAS, stroke_width=1.5,
                                          fill_color=GAS, fill_opacity=0.25) for _ in range(n)]).arrange_in_grid(
            rows=4, buff=0.18).move_to([-2.2, -0.6, 0])
        drops = VGroup(*[Triangle(stroke_width=0, fill_color=BAD, fill_opacity=1).scale(0.15).rotate(PI) for _ in range(4)]).arrange(
            RIGHT, buff=0.15).next_to(pools, UP, buff=0.5)
        head = tx(f"The EPA's limit for PFOA and PFOS in drinking water, 2024: {mcl:.0f} parts per trillion", 21, WHITE, bold=True).to_edge(
            UP, buff=0.4)
        cap = VGroup(tx("four drops", 20, BAD, bold=True), tx(f"in about {n} Olympic swimming pools", 20, GAS, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.3, -0.4, 0])
        tag = estimate_tag(f"arithmetic: a drop of {drop_ml:.2f} ml; a pool of {pool_m3:,.0f} cubic metres", corner=DR, size=12)
        src = source("US EPA, PFAS National Primary Drinking Water Regulation, Federal Register, 26 April 2024", size=13)
        with self.voiceover(
            "How little is too much? <bookmark mark='a'/> In April 2024 the Environmental Protection Agency set a limit "
            f"for the two best-known PFAS, PFOA and PFOS, in drinking water: {mcl:.0f} parts per trillion. "
            f"<bookmark mark='b'/> Four parts per trillion is about four drops in {n} Olympic swimming pools. "
            "<bookmark mark='c'/> Measuring that little, and taking it out of a city's water, is expensive, and someone "
            "has to pay for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            big = VGroup(tx(f"{mcl:.0f}", 120, GOLD, bold=True), tx("parts per trillion", 30, GOLD)).arrange(DOWN, buff=0.2).move_to(
                [0, -0.4, 0])
            self.play(FadeIn(big, scale=1.3))
            vo.wait_until("a")
            self.play(Indicate(head, color=GOLD, scale_factor=1.03), Indicate(big, color=GOLD))
            vo.wait_until("b")
            self.play(FadeOut(big, scale=0.5))
            self.play(LaggedStart(*[FadeIn(p_, scale=0.8) for p_ in pools], lag_ratio=0.05), FadeIn(tag), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(d_, shift=DOWN * 0.3) for d_ in drops], lag_ratio=0.2), FadeIn(cap), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(cap, color=GAS))
        self.clear_scene()

    def bill(self):
        H = R["harm"]
        sc = 0.42
        rows = [("3M", H["mmm"], f"${H['mmm_lo']:.1f}-{H['mmm']:.1f}bn", "to US public water systems, 2023; and a plan to stop making PFAS"),
                ("Chemours, DuPont and Corteva", H["cc"], f"${H['cc']:.3f}bn", "to US water systems, 2023"),
                ("Union Carbide, Bhopal", H["settlement"] / 1000, f"${H['settlement'] / 1000:.2f}bn", "1989, in the money of the day")]
        bars = VGroup()
        for i, (name, v, lab, note) in enumerate(rows):
            y = 1.3 - 1.4 * i
            b = Rectangle(width=v * sc, height=0.5, stroke_width=0, fill_color=BAD if i < 2 else PRICE, fill_opacity=0.85).move_to(
                [-3.0, y, 0], aligned_edge=LEFT)
            if i == 0:
                lo = Rectangle(width=H["mmm_lo"] * sc, height=0.5, stroke_width=0, fill_color=BAD, fill_opacity=1).move_to(
                    [-3.0, y, 0], aligned_edge=LEFT)
                b.set_fill(opacity=0.4)
                b = VGroup(b, lo)
            bars.add(VGroup(tx(name, 17, WHITE, bold=True).move_to([-3.0, y + 0.5, 0], aligned_edge=LEFT), b,
                            tx(lab, 17, BAD if i < 2 else PRICE, bold=True).next_to(b, RIGHT, buff=0.15),
                            tx(note, 13, GREY_A).move_to([-3.0, y - 0.45, 0], aligned_edge=LEFT)))
        head = tx("Settlements", 24, WHITE, bold=True).to_edge(UP, buff=0.4)
        lesson = VGroup(tx("The harm is paid for decades after the profit,", 17, GOLD, bold=True),
                        tx("often by people who never bought the product.", 17, GOLD, bold=True)).arrange(DOWN, buff=0.05).to_edge(
            DOWN, buff=0.7)
        src = source("3M, Form 8-K (22 June 2023); The Chemours Company, Form 8-K (2 June 2023); Supreme Court of India (1989)", size=13)
        with self.voiceover(
            "And the bills have arrived. <bookmark mark='a'/> In 2023, 3M agreed to pay American public water "
            f"systems between {H['mmm_lo']:.1f} and {H['mmm']:.1f} billion dollars over PFAS, and said it planned to stop "
            "making them. <bookmark mark='b'/> Chemours, DuPont and Corteva agreed to a fund of about "
            f"{H['cc']:.2f} billion dollars. <bookmark mark='c'/> Next to them, Bhopal's {H['settlement']:.0f} million "
            "dollars, in the money of 1989. <bookmark mark='d'/> This is the pattern of chemical harm. The products "
            "were sold, and the profits booked, decades before the bill; and the people who pay first are often "
            "people who never bought them. That is why governments set limits, and why a chemical company's filings "
            "carry pages of lawsuits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[0]) for b_ in bars])
            for m_, b_ in zip("abc", bars):
                vo.wait_until(m_)
                self.play(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]), FadeIn(b_[3]), Indicate(b_[0]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()


ATOMC = "#4A505C"
