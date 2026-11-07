from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403


class NMinus1(VoiceoverScene):
    def construct(self):
        self.card()
        self.bias()
        self.algebra()
        self.geometry()
        self.sbias()
        self.dof()

    def card(self):
        card = chapter_card(2, r"Why $n - 1$", r"The variance that divides by one less", part=PART)
        with self.voiceover("Chapter two. Why n minus one."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bias(self):
        d = load("nminus1")
        ns = np.asarray(d["ns"])
        A = axes([1.5, 10.5], [0.4, 1.15], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$",
                 ylabel=r"average estimate $\div \sigma^2$", xticks=list(range(2, 11)), yticks=[0.5, 0.75, 1.0],
                 center=[-2.0, -0.4, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(1.5, 1), ax.c2p(10.5, 1), color=EXACT, stroke_width=2)
        dn = VGroup(*[Dot(ax.c2p(n, v), radius=0.08, color=RESID) for n, v in zip(ns, d["by_n"])])
        dn1 = VGroup(*[Dot(ax.c2p(n, v), radius=0.08, color=SIM) for n, v in zip(ns, d["by_n1"])])
        theory = curve(ax, np.linspace(1.6, 10.4, 100), (np.linspace(1.6, 10.4, 100) - 1) / np.linspace(1.6, 10.4, 100), RESID, 1.8)
        leg = legend([(RESID, r"divide by $n$"), (SIM, r"divide by $n - 1$"), (EXACT, r"$\sigma^2$, the truth")],
                     font_size=24).move_to([4.6, 1.6, 0])
        rows = fit_rows(VGroup(MathTex(r"E\Big[\tfrac1n \textstyle\sum (x_i - \bar x)^2\Big] = \tfrac{n - 1}{n}\sigma^2", font_size=30, color=RESID),
                               label(r"$n = 2$: \ half the true variance, \ on average", font_size=24, color=GREY_A)),
                        5.0, 0.3, [4.4, -0.6, 0])
        tag = simulated_tag(r"simulated: 40,000 samples of each size, \ World heights")
        with self.voiceover(
            "Every course tells you to divide the sum of squared deviations by n minus one, not n. Here's why. "
            "<bookmark mark='a'/> Draw forty thousand samples of each size from the World's heights, and average the "
            "variance estimate. Divide by n, and the estimate is too small on average: at n equals two it's only "
            "half the true variance. <bookmark mark='b'/> The shortfall follows the curve n minus one over n. "
            "<bookmark mark='c'/> Divide by n minus one instead, and the average lands on the truth at every sample "
            "size. That's what unbiased means. But why is the sum of squares too small in the first place?"
        ) as vo:
            self.play(FadeIn(A), Create(one), FadeIn(tag), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dn], lag_ratio=0.1), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(theory), FadeIn(rows))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in dn1], lag_ratio=0.1), FadeIn(leg[1]))
        self.clear_scene()

    def algebra(self):
        rows = [
            cmath(r"\sum_i (x_i - \bar x)^2", r"=", r"\sum_i (x_i - \mu)^2 - n(\bar x - \mu)^2", font_size=32),
            cmath(r"E\sum_i (x_i - \bar x)^2", r"=", r"n\sigma^2 - n\cdot\frac{\sigma^2}{n}", r"=", r"(n - 1)\,\sigma^2", font_size=32),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"Pythagoras about $\bar x$: \ the cross term vanishes"), why(r"$E(x_i - \mu)^2 = \sigma^2$; \ $E(\bar x - \mu)^2 = \sigma^2/n$")]
        rem = fit_rows(VGroup(
            label(r"deviations from $\bar x$ are smaller than deviations from $\mu$: \ $\bar x$ is the point closest to the data", font_size=24),
            label(r"the shortfall is exactly the variance of $\bar x$ itself, \ one $\sigma^2$ in total", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Measure deviations from mu, the true mean, and split them at the sample mean: the "
            "sum of squares about the sample mean is the sum about mu, minus n times the squared distance between the "
            "two means. The cross term vanishes, by Part 1's fact that deviations from the mean sum to zero. "
            "<bookmark mark='b'/> Take expectations. The first part is n sigma squared; the subtracted part is n times "
            "the variance of the mean, which is one sigma squared. What's left is n minus one sigma squared. "
            "<bookmark mark='c'/> The sample mean is, by construction, the point closest to the data, so deviations "
            "about it have an expected total shortfall of n times the variance of the mean, one sigma squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.0, buff=1.0, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(rem))
        self.clear_scene()

    def geometry(self):
        d = load("nminus1")
        x3 = np.asarray(d["x3"]) - 165
        xb = float(np.mean(x3))
        ns = NSpace(scale=0.33, center=[-2.6, -0.6, 0], angle=-0.65, tilt=0.35, axis_len=11,
                    axis_labels=[r"$x_1$", r"$x_2$", r"$x_3$"])
        one = ns.line(np.ones(3) / np.sqrt(3), extent=14, color=EXACT)
        v = ns.vector(x3, color=WHITE)
        proj = ns.vector([xb] * 3, color=EXACT)
        res = ns.segment([xb] * 3, x3, color=RESID, stroke_width=4)
        pl = ns.plane(np.array([1, -1, 0]) / np.sqrt(2), np.array([1, 1, -2]) / np.sqrt(6), extent=9, color=RESID, opacity=0.12)
        ra = ns.right_angle([xb] * 3, (x3 - xb) / np.linalg.norm(x3 - xb), np.ones(3) / np.sqrt(3), size=1.0)
        rows = fit_rows(VGroup(
            MathTex(r"\mathbf x = (168,\ 175,\ 161) - 165", font_size=26),
            label(r"gold: \ $\bar x\,\mathbf 1$, \ the projection onto the line $\mathbf 1$", font_size=22, color=EXACT),
            label(r"red: \ the residual $\mathbf x - \bar x\mathbf 1$", font_size=22, color=RESID),
            label(r"it lives in the plane $\perp \mathbf 1$: \ 2 dimensions, \ not 3", font_size=24, color=RESID),
            MathTex(r"\|\mathbf x - \bar x\mathbf 1\|^2 = " + f"{d['ss3']:.0f}", font_size=26),
            label(r"$n$ numbers, \ but the residual has only $n - 1$ free directions: \ Part 4's projection", font_size=22,
                  color=S.ACCENT),
        ), 5.4, 0.25, [4.1, 0.2, 0])
        with self.voiceover(
            "Part 4 gave a better reason, in geometry. <bookmark mark='a'/> A sample of three heights is one point in "
            "three-dimensional space. <bookmark mark='b'/> The sample mean, times the vector of ones, is the "
            "projection of that point onto the diagonal line. <bookmark mark='c'/> And the residual, the deviations "
            "from the mean, is the perpendicular from the line to the point. <bookmark mark='d'/> Every possible "
            "residual lives in the plane perpendicular to the diagonal: two dimensions, not three. Turn the picture. "
            "<bookmark mark='e'/> The sum of squared deviations is the squared length of a vector confined to n "
            "minus one dimensions, and each dimension contributes, on average, one sigma squared. That's where n "
            "minus one comes from: it's a dimension."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(ns.axes3))
            vo.wait_until("a")
            self.add(v)
            self.play(NSpace.reveal(v), FadeIn(rows[0]))
            vo.wait_until("b")
            self.add(one, proj)
            self.play(NSpace.reveal(one, proj), FadeIn(rows[1]))
            vo.wait_until("c")
            self.add(res, ra)
            self.play(NSpace.reveal(res, ra), FadeIn(rows[2]))
            vo.wait_until("d")
            self.add(pl)
            self.play(NSpace.reveal(pl), FadeIn(rows[3:5]))
            self.play(ns.turn(1.1, run_time=5.0))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
            for m_ in (one, v, proj, res, pl, ra):
                m_.clear_updaters()
        self.clear_scene()

    def dof(self):
        rows = fit_rows(VGroup(
            label(r"degrees of freedom: \ the dimension of the space the residuals live in", font_size=28, color=S.ACCENT),
            MathTex(r"\text{one mean estimated: } n - 1", font_size=30),
            MathTex(r"\text{a full-rank linear regression with } p \text{ coefficients: } n - p \quad \text{(Part 4's hat matrix; Part 12)}", font_size=30),
            MathTex(r"\text{a } k\text{-group comparison: } n - k \quad \text{(Part 13)}", font_size=30),
            label(r"each independent fitted linear direction uses one residual dimension", font_size=26, color=GREY_A),
        ), 12.6, 0.4, [0, 0.2, 0])
        intro = label('Independent fitted directions use residual dimensions', font_size=36)
        with self.voiceover(
            "This idea has a name that will follow us through the course. <bookmark mark='a'/> Degrees of freedom: the "
            "dimension of the space the residuals live in. <bookmark mark='b'/> Estimate one mean, lose one dimension: "
            "n minus one. <bookmark mark='c'/> Fit a full-column-rank linear regression with p coefficients, and the residuals live in n minus "
            "p dimensions, the trace of Part 4's residual projection. <bookmark mark='d'/> Compare k groups, and it's "
            "n minus k. <bookmark mark='e'/> Each independent fitted linear direction uses one dimension; redundant coefficients do not."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sbias(self):
        d = load("extras")["c4"]
        rows = [
            cmath(r"E\,s^2 = \sigma^2", r"\ \text{ but }\ ", r"E\,s \le \sigma", font_size=34),
            cmath(r"E\,s", r"=", r"c_4(n)\,\sigma,\quad c_4(n) = \sqrt{\frac{2}{n - 1}}\,\frac{\Gamma(n/2)}{\Gamma((n - 1)/2)}", font_size=30),
            cmath(r"c_4", r":\ ", rf"n = 2:\ {d['2']:.3f},\quad n = 5:\ {d['5']:.3f},\quad n = 30:\ {d['30']:.3f}", font_size=30),
        ]
        rows[0][2].set_color(RESID)
        whys = [why(r"Jensen: strict when $s$ is nonconstant; assume finite variance, $n>1$"), why(r"from the $\chi$ distribution (normal data)"),
                why(r"quality-control charts divide by $c_4$; \ most of statistics doesn't bother")]
        hist = note(r"Gauss derived the $n - 1$ in 1823; \ Bessel's name stuck to it").to_edge(DOWN, buff=0.5)
        intro = label('Unbiased variance does not mean unbiased standard deviation', font_size=36)
        with self.voiceover(
            "One subtlety. <bookmark mark='a'/> Dividing by n minus one makes the variance unbiased, but not the "
            "standard deviation. The square root is concave, so by Jensen's inequality from Part 6, the average of s "
            "is below sigma. <bookmark mark='b'/> For normal data the shortfall factor is a ratio of gamma functions, "
            "called c four. <bookmark mark='c'/> With two observations s averages eighty percent of sigma; with five, "
            "ninety-four; with thirty, ninety-nine. Quality-control engineers divide by it; most of statistics doesn't "
            "bother, because unbiasedness isn't preserved by nonlinear functions anyway. The n minus one itself goes "
            "back to Gauss in 1823, though it's usually called Bessel's correction."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=1.0, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(hist))
        self.clear_scene()
