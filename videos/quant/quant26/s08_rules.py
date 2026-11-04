from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant26.common import (BAD, GOOD, HURDLE, IS_C, MKT, NOISE, OOS_C, PART, RULE, ask, comma, fit_right,
                                         illustration, load)


class Rules(VoiceoverScene):
    def construct(self):
        r = load("rules")
        self.card()
        self.families()
        self.universe(r)
        self.hists(r)
        self.scatter(r)
        self.table(r)
        self.why_then(load("acf"))
        self.question()

    def card(self):
        c = chapter_card(7, r"Technical rules that weren't", r"Did ten thousand rules find anything?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter seven. Ten thousand technical trading rules, run the way Sullivan, Timmermann and "
                            "White ran them, on ninety-five years of the American market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def families(self):
        rng = np.random.default_rng(11)
        P = 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.011, 260)))
        t = np.arange(len(P))
        ma = np.convolve(P, np.ones(30) / 30, mode="full")[: len(P)]
        ma[:29] = np.nan
        hi = np.array([P[max(0, i - 20):i].max() if i > 0 else P[0] for i in range(len(P))])
        lo = np.array([P[max(0, i - 20):i].min() if i > 0 else P[0] for i in range(len(P))])
        panels = VGroup()
        titles = [(r"moving average", r"long when the price (or a short average) is above a long average"),
                  (r"filter", r"long after a rise of $x\%$ from the last low, short after a fall of $x\%$ from the high"),
                  (r"support and resistance", r"long on a close above the last $n$ days' high, short below their low"),
                  (r"channel breakout", r"the same, but only when the $n$-day range is narrower than $x\%$")]
        lo_y, hi_y = float(P.min() * 0.97), float(P.max() * 1.03)
        for k, (a, b) in enumerate(titles):
            g = axes([0, 260], [lo_y, hi_y], x_length=5.6, y_length=1.9, xticks=[], yticks=[], font_size=12)
            ax = g.ax
            items = VGroup(g, curve(ax, t, P, MKT, stroke_width=2))
            if k == 0:
                m = np.isfinite(ma)
                items.add(curve(ax, t[m], ma[m], HURDLE, stroke_width=2))
            elif k in (2, 3):
                items.add(curve(ax, t[21:], hi[21:], GOOD, stroke_width=1.5), curve(ax, t[21:], lo[21:], BAD,
                                                                                    stroke_width=1.5))
            else:
                pos = BT.rule_positions(P, {"family": "filter", "x": 0.04, "delay": 0, "hold": 0})
                ch = np.flatnonzero(np.diff(pos) != 0) + 1
                items.add(*[Dot(ax.c2p(i, P[i]), radius=0.05, color=GOOD if pos[i] > 0 else BAD) for i in ch])
            cap = VGroup(label(a, font_size=20, color=RULE), wrapped_label(b, 5.6, 14, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06)
            panels.add(VGroup(cap, items).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        panels.arrange_in_grid(2, 2, buff=(0.5, 0.35)).move_to(DOWN * 0.1)
        if panels.height > 7.2:
            panels.scale_to_fit_height(7.2)
        with self.voiceover(
            "The four families, as Brock, Lakonishok and LeBaron and then Sullivan, Timmermann and White defined them. "
            "<bookmark mark='a'/> Moving averages: long when the price, or a short average of it, is above a long "
            "average. <bookmark mark='b'/> Filters: long after the price rises some percent from its last low, short "
            "after it falls that percent from its last high. <bookmark mark='c'/> Support and resistance: long when the "
            "price closes above the highest close of the last n days, short below the lowest. <bookmark mark='d'/> And "
            "channel breakouts: the same, but only after the price has traded in a narrow range. Each comes with "
            "variants: a band around the trigger, a delay before acting, a fixed holding period."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(panels[k], shift=UP * 0.15))
        self.add(illustration(r"illustration: a simulated price path"))
        self.wait(0.4)
        self.clear_scene()

    def universe(self, r):
        fam = r["families"]
        rows = VGroup(*[VGroup(label(nm, font_size=22, color=RULE), MathTex(comma(fam[k]["n"]), font_size=28)).arrange(
            RIGHT, buff=0.5) for k, nm in (("ma", r"moving averages"), ("filter", r"filters"),
                                           ("sr", r"support and resistance"), ("cb", r"channel breakouts"))])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 5.2)
        head = MathTex(rf"{comma(len(BT.rule_grid()))}\ \text{{rules in the grid}}\ \to\ {comma(r['n'])}\ \text{{drawn}}",
                       font_size=34, color=HURDLE)
        eras = VGroup(
            MathTex(rf"\text{{in sample}}:\ 1926\text{{--}}1986,\ {comma(r['eras']['in']['T'])}\ \text{{days}}",
                    font_size=28, color=IS_C),
            MathTex(rf"\text{{out of sample}}:\ 1987\text{{--}}2020,\ {comma(r['eras']['out']['T'])}\ \text{{days}}",
                    font_size=28, color=OOS_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g = VGroup(head, rows, eras).arrange(DOWN, buff=0.5)
        foot = wrapped_label(r"each rule's position at the close earns the next day's market return over T-bills "
                             r"(long $+1$, short $-1$, out $0$); Sullivan, Timmermann and White's own in-sample era "
                             r"ended in 1986, as Brock, Lakonishok and LeBaron's did", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Combine the families with their bands, delays and holding periods and the House's grid has more than "
            "thirty-two thousand rules. <bookmark mark='a'/> Ten thousand were drawn from it: four thousand moving "
            "averages, six hundred filters, and the rest support, resistance and channels. <bookmark mark='b'/> Each "
            "is run on the daily American market, long, short or out, and earns the next day's return over Treasury "
            "bills. The in-sample era ends in 1986, where Sullivan, Timmermann and White's did, and the years from "
            "1987 to 2020 are the test."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(eras), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hists(self, r):
        e = np.linspace(-1.5, 2.0, 71)
        c = (e[:-1] + e[1:]) / 2
        hi, ho = np.asarray(r["eras"]["in"]["hist"], float), np.asarray(r["eras"]["out"]["hist"], float)
        top = max(hi.max(), ho.max()) * 1.1
        g = axes([-1.5, 2.0], [0, top], x_length=8.0, y_length=4.0, xlabel=r"a rule's annualised Sharpe ratio",
                 ylabel=r"rules", xticks=[-1, 0, 1, 2], yticks=[], font_size=14).to_edge(LEFT, buff=0.45).shift(DOWN * 0.3)
        ax = g.ax
        w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]

        def bars(h, col, op):
            return VGroup(*[Rectangle(width=w * 0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=op).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
        bi, bo = bars(hi, IS_C, 0.55), bars(ho, OOS_C, 0.7)
        bh = [DashedLine(ax.c2p(r["eras"][k]["sr_bh"], 0), ax.c2p(r["eras"][k]["sr_bh"], top), color=col, stroke_width=2)
              for k, col in (("in", IS_C), ("out", OOS_C))]
        side = VGroup(
            MathTex(rf"\text{{beat buy and hold, 1926--86}}:\ {comma(r['eras']['in']['n_beat_bh'])}", font_size=22,
                    color=IS_C),
            MathTex(rf"\text{{beat buy and hold, 1987--2020}}:\ {r['eras']['out']['n_beat_bh']}", font_size=22, color=OOS_C),
            MathTex(rf"\text{{best}}:\ {r['best_in']:.2f}\ \to\ {r['best_out']:.2f}", font_size=26, color=HURDLE),
            wrapped_label(r"dashed: buy and hold in each era (0.42, then 0.50). Before 1987 the whole distribution sat "
                          r"to the right of zero; after, it collapsed onto it", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The result, era by era. <bookmark mark='a'/> In sample, the whole distribution of rules sits to the right "
            "of zero, and seven hundred and fifty-seven of the ten thousand beat simply holding the market. This is "
            "what Brock and his co-authors saw in the Dow. <bookmark mark='b'/> After 1986 the distribution collapses "
            "onto zero. Sixteen rules beat buy and hold. The best rule of the first era, with its Sharpe ratio of one "
            "point six seven, earned two hundredths."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bi], lag_ratio=0.01), Create(bh[0]), FadeIn(side[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bo], lag_ratio=0.01), Create(bh[1]),
                      FadeIn(side[1:]), run_time=2.5)
        self.add(illustration(r"Ken French daily factors; 10{,}000 rules from the House's \texttt{backtest.rule\_grid}"))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, r):
        si, so = np.asarray(r["scatter"]["in"]), np.asarray(r["scatter"]["out"])
        g = axes([-1.0, 1.8], [-1.0, 1.0], x_length=6.4, y_length=4.4, xlabel=r"Sharpe ratio, 1926--1986",
                 ylabel=r"Sharpe ratio, 1987--2020", xticks=[-1, 0, 1], yticks=[-1, 0, 1], font_size=14).to_edge(
            LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.clip(a, -1, 1.8), np.clip(b, -1, 1)), radius=0.025, color=RULE, fill_opacity=0.6)
                        for a, b in zip(si, so)])
        diag = DashedLine(ax.c2p(-1, -1), ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        zero = Line(ax.c2p(-1, 0), ax.c2p(1.8, 0), color=GREY_D, stroke_width=1)
        best = Dot(ax.c2p(r["best_in"], r["best_out"]), radius=0.08, color=HURDLE)
        side = VGroup(
            MathTex(rf"\text{{correlation}}:\ {r['corr']:.2f}", font_size=28, color=RULE),
            MathTex(rf"\text{{the best rule}}:\ \#{comma(r['rank_out_of_best'])}\ \text{{after}}", font_size=26,
                    color=HURDLE),
            wrapped_label(r"1,500 of the rules, each a dot. Had the first era's ranking carried over, the cloud would lie "
                          r"along the diagonal; it lies along zero".replace("1,500", "1{,}500"), 3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Does doing well before 1987 predict doing well after? <bookmark mark='a'/> Each dot is a rule. If the "
            "first era's ranking had carried over, the cloud would lie along the diagonal. It lies along zero: the "
            "correlation between the eras is point one five. <bookmark mark='b'/> And the best rule of the first era, "
            "the gold dot, ranked three thousand two hundred and eighty-first in the second."
        ) as vo:
            self.play(FadeIn(g), Create(diag), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.001, run_time=2.5), FadeIn(side[0]),
                      FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(best, scale=1.6), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def table(self, r):
        fam = r["families"]
        head = VGroup(*[label(h, font_size=18, color=GREY_A) for h in (r"family", r"its best rule, 1926--86",
                                                                       r"then", r"after", r"family average")])
        rows = [head]
        for k, nm in (("ma", r"moving average"), ("filter", r"filter"), ("sr", r"support/resistance"),
                      ("cb", r"channel breakout")):
            f = fam[k]
            rows.append(VGroup(label(nm, font_size=18, color=RULE), label(f["best"].replace("%", r"\%"), font_size=15),
                               MathTex(f"{f['sr_in']:.2f}", font_size=22, color=IS_C),
                               MathTex(f"{f['sr_out']:+.2f}", font_size=22, color=OOS_C),
                               MathTex(rf"{f['mean_in']:.2f} \to {f['mean_out']:+.2f}", font_size=20, color=GREY_A)))
        xs = [-5.6, -2.3, 1.6, 2.9, 4.8]
        for j, row in enumerate(rows):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.0 - 0.8 * j, 0])
                if i < 2:
                    cell.align_to([xs[i] - 1.2, 0, 0], LEFT)
        tab = VGroup(*rows)
        foot = wrapped_label(r"every family's best rule was short-horizon: five days, half a percent, a short channel. "
                             r"They all bet that a move today continues tomorrow", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Family by family. <bookmark mark='a'/> The best moving average used five days; the best filter, half a "
            "percent; the best support and resistance rule, five days; the best channel, twenty. The filter kept a "
            "Sharpe ratio of point three, below the market's; the other three fell to about zero or below, and every "
            "family's average went with them. <bookmark mark='b'/> Notice what the winners have "
            "in common. They are all very short-horizon, and they all bet on one thing: that a move in the market today "
            "continues tomorrow."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def why_then(self, a):
        rows = a["rows"]
        g = axes([-0.6, len(rows) - 0.4], [-0.1, 0.32], x_length=8.2, y_length=4.0, xlabel=r"decade",
                 ylabel=r"autocorrelation of the market's daily returns, one day apart", xticks=[], yticks=[-0.1, 0, 0.1,
                                                                                                      0.2, 0.3],
                 font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, row in enumerate(rows):
            v = row["rho1"]
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.5, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                                      fill_color=IS_C if row["decade"] < 1987 else OOS_C, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                label(r"1926" if row["decade"] == 1926 else rf"{row['decade']}s", font_size=12, color=GREY_A).next_to(
                    ax.c2p(i, -0.1), DOWN, buff=0.1)))
        side = wrapped_label(r"an index of thousands of stocks, many traded only now and then: yesterday's news reaches "
                             r"their recorded prices today, so the index's returns trail into the next day (Fisher 1966; "
                             r"Lo and MacKinlay 1990). Nobody could trade the index at those stale prices; as trading "
                             r"became continuous, and index futures and ETFs arbitraged it, the effect went", 3.6, 15,
                             GREY_A).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Why did it work before? <bookmark mark='a'/> Because the market index really did continue its moves. Its "
            "daily returns were positively autocorrelated for decades, reaching nearly point three in the 1970s. The "
            "reason is mechanical. An index of thousands of stocks includes many that traded only now and then, so "
            "yesterday's news reached their recorded prices today, and the index's return trailed into the next day. "
            "Lawrence Fisher pointed this out in 1966; Andrew Lo and Craig MacKinlay measured it in 1990. "
            "<bookmark mark='b'/> But nobody could buy the index at those stale prices. As trading became continuous, "
            "and index futures and exchange-traded funds arbitraged the index, the autocorrelation faded, and after "
            "2000 it turned negative. The rules were not overfitted to noise. They were fitted to a feature of the "
            "data that was never tradable, and that the market then removed."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"the best rule's in-sample $t$-statistic is above 13, so no correction for ten thousand tries can "
                r"explain it away. Which of this part's checks, if any, could have warned you before 1987?")
        with self.voiceover(
            "Pause and predict. The best rule's in-sample t-statistic is above thirteen, so no correction for ten "
            "thousand tries can explain it away. Which of this part's checks, if any, could have warned you before 1987?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
