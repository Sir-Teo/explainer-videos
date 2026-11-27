from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403

OFFSET = {"Maersk": UP, "C.H. Robinson": DOWN, "Expeditors": UP, "ZIM": UP, "Kirby": DOWN, "Matson": UP, "Frontline": DOWN,
          "Danaos": UP, "Global Ship Lease": LEFT, "Costamare": UP, "Star Bulk": DOWN, "Scorpio Tankers": UP, "TORM": DOWN,
          "International Seaways": DOWN, "Nordic American": DOWN, "Flex LNG": UP, "Genco": DOWN, "Diana": DOWN, "SFL": DOWN}
UNLABELLED = ("Navios Partners", "Teekay Tankers", "DHT", "Costamare", "Scorpio Tankers", "International Seaways")


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who carries, rents and books the most, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026. The container lines, the shipowners, the tankers, the bulk "
             "carriers and the forwarders, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v) + 1.0
        pa = viz.plot_axes([0.0, 3.0], [-0.1, 0.65], x_length=10.0, y_length=4.9, xticks=[lx(0.3), lx(1), lx(3), lx(10), lx(30)],
                           yticks=[0, 0.2, 0.4, 0.6], xfmt=lambda v: f"${10 ** (v - 1.0):.1f}bn" if v < 1 else f"${10 ** (v - 1.0):.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(3.0, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, 2025 (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            if c["name"] in UNLABELLED:
                groups.setdefault(c["group"], VGroup()).add(Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.55))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            name = c["name"] + (" (operating)" if c.get("ebit") else "")
            lab = tx(name, 11, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["liner", "lessor", "tanker", "bulk", "gas", "forwarder", "barge"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Shipping: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F via SEC company facts; Maersk's annual reports (operating profit, EBIT)", size=12)
        un = tx("Unlabelled: " + ", ".join(UNLABELLED), 11, GREY_B).to_edge(DOWN, buff=0.08)
        g = {c["name"]: c for c in C}
        steps = [groups["liner"], groups["lessor"], VGroup(groups["tanker"], groups["bulk"], groups["gas"]),
                 VGroup(groups["forwarder"], groups["barge"])]
        beat(self,
             "Here is the industry in one picture, over the five years to 2025. <bookmark mark='a'/> The container lines: "
             f"Maersk, the largest here, kept about {100 * g['Maersk']['margin']:.0f} cents of operating profit on each dollar; "
             f"ZIM {100 * g['ZIM']['margin']:.0f} cents of net income, a median of booms and a bust; Matson, behind the Jones "
             f"Act, {100 * g['Matson']['margin']:.0f}. <bookmark mark='b'/> The container ship lessors near the top: Danaos "
             f"{100 * g['Danaos']['margin']:.0f}, Global Ship Lease {100 * g['Global Ship Lease']['margin']:.0f}. "
             "<bookmark mark='c'/> The tanker, bulk and gas carriers, between about five and forty-five, depending on when "
             "their booms fell. <bookmark mark='d'/> And the forwarders, large in revenue and thin in margin: C.H. Robinson "
             f"{100 * g['C.H. Robinson']['margin']:.0f}, Expeditors {100 * g['Expeditors']['margin']:.0f}.",
             base=[pa, zero, xl, hd, key, src, un], steps=steps)

    def map(self):
        cols = [("Container lines", GROUP_COL["liner"], ["MSC", "Maersk", "CMA CGM", "COSCO", "Hapag-Lloyd", "ONE", "Evergreen", "ZIM"]),
                ("Ship lessors", GROUP_COL["lessor"], ["Danaos", "Global Ship Lease", "Costamare", "Seaspan", "Chinese leasing houses"]),
                ("Tankers and bulk", GROUP_COL["tanker"], ["Frontline", "Scorpio", "International Seaways", "Star Bulk", "Greek family owners"]),
                ("Shipyards", GROUP_COL["gas"], ["CSSC", "HD Hyundai", "Hanwha Ocean", "Samsung Heavy", "Imabari"]),
                ("Ports", PORT, ["PSA", "Hutchison Ports", "DP World", "APM Terminals", "Adani Ports"]),
                ("Forwarders", GROUP_COL["forwarder"], ["DSV", "Kuehne+Nagel", "Expeditors", "C.H. Robinson"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: MSC, CMA CGM, COSCO, Hapag-Lloyd, ONE, Evergreen, Seaspan, "
                  "the Chinese leasing houses and Greek family owners, the shipyards, the port operators, DSV and Kuehne+Nagel",
                  13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The container lines, most of them private or listed outside America. "
             "<bookmark mark='b'/> The lessors who own the ships the lines rent. <bookmark mark='c'/> The tanker and bulk "
             "owners. <bookmark mark='d'/> The shipyards, in China, South Korea and Japan. <bookmark mark='e'/> The terminal "
             "operators. <bookmark mark='f'/> And the forwarders. Many of these report outside America's securities regulator, "
             "so this film shows them by name only.",
             base=[head("The map of the business"), note], steps=list(gr))
