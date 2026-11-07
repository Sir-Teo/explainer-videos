from __future__ import annotations

import numpy as np

from videos.stats.stats49.common import *  # noqa: F403


class HigherOrder(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.estimators()
        self.chart()
        self.beyond()

    def card(self):
        card = chapter_card(10, r"Higher-order influence functions", r"When the first-order correction is not enough", lit=(2008,), part=PART)
        with self.voiceover("Chapter ten. Higher-order influence functions: when the first-order correction is not enough."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\psi(f) = \textstyle\int f^2", r":", r"\phi^*(x) = 2(f(x) - \psi), \ \ E\,\phi^{*2} = 4\,\mathrm{Var} f(X)", font_size=32),
            cmath(r"\psi(\hat f) - \psi(f) + \text{correction}", r"=", r"-\textstyle\int (\hat f - f)^2: \ \text{exactly second order}", font_size=32),
            cmath(r"\|\hat f - f\|^2", r"\asymp", r"h^{2s} + \frac{1}{nh^d}: \ \text{bias}^2 + \text{variance}", font_size=34),
            cmath(r"\text{root-}n \text{ needs}", r":", r"\|\hat f - f\|^2 = o(n^{-1/2}): \ \text{ordinary density plug-in route needs }s>d/2", font_size=32),
        ]
        rows[1][-1].set_color(EFFC)
        rows[3][-1].set_color(NUIC)
        whys = [why(r"a classic: \ Bickel \& Ritov (1988)"), why(r"the one-step's remainder"), why(r"a kernel estimate, \ smoothness $s$"), why(r"the product rate, \ with one function")]
        heading = label('First-order and quadratic estimators have different smoothness thresholds', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A classic test case is the integrated square of a density with finite integral of f cubed, which appears in bandwidth selection and in the efficiency of rank tests. Its efficient influence function is twice the density at x minus twice psi. <bookmark mark='b'/> Plug in a kernel estimate and add the first-order correction, and what remains is exactly minus the integrated squared error of the density estimate. <bookmark mark='c'/> That error is a squared bias, which shrinks with the bandwidth, plus a variance of order one over n h, which grows as the bandwidth shrinks. <bookmark mark='d'/> For root n estimation the squared error must be smaller than one over root n, For an ordinary optimal L-two density estimate with error order n to the minus s over two s plus d, this first-order route needs s greater than d over two. A second-order quadratic estimator can reach root n already above d over four, under the appropriate smoothness and bandwidth conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def estimators(self):
        rows = [
            cmath(r"\text{plug-in}", r":", r"\textstyle\int \hat f^2 = \frac{1}{n^2}\sum_{i,j} \bar K_h(X_i - X_j), \ \text{diagonal included}", font_size=30),
            cmath(r"\text{one-step}", r":", r"\textstyle\int \hat f_A^2 + \frac{1}{|B|}\sum_{i \in B} 2(\hat f_A(X_i) - \int \hat f_A^2), \ \text{split sample}", font_size=28),
            cmath(r"\text{second order}", r":", r"\frac{1}{n(n-1)}\textstyle\sum_{i \ne j} \bar K_h(X_i - X_j): \ \text{a U-statistic}", font_size=30),
            cmath(r"\text{what it removes}", r":", r"\text{diagonal self-pair bias; sampling variance remains}", font_size=32),
        ]
        rows[0][-1].set_color(PLUGC)
        rows[1][-1].set_color(OSC)
        rows[2][-1].set_color(EFFC)
        whys = [why(r"$\bar K_h = K_h * K_h$"), why(r"chapter 6, \ literally"), why(r"Robins, \ Li, \ Tchetgen \& van der Vaart (2008)"), why(r"a quadratic correction")]
        heading = label('Distinct-pair kernels remove diagonal bias, not sampling variance', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Three estimators. The plug-in, the integral of the squared kernel estimate, is an average of a kernel over all pairs of points, including each point paired with itself. <bookmark mark='b'/> The one-step estimator of chapter six, with the density fitted on one half of the sample and the correction averaged over the other. <bookmark mark='c'/> And a second-order estimator: the same pairwise average, but over distinct pairs only, a U-statistic. James Robins, Lingling Li, Eric Tchetgen Tchetgen and Aad van der Vaart built the general theory of such higher-order influence functions in 2008. <bookmark mark='d'/> For the quadratic kernel functional, distinct pairs remove the diagonal self-pair bias. The U-statistic still has sampling variance, including a degenerate term of order one over n squared h to the d, as well as smoothing bias."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("intsq")
        hs = np.asarray([r["h"] for r in d["rows"]])
        A = axes([0, 0.65], [-1, 0.4], x_length=7.4, y_length=4.4, xlabel=r"bandwidth $h$", ylabel=r"$\sqrt n \times$ bias",
                 xticks=[0, 0.2, 0.4, 0.6], yticks=[-1, -0.5, 0, 0.25], center=[-2.5, 0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.65, 0), color=GREY_B, stroke_width=2)

        def line(k, c):
            v = [r[k]["rbias"] for r in d["rows"]]
            return VGroup(polyline(ax, hs, v, c, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=c) for a, b in zip(hs, v)])

        cp, co, cu = line("plugin", PLUGC), line("one_step", OSC), line("ustat", EFFC)
        r0 = d["rows"][0]
        side = fit_rows(VGroup(
            label(rf"$N(0,1)$ data, \ $n = {d['n']}$; \ $\psi = 1/(2\sqrt\pi)$", font_size=22),
            label(r"purple: \ plug-in: \ diagonal, \ then smoothing", font_size=22, color=PLUGC),
            label(r"teal: \ one-step: \ $-\|\hat f_A - f\|^2$ remains", font_size=22, color=OSC),
            label(rf"gold: \ U-statistic: \ {r0['ustat']['rbias']:+.2f} at $h = 0.05$", font_size=22, color=EFFC),
            label(rf"its SD there: \ {r0['ustat']['sd']:.3f} vs.\ the bound {d['eff_sd']:.3f}", font_size=22, color=TANC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Normal samples of four hundred, and root n times the bias of each estimator across "
            f"bandwidths. <bookmark mark='b'/> The plug-in is biased upward at small bandwidths, by the diagonal terms, and "
            f"downward at large ones, by smoothing. <bookmark mark='c'/> The one-step estimator is still biased at small "
            f"bandwidths: its remainder, minus the squared error of a noisy half-sample estimate, is not negligible. "
            f"<bookmark mark='d'/> The second-order U-statistic is nearly unbiased at small bandwidths: "
            f"{say(r0['ustat']['rbias'], 2)} at h equal to point oh five. <bookmark mark='e'/> And its standard deviation "
            f"there, {say(r0['ustat']['sd'], 3)}, is close to the efficient {say(d['eff_sd'], 3)}. One more order of the "
            f"expansion bought both."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(simulated_tag(r"simulated: \ 600 samples per $h$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(co), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cu), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"higher-order influence functions: \ U-statistics of order $m$ that cancel the remainder term by term", font_size=26),
            label(r"when nuisances are too rough for root-$n$: \ quadratic-density RMSE $n^{-\min(1/2,4s/(4s+d))}$ under suitable smoothness", font_size=26, color=EFFC),
            label(r"the ATE: \ the same, \ with $\|\hat e - e\|\,\|\hat\mu - \mu\|$ in place of $\|\hat f - f\|^2$", font_size=26, color=TANC),
            label(r"minimax lower bounds say this is the best possible: \ Part 50", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Higher-order corrections can be implemented by U-statistics, often using finite-dimensional projection kernels. Exact higher-order influence functions need not exist as square-integrable kernels in an unrestricted continuous model. <bookmark mark='b'/> They matter when the nuisances are too rough for root n estimation: for integrated squared density in suitable smoothness balls, the low-smoothness minimax root-mean-square rate is n to the minus four s over four s plus d, capped at root n. This is a model-specific rate, not a universal rate for all functionals. <bookmark mark='c'/> Higher-order treatment-effect estimators can also reduce product remainders, but their rates depend on several nuisance smoothness levels, covariate dimension and design assumptions, with the product of the propensity's and the outcome regression's errors in place of the density's squared error. <bookmark mark='d'/> That this rate is the best anyone can do is a minimax statement, which is Part fifty's subject."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
