from __future__ import annotations

from videos.industry.industry31.common import *  # noqa: F403

OFFSET = {"Amazon": UP, "Walmart": DOWN, "Costco": UP, "Kroger": DOWN, "Target": UP, "Albertsons": DOWN, "Dollar General": UP,
          "BJ's": DOWN, "Dollar Tree": UP, "Casey's": UP, "Sprouts": UP, "PriceSmart": DOWN, "Ingles": DOWN, "Weis": UP,
          "Five Below": UP, "Grocery Outlet": DOWN, "Ollie's": UP, "Village": DOWN, "Natural Grocers": DOWN}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who sells America its groceries and everyday goods, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: mass merchants, clubs, supermarkets, dollar stores, "
             "convenience chains and the online giant, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([0.0, 3.0], [0, 0.10], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30), lx(100), lx(300), lx(1000)],
                           yticks=[0, 0.02, 0.04, 0.06, 0.08, 0.10], xfmt=lambda v: f"${10 ** v:.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 10)
            d = Dot(pa.ax.c2p(lx(c["rev"]), max(c["margin"], 0)), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["mass", "club", "grocer", "dollar", "convenience", "online"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Grocery and mass retail: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        bj = 100 * g["BJ's"]["margin"]
        beat(self,
             "The whole industry in one picture, and notice the vertical scale: it stops at ten per cent, where most charts "
             "in this series run to thirty or more. "
             f"<bookmark mark='a'/> Walmart kept a median {100 * g['Walmart']['margin']:.1f} cents per dollar over five years, "
             f"Target {100 * g['Target']['margin']:.1f}. <bookmark mark='b'/> Costco {100 * g['Costco']['margin']:.1f}, BJ's "
             f"{bj:.1f}. <bookmark mark='c'/> The supermarkets, one to four: "
             f"Kroger {100 * g['Kroger']['margin']:.1f}, Albertsons {100 * g['Albertsons']['margin']:.1f}, Sprouts "
             f"{100 * g['Sprouts']['margin']:.1f}. <bookmark mark='d'/> The discounters, a little more, up to nine for "
             f"Ollie's. <bookmark mark='e'/> And Amazon, the largest by revenue, {100 * g['Amazon']['margin']:.1f}; Part 32 "
             "looks at where that profit comes from.",
             base=[pa, xl, hd, key, src],
             steps=[groups["mass"], groups["club"], groups["grocer"], VGroup(groups["dollar"], groups["convenience"]), groups["online"]])

    def map(self):
        cols = [("United States", MASS, ["Walmart", "Costco", "Kroger", "Albertsons", "Target", "Publix", "H-E-B", "Aldi US"]),
                ("Discount and dollar", DOLLAR, ["Dollar General", "Dollar Tree", "Aldi", "Lidl", "Five Below", "Ollie's"]),
                ("Europe", GROCER, ["Schwarz (Lidl, Kaufland)", "Aldi", "Tesco", "Carrefour", "Ahold Delhaize", "Edeka", "Rewe"]),
                ("Asia", ONLINE, ["Seven & i", "Aeon", "CR Vanguard", "Reliance Retail", "DMart", "Coupang"]),
                ("Clubs", CLUB, ["Costco", "Sam's Club", "BJ's", "PriceSmart"]),
                ("Online", ONLINE, ["Amazon", "Instacart", "Ocado", "Walmart.com"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Publix, H-E-B, Aldi, Lidl, Schwarz, Tesco, Carrefour, Ahold Delhaize, "
                  "Edeka, Rewe, Seven & i, Aeon, CR Vanguard, Reliance Retail, DMart, Coupang, Instacart and Ocado", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> America's big chains. <bookmark mark='b'/> The discounters, including Aldi "
             "and Lidl. <bookmark mark='c'/> "
             "Europe's grocers. <bookmark mark='d'/> Asia's, from Japan's convenience stores to India's new chains. "
             "<bookmark mark='e'/> The clubs. <bookmark mark='f'/> And the online grocers and delivery platforms.",
             base=[head("The map of the business"), note], steps=list(gr))
