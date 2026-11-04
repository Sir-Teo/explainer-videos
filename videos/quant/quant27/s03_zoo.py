from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import ml as ML
from videos.quant.quant27.common import (BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, OOS_C, PART, TREE, ask, comma,
                                         fit_right, house_lab, load)

FAMILY = {"OLS": LINEAR, "OLS-3": LINEAR, "ENet": LINEAR, "PCR": LINEAR, "PLS": LINEAR, "GBRT": TREE, "NN1": NET,
          "NN2": NET, "NN3": NET}
GROUPS = [(r"momentum", ("r1d", "r1w", "r4w", "r12w", "r26w"), MOM),
          (r"risk", ("vol28", "max28", "skew28", "beta", "ivol"), BAD),
          (r"liquidity and size", ("range7", "lqv", "dqv", "amihud"), TREE),
          (r"age", ("age",), COIN)]
NAMES = {"r1d": r"last day", "r1w": r"last week", "r4w": r"weeks 2--4", "r12w": r"weeks 5--12", "r26w": r"weeks 13--26",
         "vol28": r"volatility", "max28": r"max daily return", "skew28": r"skewness", "beta": r"beta to Bitcoin",
         "ivol": r"idiosyncratic vol", "range7": r"high--low range", "lqv": r"dollar volume", "dqv": r"volume change",
         "amihud": r"Amihud illiquidity", "age": r"days listed"}


