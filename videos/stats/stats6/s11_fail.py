from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Fail(VoiceoverScene):
    def construct(self):
        self.card()
        self.cauchy()
        self.why_cauchy()
        self.pareto()
        self.stable()

    def card(self):
        card = chapter_card(10, r"When averages fail", r"Heavy tails, \ and the limits of the limit theorems", part=PART)
        with self.voiceover("Chapter ten. When averages fail."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def running(self, d, key, cx, color, yr, title):
        steps = np.asarray(d["steps"], float)
        A = axes([0, 4], yr, x_length=5.6, y_length=4.0, xlabel=r"$n$ (log scale)", xticks=[0, 1, 2, 3, 4],
                 yticks=[yr[0], (yr[0] + yr[1]) / 2, yr[1]], xfmt=lambda v: f"10^{{{int(v)}}}", center=[cx, -0.6, 0])
        ax = A.ax
        paths = VGroup(*[polyline(ax, np.log10(steps), np.clip(m, yr[0], yr[1]), color, 2, 0.85) for m in np.asarray(d[key])])
        t = label(title, font_size=26, color=color).next_to(A, UP, buff=0.15)
        return A, paths, t

    def cauchy(self):
        d = load("cauchy")
        A1, p1, t1 = self.running(d, "normal", -3.5, SIM, [-3, 3], r"running means: \ normal")
        A2, p2, t2 = self.running(d, "cauchy", 3.3, BOUND, [-3, 3], r"running means: \ Cauchy")
        tag = note(r"simulated: 6 sequences of 10,000 each; \ Cauchy paths clipped to $\pm 3$").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Every theorem so far assumed something: a finite mean, a finite variance. Here's what happens without "
            "them. <bookmark mark='a'/> On the left, running means of standard normal draws: six sequences of ten "
            "thousand, settling quickly onto zero. <bookmark mark='b'/> On the right, running means of Cauchy draws: "
            "Part 3's lighthouse, the ratio of two normals. They never settle. Every so often a single huge draw "
            "jerks the average somewhere new, and after ten thousand draws it's no more settled than after ten. "
            "The Cauchy has no mean, so there is nothing for the average to converge to."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A1), FadeIn(t1), LaggedStart(*[Create(p) for p in p1], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(A2), FadeIn(t2), LaggedStart(*[Create(p) for p in p2], lag_ratio=0.15), run_time=4.0)
        self.clear_scene()

    def why_cauchy(self):
        d = load("cauchy")
        rows = [
            cmath(r"\varphi_X(t)", r"=", r"E\,e^{itX}", r"=", r"e^{-|t|}", font_size=34),
            cmath(r"\varphi_{\bar X_n}(t)", r"=", r"\varphi_X(t/n)^n", r"=", r"\big(e^{-|t|/n}\big)^n = e^{-|t|}", font_size=34),
            cmath(r"\bar X_n", r"\sim", r"\text{Cauchy}", r"\quad \text{for every } n", font_size=36),
        ]
        rows[2][2].set_color(BOUND)
        whys = [why(r"the Cauchy's characteristic function (Part 3)"), why(r"independence, \ as in chapter five"),
                why(r"the average of a thousand is exactly as spread as one")]
        iq = d["iqr"]
        tab = VGroup(*[MathTex(rf"n = {n}:\ \ \text{{quartiles}}\ {iq[n][0]:+.2f},\ {iq[n][2]:+.2f}", font_size=28, color=GREY_A)
                       for n in ("1", "10", "100")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        tag = note(r"simulated: 20,000 means of each size").to_corner(DR, buff=0.3)
        with self.voiceover(
            "It's worse than slow. <bookmark mark='a'/> The Cauchy's characteristic function is e to the minus the "
            "absolute value of t. <bookmark mark='b'/> The mean of n independent copies has characteristic function "
            "that, at t over n, raised to the n-th power: which is e to the minus absolute t again. "
            "<bookmark mark='c'/> So the average of n Cauchy variables is Cauchy, with exactly the same spread as a "
            "single one. Averaging buys nothing. <bookmark mark='d'/> The simulation agrees: the quartiles of the "
            "mean stay at minus one and plus one whether you average one, ten or a hundred."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.9, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(tab), FadeIn(tag))
        self.clear_scene()

    def pareto(self):
        d = load("cauchy")
        A, paths, t = self.running(d, "pareto", -2.6, S.POST, [1.5, 4.5], r"running means: \ Pareto, \ $\alpha = 1.5$")
        mean = DashedLine(A.ax.c2p(0, 3), A.ax.c2p(4, 3), color=EXACT, stroke_width=2)
        ml = MathTex(r"\mu = 3", font_size=26, color=EXACT).next_to(A.ax.c2p(4, 3), RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(r"P(X > x) = x^{-1.5}\ \ (x \ge 1)", font_size=28),
            MathTex(r"E X = 3, \qquad \mathrm{Var}\,X = \infty", font_size=28),
            label(r"the weak law still holds \ (a finite mean is enough)", font_size=24, color=S.LIK),
            label(r"the CLT does not: \ $\sqrt n$ is the wrong scale", font_size=24, color=BOUND),
            MathTex(r"\bar X_n - \mu \ \approx\ n^{1/\alpha - 1} \times \text{(a skewed stable law)}", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r in rows:
            if r.width > 5.4:
                r.width = 5.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.1, 0.0, 0])
        tag = note(r"simulated: 6 sequences of 10,000").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Between the normal and the Cauchy lies a whole family of heavy tails. <bookmark mark='a'/> Take a "
            "Pareto variable with tail index one and a half: the chance of exceeding x falls like x to the minus one "
            "and a half. Its mean is three, but its variance is infinite. <bookmark mark='b'/> The running means do "
            "head for three, since the weak law needs only a finite mean, but slowly and in jumps, each time a big "
            "draw arrives. <bookmark mark='c'/> The central limit theorem fails: the errors shrink like n to the "
            "minus a third, not n to the minus a half, and their limit is not normal but a skewed law called stable. "
            "Recall that the World's incomes have tail index two point one: just inside the territory where the "
            "variance is finite, which is why chapter seven found them so slow."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(t), Create(mean), FadeIn(ml), LaggedStart(*[Create(p) for p in paths], lag_ratio=0.15),
                      FadeIn(rows[2]), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def stable(self):
        thm = theorem_card(r"The generalized central limit theorem", r"if suitably centred and scaled sums of i.i.d.\ variables "
                           r"converge at all, \ the limit is a \emph{stable} law, \ with index $0 < \alpha \le 2$; \ $\alpha = 2$ is the "
                           r"normal, \ needing only a finite variance", who=r"L\'evy, 1925; \ Gnedenko \& Kolmogorov, 1949",
                           color=S.PRIOR, width=10.6, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            MathTex(r"\alpha = 2:\ \text{normal},\ \ \text{scale } \sqrt n", font_size=30, color=EXACT),
            MathTex(r"1 < \alpha < 2:\ \text{mean finite, variance infinite},\ \ \text{scale } n^{1/\alpha}", font_size=30, color=S.POST),
            MathTex(r"\alpha = 1:\ \text{Cauchy},\ \ \text{scale } n \text{ (averaging does nothing)}", font_size=30, color=BOUND),
            label(r"heavy tails in the wild: \ city sizes, \ insurance claims, \ wealth, \ daily stock returns (Mandelbrot, 1963)",
                  font_size=22, color=GREY_A),
            label(r"before you average, \ look at the tail (Part 30, \ Part 60)", font_size=26, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(thm, DOWN, buff=0.5)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(thm, DOWN, buff=0.5)
        with self.voiceover(
            "There's a complete answer. <bookmark mark='a'/> If sums of independent, identically distributed "
            "variables converge at all, after centring and scaling, the limit must be a stable law, a family with an "
            "index alpha between zero and two. Paul Lévy found them in 1925; Boris Gnedenko and Kolmogorov wrote "
            "the theory down in 1949. <bookmark mark='b'/> Index two is the normal, and it attracts everything with "
            "a finite variance. <bookmark mark='c'/> Between one and two, the mean exists, the variance doesn't, and "
            "sums grow like n to the one over alpha. <bookmark mark='d'/> At one, the Cauchy, where averaging does "
            "nothing at all. <bookmark mark='e'/> Heavy tails are common in the real world: city sizes, insurance "
            "claims, fortunes; Benoit Mandelbrot argued in 1963 that cotton prices had them. <bookmark mark='f'/> "
            "Before you trust an average, look at the tail."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            for k, m in enumerate("bcdef"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
