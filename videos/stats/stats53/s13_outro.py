from __future__ import annotations

from videos.stats.stats53.common import *  # noqa: F403

PROBLEMS = [
    r"Prove Doob's theorem for a prior on finitely many $\theta$: \ show $\Pi(\theta_0 \mid X_{1:n}) \to 1$ by the LLN for log-likelihood ratios.",
    r"For $X_i \sim N(0, 1)$ and a Uniform$[1, 3]$ prior on the mean, \ show the posterior mean tends to 1.",
    r"In the sequence model, \ derive the posterior mean's risk $\sum (1 - w_k)^2\theta_k^2 + \sum w_k^2/n$, \ $w_k = n\lambda_k/(1 + n\lambda_k)$.",
    r"Show the Beta$(a + k, b + n - k)$ posterior's mean and variance match $\hat p$ and $\hat p(1 - \hat p)/n$ up to $O(1/n)$.",
    r"For $F \sim \mathrm{DP}(\alpha, G_0)$, \ show $E[F(A)] = G_0(A)$ \ and \ $\mathrm{Var}[F(A)] = G_0(A)(1 - G_0(A))/(\alpha + 1)$.",
    r"Show the tempered Gamma--Poisson posterior with $\eta = \mu/\sigma^2$ has variance $\approx \sigma^2/n$, \ the sandwich.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Diaconis--Freedman: \ a reasonable prior, \ wrong forever", BADC), (r"Doob: \ consistent, \ prior-almost surely", POSTC),
            (r"Schwartz: \ KL support plus tests", POSTC), (r"contraction rates; \ the contraction ball", POSTC),
            (r"Bernstein--von Mises", FREQC), (r"its failures, \ and BvM for functionals", BADC),
            (r"Dirichlet processes, \ Pólya trees", PRIORC), (r"Gaussian processes: \ RKHS, \ small balls", PRIORC),
            (r"adaptation by empirical Bayes", GOODC), (r"polished tails, \ on the Board", BALLC),
            (r"spike-and-slab, \ the horseshoe", PRIORC), (r"misspecification, \ tempered posteriors", BALLC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 53, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-three in twelve lines. Diaconis and Freedman's reasonable prior that is wrong "
            "forever. Doob's consistency, almost surely under the prior. Schwartz's two ingredients. Contraction rates, and "
            "the contraction ball. Bernstein–von Mises, its failures, and its rescue for functionals. <bookmark mark='b'/> "
            "Dirichlet processes and Pólya trees. Gaussian processes through their reproducing kernels and small balls. "
            "Adaptation by empirical Bayes. Polished tails on the Board. The spike-and-slab and the horseshoe. And "
            "misspecified models with tempered posteriors."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(53, r"when posteriors find the truth, \ how fast, \ and when credible sets cover",
                            r"a likelihood: \ a model for how data arise",
                            r"Part 54: \ learning theory, \ with no model at all, \ only a loss")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one asked when posteriors find the truth, how fast, and "
            "when credible sets can be trusted. <bookmark mark='b'/> All of it assumed a likelihood, a model of how the data "
            "arise. <bookmark mark='c'/> Part fifty-four drops the model: statistical learning theory asks why minimizing a "
            "loss on a sample generalizes at all, and ends with Gibbs posteriors in PAC-Bayes form."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"PAC-Bayes bounds for Gibbs posteriors", [54]), (r"credible sets after selection", [56]),
            (r"Bayesian anytime-valid inference: \ e-values and mixtures", [58]), (r"Bayesian causal inference with propensity priors", [62]),
            (r"Bayesian deep learning, \ and its calibration", [64]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-four bounds the risk of Gibbs posteriors by PAC-Bayes. Part "
            "fifty-six asks about credible sets after selection. Part fifty-eight builds anytime-valid tests from Bayesian "
            "mixtures. Part sixty-two returns to Bayesian causal inference with propensity-score priors. And Part sixty-four "
            "asks whether Bayesian deep learning is calibrated."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Doob for a finite parameter set; the "
            "boundary posterior; the sequence model's risk; the Beta posterior's moments; the Dirichlet process's moments; "
            "and the tempered posterior's variance. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Ghosal \& A. van der Vaart, \emph{Fundamentals of Nonparametric Bayesian Inference} (2017)",
             r"J. K. Ghosh \& R. V. Ramamoorthi, \emph{Bayesian Nonparametrics} (2003); \ E. Giné \& R. Nickl (2016), ch. 7",
             r"N. Hjort, \ C. Holmes, \ P. Müller \& S. Walker (eds.), \emph{Bayesian Nonparametrics} (2010)"],
            [r"J. Doob (1949); \ L. Schwartz (1965); \ D. Freedman (1963, 1999); \ P. Diaconis \& D. Freedman (1986); \ D. Cox (1993)",
             r"T. Ferguson (1973); \ A. Lo (1984); \ M. Lavine (1992); \ R. Neal (2000); \ S. Ghosal, \ J. Ghosh \& A. van der Vaart (2000)",
             r"A. van der Vaart \& H. van Zanten (2008); \ B. Knapik et al. (2011, 2016); \ B. Szabó et al. (2015); \ I. Castillo \& J. Rousseau (2015)",
             r"I. Castillo et al. (2015); \ S. van der Pas et al. (2014, 2017); \ B. Kleijn \& A. van der Vaart (2012); \ P. Grünwald \& T. van Ommen (2017)"])
        with self.voiceover(
            "The books this part follows: Ghosal and van der Vaart's Fundamentals of Nonparametric Bayesian Inference, Ghosh "
            "and Ramamoorthi, Giné and Nickl's seventh chapter, and Hjort, Holmes, Müller and Walker's collection; with the "
            "papers from Doob to Grünwald and van Ommen."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=53, current=None)
        nxt = VGroup(label(r"Part 54", font_size=30, color=GREY_B), label(r"Statistical Learning Theory", font_size=48),
                     label(r"why does fitting data generalize at all?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-three parts of sixty-five. <bookmark mark='a'/> A prior is an assumption, and in infinite dimensions "
            "assumptions do not wash out by themselves. The good news is that the conditions under which Bayesian methods "
            "estimate well are now precisely known, and they are mild. The harder news is that honest uncertainty, Bayesian "
            "or not, always rests on an assumption about the truth that the data cannot fully check. <bookmark mark='b'/> "
            "Next, Part fifty-four: statistical learning theory."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(53)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
