from __future__ import annotations

from videos.stats.stats52.common import *  # noqa: F403

PROBLEMS = [
    r"Derive the lasso's basic inequality, \ and show it forces $\|\Delta_{S^c}\|_1 \le 3\|\Delta_S\|_1$ when $\lambda \ge 2\|X^\top\varepsilon/n\|_\infty$.",
    r"For columns with $\|X_j\|^2 = n$, \ show $P(\|X^\top\varepsilon/n\|_\infty > \sigma\sqrt{2\log(2p/\delta)/n}) \le \delta$.",
    r"Show the nuclear norm is decomposable: \ $\|A + B\|_* = \|A\|_* + \|B\|_*$ if $A$ and $B$ have orthogonal row and column spaces.",
    r"For $\Sigma = \mathrm{diag}(1 + \delta, 1)$ and $E = \varepsilon(e_1e_2^\top + e_2e_1^\top)$, \ find the exact angle of $v_1$, \ and compare with Davis--Kahan.",
    r"Invert $\psi(\ell) = (1 + \ell)(1 + \gamma/\ell)$; \ show $\psi'(\ell) = 1 - \gamma/\ell^2$ \ and that $\psi$ is minimized at $\ell = \sqrt\gamma$.",
    r"Solve $\gamma z m^2 + (z + \gamma - 1)m + 1 = 0$ \ and recover the Marchenko--Pastur density by Stieltjes inversion.",
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
            (r"noise with structure: \ PCA on nothing", BULKC), (r"the lasso's oracle inequality", LASSOC),
            (r"support recovery; \ $2s\log p$", LASSOC), (r"decomposable regularizers", BNDC2),
            (r"matrix completion", BULKC), (r"banding, \ thresholding, \ shrinkage", BULKC),
            (r"Davis--Kahan", BNDC2), (r"Stieltjes; \ MP; \ the semicircle", TRUEC), (r"spikes and BBP; \ Harman's tests", SPIKEC),
            (r"Tracy--Widom; \ Roy's test", SPIKEC), (r"sparse PCA; \ graphs", LASSOC), (r"the debiased lasso", GOODC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 52, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-two in twelve lines. Principal components on pure noise. The lasso's oracle "
            "inequality under restricted eigenvalues. Support recovery and its threshold. Decomposable regularizers, one "
            "theorem for many problems. Matrix completion. Banding, thresholding and shrinkage for covariances. <bookmark "
            "mark='b'/> Davis and Kahan's sin theta theorem. The Stieltjes transform, Marchenko–Pastur and the semicircle. "
            "Spikes and the BBP transition, on Harman's tests. Tracy–Widom and Roy's test. Sparse PCA and graphical models. "
            "And the debiased lasso."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(52, r"rates and limits for estimators with $p \gg n$",
                            r"frequentist estimators, \ a fixed truth",
                            r"Part 53: \ do Bayesian posteriors contract at the same rates?")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one found the rates and limits of estimators when "
            "parameters outnumber observations. <bookmark mark='b'/> They were frequentist estimators of a fixed truth. "
            "<bookmark mark='c'/> Part fifty-three asks whether Bayesian posteriors, with priors like the horseshoe and the "
            "spike and slab, contract around the truth at the same rates, and when their credible sets can be trusted."
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
            (r"posterior contraction for sparse priors", [53]), (r"high-dimensional learning bounds", [54]),
            (r"selective inference after the lasso", [56]), (r"the lasso's exact risk when $p/n \to \delta$", [59]),
            (r"high-dimensional causal adjustment", [62]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-three proves posterior contraction for sparse priors. Part "
            "fifty-four gives learning bounds in high dimensions. Part fifty-six builds exact inference after selection, the "
            "other answer to chapter eleven's question. Part fifty-nine computes the lasso's exact risk when p and n grow "
            "together. And Part sixty-two adjusts for many confounders at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The basic inequality and the cone; the "
            "size of the noise's correlations; the nuclear norm's decomposability; Davis–Kahan in two dimensions; the BBP "
            "map; and the Marchenko–Pastur density from its quadratic. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. Wainwright, \emph{High-Dimensional Statistics} (2019); \ P. Bühlmann \& S. van de Geer, \emph{Statistics for High-Dimensional Data} (2011)",
             r"Z. Bai \& J. Silverstein, \emph{Spectral Analysis of Large Dimensional Random Matrices} (2010); \ R. Couillet \& Z. Liao, \emph{Random Matrix Methods for Machine Learning} (2022)",
             r"T. Hastie, \ R. Tibshirani \& M. Wainwright, \emph{Statistical Learning with Sparsity} (2015)"],
            [r"P. Bickel, \ Y. Ritov \& A. Tsybakov (2009); \ M. Wainwright (2009); \ P. Zhao \& B. Yu (2006); \ S. Negahban et al. (2012)",
             r"E. Candès \& B. Recht (2009); \ V. Koltchinskii, \ K. Lounici \& A. Tsybakov (2011); \ P. Bickel \& E. Levina (2008); \ O. Ledoit \& M. Wolf (2004)",
             r"C. Davis \& W. Kahan (1970); \ V. Marchenko \& L. Pastur (1967); \ J. Baik, \ G. Ben Arous \& S. Péché (2005); \ D. Paul (2007)",
             r"C. Tracy \& H. Widom (1994, 1996); \ I. Johnstone (2001); \ I. Johnstone \& A. Lu (2009); \ A. Javanmard \& A. Montanari (2014)"])
        with self.voiceover(
            "The books this part follows: Wainwright's High-Dimensional Statistics, Bühlmann and van de Geer, Bai and "
            "Silverstein on spectral analysis, Couillet and Liao, and Hastie, Tibshirani and Wainwright; with the papers from "
            "Marchenko and Pastur to Javanmard and Montanari."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=52, current=None)
        nxt = VGroup(label(r"Part 53", font_size=30, color=GREY_B), label(r"Bayesian Asymptotics and Nonparametric Bayes", font_size=44),
                     label(r"when does a posterior find the truth, \ and how fast?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-two parts of sixty-five. <bookmark mark='a'/> When parameters outnumber observations, nothing can be "
            "learned without structure, and with the right structure, sparsity, low rank, a few spikes, almost everything can, "
            "losing only a logarithm. But structure is an assumption, and the hook's lesson stands: before reading a signal "
            "into high-dimensional data, know exactly what noise alone would have shown. <bookmark mark='b'/> Next, Part "
            "fifty-three: Bayesian asymptotics and nonparametric Bayes."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(52)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
