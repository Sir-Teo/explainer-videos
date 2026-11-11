from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, SKILL_C, fit_right,
                                         load)


class Adaptive(VoiceoverScene):
    def construct(self):
        a = load("adaptive")
        self.card(a)
        self.lo()
        self.chart(a)
        self.decades(a)
        self.vr_chart(a)
        self.why()
        self.principles()
        self.nobel()
        self.decay()
        self.young()
        self.question()

    def card(self,a):
        d=a['by_decade'];c=chapter_card(4,r"Adaptive markets",r"What changes in a sample, and what does it identify?",part=PART)
        with self.voiceover(
            f"Chapter four. Daily market autocorrelation is {d['1970']['ac1']:.2f} in the nineteen seventies and "
            f"{d['2010']['ac1']:.2f} in the twenty tens, using the stated French return series and estimator. These "
            "are descriptive sample correlations. They are not fractions of correctly predicted directions, and the "
            "difference alone identifies neither trader learning nor an executable profit after costs."
        ):
            self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def lo(self):
        rows = [cmath(r"\text{efficient markets}", r":", r"\text{prices reflect a specified information set, relative to a pricing model}", font_size=36,
                      colors={r"\text{efficient markets}": MKT_C}),
                cmath(r"\text{adaptive markets}", r":", r"\text{efficiency is an outcome, and it moves}", font_size=36,
                      colors={r"\text{adaptive markets}": SKILL_C}),
                cmath(r"\text{prediction}", r":", r"\text{opportunities appear, are found, and are competed away}", font_size=34)]
        whys = [why(r"efficiency hypotheses specify information and expected-return models; risk-neutral martingales alone do not set physical expected returns"),
                why(r"Lo (2004): traders are adaptive species in an ecology; how efficient a market is depends on how "
                    r"many traders compete, with what tools"),
                why(r"so efficiency should vary over time and across markets, and returns to a strategy should decay as "
                    r"it spreads")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Andrew Lo's view. <bookmark mark='a'/> The efficient-markets hypothesis says prices reflect a specified set of "
            "information, relative to a model of expected returns. <bookmark mark='b'/> Lo's adaptive markets say efficiency is an outcome of competition among "
            "traders who learn, and it moves. <bookmark mark='c'/> So opportunities should appear, be found and be "
            "competed away, and how efficient a market is should change with who is trading it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def chart(self, a):
        t = np.asarray(a["t"], float)
        ac = np.asarray(a["ac"], float)
        ok = np.isfinite(ac)
        g = axes([1925, 2021], [-0.27, 0.4], x_length=10.4, y_length=4.2, xlabel=r"US market, daily, five-year windows",
                 ylabel=r"first-order autocorrelation", xticks=[1930, 1950, 1970, 1990, 2010], yticks=[-0.2, -0.1, 0, 0.1, 0.2, 0.3],
                 font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1925, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        ln = curve(ax, t[ok], ac[ok], MKT_C, stroke_width=2.5)
        with self.voiceover(
            "Ninety years of Kenneth French's daily market returns. <bookmark mark='a'/> In each trailing twelve-hundred-sixty-observation "
            "window, sampled every twenty-one trading observations, the correlation of one day's return with the next. <bookmark mark='b'/> It is positive for most of "
            "the century, peaking in the nineteen seventies, a period in which nonsynchronous constituent trading is one possible contributor to measured "
            "autocorrelation. <bookmark mark='c'/> Then it falls, through the arrival of index futures, electronic trading "
            "and, after two thousand, high-frequency market making, toward zero and below in these samples. The chart alone does not identify the contribution of any one change."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zero))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.play(Indicate(ln, color=HURDLE))
        self.wait(0.4)
        self.clear_scene()

    def decades(self, a):
        d = a["by_decade"]
        tab = VGroup(VGroup(label(r"decade", font_size=19, color=QC.IDEA), label(r"autocorrelation, daily", font_size=19, color=QC.IDEA),
                            label(r"variance ratio, 5 days", font_size=19, color=QC.IDEA)))
        for k in sorted(d):
            tab.add(VGroup(label(rf"{k}s", font_size=19), label(rf"{d[k]['ac1']:+.2f}", font_size=19, color=MKT_C),
                           label(rf"{d[k]['vr5']:.2f}", font_size=19, color=SKILL_C)))
        xs = [-3.6, 0.3, 3.8]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 3.0 - 0.55 * j, 0])
        v70, v10 = d["1970"]["vr5"], d["2010"]["vr5"]
        with self.voiceover(
            "By decade, with a second measure. <bookmark mark='a'/> Lo and MacKinlay's variance ratio: the variance of "
            "five-day returns over five times the daily variance, one for a random walk. <bookmark mark='b'/> In the "
            f"nineteen seventies, {v70:.2f}: weekly moves larger than daily ones would imply, the signature of trends. "
            f"In the twenty tens, {v10:.2f}: slight mean reversion. The same market, a different ecology."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:6]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[6:]], lag_ratio=0.2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def vr_chart(self, a):
        qs = np.asarray(a["qs"], float)
        v70 = np.asarray(a["vr"]["1970"], float)
        v10 = np.asarray(a["vr"]["2010"], float)
        g = axes([0, 21], [0.6, 1.8], x_length=7.4, y_length=4.2, xlabel=r"horizon $q$, days", ylabel=r"variance ratio",
                 xticks=[1, 5, 10, 15, 20], yticks=[0.75, 1.0, 1.25, 1.5, 1.75], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(21, 1), color=GREY_C, stroke_width=1.5)
        l1 = curve(ax, qs, v70, COST_C, stroke_width=3)
        l2 = curve(ax, qs, v10, SKILL_C, stroke_width=3)
        leg = legend([(COST_C, r"the 1970s"), (SKILL_C, r"the 2010s"), (GREY_C, r"random walk")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        e70, e10 = v70[-1], v10[-1]
        with self.voiceover(
            "The variance ratio across horizons, two decades compared. <bookmark mark='a'/> In the nineteen seventies "
            f"it rises with the horizon, to {e70:.2f} at twenty days: trends. <bookmark mark='b'/> In the twenty tens it "
            f"falls, to {e10:.2f}: reversal. A random walk would be the flat line between them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(one), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards=VGroup(
            desk_question('measurement','nonsynchronous constituent trading and bid-ask effects can affect index-return autocorrelation',width=12.4,font_size=19),
            desk_question('economic mechanisms','competition, information, market structure and time-varying risk can change return dynamics',width=12.4,font_size=19),
            desk_question('identification','a difference between sample correlations does not isolate its cause or establish executable alpha',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("How might the pattern arise? <bookmark mark='a'/> Nonsynchronous constituent trading and bid-ask effects can alter measured autocorrelation. <bookmark mark='b'/> Competition, information, market structure and time-varying risks may also change return dynamics. <bookmark mark='c'/> Comparing historical correlations does not isolate these mechanisms or establish executable alpha. A changing pattern also warns against interpreting a full-history average as a stable forecast for the next regime.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def principles(self):
        cards = VGroup(
            desk_question(r"Lo's adaptive markets, in practice", r"risk premia change with the population of "
                          r"investors; strategies have life cycles; innovation is the key to survival", width=12.4,
                          font_size=19),
            desk_question(r"what it predicts", r"crowding, as Part 33's quant quake showed; booms and busts in strategy "
                          r"returns; a market that is efficient on average and inefficient in places", width=12.4,
                          font_size=19),
            desk_question(r"what it does not", r"which strategy will work next: adaptation is a description, not a "
                          r"forecast", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the adaptive view implies. <bookmark mark='a'/> Risk premia change with the population of investors, "
            "strategies have life cycles, and innovation is how firms survive. <bookmark mark='b'/> It predicts "
            "crowding, as Part thirty-three's quant quake showed, booms and busts in strategy returns, and a market "
            "efficient on average and inefficient in places. <bookmark mark='c'/> What it does not do is say which "
            "strategy will work next."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nobel(self):
        cards = VGroup(
            desk_question(r"2013", r"the Nobel prize was shared by Eugene Fama, who argued that prices are hard to "
                          r"predict in the short run, and Robert Shiller, who showed they are predictable over long horizons "
                          r"from valuations, with Lars Peter Hansen, who built the tools to test both", width=12.4,
                          font_size=19),
            desk_question(r"not a contradiction", r"short-run unpredictability and long-run predictability can coexist "
                          r"if expected returns vary slowly, with risk or with sentiment", width=12.4, font_size=19),
            desk_question(r"what the series concluded", r"Part 23's equity premium and Part 6's predictive regressions: "
                          r"slow-moving expected returns, measured with large error", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The debate's most famous moment. <bookmark mark='a'/> In twenty thirteen the Nobel prize went to Eugene "
            "Fama, who argued that prices are hard to predict in the short run, to Robert Shiller, who showed them "
            "predictable over long horizons from valuations, and to Lars Peter Hansen, who built the tools to test "
            "both. <bookmark mark='b'/> It is not a contradiction: expected returns that vary slowly allow both. "
            "<bookmark mark='c'/> And that was the series' own conclusion, in Parts six and twenty-three: slow-moving "
            "expected returns, measured with large error."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def decay(self):
        cards=VGroup(
            desk_question(r"McLean and Pontiff (2016)",r"97 published predictors: reported returns lower out of sample and after publication",width=12.4,font_size=19),
            desk_question(r"interpretation",r"selection, sampling, changing risks and trading responses can all affect comparisons",width=12.4,font_size=19),
            desk_question(r"a prospective response",r"fix the research question and evaluation rule before observing the result",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "A published study of decay. <bookmark mark='a'/> McLean and Pontiff study ninety-seven published "
            "predictors and report lower returns after the original sample and after publication. "
            "<bookmark mark='b'/> Their analysis investigates statistical and publication effects; the simple timing "
            "comparison alone does not isolate every mechanism. <bookmark mark='c'/> A prospective response is to "
            "specify the question and evaluation before its result is known, while reporting uncertainty and adaptations."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def young(self):
        cards=VGroup(
            desk_question(r"a young market",r"funding access, market structure and participants can change",width=12.4,font_size=19),
            desk_question(r"an identification problem",r"a smaller basis can reflect funding, constraints, risks or competition; a chart does not choose among them",width=12.4,font_size=19),
            desk_question(r"the task",r"form a testable mechanism and an independent evaluation; historical strategy results are not inputs here",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "The same issue arises in young markets. <bookmark mark='a'/> Funding access, participants and market "
            "structure can change. <bookmark mark='b'/> A basis moving toward zero could reflect competition, changing "
            "funding costs, risk or constraints. Observing the change is not a causal decomposition. "
            "<bookmark mark='c'/> Form a testable mechanism and an independently justified evaluation. No historical "
            "crypto-carry strategy outcomes are inputs to this chapter."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def question(self):
        q=pause_card(r"a researcher selects the best of twenty tests. Is a single-test 5\% threshold still a 5\% family-wise error guarantee?")
        with self.voiceover(
            "Pause and predict. A researcher selects the best of twenty tests. Is a single-test five percent "
            "threshold still a five percent family-wise error guarantee? What information about the selection "
            "procedure should be fixed before evaluation?"
        ):self.play(FadeIn(q))
        self.wait(6.0);self.clear_scene()
