from __future__ import annotations

import numpy as np

from videos.stats.stats23.common import *  # noqa: F403


class GLH(VoiceoverScene):
    def construct(self):
        self.card()
        self.hypothesis()
        self.derive()
        self.cochran()
        self.r2form()
        self.families()
        self.null_hist()
        self.ellipse()
        self.scheffe()

    def card(self):
        card = chapter_card(2, r"The general linear hypothesis", r"One test for every linear question", part=PART)
        with self.voiceover("Chapter two. The general linear hypothesis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def hypothesis(self):
        rows = [
            cmath(r"H_0", r":", r"C\beta = d, \ \ C \ \text{is } q \times p", font_size=30),
            cmath(r"\beta_j = 0", r":", r"C = e_j^\top, \ d = 0, \ q = 1", font_size=30),
            cmath(r"\beta_1 = \beta_2", r":", r"C = (0, 1, -1), \ d = 0", font_size=30),
            cmath(r"\beta_1 = \beta_2 = 0", r":", r"C = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}, \ q = 2", font_size=30),
        ]
        rows[0][2].set_color(OLS_C)
        whys = [why(r"$q$ linear restrictions at once"), why(r"the $t$-test"), why(r"a contrast"), why(r"a joint test")]
        intro = label('Test linear restrictions with a full-rank design', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Almost every question asked of a linear model is a set of linear restrictions: C "
            "beta equals d, with q linearly independent rows, one per restriction, and a full-rank design with more "
            "observations than coefficients. <bookmark mark='b'/> A single coefficient being zero is one row. "
            "<bookmark mark='c'/> Two coefficients being equal is a contrast. <bookmark mark='d'/> Several "
            "coefficients all being zero at once is a joint hypothesis with two or more rows. One test handles them "
            "all."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"C\hat\beta - d", r"\sim", r"N\big(C\beta - d, \ \sigma^2 C (X^\top X)^{-1} C^\top\big)", font_size=30),
            cmath(r"Q", r"=", r"(C\hat\beta - d)^\top \big[C (X^\top X)^{-1} C^\top\big]^{-1} (C\hat\beta - d)", font_size=28),
            cmath(r"Q / \sigma^2", r"\sim", r"\chi^2_q \ \text{under } H_0, \ \ \text{independent of } s^2", font_size=30),
            cmath(r"F", r"=", r"\dfrac{Q / q}{s^2} \sim F_{q,\, n - p}", font_size=32),
        ]
        rows[3][2].set_color(OLS_C)
        whys = [why(r"Gaussian errors, \ covariance $\sigma^2 I$"), why(r"the squared distance, \ in its own metric"),
                why(r"Part 4: \ a quadratic form in normals"), why(r"replace $\sigma^2$ by $s^2$: \ Fisher's $F$")]
        intro = label('Exact F inference assumes Gaussian errors with covariance sigma squared I', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> With errors jointly normal with conditional covariance sigma squared times the "
            "identity, C beta hat minus d is normal, centred at zero under the hypothesis, with covariance sigma "
            "squared C X transpose X inverse C transpose. <bookmark mark='b'/> Measure how far it is from zero in its"
            " own metric: the quadratic form Q, the squared length after the covariance has been undone. <bookmark "
            "mark='c'/> Divided by sigma squared it is chi-squared with q degrees of freedom, and, because it depends"
            " on the fit and not the residuals, independent of the residual variance s squared. <bookmark mark='d'/> "
            "Replace sigma squared by s squared and divide by q: an F statistic with q and n minus p degrees of "
            "freedom."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cochran(self):
        rows = [
            cmath(r"\|y - \bar y\|^2", r"=", r"\|\hat y_0 - \bar y\|^2 + \|\hat y - \hat y_0\|^2 + \|y - \hat y\|^2", font_size=28),
            cmath(r"\mathrm{RSS}_0 - \mathrm{RSS}", r"=", r"Q", font_size=30),
            cmath(r"F", r"=", r"\dfrac{(\mathrm{RSS}_0 - \mathrm{RSS})/q}{\mathrm{RSS}/(n - p)}", font_size=30),
            cmath(r"\text{Cochran}", r":", r"\text{orthogonal pieces} \Rightarrow \text{independent } \chi^2\text{s}", font_size=30),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"homogeneous nested models with intercepts"), why(r"the extra residual the restriction costs"),
                why(r"the same $F$, \ as two fits"), why(r"Part 4's theorem, \ now used in full")]
        intro = label('Nested-model geometry gives the extra residual sum of squares', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "There's a second way to see the same statistic. <bookmark mark='a'/> Fit the model with the restriction "
            "imposed and without it. For homogeneous restrictions and nested models containing the intercept, these "
            "are projections onto nested linear spaces, giving the displayed Pythagorean decomposition. <bookmark "
            "mark='b'/> For general affine restrictions too, the extra residual sum of squares is exactly Q, though "
            "the first centered decomposition need not apply. <bookmark mark='c'/> So F compares two fits: how much "
            "worse the restricted model does, per restriction, against the noise level. <bookmark mark='d'/> "
            "Cochran's theorem from Part 4 says orthogonal pieces of a normal vector have independent chi-squared "
            "lengths, which is what makes the ratio an F."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def r2form(self):
        rows = [
            cmath(r"F", r"=", r"\dfrac{(R^2 - R_0^2)/q}{(1 - R^2)/(n - p)}", font_size=32),
            cmath(r"\text{all slopes } = 0", r":", r"\text{the overall } F \text{ printed under every regression}", font_size=28),
            cmath(r"q = 1", r":", r"F = t^2", font_size=30),
            cmath(r"\text{large } n", r":", r"qF \to \chi^2_q: \ \text{the Wald test of Part 22}", font_size=30),
        ]
        rows[0][2].set_color(OLS_C)
        whys = [why(r"the same ratio, \ in $R^2$"), why(r"$R_0^2 = 0$"), why(r"one restriction: \ the square of a $t$"),
                why(r"regularity and correct covariance still needed")]
        intro = label('The same nested-model test in R squared', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For nested models with a common intercept and the same response, divide the "
            "residual sums by the total sum of squares and the same statistic reads in R squared: the gain in R "
            "squared per restriction, against the unexplained share per residual degree of freedom. <bookmark "
            "mark='b'/> Testing all the slopes at once gives the overall F that every regression printout shows. "
            "<bookmark mark='c'/> With a single restriction, F is the square of the familiar t. <bookmark mark='d'/> "
            "And in large samples q times F becomes chi-squared: it is Part 22's Wald test, under moment, design and "
            "homoskedasticity conditions. With uneven variances use a robust Wald covariance instead."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def families(self):
        d = load("glh")
        b, se = d["coef"], d["se"]
        hdr = [r"\textbf{hypothesis}", r"$q$", r"$F$", r"$p$"]
        body = [[r"$\beta_{\mathrm{father}} = \beta_{\mathrm{mother}}$", "1", f"{d['eq']['F']:.3f}", f"{d['eq']['p']:.2f}"],
                [r"both $= 0.35$", "2", f"{d['joint']['F']:.3f}", f"{d['joint']['p']:.2f}"],
                [r"both $= 0$", "2", f"{d['zero']['F']:.1f}", f"{d['zero']['p']:.2e}"]]
        t = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_A, HIT, HIT, RES])
        t.move_to([0, -0.4, 0])
        top = fit_rows(VGroup(
            label(rf"{d['n']} of the World's families, \ standardized heights", font_size=24),
            label(rf"child $= {b[0]:.3f} + {b[1]:.3f}\,$father$ + {b[2]:.3f}\,$mother", font_size=24, color=OLS_C),
            label(rf"SEs {se[1]:.3f} and {se[2]:.3f}; \ the World's truth: \ 0.35 each", font_size=22, color=GREY_A),
        ), 12.0, 0.28, [0, 2.3, 0])
        foot = label(rf"as two fits: \ RSS$_0$ $-$ RSS gives $F = {d['F_rss']:.3f}$, \ the same number", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Four hundred families from the World, heights standardized. Regress each adult child on "
            "father and mother. <bookmark mark='b'/> The coefficients are point three three and point three four; the "
            "World was built with point three five for each. <bookmark mark='c'/> Do fathers and mothers count equally? "
            "F is point oh eight, p point seven eight: no evidence otherwise. <bookmark mark='d'/> Are both exactly point "
            "three five? A two-row test, p point eight five. <bookmark mark='e'/> Do parents matter at all? F is sixty-two. "
            "<bookmark mark='f'/> And the first test done as two fits, with and without the restriction, gives the same F "
            "to every digit."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(top[0]))
            vo.wait_until("b")
            self.play(FadeIn(top[1]), FadeIn(top[2]), FadeIn(t[0]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(t[k + 1]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def null_hist(self):
        from scipy import stats as st
        d = load("glh_null")
        F = np.asarray(d["F"])
        edges = np.linspace(0, 8, 33)
        counts, _ = np.histogram(F, edges)
        h = counts / (len(F) * np.diff(edges))
        A = axes([0, 8], [0, 1.6], x_length=8.0, y_length=4.2, xlabel=r"$F$ for equal parents, \ 2,000 samples",
                 ylabel=r"density", xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1, 1.5], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=OLS_C, opacity=0.6)
        gr = np.linspace(0.05, 8, 200)
        dens = curve(ax, gr, st.f.pdf(gr, 1, 397), TRUE, 3)
        crit = DashedLine(ax.c2p(d["crit"], 0), ax.c2p(d["crit"], 1.4), color=RES, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"2,000 Gaussian responses; \ fixed family design", font_size=22),
            label(r"equal-parent null; \ iid Gaussian errors", font_size=22, color=GREY_A),
            label(r"gold: \ the $F_{1, 397}$ density", font_size=22, color=TRUE),
            label(rf"red: \ the 5\% cut, \ {d['crit']:.2f}", font_size=22, color=RES),
            label(rf"rejected: \ {100 * d['reject']:.1f}\%", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Is the F distribution really right? Keep the predictor design of four hundred World"
            " families fixed, draw two thousand fresh Gaussian response vectors under equal-parent coefficients, and "
            "compute F each time. <bookmark mark='b'/> This conditional Gaussian experiment imposes the null exactly;"
            " resampling the finite World would not provide this exact reference model. <bookmark mark='c'/> The "
            "histogram follows the F density with one and three hundred and ninety-seven degrees of freedom. "
            "<bookmark mark='d'/> Its ninety-fifth percentile is three point eight six. <bookmark mark='e'/> The test"
            " rejects five point three percent of the time, within simulation error of five."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(dens), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(crit), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def scheffe(self):
        rows = [
            cmath(r"\text{one contrast } c", r":", r"c^\top\hat\beta \pm t_{n-p}\, s\sqrt{c^\top (X^\top X)^{-1} c}", font_size=30),
            cmath(r"c\in\mathcal C,\ \dim\mathcal C=q", r":", r"c^\top\hat\beta \pm \sqrt{q F_{q, n-p}}\, s\sqrt{c^\top (X^\top X)^{-1} c}", font_size=28),
            cmath(r"\text{why}", r":", r"\max_{c\in\mathcal C} \dfrac{(c^\top(\hat\beta - \beta))^2}{s^2 c^\top (X^\top X)^{-1} c} = q F", font_size=30),
            cmath(r"q = 2, \ n = 400", r":", r"1.97 \to 2.45", font_size=30),
        ]
        rows[1][2].set_color(OLS_C)
        whys = [why(r"chapter two's $t$-interval"), why(r"Scheff\'e (1953)"), why(r"Cauchy--Schwarz: \ the ellipse's shadows"),
                why(r"the price of looking at every contrast")]
        intro = label('Simultaneous contrasts within a specified coefficient subspace', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The ellipse also answers a harder question. One pre-planned contrast gets the usual"
            " t interval. <bookmark mark='b'/> But if you will look at every contrast within a specified "
            "q-dimensional coefficient subspace and report the interesting ones, Henry Scheffé's 1953 intervals "
            "replace t by the square root of q times the F quantile, and then all of them hold together with "
            "ninety-five percent confidence. <bookmark mark='c'/> The reason is Cauchy–Schwarz: the largest squared t"
            " over contrasts in that subspace is exactly q times its F statistic, the projection of the ellipse onto "
            "every direction. <bookmark mark='d'/> With two coefficients and four hundred families, the multiplier "
            "grows from one point nine seven to two point four five: the price of fishing, paid in advance. Part 33 "
            "returns to it."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ellipse(self):
        d = load("glh")
        e = np.asarray(d["ellipse"])
        A = axes([0.1, 0.6], [0.1, 0.6], x_length=5.4, y_length=5.4, xlabel=r"$\beta_{\mathrm{father}}$",
                 ylabel=r"$\beta_{\mathrm{mother}}$", xticks=[0.2, 0.3, 0.4, 0.5], yticks=[0.2, 0.3, 0.4, 0.5], center=[-2.8, 0.0, 0])
        ax = A.ax
        el = Polygon(*[ax.c2p(a, b) for a, b in e.T], color=OLS_C, stroke_width=3, fill_color=OLS_C, fill_opacity=0.2)
        diag = DashedLine(ax.c2p(0.1, 0.1), ax.c2p(0.6, 0.6), color=GREY_B, stroke_width=2)
        hat = Dot(ax.c2p(*d["coef"][1:]), radius=0.08, color=OLS_C)
        tru = Dot(ax.c2p(0.35, 0.35), radius=0.08, color=TRUE)
        rows = fit_rows(VGroup(
            label(r"blue: \ the 95\% joint confidence ellipse", font_size=22, color=OLS_C),
            label(r"$\{\beta: F(\beta) \le F_{2, n-p, 0.95}\}$", font_size=22),
            label(r"dashed: \ $\beta_f = \beta_m$, \ which it crosses", font_size=22, color=GREY_B),
            label(r"gold: \ the truth, \ inside", font_size=22, color=TRUE),
            label(r"the origin: \ far outside", font_size=22, color=RES),
        ), 4.6, 0.42, [3.9, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Inverting the joint test gives a confidence region: every pair of coefficients the F-test "
            "would not reject. <bookmark mark='b'/> It's an ellipse, its shape set by the covariance of the two estimates. "
            "<bookmark mark='c'/> The line of equal coefficients passes through it, so equality isn't rejected. "
            "<bookmark mark='d'/> The World's true pair is inside. <bookmark mark='e'/> And the origin, no effect of either "
            "parent, is far off the chart."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), FadeIn(hat))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(el), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(diag), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(tru), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
