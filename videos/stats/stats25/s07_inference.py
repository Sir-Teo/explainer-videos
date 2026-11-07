from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats25.common import *  # noqa: F403


class Inference(VoiceoverScene):
    def construct(self):
        self.card()
        self.df()
        self.board()
        self.boundary_theory()
        self.boundary_sim()
        self.profile()
        self.advice()

    def card(self):
        card = chapter_card(6, r"Inference", r"Degrees of freedom, \ and tests on the edge", lit=(1987,), part=PART)
        with self.voiceover("Chapter six. Inference for mixed models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def df(self):
        rows = [
            cmath(r"(c^\top\hat\beta - c^\top\beta)/\widehat{\mathrm{SE}}", r"\approx", r"t_\nu \ \text{for some } \nu", font_size=30),
            cmath(r"\nu", r"=", r"\dfrac{2\,\mathrm{Var}(c^\top\hat\beta)^2}{\mathrm{Var}\{\widehat{\mathrm{Var}}(c^\top\hat\beta)\}}", font_size=30),
            cmath(r"\text{balanced, \ between groups}", r":", r"\nu = G-\mathrm{rank}(X_{\rm between})", font_size=30),
            cmath(r"\text{Kenward--Roger}", r":", r"\text{also corrects the SE's own bias}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"the SE is estimated from the variance components"), why(r"Satterthwaite (1946): \ match two moments"),
                why(r"the number of groups, \ not of pupils"), why(r"Kenward \& Roger (1997)")]
        intro = label('Few-group fixed-effect inference needs an approximate reference law', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The standard error of a fixed effect depends on estimated variance components, so "
            "the ratio of estimate to standard error isn't normal; it's roughly a t with some degrees of freedom nu. "
            "<bookmark mark='b'/> Franklin Satterthwaite's 1946 recipe chooses nu so that the estimated variance has "
            "the right mean and variance for a chi-squared, computing the latter by the delta method. <bookmark "
            "mark='c'/> For a balanced design and an effect that varies between groups, it gives the number of groups"
            " minus the rank of the between-group fixed-effect design. Within-group predictors need not each cost a "
            "group degree of freedom. <bookmark mark='d'/> Michael Kenward and James Roger's refinement also adjusts "
            "the covariance estimate and the F scaling as well as approximating degrees of freedom."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=25) if r.part == 25][2:4]
        b = coverage_board(rows, lit_part=25, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: eight schools of twenty-five pupils, four with a treatment, and the treatment "
            "effect estimated by a mixed model. With the normal distribution's one point nine six, the intervals cover "
            "eighty-nine percent of the time: broken. <bookmark mark='b'/> With Satterthwaite's t, about six degrees of "
            "freedom here, they cover ninety-four: kept. Two hundred pupils, but only eight schools."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()

    def boundary_theory(self):
        rows = [
            cmath(r"H_0", r":", r"\tau^2 = 0 \ \text{on the edge of } [0, \infty)", font_size=30),
            cmath(r"\hat\tau^2", r"=", r"0 \ \text{about half the time under } H_0", font_size=30),
            cmath(r"2\{\ell_1 - \ell_0\}", r"\to", r"\tfrac12\chi^2_0 + \tfrac12\chi^2_1", font_size=32),
            cmath(r"\text{in practice}", r":", r"LR>0:\ p=\tfrac12 P(\chi^2_1\ge LR);\quad LR=0:\ p=1", font_size=28),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"Part 22, \ chapter nine"), why(r"a negative estimate is truncated"),
                why(r"Self \& Liang (1987)"), why(r"the naive test is conservative")]
        intro = label('One regular variance boundary yields a limiting mixture law', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Testing whether a variance component is zero puts the hypothesis on the edge of the"
            " parameter space, the situation of Part 22's chapter nine. <bookmark mark='b'/> Under the null, the "
            "estimate is exactly zero about half the time, whenever the data happen to look less clustered than "
            "independent noise. <bookmark mark='c'/> With one added variance, other nuisance parameters identifiable "
            "and interior, and many independent groups, the limiting ratio is zero half the time and chi-squared with"
            " one degree of freedom otherwise: a fifty-fifty mixture, as Steven Self and Kung-Yee Liang showed in "
            "1987. <bookmark mark='d'/> For a positive statistic halve the chi-squared upper-tail p-value; at zero "
            "use p equal to one. The asymptotic five-percent critical value is two point seven one rather than three "
            "point eight four."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def boundary_sim(self):
        d = load("boundary")
        lr = np.asarray(d["lr"])
        pos = lr[lr > 1e-6]
        edges = np.linspace(0, 8, 33)
        h, _ = np.histogram(pos, edges)
        h = h / len(lr) / (edges[1] - edges[0])
        A = axes([-0.6, 8], [0, 0.8], x_length=8.0, y_length=4.2, xlabel=r"$2 \times$ log likelihood ratio, \ $\tau^2 = 0$ true",
                 ylabel=r"density", xticks=[0, 2, 4, 6, 8], yticks=[0, 0.4, 0.8], center=[-1.6, 0.3, 0])
        ax = A.ax
        spike = VGroup(Arrow(ax.c2p(0, 0.65), ax.c2p(0, 0.02), color=RES, buff=0), label(r"atom at zero (mass, not density)", font_size=18, color=RES).move_to(ax.c2p(2.3, 0.7)))
        bars = hist_bars(ax, edges, h, color=MODEL, opacity=0.6)
        gr = np.linspace(0.08, 8, 200)
        c = curve(ax, gr, 0.5 * stats.chi2.pdf(gr, 1), TRUE, 3)
        rows = fit_rows(VGroup(
            label(r"1,000 data sets, \ 20 groups of 10, \ no group effect", font_size=22),
            label(rf"red: \ near 0 (tolerance $10^{-6}$), \ {100 * d['zero_share']:.0f}\% of the time", font_size=22, color=RES),
            label(r"gold: \ $\tfrac12\chi^2_1$", font_size=22, color=TRUE),
            label(rf"reject at 3.84: \ {100 * d['reject_chi1']:.1f}\%; \ at 2.71: \ {100 * d['reject_mix']:.1f}\%", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A thousand simulated data sets with no group effect at all. <bookmark mark='b'/> In"
            " fifty-eight percent the likelihood ratio is numerically near zero, a little more than half, as is usual"
            " in small samples. <bookmark mark='c'/> The continuous part is compared with the asymptotic "
            "half-chi-squared density; the finite-sample fit need not be exact. <bookmark mark='d'/> The textbook "
            "cut-off of three point eight four rejects only two percent of the time, far too rarely; the mixture's "
            "two point seven one rejects three point three percent, closer to the nominal five. A null simulation can"
            " improve finite-sample calibration. Plug-in parametric bootstrap is generally approximate; exact "
            "simulation requires a known or pivotal null law."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(spike, DOWN), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), Create(c), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"fixed effects: \ Satterthwaite or Kenward--Roger $t$, \ not $z$", font_size=24, color=HIT),
            label(r"variance components: \ profile-likelihood intervals, \ or the bootstrap", font_size=24),
            label(r"testing $\tau^2 = 0$: \ the 50:50 mixture, \ or a parametric bootstrap", font_size=24, color=PATH),
            label(r"few groups: \ every approximation strains; \ Part 26's Bayes helps", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: for fixed effects, use Satterthwaite or Kenward–Roger t intervals rather than "
            "z. <bookmark mark='b'/> For the variance components themselves, use profile-likelihood intervals or the "
            "bootstrap, since their sampling distributions are skewed. <bookmark mark='c'/> To test a variance at "
            "zero, use the mixture or a parametric bootstrap. <bookmark mark='d'/> And with very few groups, every "
            "approximation strains; a Bayesian analysis with a sensible prior on the variance, Part 26's subject, can"
            " help, with prior sensitivity especially important when there are very few groups."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def profile(self):
        rows = [
            cmath(r"\ell_p(\tau)", r"=", r"\max_{\beta, \sigma} \ell(\beta, \sigma, \tau)", font_size=30),
            cmath(r"\text{usual profile interval}", r":", r"\{\tau : 2\{\ell_p(\hat\tau) - \ell_p(\tau)\} \le 3.84\}", font_size=30),
            cmath(r"\text{Wald}", r":", r"\hat\tau \pm 1.96\,\mathrm{SE}: \ \text{symmetric, \ can go below } 0", font_size=30),
            cmath(r"\text{profile}", r":", r"\text{asymmetric; \ may reach } 0 \text{, honestly}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"Part 22's profile likelihood"), why(r"invert the likelihood ratio test"),
                why(r"a variance's sampling distribution is skewed"), why(r"lme4's \texttt{confint}")]
        intro = label('Regular profile cutoffs need separate calibration near a boundary', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For the variance components themselves, use Part 22's profile likelihood: maximize "
            "over everything else for each value of tau. <bookmark mark='b'/> The displayed usual profile interval "
            "uses the regular interior chi-squared cutoff. Boundary calibration can differ; this is not universally "
            "exact ninety-five-percent coverage. <bookmark mark='c'/> A Wald interval, estimate plus or minus two "
            "standard errors, is symmetric and with few groups can run below zero, which is meaningless for a "
            "standard deviation. <bookmark mark='d'/> The profile interval is asymmetric, longer on the high side, "
            "and when the data are compatible with no group variation it says so by reaching zero."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
