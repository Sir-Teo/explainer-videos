from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, LINEAR, MKT, NET, PART, TREE, ask, comma, fit_right, load

ETFS = ("SPY", "QQQ", "EEM", "GLD", "XLE")


class Foundation(VoiceoverScene):
    def construct(self):
        p = load("pretrained")
        self.card()
        self.idea()
        self.tokens()
        self.kronos()
        self.pocket(p)
        self.result(p)
        self.lesson()
        self.question()

    def card(self):
        c = chapter_card(11, r"Foundation models", r"Can one model, trained on every market, forecast one it has never "
                         r"seen?", lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter eleven. Foundation models: one network, pretrained on every market at once, and asked "
                            "about a market it has never seen."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        cols = VGroup()
        for name, year, body, col in (
                (r"Chronos", r"Amazon, 2024", r"scale each series by its mean absolute value, cut the range into a few "
                 r"thousand bins, and train a language model on the bin numbers as if they were words", LINEAR),
                (r"TimesFM", r"Google, 2024", r"a decoder-only transformer on patches of 32 points, pretrained on about a "
                 r"hundred billion time points from web traffic, weather, retail and synthetic series", TREE),
                (r"Kronos", r"Tsinghua, 2025", r"a tokenizer for candlesticks (open, high, low, close, volume, value), "
                 r"then an autoregressive transformer on over 12 billion K-lines from 45 exchanges", NET)):
            cols.add(VGroup(label(name, font_size=28, color=col), label(year, font_size=16, color=GREY_B),
                            wrapped_label(body, 3.6, 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15))
        cols.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(UP * 0.4)
        head = label(r"pretrain once on everything; forecast anything, zero-shot", font_size=26).to_edge(UP, buff=0.5)
        src = note(r"Ansari et al.\ (2024); Das, Kong, Sen and Zhou (2024); Shi et al.\ (2025)", font_size=15,
                   color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Language models showed that one network, trained on enough text, can answer questions it was never "
            "trained for. The same recipe has been tried on numbers. <bookmark mark='a'/> Amazon's Chronos, in 2024, "
            "scales each series, cuts its range into a few thousand bins, and trains an ordinary language model on the "
            "bin numbers as if they were words. <bookmark mark='b'/> Google's TimesFM feeds a transformer patches of "
            "points from about a hundred billion observations: web traffic, weather, retail sales. <bookmark mark='c'/> "
            "And Kronos, from Tsinghua in 2025, is built for markets: it tokenizes candlesticks, open, high, low, close "
            "and volume together, and trains on more than twelve billion of them from forty-five exchanges. The promise "
            "is zero-shot forecasting: no fitting to the series you care about at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cols[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def tokens(self):
        rows = [cmath(r"\tilde x_t", r"=", r"x_t \big/ \tfrac{1}{C}\textstyle\sum_{s \le C} |x_s|", font_size=34,
                      colors={r"\tilde x_t": LINEAR}),
                cmath(r"v_t", r"=", r"\operatorname{bin}(\tilde x_t) \in \{1, \dots, B\}", font_size=34,
                      colors={r"v_t": LINEAR}),
                cmath(r"\mathcal L", r"=", r"-\textstyle\sum_t \log p_\theta(v_{t} \mid v_{<t})", font_size=34,
                      colors={r"\mathcal L": NET}),
                cmath(r"\hat x_{T+h}", r"\sim", r"p_\theta(\,\cdot \mid v_{\le T}),\ \ \text{sampled, then unscaled}",
                      font_size=34, colors={r"\hat x_{T+h}": NET})]
        whys = [why(r"scale by the context's mean absolute value, so a penny stock and an index look alike to the model"),
                why(r"quantise into $B$ bins (Chronos: 4{,}096): a number becomes a token, a word in a vocabulary"),
                why(r"the language model's loss, next-token cross-entropy: it learns a distribution over what comes next, "
                    r"not a single number"),
                why(r"forecasts are sampled paths, so a quantile or a volatility comes from the samples; Kronos's "
                    r"tokenizer codes a whole candlestick into a coarse and a fine token instead of one value")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "How does a number become a word? <bookmark mark='a'/> Divide by the context's average size, so that a "
            "penny stock and an index look alike. <bookmark mark='b'/> Cut the scaled range into bins: each value is now "
            "a token from a vocabulary of a few thousand. <bookmark mark='c'/> Train with the language model's own "
            "loss, the probability of the next token given all the earlier ones, which teaches a whole distribution of "
            "what comes next, not one number. <bookmark mark='d'/> Then forecast by sampling paths, as a language model "
            "writes sentences, and read off a median, a quantile, or a volatility. Kronos's tokenizer goes a step "
            "further and codes a whole candlestick into a coarse token and a fine one."
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
        self.wait(0.5)
        self.clear_scene()

    def kronos(self):
        claims = [(r"price forecasting, RankIC", r"+93\%\ \text{vs the best time-series foundation model}", NET),
                  (r"", r"+87\%\ \text{vs the best model trained from scratch}", NET),
                  (r"volatility forecasting, MAE", r"-9\%", TREE),
                  (r"synthetic candlesticks, fidelity", r"+22\%", COIN)]
        tab = VGroup()
        for j, (a, b, col) in enumerate(claims):
            y = 1.6 - 0.75 * j
            row = VGroup(label(a, font_size=20, color=GREY_A) if a else VMobject(), MathTex(b, font_size=28, color=col))
            row[1].move_to([2.2, y, 0])
            if a:
                row[0].move_to([-3.6, y, 0])
            tab.add(row)
        head = label(r"Kronos, zero-shot: the authors' reported gains", font_size=28).to_edge(UP, buff=0.5)
        caveat = VGroup(
            desk_question(r"what the House did not do", r"run Kronos itself: these are the authors' numbers on their own "
                          r"benchmarks, not replicated in this series", width=12.0, font_size=19),
            desk_question(r"what to ask", r"which markets and dates the pretraining corpus covered, against the test "
                          r"windows; and whether a better RankIC survives costs, as Chapter 2's did not", width=12.0,
                          font_size=19)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        src = note(r"Shi, Fu, Chen, Zhao, Xu, Zhang and Li (2025), arXiv:2508.02739", font_size=15,
                   color=GREY_C).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "What do its authors report? <bookmark mark='a'/> Zero-shot, on their benchmarks, a rank correlation "
            "between forecast and outcome ninety-three percent higher than the best time-series foundation model's, "
            "and eighty-seven percent higher than the best model trained from scratch; a nine percent lower error in "
            "forecasting volatility; and more realistic synthetic candlesticks. <bookmark mark='b'/> The House did not "
            "run Kronos, so these are the authors' numbers, not this series'. And they come with the questions every "
            "result in this part has had to answer: which markets and which years were in a corpus of twelve billion "
            "candlesticks, against the test windows; and whether a better rank correlation survives trading costs. "
            "So the House built a small foundation model of its own, to see what such a model can and cannot carry "
            "from one market to another."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(caveat, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pocket(self, p):
        rng = np.random.default_rng(3)
        n = 60
        a = np.cumsum(rng.normal(0, 0.25, n + 1))
        a = a - a.mean()
        g = axes([0, n + 1], [a.min() - 0.6, a.max() + 0.8], x_length=7.6, y_length=3.0, xlabel=r"day",
                 ylabel=r"$\log|r_t|$, minus the window's mean", xticks=[], yticks=[], font_size=13).move_to(
            LEFT * 2.2 + UP * 0.9)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(i, a[i]), radius=0.04, color=COIN) for i in range(n)])
        target = Dot(ax.c2p(n, a[n]), radius=0.08, color=NET)
        win = SurroundingRectangle(dots, color=GREY_B, buff=0.08, stroke_width=1.5)
        net = VGroup(label(r"MLP 64--32, three seeds", font_size=20, color=NET),
                     label(rf"{comma(p['n_windows'])} windows from {p['n_coins']} coins, 2018--2020", font_size=18,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 0.9)
        fit_right(net)
        rows = VGroup(
            label(r"zero-shot: never fitted to the ETF it forecasts", font_size=20, color=NET),
            label(r"EWMA ($\lambda = 0.94$): the RiskMetrics rule, with a fitted offset", font_size=20, color=HURDLE),
            label(r"HAR: 1-, 5- and 22-day averages, regressed on each ETF's first half", font_size=20, color=TREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        test = note(r"tested on the second half of each ETF's 2010--2020 history: " + ", ".join(ETFS), font_size=16,
                    color=GREY_B).next_to(rows, UP, buff=0.25)
        with self.voiceover(
            "The House's pocket foundation model. <bookmark mark='a'/> Take sixty days of a coin's log absolute "
            "returns, the size of each day's move with its sign thrown away, and subtract the window's mean, so every "
            "asset looks alike in scale. The target is the next day's. <bookmark mark='b'/> Pool such windows from "
            "every coin Binance quoted from 2018 to 2020 and train one small network on all of them. <bookmark "
            "mark='c'/> Then, without fitting anything more, ask it about five stock and commodity funds it has never "
            "seen, against two models that are fitted to each fund: the RiskMetrics exponential average, and the "
            "heterogeneous autoregression of Part 7, with daily, weekly and monthly averages."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02, run_time=1.5), Create(win))
            self.play(FadeIn(target, scale=1.5))
            vo.wait_until("b")
            self.play(FadeIn(net))
            vo.wait_until("c")
            self.play(FadeIn(test), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
        self.add(note(r"illustration: a simulated window", font_size=16, color=GREY_B).to_corner(UL, buff=0.25))
        self.wait(0.4)
        self.clear_scene()

    def result(self, p):
        e = p["etfs"]
        r2 = {k: {m: 1 - e[k][m] / e[k]["zero"] for m in ("ewma", "har", "net")} for k in ETFS}
        top = max(max(v.values()) for v in r2.values())
        g = axes([-0.6, len(ETFS) - 0.4], [0, max(0.05, top * 1.25)], x_length=9.0, y_length=4.2, xlabel=r"",
                 ylabel=r"$R^2$ of next-day $\log|r|$, out of sample", xticks=[], yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        names = VGroup()
        cols = {"ewma": HURDLE, "har": TREE, "net": NET}
        for i, k in enumerate(ETFS):
            for j, m in enumerate(("ewma", "har", "net")):
                v = max(r2[k][m], 0.0)
                x = i + (j - 1) * 0.26
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=0.22 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=max(y1 - y0, 0.01),
                                   stroke_width=0, fill_color=cols[m], fill_opacity=0.85).move_to(
                    [ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
            names.add(label(k, font_size=18).next_to(ax.c2p(i, 0), DOWN, buff=0.15))
        leg = legend([(HURDLE, r"EWMA, offset fitted"), (TREE, r"HAR, fitted"), (NET, r"pocket model, zero-shot")],
                     font_size=18).to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        fit_right(leg)
        wins = sum(r2[k]["net"] >= max(r2[k]["ewma"], r2[k]["har"]) for k in ETFS)
        side = wrapped_label(rf"the network beats or ties both fitted models on {wins} of {len(ETFS)} funds", 3.4, 17,
                             NET).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "The result. <bookmark mark='a'/> For each fund, the share of the variance of the next day's log move each "
            "model explains, on the second half of its history. RESULT_SENTENCE"
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05, run_time=2.5))
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"what transfers", r"the shape of volatility: clustering and slow decay, the stylised facts of "
                          r"Part 7, are the same in coins, stocks and gold, so a model of them can be learned anywhere",
                          width=12.2, font_size=20),
            desk_question(r"what does not", r"a return forecast: an edge that held in every market at once would be the "
                          r"first thing every pretrained model learned, and arbitraged", width=12.2, font_size=20),
            desk_question(r"how to read a zero-shot claim", r"count the corpus as part of the search: twelve billion "
                          r"candlesticks overlap almost any test window someone later chooses", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What carries from one market to another? <bookmark mark='a'/> The shape of volatility: the clustering and "
            "the slow decay that Part 7 found in every market are the same in coins, stocks and gold, so a model of "
            "them can be learned anywhere and used anywhere. <bookmark mark='b'/> A return forecast is a different "
            "matter. An edge that held in every market at once would be the first thing every pretrained model "
            "learned, and it would be traded away. <bookmark mark='c'/> And read a zero-shot claim with the counter "
            "in mind: a corpus of twelve billion candlesticks overlaps almost any test window someone later chooses, "
            "and the corpus is part of the search."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a foundation model pretrained on prices through 2024 is tested zero-shot on 2023. Name two ways the "
                r"test leaks, and design one that does not.")
        with self.voiceover(
            "Pause and predict. A foundation model pretrained on prices through 2024 is tested, zero-shot, on 2023. "
            "Name two ways the test leaks, and design one that does not."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
