from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

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
        with self.voiceover("""For the researcher: uniform-grid rough-driver error. For the power kernel with H between zero and one half, admissible fixed within-cell evaluation rules have root mean squared error of order n to minus H. A hybrid scheme with a fixed number of exact cells can sharply reduce the constant without changing that rate. This is not a lower bound for every possible mesh, approximation class or growing exact-cell count. We will compare exact deterministic error integrals with the original simulations."""):
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
                why('uniform grid and a fixed admissible within-cell rule ($0<H<1/2$)'),
                why(r"It\^o's isometry, and the substitution $1 - s = x\Delta$: the whole error is $\Delta^{2H}$ times a sum "
                    r"that converges, because the terms fall like $j^{2a - 2}$"),
                why('Uniform grid, fixed admissible within-cell rules, $0<H<1/2$: RMSE has order $n^{-H}$; this is not a bound for every approximation class.')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            """Take the Riemann--Liouville driver at time one with H strictly between zero and one half. <bookmark mark='a'/> The power kernel is square integrable but unbounded at the endpoint. <bookmark mark='b'/> A uniform-grid step approximation uses a fixed rule for each lag cell's evaluation point; the point must stay within its cell. <bookmark mark='c'/> Itô's isometry gives the displayed exact error integral. After scaling, the tail cell errors are summable for these admissible rules and the first-cell error is positive. <bookmark mark='d'/> Thus root mean squared error has order n to minus H. At H of one tenth, an asymptotic halving needs a factor of two to the tenth in grid size. This statement does not cover arbitrary nonuniform meshes or changing approximation classes."""
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
                why('For fixed $\\kappa$, the first unresolved cell leaves rate $n^{-H}$ with a much smaller constant. Growing $\\kappa$ is a different regime.')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"The hybrid scheme's error", wrapped_label(
            'Fixed exact-cell count $\\kappa$ and uniform-grid power kernel: MSE $\\sim J(H,\\kappa,b)n^{-2H}$. The improvement depends on $H$, $\\kappa$ and the remaining evaluation rule.', 10.6, 20, GREY_A),
            who=r"Bennedsen, Lunde and Pakkanen (2017), \textit{Finance and Stochastics} 21", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The hybrid scheme attacks the constant. <bookmark mark='a'/> Simulate the first kappa cells' integrals exactly, as Gaussians jointly drawn with the increments, and step the rest. <bookmark mark='b'/> Use the optimal evaluation points of Chapter 6. <bookmark mark='c'/> The error is the same sum, but it now starts after the singularity. The rate is still n to the minus H. The constant collapses, because almost all of it sat in the first cell. <bookmark mark='d'/> Mikkel Bennedsen, Asger Lunde and Mikko Pakkanen gave the exact asymptotic constant in 2017. Here kappa is fixed as the grid is refined. Growing kappa or changing the approximation class can change the rate."
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
            f"""Now the original finite-grid price experiment: one-year at-the-money rough-Bergomi calls, with the same stock Euler step in every scheme. <bookmark mark='a'/> White uses the exact joint Gaussian driver on the grid, with covariance evaluated numerically. It still has stock time-discretization and Monte Carlo error. <bookmark mark='b'/> At eight steps, the naive scheme with the theoretical compensator is lower by {100 * (p8['exact_iv'] - p8['riemann_iv']):.0f} volatility points. Its driver variance is too small for that compensator; the driver variance deficit has order n to minus two H. That does not automatically prove the same price-bias rate. <bookmark mark='c'/> Using the scheme's own variance leaves differences of {100 * (p8['riemann_wick_iv'] - p8['exact_iv']):.1f} points at eight steps and {100 * (p64['riemann_wick_iv'] - p64['exact_iv']):.1f} at sixty-four. Four coupled grids do not establish an asymptotic weak rate. Bayer, Hall and Tempone's H plus one half theorem concerns a linear rough Stein--Stein model under payoff assumptions, not this nonlinear exponential model. <bookmark mark='d'/> The hybrid curve is close to the grid reference in this experiment; proximity to a shared-grid reference is not continuous-time pricing certification."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(lines[k]), FadeIn(leg[k]), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question('question: which weak-rate theorem matches the implemented model and payoff?', 'Check coefficient, payoff and scheme assumptions before transferring a rate. The cited linear-model result does not establish a rate for this exponential model.', width=12.4, font_size=18),
            desk_question('question: how effective is the chosen multilevel coupling?', r"multilevel methods need a good "
                          r"strong rate to couple levels cheaply; with rate $H$ their gain shrinks, and the best "
                          r"couplings for rough models are an active topic", width=12.4, font_size=18),
            desk_question('question: is grid extrapolation justified for this target?', 'Path-dependent and joint-model targets need their own discretization analysis. These four vanilla-price grids do not justify extrapolation for them.', width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            """Three questions for implementation. <bookmark mark='a'/> Which weak-error theorem actually matches the coefficients, payoff and discretization? A result for a linear rough model cannot simply be transferred to rough Bergomi. <bookmark mark='b'/> How much variance reduction does a proposed multilevel coupling deliver at its measured computational cost? A small H can make a naive coupling inefficient, but the rate alone does not settle every construction. <bookmark mark='c'/> Finally, does the target admit an error expansion that justifies grid extrapolation? Our four-grid vanilla experiment does not answer that for path-dependent products or joint SPX and VIX models. These are questions left unverified here, rather than an exhaustive claim about the current literature."""
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('Assume RMSE $\\sim Cn^{-H}$. Halving needs $2^{1/H}$ times the steps: $1024$ at $H=0.1$, $5.66$ at $H=0.4$. Starting at $n=64$: about $65{,}536$ or $362$.')
        with self.voiceover(
            """Assume the asymptotic root mean squared error is C times n to minus H. What grid-size multiplier halves it? Two to the power one over H: one thousand twenty-four for H of one tenth, and about five point seven for H of four tenths. Starting from sixty-four steps, those are roughly sixty-five thousand five hundred thirty-six and three hundred sixty-two steps. These are asymptotic planning calculations, not exact finite-grid predictions."""
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
