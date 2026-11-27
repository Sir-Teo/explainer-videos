from __future__ import annotations

from videos.industry.industry18.common import *  # noqa: F403

OFFSET = {"Airbus": RIGHT, "Boeing": DOWN, "Embraer": RIGHT, "GE Aerospace": UP, "RTX": DOWN, "Lockheed Martin": UL,
          "Northrop Grumman": UP, "General Dynamics": DOWN, "L3Harris": DOWN, "Huntington Ingalls": DOWN, "TransDigm": DOWN,
          "HEICO": UP, "Howmet": DOWN, "Textron": UP, "AerCap": UP}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who builds the aircraft, and who keeps the money?",
             "Chapter twelve. The landscape, as of November 2026. Who builds the aircraft, and who keeps the money?",
             lit=("moat", "change"))
        self.scatter()
        self.map()
        self.now()

    def scatter(self):
        C = R["landscape"]["companies"]
        lx = np.log10
        pa = viz.plot_axes([0.5, 2.1], [-0.1, 0.3], x_length=10.0, y_length=5.0, xticks=[np.log10(5), 1, np.log10(30), 2],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3], xfmt=lambda v: f"${10 ** v:.0f}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, 2021-2025 average",
                           size=13).move_to([-0.3, -0.45, 0])
        zero = DashedLine(pa.ax.c2p(0.5, 0), pa.ax.c2p(2.1, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        dots: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=0.05 + 0.03 * np.sqrt(c["rev"] / 10), color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            dots.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("airframer", "airframers"), ("engines", "engines"), ("defence", "defence primes"),
                                    ("supplier", "parts makers"), ("lessor", "lessor"))]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.95)
        head_ = tx("Aerospace and defence: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Forms 10-K and 20-F via SEC company facts; Airbus SE, Annual Report 2025 (2025 only, at the Fed's average "
                     "rate); GE Aerospace: 2025, its first full year alone", size=12)
        g = {c["name"]: c for c in C}
        with self.voiceover(
            "Here is the industry in one picture: each company by its revenue, and by what it kept of each dollar, on "
            "average over five years. <bookmark mark='a'/> The airframers, the biggest names, keep the least: Airbus "
            f"about {100 * g['Airbus']['margin']:.0f} cents, Boeing a loss of {-100 * g['Boeing']['margin']:.0f}, Embraer "
            f"{100 * g['Embraer']['margin']:.0f}. <bookmark mark='b'/> The engine makers do better, GE Aerospace "
            f"{100 * g['GE Aerospace']['margin']:.0f} cents in its first full year alone. <bookmark mark='c'/> The defence "
            "primes sit together between five and twelve cents, steady and capped. <bookmark mark='d'/> The parts makers "
            f"with their own designs keep the most: TransDigm {100 * g['TransDigm']['margin']:.0f} cents, HEICO "
            f"{100 * g['HEICO']['margin']:.0f}. <bookmark mark='e'/> And AerCap, the lessor, "
            f"{100 * g['AerCap']['margin']:.0f}, helped by its recovery from Russia. The closer a company sits to the "
            "aircraft already flying, the more it keeps."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(xl), FadeIn(head_), FadeIn(src), FadeIn(key),
                      FadeIn(ghost(*[v for v in dots.values()], opacity=0.2)))
            for mk, grp in zip("abcde", ("airframer", "engines", "defence", "supplier", "lessor")):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x) for x in dots[grp]], lag_ratio=0.15), run_time=1.4)
        self.clear_scene()

    def map(self):
        cols = [("Airframers", AIRBUS, ["Airbus", "Boeing", "Embraer", "ATR (Airbus and Leonardo)", "COMAC"]),
                ("Engines", ENGINE, ["GE Aerospace", "Safran", "CFM (GE and Safran)", "Pratt & Whitney (RTX)", "Rolls-Royce"]),
                ("Parts and structures", SUPPLIER, ["TransDigm", "HEICO", "Howmet", "Textron", "Spirit (now Boeing's)"]),
                ("Lessors", PRICE, ["AerCap"]),
                ("Defence, US", DEFENCE, ["Lockheed Martin", "RTX", "Northrop Grumman", "General Dynamics", "L3Harris",
                                          "Huntington Ingalls", "Boeing Defense"]),
                ("Defence, Europe", DEFENCE, ["Airbus Defence and Space", "BAE Systems", "Leonardo", "Thales"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            x = -6.2 + 2.2 * i
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([x, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: COMAC, Safran, Rolls-Royce, BAE Systems, Leonardo and Thales "
                  "report outside the SEC, and are left for later parts", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        head_ = tx("The map of the business", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "And the map, by role. <bookmark mark='a'/> The airframers: the two giants, Brazil's Embraer, the turboprop "
            "maker ATR, and China's state-owned COMAC, which is building its own single-aisle jet. <bookmark mark='b'/> "
            "The engine makers, including the two halves of CFM, and Britain's Rolls-Royce on twin-aisle jets. "
            "<bookmark mark='c'/> The makers of parts and structures. <bookmark mark='d'/> The lessors. "
            "<bookmark mark='e'/> America's defence primes, <bookmark mark='f'/> and Europe's."
        ) as vo:
            self.play(FadeIn(head_), FadeIn(note), FadeIn(ghost(*[b[0] for b in g], opacity=0.35)))
            for mk, box in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in box], lag_ratio=0.08), run_time=1.2)
        self.clear_scene()

    def now(self):
        L = R["landscape"]
        rows = VGroup(
            tx(f"Boeing delivered {L['q9']} airliners in the first nine months of 2026, against {L['q9_prev']} a year earlier", 17, BOEING),
            tx(f"the 737 line began moving to {L['rate47']} a month, with the FAA's agreement; Boeing now expects it to settle in 2027", 17, WHITE),
            tx(f"the 737-7 was certified in the third quarter, the 737-10 in October {L['cert10']}", 17, WHITE),
            tx(f"the 777-9's first delivery: still expected in {L['x_first']}", 17, PRICE),
            tx(f"Boeing's backlog: ${L['backlog'] / 1e3:,.0f}bn at the end of September", 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.1, 0])
        for r_ in rows:
            if r_.width > 12.6:
                r_.scale_to_fit_width(12.6)
        stamp = as_of("as of 30 September 2026")
        src = source("The Boeing Company, Form 10-Q for the third quarter of 2026 (filed 27 October 2026)", size=12)
        beat(self,
             "Where things stand as this film is made. <bookmark mark='a'/> Boeing is recovering: "
             f"{L['q9']} deliveries in the first nine months of 2026, more than a year earlier. "
             f"<bookmark mark='b'/> The 737 line began moving to {L['rate47']} a month in the spring, and Boeing now "
             "expects it to settle there in 2027. <bookmark mark='c'/> The two missing 737 models, the smallest and the "
             "largest, were finally certified. <bookmark mark='d'/> The 777-9 is still expected in "
             f"{L['x_first']}. <bookmark mark='e'/> And the order book stands at "
             f"{L['backlog'] / 1e3:,.0f} billion dollars.",
             base=[stamp, src], steps=list(rows))
