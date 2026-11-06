from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class Wishart(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.bartlett()
        self.check()
        self.consequences()
        self.conjugate()
        self.spread()
        self.mp()

    def card(self):
        card = chapter_card(2, r"Wishart", r"The distribution of a covariance matrix", lit=(1928,), part=PART)
        with self.voiceover("Chapter two. The Wishart distribution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"z_1, \dots, z_m", r"\sim", r"N_p(0, \Sigma) \ \text{independent}", font_size=30),
            cmath(r"W", r"=", r"\textstyle\sum_k z_k z_k^\top \ \sim \ W_p(m, \Sigma)", font_size=32),
            cmath(r"(n - 1) S", r"\sim", r"W_p(n - 1, \Sigma), \ \text{independent of } \bar x", font_size=30),
            cmath(r"p = 1", r":", r"\sigma^2 \chi^2_m", font_size=32),
        ]
        rows[1][2].set_color(PCC)
        whys = [why(r"centred normal vectors"), why(r"John Wishart (1928)"), why(r"Part 8's result, \ in $p$ dimensions"),
                why(r"the chi-squared, \ generalized")]
        with self.voiceover(
            "<bookmark mark='a'/> Take m independent normal vectors with covariance sigma. <bookmark mark='b'/> The sum of "
            "their outer products has the Wishart distribution, found by John Wishart in 1928. <bookmark mark='c'/> The "
            "sample covariance, times n minus one, is Wishart with n minus one degrees of freedom and independent of the "
            "sample mean, the multivariate form of Part 8's theorem. <bookmark mark='d'/> In one dimension it is sigma "
            "squared times a chi-squared: the Wishart is the chi-squared of matrices."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bartlett(self):
        rows = [
            cmath(r"\Sigma", r"=", r"L L^\top", font_size=32),
            cmath(r"W", r"=", r"L A A^\top L^\top", font_size=32),
            cmath(r"A_{ii}^2", r"\sim", r"\chi^2_{m - i + 1}, \ \ A_{ij} \sim N(0, 1) \ (i > j)", font_size=30),
            cmath(r"\det W", r"=", r"\det \Sigma \cdot \textstyle\prod_i \chi^2_{m - i + 1}", font_size=30),
        ]
        rows[2][2].set_color(PCC)
        whys = [why(r"Cholesky"), why(r"Bartlett (1933)"), why(r"all independent"),
                why(r"the generalized variance: \ a product of chi-squareds")]
        with self.voiceover(
            "<bookmark mark='a'/> Maurice Bartlett found the structure inside. Factor sigma by Cholesky. "
            "<bookmark mark='b'/> Then a Wishart matrix is L times A A transpose times L transpose, <bookmark mark='c'/> "
            "where A is lower triangular with chi-distributed diagonal, degrees of freedom falling by one down the diagonal, "
            "and independent standard normals below it. <bookmark mark='d'/> One consequence: the determinant, the "
            "generalized variance, is a product of independent chi-squareds. Statkit draws Wisharts this way."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        d = load("wishart")
        S, mu = np.asarray(d["S"]), np.asarray(d["mean"])
        hdr = [r"\textbf{quantity}", r"\textbf{20,000 Bartlett draws}", r"\textbf{theory}"]
        body = [[r"$E W / m$, \ entry (1,1)", f"{mu[0, 0]:.3f}", f"{S[0, 0]:.3f}"],
                [r"$E W / m$, \ entry (1,2)", f"{mu[0, 1]:.3f}", f"{S[0, 1]:.3f}"],
                [r"$E W / m$, \ entry (2,3)", f"{mu[1, 2]:.3f}", f"{S[1, 2]:.3f}"],
                [r"$\mathrm{Var}\, W_{11}$", f"{d['var11']:.1f}", rf"$2m\sigma_{{11}}^2 = {d['th11']:.1f}$"],
                [r"$\mathrm{Var}\, W_{12}$", f"{d['var12']:.1f}", rf"$m(\sigma_{{12}}^2 + \sigma_{{11}}\sigma_{{22}}) = {d['th12']:.1f}$"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.3, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[1].set_color(PCC)
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(rf"$p = 3$, \ $m = {d['df']}$ degrees of freedom", font_size=22),
            label(r"the variance of a covariance depends on the variances too", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A check, with three variables and ten degrees of freedom, twenty thousand draws. The average "
            "matrix divided by ten matches sigma to the third decimal. <bookmark mark='b'/> The variances of its entries match "
            "the theory too: two m sigma one one squared for a diagonal entry, and m times sigma one two squared plus sigma "
            "one one sigma two two for an off-diagonal one. The noise in an estimated covariance depends on the variances as "
            "well, which is why correlations are easier to compare than covariances."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:4]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[4:]), FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def consequences(self):
        rows = [
            cmath(r"a^\top W a / a^\top \Sigma a", r"\sim", r"\chi^2_m \ \text{for any fixed } a", font_size=30),
            cmath(r"T^2", r"=", r"n (\bar x - \mu)^\top S^{-1} (\bar x - \mu)", font_size=30),
            cmath(r"\tfrac{n - p}{p(n - 1)} T^2", r"\sim", r"F_{p, n - p}", font_size=32),
            cmath(r"\text{needs}", r":", r"S \text{ invertible: \ } n > p", font_size=30),
        ]
        rows[2][2].set_color(PCC)
        whys = [why(r"every projection is chi-squared"), why(r"chapter three's statistic"),
                why(r"exact, \ from the Wishart"), why(r"chapter ten")]
        with self.voiceover(
            "<bookmark mark='a'/> The Wishart's main use is distribution theory. Every one-dimensional projection is a "
            "scaled chi-squared. <bookmark mark='b'/> From that, the next chapter's statistic, Hotelling's T squared, "
            "<bookmark mark='c'/> has an exact F distribution after rescaling, for any sample size. <bookmark mark='d'/> All "
            "of it needs the sample covariance to be invertible, which requires more observations than variables, chapter "
            "ten's warning."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def spread(self):
        rows = [
            cmath(r"\Sigma = I_p", r":", r"\text{every true eigenvalue is } 1", font_size=30),
            cmath(r"E\, S", r"=", r"I_p \ \text{ but } \ E\, \lambda_{\max}(S) > 1 > E\, \lambda_{\min}(S)", font_size=30),
            cmath(r"\text{spread}", r":", r"\text{the sample eigenvalues fan out}", font_size=30),
            cmath(r"p/n \to \gamma", r":", r"\text{they fill } [(1 - \sqrt\gamma)^2, (1 + \sqrt\gamma)^2]", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"no direction is special"), why(r"unbiased entries, \ biased eigenvalues"),
                why(r"the largest overstated, \ the smallest understated"), why(r"Marchenko \& Pastur (1967)")]
        with self.voiceover(
            "<bookmark mark='a'/> A warning already visible here. Suppose the true covariance is the identity, all "
            "eigenvalues one. <bookmark mark='b'/> The sample covariance is unbiased entry by entry, but its eigenvalues are "
            "not: the largest is too big on average and the smallest too small. <bookmark mark='c'/> The sample eigenvalues "
            "fan out. <bookmark mark='d'/> When p grows with n, Vladimir Marchenko and Leonid Pastur showed in 1967 that they "
            "fill a whole interval determined by the ratio gamma, p over n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mp(self):
        d = load("wishart")
        ev = np.asarray(d["ev"])
        a, b = d["mp_ab"]
        A = axes([0, 3.2], [0, 1.6], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of $S$", ylabel=r"density",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5], center=[-2.0, 0.3, 0])
        ax = A.ax
        edges = np.linspace(0, 3.2, 33)
        h = np.histogram(ev, edges)[0] / (len(ev) * (edges[1] - edges[0]))
        bars = hist_bars(ax, edges, h, color=PCC, opacity=0.7)
        mp = curve(ax, np.asarray(d["mp_x"]), np.asarray(d["mp_y"]), TRUE, 3)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.55), color=WHITE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"$p = {d['p']}$ variables, \ $n = {d['n']}$ observations, \ $\Sigma = I$", font_size=22),
            label(r"white: \ every true eigenvalue", font_size=22),
            label(rf"blue: \ the sample's, \ from {min(ev):.2f} to {max(ev):.2f}", font_size=22, color=PCC),
            label(rf"gold: \ Marchenko--Pastur on [{a:.2f}, {b:.2f}]", font_size=22, color=TRUE),
            label(r"a `top component' that is pure noise: \ Part 52", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fifty variables, a hundred observations, true covariance the identity. "
            "<bookmark mark='b'/> Every true eigenvalue is one. <bookmark mark='c'/> The sample eigenvalues run from point one "
            "to two point seven six. <bookmark mark='d'/> They follow the Marchenko–Pastur law closely. <bookmark mark='e'/> So "
            "a principal component analysis of pure noise would report a dominant direction nearly three times the average: "
            "with many variables, large sample eigenvalues are not evidence of structure. Part 52 returns to this."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.03), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(mp), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def conjugate(self):
        rows = [
            cmath(r"f(W)", r"\propto", r"|W|^{(m - p - 1)/2} \exp\{-\tfrac12 \mathrm{tr}(\Sigma^{-1} W)\}", font_size=28),
            cmath(r"\Sigma", r"\sim", r"\mathrm{IW}(\nu, \Psi) \ \text{a priori}", font_size=30),
            cmath(r"\Sigma \mid X", r"\sim", r"\mathrm{IW}(\nu + n, \ \Psi + (n - 1)S)", font_size=30),
            cmath(r"\text{caution}", r":", r"\text{one } \nu \text{ governs every variance's certainty}", font_size=28),
        ]
        rows[2][-1].set_color(POST)
        whys = [why(r"for $m \ge p$"), why(r"inverse-Wishart, \ Part 26"), why(r"conjugate: \ add the data's scatter"), why(r"LKJ priors separate scale and correlation")]
        with self.voiceover(
            "<bookmark mark='a'/> The Wishart has an explicit density, a power of the determinant times an exponential "
            "of a trace. <bookmark mark='b'/> Its inverse is the conjugate prior for a normal covariance matrix, Part "
            "26's language. <bookmark mark='c'/> The posterior is again inverse-Wishart: add the sample size to the "
            "degrees of freedom and the data's scatter matrix to the scale. Bayesian updating of a covariance is "
            "addition. <bookmark mark='d'/> But a single degrees-of-freedom parameter controls how certain the prior "
            "is about every variance and every correlation at once, which is why modern practice, as in Stan, often "
            "prefers separate priors on the scales and on the correlation matrix."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
