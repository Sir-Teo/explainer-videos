from __future__ import annotations

from videos.industry.industry33.common import *  # noqa: F403

OFFSET = {"McKesson": UP, "Cencora": DOWN, "Cardinal Health": LEFT, "Mitsui & Co.": UP, "Sysco": RIGHT, "ADM": UP, "Bunge": LEFT,
          "Performance Food": DOWN, "TD Synnex": LEFT, "US Foods": DOWN, "UNFI": DOWN, "Arrow": UP, "Avnet": DOWN,
          "Genuine Parts": RIGHT, "WESCO": DOWN, "CDW": LEFT, "Grainger": UP, "Henry Schein": DOWN, "Andersons": DOWN, "Fastenal": UP,
          "Core & Main": DOWN, "Watsco": UP, "Pool Corp": UP, "Applied Industrial": RIGHT, "SiteOne": DOWN,
          "Chefs' Warehouse": DOWN, "MSC Industrial": LEFT, "ScanSource": DOWN, "Owens & Minor": DOWN, "Global Industrial": LEFT}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 9, "The landscape, November 2026", "Who are the middlemen, and who keeps the most?",
             "Chapter nine. The landscape, as of November 2026: drug and food distributors, electronics and industrial "
             "suppliers, crop traders and a trading house, by size and by what they keep.", lit=("moat", "change"))
        self.scatter()
        self.profits()
        self.map()

    def scatter(self):
        C = R["landscape"]["companies"]

        def lx(v):
            return np.log10(v)
        pa = viz.plot_axes([0.0, 2.8], [-0.02, 0.16], x_length=10.0, y_length=4.9, xticks=[lx(1), lx(3), lx(10), lx(30), lx(100), lx(300)],
                           yticks=[0, 0.04, 0.08, 0.12, 0.16], xfmt=lambda v: f"${10 ** v:.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, median of the last five years",
                           size=13).move_to([-0.3, -0.5, 0])
        xl = tx("revenue, latest fiscal year (log scale; Mitsui's yen at its average rate)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.02 * np.sqrt(c["rev"] / 10)
            d = Dot(pa.ax.c2p(lx(c["rev"]), max(c["margin"], -0.018)), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        order = ["drugs", "food", "tech", "industrial", "crops", "trading"]
        key = VGroup(*[VGroup(Dot(radius=0.07, color=GROUP_COL[g]), tx(GROUP_NAME[g], 12, GROUP_COL[g])).arrange(RIGHT, buff=0.06)
                       for g in order if g in groups]).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.95)
        hd = tx("The middlemen: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K via SEC company facts; Mitsui & Co.'s results for the year to March 2026", size=12)
        g = {c["name"]: c for c in C}
        pc = lambda n: 100 * g[n]["margin"]  # noqa: E731
        beat(self,
             "The whole trade in one picture. <bookmark mark='a'/> The drug wholesalers, the largest by far, keep the least: "
             f"McKesson a median {pc('McKesson'):.1f} cents a dollar over five years, Cardinal {pc('Cardinal Health'):.1f}. "
             f"<bookmark mark='b'/> The food distributors, around one to two: Sysco {pc('Sysco'):.1f}. "
             f"<bookmark mark='c'/> Electronics and IT, one to five. <bookmark mark='d'/> The industrial and trade suppliers "
             f"keep the most: Grainger {pc('Grainger'):.0f}, Fastenal {pc('Fastenal'):.0f}, Pool {pc('Pool Corp'):.0f}. "
             f"<bookmark mark='e'/> The crop traders, two to three. <bookmark mark='f'/> And the trading house, "
             f"{pc('Mitsui & Co.'):.0f}, because it is partly a mining and energy company now.",
             base=[pa, xl, hd, key, src],
             steps=[groups["drugs"], groups["food"], groups["tech"], groups["industrial"], groups["crops"], groups["trading"]])

    def profits(self):
        C = {c["name"]: c for c in R["landscape"]["companies"]}
        M = R["returns"]["margins"]
        names = ["McKesson", "Cencora", "Sysco", "Grainger", "Cardinal Health", "Fastenal"]
        items = [(n, M[n]["net"] * M[n]["rev"] / 100, GROUP_COL[C[n]["group"]], f"${M[n]['net'] * M[n]['rev'] / 100:.1f}bn") for n in names]
        rows = hbars(items, max_value=5.2, x0=-0.6, top=2.0, row=0.75, length=6.2, size=17, bar_h=0.42)
        hd = tx("Net profit, latest year", 21, WHITE, bold=True).to_edge(UP, buff=0.6)
        src = source("Forms 10-K via SEC company facts", size=12)
        f, mk = M["Fastenal"], M["McKesson"]
        beat(self,
             "Now count profit in dollars instead of cents. <bookmark mark='a'/> McKesson and Cencora still lead: "
             f"{mk['net'] * mk['rev'] / 100:.1f} and {M['Cencora']['net'] * M['Cencora']['rev'] / 100:.1f} billion dollars. "
             "<bookmark mark='b'/> But look at the bottom of the list. <bookmark mark='c'/> Fastenal, with "
             f"{100 * f['rev'] / mk['rev']:.0f} per cent of McKesson's revenue, made {100 * (f['net'] * f['rev']) / (mk['net'] * mk['rev']):.0f} "
             "per cent of its profit, selling nuts, bolts and gloves. The biggest middleman by revenue is not always the "
             "best business; the one whose customers can least do without it today usually is.",
             base=[rows.axis, hd, src], steps=[VGroup(rows[0], rows[1]), VGroup(rows[2], rows[3], rows[4]), rows[5]])

    def map(self):
        cols = [("Drugs and medical", DRUG, ["McKesson", "Cencora", "Cardinal Health", "Henry Schein", "Sinopharm", "Alliance Healthcare"]),
                ("Food service", FOOD, ["Sysco", "US Foods", "Performance Food", "UNFI", "Chefs' Warehouse", "Metro (cash and carry)"]),
                ("Electronics and IT", TECH, ["Arrow", "Avnet", "TD Synnex", "WPG", "CDW", "Redington"]),
                ("Industrial and trade", IND, ["Grainger", "Fastenal", "WESCO", "Genuine Parts", "Würth", "MonotaRO"]),
                ("Commodity traders", CROP, ["Bunge", "ADM", "Cargill", "Louis Dreyfus", "Glencore", "Trafigura", "Vitol"]),
                ("Trading houses", TRADE, ["Mitsubishi Corp.", "Mitsui & Co.", "Itochu", "Sumitomo Corp.", "Marubeni", "Li & Fung"])]
        gr = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            gr.add(box)
        note = tx("Names only where this film has not measured them: Sinopharm, Alliance Healthcare, Metro, WPG, Redington, Würth, Cargill, "
                  "Louis Dreyfus, Glencore, Trafigura, Vitol, Mitsubishi Corp., Itochu, Sumitomo Corp., Marubeni and Li & Fung", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map. <bookmark mark='a'/> Drug and medical distributors, in America, China and Europe. "
             "<bookmark mark='b'/> Food service. <bookmark mark='c'/> Electronics and IT, from Arrow to Taiwan's WPG and "
             "India's Redington. <bookmark mark='d'/> Industrial and trade supply. <bookmark mark='e'/> The commodity "
             "traders, many of them private. <bookmark mark='f'/> And the trading houses of Japan and Hong Kong.",
             base=[head("The map of the business"), note], steps=list(gr))
