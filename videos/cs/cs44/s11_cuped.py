from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load


def _spread(ax, x, ys, color):
    """A vertical bar at x spanning the mean plus or minus two standard deviations of ys, with end ticks."""
    m, s = float(np.mean(ys)), float(np.std(ys))
    a, b = ax.c2p(x, m - 2 * s), ax.c2p(x, m + 2 * s)
    return VGroup(Line(a, b, color=color, stroke_width=4), Line(a + LEFT * 0.1, a + RIGHT * 0.1, color=color),
                  Line(b + LEFT * 0.1, b + RIGHT * 0.1, color=color))


class Cuped(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.derive()
        self.measured()
        self.interval()
        self.strata()

    def card(self):
        card = chapter_card(10, r"Less noise, \ same truth", r"Can a user's past make an experiment more precise?",
                            lit=(2013,), extra=((2013, r"Deng, \ Xu, \ Kohavi and Walker: \ CUPED"),), part=PART)
        with self.voiceover("Chapter ten. Less noise, same truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"What the past already explains", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(44)
        x = rng.normal(0, 1, 70)
        y = 0.85 * x + np.sqrt(1 - 0.85 ** 2) * rng.normal(0, 1, 70)
        theta = float(np.cov(x, y)[0, 1] / x.var())
        g = axes([-3, 3, 1], [-3.2, 3.2, 1], x_length=5.6, y_length=4.6, x_label=r"$X$: \ the user's metric in the "
                 r"month before", y_label=r"$Y$: \ the same metric during the experiment").move_to([-3.0, -0.4, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=DATA) for a, b in zip(x, y)])
        flat = VGroup(*[Dot(ax.c2p(a, b - theta * (a - x.mean())), radius=0.05, color=YES) for a, b in zip(x, y)])
        fit = Line(ax.c2p(-2.9, y.mean() + theta * (-2.9 - x.mean())), ax.c2p(2.9, y.mean() + theta * (2.9 - x.mean())),
                   color=HEAD, stroke_width=3)
        level = Line(ax.c2p(-2.9, y.mean()), ax.c2p(2.9, y.mean()), color=HEAD, stroke_width=3)
        sp0 = _spread(ax, 3.3, y, DATA)
        sp1 = _spread(ax, 3.3, y - theta * (x - x.mean()), YES)
        ill = note(r"illustrative", font_size=17).next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        notes = VGroup(
            wrapped_label(r"most of the spread in $Y$ is who the user is, \ not which version they saw", 5.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"CUPED \ (Deng, \ Xu, \ Kohavi and Walker, \ Microsoft, \ 2013): \ controlled experiments "
                          r"using pre-experiment data", 5.4, font_size=20, color=GREY_A),
            MathTex(r"Y_{\text{cv}} = Y - \theta\,(X - \bar X)", font_size=34, color=YES),
            wrapped_label(r"subtract what last month predicts; \ the treatment's effect is untouched, \ the noise "
                          r"shrinks", 5.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "Most of the variation in a metric has nothing to do with the experiment. A user who spent a lot last "
            "month will probably spend a lot this month, whatever version they see. <bookmark mark='a'/> Plot each "
            "user's metric during the experiment against the same metric in the month before. The spread of the "
            "metric is mostly who the user is. <bookmark mark='b'/> In 2013 Alex Deng, Ya Xu, Ron Kohavi and Toby "
            "Walker, at Microsoft, called the remedy CUPED. <bookmark mark='c'/> Subtract from each user what their "
            "past predicts: theta times their pre-period metric, less its average. <bookmark mark='d'/> The cloud "
            "flattens, and the spread shrinks. The difference between the versions is untouched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), run_time=2)
            self.play(Create(sp0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(fit), Write(notes[2]))
            vo.wait_until("d")
            self.play(Transform(dots, flat), Transform(fit, level), Transform(sp0, sp1), run_time=2.5)
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        head = label(r"Why $1 - \rho^2$", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"\operatorname{Var}(Y - \theta X)", r"=", r"\operatorname{Var}Y - 2\theta\,"
                    r"\operatorname{Cov}(X,Y) + \theta^2\operatorname{Var}X", font_size=34),
            MathTex(r"\frac{d}{d\theta} = 0", r"\;\Rightarrow\;", r"\theta^\ast = \frac{\operatorname{Cov}(X,Y)}"
                    r"{\operatorname{Var}X}", font_size=34, color=HEAD),
            MathTex(r"\operatorname{Var}(Y - \theta^\ast X)", r"=", r"\operatorname{Var}Y - \frac{\operatorname{Cov}"
                    r"(X,Y)^2}{\operatorname{Var}X}", font_size=34),
            MathTex(r"", r"=", r"\operatorname{Var}Y\,(1 - \rho^2), \qquad \rho = \frac{\operatorname{Cov}(X,Y)}"
                    r"{\sqrt{\operatorname{Var}X\,\operatorname{Var}Y}}", font_size=34, color=YES),
        ).arrange(DOWN, buff=0.38)
        for s in steps[1:]:
            s.shift((steps[0][1].get_x() - s[1].get_x()) * RIGHT)
        steps.next_to(head, DOWN, buff=0.5).set_x(0)
        whys = VGroup(
            wrapped_label(r"$\theta^\ast$: \ the slope of the regression of $Y$ on $X$", 3.6, font_size=19,
                          color=HEAD),
            wrapped_label(r"same truth: \ $X$ is measured before randomization, \ so both groups have the same mean "
                          r"$X$ in expectation, \ and subtracting $\theta(\bar X_T - \bar X_C)$ leaves the expected "
                          r"difference unchanged", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the covariate must not be affected by the treatment: \ use the past, \ never something "
                          r"measured during the test", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        whys[1:].arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(steps, DOWN, buff=0.45)
        whys[0].next_to(steps[1], RIGHT, buff=0.5)
        with self.voiceover(
            "How much does it help? <bookmark mark='a'/> Expand the variance of the adjusted metric: the variance "
            "of Y, minus twice theta times the covariance, plus theta squared times the variance of X. "
            "<bookmark mark='b'/> It is a parabola in theta, smallest where the derivative vanishes: at the "
            "covariance over the variance of X, the slope of the regression line. <bookmark mark='c'/> Put that "
            "back, and the variance is the plain one times one minus rho squared, rho being the correlation of "
            "past and present. <bookmark mark='d'/> And the truth is the same, because X was measured before "
            "randomization: both groups have the same average past, in expectation, so the adjustment removes noise "
            "and not effect. Hence the one rule: never adjust by anything the treatment could change."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(Write(steps[1]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(whys[1]))
            self.play(FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        rows = load("cuped")["rows"]
        head = label(r"Measured on simulated experiments", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, len(rows), 1], [0, 1.1, 0.25], x_length=7.4, y_length=4.0,
                 y_label=r"variance with CUPED $\div$ \ without", yticks=(0.25, 0.5, 0.75, 1.0)).move_to(
            [-2.6, -0.2, 0])
        ax = g.ax
        bars, vals, ticks, names, gains = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for k, r in enumerate(rows):
            x = k + 0.5
            b = Rectangle(width=0.8, height=max(0.02, ax.c2p(0, r["ratio"])[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                          fill_color=DATA, fill_opacity=0.85)
            b.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.add(b)
            vals.add(label(f"{r['ratio']:.2f}", font_size=18, color=DATA).next_to(b, UP, buff=0.18))
            ticks.add(Line(ax.c2p(x - 0.5, r["theory"]) + RIGHT * 0.12, ax.c2p(x + 0.5, r["theory"]) + LEFT * 0.12,
                           color=HEAD, stroke_width=4))
            names.add(label(rf"$\rho = {r['rho']:.1f}$", font_size=18, color=GREY_A).next_to(ax.c2p(x, 0), DOWN,
                                                                                         buff=0.15))
            gains.add(label(rf"$\times{1 / r['ratio']:.1f}$", font_size=18, color=YES).next_to(names[-1], DOWN,
                                                                                            buff=0.15))
        glab = label(r"worth this many times the users", font_size=17, color=YES).next_to(gains, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(r"20,000 users per arm, \ 2,000 repeated experiments for each correlation", 4.2,
                          font_size=19, color=GREY_A),
            VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=DATA, fill_opacity=0.85),
                   label(r"measured", font_size=19, color=DATA)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.3, color=HEAD, stroke_width=4),
                   label(r"theory: \ $1 - \rho^2$", font_size=19, color=HEAD)).arrange(RIGHT, buff=0.15),
            MathTex(r"\text{equivalent sample size} = \frac{1}{1 - \rho^2}", font_size=28, color=YES),
            wrapped_label(r"in practice, \ last month's value of the same metric is often the best covariate", 4.2,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -0.2, 0])
        r9 = rows[-1]
        r7 = next(r for r in rows if abs(r["rho"] - 0.7) < 1e-9)
        with self.voiceover(
            "We checked the formula on simulated experiments: twenty thousand users per arm, repeated two thousand "
            "times for each of five correlations. <bookmark mark='a'/> The blue bars are the measured "
            "variance with CUPED, divided by the variance without; the yellow marks are one minus rho squared. "
            "<bookmark mark='b'/> They agree, from no help at all when the past says nothing, "
            f"<bookmark mark='c'/> to a variance cut to {r7['ratio']:.2f} at a correlation of point seven, and "
            f"{r9['ratio']:.2f} at point nine. <bookmark mark='d'/> Variance falls as one over the number of users, "
            f"so a correlation of point seven is worth about {1 / r7['ratio']:.0f} times the traffic, and point nine "
            f"about {1 / r9['ratio']:.0f} times: weeks of experiment, for one line of arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(names), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b, DOWN) for b in bars[:3]], *[FadeIn(v) for v in vals[:3]],
                      *[Create(t) for t in ticks[:3]])
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b, DOWN) for b in bars[3:]], *[FadeIn(v) for v in vals[3:]],
                      *[Create(t) for t in ticks[3:]])
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), FadeIn(gains), FadeIn(glab))
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def interval(self):
        rows = load("cuped")["rows"]
        eff = rows[0]["effect"]
        head = label(r"The interval shrinks", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = -0.01, 0.045
        line = NumberLine(x_range=[lo, hi, 0.01], length=11.0, color=GREY_C, include_ticks=True).move_to(
            [0, 0.2, 0])
        tl = VGroup(*[label(f"{v:.2f}", font_size=17, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.15)
                      for v in (0.0, 0.01, 0.02, 0.03, 0.04)])
        zero = DashedLine(line.n2p(0) + UP * 1.4, line.n2p(0) + DOWN * 0.15, color=NO)
        zl = label(r"no effect", font_size=17, color=NO).next_to(zero, UP, buff=0.08)
        dot = Dot(line.n2p(eff) + UP * 0.6, radius=0.08, color=HEAD)
        dl = label(rf"true effect \ {eff:.2f}", font_size=17, color=HEAD).next_to(dot, UP, buff=0.25)

        def bar(r, key, col):
            h = r[key]
            return VGroup(Line(line.n2p(eff - h) + UP * 0.6, line.n2p(eff + h) + UP * 0.6, color=col,
                               stroke_width=7),
                          Line(line.n2p(eff - h) + UP * 0.45, line.n2p(eff - h) + UP * 0.75, color=col),
                          Line(line.n2p(eff + h) + UP * 0.45, line.n2p(eff + h) + UP * 0.75, color=col))
        plain = bar(rows[0], "ci_plain", DATA)
        cur = bar(rows[0], "ci_plain", YES)

        def readout(r):
            return label(rf"$\rho = {r['rho']:.1f}$: \ $\pm {r['ci_cuped']:.4f}$ \ (without CUPED $\pm "
                         rf"{r['ci_plain']:.4f}$)", font_size=22, color=YES).next_to(line, DOWN, buff=0.9)
        ro = readout(rows[0])
        unit = note(r"effect in units of the metric's standard deviation; \ 95\% intervals, \ half-width $1.96$ "
                    r"times the measured spread of the estimate", font_size=18).to_edge(DOWN, buff=1.2)
        foot = wrapped_label(r"the same users and the same effect; \ only the noise the past explains is gone", 12.4,
                             font_size=21, color=WHITE).to_edge(DOWN, buff=0.45)
        r7, r9 = rows[3], rows[-1]
        with self.voiceover(
            "Here is what that means for one experiment's conclusion. <bookmark mark='a'/> The true effect is "
            "point zero two standard deviations. Without CUPED, the ninety-five percent interval reaches almost "
            "as far as the effect itself on either side, and only just clears zero. <bookmark mark='b'/> Now raise "
            "the correlation with the past. At point five the interval narrows a little; <bookmark mark='c'/> at "
            f"point seven, by {100 * (1 - r7['ci_cuped'] / r7['ci_plain']):.0f} percent; <bookmark mark='d'/> at "
            f"point nine, by {100 * (1 - r9['ci_cuped'] / r9['ci_plain']):.0f} percent, to less than half its "
            "width. "
            "<bookmark mark='e'/> The same users and the same effect; the only thing removed is the noise that "
            "each user's own history already explained."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(tl), Create(zero), FadeIn(zl), FadeIn(unit))
            vo.wait_until("a")
            self.play(FadeIn(dot), FadeIn(dl), Create(plain))
            self.add(cur)
            self.play(FadeIn(ro))
            for mk, k in (("b", 2), ("c", 3), ("d", 4)):
                vo.wait_until(mk)
                self.play(Transform(cur, bar(rows[k], "ci_cuped", YES)), Transform(ro, readout(rows[k])),
                          run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def strata(self):
        head = label(r"Stratification, \ and regression in general", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(10)
        groups = [(-1.4, 0.45, LAM, r"light users"), (1.2, 0.5, KERN, r"heavy users")]
        col = VGroup()
        for k, (m, s, c, _) in enumerate(groups):
            ys = m + s * rng.normal(0, 1, 26)
            col.add(VGroup(*[Dot([-4.5 + 1.5 * k + rng.uniform(-0.25, 0.25), y * 0.95, 0], radius=0.05, color=c)
                             for y in ys]))
        allg = VGroup(*[Dot(d.get_center(), radius=0.05, color=DATA) for grp in col for d in grp])
        total = DoubleArrow([-5.7, -2.6, 0], [-5.7, 2.5, 0], buff=0, color=DATA, stroke_width=3,
                            max_tip_length_to_length_ratio=0.05)
        tl = label(r"total spread", font_size=17, color=DATA).next_to(total, LEFT, buff=0.1).rotate(PI / 2)
        tl.next_to(total, LEFT, buff=0.1)
        within = VGroup(*[DoubleArrow([-4.5 + 1.5 * k + 0.5, (m - 2 * s) * 0.95, 0],
                                      [-4.5 + 1.5 * k + 0.5, (m + 2 * s) * 0.95, 0], buff=0, color=c,
                                      stroke_width=3, max_tip_length_to_length_ratio=0.15)
                          for k, (m, s, c, _) in enumerate(groups)])
        gl = VGroup(*[label(t, font_size=17, color=c).next_to(col[k], DOWN, buff=0.2)
                      for k, (_, _, c, t) in enumerate(groups)])
        ill = note(r"illustrative", font_size=17).move_to([-3.9, -3.5, 0])
        eqs = VGroup(
            MathTex(r"\operatorname{Var}Y = \underbrace{\mathbb{E}\,\operatorname{Var}(Y \mid S)}_{\text{within}} + "
                    r"\underbrace{\operatorname{Var}\,\mathbb{E}(Y \mid S)}_{\text{between strata}}", font_size=30),
            wrapped_label(r"\textbf{stratify}: \ compare versions within each stratum \ (platform, \ country, \ "
                          r"heavy or light), \ then weight the strata; \ the between-strata part drops out", 7.6,
                          font_size=20, color=WHITE),
            MathTex(r"Y = \alpha + \tau\, T + \beta_1 X_1 + \beta_2 X_2 + \dots + \varepsilon", font_size=30,
                    color=YES),
            wrapped_label(r"\textbf{regression adjustment}: \ CUPED with one covariate is the simplest case; \ "
                          r"with many, \ or with a model's prediction of $Y$ from the past, \ the same rule holds: \ "
                          r"pre-treatment covariates only", 7.6, font_size=20, color=YES),
            wrapped_label(r"with treatment-by-covariate terms, \ adjustment cannot hurt precision in large samples \ "
                          r"(Lin, \ 2013)", 7.6, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.6, -0.3, 0])
        with self.voiceover(
            "CUPED belongs to an old family. <bookmark mark='a'/> When users fall into groups that behave "
            "differently, light and heavy users say, part of the spread lies between the groups. "
            "<bookmark mark='b'/> Stratification compares the versions within each group and then weights the "
            "groups, so the between-group part drops out of the noise. <bookmark mark='c'/> In general, regress "
            "the metric on the treatment and on covariates measured before it; the treatment's coefficient is the "
            "effect. CUPED is the one-covariate case, and the covariate can be a model's prediction from the past. "
            "<bookmark mark='d'/> Winston Lin showed in 2013 that, with interaction terms, this cannot hurt "
            "precision in large samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(allg), Create(total), FadeIn(tl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Transform(allg, VGroup(*[d.copy() for grp in col for d in grp])), FadeIn(gl), FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(Create(within), FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(eqs[3]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[4]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO, LAM)
