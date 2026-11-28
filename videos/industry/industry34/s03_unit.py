from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Unit(VoiceoverScene):
    def construct(self):
        card(self, 2, "One restaurant's dollar", "Where does the money go in a restaurant the company runs itself?",
             "Chapter two. One restaurant's dollar, in restaurants the companies run themselves, where they have to report "
             "every cost.", lit=("dollar", "make"))
        self.bars()
        self.prime()
        self.sitdown()
        self.auv()

    def bars(self):
        Un = R["unit"]
        rows = VGroup()
        for i, (n, col) in enumerate((("McDonald's company stores", FR), ("Chipotle", OP), ("Darden", FULL))):
            u = Un[n]
            bar = viz.bar_split([("food", u["food"], FOODC), ("labour", u["labour"], LABC), ("rent and the rest", u["occupancy"], OTHER),
                                 ("margin", u["margin"], GOOD)], 1.0, width=8.6, height=0.6).move_to([1.4, 1.4 - 1.35 * i, 0])
            nm = tx(n, 17, col, bold=True).next_to(bar, LEFT, buff=0.25)
            labs = VGroup(*[tx(f"{100 * v:.0f}c", 15, WHITE, bold=True).move_to(bar[j]) for j, v in
                            enumerate((u["food"], u["labour"], u["occupancy"], u["margin"]))])
            rows.add(VGroup(nm, bar, labs))
        key = VGroup(*[VGroup(Square(0.2, fill_color=c, fill_opacity=1, stroke_width=0), tx(t, 14, GREY_A)).arrange(RIGHT, buff=0.1)
                       for t, c in (("food", FOODC), ("labour", LABC), ("rent, utilities and other costs", OTHER), ("restaurant margin", GOOD))]
                     ).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.7)
        src = source("McDonald's and Chipotle, Forms 10-K for 2025; Darden, Form 10-K for fiscal 2026", size=12)
        mc = Un["McDonald's company stores"]
        beat(self,
             "<bookmark mark='a'/> At the restaurants McDonald's runs itself, food and paper took "
             f"{100 * mc['food']:.0f} cents of each dollar in 2025, the crew {100 * mc['labour']:.0f}, rent and everything else "
             f"{100 * mc['occupancy']:.0f}, leaving {100 * mc['margin']:.0f} cents. <bookmark mark='b'/> Chipotle, which runs its "
             f"restaurants itself, kept {100 * Un['Chipotle']['margin']:.0f} cents: its labour is lighter, its food much the same. "
             f"<bookmark mark='c'/> Darden, which runs Olive Garden and other sit-down chains, kept about "
             f"{100 * Un['Darden']['margin']:.0f} cents before marketing, depreciation and its head office, with labour the biggest "
             "cost of all. Food and labour together, which the trade calls prime cost, take between fifty-five and sixty-two "
             "cents in all three.",
             base=[key, src], steps=[rows[0], rows[1], rows[2]])

    def prime(self):
        Un = R["unit"]
        items = [(n, 100 * (u["food"] + u["labour"]), c, f"{100 * (u['food'] + u['labour']):.0f}c")
                 for n, u, c in ((n, Un[n], c) for n, c in (("McDonald's company stores", FR), ("Chipotle", OP), ("Darden", FULL)))]
        rows = hbars(items, max_value=70, x0=-0.2, top=1.2, row=1.1, length=6.4, size=18, bar_h=0.55)
        hd = tx("Prime cost: food plus labour, cents per dollar of sales", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        burgers = VGroup(*[draw.burger(0.7) for _ in range(5)]).arrange(RIGHT, buff=0.4).move_to([0, -2.1, 0])
        src = source("McDonald's, Chipotle and Darden, Forms 10-K", size=12)
        beat(self,
             "<bookmark mark='a'/> Prime cost at McDonald's company restaurants: "
             f"{items[0][1]:.0f} cents. <bookmark mark='b'/> At Chipotle, {items[1][1]:.0f}. <bookmark mark='c'/> At Darden, "
             f"{items[2][1]:.0f}. Every restaurant manager watches this number weekly: a few points of waste in the kitchen or "
             "an hour too many on the rota, and the margin is gone.",
             base=[rows.axis, hd, burgers, src], steps=[rows[0], rows[1], rows[2]])

    def auv(self):
        X = R["unit_extra"]
        c = stat_cards([(f"${X['auv'] / 1e6:.1f}m", "a franchised McDonald's in America, a year", FR),
                        (f"${X['cmg_ars']:.1f}m", "a Chipotle, a year", OP),
                        (f"${X['wing_auv']:.1f}m", "a Wingstop in America, a year", MASTER)], y=0.5, size=38, span=12)
        rs = VGroup(*[draw.restaurant(1.6) for _ in range(3)]).arrange(RIGHT, buff=0.8).move_to([0, -1.9, 0])
        src = source("McDonald's (franchised sales over franchised restaurants), Chipotle and Wingstop, Forms 10-K for 2025", size=12)
        beat(self,
             "And how much does one restaurant sell? <bookmark mark='a'/> A franchised McDonald's in America, about "
             f"{X['auv'] / 1e6:.1f} million dollars a year. <bookmark mark='b'/> A Chipotle, {X['cmg_ars']:.1f} million, down a "
             f"little in 2025. <bookmark mark='c'/> A Wingstop, {X['wing_auv']:.1f} million. "
             "The fixed costs of a restaurant, the manager, the rent, the equipment, are much the same whatever it "
             "sells, so a brand that can push more sales through each one wins twice.",
             base=[rs, src], steps=[c[0], c[1], c[2]])

    def sitdown(self):
        X = R["unit_extra"]
        dr = get("dr34.sales") * 1e3 / get("dr34.units")
        items = [("a Darden restaurant (Olive Garden and others)", dr, FULL, f"${dr:.1f}m"),
                 ("a franchised McDonald's in America", X["auv"] / 1e6, FR, f"${X['auv'] / 1e6:.1f}m"),
                 ("a Chipotle", X["cmg_ars"], OP, f"${X['cmg_ars']:.1f}m")]
        rows = hbars(items, max_value=7, x0=0.6, top=1.2, row=1.1, length=5.4, size=17, bar_h=0.55)
        hd = tx("Sales a restaurant, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Darden, Form 10-K for fiscal 2026 (sales over restaurants); McDonald's and Chipotle, Forms 10-K for 2025", size=12)
        beat(self,
             "Sit-down restaurants are a different trade. <bookmark mark='a'/> Darden's restaurants each sold about "
             f"{dr:.1f} million dollars in its last year, <bookmark mark='b'/> more than a franchised McDonald's in America, "
             f"<bookmark mark='c'/> and nearly twice a Chipotle. But they need waiters, bigger kitchens and bigger dining rooms, "
             "and the customer stays an hour instead of five minutes. Darden runs every one of its restaurants itself: a "
             "sit-down restaurant's quality depends on how it is run each night, which is hard to write into a franchise "
             "manual.",
             base=[rows.axis, hd, src], steps=[rows[0], rows[1], rows[2]])
