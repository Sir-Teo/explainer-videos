from __future__ import annotations

from videos.stats.stats15.common import *  # noqa: F403

PROBLEMS = [
    r"Uniform prior, \ 3 successes in 5 trials: \ the posterior, \ its mean, \ and $P(p > \tfrac12 \mid \text{data})$.",
    r"Show that a Gamma$(\alpha, \beta)$ prior and Poisson counts $y_1, \ldots, y_n$ give a Gamma$(\alpha + \sum y_i,\ \beta + n)$ posterior.",
    r"Prior $\mu \sim N(0, 1)$, \ one observation $x = 2$ with $\sigma = 1$: \ the posterior for $\mu$.",
    r"Show the Beta--binomial posterior mean is a weighted average of $a/(a + b)$ and $s/n$, \ and give the weights.",
    r"Derive Laplace's rule of succession, \ $(s + 1)/(n + 2)$.",
    r"9 heads in 10 tosses: \ the Bayes factor for $p \sim U(0, 1)$ against $p = \tfrac12$, \ and Jeffreys's verdict.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Bayes's table; \ Laplace's births", PRIOR), (r"posterior $\propto$ likelihood $\times$ prior", POST),
            (r"sequential = batch", POST), (r"conjugacy: \ beta, \ gamma, \ normal", S.ALT),
            (r"the prior as imaginary data", PRIOR), (r"mean, \ median, \ mode as decisions", OBS),
            (r"equal-tailed and HPD intervals", OBS), (r"the predictive distribution", LIKE),
            (r"priors: \ sensitivity, \ Jeffreys", S.ALT), (r"the normal model gives Student's $t$", FIT),
            (r"grids; \ Metropolis, \ steps and coordinates", POST), (r"coverage: \ calibrated over the prior", HIT),
            (r"Bayes factors; \ Lindley's warning", RES),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 15, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part fifteen in thirteen lines. <bookmark mark='a'/> Bayes's billiard table gave the first posterior, and Laplace "
            "used one to make the excess of boys a near certainty. The posterior is proportional to likelihood times prior, and "
            "updating step by step gives the same answer as updating at once. Conjugate priors make it bookkeeping, and the "
            "prior acts like imaginary data. The posterior's mean, median and mode answer different loss functions, and its "
            "intervals can be equal-tailed or highest-density. Predictions average over the posterior, so they're wider than "
            "plug-ins. Priors matter with little data, so check sensitivity; Jeffreys's prior is invariant. The normal model's "
            "reference posterior is Student's t. Grids compute any small posterior, and a Metropolis walk handles larger "
            "ones, if the steps and coordinates are right. Credible intervals are exactly calibrated on average over a true "
            "prior, but not at every fixed truth. And Bayes factors, unlike p-values, can favour the null."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=30.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the bootstrap: \ another way to get a distribution", [16]), (r"Bayesian computation in depth", [21, 27]),
            (r"shrinkage and hierarchical models", [25]), (r"the Bayesian workflow", [26]),
            (r"model choice", [28]), (r"Bernstein--von Mises; \ nonparametric Bayes", [53]),
            (r"decision theory and admissibility", [45]), (r"e-values and betting", [58]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 16's bootstrap gives a frequentist cousin of a posterior. Bayesian "
            "computation returns in Parts 21 and 27, with EM, Hamiltonian Monte Carlo and variational inference. Hierarchical "
            "models and shrinkage, the place Bayes shines brightest, come in Part 25, and the full Bayesian workflow in Part 26. "
            "Model choice is Part 28; the Bernstein–von Mises theorem and nonparametric Bayes, Part 53; decision theory, Part "
            "45; and betting and e-values, a different bridge between belief and evidence, Part 58."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> A small beta posterior; the gamma–Poisson "
            "update; one normal observation; the prior as imaginary data; Laplace's rule; and a Bayes factor for a coin. Pause "
            "here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Gelman, J. Carlin, H. Stern, D. Dunson, A. Vehtari \& D. Rubin, \emph{Bayesian Data Analysis} (3rd ed., 2013), chs.~1--3, 10--11",
             r"P. Hoff, \emph{A First Course in Bayesian Statistical Methods} (2009)",
             r"R. McElreath, \emph{Statistical Rethinking} (2nd ed., 2020); \ H. Jeffreys, \emph{Theory of Probability} (1939)",
             r"S. Stigler, \emph{The History of Statistics} (1986), ch.~3; \ S. McGrayne, \emph{The Theory That Would Not Die} (2011)"],
            [r"T. Bayes (1763); \ P.-S. Laplace (1774, 1778, 1814)",
             r"H. Jeffreys (1946); \ H. Raiffa \& R. Schlaifer (1961); \ D. Lindley (1957)",
             r"N. Metropolis et al.\ (1953); \ G. Roberts, A. Gelman \& W. Gilks (1997)",
             r"T. Sellke, M. Bayarri \& J. Berger (2001); \ S. Cook, A. Gelman \& D. Rubin (2006)"])
        with self.voiceover(
            "The books and papers this part follows: Gelman and colleagues' Bayesian Data Analysis, Hoff's first course, "
            "McElreath's Statistical Rethinking, Jeffreys, Stigler's history and McGrayne's popular one, with the papers from "
            "Bayes and Laplace to Sellke, Bayarri and Berger."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=15, current=None)
        nxt = VGroup(label(r"Part 16", font_size=30, color=GREY_B), label(r"Without Assumptions", font_size=48),
                     label(r"pulling yourself up by your bootstraps, \ and tests that need no model at all", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifteen parts of sixty-five, the fifth of Stage II. <bookmark mark='a'/> We can now say what to believe after "
            "seeing data, and compute it. <bookmark mark='b'/> But every method so far, Bayesian or not, has leaned on a model "
            "for the data: normal, binomial, Poisson. What if we assume nothing about the distribution at all? In 1979 Bradley "
            "Efron showed how to resample the data themselves, and ranks had long offered tests that need no model. Part 16: "
            "without assumptions."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(15)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
