from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403

PCOL = {"uniform": PRIOR, "Jeffreys": S.ALT, "sceptic": S.CTRL, "pessimist": RES}


class Priors(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.small_n()
        self.large_n()
        self.flat_trap()
        self.jeffreys()
        self.prior_predictive()
        self.kinds()

    def card(self):
        card = chapter_card(5, r"Priors", r"Where they come from, \ and how much they matter", lit=(1939,), part=PART)
        with self.voiceover("Chapter five. Priors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def four(self):
        d = load("priors")
        A = axes([0, 1], [0, 5.5], x_length=7.4, y_length=4.2, xlabel=r"$p$", ylabel=r"prior density", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 2, 4], center=[-2.2, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0.003, 0.997, 300)
        curves = VGroup(*[curve(ax, xs, np.minimum(stats.beta(a, b).pdf(xs), 5.4), PCOL[k], 3) for k, (a, b) in d["priors"].items()])
        rows = fit_rows(VGroup(
            label(r"uniform: \ Beta(1, 1)", font_size=24, color=PRIOR),
            label(r"Jeffreys: \ Beta($\frac12$, $\frac12$)", font_size=24, color=S.ALT),
            label(r"sceptic: \ Beta(20, 20), \ ``surely near a half''", font_size=24, color=S.CTRL),
            label(r"pessimist: \ Beta(2, 8), \ ``probably low''", font_size=24, color=RES),
        ), 4.6, 0.4, [4.5, 0.2, 0])
        with self.voiceover(
            "Where does a prior come from, and does it matter? Take four. <bookmark mark='a'/> The uniform, Bayes's and "
            "Laplace's. <bookmark mark='b'/> Jeffreys's Beta a half, a half, which we'll meet properly in a moment. "
            "<bookmark mark='c'/> A sceptic, Beta twenty twenty, confident that p is close to a half: worth forty imaginary "
            "trials. <bookmark mark='d'/> And a pessimist, Beta two eight, who thinks p is probably low. Now give all four the "
            "same data."
        ) as vo:
            self.play(FadeIn(A))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(rows[k]))
        self.clear_scene()

    def posteriors(self, n, s, center):
        d = load("priors")
        A = axes([0, 1], [0, 10], x_length=6.0, y_length=3.6, xlabel=r"$p$", ylabel=r"", xticks=[0, 0.5, 1], yticks=[], center=center)
        ax = A.ax
        xs = np.linspace(0.002, 0.998, 300)
        cs = VGroup(*[curve(ax, xs, np.minimum(stats.beta(a + s, b + n - s).pdf(xs), 9.8), PCOL[k], 3) for k, (a, b) in d["priors"].items()])
        return A, cs

    def small_n(self):
        d = load("priors")["post"]["10"]
        A, cs = self.posteriors(10, 7, [-3.2, 0.3, 0])
        hd = label(r"7 of 10", font_size=26).next_to(A, UP, buff=0.1)
        tab = table_rows([[r"prior", r"mean", r"95\% interval"]] + [[k, rf"{v['mean']:.2f}", rf"[{v['ci'][0]:.2f}, {v['ci'][1]:.2f}]"]
                                                                     for k, v in d.items()],
                         font_size=24, col_buff=0.5, row_buff=0.22, colors=[GREY_B] + [PCOL[k] for k in d]).move_to([3.7, 0.3, 0])
        foot = label(r"with 10 trials, \ the prior matters: \ the means run from 0.45 to 0.68", font_size=24, color=OBS).move_to([0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With seven successes in ten trials, the four posteriors disagree. The uniform and Jeffreys "
            "priors give means near point seven, close to the data. The sceptic is dragged to point five four, and the "
            "pessimist to point four five. <bookmark mark='b'/> With ten trials, a prior worth forty imaginary trials "
            "dominates. That's not a flaw: if the sceptic really had forty trials' worth of earlier evidence, ten new ones "
            "shouldn't overturn it. The danger is a prior that claims knowledge nobody has."
        ) as vo:
            self.play(FadeIn(A), FadeIn(hd))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(tab, lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def large_n(self):
        d = load("priors")["post"]["100"]
        A, cs = self.posteriors(100, 70, [-3.2, 0.3, 0])
        hd = label(r"70 of 100", font_size=26).next_to(A, UP, buff=0.1)
        tab = table_rows([[r"prior", r"mean", r"95\% interval"]] + [[k, rf"{v['mean']:.2f}", rf"[{v['ci'][0]:.2f}, {v['ci'][1]:.2f}]"]
                                                                     for k, v in d.items()],
                         font_size=24, col_buff=0.5, row_buff=0.22, colors=[GREY_B] + [PCOL[k] for k in d]).move_to([3.7, 0.3, 0])
        foot = label(r"the data swamp the prior: \ ten times the data, \ a quarter of the disagreement", font_size=24, color=OBS).move_to([0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now seventy successes in a hundred. The uniform and Jeffreys posteriors are indistinguishable, "
            "at point seven. Even the sceptic and the pessimist have moved most of the way, to point six four and point six "
            "five, and all four intervals overlap heavily. <bookmark mark='b'/> As the data grow, the likelihood overwhelms any "
            "prior that doesn't rule the truth out completely. That's the Bernstein–von Mises theorem, which Part 53 proves: "
            "with enough data, Bayesian and likelihood answers converge."
        ) as vo:
            self.play(FadeIn(A), FadeIn(hd))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(tab, lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def flat_trap(self):
        d = load("priors")
        A = axes([0, 10], [0, 1.05], x_length=6.4, y_length=3.8, xlabel=r"odds $p/(1 - p)$", ylabel=r"prior density", xticks=[0, 2, 4, 6, 8, 10],
                 yticks=[0, 0.5, 1], center=[-2.6, 0.3, 0])
        ax = A.ax
        cv = density(ax, np.asarray(d["odds"]), np.asarray(d["odds_density"]), PRIOR)
        rows = fit_rows(VGroup(
            label(r"``no idea'' about $p$: \ uniform", font_size=24, color=PRIOR),
            label(r"then the odds are far from uniform", font_size=24),
            MathTex(r"\pi(o) = \frac{1}{(1 + o)^2}", font_size=30, color=PRIOR),
            label(r"half the prior has odds below 1", font_size=22),
            label(r"flat on one scale is informative on another", font_size=24, color=RES),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "Flat priors have a trap. <bookmark mark='a'/> Suppose you know nothing about p, so you make it uniform. "
            "<bookmark mark='b'/> Then what do you believe about the odds? <bookmark mark='c'/> Not that they're uniform: by "
            "Part 5's change of variables, a uniform p gives the odds the density one over one plus o, squared, piled up near "
            "zero. <bookmark mark='d'/> Half the prior has odds below one. <bookmark mark='e'/> A prior that's flat on one "
            "scale is informative on another, and \"knowing nothing\" doesn't pick out a scale. This bothered Laplace's critics "
            "for a century, Boole and Venn among them."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(cv), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def jeffreys(self):
        rows = [
            cmath(r"\pi_J(\theta)", r"\propto", r"\sqrt{I(\theta)}", font_size=36),
            cmath(r"\phi = g(\theta)", r"\Rightarrow", r"\sqrt{I(\phi)} = \sqrt{I(\theta)}\,\Big|\frac{d\theta}{d\phi}\Big|", font_size=32),
            cmath(r"\text{binomial}", r":", r"I(p) = \frac{n}{p(1 - p)}\ \Rightarrow\ \pi_J = \text{Beta}(\tfrac12, \tfrac12)", font_size=30),
            cmath(r"\text{Part 11}", r":", r"\text{the Jeffreys interval}", font_size=30),
        ]
        rows[0][2].set_color(S.ALT)
        whys = [why(r"Jeffreys (1946): \ Part 9's Fisher information"), why(r"it transforms exactly like a density"),
                why(r"the same answer on every scale"), why(r"invariant is not the same as well-calibrated: \ chapter nine")]
        with self.voiceover(
            "Harold Jeffreys found a way out in 1946. <bookmark mark='a'/> Make the prior proportional to the square root of "
            "Part 9's Fisher information. <bookmark mark='b'/> Under a change of parameter, the information changes by the square "
            "of the derivative, so its square root picks up exactly the Jacobian a density needs. Jeffreys's rule gives the "
            "same answer whichever scale you start on. <bookmark mark='c'/> For a binomial probability, the information is n "
            "over p times one minus p, and the Jeffreys prior is Beta a half, a half, heavier at the ends than the uniform. "
            "<bookmark mark='d'/> It's the prior behind Part 11's Jeffreys interval. Invariance is an attractive property, but "
            "it isn't a guarantee of coverage, and chapter nine will find this prior falling short near the edge."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kinds(self):
        rows = fit_rows(VGroup(
            label(r"informative: \ real earlier evidence, \ stated and defended", font_size=26, color=S.CTRL),
            label(r"weakly informative: \ rule out the absurd, \ e.g. \ Cauchy(0, 2.5) on scaled log-odds slopes \ (Gelman et al. 2008)", font_size=24, color=S.LIK),
            label(r"reference and Jeffreys priors: \ let the data speak, \ invariantly", font_size=24, color=S.ALT),
            label(r"improper priors: \ fine if the posterior integrates, \ fatal if it does not", font_size=24, color=RES),
            label(r"always: \ a sensitivity analysis, \ several priors side by side", font_size=26, color=OBS),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "In practice there are several kinds of prior. <bookmark mark='a'/> Informative priors encode real earlier evidence, "
            "a previous trial or a physical law, and should be stated and defended like any other assumption. "
            "<bookmark mark='b'/> Weakly informative priors rule out the absurd without claiming more, for instance a Cauchy "
            "prior with scale two and a half on standardized logistic coefficients, which makes enormous effects unlikely, as "
            "Andrew Gelman and colleagues recommended in 2008. <bookmark mark='c'/> Reference priors, Jeffreys's among them, try to let the data speak. "
            "<bookmark mark='d'/> Improper priors, which don't integrate to one, are acceptable only if the posterior does; "
            "with separated logistic data, as in Part 14, a flat prior gives an improper posterior. <bookmark mark='e'/> And "
            "always do what we just did: a sensitivity analysis, reporting how the conclusion moves across reasonable priors."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def prior_predictive(self):
        rows = [
            cmath(r"\theta \sim \pi,\ \ \tilde y \sim p(y \mid \theta)", r":", r"\text{what the prior expects to see}", font_size=30),
            cmath(r"\text{Beta}(2, 8),\ n = 10", r":", r"P(\tilde s \ge 7) = 0.015", font_size=32),
            cmath(r"\text{observed}", r":", r"s = 7", font_size=32),
            cmath(r"\text{so}", r":", r"\text{the pessimist's prior was surprised: \ reconsider it}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the prior predictive distribution"), why(r"the beta-binomial with the prior's parameters"),
                why(r"the data we actually saw"), why(r"Box (1980): \ prior predictive checks")]
        with self.voiceover(
            "How can a prior be checked? <bookmark mark='a'/> Simulate data from it: draw a parameter from the prior, then data "
            "from the model. That's the prior predictive distribution, what the prior expects to see. <bookmark mark='b'/> The "
            "pessimist's Beta two eight, with ten trials, expects seven or more successes only about one and a half percent of the time. "
            "<bookmark mark='c'/> We saw seven. <bookmark mark='d'/> The pessimist should be surprised, and should ask whether "
            "the prior was reasonable, before trusting the posterior. George Box proposed prior predictive checks in 1980, and "
            "they're now a routine first step: if a prior predicts data that are absurd, like adult heights of five metres, "
            "fix the prior before seeing any data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
