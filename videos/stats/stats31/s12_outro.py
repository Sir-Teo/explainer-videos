from __future__ import annotations

from videos.stats.stats31.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $B = -\tfrac12 J D^{(2)} J$ equals $X_0 X_0^\top$ when $D$ holds the Euclidean distances between the rows of $X$.",
    r"Show that $\max_a t^2(a) = \tfrac{n_1 n_2}{n_1 + n_2} d^\top S^{-1} d$, \ $d = \bar x_1 - \bar x_2$, \ attained at $a \propto S^{-1} d$.",
    r"Prove Eckart--Young for the Frobenius norm: \ the best rank-$k$ approximation of $X_0$ truncates its SVD.",
    r"Show that the canonical correlations are invariant to invertible linear maps of $x$ and of $y$ separately.",
    r"Show that $\theta_{ij} = 0$ iff the coefficient of $x_j$ is zero in the regression of $x_i$ on all the others.",
    r"Show that $k$-means's objective never increases under Lloyd's two steps, \ and that it stops in finitely many.",
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
            (r"a map from road distances: \ Torgerson", MAPC), (r"Mahalanobis: \ distance in the data's own units", MAPC),
            (r"Wishart: \ the chi-squared of matrices", PCC), (r"Hotelling: \ the best combination's $t^2$", PCC),
            (r"MANOVA: \ four statistics, \ one eigenproblem", PCC), (r"PCA: \ the SVD; \ units matter", PCC),
            (r"factors: rotations within four factors preserve $\Sigma$", FAC), (r"CCA: \ age and income, \ $r = 0.82$", CCC),
            (r"LDA and QDA: \ 2\% of irises wrong", SP[2]), (r"clustering: this mixture BIC prefers two components", MAPC),
            (r"graphs: \ zeros of $\Sigma^{-1}$, \ the graphical lasso", MAPC), (r"$p/n$: \ $\chi^2$ fails, \ drop $S^{-1}$", RES),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 31, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-one in twelve lines. <bookmark mark='a'/> Classical scaling rebuilt a map from nothing but "
            "road distances, and identified entries whose residuals warrant source checking. Mahalanobis distance "
            "measures distance in the data's own units. The Wishart distribution is the chi-squared of covariance "
            "matrices. Hotelling's T squared is the largest t squared over all linear combinations, and MANOVA's four"
            " statistics summarize one eigenproblem. Principal components are the SVD of the data, and depend on its "
            "units. Orthogonal rotations within the same four-factor model preserve its covariance; a one-factor "
            "model is a different restriction. Canonical correlation linked age structure to income across fifty "
            "countries. Discriminant analysis misclassified two percent of the irises, and clustering, without "
            "labels, found two components preferred by this regularized mixture BIC, not two biological species. For "
            "a Gaussian population, zeros in its inverse covariance mean conditional independence, and the graphical "
            "lasso finds them. And when the number of variables grows with the sample, the chi-squared calibration "
            "fails and methods that avoid S inverse take over."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(31, r"the sample covariance estimates $\Sigma$; \ its top eigenvectors reveal structure",
                            r"$p$ fixed while $n$ grows",
                            r"Part 52: \ random-matrix laws, \ and the threshold below which a component is invisible")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part treated the sample covariance as a good estimate of "
            "the true one, and read structure from its top eigenvectors. <bookmark mark='b'/> That quietly assumed "
            "the number of variables stays fixed while the sample grows. <bookmark mark='c'/> Part 52 drops the "
            "assumption. With random-matrix theory it shows exactly where sample eigenvalues fall, and proves that a "
            "real component weaker than a sharp threshold is invisible to principal components, under the specified "
            "high-dimensional spiked-model asymptotics."
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
            (r"the graphical lasso's penalty: \ sparsity", [32]), (r"thousands of correlated tests", [33]),
            (r"Mahalanobis matching", [36]), (r"latent variables and measurement error", [41]),
            (r"Marchenko--Pastur; \ the spiked model", [52]), (r"sparse PCA's computational barrier", [50]),
            (r"proportional asymptotics", [59]), (r"robust covariance in high dimensions", [60]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 32 explains the graphical lasso's penalty, and sparsity in "
            "general. Part 33 tests thousands of correlated hypotheses. Part 36 matches treated and control units by "
            "Mahalanobis distance. Part 41 returns to latent variables, as measurement error. Part 52 proves the "
            "Marchenko–Pastur law and studies spiked covariance models, and Part 50 shows why sparse principal components "
            "may be computationally hard. Part 59 redoes classical tests when p and n grow together, and Part 60 makes "
            "covariance estimation robust in high dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Why double-centring recovers the Gram "
            "matrix; the union–intersection derivation of T squared; the Eckart–Young theorem; the invariance of canonical "
            "correlations; zeros of the precision matrix as zero regression coefficients; and why Lloyd's algorithm "
            "stops. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"T. W. Anderson, \emph{An Introduction to Multivariate Statistical Analysis} (3rd ed., 2003)",
             r"K. Mardia, J. Kent \& J. Bibby, \emph{Multivariate Analysis} (1979)",
             r"R. Muirhead, \emph{Aspects of Multivariate Statistical Theory} (1982); \ I. Jolliffe, \emph{Principal Component Analysis} (2002)",
             r"S. Lauritzen, \emph{Graphical Models} (1996); \ T. Hastie, R. Tibshirani \& J. Friedman, \emph{The Elements of Statistical Learning} (2009)"],
            [r"K. Pearson (1901); \ C. Spearman (1904); \ J. Wishart (1928); \ H. Hotelling (1931, 1933, 1936); \ M. Bartlett (1933)",
             r"P. C. Mahalanobis (1936); \ R. A. Fisher (1936); \ C. R. Rao (1948); \ S. N. Roy (1953); \ W. Torgerson (1952)",
             r"D. Lawley (1940); \ K. J\"oreskog (1967); \ H. Kaiser (1958); \ J. Horn (1965); \ S. Lloyd (1957/1982)",
             r"V. Marchenko \& L. Pastur (1967); \ A. Dempster (1972); \ Z. Bai \& H. Saranadasa (1996); \ J. Friedman, T. Hastie \& R. Tibshirani (2008)"])
        with self.voiceover(
            "The books this part follows: T. W. Anderson's classic text; Mardia, Kent and Bibby; Muirhead's distribution "
            "theory; Jolliffe on principal components; Lauritzen on graphical models; and The Elements of Statistical "
            "Learning; with the papers from Pearson to Friedman, Hastie and Tibshirani."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=31, current=None)
        nxt = VGroup(label(r"Part 32", font_size=30, color=GREY_B), label(r"Sparsity", font_size=48),
                     label(r"how can you solve for 1,000 unknowns from 100 equations?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-one parts of sixty-five. <bookmark mark='a'/> We can find structure in many correlated variables, and "
            "we know when the classical tools stop working. <bookmark mark='b'/> The graphical lasso set most of a matrix "
            "to zero, and that was what made it work. Part 32 asks how far that idea goes: how can you solve for a thousand "
            "unknowns from a hundred equations? Sparsity."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(31)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
