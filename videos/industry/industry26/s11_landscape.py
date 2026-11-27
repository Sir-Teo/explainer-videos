from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403

OFFSET = {"CBRE": UP, "JLL": UP, "Blackstone": UP, "Welltower": DOWN, "American Tower": UP, "Equinix": UP, "Prologis": UP,
          "Simon": UP, "Public Storage": UP, "Realty Income": DOWN, "BXP": DOWN, "Macerich": RIGHT, "SL Green": RIGHT,
          "Hudson Pacific": LEFT, "Cushman & Wakefield": DOWN, "Ventas": DOWN, "Digital Realty": UP, "AvalonBay": UP,
          "Crown Castle": DOWN, "Alexandria": UP, "Vornado": DOWN, "EastGroup": UP}
UNLABELLED = ("Rexford", "Regency", "Federal Realty", "Kilroy", "Douglas Emmett", "Kimco", "MAA", "Starwood Property", "SBA",
              "Equity Residential", "Extra Space")


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who owns, lends and earns the most?",
             "Chapter nine. The landscape, as of November 2026. The owners of each kind of building, the managers, the "
             "services firms and a lender, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        def lx(v):
            return np.log10(v) + 0.3
        pa = viz.plot_axes([0.0, 2.0], [-0.25, 0.5], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30)],
                           yticks=[-0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5], xfmt=lambda v: f"${10 ** (v - 0.3):.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.0, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, 2025 (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        order = ["industrial", "storage", "retail", "homes", "towers", "data", "health", "office", "manager", "services", "lender"]
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            if c["name"] in UNLABELLED:
                groups.setdefault(c["group"], VGroup()).add(Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col,
                                                                fill_opacity=0.55))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 11, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order]).arrange(RIGHT, buff=0.22).to_edge(UP, buff=0.95)
        if key.width > 13.2:
            key.scale_to_fit_width(13.2)
        hd = tx("Property: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts", size=12)
        un = tx("Unlabelled: " + ", ".join(UNLABELLED), 11, GREY_B).to_edge(DOWN, buff=0.08)
        if un.width > 13:
            un.scale_to_fit_width(13)
        g = {c["name"]: c for c in C}
        steps = [VGroup(groups["industrial"], groups["storage"]), VGroup(groups["retail"], groups["homes"]),
                 VGroup(groups["towers"], groups["data"], groups["health"]), groups["office"],
                 VGroup(groups["manager"], groups["services"], groups["lender"])]
        beat(self,
             "Here is the industry in one picture. <bookmark mark='a'/> The warehouse and storage landlords sit at the top: "
             f"Prologis kept about {100 * g['Prologis']['margin']:.0f} cents of each dollar over five years, Public Storage "
             f"{100 * g['Public Storage']['margin']:.0f}. <bookmark mark='b'/> Shops and flats in the twenties and thirties, "
             f"Simon higher with its gains. <bookmark mark='c'/> Towers about twenty, data centres and senior housing lower, "
             "running businesses inside their buildings. <bookmark mark='d'/> The offices spread from a little above zero to "
             f"well below it: Hudson Pacific {100 * g['Hudson Pacific']['margin']:.0f}, SL Green "
             f"{100 * g['SL Green']['margin']:.0f}. <bookmark mark='e'/> And at the right, the biggest by revenue and the "
             f"thinnest: CBRE and JLL at about three cents, with Blackstone, which earns fees on other people's buildings, at "
             f"{100 * g['Blackstone']['margin']:.0f}.",
             base=[pa, zero, xl, hd, key, src, un], steps=steps)

    def map(self):
        cols = [("Warehouses", GROUP_COL["industrial"], ["Prologis", "Rexford", "EastGroup", "Goodman", "GLP", "Segro"]),
                ("Offices", GROUP_COL["office"], ["BXP", "Vornado", "SL Green", "Mitsui Fudosan", "Mitsubishi Estate", "Brookfield"]),
                ("Shops", GROUP_COL["retail"], ["Simon", "Realty Income", "Kimco", "Unibail-Rodamco-Westfield", "Link REIT", "Scentre"]),
                ("Towers and data", GROUP_COL["data"], ["American Tower", "Crown Castle", "Equinix", "Digital Realty", "Cellnex"]),
                ("Homes, storage, care", GROUP_COL["homes"], ["AvalonBay", "Equity Residential", "Public Storage", "Welltower",
                                                              "Vonovia", "Sun Hung Kai"]),
                ("Money and services", GROUP_COL["manager"], ["Blackstone", "Brookfield", "Starwood", "CBRE", "JLL",
                                                              "Cushman & Wakefield"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Goodman, GLP, Segro, Mitsui Fudosan, Mitsubishi Estate, "
                  "Brookfield, Unibail-Rodamco-Westfield, Link REIT, Scentre, Cellnex, Vonovia and Sun Hung Kai", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The warehouse owners, American, Australian, Asian and British. "
             "<bookmark mark='b'/> The office owners, in New York, Tokyo and Toronto. <bookmark mark='c'/> The shopping "
             "centres, from Simon to Westfield and Hong Kong's Link. <bookmark mark='d'/> Towers and data centres. "
             "<bookmark mark='e'/> Flats, storage and care homes. <bookmark mark='f'/> And the money and services around them. "
             "Many of these report outside America's securities regulator, so this film shows them by name only.",
             base=[head("The map of the business"), note], steps=list(g))
