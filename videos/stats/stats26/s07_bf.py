from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class BayesFactors(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.scale()
        self.normal()
        self.bartlett()
        self.bic()
        self.bma()
        self.cautions()

    def card(self):
        card = chapter_card(6, r"Bayes factors", r"Evidence as a ratio of predictions", lit=(1939, 1995), part=PART)
        with self.voiceover("Chapter six. Bayes factors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\frac{P(H_1 \mid y)}{P(H_0 \mid y)}", r"=", r"\frac{p(y \mid H_1)}{p(y \mid H_0)} \times \frac{P(H_1)}{P(H_0)}", font_size=32),
            cmath(r"BF_{10}", r"=", r"\frac{p(y \mid H_1)}{p(y \mid H_0)}", font_size=32),
            cmath(r"p(y \mid H)", r"=", r"\textstyle\int p(y \mid \theta, H)\, p(\theta \mid H)\, d\theta", font_size=30),
            cmath(r"\text{read as}", r":", r"\text{which hypothesis predicted the data better}", font_size=30),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"posterior odds = Bayes factor $\times$ prior odds"), why(r"Jeffreys (1939), \ Part 15's first look"),
                why(r"the marginal likelihood, \ or evidence"), why(r"averaged over each hypothesis's prior")]
        with self.voiceover(
            "<bookmark mark='a'/> Bayes's rule for two hypotheses says the posterior odds are the prior odds times a factor "
            "the data supply. <bookmark mark='b'/> That factor, the Bayes factor, is the ratio of how probable the data were "
            "under each hypothesis, Harold Jeffreys's tool, met briefly in Part 15. <bookmark mark='c'/> Each probability is "
            "a marginal likelihood: the likelihood averaged over the hypothesis's own prior. <bookmark mark='d'/> So a Bayes "
            "factor compares predictions. A hypothesis that spreads its bets thinly over many possible results is penalized "
            "when the result is one it barely predicted."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scale(self):
        hdr = [r"\textbf{$BF_{10}$}", r"\textbf{$2\log BF_{10}$}", r"\textbf{Kass \& Raftery (1995)}"]
        body = [[r"1 to 3", r"0 to 2", r"not worth more than a bare mention"],
                [r"3 to 20", r"2 to 6", r"positive"],
                [r"20 to 150", r"6 to 10", r"strong"],
                [r"above 150", r"above 10", r"very strong"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A, GREY_B, HIT, HIT, HIT])
        tb.move_to([0, 0.6, 0])
        foot = label(r"a verbal scale on the log of a ratio: \ like a deviance, \ not a probability", font_size=22, color=GREY_A).move_to([0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robert Kass and Adrian Raftery's 1995 review gave the scale most people quote, a tidier "
            "version of Jeffreys's own. A factor below three is barely worth mentioning; three to twenty is positive "
            "evidence; twenty to a hundred and fifty, strong; beyond that, very strong. <bookmark mark='b'/> Twice the log "
            "Bayes factor sits on the same scale as a likelihood-ratio statistic, which makes comparisons with Part 22 easy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def normal(self):
        rows = [
            cmath(r"H_0", r":", r"\mu = 0; \ \ H_1: \ \mu \sim N(0, \tau^2)", font_size=30),
            cmath(r"\bar y", r"\sim", r"N(0, \sigma^2/n) \text{ under } H_0, \ \ N(0, \sigma^2/n + \tau^2) \text{ under } H_1", font_size=28),
            cmath(r"BF_{01}", r"=", r"\sqrt{1 + n\tau^2/\sigma^2}\; \exp\Bigl\{-\tfrac{z^2}{2}\,\tfrac{n\tau^2}{\sigma^2 + n\tau^2}\Bigr\}", font_size=28),
            cmath(r"z = 2.5, \ n = 50", r":", r"p = 0.012; \ \ BF_{01} = 0.33 \text{ for } \tau = \sigma", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"a point null against a normal alternative"), why(r"both are just normal predictions"),
                why(r"two normal densities, \ divided"), why(r"a `significant' result: \ odds of 3 to 1 for $H_1$")]
        with self.voiceover(
            "<bookmark mark='a'/> The workhorse case: is a normal mean zero, or drawn from a normal of spread tau? "
            "<bookmark mark='b'/> Under each hypothesis the sample mean is simply normal, with a larger variance under the "
            "alternative. <bookmark mark='c'/> So the Bayes factor is a ratio of two normal densities, in closed form. "
            "<bookmark mark='d'/> Take a z-statistic of two and a half from fifty observations: a p-value of point oh one "
            "two, conventionally significant. With tau equal to sigma, the Bayes factor for the null is point three three: "
            "the data favour the alternative by three to one. Positive evidence, on Kass and Raftery's scale, but far weaker "
            "than 'p below point oh five' sounds."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bartlett(self):
        d = load("bf")
        taus, bf = np.asarray(d["taus"]), np.asarray(d["bf01"])
        A = axes([-2, 3], [-2, 3], x_length=7.4, y_length=4.4, xlabel=r"prior SD $\tau$ under $H_1$ \ (log scale)",
                 ylabel=r"$BF_{01}$ \ (log scale)", xticks=[-2, -1, 0, 1, 2, 3], yticks=[-2, -1, 0, 1, 2, 3],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        c = curve(ax, np.log10(taus), np.log10(bf), SHRUNK, 3.5)
        one = DashedLine(ax.c2p(-2, 0), ax.c2p(3, 0), color=GREY_B, stroke_width=1.5)
        mn = Dot(ax.c2p(np.log10(d["tau_min"]), np.log10(d["bf_min"])), radius=0.08, color=HIT)
        rows = fit_rows(VGroup(
            label(r"the same data: \ $z = 2.5$, \ $n = 50$", font_size=22),
            label(rf"best case for $H_1$: \ $BF_{{01}} = {d['bf_min']:.2f}$ at $\tau = {d['tau_min']:.2f}$", font_size=22, color=HIT),
            label(rf"$\tau = 1000$: \ $BF_{{01}} = {d['bf01'][-1]:.0f}$, \ the null wins", font_size=22, color=RES),
            label(r"Bartlett (1957): \ a vague prior is not harmless here", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But that number depends on tau, the alternative's prior spread, and not weakly. Here is the "
            "Bayes factor for the same data as tau ranges over five orders of magnitude. <bookmark mark='b'/> The most the "
            "alternative can ever do is a factor of point one eight, at a tau of a third. <bookmark mark='c'/> Make the prior "
            "vague, tau of a thousand, and the Bayes factor is three hundred in favour of the null, from data with a p-value "
            "of point oh one. <bookmark mark='d'/> Maurice Bartlett pointed this out in 1957. In estimation a vague prior "
            "washes out; in testing it never does, because it decides how thinly the alternative spreads its predictions."
        ) as vo:
            self.play(FadeIn(A), Create(one))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(mn, scale=2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bic(self):
        d = load("bf")
        rows = [
            cmath(r"\log p(y \mid H)", r"\approx", r"\ell(\hat\theta) - \tfrac{k}{2}\log n", font_size=32),
            cmath(r"\text{BIC}", r"=", r"-2\ell(\hat\theta) + k\log n", font_size=32),
            cmath(r"BF_{01}", r"\approx", rf"\exp\{{\tfrac12(\log n - z^2)\}} = {d['bic01']:.2f}", font_size=30),
            cmath(r"\text{exact, \ unit-information prior}", r":", rf"{d['unit01']:.2f}", font_size=30),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"Laplace's method on the evidence"), why(r"Schwarz (1978)"), why(r"one extra parameter"),
                why(r"Kass \& Wasserman (1995): \ BIC's implicit prior")]
        with self.voiceover(
            "<bookmark mark='a'/> A rough but prior-free version comes from Laplace's approximation to the evidence: the "
            "maximized log likelihood minus half the number of parameters times log n. <bookmark mark='b'/> Twice its "
            "negative is Gideon Schwarz's Bayesian information criterion. <bookmark mark='c'/> For our example it gives a "
            "Bayes factor of point three one. <bookmark mark='d'/> Robert Kass and Larry Wasserman showed that BIC "
            "approximates the exact Bayes factor for a unit-information prior, a normal prior worth one observation, "
            "which gives point three three. Part 28 compares BIC with AIC."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"Bayes factors need proper priors on the parameters being tested", font_size=24, color=RES),
            label(r"report them with the prior, \ and a sensitivity range", font_size=24),
            label(r"point nulls are rarely exactly true: \ is $\mu = 0$ the question?", font_size=24, color=PATH),
            label(r"for estimation, \ the posterior; \ for prediction, \ Part 28's cross-validation", font_size=24, color=SHRUNK),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lessons. Bayes factors need genuine, proper priors on whatever is being tested; "
            "improper priors make them arbitrary. <bookmark mark='b'/> Report them with the prior used, and how they move "
            "as it changes. <bookmark mark='c'/> Ask whether a point null is even the question: an effect of exactly zero is "
            "rarely plausible, and an interval estimate may say more. <bookmark mark='d'/> For estimating sizes, use the "
            "posterior; for choosing models to predict with, Part 28's cross-validation."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def bma(self):
        rows = [
            cmath(r"P(M_k \mid y)", r"=", r"\dfrac{p(y \mid M_k)\, P(M_k)}{\sum_j p(y \mid M_j)\, P(M_j)}", font_size=30),
            cmath(r"p(\Delta \mid y)", r"=", r"\textstyle\sum_k p(\Delta \mid M_k, y)\, P(M_k \mid y)", font_size=30),
            cmath(r"\text{why}", r":", r"\text{choosing one model hides the uncertainty of choosing}", font_size=28),
            cmath(r"\text{caveat}", r":", r"\text{inherits every Bayes factor's prior sensitivity}", font_size=28),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"posterior model probabilities"), why(r"Bayesian model averaging"),
                why(r"Hoeting, Madigan, Raftery \& Volinsky (1999)"), why(r"Part 28's stacking avoids it")]
        with self.voiceover(
            "<bookmark mark='a'/> With several models, Bayes factors give each a posterior probability. <bookmark mark='b'/> "
            "Then any quantity of interest can be averaged across models, weighted by those probabilities: Bayesian model "
            "averaging. <bookmark mark='c'/> It answers a real weakness of choosing one model and reporting it as if it had "
            "been known all along, a problem Part 28 takes up as inference after selection. <bookmark mark='d'/> But the weights inherit "
            "every Bayes factor's sensitivity to priors; Part 28's stacking weights models by predictive performance instead."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
