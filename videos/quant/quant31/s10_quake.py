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
                           r"moved much less than some reported fund losses; on 13 August Goldman Sachs said it would invest \$3 billion, with outside "
                           r"investors, in its Global Equity Opportunities fund, citing an increase in overlapping trades "
                           r"and in correlations",
                           stats=((r"\$3\ \text{bn}", r"the GEO recapitalisation, Goldman's release of 13 August"),
                                  (r"\approx 30\%", r"the fund's loss before it, as reported")), width=11.0,
                           font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The crisis file. In the week of the sixth of August 2007, many quantitative long-short equity funds lost "
            "heavily in three days, while the stock market moved much less than some reported fund losses. On the thirteenth, Goldman Sachs said it "
            "would put three billion dollars, with outside investors, into its Global Equity Opportunities fund, a "
            "quantitative long-short fund that had lost, as reported, about thirty percent. Its explanation named "
            "overlapping trades, rising volatility and rising correlations."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def strategy(self):
        rows = [cmath(r"w_{i,t}", r"=", r"\frac{-(R_{i,t-1}-\bar R_{t-1})}{\sum_j|R_{j,t-1}-\bar R_{t-1}|}", font_size=40, colors={r"w_{i,t}": IC_C}),
                cmath(r"\textstyle\sum_i w_{i,t}", r"=", r"0", font_size=36),
                cmath(r"\pi_t", r"=", r"\textstyle\sum_i w_{i,t} R_{i,t}", font_size=36)]
        whys = [why(r"Khandani and Lo's contrarian strategy (2007; 2011): buy yesterday's losers, sell yesterday's "
                    r"winners, in proportion to how far they moved from the market"),
                why(r"dollar neutral, gross exposure one when the denominator is nonzero; not necessarily beta neutral"),
                why(r"contrarian next-day P\&L; liquidity provision is an interpretation, not established by the weights alone")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A contrarian proxy related to Khandani and Lo's work. <bookmark mark='a'/> Negate yesterday's return minus the cross-sectional mean, then divide by total absolute deviation. <bookmark mark='b'/> This gives zero net dollars and unit gross exposure when defined, not beta neutrality. <bookmark mark='c'/> Next day's weighted return measures the contrarian payoff. Calling it liquidity provision requires an economic interpretation beyond the weight formula."
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
        lo, hi = float(np.floor(cum.min())) + 0.0, float(np.ceil(cum.max())) + 0.0   # + 0.0 turns -0 into 0
        g = axes([0, len(d) - 1], [lo, hi], x_length=7.6, y_length=4.4, xlabel=r"July--August 2007, trading days",
                 ylabel=r"sum of daily proxy P\&L, \%", xticks=[], yticks=sorted({lo, 0.0, hi}), font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, x, cum, IC_C, stroke_width=3)
        i6 = int(np.searchsorted(d, 20070806))
        band = Rectangle(width=ax.c2p(i6 + 4, 0)[0] - ax.c2p(i6, 0)[0], height=4.4, fill_color=BAD, fill_opacity=0.15,
                         stroke_width=0).move_to(ax.c2p(i6 + 2, (lo + hi) / 2))
        aug = q["aug"]
        sd = q["sd_before"]
        stats = VGroup(*[label(rf"{int(k) % 100} Aug: {100 * v:+.2f}\%", font_size=17,
                               color=BAD if v < 0 else GOOD) for k, v in sorted(aug.items())])
        stats.add(label(rf"daily SD, Jan 2006--Jun 2007: $\pm${100 * sd:.2f}\%", font_size=16, color=GREY_B))
        stats.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        fit_right(stats)
        foot = wrapped_label(r"the contrarian rule replayed on Kenneth French's 49 daily US industry portfolios, not the "
                             r"individual stocks or actual fund holdings; missing returns filled by zero; no trading or borrowing costs", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.25)
        a8, a9, a10 = aug["20070808"], aug["20070809"], aug["20070810"]
        with self.voiceover(
            f"""The saved replay uses forty-nine French industry portfolios, prior-day weights and unit gross exposure. It is not a reconstruction of individual stocks or fund holdings. The curve adds daily proxy payoffs rather than compounding wealth. <bookmark mark='a'/> On August eighth the payoff was {100 * a8:.2f} percent and on the ninth {100 * a9:.2f} percent. Reference daily standard deviation is {100 * sd:.2f} percent over January twenty-oh-six through June twenty-oh-seven, not a confidence interval. <bookmark mark='b'/> August tenth returned {100 * a10:+.2f} percent. Missing returns are filled by zero and costs are omitted. The shape resembles the reported stock-level episode, but the magnitude is a different proxy."""
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
            self.play(FadeIn(rows[0]))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.2)) if k else self.play(Indicate(rows[0]))
        self.wait(0.4)
        self.clear_scene()

    def through_model(self):
        rows = [cmath(r"h^\top X", r"=", r"0\quad\text{(neutral to every factor in the model)}", font_size=34,
                      colors={r"h^\top X": FAC_C}),
                cmath(r"\widehat{\operatorname{Var}}(h^\top r)", r"=", r"\textstyle\sum_i h_i^2 s_i^2\quad\text{(diagonal-residual forecast)}",
                      font_size=32, colors={r"\textstyle\sum_i h_i^2 s_i^2": SPEC_C}),
                cmath(r"\text{but}", r":", r"\operatorname{Corr}(u_i, u_j) \neq 0\ \text{for the crowded positions}",
                      font_size=32, colors={r"\text{but}": BAD})]
        whys = [why(r"stylised example, separate from the industry replay: a book neutral to its chosen model factors"),
                why(r"the forecast then contains specific terms; their size still depends on gross exposure, concentration and variances"),
                why(r"residual dependence from common positions can invalidate the diagonal assumption")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A stylised model example, separate from the industry replay. <bookmark mark='a'/> Suppose a book is neutral to the factors its chosen model contains. <bookmark mark='b'/> A diagonal-residual model then forecasts the sum of squared holdings times specific variances. This need not be small: gross leverage and concentration still matter. <bookmark mark='c'/> If residuals co-move during crowded unwinds, omitted covariance can raise realised risk. This does not establish that every historical fund was factor neutral or that every vendor omitted crowding."
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
                          r"returns in momentum portfolios, studied as a crowding proxy; sample associations are not direct fund counts or guarantees", width=12.4, font_size=19),
            desk_question(r"other gauges", r"short interest in the short leg, the strategy's own turnover in the "
                          r"market's volume, and the correlation of a fund's returns with peers'", width=12.4, font_size=19),
            desk_question(r"what the industry kept", r"stress tests for a forced unwind of the book, liquidity-weighted "
                          r"position limits, and caution about residual bets that everyone's model calls safe", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Crowding is imperfectly observed. <bookmark mark='a'/> Lou and Polk study excess residual correlation in momentum portfolios, called comomentum, and its associations with later returns. This is a proxy, not a count of arbitrageurs or a guaranteed prediction. <bookmark mark='b'/> Short interest, participation in market volume and correlation with peer funds provide other incomplete gauges. <bookmark mark='c'/> Stress tests of joint unwinds and liquidity-sensitive limits address scenarios that ordinary covariance estimates can miss."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        q = load("quake")
        cards = VGroup(
            desk_question(r"the risk model measures the risks it contains", r"a factor-neutral book is neutral to the "
                          r"model's factors, not to every common risk", width=12.4, font_size=19),
            desk_question(r"proxy and mechanism differ", rf"industry proxy Sharpe, 1997--2007: {q['sharpe_1997_2007']:.2f}; "
                          r"descriptive performance does not identify liquidity provision or a universal crash exposure", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            f"""Two lessons. <bookmark mark='a'/> Neutrality is relative to a specified factor set; shared residual risks can remain. <bookmark mark='b'/> The industry proxy's saved nineteen-ninety-seven to twenty-oh-seven Sharpe is {q['sharpe_1997_2007']:.2f}. That descriptive result does not prove that all industries trend, that all stock reversal is a liquidity premium, or that every liquidity strategy has the same crash exposure. The unwind account remains an economic hypothesis."""
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
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
