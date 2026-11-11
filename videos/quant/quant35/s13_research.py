from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (BAD, DEALER_C, FLOW_C, GOOD, HURDLE, INF_C, NOISE_C, PART, PRICE_C, VALUE_C,
                                         fit_right, illustration, load)


class Research(VoiceoverScene):
    def construct(self):
        k = load("kyle")
        self.card()
        self.setup_()
        self.filter_()
        self.value()
        self.hjb()
        self.pin_down()
        self.theorem()
        self.views()
        self.bridge(k)
        self.variance(k)
        self.converge(k)
        self.intensity()
        self.compare(k)
        self.data(load("flow"))
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Kyle in continuous time", r"How does an insider who can trade at every instant reveal what it "
                          r"knows?", part=PART)
        self.add(c)
        with self.voiceover("For the researcher. Chapter three's recursion suggested a limit: as the auctions multiply, "
                            "the price impact settles and the remaining uncertainty falls in a straight line. This chapter "
                            "proves the limit in continuous time, following Kyle's 1985 paper and Kerry Back's 1992 "
                            "proof, and checks it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"v", r"\sim", r"N(p_0, \Sigma_0),\ \text{revealed at } t = 1", font_size=36, colors={r"v": VALUE_C}),
                cmath(r"dY_t", r"=", r"\theta_t\,dt + \sigma_u\,dW_t", font_size=38, colors={r"\theta_t": INF_C}),
                cmath(r"p_t", r"=", r"\mathbb E[v \mid Y_s, s \le t]", font_size=38, colors={r"p_t": PRICE_C}),
                cmath(r"\pi", r"=", r"\textstyle\int_0^1 (v - p_t)\,\theta_t\,dt", font_size=36)]
        whys = [why(r"one asset, its value known to the insider from the start"),
                why(r"total order flow: the insider trades at rate $\theta_t$, noise traders as Brownian motion"),
                why(r"a competitive market maker sets the price to the expected value given the flow so far"),
                why(r"the insider's profit: each unit bought at $p_t$ is worth $v$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "State the equilibrium problem precisely. <bookmark mark='a'/> Gaussian value has public prior mean p zero and positive variance; it is independent of the noise Brownian motion, and only the insider initially observes it. <bookmark mark='b'/> Noise variance per unit time is sigma u squared. The risk-neutral insider uses a predictable, absolutely continuous order process adapted to value and observed noise or prices, never future noise. <bookmark mark='c'/> Competitive risk-neutral dealers condition only on total flow. <bookmark mark='d'/> Profit is the time integral of mispricing times trading rate. Admissibility must make that profit integrable, the verification stochastic integral mean zero and the terminal limit justified. These are essential conditions, not consequences of a formal maximization."
        ) as vo:
            step(0)
            for k_, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k_:
                    step(k_)
        self.wait(0.5)
        self.clear_scene()

    def filter_(self):
        rows = [cmath(r"\theta_t", r"=", r"\beta_t\,(v - p_t)", font_size=38, colors={r"\beta_t": INF_C}),
                cmath(r"dp_t", r"=", r"\lambda_t\, dY_t,\qquad \lambda_t = \frac{\beta_t\,\Sigma_t}{\sigma_u^2}", font_size=34,
                      colors={r"\lambda_t": FLOW_C}),
                cmath(r"\frac{d\Sigma_t}{dt}", r"=", r"-\lambda_t^2\,\sigma_u^2", font_size=36)]
        whys = [why(r"Lemma 1: suppose the insider trades in proportion to the remaining mispricing"),
                why(r"then the market maker's problem is a Kalman--Bucy filter (Part 7, in continuous time): the price "
                    r"moves in proportion to the flow, with gain $\lambda_t$"),
                why(r"and the posterior variance $\Sigma_t = \operatorname{Var}(v \mid \mathcal F^Y_t)$ falls at the rate the "
                    r"filter learns")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Filtering within the linear Gaussian candidate. <bookmark mark='a'/> Take a deterministic locally regular trading coefficient beta times the remaining mispricing, on times strictly before the terminal horizon. <bookmark mark='b'/> The dealer's innovations process yields gain beta times posterior variance over noise variance, and price changes equal that gain times total flow. <bookmark mark='c'/> The Riccati equation makes posterior variance decline at gain squared times noise variance. This is conditional on the specified information structure and candidate strategy; it is not a filtering theorem for arbitrary real signed flow."
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

    def value(self):
        rows = [cmath(r"J(t, p)", r"=", r"\frac{(v - p)^2 + \lambda^2\sigma_u^2\,(1 - t)}{2\lambda}", font_size=36,
                      colors={r"J(t, p)": INF_C}),
                cmath(r"J_p", r"=", r"-\frac{v - p}{\lambda},\quad J_{pp} = \frac{1}{\lambda},\quad J_t = -\frac{\lambda\sigma_u^2}{2}",
                      font_size=32),
                cmath(r"J(1, p)", r"=", r"\frac{(v - p)^2}{2\lambda} \ge 0", font_size=34)]
        whys = [why("a candidate verification potential for a fixed positive price slope; its terminal value is a penalty, not the remaining horizon's literal payoff"),
                why(r"its derivatives"),
                why('the nonnegative terminal mispricing penalty vanishes under complete endpoint learning; admissibility and justified expectations are still required')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Fix a positive constant price slope for the deviation problem. <bookmark mark='a'/> Consider this quadratic verification potential, conditional on the insider's known value. <bookmark mark='b'/> Its derivatives cancel the trading-rate term in the formal HJB expression. <bookmark mark='c'/> At time one it is squared mispricing over twice lambda, a nonnegative penalty. It is not the literal terminal value function for arbitrary price: there is no trading time left then. The useful result is an upper bound on admissible expected profit, attained when this penalty vanishes. We prove that bound with Ito's identity."
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

    def hjb(self):
        rows = [
            cmath(r"dJ_t", r"=", r"-(v-p_t)\theta_t\,dt-\sigma_u(v-p_t)\,dW_t", font_size=32),
            cmath(r"\pi", r"=", r"J_0-J_1-\sigma_u\!\int_0^1(v-p_t)\,dW_t", font_size=32),
            cmath(r"\mathbb E\pi", r"=", r"\mathbb EJ_0-\mathbb EJ_1\le\mathbb EJ_0", font_size=34),
        ]
        whys = [why(r"Ito under the fixed rule $dp=\lambda\theta\,dt+\lambda\sigma_u\,dW$: the drift terms cancel except negative profit rate"),
                why(r"require $\mathbb E\int_0^1(v-p_t)^2dt<\infty$, integrable absolute profit and a justified terminal limit; the stochastic integral is then mean zero"),
                why(r"equality additionally requires zero terminal penalty. Formal cancellation does not make every arbitrary strategy admissible or optimal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover("Verification replaces a purely formal HJB claim. <bookmark mark='a'/> Apply Ito under the fixed constant-slope price rule. The potential's drift is minus the profit rate, and its noise term is minus sigma u times the gap. <bookmark mark='b'/> Integrate. Require finite expected integrated squared gap, integrable absolute profit and terminal convergence sufficient to pass expectations. The stochastic integral is square-integrable and has mean zero. Alternatively, localization needs justified limits, not just stopped identities. <bookmark mark='c'/> Expected profit equals initial potential minus nonnegative terminal penalty, hence is bounded above. Endpoint learning attains that bound within the admissible class. Pointwise cancellation alone proves neither admissibility nor optimality for an arbitrary rate.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def pin_down(self):
        rows = [cmath(r"\Sigma_1 = 0", r"\Rightarrow", r"\Sigma_0 - \lambda^2\sigma_u^2 = 0", font_size=36),
                cmath(r"\lambda", r"=", r"\frac{\sqrt{\Sigma_0}}{\sigma_u}", font_size=40, colors={r"\lambda": FLOW_C}),
                cmath(r"\theta_t", r"=", r"\frac{v - p_t}{\lambda\,(1 - t)}", font_size=38, colors={r"\theta_t": INF_C})]
        whys = [why(r"Lemma 3: with a constant $\lambda$, Lemma 1's variance falls linearly; it must reach zero at the end"),
                why(r"which fixes the price impact"),
                why(r"the strategy that makes the price arrive exactly: trade the remaining gap over the remaining time, "
                    r"and $\beta_t = 1/(\lambda(1 - t))$ is consistent with Lemma 1")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Close the equilibrium loop. <bookmark mark='a'/> Seek an admissible strategy with endpoint learning and a constant positive slope. The Gaussian filter then requires initial variance minus lambda squared sigma u squared to be zero at time one. <bookmark mark='b'/> Thus lambda is sigma v over sigma u. <bookmark mark='c'/> Beta equals one over lambda times remaining time. Its filtered variance is sigma v squared times remaining time, consistently giving the same gain. The bridge has finite expected integrated squared gap and finite expected absolute profit; its terminal gap converges in mean square to zero. These checks both validate pricing and attain the insider's upper bound. They hold despite a divergent integral of the squared trading rate."
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

    def theorem(self):
        st = VGroup(MathTex(r"\lambda = \frac{\sigma_v}{\sigma_u},\qquad \theta_t = \frac{v - p_t}{\lambda(1 - t)},\qquad "
                            r"\Sigma_t = \sigma_v^2(1 - t)", font_size=32),
                    MathTex(r"\mathbb E[\pi] = \frac{\Sigma_0 + \lambda^2\sigma_u^2}{2\lambda} = \sigma_v\sigma_u "
                            r"\quad (\text{one auction: } \tfrac12\sigma_v\sigma_u)", font_size=30),
                    wrapped_label('Gaussian value independent of Brownian noise, risk-neutral agents and admissible trading on the same unit horizon: posterior variance falls linearly; profit doubles the matched one-auction value. Shannon information is not released at a constant rate', 9.6, 20)).arrange(
            DOWN, buff=0.35)
        card = theorem_card(r"Kyle in continuous time (Kyle 1985; Back 1992)", st, 'specified Gaussian equilibrium; verification and filtering', width=11.8,
                            font_size=22)
        self.add(card)
        with self.voiceover(
            "The specified Gaussian equilibrium. <bookmark mark='a'/> Positive lambda is sigma v over sigma u; the trading rate is the remaining gap divided by lambda times remaining time. Conditional variance falls linearly to zero. <bookmark mark='b'/> Average the attained initial bound over the Gaussian value to obtain sigma v sigma u. That doubles one-auction profit only at the same horizon and total noise variance. To the market, price is a martingale with diffusion coefficient sigma v; conditional on value, it is a Brownian bridge. Linear variance decline does not mean constant Shannon-information release, which accelerates as remaining variance vanishes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def views(self):
        rows = [cmath(r"\text{the market}", r":", r"dp_t = \lambda\sigma_u\,d\hat W_t,\ \ \text{a martingale}", font_size=32,
                      colors={r"\text{the market}": PRICE_C}),
                cmath(r"\text{the insider}", r":", r"dp_t = \frac{v - p_t}{1 - t}\,dt + \lambda\sigma_u\,dW_t", font_size=32,
                      colors={r"\text{the insider}": INF_C}),
                cmath(r"\text{both}", r":", r"\text{the same path, two filtrations}", font_size=32)]
        whys = [why(r"to the market maker the total flow is indistinguishable from noise: its innovation $d\hat W$ is a "
                    r"Brownian motion, so the price is a fair game (Part 4)"),
                why(r"to the insider, who knows $v$, the same price has a drift pulling it to $v$: a Brownian bridge"),
                why("in this equilibrium, total flow is a noise-scaled Brownian motion in the dealer's filtration; this is not identification of real informed trades")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The filtration changes the description. <bookmark mark='a'/> Under the equilibrium prior mixture, total flow is sigma u times a Brownian motion in the market filtration, and price is a martingale there. <bookmark mark='b'/> The insider also knows the terminal value, so the same path has bridge drift pulling it toward that endpoint. <bookmark mark='c'/> These are consistent descriptions of one Gaussian equilibrium. The noise-like marginal flow law does not mean the insider does nothing, nor does it let an observer identify private information in real data. Constant impact was verified jointly with strategy and filtering."
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

    def bridge(self, k):
        t = np.asarray(k["bridge_t"], float)
        P = [np.asarray(p, float) for p in k["bridge_example"]]
        V = np.asarray(k["bridge_v"], float)
        lim = float(np.ceil(max(np.abs(np.concatenate(P)).max(), np.abs(V).max()) * 2) / 2)
        g = axes([0, 1], [-lim, lim], x_length=7.6, y_length=4.4, xlabel=r"time", ylabel=r"the price",
                 xticks=[0, 0.5, 1], yticks=[-lim, 0, lim], font_size=15).move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        cols = [QC.SPOT, QC.DELTA, QC.GAIN, QC.OPTION]
        lines = VGroup(*[curve(ax, t, P[i], cols[i], stroke_width=2.5) for i in range(len(P))])
        ends = VGroup(*[Dot(ax.c2p(1, V[i]), radius=0.08, color=cols[i]) for i in range(len(P))])
        ill = illustration(r"simulated: $\sigma_v = \sigma_u = 1$, 400 steps; dots are the values")
        self.add(g, lines[0], ill)
        with self.voiceover(
            "Four saved Euler paths with four hundred steps. <bookmark mark='a'/> They approximate the Gaussian bridge; the dots mark their true values. <bookmark mark='b'/> At the last Euler step the drift removes the prior gap, but a fresh noise increment remains. The final price equals value plus lambda sigma u times the square root of the step times a standard Normal draw. These finite-grid paths therefore do not end exactly on their dots. Exact endpoint learning is a continuous-time limit, not an identity of this numerical scheme."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(ends))
        self.wait(0.4)
        self.clear_scene()

    def variance(self, k):
        t = np.asarray(k["bridge_t"], float)
        var = np.asarray(k["bridge_var"], float)
        g = axes([0, 1], [0, 1.2], x_length=7.4, y_length=4.4, xlabel=r"time",
                 ylabel=r"$\mathbb E[(v - p_t)^2]$", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], font_size=15)
        g.move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, t, var, PRICE_C, stroke_width=3)
        c2 = DashedLine(ax.c2p(0, 1), ax.c2p(1, 0), color=HURDLE, stroke_width=2)
        leg = legend([(PRICE_C, r"600 simulated markets"), (HURDLE, r"theorem: $1 - t$")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        pr, prt = k["bridge_profit"], k["bridge_profit_theory"]
        st = label(rf"insider's profit: {pr:.3f} against {prt:.3f}", font_size=17, color=INF_C).next_to(leg, DOWN, buff=0.4)
        fit_right(st)
        self.add(g, c1, leg)
        with self.voiceover(
            f"""Six hundred saved simulated markets. <bookmark mark='a'/> The plotted mean squared gaps can be compared with one minus time. The sample mean has Monte Carlo error, and the Euler scheme has discretization error, including a nonzero final-step gap. <bookmark mark='b'/> Its average profit is {pr:.3f}, compared with theory {prt:.0f}. The original numerical profit prices each increment at its post-step price. It is an approximation, without a provided numerical error bound or confidence interval. This supports an illustration; the verification argument establishes the theorem."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def converge(self, k):
        m = k["multi"]
        hx = [-3.6, -0.8, 2.0, 4.6]
        head = VGroup(label(r"auctions $N$", font_size=17, color=GREY_B), label(r"$\lambda_1$", font_size=17, color=FLOW_C),
                      label(r"$\Sigma_{1/2}/\sigma_v^2$", font_size=17, color=GREY_B),
                      label(r"$\Sigma_1/\sigma_v^2$", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for n in ("1", "4", "16", "64", "256"):
            r = m[n]
            tab.add(VGroup(MathTex(n, font_size=24), MathTex(f"{r['lambda0']:.3f}", font_size=24),
                           MathTex(f"{r['Sigma_half']:.3f}", font_size=24), MathTex(f"{r['Sigma_end']:.4f}", font_size=24)))
        tab.add(VGroup(label(r"limit", font_size=20, color=HURDLE), MathTex(r"1", font_size=24), MathTex(r"0.5", font_size=24),
                       MathTex(r"0", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.62 * j, 0])
        self.add(tab[0], tab[1])
        with self.voiceover(
            "The saved discrete recursion. <bookmark mark='a'/> As auction count increases, initial impact approaches one and terminal conditional variance becomes smaller. The column at half-time uses interpolation between saved variance points; for one auction its interpolated value is not an additional mid-auction observation. The unit horizon and total noise variance are held fixed. These selected numerical cases illustrate convergence; a table alone is not a convergence proof or a bound on approximation error."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25))
        self.wait(0.4)
        self.clear_scene()

    def intensity(self):
        rows = [cmath(r"\beta_t", r"=", r"\frac{1}{\lambda(1 - t)}\ \to\ \infty\ \text{as } t \to 1", font_size=34,
                      colors={r"\beta_t": INF_C}),
                cmath(r"\mathbb E[\theta_t^2]\,dt", r"=", r"\beta_t^2\,\Sigma_t\,dt = \frac{\sigma_u^2}{1 - t}\,dt", font_size=32),
                cmath(r"T \ne 1", r":", r"\lambda = \frac{\sigma_v}{\sigma_u\sqrt T},\ \ \mathbb E\pi = \sigma_v\sigma_u\sqrt T",
                      font_size=32, colors={r"T \ne 1": HURDLE})]
        whys = [why(r"the insider's intensity rises without bound near the end, as the remaining time shrinks"),
                why("this is the squared rate's expectation, not signed or absolute trading: it diverges as $1/(1-t)$, whereas expected absolute rate grows as $1/\\sqrt{1-t}$ and is integrable"),
                why(r"over a horizon $T$, the noise traders have more time to hide the insider: impact falls, and profit "
                    r"grows with the root of the horizon")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "The singular rate needs care. <bookmark mark='a'/> Beta diverges near the endpoint, while mispricing shrinks. <bookmark mark='b'/> The displayed expectation is of squared trading rate: sigma u squared over remaining time. Its integral diverges, so requiring globally square-integrable rate would exclude this equilibrium. Expected absolute rate instead grows as inverse square root of remaining time and is integrable. The integrated squared gap and absolute profit satisfy the verification requirements. <bookmark mark='c'/> For horizon T with fixed noise variance rate, lambda is sigma v over sigma u square root T, and expected profit is sigma v sigma u square root T. If total noise variance were held fixed instead, that horizon comparison would change."
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

    def compare(self, k):
        rows = [cmath(r"\text{one auction}", r":", r"\lambda = \tfrac{\sigma_v}{2\sigma_u},\ \ \mathbb E[\pi] = \tfrac12\sigma_v"
                      r"\sigma_u,\ \ \Sigma_1 = \tfrac12\sigma_v^2", font_size=30),
                cmath(r"\text{continuous}", r":", r"\lambda = \tfrac{\sigma_v}{\sigma_u},\ \ \mathbb E[\pi] = \sigma_v\sigma_u,"
                      r"\ \ \Sigma_1 = 0", font_size=30, colors={r"\text{continuous}": GOOD}),
                cmath(r"\text{noise traders}", r":", r"\text{lose } \sigma_v\sigma_u \text{ in total}", font_size=30,
                      colors={r"\text{noise traders}": NOISE_C})]
        whys = [why(r"Chapter 3's single trade: half the information revealed"),
                why(r"trading over time, the insider reveals everything, and still earns twice as much"),
                why('under matched post-trade execution and competitive zero-profit accounting, expected noise loss equals insider gain; a pre-trade Ito convention is different')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Match both normalization and execution convention. <bookmark mark='a'/> One auction over a unit horizon with noise variance sigma u squared leaves half the value variance unrevealed. <bookmark mark='b'/> The admissible continuous Gaussian equilibrium at the same total noise variance reaches zero posterior variance and doubles expected insider profit. <bookmark mark='c'/> Noise losses equal that gain under the compatible post-trade discrete-auction limit and competitive zero-profit accounting. A naive pre-trade Ito integral is a different execution convention and cannot be substituted silently. This is an equilibrium accounting comparison, not the payoff from accelerating an arbitrary real trader."
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

    def data(self, f):
        r1, r60 = f["agg"]["1"]["r2"], f["agg"]["60"]["r2"]
        rows = [cmath(r"\text{Kyle}", r":", r"dp = \lambda\, dY\ \Rightarrow\ R^2 = 1", font_size=36,
                      colors={r"\text{Kyle}": HURDLE}),
                cmath(r"\text{Bitcoin}", r":", rf"R^2 = {r1:.2f}\ \text{{(1 minute)}},\ {r60:.2f}\ \text{{(1 hour)}}",
                      font_size=34, colors={r"\text{Bitcoin}": FLOW_C}),
                cmath(r"1 - R^2", r"=", '\\text{unexplained variance; causes not identified}', font_size=30,
                      colors={r"1 - R^2": BAD})]
        whys = [why(r"in the model every price change comes through order flow: the regression of returns on flow would "
                    r"fit perfectly"),
                why(r"Chapter 5's regressions: flow explains a fifth to a third of the variance"),
                why('residual variation can include quote/transaction differences, clock mismatch, nonlinear impact, public news and measurement error; no variance attribution is identified')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""A model-data distinction. <bookmark mark='a'/> Under the exact constant-slope model, price increments equal lambda times total-flow increments. An aligned regression of those same objects would fit perfectly. <bookmark mark='b'/> Our Bitcoin regression instead uses log returns between closes and an approximate dollar imbalance from minute bars, with R squared {r1:.2f} at one row and {r60:.2f} at sixty rows. <bookmark mark='c'/> Their residuals do not measure the share of public information. Transaction noise, missing bars, timing, nonlinear relationships and omitted variables also matter. This comparison identifies neither public-news variance nor the fraction learned through private trading."""
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

    def related(self):
        cards = VGroup(
            desk_question(r"Back (1992)", 'continuous-time equilibrium constructions beyond Gaussian values; the quadratic potential and literal price bridge shown here are specific to the Gaussian case', width=12.4,
                          font_size=25),
            desk_question(r"Holden and Subrahmanyam (1992)", r"several competing insiders race to trade first, and almost "
                          r"all the information is revealed at once: competition destroys the gradual leak", width=12.4,
                          font_size=25),
            desk_question(r"Back and Baruch (2004)", 'the cited strategic sequential-trade and continuous-flow models connect under particular assumptions and limits; frequency alone is insufficient', width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Related models require their own hypotheses. <bookmark mark='a'/> Back's continuous-time work treats more general value distributions; the quadratic potential and literal Gaussian price bridge here should not be copied unchanged to that setting. <bookmark mark='b'/> Holden and Subrahmanyam study competition among informed traders, changing how quickly information is revealed. <bookmark mark='c'/> Back and Baruch connect strategic sequential-trade and continuous-flow models under particular limits. Frequent small binary-value trades alone do not establish every claimed equivalence."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"extension: public and private signals", r"Specify timing, signal distributions and observations before seeking an equilibrium. A minute-regression residual is not a direct target for the public-news share.", width=12.4, font_size=25),
            desk_question(r"extension: strategic liquidity demand", r"Trading needs and deadlines make the noise law endogenous. Existing models study these choices; their conclusions depend on preferences and information.", width=12.4, font_size=25),
            desk_question(r"extension: multiple venues", r"Routing among lit, dark and derivative markets changes execution probability and inference. A useful research question needs a precise model and evidence design.", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover("Three extension questions, without claiming the literature has no answers. <bookmark mark='a'/> How do specified public signals interact with private learning? A regression residual alone does not calibrate that split. <bookmark mark='b'/> How do strategic liquidity traders change the noise process? Preferences, deadlines and observations matter. <bookmark mark='c'/> How does venue choice change execution and information revelation? These questions have existing research; any new contribution needs a precise scope and comparison with it.") as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.clear_scene()

    def question(self):
        eq = MathTex('\\sigma_v=2,\\quad\\sigma_u=1\\ \\mathrm{unit}/\\sqrt{\\mathrm{year}},\\quad T\\in\\{1,4\\}\\ \\mathrm{years}', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('Independent Gaussian value and Brownian noise, admissible continuous equilibrium. Derive lambda, instantaneous price diffusion and expected profit; hold noise variance rate fixed.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. Prior value standard deviation is two, and noise diffusion is one unit per square-root year. Compare one- and four-year horizons, holding that noise variance rate fixed. Derive lambda, the price diffusion coefficient and expected profit. Check the time and quantity units.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
