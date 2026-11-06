from __future__ import annotations

import math

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamEstimation(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p3()
        self.p4()

    def card(self):
        card = chapter_card(2, r"Sitting II: \ estimation", r"Problems 3 and 4", lit=(1947, 1950, 1951), part=PART)
        with self.voiceover("Sitting two: estimation. A best unbiased estimator, one that cannot exist, and an admissibility proof."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 3
    def p3(self):
        d = load("umvue")
        ex = d["example"]
        card = ExamCard(3, r"a UMVUE, \ and a case with none", r"Part 45", [
            r"$X_1, \dots, X_n$ are i.i.d.\ Poisson($\lambda$). \ Find the UMVUE of $P(X = 0) = e^{-\lambda}$ and its variance,",
            r"and compare it with the Cram\'er--Rao bound and with the MLE $e^{-\bar X}$.",
            r"Then show that for $X \sim$ Binomial($n, p$) \ no unbiased estimator of $1/p$ exists."], marks=10, color=ESTC5)
        self.pose_voiceover(
            "Problem three. Given n independent Poisson counts with mean lambda, find the uniformly minimum-variance unbiased "
            "estimator of the chance of a zero, e to the minus lambda, and its variance. Compare it with the Cramér–Rao "
            "bound and with the maximum likelihood estimator. Then show that for a binomial count, no unbiased estimator of "
            "one over p exists at all. Pause and try it.", card)
        rows = [
            cmath(r"T = \textstyle\sum X_i", r":", r"\text{sufficient and complete \ (a full-rank exponential family)}", font_size=32),
            cmath(r"E[1\{X_1 = 0\} \mid T]", r"=", r"P(X_1 = 0 \mid T) = (1 - 1/n)^T, \ \ X_1 \mid T \sim \mathrm{Bin}(T, 1/n)", font_size=30),
            cmath(r"\text{Lehmann--Scheff\'e}", r":", r"(1 - 1/n)^T \text{ is the UMVUE}", font_size=34),
            cmath(r"\mathrm{Var}", r"=", r"E(1 - \tfrac1n)^{2T} - e^{-2\lambda} = e^{-2\lambda}(e^{\lambda/n} - 1) > \frac{\lambda e^{-2\lambda}}{n}", font_size=32),
        ]
        rows[2][-1].set_color(ESTC5)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"Part 45"), why(r"Rao--Blackwell a crude unbiased start"), why(r"unique, \ by completeness"), why(r"the Poisson pgf; \ the CR bound")]
        self.steps_voiceover("<bookmark mark='a'/> The total count T is sufficient, and complete, because the Poisson is a full-rank "
                   "exponential family. <bookmark mark='b'/> Start from the crudest unbiased estimator, the indicator that the "
                   "first count is zero, and Rao–Blackwellize it. Given T, the first count is binomial with T trials and "
                   "chance one over n, so the conditional probability of a zero is one minus one over n, to the T. <bookmark "
                   "mark='c'/> By Lehmann and Scheffé, an unbiased function of a complete sufficient statistic is the UMVUE. "
                   "<bookmark mark='d'/> Its variance, from the Poisson generating function, is e to the minus two lambda "
                   "times e to the lambda over n, minus one: strictly above the Cramér–Rao bound, lambda e to the minus two "
                   "lambda over n, because the bound is attained only by linear functions of T.", rows, whys, keep=3)
        self.clear_but(card)
        self.p3_chart(d, card)
        rows = [
            cmath(r"E_p\, g(X)", r"=", r"\textstyle\sum_{k=0}^n g(k)\binom nk p^k (1 - p)^{n-k}: \ \text{a polynomial of degree} \le n", font_size=30),
            cmath(r"1/p", r":", r"\to \infty \text{ as } p \to 0: \ \text{no polynomial equals it on } (0, 1)", font_size=32),
            cmath(r"\text{so}", r":", r"\text{no unbiased estimator; \ a fortiori no UMVUE}", font_size=34),
            cmath(r"\text{and}", r":", r"\text{the unbiased can be absurd: \ } (-1)^X \text{ for } e^{-2\lambda} \ (\text{Part 45})", font_size=32),
        ]
        rows[2][-1].set_color(S.RESID)
        whys = [why(r"finitely many outcomes"), why(r"unbounded near 0"), why(r"unbiasedness can be impossible"), why(r"or ridiculous")]
        self.steps_voiceover("<bookmark mark='a'/> The second half. Whatever g is, its expectation under a binomial with n trials is a "
                   "sum of n plus one terms, a polynomial in p of degree at most n. <bookmark mark='b'/> One over p goes to "
                   "infinity as p goes to zero, and no polynomial does that on the open interval. <bookmark mark='c'/> So no "
                   "unbiased estimator of one over p exists, and certainly no best one. <bookmark mark='d'/> Unbiasedness can "
                   "also be absurd: from a single Poisson count, the only unbiased estimator of e to the minus two lambda is "
                   "minus one to the X, which says a probability is minus one, as Part forty-five showed.", rows, whys)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Completeness of the sufficient statistic, <bookmark mark='b'/> "
                       "Rao–Blackwellization of a crude unbiased start, <bookmark mark='c'/> Lehmann–Scheffé for uniqueness, "
                       "<bookmark mark='d'/> and a generating function for the exact variance.", [(r"complete sufficient $T$", 45), (r"Rao--Blackwell \ $1\{X_1 = 0\}$", 45),
                        (r"Lehmann--Scheff\'e", 45), (r"the pgf: \ its variance", 43)], "abcd", color=ESTC5)

    def p3_chart(self, d, card):
        lam = np.asarray(d["lams"])
        n5 = d["5"]
        cr = np.asarray(n5["crlb"])
        ru = np.asarray(n5["var_umvue"]) / cr
        rm = np.asarray(n5["mle_mse"]) / cr
        A = axes([0, 5], [0.5, 3.4], x_length=6.8, y_length=3.4, xlabel=r"$\lambda$, \ $n = 5$", ylabel=r"risk / Cram\'er--Rao bound",
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[1, 2, 3], center=CHART)
        ax = A.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(5, 1), color=WHITE, stroke_width=2)
        cu = polyline(ax, lam, ru, ESTC5, 4)
        cm = polyline(ax, lam, rm, S.EST, 4)
        ex = d["example"]
        side = fit_rows(VGroup(
            label(r"variance or MSE, \ divided by the bound", font_size=22),
            label(r"gold: \ the UMVUE, \ above 1 everywhere", font_size=22, color=ESTC5),
            label(r"blue: \ the MLE $e^{-\bar X}$: \ biased; \ better only for $\lambda < 1$", font_size=22, color=S.EST),
            label(rf"$n = 10$, \ $\lambda = 2$: \ {ex['var_umvue']:.5f} \ vs \ {ex['crlb']:.5f} \ vs \ MLE {ex['mle_mse']:.5f}", font_size=22, color=GREY_A),
            label(rf"Monte Carlo: \ mean {d['mc']['mean']:.4f}, \ variance {d['mc']['var']:.5f}", font_size=22, color=PROOFC),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> Each estimator's risk divided by the Cramér–Rao bound, for five observations. <bookmark "
            f"mark='b'/> The UMVUE, in gold, sits above one for every lambda: the bound is not attained. <bookmark "
            f"mark='c'/> The maximum likelihood estimator, e to the minus the sample mean, is biased. For lambda below about one its "
            f"mean squared error is below the UMVUE's variance, and even below the bound, which constrains only unbiased "
            f"estimators; for larger lambda it is worse, three times the bound by lambda five. <bookmark mark='d'/> With ten observations and lambda two: a variance of {say(ex['var_umvue'], 5)} "
            f"against a bound of {say(ex['crlb'], 5)}, and an MLE error of {say(ex['mle_mse'], 5)}. <bookmark mark='e'/> A "
            f"simulation of two hundred thousand totals confirms the mean and the variance."
        ) as vo:
            self.play(FadeIn(A), FadeIn(one), FadeIn(exact_tag(r"exact; \ one check by simulation")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 4
    def p4(self):
        d = load("blyth")
        card = ExamCard(4, r"admissibility by Blyth's method", r"Part 45", [
            r"$X \sim N(\theta, 1)$, \ squared-error loss. \ Using the priors $\pi_\tau(\theta) = e^{-\theta^2/2\tau^2}$ (unnormalized),",
            r"prove that $\delta(X) = X$ is admissible.",
            r"Where does the same argument fail for $X \sim N(\theta, I_2)$, \ and what is true there?"], marks=10, color=ESTC5)
        self.pose_voiceover(
            "Problem four. One observation from a normal with unknown mean theta and variance one, and squared error loss. "
            "Using the unnormalized normal priors with scale tau, prove that the estimator X itself is admissible: no other "
            "estimator does at least as well for every theta and strictly better for some. Then say where the same argument "
            "fails in two dimensions, and what is true there. Pause and try it.", card)
        rows = [
            cmath(r"\text{suppose}", r":", r"R(\theta, \delta') \le 1 \ \forall\theta, \ \ < 1 - \varepsilon \text{ on an interval } I", font_size=32),
            cmath(r"\delta_\tau", r"=", r"\frac{\tau^2}{1 + \tau^2}X: \ \ r(\pi_\tau, X) - r(\pi_\tau, \delta_\tau) = \frac{\sqrt{2\pi}\,\tau}{1 + \tau^2}", font_size=32),
            cmath(r"\varepsilon \textstyle\int_I \pi_\tau", r"\le", r"r(\pi_\tau, X) - r(\pi_\tau, \delta') \le r(\pi_\tau, X) - r(\pi_\tau, \delta_\tau)", font_size=32),
            cmath(r"\tau \to \infty", r":", r"\text{left} \to \varepsilon |I| > 0, \ \ \text{right} \to 0: \ \text{contradiction}", font_size=32),
        ]
        rows[1][-1].set_color(ESTC5)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"risks are continuous in $\theta$"), why(r"the Bayes rule and its gap, \ times the prior's mass"), why(r"$\delta_\tau$ is Bayes"), why(r"so no such $\delta'$")]
        self.steps_voiceover("<bookmark mark='a'/> Suppose some estimator delta prime dominates X. X has risk one everywhere, so delta "
                   "prime's risk is at most one, and since risks of estimators in this family are continuous, it is below one "
                   "minus epsilon on some interval. <bookmark mark='b'/> Under the prior with scale tau, the Bayes rule shrinks "
                   "X by tau squared over one plus tau squared, and the gap between X's Bayes risk and the Bayes rule's, "
                   "multiplied by the prior's total mass, is the root of two pi times tau over one plus tau squared. "
                   "<bookmark mark='c'/> Delta prime's advantage over X, integrated against the prior, is at least epsilon times "
                   "the prior's mass on the interval, and it can be no larger than the Bayes rule's advantage. <bookmark "
                   "mark='d'/> As tau grows, the left side tends to epsilon times the interval's length, while the right "
                   "side goes to zero. That is impossible, so X is admissible.", rows, whys)
        self.clear_but(card)
        self.p4_chart(d, card)
        rows = [
            cmath(r"d = 2", r":", r"\text{gap} \times \text{mass} = \frac{2}{1 + \tau^2}\cdot 2\pi\tau^2 \to 4\pi: \ \text{no contradiction}", font_size=32),
            cmath(r"\text{but}", r":", r"X \text{ is still admissible in } \mathbb R^2 \ (\text{Stein 1956; \ Brown 1971, \ smarter priors})", font_size=30),
            cmath(r"d \ge 3", r":", r"X \text{ is inadmissible: \ James--Stein dominates it (Part 45)}", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{Blyth's method needs priors whose Bayes-risk gap vanishes}", font_size=32),
        ]
        rows[2][-1].set_color(S.RESID)
        whys = [why(r"the gap $d/(1 + \tau^2)$, \ the mass $(2\pi\tau^2)^{d/2}$"), why(r"recurrence of Brownian motion"), why(r"transience"), why(r"a method, \ not a theorem")]
        self.steps_voiceover("<bookmark mark='a'/> In two dimensions the same priors give a gap of two over one plus tau squared, but the "
                   "prior's mass grows like two pi tau squared, so the product tends to four pi, not zero, and there is no "
                   "contradiction. <bookmark mark='b'/> X is nevertheless admissible in the plane, as Charles Stein showed, and "
                   "Lawrence Brown's 1971 theory explains why, with priors that are flatter than normal. <bookmark mark='c'/> "
                   "In three or more dimensions it is inadmissible: the James–Stein estimator dominates it. Brown linked the "
                   "boundary to the recurrence of Brownian motion in one and two dimensions and its transience in three. "
                   "<bookmark mark='d'/> So Blyth's method is a method, not a theorem: it works when you can find priors whose "
                   "Bayes-risk gap vanishes faster than their mass grows.", rows, whys)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Assume a dominating estimator and use continuity, <bookmark "
                       "mark='b'/> compute Bayes rules for a sequence of flattening priors, <bookmark mark='c'/> show the "
                       "Bayes-risk gap times the prior mass vanishes, <bookmark mark='d'/> and know the boundary: Stein's "
                       "dimension three, where Part forty-four's Brownian motion stops returning home.", [(r"a dominating $\delta'$, \ continuity", 45), (r"Bayes rules for $\pi_\tau$", 45),
                        (r"gap $\times$ mass $\to 0$", 45), (r"$d \ge 3$: \ Stein; \ recurrence", 44)], "abcd", color=ESTC5)

    def p4_chart(self, d, card):
        lt = np.log10(np.asarray(d["taus"]))
        A = axes([-0.6, 2.5], [-2.2, 4.3], x_length=6.8, y_length=3.4, xlabel=r"prior scale $\tau$ \ (log scale)", ylabel=r"$\log_{10}$(gap $\times$ mass)",
                 xticks=[0, 1, 2], xfmt=lambda v: f"{10 ** v:g}", yticks=[-2, 0, 2, 4], center=CHART)
        ax = A.ax
        c1 = polyline(ax, lt, np.log10(d["d1"]), PROOFC, 4)
        c2 = polyline(ax, lt, np.log10(d["d2"]), ESTC5, 4)
        c3 = clip_curve(ax, lt, np.log10(d["d3"]), S.RESID, 4, ymin=-2.2, ymax=4.3)
        lim = DashedLine(ax.c2p(-0.6, math.log10(4 * math.pi)), ax.c2p(2.5, math.log10(4 * math.pi)), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$\frac{d}{1 + \tau^2}\,(2\pi\tau^2)^{d/2}$, \ exact", font_size=22),
            label(rf"green: \ $d = 1$: \ {d['d1'][-1]:.4f} at $\tau = 300$, \ falling like $1/\tau$", font_size=22, color=PROOFC),
            label(r"gold: \ $d = 2$: \ levels off at $4\pi$", font_size=22, color=ESTC5),
            label(r"red: \ $d = 3$: \ grows like $\tau$", font_size=22, color=S.RESID),
        ), 4.6, 0.4, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The quantity that must vanish, computed exactly, against the prior scale. <bookmark "
            f"mark='b'/> In one dimension it falls like one over tau, to {say(d['d1'][-1], 4)} at tau three hundred: Blyth's "
            f"argument goes through. <bookmark mark='c'/> In two it levels off at four pi. <bookmark mark='d'/> In three it "
            f"grows without bound."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c2), Create(lim), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c3), FadeIn(side[3]))
        self.clear_but(card)
