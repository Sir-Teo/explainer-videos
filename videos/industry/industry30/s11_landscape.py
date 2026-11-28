from __future__ import annotations

from videos.industry.industry30.common import *  # noqa: F403

OFFSET = {"Verizon": UR, "AT&T": DOWN, "Comcast": UL, "T-Mobile": DOWN, "Charter": DOWN, "Telefónica": UR, "Vodafone": DOWN,
          "BCE": UP, "Rogers": DOWN, "Telus": DOWN, "Nokia": UP, "EchoStar": DOWN, "Lumen": DOWN, "American Tower": UP,
          "Frontier": DOWN, "Millicom": UP, "Viasat": DOWN, "Crown Castle": UP, "SBA": UP, "Cable One": UP, "TDS": DOWN,
          "Iridium": DOWN}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who carries the world's calls and data, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: carriers, cable companies, tower owners, satellite firms "
             "and equipment makers, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.europe()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v) + 0.2
        pa = viz.plot_axes([0.0, 2.6], [-0.1, 0.3], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30), lx(100)],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3], xfmt=lambda v: f"{10 ** (v - 0.2):.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.6, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest year (log scale; euros for Vodafone, Telefónica and Nokia, Canadian dollars for BCE, Rogers and Telus)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        if xl.width > 12:
            xl.scale_to_fit_width(12)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.025 * np.sqrt(c["rev"] / 10)
            d = Dot(pa.ax.c2p(lx(c["rev"]), max(c["margin"], -0.1)), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["wireless", "cable", "wireline", "towers", "satellite", "foreign", "equipment"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Telecoms: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K, 20-F and 40-F via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        beat(self,
             "The industry in one picture. <bookmark mark='a'/> The American carriers and cable companies are the giants, "
             f"keeping nine to thirteen cents of net profit per dollar: Verizon {100 * g['Verizon']['margin']:.0f}, AT&T "
             f"{100 * g['AT&T']['margin']:.0f}, Comcast {100 * g['Comcast']['margin']:.0f}. <bookmark mark='b'/> Those "
             "selling copper or bidding for a fourth network lost money: Lumen, Frontier, EchoStar. "
             "<bookmark mark='c'/> The tower owners keep the most: American Tower "
             f"{100 * g['American Tower']['margin']:.0f}, SBA {100 * g['SBA']['margin']:.0f}. <bookmark mark='d'/> Europe's "
             f"carriers keep less: Vodafone {100 * g['Vodafone']['margin']:.0f}, Telefónica "
             f"{100 * g['Telefónica']['margin']:.0f}.",
             base=[pa, zero, xl, hd, key, src],
             steps=[VGroup(groups["wireless"], groups["cable"]), VGroup(groups["wireline"], groups["satellite"]), groups["towers"],
                    VGroup(groups["foreign"], groups["equipment"])])

    def europe(self):
        V = R["landscape"]["vod"]
        items = [(f"fiscal {y}", v, FOREIGN, f"EUR {v:.1f}bn") for y, v in V.items()]
        rows = hbars(items, max_value=55, x0=0.0, top=1.4, row=0.9, length=5.6, size=17, bar_h=0.45)
        lab = tx("Vodafone: revenue, years to March", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Vodafone Group, Forms 20-F via SEC company facts", size=12)
        beat(self,
             f"Europe shows where the American story could go. <bookmark mark='a'/> Vodafone took in {list(V.values())[0]:.1f} billion euros in its year to March 2016 "
             f"<bookmark mark='b'/> and {list(V.values())[-1]:.1f} billion in its year to March 2025, with a loss. In this "
             "series' reading, Europe's carriers sell into many small national markets, each with several networks, and "
             "have little of the scale the American three enjoy.",
             base=[rows.axis, lab, src], steps=[rows[0], VGroup(*rows[1:])])

    def map(self):
        cols = [("United States", WIRELESS, ["Verizon", "AT&T", "T-Mobile", "Comcast", "Charter", "Lumen"]),
                ("Europe", FOREIGN, ["Deutsche Telekom", "Vodafone", "Orange", "Telefónica", "BT"]),
                ("Asia", CABLE, ["China Mobile", "NTT", "KDDI", "SoftBank", "SK Telecom", "KT", "Reliance Jio", "Bharti Airtel"]),
                ("Americas", GOOD, ["América Móvil", "BCE", "Rogers", "Telus", "Millicom"]),
                ("Towers", TOWER, ["American Tower", "Crown Castle", "SBA", "Cellnex", "China Tower", "Indus"]),
                ("Equipment and satellites", EQUIP, ["Huawei", "Ericsson", "Nokia", "Samsung", "SpaceX (Starlink)", "Iridium", "Viasat"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Deutsche Telekom, Orange, BT, China Mobile, NTT, KDDI, SoftBank, "
                  "Reliance Jio, Bharti Airtel, Cellnex, China Tower, Indus, Huawei, Samsung and SpaceX", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> America's carriers and cable companies. <bookmark mark='b'/> Europe's, "
             "many of them, one or more in every country. <bookmark mark='c'/> Asia's. <bookmark mark='d'/> The rest of the Americas. <bookmark mark='e'/> The tower owners. "
             "<bookmark mark='f'/> And the equipment makers and satellite operators, including the rocket company now "
             "buying spectrum.",
             base=[head("The map of the business"), note], steps=list(gr))
