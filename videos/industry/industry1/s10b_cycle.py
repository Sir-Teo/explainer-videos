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
        C0, RAD = np.array([0.0, -0.15, 0.0]), 2.35
        ang = {"top": PI / 2, "right": 0.0, "bottom": -PI / 2, "left": PI}
        pos = {k: C0 + RAD * np.array([np.cos(a), np.sin(a), 0]) for k, a in ang.items()}
        ring = Circle(radius=RAD, stroke_color=I.MEMORY, stroke_width=2, stroke_opacity=0.35).move_to(C0)
        # clockwise: top -> right -> bottom -> left -> top
        arrows = VGroup(*[Arc(radius=RAD, start_angle=a - 0.38, angle=-(PI / 2 - 0.76), arc_center=C0,
                              stroke_color=I.MEMORY, stroke_width=4).add_tip(tip_length=0.18)
                          for a in (PI / 2, 0.0, -PI / 2, PI)])
        head = TB("Why memory swings", 30, I.MEMORY).to_edge(UP, buff=0.35)

        # (a) a commodity: two makers' chips, the same job
        twins = VGroup(draw.chip(0.7, color=I.MEMORY), MathTex("=", font_size=48), draw.chip(0.7, color="#8FB3E8")
                       ).arrange(RIGHT, buff=0.3).move_to(C0)
        twins_t = T("one maker's chip does the job of another's", 19, I.DIM).next_to(twins, DOWN, buff=0.2)
        # (b) the factory: billions, and years
        fab = draw.factory(1.5).move_to(pos["top"] + UP * 0.15)
        fab_t = T("billions of dollars, years to build", 18, I.DIM).next_to(fab, UP, buff=0.1)
        # (c) prices high, everyone builds
        tag_hi = VGroup(RoundedRectangle(corner_radius=0.08, width=1.2, height=0.55, stroke_width=0, fill_color=I.PROFIT,
                                         fill_opacity=1), TB("price", 18, "#0E1117")).move_to(pos["right"] + RIGHT * 0.9)
        up = Arrow(tag_hi.get_bottom() + DOWN * 0.45, tag_hi.get_bottom(), buff=0.02, color=I.PROFIT, stroke_width=5)
        fabs = VGroup(*[draw.factory(0.85) for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to(pos["right"] + LEFT * 0.75 + DOWN * 0.1)
        build_t = T("so everyone builds", 18, I.DIM).next_to(fabs, DOWN, buff=0.1)
        # (d) supply overshoots: wafers pile up; the price falls; a maker leaves
        pile = VGroup(*[draw.wafer(0.22, die=0.05) for _ in range(9)])
        for k, w in enumerate(pile):
            r_, c_ = divmod(k, 4)
            w.move_to(pos["bottom"] + np.array([-0.75 + 0.5 * c_ + 0.25 * (r_ % 2), -0.3 + 0.38 * r_, 0]))
        tag_lo = VGroup(RoundedRectangle(corner_radius=0.08, width=1.2, height=0.55, stroke_width=0, fill_color=I.COST,
                                         fill_opacity=1), TB("price", 18, "#0E1117")).move_to(pos["left"] + LEFT * 0.9)
        down = Arrow(tag_lo.get_top() + UP * 0.45, tag_lo.get_top(), buff=0.02, color=I.COST, stroke_width=5)
        glut_t = T("supply overshoots", 18, I.DIM).next_to(pile, DOWN, buff=0.1)
        # (e) the survivors
        three = VGroup(*[VGroup(draw.factory(0.75, color=c), T(n, 16, I.TEXT)).arrange(DOWN, buff=0.06)
                         for n, c in (("Samsung", "#8FB3E8"), ("SK hynix", "#E9A0A0"), ("Micron", I.MEMORY))])
        three.arrange(RIGHT, buff=0.3).move_to(C0)
        tail = T("In 2026 the demand that arrived was new: artificial intelligence. Part 6 returns to the cycle.", 22,
                 I.ACCENT).to_edge(DOWN, buff=0.25)
        dot = glow_dot(pos["top"], color=I.MEMORY, radius=0.1)
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
            self.play(FadeIn(head), Create(ring))
            vo.wait_until("a")
            self.play(FadeIn(twins, scale=0.8), FadeIn(twins_t))
            vo.wait_until("b")
            self.play(FadeIn(fab, shift=UP * 0.2), FadeIn(fab_t), FadeIn(dot))
            vo.wait_until("c")
            self.play(FadeOut(twins), FadeOut(twins_t), MoveAlongPath(dot, arrows[0].copy()), Create(arrows[0]),
                      run_time=1.2)
            self.play(FadeIn(tag_hi), GrowArrow(up))
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.3) for f in fabs], lag_ratio=0.3), FadeIn(build_t))
            vo.wait_until("d")
            self.play(MoveAlongPath(dot, arrows[1].copy()), Create(arrows[1]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(w, shift=DOWN * 0.3) for w in pile], lag_ratio=0.1), FadeIn(glut_t),
                      run_time=1.4)
            self.play(MoveAlongPath(dot, arrows[2].copy()), Create(arrows[2]), run_time=1.0)
            self.play(FadeIn(tag_lo), GrowArrow(down), fabs[2].animate.set_opacity(0.15))
            self.play(MoveAlongPath(dot, arrows[3].copy()), Create(arrows[3]), run_time=1.0)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(t_, scale=0.8) for t_ in three], lag_ratio=0.3))
            vo.wait_until("f")
            self.play(FadeIn(tail))
            self.play(Rotate(VGroup(ring, arrows), angle=-TAU, about_point=C0), run_time=3.0)
        self.clear_scene()
