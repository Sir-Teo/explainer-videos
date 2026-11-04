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
        with self.voiceover("For the researcher: Chapter 10 found that three components explain almost every move of the "
                            "curve, and that they look like a level, a slope and a curvature. Every bond market in the "
                            "world shows the same shapes. Is that a fact about economies? Mostly, it is a theorem about "
                            "matrices."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        rows = [cmath(r"\Sigma_{ij}", r"=", r"\operatorname{Cov}\big(\Delta y(m_i), \Delta y(m_j)\big),\quad m_1 < m_2 < \dots",
                      font_size=30, colors={r"\Sigma_{ij}": ZERO}),
                cmath(r"\det \Sigma_{I, J}", r"\ge", r"0\quad\text{for all ordered index sets } I, J", font_size=30,
                      colors={r"\det \Sigma_{I, J}": GOOD}),
                cmath(r"v_k", r":", r"\text{exactly } k - 1 \text{ sign changes}", font_size=32, colors={r"v_k": CURV})]
        whys = [why(r"the covariance of daily yield changes, with the maturities in order"),
                why(r"totally nonnegative: every minor built from ordered rows and columns is nonnegative (and some power "
                    r"of the matrix strictly positive): an oscillation matrix"),
                why(r"then the eigenvalues are distinct and positive, and the eigenvector of the $k$-th largest changes "
                    r"sign $k - 1$ times: no sign change (a level), one (a slope), two (a curvature)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The oscillation theorem", wrapped_label(
            r"an oscillation matrix has $n$ distinct positive eigenvalues, and the eigenvector of the $k$-th largest has "
            r"exactly $k - 1$ sign changes; the continuous version holds for totally positive kernels", 10.6, 20, GREY_A),
            who=r"Gantmacher and Krein (1937, 1950); applied to the yield curve by Forzani and Tolmasky (2003) and Salinelli "
                r"and Sgarra (2006)", width=11.6, font_size=21).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Order the maturities. <bookmark mark='a'/> Take the covariance matrix of daily yield changes. "
            "<bookmark mark='b'/> Suppose every minor built from ordered rows and columns is nonnegative, and some "
            "power of the matrix strictly positive. That makes it an oscillation matrix. <bookmark mark='c'/> Then its "
            "eigenvector number k changes sign exactly k minus one times: none, a level; one, a slope; two, a "
            "curvature. <bookmark mark='d'/> This is Felix Gantmacher and Mark Krein's oscillation theorem, from the "
            "1930s, and it says nothing about central banks or term premia. Forzani and Tolmasky, and Salinelli and "
            "Sgarra, pointed it at the yield curve."
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
        side = wrapped_label(rf"the correlation $\rho^{{|i - j|}}$ with $\rho = {m['rho']}$: a Markov chain's, the "
                             r"simplest totally positive matrix; no economics in it at all", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The simplest example has no economics in it at all: a correlation that decays geometrically with the "
            "distance between maturities, the correlation of a Markov chain. <bookmark mark='a'/> Its first "
            "eigenvector is a level. <bookmark mark='b'/> The second, a slope. <bookmark mark='c'/> The third, a "
            "curvature, and the fourth has three sign changes. Discrete sinusoids, like the vibrations of a string."
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
        foot = wrapped_label(r"ordered: a Gaussian kernel $e^{-(m_i - m_j)^2/\ell^2}$, totally positive, on 9 random "
                             r"maturities with a random length scale $\ell$; no order: a random three-factor correlation "
                             r"matrix, with the same number of strong factors but no reason to respect the ordering",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Try it on random matrices. <bookmark mark='a'/> Two thousand smooth, ordered kernels, each with random "
            "maturities and a random length scale: every single one gives a level, a slope and a curvature. "
            "<bookmark mark='b'/> Two thousand random correlation matrices with three strong factors but no ordering: "
            "almost never. Three factors explaining most of the variance is not enough. The shapes come from the "
            "ordering: nearby maturities move together more than distant ones."
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
        side = wrapped_label(rf"Gürkaynak, Sack and Wright's zero curve, {tr['n_days']:,} daily changes, 1986--2025; the "
                             r"correlation matrix of nine maturities. The theorem's condition holds only approximately, "
                             r"and its conclusion holds exactly", 3.3, 14, GREY_A).next_to(
            stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Now the Treasury curve: forty years of daily changes in zero yields, at nine maturities. "
            "<bookmark mark='a'/> The level, the slope and the curvature, as in Chapter 10. <bookmark mark='b'/> The "
            "first five components change sign zero, one, two, three and four times. <bookmark mark='c'/> Is the "
            "matrix totally positive? Not quite: ninety-six percent of its two-by-two minors are positive, and three "
            "quarters of the three-by-three. The condition is sufficient, not necessary, and the curve's correlations, "
            "falling smoothly with the distance between maturities, are close enough to it for the conclusion to hold "
            "exactly."
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
        g = axes([0, 31], [-1.0, 0.7], x_length=7.8, y_length=4.0, xlabel=r"end of the forward period, years",
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
        side = wrapped_label(r"the same days, the forward rates between consecutive maturities. Yields are averages of "
                             r"forwards, and averaging is what smooths a covariance into an oscillation matrix "
                             r"(Lekkos 2000)", 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A test of the explanation. Yields are averages of forward rates, and averaging is what smooths a "
            "covariance. So look at forward rates themselves. <bookmark mark='a'/> The first component is still a "
            "level, and the sign changes still run zero, one, two. But the second is no slope: it is almost all the "
            "thirty-year forward. <bookmark mark='b'/> Only "
            f"{100 * tr['fwd_tp2']:.0f} percent of the two-by-two minors are positive, and the first three components "
            f"explain {100 * sum(tr['fwd_share'][:3]):.0f} percent, against "
            f"{100 * sum(tr['share'][:3]):.0f} for yields. Ilias Lekkos made this point in 2000: the smooth, "
            "concentrated three-factor picture owes much to averaging, not only to the economy."
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
            desk_question(r"open: which shapes are economic", r"the oscillation theorem fixes the sign pattern, not the "
                          r"magnitudes or the curvature's location; which features of the loadings carry information "
                          r"about policy and premia is unsettled", width=12.4, font_size=18),
            desk_question(r"open: total positivity under stress", r"in crises the curve twists in ways the ordering does "
                          r"not predict (March 2020, Chapter 17's gilts); when and why the correlation stops decaying with "
                          r"maturity distance is not well studied", width=12.4, font_size=18),
            desk_question(r"open: factors for hedging and for forecasting", r"principal components maximize explained "
                          r"variance today; the factors that best predict excess returns (Cochrane and Piazzesi's) are "
                          r"different, and reconciling the two is open", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The theorem fixes the sign pattern, not the magnitudes or where "
            "the curvature bends; which features of the loadings carry economic information is unsettled. "
            "<bookmark mark='b'/> In crises the curve twists in ways the ordering does not predict; when and why the "
            "correlation stops decaying with distance is not well studied. <bookmark mark='c'/> And principal "
            "components maximize the variance explained today, while the factors that best forecast bond returns, "
            "Cochrane and Piazzesi's, are different. Reconciling the two is open."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
        self.wait(0.5)
        self.clear_scene()
