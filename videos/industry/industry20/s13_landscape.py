from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403

OFFSET = {"Pfizer": RIGHT, "Merck": UP, "Johnson & Johnson": UP, "Eli Lilly": DOWN, "AbbVie": DOWN, "Bristol Myers Squibb": LEFT,
          "AstraZeneca": UP, "Amgen": UP, "Gilead": DOWN, "Vertex": UP, "Regeneron": DOWN, "Biogen": DOWN, "Teva": DOWN,
          "Viatris": UP}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 11, "The landscape, November 2026", "Who makes medicines, and who keeps the most?",
             "Chapter eleven. The landscape, as of November 2026. Who makes the world's medicines, and who keeps the most?",
             lit=("moat", "change"))
        self.scatter()
        self.dollar()
        self.map()

    def scatter(self):
        C = [c for c in R["landscape"]["companies"] if c["name"] != "Moderna"]
        lx = np.log10
        pa = viz.plot_axes([0.9, 2.05], [-0.1, 0.4], x_length=10.0, y_length=4.9, xticks=[1, np.log10(30), 2],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3, 0.4], xfmt=lambda v: f"${10 ** v:.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, median of 2021-2025", size=13).move_to([-0.3, -0.5, 0])
        zero = DashedLine(pa.ax.c2p(0.9, 0), pa.ax.c2p(2.05, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        xl = tx("revenue, 2025 (log scale)", 13, GREY_B).next_to(pa.ax, DOWN, buff=0.45)
        dots: dict = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            d = Dot(pa.ax.c2p(lx(c["rev"]), c["margin"]), radius=0.05 + 0.03 * np.sqrt(c["rev"] / 10), color=col, fill_opacity=0.85)
            lab = tx(c["name"], 12, col, bold=True).next_to(d, OFFSET.get(c["name"], UP), buff=0.06)
            dots.setdefault(c["group"], VGroup()).add(VGroup(d, lab))
        key = VGroup(*[VGroup(Dot(radius=0.08, color=GROUP_COL[g]), tx(n, 13, GROUP_COL[g])).arrange(RIGHT, buff=0.08)
                       for g, n in (("large", "large drug companies"), ("biotech", "biotech"), ("generics", "generics"))]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.95)
        head_ = tx("Medicines: size against what each company kept", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        mod = next(c for c in R["landscape"]["companies"] if c["name"] == "Moderna")
        off = tx(f"off the chart: Moderna, ${mod['rev']:.1f}bn of revenue and a median margin of {100 * mod['margin']:.0f}%", 13, BAD)
        off.move_to(pa.ax.c2p(1.45, -0.065), aligned_edge=LEFT)
        src = source("Forms 10-K and 20-F via SEC company facts (median of 2021-2025)", size=12)
        g = {c["name"]: c for c in C}
        with self.voiceover(
            "Here is the industry in one picture: each company by its revenue and by what it typically kept of each "
            "dollar. <bookmark mark='a'/> The large drug companies keep a lot: Merck about "
            f"{100 * g['Merck']['margin']:.0f} cents, Johnson and Johnson {100 * g['Johnson & Johnson']['margin']:.0f}, "
            f"Lilly {100 * g['Eli Lilly']['margin']:.0f}; Pfizer and AbbVie less. "
            "<bookmark mark='b'/> The biotech companies with protected products keep the most: Vertex "
            f"{100 * g['Vertex']['margin']:.0f}, Regeneron {100 * g['Regeneron']['margin']:.0f}. Moderna, whose revenue "
            f"fell from {R['landscape']['mrna'][2022]:.0f} billion dollars in 2022 to {R['landscape']['mrna'][2025]:.1f} "
            "billion in 2025, lost more than it sold. <bookmark mark='c'/> And the generic makers, Teva and "
            "Viatris, which sell the medicines after the cliff, lost money. Protection is the profit. Johnson and "
            f"Johnson, the largest by revenue at {g['Johnson & Johnson']['rev']:.0f} billion dollars, also sells medical "
            "devices, the subject of the next part."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(xl), FadeIn(head_), FadeIn(src), FadeIn(key), FadeIn(off),
                      FadeIn(ghost(*[v for v in dots.values()], opacity=0.2)))
            for mk, grp in zip("abc", ("large", "biotech", "generics")):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x) for x in dots[grp]], lag_ratio=0.15), run_time=1.4)
        self.clear_scene()

    def dollar(self):
        D = R["dollar"]
        parts = [("making the medicines", D["make"], GENERIC), ("research and development", D["research"], LAB),
                 ("selling, running, buying, taxes", D["rest"], PRICE), ("profit", D["profit"], GOOD)]
        bar = viz.bar_split([(n, v, c) for n, v, c in parts], 1.0, width=12.0, height=0.9).move_to(UP * 0.7)
        labs = VGroup()
        for k, (n, v, c) in enumerate(parts):
            t = VGroup(tx(f"{100 * v:.0f}c", 24, c, bold=True), tx(n, 13, GREY_A)).arrange(DOWN, buff=0.06)
            if t.width > bar[k].width + 0.2:
                t.scale_to_fit_width(bar[k].width + 0.2)
            t.next_to(bar[k], DOWN, buff=0.25)
            labs.add(t)
        steps = [VGroup(bar[k], labs[k]) for k in range(4)]
        hd = tx(f"Each dollar of revenue, {D['n']} drug companies together, 2025 (${D['revenue']:.0f}bn)", 20, WHITE, bold=True).to_edge(UP, buff=0.9)
        cap = tx("each line as each company reports it; Johnson & Johnson, Regeneron and Novartis left out for want of a line", 13, GREY_B).to_edge(DOWN, buff=0.8)
        pill = draw.capsule(1.0, BRAND).move_to([0, 2.2, 0]).shift(LEFT * 5.2)
        src = source("Forms 10-K and 20-F via SEC company facts, 2025: revenue, cost of sales, research and development, net income", size=12)
        beat(self,
             f"Where does a dollar spent on these companies' medicines go? Take {D['n']} of them together, "
             f"{D['revenue']:.0f} billion dollars of revenue in 2025. <bookmark mark='a'/> Making the medicines, the "
             f"factories, the materials and the people in them, took about {100 * D['make']:.0f} cents of each dollar. "
             f"<bookmark mark='b'/> Research and development took {100 * D['research']:.0f} cents, a fifth of all the "
             f"money coming in. <bookmark mark='c'/> {100 * D['rest']:.0f} cents went on everything else: "
             "selling to doctors and insurers, running the company, writing off research bought from others, interest and "
             f"taxes. <bookmark mark='d'/> And {100 * D['profit']:.0f} cents was profit. Making the medicine is only "
             "about a quarter of its price; most of what a patient or insurer pays for is the search that found it, the "
             "selling of it, and the protection that lets it be sold above cost.",
             base=[hd, cap, pill, src], steps=steps)

    def map(self):
        cols = [("Large, America", BRAND, ["Eli Lilly", "Johnson & Johnson", "Merck", "Pfizer", "AbbVie", "Bristol Myers Squibb"]),
                ("Large, Europe", BRAND, ["Novo Nordisk", "Roche", "Novartis", "AstraZeneca", "Sanofi", "GSK"]),
                ("Japan and China", GOV, ["Takeda", "Daiichi Sankyo", "Hengrui", "BeiGene"]),
                ("Biotech", BIO, ["Amgen", "Gilead", "Vertex", "Regeneron", "Biogen", "Moderna"]),
                ("Generics", GENERIC, ["Teva", "Viatris", "Sandoz", "Sun Pharma", "Dr. Reddy's", "Cipla"]),
                ("Contract makers", LAB, ["Lonza", "Samsung Biologics", "WuXi"])]
        g = VGroup()
        for i, (title, col, names) in enumerate(cols):
            box = VGroup(tx(title, 16, col, bold=True), *[tx(n, 13, WHITE) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            if box.width > 2.1:
                box.scale_to_fit_width(2.1)
            box.move_to([-6.2 + 2.2 * i, 2.2, 0], aligned_edge=UL)
            g.add(box)
        note = tx("Names only where this film has not measured them: Novo Nordisk, Roche, Novartis, Sanofi, GSK, Takeda, Daiichi "
                  "Sankyo, Hengrui, BeiGene, Sandoz, Sun, Dr. Reddy's, Cipla, Lonza, Samsung Biologics and WuXi", 13, GREY_B).to_edge(DOWN, buff=0.6)
        if note.width > 13:
            note.scale_to_fit_width(13)
        head_ = tx("The map of the business", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        with self.voiceover(
            "And the map, by role. <bookmark mark='a'/> The large American companies, <bookmark mark='b'/> and the large "
            "European ones. <bookmark mark='c'/> "
            "Japan's and China's. <bookmark mark='d'/> The biotech companies, "
            "<bookmark mark='e'/> the generic makers, several of them Indian, <bookmark mark='f'/> and the contract makers "
            "who manufacture medicines for others. Many report outside America's securities regulator, so this film "
            "shows them by name only."
        ) as vo:
            self.play(FadeIn(head_), FadeIn(note), FadeIn(ghost(*[b[0] for b in g], opacity=0.35)))
            for mk, box in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in box], lag_ratio=0.08), run_time=1.2)
        self.clear_scene()
