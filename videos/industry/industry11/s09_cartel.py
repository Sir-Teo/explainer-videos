from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Cartel(VoiceoverScene):
    def construct(self):
        card(self, 8, "The home market rule", "What do cement makers do when the circles overlap?",
             "Chapter eight. The home market rule.", lit=("moat",))
        self.europe()
        self.verdict()
        self.swaps()

    def europe(self):
        C = R["cement"]["cartel"]
        wm = draw.world_map(13.0, lon=(-12, 32), lat=(34, 62)).move_to([0, -0.4, 0])
        hubs = {"France": (2.5, 46.5), "Germany": (10.0, 51.0), "Italy": (12.5, 42.8), "Spain": (-3.7, 40.3),
                "Belgium": (4.5, 50.6), "UK": (-1.8, 52.8), "Greece": (22.0, 39.3)}
        rings = VGroup()
        for n, (lo, la) in hubs.items():
            p = wm.p(lo, la)
            rings.add(VGroup(Circle(radius=0.55, stroke_color=PRICE, stroke_width=2, fill_color=PRICE, fill_opacity=0.12).move_to(p),
                             tx(n, 13, WHITE, bold=True).move_to(p)))
        pairs = [("Greece", "Italy"), ("Spain", "France"), ("Belgium", "Germany"), ("France", "UK")]
        arrows = VGroup()
        for a, b in pairs:
            pa_, pb_ = wm.p(*hubs[a]), wm.p(*hubs[b])
            ar = Arrow(pa_, pb_, buff=0.35, color=CARBON, stroke_width=3, tip_length=0.15)
            mid = (pa_ + pb_) / 2
            x = VGroup(Line(mid + UL * 0.12, mid + DR * 0.12, stroke_color=WHITE, stroke_width=4),
                       Line(mid + UR * 0.12, mid + DL * 0.12, stroke_color=WHITE, stroke_width=4))
            arrows.add(VGroup(ar, x))
        rule = VGroup(tx("14 January 1983: \"non-transhipment to home markets\"", 20, PRICE, bold=True),
                      tx("no exports within Europe that might destabilise a neighbour's market", 15, GREY_A)).arrange(
            DOWN, buff=0.05).to_edge(UP, buff=0.35)
        note = VGroup(tx("\"(1) Home market principle OK.", 19, WHITE, bold=True),
                      tx("But is it easily complied with - In Belgium?\"", 19, WHITE, bold=True),
                      tx("a handwritten note of an industry meeting, in the Commission's file", 13, GREY_A)).arrange(
            DOWN, buff=0.05, aligned_edge=LEFT).to_corner(DL, buff=0.55)
        src = source("European Commission Decision 94/815/EC; Court of First Instance, Press Release 16/00 (2000)",
                     corner=DR, size=12)
        with self.voiceover(
            "Circles that overlap are a temptation. Where two plants' markets meet, they compete on price, and a "
            "producer with a spare kiln can always ship to a neighbour's town by sea or by rail. <bookmark mark='a'/> "
            "In Western Europe, the cement industry's leaders found a way round that. The European Commission later "
            "established that at a meeting on the fourteenth of January 1983 they agreed a rule of, in its words, "
            "non-transhipment to home markets: <bookmark mark='b'/> no exports into another country's market that "
            "might destabilise it. Each country's producers kept their own circle. <bookmark mark='c'/> In the "
            "Commission's file there is a handwritten note of one meeting. It reads: Home market principle OK. But is "
            "it easily complied with, in Belgium?"
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), LaggedStart(*[FadeIn(r_) for r_ in rings], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rule, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a_[0]) for a_ in arrows], lag_ratio=0.2), run_time=1.5)
            self.play(LaggedStart(*[Create(a_[1]) for a_ in arrows], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(note, shift=UP * 0.1))
        self.clear_scene()

    def verdict(self):
        C = R["cement"]["cartel"]
        stamp = VGroup(RoundedRectangle(corner_radius=0.1, width=5.6, height=1.6, stroke_color=CARBON, stroke_width=5),
                       VGroup(tx("30 November 1994", 22, CARBON, bold=True),
                              tx(f"{C['parties']:.0f} companies and associations", 20, WHITE),
                              tx(f"fined about EUR {C['fine']:.0f} million in all", 20, WHITE)).arrange(DOWN, buff=0.06)
                       ).rotate(0.06).move_to([-2.6, 0.9, 0])
        names = VGroup(tx("Among the addressees:", 15, GREY_A),
                       tx("Holderbank, Lafarge Coppée, Heidelberger Zement,", 15, WHITE),
                       tx("Dyckerhoff, Italcementi, Fratelli Buzzi, Vicat,", 15, WHITE),
                       tx("Ciments Français, Cimpor, Secil, Aalborg Portland", 15, WHITE)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.6, 0.8, 0])
        court = VGroup(tx(f"15 March 2000: the Court of First Instance cuts the fines by almost EUR {C['cut']:.0f} million,", 16,
                          PRICE),
                       tx("mostly for flaws in the procedure; the cartel's finding largely stands", 15, GREY_A)).arrange(
            DOWN, buff=0.05).to_edge(DOWN, buff=1.0)
        why = VGroup(tx("Why cement is prone to it:", 17, WHITE, bold=True),
                     tx("few plants in each region, an identical product,", 15, GREY_A),
                     tx("heavy fixed costs, and prices everyone can see", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.04).move_to([-2.8, -1.4, 0])
        src = source("European Commission Decision 94/815/EC, Article 12 (addressees); Court of First Instance, Press "
                     "Release 16/00 (15 March 2000)", size=13)
        with self.voiceover(
            f"<bookmark mark='a'/> On the thirtieth of November 1994, the Commission fined {C['parties']:.0f} cement "
            f"companies and trade associations a total of about {C['fine']:.0f} million euros. <bookmark mark='b'/> The "
            "names on the decision include Holderbank, Lafarge, Heidelberger Zement, Italcementi, Buzzi and Vicat: many "
            "of them still names, or the roots of names, among the biggest cement companies today. "
            f"<bookmark mark='c'/> In 2000, a European court cut the fines by almost {C['cut']:.0f} million euros, mostly "
            "because of flaws in how the case was run, not because the agreement had not existed. <bookmark mark='d'/> "
            "Cement is prone to it, for the reasons this chapter and the last describe: a few plants in each region, a "
            "product that is the same whoever makes it, heavy fixed costs, and prices that everyone can see."
        ) as vo:
            self.play(FadeIn(src), FadeIn(stamp, scale=1.4), run_time=0.8)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(names, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(court, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def swaps(self):
        L = {c["ticker"]: c for c in R["landscape"]["companies"]}
        cards_ = VGroup()
        items = [("Holcim → Amrize", f"23 June 2025: Holcim spins off its North American business; "
                  f"{get('amrz.cement_plants'):.0f} cement plants", draw.silo(0.9)),
                 ("Martin Marietta → CRH", f"February 2024: South Texas cement sold for ${get('mlm.crh.2024'):.1f} billion",
                  draw.rotary_kiln(1.1)),
                 ("Martin Marietta ↔ QUIKRETE", "pending: the Midlothian cement plant swapped for quarries", draw.quarry(1.2, 0.5))]
        for h, d, ic in items:
            ic.scale_to_fit_height(0.6)
            if ic.width > 1.2:
                ic.scale_to_fit_width(1.2)
            cards_.add(VGroup(ic, VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.04)).arrange(RIGHT, buff=0.35))
        cards_.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-0.6, 0.0, 0])
        head = tx("Trading the circles", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        rev = VGroup(tx("Revenue, latest year", 15, WHITE, bold=True),
                     tx(f"CRH ${L['CRH']['revenue']:.1f}bn", 15, CEMENT), tx(f"Cemex ${L['CX']['revenue']:.1f}bn", 15, CEMENT),
                     tx(f"Amrize ${L['AMRZ']['revenue']:.1f}bn", 15, CEMENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to(
            [5.4, -2.2, 0])
        src = source("Amrize and Martin Marietta, Forms 10-K 2025; SEC company facts (CRH, Amrize; Cemex's 20-F for 2024)",
                     size=13)
        with self.voiceover(
            "Today the circles are bought, sold and swapped like pieces on a board. <bookmark mark='a'/> In June 2025, "
            "Holcim, the Swiss cement group, spun off its North American business as a separate "
            f"company, Amrize, with {get('amrz.cement_plants'):.0f} cement plants. <bookmark mark='b'/> Martin Marietta "
            f"sold its South Texas cement plant to CRH for {get('mlm.crh.2024'):.1f} billion dollars in 2024, "
            "<bookmark mark='c'/> and agreed to swap its other Texas cement plant with QUIKRETE for quarries. A company "
            "that owned both chose to keep the stone and sell the cement. We will see why in chapter eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(rev))
            for m_, c_ in zip("abc", cards_):
                vo.wait_until(m_)
                self.play(FadeIn(c_, shift=RIGHT * 0.2))
        self.clear_scene()
