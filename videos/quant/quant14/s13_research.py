from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, SPOT, VAR, load

S_COL = {"riemann": BAD, "hybrid1": ROUGH, "hybrid2": RV}
S_NAME = {"riemann": r"step kernel (Riemann sum)", "hybrid1": r"hybrid, $\kappa = 1$", "hybrid2": r"hybrid, $\kappa = 2$"}


class Research(VoiceoverScene):
    def construct(self):
        t = load("convergence_theory")
        self.card()
        self.strong()
        self.hybrid()
        self.rate_plot(t)
        self.mc(t)
        self.weak(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How fast a rough simulation converges", r"Why does refining the grid barely help, and what "
                          r"does help?", part=PART)
        with self.voiceover("For the researcher: Chapter 6 introduced the hybrid scheme as the right way to simulate a "
                            "rough path. Here is the theorem behind it: the error of any step-function kernel falls like "
                            "n to the minus H, which for H of a tenth is almost not at all, and the hybrid scheme cannot "
                            "change that rate. What it changes, and why the price may still converge, is the story."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def strong(self):
        rows = [cmath(r"Y_1", r"=", r"\sqrt{2H}\int_0^1 (1 - s)^{a}\,dW_s,\quad a = H - \tfrac12", font_size=32,
                      colors={r"Y_1": ROUGH}),
                cmath(r"\hat Y_1", r"=", r"\sqrt{2H}\sum_{j = 1}^{n} (c_j\Delta)^{a}\,\Delta W_{(j)}", font_size=32,
                      colors={r"\hat Y_1": BAD}),
                cmath(r"\mathbb E\big|Y_1 - \hat Y_1\big|^2", r"=", r"2H\,\Delta^{2H}\sum_{j=1}^{n}\int_{j-1}^{j}\big(x^{a} - "
                      r"c_j^{a}\big)^2 dx", font_size=30, colors={r"\mathbb E\big|Y_1 - \hat Y_1\big|^2": BAD}),
                cmath(r"\operatorname{RMSE}", r"\sim", r"\sqrt{C}\;n^{-H}", font_size=34, colors={r"\operatorname{RMSE}": BAD})]
        whys = [why(r"the Riemann--Liouville process of Chapter 5, at $t = 1$; the kernel is infinite at $s = 1$"),
                why(r"any step-function approximation: on the cell at lag $j$ the kernel is frozen at $c_j\Delta$ (the left "
                    r"end, $c_j = j$, is the naive choice)"),
                why(r"It\^o's isometry, and the substitution $1 - s = x\Delta$: the whole error is $\Delta^{2H}$ times a sum "
                    r"that converges, because the terms fall like $j^{2a - 2}$"),
                why(r"so the strong rate is $n^{-H}$ for every choice of the points: at $H = 0.1$, halving the error needs "
                    r"$2^{10} \approx 1{,}000$ times the steps")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "Take the rough driver at time one. <bookmark mark='a'/> Its kernel is infinite at the end of the "
            "integral. <bookmark mark='b'/> Any step-function scheme freezes the kernel on each cell, at some point c "
            "j times delta; the naive choice is the cell's end. <bookmark mark='c'/> By Itô's isometry the squared "
            "error is a deterministic integral, and substituting one minus s equals x delta pulls out delta to the two "
            "H, times a sum that converges. <bookmark mark='d'/> So the error falls like n to the minus H, whatever "
            "points you choose. At H of a tenth, halving the error takes a thousand times as many steps."
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

    def hybrid(self):
        rows = [cmath(r"\hat Y_1^{(\kappa)}", r"=", r"\sqrt{2H}\Big[\sum_{j \le \kappa}\int_{\text{cell } j}(1 - s)^{a}dW_s "
                      r"+ \sum_{j > \kappa}(b_j\Delta)^{a}\Delta W_{(j)}\Big]", font_size=28,
                      colors={r"\hat Y_1^{(\kappa)}": ROUGH}),
                cmath(r"b_j", r"=", r"\Big(\frac{j^{a+1} - (j-1)^{a+1}}{a + 1}\Big)^{1/a}", font_size=30, colors={r"b_j": ROUGH}),
                cmath(r"\mathbb E\big|Y_1 - \hat Y_1^{(\kappa)}\big|^2", r"=", r"2H\,\Delta^{2H}\sum_{j > \kappa}\int_{j-1}^{j}"
                      r"\big(x^{a} - b_j^{a}\big)^2 dx", font_size=28, colors={r"\mathbb E\big|Y_1 - \hat Y_1^{(\kappa)}\big|^2": ROUGH})]
        whys = [why(r"simulate the first $\kappa$ cells' Wiener integrals exactly, jointly Gaussian with the increments, "
                    r"and step the rest"),
                why(r"the points that minimize each remaining cell's error (Chapter 6's optimal points)"),
                why(r"the sum now starts after the singularity: the rate is still $n^{-H}$, but the constant collapses, "
                    r"because almost all of it sat in the first cell")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The hybrid scheme's error", wrapped_label(
            r"the mean squared error of the hybrid scheme is asymptotically $J(H, \kappa, b)\,n^{-2H}$, with an explicit "
            r"constant; for rough kernels, moving from the Riemann sum to $\kappa = 1$ cuts the root mean squared error by "
            r"nearly 100\%", 10.6, 20, GREY_A),
            who=r"Bennedsen, Lunde and Pakkanen (2017), \textit{Finance and Stochastics} 21", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The hybrid scheme attacks the constant. <bookmark mark='a'/> Simulate the first kappa cells' integrals "
            "exactly, as Gaussians jointly drawn with the increments, and step the rest. <bookmark mark='b'/> Use the "
            "optimal evaluation points of Chapter 6. <bookmark mark='c'/> The error is the same sum, but it now starts "
            "after the singularity. The rate is still n to the minus H. The constant collapses, because almost all of "
            "it sat in the first cell. <bookmark mark='d'/> Mikkel Bennedsen, Asger Lunde and Mikko Pakkanen gave the "
            "exact asymptotic constant in 2017."
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

    def rate_plot(self, t):
        ns = np.asarray(t["n"], float)
        e = t["exact"]["0.1"]
        g = axes([0.8, 3.1], [-2.2, 0.0], x_length=8.0, y_length=4.2, xlabel=r"steps $n$ on $[0, 1]$",
                 ylabel=r"root mean squared error of $Y_1$, $H = 0.1$ (log scale)",
                 xticks=[np.log10(8), np.log10(64), np.log10(512)], yticks=[-2, -1.5, -1, -0.5, 0],
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{10 ** v:.3g}", font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for k in ("riemann", "hybrid1", "hybrid2"):
            lines.add(VGroup(curve(ax, np.log10(ns), np.log10(e[k]["rmse"]), S_COL[k], stroke_width=3),
                             *[Dot(ax.c2p(np.log10(a_), np.log10(b_)), radius=0.05, color=S_COL[k])
                               for a_, b_ in zip(ns, e[k]["rmse"])]))
        leg = legend([(S_COL[k], S_NAME[k]) for k in S_COL], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r8, r1024 = e["riemann"]["rmse"][0], e["riemann"]["rmse"][-1]
        h8 = e["hybrid1"]["rmse"][0]
        side = wrapped_label(rf"exact, from the cell sums; the standard deviation of $Y_1$ itself is 1. From 8 to 1{{,}}024 "
                             rf"steps the Riemann error falls from {r8:.2f} to {r1024:.2f}; the hybrid scheme starts at "
                             rf"{h8:.3f}", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The errors, computed exactly. <bookmark mark='a'/> The Riemann sum: from eight steps to over a thousand, "
            f"its error falls from {r8:.2f} to {r1024:.2f}, on a variable whose own standard deviation is one. The "
            "slope is a tenth. <bookmark mark='b'/> The hybrid scheme with one exact cell: the same slope, twenty times "
            "lower. <bookmark mark='c'/> With two exact cells, lower again. The rate is set by H; the scheme only "
            "chooses the constant."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(lines[k]), FadeIn(leg[k]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def mc(self, t):
        hx = [-3.8, -1.4, 0.9, 3.3, 5.6]
        head = VGroup(label(r"steps $n$", font_size=20, color=GREY_B), label(r"Riemann, MC", font_size=20, color=BAD),
                      label(r"formula", font_size=20, color=BAD), label(r"hybrid, MC", font_size=20, color=ROUGH),
                      label(r"formula", font_size=20, color=ROUGH))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(str(m["n"]), font_size=26),
                                                 MathTex(rf"{m['rmse_riemann']:.4f}", font_size=26),
                                                 MathTex(rf"{m['formula_riemann']:.4f}", font_size=26),
                                                 MathTex(rf"{m['rmse_hybrid1']:.4f}", font_size=26),
                                                 MathTex(rf"{m['formula_hybrid1']:.4f}", font_size=26)) for m in t["mc"]]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.68 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"Monte Carlo against the formula, $H = 0.1$: 200{,}000 draws of the exact joint Gaussian law "
                             r"of the increments, the cells' exact integrals and $Y$ on the grid (its covariance by "
                             r"quadrature), so the true $Y$ and both schemes are computed from the same Brownian path",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Check the formula by simulation. Draw the increments, the exact cell integrals and the true rough path on "
            "the grid from their exact joint Gaussian law, so the true value and both schemes come from the same "
            "Brownian path. <bookmark mark='a'/> The simulated errors match the formula to three digits, for both "
            "schemes, at every grid."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def weak(self, t):
        P = t["price"]
        ns = np.array([p["n"] for p in P], float)
        g = axes([0.8, 1.9], [11, 18.5], x_length=7.6, y_length=4.2, xlabel=r"steps $n$",
                 ylabel=r"implied volatility of a one-year at-the-money call, \%",
                 xticks=[np.log10(8), np.log10(16), np.log10(32), np.log10(64)], yticks=[12, 14, 16, 18],
                 xfmt=lambda v: f"{10 ** v:.0f}", font_size=15, log_x=True).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        sets = [("exact_iv", WHITE, r"exact $Y$ on the grid"), ("riemann_iv", BAD, r"Riemann, true compensator $t^{2H}$"),
                ("riemann_wick_iv", OPT, r"Riemann, its own variance"), ("hybrid1_iv", ROUGH, r"hybrid, $\kappa = 1$")]
        lines = VGroup()
        for key, col, _ in sets:
            y = 100 * np.array([p[key] for p in P])
            lines.add(VGroup(curve(ax, np.log10(ns), y, col, stroke_width=3),
                             *[Dot(ax.c2p(np.log10(a_), b_), radius=0.05, color=col) for a_, b_ in zip(ns, y)]))
        leg = legend([(c, n) for _, c, n in sets], font_size=15).to_edge(RIGHT, buff=0.25).shift(UP * 1.5)
        fit_right(leg)
        rb = t["rbergomi"]
        side = wrapped_label(rf"rough Bergomi, $H = {rb['H']}$, $\eta = {rb['eta']}$, $\rho = {rb['rho']}$, $\xi = "
                             rf"{rb['xi']}$; the price step is the same Euler step in all four, so only the volatility's "
                             r"discretization differs; 200{,}000 paths with common random numbers", 3.4, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        p8, p64 = P[0], P[-1]
        with self.voiceover(
            "Prices are what desks need, and there the story changes. A one-year at-the-money call in rough Bergomi, "
            "with every scheme sharing the same price step. <bookmark mark='a'/> In white, the exact rough path on the "
            "grid. <bookmark mark='b'/> The naive Riemann sum, exponentiated with the true variance t to the two H, is "
            f"about {100 * (p8['exact_iv'] - p8['riemann_iv']):.0f} vol points too low at every grid: its path has too "
            "little variance, so the mean of the variance process is biased down, and that bias shrinks like n to "
            "the minus two H. <bookmark mark='c'/> Use the scheme's own variance in the exponent instead, and the "
            f"price converges: {100 * (p8['riemann_wick_iv'] - p8['exact_iv']):.1f} points off at eight steps, "
            f"{100 * (p64['riemann_wick_iv'] - p64['exact_iv']):.1f} at sixty-four, roughly n to the minus two "
            "thirds, close to the rate H plus a half that Christian Bayer, Eric Hall and Raúl Tempone prove for a "
            "linear rough model. "
            "<bookmark mark='d'/> The hybrid scheme is within a hundredth of a point at every grid."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(lines[k]), FadeIn(leg[k]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the weak rate of rough Bergomi", r"sharp weak rates are proved for linear rough models "
                          r"(Bayer, Hall and Tempone 2022) and special payoffs (Gassiat 2022); for the exponential, "
                          r"nonlinear rough Bergomi with general payoffs the rate is open", width=12.4, font_size=18),
            desk_question(r"open: multilevel Monte Carlo when the strong rate is $H$", r"multilevel methods need a good "
                          r"strong rate to couple levels cheaply; with rate $H$ their gain shrinks, and the best "
                          r"couplings for rough models are an active topic", width=12.4, font_size=18),
            desk_question(r"open: rough and path-dependent at once", r"for path-dependent payoffs and for the joint "
                          r"SPX/VIX models of Chapter 15, error expansions that would justify extrapolation in $n$ are "
                          r"not available", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Sharp weak rates are proved for linear rough models and for "
            "special payoffs; for the exponential rough Bergomi with a general payoff, the rate is open. "
            "<bookmark mark='b'/> Multilevel Monte Carlo couples coarse and fine grids cheaply only when the strong "
            "rate is good; with a rate of H its gain shrinks, and the best couplings are an active topic. "
            "<bookmark mark='c'/> And for path-dependent payoffs, or the joint models of Chapter 15, there are no "
            "error expansions that would justify extrapolating in the number of steps."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"at $H = 0.1$, a Riemann scheme with 64 steps has error 0.48. How many steps would cut it to 0.24? "
                       r"And at $H = 0.4$?")
        with self.voiceover(
            "Pause and predict. At H of a tenth, a Riemann scheme with sixty-four steps has an error of point four "
            "eight. How many steps would halve it? And at H of point four?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
