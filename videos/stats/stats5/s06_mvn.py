from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class MVN(VoiceoverScene):
    def construct(self):
        self.card()
        self.affine()
        self.properties()
        self.counterexample()
        self.check()

    def card(self):
        card = chapter_card(5, r"The multivariate normal", r"Independent normals, \ stretched and turned", lit=(1886,), part=PART)
        with self.voiceover("Chapter five. The multivariate normal."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def affine(self):
        d = load("mvn")
        z, x = np.asarray(d["z"]), np.asarray(d["x"])
        A_ = np.asarray(d["A"])
        c0 = np.array([-3.2, -0.5, 0])
        sc = 0.62
        frame = VGroup(Line(c0 + LEFT * 3.2, c0 + RIGHT * 3.2, color=GREY_D), Line(c0 + DOWN * 3.0, c0 + UP * 3.0, color=GREY_D))
        dots = VGroup(*[Dot(c0 + sc * np.array([a, b, 0]), radius=0.022, color=SIM, fill_opacity=0.7) for a, b in z])
        circ = Circle(radius=sc * 2, stroke_color=GREY_B, stroke_width=1.5).move_to(c0)
        mu = np.asarray(d["mu"])
        Sg = np.asarray(d["Sigma"])
        ev, V = np.linalg.eigh(Sg)
        th = np.linspace(0, TAU, 120)
        ell = VMobject(stroke_color=S.ACCENT, stroke_width=2.5).set_points_smoothly(
            [c0 + sc * np.array([*(mu + 2 * (np.sqrt(ev[0]) * np.cos(t) * V[:, 0] + np.sqrt(ev[1]) * np.sin(t) * V[:, 1])), 0])
             for t in th])
        dfn = definition_card(r"Multivariate normal", r"$\mathbf X = A\mathbf Z + \boldsymbol\mu$ with $\mathbf Z$ independent "
                              r"standard normals: \ $\mathbf X \sim N(\boldsymbol\mu, \Sigma)$, \ $\Sigma = AA^\top$", color=S.ACCENT,
                              width=6.0, font_size=24).move_to([3.4, 2.3, 0])
        rows = VGroup(MathTex(r"A = " + mat_tex_(A_), font_size=30), MathTex(r"\Sigma = AA^\top = " + mat_tex_(Sg), font_size=30, color=S.ACCENT),
                      MathTex(r"\text{sample covariance: }" + mat_tex_(np.asarray(d["emp"])), font_size=26, color=SIM))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.4, 0])
        dens = MathTex(r"f(\mathbf x) = (2\pi)^{-p/2}\det(\Sigma)^{-1/2} e^{-\frac12(\mathbf x - \boldsymbol\mu)^\top\Sigma^{-1}(\mathbf x - "
                       r"\boldsymbol\mu)}", font_size=26).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.6)
        dw = label(r"Part 3's change of variables, \ with Part 4's Jacobian $|\det A|$", font_size=20, color=GREY_B).next_to(dens, UP, buff=0.12)
        with self.voiceover(
            "Galton's ellipses belong to one distribution, and it has a simple definition. <bookmark mark='a'/> "
            "Start with independent standard normals: a round cloud. <bookmark mark='b'/> Multiply by a matrix A "
            "and add a vector mu. <bookmark mark='c'/> The cloud stretches, turns and moves, and its circles become "
            "ellipses. That's the multivariate normal: any affine image of independent standard normals. Its "
            "covariance is A A transpose, by Part 4's rule, and the sample covariance of the simulated points "
            "agrees. <bookmark mark='d'/> Its density follows from the change of variables: the inverse of Sigma in "
            "the exponent, and the square root of its determinant, the Jacobian, in front."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(dots, lag_ratio=0.001), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(*[dt.animate.move_to(c0 + sc * np.array([a, b, 0])) for dt, (a, b) in zip(dots, x)],
                      Transform(circ, ell), run_time=3.0)
            self.play(FadeIn(rows[1:]))
            vo.wait_until("d")
            self.play(FadeIn(dens), FadeIn(dw))
        self.clear_scene()

    def properties(self):
        rows = VGroup(
            MathTex(r"B\mathbf X + \mathbf c \sim N(B\boldsymbol\mu + \mathbf c,\ B\Sigma B^\top)", r"\quad \text{affine images stay normal}",
                    font_size=30),
            MathTex(r"X_1 \sim N(\mu_1, \Sigma_{11})", r"\quad \text{marginals: } B = (1\ \ 0)", font_size=30),
            MathTex(r"\mathbf u^\top \mathbf X \sim N(\mathbf u^\top\boldsymbol\mu,\ \mathbf u^\top\Sigma\mathbf u)", r"\quad \text{every linear "
                    r"combination is normal}", font_size=30),
            MathTex(r"\text{ellipsoids: } (\mathbf x - \boldsymbol\mu)^\top\Sigma^{-1}(\mathbf x - \boldsymbol\mu) = c^2", r"\quad \text{Part 4's spectral "
                    r"theorem}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.6, 0])
        for r in rows:
            r[1].set_color(GREY_B)
            if r.width > 12.8:
                r.width = 12.8
        crm = label(r"Cram\'er--Wold: \ a vector is multivariate normal \ iff \ every linear combination is normal", font_size=26,
                    color=S.ACCENT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "From the definition, everything follows. <bookmark mark='a'/> An affine image of a multivariate normal "
            "is again multivariate normal, with covariance B Sigma B transpose. <bookmark mark='b'/> So the marginals "
            "are normal: pick out coordinates with a matrix of zeros and ones. <bookmark mark='c'/> Every linear "
            "combination is normal. <bookmark mark='d'/> And the contours of the density are the ellipsoids of the "
            "spectral theorem. <bookmark mark='e'/> In fact the third property characterizes it: a vector is "
            "multivariate normal exactly when every linear combination of its coordinates is normal, a consequence "
            "of the Cramér–Wold device that Part 6 will use."
        ) as vo:
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(crm))
        self.clear_scene()

    def counterexample(self):
        d = load("dependence")
        x, z = np.asarray(d["x"]), np.asarray(d["z"])
        A = axes([-3.2, 3.2], [-3.2, 3.2], x_length=5.0, y_length=5.0, xlabel=r"$X$", ylabel=r"$Y = SX$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], center=[-3.6, -0.4, 0])
        pts = scatter(A.ax, x, z, color=SIM, radius=0.022)
        rows = VGroup(
            label(r"$X$ normal, \ $Y$ normal, \ $\mathrm{Cov}(X, Y) = 0$", font_size=28),
            label(r"but $|Y| = |X|$: \ not independent", font_size=28, color=S.RESID),
            label(r"and $X + Y = 0$ half the time: \ not jointly normal", font_size=28, color=S.RESID),
            label(r"for a \emph{jointly} normal vector: \ uncorrelated $\iff$ independent", font_size=28, color=S.ACCENT),
            MathTex(r"\Sigma \text{ diagonal} \ \Rightarrow\ f(\mathbf x) = \prod_i f_i(x_i)", font_size=30, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.8, 0.2, 0])
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        with self.voiceover(
            "There's one trap. <bookmark mark='a'/> Remember the random-sign pair from chapter two: X standard normal, "
            "Y equal to X times a random sign. Y is standard normal too, and they're uncorrelated. "
            "<bookmark mark='b'/> But they're dependent, since the size of Y is the size of X. <bookmark mark='c'/> And "
            "the pair isn't jointly normal: X plus Y is exactly zero half the time, and no normal variable does that. "
            "<bookmark mark='d'/> Two normals need not be jointly normal. When they are, the special property holds: "
            "uncorrelated means independent, because a diagonal covariance makes the density factor."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.001))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()


    def check(self):
        e = load("extras")["mvncheck"]
        emp, theo = np.asarray(e["emp"]), np.asarray(e["theo"])
        A = axes([0, 16], [0, 16], x_length=5.0, y_length=5.0, xlabel=r"$\chi^2_3$ quantiles", ylabel=r"sorted $d_M^2$",
                 xticks=[0, 4, 8, 12, 16], yticks=[0, 4, 8, 12, 16], center=[-3.6, -0.4, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(16, 16), color=GREY_C, stroke_width=1.5)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=SIM) for a, b in zip(theo, emp) if a < 16 and b < 16])
        rows = VGroup(
            MathTex(r"d_M^2 = (\mathbf X - \boldsymbol\mu)^\top \Sigma^{-1} (\mathbf X - \boldsymbol\mu) = \|\mathbf Z\|^2 \sim \chi^2_p",
                    font_size=28),
            label(r"so: \ a QQ plot of squared Mahalanobis distances against $\chi^2_p$ \ checks multivariate normality", font_size=24,
                  color=GREY_A),
            label(r"Part 1's QQ plot, \ in $p$ dimensions at once", font_size=24, color=S.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.9, 0.6, 0])
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        tag = note(r"simulated: 4,000 draws from a 3-dimensional normal").to_corner(DR, buff=0.3)
        with self.voiceover(
            "How would you check that data are multivariate normal? <bookmark mark='a'/> Whiten them: the squared "
            "Mahalanobis distance of a multivariate normal vector is the squared length of the underlying standard "
            "normal, so it's chi-squared with p degrees of freedom. <bookmark mark='b'/> So sort the squared "
            "distances and plot them against chi-squared quantiles: Part 1's QQ plot, now testing p dimensions at "
            "once. <bookmark mark='c'/> For four thousand simulated three-dimensional normal vectors, the points lie "
            "on the diagonal. Curvature at the top would signal heavy tails or outliers, which Part 30 hunts."
        ) as vo:
            self.play(FadeIn(A), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), run_time=2.0)
        self.clear_scene()


def mat_tex_(M, fmt="{:.2f}") -> str:
    rows = [" & ".join(fmt.format(v) for v in r) for r in np.atleast_2d(M)]
    return r"\begin{pmatrix}" + r" \\ ".join(rows) + r"\end{pmatrix}"
