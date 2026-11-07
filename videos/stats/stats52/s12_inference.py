from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.debias()
        self.theory()
        self.data()
        self.forest()
        self.table()
        self.caveats()

    def card(self):
        card = chapter_card(11, r"Inference: \ the debiased lasso", r"Confidence intervals when $p$ is large", lit=(2014,), part=PART)
        with self.voiceover("Chapter eleven. Inference: the debiased lasso, or confidence intervals when p is large."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\hat\beta_j^{\text{lasso}}", r":", r"\text{biased towards zero, \ often exactly zero}", font_size=34),
            cmath(r"\text{its law}", r":", r"\text{a point mass at zero plus a shrunken bump: \ not normal}", font_size=32),
            cmath(r"\text{refit OLS on the selected set}", r":", r"\text{ignores the selection; \ Part 32's Board: \ broken}", font_size=30),
            cmath(r"\text{ordinary residual bootstrap near zero}", r":", r"\text{can fail; modified bootstraps need separate conditions}", font_size=34),
        ]
        rows[2][-1].set_color(BADC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"shrinkage"), why(r"Knight \& Fu (2000)"), why(r"selection then inference"), why(r"Chatterjee \& Lahiri (2010)")]
        heading = label('The estimator, loss, sampling law and target must be specified', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Estimation is not inference. The lasso's coefficients are shrunk towards zero, and often set exactly to zero. <bookmark mark='b'/> Their distribution is a point mass at zero plus a shrunken bump, as Keith Knight and Wenjiang Fu showed in 2000: nothing like a normal. <bookmark mark='c'/> Refitting least squares on the selected variables and reporting the usual intervals ignores the selection, and Part thirty-two's Board found those intervals broken. <bookmark mark='d'/> The ordinary residual bootstrap can fail near zero coefficients because of the nonsmooth selection boundary. Modified bootstrap procedures need separate theory."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def debias(self):
        rows = [
            cmath(r"\hat b_j", r"=", r"\hat\beta_j + \theta_j^\top X^\top(y - X\hat\beta)/n: \ \text{one Newton step}", font_size=32),
            cmath(r"\theta_j", r":", r"\text{the } j\text{-th row of an approximate inverse of } \hat\Sigma, \ \text{by a nodewise lasso}", font_size=30),
            cmath(r"\sqrt n(\hat b_j - \beta_j)", r"=", r"\underbrace{\theta_j^\top X^\top\varepsilon/\sqrt n}_{\text{normal}} + \underbrace{\sqrt n\,(\theta_j^\top\hat\Sigma - e_j^\top)(\beta - \hat\beta)}_{\text{bias} \ \lesssim\ s\log p/\sqrt n}", font_size=28),
            cmath(r"s\log p/\sqrt n\to0\text{ and inverse/noise conditions}", r"\Rightarrow", r"\hat b_j \pm 1.96\,\hat\sigma\sqrt{\theta_j^\top\hat\Sigma\theta_j/n}", font_size=32),
        ]
        rows[0][-1].set_color(GOODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Zhang \& Zhang (2014)"), why(r"van de Geer et al. (2014)"), why(r"Javanmard \& Montanari (2014)"), why(r"an honest interval, \ per coordinate")]
        heading = label('A small bias remainder requires inverse and noise conditions too', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The fix, found independently in 2014 by Cun-Hui Zhang and Stephanie Zhang, by Sara van de Geer and colleagues, and by Adel Javanmard and Andrea Montanari: add back a correction, one Newton step from the lasso towards least squares. <bookmark mark='b'/> The step uses a row of an approximate inverse of the sample covariance, which does not exist when p exceeds n, so it is built by regressing variable j on all the others with a lasso: the nodewise regression. <bookmark mark='c'/> The scaled error then splits into a term that is conditionally Gaussian when the model has independent homoskedastic Gaussian errors and the nodewise direction depends only on the design, and a bias term bounded by the lasso's error times the nodewise error, of order s log p over root n. <bookmark mark='d'/> When coefficient sparsity, the approximate inverse, conditional variances and noise estimation satisfy the theorem's uniform conditions so that this remainder vanishes, the debiased coefficient is asymptotically normal, with an estimable standard error, and the usual interval is honest, one coordinate at a time."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theory(self):
        rows = fit_rows(VGroup(
            label(r"Why the debiased lasso has a small bias remainder", font_size=36, color=GREY_A),
            label(r"the lasso's $\ell_1$ error, \ $s\sqrt{\log p/n}$, \ from chapter 1", font_size=26, color=LASSOC),
            label(r"the nodewise error, \ $\|\theta_j^\top\hat\Sigma - e_j^\top\|_\infty \lesssim \sqrt{\log p/n}$", font_size=26, color=BNDC2),
            label(r"their product is the bias, \ by H\"older: \ $\sqrt n \times s\log p/n$", font_size=26, color=SPIKEC),
            label(r"and the efficient variance: \ the interval is as short as semiparametric theory allows (Part 49)", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why the bias is small. <bookmark mark='b'/> The lasso's l-one error is s times the root of log p over n, from chapter one. <bookmark mark='c'/> The nodewise regression makes the approximate inverse accurate to the root of log p over n in each entry. <bookmark mark='d'/> By Hölder's inequality the bias is at most root n times their product, s log p over root n. <bookmark mark='e'/> And van de Geer and colleagues showed the resulting variance is the semiparametric efficiency bound of Part forty-nine: under their regularity and inverse-estimation conditions it can attain that bound; arbitrary regularized directions need not be efficient."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def data(self):
        d = load("diabetes")
        rows = [
            cmath(r"\text{the LARS paper's diabetes data}", r":", rf"n = {d['n']}, \ \text{{10 baseline variables}}", font_size=32),
            cmath(r"\text{add all interactions and squares}", r":", rf"p = {d['p']}: \ \text{{OLS is legal, \ but badly conditioned}}", font_size=30),
            cmath(r"\text{the lasso, \ by CV (one SE)}", r":", rf"{d['selected']} \text{{ of }} {d['p']} \text{{ selected}}", font_size=32),
            cmath(r"\text{then}", r":", r"\text{debiased intervals for the 10 main effects}", font_size=34),
        ]
        rows[2][-1].set_color(LASSOC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Efron et al. (2004)"), why(r"Part 32's model"), why(r"Part 28's rule"), why(r"per SD of each variable")]
        sel = ", ".join(d["selected_names"])
        heading = label('The diabetes intervals illustrate a highly ill-conditioned full model', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the diabetes study of the LARS paper, {d['n']} patients and ten baseline measurements, with disease progression a year later. <bookmark mark='b'/> Add every pairwise interaction and square, as Part thirty-two did: {d['p']} predictors. Least squares still has a solution, but the total, LDL and HDL cholesterol measures are nearly collinear. <bookmark mark='c'/> The lasso with cross-validation's one-standard-error rule keeps {d['selected']}: {sel.replace('*', ' times ').replace('^2', ' squared')}. <bookmark mark='d'/> Now the debiased intervals for the ten main effects, in units of one standard deviation of each standardized design term. With interactions, a main coefficient is a conditional association at zero values of the other centered main predictors, not a total or causal effect."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def forest(self):
        d = load("diabetes")
        lim = 45.0
        A = axes([-lim, lim], [0, 11], x_length=7.6, y_length=4.8, xlabel=r"full-model association coefficient, \ per design SD", ylabel=r"",
                 xticks=[-40, -20, 0, 20, 40], yticks=[], center=[-2.2, 0.0, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 11), color=GREY_C, stroke_width=2)
        names = VGroup()
        ols, deb = VGroup(), VGroup()
        for i, (o, b) in enumerate(zip(d["ols"], d["deb"])):
            y = 10 - i
            names.add(label(o["name"], font_size=22, color=GREY_A).next_to(ax.c2p(-lim, y), LEFT, buff=0.15))
            lo, hi = max(o["lo"], -lim), min(o["hi"], lim)
            seg = Line(ax.c2p(lo, y + 0.18), ax.c2p(hi, y + 0.18), color=BADC, stroke_width=4)
            if o["lo"] < -lim or o["hi"] > lim:
                seg = VGroup(seg, Arrow(ax.c2p(-lim + 8, y + 0.18), ax.c2p(-lim, y + 0.18), color=BADC, buff=0, stroke_width=3),
                             Arrow(ax.c2p(lim - 8, y + 0.18), ax.c2p(lim, y + 0.18), color=BADC, buff=0, stroke_width=3))
            ols.add(VGroup(seg, Dot(ax.c2p(max(min(o["b"], lim), -lim), y + 0.18), radius=0.06, color=BADC)))
            deb.add(VGroup(Line(ax.c2p(b["lo"], y - 0.18), ax.c2p(b["hi"], y - 0.18), color=GOODC, stroke_width=4),
                           Dot(ax.c2p(b["b"], y - 0.18), radius=0.07, color=GOODC)))
        excl = [b["name"] for b in d["deb"] if b["lo"] > 0 or b["hi"] < 0]
        wide = [o["name"] for o in d["ols"] if o["hi"] - o["lo"] > 100]
        side = fit_rows(VGroup(
            label(r"nominal 95\% intervals; \ coverage not validated here", font_size=22),
            label(rf"red: \ OLS with all {d['p']} terms", font_size=22, color=BADC),
            label(rf"{len(wide)} OLS intervals run off the chart: \ collinearity", font_size=22, color=BADC),
            label(r"green: \ debiased lasso; \ model/inverse assumptions unverified", font_size=22, color=GOODC),
            label(rf"{len(excl)} exclude zero: \ {', '.join(excl)}", font_size=22, color=GOODC),
        ), 3.8, 0.42, [5.0, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Ninety-five percent intervals for the ten main effects. <bookmark mark='b'/> In red, least squares with all {d['p']} terms. <bookmark mark='c'/> For {len(wide)} of the variables, the cholesterol measures and the triglycerides, its intervals are thousands of units wide and run off the chart: their separate full-model coefficients are weakly identified, despite a full-rank design. <bookmark mark='d'/> In green, the debiased lasso, using regularized nodewise directions. Regularization does not restore missing information about the original coefficients. <bookmark mark='e'/> {len(excl)} of its intervals exclude zero. But note what the price is: the intended target remains the original full-model coefficient, not a new regularized estimand. These narrow intervals have not been validated here. Near-collinearity can leave a large bias remainder; coefficient sparsity alone is insufficient for coverage."
        ) as vo:
            self.play(FadeIn(A), FadeIn(zero), FadeIn(names), FadeIn(museum_tag(r"Efron, \ Hastie, \ Johnstone \& Tibshirani (2004)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ols), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(deb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("diabetes")
        pick = [b for b in d["deb"] if b["name"] in ("bmi", "bp", "hdl", "ltg", "sex", "glu")]
        rows = [[r"variable", r"lasso", r"debiased", r"95\% interval"]]
        for b in pick:
            rows.append([b["name"], f"{b['lasso']:.1f}", f"{b['b']:.1f}", f"[{b['lo']:.1f}, {b['hi']:.1f}]"])
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.38, colors=[GREY_B] + [None] * len(pick))
        tab.move_to([0, 0.8, 0])
        for i in range(1, len(rows)):
            tab[i][1].set_color(LASSOC)
            tab[i][2].set_color(GOODC)
        r = {b["name"]: b for b in d["deb"]}
        foot = label(r"one-step correction may reduce shrinkage; \ residual bias remains", font_size=24, color=GREY_A).move_to([0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers for six of them. The lasso's estimate for body-mass index is {say(r['bmi']['lasso'], 1)}; debiased, {say(r['bmi']['b'], 1)}. For the log triglycerides, {say(r['ltg']['lasso'], 1)} becomes {say(r['ltg']['b'], 1)}. Variables the lasso dropped, like sex, get estimates and intervals too. <bookmark mark='b'/> The correction undoes the shrinkage, which is exactly what it is for: the lasso's estimates are biased towards zero, and the correction reduces shrinkage in these examples, but does not make the estimator exactly unbiased."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(museum_tag(r"Efron et al. (2004)")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def caveats(self):
        rows = fit_rows(VGroup(
            label(r"Conditions and limits of debiased lasso inference", font_size=36, color=GREY_A),
            label(r"the sparsity needed, \ $s\log p/\sqrt n\to0\text{ and inverse/noise conditions}$, \ is stronger than estimation's $s \ll n/\log p$", font_size=26, color=BADC),
            label(r"coverage can fall short in finite samples, \ especially for large, \ correlated effects", font_size=26, color=BADC),
            label(r"intervals hold one coordinate at a time: \ many at once needs Part 33's corrections", font_size=26, color=SPIKEC),
            label(r"the alternative: \ condition on the selection, \ exactly (Part 56)", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fine print. <bookmark mark='b'/> The sparsity the theory needs, s much smaller than root n over log p, is much stronger than estimation needs. <bookmark mark='c'/> In finite samples, coverage can fall short, especially for large effects among correlated variables, where the bias term is largest. <bookmark mark='d'/> The intervals hold one coordinate at a time; for many at once, the multiplicity corrections of Part thirty-three apply. <bookmark mark='e'/> And there is a different answer to the same question: under the corresponding linear-Gaussian selection model, condition on the lasso selection event and compute conditional intervals. Those can target selected-model rather than full-model parameters, the selective inference of Part fifty-six."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
