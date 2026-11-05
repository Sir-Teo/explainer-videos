from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats24.common import *  # noqa: F403


class Asymptotics(VoiceoverScene):
    def construct(self):
        self.card()
        self.trinity()
        self.dispersion()
        self.ld50_ci()
        self.grouped()
        self.binary()
        self.od_test()
        self.advice()

    def card(self):
        card = chapter_card(5, r"Asymptotics for GLMs", r"Which approximations hold, \ and when", part=PART)
        with self.voiceover("Chapter five. Asymptotics for generalized linear models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def trinity(self):
        d = load("bliss")
        f = d["fits"]["cloglog"]
        rows = [
            cmath(r"\hat\beta", r"\approx", r"N\big(\beta, \ \phi (X^\top W X)^{-1}\big)", font_size=30),
            cmath(r"\text{Wald}", r":", rf"\hat\beta_1 = {f['coef'][1]:.1f} \pm 1.96 \times {f['se'][1]:.2f}", font_size=30),
            cmath(r"\text{LR}", r":", r"D_0 - D_1 \sim \chi^2_q", font_size=30),
            cmath(r"\text{score}", r":", r"\text{needs only the smaller model}", font_size=30),
        ]
        rows[0][2].set_color(MODEL)
        whys = [why(r"Part 22, \ chapter three"), why(r"the beetles' cloglog slope"), why(r"a drop in deviance: \ Wilks"),
                why(r"Rao: \ add a term without fitting it")]
        with self.voiceover(
            "<bookmark mark='a'/> Everything in Part 22 applies. The estimates are approximately normal, with covariance phi "
            "times X transpose W X inverse, the last IRLS step's weights. <bookmark mark='b'/> For the beetles' complementary "
            "log-log slope that's twenty-two plus or minus about three and a half. <bookmark mark='c'/> The likelihood-ratio "
            "test is a drop in deviance, chi-squared with as many degrees of freedom as terms removed. "
            "<bookmark mark='d'/> And the score test needs only the smaller model, which makes it the cheap way to screen "
            "many candidate terms."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dispersion(self):
        rows = [
            cmath(r"\hat\phi", r"=", r"\textstyle\sum (r_i^P)^2/(n - p)", font_size=30),
            cmath(r"F", r"=", r"\dfrac{(D_0 - D_1)/q}{\hat\phi}", font_size=30),
            cmath(r"\text{gamma, \ normal}", r":", r"\phi \ \text{always estimated}", font_size=30),
            cmath(r"\text{binomial, \ Poisson}", r":", r"\phi = 1 \text{ assumed: \ check it}", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"Pearson's moment estimate"), why(r"compare with $F_{q,\, n-p}$"),
                why(r"like $s^2$ in least squares"), why(r"$\hat\phi \gg 1$: \ overdispersion")]
        with self.voiceover(
            "<bookmark mark='a'/> When the dispersion is unknown, estimate it from the Pearson residuals, like s squared in "
            "least squares. <bookmark mark='b'/> Then a drop in deviance per term, divided by that estimate, is compared "
            "with an F distribution, as in the analysis of deviance we just did. <bookmark mark='c'/> For the gamma and the "
            "normal, the dispersion is always estimated. <bookmark mark='d'/> For the binomial and the Poisson it's assumed "
            "to be one, and the assumption is worth checking: an estimate well above one means overdispersion."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ld50_ci(self):
        d = load("bliss")
        L50 = d["fits"]["cloglog"]["ld50"]
        rows = [
            cmath(r"\text{LD50}", r"=", r"(g(\tfrac12) - \hat\alpha)/\hat\beta", font_size=30),
            cmath(r"\text{delta method}", r":", rf"{L50['x']:.4f} \pm 1.96 \times {L50['se']:.4f}", font_size=30),
            cmath(r"\text{Fieller}", r":", rf"[{L50['fieller'][0]:.4f}, \ {L50['fieller'][1]:.4f}]", font_size=30),
            cmath(r"\text{when they differ}", r":", r"\hat\beta \text{ near zero: \ Fieller can be unbounded}", font_size=30),
        ]
        rows[2][-1].set_color(PATH)
        whys = [why(r"a ratio of coefficients"), why(r"symmetric by construction"), why(r"Part 11: \ invert a test of the ratio"),
                why(r"an honest ``we cannot say''")]
        with self.voiceover(
            "<bookmark mark='a'/> Functions of the coefficients need the same care as in Part 11. The LD fifty is a ratio. "
            "<bookmark mark='b'/> The delta method gives a symmetric interval, the estimate plus or minus about point oh oh "
            "eight. <bookmark mark='c'/> Fieller's method inverts a test of the ratio directly; for the beetles the two "
            "agree to the third decimal, because the slope is estimated very precisely. <bookmark mark='d'/> When the slope "
            "is close to zero they part company: Fieller's set can be a whole line, which is the honest answer when the data "
            "can't locate the dose at all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def grouped(self):
        d = load("binary_dev")
        D = np.asarray(d["grouped"])
        edges = np.linspace(0, 25, 51)
        h, _ = np.histogram(np.clip(D, 0, 25 - 1e-9), edges, density=True)
        A = axes([0, 25], [0, 0.16], x_length=8.0, y_length=4.2, xlabel=r"deviance of a correct model",
                 ylabel=r"density", xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 0.05, 0.1, 0.15], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=MODEL, opacity=0.6)
        gr = np.linspace(0.05, 25, 200)
        c = curve(ax, gr, stats.chi2.pdf(gr, 6), TRUE, 3)
        rows = fit_rows(VGroup(
            label(r"2,000 fake Bliss experiments", font_size=22),
            label(r"same doses and beetles, \ a true logit", font_size=22, color=GREY_A),
            label(r"gold: \ $\chi^2_6$", font_size=22, color=TRUE),
            label(rf"rejects at 5\%: \ {100 * d['grouped_reject']:.1f}\%", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But the deviance as a test of fit needs care. Simulate two thousand Bliss experiments, same "
            "doses and numbers of beetles, from a logistic model that is exactly right. <bookmark mark='b'/> Refit each. "
            "<bookmark mark='c'/> The deviances follow chi-squared with six degrees of freedom, <bookmark mark='d'/> and the "
            "test rejects six percent of the time. With about sixty beetles per dose, the approximation works."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def binary(self):
        d = load("binary_dev")
        D = np.asarray(d["binary"])
        lo, hi = 150, 300
        edges = np.linspace(lo, hi, 51)
        h, _ = np.histogram(np.clip(D, lo, hi - 1e-9), edges, density=True)
        A = axes([lo, hi], [0, 0.04], x_length=8.0, y_length=4.2, xlabel=r"deviance of a correct model, \ binary $y$",
                 ylabel=r"density", xticks=[150, 200, 250, 300], yticks=[0, 0.02, 0.04], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=RES, opacity=0.6)
        gr = np.linspace(lo, hi, 200)
        c = curve(ax, gr, stats.chi2.pdf(gr, d["df_binary"]), TRUE, 3)
        rows = fit_rows(VGroup(
            label(r"200 people, \ one yes-or-no each", font_size=22),
            label(rf"gold: \ $\chi^2_{{{d['df_binary']}}}$, \ the textbook claim", font_size=22, color=TRUE),
            label(rf"actual: \ mean {d['binary_mean']:.0f}, \ SD {d['binary_sd']:.0f}", font_size=22, color=RES),
            label(rf"``rejects'' a correct model: \ {100 * d['binary_reject']:.0f}\%", font_size=22, color=RES),
            label(r"the saturated model grows with $n$", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now ungrouped data: two hundred people, one yes-or-no outcome each, again from a correct "
            "logistic model. <bookmark mark='b'/> The textbook would compare the deviance with chi-squared on a hundred and "
            "ninety-eight degrees of freedom. <bookmark mark='c'/> The actual distribution is centred at two hundred and "
            "thirty-five with a standard deviation of twelve, much narrower than the chi-squared's twenty, and in the wrong "
            "place. <bookmark mark='d'/> Used as a test of fit, it would reject this correct model sixty-three percent of "
            "the time. <bookmark mark='e'/> The reason: the saturated model's number of parameters grows with the sample, "
            "the Neyman–Scott situation of Part 22. For binary data the deviance compares nested models, never a model with "
            "the truth; Hosmer and Lemeshow's grouping, or calibration plots, check fit instead."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def od_test(self):
        rows = [
            cmath(r"H_0", r":", r"\mathrm{Var}\,y = \mu \ \text{vs} \ \mu + \alpha\mu^2", font_size=30),
            cmath(r"\text{score test}", r":", r"\text{regress } \{(y - \hat\mu)^2 - y\}/\hat\mu \text{ on } \hat\mu", font_size=30),
            cmath(r"\text{LR, \ Poisson vs NB}", r":", r"\alpha = 0 \text{ is on the boundary: \ } \tfrac12\chi^2_0 + \tfrac12\chi^2_1", font_size=28),
            cmath(r"\text{the visits}", r":", r"2 \times (4682 - 3721) = 1924", font_size=30),
        ]
        rows[2][-1].set_color(PATH)
        whys = [why(r"overdispersion as a hypothesis"), why(r"Cameron \& Trivedi (1990)"), why(r"Part 22, \ chapter nine"),
                why(r"overwhelming")]
        with self.voiceover(
            "<bookmark mark='a'/> Overdispersion can be tested. Under the Poisson the variance equals the mean; the "
            "alternative adds alpha times mu squared. <bookmark mark='b'/> Colin Cameron and Pravin Trivedi's score test "
            "needs only the Poisson fit: regress a scaled squared residual on the fitted mean and test the slope. "
            "<bookmark mark='c'/> The likelihood-ratio test of Poisson against negative binomial puts alpha equal to zero on "
            "the edge of its range, so, as in Part 22's chapter nine, its null distribution is half a point mass at zero "
            "and half a chi-squared with one degree of freedom. <bookmark mark='d'/> For the visits the statistic is "
            "nineteen hundred: overwhelming."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"differences of deviance between nested models: \ $\chi^2$, \ reliably", font_size=24, color=HIT),
            label(r"the deviance itself as a fit test: \ only for well-grouped data", font_size=24, color=PATH),
            label(r"intervals: \ profile likelihood beats Wald when $\hat p$ is extreme", font_size=24),
            label(r"small samples: \ exact conditional tests, \ or the parametric bootstrap", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: differences in deviance between nested models are reliably chi-squared, grouped or "
            "not. <bookmark mark='b'/> The deviance alone, as a test of fit, works only when the data are well grouped. "
            "<bookmark mark='c'/> For intervals, Part 22's profile likelihood beats the Wald interval when probabilities are "
            "near zero or one. <bookmark mark='d'/> And in small samples, exact conditional tests or a parametric bootstrap "
            "replace the approximations."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
