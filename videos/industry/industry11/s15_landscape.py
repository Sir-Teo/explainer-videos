from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403

NAMES = {"NUE": "Nucor", "STLD": "Steel Dynamics", "CLF": "Cleveland-Cliffs", "CMC": "Commercial Metals", "MT": "ArcelorMittal",
         "CRH": "CRH", "AMRZ": "Amrize", "VMC": "Vulcan", "MLM": "Martin Marietta", "EXP": "Eagle Materials", "CX": "Cemex",
         "AA": "Alcoa", "CENX": "Century Aluminum", "IP": "International Paper", "SW": "Smurfit Westrock",
         "PKG": "Packaging Corp.", "BALL": "Ball", "CCK": "Crown", "OI": "O-I Glass"}
GROUP_COL = {"steel": "#7EC8F5", "cement and aggregates": "#E8EAED", "aluminium": "#B58CFF", "packaging": "#F2C14E"}
SIDE = {"NUE": UP, "STLD": LEFT, "CLF": UP, "CMC": LEFT, "MT": UP, "CRH": RIGHT, "AMRZ": DOWN, "VMC": LEFT, "MLM": UP,
        "EXP": UP, "CX": DOWN, "AA": LEFT, "CENX": UP, "IP": DOWN + RIGHT * 0.6, "SW": RIGHT, "PKG": LEFT, "BALL": RIGHT,
        "CCK": UP, "OI": DOWN}
