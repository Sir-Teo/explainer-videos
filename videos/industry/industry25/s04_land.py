from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Land(VoiceoverScene):
    def construct(self):
        card(self, 3, "Own the land, or control it", "What do the real builders choose?",
             "Chapter three. Own the land, or control it. Run it's choice is the central decision of the business, and "
             "the largest builders have all moved the same way.", lit=("moat", "change"))
        self.horton()
        self.lennar()
        self.years()
        self.forestar()
        self.nvr()
        self.walk()

    def horton(self):
        D = R["builder"]["dhi"]
        tot = D["owned"] + D["controlled"]
        bar = viz.bar_split([("owned", D["owned"], OWN), ("controlled", D["controlled"], OPTION)], tot, width=11.0, height=0.9).move_to([0, 0.6, 0])
        labs = VGroup(tx(f"owned {D['owned']:,.0f} ({100 * D['owned'] / tot:.0f}%)", 17, OWN, bold=True).next_to(bar[0], DOWN, buff=0.2),
                      tx(f"controlled through purchase contracts {D['controlled']:,.0f} ({100 * D['controlled'] / tot:.0f}%)", 17, OPTION, bold=True).next_to(bar[1], DOWN, buff=0.2))
        lots = VGroup(*[draw.plot_lot(0.6) for _ in range(8)]).arrange(RIGHT, buff=0.2).move_to([0, 2.3, 0])
        src = source("D.R. Horton, Inc., Form 8-K of 29 October 2026: land and lot position", size=12)
        beat(self,
             f"D.R. Horton had {tot:,.0f} lots owned or controlled in September 2026: enough for about seven years of its "
             f"sales. <bookmark mark='a'/> It owned {D['owned']:,.0f} of them, {100 * D['owned'] / tot:.0f} per cent. "
             f"<bookmark mark='b'/> The other {D['controlled']:,.0f}, {100 * D['controlled'] / tot:.0f} per cent, it "
             "controlled through contracts to buy them later, many from Forestar, a lot developer it majority owns. A year "
             f"earlier the owned share was {100 * D['owned25'] / (D['owned25'] + D['controlled25']):.0f} per cent.",
             base=[lots, src], steps=[[bar[0], labs[0]], [bar[1], labs[1]]])

    def lennar(self):
        L = R["builder"]["len"]
        items = [("30 November 2024", L["controlled"][0], GREY_B, f"{L['controlled'][0]:.0f}%"),
                 ("30 November 2025", L["controlled"][1], OPTION, f"{L['controlled'][1]:.0f}%")]
        rows = hbars(items, max_value=100, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx("Lennar: share of its homesites controlled through options rather than owned", 16, GREY_A).move_to([0, 2.1, 0])
        q = tx("'Land-light strategy'", 20, PRICE, bold=True).move_to([0, -1.6, 0])
        src = source("Lennar Corporation, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "Lennar went further. <bookmark mark='a'/> At the end of fiscal 2024, "
             f"{L['controlled'][0]:.0f} per cent of its homesites were controlled through options rather than owned. "
             f"<bookmark mark='b'/> A year later, {L['controlled'][1]:.0f} per cent, mostly through land banks: investors who "
             "buy and hold the land and sell it to Lennar lot by lot as it builds. In February 2025 it spun off much of its "
             "own land into a separate listed company, Millrose, to do exactly that. <bookmark mark='c'/> It calls this "
             "its 'land-light strategy'.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], q])

    def nvr(self):
        N = R["builder"]["nvr"]
        q = quote(["'We generally do not engage in land development ... Instead, we typically acquire finished building",
                   "lots from various third-party land developers pursuant to fixed price lot purchase agreements (LPAs)",
                   "that require deposits that may be forfeited'"], "NVR, Inc., Form 10-K for 2025", size=17).move_to([0, 1.7, 0])
        c = stat_cards([(f"{N['lots']:,.0f}", "lots controlled under purchase agreements, end of 2025", OPTION),
                        (f"${N['deposits']:,.0f}m", "of cash deposits on them", PRICE),
                        (f"${N['per_lot']:.1f}k", "deposit per lot, on average", GOOD)], y=-0.8, size=36, span=12)
        src = source("NVR, Inc., Form 10-K for 2025", size=12)
        beat(self,
             "And one builder has done it for decades. <bookmark mark='a'/> NVR, whose homes are sold under brands such "
             "as Ryan Homes, says it generally does not develop land at all: it buys finished lots from developers under "
             "fixed-price agreements, with deposits it can forfeit. <bookmark mark='b'/> At the end of 2025 it controlled "
             f"{N['lots']:,.0f} lots that way, <bookmark mark='c'/> backed by {N['deposits']:,.0f} million dollars of cash "
             f"deposits: <bookmark mark='d'/> about {N['per_lot']:.1f} thousand dollars a lot. Its median profit margin "
             "over the last five years has been among the highest of the large builders.",
             base=[src], steps=[q, c[0], c[1], c[2]])

    def walk(self):
        L = R["builder"]["len"]
        lots = VGroup(*[draw.plot_lot(0.5) for _ in range(12)]).arrange_in_grid(rows=2, buff=0.2).move_to([-3.2, 0.6, 0])
        cross = VGroup(*[Line(l.get_corner(UL), l.get_corner(DR), stroke_color=BAD, stroke_width=3) for l in lots[:5]])
        c = stat_cards([(f"{L['walked']:,.0f}", "controlled homesites Lennar walked away from in fiscal 2025", BAD),
                        (f"${L['writeoff']:.1f}m", "of deposits it wrote off", PRICE)], y=0.6, size=38, span=6.0)
        c.shift(RIGHT * 3.2)
        src = source("Lennar Corporation, Form 10-K for fiscal 2025", size=12)
        beat(self,
             "And the option was used. <bookmark mark='a'/> In fiscal 2025 Lennar walked away from "
             f"{L['walked']:,.0f} homesites it had controlled, <bookmark mark='b'/> and wrote off "
             f"{L['writeoff']:.1f} million dollars of deposits: about {1e3 * L['writeoff'] / L['walked']:.1f} thousand "
             "dollars a lot, a small price for land it no longer wanted. That is Run it's bust case, in a real annual "
             "report.",
             base=[lots, src], steps=[[c[0], cross], c[1]])

    def years(self):
        D = R["builder"]["dhi"]
        own_y = D["owned"] / D["closed"]
        tot_y = (D["owned"] + D["controlled"]) / D["closed"]
        items = [("lots owned", own_y, OWN, f"{own_y:.1f} years"), ("lots owned or controlled", tot_y, OPTION, f"{tot_y:.1f} years")]
        rows = hbars(items, max_value=8, x0=-0.2, top=1.0, row=1.1, length=6.0, size=18, bar_h=0.55)
        lab = tx("D.R. Horton's lots, in years of its fiscal 2026 closings", 16, GREY_A).move_to([0, 2.1, 0])
        tag = estimate_tag("this series' arithmetic: lots over homes closed in fiscal 2026", size=12)
        src = source("D.R. Horton, Inc., Form 8-K of 29 October 2026", size=12)
        beat(self,
             "Measured in years of building, the difference is plain. <bookmark mark='a'/> The lots D.R. Horton owns would "
             f"last about {own_y:.1f} years at its current pace. <bookmark mark='b'/> With the lots it controls by "
             f"contract, about {tot_y:.1f} years. It owns what it needs for the next year or two, and holds the rest of "
             "its future as options, the Run it answer for a world in which nobody knows the rate three years out.",
             base=[rows.axis, lab, tag, src], steps=[rows[0], rows[1]])

    def forestar(self):
        lots = VGroup(*[draw.plot_lot(0.55) for _ in range(10)]).arrange(RIGHT, buff=0.15).move_to([0, 2.2, 0])
        c = stat_cards([(f"{get('dhi.forestar'):,.0f}", "lots owned or controlled by Forestar, D.R. Horton's majority-owned lot developer", LAND),
                        (f"{get('dhi.third'):.0f}%", "of its fiscal 2026 homes built on lots developed by Forestar or by others", OPTION)],
                       y=0.2, size=40, span=11)
        src = source("D.R. Horton, Inc., Form 8-K of 29 October 2026 and Form 10-K for fiscal 2026", size=12)
        beat(self,
             "D.R. Horton also split the business in two. <bookmark mark='a'/> Forestar, a separately listed company it "
             "majority owns, buys raw land and turns it into finished lots, roads and pipes included: it owned or "
             f"controlled {get('dhi.forestar'):,.0f} lots in September 2026. <bookmark mark='b'/> And {get('dhi.third'):.0f} "
             "per cent of the homes D.R. Horton "
             "closed in fiscal 2026 stood on lots developed by Forestar or by other developers, up from 65 per cent a year "
             "before. The builder builds; someone else does the slow, risky work of turning fields into lots.",
             base=[lots, src], steps=[c[0], c[1]])
