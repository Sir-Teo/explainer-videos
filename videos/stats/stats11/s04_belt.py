from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats11.common import *  # noqa: F403


class Belt(VoiceoverScene):
    def construct(self):
        self.card()
        self.duality()
        self.belt()
        self.wald_belt()
        self.curve()
        self.family()

    def card(self):
        card = chapter_card(3, r"Inverting tests", r"A confidence set contains every value a test would not reject", part=PART)
        with self.voiceover("Chapter three. Inverting tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def duality(self):
        tc = theorem_card(r"Tests and intervals are the same thing", r"For each $\theta_0$ let $A(\theta_0)$ be the acceptance region of a "
                          r"size-$\alpha$ test of $\theta = \theta_0$. \ Then $C(x) = \{\theta_0 : x \in A(\theta_0)\}$ is a $1 - \alpha$ "
                          r"confidence set; \ and conversely, \ ``$\theta_0 \notin C(X)$'' is a size-$\alpha$ test.", who=r"Neyman (1937)",
                          color=OBS, width=10.6, font_size=26).move_to([0, 1.4, 0])
        rows = [
            cmath(r"P_\theta\big(\theta \in C(X)\big)", r"=", r"P_\theta\big(X \in A(\theta)\big) \ge 1 - \alpha", font_size=34),
        ]
        rows[0][2].set_color(OBS)
        whys = [why(r"the same event, \ read two ways: \ the proof is one line")]
        intro = label('A confidence set inverts a family of tests', font_size=36)
        with self.voiceover(
            "There's a second way to build intervals, and it works almost everywhere. <bookmark mark='a'/> For every "
            "candidate value theta-nought, run a test of whether the parameter equals theta-nought. The confidence set is "
            "every value the test doesn't reject. And conversely, rejecting whenever theta-nought falls outside a "
            "confidence set is a test. <bookmark mark='b'/> The proof is one line: the event that the true theta is in "
            "the set is the event that the data land in the true theta's acceptance region, which has probability at least "
            "one minus alpha. Tests and intervals are two views of one object."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=1, top=-1.4, x=-0.6, buff=0.8, edge=6.9)
            vo.wait_until("b")
            step(0, transform=False)
        self.clear_scene()

    def belt(self):
        d = load("belt")
        n, ps, lo, hi = d["n"], np.asarray(d["ps"]), d["lo"], d["hi"]
        A = axes([-0.5, 20.5], [0, 1], x_length=7.0, y_length=5.4, xlabel=r"the count $x$, \ $n = 20$", ylabel=r"the parameter $p$",
                 xticks=[0, 5, 7, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.4, -0.2, 0])
        ax = A.ax
        strips = VGroup()
        for p, a, b in zip(ps[::3], lo[::3], hi[::3]):
            strips.add(Line(ax.c2p(a - 0.45, p), ax.c2p(b + 0.45, p), color=OBS, stroke_width=2.2, stroke_opacity=0.5))
        demo = []
        for p0 in (0.3, 0.7):
            j = int(np.argmin(np.abs(ps - p0)))
            demo.append(VGroup(Line(ax.c2p(lo[j] - 0.45, ps[j]), ax.c2p(hi[j] + 0.45, ps[j]), color=EXACT, stroke_width=6),
                               MathTex(rf"p = {p0}:\ x \in [{lo[j]}, {hi[j]}]", font_size=24, color=EXACT).next_to(ax.c2p(hi[j] + 0.5, ps[j]), RIGHT, buff=0.15)))
        x = d["x"]
        cut = Line(ax.c2p(x, 0), ax.c2p(x, 1), color=S.LIK, stroke_width=4)
        cp_lo, cp_hi = d["cp"]
        seg = Line(ax.c2p(x, cp_lo), ax.c2p(x, cp_hi), color=S.LIK, stroke_width=10)
        rows = fit_rows(VGroup(
            label(r"for each $p$: \ the counts an exact 95\% test accepts", font_size=24, color=GREY_A),
            label(r"read across: \ a test; \ read up: \ an interval", font_size=26, color=OBS),
            MathTex(rf"x = {x}:\ \ p \in [{cp_lo:.3f},\ {cp_hi:.3f}]", font_size=30, color=S.LIK),
            label(r"Clopper \& Pearson (1934)", font_size=22, color=GREY_A),
            MathTex(rf"\text{{Wald: }} [{d['wald'][0]:.3f},\ {d['wald'][1]:.3f}]", font_size=26, color=METHOD_COL["wald"]),
        ), 4.8, 0.34, [4.5, -0.2, 0])
        with self.voiceover(
            "Neyman drew this as a picture, the confidence belt. <bookmark mark='a'/> Twenty trials. For a given true "
            "p, say point three, the central equal-tail exact test at five percent accepts the counts from two to ten: those are the "
            "outcomes not too surprising if p is point three. <bookmark mark='b'/> At p equals point seven, it accepts "
            "ten to eighteen. <bookmark mark='c'/> Do that for every p, and the accepted regions sweep out a belt. Read "
            "across, the belt is a family of tests. <bookmark mark='d'/> Now read it the other way. We observed seven "
            "successes. Go up the column at x equals seven, and the p's whose belt contains seven form the interval: "
            "point one five four to point five nine two. <bookmark mark='e'/> That's the Clopper–Pearson interval, from "
            "1934, built by inverting exact binomial tests. By the duality, its coverage is at least ninety-five percent "
            "for every p. The Wald interval for the same data is shifted down and narrower: that's where its missing "
            "coverage goes."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(demo[0][0]), FadeIn(demo[0][1]))
            vo.wait_until("b")
            self.play(Create(demo[1][0]), FadeIn(demo[1][1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s_) for s_ in strips], lag_ratio=0.01), FadeIn(rows[0]), run_time=3.0)
            self.play(FadeOut(demo[0][1]), FadeOut(demo[1][1]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(cut))
            self.play(Create(seg), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def curve(self):
        x, n = 7, 20
        ps = np.linspace(0.01, 0.8, 300)
        pv = np.minimum(1, 2 * np.minimum(stats.binom.cdf(x, n, ps), stats.binom.sf(x - 1, n, ps)))
        A = axes([0, 0.8], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"$p_0$", ylabel=r"two-sided exact $p$-value for $H_0: p = p_0$, \ $x = 7$",
                 xticks=[0, 0.154, 0.35, 0.592, 0.8], yticks=[0, 0.05, 0.5, 1], xfmt=lambda v: f"{v:g}", center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = polyline(ax, ps, pv, OBS, 3)
        cut = DashedLine(ax.c2p(0, 0.05), ax.c2p(0.8, 0.05), color=MISS, stroke_width=2)
        cut2 = DashedLine(ax.c2p(0, 0.5), ax.c2p(0.8, 0.5), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"the $p$-value function \ (or confidence curve)", font_size=26, color=OBS),
            label(r"cut at 0.05: \ the 95\% interval", font_size=24, color=MISS),
            label(r"cut at 0.5: \ a 50\% interval", font_size=24, color=GREY_A),
            label(r"its plateau: \ most compatible under this test ordering", font_size=24, color=GREY_A),
            label(r"every interval at every level, \ in one picture", font_size=24, color=OBS),
        ), 5.0, 0.34, [4.4, -0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The duality gives a richer summary than any single interval. For our seven of twenty, "
            "test every possible p-nought and plot the p-value. This is the p-value function, sometimes called the "
            "confidence curve. <bookmark mark='b'/> Cut it at point zero five, and the values above the line are the "
            "ninety-five percent interval. <bookmark mark='c'/> Cut at point five, and you get a fifty percent interval. "
            "<bookmark mark='d'/> Its maximum can be a plateau: the most compatible values under this particular test ordering. It shows every interval at every "
            "level at once, and it makes clear that the edges of a ninety-five percent interval aren't walls: values just "
            "outside are barely less compatible than values just inside."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cut2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def family(self):
        items = [
            (r"equal-tail exact binomial tests", r"Clopper--Pearson", METHOD_COL["clopper_pearson"]),
            (r"the score test, \ $\frac{\hat p - p_0}{\sqrt{p_0(1 - p_0)/n}}$", r"Wilson", METHOD_COL["wilson"]),
            (r"the likelihood ratio test", r"the likelihood interval", METHOD_COL["lr"]),
            (r"the Wald test, \ $\frac{\hat p - p_0}{\sqrt{\hat p(1 - \hat p)/n}}$", r"Wald", METHOD_COL["wald"]),
            (r"Wilcoxon rank test: \ common shift model", r"Hodges--Lehmann (Part 16)", GREY_A),
        ]
        rows = VGroup()
        for t, i, c in items:
            rows.add(VGroup(label(t, font_size=24), MathTex(r"\longrightarrow", font_size=30, color=GREY_B), label(i, font_size=26, color=c)))
        for r in rows:
            r[0].move_to([-3.0, 0, 0])
            r[1].move_to([0.9, 0, 0])
            r[2].move_to([3.8, 0, 0])
        rows.arrange(DOWN, buff=0.42).move_to([0, -0.2, 0])
        for r in rows:
            r[0].set_x(-3.0)
            r[1].set_x(0.9)
            r[2].set_x(3.8)
        head = label(r"invert tests, \ get a confidence set", font_size=32, color=OBS).to_edge(UP, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> A family of tests inverts into a confidence set, which need not be an interval. <bookmark mark='b'/> Central equal-tail exact binomial tests give "
            "Clopper–Pearson. <bookmark mark='c'/> The score test, which uses the standard error the null hypothesis "
            "implies, gives Wilson's interval. <bookmark mark='d'/> The likelihood ratio test gives the likelihood "
            "interval. <bookmark mark='e'/> The Wald test, which uses the estimated standard error, gives the Wald "
            "interval. <bookmark mark='f'/> And in a common location-shift model, inversion of a Wilcoxon rank test gives the Hodges–Lehmann interval of Part "
            "16. The quality of the interval is the quality of the test, and the next chapter compares them."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wald_belt(self):
        from explainer.stats.kit import intervals as I
        n = 20
        ps = np.linspace(0.005, 0.995, 120)
        panels = VGroup()
        for j, (k, nm) in enumerate((("clopper_pearson", r"Clopper--Pearson belt"), ("wald", r"Wald belt"))):
            m = I.BINOMIAL[k]
            ints = [m(x, n) for x in range(n + 1)]
            A = axes([-0.5, 20.5], [0, 1], x_length=5.2, y_length=4.2, xlabel=r"$x$", xticks=[0, 10, 20], yticks=[0, 0.5, 1],
                     center=[-3.4 + 6.8 * j, -0.1, 0], font_size=18)
            ax = A.ax
            strips = VGroup()
            for p in ps:
                acc = [x for x, (lo, hi) in enumerate(ints) if lo <= p <= hi]
                if acc:
                    strips.add(Line(ax.c2p(min(acc) - 0.45, p), ax.c2p(max(acc) + 0.45, p), color=METHOD_COL[k], stroke_width=2, stroke_opacity=0.6))
            panels.add(VGroup(A, strips, label(nm, font_size=24, color=METHOD_COL[k]).next_to(A, UP, buff=0.15)))
        foot = fit_rows(VGroup(
            label(r"every interval family has a belt: \ read across it to see which counts each $p$ ``accepts''", font_size=24),
            label(r"Wald's belt pinches shut near $p = 0$ and $1$: \ there the outcomes it accepts have too little probability", font_size=24,
                  color=MISS),
        ), 12.6, 0.28, [0, -3.0, 0])
        intro = label('Compare the probability accepted by each belt', font_size=36)
        with self.voiceover(
            "Every family of intervals has a belt, and comparing belts shows what goes wrong. <bookmark mark='a'/> On the "
            "left, Clopper–Pearson's belt, built from exact tests. <bookmark mark='b'/> On the right, the belt the Wald "
            "intervals imply: for each p, the counts whose Wald interval contains it. <bookmark mark='c'/> Near zero and "
            "one, Wald's belt pinches almost shut. For a small p, only a count or two is accepted, and together they "
            "carry far less than ninety-five percent of the probability. That pinch is the collapse of coverage at the "
            "edges, seen from the side."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][2]), LaggedStart(*[Create(s_) for s_ in panels[0][1]], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), LaggedStart(*[Create(s_) for s_ in panels[1][1]], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
