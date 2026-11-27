from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Tools(VoiceoverScene):
    def construct(self):
        card(self, 7, "The tools", "Who sells the shovels in this gold rush?",
             "Chapter seven. The tools.", lit=("moat", "make"))
        self.asml()
        self.others()
        self.upstream()

    def asml(self):
        T = R["tools"]
        hist = T["asml_hist"]
        ys = sorted(y for y in hist if y >= 2019)
        pa = viz.plot_axes([2018.4, 2025.6], [0, 36], x_length=6.0, y_length=4.2, xticks=ys, yticks=[10, 20, 30],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"€{v:.0f}bn", ylabel="ASML, revenue", size=12).move_to([-3.4, -0.4, 0])
        bars = VGroup()
        for y in ys:
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            bars.add(Rectangle(width=0.5, height=pa.ax.c2p(y, hist[y])[1] - y0, stroke_width=0, fill_color=GROUP_COL["equipment"], fill_opacity=0.85).move_to(
                [x0, y0, 0], aligned_edge=DOWN))
        machine = VGroup(RoundedRectangle(corner_radius=0.1, width=2.6, height=1.4, stroke_color=LIGHT, stroke_width=3, fill_color="#1B2230", fill_opacity=1),
                         tx("EUV", 26, LIGHT, bold=True)).move_to([3.4, 1.7, 0])
        facts = VGroup(tx(f"2025: {T['asml_units']:.0f} lithography systems sold,", 16, WHITE),
                       tx(f"{T['asml_euv']:.0f} of them EUV", 18, LIGHT, bold=True),
                       tx(f"revenue €{T['asml_rev']:.1f}bn, gross margin {T['asml_gm']:.1f}%", 16, WHITE),
                       tx("'the world's only manufacturer of", 15, GREY_A), tx("EUV lithography systems'", 15, GREY_A),
                       tx("its lenses and mirrors: one supplier, Carl Zeiss SMT", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([3.4, -1.0, 0])
        src = source("SEC EDGAR: ASML Holding, Forms 20-F (US GAAP, euros), 2019-2025; Form 20-F 2025", size=13)
        with self.voiceover(
            "A fab's machines come from specialist makers, and at the very front there is only one. "
            "<bookmark mark='a'/> ASML, a Dutch company, sold "
            f"€{T['asml_rev']:.1f} billion of machines and service in 2025. <bookmark mark='b'/> It sold "
            f"{T['asml_units']:.0f} lithography systems, {T['asml_euv']:.0f} of them the extreme-ultraviolet machines that "
            "print the finest layers of the newest chips. It is, in its own words, the world's only manufacturer of "
            "them, and their optics come from one supplier, Carl Zeiss. <bookmark mark='c'/> One maker of the machine "
            "the newest chips need: which is why, as we will see, governments decide who may buy one."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(bars)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(machine, scale=0.9), FadeIn(facts[:3]))
            self.play(FadeIn(facts[3:]))
            vo.wait_until("c")
            self.play(Indicate(machine, color=LIGHT, scale_factor=1.05))
        self.clear_scene()

    def others(self):
        T = R["tools"]["companies"]
        rows = [("AMAT", "deposition, etch and more"), ("LRCX", "etch and deposition"), ("KLAC", "inspection and measurement"),
                ("SNPS", "design software"), ("CDNS", "design software")]
        sc = 6.0 / 30
        bars = VGroup()
        for i, (tk, what) in enumerate(rows):
            c = T[tk]
            y = 1.9 - 0.95 * i
            col = GROUP_COL["equipment"] if i < 3 else GROUP_COL["design software"]
            b = Rectangle(width=c["revenue"] * sc, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-2.4, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(VGroup(tx(NAMES[tk], 17, WHITE, bold=True), tx(what, 12, GREY_A)).arrange(DOWN, aligned_edge=RIGHT, buff=0.03).next_to([-2.55, y, 0], LEFT, buff=0),
                            b, tx(f"${c['revenue']:.1f}bn; kept {100 * c['net'] / c['revenue']:.0f}%", 15, col, bold=True).next_to(b, RIGHT, buff=0.12)))
        head = tx("The other toolmakers, latest fiscal year: revenue and profit kept", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR: Forms 10-K of Applied Materials, Lam Research, KLA, Synopsys and Cadence", size=13)
        with self.voiceover(
            "Behind ASML stand a few more specialists. <bookmark mark='a'/> Applied Materials, Lam Research and KLA make "
            "many of the other machines: the ones that lay down films, etch them away, and inspect the wafer for flaws. "
            "<bookmark mark='b'/> And Synopsys and Cadence sell the software that chip designers use to draw billions "
            "of transistors and check that they will work. <bookmark mark='c'/> Every one of them kept at least "
            f"{100 * min(c['net'] / c['revenue'] for c in T.values()):.0f} per cent of its revenue as profit in its latest "
            "year. In a gold rush, the shovel makers do well whoever strikes gold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[0]) for b_ in bars], FadeIn(ghost(*[b_[1] for b_ in bars])))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2])) for b_ in bars[:3]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2])) for b_ in bars[3:]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Indicate(b_[2], scale_factor=1.05) for b_ in bars])
        self.clear_scene()

    def upstream(self):
        S, T, F = R["split"], R["tools"], R["fab"]
        rev, gm = S["nvda_rev"], R["markets"]["nvda_gm"] / 100
        cost = rev * (1 - gm)
        tsm = get("tsm.rev.2025.usd")
        sc = 10.0 / 220
        x0 = -5.2

        def bar(w, col, y, op=0.85):
            return Rectangle(width=w * sc, height=0.55, stroke_width=0, fill_color=col, fill_opacity=op).move_to([x0, y, 0], aligned_edge=LEFT)
        y1, y2, y3 = 2.1, 0.1, -1.9
        gp = bar(rev * gm, GOOD, y1)
        cs = bar(cost, PRICE, y1).next_to(gp, RIGHT, buff=0.04)
        l1 = tx("Nvidia, year to January 2026", 15, WHITE, bold=True).next_to(gp, UP, buff=0.08).align_to(gp, LEFT)
        gpl = tx(f"kept as gross profit: ${rev * gm:.0f}bn ({100 * gm:.0f}%)", 14, "#0E1117", bold=True).move_to(gp)
        csl = tx(f"cost: ${cost:.0f}bn", 13, "#0E1117", bold=True).move_to(cs)
        what = VGroup(tx("wafers: TSMC, Samsung", 12, GREY_A), tx("memory: SK hynix, Micron, Samsung", 12, GREY_A),
                      tx("CoWoS packaging; assembly: Hon Hai, Wistron, Fabrinet", 12, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).next_to(cs, DOWN, buff=0.1).align_to(cs, LEFT)
        tb = bar(tsm, GROUP_COL["foundry"], y2)
        top = bar(tsm * S["top1"] / 100, WHITE, y2, op=0.35).align_to(tb, RIGHT)
        l2 = tx("TSMC, 2025: revenue from all its customers", 15, WHITE, bold=True).next_to(tb, UP, buff=0.08).align_to(tb, LEFT)
        tbl = tx(f"${tsm:.0f}bn", 15, "#0E1117", bold=True).move_to(tb).align_to(tb, LEFT).shift(RIGHT * 0.15)
        topl = tx(f"largest customer: {S['top1']:.0f}%", 12, WHITE).next_to(top, RIGHT, buff=0.1)
        cx = bar(F["capex25"], GROUP_COL["equipment"], y2 - 0.75).align_to(tb, LEFT)
        cxl = tx(f"spent on fabs and tools: ${F['capex25']:.0f}bn", 13, GROUP_COL["equipment"], bold=True).next_to(cx, RIGHT, buff=0.12)
        tools = VGroup()
        x = x0
        for tk in ("AMAT", "LRCX", "KLAC"):
            v = T["companies"][tk]["revenue"]
            b_ = Rectangle(width=v * sc, height=0.55, stroke_width=0, fill_color=GROUP_COL["equipment"], fill_opacity=0.6).move_to([x, y3, 0], aligned_edge=LEFT)
            t_l = tx(f"{NAMES[tk].split()[0]} ${v:.0f}bn", 12, WHITE, bold=True).move_to(b_)
            if t_l.width > b_.width - 0.1:
                t_l.scale_to_fit_width(b_.width - 0.1)
            tools.add(VGroup(b_, t_l))
            x += v * sc + 0.06
        asml = tx(f"and ASML: €{T['asml_rev']:.1f}bn", 14, GROUP_COL["equipment"], bold=True).next_to(tools, RIGHT, buff=0.2)
        l3 = tx("the toolmakers, latest fiscal year: revenue", 15, WHITE, bold=True).next_to(tools, UP, buff=0.08).align_to(tools, LEFT)
        a1 = Arrow(cs.get_bottom() + DOWN * 0.55, tb.get_top() + UP * 0.35 + RIGHT * 2.0, color=GREY_B, stroke_width=2.5, buff=0.05)
        a2 = Arrow(cx.get_bottom(), tools.get_top() + UP * 0.35, color=GREY_B, stroke_width=2.5, buff=0.08)
        src = source("NVIDIA, Form 10-K FY2026 (revenue, gross margin, suppliers); TSMC, Form 20-F 2025; Forms 10-K of Applied "
                     "Materials, Lam Research and KLA; ASML, Form 20-F 2025", size=12)
        with self.voiceover(
            "Now follow the money upstream, from the chip to the machines. <bookmark mark='a'/> In the year to January "
            f"2026 Nvidia sold ${rev:.0f} billion of chips and systems, and kept {100 * gm:.0f} dollars of every hundred "
            f"as gross profit. <bookmark mark='b'/> The rest, about ${cost:.0f} billion, paid for making them: wafers "
            "from its foundries, TSMC and Samsung; memory from SK hynix, Micron and Samsung; packaging; and assembly by "
            f"contract manufacturers. <bookmark mark='c'/> Upstream, TSMC took in ${tsm:.0f} billion in 2025 from all its "
            f"customers, its largest alone bringing in {S['top1']:.0f} per cent. <bookmark mark='d'/> It spent "
            f"${F['capex25']:.0f} billion on fabs and tools, <bookmark mark='e'/> money that flows on to the toolmakers: "
            "Applied Materials, Lam Research, KLA and ASML. At every step the stream is smaller, and at every step a "
            "company with few rivals keeps a large share of it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(l1), FadeIn(l2), FadeIn(l3), FadeIn(ghost(gp, cs, tb, cx, *[t_[0] for t_ in tools], opacity=0.3)))
            vo.wait_until("a")
            self.play(GrowFromEdge(gp, LEFT), GrowFromEdge(cs, LEFT), run_time=1.5)
            self.play(FadeIn(gpl), FadeIn(csl))
            vo.wait_until("b")
            self.play(Indicate(cs, color=PRICE, scale_factor=1.03), FadeIn(what, shift=DOWN * 0.1))
            vo.wait_until("c")
            coins, anim = draw.coin_flow(cs.get_center(), tb.get_right() + LEFT * 0.4, n=8, arc=-0.4)
            self.add(coins)
            self.play(anim, GrowFromEdge(tb, LEFT), Create(a1), run_time=1.6)
            self.remove(coins)
            self.play(FadeIn(tbl), FadeIn(top), FadeIn(topl))
            vo.wait_until("d")
            self.play(GrowFromEdge(cx, LEFT), FadeIn(cxl))
            vo.wait_until("e")
            coins, anim = draw.coin_flow(cx.get_center(), tools.get_center(), n=6, arc=-0.4)
            self.add(coins)
            self.play(anim, Create(a2), LaggedStart(*[GrowFromEdge(t_[0], LEFT) for t_ in tools], lag_ratio=0.2), run_time=1.6)
            self.remove(coins)
            self.play(*[FadeIn(t_[1]) for t_ in tools], FadeIn(asml))
        self.clear_scene()
