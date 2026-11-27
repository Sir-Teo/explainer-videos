from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

L0 = np.log10(3)
# where each name sits relative to its bubble
SIDE = {"TSM": UP, "GFS": DOWN, "UMC": RIGHT, "INTC": DOWN, "TXN": UP, "MCHP": DOWN, "ON": DOWN, "NXPI": RIGHT,
        "STM": LEFT, "NVDA": DOWN, "AVGO": UP, "QCOM": DOWN, "AMD": DOWN, "MRVL": DOWN, "MU": DOWN,
        "KLAC": LEFT, "SNPS": UP, "CDNS": LEFT, "AMKR": LEFT}
# crowded ones: a label placed at (revenue, margin) with a leader line
LEADER = {"AMAT": (52, 0.41), "LRCX": (27, 0.35), "ADI": (19, 0.105)}
ORDER = [("foundry", "a"), ("fabless", "b"), ("memory", "c"), ("integrated", "d"), ("equipment", "e"), ("design software", "e"),
         ("packaging", "e")]


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who designs, who makes, who sells the tools?",
             "Chapter twelve. The landscape, November 2026.", lit=("sold", "moat", "change"))
        self.bubbles()
        self.watch()

    def bubbles(self):
        C = R["landscape"]["companies"]
        L = {c["ticker"]: c for c in C}
        pa = viz.plot_axes([0, np.log10(300) - L0], [-0.05, 0.5], x_length=8.8, y_length=5.0,
                           xticks=[np.log10(v) - L0 for v in (3, 10, 30, 100, 300)], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                           xfmt=lambda v: f"${10 ** (v + L0):g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of revenue, five-year average", size=13).move_to([-1.7, -0.4, 0])
        xl = tx("revenue, latest fiscal year (log scale)", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(np.log10(300) - L0, 0), stroke_color=GREY_B, stroke_width=1.2, dash_length=0.08)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]) - L0, c["margin5"])
            d = VGroup(Circle(0.07 + 0.045 * np.sqrt(c["revenue"]), stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.4).move_to(p),
                       tx(NAMES[c["ticker"]], 12, WHITE, bold=True))
            if c["ticker"] in LEADER:
                rv, mg = LEADER[c["ticker"]]
                d[1].move_to(pa.ax.c2p(np.log10(rv) - L0, mg))
                end = d[1].get_bottom() if d[1].get_center()[1] > p[1] else d[1].get_top()
                ln = Line(d[0].get_center(), end, stroke_color=GREY_B, stroke_width=1.2)
                ln.put_start_and_end_on(d[0].point_at_angle(np.arctan2(end[1] - p[1], end[0] - p[0])), end)
                d.add(ln)
            else:
                d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(g, 14, WHITE)).arrange(RIGHT, buff=0.1)
                       for g in ("foundry", "fabless", "memory", "integrated", "equipment", "design software", "packaging")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.3, 1.7, 0])
        note = VGroup(tx("Not drawn (no American filings):", 13, GREY_A), tx("Samsung Electronics, SK hynix (Korea)", 12, GREY_B),
                      tx("SMIC, Hua Hong (China)", 12, GREY_B), tx("MediaTek (Taiwan)", 12, GREY_B),
                      tx("Tokyo Electron (Japan)", 12, GREY_B), tx("Infineon (Germany)", 12, GREY_B),
                      tx(f"ASML: €{R['landscape']['asml_rev']:.1f}bn, files 20-F in euros", 12, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([5.25, -1.4, 0])
        head = tx("The listed chip companies, by what they do", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        stamp = as_of("as of November 2026")
        src = source("SEC EDGAR: Forms 10-K and 20-F (net income or profit, revenue), last five fiscal years; TSMC and UMC in NT$, "
                     "converted at about 32 to the dollar for size", size=12)
        tsm, nv, mu, intc = L["TSM"], L["NVDA"], L["MU"], L["INTC"]
        with self.voiceover(
            "The landscape, as of November 2026, for the chip companies that file accounts in America. Across: revenue in "
            "the latest year. Up: profit kept per dollar, averaged over five years. <bookmark mark='a'/> The foundries: "
            f"TSMC, with about ${tsm['revenue']:.0f} billion of revenue and about {100 * tsm['margin5']:.0f} cents kept "
            "in every dollar, far above GlobalFoundries and UMC. <bookmark mark='b'/> The fabless designers: Nvidia, the "
            f"biggest of all, with about {100 * nv['margin5']:.0f} cents; Broadcom and Qualcomm behind it; AMD and Marvell "
            f"kept much less. <bookmark mark='c'/> Micron, the memory maker: ${mu['revenue']:.0f} billion in its latest "
            f"year, but only about {100 * mu['margin5']:.0f} cents on average across the cycle. <bookmark mark='d'/> The "
            f"integrated makers: Intel, ${intc['revenue']:.0f} billion of revenue and about one cent kept on average; the "
            "analog makers, smaller and steadier. <bookmark mark='e'/> And the toolmakers, design-software companies and "
            "Amkor, the packager. Beyond the chart, with no American filings: Samsung and SK hynix in Korea, SMIC in "
            "China, MediaTek in Taiwan, Tokyo Electron in Japan, Infineon in Germany."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(zero), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(stamp))
            done = set()
            for g, mk in ORDER:
                if mk not in done:
                    vo.wait_until(mk)
                    done.add(mk)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups[g]], lag_ratio=0.12), run_time=1.0 + 0.1 * len(groups[g]))
            self.play(FadeIn(note, shift=LEFT * 0.1))
        self.clear_scene()

    def watch(self):
        F = R["fab"]
        items = [(draw.chip(0.5, PRICE), "Memory prices", "the boom in DRAM, and when the next bust comes"),
                 (draw.chip_fab(1.0), "TSMC's spending", f"${F['capex26'][0]:.0f}-{F['capex26'][1]:.0f}bn planned for 2026; 2nm ramping"),
                 (draw.wafer(0.5), "Intel 14A", "an outside customer, or a pause"),
                 (draw.capitol(0.7), "The rules", "who may buy, and who may rent, the newest chips"),
                 (draw.car(0.9), "The trailing edge", "cars and factories: when the analog makers recover"),
                 (draw.server_rack(0.6), "World chip sales in 2026", "our call")]
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
        src = source("TSMC, Form 20-F 2025; Intel, Form 10-K 2025; Federal Register, 91 FR 74970", size=13)
        with self.voiceover(
            "What to watch. <bookmark mark='a'/> Memory prices, and when the boom turns, as memory booms always have. "
            f"<bookmark mark='b'/> TSMC's spending: {F['capex26'][0]:.0f} to {F['capex26'][1]:.0f} billion dollars planned "
            "for 2026, as its two-nanometre fabs fill. <bookmark mark='c'/> Intel's next process, which it says it may "
            "pause without an outside customer. <bookmark mark='d'/> The rules on who may buy, and now who may rent, the "
            "newest chips. <bookmark mark='e'/> The trailing edge: when cars and factories buy again. "
            "<bookmark mark='f'/> And the size of the whole market this year, which brings us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(r_[0].animate.set_opacity(1), FadeIn(r_[1], shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()
