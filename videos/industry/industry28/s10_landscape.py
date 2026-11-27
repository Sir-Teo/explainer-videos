from __future__ import annotations

from videos.industry.industry28.common import *  # noqa: F403

OFFSET = {"Delta": UP, "United": DOWN, "American": DOWN, "Southwest": DOWN, "LATAM": UP, "Alaska": DOWN, "Ryanair": UP,
          "JetBlue": DOWN, "AerCap": UP, "SkyWest": UP, "Frontier": DOWN, "Copa": UP, "Air Lease": UP, "Sabre": DOWN,
          "Allegiant": UP}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 8, "The landscape, November 2026", "Who flies, who rents and who keeps the most?",
             "Chapter eight. The landscape, as of November 2026. America's airlines, three from abroad, the lessors and a "
             "booking system, by size and by what they keep.", lit=("moat", "change"))
        self.four()
        self.scatter()
        self.map()

    def four(self):
        L = R["landscape"]
        items = [(n, v, SKY if i < 4 else FUEL, f"${v:.1f}bn") for i, (n, v) in enumerate(L["us_rev"])]
        rows = hbars(items, max_value=66, x0=-0.6, top=2.2, row=0.58, length=6.4, size=16, bar_h=0.34)
        lab = tx("revenue, 2025: America's listed airlines that sell their own tickets", 17, GREY_A).to_edge(UP, buff=0.6)
        tot = tx(f"the four largest: {100 * L['top4']:.0f}% of the eight's revenue", 19, SKY, bold=True).to_edge(DOWN, buff=0.9)
        src = source("Forms 10-K via SEC company facts; Alaska Air Group, Form 10-K for 2025; Spirit filed no 2025 revenue in this form; SkyWest flies for the majors", size=12)
        beat(self,
             "First, who is big. <bookmark mark='a'/> Four airlines dominate America: Delta, United, American and "
             f"Southwest. <bookmark mark='b'/> Then Alaska, which bought Hawaiian, JetBlue, Frontier and Allegiant. "
             f"<bookmark mark='c'/> Of the revenue of these eight, the four largest took {100 * L['top4']:.0f} per cent in "
             "2025. Alaska's purchase of Hawaiian, in 2024, was only the latest of the mergers that have left a few airlines "
             "with most of America's flying.",
             base=[rows.axis, lab, src], steps=[VGroup(*rows[:4]), VGroup(*rows[4:]), tot])

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v) + 0.5
        pa = viz.plot_axes([0.0, 2.5], [-0.2, 0.3], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30), lx(60)],
                           yticks=[-0.2, -0.1, 0, 0.1, 0.2, 0.3], xfmt=lambda v: f"${10 ** (v - 0.5):.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(2.5, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest year (log scale; Ryanair in euros)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["network", "lowcost", "ulcc", "regional", "foreign", "lessor", "systems"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Airlines: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F via SEC company facts; Spirit's filed net income is mis-scaled and left out", size=12)
        g = {c["name"]: c for c in C}
        steps = [groups["network"], VGroup(groups["lowcost"], groups["ulcc"], groups["regional"]), groups["foreign"],
                 VGroup(groups["lessor"], groups["systems"])]
        beat(self,
             "Here is the industry in one picture, over five years that included the pandemic's tail. <bookmark mark='a'/> "
             f"The big American network airlines: Delta about {100 * g['Delta']['margin']:.0f} cents of each dollar, United "
             f"{100 * g['United']['margin']:.0f}, American close to zero. <bookmark mark='b'/> The low-cost and "
             f"ultra-low-cost carriers around or below zero: JetBlue {100 * g['JetBlue']['margin']:.0f}, Frontier "
             f"{100 * g['Frontier']['margin']:.0f}. <bookmark mark='c'/> From abroad, Copa "
             f"{100 * g['Copa']['margin']:.0f} and Ryanair {100 * g['Ryanair']['margin']:.0f}, well above the American "
             "carriers. <bookmark mark='d'/> And the lessors at the top: AerCap "
             f"{100 * g['AerCap']['margin']:.0f}, Air Lease {100 * g['Air Lease']['margin']:.0f}.",
             base=[pa, zero, xl, hd, key, src], steps=steps)

    def map(self):
        cols = [("Network airlines", GROUP_COL["network"], ["Delta", "United", "American", "Lufthansa", "IAG", "Air France-KLM",
                                                            "China's big three", "Emirates", "Qatar", "Turkish"]),
                ("Low-cost", GROUP_COL["lowcost"], ["Southwest", "Ryanair", "easyJet", "IndiGo", "AirAsia", "JetBlue"]),
                ("Ultra-low-cost", GROUP_COL["ulcc"], ["Spirit", "Frontier", "Allegiant", "Wizz Air"]),
                ("Lessors", GROUP_COL["lessor"], ["AerCap", "Air Lease", "SMBC Aviation Capital", "BOC Aviation"]),
                ("Airports", GROUP_COL["foreign"], ["Aena", "Fraport", "Heathrow", "ADP"]),
                ("Booking systems", GROUP_COL["systems"], ["Amadeus", "Sabre", "Travelport"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Lufthansa, IAG, Air France-KLM, the Chinese airlines, Emirates, "
                  "Qatar, Turkish, easyJet, IndiGo, AirAsia, Wizz Air, SMBC, BOC Aviation, the airports, Amadeus and Travelport", 13,
                  GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The network airlines of America, Europe, China and the Gulf. "
             "<bookmark mark='b'/> The low-cost airlines. <bookmark mark='c'/> The ultra-low-cost ones. <bookmark mark='d'/> "
             "The lessors. <bookmark mark='e'/> The airports. <bookmark mark='f'/> And the booking systems through which agents sell seats. Many of these report outside "
             "America's securities regulator, so this film shows them by name only. Around the world the pattern of this film "
             "repeats: a few large network airlines in each country, low-cost challengers on the short routes, and the "
             "lessors, airports and booking systems taking their share from all of them.",
             base=[head("The map of the business"), note], steps=list(gr))
