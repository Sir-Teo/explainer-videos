from __future__ import annotations

import numpy as np
from scipy import stats as sst

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, ellipse_curve, load, predict, show_card


class GMM(VoiceoverScene):
    def construct(self):
        t = load("gmm_toy")
        self.card()
        self.plane(t)
        self.derive()
        self.special(t)

    def card(self):
        c = chapter_card(8, r"GMM: moments as close to zero as possible", r"What if a theory gives averages, not a "
                         r"likelihood?", lit=(1982,), part=PART)
        with self.voiceover("Chapter eight. The generalized method of moments: getting the moments as close to zero "
                            "as possible."):
            show_card(self, c)
        self.play(FadeOut(c))

    def plane(self, t):
        m1, m2, n = t["m1"], t["m2"], t["n"]
        W1, W2 = np.eye(2), np.asarray(t["W"])
        g = axes([-0.6, 0.7], [-0.6, 0.7], x_length=5.6, y_length=5.6, xlabel=r"$\bar g_1(\mu) = \bar x_1 - \mu$",
                 ylabel=r"$\bar g_2(\mu) = \bar x_2 - \mu$", xticks=[-0.5, 0, 0.5], yticks=[-0.5, 0, 0.5],
                 font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ax = g.ax
        origin = Dot(ax.c2p(0, 0), radius=0.07, color=WHITE)
        ol = label(r"theory: $\mathbb{E}[g] = 0$", font_size=20, color=WHITE).next_to(origin, DL, buff=0.08)
        mus = np.linspace(0.45, 1.55, 50)
        line = curve(ax, m1 - mus, m2 - mus, DATA_C, stroke_width=3)
        mu = ValueTracker(0.5)
        dot = always_redraw(lambda: Dot(ax.c2p(m1 - mu.get_value(), m2 - mu.get_value()), radius=0.08, color=YELLOW))
        mu_ro = always_redraw(lambda: MathTex(rf"\mu = {mu.get_value():.3f}", font_size=30, color=YELLOW).next_to(
            g, UP, buff=0.05).align_to(g, RIGHT))
        c = ValueTracker(1e-4)
        W = [W1]
        ell = always_redraw(lambda: ellipse_curve(ax, (0, 0), np.linalg.inv(W[0]), EST, k2=c.get_value()))
        th1 = (m1 + m2) / 2
        gap1 = np.array([m1 - th1, m2 - th1])
        c1 = float(gap1 @ W1 @ gap1)
        th2 = t["theta"]
        gap2 = np.array([m1 - th2, m2 - th2])
        c2 = float(gap2 @ W2 @ gap2)
        S = np.asarray(t["S"])
        side = VGroup(
            label(r"a toy: one mean $\mu$, two noisy measures of it", font_size=22, color=GREY_A),
            MathTex(rf"\bar x_1 = {m1:.3f}\ (\text{{sd }} 1),\ \ \bar x_2 = {m2:.3f}\ (\text{{sd }} 2),\ n = {n}",
                    font_size=26),
            MathTex(rf"W = I:\ \hat\mu = {th1:.3f}", font_size=30, color=EST),
            MathTex(rf"W = \hat S^{{-1}}:\ \hat\mu = {th2:.3f}\ ({t['se']:.3f})", font_size=30, color=GOOD),
            MathTex(rf"J = n\,\bar g^\top \hat S^{{-1}} \bar g = {t['J']:.2f},\ \ p = {t['p_J']:.2f}", font_size=30,
                    color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        cg = axes([0, 6], [0, 1.2], x_length=4.4, y_length=1.5, xticks=[0, 2, 4, 6], yticks=[], font_size=14,
                  xlabel=r"$\chi^2_1$").next_to(side, DOWN, buff=0.4)
        xs = np.linspace(0.02, 6, 120)
        dens = curve(cg.ax, xs, np.minimum(sst.chi2.pdf(xs, 1), 1.2), GREY_B, stroke_width=2)
        jm = Line(cg.ax.c2p(t["J"], 0), cg.ax.c2p(t["J"], 1.1), color=ALT, stroke_width=4)
        with self.voiceover(
            "Many theories in finance do not give a likelihood. They give averages that should be zero: moment "
            "conditions. Lars Peter Hansen built an estimator on exactly that in 1982, and shared the 2013 Nobel "
            "prize for it. Here is its geometry in the simplest case. Two noisy measurements of one mean: the first "
            "with a standard deviation of one, the second of two. Each gives a moment: its sample mean minus mu. "
            "<bookmark mark='a'/> Draw the two sample moments as a point in the plane. Theory says the point should "
            "be the origin. As mu changes, the point slides along a line. <bookmark mark='b'/> No mu puts it exactly "
            "at the origin, because the two measures disagree. So pick the point of the line closest to the origin. "
            "Closest in which metric? With the identity, inflate circles from the origin until one touches the "
            f"line: the plain average, {th1:.3f}. <bookmark mark='c'/> But the second measure is four times as noisy. "
            "Hansen's efficient weight is the inverse of the moments' covariance, which stretches the circles into "
            "ellipses, long along the noisy direction. Inflate again: the touching point slides toward the precise "
            f"measure, and mu hat is {th2:.3f}. <bookmark mark='d'/> What is left, the distance from the origin in "
            "that metric, scaled by the sample size, is Hansen's J statistic. With two moments and one parameter it "
            f"is chi-squared with one degree of freedom: here {t['J']:.2f}, a p-value of {t['p_J']:.2f}. The two "
            "measures are consistent with one mean."
        ) as vo:
            self.play(FadeIn(g), FadeIn(origin), FadeIn(ol), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.add(dot, mu_ro)
            self.play(Create(line), mu.animate.set_value(1.5), run_time=3)
            vo.wait_until("b")
            self.add(ell)
            self.play(mu.animate.set_value(th1), c.animate.set_value(c1), run_time=3)
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(c.animate.set_value(1e-4), run_time=0.8)
            W[0] = W2
            self.play(mu.animate.set_value(th2), c.animate.set_value(c2), run_time=3)
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            gapv = Arrow(ax.c2p(0, 0), ax.c2p(*gap2), buff=0, color=ALT, stroke_width=4)
            self.play(GrowArrow(gapv), FadeIn(side[4]), FadeIn(cg), Create(dens))
            self.play(Create(jm))
        for x in (dot, mu_ro, ell):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\hat\theta": EST, r"S": ALT, r"J": BAD}
        rows = [cmath(r"\hat\theta", r"=", r"\arg\min_\theta\ g_T(\theta)^\top W g_T(\theta)", font_size=36, colors=C_),
                cmath(r"D^\top W g_T(\hat\theta)", r"=", r"0,\quad D = \partial g_T / \partial\theta^\top", font_size=36,
                      colors=C_),
                cmath(r"\hat\theta - \theta_0", r"\approx", r"-(D^\top W D)^{-1} D^\top W g_T(\theta_0)", font_size=36,
                      colors=C_),
                cmath(r"\mathrm{Var}(\hat\theta)", r"=", r"\tfrac1T (D^\top W D)^{-1} D^\top W S W D (D^\top W D)^{-1}",
                      font_size=36, colors=C_),
                cmath(r"W = S^{-1}", r"\Rightarrow", r"\mathrm{Var}(\hat\theta) = \tfrac1T (D^\top S^{-1} D)^{-1}",
                      font_size=36, colors=C_),
                cmath(r"J", r"=", r"T\, g_T(\hat\theta)^\top \hat S^{-1} g_T(\hat\theta) \to \chi^2_{q - p}", font_size=36,
                      colors=C_)]
        whys = [why(r"definition: the sample moments, made as small as possible in the metric $W$"),
                why(r"first-order condition: the gap is perpendicular, in the metric $W$, to the directions $\theta$ "
                    r"can move"),
                why(r"linearise $g_T(\hat\theta) \approx g_T(\theta_0) + D(\hat\theta - \theta_0)$ and solve"),
                why(r"the variance of a linear map of $g_T(\theta_0)$, whose variance is $S/T$: $S$ is chapter two's "
                    r"long-run variance"),
                why(r"the sandwich collapses: the efficient weight"),
                why(r"$q$ moments, $p$ directions used up fitting $\theta$: what is left is a test of the theory")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.72, edge=6.8)
        with self.voiceover(
            "In general, the estimator minimises the moments' length in a metric W. <bookmark mark='a'/> At the "
            "minimum, the leftover gap is perpendicular, in that metric, to every direction the parameters can "
            "move the moments. <bookmark mark='b'/> Linearise the moments around the truth and solve: the error is "
            "a fixed matrix times the moments at the true parameter. <bookmark mark='c'/> So its variance is a "
            "sandwich again, with S, the long-run variance of the moments from chapter two, as the meat. "
            "<bookmark mark='d'/> Choose W equal to S inverse and the sandwich collapses: no other weight gives a "
            "smaller variance. <bookmark mark='e'/> And the leftover, scaled, is chi-squared with as many degrees "
            "of freedom as there are moments beyond parameters."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.5)
        self.clear_scene()

    def special(self, t):
        rows = VGroup(
            label(r"Three estimators you know are GMM", font_size=32),
            MathTex(r"\text{OLS:}\quad g = x_t\,(y_t - x_t^\top\beta)", font_size=32, color=EST),
            MathTex(r"\text{IV:}\quad g = z_t\,(y_t - x_t^\top\beta)", font_size=32, color=GOOD),
            MathTex(r"\text{ML:}\quad g = \nabla_\theta \log f(x_t;\theta)", font_size=32, color=ALT),
            wrapped_label(r"exactly identified (as many moments as parameters): the moments can all be set to zero, "
                          r"$W$ does not matter, and $J = 0$; Cochrane's \textit{Asset Pricing}, chapters 10--11 and "
                          r"13--16, compares the methods", 11.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        q = predict(r"Exactly as many moments as parameters. What is $J$?").next_to(rows, DOWN, buff=0.45)
        with self.voiceover(
            "This is why GMM is the umbrella. Least squares is GMM with moments x times the residual. Instrumental "
            "variables replace x with an instrument z. Maximum likelihood uses the score as its moments. "
            "<bookmark mark='a'/> Pause and predict: what is J when there are exactly as many moments as "
            "parameters? <bookmark mark='b'/> Zero. Every moment can be set exactly to zero, the weight no longer "
            "matters, and nothing is left over to test. A theory can only be rejected by GMM if it says more than "
            "the parameters can absorb. The next chapter's theory says a great deal."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.5, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()
