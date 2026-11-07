from __future__ import annotations

from videos.stats.stats10.common import *  # noqa: F403

PROBLEMS = [
    r"The tea with 10 cups, five milk-first: \ what is $p$ if she gets four of the five right? \ What is the smallest possible $p$?",
    r"Show that if $T$ has a continuous distribution under $H_0$, \ then $p = 1 - F_0(T)$ is Uniform$(0,1)$.",
    r"$X \sim$ Poisson$(\lambda)$, \ one observation: \ find the most powerful test of $\lambda = 1$ against $\lambda = 3$ of size at most $0.05$, "
    r"\ and its power. \ (Randomize if you want size exactly $0.05$.)",
    r"Derive $W = -2\log\Lambda$ for $H_0: p = p_0$ from $x$ successes in $n$ trials, \ and evaluate it for Arbuthnot's 82 of 82 with $p_0 = \tfrac12$.",
    r"How many observations per group give 90\% power to detect $\delta = 0.4\sigma$ with a two-sided two-sample $z$-test at $\alpha = 0.05$?",
    r"Ten independent tests, all nulls true: \ find $P(\text{at least one } p < 0.05)$, \ and the Šidák level $1 - (1 - \alpha)^{1/m}$ "
    r"that makes it exactly $0.05$.",
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
            (r"Arbuthnot's coins; \ the lady's tea", DATA),
            (r"Fisher: \ a null, \ a statistic, \ a tail", NULLC),
            (r"exact tests from the randomization", OBS),
            (r"continuous-null $p$ is uniform; discrete $p$ is super-uniform", OBS),
            (r"two errors: \ size and power", ALTC),
            (r"the most powerful test: \ a knapsack", ALTC),
            (r"likelihood ratios and Wilks", S.LIK),
            (r"$z$, \ $t$, \ paired, \ Welch", SIM),
            (r"Pearson's $\chi^2$; \ Mendel too good", DATA),
            (r"power; \ types S and M", OBS),
            (r"peeking breaks the size", REJ),
            (r"$p \ne P(H_0 \mid \text{data})$", REJ),
            (r"many tests; \ Bonferroni", REJ),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=28, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 10, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part ten in thirteen lines. <bookmark mark='a'/> Arbuthnot's eighty-two years and the lady's eight cups "
            "share Fisher's logic: a null hypothesis, a statistic, and the probability of something at least as "
            "extreme. When the experimenter randomized, the null distribution is the randomization itself, and the test "
            "is exact. Under an exact continuous null distribution, a p-value is uniform; discrete p-values are generally super-uniform. Neyman and Pearson added a second error and "
            "turned testing into optimization: the most powerful test fills a knapsack by likelihood ratio, and the "
            "likelihood ratio, with Wilks' theorem, gives a test for almost anything. The everyday tests are estimates "
            "over standard errors, and Welch's test survives unequal variances where Student's doesn't. Pearson's "
            "chi-squared tests counts, and showed Mendel's to be almost too good. Power decides whether a study can find "
            "an effect, and low power exaggerates the effects it does find. Peeking breaks a test's size; a p-value is "
            "not the probability that the null is true; and many tests need correcting."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=26.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"tests and intervals by inversion", [11, 46]),
            (r"randomization inference", [13, 16, 35]),
            (r"likelihood ratio, Wald, score", [14, 22, 24]),
            (r"$\chi^2$ tests for tables", [14]),
            (r"power and design", [13, 35]),
            (r"sequential and anytime-valid tests", [35, 58]),
            (r"multiple testing, FDR", [33, 56]),
            (r"Bayes factors, posterior odds", [15, 26]),
        ], font_size=22)
        intro = label('Where testing theory returns', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Every test inverts into a confidence interval, which is Part 11. "
            "Randomization inference returns with experiments and permutation methods in Parts 13, 16 and 35. The "
            "likelihood trinity runs logistic and Poisson regression in Parts 14 and 24. Sequential testing comes back "
            "with clinical trials and anytime-valid inference in Parts 35 and 58; multiple testing and the false "
            "discovery rate in Part 33; and the Bayesian answer to the question p-values can't answer, how probable is "
            "the hypothesis, in Part 15."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> A ten-cup tea test; the uniform "
            "p-value proved; a most powerful test for a Poisson count; the likelihood ratio for a proportion, applied to "
            "Arbuthnot; a sample size for ninety percent power; and the family-wise error of ten tests, with Šidák's "
            "exact correction. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Casella \& R. Berger, \emph{Statistical Inference} (2nd ed., 2002), ch.~8",
             r"E. Lehmann \& J. Romano, \emph{Testing Statistical Hypotheses} (4th ed., 2022), chs.~1--3",
             r"R. A. Fisher, \emph{Statistical Methods for Research Workers} (1925); \ \emph{The Design of Experiments} (1935)",
             r"D. Salsburg, \emph{The Lady Tasting Tea} (2001); \ S. Stigler, \emph{The History of Statistics} (1986)"],
            [r"J. Arbuthnot (1710); \ K. Pearson (1900); \ J. Neyman \& E. Pearson (1928, 1933); \ S. Wilks (1938)",
             r"B. L. Welch (1947); \ A. Wald (1945); \ P. Armitage, C. McPherson \& B. Rowe (1969); \ R. A. Fisher (1936)",
             r"J. Cohen (1962); \ A. Gelman \& J. Carlin (2014); \ J. Ioannidis (2005); \ G. Cumming (2008)",
             r"R. Wasserstein \& N. Lazar (2016); \ C. Bennett et al.\ (2009); \ S. Greenland (2019)"])
        with self.voiceover(
            "The books and papers this part follows: Casella and Berger, Lehmann and Romano's Testing Statistical "
            "Hypotheses, Fisher's own two books, and David Salsburg's history, The Lady Tasting Tea, with the original "
            "papers from Arbuthnot to the American Statistical Association."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=10, current=None)
        nxt = VGroup(label(r"Part 11", font_size=30, color=GREY_B), label(r"Honest Intervals", font_size=48),
                     label(r"what does ``95\% confident'' promise, \ and which intervals keep it?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Ten parts of sixty-five. <bookmark mark='a'/> We can ask whether a pattern is too strong to be chance, and "
            "we know the many ways the answer can mislead. <bookmark mark='b'/> But a test says yes or no. How big is "
            "the effect, and how sure are we of its size? The interval taught in every textbook for a proportion "
            "fails, in a sawtooth pattern, even with large samples. Part 11: honest intervals."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(10)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
