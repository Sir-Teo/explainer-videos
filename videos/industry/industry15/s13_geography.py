from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

SITES = {"Hsinchu": (121.0, 24.78), "Central Taiwan": (120.62, 24.2), "Southern Taiwan": (120.28, 23.1),
         "Washington, US": (-122.4, 45.6), "Shanghai, China": (121.2, 31.0), "Nanjing, China": (118.8, 32.05),
         "Arizona, US": (-112.1, 33.8), "Kumamoto, Japan": (130.8, 32.9)}
DRESDEN = (13.74, 51.05)
TW = {"Hsinchu": (121.35, 24.65), "Central Taiwan": (120.95, 24.05), "Southern Taiwan": (120.65, 23.05)}  # inset, nudged onto the coarse coastline
TIGHT, LOOSE = "#E8554E", "#7BD88F"


def nm_col(nm: float) -> str:
    return PRICE if nm <= 3 else LIGHT if nm <= 7 else DIE if nm <= 40 else SILICON


class Geography(VoiceoverScene):
    def construct(self):
        card(self, 11, "Geography and the state", "Why do governments care where chips are made?",
             "Chapter eleven. Geography and the state.", lit=("moat", "change"))
        self.fabs()
        self.money()
        self.controls()
        self.regions()

    def fabs(self):
        G = R["geography"]
        F, Y = G["fabs"], G["fab_year"]
        wm = draw.world_map(12.6, lon=(-130, 150), lat=(8, 60)).move_to([0, 1.55, 0])
        dots, rings = VGroup(), VGroup()
        for place, d in F.items():
            lo, la = SITES[place]
            dots.add(Dot(wm.p(lo, la), radius=0.07 + 0.025 * len(d), color=nm_col(min(d.values()))).set_z_index(3))
        dres = Circle(radius=0.09, stroke_color=WHITE, stroke_width=2.5).move_to(wm.p(*DRESDEN)).set_z_index(3)
        # Taiwan, enlarged
        tw = draw.world_map(1.9, lon=(119.6, 122.4), lat=(21.8, 25.5)).move_to([4.9, -1.75, 0])
        twbox = SurroundingRectangle(tw, buff=0.08, stroke_color=GREY_B, stroke_width=1.5)
        tdots, tlabs = VGroup(), VGroup()
        for place in ("Hsinchu", "Central Taiwan", "Southern Taiwan"):
            lo, la = TW[place]
            d = F[place]
            row = VGroup(*[Dot(radius=0.065, color=nm_col(nm)) for f, nm in sorted(d.items(), key=lambda kv: kv[1])])
            row.arrange_in_grid(cols=min(3, len(d)), buff=0.04)
            row.move_to(tw.p(lo, la)).align_to(tw.p(lo, la), RIGHT)
            tdots.add(row.set_z_index(3))
            tlabs.add(tx(f"{place.replace(' Taiwan', '')}: {len(d)} fab{'s' if len(d) > 1 else ''}, to {min(d.values()):.0f}nm", 13, GREY_A))
        tlabs.arrange(DOWN, aligned_edge=RIGHT, buff=0.1).next_to(twbox, LEFT, buff=0.25).align_to(twbox, UP).shift(DOWN * 0.3)
        zoom = DashedLine(wm.p(121, 23.8), twbox.get_top(), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.06)
        # the fabs abroad
        rows = [("Arizona, US", 21), ("Kumamoto, Japan", 23), ("Nanjing, China", 16), ("Shanghai, China", 10), ("Washington, US", 11)]
        cards = VGroup()
        for place, f in rows:
            nm = F[place][f]
            cards.add(VGroup(Dot(radius=0.07, color=nm_col(nm)), tx(f"{place}: Fab {f}, since {Y[f]}, {nm:.0f}nm", 14, WHITE)).arrange(RIGHT, buff=0.12))
        cards.add(VGroup(Circle(radius=0.07, stroke_color=WHITE, stroke_width=2), tx("Dresden, Germany: Fab 24, being built", 14, WHITE)).arrange(RIGHT, buff=0.12))
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.7, -1.85, 0])
        key = VGroup(*[VGroup(Dot(radius=0.07, color=c), tx(t, 12, GREY_B)).arrange(RIGHT, buff=0.08)
                       for c, t in ((PRICE, "2-3nm"), (LIGHT, "5-7nm"), (DIE, "16-40nm"), (SILICON, "110nm+"))]).arrange(RIGHT, buff=0.3)
        key.move_to([0, 3.55, 0])
        src = source("TSMC, Form 20-F 2025: fabs in operation as of 28 February 2026, their locations and most advanced processes", size=13)
        with self.voiceover(
            "Where are the chips made? Take the biggest foundry. <bookmark mark='a'/> TSMC listed "
            f"{G['n_fabs']} fabs in operation in early 2026. <bookmark mark='b'/> {G['n_taiwan']} of them are in Taiwan, "
            "in three science parks: Hsinchu, Central Taiwan and Southern Taiwan. <bookmark mark='c'/> And the "
            f"{len(G['leading'])} fabs making its most advanced chips, at two and three nanometres, are all among them. "
            "<bookmark mark='d'/> The rest are abroad: an old fab in Washington State, two in China, one in Kumamoto in "
            f"Japan, and in Arizona a fab producing since 2024 at {G['best_abroad']:.0f} nanometres. "
            "<bookmark mark='e'/> A fab in Dresden, Germany, is being built. The most valuable machines in the industry sit, "
            "for now, mostly on one island."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(zoom), FadeIn(tw), Create(twbox))
            self.play(LaggedStart(*[FadeIn(r_, scale=0.6) for r_ in tdots], lag_ratio=0.3), FadeIn(tlabs), run_time=1.5)
            vo.wait_until("c")
            gold = [d for r_ in tdots for d in r_ if d.get_color() == ManimColor(PRICE)]
            self.play(*[Indicate(d, color=PRICE, scale_factor=1.6) for d in gold], run_time=1.2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in cards[:5]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("e")
            self.play(Create(dres), FadeIn(cards[5], shift=RIGHT * 0.1))
        self.clear_scene()

    def money(self):
        G = R["geography"]
        usa = draw.capitol(1.5).move_to([-4.6, 1.4, 0])
        ger = draw.capitol(1.5, "#E6D9A8").move_to([-4.6, -1.5, 0])
        az = draw.chip_fab(2.4).move_to([3.4, 1.4, 0])
        dd = draw.chip_fab(2.4, accent=PRICE).move_to([3.4, -1.5, 0])
        lu = tx("US Department of Commerce", 15, GREY_A).next_to(usa, DOWN, buff=0.12)
        lg = tx("Germany", 15, GREY_A).next_to(ger, DOWN, buff=0.12)
        la = tx("TSMC Arizona, Phoenix", 15, GREY_A).next_to(az, DOWN, buff=0.12)
        ld = tx("ESMC (TSMC), Dresden", 15, GREY_A).next_to(dd, DOWN, buff=0.12)
        d1 = VGroup(tx(f"up to ${G['chips_tsm']:.1f}bn of grants", 19, PRICE, bold=True), tx("and up to $5bn of loans", 15, WHITE),
                    tx("CHIPS Act, November 2024", 13, GREY_B)).arrange(DOWN, buff=0.05).move_to([-0.6, 2.25, 0])
        d2 = VGroup(tx(f"up to €{G['esmc']:.0f}bn of state aid", 19, PRICE, bold=True), tx("European Chips Act, December 2024", 13, GREY_B)).arrange(
            DOWN, buff=0.05).move_to([-0.6, -0.65, 0])
        intel = tx(f"and Intel: {G['intel_shares']:.0f} million shares now held by the US government (chapter six)", 15, GREY_A).move_to([0, -3.1, 0])
        src = source("TSMC, Form 20-F 2025 (CHIPS Act and European Chips Act agreements); Intel, Form 10-K 2025", size=13)
        with self.voiceover(
            "Governments want those fabs at home, and they pay for them. <bookmark mark='a'/> In November 2024 America's "
            f"Commerce Department agreed to give TSMC's Arizona company up to ${G['chips_tsm']:.1f} billion under the CHIPS "
            "Act, and to lend it up to 5 billion more. <bookmark mark='b'/> A month later Germany agreed to up to "
            f"{G['esmc']:.0f} billion euros of state aid for TSMC's fab in Dresden. <bookmark mark='c'/> And, as we saw, "
            f"the American government now holds {G['intel_shares']:.0f} million shares of Intel. A chip factory used to be "
            "a business decision. Now it is also a matter of state."
        ) as vo:
            self.play(FadeIn(src), FadeIn(usa), FadeIn(lu), FadeIn(az), FadeIn(la), FadeIn(ghost(ger, dd, d1, d2)))
            vo.wait_until("a")
            coins, anim = draw.coin_flow(usa.get_right() + RIGHT * 0.2, az.get_left() + LEFT * 0.1, n=8, arc=-0.5)
            self.add(coins)
            self.play(anim, FadeIn(d1, shift=UP * 0.1))
            self.remove(coins)
            vo.wait_until("b")
            self.play(FadeIn(ger), FadeIn(lg), FadeIn(dd), FadeIn(ld))
            coins, anim = draw.coin_flow(ger.get_right() + RIGHT * 0.2, dd.get_left() + LEFT * 0.1, n=6, arc=-0.5)
            self.add(coins)
            self.play(anim, FadeIn(d2, shift=UP * 0.1))
            self.remove(coins)
            vo.wait_until("c")
            self.play(FadeIn(intel, shift=UP * 0.1))
        self.clear_scene()

    def controls(self):
        G = R["geography"]
        x0, x1, t0, t1 = -6.2, 6.2, 2022.4, 2027.1

        def X(t):
            return x0 + (t - t0) / (t1 - t0) * (x1 - x0)
        axis = Line([x0, -0.2, 0], [x1, -0.2, 0], stroke_color=GREY_B, stroke_width=2.5)
        ticks = VGroup(*[VGroup(Line([X(y), -0.3, 0], [X(y), -0.1, 0], stroke_color=GREY_B, stroke_width=2),
                                tx(str(y), 14, GREY_B).move_to([X(y) + 1.33, -0.5, 0])) for y in range(2023, 2027 + 1) if X(y) < x1]).set_opacity(0.9)
        ticks.add(tx("2022", 14, GREY_B).move_to([X(2022.7), -0.5, 0]))
        ev = [(2022.78, 1, "October 2022", "licences for advanced AI chips and\nchipmaking tools for China", "87 FR 62186", True, "c"),
              (2023.82, 2, "October 2023", "the rules tightened and widened", "88 FR 73458", True, "c"),
              (2024.93, 1, "December 2024", "more chipmaking machines made\nabroad brought under the rules", "89 FR 96790", True, "l"),
              (2025.04, 3, "January 2025", "a framework to ration AI chips\nworldwide; never enforced", "90 FR 4544", True, "c"),
              (2025.30, 2, "April 2025", f"Nvidia's H20 needs a licence:\na ${G['h20']:.1f}bn charge", "Nvidia 10-K", True, "r"),
              (2025.62, 1, "August 2025", "some H20 licences granted", "Nvidia 10-K", False, "c"),
              (2026.04, 2, "January 2026", "H200 to China: case by case\ninstead of presumed denial", "91 FR 1684", False, "c"),
              (2026.89, 1, "November 2026", "data centres abroad serving Chinese\nfirms; 5 more countries; the 2025\nframework formally rescinded", "91 FR 74970", True, "c")]
        marks, labels = [], []
        for t, tier, when, what, cite, tight, side in ev:
            col = TIGHT if tight else LOOSE
            y = -0.2 + (0.95 * tier if tight else -0.95 * tier)
            stem = Line([X(t), -0.2, 0], [X(t), y, 0], stroke_color=col, stroke_width=2)
            tri = Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.09).move_to([X(t), -0.2, 0])
            if not tight:
                tri.rotate(PI)
            lines = what.split("\n")
            lab = VGroup(tx(when, 14, col, bold=True), *[tx(s_, 12, WHITE) for s_ in lines], tx(cite, 11, GREY_B)).arrange(DOWN, buff=0.03)
            lab.next_to([X(t), y, 0], UP if tight else DOWN, buff=0.05)
            if side == "l":
                lab.align_to([X(t) - 0.08, 0, 0], RIGHT).shift(DOWN * (lab.height + 0.05))
            elif side == "r":
                lab.align_to([X(t) + 0.08, 0, 0], LEFT).shift(DOWN * (lab.height + 0.05))
            if lab.get_right()[0] > 6.9:
                lab.shift(LEFT * (lab.get_right()[0] - 6.9))
            if lab.get_left()[0] < -6.9:
                lab.shift(RIGHT * (-6.9 - lab.get_left()[0]))
            marks.append(VGroup(stem, tri))
            labels.append(lab)
        kt = VGroup(VGroup(Triangle(fill_color=TIGHT, fill_opacity=1, stroke_width=0).scale(0.09), tx("tighter", 13, TIGHT)).arrange(RIGHT, buff=0.08),
                    VGroup(Triangle(fill_color=LOOSE, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI), tx("looser", 13, LOOSE)).arrange(RIGHT, buff=0.08)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([-5.9, -2.6, 0])
        src = source("Federal Register: Bureau of Industry and Security rules 87 FR 62186, 88 FR 73458, 89 FR 96790, 90 FR 4544, 91 FR 1684, "
                     "91 FR 74970; NVIDIA, Form 10-K FY2026", size=12)
        groups = [(0,), (1, 2), (3,), (4,), (5, 6), (7,)]
        with self.voiceover(
            "And governments decide who may buy the chips. <bookmark mark='a'/> In October 2022 America required licences "
            "to send China the most advanced AI chips and the tools to make them. <bookmark mark='b'/> It tightened the "
            "rules in October 2023, and in December 2024 extended them to more chipmaking machines made abroad with "
            "American technology. <bookmark mark='c'/> In January 2025 it published a framework to ration AI chips across "
            "the whole world. It was never enforced. <bookmark mark='d'/> In April 2025 even Nvidia's H20, a chip it sold "
            f"in China, needed a licence, and Nvidia took a charge of ${G['h20']:.1f} billion. <bookmark mark='e'/> Then "
            "the rules loosened: licences for some H20s that August, and in January 2026 case-by-case review for the "
            "more powerful H200. <bookmark mark='f'/> And in November 2026 a new rule reached data centres abroad that "
            "rent computing to Chinese companies, required licences for five more countries, and formally rescinded the "
            "2025 framework. For a chip company, who may buy is now a forecast in itself."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(kt), FadeIn(src))
            for mk, grp in zip("abcdef", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[AnimationGroup(Create(marks[i]), FadeIn(labels[i], shift=UP * 0.1)) for i in grp], lag_ratio=0.5),
                          run_time=1.0 + 0.4 * len(grp))
        self.clear_scene()

    def regions(self):
        G = R["geography"]
        Rg = G["regions"]
        names = {"ap": "Asia Pacific", "am": "the Americas", "eu": "Europe", "jp": "Japan"}
        order = ["ap", "am", "eu", "jp"]
        sc = 7.0 / 850
        rows = VGroup()
        for i, k in enumerate(order):
            a, b = Rg[k]
            y = 1.6 - 1.25 * i
            lab = tx(names[k].replace("the ", "").capitalize() if k == "am" else names[k], 18, WHITE, bold=True).next_to([-3.6, y, 0], LEFT, buff=0)
            b25 = Rectangle(width=a * sc, height=0.42, stroke_width=0, fill_color=DIE, fill_opacity=0.9).move_to([-3.4, y + 0.22, 0], aligned_edge=LEFT)
            b26 = Rectangle(width=b * sc, height=0.42, stroke_color=PRICE, stroke_width=2, fill_color=PRICE, fill_opacity=0.25).move_to(
                [-3.4, y - 0.24, 0], aligned_edge=LEFT)
            v25 = tx(f"${a:.0f}bn", 14, DIE).next_to(b25, RIGHT, buff=0.1)
            v26 = tx(f"${b:.0f}bn  (+{100 * (b / a - 1):.0f}%)", 15, PRICE, bold=True).next_to(b26, RIGHT, buff=0.1)
            rows.add(VGroup(lab, b25, v25, b26, v26))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=DIE, fill_opacity=0.9), tx("2025", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_color=PRICE, stroke_width=2, fill_color=PRICE, fill_opacity=0.25), tx("2026, forecast of May 2026", 14, GREY_A)).arrange(
                         RIGHT, buff=0.08)).arrange(RIGHT, buff=0.5).move_to([0.6, 2.75, 0])
        head = tx("Chip sales by where the buyer is", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("World Semiconductor Trade Statistics, Spring 2026 forecast (sales by region)", size=13)
        a, b = Rg["am"]
        with self.voiceover(
            "And where are chips bought? WSTS also counts sales by where the buyer is. <bookmark mark='a'/> In 2025 "
            f"buyers in Asia Pacific took the most, about ${Rg['ap'][0]:.0f} billion, then the Americas, "
            f"${Rg['am'][0]:.0f} billion, Europe ${Rg['eu'][0]:.0f} billion, and Japan ${Rg['jp'][0]:.0f} billion. "
            f"<bookmark mark='b'/> For 2026, its spring forecast had sales to the Americas up {100 * (b / a - 1):.0f} "
            f"per cent, to ${b:.0f} billion, the fastest growth of any region, against {100 * (Rg['eu'][1] / Rg['eu'][0] - 1):.0f} "
            f"per cent for Europe and {100 * (Rg['jp'][1] / Rg['jp'][0] - 1):.0f} for Japan. The chips are made mostly in "
            "Asia, and bought, more and more, wherever the data centres are being built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[1] for r_ in rows])))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[3], LEFT), FadeIn(r_[4])) for r_ in rows], lag_ratio=0.25), run_time=2.5)
            self.play(Indicate(rows[1][4], color=PRICE))
        self.clear_scene()
