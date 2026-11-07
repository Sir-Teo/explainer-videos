from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, IV, OPT, PART, SPOT, load, axes, data_range, pause_card, flat_camera

N_COL = {"500": BAD, "2000": QC.THETA, "10000": IV, "50000": GOOD}


class Research(VoiceoverScene):
    def construct(self):
        t = load("paths_basis")
        self.card()
        self.regression()
        self.moments(t)
        self.experiment(t)
        self.boundary()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Paths against basis functions", r"In Longstaff and Schwartz's method, how many paths does a "
                          r"richer basis need?", part=PART)
        with self.voiceover("For the researcher: Chapter 8 regressed continuation values on a few polynomials. A richer "
                            "basis approximates the true continuation value better, so why not use thirty? Because each "
                            "extra function costs paths, and the cost grows faster than you would guess. Here is why, "
                            "and how much it matters for the price."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def regression(self):
        rows = [cmath(r"\hat\beta", r"=", r"\hat G^{+}\hat m,\qquad \hat G = \tfrac1N\sum_n \psi(X_n)\psi(X_n)^{\top}",
                      font_size=32, colors={r"\hat\beta": OPT}),
                cmath(r"\operatorname{Var}\big(\hat G_{kk}\big)", r"=", r"\tfrac1N\Big(\mathbb E\,\psi_k^4 - \big(\mathbb E\,"
                      r"\psi_k^2\big)^2\Big)", font_size=32, colors={r"\operatorname{Var}\big(\hat G_{kk}\big)": BAD}),
                cmath(r"\operatorname{SD}(\hat G_{kk})", r"=", r"\sqrt{(\mathbb E\psi_k^4-1)/N}\quad(\mathbb E\psi_k^2=1)", font_size=32,
                      colors={r"\operatorname{SD}(\hat G_{kk})": BAD})]
        whys = [why(r"each date's least-squares fit: the sample Gram matrix of the basis, inverted against the sample "
                    r"cross-moments with the discounted future cash flows"),
                why(r"the Gram matrix's own sampling error is driven by the fourth moments of the basis functions"),
                why(r"a single-diagonal iid RMS diagnostic; full regression also depends on dimension, off-diagonals, cross-moments and Gram conditioning")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Paths versus basis functions", wrapped_label(
            r"for polynomial bases, the number of paths needed for the regression estimates to converge, in the worst "
            r"case, grows exponentially in the degree when the underlying is Brownian motion, and faster still for "
            r"geometric Brownian motion", 10.6, 20, GREY_A),
            who=r"Glasserman and Yu (2004), \textit{Annals of Applied Probability} 14", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "At a regression date, least squares uses a sample Gram matrix and cross-moments; a pseudoinverse handles possible rank deficiency. <bookmark mark='a'/> For independent identically distributed states with finite fourth moments, a Gram diagonal is a sample average of squared basis values. <bookmark mark='b'/> Its variance is the displayed fourth-moment expression. <bookmark mark='c'/> If a basis function has unit second moment, its diagonal standard deviation is the square root of fourth moment minus one divided by path count. This is one RMS diagnostic, not a necessary and sufficient path budget. Full regression also depends on dimension, off-diagonal errors, target cross-moments and the smallest Gram eigenvalues. <bookmark mark='d'/> Glasserman and Yu analyse particular worst-case polynomial settings, obtaining exponential path growth for Brownian motion and faster growth for geometric Brownian motion. Their result does not prescribe the required paths for every option or basis."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(VGroup(*list(self.mobjects))))
            thm.move_to(ORIGIN)
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def moments(self, t):
        yr = data_range(np.log10(t["m4_bm"]), np.log10(t["m4_gbm"]), [0, 30 * np.log10(9)])
        g = axes([0, 30], yr, x_length=6.8, y_length=4.2, xlabel=r"degree $k$ of the basis function",
                 ylabel=r"$\log_{10}$ of its fourth moment, normalized", xticks=[0, 5, 10, 15, 20, 25, 30],
                 yticks=[0, 5, 10, 15, 20, 25], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        kb = np.asarray(t["k_bm"], float)
        bm = curve(ax, kb, np.log10(np.asarray(t["m4_bm"])), IV, stroke_width=3)
        kg = np.asarray(t["k_gbm"], float)
        gb = curve(ax, kg, np.log10(np.asarray(t["m4_gbm"])), BAD, stroke_width=3)
        ref = DashedLine(ax.c2p(0, 0), ax.c2p(30, 30 * np.log10(9)), color=GREY_B, stroke_width=1.5)
        leg = legend([(IV, r"Gaussian Hermite basis"), (BAD, r"normalized lognormal monomials"), (GREY_B, r"$9^k$")], font_size=19).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        m = t["m4_bm"]
        side = wrapped_label(rf"floating-point Gauss--Hermite quadrature: $\mathbb E h_k^4$ = {m[3]:,.0f} at $k = 3$, "
                             rf"{m[6]:.1e} at 6, {m[12]:.1e} at 12; for the lognormal $\mathbb E S^{{4k}}/(\mathbb E S^{{2k}})^2 = "
                             r"e^{4\sigma^2tk^2}$, which bends upward on this scale", 4.5, 21, GREY_A).next_to(leg, DOWN,
                                                                                                  buff=0.3)
        fit_right(side)
        with self.voiceover(
            "These curves concern unconditional normalized basis moments, not the actual in-the-money design distribution at every exercise date. <bookmark mark='a'/> Gaussian Hermite fourth moments grow roughly as nine to the degree, with polynomial factors. Values here are floating-point quadrature results; polynomial quadrature identities in exact arithmetic do not make every stored number exact. <bookmark mark='b'/> Normalized lognormal monomials have fourth-moment ratio exponential in degree squared, as shown. A large degree-twelve moment warns about this particular diagonal statistic. It does not imply that a degree-twelve put requires ten billion paths, nor supply a price-error guarantee."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), Create(ref), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(bm), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(gb), FadeIn(leg[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def experiment(self, t):
        L = t["lsm"]
        yr = data_range([L["true"]], *[[r["min"], r["max"]] for rr in L["grid"].values() for r in rr])
        g = axes([0.5, 12.5], yr, x_length=6.8, y_length=4.2, xlabel=r"degree of the polynomial basis in $S/K$",
                 ylabel=r"policy estimate; shared 100{,}000 evaluation paths", xticks=[1, 3, 6, 9, 12],
                 yticks=[4.30, 4.35, 4.40, 4.45, 4.50], yfmt=lambda v: f"{v:.2f}", font_size=15).move_to(
            LEFT * 2.3 + DOWN * 0.2)
        ax = g.ax
        tru = DashedLine(ax.c2p(0.5, L["true"]), ax.c2p(12.5, L["true"]), color=WHITE, stroke_width=2)
        tl = label(rf"tree: {L['true']:.3f}", font_size=15, color=GREY_A).next_to(ax.c2p(12.5, L["true"]), UP, buff=0.06).shift(
            LEFT * 0.6)
        lines = VGroup()
        for N, col in N_COL.items():
            rows = L["grid"][N]
            d = np.array([r_["deg"] for r_ in rows], float)
            m = np.array([r_["mean"] for r_ in rows])
            lines.add(VGroup(curve(ax, d, m, col, stroke_width=3),
                             *[Line(ax.c2p(r_["deg"], r_["min"]), ax.c2p(r_["deg"], r_["max"]), color=col, stroke_width=2)
                               for r_ in rows]))
        leg = legend([(col, rf"{int(N):,} paths".replace(",", "{,}")) for N, col in N_COL.items()], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"Bermudan put: $S_0 = {L['S0']:g}$, $K = {L['K']:g}$, $\sigma = {100 * L['sigma']:g}\%$, "
                             rf"$r = {100 * L['r']:g}\%$, one year, {L['dates']} exercise dates; in-the-money regressions; "
                             rf"bars: three-seed min--max, not confidence intervals; one saved policy's evaluation s.e. is {L['test_se']:.3f}. "
                             r"Evaluation paths are reused across all fits and degrees.", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r500 = L["grid"]["500"]
        with self.voiceover(
            f"Here each fitted policy is evaluated on the same one hundred thousand paths, independent of fitting but repeatedly reused across training sizes, degrees and seeds. Its expectation is a lower bound; the finite estimate has Monte Carlo noise. Bars show three-seed minima and maxima, not confidence intervals. <bookmark mark='a'/> With five hundred training paths the displayed degree-four mean is {r500[3]['mean']:.3f}; degree twelve is lower by {r500[3]['mean'] - r500[-1]['mean']:.2f}. This is a finite observed comparison, not proof that four is optimal. <bookmark mark='b'/> The two-thousand-path curves also show sensitivity to basis richness. <bookmark mark='c'/> With more training paths several degrees move closer to the three-thousand-step tree reference. That tree is itself approximate, and one policy's evaluation standard error is not a universal noise level. Observed shortfalls mix policy quality, evaluation noise and reference error; they cannot all be attributed to the rule."
        ) as vo:
            self.play(FadeIn(g), Create(tru), FadeIn(tl), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(leg[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(leg[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), FadeIn(leg[2]), FadeIn(lines[3]), FadeIn(leg[3]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def boundary(self):
        rows = [cmath(r"Z_i=e^{-rt_i}h_i,\quad C_i=E_iY_{i+1}", r",\quad", r"\Delta_i=|C_i-Z_i|,\quad\|\hat C_i-C_i\|_\infty\le\delta", font_size=29),
                cmath(r"V_0-EZ_{\hat\tau}", r"\le", r"\sum_{i<N}E[\Delta_i\,\mathbf1_{\{0<\Delta_i\le\delta\}}]", font_size=32, colors={r"V_0-EZ_{\hat\tau}": OPT}),
                cmath(r"P(0<\Delta_i\le u)\le A_i u^\alpha", r"\Rightarrow", r"V_0-EZ_{\hat\tau}\le\Big(\sum_{i<N}A_i\Big)\delta^{1+\alpha}", font_size=30, colors={r"\Rightarrow": GOOD})]
        whys = [why(r"discounted rewards and the optimal Snell continuation; fixed fitted policy with a uniform error bound at every exercise date"),
                why(r"wrong decisions have gap at most $\delta$; the performance-loss identity includes policy occupancy, so dropping occupancy gives this upper bound"),
                why(r"a margin assumption controls probability near, but not exactly on, the boundary; $\alpha=1$ gives a quadratic bound with dimensional constants and horizon")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Use discounted rewards Z and the optimal Snell continuation C on a finite exercise grid. Assume a fixed fitted continuation is uniformly within delta at every date. This is a strong hypothesis, not something the preceding finite experiment certifies. <bookmark mark='a'/> The performance-loss identity weights errors by which states the policy actually visits; a naive equality summing all wrong decisions at all dates is incorrect. Dropping occupancy gives the displayed upper bound. <bookmark mark='b'/> A wrong decision can occur only where the positive exercise gap is at most delta. Zero-gap decisions incur no loss. <bookmark mark='c'/> If each date satisfies a margin bound with exponent alpha, price loss is at most the sum of margin constants times delta to one plus alpha. Alpha one gives a quadratic bound. The constants have units and depend on the problem and horizon, so a two-percent continuation error does not automatically imply a four-hundredths-percent price loss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"follow-up: basis design in high dimension", r"for many assets, polynomial bases explode in size; "
                          r"compare polynomial, signature, network and kernel features under fixed training and evaluation budgets; "
                          r"account for approximation, estimation and optimization error", width=12.4, font_size=23),
            desk_question(r"follow-up: the upper estimate's cost", r"the dual bound of Chapter 9 needs nested simulation or a "
                          r"martingale basis; separate outer sampling error, inner bias and martingale approximation in a fixed budget",
                          width=12.4, font_size=23),
            desk_question(r"follow-up: Greeks of a regressed rule", r"differentiating through an estimated exercise boundary "
                          r"needs boundary and differentiation assumptions; compare smoothing, likelihood-ratio and dual approaches",
                          width=12.4, font_size=23),
        ).arrange(DOWN, buff=0.22)
        self.play(FadeIn(cards[0], shift=UP * 0.2))
        with self.voiceover(
            "Three follow-up directions for this demonstration. <bookmark mark='a'/> Compare basis designs in high dimension with fixed training, tuning and independent evaluation budgets. Separate approximation, estimation and optimization effects rather than asserting that one family always scales better. <bookmark mark='b'/> Allocate dual-estimator work across outer paths, inner simulations and martingale approximation, reporting each uncertainty source. <bookmark mark='c'/> For Greeks of fitted stopping rules, study boundary effects and the assumptions behind smoothing, score and differentiation methods. These are useful extensions of the demonstration, not claims that the literature has no rates or consistent estimators."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"Under the same linear-margin assumptions and constants, halve the uniform continuation error $\delta$. What happens to the quadratic price-loss bound?", width=11.6, font_size=32).move_to(UP * 0.8)
        answer = wrapped_label(r"The bound becomes one quarter: $A(\delta/2)^2=A\delta^2/4$. This scales a conditional upper bound, not the realised loss or an automatic percentage of the option price.", 11.4, 28, GOOD).move_to(DOWN * 1.7)
        with self.voiceover(
            'Pause and predict. Under the same linear-margin assumptions, constants and horizon, halve the uniform continuation error delta. What happens to the quadratic upper bound on policy price loss? Distinguish the bound from the realised loss.'
        ):
            self.play(FadeIn(q))
        self.wait(3.0)
        self.play(FadeIn(answer))
        self.wait(6.0)
        self.clear_scene()
