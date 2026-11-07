from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403


class Summaries(VoiceoverScene):
    def construct(self):
        self.card()
        self.centres()
        self.losses()
        self.intervals()
        self.invariance()
        self.laplace_approx()
        self.reading()

    def card(self):
        card = chapter_card(3, r"Summaries", r"Point estimates and credible intervals from a posterior", part=PART)
        with self.voiceover("Chapter three. Summaries."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes_beta(self, center=(-2.2, 0.2, 0)):
        A = axes([0, 0.7], [0, 5], x_length=7.4, y_length=4.2, xlabel=r"$p$", ylabel=r"posterior density", xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                 yticks=[0, 2, 4], center=list(center))
        return A, A.ax

    def centres(self):
        d = load("summaries")
        A, ax = self.axes_beta()
        xs = np.linspace(0, 0.7, 400)
        f = stats.beta(3, 12).pdf(xs)
        po = density(ax, xs, f, POST)
        marks = VGroup()
        cols = [(d["mode"], r"mode", S.ALT), (d["median"], r"median", S.LIK), (d["mean"], r"mean", OBS)]
        for k, (v, nm, c) in enumerate(cols):
            h = stats.beta(3, 12).pdf(v)
            marks.add(VGroup(DashedLine(ax.c2p(v, 0), ax.c2p(v, h), color=c, stroke_width=3),
                             label(nm, font_size=20, color=c).move_to(ax.c2p(v, h) + UP * (0.25 + 0.3 * k))))
        rows = fit_rows(VGroup(
            label(r"2 successes in 13 trials, \ uniform prior: \ Beta(3, 12)", font_size=24),
            MathTex(rf"\text{{mode}}\ {d['mode']:.3f}", font_size=28, color=S.ALT),
            MathTex(rf"\text{{median}}\ {d['median']:.3f}", font_size=28, color=S.LIK),
            MathTex(rf"\text{{mean}}\ {d['mean']:.3f}", font_size=28, color=OBS),
            label(r"a skewed posterior has three different centres", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "The posterior is the full answer, but we usually want summaries. <bookmark mark='a'/> Take two successes in thirteen "
            "trials with a uniform prior: Beta three twelve, skewed to the right. <bookmark mark='b'/> Its peak, the mode, is "
            "at point one five four; that's also the maximum-likelihood estimate's Bayesian twin, since with a flat prior the "
            "posterior is the likelihood. <bookmark mark='c'/> The median, splitting the probability in half, is at point one "
            "eight six. <bookmark mark='d'/> The mean, the balance point, is at point two. <bookmark mark='e'/> For a skewed "
            "posterior the three differ. Which one should you report?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(po))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(marks[k][0]), FadeIn(marks[k][1]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def losses(self):
        rows = [
            cmath(r"\text{choose } a \text{ to minimize}", r"\ ", r"\mathbb E\big[L(\theta, a) \mid y\big]", font_size=32),
            cmath(r"L = (\theta - a)^2", r"\Rightarrow", r"a = \text{posterior mean}", font_size=32),
            cmath(r"L = |\theta - a|", r"\Rightarrow", r"a = \text{posterior median}", font_size=32),
            cmath(r"L = \mathbb 1\{|\theta - a| > \epsilon\},\ \epsilon \to 0", r"\Rightarrow", r"a = \text{posterior mode}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"decision theory: \ the posterior expected loss"), why(r"Part 9's MSE, \ averaged over belief"),
                why(r"the same argument as for the sample median (Part 1)"), why(r"``maximum a posteriori'' (MAP)")]
        intro = label('Choose the estimate using posterior expected loss', font_size=36)
        with self.voiceover(
            "The answer depends on what an error costs. <bookmark mark='a'/> Choose the estimate that minimizes the expected "
            "loss under the posterior. <bookmark mark='b'/> If the loss is the squared error, as in Part 9's mean squared error, "
            "the best estimate is the posterior mean. <bookmark mark='c'/> If it's the absolute error, the posterior median, by "
            "the same argument that made the median minimize absolute deviations in Part 1. <bookmark mark='d'/> And if you only "
            "care about being within a shrinking symmetric tolerance, a regular posterior mode is the limiting choice. Exact zero-one loss is uninformative for a continuous posterior, since every single point has probability zero. That limiting choice is the maximum a posteriori estimate. The posterior is shared; the "
            "summary is a decision."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def intervals(self):
        d = load("summaries")
        A, ax = self.axes_beta(center=(-2.2, 1.1, 0))
        xs = np.linspace(0, 0.7, 400)
        dist = stats.beta(3, 12)
        f = dist.pdf(xs)
        cv = curve(ax, xs, f, POST, 3)
        lo, hi = d["et"]
        h0, h1 = d["hpd"]
        m1 = (xs >= lo) & (xs <= hi)
        m2 = (xs >= h0) & (xs <= h1)
        et = shade(ax, xs[m1], f[m1], S.ALT, 0.35)
        hp = shade(ax, xs[m2], f[m2], OBS, 0.45)
        lev = DashedLine(ax.c2p(0, dist.pdf(h0)), ax.c2p(0.7, dist.pdf(h0)), color=OBS, stroke_width=2)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{equal-tailed:}}\ [{lo:.3f},\ {hi:.3f}]", font_size=28, color=S.ALT),
            label(r"2.5\% cut from each tail", font_size=22),
            MathTex(rf"\text{{HPD:}}\ [{h0:.3f},\ {h1:.3f}]", font_size=28, color=OBS),
            label(r"the shortest 95\% interval: \ every point inside is more plausible than every point outside", font_size=22),
            label(rf"widths: \ {hi - lo:.3f} \ vs \ {h1 - h0:.3f}", font_size=22, color=GREY_A),
        ), 12.4, 0.16, [0, -2.65, 0])
        with self.voiceover(
            "Intervals. <bookmark mark='a'/> The simplest ninety-five percent credible interval cuts two and a half percent of "
            "the posterior probability from each tail: from point oh four seven to point four two eight. <bookmark mark='b'/> "
            "But for a skewed posterior, that interval includes values in the long right tail that are less plausible than "
            "values it excludes on the left. <bookmark mark='c'/> The highest posterior density interval fixes this: lower a "
            "horizontal line until the region above it holds ninety-five percent. Every point inside is more plausible than "
            "every point outside, and it's the shortest ninety-five percent interval: from point oh two nine to point three nine "
            "five. <bookmark mark='d'/> Here it's about four percent shorter."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(et), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.wait(0.3)
            vo.wait_until("c")
            self.play(FadeOut(et), FadeIn(hp), Create(lev), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def invariance(self):
        d = load("summaries")
        lo, hi = d["et"]
        rows = [
            cmath(r"g \text{ increasing}", r":", r"P(\theta \in [l, u]) = P(g(\theta) \in [g(l), g(u)])", font_size=30),
            cmath(r"\text{odds, \ equal-tailed}", r":", rf"[{lo / (1 - lo):.3f},\ {hi / (1 - hi):.3f}]", font_size=30),
            cmath(r"\text{HPD}", r":", r"\text{not invariant: \ the odds' HPD is a different interval}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{equal-tailed for reporting; \ HPD for skewed, \ one-scale summaries}", font_size=30),
        ]
        rows[1][2].set_color(S.ALT)
        whys = [why(r"quantiles map through monotone functions"), why(r"just transform the endpoints"),
                why(r"densities change by the Jacobian (Part 5)"), why(r"a convention, \ stated")]
        intro = label('Credible intervals depend on the reporting scale', font_size=36)
        with self.voiceover(
            "There's a trade-off. <bookmark mark='a'/> Quantiles pass through any increasing transformation, so the "
            "equal-tailed interval for the odds is just the equal-tailed interval for p, with its endpoints transformed. "
            "<bookmark mark='b'/> Here, odds from point oh four nine to point seven four nine. <bookmark mark='c'/> The HPD "
            "interval doesn't transform that way: densities pick up a Jacobian, Part 5's, so the most plausible region for the "
            "odds isn't the image of the most plausible region for p. <bookmark mark='d'/> Equal-tailed intervals are the "
            "usual default for reporting; HPD intervals minimize length for this unimodal posterior on the scale you care about. "
            "Either way, say which."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def reading(self):
        rows = fit_rows(VGroup(
            label(r"``given the data and the prior, \ $P(0.047 < p < 0.428) = 0.95$''", font_size=26, color=POST),
            label(r"a statement about $p$, \ conditional on what was actually observed", font_size=24),
            label(r"a confidence interval's 95\% is a statement about the procedure", font_size=24, color=S.ALT),
            label(r"they often nearly agree: \ chapter nine checks when", font_size=24, color=OBS),
            label(r"regular identifiable models: posterior SD often shrinks like $1/\sqrt n$", font_size=22, color=GREY_A),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A credible interval reads the way people want an interval to read: given these data and this "
            "prior, the probability that p lies between point oh four seven and point four two eight is ninety-five percent. "
            "<bookmark mark='b'/> It's conditional on what was actually observed, not on imagined repetitions. "
            "<bookmark mark='c'/> A confidence interval's ninety-five percent describes the procedure that made it. "
            "<bookmark mark='d'/> They're different promises, and yet they often nearly agree, numerically; chapter nine checks "
            "when, on the Coverage Board. <bookmark mark='e'/> Under regular finite-dimensional identifiable models with a prior positive near the truth, posterior width typically shrinks like one over root n. Boundaries, nonidentification and other irregular cases can differ."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def laplace_approx(self):
        rows = [
            cmath(r"\log\pi(\theta \mid y)", r"\approx", r"\log\pi(\hat\theta \mid y) - \tfrac12 J(\hat\theta)(\theta - \hat\theta)^2", font_size=30),
            cmath(r"\pi(\theta \mid y)", r"\approx", r"N\big(\hat\theta,\ J(\hat\theta)^{-1}\big)", font_size=34),
            cmath(r"\text{Beta}(3, 12)", r":", r"N(0.154,\ 0.100^2)\ \text{vs the exact SD } 0.100", font_size=30),
            cmath(r"\text{large } n", r":", r"\text{the posterior is nearly normal, \ centred at the MLE}", font_size=30),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"a quadratic at the mode: \ Laplace (1774)"), why(r"$J$: \ the curvature, \ Part 9's observed information"),
                why(r"close here, \ though it misses the skew"), why(r"Bernstein--von Mises (Part 53)")]
        intro = label('Approximate the log posterior near its mode', font_size=36)
        with self.voiceover(
            "One more summary, Laplace's own. <bookmark mark='a'/> Expand the log posterior to second order around its peak: a "
            "quadratic, with curvature J. <bookmark mark='b'/> Then the posterior is approximately normal, centred at the mode, "
            "with variance one over the curvature: Part 9's observed information, now as a posterior variance. "
            "<bookmark mark='c'/> For Beta three twelve the approximating normal has standard deviation point one oh, matching "
            "the exact posterior's, though it misses the skew and puts some mass below zero. <bookmark mark='d'/> Under Bernstein-von Mises regularity, including local identifiability and a suitable prior near the truth, the posterior approaches a normal centred near the maximum-likelihood estimate, with the "
            "inverse information as its variance. That's why Bayesian and likelihood intervals agree in large samples."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
