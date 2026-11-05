from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
            f"Chapter three, and the answer to the pause: about {lv['lvr_pct']:.1f} percent of its value over the year. "
            "Not the impermanent loss, which depends only on where the price ended, but a loss to arbitrageurs that "
            "accrued minute by minute. This chapter shows how to measure it, and why it is the right measure."
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
        whys = [why(r"impermanent loss: mixes the cost of trading with the effect of holding less ether in a rally"),
                why(r"loss-versus-rebalancing: the same exposure at every instant, so the gap is only the cost of trading "
                    r"at stale prices"),
                why(r"the market part: the pool's falling ether holdings missed some of the rally; a choice of exposure, "
                    r"not a cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"Take the differences. <bookmark mark='a'/> Pool minus hold, {il:+.3f}, is the impermanent loss; it mixes "
            "two things. <bookmark mark='b'/> Pool minus rebalancing, "
            f"{-lvr:+.3f}, is loss-versus-rebalancing: the two had the same exposure at every instant, so the gap is "
            f"purely the cost of trading at stale prices. <bookmark mark='c'/> And rebalancing minus hold, {mk:+.3f}, is "
            "the market part: holding less ether as it rallied. That is a choice of exposure, which a hedge can undo, "
            "not a cost."
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
            desk_question(r"it can be hedged away", r"a provider who shorts the pool's token holdings on a perpetual is "
                          r"left with exactly the gap to the rebalancing portfolio, plus fees", width=12.4, font_size=19),
            desk_question(r"it is predictable", r"it accrues at a known rate, set by volatility, and does not depend on "
                          r"where the price ends", width=12.4, font_size=19),
            desk_question(r"it is someone's income", r"every unit of it is an arbitrageur's profit, or a fee, or paid to "
                          r"block builders: Chapter 5", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why the rebalancing benchmark is the right one. <bookmark mark='a'/> It can be hedged: a provider who shorts "
            "the pool's token holdings on a perpetual is left with exactly the gap, plus fees. <bookmark mark='b'/> It is "
            "predictable: it accrues at a rate set by volatility and does not depend on where the price ends. "
            "<bookmark mark='c'/> And it is someone's income: an arbitrageur's profit, a fee, or a payment to whoever "
            "builds the block."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
                why(r"the minute-by-minute loss of a pool arbitraged every minute, summed: the formula to the second "
                    r"decimal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The rate has a formula, proved in the research chapter. <bookmark mark='a'/> For a constant-product pool, "
            "variance over eight, times the pool's value, per unit of time. <bookmark mark='b'/> Ether's volatility in "
            f"twenty twenty-three was {100 * lv['vol']:.0f} percent, so variance over eight is {lv['rv8_pct']:.2f} percent. "
            f"<bookmark mark='c'/> The measured loss of a pool arbitraged every minute: {lv['lvr_pct']:.2f} percent."
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
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"arbitraged every", r"loss, \% of value",
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
            "Does it depend on how often the pool is arbitraged? <bookmark mark='a'/> Every minute, every five, every "
            "hour, every day: the loss stays between "
            f"{lo:.2f} and {hi:.2f} percent, "
            "because ether's realised variance hardly depends on the sampling. A pool loses its variance over eight, "
            "however finely the arbitrageurs slice it."
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
        whys = [why(r"a provider who hedges the token exposure earns fees and pays LVR"),
                why(r"fee income is the fee rate times turnover, as a share of the pool"),
                why(r"in ether's 2023, a 0.3\% pool needed annual volume of about nine times its value"),
                why(r"from traders who are not arbitrageurs: arbitrage volume pays fees too, but on trades that are "
                    r"themselves the loss")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "When providing pays. <bookmark mark='a'/> A hedged provider earns fees and pays LVR. <bookmark mark='b'/> "
            "Fee income is the fee rate times turnover. <bookmark mark='c'/> At three tenths of a percent, a pool in "
            f"ether's twenty twenty-three needed volume of about {need:.0f} times its value in the year, "
            f"<bookmark mark='d'/> about {per_day:.1f} percent of the pool every day, from traders who are not "
            "arbitrageurs. Arbitrage pays fees too, but on the very trades that are the loss."
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
                why(r"Part 11's hedged option seller pays half gamma times variance; a hedged LP pays exactly that"),
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
        q = pause_card(r"a concentrated position supplies liquidity only within 5\% either side of the price. How many "
                       r"times more liquidity per dollar does it provide than a constant-product position, and what "
                       r"happens to its LVR per dollar?")
        with self.voiceover(
            "Pause and predict. A concentrated position supplies liquidity only within five percent either side of the "
            "price. How many times more liquidity per dollar does it provide than a constant-product position, and what "
            "happens to its loss per dollar?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
