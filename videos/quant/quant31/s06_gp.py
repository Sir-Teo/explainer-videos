from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import BAD, COST_C, GOOD, GP_C, HURDLE, IC_C, MYO_C, PART, fit_right, illustration, load


class AimPortfolio(VoiceoverScene):
    def construct(self):
        g = load("gp")
        self.card()
        self.problem()
        self.solution()
        self.aim()
        self.picture()
        self.check()
        self.multi()
        self.coins(g)
        self.table(g)
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(5, r"Trading toward a moving target", r"If the forecast will change tomorrow, how far should you "
                         r"trade today?", part=PART)
        with self.voiceover("Chapter five. Nicolae Garleanu and Lasse Pedersen solved, in 2013, the problem every "
                            "systematic trader faces each morning: the forecasts have moved, trading costs money, and they "
                            "will move again tomorrow."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self):
        rows = [cmath(r"r_{t+1}", r"=", r"B f_t + u_{t+1},\qquad f_{t+1} = (I - \Phi) f_t + \varepsilon_{t+1}", font_size=32,
                      colors={r"B f_t": IC_C}),
                cmath(r"V(x_-,f)", r"=", r"\max_x\{d[x^\top Bf-\tfrac\gamma2x^\top\Sigma x]-\tfrac\lambda2\Delta x^\top\Sigma\Delta x+d\mathbb EV(x,f^+)\}", font_size=27),
                cmath(r"\Phi", r"=", r"\operatorname{diag}(\phi_1, \dots, \phi_K)", font_size=32)]
        whys = [why(r"expected returns come from signals $f_t$, each mean-reverting at its own speed: momentum slowly, "
                    r"reversal fast"),
                why(r"choose a path of holdings to maximise discounted expected return, less risk, less a quadratic cost "
                    r"of each trade $\Delta x_t = x_t - x_{t-1}$, scaled by risk"),
                why(r"$\phi_k$ is the fraction of signal $k$ that decays each period: its half-life is $\ln 2/\phi_k$ "
                    r"periods, roughly")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Specify the timing before using the closed form. <bookmark mark='a'/> Signals have linear conditional dynamics and finite second moments. B f denotes the conditional next return, absorbing any one-step signal decay into B. <bookmark mark='b'/> In this Bellman convention, d equals one minus rho. Operating return and risk are discounted by d; the current trade cost is paid now; continuation value is discounted by d. Assume known fixed positive-definite covariance, positive risk aversion and quadratic cost, unconstrained notional holdings and a well-posed infinite horizon. <bookmark mark='c'/> Phi is diagonal here. Its entries parameterise geometric decay, rather than a universal description of empirical signals."
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

    def solution(self):
        rows = [cmath(r"V(x, f)", r"=", r"-\tfrac12 x^\top A_{xx} x + x^\top A_{xf} f + \dots", font_size=34),
                cmath(r"x_t", r"=", r"\Big(1 - \frac{a}{\lambda}\Big)x_{t-1} + \frac{a}{\lambda}\,\text{aim}_t", font_size=38,
                      colors={r"\text{aim}_t": GP_C}),
                cmath(r"a", r"=", r"\frac{-(\gamma\bar\rho + \lambda\rho) + \sqrt{(\gamma\bar\rho + \lambda\rho)^2 + "
                      r"4\gamma\lambda\bar\rho^{\,2}}}{2\bar\rho}", font_size=30),
                cmath(r"\frac{a}{\lambda}", r"\approx", r"\sqrt{\gamma/\lambda}\quad(\rho=0,\ \lambda\gg\gamma)", font_size=32,
                      colors={r"\frac{a}{\lambda}": HURDLE})]
        whys = [why(r"linear dynamics, quadratic objective: the value function is quadratic, and the Bellman equation "
                    r"becomes a Riccati equation (Part 8)"),
                why(r"Garleanu and Pedersen's Proposition: trade a fixed fraction of the way from yesterday's holdings to "
                    r"an aim portfolio"),
                why(r"the fraction solves the scalar Riccati equation; $\bar\rho = 1 - \rho$"),
                why(r"negligible-discount regime: $\gamma\ll\lambda\ll\gamma/\rho^2$; fixed $\rho>0$ instead gives a $1/\lambda$ tail")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Linear dynamics and quadratic costs give a quadratic value function. <bookmark mark='a'/> Matching Bellman coefficients gives a Riccati equation. <bookmark mark='b'/> Under these assumptions, trade a fixed fraction toward an aim portfolio. <bookmark mark='c'/> The fraction is a over lambda, with a the displayed positive root and rho bar equal to one minus rho. <bookmark mark='d'/> With zero or negligible discount and costs large relative to risk aversion, the rate is approximately square root of gamma over lambda. Quadrupling costs then roughly halves speed. At fixed positive rho and arbitrarily large lambda the rate instead behaves as gamma times one minus rho, divided by rho lambda."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def aim(self):
        rows = [cmath(r"\text{aim}_t", r"=", r"(\gamma\Sigma)^{-1} B\,\big(I + a\Phi/\gamma\big)^{-1} f_t", font_size=36,
                      colors={r"\text{aim}_t": GP_C}),
                cmath(r"\text{Markowitz}_t", r"=", r"(\gamma\Sigma)^{-1} B f_t", font_size=36, colors={r"\text{Markowitz}_t": MYO_C}),
                cmath(r"w_k", r"=", r"\frac{1}{1 + \phi_k a/\gamma}", font_size=38, colors={r"w_k": GP_C})]
        whys = [why(r"the aim portfolio: a weighted average of today's and future Markowitz portfolios, which for "
                    r"mean-reverting signals is Markowitz with each signal discounted"),
                why(r"the myopic target: the portfolio you would hold if trading were free"),
                why(r"each signal's weight in the aim: near one for a slow signal, small for a fast one, which will have "
                    r"decayed before you finish trading on it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And the aim portfolio is the insight. <bookmark mark='a'/> It is a weighted average of the Markowitz "
            "portfolio today and the Markowitz portfolios expected in the future. <bookmark mark='b'/> For signals that "
            "decay geometrically, that average is today's Markowitz portfolio with each signal discounted. "
            "<bookmark mark='c'/> A slow signal keeps almost all its weight. A fast signal is cut, because it will have "
            "decayed before you finish trading on it. Aim in front of the target, and move partway."
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

    def picture(self):
        rng = np.random.default_rng(31)
        T = 120
        phi_s, phi_f = 0.03, 0.4
        fs, ff = np.zeros(T), np.zeros(T)
        for t in range(1, T):
            fs[t] = (1 - phi_s) * fs[t - 1] + 0.25 * rng.standard_normal()
            ff[t] = (1 - phi_f) * ff[t - 1] + 0.9 * rng.standard_normal()
        lam, gam = 8.0, 1.0
        mk = fs + ff
        rate = RM.gp_trade_rate(gam, lam, 0.0005)
        aim = RM.gp_aim_weight(gam, lam, 0.0005, phi_s) * fs + RM.gp_aim_weight(gam, lam, 0.0005, phi_f) * ff
        x = np.zeros(T)
        for t in range(1, T):
            x[t] = x[t - 1] + rate * (aim[t] - x[t - 1])
        lo = float(np.floor(min(mk.min(), aim.min(), x.min())))
        hi = float(np.ceil(max(mk.max(), aim.max(), x.max())))
        g = axes([0, T], [lo, hi], x_length=8.4, y_length=4.4, xlabel=r"days", ylabel=r"position in one asset",
                 xticks=[0, 60, 120], yticks=[lo, 0, hi], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        ts = np.arange(T)
        c_m = curve(ax, ts, mk, MYO_C, stroke_width=2)
        c_a = curve(ax, ts, aim, HURDLE, stroke_width=2)
        c_x = curve(ax, ts, x, GP_C, stroke_width=4)
        leg = legend([(MYO_C, r"Markowitz: the myopic target"), (HURDLE, r"aim: fast signal discounted"),
                      (GP_C, r"Garleanu--Pedersen holdings")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 2.4)
        fit_right(leg)
        ill = illustration(r"illustration: a slow and a fast signal, simulated; $\lambda = 8$")
        with self.voiceover(
            "Here is what it looks like, for one asset driven by a slow and a fast signal. <bookmark mark='a'/> The "
            "Markowitz target jumps around with the fast signal; a myopic trader chases it, and pays for every jump. "
            "<bookmark mark='b'/> The aim portfolio discounts the fast signal, so it moves less. <bookmark mark='c'/> And "
            "the optimal holdings move only part of the way toward the aim each day: a smooth path that follows the "
            "slow signal and ignores most of the fast one's noise."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c_m), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c_a), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(c_x), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def check(self):
        rows = []
        hx = [-4.6, -2.6, -0.2, 2.4, 4.8]
        head = VGroup(label(r"$\lambda$", font_size=18, color=GREY_B), label(r"$\phi$", font_size=18, color=GREY_B),
                      label(r"trade rate: formula", font_size=18, color=GP_C),
                      label(r"value iteration", font_size=18, color=HURDLE), label(r"aim weight: both", font_size=18,
                                                                                   color=GP_C))
        tab = VGroup(head)
        for lam in (2.0, 8.0, 32.0):
            for phi in (0.02, 0.4):
                r_f, w_f = RM.gp_trade_rate(1.0, lam, 0.0005), RM.gp_aim_weight(1.0, lam, 0.0005, phi)
                r_v, w_v = RM.riccati_scalar(1.0, lam, 0.0005, phi)
                rows.append(abs(r_f - r_v) + abs(w_f - w_v))
                tab.add(VGroup(MathTex(f"{lam:g}", font_size=24), MathTex(f"{phi:g}", font_size=24),
                               MathTex(f"{r_f:.6f}", font_size=24), MathTex(f"{r_v:.6f}", font_size=24),
                               MathTex(rf"{w_f:.4f}\ /\ {w_v:.4f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.5 - 0.6 * j, 0])
        err = max(rows)
        foot = wrapped_label(rf"one asset, $\gamma = 1$, $\rho = 0.0005$ a day; value iteration on the quadratic value "
                             rf"function until it stops changing; largest gap {err:.0e}", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Is the formula right? The House checks it the slow way. <bookmark mark='a'/> Iterate the Bellman equation on "
            "a quadratic value function until it stops changing, and read off the trade rate and the aim weight. "
            "<bookmark mark='b'/> They agree with the closed form to every digit shown, for cheap and expensive trading "
            "and for slow and fast signals."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:3])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[3:])) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def multi(self):
        rows = [cmath(r"\text{cost}", r"=", r"\tfrac{\lambda}{2}\,\Delta x^\top\Sigma\,\Delta x", font_size=36,
                      colors={r"\text{cost}": COST_C}),
                cmath(r"x_t", r"=", r"\big(1 - \tfrac a\lambda\big)x_{t-1} + \tfrac a\lambda\,\text{aim}_t\quad"
                      r"\text{(the same scalar rate for every asset)}", font_size=30),
                cmath(r"\text{if}\ \Lambda \neq \lambda\Sigma", r":", r"\text{a matrix Riccati policy with coupled risk--liquidity modes}", font_size=30)]
        whys = [why(r"Garleanu and Pedersen's key modelling choice: costs proportional to risk, motivated by dealers who "
                    r"charge for the risk of the inventory they absorb"),
                why(r"then the trade rate is one number for the whole book, and every asset moves the same fraction of its "
                    r"gap"),
                why(r"a general cost matrix requires a matrix Riccati solution with coupled risk--liquidity modes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A special cost matrix makes the multi-asset policy simple. <bookmark mark='a'/> If the quadratic cost matrix is lambda times the fixed return covariance, all assets share a scalar adjustment rate. <bookmark mark='b'/> Each moves the same fraction of its gap toward the aim. <bookmark mark='c'/> With a general positive-definite cost matrix, risk and liquidity interact through a matrix Riccati equation. Its modes can mix assets; a simple asset-by-asset fast-versus-slow rule does not describe the general solution."
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

    def coins(self, g):
        hl, ph = g["half_life"], g["phi"]
        rows = [cmath(r"\text{slow}", r":", rf"\text{{calm (low 20-day volatility)}},\ \phi = {ph['slow']:.3f},\ "
                      rf"\text{{half-life}}\ {hl['slow']:.0f}\ \text{{days}}", font_size=28, colors={r"\text{slow}": GP_C}),
                cmath(r"\text{fast}", r":", rf"\text{{3-day reversal}},\ \phi = {ph['fast']:.2f},\ \text{{half-life}}\ "
                      rf"{hl['fast']:.1f}\ \text{{days}}", font_size=28, colors={r"\text{fast}": MYO_C}),
                cmath(r"\alpha_{i,t}", r"=", r"IC_k\,\bar\sigma\, z_{ik,t},\qquad \Sigma = \operatorname{diag}(\sigma^2_{i,t})",
                      font_size=30)]
        whys = [why(r"one minus average day-to-day cross-sectional Pearson score correlation; a geometric-persistence proxy"),
                why(r"the reversal signal is almost new every day; the calm signal barely changes in a week"),
                why(r"each signal's expected return per unit of score is Grinold's rule, with the IC fitted on 2018--19; a "
                    r"diagonal risk model, 60-day volatilities")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"""The saved research comparison uses two signals. <bookmark mark='a'/> Calm has persistence proxy phi {ph['slow']:.3f}, corresponding to geometric half-life {hl['slow']:.0f} days. <bookmark mark='b'/> Three-day reversal has proxy {ph['fast']:.3f}. These are derived from average cross-sectional Pearson score correlations, not fitted individual time-series autoregressions. <bookmark mark='c'/> Signal coefficients use training rank correlations and the full research period's volatility scale; persistence also uses the full research period. This comparison includes estimation data and is not a holdout test."""
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

    def table(self, g):
        rows = g["rows"]
        hx = [-4.8, -2.7, -0.6, 1.4, 3.3, 5.2]
        head = VGroup(label(r"cost $\lambda$", font_size=17, color=GREY_B), label(r"myopic Sharpe", font_size=17, color=MYO_C),
                      label(r"GP Sharpe", font_size=17, color=GP_C), label(r"trade rate", font_size=17, color=GREY_B),
                      label(r"fast weight", font_size=17, color=GREY_B), label(r"slow weight", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['lam']:g}", font_size=24),
                           MathTex(f"{r['myopic']:.2f}", font_size=24, color=BAD if r["myopic"] < 0 else WHITE),
                           MathTex(f"{r['gp']:.2f}", font_size=24, color=GOOD),
                           MathTex(f"{r['rate']:.2f}", font_size=24), MathTex(f"{r['w_fast']:.2f}", font_size=24),
                           MathTex(f"{r['w_slow']:.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.3 - 0.7 * j, 0])
        foot = wrapped_label(r"2018--2020, net of the quadratic cost model; Sharpe ratios annualised; the same signals and "
                             r"risk model for both traders", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.4)
        r8 = [r for r in rows if r["lam"] == 8][0]
        r32 = rows[-1]
        with self.voiceover(
            f"The saved research result as quadratic cost increases. <bookmark mark='a'/> In the near-free numerical limit the traders agree: {rows[0]['gp']:.2f}. <bookmark mark='b'/> As costs rise, the myopic trader, who "
            f"chases the Markowitz target every day, falls to {r8['myopic']:.2f} at lambda eight and {r32['myopic']:.2f} "
            f"at thirty-two. Garleanu and Pedersen's trader keeps {r8['gp']:.2f} and {r32['gp']:.2f}, by trading "
            f"{100 * r8['rate']:.0f} and then {100 * r32['rate']:.0f} percent of the way each day and cutting the fast "
            f"signal to {r32['w_fast']:.2f} of its weight."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"trade partially", r"with positive quadratic cost in this model, move partway toward the aim; the zero-cost limit is full trading", width=12.4, font_size=19),
            desk_question(r"aim in front", r"discount fast signals more than slow signals; both aim weights are at most one for positive decay rates", width=12.4, font_size=19),
            desk_question(r"where it is approximate", r"impact is model dependent and risk is estimated; convex multi-period models can add nonlinear costs and constraints, but retain estimation error",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three conditional lessons. <bookmark mark='a'/> With strictly positive quadratic costs, partial trading balances present and future objectives. The free-cost limit is full adjustment. <bookmark mark='b'/> Persistent signals receive greater relative weight than fast signals. With positive decay, neither weight exceeds its own raw Markowitz weight. <bookmark mark='c'/> Estimated risk, nonlinear impact and constraints require further modelling. A convex multi-period formulation accommodates some of those features, but does not remove estimation error."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in the negligible-discount, large-cost regime, quadratic cost quadruples. How do the approximate trade rate and fast-signal aim weight change?")
        with self.voiceover(
            "Pause and predict. Trading costs quadruple. Roughly how does the optimal trade rate change, and what happens "
            "to the weight of a fast signal in the aim?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
