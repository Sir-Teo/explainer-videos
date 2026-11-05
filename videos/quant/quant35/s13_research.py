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
        with self.voiceover(
            "The setup. <bookmark mark='a'/> A value v, known to the insider, revealed to everyone at time one. "
            "<bookmark mark='b'/> Total order flow: the insider trades at a rate theta, noise traders as a Brownian "
            "motion. <bookmark mark='c'/> The market maker sets the price to the expected value given the flow so far. "
            "<bookmark mark='d'/> And the insider's profit accumulates the gap between value and price on every unit it "
            "buys."
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
        with self.voiceover(
            "Lemma one, the market maker. <bookmark mark='a'/> Suppose the insider trades in proportion to the remaining "
            "mispricing. <bookmark mark='b'/> Then the market maker's problem is a Kalman-Bucy filter, Part seven's "
            "filter in continuous time: the price moves in proportion to the flow, with gain lambda. "
            "<bookmark mark='c'/> And the remaining uncertainty falls at a rate of lambda squared times the noise "
            "variance."
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
        whys = [why(r"Lemma 2 (Back 1992): guess the insider's value function, for a constant $\lambda$"),
                why(r"its derivatives"),
                why(r"at the end, the value left is the square of what was never traded on: money left on the table")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, the insider. <bookmark mark='a'/> Kerry Back's guess for the insider's value function, with a "
            "constant lambda: the squared mispricing, plus lambda squared sigma u squared times the time left, over two "
            "lambda. <bookmark mark='b'/> Its derivatives are simple. <bookmark mark='c'/> And at the end, what remains "
            "is the squared mispricing never traded on: money left on the table."
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
        rows = [cmath(r"0", r"=", r"\max_\theta\ \big[(v - p)\theta + J_p\,\lambda\theta\big] + J_t + \tfrac12 J_{pp}\lambda^2\sigma_u^2",
                      font_size=32),
                cmath(r"(v - p)\theta + J_p\lambda\theta", r"=", r"0\ \ \text{for every } \theta", font_size=32,
                      colors={r"0\ \ \text{for every } \theta": HURDLE}),
                cmath(r"J_t + \tfrac12 J_{pp}\lambda^2\sigma_u^2", r"=", r"-\tfrac{\lambda\sigma_u^2}{2} + "
                      r"\tfrac{\lambda\sigma_u^2}{2} = 0", font_size=32)]
        whys = [why(r"the Hamilton--Jacobi--Bellman equation of Part 8, for the profit rate plus the value's drift"),
                why(r"the terms in $\theta$ cancel exactly: the insider is indifferent to how fast it trades"),
                why(r"and the rest cancels too, so $J$ solves the equation; every strategy earns the same, provided it "
                    r"leaves nothing on the table at the end")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Check it in Part eight's Hamilton-Jacobi-Bellman equation. <bookmark mark='a'/> The profit rate plus the "
            "drift of the value function must be zero at the best rate of trade. <bookmark mark='b'/> The terms in theta "
            "cancel exactly: the insider is indifferent to how fast it trades. <bookmark mark='c'/> The rest cancels too. "
            "So every strategy earns the same, as long as it leaves nothing on the table: the price must reach the value "
            "by time one."
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

    def pin_down(self):
        rows = [cmath(r"\Sigma_1 = 0", r"\Rightarrow", r"\Sigma_0 - \lambda^2\sigma_u^2 = 0", font_size=36),
                cmath(r"\lambda", r"=", r"\frac{\sqrt{\Sigma_0}}{\sigma_u}", font_size=40, colors={r"\lambda": FLOW_C}),
                cmath(r"\theta_t", r"=", r"\frac{v - p_t}{\lambda\,(1 - t)}", font_size=38, colors={r"\theta_t": INF_C})]
        whys = [why(r"Lemma 3: with a constant $\lambda$, Lemma 1's variance falls linearly; it must reach zero at the end"),
                why(r"which fixes the price impact"),
                why(r"the strategy that makes the price arrive exactly: trade the remaining gap over the remaining time, "
                    r"and $\beta_t = 1/(\lambda(1 - t))$ is consistent with Lemma 1")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma three closes the loop. <bookmark mark='a'/> With a constant lambda, Lemma one's variance falls in a "
            "straight line, and it must reach zero at the end. <bookmark mark='b'/> That fixes lambda: the root of the "
            "initial variance over sigma u. <bookmark mark='c'/> And the strategy that brings the price exactly to the "
            "value is to trade the remaining gap over the remaining time, which is linear in the gap, as Lemma one "
            "assumed."
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
                    wrapped_label(r"in the market's eyes the price is a martingale with constant volatility $\sigma_v$; in "
                                  r"the insider's, a Brownian bridge from $p_0$ to $v$; the information comes out at a "
                                  r"constant rate, and trading over time doubles the insider's profit", 9.6, 20)).arrange(
            DOWN, buff=0.35)
        card = theorem_card(r"Kyle in continuous time (Kyle 1985; Back 1992)", st, r"this part's proof", width=11.8,
                            font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> Lambda is sigma v over sigma u; the insider trades the remaining gap over "
            "the remaining time; and the remaining uncertainty falls linearly to zero. <bookmark mark='b'/> The expected "
            "profit, the value function at the start averaged over v, is sigma v times sigma u: twice the one-auction "
            "profit. To the market, the price is a martingale with constant volatility; to the insider, it is a Brownian "
            "bridge that ends at the value."
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
                why(r"the insider hides perfectly: its trading leaves the flow's distribution unchanged, which is why "
                    r"$\lambda$ can be constant")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "One path, two views. <bookmark mark='a'/> To the market maker, the total flow looks exactly like noise: the "
            "price is a martingale, Part four's fair game. <bookmark mark='b'/> To the insider, who knows v, the same "
            "price has a drift pulling it to the value: a Brownian bridge. <bookmark mark='c'/> The insider hides "
            "perfectly. Its trading leaves the distribution of the flow unchanged, which is exactly why lambda can stay "
            "constant."
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
        with self.voiceover(
            "Four simulated markets. <bookmark mark='a'/> Each price wanders like a random walk, pushed by noise. "
            "<bookmark mark='b'/> And each ends exactly at its value, the dot, because the insider's trading pulls it "
            "there harder and harder as time runs out."
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
        with self.voiceover(
            "Across six hundred markets. <bookmark mark='a'/> The mean squared gap between value and price falls along "
            "the theorem's straight line, one minus t. <bookmark mark='b'/> And the insider's average profit is "
            f"{pr:.3f}, against the theorem's {prt:.0f}. Information leaks out at a constant rate, exactly as fast as the "
            "noise allows."
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
        with self.voiceover(
            "And Kyle's discrete recursion approaches it. <bookmark mark='a'/> With more auctions the first price impact "
            "rises toward one, the uncertainty halfway through toward one half, and the uncertainty at the end toward "
            "zero. The continuous theorem is the limit of the discrete game, as Kyle conjectured and Back proved."
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
                why(r"but its expected trading per unit time grows only like $1/(1-t)$, because the remaining mispricing "
                    r"shrinks at the same time"),
                why(r"over a horizon $T$, the noise traders have more time to hide the insider: impact falls, and profit "
                    r"grows with the root of the horizon")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Two refinements. <bookmark mark='a'/> The insider's intensity rises without bound as the end approaches. "
            "<bookmark mark='b'/> But the gap it trades on shrinks at the same time, so its expected trading grows only "
            "like one over the time remaining. <bookmark mark='c'/> And over a longer horizon the noise has more time to "
            "hide the insider: lambda falls with the root of the horizon, and the profit rises with it."
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
                why(r"the market maker breaks even, so the insider's gain is exactly the noise traders' loss; noise trading "
                    r"pays for the informativeness of prices")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Compared. <bookmark mark='a'/> One auction reveals half the information. <bookmark mark='b'/> Trading over "
            "time, the insider reveals all of it and still earns twice as much, because it never trades faster than the "
            "noise can hide. <bookmark mark='c'/> And the noise traders lose exactly what the insider gains: they pay for "
            "the informativeness of prices."
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
                cmath(r"1 - R^2", r"=", r"\text{price moves without trade: public information}", font_size=30,
                      colors={r"1 - R^2": BAD})]
        whys = [why(r"in the model every price change comes through order flow: the regression of returns on flow would "
                    r"fit perfectly"),
                why(r"Chapter 5's regressions: flow explains a fifth to a third of the variance"),
                why(r"the rest is public news that moves quotes before anyone trades: Chapter 9's sniping races, which "
                    r"Kyle's model leaves out")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A test against data. <bookmark mark='a'/> In Kyle's model every price change comes through order flow, so "
            "a regression of returns on flow would fit perfectly. <bookmark mark='b'/> On Bitcoin, Chapter five found "
            f"an R squared of {r1:.2f} at one minute and {r60:.2f} at an hour. <bookmark mark='c'/> The rest is public "
            "information that moves quotes before anyone trades: the sniping races of Chapter nine, which Kyle's model, "
            "with only private information, leaves out. The model explains the part of prices that is learned from "
            "trading, and the data say it is a fifth to a third."
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
            desk_question(r"Back (1992)", r"the continuous-time equilibrium for general value distributions, by the value "
                          r"function used here; the price is a Brownian bridge in the insider's filtration", width=12.4,
                          font_size=18),
            desk_question(r"Holden and Subrahmanyam (1992)", r"several competing insiders race to trade first, and almost "
                          r"all the information is revealed at once: competition destroys the gradual leak", width=12.4,
                          font_size=18),
            desk_question(r"Back and Baruch (2004)", r"the Kyle and Glosten--Milgrom models meet: a Glosten--Milgrom market "
                          r"with frequent small trades converges to Kyle's", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Kerry Back proved the continuous equilibrium for general value "
            "distributions, by the value function used here. <bookmark mark='b'/> Craig Holden and Avanidhar "
            "Subrahmanyam showed that several competing insiders race each other, and the information comes out almost "
            "at once. <bookmark mark='c'/> And Back and Shmuel Baruch connected the two models of this part: a Glosten-"
            "Milgrom market with frequent small trades becomes Kyle's."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: public and private information together", r"a tractable equilibrium with both public "
                          r"news (sniping) and gradual private information, matching Chapter 5's R squared, is not known",
                          width=12.4, font_size=18),
            desk_question(r"open: strategic liquidity traders", r"noise traders who time their trades, as Part 37's "
                          r"executors do, change what flow reveals; the general equilibrium is unsolved", width=12.4,
                          font_size=18),
            desk_question(r"open: many venues", r"an insider choosing among lit, dark and derivative markets (Chapter 7) "
                          r"with different depths; where information is revealed first has no closed form", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> A tractable equilibrium with both public news and gradual private "
            "information, that matches the R squared of Chapter five, is not known. <bookmark mark='b'/> Noise traders "
            "who time their trades, as optimal executors do, change what the flow reveals. <bookmark mark='c'/> And an "
            "insider choosing among lit, dark and derivative markets: where its information first shows up has no closed "
            "form."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in continuous Kyle, $\sigma_v = 2$ and $\sigma_u = 1$. What are $\lambda$, the price's volatility, "
                       r"and the insider's expected profit? How do they change if the horizon is four years, not one?")
        with self.voiceover(
            "Pause and predict. In continuous Kyle, sigma v is two and sigma u is one. What are lambda, the price's "
            "volatility, and the insider's expected profit? And how do they change if the horizon is four years, not one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
