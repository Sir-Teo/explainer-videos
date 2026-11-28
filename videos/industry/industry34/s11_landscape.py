from __future__ import annotations

from videos.industry.industry34.common import *  # noqa: F403

OFFSET = {"Starbucks": UP, "McDonald's": UP, "DoorDash": DOWN, "Darden": DOWN, "Chipotle": UP, "Yum China": LEFT, "Restaurant Brands": UP,
          "Yum! Brands": DOWN, "Texas Roadhouse": UP, "Brinker": RIGHT, "Domino's": UP, "Arcos Dorados": UP, "Bloomin' Brands": DOWN,
          "Cheesecake Factory": LEFT, "Cracker Barrel": RIGHT, "Wendy's": UP, "Papa John's": RIGHT, "Dutch Bros": RIGHT,
          "Jack in the Box": UP, "Krispy Kreme": DOWN, "Shake Shack": DOWN, "Cava": UP, "First Watch": DOWN, "Dine Brands": UP,
          "Wingstop": UP, "Sweetgreen": RIGHT, "Portillo's": LEFT, "El Pollo Loco": LEFT}
FLOOR = -0.08


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who runs the restaurants, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: franchisors, chains that run their own restaurants, sit-down "
             "groups, master franchisees and the delivery app, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.profits()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([-0.4, 1.7], [FLOOR - 0.01, 0.35], x_length=10.0, y_length=4.9,
                           xticks=[lx(0.5), lx(1), lx(2), lx(5), lx(10), lx(20), lx(50)], yticks=[0, 0.1, 0.2, 0.3],
                           xfmt=lambda v: f"${10 ** v:g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of the last five years", size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 2)
            y = max(c["margin"], FLOOR)
            d = Dot(pa.ax.c2p(lx(c["rev"]), y), radius=r, color=col, fill_opacity=0.85)
            name = c["name"] if c["margin"] >= FLOOR else f"{c['name']} ({100 * c['margin']:.0f}%)"
            lab = tx(name, 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["franchisor", "operator", "full", "master", "delivery"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("Restaurants: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        zero = DashedLine(pa.ax.c2p(-0.4, 0), pa.ax.c2p(1.7, 0), color=GREY_B, stroke_width=1.5)
        src = source("Forms 10-K and 20-F via SEC company facts", size=12)
        g = {c["name"]: c for c in C}
        pc = lambda n: 100 * g[n]["margin"]  # noqa: E731
        MC = "McDonald's"
        beat(self,
             "The whole industry in one picture. <bookmark mark='a'/> The franchisors are on top: McDonald's kept a median "
             f"{pc(MC):.0f} cents of each dollar of revenue over five years, Restaurant Brands {pc('Restaurant Brands'):.0f}, Yum "
             f"{pc('Yum! Brands'):.0f}, Wingstop {pc('Wingstop'):.0f}. <bookmark mark='b'/> The chains that run their own "
             f"restaurants keep less: Chipotle {pc('Chipotle'):.0f}, Starbucks {pc('Starbucks'):.0f}, and the young fast-casual "
             f"chains next to nothing. <bookmark mark='c'/> The sit-down groups, one to nine. <bookmark mark='d'/> The master "
             f"franchisees, Arcos Dorados {pc('Arcos Dorados'):.0f} and Yum China {pc('Yum China'):.0f}. <bookmark mark='e'/> "
             "And DoorDash, below the line over five years, only now crossing it. Owning the brand and the land beats "
             "running the kitchen.",
             base=[pa, xl, hd, key, zero, src],
             steps=[groups["franchisor"], groups["operator"], groups["full"], groups["master"], groups["delivery"]])

    def map(self):
        cols = [("Franchisors", FR, ["McDonald's", "Yum! Brands", "Restaurant Brands", "Domino's", "Wingstop", "Wendy's", "Papa John's"]),
                ("Run their own", OP, ["Starbucks", "Chipotle", "Shake Shack", "Sweetgreen", "Cava", "Luckin", "Haidilao"]),
                ("Sit-down", FULL, ["Darden", "Texas Roadhouse", "Brinker", "Bloomin' Brands", "Cheesecake Factory"]),
                ("Master franchisees", MASTER, ["Arcos Dorados", "Yum China", "Jubilant FoodWorks", "Jollibee"]),
                ("Delivery", APPS, ["DoorDash", "Uber Eats", "Meituan", "Zomato", "Swiggy"]),
                ("Contract catering", ALL, ["Compass", "Sodexo", "Aramark"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Luckin, Haidilao, Jubilant FoodWorks, Jollibee, Uber Eats, Meituan, "
                  "Zomato, Swiggy, Compass, Sodexo and Aramark", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> The franchisors. <bookmark mark='b'/> The chains that run their own "
             "restaurants, including China's Luckin coffee and Haidilao hot pot. <bookmark mark='c'/> The sit-down groups. "
             "<bookmark mark='d'/> The master franchisees. <bookmark mark='e'/> The delivery apps, from DoorDash to China's "
             "Meituan and India's Zomato and Swiggy. <bookmark mark='f'/> And the contract caterers, who run the canteens of "
             "offices, schools and hospitals.",
             base=[head("The map of the business"), note], steps=list(gr))

    def profits(self):
        C = {c["name"]: c for c in R["landscape"]["companies"]}
        names = ["McDonald's", "Starbucks", "Chipotle", "Yum! Brands", "Darden", "Restaurant Brands", "DoorDash"]
        items = []
        for n in names:
            c = C[n]
            v = c["rev"] * c["margin"]
            items.append((n, v, GROUP_COL[c["group"]], f"{'-' if v < 0 else ''}${abs(v):.1f}bn"))
        rows = hbars(items, max_value=9, x0=-0.4, top=2.2, row=0.62, length=6.2, size=16, bar_h=0.36)
        hd = tx("Revenue times its five-year median margin, $bn: a typical year's profit", 20, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("Forms 10-K via SEC company facts; this series' calculation", size=12)
        beat(self,
             "Count it in dollars. <bookmark mark='a'/> On a typical year's margin, McDonald's earns about "
             f"{items[0][1]:.1f} billion dollars, <bookmark mark='b'/> Starbucks, with more revenue, about {items[1][1]:.1f} "
             f"billion, and Chipotle {items[2][1]:.1f}. <bookmark mark='c'/> The franchisors and sit-down groups follow. "
             "One burger brand that mostly collects rent earns more than the whole of the next two chains that cook for "
             "their customers themselves.",
             base=[rows.axis, hd, src], steps=[rows[0], VGroup(rows[1], rows[2]), VGroup(*rows[3:])])
