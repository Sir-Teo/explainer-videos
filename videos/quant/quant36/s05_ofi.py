from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BAD, BID_C, GOOD, HURDLE, MID_C, OFI_C, PART, load)


class OFI(VoiceoverScene):
    def construct(self):
        o = load("ofi")
        self.card()
        self.define()
        self.example(o)
        self.by_hand()
        self.regress(o)
        self.depth(o)
        self.versus()
        self.deep_ofi()
        self.integrated()
        self.question()

    def card(self):
        c = chapter_card(4, r"Order-flow imbalance", r"What single number about the book best explains the next price "
                         r"change?", part=PART)
        with self.voiceover("Chapter four. Part thirty-five measured the price of trades. But trades are a minority of "
                            "book events: adds and cancellations move the queues too. Rama Cont, Arseniy Kukanov and Sasha "
                            "Stoikov asked what single number about the queues explains price changes best."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def define(self):
        rows = [cmath(r"e^{\text{bid}}_t", r"=", r"q^b_t\,\mathbb 1[p^b_t \ge p^b_{t-1}] - q^b_{t-1}\,\mathbb 1[p^b_t \le "
                      r"p^b_{t-1}]", font_size=30, colors={r"e^{\text{bid}}_t": BID_C}),
                cmath(r"e^{\text{ask}}_t", r"=", r"q^a_t\,\mathbb 1[p^a_t \le p^a_{t-1}] - q^a_{t-1}\,\mathbb 1[p^a_t \ge "
                      r"p^a_{t-1}]", font_size=30, colors={r"e^{\text{ask}}_t": ASK_C}),
                cmath(r"\text{OFI}", r"=", r"\textstyle\sum (e^{\text{bid}} - e^{\text{ask}})", font_size=36,
                      colors={r"\text{OFI}": OFI_C})]
        whys = [why(r"the change in buying interest at the best bid: size added, or the whole new queue if the bid rose, "
                    r"less size removed, or the whole old queue if it fell"),
                why(r"the same for selling interest at the best offer"),
                why(r"Cont, Kukanov and Stoikov (2014): net buying pressure at the top of the book over an interval, from "
                    r"adds, cancels and trades alike")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The definition. <bookmark mark='a'/> At the best bid, count size added, or the whole new queue if the bid "
            "rose, less size removed, or the whole old queue if it fell. <bookmark mark='b'/> The same at the best offer. "
            "<bookmark mark='c'/> Their difference, summed over an interval, is the order-flow imbalance: net buying "
            "pressure at the top of the book, from additions, cancellations and trades alike."
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

    def example(self, o):
        e = np.asarray(o["example"]["ofi"], float)
        dm = np.asarray(o["example"]["dmid"], float)
        n = min(len(e), len(dm))
        lim_e = float(np.ceil(np.abs(e).max()))
        lim_d = float(np.ceil(np.abs(dm).max() * 10) / 10)
        g1 = axes([0, n], [-lim_e, lim_e], x_length=8.0, y_length=2.4, xlabel="", ylabel=r"OFI, BTC", xticks=[],
                  yticks=[-lim_e, 0, lim_e], yfmt=lambda v: f"{v:.0f}", font_size=13).move_to(UP * 1.4)
        g2 = axes([0, n], [-lim_d, lim_d], x_length=8.0, y_length=2.4, xlabel=r"seconds", ylabel=r"mid change, \$",
                  xticks=[0, 60, 120], yticks=[-lim_d, 0, lim_d], font_size=13).move_to(DOWN * 1.8)
        b1 = VGroup(*[Rectangle(width=0.05, height=max(1e-3, abs(g1.ax.c2p(0, v)[1] - g1.ax.c2p(0, 0)[1])),
                                fill_color=GOOD if v > 0 else BAD, fill_opacity=0.8, stroke_width=0)
                      .move_to(g1.ax.c2p(i, v / 2)) for i, v in enumerate(e[:n])])
        b2 = VGroup(*[Rectangle(width=0.05, height=max(1e-3, abs(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1])),
                                fill_color=MID_C, fill_opacity=0.8, stroke_width=0)
                      .move_to(g2.ax.c2p(i, v / 2)) for i, v in enumerate(dm[:n])])
        with self.voiceover(
            "Two aligned minutes from the snapshots. <bookmark mark='a'/> The top plot shows net best-quote order-flow imbalance, with positive and negative pressure. <bookmark mark='b'/> The bottom plot is the mid change in the same interval. Their comovement is descriptive; this two-minute illustration does not compare forecasts, establish causation or measure the explanatory power of trades alone."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in b1], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in b2], lag_ratio=0.01))
        self.wait(0.4)
        self.clear_scene()

    def by_hand(self):
        rows = [cmath(r"t_0", r":", r"100.0 \times 5\ \big|\ 100.1 \times 4", font_size=36),
                cmath(r"t_1", r":", r"100.0 \times 7\ \big|\ 100.1 \times 3 \qquad e = (7 - 5) - (3 - 4) = 3", font_size=32),
                cmath(r"t_2", r":", r"100.1 \times 2\ \big|\ 100.2 \times 6 \qquad e = 2 - (-3) = 5", font_size=32),
                cmath(r"\text{OFI}", r"=", r"8,\quad \Delta\text{mid} = +\$0.10", font_size=38, colors={r"\text{OFI}": OFI_C})]
        whys = [why(r"bid and offer, price and size in BTC"),
                why(r"same prices: two added to the bid, one removed from the offer; both are buying pressure"),
                why(r"the offer of 3 was taken and the price rose: the old offer counts $-3$ on the ask side, and the "
                    r"new bid queue counts in full"),
                why(r"eight bitcoin of net pressure, and the mid rose a tick: OFI saw the cancellation that trades alone "
                    r"would have missed")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "By hand, three snapshots. <bookmark mark='a'/> Five bitcoin bid at a hundred, four offered at a hundred and "
            "ten cents. <bookmark mark='b'/> Then two are added to the bid and one is cancelled from the offer: three of "
            "buying pressure, with no trade at all. <bookmark mark='c'/> Then the offer is taken, the price rises a tick, "
            "and a new bid of two appears at the old offer: the vanished offer counts minus three on the ask side, and "
            "the new bid counts in full, five more. <bookmark mark='d'/> Eight bitcoin of net pressure, and the mid rose "
            "ten cents. Trades alone would have missed the cancellation."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def regress(self, o):
        f = o["fits"]
        hx = [-4.4, -2.0, 0.4, 2.8, 5.0]
        days = [r["day"] for r in f["1 s"]]
        head = VGroup(label(r"$R^2$ of $\Delta$mid on OFI", font_size=16, color=GREY_B),
                      *[label(d[5:], font_size=16, color=GREY_B if i < 2 else HURDLE) for i, d in enumerate(days)])
        tab = VGroup(head)
        for h in ("1 s", "10 s", "1 min"):
            tab.add(VGroup(label(h, font_size=20), *[MathTex(f"{r['r2']:.2f}", font_size=26) for r in f[h]]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        foot = wrapped_label('daily in-sample contemporaneous regressions, each refitted; yellow dates are held out only for other forecast experiments', 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        r10 = np.mean([r["r2"] for r in f["10 s"]])
        r60 = np.mean([r["r2"] for r in f["1 min"]])
        with self.voiceover(
            f"""Separate contemporaneous fit from prediction. <bookmark mark='a'/> Each day is refitted on its own same-interval mid changes and imbalance. Mean reported R squared is about {100 * r10:.0f} percent at ten seconds and {100 * r60:.0f} at a minute. Calling the weekend a test day elsewhere does not make these daily regressions held-out forecasts. The response and the explanatory variable share quote events, so both are endogenous. Different samples, units and targets prevent interpreting the comparison with Part thirty-five as a controlled doubling of explanatory power. No causal effect or robust inference is established here."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def depth(self, o):
        pts = o["depth_pts"]
        x = np.log10([p["depth"] for p in pts])
        y = np.log10(np.maximum([p["beta"] for p in pts], 1e-4))
        g = axes([float(np.floor(x.min() * 2) / 2), float(np.ceil(x.max() * 2) / 2)],
                 [float(np.floor(y.min() * 2) / 2), float(np.ceil(y.max() * 2) / 2)], x_length=6.6, y_length=4.4,
                 xlabel=r"$\log_{10}$ mean best-queue depth, BTC", ylabel=r"$\log_{10}$ impact per BTC of OFI",
                 xticks=[], yticks=[], font_size=14).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=OFI_C, fill_opacity=0.7) for a, b in zip(x, y)])
        sl = o["depth_slope"]
        b0 = float(np.mean(y) - sl * np.mean(x))
        x0, x1 = float(x.min()), float(x.max())
        fit = Line(ax.c2p(x0, b0 + sl * x0), ax.c2p(x1, b0 + sl * x1), color=HURDLE, stroke_width=2.5)
        st = VGroup(label(rf"slope {sl:.2f}", font_size=18, color=HURDLE),
                    label(r"theory: $-1$", font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        st.to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        with self.voiceover(
            f"""A descriptive depth comparison. <bookmark mark='a'/> Each point pairs a half-hour regression slope with average displayed depth from that interval. <bookmark mark='b'/> The stored pooled log-log slope is {sl:.2f}. The original routine floors nonpositive slopes before taking logs, so this is not an unrestricted log-law estimate. The plot also has its own positive display floor. The minus-one benchmark comes from a stipulated constant-depth model in which a queue's worth of imbalance moves the mid half a tick. Neither the scatter nor its unreported uncertainty identifies a causal response to removing liquidity."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def versus(self):
        rows = [cmath(r"\Delta p", r"\approx", r"\frac{\text{tick}}{2\,\bar q}\ \text{OFI}", font_size=38,
                      colors={r"\text{OFI}": OFI_C}),
                cmath(r"\text{Kyle}", r":", r"\Delta p = \lambda \times \text{trades}", font_size=34),
                cmath(r"\text{OFI}", r":", r"\text{trades} + \text{adds} - \text{cancels},\ \text{linear}", font_size=32)]
        whys = [why(r"the stylised model: each queue's worth of imbalance moves the mid by about half a tick"),
                why(r"Part 35 regressed returns on trades alone, and found concavity"),
                why('the distinct flow definitions can change descriptive shape; these separate regressions do not identify refill as the cause of trade-impact concavity')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Keep the benchmark's units explicit. <bookmark mark='a'/> With average queue q in base units and tick delta in dollars, the stylised coefficient is delta over twice q, dollars per base unit. <bookmark mark='b'/> Part thirty-five's signed-trade regressions use a different flow definition and sometimes different normalization. <bookmark mark='c'/> Including additions and cancellations can change the shape of a descriptive relation. These separate regressions do not prove that queue refill caused trade-impact concavity or that contemporaneous linearity predicts the next interval."
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

    def deep_ofi(self):
        cards = VGroup(
            desk_question(r"multi-level OFI", r"Xu, Gould and Howison (2018): the same imbalance at the second, "
                          r"third and deeper levels adds information, especially when the best queues are thin", width=12.4, font_size=19),
            desk_question(r"deep OFI", r"Kolm, Turiel and Westray (2023) fed order-flow imbalances, rather than raw "
                          r"prices and sizes, to deep networks, and reported better short-horizon forecasts: the input "
                          r"representation mattered more than the architecture", width=12.4, font_size=19),
            desk_question(r"contemporaneous, not predictive", r"OFI explains the price change in the same interval; "
                          r"forecasting the next interval is much harder (Chapter 6)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where it goes next. <bookmark mark='a'/> Ke Xu, Martin Gould and Sam Howison showed that the same imbalance at deeper levels of the book adds information, "
            "especially when the best queues are thin. <bookmark mark='b'/> Petter Kolm, Jeremy Turiel and Nicholas "
            "Westray fed order-flow imbalances, rather than raw prices and sizes, to deep networks, and reported better "
            "short-horizon forecasts: the input mattered more than the architecture. <bookmark mark='c'/> And a caution: "
            "everything in this chapter explains the price change in the same interval. Predicting the next one is "
            "Chapter six's much harder problem."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def integrated(self):
        cards = VGroup(
            desk_question(r"integrated OFI", r"Cont, Cucuringu and Zhang (2023): combine the imbalances of the first "
                          r"ten levels with their first principal component, and one number explains more than the best "
                          r"level alone", width=12.4, font_size=19),
            desk_question(r"cross-impact", r"in the same paper, once a stock's own integrated OFI is known, other "
                          r"stocks' OFIs add little to its contemporaneous return, but do help forecast the next ones",
                          width=12.4, font_size=19),
            desk_question(r"what this book can show", r"Binance's best-quote stream has only the best level, so this "
                          r"part measures best-level OFI; the deeper versions need the full depth feed", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two refinements. <bookmark mark='a'/> Rama Cont, Mihai Cucuringu and Chao Zhang combined the imbalances "
            "of the first ten levels through their first principal component: one integrated number that explains "
            "more than the best level alone. <bookmark mark='b'/> And across stocks: once a stock's own integrated "
            "imbalance is known, other stocks' imbalances add little to its price change in the same interval, but they "
            "do help forecast the next ones. <bookmark mark='c'/> Our feed carries only the best quotes, so this part "
            "measures the best-level version; the deeper ones need the full depth stream."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('A stipulated depth coefficient with units', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('\\delta=\\$0.10,\\quad\\bar q=8\\ \\mathrm{BTC},\\quad E=12\\ \\mathrm{BTC},\\qquad\\Delta m=\\frac\\delta{2\\bar q}E', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Constant-depth stylised relation; E is best-quote OFI in base units. This is not a causal estimate.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Compute dollars and ticks. What happens if depth doubles while E stays fixed?', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('Use the stipulated constant-depth relation: the tick is ten cents, average best queue is eight bitcoin and OFI is plus twelve bitcoin. Calculate the implied mid change in dollars and ticks. Then double depth holding flow fixed. State the coefficient units and why arithmetic under this assumption is not an empirical causal effect.'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()
