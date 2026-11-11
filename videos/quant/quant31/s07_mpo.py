from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, COST_C, GOOD, GP_C, HURDLE, IC_C, MYO_C, PART, fit_right, illustration

A0, PHI, GAM, S2, CC = 0.01, 0.15, 5.0, 0.0025, 0.02


def plan(H: int, x0: float = 0.0):
    """The multi-period plan for one asset: forecasts a0 (1 - phi)^tau, risk gam/2 s2 x^2, impact c |dx|^(3/2); the
    plan's holdings for tau = 1..H (free terminal holdings: no forced liquidation; smooth impact approximation)."""
    al = A0 * (1 - PHI) ** np.arange(H)

    def f(x):
        dx = np.diff(np.r_[x0, x])
        return -(al @ x - 0.5 * GAM * S2 * np.sum(x ** 2) - CC * np.sum((dx ** 2 + 1e-12) ** 0.75))
    result = minimize(f, np.zeros(H), method="L-BFGS-B")
    if not result.success:
        raise RuntimeError(f"Fixed toy horizon {H} did not converge: {result.message}")
    return result.x


class MultiPeriod(VoiceoverScene):
    def construct(self):
        self.card()
        self.formulation()
        self.receding()
        self.forecasts()
        self.inside()
        self.demo()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Multi-period optimization", r"What if the costs are not quadratic and the constraints are "
                         r"real?", part=PART)
        with self.voiceover("Chapter six. Garleanu and Pedersen's closed form needs quadratic costs and no constraints. "
                            "Real books have neither. The modern answer gives up the closed form and keeps the idea."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def formulation(self):
        rows = [cmath(r"\max_{x_{t+1},\dots,x_{t+H}}", r"\ ", r"\textstyle\sum_{\tau=1}^{H}\Big[\hat\alpha_{t+\tau|t}^\top "
                      r"x_{t+\tau} - \gamma\,\psi(x_{t+\tau}) - \phi^{\text{trade}}(x_{t+\tau} - x_{t+\tau-1})\Big]",
                      font_size=28, colors={r"\phi^{\text{trade}}(x_{t+\tau} - x_{t+\tau-1})": COST_C}),
                cmath(r"\text{s.t.}", r"\ ", r"x_{t+\tau} \in \mathcal C_{t+\tau}\quad\text{(limits, leverage, turnover, "
                      r"neutrality)}", font_size=28),
                cmath(r"\text{trade}", r":", r"x_{t+1} - x_t\ \text{ only; then re-plan tomorrow}", font_size=30,
                      colors={r"\text{trade}": GP_C})]
        whys = [why(r"Boyd and coauthors (2017): forecasts for each future period, any convex risk $\psi$, any convex "
                    r"trade cost $\phi$: spread and three-halves impact; borrowing instead requires a separate holding-cost term"),
                why(r"any convex constraint, on every planned period"),
                why(r"model predictive control: execute only the first step of the plan, then solve again with new "
                    r"forecasts")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "In 2017 Stephen Boyd and coauthors set out the general version. <bookmark mark='a'/> Plan a path of holdings "
            "over the next H periods, using a forecast for each: maximise expected return, less any convex measure of "
            "risk, less any convex trading cost, such as the spread and the three-halves power of impact. "
            "<bookmark mark='b'/> Add any convex constraint on every planned period. <bookmark mark='c'/> Then execute "
            "only the first trade, and tomorrow, with new forecasts, plan again. It is a convex problem, which standard "
            "solvers handle quickly for thousands of assets."
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

    def receding(self):
        boxes = VGroup()
        for k in range(4):
            row = VGroup(*[Square(0.42, stroke_color=GREY_C, stroke_width=1.2, fill_opacity=0.0) for _ in range(6)])
            row.arrange(RIGHT, buff=0.06)
            row[0].set_fill(GP_C, 0.7).set_stroke(GP_C)
            row.move_to([-2.6 + 0.48 * k, 1.6 - 0.8 * k, 0])
            lab_ = label(rf"day {k + 1}: plan 6 periods, trade the first", font_size=17, color=GREY_A)
            lab_.next_to(row, RIGHT, buff=0.4)
            boxes.add(VGroup(row, lab_))
        foot = wrapped_label(r"model predictive control, the same idea that steers chemical plants and self-driving cars: plan far, "
                             r"commit to one step, re-plan with what you learn", 11.4, 18, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The receding horizon. <bookmark mark='a'/> Each day, plan several periods ahead, execute the first step, and move the window forward. This is model predictive control. <bookmark mark='b'/> Replanning incorporates new information; it does not make an inaccurate forecast correct. Forecast error, covariance error, solver accuracy and actual execution all remain relevant."
        ) as vo:
            self.play(FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in boxes[1:]], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def forecasts(self):
        rows = [cmath(r"\hat\alpha_{t+\tau|t}", r"=", r"(1 - \phi)^{\tau - 1}\,\hat\alpha_{t+1|t}", font_size=36,
                      colors={r"\hat\alpha_{t+\tau|t}": IC_C}),
                cmath(r"\hat\Sigma_{t+\tau|t}", r"=", r"\hat\Sigma_t\quad\text{(or a GARCH forecast, Part 7)}", font_size=32),
                cmath(r"\hat\kappa_{t+\tau|t}", r":", r"\text{volume and spread forecasts by time of day and calendar}",
                      font_size=30, colors={r"\hat\kappa_{t+\tau|t}": COST_C})]
        whys = [why(r"a term structure of expected returns: each signal decays at its measured speed (Chapter 5)"),
                why(r"risk forecasts for each period: often held constant, since risk is more persistent than alpha"),
                why(r"and cost forecasts: trading is cheaper when volume is high, so the plan schedules trades into "
                    r"liquid periods")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the plan needs is a forecast for every period ahead. <bookmark mark='a'/> For returns, a term "
            "structure: each signal's forecast decays at its measured speed, as in Chapter five. "
            "<bookmark mark='b'/> For risk, often today's estimate, held constant, since risk is far more persistent "
            "than alpha; or a GARCH forecast from Part seven. <bookmark mark='c'/> And for costs: volume and spreads "
            "vary by the hour and the calendar, so the plan moves trades into the periods when trading is cheap."
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

    def inside(self):
        items = [(r"position limits", r"no more than a few percent of the book in any asset", HURDLE),
                 (r"liquidity limits", r"no position larger than a few days' volume", COST_C),
                 (r"factor neutrality", r"zero exposure to market, size, industries, from the risk model", QC.OPTION),
                 (r"turnover budget", r"total trading capped per day", GREY_B),
                 (r"a variance floor", r"no asset's forecast risk below a minimum: Chapter 11 shows why", BAD)]
        rows = VGroup()
        for nm, d, col in items:
            rows.add(VGroup(label(nm, font_size=23, color=col), label(d, font_size=17, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.2 + LEFT * 0.6)
        head = label(r"Convex position constraints and risk-input safeguards", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Separate position constraints from model safeguards. <bookmark mark='a'/> Position, liquidity, exposure and turnover limits define a feasible set when expressed as convex constraints. They restrict planned positions; they do not guarantee realised risk or execution. <bookmark mark='b'/> A variance floor changes the risk input rather than adding a position constraint. Chapter eleven illustrates the distinction with fixed numbers, without a market experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def demo(self):
        T = 40
        mk = A0 * (1 - PHI) ** np.arange(T) / (GAM * S2)
        p1, p5, p40 = plan(1), plan(5), plan(40)
        g = axes([0, T], [0, 0.85], x_length=7.6, y_length=4.4, xlabel=r"days ahead", ylabel=r"planned position",
                 xticks=[0, 10, 20, 30, 40], yticks=[0, 0.4, 0.8], yfmt=lambda v: f"{v:.1f}", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        ts = np.arange(1, T + 1)
        c_m = curve(ax, ts, mk, MYO_C, stroke_width=2)
        c40 = curve(ax, ts, p40, GP_C, stroke_width=4)
        c5 = curve(ax, ts[:5], p5, HURDLE, stroke_width=3)
        d1 = Dot(ax.c2p(1, p1[0]), radius=0.09, color=BAD)
        leg = legend([(MYO_C, r"Markowitz, if trading were free"), (BAD, r"one period ahead"),
                      (HURDLE, r"5 periods ahead"), (GP_C, r"40 periods ahead")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 2.0)
        fit_right(leg)
        ill = illustration(r"illustration: one asset, a forecast that decays 15\% a day, smoothed $|\Delta x|^{3/2}$ cost; free terminal holdings")
        with self.voiceover(
            f"""A fixed mathematical toy, not a trading backtest. One asset, geometric forecast decay of fifteen percent, fixed risk, and a smooth approximation to three-halves impact. All three numerical solves converged. <bookmark mark='a'/> The frictionless target uses the same period indexing. <bookmark mark='b'/> The one-period solution starts at {p1[0]:.2f}. <bookmark mark='c'/> Five periods starts at {p5[0]:.2f}. <bookmark mark='d'/> Forty periods starts at {p40[0]:.2f}; its complete path is shown. All horizons have free terminal holdings, not forced liquidation. Their objectives differ, so these paths illustrate boundary effects, not a theorem that more periods always improve the first trade."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c_m))
            vo.wait_until("b")
            self.play(FadeIn(d1, scale=1.5))
            vo.wait_until("c")
            self.play(Create(c5))
            vo.wait_until("d")
            self.play(Create(c40), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"single-period optimisation with costs", r"values only one period of expected benefit; its decision can differ from a longer-horizon objective", width=12.4, font_size=19),
            desk_question(r"a short horizon", r"has boundary effects with free terminal holdings; first-trade errors need not have a universal sign",
                          width=12.4, font_size=19),
            desk_question(r"the link", r"matching quadratic costs, timing, discount and forecasts can recover the infinite-horizon Riccati policy", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons about objectives. <bookmark mark='a'/> A one-period model values only one period of future benefit. <bookmark mark='b'/> A finite horizon and its terminal assumptions create boundary effects; neither the size nor the sign of the first-trade difference is universal. <bookmark mark='c'/> With matching quadratic costs, timing, discount, forecasts and no constraints, an infinite-horizon limit can recover the Riccati policy. The displayed three-halves toy is a different cost model."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a forecast is expected to last one day. Does a longer planning horizon change today's trade much?")
        with self.voiceover(
            "Pause and predict. A forecast is expected to last only one day. Does a longer planning horizon change today's "
            "trade much?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
