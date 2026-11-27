from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403

OFFSET = {"Home Depot": UP, "Lowe's": UP, "Lennar": DOWN, "D.R. Horton": UP, "Builders FirstSource": DOWN, "NVR": UP,
          "PulteGroup": UP, "Toll Brothers": DOWN, "Invitation Homes": UP, "Opendoor": DOWN, "Compass": DOWN, "Zillow": UP,
          "UWM": DOWN}
CALLOUT = {"KB Home": (0.55, 0.115), "M/I Homes": (0.45, 0.15), "Century Communities": (0.4, 0.05), "Dream Finders": (0.8, 0.045),
           "LGI Homes": (0.05, 0.12), "Cavco": (0.15, 0.04), "Champion Homes": (0.3, 0.02)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 8, "The landscape, November 2026", "Who builds, lends, sells and keeps the most?",
             "Chapter eight. The landscape, as of November 2026. The builders, the suppliers, the lenders and the brokers, "
             "by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = np.log10
        pa = viz.plot_axes([0.0, 2.35], [-0.1, 0.2], x_length=10.0, y_length=4.9, xticks=[np.log10(2), 1, np.log10(30), 2],
                           yticks=[-0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2], xfmt=lambda v: f"${10 ** v:.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.35, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            if c["name"] in CALLOUT:
                groups.setdefault(c["group"], VGroup()).add(callout(pa.ax, lx(c["rev"]), c["margin"], c["name"], col,
                                                                    CALLOUT[c["name"]], size=12, radius=r))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(GROUP_NAME[g], 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g in ("builder", "factory", "supply", "landlord", "mortgage", "broker")]).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.95)
        hd = tx("Homes: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        beat(self,
             "Here is the industry in one picture. <bookmark mark='a'/> The builders sit high: PulteGroup and NVR kept "
             f"about {100 * g['PulteGroup']['margin']:.0f} cents of each dollar over the last five years, D.R. Horton "
             f"{100 * g['D.R. Horton']['margin']:.0f}, Lennar {100 * g['Lennar']['margin']:.0f}, in years that began with a "
             "boom. <bookmark mark='b'/> The factory-built home makers, about eight or nine. <bookmark mark='c'/> The "
             f"suppliers and the stores, Home Depot the giant at {g['Home Depot']['rev']:.0f} billion dollars of revenue and "
             f"about {100 * g['Home Depot']['margin']:.0f} cents. <bookmark mark='d'/> The landlord, Invitation Homes, "
             f"{100 * g['Invitation Homes']['margin']:.0f}. <bookmark mark='e'/> A mortgage lender, UWM, about one. "
             "<bookmark mark='f'/> And the brokers and portals below zero. The money is with whoever holds the land, the "
             "shelves or the houses; the middlemen of the sale keep least.",
             base=[pa, zero, xl, hd, key, src], steps=[groups["builder"], groups["factory"], groups["supply"], groups["landlord"],
                                                       groups["mortgage"], groups["broker"]])

    def map(self):
        cols = [("Builders", GROUP_COL["builder"], ["D.R. Horton", "Lennar", "PulteGroup", "NVR", "Barratt Redrow", "Sekisui House",
                                                    "Vanke", "China Overseas Land"]),
                ("Land and supplies", GROUP_COL["supply"], ["Forestar", "Millrose", "Builders FirstSource", "Home Depot", "Lowe's"]),
                ("Mortgages", GROUP_COL["mortgage"], ["Fannie Mae", "Freddie Mac", "Ginnie Mae", "Rocket", "UWM", "the banks"]),
                ("Brokers and portals", GROUP_COL["broker"], ["Compass", "Zillow", "eXp", "Rightmove", "KE Holdings"]),
                ("Landlords", GROUP_COL["landlord"], ["Invitation Homes", "American Homes 4 Rent", "Vonovia"]),
                ("Factory-built", GROUP_COL["factory"], ["Clayton (Berkshire)", "Cavco", "Champion"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Barratt Redrow, Sekisui House, Vanke, China Overseas Land, "
                  "Freddie Mac, Ginnie Mae, Rocket, the banks, eXp, Rightmove, KE Holdings, American Homes 4 Rent, Vonovia and "
                  "Clayton", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The builders, American, British, Japanese and Chinese. "
             "<bookmark mark='b'/> The land companies and the suppliers. <bookmark mark='c'/> The mortgage system, with its "
             "three government-backed guarantors. <bookmark mark='d'/> The brokers and the listing portals. "
             "<bookmark mark='e'/> The landlords. <bookmark mark='f'/> And the factory-built home makers. Many of these "
             "report outside America's securities regulator, so this film shows them by name only.",
             base=[head("The map of the business"), note], steps=list(g))
