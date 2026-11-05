from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BUY_C, SELL_C, BAD, FAST_C, HURDLE, MAKER_C, PART, SNIPE_C, fit_right, load)


class Speed(VoiceoverScene):
    def construct(self):
        b = load("bcs")
        self.card()
        self.race()
        self.model()
        self.sim(b)
        self.n_table(b)
        self.btc_prize(load("maker"))
        self.arms()
        self.measured()
        self.physics()
        self.remedies()
        self.auction_example()
        self.adoption()
        self.question()

    def card(self):
        c = chapter_card(6, r"The speed race", r"Why do market makers spend fortunes on microseconds?", part=PART)
        with self.voiceover("Chapter six, and the answer to the pause: four times in five. When news is public, the maker "
                            "who quoted is one runner against many, and wins the race to cancel only as often as anyone "
                            "else wins the race to trade. Eric Budish, Peter Cramton and John Shim turned that into an "
                            "equilibrium."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def race(self):
        cards = VGroup(
            desk_question(r"the news", r"a futures price moves, a correlated stock ticks, an index level updates: "
                          r"public information, seen by every fast firm within microseconds", width=12.4, font_size=19),
            desk_question(r"the race", r"the maker sends a cancel; its rivals send orders to hit the stale quote; the "
                          r"exchange processes messages one at a time, in the order they arrive", width=12.4, font_size=19),
            desk_question(r"the outcome", r"with N equally fast firms, the maker's cancel arrives first one time in N; "
                          r"otherwise its quote is sniped", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The race. <bookmark mark='a'/> News arrives: a futures price moves, or a correlated asset ticks, public "
            "information that every fast firm sees within microseconds. <bookmark mark='b'/> The maker sends a cancel; "
            "its rivals send orders to hit the stale quote; the exchange processes messages one at a time, in the order "
            "they arrive. <bookmark mark='c'/> With N equally fast firms, the maker's cancel arrives first one time in N."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"\pi_{\text{maker}}", r"=", r"\lambda_I \tfrac{s}{2} - \lambda_J \tfrac{N-1}{N}(J - \tfrac s2)",
                      font_size=36, colors={r"\pi_{\text{maker}}": MAKER_C}),
                cmath(r"\pi_{\text{sniper}}", r"=", r"\lambda_J \tfrac1N (J - \tfrac s2)", font_size=36,
                      colors={r"\pi_{\text{sniper}}": SNIPE_C}),
                cmath(r"\pi_{\text{maker}} = \pi_{\text{sniper}}", r"\Rightarrow", r"\tfrac{s^*}{2} = \frac{\lambda_J J}"
                      r"{\lambda_I + \lambda_J}", font_size=34, colors={r"\tfrac{s^*}{2} = \frac{\lambda_J J}{\lambda_I + \lambda_J}": HURDLE})]
        whys = [why(r"the maker earns half the spread from investors arriving at rate $\lambda_I$, and loses $J - s/2$ "
                    r"each time a jump of size $J$ (rate $\lambda_J$) catches its quote stale"),
                why(r"each of the others wins a race one time in $N$"),
                why(r"in equilibrium no firm prefers the other role; the $N$ cancels: the spread is independent of "
                    r"how many firms compete")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The model, simplified to its core. <bookmark mark='a'/> The maker earns half the spread from investors, and "
            "loses the jump minus half the spread whenever news catches its quote stale and it loses the race. "
            "<bookmark mark='b'/> Each sniper wins one race in N. <bookmark mark='c'/> In equilibrium no firm wants to "
            "switch roles, so the two profits are equal, and N cancels: the half-spread is lambda J times J over "
            "lambda I plus lambda J, however many firms compete. The research chapter proves it."
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

    def sim(self, b):
        sims = b["sims"]
        x = np.asarray([s["half"] for s in sims], float)
        lp = np.asarray([s["lp"] for s in sims], float)
        sn = np.asarray([s["sniper"] for s in sims], float)
        top = float(np.ceil(max(lp.max(), sn.max()) * 2) / 2)
        lo = float(np.floor(min(lp.min(), 0) * 2) / 2)
        g = axes([0, float(x.max())], [lo, top], x_length=6.4, y_length=4.4, xlabel=r"half-spread $s/2$",
                 ylabel=r"profit per unit time", xticks=[0, 1, 2, 3, 4], yticks=[lo, 0, top], yfmt=lambda v: f"{v:.1f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        cl = curve(ax, x, lp, MAKER_C, stroke_width=3)
        cs = curve(ax, x, sn, SNIPE_C, stroke_width=3)
        star = DashedLine(ax.c2p(b["s_star"], lo), ax.c2p(b["s_star"], top), color=HURDLE, stroke_width=1.8)
        leg = legend([(MAKER_C, r"the maker"), (SNIPE_C, r"each sniper"), (HURDLE, r"$s^*/2$, the formula")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "Simulate it: investors at rate one, jumps of four at rate a tenth, five firms, a long run. "
            "<bookmark mark='a'/> As the half-spread widens, the maker's profit rises and each sniper's falls. "
            f"<bookmark mark='b'/> They cross where the formula says, at {b['s_star']:.2f}. A narrower spread would make "
            "makers become snipers; a wider one would draw snipers into making."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cl), Create(cs))
            vo.wait_until("b")
            self.play(Create(star))
        self.wait(0.4)
        self.clear_scene()

    def n_table(self, b):
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"firms $N$", r"maker's profit", r"each sniper's")])
        tab = VGroup(head)
        for r in b["byN"]:
            tab.add(VGroup(MathTex(str(r["N"]), font_size=26), MathTex(f"{r['lp']:.3f}", font_size=26, color=MAKER_C),
                           MathTex(f"{r['sniper']:.3f}", font_size=26, color=SNIPE_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label(rf"all at the same spread, $s^*/2 = {b['s_star']:.2f}$: the two profits stay equal whatever the "
                             r"number of firms, and both shrink as firms are added", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "And the spread does not depend on how many race. <bookmark mark='a'/> At the same spread, with two firms "
            "or thirty, the maker's and each sniper's profits stay equal. Both shrink as firms are added, because the "
            "same prize is split more ways; but the prize itself, paid by investors through the spread, does not "
            "shrink. Competition among fast firms does not narrow the spread."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def btc_prize(self, mk):
        d = mk["days"]["2023-05-17"]
        rows = [cmath(r"\text{slow}", r":", rf"{d['slow']['n']:,}\ \text{{fills}} \times {d['slow']['pnl_per_fill']:.1f}".replace(",", "{,}"),
                      font_size=34, colors={r"\text{slow}": SNIPE_C}),
                cmath(r"\text{fast}", r":", rf"{d['fast']['n']:,}\ \text{{fills}} \times {d['fast']['pnl_per_fill']:.1f}".replace(",", "{,}"),
                      font_size=34, colors={r"\text{fast}": FAST_C}),
                cmath(r"\text{per unit quoted, a day}", r":", rf"\${0.1 * abs(d['slow']['n'] * d['slow']['pnl_per_fill']) / 1000:.0f}"
                      rf"\text{{k}} \to \${0.1 * abs(d['fast']['n'] * d['fast']['pnl_per_fill']) / 1000:.0f}\text{{k lost}}",
                      font_size=32, colors={r"\text{per unit quoted, a day}": HURDLE})]
        whys = [why(r"17 May, the slow maker of Chapter 2"),
                why(r"the idealised fast maker on the same day"),
                why(r"for a maker quoting one bitcoin a side, in dollars: speed alone cuts the day's loss by more than half, "
                    r"and still leaves a loss; the rest needs forecasts and fees")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        slow_k = 0.1 * abs(d["slow"]["n"] * d["slow"]["pnl_per_fill"]) / 1000
        fast_k = 0.1 * abs(d["fast"]["n"] * d["fast"]["pnl_per_fill"]) / 1000
        with self.voiceover(
            "The same prize on Bitcoin, in dollars. <bookmark mark='a'/> Chapter two's slow maker, quoting one bitcoin a "
            f"side, would have lost about {slow_k:.0f} thousand dollars on the seventeenth of May. <bookmark mark='b'/> "
            f"The idealised fast one, about {fast_k:.0f} thousand. <bookmark mark='c'/> Speed alone cuts the loss by more "
            "than half, and still leaves a loss: the rest needs forecasts and fee tiers."
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

    def arms(self):
        rows = [cmath(r"\text{prize}", r"=", r"\lambda_J (J - \tfrac{s^*}{2}) = \lambda_I \tfrac{s^*}{2}", font_size=36),
                cmath(r"\text{faster by } \varepsilon", r"\Rightarrow", r"\text{win every race}", font_size=36,
                      colors={r"\text{win every race}": FAST_C}),
                cmath(r"\text{equilibrium}", r":", r"\text{everyone invests; no one gains}", font_size=36,
                      colors={r"\text{everyone invests; no one gains}": BAD})]
        whys = [why(r"the value of the sniping races each unit of time, which investors pay in the spread"),
                why(r"in a continuous market any speed advantage, however small, wins the race outright"),
                why(r"so every firm buys speed; in the end all are equally fast, the prize is split as before, and the "
                    r"spending is a pure social cost: a prisoner's dilemma")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The arms race. <bookmark mark='a'/> The prize is the value of the sniping races, which investors pay "
            "through the spread. <bookmark mark='b'/> In a continuous market, being faster by any amount, however small, "
            "wins every race. <bookmark mark='c'/> So every firm buys speed; in the end they are equally fast again, the "
            "prize is split as before, and the money spent is a pure social cost. A prisoner's dilemma, in fibre and "
            "microwave towers."
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

    def measured(self):
        cards = VGroup(
            desk_question(r"London, measured", r"Aquilina, Budish and O'Neill (2022): races last microseconds, involve a "
                          r"handful of firms, cover about a fifth of volume, and tax all trading about half a basis point "
                          r"(Part 35)",
                          width=12.4, font_size=19),
            desk_question(r"Bitcoin, in our replay", r"the gap between the slow and the idealised fast maker of Chapter 2, "
                          r"about ten ticks a fill, is the same prize seen from the maker's chair", width=12.4, font_size=19),
            desk_question(r"the economics of speed", r"Baron, Brogaard, Hagströmer and Kirilenko (2019): among "
                          r"high-frequency firms, the fastest earn the most, and profits are concentrated in a few",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Is it real? <bookmark mark='a'/> On the London Stock Exchange, Matteo Aquilina, Budish and Peter O'Neill "
            "measured races lasting microseconds among a handful of firms, in about a fifth of trading volume, with a "
            "tax of about half a basis point on all trading. "
            "<bookmark mark='b'/> On Bitcoin, Chapter two's gap between the slow and the fast maker, about ten ticks a "
            "fill, is the same prize seen from the maker's chair. <bookmark mark='c'/> And Matthew Baron, Jonathan "
            "Brogaard, Björn Hagströmer and Andrei Kirilenko found that among high-frequency firms the fastest earn the "
            "most, with profits concentrated in a few."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def physics(self):
        km = 1150.0
        c = 299792.458
        t_air = 1000 * km / c
        t_fibre = t_air * 1.47
        rows = [cmath(r"\text{Chicago--New York}", r"\approx", rf"{km:,.0f}\ \text{{km}}".replace(",", "{,}"), font_size=36),
                cmath(r"\text{light in air}", r":", rf"{t_air:.1f}\ \text{{ms one way}}", font_size=38, colors={r"\text{light in air}": FAST_C}),
                cmath(r"\text{light in fibre}", r":", rf"{t_fibre:.1f}\ \text{{ms}}\ (n \approx 1.47)", font_size=36),
                cmath(r"\text{the prize}", r":", rf"{t_fibre - t_air:.1f}\ \text{{ms}}", font_size=40, colors={r"\text{the prize}": HURDLE})]
        whys = [why(r"roughly the great-circle distance between the futures exchanges near Chicago and the stock exchanges "
                    r"near New York"),
                why(r"the physical limit: microwave and laser links come close to it"),
                why(r"glass slows light by its refractive index, and fibre routes are longer than the straight line"),
                why(r"a few milliseconds, the edge that paid for towers between the two cities; a calculation, not a "
                    r"measured route")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The physics of the race. <bookmark mark='a'/> The futures exchanges near Chicago and the stock exchanges "
            "near New York are about eleven hundred and fifty kilometres apart. <bookmark mark='b'/> Light in air "
            f"covers that in about {t_air:.1f} milliseconds. <bookmark mark='c'/> In glass fibre, slowed by its "
            f"refractive index, about {t_fibre:.1f}. <bookmark mark='d'/> The difference, under two milliseconds, is "
            "what paid for chains of microwave towers between the two cities: a calculation from physics, not any "
            "firm's measured route."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def remedies(self):
        cards = VGroup(
            desk_question(r"frequent batch auctions", r"collect orders for, say, a tenth of a second, then clear them at "
                          r"one price: a tiny speed edge no longer wins, and firms compete on price (the research chapter)",
                          width=12.4, font_size=19),
            desk_question(r"speed bumps", r"IEX delays every incoming order by 350 microseconds, and reprices its own "
                          r"pegged orders before the delay ends, so stale pegged quotes are not picked off", width=12.4,
                          font_size=19),
            desk_question(r"asymmetric delays and fees", r"some venues delay only takers, or price cancels and order-to-"
                          r"trade ratios; each moves rents between makers and snipers", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The remedies proposed. <bookmark mark='a'/> Frequent batch auctions: collect orders for a fraction of a "
            "second, then clear them at one price, so a tiny speed edge no longer wins and firms compete on price. "
            "<bookmark mark='b'/> Speed bumps: IEX delays every incoming order by three hundred and fifty microseconds, "
            "and updates its own pegged orders before the delay ends. <bookmark mark='c'/> And asymmetric delays or "
            "fees, which move rents between makers and snipers."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def auction_example(self):
        rows = [cmath(r"\text{bids}", r":", r"100.02 \times 3,\ 100.01 \times 5,\ 100.00 \times 4", font_size=32, colors={r"\text{bids}": BUY_C}),
                cmath(r"\text{offers}", r":", r"100.00 \times 2,\ 100.01 \times 4,\ 100.03 \times 6", font_size=32,
                      colors={r"\text{offers}": SELL_C}),
                cmath(r"p^*", r"=", r"100.01:\ \text{demand } 8,\ \text{supply } 6 \Rightarrow 6\ \text{trade}", font_size=32,
                      colors={r"p^*": HURDLE})]
        whys = [why(r"all orders that arrived during the batch, sorted by price; time within the batch does not matter"),
                why(r"the same for offers"),
                why(r"one uniform price where demand meets supply; everyone trades at it, and the excess demand at that "
                    r"price is rationed pro rata")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How a batch auction clears. <bookmark mark='a'/> All the bids that arrived during the batch, sorted by "
            "price; when they arrived within the batch does not matter. <bookmark mark='b'/> The same for offers. "
            "<bookmark mark='c'/> One uniform price where demand meets supply, here a hundred dollars and a cent: six "
            "units trade, everyone at the same price, and the excess demand at that price is shared out in proportion. "
            "A microsecond earlier buys nothing."
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

    def adoption(self):
        cards = VGroup(
            desk_question(r"why exchanges keep continuous trading", r"Budish, Lee and Shim (2024) argue exchanges earn "
                          r"from selling speed (colocation, data) and have little private incentive to switch", width=12.4,
                          font_size=19),
            desk_question(r"costs of batching", r"fragmented liquidity if only one venue batches, the choice of interval, "
                          r"and new games at the batch boundary", width=12.4, font_size=19),
            desk_question(r"where batching already exists", r"opening and closing auctions, and some venues' periodic "
                          r"auctions: the idea is old; doing it every tenth of a second is the novelty", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it has not happened. <bookmark mark='a'/> Budish, Robin Lee and Shim argue that exchanges earn from "
            "selling speed, colocation and data, and have little private reason to switch. <bookmark mark='b'/> Batching "
            "has costs too: liquidity fragments if one venue batches alone, the interval must be chosen, and new games "
            "appear at the batch boundary. <bookmark mark='c'/> And batching already exists, in opening and closing "
            "auctions: doing it ten times a second is the novelty."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"if a market switched to batch auctions every 100 ms, what would happen to the sniping prize, to "
                       r"the spread, and to the value of being a microsecond faster?")
        with self.voiceover(
            "Pause and predict. If a market switched to batch auctions every tenth of a second, what would happen to the "
            "sniping prize, to the spread, and to the value of being a microsecond faster?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
