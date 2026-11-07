from __future__ import annotations

from videos.stats.stats30.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the Wilcoxon test's Pitman efficacy is $12(\int f^2)^2$ and that $\mathrm{ARE}(W : t) = 3/\pi$ at the normal.",
    r"Show that $12\sigma^2(\int f^2)^2 \ge 108/125$ for every density with variance $\sigma^2$, \ with equality at the parabola.",
    r"Find the influence function of the $\alpha$-trimmed mean at a symmetric $F$, \ and its gross-error sensitivity.",
    r"Show that the Hodges--Lehmann estimator's asymptotic breakdown point is $1 - 1/\sqrt2$.",
    r"Verify that Huber's least favourable $f_0$ integrates to 1 iff $2\phi(k)/k - 2\Phi(-k) = \varepsilon/(1 - \varepsilon)$.",
    r"Prove the median-of-means bound: \ with $k = \lceil 8 \log(1/\delta) \rceil$ blocks, \ $|\hat\mu - \mu| \le 2\sigma\sqrt{2k/n}$ w.p. $\ge 1 - \delta$.",
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
            (r"Tukey: \ 1 error in 570 tips the scales", PATH), (r"Newcomb: \ robust, \ and still short of 33", RES),
            (r"Wilcoxon: \ $3/\pi$, \ never below 0.864", HLC), (r"Hodges--Lehmann: \ the median of Walsh averages", HLC),
            (r"influence functions: \ bounded or not", HUBC), (r"breakdown: \ $1/n$ to $1/2$", MEDC),
            (r"Huber: \ the minimax $\psi$", HUBC), (r"scale: \ MAD, \ $Q_n$", MEDC),
            (r"regression: \ LTS, \ MM on the stars", BIWC), (r"MCD: \ masking undone", HLC),
            (r"median of means: \ sub-Gaussian from a variance", MOMC), (r"the World: \ HL 40\% shorter, \ one-sided errors win", RES),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 30, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty in twelve lines. <bookmark mark='a'/> Tukey showed that one gross error in five hundred and "
            "seventy is enough to make the standard deviation lose to a cruder rival. Newcomb's light gave robust "
            "estimates that agreed with each other and still fell short of the truth. The Wilcoxon test is three over"
            " pi as efficient as t at the normal with a point eight six four lower local asymptotic bound under the "
            "stated regular location assumptions. Hodges and Lehmann turned it into an estimate, the median of the "
            "Walsh averages. Influence functions measure what one point can do, breakdown what a fraction can. "
            "Huber's clipped psi is the minimax M-estimator. Robust scale comes from the MAD and Qn. Least trimmed "
            "squares and MM regression ignore the giant stars. The minimum covariance determinant unmasks hidden "
            "outliers. With iid sampling and a confidence-dependent feasible block count, median of means yields "
            "sub-Gaussian deviation bounds from finite variance. And on the World, robust intervals have a small "
            "width cost when these data are clean and are forty percent shorter under the simulated symmetric errors,"
            " while one-sided errors defeat them all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(30, r"a fraction $\varepsilon$ of gross errors can be survived, \ in one dimension, \ by the median, \ Huber, \ MCD",
                            r"low dimension, \ and estimators that are cheap only there",
                            r"Part 60: \ Tukey depth, \ and efficient algorithms with optimal error in high dimensions")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part showed that a fraction of gross errors can be survived, by "
            "the median, by Huber's estimate, by the minimum covariance determinant. <bookmark mark='b'/> All in low "
            "dimension: the MCD's cost explodes as dimension grows. <bookmark mark='c'/> Part 60 brings Tukey's depth and the "
            "recent algorithms that estimate a mean robustly in high dimension, efficiently and with optimal error."
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
            (r"robust PCA and covariance", [31]), (r"robust selection; \ heavy-tailed lasso", [32]),
            (r"rank-based conformal prediction", [34]), (r"doubly robust estimation", [36]),
            (r"influence functions in semiparametrics", [49]), (r"concentration for heavy tails", [51]),
            (r"Bahadur--Savage: \ no uniform $t$-interval", [57]), (r"robustness in high dimensions", [60]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 31 makes principal components and covariance robust. Part 32 "
            "selects variables with heavy-tailed losses. Part 34 builds conformal prediction on ranks. Part 36's doubly "
            "robust estimators are robust in a different sense, to a wrong model. Part 49 makes influence functions the "
            "heart of semiparametric efficiency. Part 51 proves concentration for heavy tails. Part 57 shows no t-interval "
            "can be valid over all distributions. And Part 60 takes robustness to high dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The Wilcoxon efficacy and three over pi; "
            "the Hodges–Lehmann bound; the trimmed mean's influence function; Hodges–Lehmann's breakdown point; Huber's "
            "least favourable density; and the median-of-means bound. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"P. Huber \& E. Ronchetti, \emph{Robust Statistics} (2nd ed., 2009)",
             r"F. Hampel, E. Ronchetti, P. Rousseeuw \& W. Stahel, \emph{Robust Statistics: The Approach Based on Influence Functions} (1986)",
             r"R. Maronna, D. Martin, V. Yohai \& M. Salibián-Barrera, \emph{Robust Statistics: Theory and Methods} (2nd ed., 2019)",
             r"P. Rousseeuw \& A. Leroy, \emph{Robust Regression and Outlier Detection} (1987); \ E. Lehmann, \emph{Nonparametrics} (1975)"],
            [r"J. Tukey (1960); \ S. Stigler (1977); \ E. Pitman (1948); \ J. Hodges \& E. Lehmann (1956, 1963); \ H. Chernoff \& R. Savage (1958)",
             r"P. Huber (1964); \ F. Hampel (1971, 1974); \ D. Donoho \& P. Huber (1983); \ P. Rousseeuw \& C. Croux (1993)",
             r"P. Rousseeuw (1984); \ V. Yohai (1987); \ P. Rousseeuw \& K. Van Driessen (1999, 2006)",
             r"A. Nemirovski \& D. Yudin (1983); \ N. Alon, Y. Matias \& M. Szegedy (1996); \ O. Catoni (2012); \ G. Lugosi \& S. Mendelson (2019)"])
        with self.voiceover(
            "The books this part follows: Huber and Ronchetti; Hampel, Ronchetti, Rousseeuw and Stahel on influence "
            "functions; Maronna, Martin, Yohai and Salibián-Barrera; Rousseeuw and Leroy on robust regression; and "
            "Lehmann's Nonparametrics; with the papers from Tukey to Lugosi and Mendelson."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=30, current=None)
        nxt = VGroup(label(r"Part 31", font_size=30, color=GREY_B), label(r"Multivariate Analysis", font_size=48),
                     label(r"Wishart, \ Hotelling, \ principal components, \ and what happens when $p$ grows with $n$", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty parts of sixty-five. <bookmark mark='a'/> We can estimate when the model is only nearly right, and say "
            "what bad data can and cannot do. <bookmark mark='b'/> Chapter eight already showed that many variables make "
            "everything harder. Part 31 studies the geometry of many variables properly: the Wishart distribution, "
            "Hotelling's T squared, principal components, and the surprises that appear when the number of variables grows "
            "with the sample size. Multivariate analysis."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(30)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
