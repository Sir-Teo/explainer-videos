from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, IV, OPT, PART, SPOT, load

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
        rows = [cmath(r"\hat\beta", r"=", r"\hat G^{-1}\hat m,\qquad \hat G = \tfrac1N\sum_n \psi(X_n)\psi(X_n)^{\top}",
                      font_size=32, colors={r"\hat\beta": OPT}),
                cmath(r"\operatorname{Var}\big(\hat G_{kk}\big)", r"=", r"\tfrac1N\Big(\mathbb E\,\psi_k^4 - \big(\mathbb E\,"
                      r"\psi_k^2\big)^2\Big)", font_size=32, colors={r"\operatorname{Var}\big(\hat G_{kk}\big)": BAD}),
                cmath(r"N", r"\gg", r"\max_{k \le K}\ \mathbb E\,\psi_k^4\quad(\psi_k\ \text{normalized})", font_size=32,
                      colors={r"N": BAD})]
        whys = [why(r"each date's least-squares fit: the sample Gram matrix of the basis, inverted against the sample "
                    r"cross-moments with the discounted future cash flows"),
                why(r"the Gram matrix's own sampling error is driven by the fourth moments of the basis functions"),
                why(r"so the fit is reliable only when the paths outnumber the largest fourth moment: Glasserman and Yu "
                    r"(2004) turn this into worst-case growth rates")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Paths versus basis functions", wrapped_label(
            r"for polynomial bases, the number of paths needed for the regression estimates to converge, in the worst "
            r"case, grows exponentially in the degree when the underlying is Brownian motion, and faster still for "
            r"geometric Brownian motion", 10.6, 20, GREY_A),
            who=r"Glasserman and Yu (2004), \textit{Annals of Applied Probability} 14", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "At each exercise date the method regresses. <bookmark mark='a'/> The coefficients are the inverse of the "
            "sample Gram matrix of the basis times the sample cross-moments. <bookmark mark='b'/> The Gram matrix is "
            "itself an average, and its error is driven by the fourth moments of the basis functions. "
            "<bookmark mark='c'/> So the regression is reliable only when the number of paths dwarfs the largest "
            "fourth moment in the basis. <bookmark mark='d'/> Paul Glasserman and Bin Yu turned this into worst-case "
            "rates in 2004: exponential growth in the degree for Brownian motion, faster for geometric Brownian motion."
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

    def moments(self, t):
        g = axes([0, 30], [0, 28], x_length=8.2, y_length=4.2, xlabel=r"degree $k$ of the basis function",
                 ylabel=r"$\log_{10}$ of its fourth moment, normalized", xticks=[0, 5, 10, 15, 20, 25, 30],
                 yticks=[0, 5, 10, 15, 20, 25], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        kb = np.asarray(t["k_bm"], float)
        bm = curve(ax, kb, np.log10(np.asarray(t["m4_bm"])), IV, stroke_width=3)
        kg = np.asarray(t["k_gbm"], float)
        gb = curve(ax, kg, np.log10(np.asarray(t["m4_gbm"])), BAD, stroke_width=3)
        ref = DashedLine(ax.c2p(0, 0), ax.c2p(30, 30 * np.log10(9)), color=GREY_B, stroke_width=1.5)
        leg = legend([(IV, r"Hermite $h_k$ of a Gaussian (Brownian motion)"), (BAD, r"$S^k$, normalized, $S$ lognormal "
                      r"at $\sigma\sqrt t = 0.2$"), (GREY_B, r"$9^k$")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        m = t["m4_bm"]
        side = wrapped_label(rf"exact, by Gauss--Hermite quadrature: $\mathbb E h_k^4$ = {m[3]:,.0f} at $k = 3$, "
                             rf"{m[6]:.1e} at 6, {m[12]:.1e} at 12; for the lognormal $\mathbb E S^{{4k}}/(\mathbb E S^{{2k}})^2 = "
                             r"e^{4\sigma^2tk^2}$, which bends upward on this scale", 3.3, 14, GREY_A).next_to(leg, DOWN,
                                                                                                  buff=0.3)
        fit_right(side)
        with self.voiceover(
            "How fast do those fourth moments grow? <bookmark mark='a'/> For orthonormal Hermite polynomials of a "
            "Gaussian, the natural basis when the state is a Brownian motion, they grow geometrically, roughly nine "
            "to the k: a straight line on this log scale. <bookmark mark='b'/> For powers of a lognormal price, the "
            "classic basis in Longstaff and Schwartz, the growth is like e to the k squared: the curve bends upward. "
            "A degree-twelve fit in the price needs about ten billion paths before its Gram matrix can be "
            "trusted, in the worst case."
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
        g = axes([0.5, 12.5], [4.30, 4.50], x_length=8.2, y_length=4.2, xlabel=r"degree of the polynomial basis in $S/K$",
                 ylabel=r"value of the fitted exercise rule on 100{,}000 fresh paths", xticks=[1, 3, 6, 9, 12],
                 yticks=[4.30, 4.35, 4.40, 4.45, 4.50], yfmt=lambda v: f"{v:.2f}", font_size=15).move_to(
            LEFT * 1.4 + DOWN * 0.2)
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
                             rf"bars: three seeds; the test set's own standard error is {L['test_se']:.3f}", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r500 = L["grid"]["500"]
        with self.voiceover(
            "Now the price. A Bermudan put, Longstaff and Schwartz's own example. Fit the exercise rule on N paths, "
            "then value it on a hundred thousand fresh ones: a lower bound, so every shortfall is the rule's fault. "
            f"<bookmark mark='a'/> With five hundred paths, the best degree is about four, at {r500[3]['mean']:.3f}; by "
            f"degree twelve the rule has lost {r500[3]['mean'] - r500[-1]['mean']:.2f}, two percent of the price. "
            "<bookmark mark='b'/> With two thousand, the loss from a rich basis is a cent. <bookmark mark='c'/> With "
            "ten and fifty thousand, every degree from three to twelve lands on the tree's value, within the test "
            "set's noise. The more paths, the richer the basis you can afford, exactly as the theory says; but the "
            "price is far more forgiving than the worst case."
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
        rows = [cmath(r"V - V^{\hat\tau}", r"=", r"\mathbb E\sum_t \big|C_t - h_t\big|\,\mathbf 1\{\text{wrong decision at } t\}",
                      font_size=30, colors={r"V - V^{\hat\tau}": BAD}),
                cmath(r"\big|C_t - h_t\big|", r"\le", r"\big|C_t - \hat C_t\big|\quad\text{when the decision is wrong}",
                      font_size=30, colors={r"\big|C_t - h_t\big|": OPT}),
                cmath(r"V - V^{\hat\tau}", r"\lesssim", r"\mathbb E\,\big|C - \hat C\big|^{2}\ \ \text{(near the boundary)}",
                      font_size=30, colors={r"V - V^{\hat\tau}": GOOD})]
        whys = [why(r"a rule that stops at the wrong time loses the gap between continuing ($C$) and exercising ($h$), "
                    r"summed over the dates where it errs (up to the effect on later dates)"),
                why(r"but it errs only where the estimated continuation value $\hat C$ is on the wrong side of $h$, so "
                    r"the gap there is smaller than the estimation error"),
                why(r"and wrong decisions happen only in a band around the boundary whose probability is itself of the "
                    r"order of the error: the price's error is second order in the regression's (Belomestny 2011's "
                    r"margin condition)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Why is the price so forgiving? <bookmark mark='a'/> A rule loses value only where it decides wrongly, "
            "and there it loses the gap between continuing and exercising. <bookmark mark='b'/> But it decides wrongly "
            "only where the estimated continuation value lies on the wrong side of the payoff, so that gap is smaller "
            "than the estimation error. <bookmark mark='c'/> And such dates sit in a thin band around the exercise "
            "boundary, whose probability is itself of the order of the error. The price's error is second order in the "
            "regression's. Denis Belomestny made this precise in 2011, with a margin condition on how the boundary "
            "is approached."
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
            desk_question(r"open: which basis in high dimension", r"for many assets, polynomial bases explode in size; "
                          r"networks (Part 17's deep stopping) and kernel bases scale better, but rates with realistic path "
                          r"budgets are not known", width=12.4, font_size=18),
            desk_question(r"open: the upper bound's cost", r"the dual bound of Chapter 9 needs nested simulation or a "
                          r"martingale basis; how its error trades off against paths and basis is understood only partly",
                          width=12.4, font_size=18),
            desk_question(r"open: Greeks of a regressed rule", r"differentiating through an estimated exercise boundary "
                          r"is unstable; consistent, low-variance Greeks for Bermudans are still an active topic",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With many assets, polynomial bases explode in size. Networks and "
            "kernels scale better, but rates for realistic path budgets are not known. <bookmark mark='b'/> The dual "
            "upper bound of Chapter 9 needs nested simulation or a martingale basis, and its own trade-off between "
            "paths and basis is understood only in part. <bookmark mark='c'/> And Greeks: differentiating through an "
            "estimated exercise boundary is unstable, and consistent low-variance Greeks for Bermudans are an active "
            "topic."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"if the continuation value is estimated with error of 2\%, roughly how large is the loss in the "
                       r"price of the exercise rule: 2\%, 0.2\%, or 0.04\%? Why?")
        with self.voiceover(
            "Pause and predict. If the continuation value is estimated with an error of two percent, roughly how large "
            "is the loss in the exercise rule's value: two percent, a fifth of a percent, or four hundredths? Why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
