from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403


class Returns(VoiceoverScene):
    def construct(self):
        card(self, 3, "Thin margin, fast money", "How can a penny a dollar be a good business?",
             "Chapter three. Thin margin, fast money. A distributor's accounts look terrible at the bottom of the income "
             "statement and wonderful on the balance sheet.", lit=("dollar", "moat"))
        self.margins()
        self.days()
        self.turns()

    def margins(self):
        M = R["returns"]["margins"]
        names = ["McKesson", "Cencora", "Cardinal Health", "Sysco", "US Foods", "Arrow", "Grainger", "Fastenal"]
        col = {"McKesson": DRUG, "Cencora": DRUG, "Cardinal Health": DRUG, "Sysco": FOOD, "US Foods": FOOD, "Arrow": TECH,
               "Grainger": IND, "Fastenal": IND}
        items = [(n, M[n]["net"], col[n], f"{M[n]['net']:.1f}c") for n in names]
        rows = hbars(items, max_value=16, x0=-0.6, top=2.2, row=0.62, length=6.4, size=17, bar_h=0.38)
        hd = tx("Net profit per dollar of revenue, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.5)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Start with the bottom line. <bookmark mark='a'/> The three drug wholesalers kept between "
             f"{M['Cardinal Health']['net']:.1f} and {M['McKesson']['net']:.1f} cents of each dollar. <bookmark mark='b'/> "
             f"The food distributors, Sysco and US Foods, about two. <bookmark mark='c'/> Arrow, which distributes electronic "
             f"components, {M['Arrow']['net']:.1f}. <bookmark mark='d'/> And the industrial suppliers, Grainger and Fastenal, "
             f"{M['Grainger']['net']:.0f} and {M['Fastenal']['net']:.0f}: they sell screws, gloves and spare parts in small "
             "quantities, and in this series' reading a buyer who needs one part today does not haggle over its price.",
             base=[rows.axis, hd, src], steps=[VGroup(*rows[:3]), VGroup(*rows[3:5]), rows[5], VGroup(*rows[6:])])

    def days(self):
        D = R["returns"]["days"]
        names = ["McKesson", "Cencora", "Cardinal Health", "US Foods", "WESCO", "Fastenal"]
        rows = [["", "days of stock", "days customers take", "days to pay suppliers", "net days of money tied up"]]
        cols = [None]
        for n in names:
            d = D[n]
            rows.append([n, f"{d['inv']:.0f}", f"{d['rec']:.0f}", f"{d['pay']:.0f}", f"{d['wc_days']:+.0f}"])
            cols.append([WHITE, GOODS, DRUG, BAD, GOOD if d["wc_days"] < 0 else IND])
        t = table(rows, col_x=[-6.6, -2.8, -0.7, 1.6, 4.1], top=1.9, row_h=0.62, size=17, colors=cols)
        src = source("Forms 10-K via SEC company facts: inventory and payables over cost of sales, receivables over revenue", size=12)
        beat(self,
             "Now the balance sheet. <bookmark mark='a'/> McKesson holds about "
             f"{D['McKesson']['inv']:.0f} days of stock and its customers take {D['McKesson']['rec']:.0f} days to pay; but it "
             f"takes {D['McKesson']['pay']:.0f} days to pay the drug makers. <bookmark mark='b'/> Cencora and Cardinal are the "
             "same: all three run on less than nothing. <bookmark mark='c'/> A food distributor needs about ten days of "
             "money, <bookmark mark='d'/> an electrical distributor like WESCO about eighty, <bookmark mark='e'/> and "
             f"Fastenal, which keeps a wide range in its own branches and at its customers' sites, {D['Fastenal']['wc_days']:.0f}. "
             "The thinner the margin, the faster the money has to turn.",
             base=[t[0], src], steps=[t[1], VGroup(t[2], t[3]), t[4], t[5], t[6]])

    def turns(self):
        M = R["returns"]["margins"]
        rows = [["", "profit per dollar", "x", "dollars of sales per dollar of assets", "=", "return on assets"]]
        cols = [None]
        for n in ("McKesson", "Sysco", "Arrow", "Fastenal"):
            r = M[n]
            rows.append([n, f"{r['net']:.1f}c", "x", f"{r['turns']:.2f}", "=", f"{r['net'] * r['turns']:.1f}%"])
            cols.append([WHITE, GOOD, GREY_B, DRUG, GREY_B, TRADE])
        t = table(rows, col_x=[-6.6, -3.6, -1.6, -0.9, 3.4, 4.1], top=1.6, row_h=0.8, size=18, colors=cols)
        tag = estimate_tag("this series' reading: on the money a drug wholesaler's owners actually put in, the return is far higher", size=12)
        beat(self,
             "Put the two together: return equals margin times turns, as in Part 31. <bookmark mark='a'/> McKesson's "
             f"{M['McKesson']['net']:.1f} cents, turned {M['McKesson']['turns']:.1f} times a year, makes "
             f"{M['McKesson']['net'] * M['McKesson']['turns']:.1f} per cent on its assets, and much of what those assets hold is "
             "stock and customers' debts that its suppliers' credit pays for. <bookmark mark='b'/> Sysco, "
             f"{M['Sysco']['net'] * M['Sysco']['turns']:.1f}. <bookmark mark='c'/> Arrow, whose stock and credit to customers "
             f"are heavy, {M['Arrow']['net'] * M['Arrow']['turns']:.1f}. <bookmark mark='d'/> Fastenal, with a fat margin "
             f"and slow turns, {M['Fastenal']['net'] * M['Fastenal']['turns']:.0f}. There is more than one way to be a good "
             "middleman, but there is no way to be a slow one on a thin margin.",
             base=[t[0], tag], steps=[t[1], t[2], t[3], t[4]])
