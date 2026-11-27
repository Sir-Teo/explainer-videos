from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Unit(VoiceoverScene):
    def construct(self):
        card(self, 2, "A mile, a hundredweight, a parcel", "What does it cost to move one thing one mile?",
             "Chapter two. A mile, a hundredweight, a parcel. Freight comes in four sizes, and each is sold by its own "
             "unit: a train by the ton-mile, a truck by the mile, a part load by the hundred pounds, a parcel by the piece.",
             lit=("unit",))
        self.ladder()
        self.container()
        self.part()
        self.piece()

    def ladder(self):
        Un = R["unit"]
        tr = draw.train(3, 0.7, kinds=("hopper",), colors=("#B58CFF",)).move_to([-4.7, 1.6, 0])
        s = draw.semi(1.8, cab_color=TRUCK).move_to([-1.3, 1.6, 0])
        t = draw.truck(1.4, color=LTL).move_to([1.6, 1.6, 0])
        p = draw.parcel(0.8).move_to([4.6, 1.6, 0])
        labs = VGroup(*[VGroup(tx(a, 26, c, bold=True), tx(b, 14, GREY_A)).arrange(DOWN, buff=0.08).next_to(obj, DOWN, buff=0.4)
                        for obj, a, b, c in ((tr, f"{Un['rail_tm']:.1f}c", "a ton carried a mile by rail", RAIL),
                                             (s, f"${Un['tl_mile']:.2f}", "a loaded mile, a whole truck", TRUCK),
                                             (t, f"${Un['ltl_cwt']:.2f}", "a hundred pounds, part of a truck", LTL),
                                             (p, f"${Un['ups']:.2f}", "a parcel in America", PARCEL))])
        src = source("Forms 10-K for 2025 of Union Pacific, J.B. Hunt, Old Dominion and UPS", size=12)
        beat(self,
             "Four ways to sell moving things. <bookmark mark='a'/> Union Pacific earned "
             f"{Un['rail_tm']:.1f} cents for each ton it carried a mile in 2025. <bookmark mark='b'/> J.B. Hunt's trucks "
             f"earned {Un['tl_mile']:.2f} dollars for each mile with a full trailer. <bookmark mark='c'/> Old Dominion, "
             "which carries loads too small to fill a truck, earned "
             f"{Un['ltl_cwt']:.2f} for every hundred pounds. <bookmark mark='d'/> And UPS earned {Un['ups']:.2f} for each "
             "parcel it delivered in America. Each unit fits its business, and the businesses are very different.",
             base=[src], steps=[VGroup(tr, labs[0]), VGroup(s, labs[1]), VGroup(t, labs[2]), VGroup(p, labs[3])])

    def container(self):
        Un = R["unit"]
        tr = draw.train(3, 1.0, kinds=("well",), colors=("#E8554E",)).move_to([-3.2, 1.5, 0])
        s = draw.semi(2.4, cab_color=TRUCK).move_to([3.2, 1.5, 0])
        items = [("intermodal: a container by train, with a truck at each end", Un["int_mile"], RAIL, f"${Un['int_mile']:.2f}"),
                 ("truckload: a trailer by road, door to door", Un["tl_mile"], TRUCK, f"${Un['tl_mile']:.2f}")]
        rows = hbars(items, max_value=3.2, x0=0.6, top=-0.4, row=0.9, length=5.0, size=16, bar_h=0.45)
        hauls = tx(f"average haul: {Un['int_haul']:,.0f} miles by intermodal, {Un['tl_haul']:,.0f} by truckload", 17, GREY_A).to_edge(DOWN, buff=0.9)
        lab = tx("J.B. Hunt, 2025: revenue per mile of a load", 17, GREY_A).to_edge(UP, buff=0.6)
        src = source("J.B. Hunt Transport Services, Form 10-K for 2025 (revenue per load over average length of haul)", size=12)
        beat(self,
             "The same box can go two ways. J.B. Hunt sells both, so its numbers compare like with like. "
             f"<bookmark mark='a'/> A container on a train, with a truck to collect it and another to deliver it, earned "
             f"about {Un['int_mile']:.2f} dollars a mile in 2025. <bookmark mark='b'/> A trailer pulled the whole way by a "
             f"truck, {Un['tl_mile']:.2f}. <bookmark mark='c'/> The train is cheaper by about two-fifths a mile, but slower, "
             f"and the trucks at each end cost the same however far it goes. So rail wins the long hauls, "
             f"{Un['int_haul']:,.0f} miles on average, and the truck the shorter ones, {Un['tl_haul']:,.0f}.",
             base=[lab, src, rows.axis], steps=[VGroup(tr, rows[0]), VGroup(s, rows[1]), hauls])

    def part(self):
        Un = R["unit"]
        t = draw.truck(2.6, color=LTL).move_to([-3.6, 1.0, 0])
        boxes = VGroup(*[draw.parcel(0.42, color=c) for c in ("#C89F6A", "#B58CFF", "#7BD88F", "#7EC8F5", "#F6C453", "#E8554E")]
                       ).arrange(RIGHT, buff=0.08).next_to(t, UP, buff=0.3)
        c = stat_cards([(f"{Un['ltl_wps']:,.0f} lb", "an average shipment", LTL), (f"{Un['ltl_haul']:,.0f} miles", "carried this far", ALL),
                        (f"${Un['ltl_rps']:,.0f}", "paid for it", GOOD)], y=-1.8, size=34, span=12)
        src = source("Old Dominion Freight Line, Form 10-K for 2025", size=12)
        beat(self,
             "Between the full truck and the parcel is the part load, too big for a parcel company and too small to fill "
             f"a trailer. <bookmark mark='a'/> Old Dominion's average shipment in 2025 weighed {Un['ltl_wps']:,.0f} pounds: "
             f"a few pallets. <bookmark mark='b'/> It travelled {Un['ltl_haul']:,.0f} miles <bookmark mark='c'/> and paid "
             f"about {Un['ltl_rps']:,.0f} dollars. Several customers share each trailer, so somebody has to collect the "
             "pallets, sort them and load them in the right order, and that takes buildings. Chapter five comes back to them.",
             base=[src], steps=[VGroup(t, boxes), c[0], VGroup(c[1], c[2])])

    def piece(self):
        Un = R["unit"]
        items = [("FedEx, US ground (fiscal 2026)", Un["fdx"], PARCEL, f"${Un['fdx']:.2f}"),
                 ("UPS, US domestic (2025)", Un["ups"], PARCEL, f"${Un['ups']:.2f}"),
                 ("US Postal Service, shipping and packages (fiscal 2025)", Un["usps"], SKY, f"${Un['usps']:.2f}")]
        rows = hbars(items, max_value=15, x0=0.8, top=1.2, row=1.0, length=5.6, size=16, bar_h=0.5)
        lab = tx("revenue per package", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Forms 10-K of FedEx (fiscal 2026) and UPS (2025); the Postal Service's report on Form 10-K for fiscal 2025 (revenue over pieces)", size=12)
        beat(self,
             f"And the parcel. <bookmark mark='a'/> FedEx earned {Un['fdx']:.2f} dollars for a ground package in America, "
             f"<bookmark mark='b'/> UPS {Un['ups']:.2f} for a domestic one. <bookmark mark='c'/> The Postal Service took about "
             f"{Un['usps']:.2f} a piece for its shipping and packages, a mix that runs from Priority Mail to Ground "
             "Advantage and Parcel Select. A "
             "parcel's price depends on its weight and speed, but most of its cost, as chapter seven shows, is in the last "
             "few hundred yards.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2]])
