from __future__ import annotations

from videos.stats.stats8.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $E\sum_i (x_i - \bar x)^2 = (n - 1)\sigma^2$ for any i.i.d.\ sample with variance $\sigma^2$.",
    r"For $n = 9$ normal observations with $\bar x = 50$ and $s = 6$, \ give 95\% intervals for $\mu$ and for $\sigma$.",
    r"Show that if $T \sim t_k$ then $T^2 \sim F_{1,k}$.",
    r"Normal data: \ find the $c$ minimizing $E\big(\tfrac1c\sum (x_i - \bar x)^2 - \sigma^2\big)^2$, \ and the minimum MSE.",
    r"Use the delta method to find the SE of $\bar y/\bar x$ when $(x_i, y_i)$ are i.i.d.\ pairs.",
    r"How large a simple random sample (without replacement) from $N = 2{,}000$ gives $\mathrm{SE}(\bar x) = \sigma/20$?",
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
            (r"Student's cards: \ $1.96$ covers 87\%", DATA),
            (r"sampling distributions; \ SE $= \sigma/\sqrt n$", SIM),
            (r"$n - 1$: \ a dimension", S.ACCENT),
            (r"Fisher's rotation: \ $\bar x \perp s^2$", S.PRIOR),
            (r"$\chi^2$ and Cochran", EXACT),
            (r"Student's $t$: \ a scale mixture", EXACT),
            (r"$F$: \ ratios of variances", S.POST),
            (r"MSE $=$ variance $+$ bias$^2$; \ $n + 1$", S.ACCENT),
            (r"plug-in and consistency", S.LIK),
            (r"ratios: \ Laplace's 28 million", DATA),
            (r"the finite-population correction", EXACT),
            (r"the Coverage Board's first rows", S.KEPT),
            (r"$t$ is robust; \ $F$ for variances is not", RESID),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 8, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part eight in thirteen lines. <bookmark mark='a'/> Gosset's shuffled cards showed that the textbook "
            "interval covers only eighty-seven percent with four observations. A statistic has a sampling distribution, "
            "and the standard error, sigma over root n, is its spread, estimated from one sample. The n minus one is a "
            "dimension: residuals live in a subspace. Fisher's rotation splits a normal sample into its mean and its "
            "deviations, independent of each other, and from it come chi-squared and Cochran's theorem, Student's t, a "
            "normal over an uncertain scale, and F, a ratio of variances. Mean squared error is variance plus squared "
            "bias, and among constant SS divisors for normal data the best is n plus one. Plug-in estimators are consistent under appropriate continuity and moment conditions. Laplace estimated France's "
            "population with a ratio, and the delta method gives its standard error; the finite-population correction "
            "handles samples from small lists. The Coverage Board has its first rows. And the t-test can be more robust in these examples, while "
            "the F-test for variances is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=26.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"sampling distributions, SEs", [9, 11, 16, 47]),
            (r"$t$, $\chi^2$, $F$; Cochran", [10, 12, 13, 23]),
            (r"bias--variance, shrinkage", [25, 29, 32]),
            (r"plug-in, consistency", [9, 16, 47, 48]),
            (r"ratio estimation, delta SEs", [14, 18, 22]),
            (r"finite populations", [18, 41]),
            (r"the Coverage Board", [10, 11, 12, 65]),
            (r"robustness", [16, 30, 60]),
        ], font_size=22)
        intro = label('Where these sampling distributions return', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Sampling distributions and standard errors underlie every "
            "estimator from Part 9 on, and the bootstrap of Part 16 computes them by simulation. The t, chi-squared "
            "and F distributions run the tests of Part 10 and the regressions and designed experiments of Parts 12 and "
            "13. The bias–variance trade-off becomes shrinkage, smoothing and the lasso. Ratio estimation and finite "
            "populations return in survey sampling, Part 18. And the Coverage Board grows with every part."
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
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The n minus one proved; two intervals "
            "from one sample; t squared as an F; the best divisor; the standard error of a ratio; and a sample size from "
            "a finite population. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Casella \& R. Berger, \emph{Statistical Inference} (2nd ed., 2002), ch.~5",
             r"J. Rice, \emph{Mathematical Statistics and Data Analysis} (3rd ed., 2007), chs.~6--8",
             r"W. G. Cochran, \emph{Sampling Techniques} (3rd ed., 1977); \ S. Stigler, \emph{The History of Statistics} (1986)",
             r"J. Fox, \emph{Student's $t$}: \ E. S. Pearson, \emph{`Student': A Statistical Biography} (1990)"],
            [r"Student (1908); \ W. R. Macdonell (1902); \ A. Cushny \& A. Peebles (1905)",
             r"R. A. Fisher (1915, 1925); \ F. R. Helmert (1876); \ W. G. Cochran (1934); \ G. Snedecor (1934)",
             r"P.-S. Laplace (1802, 1812); \ W. G. Cochran, ``Laplace's ratio estimator'' (1978)",
             r"R. C. Geary (1936); \ G. E. P. Box (1953); \ W. James \& C. Stein (1961)"])
        with self.voiceover(
            "The books and papers this part follows: Casella and Berger, Rice, Cochran on sampling, Stigler's history, "
            "and Egon Pearson's biography of Gosset, with the original papers from Student to Box."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=8, current=None)
        nxt = VGroup(label(r"Part 9", font_size=30, color=GREY_B), label(r"Estimation", font_size=48),
                     label(r"how many tanks did Germany build? \ how do we invent good estimators?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Eight parts of sixty-five. <bookmark mark='a'/> We know how statistics vary from sample to sample, and we "
            "have a board to hold methods to their promises. <bookmark mark='b'/> But where do good estimators come "
            "from? During the Second World War, Allied statisticians estimated German tank production from the serial "
            "numbers on captured tanks, and beat the intelligence services. Part 9: estimation."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(8)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
