from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class HeavyTails(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. Heavy tails in high dimensions: median-of-means tournaments.", 4,
                            r"Heavy tails in high dimensions", r"Sub-Gaussian with two moments", lit=(2019,))
        self.problem()
        self.mom()
        self.delta()
        self.chart()
        self.tournaments()
        self.catoni()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A different threat: no adversary, but heavy tails. If the data have only a finite variance, "
            "the sample mean's deviations are controlled only by Chebyshev's inequality. <bookmark mark='b'/> To be within t of "
            "the truth with probability one minus delta, the mean needs n of order one over delta: <bookmark mark='c'/> a "
            "polynomial dependence on the confidence, where Gaussian data give a logarithm. <bookmark mark='d'/> Can an "
            "estimator do as well, for heavy-tailed data, as the mean does for Gaussian data?",
            [(r"\text{finite variance only}", r":", r"P(|\bar X - \mu| > t) \le \sigma^2/(nt^2)", 40),
             (r"\text{confidence } 1 - \delta", r":", r"\text{width} \propto \sigma\sqrt{1/(n\delta)}", 40),
             (r"\text{Gaussian}", r":", r"\text{width} \propto \sigma\sqrt{\log(1/\delta)/n}", 40),
             (r"\text{question}", r":", r"\text{the Gaussian rate with two moments?}", 40)],
            [r"Chebyshev", r"polynomial in $1/\delta$", r"logarithmic", r"yes"],
            colors=[(1, NAIVEC), (2, FIXC)])

    def mom(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The median of means, from Nemirovski and Yudin, and Alon, Matias and Szegedy: split the data "
            "into k blocks, average each, and take the median of the averages. <bookmark mark='b'/> Each block mean is within "
            "two sigma root of k over n of the truth with probability at least three quarters, by Chebyshev. <bookmark "
            "mark='c'/> The median fails only if half the blocks fail, which by Hoeffding has probability e to the minus k "
            "over eight. <bookmark mark='d'/> With k of order log one over delta, the median of means has the Gaussian width, "
            "for any finite-variance distribution: Part thirty's robust estimators, in their sharpest form.",
            [(r"\text{MoM}", r"=", r"\mathrm{median}(\bar X_1, \dots, \bar X_k)", 40),
             (r"\text{each block}", r":", r"|\bar X_j - \mu| \le 2\sigma\sqrt{k/n} \ \text{w.p.} \ge \tfrac34", 40),
             (r"\text{the median fails}", r":", r"\text{w.p.} \le e^{-k/8}", 40),
             (r"k \asymp \log(1/\delta)", r":", r"\text{width} \asymp \sigma\sqrt{\log(1/\delta)/n}", 40)],
            [r"Nemirovski \& Yudin; \ Alon et al.", r"Chebyshev per block", r"Hoeffding over blocks", r"the Gaussian rate"],
            colors=[(3, FIXC)])

    def chart(self):
        d = load("heavy")
        em, eg = np.asarray(d["mean_err"]), np.asarray(d["mom_err"])
        A = axes([0.2, 0.9], [-2.7, 0], x_length=7.4, y_length=4.4, xlabel=r"error $t$", ylabel=r"fraction of samples with error $> t$",
                 xticks=[0.2, 0.4, 0.6, 0.8], yticks=[0, -1, -2], yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax

        def exceed(e, c):
            e = np.sort(e)
            m = len(e)
            ts = np.linspace(0.2, 0.9, 300)
            fr = np.array([np.sum(e > t) / m for t in ts])
            keep = fr > 0
            return polyline(ax, ts[keep], np.log10(fr[keep]), c, 4)
        h1, h2 = exceed(em, NAIVEC), exceed(eg, FIXC)
        lvl = DashedLine(ax.c2p(0.2, -2), ax.c2p(0.9, -2), color=GREY_B, stroke_width=1.5)
        mq, gq = d["mean_q"], d["mom_q"]
        side = side_groups([
            [(rf"$n = {d['n']}$, \ $d = {d['d']}$", WHITE), (rf"Student $t$, \ {d['df']:g} d.f.", WHITE)],
            [(r"red: \ the sample mean", NAIVEC), (rf"99th percentile {mq[2]:.3f}", NAIVEC)],
            [(rf"green: \ median of {d['k']} block means", FIXC), (rf"99th percentile {gq[2]:.3f}", FIXC)],
            [(rf"medians {mq[0]:.3f} \ vs \ {gq[0]:.3f}", GREY_A), (r"the tails differ most", GREY_A)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> In twenty dimensions, with Student t data of two and a half degrees of freedom, whose "
            f"variance is finite but whose tails are heavy. The curves show, for each error t, the fraction of four hundred "
            f"samples whose error exceeds it, on a log scale. <bookmark mark='b'/> The sample mean's curve, in red, falls "
            f"slowly: one sample in a hundred, the dashed line, has error above {say(mq[2], 3)}. <bookmark mark='c'/> The median of {d['k']} block means, "
            f"with the geometric median for the vector case, falls much faster: its one-in-a-hundred error is {say(gq[2], 3)}. <bookmark "
            f"mark='d'/> Their typical errors differ less, {say(mq[0], 3)} against {say(gq[0], 3)}: the gain is in the tail, which "
            f"illustrates upper-tail behavior. The empirical ninety-ninth percentile uses only about four tail observations among four hundred; its order-statistic uncertainty is recorded with the computation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 400 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(h1), Create(lvl), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(h2), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tournaments(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In high dimensions, the geometric median of block means is good but not optimal: its width "
            "has the wrong dependence on the covariance. <bookmark mark='b'/> Gábor Lugosi and Shahar Mendelson's median-of-means "
            "tournament, in 2019, compares every pair of candidate means block by block, and keeps those that win most of "
            "their matches. <bookmark mark='c'/> The winner's error is the trace of the covariance over n, plus the top "
            "eigenvalue times log one over delta over n, under roots: exactly the Gaussian sample mean's. <bookmark mark='d'/> "
            "Sam Hopkins found a polynomial-time version through sum-of-squares, in 2020.",
            [(r"\text{geometric MoM}", r":", r"\text{good; \ not optimal in } \Sigma", 40),
             (r"\text{tournament}", r":", r"\text{pairwise matches, \ block by block}", 40),
             (r"\text{error}", r"\lesssim", r"\sqrt{\operatorname{tr}\Sigma/n} + \sqrt{\|\Sigma\|\log(1/\delta)/n}", 38),
             (r"\text{efficient}", r":", r"\text{Hopkins (2020), \ by sum-of-squares}", 40)],
            [r"Minsker (2015)", r"Lugosi \& Mendelson (2019)", r"the Gaussian rate", r"polynomial time"],
            colors=[(2, FIXC)])

    def catoni(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Catoni's scalar estimator uses a smoothed estimating equation. Near-optimal constants require the theorem's variance information, tuning and confidence range. <bookmark mark='b'/> Extensions to regression and covariance estimation require their own moment and structural assumptions. <bookmark mark='c'/> Median-of-means methods can also resist adversarial observations, provided enough blocks remain clean: the block count must account for the number of corrupted points as well as the confidence level. A fixed thirty-block choice does not resist an arbitrary fraction at every sample size. <bookmark mark='d'/> Heavy-tail and contamination guarantees can be combined when these conditions are made explicit.",
            [(r"\text{Catoni}", r":", r"\text{near-optimal constants under scale/tuning conditions}", 40),
             (r"\text{extensions}", r":", r"\text{regression, \ covariance}", 40),
             (r"\text{combined}", r":", r"\text{heavy tails and outliers together}", 40),
             (r"\text{so}", r":", r"\text{one theory}", 40)],
            [r"Part 30", r"Lugosi \& Mendelson's survey", r"block medians", r"unification"],
            colors=[(3, FIXC)])

    def delta(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Median of means tunes its block count to a requested confidence level, with at most n nonempty blocks. <bookmark mark='b'/> Devroye, Lerasle, Lugosi and Oliveira distinguish this from a single estimator with guarantees at many confidence levels. <bookmark mark='c'/> Over the full class of finite-variance laws, without further scale information, that stronger property is impossible. Known variance, or variance known within fixed factors, changes the answer. <bookmark mark='d'/> Bounded kurtosis also permits multiple-confidence estimators over stated ranges. Near-optimal constants require a smaller range than a blanket claim down to exponential minus n; the constants and kurtosis bound enter the theorem.",
            [(r"k \asymp \log(1/\delta)", r":", r"\text{one estimator per confidence level}", 40),
             (r"\text{question}", r":", r"\text{one estimator for every } \delta?", 40),
             (r"\text{two moments}", r":", r"\text{full finite-variance class: \ no multiple-}\delta\text{ estimator}", 40),
             (r"\text{bounded kurtosis}", r":", r"\text{yes, \ with theorem-specific constants and range}", 40)],
            [r"a tuned estimator", r"Devroye et al. (2016)", r"an impossibility", r"a little more assumed"],
            colors=[(2, NAIVEC), (3, FIXC)])
