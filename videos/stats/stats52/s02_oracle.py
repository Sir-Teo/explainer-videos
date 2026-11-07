from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Oracle(VoiceoverScene):
    def construct(self):
        self.card()
        self.setting()
        self.cone()
        self.proof()
        self.chart()
        self.penalty()
        self.random_design()

    def card(self):
        card = chapter_card(1, r"The lasso's oracle inequality", r"As good as knowing the support, \ up to $\log p$", lit=(2009,), part=PART)
        with self.voiceover("Chapter one. The lasso's oracle inequality: as good as knowing the support, up to a log p."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setting(self):
        rows = [
            cmath(r"y = X\beta^* + \varepsilon", r":", r"X \in \mathbb R^{n \times p}, \ p \gg n, \ \ \|\beta^*\|_0 = s", font_size=34),
            cmath(r"\text{the oracle}", r":", r"\text{least squares on the true support: \ error}^2 \approx \sigma^2 s/n", font_size=32),
            cmath(r"\hat\beta", r"=", r"\arg\min \tfrac{1}{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1", font_size=34),
            cmath(r"\text{the claim}", r":", r"\|\hat\beta - \beta^*\|_2^2 \lesssim \sigma^2\, s\log p / n: \ \text{only a } \log p \text{ lost}", font_size=32),
        ]
        rows[2][-1].set_color(LASSOC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"$s$ non-zero coefficients"), why(r"needs to know which"), why(r"Tibshirani (1996), \ Part 32"), why(r"Bickel, \ Ritov \& Tsybakov (2009)")]
        heading = label('Sparse estimation rates require a well-conditioned design on the error cone', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The setting: a linear model with many more coefficients than observations, of which only s are non-zero. <bookmark mark='b'/> An oracle who knew the support would fit least squares on those s variables, with squared coefficient error of that order when the support covariance is well conditioned. <bookmark mark='c'/> The lasso does not know the support. It minimizes the squared error plus lambda times the l-one norm. <bookmark mark='d'/> The claim, proved by Peter Bickel, Ya'acov Ritov and Alexandre Tsybakov in 2009: under a positive restricted eigenvalue, normalized design columns and a sufficiently large noise-calibrated penalty, its squared error is of order sigma squared s log p over n, with a curvature-dependent constant. Not knowing which s of the p variables matter costs only a factor of log p."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cone(self):
        rows = [
            cmath(r"\lambda \ge 2\|X^\top\varepsilon/n\|_\infty", r"\Rightarrow", r"\Delta = \hat\beta - \beta^* \in \mathcal C = \{\|\Delta_{S^c}\|_1 \le 3\|\Delta_S\|_1\}", font_size=30),
            cmath(r"\|X^\top\varepsilon/n\|_\infty", r"\approx", r"\sigma\sqrt{2\log p/n}: \ \text{Gaussian noise, }\|X_j\|^2=n\text{ (Part 51)}", font_size=30),
            cmath(r"\kappa", r"=", r"\inf_{\Delta \in \mathcal C\setminus\{0\}} \frac{\|X\Delta\|^2/n}{\|\Delta\|^2} > 0: \ \text{restricted eigenvalue}", font_size=32),
            cmath(r"p > n", r":", r"X^\top X \text{ is singular, \ but can be well-conditioned on the cone}", font_size=30),
        ]
        rows[0][-1].set_color(LASSOC)
        rows[2][-1].set_color(BNDC2)
        whys = [why(r"the basic inequality"), why(r"the penalty's size"), why(r"Bickel--Ritov--Tsybakov"), why(r"the whole point")]
        heading = label('The noise event and penalty place the lasso error in a cone', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The key step. If lambda is at least twice the largest correlation between the noise and a "
            "column, the error vector lies in a cone, where its mass off the true support is at most three times its mass on "
            "it. <bookmark mark='b'/> That largest correlation is the maximum of p Gaussians, of size sigma times the root of "
            "two log p over n, from Part fifty-one. <bookmark mark='c'/> The restricted eigenvalue, kappa, is the smallest "
            "ratio of the prediction error to the coefficient error, over that cone only. <bookmark mark='d'/> With more "
            "variables than observations, X transpose X is singular, so some directions are invisible. But the cone can avoid "
            "all of them, and then the problem is well-conditioned exactly where the error lives."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\tfrac{1}{2n}\|X\Delta\|^2", r"\le", r"\tfrac{\lambda}{2}\|\Delta\|_1 + \lambda(\|\beta^*\|_1 - \|\hat\beta\|_1)", font_size=32),
            cmath(r"\|\beta^*\|_1 - \|\hat\beta\|_1", r"\le", r"\|\Delta_S\|_1 - \|\Delta_{S^c}\|_1", font_size=34),
            cmath(r"\tfrac{\kappa}{2}\|\Delta\|^2 \le \tfrac{1}{2n}\|X\Delta\|^2", r"\le", r"\tfrac{3\lambda}{2}\|\Delta_S\|_1 \le \tfrac{3\lambda}{2}\sqrt s\,\|\Delta\|", font_size=32),
            cmath(r"\|\hat\beta - \beta^*\|_2", r"\le", r"\frac{3\sqrt s\,\lambda}{\kappa} \asymp \frac{\sigma}{\kappa}\sqrt{\frac{s\log p}{n}}", font_size=34),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"optimality of $\hat\beta$, \ and $\lambda$"), why(r"the triangle inequality"), why(r"RE, \ then Cauchy--Schwarz"), why(r"divide by $\|\Delta\|$")]
        heading = label('Restricted curvature turns the basic inequality into an error bound', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The proof fits on one screen. Because the lasso minimizes its objective, comparing it with "
            "the truth gives a basic inequality: half the prediction error is at most half lambda times the error's l-one "
            "norm, plus lambda times the drop in the penalty. <bookmark mark='b'/> The triangle inequality bounds that drop by "
            "the error on the support minus the error off it, which is what forces the cone. <bookmark mark='c'/> On the cone, "
            "the restricted eigenvalue turns the prediction error into a coefficient error, and Cauchy–Schwarz turns an l-one "
            "norm on s coordinates into root s times an l-two norm. <bookmark mark='d'/> Dividing through: the error is at "
            "most three root s lambda over kappa, which with the right lambda is sigma over kappa times the root of s log p over n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("oracle")
        n = np.asarray([r["n"] for r in d["rows"]], float)
        ln = np.log10(n)
        err = np.log10([r["err"] for r in d["rows"]])
        rate = np.log10([r["rate"] for r in d["rows"]])
        ymin = min(-.8, float(min(err.min(),rate.min()))-.08)
        ymax = max(.3, float(max(err.max(),rate.max()))+.08)
        A = axes([1.9, 3.2], [ymin, ymax], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}\|\hat\beta - \beta^*\|_2$",
                 xticks=[2, np.log10(300), 3], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-0.75, -0.5, -0.25, 0, 0.25], center=[-2.5, 0.2, 0])
        ax = A.ax
        cr = VGroup(polyline(ax, ln, rate, BNDC2, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=BNDC2) for a, b in zip(ln, rate)])
        ce = VGroup(polyline(ax, ln, err, LASSOC, 3), *[Dot(ax.c2p(a, b), radius=0.1, color=LASSOC) for a, b in zip(ln, err)])
        ratio = float(np.mean([r["err"] / r["rate"] for r in d["rows"]]))
        slope = float(np.polyfit(ln, err, 1)[0])
        r0, r1 = d["rows"][0], d["rows"][-1]
        side = fit_rows(VGroup(
            label(rf"$p = {d['p']}$, \ $s = {d['s']}$, \ $\sigma = 1$, \ Gaussian design", font_size=22),
            label(r"purple: \ the rate $\sqrt{s\log p/n}$", font_size=22, color=BNDC2),
            label(rf"blue: \ the lasso, \ {r0['err']:.2f} at $n = 100$, \ {r1['err']:.2f} at 1,200", font_size=22, color=LASSOC),
            label(rf"slope {slope:.2f} \ (rate: $-0.50$); \ ratio about {ratio:.1f}", font_size=22, color=GOODC),
            label(rf"variables selected: \ {r0['size']:.0f} at $n = 100$, \ {r1['size']:.0f} at 1,200", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: five hundred variables, ten of them non-zero, Gaussian design, and a conditional-Gaussian union-bound penalty with failure probability at most five percent. <bookmark mark='b'/> The purple line is the rate, the root of s log p over n. <bookmark mark='c'/> The lasso's error, in blue, falls from {say(r0['err'], 2)} with a hundred observations, fewer than there are variables, to {say(r1['err'], 2)} with twelve hundred. <bookmark mark='d'/> Its slope on the log scale is {say(slope, 2)}, against the theory's minus a half, and it stays within a constant factor of about {ratio:.1f} of the rate throughout. <bookmark mark='e'/> The number of variables it selects falls from about {r0['size']:.0f} towards the true ten."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ rate proxy; \ 95\% noise-event penalty")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cr), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ce), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def penalty(self):
        d = load("oracle")
        rows = [[r"$\lambda$ / the theory's"] + [f"{r['mult']:g}" for r in d["lam_rows"]],
                [r"$\|\hat\beta - \beta^*\|_2$"] + [f"{r['err']:.2f}" for r in d["lam_rows"]],
                [r"variables selected"] + [f"{r['size']:.0f}" for r in d["lam_rows"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.45, colors=[GREY_B, LASSOC, GREY_A])
        tab.move_to([0, 0.9, 0])
        best = min(d["lam_rows"], key=lambda r: r["err"])
        foot = label(rf"best error at {best['mult']:g}$\times$ the theory's $\lambda$, \ with {best['size']:.0f} variables: \ the theory is conservative", font_size=24, color=GREY_A).move_to([0, -1.1, 0])
        foot2 = label(r"too small: \ noise enters; \ too large: \ shrinkage bias; \ in practice, \ cross-validate", font_size=24, color=LASSOC).move_to([0, -1.9, 0])
        rr = {r["mult"]: r for r in d["lam_rows"]}
        with self.voiceover(
            f"<bookmark mark='a'/> How much does the penalty matter? At four hundred observations, scaling the theory's lambda from an eighth to four times. <bookmark mark='b'/> The smallest error, {say(best['err'], 2)}, comes at {best['mult']:g} times the theory's choice, which selects about {best['size']:.0f} variables: the theorem's lambda guarantees the cone on its stated high-probability noise event, but at the price of extra shrinkage. <bookmark mark='c'/> Too small, and noise variables enter by the hundred; too large, and the true coefficients are shrunk towards zero, an error of {say(rr[4.0]['err'], 1)} at four times. In practice lambda is chosen by cross-validation, as in Part thirty-two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def random_design(self):
        rows = [
            cmath(r"\text{i.i.d. rows }x_i\sim N(0,\Sigma),\ \max_j\Sigma_{jj}\le C", r":", r"\tfrac{\|X\Delta\|^2}{n} \ge \tfrac{1}{4}\|\Sigma^{1/2}\Delta\|^2 - c\,\tfrac{\log p}{n}\|\Delta\|_1^2", font_size=30),
            cmath(r"\Delta \in \mathcal C", r":", r"\|\Delta\|_1 \le 4\sqrt s\,\|\Delta\|_2", font_size=34),
            cmath(r"n \gtrsim s\log p", r"\Rightarrow", r"\kappa \ge \lambda_{\min}(\Sigma)/8: \ \text{RE w.h.p.; covariance-dependent sample constant}", font_size=32),
            cmath(r"\text{the proof}", r":", r"\text{Gordon's inequality \ (Part 51, \ chapter 7)}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Raskutti, \ Wainwright \& Yu (2010)"), why(r"the cone's geometry"), why(r"correlated designs too"), why(r"min--max comparison")]
        heading = label('Gaussian restricted eigenvalues depend on covariance and sample size', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Does a real design satisfy the restricted eigenvalue condition? Garvesh Raskutti, Martin Wainwright and Bin Yu showed in 2010 that for independent Gaussian rows with controlled marginal variances and a positive lower population eigenvalue, the prediction error is at least a quarter of the population quadratic form, minus a term of order log p over n times the squared l-one norm. <bookmark mark='b'/> On the cone, the l-one norm is at most four root s times the l-two norm. <bookmark mark='c'/> So once n is a covariance-dependent constant times s log p, the restricted eigenvalue is at least an eighth of the smallest eigenvalue of the population covariance, with high probability, even for correlated designs. <bookmark mark='d'/> The proof is Gordon's min-max comparison from Part fifty-one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
