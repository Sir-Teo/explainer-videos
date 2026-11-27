from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403

OFFSET = {"Quanta Services": UP, "CRH": UP, "United Rentals": UP, "EMCOR": DOWN, "Jacobs": UP, "Eagle Materials": UP,
          "Martin Marietta": UP, "Vulcan Materials": UP, "Tutor Perini": DOWN, "Herc": RIGHT, "Argan": UP, "Sterling": UP}
CALLOUT = {"Fluor": (1.42, -0.03), "MasTec": (1.12, -0.035), "AECOM": (1.42, 0.012), "Ferrovial": (1.1, 0.095),
           "Comfort Systems": (0.98, 0.084), "KBR": (1.03, 0.04), "Primoris": (0.84, -0.022), "APi Group": (1.0, 0.008),
           "Tetra Tech": (0.53, 0.09), "Dycom": (0.6, 0.053), "MYR Group": (0.4, 0.014), "Granite": (0.5, -0.022),
           "Construction Partners": (0.33, 0.045)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who builds, who supplies, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026. The builders, the engineers, the suppliers and the "
             "owners, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = np.log10
        pa = viz.plot_axes([-0.2, 1.7], [-0.06, 0.22], x_length=10.0, y_length=4.9, xticks=[0, np.log10(3), 1, np.log10(30)],
                           yticks=[-0.05, 0, 0.05, 0.1, 0.15, 0.2], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of the last five years", size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(-0.2, 0), pa.ax.c2p(1.7, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest fiscal year, US dollars (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
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
                       for g in ("general", "trade", "engineer", "materials", "rental", "concession")]).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.95)
        hd = tx("Construction: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F via SEC company facts (Ferrovial in euros at 2025's average rate)", size=12)
        g = {c["name"]: c for c in C}
        beat(self,
             "Here is the industry in one picture. <bookmark mark='a'/> The general contractors, who take on whole "
             f"projects, sit low: Fluor about {100 * g['Fluor']['margin']:.0f} cent, Granite two, Tutor Perini below zero. "
             f"<bookmark mark='b'/> The specialty contractors are larger than you might expect: Quanta, with "
             f"{g['Quanta Services']['rev']:.0f} billion dollars of revenue, keeps about {100 * g['Quanta Services']['margin']:.0f} "
             f"cents; EMCOR {100 * g['EMCOR']['margin']:.0f}; Comfort Systems {100 * g['Comfort Systems']['margin']:.0f}. "
             f"<bookmark mark='c'/> The engineers, Jacobs and AECOM, between two and six. <bookmark mark='d'/> The "
             f"materials companies sit high: Martin Marietta {100 * g['Martin Marietta']['margin']:.0f}, Eagle "
             f"{100 * g['Eagle Materials']['margin']:.0f}. <bookmark mark='e'/> The equipment renters too: United Rentals "
             f"{100 * g['United Rentals']['margin']:.0f}. <bookmark mark='f'/> And Ferrovial, half builder and half "
             f"owner, {100 * g['Ferrovial']['margin']:.0f}. Owning the stone, the machines or the road pays; doing the "
             "work pays least.",
             base=[pa, zero, xl, hd, key, src], steps=[groups["general"], groups["trade"], groups["engineer"], groups["materials"],
                                                       groups["rental"], groups["concession"]])

    def map(self):
        cols = [("Contractors", GROUP_COL["general"], ["Vinci", "Bouygues", "ACS (Hochtief, Turner)", "Skanska", "Bechtel", "Fluor",
                                                       "Kiewit"]),
                ("China and Asia", BAD, ["China State Construction", "China Railway Group", "China Railway Construction",
                                         "Larsen & Toubro", "Kajima", "Obayashi"]),
                ("Engineers", GROUP_COL["engineer"], ["Jacobs", "AECOM", "WSP", "AtkinsRealis", "Arcadis"]),
                ("Specialty", GROUP_COL["trade"], ["Quanta", "EMCOR", "Comfort Systems", "MasTec"]),
                ("Materials and rental", GROUP_COL["materials"], ["CRH", "Holcim", "Heidelberg Materials", "Vulcan",
                                                                  "United Rentals", "Ashtead (Sunbelt)"]),
                ("Owners", GROUP_COL["concession"], ["Vinci Autoroutes", "Ferrovial", "Transurban", "Brookfield"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Vinci, Bouygues, ACS, Skanska, Bechtel, Kiewit, the Chinese "
                  "and Japanese builders, Larsen & Toubro, WSP, AtkinsRealis, Arcadis, Holcim, Heidelberg Materials, Ashtead, "
                  "Transurban and Brookfield", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The big contractors, most of them European, and America's private ones. "
             "<bookmark mark='b'/> China's state builders and the other Asian giants. <bookmark mark='c'/> The engineering "
             "firms. <bookmark mark='d'/> The specialty contractors. <bookmark mark='e'/> The materials and rental "
             "companies. <bookmark mark='f'/> And the owners of roads and other infrastructure. Many of these report "
             "outside America's securities regulator, or are privately owned, so this film shows them by name only.",
             base=[head("The map of the business"), note], steps=list(g))
