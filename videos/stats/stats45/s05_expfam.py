from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class ExpFamilies(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.duality()
        self.legendre()
        self.bregman()
        self.efficiency()
        self.pkd()

    def card(self):
        card = chapter_card(4, r"Exponential families as convex duality", r"One convex function holds the whole model", part=PART)
        with self.voiceover("Chapter four. Exponential families as convex duality: one convex function holds the whole model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"p_\eta(x)", r"=", r"h(x)\, \exp\{\eta\, T(x) - A(\eta)\}", font_size=36),
            cmath(r"A(\eta)", r"=", r"\log \textstyle\int h(x)\, e^{\eta T(x)}\, dx: \ \text{convex (H\"older)}", font_size=32),
            cmath(r"A'(\eta) = E_\eta T", r",", r"\ A''(\eta) = \mathrm{Var}_\eta T = I(\eta)", font_size=34),
            cmath(r"\text{the MLE}", r":", r"A'(\hat\eta) = \bar T: \ \text{match the mean}", font_size=34),
        ]
        rows[0][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(ADMC)
        rows[3][-1].set_color(MMC)
        whys = [why(r"natural parameter $\eta$"), why(r"the cumulant function"), why(r"differentiate under the integral"), why(r"the score is $T - A'(\eta)$")]
        with self.voiceover(
            "<bookmark mark='a'/> An exponential family has densities of this form: a base measure h, a statistic T, a "
            "natural parameter eta, and a normalizer A of eta. <bookmark mark='b'/> A is the log of the Laplace transform of "
            "h along T, and by Hölder's inequality it is convex. <bookmark mark='c'/> Its derivatives are the moments of T: "
            "the first is the mean, the second the variance, which is also the Fisher information about eta. <bookmark "
            "mark='d'/> The score is T minus A prime of eta, so the maximum likelihood estimate simply matches the model's "
            "mean of T to the sample's. Everything about the family is coded in the single convex function A."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def duality(self):
        d = load("expfam")
        eta = np.asarray(d["eta"])
        mu = np.asarray(d["mu"])
        A = axes([-4, 4], [0, 4.5], x_length=5.4, y_length=3.6, xlabel=r"$\eta$", ylabel=r"$A(\eta) = \log(1 + e^\eta)$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 2, 4], center=[-3.4, 0.7, 0])
        B = axes([0, 1], [-0.75, 0.05], x_length=5.4, y_length=3.6, xlabel=r"$\mu$", ylabel=r"$A^*(\mu)$",
                 xticks=[0, 0.5, 1], yticks=[-0.6, -0.3, 0], center=[3.4, 0.7, 0])
        ca = polyline(A.ax, eta, d["A"], MLEC, 4)
        cb = polyline(B.ax, mu, d["Astar"], JSC, 4)
        e0, a0, m0 = d["slope_at"], d["A_at"], d["mu_at"]
        tan = Line(A.ax.c2p(e0 - 2.2, a0 - 2.2 * m0), A.ax.c2p(e0 + 2.2, a0 + 2.2 * m0), color=MMC, stroke_width=3)
        dot_a = Dot(A.ax.c2p(e0, a0), radius=0.09, color=MMC)
        as0 = m0 * np.log(m0) + (1 - m0) * np.log(1 - m0)
        tb = Line(B.ax.c2p(m0 - 0.25, as0 - 0.25 * e0), B.ax.c2p(m0 + 0.25, as0 + 0.25 * e0), color=MMC, stroke_width=3)
        dot_b = Dot(B.ax.c2p(m0, as0), radius=0.09, color=MMC)
        side = fit_rows(VGroup(
            label(r"Bernoulli: \ $\eta = \log\frac{p}{1 - p}$, \ $T(x) = x$", font_size=22),
            label(rf"left: \ $A$; \ its slope at $\eta = {e0}$ is the mean $\mu = {m0:.3f}$", font_size=22, color=MMC),
            label(r"right: \ $A^*(\mu) = \mu \log \mu + (1 - \mu) \log(1 - \mu)$, \ minus the entropy", font_size=22, color=JSC),
            label(rf"its slope at $\mu = {m0:.3f}$ is back to $\eta = {e0}$: \ $(A^*)' = (A')^{{-1}}$", font_size=22, color=MMC),
        ), 12.4, 0.25, [0, -2.45, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The Bernoulli family, drawn. Its natural parameter is the log-odds, and its statistic is "
            f"the outcome itself. <bookmark mark='b'/> On the left, A of eta, the log of one plus e to the eta: convex, with "
            f"slope at each eta equal to the success probability. At eta equal to {say(e0, 1)}, the tangent's slope is "
            f"{say(m0, 2)}. <bookmark mark='c'/> On the right, its convex conjugate, A star of mu: mu log mu plus one minus "
            f"mu log one minus mu, which is minus the entropy of the coin. <bookmark mark='d'/> Its slope at mu equal to "
            f"{say(m0, 2)} is {say(e0, 1)} again. The two derivatives are inverse maps: one carries the natural parameter to "
            f"the mean, the other carries the mean back."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(exact_tag(r"exact: \ closed forms")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ca), Create(tan), FadeIn(dot_a), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(tb), FadeIn(dot_b), FadeIn(side[3]))
        self.clear_scene()

    def legendre(self):
        rows = [
            cmath(r"A^*(\mu)", r"=", r"\sup_\eta\, \{\eta \mu - A(\eta)\}", font_size=36),
            cmath(r"\ell(\eta)", r"=", r"n\{\eta \bar T - A(\eta)\} + \text{const}", font_size=34),
            cmath(r"\max_\eta \ell / n", r"=", r"A^*(\bar T): \ \text{the conjugate, at the data}", font_size=34),
            cmath(r"\text{mean-value parameter}", r":", r"\mu = A'(\eta) \in \text{the interior of the convex hull of } T", font_size=30),
        ]
        rows[0][-1].set_color(JSC)
        rows[2][-1].set_color(MMC)
        whys = [why(r"Legendre--Fenchel"), why(r"the log-likelihood"), why(r"maximum likelihood is a Legendre transform"), why(r"Barndorff-Nielsen (1978)")]
        with self.voiceover(
            "<bookmark mark='a'/> The conjugate is the Legendre–Fenchel transform: the largest gap between a line of slope "
            "mu and the curve A. <bookmark mark='b'/> And look at the log-likelihood of n observations: n times eta times the "
            "average of T, minus A of eta. <bookmark mark='c'/> Maximizing over eta is exactly the Legendre transform, "
            "evaluated at the sample mean of T. Maximum likelihood in an exponential family is convex duality. <bookmark "
            "mark='d'/> The two parametrizations, natural and mean-value, are dual coordinates, and the MLE exists exactly "
            "when the sample mean of T lies inside the convex hull of T's possible values, as Ole Barndorff-Nielsen showed "
            "in 1978. All heads, in a Bernoulli sample, lies on the edge: no finite log-odds."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bregman(self):
        d = load("expfam")
        rows = [
            cmath(r"D_{A^*}(\mu_1, \mu_2)", r"=", r"A^*(\mu_1) - A^*(\mu_2) - (A^*)'(\mu_2)(\mu_1 - \mu_2)", font_size=32),
            cmath(r"\mathrm{KL}(p_{\mu_1} \,\|\, p_{\mu_2})", r"=", r"D_{A^*}(\mu_1, \mu_2): \ \text{a Bregman divergence}", font_size=32),
            cmath(r"\mu_1 = 0.3, \ \mu_2 = 0.7", r":", rf"\mathrm{{KL}} = {d['kl']:.4f}, \ \ D_{{A^*}} = {d['bregman']:.4f}", font_size=32),
            cmath(r"\text{deviance}", r"=", r"2n\, D_{A^*}(\bar T, \hat\mu_0): \ \text{Part 24's, \ for any family}", font_size=32),
        ]
        rows[1][-1].set_color(JSC)
        rows[2][-1].set_color(MMC)
        whys = [why(r"the gap below a tangent"), why(r"the family's geometry"), why(r"two coins, \ checked"), why(r"likelihood-ratio tests")]
        with self.voiceover(
            f"<bookmark mark='a'/> Duality also gives the family its geometry. The Bregman divergence of a convex function "
            f"is the gap between the function and its tangent line. <bookmark mark='b'/> For A star, that gap is exactly the "
            f"Kullback–Leibler divergence between the two members of the family. <bookmark mark='c'/> For coins with "
            f"success probabilities point three and point seven, both are {say(d['kl'], 4)}. <bookmark mark='d'/> And the "
            f"deviance of Part twenty-four, the likelihood-ratio statistic, is twice n times the Bregman gap between the "
            f"sample mean and the fitted mean, in every exponential family at once."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def efficiency(self):
        d = load("expfam")
        eta = np.asarray(d["eta_p"])
        A = axes([-2.5, 1.8], [0, 6.2], x_length=7.4, y_length=4.4, xlabel=r"$\eta = \log \lambda$", ylabel=r"$e^\eta$",
                 xticks=[-2, -1, 0, 1], yticks=[0, 2, 4, 6], center=[-2.5, 0.2, 0])
        ca = polyline(A.ax, eta, d["A_p"], MLEC, 4)
        cv = DashedVMobject(polyline(A.ax, eta, d["V_p"], MMC, 4), num_dashes=40)
        side = fit_rows(VGroup(
            label(r"Poisson: \ $A(\eta) = e^\eta = A'(\eta) = A''(\eta)$", font_size=22, color=MLEC),
            label(r"in $\eta$: \ $I(\eta) = \lambda$; \ \ in $\lambda$: \ $I(\lambda) = 1/\lambda$", font_size=22, color=MMC),
            label(r"$\bar X$ is unbiased for $\lambda$ \ with variance $\lambda/n$: \ the bound, \ attained", font_size=22, color=ADMC),
            label(r"no unbiased estimator of $\eta = \log\lambda$ exists at all", font_size=22, color=INADC),
            label(r"the bound is attained only for $\mu = A'(\eta)$ \ (and linear maps of it)", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the Poisson family A is the exponential function, so the mean, the variance and A "
            "itself all coincide: one blue curve. <bookmark mark='b'/> Dashed in gold, the information about eta, the same curve "
            "again. The information about "
            "eta is lambda; about lambda it is one over lambda. <bookmark mark='c'/> The sample mean is unbiased for lambda "
            "with variance lambda over n, exactly the Cramér–Rao bound. <bookmark mark='d'/> But no unbiased estimator of "
            "the log of lambda exists at all, because a single zero count has positive probability. <bookmark mark='e'/> In "
            "general the Cramér–Rao bound is attained only by the mean-value parameter and affine functions of it, and only "
            "in exponential families: the bound singles out the family's dual coordinates."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ca), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def pkd(self):
        rows = fit_rows(VGroup(
            label(r"Pitman, \ Koopman, \ Darmois (1935--36):", font_size=28, color=S.ACCENT),
            label(r"if, \ for every $n$, \ a statistic of fixed dimension is sufficient \ (and the support does not move)", font_size=26),
            label(r"then the family is exponential", font_size=28, color=JSC),
            label(r"the exception that proves it: \ $U(0, \theta)$, \ whose support moves: \ $\max X_i$ suffices", font_size=26, color=MMC),
            label(r"the Cauchy family: \ nothing smaller than the whole sorted sample", font_size=26, color=INADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why do exponential families matter so much? Edwin Pitman, Bernard Koopman and Georges "
            "Darmois proved independently, in 1935 and 1936, <bookmark mark='b'/> that if a statistic of fixed dimension is "
            "sufficient for every sample size, and the support of the distribution does not depend on the parameter, <bookmark "
            "mark='c'/> then the family is exponential. Data reduction without loss, at every n, essentially characterizes "
            "them. <bookmark mark='d'/> The uniform on zero to theta escapes because its support moves; its maximum is "
            "sufficient. <bookmark mark='e'/> And the Cauchy location family, at the other extreme, admits no reduction below "
            "the sorted sample: the next chapter makes these ideas precise."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
