from __future__ import annotations

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamTesting(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p5()
        self.p6()

    def card(self):
        card = chapter_card(3, r"Sitting III: \ testing and asymptotics", r"Problems 5 and 6", lit=(1855, 1933, 1960), part=PART)
        with self.voiceover("Sitting three: testing and asymptotics. Neyman structure on John Snow's data, and local power."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 5
    def p5(self):
        d = load("snow")
        card = ExamCard(5, r"Neyman structure: \ Snow's Table IX", r"Part 46", [
            rf"London, \ 1854: \ {d['x']:,} cholera deaths in {d['e1']:,} houses supplied by Southwark \& Vauxhall,",
            rf"{d['y']} in {d['e2']:,} supplied by Lambeth. \ Model deaths as Poisson($e_i\lambda_i$), \ $e_i$ the houses.",
            r"Derive the UMPU test of $\lambda_1 = \lambda_2$, \ apply it, \ and give an exact 95\% interval for $\lambda_1/\lambda_2$."],
            marks=10, color=TESTC5)
        self.pose_voiceover(
            f"Problem five. In the first seven weeks of the 1854 epidemic, John Snow counted {d['x']:,} cholera deaths among "
            f"{d['e1']:,} houses supplied with water by the Southwark and Vauxhall company, which drew from the Thames below "
            f"the sewer outfalls, and {d['y']} among {d['e2']:,} supplied by Lambeth, which had moved its intake upstream. "
            f"Model the deaths as Poisson, with means proportional to the number of houses. Derive the uniformly most powerful "
            f"unbiased test of equal rates, apply it, and give an exact ninety-five percent interval for the rate ratio. "
            f"Pause and try it.", card)
        rows = [
            cmath(r"p(x, y)", r"\propto", r"\exp\big(x \log\tfrac{\lambda_1}{\lambda_2} + (x + y)\log\lambda_2\big): \ \psi = \log\tfrac{\lambda_1}{\lambda_2}, \ T = X + Y", font_size=30),
            cmath(r"X \mid T = t", r"\sim", r"\mathrm{Bin}(t, p), \ \ p = \frac{\rho e_1}{\rho e_1 + e_2}: \ \text{free of the nuisance } \lambda_2", font_size=32),
            cmath(r"\text{Neyman structure}", r":", r"T \text{ complete under } H_0 \Rightarrow \text{similar tests are level } \alpha \text{ in every slice}", font_size=30),
            cmath(r"\text{UMPU}", r"=", r"\text{the two-sided UMPU binomial test of } p = p_0 = \tfrac{e_1}{e_1 + e_2}, \text{ given } t", font_size=30),
        ]
        rows[1][-1].set_color(TESTC5)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"an exponential family"), why(r"condition on the nuisance's statistic"), why(r"Lehmann--Scheff\'e, \ for tests"), why(r"randomized at its two boundaries")]
        self.steps_voiceover("<bookmark mark='a'/> Write the joint probability as an exponential family. The parameter of interest is psi, "
                   "the log of the rate ratio, attached to X, and the nuisance rate attaches to the total, T. <bookmark "
                   "mark='b'/> Given the total, X is binomial, with a success probability that depends only on the ratio rho, "
                   "not on the nuisance. <bookmark mark='c'/> Under the null, T is sufficient and complete for the nuisance, so "
                   "every similar test has level alpha within every slice of T: that is Neyman structure. <bookmark mark='d'/> "
                   "So the optimal unbiased test is, slice by slice, the two-sided UMPU binomial test of p equal to the share "
                   "of houses, p zero.", rows, whys)
        self.clear_but(card)
        rows = [
            cmath(r"t = 1{,}361", r":", rf"p_0 = {d['p0']:.3f}: \ E X = {d['t'] * d['p0']:.0f}, \ \text{{observed}} \ {d['x']:,} \ (\hat p = {d['phat']:.3f})", font_size=32),
            cmath(r"z", r"=", rf"{d['z']:.1f}: \ \ P\text{{-value}} \approx 10^{{{d['log10p']:.0f}}}", font_size=36),
            cmath(r"\text{interval}", r":", r"\text{invert Clopper--Pearson for } p, \ \text{map } \rho = \frac{p}{1 - p}\cdot\frac{e_2}{e_1}", font_size=32),
            cmath(r"\hat\rho", r"=", rf"{d['ratio']:.2f}, \ \ 95\%: \ ({d['ci'][0]:.2f}, \ {d['ci'][1]:.2f})", font_size=36),
        ]
        rows[1][-1].set_color(S.RESID)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the slice Snow observed"), why(r"the normal approximation, \ for scale"), why(r"monotone in $\rho$"), why(r"eight times the death rate")]
        self.steps_voiceover(f"<bookmark mark='a'/> Snow's slice has {d['t']:,} deaths in all. Southwark and Vauxhall supplied "
                   f"{100 * d['p0']:.1f} percent of the houses, so under equal rates about {d['t'] * d['p0']:.0f} of the deaths "
                   f"should be theirs. They had {d['x']:,}, ninety-three percent. <bookmark mark='b'/> That is "
                   f"{say(d['z'], 1)} standard errors out: the P-value is about ten to the minus {abs(d['log10p']):.0f}. "
                   f"<bookmark mark='c'/> For the interval, invert the exact binomial test: take the Clopper–Pearson interval "
                   f"for p and map it to the rate ratio, which is increasing in p. <bookmark mark='d'/> The death rate in "
                   f"houses on the polluted supply was {say(d['ratio'], 2)} times Lambeth's, with an exact interval from "
                   f"{say(d['ci'][0], 2)} to {say(d['ci'][1], 2)}. Snow called it his grand experiment, because the two "
                   f"companies' pipes ran down the same streets.", rows, whys)
        self.clear_but(card)
        self.p5_sizes(d, card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        br = load("board")["rows"]
        show_board(self, board_rows("Poisson"),
                   f"<bookmark mark='a'/> The Board, with twenty thousand pairs of Poisson counts at a common rate of five. "
                   f"The unrandomized conditional test rejects only {100 * br[0]['achieved']:.1f} percent of the time: "
                   f"conservative, as the size chart said. <bookmark mark='b'/> The randomized UMPU test rejects "
                   f"{100 * br[1]['achieved']:.1f} percent, within simulation error of five: kept, as Neyman structure promises.",
                   [("a", [0]), ("b", [1])])
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Write the family with the parameter of interest separated, "
                       "<bookmark mark='b'/> condition on the nuisance's sufficient statistic, <bookmark mark='c'/> use "
                       "completeness, from Part forty-five, to show conditioning loses nothing, <bookmark mark='d'/> and "
                       "invert the test for an interval.", [(r"exponential family; \ $\psi$ and $T$", 46), (r"condition on $T$: \ binomial", 46),
                        (r"completeness: \ Neyman structure", 45), (r"invert: \ an exact interval", 46)], "abcd", color=TESTC5)

    def p5_sizes(self, d, card):
        lams = [1, 2, 5, 10, 20, 50]
        nr = [d["sizes"][str(l)][0] for l in lams]
        rr = [d["sizes"][str(l)][1] for l in lams]
        A = axes([-0.1, 1.8], [0, 0.06], x_length=6.8, y_length=3.4, xlabel=r"common rate $\lambda$ \ (log scale)", ylabel=r"unconditional size",
                 xticks=[0, 1, np.log10(50)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.025, 0.05], yfmt=lambda v: f"{v:.3f}", center=CHART)
        ax = A.ax
        lx = np.log10(lams)
        c_nr = VGroup(polyline(ax, lx, nr, S.RESID, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=S.RESID) for a, b in zip(lx, nr)])
        c_r = VGroup(polyline(ax, lx, rr, PROOFC, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=PROOFC) for a, b in zip(lx, rr)])
        side = fit_rows(VGroup(
            label(r"equal rates, \ equal exposures: \ the size, \ exactly", font_size=22),
            label(r"green: \ randomized UMPU: \ 0.050 at every $\lambda$", font_size=22, color=PROOFC),
            label(rf"red: \ unrandomized: \ {nr[0]:.4f} at 1, \ {nr[2]:.3f} at 5, \ {nr[-1]:.3f} at 50", font_size=22, color=S.RESID),
            label(rf"the toy $X = 12$, \ $Y = 4$: \ conditional $P = {d['toy']['p']:.3f}$", font_size=22, color=GREY_A),
        ), 4.6, 0.4, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> What the randomization buys, computed exactly by summing over the slices. <bookmark "
            f"mark='b'/> The randomized UMPU test has size exactly five percent at every common rate: similar, as Neyman "
            f"structure requires. <bookmark mark='c'/> The ordinary conditional test, which rejects only when the binomial "
            f"P-value is below five percent, has size {say(nr[0], 4)} when the rate is one, {say(nr[2], 3)} at five, and "
            f"creeps toward five percent only as the counts grow. <bookmark mark='d'/> A small example: twelve events against "
            f"four, with equal exposure, gives a conditional P-value of {say(d['toy']['p'], 3)}: not significant, though the "
            f"ratio is three."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c_r), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c_nr), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 6
    def p6(self):
        d = load("lan")
        card = ExamCard(6, r"LAN and local power", r"Part 47", [
            r"The logistic location model: \ density $f(x - \theta)$, \ $f(x) = e^{-x}/(1 + e^{-x})^2$.",
            r"Show the model is LAN with information $I = 1/3$. \ At $\theta = h/\sqrt n$, \ find the local power of the",
            r"one-sided level-$\alpha$ score test, \ the $t$-test and the sign test. \ Which is best, \ and by how much?"],
            marks=10, color=TESTC5)
        self.pose_voiceover(
            "Problem six. Observations come from the logistic distribution shifted by theta. Show that the model is locally "
            "asymptotically normal with Fisher information one third. Then, at alternatives theta equal to h over root n, "
            "find the local power of three one-sided tests at level alpha: the score test, the t-test and the sign test. "
            "Which is best, and by how much? Pause and try it.", card)
        rows = [
            cmath(r"\dot\ell(x)", r"=", r"\partial_\theta \log f(x - \theta)\big|_0 = 2F(x) - 1 = \tanh(x/2)", font_size=34),
            cmath(r"I", r"=", r"E\tanh^2(X/2) = \textstyle\int_0^1 (2u - 1)^2\,du = 1/3", font_size=34),
            cmath(r"\log\frac{dP^n_{h/\sqrt n}}{dP^n_0}", r"=", r"h\Delta_n - \tfrac{h^2}{6} + o_P(1), \ \ \Delta_n = \tfrac{1}{\sqrt n}\textstyle\sum\dot\ell(X_i) \rightsquigarrow N(0, \tfrac13)", font_size=30),
            cmath(r"\text{third lemma}", r":", r"T_n \text{ with } \mathrm{Cov}(T_n, \Delta_n) \to c \ \Rightarrow \ T_n \rightsquigarrow N(hc, \cdot) \text{ under } h/\sqrt n", font_size=30),
        ]
        rows[2][-1].set_color(TESTC5)
        whys = [why(r"$f'/f = 2F - 1$"), why(r"$F(X) \sim U(0, 1)$"), why(r"a smooth (DQM) model is LAN"), why(r"Le Cam (1960)")]
        self.steps_voiceover("<bookmark mark='a'/> The score of the logistic location model at zero is two F of x minus one, which is the "
                   "hyperbolic tangent of x over two. <bookmark mark='b'/> Its variance is the Fisher information: since F of "
                   "X is uniform, it is the integral of two u minus one squared, one third. <bookmark mark='c'/> The model is "
                   "smooth, differentiable in quadratic mean, so the log likelihood ratio for theta equal to h over root n is h "
                   "times the normalized score sum, minus h squared over six, plus a negligible term: local asymptotic "
                   "normality. <bookmark mark='d'/> Le Cam's third lemma then says that any statistic jointly normal with the "
                   "score, with covariance c, is shifted by h times c under the local alternative.", rows, whys)
        self.clear_but(card)
        rows = [
            cmath(r"\text{score}", r":", r"Z = \Delta_n/\sqrt I, \ c = \sqrt I \ \Rightarrow \ \pi(h) = 1 - \Phi(z_\alpha - h/\sqrt3)", font_size=32),
            cmath(r"t\text{-test}", r":", r"\sigma^2 = \pi^2/3 \ \Rightarrow \ \pi(h) = 1 - \Phi(z_\alpha - h\sqrt3/\pi)", font_size=32),
            cmath(r"\text{sign test}", r":", r"2f(0) = \tfrac12 \ \Rightarrow \ \pi(h) = 1 - \Phi(z_\alpha - h/2)", font_size=32),
            cmath(r"\text{AREs}", r":", rf"t: \ 9/\pi^2 = {d['are_t']:.3f}; \ \ \text{{sign}}: \ (1/2)^2/(1/3) = {d['are_sign']:.2f}", font_size=34),
        ]
        rows[0][-1].set_color(PROOFC)
        rows[3][-1].set_color(TESTC5)
        whys = [why(r"efficient: \ the envelope"), why(r"the mean's variance"), why(r"the median's density"), why(r"ratios of squared slopes (Pitman)")]
        self.steps_voiceover("<bookmark mark='a'/> For the score test itself, standardized by the root of I, the covariance is the root of "
                   "I, so its local power is one minus Phi of z alpha minus h over root three. That is the asymptotic power "
                   "envelope: no test does better. <bookmark mark='b'/> The t-test is based on the mean, whose variance for "
                   "the logistic is pi squared over three, so its slope is root three over pi. <bookmark mark='c'/> The sign "
                   "test is based on the median, whose slope is two times the density at zero, one half. <bookmark mark='d'/> "
                   "The asymptotic relative efficiencies, ratios of squared slopes, are nine over pi squared, ninety-one "
                   "percent, for the t-test, and three quarters for the sign test.", rows, whys)
        self.clear_but(card)
        self.p6_chart(d, card)
        self.p6_envelope(card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Compute the score, <bookmark mark='b'/> its variance, the "
                       "information, <bookmark mark='c'/> local asymptotic normality from quadratic-mean differentiability, "
                       "<bookmark mark='d'/> and Le Cam's third lemma, which turns covariances with the score into local "
                       "power.", [(r"the score $\tanh(x/2)$", 47), (r"information $1/3$", 45), (r"LAN, \ from DQM", 47),
                        (r"Le Cam's third lemma", 47)], "abcd", color=TESTC5)

    def p6_envelope(self, card):
        rows = [
            cmath(r"\text{any test } \phi_n", r":", r"\limsup E_{h/\sqrt n}\phi_n \le 1 - \Phi(z_\alpha - h\sqrt I) \ \text{ if } \limsup E_0\phi_n \le \alpha", font_size=30),
            cmath(r"\text{proof}", r":", r"\text{the limit experiment } N(h, I^{-1}) \text{: \ Neyman--Pearson there}", font_size=32),
            cmath(r"\text{estimators}", r":", r"\text{H\'ajek: \ regular } \sqrt n(T_n - \theta) \rightsquigarrow N(0, I^{-1}) * M", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the score test, \ and the MLE, \ are locally optimal}", font_size=32),
        ]
        rows[0][-1].set_color(TESTC5)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the power envelope"), why(r"Le Cam's limits of experiments"), why(r"the convolution theorem (1970)"), why(r"both sides of Part 47")]
        self.steps_voiceover(
            "<bookmark mark='a'/> Why is the score test the best possible? For any sequence of tests with asymptotic "
            "level alpha, the limiting power at h over root n is at most one minus Phi of z alpha minus h root I. "
            "<bookmark mark='b'/> The proof passes to the limit experiment, a single normal observation with mean h "
            "and variance one over I, where the Neyman–Pearson lemma decides everything. <bookmark mark='c'/> The same "
            "limit gives Hájek's convolution theorem for estimators: any regular estimator's limit law is the "
            "efficient normal convolved with extra noise. <bookmark mark='d'/> So the score test, and the maximum "
            "likelihood estimator, are locally optimal, which is the whole of Part forty-seven in one sentence.",
            rows, whys)
        self.clear_but(card)

    def p6_chart(self, d, card):
        hs = np.asarray(d["hs"])
        A = axes([0, 6], [0, 1], x_length=6.8, y_length=3.4, xlabel=r"local alternative $h$ \ ($\theta = h/\sqrt n$)", ylabel=r"power, \ $\alpha = 0.05$",
                 xticks=[0, 2, 4, 6], yticks=[0, 0.5, 1], center=CHART)
        ax = A.ax
        cs = {"score": (PROOFC, 4), "t": (S.EST, 4), "sign": (S.RESID, 4)}
        curves = {k: polyline(ax, hs, d[k], c, w) for k, (c, w) in cs.items()}
        dots = {k: VGroup(*[Dot(ax.c2p(h, p), radius=0.07, color=cs[k][0]) for h, p in zip(d["sim_h"], d["sim"][k])]) for k in cs}
        i = 2
        side = fit_rows(VGroup(
            label(r"lines: \ the limits; \ dots: \ $n = 400$, \ 4,000 runs", font_size=22),
            label(rf"green: \ score test: \ {d['score'][30]:.3f} at $h = 3$ \ (simulated {d['sim']['score'][i]:.3f})", font_size=22, color=PROOFC),
            label(rf"blue: \ $t$-test: \ {d['t'][30]:.3f} \ ({d['sim']['t'][i]:.3f})", font_size=22, color=S.EST),
            label(rf"red: \ sign test: \ {d['sign'][30]:.3f} \ ({d['sim']['sign'][i]:.3f})", font_size=22, color=S.RESID),
            label(r"the third lemma predicts finite-sample power", font_size=22, color=GREY_A),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The three local power curves, with simulations at n equal to four hundred. <bookmark "
            f"mark='b'/> At h equal to three, the score test's limiting power is {say(d['score'][30], 3)}, and the simulation "
            f"gives {say(d['sim']['score'][i], 3)}. <bookmark mark='c'/> The t-test: {say(d['t'][30], 3)}, simulated "
            f"{say(d['sim']['t'][i], 3)}. <bookmark mark='d'/> The sign test: {say(d['sign'][30], 3)}, simulated "
            f"{say(d['sim']['sign'][i], 3)}. <bookmark mark='e'/> Le Cam's limit is not just a theorem about infinity: at "
            f"four hundred observations it predicts the power to within a percentage point or two."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"limits exact; \ dots simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves["score"]), FadeIn(dots["score"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curves["t"]), FadeIn(dots["t"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(curves["sign"]), FadeIn(dots["sign"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)
