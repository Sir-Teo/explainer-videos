from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import firm as F
from videos.quant.quant34.common import (BAD, FIRM_C, GOOD, LAW_C, PART, PLAT_C, PM_C, STOP_C, comma, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("virtu"), load("theory"), load("power"), load("platform"), load("stops"))
        self.lab()
        self.lab2()
        self.lab3()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(11, r"Rule 34: the firm", r"What must be true of the firm before any desk trades?", part=PART)
        self.add(c)
        with self.voiceover('Chapter eleven. The proposed firm-level checklist separates mathematical tools from operational controls. Limits, independent authority, records and review matter, but the small functions shown here are not a deployed trading, risk or surveillance system. This lesson authorizes no live strategy.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, v, t, pw, p, s):
        S1 = t["grid"][t["S"].index(1.0)]
        pr = {r["S"]: r for r in pw["rows"]}
        on, off = p["5% vol, halve 5%, cut 7.5% | skill sd 0.5"], p["5% vol, no stops | skill sd 0.5"]
        hml = dict(zip(s["names"], s["rows"]))["HML"]
        rows = [(r"1 loss in 1{,}238: Gaussian/iid implied daily and annual ratio", rf"{v['normal']:.2f},\ {v['annual']:.0f}",
                 GOOD),
                (r"Sharpe 1: years to a stop 0.5 and 1 volatility deep", rf"{S1[0]:.2f},\ {S1[2]:.2f}", STOP_C),
                (r"stopped within 3 years at 1.5 vols: Sharpe 0 and 1", rf"{100 * pr[0.0]['d1.5_3y']:.0f}\%,\ "
                 rf"{100 * pr[1.0]['d1.5_3y']:.0f}\%", STOP_C),
                (r"platform, skill varies: investors' Sharpe with and without stops", rf"{on['investor_sharpe']:.2f},\ "
                 rf"{off['investor_sharpe']:.2f}", PLAT_C),
                (r"share of the platform's P\&L paid to pods", rf"{100 * on['payout_share']:.0f}\%", PLAT_C),
                (r"chosen Gaussian prior: one-year shrink factor", r"0.20", FIRM_C),
                (r"value with a 15\%/12-month stop: Sharpe, no stop and stop", rf"{hml['none']['sharpe']:.2f},\ "
                 rf"{hml['15%/12m']['sharpe']:.2f}", PM_C),
                (r"the trial counter", comma(23552), QC.HOUSE)]
        hx = [-2.4, 4.6]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.5 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The firm's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label('five verified ordinary caches: specified distribution, Brownian mathematics, stipulated simulations and reused factor research; search count from unchanged registration metadata; no sealed outcomes', 12.0, 15, GREY_A).to_edge(DOWN, buff=0.25)
        self.add(title, tab[0], foot)
        with self.voiceover(
            f"""The first sheet separates models and evidence. <bookmark mark='a'/> Under a Gaussian daily model, the disclosed loss frequency maps to ratio {v['normal']:.2f}; square-root annualization also needs its assumptions. A known Brownian Sharpe-one process has mean stop times {S1[0]:.2f} and {S1[2]:.2f} years at these two barriers. The chosen heterogeneous-skill simulation gives investor ratios {on['investor_sharpe']:.2f} and {off['investor_sharpe']:.2f}; its replacement and payout accounting matter. The prior shrink factor is stipulated. Value's factor-stop comparison reuses research data and is before costs. None of these rows is a sealed strategy verdict or a live-firm calibration."""
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
        self.add(card)
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
        self.add(card)
        with self.voiceover(
            'The unchanged arithmetic stop includes the whole breach-period return. It then skips exactly the next wait observations and restarts with a fresh arithmetic peak. That is distinct from drawdown in compounded wealth. Cash is assigned zero return, and costs and execution constraints are absent. The example code defines this research calculation; it does not implement every practical stop a firm might need.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"A platform, one month", F.platform, "for t in range(years * steps):", 20, width=10.6)
        card.move_to(ORIGIN)
        self.add(card)
        with self.voiceover(
            "The platform code applies monthly arithmetic returns with a common shock, then updates drawdowns, scales positions and replaces fired managers with new independent skill draws. Replacement is immediate and frictionless. It resets the fired manager's running state and calendar-year payout accumulator; that accounting choice affects investor comparisons. Year-end restoration and positive-year payouts are additional rules, not consequences of the Brownian theorem."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("compliance",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [(r"\texttt{stop\_time},\ \texttt{peak\_at\_stop}", r"known-parameter mathematics"),
                (r"\texttt{simulate\_stop},\ \texttt{apply\_stop}", r"grid and arithmetic conventions"),
                (r"\texttt{platform}", r"stipulated pods and payout accounting"),
                (r"\texttt{implied\_daily\_sharpe}", r"a specified distributional model")]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=QC.HOUSE), label(b, font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.4) for a,b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 12.5:
            tab.scale_to_fit_width(12.5)
        rule = wrapped_label(r"Proposed Rule 34: independent risk limits; explicit liquidity and funding assumptions; pre-trade controls and authority to stop; complete order records; staged evaluation. An educational checklist, not an implemented live trading or surveillance system.", 12.2, 18, QC.HOUSE).to_edge(DOWN, buff=0.25)
        self.add(chart, tab, rule)
        with self.voiceover("The code illustrates known-parameter stopping mathematics, grid monitoring, an arithmetic research stop and a stipulated payout model. <bookmark mark='a'/> The compliance desk on this chart is a proposed responsibility. <bookmark mark='b'/> Our firm-level checklist asks for independent limits, explicit funding and liquidity assumptions, pre-trade controls, authority to halt, complete records and staged evaluation. A diagram and a pure numerical module do not establish a functioning control system, legal compliance or permission to trade.") as vo:
            vo.wait_until("a")
            self.wait(0.2)
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the platform pitch with a Sharpe of 3", r"ask how many pods were closed and whether their "
                          r"losses are in the record; ask what share of gross P\&L the pods were paid (Chapter 3)",
                          width=12.0, font_size=26),
            desk_question(r"the manager stopped out at 7.5\%", r"ask how deep the stop was in volatilities; at half a "
                          r"volatility, a good manager is stopped within months (the research chapter)", width=12.0,
                          font_size=26),
            desk_question(r"the algorithm that went live on Friday", r"ask for its price, size and rate checks, its credit "
                          r"limit and who holds the kill switch (Chapter 5)", width=12.0, font_size=26),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
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
