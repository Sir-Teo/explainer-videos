from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class System(VoiceoverScene):
    def construct(self):
        card(self, 5, "The system", "What does the franchisor sell besides a name?",
             "Chapter five. The system. A franchise sells a way of running a restaurant, and some franchisors sell the food "
             "too.", lit=("make", "moat"))
        self.dough()
        self.digital()
        self.loyalty()
        self.drive()

    def dough(self):
        Sy = R["system"]
        items = [("supply chain: dough and supplies sold to its stores", Sy["supply"], MASTER, f"${Sy['supply']:.2f}bn"),
                 ("U.S. franchise royalties and fees", Sy["dpz_royal"], FR, f"${Sy['dpz_royal']:.2f}bn")]
        rows = hbars(items, max_value=3.2, x0=1.4, top=1.2, row=1.3, length=5.0, size=17, bar_h=0.65)
        hd = tx("Domino's revenue in 2025, two of its lines", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        note = tx(f"supply chain income ${Sy['scinc'] * 1e3:.0f}m: about {100 * Sy['scinc'] / Sy['supply']:.0f} cents on each dollar of supplies", 17, GREY_B).move_to([0, -1.6, 0])
        pz = draw.pallet(1.4).move_to([-5.2, -2.2, 0])
        src = source("Domino's Pizza, Form 10-K for 2025", size=12)
        beat(self,
             "Domino's makes the dough. It runs 22 regional dough centres in America that make dough and deliver food and other "
             f"supplies to substantially all its American stores. <bookmark mark='a'/> In 2025 that supply business sold "
             f"{Sy['supply']:.1f} billion dollars, {100 * Sy['supply'] / Sy['dpz_rev']:.0f} per cent of Domino's revenue. "
             f"<bookmark mark='b'/> Royalties and fees from its American franchisees were only {Sy['dpz_royal'] * 1e3:.0f} million. "
             f"<bookmark mark='c'/> The supply business earned about {100 * Sy['scinc'] / Sy['supply']:.0f} cents on the dollar: "
             "a wholesaler's margin from Part 33, on a captive customer base, with the pizza made the same everywhere.",
             base=[rows.axis, hd, pz, src], steps=[rows[0], rows[1], note])

    def digital(self):
        Sy = R["system"]
        ph = draw.phone(2.2, screen=FR).move_to([-4.2, 0.3, 0])
        c = stat_cards([(f"{Sy['digital']:.1f}%", "of Wingstop's system sales came through digital orders, late 2025", FR),
                        (f"{Sy['delivery'] / 1e3:.0f}k", "McDonald's restaurants that deliver, about 90% of them", APPS)], y=0.4, size=36, span=8)
        c.shift(RIGHT * 2.0)
        src = source("Wingstop and McDonald's, Forms 10-K for 2025", size=12)
        beat(self,
             "The system is increasingly software. <bookmark mark='a'/> Almost three-quarters of what Wingstop's "
             "restaurants sold at the end of 2025 was ordered on a phone or a website. <bookmark mark='b'/> McDonald's "
             f"offered delivery from nearly {Sy['delivery'] / 1e3:.0f} thousand restaurants. A franchisee cannot build an app, "
             "a loyalty programme or a delivery partnership alone; the franchisor can, once, for everyone, and that is part "
             "of what the royalty buys.",
             base=[ph, src], steps=[c[0], c[1]])

    def drive(self):
        rs = draw.restaurant(5.0).move_to([0, 0.6, 0])
        cars = VGroup(*[draw.car(0.9, color=c) for c in (OP, FR, GOOD, APPS)]).arrange(RIGHT, buff=0.25).move_to([0.5, -1.3, 0])
        g = VGroup(tx("the system decides", 19, WHITE, bold=True),
                   tx("the menu, the recipes and the kitchen layout", 16, GREY_A),
                   tx("the approved suppliers", 16, GREY_A),
                   tx("the training, the uniforms and the opening hours", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -2.2, 0])
        tag = estimate_tag("this series' summary", size=12)
        beat(self,
             "And the system is a set of rules. <bookmark mark='a'/> A franchisee follows the franchisor's menu, recipes, "
             "kitchen layout and suppliers, which is what makes a meal taste the same in every town, <bookmark mark='b'/> "
             "and what keeps a drive-through queue moving. <bookmark mark='c'/> In this series' reading, the rules are the "
             "product: a customer trusts a sign on a strange road because the system makes the restaurant behind it "
             "predictable, and every franchisee pays for that trust and benefits from it.",
             base=[tag], steps=[rs, cars, g])

    def loyalty(self):
        c = stat_cards([(f"${get('md34.loyalty'):.0f}bn", "McDonald's target for a year's sales to loyalty members, by 2027", FR),
                        ("250m", "its target for 90-day active loyalty users", FR),
                        ("70", "markets with its loyalty programme", OP)], y=0.6, size=36, span=12)
        ph = VGroup(*[draw.phone(1.2, screen=FR) for _ in range(5)]).arrange(RIGHT, buff=0.5).move_to([0, -1.9, 0])
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "The newest part of the system is data. <bookmark mark='a'/> McDonald's plans to sell 45 billion dollars a "
             "year to members of its loyalty programme by the end of 2027, <bookmark mark='b'/> and to have 250 million "
             "people using it every three months, <bookmark mark='c'/> across the seventy markets where it runs one. The "
             "app knows what each customer buys and can send an offer to bring them back; no single franchisee could own "
             "that relationship, which binds the franchisees more tightly to the brand.",
             base=[ph, src], steps=[c[0], c[1], c[2]])
