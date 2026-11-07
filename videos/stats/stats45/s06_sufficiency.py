from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Sufficiency(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.minimal()
        self.table()
        self.completeness()
        self.range_law()
        self.fullrank()

    def card(self):
        card = chapter_card(5, r"Sufficiency in general", r"When can data be thrown away without loss?", lit=(1949,), part=PART)
        with self.voiceover("Chapter five. Sufficiency in general: when can data be thrown away without loss?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"T \text{ sufficient}", r":", r"P_\theta(X \in \cdot \mid T) \text{ does not depend on } \theta", font_size=32),
            cmath(r"\text{equivalently}", r":", r"E_\theta[f(X) \mid \sigma(T)] \text{ is the same for all } \theta", font_size=32),
            cmath(r"\{P_\theta\}\ll\nu,\ \nu\text{ sigma-finite}", r"\Rightarrow", r"T \text{ sufficient} \iff p_\theta(x) = g_\theta(T(x))\, h(x)", font_size=32),
            cmath(r"\text{proof}", r":", r"\text{a countable mixture } \textstyle\sum c_i P_{\theta_i} \text{ dominates all } P_\theta", font_size=30),
        ]
        rows[0][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(ADMC)
        whys = [why(r"Fisher (1922)"), why(r"Part 44's conditional expectation"), why(r"Halmos--Savage (1949)"), why(r"the key lemma")]
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's definition, from 1922: a statistic T is sufficient if, once T is known, "
            "the conditional law of the rest of the data no longer depends on the parameter. <bookmark mark='b'/> In "
            "Part forty-four's language, conditional expectations given the sigma-algebra of T can be chosen the same"
            " for every theta. <bookmark mark='c'/> Paul Halmos and Jimmie Savage proved the factorization theorem in"
            " this generality in 1949: for a family dominated by a common sigma-finite measure, T is sufficient "
            "exactly when each density factors into a function of theta and T, times a function of the data alone. "
            "<bookmark mark='d'/> The key step is a lemma: a family dominated by a sigma-finite measure admits a "
            "dominating countable mixture of its own members, which plays the role of a reference measure that no "
            "parameter value can see past."
        ) as vo:
            heading=label('Sufficiency permits a common parameter-free conditional law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def minimal(self):
        rows = [
            cmath(r"T \text{ minimal sufficient}", r":", r"\text{a function of every sufficient statistic}", font_size=32),
            cmath(r"\text{test}", r":", r"\tfrac{p_\theta(x)}{p_\theta(y)} \text{ free of } \theta \iff T(x) = T(y)", font_size=34),
            cmath(r"\text{normal}", r":", r"\tfrac{p(x)}{p(y)} = e^{-\{\sum x_i^2 - \sum y_i^2 - 2\mu(\sum x_i - \sum y_i)\}/2\sigma^2}", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"T = (\textstyle\sum x_i, \sum x_i^2), \ \text{equivalently } (\bar x, s^2)", font_size=32),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"the coarsest lossless summary"), why(r"Lehmann--Scheff\'e (1950)"), why(r"the ratio of two samples"), why(r"two numbers, \ any $n$")]
        with self.voiceover(
            "<bookmark mark='a'/> Sufficient statistics are not unique: the whole data set is one. The useful one is "
            "minimal, a function of every other sufficient statistic, the coarsest summary that loses nothing. "
            "<bookmark mark='b'/> Erich Lehmann and Henry Scheffé gave a test in 1950: two samples should be lumped "
            "together exactly when their likelihood ratio does not depend on the parameter. <bookmark mark='c'/> For "
            "the normal, the ratio involves the data only through the sums of the observations and of their squares, "
            "<bookmark mark='d'/> so those two numbers, or equivalently its mean and the sample variance, are minimal"
            " sufficient for n at least two."
        ) as vo:
            heading=label('Minimal sufficiency identifies proportional likelihoods',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        rows = [[r"family", r"minimal sufficient", r"complete?"],
                [r"$N(\mu, \sigma^2)$", r"$(\bar x, s^2)$", r"yes"],
                [r"Poisson, \ binomial", r"$\sum x_i$", r"yes"],
                [r"$U(0, \theta)$", r"$\max x_i$", r"yes"],
                [r"$U(\theta, \theta + 1)$", r"$(\min x_i, \max x_i)$", r"no"],
                [r"$N(\theta, \theta^2)$, $\theta>0$", r"$(\sum x_i, \sum x_i^2)$", r"no"],
                [r"Cauchy, \ Laplace location", r"the order statistics", r"no"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.28, colors=[GREY_A, None, None, None, MMC, MMC, INADC]).move_to([0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A small catalogue. <bookmark mark='b'/> For the normal, the mean and the variance; for "
            "the Poisson and the binomial, the total count; for the uniform on zero to theta, the maximum. These are all "
            "complete, a property defined next. <bookmark mark='c'/> The uniform on theta to theta plus one needs both the "
            "minimum and the maximum, and the normal whose standard deviation equals its mean, a curved family, still needs "
            "two numbers for one parameter; neither is complete. <bookmark mark='d'/> For the Cauchy and the Laplace "
            "location families, nothing short of the whole sorted sample will do."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:4]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]))
            vo.wait_until("d")
            self.play(FadeIn(tab[6]))
        self.clear_scene()

    def completeness(self):
        rows = [
            cmath(r"T \text{ complete}", r":", r"E_\theta\, g(T) = 0 \ \forall \theta \ \Rightarrow \ g(T) = 0 \text{ a.s.}", font_size=32),
            cmath(r"\text{binomial}", r":", r"\textstyle\sum_x g(x)\binom{n}{x} r^x = 0 \ \forall r = \tfrac{p}{1-p} \Rightarrow g \equiv 0", font_size=30),
            cmath(r"U(\theta, \theta + 1)", r":", r"g = \max - \min - \tfrac{n - 1}{n + 1} \text{ has mean } 0 \text{ for every } \theta", font_size=30),
            cmath(r"\text{meaning}", r":", r"T \text{ carries no ``noise'' that averages to nothing}", font_size=32),
        ]
        rows[0][-1].set_color(S.ACCENT)
        rows[1][-1].set_color(ADMC)
        rows[2][-1].set_color(INADC)
        whys = [why(r"only zero is unbiased for zero"), why(r"a polynomial with all roots"), why(r"not complete"), why(r"for Lehmann--Scheff\'e")]
        with self.voiceover(
            "<bookmark mark='a'/> A statistic is complete if every function integrable under all parameter values, "
            "with mean zero for every theta, vanishes almost surely under every model law. <bookmark mark='b'/> For "
            "the binomial, a function with mean zero gives a polynomial in the odds that vanishes for every value of "
            "the odds, so every coefficient is zero: the count is complete. <bookmark mark='c'/> For the uniform on "
            "theta to theta plus one, the range minus its expectation, n minus one over n plus one, has mean zero for"
            " every theta but is not zero: the minimal sufficient statistic is not complete. <bookmark mark='d'/> "
            "Completeness says that the statistic carries no component whose average is always nothing, no pure "
            "noise. That is exactly what the next chapter needs to make a best unbiased estimator unique."
        ) as vo:
            heading=label('Completeness rules out integrable nonzero unbiased zeros',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def range_law(self):
        n = 5
        r = np.linspace(0, 1, 201)
        f = n * (n - 1) * r ** (n - 2) * (1 - r)
        A = axes([0, 1], [0, 2.4], x_length=7.4, y_length=4.4, xlabel=r"range $\max x_i - \min x_i$", ylabel=r"density",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        dens = density(ax, r, f, MMC, 4, 0.3)
        mean = (n - 1) / (n + 1)
        ml = DashedLine(ax.c2p(mean, 0), ax.c2p(mean, 2.3), color=S.ACCENT, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"$n = {n}$ from $U(\theta, \theta + 1)$", font_size=22),
            label(r"the range has density $n(n - 1) r^{n-2}(1 - r)$", font_size=22, color=MMC),
            label(r"the same for $\theta = 0$, \ $\theta = 5$, \ any $\theta$: \ ancillary", font_size=22, color=S.ACCENT),
            label(rf"$R-E R$: mean zero; $E R={mean:.3f}$; a nonzero function of $T$", font_size=22, color=INADC),
            label(r"yet it tells us how precise this sample is", font_size=22, color=ADMC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is that offending piece of the uniform's sufficient statistic. Take five observations "
            f"from the uniform on theta to theta plus one. <bookmark mark='b'/> The range, the maximum minus the minimum, has "
            f"this beta-shaped density, <bookmark mark='c'/> and shifting theta shifts every observation together, so the "
            f"range's law is the same for every theta: it is ancillary, carrying no information about theta by itself. "
            f"<bookmark mark='d'/> Its mean, {say(mean, 3)}, is the constant that makes the counterexample to "
            f"completeness. <bookmark mark='e'/> Yet the range is far from useless: a wide range pins theta down tightly. "
            f"Chapter seven returns to this."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ the law of the range")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dens), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ml), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def fullrank(self):
        rows = fit_rows(VGroup(
            label(r"the theorem that covers most cases:", font_size=28, color=GREY_A),
            label(r"in an exponential family whose natural parameters fill an open set,", font_size=28),
            label(r"$T = \sum_i T(x_i)$ is complete and minimal sufficient", font_size=30, color=ADMC),
            label(r"proof: \ $E_\eta g(T) = 0$ on an open set \ $\Rightarrow$ \ a Laplace transform vanishes \ $\Rightarrow g = 0$", font_size=26, color=S.ACCENT),
            label(r"curved families \ (fewer parameters than statistics) \ can fail it", font_size=26, color=MMC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Most of the families in this course are covered by one theorem. <bookmark mark='b'/> In an "
            "exponential family whose natural parameter ranges over a set with nonempty interior, <bookmark mark='c'/> the "
            "sum of the statistics T is both complete and minimal sufficient. <bookmark mark='d'/> The proof: if a function "
            "of T has mean zero on an open set of natural parameters, a two-sided Laplace transform vanishes on an open set, "
            "and by its uniqueness the function is zero. <bookmark mark='e'/> Curved families, with fewer free parameters "
            "than statistics, like the normal whose mean equals its standard deviation, can fail it."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
