from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import firm as F
from videos.quant.quant34.common import (BAD, FIRM_C, GOOD, LAW_C, PART, PLAT_C, PM_C, STOP_C, comma, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("virtu"), load("theory"), load("power"), load("platform"), load("house"), load("stops"))
        self.lab()
        self.lab2()
        self.lab3()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(11, r"Rule 34: the firm", r"What must be true of the firm before any desk trades?", part=PART)
        with self.voiceover("Chapter eleven. The House's thirty-fourth rule is not about a strategy. It is about the "
                            "firm: the limits, controls and records under which every desk in the House now trades."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, v, t, pw, p, h, s):
        S1 = t["grid"][t["S"].index(1.0)]
        pr = {r["S"]: r for r in pw["rows"]}
        on, off = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"], p["5% vol, no stops | skill sd 0.5"]
        hml = dict(zip(s["names"], s["rows"]))["HML"]
        rows = [(r"1 losing day in 1{,}238: daily and annual Sharpe, normal", rf"{v['normal']:.2f},\ {v['annual']:.0f}",
                 GOOD),
                (r"Sharpe 1: years to a stop 0.5 and 1 volatility deep", rf"{S1[0]:.2f},\ {S1[2]:.2f}", STOP_C),
                (r"stopped within 3 years at 1.5 vols: Sharpe 0 and 1", rf"{100 * pr[0.0]['d1.5_3y']:.0f}\%,\ "
                 rf"{100 * pr[1.0]['d1.5_3y']:.0f}\%", STOP_C),
                (r"platform, skill varies: investors' Sharpe with and without stops", rf"{on['investor_sharpe']:.2f},\ "
                 rf"{off['investor_sharpe']:.2f}", PLAT_C),
                (r"share of the platform's P\&L paid to pods", rf"{100 * on['payout_share']:.0f}\%", PLAT_C),
                (r"the House's record: sealed on research, slope", rf"{h['slope']:.2f}", FIRM_C),
                (r"value with a 15\%/12-month stop: Sharpe, no stop and stop", rf"{hml['none']['sharpe']:.2f},\ "
                 rf"{hml['15%/12m']['sharpe']:.2f}", PM_C),
                (r"the trial counter", comma(h["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.6]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.5 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The firm's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Virtu's disclosed statistic, the stop-time formulas, simulation, "
                             r"the House's own Track Record and Kenneth French's factors; firms' facts as reported; none "
                             r"is advice", 12.0, 15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A disclosed loss rate implies a daily Sharpe ratio above three. A "
            "Sharpe-one manager hits a stop half a volatility deep in months, and one a volatility deep in about two "
            "years. A stop one and a half volatilities deep fires on most managers without skill within three years, and "
            "on a quarter of good ones. On a platform where skill varies, stops raise what investors keep, while the "
            "payout to pods exceeds its headline share. The House's own registered books kept about three quarters of "
            "their research Sharpe ratio. And a stop helps value, whose losses persist."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"How long a seat lasts", F.stop_time, "if abs(mu) < 1e-12:", 4,
                         extra=((F.peak_at_stop, "if abs(mu) < 1e-12:", 4),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "The research chapter's formulas, in eight lines. The expected time to a drawdown stop: sigma squared over "
            "two mu squared, times e to the a, minus one, minus a, where a is twice the drift times the stop over the "
            "variance. And the expected peak before the stop: sigma squared over two mu, times e to the a minus one. "
            "Both fall back to the driftless case when the manager has no skill."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"A drawdown stop on a return series", F.apply_stop, "r = np.asarray(r, float)", 17, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter ten's rule. Walk through the returns; while standing aside, count down the time-out and then "
            "restart from a fresh peak; otherwise take the return, update the running peak, and if the fall from it "
            "reaches the threshold, count a stop and stand aside. Every stop the House ever applies goes through these "
            "lines."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"A platform, one month", F.platform, "for t in range(years * steps):", 20, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter three's platform, one month at a time. Each pod's return, with a common shock; the running "
            "peak and the drawdown; halve at the first threshold; at the second, fire the manager, record their true "
            "skill, and hire a new draw from the pool. The skill the rule fires and the skill it keeps are how the "
            "chapter measured selection."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("compliance",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{stop\_time}, \texttt{peak\_at\_stop}, \texttt{stop\_time\_sharpe}", r"the theorem"),
            (r"\texttt{simulate\_stop}, \texttt{apply\_stop}", r"its checks"),
            (r"\texttt{platform}", r"pods, stops, payouts"),
            (r"\texttt{implied\_daily\_sharpe}, \texttt{binomial\_upper}", r"disclosed statistics"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 34: a desk trades in the House only under limits it can see and an independent desk "
                             r"can enforce (a volatility budget, factor and concentration caps, a liquidity limit set for a "
                             r"crisis, and a drawdown rule whose stop time is computed in advance); behind pre-trade "
                             r"checks and a kill switch; with every order recorded and surveilled; and with every "
                             r"strategy reaching capital through review, incubation and a ramp sized on the posterior, "
                             r"its trials counted.", 12.4, 16, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds, in the House's new firm module: the theorem, its checks, the platform and the "
            "disclosed-statistic map. <bookmark mark='a'/> And the compliance desk, lit on the chart. "
            "<bookmark mark='b'/> The thirty-fourth rule. A desk trades in the House only under limits it can see and an "
            "independent desk can enforce: a volatility budget, factor and concentration caps, a liquidity limit set for "
            "a crisis, and a drawdown rule whose stop time is computed in advance; behind pre-trade checks and a kill "
            "switch; with every order recorded and watched; and with every strategy reaching capital through review, "
            "incubation and a ramp sized on the evidence, its trials counted."
        ) as vo:
            self.play(FadeIn(chart), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=3))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["compliance"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the platform pitch with a Sharpe of 3", r"ask how many pods were closed and whether their "
                          r"losses are in the record; ask what share of gross P\&L the pods were paid (Chapter 3)",
                          width=12.0, font_size=19),
            desk_question(r"the manager stopped out at 7.5\%", r"ask how deep the stop was in volatilities; at half a "
                          r"volatility, a good manager is stopped within months (the research chapter)", width=12.0,
                          font_size=19),
            desk_question(r"the algorithm that went live on Friday", r"ask for its price, size and rate checks, its credit "
                          r"limit and who holds the kill switch (Chapter 5)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A platform pitching a Sharpe ratio of three: ask how "
            "many pods were closed, whether their losses are in the record, and what share of gross profit the pods were "
            "paid. <bookmark mark='b'/> A manager stopped out at seven and a half percent: ask how deep that was in "
            "volatilities. <bookmark mark='c'/> And an algorithm that went live on Friday: ask for its checks, its credit "
            "limit, and who holds the kill switch."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
