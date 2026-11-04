from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import (BAD, HURDLE, IS_C, MKT, OOS_C, PART, RULE, era_strip, fit_right,
                                         illustration, load)


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.best(load("rules"))
        self.desk()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Backtesting Without Fooling Yourself")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-six. Backtesting without fooling yourself: how a strategy's history is simulated, and the "
            "dozen ways that simulation lies."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def best(self, r):
        ci, co = r["curves"]["in"], r["curves"]["out"]
        yi, yo = _years(ci["ym"]), _years(co["ym"])
        bi, mi = np.log10(np.asarray(ci["best"])), np.log10(np.asarray(ci["mkt"]))
        bo = bi[-1] + np.log10(np.asarray(co["best"]))
        mo = mi[-1] + np.log10(np.asarray(co["mkt"]))
        top = float(np.ceil(max(bi.max(), bo.max()) + 0.3))
        g = axes([1926, 2021], [-0.5, top], x_length=8.6, y_length=4.6, xlabel=r"year",
                 ylabel=r"growth of \$1, $\log_{10}$ (excess of T-bills)", xticks=[1930, 1950, 1970, 1990, 2010],
                 yticks=list(range(0, int(top) + 1, 2)), font_size=14).to_edge(LEFT, buff=0.45).shift(DOWN * 0.3)
        ax = g.ax
        cut = DashedLine(ax.c2p(1987, -0.5), ax.c2p(1987, top), color=GREY_C, stroke_width=1.5)
        cut_l = label(r"chosen on data to 1986", font_size=14, color=GREY_B).next_to(ax.c2p(1987, top), DOWN,
                                                                                   buff=0.1).shift(LEFT * 1.1)
        li, lm = curve(ax, yi, bi, IS_C, stroke_width=3), curve(ax, yi, mi, MKT, stroke_width=2)
        lo, lm2 = curve(ax, yo, bo, OOS_C, stroke_width=3), curve(ax, yo, mo, MKT, stroke_width=2)
        side = VGroup(
            label(r"the best of 10{,}000 rules", font_size=22, color=RULE),
            label(rf"``{r['best_label'].replace('%', chr(92) + '%')}''", font_size=19, color=GREY_A),
            MathTex(rf"\text{{Sharpe, 1926--86}}:\ {r['best_in']:.2f}", font_size=26, color=IS_C),
            MathTex(rf"\text{{Sharpe, 1987--2020}}:\ {r['best_out']:.2f}", font_size=26, color=OOS_C),
            MathTex(rf"\text{{the market}}:\ {r['eras']['in']['sr_bh']:.2f}\ \text{{and}}\ {r['eras']['out']['sr_bh']:.2f}",
                    font_size=22, color=MKT),
            wrapped_label(r"long when the market closes above its five-day average, short when below. Ten thousand "
                          r"rules of four classic kinds were tried on the daily US market to 1986; this one won", 3.6,
                          15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Ten thousand trading rules, of the four classic kinds that technical analysts use, each tried on the "
            "daily American stock market from 1926 to 1986. <bookmark mark='a'/> The best of them is almost "
            "embarrassingly simple: be long when the market closes above its own five-day average, short when it "
            "closes below. Over sixty years its Sharpe ratio was one point six seven, four times the market's. A "
            "dollar became something absurd. <bookmark mark='b'/> Then the rule met the years after 1986, which it "
            "had never seen. <bookmark mark='c'/> Its Sharpe ratio for the next thirty-four years was two hundredths. "
            "Nothing. It ranked three thousand two hundred and eighty-first of the ten thousand. Nobody had cheated. "
            "The data were clean, the code was correct, and the backtest was still a lie. This part is about why."
        ) as vo:
            self.play(FadeIn(g), Create(cut), FadeIn(cut_l))
            vo.wait_until("a")
            self.play(Create(lm), Create(li), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[5]))
            vo.wait_until("c")
            self.play(Create(lm2), Create(lo), FadeIn(side[3]), FadeIn(side[4]), run_time=3)
        self.add(illustration(r"Ken French's daily market and T-bill returns; the House's \texttt{backtest.RuleEngine}"))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        q = desk_question(r"Your backtest has a Sharpe ratio of 3. List what could be wrong.", width=12.0, font_size=26)
        items = [(r"it used tomorrow's data", r"look-ahead, point in time"),
                 (r"the losers are missing from the data", r"survivorship"),
                 (r"it was the best of many", r"selection, the trial counter"),
                 (r"it traded at prices no one could get", r"fills, latency, costs, borrow"),
                 (r"it mishandled a split or a dividend", r"corporate actions"),
                 (r"three years cannot tell", r"the Sharpe ratio's error"),
                 (r"its validation leaked", r"purged cross-validation"),
                 (r"the market changed", r"monitoring, live")]
        rows = VGroup(*[VGroup(label(a, font_size=20), label(b, font_size=18, color=HURDLE)).arrange(RIGHT, buff=0.4)
                        for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 6.6)
        q.to_edge(UP, buff=0.4)
        rows.next_to(q, DOWN, buff=0.35)
        if rows.width > 12.6:
            rows.scale_to_fit_width(12.6)
        with self.voiceover(
            "Every quantitative firm asks some version of this question at interview. Your backtest has a Sharpe ratio "
            "of three: list what could be wrong. <bookmark mark='a'/> It used tomorrow's data. The losers are missing "
            "from the data. It was the best of many tries. It traded at prices nobody could get. <bookmark mark='b'/> It "
            "mishandled a split or a dividend. Three years of data cannot tell a Sharpe of three from one. Its "
            "validation leaked. Or the market changed. <bookmark mark='c'/> Each of these is a chapter, and for each "
            "the House will plant the error on purpose, measure what it does, and build the check that catches it."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:4]], lag_ratio=0.5, run_time=4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[4:]], lag_ratio=0.5, run_time=4))
            vo.wait_until("c")
            self.play(*[Indicate(r_[1], color=HURDLE, scale_factor=1.04) for r_ in rows])
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, C = QC.IDEA, QC.CRISIS
        entries = [(1933, r"Cowles: can forecasters forecast?", I), (1961, r"Alexander's filters", I),
                   (1966, r"Fama--Blume", I), (1992, r"Brock--Lakonishok--LeBaron", I),
                   (1992.6, r"survivorship (Brown et al.)", C), (1997, r"Shumway: delisting", C),
                   (1999, r"Sullivan--Timmermann--White", I), (2000, r"White's reality check", I),
                   (2002, r"Lo: the Sharpe ratio's error", I), (2005, r"Hansen's SPA; Romano--Wolf", I),
                   (2014, r"the deflated Sharpe ratio", I), (2017, r"PBO", I), (2018, r"purged CV", I),
                   (2019, r"a backtesting protocol", I)]
        strip = era_strip(entries, y0=1925, y1=2026, font_size=13).move_to(DOWN * 0.3)
        head = label(r"How backtests learned to doubt themselves", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 10), (10, 14)]
        with self.voiceover(
            "The doubt is old. In 1933 Alfred Cowles asked whether stock market forecasters could forecast, and found "
            "that they could not. Sidney Alexander's filter rules in 1961, and Eugene Fama and Marshall Blume's test of "
            "them in 1966, made trading rules a subject of statistics; in 1992 William Brock, Josef Lakonishok and "
            "Blake LeBaron found that simple rules had worked on ninety years of the Dow. <bookmark mark='a'/> Then "
            "the corrections: survivorship, found in fund databases in 1992; missing delisting returns in 1997; and in "
            "1999 Ryan Sullivan, Allan Timmermann and Halbert White asked whether Brock's rules were the best of a "
            "much larger universe, using White's new reality check. Andrew Lo gave the Sharpe ratio a standard error "
            "in 2002. <bookmark mark='b'/> The modern toolkit came after 2010, much of it from David Bailey and Marcos "
            "Lopez de Prado: the deflated Sharpe ratio, the probability of backtest overfitting, purged "
            "cross-validation, and in 2019 a written protocol for backtesting from Robert Arnott, Campbell Harvey and "
            "Harry Markowitz."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Look-ahead, survivorship and selection, each planted and measured",
            r"An event-driven backtester: fills, latency, costs, borrow, splits and dividends",
            r"The Sharpe ratio's standard error; the minimum backtest length",
            r"The trial counter; the deflated Sharpe ratio; the probability of backtest overfitting",
            r"Purged cross-validation; reality checks; technical rules re-run",
            r"Monitoring live strategies with e-values; planted alpha; how strategies get capital",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: three biases, each planted on purpose and measured; an event-driven backtester that fills "
            "orders the way a broker would; the standard error of a Sharpe ratio, and how long a backtest must be; "
            "the trial counter, the deflated Sharpe ratio and the probability of overfitting; cross-validation that "
            "does not leak, and reality checks for data snooping, used on ten thousand technical rules; and finally "
            "what happens after the backtest: monitoring a live strategy, testing the tests on planted alpha, and how "
            "a firm decides to give a strategy money."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research", "data"))
        with self.voiceover(
            "In the House, this part builds the backtester itself, which the research desk and the data team share, "
            "and the statistics that keep it honest. From now on no strategy in the series is believed because of its "
            "backtest alone. It is believed, a little, because of what its backtest survived."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05),
                      Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
