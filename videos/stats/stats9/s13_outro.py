from __future__ import annotations

from videos.stats.stats9.common import *  # noqa: F403

PROBLEMS = [
    r"Method of moments for the Beta$(\alpha, \beta)$: \ express $\hat\alpha, \hat\beta$ in terms of $\bar x$ and "
    r"$v = \tfrac1n\sum (x_i - \bar x)^2$.",
    r"Pareto: \ $p_\theta(x) = \theta x^{-\theta - 1}$ for $x \ge 1$. \ Find the MLE of $\theta$, \ the Fisher information, \ "
    r"and the MLE's approximate standard error.",
    r"For $X_1, \dots, X_n$ uniform on $(0, \theta)$: \ show $M = \max X_i$ is sufficient and complete, \ and find the UMVUE of $\theta$.",
    r"$X_i \sim N(\mu, 1)$: \ Rao--Blackwellize $\mathbf 1\{X_1 \le c\}$ given $\bar X$ \ to get the UMVUE of $P(X \le c) = \Phi(c - \mu)$.",
    r"$X_i \sim N(0, \sigma^2)$: \ find $I(\sigma)$ \ and the Cram\'er--Rao bound for unbiased estimators of $\sigma^2$; \ "
    r"is it attained?",
    r"Tanks: \ show $E\,m = \tfrac{k(N + 1)}{k + 1}$, \ so $m(1 + \tfrac1k) - 1$ is unbiased. \ (Hint: \ "
    r"$\sum_{j=k}^N j\binom{j-1}{k-1} = k\sum_{j=k}^N \binom{j}{k}$.)",
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
            (r"serial numbers beat the spies", DATA),
            (r"estimators: \ recipes with sampling distributions", SIM),
            (r"moments: \ match averages (Pearson)", MOM),
            (r"likelihood: \ make the data probable (Fisher)", LIK),
            (r"Newton, \ invariance, \ the boundary MLE", LIK),
            (r"consistency by KL; \ SE $= 1/\sqrt{J}$", S.ACCENT),
            (r"sufficiency and factorization", S.PRIOR),
            (r"Rao--Blackwell: \ conditioning never hurts", UMVUE),
            (r"completeness: \ the UMVUE, \ $m + $ the average gap", UMVUE),
            (r"Fisher information: \ the score's variance", LIK),
            (r"Cram\'er--Rao, \ and how the tanks beat it", EXACT),
            (r"efficiency is bought with assumptions", S.RESID),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=28, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.46),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.46)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 9, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part nine in twelve lines. <bookmark mark='a'/> Serial numbers on captured tanks beat the intelligence "
            "services. An estimator is a recipe, judged by its sampling distribution. The method of moments matches "
            "averages; maximum likelihood chooses the parameter that makes the data most probable, solved by calculus, "
            "or by Newton's method, or, at a boundary, by inspection, and it's invariant to reparametrization. It's "
            "consistent because the expected log-likelihood peaks at the truth, and its standard error comes from the "
            "curvature. Sufficiency says which part of the data matters, and factorization finds it. Rao–Blackwell "
            "improves any estimator by conditioning on it, and with completeness, the result is the best unbiased "
            "estimator: for the tanks, the maximum plus the average gap. Fisher information is the variance of the "
            "score, and the Cramér–Rao bound says no unbiased estimator beats one over n I, except in irregular "
            "problems like the tanks. And efficiency is bought with assumptions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=28.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"likelihood, MLE, information", [10, 14, 22, 24, 47]),
            (r"Newton, scoring, EM", [21, 24, 27]),
            (r"sufficiency, exponential families", [22, 45]),
            (r"Rao--Blackwell, conditioning", [18, 27, 45]),
            (r"UMVUE, completeness", [45]),
            (r"Cram\'er--Rao, efficiency", [45, 47, 49, 50]),
            (r"irregular rates, superefficiency", [47, 50]),
            (r"misspecification, robustness", [22, 30, 60]),
        ], font_size=22)
        intro = label('Where estimation theory returns', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Likelihood is the backbone of the rest of the course: the "
            "likelihood ratio test in Part 10, logistic and Poisson regression in Parts 14 and 24, and likelihood in "
            "depth in Part 22. Newton's method grows into Fisher scoring and the EM algorithm in Part 21. Sufficiency, "
            "completeness and the best unbiased estimators are proved in full generality in Part 45, with decision "
            "theory. And the Cramér–Rao bound becomes the theory of efficiency: asymptotic in Part 47, semiparametric "
            "in Part 49, and minimax in Part 50."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3),
                      run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Moments for the beta distribution; "
            "the Pareto's maximum likelihood estimate and its standard error; the best unbiased estimator for a "
            "uniform; a Rao–Blackwellized normal probability; the Cramér–Rao bound for a normal variance; and the "
            "unbiasedness of the tank estimator, with a hint. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Casella \& R. Berger, \emph{Statistical Inference} (2nd ed., 2002), chs.~6--7",
             r"E. Lehmann \& G. Casella, \emph{Theory of Point Estimation} (2nd ed., 1998), chs.~1--2",
             r"J. Rice, \emph{Mathematical Statistics and Data Analysis} (3rd ed., 2007), ch.~8; \ L. Wasserman, "
             r"\emph{All of Statistics} (2004), ch.~9",
             r"H. Cram\'er, \emph{Mathematical Methods of Statistics} (1946); \ S. Stigler, ``The epic story of maximum "
             r"likelihood'' (2007)"],
            [r"K. Pearson (1894); \ R. A. Fisher (1912, 1922); \ A. Wald (1949); \ J. Neyman \& E. Scott (1948)",
             r"C. R. Rao (1945); \ D. Blackwell (1947); \ E. Lehmann \& H. Scheff\'e (1950, 1955)",
             r"R. Ruggles \& H. Brodie, \emph{JASA} 42 (1947); \ L. Goodman, \emph{JASA} 47 (1952)",
             r"M. Fr\'echet (1943); \ S. Kullback \& R. Leibler (1951); \ L. Hansen (1982)"])
        with self.voiceover(
            "The books and papers this part follows: Casella and Berger, Lehmann and Casella's Theory of Point "
            "Estimation, Rice and Wasserman, Cramér's 1946 book and Stephen Stigler's history of maximum likelihood, "
            "with the original papers from Pearson and Fisher to Ruggles and Brodie, and Leo Goodman's 1952 analysis "
            "of serial-number estimation."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=9, current=None)
        nxt = VGroup(label(r"Part 10", font_size=30, color=GREY_B), label(r"Significance", font_size=48),
                     label(r"eighty-two years of more boys than girls; \ a lady who tastes milk-first tea", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Nine parts of sixty-five. <bookmark mark='a'/> We can now build estimators, grade them, improve them, and "
            "say how good any of them can be. <bookmark mark='b'/> But an estimate is not yet a decision. In 1710, John "
            "Arbuthnot noticed that more boys than girls had been baptized in London in each of eighty-two years in a "
            "row, and asked whether chance could explain it. Two centuries later, a lady at Rothamsted claimed she could "
            "taste whether the milk had been poured before the tea. When is a pattern too strong to be chance? Part 10: "
            "significance."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(9)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
