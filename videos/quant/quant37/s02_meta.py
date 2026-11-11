from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (GOOD, HURDLE, IMPACT_C, PART, PRICE_C, comma,
                                         fit_right, illustration, load)


class Meta(VoiceoverScene):
    def construct(self):
        ag = load("aggregate")
        self.card()
        self.metaorder()
        self.shortfall()
        self.path()
        self.who_pays()
        self.public(ag)
        self.detect()
        self.phi(ag)
        self.size(ag)
        self.question()

    def card(self):
        c = chapter_card(1, r"Metaorders", r"What does it cost to buy a lot of something?", part=PART)
        with self.voiceover("Chapter one. No institution buys a large position in one order. It splits the decision into "
                            "hundreds or thousands of child orders over hours or days. The whole is called a metaorder, "
                            "and its cost is the subject of this part."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def metaorder(self):
        rows = [cmath(r"Q", r"=", r"\textstyle\sum_i q_i", font_size=40, colors={r"Q": HURDLE}),
                cmath(r"\text{participation}", r"=", r"\frac{Q}{V_{\text{during}}}", font_size=36),
                cmath(r"I(Q)", r"=", r"\varepsilon\,(p_{\text{end}} - p_{\text{start}})", font_size=38,
                      colors={r"I(Q)": IMPACT_C})]
        whys = [why(r"a parent order of total size $Q$, sent as child orders $q_i$ by an algorithm or a trader"),
                why(r"its share of the market's volume while it runs: the main dial an executor controls"),
                why('signed terminal displacement, including information and other flow; not causal impact by itself')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The vocabulary. <bookmark mark='a'/> A parent order of total size Q is sent as child orders. <bookmark mark='b'/> Realized participation divides Q by the market volume during execution; specify whether that denominator includes our own trades. <bookmark mark='c'/> Signed terminal displacement is the end-minus-start price in the order's direction. That observable contains market news and other traders' flow as well as any mechanical impact, so displacement alone is not a causal estimate."
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

    def shortfall(self):
        rows = [cmath(r"\text{IS}", r"=", r"\textstyle\sum_i q_i (p_i - p_{\text{decision}}) + (Q - \sum_i q_i)(p_{\text{end}} "
                      r"- p_{\text{decision}})", font_size=28, colors={r"\text{IS}": IMPACT_C}),
                cmath(r"", r"=", r"\text{delay} + \text{spread and impact} + \text{timing} + \text{opportunity}",
                      font_size=30),
                cmath(r"\text{fees}", r"\ll", r"\text{impact}\ \ \text{(for large orders)}", font_size=34)]
        whys = [why(r"Perold (1988): the paper portfolio traded at the decision price, against the real one; the second "
                    r"term is what was never filled"),
                why(r"the shortfall splits into the cost of waiting to start, crossing and pushing the price, luck in the "
                    r"price's path, and the trades missed"),
                why('impact can dominate commissions for sufficiently large orders; compare matching cost units')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How cost is measured for a buy. <bookmark mark='a'/> Perold's implementation shortfall compares executed shares with a paper portfolio at the decision price, plus an explicitly chosen terminal mark for unfilled shares. The displayed formula excludes fees until added separately; sells require the signed convention. <bookmark mark='b'/> Delay, execution, timing and opportunity are accounting and modeling decompositions. A public tape does not separately identify mechanical impact from news. <bookmark mark='c'/> For large orders impact may dominate commissions, but the comparison must use consistent dollars or basis points."
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

    def path(self):
        g = axes([0, 3], [0, 1.15], x_length=8.4, y_length=4.2, xlabel=r"time, in units of the order's duration",
                 ylabel=r"price impact", xticks=[0, 1, 2, 3], yticks=[], font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        t1 = np.linspace(0, 1, 60)
        t2 = np.linspace(1, 3, 80)
        up = curve(ax, t1, np.sqrt(t1), IMPACT_C, stroke_width=3.5)
        down = curve(ax, t2, 2 / 3 + (1 - 2 / 3) * np.exp(-3 * (t2 - 1)), IMPACT_C, stroke_width=3.5)
        perm = DashedLine(ax.c2p(1, 2 / 3), ax.c2p(3, 2 / 3), color=GREY_B, stroke_width=1.5)
        labs = VGroup(label(r"during: concave", font_size=18, color=IMPACT_C).next_to(ax.c2p(0.5, 0.7), UP, buff=0.1),
                      label(r"after: partial reversion", font_size=18, color=IMPACT_C).next_to(ax.c2p(2.0, 0.85), UP,
                                                                                            buff=0.1),
                      label('illustrative two-thirds level', font_size=16, color=GREY_B).next_to(ax.c2p(2.5, 2 / 3), DOWN,
                                                                                         buff=0.15))
        ill = illustration('illustrative path; reversion fraction varies by sample and horizon')
        with self.voiceover(
            "An illustrative shape reported in some metaorder studies. <bookmark mark='a'/> During execution, average signed displacement can rise concavely. <bookmark mark='b'/> Afterwards it may partially revert. Moro and colleagues, and Bershova and Rakhlin, discuss such decay; the fraction and measurement horizon depend on conditioning and the sample. The two-thirds level here is illustrative, not a universal permanent fraction. The trader pays an average of fill prices rather than the terminal peak, and price reversion does not directly allocate a third of the order's total cost."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(up), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(Create(down), Create(perm), FadeIn(labs[1:]))
        self.wait(0.4)
        self.clear_scene()

    def who_pays(self):
        cards = VGroup(
            desk_question(r"impact is someone's revenue", 'counterparties receive fill prices; benchmark displacement is not their net profit after risk and hedging', width=12.4,
                          font_size=19),
            desk_question(r"temporary and permanent", 'liquidity, information and correlated future flow can all affect the path; a tape does not identify their shares', width=12.4, font_size=19),
            desk_question(r"Kyle's answer and the data's", r"Part 35's Kyle market makes all impact permanent and "
                          r"linear; real metaorders are concave and partly transient, which needs more than Kyle",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Who is on the other side. <bookmark mark='a'/> Sellers receive the transaction prices a buyer pays, but the difference from a benchmark is not automatically their net profit; hedging, inventory risk and subsequent prices matter. <bookmark mark='b'/> Reversion can be consistent with liquidity provision, while persistent displacement can reflect information or correlated future trading. This is an economic interpretation, not an identified decomposition. <bookmark mark='c'/> Kyle's specific equilibrium gives linear permanent pricing of order flow; richer models allow concavity and transience."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def public(self, ag):
        cards = VGroup(
            desk_question(r"metaorders are private", r"the studies use brokers' or funds' own execution records; a "
                          r"public tape shows trades, not who sent them or which belong together", width=12.4,
                          font_size=19),
            desk_question(r"what the tape does show", r"aggregate impact: the price change over a window against the "
                          r"window's signed volume, all traders together", width=12.4, font_size=19),
            desk_question(r"our data", rf"ten days of Binance's BTCUSDT perpetual trade tape, May 2023, "
                          rf"{comma(ag['n_min'])} minutes, about {comma(ag['v_day'])} BTC traded a day", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            f"""What we can measure. <bookmark mark='a'/> Parent-order links usually require brokers' or funds' records. The public aggregate-trade tape does not identify those parents. <bookmark mark='b'/> Here aggregate impact means the conditional association of a window's signed volume with its price change, using all traders together. <bookmark mark='c'/> Ten date files from May 2023 yield {ag['n_min']:,} one-minute intervals and mean recorded volume about {ag['v_day']/1000:.0f} thousand bitcoin per file. These are recorded spans, not an assertion of complete daily coverage; partial files and gaps affect day normalization."""
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def detect(self):
        cards = VGroup(
            desk_question(r"proprietary records", r"a broker's or fund's own child orders, linked to their parents: the "
                          r"gold standard, behind the published square-root law", width=12.4, font_size=19),
            desk_question(r"leaked account data", r"Mt.\ Gox's records identified accounts, so metaorders could be "
                          r"rebuilt from public-looking trades (Chapter 2)", width=12.4, font_size=19),
            desk_question(r"proxies from the tape", r"runs of same-sign trades, or broker codes on some exchanges: noisy, "
                          r"and biased toward the orders that were easy to see", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "How researchers see metaorders at all. <bookmark mark='a'/> Proprietary records, a broker's or a fund's "
            "own child orders linked to their parents: the gold standard. <bookmark mark='b'/> Leaked account data, as "
            "from the Mt. Gox exchange. <bookmark mark='c'/> Or proxies from the tape, such as runs of same-sign trades "
            "or broker codes: noisy, and biased toward the orders that were easy to spot."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def phi(self, ag):
        cols = {"10 s": GREY_B, "1 min": PRICE_C, "5 min": IMPACT_C}
        allv = [v for d in ag["phi"].values() for v in d["mean"] if v == v]
        top = float(np.ceil(max(abs(v) for v in allv) / 50) * 50)
        g = axes([-1, 1], [-top, top], x_length=6.4, y_length=4.4, xlabel=r"signed volume imbalance $\phi$",
                 ylabel=r"mean price change, ticks", xticks=[-1, 0, 1], yticks=[-top, 0, top], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        curves = {}
        for k, d in ag["phi"].items():
            xs = [c for c, m in zip(d["centers"], d["mean"]) if m == m]
            ys = [m for m in d["mean"] if m == m]
            curves[k] = VGroup(curve(ax, xs, ys, cols[k], stroke_width=3),
                               *[Dot(ax.c2p(a, b), radius=0.06, color=cols[k]) for a, b in zip(xs, ys)])
        leg = legend([(cols[k], rf"windows of {k}") for k in cols], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        mx = float(np.nanmax(ag["phi"]["1 min"]["mean"]))
        with self.voiceover(
            f"""Aggregate flow and prices on Bitcoin. <bookmark mark='a'/> For ten-second, one-minute and five-minute windows, plot conditional mean price change against buy-minus-sell volume divided by their sum. Days are pooled with bin-count weights, using the nearest populated center. <bookmark mark='b'/> These finite bins suggest a saturating pattern; Patzelt and Bouchaud discuss related associations. The largest one-minute bin mean is about {mx:.0f} ticks. This is same-window association with no causal intervention, held-out forecast or robust uncertainty band, and a flat conditional mean is not a hard limit on price moves."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves["10 s"]), Create(curves["1 min"]))
            vo.wait_until("b")
            self.play(Create(curves["5 min"]))
        self.wait(0.4)
        self.clear_scene()

    def size(self, ag):
        rows = ag["size"][1:]
        x = np.log10([r["q"] for r in rows])
        y = np.log10([r["impact"] for r in rows])
        g = axes([0.5, 2.5], [0.5, 2.5], x_length=6.0, y_length=4.4, xlabel=r"signed volume in a minute, BTC",
                 ylabel=r"price move in its direction, ticks", xticks=[1, 2], yticks=[1, 2],
                 xfmt=lambda v: f"10^{{{v:.0f}}}", yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=15)
        g.move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=IMPACT_C) for a, b in zip(x, y)])
        sl = ag["slope"]
        b0 = float(np.mean(y) - sl * np.mean(x))
        fit = Line(ax.c2p(x[0], b0 + sl * x[0]), ax.c2p(x[-1], b0 + sl * x[-1]), color=HURDLE, stroke_width=2.5)
        lin = DashedLine(ax.c2p(x[0], y[0]), ax.c2p(x[-1], y[0] + (x[-1] - x[0])), color=GREY_B, stroke_width=1.5)
        sq = DashedLine(ax.c2p(x[0], y[0]), ax.c2p(x[-1], y[0] + 0.5 * (x[-1] - x[0])), color=GOOD, stroke_width=1.5)
        leg = legend([(HURDLE, rf"fit: slope {sl:.2f}"), (GREY_B, r"linear"), (GOOD, r"square root")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            f"""And against absolute net volume. <bookmark mark='a'/> Group minutes by the magnitude of their signed volume, then show median magnitude and mean price change multiplied by its sign, on logarithmic scales. The smallest bin is excluded from the slope fit. <bookmark mark='b'/> The resulting finite-bin slope is {sl:.2f}, between one half and one in this sample. No parent orders are identified, and no confidence interval establishes a universal exponent. It is a descriptive contemporaneous association, distinct from the causal execution cost of one metaorder."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lin), Create(sq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('1. Square-root scaling', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('$1\\%$ of daily volume has terminal impact $10$ bp; hold $Y,\\sigma,V$ fixed.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Find the terminal impacts at $4\\%$ and $9\\%$, and compare linear scaling.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause one. One percent of daily volume has terminal displacement ten basis points. Keeping the model inputs fixed, compute the four-percent and nine-percent values under square-root and linear scaling.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
