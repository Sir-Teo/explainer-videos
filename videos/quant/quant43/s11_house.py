from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import skill as SK
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         comma, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        r, e = load("record"), load("ensemble")
        self.answer()
        self.card()
        self.last_report(r)
        self.rules()
        self.policy(e)
        self.complete()
        self.advice()
        self.lab()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"\text{assume}", r":", r"\text{the House cannot beat the market}", font_size=40, colors={r"\text{assume}": MKT_C}),
                cmath(r"\text{until}", r":", r"\text{a registered, out-of-sample, cost-adjusted record says otherwise}",
                      font_size=32, colors={r"\text{until}": REC_C}),
                cmath(r"\text{and then}", r":", r"\text{size the bet to what the record can bear}", font_size=38,
                      colors={r"\text{and then}": SKILL_C})]
        whys = [why(r"Sharpe's arithmetic and the fair game: the default is the index, at its cost"),
                why(r"the Track Record's standard: registered first, opened once, costs included, every trial counted"),
                why(r"a five-year hold-out Sharpe has a standard error near 0.45: evidence enough for a sleeve, not for "
                    r"the whole fund")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The answer to the pause, the forty-third rule. <bookmark mark='a'/> Assume the House cannot beat the "
            "market. <bookmark mark='b'/> Until a record that was registered first, opened once, net of costs and with "
            "every trial counted, says otherwise. <bookmark mark='c'/> And then size the bet to what that record can "
            "bear, which, after five years, is a sleeve, not the whole fund."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def last_report(self, r):
        lines = VGroup(
            label(r"The House's last evening report", font_size=24, color=QC.HOUSE),
            label(r"risk: every number a forecast with its backtest (Rule 40)", font_size=19, color=GREY_A),
            label(r"treasury: gross leverage at most two, margins locked, cash against a doubling (Rule 41)", font_size=19,
                  color=GREY_A),
            label(r"agents: each tested against its own copies and a forced deviation (Rule 42)", font_size=19, color=GREY_A),
            label(rf"research: {r['n_rows']} rows on the Track Record; {comma(r['trials'])} trials counted", font_size=19,
                  color=REC_C),
            label(r"portfolio: the market, a capped sleeve of premia, nothing else until the record argues", font_size=19,
                  color=SKILL_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)
        nr, tr = r["n_rows"], r["trials"]
        with self.voiceover(
            "The House's last evening report, desk by desk. <bookmark mark='a'/> Risk: every number a forecast, shown "
            "with its backtest. <bookmark mark='b'/> Treasury: leverage capped, margins locked, cash held against a "
            "doubling. <bookmark mark='c'/> Agents: each tested against its own copies. <bookmark mark='d'/> Research: "
            f"{nr} rows on the Track Record, and {tr:,.0f} trials counted. <bookmark mark='e'/> And the portfolio: the "
            "market, a capped sleeve of premia, and nothing else until the record argues for it."
        ) as vo:
            self.play(FadeIn(lines[0]))
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                self.play(FadeIn(lines[k + 1], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def card(self):
        c = chapter_card(10, r"Rule 43: the market is the default", r"After forty-three parts, how should the House invest?",
                         part=PART)
        with self.voiceover("Chapter ten. The forty-third rule belongs to the whole House, and it is the one every other "
                            "rule was building toward: the burden of proof is on the strategy, not on the market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        items = [(r"Rule 1", r"point in time: nothing is known before it was known"),
                 (r"Rule 14", r"a new model is adopted only if it beats the simpler one out of sample"),
                 (r"Rule 26", r"the backtest protocol: register, count every trial, deflate"),
                 (r"Rule 40", r"a risk number is a forecast, reported with its backtest"),
                 (r"Rule 41", r"survive the margin call you have not been sent"),
                 (r"Rule 42", r"test the agent against the market it creates"),
                 (r"Rule 43", r"the market is the default; the record must argue otherwise")]
        rows = VGroup(*[VGroup(label(a_, font_size=21, color=REC_C if a_ != "Rule 43" else SKILL_C),
                               label(b_, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.4) for a_, b_ in items])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "Some of the rules that got the House here. <bookmark mark='a'/> The first: point in time. "
            "<bookmark mark='b'/> A new model must beat the simpler one out of sample. <bookmark mark='c'/> The "
            "backtest protocol: register, count, deflate. <bookmark mark='d'/> A risk number is a forecast; survive the "
            "margin call you have not been sent; test the agent against the market it creates. "
            "<bookmark mark='e'/> And the last: the market is the default."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[3:6]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[6], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def policy(self, e):
        h = e["row"]["holdout"]
        rows = [cmath(r"\text{core}", r":", r"\text{the market, at index cost}", font_size=40, colors={r"\text{core}": MKT_C}),
                cmath(r"\text{sleeve}", r":", r"\text{the registered premia ensemble, risk-capped}", font_size=38,
                      colors={r"\text{sleeve}": REC_C}),
                cmath(r"\text{research}", r":", r"\text{new rows, registered, opened only when their window closes}",
                      font_size=34, colors={r"\text{research}": SKILL_C}),
                cmath(r"\text{limits}", r":", r"\text{Rules 40 to 42, outside every model}", font_size=38,
                      colors={r"\text{limits}": COST_C})]
        whys = [why(r"what Sharpe's arithmetic guarantees, cheapest"),
                why(rf"the one row the House built from the classic premia: hold-out Sharpe {h['sharpe']:.2f}, "
                    rf"{h['sharpe_net']:.2f} net"),
                why(r"the next hold-out begins where this one ended; the counter keeps running"),
                why(r"risk forecasts with backtests, liquidity stress, and agents tested against their own copies")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "So what the House does with its money, as a teaching example and not advice. <bookmark mark='a'/> A core "
            "in the market itself, at index cost. <bookmark mark='b'/> A sleeve in the one strategy the House built "
            "from published premia and opened once, sized so that its risk is capped. <bookmark mark='c'/> Research "
            "continues: new rows registered now, opened only when their own windows close. <bookmark mark='d'/> And "
            "the limits of Rules forty to forty-two, outside every model."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def complete(self):
        chart = house_chart(PART, lit=tuple(DESKS.keys()))
        with self.voiceover(
            "The House, complete. Data and technology across the top; the trading desks, from volatility and rates to "
            "credit, macro and digital assets; research, portfolio and risk, execution and market making; and "
            "treasury and compliance underneath. Forty-three parts ago it was an empty building and a sealed envelope."
        ):
            self.play(FadeIn(chart))
            self.wait(2)
        self.clear_scene()

    def advice(self):
        cards = VGroup(
            desk_question(r"to a new analyst", r"write down the test before you run it; count what you try; keep the "
                          r"last years sealed; report the costs", width=12.4, font_size=19),
            desk_question(r"to a portfolio manager", r"own the market cheaply; size a strategy by its out-of-sample "
                          r"record, not its backtest; know who is on the other side", width=12.4, font_size=19),
            desk_question(r"to a researcher", r"prove what you claim, then check it on data the proof never saw; and "
                          r"publish the null results", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the House would tell the people who join it. <bookmark mark='a'/> To a new analyst: write down the "
            "test before you run it, count what you try, keep the last years sealed, and report the costs. "
            "<bookmark mark='b'/> To a portfolio manager: own the market cheaply, size a strategy by its out-of-sample "
            "record, and know who is on the other side. <bookmark mark='c'/> And to a researcher: prove what you "
            "claim, check it on data the proof never saw, and publish the null results."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Counting skill without finding it", SK.storey_pi0, "p = np.asarray(p, float)", 2,
                         extra=((SK.bsw, "pi0 = storey_pi0(p, lam)", 6),), width=10.6)
        with self.voiceover(
            "The House's code for Chapter two. Storey's estimate is two lines: the share of p-values above lambda, "
            "scaled up. Barras, Scaillet and Wermers' shares subtract, from each significant tail, the lucky nulls that "
            "estimate implies."
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research", "portfolio", "compliance")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{beat\_prob}, \texttt{fund\_population}", r"Sharpe's arithmetic and luck"),
            (r"\texttt{storey\_pi0}, \texttt{bsw}, \texttt{berk\_green}", r"skill, counted and priced"),
            (r"\texttt{rolling\_autocorr}, \texttt{variance\_ratio}", r"adaptive efficiency"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 43: the House assumes it cannot beat the market, until a record registered first, "
                             r"opened once, net of costs and with every trial counted says otherwise; and then it sizes "
                             r"the bet to what that record can bear.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds, in the House's skill module. <bookmark mark='a'/> Sharpe's arithmetic and luck; "
            "skill counted and priced; and adaptive efficiency. <bookmark mark='b'/> And the forty-third rule, in "
            "full."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"a fund that beat the market for five years", r"ask how many funds tried, what luck alone "
                          r"would give, and whether its record was registered before it was run (Chapter 2)", width=12.0,
                          font_size=19),
            desk_question(r"a manager with real skill", r"ask who receives it: the manager, through size and fees, or "
                          r"you (Chapter 3)", width=12.0, font_size=19),
            desk_question(r"a strategy that worked for decades", r"ask whether the market that paid it still exists "
                          r"(Chapter 4), and what its hold-out said (Chapter 5)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three last tests to carry away. <bookmark mark='a'/> When a fund beat the market for five years, ask how "
            "many tried, what luck alone would give, and whether its record was registered before it was run. "
            "<bookmark mark='b'/> When a manager has real skill, ask who receives it. <bookmark mark='c'/> And when a "
            "strategy worked for decades, ask whether the market that paid it still exists, and what its hold-out said."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
