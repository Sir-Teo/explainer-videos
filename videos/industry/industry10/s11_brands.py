from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403

STAGES = [("inputs", ["CF", "DE", "MOS", "CTVA"], COST), ("the farm", ["corn"], CORN), ("traders", ["ADM", "BG"], TRADE),
          ("meat", ["TSN", "PPC", "HRL"], MEAT), ("brands", ["HSY", "GIS", "MDLZ", "PEP", "KHC"], BRAND),
          ("shops", ["COST", "WMT", "KR"], SHOP)]


class Brands(VoiceoverScene):
    def construct(self):
        card(self, 9, "From a bushel to a box", "Along the whole chain, who keeps the most of each dollar?",
             "Chapter nine. From a bushel to a box.", lit=("dollar", "moat"))
        self.smile()
        self.scale_()

    def smile(self):
        C = R["chain"]
        co = {c["ticker"]: c for c in C["companies"]}
        x0 = -6.2
        bars = VGroup()
        stage_labels = VGroup()
        means = []
        x = x0
        for name, tics, col in STAGES:
            start = x
            vals = []
            for t in tics:
                m = C["corn5"] if t == "corn" else co[t]["margin5"]
                n = "growing corn" if t == "corn" else co[t]["name"]
                vals.append(m)
                h = max(m, 0) / 0.22 * 3.6
                b = Rectangle(width=0.48, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                    [x + 0.24, -2.0, 0], aligned_edge=DOWN)
                lab = VGroup(tx(f"{100 * m:.1f}%", 12, WHITE, bold=True).next_to(b, UP, buff=0.04),
                             tx(n, 11, GREY_A).rotate(PI / 2).next_to([x + 0.24, -2.05, 0], DOWN, buff=0.05))
                lab[1].align_to([0, -2.1, 0], UP)
                bars.add(VGroup(b, lab))
                x += 0.58
            means.append(((start + x - 0.1) / 2, float(np.mean(vals))))
            stage_labels.add(tx(name, 17, col, bold=True).move_to([(start + x - 0.1) / 2, 2.55, 0]))
            x += 0.35
        base = Line([x0 - 0.1, -2.0, 0], [x - 0.2, -2.0, 0], stroke_color=GREY_B, stroke_width=1.2)
        curve = VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly(
            [[mx_, -2.0 + mv / 0.22 * 3.6 + 0.35, 0] for mx_, mv in means])
        curve.set_stroke(opacity=0.7)
        head = tx("Profit kept from each dollar of sales, average 2021-2025, from field to shop", 21, WHITE, bold=True
                  ).to_edge(UP, buff=0.3)
        src = source("SEC EDGAR, Forms 10-K (net income / revenue); USDA ERS costs and returns (corn)", size=13)
        with self.voiceover(
            "Now line up the whole chain, from the field to the shop, by how much profit each kind of company keeps "
            "from a dollar of sales. Each bar is one company's average over the five years to 2025. "
            "<bookmark mark='a'/> On the left, the companies that sell to farmers: fertilizer, machinery, seed. Twenty, "
            "fourteen, nine, seven cents on the dollar. <bookmark mark='b'/> Then the farm, a few cents at most. "
            "<bookmark mark='c'/> Then the traders and the meat packers: two to four cents, Hormel's brands a little "
            "more. <bookmark mark='d'/> Then the brand owners, the makers of cereal, snacks and chocolate: ten to "
            "fifteen cents, except Kraft Heinz, about which more in a moment. <bookmark mark='e'/> And then the shops: "
            "two or three cents. <bookmark mark='f'/> It makes a smile. The money is kept at the two ends where "
            "something is hard to copy: a patent, a fertilizer plant, a brand that people ask for by name. In the "
            "middle, where the product is a commodity, a bushel, a carcass or a tonne of soybean meal, competition takes "
            "almost everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(base), FadeIn(stage_labels))
            groups = [bars[0:4], bars[4:5], bars[5:7], bars[7:10], bars[10:15], bars[15:18]]
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                anims = [Indicate(stage_labels[k], scale_factor=1.1)] + [AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in groups[k]]
                if k == 2:
                    anims += [Indicate(stage_labels[3], scale_factor=1.1)] + [AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in groups[3]]
                if k == 4:
                    anims += [Indicate(stage_labels[5], scale_factor=1.1)] + [AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in groups[5]]
                self.play(*anims, run_time=1.6)
            vo.wait_until("f")
            self.play(Create(curve), run_time=2.0)
        self.clear_scene()

    def scale_(self):
        C = R["chain"]
        co = {c["ticker"]: c for c in C["companies"]}
        wm, kr, khc = co["WMT"], co["KR"], co["KHC"]
        circles = VGroup()
        for c, col in ((wm, SHOP), (kr, SHOP), (co["PEP"], BRAND), (co["HSY"], BRAND)):
            r_ = 0.06 * np.sqrt(c["revenue"])
            g = VGroup(Circle(r_, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3),
                       VGroup(tx(c["name"], 15, WHITE, bold=True), tx(f"${c['revenue']:.0f}bn sales", 13, GREY_A),
                              tx(f"{100 * c['margin']:.1f}% kept", 14, col, bold=True)).arrange(DOWN, buff=0.03))
            g[1].move_to(g[0]) if r_ > 0.7 else g[1].next_to(g[0], DOWN, buff=0.08)
            circles.add(g)
        circles.arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to([-1.8, 0.2, 0])
        kh = VGroup(tx("Kraft Heinz, 2025", 20, BRAND, bold=True),
                    tx(f"sales ${khc['revenue']:.1f}bn", 17, WHITE),
                    tx(f"loss ${abs(khc['net']):.1f}bn", 20, STATE, bold=True),
                    tx("after writing down the value of", 15, GREY_A), tx("its brands and acquisitions", 15, GREY_A)
                    ).arrange(DOWN, buff=0.06).move_to([5.0, 0.4, 0])
        head = tx("Thin margins, big numbers; and brands are not forever", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("SEC EDGAR, Forms 10-K, latest years (Walmart and Kroger: years to January 2026)", size=13)
        with self.voiceover(
            "Two footnotes to the smile. <bookmark mark='a'/> A thin margin can still make a giant. Walmart, America's "
            f"biggest grocer, sold about {wm['revenue']:.0f} billion dollars of goods in its latest year and kept about "
            f"{100 * wm['margin']:.0f} cents of each dollar: still about {wm['net']:.0f} billion dollars of profit. "
            "Supermarkets live on turning their stock over quickly, many times a year. <bookmark mark='b'/> And a "
            "brand's power is not permanent. In 2025 Kraft Heinz, the maker of ketchup, cheese slices and macaroni, "
            f"reported a loss of {abs(khc['net']):.1f} billion dollars, mostly because it wrote down the value it puts on "
            "its brands and on the businesses it had bought, as its sales kept shrinking. A brand is a moat only as long "
            "as people keep asking for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in circles], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in kh], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()
