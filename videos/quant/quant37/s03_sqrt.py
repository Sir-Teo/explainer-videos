from __future__ import annotations


import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (BUY_C, GOOD, HURDLE, IMPACT_C, PART, SELL_C, SIM_C, fit_right,
                                         load)


class Sqrt(VoiceoverScene):
    def construct(self):
        lt = load("latent")
        self.answer()
        self.card()
        self.law()
        self.universal()
        self.bitcoin_sizes()
        self.puzzle()
        self.dimensions()
        self.visible()
        self.latent_picture()
        self.derive()
        self.sim(lt)
        self.decay(lt)
        self.fair_pricing()
        self.invariance()
        self.question()

    def answer(self):
        rows = [cmath(r"\sqrt{4}\times 10", r"=", r"20\ \text{bp}", font_size=40, colors={r"20\ \text{bp}": GOOD}),
                cmath(r"4 \times 10", r"=", r"40\ \text{bp}", font_size=40),
                cmath(r"\text{per unit bought}", r":", r"\text{cheaper for big orders}", font_size=34)]
        whys = [why(r"the square root: four times the size, twice the impact"),
                why(r"a straight line: four times the size, four times the impact"),
                why(r"under the square root the cost per share falls with size, which is why it matters so much for "
                    r"capacity and for how to slice")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> Under the square-root law, four times the size moves the "
            "price twice as far: twenty basis points. <bookmark mark='b'/> Under a straight line, forty. "
            "<bookmark mark='c'/> The difference is not a detail: under the square root, the impact per unit bought "
            "falls with size."
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

    def card(self):
        c = chapter_card(2, r"The square-root law", r"Why does impact grow like the square root of size?", part=PART)
        with self.voiceover("Chapter two. The most robust empirical regularity in market microstructure, and a puzzle "
                            "about why it holds. Then a model of hidden liquidity that explains it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def law(self):
        rows = [cmath(r"I(Q)", r"\approx", r"Y\,\sigma_{\text{day}}\,\sqrt{\frac{Q}{V_{\text{day}}}}", font_size=44,
                      colors={r"I(Q)": IMPACT_C}),
                cmath(r"Y", r"\approx", r"0.5\text{--}1", font_size=40, colors={r"Y": HURDLE}),
                cmath(r"\text{independent of}", r":", r"\text{the duration, roughly}", font_size=34)]
        whys = [why(r"Loeb (1983) and Torre (1997) for equities; Almgren, Thum, Hauptmann and Li (2005); Tóth et al. (2011): "
                    r"the impact of a metaorder in units of the daily volatility, against its share of daily volume"),
                why(r"a prefactor of order one, the same for very different markets"),
                why(r"to a first approximation, the impact depends on how much was bought, not on how fast")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The law. <bookmark mark='a'/> The impact of a metaorder, in units of the daily volatility, is about the "
            "square root of its share of daily volume. Measured on equities by Thomas Loeb and Nicolò Torre, by Almgren "
            "and colleagues on Citigroup's orders, and by Bence Tóth and colleagues on futures. "
            "<bookmark mark='b'/> With a prefactor of order one in very different markets. <bookmark mark='c'/> And, "
            "to a first approximation, it depends on how much was bought, not on how fast."
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

    def universal(self):
        cards = VGroup(
            desk_question(r"equities and futures", r"brokers' and funds' records across thousands of stocks and dozens of "
                          r"futures: exponents near one half over several decades of size", width=12.4, font_size=19),
            desk_question(r"Bitcoin", r"Donier and Bonart (2015) reconstructed about a million metaorders from the Mt.Gox "
                          r"exchange's leaked account-level records, and found the square root there too", width=12.4,
                          font_size=19),
            desk_question(r"its limits", r"very small orders show linear impact (Bucci et al. 2019); some data sets fit a "
                          r"logarithm better (Zarinelli et al. 2015); the prefactor varies with the market", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How universal. <bookmark mark='a'/> Across thousands of stocks and dozens of futures, exponents near one "
            "half over several decades of size. <bookmark mark='b'/> On Bitcoin, Jonathan Donier and Julius Bonart "
            "reconstructed about a million metaorders from the account-level records leaked from the Mt. Gox exchange, "
            "and found a square root there too. <bookmark mark='c'/> With limits: very small orders show linear impact, "
            "some data fit a logarithm better, and the prefactor varies."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def bitcoin_sizes(self):
        ac = load("ac")
        sig = ac["sigma_day"] / ac["price"]
        v_usd = ac["v_day"] * ac["price"]
        shares = (0.001, 0.01, 0.1)
        costs = [1e4 * sig * (s ** 0.5) for s in shares]
        m01 = shares[0] * v_usd / 1e6
        rows = [cmath(rf"{100 * s:g}\%\ \text{{of a day}}", r":", rf"\${s * v_usd / 1e6:,.0f}\text{{m}} \to {c:.0f}\ "
                      r"\text{bp}".replace(",", "{,}"), font_size=36, colors={rf"{c:.0f}\ \text{{bp}}": IMPACT_C})
                for s, c in zip(shares, costs)]
        whys = [why(rf"Bitcoin's perpetual: daily volatility {100 * sig:.1f}\%, daily volume about "
                    rf"\${v_usd / 1e9:.0f}bn, with $Y = 1$"),
                why(r"ten times the size, about three times the impact"),
                why(r"a tenth of the day's volume: an order that moves the price by a third of a day's volatility")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the law says for Bitcoin's perpetual, with a prefactor of one. <bookmark mark='a'/> A tenth of a "
            f"percent of a day's volume, about {m01:.0f} million dollars, costs about "
            f"{costs[0]:.0f} basis points. <bookmark mark='b'/> One percent, about {costs[1]:.0f}: ten times the size, "
            f"three times the cost. <bookmark mark='c'/> A tenth of the day, about {costs[2]:.0f} basis points, a third "
            "of a day's volatility."
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

    def puzzle(self):
        cards = VGroup(
            desk_question(r"not Kyle", r"Part 35's Kyle model gives linear impact; a square root means the market absorbs "
                          r"large orders more cheaply than a fixed depth would", width=12.4, font_size=19),
            desk_question(r"not the visible book", r"the displayed book holds a tiny fraction of a day's volume; a "
                          r"metaorder of 1\% of the day would empty it many times over", width=12.4, font_size=19),
            desk_question(r"so where is the liquidity?", r"in orders that are not yet in the book: traders who would buy "
                          r"or sell at a price, and reveal it only when the price comes near", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why is it a puzzle? <bookmark mark='a'/> Kyle's model gives a straight line. A square root means the market "
            "absorbs large orders more cheaply than any fixed depth would. <bookmark mark='b'/> The visible book is no "
            "help: it holds a tiny fraction of a day's volume, and a metaorder of one percent would empty it many times "
            "over. <bookmark mark='c'/> So the liquidity must be latent: traders who would buy or sell at some price, "
            "and reveal it only when the price comes near."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def dimensions(self):
        rows = [cmath(r"\frac{I}{\sigma}", r"=", r"F\!\left(\frac{Q}{V},\ \frac{T}{T_{\text{day}}}\right)", font_size=40),
                cmath(r"\text{no } T", r"\Rightarrow", r"F = F(Q/V)", font_size=40),
                cmath(r"\text{risk-neutral liquidity}", r"\Rightarrow", r"F \propto \sqrt{Q/V}", font_size=36,
                      colors={r"F \propto \sqrt{Q/V}": GOOD})]
        whys = [why(r"impact in units of volatility, as a function of the order's share of volume and its duration"),
                why(r"the empirical fact that duration barely matters"),
                why(r"one argument: liquidity providers demand compensation proportional to the risk of the position they "
                    r"absorb, $\sigma\sqrt{T}$, while the volume they supply in that time is $\propto V T$; eliminating "
                    r"$T$ leaves a square root (a heuristic, not a theorem)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A second route, by dimensions. <bookmark mark='a'/> Impact in units of volatility can depend only on the "
            "order's share of volume and its duration. <bookmark mark='b'/> The data say the duration barely matters. "
            "<bookmark mark='c'/> A heuristic closes the argument: liquidity providers absorbing the order over a time "
            "T demand compensation for a risk of sigma root T, while the volume they supply grows with T; eliminating "
            "the time leaves a square root. A heuristic, not a theorem, but it explains why the law is so universal."
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

    def visible(self):
        ac = load("ac")
        best = 10.0
        share = 100 * best / ac["v_day"]
        rows = [cmath(r"\text{best queues}", r"\approx", r"10\ \text{BTC}", font_size=38),
                cmath(r"V_{\text{day}}", r"\approx", rf"{ac['v_day'] / 1000:.0f}{{,}}000\ \text{{BTC}}", font_size=38),
                cmath(r"\text{displayed}", r"\approx", rf"{share:.3f}\%\ \text{{of a day}}", font_size=38,
                      colors={r"\text{displayed}": HURDLE})]
        whys = [why(r"Part 36: the two best queues of Bitcoin's perpetual hold about ten bitcoin at a time"),
                why(r"against the day's volume on the same contract"),
                why(r"the displayed book is a sliver; the liquidity that absorbs a metaorder arrives as the price moves, "
                    r"which is what latent means")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How small the visible book is. <bookmark mark='a'/> Part thirty-six measured about ten bitcoin at the two "
            "best quotes. <bookmark mark='b'/> The contract trades about "
            f"{ac['v_day'] / 1000:.0f} thousand bitcoin a day. <bookmark mark='c'/> The displayed best quotes hold "
            f"{share:.3f} percent of a day's volume. Whatever absorbs a large order arrives as the price moves: that is "
            "what latent means."
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

    def latent_picture(self):
        g = axes([-4, 4], [-4, 4], x_length=7.4, y_length=4.4, xlabel=r"price, relative to the current price",
                 ylabel=r"latent volume", xticks=[0], yticks=[0], font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        bids = Polygon(ax.c2p(-4, 0), ax.c2p(0, 0), ax.c2p(-4, 4), fill_color=BUY_C, fill_opacity=0.45, stroke_width=0)
        asks = Polygon(ax.c2p(0, 0), ax.c2p(4, 0), ax.c2p(4, -4), fill_color=SELL_C, fill_opacity=0.45, stroke_width=0)
        eaten = Polygon(ax.c2p(0, 0), ax.c2p(2, 0), ax.c2p(2, -2), fill_color=IMPACT_C, fill_opacity=0.9, stroke_width=0)
        mark = DashedLine(ax.c2p(2, -4), ax.c2p(2, 4), color=HURDLE, stroke_width=2)
        labs = VGroup(label(r"latent bids", font_size=18, color=BUY_C).move_to(ax.c2p(-2.6, 1.5)),
                      label(r"latent offers", font_size=18, color=SELL_C).move_to(ax.c2p(2.8, -1.0)),
                      label(r"a buyer eats a triangle", font_size=18, color=IMPACT_C).next_to(ax.c2p(1, -2), DOWN,
                                                                                         buff=0.6))
        with self.voiceover(
            "The picture of latent liquidity. <bookmark mark='a'/> Hidden intentions to buy below the price and to sell "
            "above it. Jonathan Donier, Julius Bonart, Iacopo Mastromatteo and Bouchaud showed that if these latent "
            "orders keep arriving, being cancelled and revising their prices at random, the density near the price is "
            "a V: it grows linearly with the distance from the price. <bookmark mark='b'/> A buyer must eat the offers "
            "between the old price and the new one: a triangle."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(bids), FadeIn(asks), FadeIn(labs[:2]))
            vo.wait_until("b")
            self.play(FadeIn(eaten), Create(mark), FadeIn(labs[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\rho(x)", r"=", r"\mathcal L\,|x|", font_size=40),
                cmath(r"Q", r"=", r"\int_0^{\Delta} \mathcal L\,x\,dx = \tfrac12\,\mathcal L\,\Delta^2", font_size=40),
                cmath(r"\Delta", r"=", r"\sqrt{2Q/\mathcal L}", font_size=44, colors={r"\Delta": IMPACT_C}),
                cmath(r"\mathcal L", r"\propto", r"V_{\text{day}} / \sigma_{\text{day}}^2", font_size=38)]
        whys = [why(r"the latent density near the price: linear, with slope $\mathcal L$"),
                why(r"to move the price from 0 to $\Delta$, a buyer must absorb all the offers in between: the area of the "
                    r"triangle"),
                why(r"invert: the square root, from nothing but the V shape"),
                why(r"by dimensional analysis the slope scales as volume over variance, which gives the law's "
                    r"$\sigma\sqrt{Q/V}$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The derivation in three lines. <bookmark mark='a'/> Near the price, the latent density is linear, with "
            "slope script L. <bookmark mark='b'/> To move the price from zero to delta, a buyer must absorb every offer "
            "in between: the area of the triangle, one half L delta squared. <bookmark mark='c'/> Invert, and the price "
            "moves as the square root of two Q over L. <bookmark mark='d'/> And by dimensions the slope scales as volume "
            "over variance, which turns this into the law's sigma times the root of Q over V."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def sim(self, lt):
        rows = lt["rows"]
        x = np.log10([r["Q"] for r in rows])
        y = np.log10([r["I"] for r in rows])
        g = axes([-2, 3], [float(np.floor(y.min())), float(np.ceil(y.max()))], x_length=6.4, y_length=4.4,
                 xlabel=r"metaorder size $Q$, executed in one unit of time", ylabel=r"impact at the end",
                 xticks=[-2, 0, 2], yticks=[float(np.floor(y.min())), 0, float(np.ceil(y.max()))],
                 xfmt=lambda v: f"10^{{{v:.0f}}}", yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=SIM_C) for a, b in zip(x, y)])
        sq = DashedLine(ax.c2p(0, 0.5 * np.log10(2)), ax.c2p(3, 0.5 * np.log10(2) + 1.5), color=GOOD, stroke_width=2)
        st = VGroup(label(rf"small orders: slope {lt['slope_small']:.2f}", font_size=18, color=SIM_C),
                    label(rf"large orders: slope {lt['slope_large']:.2f}", font_size=18, color=SIM_C),
                    label(r"$\sqrt{2Q/\mathcal L}$, the static book", font_size=18, color=GOOD))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "Now simulate it: the latent density diffusing, a buyer removing offers at the price for one unit of time, "
            "for sizes across five decades. <bookmark mark='a'/> Small orders move the price in proportion, slope "
            f"{lt['slope_small']:.2f}: the book has time to refill around them. <bookmark mark='b'/> Large orders bend "
            f"toward the square root, slope {lt['slope_large']:.2f}, approaching the static book's formula. Linear for "
            "small orders, square root for large: the crossover Federico Bucci and colleagues found in real data."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(Create(sq))
        self.wait(0.4)
        self.clear_scene()

    def decay(self, lt):
        t = np.asarray(lt["path_t"], float)
        p = np.asarray(lt["path_p"], float)
        top = float(np.ceil(p.max()))
        g = axes([0, float(t[-1])], [0, top], x_length=8.4, y_length=4.2, xlabel=r"time (the order runs from 0 to 1)",
                 ylabel=r"price", xticks=[0, 1, 5, 10], yticks=[0, top], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(DOWN * 0.2)
        c_ = curve(g.ax, t, p, IMPACT_C, stroke_width=3)
        stop = DashedLine(g.ax.c2p(1, 0), g.ax.c2p(1, top), color=GREY_B, stroke_width=1.5)
        peak = float(p.max())
        end = float(p[-1])
        with self.voiceover(
            "And after the order stops. <bookmark mark='a'/> The price peaks when buying ends, at "
            f"{peak:.1f}, <bookmark mark='b'/> then decays as the latent book heals, to {end:.1f} after nine more units "
            "of time, and on, slowly, like one over the square root of time. In this pure model nothing is permanent; "
            "in real markets, information makes part of it stay."
        ) as vo:
            self.play(FadeIn(g), Create(stop))
            vo.wait_until("a")
            self.play(Create(c_), run_time=3)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def fair_pricing(self):
        rows = [cmath(r"I(q)", r"=", r"c\sqrt q\quad (0 \le q \le Q)", font_size=40, colors={r"I(q)": IMPACT_C}),
                cmath(r"\bar p - p_0", r"=", r"\frac1Q\int_0^Q c\sqrt q\,dq = \tfrac23\,c\sqrt Q", font_size=36),
                cmath(r"\text{fair pricing}", r":", r"p_\infty = \bar p \Rightarrow \frac{I_\infty}{I(Q)} = \frac23",
                      font_size=36, colors={r"\frac{I_\infty}{I(Q)} = \frac23": GOOD})]
        whys = [why(r"the price impact after the first $q$ units of a metaorder: a square root"),
                why(r"the average price the buyer paid lies two-thirds of the way up"),
                why(r"Farmer, Gerig, Lillo and Waelbroeck (2013): if, after the order, the price settles at the average "
                    r"price paid, neither side profits on average; then two-thirds of the peak remains, as Chapter 1 "
                    r"reported")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And a striking consequence. <bookmark mark='a'/> Suppose impact grows as the square root of the quantity "
            "already bought. <bookmark mark='b'/> Then the average price paid is two-thirds of the way up to the peak. "
            "<bookmark mark='c'/> Doyne Farmer, Austin Gerig, Fabrizio Lillo and Henri Waelbroeck argued for fair "
            "pricing: in a competitive market, the price should settle at the average price paid, so that neither the "
            "buyer nor the liquidity providers profit on average. Then two-thirds of the peak remains: the reversion "
            "Chapter one reported, derived from the square root."
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

    def invariance(self):
        rows = [cmath(r"W", r"=", r"\sigma\,P\,V", font_size=40, colors={r"W": HURDLE}),
                cmath(r"\text{bets per day}", r"\propto", r"W^{2/3}", font_size=38),
                cmath(r"\frac{I}{\sigma}", r"=", r"f\!\left(\frac{Q}{V}\,W^{2/3}\right)", font_size=40,
                      colors={r"\frac{I}{\sigma}": IMPACT_C})]
        whys = [why(r"Kyle and Obizhaeva (2016): trading activity, volatility times dollar volume"),
                why(r"their invariance hypothesis: bets arrive in business time, and their dollar risk transfer is the "
                    r"same in every market; this fixes how the number of bets, and so their typical share of volume, scale "
                    r"with activity"),
                why(r"so impact in units of volatility is one function of size measured in bets, the same for every "
                    r"asset; a square root is consistent with it, and it predicts how the prefactor varies")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A different route to universality. <bookmark mark='a'/> Albert Kyle and Anna Obizhaeva define trading "
            "activity as volatility times dollar volume. <bookmark mark='b'/> Their invariance hypothesis says that "
            "bets arrive in business time, and transfer the same dollar risk in every market; that fixes how the number "
            "of bets scales with activity, as its two-thirds power. <bookmark mark='c'/> So impact in units of volatility is one function of size "
            "measured in bets, for every asset. The square root fits inside it, and it predicts how the prefactor "
            "should vary from market to market."
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

    def question(self):
        q = pause_card(r"signs of trades are predictable for hundreds of trades ahead (Part 36), yet prices are not. "
                       r"What must happen to the impact of each trade over time?")
        with self.voiceover(
            "Pause and predict. The signs of trades are predictable hundreds of trades ahead, as Part thirty-six "
            "showed, yet prices are not. What must happen to the impact of each trade over time?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
