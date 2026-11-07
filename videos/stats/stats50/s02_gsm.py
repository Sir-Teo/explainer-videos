from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class SequenceModel(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.chart()
        self.equivalence()
        self.examples()
        self.ellipsoid()

    def card(self):
        card = chapter_card(1, r"The Gaussian sequence model", r"A model for regular Gaussian approximation problems", lit=(1996,), part=PART)
        with self.voiceover("Chapter one. The Gaussian sequence model: one model that stands for almost every problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"y_i = f(i/n) + \sigma z_i", r":", r"\text{nonparametric regression}", font_size=34),
            cmath(r"y_k = \tfrac1n \textstyle\sum_i y_i\, \varphi_k(i/n)", r"\approx", r"\theta_k + \frac{\sigma}{\sqrt n}\, z_k, \ \ \theta_k = \langle f, \varphi_k\rangle", font_size=32),
            cmath(r"y_k = \theta_k + \varepsilon z_k", r",", r"k = 1, 2, \dots, \ \ \varepsilon = \sigma/\sqrt n: \ \text{the Gaussian sequence model}", font_size=30),
            cmath(r"\|\hat f - f\|^2", r"=", r"\textstyle\sum_k (\hat\theta_k - \theta_k)^2: \ \text{Parseval}", font_size=34),
        ]
        rows[2][-1].set_color(HYPC)
        whys = [why(r"Part 29's problem"), why(r"an orthonormal basis $\varphi_k$"), why(r"independent noise, \ coordinate by coordinate"), why(r"errors add up, \ too")]
        heading = label('Orthogonal Gaussian coefficients make function estimation a sequence problem', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Start from nonparametric regression: noisy observations of an unknown function at n points. <bookmark mark='b'/> Take inner products of the data with an orthonormal basis, such as cosines or wavelets. With a discretely orthonormal design transform, the finite coefficients have independent Gaussian errors. Continuous coefficients are approximated by quadrature; the white-noise model gives the exact infinite orthonormal sequence representation. <bookmark mark='c'/> That is the Gaussian sequence model: infinitely many unknown means, each observed once with noise of size epsilon. <bookmark mark='d'/> And by Parseval's identity, the squared error of the function is the sum of the squared errors of its coefficients. Estimating a function becomes estimating a long vector of means."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("gsm")
        k = np.asarray(d["k"], float)
        A = axes([0, 64], [-4.5, 0], x_length=7.4, y_length=4.4, xlabel=r"coefficient index $k$", ylabel=r"$\log_{10}|\theta_k|$",
                 xticks=[0, 16, 32, 48, 64], yticks=[-4, -3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        th = np.log10(np.asarray(d["theta"]))
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=TRUTHC) for a, b in zip(k, th) if b > -4.5])
        e100 = DashedLine(ax.c2p(0, np.log10(d["eps100"])), ax.c2p(64, np.log10(d["eps100"])), color=LOWC, stroke_width=2.5)
        e1e4 = DashedLine(ax.c2p(0, np.log10(d["eps10000"])), ax.c2p(64, np.log10(d["eps10000"])), color=UPC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"a function's cosine coefficients", font_size=22),
            label(r"white: \ $|\theta_k|$, \ decaying with smoothness", font_size=22, color=TRUTHC),
            label(r"red: \ the noise $\varepsilon = 1/\sqrt n$ at $n = 100$", font_size=22, color=LOWC),
            label(r"blue: \ at $n = 10{,}000$", font_size=22, color=UPC),
            label(r"keep above the noise, \ shrink below", font_size=22, color=HYPC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A function's coefficients in a cosine basis, <bookmark mark='b'/> on a log scale: they "
            "decay, faster for smoother functions. <bookmark mark='c'/> With a hundred observations the noise level is a "
            "tenth: <bookmark mark='d'/> with ten thousand, a hundredth. <bookmark mark='e'/> Coefficients well above the "
            "noise should be kept, those below it should be shrunk towards zero, and the question of how to shrink, "
            "coordinate by coordinate, is the whole of nonparametric estimation in this model. More data lowers the noise "
            "line and lets more coefficients through, which is where the rates come from."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"numerical cosine quadrature coefficients")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(e100), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(e1e4), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def equivalence(self):
        rows = fit_rows(VGroup(
            label(r"Le Cam's deficiency: \ two experiments are equivalent if each can simulate the other's decisions", font_size=26),
            label(r"Brown \& Low (1996): \ regression on $[0,1]$ $\equiv$ white noise $dY = f\,dt + \tfrac{\sigma}{\sqrt n}\,dW$, \ for $f$ smoother than $\tfrac12$", font_size=26, color=UPC),
            label(r"Nussbaum (1996): \ density estimation $\equiv$ white noise with $f$ replaced by $2\sqrt f$", font_size=26, color=S.ALT),
            label(r"transfer needs the specified classes, transformation and loss conditions", font_size=26, color=HYPC),
            label(r"the same role the Gaussian shift played for LAN in Part 47", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The connection is more than an analogy. Le Cam defined when two statistical experiments are equivalent: when each can mimic the other's decisions with vanishing loss. <bookmark mark='b'/> In 1996 Lawrence Brown and Mark Low proved that nonparametric regression is asymptotically equivalent to the white-noise model, and so to the sequence model, on appropriate bounded smoothness classes above one half, with regular design and known Gaussian noise. <bookmark mark='c'/> The same year Michael Nussbaum proved it for density estimation, for sufficiently smooth densities bounded away from zero, with twice the square root of the density as the white-noise drift. <bookmark mark='d'/> Within the equivalence theorem's model classes and suitable loss conditions, decision bounds can transfer asymptotically. Density transformations and constants must be tracked; arbitrary unbounded losses do not transfer automatically. <bookmark mark='e'/> The sequence model plays the role here that the Gaussian shift played for local asymptotic normality in Part forty-seven: a useful clean experiment that these regular models approach as the data grow, so that one theorem proved there is many theorems proved at once."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def examples(self):
        rows = fit_rows(VGroup(
            label(r"the same model, \ in other clothes:", font_size=28, color=GREY_A),
            label(r"Part 29's smoothing: \ kernels, \ splines and wavelets are coordinate-wise shrinkers in some basis", font_size=26, color=UPC),
            label(r"Part 25's James--Stein: \ the sequence model with $K$ coordinates and a common shrinkage", font_size=26, color=LINC),
            label(r"Part 32's sparse means: \ the sequence model with most $\theta_k = 0$", font_size=26, color=HYPC),
            label(r"inverse problems, \ deconvolution, \ spectral density estimation: \ the noise level varies with $k$", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The sequence model has appeared before, in other clothes. <bookmark mark='b'/> Part twenty-nine's many linear smoothers can be understood spectrally as shrinkage in a suitable basis. Boundary rules, irregular designs and nonlinear procedures require their own analysis. <bookmark mark='c'/> Part twenty-five's James–Stein estimator is the sequence model with a finite number of coordinates and one common shrinkage. <bookmark mark='d'/> Part thirty-two's sparse means are the sequence model with most coefficients zero. <bookmark mark='e'/> And inverse problems, such as deconvolution or estimating a spectral density, are sequence models whose noise level grows with k. One model, studied once, answers all of them."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ellipsoid(self):
        rows = [
            cmath(r"\Theta(\alpha, C)", r"=", r"\{\theta : \textstyle\sum_k k^{2\alpha} \theta_k^2 \le C^2\}", font_size=36),
            cmath(r"\text{cosines}, \ \alpha \in \mathbb N", r":", r"\int (f^{(\alpha)})^2 \le \pi^{2\alpha} C^2: \ \text{a Sobolev ball}", font_size=32),
            cmath(r"\text{the minimax risk}", r":", r"R^*(\varepsilon) = \inf_{\hat\theta} \sup_{\Theta(\alpha, C)} E \|\hat\theta - \theta\|^2", font_size=32),
            cmath(r"\varepsilon = 1/\sqrt n", r"\Rightarrow", r"R^* \asymp n^{-2\alpha/(2\alpha + 1)}: \ \text{Stone's rate with } d = 1", font_size=32),
        ]
        rows[2][-1].set_color(HYPC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"a Sobolev ellipsoid"), why(r"smoothness as coefficient decay"), why(r"the target"), why(r"chapters 2--5 prove it")]
        heading = label('A Sobolev ellipsoid bounds weighted coefficient energy', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Smoothness becomes a constraint on the coefficients: the sum of k to the two alpha times theta k squared is at most C squared, an ellipsoid. <bookmark mark='b'/> For the appropriate Sobolev domain and boundary conditions in a complete cosine expansion, including its constant term, it is a bound on the integral of the alpha-th derivative squared: a Sobolev ball. <bookmark mark='c'/> The minimax risk is the best worst-case squared error over the ellipsoid. <bookmark mark='d'/> With epsilon one over root n it is of order n to the minus two alpha over two alpha plus one, Stone's rate in one dimension. The next four chapters find its constant, prove it is a lower bound, and match it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
