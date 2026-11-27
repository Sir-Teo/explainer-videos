from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Price(VoiceoverScene):
    def construct(self):
        card(self, 8, "The price, and Medicare's turn", "Who sets the price of a protected medicine?",
             "Chapter eight. The price. Who sets the price of a medicine that only one company may sell?", lit=("dollar", "change"))
        self.who()
        self.cms()
        self.timeline()

    def timeline(self):
        pa = viz.plot_axes([2023.95, 2026.15], [0, 1], x_length=12.0, y_length=1.2, xticks=[2024, 2025, 2026],
                           xfmt=lambda v: f"{int(v)}", grid=False, size=14).move_to([0, 0.4, 0])
        ax = pa.ax
        evs = [(2024.08, "1 Feb 2024: CMS's first offers", GOV, UP), (2024.17, "by 2 Mar: counteroffers", GREY_A, DOWN),
               (2024.53, "15 Jul: final offers", GOV, UP), (2024.58, "1 Aug: all ten agreed", GOOD, DOWN),
               (2026.0, "1 Jan 2026: in force", PRICE, UP)]
        ms = [marker(ax, x, 0.5, lab, col, side=side, size=13) for x, lab, col, side in evs]
        src = source("Centers for Medicare & Medicaid Services: key milestones for the first cycle of negotiations", size=12)
        beat(self,
             "The first negotiation ran for six months. <bookmark mark='a'/> Medicare sent its first offers on 1 "
             "February 2024, <bookmark mark='b'/> the companies answered with counteroffers within a month, "
             "<bookmark mark='c'/> and after three meetings for each drug, Medicare sent final offers in July for the "
             "five where no price had yet been agreed. "
             "<bookmark mark='d'/> By 1 August 2024 all ten prices were agreed, <bookmark mark='e'/> and they came into "
             "force on 1 January 2026, a year and a half later. A new buyer had learned to bargain, and the sellers now plan "
             "for it.",
             base=[pa, src], steps=ms)

    def who(self):
        steps_ = []
        nodes = [("the maker", BRAND, BRAND, -5.2), ("the wholesaler", GREY_B, GREY_B, -2.6), ("the pharmacy", GREY_B, GREY_B, 0.0),
                 ("the insurer and its benefit manager", GOV, GOV, 2.8), ("the patient", WHITE, LAB, 5.4)]
        g = VGroup()
        for name, col, pill, x in nodes:
            n = VGroup(draw.capsule(0.6, pill), tx(name, 14, col, bold=True)).arrange(DOWN, buff=0.1).move_to([x, 0.8, 0])
            if n.width > 2.4:
                n.scale_to_fit_width(2.4)
            g.add(n)
        arrows = VGroup(*[Arrow(g[i].get_right(), g[i + 1].get_left(), buff=0.12, stroke_width=3, color=GREY_B) for i in range(4)])
        rb = CurvedArrow(g[0].get_bottom() + DOWN * 0.2, g[3].get_bottom() + DOWN * 0.2, angle=PI / 4, color=PRICE)
        rbl = tx("rebates: discounts paid back to the insurer for a good place on its list", 15, PRICE, bold=True).move_to([0, -1.6, 0])
        lst = tx("the list price is what the maker asks; the net price is what it keeps after rebates", 16, WHITE).move_to([0, -2.4, 0])
        src = source("Illustration of the US channel; Part 51 follows it in detail", size=12)
        beat(self,
             "In America a medicine passes through several hands. <bookmark mark='a'/> The maker sells it to a "
             "wholesaler, <bookmark mark='b'/> who sells it to a pharmacy, <bookmark mark='c'/> which dispenses it to a "
             "patient whose insurer pays most of the bill, <bookmark mark='d'/> through a company that manages its drug "
             "benefits. <bookmark mark='e'/> Makers pay discounts, called rebates, back to insurers, often in return for "
             "a good place on the insurer's list of covered drugs. <bookmark mark='f'/> So there are two prices: the list price, which makes the headlines, and "
             "the net price the maker keeps. For a protected drug with no rival, there is little to discount.",
             base=[g[0], src], steps=[[arrows[0], g[1]], [arrows[1], g[2]], [arrows[2], g[3]], [arrows[3], g[4]], [rb, rbl], lst])

    def cms(self):
        M = R["medicare"]
        c = stat_cards([("10", "drugs in the first round of Medicare's negotiation", GOV),
                        (f"{M['users']:.1f}m", "people with Medicare used them in 2023", WHITE),
                        (f"${M['saving']:.0f}bn", f"saved had the prices applied in 2023: {M['pct']}% lower net spending", GOOD)],
                       y=0.6, size=40, span=12)
        when = tx("law: August 2022 (the Inflation Reduction Act); negotiated prices in force from 1 January 2026", 17, GREY_A).move_to([0, -1.6, 0])
        src = source("Centers for Medicare & Medicaid Services, fact sheet: negotiated prices for initial price applicability year 2026",
                     size=12)
        beat(self,
             "For most of its history Medicare, America's insurer for the elderly, was not allowed to negotiate the prices "
             "of the drugs it covers. In 2022 Congress changed that for a few high-spending drugs without generic or "
             "biosimilar competition. <bookmark mark='a'/> The first round covered ten drugs, "
             f"<bookmark mark='b'/> used by {M['users']:.1f} million people in 2023. <bookmark mark='c'/> Had the "
             f"negotiated prices applied that year, Medicare says, it would have spent {M['saving']:.0f} billion dollars "
             f"less, {M['pct']} per cent of its net spending on them. <bookmark mark='d'/> The prices took effect on 1 "
             "January 2026. Drug companies now plan for a negotiated Medicare price on their biggest sellers, years "
             "before their patents end.",
             base=[src], steps=[c[0], c[1], c[2], when])
