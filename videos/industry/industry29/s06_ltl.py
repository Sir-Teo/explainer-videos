from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Ltl(VoiceoverScene):
    def construct(self):
        card(self, 5, "Less than a truckload", "Why does a network of buildings change the business?",
             "Chapter five. Less than a truckload. Carry a few pallets for many customers, and you need buildings to sort "
             "them in, and the buildings change everything.", lit=("make", "moat"))
        self.network()
        self.price()
        self.old()
        self.margins()

    def network(self):
        L = R["ltl"]
        pts = [np.array(p) for p in ([-5.2, 1.6, 0], [-5.6, 0.2, 0], [-4.8, -1.2, 0], [5.2, 1.6, 0], [5.6, 0.2, 0], [4.8, -1.2, 0])]
        a, b = np.array([-2.6, 0.2, 0]), np.array([2.6, 0.2, 0])
        sc = VGroup(*[VGroup(draw.warehouse(1.4).move_to(p), tx("service center", 13, LTL).next_to(p, DOWN, buff=0.55))
                      for p in (a, b)])
        shippers = VGroup(*[VGroup(Dot(p, radius=0.08, color=WHITE), draw.parcel(0.3).next_to(p, UP, buff=0.05)) for p in pts])
        pick = VGroup(*[Line(pts[i], a, stroke_color=GREY_B, stroke_width=2) for i in range(3)])
        drop = VGroup(*[Line(b, pts[i], stroke_color=GREY_B, stroke_width=2) for i in range(3, 6)])
        trunk = Arrow(a + RIGHT * 0.8, b + LEFT * 0.8, buff=0, color=LTL, stroke_width=7)
        tl = tx("one full trailer between the buildings", 15, LTL).next_to(trunk, UP, buff=0.15)
        c = stat_cards([(f"{L['sc']:.0f}", "Old Dominion's service centers", LTL), (f"{L['spd']:,.0f}", "shipments a day, 2025", ALL)],
                       y=-2.6, size=34, span=8)
        src = source("Old Dominion Freight Line, Form 10-K for 2025", size=12)
        beat(self,
             "Here is how a part load travels. <bookmark mark='a'/> Small trucks collect a few pallets each from many "
             "shippers and bring them to a service center, a long building with dozens of doors. <bookmark mark='b'/> "
             "There they are sorted and packed into full trailers bound for another service center, near where they are "
             "going, <bookmark mark='c'/> and delivered from there. Every shipment is handled several times, and the "
             f"network needs buildings everywhere. <bookmark mark='d'/> Old Dominion had {L['sc']:.0f} of them at the end "
             f"of 2025, handling {L['spd']:,.0f} shipments a day.",
             base=[src], steps=[VGroup(shippers[:3], pick, sc[0]), VGroup(trunk, tl, sc[1]), VGroup(shippers[3:], drop), c])

    def price(self):
        items = [("tons carried", -9.1, BAD, "-9.1%"), ("shipments", -7.8, BAD, "-7.8%"),
                 ("revenue a hundredweight", 3.9, GOOD, "+3.9%"), ("revenue a shipment", 2.4, GOOD, "+2.4%")]
        rows = hbars([(n, abs(v), c, t) for n, v, c, t in items], max_value=10, x0=0.6, top=1.6, row=0.85, length=5.0,
                     size=17, bar_h=0.45)
        lab = tx("Old Dominion, 2025 against 2024", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Old Dominion Freight Line, Form 10-K for 2025", size=12)
        beat(self,
             "Watch what that network allows in a bad year. <bookmark mark='a'/> In 2025 Old Dominion carried 9.1 per cent "
             "fewer tons <bookmark mark='b'/> and 7.8 per cent fewer shipments. <bookmark mark='c'/> Yet it was paid 3.9 "
             "per cent more for each hundred pounds, <bookmark mark='d'/> and 2.4 per cent more for each shipment. A "
             "In this series' reading, a truckload carrier in a falling market cuts its price to keep its trucks moving; a "
             "part-load network with few rivals can hold its price and carry less.",
             base=[rows.axis, lab, src], steps=[rows[0], rows[1], rows[2], rows[3]])

    def old(self):
        L = R["ltl"]
        ch = line_chart({"Old Dominion": (L["odfl"], GOOD), "Yellow": (L["yell"], BAD)}, x=(2013, 2025), y=(65, 105),
                        xticks=[2013, 2016, 2019, 2022, 2025], yticks=[70, 80, 90, 100], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="operating ratio: costs per dollar of revenue (lower is better)", width=9.0, height=4.4,
                        center=(-1.2, -0.45))
        hund = DashedLine(ch.ax.c2p(2013, 100), ch.ax.c2p(2025, 100), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        end = tx("Chapter 11, 6 August 2023", 15, BAD, bold=True).move_to(ch.ax.c2p(2022.6, 91.5))
        src = source("Forms 10-K via SEC company facts; Yellow Corporation, Forms 10-K for 2022 and 8-K of 7 August 2023", size=12)
        beat(self,
             "Two companies with the same kind of network. <bookmark mark='a'/> Old Dominion, 'a single integrated, "
             f"union-free organization' that opened a net 35 service centers in ten years, spent {L['odfl'][2016]:.0f} cents of each dollar in 2016 and "
             f"{L['odfl'][2022]:.0f} in 2022. <bookmark mark='b'/> Yellow, once one of the largest, spent "
             f"{L['yell'][2019]:.0f} or more in most years. <bookmark mark='c'/> On 6 August 2023 it filed for bankruptcy; "
             f"about {L['yell_emp']:,.0f} people had worked there at the end of 2022.",
             base=[ch.frame, hund, src], steps=[VGroup(ch.lines["Old Dominion"], ch.labels["Old Dominion"]),
                                                VGroup(ch.lines["Yellow"], ch.labels["Yellow"]), end])

    def margins(self):
        M = R["trucks"]["margins"]
        items = [(k, M[k][2025], LTL, f"{M[k][2025]:.1f}%") for k in ("Old Dominion", "Saia", "XPO")]
        items += [(k, M[k][2025], TRUCK, f"{M[k][2025]:.1f}%") for k in ("Knight-Swift", "Schneider", "Werner")]
        rows = hbars(items, max_value=28, x0=0.6, top=2.0, row=0.68, length=5.4, size=16, bar_h=0.38)
        lab = tx("operating profit per dollar of revenue, 2025: less than truckload against truckload", 16, GREY_A).to_edge(UP, buff=0.6)
        tag = estimate_tag("Forms 10-K via SEC company facts; the reading is this series'", size=12)
        beat(self,
             "And the result, in a soft year. <bookmark mark='a'/> The part-load carriers kept "
             f"{M['Old Dominion'][2025]:.0f}, {M['Saia'][2025]:.0f} and {M['XPO'][2025]:.0f} cents of each dollar in 2025. "
             f"<bookmark mark='b'/> The truckload carriers, {M['Knight-Swift'][2025]:.0f}, {M['Schneider'][2025]:.0f} and "
             f"{M['Werner'][2025]:.1f}. In this series' reading, the buildings are the moat: anyone can buy a truck, but "
             "hundreds of service centers near every city take many years to assemble.",
             base=[rows.axis, lab, tag], steps=[VGroup(*rows[:3]), VGroup(*rows[3:])])
