from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    FEE_C,
    HURDLE,
    PART,
    POOL_C,
    REBAL_C,
    SPOT_C,
    load,
)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        lv = load("lvr")
        fe = load("fees")
        self.card()
        self.setup_()
        self.envelope()
        self.monotone()
        self.theorem()
        self.proof()
        self.corollaries()
        self.discrete()
        self.check_sim(r)
        self.check_v3(r)
        self.check_eth(lv)
        self.fee_model()
        self.stationary()
        self.fee_theorem()
        self.check_poisson(r, fe)
        self.check_fixed(fe)
        self.check_eth_fees(fe)
        self.meaning()
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Loss-versus-rebalancing", r"What exactly does a pool pay to arbitrageurs, and what do fees "
                          r"recover?", part=PART)
        with self.voiceover("For the researcher. Chapter three measured the loss of a pool to arbitrageurs. This chapter "
                            "proves the formula behind it, due to Jason Milionis, Ciamac Moallemi, Tim Roughgarden and "
                            "Anthony Lee Zhang; derives the exact discrete version; proves how fees and block times decide "
                            "what arbitrageurs keep; and checks each result by simulation and on ether's real prices."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"dP_t", r"=", r"\sigma P_t\,dW_t", font_size=40, colors={r"dP_t": SPOT_C}),
                cmath(r"(x^*(P),\,y^*(P))", r"=", r"\arg\min\{P x + y : \varphi(x, y) = k\}", font_size=34,
                      colors={r"(x^*(P),\,y^*(P))": POOL_C}),
                cmath(r"V(P)", r"=", r"P\,x^*(P) + y^*(P)", font_size=40, colors={r"V(P)": POOL_C}),
                cmath(r"dR_t", r"=", r"x^*(P_t)\,dP_t", font_size=40, colors={r"dR_t": REBAL_C})]
        whys = [why(r"the market price, a martingale in the numeraire: what a centralised exchange shows"),
                why(r"a pool arbitraged continuously holds whatever point of its curve is cheapest at the market price: "
                    r"its demand curve"),
                why(r"the pool's value, marked to the market"),
                why(r"the rebalancing portfolio: the same holdings of the token at every instant, but bought and sold at "
                    r"the market price, self-financing")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> The market price follows a martingale with volatility sigma. "
            "<bookmark mark='b'/> A pool arbitraged continuously sits at the point of its curve that is cheapest at the "
            "market price: an arbitrageur would trade against any other point. That defines its holdings x star and y "
            "star of P. <bookmark mark='c'/> The pool's value is P x star plus y star. <bookmark mark='d'/> And the "
            "benchmark: a portfolio holding the same amount of the token at every instant, but trading at the market "
            "price. Its gains are x star times d P."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def envelope(self):
        rows = [cmath(r"V(P)", r"=", r"\min_{\varphi(x, y) = k}\,(P x + y)", font_size=40),
                cmath(r"\Rightarrow", r"\ ", r"V \text{ concave in } P", font_size=38),
                cmath(r"V'(P)", r"=", r"x^*(P)", font_size=44, colors={r"x^*(P)": POOL_C})]
        whys = [why(r"the value is a minimum, over the curve, of functions linear in $P$"),
                why(r"a minimum of linear functions is concave"),
                why(r"the envelope theorem: moving $P$ moves the minimiser, but to first order only the direct effect "
                    r"counts, and that is $x$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Lemma one. <bookmark mark='a'/> The pool's value is a minimum, over its curve, of functions that are linear "
            "in the price. <bookmark mark='b'/> So it is concave. <bookmark mark='c'/> And by the envelope theorem its "
            "derivative is the holding itself: V prime of P equals x star of P. To first order, a pool's value moves "
            "exactly like its holdings."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def monotone(self):
        rows = [cmath(r"V''(P)", r"=", r"x^{*\prime}(P) \le 0", font_size=44, colors={r"x^{*\prime}(P) \le 0": ARB_C}),
                cmath(r"P \uparrow", r"\Rightarrow", r"x^* \downarrow", font_size=42)]
        whys = [why(r"concavity says the holdings fall as the price rises"),
                why(r"a pool always sells the token into a rally and buys it in a fall: it trades against the move, at "
                    r"prices that are already stale")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Lemma two. <bookmark mark='a'/> The second derivative is the slope of the holdings, and concavity makes it "
            "negative or zero. <bookmark mark='b'/> A pool sells the token as its price rises and buys as it falls: it "
            "always trades against the move. That is the whole source of the loss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\text{LVR}_t \equiv R_t - V_t = \int_0^t \ell(P_s)\,ds,\qquad \ell(P) = "
                            r"\frac{\sigma^2 P^2}{2}\,\bigl|x^{*\prime}(P)\bigr| \ \ge 0", font_size=30),
                    wrapped_label(r"a pool loses to the rebalancing portfolio at a predictable, non-negative rate, set by "
                                  r"the variance and by how steeply its holdings respond to the price; nothing about the "
                                  r"path's end point enters", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Loss-versus-rebalancing (Milionis, Moallemi, Roughgarden and Zhang 2022)", st,
                            r"this part's proof", width=11.8, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The rebalancing portfolio minus the pool, called loss-versus-rebalancing, "
            "is the integral of a running rate: sigma squared P squared over two, times the absolute slope of the "
            "holdings. <bookmark mark='b'/> It is never negative, it accumulates at a predictable rate, and unlike "
            "impermanent loss it does not care where the path ends."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[0], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"dV", r"=", r"V'(P)\,dP + \tfrac12 V''(P)\,\sigma^2 P^2\,dt", font_size=38),
                cmath(r"", r"=", r"x^*(P)\,dP - \tfrac12\,|x^{*\prime}(P)|\,\sigma^2 P^2\,dt", font_size=38),
                cmath(r"dR - dV", r"=", r"\tfrac12\,\sigma^2 P^2\,|x^{*\prime}(P)|\,dt", font_size=40,
                      colors={r"dR - dV": ARB_C})]
        whys = [why(r"Itô's formula for the pool's value (Part 5)"),
                why(r"Lemma 1 for the first derivative, Lemma 2 for the sign of the second"),
                why(r"subtract the rebalancing portfolio's gains, $x^*\,dP$: the martingale parts cancel exactly, leaving "
                    r"the drift; integrate")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The proof is three lines. <bookmark mark='a'/> Itô's formula for the pool's value. <bookmark mark='b'/> "
            "Lemma one turns the first derivative into the holdings, and lemma two gives the second its sign. "
            "<bookmark mark='c'/> Subtract the rebalancing portfolio's gains: the random parts cancel exactly, and what "
            "is left is a pure drift, half sigma squared P squared times the slope. Integrate, and that is the theorem."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def corollaries(self):
        rows = [cmath(r"x^* = \sqrt{k/P}", r"\Rightarrow", r"\ell = \frac{\sigma^2}{8}\,V(P)", font_size=40,
                      colors={r"\ell = \frac{\sigma^2}{8}\,V(P)": ARB_C}),
                cmath(r"\text{concentrated on } [p_a, p_b]", r"\Rightarrow", r"\ell = \frac{\sigma^2}{4}\,L\sqrt P\ "
                      r"\text{inside, } 0 \text{ outside}", font_size=34),
                cmath(r"\sigma = 50\%", r"\Rightarrow", r"\tfrac{0.25}{8} = 3.1\%\ \text{a year}", font_size=38)]
        whys = [why(r"constant product: $|x^{*\prime}| = \tfrac12\sqrt k\,P^{-3/2}$, and $V = 2\sqrt{kP}$"),
                why(r"Uniswap v3: the same rate per unit of liquidity, but liquidity per dollar is multiplied by the "
                    r"range's capital efficiency"),
                why(r"a constant-product pool in a 50\%-volatility asset loses about 3\% of its value a year to "
                    r"arbitrage; fees must exceed that")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Two corollaries. <bookmark mark='a'/> For the constant-product pool the rate is sigma squared over eight, "
            "times the pool's value: Chapter three's formula. <bookmark mark='b'/> For a concentrated position it is "
            "sigma squared over four, times liquidity times root P, inside the range, and nothing outside. "
            "<bookmark mark='c'/> In numbers, at fifty percent volatility a constant-product pool loses about three "
            "percent of its value a year. Its fees must beat that."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def discrete(self):
        rows = [cmath(r"\Delta\text{LVR}", r"=", r"x_0\,(P_1 - P_0) - \bigl(V(P_1) - V(P_0)\bigr)", font_size=36),
                cmath(r"", r"=", r"\frac{V_0}{2}\,\Bigl(\sqrt{P_1/P_0} - 1\Bigr)^2", font_size=40,
                      colors={r"\frac{V_0}{2}\,\Bigl(\sqrt{P_1/P_0} - 1\Bigr)^2": ARB_C}),
                cmath(r"\mathbb E[\Delta\text{LVR}]", r"=", r"V_0\,\bigl(1 - e^{-\sigma^2\Delta t/8}\bigr)", font_size=38),
                cmath(r"", r"\to", r"\frac{\sigma^2}{8}\,V_0\,\Delta t", font_size=38)]
        whys = [why(r"one step of a constant-product pool: the rebalancing gain minus the pool's change, arbitraged once "
                    r"at the end"),
                why(r"with $V = 2\sqrt{kP}$ and $x_0 = \sqrt{k/P_0}$, the difference is a perfect square: exact, for any "
                    r"step"),
                why(r"for a lognormal step with mean one, $\mathbb E\sqrt{P_1/P_0} = e^{-\sigma^2\Delta t/8}$"),
                why(r"the continuous rate is the limit as blocks shrink")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "This part adds an exact discrete version. <bookmark mark='a'/> Over one step, with the pool arbitraged once "
            "at its end, the loss is the rebalancing gain minus the pool's change in value. <bookmark mark='b'/> For a "
            "constant-product pool it is a perfect square: half the value times root of the price ratio minus one, "
            "squared. Exact, for steps of any size. <bookmark mark='c'/> For a lognormal step its expectation is V times "
            "one minus e to the minus sigma squared delta t over eight, <bookmark mark='d'/> which tends to the "
            "continuous rate as the steps shrink."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check_sim(self, r):
        rows = [cmath(r"\text{simulated pool against arbitrageurs}", r":", rf"{r['sim']:.4f}", font_size=36,
                      colors={rf"{r['sim']:.4f}": ARB_C}),
                cmath(r"\textstyle\sum \frac{V}{2}(\sqrt R - 1)^2", r":", rf"{r['exact']:.4f}", font_size=36),
                cmath(r"\textstyle\sum \frac{\sigma^2}{8} V\,\Delta t", r":", rf"{r['cont']:.4f}", font_size=36,
                      colors={rf"{r['cont']:.4f}": HURDLE})]
        whys = [why(r"400,000 steps of a lognormal price, a constant-product pool traded to the market at each step by "
                    r"the House's arbitrage simulator"),
                why(r"the exact identity, step by step: equal to the simulation to rounding"),
                why(r"the continuous formula, within a few hundredths of a percent")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Check one: simulation. <bookmark mark='a'/> Four hundred thousand steps of a lognormal price, and a pool "
            "traded to the market at every step. <bookmark mark='b'/> The exact identity, summed step by step, matches "
            "the simulated loss to rounding. <bookmark mark='c'/> And the continuous formula is within "
            f"{100 * abs(r['ratio'] - 1):.2f} percent."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check_v3(self, r):
        v = r["v3"]
        rows = [cmath(r"\text{simulated}", r":", rf"{v['sim']:.3f}", font_size=40, colors={rf"{v['sim']:.3f}": ARB_C}),
                cmath(r"\textstyle\sum \frac{\sigma^2}{4} L\sqrt P\,\mathbf 1_{\text{in range}}\,\Delta t", r":",
                      rf"{v['theory']:.3f}", font_size=36, colors={rf"{v['theory']:.3f}": HURDLE})]
        whys = [why(rf"a concentrated position on $[60, 160]$ along the same path, which spent {100 * v['in_range']:.0f}\% "
                    r"of its steps in range"),
                why(r"the theorem's rate, switched off outside the range")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Check two: a concentrated position. <bookmark mark='a'/> A range from sixty to a hundred and sixty along the "
            f"same kind of path, in range {100 * v['in_range']:.0f} percent of the time. <bookmark mark='b'/> The "
            f"simulated loss and the theorem's rate, switched off outside the range, agree within "
            f"{100 * abs(v['sim'] / v['theory'] - 1):.1f} percent."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def check_eth(self, lv):
        months = lv["months"]
        g = axes([0.5, 12.5], [0, 0.5], x_length=7.4, y_length=3.8, xlabel=r"2023, by month",
                 ylabel=r"loss to arbitrage, \% of pool value", xticks=[1, 3, 6, 9, 12], yticks=[0, 0.25, 0.5],
                 font_size=16).move_to(LEFT * 1.2 + DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.36, height=max(ax.c2p(0, m["lvr_pct"])[1] - ax.c2p(0, 0)[1], 0.01),
                                  stroke_width=0, fill_color=ARB_C, fill_opacity=0.8)
                        .move_to(ax.c2p(i + 1, 0), aligned_edge=DOWN) for i, m in enumerate(months)])
        dots = VGroup(*[Dot(ax.c2p(i + 1, m["rv8_pct"]), radius=0.06, color=HURDLE) for i, m in enumerate(months)])
        leg = legend([(ARB_C, r"exact loss, minute by minute"), (HURDLE, r"realised variance / 8")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 2.2)
        lo = min(m["lvr_pct"] for m in months)
        hi = max(m["lvr_pct"] for m in months)
        with self.voiceover(
            "Check three: ether in twenty twenty-three, the pause's pool. <bookmark mark='a'/> Minute by minute, the "
            f"pool lost {lv['lvr_pct']:.2f} percent of its value to arbitrage over the year, against "
            f"{lv['rv8_pct']:.2f} percent from realised variance over eight: equal month by month, from "
            f"{lo:.2f} percent in a calm month to {hi:.2f} "
            "in March. <bookmark mark='b'/> The formula needs no model of the price at all: only its realised variance "
            "at the frequency the pool is arbitraged."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(dots))
            vo.wait_until("b")
            self.play(Indicate(dots, color=HURDLE, scale_factor=1.2))
        self.wait(0.4)
        self.clear_scene()

    def fee_model(self):
        rows = [cmath(r"z_t", r"=", r"\log(p_t / P_t)", font_size=42, colors={r"z_t": ARB_C}),
                cmath(r"|z| \le \gamma", r":", r"\text{no trade}", font_size=40, colors={r"\text{no trade}": FEE_C}),
                cmath(r"\text{blocks}", r"\sim", r"\text{Poisson}(\lambda)", font_size=40),
                cmath(r"|z| > \gamma", r"\Rightarrow", r"z \to \pm\gamma", font_size=40)]
        whys = [why(r"the mispricing: market price against the pool's own, in logs"),
                why(r"with a fee $\gamma$ an arbitrageur gains nothing until the gap exceeds the fee"),
                why(r"the pool can only be traded when a block is produced"),
                why(r"in a block, if the gap is outside the band, an arbitrageur trades the pool to the band's edge, "
                    r"paying the fee; between blocks $z$ is a Brownian motion with volatility $\sigma$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Now fees and blocks, after Milionis, Moallemi and Roughgarden. <bookmark mark='a'/> Let z be the "
            "mispricing, the log of the market price over the pool's. <bookmark mark='b'/> Inside a band of width gamma, "
            "the fee, no arbitrage pays. <bookmark mark='c'/> The pool can only be traded when a block arrives, at Poisson "
            "rate lambda. <bookmark mark='d'/> If a block finds z outside the band, an arbitrageur trades the pool back "
            "to the band's edge. Between blocks, z wanders as a Brownian motion."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def stationary(self):
        rows = [cmath(r"|z| < \gamma", r":", r"\tfrac{\sigma^2}{2} f'' = 0 \Rightarrow f = c", font_size=36),
                cmath(r"|z| > \gamma", r":", r"\tfrac{\sigma^2}{2} f'' = \lambda f \Rightarrow f = c\,e^{-a(|z| - \gamma)},\ "
                      r"a = \tfrac{\sqrt{2\lambda}}{\sigma}", font_size=32),
                cmath(r"\int f", r"=", r"2c\gamma + \tfrac{2c}{a} = 1", font_size=38),
                cmath(r"P_{\text{trade}}", r"=", r"\int_{|z| > \gamma} f = \frac{1}{1 + \gamma\sqrt{2\lambda}/\sigma}",
                      font_size=36, colors={r"P_{\text{trade}}": ARB_C})]
        whys = [why(r"inside the band nothing removes probability, and the reinjected mass sits at the edges: the "
                    r"density is flat, by symmetry"),
                why(r"outside, mass is removed at rate $\lambda$ (a block resets it to the edge): exponential tails, "
                    r"continuous at the edge"),
                why(r"normalise"),
                why(r"a block sees the stationary law (Poisson arrivals see time averages), so the probability that a "
                    r"block holds an arbitrage is the mass outside the band")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Lemma three: the mispricing's stationary law. <bookmark mark='a'/> Inside the band nothing removes "
            "probability, so the density is flat. <bookmark mark='b'/> Outside, every block removes mass at rate lambda "
            "and returns it to the edge, so the density decays exponentially, at rate root two lambda over sigma. "
            "<bookmark mark='c'/> Normalise. <bookmark mark='d'/> Poisson arrivals see time averages, so the chance that "
            "a block finds an arbitrage is the mass outside the band: one over one plus gamma root two lambda over "
            "sigma."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def fee_theorem(self):
        st = VGroup(MathTex(r"P_{\text{trade}} = \frac{1}{1 + \eta},\quad \eta = \frac{\gamma\sqrt{2\lambda}}{\sigma},\qquad "
                            r"\text{ARB} \approx P_{\text{trade}} \times \text{LVR}", font_size=32),
                    wrapped_label(r"fees do not reduce the loss to the rebalancing portfolio; they split it between "
                                  r"arbitrageurs and the pool's own fee income. Faster blocks or a lower fee hand more of "
                                  r"it to arbitrageurs", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Arbitrage with fees (Milionis, Moallemi and Roughgarden 2023)", st,
                            r"Lemma 3 proved here; the profit identity to leading order", width=11.8, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The trade probability is one over one plus eta, where eta is gamma root "
            "two lambda over sigma. And arbitrageurs' profit is, to leading order, that probability times LVR. "
            "<bookmark mark='b'/> So fees do not shrink the loss to the rebalancing portfolio: they split it between "
            "arbitrageurs and the pool's own fee income. Faster blocks, or a lower fee, hand more of it to arbitrageurs."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.02))
        self.wait(0.5)
        self.clear_scene()

    def check_poisson(self, r, fe):
        t = r["trade"]
        zc = np.asarray(t["zc"], float)
        hist = np.asarray(t["hist"], float)
        dens = np.asarray(t["dens"], float)
        band = t["band"]
        top = float(max(hist.max(), dens.max()) * 1.1)
        g = axes([-4, 4], [0, top], x_length=6.2, y_length=3.6, xlabel=r"mispricing $z$, in units of the fee band",
                 ylabel=r"density", xticks=[-4, -1, 0, 1, 4], yticks=[], font_size=16).move_to(LEFT * 2.6 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.06, height=max(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                  fill_color=ARB_C, fill_opacity=0.7).move_to(ax.c2p(z / band, 0), aligned_edge=DOWN)
                        for z, h in zip(zc, hist)])
        th = curve(ax, zc / band, dens, HURDLE, stroke_width=3)
        hx = [2.2, 3.8, 5.4, 6.6]
        head = VGroup(*[label(s_, font_size=14, color=GREY_B) for s_ in (r"fee", r"$P_{\text{trade}}$", r"theory",
                                                                         r"ARB/LVR")])
        tab = VGroup(head)
        for x in fe["poisson"]:
            tab.add(VGroup(MathTex(rf"{100 * x['fee']:g}\%", font_size=22), MathTex(f"{x['p_trade']:.3f}", font_size=22,
                                                                                    color=ARB_C),
                           MathTex(f"{x['theory']:.3f}", font_size=22, color=HURDLE),
                           MathTex(f"{x['arb_lvr']:.3f}", font_size=22, color=FEE_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i] - 0.4, 2.0 - 0.6 * j, 0])
        with self.voiceover(
            "Check four: Poisson blocks in simulation, at eighty percent volatility and twelve-second blocks on average. "
            "<bookmark mark='a'/> The measured mispricing just before each block: flat inside the fee band, "
            "exponential outside, exactly lemma three's density. <bookmark mark='b'/> Across fees from a hundredth of a "
            f"percent to one percent, the share of blocks with a trade matches the formula; at three tenths of a percent, "
            f"{t['p_trade']:.3f} against {t['theory']:.3f} in the research run. And arbitrage profit over LVR tracks it "
            "almost exactly."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.01), Create(th))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def check_fixed(self, fe):
        hx = [-4.2, -1.6, 1.0, 3.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"fee", r"$P_{\text{trade}}$, fixed blocks",
                                                                         r"Poisson theory", r"ARB/LVR, fixed")])
        tab = VGroup(head)
        for x in fe["fixed"]:
            tab.add(VGroup(MathTex(rf"{100 * x['fee']:g}\%", font_size=26), MathTex(f"{x['p_trade']:.3f}", font_size=26,
                                                                                    color=ARB_C),
                           MathTex(f"{x['theory']:.3f}", font_size=26, color=HURDLE),
                           MathTex(f"{x['arb_lvr']:.3f}", font_size=26, color=FEE_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.72 * j, 0])
        f3 = [x for x in fe["fixed"] if abs(x["fee"] - 0.003) < 1e-9][0]
        with self.voiceover(
            "But Ethereum's blocks are not Poisson: since twenty twenty-two they come every twelve seconds, like a clock. "
            "<bookmark mark='a'/> With fixed blocks, trades are a little more frequent than the Poisson formula, and "
            f"arbitrageurs keep less: at three tenths of a percent, {f3['arb_lvr']:.3f} of LVR against the formula's "
            f"{f3['theory']:.3f}. A regular clock gives the mispricing less time to run far outside the band."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def check_eth_fees(self, fe):
        hx = [-4.2, -1.6, 1.0, 3.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"fee", r"$P_{\text{trade}}$, ETH minutes",
                                                                         r"GBM theory", r"ARB/LVR, ETH")])
        tab = VGroup(head)
        for x in fe["eth"]:
            tab.add(VGroup(MathTex(rf"{100 * x['fee']:g}\%", font_size=26), MathTex(f"{x['p_trade']:.3f}", font_size=26,
                                                                                    color=ARB_C),
                           MathTex(f"{x['theory']:.3f}", font_size=26, color=HURDLE),
                           MathTex(f"{x['arb_lvr']:.3f}", font_size=26, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.72 * j, 0])
        f3 = [x for x in fe["eth"] if abs(x["fee"] - 0.003) < 1e-9][0]
        ratio = f3["arb_lvr"] / f3["theory"]
        with self.voiceover(
            "Check five: ether's real minutes in twenty twenty-three, a pool arbitraged once a minute. "
            "<bookmark mark='a'/> Trades are rarer than the Brownian formula predicts, but arbitrageurs keep far more: at "
            f"three tenths of a percent, {f3['arb_lvr']:.2f} of LVR, about {ratio:.1f} times the formula. "
            "<bookmark mark='b'/> Real prices are calm most minutes and jump in a few, and a jump carries the mispricing "
            "far outside the band, where every tick of it is profit. The Brownian theorem is exact for Brownian prices; "
            "on real ones it understates what arbitrageurs take, and overstates what fees give back."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r_[3] for r_ in tab[1:]]), color=BAD, scale_factor=1.1))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        cards = VGroup(
            desk_question(r"for liquidity providers", r"the right benchmark is LVR, not impermanent loss: compare fee "
                          r"income with $\sigma^2/8$ of value, at the arbitrage frequency, and with fat tails in mind",
                          width=12.4, font_size=19),
            desk_question(r"for pool designers", r"a fee only reallocates the loss; to reduce it, auction the right to "
                          r"arbitrage, or let the fee rise with volatility, as Uniswap v4's hooks allow", width=12.4,
                          font_size=19),
            desk_question(r"for the House", r"hedging a pool's token exposure with a perpetual leaves exactly LVR minus "
                          r"fees: a short position in variance, Part 11's gamma, written on chain", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What it means. <bookmark mark='a'/> For liquidity providers, the benchmark is LVR, not impermanent loss: "
            "fee income against sigma squared over eight of value, measured at the frequency of arbitrage, and with fat "
            "tails in mind. <bookmark mark='b'/> For pool designers, a fee only reallocates the loss; reducing it means "
            "auctioning the right to arbitrage, or a fee that rises with volatility. <bookmark mark='c'/> And for the "
            "House: a pool hedged with a perpetual earns fees minus LVR, a short position in variance. It is Part "
            "eleven's short gamma, written on a blockchain."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"the measure", r"Milionis, Moallemi, Roughgarden and Zhang (2022) defined LVR and proved the "
                          r"rate; Milionis, Moallemi and Roughgarden (2023) added fees and discrete blocks", width=12.4,
                          font_size=19),
            desk_question(r"the economics", r"Capponi and Jia (2021) on the fee's trade-off between providers and "
                          r"arbitrageurs; Lehar and Parlour on who provides liquidity on Uniswap and why", width=12.4,
                          font_size=19),
            desk_question(r"the geometry", r"Angeris, Chitra and coauthors on constant-function market makers as convex "
                          r"objects, their oracles and their optimal routing", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Milionis, Moallemi, Roughgarden and Zhang defined LVR and proved the "
            "rate; Milionis, Moallemi and Roughgarden added fees and blocks. <bookmark mark='b'/> Agostino Capponi and "
            "Ruizhe Jia studied the fee's trade-off between providers and arbitrageurs, and Andreas Lehar and Christine "
            "Parlour who provides liquidity on Uniswap. <bookmark mark='c'/> And Angeris, Chitra and coauthors developed "
            "the convex geometry of these markets, their oracles and their routing."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"fat tails", r"the trade probability and arbitrageurs' share when prices jump: what replaces "
                          r"$1/(1 + \eta)$ for a L\'evy process, and how should the fee depend on it?", width=12.4,
                          font_size=19),
            desk_question(r"the optimal mechanism", r"a pool that recovers LVR by auctioning the arbitrage right each "
                          r"block, or by dynamic fees: what is the best a pool can do against informed flow?",
                          width=12.4, font_size=19),
            desk_question(r"many pools, many venues", r"LVR when the same pair trades in many pools with different fees "
                          r"and ranges, and arbitrageurs route across them", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Fat tails: what replaces one over one plus eta when prices jump, "
            "as check five showed they do, and how should the fee respond? <bookmark mark='b'/> The best mechanism: a "
            "pool that auctions the right to arbitrage each block, or sets its fee dynamically. What is the most a pool "
            "can recover? <bookmark mark='c'/> And many pools at once: the same pair in pools with different fees and "
            "ranges, with arbitrageurs routing across all of them."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a constant-product pool's volatility doubles, with the fee and block rate unchanged. What happens "
                       r"to its LVR, and to the share of it that arbitrageurs keep, if $\eta$ was 1?")
        with self.voiceover(
            "Pause and predict. A constant-product pool's volatility doubles, with the fee and the block rate unchanged. "
            "What happens to its loss-versus-rebalancing, and to the share of it arbitrageurs keep, if eta was one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
