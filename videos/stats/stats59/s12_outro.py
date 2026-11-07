from __future__ import annotations

from videos.stats.stats59.common import *  # noqa: F403

PROBLEMS = [
    r"Show that for Gaussian least squares $E\|\hat\beta - \beta\|^2 = \sigma^2 p/(n - p - 1)$, \ and find its limit.",
    r"Derive the Marchenko--Pastur equation $\kappa z m^2 - (1 - \kappa - z)m + 1 = 0$ by leaving one independent row contribution out.",
    r"From the ridge risk, \ show the optimal penalty is $\lambda_\star = \gamma\sigma^2/r^2$.",
    r"Derive the ridgeless risk for $\gamma > 1$: \ $r^2(1 - 1/\gamma) + \sigma^2/(\gamma - 1)$.",
    r"Solve Gordon's auxiliary problem for least squares and recover $\sigma^2\kappa/(1 - \kappa)$.",
    r"Show that AMP's fixed points with the soft threshold are lasso solutions at the calibrated $\lambda$.",
]


class Outro(LectureMixin, VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"$p/n = 0.2$: \ the logistic MLE inflated by half", CLASSC), (r"the LRT: \ $\kappa\sigma_\star^2/\lambda_\star$, \ not 1", CLASSC),
            (r"OLS: \ variance times $1/(1 - \kappa)$", SIMC), (r"Marchenko--Pastur and Stieltjes", RMTC),
            (r"free convolution, \ by Pastur's equation", RMTC), (r"ridge risk in closed form", PROPC),
            (r"double descent, \ derived", PROPC), (r"LAD loses to OLS at large $\kappa$", CLASSC),
            (r"AMP and its state evolution", AMPC), (r"Gordon: \ a matrix becomes two vectors", PROPC),
            (r"replicas, \ Bayes-AMP, \ hard phases", AMPC), (r"random features; \ corrections; \ open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 59, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "<bookmark mark='a'/> Part fifty-nine in twelve lines. In the stated Gaussian logistic example with "
            'signal variance five and dimension ratio one-fifth, the MLE has inflation factor about one point five, '
            "and the likelihood-ratio test needs a rescaling. Least squares' variance is inflated by one over one "
            'minus kappa. The Marchenko–Pastur law and Stieltjes transforms explain why, and free convolution adds '
            "matrices. Ridge's risk is in closed form. <bookmark mark='b'/> Double descent is derived, peak and "
            "all. Least absolute deviations loses to least squares when kappa is large. AMP's trajectory is "
            "predicted by state evolution, and Gordon's comparison turns a matrix into two vectors. Replicas give "
            'the Bayes-optimal error and its hard phases; random features give a first exact theory of wide '
            'networks; and the corrections make inference honest again.'
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(59, r"exact limiting formulas under specified sampling assumptions", r"the test data look like the training data",
                            r"Part 60: \ robustness and distribution shift")
        with self.voiceover(
            (
            "<bookmark mark='a'/> A promise for the next part. We studied exact limiting formulas under specified "
            "sampling models and numerical illustrations with finite-sample error. <bookmark mark='b'/> It assumed "
            "the test data look like the training data. <bookmark mark='c'/> Part sixty asks what can be guaranteed "
            'when the data are corrupted, or the future differs from the past.'
        )
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
            (r"robust estimation in high dimensions", [60]), (r"optimal transport's sample complexity", [61]),
            (r"high-dimensional causal adjustment", [62]), (r"the theory of large models", [64]),
            (r"the dissertation's simulation study", [65]),
        ], font_size=22)
        with self.voiceover(
            (
            "Where it comes back. <bookmark mark='a'/> Part sixty's robust estimation in high dimensions. Part "
            "sixty-one's sample complexity of optimal transport. Part sixty-two's high-dimensional causal "
            "adjustment. Part sixty-four's theory of large models. And the dissertation's simulation study."
        )
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            (
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Least squares' exact error; the "
            "Marchenko–Pastur equation; the optimal ridge penalty; the ridgeless risk; Gordon's auxiliary problem "
            "for least squares; and AMP's fixed points as lasso solutions. Pause here if you want to try them."
        )
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Z. Bai \& J. Silverstein, \ \emph{Spectral Analysis of Large Dimensional Random Matrices} (2010)",
             r"J. Mingo \& R. Speicher, \ \emph{Free Probability and Random Matrices} (2017)",
             r"M. M\'ezard \& A. Montanari, \ \emph{Information, Physics, and Computation} (2009)"],
            [r"P. Sur \& E. Cand\`es, \ \emph{PNAS} (2019); \ E. Cand\`es \& P. Sur, \ \emph{Ann. Stat.} (2020); \ V. Marchenko \& L. Pastur (1967)",
             r"E. Dobriban \& S. Wager, \ \emph{Ann. Stat.} (2018); \ T. Hastie, \ A. Montanari, \ S. Rosset \& R. Tibshirani, \ \emph{Ann. Stat.} (2022)",
             r"N. El Karoui et al., \ \emph{PNAS} (2013); \ D. Donoho \& A. Montanari, \ \emph{PTRF} (2016); \ D. Donoho, \ A. Maleki \& A. Montanari, \ \emph{PNAS} (2009)",
             r"M. Bayati \& A. Montanari (2011, 2012); \ C. Thrampoulidis et al. (2015); \ J. Barbier et al., \ \emph{PNAS} (2019); \ S. Mei \& A. Montanari (2022)"])
        with self.voiceover(
            (
            'The books behind this part: Bai and Silverstein on random matrices; Mingo and Speicher on free '
            'probability; and Mézard and Montanari on information, physics and computation; with the papers from '
            'Marchenko and Pastur to Sur and Candès.'
        )
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=59, current=None)
        nxt = VGroup(label(r"Part 60", font_size=30, color=GREY_B), label(r"Robustness and Distribution Shift", font_size=48),
                     label(r"what can be guaranteed when the data are corrupted, \ or the future differs from the past?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            (
            "Fifty-nine parts of sixty-five. <bookmark mark='a'/> In 2019 a team rebuilt the ImageNet test set, "
            'following the original recipe as closely as they could, and every model they tested lost accuracy on '
            "the new images: test sets are not the future. <bookmark mark='b'/> Next, Part sixty: robustness and "
            'distribution shift.'
        )
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(59)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
