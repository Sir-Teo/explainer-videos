from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, CURV, FWD, GOOD, LEVEL, PART, SLOPE, ZERO, load

PC_COL = [LEVEL, SLOPE, CURV]


class Research(VoiceoverScene):
    def construct(self):
        t = load("oscillation_theory")
        self.card()
        self.theorem()
        self.markov(t)
        self.sims(t)
        self.treasury(t)
        self.forwards(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Why level, slope and curvature", r"Are the curve's three factors economics, or mathematics?",
                          part=PART)
        with self.voiceover('The first three fitted components explained most sample variance, with broad level, slope and bend patterns. A conditional matrix theorem helps explain sign ordering in some models. It does not prove that every bond market has these shapes or that economics is irrelevant.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        rows = [cmath(r"\Sigma_{ij}", r"=", r"\operatorname{Cov}\big(\Delta y(m_i), \Delta y(m_j)\big),\quad m_1 < m_2 < \dots",
                      font_size=30, colors={r"\Sigma_{ij}": ZERO}),
                cmath(r"\det \Sigma_{I, J}", r"\ge", r"0\quad\text{for all ordered index sets } I, J", font_size=30,
                      colors={r"\det \Sigma_{I, J}": GOOD}),
                cmath(r"v_k", r":", r"\text{exactly } k - 1 \text{ sign changes}", font_size=32, colors={r"v_k": CURV})]
        whys = [why(r"the covariance of daily yield changes, with the maturities in order"),
                why(r"oscillatory: all minors nonnegative, and some positive integer power has every minor strictly positive; entrywise positivity alone is insufficient"),
                why(r"distinct positive eigenvalues; the $k$-th eigenvector has $k-1$ sign changes, ignoring zeros. This fixes sign counts, not flatness, monotonicity or variance shares")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The oscillation theorem", wrapped_label(
            r"an oscillation matrix has $n$ distinct positive eigenvalues, and the eigenvector of the $k$-th largest has "
            r"exactly $k - 1$ sign changes, ignoring zero coordinates. The hypothesis concerns every minor, not just entries", 10.6, 20, GREY_A),
            who=r"Gantmacher and Krein (1937, 1950); applied to the yield curve by Forzani and Tolmasky (2003) and Salinelli "
                r"and Sgarra (2006)", width=11.6, font_size=21).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Order the selected maturities. <bookmark mark='a'/> Form their symmetric covariance matrix. <bookmark mark='b'/> Assume every square minor from increasing row and column index sets is nonnegative, and some positive integer power has every such minor strictly positive. The power must be totally positive, not merely entrywise positive. This is the oscillatory condition. <bookmark mark='c'/> Its eigenvalues are distinct and positive, and eigenvector k in descending eigenvalue order has k minus one sign changes, ignoring zero coordinates. A positive first vector need not be flat, and one sign change does not imply monotonicity. <bookmark mark='d'/> The Gantmacher-Krein result constrains sign ordering under these assumptions. It gives neither three-factor variance concentration nor economic identification. Empirical covariance matrices need not satisfy it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def markov(self, t):
        m = t["markov"]
        V = np.asarray(m["vec"])
        x = np.arange(V.shape[1])
        g = axes([-0.3, 8.3], [-0.7, 0.7], x_length=8.0, y_length=4.0, xlabel=r"maturity, in order (9 points)",
                 ylabel=r"eigenvector loadings", xticks=[0, 4, 8], yticks=[-0.5, 0, 0.5], font_size=15).move_to(
            LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(-0.3, 0), ax.c2p(8.3, 0), color=GREY_C, stroke_width=1.2)
        cols = PC_COL + [BAD]
        lines = VGroup(*[VGroup(curve(ax, x, V[k], cols[k], stroke_width=3),
                                *[Dot(ax.c2p(a_, b_), radius=0.05, color=cols[k]) for a_, b_ in zip(x, V[k])])
                         for k in range(4)])
        leg = legend([(cols[k], rf"PC{k + 1}: {100 * m['share'][k]:.0f}\%, {m['changes'][k]} sign change"
                       + ("s" if m["changes"][k] != 1 else "")) for k in range(4)], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"the correlation $\rho^{{|i - j|}}$, $\rho={m['rho']}$: a nonsingular totally nonnegative Markov example. Some non-principal minors are zero", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "For zero less than rho less than one, the matrix with entries rho to the distance between indices is a stationary first-order autoregressive correlation. It is totally nonnegative and nonsingular, with positive adjacent off-diagonal entries, so it is oscillatory. It is not itself strictly totally positive: some minors vanish. <bookmark mark='a'/> At rho equal to zero-point-nine its first vector has no sign changes. <bookmark mark='b'/> The second has one. <bookmark mark='c'/> The third has two and the fourth three. These are ordered discrete modes, resembling string vibrations; their exact entries depend on rho and the boundary conditions."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[2]), Create(lines[3]), FadeIn(leg[3]))
        self.wait(0.4)
        self.clear_scene()

    def sims(self, t):
        s = t["sims"]
        M = t["M"]
        hx = [-3.6, -0.6, 1.4, 3.4, 5.4]
        head = VGroup(label(rf"{M:,} random matrices".replace(",", "{,}"), font_size=18, color=GREY_B),
                      label(r"0 changes", font_size=19), label(r"1", font_size=19), label(r"2", font_size=19),
                      label(r"3 or more", font_size=19))
        rows = []
        for kind, name in (("ordered", r"smooth kernel, ordered"), ("unordered", r"three factors, no order")):
            for k in range(3):
                rows.append(VGroup(label(rf"{name}: PC{k + 1}", font_size=18, color=PC_COL[k]),
                                   *[MathTex(rf"{100 * c / M:.0f}\%", font_size=24, color=GOOD if (c == M) else WHITE)
                                     for c in s[kind][k]]))
        tab = VGroup()
        for j, row in enumerate([head] + rows):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.1 - 0.58 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.8, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(r"Ordered experiment: Gaussian kernel on 9 sorted random maturities, random length scale, plus $10^{-9}I$ numerical regularization. Unordered: normalized three-factor covariance plus diagonal noise; spectra are not matched",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "These are the saved synthetic experiments, not new market trials. <bookmark mark='a'/> In two thousand draws of a sorted-maturity Gaussian-kernel construction, the first three numerical eigenvectors had zero, one and two sign changes in every draw. The implementation adds ten to the minus nine times identity for numerical regularization; that perturbation is not a general total-positivity preservation theorem. <bookmark mark='b'/> The unordered experiment uses random three-factor covariances with diagonal noise, normalized to correlations. The corresponding sign counts are rare individually. The two designs do not match eigenvalue spectra or every other feature, so this is an illustration, not identification of ordering as the sole cause. Nearby-maturity correlation alone is weaker than the all-minors condition."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:7]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def treasury(self, t):
        tr = t["treasury"]
        mats = np.asarray(tr["mats"], float)
        V = np.asarray(tr["vec"])
        g = axes([0, 31], [-0.6, 0.9], x_length=7.8, y_length=4.0, xlabel=r"maturity, years",
                 ylabel=r"loadings, daily changes of zero yields", xticks=[1, 5, 10, 20, 30], yticks=[-0.5, 0, 0.5],
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(31, 0), color=GREY_C, stroke_width=1.2)
        lines = VGroup(*[VGroup(curve(ax, mats, V[k], PC_COL[k], stroke_width=3),
                                *[Dot(ax.c2p(a_, b_), radius=0.05, color=PC_COL[k]) for a_, b_ in zip(mats, V[k])])
                         for k in range(3)])
        stats = VGroup(MathTex(r"\text{sign changes, PC1--5}:\ " + ",\\ ".join(str(c) for c in tr["changes"]), font_size=24),
                       MathTex(rf"\text{{2}} \times \text{{2 minors positive}}:\ {100 * tr['tp2']:.0f}\%", font_size=24),
                       MathTex(rf"\text{{3}} \times \text{{3 minors positive}}:\ {100 * tr['tp3']:.0f}\%", font_size=24),
                       MathTex(rf"\text{{variance}}:\ {100 * tr['share'][0]:.1f},\ {100 * tr['share'][1]:.1f},\ "
                               rf"{100 * tr['share'][2]:.1f}\%", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stats.to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(stats)
        side = wrapped_label(rf"Gürkaynak, Sack and Wright's zero curve, {tr['n_days']:,} consecutive-observation changes, December 1985--2025; the "
                             r"correlation-minor diagnostics use positive diagonal rescaling of covariance. Negative minors violate total nonnegativity; observed sign counts are descriptive", 3.3, 14, GREY_A).next_to(
            stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"For these nine maturities, the displayed covariance eigenvectors use ten thousand five consecutive-observation changes. <bookmark mark='a'/> Their first three sign patterns look level-like, tilted and bent, while actual magnitudes differ. <bookmark mark='b'/> The saved first-five sign counts are zero, one, two, three and four under the code's relative zero tolerance. <bookmark mark='c'/> About {100 * tr['tp2']:.0f} percent of ordered two-by-two correlation minors and {100 * tr['tp3']:.0f} percent of three-by-three minors are positive. Positive diagonal normalization preserves each minor's sign, but not covariance eigenvectors. Some minors are negative, so total nonnegativity fails. Observing the sign pattern does not let us apply the theorem backwards, nor does a high fraction of positive minors certify that we are close enough for it to apply."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(stats[0]), FadeIn(stats[3]))
            vo.wait_until("c")
            self.play(FadeIn(stats[1]), FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def forwards(self, t):
        tr = t["treasury"]
        mats = np.asarray(tr["mats"], float)
        V = np.asarray(tr["fwd_vec"])
        g = axes([0, 31], [-1.0, 1.0], x_length=7.8, y_length=4.0, xlabel=r"end of the forward period, years",
                 ylabel=r"loadings, daily changes of forward rates", xticks=[1, 5, 10, 20, 30], yticks=[-1, -0.5, 0, 0.5],
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(31, 0), color=GREY_C, stroke_width=1.2)
        lines = VGroup(*[VGroup(curve(ax, mats, V[k], PC_COL[k], stroke_width=3),
                                *[Dot(ax.c2p(a_, b_), radius=0.05, color=PC_COL[k]) for a_, b_ in zip(mats, V[k])])
                         for k in range(3)])
        stats = VGroup(MathTex(r"\text{sign changes}:\ " + ",\\ ".join(str(c) for c in tr["fwd_changes"]), font_size=24),
                       MathTex(rf"\text{{2}} \times \text{{2 minors positive}}:\ {100 * tr['fwd_tp2']:.0f}\%", font_size=24),
                       MathTex(rf"\text{{variance}}:\ {100 * tr['fwd_share'][0]:.0f},\ {100 * tr['fwd_share'][1]:.0f},\ "
                               rf"{100 * tr['fwd_share'][2]:.0f}\%", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stats.to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(stats)
        side = wrapped_label(r"Same days; interval forwards between the nine maturity endpoints (unequal interval widths). Averaging changes covariance and variance weighting; it does not guarantee an oscillatory matrix", 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Continuously compounded zero yields average instantaneous forwards over maturity. Here the comparison uses interval forwards between the nine selected endpoints, with unequal interval widths. <bookmark mark='a'/> Its components have different loadings and volatility weights; the first-three sign counts remain zero, one and two. All loadings are shown. <bookmark mark='b'/> About {100 * tr['fwd_tp2']:.0f} percent of two-by-two minors are positive, and the first three covariance components explain {100 * sum(tr['fwd_share'][:3]):.0f} percent, compared with {100 * sum(tr['share'][:3]):.0f} for yields. These descriptive differences are consistent with averaging changing the statistical picture, as discussed by Lekkos. Averaging can smooth covariance, but without additional assumptions it does not turn every covariance into a totally nonnegative or oscillatory matrix."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(stats))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: which shapes are economic", r"Under its assumptions the theorem constrains signs. A research task is to identify which loading magnitudes or locations carry economic information", width=12.4, font_size=18),
            desk_question(r"open: total positivity under stress", r"Test rolling covariance, minor signs and hedge residuals across stress periods; distinguish sampling uncertainty and changing market structure from theorem violations", width=12.4, font_size=18),
            desk_question(r"open: factors for hedging and for forecasting", r"PCA reconstructs sample variance; return forecasting optimizes a different objective. Compare them using decision-time inputs, costs and untouched outcomes", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three research tasks follow, rather than claims that whole literatures are unresolved. <bookmark mark='a'/> Separate sign constraints from economic information in loading magnitudes and locations. <bookmark mark='b'/> Measure rolling covariance, minor signs and hedge errors under stress, with sampling uncertainty. A stress event does not by itself identify why a condition fails. <bookmark mark='c'/> Compare variance-reconstruction factors with return-forecasting factors. Their objectives differ, so they need not coincide. Predictive evidence requires decision-time inputs, costs, full search accounting and untouched outcomes, none of which the covariance illustration supplies."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"for the 3 by 3 correlation $\begin{pmatrix}1&\rho&\rho^2\\\rho&1&\rho\\\rho^2&\rho&1\end{pmatrix}$, "
                       r"find the eigenvectors and count their sign changes. Does the answer depend on $\rho \in (0, 1)$?")
        with self.voiceover(
            "Pause and predict. For a three-by-three correlation matrix with rho next to the diagonal and rho squared in "
            "the corners, find the eigenvectors and count their sign changes. Does the answer depend on rho?"
        ):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        ans = VGroup(
            MathTex(r"a_\pm=(-\rho\pm\sqrt{\rho^2+8})/2,\quad v_\pm=(1,a_\pm,1)", font_size=32),
            MathTex(r"\lambda_\pm=1+\rho^2/2\pm(\rho/2)\sqrt{\rho^2+8}", font_size=32),
            MathTex(r"v_2=(1,0,-1),\quad\lambda_2=1-\rho^2,\quad\lambda_+>\lambda_2>\lambda_->0", font_size=30),
            wrapped_label(r"For $0<\rho<1$: 0, 1, 2 sign changes (ignore the middle zero). Entries and eigenvalues vary with $\rho$; the ordering is unchanged. At the excluded endpoints, degeneracy or singularity changes the assumptions.", 11.6, 22, GREY_A),
        ).arrange(DOWN, buff=0.45)
        with self.voiceover("The antisymmetric vector is one, zero, minus one, with eigenvalue one minus rho squared. For symmetric vectors one, a, one, solve a squared plus rho a minus two equals zero. The positive-root vector is first and has no sign change; the antisymmetric vector is second with one; the negative-root vector is third with two. For rho strictly between zero and one the sign counts stay fixed, while entries and eigenvalues change. The endpoints are excluded."):
            self.play(FadeIn(ans))
        self.clear_scene()
