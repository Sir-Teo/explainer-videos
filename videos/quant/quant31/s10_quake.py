from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, FAC_C, GOOD, HURDLE, IC_C, PART, SPEC_C, fit_right, load


class Quake(VoiceoverScene):
    def construct(self):
        q = load("quake")
        self.card()
        self.crisis(q)
        self.strategy()
        self.replay(q)
        self.mechanism()
        self.through_model()
        self.crowding()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(9, r"Crowding and August 2007", r"What happens when everyone holds the same factor-neutral book?",
                         part=PART)
        with self.voiceover("Chapter nine. A risk model that everyone uses steers everyone toward the same trades. In the "
                            "second week of August 2007, that bill came due."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def crisis(self, q):
        card = crisis_card(r"6--10 August 2007", r"The quant quake",
                           r"many quantitative long--short equity funds lost heavily in three days while the stock market "
                           r"itself barely moved; on 13 August Goldman Sachs said it would invest \$3 billion, with outside "
                           r"investors, in its Global Equity Opportunities fund, citing an increase in overlapping trades "
                           r"and in correlations",
                           stats=((r"\$3\ \text{bn}", r"the GEO recapitalisation, Goldman's release of 13 August"),
                                  (r"\approx 30\%", r"the fund's loss before it, as reported")), width=11.0,
                           font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The crisis file. In the week of the sixth of August 2007, many quantitative long-short equity funds lost "
            "heavily in three days, while the stock market itself barely moved. On the thirteenth, Goldman Sachs said it "
            "would put three billion dollars, with outside investors, into its Global Equity Opportunities fund, a "
            "quantitative long-short fund that had lost, as reported, about thirty percent. Its explanation named "
            "overlapping trades, rising volatility and rising correlations."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def strategy(self):
        rows = [cmath(r"w_{i,t}", r"=", r"-\tfrac1N\big(R_{i,t-1} - R_{m,t-1}\big)", font_size=40, colors={r"w_{i,t}": IC_C}),
                cmath(r"\textstyle\sum_i w_{i,t}", r"=", r"0", font_size=36),
                cmath(r"\pi_t", r"=", r"\textstyle\sum_i w_{i,t} R_{i,t}", font_size=36)]
        whys = [why(r"Khandani and Lo's contrarian strategy (2007; 2011): buy yesterday's losers, sell yesterday's "
                    r"winners, in proportion to how far they moved from the market"),
                why(r"dollar-neutral by construction: a stand-in for the market-neutral books the funds held"),
                why(r"its daily return: it earns when yesterday's moves reverse, by providing liquidity to those who "
                    r"traded them")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Amir Khandani and Andrew Lo studied it with the simplest possible market-neutral book. "
            "<bookmark mark='a'/> Each day, buy yesterday's losers and sell yesterday's winners, in proportion to how far "
            "each moved from the market. <bookmark mark='b'/> The book is dollar-neutral. <bookmark mark='c'/> It earns "
            "when moves reverse: it is paid for providing liquidity to whoever traded yesterday."
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

    def replay(self, q):
        d = np.asarray(q["days"], int)
        cum = 100 * np.asarray(q["cum"], float)
        x = np.arange(len(d))
        lo, hi = float(np.floor(cum.min())), float(np.ceil(cum.max()))
        g = axes([0, len(d) - 1], [lo, hi], x_length=7.6, y_length=4.4, xlabel=r"July--August 2007, trading days",
                 ylabel=r"cumulative return, \%", xticks=[], yticks=[lo, 0, hi], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, x, cum, IC_C, stroke_width=3)
        i6 = int(np.searchsorted(d, 20070806))
        band = Rectangle(width=ax.c2p(i6 + 4, 0)[0] - ax.c2p(i6, 0)[0], height=4.4, fill_color=BAD, fill_opacity=0.15,
                         stroke_width=0).move_to(ax.c2p(i6 + 2, (lo + hi) / 2))
        aug = q["aug"]
        sd = q["sd_before"]
        stats = VGroup(*[label(rf"{int(k) % 100} Aug: {100 * v:+.2f}\%", font_size=17,
                               color=BAD if v < 0 else GOOD) for k, v in sorted(aug.items())])
        stats.add(label(rf"typical day, 2006--07: $\pm${100 * sd:.2f}\%", font_size=16, color=GREY_B))
        stats.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        fit_right(stats)
        foot = wrapped_label(r"the contrarian rule replayed on Kenneth French's 49 daily US industry portfolios, not the "
                             r"individual stocks Khandani and Lo used, so the moves are smaller", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.25)
        a8, a9, a10 = aug["20070808"], aug["20070809"], aug["20070810"]
        with self.voiceover(
            "The House replays the rule on the forty-nine US industry portfolios, day by day through July and August "
            "2007. <bookmark mark='a'/> In the week of the sixth: on the eighth, "
            f"{100 * a8:.2f} percent; on the ninth, {100 * a9:.2f}; against a typical daily move of {100 * sd:.2f} "
            f"percent in the year before. <bookmark mark='b'/> And on the tenth, {100 * a10:+.2f} percent, most of it "
            "back. Khandani and Lo, on individual stocks, saw the same shape, much larger: losses on the seventh, "
            "eighth and ninth, and a sharp rebound on the tenth."
        ) as vo:
            self.play(FadeIn(g), FadeIn(foot))
            self.play(Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(band), LaggedStart(*[FadeIn(s) for s in stats[:4]], lag_ratio=0.3), FadeIn(stats[5]))
            vo.wait_until("b")
            self.play(FadeIn(stats[4]))
        self.wait(0.4)
        self.clear_scene()

    def mechanism(self):
        steps_ = [(r"a large fund with a similar book must raise cash", r"losses elsewhere, perhaps in credit, as Khandani "
                                                                       r"and Lo conjectured", HURDLE),
                  (r"it sells its longs and buys back its shorts, fast", r"its trades move prices against everyone holding "
                                                                         r"the same positions", BAD),
                  (r"the others lose, hit risk limits, and unwind too", r"a spiral of forced selling inside the "
                                                                        r"crowded trade", BAD),
                  (r"the selling stops; prices snap back", r"10 August: the funds that held on recovered much of it",
                   GOOD)]
        rows = VGroup()
        for t, d, col in steps_:
            rows.add(VGroup(label(t, font_size=22, color=col), label(d, font_size=17, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.2 + LEFT * 0.4)
        head = label(r"The unwind hypothesis", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Khandani and Lo's explanation, offered as a hypothesis. <bookmark mark='a'/> A large fund with a similar "
            "book had to raise cash, perhaps because of losses elsewhere as the credit markets broke. "
            "<bookmark mark='b'/> It sold its longs and bought back its shorts quickly, moving prices against everyone "
            "who held the same positions. <bookmark mark='c'/> The others lost, hit their risk limits, and unwound too. "
            "<bookmark mark='d'/> When the selling stopped, prices snapped back."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def through_model(self):
        rows = [cmath(r"h^\top X", r"=", r"0\quad\text{(neutral to every factor in the model)}", font_size=34,
                      colors={r"h^\top X": FAC_C}),
                cmath(r"\operatorname{Var}(h^\top r)", r"=", r"\textstyle\sum_i h_i^2 s_i^2\ \ \text{(small, diversified)}",
                      font_size=32, colors={r"\textstyle\sum_i h_i^2 s_i^2": SPEC_C}),
                cmath(r"\text{but}", r":", r"\operatorname{Corr}(u_i, u_j) \neq 0\ \text{for the crowded positions}",
                      font_size=32, colors={r"\text{but}": BAD})]
        whys = [why(r"the funds' books were built to have no exposure to the risk model's factors"),
                why(r"so the model saw only specific risk, which diversifies across hundreds of names"),
                why(r"the hidden factor was the crowd itself: the common positions of funds using similar signals and "
                    r"similar models, which no vendor's model contained")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Seen through the risk model of Chapter two. <bookmark mark='a'/> The books were neutral to every factor in "
            "the model. <bookmark mark='b'/> So the model saw only specific risk, spread across hundreds of names, and "
            "forecast a small, diversified variance. <bookmark mark='c'/> But the residuals of the crowded positions "
            "were not independent: the funds held them in common. The missing factor was the crowd itself, and no "
            "vendor's model contained it."
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

    def crowding(self):
        cards = VGroup(
            desk_question(r"measuring the crowd", r"Lou and Polk's comomentum: the excess correlation of the residual "
                          r"returns of a strategy's long and short legs; when it is high, many arbitrageurs are in, and the "
                          r"strategy's later returns are worse", width=12.4, font_size=19),
            desk_question(r"other gauges", r"short interest in the short leg, the strategy's own turnover in the "
                          r"market's volume, and the correlation of a fund's returns with peers'", width=12.4, font_size=19),
            desk_question(r"what the industry kept", r"stress tests for a forced unwind of the book, liquidity-weighted "
                          r"position limits, and caution about residual bets that everyone's model calls safe", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Can crowding be measured before it bites? <bookmark mark='a'/> Dong Lou and Christopher Polk proposed one "
            "gauge for momentum, which they called comomentum: the excess correlation among the residual returns of the "
            "stocks a strategy holds. When it is high, many arbitrageurs are in, and the strategy's later returns are "
            "worse. <bookmark mark='b'/> Others watch short interest, the strategy's share of volume, and the "
            "correlation of a fund with its peers. <bookmark mark='c'/> And the industry kept the lesson as stress tests "
            "of a forced unwind and position limits weighted by liquidity."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        q = load("quake")
        cards = VGroup(
            desk_question(r"the risk model measures the risks it contains", r"a factor-neutral book is neutral to the "
                          r"model's factors, not to every common risk", width=12.4, font_size=19),
            desk_question(r"liquidity provision is short a crash", rf"the contrarian rule earns by absorbing others' "
                          rf"trades, and loses when they all trade at once; on the industries, over 1997--2007, it did not "
                          rf"earn at all: a Sharpe ratio of {q['sharpe_1997_2007']:.2f}, because industries trend rather "
                          r"than reverse", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Two lessons. <bookmark mark='a'/> The risk model measures only the risks it contains: neutral to the model "
            "is not neutral to everything. <bookmark mark='b'/> And liquidity provision is short a crash: it earns by "
            "absorbing other people's trades and loses when they all trade at once. An honest footnote: on industry "
            "portfolios, the contrarian rule did not earn at all over the previous decade, a Sharpe ratio of "
            f"{q['sharpe_1997_2007']:.2f}, because industries trend rather than reverse. The reversal premium lives in "
            "individual stocks."
        ) as vo:
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"your book's forecast volatility is 4\% a year and it is neutral to every factor. Name one way it "
                       r"could lose 10\% in a week.")
        with self.voiceover(
            "Pause and predict. Your book's forecast volatility is four percent a year, and it is neutral to every factor "
            "in your model. Name one way it could lose ten percent in a week."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
