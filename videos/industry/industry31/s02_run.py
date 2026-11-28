from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a store for a year", "A supermarket on a two per cent margin. How do you price it, and how do you staff it?",
             "Chapter one. Run it. You run a supermarket for a year: fifty million dollars of sales, a few rivals within a "
             "short drive, and two cents of profit on every dollar if nothing goes wrong.", lit=("unit", "make"))
        self.store()
        self.dollar()
        self.price()
        self.cut()
        self.staff()
        self.drop()
        self.lesson()

    def store(self):
        U = R["run"]
        shop = draw.shop(3.0, color=GROCER).move_to([-3.6, 0.8, 0])
        shelf = draw.shelf(5.0, rows=3, n=8).move_to([2.6, 0.8, 0])
        c = stat_cards([(f"${U['sales'] / 1e6:.0f}m", "sales a year", ALL), (f"{100 * U['gm']:.1f}%", "gross margin (Kroger's, 2025)", GOOD),
                        (f"{100 * U['base']['margin']:.1f}%", "left as profit", GOOD)], y=-2.0, size=34, span=11)
        tag = estimate_tag("the Works: a supermarket with Kroger's gross margin and this series' assumptions for its costs", size=12)
        beat(self,
             "Here is the store. <bookmark mark='a'/> It sells fifty million dollars a year; Kroger's revenue divided by its "
             f"supermarkets comes to about fifty-five million each, pharmacies and fuel included. <bookmark mark='b'/> After paying for the goods it keeps {100 * U['gm']:.1f} cents of each "
             "dollar, Kroger's own gross margin in 2025. <bookmark mark='c'/> And after the staff, the rent and everything "
             f"else, {100 * U['base']['margin']:.1f} cents is left: {U['base']['profit'] / 1e6:.2f} million dollars a year.",
             base=[shop, shelf, tag], steps=[c[0], c[1], c[2]])

    def dollar(self):
        U = R["run"]
        b = U["base"]
        parts = [("goods", b["goods"] / b["revenue"], GOODS), ("staff", b["labour"] / b["revenue"], MASS),
                 ("rent", b["occupancy"] / b["revenue"], ONLINE), ("other", b["other"] / b["revenue"], ALL),
                 ("profit", b["profit"] / b["revenue"], GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.1f}c", 20, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx("the Works' store: a dollar at the till", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works: staff, rent and other costs are this series' assumptions", size=12)
        beat(self,
             f"Follow a dollar. <bookmark mark='a'/> {100 * parts[0][1]:.1f} cents pays for the goods on the shelf. "
             f"<bookmark mark='b'/> {100 * parts[1][1]:.0f} cents pays the people who stock, cut, check out and clean. "
             f"<bookmark mark='c'/> {100 * parts[2][1]:.0f} cents pays the rent. <bookmark mark='d'/> {100 * parts[3][1]:.0f} "
             "cents goes on lorries from the warehouse, card fees, bags and the goods that are stolen or spoil. "
             f"<bookmark mark='e'/> {100 * parts[4][1]:.1f} cents is yours.",
             base=[hd, tag], steps=[VGroup(bar[i], labs[i]) for i in range(5)])

    def price(self):
        U = R["run"]
        bp = {(p - 1) * 100: v / 1e6 for p, v in U["by_price"].items()}
        ch = line_chart({"profit": (bp, GOOD)}, x=(-6, 6), y=(0.4, 1.3), xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[0.4, 0.6, 0.8, 1.0, 1.2],
                        xfmt=lambda v: f"{v:+.0f}%", yfmt=lambda v: f"${v:.1f}m",
                        ylabel="the Works: a year's profit, by the store's prices against its rivals'", width=9.0, height=4.2,
                        center=(-0.8, -0.45), label_end=False)
        m0 = marker(ch.ax, 0, U["base"]["profit"] / 1e6, f"today: ${U['base']['profit'] / 1e6:.2f}m", GOOD, side=UP)
        m1 = marker(ch.ax, -3, U["by_price"][0.97] / 1e6, f"3% cheaper: ${U['by_price'][0.97] / 1e6:.2f}m", BAD, side=LEFT)
        m2 = marker(ch.ax, 3, U["by_price"][1.03] / 1e6, f"3% dearer: ${U['by_price'][1.03] / 1e6:.2f}m", BAD, side=RIGHT)
        tag = estimate_tag(f"the Works: for each 1% dearer, about {abs(U['elasticity']):.1f}% fewer sales (shoppers have rivals nearby)", size=12)
        beat(self,
             "Your first lever is price. <bookmark mark='a'/> Your shoppers have other stores nearby, so if you are one per "
             f"cent dearer than them you lose about {abs(U['elasticity']):.1f} per cent of your sales. <bookmark mark='b'/> "
             f"Cut prices three per cent and you win shoppers, but profit falls to {U['by_price'][0.97] / 1e6:.2f} million. "
             f"<bookmark mark='c'/> Raise them three per cent and it falls to {U['by_price'][1.03] / 1e6:.2f} million, as "
             "shoppers drift away. Competition has already put your prices about where they should be: the thin margin is "
             "not a choice, it is what the rivals allow.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["profit"], m0), m1, m2])

    def cut(self):
        U = R["run"]
        c = stat_cards([("1%", "price cut", BAD), (f"+{100 * U['cut1_need']:.1f}%", "more sales needed to stand still", MASS),
                        (f"+{100 * U['cut2_need']:.1f}%", "for a 2% cut", MASS)], y=0.6, size=40, span=11)
        cartg = VGroup(*[draw.cart(0.9) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, -1.8, 0])
        tag = estimate_tag("the Works: with staff and rent fixed", size=12)
        beat(self,
             "Why are price cuts so dangerous? <bookmark mark='a'/> Cut prices by one per cent and that cent comes straight "
             f"out of your profit of {100 * U['base']['margin']:.1f}. <bookmark mark='b'/> To earn the same as before you "
             f"would need {100 * U['cut1_need']:.1f} per cent more sales: more shoppers, bigger baskets, every week of the "
             f"year. <bookmark mark='c'/> For a two per cent cut, {100 * U['cut2_need']:.0f} per cent more. When one grocer "
             "cuts and the others follow, nobody wins the extra shoppers and everyone loses the cent.",
             base=[cartg, tag], steps=[c[0], c[1], c[2]])

    def staff(self):
        U = R["run"]
        bs = {(s - 1) * 100: v / 1e6 for s, v in U["by_staff"].items()}
        ch = line_chart({"profit": (bs, MASS)}, x=(-25, 25), y=(-0.2, 1.3), xticks=[-20, -10, 0, 10, 20], yticks=[0, 0.4, 0.8, 1.2],
                        xfmt=lambda v: f"{v:+.0f}%", yfmt=lambda v: f"${v:.1f}m",
                        ylabel="the Works: a year's profit, by staff hours against normal", width=9.0, height=4.2,
                        center=(-0.8, -0.45), label_end=False)
        a, b = U["staff80"], U["staff120"]
        m1 = marker(ch.ax, -20, a["profit"] / 1e6, f"20% fewer hours: ${a['profit'] / 1e6:.2f}m", BAD, side=RIGHT)
        m2 = marker(ch.ax, 20, b["profit"] / 1e6, f"20% more: ${b['profit'] / 1e6:.2f}m", BAD, side=LEFT)
        tag = estimate_tag("the Works: fewer hours mean queues, empty shelves and theft; more hours earn little extra (assumptions)", size=12)
        beat(self,
             "Your second lever is staff, the biggest cost you control. <bookmark mark='a'/> Cut hours by a fifth and you "
             f"save {0.2 * U['labour'] * 100:.1f} cents on the dollar, but queues lengthen, shelves go empty and more is "
             f"stolen; you lose {100 * (1 - a['volume']):.0f} per cent of your sales and profit falls to "
             f"{a['profit'] / 1e6:.2f} million. <bookmark mark='b'/> Add a fifth more hours and service improves, but "
             f"barely sells more: profit falls to {b['profit'] / 1e6:.2f} million. The store that is run well is the one "
             "staffed just right, week by week, and that is the daily craft of the business.",
             base=[ch.frame, tag], steps=[VGroup(ch.lines["profit"], m1), m2])

    def drop(self):
        D = R["run"]["drops"]
        items = [(f"sales {100 * d:.0f}% lower" if d else "a normal year", v / 1e6, GOOD if d == 0 else BAD,
                  f"{'-' if v < 0 else ''}${abs(v) / 1e6:.2f}m") for d, v in D.items()]
        rows = hbars(items, max_value=1.3, x0=0.4, top=1.5, row=0.9, length=5.4, size=17, bar_h=0.45)
        lab = tx("the Works' store: a year's profit if sales fall, with staff and rent unchanged", 17, GREY_A).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works", size=12)
        beat(self,
             "And one more danger: a bad year. <bookmark mark='a'/> In a normal year the store makes "
             f"{D[0.0] / 1e6:.2f} million dollars. <bookmark mark='b'/> If a new rival opens nearby and sales fall five per "
             f"cent, with the same staff and the same rent, profit falls to {D[0.05] / 1e6:.2f} million. "
             f"<bookmark mark='c'/> At ten per cent lower, {D[0.1] / 1e6:.2f} million; at fifteen, a loss. The store's costs "
             "barely move with its sales, so a small loss of shoppers takes a large bite out of a small profit. That is why "
             "grocers watch every new store opening within a few miles.",
             base=[rows.axis, lab, tag], steps=[rows[0], rows[1], VGroup(rows[2], rows[3])])

    def lesson(self):
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx("three-quarters of every dollar is the goods; the rest is staff, rent and the lorries", 18, GOODS),
                   tx("the price is set by the rivals down the road, not by the store", 18, MASS),
                   tx("a 1% price cut needs 6% more sales to pay for itself", 18, BAD),
                   tx("so the money is made by running the store well, and running many of them", 18, GOOD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' store", size=12)
        beat(self,
             "So: <bookmark mark='a'/> three-quarters of each dollar is the goods. <bookmark mark='b'/> The price is set by "
             "the rivals down the road. <bookmark mark='c'/> A small price war wipes out the profit. <bookmark mark='d'/> "
             "The money is made by running each store a little better than the next, and by running thousands of them "
             "with the same lorries, the same warehouses and the same buyers. That is what the rest of this film is about.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
