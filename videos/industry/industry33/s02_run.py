from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a distributor for a year", "Five billion dollars of medicines on a margin of four cents. How much do you stock?",
             "Chapter one. Run it. You run a regional drug wholesaler for a year: thousands of medicines bought from the "
             "makers, held in a warehouse, and delivered every day to hundreds of pharmacies.", lit=("unit", "make"))
        self.picture()
        self.dollar()
        self.money()
        self.service()
        self.drop()
        self.lesson()

    def picture(self):
        U = R["run"]
        makers = VGroup(*[draw.factory(1.0) for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([-5.4, 0.5, 0])
        wh = draw.warehouse(3.0, docks=5, trucks=1).move_to([0, 0.6, 0])
        shops = VGroup(*[draw.shop(0.7, color=DRUG) for _ in range(8)]).arrange_in_grid(4, 2, buff=0.25).move_to([5.2, 0.5, 0])
        a1 = Arrow([-4.6, 0.5, 0], [-1.7, 0.6, 0], color=GOODS, buff=0.1)
        a2 = Arrow([1.7, 0.6, 0], [4.2, 0.5, 0], color=DRUG, buff=0.1)
        t1 = tx("pallets, every week or two", 15, GOODS).next_to(a1, UP, buff=0.1)
        t2 = tx("totes, every day", 15, DRUG).next_to(a2, UP, buff=0.1)
        c = stat_cards([(f"${U['sales'] / 1e9:.0f}bn", "sales a year", ALL), (f"{100 * U['gm']:.1f}c", "kept of each dollar after the goods", GOOD)],
                       y=-2.2, size=30, span=8)
        tag = estimate_tag("the Works: a distributor with McKesson's margins and payment terms (explainer/industry/works/distributor.py)", size=12)
        beat(self,
             "Here is the business. <bookmark mark='a'/> Makers ship you pallets of medicine every week or two. "
             "<bookmark mark='b'/> You hold it in one warehouse. <bookmark mark='c'/> And every day your vans take small "
             "totes to pharmacies, a few boxes of this and a few of that, so that none of them needs a stockroom. "
             f"<bookmark mark='d'/> You sell {U['sales'] / 1e9:.0f} billion dollars a year and keep "
             f"{100 * U['gm']:.1f} cents of each dollar after paying the makers: McKesson's own gross margin.",
             base=[tag], steps=[VGroup(makers, a1, t1), wh, VGroup(shops, a2, t2), c])

    def dollar(self):
        U = R["run"]
        b = U["base"]
        parts = [("the medicines", 1 - U["gm"], GOODS), ("warehouse, vans, people", U["opex"], DRUG), ("operating profit", U["gm"] - U["opex"], GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 1.3, 0])
        l0 = tx(f"{100 * parts[0][1]:.1f}c: the medicines", 20, GOODS, bold=True).next_to(bar[0], DOWN, buff=0.25)
        tail = parts[1][1] + parts[2][1]
        zoom = viz.bar_split(parts[1:], tail, width=8.0, height=0.9).move_to([0, -1.2, 0])
        guide = VGroup(DashedLine(bar[1].get_corner(DL), zoom.get_corner(UL), color=GREY_B, stroke_width=1.5),
                       DashedLine(bar[2].get_corner(DR), zoom.get_corner(UR), color=GREY_B, stroke_width=1.5))
        l1 = VGroup(tx(f"{100 * parts[1][1]:.1f}c", 20, DRUG, bold=True), tx("warehouse, vans, people", 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(zoom[0], DOWN, buff=0.2)
        l2 = VGroup(tx(f"{100 * parts[2][1]:.1f}c", 20, GOOD, bold=True), tx("operating profit", 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(zoom[1], DOWN, buff=0.2)
        cap = tx(f"the last {100 * tail:.1f} cents, magnified: about ${b['op'] / 1e6:.0f}m of operating profit", 17, WHITE, bold=True).to_edge(DOWN, buff=0.85)
        hd = tx("a dollar through the Works' distributor", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        tag = estimate_tag("the Works: McKesson's gross and operating margins, fiscal 2026", size=12)
        beat(self,
             f"Follow a dollar. <bookmark mark='a'/> {100 * parts[0][1]:.1f} cents goes straight to the maker of the "
             f"medicine. <bookmark mark='b'/> Magnify the rest. {100 * parts[1][1]:.1f} cents pays for the warehouse, the "
             f"vans, the drivers and the people who pick each order. <bookmark mark='c'/> {100 * parts[2][1]:.1f} cents is "
             f"left. <bookmark mark='d'/> That sliver is the whole business: on your {U['sales'] / 1e9:.0f} billion dollars "
             f"of sales, about {b['op'] / 1e6:.0f} million dollars of operating profit.",
             base=[hd, tag], steps=[VGroup(bar[0], l0), VGroup(bar[1], guide, zoom[0], l1), VGroup(bar[2], zoom[1], l2), cap])

    def money(self):
        U = R["run"]
        b = U["base"]
        items = [("medicines on the shelves", b["inventory"] / 1e6, GOODS, m(b["inventory"])),
                 ("owed to you by pharmacies", b["receivables"] / 1e6, DRUG, m(b["receivables"])),
                 ("owed by you to the makers", -b["payables"] / 1e6, BAD, m(-b["payables"])),
                 ("money you need", b["capital"] / 1e6, GOOD, m(b["capital"]))]
        rows = hbars(items, max_value=800, x0=0.4, top=1.6, row=0.95, length=5.2, size=17, bar_h=0.5)
        hd = tx("the Works' distributor: money tied up at the end of the year", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        days = tx(f"stock {b['stock_days']:.0f} days; pharmacies pay in {U['recv']:.0f}; you pay makers in {U['pay']:.0f}", 17, GREY_A).to_edge(DOWN, buff=0.75)
        tag = estimate_tag("the Works: payment days are McKesson's, from its balance sheet at March 2026", size=12)
        beat(self,
             "Now the money. <bookmark mark='a'/> You hold about "
             f"{b['stock_days']:.0f} days of stock: {b['inventory'] / 1e6:.0f} million dollars of medicine on the shelves. "
             f"<bookmark mark='b'/> Pharmacies take {U['recv']:.0f} days to pay you, so they owe you {b['receivables'] / 1e6:.0f} "
             f"million. <bookmark mark='c'/> But you take {U['pay']:.0f} days to pay the makers, so you owe them "
             f"{b['payables'] / 1e6:.0f} million. <bookmark mark='d'/> Add it up and the business needs less than nothing: "
             f"the makers' money funds your stock and your customers' credit, with {abs(b['capital']) / 1e6:.0f} million to "
             "spare. A penny of profit on almost no capital is a very good return.",
             base=[rows.axis, hd, days, tag], steps=[rows[0], rows[1], rows[2], rows[3]])

    def service(self):
        U = R["run"]
        Z = U["by_z"]
        days = {s["stock_days"]: s["profit"] / 1e6 for s in Z.values()}
        ch = line_chart({"profit": (days, GOOD)}, x=(8, 26), y=(-20, 100), xticks=[8, 12, 16, 20, 24], yticks=[-20, 0, 25, 50, 75, 100],
                        xfmt=lambda v: f"{v:.0f} days", yfmt=lambda v: f"${v:.0f}m",
                        ylabel="the Works: a year's profit, after the cost of capital, by days of stock held", width=8.6, height=4.3,
                        center=(-1.0, -0.45), label_end=False)
        zero = DashedLine(ch.ax.c2p(8, 0), ch.ax.c2p(26, 0), color=GREY_B, stroke_width=1.5)
        bz, base, full = U["best"], U["base"], U["full"]
        lo = Z[min(Z)]
        m00 = marker(ch.ax, lo["stock_days"], lo["profit"] / 1e6, f"{100 * lo['fill']:.0f}% of lines filled", BAD, side=RIGHT)
        m0 = marker(ch.ax, base["stock_days"], base["profit"] / 1e6, f"{100 * base['fill']:.1f}% filled: ${base['profit'] / 1e6:.0f}m", DRUG, side=DOWN + RIGHT)
        m1 = marker(ch.ax, bz["stock_days"], bz["profit"] / 1e6, f"{100 * bz['fill']:.0f}%: ${bz['profit'] / 1e6:.0f}m", GOOD, side=UP)
        m2 = marker(ch.ax, full["stock_days"], full["profit"] / 1e6, f"{100 * full['fill']:.2f}%: ${full['profit'] / 1e6:.0f}m", BAD, side=DOWN + LEFT)
        tag = estimate_tag("the Works: each point of orders filled below 99% loses 2% of sales; stock costs 8% a year", size=12)
        beat(self,
             "Your one big decision is how much to stock. <bookmark mark='a'/> Hold too little and you fill too few order "
             "lines; every line you cannot fill sends a pharmacist to a rival, and some do not come back. With "
             f"{base['stock_days']:.0f} days of stock you fill {100 * base['fill']:.1f} per cent of lines and make "
             f"{base['profit'] / 1e6:.0f} million dollars after the cost of your capital. <bookmark mark='b'/> Hold "
             f"{bz['stock_days']:.0f} days, enough for {100 * bz['fill']:.0f} per cent, and you keep every customer: "
             f"{bz['profit'] / 1e6:.0f} million. <bookmark mark='c'/> Try to fill every last line and you hold "
             f"{full['stock_days']:.0f} days; the extra shelves earn nothing, and profit falls to {full['profit'] / 1e6:.0f} "
             "million. A distributor sells availability, and the art is knowing how much is enough.",
             base=[ch.frame, zero, tag], steps=[VGroup(ch.lines["profit"], m00, m0), m1, m2])

    def drop(self):
        U = R["run"]
        a, d = U["best"], U["drop"]
        rows = [["", "hold the stock", "drop-ship from the maker"],
                ["sales a year", f"${a['sales'] / 1e9:.1f}bn", f"${d['sales'] / 1e9:.2f}bn"],
                ["kept of each dollar", f"{100 * (a['gp'] / a['sales']):.1f}c", f"{100 * (d['gp'] / d['sales']):.1f}c"],
                ["stock on the shelves", m(a["inventory"]), "none"],
                ["profit after capital", m(a["profit"]), m(d["profit"])]]
        cols = [None, [WHITE, GOOD, BAD], [WHITE, GOOD, BAD], [WHITE, GOODS, GREY_A], [WHITE, GOOD, BAD]]
        t = table(rows, col_x=[-6.0, -1.0, 2.6], top=1.6, row_h=0.8, size=19, colors=cols)
        tag = estimate_tag("the Works: drop-shipped orders take four days, and pharmacies that need them tomorrow go elsewhere", size=12)
        beat(self,
             "Could you skip the warehouse? <bookmark mark='a'/> Some distributors drop-ship: they take the order and the "
             "maker sends it straight to the customer. <bookmark mark='b'/> But the order takes four days instead of one, "
             f"and a pharmacy with a patient waiting cannot wait; in the Works it keeps only {100 * get('wk33.dropkeep'):.0f} "
             "per cent of its custom. And a firm that only passes orders on earns a thinner margin, because it adds less. "
             f"<bookmark mark='c'/> There is no stock to pay for, <bookmark mark='d'/> but profit falls from "
             f"{a['profit'] / 1e6:.0f} million to {d['profit'] / 1e6:.0f} million. The stock is not a burden the middleman "
             "carries; it is the product.",
             base=[t[0], tag], steps=[t[1], t[2], t[3], t[4]])

    def lesson(self):
        g = VGroup(tx("What Run it shows", 22, WHITE, bold=True),
                   tx("the distributor keeps a few cents of each dollar, and spends most of them on warehouses and vans", 18, DRUG),
                   tx("but the makers' credit pays for its stock: it needs almost no money of its own", 18, GOOD),
                   tx("it sells availability: fill nearly every order, but not every last one", 18, GOODS),
                   tx("holding the stock earns more than passing the order on", 18, TRADE)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' summary of the Works' distributor", size=12)
        beat(self,
             "So: <bookmark mark='a'/> the distributor keeps a few cents of each dollar and spends most of them on "
             "warehouses and vans. <bookmark mark='b'/> Its suppliers' credit pays for its stock. <bookmark mark='c'/> It "
             "sells availability. <bookmark mark='d'/> And holding the stock is the job, not a cost to be cut. The rest of "
             "this film is about why a few such companies end up handling so much of the economy.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
