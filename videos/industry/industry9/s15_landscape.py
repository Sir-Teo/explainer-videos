from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

KIND = {"iron": IRON, "copper": COPPER, "gold": GOLDC, "lithium": LITH}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 13, "The landscape, November 2026", "Who are the miners, and how are they doing?",
             "Chapter thirteen. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.bubbles()
        self.watch()

    def bubbles(self):
        L = R["landscape"]
        pa = viz.plot_axes([0, 64], [-0.15, 0.4], x_length=9.0, y_length=5.0, xticks=[0, 20, 40, 60],
                           yticks=[-0.1, 0, 0.1, 0.2, 0.3, 0.4], xfmt=lambda v: f"${v:g}bn",
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income as a share of revenue", size=14
                           ).move_to([-1.4, -0.35, 0])
        xl = tx("revenue, latest financial year", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        zero = Line(pa.ax.c2p(0, 0), pa.ax.c2p(64, 0), stroke_color=GREY_B, stroke_width=1.2)
        bub = VGroup()
        labs = VGroup()
        for c in L:
            col = KIND[c["kind"]]
            p = pa.ax.c2p(c["revenue"], c["margin"])
            b = Circle(0.085 * np.sqrt(c["revenue"]), stroke_color=col, stroke_width=2.5, fill_color=col,
                       fill_opacity=0.35).move_to(p)
            bub.add(b)
            labs.add(VGroup(tx(c["name"], 15, WHITE, bold=True), tx(c["metals"], 12, GREY_A)).arrange(DOWN, buff=0.02))
        for c, b, l_ in zip(L, bub, labs):
            side = {"RIO": UP, "BHP": DOWN, "VALE": DOWN, "FCX": DOWN, "NEM": UP, "SCCO": UP, "ALB": RIGHT}[c["ticker"]]
            l_.next_to(b, side, buff=0.06)
        key = VGroup(*[VGroup(Dot(radius=0.09, color=c), tx(n, 15, WHITE)).arrange(RIGHT, buff=0.1)
                       for n, c in [("iron ore", IRON), ("copper", COPPER), ("gold", GOLDC), ("lithium", LITH)]]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.3, 1.6, 0])
        price = VGroup(tx("copper, September 2026", 15, GREY_A),
                       tx(f"${R['prices']['copper_last']:,.0f} a tonne", 22, COPPER, bold=True),
                       tx("iron ore", 15, GREY_A), tx(f"${R['prices']['nominal']['PIORECRUSDM'][-1]:,.0f} a tonne", 22,
                                                      IRON, bold=True)).arrange(DOWN, buff=0.05).move_to([5.3, -1.0, 0])
        absent = VGroup(tx("Not drawn: they do not file", 13, GREY_B), tx("with the SEC. Codelco, Glencore,", 13, GREY_B),
                        tx("Anglo American, Zijin, Barrick", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.03
                                                                                   ).move_to([5.3, -2.7, 0])
        stamp = as_of("as of November 2026")
        head = tx("The miners that file with the SEC", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR: Forms 20-F (BHP, year to June 2025; Rio Tinto; Vale) and 10-K (Freeport, Southern Copper, "
                     "Newmont, Albemarle), 2025; prices: IMF via FRED", size=13)
        with self.voiceover(
            "So here is the landscape, as of November 2026. <bookmark mark='a'/> Each bubble is a mining company that "
            "files its accounts with the US Securities and Exchange Commission, placed by its revenue in its latest "
            "financial year and by how much of that revenue it kept as profit. <bookmark mark='b'/> The two giants, Rio "
            "Tinto and BHP, each sold more than fifty billion dollars, mostly iron ore, and kept about a sixth of it. "
            "Vale, the third iron ore giant, kept much less. <bookmark mark='c'/> Freeport sells more copper than "
            "almost anyone, but much of Grasberg's and Cerro Verde's profit belongs to its partners, including the "
            "Indonesian state, and the mud rush hurt. Southern Copper, with mines in Peru and Mexico, kept almost a "
            "third of its revenue. <bookmark mark='d'/> Newmont, riding the gold price, did as well. And Albemarle, the "
            "lithium producer, is still losing money. <bookmark mark='e'/> Some of the biggest names are not here, "
            "because they do not file with the SEC: Chile's state-owned Codelco, Glencore, Anglo American, China's "
            "Zijin, and Barrick. <bookmark mark='f'/> Since those accounts closed, copper has risen to a record in "
            f"dollars, about {R['prices']['copper_last']:,.0f} a tonne in September 2026, while iron ore has stayed "
            "around a hundred."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(head), FadeIn(src), FadeIn(stamp))
            vo.wait_until("a")
            self.play(FadeIn(key))
            vo.wait_until("b")
            idx = {c["ticker"]: k for k, c in enumerate(L)}
            for t_ in ("RIO", "BHP", "VALE"):
                self.play(GrowFromCenter(bub[idx[t_]]), FadeIn(labs[idx[t_]]), run_time=0.7)
            vo.wait_until("c")
            for t_ in ("FCX", "SCCO"):
                self.play(GrowFromCenter(bub[idx[t_]]), FadeIn(labs[idx[t_]]), run_time=0.7)
            vo.wait_until("d")
            for t_ in ("NEM", "ALB"):
                self.play(GrowFromCenter(bub[idx[t_]]), FadeIn(labs[idx[t_]]), run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(absent))
            vo.wait_until("f")
            self.play(FadeIn(price, shift=UP * 0.1))
        self.clear_scene()

    def watch(self):
        items = [(draw.mill_drum(0.32), "Escondida's grade", "BHP expects 0.85% this year, and 900-1,000 kt a year to 2031"),
                 (draw.open_pit(0.9, 0.4, benches=2), "Grasberg's restart", "a phased restart of the block cave from 2026"),
                 (draw.battery(0.6, "#5DA9E9", 0.5), "Congo's cobalt quotas", "96,600 t a year in 2026 and 2027"),
                 (VGroup(*[Dot(radius=0.08, color=CHINA) for _ in range(3)]).arrange(RIGHT, buff=0.06),
                  "China's export controls", "October's rare-earth controls suspended for a year, to late 2026"),
                 (draw.cathode(0.5), "The tariff gap", "whether New York's copper price stays above London's")]
        rows = VGroup()
        for ic, h, d in items:
            ic.scale_to_fit_height(min(ic.height, 0.5))
            rows.add(VGroup(ic, VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.04)).arrange(
                RIGHT, buff=0.4))
        for r_ in rows:
            r_[0].set_x(-4.6)
            r_[1].next_to(r_[0], RIGHT, buff=0.4).set_x(-4.0 + r_[1].width / 2)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("BHP (2025 results), Freeport-McMoRan 10-K for 2025, USGS Mineral Commodity Summaries 2026", size=13)
        with self.voiceover(
            "And here is what to watch. <bookmark mark='a'/> Escondida's grade, falling towards point eight five "
            "percent this year. <bookmark mark='b'/> Grasberg's restart after the mud rush. <bookmark mark='c'/> "
            "Congo's cobalt quotas, which run through 2027. <bookmark mark='d'/> China's rare-earth controls, half of "
            "which are only suspended. <bookmark mark='e'/> And the gap between New York's copper price and London's, "
            "which measures how much the world expects American tariffs to matter. Every one of those is a story about "
            "rock, or about a state, and none of them is about the demand for copper, which keeps rising regardless."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
