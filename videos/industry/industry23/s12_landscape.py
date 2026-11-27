from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403

OFFSET = {"NIKE": UP, "TJX": UP, "LVMH": UP, "Hermès": UP, "Inditex (Zara)": UP, "Ross": DOWN, "Macy's": RIGHT,
          "Lululemon": RIGHT, "Deckers (HOKA, UGG)": UP, "Tapestry (Coach)": UP, "Birkenstock": UP, "Under Armour": DOWN,
          "PVH (Calvin Klein, Tommy Hilfiger)": LEFT}
SHORT = {"VF (The North Face, Vans)": "VF", "PVH (Calvin Klein, Tommy Hilfiger)": "PVH", "Deckers (HOKA, UGG)": "Deckers",
         "Tapestry (Coach)": "Tapestry"}
CALLOUT = {"Gap": (1.25, 0.065), "Kohl's": (1.32, -0.027), "Kering (Gucci)": (1.1, -0.035), "Burlington": (1.03, 0.078),
           "VF (The North Face, Vans)": (0.9, -0.03), "Ralph Lauren": (1.14, 0.112), "Levi Strauss": (0.6, 0.115)}
UNLABELLED = ("Abercrombie & Fitch", "American Eagle", "Urban Outfitters", "Signet", "Columbia", "On", "Capri (Michael Kors)")


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 10, "The landscape, November 2026", "Who sells the world's clothes, and who keeps the most?",
             "Chapter ten. The landscape, as of November 2026. Who sells the world's clothes, shoes and bags, and who keeps "
             "the most of what they charge?", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = np.log10
        pa = viz.plot_axes([0.3, 2.05], [-0.05, 0.32], x_length=10.0, y_length=4.9, xticks=[np.log10(3), 1, np.log10(30), 2],
                           yticks=[0, 0.1, 0.2, 0.3], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue (US: median of last five years; Europe: 2025)", size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0.3, 0), pa.ax.c2p(2.05, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest fiscal year, US dollars (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            nm = SHORT.get(c["name"], c["name"])
            if c["name"] in UNLABELLED:
                groups.setdefault(c["group"], VGroup()).add(Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col,
                                                                fill_opacity=0.6))
                continue
            if c["name"] in CALLOUT:
                groups.setdefault(c["group"], VGroup()).add(callout(pa.ax, lx(c["rev"]), c["margin"], nm, col, CALLOUT[c["name"]],
                                                                    size=12, radius=r))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(nm, 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("store", "fast fashion and chains"), ("off", "off-price"), ("dept", "department stores"),
                                    ("sport", "sport"), ("brand", "brands"), ("luxury", "luxury"))]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.95)
        hd = tx("Fashion and luxury: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        unl = tx("unlabelled: Abercrombie & Fitch, American Eagle, Urban Outfitters, Signet, Columbia, On, Capri", 11, GREY_B
                 ).move_to(pa.ax.c2p(0.33, 0.29), aligned_edge=LEFT)
        src = source("Forms 10-K and 20-F via SEC company facts; Inditex, Hermès, LVMH and Kering 2025 results, converted at "
                     f"2025's average of ${R['landscape']['eur']:.3f} per euro (Federal Reserve H.10 via FRED)", size=12)
        g = {c["name"]: c for c in C}
        beat(self,
             "Here is the industry in one picture: each company by its revenue and by what it kept of each dollar. "
             "<bookmark mark='a'/> The chains: Inditex, the largest, kept about "
             f"{100 * g['Inditex (Zara)']['margin']:.0f} cents in its last year; Gap, about {100 * g['Gap']['margin']:.0f}. "
             f"<bookmark mark='b'/> The off-price shops, TJX and Ross, about {100 * g['TJX']['margin']:.0f} and "
             f"{100 * g['Ross']['margin']:.0f} cents on large sales. <bookmark mark='c'/> The department stores, Macy's and "
             "Kohl's, about two. <bookmark mark='d'/> "
             f"The sports brands spread widely: Deckers {100 * g['Deckers (HOKA, UGG)']['margin']:.0f} cents, Lululemon "
             f"{100 * g['Lululemon']['margin']:.0f}, NIKE {100 * g['NIKE']['margin']:.0f}, Under Armour nothing. "
             "<bookmark mark='e'/> The brands, from Ralph Lauren's ten to VF's one. <bookmark mark='f'/> And luxury, the "
             f"widest of all: Hermès {100 * g['Hermès']['margin']:.0f} cents, LVMH {100 * g['LVMH']['margin']:.0f}, "
             f"Tapestry {100 * g['Tapestry (Coach)']['margin']:.0f}, and Kering, with Gucci falling, almost nothing in 2025. "
             "The highest margins and the lowest sit in the same corner of the industry: luxury pays very well while the "
             "name holds, and very badly when it does not.",
             base=[pa, zero, xl, hd, key, src, unl], steps=[groups["store"], groups["off"], groups["dept"], groups["sport"],
                                                       groups["brand"], groups["luxury"]])

    def map(self):
        cols = [("Fast fashion", FAST, ["Inditex (Zara)", "H&M", "Fast Retailing (Uniqlo)", "Shein", "Primark", "Gap"]),
                ("Luxury", LUX, ["LVMH", "Hermès", "Chanel", "Kering (Gucci)", "Richemont", "Prada", "Tapestry", "Capri"]),
                ("Sport", SPORT, ["NIKE", "adidas", "Anta", "Lululemon", "Puma", "Deckers", "On"]),
                ("Off-price", OFF, ["TJX", "Ross", "Burlington"]),
                ("Department stores", DEPT, ["Macy's", "Kohl's", "Nordstrom", "Selfridges"]),
                ("The makers", BAD, ["Shenzhou", "Pou Chen", "Crystal", "and thousands of others"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: H&M, Fast Retailing, Shein, Primark, Chanel, Richemont, "
                  "Prada, adidas, Anta, Puma, Nordstrom, Selfridges and the makers", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The fast-fashion chains, from Europe, Japan and China. "
             "<bookmark mark='b'/> The luxury houses, most of them European. <bookmark mark='c'/> The sports brands. "
             "<bookmark mark='d'/> The off-price shops. <bookmark mark='e'/> The department stores. <bookmark mark='f'/> And "
             "the makers: a few large contract manufacturers that make for many brands at once, and thousands of smaller "
             "ones. Many of these report outside America's securities regulator, or not at all, so this film shows them "
             "by name only.",
             base=[head("The map of the business"), note], steps=list(g))
