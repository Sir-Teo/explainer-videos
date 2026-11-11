from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
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
        self.refinement(r)
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
        whys = [why(r"positive continuous price; displayed driftless special case; local regularity and integrability assumed"),
                why(r"a pool arbitraged continuously holds whatever point of its curve is cheapest at the market price: "
                    r"its demand curve"),
                why(r"the pool's value, marked to the market"),
                why(r"the benchmark starts at $R_0=V(P_0)$; it follows the same token holdings, trading at "
                    r"the market price, self-financing")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Specify the model before the proof. <bookmark mark='a'/> Let price be a positive continuous semimartingale. The displayed driftless diffusion is a useful special case; a drift term would cancel from the loss identity too. Assume predictable locally integrable holdings and sufficient local smoothness of pool value. <bookmark mark='b'/> With instantaneous fee-free arbitrage, the pool chooses the minimum external-price value on its feasible curve, with a well-defined minimizing holding. <bookmark mark='c'/> Its marked value is price times token holdings plus numeraire holdings. <bookmark mark='d'/> Start the self-financing rebalancing portfolio at exactly the same value and let its gains be token holdings times the price increment. Expectation statements require additional martingale and integrability conditions."
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
            "Lemma one uses the pool's value function. <bookmark mark='a'/> It is the infimum over a price-independent feasible set of affine functions of the external price. <bookmark mark='b'/> An infimum of affine functions is concave. <bookmark mark='c'/> If the minimizing token holding is unique and the value function differentiable, the envelope theorem gives V prime equal to that holding. Without uniqueness, supergradients replace a single derivative and the smooth proof needs modification. The geometry explains the sign; it does not by itself guarantee all the regularity needed for Itô's formula."
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
                                  r"quadratic variation and local curvature, with common initial wealth; the "
                                  r"endpoint alone does not determine the loss", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Loss-versus-rebalancing (Milionis, Moallemi, Roughgarden and Zhang 2022)", st,
                            r"this part's proof", width=11.8, font_size=22)
        self.add(card)
        with self.voiceover(
            "The pathwise identity. <bookmark mark='a'/> With common initial wealth, smooth concave pool value and instantaneous fee-free arbitrage, rebalancing minus pool value equals minus one half the integral of V double prime against the continuous price's quadratic variation. For the displayed diffusion that is the integral of sigma squared P squared over two times the absolute derivative of token holdings. <bookmark mark='b'/> It is nondecreasing under these assumptions. It depends on the path and its price levels, not only the endpoint. Jumps introduce additional concavity gaps, and fee bands use different holdings; neither is covered by simply reusing the smooth continuous rate."
        ) as vo:
            vo.wait_until("a")
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
            "Apply Itô's formula, locally if necessary. <bookmark mark='a'/> The pool change is V prime times d P plus one half V double prime times d quadratic variation of P. <bookmark mark='b'/> Replace V prime by token holdings. Concavity makes V double prime nonpositive wherever it exists. <bookmark mark='c'/> The benchmark's gains are those same holdings times d P, so their entire stochastic integral cancels, including any finite-variation drift. Integrate from a common initial value. What remains is a nonnegative finite-variation process. It need not be deterministic; its coefficient can depend on the realized price path. A true-martingale expectation claim needs integrability beyond this local identity."
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
                why('at annual sigma 50\\%, the local normalized rate is 3.125\\% a year; realized return and finite-step losses are different')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Two local rates. <bookmark mark='a'/> Constant-product value is twice square root of k P, whose second derivative gives sigma squared V over eight. <bookmark mark='b'/> A concentrated position gives sigma squared L square root of P over four while strictly in range, and zero outside. Its first derivative is continuous at the boundaries; a piecewise smooth Itô formula applies without an extra local-time term from a derivative jump. <bookmark mark='c'/> At fifty percent annual volatility the instantaneous normalized full-range loss rate is three point one two five percent per year. That is a rate relative to current value, not the realized annual return or a fee-inclusive strategy forecast."
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
            "An exact discrete accounting check. <bookmark mark='a'/> Start a fee-free constant-product pool at external price P zero. The benchmark holds its initial token quantity through one price step and starts at the same value. Subtract the pool's value change from that holding's gains. <bookmark mark='b'/> The result is starting pool value over two times square root of the price ratio minus one, squared, for any positive ratio. <bookmark mark='c'/> For a conditionally martingale lognormal ratio with variance parameter sigma squared delta t, its conditional expectation is starting value times one minus exp of minus sigma squared delta t over eight. <bookmark mark='d'/> Divide by delta t and shrink the step to obtain the local continuous rate. A finite price doubling alone does not specify the variance parameter."
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

    def refinement(self, r):
        rows = r["refine"]
        title = label(r"One-step moments at smaller variance", font_size=32).to_edge(UP, buff=0.4)
        heads = [r"$m$", r"step sigma", r"Monte Carlo / rate", r"closed expectation / rate"]
        tab = VGroup(VGroup(*[label(h, font_size=18, color=GREY_B) for h in heads]))
        for row in rows:
            tab.add(VGroup(*[MathTex(v, font_size=26) for v in [str(row["m"]), f'{row["step_sigma"]:.3f}', f'{row["ratio"]:.4f}', f'{row["closed"]:.4f}']]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([[-4.9, -2.4, 0.8, 4.4][i], 1.9-0.8*j, 0])
        foot = wrapped_label(r"same 4,000,000 standard-normal draws rescaled at each $m$; not nested fixed-horizon paths", 12.0, 20, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover("A different check examines one-step moments. The unchanged calculation resets its generator and rescales the same four million standard-normal draws for each variance, while keeping the number of draws fixed. <bookmark mark='a'/> Step sigma falls from one to one eighth. The Monte Carlo column estimates the expected normalized one-step loss divided by sigma squared over eight. <bookmark mark='b'/> The closed expectation ratio is one minus exp of minus sigma squared over eight, divided by sigma squared over eight, approaching one as step variance shrinks. <bookmark mark='c'/> This is a moment comparison with sampling error. It is not a nested Brownian path, a fixed-horizon refinement experiment, or proof of pathwise convergence.") as vo:
            self.play(FadeIn(title), FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.wait(0.1)
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
                 ylabel=r"sum of local normalized loss fractions, \%", xticks=[1, 3, 6, 9, 12], yticks=[0, 0.25, 0.5],
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
            f"Check the discrete data comparison. <bookmark mark='a'/> On ether's twenty twenty-three minute closes, the sum of step losses divided by changing starting pool values is {lv['lvr_pct']:.2f} percent, versus {lv['rv8_pct']:.2f} percent for squared log increments over eight. Monthly normalized loss sums range from {lo:.2f} to {hi:.2f} percent in this sample. <bookmark mark='b'/> Exact discrete accounting needs positive prices and the stated rebalancing convention; interpreting squared log increments through the continuous rate uses a small-step approximation and continuous-price assumptions. Minute closes omit within-minute moves and can include market noise. Similar rounded totals do not independently validate those assumptions or establish an executable return."
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
                why(r"input fee $f$ gives log half-band $\gamma=-\log(1-f)$; $\gamma\approx f$ only for small fees"),
                why(r"the pool can only be traded when a block is produced"),
                why(r"in a block, if the gap is outside the band, an arbitrageur trades the pool to the band's edge, "
                    r"paying the fee; between blocks $z$ is a Brownian motion with volatility $\sigma$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Now use a separate stationary reset model. <bookmark mark='a'/> Mispricing z is log external price over pool price. Between blocks, assume z has driftless Brownian increments of scale sigma. This is a log-price assumption, distinct from a martingale price level. <bookmark mark='b'/> For proportional input fee f, the exact symmetric log half-band is gamma equal to minus log one minus f. The small-fee approximation replaces gamma by f. <bookmark mark='c'/> Blocks arrive independently at Poisson rate lambda. <bookmark mark='d'/> A block outside the band resets z to the nearest edge. Inside, nothing resets it. Fixed blocks, log drift, jumps, discrete liquidity and transaction costs change this model."
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
            "The stationary law for the stated reset model. <bookmark mark='a'/> Inside the band, zero drift and symmetry reduce the stationary equation to a second derivative of zero, giving constant density c. <bookmark mark='b'/> Outside, Poisson resets remove density at rate lambda, giving exponential tails with rate a equal to square root of two lambda divided by sigma. Continuity and probability-flux balance connect the tails to the interior at both edges. <bookmark mark='c'/> Normalization gives c equal to one over twice gamma plus twice over a. <bookmark mark='d'/> Independent Poisson arrivals see stationary time averages, so the pre-block outside probability is one over one plus a gamma. This is exact for this stationary driftless-log reset model; substituting proportional fee f for gamma is an approximation."
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
                    wrapped_label(r"leading-order comparison with fee-free LVR; fees alter trades and holdings. Reconcile "
                                  r"arbitrage profit, LP fees and benchmark shortfall in matching units; no exact finite-sample invariance", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Arbitrage with fees (Milionis, Moallemi and Roughgarden 2023)", st,
                            r"Lemma 3 proved here; the profit identity to leading order", width=11.8, font_size=22)
        self.add(card)
        with self.voiceover(
            "Separate probability from profit. <bookmark mark='a'/> In the driftless-log Poisson reset model, trade probability is one over one plus eta, with eta equal to log half-band times square root of two lambda over sigma. Replacing the log half-band by proportional fee is a small-fee approximation. Relating arbitrage profit to a fee-free continuous LVR rate is a leading-order result under the paper's regularity and scaling. <bookmark mark='b'/> A fee changes the pool's trades and holdings, so it does not leave every finite-sample benchmark loss unchanged. In our outside-curve fee simulator, fee-inclusive rebalancing shortfall can be reconciled with arbitrage profit, while fee-free discrete LVR is a different comparison denominator. No general exact invariance follows."
        ) as vo:
            vo.wait_until("a")
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
            f"Check the simulator's Poisson-clock comparisons with their assumptions visible. <bookmark mark='a'/> The research histogram uses diffusion scale {t['sigma']:.3f} per square root of one mean block unit. The plotted symmetric density assumes zero log drift, whereas the simulated exponential price has the negative half-variance log drift needed for a martingale level. Finite samples and window truncation also matter; close curves are an approximation check. <bookmark mark='b'/> At fee {100*t['fee']:.1f} percent, observed trade frequency is {t['p_trade']:.3f}, versus {t['theory']:.3f} using the proportional-fee approximation. The separate multi-fee experiment chooses eighty percent annual volatility and mean twelve-second blocks. Profit divided by fee-free discrete LVR is a different statistic from trade frequency."
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
            f"Change the block clock. Ethereum has twelve-second slots after the Merge, but some slots are missed and actual execution includes more than a clock. <bookmark mark='a'/> In the chosen fixed-block simulation at three-tenths-percent fee, arbitrage profit divided by fee-free discrete LVR is {f3['arb_lvr']:.3f}, versus {f3['theory']:.3f} for the Poisson small-fee benchmark. Fixed times and exponential waiting times have different overshoot distributions, so agreement is not required. This descriptive comparison does not validate actual Ethereum execution or identify an exact universal ordering of all fee effects."
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
            f"Use ether's actual minute-close path as an external input to the unchanged fee simulator. <bookmark mark='a'/> At three-tenths-percent fee, simulated arbitrage profit divided by the fee-free discrete loss sum is {f3['arb_lvr']:.2f}; relative to the displayed leading-order Brownian comparison it is about {ratio:.1f} times as large. <bookmark mark='b'/> That discrepancy is descriptive. Jumps, volatility clustering, log drift, sampling, finite fees and a changed pool state can all affect it. The close data do not isolate fat tails as the cause or prove that a Brownian theorem applies unchanged to this market. Fees are paid outside a fixed curve here and token fees are immediately valued in numeraire; native retained-fee compounding, gas and execution competition are omitted."
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
            desk_question(r"for liquidity providers", 'holding and rebalancing answer different questions; compare fees, loss, hedge costs and capital in matching units',
                          width=12.4, font_size=19),
            desk_question(r"for pool designers", 'fees and auctions can change trading, holdings and surplus allocation; the examples do not establish a universal recovery guarantee', width=12.4,
                          font_size=19),
            desk_question(r"for the House", 'idealized curvature loss is one component; a perpetual hedge also adds funding, basis, collateral and execution costs', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "What the accounting suggests. <bookmark mark='a'/> Compare LP performance with both holding and a clearly defined self-financing rebalancing benchmark. Under a continuous fee-free model, the loss is a curvature-weighted quadratic-variation integral; real fee-inclusive trading needs its own ledger. <bookmark mark='b'/> Fee and auction design can change trading incentives, activity and allocation. Neither a static fee nor an auction is proved to recover a fixed universal amount by the examples here. <bookmark mark='c'/> A perpetual hedge adds funding, basis, collateral and execution costs. Fees minus idealized LVR is one component, rather than a complete net LP investment return."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        self.add(cards[0])
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Milionis, Moallemi, Roughgarden and Zhang defined LVR and proved the "
            "rate; Milionis, Moallemi and Roughgarden added fees and blocks. <bookmark mark='b'/> Agostino Capponi and "
            "Ruizhe Jia studied the fee's trade-off between providers and arbitrageurs, and Andreas Lehar and Christine "
            "Parlour who provides liquidity on Uniswap. <bookmark mark='c'/> And Angeris, Chitra and coauthors developed "
            "the convex geometry of these markets, their oracles and their routing."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
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
        self.add(cards[0])
        with self.voiceover(
            "Three research directions, framed by the cited literature rather than claimed absent from all later work. <bookmark mark='a'/> Extend fee-band comparisons to jumps, state-dependent volatility and execution costs; separate their effects empirically instead of attributing every residual to tails. <bookmark mark='b'/> Compare dynamic fees and auctions of arbitrage rights with strategic participants and measurable LP welfare. <bookmark mark='c'/> Study routing among many pools with different fees and ranges, including liquidity migration and competition. Existing papers address parts of these questions; the lecture's simplified simulator does not settle the general problems or establish the latest frontier."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"a constant-product pool's volatility doubles, with the fee and block rate unchanged. What happens "
                       r"to its LVR, and to the share of it that arbitrageurs keep, if $\eta$ was 1?")
        with self.voiceover(
            "Pause and predict. A constant-product pool's volatility doubles, with the fee and the block rate unchanged. "
            "What happens to its loss-versus-rebalancing, and to the share of it arbitrageurs keep, if eta was one?"
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
