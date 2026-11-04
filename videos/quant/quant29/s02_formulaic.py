from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load

NAMES = ["Alpha#12", "Alpha#41", "Alpha#101"]


class Formulaic(VoiceoverScene):
    def construct(self):
        c = load("classic")
        g = load("grid")
        self.card()
        self.paper()
        self.operators()
        self.tree()
        self.settings()
        self.coins(g)
        self.table(c)
        self.question()

    def card(self):
        c = chapter_card(1, r"Formulaic alphas", r"What does a signal look like when a machine is to search for it?",
                         part=PART)
        with self.voiceover("Chapter one. Before a machine can search for signals, a signal has to be something it can "
                            "write down. What does that look like?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paper(self):
        card = firm_card(r"Kakushadze (2016)", r"`101 Formulaic Alphas': 101 real-life trading signals published with "
                         r"their formulas, written in a small language of prices, volumes and a dozen operators. Each is "
                         r"a short-horizon bet on the cross-section of stocks",
                         numbers=((r"0.6\text{--}6.4", r"days: the alphas' average holding periods"),
                                  (r"15.9\%", r"their average pairwise correlation: low"),
                                  (r"\times", r"turnover explains little of the correlations")),
                         source=r"\textit{Wilmott} 84 (2016); arXiv 1601.00991", kind=r"Paper file", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "In 2016 Zura Kakushadze did something unusual for the industry: he published a hundred and one real trading "
            "signals, with their formulas. <bookmark mark='a'/> Each is a line or two in a small language: prices, "
            "volumes, and a dozen operators such as rank, correlation and delay. They hold positions for between "
            "about half a day and six days. <bookmark mark='b'/> And their average pairwise correlation is only "
            "sixteen percent: a hundred and one different, weak bets, which is exactly what you want to combine."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def operators(self):
        groups = [(r"fields", [r"\texttt{close}", r"\texttt{high}", r"\texttt{low}", r"\texttt{volume}", r"\texttt{ret}",
                               r"\texttt{vwap}"], QC.SPOT),
                  (r"across assets", [r"\texttt{rank}(x)"], QC.CASH),
                  (r"through time", [r"\texttt{ts\_mean}(x, d)", r"\texttt{ts\_std}(x, d)", r"\texttt{ts\_rank}(x, d)",
                                     r"\texttt{ts\_max}(x, d)", r"\texttt{ts\_min}(x, d)", r"\texttt{delta}(x, d)",
                                     r"\texttt{delay}(x, d)", r"\texttt{corr}(x, y, d)"], QC.OPTION),
                  (r"arithmetic", [r"$+\ -\ \times\ \div$", r"\texttt{neg}", r"\texttt{sign}", r"\texttt{abs}",
                                   r"\texttt{slog}: signed log"], QC.VEGA)]
        cols = VGroup()
        for title, items, col in groups:
            g = VGroup(label(title, font_size=22, color=col), *[label(t_, font_size=19) for t_ in items])
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            cols.add(g)
        cols.arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(UP * 0.4)
        note_ = wrapped_label(r"$d$ is a window in days (here 3, 5, 10 or 20). \texttt{rank} sorts the assets each day; "
                              r"the time-series operators look back over each asset's own past", 11.4, 18,
                              GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The language has three kinds of words. <bookmark mark='a'/> Fields: the day's close, high, low, volume, "
            "return, and a typical price. <bookmark mark='b'/> Operators across assets, chiefly rank, which sorts every "
            "asset each day. Operators through time: a moving average, a moving standard deviation, today's rank within "
            "the last d days, a change, a delay, a rolling correlation. <bookmark mark='c'/> And arithmetic. Every "
            "formula in this part is a sentence in this language."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]), FadeIn(cols[2]))
            vo.wait_until("c")
            self.play(FadeIn(cols[3]), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def tree(self):
        def node(text, col):
            t = label(text, font_size=22, color=col)
            box = RoundedRectangle(width=max(t.width + 0.4, 1.2), height=0.6, corner_radius=0.12, stroke_color=col,
                                   fill_color=col, fill_opacity=0.12)
            t.move_to(box)
            return VGroup(box, t)
        root = node(r"\texttt{mul}", QC.VEGA).move_to(UP * 2.2)
        a = node(r"\texttt{sign}", QC.VEGA).move_to(LEFT * 2.6 + UP * 0.9)
        b = node(r"\texttt{neg}", QC.VEGA).move_to(RIGHT * 2.6 + UP * 0.9)
        a1 = node(r"\texttt{delta}($\cdot$, 1)", QC.OPTION).move_to(LEFT * 2.6 + DOWN * 0.4)
        b1 = node(r"\texttt{delta}($\cdot$, 1)", QC.OPTION).move_to(RIGHT * 2.6 + DOWN * 0.4)
        a2 = node(r"\texttt{volume}", QC.SPOT).move_to(LEFT * 2.6 + DOWN * 1.7)
        b2 = node(r"\texttt{close}", QC.SPOT).move_to(RIGHT * 2.6 + DOWN * 1.7)
        nodes = [root, a, b, a1, b1, a2, b2]
        edges = VGroup(*[Line(p.get_bottom(), q.get_top(), color=GREY_C, stroke_width=2)
                         for p, q in ((root, a), (root, b), (a, a1), (b, b1), (a1, a2), (b1, b2))])
        f = label(r"Alpha\#12:\ \ \texttt{sign(delta(volume, 1))} $\times$ \texttt{(-1 * delta(close, 1))}", font_size=22,
                  color=FORMULA).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is Alpha number twelve as a tree. <bookmark mark='a'/> At the leaves, volume and close. One level up, "
            "their changes since yesterday. <bookmark mark='b'/> Then the sign of the volume change, and minus the "
            "price change, multiplied together. In words: if volume rose, bet against today's price move; if it fell, "
            "bet with it. <bookmark mark='c'/> Every formula is a tree like this, and that is what makes searching "
            "over them possible: trees can be grown, cut and spliced."
        ) as vo:
            self.play(FadeIn(a2), FadeIn(b2))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(b1), Create(edges[4]), Create(edges[5]))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(b), FadeIn(root), *[Create(e) for e in edges[:4]])
            vo.wait_until("c")
            self.play(FadeIn(f))
        self.wait(0.4)
        self.clear_scene()

    def settings(self):
        rows = [cmath(r"\text{delay}", r":", r"s_t \text{ uses data to the close of day } t;\ \text{traded from that close}",
                      font_size=30, colors={r"\text{delay}": FORMULA}),
                cmath(r"\text{neutralise}", r":", r"s_{t,i} - \tfrac1{n_t}\textstyle\sum_j s_{t,j}\quad"
                      r"\text{(or within each industry)}", font_size=30, colors={r"\text{neutralise}": FORMULA}),
                cmath(r"\text{weights}", r":", r"w_{t,i} \propto \operatorname{rank}(s_t)_i - \overline{\operatorname{rank}},"
                      r"\quad \textstyle\sum_i |w_{t,i}| = 2", font_size=30, colors={r"\text{weights}": FORMULA}),
                cmath(r"\text{decay}", r":", r"\tilde s_t = \textstyle\sum_{k=0}^{m-1}(m - k)\, s_{t-k}\big/\sum_k (m - k)",
                      font_size=30, colors={r"\text{decay}": FORMULA})]
        whys = [why(r"when the signal is known, and when it can first be traded: the commonest source of a too-good "
                    r"backtest is a delay of zero that could not be traded"),
                why(r"take out the day's average, so the book bets on differences between assets, not on the market"),
                why(r"the portfolio of this part: one dollar long and one short, in proportion to the demeaned rank"),
                why(r"an optional linear moving average of the signal, which trades less at the price of a slower "
                    r"signal; we do not use it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "A formula is not yet a trade. In practice it comes with settings. <bookmark mark='a'/> The delay: the "
            "signal for day t uses data up to that day's close, and is traded from that close onward, never before. A "
            "delay of zero that no one could have traded is the commonest way a formula looks too good. "
            "<bookmark mark='b'/> Neutralisation: subtract the day's average, across all assets or within each industry, "
            "so the book bets on differences, not on the market. <bookmark mark='c'/> The weights: here, one dollar long "
            "and one dollar short, in proportion to each asset's rank. <bookmark mark='d'/> And sometimes a decay, a "
            "moving average of the signal itself, which trades less but reacts more slowly. Every one of these choices "
            "is another dial a miner can turn, and every turn is a trial."
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

    def coins(self, g):
        d = np.asarray(g["dates"])
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12 + (d % 100) / 365
        y = np.asarray(g["per_day"], float)
        top = float(np.ceil(y.max() / 50) * 50)
        gr = axes([2018, 2021], [0, top], x_length=9.0, y_length=4.2, xlabel=r"", ylabel=r"eligible coins that day",
                  xticks=[2018, 2019, 2020, 2021], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 0.6 + DOWN * 0.3)
        ax = gr.ax
        c = curve(ax, x, y, FORMULA, stroke_width=2)
        split = DashedLine(ax.c2p(2020, 0), ax.c2p(2020, top), color=HURDLE)
        tags = VGroup(label(r"train", font_size=18, color=TRAIN_C).move_to(ax.c2p(2019, top * 0.92)),
                      label(r"validate", font_size=18, color=VALID_C).move_to(ax.c2p(2020.5, top * 0.92)))
        side = wrapped_label(rf"{g['n_coins']} coins were eligible on some day of 2018--2020 (listed for 60 days, median "
                             rf"daily volume above 250{{,}}000 USDT); a median of {g['median_per_day']:.0f} on a given day",
                             3.2, 15, GREY_A).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        fit_right(side)
        with self.voiceover(
            "Our hunting ground is Part twenty-seven's: every coin Binance has quoted in tether, listed or delisted, so "
            "nothing is lost to survivorship. <bookmark mark='a'/> On each day, a coin counts if it has traded for sixty "
            f"days and enough volume; there were {g['n_coins']} such coins in 2018 to 2020, a median of "
            f"{g['median_per_day']:.0f} on a given day. <bookmark mark='b'/> A formula is scored by its daily information "
            "coefficient: the rank correlation between today's signal and tomorrow's return across the coins. Train on "
            "2018 and 2019; validate on 2020; and keep 2021 to 2025 sealed."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(c), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(split), FadeIn(tags))
        self.wait(0.4)
        self.clear_scene()

    def table(self, c):
        hx = [-3.6, 0.6, 2.6, 4.6]
        head = VGroup(label(r"formula", font_size=18, color=GREY_B), label(r"IC, 2018--19", font_size=18, color=TRAIN_C),
                      label(r"IC, 2020", font_size=18, color=VALID_C), label(r"Sharpe, 2020", font_size=18, color=VALID_C))
        tab = VGroup(head)
        for nm in NAMES:
            r = c["rows"][nm]
            tab.add(VGroup(VGroup(label(nm, font_size=19), label(r"\texttt{" + r["formula"].replace("_", r"\_")
                                                                 .replace("^", r"\^{}").replace("#", r"\#")
                                                                 .split(", open")[0] + "}", font_size=12, color=GREY_A)
                                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
                           MathTex(rf"{r['train']['ic']:+.3f}\ (t\ {r['train']['t']:+.1f})", font_size=22),
                           MathTex(rf"{r['valid']['ic']:+.3f}\ (t\ {r['valid']['t']:+.1f})", font_size=22),
                           MathTex(rf"{r['sr_valid']:+.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 1.0 * j, 0])
            row[0].align_to(np.array([-6.0, 0, 0]), LEFT)
        foot = wrapped_label(r"information coefficient: the daily rank correlation of signal and next-day return, "
                             r"averaged; Sharpe ratio of the dollar-neutral rank portfolio, annualised over 365 days, before "
                             r"costs. On a 24-hour market a day's open is the previous close, which Alpha\#101 uses", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        r12, r41 = c["rows"]["Alpha#12"], c["rows"]["Alpha#41"]
        with self.voiceover(
            "Three of the hundred and one, run on coins. <bookmark mark='a'/> Each was built for American stocks a decade "
            "ago, and on coins in 2018 and 2019 all three have negative information coefficients: on this market they "
            f"point the wrong way. <bookmark mark='b'/> In 2020, Alpha forty-one turns to {r41['valid']['ic']:+.3f}, and "
            f"Alpha twelve to {r12['valid']['ic']:+.3f}. A formula's sign and size change from one market and one year to "
            "the next. That is the raw material of mining: thousands of weak relations that do not travel well."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3])) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"Alpha\#12 bets against today's move when volume rose. Which market behaviour would make it work, "
                       r"and which would make it fail?")
        with self.voiceover(
            "Pause and predict. Alpha twelve bets against today's price move when volume rose. What market behaviour "
            "would make it work, and what would make it fail?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
