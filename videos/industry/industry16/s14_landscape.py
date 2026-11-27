from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

L0 = np.log10(2)
SIDE = {"AAPL": LEFT, "DELL": DOWN, "HPQ": DOWN, "LOGI": UP, "SONY": UP, "HONHAI": DOWN, "JBL": DOWN, "FLEX": UP,
        "SANM": DOWN, "CLS": UP, "PLXS": DOWN, "BHE": DOWN, "SMCI": UP, "APH": UP, "TEL": DOWN, "GLW": LEFT, "LPL": DOWN,
        "ASX": RIGHT}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who designs, who builds, who makes the parts?",
             "Chapter twelve. The landscape, November 2026.", lit=("sold", "moat", "change"))
        self.scale()
        self.bubbles()
        self.watch()

    def bubbles(self):
        C = R["landscape"]["companies"]
        L = {c["ticker"]: c for c in C}
        pa = viz.plot_axes([0, np.log10(600) - L0], [-0.08, 0.3], x_length=8.8, y_length=5.0,
                           xticks=[np.log10(v) - L0 for v in (2, 5, 20, 50, 200, 500)], yticks=[-0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3],
                           xfmt=lambda v: f"${10 ** (v + L0):g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue, five-year average", size=13).move_to([-1.7, -0.4, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(np.log10(600) - L0, 0), stroke_color=GREY_B, stroke_width=1.2, dash_length=0.08)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]) - L0, c["margin"])
            d = VGroup(Circle(0.06 + 0.035 * np.sqrt(c["revenue"]), stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.4).move_to(p),
                       tx(NAMES[c["ticker"]].replace(" (Foxconn)", ""), 12, WHITE, bold=True))
            d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(g, 15, WHITE)).arrange(RIGHT, buff=0.1)
                       for g in ("brand", "assembler", "components")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 2.1, 0])
        note = VGroup(tx("Not drawn (no American filings):", 13, GREY_A), tx("Samsung Electronics (Korea)", 12, GREY_B),
                      tx("Xiaomi, Lenovo (Hong Kong)", 12, GREY_B), tx("Luxshare, BOE (China)", 12, GREY_B),
                      tx("Pegatron, Quanta, Wistron (Taiwan)", 12, GREY_B), tx("Murata, TDK (Japan)", 12, GREY_B),
                      tx("Hon Hai: two years, 2024-2025", 12, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([5.2, -1.2, 0])
        head = tx("The listed electronics companies, by what they do", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        stamp = as_of("as of November 2026")
        src = source("SEC EDGAR: Forms 10-K and 20-F, last five fiscal years (Sony, LG Display and ASE converted at the Federal "
                     "Reserve's annual rates); Hon Hai, audited statements 2024-2025", size=12)
        ap, hh = L["AAPL"], L["HONHAI"]
        with self.voiceover(
            "The landscape, as of November 2026. Across: revenue in the latest year. Up: profit kept per dollar, averaged "
            f"over five years. <bookmark mark='a'/> The brands: Apple far above the rest, about {100 * ap['margin']:.0f} "
            "cents; Sony, Logitech, HP and Dell much lower. <bookmark mark='b'/> The assemblers, from Hon Hai, the largest by "
            "far, to Jabil, Flex, Sanmina, Celestica, Plexus and Benchmark, all in a thin band near the bottom; Supermicro, "
            "the server maker, a little higher. <bookmark mark='c'/> And the component makers: Amphenol and TE well up the "
            "chart, Corning and ASE between, LG Display below the line. Beyond the chart, with no American filings: "
            "Samsung, Xiaomi, Lenovo, Luxshare, BOE, the Taiwanese assemblers Pegatron, Quanta and Wistron, and Japan's "
            "Murata and TDK."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(zero), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(stamp))
            for g, mk in (("brand", "a"), ("assembler", "b"), ("components", "c")):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups[g]], lag_ratio=0.12), run_time=1.0 + 0.15 * len(groups[g]))
            self.play(FadeIn(note, shift=LEFT * 0.1))
        self.clear_scene()

    def watch(self):
        items = [(draw.phone(0.5), "India's share of America's phones", "more than half in 2026? our call"),
                 (draw.server_rack(0.6), "Servers", "how long the data-centre build-out runs, and who builds it"),
                 (draw.capitol(0.7), "Tariffs", "refunds after the Supreme Court's ruling; the chip investigation"),
                 (draw.chip(0.5, PRICE), "Memory costs", "what the 2026 memory boom does to device prices and margins"),
                 (draw.factory(0.8), "Hon Hai's customers", "the share of its biggest one, 44% in 2025"),
                 (draw.pcb(0.8, BOARD, parts=True), "The laptop's move", "Vietnam, Thailand and Mexico after China")]
        rows = VGroup()
        for i, (ic, h, d) in enumerate(items):
            ic.scale_to_fit_height(min(ic.height, 0.5))
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            y = 2.0 - 0.82 * i
            ic.move_to([-5.2, y, 0])
            t = VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-4.5, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(ic, t))
        for r_ in rows:
            r_[0].set_opacity(0.3)
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("Apple, Form 10-K FY2026; Hon Hai, audited statements 2025; UN Comtrade", size=13)
        with self.voiceover(
            "What to watch. <bookmark mark='a'/> Where America's phones come from: India's share, which brings us to our "
            "call. <bookmark mark='b'/> Servers, and how long the data-centre build-out keeps the assemblers busy. "
            "<bookmark mark='c'/> Tariffs: the refunds after the Supreme Court's ruling, and whatever replaces them. "
            "<bookmark mark='d'/> Memory, whose soaring price Apple already names as a cost. <bookmark mark='e'/> Hon Hai's "
            "biggest customer, and whether its share keeps falling. <bookmark mark='f'/> And the laptop's move out of "
            "China, which happened in three years after five of standing still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(r_[0].animate.set_opacity(1), FadeIn(r_[1], shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()

    def scale(self):
        L = R["landscape"]
        C = R["contract"]["latest"]
        sc = 0.04
        hh = Rectangle(width=1.6, height=L["hh_usd"] * sc / 2, stroke_width=0, fill_color=ASSEMBLER, fill_opacity=0.9).move_to([-3.0, -2.6, 0], aligned_edge=DOWN)
        stack, h0 = VGroup(), -2.6
        labs = VGroup()
        for tk in ("JBL", "FLEX", "SANM", "CLS", "PLXS", "BHE"):
            v = C[tk]["revenue"]
            r_ = Rectangle(width=1.6, height=v * sc / 2, stroke_color="#0E1117", stroke_width=1.5, fill_color=ASSEMBLER, fill_opacity=0.45).move_to([1.6, h0, 0], aligned_edge=DOWN)
            stack.add(r_)
            if v > 10:
                labs.add(tx(f"{NAMES[tk]} ${v:.0f}bn", 12, WHITE).move_to(r_))
            h0 += v * sc / 2
        l1 = VGroup(tx("Hon Hai", 18, WHITE, bold=True), tx(f"about ${L['hh_usd']:.0f}bn, 2025", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(hh, UP, buff=0.12)
        l2 = VGroup(tx("six US-listed contract manufacturers", 16, WHITE, bold=True), tx(f"together about ${L['six']:.0f}bn", 14, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(stack, UP, buff=0.12)
        head = tx("Revenue, latest fiscal year", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Hon Hai, audited statements 2025 (at NT$31.17 to the dollar); Forms 10-K of Jabil, Flex, Sanmina, Celestica, Plexus and Benchmark", size=12)
        with self.voiceover(
            "First, scale. <bookmark mark='a'/> Hon Hai took in about "
            f"${L['hh_usd']:.0f} billion in 2025. <bookmark mark='b'/> The six contract manufacturers that file accounts in "
            f"America took in about ${L['six']:.0f} billion between them in their latest years. Hon Hai alone is more than "
            "two and a half times their size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(l1[0]), FadeIn(l2[0]), FadeIn(ghost(hh, stack, opacity=0.4)))
            vo.wait_until("a")
            self.play(GrowFromEdge(hh, DOWN), FadeIn(l1[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in stack], lag_ratio=0.2), FadeIn(labs), FadeIn(l2[1]), run_time=1.8)
        self.clear_scene()
