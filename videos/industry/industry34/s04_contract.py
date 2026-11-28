from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403


class Contract(VoiceoverScene):
    def construct(self):
        card(self, 3, "The contract and the land", "What does a franchisee actually buy, and what does the franchisor keep?",
             "Chapter three. The contract and the land. A franchise is a long contract: the right to use a name, a menu and a "
             "system, in return for a share of sales, for twenty years.", lit=("dollar", "moat"))
        self.terms()
        self.take()
        self.land()
        self.fees()
        self.others()

    def terms(self):
        Ct = R["contract"]
        rows = [["the franchisee pays for", "the franchisor provides"],
                ["equipment, seating, signs and decor", "the land and building, owned or leased"],
                ["the crew, the food, the running costs", "the name, the menu, the system and training"],
                ["rent and royalties, a share of sales", "advertising, through cooperatives funded by a share of sales"],
                [f"a {Ct['term']:.0f}-year agreement", "at the end, it keeps the site and chooses the next operator"]]
        cols = [None, [OP, FR], [OP, FR], [OP, FR], [OP, FR]]
        t = table(rows, col_x=[-6.4, 0.4], top=1.8, row_h=0.8, size=18, colors=cols)
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "Here is McDonald's conventional franchise, as its annual report describes it. <bookmark mark='a'/> The "
             "franchisee pays for the equipment, the seating, the signs and the decor; McDonald's owns or leases the land "
             "and the building. <bookmark mark='b'/> The franchisee hires the crew and buys the food; McDonald's provides the "
             "name, the menu and the system. <bookmark mark='c'/> The franchisee pays rent and royalties as a share of sales. "
             f"<bookmark mark='d'/> The agreement generally runs {Ct['term']:.0f} years, and at the end McDonald's still "
             "controls the property and decides who runs it next.",
             base=[t[0], src], steps=[t[1], t[2], t[3], t[4]])

    def take(self):
        Ct = R["contract"]
        bar = viz.bar_split([("rent", Ct["rents"], FR), ("royalties", Ct["royal"], MASTER)], Ct["rents"] + Ct["royal"], width=10.0, height=0.9).move_to([0, 0.8, 0])
        l1 = tx(f"rent ${Ct['rents']:.1f}bn ({100 * Ct['rent_share']:.0f}%)", 19, FR, bold=True).next_to(bar[0], DOWN, buff=0.2)
        l2 = tx(f"royalties ${Ct['royal']:.1f}bn", 19, MASTER, bold=True).next_to(bar[1], DOWN, buff=0.2)
        c = tx(f"together {100 * Ct['take']:.1f}% of franchisees' sales of ${Ct['frsales']:.0f}bn", 21, WHITE, bold=True).move_to([0, -1.4, 0])
        hd = tx("What McDonald's franchisees paid it in 2025", 21, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             f"<bookmark mark='a'/> In 2025 franchisees paid McDonald's {Ct['rents']:.1f} billion dollars of rent, "
             f"<bookmark mark='b'/> and {Ct['royal']:.1f} billion of royalties. <bookmark mark='c'/> Together, about "
             f"{100 * Ct['take']:.1f} cents of every dollar they took. Nearly two-thirds of it was rent: the franchisees are, "
             "above all, McDonald's tenants.",
             base=[hd, src], steps=[VGroup(bar[0], l1), VGroup(bar[1], l2), c])

    def land(self):
        Ct = R["contract"]
        lot = draw.plot_lot(3.0).move_to([-3.6, 0.6, 0])
        rs = draw.restaurant(3.0).move_to([2.6, 0.6, 0])
        c = stat_cards([(f"{Ct['land']:.0f}%", "of the land under its restaurants McDonald's owns", FR),
                        (f"{Ct['bldg']:.0f}%", "of the buildings", FR)], y=-1.6, size=40, span=9)
        src = source("McDonald's, Form 10-K for 2025 (restaurants in its consolidated markets)", size=12)
        beat(self,
             "And the property is the point. <bookmark mark='a'/> In the markets it runs directly, McDonald's owns about "
             f"{Ct['land']:.0f} per cent of the land under its restaurants <bookmark mark='b'/> and {Ct['bldg']:.0f} per cent of "
             "the buildings, and leases the rest on long terms. In this series' reading, that is why the system lasts: a "
             "franchisee who leaves loses the site, and the brand never has to find a new corner on a busy road.",
             base=[lot, rs, src], steps=[c[0], c[1]])

    def others(self):
        Ct = R["contract"]
        rows = [["", "royalty", "advertising", "who holds the property"],
                ["Wingstop", f"{Ct['wing_roy']:.1f}% of sales", f"{get('wg34.ad'):.1f}% to the national fund", "the franchisee"],
                ["Arcos Dorados (McDonald's in Latin America)", f"{Ct['arco_roy']:.1f}%, rising to 6.5%", "at least 5% of sales", "itself, as master franchisee"],
                ["McDonald's conventional franchisees", "rent and royalties", "a shared fund", "McDonald's"]]
        cols = [None, [MASTER, WHITE, WHITE, WHITE], [MASTER, WHITE, WHITE, WHITE], [FR, WHITE, WHITE, WHITE]]
        t = table(rows, col_x=[-6.6, -1.6, 1.0, 3.9], top=1.6, row_h=0.85, size=16, colors=cols)
        src = source("Wingstop, Form 10-K for 2025; Arcos Dorados, Form 20-F for 2025; McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "Other systems split it differently. <bookmark mark='a'/> Wingstop takes a royalty of "
             f"{Ct['wing_roy']:.0f} per cent of sales and {get('wg34.ad'):.1f} per cent for advertising, and owns no property: "
             "a lighter, purer franchise. <bookmark mark='b'/> Arcos Dorados, which runs McDonald's across Latin America, pays "
             f"McDonald's a royalty starting at {Ct['arco_roy']:.0f} per cent, rising to six and a half, and must spend at least "
             "five per cent on advertising. <bookmark mark='c'/> McDonald's own franchisees in America and Europe pay rent "
             "as well as royalties, because the company is their landlord.",
             base=[t[0], src], steps=[t[1], t[2], t[3]])

    def fees(self):
        Ct = R["contract"]
        c = stat_cards([(f"${get('md34.initial') * 1e3:.0f}m", "initial fees from new franchisees, 2025", MASTER),
                        (f"${Ct['rents'] + Ct['royal']:.1f}bn", "rent and royalties, 2025", FR)], y=0.6, size=40, span=10)
        note = tx("the money is in the years of rent and royalties, not in selling the franchise", 18, GREY_A).move_to([0, -1.4, 0])
        rs = VGroup(*[draw.restaurant(1.2) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([0, -2.5, 0])
        src = source("McDonald's, Form 10-K for 2025", size=12)
        beat(self,
             "Notice what McDonald's does not earn. <bookmark mark='a'/> New franchisees paid it only "
             f"{get('md34.initial') * 1e3:.0f} million dollars of initial fees in 2025, <bookmark mark='b'/> against "
             f"{Ct['rents'] + Ct['royal']:.1f} billion of rent and royalties. A sound franchisor makes its money from its "
             "franchisees' sales year after year, not from selling them the franchise; in this series' reading, a system that "
             "lives on opening fees is a warning sign, because it profits whether or not the restaurants do.",
             base=[note, rs, src], steps=[c[0], c[1]])
