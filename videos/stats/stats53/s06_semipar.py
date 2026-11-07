from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Semiparametric(VoiceoverScene):
    def construct(self):
        self.card()
        self.failures()
        self.chart()
        self.why()
        self.repairs()
        self.functionals()
        self.castillo()

    def card(self):
        card = chapter_card(5, r"Semiparametric BvM, \ and its failures", r"In infinite dimensions, \ credible is not confident", lit=(1999,), part=PART)
        with self.voiceover("Chapter five. Semiparametric Bernstein–von Mises, and its failures: in infinite dimensions, credible is not confident."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def failures(self):
        rows = [
            cmath(r"\text{Cox (1993)}", r":", r"\text{GP regression: \ bands can cover near } 0", font_size=32),
            cmath(r"\text{Freedman (1999)}", r":", r"\text{no BvM for the whole function}", font_size=32),
            cmath(r"\text{the reason}", r":", r"\text{spread and error differ in size}", font_size=32),
            cmath(r"\text{in a ball}", r":", r"\text{right size, \ wrong centre}", font_size=32),
        ]
        rows[0][-1].set_color(BADC)
        rows[1][-1].set_color(BADC)
        whys = [why(r"``an analysis of Bayesian inference''"), why(r"``Wald lecture''"), why(r"bias $\gg$ spread"), why(r"chapter 9's question")]
        heading = label('Strong-norm infinite-dimensional normal approximation can fail', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> In 1993, Dennis Cox showed that for Gaussian-process regression, a ninety-five percent credible band for the regression function can have frequentist coverage close to zero. <bookmark mark='b'/> In 1999, David Freedman showed in the Gaussian white-noise model that the Bernstein–von Mises theorem fails for the function as a whole: the classical strong-norm infinite-dimensional normal approximation can fail. This does not rule out finite-dimensional marginals or BvM in weaker multiscale spaces. <bookmark mark='c'/> The reason is that in infinitely many dimensions the posterior's spread and the posterior mean's error need not be of the same size. <bookmark mark='d'/> A credible ball can be the right size and still be centred in the wrong place, so that the truth falls outside nearly always."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("semipar")
        a = np.asarray(d["alphas"])
        A = axes([0.2, 3.05], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=rf"prior smoothness $\alpha$ \ (truth $\beta = {d['beta']:g}$, \ $n = 10^4$)", ylabel=r"frequentist coverage",
                 xticks=[0.5, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.25, 0.5, 0.75, 0.95], center=[-2.5, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0.2, 0.95), ax.c2p(3.05, 0.95), color=GREY_B, stroke_width=2)
        cb = VGroup(polyline(ax, a, d["ball"], BALLC, 4), *[Dot(ax.c2p(x, y), radius=0.06, color=BALLC) for x, y in zip(a, d["ball"])])
        cs = VGroup(polyline(ax, a, d["smooth"], GOODC, 4), *[Dot(ax.c2p(x, y), radius=0.06, color=GOODC) for x, y in zip(a, d["smooth"])])
        cr = VGroup(polyline(ax, a, d["rough"], FREQC, 4), *[Dot(ax.c2p(x, y), radius=0.06, color=FREQC) for x, y in zip(a, d["rough"])])
        b = dict(zip(np.round(a, 3), d["ball"]))
        side = fit_rows(VGroup(
            label(r"95\% credible sets, \ their frequentist coverage", font_size=22),
            label(r"gold: \ ball for the $K=3{,}000$ retained coordinates", font_size=22, color=BALLC),
            label(rf"\ \ 100\% if rough; \ {100 * d['ball'][8]:.0f}\% at 1.25; \ $\approx 0$ from 1.5", font_size=22, color=BALLC),
            label(r"green: \ $\sum k^{-1}\theta_k$: \ fine to $\alpha = 2$", font_size=22, color=GOODC),
            label(r"teal: \ $\sum k^{-0.6}\theta_k$: \ fails sooner", font_size=22, color=FREQC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The comparison uses exact finite-coordinate functional coverage and simulated credible-ball coverage, for a truth of smoothness one and ten thousand observations, as the prior's smoothness varies. <bookmark mark='b'/> In gold, the credible ball for the three thousand retained coefficients. The posterior quantile has an independent Monte Carlo reference; uncertainty in that calibration is recorded separately from dataset simulation error. <bookmark mark='c'/> For rough priors it is conservative, covering in all sampled replicates here, with Monte Carlo and radius-calibration uncertainty. As the prior grows smoother than the truth, coverage collapses: {100 * d['ball'][8]:.0f} percent at one and a quarter, and nearly zero from one and a half on. This is Freedman's phenomenon. <bookmark mark='d'/> In green, the credible interval for a smooth linear functional, a weighted sum of coefficients with weights one over k: it keeps its ninety-five percent almost to alpha two. <bookmark mark='e'/> In teal, a rougher functional, with weights k to the minus point six: it fails sooner and harder, {100 * d['rough'][-1]:.0f} percent at alpha three."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(exact_tag(r"exact; \ the ball simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cr), FadeIn(side[4]))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"\text{oversmoothing prior}", r":", r"\text{posterior spread} \asymp n^{-\alpha/(1+2\alpha)}, \ \text{bias} \asymp n^{-\beta/(1+2\alpha)}", font_size=30),
            cmath(r"\alpha > \beta", r":", r"\text{bias} \gg \text{spread}: \ \text{the ball misses the truth}", font_size=34),
            cmath(r"\alpha < \beta", r":", r"\text{spread} \gg \text{bias}: \ \text{the ball covers, \ but is too large}", font_size=34),
            cmath(r"\alpha = \beta", r":", r"\text{same rate order; coverage depends on constants, not generally }95\%", font_size=32),
        ]
        rows[1][-1].set_color(BADC)
        rows[2][-1].set_color(FREQC)
        whys = [why(r"Knapik et al. (2011)"), why(r"overconfident"), why(r"conservative"), why(r"even the right prior")]
        heading = label('Bias and posterior spread need not balance as their rate suggests', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why. The posterior's spread shrinks at rate n to the minus alpha over one plus two alpha, while the posterior mean's bias for a beta-smooth truth shrinks at n to the minus beta over the same denominator. <bookmark mark='b'/> When the prior is smoother than the truth, the bias dominates the spread: the credible ball is too small for its own error, and misses. <bookmark mark='c'/> When the prior is rougher, the spread dominates: the ball covers, but is wastefully large and the rate is suboptimal. <bookmark mark='d'/> And when the smoothness matches exactly, they are of the same order, so coverage depends on the bias, spread and noise constants. It need not tend to ninety-five percent or even to a nontrivial fraction between zero and one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def repairs(self):
        rows = [
            cmath(r"\text{undersmooth}", r":", r"\alpha < \beta: \ \text{the ball covers, \ at a slower rate}", font_size=34),
            cmath(r"\text{inflate}", r":", r"\text{multiply the radius by a constant } L > 1", font_size=34),
            cmath(r"\text{adapt}", r":", r"\text{estimate } \alpha \text{ \ (chapter 8), \ then inflate \ (chapter 9)}", font_size=34),
            cmath(r"\text{change the norm}", r":", r"\text{BvM in a weaker, \ multiscale norm}", font_size=32),
        ]
        rows[0][-1].set_color(FREQC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"conservative"), why(r"a fudge, \ with a theorem"), why(r"the practical route"), why(r"multiscale")]
        heading = label('Inflation and weaker norms require their own coverage conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Four repairs. Use a rougher prior than the truth: the ball covers, at the price of a slower rate. <bookmark mark='b'/> Inflate the credible ball by a constant factor. <bookmark mark='c'/> Estimate the smoothness from the data and then inflate, the route of chapters eight and nine. <bookmark mark='d'/> Or change the norm: Castillo and Nickl proved Bernstein–von Mises theorems for the whole function in weaker, multiscale norms, where credible sets do cover, and turned them into honest bands."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def functionals(self):
        rows = [
            cmath(r"L(\theta) = \textstyle\sum_k a_k\theta_k", r":", r"\text{a linear functional}", font_size=34),
            cmath(r"\text{smooth } L", r":", r"a_k \text{ decay fast: \ the bias is averaged away}", font_size=34),
            cmath(r"\Pi(L(\theta) \mid Y)", r"\approx", r"N\big(\hat L, \mathrm{Var}(\hat L)\big): \ \text{BvM holds for } L", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{BvM can hold for a functional, \ not automatically for the function in a strong norm}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(BALLC)
        whys = [why(r"a mean, \ an integral, \ a coefficient"), why(r"low-frequency weighting"), why(r"Castillo \& Nickl (2013)"), why(r"Freedman, \ resolved")]
        heading = label('A smooth functional can be asymptotically normal despite global failure', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> But for a linear functional, a weighted sum of the coefficients like a mean or an integral, the picture changes. <bookmark mark='b'/> If the weights decay fast, the functional depends mainly on low frequencies, where the data dominate the prior, and the high-frequency bias averages away. <bookmark mark='c'/> Then the marginal posterior of the functional is asymptotically the normal sampling distribution of an efficient estimator: a Bernstein–von Mises theorem for the functional. <bookmark mark='d'/> The lesson, made precise by Ismaël Castillo and Richard Nickl: Bernstein–von Mises can hold for smooth aspects of an infinite-dimensional parameter, while strong-norm infinite-dimensional BvM can fail. Weaker-norm theorems are a distinct possibility."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def castillo(self):
        rows = fit_rows(VGroup(
            label(r"semiparametric BvM \ (Castillo \& Rousseau 2015):", font_size=28, color=GREY_A),
            label(r"for $\psi(P)$ smooth, \ the marginal posterior of $\psi$ \ $\approx$ \ $N(\hat\psi, I_\psi^{-1}/n)$, \ $I_\psi$ efficient (Part 49)", font_size=26, color=GOODC),
            label(r"conditions: \ the prior must not be too biased in the direction of the efficient influence function", font_size=26, color=FREQC),
            label(r"failures: \ priors that ignore a nuisance can give the wrong centre (Rivoirard \& Rousseau 2012)", font_size=26, color=BADC),
            label(r"in causal inference: \ least-favourable outcome-prior alignment can remove bias (Ray \& van der Vaart 2020)", font_size=26, color=BALLC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The general theory is Ismaël Castillo and Judith Rousseau's of 2015. <bookmark mark='b'/> For a smooth functional of the distribution, the marginal posterior is asymptotically normal, centred at an efficient estimator with the efficient variance of Part forty-nine. <bookmark mark='c'/> The condition is that the prior is not too biased in the direction of the efficient influence function. <bookmark mark='d'/> When it is, the posterior can centre in the wrong place, as Vincent Rivoirard and Rousseau showed for densities. <bookmark mark='e'/> And in causal inference, Kolyan Ray and Aad van der Vaart showed in 2020 that aligning the outcome-regression prior with a least-favourable direction involving an estimated propensity score can remove bias under overlap and nuisance-rate conditions. An unrelated prior on the propensity score is not sufficient."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
