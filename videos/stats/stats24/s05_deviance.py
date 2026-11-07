from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats24.common import *  # noqa: F403


class Deviance(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.beetles()
        self.analysis()
        self.order()
        self.residuals()
        self.binned()
        self.qq()

    def card(self):
        card = chapter_card(4, r"Deviance", r"How far from the saturated model?", part=PART)
        with self.voiceover("Chapter four. Deviance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def define(self):
        rows = [
            cmath(r"\text{saturated}", r":", r"\hat\mu_i = y_i: \ \text{one parameter per observation}", font_size=30),
            cmath(r"D", r"=", r"2\phi\{\ell(\text{saturated}) - \ell(\hat\beta)\} = \textstyle\sum_i d_i", font_size=30),
            cmath(r"\text{normal}", r":", r"D = \textstyle\sum (y_i - \hat\mu_i)^2, \ \text{the residual sum of squares}", font_size=28),
            cmath(r"\text{Poisson}", r":", r"D = 2\textstyle\sum \{y_i \log(y_i/\hat\mu_i) - (y_i - \hat\mu_i)\}", font_size=30),
        ]
        rows[1][2].set_color(MODEL)
        whys = [why(r"the best any model could do"), why(r"twice the log-likelihood gap"),
                why(r"the deviance generalizes RSS"), why(r"$d_i$: \ the unit deviances")]
        intro = label('Deviance measures a scaled gap from a saturated fit', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The saturated model gives every observation its own parameter, so it fits each "
            "observed mean, sometimes as a boundary limit rather than at a finite natural parameter. <bookmark "
            "mark='b'/> The deviance is twice the gap in log likelihood between the saturated model and ours, scaled "
            "by the dispersion: a sum of one piece per observation, the unit deviances. <bookmark mark='c'/> For "
            "normal errors it is exactly the residual sum of squares, so the deviance is least squares' yardstick "
            "generalized. <bookmark mark='d'/> For the Poisson it's twice the sum of y log y over mu hat, minus the "
            "residuals."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def beetles(self):
        d = load("bliss")
        f = d["fits"]
        hdr = [r"\textbf{link}", r"\textbf{deviance}", r"\textbf{df}", r"$P(\chi^2_6 > D)$", r"\textbf{AIC}"]
        body = [[l, f"{f[l]['deviance']:.2f}", f"{f[l]['df']}", f"{f[l]['p']:.3f}", f"{f[l]['aic']:.1f}"] for l in ("logit", "probit", "cloglog")]
        t = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.32, colors=[GREY_A, LOGIT, PROBIT, CLOGLOG])
        t.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"grouped data, \ about 60 beetles a dose: \ $D \approx \chi^2_{n-p}$ if the model is right", font_size=24),
            label(r"logit $p=0.08$ is not rejected at 5\%; \ cloglog has lower AIC", font_size=24, color=HIT),
        ), 12.0, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bliss's beetles, with the three links. <bookmark mark='b'/> With grouped data and "
            "around sixty beetles per dose, the deviance of a correct model is approximately chi-squared with eight "
            "minus two, six, degrees of freedom. <bookmark mark='c'/> The logit's eleven point two has a tail "
            "probability of point oh eight; the probit's, point one two; the complementary log-log's three point four"
            " five, point seven five. The Akaike criteria agree: the asymmetric link has the lowest AIC by about "
            "eight units against the logit, among these three fits. Part 28 explains what such a difference means."
        ) as vo:
            self.add(bliss_tag())
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def analysis(self):
        d = load("devtable")
        hdr = [r"\textbf{model adds}", r"\textbf{deviance}", r"\textbf{df}", r"\textbf{drop}", r"$F$"]
        body = []
        for i, r in enumerate(d["rows"]):
            body.append([r["terms"] if i == 0 else rf"+ {r['terms']}", f"{r['dev']:.0f}", f"{r['df']}",
                         "" if i == 0 else f"{r['drop']:.0f}", "" if i == 0 else f"{r['F']:.0f}"])
        t = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.28, colors=[GREY_A] + [None] * 5)
        t.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"2,000 of the World's adults: \ doctor visits last year, \ Poisson", font_size=22),
            label(rf"residual deviance {d['rows'][-1]['dev']:.0f} on {d['rows'][-1]['df']} df: \ far too big", font_size=22, color=RES),
            label(rf"so each drop is judged against $\hat\phi = {d['rows'][-1]['phi']:.2f}$: \ an $F$, \ chapter seven", font_size=22, color=HIT),
        ), 12.0, 0.25, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The deviance also compares nested models, like Part 23's residual sums of squares. "
            "Two thousand of the World's adults, and the number of times each saw a doctor last year. Add terms one "
            "at a time to a Poisson regression. <bookmark mark='b'/> Age cuts the deviance by seven hundred and "
            "fifty-four, body mass by three hundred, a diagnosis of high blood pressure by two hundred and "
            "fifty-seven, sex by sixty-eight. <bookmark mark='c'/> But the final deviance is nearly six thousand on "
            "two thousand degrees of freedom, three times what a Poisson model allows. <bookmark mark='d'/> An "
            "approximate quasi-Poisson calculation divides each drop by the estimated dispersion, three point three "
            "six. This is a working variance assumption, not an exact F test; chapter seven checks it against a "
            "robust sandwich."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in t[2:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def order(self):
        rows = [
            cmath(r"\text{sequential}", r":", r"\text{each drop given the terms above it}", font_size=30),
            cmath(r"\text{order matters}", r":", r"\text{correlated predictors share their deviance}", font_size=30),
            cmath(r"\text{drop-one}", r":", r"\text{each term given all the others}", font_size=30),
            cmath(r"\text{both}", r":", r"\text{nested LR tests, \ asking different questions}", font_size=30),
        ]
        rows[1][-1].set_color(RES)
        whys = [why(r"type I, \ in SAS's terms"), why(r"age and BMI, \ told and age"), why(r"type II / III"),
                why(r"say which you report")]
        intro = label('Sequential and drop-one comparisons ask different questions', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> That table was sequential: each drop is the contribution of a term given the ones "
            "above it. <bookmark mark='b'/> Order matters when predictors are correlated; age and a high blood "
            "pressure diagnosis overlap, so whichever enters first collects the shared part. <bookmark mark='c'/> "
            "Dropping each term from the full model instead asks what it adds given everything else. <bookmark "
            "mark='d'/> Under a correctly specified likelihood, both are nested-model comparisons with the "
            "appropriate likelihood-ratio reference; they answer different questions, so say which one you report."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def residuals(self):
        rows = [
            cmath(r"\text{Pearson}", r":", r"r_i^P = \sqrt{n_i}\,(y_i-\hat\mu_i)/\sqrt{V(\hat\mu_i)}", font_size=30),
            cmath(r"\text{deviance}", r":", r"r_i^D = \mathrm{sign}(y_i - \hat\mu_i)\sqrt{d_i}", font_size=30),
            cmath(r"\text{randomized quantile}", r":", r"r_i^Q = \Phi^{-1}(u_i), \ u_i \sim U(F(y_i^-), F(y_i))", font_size=28),
            cmath(r"\text{true CDF known}", r":", r"r^Q\sim N(0,1);\ \text{fitted CDF: diagnostic approximation}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"$\sum (r^P)^2$: \ Pearson's $X^2$"), why(r"$\sum (r^D)^2 = D$"),
                why(r"Dunn \& Smyth (1996)"), why(r"even for counts and zeros")]
        intro = label('Fitted residual transforms are diagnostic approximations', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Residuals come in several kinds. The unscaled Pearson residual divides the observed"
            " discrepancy by the square root of the variance function and includes prior trial weights. Dispersion is"
            " handled separately; their squares add up to Pearson's chi-squared. <bookmark mark='b'/> Deviance "
            "residuals take the square root of each unit deviance, with a sign; their squares add up to the deviance."
            " For counts and binary outcomes, neither looks normal, even when the model is right. <bookmark "
            "mark='c'/> Peter Dunn and Gordon Smyth's randomized quantile residuals fix that: find where the "
            "observation sits in its fitted distribution, spread that point uniformly across the jump of a discrete "
            "distribution, and map it through the inverse normal. <bookmark mark='d'/> With the true CDF known, "
            "independent randomized probability transforms are exactly normal. Plugging in fitted parameters changes "
            "their dependence and finite-sample distribution: the QQ plot is a diagnostic, not an exact normality "
            "test."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def binned(self):
        rows = [
            cmath(r"\text{binary } y", r":", r"\text{residuals take two values at each } \hat p", font_size=30),
            cmath(r"\text{binned residuals}", r":", r"\text{average } y - \hat p \text{ within bins of } \hat p", font_size=30),
            cmath(r"\text{Hosmer--Lemeshow}", r":", r"\text{a } \chi^2 \text{ over deciles of risk}", font_size=30),
            cmath(r"\text{calibration plot}", r":", r"\text{observed rate against predicted, \ chapter twelve}", font_size=30),
        ]
        rows[1][-1].set_color(PATH)
        whys = [why(r"two bands of dots: \ uninformative"), why(r"Gelman \& Hill (2007)"), why(r"Hosmer \& Lemeshow (1980)"), why(r"the picture behind both")]
        intro = label('Binning can make probability residual patterns easier to read', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For binary outcomes even quantile residuals are noisy, and raw residuals form two "
            "bands that can be hard to read. <bookmark mark='b'/> The practical fix is to bin: sort observations by "
            "fitted probability, and average the residuals within each bin. <bookmark mark='c'/> David Hosmer and "
            "Stanley Lemeshow turned the same idea into a chi-squared test over deciles of predicted risk. <bookmark "
            "mark='d'/> And the picture behind both, observed rate against predicted, is the calibration plot of "
            "chapter twelve."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def qq(self):
        d = load("visits")
        qp, qn = np.asarray(d["q_pois"]), np.asarray(d["q_nb"])
        n = len(qp)
        th = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
        keep = np.arange(0, n, 8)
        A = axes([-3.5, 3.5], [-5, 6], x_length=6.6, y_length=4.6, xlabel=r"normal quantile", ylabel=r"quantile residual",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-4, -2, 0, 2, 4, 6], center=[-2.4, 0.3, 0])
        ax = A.ax
        line = DashedLine(ax.c2p(-3.5, -3.5), ax.c2p(3.5, 3.5), color=GREY_B, stroke_width=2)
        dp = VGroup(*[Dot(ax.c2p(th[i], qp[i]), radius=0.035, color=POIS) for i in keep if -3.5 <= th[i] <= 3.5 and -5 <= qp[i] <= 6])
        dn = VGroup(*[Dot(ax.c2p(th[i], qn[i]), radius=0.035, color=NBC) for i in keep if -3.5 <= th[i] <= 3.5 and -5 <= qn[i] <= 6])
        rows = fit_rows(VGroup(
            label(r"the visits; 250 of 2,000 residuals sampled for display", font_size=22),
            label(r"red: \ Poisson: \ an S, \ tails far too long", font_size=22, color=POIS),
            label(rf"green: \ negative binomial, \ $\hat k = {d['nb']['k']:.2f}$", font_size=22, color=NBC),
            label(r"closer to the line: \ a better approximation", font_size=22, color=HIT),
        ), 4.4, 0.42, [4.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here they are for the doctor visits. <bookmark mark='b'/> Under the Poisson model "
            "the quantile residuals bend into an S with tails far too long: the counts are much more spread out than "
            "the Poisson allows. <bookmark mark='c'/> Under a negative binomial model, chapter eight's, <bookmark "
            "mark='d'/> they lie much closer to the line. This supports a better distributional approximation; it "
            "does not prove that the negative binomial is the generating mechanism."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in dp], lag_ratio=0.003), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in dn], lag_ratio=0.003), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
