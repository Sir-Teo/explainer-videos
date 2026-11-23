from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Tiers(VoiceoverScene):
    def construct(self):
        card(self, 13, "Who pays for the memory?", "How did Apple pass the bill on, and to whom?",
             "Chapter thirteen. Who pays for the memory?", lit=("change", "dollar"))
        self.tiers()
        self.margin()

    def tiers(self):
        tiers = R["tiers"]
        pa = viz.plot_axes((0, 4), (0, 560), x_length=9.6, y_length=4.6, yticks=[0, 100, 200, 300, 400, 500],
                           yfmt=lambda v: f"+${v:.0f}", size=17, ylabel="change, 2025 to 2026, per phone"
                           ).shift(DOWN * 0.4 + LEFT * 0.6)
        groups = VGroup()
        for i, t in enumerate(tiers):
            x = i + 0.5
            def bar(v, dx, c, op=0.92):
                p0, p1 = pa.ax.c2p(x + dx, 0), pa.ax.c2p(x + dx, v)
                return Rectangle(width=0.6, height=max(p1[1] - p0[1], 0.02), fill_color=c, fill_opacity=op,
                                 stroke_width=0).move_to(np.array([p0[0], (p0[1] + p1[1]) / 2, 0]))
            price = bar(t["price_up"], -0.2, I.MONEY)
            mem_lo = bar(t["mem_up_lo"], 0.2, I.MEMORY)
            mem_hi = bar(t["mem_up_hi"], 0.2, I.MEMORY, 0.35)
            mem = VGroup(mem_hi, mem_lo)
            lp = TB(f"+${t['price_up']}", 18, I.MONEY).next_to(price, UP, buff=0.08)
            lm = T(f"+${t['mem_up_lo']:.0f}-{t['mem_up_hi']:.0f}", 16, I.MEMORY).next_to(mem_hi, UP, buff=0.08)
            size = f"{t['gb'] // 1024}TB" if t["gb"] >= 1024 else f"{t['gb']}GB"
            xl = VGroup(TB(size, 20, I.TEXT), T(f"${t['old']:,} → ${t['new']:,}", 15, I.DIM)).arrange(DOWN, buff=0.04)
            xl.next_to(pa.ax.c2p(x, 0), DOWN, buff=0.15)
            groups.add(VGroup(price, lp, mem, lm, xl))
        legend = VGroup(VGroup(Square(0.22, fill_color=I.MONEY, fill_opacity=1, stroke_width=0),
                               T("price rise", 18, I.TEXT)).arrange(RIGHT, buff=0.12),
                        VGroup(Square(0.22, fill_color=I.MEMORY, fill_opacity=1, stroke_width=0),
                               T("memory-cost rise (low to high estimate)", 18, I.TEXT)).arrange(RIGHT, buff=0.12)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.4).shift(DOWN * 0.55)
        head = T("iPhone Pro Max, by storage size: 2025 → 2026 list prices", 24, I.TEXT).to_corner(UL, buff=0.4)
        src = source("Apple list prices via MacRumors (2026-09); DRAM and flash costs: WSJ, Counterpoint; this "
                     "film's arithmetic")
        with self.voiceover(
            "So who pays? Apple does not raise every price by the same amount, and that turns out to be the "
            "answer. <bookmark mark='a'/> Take the iPhone Pro Max in each storage size, and set the rise in its US "
            "price from 2025 to 2026 beside the rise in what its memory costs. A phone has the same working memory "
            "in every size, about 106 dollars dearer this year; the storage cost grows with the size. <bookmark "
            "mark='b'/> On the 256- and 512-gigabyte models, the price went up 100 dollars, but the memory went up "
            "by about 140 to 200. Apple absorbed the difference. <bookmark mark='c'/> On the one-terabyte model the "
            "price rose 300 dollars, against a memory rise of about 260 to 300. <bookmark mark='d'/> And on the "
            "two-terabyte model the price rose 500 dollars, against roughly 410 to 500 of extra memory. <bookmark "
            "mark='e'/> The pattern is clear. Buyers of the biggest phones pay for their memory almost dollar for "
            "dollar. Buyers of the cheapest Pro are partly shielded, by Apple's margin."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(legend))
            self.play(LaggedStart(*[FadeIn(g[4]) for g in groups], lag_ratio=0.2))
            vo.wait_until("b")
            for g in groups[:2]:
                self.play(GrowFromEdge(g[0], DOWN), FadeIn(g[1]), GrowFromEdge(g[2], DOWN), FadeIn(g[3]), run_time=0.9)
            vo.wait_until("c")
            self.play(GrowFromEdge(groups[2][0], DOWN), FadeIn(groups[2][1]), GrowFromEdge(groups[2][2], DOWN),
                      FadeIn(groups[2][3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(groups[3][0], DOWN), FadeIn(groups[3][1]), GrowFromEdge(groups[3][2], DOWN),
                      FadeIn(groups[3][3]))
            vo.wait_until("e")
            self.play(Indicate(VGroup(groups[2], groups[3]), color=I.MONEY, scale_factor=1.03))
        self.clear_scene()

    def margin(self):
        gm25, gm26 = get("apple.gm_products.fy2025"), get("apple.gm_products.fy2026")
        pair = VGroup(VGroup(TB(pct(gm25, 1), 38, I.BRAND), T("fiscal 2025", 18, I.DIM)).arrange(DOWN, buff=0.04),
                      VGroup(TB(pct(gm26, 1), 46, I.BRAND), T("fiscal 2026, to September", 18, I.DIM)).arrange(
                          DOWN, buff=0.04)).arrange(RIGHT, buff=1.2, aligned_edge=DOWN)
        q = VGroup(T("Apple's products gross margin", 24, I.TEXT), pair).arrange(DOWN, buff=0.35).shift(UP * 1.1)
        why = VGroup(T("“... primarily due to product mix and tariff refunds, partially offset by higher costs,", 20,
                       I.TEXT), T("including memory.”   Apple, Form 10-K, fiscal 2026", 20, I.TEXT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(q, DOWN, buff=0.5)
        nxt = T("The iPhone 18 went on sale in the last two weeks of that year: the test is fiscal 2027.", 22,
                I.ACCENT).to_edge(DOWN, buff=0.6)
        src = source("Apple Form 10-K FY2026", corner=UR)
        with self.voiceover(
            "Has it hurt Apple yet? <bookmark mark='a'/> Not in the year it has reported. Apple's margin on products "
            "rose, from 36.8 percent in fiscal 2025 to 39.3 percent in the year to September 2026. <bookmark "
            "mark='b'/> Apple's own explanation: a richer mix of products, and refunds of tariffs it had paid, partly "
            "offset by higher costs, including memory. <bookmark mark='c'/> But the iPhone 18 went on sale in the "
            "last two weeks of that fiscal year. The test of who pays for the memory is the year that has just begun."
        ) as vo:
            self.play(FadeIn(src), FadeIn(q[0]))
            vo.wait_until("a")
            self.play(FadeIn(q[1]))
            vo.wait_until("b")
            self.play(FadeIn(why, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.clear_scene()
