from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

INTEL, HPC, DELLC = "#7EC8F5", "#F2A65A", "#B58CFF"


class PC(VoiceoverScene):
    def construct(self):
        card(self, 8, "The PC, the earlier case", "Who made the money from the personal computer?",
             "Chapter eight. The PC, the earlier case.", lit=("moat", "dollar"))
        self.margins()
        self.volume()
        self.printer()

    def margins(self):
        P = R["pc"]
        series = [("Intel: PC processors", P["intel"], INTEL, (2023, 2024, 2025)),
                  ("HP: personal computers", P["hp"], HPC, (2023, 2024, 2025)),
                  ("Dell: personal computers", P["dell"], DELLC, (2024, 2025, 2026))]
        sc = 9.0
        base = -2.2
        groups = VGroup()
        for gi, (name, d, col, ys) in enumerate(series):
            x0 = -4.4 + 4.4 * gi
            bars = VGroup()
            for j, y in enumerate(ys):
                rev, op = d[y]
                m = op / rev
                b = Rectangle(width=0.7, height=m * sc, stroke_width=0, fill_color=col, fill_opacity=0.5 + 0.2 * j).move_to([x0 - 0.85 + 0.85 * j, base, 0], aligned_edge=DOWN)
                bars.add(VGroup(b, tx(f"{100 * m:.0f}%", 15, col, bold=True).next_to(b, UP, buff=0.06),
                                tx(f"{'FY' if gi else ''}{y}", 11, GREY_B).next_to(b, DOWN, buff=0.08)))
            lab = VGroup(tx(name, 16, col, bold=True), tx(f"revenue ${d[ys[-1]][0]:.0f}bn in {ys[-1]}", 12, GREY_A)).arrange(DOWN, buff=0.04).move_to([x0, base - 0.8, 0])
            groups.add(VGroup(bars, lab))
        zero = Line([-6.3, base, 0], [6.3, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        head = tx("Operating income per dollar of revenue", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Intel, Form 10-K 2025 (Client Computing Group); HP, Form 10-K FY2025 (Personal Systems); Dell, Form 10-K FY2026 "
                     "(Client Solutions Group)", size=12)
        i25 = P["intel"][2025]
        with self.voiceover(
            "Shih drew his curve about the personal computer, and the computer still fits it. A PC is assembled from "
            "standard parts: anyone can buy the same processor, memory and operating system. <bookmark mark='a'/> The "
            f"maker of the processor, Intel's PC chip business, kept {100 * i25[1] / i25[0]:.0f} cents of operating income "
            "on each dollar of sales in 2025, and more the year before. <bookmark mark='b'/> HP, one of the largest makers "
            f"of the computers themselves, kept about {100 * P['hp'][2025][1] / P['hp'][2025][0]:.0f} cents. "
            f"<bookmark mark='c'/> Dell, about {100 * P['dell'][2026][1] / P['dell'][2026][0]:.0f}. The parts that cannot be "
            "swapped earn the money; the box that anyone can put together does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(zero), *[FadeIn(g_[1]) for g_ in groups],
                      FadeIn(ghost(*[b_[0] for g_ in groups for b_ in g_[0]], opacity=0.25)))
            for mk, g_ in zip("abc", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in g_[0]], lag_ratio=0.25), run_time=1.5)
        self.clear_scene()

    def printer(self):
        P = R["pc"]
        (ps_rev, ps_op), (pr_rev, pr_op) = P["hp"][2025], P["hp_print"]
        sc = 0.12
        def block(x, rev, op, col, name, sub):
            r_ = Rectangle(width=1.6, height=rev * sc, stroke_width=0, fill_color=col, fill_opacity=0.3).move_to([x, -2.4, 0], aligned_edge=DOWN)
            o_ = Rectangle(width=1.6, height=op * sc, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x, -2.4, 0], aligned_edge=DOWN)
            lab = VGroup(tx(name, 17, WHITE, bold=True), tx(sub, 12, GREY_A)).arrange(DOWN, buff=0.04).next_to(r_, UP, buff=0.12)
            v = VGroup(tx(f"revenue ${rev:.1f}bn", 14, col), tx(f"operating income ${op:.1f}bn", 14, col, bold=True),
                       tx(f"{100 * op / rev:.1f} cents per dollar", 18, col, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(r_, RIGHT, buff=0.25)
            return VGroup(r_, o_, lab, v)
        pcs = block(-4.6, ps_rev, ps_op, HPC, "HP's computers", "Personal Systems")
        prn = block(0.8, pr_rev, pr_op, PRICE, "HP's printers and ink", f"of which ink and toner: ${P['hp_supplies']:.1f}bn")
        ink = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.32, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.95)
                       for c in ("#00B7EB", "#E0218A", "#F6E000", "#20242C")]).arrange(RIGHT, buff=0.08).move_to([5.4, 2.2, 0])
        src = source("HP Inc., Form 10-K FY2025 (segment results: Personal Systems and Printing; printing revenue by business unit)", size=13)
        with self.voiceover(
            "HP shows the same curve inside one company. <bookmark mark='a'/> Its computers brought in "
            f"${ps_rev:.0f} billion in fiscal 2025 and earned {100 * ps_op / ps_rev:.1f} cents on the dollar. "
            f"<bookmark mark='b'/> Its printing business brought in less than half that, ${pr_rev:.0f} billion, but earned "
            f"more in total: ${pr_op:.1f} billion, {100 * pr_op / pr_rev:.0f} cents on the dollar. <bookmark mark='c'/> "
            f"${P['hp_supplies']:.0f} billion of that revenue was ink and toner: the part bought again and again, for a "
            "machine only one company's cartridges fit."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pcs[2]), FadeIn(prn[2]), FadeIn(ghost(pcs[0], prn[0], opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(pcs[0], DOWN), run_time=1.2)
            self.play(GrowFromEdge(pcs[1], DOWN), FadeIn(pcs[3]))
            vo.wait_until("b")
            self.play(GrowFromEdge(prn[0], DOWN), run_time=1.2)
            self.play(GrowFromEdge(prn[1], DOWN), FadeIn(prn[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.2) for k in ink], lag_ratio=0.2))
        self.clear_scene()

    def volume(self):
        T = R["tariffs"]
        U, V = T["units"]["laptops"]["World"], T["unit_value"]["laptops"]
        ys = [y for y in sorted(U) if y >= 2015]
        sc = 0.025
        bars = VGroup()
        for i, y in enumerate(ys):
            b = Rectangle(width=0.62, height=U[y] * sc, stroke_width=0, fill_color=PARTS, fill_opacity=0.85).move_to([-5.6 + 0.95 * i, -2.5, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{U[y]:.0f}m", 12, PARTS, bold=True).next_to(b, UP, buff=0.05), tx(str(y), 11, GREY_B).next_to(b, DOWN, buff=0.08),
                            tx(f"${V[y]:.0f}", 11, GREY_A).move_to(b).shift(DOWN * (b.height / 2 - 0.2))))
        head = tx("Laptops imported into the United States, each year (inside each bar: average declared value)", 18, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("UN Comtrade: US imports of portable computers (HS 847130), units and value, 2015-2025", size=13)
        with self.voiceover(
            "And the market itself barely grows. <bookmark mark='a'/> America imports about a hundred million laptops a "
            f"year: {U[2015]:.0f} million in 2015, {U[2021]:.0f} million in the pandemic year of 2021, <bookmark mark='b'/> "
            f"{U[2025]:.0f} million in 2025, at an average declared value of about ${V[2025]:.0f}. A market that does not "
            "grow, built from parts anyone can buy, leaves the box makers with thin margins, as HP's and Dell's show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[2]) for b_ in bars], FadeIn(ghost(*[b_[0] for b_ in bars], opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[3])) for b_ in bars[:7]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[3])) for b_ in bars[7:]], lag_ratio=0.2), run_time=1.5)
        self.clear_scene()
