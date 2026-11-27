from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Split(VoiceoverScene):
    def construct(self):
        card(self, 6, "Fabless and foundry", "Why did most chip companies stop making their own chips?",
             "Chapter six. Fabless and foundry.", lit=("moat", "dollar"))
        self.diagram()
        self.customers()
        self.nvidia()
        self.intel()

    def diagram(self):
        def box(t, sub, col, w=3.4):
            b = RoundedRectangle(corner_radius=0.12, width=w, height=1.0, stroke_color=col, stroke_width=3, fill_color="#151A23", fill_opacity=1)
            return VGroup(b, VGroup(tx(t, 18, col, bold=True), tx(sub, 13, GREY_A)).arrange(DOWN, buff=0.05).move_to(b))
        design = box("Fabless designers", "Nvidia, Broadcom, Qualcomm, AMD", GROUP_COL["fabless"]).move_to([-3.6, 1.6, 0])
        found = box("Foundries", "TSMC, Samsung, GlobalFoundries, UMC", GROUP_COL["foundry"]).move_to([-3.6, -0.6, 0])
        tools = box("Tools, software, cores", "ASML, Applied, Lam, KLA, Synopsys", GROUP_COL["equipment"]).move_to([-3.6, -2.6, 0])
        idm = box("Integrated makers", "Intel, Texas Instruments, Micron", GROUP_COL["integrated"], w=3.6).move_to([3.4, 0.5, 0])
        a1 = Arrow(design.get_bottom(), found.get_top(), color=GREY_B, stroke_width=3, buff=0.08)
        a2 = Arrow(tools.get_top(), found.get_bottom(), color=GREY_B, stroke_width=3, buff=0.08)
        l1 = tx("designs", 13, GREY_B).next_to(a1, RIGHT, buff=0.1)
        l2 = tx("machines", 13, GREY_B).next_to(a2, RIGHT, buff=0.1)
        idm_l = tx("design and make their own chips", 14, GREY_A).next_to(idm, DOWN, buff=0.15)
        brace = Brace(VGroup(design, found), LEFT, color=GREY_B)
        bl = tx("the split", 14, GREY_B).next_to(brace, LEFT, buff=0.1)
        src = source("TSMC, Form 20-F 2025; NVIDIA, Form 10-K FY2026 (its foundries); the companies' filings", size=13)
        with self.voiceover(
            "The Run it chapter's arithmetic split the industry in two. <bookmark mark='a'/> On one side, designers with "
            "no factories at all, called fabless: Nvidia, Broadcom, Qualcomm, AMD. <bookmark mark='b'/> They send their "
            "designs to foundries, which make chips for anyone. <bookmark mark='c'/> Both depend on the toolmakers and the "
            "design-software companies. <bookmark mark='d'/> On the other side, the integrated makers who still design "
            "and make their own: Intel, Texas Instruments, Micron. Nvidia says in its annual report that it uses "
            "foundries such as TSMC and Samsung."
        ) as vo:
            self.play(FadeIn(src), FadeIn(ghost(design, found, tools, idm, opacity=0.35)))
            vo.wait_until("a")
            self.play(FadeIn(design, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(found))
            vo.wait_until("c")
            self.play(FadeIn(tools), GrowArrow(a2), FadeIn(l2), FadeIn(brace), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(idm, shift=LEFT * 0.1), FadeIn(idm_l))
        self.clear_scene()

    def customers(self):
        S = R["split"]
        parts = [("largest customer", S["top1"], "#7BD88F"), ("second", S["top2"], "#5DA9E9"),
                 ("next eight", S["top10"] - S["top1"] - S["top2"], "#9AA3B2"), ("all the rest", 100 - S["top10"], "#3A4152")]
        sc = 10.0 / 100
        x = -5.0
        blocks = VGroup()
        for n, v, col in parts:
            b = Rectangle(width=v * sc, height=1.2, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=0.9).move_to([x, 0.3, 0], aligned_edge=LEFT)
            x += v * sc
            blocks.add(VGroup(b, tx(f"{v:.0f}%", 20, WHITE, bold=True).move_to(b), tx(n, 14, GREY_A).next_to(b, DOWN, buff=0.12)))
        head = tx("TSMC's revenue in 2025, by customer", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
        hist = tx("its ten largest customers: 70% in 2023, 76% in 2024, 78% in 2025", 16, GREY_A).move_to([0, -1.6, 0])
        src = source("TSMC, Form 20-F 2025 (customer concentration; the customers are not named)", size=13)
        with self.voiceover(
            "And the foundry's customers are concentrated. <bookmark mark='a'/> TSMC does not name them, but its "
            f"largest customer brought in {S['top1']:.0f} per cent of its revenue in 2025, <bookmark mark='b'/> the second "
            f"{S['top2']:.0f} per cent, <bookmark mark='c'/> and the ten largest together {S['top10']:.0f} per cent, up from "
            "70 per cent two years earlier. The foundry is shared by hundreds of companies, but paid for by a few."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(*[b_[0] for b_ in blocks])))
            vo.wait_until("a")
            self.play(GrowFromEdge(blocks[0][0], LEFT), FadeIn(blocks[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(blocks[1][0], LEFT), FadeIn(blocks[1][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(blocks[2][0], LEFT), FadeIn(blocks[2][1:]), GrowFromEdge(blocks[3][0], LEFT), FadeIn(blocks[3][1:]), FadeIn(hist))
        self.clear_scene()

    def nvidia(self):
        S = R["split"]
        nv = S["nvda"]
        ys = [y for y in sorted(nv) if y >= 2017]
        pa = viz.plot_axes([2016.4, 2026.6], [0, 240], x_length=8.4, y_length=4.4, xticks=[2017, 2019, 2021, 2023, 2026],
                           yticks=[50, 100, 150, 200], xfmt=lambda v: f"FY{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="Nvidia, each fiscal year (to late January)", size=13).move_to([-1.4, -0.4, 0])
        rb, nb = VGroup(), VGroup()
        for y in ys:
            r_, n_ = nv[y]
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            rb.add(Rectangle(width=0.34, height=pa.ax.c2p(y, r_)[1] - y0, stroke_width=0, fill_color=GROUP_COL["fabless"], fill_opacity=0.85).move_to([x0 - 0.17, y0, 0], aligned_edge=DOWN))
            nb.add(Rectangle(width=0.34, height=max(pa.ax.c2p(y, n_)[1] - y0, 0.01), stroke_width=0, fill_color=PRICE, fill_opacity=0.9).move_to([x0 + 0.17, y0, 0], aligned_edge=DOWN))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=GROUP_COL["fabless"], fill_opacity=0.85), tx("revenue", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color=PRICE, fill_opacity=0.9), tx("profit", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.5).move_to([-1.0, 2.75, 0])
        last = nv[max(ys)]
        side = VGroup(tx(f"FY2026: ${last[0]:.0f}bn of revenue", 18, WHITE, bold=True),
                      tx(f"${last[1]:.0f}bn of profit", 17, PRICE, bold=True),
                      tx(f"data centres: ${S['nvda_dc'][2026]:.0f}bn", 16, GREY_A),
                      tx(f"(FY2024: ${S['nvda_dc'][2024]:.0f}bn)", 14, GREY_B),
                      tx("no fabs: made by foundries", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([4.8, 0.4, 0])
        src = source("SEC EDGAR: NVIDIA, Forms 10-K (revenue, net income), fiscal years 2017-2026", size=13)
        with self.voiceover(
            "The fabless model's biggest winner is Nvidia. <bookmark mark='a'/> Its revenue was about "
            f"${nv[2017][0]:.0f} billion in fiscal 2017. <bookmark mark='b'/> In the year to January 2026 it was about ${last[0]:.0f} billion, with "
            f"about ${last[1]:.0f} billion of profit, <bookmark mark='c'/> ${S['nvda_dc'][2026]:.0f} billion of it from "
            f"chips for data centres, up from ${S['nvda_dc'][2024]:.0f} billion two years before. It owns no fab. Every one "
            "of those chips was made by a foundry."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in rb[:6]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in rb[6:]], lag_ratio=0.15),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in nb], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()

    def intel(self):
        S = R["split"]
        L = S["intel_loss"]
        bars = VGroup()
        for i, (y, v) in enumerate(sorted(L.items())):
            b = Rectangle(width=1.0, height=v * 0.3, stroke_width=0, fill_color=BAD, fill_opacity=0.85).move_to([-4.6 + 1.5 * i, 1.0, 0], aligned_edge=UP)
            bars.add(VGroup(b, tx(f"-${v:.1f}bn", 17, BAD, bold=True).next_to(b, DOWN, buff=0.08), tx(str(y), 15, GREY_A).next_to(b, UP, buff=0.1)))
        head = VGroup(tx("Intel Foundry: operating loss", 20, WHITE, bold=True)).move_to([-3.1, 2.4, 0])
        side = VGroup(tx(f"2025: ${S['intel_rev']:.1f}bn of revenue,", 17, WHITE, bold=True),
                      tx(f"${1000 * S['intel_ext']:.0f}m of it from outside customers", 17, PRICE, bold=True),
                      tx("next process (14A) may be paused without", 15, GREY_A), tx("'a significant external foundry customer'", 15, GREY_A),
                      tx(f"August 2025: {S['intel_usg']:.0f}m shares to the US government,", 15, GREY_A),
                      tx("for CHIPS Act money already promised", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to([3.6, 0.2, 0])
        src = source("Intel Corporation, Form 10-K 2025 (segment results; Intel 14A; the US Government Agreement)", size=13)
        with self.voiceover(
            "The other way, making chips for yourself and others, is the hardest. Intel has tried to become a foundry "
            "too. <bookmark mark='a'/> Its foundry division lost about "
            f"${L[2023]:.0f} billion in 2023, ${L[2024]:.0f} billion in 2024 and ${L[2025]:.0f} billion in 2025. "
            f"<bookmark mark='b'/> Of its ${S['intel_rev']:.0f} billion of revenue in 2025, only about "
            f"${1000 * S['intel_ext']:.0f} million came from outside customers; the rest was Intel's own chips. Intel says "
            "that without a significant outside customer it may pause its next process altogether. <bookmark mark='c'/> In "
            f"August 2025 the US government took {S['intel_usg']:.0f} million Intel shares, in a deal that released the "
            "subsidies it had already promised. A fab needs volume, and volume is exactly what the foundry model gives TSMC and "
            "denies its rivals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[2]) for b_ in bars], FadeIn(ghost(*[b_[0] for b_ in bars])))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], UP), FadeIn(b_[1])) for b_ in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[:4], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(side[4:], shift=LEFT * 0.1))
        self.clear_scene()
