from __future__ import annotations

from videos.industry.industry20.compute import results as drug_results
from videos.industry.industry21.common import *  # noqa: F403

OFFSET = {"Medtronic": UP, "Abbott": UP, "Boston Scientific": DOWN, "Stryker": UP, "Intuitive": UP, "Edwards": UP,
          "BD": DOWN, "Zimmer Biomet": DOWN, "Baxter": DOWN, "Dexcom": UP, "Insulet": DOWN, "ResMed": UP, "Align": UP,
          "Steris": DOWN, "GE HealthCare": DOWN, "Danaher": UP, "Thermo Fisher": DOWN, "Agilent": DOWN, "Labcorp": DOWN,
          "Quest": UP, "IQVIA": RIGHT}
# crowded points: label positions in data coordinates (log10 revenue, margin), joined by a leader line
CALLOUT = {"Boston Scientific": (1.12, 0.165), "BD": (0.98, 0.05), "GE HealthCare": (1.4, 0.045),
           "IQVIA": (1.02, 0.135), "Labcorp": (1.18, 0.02), "Abbott": (1.6, 0.245), "Thermo Fisher": (1.7, 0.09),
           "Medtronic": (1.6, 0.02)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 10, "The landscape, November 2026", "Who makes medical technology, and who keeps the most?",
             "Chapter ten. The landscape, as of November 2026. Who makes medical technology, and who keeps the most of "
             "what it sells?", lit=("moat", "change"))
        self.scatter()
        self.dollar()
        self.map()

    def scatter(self):
        C = [c for c in R["landscape"]["companies"] if c["name"] != "Illumina"]
        lx = np.log10
        pa = viz.plot_axes([0.35, 1.75], [-0.1, 0.35], x_length=10.0, y_length=4.9, xticks=[np.log10(3), 1, np.log10(30)],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of 2021-2025", size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0.35, 0), pa.ax.c2p(1.75, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, latest fiscal year (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        groups: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            r = 0.05 + 0.03 * np.sqrt(c["rev"] / 10)
            if c["name"] in CALLOUT:
                groups.setdefault(c["group"], VGroup()).add(callout(pa.ax, lx(c["rev"]), c["margin"], c["name"], col,
                                                                    CALLOUT[c["name"]], size=12, radius=r))
                continue
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=r, color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            groups.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("devices", "devices"), ("imaging", "imaging"), ("tools", "tools and diagnostics makers"),
                                    ("labs", "laboratories and trials"))]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.95)
        hd = tx("Medical technology: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        il = next(c for c in R["landscape"]["companies"] if c["name"] == "Illumina")
        off = tx(f"off the chart: Illumina, ${il['rev']:.1f}bn of revenue, median margin {100 * il['margin']:.0f}%", 13, BAD)
        off.move_to(pa.ax.c2p(0.37, -0.035), aligned_edge=LEFT)
        src = source("Forms 10-K via SEC company facts (median of 2021-2025)", size=12)
        g = {c["name"]: c for c in C}
        with self.voiceover(
            "Here is the industry in one picture: each company by its revenue and by what it typically kept of each dollar. "
            "<bookmark mark='a'/> The device makers spread widely. Edwards, with its heart valves, and Intuitive, with its "
            f"robots, kept about {100 * g['Edwards']['margin']:.0f} and {100 * g['Intuitive']['margin']:.0f} cents; "
            f"Medtronic and Stryker about {100 * g['Medtronic']['margin']:.0f} and {100 * g['Stryker']['margin']:.0f}; "
            "Baxter, which sells hospital supplies, lost money. <bookmark mark='b'/> GE HealthCare, the one imaging company "
            f"here, about {100 * g['GE HealthCare']['margin']:.0f}. <bookmark mark='c'/> The makers of instruments and "
            f"tests, Danaher, Thermo Fisher and Agilent, {100 * min(g[n]['margin'] for n in ('Danaher', 'Thermo Fisher', 'Agilent')):.0f} "
            f"to {100 * max(g[n]['margin'] for n in ('Danaher', 'Thermo Fisher', 'Agilent')):.0f}. "
            "<bookmark mark='d'/> And the laboratories and the trial runner, Quest, Labcorp and IQVIA, less than ten. "
            "The more a company's product is chosen for what it does, and the less it is bought on price, the more it keeps."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(xl), FadeIn(hd), FadeIn(key), FadeIn(src), run_time=1.0)
            for mk, grp in zip("abcd", ("devices", "imaging", "tools", "labs")):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x) for x in groups[grp]], lag_ratio=0.1), run_time=1.4)
            self.play(FadeIn(off))
        self.clear_scene()

    def dollar(self):
        D = R["dollar"]
        P = drug_results()["dollar"]
        parts = [("making", "make", PRICE), ("research", "research", GOOD), ("everything else", "rest", GREY_B),
                 ("profit", "profit", DEVICE)]

        def row(d, y, title):
            bar = viz.bar_split([(n, d[k], c) for n, k, c in parts], 1.0, width=10.0, height=0.7).move_to([0.8, y, 0])
            labs = VGroup(*[tx(f"{100 * d[k]:.0f}c", 18, "#0E1117", bold=True).move_to(bar[i]) for i, (n, k, c) in enumerate(parts)])
            ttl = tx(title, 16, WHITE, bold=True).next_to(bar, LEFT, buff=0.25)
            if ttl.get_left()[0] < -7.0:
                ttl.shift(RIGHT * (-7.0 - ttl.get_left()[0]))
            return VGroup(bar, labs, ttl)
        dev = row(D, 0.9, "devices")
        drg = row(P, -0.6, "medicines")
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9), tx(n, 14, GREY_A)).arrange(RIGHT, buff=0.1)
                       for n, _, c in parts]).arrange(RIGHT, buff=0.5).move_to([0.8, -2.0, 0])
        hd = tx(f"Each dollar of revenue: {D['n']} device makers (${D['revenue']:.0f}bn) and Part 20's {P['n']} drug makers",
                19, WHITE, bold=True).to_edge(UP, buff=0.9)
        src = source("Forms 10-K via SEC company facts, latest fiscal year: revenue, cost of sales, research and development, "
                     "net income", size=12)
        beat(self,
             f"Where does a dollar spent on devices go? Take {D['n']} device makers together, {D['revenue']:.0f} billion "
             f"dollars of revenue in their latest year. <bookmark mark='a'/> Making the devices took about "
             f"{100 * D['make']:.0f} cents, research {100 * D['research']:.0f}, everything else, mostly selling and "
             f"running the company, {100 * D['rest']:.0f}, and profit {100 * D['profit']:.0f}. <bookmark mark='b'/> Set it "
             f"beside Part 20's drug makers: {100 * P['make']:.0f} cents for making, {100 * P['research']:.0f} for "
             f"research, {100 * P['profit']:.0f} for profit. <bookmark mark='c'/> A device costs more to make and less to "
             "invent than a medicine, and it keeps less of each dollar as profit. Its advantage is the surgeon's habit and "
             "the installed base, not a patent date.",
             base=[hd, src], steps=[dev, drg, key])

    def map(self):
        cols = [("Devices, America", DEVICE, ["Medtronic", "Abbott", "Boston Scientific", "Stryker", "J&J MedTech", "Intuitive",
                                              "Edwards", "BD", "Zimmer Biomet"]),
                ("Imaging", IMAGING, ["Siemens Healthineers", "GE HealthCare", "Philips", "United Imaging"]),
                ("Diagnostics, tools", TOOLS, ["Roche Diagnostics", "Danaher", "Thermo Fisher", "Illumina", "Agilent"]),
                ("Labs and trials", LABS, ["Quest", "Labcorp", "IQVIA"]),
                ("Japan and China", PRICE, ["Olympus", "Terumo", "Mindray"]),
                ("Diabetes and sleep", GOOD, ["Dexcom", "Insulet", "ResMed"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: J&J MedTech, Siemens Healthineers, Philips, United "
                  "Imaging, Roche Diagnostics, Olympus, Terumo and Mindray", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        beat(self,
             "And the map, by role. <bookmark mark='a'/> The American device makers. <bookmark mark='b'/> The imaging "
             "companies, two of them European and one Chinese. <bookmark mark='c'/> The makers of diagnostics and tools. "
             "<bookmark mark='d'/> The laboratories and the trial runners. <bookmark mark='e'/> Japan's and China's makers. "
             "<bookmark mark='f'/> And the companies that sell devices people wear every day, for diabetes and sleep. "
             "Several report outside America's securities regulator, or inside larger companies, so this film shows them "
             "by name only.",
             base=[head("The map of the business"), note], steps=list(g))
