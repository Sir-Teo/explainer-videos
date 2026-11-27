from __future__ import annotations

from videos.industry.industry22.common import *  # noqa: F403


class Tobacco(VoiceoverScene):
    def construct(self):
        card(self, 7, "Tobacco: price against volume", "How does a business grow while selling less every year?",
             "Chapter seven. Tobacco. The most profitable legal products in this film are sold in falling numbers, at rising "
             "prices. It is the extreme case of this film's question, and one where the law sets the limits.", lit=("change", "moat"))
        self.bridge()
        self.margin()
        self.brand()
        self.smokefree()

    def bridge(self):
        T = R["tobacco"]
        items = [("lost to lower volume", T["volfx"] / 1e3, BAD, f"-${-T['volfx'] / 1e3:.2f}bn"),
                 ("gained from higher prices", T["price"] / 1e3, GOOD, f"+${T['price'] / 1e3:.2f}bn")]
        rows = hbars(items, max_value=2.6, x0=0.4, top=0.6, row=1.1, length=5.0, size=18, bar_h=0.55)
        packs = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.42, height=0.6, stroke_width=0, fill_color="#E8EAED", fill_opacity=1)
                         for _ in range(10)]).arrange(RIGHT, buff=0.12).move_to([0, 2.2, 0])
        for p in packs:
            p.add(Rectangle(width=0.42, height=0.18, stroke_width=0, fill_color=BAD, fill_opacity=1).move_to(p.get_top() + DOWN * 0.09))
        vol = tx(f"cigarettes shipped: {T['vol']:.1f} billion, {T['fall']:.0f}% in a year", 18, WHITE, bold=True).move_to([0, -1.9, 0])
        src = source("Altria Group, Inc., Form 10-K 2025: smokeable products segment", size=12)

        def fade(vo):
            self.play(packs[-1].animate.set_opacity(0.15), run_time=0.8)
        beat(self,
             "Altria sells Marlboro in America. <bookmark mark='a'/> In 2025 it shipped "
             f"{T['vol']:.1f} billion cigarettes, ten per cent fewer than the year before. <bookmark mark='b'/> Fewer "
             f"cigarettes cost it {-T['volfx'] / 1e3:.1f} billion dollars of revenue. <bookmark mark='c'/> Higher prices "
             f"brought back {T['price'] / 1e3:.1f} billion of it. Revenue fell three per cent while volume fell ten.",
             base=[packs, rows.axis, src], steps=[vol, rows[0], rows[1]], after=fade)

    def margin(self):
        T = R["tobacco"]
        c = stat_cards([(f"{T['margin']:.0f}%", "operating margin on cigarettes and cigars, after excise taxes, 2025", GOOD),
                        (f"{T['discount']:.1f}%", "of America's cigarettes sold as discount brands, up 2.2 points", BAD)],
                       y=0.8, size=44, span=12)
        q = quote(["'In 1998, PM USA and certain other tobacco product manufacturers entered into the MSA with 46 states,",
                   "the District of Columbia and certain United States territories to settle asserted and unasserted",
                   "health care cost recovery and other claims.'"], "Altria Group, Form 10-K 2025", size=14, width=11.5).move_to([0, -1.6, 0])
        src = source("Altria Group, Inc., Form 10-K 2025", size=12)
        beat(self,
             "And it keeps most of what it charges. <bookmark mark='a'/> Altria's cigarette and cigar business made an "
             f"operating profit of {T['margin']:.0f} cents on every dollar of revenue after excise taxes. "
             f"<bookmark mark='b'/> The threat is not a rival brand so much as cheaper ones: discount cigarettes rose to "
             f"{T['discount']:.0f} per cent of the market. <bookmark mark='c'/> And law shapes the business: under the "
             "settlements of 1997 and 1998 with the states, the makers pay substantial sums every year, and an FDA rule places "
             "a wide range of restrictions on how cigarettes may be advertised and promoted. A newcomer would find it hard to "
             "be noticed at all.",
             base=[src], steps=[c[0], c[1], q])

    def smokefree(self):
        E = R["extra"]
        sf = E["pm_sf"]
        tot = {2023: 35174, 2024: 37878, 2025: 40648}
        items = [(str(y), sf[y] / 1e3, GOOD, f"${sf[y] / 1e3:.1f}bn ({100 * sf[y] / tot[y]:.0f}%)") for y in (2023, 2024, 2025)]
        bars_ = vbars(items, base_y=-2.2, height=3.4, width=1.4, gap=0.9, x0=-5.2, size=14)
        lab = tx("Philip Morris International: smoke-free revenue (share of all its revenue)", 16, GREY_A).to_edge(UP, buff=0.9)
        t = VGroup(tx("heated tobacco (IQOS), nicotine pouches (ZYN), vapour (VEEV)", 16, WHITE),
                   tx(f"on sale in {E['pm_markets']} markets at the end of 2025", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        t.move_to([1.0, 0.6, 0], aligned_edge=LEFT)
        src = source("Philip Morris International Inc., Form 10-K 2025: net revenues by product category", size=12)
        beat(self,
             "Philip Morris International, which sells Marlboro outside the United States, is moving to new products. <bookmark mark='a'/> Its "
             f"smoke-free products, heated tobacco, nicotine pouches and vapour, brought in {sf[2023] / 1e3:.1f} billion "
             f"dollars in 2023 <bookmark mark='b'/> and {sf[2025] / 1e3:.1f} billion in 2025, {100 * sf[2025] / tot[2025]:.0f} "
             f"per cent of all its revenue, on sale in {E['pm_markets']} markets. The same playbook, a known name and a habit, "
             "carried to a new product before the old one fades. Whether those products are better for the people who use "
             "them is a question for health researchers and regulators, not for this film's accounts.",
             base=[lab, src], steps=[VGroup(bars_[0], t), VGroup(bars_[1], bars_[2])])

    def brand(self):
        T = R["tobacco"]
        pie = VGroup()
        ang = T["share"] / 100 * TAU
        a = AnnularSector(inner_radius=0.8, outer_radius=1.6, angle=ang, start_angle=PI / 2, color=BAD, fill_opacity=0.9).move_to([-3.4, 0.2, 0])
        b = AnnularSector(inner_radius=0.8, outer_radius=1.6, angle=TAU - ang, start_angle=PI / 2 + ang, color=GREY_B, fill_opacity=0.3)
        b.move_arc_center_to(a.get_arc_center())
        pie.add(a, b)
        lab = VGroup(tx(f"{T['share']}%", 28, BAD, bold=True), tx("Marlboro", 15, BAD)).arrange(DOWN, buff=0.05).move_to(a.get_arc_center())
        q = VGroup(tx("'Marlboro ... has been the largest-selling", 17, WHITE), tx("cigarette brand in the United States", 17, WHITE),
                   tx("for over 50 years.'", 17, WHITE), tx("Altria Group, Form 10-K 2025", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.8, 0.6, 0])
        src = source("Altria Group, Inc., Form 10-K 2025: retail share", size=12)
        beat(self,
             "And the leading brand stays the leading brand. <bookmark mark='a'/> Marlboro alone had "
             f"{T['share']} per cent of America's cigarette sales in 2025. <bookmark mark='b'/> Altria's report says it has "
             "been the country's best-selling cigarette for over fifty years. A brand that leads for half a century is the "
             "extreme case of this film's question: once the premium is established, it is very hard to take away.",
             base=[src], steps=[[pie, lab], q])
