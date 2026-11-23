from __future__ import annotations

from videos.industry.industry1.common import *  # noqa: F403


class Cycle(VoiceoverScene):
    def construct(self):
        card(self, 11, "Memory's boom and bust", "Why do memory makers swing from losses to fortunes?",
             "Chapter eleven. Memory's boom and bust.", lit=("make", "change"))
        self.chart()
        self.why()

    def chart(self):
        Y = R["cycle"]
        years, gm, rev = Y["years"], Y["gm"], Y["revenue"]
        pa = viz.plot_axes((2015.4, 2026.6), (-0.15, 0.9), x_length=11.0, y_length=4.6,
                           xticks=[2016, 2018, 2020, 2022, 2024, 2026], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                           xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}%", size=17,
                           ylabel="Micron's gross margin, by fiscal year").shift(DOWN * 0.3 + RIGHT * 0.3)
        bars = VGroup()
        for y, g in zip(years, gm):
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, g)
            h = p1[1] - p0[1]
            bars.add(Rectangle(width=0.62, height=max(abs(h), 0.02), fill_color=I.MEMORY if g > 0 else I.COST,
                               fill_opacity=0.9, stroke_width=0).move_to(np.array([p0[0], p0[1] + h / 2, 0])))
        notes = {2018: "boom", 2019: "glut"}
        labs = VGroup()
        for y, g, b in zip(years, gm, bars):
            if y in (2016, 2018, 2023, 2025, 2026):
                t = TB(pct(g), 17, I.MEMORY if g > 0 else I.COST)
                t.next_to(b, UP if g > 0 else DOWN, buff=0.08)
                labs.add(t)
        tags = VGroup(*[T(n, 16, I.DIM).next_to(pa.ax.c2p(y, -0.15), UP, buff=0.05) for y, n in notes.items()])
        src = source("Micron Forms 10-K, fiscal 2016-2026")
        with self.voiceover(
            "Before the shock, a word about memory itself, because its makers have always lived on a roller coaster. "
            "<bookmark mark='a'/> Here is what Micron, the American memory maker, kept of each dollar of sales in each "
            "of its last eleven fiscal years. <bookmark mark='b'/> 20 percent in 2016. 59 percent at the peak of a "
            "boom in 2018. <bookmark mark='c'/> Then a glut, and by 2023 it was selling memory for less than it cost "
            "to make. <bookmark mark='d'/> Back to 40 percent in 2025, and then 81 percent in 2026, the highest in its "
            "history, on sales that more than tripled."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if g > 0 else UP) for b, g in zip(bars[:3], gm[:3])],
                                  lag_ratio=0.3), FadeIn(labs[0]), FadeIn(labs[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(tags[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if g > 0 else UP) for b, g in zip(bars[3:8], gm[3:8])],
                                  lag_ratio=0.3), FadeIn(labs[2]), FadeIn(tags[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[8:]], lag_ratio=0.4), FadeIn(labs[3:]),
                      run_time=2.0)
        self.clear_scene()

    def why(self):
        steps = ["Memory is a commodity: one maker's chip works like another's, so price is everything",
                 "A memory factory costs many billions and takes years to build",
                 "When prices are high, every maker builds; the new factories open at about the same time",
                 "Supply overshoots, prices collapse, the weakest makers leave",
                 "Today three companies make most of the world's DRAM: Samsung, SK hynix, Micron"]
        loop = VGroup()
        for i, s in enumerate(steps):
            r = VGroup(TB(str(i + 1), 24, I.MEMORY), T(s, 22, I.TEXT)).arrange(RIGHT, buff=0.3)
            if r.width > 12.6:
                r.scale_to_fit_width(12.6)
            loop.add(r)
        loop.arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(UP * 0.3).align_to(LEFT * 6.2, LEFT)
        head = TB("Why memory swings", 30, I.MEMORY).to_edge(UP, buff=0.6)
        tail = T("In 2026 the demand that arrived was new: artificial intelligence. Part 6 returns to the cycle.", 22,
                 I.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why does memory swing like this? <bookmark mark='a'/> Memory is a commodity: one maker's chip does the "
            "same job as another's, so they compete on price. <bookmark mark='b'/> A new memory factory costs many "
            "billions of dollars and takes years to build. <bookmark mark='c'/> So when prices are high, every maker "
            "builds at once, and the new factories open at about the same time. <bookmark mark='d'/> Supply "
            "overshoots, prices collapse, and the weakest makers leave or are bought. <bookmark mark='e'/> After "
            "decades of this, three companies make most of the world's working memory. <bookmark mark='f'/> In 2026 "
            "the demand that arrived was a new kind, from artificial intelligence, and it met an industry with only "
            "three big suppliers. Part 6 of this series is about cycles like this one."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(loop[i], shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("f")
            self.play(FadeIn(tail))
        self.clear_scene()
