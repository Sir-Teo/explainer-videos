from __future__ import annotations

from videos.stats.stats22.common import *  # noqa: F403


class Upgrade(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.score()
        self.conditions()
        self.tanks()

    def card(self):
        card = chapter_card(1, r"Upgrade: \ what Part 9 promised", r"From statement to proof", lit=(1922,), part=PART)
        with self.voiceover("Chapter one. An upgrade of Part 9."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        u = upgrade_card(9, r"the MLE is consistent and approximately normal, \ with variance $1/(n\,I(\theta))$",
                         r"smooth likelihoods, \ a fixed number of parameters, \ a true model; \ and no proof",
                         r"the proofs, \ the conditions they need, \ and what breaks when a condition fails",
                         width=11.0, font_size=24).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 9 introduced maximum likelihood and made two promises: the maximum likelihood estimator "
            "is consistent, closing in on the truth as the sample grows, and it is approximately normal with variance one over "
            "n times the Fisher information. <bookmark mark='b'/> It quietly assumed a smooth likelihood, a fixed number of "
            "parameters, and a model that is actually true, and it proved nothing. <bookmark mark='c'/> Now we prove both "
            "promises, see exactly which conditions the proofs use, and then break each condition in turn."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(u[0]), FadeIn(u[1][0]), FadeIn(u[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(u[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(u[1][1][2]))
        self.wait(1.0)
        self.clear_scene()

    def score(self):
        rows = [
            cmath(r"U(\theta)", r"=", r"\frac{\partial}{\partial\theta}\log f(X;\theta)", font_size=30),
            cmath(r"E_\theta\, U", r"=", r"\int \frac{\partial_\theta f}{f}\, f\, dx = \partial_\theta \int f\, dx = 0", font_size=30),
            cmath(r"\mathrm{Var}_\theta\, U", r"=", r"-E_\theta\, \frac{\partial^2}{\partial\theta^2}\log f(X;\theta) = I(\theta)", font_size=30),
            cmath(r"\text{for } n \text{ observations}", r":", r"E\,U_n = 0, \ \ \mathrm{Var}\,U_n = n\,I(\theta)", font_size=30),
        ]
        rows[2][2].set_color(LIK)
        whys = [why(r"the score: \ the slope of one log likelihood"), why(r"swap derivative and integral"),
                why(r"differentiate the first identity once more"), why(r"independent scores add")]
        intro = label('Score identities require differentiation under the integral', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Two identities carry everything. <bookmark mark='a'/> The score is the derivative of an observation's "
            "log likelihood with respect to theta. <bookmark mark='b'/> At the true theta its expectation is zero: "
            "it's the derivative of the integral of the density, which is one for every theta. <bookmark mark='c'/> "
            "Differentiate that identity again and you find that the score's variance equals minus the expected "
            "second derivative: the Fisher information, two definitions that agree. <bookmark mark='d'/> For n "
            "independent identically distributed observations the scores add: mean zero, variance n times I. Both "
            "steps need the derivative to pass through the integral, our first regularity condition."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def conditions(self):
        rows = fit_rows(VGroup(
            label(r"1. \ the support does not depend on $\theta$", font_size=24, color=LIK),
            label(r"2. \ the truth is inside the parameter space, \ not on its edge", font_size=24, color=LIK),
            label(r"3. \ local smoothness, \ integrable derivative envelopes, \ nonsingular information", font_size=24, color=LIK),
            label(r"4. \ identifiable: \ different $\theta$, \ different distributions", font_size=24, color=LIK),
            label(r"5. \ a fixed number of parameters, \ however large $n$", font_size=24, color=LIK),
            label(r"6. \ the model is true", font_size=24, color=LIK),
            label(r"broken here: \ 1 in chapter 1, \ 2--4 in chapter 9, \ 5 in chapter 7, \ 6 in chapter 10", font_size=22, color=RES),
        ), 12.4, 0.38, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is a useful checklist of sufficient regularity assumptions, not a complete "
            "theorem. We also need integrability and uniform local derivative control, nonsingular information, and a"
            " consistent interior solution. The set of possible values doesn't depend on theta; <bookmark mark='b'/> "
            "the true value is in the interior of the parameter space; <bookmark mark='c'/> the log likelihood has "
            "three derivatives, suitably bounded; <bookmark mark='d'/> the model is identifiable, so different "
            "parameters give different distributions; <bookmark mark='e'/> the number of parameters stays fixed as n "
            "grows; <bookmark mark='f'/> and the model is true. <bookmark mark='g'/> This part breaks every one of "
            "them: the first in a moment, the second, third and fourth in chapter nine, the fifth in chapter seven, "
            "the sixth in chapter ten."
        ) as vo:
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def tanks(self):
        rows = [
            cmath(r"X_i \sim \text{Uniform}(0, \theta)", r":", r"\text{the support depends on } \theta", font_size=30),
            cmath(r"\hat\theta_{\text{MLE}}", r"=", r"\max_i X_i", font_size=30),
            cmath(r"\theta - \hat\theta", r"\approx", r"\theta / n, \ \text{not } 1/\sqrt n", font_size=30),
            cmath(r"n(\theta - \hat\theta)/\theta", r"\to", r"\text{Exponential}(1), \ \text{not normal}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"continuous analogue of Part 9's tanks"), why(r"the likelihood $\theta^{-n}$ on $\theta \ge \max X_i$"),
                why(r"faster than the usual rate"), why(r"no score identity, \ no CLT")]
        intro = label('Parameter-dependent support changes the limiting distribution', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> A continuous analogue of Part 9's German tank problem breaks the fixed-support "
            "assumption. Independent Uniform zero theta observations have a support that depends on theta. This "
            "differs from discrete serial numbers sampled without replacement. <bookmark mark='b'/> The likelihood is"
            " theta to the minus n, but only for theta at least the largest serial number, so the maximum likelihood "
            "estimate is the largest number seen. <bookmark mark='c'/> Its error shrinks like one over n, much faster"
            " than the usual one over root n, <bookmark mark='d'/> and its scaled error is exponential, not normal. "
            "The theory of this part doesn't apply, and the root-n regular benchmark does not apply to this different"
            " model."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
