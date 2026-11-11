from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
from videos.quant.quant39.common import (
    ARB_C,
    FEE_C,
    HURDLE,
    PART,
    POOL_C,
    REBAL_C,
    fit_right,
    load,
)


class LVR(VoiceoverScene):
    def construct(self):
        lv = load("lvr")
        self.card(lv)
        self.benchmarks()
        self.paths(lv)
        self.decompose(lv)
        self.why_rebal()
        self.formula(lv)
        self.by_freq(lv)
        self.breakeven(lv)
        self.gamma()
        self.question()

    def card(self, lv):
        c = chapter_card(3, r"What liquidity providers lose", r"Is impermanent loss the right measure of an LP's cost?",
                         part=PART)
        with self.voiceover(
            f"Chapter three. On the minute grid, the sum of exact step losses divided by each step's starting pool value is {lv['lvr_pct']:.1f} percent. This changing-denominator sum is not a total return on initial capital. Impermanent loss compares the endpoint with holding initial assets; loss-versus-rebalancing uses a different self-financing benchmark. We need both comparisons and their assumptions."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def benchmarks(self):
        rows = [cmath(r"\text{hold}", r":", r"x_0 P_t + y_0", font_size=40),
                cmath(r"\text{pool}", r":", r"x^*(P_t)\,P_t + y^*(P_t)", font_size=40, colors={r"\text{pool}": POOL_C}),
                cmath(r"\text{rebalance}", r":", r"\text{hold } x^*(P_t),\ \text{trade at } P_t", font_size=38,
                      colors={r"\text{rebalance}": REBAL_C})]
        whys = [why(r"the assets the provider started with, simply kept"),
                why(r"the pool: it sells the token as it rises and buys as it falls, at its own stale price"),
                why(r"Milionis, Moallemi, Roughgarden and Zhang's benchmark: the same holdings as the pool at every "
                    r"instant, but every adjustment made at the market price")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Three portfolios. <bookmark mark='a'/> Hold: the starting assets, kept. <bookmark mark='b'/> The pool, "
            "which sells the token as it rises and buys as it falls, at its own stale price. <bookmark mark='c'/> And "
            "the rebalancing portfolio of Jason Milionis, Ciamac Moallemi, Tim Roughgarden and Anthony Lee Zhang: the "
            "same holdings as the pool at every instant, but every adjustment made at the market price."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def paths(self, lv):
        pth = lv["path"]
        d = np.asarray(pth["day"], float)
        g = axes([0, 365], [0.9, 1.6], x_length=7.4, y_length=4.2, xlabel=r"2023, days",
                 ylabel=r"value, start = 1", xticks=[0, 90, 180, 270, 365], yticks=[1.0, 1.2, 1.4, 1.6],
                 font_size=16).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        cs = [curve(ax, d, np.asarray(pth[k], float), c, stroke_width=2.5)
              for k, c in (("hold", GREY_B), ("rebal", REBAL_C), ("lp", POOL_C))]
        leg = legend([(GREY_B, rf"hold: {pth['hold'][-1]:.3f}"), (REBAL_C, rf"rebalance: {pth['rebal'][-1]:.3f}"),
                      (POOL_C, rf"pool: {pth['lp'][-1]:.3f}")], font_size=18)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.8)
        fit_right(leg)
        with self.voiceover(
            "Ether in twenty twenty-three, a constant-product pool with no fee, arbitraged to Binance's price every ten "
            f"minutes. <bookmark mark='a'/> Holding the starting assets ended at {pth['hold'][-1]:.3f} of the start. "
            f"<bookmark mark='b'/> The rebalancing portfolio, at {pth['rebal'][-1]:.3f}. <bookmark mark='c'/> The pool, "
            f"at {pth['lp'][-1]:.3f}: below both, and the gap to the rebalancing portfolio widens steadily, through calm "
            "and rally alike."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), Create(cs[0]))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), Create(cs[1]))
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.play(FadeIn(leg[2]), Create(cs[2]))
        self.wait(0.4)
        self.clear_scene()

    def decompose(self, lv):
        pth = lv["path"]
        il = pth["lp"][-1] - pth["hold"][-1]
        lvr = pth["rebal"][-1] - pth["lp"][-1]
        mk = pth["rebal"][-1] - pth["hold"][-1]
        rows = [cmath(r"\text{pool} - \text{hold}", r"=", rf"{il:+.3f}", font_size=40, colors={rf"{il:+.3f}": GREY_A}),
                cmath(r"\text{pool} - \text{rebalance}", r"=", rf"{-lvr:+.3f}", font_size=40, colors={rf"{-lvr:+.3f}": ARB_C}),
                cmath(r"\text{rebalance} - \text{hold}", r"=", rf"{mk:+.3f}", font_size=40)]
        whys = [why('pool-minus-hold in initial-value units; divide by terminal hold value for standard relative impermanent loss'),
                why('common initial value and previous-step holdings define this fee-free discrete benchmark gap'),
                why(r"the market part: the pool's falling ether holdings missed some of the rally; a choice of exposure, "
                    r"not a cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"Take differences in units of initial value. <bookmark mark='a'/> Pool minus hold is {il:+.3f}; divide this gap by terminal hold value to recover the standard relative impermanent-loss percentage. <bookmark mark='b'/> Pool minus the common-initial-value rebalancing portfolio is {-lvr:+.3f}. On this grid, the benchmark holds the pool's previous-step token amount over each external price move, without fees. <bookmark mark='c'/> Rebalancing minus hold is {mk:+.3f}, an exposure difference. Hedging it in practice adds funding, execution, collateral and timing costs; the accounting decomposition alone does not make those costs disappear."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def why_rebal(self):
        cards = VGroup(
            desk_question(r"it can be hedged away", 'ideal frictionless token hedging isolates the benchmark gap; real perpetual hedges add funding, basis and execution costs', width=12.4, font_size=19),
            desk_question(r"it is predictable", 'under continuous assumptions, a path-dependent curvature rate accumulates; the endpoint alone does not determine the loss', width=12.4, font_size=19),
            desk_question(r"it is someone's income", 'arbitrage profits, fees and ordering payments need separate ledgers and a specified trading mechanism', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Why use this benchmark? <bookmark mark='a'/> With common initial wealth, the self-financing rebalancing portfolio follows the pool's token holdings while trading at the external price. In an ideal continuous, frictionless model, offsetting that token exposure isolates the loss term. <bookmark mark='b'/> The continuous loss depends on the whole path through volatility and the pool's curvature; an endpoint alone does not determine it. With jumps or discrete trading, finite-step terms matter. <bookmark mark='c'/> Arbitrage profits, fees and ordering payments are related but distinct ledgers. Their equality needs a specified mechanism and common units, rather than a general claim that every measured loss has one recipient."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formula(self, lv):
        rows = [cmath(r"\frac{d\,\text{LVR}}{dt}", r"=", r"\frac{\sigma^2}{8}\,V", font_size=48, colors={r"\frac{\sigma^2}{8}\,V": ARB_C}),
                cmath(r"\text{ETH, 2023}", r":", rf"\sigma = {100 * lv['vol']:.0f}\%,\ \ \sigma^2/8 = {lv['rv8_pct']:.2f}\%", font_size=38),
                cmath(r"\text{measured}", r":", rf"{lv['lvr_pct']:.2f}\%", font_size=40, colors={r"\text{measured}": POOL_C})]
        whys = [why(r"the constant-product rate, proved in the research chapter: variance over eight, times the pool's "
                    r"value, per unit of time"),
                why(r"ether's realised volatility from 2023's minutes"),
                why('computed local normalized sum; similar rounded values do not independently validate the continuous assumptions')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"For a smooth fee-free constant-product pool arbitraged continuously against a continuous semimartingale price, the local loss rate is variance over eight times current pool value. <bookmark mark='a'/> Realized squared log increments on ether's selected twenty twenty-three grid give a volatility scale of {100 * lv['vol']:.0f} percent. <bookmark mark='b'/> Their sum divided by eight is {lv['rv8_pct']:.2f} percent. <bookmark mark='c'/> The sum of exact discrete losses normalized by each starting pool value is {lv['lvr_pct']:.2f} percent. Close numbers describe a small-increment relation on this sample; they neither establish a continuous price model nor represent a compounded LP return."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def by_freq(self, lv):
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"arbitraged every", 'sum local loss fractions, \\%',
                                                                         r"realised volatility")])
        tab = VGroup(head)
        for r in lv["by_freq"]:
            tab.add(VGroup(label(r["freq"], font_size=20), MathTex(f"{r['lvr_pct']:.2f}", font_size=28, color=ARB_C),
                           MathTex(rf"{100 * r['vol']:.1f}\%", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.8 * j, 0])
        lo = min(r["lvr_pct"] for r in lv["by_freq"])
        hi = max(r["lvr_pct"] for r in lv["by_freq"])
        with self.voiceover(
            f"Sampling matters. <bookmark mark='a'/> On this one price history, the local normalized loss sums on minute, five-minute, hourly and daily grids range from {lo:.2f} to {hi:.2f} percent. Each grid uses different endpoints and misses its within-step price path. These similar totals are a sample finding, not a theorem that arbitrage frequency is irrelevant. Microstructure noise, jumps, omitted intraperiod variation and fee bands can change the comparison. The continuous variance formula is a limit under specified assumptions."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def breakeven(self, lv):
        need = lv["lvr_pct"] / 0.3
        per_day = 100 * need / 365
        rows = [cmath(r"\text{fees}", r">", r"\text{LVR}", font_size=44, colors={r"\text{fees}": FEE_C, r"\text{LVR}": ARB_C}),
                cmath(r"f \times \frac{\text{volume}}{V}", r">", rf"{lv['lvr_pct']:.2f}\%\ \text{{a year}}", font_size=38),
                cmath(r"f = 0.3\%", r"\Rightarrow", rf"\text{{volume}} > {need:.1f}\,V\ \text{{a year}}", font_size=38),
                cmath(r"", r"=", rf"{per_day:.1f}\%\ \text{{of the pool a day}}", font_size=38, colors={rf"{per_day:.1f}\%\ \text{{of the pool a day}}": HURDLE})]
        whys = [why('ideal token-hedged reference: fees less LVR; add financing, hedge, venue and execution costs'),
                why(r"fee income is the fee rate times turnover, as a share of the pool"),
                why(r"in ether's 2023, a 0.3\% pool needed annual volume of about nine times its value"),
                why('rough changing-capital turnover hurdle; fee-band trades require a separately reconciled ledger')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"A useful first hurdle matches units. <bookmark mark='a'/> In an ideal token-hedged, fee-free reference calculation, fees must offset loss-versus-rebalancing plus all hedge and operating costs. <bookmark mark='b'/> A constant fee times turnover measured against the same contemporaneous capital gives fee yield. <bookmark mark='c'/> Dividing the sample's normalized loss sum by a three-tenths-percent fee gives about {need:.0f} capital turns for the year, <bookmark mark='d'/> or {per_day:.1f} percent per calendar day if spread evenly. This is a rough changing-capital turnover hurdle, not a validated fixed-initial-capital break-even strategy. Fee bands change trades and holdings; arbitrage fees must be reconciled with their own loss ledger."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def gamma(self):
        rows = [cmath(r"V''(P)", r"=", r"x^{*\prime}(P) < 0", font_size=42, colors={r"x^{*\prime}(P) < 0": ARB_C}),
                cmath(r"\text{LVR rate}", r"=", r"\tfrac12\,|\Gamma|\,\sigma^2 P^2", font_size=42),
                cmath(r"\text{fees}", r"\leftrightarrow", r"\Theta", font_size=42, colors={r"\text{fees}": FEE_C})]
        whys = [why(r"a pool's value is concave in the price: it is short gamma, like a written straddle"),
                why('continuous fee-free model: curvature times quadratic variation; a real hedge also has costs'),
                why(r"and is paid fees in place of the option's time decay: providing liquidity is selling volatility")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The same thing in Part eleven's language. <bookmark mark='a'/> A pool's value is concave in the price: it "
            "is short gamma, like a written straddle. <bookmark mark='b'/> A hedged option seller pays half gamma times "
            "variance, and a hedged liquidity provider pays exactly that. <bookmark mark='c'/> Its fees play the role "
            "of the option's time decay. Providing liquidity to a pool is selling volatility."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"a concentrated position supplies liquidity on $[P/1.05,1.05P]$. At its geometric centre, how many "
                       r"times more liquidity per dollar does it provide than a constant-product position, and what "
                       r"happens to its LVR per dollar?")
        with self.voiceover(
            'Pause and predict. Choose a multiplicative range from P divided by one point zero five to one point zero five times P. At its geometric centre, how many times as much liquidity per dollar does it provide as a full-range constant-product position? What happens to local loss per dollar while the position is in range? Distinguish this centre comparison from its realized fee income over a whole path.'
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
