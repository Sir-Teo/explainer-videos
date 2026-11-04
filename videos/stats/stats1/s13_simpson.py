from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Simpson(VoiceoverScene):
    def construct(self):
        self.card()
        self.overall()
        self.split()
        self.weights()
        self.which()
        self.ecological()

    def card(self):
        card = chapter_card(12, r"The trap of aggregation", r"Better in every group, worse overall?", lit=(),
                            part=PART)
        with self.voiceover("Chapter twelve. The trap of aggregation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bar(self, ax, x, v, col, w=0.7):
        lo, hi = ax.c2p(x - w / 2, 0), ax.c2p(x + w / 2, v)
        r = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
        r.move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0])
        t = MathTex(rf"{100 * v:.1f}\%", font_size=28, color=col).next_to(r, UP, buff=0.1)
        return VGroup(r, t)

    def overall(self):
        d = load("simpson")
        A = axes([0, 7], [0, 1], x_length=10.0, y_length=4.4, ylabel=r"recovered", yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[0, -0.5, 0])
        A.ax.x_axis.set_opacity(0.5)
        ax = A.ax
        bt = self.bar(ax, 3.0, d["all_t_rate"], S.TREAT)
        bu = self.bar(ax, 4.0, d["all_u_rate"], S.CTRL)
        lab = VGroup(VGroup(label(r"treated", font_size=24, color=S.TREAT),
                            label(rf"${fmt_int(d['all_t_n'])}$", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.06)
                     .next_to(ax.c2p(3.0, 0), DOWN, buff=0.15).shift(LEFT * 0.15),
                     VGroup(label(r"untreated", font_size=24, color=S.CTRL),
                            label(rf"${fmt_int(d['all_u_n'])}$", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.06)
                     .next_to(ax.c2p(4.0, 0), DOWN, buff=0.15).shift(RIGHT * 0.15))
        title = label(r"the World's clinic", font_size=32, color=GREY_A).to_edge(UP, buff=0.5)
        tag = simulated_tag(rf"simulated: the World's clinic, \ {fmt_int(d['n'])} patients", corner=UR)
        with self.voiceover(
            f"The World has a clinic. <bookmark mark='a'/> Over the years it has seen {money(d['n'])} patients with "
            "the same illness. Some were given a new treatment; some weren't. <bookmark mark='b'/> Of those treated, "
            f"{pct(d['all_t_rate'])} percent recovered. Of those not treated, {pct(d['all_u_rate'])} percent. "
            "<bookmark mark='c'/> On these numbers the treatment looks harmful: eleven points worse. Should the "
            "clinic stop using it?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(title), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lab))
            vo.wait_until("b")
            self.play(GrowFromEdge(bt[0], DOWN), FadeIn(bt[1]), GrowFromEdge(bu[0], DOWN), FadeIn(bu[1]))
            vo.wait_until("c")
            self.play(Indicate(bt, color=S.RESID, scale_factor=1.05))
        self.A, self.bt, self.bu, self.lab, self.title, self.tag = A, bt, bu, lab, title, tag

    def split(self):
        d = load("simpson")
        ax = self.A.ax
        bars = VGroup(self.bar(ax, 1.0, d["mild_t_rate"], S.TREAT), self.bar(ax, 2.0, d["mild_u_rate"], S.CTRL),
                      self.bar(ax, 5.0, d["severe_t_rate"], S.TREAT), self.bar(ax, 6.0, d["severe_u_rate"], S.CTRL))
        groups = VGroup(label(r"mild illness", font_size=26).next_to(ax.c2p(1.5, 0), DOWN, buff=0.5),
                        label(r"severe illness", font_size=26).next_to(ax.c2p(5.5, 0), DOWN, buff=0.5))
        ns = VGroup(*[label(rf"${fmt_int(n)}$", font_size=20, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.12)
                      for x, n in ((1, d["mild_t_n"]), (2, d["mild_u_n"]), (5, d["severe_t_n"]), (6, d["severe_u_n"]))])
        arrows = VGroup(Arrow(bars[1][0].get_top() + UP * 0.45, bars[0][0].get_top() + UP * 0.45, buff=0.1,
                              color=S.KEPT, stroke_width=4),
                        Arrow(bars[3][0].get_top() + UP * 0.45, bars[2][0].get_top() + UP * 0.45, buff=0.1,
                              color=S.KEPT, stroke_width=4))
        with self.voiceover(
            "Before deciding, look at who was treated. The illness comes in two forms, mild and severe. "
            "<bookmark mark='a'/> Split the patients by severity. Among the mild cases, "
            f"{pct(d['mild_t_rate'])} percent of the treated recovered, against {pct(d['mild_u_rate'])} percent of "
            f"the untreated. <bookmark mark='b'/> Among the severe cases, {pct(d['severe_t_rate'])} percent against "
            f"{pct(d['severe_u_rate'])}. <bookmark mark='c'/> The treatment is better in each group, by about eight "
            "points, and worse when the groups are combined. Nothing is miscounted. Every patient is in exactly one "
            "group and in the total. This is Simpson's paradox, described by Yule in 1903 and by Simpson in 1951."
        ) as vo:
            vo.wait_until("a")
            ov = label(r"overall", font_size=24, color=GREY_C).next_to(ax.c2p(3.5, 0), DOWN, buff=0.5)
            self.play(FadeOut(self.lab), self.bt.animate.set_opacity(0.15), self.bu.animate.set_opacity(0.15),
                      FadeIn(ov))
            self.play(FadeIn(groups[0]), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]),
                      GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), FadeIn(ns[:2]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]), GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]),
                      GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]), FadeIn(ns[2:]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]))
        self.clear_scene()

    def weights(self):
        d = load("simpson")
        A = axes([0.3, 0.95], [0, 3], x_length=11.0, y_length=3.2, xlabel=r"recovery rate",
                 xticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9], xfmt=lambda v: rf"{int(round(100 * v))}\%",
                 center=[0, -0.6, 0])
        A.ax.y_axis.set_opacity(0)
        ax = A.ax
        rows = []
        for y, key, col, name in ((2.2, "t", S.TREAT, r"treated"), (0.9, "u", S.CTRL, r"untreated")):
            sv, ml = d[f"severe_{key}_rate"], d[f"mild_{key}_rate"]
            w = d[f"share_severe_{key}"]
            seg = Line(ax.c2p(sv, y), ax.c2p(ml, y), color=col, stroke_width=6)
            ends = VGroup(label(r"severe", font_size=20, color=GREY_B).next_to(ax.c2p(sv, y), UP, buff=0.12),
                          label(r"mild", font_size=20, color=GREY_B).next_to(ax.c2p(ml, y), UP, buff=0.12))
            tr = ValueTracker(0.5)
            dot = always_redraw(lambda tr=tr, sv=sv, ml=ml, y=y, col=col: Dot(
                ax.c2p(tr.get_value() * sv + (1 - tr.get_value()) * ml, y), radius=0.13, color=WHITE, stroke_width=3,
                stroke_color=col))
            nm = label(name, font_size=26, color=col).next_to(ax.c2p(0.3, y), LEFT, buff=0.15)
            share = label(rf"{pct(w, 0)}\% severe", font_size=22, color=col).next_to(ax.c2p(sv, y), DOWN, buff=0.15)
            rows.append(dict(seg=seg, ends=ends, tr=tr, dot=dot, nm=nm, w=w, share=share))
        eq = cmath(r"P(R \mid T)", r"=", r"P(R \mid T, \text{mild})\,P(\text{mild} \mid T)", r"+",
                   r"P(R \mid T, \text{severe})\,P(\text{severe} \mid T)", font_size=32).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here's the mechanism. <bookmark mark='a'/> Each group's overall recovery rate is an average of its mild "
            "and severe rates, weighted by how many of its patients were mild and how many severe. Draw each group "
            "as a segment from its severe rate to its mild rate; the overall rate is a point on the segment, "
            "placed by the mix. <bookmark mark='b'/> The treated segment lies entirely to the right of the untreated "
            "one at both ends: better for mild patients, better for severe. <bookmark mark='c'/> But the doctors "
            f"gave the treatment mostly to the sickest. {pct(rows[0]['w'], 0)} percent of the treated were severe "
            f"cases, against {pct(rows[1]['w'], 0)} percent of the untreated. <bookmark mark='d'/> So the treated "
            "point slides down toward its severe end, the untreated point toward its mild end, and they cross. The "
            "comparison of totals is mostly a comparison of how sick the two groups were."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Write(eq))
            for r in rows:
                self.play(Create(r["seg"]), FadeIn(r["ends"]), FadeIn(r["nm"]), run_time=0.8)
            vo.wait_until("b")
            for r in rows:
                self.add(r["dot"])
            vo.wait_until("c")
            self.play(FadeIn(rows[0]["share"]), FadeIn(rows[1]["share"]))
            vo.wait_until("d")
            self.play(*[r["tr"].animate.set_value(r["w"]) for r in rows], run_time=3.0)
        for r in rows:
            r["dot"].clear_updaters()
        self.clear_scene()

    def which(self):
        left = VGroup(label(r"severity affects treatment", font_size=26, color=S.ACCENT),
                      MathTex(r"\text{severity} \to \text{treatment}, \quad \text{severity} \to \text{recovery}",
                              font_size=30),
                      label(r"compare within severity", font_size=26, color=S.KEPT)).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"treatment affects the third variable", font_size=26, color=S.ACCENT),
                       MathTex(r"\text{treatment} \to \text{blood pressure} \to \text{recovery}", font_size=30),
                       label(r"compare the totals", font_size=26, color=S.KEPT)).arrange(DOWN, buff=0.3)
        g = VGroup(left, right).arrange(DOWN, buff=1.0).move_to(DOWN * 0.2)
        head = label(r"Which comparison is right? \ The numbers alone cannot say.", font_size=32).to_edge(UP, buff=0.5)
        fwd = note(r"causal graphs: \ Part 36; \ the Berkeley admissions: \ Part 14").to_corner(DR, buff=0.3)
        with self.voiceover(
            "So is the right answer the one within groups? <bookmark mark='a'/> Here, yes, because of how the data "
            "arose. Severity came first: it influenced who got treated, and it influenced who recovered. To "
            "compare the treatment fairly, you compare like with like, within severity. <bookmark mark='b'/> But "
            "the very same table could arise differently. Suppose the third variable were something the treatment "
            "itself changes, say it lowers blood pressure, which is how it helps. Then splitting by blood pressure "
            "would compare people after the treatment had already done its work, and the totals would be the fair "
            "comparison. <bookmark mark='c'/> The arithmetic is identical in the two stories; only the causal "
            "picture differs. Data never tell you on their own which way to slice them. That question has a "
            "precise answer, a graph of what causes what, and Part 36 is about it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(fwd))
        self.clear_scene()

    def ecological(self):
        g = np.random.Generator(np.random.PCG64(12))
        A = axes([0, 10], [0, 10], x_length=6.0, y_length=4.8, xlabel=r"$x$", ylabel=r"$y$", center=[-3.4, -0.4, 0])
        ax = A.ax
        cols = [REGION_COLORS[i] for i in (0, 1, 2, 3, 4)]
        clouds, means = VGroup(), []
        for k in range(5):
            cx, cy = 1.5 + 1.8 * k, 2.0 + 1.4 * k
            xs = cx + 0.6 * g.standard_normal(40)
            ys = cy - 0.9 * (xs - cx) + 0.35 * g.standard_normal(40)
            clouds.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=cols[k]) for a, b in zip(xs, ys)
                                if 0 < a < 10 and 0 < b < 10]))
            means.append((xs.mean(), ys.mean()))
        mdots = VGroup(*[Dot(ax.c2p(a, b), radius=0.12, color=WHITE) for a, b in means])
        up = Line(ax.c2p(1.0, 1.6), ax.c2p(9.4, 7.9), color=WHITE, stroke_width=3)
        txt = VGroup(label(r"within every group: \ $y$ falls as $x$ rises", font_size=26, color=GREY_A),
                     label(r"across the group averages: \ $y$ rises", font_size=26, color=WHITE),
                     label(r"Robinson (1950): \ the ecological fallacy", font_size=26, color=S.ACCENT),
                     label(r"a correlation between groups is not \\ a correlation between people", font_size=24,
                           color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0, 0])
        tag = note(r"illustrative").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Aggregation has a cousin trap. <bookmark mark='a'/> Here are five groups, say five regions. Within every "
            "one, y falls as x rises. <bookmark mark='b'/> But compare the regions' averages, and y rises with x. "
            "<bookmark mark='c'/> In 1950 the sociologist W. S. Robinson showed that correlations computed across "
            "American states between immigration and literacy had nothing like the sign or size of the "
            "correlation among the individual people in them. Inferring how individuals behave from how groups "
            "behave is the ecological fallacy. A correlation between groups is not a correlation between people."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in clouds], lag_ratio=0.2), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(*[c.animate.set_opacity(0.3) for c in clouds], LaggedStart(*[GrowFromCenter(m) for m in mdots],
                                                                                 lag_ratio=0.15))
            self.play(Create(up), FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        self.clear_scene()
