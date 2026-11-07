from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats22.common import *  # noqa: F403


class NeymanScott(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_problem()
        self.derive()
        self.simulate()
        self.why_profile()
        self.fixes()
        self.board()

    def card(self):
        card = chapter_card(7, r"Neyman--Scott", r"When the parameters grow with the data", lit=(1948,), part=PART)
        with self.voiceover("Chapter seven. The Neyman–Scott problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_problem(self):
        rows = [
            cmath(r"x_{i1}, x_{i2}", r"\sim", r"N(\mu_i, \sigma^2), \ \ i = 1, \dots, n", font_size=30),
            cmath(r"\text{parameters}", r":", r"\mu_1, \dots, \mu_n, \ \sigma^2: \ n + 1 \text{ of them}", font_size=30),
            cmath(r"\text{e.g.}", r":", r"\text{each patient measured twice; \ each lab's two readings}", font_size=28),
            cmath(r"\text{the wish}", r":", r"\sigma^2, \ \text{the measurement error}", font_size=30),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"pairs, \ each with its own mean"), why(r"they grow with the data"),
                why(r"incidental parameters"), why(r"the structural parameter")]
        intro = label('Each pair introduces a new nuisance mean', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Jerzy Neyman and Elizabeth Scott found in 1948 how to break maximum likelihood. <bookmark mark='a'/> Observe "
            "pairs of measurements; each pair has its own mean, mu i, and every measurement the same error variance sigma "
            "squared. <bookmark mark='b'/> There are n plus one parameters, and each new pair brings a new one. "
            "<bookmark mark='c'/> It's an ordinary situation: each patient's blood pressure measured twice, or each lab's two "
            "readings of a sample. <bookmark mark='d'/> We don't care about the means, which Neyman and Scott called "
            "incidental parameters; we want sigma squared, the precision of the measurement."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\hat\mu_i", r"=", r"\tfrac12(x_{i1} + x_{i2})", font_size=30),
            cmath(r"\hat\sigma^2", r"=", r"\frac{1}{2n}\textstyle\sum_i \sum_j (x_{ij} - \hat\mu_i)^2 = \frac{1}{4n}\sum_i (x_{i1} - x_{i2})^2", font_size=28),
            cmath(r"E(x_{i1} - x_{i2})^2", r"=", r"2\sigma^2", font_size=30),
            cmath(r"\hat\sigma^2", r"\to", r"\sigma^2 / 2", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"each pair's own average"), why(r"the MLE: \ divide by the number of observations"),
                why(r"the difference cancels $\mu_i$"), why(r"inconsistent: \ wrong by half, \ forever")]
        intro = label('The incidental-mean variance MLE converges to half the truth', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Maximize the likelihood: each mean is estimated by its pair's average. "
            "<bookmark mark='b'/> Then sigma squared is estimated by the average squared deviation from those averages, which "
            "works out as the sum of squared differences within pairs divided by four n. <bookmark mark='c'/> But the "
            "expected squared difference is two sigma squared. <bookmark mark='d'/> So the estimate converges to half the true "
            "variance, no matter how many pairs we collect. Each pair spends one of its two observations estimating its own "
            "mean, and the maximum likelihood estimate never charges for it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simulate(self):
        d = load("neyman")
        A = axes([0, 1.3], [0, 3.4], x_length=8.4, y_length=3.0, xlabel=r"estimate of $\sigma^2$ \ (truth 1)", xticks=[0, 0.25, 0.5, 0.75, 1.0, 1.25],
                 center=[-0.8, 0.6, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 3.4), color=TRUE, stroke_width=2.5)
        g = np.random.Generator(np.random.PCG64(48))
        mle = VGroup(*[Dot(ax.c2p(v, 2.3 + 0.6 * (g.random() - 0.5)), radius=0.035, color=RES) for v in d["mles"]])
        fix = VGroup(*[Dot(ax.c2p(v, 1.0 + 0.6 * (g.random() - 0.5)), radius=0.035, color=HIT) for v in d["fixeds"]])
        lm = label(rf"the MLE: \ mean {d['mle']:.3f}", font_size=22, color=RES).next_to(ax.c2p(0.5, 2.62), UP, buff=0.12)
        lf = label(rf"divide by $2n$: \ {d['fixed']:.3f}", font_size=22, color=HIT).next_to(ax.c2p(1.16, 1.0), RIGHT, buff=0.2)
        rows = fit_rows(VGroup(
            label(rf"300 data sets of {d['pairs']:,} pairs, \ $\sigma^2 = 1$", font_size=22),
            label(r"the MLE is tightly concentrated, \ around the wrong answer", font_size=22, color=RES),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulation: three hundred data sets, each of a thousand pairs, with the true variance one. "
            "<bookmark mark='b'/> The maximum likelihood estimates cluster tightly around point five oh two, "
            "<bookmark mark='c'/> very precisely wrong. <bookmark mark='d'/> Dividing by two n instead of four n, which is what "
            "anyone using the within-pair differences directly would do, gives one point oh oh three."
        ) as vo:
            self.play(FadeIn(A), Create(truth), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in mle], lag_ratio=0.01), FadeIn(lm))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in fix], lag_ratio=0.01), FadeIn(lf))
        self.clear_scene()

    def why_profile(self):
        rows = [
            cmath(r"\ell_p(\sigma^2)", r"=", r"-n \log \sigma^2 - \textstyle\sum_i d_i^2 / (4\sigma^2)", font_size=30),
            cmath(r"\ell_m(\sigma^2)", r"=", r"-\tfrac{n}{2} \log \sigma^2 - \textstyle\sum_i d_i^2 / (4\sigma^2)", font_size=30),
            cmath(r"\text{the difference}", r":", r"-\tfrac n2 \log \sigma^2, \ \text{one half-unit per pair}", font_size=30),
            cmath(r"\text{in general}", r":", r"\text{incidental bias can persist when information per nuisance stays bounded}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"profile out each $\mu_i$: \ $d_i = x_{i1} - x_{i2}$"), why(r"the marginal likelihood of the $d_i$ alone"),
                why(r"the profile's extra pull towards small $\sigma^2$"), why(r"fixed dimension plus regularity avoids this example")]
        intro = label('The contrast likelihood removes the incidental means', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Chapter five distinguished first-order nuisance adjustment from the incidental-parameter problem. Here "
            "the number of means grows with the data. <bookmark mark='a'/> Profile out each pair's mean, and the log "
            "likelihood for sigma squared is minus n log sigma squared, minus the sum of squared differences over "
            "four sigma squared. <bookmark mark='b'/> The likelihood of the differences alone, a genuine likelihood, "
            "has the same second term but only half the first. <bookmark mark='c'/> The profile's extra minus n over "
            "two log sigma squared drags the maximum towards small variances, by exactly a factor of two. <bookmark "
            "mark='d'/> Here each new nuisance mean still has only two observations, so its estimation error does not"
            " vanish and the variance bias persists. Growing dimension is not automatically fatal in every model; "
            "rates depend on how much information each nuisance parameter receives."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.82, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fixes(self):
        rows = [
            cmath(r"\text{marginal likelihood}", r":", r"\text{use only } d_i = x_{i1} - x_{i2} \sim N(0, 2\sigma^2)", font_size=28),
            cmath(r"\text{conditional likelihood}", r":", r"\text{condition on the sufficient statistics for } \mu_i", font_size=28),
            cmath(r"\text{REML}", r":", r"\text{the same idea for mixed models (Part 25)}", font_size=28),
            cmath(r"\text{panel data}", r":", r"\text{nonlinear short-panel fixed effects can have this trap}", font_size=28),
        ]
        rows[0][2].set_color(HIT)
        whys = [why(r"a likelihood free of the nuisance"), why(r"Andersen (1970) for logit models"),
                why(r"restricted maximum likelihood"), why(r"Lancaster (2000)")]
        intro = label('Eliminate nuisance parameters through suitable contrasts or conditioning', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "The cures all remove the incidental parameters before maximizing. <bookmark mark='a'/> The marginal "
            "likelihood uses only the within-pair differences, whose distribution doesn't involve the means at all; "
            "maximizing it gives the right answer. <bookmark mark='b'/> A conditional likelihood conditions on "
            "statistics that capture the nuisance parameters, as Erling Andersen did for logistic models in 1970. "
            "<bookmark mark='c'/> Restricted maximum likelihood, REML, applies the same idea to mixed models, as Part"
            " 25 will. <bookmark mark='d'/> And economists meet the problem in nonlinear short-panel fixed-effect "
            "models. Ordinary linear fixed-effect slopes need not suffer this same inconsistency."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=22) if r.part == 22][2:3]
        b = coverage_board(rows, lit_part=22, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The Board: a Wald interval for sigma squared built from the maximum likelihood "
            "estimate and the inverse-profile-curvature standard error, two hundred pairs, a thousand data sets. "
            "Coverage: zero. Not one of a thousand intervals contains the truth, because they're all centred on half "
            "of it."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
        self.wait(1.0)
        self.clear_scene()
