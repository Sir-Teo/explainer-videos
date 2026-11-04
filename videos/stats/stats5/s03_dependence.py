from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Dependence(VoiceoverScene):
    def construct(self):
        self.card()
        self.gallery()
        self.covariance()

    def card(self):
        card = chapter_card(2, r"Dependence", r"Uncorrelated is not independent", lit=(), part=PART)
        with self.voiceover("Chapter two. Dependence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def gallery(self):
        d = load("dependence")
        specs = [("x", "y", r"$Y = X^2 + \text{noise}$", d["r_par"], [-3, 3], [-0.5, 9]),
                 ("cx", "cy", r"a ring", d["r_ring"], [-1.4, 1.4], [-1.4, 1.4]),
                 ("x", "z", r"$Y = S X$, \ $S = \pm 1$", d["r_sign"], [-3.2, 3.2], [-3.2, 3.2])]
        panels = VGroup()
        for k, (a, b, ttl, r, xr, yr) in enumerate(specs):
            A = axes(xr, yr, x_length=3.6, y_length=3.0, center=[-4.4 + 4.4 * k, 0.2, 0])
            A.ax.x_axis.set_opacity(0.4)
            A.ax.y_axis.set_opacity(0.4)
            pts = scatter(A.ax, d[a], d[b], color=SIM, radius=0.02, opacity=0.6)
            t = label(ttl, font_size=24).next_to(A, UP, buff=0.2)
            rr = MathTex(rf"r = {r:.3f}", font_size=30, color=S.ACCENT).next_to(A, DOWN, buff=0.25)
            panels.add(VGroup(A, pts, t, rr))
        sign = label(rf"knowing $|X| > 1.5$ makes $|Y| > 1.5$ certain: \ {100 * d['p_big']:.0f}\% $\to$ "
                     rf"{100 * d['p_big_given']:.0f}\%", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Correlation measures one kind of dependence: how well a straight line fits. <bookmark mark='a'/> Here y "
            "is x squared, plus a little noise: completely determined by x. Yet the correlation is zero, because "
            "the parabola's two arms cancel. <bookmark mark='b'/> A ring: knowing x pins y to two values, yet the "
            "correlation is zero. <bookmark mark='c'/> And here y is x times a random sign. Each variable is "
            "standard normal, the correlation is zero, but the size of y is exactly the size of x: if x is beyond "
            "one and a half, so is y, every time. <bookmark mark='d'/> Independence implies zero correlation. Zero "
            "correlation implies nothing of the kind."
        ) as vo:
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k][0]), FadeIn(panels[k][2]), FadeIn(panels[k][1], lag_ratio=0.002),
                          FadeIn(panels[k][3]))
            self.play(FadeIn(sign))
            vo.wait_until("d")
            self.play(*[Indicate(p[3], color=S.RESID) for p in panels])
        self.clear_scene()

    def covariance(self):
        rows = [
            cmath(r"\mathrm{Cov}(X, Y)", r"=", r"E[(X - EX)(Y - EY)]", r"=", r"E[XY] - EX\, EY", font_size=34),
            cmath(r"\Sigma", r"=", r"\mathrm{Cov}(\mathbf X)", r"=", r"E[(\mathbf X - \boldsymbol\mu)(\mathbf X - \boldsymbol\mu)^\top]",
                  font_size=34),
            cmath(r"\mathbf u^\top \Sigma\, \mathbf u", r"=", r"\mathrm{Var}(\mathbf u^\top \mathbf X)", r"\ge", r"0", font_size=36),
            cmath(r"|\mathrm{Cov}(X, Y)|", r"\le", r"\sigma_X\,\sigma_Y", font_size=36),
        ]
        rows[2][0].set_color(S.ACCENT)
        whys = [why(r"the expected product of deviations"), why(r"all the pairs, \ as a matrix"),
                why(r"PSD: \ Part 4, chapter 5"), why(r"Cauchy--Schwarz in $L^2$: \ $|\rho| \le 1$")]
        lp = label(r"random variables with finite variance form an inner-product space, \ $L^2$: \ $\langle X, Y\rangle = E[XY]$",
                   font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Covariance is what correlation is built from. <bookmark mark='a'/> The expected product of the two "
            "deviations from the means, or the mean of the product minus the product of the means. "
            "<bookmark mark='b'/> For a vector of variables, all the covariances form a matrix, <bookmark mark='c'/> "
            "and it's positive semidefinite, by Part 4's argument: every linear combination has a variance, and "
            "variances aren't negative. <bookmark mark='d'/> And covariance is bounded by the product of the "
            "standard deviations: Cauchy–Schwarz again. <bookmark mark='e'/> That's not a coincidence. Random "
            "variables with finite variance form an inner-product space, with the expected product as the inner "
            "product. Covariance is an inner product, correlation a cosine, and in the next chapter conditional "
            "expectation will be a projection."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.6, buff=0.5, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(lp))
        self.clear_scene()
