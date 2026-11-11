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
        with self.voiceover("Chapter seven. Ten thousand technical-rule configurations inspired by the rule families studied by Brock, Lakonishok and LeBaron, and Sullivan, Timmermann and White. This is a House illustration, not an exact replication."):
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
                if k:
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
            f"The implementation samples {r['n']:,} parameter configurations from four technical-rule families with a fixed seed. <bookmark mark='a'/> Many configurations are strongly correlated; this is not ten thousand independent experiments or an exact reconstruction of a published grid. <bookmark mark='b'/> Positions earn the next daily excess-cash return, before implementation costs. Selection uses data through 1986, followed by a descriptive 1987 to 2020 comparison. Cash and market buy-and-hold are distinct benchmarks."
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
            f"The saved research eras differ sharply. <bookmark mark='a'/> Before 1987, {r['eras']['in']['n_beat_bh']} of {r['n']} configurations exceed the market's Sharpe ratio. <bookmark mark='b'/> During 1987 to 2020, {r['eras']['out']['n_beat_bh']} do. The earlier winner changes from {r['best_in']:.2f} to {r['best_out']:.2f}. These gross long-short excess-cash calculations do not establish market alpha, executable stale-price profits or a causal explanation of the decline."
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
            f"Each saved dot represents a rule, with earlier and later Sharpe ratios. <bookmark mark='a'/> The full set's cross-era correlation is {r['corr']:.2f}; rankings are far from stable. <bookmark mark='b'/> The earlier winner ranks {r['rank_out_of_best']:,} in the later era. The later sample is now public research data. Repeatedly studying it prevents treating it as a fresh untouched performance test."
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
                    cell.align_to(np.array([xs[i] - 1.2, 0, 0]), LEFT)
        tab = VGroup(*rows)
        foot = wrapped_label(r"every family's best rule was short-horizon: five days, half a percent, a short channel. "
                             r"They all bet that a move today continues tomorrow", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The table selects the best earlier configuration within each family. <bookmark mark='a'/> It reports that selected rule's earlier and later ratios, alongside family averages. The later outcomes are descriptive gross returns, with neither calibrated execution costs nor a causal correction. <bookmark mark='b'/> Short-horizon trend rules are prominent among these earlier winners. That pattern motivates checking return timing, nonsynchronous prices and implementation, rather than declaring a universal source of alpha."
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
        side = wrapped_label(r"Nonsynchronous prices can create index autocorrelation (Fisher 1966; Lo and MacKinlay 1990). This chart alone does not identify the mechanism's contribution, executable profits or the roles of costs, selection and structural change.",3.6,16,GREY_A).to_edge(RIGHT,buff=0.3)
        with self.voiceover(
            "The saved decade summaries show changing daily autocorrelation. <bookmark mark='a'/> Nonsynchronous trading is one plausible mechanism: stocks with stale recorded prices can make an aggregate index adjust gradually. Fisher discussed this in 1966, and Lo and MacKinlay studied nonsynchronous trading in 1990. <bookmark mark='b'/> A historical index return is not automatically an executable index trade. Costs, market structure, economic change and selection may also matter. This chart does not identify how much each mechanism caused the decline, or prove that the early rules were free of overfitting."
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
