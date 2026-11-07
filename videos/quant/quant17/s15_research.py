from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, load

N_COL = {"5": BAD, "10": QC.THETA, "20": IV, "40": GOOD}


class Research(VoiceoverScene):
    def construct(self):
        t = load("aposteriori")
        self.card()
        self.identity()
        self.theorem()
        self.curves(t)
        self.floors(t)
        self.nonlinear(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The deep BSDE's loss as an error certificate", r"Without knowing the answer, how do you know "
                          r"how wrong the network is?", part=PART)
        with self.voiceover("For the researcher: Chapters 8 and 9 trained a deep BSDE solver and checked its price "
                            "against a reference. In a hundred dimensions there usually is no reference. Here is the "
                            "theorem that turns the training loss itself into a bound on the error, and how tight that "
                            "bound turns out to be."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def identity(self):
        rows = [cmath(r"dY_t", r"=", r"RY_t\,dt + Z_t\cdot dW_t,\qquad Y_0 = y_0", font_size=32, colors={r"dY_t": NET}),
                cmath(r"g(X_T)", r"=", r"e^{RT}u_0 + \int_0^T e^{R(T - t)} Z^*_t\cdot dW_t", font_size=32,
                      colors={r"g(X_T)": REF}),
                cmath(r"\mathbb E\big|Y_T - g\big|^2", r"=", r"e^{2RT}(y_0 - u_0)^2 + \mathbb E\!\int_0^T e^{2R(T-t)}|Z_t - "
                      r"Z^*_t|^2 dt", font_size=28, colors={r"\mathbb E\big|Y_T - g\big|^2": BAD}),
                cmath(r"|y_0 - u_0|", r"\le", r"e^{-RT}\sqrt{\text{loss}}", font_size=34, colors={r"|y_0 - u_0|": GOOD})]
        whys = [why(r"the linear case of Chapter 8 (no default): the solver's process, driven by a trainable $y_0$ and "
                    r"networks for $Z$"),
                why(r"the true price $u_0$ and the true hedge $Z^*$, by the martingale representation of the discounted "
                    r"payoff"),
                why(r"subtract: the difference is $e^{RT}(y_0 - u_0)$ plus a stochastic integral of $Z - Z^*$, and the two "
                    r"are orthogonal (It\^o's isometry; the cross term has mean zero)"),
                why(r"so the training loss, the terminal mismatch, bounds the price error, with no reference needed. "
                    r"Everything else in the loss is the hedge's own error")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "Start with the linear case. <bookmark mark='a'/> The solver runs a process from a trainable starting "
            "value, with networks for the hedge Z. <bookmark mark='b'/> The true payoff has the same form, with the true "
            "price and the true hedge, by the martingale representation theorem. <bookmark mark='c'/> Subtract. The "
            "terminal mismatch is the price error, grown at the rate R, plus a stochastic integral of the hedge error, "
            "and by Itô's isometry the two are orthogonal. <bookmark mark='d'/> So the square root of the training "
            "loss, discounted, bounds the error in the price. No reference is needed. Everything else in the loss is "
            "the error of the learned hedge."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        thm = theorem_card(r"A posteriori error estimate for the deep BSDE method", VGroup(
            MathTex(r"\sup_t\mathbb E|Y_t - \hat Y_t|^2 + \mathbb E\!\int_0^T|Z_t - \hat Z_t|^2dt\ \le\ C\Big(h + \mathbb E"
                    r"\big|g(X^\pi_T) - \hat Y_T\big|^2\Big)", font_size=30),
            wrapped_label(r"for Lipschitz drivers and coefficients (and, with a smallness condition, for coupled "
                          r"forward--backward systems), with $h$ the time step: drive the loss to zero on a fine grid and "
                          r"the solution converges", 10.4, 20, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25),
            who=r"Han and Long (2020), \textit{Probability, Uncertainty and Quantitative Risk} 5", width=11.8,
            font_size=22).move_to(UP * 0.4)
        note_ = why(r"in the linear case the constant is $e^{-2RT}$ and the $h$-term is the time-discretization floor of "
                    r"the best step-function hedge, $O(h)$ for Lipschitz payoffs (Zhang 2004)").to_edge(DOWN, buff=0.5)
        if note_.width > 12.6:
            note_.scale_to_fit_width(12.6)
        with self.voiceover(
            "With a nonlinear driver, such as the default-risk discount of Chapter 8, the identity becomes an "
            "inequality. <bookmark mark='a'/> Jiequn Han and Jihao Long proved in 2020 that the error in the whole "
            "solution, price and hedge, is bounded by a constant times the time step plus the training loss. Drive "
            "the loss to zero on a fine grid, and the solution converges. <bookmark mark='b'/> In the linear case the "
            "constant is explicit, and the time-step term is the floor that even the best step-function hedge cannot "
            "beat."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def curves(self, t):
        g = axes([0, 3000], [-2.6, 1.4], x_length=8.2, y_length=4.2, xlabel=r"training iteration",
                 ylabel=r"$\log_{10}$: price error (solid), certified bound (dashed)", xticks=[0, 1000, 2000, 3000],
                 yticks=[-2, -1, 0, 1], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for N, col in N_COL.items():
            r = t["runs"][N]
            it = np.asarray(r["iter"], float)
            e = np.log10(np.clip(np.asarray(r["err"]), 10 ** -2.6, None))
            b = np.log10(np.asarray(r["bound"]))
            lines.add(VGroup(curve(ax, it, e, col, stroke_width=2.5),
                             DashedVMobject(curve(ax, it, b, col, stroke_width=2.5), num_dashes=40)))
        leg = legend([(c, rf"$N = {N}$ steps") for N, c in N_COL.items()], font_size=16).to_edge(RIGHT, buff=0.3).shift(
            UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"the basket-minimum of Chapter 8 in {t['d']} dimensions, no default; reference "
                             rf"{t['reference']:.3f} from 2 million paths (s.e. {t['reference_se']:.3f}); bound "
                             r"$e^{-RT}\sqrt{\text{loss}}$, the loss averaged over 500 iterations; the error never "
                             r"crosses it", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Test it in ten dimensions, where Monte Carlo gives the answer to a few thousandths. Train at four time "
            "steps. <bookmark mark='a'/> The solid lines are the true price errors; the dashed lines the bound computed "
            "from the loss alone. In every run, at every iteration, the error stays under its bound. "
            "<bookmark mark='b'/> But look at the gap at the end: the bound sits near three, while the error is a few "
            "hundredths or less. The certificate is valid, and loose by a factor of twenty to a thousand."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.3), FadeIn(leg), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Indicate(l_[1], color=WHITE) for l_ in lines])
        self.wait(0.4)
        self.clear_scene()

    def floors(self, t):
        hx = [-4.0, -1.6, 0.8, 3.2, 5.6]
        head = VGroup(label(r"time steps $N$", font_size=18, color=GREY_B), label(r"final loss", font_size=20, color=BAD),
                      label(r"bound", font_size=20, color=BAD), label(r"actual error", font_size=20, color=GOOD),
                      label(r"seconds", font_size=20))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(N, font_size=26),
                                                 MathTex(rf"{t['runs'][N]['floor']:.1f}", font_size=26),
                                                 MathTex(rf"{t['disc'] * np.sqrt(t['runs'][N]['floor']):.2f}", font_size=26),
                                                 MathTex(rf"{t['runs'][N]['final_err']:.3f}", font_size=26),
                                                 MathTex(rf"{t['runs'][N]['seconds']:.0f}", font_size=26))
                                          for N in N_COL]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.72 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"final loss: the mean of the last 1{,}000 iterations' batch losses; actual error: the mean "
                             r"distance of $y_0$ from the reference over the last 500. The loss is mostly the variance of the "
                             r"learned hedge's error, which the price does not need to be accurate", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Where does the loss go? <bookmark mark='a'/> With five time steps it settles near seventeen; with ten, "
            "twelve; with twenty and forty, about nine and a half. The floor falls with the step, then stops: the "
            "networks' own error in the hedge takes over. <bookmark mark='b'/> And the price is accurate long before "
            "the hedge is: the loss is mostly the variance of the hedging error, which the price does not depend on. "
            "That is why the bound is loose, and why a small loss is the more demanding requirement."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2], r_[4])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def nonlinear(self, t):
        n = t["nonlinear"]
        it = np.asarray(n["iter"], float)
        u = np.asarray(n["u0"])
        L = np.asarray(n["loss"])
        k = 10
        sm = np.convolve(L, np.ones(k), mode="full")[: len(L)] / np.minimum(np.arange(1, len(L) + 1), k)
        g = axes([0, it.max()], [54, 61], x_length=8.2, y_length=4.2, xlabel=r"training iteration",
                 ylabel=r"$u(0, x_0)$, 100 dimensions, with default risk", xticks=[0, 500, 1000, 1500, 2000],
                 yticks=[54, 56, 58, 60], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        ref = DashedLine(ax.c2p(0, n["reference"]), ax.c2p(it.max(), n["reference"]), color=REF, stroke_width=2)
        hi_, lo_ = np.clip(u + np.sqrt(sm), 54, 61), np.clip(u - np.sqrt(sm), 54, 61)
        pts = [ax.c2p(a_, b_) for a_, b_ in zip(it, hi_)] + [ax.c2p(a_, b_) for a_, b_ in zip(it[::-1], lo_[::-1])]
        band = Polygon(*pts, stroke_width=0, fill_color=NET, fill_opacity=0.18)
        line = curve(ax, it, u, NET, stroke_width=3)
        leg = legend([(NET, r"$y_0$ during training"), (REF, rf"published reference, {n['reference']:.1f}")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"Chapter 9's cached run (seed 1); shaded: $y_0 \pm \sqrt{\text{loss}}$, the loss averaged "
                             r"over 500 iterations. With a nonlinear driver the constant $C$ is not known, so the band is "
                             r"indicative, not a certificate", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "And the hundred-dimensional problem with default risk, from Chapter 9. <bookmark mark='a'/> The starting "
            "value converges to the published reference, fifty-seven point three. <bookmark mark='b'/> The shaded band "
            "is the starting value plus or minus the square root of the loss. With a nonlinear driver the theorem's "
            "constant is not explicit, so this is indicative, not a certificate; but it contains the reference "
            "throughout, and it narrows as training goes on."
        ) as vo:
            self.play(FadeIn(g), Create(ref), FadeIn(leg[1]), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(band))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: sharper certificates", r"the bound charges the whole hedging error to the price; "
                          r"splitting the loss into its price and hedge parts (by a control variate on the learned $Z$) "
                          r"would tighten it, but rigorous versions for nonlinear drivers are missing", width=12.4,
                          font_size=18),
            desk_question(r"open: the optimization gap", r"the theorem bounds the error by the loss actually reached; "
                          r"why stochastic gradient descent reaches small losses in a hundred dimensions is not "
                          r"understood", width=12.4, font_size=18),
            desk_question(r"open: certificates that regulators accept", r"model validation asks for error bounds; a "
                          r"posteriori estimates are a candidate, but their constants for real products are rarely "
                          r"computable", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The bound charges the whole hedging error to the price; "
            "splitting the loss into its two parts would tighten it, but rigorous versions for nonlinear drivers are "
            "missing. <bookmark mark='b'/> The theorem bounds the error by the loss actually reached; why stochastic "
            "gradient descent reaches small losses in a hundred dimensions is not understood. <bookmark mark='c'/> And "
            "model validation asks for error bounds; a posteriori estimates are a candidate, but their constants for "
            "real products are rarely computable."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a linear deep-BSDE run ends with loss 9 at $R = 2\%$, $T = 1$. What is the most the price can be "
                       r"off by? If the true hedge were used, what would the loss become?")
        with self.voiceover(
            "Pause and predict. A linear deep BSDE run ends with a loss of nine, at two percent over one year. What is "
            "the most the price can be off by? And if the true hedge were used, what would the loss become?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
