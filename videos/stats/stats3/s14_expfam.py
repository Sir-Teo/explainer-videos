from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403


class ExpFam(VoiceoverScene):
    def construct(self):
        self.card()
        self.form()
        self.members()
        self.mean()
        self.ahead()

    def card(self):
        card = chapter_card(13, r"Exponential families", r"One formula behind most of the family", lit=(),
                            part=PART)
        with self.voiceover("Chapter thirteen. Exponential families, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def form(self):
        f = cmath(r"f(x \mid \eta)", r"=", r"h(x)", r"\,\exp\!\big(", r"\eta", r"\, T(x)", r"-", r"A(\eta)", r"\big)",
                  font_size=48).move_to([0, 1.4, 0])
        f[4].set_color(S.ACCENT)
        f[5].set_color(S.LIK)
        f[7].set_color(S.POST)
        braces = VGroup(
            brace_note(f[4], r"natural parameter", direction=DOWN, color=S.ACCENT, font_size=22),
            brace_note(f[5], r"sufficient statistic", direction=UP, color=S.LIK, font_size=22),
            brace_note(f[7], r"log-normalizer", direction=DOWN, color=S.POST, font_size=22),
        )
        hc = label(r"Darmois, Koopman, Pitman (1935--36): \ the families with fixed-size sufficient statistics",
                   font_size=22, color=GREY_B).to_edge(DOWN, buff=0.5)
        if hc.width > 13:
            hc.width = 13
        with self.voiceover(
            "Look across the family tree and one formula keeps appearing. <bookmark mark='a'/> The density is a "
            "function of x alone, times the exponential of a parameter eta times a statistic T of x, minus a "
            "function A of eta. <bookmark mark='b'/> Eta is the natural parameter, T is the sufficient statistic, "
            "and A, the log-normalizer, is whatever makes the density integrate to one. <bookmark mark='c'/> "
            "Families of this form are called exponential families. Three mathematicians, Darmois, Koopman and "
            "Pitman, showed independently in the mid-1930s that they're exactly the families in which a fixed "
            "number of summaries can capture everything a sample of any size says about the parameter."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in braces], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.clear_scene()

    def members(self):
        head = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (r"family", r"$\eta$", r"$T(x)$", r"$A(\eta)$")])
        data = [
            (r"Bernoulli$(p)$", r"\log\frac{p}{1-p}", r"x", r"\log(1 + e^\eta)"),
            (r"Poisson$(\lambda)$", r"\log\lambda", r"x", r"e^\eta"),
            (r"normal$(\mu, 1)$", r"\mu", r"x", r"\eta^2/2"),
            (r"exponential$(\lambda)$", r"-\lambda", r"x", r"-\log(-\eta)"),
            (r"binomial$(n, p)$", r"\log\frac{p}{1-p}", r"x", r"n\log(1 + e^\eta)"),
        ]
        rows = VGroup(head)
        for nm, eta, t, a in data:
            rows.add(VGroup(label(nm, font_size=26), MathTex(eta, font_size=30, color=S.ACCENT),
                            MathTex(t, font_size=30, color=S.LIK), MathTex(a, font_size=30, color=S.POST)))
        xs = [-4.6, -1.2, 1.4, 4.2]
        y = 2.6
        for r in rows:
            for m, x in zip(r, xs):
                m.move_to([x, y, 0])
            y -= 0.95
        line = Line([-6.4, 2.15, 0], [6.4, 2.15, 0], color=GREY_D)
        note_ = label(r"not members: \ the uniform on $[0, \theta]$, \ Cauchy, \ $t$: \ their supports or tails do not fit",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Many of our distributions fit the form. <bookmark mark='a'/> The Bernoulli: write p to the x times one "
            "minus p to the one minus x as an exponential, and the natural parameter is the log odds, the logit. "
            "<bookmark mark='b'/> The Poisson: the natural parameter is log lambda. The normal with known variance: "
            "the mean itself. The exponential, and the binomial with a fixed number of trials. "
            "<bookmark mark='c'/> Not everything fits: the uniform on zero to theta, whose support moves with the "
            "parameter, and the Cauchy and t, whose tails don't have the exponential form."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[2:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def mean(self):
        d = load("expfam")
        rows = [
            cmath(r"\int h(x)\, e^{\eta T(x) - A(\eta)}\, dx", r"=", r"1", font_size=34),
            cmath(r"\int \big(T(x) - A'(\eta)\big)\, f(x \mid \eta)\, dx", r"=", r"0", font_size=34),
            cmath(r"A'(\eta)", r"=", r"E_\eta\, T(X)", font_size=40),
            cmath(r"A''(\eta)", r"=", r"\mathrm{Var}_\eta\, T(X)", r"\ge", r"0", font_size=40),
        ]
        rows[2][0].set_color(S.POST)
        rows[3][0].set_color(S.POST)
        whys = [why(r"$f$ is a density, \ for every $\eta$"), why(r"differentiate in $\eta$"), why(r"rearrange"),
                why(r"once more: \ $A$ is convex")]
        chk = VGroup(*[MathTex(rf"\text{{{r[0]}}}: A'(\eta) = {r[2]:.6f},\ \ E T = {r[3]:g}", font_size=22, color=SIM)
                       for r in d["rows"][::2]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.35)
        with self.voiceover(
            "The log-normalizer is more than a constant: it generates the moments. <bookmark mark='a'/> The density "
            "integrates to one for every value of eta. <bookmark mark='b'/> Differentiate that identity with "
            "respect to eta. <bookmark mark='c'/> The derivative of A is the expectation of the sufficient "
            "statistic. <bookmark mark='d'/> Differentiate again and A's second derivative is its variance, which "
            "is never negative, so A is convex. For the Poisson, A is e to the eta, and both derivatives give "
            "lambda: mean and variance equal, as we've seen. Numerical derivatives confirm it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.5)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k in (2, 3))
            self.play(FadeIn(chk))
        self.clear_scene()

    def ahead(self):
        items = VGroup(
            label(r"sufficiency: \ $\sum_i T(x_i)$ says everything about $\eta$ \ (Parts 9, 45)", font_size=28),
            label(r"maximum likelihood: \ solve $A'(\hat\eta) = \bar T$ \ (Part 22)", font_size=28),
            label(r"generalized linear models: \ $\eta$ linear in covariates \ (Part 24)", font_size=28),
            label(r"conjugate priors: \ posteriors stay in the family \ (Part 15)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        head = label(r"Why the form matters", font_size=36, color=S.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Why care? Because the form makes almost everything easy. <bookmark mark='a'/> The sum of T over a "
            "sample carries all the information about the parameter: that's sufficiency, Parts 9 and 45. "
            "<bookmark mark='b'/> Maximum likelihood reduces to matching A prime to the sample average of T. "
            "<bookmark mark='c'/> Make the natural parameter a linear function of covariates and you have the "
            "generalized linear models of Part 24, logistic and Poisson regression among them. "
            "<bookmark mark='d'/> And Bayesian updating stays inside the family, with conjugate priors, in Part 15."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(items[k], shift=RIGHT * 0.2))
        self.clear_scene()
