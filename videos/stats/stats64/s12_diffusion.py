from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Diffusion(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eleven. Generative models are density estimators: Tweedie's formula inside diffusion.", 11,
                            r"Generative models as estimators", r"Denoising is Bayes")
        self.idea()
        self.tweedie_()
        self.tweedie_chart()
        self.sampler()
        self.memorize()
        self.chart()
        self.rates()

    def idea(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A diffusion model generates images by starting from noise and removing it step by step. "
            "<bookmark mark='b'/> Forward: add Gaussian noise to a data point, more and more, until nothing of it is left. "
            "<bookmark mark='c'/> Backward: learn to undo a little noise at each level, and run the chain in reverse. "
            "<bookmark mark='d'/> Everything the model learns is one function, the score: the gradient of the log density of "
            "the noised data at each noise level. A generative model is a density estimator, Part twenty-nine's subject, "
            "in disguise.",
            [(r"\text{forward}", r":", r"y = x + \sigma Z", 40),
             (r"\text{backward}", r":", r"\text{undo noise, \ level by level}", 40),
             (r"\text{learned}", r":", r"s(y, \sigma) = \nabla_y \log p_\sigma(y)", 40),
             (r"\text{so}", r":", r"\text{a density estimator}", 40)],
            [r"Sohl-Dickstein et al. (2015)", r"noising", r"Song \& Ermon (2019); \ Ho et al. (2020)", r"Part 29"],
            colors=[(2, JUDGEC)])

    def tweedie_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The link to statistics is Part twenty-five's Tweedie formula. <bookmark mark='b'/> If y is x plus normal noise of variance sigma squared, the posterior mean of x given y is y plus sigma squared times the score of y's marginal density. <bookmark mark='c'/> So learning the score is learning the Bayes denoiser, and the training loss, denoising score matching, is the mean squared error of a denoiser, Part forty-five's Bayes risk. <bookmark mark='d'/> Robbins's empirical Bayes estimated the same quantity from data in 1956, in the empirical-Bayes estimation tradition. Robbins's 1956 work was not the later baseball-data example.",
            [(r"y", r"=", r"x + \sigma Z", 40),
             (r"E[x \mid y]", r"=", r"y + \sigma^2 \nabla_y \log p_\sigma(y)", 40),
             (r"\text{training}", r":", r"\min E\|\hat x(y) - x\|^2", 40),
             (r"\text{the same as}", r":", r"\text{empirical Bayes}", 40)],
            [r"Part 25", r"Tweedie's formula", r"Part 45", r"Robbins (1956)"],
            colors=[(1, HONC)])

    def tweedie_chart(self):
        d = load("diffusion")
        y, tw = np.asarray(d["y"]), np.asarray(d["tweedie"])
        A = axes([-5, 5], [-5, 5], x_length=5.2, y_length=4.6, xlabel=r"noisy observation $y$ ($\sigma = 1$)",
                 ylabel=r"$E[x \mid y]$ by Tweedie", xticks=[-4, -2, 0, 2, 4], yticks=[-4, -2, 0, 2, 4], center=[-3.0, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-5, -5), ax.c2p(5, 5), color=GREY_B, stroke_width=2)
        lev = VGroup(DashedLine(ax.c2p(-5, -2), ax.c2p(5, -2), color=JUDGEC, stroke_width=1.5),
                     DashedLine(ax.c2p(-5, 1.5), ax.c2p(5, 1.5), color=JUDGEC, stroke_width=1.5))
        cur = polyline(ax, y, tw, HONC, 4)
        side = side_groups([
            [(r"data: \ two clusters, \ at $-2$ and $1.5$", JUDGEC), (r"(purple dashes)", JUDGEC)],
            [(r"grey: \ no denoising, \ $E[x \mid y] = y$", GREY_B)],
            [(r"green: \ the Bayes denoiser", HONC), (r"pulls $y$ towards the nearer cluster", HONC)],
        ], pos=(3.3, 0.1, 0))
        with self.voiceover(
            "<bookmark mark='a'/> The data: a mixture of two normal clusters, centred at minus two and one and a half. "
            "Observe a point with noise of standard deviation one. <bookmark mark='b'/> The grey diagonal would trust the "
            "observation. <bookmark mark='c'/> Tweedie's denoiser, in green, pulls each observation towards the cluster it "
            "probably came from, with a steep switch in between: shrinkage, Part twenty-five's, towards a learned prior. A "
            "diffusion model learns this curve at every noise level."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag()))
            vo.wait_until("a")
            self.play(FadeIn(lev), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cur), FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def sampler(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Probability flow uses the score of the noised marginal density. <bookmark mark='b'/> Exact transport requires starting from that same noised law. Here each sampler starts from its exact Gaussian-mixture marginal at sigma eight, using common component uniforms and normal draws, rather than replacing that marginal by a centered wide Gaussian. <bookmark mark='c'/> Integrate dx over d sigma equal to minus sigma times the score down a decreasing grid. The comparison uses Heun integration on four hundred noise levels and checks its change against a two-hundred-level grid. <bookmark mark='d'/> The endpoint is sigma .01, not zero, so even the empirical-score sampler ends near the training points with residual noise. Finite grid error and positive endpoint noise make these approximate samples. Arbitrary estimated scores at different noise levels need not correspond to one internally consistent density family.",
            [(r"\text{start}", r":", r"x \sim p_{\sigma_{\max}}\ \text{(exact noised mixture)}", 40),
             (r"\frac{dx}{d\sigma}", r"=", r"-\sigma \, s(x, \sigma)", 40),
             (r"\text{true score}", r":", r"\text{approximate finite-grid, positive-noise samples}", 40),
             (r"\text{estimated score}", r":", r"\text{samples from the estimate}", 40)],
            [r"$\sigma_{\max} = 8$", r"Song et al. (2021)", r"Part 61", r"the crux"],
            colors=[(1, HONC)])

    def memorize(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Now the statistical puzzle. <bookmark mark='b'/> With n training points, the score that minimizes the training loss exactly is the score of the empirical distribution, noised: a mixture of n tiny normals centred on the training points. <bookmark mark='c'/> Sampling with it reproduces the training points. The optimal model, on the training data, is a lookup table: memorization. <bookmark mark='d'/> Architecture, optimization, stopping and data can regularize real diffusion models, while large networks may still memorize. Explicit smoothness in this toy acts as a bandwidth, Part twenty-nine's kernel smoothing, applied implicitly.",
            [(r"\text{training optimum}", r":", r"\text{the empirical score}", 40),
             (r"p_\sigma", r"=", r"\frac1n \sum_i N(x_i, \sigma^2)", 40),
             (r"\text{samples}", r":", r"\text{the training points}", 40),
             (r"\text{generalization}", r":", r"\text{implicit smoothing}", 40)],
            [r"overfitting", r"exact", r"memorization", r"Part 29's bandwidth"],
            colors=[(2, NAIVEC), (3, HONC)])

    def chart(self):
        d = load("diffusion")
        xs = np.asarray(d["xs"])
        top = 1.12 * max(max(d[k]) for k in ("density", "kde_emp", "kde_smooth", "kde_true"))
        A = axes([-5, 5], [0, top], x_length=7.4, y_length=4.2, xlabel=r"$x$", ylabel=r"density of 4{,}000 generated samples",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.25, 0.5, 0.75], center=[-2.3, 0.3, 0])
        ax = A.ax
        clip = lambda v: np.asarray(v)  # noqa: E731
        truth = polyline(ax, xs, d["density"], WHITE, 2.5)
        tr = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 0.05), color=MODB, stroke_width=3) for x in d["train"]])
        emp = polyline(ax, xs, clip(d["kde_emp"]), NAIVEC, 2.5)
        smo = polyline(ax, xs, clip(d["kde_smooth"]), HONC, 3.5)
        side = side_groups([
            [(r"white: \ the true density", WHITE), (r"gold ticks: \ 20 training points", MODB)],
            [(r"red: \ the exact empirical score", NAIVEC), (r"spikes on the training points", NAIVEC),
             (rf"median distance to one: \ {d['near_emp']:.3f}", NAIVEC)],
            [(r"green: \ a smoothed empirical score", HONC), (rf"median distance {d['near_smooth']:.3f}", HONC),
             (rf"true sampler: \ {d['near_true']:.3f}", HONC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Twenty training points from the two-cluster density, in white. <bookmark mark='b'/> Samples from the probability flow with the exact empirical score land on the training points: the median distance from a sample to the nearest training point is {d['near_emp']:.3f}. The small positive endpoint noise leaves narrow neighborhoods of training points; this is approximate reproduction rather than exactly identical atoms. <bookmark mark='c'/> Smooth the empirical score, here by giving each training point a little spread of its own, and the samples spread out: a median distance of {d['near_smooth']:.3f}, compared with the true-law sampler's {d['near_true']:.3f}. Similar nearest-point distance is not evidence of correct density or full generalization. The density plot and this diagnostic show only this one-dimensional example."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(tr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(emp), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(smo), FadeIn(side[2]), run_time=2)
        self.wait(1.0)
        self.clear_scene()

    def rates(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What the theory says. <bookmark mark='b'/> Kazusato Oko, Shunta Akiyama and Taiji Suzuki proved in 2023 that diffusion models with suitably chosen networks estimate a smooth density at nearly minimax rates, up to stated logarithmic factors, in total variation and Wasserstein-one for specified Besov smoothness classes, suitable networks, loss minimization and sampling conditions. This is not a guarantee for arbitrary trained networks or data distributions. <bookmark mark='c'/> Fitted to an unrestricted class instead, they memorize, as the red curve showed. <bookmark mark='d'/> So generative modelling inherits density estimation's whole theory: the curse of dimensionality, unless the data lie near a low-dimensional set; and the bandwidth choice, now hidden inside the network and its training.",
            [(r"\text{suitable networks}", r":", r"\text{minimax-optimal densities}", 40),
             (r"\text{unrestricted}", r":", r"\text{memorization}", 40),
             (r"\text{dimension}", r":", r"\text{the curse, \ unless low-dimensional}", 40),
             (r"\text{bandwidth}", r":", r"\text{inside the network}", 40)],
            [r"Oko, \ Akiyama \& Suzuki (2023)", r"the empirical score", r"Part 29", r"implicit regularization"],
            colors=[(0, HONC), (1, NAIVEC)])
