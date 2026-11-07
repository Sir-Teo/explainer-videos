from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class GAM(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.backfitting()
        self.concurvity()
        self.ozone()
        self.verdict()
        self.extensions()

    def card(self):
        card = chapter_card(10, r"Additive models", r"Many variables, \ one dimension at a time", lit=(1990,), part=PART)
        with self.voiceover("Chapter ten. Additive models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"E(Y \mid x)", r"=", r"\alpha + f_1(x_1) + \dots + f_p(x_p)", font_size=32),
            cmath(r"\text{each } f_j", r":", r"\text{a smooth curve, \ mean zero}", font_size=30),
            cmath(r"\text{rate}", r":", r"n^{-4/5} \text{ per component, fixed }p \text{ and regular design}", font_size=32),
            cmath(r"\text{GAM}", r":", r"g(E\,Y) = \alpha + \textstyle\sum_j f_j(x_j)", font_size=30),
        ]
        rows[2][2].set_color(SPLC)
        whys = [why(r"no interactions"), why(r"identifiable up to the constant"), why(r"Stone (1985): \ fixed $p$, smoothness and design conditions"),
                why(r"Hastie \& Tibshirani (1990): \ Part 24's links")]
        with self.voiceover(
            "<bookmark mark='a'/> Chapter four's escape, made concrete. Assume the regression function is a sum of "
            "smooth curves, one per variable, with no interactions. <bookmark mark='b'/> Centering separates the "
            "intercept; identifying individual curves also requires a design without exact concurvity. <bookmark "
            "mark='c'/> Charles Stone proved in 1985 that for a fixed number of twice-smooth additive components "
            "under suitable design conditions, each has the one-dimensional squared-error rate. The claim is not "
            "uniform as the number of predictors grows. <bookmark mark='d'/> Trevor Hastie and Robert Tibshirani "
            "added Part 24's link functions: the generalized additive model."
        ) as vo:
            intro=label('Additivity replaces one high-dimensional surface by component curves',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def backfitting(self):
        rows = [
            cmath(r"r_j", r"=", r"y - \hat\alpha - \textstyle\sum_{k \ne j} \hat f_k(x_k)", font_size=30),
            cmath(r"\hat f_j", r"\leftarrow", r"S_j\, r_j, \ \text{then centre}", font_size=32),
            cmath(r"\text{repeat}", r":", r"\text{cycle over } j \text{ until nothing moves}", font_size=30),
            cmath(r"\text{converges}", r":", r"\text{Gauss--Seidel for } (I + \text{coupled } S_j)\, f = S y", font_size=28),
        ]
        rows[1][2].set_color(SPLC)
        whys = [why(r"the partial residual for variable $j$"), why(r"smooth it against $x_j$ alone"),
                why(r"Friedman \& Stuetzle (1981)"), why(r"Buja, Hastie \& Tibshirani (1989)")]
        with self.voiceover(
            "<bookmark mark='a'/> The fitting algorithm is simple. For variable j, form the partial residual: the "
            "response minus every other curve. <bookmark mark='b'/> Smooth it against x j alone, with any "
            "one-dimensional smoother, and centre the result. <bookmark mark='c'/> Cycle through the variables until "
            "nothing changes: backfitting, from Jerome Friedman and Werner Stuetzle. <bookmark mark='d'/> Andreas "
            "Buja, Hastie and Tibshirani showed it is Gauss–Seidel iteration on a linear system, with convergence "
            "under appropriate compatibility and contraction conditions. Exact concurvity can prevent unique "
            "component estimates."       ) as vo:
            intro=label('Partial-residual updates fit one component at a time',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ozone(self):
        d = load("gam")
        panels = VGroup()
        spec = (("temp", r"temperature (F)", NWC), ("wind", r"wind (mph)", KDEC), ("solar", r"solar radiation (ly)", PATH))
        for k, (nm, xl, col) in enumerate(spec):
            c = d["comps"][nm]
            x, f, pr, ln = (np.asarray(c[q]) for q in ("x", "f", "partial", "lin"))
            lo, hi = float(min(pr.min(),f.min(),ln.min()))-0.2, float(max(pr.max(),f.max(),ln.max()))+0.2
            A = axes([float(x.min()), float(x.max())], [lo, hi], x_length=3.8, y_length=3.0, xlabel=xl, ylabel=r"",
                     xticks=[], yticks=[], center=[-4.4 + 4.4 * k, 0.6, 0])
            ax = A.ax
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=GREY_B, fill_opacity=0.6) for a, b in zip(x, pr)])
            fc = polyline(ax, x, f, col, 3.5)
            lc = DashedVMobject(polyline(ax, x, ln, WHITE, 1.5), num_dashes=20)
            tl = label(nm, font_size=22, color=col).next_to(A, UP, buff=0.1)
            panels.add(VGroup(A, pts, fc, lc, tl))
        foot = fit_rows(VGroup(
            label(rf"response: \ cube-root ozone, \ {d['n']} complete days; \ each curve with 4 df; \ backfitting converged in {d['iterations']} sweeps", font_size=22),
            label(r"dots: \ partial residuals; \ dashed: \ the linear model's slope", font_size=22, color=GREY_B),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> New York's ozone in the summer of 1973, a hundred and eleven complete days, on a "
            "chosen cube-root response scale, against temperature, wind and sunshine, each as a smooth curve with "
            "four degrees of freedom. Backfitting converged in seventeen sweeps in this fit. <bookmark mark='b'/> "
            "Temperature: ozone rises with heat, gently at first and more steeply above about seventy-five degrees. "
            "<bookmark mark='c'/> Wind: ozone falls with wind, steeply at first and then levelling off, as a partial "
            "association; this fit alone does not establish a causal wind effect. <bookmark mark='d'/> Sunshine: "
            "ozone rises with radiation and then flattens or dips on the brightest days. In each panel the dashed "
            "line is the linear model's slope; every curve bends where the line cannot."
        ) as vo:
            self.add(airq_tag())
            vo.wait_until("a")
            self.play(FadeIn(foot))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                p = panels[k]
                self.play(FadeIn(p[0]), FadeIn(p[4]), FadeIn(p[1]), Create(p[2]), Create(p[3]))
        self.clear_scene()

    def verdict(self):
        d = load("gam")
        hdr = [r"\textbf{model for cube-root ozone}", r"\textbf{$R^2$}", r"\textbf{10-fold CV error}"]
        body = [[r"linear in temperature, \ wind, \ sun", f"{d['r2_lin']:.3f}", f"{d['cv_lin']:.3f}"],
                [r"additive, \ 4 df per curve", f"{d['r2_add']:.3f}", f"{d['cv_add']:.3f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.36, colors=[GREY_A, GREY_B, SPLC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"paired CV MSE difference (additive minus linear): {d['cv_paired_delta']:.3f} $\pm$ {d['cv_paired_se']:.3f} case-loss SE", font_size=22),
            label(r"each curve is a one-dimensional smooth: \ readable, \ plottable, \ checkable", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Is the extra flexibility real? The linear model explains sixty-eight percent of the"
            " variation; the additive model seventy-six. <bookmark mark='b'/> More to the point, ten-fold "
            "cross-validation, with training-fold smoothing parameters and natural-spline prediction, compares "
            "held-out squared error on the cube-root scale. The displayed paired loss error describes this split, not"
            " uncertainty from re-running the entire CV procedure. And unlike a black box, every piece of the model "
            "is a curve you can plot and argue with."
        ) as vo:
            self.add(airq_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(tb[2]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def extensions(self):
        rows = fit_rows(VGroup(
            label(r"interactions: \ tensor-product smooths $f(x_1, x_2)$, \ sparingly", font_size=24, color=SPLC),
            label(r"penalized regression splines: \ a few dozen knots, \ REML for every $\lambda$ (Wood 2011)", font_size=24, color=KDEC),
            label(r"varying coefficients: \ $\beta(t)\, x$", font_size=24, color=PATH),
            label(r"the additive assumption is a model: \ check it, \ like linearity", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Extensions add structure back carefully: a few two-dimensional tensor-product smooths for "
            "interactions that matter. <bookmark mark='b'/> Simon Wood's penalized regression splines use a few dozen knots "
            "instead of n, and choose every smoothing parameter at once by REML, chapter seven's lesson. "
            "<bookmark mark='c'/> Varying-coefficient models let slopes change smoothly with time or place. "
            "<bookmark mark='d'/> But additivity is itself an assumption, to be checked like linearity was in Part 23."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def concurvity(self):
        rows = [
            cmath(r"\text{collinearity}", r":", r"x_1 \approx a + b x_2: \ \text{slopes unstable}", font_size=30),
            cmath(r"\text{concurvity}", r":", r"f_1(x_1) \approx g(x_2): \ \text{curves trade off}", font_size=30),
            cmath(r"\text{symptom}", r":", r"\text{slow backfitting, \ wide bands}", font_size=30),
            cmath(r"\text{ozone}", r":", r"\text{hot days are calm and sunny: \ correlated predictors}", font_size=28),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"Part 23's problem"), why(r"its nonparametric version"), why(r"the smoothers fight over the signal"),
                why(r"read the curves as partial effects")]
        with self.voiceover(
            "<bookmark mark='a'/> One caution. Part 23 met collinearity: when one predictor is nearly a linear function of "
            "another, their slopes are unstable. <bookmark mark='b'/> Additive models have a nonparametric version, "
            "concurvity: a smooth function of one variable that nearly equals a smooth function of another. Then the two "
            "curves can trade signal back and forth. <bookmark mark='c'/> Backfitting slows down and the curves' "
            "uncertainty grows. <bookmark mark='d'/> In the ozone data hot days also tend to be calm and sunny, so each curve "
            "is a partial effect, holding the others fixed, not a causal one."
        ) as vo:
            intro=label('Predictor dependence can make additive components unstable',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
