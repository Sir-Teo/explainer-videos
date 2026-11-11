from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT, pit
from videos.quant.quant26.common import BAD, BUG, GOOD, HONEST, HURDLE, NOISE, OOS_C, PART, RULE, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("lookahead"), load("rules"), load("dsr"), load("pbo"),
                   load("cv"), load("rc"), load("monitor"), pit.trials_upto(PART))
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

    def sheet(self,a,r,d,p,c,rc,m,trials):
        rows=[(r"one-day look-ahead: original honest and planted Sharpe",rf"{a['ma200']['sr_honest']:.2f}\ \to\ {a['ma200']['sr_bug']:.2f}",BUG),
              (r"original SEC empirical item",r"\text{blocked: source hash mismatch}",BAD),
              (r"original Yahoo execution empirical item",r"\text{blocked: source hash mismatch}",BAD),
              (r"selected rule: 1926--86 and 1987--2020 Sharpe",rf"{r['best_in']:.2f},\ {r['best_out']:.2f}",HURDLE),
              (r"later-era diagnostic: DSR score, PBO, bootstrap RC fraction",rf"{d['out']['eff']['dsr']:.2f},\ {p['out']['pbo']:.2f},\ {rc['out']['rc_p']:.3f}",OOS_C),
              (r"original shuffled and purged scores; residual leakage",rf"{100*c['res']['shuffled']['r2']:+.1f}\%\ \text{{vs}}\ {100*c['res']['purged']['r2']:+.1f}\%",BUG),
              (r"retrospective clipped paths that crossed 20",rf"{m['full']['flagged']}\ \text{{of}}\ {m['n']}",BAD),
              (r"existing cumulative registrations through Part 26",comma(trials),QC.HOUSE),
              (r"sealed experiment in this review",r"\text{not opened or scored}",QC.HOUSE)]
        tab=VGroup()
        for j,(t,v,col) in enumerate(rows):
            y=2.4-.57*j;tab.add(VGroup(label(t,font_size=17,color=col).move_to([-2.35,y,0]),MathTex(v,font_size=23).move_to([4.2,y,0])))
        title=label(r"The backtester's diagnostic sheet",font_size=28).to_edge(UP,buff=.35)
        foot=wrapped_label(r"Original numerical methods and outputs are unchanged. Inference proxies, residual leakage, revised data and implementation assumptions limit interpretation; no sealed result or new market trial is used.",12,17,GREY_A).to_edge(DOWN,buff=.35)
        with self.voiceover("The diagnostic sheet preserves the original numbers with their scope. <bookmark mark='a'/> A same-bar signal illustrates look-ahead. The original SEC and Yahoo calculations remain blocked by source hash mismatches. Their unavailable numerical outputs are withheld; fixed illustrations cover the conditioning and execution mechanisms. The selected rule is compared across the two research eras only. DSR, PBO and bootstrap fractions are qualified inference diagnostics. Every validation score retains some leakage, and the clipped monitoring paths do not certify raw-return error rates. The ledger reports existing registrations; this review adds none. The sealed experiment remains unopened and unscored.") as vo:
            self.play(FadeIn(title));vo.wait_until('a');self.play(LaggedStart(*[FadeIn(row,shift=RIGHT*.2) for row in tab],lag_ratio=.35),FadeIn(foot))
        self.clear_scene()

    def protocol(self):
        items = [(r"motivation", r"an economic reason for the edge, written before the data are touched"),
                 (r"multiple testing", r"every trial counted; the hurdle and the deflated Sharpe ratio reported"),
                 (r"data", r"point in time, survivorship-free, delisting returns, vintages for revised series"),
                 (r"execution", r"the event-driven engine: latency, costs, borrow, corporate actions"),
                 (r"validation", r"training-only preprocessing; mature labels; justified time/group splits; a genuinely fresh holdout"),
                 (r"model dynamics", r"why the edge should persist, and what would end it"),
                 (r"complexity", r"the simplest version first; each addition must pay for itself out of sample"),
                 (r"culture", r"a failed backtest is a result, recorded, not a reason to try again quietly")]
        rows = VGroup(*[VGroup(label(a, font_size=22, color=QC.HOUSE), wrapped_label(b, 9.1, 21, GREY_A)).arrange(
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
            "The protocol is a set of checks, not a certificate produced by a software class. <bookmark mark='a'/> Write the economic claim, document search choices and available-time data, retain exits and inspect plausible execution and costs. <bookmark mark='b'/> Match validation to the target: fit preprocessing on available training data, wait for labels to mature, remove relevant overlap, and preserve a fresh evaluation sample. A chronological split alone does not prove those conditions. Complexity and robustness checks also count as research choices. <bookmark mark='c'/> A failed test is a result to record. No fitted diagnostic, timestamp or selected backtest replaces a defensible information clock and evaluation design."
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
                             r"Sharpe score and PBO reported with assumptions; capital ramps require implementation controls and a monitor whose actual process null is justified.", 11.8, 28, QC.HOUSE).move_to(ORIGIN)
        with self.voiceover(
            "The tools this part adds to the House. <bookmark mark='a'/> The engine and the vectorised line it "
            "replaces; the Sharpe ratio's error; selection and its hurdle; overfitting and validation; data snooping, "
            "bootstrapped; and the rules and the planted market. <bookmark mark='b'/> And the twenty-sixth rule. No "
            "strategy is believed because of its backtest. A backtest counts only if it ran on point-in-time, "
            "survivorship-free data, through the event-driven engine with its costs and corporate actions, validated "
            "without shuffling, with its trials counted and its deflated Sharpe ratio and probability of overfitting "
            "reported with their assumptions. Capital ramps need implementation controls and a monitor with a justified process null; a clipped diagnostic alone does not certify the raw-return claim."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeOut(Group(*self.mobjects)))
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the Sharpe 3 backtest", r"audit the information clock, assumed fills and costs; then inspect "
                          r"the search record and estimation uncertainty", width=12.0, font_size=19),
            desk_question(r"the beautiful long history", r"an index's stale prices, today's tickers, revised data: is "
                          r"every input as of its date, and could the thing have been traded?", width=12.0, font_size=19),
            desk_question(r"the model that cross-validates at 55\%", r"fit training-only transformations, require mature labels and use an available-time replay before "
                          r"anyone looks at the number", width=12.0, font_size=19),
            desk_question(r"the favourite strategy, slipping", r"precommit an economic claim and justify the actual bounded-increment null; do not change "
                          r"the error guarantee after seeing the path", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Apply the protocol to four cases. <bookmark mark='a'/> An impressive selected backtest prompts an audit of information availability, assumed fills, costs, research choices and uncertainty. No failure frequency is inferred from these examples. <bookmark mark='b'/> A long historical record needs point-in-time inputs, a documented universe and executable trading assumptions. <bookmark mark='c'/> A prediction model needs mature labels, training-only preprocessing and a split that matches its forecasting target; purging alone does not remove every leak. <bookmark mark='d'/> A slipping strategy needs a precommitted economic claim and a monitor whose actual conditional null is justified. Lowering a threshold cannot retain the original error bound. These are checks on evidence, not automatic certificates of truth or future performance."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
