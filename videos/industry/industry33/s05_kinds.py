from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Kinds(VoiceoverScene):
    def construct(self):
        card(self, 4, "Four kinds of middlemen", "Why does one distributor keep four cents of a dollar and another forty-five?",
             "Chapter four. Four kinds of middlemen, and what each keeps of a dollar before its own costs.", lit=("dollar",))
        self.bars()
        self.why()
        self.chips()
        self.labels()

    def bars(self):
        K = R["kinds"]
        order = [("McKesson", "medicines", DRUG), ("Sysco", "food for restaurants", FOOD), ("Arrow", "electronic components", TECH),
                 ("Grainger", "maintenance supplies", IND), ("Fastenal", "fasteners and supplies", IND)]
        rows = VGroup()
        for i, (n, what, col) in enumerate(order):
            k = K[n]
            g_, o_ = k["gross"] / 100, k["op"] / 100
            bar = viz.bar_split([("goods", 1 - g_, GOODS), ("costs", g_ - o_, col), ("profit", o_, WHITE)], 1.0, width=7.6, height=0.5)
            bar.move_to([1.6, 2.0 - 0.95 * i, 0])
            nm = VGroup(tx(n, 17, col, bold=True), tx(what, 12, GREY_A)).arrange(DOWN, aligned_edge=RIGHT, buff=0.04).next_to(bar, LEFT, buff=0.25)
            val = tx(f"{k['gross']:.1f}c kept; {k['op']:.1f}c profit", 14, col).next_to(bar, RIGHT, buff=0.15)
            if val.get_right()[0] > 7.0:
                val.next_to(bar, DOWN, buff=0.05, aligned_edge=RIGHT)
            rows.add(VGroup(nm, bar, val))
        hd = tx("A dollar of sales: the goods (brown), the distributor's costs (colour), its operating profit (white)", 18, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("Forms 10-K via SEC company facts, latest year", size=12)
        beat(self,
             f"<bookmark mark='a'/> McKesson keeps {K['McKesson']['gross']:.1f} cents of each dollar after paying for the "
             f"goods. <bookmark mark='b'/> Sysco keeps {K['Sysco']['gross']:.0f}. <bookmark mark='c'/> Arrow, "
             f"{K['Arrow']['gross']:.0f}. <bookmark mark='d'/> Grainger, {K['Grainger']['gross']:.0f}. <bookmark mark='e'/> "
             f"Fastenal, {K['Fastenal']['gross']:.0f}. And yet the white slivers at the end, the operating profit, run only "
             f"from {K['McKesson']['op']:.1f} cents to {K['Fastenal']['op']:.0f}: most of what each keeps pays for the work.",
             base=[hd, src], steps=list(rows))

    def why(self):
        rows = [["", "a typical delivery", "what the customer pays for"],
                ["medicines", "a tote of small, costly boxes", "speed and accuracy; the price is set by the maker"],
                ["food", "a truckload of cases to one kitchen", "the whole menu in one drop, kept cold"],
                ["electronics", "reels of parts for a factory", "credit, supply in shortages, design help"],
                ["maintenance", "one part, today", "having it at all, now"]]
        cols = [None, [DRUG, WHITE, GREY_A], [FOOD, WHITE, GREY_A], [TECH, WHITE, GREY_A], [IND, WHITE, GREY_A]]
        t = table(rows, col_x=[-6.6, -3.9, 0.6], top=1.6, row_h=0.8, size=17, colors=cols)
        tag = estimate_tag("this series' reading", size=12)
        beat(self,
             "Why so different? In this series' reading, because the work per dollar is so different. "
             "<bookmark mark='a'/> A tote of medicines is worth thousands of dollars and weighs a few kilos, so the work is "
             "small beside the value. <bookmark mark='b'/> A restaurant's order is heavy, cheap per kilo and must be kept "
             "cold. <bookmark mark='c'/> An electronics distributor carries parts and credit for factories through "
             "shortages and gluts. <bookmark mark='d'/> And a maintenance supplier sells one part, today, to someone whose "
             "production line has stopped: the cost of the part is nothing beside the cost of waiting for it.",
             base=[t[0], tag], steps=[t[1], t[2], t[3], t[4]])

    def chips(self):
        D = R["returns"]["days"]
        M = R["returns"]["margins"]
        reels = VGroup(*[draw.chip(0.6) for _ in range(5)]).arrange(RIGHT, buff=0.35).move_to([0, 1.9, 0])
        c = stat_cards([(f"{D['Avnet']['inv']:.0f} days", "of stock at Avnet, June 2026", TECH),
                        (f"{D['TD Synnex']['inv']:.0f} days", "at TD Synnex, November 2025", TECH),
                        (f"{M['Avnet']['net']:.1f}c", "Avnet's profit per dollar", GOOD)], y=0.0, size=34, span=11.4)
        tag = estimate_tag("Forms 10-K via SEC company facts; this series' reading, with Part 15's chip cycle", size=12)
        beat(self,
             "The electronics distributors show what holding stock really means. <bookmark mark='a'/> Avnet carried about "
             f"{D['Avnet']['inv']:.0f} days of chips and parts at the end of its last year, <bookmark mark='b'/> TD Synnex, "
             f"which mostly sells computers and software, {D['TD Synnex']['inv']:.0f}. <bookmark mark='c'/> On a profit of "
             f"{M['Avnet']['net']:.1f} cents a dollar, that stock is the whole bet. In this series' reading, in a shortage, "
             "like the chip shortage of Part 15, a distributor with parts on the shelf can sell them to any factory that "
             "has stopped; in a glut, the same shelves are full of parts nobody wants, and the margin is lost in "
             "write-downs.",
             base=[reels, tag], steps=[c[0], c[1], c[2]])

    def labels(self):
        c = stat_cards([(f"{get('sy33.brand'):.1f}%", "of Sysco's U.S. Broadline sales are its own brands, fiscal 2026", FOOD),
                        (f"{get('sy33.brand.local'):.1f}%", "for its local customers: independent restaurants", FOOD)], y=0.6, size=40, span=11)
        crates = VGroup(*[draw.carton(0.8) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([0, -1.9, 0])
        src = source("Sysco, Form 10-K for fiscal 2026", size=12)
        beat(self,
             "Middlemen also make more where they can put their own name on the box. <bookmark mark='a'/> In its 2026 year, "
             f"{get('sy33.brand'):.0f} per cent of Sysco's broadline sales in America were Sysco's own brands. "
             f"<bookmark mark='b'/> For independent restaurants, its local customers, {get('sy33.brand.local'):.0f} per cent. "
             "Like the grocers' own labels in Part 31, a distributor's own brand turns a middleman's margin into something "
             "closer to a maker's.",
             base=[crates, src], steps=[c[0], c[1]])
