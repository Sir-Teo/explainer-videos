from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403

OFFSET = {"Caterpillar": UP, "Deere": DOWN, "CNH": DOWN, "AGCO": DOWN, "Cummins": UP, "Otis": DOWN, "Carrier": DOWN,
          "Trane": LEFT, "Johnson Controls": DOWN, "Rockwell": LEFT, "Emerson": UP, "Honeywell": UP, "Illinois Tool Works": UP,
          "Parker Hannifin": RIGHT, "Eaton": UP, "Dover": RIGHT, "United Rentals": LEFT, "Terex": DOWN, "Oshkosh": UP, "3M": DOWN,
          "GE Vernova": DOWN, "Ingersoll Rand": UP, "Xylem": DOWN}
SHOW = {"Caterpillar", "Deere", "CNH", "Cummins", "Otis", "Carrier", "Trane", "Rockwell", "Emerson", "Honeywell",
        "Illinois Tool Works", "Parker Hannifin", "Eaton", "United Rentals", "Terex", "3M", "GE Vernova", "Dover"}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 10, "The landscape, November 2026", "Who makes the machines, and who keeps the most?",
             "Chapter ten. The landscape, as of November 2026. Who makes the machines, and who keeps the most?",
             lit=("moat", "change"))
        self.scatter()
        self.steady()
        self.map()

    def steady(self):
        S = R["steady"]
        ser = {"Illinois Tool Works": ({y: 100 * v for y, v in S["ITW"].items() if y <= 2025}, "#E6A0C4"),
               "Caterpillar": ({y: 100 * v for y, v in S["CAT"].items() if y <= 2025}, MACHINE),
               "Terex": ({y: 100 * v for y, v in S["TEX"].items() if y <= 2025}, PRICE)}
        ch = line_chart(ser, x=(2010, 2025), y=(-5, 25), xticks=[2010, 2013, 2016, 2019, 2022, 2025], yticks=[-5, 0, 5, 10, 15, 20, 25],
                        yfmt=lambda v: f"{v:.0f}%", ylabel="net income, % of revenue", width=9.0, height=4.4, center=(-1.0, -0.45))
        zero = DashedLine(ch.ax.c2p(2010, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("Forms 10-K via SEC company facts", size=12)
        beat(self,
             "Margins also differ in how steady they are. <bookmark mark='a'/> Illinois Tool Works kept between ten and "
             "twenty-two cents of each dollar every year since 2010. "
             "<bookmark mark='b'/> Caterpillar's margin fell to about zero in 2016 before climbing to records. "
             "<bookmark mark='c'/> Terex, a smaller machine maker, lost money in 2016 and 2020. The bigger "
             "the swings in a maker's sales, the more its profit depends on where the cycle stands.",
             base=[ch.frame, zero, src], steps=[[ch.lines["Illinois Tool Works"], ch.labels["Illinois Tool Works"]],
                                               [ch.lines["Caterpillar"], ch.labels["Caterpillar"]],
                                               [ch.lines["Terex"], ch.labels["Terex"]]])

    def scatter(self):
        C = [c for c in R["landscape"]["companies"] if c["name"] in SHOW]
        lx = np.log10
        pa = viz.plot_axes([0.6, 1.95], [0, 0.22], x_length=10.0, y_length=4.9, xticks=[np.log10(5), 1, np.log10(30), np.log10(60)],
                           yticks=[0, 0.05, 0.1, 0.15, 0.2], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of 2021-2025", size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        dots: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=0.05 + 0.03 * np.sqrt(c["rev"] / 10), color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            dots.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("construction", "construction"), ("farm", "farm"), ("buildings", "buildings"),
                                    ("automation", "automation"), ("components", "components and power"),
                                    ("conglomerate", "diversified"), ("rental", "rental"))]).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.95)
        head_ = tx("Machinery: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts (median of 2021-2025, robust to one-off gains on sales of businesses)",
                     size=12)
        g = {c["name"]: c for c in C}
        order = ("construction", "farm", "buildings", "automation", "components", "conglomerate", "rental")
        with self.voiceover(
            "Here is the industry in one picture: each company by its revenue and by what it typically kept of each "
            "dollar. <bookmark mark='a'/> Caterpillar and Deere, the two giants of construction and farm machines, kept "
            f"about {100 * g['Caterpillar']['margin']:.0f} and {100 * g['Deere']['margin']:.0f} cents; smaller rivals like "
            f"Terex and CNH much less. <bookmark mark='b'/> The makers for buildings, elevators, heating and cooling: "
            f"Trane kept {100 * g['Trane']['margin']:.0f}, Otis {100 * g['Otis']['margin']:.0f}. <bookmark mark='c'/> The "
            f"automation and component makers: Emerson {100 * g['Emerson']['margin']:.0f}, Eaton "
            f"{100 * g['Eaton']['margin']:.0f}, Rockwell {100 * g['Rockwell']['margin']:.0f}, and Illinois Tool Works "
            f"{100 * g['Illinois Tool Works']['margin']:.0f}. <bookmark mark='d'/> GE Vernova, the newest company here, kept "
            f"about {100 * g['GE Vernova']['margin']:.0f}, and United Rentals {100 * g['United Rentals']['margin']:.0f}. "
            "Size does not buy margin in this industry."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(head_), FadeIn(src), FadeIn(key),
                      FadeIn(ghost(*[v for v in dots.values()], opacity=0.2)))
            for mk, grps in zip("abcd", (("construction", "farm"), ("buildings",), ("automation", "conglomerate"),
                                         ("components", "rental"))):
                vo.wait_until(mk)
                self.play(*[LaggedStart(*[FadeIn(x) for x in dots[k]], lag_ratio=0.15) for k in grps if k in dots], run_time=1.4)
        self.clear_scene()

    def map(self):
        cols = [("Construction and farm", MACHINE, ["Caterpillar", "Deere", "Komatsu", "CNH", "AGCO", "Sany", "XCMG", "Volvo CE"]),
                ("Automation", ROBOT, ["Siemens", "ABB", "Fanuc", "Yaskawa", "Keyence", "Rockwell", "Emerson", "Schneider"]),
                ("Buildings", BLUE, ["Otis", "Schindler", "Kone", "Trane", "Carrier", "Johnson Controls", "Daikin"]),
                ("Components and power", "#C9D3E0", ["Cummins", "Parker Hannifin", "Eaton", "Atlas Copco", "SKF", "GE Vernova"]),
                ("Diversified", "#E6A0C4", ["Honeywell", "3M", "Illinois Tool Works", "Dover", "Hitachi"]),
                ("Rental", PRICE, ["United Rentals", "Ashtead (Sunbelt)", "Herc"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Komatsu, Sany, XCMG, Volvo, Siemens, ABB, Fanuc, Yaskawa, "
                  "Keyence, Schneider, Schindler, Kone, Daikin, Atlas Copco, SKF, Hitachi, Ashtead and Herc", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        head_ = tx("The map of the business", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "And the map, by role. <bookmark mark='a'/> Construction and farm machines, American, Japanese, European and "
            "now Chinese. <bookmark mark='b'/> Automation: European, Japanese and American. <bookmark mark='c'/> The "
            "makers for buildings: elevators, heating and cooling. <bookmark mark='d'/> Components and power. "
            "<bookmark mark='e'/> The diversified groups that remain, <bookmark mark='f'/> and the rental companies. Many "
            "of these names report outside America's securities regulator, Komatsu and Fanuc in Japan, Siemens, ABB and "
            "Kone in Europe, Sany and XCMG in China, so this film shows them by name only, and leaves their accounts for "
            "later parts."
        ) as vo:
            self.play(FadeIn(head_), FadeIn(note), FadeIn(ghost(*[b[0] for b in g], opacity=0.35)))
            for mk, box in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in box], lag_ratio=0.08), run_time=1.2)
        self.clear_scene()
