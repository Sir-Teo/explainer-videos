from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    HURDLE,
    PART,
    POOL_C,
    SPOT_C,
    STABLE_C,
    comma,
    load,
)


class AMM(VoiceoverScene):
    def construct(self):
        a = load("amm")
        self.card(a)
        self.invariant(a)
        self.trade_anim(a)
        self.slippage(a)
        self.general()
        self.arbitrage()
        self.oracle()
        self.il_formula(a)
        self.il_curve(a)
        self.question()

    def card(self, a):
        t = a["trades"][2]
        c = chapter_card(2, r"Automated market makers", r"How can a formula be a market maker?", part=PART)
        with self.voiceover(
            f"Chapter two, and the answer to the pause: about {t['avg']:,.0f} dollars per ether on average, "
            f"{100 * t['slip']:.0f} percent above the pool's starting price. A pool has no order book, only a formula, and "
            "the formula charges more for every additional unit. This chapter takes the formula apart."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def invariant(self, a):
        rows = [cmath(r"x\,y", r"=", r"k", font_size=48, colors={r"k": POOL_C}),
                cmath(r"P", r"=", r"\frac{y}{x}", font_size=44, colors={r"P": SPOT_C}),
                cmath(r"(x + (1-f)\Delta x)(y - \Delta y)", r"=", r"k", font_size=38),
                cmath(r"\Delta y", r"=", r"\frac{y\,(1 - f)\Delta x}{x + (1 - f)\Delta x}", font_size=38,
                      colors={r"\Delta y": POOL_C})]
        whys = [why(r"a pool holds $x$ of a token and $y$ of a numeraire, and accepts any trade that keeps their product "
                    r"fixed (Uniswap v2, after Hayden Adams and Vitalik Buterin's sketch)"),
                why(r"its price is the slope of the curve: the ratio of its reserves"),
                why(r"a trader adds $\Delta x$ and removes $\Delta y$; the curve decides how much"),
                why(r"with a fee $f$ (0.3\% in the classic pool) taken on the input and paid to the liquidity "
                    r"providers")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The fee-adjusted constant-product swap. <bookmark mark='a'/> A pool has token reserve x and numeraire reserve y. Without fees, swaps follow a fixed product. <bookmark mark='b'/> Its infinitesimal pre-fee token price is y over x, the negative slope of the reserve curve. <bookmark mark='c'/> If gross token input is delta x and input fee is f, only one minus f times delta x enters the invariant, giving the displayed output. <bookmark mark='d'/> In a native fee-retaining pool, the actual reserve product grows as fees accumulate. The lecture's arbitrage simulator instead keeps its curve fixed and accounts for fees outside it. Those are distinct conventions, so its results are not a complete replay of native Uniswap fee compounding."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def trade_anim(self, a):
        x0, y0 = a["x"] / 1000, a["y"] / 1e6           # thousands of ETH, millions of USDC
        k = x0 * y0
        g = axes([0, 12], [0, 24], x_length=6.6, y_length=4.6, xlabel=r"ETH in the pool, thousands",
                 ylabel=r"USDC in the pool, millions", xticks=[0, 4, 8, 12], yticks=[0, 8, 16, 24], font_size=16)
        g.move_to(LEFT * 2.2 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(2.1, 12, 200)
        hyp = curve(ax, xs, k / xs, POOL_C, stroke_width=3)
        xt = ValueTracker(x0)
        dot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), k / xt.get_value()), radius=0.09, color=SPOT_C))
        tang = always_redraw(lambda: Line(ax.c2p(xt.get_value() - 1.6, k / xt.get_value() + 1.6 * k / xt.get_value() ** 2),
                                          ax.c2p(xt.get_value() + 1.6, k / xt.get_value() - 1.6 * k / xt.get_value() ** 2),
                                          color=HURDLE, stroke_width=2.5))
        read = always_redraw(lambda: VGroup(
            label(rf"price $y/x$ = {1000 * k / xt.get_value() ** 2:,.0f}", font_size=20, color=SPOT_C),
            label(rf"ETH {1000 * xt.get_value():,.0f}, USDC {k / xt.get_value():.2f}m", font_size=18, color=GREY_A))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(UP * 1.6))
        y_m = a["y"] / 1e6
        with self.voiceover(
            f"A pool of {a['x']:,.0f} ether and {y_m:.0f} million dollars of a dollar stablecoin, so a price of "
            "two thousand. <bookmark mark='a'/> A buyer of ether moves the point up the curve: ether leaves, dollars "
            "arrive, and the slope, the price, rises. <bookmark mark='b'/> A seller moves it back down. The curve never "
            "runs out: it simply asks a higher price for every further unit, without limit."
        ) as vo:
            self.play(FadeIn(g), Create(hyp))
            self.add(dot, tang, read)
            vo.wait_until("a")
            self.play(xt.animate.set_value(3.2), run_time=3)
            vo.wait_until("b")
            self.play(xt.animate.set_value(7.0), run_time=3)
            self.play(xt.animate.set_value(x0), run_time=1.5)
        self.wait(0.4)
        self.remove(dot, tang, read)
        self.clear_scene()

    def slippage(self, a):
        hx = [-4.0, -1.0, 2.2, 5.0]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"ETH bought", r"USDC paid", r"average price",
                                                                         r"above 2,000")])
        tab = VGroup(head)
        for r in a["trades"]:
            tab.add(VGroup(MathTex(comma(r["dx"]), font_size=28), MathTex(comma(r["paid"]), font_size=28),
                           MathTex(comma(r["avg"]), font_size=28, color=SPOT_C),
                           MathTex(rf"{100 * r['slip']:.1f}\%", font_size=28, color=BAD if r["slip"] > 0.05 else GREY_A)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(r"constant product, 0.3\% fee; the first row is the fee plus a fifth of a percent of curve",
                             11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        t0, t3 = a["trades"][0], a["trades"][3]
        with self.voiceover(
            f"What the curve charges. <bookmark mark='a'/> Ten ether cost {100 * t0['slip']:.1f} percent above the "
            "starting price: mostly the fee. <bookmark mark='b'/> A hundred, "
            f"{100 * a['trades'][1]['slip']:.1f} percent; five hundred, a tenth of the pool, {100 * a['trades'][2]['slip']:.0f} percent; <bookmark mark='c'/> and a thousand, a fifth of the "
            f"pool, {100 * t3['slip']:.0f} percent. Slippage grows faster than size, because the trade walks along a "
            "curve that steepens. It is Part thirty-six's order book, with the depth set by a formula instead of by "
            "makers."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def general(self):
        rows = [cmath(r"\varphi(x, y)", r"=", r"k", font_size=44, colors={r"\varphi(x, y)": POOL_C}),
                cmath(r"P", r"=", r"\frac{\partial\varphi/\partial x}{\partial\varphi/\partial y}", font_size=40),
                cmath(r"x^{w} y^{1 - w}", r"=", r"k", font_size=40),
                cmath(r"\text{flat near } P = 1", r":", r"\text{stableswap}", font_size=38,
                      colors={r"\text{stableswap}": STABLE_C})]
        whys = [why(r"a constant-function market maker: any invariant whose level sets are convex curves"),
                why(r"the price is the ratio of marginal values: the slope of the level set at the reserves"),
                why(r"Balancer's weighted pools: a pool that keeps a fixed share $w$ of its value in the token"),
                why(r"Michael Egorov's Curve pools for assets that should trade at par: nearly a straight line near the "
                    r"peg, so small trades barely move the price, bending sharply away from it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The general form. <bookmark mark='a'/> A constant-function market maker accepts any trade that keeps an "
            "invariant fixed, with convex level sets. <bookmark mark='b'/> Its price is the slope of the level set. "
            "<bookmark mark='c'/> Balancer's weighted pools keep a fixed share of their value in each token. "
            "<bookmark mark='d'/> And Curve's stableswap, for assets meant to trade at par, is almost a straight line "
            "near the peg, so stablecoin swaps barely move the price, and bends sharply when the peg is lost."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def arbitrage(self):
        cards = VGroup(
            desk_question(r"the pool does not know the price", r"it only knows its reserves; when ether rises on Binance, "
                          r"the pool still quotes the old price", width=12.4, font_size=19),
            desk_question(r"arbitrageurs move it", r"they buy the cheap ether from the pool and sell it elsewhere, until the "
                          r"pool's price, net of the fee, matches the market", width=12.4, font_size=19),
            desk_question(r"who pays", r"every such trade is made against stale prices: the arbitrageur's profit is the "
                          r"liquidity providers' loss, the subject of the next chapter", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "How the pool's price stays right. <bookmark mark='a'/> The pool does not know the market price; it only "
            "knows its reserves. When ether rises on a centralised exchange, the pool still quotes the old price. "
            "<bookmark mark='b'/> Arbitrageurs buy the cheap ether from the pool and sell it elsewhere, until the pool's "
            "price, net of its fee, matches the market. <bookmark mark='c'/> Every such trade is made against a stale "
            "price, like the sniped quotes of Part thirty-eight: the arbitrageur's profit is the liquidity providers' "
            "loss."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def oracle(self):
        rows=[cmath(r"P_1/P_0=r\ge1",r"\Rightarrow",r"x_1=x_0/\sqrt r,\quad y_1=y_0\sqrt r",font_size=34),
              cmath(r"\text{arithmetic TWAP}",r"=",r"T^{-1}\int_0^T P_t\,dt",font_size=36),
              cmath(r"\text{geometric time average}",r"=",r"\exp(T^{-1}\int_0^T\log P_t\,dt)",font_size=34),
              cmath(r"\text{flash loan}",r":",r"\text{atomic repayment; costs and constraints remain}",font_size=30)]
        whys=[why(r"fee-free fixed product: gross numeraire input is $y_0(\sqrt r-1)$, not net manipulation profit"),
              why(r"the protocol's exact arithmetic or observation rule must be checked"),
              why(r"averaging log prices then exponentiating gives a geometric average, not arithmetic TWAP"),
              why(r"a flash loan must be repaid in the same transaction; fees, gas, price impact and oracle safeguards remain")]
        step=ladder(self,rows,whys,keep=4,top=2.8,x=-0.3,buff=0.42,edge=6.9)
        with self.voiceover("A pool can be used as a price input, but the observation rule matters. <bookmark mark='a'/> For a fee-free fixed-product move that multiplies pool price by r, the token reserve falls by root r and the numeraire reserve rises by root r. Gross input is not the attacker's net loss or profit. <bookmark mark='b'/> Arithmetic TWAP averages prices over time. <bookmark mark='c'/> Averaging log prices and exponentiating gives a geometric time average instead; an integral of log price alone is not either price-level average. <bookmark mark='d'/> Flash loans require atomic repayment. They can relax upfront capital needs, but fees, gas, impact, competing arbitrage and oracle safeguards still matter. An attack's profitability needs a full transaction and valuation model.") as vo:
            step(0)
            for i,m in enumerate(("a","b","c","d")):
                vo.wait_until(m)
                if i:step(i)
        self.wait(0.5)
        self.clear_scene()

    def il_formula(self, a):
        rows = [cmath(r"V_{\text{pool}}(P)", r"=", r"2\sqrt{kP}", font_size=44, colors={r"V_{\text{pool}}(P)": POOL_C}),
                cmath(r"V_{\text{hold}}", r"=", r"x_0 P + y_0 = \sqrt{kP_0}\,(r + 1)", font_size=38),
                cmath(r"\frac{V_{\text{pool}}}{V_{\text{hold}}} - 1", r"=", r"\frac{2\sqrt r}{1 + r} - 1", font_size=42,
                      colors={r"\frac{2\sqrt r}{1 + r} - 1": ARB_C}),
                cmath(r"r = 2", r"\Rightarrow", rf"{100 * a['il2']:.1f}\%", font_size=44, colors={r"r = 2": SPOT_C})]
        whys = [why(r"at price $P$ the pool holds $x = \sqrt{k/P}$ and $y = \sqrt{kP}$, worth $2\sqrt{kP}$"),
                why(r"the same initial assets, simply held: a price ratio $r = P/P_0$"),
                why(r"impermanent loss: the pool against holding, from the price ratio alone"),
                why(rf"the desk question: if ether doubles, the pool is worth {100 * abs(a['il2']):.1f}\% less than the "
                    r"assets it started with; a halving costs the same")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What a liquidity provider gives up. <bookmark mark='a'/> At price P the constant-product pool holds the "
            "square root of k over P of the token, and is worth two root k P. <bookmark mark='b'/> Simply holding the "
            "starting assets would be worth the start times r plus one, where r is the price ratio. "
            "<bookmark mark='c'/> Their ratio, minus one, is the impermanent loss: two root r over one plus r, minus "
            f"one. <bookmark mark='d'/> If ether doubles, the pool is worth {100 * abs(a['il2']):.1f} percent less than "
            "holding: the desk question's answer. A halving costs exactly the same."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def il_curve(self, a):
        r = np.asarray(a["r"], float)
        il = 100 * np.asarray(a["il"], float)
        g = axes([-1, 1], [-45, 0], x_length=7.0, y_length=4.2, xlabel=r"price ratio $r = P/P_0$",
                 ylabel=r"pool against holding, \%", xticks=[-1, np.log10(0.5), 0, np.log10(2), 1],
                 xfmt=lambda v: {-1: "0.1", 0: "1", 1: "10"}.get(round(v), "0.5" if v < 0 else "2"),
                 yticks=[-40, -20, 0], font_size=16)
        g.move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, np.log10(r), il, ARB_C, stroke_width=3)
        pts = VGroup(*[Dot(ax.c2p(np.log10(rr), 100 * v), radius=0.08, color=SPOT_C)
                       for rr, v in ((2.0, a["il2"]), (0.5, a["il_half"]), (4.0, a["il4"]))])
        side = VGroup(label(rf"$r = 2$ or $\tfrac12$: {100 * a['il2']:.1f}\%", font_size=20, color=SPOT_C),
                      label(rf"$r = 4$: {100 * a['il4']:.0f}\%", font_size=20, color=SPOT_C),
                      label(r"zero if the price comes back", font_size=20, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        with self.voiceover(
            "The whole curve. <bookmark mark='a'/> Small for small moves, symmetric in the logarithm of the price, and "
            f"{100 * abs(a['il4']):.0f} percent at a fourfold move either way. <bookmark mark='b'/> It is called "
            "impermanent because it vanishes if the price returns to where it started. That name is the problem: it "
            "depends only on where the price ends, not on the path, so it says nothing about how much the pool paid to "
            "arbitrageurs along the way, or whether the fees covered it."
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"in 2023 ether rose from about \$1,200 to \$2,300. A constant-product pool was arbitraged to "
                       r"Binance's price every minute. What share of its value did it lose to arbitrageurs, against a "
                       r"portfolio that held the same ether but traded at market prices?")
        with self.voiceover(
            "Pause and predict. In twenty twenty-three ether rose from about twelve hundred dollars to twenty-three "
            "hundred. A constant-product pool was arbitraged to Binance's price every minute. What share of its value did "
            "it lose to arbitrageurs, against a portfolio that held the same ether but traded at market prices?"
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
