from __future__ import annotations

import numpy as np
from scipy import special, stats

from videos.stats.stats24.common import *  # noqa: F403


class Family(VoiceoverScene):
    def construct(self):
        self.card()
        self.edf()
        self.moments()
        self.table()
        self.gamma_ex()
        self.tweedie()
        self.links()
        self.canonical()

    def card(self):
        card = chapter_card(2, r"The exponential dispersion family", r"One form for many distributions", lit=(1972,), part=PART)
        with self.voiceover("Chapter two. The exponential dispersion family."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def edf(self):
        rows = [
            cmath(r"f(y;\theta,\phi)", r"=", r"\exp\Big\{\dfrac{y\theta - b(\theta)}{\phi/w} + c(y,\phi,w)\Big\}", font_size=30),
            cmath(r"\text{Poisson}", r":", r"y\log\mu - \mu - \log y!: \ \ \theta = \log\mu, \ b = e^\theta, \ \phi = 1", font_size=28),
            cmath(r"\text{binomial } (k/n)", r":", r"\theta = \log\tfrac{p}{1-p}, \ b = \log(1 + e^\theta), \ w = n", font_size=28),
            cmath(r"\text{normal}", r":", r"\theta = \mu, \ b = \theta^2/2, \ \phi = \sigma^2", font_size=30),
        ]
        rows[0][2].set_color(MODEL)
        whys = [why(r"$\theta$ canonical, \ $\phi$ dispersion, \ $w$ a prior weight"), why(r"read off the log density"),
                why(r"the proportion, \ weighted by its trials"), why(r"the dispersion is the variance")]
        intro = label('Prior weights determine observation-level dispersion', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Every distribution in the family has a density of one form: the exponential of y times a "
            "canonical parameter theta, minus a function b of theta, all over a dispersion phi divided by a weight, plus a "
            "term that doesn't involve theta. <bookmark mark='b'/> Write the Poisson's log probability as y log mu minus mu "
            "minus log y factorial, and read off: theta is log mu, b is e to the theta, and the dispersion is one. "
            "<bookmark mark='c'/> For a binomial proportion, theta is the log odds and the weight is the number of trials. "
            "<bookmark mark='d'/> For the normal, theta is the mean itself and the dispersion is the variance."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def moments(self):
        rows = [
            cmath(r"\ell(\theta)", r"=", r"\{y\theta - b(\theta)\}/\phi", font_size=30),
            cmath(r"E\,\ell' = 0", r"\Rightarrow", r"\mu = E\,y = b'(\theta)", font_size=30),
            cmath(r"\mathrm{Var}\,\ell' = -E\,\ell''", r"\Rightarrow", r"\mathrm{Var}\,y = \phi\, b''(\theta) = \phi\, V(\mu)", font_size=30),
            cmath(r"V(\mu)", r":", r"\text{the variance function: \ it identifies the family}", font_size=28),
        ]
        rows[2][-1].set_color(PATH)
        whys = [why(r"one observation's log likelihood"), why(r"Part 22's first score identity"),
                why(r"Part 22's second identity"), why(r"Poisson: \ $V = \mu$; \ binomial: \ $\mu(1-\mu)$")]
        intro = label('Score identities give the mean and variance for unit prior weight', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Why this form? Take one observation with unit prior weight, and omit terms constant"
            " in theta. <bookmark mark='b'/> Part 22's first identity, that the score has mean zero, says the mean of"
            " y is b prime of theta. <bookmark mark='c'/> The second identity, that the score's variance is minus the"
            " expected curvature, says the variance of y is phi times b double prime. Written as a function of the "
            "mean, that's phi times V of mu. <bookmark mark='d'/> The variance function V is the family's "
            "fingerprint: mu for the Poisson, mu times one minus mu for the binomial, one for the normal, mu squared "
            "for the gamma. Chapter seven will keep only the variance function and drop the rest."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        hdr = [r"\textbf{family}", r"\textbf{outcome}", r"$V(\mu)$", r"\textbf{canonical link}", r"$\phi$"]
        body = [[r"normal", r"any real", r"$1$", r"identity", r"$\sigma^2$"],
                [r"binomial", r"proportion", r"$\mu(1 - \mu)$", r"logit", r"1"],
                [r"Poisson", r"count", r"$\mu$", r"log", r"1"],
                [r"gamma", r"positive", r"$\mu^2$", r"$-1/\mu$", r"$1/\text{shape}$"],
                [r"inverse Gaussian", r"positive", r"$\mu^3$", r"$-1/(2\mu^2)$", r"$\lambda^{-1}$"]]
        t = table_rows([hdr] + body, font_size=26, col_buff=0.65, row_buff=0.3, colors=[GREY_A, None, RES, None, PATH, TEAL])
        t.move_to([0, 0.5, 0])
        foot = label(r"the gamma: \ constant coefficient of variation; \ waiting times, \ costs, \ rainfall", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "<bookmark mark='a'/> The common members. The normal, for any real outcome, with constant variance. "
            "<bookmark mark='b'/> The binomial, for proportions, <bookmark mark='c'/> the Poisson, for counts. "
            "<bookmark mark='d'/> The gamma, for positive amounts whose standard deviation grows in proportion to the"
            " mean: waiting times, insurance claims, rainfall. <bookmark mark='e'/> And the inverse Gaussian, for "
            "positive amounts whose variance is proportional to the cube of the mean. Relative skewness also depends "
            "on dispersion. Each has a canonical link, one that makes the linear predictor equal theta, up to a fixed"
            " rescaling or sign convention in commonly named inverse links."
        ) as vo:
            self.play(FadeIn(t[0]))
            vo.wait_until("a")
            self.play(FadeIn(t[1]))
            vo.wait_until("b")
            self.play(FadeIn(t[2]))
            vo.wait_until("c")
            self.play(FadeIn(t[3]))
            vo.wait_until("d")
            self.play(FadeIn(t[4]), FadeIn(foot))
            vo.wait_until("e")
            self.play(FadeIn(t[5]))
        self.clear_scene()

    def gamma_ex(self):
        rows = [
            cmath(r"\text{gamma, log link}", r":", r"\log E(\text{income}\mid a) = \beta_0 + \beta_1(a-45)/10", font_size=30),
            cmath(r"\hat\beta_1", r"=", rf"{load('extras')['gamma']['coef'][1]:.3f} \ \text{{per decade: \ mean }} \times {np.exp(load('extras')['gamma']['coef'][1]):.3f}", font_size=30),
            cmath(r"\text{log-normal}", r":", rf"E(\log \text{{income}}): \ {load('extras')['lognormal']['coef'][1]:.3f} \ \text{{per decade}}", font_size=30),
            cmath(r"\text{the difference}", r":", r"\text{the mean of the logs vs the log of the mean}", font_size=30),
        ]
        rows[1][-1].set_color(PATH)
        whys = [why(rf"{load('extras')['n_inc']:,} of the World's working adults"), why(rf"$\hat\phi = {load('extras')['gamma']['phi']:.2f}$: \ CV {load('extras')['gamma']['cv']:.2f}"), why(r"least squares on log income"), why(r"Jensen: \ different targets")]
        intro = label('The log of a mean and the mean of a log are different targets', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> An example of the gamma. Model the mean income of fifteen hundred of the World's "
            "working adults with a log link and gamma errors. <bookmark mark='b'/> Each decade of age multiplies the "
            "mean by one point one one seven, with a dispersion of point eight six, a coefficient of variation of "
            "about point nine three. <bookmark mark='c'/> The usual alternative, least squares on log income, gives "
            "point one oh oh per decade. <bookmark mark='d'/> They answer different questions: the gamma model "
            "describes the log of the mean income, the log-normal regression the mean of the log, which determines "
            "the median only under an appropriate symmetric log-error model. By Jensen's inequality from Part 21 they"
            " are distinct targets. A changing conditional distribution can also change their age slopes; Jensen "
            "alone does not quantify that difference."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tweedie(self):
        rows = [
            cmath(r"\text{Tweedie}", r":", r"V(\mu) = \mu^{q}", font_size=30),
            cmath(r"q = 0, 1, 2, 3", r":", r"\text{normal, \ Poisson, \ gamma, \ inverse Gaussian}", font_size=30),
            cmath(r"1 < q < 2", r":", r"\text{a Poisson number of gamma amounts}", font_size=30),
            cmath(r"\text{insurance}", r":", r"\text{a point mass at } 0 \text{ plus a skewed positive part}", font_size=30),
        ]
        rows[2][-1].set_color(PATH)
        whys = [why(r"Tweedie (1984): \ power variance functions"), why(r"the table, \ as one family"),
                why(r"the compound Poisson--gamma"), why(r"most policies claim nothing; \ a few claim a lot")]
        intro = label('Power variance functions connect several outcome families', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Maurice Tweedie noticed in 1984 that the table's variance functions are powers of the mean. "
            "<bookmark mark='b'/> Power zero is the normal, one the Poisson, two the gamma, three the inverse Gaussian. "
            "<bookmark mark='c'/> Powers between one and two give something new: a Poisson number of gamma-sized amounts. "
            "<bookmark mark='d'/> That has an exact zero when the Poisson count is zero, plus a skewed continuous part, "
            "which is precisely what a year of insurance claims looks like: most policies claim nothing, and a few claim a "
            "lot. Actuaries fit it as a GLM."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def links(self):
        A = axes([-4, 4], [0, 1], x_length=8.0, y_length=4.4, xlabel=r"linear predictor $\eta$", ylabel=r"$\mu = g^{-1}(\eta)$",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1], center=[-1.6, 0.3, 0])
        ax = A.ax
        e = np.linspace(-4, 4, 200)
        cl = curve(ax, e, special.expit(e), LOGIT, 3.5)
        cp = curve(ax, e, stats.norm.cdf(e), PROBIT, 3.5)
        cc = curve(ax, e, -np.expm1(-np.exp(e)), CLOGLOG, 3.5)
        rows = fit_rows(VGroup(
            label(r"three inverse links for a probability", font_size=22),
            label(r"blue: \ logit, \ effects on log odds", font_size=22, color=LOGIT),
            label(r"teal: \ probit, \ a normal tolerance", font_size=22, color=PROBIT),
            label(r"gold: \ cloglog, \ asymmetric", font_size=22, color=CLOGLOG),
            label(r"$\operatorname{expit}(\eta)\approx\Phi(\eta/1.7)$", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For a probability, an inverse link maps the real linear predictor into zero to one;"
            " the link itself goes the other way. <bookmark mark='b'/> The logit makes effects additive on the "
            "log-odds scale, the canonical choice. <bookmark mark='c'/> The probit corresponds to a normal tolerance,"
            " as Bliss argued. <bookmark mark='d'/> The complementary log-log is asymmetric: it approaches one much "
            "faster than it leaves zero, which is what you get if death comes from the first of many independent "
            "hits, and why it suits Bliss's beetles. <bookmark mark='e'/> The probit is steeper, but stretch it by "
            "about one point seven and it is almost indistinguishable from the logit; only data in the tails, or lots"
            " of data, can tell them apart."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, (m_, c) in enumerate(zip("bcd", (cl, cp, cc))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def canonical(self):
        rows = [
            cmath(r"\text{canonical link}", r":", r"g(\mu) = \theta \ \Rightarrow \ \eta = \theta", font_size=30),
            cmath(r"\text{score}", r"=", r"\textstyle\sum_i w_i x_i (y_i-\mu_i)/\phi", font_size=30),
            cmath(r"\text{sufficient for }\beta", r":", r"X^\top\mathrm{diag}(w_i)y\ \ (\phi\ \text{known})", font_size=30),
            cmath(r"\text{observed} = \text{expected}", r":", r"\text{Newton} = \text{Fisher scoring}", font_size=30),
        ]
        rows[1][2].set_color(MODEL)
        whys = [why(r"the link that makes the linear predictor $\theta$"), why(r"residuals times covariates: \ zero at the fit"),
                why(r"a sufficient statistic of fixed size"), why(r"Part 22, \ chapter four")]
        intro = label('Canonical links simplify weighted score equations', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The canonical link is special. With it, the linear predictor is the canonical "
            "parameter itself, <bookmark mark='b'/> and the score equations become the sum of covariates times "
            "residuals equals zero, the same form as least squares' normal equations. <bookmark mark='c'/> With known"
            " dispersion and fixed prior weights, the weighted predictor-response sum is sufficient for beta. For "
            "binomial proportions, trials must enter those weights. <bookmark mark='d'/> And the observed and "
            "expected information coincide, so Newton's method and Fisher scoring are the same, as Part 22 noted. "
            "Other links lose these conveniences, but often fit better, as the beetles showed."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
