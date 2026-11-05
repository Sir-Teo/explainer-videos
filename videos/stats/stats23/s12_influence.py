from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403


class Influence(VoiceoverScene):
    def construct(self):
        self.card()
        self.deletion()
        self.leverage()
        self.bars()
        self.jackknife()
        self.masking()
        self.advice()

    def card(self):
        card = chapter_card(11, r"Influence", r"Which points move the answer?", part=PART)
        with self.voiceover("Chapter eleven. Influence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def deletion(self):
        rows = [
            cmath(r"\hat\beta - \hat\beta_{(i)}", r"=", r"\dfrac{(X^\top X)^{-1} x_i\, e_i}{1 - h_{ii}}", font_size=30),
            cmath(r"\text{DFBETAS}_{ij}", r"=", r"\dfrac{\hat\beta_j - \hat\beta_{(i)j}}{s_{(i)} \sqrt{(X^\top X)^{-1}_{jj}}}", font_size=30),
            cmath(r"\text{Cook's } D_i", r"=", r"\dfrac{r_i^2}{p}\, \dfrac{h_{ii}}{1 - h_{ii}}", font_size=30),
            cmath(r"\text{flag}", r":", r"|\text{DFBETAS}| > 2/\sqrt n", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"leave one out, \ without refitting: \ Sherman--Morrison"), why(r"in SEs: \ Belsley, \ Kuh \& Welsch (1980)"),
                why(r"Part 12: \ residual times leverage"), why(r"a size-adjusted rule of thumb")]
        with self.voiceover(
            "<bookmark mark='a'/> How much does one observation matter? Deleting it changes the coefficients by a formula "
            "that needs no refit: X transpose X inverse times x i, times its residual, divided by one minus its leverage. "
            "It follows from the Sherman–Morrison identity for updating an inverse. <bookmark mark='b'/> Scaled by the "
            "coefficient's standard error, that's DFBETAS. <bookmark mark='c'/> Part 12's Cook's distance summarizes the "
            "change in all the coefficients at once: large residual times large leverage. <bookmark mark='d'/> A common flag "
            "for DFBETAS is two over root n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def leverage(self):
        rows = [
            cmath(r"h_{ii}", r"=", r"x_i^\top (X^\top X)^{-1} x_i", font_size=30),
            cmath(r"", r"=", r"\tfrac1n + \tfrac{1}{n - 1}\, D_i^2", font_size=30),
            cmath(r"\textstyle\sum_i h_{ii}", r"=", r"p, \ \ \text{average } p/n", font_size=30),
            cmath(r"\mathrm{Var}(e_i)", r"=", r"(1 - h_{ii})\sigma^2", font_size=30),
        ]
        rows[1][-1].set_color(PATH)
        whys = [why(r"the diagonal of the hat matrix"), why(r"$D_i$: \ Mahalanobis distance from the centre of $x$"),
                why(r"the trace of a projection"), why(r"chapter four, \ again")]
        with self.voiceover(
            "<bookmark mark='a'/> First, leverage, the diagonal of the hat matrix. <bookmark mark='b'/> With an intercept it "
            "is one over n plus the squared Mahalanobis distance of x i from the centre of the predictors, scaled by n minus "
            "one: leverage is distance in x, measured in the predictors' own covariance. <bookmark mark='c'/> The leverages "
            "add up to p, the trace of a projection, so their average is p over n. <bookmark mark='d'/> And a residual's "
            "variance is one minus its leverage times sigma squared, which is why chapter four's small-sample corrections "
            "divide by it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bars(self):
        d = load("influence")
        e = load("eiv")
        dfb = np.asarray(d["dfbetas"])
        dist = np.asarray(e["d"])
        n = len(dfb)
        A = axes([0.3, n + 0.7], [-0.9, 0.9], x_length=8.4, y_length=4.2, xlabel=r"nebula, \ in order of distance",
                 ylabel=r"DFBETAS for the slope", xticks=[], yticks=[-0.8, -0.4, 0, 0.4, 0.8], center=[-1.4, 0.4, 0])
        ax = A.ax
        cut = VGroup(*[DashedLine(ax.c2p(0.3, s * d["cut"]), ax.c2p(n + 0.7, s * d["cut"]), color=RES, stroke_width=2) for s in (1, -1)])
        bars = VGroup()
        for i, v in enumerate(dfb):
            col = RES if abs(v) > d["cut"] else OLS_C
            h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            bars.add(Rectangle(width=0.22, height=max(h, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85)
                     .move_to(ax.c2p(i + 1, 0), aligned_edge=DOWN if v > 0 else UP))
        k = d["most"]
        rows = fit_rows(VGroup(
            label(r"Hubble's 24 nebulae", font_size=22),
            label(rf"dashed: \ $\pm 2/\sqrt{{24}} = \pm {d['cut']:.2f}$", font_size=22, color=RES),
            label(rf"most influential: \ {dist[k]:.1f} Mpc, \ {e['v'][k]:.0f} km/s", font_size=22, color=RES),
            label(rf"slope {d['slope']:.0f} $\to$ {d['slope_without']:.0f} without it", font_size=22, color=PATH),
            label(r"the ends have the leverage", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.2, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Hubble's nebulae, in order of distance, with each one's DFBETAS for the slope. "
            "<bookmark mark='b'/> The dashed lines are the two over root twenty-four flag. <bookmark mark='c'/> The most "
            "influential is a nebula at two megaparsecs moving at only five hundred kilometres per second, at the far edge "
            "of the data with a large negative residual. <bookmark mark='d'/> Remove it and the slope rises from four "
            "hundred and fifty-four to five hundred and four. <bookmark mark='e'/> The points at either end have the leverage: the "
            "slow far one, and the two nearest, which recede surprisingly fast, both hold the slope down. Influence isn't a reason to delete a point; it's a reason to check it."
        ) as vo:
            self.add(hubble_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v > 0 else UP) for b, v in zip(bars, dfb)], lag_ratio=0.04), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(bars[k], color=PATH), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def jackknife(self):
        d = load("influence")
        rows = [
            cmath(r"\hat\beta_{(i)}", r":", r"\text{all } n \text{ leave-one-out fits, \ from one fit}", font_size=30),
            cmath(r"\widehat{\mathrm{Var}}_{\mathrm{jack}}", r"=", r"\tfrac{n - 1}{n} \textstyle\sum_i (\hat\beta_{(i)} - \bar\beta_{(\cdot)})(\cdot)^\top", font_size=30),
            cmath(r"\text{Hubble's slope}", r":", rf"\text{{SE}}: \ {d['se'][1]:.1f} \ \text{{(classical)}}, \ {d['jack_se'][1]:.1f} \ \text{{(jackknife)}}, \ {d['se_hc3'][1]:.1f} \ \text{{(HC3)}}", font_size=28),
            cmath(r"\text{HC3}", r"\approx", r"\text{the jackknife, \ up to } (n - 1)/n", font_size=30),
        ]
        rows[2][2].set_color(OLS_C)
        whys = [why(r"the deletion formula"), why(r"Part 16's jackknife (Quenouille, \ Tukey)"),
                why(r"both robust SEs a little above the classical"), why(r"chapter four's best formula is a jackknife")]
        with self.voiceover(
            "<bookmark mark='a'/> The deletion formula gives every leave-one-out fit from a single fit. <bookmark mark='b'/> "
            "Their spread is Part 16's jackknife variance. <bookmark mark='c'/> For Hubble's slope the classical standard "
            "error is seventy-five, the jackknife's eighty-one, and HC three's eighty-two. <bookmark mark='d'/> That's no "
            "coincidence: HC three is the jackknife variance, up to a factor of n minus one over n and the centring. "
            "Chapter four's best formula and Part 16's resampling turn out to be one idea."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def masking(self):
        d = load("masking")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([0, 16], [-1, 9], x_length=8.0, y_length=4.4, xlabel=r"$x$", ylabel=r"$y$", xticks=[0, 4, 8, 12, 16],
                 yticks=[0, 4, 8], center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=GREY_A if i < 20 else RES) for i, (a, b) in enumerate(zip(x, y))])

        def line(c, col):
            return Line(ax.c2p(0, c[0]), ax.c2p(16, c[0] + 16 * c[1]), color=col, stroke_width=3.5)

        all_ = line(d["coef"], OLS_C)
        one = line(d["coef_drop1"], PATH)
        clean = line(d["coef_clean"], GLS_C)
        rows = fit_rows(VGroup(
            label(r"20 ordinary points; \ 3 outliers together", font_size=22),
            label(rf"blue: \ all 23: \ slope ${d['coef'][1]:.2f}$", font_size=22, color=OLS_C),
            label(rf"amber: \ drop one outlier: \ ${d['coef_drop1'][1]:.2f}$", font_size=22, color=PATH),
            label(rf"teal: \ drop all three: \ ${d['coef_clean'][1]:.2f}$", font_size=22, color=GLS_C),
            label(rf"Cook's $D$: \ {d['cooks'][-3]:.2f}, {d['cooks'][-2]:.2f}, {d['cooks'][-1]:.2f}; \ all below 1", font_size=22, color=RES),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Leave-one-out has a blind spot. Twenty ordinary points and three outliers sitting together "
            "far to the right. <bookmark mark='b'/> With all twenty-three, the slope is flat. <bookmark mark='c'/> Delete "
            "one outlier and the other two hold the line almost where it was: the slope barely moves. <bookmark mark='d'/> "
            "Delete all three and it jumps to point four six. <bookmark mark='e'/> Each outlier's Cook's distance is below the "
            "usual cut-off of one, because each is masked by its neighbours. Groups of points need group diagnostics, or "
            "robust fits that don't let any group take over."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(all_), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(one), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(clean), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"leverage: \ unusual $x$; \ residual: \ unusual $y$; \ influence: \ both", font_size=24, color=PATH),
            label(r"check influential points; \ refit without them; \ report both", font_size=24),
            label(r"robust regression downweights them automatically: \ Part 30", font_size=24, color=TEAL),
            label(r"influence functions, \ for any estimator: \ Parts 30 and 49", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Leverage is an unusual x; a large residual is an unusual y; influence needs both. "
            "<bookmark mark='b'/> Look at the influential points, refit without them, and if the conclusion changes, say so. "
            "<bookmark mark='c'/> Robust regression, in Part 30, downweights such points automatically. <bookmark mark='d'/> "
            "And the deletion change, scaled up by n, is a first look at the influence function, which Parts 30 and 49 build "
            "into a theory of every estimator."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
