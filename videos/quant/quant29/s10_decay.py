from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load, tt


class Decay(VoiceoverScene):
    def construct(self):
        d = load("decay")
        self.card()
        self.lags(d)
        self.years(d)
        self.model()
        self.factory()
        self.crowding()
        self.question()

    def card(self):
        c = chapter_card(9, r"Decay, crowding and the alpha factory", r"How long does a mined signal last, and who else "
                         r"has found it?", part=PART)
        with self.voiceover("Chapter nine. A signal can fade in two ways: over the days after it is measured, and over "
                            "the years, as others find it. How long does a mined signal last?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lags(self, d):
        L = d["lag"]
        hs = np.array(sorted(int(k) for k in L), float)
        tr = np.array([L[str(int(h))]["train"] for h in hs])
        va = np.array([L[str(int(h))]["valid"] for h in hs])
        top = float(np.ceil(max(tr.max(), va.max()) * 100 + 1) / 100)
        g = axes([1, hs[-1]], [0, top], x_length=7.2, y_length=4.4, xlabel=r"the day ahead, $h$",
                 ylabel=r"IC with the return on day $t + h$ alone", xticks=[1, 5, 10], yticks=[0, top / 2, top],
                 yfmt=lambda v: f"{v:.2f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lt = VGroup(curve(ax, hs, tr, TRAIN_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.05, color=TRAIN_C)
                                                                  for a, b in zip(hs, tr)])
        lv = VGroup(curve(ax, hs, va, VALID_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.05, color=VALID_C)
                                                                  for a, b in zip(hs, va)])
        leg = legend([(TRAIN_C, r"2018--19"), (VALID_C, r"2020")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(label(r"the best random formula:", font_size=15, color=GREY_B),
                      label(tt(d["formula"], 44), font_size=13, color=FORMULA),
                      wrapped_label(r"Kakushadze's 101 alphas hold for 0.6 to 6.4 days on average; this one fades far "
                                    r"more slowly", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(
            leg, DOWN, buff=0.35)
        fit_right(side)
        h10 = L[str(int(hs[-1]))]
        with self.voiceover(
            "First, over the days. <bookmark mark='a'/> Take the best random formula, and ask how well today's signal "
            "predicts the return on each day ahead, one day at a time. <bookmark mark='b'/> On the training years its IC "
            f"is {tr[0]:.3f} for tomorrow, and still {h10['train']:.3f} ten days out. In 2020 the same: it fades "
            f"slowly, from {va[0]:.3f} to {h10['valid']:.3f}. A fast alpha would fall to zero within days; this one "
            "describes what kind of coin something is, and that changes slowly. Slow signals trade less and cost less, "
            "which matters in Chapter 13."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def years(self, d):
        by = d["by_year"]
        ys = sorted(by)
        vals = [by[y] for y in ys]
        top = float(np.ceil(max(vals) * 100 + 1) / 100)
        g = axes([2017.4, 2020.6], [0, top], x_length=6.0, y_length=4.0, xlabel=r"", ylabel=r"mean daily IC",
                 xticks=[2018, 2019, 2020], yticks=[0, top / 2, top], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                 font_size=15).move_to(LEFT * 2.2 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=(VALID_C if int(y) == 2020 else TRAIN_C), fill_opacity=0.85).move_to(
            ax.c2p(int(y), 0), aligned_edge=DOWN) for y, v in zip(ys, vals)])
        labs = VGroup(*[MathTex(f"{v:.3f}", font_size=22).next_to(b, UP, buff=0.1) for b, v in zip(bars, vals)])
        side = wrapped_label(r"three years is far too short to measure decay through time; the sealed years 2021--25 "
                             r"will add five", 4.0, 16, GREY_A).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            "Second, over the years. <bookmark mark='a'/> Year by year the same formula scored "
            f"{vals[0]:.3f}, {vals[1]:.3f} and {vals[2]:.3f}. <bookmark mark='b'/> A slight fall, or none: three years "
            "cannot tell. The sealed years will add five more."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"IC_h", r"\approx", r"IC_1\,\phi^{\,h - 1}", font_size=34, colors={r"IC_h": TRAIN_C}),
                cmath(r"\text{turnover}", r"\propto", r"\sqrt{1 - \operatorname{Corr}(s_t, s_{t-1})}", font_size=32),
                cmath(r"\text{net}", r"=", r"\text{edge} - \text{cost} \times \text{turnover}", font_size=34,
                      colors={r"\text{net}": GOOD}),
                cmath(r"\text{edge}_{\text{after}}", r"\approx", r"0.42 \times \text{edge}_{\text{before}}\quad "
                      r"\text{(McLean and Pontiff)}", font_size=30, colors={r"\text{edge}_{\text{after}}": BAD})]
        whys = [why(r"decay with the horizon: a fast signal has $\phi$ near zero, a slow one near one"),
                why(r"a signal that changes a lot from day to day forces trading: for normally distributed signals, the expected change "
                    r"in a position grows with the square root of one minus the signal's autocorrelation"),
                why(r"the desk keeps what the costs leave: fast alphas need cheap execution (Part 31)"),
                why(r"decay through time: across 97 published US anomalies, returns fell 26\% out of sample and 58\% "
                    r"after publication (McLean and Pontiff 2016, \textit{Journal of Finance})")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "A small model of both. <bookmark mark='a'/> Over the horizon, the IC shrinks by a factor phi each day: near "
            "zero for a fast alpha, near one for a slow one. <bookmark mark='b'/> A signal that changes a lot from day to "
            "day forces the book to trade. <bookmark mark='c'/> The desk keeps the edge minus the costs, so fast alphas "
            "live or die by their execution. <bookmark mark='d'/> And over the years, crowding: David McLean and Jeffrey "
            "Pontiff followed ninety-seven published anomalies in American stocks. Their returns were twenty-six percent "
            "lower out of sample and fifty-eight percent lower after publication, as investors learned of them."
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

    def factory(self):
        card = firm_card(r"WorldQuant", r"the `alpha factory': founded by Igor Tulchinsky, it marked its fifteenth "
                         r"anniversary in 2022. Many researchers each write many small formulaic signals, and a central "
                         r"process tests and combines them; Tulchinsky's \textit{Finding Alphas} (2015) describes the "
                         r"approach",
                         numbers=((r"\text{BRAIN}", r"a web platform where outside `research consultants' write and "
                                                    r"simulate alphas, opened to new consultants in August 2022"),
                                  (r"80{,}000+", r"users and more than 3{,}000 consultants by late 2023, as the firm "
                                                 r"reported")),
                         source=r"WorldQuant press releases, 2022--23", kind=r"Public record", width=10.6,
                         font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "The best-known alpha factory works exactly this way. <bookmark mark='a'/> WorldQuant, founded by Igor "
            "Tulchinsky, built its business on many researchers each writing many small formulaic signals, tested and "
            "combined centrally; his book Finding Alphas describes the method. <bookmark mark='b'/> In 2022 the firm "
            "opened BRAIN, a web platform where outside researchers write and simulate alphas and can be paid as "
            "consultants; by late 2023 it reported more than eighty thousand users. Decay is the reason for the scale: "
            "a factory must keep producing because its products wear out."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def crowding(self):
        cards = VGroup(
            desk_question(r"a shared grammar finds shared signals", r"many miners on the same data with the same operators "
                          r"find the same cousins: Chapter 7's correlation, across firms", width=12.4, font_size=19),
            desk_question(r"crowding shows in the price", r"as money arrives, a signal's return falls and its correlation "
                          r"with other crowded trades rises; when the money leaves, they fall together", width=12.4,
                          font_size=19),
            desk_question(r"the defence is breadth and novelty", r"new data, new horizons, and a library whose members "
                          r"are as uncorrelated as possible: AlphaAgent's originality penalty, in Chapter 6", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Crowding, in three lines. <bookmark mark='a'/> Miners using the same data and the same operators find the "
            "same cousins: Chapter seven's correlation, across firms. <bookmark mark='b'/> As money arrives, a signal's "
            "return falls and its correlation with other crowded trades rises; when the money leaves, they fall "
            "together. <bookmark mark='c'/> The defence is breadth and novelty: new data, new horizons, and a library "
            "whose members are as different from one another as possible. Chapter ten shows what happens without it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an alpha's IC halves every two years as others find it. Starting from 0.03, after how many years "
                       r"is it below 0.01?")
        with self.voiceover(
            "Pause and predict. An alpha's IC halves every two years as others find it. Starting from point zero three, "
            "after how many years is it below point zero one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