STEELMAKERS = {"baowu": ("China Baowu", CHINA), "arcelormittal": ("ArcelorMittal", "#B58CFF"), "nippon": ("Nippon Steel", "#E8EAED"),
               "ansteel": ("Ansteel", CHINA), "hbis": ("HBIS", CHINA), "shagang": ("Shagang", CHINA),
               "jianlong": ("Jianlong", CHINA), "posco": ("POSCO", "#9AD1F5"), "delong": ("Delong", CHINA),
               "tata": ("Tata Steel", "#F2C14E"), "jsw": ("JSW Steel", "#F2C14E"), "shougang": ("Shougang", CHINA),
               "jfe": ("JFE", "#E8EAED"), "nucor": ("Nucor", USA), "cliffs": ("Cleveland-Cliffs", USA),
               "stld": ("Steel Dynamics", USA)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 13, "The landscape, November 2026", "Who makes the heavy materials, and who earns anything on them?",
             "Chapter thirteen. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.makers()
        self.bubbles()
        self.watch()

    def makers(self):
        L = R["landscape"]["steelmakers"]
        rows = VGroup()
        for i, (k, v) in enumerate(L):
            n, col = STEELMAKERS[k]
            y = 2.7 - 0.36 * i
            b = Rectangle(width=8.4 * v / L[0][1], height=0.26, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [-2.4, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(tx(n, 14, WHITE).next_to([-2.5, y, 0], LEFT, buff=0.1), b,
                            tx(f"{v:.1f}", 12, WHITE, bold=True).next_to(b, RIGHT, buff=0.06)))
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=c, fill_opacity=0.85), tx(t_, 13, GREY_A)).arrange(
            RIGHT, buff=0.08) for c, t_ in ((CHINA, "China"), ("#E8EAED", "Japan"), ("#9AD1F5", "South Korea"),
                                           ("#F2C14E", "India"), ("#B58CFF", "Luxembourg"), (USA, "United States"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([5.6, -1.6, 0])
        head = tx("The largest steelmakers, 2025, million tonnes", 20, WHITE, bold=True).to_edge(UP, buff=0.2)
        stamp = as_of("as of November 2026")
        src = source("World Steel Association, World Steel in Figures 2026 (top 50 companies; ArcelorMittal includes 60% of "
                     "AM/NS India; Nippon Steel includes US Steel)", size=12)
        with self.voiceover(
            "Here is the landscape, as of November 2026. First the steelmakers, by the tonnes they made in 2025. "
            f"<bookmark mark='a'/> The largest by far is China Baowu, with about {L[0][1]:.0f} million tonnes, more "
            "than the whole of Japan. Then ArcelorMittal, based in Luxembourg, and Nippon Steel, which now includes US "
            "Steel. <bookmark mark='b'/> Seven of the top twelve are Chinese; India's Tata and JSW are climbing. "
            f"<bookmark mark='c'/> The largest American, Nucor, comes in at about {dict(L)['nucor']:.0f} million tonnes, "
            "sixteenth in the world."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(stamp),
                      LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[:3]],
                                  lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=CHINA), run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[3:13]],
                                  lag_ratio=0.12), FadeIn(key), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[13:]],
                                  lag_ratio=0.2), run_time=1.2)
            self.play(Indicate(rows[13], color=USA))
        self.clear_scene()

    def bubbles(self):
        C = R["landscape"]["companies"]
        pa = viz.plot_axes([np.log10(1.8), np.log10(80)], [-0.01, 0.23], x_length=9.0, y_length=5.0,
                           xticks=[np.log10(v) for v in (2, 5, 10, 20, 50)], yticks=[0, 0.05, 0.1, 0.15, 0.2],
                           xfmt=lambda v: f"${10 ** v:,.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of sales, five-year average", size=13).move_to([-1.4, -0.35, 0])
        xl = tx("revenue in the latest year (log scale)", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        zero = Line(pa.ax.c2p(np.log10(1.8), 0), pa.ax.c2p(np.log10(80), 0), stroke_color=GREY_B, stroke_width=1.2)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]), c["margin5"])
            d = VGroup(Circle(0.06 * np.sqrt(c["revenue"]) ** 0.8, stroke_color=col, stroke_width=2, fill_color=col,
                              fill_opacity=0.4).move_to(p), tx(NAMES[c["ticker"]], 12, WHITE, bold=True))
            d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        order = ["steel", "cement and aggregates", "aluminium", "packaging"]
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(g, 15, WHITE)).arrange(RIGHT, buff=0.1) for g in order]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.4, 1.8, 0])
        note = VGroup(tx("Not drawn (no US annual filing):", 13, GREY_A), tx("Baowu, Nippon Steel, POSCO, Tata,", 12, GREY_B),
                      tx("Holcim, Heidelberg Materials,", 12, GREY_B), tx("Chalco, Hongqiao, Rio Tinto", 12, GREY_B),
                      tx("Ball's and Martin Marietta's 2024", 12, GREY_B), tx("(years of big sales) left out", 12, GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([5.4, -1.3, 0])
        head = tx("The listed makers of heavy materials", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("SEC EDGAR: Forms 10-K (net income attributable to the company) and 20-F (ArcelorMittal; Cemex to "
                     "2024)", size=13)
        L = {c["ticker"]: c for c in C}
        with self.voiceover(
            "Now the companies that file accounts in the United States, by revenue and by how much of each dollar they "
            "kept over five years. <bookmark mark='a'/> The steelmakers: Nucor and Steel Dynamics, the minimills, "
            f"around {100 * L['NUE']['margin5']:.0f} cents in the dollar over a boom and a bust; ArcelorMittal, the "
            "biggest; and Cleveland-Cliffs, with blast furnaces, near zero. <bookmark mark='b'/> Cement and stone: CRH, "
            "the largest of them all by revenue, Amrize, and Cemex; and the "
            f"quarry owners, Vulcan and Martin Marietta, at {100 * L['VMC']['margin5']:.0f} and "
            f"{100 * L['MLM']['margin5']:.0f} cents, the best of the large ones. <bookmark mark='c'/> Aluminium, Alcoa "
            "and Century, barely above zero. <bookmark mark='d'/> And packaging, from Packaging Corporation near the "
            "top to International Paper and O-I Glass near the bottom. Big, essential and, mostly, thin: the "
            "money sits with whoever has a moat, a permit near a city, a scrap-fed mill near its customers."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(note))
            for g, m in zip(order, "abcd"):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups[g]], lag_ratio=0.2), run_time=1.4)
        self.clear_scene()

    def watch(self):
        G = R["glut"]
        A = R["aluminium"]
        items = [(draw.ship(1.2), "China's steel", f"output down {abs(get('ws.prod.china.jan_oct.change')):.1f}% in Jan-Oct 2026; "
                  f"exports {G['exports25']:.0f} Mt in 2025"),
                 (draw.coil(0.3), "Tariffs", f"America's {G['tariff50']:.0f}% on steel and aluminium, and what it does to "
                  "prices at home"),
                 (draw.can(0.6), "The Gulf's smelters", f"back to {A['gcc_monthly']['2026-10']:.0f} kt in October 2026, "
                  f"from {A['gcc_low']:.0f} in April"),
                 (draw.ibeam(0.4), "Building", "data centres and factories against housing and roads; Nucor cites data "
                  "centres"),
                 (draw.rotary_kiln(0.8), "Carbon", "the EU's border charge in its first year; hydrogen steel and capture"),
                 (draw.coin(0.2), "China's demand", "worldsteel's forecast for 2026 "
                  "against the outcome: our call")]
        rows = VGroup()
        for ic, h, d in items:
            ic.scale_to_fit_height(min(ic.height, 0.5))
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            rows.add(VGroup(ic, VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                              buff=0.04)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([0, -0.4, 0])
        for r_ in rows:
            r_[0].set_opacity(0.3)
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("World Steel Association (24 November 2026); International Aluminium Institute; USGS MCS 2026; Nucor, "
                     "Form 10-K 2025", size=13)
        with self.voiceover(
            "And what to watch. <bookmark mark='a'/> China's steel: its output was down almost three per cent in the "
            "first ten months of 2026, and how much of the rest it sends abroad. <bookmark mark='b'/> America's tariffs "
            "of fifty per cent on steel and aluminium, and what they do to prices at home. <bookmark mark='c'/> The Gulf's "
            "smelters, climbing back after the war. <bookmark mark='d'/> Building: data centres and factories, which "
            "Nucor says are driving its orders, against housing and roads. <bookmark mark='e'/> Carbon: Europe's border "
            "charge in its first year, and whether hydrogen steel gets built. <bookmark mark='f'/> And China's demand for "
            "steel, which brings us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(rows[k][0].animate.set_opacity(1), FadeIn(rows[k][1], shift=RIGHT * 0.2))
        self.clear_scene()
