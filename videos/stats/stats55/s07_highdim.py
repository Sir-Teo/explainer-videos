from __future__ import annotations

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamHighDim(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p11()
        self.p12()

    def card(self):
        card = chapter_card(6, r"Sitting VI: \ the lasso and the posterior", r"Problems 11 and 12", lit=(1996, 2000, 2009), part=PART)
        with self.voiceover("Sitting six, the last: high-dimensional statistics and Bayesian asymptotics. The lasso's oracle inequality, and a posterior contraction rate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 11
    def p11(self):
        d = load("lasso")
        card = ExamCard(11, r"the lasso's oracle inequality", r"Part 52", [
            r"$y = X\beta^* + \varepsilon$, \ $\varepsilon \sim N(0, \sigma^2 I_n)$, \ $\|X_j\|^2 = n$, \ $\beta^*$ $s$-sparse on $S$, \ compatibility constant $\phi$.",
            r"For $\hat\beta = \arg\min \frac{1}{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1$, \ prove that on $\{\|X^\top\varepsilon/n\|_\infty \le \lambda/2\}$",
            r"$\|X(\hat\beta - \beta^*)\|^2/n \le 9s\lambda^2/\phi^2$ and $\|\hat\beta - \beta^*\|_1 \le 12s\lambda/\phi^2$; \ choose $\lambda$ so the event has probability $1 - \delta$."],
            marks=10, color=BAYC)
        self.pose_voiceover(
            "Problem eleven. A linear model with Gaussian noise, columns of the design scaled to have squared norm n, and a "
            "true coefficient vector with s nonzero entries, on a set S where the design satisfies the compatibility "
            "condition with constant phi. Prove that on the event that every column's correlation with the noise is at "
            "most lambda over two, the lasso's prediction error is at most nine s lambda squared over phi squared, and its "
            "l one error at most twelve s lambda over phi squared. Then choose lambda so that the event has probability one "
            "minus delta. Pause and try it.", card)
        rows = [
            cmath(r"\tfrac{1}{2n}\|X\Delta\|^2", r"\le", r"\tfrac1n\varepsilon^\top X\Delta + \lambda\big(\|\beta^*\|_1 - \|\hat\beta\|_1\big), \ \ \Delta = \hat\beta - \beta^*", font_size=30),
            cmath(r"\text{on the event}", r":", r"\tfrac{1}{2n}\|X\Delta\|^2 + \tfrac\lambda2\|\Delta_{S^c}\|_1 \le \tfrac{3\lambda}{2}\|\Delta_S\|_1 \ \Rightarrow \ \|\Delta_{S^c}\|_1 \le 3\|\Delta_S\|_1", font_size=28),
            cmath(r"\text{compatibility}", r":", r"\|\Delta_S\|_1 \le \sqrt s\,\|X\Delta\|/(\sqrt n\,\phi) \ \text{ on that cone}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\|X\Delta\|/\sqrt n \le 3\lambda\sqrt s/\phi: \ \ \tfrac1n\|X\Delta\|^2 \le \frac{9s\lambda^2}{\phi^2}, \ \ \|\Delta\|_1 \le 4\|\Delta_S\|_1 \le \frac{12 s\lambda}{\phi^2}", font_size=28),
        ]
        rows[1][-1].set_color(BAYC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the basic inequality: \ $\hat\beta$ beats $\beta^*$"), why(r"H\"older, \ and the triangle inequality on $S$"), why(r"van de Geer (2007)"), why(r"divide by $\|X\Delta\|$")]
        self.steps_voiceover("<bookmark mark='a'/> Start from the basic inequality: the lasso's objective at its minimizer is no larger "
                   "than at the truth. Expanding the squares leaves the prediction error on the left, and on the right the "
                   "noise's correlation with the error vector delta, plus lambda times the difference in l one norms. "
                   "<bookmark mark='b'/> On the event, Hölder's inequality bounds the noise term by lambda over two times the "
                   "l one norm of delta; splitting delta into its parts on S and off S, and using the triangle inequality, the "
                   "off-support part is at most three times the on-support part: delta lies in a cone. <bookmark mark='c'/> On "
                   "that cone, the compatibility condition bounds the on-support l one norm by root s times the prediction "
                   "norm, over phi. <bookmark mark='d'/> Substituting and dividing by the prediction norm gives the prediction "
                   "bound, nine s lambda squared over phi squared, and the cone gives the l one bound, twelve s lambda over phi "
                   "squared.", rows, whys)
        self.clear_but(card)
        rows = [
            cmath(r"X_j^\top\varepsilon/n", r"\sim", r"N(0, \sigma^2/n): \ \ P\big(\max_j |X_j^\top\varepsilon/n| > \lambda/2\big) \le 2p\,e^{-n\lambda^2/8\sigma^2}", font_size=30),
            cmath(r"\lambda", r"=", r"2\sigma\sqrt{2\log(2p/\delta)/n} \ \Rightarrow \ \text{probability} \ge 1 - \delta", font_size=32),
            cmath(r"\text{so}", r":", r"\tfrac1n\|X\Delta\|^2 \lesssim \frac{\sigma^2 s\log(p/\delta)}{\phi^2 n}: \ \text{the oracle's } \sigma^2 s/n, \ \text{times } \log p", font_size=30),
        ]
        rows[2][-1].set_color(PROOFC)
        whys = [why(r"a union bound over Gaussian tails \ (Part 51)"), why(r"solve for $\lambda$"), why(r"the price of not knowing $S$")]
        self.steps_voiceover("<bookmark mark='a'/> The event. Each column's correlation with the noise is normal with variance sigma "
                   "squared over n, and a union bound over the p columns, Part fifty-one's maximal inequality, bounds the "
                   "chance that any exceeds lambda over two. <bookmark mark='b'/> Taking lambda equal to two sigma times the "
                   "root of two log two p over delta, over n, makes it at most delta. <bookmark mark='c'/> So the prediction "
                   "error is of order sigma squared s log p over n: what an oracle that knew S would achieve, sigma squared s "
                   "over n, times only the logarithm of the number of candidate variables.", rows, whys)
        self.clear_but(card)
        self.p11_chart(d, card)
        self.p11_support(card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. The basic inequality, <bookmark mark='b'/> the noise event, "
                       "controlled by Part fifty-one's Gaussian maxima, <bookmark mark='c'/> the cone that the error must lie "
                       "in, <bookmark mark='d'/> and the compatibility condition, which turns the cone into a rate.", [(r"the basic inequality", 52), (r"the noise event: \ Gaussian maxima", 51), (r"the cone", 52),
                        (r"compatibility $\Rightarrow$ the rate", 52)], "abcd", color=BAYC)

    def p11_support(self, card):
        rows = [
            cmath(r"\text{compatibility}", r":", r"\text{enough for prediction and } \ell_1: \ \text{weaker than RIP}", font_size=34),
            cmath(r"\text{support recovery}", r":", r"\text{needs irrepresentability: \ } \|X_{S^c}^\top X_S(X_S^\top X_S)^{-1}\mathrm{sign}(\beta_S)\|_\infty < 1", font_size=32),
            cmath(r"\text{and a beta-min condition}", r":", r"\min_{j \in S}|\beta_j| \gtrsim \lambda\sqrt s / \phi^2", font_size=32),
            cmath(r"\text{so}", r":", r"\text{predicting well is easier than choosing the right variables}", font_size=32),
        ]
        rows[1][-1].set_color(BAYC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"van de Geer \& B\"uhlmann (2009)"), why(r"Zhao \& Yu; \ Wainwright (Part 52)"), why(r"signals above the noise"), why(r"Part 56's problem")]
        self.steps_voiceover(
            "<bookmark mark='a'/> What the theorem does not say. Compatibility, a condition on the design restricted "
            "to the cone, is enough for prediction and l one error; it is weaker than the restricted isometry property "
            "of compressed sensing. <bookmark mark='b'/> Recovering the exact set of variables needs much more: the "
            "irrepresentable condition of Zhao, Yu and Wainwright from Part fifty-two, which says the irrelevant "
            "variables are not too correlated with the relevant ones. <bookmark mark='c'/> And every true coefficient "
            "must be large compared with the noise. <bookmark mark='d'/> Predicting well is easier than choosing the "
            "right variables, which is why inference about the variables a lasso selects is the subject of Part "
            "fifty-six.",
            rows, whys)
        self.clear_but(card)

    def p11_chart(self, d, card):
        rows = d["rows"]
        ln = np.log10([r["n"] for r in rows])
        A = axes([1.95, 2.95], [-0.5, 2.1], x_length=6.8, y_length=3.4, xlabel=rf"$n$ \ (log scale), \ $p = {d['p']}$, \ $s = {d['s']}$", ylabel=r"$\log_{10}$ error",
                 xticks=[2, np.log10(200), np.log10(500), np.log10(800)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 1, 2], center=CHART)
        ax = A.ax

        def ln_(key, col, dash=False):
            c = polyline(ax, ln, np.log10([r[key] for r in rows]), col, 4)
            return DashedVMobject(c, num_dashes=30) if dash else c

        cp, cpb = ln_("pred", BAYC), ln_("pred_bound", BAYC, True)
        cl, clb = ln_("l1", S.EST), ln_("l1_bound", S.EST, True)
        r2 = [r for r in rows if r["n"] == 200][0]
        ev = min(r["event"] for r in rows)
        side = fit_rows(VGroup(
            label(r"Gaussian designs, \ 30 replications per $n$; \ $\phi^2 = 1/2$ assumed", font_size=22),
            label(rf"orange: \ prediction error, \ {r2['pred']:.2f} at $n = 200$ \ (bound {r2['pred_bound']:.1f})", font_size=22, color=BAYC),
            label(rf"blue: \ $\ell_1$ error, \ {r2['l1']:.2f} \ (bound {r2['l1_bound']:.0f})", font_size=22, color=S.EST),
            label(rf"the event held in at least {100 * ev:.0f}\% of runs", font_size=22, color=GREY_A),
            label(r"valid, \ loose by about 20, \ and the right slope", font_size=22, color=PROOFC),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The theorem against simulation: five hundred candidate variables, five of them real, and "
            f"Gaussian designs, with the compatibility constant squared taken as a half. <bookmark mark='b'/> The prediction "
            f"error, solid, is {say(r2['pred'], 2)} at two hundred observations; the bound, dashed, is {say(r2['pred_bound'], 1)}. "
            f"<bookmark mark='c'/> The l one error is {say(r2['l1'], 2)}, against a bound of {say(r2['l1_bound'], 0)}. "
            f"<bookmark mark='d'/> The noise event held in at least {100 * ev:.0f} percent of the runs. <bookmark mark='e'/> "
            f"The bounds are valid, loose by a factor of about twenty, and fall at the right rate, one over n."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bounds exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cp), Create(cpb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl), Create(clb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 12
    def p12(self):
        d = load("contract")
        card = ExamCard(12, r"a posterior contraction rate", r"Part 53", [
            r"$Y_k = \theta_k + Z_k/\sqrt n$, \ $k \ge 1$, \ with the prior $\theta_k \sim N(0, k^{-1-2\alpha})$ independently,",
            r"and a truth $\theta_0$ in the Sobolev ball $\sum k^{2\beta}\theta_{0k}^2 \le B$. \ Show the posterior contracts at",
            r"$\varepsilon_n = n^{-\min(\alpha, \beta)/(1 + 2\alpha)}$: \ $E_{\theta_0}\Pi(\|\theta - \theta_0\| > M_n\varepsilon_n \mid Y) \to 0$ for every $M_n \to \infty$."],
            marks=10, color=BAYC)
        self.pose_voiceover(
            "Problem twelve, the last. The Gaussian sequence model, with independent normal priors on the coefficients whose "
            "variances decay like k to the minus one minus two alpha, and a true sequence in a Sobolev ball of smoothness "
            "beta. Show that the posterior contracts around the truth at the rate n to the minus the smaller of alpha and "
            "beta, over one plus two alpha. Pause and try it.", card)
        rows = [
            cmath(r"\theta_k \mid Y", r"\sim", r"N\Big(w_k Y_k, \ \frac{\lambda_k}{1 + n\lambda_k}\Big), \ \ \lambda_k = k^{-1-2\alpha}, \ \ w_k = \frac{n\lambda_k}{1 + n\lambda_k}", font_size=30),
            cmath(r"E_{\theta_0}\Pi(\|\theta - \theta_0\|^2 \mid Y)", r"=", r"\textstyle\sum(1 - w_k)^2\theta_{0k}^2 + \sum w_k^2/n + \sum\frac{\lambda_k}{1 + n\lambda_k}", font_size=30),
            cmath(r"N = n^{1/(1 + 2\alpha)}", r":", r"\text{variance} + \text{spread} \asymp \frac Nn = n^{-\frac{2\alpha}{1 + 2\alpha}}, \ \ \text{bias}^2 \lesssim B\,N^{-2\min(\alpha,\beta)}", font_size=30),
            cmath(r"\text{Markov}", r":", r"\Pi(\|\theta - \theta_0\| > M_n\varepsilon_n \mid Y) \le \frac{E\Pi(\|\theta - \theta_0\|^2 \mid Y)}{M_n^2\varepsilon_n^2} \lesssim M_n^{-2} \to 0", font_size=30),
        ]
        rows[1][-1].set_color(BAYC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"conjugate, \ coordinate by coordinate"), why(r"bias$^2$ $+$ variance $+$ posterior spread"), why(r"where $n\lambda_k \approx 1$"), why(r"in expectation, \ then in probability")]
        self.steps_voiceover("<bookmark mark='a'/> The model is conjugate, coordinate by coordinate: the posterior for theta k is normal, "
                   "centred at w k times Y k, with w k equal to n lambda k over one plus n lambda k. <bookmark mark='b'/> So the "
                   "posterior's expected squared distance from the truth splits into three sums: the squared bias of the "
                   "posterior mean, its variance, and the posterior's own spread. <bookmark mark='c'/> Split the coordinates "
                   "where n lambda k is about one, at N equal to n to the one over one plus two alpha. The variance and the "
                   "spread are each of order N over n, n to the minus two alpha over one plus two alpha; the bias is at most "
                   "the Sobolev radius times N to the minus two times the smaller of alpha and beta. Both are the square of "
                   "the claimed rate. <bookmark mark='d'/> Markov's inequality, applied to the posterior, finishes it: the "
                   "posterior mass outside a ball of radius M n epsilon n is at most a constant over M n squared.", rows, whys)
        self.clear_but(card)
        self.p12_chart(d, card)
        self.p12_ggv(card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. Conjugacy, <bookmark mark='b'/> a decomposition into bias, "
                       "variance and spread, <bookmark mark='c'/> the bias–variance split at the critical index, as in Part "
                       "fifty's Pinsker theory, <bookmark mark='d'/> and Markov's inequality. With that, the exam's twelve "
                       "proofs are done.", [(r"conjugate posteriors", 53), (r"bias, \ variance, \ spread", 50), (r"split at $N$", 50),
                        (r"Markov: \ contraction", 43)], "abcd", color=BAYC)

    def p12_ggv(self, card):
        rows = [
            cmath(r"\text{prior mass}", r":", r"\Pi\big(\mathrm{KL}\text{-ball of radius } \varepsilon_n^2\big) \ge e^{-Cn\varepsilon_n^2}", font_size=32),
            cmath(r"\text{a sieve}", r":", r"\Pi(\Theta_n^c) \le e^{-(C + 4)n\varepsilon_n^2}, \ \ \log N(\varepsilon_n, \Theta_n) \le n\varepsilon_n^2", font_size=32),
            cmath(r"\text{tests}", r":", r"\text{errors } e^{-cn\varepsilon_n^2} \text{ against } \|\theta - \theta_0\| > M\varepsilon_n", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\Pi(\|\theta - \theta_0\| > M\varepsilon_n \mid Y) \to 0: \ \text{the general theorem, \ no conjugacy}", font_size=32),
        ]
        rows[0][-1].set_color(BAYC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"small balls (Part 53)"), why(r"most of the prior's mass is simple"), why(r"Le Cam--Birg\'e tests (Part 50)"), why(r"Ghosal, \ Ghosh \& van der Vaart (2000)")]
        self.steps_voiceover(
            "<bookmark mark='a'/> Without conjugacy, the general theorem of Ghosal, Ghosh and van der Vaart gives the "
            "same answer from three conditions. The prior must put mass at least e to the minus C n epsilon squared on "
            "a small Kullback–Leibler ball around the truth. <bookmark mark='b'/> Outside a sieve whose metric entropy "
            "is at most n epsilon squared, it must put exponentially less mass. <bookmark mark='c'/> The entropy bound "
            "yields tests that separate the truth from everything farther than M epsilon away, with exponentially "
            "small errors, as in Le Cam and Birgé's construction from Part fifty. <bookmark mark='d'/> Together, they "
            "force the posterior to contract at rate epsilon n. For the Gaussian prior, the small-ball probability "
            "gives exactly the rate computed here by hand.",
            rows, whys)
        self.clear_but(card)

    def p12_chart(self, d, card):
        ln = np.log10(np.asarray(d["ns"], float))
        A = axes([1, 6], [-4.2, 0.2], x_length=6.8, y_length=3.4, xlabel=r"$n$ \ (log scale), \ $\beta = 1$", ylabel=r"$\log_{10} E\Pi(\|\theta - \theta_0\|^2 \mid Y)$",
                 xticks=[1, 2, 3, 4, 5, 6], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-4, -3, -2, -1, 0], center=CHART)
        ax = A.ax
        cols = {"0.5": S.EST, "1.0": PROOFC, "2.0": S.RESID}
        cs = {a: polyline(ax, ln, np.log10(d[a]["total"]), c, 4) for a, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"exact, \ truth $\theta_{0k} = k^{-3/2}$ \ (smoothness just below 1)", font_size=22),
            label(rf"blue: \ $\alpha = 1/2$: \ slope {d['0.5']['slope']:.3f} \ (theory {d['0.5']['theory']:.3f})", font_size=22, color=S.EST),
            label(rf"green: \ $\alpha = 1 = \beta$: \ {d['1.0']['slope']:.3f} \ ({d['1.0']['theory']:.3f}), \ the minimax rate", font_size=22, color=PROOFC),
            label(rf"red: \ $\alpha = 2$: \ {d['2.0']['slope']:.3f} \ ({d['2.0']['theory']:.3f}): \ too smooth a prior", font_size=22, color=S.RESID),
            label(r"the prior's smoothness must match the truth's", font_size=22, color=GREY_A),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The posterior's expected squared distance from the truth, computed exactly, for a truth of "
            f"smoothness one and three priors. <bookmark mark='b'/> A rough prior, alpha one half: the fitted slope is "
            f"{say(d['0.5']['slope'], 3)}, against the theory's minus one half. <bookmark mark='c'/> A matched prior, alpha "
            f"one: {say(d['1.0']['slope'], 3)}, against minus two thirds, the minimax rate of Part fifty. <bookmark mark='d'/> "
            f"A prior smoother than the truth, alpha two: {say(d['2.0']['slope'], 3)}, against minus two fifths: the posterior "
            f"is too sure the function is smooth, and contracts too slowly to the right answer. <bookmark mark='e'/> The "
            f"prior's smoothness must match the truth's, or be learned from the data, as Part fifty-three's adaptation did."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["0.5"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["1.0"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["2.0"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)
