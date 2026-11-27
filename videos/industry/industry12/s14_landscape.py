from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403

NAMES = {"DOW": "Dow", "LYB": "LyondellBasell", "WLK": "Westlake", "OLN": "Olin", "HUN": "Huntsman", "EMN": "Eastman",
         "CE": "Celanese", "LIN": "Linde", "APD": "Air Products", "CF": "CF Industries", "MOS": "Mosaic", "ICL": "ICL",
         "SHW": "Sherwin-Williams", "PPG": "PPG", "ECL": "Ecolab", "IFF": "IFF", "DD": "DuPont", "CC": "Chemours"}
GROUP_COL = {"commodity": ETHYL, "industrial gases": GASES, "fertilizer": "#E0B07A", "specialty": PRICE}
SIDE = {"DOW": DOWN, "LYB": UP, "WLK": LEFT, "OLN": UP, "HUN": UP, "EMN": UP, "CE": LEFT, "LIN": UP, "APD": LEFT, "CF": UP,
        "MOS": DOWN, "ICL": UP, "SHW": UP, "PPG": DOWN, "ECL": DOWN + RIGHT * 0.5, "IFF": UP, "CC": DOWN}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who are the chemical companies, and where in the chain do they earn?",
             "Chapter twelve. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.bubbles()
        self.watch()

    def bubbles(self):
        C = [c for c in R["landscape"]["companies"] if c["ticker"] != "DD"]
        L = {c["ticker"]: c for c in C}
        pa = viz.plot_axes([np.log10(4.5), np.log10(55)], [-0.09, 0.24], x_length=9.0, y_length=5.0,
                           xticks=[np.log10(v) for v in (5, 10, 20, 40)], yticks=[-0.05, 0, 0.05, 0.1, 0.15, 0.2],
                           xfmt=lambda v: f"${10 ** v:,.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of sales, five-year average", size=13).move_to([-1.4, -0.35, 0])
        xl = tx("revenue in the latest year (log scale)", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        zero = Line(pa.ax.c2p(np.log10(4.5), 0), pa.ax.c2p(np.log10(55), 0), stroke_color=GREY_B, stroke_width=1.2)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]), c["margin5"])
            d = VGroup(Circle(0.07 * np.sqrt(c["revenue"]) ** 0.8, stroke_color=col, stroke_width=2, fill_color=col,
                              fill_opacity=0.4).move_to(p), tx(NAMES[c["ticker"]], 12, WHITE, bold=True))
            d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        order = ["commodity", "industrial gases", "fertilizer", "specialty"]
        names = {"commodity": "commodity chemicals and plastics", "industrial gases": "industrial gases",
                 "fertilizer": "fertilizer", "specialty": "specialty"}
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(names[g], 15, WHITE)).arrange(RIGHT, buff=0.1) for g in order]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 1.9, 0])
        note = VGroup(tx("Not drawn (no 10-K or 20-F):", 13, GREY_A), tx("BASF, SABIC, Sinopec, Air Liquide,", 12, GREY_B),
                      tx("Yara, Nutrien, Wanhua", 12, GREY_B), tx("DuPont: its accounts are dominated", 12, GREY_B),
                      tx("by businesses sold or spun off", 12, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([5.3, -1.4, 0])
        head = tx("America's listed chemical makers", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        stamp = as_of("as of November 2026")
        src = source("SEC EDGAR: Forms 10-K (net income attributable to the company) and 20-F (ICL); fiscal years to 2025", size=13)
        with self.voiceover(
            "Here is the landscape, as of November 2026: the chemical companies that file annual accounts in America, "
            "by revenue and by how much of each dollar they kept over five years. <bookmark mark='a'/> The commodity "
            f"makers: Dow, the largest, and LyondellBasell, at {100 * L['DOW']['margin5']:.0f} and "
            f"{100 * L['LYB']['margin5']:.0f} cents in the dollar; Westlake, Olin, Eastman, Celanese, Huntsman, all in "
            "single digits, through a boom and a bust. <bookmark mark='b'/> The gas companies, Linde and Air Products, "
            f"around {100 * L['LIN']['margin5']:.0f} cents, the steadiest. <bookmark mark='c'/> Fertilizer: CF at "
            f"{100 * L['CF']['margin5']:.0f}, the highest here, thanks to cheap American gas; Mosaic and ICL near ten. "
            "<bookmark mark='d'/> And the specialty makers, Sherwin-Williams, Ecolab and PPG around eight to ten, with "
            "IFF, after its write-downs, and Chemours, which shares the PFAS bill, at the bottom. The pattern of the whole part: "
            "the money is not in the size of the plant, it is in the price of the molecule going in and the hold on the "
            "customer coming out."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(note), FadeIn(stamp))
            for g, m in zip(order, "abcd"):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups[g]], lag_ratio=0.15), run_time=1.4)
        self.clear_scene()

    def watch(self):
        E = R["europe"]
        F = R["feedstock"]
        eu = E["gas_eu"]
        ms = sorted(eu)
        last = ms[-1]
        higher = [m for m in ms if m < last and eu[m] >= eu[last]]
        items = [(draw.molecule("CH4", bond=0.3), "Europe's gas", f"${eu[last]:.1f} in {mlabel(last)}, the highest since "
                  f"{mlabel(higher[-1]) if higher else 'the record began'}"),
                 (draw.ship(1.2), "American ethane abroad", f"exports a record {F['exports_last']:,.0f} thousand barrels a day in "
                  f"{mlabel(F['exports_last_m'])}; INEOS's Antwerp cracker due to start"),
                 (draw.factory(1.0), "Europe's closures", f"Dow's Böhlen cracker to shut by the end of {R['run']['bohlen']:.0f}"),
                 (draw.sack(0.5, NITRO, label_="N"), "Fertilizer", f"CF's gas cost ${get('cf.gascost.2025'):.2f} in 2025, against "
                  "$2.40 in 2024"),
                 (draw.bottle(0.6), "PFAS", "the 2024 drinking-water limits, the settlements and the lawsuits still open"),
                 (draw.cracker_unit(1.0), "Germany's chemistry", "whether output recovers: our call")]
        rows = VGroup()
        for ic, h, d in items:
            ic.scale_to_fit_height(min(ic.height, 0.5))
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            rows.add(VGroup(ic, VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)))
        for i, r_ in enumerate(rows):
            y = 2.0 - 0.82 * i
            r_[0].move_to([-5.2, y, 0])
            r_[1].move_to([-4.5, y, 0], aligned_edge=LEFT)
        for r_ in rows:
            r_[0].set_opacity(0.3)
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("IMF via FRED; EIA; Dow Inc. and CF Industries, Forms 10-K 2025; US EPA", size=13)
        with self.voiceover(
            "And what to watch. <bookmark mark='a'/> Europe's gas: in "
            f"{mlabel(last)} it cost about {eu[last]:.0f} dollars per million Btu, the highest since "
            f"{mlabel(higher[-1]) if higher else 'the record began'}. <bookmark mark='b'/> American ethane abroad: "
            f"exports reached a record {F['exports_last']:,.0f} thousand barrels a day in {mlabel(F['exports_last_m'])}, "
            "and Europe's new cracker in Antwerp is built to use it. <bookmark mark='c'/> Europe's closures, Dow's "
            f"Böhlen among them. <bookmark mark='d'/> Fertilizer: CF paid {get('cf.gascost.2025'):.2f} dollars for its "
            "gas in 2025, up from 2.40; its margin rides on that number. <bookmark mark='e'/> PFAS: the limits, the "
            "settlements, and the lawsuits still open. <bookmark mark='f'/> And Germany's chemical output, which brings "
            "us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(r_[0].animate.set_opacity(1), FadeIn(r_[1], shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()

