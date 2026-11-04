from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, GOOD, GP_C, HURDLE, IC_C, OOS_C, PART, fit_right, load


class Combine(VoiceoverScene):
    def construct(self):
        c = load("combine")
        self.card()
        self.theory()
        self.signals(c)
        self.rules()
        self.table(c)
        self.reading(c)
        self.horizons()
        self.blend()
        self.question()

    def card(self):
        c = chapter_card(7, r"Alpha combination", r"Six signals, one forecast: how should they be weighted?", part=PART)
        with self.voiceover("Chapter seven. A desk never has one signal; Part twenty-nine mined thousands. Before the "
                            "optimizer sees them, they must become one forecast per asset."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theory(self):
        rows = [cmath(r"\alpha_i", r"=", r"\textstyle\sum_k w_k\, z_{ik}", font_size=38, colors={r"\alpha_i": IC_C}),
                cmath(r"IC^2_{\text{combined}}", r"=", r"\mathbf{ic}^\top C^{-1}\,\mathbf{ic}", font_size=38,
                      colors={r"IC^2_{\text{combined}}": GOOD}),
                cmath(r"w", r"\propto", r"C^{-1}\mathbf{ic}", font_size=38),
                cmath(r"K\ \text{independent signals}", r":", r"IC_{\text{combined}} = \sqrt{\textstyle\sum_k IC_k^2}",
                      font_size=32)]
        whys = [why(r"the combined forecast: a weighted sum of the standardised scores"),
                why(r"with $\mathbf{ic}$ the signals' ICs and $C$ the correlation of their scores, the best combination's "
                    r"IC, squared (Grinold and Kahn)"),
                why(r"the best weights: a regression of returns on the scores, the same algebra as a tangency portfolio"),
                why(r"uncorrelated signals add like independent bets: the fundamental law again, across signals")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The theory is Part thirty again. <bookmark mark='a'/> The forecast is a weighted sum of standardised "
            "scores. <bookmark mark='b'/> If the signals have ICs collected in a vector, and their scores have "
            "correlation matrix C, the best combination's IC squared is ic transpose C inverse ic. "
            "<bookmark mark='c'/> The best weights are C inverse times the ICs: a regression of returns on the scores, "
            "with the algebra of a tangency portfolio. <bookmark mark='d'/> Uncorrelated signals add like independent "
            "bets. And so the best weights inherit every problem of the tangency portfolio: estimated ICs, estimated "
            "correlations, and an optimizer that maximises their errors."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def signals(self, c):
        keys = c["keys"]
        tr, va = c["ic_train"], c["ic_valid"]
        mx = max(max(abs(tr[k]), abs(va[k])) for k in keys)
        bars = VGroup()
        sc = 3.0 / mx
        for j, k in enumerate(keys):
            y = 2.0 - 0.75 * j
            b1 = Rectangle(width=abs(tr[k]) * sc, height=0.26, fill_color=IC_C, fill_opacity=0.8, stroke_width=0)
            b2 = Rectangle(width=abs(va[k]) * sc, height=0.26, fill_color=OOS_C, fill_opacity=0.8, stroke_width=0)
            b1.move_to([0.0, y + 0.15, 0], aligned_edge=LEFT if tr[k] > 0 else RIGHT)
            b2.move_to([0.0, y - 0.15, 0], aligned_edge=LEFT if va[k] > 0 else RIGHT)
            nm = label(k, font_size=20, color=GREY_A).move_to([-4.6, y, 0])
            bars.add(VGroup(nm, b1, b2))
        axis = Line([0, 2.5, 0], [0, -2.2, 0], color=GREY_C, stroke_width=1.5)
        leg = legend([(IC_C, r"IC, 2018--19 (training)"), (OOS_C, r"IC, 2020 (validation)")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 2.4)
        fit_right(leg)
        foot = wrapped_label(r"daily rank ICs of each standardised exposure from Chapter 2, and Part 29's mined alpha, "
                             r"against the next day's return; bars left of the line are negative", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Six signals on the coins: the five style exposures of Chapter two, and the mined alpha of Part twenty-nine. "
            "<bookmark mark='a'/> In blue, each signal's average daily IC in 2018 and 2019; in teal, in 2020. "
            f"<bookmark mark='b'/> The mined alpha is the strongest in both, {tr['mined']:.3f} and then "
            f"{va['mined']:.3f}. Low volatility is next, with a negative sign. Momentum changed sign between the two "
            "periods, and reversal's IC grew several times over."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(leg), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(bars[-1], color=GOOD))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        cards = VGroup(
            desk_question(r"equal weights", r"each signal's sign from training, magnitude one: 1/N across signals", width=12.4,
                          font_size=19),
            desk_question(r"IC weights", r"in proportion to each training IC, ignoring the correlations", width=12.4,
                          font_size=19),
            desk_question(r"ridge regression", r"$C^{-1}\mathbf{ic}$, estimated by pooled regression of returns on the "
                          r"scores, with a penalty that shrinks it toward equal weights: the penalty set from 0 to $10^6$",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three combinations, from the most humble to the most ambitious. <bookmark mark='a'/> Equal weights, with "
            "each signal's sign from training. <bookmark mark='b'/> Weights in proportion to the training ICs, ignoring "
            "how the signals correlate. <bookmark mark='c'/> And the regression itself, pooled over every coin and day "
            "of training, with a ridge penalty that ranges from none to a great deal."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def table(self, c):
        cb = c["combos"]
        order = [("equal", r"equal weights"), ("IC-weighted", r"IC weights"), ("ridge 0", r"regression"),
                 ("ridge 10000", r"ridge, $10^4$"), ("ridge 1e+06", r"ridge, $10^6$")]
        hx = [-3.6, 0.6, 3.6]
        head = VGroup(label(r"combination", font_size=18, color=GREY_B), label(r"IC, 2018--19", font_size=18, color=IC_C),
                      label(r"IC, 2020", font_size=18, color=OOS_C))
        tab = VGroup(head)
        for k, nm in order:
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{cb[k]['train']:.3f}", font_size=26),
                           MathTex(f"{cb[k]['valid']:.3f}", font_size=26)))
        tab.add(VGroup(label(r"the mined alpha alone", font_size=20, color=GOOD),
                       MathTex(f"{c['ic_train']['mined']:.3f}", font_size=26), MathTex(f"{c['ic_valid']['mined']:.3f}",
                                                                                      font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.62 * j, 0])
        r0 = cb["ridge 0"]
        with self.voiceover(
            "The scores. <bookmark mark='a'/> On the training years, the regression wins, as it must: "
            f"{r0['train']:.3f}. <bookmark mark='b'/> On 2020 the order reverses. The regression falls to "
            f"{r0['valid']:.3f}. IC weights hold {cb['IC-weighted']['valid']:.3f}, equal weights "
            f"{cb['equal']['valid']:.3f}. <bookmark mark='c'/> And the mined alpha alone, {c['ic_valid']['mined']:.3f}, "
            "beats every combination."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:6]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:6]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(tab[6]))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, c):
        cards = VGroup(
            desk_question(r"why the regression lost", r"it fitted the correlations and the training ICs, and in 2020 "
                          r"momentum changed sign and reversal strengthened: estimated weights carry estimated errors", width=12.4, font_size=19),
            desk_question(r"why the best signal won", r"combining helps when the signals are of similar strength and "
                          r"weakly correlated; here one signal carried most of the information", width=12.4, font_size=19),
            desk_question(r"what desks do", r"shrink the combination toward equal or IC weights, refit slowly, and judge "
                          r"it on the information ratio of the traded book, not the IC of the forecast", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How to read it. <bookmark mark='a'/> The regression fitted training ICs and correlations, and then the signals "
            "moved: estimated weights carry estimated errors, exactly as in Part thirty. <bookmark mark='b'/> "
            "Combining helps most when the signals are of similar strength and weakly correlated; here one signal "
            "carried most of the information. <bookmark mark='c'/> Desks shrink the combination toward simple weights, "
            "refit slowly, and judge it on the traded book."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def horizons(self):
        rows = [cmath(r"\alpha_{i,t}", r"=", r"\textstyle\sum_k w_k\,\frac{1}{1 + \phi_k a/\gamma}\; IC_k\,\sigma_i\, z_{ik,t}",
                      font_size=34, colors={r"\frac{1}{1 + \phi_k a/\gamma}": GP_C}),
                cmath(r"\text{IC at horizon } h", r"\approx", r"IC_k(1)\,\frac{1 - (1-\phi_k)^h}{\phi_k\sqrt h}", font_size=32)]
        whys = [why(r"blending horizons: Chapter 5's discount enters the combination, so slow signals count for more in a "
                    r"book that trades slowly"),
                why(r"a signal's IC over $h$ days, if its one-day forecasting power decays geometrically and returns are "
                    r"independent: fast signals peak early, slow ones keep rising")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "One more ingredient: horizon. <bookmark mark='a'/> In a book that trades slowly, a fast signal's forecast has "
            "decayed before the trade is done, so Chapter five's discount belongs inside the combination. "
            "<bookmark mark='b'/> Equivalently, measure each signal's IC at the horizon over which you will hold: a fast "
            "signal's IC peaks after a day or two, a slow signal's keeps rising for weeks."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def blend(self):
        cards = VGroup(
            desk_question(r"combine forecasts", r"one combined alpha, one optimisation: opposite trades from different "
                          r"signals net out before they reach the market, and the risk model sees the whole book",
                          width=12.4, font_size=19),
            desk_question(r"combine portfolios", r"one book per signal, each optimised alone, then added: simple to run "
                          r"and attribute, but one book buys what another sells, and both pay the spread", width=12.4,
                          font_size=19),
            desk_question(r"the price of separation", r"with costs, the sum of separately optimal books is not the optimal "
                          r"book; crossing the trades internally recovers part of the difference", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And where to combine. <bookmark mark='a'/> Combine forecasts, and run one optimisation: opposite trades from "
            "different signals cancel before they reach the market, and the risk model sees the whole book. "
            "<bookmark mark='b'/> Or combine portfolios: a separate book for each signal, added together. Simpler to run "
            "and to attribute, but one book buys what another sells, and both pay the spread. <bookmark mark='c'/> With "
            "costs, the sum of separately optimal books is not the optimal book. Large firms recover part of the "
            "difference by crossing the trades internally."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"two signals each have IC 0.04, and their scores correlate 0.5. What is the IC of their best "
                       r"combination?")
        with self.voiceover(
            "Pause and predict. Two signals each have an IC of point zero four, and their scores correlate point five. "
            "What is the IC of their best combination?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
