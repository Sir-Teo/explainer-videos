from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 2, "A dollar at the till", "Where does a dollar spent at Walmart go?",
             "Chapter two. A dollar at the till. Every big retailer splits the same dollar three ways: the goods, the "
             "running of the stores, and the sliver that is left.", lit=("dollar",))
        self.walmart()
        self.us()
        self.gross_net()
        self.kroger()
        self.reading()

    def walmart(self):
        W = R["dollar"]["wmt"]
        parts = [("the goods", 1 - W["gp"] / 100, GOODS), ("running the stores and the company", W["opex"] / 100, MASS),
                 ("operating profit", W["op"] / 100, GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.1f}c", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"Walmart, year to January 2026: a dollar of its ${W['sales']:.0f}bn of net sales", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Walmart, Form 10-K for fiscal 2026 (as percentages of net sales; membership and other income are on top)", size=12)
        beat(self,
             f"Walmart's dollar, from its own accounts. <bookmark mark='a'/> {100 - W['gp']:.1f} cents bought the goods. "
             f"<bookmark mark='b'/> {W['opex']:.1f} cents ran the stores, the warehouses, the lorries, the website and the "
             f"head office. <bookmark mark='c'/> {W['op']:.1f} cents was left as operating profit, before interest and tax. "
             "Membership fees from Sam's Club and Walmart Plus come on top, and are worth more than they look.",
             base=[hd, src], steps=[VGroup(bar[i], labs[i]) for i in range(3)])

    def us(self):
        c = stat_cards([(f"${get('wm31.us.sales'):.0f}bn", "Walmart U.S. net sales", MASS), (f"{get('wm31.us.op'):.1f}%", "its operating margin", GOOD),
                        (f"${get('wm31.us.sales') * get('wm31.us.op') / 100:.1f}bn", "its operating income", GOOD),
                        (f"{get('wm31.us.units'):,}", "stores", ALL)], y=0.6, size=34, span=12.6)
        shops = VGroup(*[draw.shop(0.9, color=MASS) for _ in range(8)]).arrange(RIGHT, buff=0.2).move_to([0, -1.8, 0])
        src = source("Walmart, Form 10-K for fiscal 2026: Walmart U.S. segment", size=12)
        beat(self,
             "The American stores are the core of it. <bookmark mark='a'/> Walmart U.S. sold "
             f"{get('wm31.us.sales'):.0f} billion dollars of goods in the year to January 2026 <bookmark mark='b'/> at an "
             f"operating margin of {get('wm31.us.op'):.1f} per cent, <bookmark mark='c'/> which comes to about "
             f"{get('wm31.us.sales') * get('wm31.us.op') / 100:.0f} billion dollars, <bookmark mark='d'/> from "
             f"{get('wm31.us.units'):,} stores. Five cents in the dollar, earned on almost half a trillion dollars of sales.",
             base=[shops, src], steps=[c[0], c[1], c[2], c[3]])

    def gross_net(self):
        M = R["dollar"]["margins"]
        order = ["Costco", "BJ's", "Kroger", "Walmart", "Albertsons", "Target", "Dollar General", "Dollar Tree", "Sprouts"]
        items = [(k, M[k]["gross"], M[k]["net"]) for k in order]
        pa = viz.plot_axes([0, 40], [0, len(items)], x_length=8.4, y_length=4.8, xticks=[0, 10, 20, 30, 40],
                           xfmt=lambda v: f"{v:.0f}%", grid=False, size=13).move_to([0.9, -0.4, 0])
        rows = VGroup()
        for i, (n, gm, nm) in enumerate(items):
            y = len(items) - 0.5 - i
            seg = Line(pa.ax.c2p(nm, y), pa.ax.c2p(gm, y), stroke_color=GREY_B, stroke_width=3)
            d1 = Dot(pa.ax.c2p(gm, y), radius=0.08, color=GOODS)
            d2 = Dot(pa.ax.c2p(nm, y), radius=0.08, color=GOOD)
            lab = tx(n, 15, WHITE, bold=True).next_to(pa.ax.c2p(0, y), LEFT, buff=0.2)
            v = tx(f"{gm:.0f}% to {nm:.1f}%", 13, GREY_A).next_to(d1, RIGHT, buff=0.12)
            rows.add(VGroup(lab, seg, d1, d2, v))
        key = VGroup(VGroup(Dot(color=GOODS), tx("gross margin: sales less the goods", 14, GOODS)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=GOOD), tx("net margin: what is kept", 14, GOOD)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.6)
        src = source("Forms 10-K via SEC company facts, latest fiscal year", size=12)
        bj = M["BJ's"]["gross"]
        beat(self,
             "Now line up the retailers by what they keep. <bookmark mark='a'/> Costco and BJ's, the warehouse clubs, keep "
             f"only {M['Costco']['gross']:.0f} and {bj:.0f} cents of each dollar after "
             "paying for the goods. <bookmark mark='b'/> The supermarkets, Walmart and Target, about a quarter. "
             "<bookmark mark='c'/> The dollar stores and Sprouts, which sells fresh and organic food, more than a third. "
             "But follow each line to its green end: after running the shops, almost all of them keep between one and "
             f"seven cents. Costco {M['Costco']['net']:.1f}, Walmart {M['Walmart']['net']:.1f}, Kroger {M['Kroger']['net']:.1f}.",
             base=[pa, key, src], steps=[VGroup(*rows[:2]), VGroup(*rows[2:6]), VGroup(*rows[6:])])

    def kroger(self):
        M = R["dollar"]["margins"]["Kroger"]
        parts = [("goods", 1 - M["gross"] / 100, GOODS), ("running the stores", (M["gross"] - M["op"]) / 100, GROCER),
                 ("operating profit", M["op"] / 100, GOOD)]
        bar = viz.bar_split(parts, 1.0, width=12.4, height=0.9).move_to([0, 0.8, 0])
        labs = VGroup(*[VGroup(tx(f"{100 * v:.1f}c", 22, c, bold=True), tx(n, 14, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar[i], DOWN, buff=0.2)
                        for i, (n, v, c) in enumerate(parts)])
        hd = tx(f"Kroger, year to January 2026: a dollar of its ${M['rev']:.0f}bn of sales", 20, WHITE, bold=True).to_edge(UP, buff=0.8)
        src = source("Kroger, Form 10-K for fiscal 2025, via SEC company facts; the year includes $2.5bn of charges on its automated warehouses", size=12)
        beat(self,
             f"Now the biggest pure grocer. <bookmark mark='a'/> Kroger spent {100 - M['gross']:.0f} cents of each dollar "
             f"on the goods. <bookmark mark='b'/> {M['gross'] - M['op']:.0f} cents ran the stores, the pharmacies and the "
             f"rest. <bookmark mark='c'/> Just {M['op']:.1f} cents was left as operating profit, in a year when it wrote off "
             "two and a half billion dollars of automated warehouses, a story chapter eight tells. Without that charge it "
             "would have kept nearer three cents: the business works, but there is no room for a large mistake.",
             base=[hd, src], steps=[VGroup(bar[i], labs[i]) for i in range(3)])

    def reading(self):
        g = VGroup(tx("Why the margin is thin, in this series' reading", 21, WHITE, bold=True),
                   tx("shoppers can compare the price of milk and bread in a glance", 18, MASS),
                   tx("rivals are a short drive or a click away", 18, ONLINE),
                   tx("and the goods are the same brands, from the same suppliers, in every store", 18, GOODS),
                   tx("so the only lasting edge is cost: buying, moving and selling for less", 18, GOOD)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.2, 0])
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Why so thin? In this series' reading, <bookmark mark='a'/> shoppers know the price of milk and bread, "
             "<bookmark mark='b'/> a rival is always a short drive or a click away, <bookmark mark='c'/> and most of the "
             "goods are the same brands in every store. <bookmark mark='d'/> So the only edge that lasts is cost: buying "
             "for less, moving for less and selling for less than anyone else, at a scale nobody else can match. Every other "
             "advantage, a better location, a cleverer promotion, a nicer store, can be copied by a rival within a year.",
             base=[tag], steps=[g[:2], g[2], g[3], g[4]])
