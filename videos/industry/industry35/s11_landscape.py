from __future__ import annotations

from videos.industry.industry35.common import *  # noqa: F403

OFFSET = {"Carnival": DOWN, "Marriott": UP, "Royal Caribbean": DOWN, "MGM Resorts": RIGHT, "Flutter": DOWN, "Expedia": LEFT,
          "Las Vegas Sands": UP, "Airbnb": UP, "Hilton": DOWN, "Caesars": DOWN, "Norwegian": DOWN, "Trip.com": DOWN,
          "Hyatt": LEFT, "Wynn": RIGHT, "Host Hotels": RIGHT, "DraftKings": RIGHT, "IHG": LEFT, "Marriott Vacations": LEFT,
          "Hilton Grand Vacations": RIGHT, "H World": DOWN, "Six Flags": RIGHT, "Sabre": RIGHT, "Ryman": LEFT,
          "Park Hotels": LEFT, "Tripadvisor": LEFT, "United Parks": UP, "Choice": UP, "Wyndham": LEFT, "Atour": RIGHT,
          "Apple Hospitality": DOWN, "MakeMyTrip": LEFT, "Booking": UP}
FLOOR = -0.08


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who owns the rooms, who sells them, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: hotel brands, hotel owners, online agents, cruise lines, "
             "casinos and parks, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.profits()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([-0.1, 1.55], [FLOOR - 0.01, 0.3], x_length=10.0, y_length=4.9,
                           xticks=[lx(1), lx(2), lx(5), lx(10), lx(20)], yticks=[0, 0.1, 0.2, 0.3],
                           xfmt=lambda v: f"${10 ** v:g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of the last five years", size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 2)
            y = max(c["margin"], FLOOR)
            d = Dot(pa.ax.c2p(lx(max(c["rev"], 0.9)), y), radius=r, color=col, fill_opacity=0.85)
            name = c["name"] if c["margin"] >= FLOOR else f"{c['name']} ({100 * c['margin']:.0f}%)"
            lab = tx(name, 11, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.05)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["brand", "owner", "agent", "cruise", "casino", "park"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Travel: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        zero = DashedLine(pa.ax.c2p(-0.1, 0), pa.ax.c2p(1.55, 0), color=GREY_B, stroke_width=1.5)
        src = source("Forms 10-K and 20-F via SEC company facts (yuan at the Federal Reserve's annual average rate)", size=12)
        g = {c["name"]: c for c in C}
        pc = lambda n: 100 * g[n]["margin"]  # noqa: E731
        beat(self,
             "The whole industry in one picture. <bookmark mark='a'/> The hotel brands sit high: Choice kept a median "
             f"{pc('Choice'):.0f} cents of each dollar over five years, Wyndham {pc('Wyndham'):.0f}, IHG {pc('IHG'):.0f}, "
             f"Hilton {pc('Hilton'):.0f} and Marriott {pc('Marriott'):.0f}, the last two held down by the reimbursed payroll in "
             f"their revenue. <bookmark mark='b'/> The owners: Host {pc('Host Hotels'):.0f}, level with Hilton on this measure, "
             "though it needs far more assets for each dollar of revenue, as chapter four showed; "
             f"Park {pc('Park Hotels'):.0f}. "
             f"<bookmark mark='c'/> The online agents span the chart: Booking {pc('Booking'):.0f}, Airbnb {pc('Airbnb'):.0f}, "
             f"Trip.com {pc('Trip.com'):.0f}, but Expedia {pc('Expedia'):.0f} and Tripadvisor next to nothing. "
             "<bookmark mark='d'/> The cruise lines, large, with five years that include the pandemic's losses. "
             "<bookmark mark='e'/> The casino "
             "companies, from Las Vegas Sands at the top to the online bookmakers still below the line. "
             "<bookmark mark='f'/> And the parks and timeshare companies in between.",
             base=[pa, xl, hd, key, zero, src],
             steps=[groups["brand"], groups["owner"], groups["agent"], groups["cruise"], groups["casino"], groups["park"]])

    def profits(self):
        C = {c["name"]: c for c in R["landscape"]["companies"]}
        names = ["Booking", "Airbnb", "Marriott", "Royal Caribbean", "Trip.com", "Las Vegas Sands", "Hilton", "Host Hotels", "Carnival"]
        items = []
        for n in names:
            c = C[n]
            v = c["rev"] * c["margin"]
            items.append((n, v, GROUP_COL[c["group"]], f"{'-' if v < 0 else ''}${abs(v):.1f}bn"))
        rows = hbars(items, max_value=7, x0=-0.2, top=2.4, row=0.56, length=6.0, size=15, bar_h=0.33)
        hd = tx("Revenue times its five-year median margin, $bn: a typical year's profit", 20, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("Forms 10-K and 20-F via SEC company facts; this series' calculation", size=12)
        beat(self,
             "Count it in dollars. <bookmark mark='a'/> On a typical year's margin, Booking earns about "
             f"{items[0][1]:.1f} billion dollars: the biggest profit in travel belongs to the company that owns no rooms, no "
             f"ships and no planes. <bookmark mark='b'/> Airbnb about {items[1][1]:.1f} billion and Marriott "
             f"{items[2][1]:.1f}. <bookmark mark='c'/> Then Royal Caribbean, the Chinese agent Trip.com, the casinos and the "
             "rest; Carnival's median year is still a small loss. The middle of the market, where the traveller is found, earns more than the buildings.",
             base=[rows.axis, hd, src], steps=[rows[0], VGroup(rows[1], rows[2]), VGroup(*rows[3:])])

    def map(self):
        cols = [("Hotel brands", BRAND, ["Marriott", "Hilton", "IHG", "Hyatt", "Accor", "Wyndham", "Choice", "Jin Jiang", "H World", "OYO"]),
                ("Owners", OWNER, ["Host Hotels", "Park Hotels", "Apple Hospitality", "Indian Hotels", "pension and property funds"]),
                ("Online travel", AGENT, ["Booking", "Expedia", "Airbnb", "Trip.com", "MakeMyTrip", "Tripadvisor", "Google"]),
                ("Cruise", CRUISE, ["Carnival", "Royal Caribbean", "Norwegian", "MSC"]),
                ("Casinos and betting", CASINO, ["Las Vegas Sands", "MGM", "Wynn", "Caesars", "Galaxy", "Flutter", "DraftKings"]),
                ("Parks", PARK, ["Disney", "Comcast's Universal", "Oriental Land", "Six Flags", "United Parks", "Merlin"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.3, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Accor, Jin Jiang, OYO, Indian Hotels, Google, MSC, Galaxy, Comcast's "
                  "Universal, Oriental Land and Merlin", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The hotel brands, from Marriott to France's Accor, China's Jin Jiang and H "
             "World, and India's OYO. <bookmark mark='b'/> The owners: listed property trusts, India's Indian Hotels, and the "
             "pension and property funds behind most buildings. <bookmark mark='c'/> The online agents, with Google's travel "
             "search above them all. <bookmark mark='d'/> Four cruise companies. <bookmark mark='e'/> The casino operators of "
             "Macao, Las Vegas and Singapore, and the online bookmakers. <bookmark mark='f'/> And the parks.",
             base=[head("The map of the business"), note], steps=list(gr))
