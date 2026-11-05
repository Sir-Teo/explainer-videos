from __future__ import annotations

from videos.stats.stats24.common import *  # noqa: F403


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.three()
        self.lpm()
        self.recipe()

    def card(self):
        card = chapter_card(1, r"Upgrade: \ what Part 14 fitted", r"Two models become one family", lit=(1972,), part=PART)
        with self.voiceover("Chapter one. An upgrade of Part 14."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        u = upgrade_card(14, r"logistic regression for yes-or-no, \ Poisson regression for counts, \ fitted by IRLS",
                         r"two separate models, \ the canonical link, \ variance fixed by the mean, \ independent units",
                         r"one family, \ any link, \ deviance, \ overdispersion, \ many categories, \ clusters",
                         width=11.0, font_size=24).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 14 fitted logistic regression for yes-or-no outcomes and Poisson regression for counts, "
            "and promised that the algorithm behind both, iteratively reweighted least squares, would be explained later. "
            "<bookmark mark='b'/> It treated them as two separate models, each with its natural link, with a variance "
            "fixed by the mean, and with independent units. <bookmark mark='c'/> John Nelder and Robert Wedderburn showed "
            "in 1972 that they are members of one family, fitted by one algorithm. This part builds that family and pushes "
            "it in every direction."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(u[0]), FadeIn(u[1][0]), FadeIn(u[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(u[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(u[1][1][2]))
        self.wait(1.0)
        self.clear_scene()

    def three(self):
        rows = [
            cmath(r"\text{random part}", r":", r"y_i \sim \text{an exponential family}, \ E\,y_i = \mu_i", font_size=30),
            cmath(r"\text{systematic part}", r":", r"\eta_i = x_i^\top\beta", font_size=30),
            cmath(r"\text{link}", r":", r"g(\mu_i) = \eta_i", font_size=30),
            cmath(r"\text{examples}", r":", r"\text{normal + identity; \ binomial + logit; \ Poisson + log}", font_size=28),
        ]
        rows[2][2].set_color(MODEL)
        whys = [why(r"normal, \ binomial, \ Poisson, \ gamma, \ ..."), why(r"the linear predictor, \ as in Part 23"),
                why(r"a monotone map from mean to linear predictor"), why(r"Part 12 and Part 14, \ as special cases")]
        with self.voiceover(
            "A generalized linear model has three parts. <bookmark mark='a'/> A random part: each outcome comes from a "
            "distribution in the exponential family, with mean mu i. <bookmark mark='b'/> A systematic part: a linear "
            "predictor eta i, a linear combination of the covariates, exactly as in Part 23. <bookmark mark='c'/> And a "
            "link function that connects them: g of the mean equals the linear predictor. <bookmark mark='d'/> Normal "
            "errors with the identity link is ordinary regression; binomial with the logit is logistic regression; Poisson "
            "with the log is Poisson regression. Bliss's model is binomial with the probit link."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lpm(self):
        rows = [
            cmath(r"\text{least squares on } y \in \{0, 1\}", r":", r"\hat p = x^\top\hat\beta, \ \text{the linear probability model}", font_size=28),
            cmath(r"\text{problem 1}", r":", r"\hat p < 0 \text{ or } > 1 \text{ at the edges}", font_size=30),
            cmath(r"\text{problem 2}", r":", r"\mathrm{Var}\,y = p(1 - p): \ \text{heteroskedastic by construction}", font_size=30),
            cmath(r"\text{problem 3}", r":", r"\text{effects cannot be constant on a bounded scale}", font_size=30),
        ]
        rows[3][-1].set_color(MODEL)
        whys = [why(r"still common in economics"), why(r"Bliss's highest doses: \ predictions above 1"), why(r"Part 23's HC SEs patch it"), why(r"the link moves to a scale where they can be")]
        with self.voiceover(
            "<bookmark mark='a'/> Why not just run least squares on the zeros and ones? That's the linear probability model, "
            "still common in economics, and with Part 23's robust standard errors it estimates a best linear "
            "approximation honestly. <bookmark mark='b'/> But its fitted probabilities leave zero to one at the edges, as a "
            "straight line through Bliss's beetles would above the highest doses. <bookmark mark='c'/> Its errors are "
            "heteroskedastic by construction, since a yes-or-no outcome has variance p times one minus p. "
            "<bookmark mark='d'/> And an effect cannot be the same size everywhere on a bounded scale: a dose that adds "
            "thirty points to a ten percent death rate cannot add thirty to ninety. The link moves the model to a scale "
            "where constant effects make sense."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def recipe(self):
        rows = fit_rows(VGroup(
            label(r"choose the family: \ what kind of number is $y$?", font_size=24, color=MODEL),
            label(r"choose the link: \ on what scale are effects additive?", font_size=24, color=PATH),
            label(r"fit by IRLS; \ check by the deviance and residuals", font_size=24),
            label(r"if the variance is wrong: \ quasi-likelihood or the sandwich", font_size=24, color=HIT),
            label(r"if units cluster: \ GEE, \ or Part 25's mixed models", font_size=24, color=TEAL),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "The recipe this part follows. <bookmark mark='a'/> Choose the family from what kind of number the outcome is: "
            "a proportion, a count, a positive amount. <bookmark mark='b'/> Choose the link from the scale on which "
            "effects should add up: odds, rates, or the mean itself. <bookmark mark='c'/> Fit by IRLS and check the fit "
            "with the deviance and residuals. <bookmark mark='d'/> If the variance assumed by the family is wrong, use "
            "quasi-likelihood or the sandwich of Parts 22 and 23. <bookmark mark='e'/> And if units come in clusters, use "
            "generalized estimating equations, or wait for Part 25's mixed models."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
