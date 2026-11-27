from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403

STAGE = {"CF": ("inputs", COST), "DE": ("inputs", COST), "MOS": ("inputs", COST), "CTVA": ("inputs", COST),
         "ADM": ("traders", TRADE), "BG": ("traders", TRADE), "TSN": ("meat", MEAT), "PPC": ("meat", MEAT),
         "HRL": ("meat", MEAT), "PEP": ("brands", BRAND), "MDLZ": ("brands", BRAND), "GIS": ("brands", BRAND),
         "KHC": ("brands", BRAND), "HSY": ("brands", BRAND), "KR": ("shops", SHOP)}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 13, "The landscape, November 2026", "Who are the companies of the food chain, and how are they doing?",
             "Chapter thirteen. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.bubbles()
        self.watch()

    def bubbles(self):
        C = {c["ticker"]: c for c in R["chain"]["companies"]}
        pa = viz.plot_axes([np.log10(4), np.log10(200)], [-0.04, 0.24], x_length=9.0, y_length=5.0,
                           xticks=[np.log10(v) for v in (5, 10, 20, 50, 100, 200)], yticks=[0, 0.05, 0.1, 0.15, 0.2],
                           xfmt=lambda v: f"${10 ** v:,.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of sales, average 2021-2025", size=14).move_to([-1.4, -0.35, 0])
        xl = tx("revenue in the latest year (log scale)", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        zero = Line(pa.ax.c2p(np.log10(4), 0), pa.ax.c2p(np.log10(200), 0), stroke_color=GREY_B, stroke_width=1.2)
        bub = VGroup()
        for t, (stage, col) in STAGE.items():
            c = C[t]
            p = pa.ax.c2p(np.log10(c["revenue"]), c["margin5"])
            d = VGroup(Circle(0.07 * np.sqrt(c["revenue"]) ** 0.75, stroke_color=col, stroke_width=2, fill_color=col,
                              fill_opacity=0.4).move_to(p), tx(c["name"], 13, WHITE, bold=True))
            d[1].next_to(d[0], UP, buff=0.04)
            bub.add(d)
        order = ["inputs", "traders", "meat", "brands", "shops"]
        key = VGroup(*[VGroup(Dot(radius=0.09, color={"inputs": COST, "traders": TRADE, "meat": MEAT, "brands": BRAND,
                                                    "shops": SHOP}[s]),
                              tx(s, 15, WHITE)).arrange(RIGHT, buff=0.1) for s in order]).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.12).move_to(
            [5.4, 1.6, 0])
        absent = VGroup(tx("Not drawn (no US annual filing):", 14, GREY_A),
                        tx(f"Cargill (${R['traders']['cargill']:.0f}bn, private),", 13, GREY_B),
                        tx("Louis Dreyfus, COFCO, Bayer,", 13, GREY_B), tx("Syngenta, Nestlé, Unilever,", 13, GREY_B),
                        tx("WH Group, Yara, JBS's history", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [5.4, -1.3, 0])
        stamp = as_of("as of November 2026")
        head = tx("The food chain's listed companies", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR, Forms 10-K (latest years, mostly 2025); Cargill, 2025 Annual Report", size=13)
        groups = {s: [bub[i] for i, (t, (st, _)) in enumerate(STAGE.items()) if st == s] for s in order}
        with self.voiceover(
            "Here is the landscape, as of November 2026. Each bubble is a company that files its accounts in the "
            "United States, placed by its revenue and by how much of each dollar it kept over five years. "
            "<bookmark mark='a'/> High and to the left, the input makers: CF Industries, Mosaic, Corteva, and Deere, "
            "the biggest of them. <bookmark mark='b'/> Low and to the right, the traders, ADM and Bunge, huge and "
            "thin. <bookmark mark='c'/> The meat companies, Tyson, Pilgrim's and Hormel, low as well. "
            "<bookmark mark='d'/> The brand owners, higher: PepsiCo, by far the largest, Mondelez, General Mills, "
            "Hershey, and Kraft Heinz pulled down by its write-downs. <bookmark mark='e'/> And Kroger, the largest "
            "supermarket chain that sells mostly food, with the thinnest margin of all. <bookmark mark='f'/> Many of "
            "the biggest players are not here at all, because they do not file in the United States: Cargill, the "
            "largest private company in America, Louis Dreyfus, China's COFCO, Bayer, Syngenta, Nestlé and Unilever."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(head), FadeIn(src), FadeIn(stamp), FadeIn(key))
            for s, m in zip(order, "abcde"):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups[s]], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("f")
            self.play(FadeIn(absent))
        self.clear_scene()

    def watch(self):
        I = R["income"]
        C = R["traders"]["crush"]
        items = [(draw.coin_stack(3, r=0.16), "Government payments",
                  f"USDA forecasts ${I['gov2026']:.0f}bn for 2026, after ${I['gov2025']:.0f}bn in 2025"),
                 (draw.cow(0.7), "The cattle herd", "beef at a record; when the herd rebuilds, prices and packers' margins turn"),
                 (draw.bottle(0.6, "#F2C14E", 0.8), "Biofuel rules", f"soybean oil in diesel: the crush margin at ${C['last']:.0f} a tonne"),
                 (draw.cocoa_pod(0.5), "Cocoa", "whether West Africa's crop recovers from disease and weather"),
                 (draw.sack(0.5, label_="N"), "Fertilizer", "natural gas prices and trade in nitrogen and potash"),
                 (draw.coin(0.2), "The farm share", "USDA's next food dollar, for 2026, due in late 2027")]
        rows = VGroup()
        for ic, h, d in items:
            ic.scale_to_fit_height(min(ic.height, 0.5))
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            rows.add(VGroup(ic, VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.04)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -0.4, 0])
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("USDA ERS (farm income, food dollar); IMF prices via FRED", size=13)
        with self.voiceover(
            "And what to watch. <bookmark mark='a'/> Government payments: the Department of Agriculture forecasts "
            f"about {I['gov2026']:.0f} billion dollars for 2026. <bookmark mark='b'/> The cattle herd: beef is at a "
            "record, and when ranchers start keeping heifers to rebuild their herds, prices and the packers' margins "
            "will turn. <bookmark mark='c'/> Biofuel rules, which now decide what soybean oil is worth. "
            "<bookmark mark='d'/> Cocoa, and whether West Africa's trees recover. <bookmark mark='e'/> Fertilizer, which "
            "follows the price of natural gas. <bookmark mark='f'/> And the farm share of the food dollar, which brings "
            "us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