class Zoo(VoiceoverScene):
    def construct(self):
        p, z = load("panel"), load("zoo")
        self.card()
        self.universe(p)
        self.features()
        self.models()
        self.protocol()
        self.lab()
        self.results(z)
        self.power(z)
        self.importance(z)
        self.question()

    def card(self):
        c = chapter_card(2, r"The model zoo", r"Which learner forecasts best, and can the test tell them apart?",
                         part=PART)
        with self.voiceover("Chapter two. The whole model zoo of Gu, Kelly and Xiu, run on a market where nobody can "
                            "claim the data were picked: every coin Binance has ever quoted in dollars."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def universe(self, p):
        weeks, count = np.asarray(p["weeks"]), np.asarray(p["count"], float)
        n = len(weeks)
        k_hold = int(np.searchsorted(weeks, 20210101))
        top = count.max() * 1.1
        g = axes([0, n - 1], [0, top], x_length=10.0, y_length=3.6, xlabel=r"week, July 2018 to December 2025",
                 ylabel=r"coins in the universe", xticks=[], yticks=[0, 100, 200, 300], font_size=13).move_to(DOWN * 0.4)
        ax = g.ax
        res = curve(ax, np.arange(k_hold), count[:k_hold], COIN, stroke_width=3)
        seal = Rectangle(width=ax.c2p(n - 1, 0)[0] - ax.c2p(k_hold, 0)[0], height=ax.c2p(0, top)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=GREY_D, fill_opacity=0.55).move_to(
            [(ax.c2p(k_hold, 0)[0] + ax.c2p(n - 1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, top)[1]) / 2, 0])
        seal_lab = label(r"2021--2025: sealed, read once in Chapter 15", font_size=18, color=GREY_A).move_to(seal)
        side = VGroup(
            MathTex(rf"{p['n_coins']}\ \text{{coins ever quoted}}", font_size=24, color=COIN),
            MathTex(rf"{p['n_research']}\ \text{{in the research years}}", font_size=24),
            MathTex(rf"{p['n_research_gone']}\ \text{{of them since delisted}}", font_size=24, color=BAD),
            MathTex(rf"{comma(p['obs_research'])}\ \text{{coin-weeks, 2018--2020}}", font_size=24, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.35).to_edge(RIGHT, buff=0.4)
        rule = wrapped_label(r"in a week's universe: listed at least 60 days, and a median of at least \$250{,}000 traded "
                             r"a day over the past four; the target is the next week's log return, to the last close if "
                             r"the coin is delisted. Binance's public archive keeps the dead coins, so the panel has no "
                             r"survivorship bias (Part 26)", 6.4, 15, GREY_A).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.4)
        with self.voiceover(
            "The data first. <bookmark mark='a'/> Binance's public archive keeps the daily candles of every pair it "
            "has ever listed, including the hundreds it has since delisted, so this panel has no survivorship bias. "
            "Each Sunday, the universe is every coin listed for at least sixty days that traded a median of a quarter "
            "of a million dollars a day over the last four weeks. <bookmark mark='b'/> In mid-2018 that is six coins. "
            "By the end of 2020, about a hundred and forty. <bookmark mark='c'/> Then the panel is sealed: the five "
            "years from 2021 are read once, at the end of this part, when they hold about three hundred coins a "
            "week. <bookmark mark='d'/> What is left for research is small: a hundred and seventy coins, sixty-two of "
            "them since delisted, and six thousand coin-weeks. Gu, Kelly and Xiu had thirty thousand stocks and sixty "
            "years. Keep that ratio in mind."
        ) as vo:
            self.play(FadeIn(g), FadeIn(rule))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(res), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(seal), FadeIn(seal_lab))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def features(self):
        cols = VGroup()
        for name, keys, col in GROUPS:
            items = VGroup(label(name, font_size=22, color=col),
                           *[label(NAMES[k], font_size=17, color=GREY_A) for k in keys]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.12)
            cols.add(items)
        cols.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(UP * 0.6)
        if cols.width > 12.8:
            cols.scale_to_fit_width(12.8)
        rank = cmath(r"c_{i,t}", r"=", r"2\,\frac{\operatorname{rank}_t(x_{i,t}) - 1}{N_t - 1} - 1\ \in [-1, 1]",
                     font_size=32, colors={r"c_{i,t}": HURDLE}).to_edge(DOWN, buff=1.0)
        note_ = note(r"each week, each characteristic is replaced by its cross-sectional rank (a missing value by the "
                     r"median, 0), as in Gu, Kelly and Xiu: the models see where a coin stands, not its raw level",
                     font_size=17, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Fifteen characteristics per coin, the crypto analogue of the stock zoo's ninety-four. <bookmark "
            "mark='a'/> Momentum at five horizons, from the last day to the last half year. Risk: volatility, the "
            "largest daily move, skewness, beta to Bitcoin and the volatility left over. Liquidity and size: the "
            "daily range, dollar volume, its recent change, and Amihud's illiquidity. And how long the coin has "
            "been listed. <bookmark mark='b'/> Each week every characteristic is replaced by its rank in the cross "
            "section, scaled to run from minus one to one. A model sees where a coin stands among its peers that "
            "week, never a raw level that drifts from one year to the next."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rank), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def models(self):
        rows = [cmath(r"\text{OLS}", r":", r"\min_\beta \textstyle\sum (y - c^{\top}\beta)^2\quad(\text{and OLS-3: "
                      r"momentum, volume, volatility})", font_size=28, colors={r"\text{OLS}": LINEAR}),
                cmath(r"\text{ENet}", r":", r"\min_\beta \textstyle\sum (y - c^{\top}\beta)^2 + \lambda\big(\alpha|\beta|_1 + "
                      r"\tfrac{1 - \alpha}{2}|\beta|_2^2\big)", font_size=28, colors={r"\text{ENet}": LINEAR}),
                cmath(r"\text{PCR, PLS}", r":", r"y \approx (C W_K)\,\theta,\ \ W_K = \text{top } K \text{ directions of } "
                      r"C\ \text{(PCR) or of } \operatorname{Cov}(C, y)\ \text{(PLS)}", font_size=28,
                      colors={r"\text{PCR, PLS}": LINEAR}),
                cmath(r"\text{GBRT}", r":", r"\hat f = \textstyle\sum_{m} \nu\, T_m(c),\ \ T_m \text{ a depth-2 tree "
                      r"fitted to the residuals}", font_size=28, colors={r"\text{GBRT}": TREE}),
                cmath(r"\text{NN1--3}", r":", r"\hat f = W_L\,\sigma(\cdots\sigma(W_1 c)),\ \ 32,\ 32\text{--}16,\ "
                      r"32\text{--}16\text{--}8\ \text{units, 5 seeds averaged}", font_size=28,
                      colors={r"\text{NN1--3}": NET})]
        whys = [why(r"the benchmark, all fifteen; and a three-variable model, Gu, Kelly and Xiu's strawman"),
                why(r"the elastic net: the lasso's selection and ridge's shrinkage at once, $\lambda$ chosen on validation"),
                why(r"dimension reduction: regress on a few combinations of the characteristics, chosen for their "
                    r"variance (PCR) or for their covariance with the target (PLS)"),
                why(r"boosting (Part 20's engine): many small trees, each correcting the last, shrunk by $\nu = 0.03$; "
                    r"stopped early on validation"),
                why(r"feed-forward networks with ReLU, an $L_1$ penalty, Adam, early stopping, and an ensemble of five "
                    r"seeds, exactly the paper's recipe")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The zoo, nine animals in three families. <bookmark mark='a'/> Ordinary least squares on all fifteen, and "
            "on three, the paper's strawman. <bookmark mark='b'/> The elastic net, which shrinks every coefficient and "
            "sets the useless ones exactly to zero. <bookmark mark='c'/> Two ways of regressing on a few combinations "
            "of the characteristics: principal components, chosen for their variance, and partial least squares, "
            "chosen for their covariance with the target. <bookmark mark='d'/> Gradient-boosted trees, the engine of "
            "Part 20, small trees each correcting the last. <bookmark mark='e'/> And three feed-forward networks of "
            "one, two and three hidden layers, each an average of five seeds, with the paper's penalty, optimiser and "
            "early stopping."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def protocol(self):
        years = [(r"2018", 0.0, 1.0), (r"2019", 1.0, 2.0), (r"2020", 2.0, 3.0)]
        line = NumberLine(x_range=[0, 3, 1], length=10.0, include_numbers=False, color=GREY_C).move_to(UP * 0.4)
        labels = VGroup(*[label(y, font_size=20).next_to(line.n2p((a + b) / 2), UP, buff=0.5) for y, a, b in years])

        def bar(a, b, col, y, txt):
            r = Rectangle(width=line.n2p(b)[0] - line.n2p(a)[0], height=0.34, stroke_width=0, fill_color=col,
                          fill_opacity=0.8).move_to([(line.n2p(a)[0] + line.n2p(b)[0]) / 2, y, 0])
            return VGroup(r, label(txt, font_size=15, color=BLACK).move_to(r))
        t1 = VGroup(bar(0.55, 1.0 - 0.5, LINEAR, -0.4, r"train"), bar(0.5, 1.0, HURDLE, -0.4, r"validate"),
                    bar(1.0, 2.0, OOS_C, -0.4, r"test 2019"))
        t2 = VGroup(bar(0.55, 1.5, LINEAR, -1.0, r"train"), bar(1.5, 2.0, HURDLE, -1.0, r"validate"),
                    bar(2.0, 3.0, OOS_C, -1.0, r"test 2020"))
        note_ = wrapped_label(r"expanding window, refitted once a year; validation: the last 26 weeks before the test year, "
                              r"for early stopping and the penalties; every label ends inside its own period. Targets "
                              r"winsorised at 1\% and 99\% for training only", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The protocol is Part 26's. <bookmark mark='a'/> Train on everything before the last half year, tune on "
            "that half year, and test on the next calendar year, 2019. <bookmark mark='b'/> Then extend the window, "
            "refit, and test on 2020. Every label ends inside its own period, nothing is shuffled, and the extreme "
            "weekly moves, which in coins can be several hundred percent, are clipped for training only, never for "
            "the test."
        ) as vo:
            self.play(Create(line), FadeIn(labels))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in t1], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in t2], lag_ratio=0.3), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The network ensemble, in the House", ML.MLPEnsemble.fit, "for s in self.seeds:", 8,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "In the House, the ensemble is a short loop. For each seed, a fresh network; batches drawn in a seeded "
            "random order; the loss is mean squared error; training stops when the validation loss stops improving. "
            "The forecast is the average of the five networks. Averaging is not decoration here: each network's "
            "forecast is mostly noise from its own initialisation, and the average keeps what they share."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def results(self, z):
        rows = z["rows"]
        models = z["models"]
        n = len(models)
        lo, hi = -2.5, 2.5
        g = axes([-0.6, n - 0.4], [lo, hi], x_length=9.0, y_length=4.4, xlabel=r"",
                 ylabel=r"quintile long-short Sharpe ratio, 2019--2020, equal weights", xticks=[],
                 yticks=[-2, -1, 0, 1, 2], font_size=13).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        se = {}
        bars, errs, names = VGroup(), VGroup(), VGroup()
        for i, m in enumerate(models):
            r = rows[m]
            sr = r["sr_ew"]
            s_ = math.sqrt((1 + sr ** 2 / 2) / r["years"])
            se[m] = s_
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, sr)[1]
            bars.add(Rectangle(width=0.5, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=FAMILY[m],
                               fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]))
            errs.add(Line(ax.c2p(i, max(sr - 2 * s_, lo)), ax.c2p(i, min(sr + 2 * s_, hi)), color=WHITE, stroke_width=2))
            names.add(label(m, font_size=16, color=FAMILY[m]).next_to(ax.c2p(i, lo), DOWN, buff=0.15))
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(n - 0.4, 0), color=GREY_B, stroke_width=1.5)
        r2s = [rows[m]["r2"] for m in models]
        side = VGroup(
            MathTex(rf"R^2_{{\text{{oos}}}}:\ {100 * min(r2s):.1f}\%\ \text{{to}}\ {100 * max(r2s):.1f}\%", font_size=24,
                    color=BAD),
            MathTex(rf"\pm 2\,\text{{s.e.}}\ \approx \pm {2 * np.mean(list(se.values())):.1f}", font_size=24),
            wrapped_label(rf"{rows[models[0]]['coins_week']:.0f} coins a week on average, {rows[models[0]]['years']:.1f} "
                          r"years of weekly tests. White bars: two standard errors of the Sharpe ratio (Lo 2002)", 3.3,
                          15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The results. <bookmark mark='a'/> First the R squared, out of sample, against a forecast of zero: every "
            "model is negative, between about minus one and a half and minus two and a half percent. On coins, a "
            "week is so noisy that no learner beats saying nothing. <bookmark mark='b'/> Then the portfolio: each "
            "week, buy the fifth of coins a model likes best and sell the fifth it likes least. The Sharpe ratios "
            "run from minus one point four for the three-layer network to about one for the boosted trees. "
            "<bookmark mark='c'/> But draw the error bars. Two years of weekly tests give a "
            "Sharpe ratio a standard error of about seven tenths, and every bar overlaps every other and zero. This "
            "test cannot rank the zoo. That is itself the first finding."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if rows[m]["sr_ew"] >= 0 else UP)
                                    for b_, m in zip(bars, models)], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e_) for e_ in errs], lag_ratio=0.1), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def power(self, z):
        rows = [cmath(r"\operatorname{se}(\widehat{SR})", r"\approx", r"\sqrt{(1 + SR^2/2)/T_{\text{years}}}", font_size=32,
                      colors={r"\operatorname{se}(\widehat{SR})": HURDLE}),
                cmath(r"T_{\text{years}}", r"\ge", r"4\,(1 + SR^2/2)/SR^2", font_size=32, colors={r"T_{\text{years}}": HURDLE}),
                cmath(r"SR_{\text{long-short}}", r"\approx", r"\sqrt{\tfrac{R^2}{1 - R^2}}\,\sqrt{N_{\text{bets}}}\,"
                      r"\sqrt{52}", font_size=32, colors={r"SR_{\text{long-short}}": NET})]
        whys = [why(r"Part 26: the Sharpe ratio's standard error from $T$ years of independent returns"),
                why(r"two standard errors from zero: a true Sharpe ratio of 1 needs six years, of 0.5 eighteen"),
                why(r"Chapter 1's arithmetic, weekly: the long-short's Sharpe ratio scales with the square root of the "
                    r"number of independent bets; 40 coins sharing one crypto factor are far fewer than 40 bets")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.3, buff=0.5, edge=6.9)
        cmp_ = VGroup(
            label(r"Gu, Kelly and Xiu: about 6{,}000 stocks a month, a 30-year test", font_size=19, color=GREY_A),
            label(r"here: about 40 coins a week, a 2-year test", font_size=19, color=COIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why can't it? <bookmark mark='a'/> A Sharpe ratio's standard error is roughly one over the square root of "
            "the years of data. <bookmark mark='b'/> To be two standard errors from zero, a true Sharpe ratio of one "
            "needs six years, and one of a half needs eighteen. <bookmark mark='c'/> And the strategy's Sharpe ratio "
            "grows with the square root of the number of independent bets, which, for forty coins that all move with "
            "Bitcoin, is far fewer than forty. Gu, Kelly and Xiu tested on thirty years of several thousand stocks. "
            "Here there are two years of forty coins. The models are the same; the power is not. The sealed five "
            "years, with three hundred coins a week, will be a much better judge."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(cmp_))
        self.wait(0.5)
        self.clear_scene()

    def importance(self, z):
        imp = z["importance"]
        feats = z["features"]
        models = [m for m in ("OLS", "GBRT", "NN3") if m in imp]
        panels = VGroup()
        for m in models:
            v = np.array([max(imp[m][f], 0.0) for f in feats])
            v = v / max(v.sum(), 1e-12)
            order = np.argsort(-v)[:6]
            rowsg = VGroup()
            for k in order:
                f = feats[k]
                col = next(c for _, ks, c in GROUPS if f in ks)
                bar = Rectangle(width=max(3.0 * v[k] / max(v.max(), 1e-12), 0.02), height=0.28, stroke_width=0,
                                fill_color=col, fill_opacity=0.85)
                rowsg.add(VGroup(label(NAMES[f], font_size=15, color=GREY_A), bar).arrange(RIGHT, buff=0.15))
            for r_ in rowsg:
                r_[1].align_to(rowsg, LEFT).shift(RIGHT * 1.9)
            rowsg.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            for r_ in rowsg:
                r_[1].next_to(r_[0], RIGHT, buff=0.15)
                r_[1].align_to(np.array([r_[0].get_left()[0] + 1.95, 0, 0]), LEFT)
            panels.add(VGroup(label(m, font_size=22, color=FAMILY[m]), rowsg).arrange(DOWN, aligned_edge=LEFT, buff=0.2))
        panels.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(UP * 0.4)
        if panels.width > 13.0:
            panels.scale_to_fit_width(13.0)
        foot = wrapped_label(r"importance: the fall in the training $R^2$ when a characteristic is set to its median, as "
                             r"a share of the total (Gu, Kelly and Xiu's measure), 2020 fit. Colour: the family of Chapter "
                             r"2's list", 12.4, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What do the models lean on? <bookmark mark='a'/> Set one characteristic to its median and see how much "
            "of the fit is lost. For least squares, the boosted trees and the deepest network alike, the top of the "
            "list is liquidity, size and age: dollar volume, Amihud's illiquidity, how long the coin has traded. "
            "Gu, Kelly and Xiu found the same family near the top for stocks, with momentum. <bookmark mark='b'/> "
            "That agreement is worth more than any of the Sharpe ratios: it says what the models are reaching for. "
            "Whether it is an edge, or the premium for holding coins that are hard to trade, is the next chapter's "
            "question."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in panels], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a model's weekly long-short Sharpe ratio on 40 coins over two years is 1.0. Give a 95\% interval, and "
                r"say how many coin-weeks a 30-stock-equivalent test would need to separate 1.0 from 0.5.")
        with self.voiceover(
            "Pause and predict. A model's long-short Sharpe ratio over two years of weekly tests on forty coins is "
            "one. Give a ninety-five percent interval. And how much longer a test would you need to tell a Sharpe "
            "ratio of one from one of a half?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
