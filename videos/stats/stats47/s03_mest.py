from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class MEstimators(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.consistency()
        self.normality()
        self.table()
        self.newcomb()
        self.misspec()

    def card(self):
        card = chapter_card(2, r"M- and Z-estimators", r"Maximize an average, \ or solve one", lit=(1964,), part=PART)
        with self.voiceover("Chapter two. M- and Z-estimators: maximize an average, or solve one."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\hat\theta_n", r"=", r"\arg\max_\theta M_n(\theta), \ \ M_n(\theta) = \tfrac1n \textstyle\sum_i m_\theta(X_i)", font_size=32),
            cmath(r"\text{or}", r":", r"\Psi_n(\hat\theta_n) = \tfrac1n \textstyle\sum_i \psi_{\hat\theta_n}(X_i) = 0", font_size=34),
            cmath(r"\text{examples}", r":", r"m = \log p_\theta \ (\text{MLE}); \ \ \psi = x - \theta \ (\text{mean}); \ \ \psi = \mathrm{sign}(x - \theta) \ (\text{median})", font_size=28),
            cmath(r"\text{Huber}", r":", r"\psi_k(u) = \max(-k, \min(k, u))", font_size=34),
        ]
        rows[0][-1].set_color(MLEC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"M for maximum"), why(r"Z for zero"), why(r"one theory for all"), why(r"Huber (1964), \ Part 30")]
        with self.voiceover(
            "<bookmark mark='a'/> Most estimators maximize an average of some criterion over the data: M-estimators, "
            "as Peter Huber named them. <bookmark mark='b'/> Or they solve an average estimating equation: "
            "Z-estimators. <bookmark mark='c'/> The MLE maximizes the average log-likelihood; the mean solves the "
            "average of x minus theta equal to zero; a median minimizes absolute deviations and satisfies a sign "
            "subgradient condition. For a discrete sample, an exact ordinary zero of the sign average need not exist."
            " <bookmark mark='d'/> Huber's estimator from Part thirty uses a psi that is linear near the centre and "
            "flat in the tails. One theory covers them all."
        ) as vo:
            heading=label('M-estimators optimize; Z-estimators solve estimating equations',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def consistency(self):
        rows = [
            cmath(r"\sup_\theta |M_n(\theta) - M(\theta)|", r"\to_P", r"0", font_size=36),
            cmath(r"\sup_{d(\theta, \theta_0) \ge \varepsilon} M(\theta)", r"<", r"M(\theta_0) \ \ \forall \varepsilon > 0", font_size=34),
            cmath(r"M_n(\hat\theta_n)", r"\ge", r"M_n(\theta_0) - o_P(1)", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\hat\theta_n \to_P \theta_0", font_size=36),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a uniform law of large numbers \ (Part 48)"), why(r"a well-separated maximum"), why(r"a near-maximizer suffices"), why(r"Wald (1949); \ van der Vaart Thm 5.7")]
        with self.voiceover(
            "<bookmark mark='a'/> Consistency needs two things. First, the random criterion converges to its expectation "
            "uniformly in theta: a uniform law of large numbers, which Part forty-eight proves for whole classes of "
            "functions. <bookmark mark='b'/> Second, the limit criterion has a well-separated maximum at the truth: "
            "anything a fixed distance away is strictly worse. <bookmark mark='c'/> Then any estimator that nearly "
            "maximizes the random criterion, <bookmark mark='d'/> must be close to the truth with probability tending to one. "
            "Uniform convergence prevents a spurious maximum far away from sneaking in, the failure that Wald's 1949 proof "
            "for the MLE guarded against."
        ) as vo:
            heading=label('Uniform convergence and separation force consistency',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def normality(self):
        rows = [
            cmath(r"0 = \Psi_n(\hat\theta)", r"=", r"\Psi_n(\theta_0) + A_n(\hat\theta-\theta_0), \ \ A_n=\int_0^1\dot\Psi_n(\theta_0+t(\hat\theta-\theta_0))\,dt", font_size=32),
            cmath(r"\sqrt n(\hat\theta - \theta_0)", r"=", r"-V^{-1} \tfrac{1}{\sqrt n}\textstyle\sum \psi_{\theta_0}(X_i) + o_P(1)", font_size=32),
            cmath(r"\phantom{X}", r"\Rightarrow", r"N(0, \ V^{-1} B V^{-\top}), \ \ V = E\dot\psi_{\theta_0}, \ B = E\psi\psi^\top", font_size=30),
            cmath(r"\text{MLE}", r":", r"V = -I, \ B = I \ \Rightarrow \ I^{-1}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(MLEC)
        whys = [why(r"consistent root; \ integrated Jacobian $A_n\to_P V$"), why(r"an average of influence terms"), why(r"the sandwich"), why(r"Part 22, \ proved")]
        with self.voiceover(
            "<bookmark mark='a'/> For a consistent solution, a differentiable estimating equation with a uniformly "
            "convergent Jacobian, nonsingular limiting derivative, and a finite-variance score CLT yields an "
            "asymptotic linear expansion. For a vector equation use an integrated Jacobian; there need not be one "
            "intermediate point that works for every coordinate. <bookmark mark='b'/> Solving it, root n times the "
            "error is minus the inverse of the derivative matrix V, times a normalized sum of independent terms, plus"
            " something negligible. <bookmark mark='c'/> By the central limit theorem and Slutsky, the limit is "
            "normal with the sandwich covariance: V inverse, B, V inverse, where B is the variance of psi. <bookmark "
            "mark='d'/> For the MLE, V is minus the information and B is the information, so the sandwich collapses "
            "to the inverse information: Part twenty-two's statement, now proved, under those conditions. Nonsmooth "
            "quantile scores need a separate stochastic-equicontinuity argument, rather than a literal derivative of "
            "the sample signs."
        ) as vo:
            heading=label('A regular consistent root has a sandwich limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("mest")
        nm, ct = d["normal"], d["contaminated"]
        rows = [[r"errors", r"Huber: \ sandwich", r"Huber: \ simulated", r"mean: \ theory", r"mean: \ simulated"],
                [r"$N(0, 1)$", f"{nm['sandwich']:.3f}", f"{nm['sim_huber']:.3f}", f"{nm['mean_theory']:.3f}", f"{nm['sim_mean']:.3f}"],
                [r"$0.9\,N(0, 1) + 0.1\,N(0, 25)$", f"{ct['sandwich']:.3f}", f"{ct['sim_huber']:.3f}", f"{ct['mean_theory']:.3f}", f"{ct['sim_mean']:.3f}"]]
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.35, colors=[GREY_A, MLEC, HODC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"$n \times$ variance, \ $n = 50$, \ 4,000 samples; \ Huber with $k = 1.345$, \ scale fixed", font_size=24, color=GREY_A),
            label(r"the sandwich predicts the simulation; \ Huber gives up 5\% at the normal \ and gains 2.5 times under contamination", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -1.8, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Check the sandwich against simulation, for Huber's estimator with fifty observations. "
            f"<bookmark mark='b'/> For normal errors the sandwich formula gives {say(nm['sandwich'], 3)} for n times the "
            f"variance, and the simulation {say(nm['sim_huber'], 3)}; the mean's is one. <bookmark mark='c'/> With ten "
            f"percent of the errors five times as spread out, the sandwich gives {say(ct['sandwich'], 2)} and the simulation "
            f"{say(ct['sim_huber'], 2)}, while the mean's variance jumps to {say(ct['sim_mean'], 1)}. <bookmark mark='d'/> "
            f"The formula predicts the finite-sample behaviour well, and it quantifies Huber's bargain: five percent lost at "
            f"the normal, more than half the variance saved under contamination."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated: 4,000 samples; \ sandwich by quadrature")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def newcomb(self):
        d = load("mest")["newcomb"]
        rows = [
            cmath(r"\text{Newcomb (1882)}", r":", rf"{d['n']} \ \text{{passage times of light}}; \ \text{{one at}} \ {d['min']:.0f}", font_size=32),
            cmath(r"\text{mean}", r":", rf"{d['mean']:.2f}, \ \ \text{{SE}} \ {d['se_mean']:.2f}", font_size=34),
            cmath(r"\text{Huber}", r":", rf"{d['huber']:.2f}, \ \ \text{{symmetry-model sandwich SE}} \ {d['se_huber']:.2f}", font_size=34),
            cmath(r"\text{median}", r":", rf"{d['median']:.1f}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Part 30's data"), why(r"pulled down by the outliers"), why(r"half the standard error"), why(r"for comparison")]
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: Simon Newcomb's sixty-six measurements of the passage time of light, one of them a wild {d['min']:.0f}. <bookmark mark='b'/> The mean is {say(d['mean'], 1)}, with a standard error of {say(d['se_mean'], 2)}, dragged down by the outliers. <bookmark mark='c'/> Huber's estimate is {say(d['huber'], 1)}, and its sandwich standard error is {say(d['se_huber'], 2)}, half the mean's. <bookmark mark='d'/> The median, {d['median']:.0f}, agrees with Huber. The sandwich standard error is computed from the data's own psi values, so it is a plug-in asymptotic calculation, not a distribution-free guarantee. Here the scale is estimated by the MAD; symmetry makes its first-order effect on location orthogonal. Without symmetry, joint location-scale uncertainty needs a fuller sandwich. The mean and Huber location can also target different functionals outside a symmetric model."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Newcomb (1882), \ via Stigler (1977)")))
            heading=label('Newcomb contrasts two location targets under model assumptions',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def misspec(self):
        rows = fit_rows(VGroup(
            label(r"with identification and uniform convergence: \ a misspecified MLE can converge to a KL projection", font_size=26),
            label(r"its variance is the sandwich $V^{-1} B V^{-\top}$, \ not $I^{-1}$ \ (Huber 1967; \ White 1982)", font_size=26, color=GOODC),
            label(r"a calibrated information-matrix test can detect some failures of $V=-B$", font_size=26, color=S.ACCENT),
            label(r"Part 23's robust standard errors \ are this theorem, \ applied", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theory does not need the model to be right. Under suitable identification, "
            "uniform convergence, and a well-separated finite maximizer, a misspecified likelihood can converge to "
            "its pseudo-true KL projection. <bookmark mark='b'/> Its variance is the sandwich, not the inverse "
            "information: Huber's result of 1967, made central to econometrics by Halbert White in 1982. <bookmark "
            "mark='c'/> When the model is right, V equals minus B, the information equality; misspecification can "
            "break that equality, although some wrong models still satisfy it. An information-matrix test also needs "
            "its own estimated null distribution. <bookmark mark='d'/> Part twenty-three's robust standard errors are"
            " this theorem, applied to least squares."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
