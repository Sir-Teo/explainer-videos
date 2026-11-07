from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats23.common import *  # noqa: F403


class Cluster(VoiceoverScene):
    def construct(self):
        self.card()
        self.schools()
        self.moulton()
        self.robust()
        self.few()
        self.wild()
        self.level()
        self.model_it()
        self.board()

    def card(self):
        card = chapter_card(5, r"Clustering", r"Sixty pupils are not sixty schools", lit=(1986, 2008), part=PART)
        with self.voiceover("Chapter five. Clustering."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def schools(self):
        d = load("schools")
        per = d["per_school"]
        A = axes([-0.5, 1.5], [410, 620], x_length=5.6, y_length=4.8, xlabel=r"", ylabel=r"school mean score",
                 xticks=[], yticks=[450, 500, 550], center=[-3.2, 0.1, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(5))
        dots = VGroup()
        for m, prog, size in per:
            x = (1.0 if prog else 0.0) + 0.35 * (g.random() - 0.5)
            dots.add(Dot(ax.c2p(x, m), radius=0.03 + 0.0012 * size, color=PROG if prog else CTRL, fill_opacity=0.8))
        names = VGroup(label(r"no programme", font_size=22, color=CTRL).next_to(ax.c2p(0, 410), DOWN, buff=0.3),
                       label(r"programme", font_size=22, color=PROG).next_to(ax.c2p(1, 410), DOWN, buff=0.3))
        b, si, sc = d["coef"], d["se_iid"], d["se_cr1"]
        rows = fit_rows(VGroup(
            label(rf"40 of the World's 400 schools; \ {d['n']:,} pupils", font_size=22),
            label(r"half the schools run a tutoring programme", font_size=22, color=PROG),
            label(rf"OLS on pupils: \ effect {b[1]:.1f} points \ (truth {d['truth']:.0f})", font_size=22, color=OLS_C),
            label(rf"iid SE: \ {si[1]:.2f}", font_size=22, color=RES),
            label(rf"cluster-robust SE: \ {sc[1]:.2f}", font_size=22, color=CLUSTER),
        ), 5.0, 0.42, [3.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has four hundred schools. Sample forty and take every pupil in them: about two "
            "and a half thousand pupils. <bookmark mark='b'/> Half the schools run a tutoring programme, assigned to whole "
            "schools. Each dot is a school's mean score, sized by its number of pupils. <bookmark mark='c'/> A regression "
            "of pupils' scores on the programme and home background estimates the effect at twenty-seven and a half points; "
            "the World's truth is twenty. <bookmark mark='d'/> The usual standard error says three point six five, so the "
            "estimate looks precise and wrong. <bookmark mark='e'/> The cluster-robust standard error says ten. The truth is "
            "well inside its interval."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.03), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def moulton(self):
        d = load("schools")
        rows = [
            cmath(r"\dfrac{\mathrm{Var}_{\text{true}}}{\mathrm{Var}_{\text{iid}}}", r"\approx", r"1 + (\bar m - 1)\, \rho_x \rho_\varepsilon", font_size=30),
            cmath(r"\bar m, \ \rho_x, \ \rho_\varepsilon", r"=", rf"{d['m_bar']:.1f}, \ {d['rho_x']:.0f}, \ {d['rho_e']:.3f}", font_size=30),
            cmath(r"\text{factor}", r"=", rf"{d['moulton']:.1f}: \ \ \text{{SE}} \times {np.sqrt(d['moulton']):.2f}", font_size=30),
            cmath(r"\text{observed}", r":", rf"\text{{CR1 / iid}} = {d['ratio']:.2f}", font_size=30),
        ]
        rows[2][2].set_color(CLUSTER)
        whys = [why(r"Moulton (1986); \ Kish's design effect, \ Part 18"), why(r"pupils per school; \ the programme is constant within a school"),
                why(r"a small correlation, \ times sixty"), why(r"a useful approximation, \ not an exact adjustment")]
        intro = label('The Moulton factor is an approximation for this adjusted unequal-size design', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Brent Moulton gave the size of the problem in 1986. A simple equal-size "
            "exchangeable model gives a variance inflation factor of one plus cluster size minus one, times the "
            "regressor and error intraclass correlations. Using average size with unequal clusters and covariate "
            "adjustment is a heuristic. It's Kish's design effect from Part 18. <bookmark mark='b'/> Here there are "
            "sixty-one pupils per school; the programme is the same for every pupil in a school, so its correlation "
            "is one; and the residuals' intraclass correlation is only point one one four. <bookmark mark='c'/> But "
            "point one one four times sixty is about seven: the variance is understated eightfold, the standard error"
            " by a factor of two point eight. <bookmark mark='d'/> The cluster-robust standard error came out two "
            "point seven five times the iid one."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def robust(self):
        rows = [
            cmath(r"\mathrm{Var}(\hat\beta)", r"=", r"(X^\top X)^{-1} \Big(\textstyle\sum_g X_g^\top \Sigma_g X_g\Big) (X^\top X)^{-1}", font_size=28),
            cmath(r"\widehat{\text{meat}}", r"=", r"\textstyle\sum_g (X_g^\top e_g)(X_g^\top e_g)^\top", font_size=30),
            cmath(r"\text{CR1}", r":", r"\times \tfrac{G}{G - 1}\tfrac{n - 1}{n - p}, \ \ \text{compare with } t_{G - 1}", font_size=30),
            cmath(r"\text{consistent}", r":", r"\text{as } G \to \infty, \ \text{any correlation within clusters}", font_size=30),
        ]
        rows[1][2].set_color(CLUSTER)
        whys = [why(r"independent clusters, \ anything inside"), why(r"sum the scores in a cluster, \ then square"),
                why(r"Liang \& Zeger (1986); \ Arellano (1987)"), why(r"the number of clusters is the sample size")]
        intro = label('Cluster inference relies on many independent, non-dominant clusters', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The fix is chapter one's sandwich again, with clusters independent of each other "
            "but anything allowed inside. <bookmark mark='b'/> For the meat, add up each cluster's scores, X "
            "transpose e, and square the sum: correlations within a cluster are captured because the cross-products "
            "are kept. <bookmark mark='c'/> With a small-sample factor this is CR one, from Kung-Yee Liang and Scott "
            "Zeger and from Manuel Arellano, and it's compared with a t distribution with G minus one degrees of "
            "freedom. <bookmark mark='d'/> It is consistent as the number of clusters grows. Cluster asymptotics need"
            " many independent schools, finite moments and no dominant cluster. Information also depends on "
            "within-school predictor variation; there is no universal effective sample size equal to G."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def few(self):
        rows = [
            cmath(r"G = 8", r":", r"\text{eight residual sums estimate a } 3 \times 3 \text{ meat}", font_size=30),
            cmath(r"e_g", r"\ne", r"\varepsilon_g: \ \text{residuals are shrunk, \ most in big or unusual clusters}", font_size=28),
            cmath(r"\text{result}", r":", r"\text{SEs can be too small; tests can over-reject}", font_size=30),
            cmath(r"\text{in the wild}", r":", r"\text{states, \ countries, \ industries: \ often } G < 20", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"a variance from eight numbers"), why(r"chapter four's leverage problem, \ per cluster"),
                why(r"Cameron, \ Gelbach \& Miller (2008)"), why(r"difference-in-differences, \ Part 37")]
        intro = label('Few clusters can make variance estimates unreliable', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> But clusters are often few. With eight schools, the meat is estimated from eight "
            "summed residual vectors. <bookmark mark='b'/> And as chapter four found for single points, residuals "
            "understate errors, most for clusters that are large or unusual. <bookmark mark='c'/> With few clusters "
            "CR one can be too small and tests can reject too often, as Colin Cameron, Jonah Gelbach and Douglas "
            "Miller documented in 2008. <bookmark mark='d'/> This is everyday reality: policy studies cluster by "
            "state or country, and Part 37's difference-in-differences studies often have fewer than twenty."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wild(self):
        rows = [
            cmath(r"\text{1. fit under } H_0", r":", r"\beta_j = b_0: \ \tilde y_i, \ \tilde e_i", font_size=30),
            cmath(r"\text{2. flip clusters}", r":", r"y_i^* = \tilde y_i + w_{g(i)}\, \tilde e_i, \ \ w_g \in \{\pm 1\} \text{ or Webb's six}", font_size=28),
            cmath(r"\text{3. refit}", r":", r"t^* = (\hat\beta_j^* - b_0)/\mathrm{SE}_{\mathrm{CR1}}^*", font_size=30),
            cmath(r"\text{4. compare}", r":", r"p_{MC} = (1 + \#\{|t^*|\ge|t|\})/(B+1)", font_size=30),
        ]
        rows[1][2].set_color(CLUSTER)
        whys = [why(r"impose the null: \ the restricted bootstrap"), why(r"each school's residuals keep their pattern"),
                why(r"bootstrap the $t$, \ not $\hat\beta$: \ Part 16"), why(r"Rademacher: \ only $2^8 = 256$ distinct draws; \ Webb (2014): $6^8$")]
        intro = label('Resample clusters under the tested null', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The wild cluster bootstrap. First, fit the model with the null hypothesis imposed, "
            "keeping fitted values and residuals. <bookmark mark='b'/> Then make new data sets by multiplying all the"
            " residuals in a cluster by the same random weight, plus or minus one, or one of Matthew Webb's six "
            "values. Each school's residuals keep their internal pattern, which is what the inference needs to "
            "respect. <bookmark mark='c'/> Refit and compute the cluster-robust t-statistic each time. <bookmark "
            "mark='d'/> We use one plus the number of at-least-as-extreme bootstrap statistics, divided by one plus "
            "the number of draws. This Monte Carlo correction prevents zero p-values; it does not make few-cluster "
            "inference exact. With eight clusters, signs alone give only two hundred and fifty-six possible data "
            "sets; Webb's weights give one point seven million."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def level(self):
        rows = [
            cmath(r"\text{which level?}", r":", r"\text{pupils, \ schools, \ towns, \ regions}", font_size=30),
            cmath(r"\text{design view}", r":", r"\text{cluster where the treatment was assigned}", font_size=30),
            cmath(r"\text{two-way}", r":", r"V = V_{\text{school}} + V_{\text{year}} - V_{\text{school} \times \text{year}}", font_size=30),
            cmath(r"\text{too coarse}", r":", r"\text{fewer clusters; not automatically conservative}", font_size=30),
        ]
        rows[1][2].set_color(CLUSTER)
        whys = [why(r"each level nests the one before"), why(r"Abadie, \ Athey, \ Imbens \& Wooldridge (2023)"),
                why(r"Cameron, \ Gelbach \& Miller (2011)"), why(r"the trade-off of the Board's two rows")]
        intro = label('Choose clustering from treatment assignment and sampling design', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> At which level should you cluster: pupils, schools, towns, or regions? <bookmark "
            "mark='b'/> Alberto Abadie, Susan Athey, Guido Imbens and Jeffrey Wooldridge argue from the design: "
            "cluster at the level where the treatment was assigned, or where the sample was drawn. Here the programme"
            " was assigned to schools, so schools. <bookmark mark='c'/> When errors are correlated along two "
            "dimensions at once, say schools and years, two-way clustering adds the two one-way variances and "
            "subtracts their intersection. <bookmark mark='d'/> Coarser clustering can reduce the available "
            "independent units and make variance estimates unreliable; it is not automatically conservative. "
            "Few-cluster two-way estimates can even be indefinite."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def model_it(self):
        rows = [
            cmath(r"y_{gi}", r"=", r"x_{gi}^\top\beta + u_g + \varepsilon_{gi}", font_size=30),
            cmath(r"\Omega_g", r"=", r"\sigma_\varepsilon^2 I + \sigma_u^2 \mathbf{1}\mathbf{1}^\top", font_size=30),
            cmath(r"\text{GLS with } \Omega_g", r"=", r"\text{fixed effects in a random-intercept model}", font_size=30),
            cmath(r"\text{robust SE}", r":", r"\text{still advised, \ in case } \Omega_g \text{ is wrong}", font_size=30),
        ]
        rows[2][2].set_color(GLS_C)
        whys = [why(r"a school effect shared by its pupils"), why(r"exchangeable: \ one correlation $\rho$"),
                why(r"chapter three, \ applied per school: \ Part 25"), why(r"Part 24's GEE does the same")]
        intro = label('A random intercept models a shared school effect', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Clustering can be modelled instead of merely corrected. Give each school a "
            "mean-zero effect u g shared by all its pupils, uncorrelated with the predictors and independent of "
            "individual errors. <bookmark mark='b'/> Then each school's errors have an exchangeable covariance: equal"
            " variances, and one correlation between any two pupils. <bookmark mark='c'/> Generalized least squares "
            "with a known covariance gives the fixed-coefficient estimator for the random-intercept model of Part 25,"
            " more efficient than least squares when the model is right. <bookmark mark='d'/> Pairing it with a "
            "cluster-robust standard error can protect against covariance misspecification under cluster asymptotics,"
            " while a biased conditional-mean model still needs attention, which is exactly what Part 24's "
            "generalized estimating equations do."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=23) if r.part == 23][:4]
        b = coverage_board(rows, lit_part=23, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board, with a thousand samples of forty schools. The iid standard error covers the "
            "programme's true effect forty-nine percent of the time: broken. <bookmark mark='b'/> Cluster-robust: ninety-five, "
            "kept. <bookmark mark='c'/> Now only eight schools. Cluster-robust with t on seven degrees of freedom: eighty-nine, "
            "broken. <bookmark mark='d'/> The wild cluster bootstrap with Webb's weights: ninety-six, kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()
