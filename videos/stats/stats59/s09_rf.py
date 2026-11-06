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
        self.lad_voiceover(
            "<bookmark mark='a'/> Random-features regression: draw N random weight vectors w, once, and use the features "
            "sigma of w transpose x, with sigma a fixed nonlinearity such as the ReLU. <bookmark mark='b'/> Then fit the "
            "output weights by ridge regression. <bookmark mark='c'/> It is a two-layer neural network whose first layer is "
            "frozen at random, and Ali Rahimi and Ben Recht introduced it in 2007 as a cheap kernel method. <bookmark "
            "mark='d'/> Its proportional limit has three sizes growing together: observations n, input dimension d, and "
            "features N.",
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
        A = axes([-1.6, 1.0], [-1.8, 2.0], x_length=7.4, y_length=4.4, xlabel=r"features per observation, \ $N/n$ (log scale)",
                 ylabel=r"test error (log scale)", xticks=[-1, 0, 1], xfmt=lambda v: f"{10 ** v:g}", yticks=[-1, 0, 1, 2],
                 yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c0 = VGroup(polyline(ax, x, np.clip(y0, -1.8, 2.0), CLASSC, 4), *[Dot(ax.c2p(a, min(b, 2.0)), radius=0.06, color=CLASSC) for a, b in zip(x, y0)])
        c1 = VGroup(polyline(ax, x, np.clip(y1, -1.8, 2.0), PROPC, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=PROPC) for a, b in zip(x, y1)])
        thr = DashedLine(ax.c2p(0, -1.8), ax.c2p(0, 2.0), color=GREY_B, stroke_width=2)
        peak = max(d["ridgeless"])
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ $d = {d['d']}$; \ ReLU features; \ a linear target plus noise", font_size=22),
            label(rf"red: \ ridgeless; \ its peak at $N = n$ is {peak:.0f}", font_size=22, color=CLASSC),
            label(r"green: \ a small ridge penalty, \ $\lambda = 10^{-3}$", font_size=22, color=PROPC),
            label(r"past the peak, \ more features help: \ the second descent", font_size=22, color=GREY_A),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Three hundred observations in thirty dimensions, with a linear target, fitted with "
            f"between ten and two and a half thousand ReLU features. <bookmark mark='b'/> Without a penalty, the test error "
            f"rises to a spike, {peak:.0f}, where the number of features equals the number of observations, and then falls "
            f"again. <bookmark mark='c'/> A tiny ridge penalty, in green, removes the spike: <bookmark mark='d'/> what remains "
            f"is a smooth curve that keeps improving as the network widens, the second descent without the first ascent."
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
        self.lad_voiceover(
            "<bookmark mark='a'/> Song Mei and Andrea Montanari computed the exact limiting test error of random-features "
            "ridge regression in 2022. <bookmark mark='b'/> The key fact is a linearization: the nonlinear features behave, "
            "in the proportional limit, like a linear function of the inputs plus independent Gaussian noise, with "
            "coefficients from the Hermite expansion of sigma. <bookmark mark='c'/> The error is then a ridge-type formula in "
            "chapter two's random-matrix transforms, now of a structured matrix. <bookmark mark='d'/> It reproduces the spike "
            "at N equal to n, the descent beyond it, and the optimal penalty, all exactly.",
            [(r"\text{Mei \& Montanari (2022)}", r":", r"\text{the exact test error}", 40),
             (r"\sigma(w'x)", r"\approx", r"\mu_0 + \mu_1 w'x + \mu_\star Z", 40),
             (r"\text{error}", r"=", r"\text{a ridge formula in structured-matrix transforms}", 38),
             (r"\text{reproduces}", r":", r"\text{the spike, \ the descent, \ the best penalty}", 40)],
            [r"\emph{CPAM}", r"Gaussian equivalence", r"chapter 2's tools", r"double descent, \ derived"],
            colors=[(1, AMPC), (3, PROPC)])

    def kernel(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> As the number of features grows without limit, random-features ridge becomes kernel ridge "
            "regression, Part twenty-nine's, with the kernel equal to the expected product of features. <bookmark mark='b'/> "
            "In the proportional regime, kernels with n and d of the same order are effectively linear: they learn only the "
            "linear part of the target, plus a ridge penalty from the nonlinear part, as Noureddine El Karoui showed for "
            "kernel matrices in 2010. <bookmark mark='c'/> To learn more, n must grow like a higher power of d. <bookmark "
            "mark='d'/> That staircase, one polynomial degree for each power of d, is a theory of what wide networks in this "
            "lazy regime can and cannot learn.",
            [(r"N \to \infty", r":", r"\text{kernel ridge, \ } k(x, x') = E_w[\sigma(w'x)\sigma(w'x')]", 36),
             (r"n \asymp d", r":", r"\text{the kernel is effectively linear}", 40),
             (r"n \asymp d^\ell", r":", r"\text{degree-}\ell \text{ polynomials learned}", 40),
             (r"\text{so}", r":", r"\text{a staircase of learnability}", 40)],
            [r"Part 29's kernels", r"El Karoui (2010)", r"more data, \ more degrees", r"the lazy regime"],
            colors=[(1, CLASSC), (3, PROPC)])

    def lessons(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What random features teach. <bookmark mark='b'/> Overparameterization is not the problem; "
            "the interpolation threshold is. <bookmark mark='c'/> A little regularization removes the spike, and then more "
            "features never hurt. <bookmark mark='d'/> And exact formulas for a simple network explain, at least in this "
            "lazy regime, why wide models generalize, which Part sixty-four will take further.",
            [(r"what random features teach:", GREY_A),
             (r"the threshold $N = n$ is the problem, \ not size", CLASSC),
             (r"a little ridge removes the spike; \ then more features never hurt", PROPC),
             (r"exact formulas for a simple network \ (Part 64 goes further)", AMPC)])

    def hermite(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Gaussian equivalence in numbers, for the ReLU with standard normal input. Its mean, mu nought, is one over root two pi, about 0.40. <bookmark mark='b'/> Its linear coefficient, mu one, is the expectation of Z times ReLU of Z: a half. <bookmark mark='c'/> Its second moment is a half, so the nonlinear remainder has variance a half minus 0.16 minus a quarter, about 0.09. <bookmark mark='d'/> So in the limit a ReLU feature is 0.40 plus a half times the projection, plus independent noise of standard deviation 0.30: the network's nonlinearity acts like a ridge penalty.",
            [('\\mu_0', '=', 'E[\\mathrm{ReLU}(Z)] = 1/\\sqrt{2\\pi} \\approx 0.40', 40),
             ('\\mu_1', '=', 'E[Z\\,\\mathrm{ReLU}(Z)] = 1/2', 40),
             ('\\mu_\\star^2', '=', '\\tfrac12 - \\mu_0^2 - \\mu_1^2 \\approx 0.09', 40),
             ('\\Rightarrow', '\\;', "\\text{feature} \\approx 0.40 + 0.5\\,w'x + 0.30\\,Z", 40)],
            ['the constant', 'the linear part', 'the remainder', 'implicit ridge'],
            colors=[(3, AMPC)])

    def kernel_worked(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A worked consequence. With n equal to three hundred and d equal to thirty, n is ten times d: the kernel limit learns the linear part of a target well, and nothing quadratic. <bookmark mark='b'/> To learn quadratics in thirty dimensions it would need n of order d squared, nine hundred, times a constant. <bookmark mark='c'/> Our target was linear, so the wide random-features model did well, reaching an error of 0.23 with two and a half thousand features. <bookmark mark='d'/> A quadratic target, at this sample size, would have defeated it however wide it grew.",
            [('n = 300, \\ d = 30', ':', 'n \\approx 10d', 40),
             ('\\text{quadratics}', ':', '\\text{need } n \\gtrsim d^2 = 900', 40),
             ('\\text{our target}', ':', '\\text{linear: \\ error } 0.23 \\text{ at } N = 2{,}500', 40),
             ('\\text{a quadratic target}', ':', '\\text{unlearnable here, \\ at any width}', 40)],
            ["the staircase's first step", 'the second step', "the chart's end", 'width does not help'],
            colors=[(3, CLASSC)])
