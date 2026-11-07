from __future__ import annotations

import numpy as np

from videos.stats.stats15.common import *  # noqa: F403


class Prediction(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.bars()
        self.why_wider()
        self.kicks()
        self.normal_pred()
        self.checks()

    def card(self):
        card = chapter_card(4, r"Prediction", r"What will the next data look like?", lit=(1774,), part=PART)
        with self.voiceover("Chapter four. Prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def formula(self):
        rows = [
            cmath(r"p(\tilde y \mid y)", r"=", r"\int p(\tilde y \mid \theta)\,\pi(\theta \mid y)\,d\theta", font_size=34),
            cmath(r"\text{Beta}(a, b)\ \text{posterior}", r":", r"P(\tilde k \text{ of } m) = \binom{m}{\tilde k}\frac{B(\tilde k + a,\ m - \tilde k + b)}{B(a, b)}", font_size=28),
            cmath(r"m = 1", r":", r"P(\text{success}) = \frac{a}{a + b}", font_size=32),
            cmath(r"\text{uniform prior}", r":", r"\frac{s + 1}{n + 2}\ \text{(Laplace's rule)}", font_size=32),
        ]
        rows[0][2].set_color(POST)
        whys = [why(r"average the data model over the posterior"), why(r"the beta-binomial distribution"),
                why(r"one new trial: \ the posterior mean"), why(r"the hook's rule of succession")]
        with self.voiceover(
            "<bookmark mark='a'/> To predict new data, don't plug in a single estimate. Average the data model over the "
            "posterior: the posterior predictive distribution. <bookmark mark='b'/> For binomial data with a beta posterior, "
            "the average can be done exactly, and gives the beta-binomial distribution. <bookmark mark='c'/> For a single new "
            "trial, the predictive chance of success is just the posterior mean. <bookmark mark='d'/> With a uniform prior, "
            "that's s plus one over n plus two: Laplace's rule of succession is the simplest posterior predictive."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bars(self):
        d = load("predictive")
        k = np.asarray(d["k"])
        A = axes([-0.6, 10.6], [0, 0.3], x_length=8.0, y_length=4.2, xlabel=r"successes in the next 10 trials", ylabel=r"probability",
                 xticks=list(range(0, 11)), yticks=[0, 0.1, 0.2, 0.3], center=[-1.8, 0.2, 0])
        ax = A.ax
        w = ax.c2p(0.38, 0)[0] - ax.c2p(0, 0)[0]
        b1 = VGroup(*[Rectangle(width=w, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=GREY_B,
                                fill_opacity=0.7).move_to(ax.c2p(kk - 0.2, 0), aligned_edge=DOWN) for kk, v in zip(k, d["plug"])])
        b2 = VGroup(*[Rectangle(width=w, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=POST,
                                fill_opacity=0.85).move_to(ax.c2p(kk + 0.2, 0), aligned_edge=DOWN) for kk, v in zip(k, d["pred"])])
        rows = fit_rows(VGroup(
            label(r"after 7 of 10, \ Beta(9, 5)", font_size=24),
            label(r"grey: \ plug in $\bar p = 9/14$", font_size=24, color=GREY_B),
            label(r"orange: \ the posterior predictive", font_size=24, color=POST),
            MathTex(rf"\text{{SD}}\ {d['plug_sd']:.2f}\ \text{{vs}}\ {d['pred_sd']:.2f}", font_size=28),
            label(r"the predictive is wider, \ and honest", font_size=24, color=OBS),
        ), 4.0, 0.36, [5.0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> After seven successes in ten, with the Beta two two prior, how many successes will the next "
            "ten trials bring? <bookmark mark='b'/> Plugging in the posterior mean, nine fourteenths, gives a binomial distribution in grey, with standard deviation one point five two. Both forecasts now have the same mean. <bookmark mark='c'/> The posterior predictive, in orange, is "
            "wider, with standard deviation one point nine two, and its peak is lower. <bookmark mark='d'/> <bookmark mark='e'/> "
            "The plug-in forecast pretends we know p exactly. The predictive admits we don't."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.05), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def why_wider(self):
        rows = [
            cmath(r"\mathrm{Var}(\tilde k \mid y)", r"=", r"\mathbb E[\mathrm{Var}(\tilde k \mid p) \mid y] + \mathrm{Var}(\mathbb E[\tilde k \mid p] \mid y)", font_size=30),
            cmath(r"\ ", r"=", r"\mathbb E[m p(1 - p) \mid y] + m^2\,\mathrm{Var}(p \mid y)", font_size=32),
            cmath(r"\text{plug-in}", r":", r"m\bar p(1-\bar p);\quad\text{predictive adds }m(m-1)\mathrm{Var}(p\mid y)", font_size=32),
            cmath(r"\text{so}", r":", r"\text{sampling noise} + \text{parameter uncertainty}", font_size=32),
        ]
        rows[3][2].set_color(POST)
        whys = [why(r"Part 5's law of total variance"), why(r"binomial noise, \ plus the spread of $p$"),
                why(r"at equal mean: extra variance is $m(m-1)\mathrm{Var}(p\mid y)$"), why(r"it vanishes only as $n \to \infty$")]
        with self.voiceover(
            "<bookmark mark='a'/> Why wider? Part 5's law of total variance: the predictive variance is the average sampling "
            "variance, plus the variance of the mean across the posterior. <bookmark mark='b'/> For the binomial, that's the "
            "familiar m p one minus p, averaged, plus m squared times the posterior variance of p. <bookmark mark='c'/> The "
            "plug-in variance at the posterior mean exceeds the first term by m times the posterior variance of p; the predictive adds m times m minus one times that variance beyond the plug-in. For one new Bernoulli trial the predictive and plug-in coincide. <bookmark mark='d'/> A forecast must carry both the noise of the next "
            "data and our uncertainty about the parameter. The second shrinks as the data grow, but with ten trials it's "
            "large: it multiplies by m squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def normal_pred(self):
        rows = [
            cmath(r"\tilde x \mid x", r"\sim", r"\bar x + s\sqrt{1 + 1/n}\;t_{n - 1}", font_size=34),
            cmath(r"\text{Part 11}", r":", r"\text{the prediction interval } \bar x \pm t\, s\sqrt{1 + 1/n}", font_size=32),
            cmath(r"1", r"\leftrightarrow", r"\text{the new observation's own noise}", font_size=32),
            cmath(r"1/n", r"\leftrightarrow", r"\text{our uncertainty about } \mu", font_size=32),
        ]
        rows[0][2].set_color(POST)
        whys = [why(r"the normal model, \ reference prior (chapter six)"), why(r"the same interval, \ read as a probability"),
                why(r"sampling noise"), why(r"parameter uncertainty")]
        with self.voiceover(
            "<bookmark mark='a'/> For normal data with the reference prior of chapter six, the predictive distribution of one "
            "new observation is a t distribution centred at the sample mean, with scale s times the square root of one plus "
            "one over n. <bookmark mark='b'/> That's exactly Part 11's prediction interval, now read as a probability "
            "statement about the next value. <bookmark mark='c'/> The one under the root is the new observation's own noise; "
            "<bookmark mark='d'/> the one over n is our uncertainty about mu. Same two ingredients."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def checks(self):
        rows = fit_rows(VGroup(
            label(r"the predictive also tests the model", font_size=26),
            label(r"simulate replicated datasets from the posterior predictive", font_size=24, color=POST),
            label(r"compare a feature of the real data with the replicates", font_size=24),
            label(r"if the real data look unlike every replicate, \ the model is missing something", font_size=24, color=RES),
            label(r"posterior predictive checks: \ Rubin (1984), \ Gelman et al. \ (Part 26)", font_size=22, color=GREY_A),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The predictive distribution has a second use: checking the model. <bookmark mark='b'/> Simulate "
            "many replicated datasets from it, datasets the fitted model says could have happened. <bookmark mark='c'/> Then "
            "compare some feature of the real data, its largest value, say, or its number of runs, with the same feature in "
            "the replicates. <bookmark mark='d'/> If the real data look unlike all of them, the model is missing something. "
            "<bookmark mark='e'/> These posterior predictive checks, developed by Donald Rubin in 1984 and by Andrew Gelman and "
            "colleagues since, are a core part of the Bayesian workflow in Part 26."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def kicks(self):
        rows = [
            cmath(r"\text{Gamma}(\alpha, \beta)\ \text{posterior}", r"\Rightarrow", r"\tilde y \sim \text{negative binomial}", font_size=30),
            cmath(r"P(\tilde y = 0)", r"=", r"\Big(\frac{\beta}{\beta + 1}\Big)^{\alpha} = \Big(\frac{201}{202}\Big)^{123} = 0.543", font_size=30),
            cmath(r"\text{plug-in}", r":", r"e^{-0.61} = 0.543", font_size=32),
            cmath(r"\text{so}", r":", r"\text{with 200 corps-years, \ parameter uncertainty is negligible}", font_size=30),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"a gamma-mixed Poisson, \ Part 14's overdispersion"), why(r"next year, \ one corps: \ no deaths"),
                why(r"almost identical"), why(r"the predictive matters most when data are few")]
        intro = label('Predict the next count by averaging over the rate', font_size=36)
        with self.voiceover(
            "Contrast the horse kicks of chapter two. <bookmark mark='a'/> A gamma posterior for a Poisson rate makes the "
            "predictive distribution of next year's count a negative binomial, the gamma-mixed Poisson of Part 14. "
            "<bookmark mark='b'/> The predictive probability that a given corps has no deaths next year is two hundred and one "
            "over two hundred and two, to the power one hundred and twenty-three: point five four three. <bookmark mark='c'/> "
            "Plugging in the estimated rate gives e to the minus point six one, also point five four three. "
            "<bookmark mark='d'/> With two hundred corps-years of data, the uncertainty about the rate is negligible next to the "
            "Poisson noise. The difference is small for this one-year prediction, though it can matter for longer prediction horizons even with substantial data."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
