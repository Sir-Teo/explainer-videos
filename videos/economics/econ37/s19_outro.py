from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

PROBLEMS = [
    r"Rent gradient: \ commuting costs \$1,000 a kilometre a year and a household near the centre has 150 m$^2$. "
    r"\ How fast must floor rent fall with distance?",
    r"Von Th\"unen: \ grain yields 2.6 tons a hectare, \ sells for \$150 a ton, \ costs \$90 to grow and \$1 a "
    r"ton-kilometre to cart. \ Find its bid rent at the market and where it reaches zero.",
    r"Zipf: \ with an exponent of one and a largest city of 20 million, \ how large are the 10th and the 100th?",
    r"Agglomeration: \ with an elasticity of 0.03, \ how much more productive is a worker in a city twice as "
    r"dense? \ Ten times?",
    r"Quality of life: \ with $\alpha$ = 0.3, \ town A's log wage is 0.10 above B's and its log rent 0.40 above. "
    r"\ Which is nicer, \ and by how much?",
    r"Housing: \ demand rises 20\%, \ demand elasticity 1. \ Find the change in price and quantity with supply "
    r"elasticities 0.6 and 3.",
    r"Core and periphery: \ compute the break point for $\mu$ = 0.4 and $\sigma$ = 5.",
    r"$\bigstar$ \ Gibrat with a floor: \ show that a stationary power law has exponent $1/(1 - s_{\min}/\bar s)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Because crowding together makes people more productive, \ through sharing, \ matching "
                          r"and learning, \ and because small advantages compound, \ activity piles up; \ "
                          r"people follow until rents and congestion offset the gains, \ so in equilibrium the "
                          r"places differ more in prices than in welfare. \ Tight housing turns booms into rents, \ "
                          r"and where a child grows up changes the adult.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        S = load("schelling")
        logo = board(S["frames"][-1], size=1.3).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why is economic activity piled up in a few places, and what does that do to the people in them? "
            "<bookmark mark='a'/> Because crowding together makes people more productive, through sharing, "
            "matching and learning, and because small advantages compound, activity piles up. People follow until "
            "rents and congestion offset the gains, so in equilibrium places differ more in their prices than in "
            "the welfare of the people who live there. Tight housing turns booms into rents, and where a child "
            "grows up changes the adult."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, lag_ratio=0.002), run_time=1.5)
        self.clear_scene()

    def recap(self):
        S, T, M, A, Z, C, R, H, B, TR, P, W = (load(x) for x in (
            "schelling", "thunen", "mono", "agglo", "zipf", "cp", "towns", "housing", "berlin", "transport", "place",
            "wfh"))
        chk = H["chk"]
        items = [
            (rf"Schelling: \ content with a third alike, \ {100 * S['start']:.0f}\% $\to$ {100 * S['final']:.0f}\% "
             r"alike", TEAL),
            (r"von Th\"unen: \ four rings; \ a railway pushes grain from 35 to 70 km", FARM),
            (rf"the city: \ rent falls {M['grad']:.1f}\% a km; \ the car: \ edge {M['base']['edge']:.0f} $\to$ "
             rf"{M['car']['edge']:.0f} km", CITY),
            (rf"agglomeration: \ across towns {A['naive']:.3f}, \ movers {A['movers']:.3f}, \ France 0.02", WAGE),
            (rf"Zipf: \ America's top 100, \ {Z['zeta_100']:.2f}; \ Gibrat's towns, \ {Z['gibrat_zeta']:.2f}", GOLD),
            (rf"core and periphery: \ break {C['break']:.2f}, \ sustain {C['sustain']:.2f}", RENT),
            (rf"spatial equilibrium: \ Harbour +10\%: \ rents +{100 * R['prod']['dlogr']:.0f}\%, \ utility "
             rf"+{100 * R['prod']['dv']:.1f}\% everywhere", AMENITY),
            (rf"housing: \ Saiz 0.60 to 5.45; \ prices since 2000, \ correlation {H['corr']:.2f}", RENT),
            (r"rent control: \ tenants 20\% less mobile, \ rental supply $-$15\%", CITY),
            (rf"Moving to Opportunity: \ +\${chk['gain']:,} a year, \ +{chk['pct']}\%, \ if moved before 13", GAIN),
            (rf"Berlin: \ $\lambda$ = 0.07; \ the line city, \ near the Wall {100 * B['division'][-1]:+.0f}\%", WHITE),
            (rf"transport and places: \ highways $-$18\% a city; \ working from home {W['last12']:.0f}\% of days",
             ROAD),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 37, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        _ = (T, TR, P)
        with self.voiceover(
            "Part thirty-seven in twelve lines. <bookmark mark='a'/> Mild preferences sort a board of coins. Land "
            "goes to whoever bids most, so crops and then commuters arrange themselves in rings, and rents fall "
            "with distance from the centre; cars spread cities out and lifts build them up. Density makes workers "
            "more productive, by less than it seems, because talent sorts into cities. City sizes follow Zipf's "
            "law, which random proportional growth explains. Falling transport costs can tip a country suddenly "
            "into a core and a periphery. In spatial equilibrium, wages, rents and amenities move together, and "
            "local booms become rents, above all where housing is hard to build. Rent control protects sitting "
            "tenants and shrinks the supply. Better neighbourhoods raise the earnings of children who move young. "
            "The Berlin Wall measured how local agglomeration is. And transport, and now remote work, keep "
            "redrawing the map."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The rent gradient; von Thünen's bid rent; Zipf's arithmetic; agglomeration by the "
            "doubling; quality of life read from prices; housing supply and a demand shock; the break point of the "
            "tomahawk; and a starred derivation of Zipf's law from Gibrat's growth with a floor. Full solutions are "
            "in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jan Brueckner, \emph{Lectures on Urban Economics} (2011)",
             r"Edward Glaeser, \emph{Triumph of the City} (2011)",
             r"Masahisa Fujita, \ Paul Krugman and Anthony Venables, \emph{The Spatial Economy} (1999)",
             r"Stephen Redding and Esteban Rossi-Hansberg, \ ``Quantitative Spatial Economics'', \emph{Annual Review "
             r"of Economics} 9 (2017)"],
            [r"von Th\"unen (1826); \ Alonso (1964); \ Schelling (1971); \ Rosen (1979); \ Roback (1982)",
             r"Krugman (1991); \ Ciccone and Hall (1996); \ Gabaix (1999); \ Duranton and Puga (2004)",
             r"Baum-Snow (2007); \ Saiz (2010); \ Combes et al.\ (2010); \ Kline and Moretti (2014)",
             r"Ahlfeldt et al.\ (2015); \ Chetty, \ Hendren and Katz (2016); \ Donaldson (2018)",
             r"Diamond, \ McQuade and Qian (2019); \ Hsieh and Moretti (2019); \ Greaney (2026)"])
        with self.voiceover(
            "The reading: Jan Brueckner's lectures for the models; Edward Glaeser's Triumph of the City; Fujita, "
            "Krugman and Venables for core and periphery; and Redding and Rossi-Hansberg's survey of quantitative "
            "spatial models. Then the papers, from von Thünen to the comment of 2026."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1992, r"David Card and Alan Krueger", r"New Jersey raises its minimum wage from \$4.25 to "
                          r"\$5.05; \ Pennsylvania, \ next door, \ does not; \ two economists survey the fast-food "
                          r"restaurants on both sides of the border", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 38 \ $\cdot$ \ Act VIII, \ Work and the State", font_size=30,
                           color=GREY_B),
                     label(r"Work and Wages", font_size=46),
                     label(r"what sets a wage, \ and what happens when the law sets it instead?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from where people work \ to what they are paid", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked where people work. The next asks what they are paid, and opens a new act: work and the "
            "state. <bookmark mark='a'/> In 1992 New Jersey raised its minimum wage from four dollars and "
            "twenty-five cents to five dollars and five cents an hour. Pennsylvania, next door, did not. David Card "
            "and Alan Krueger surveyed fast-food restaurants on both sides of the border, before and after. "
            "<bookmark mark='b'/> Part thirty-eight: work and wages. What sets a wage, and what happens when the "
            "law sets it instead?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
