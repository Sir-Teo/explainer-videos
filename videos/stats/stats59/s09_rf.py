from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class RandomFeatures(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Random features and kernels: a bridge from regression to neural networks.", 8,
                            r"Random features and kernels", r"A two-layer network, \ first layer frozen", lit=(2022,))
        self.model()
        self.chart()
        self.theory()
        self.hermite()
        self.kernel()
        self.kernel_worked()
        self.lessons()

    def model(self):
        heading = label('A frozen random first layer', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Random-features regression: draw N random weight vectors w, once, and use the "
            'features sigma of w transpose x, with sigma a fixed nonlinearity such as the ReLU. <bookmark '
            "mark='b'/> Then fit the output weights by ridge regression. <bookmark mark='c'/> It is a two-layer "
            'neural network whose first layer is frozen at random, and Ali Rahimi and Ben Recht introduced it in '
            "2007 as a cheap kernel method. <bookmark mark='d'/> Its proportional limit has three sizes growing "
            'together: observations n, input dimension d, and features N.'
        ),
            [(r"\text{features}", r":", r"\sigma(w_k'x), \ \ k = 1, \dots, N, \ \ w_k \text{ random, \ fixed}", 38),
             (r"\text{fit}", r":", r"\text{ridge on the } N \text{ features}", 40),
             (r"\text{reading}", r":", r"\text{a two-layer network, \ first layer frozen}", 40),
             (r"\text{regime}", r":", r"n, d, N \to \infty \text{ proportionally}", 40)],
            [r"ReLU", r"chapter 3's ridge", r"Rahimi \& Recht (2007)", r"three ratios"],
            colors=[(2, AMPC)])

    def chart(self):
        d = load("rf")
        Ns = np.asarray(d["Ns"], float)
        x = np.log10(Ns / d["n"])
        y0 = np.log10(np.asarray(d["ridgeless"]))
        y1 = np.log10(np.asarray(d["ridge"]))
        lower = min(-1.8, float(np.floor(min(y0.min(), y1.min()))))
        upper = max(2.0, float(np.ceil(max(y0.max(), y1.max()))))
        A = axes([-1.6, 1.0], [lower, upper], x_length=7.4, y_length=4.4, xlabel=r"features per observation, \ $N/n$ (log scale)",
                 ylabel=r"excess prediction error (log scale)", xticks=[-1, 0, 1], xfmt=lambda v: f"{10 ** v:g}", yticks=list(range(math.ceil(lower), math.floor(upper)+1)),
                 yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c0 = VGroup(polyline(ax, x, y0, CLASSC, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=CLASSC) for a, b in zip(x, y0)])
        c1 = VGroup(polyline(ax, x, y1, PROPC, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=PROPC) for a, b in zip(x, y1)])
        thr = DashedLine(ax.c2p(0, lower), ax.c2p(0, upper), color=GREY_B, stroke_width=2)
        peak = max(d["ridgeless"])
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ $d = {d['d']}$; \ ReLU features; \ noiseless target variance $1/d$; \ error excludes test noise", font_size=22),
            label(rf"red: \ ridgeless; \ six-run mean peak {peak:.0f}; \\ empirical SE {d['audit']['mcse'][0][int(np.argmax(d['ridgeless']))]:.0f}", font_size=22, color=CLASSC),
            label(r"green: \ a small ridge penalty, \ $\lambda = 10^{-3}$", font_size=22, color=PROPC),
            label(r"past the peak, \ more features help: \ the second descent", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Three hundred observations in thirty dimensions, with a linear target, fitted with between ten and two and a half thousand ReLU features. <bookmark mark='b'/> Without a penalty, the test error rises to a spike, {peak:.0f}, where the number of features equals the number of observations, and then falls again. <bookmark mark='c'/> A tiny ridge penalty, in green, removes the spike: <bookmark mark='d'/> the remaining curve has much less interpolation amplification in this example. Width effects need not be monotone in every model. At the square fit, heavy tails make a six-run mean especially unstable."
        ) as vo:
            self.play(FadeIn(A), Create(thr), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c0), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def theory(self):
        heading = label('Gaussian equivalence for limiting risk', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Song Mei and Andrea Montanari computed the exact limiting test error of random-features ridge regression in 2022. <bookmark mark='b'/> The key fact is a linearization: the nonlinear features behave, in the proportional limit, like a Gaussian-equivalent matrix for the risk quantities in the theorem, with coefficients determined by the activation's Hermite moments. This is not an identity in distribution for each individual feature. <bookmark mark='c'/> The error is then a ridge-type formula in chapter two's random-matrix transforms, now of a structured matrix. <bookmark mark='d'/> Under their spherical input/weight and target assumptions it gives an exact limiting risk. Our finite Gaussian-input simulation is an illustration, with no computed theorem curve overlaid."
        ),
            [(r"\text{Mei \& Montanari (2022)}", r":", r"\text{the exact test error}", 40),
             (r"\sigma(w'x)", r"\approx", r"\mu_0 + \mu_1 w'x + \mu_\star Z", 40),
             (r"\text{error}", r"=", r"\text{a ridge formula in structured-matrix transforms}", 38),
             (r"\text{reproduces}", r":", r"\text{the spike, \ the descent, \ the best penalty}", 40)],
            [r"\emph{CPAM}", r"Gaussian equivalence", r"chapter 2's tools", r"double descent, \ derived"],
            colors=[(1, AMPC), (3, PROPC)])

    def kernel(self):
        heading = label('Kernel limits with normalized features', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> As the number of features grows without limit, random-features ridge becomes kernel ridge regression, Part twenty-nine's, with the kernel equal to the expected product of features. <bookmark mark='b'/> In the proportional regime, suitable isotropic high-dimensional inner-product kernels can be effectively linear for generic target components: they learn only the linear part of the target, plus a ridge penalty from the nonlinear part, as Noureddine El Karoui showed for kernel matrices in 2010. <bookmark mark='c'/> To learn more, n must grow like a higher power of d. <bookmark mark='d'/> That staircase, one polynomial degree for each power of d, is a theory of what wide networks in this lazy regime can and cannot learn."
        ),
            [(r"N \to \infty", r":", r"\text{kernel ridge, \ } k(x, x') = E_w[\sigma(w'x)\sigma(w'x')]", 36),
             (r"n \asymp d", r":", r"\text{the kernel is effectively linear}", 40),
             (r"n \asymp d^\ell", r":", r"\text{a generic degree-}\ell\text{ learning transition, under assumptions}", 40),
             (r"\text{so}", r":", r"\text{a staircase of learnability}", 40)],
            [r"Part 29's kernels", r"El Karoui (2010)", r"more data, \ more degrees", r"the lazy regime"],
            colors=[(1, CLASSC), (3, PROPC)])

    def lessons(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> The experiment illustrates one random-feature model, with six repeated datasets "
            "per curve. <bookmark mark='b'/> Ridgeless interpolation can have a large spike near the square feature "
            "matrix, while sufficiently overparameterized fits can have lower excess risk. <bookmark mark='c'/> A "
            'positive penalty regularizes small singular values, but neither monotone improvement with width nor a '
            'particular optimal penalty is universal. Read the simulation with its Monte Carlo uncertainty. '
            "<bookmark mark='d'/> Rigorous limiting formulas cover particular input, weight, activation and target "
            'models. They help explain a frozen first layer, rather than all trained neural networks.'
        ),
            [(r"what random features teach:", GREY_A),
             (r"the threshold $N = n$ is the problem, \ not size", CLASSC),
             (r"ridge controls small singular values; \ width effects depend on the model", PROPC),
             (r"exact formulas for a simple network \ (Part 64 goes further)", AMPC)])

    def hermite(self):
        heading = label('Orthogonal Hermite moments, not a feature identity', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> For a standard normal projection, ReLU has mean one over the square root of two "
            "pi, about point four. <bookmark mark='b'/> Its linear Hermite coefficient is one-half. <bookmark "
            "mark='c'/> The remaining orthogonal Hermite components have variance one-half minus one over two pi "
            "minus one-quarter, about point zero nine one. <bookmark mark='d'/> A Gaussian-equivalent matrix with "
            'these matched coefficients can reproduce certain limiting spectral and risk quantities under the '
            "random-feature theorem's assumptions. This is not a distributional identity turning each nonlinear "
            'feature into a linear projection plus independent Gaussian noise.'
        ),
            [('\\mu_0', '=', 'E[\\mathrm{ReLU}(Z)] = 1/\\sqrt{2\\pi} \\approx 0.40', 40),
             ('\\mu_1', '=', 'E[Z\\,\\mathrm{ReLU}(Z)] = 1/2', 40),
             ('\\mu_\\star^2', '=', '\\tfrac12 - \\mu_0^2 - \\mu_1^2 \\approx 0.09', 40),
             ('\\Rightarrow', '\\;', "\\text{feature} \\approx 0.40 + 0.5\\,w'x + 0.30\\,Z", 40)],
            ['the constant', 'the linear part', 'the remainder', 'implicit ridge'],
            colors=[(3, AMPC)])

    def kernel_worked(self):
        heading = label('Degree and sample size: an asymptotic guide', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Our finite example has three hundred observations and thirty input coordinates. "
            'Comparing n to powers of d is an asymptotic guide, not a sharp finite-data impossibility test. '
            "<bookmark mark='b'/> In suitable high-dimensional isotropic kernel models, learning a generic "
            'degree-two component typically needs a sample size comparable to the quadratic feature dimension, of '
            "order d squared. Special low-rank quadratics can be easier. <bookmark mark='c'/> Here the target is "
            'linear with variance one over thirty; reported error is against its noiseless conditional mean and '
            'excludes test noise. The two penalties use the same repeated datasets and nested features normalized '
            "by one over root N. <bookmark mark='d'/> Width can improve approximation to the kernel, but cannot by "
            'itself guarantee recovery of every target. We do not infer that all quadratic targets are unlearnable '
            'at this finite sample size.'
        ),
            [('n = 300, \\ d = 30', ':', 'n \\approx 10d', 40),
             ('\\text{quadratics}', ':', '\\text{need } n \\gtrsim d^2 = 900', 40),
             ('\\text{our target}', ':', '\\text{linear: \\ error } 0.23 \\text{ at } N = 2{,}500', 40),
             ('\\text{a quadratic target}', ':', '\\text{generic degree-two learning needs its own sample-size analysis}', 40)],
            ["the staircase's first step", 'the second step', "the chart's end", 'width does not help'],
            colors=[(3, CLASSC)])
