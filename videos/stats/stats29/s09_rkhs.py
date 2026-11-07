from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class RKHS(VoiceoverScene):
    def construct(self):
        self.card()
        self.space()
        self.representer()
        self.splines_are()
        self.fits()
        self.gp()
        self.bridge()

    def card(self):
        card = chapter_card(8, r"Kernels and the representer theorem", r"Infinite dimensions, \ finite answers", lit=(1970,), part=PART)
        with self.voiceover("Chapter eight. Reproducing kernels and the representer theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def space(self):
        rows = [
            cmath(r"k(x, x')", r":", r"\text{symmetric, \ positive semidefinite}", font_size=30),
            cmath(r"\mathcal H", r"=", r"\overline{\mathrm{span}}\{k(x, \cdot)\}, \ \ \langle k(x, \cdot), k(x', \cdot)\rangle = k(x, x')", font_size=28),
            cmath(r"f(x)", r"=", r"\langle f, k(x, \cdot) \rangle", font_size=32),
            cmath(r"\|f\|_{\mathcal H}", r":", r"\text{a roughness measure set by } k", font_size=30),
        ]
        rows[2][2].set_color(KDEC)
        whys = [why(r"e.g.\ $e^{-(x - x')^2 / 2\ell^2}$"), why(r"Aronszajn (1950)"), why(r"the reproducing property"),
                why(r"smooth $k$: \ smooth functions are cheap")]
        with self.voiceover(
            "<bookmark mark='a'/> The general idea behind the spline. Start with a symmetric positive semidefinite "
            "kernel, now a function of two points, like a Gaussian bump in their distance. <bookmark mark='b'/> It "
            "generates a Hilbert space of functions, sums of kernel sections, with the inner product of two sections "
            "defined as the kernel itself, Nachman Aronszajn's construction. <bookmark mark='c'/> Then evaluating a "
            "function at x is an inner product with the section at x: the reproducing property. <bookmark mark='d'/> "
            "And the space's norm is a measure of roughness, decided by the kernel."
        ) as vo:
            intro=label('A positive semidefinite kernel defines a space with bounded evaluation',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def representer(self):
        rows = [
            cmath(r"\min_{f \in \mathcal H}", r"\ ", r"\textstyle\sum_i L(y_i, f(x_i)) + \lambda \|f\|_{\mathcal H}^2", font_size=30),
            cmath(r"f", r"=", r"f_\parallel + f_\perp, \ \ f_\parallel \in \mathrm{span}\{k(x_i, \cdot)\}", font_size=30),
            cmath(r"f(x_i)", r"=", r"\langle f_\parallel + f_\perp, k(x_i, \cdot)\rangle = f_\parallel(x_i)", font_size=30),
            cmath(r"\hat f", r"=", r"\textstyle\sum_i \alpha_i k(x_i, \cdot)", font_size=34),
        ]
        rows[3][2].set_color(KDEC)
        whys = [why(r"$\lambda>0$, \ a minimizer exists"), why(r"split off the part orthogonal to the data's sections"),
                why(r"$f_\perp$ is invisible to the data, \ and only adds norm"), why(r"Kimeldorf \& Wahba (1970)")]
        with self.voiceover(
            "<bookmark mark='a'/> For positive lambda and a loss admitting a minimizer, minimize data loss plus "
            "lambda times the squared norm. <bookmark mark='b'/> Split any candidate into its projection on the n "
            "kernel sections at the data points, and the rest. <bookmark mark='c'/> By the reproducing property, the "
            "rest is zero at every data point: the data cannot see it, and it only adds to the norm. <bookmark "
            "mark='d'/> So the minimizer is a combination of n kernel sections: George Kimeldorf and Grace Wahba's "
            "representer theorem of 1970. An infinite-dimensional problem with an n-dimensional answer."
        ) as vo:
            intro=label('Orthogonal components invisible to the data only add penalty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def splines_are(self):
        rows = [
            cmath(r"\text{squared loss}", r":", r"\hat\alpha = (K + \lambda I)^{-1} y", font_size=30),
            cmath(r"\hat f(x)", r"=", r"k(x)^\top (K + \lambda I)^{-1} y", font_size=30),
            cmath(r"\|f\|^2 = \textstyle\int f''^2", r":", r"\text{the cubic smoothing spline}", font_size=28),
            cmath(r"\text{SVM representers; \ related kernel PCA and GP conditioning}", r":", r"\text{related Gram-matrix methods}", font_size=28),
        ]
        rows[0][2].set_color(KDEC)
        whys = [why(r"kernel ridge regression"), why(r"$k(x)$: \ the kernel to each data point"),
                why(r"with lines unpenalized: \ chapter six's theorem"), why(r"machine learning's kernel trick")]
        with self.voiceover(
            "<bookmark mark='a'/> With squared loss the coefficients solve a linear system: kernel ridge regression. "
            "<bookmark mark='b'/> The fit at a new point is the vector of kernels to the data times that system's "
            "solution. <bookmark mark='c'/> The cubic spline uses a roughness seminorm with a two-dimensional linear "
            "null space: the representer argument must retain those unpenalized lines. <bookmark mark='d'/> Support "
            "vector machines use a representer theorem too. Kernel PCA uses related Gram-matrix geometry, and "
            "Gaussian-process conditioning gives a matching posterior mean under Gaussian noise."
        ) as vo:
            intro=label('Gram matrices connect regularization and Gaussian conditioning',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fits(self):
        d = load("rkhs")
        t, a, tt = np.asarray(d["t"]), np.asarray(d["a"]), np.asarray(d["tt"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"milliseconds after impact",
                 ylabel=r"head acceleration ($g$)", xticks=[0, 20, 40, 60], yticks=[-100, 0, 50], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE, fill_opacity=0.7) for x, y in zip(t, a)])
        spec = (("0.5_1", GREY_B), ("0.15_1", KDEC), ("0.05_0.1", NWC))
        cs = {k: clip_curve(ax, tt, np.asarray(d["fits"][k]["pred"]), c, 3, ymin=-150, ymax=90) for k, c in spec}
        sd = np.std(t)
        rows = fit_rows(VGroup(
            label(r"Gaussian kernel, \ width $\ell$, \ penalty $\lambda$", font_size=22),
            label(rf"$\ell = {0.5 * sd:.1f}$ ms: \ df {d['fits']['0.5_1']['df']:.1f}, \ too smooth", font_size=22, color=GREY_B),
            label(rf"$\ell = {0.15 * sd:.1f}$ ms: \ df {d['fits']['0.15_1']['df']:.1f}", font_size=22, color=KDEC),
            label(rf"$\ell = {0.05 * sd:.1f}$ ms, \ small $\lambda$: \ df {d['fits']['0.05_0.1']['df']:.0f}", font_size=22, color=NWC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Kernel ridge regression on the motorcycle data, with a Gaussian kernel of width ell. "
            "<bookmark mark='b'/> A wide kernel, six and a half milliseconds, can't bend fast enough: seven degrees of freedom, and the "
            "dip is too shallow. <bookmark mark='c'/> A kernel of two milliseconds: eighteen degrees of freedom, "
            "close to the smoothing spline. <bookmark mark='d'/> A narrow kernel with little penalty: fifty-six degrees of "
            "freedom and a wiggly fit. The kernel's width and lambda together set the smoothness."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, ((key, _), m_) in enumerate(zip(spec, "bcd")):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(rows[k + 1]))
        self.clear_scene()

    def gp(self):
        d = load("rkhs")
        t, a, tt = np.asarray(d["t"]), np.asarray(d["a"]), np.asarray(d["tt"])
        m, s = np.asarray(d["gp_mean"]), np.asarray(d["gp_sd"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"milliseconds after impact",
                 ylabel=r"head acceleration ($g$)", xticks=[0, 20, 40, 60], yticks=[-100, 0, 50], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE, fill_opacity=0.7) for x, y in zip(t, a)])
        bnd = band(ax, tt, np.clip(m - 2 * s, -150, 90), np.clip(m + 2 * s, -150, 90), KDEC, 0.3)
        mean = curve(ax, tt, m, KDEC, 4)
        rows = fit_rows(VGroup(
            label(r"$f \sim \mathrm{GP}(0, \tau^2 k)$, \ noise $\sigma^2$, \ $\lambda = \sigma^2/\tau^2$", font_size=22),
            label(r"posterior mean $=$ the kernel ridge fit", font_size=22, color=KDEC),
            label(r"band: \ $\pm 2$ posterior SD of $f$", font_size=22, color=KDEC),
            label(rf"$\hat\sigma = {d['sigma']:.1f}$ $g$, \ one value for the whole curve", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same fit has a Bayesian reading. Put a Gaussian-process prior on the curve, "
            "with covariance tau squared times the kernel, and normal noise. <bookmark mark='b'/> The posterior mean "
            "is exactly the kernel ridge fit, with lambda the ratio of noise to signal variance, as for the spline's "
            "mixed model. <bookmark mark='c'/> At fixed hyperparameters the posterior gives pointwise uncertainty for"
            " the latent curve, not a simultaneous band or a predictive interval for a new noisy observation. "
            "<bookmark mark='d'/> Its width assumes one noise level, twenty-three g, everywhere: a potentially "
            "inadequate assumption given the changing residual spread. Plugging in an estimated noise level also "
            "leaves hyperparameter uncertainty out. Part 39 builds Gaussian processes properly, with estimated "
            "kernels."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bnd), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bridge(self):
        rows = fit_rows(VGroup(
            label(r"penalized least squares in an RKHS \ $=$ \ a Gaussian-process posterior mean", font_size=24, color=KDEC),
            label(r"the penalty \ $=$ \ the prior; \ \ $\lambda$ \ $=$ \ noise over signal", font_size=24),
            label(r"kernel width and $\lambda$ \ $=$ \ hyperparameters: \ choose by CV or marginal likelihood", font_size=24, color=PATH),
            label(r"general dense solve: \ $O(n^3)$; structure or approximations can reduce it", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The dictionary: penalized least squares in a reproducing kernel space is a "
            "Gaussian-process posterior mean. <bookmark mark='b'/> The penalty is the prior, and lambda the "
            "noise-to-signal ratio. <bookmark mark='c'/> The kernel's width and lambda are hyperparameters, chosen by"
            " cross-validation or by the marginal likelihood, REML's cousin. <bookmark mark='d'/> A general dense "
            "solve costs order n cubed; specialized banded spline solvers and approximate kernel methods can cost "
            "less."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
