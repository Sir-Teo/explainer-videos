from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry2.common import *  # noqa: F403


class Profit(VoiceoverScene):
    def construct(self):
        card(self, 16, "Where the profit is", "Which businesses earn the most, and from how many people?",
             "Chapter sixteen. Where the profit is.", lit=("moat",))
        self.profits()
        self.margins()

    def profits(self):
        C = R["companies"]
        top = C["by_profit"]
        mx = max(v for _, v in top)
        bars = VGroup()
        for name, v in top:
            b = Rectangle(width=0.95, height=3.6 * v / mx, fill_color="#B58CFF", fill_opacity=0.85, stroke_width=0)
            bars.add(VGroup(b, TB(f"${v:.0f}bn", 18, "#B58CFF").next_to(b, UP, buff=0.08),
                            T(name, 17, I.TEXT).next_to(b, DOWN, buff=0.12)))
        for i, g in enumerate(bars):
            g.shift(RIGHT * (i * 1.25) - g[0].get_bottom() + np.array([-6.2, -1.4, 0]))
        wm = VGroup(TB(f"${get('oi.walmart.fy2026'):.0f}bn", 18, I.CHANNEL), T("Walmart", 17, I.TEXT))
        wbar = Rectangle(width=0.95, height=3.6 * get("oi.walmart.fy2026") / mx, fill_color=I.CHANNEL,
                         fill_opacity=0.85, stroke_width=0)
        wbar.move_to(np.array([-6.2 + 6 * 1.25 + 0.3, -1.4, 0]), aligned_edge=DOWN)
        wm[0].next_to(wbar, UP, buff=0.08)
        wm[1].next_to(wbar, DOWN, buff=0.12)
        head = T("Operating profit, fiscal years ending June 2025 to March 2026", 22, I.TEXT).to_corner(UL, buff=0.4)
        P = C["per_worker"]
        per = VGroup(T("Operating profit per employee", 22, I.DIM),
                     VGroup(TB(f"${P['nvidia'] / 1e6:.1f} million", 34, "#B58CFF"), T("NVIDIA, about 42,000 people", 18,
                            I.TEXT)).arrange(DOWN, buff=0.04),
                     VGroup(TB(f"${P['walmart'] / 1e3:.0f} thousand", 34, I.CHANNEL), T("Walmart, about 2.1 million "
                            "people", 18, I.TEXT)).arrange(DOWN, buff=0.04)).arrange(DOWN, buff=0.4).move_to(
            RIGHT * 4.6 + DOWN * 0.2)
        src = source("Companies' 10-Ks via SEC structured data; employee counts from each 10-K", size=14)
        with self.voiceover(
            "Last, the profit. <bookmark mark='a'/> The six American companies with the largest operating profit "
            "are all, in one way or another, technology companies: Apple, NVIDIA, Alphabet, Microsoft, Meta and "
            "Amazon. Each made between 80 and 133 billion dollars. <bookmark mark='b'/> Walmart, the largest employer, "
            "made 30 billion. <bookmark mark='c'/> Divide by the people. NVIDIA made about 3.1 million dollars of "
            "operating profit for each of its 42 thousand employees; Walmart about 14 thousand for each of its 2.1 "
            "million. <bookmark mark='d'/> That is chapter seven again, at the scale of companies: where the product "
            "is software, chips designed once and sold millions of times, or a network everyone has to use, a few "
            "people can earn enormous profits. Where the product is a person's work in a shop or a hospital, the "
            "value added goes mostly in wages, and the profit per person is small."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), FadeIn(g[2]))
                                    for g in bars], lag_ratio=0.2), run_time=2.4)
            vo.wait_until("b")
            self.play(GrowFromEdge(wbar, DOWN), FadeIn(wm))
            vo.wait_until("c")
            self.play(FadeIn(per, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(Indicate(per[1], color="#B58CFF", scale_factor=1.05), Indicate(per[2], color=I.CHANNEL,
                                                                                     scale_factor=1.05))
        self.clear_scene()

    def margins(self):
        fig = {"NVIDIA": (get("oi.nvidia.fy2026"), get("rev.nvidia.fy2026")),
               "Microsoft": (get("oi.microsoft.fy2025"), get("rev.microsoft.fy2025")),
               "Meta": (get("oi.meta.2025"), get("rev.meta.2025")),
               "Apple": (get("oi.apple.fy2025"), get("rev.apple.fy2025")),
               "Alphabet": (get("oi.alphabet.2025"), get("rev.alphabet.2025")),
               "Amazon": (get("oi.amazon.2025"), get("rev.amazon.2025")),
               "Walmart": (get("oi.walmart.fy2026"), get("rev.walmart.fy2026")),
               "UnitedHealth": (get("oi.unitedhealth.2025"), get("rev.unitedhealth.2025")),
               "McKesson": (get("oi.mckesson.fy2026"), get("rev.mckesson.fy2026"))}
        m = {n: oi / rev for n, (oi, rev) in fig.items()}
        items = [(n, m[n], "#B58CFF" if m[n] > 0.25 else (I.CHANNEL if m[n] > 0.08 else "#7EC8F5"),
                 f"on ${rev:.0f}bn of sales") for n, (oi, rev) in fig.items()]
        rows = viz.margin_ladder(items, max_value=0.65, bar_len=6.4, row_h=0.5, size=20, name_w=2.6)
        rows.move_to(LEFT * 0.4 + DOWN * 0.3)
        head = T("Operating profit per dollar of sales (operating margin)", 24, I.TEXT).to_edge(UP, buff=0.4)
        note = T("A thin margin turned over many times can still pay well: Part 3", 19, I.DIM).to_edge(DOWN, buff=0.45)
        src = source("Companies' 10-Ks, fiscal years ending June 2025 to March 2026; SEC structured data", corner=UR,
                     size=13).shift(DOWN * 0.45)
        with self.voiceover(
            "Divide each company's profit by its sales and you get its margin: how many cents of each dollar of "
            f"sales it keeps as operating profit. <bookmark mark='a'/> NVIDIA kept {100 * m['NVIDIA']:.0f} cents. "
            f"Microsoft {100 * m['Microsoft']:.0f}, Meta {100 * m['Meta']:.0f}, Apple and Alphabet "
            f"{100 * m['Apple']:.0f}. <bookmark mark='b'/> Amazon kept {100 * m['Amazon']:.0f}, more than half of it "
            f"earned by its cloud. Walmart and UnitedHealth about four cents, and McKesson, the medicine wholesaler, "
            f"one and a half. <bookmark mark='c'/> A thin margin is not a failure. A wholesaler that keeps a cent "
            "and a half of every dollar, but sells its whole stock many times a year, can earn a good return on the "
            "money tied up in it. How margin, speed and borrowing combine into that return is the subject of Part "
            "three: the accounts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:5]], lag_ratio=0.15), run_time=1.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[5:]], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(note), Indicate(rows[-1], color="#7EC8F5", scale_factor=1.04))
        self.clear_scene()
        assert m["NVIDIA"] > 0.55 and m["McKesson"] < 0.02
