from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Information(VoiceoverScene):
    def construct(self):
        self.card()
        self.multi()
        self.normal()
        self.bhattacharyya()
        self.chart()
        self.chapman()
        self.uniform()
        self.hodges()

    def card(self):
        card = chapter_card(8, r"Information inequalities", r"How small can a variance be?", lit=(1945, 1946), part=PART)
        with self.voiceover("Chapter eight. Information inequalities: how small can the variance of an unbiased estimator be?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multi(self):
        rows = [
            cmath(r"s_\theta = \nabla \log p_\theta(X)", r":", r"E s = 0, \ \ \mathrm{Cov}\, s = I(\theta)", font_size=32),
            cmath(r"E_\theta T = g(\theta)", r"\Rightarrow", r"\mathrm{Cov}(T, s) = \nabla g(\theta)^\top", font_size=32),
            cmath(r"\mathrm{Cov}\begin{pmatrix} T \\ s \end{pmatrix} \succeq 0", r"\Rightarrow", r"\mathrm{Var}\, T \ge \nabla g^\top I(\theta)^{-1} \nabla g", font_size=32),
            cmath(r"\text{equality}", r"\iff", r"T - g(\theta) = c(\theta)^\top s_\theta: \ \text{an exponential family}", font_size=30),
        ]
        rows[2][-1].set_color(MMC)
        whys = [why(r"the score"), why(r"differentiate under the integral"), why(r"a Schur complement"), why(r"chapter 4's dual coordinates")]
        with self.voiceover(
            "<bookmark mark='a'/> First the general Cramér–Rao bound, for a vector parameter. Assume a regular model "
            "with justified differentiation of expectations, finite second moments and nonsingular information. The "
            "score then has mean zero and covariance equal to the Fisher information matrix. <bookmark mark='b'/> If "
            "T is unbiased for g of theta, differentiating its expectation under the integral shows that the "
            "covariance of T with the score is the gradient of g. <bookmark mark='c'/> The joint covariance matrix of"
            " T and the score is positive semidefinite, and its Schur complement gives the bound: the variance of T "
            "is at least the gradient of g, times the inverse information, times the gradient again. <bookmark "
            "mark='d'/> Equality needs T to be an affine function of the score, at the parameter value in question. A"
            " global exponential-family characterization requires additional regularity; being an exponential family "
            "alone does not make every target efficient."
        ) as vo:
            heading=label('The regular information bound is a covariance inequality',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def normal(self):
        d = load("info")
        e = d["eff_s2"]
        rows = [
            cmath(r"N(\mu, \sigma^2)", r":", r"I = n\,\mathrm{diag}(1/\sigma^2, \ 1/(2\sigma^4))", font_size=34),
            cmath(r"\text{bound for } \sigma^2", r":", r"2\sigma^4 / n; \ \ s^2 \text{ has } 2\sigma^4/(n - 1)", font_size=34),
            cmath(r"\text{efficiency } \tfrac{n - 1}{n}", r":", rf"{e[0]:.2f}, \ {e[1]:.2f}, \ {e[2]:.2f} \ \ (n = 5, 10, 50)", font_size=32),
            cmath(r"[I^{-1}]_{11} \ge 1/I_{11}", r":", r"\text{not knowing a nuisance parameter costs, \ unless } I_{12} = 0", font_size=30),
        ]
        rows[2][-1].set_color(MMC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"two parameters"), why(r"the UMVUE misses it"), why(r"so no unbiased estimator attains it"), why(r"orthogonal parameters")]
        with self.voiceover(
            f"<bookmark mark='a'/> For the normal with unknown mean and variance, the information matrix is diagonal. "
            f"<bookmark mark='b'/> The bound for the variance is two sigma to the fourth over n, but the sample variance, "
            f"the UMVUE, has two sigma to the fourth over n minus one. <bookmark mark='c'/> Its efficiency is n minus one over "
            f"n: {say(e[0], 1)} at five observations, {say(e[2], 2)} at fifty. Since the UMVUE is best among unbiased "
            f"estimators, no unbiased estimator attains the bound. <bookmark mark='d'/> The matrix form also prices "
            f"ignorance: the bound for one parameter with the others unknown uses the inverse matrix's diagonal entry, which "
            f"is at least one over the information's entry, with equality only when the parameters are orthogonal, as the "
            f"normal's mean and variance are."
        ) as vo:
            heading=label('A valid lower bound need not be attainable',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bhattacharyya(self):
        rows = [
            cmath(r"s_j", r"=", r"\partial_\theta^j p_\theta / p_\theta, \ \ j = 1, \ldots, k", font_size=34),
            cmath(r"\mathrm{Var}\, T", r"\ge", r"\mathbf g^\top J^{-1} \mathbf g, \ \ \mathbf g = (g', \ldots, g^{(k)}), \ J_{ij} = E s_i s_j", font_size=30),
            cmath(r"\theta^2 \text{ from } N(\theta, 1)", r":", r"J = \mathrm{diag}(n, 2n^2), \ \ \mathbf g = (2\theta, 2)", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\mathrm{Var}\, T \ge 4\theta^2/n + 2/n^2: \ \text{attained by } \bar x^2 - 1/n", font_size=32),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"higher derivatives"), why(r"project on more directions"), why(r"order 2"), why(r"Bhattacharyya (1946)")]
        with self.voiceover(
            "<bookmark mark='a'/> When the bound is not attained, it can be sharpened. Anil Bhattacharyya, in 1946, used "
            "the higher derivatives of the density, each divided by the density. <bookmark mark='b'/> Projecting T onto all "
            "of them, instead of the score alone, gives a larger lower bound. <bookmark mark='c'/> For theta squared from n "
            "normal observations, the first two of these functions are uncorrelated, with variances n and two n squared, "
            "and the derivatives of theta squared are two theta and two. <bookmark mark='d'/> The second-order bound is four "
            "theta squared over n plus two over n squared, and the UMVUE, x-bar squared minus one over n, attains it "
            "exactly."
        ) as vo:
            heading=label('Higher score derivatives sharpen an unbiased variance bound',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("info")
        th = np.asarray(d["theta"])
        n = d["n"]
        A = axes([0, 1], [0, 0.45], x_length=7.4, y_length=4.4, xlabel=r"$\theta$", ylabel=r"variance",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        k = th <= 1.0
        cu = polyline(ax, th[k], np.asarray(d["var_umvue"])[k], ADMC, 5)
        cc = polyline(ax, th[k], np.asarray(d["cr"])[k], MLEC, 4)
        side = fit_rows(VGroup(
            label(rf"$n = {n}$: \ estimate $\theta^2$", font_size=22),
            label(r"blue: \ Cram\'er--Rao, \ $4\theta^2/n$", font_size=22, color=MLEC),
            label(r"green: \ UMVUE $=$ Bhattacharyya", font_size=22, color=ADMC),
            label(rf"at $\theta = 0$: \ CR says 0; \ truth $2/n^2 = {2 / n ** 2:.2f}$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Drawn for ten observations. <bookmark mark='b'/> In blue the Cramér–Rao bound, four theta squared over n. <bookmark mark='c'/> In green the UMVUE's variance, which coincides with Bhattacharyya's second-order bound. <bookmark mark='d'/> The absolute gap is constant, two over n squared. Its relative size is largest at theta equal to zero, where the first derivative of theta squared vanishes and the Cramér–Rao bound says nothing at all, while the true minimum is two over n squared."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cu), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def chapman(self):
        rows = [
            cmath(r"E_\theta T = g(\theta)", r",", r"\ E_{\theta'} T = g(\theta')", font_size=34),
            cmath(r"g(\theta') - g(\theta)", r"=", r"\mathrm{Cov}_\theta\big(T, \ p_{\theta'}/p_\theta - 1\big)", font_size=32),
            cmath(r"\mathrm{Var}_\theta T", r"\ge", r"\sup_{\theta'} \frac{(g(\theta') - g(\theta))^2}{E_\theta (p_{\theta'}/p_\theta - 1)^2}", font_size=32),
            cmath(r"\text{nontrivial bound}", r":", r"P_{\theta'}\ll P_\theta;\ T,\ p_{\theta'}/p_\theta\in L^2(P_\theta)", font_size=32),
        ]
        rows[2][-1].set_color(MMC)
        whys = [why(r"unbiased at two points"), why(r"change of measure"), why(r"Cauchy--Schwarz"), why(r"Chapman \& Robbins (1951)")]
        with self.voiceover(
            "<bookmark mark='a'/> Douglas Chapman and Herbert Robbins removed the regularity altogether in 1951. Use "
            "unbiasedness at two parameter values, theta and theta prime. <bookmark mark='b'/> The difference of the "
            "two means is the covariance of T with the likelihood ratio minus one, by a change of measure. <bookmark "
            "mark='c'/> Cauchy–Schwarz bounds the variance of T below by the squared difference over the ratio's "
            "second moment, and we may take the supremum over theta prime. <bookmark mark='d'/> Comparison uses those"
            " theta prime whose model law is absolutely continuous with respect to the law at theta. Finite estimator"
            " variance and a finite likelihood-ratio second moment give a nontrivial bound; derivatives are not "
            "required. Letting theta prime approach theta recovers Cramér–Rao when the model is smooth."
        ) as vo:
            heading=label('Likelihood-ratio comparisons give derivative-free bounds',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uniform(self):
        d = load("info")
        ns = d["ns"]
        rows = [[r"$n$", r"Chapman--Robbins", r"UMVUE $\tfrac{n+1}{n}\max$", r"ratio", r"best $\theta'/\theta$"]]
        for n, b, u, t in zip(ns, d["cr_bound"], d["cr_umvue"], d["cr_t"]):
            rows.append([f"{n}", f"{b:.2e}", f"{u:.2e}", f"{b / u:.2f}", f"{t:.3f}"])
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.18, colors=[GREY_A] + [None] * len(ns)).move_to([0, 0.6, 0])
        note_ = fit_rows(VGroup(
            label(r"$U(0,\theta)$: moving support invalidates the regular score identities", font_size=24),
            label(r"both shrink like $1/n^2$, \ not the $1/n$ of regular models", font_size=24, color=MMC),
        ), 12.4, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The uniform on zero to theta is the standard non-regular case: the support moves "
            "with theta, and the interior score does not satisfy the usual zero-mean identity, and Part nine's tanks "
            "broke the Cramér–Rao bound. <bookmark mark='b'/> Chapman–Robbins still applies, with theta prime below "
            "theta. Here is its bound against the UMVUE's variance, for two up to a hundred observations. The ratio "
            "falls toward point six five, the maximum of s squared over e to the s minus one, and the best theta "
            "prime closes in on theta. <bookmark mark='c'/> Both shrink like one over n squared, faster than the "
            "usual regular root-n squared-error rate over a neighborhood. A biased estimator can still be "
            "superefficient at individual parameter values."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(note_[0]), FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def hodges(self):
        rows = fit_rows(VGroup(
            label(r"the bounds are for unbiased estimators, \ at each $\theta$ separately", font_size=26),
            label(r"Hodges (1951): \ $\hat\theta = \bar x$ unless $|\bar x| < n^{-1/4}$, \ then 0", font_size=26, color=INADC),
            label(r"beats $1/n$ at $\theta = 0$ \ (superefficiency), \ pays nearby", font_size=26, color=INADC),
            label(r"the right asymptotic statement is local and minimax: \ H\'ajek and Le Cam, \ Part 47", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A caution. These bounds are for unbiased estimators, one parameter value at a time. "
            "<bookmark mark='b'/> Joseph Hodges's estimator of 1951 uses the sample mean unless it is very close to zero, "
            "and then reports zero. <bookmark mark='c'/> At theta equal to zero it beats the information bound, a "
            "phenomenon called superefficiency, but it pays with large risk at parameter values near zero. <bookmark "
            "mark='d'/> The correct asymptotic version of the bound is local and minimax: Jaroslav Hájek's and Lucien Le "
            "Cam's theory, in Part forty-seven."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
