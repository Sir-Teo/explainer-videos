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
                why(r"its impact: the price move over its life, in the direction of the trade ($\varepsilon = \pm 1$)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The vocabulary. <bookmark mark='a'/> A parent order of total size Q, sent as many child orders. "
            "<bookmark mark='b'/> Its participation rate: its share of the market's volume while it runs, the main dial "
            "an executor controls. <bookmark mark='c'/> And its impact: the price move over its life, in the direction "
            "of the trade."
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
                why(r"commissions are cents; for an order that is a real share of the day's volume, impact is the bill")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How the cost is measured. <bookmark mark='a'/> André Perold's implementation shortfall: the real "
            "portfolio against a paper one traded at the price when the decision was made, plus what was never filled. "
            "<bookmark mark='b'/> It splits into the cost of delay, of crossing the spread and pushing the price, the "
            "luck of the price's path, and the opportunity missed. <bookmark mark='c'/> For any order that is a real "
            "share of the day's volume, the commission is cents, and the impact is the bill."
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
                      label(r"about two-thirds remains", font_size=16, color=GREY_B).next_to(ax.c2p(2.5, 2 / 3), DOWN,
                                                                                         buff=0.15))
        ill = illustration(r"illustration: the shape reported in large metaorder data sets")
        with self.voiceover(
            "The shape every large study reports. <bookmark mark='a'/> While the metaorder runs, the price moves its "
            "way, concavely: fast at first, slower later. <bookmark mark='b'/> When it stops, the price reverts part of "
            "the way. Esteban Moro and colleagues, and Nataliya Bershova and Dmitry Rakhlin, found that roughly "
            "two-thirds of the peak remains. A trader who pays the peak and keeps two-thirds has paid one-third as "
            "pure cost."
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
            desk_question(r"impact is someone's revenue", r"the price moved against the buyer is the price earned by "
                          r"those who sold to it: market makers, and patient traders on the other side", width=12.4,
                          font_size=19),
            desk_question(r"temporary and permanent", r"the part that reverts is paid for liquidity; the part that "
                          r"stays is the market learning that someone wanted to buy", width=12.4, font_size=19),
            desk_question(r"Kyle's answer and the data's", r"Part 35's Kyle market makes all impact permanent and "
                          r"linear; real metaorders are concave and partly transient, which needs more than Kyle",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who receives the cost. <bookmark mark='a'/> Impact is someone's revenue: the price moved against the buyer "
            "is earned by those who sold to it, the market makers and the patient traders on the other side. "
            "<bookmark mark='b'/> The part that reverts is the price of liquidity. The part that stays is the market "
            "learning that someone wanted to buy. <bookmark mark='c'/> Kyle's market of Part thirty-five makes all of "
            "it permanent and linear. Real metaorders are concave and partly transient, which needs more than Kyle."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
        with self.voiceover(
            "What we can measure. <bookmark mark='a'/> Metaorders are private: the large studies use brokers' and funds' "
            "own records. A public tape shows trades, not who sent them. <bookmark mark='b'/> It does show aggregate "
            "impact: the price change over a window against the signed volume of everyone together. "
            "<bookmark mark='c'/> Our tape: ten days of Bitcoin's perpetual future in May twenty twenty-three, with "
            f"about {ag['v_day'] / 1000:.0f} thousand bitcoin traded a day."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
        with self.voiceover(
            "How researchers see metaorders at all. <bookmark mark='a'/> Proprietary records, a broker's or a fund's "
            "own child orders linked to their parents: the gold standard. <bookmark mark='b'/> Leaked account data, as "
            "from the Mt. Gox exchange. <bookmark mark='c'/> Or proxies from the tape, such as runs of same-sign trades "
            "or broker codes: noisy, and biased toward the orders that were easy to spot."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
            "Aggregate impact on Bitcoin. <bookmark mark='a'/> In windows of ten seconds, a minute and five minutes, "
            "the mean price change against the imbalance: buying minus selling over their sum. "
            "<bookmark mark='b'/> Linear near zero, then flat: beyond an imbalance of about a half, more one-sidedness "
            "buys no more price. Felix Patzelt and Jean-Philippe Bouchaud found the same sigmoid shape across "
            f"futures and stocks. At a minute, the strongest imbalances move the price about {mx:.0f} ticks."
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
            "And against size. <bookmark mark='a'/> Sort every minute by the size of its signed volume, and plot the "
            "price move in its direction, on logarithmic scales. <bookmark mark='b'/> The slope is "
            f"{sl:.2f}: concave, between a straight line and a square root. This is not yet the square-root law, "
            "which is about a single trader's metaorder over its whole life. But it is the same concavity, seen in "
            "everyone's flow at once."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lin), Create(sq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an order buys 1\% of the day's volume and moves the price 10 bp. Under a square-root law, what "
                       r"does an order of 4\% move it? And under a linear law?")
        with self.voiceover(
            "Pause and predict. An order buying one percent of the day's volume moves the price ten basis points. Under "
            "a square-root law, what does an order of four percent do? And under a linear one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
