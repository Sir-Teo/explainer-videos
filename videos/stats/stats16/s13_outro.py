from __future__ import annotations

from videos.stats.stats16.common import *  # noqa: F403

PROBLEMS = [
    r"Two groups $\{3, 5, 9\}$ and $\{1, 2, 4\}$: \ the exact permutation $p$-value for the difference in means, \ one-sided.",
    r"$n = 4$: \ list the null distribution of Wilcoxon's $W^+$, \ and find $P(W^+ \ge 9)$.",
    r"Show that $U = R - m(m+1)/2$ counts the pairs $(i, j)$ with $x_i > y_j$, \ where $R$ is the rank sum of the $x$'s.",
    r"Show that the jackknife bias correction of $\hat\sigma^2 = \frac1n\sum(x_i - \bar x)^2$ gives exactly $s^2$.",
    r"For $n$ distinct values, \ find $P^*(\text{a resample contains } x_1)$, \ and its limit.",
    r"Show that the percentile interval for $\max_i x_i$ from Uniform$(0, \theta)$ never contains $\theta$.",
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
            (r"Efron's question: \ the SE of $r$", BOOT), (r"permutation tests from exchangeability", NULLC),
            (r"the sign test; \ Fisher's sign flip", RANK), (r"Wilcoxon's signed rank; \ Hodges--Lehmann", RANK),
            (r"Mann--Whitney $U$ = the AUC", RANK), (r"Kruskal--Wallis, \ Friedman, \ Spearman, \ Kendall", RANK),
            (r"efficiency: \ $3/\pi$, \ never below 0.864", OBS), (r"the jackknife: \ bias, \ SE, \ influence", BOOT),
            (r"the bootstrap: \ two worlds", BOOT), (r"percentile, \ basic, \ $t$, \ BCa", BOOT),
            (r"the maximum: \ a spike of $1 - 1/e$", RES), (r"cross-validation and optimism", FIT),
            (r"kernel densities and the bandwidth", S.ALT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 16, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part sixteen in thirteen lines. <bookmark mark='a'/> Efron asked for the standard error of a correlation from "
            "fifteen law schools, without a model. Permutation tests give exact p-values whenever the null makes the data "
            "exchangeable. The sign test uses only signs, and Fisher's sign flip tested Darwin's maize exactly. Wilcoxon's "
            "signed rank needs only symmetry, and the Hodges–Lehmann estimate goes with it. Mann and Whitney's U counts pairs, "
            "and divided by their number it's the area under the ROC curve. Ranks extend to many groups, to blocks and to "
            "correlation. They cost four and a half percent at the normal, never more than fourteen, and can gain without "
            "limit. The jackknife estimates bias and standard error, and measures each point's influence, but fails for the "
            "median. The bootstrap mirrors the real world with the empirical distribution. Its intervals come in four kinds, "
            "and the Board found none of them reaches ninety-five percent for a mean of fifteen skewed incomes. For a maximum, "
            "it fails outright. Cross-validation measures prediction honestly, and kernel estimates draw a density without "
            "bins, if the bandwidth is right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=30.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"block bootstraps for dependent data", [17]), (r"cross-validation and model choice", [19]),
            (r"nonparametric regression; \ the curse of dimensionality", [29]),
            (r"robustness: \ influence functions; \ efficiency proved", [30]),
            (r"bootstrap theory: \ Edgeworth expansions, \ second-order accuracy", [47]),
            (r"permutation tests and multiple testing", [33]), (r"conformal prediction", [34, 57]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 17 resamples dependent data in blocks. Part 19 makes cross-"
            "validation the centre of model choice. Part 29 builds nonparametric regression from kernels and meets the curse "
            "of dimensionality. Part 30 proves the efficiency results and measures robustness with influence functions. Part 47 "
            "explains, with Edgeworth expansions, why the bootstrap-t and BCa are second-order accurate. Permutation methods "
            "return for multiple testing in Part 33, and exchangeability gives conformal prediction, intervals with guaranteed "
            "coverage and no model at all, in Parts 34 and 57."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> A small permutation test; Wilcoxon's "
            "distribution for four pairs; the rank sum as a pair count; the jackknife and Bessel's correction; the chance a "
            "resample contains a given point; and why the percentile interval misses the tank total. Pause here if you want to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. Efron \& R. Tibshirani, \emph{An Introduction to the Bootstrap} (1993)",
             r"A. Davison \& D. Hinkley, \emph{Bootstrap Methods and their Application} (1997)",
             r"E. Lehmann, \emph{Nonparametrics: Statistical Methods Based on Ranks} (1975; rev.\ 2006)",
             r"L. Wasserman, \emph{All of Nonparametric Statistics} (2006); \ B. Silverman, \emph{Density Estimation} (1986)"],
            [r"R. A. Fisher (1935); \ F. Wilcoxon (1945); \ H. Mann \& D. Whitney (1947); \ W. Kruskal \& W. A. Wallis (1952)",
             r"E. Pitman (1948); \ J. Hodges \& E. Lehmann (1956, 1963); \ M. Quenouille (1949); \ J. Tukey (1958)",
             r"B. Efron (1979, 1987); \ P. Bickel \& D. Freedman (1981); \ P. Hall (1988)",
             r"M. Stone (1974); \ S. Geisser (1975); \ M. Rosenblatt (1956); \ E. Parzen (1962)"])
        with self.voiceover(
            "The books and papers this part follows: Efron and Tibshirani's introduction to the bootstrap, Davison and Hinkley, "
            "Lehmann on ranks, Wasserman's all of nonparametric statistics and Silverman on density estimation, with the papers "
            "from Fisher and Wilcoxon to Efron, Hall and Parzen."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=16, current=None)
        nxt = VGroup(label(r"Part 17", font_size=30, color=GREY_B), label(r"Time Series", font_size=48),
                     label(r"when each observation remembers the last", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixteen parts of sixty-five, the sixth of Stage II. <bookmark mark='a'/> We can now test, estimate and draw "
            "intervals with very few assumptions. <bookmark mark='b'/> All but one: independence. Every method in this part "
            "shuffled or resampled observations as if each were a separate draw. In 1926 George Udny Yule found that marriages "
            "in the Church of England correlated nought point nine five with mortality, and asked why time series produce such "
            "nonsense. Part 17: time series."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(16)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
