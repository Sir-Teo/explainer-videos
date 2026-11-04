from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant26.common import BAD, BUG, GOOD, HONEST, HURDLE, NOISE, OOS_C, PART, RULE, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("lookahead"), load("survivor"), load("engine"), load("rules"), load("dsr"), load("pbo"),
                   load("cv"), load("rc"), load("monitor"), load("envelope"))
        self.protocol()
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(16, r"Rule 26: the backtest protocol", r"What must a backtest survive before the House "
                         r"believes it?", part=PART)
        with self.voiceover("Chapter sixteen. The House's twenty-sixth rule: the protocol every backtest must pass."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, a, s, e, r, d, p, c, rc, m, env):
        rows = [(r"a one-day look-ahead: Sharpe ratio, honest and planted",
                 rf"{a['ma200']['sr_honest']:.2f}\ \to\ {a['ma200']['sr_bug']:.2f}", BUG),
                (r"bankrupt filers still in today's ticker file", rf"{100 * s['bank_share']:.0f}\%", BAD),
                (r"EEM reversal: vectorised, next open, all costs",
                 rf"{e['vector']['sr']:.2f},\ {e['runs']['open_next']['sr']:.2f},\ {e['runs']['all']['sr']:.2f}", RULE),
                (r"best of 10{,}000 rules: 1926--86, 1987--2020, 2021--25",
                 rf"{r['best_in']:.2f},\ {r['best_out']:.2f},\ {env['sr_hold']:.2f}", HURDLE),
                (r"1987--2020 winner: DSR, PBO, reality check $p$",
                 rf"{d['out']['eff']['dsr']:.2f},\ {p['out']['pbo']:.2f},\ {rc['out']['rc_p']:.3f}", OOS_C),
                (r"shuffled against purged cross-validation, $R^2$",
                 rf"{100 * c['res']['shuffled']['r2']:+.1f}\%\ \text{{vs}}\ {100 * c['res']['purged']['r2']:+.1f}\%", BUG),
                (r"published predictors flagged by the monitor", rf"{m['full']['flagged']}\ \text{{of}}\ {m['n']}", BAD),
                (r"the trial counter", comma(env["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.0]
        tab = VGroup()
        for j, (t, v, col) in enumerate(rows):
            y = 2.4 - 0.6 * j
            tab.add(VGroup(label(t, font_size=18, color=col).move_to([hx[0], y, 0]), MathTex(v, font_size=24).move_to(
                [hx[1], y, 0])))
        title = label(r"The backtester's first sheet", font_size=28).to_edge(UP, buff=0.35)
        foot = wrapped_label(r"every number computed in this part from public data or simulation; none is a forecast, "
                             r"and none is advice", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> One subscript turned a Sharpe ratio of point two two into one point "
            "three one. Six percent of bankrupt companies are still in today's ticker list. A reversal worth point four "
            "three on paper was worth minus a half once it was filled and charged. The best of ten thousand rules went "
            "from one point six seven to nothing to a loss. The modern era's winner failed the deflated test, the "
            "overfitting test and the reality check. Shuffled cross-validation found a forecast that did not exist. The "
            "monitor flagged sixty-eight published predictors. And the counter reads ten thousand three hundred and "
            "forty-six."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def protocol(self):
        items = [(r"motivation", r"an economic reason for the edge, written before the data are touched"),
                 (r"multiple testing", r"every trial counted; the hurdle and the deflated Sharpe ratio reported"),
                 (r"data", r"point in time, survivorship-free, delisting returns, vintages for revised series"),
                 (r"execution", r"the event-driven engine: latency, costs, borrow, corporate actions"),
                 (r"validation", r"purged and embargoed, or walk-forward; never shuffled; a sealed hold-out"),
                 (r"model dynamics", r"why the edge should persist, and what would end it"),
                 (r"complexity", r"the simplest version first; each addition must pay for itself out of sample"),
                 (r"culture", r"a failed backtest is a result, recorded, not a reason to try again quietly")]
        rows = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 3.0)
        head = label(r"A backtesting protocol", font_size=30).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        src = note(r"after Arnott, Harvey and Markowitz (2019), whose seven headings these follow, with execution added",
                   font_size=15, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2019 Robert Arnott, Campbell Harvey and Harry Markowitz wrote down a protocol for backtesting, and the "
            "House's follows its headings, with one added. <bookmark mark='a'/> Motivation: an economic reason for the "
            "edge, written before the data are touched. Multiple testing: every trial counted. Data: point in time, "
            "free of survivorship, with vintages for anything revised. <bookmark mark='b'/> Execution, the House's "
            "addition: the event-driven engine. Validation: purged, walked forward, or sealed, but never shuffled. "
            "<bookmark mark='c'/> Model dynamics: why the edge should persist, and what would end it, the question the "
            "technical rules never asked. Complexity: the simplest version first. And culture: a failed backtest is a "
            "result, to be recorded, not a reason to try again quietly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[3:5]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[5:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Deflating, in the House", BT.expected_max_sr, "z = stats.norm.ppf", 2,
                         extra=((BT.deflated_sharpe, "sr0 = expected_max_sr", 2), (BT.psr, "den = math.sqrt", 2)),
                         width=10.4)
        card.move_to(ORIGIN)
        with self.voiceover(
            "The deflation is three short functions. The expected best of N, from the normal quantiles and Euler's "
            "constant. The benchmark it implies. And the probabilistic Sharpe ratio against that benchmark, with the "
            "skewness and kurtosis in the denominator. Six lines; the hard part is not the code but the honesty of the N "
            "that goes into it."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research", "data")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{Backtester}, \texttt{Costs}, \texttt{vectorized}", r"the engine, and the line it replaces"),
            (r"\texttt{sharpe\_se}, \texttt{lo\_eta}, \texttt{psr}", r"the Sharpe ratio's error"),
            (r"\texttt{expected\_max\_sr}, \texttt{deflated\_sharpe}, \texttt{min\_btl}", r"selection and its hurdle"),
            (r"\texttt{cscv}, \texttt{purged\_kfold}, \texttt{walk\_forward}", r"overfitting and validation"),
            (r"\texttt{reality\_check}, \texttt{spa}, \texttt{romano\_wolf}", r"data snooping, bootstrapped"),
            (r"\texttt{rule\_grid}, \texttt{RuleEngine}, \texttt{planted\_market}", r"the rules, and planted alpha"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 26: no strategy is believed because of its backtest. A backtest counts only if it ran "
                             r"on point-in-time, survivorship-free data through the event-driven engine with costs and "
                             r"corporate actions, validated without shuffling, with its trials counted and its deflated "
                             r"Sharpe ratio and PBO reported; and a strategy gets capital only by a ramp, gated by a monitor "
                             r"that tests the claim that funded it.", 12.4, 19, QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The tools this part adds to the House. <bookmark mark='a'/> The engine and the vectorised line it "
            "replaces; the Sharpe ratio's error; selection and its hurdle; overfitting and validation; data snooping, "
            "bootstrapped; and the rules and the planted market. <bookmark mark='b'/> And the twenty-sixth rule. No "
            "strategy is believed because of its backtest. A backtest counts only if it ran on point-in-time, "
            "survivorship-free data, through the event-driven engine with its costs and corporate actions, validated "
            "without shuffling, with its trials counted and its deflated Sharpe ratio and probability of overfitting "
            "reported. And a strategy gets capital only by a ramp, gated by a monitor that tests the claim that funded "
            "it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the Sharpe 3 backtest", r"first the engine, then the count: most die at the open, the rest at "
                          r"the deflation", width=12.0, font_size=19),
            desk_question(r"the beautiful long history", r"an index's stale prices, today's tickers, revised data: is "
                          r"every input as of its date, and could the thing have been traded?", width=12.0, font_size=19),
            desk_question(r"the model that cross-validates at 55\%", r"rerun with purged folds and walk-forward before "
                          r"anyone looks at the number", width=12.0, font_size=19),
            desk_question(r"the favourite strategy, slipping", r"its monitor tests the claim that funded it; no one "
                          r"lowers the bar after the fact", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> The backtest with a Sharpe ratio of three "
            "goes through the engine first, then the count: most such backtests die at the next morning's open, and "
            "the rest at the deflation. <bookmark mark='b'/> A beautiful long history is asked whether every input was "
            "as of its date, and whether the thing could have been traded at all. <bookmark mark='c'/> A model that "
            "cross-validates at fifty-five percent is rerun with purged folds before anyone celebrates. <bookmark "
            "mark='d'/> And the favourite strategy, slipping, is judged by a monitor whose bar nobody may lower. None "
            "of this is clever. All of it is the difference between research and storytelling."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
