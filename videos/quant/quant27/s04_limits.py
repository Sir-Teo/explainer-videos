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
        with self.voiceover('Chapter three. Examine where an apparent forecasting return comes from, what it costs to trade, and what these small descriptive comparisons cannot identify.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def papers(self):
        cards=VGroup(definition_card(r"U.S. stock study (2023)",wrapped_label(r"Avramov, Cheng and Metzker examine how economic restrictions, difficult-to-arbitrage stocks and turnover costs alter machine-learning portfolio results in their sample.",5.4,25),width=6.2,font_size=25,kind=r"Paper"),definition_card(r"Chinese A-share study (2022)",wrapped_label(r"Leippold, Wang and Zhou study machine learning in a different market, with different predictors, participants and constraints. Neither paper establishes a universal cross-market ranking.",5.4,25),width=6.2,font_size=25,kind=r"Paper")).arrange(RIGHT,buff=.3,aligned_edge=UP)
        with self.voiceover("Published studies motivate the questions. <bookmark mark='a'/> Avramov, Cheng and Metzker examine how economic restrictions, difficult-to-arbitrage stocks and trading costs alter machine-learning portfolio results in their American-stock sample. <bookmark mark='b'/> Leippold, Wang and Zhou study a different Chinese-market setting with different predictors, participants and constraints. Neither paper supplies a universal cross-market ranking. Our smaller crypto illustration examines quote-volume splits, without identifying the causal source of their differences.") as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a");self.wait(.1)
            vo.wait_until("b");self.play(FadeIn(cards[1]))
        self.clear_scene()

    def split(self, z):
        rows, models = z["rows"], z["models"]
        n = len(models)
        vals=[rows[m]["liq_split"][half] for m in models for half in ["liquid","illiquid"]]
        lo=float(np.floor(min(0,min(vals))-.1));hi=float(np.ceil(max(0,max(vals))+.1))
        g = axes([-0.6, n - 0.4], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"",
                 ylabel=r"tercile long-short Sharpe ratio, 2019--2020", xticks=[], yticks=list(np.linspace(lo,hi,5)), font_size=17).move_to(
            LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        bars, names = VGroup(), VGroup()
        for i, m in enumerate(models):
            for j, (half, col) in enumerate((("liquid", COIN), ("illiquid", BAD))):
                v = float(rows[m]["liq_split"][half])
                x = i + (j - 0.5) * 0.36
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=.26*(ax.c2p(1,0)[0]-ax.c2p(0,0)[0]), height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
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
            wrapped_label('Past four-week quote-volume split; forecast terciles within each half. Gross, short-sample diagnostics; no paired dependence-adjusted confidence intervals.', 3.3, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"The original splits each week's eligible coins by past quote volume, then sorts forecasts into thirds within each half. <bookmark mark='a'/> The more-liquid mean gross Sharpe is {liq:.2f}. <bookmark mark='b'/> The less-liquid mean is {ill:.2f}, and {better} of {n} models have a larger value there. <bookmark mark='c'/> These are selected, dependent, short-sample comparisons. They do not establish significance, a causal illiquidity premium, or a return achievable after spreads, impact and borrow."
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
        g = axes([-0.6, n - 0.4], [bot, top], x_length=7.4, y_length=4.2, xlabel=r"",
                 ylabel=r"\% a year: gross return, and its trading cost", xticks=[],
                 yticks=list(np.linspace(bot,top,5)), yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=17).move_to(
            LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        gross, c10, c50, names = VGroup(), VGroup(), VGroup(), VGroup()
        for i, m in enumerate(models):
            r = rows[m]
            for grp, v, col, dx in ((gross, r["mean_vw"], FAMILY[m], -0.2), (c10, r["cost"], HURDLE, 0.2),
                                    (c50, 5 * r["cost"], BAD, 0.2)):
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                grp.add(Rectangle(width=.28*(ax.c2p(1,0)[0]-ax.c2p(0,0)[0]), height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=0.85 if grp is not c50 else 0.35).move_to(
                    [ax.c2p(i + dx, 0)[0], (y0 + y1) / 2, 0]))
            names.add(label(m, font_size=16, color=FAMILY[m]).next_to(ax.c2p(i, bot), DOWN, buff=0.15))
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(n - 0.4, 0), color=GREY_B, stroke_width=1.5)
        leg = legend([(GREY_A, r"gross, quote-volume-weighted"), (HURDLE, r"cost at 10 bp a trade"),
                      (BAD, r"cost at 50 bp")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        hi_t = max(models, key=lambda m: rows[m]["cost"])
        lo_t = min(models, key=lambda m: rows[m]["cost"])
        side = wrapped_label(rf"Fixed 10 and 50 bp turnover scenarios, not a verified historical fee schedule or an impact model. Original annual 10 bp costs range from {100*rows[lo_t]['cost']:.1f}\% to {100*rows[hi_t]['cost']:.1f}\%. Quote volume is not market capitalisation.",3.3,20,GREY_A).next_to(leg,DOWN,buff=.35)
        fit_right(side)
        with self.voiceover(
            f"These are fixed fee-times-turnover scenarios. <bookmark mark='a'/> The gross portfolios use quote-volume weights, not market-capitalisation value weights. At ten basis points, annual scenario costs range from {100*min(rows[m]['cost'] for m in models):.1f} to {100*max(rows[m]['cost'] for m in models):.1f} percent. <bookmark mark='b'/> At fifty basis points, {sum(rows[m]['mean_vw']-5*rows[m]['cost']<0 for m in models)} of {n} have a negative scenario net arithmetic return. These calculations omit a validated historical fee schedule, spread, impact, borrow and capacity model. The original turnover convention is retained; these are not executable net-return estimates."
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
            desk_question(r"restrict the universe", 'Predefine liquidity and stress restrictions. A disappearing edge does not identify a friction premium; outcome-selected filters add search.', width=12.2,
                          font_size=29),
            desk_question(r"charge for every trade", r"turnover times a cost that grows with size and falls with "
                          r"liquidity (Part 26's engine); report the net Sharpe ratio, not the gross", width=12.2,
                          font_size=29),
            desk_question(r"weight by value, and look at the long side", 'Compare relevant weighting and long-only constraints. Quote-volume weights are not market-capitalisation weights; verify short availability.', width=12.2,
                          font_size=29),
        ).arrange(DOWN, buff=0.22).shift(DOWN * 0.3)
        head = label(r"Three restrictions before a signal is believed", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Evaluate economic restrictions as protocol choices. <bookmark mark='a'/> Compare liquid assets and stressed periods using rules fixed before evaluation; removing observations after seeing results creates another selection. A disappearing edge does not identify its cause. <bookmark mark='b'/> State turnover, fills, spreads, impact, fees and borrow, including position size. <bookmark mark='c'/> Compare weighting and long-only choices when relevant. Quote-volume weights are not market-cap weights. These are evaluation questions, not new strategies tested in this review."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask('Fixed hypothetical scenario: gross Sharpe 1.2 on all assets, 0.2 on a predeclared liquid half. What cost, capacity, uncertainty and selection evidence is needed before trading?')
        with self.voiceover(
            "Pause and predict with a fixed hypothetical scenario. A signal's gross Sharpe is one point two on all assets and point two on a predeclared liquid half. What information about costs, capacity, uncertainty and selection is needed before deciding who could trade it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
