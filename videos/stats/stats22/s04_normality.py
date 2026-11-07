from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats22.common import *  # noqa: F403


class Normality(VoiceoverScene):
    def construct(self):
        self.card()
        self.expand()
        self.limit()
        self.cauchy()
        self.efficiency()

    def card(self):
        card = chapter_card(3, r"Asymptotic normality", r"Expand the score", part=PART)
        with self.voiceover("Chapter three. Asymptotic normality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def expand(self):
        rows = [
            cmath(r"0 = U_n(\hat\theta)", r"\approx", r"U_n(\theta_0) + (\hat\theta - \theta_0)\, U_n'(\theta_0)", font_size=30),
            cmath(r"\sqrt n(\hat\theta - \theta_0)", r"\approx", r"\dfrac{U_n(\theta_0)/\sqrt n}{-U_n'(\theta_0)/n}", font_size=30),
            cmath(r"\text{numerator}", r"\to", r"N\big(0, I(\theta_0)\big)", font_size=30),
            cmath(r"\text{denominator}", r"\to", r"I(\theta_0)", font_size=30),
        ]
        rows[1][2].set_color(LIK)
        whys = [why(r"a Taylor step: \ consistency puts $\hat\theta$ near $\theta_0$"), why(r"solve for the error"),
                why(r"the CLT: \ a sum of mean-zero scores"), why(r"the LLN: \ an average of $-\partial^2 \log f$")]
        intro = label('Expand the score around a consistent interior solution', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Now the second promise. <bookmark mark='a'/> At a consistent interior differentiable maximum the score "
            "is zero; nonsingular information and local derivative bounds control the expansion. Since consistency "
            "puts the estimate near the truth, expand the score around the truth to first order: zero equals the "
            "score at theta zero plus the error times the score's slope. <bookmark mark='b'/> Solve for the error and"
            " scale by root n: a ratio. <bookmark mark='c'/> The numerator is a sum of independent scores, each with "
            "mean zero and variance I, divided by root n, so by the central limit theorem it's approximately normal "
            "with variance I. <bookmark mark='d'/> The denominator is an average of minus second derivatives, so by "
            "the law of large numbers it converges to I itself."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def limit(self):
        rows = [
            cmath(r"\sqrt n(\hat\theta - \theta_0)", r"\to", r"\frac{N(0, I)}{I} = N\big(0, I(\theta_0)^{-1}\big)", font_size=32),
            cmath(r"\text{in practice}", r":", r"\hat\theta \approx N\big(\theta_0, 1/(n\,I(\hat\theta))\big)", font_size=30),
            cmath(r"\text{the remainder}", r":", r"\text{controlled by the third derivative}", font_size=28),
            cmath(r"\text{many parameters}", r":", r"\sqrt n(\hat\theta - \theta_0) \to N\big(0, I(\theta_0)^{-1}\big), \ \text{a matrix}", font_size=28),
        ]
        rows[0][2].set_color(HIT)
        whys = [why(r"Slutsky: \ a normal divided by a constant"), why(r"plug in the estimate"),
                why(r"regularity condition 3"), why(r"the same algebra with vectors")]
        intro = label('Nonsingular information determines asymptotic variance', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> A normal divided by a constant is normal, by Slutsky's theorem: root n times the error "
            "converges to a normal with variance one over the information. <bookmark mark='b'/> In practice we plug in the "
            "estimate, which gives Part 9's approximation. <bookmark mark='c'/> The remainder we dropped in the expansion is "
            "kept small by the bound on the third derivative, the third regularity condition. <bookmark mark='d'/> With "
            "several parameters the same algebra runs with vectors and matrices: the inverse of the information matrix is the "
            "asymptotic covariance."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cauchy(self):
        d = load("asymp")
        mle, med = np.asarray(d["mle"]), np.asarray(d["med"])
        edges = np.linspace(-1, 1, 41)
        hm, _ = np.histogram(mle, edges)[0] / (len(mle) * np.diff(edges)), edges
        hd, _ = np.histogram(med, edges)[0] / (len(med) * np.diff(edges)), edges
        A = axes([-1, 1], [0, 2.4], x_length=8.2, y_length=4.4, xlabel=r"estimate of the centre (truth 0)", ylabel=r"density",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 1, 2], center=[-1.5, 0.3, 0])
        ax = A.ax
        bm = hist_bars(ax, edges, hm, color=MLE_C, opacity=0.55)
        bd = hist_bars(ax, edges, hd, color=GREY_B, opacity=0.35)
        gr = np.linspace(-1, 1, 200)
        nc = curve(ax, gr, stats.norm.pdf(gr, 0, d["theory_mle"]), TRUE, 3)
        rows = fit_rows(VGroup(
            label(rf"{d['R']:,} samples of {d['n']}; \ histogram restricted to $[-1,1]$", font_size=22),
            label(rf"grey: \ the median, \ SD {d['sd_med']:.3f} \ (theory {d['theory_med']:.3f})", font_size=22, color=GREY_B),
            label(rf"blue: \ the MLE, \ SD {d['sd_mle']:.3f} \ (theory {d['theory_mle']:.3f})", font_size=22, color=MLE_C),
            label(r"gold: \ $N(0, 1/(nI))$, \ $I = 1/2$", font_size=22, color=TRUE),
            label(r"raw Cauchy: no moments; \ estimator: approximately normal", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A demanding test: the Cauchy distribution, which has no mean and no variance, so "
            "the sample average is useless. Four thousand samples of fifty, estimating the centre. <bookmark "
            "mark='b'/> The sample median, in grey, has a standard deviation of point two three, near its theory. "
            "<bookmark mark='c'/> The maximum likelihood estimate, found by Newton's method from the median, does "
            "better: point two oh eight. <bookmark mark='d'/> The Cauchy's information is one half per observation, "
            "so the theory says point two oh, and the gold normal curve is what we see. <bookmark mark='e'/> The raw "
            "observations lack a variance, but the regular location estimator has an approximately normal sampling "
            "distribution here and asymptotic efficiency."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bd], lag_ratio=0.02), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bm], lag_ratio=0.02), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(nc), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def efficiency(self):
        rows = [
            cmath(r"\text{Cram\'er--Rao}", r":", r"\mathrm{Var}(T) \ge 1/(n\,I) \ \text{for regular unbiased } T", font_size=30),
            cmath(r"\text{the MLE}", r":", r"\text{attains it, \ asymptotically}", font_size=30),
            cmath(r"\text{Cauchy}", r":", rf"\text{{median / MLE variance}} \approx {(load('asymp')['sd_med'] / load('asymp')['sd_mle']) ** 2:.2f}", font_size=30),
            cmath(r"\text{fine print}", r":", r"\text{Hodges's superefficient estimator; \ Part 47}", font_size=28),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"Part 9"), why(r"no regular estimator does better"), why(r"the median wastes about 20\% of the data"),
                why(r"better at one point, \ worse nearby")]
        intro = label('Efficiency is a regular asymptotic comparison', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Part 9's Cramér–Rao bound says no unbiased estimator can have variance below one "
            "over n I. <bookmark mark='b'/> The maximum likelihood estimator reaches it in the limit: it is "
            "asymptotically efficient. <bookmark mark='c'/> For the Cauchy, the median's variance is about twenty-two"
            " percent larger, so using the median wastes about a fifth of the data. <bookmark mark='d'/> The fine "
            "print: Joseph Hodges constructed a biased estimator whose limiting variance beats the regular asymptotic"
            " benchmark at a point, at the price of doing worse nearby; Part 47 explains why such estimators are "
            "ruled out by asking for regularity."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
