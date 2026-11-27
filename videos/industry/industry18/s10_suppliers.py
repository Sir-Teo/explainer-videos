from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403


class Suppliers(VoiceoverScene):
    def construct(self):
        card(self, 8, "The suppliers", "Who in the chain makes the money?",
             "Chapter eight. The suppliers. Two airframers and two or three engine makers sit on top of a long chain of "
             "companies. Who in that chain makes the money?", lit=("dollar", "moat"))
        self.margins()
        self.tdg()
        self.spirit()

    def margins(self):
        S = R["suppliers"]
        m = S["margins"]
        ser = {"TransDigm": ({y: 100 * v for y, v in m["TDG"].items() if y <= 2025}, SUPPLIER),
               "HEICO": ({y: 100 * v for y, v in m["HEI"].items()}, PRICE),
               "Boeing": ({y: 100 * v for y, v in m["BA"].items()}, BOEING),
               "Spirit AeroSystems": ({y: 100 * v for y, v in m["SPR"].items()}, BAD)}
        ch = line_chart(ser, x=(2015, 2025), y=(-35, 30), xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                        yticks=[-30, -20, -10, 0, 10, 20, 30], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="net income as a share of revenue, by fiscal year", width=9.2, height=4.6, center=(-1.0, -0.45),
                        nudge={"HEICO": -0.15, "TransDigm": 0.15})
        zero = DashedLine(ch.ax.c2p(2015, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        avg = S["avg"]
        note = tx(f"averages 2015-2025: TransDigm {100 * avg['TDG']:.1f}%, HEICO {100 * avg['HEI']:.1f}%, Boeing "
                  f"{100 * avg['BA']:.1f}%, Spirit {100 * avg['SPR']:.1f}% (to 2024)", 14, GREY_A).to_edge(DOWN, buff=0.7)
        src = source("Forms 10-K of TransDigm Group, HEICO, The Boeing Company and Spirit AeroSystems (to 2024), via SEC "
                     "company facts", size=12)
        beat(self,
             "Here are the profit margins of four companies in the chain since 2015. <bookmark mark='a'/> Boeing's "
             "swung from ten per cent to losses. <bookmark mark='b'/> Spirit AeroSystems, which built Boeing's 737 "
             "fuselages, did worse: from 2020 it lost money every year, a third of its revenue in 2024. "
             "<bookmark mark='c'/> Now two parts makers. TransDigm kept a margin near twenty per cent through the "
             "grounding and the pandemic, <bookmark mark='d'/> and HEICO near fifteen. <bookmark mark='e'/> The "
             "companies that build the aircraft struggled. Some of the companies that sell small parts for them barely "
             "noticed.",
             base=[ch.frame, zero, src],
             steps=[[ch.lines["Boeing"], ch.labels["Boeing"]], [ch.lines["Spirit AeroSystems"], ch.labels["Spirit AeroSystems"]],
                    [ch.lines["TransDigm"], ch.labels["TransDigm"]], [ch.lines["HEICO"], ch.labels["HEICO"]], note])

    def tdg(self):
        S = R["suppliers"]
        prop, after = S["tdg"]
        plane = draw.plane(5.0, "#3A4152").move_to([-3.2, 1.4, 0])
        parts = VGroup(*[Dot([-5.2 + 0.36 * (i % 12), 0.15 - 0.22 * (i // 12), 0], radius=0.06, color=GREY_B) for i in range(36)])
        star = VGroup(*[Dot(parts[i].get_center(), radius=0.08, color=SUPPLIER) for i in (3, 14, 22, 31)])
        pl = tx("a pump, a valve, an actuator: thousands of small parts", 14, GREY_A).next_to(parts, DOWN, buff=0.15).align_to(parts, LEFT)
        c = VGroup(VGroup(tx(f"{prop:.0f}%", 44, SUPPLIER, bold=True),
                          tx("of TransDigm's sales: its own proprietary products", 16, GREY_A)).arrange(DOWN, buff=0.08),
                   VGroup(tx(f"{after:.0f}%", 44, PRICE, bold=True),
                          tx("from the aftermarket: parts for aircraft in service", 16, GREY_A)).arrange(DOWN, buff=0.08)
                   ).arrange(DOWN, buff=0.35).move_to([3.4, 1.4, 0])
        q = quote(["'we generate net sales from aftermarket consumption over the life of", "that aircraft, which is generally "
                   "estimated at 25 to 30 years'"], "TransDigm Group, Form 10-K fiscal 2026", size=14, width=6.0).move_to([3.4, -0.9, 0])
        sole = quote(["'Many major components and product equipment items are procured or subcontracted",
                      "on a sole-source basis'"], "The Boeing Company, Form 10-K 2025", size=14, width=8).to_edge(DOWN, buff=0.7)
        src = source("TransDigm Group, Form 10-K fiscal 2026; The Boeing Company, Form 10-K 2025", size=12)
        beat(self,
             "Why the difference? <bookmark mark='a'/> An airliner holds thousands of small parts: pumps, valves, "
             "actuators, ignition systems. <bookmark mark='b'/> Many are designed by one supplier and certified with the aircraft, so for "
             "that aircraft's whole life there is one approved source. <bookmark mark='c'/> TransDigm's annual report "
             f"says about {prop:.0f} per cent of its sales are its own proprietary products, and about {after:.0f} per "
             "cent come from the aftermarket: replacement parts, over the twenty-five to thirty year life of an aircraft. "
             "<bookmark mark='d'/> Boeing's own report says many major components are bought from a single source. A "
             "single approved source of a part the airline must replace is a business with very few competitors, and "
             "TransDigm says it buys such businesses to earn what it calls private equity-like returns.",
             base=[plane, src], steps=[[parts, pl], star, [c, q], sole])

    def spirit(self):
        M = R["making"]
        left = VGroup(tx("Spirit AeroSystems", 22, BAD, bold=True),
                      tx("built the 737's fuselage and big parts of the 767, 777 and 787", 15, WHITE),
                      tx("its biggest customers: Boeing and Airbus", 15, WHITE),
                      tx(f"bought by Boeing, December 2025: ${M['spirit'] / 1e3:.1f}bn", 15, BOEING, bold=True)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.2, 1.2, 0])
        right = VGroup(tx("Airbus took the plants building its parts", 18, AIRBUS, bold=True),
                       tx(f"and booked a EUR {M['ab_spirit']:,}m charge", 18, AIRBUS, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, 1.4, 0])
        q = quote(["'the shift from contractual pricing ('buy') to the underlying internal production costs ('make')",
                   "resulted in an increase in the projected costs for these programmes'"], "Airbus SE, Annual Report 2025",
                  size=15, width=11.5).move_to([0, -1.0, 0])
        moral = tx("Airbus had been paying less for the parts than they cost to make.", 18, PRICE, bold=True).to_edge(DOWN, buff=0.8)
        src = source("The Boeing Company, Form 10-K 2025; Airbus SE, Annual Report 2025 (Note 8)", size=12)
        beat(self,
             "And the companies that build big structures? <bookmark mark='a'/> Spirit AeroSystems built the 737's "
             "fuselage and large parts of Boeing's twin-aisle jets, and parts for Airbus. After five years of losses, its "
             "two biggest customers split it between them. <bookmark mark='b'/> Airbus "
             f"took the plants making its parts and booked a charge of {M['ab_spirit']:,} million euros, "
             "<bookmark mark='c'/> because, in its own words, moving from the contract price it had paid to the real cost "
             "of making the parts raised its projected costs. <bookmark mark='d'/> In plain language, Airbus had been "
             "buying those parts for less than they cost to make. A supplier with two customers and no parts of its own has "
             "little to bargain with. One that owns a part the airlines must keep buying has a great deal.",
             base=[src], steps=[left, right, q, moral])
