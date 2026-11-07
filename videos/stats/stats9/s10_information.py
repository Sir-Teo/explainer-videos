from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class Information(VoiceoverScene):
    def construct(self):
        self.card()
        self.mean_zero()
        self.variance()
        self.scores()
        self.catalogue()
        self.bernoulli()
        self.reparam()
        self.matrix()
        self.kl_curvature()

    def card(self):
        card = chapter_card(9, r"Fisher information", r"How much does one observation say about $\theta$?", part=PART)
        with self.voiceover("Chapter nine. Fisher information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def mean_zero(self):
        rows = [
            cmath(r"u_\theta(x)", r"=", r"\frac{\partial}{\partial\theta}\log p_\theta(x) = \frac{\partial_\theta p_\theta(x)}{p_\theta(x)}",
                  font_size=34),
            cmath(r"E_\theta\, u_\theta(X)", r"=", r"\int \frac{\partial_\theta p_\theta(x)}{p_\theta(x)}\,p_\theta(x)\,dx", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"\frac{\partial}{\partial\theta}\int p_\theta(x)\,dx", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"\frac{\partial}{\partial\theta}\,1 = 0", font_size=34),
        ]
        rows[3][2].set_color(LIK)
        whys = [why(r"the score of one observation"), why(r"average it under the same $\theta$"),
                why(r"swap derivative and integral: \ the regularity conditions"), why(r"the score is centred at the truth")]
        intro = label('Why a regular score has mean zero', font_size=36)
        with self.voiceover(
            "Chapter five's standard error depended on something called the Fisher information. Here's what it is. "
            "<bookmark mark='a'/> Start with the score of a single observation, the derivative of its log-density. "
            "<bookmark mark='b'/> Average it, with the observation drawn from the same theta. The density in the "
            "denominator cancels the one we're averaging over. <bookmark mark='c'/> What's left is the derivative of the "
            "total probability, if we can swap the derivative and the integral, which is exactly what the regularity "
            "conditions guarantee. <bookmark mark='d'/> The total probability is always one, so its derivative is zero. "
            "The score has mean zero at the true parameter. Evaluated at the truth, the log-likelihood is, on average, "
            "flat."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def variance(self):
        dc = definition_card(r"Fisher information", r"$I(\theta) = \mathrm{Var}_\theta\, u_\theta(X) = E_\theta\, u_\theta(X)^2$",
                             color=LIK, width=8.4, font_size=30).move_to([0, 2.2, 0])
        rows = [
            cmath(r"0 = \frac{\partial}{\partial\theta}\int u_\theta\,p_\theta", r"=", r"\int \partial_\theta u_\theta\;p_\theta + \int u_\theta\;\partial_\theta p_\theta",
                  font_size=30),
            cmath(r"\vphantom{x}", r"=", r"E\,\partial_\theta u_\theta + E\,u_\theta^2", font_size=32),
            cmath(r"I(\theta)", r"=", r"-E_\theta\,\frac{\partial^2}{\partial\theta^2}\log p_\theta(X)", font_size=34),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"differentiate $E u = 0$ once more"), why(r"$\partial_\theta p = u\,p$"), why(r"variance of the slope $=$ mean curvature")]
        with self.voiceover(
            "<bookmark mark='a'/> The Fisher information is the variance of the score: how much the slope of the "
            "log-likelihood at the truth varies from one observation to the next. A big variance means the data push "
            "the slope hard one way or the other, so they carry a lot of information about theta. "
            "<bookmark mark='b'/> And there's a second formula. Differentiate the mean-zero identity again. By the "
            "product rule we get two terms. <bookmark mark='c'/> Since the derivative of p is the score times p, the "
            "second term is the mean squared score. <bookmark mark='d'/> So the information is also minus the average "
            "second derivative of the log-density: its average curvature. The variance of the slope equals the mean "
            "curvature. That's the identity chapter five needed: the denominator and the numerator of the Taylor "
            "argument are the same number."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            step = ladder(self, rows, whys, keep=3, top=0.9, x=-0.6, buff=0.5, edge=6.9)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scores(self):
        g = np.random.Generator(np.random.PCG64(1926))
        lam0, n, R = 0.7, 20, 40
        S_ = g.poisson(lam0, (R, n)).sum(1)
        lams = np.linspace(0.35, 1.4, 120)
        A = axes([0.35, 1.4], [-20, 30], x_length=7.2, y_length=4.6, xlabel=r"$\lambda$", ylabel=r"score $U(\lambda) = S/\lambda - n$",
                 xticks=[0.4, 0.7, 1.0, 1.3], yticks=[-20, -10, 0, 10, 20, 30], center=[-2.0, -0.3, 0])
        ax = A.ax
        cvs = VGroup(*[clip_curve(ax, lams, s_ / lams - n, LIK, 1.4, ymin=-20, ymax=30).set_stroke(opacity=0.55) for s_ in S_])
        zero = DashedLine(ax.c2p(0.35, 0), ax.c2p(1.4, 0), color=GREY_C, stroke_width=1.5)
        vl = DashedLine(ax.c2p(lam0, -20), ax.c2p(lam0, 30), color=EXACT, stroke_width=2)
        at = VGroup(*[Dot(ax.c2p(lam0, s_ / lam0 - n), radius=0.05, color=S.ACCENT) for s_ in S_])
        u0 = S_ / lam0 - n
        rows = fit_rows(VGroup(
            label(r"40 samples of $n = 20$, \ $\lambda_0 = 0.7$", font_size=24, color=GREY_A),
            MathTex(rf"\text{{at }}\lambda_0:\ \text{{mean }} {u0.mean():+.2f},\ \text{{var }} {u0.var():.1f}", font_size=28, color=S.ACCENT),
            MathTex(rf"n\,I(\lambda_0) = \frac{{n}}{{\lambda_0}} = {n / lam0:.1f}", font_size=28, color=LIK),
            MathTex(rf"\text{{mean slope at }}\lambda_0 = -\frac{{E S}}{{\lambda_0^2}} = -{n / lam0:.1f}", font_size=28, color=LIK),
            label(r"each curve crosses zero at its own $\hat\lambda = \bar x$", font_size=24, color=GREY_A),
        ), 5.2, 0.34, [4.3, -0.2, 0])
        tag = simulated_tag(r"simulated: \ Poisson samples", corner=DR)
        with self.voiceover(
            "Here's the picture. <bookmark mark='a'/> Forty Poisson samples of twenty, each drawn with lambda point "
            "seven. Each curve is one sample's score function. Each crosses zero at its own estimate. "
            "<bookmark mark='b'/> Now look along the line at the true value. The scores there scatter around zero: their "
            "mean is close to zero, and their variance is twenty-six, close to n over lambda, twenty-eight point six, "
            "for only forty samples. That's n times the information. <bookmark mark='c'/> And the curves' slopes at the truth average minus twenty-eight point "
            "six as well. A big spread at the truth goes with steep slopes, and steep slopes mean each curve crosses "
            "zero close to the truth. That's why the error of the MLE is about the spread divided by the slope: root n "
            "I over n I, one over root n I."
        ) as vo:
            self.play(FadeIn(A), Create(zero), Create(vl), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(at), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def catalogue(self):
        items = [
            (r"Bernoulli$(p)$", r"\frac{1}{p(1 - p)}", r"\frac{p(1-p)}{n}"),
            (r"Poisson$(\lambda)$", r"\frac{1}{\lambda}", r"\frac{\lambda}{n}"),
            (r"$N(\mu, \sigma^2)$, \ $\mu$", r"\frac{1}{\sigma^2}", r"\frac{\sigma^2}{n}"),
            (r"$N(\mu, \sigma^2)$, \ $\sigma^2$", r"\frac{1}{2\sigma^4}", r"\frac{2\sigma^4}{n}"),
            (r"Exponential$(\lambda)$", r"\frac{1}{\lambda^2}", r"\frac{\lambda^2}{n}"),
            (r"Cauchy, \ location (scale 1)", r"\frac12", r"\frac2n"),
        ]
        hdr = VGroup(label(r"model", font_size=24, color=GREY_B), label(r"$I(\theta)$", font_size=26, color=GREY_B),
                     label(r"$1/(nI)$", font_size=26, color=GREY_B))
        rows = VGroup(hdr)
        for nm, I, inv in items:
            rows.add(VGroup(label(nm, font_size=26, color=GREY_A), MathTex(I, font_size=32, color=LIK), MathTex(inv, font_size=32, color=S.ACCENT)))
        rows.arrange(DOWN, buff=0.22).move_to([-1.6, -0.2, 0])
        for r in rows:
            r[0].set_x(-4.6)
            r[1].set_x(-0.9)
            r[2].set_x(1.6)
        notes = fit_rows(VGroup(
            label(r"$1/(nI)$ is the MLE's large-sample variance", font_size=22),
            label(r"the normal: \ $\bar x$ achieves it exactly", font_size=22, color=GREY_A),
            label(r"the Cauchy: \ the median has", font_size=22, color=GREY_A),
            label(r"$\pi^2/(4n) = 2.47/n$; \ the MLE $2/n$", font_size=22, color=GREY_A),
        ), 3.8, 0.3, [4.6, -0.3, 0])
        with self.voiceover(
            "The information for the familiar models. <bookmark mark='a'/> For a coin, one over p times one minus p. "
            "For the Poisson, one over lambda. For a normal mean, one over sigma squared, and for its variance, one "
            "over two sigma to the fourth. For the exponential rate, one over lambda squared. And for the centre of a "
            "Cauchy distribution, one half. <bookmark mark='b'/> The last column, one over n I, is the variance the "
            "maximum likelihood estimator achieves in large samples. For the normal mean it's sigma squared over n, "
            "which x-bar achieves exactly. For the Cauchy it's two over n. The sample mean of Cauchy data doesn't "
            "converge at all, as Part 6 showed, and the median does reasonably well, at about two point four seven "
            "over n, but the MLE does better still."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[1:]], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(notes))
        self.clear_scene()

    def bernoulli(self):
        ps = np.linspace(0.01, 0.99, 200)
        A = axes([0, 1], [0, 0.3], x_length=6.0, y_length=3.8, xlabel=r"$p$", ylabel=r"$1/I(p) = p(1 - p)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.1, 0.2, 0.3], center=[-3.4, -0.3, 0])
        ax = A.ax
        cv = curve(ax, ps, ps * (1 - ps), LIK, 3.5)
        B = axes([0, 1], [0, 4.5], x_length=6.0, y_length=3.8, xlabel=r"$p$", ylabel=r"relative SE: \ $\sqrt{(1-p)/p}$ \ (per $\sqrt n$)",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2, 3, 4], center=[3.4, -0.3, 0])
        bx = B.ax
        ps2 = np.linspace(0.05, 0.99, 200)
        cv2 = curve(bx, ps2, np.sqrt((1 - ps2) / ps2), S.RESID, 3.5)
        foot = label(r"a fair coin is the hardest to pin down in absolute terms; \ a rare event, \ in relative terms", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.35)
        intro = label('Absolute error and relative error for a coin', font_size=36)
        with self.voiceover(
            "The coin's information has a lesson. <bookmark mark='a'/> One over the information is p times one minus "
            "p, largest at a half. A fair coin is the hardest coin to pin down: each toss is maximally unpredictable, "
            "and an unpredictable outcome is a noisy measurement. Near zero or one, the tosses are nearly all the same, "
            "and p is pinned down well, in absolute terms. <bookmark mark='b'/> But divide the standard error by p "
            "itself. For a rare event, a disease with prevalence one in a hundred, say, the relative error explodes: "
            "you need huge samples to see enough cases. Which picture matters depends on the question, and on the "
            "coordinates you measure in."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("b")
            self.play(FadeIn(B), Create(cv2))
            self.play(FadeIn(foot))
        self.clear_scene()

    def reparam(self):
        rows = [
            cmath(r"I_n(\theta)", r"=", r"n\,I(\theta)", r"\quad\text{independent observations add}", font_size=34),
            cmath(r"\theta = h(\eta):\quad I_\eta(\eta)", r"=", r"I_\theta\big(h(\eta)\big)\,h'(\eta)^2", font_size=34),
            cmath(r"\eta = \log\frac{p}{1-p}:\quad I_\eta", r"=", r"\frac{1}{p(1-p)}\cdot\big(p(1-p)\big)^2 = p(1 - p)", font_size=32),
            cmath(r"\mathrm{SE}(\hat\eta)", r"\approx", r"\frac{1}{\sqrt{n\,p(1-p)}}", r"\quad\text{the log-odds: hardest at the extremes}",
                  font_size=32),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"variances of independent scores add"), why(r"the chain rule on the score"),
                why(r"$dp/d\eta = p(1-p)$"), why(r"the delta method, \ again: \ Part 14's logistic regression")]
        intro = label('Information adds and transforms', font_size=36)
        with self.voiceover(
            "Two rules make information easy to work with. <bookmark mark='a'/> First, it adds: n independent identically distributed "
            "observations carry n times the information of one, which is where the root n in regular standard errors comes "
            "from. <bookmark mark='b'/> Second, it transforms by the chain rule. If theta is a function of some other "
            "parameter eta, the score picks up a factor of the derivative, and the information picks up its square. "
            "<bookmark mark='c'/> Measure a coin on the log-odds scale, the scale of logistic regression: the "
            "information becomes p times one minus p, now largest at a half. <bookmark mark='d'/> So on the log-odds "
            "scale, extreme probabilities are the hardest to estimate. Information isn't a property of the experiment "
            "alone; it depends on what you're asking."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def matrix(self):
        rows = [
            cmath(r"I(\theta)_{jk}", r"=", r"E_\theta\big[u_j\,u_k\big] = -E_\theta\,\frac{\partial^2 \log p_\theta}{\partial\theta_j\,\partial\theta_k}",
                  font_size=32),
            cmath(r"N(\mu, \sigma^2):\ \ I", r"=", r"\begin{pmatrix} 1/\sigma^2 & 0 \\ 0 & 1/(2\sigma^4) \end{pmatrix}", font_size=32),
            cmath(r"\sqrt n\,(\hat\theta - \theta)", r"\to", r"N\big(0,\ I(\theta)^{-1}\big)", font_size=34),
            cmath(r"\big(I^{-1}\big)_{11}", r"\ge", r"\frac{1}{I_{11}}", r"\quad\text{nuisance parameters cost information}", font_size=32),
        ]
        rows[2][2].set_color(LIK)
        rows[3][2].set_color(S.ACCENT)
        whys = [why(r"several parameters: \ a covariance matrix; positive definite to invert (Part 4)"), why(r"orthogonal: \ no first-order asymptotic information loss for $\mu$"),
                why(r"the multivariate version of ch.~5"), why(r"the Schur complement (Part 4); \ equality iff orthogonal")]
        with self.voiceover(
            "<bookmark mark='a'/> With several parameters, the information becomes a matrix: the covariance matrix of "
            "the score vector, or minus the average Hessian of the log-density. Being a covariance matrix, it's positive "
            "semidefinite. <bookmark mark='b'/> For the normal, it's diagonal: the mean and the variance are orthogonal "
            "parameters, so not knowing one costs no first-order asymptotic information for the other. Finite-sample uncertainty can still increase. <bookmark mark='c'/> The MLE is "
            "asymptotically normal with covariance matrix the inverse of the information. <bookmark mark='d'/> And here's "
            "a subtle fact from Part 4's Schur complement: the first diagonal entry of the inverse is at least one over "
            "the first diagonal entry. Not knowing the other parameters can only hurt. Unknown nuisance parameters cost "
            "information, unless they're orthogonal to the one you care about."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kl_curvature(self):
        lam0 = 0.7
        lams = np.linspace(0.2, 1.6, 200)
        kl = lam0 * np.log(lam0 / lams) - lam0 + lams
        A = axes([0.2, 1.6], [0, 0.6], x_length=6.8, y_length=4.2, xlabel=r"$\lambda$", ylabel=r"$\mathrm{KL}(0.7 \,\|\, \lambda)$, \ Poisson",
                 xticks=[0.2, 0.7, 1.2, 1.6], yticks=[0, 0.2, 0.4, 0.6], center=[-2.6, -0.3, 0])
        ax = A.ax
        cv = curve(ax, lams, kl, LIK, 3.5)
        par = DashedVMobject(clip_curve(ax, lams, 0.5 / lam0 * (lams - lam0) ** 2, S.ACCENT, 2.5, ymax=0.6), num_dashes=40)
        rows = fit_rows(VGroup(
            MathTex(r"\mathrm{KL}(\theta_0 \,\|\, \theta) \approx \tfrac12\, I(\theta_0)\,(\theta - \theta_0)^2", font_size=30, color=S.ACCENT),
            label(r"information: \ the curvature of the divergence at the truth", font_size=24),
            label(r"how fast nearby distributions become distinguishable", font_size=24, color=GREY_A),
            label(r"Rao (1945): \ $I$ as a Riemannian metric on the model, \ information geometry", font_size=22, color=GREY_A),
        ), 5.2, 0.34, [4.2, -0.2, 0])
        intro = label('Information as local KL curvature', font_size=36)
        with self.voiceover(
            "One last view, which ties this chapter to chapter five. <bookmark mark='a'/> Here is the Kullback–Leibler "
            "divergence from the true Poisson, with rate point seven, to every other Poisson. It's zero at the truth "
            "and grows on both sides. <bookmark mark='b'/> Near the bottom it's a parabola, and the parabola's curvature "
            "is the Fisher information, exactly. <bookmark mark='c'/> So information measures how quickly the "
            "distributions near the truth become distinguishable from it. Large information, a steep bowl: a slightly "
            "wrong parameter already predicts visibly different data. <bookmark mark='d'/> Rao noticed in 1945 that this "
            "makes the information a way of measuring distance on the space of models, a Riemannian metric, and that "
            "idea grew into the field of information geometry."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("b")
            self.play(Create(par), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
