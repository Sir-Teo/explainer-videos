from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403

FERT = [r"none", r"N", r"P", r"NPK"]


class Anova(VoiceoverScene):
    def construct(self):
        self.card()
        self.trial()
        self.decompose()
        self.pythagoras()
        self.f_test()
        self.table()
        self.regression()
        self.expectations()

    def card(self):
        card = chapter_card(3, r"One-way ANOVA", r"Splitting the variation, \ and Pythagoras again", lit=(1919,), part=PART)
        with self.voiceover("Chapter three. The analysis of variance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dotplot(self, d, center, x_length=6.2, y_length=4.4):
        y = np.asarray(d["y"])
        alloc = np.asarray(d["alloc"])
        A = axes([-0.6, 3.6], [46, 57], x_length=x_length, y_length=y_length, xlabel=r"", ylabel=r"yield", xticks=[], yticks=[48, 50, 52, 54, 56],
                 center=center)
        ax = A.ax
        dots = VGroup()
        for k in range(4):
            v = np.sort(y[alloc == k])
            for j, val in enumerate(v):
                dots.add(Dot(ax.c2p(k + (j - 2.5) * 0.07, val), radius=0.07, color=TRT[k]))
        names = VGroup(*[label(FERT[k], font_size=22, color=TRT[k]).move_to(ax.c2p(k, 46) + DOWN * 0.3) for k in range(4)])
        return A, ax, dots, names

    def trial(self):
        d = load("anova")
        y = np.asarray(d["y"])
        alloc = np.asarray(d["alloc"])
        fp = field_from(y, cell=0.62, center=[-3.8, 0.4, 0], lo=46, hi=57)
        tags = fp.tags(alloc, names="ONPK", colors=TRT, font_size=22)
        key = VGroup(*[label(rf"{c}: \ {n}", font_size=20, color=TRT[k]) for k, (c, n) in enumerate(zip("ONPK", FERT))]).arrange(RIGHT, buff=0.35)
        key.next_to(fp, DOWN, buff=0.35)
        A, ax, dots, names = self.dotplot(d, [3.3, 0.3, 0], x_length=5.6, y_length=4.2)
        means = d["anova"]["means"]
        bars = VGroup(*[Line(ax.c2p(k - 0.3, m), ax.c2p(k + 0.3, m), color=TRT[k], stroke_width=5) for k, m in enumerate(means)])
        gm = float(y.mean())
        gl = DashedLine(ax.c2p(-0.6, gm), ax.c2p(3.6, gm), color=GREY_B, stroke_width=2)
        foot = fit_rows(VGroup(
            label(r"four fertilizers, \ six plots each, \ placed by lot: \ a completely randomized design", font_size=24),
            label(r"is there any difference among the four? \ One question about four means", font_size=24, color=OBS),
        ), 12.4, 0.25, [0, -3.0, 0])
        tag = simulated_tag(r"the field-trial simulator", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Four fertilizers this time: none, nitrogen, phosphate, and the full mixture N P K. Twenty-four "
            "plots, six for each fertilizer, placed by lot. That's a completely randomized design. <bookmark mark='b'/> "
            "Lay the yields out by fertilizer. Their means differ: forty-nine point five with nothing, about fifty-three with "
            "nitrogen or the mixture. <bookmark mark='c'/> But the plots within each group differ too, by as much. Is there "
            "any real difference among the four fertilizers, or is this the soil? Notice the question is about four means at "
            "once. Six separate t-tests would be the wrong tool, as chapter four will show."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.02), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tags, lag_ratio=0.03), FadeIn(key), FadeIn(foot[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(names), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.04), run_time=2.0)
            self.play(Create(bars), Create(gl))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def decompose(self):
        d = load("anova")
        y = np.asarray(d["y"])
        alloc = np.asarray(d["alloc"])
        A, ax, dots, names = self.dotplot(d, [-2.6, 0.0, 0], x_length=7.0, y_length=4.8)
        means = d["anova"]["means"]
        gm = float(y.mean())
        gl = DashedLine(ax.c2p(-0.6, gm), ax.c2p(3.6, gm), color=GREY_B, stroke_width=2)
        bars = VGroup(*[Line(ax.c2p(k - 0.3, m), ax.c2p(k + 0.3, m), color=TRT[k], stroke_width=5) for k, m in enumerate(means)])
        between = VGroup(*[Arrow(ax.c2p(k + 0.36, gm), ax.c2p(k + 0.36, m), buff=0, color=OBS, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.25) for k, m in enumerate(means)])
        within = VGroup()
        for k in range(4):
            v = np.sort(y[alloc == k])
            for j, val in enumerate(v):
                x = k + (j - 2.5) * 0.07
                within.add(Line(ax.c2p(x, means[k]), ax.c2p(x, val), color=RES, stroke_width=2))
        rows = fit_rows(VGroup(
            MathTex(r"y_{ij} - \bar y", r"=", r"(\bar y_i - \bar y)", r"+", r"(y_{ij} - \bar y_i)", font_size=32),
            label(r"each plot's distance from the grand mean", font_size=22),
            label(r"= its fertilizer's distance \ (between groups)", font_size=22, color=OBS),
            label(r"+ its own distance from its group \ (within groups)", font_size=22, color=RES),
            MathTex(r"\sum_{ij}(\bar y_i - \bar y)(y_{ij} - \bar y_i) = 0", font_size=28),
            label(r"the cross term vanishes: \ within each group the residuals sum to zero", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, 0.0, 0])
        rows[0][2].set_color(OBS)
        rows[0][4].set_color(RES)
        with self.voiceover(
            "Fisher's idea was to split the variation itself. <bookmark mark='a'/> Each plot's distance from the grand mean "
            "is the sum of two pieces. <bookmark mark='b'/> First, its fertilizer's distance from the grand mean, the gold "
            "arrows: variation between groups. <bookmark mark='c'/> Second, the plot's own distance from its group's mean, the "
            "red lines: variation within groups, which can only be the soil and the noise. <bookmark mark='d'/> Square both "
            "sides and sum over all twenty-four plots, and the cross term vanishes, because within each group the residuals "
            "sum to zero. <bookmark mark='e'/> So the squares add. That's Pythagoras, and it means the right picture is "
            "geometric."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(dots), Create(gl), Create(bars))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in between], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Create(within, lag_ratio=0.03), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.clear_scene()

    def pythagoras(self):
        d = load("anova")
        a = d["anova"]
        ns = NSpace(scale=0.50, center=[-2.8, -0.5, 0], angle=-0.7, tilt=0.38, axis_len=5.6, axis_labels=[r"", r"", r""])
        u1 = np.array([1.0, 0.0, 0.0])
        u2 = np.array([0.0, 1.0, 0.0])
        pl = ns.plane(u1, u2, extent=5.0, color=OBS, opacity=0.14)
        sb, sw = np.sqrt(a["ssb"]), np.sqrt(a["ssw"])
        k = 4.6 / np.sqrt(a["sst"])
        yv = np.array([sb * 0.8, sb * 0.6, sw]) * k
        yh = np.array([sb * 0.8, sb * 0.6, 0]) * k
        vy = ns.vector(yv, color=DATA)
        vh = ns.vector(yh, color=OBS)
        res = ns.segment(yh, yv, color=RES, stroke_width=4)
        ra = ns.right_angle(yh, np.array([0, 0, 1.0]), -yh / np.linalg.norm(yh), size=0.45)
        rows = fit_rows(VGroup(
            label(r"the 24 deviations $y_{ij} - \bar y$: \ one vector in $\mathbb R^{24}$", font_size=22, color=DATA),
            label(r"the group means' part lies in a 3-dimensional subspace", font_size=22, color=OBS),
            label(r"the residuals are perpendicular to it, \ in the other 20 dimensions", font_size=22, color=RES),
            MathTex(rf"\underbrace{{{a['sst']:.1f}}}_{{\text{{SST}}}} = \underbrace{{{a['ssb']:.1f}}}_{{\text{{SSB}}}} + "
                    rf"\underbrace{{{a['ssw']:.1f}}}_{{\text{{SSW}}}}", font_size=32),
            MathTex(r"23 = 3 + 20\ \ \text{degrees of freedom}", font_size=28, color=GREY_A),
        ), 5.4, 0.34, [3.9, 0.1, 0])
        intro = label('Orthogonal projections split the sum of squares', font_size=32).move_to([0, 2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Write the twenty-four deviations from the grand mean as one vector, in twenty-four-dimensional "
            "space; we can only draw three of the dimensions. <bookmark mark='b'/> The between-groups part, the group means "
            "repeated six times each, lives in a subspace with only three dimensions, four group means minus one for the grand "
            "mean. It's a projection of the data, exactly as in Part 12. <bookmark mark='c'/> The within-groups residuals are "
            "perpendicular to it, in the other twenty dimensions. <bookmark mark='d'/> So the total sum of squares, one hundred "
            "and seven point eight, is the between sum of squares, forty-six point six, plus the within sum of squares, "
            "sixty-one point two. <bookmark mark='e'/> And the dimensions add the same way: twenty-three degrees of freedom "
            "are three between plus twenty within. That's the orthogonal geometry behind Cochran's theorem. Normal errors also give the independent chi-squared laws."
        ) as vo:
            self.add(ns)
            self.play(FadeIn(ns.axes3), FadeIn(intro))
            vo.wait_until("a")
            self.add(vy)
            self.play(NSpace.reveal(vy), FadeIn(rows[0]), FadeOut(intro))
            vo.wait_until("b")
            self.add(pl, vh)
            self.play(NSpace.reveal(pl, vh), FadeIn(rows[1]))
            vo.wait_until("c")
            self.add(res, ra)
            self.play(NSpace.reveal(res, ra), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            self.play(ns.turn(0.9, run_time=4.0))
            for m_ in (pl, vy, vh, res, ra):
                m_.clear_updaters()
        self.clear_scene()

    def f_test(self):
        d = load("anova")
        a = d["anova"]
        A = axes([0, 8], [0, 0.75], x_length=6.4, y_length=3.8, xlabel=r"$F$", ylabel=r"density", xticks=[0, 2, 4, 6, 8],
                 yticks=[0, 0.25, 0.5, 0.75], center=[-3.0, -0.5, 0])
        ax = A.ax
        fx, fp = np.asarray(d["f_x"]), np.asarray(d["f_pdf"])
        keep = fx <= 8
        cv = curve(ax, fx[keep], fp[keep], NULLC, 3)
        tail = fx[keep] >= a["F"]
        sh = shade(ax, fx[keep][tail], fp[keep][tail], OBS, 0.6)
        mk = DashedLine(ax.c2p(a["F"], 0), ax.c2p(a["F"], 0.5), color=OBS, stroke_width=3)
        ml = label(rf"$F = {a['F']:.2f}$", font_size=22, color=OBS).next_to(mk, UP, buff=0.08)
        rows = [
            cmath(r"\text{MSB}", r"=", rf"\frac{{\text{{SSB}}}}{{k - 1}} = \frac{{{a['ssb']:.1f}}}{{3}} = {a['ssb'] / 3:.2f}", font_size=30),
            cmath(r"\text{MSW}", r"=", rf"\frac{{\text{{SSW}}}}{{N - k}} = \frac{{{a['ssw']:.1f}}}{{20}} = {a['mse']:.2f}", font_size=30),
            cmath(r"F", r"=", rf"\frac{{\text{{MSB}}}}{{\text{{MSW}}}} = {a['F']:.2f}", font_size=32),
            cmath(r"H_0", r":", rf"F \sim F_{{3,20}},\quad p = {a['p']:.4f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"between: \ per degree of freedom"), why(r"within: \ the pure error, \ $\hat\sigma^2$"),
                why(r"signal-to-noise"), why(r"Part 8's $F$ distribution")]
        with self.voiceover(
            "Now the normal-theory test: assume independent Gaussian errors with the same variance in all groups. <bookmark mark='a'/> Divide each sum of squares by its degrees of freedom. The between mean square "
            "is forty-six point six over three, fifteen point five. <bookmark mark='b'/> The within mean square, sixty-one "
            "point two over twenty, three point oh six, is the pure error: an estimate of sigma squared, whatever the "
            "fertilizers do. <bookmark mark='c'/> Their ratio, F, is five point oh seven. <bookmark mark='d'/> If the fertilizers "
            "made no difference, the between mean square would also estimate sigma squared, and the ratio would follow Part "
            "8's F distribution with three and twenty degrees of freedom, shown here. An F of five or more happens less than "
            "one time in a hundred: p is point zero zero nine. Fisher named the distribution's ancestor, z; Snedecor named it F, "
            "for Fisher."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            step = ladder(self, rows, whys, keep=4, top=2.4, x=3.2, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 3:
                    self.play(FadeIn(sh), Create(mk), FadeIn(ml))
        self.clear_scene()

    def table(self):
        d = load("anova")
        a = d["anova"]
        tab = table_rows([
            [r"source", r"df", r"sum of squares", r"mean square", r"$F$", r"$p$"],
            [r"fertilizer", r"3", rf"{a['ssb']:.1f}", rf"{a['ssb'] / 3:.2f}", rf"{a['F']:.2f}", rf"{a['p']:.4f}"],
            [r"residual", r"20", rf"{a['ssw']:.1f}", rf"{a['mse']:.2f}", r"", r""],
            [r"total", r"23", rf"{a['sst']:.1f}", r"", r"", r""],
        ], font_size=28, col_buff=0.7, row_buff=0.3, colors=[GREY_B, OBS, RES, DATA]).move_to([0, 1.0, 0])
        line = Line(tab[0].get_corner(DL) + DOWN * 0.12 + LEFT * 0.2, tab[0].get_corner(DR) + DOWN * 0.12 + RIGHT * 0.2, color=GREY_D)
        hc = history_card(1923, r"R. A. Fisher \ and \ W. A. Mackenzie, \ \emph{Studies in Crop Variation II}",
                          r"the manuring of potato varieties: \ the first published analysis-of-variance table", color=OBS, width=9.0,
                          font_size=22).move_to([0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The whole calculation fits in a table, one row per source of variation: degrees of freedom, "
            "sums of squares, mean squares, and F. The total row is the sum of the rows above it, in both the degrees of "
            "freedom and the sums of squares. <bookmark mark='b'/> The first published table of this kind appeared in 1923, in "
            "Fisher and Mackenzie's study of potatoes grown with different manures. Within a decade agricultural stations "
            "around the world were printing them, and the analysis of variance table is still the standard summary of an "
            "experiment."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), Create(line))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def regression(self):
        d = load("anova")
        a = d["anova"]
        c = d["coef"]
        rows = [
            cmath(r"y", r"=", r"\beta_0 + \beta_N\,d_N + \beta_P\,d_P + \beta_{NPK}\,d_{NPK} + \varepsilon", font_size=32),
            cmath(r"\hat\beta", r"=", rf"({c[0]:.2f},\ {c[1]:.2f},\ {c[2]:.2f},\ {c[3]:.2f})", font_size=32),
            cmath(r"R^2", r"=", rf"\frac{{\text{{SSB}}}}{{\text{{SST}}}} = {d['r2']:.3f}", font_size=32),
            cmath(r"F_{\text{nested}}", r"=", rf"\frac{{(\text{{RSS}}_0 - \text{{RSS}})/3}}{{\text{{RSS}}/20}} = {a['F']:.2f}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"dummy variables: \ ``none'' is the baseline"), why(r"the control mean, \ then each fertilizer's gain"),
                why(r"the share of variation the fertilizers explain"), why(r"Part 12's nested $F$-test: \ the same number")]
        intro = label('ANOVA is a nested linear-model comparison', font_size=36)
        with self.voiceover(
            "The analysis of variance is also a regression. <bookmark mark='a'/> Code each fertilizer with a dummy variable, "
            "leaving none as the baseline, and regress the yields on the dummies. <bookmark mark='b'/> The intercept is the "
            "unfertilized mean, forty-nine point four five, and each coefficient is a fertilizer's gain over nothing: three "
            "point two for nitrogen, one point nine for phosphate, three point five for the mixture. <bookmark mark='c'/> R "
            "squared is the between sum of squares over the total: point four three two. <bookmark mark='d'/> And Part 12's "
            "nested F-test, comparing this model with the intercept alone, gives exactly the same five point oh seven. ANOVA "
            "and regression are one linear model, seen from two sides. Fisher's tables became regression software."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def expectations(self):
        rows = [
            cmath(r"y_{ij}", r"=", r"\mu + \alpha_i + \varepsilon_{ij},\qquad \textstyle\sum_i \alpha_i = 0", font_size=32),
            cmath(r"\mathbb E[\text{MSW}]", r"=", r"\sigma^2", font_size=34),
            cmath(r"\mathbb E[\text{MSB}]", r"=", r"\sigma^2 + \frac{n}{k - 1}\sum_i \alpha_i^2", font_size=34),
            cmath(r"\mathbb E[F]", r"=", r"\frac{\nu}{\nu-2}\left(1 + \frac{n\sum_i\alpha_i^2}{(k-1)\,\sigma^2}\right),\quad\nu=N-k>2", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the effects model: \ $k$ groups of $n$"), why(r"always: \ the yardstick"),
                why(r"inflated by real differences, \ and only by them"), why(r"the noncentrality: \ power, \ chapter 12")]
        intro = label('What the mean squares estimate', font_size=36)
        with self.voiceover(
            "Why does the ratio work? <bookmark mark='a'/> Write the balanced model with independent mean-zero, equal-variance errors as a grand mean, plus a fertilizer effect alpha "
            "summing to zero, plus noise. <bookmark mark='b'/> The within mean square always estimates sigma squared, "
            "whatever the effects. <bookmark mark='c'/> The between mean square estimates sigma squared plus n over k minus "
            "one times the sum of the squared effects: inflated by real differences, and by nothing else. <bookmark mark='d'/> "
            "Under Gaussian errors, the mean of F includes the denominator correction, nu over nu minus two. It approaches one under the null as error degrees of freedom grow, and increases with the effects relative to the noise. That "
            "growth, the noncentrality, is what determines an experiment's power, the subject of chapter twelve."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
