from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403

OFFSET = {"FedEx": DOWN, "UPS": UP, "ZTO Express": UP, "Union Pacific": UP, "BNSF": DOWN, "CPKC": UP, "CSX": RIGHT,
          "GXO": DOWN, "Norfolk Southern": DOWN, "J.B. Hunt": UP, "XPO": RIGHT, "TFI International": UP, "Knight-Swift": DOWN,
          "Schneider": UR, "RXO": DOWN, "Old Dominion": UP, "Landstar": UP, "ArcBest": UL, "Hub Group": DR, "Saia": UP,
          "Werner": DOWN, "Marten": UP, "Heartland": DOWN}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who carries America's freight, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: railways, parcel networks, truckers, part-load carriers, "
             "brokers and warehouses, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v) + 0.3
        pa = viz.plot_axes([0.0, 2.4], [-0.05, 0.35], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30), lx(100)],
                           yticks=[0, 0.1, 0.2, 0.3], xfmt=lambda v: f"{10 ** (v - 0.3):.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.4, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest year (log scale; CPKC in Canadian dollars, ZTO in yuan, $ for the rest)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.025 * np.sqrt(c["rev"] / 10)
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["rail", "parcel", "intermodal", "truckload", "ltl", "broker", "logistics"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Freight: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K, 40-F and 20-F via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        beat(self,
             "The whole industry in one picture. <bookmark mark='a'/> The railways sit at the top: Union Pacific kept a "
             f"median of {100 * g['Union Pacific']['margin']:.0f} cents of net profit per dollar over five years, CPKC "
             f"{100 * g['CPKC']['margin']:.0f}. <bookmark mark='b'/> The parcel giants are the largest by revenue, and keep "
             f"{100 * g['UPS']['margin']:.0f} and {100 * g['FedEx']['margin']:.0f} cents; China's ZTO Express keeps "
             f"{100 * g['ZTO Express']['margin']:.0f}. <bookmark mark='c'/> The truckers and brokers crowd the bottom, "
             f"between zero and six cents, <bookmark mark='d'/> except the part-load carriers with their buildings: Old "
             f"Dominion {100 * g['Old Dominion']['margin']:.0f}, Saia {100 * g['Saia']['margin']:.0f}. Size alone buys "
             "little here: FedEx is the largest company on the chart and keeps a fraction of what railways a quarter its "
             "size keep. What pays is owning the network others cannot copy.",
             base=[pa, zero, xl, hd, key, src],
             steps=[groups["rail"], groups["parcel"], VGroup(groups["intermodal"], groups["truckload"], groups["broker"], groups["logistics"]),
                    groups["ltl"]])

    def map(self):
        cols = [("Railways", RAIL, ["Union Pacific", "BNSF", "CSX", "Norfolk Southern", "CN", "CPKC", "Deutsche Bahn",
                                    "JR Freight", "China Railway", "Indian Railways"]),
                ("Parcels and posts", PARCEL, ["UPS", "FedEx", "DHL", "Amazon Logistics", "USPS", "SF Express", "ZTO Express",
                                                "Yamato", "Delhivery"]),
                ("Truckload", TRUCK, ["Knight-Swift", "J.B. Hunt", "Schneider", "Werner", "Heartland", "half a million others"]),
                ("Less than truckload", LTL, ["Old Dominion", "FedEx Freight", "XPO", "Saia", "Estes", "ArcBest", "TFI"]),
                ("Brokers and logistics", FUEL, ["C.H. Robinson", "RXO", "Landstar", "Uber Freight", "GXO", "DSV", "Kuehne+Nagel"]),
                ("Driverless", SKY, ["Aurora", "Kodiak", "Waabi"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: CN, Deutsche Bahn, JR Freight, China Railway, Indian Railways, "
                  "DHL, Amazon Logistics, SF Express, Yamato, Delhivery, Estes, Uber Freight, DSV, Kuehne+Nagel, Kodiak and Waabi", 13,
                  GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The railways of North America, Europe and Asia. <bookmark mark='b'/> The parcel networks and the posts. <bookmark mark='c'/> The truckload "
             "carriers, and half a million smaller ones. <bookmark mark='d'/> The part-load networks. <bookmark mark='e'/> "
             "The brokers and warehouse operators, who own few trucks and sell the matching of loads. <bookmark mark='f'/> "
             "And the companies trying to take the driver out.",
             base=[head("The map of the business"), note], steps=list(gr))
