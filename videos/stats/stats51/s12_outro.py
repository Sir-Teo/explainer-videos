from __future__ import annotations

from videos.stats.stats51.common import *  # noqa: F403

PROBLEMS = [
    r"Show that a variable in $[a, b]$ with mean zero has $E e^{\lambda X} \le e^{\lambda^2(b-a)^2/8}$ \ (Hoeffding's lemma).",
    r"For $x$ uniform on $S^{n-1}$, \ show $E x_1^2 = 1/n$ \ and that $\sqrt n\, x_1 \to N(0, 1)$.",
    r"Prove Johnson--Lindenstrauss for one pair: \ $P(|\,\|Gu\|^2/k - 1| > \varepsilon) \le 2e^{-k\varepsilon^2/8}$, \ $\|u\| = 1$.",
    r"Show that $\|g\|$ and $\max_i g_i$ are 1-Lipschitz, \ and that $s_{\max}(A)$ is 1-Lipschitz in the entries of $A$.",
    r"For exchangeable $X_i = \sqrt{1-\rho}Z_i + \sqrt\rho W$, \ show $E\max_i X_i = \sqrt{1-\rho}\,E\max_i Z_i$.",
    r"Show the statistical dimension of an orthant in $\mathbb R^p$ is $p/2$, \ and of a $k$-dimensional subspace is $k$.",
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
            (r"Lévy: \ the sphere's equator", SPHC), (r"sub-Gaussian and sub-exponential tails", BNDC),
            (r"thin shells; \ Johnson--Lindenstrauss", GAUSSC), (r"Lipschitz functions concentrate", GAUSSC),
            (r"$\sqrt n \pm \sqrt p$; \ Marchenko--Pastur; \ a real spectrum", MATC), (r"matrix Bernstein", MATC),
            (r"Dudley, \ Sudakov, \ generic chaining", BNDC), (r"Slepian, \ Fernique, \ Gordon", GAUSSC),
            (r"widths; \ escape through the mesh", SPHC), (r"the statistical dimension", SPHC),
            (r"intervals from concentration, \ on the Board", GOODC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 51, \ in eleven lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-one in eleven lines. Lévy's equator. Sub-Gaussian and sub-exponential tails. "
            "Thin shells and the Johnson–Lindenstrauss lemma. The concentration of Lipschitz functions. Random matrices "
            "without asymptotics, Marchenko–Pastur, and a real covariance spectrum judged against it. Matrix Bernstein. "
            "<bookmark mark='b'/> Chaining by Dudley, Sudakov's lower bound and generic chaining. Gaussian comparison by "
            "Slepian, Fernique and Gordon. Widths and the escape through the mesh. The statistical dimension, which explains "
            "the phase transition of sparse recovery. And intervals from concentration on the Board."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(51, r"how random vectors, \ matrices and processes behave in high dimension",
                            r"no statistical model: \ only probability",
                            r"Part 52: \ estimation with $p \gg n$, \ where these are the proofs")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one described how random vectors, matrices and processes "
            "behave in high dimension. <bookmark mark='b'/> It fitted no models: it was probability, not yet statistics. "
            "<bookmark mark='c'/> Part fifty-two puts these tools to work on estimation with more parameters than "
            "observations, where they become the proofs of the lasso's rates, of covariance estimation and of matrix "
            "completion."
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
            (r"restricted eigenvalues of random designs; \ the lasso's rate", [52]), (r"sparse PCA and the spiked covariance", [52, 59]),
            (r"Rademacher complexity, \ contraction, \ uniform laws", [54]), (r"confidence sequences by Ville's inequality", [58]),
            (r"proportional asymptotics: \ Marchenko--Pastur at work", [59]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-two proves that random designs satisfy restricted eigenvalue "
            "conditions and derives the lasso's rate, and studies sparse PCA against the spiked covariance model, to which "
            "Part fifty-nine returns. Part fifty-four uses Rademacher complexity and contraction for learning theory. Part "
            "fifty-eight builds confidence sequences from Ville's inequality. And Part fifty-nine studies estimators when p "
            "and n grow together, where Marchenko–Pastur is the starting point."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Hoeffding's lemma; the sphere's coordinate; "
            "Johnson–Lindenstrauss for one pair; three Lipschitz functions; the exchangeable maximum; and two statistical "
            "dimensions. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. Vershynin, \emph{High-Dimensional Probability} (2018); \ M. Wainwright, \emph{High-Dimensional Statistics} (2019), ch. 2--6",
             r"S. Boucheron, \ G. Lugosi \& P. Massart, \emph{Concentration Inequalities} (2013); \ M. Ledoux, \emph{The Concentration of Measure Phenomenon} (2001)",
             r"J. Tropp, \emph{An Introduction to Matrix Concentration Inequalities} (2015); \ M. Talagrand, \emph{Upper and Lower Bounds for Stochastic Processes} (2021)"],
            [r"P. Lévy (1922, 1951); \ W. Hoeffding (1963); \ D. Slepian (1962); \ V. Sudakov (1969); \ R. Dudley (1967); \ X. Fernique (1975)",
             r"B. Tsirelson, \ I. Ibragimov \& V. Sudakov (1976); \ W. Johnson \& J. Lindenstrauss (1984); \ Y. Gordon (1985, 1988)",
             r"V. Marchenko \& L. Pastur (1967); \ M. Talagrand (1987, 1995); \ R. Ahlswede \& A. Winter (2002); \ J. Tropp (2012)",
             r"V. Chandrasekaran et al. (2012); \ D. Amelunxen, \ M. Lotz, \ M. McCoy \& J. Tropp (2014); \ A. Maurer \& M. Pontil (2009)"])
        with self.voiceover(
            "The books this part follows: Vershynin's High-Dimensional Probability, Wainwright's chapters two to six, "
            "Boucheron, Lugosi and Massart, Ledoux, Tropp's matrix concentration, and Talagrand; with the papers from Lévy to "
            "Amelunxen, Lotz, McCoy and Tropp."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=51, current=None)
        nxt = VGroup(label(r"Part 52", font_size=30, color=GREY_B), label(r"High-Dimensional Statistics", font_size=48),
                     label(r"can you estimate a thousand parameters from a hundred observations?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-one parts of sixty-five. <bookmark mark='a'/> In high dimensions, randomness becomes predictable. A random point sits on the equator, a random vector on a thin shell, a random matrix has expected extreme singular values bounded by root n minus root p and root n plus root p, with random deviations around those expectations, and the maximum of a million Gaussians is very nearly a fixed number. That predictability is what makes statistics with many parameters possible at all. <bookmark mark='b'/> Next, Part fifty-two: high-dimensional statistics."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(51)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
