from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, SHRINK_C, fit_right, load


class CVaR(VoiceoverScene):
    def construct(self):
        c = load("cvar")
        self.card()
        self.robust()
        self.robust_meaning()
        self.lp()
        self.var_problem()
        self.tails(c)
        self.result(c)
        self.question()

    def card(self):
        c = chapter_card(8, r"Robust optimisation and CVaR", r"What if risk is not variance, and the inputs are not "
                         r"known?", part=PART)
        with self.voiceover("Chapter eight. Two more ways to make the optimizer humble: plan for the worst inputs, and "
                            "measure risk by the losses that matter, not by variance."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def robust(self):
        rows = [cmath(r"\max_w\ \min_{\mu \in U}", r"\ ", r"w^\top\mu - \tfrac\gamma2 w^\top\Sigma w", font_size=32,
                      colors={r"\max_w\ \min_{\mu \in U}": SHRINK_C}),
                cmath(r"U", r"=", r"\{\mu : (\mu - \hat\mu)^\top\Omega^{-1}(\mu - \hat\mu) \le \kappa^2\}", font_size=32),
                cmath(r"\min_{\mu \in U} w^\top\mu", r"=", r"w^\top\hat\mu - \kappa\sqrt{w^\top\Omega w}", font_size=32,
                      colors={r"\min_{\mu \in U} w^\top\mu": BAD})]
        whys = [why(r"choose the weights that do best when nature picks the worst means in an uncertainty set"),
                why(r"an ellipsoid around the estimate, its shape the estimate's own covariance (Goldfarb and Iyengar "
                    r"2003; Ceria and Stubbs 2006)"),
                why(r"the inner minimum has a closed form: a penalty on exactly the bets the estimates are least sure of; "
                    r"the problem becomes a second-order cone program")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Robust optimisation first. <bookmark mark='a'/> Choose the weights that do best when nature picks the worst "
            "expected returns from a set of plausible ones. <bookmark mark='b'/> Make the set an ellipsoid around the "
            "estimate, shaped by the estimate's own uncertainty. <bookmark mark='c'/> The worst case has a closed form: "
            "the estimated return minus kappa times the uncertainty of the bet. The optimizer is charged for leaning on "
            "noisy estimates, which is Chapter one's disease, treated at its source."
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

    def robust_meaning(self):
        rows = [cmath(r"\Omega = \Sigma/T", r":", r"\max_w\ w^\top\hat\mu - \tfrac{\kappa}{\sqrt T}\sqrt{w^\top\Sigma w} - "
                      r"\tfrac\gamma2 w^\top\Sigma w", font_size=30, colors={r"\Omega = \Sigma/T": HURDLE}),
                cmath(r"\hat w", r"\propto", r"\Sigma^{-1}\hat\mu\ \text{with a larger effective risk aversion}", font_size=30),
                cmath(r"1^\top w = 1", r"\Rightarrow", r"\hat w = (1 - a)\,w_{\text{tan}} + a\,w_{\text{GMV}},\ a \uparrow "
                      r"\text{in } \kappa", font_size=30, colors={r"1^\top w = 1": SHRINK_C})]
        whys = [why(r"the most common choice: the uncertainty of the means is the covariance over the sample size"),
                why(r"the first-order condition is still $\Sigma w \propto \hat\mu$ minus a multiple of $\Sigma w$: only "
                    r"the scale changes"),
                why(r"with a budget constraint the extra caution moves the portfolio toward the minimum-variance "
                    r"portfolio, which uses no estimated means")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What robustness buys depends on the shape of the set. <bookmark mark='a'/> The common choice makes the means' "
            "uncertainty the covariance divided by the sample size. <bookmark mark='b'/> Then the robust portfolio "
            "points in the same direction as the ordinary one: the worst case acts like extra risk aversion. "
            "<bookmark mark='c'/> With the budget fixed at one, more aversion means a mix that leans toward the "
            "minimum-variance portfolio, the one that needs no expected returns. Robust optimisation, done this way, "
            "rediscovers Chapter two's lesson."
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

    def lp(self):
        rows = [cmath(r"\mathrm{CVaR}_\beta(L)", r"=", r"\mathbb E[L \mid L \ge \mathrm{VaR}_\beta]", font_size=32,
                      colors={r"\mathrm{CVaR}_\beta(L)": BAD}),
                cmath(r"\mathrm{CVaR}_\beta", r"=", r"\min_\alpha\ \alpha + \frac{1}{1 - \beta}\mathbb E\big[(L - \alpha)^+\big]",
                      font_size=32, colors={r"\mathrm{CVaR}_\beta": BAD}),
                cmath(r"\min_{w, \alpha, u}", r"\ ", r"\alpha + \frac{1}{(1 - \beta)J}\textstyle\sum_j u_j,\ \ u_j \ge -r_j^\top w - "
                      r"\alpha,\ u_j \ge 0", font_size=28, colors={r"\min_{w, \alpha, u}": SHRINK_C})]
        whys = [why(r"the expected loss in the worst $1 - \beta$ of outcomes: unlike VaR, it sees how bad the tail is, "
                    r"and it is coherent (Part 40)"),
                why(r"Rockafellar and Uryasev (2000): a minimisation over one number, $\alpha$, whose minimiser is the VaR"),
                why(r"over $J$ scenarios the whole problem, weights included, is one linear program")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Then a different risk. <bookmark mark='a'/> Conditional value at risk: the average loss in the worst five "
            "percent of outcomes. It sees how deep the tail goes, which variance and value at risk do not. "
            "<bookmark mark='b'/> Tyrrell Rockafellar and Stanislav Uryasev found in 2000 that it is a minimum over a "
            "single number alpha, whose minimiser is the value at risk itself. <bookmark mark='c'/> Over a set of "
            "scenarios, the whole portfolio problem becomes one linear program: one auxiliary variable per scenario, and "
            "a solver finds the answer in a fraction of a second."
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

    def var_problem(self):
        cards = VGroup(
            desk_question(r"VaR is not subadditive", r"two bonds, each defaulting with probability 4\%, each have a 95\% "
                          r"VaR of zero; together, the chance of at least one default is 7.8\%, so the pair's VaR is a "
                          r"full loss: diversification `raised' the risk", width=12.4, font_size=19),
            desk_question(r"so VaR is a bad objective", r"it is not convex in the weights: an optimizer that minimises it "
                          r"finds local minima and hides risk just beyond the quantile", width=12.4, font_size=19),
            desk_question(r"CVaR is coherent and convex", r"subadditive, it rewards diversification, and its minimisation is "
                          r"a linear program (Artzner, Delbaen, Eber and Heath 1999 define coherence; Part 40)",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why not simply minimise value at risk? <bookmark mark='a'/> Two bonds, each with a four percent chance of "
            "default. Each alone has a ninety-five percent value at risk of zero. Together, the chance that at least one "
            "defaults is seven point eight percent, so the pair's value at risk is a full default: by this measure, "
            "diversifying raised the risk. <bookmark mark='b'/> Value at risk is not convex in the weights, and an "
            "optimizer minimising it learns to hide losses just beyond the quantile. <bookmark mark='c'/> CVaR is "
            "coherent: it always rewards diversification, and minimising it is a linear program."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, c):
        a = 100 * np.asarray(c["in"]["min variance"]["r"], float)
        b = 100 * np.asarray(c["in"]["min CVaR"]["r"], float)
        lo, hi = -18, 0
        bins = np.linspace(lo, hi, 19)
        ha, _ = np.histogram(np.clip(a, lo, hi), bins)
        hb, _ = np.histogram(np.clip(b, lo, hi), bins)
        ym = float(max(ha.max(), hb.max()) + 2)
        g = axes([lo, hi], [0, ym], x_length=7.4, y_length=4.2, xlabel=r"monthly excess return, \% (losses only)",
                 ylabel=r"months", xticks=[-15, -10, -5, 0], yticks=[0, ym], yfmt=lambda v: f"{v:.0f}", font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        w = bins[1] - bins[0]

        def bars(h, col, dx):
            return VGroup(*[Rectangle(width=(ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0]) * 0.42,
                                      height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to(ax.c2p(x0 + w * (0.5 + dx), 0), aligned_edge=DOWN)
                            for x0, v in zip(bins[:-1], h) if v > 0])
        ba, bb = bars(ha, SHRINK_C, -0.22), bars(hb, BAD, 0.22)
        q = float(np.quantile(a, 0.05))
        n6a, n6b = int((a < -6).sum()), int((b < -6).sum())
        n2a, n2b = int((a < -2).sum()), int((b < -2).sum())
        line = DashedLine(ax.c2p(q, 0), ax.c2p(q, ym), color=HURDLE, stroke_width=2)
        leg = legend([(SHRINK_C, rf"min variance ({c['in']['min variance']['n_held']} industries held)"),
                      (BAD, rf"min CVaR ({c['in']['min CVaR']['n_held']} held)")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        with self.voiceover(
            "The two portfolios' losing months, 1970 to 2020. <bookmark mark='a'/> The minimum-variance portfolio's in "
            "grey, the minimum-CVaR portfolio's in red, with the five percent quantile marked. Minimising CVaR moves "
            f"months out of the tail: {n6a} months below minus six percent become {n6b}. The price is more moderate "
            f"losses, {n2a} months below minus two percent become {n2b}. It also holds fewer industries, because it fits "
            "itself to a few dozen worst months."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in ba], lag_ratio=0.05),
                      LaggedStart(*[GrowFromEdge(x, DOWN) for x in bb], lag_ratio=0.05))
        self.wait(0.4)
        self.clear_scene()

    def result(self, c):
        hx = [-3.6, -0.4, 2.2, 4.8]
        head = VGroup(label(r"long-only portfolio", font_size=18, color=GREY_B), label(r"volatility", font_size=18,
                                                                                     color=GREY_B),
                      label(r"CVaR 95\%, a month", font_size=18, color=GREY_B), label(r"worst month", font_size=18,
                                                                                   color=GREY_B))
        sec = [(r"in sample, 1970--2020", c["in"]), (r"rolling, 1980--2020", c["oos"])]
        rows = VGroup()
        y = 2.0
        groups = []
        for title, d in sec:
            t = label(title, font_size=19, color=HURDLE).move_to([-3.6, y, 0])
            y -= 0.6
            g = VGroup(t)
            for k, col in (("min variance", SHRINK_C), ("min CVaR", BAD)):
                x = d[k]
                r = VGroup(label(k, font_size=19, color=col), MathTex(rf"{100 * x['vol']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * x['cvar']:.2f}\%", font_size=24), MathTex(rf"{100 * x['worst']:.1f}\%", font_size=24))
                for i, cell in enumerate(r):
                    cell.move_to([hx[i], y, 0])
                g.add(r)
                y -= 0.55
            y -= 0.2
            groups.append(g)
        for i, cell in enumerate(head):
            cell.move_to([hx[i], 2.7, 0])
        foot = wrapped_label(rf"monthly excess returns of the 49 industries as scenarios ({c['J']} in sample; 120 in each "
                             r"rolling window); the rolling rows are realised the month after", 11.4, 16, GREY_A
                             ).to_edge(DOWN, buff=0.5)
        ci, co = c["in"], c["oos"]
        n_win = 120
        n_tail = int(round(n_win * 0.05))
        with self.voiceover(
            "On the industries. <bookmark mark='a'/> In sample, minimising CVaR does what it says: a CVaR of "
            f"{100 * ci['min CVaR']['cvar']:.2f} percent a month against {100 * ci['min variance']['cvar']:.2f} for "
            "minimum variance. <bookmark mark='b'/> Rolled forward on ten-year windows, the order flips: minimum CVaR "
            f"realises a CVaR of {100 * co['min CVaR']['cvar']:.2f} percent and minimum variance "
            f"{100 * co['min variance']['cvar']:.2f}. A tail is estimated from its few worst scenarios, {n_tail} out of "
            f"{n_win}, and an optimizer fed {n_tail} numbers per asset fits them. The better risk measure needs "
            "more data than the worse one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with 120 monthly scenarios and $\beta = 95\%$, how many scenarios determine the CVaR? And with "
                       r"$\beta = 99\%$?")
        with self.voiceover(
            "Pause and predict. With a hundred and twenty monthly scenarios, how many of them determine the CVaR at "
            "ninety-five percent? And at ninety-nine?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
