from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, ask, fit_right, load

FAMILY = {"OLS": LINEAR, "OLS-3": LINEAR, "ENet": LINEAR, "PCR": LINEAR, "PLS": LINEAR, "GBRT": TREE, "NN1": NET,
          "NN2": NET, "NN3": NET}


class Limits(VoiceoverScene):
    def construct(self):
        z = load("zoo")
        self.card()
        self.papers()
        self.split(z)
        self.costs(z)
        self.restrictions()
        self.question()

    def card(self):
        c = chapter_card(3, r"Where the edge lives", r"Is the machine's edge in the assets anyone can actually trade?",
                         part=PART)
        with self.voiceover("Chapter three. A forecast that works only where trading is expensive or impossible is "
                            "not an edge. Where does the machine's edge live?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def papers(self):
        cards = VGroup(
            firm_card(r"Avramov, Cheng and Metzker (2023)", r"deep-learning signals on U.S. stocks earn their profits in "
                      r"difficult-to-arbitrage stocks and in turbulent months: excluding microcaps, distressed firms or "
                      r"high-volatility periods considerably attenuates them; with reasonable trading costs, high "
                      r"turnover and extreme positions erode them further. Long positions and recent years hold up "
                      r"best", source=r"\textit{Management Science} 69(5)", width=6.2, font_size=19, kind=r"Paper"),
            firm_card(r"Leippold, Wang and Zhou (2022)", r"in Chinese A-shares, unlike the U.S., liquidity is the most "
                      r"important predictor; retail investors' dominance makes small stocks predictable at short "
                      r"horizons; performance stays significant after transaction costs", source=r"\textit{Journal of "
                      r"Financial Economics} 145(2)", width=6.2, font_size=19, kind=r"Paper"),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.2)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        with self.voiceover(
            "Two papers set the question. <bookmark mark='a'/> In 2023 Doron Avramov, Si Cheng and Lior Metzker "
            "showed that deep-learning signals on American stocks earn their money in the stocks that are hardest to "
            "arbitrage, and in turbulent months. Leave out the microcaps, the distressed firms or the volatile "
            "periods, and the profits shrink considerably; charge realistic costs, and the high turnover erodes them "
            "further. <bookmark mark='b'/> In China, Markus Leippold, Qian Wang and Wenyu Zhou found the opposite of "
            "the American ranking of predictors: liquidity matters most, because retail traders dominate the small "
            "stocks, and there the edge survives costs. The coin models of the last chapter leaned on liquidity too. "
            "So where does their edge, such as it is, live?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def split(self, z):
        rows, models = z["rows"], z["models"]
        n = len(models)
        lo, hi = -1.5, 1.5
        g = axes([-0.6, n - 0.4], [lo, hi], x_length=9.0, y_length=4.2, xlabel=r"",
                 ylabel=r"tercile long-short Sharpe ratio, 2019--2020", xticks=[], yticks=[-1, 0, 1], font_size=13).move_to(
            LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        bars, names = VGroup(), VGroup()
        for i, m in enumerate(models):
            for j, (half, col) in enumerate((("liquid", COIN), ("illiquid", BAD))):
                v = float(np.clip(rows[m]["liq_split"][half], lo, hi))
                x = i + (j - 0.5) * 0.36
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=0.3, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
            names.add(label(m, font_size=16, color=FAMILY[m]).next_to(ax.c2p(i, lo), DOWN, buff=0.15))
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(n - 0.4, 0), color=GREY_B, stroke_width=1.5)
        liq = np.mean([rows[m]["liq_split"]["liquid"] for m in models])
        ill = np.mean([rows[m]["liq_split"]["illiquid"] for m in models])
        better = sum(rows[m]["liq_split"]["illiquid"] > rows[m]["liq_split"]["liquid"] for m in models)
        leg = legend([(COIN, r"the more liquid half"), (BAD, r"the less liquid half")], font_size=17).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(
            MathTex(rf"\text{{average}}:\ {liq:.2f}\ \text{{vs}}\ {ill:.2f}", font_size=24),
            MathTex(rf"\text{{better in the illiquid half}}:\ {better}\ \text{{of}}\ {n}", font_size=24, color=BAD),
            wrapped_label(r"each week the coins are split at the median of their four-week dollar volume, and each model's "
                          r"forecast sorted into thirds within each half. Each bar alone carries a standard error near "
                          r"0.7", 3.3, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Split each week's coins at the median of their dollar volume and sort within each half. <bookmark "
            "mark='a'/> In the more liquid half, the nine models' long-short Sharpe ratios average almost exactly "
            "zero. <bookmark mark='b'/> In the less liquid half they average about point one seven, and six of the "
            "nine do better there. <bookmark mark='c'/> On two years, no single bar is distinguishable from zero. But "
            "the direction is Avramov, Cheng and Metzker's: what edge the machines find is in the coins that are "
            "hardest to trade."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[0::2]], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1::2]], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def costs(self, z):
        rows, models = z["rows"], z["models"]
        n = len(models)
        top = max(max(rows[m]["mean_vw"] for m in models), max(5 * rows[m]["cost"] for m in models)) * 1.1
        bot = min(min(rows[m]["mean_vw"] for m in models), 0) * 1.1
        g = axes([-0.6, n - 0.4], [bot, top], x_length=9.0, y_length=4.2, xlabel=r"",
                 ylabel=r"\% a year: gross return, and its trading cost", xticks=[],
                 yticks=[-0.4, 0, 0.4, 0.8], yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(
            LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        gross, c10, c50, names = VGroup(), VGroup(), VGroup(), VGroup()
        for i, m in enumerate(models):
            r = rows[m]
            for grp, v, col, dx in ((gross, r["mean_vw"], FAMILY[m], -0.2), (c10, r["cost"], HURDLE, 0.2),
                                    (c50, 5 * r["cost"], BAD, 0.2)):
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                grp.add(Rectangle(width=0.32, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=0.85 if grp is not c50 else 0.35).move_to(
                    [ax.c2p(i + dx, 0)[0], (y0 + y1) / 2, 0]))
            names.add(label(m, font_size=16, color=FAMILY[m]).next_to(ax.c2p(i, bot), DOWN, buff=0.15))
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(n - 0.4, 0), color=GREY_B, stroke_width=1.5)
        leg = legend([(GREY_A, r"gross, value-weighted"), (HURDLE, r"cost at 10 bp a trade"),
                      (BAD, r"cost at 50 bp")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        hi_t = max(models, key=lambda m: rows[m]["cost"])
        lo_t = min(models, key=lambda m: rows[m]["cost"])
        side = wrapped_label(rf"10 bp is Binance's base taker fee alone; the spread and impact on a coin that trades "
                             rf"\$250{{,}}000 a day can be several times that. Turnover is highest for {hi_t} "
                             rf"({100 * rows[hi_t]['cost']:.0f}\% a year at 10 bp) and lowest for {lo_t} "
                             rf"({100 * rows[lo_t]['cost']:.0f}\%)", 3.3, 15, GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Then the cost of getting there. <bookmark mark='a'/> Each model's gross annual return, value-weighted, "
            "next to what its weekly turnover costs at ten basis points a trade, Binance's base fee alone. That takes "
            "five to fourteen percent a year, the most for the boosted trees, whose rankings change the most from "
            "week to week. <bookmark mark='b'/> But a coin trading a quarter of a million dollars a day does not "
            "trade at the fee: its spread and impact can be several times larger. At fifty basis points, five of the "
            "nine lose money."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if rows[m]["mean_vw"] >= 0 else UP)
                                    for b_, m in zip(gross, models)], lag_ratio=0.08))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in c10], lag_ratio=0.08), FadeIn(side))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in c50], lag_ratio=0.08))
        self.wait(0.4)
        self.clear_scene()

    def restrictions(self):
        cards = VGroup(
            desk_question(r"restrict the universe", r"rerun without the least liquid assets, the distressed ones and the "
                          r"turbulent months; an edge that vanishes was a premium for bearing the friction", width=12.2,
                          font_size=20),
            desk_question(r"charge for every trade", r"turnover times a cost that grows with size and falls with "
                          r"liquidity (Part 26's engine); report the net Sharpe ratio, not the gross", width=12.2,
                          font_size=20),
            desk_question(r"weight by value, and look at the long side", r"equal weights put the money where trading is "
                          r"hardest; short positions in illiquid assets often cannot be had at all", width=12.2,
                          font_size=20),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "So every machine-learned signal gets three economic restrictions before it is believed. <bookmark "
            "mark='a'/> Restrict the universe: drop the least liquid, the distressed, the turbulent months. An edge "
            "that vanishes was a premium for bearing the friction. <bookmark mark='b'/> Charge for every trade, with a "
            "cost that rises with size and falls with liquidity, and report the net. <bookmark mark='c'/> And weight "
            "by value and look at the long side alone, because equal weights put the money where trading is hardest, "
            "and the short side of an illiquid asset often cannot be had."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a signal's long-short Sharpe ratio is 1.2 on all coins and 0.2 on the most liquid half. Is it "
                r"worthless? Who could trade it, and at what size?")
        with self.voiceover(
            "Pause and predict. A signal earns a Sharpe ratio of one point two on all coins, and point two on the "
            "more liquid half. Is it worthless? Who could trade it, and at what size?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
