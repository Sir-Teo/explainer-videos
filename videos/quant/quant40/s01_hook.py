from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
from videos.quant.quant40.common import HURDLE, PART, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.question(load("sqrt"))
        self.claims(load("backtest"), load("research"), load("ra"))
        self.stakes()
        self.not_risk()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Measuring Risk")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part forty. Measuring risk: the numbers a firm uses to say how much it could lose, how to make them, how to "
            "check them, and what they cannot see. The first part of Act seven, the system."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self, s):
        rows = VGroup(label(r"your 99\% one-day VaR is \$10m", font_size=26),
                      label('a chosen horizon exercise asks for ten days', font_size=26, color=GREY_A),
                      label(r"what is it, and what did you assume?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        ratio = s["direct"] / s["one_day"]
        with self.voiceover(
            f"A desk question. <bookmark mark='a'/> Your ninety-nine percent one-day value at risk is ten million dollars. <bookmark mark='b'/> A chosen horizon exercise asks for ten days. <bookmark mark='c'/> Root ten gives about thirty-two million only for zero-mean independent Gaussian additive daily losses with constant variance. A nonzero mean adds linearly. The cached historical exercise sums ten simple daily returns, rather than compounding wealth; its ratio is {ratio:.1f}. That descriptive comparison neither identifies clustering as the sole cause nor certifies a regulatory capital number."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, b, r, ra):
        n = b["methods"]["normal"]
        r2 = [x for x in ra["rows"] if x["theta"] == 2.0][0]
        p = r["power"]
        cards = VGroup(
            desk_question('a descriptive filter comparison', rf"normal VaR: "
                          rf"{100 * n['rate']:.2f}\% exceptions versus 1\%; GJR-filtered results did not reject selected tests; initialization limits strict forecasting claims", width=12.4, font_size=19),
            desk_question('scoring differs from calibration', rf"no strictly consistent score for ES alone on this class; joint VaR--ES scores exist; the chosen Z2 alternative rejects {100 * p['z2']:.0f}\%", width=12.4, font_size=19),
            desk_question('a dependence sensitivity exercise', rf"a finite-grid Pareto rearrangement estimate is "
                          rf"{r2['worst_lo'] / r2['comonotonic']:.1f} times the sum of the VaRs", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"What this part measures. <bookmark mark='a'/> The normal forecast has {100*n['rate']:.2f} percent exceptions against one percent. Selected GJR-filtered tests do not reject, but filtering initialization uses part of each refit segment, so this is not a fully past-measurable forecasting certificate. <bookmark mark='b'/> Expected shortfall is not elicitable alone on the class shown: no strictly consistent standalone score exists. That is different from being impossible to backtest; joint scores and calibration tests answer different questions. <bookmark mark='c'/> A finite-grid Pareto rearrangement estimate is {r2['worst_lo']/r2['comonotonic']:.1f} times the sum of individual VaRs, showing dependence sensitivity without certifying a global optimum."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"it sets capital", r"banks' trading capital, clearing houses' margins and funds' limits are "
                          r"all risk numbers; get them wrong and the firm is either fragile or idle", width=12.4,
                          font_size=19),
            desk_question(r"it failed in public", r"in 2007--08 banks reported VaR exceptions in clusters, and losses "
                          r"many times their stated VaR, as reported", width=12.4, font_size=19),
            desk_question(r"why the House cares", r"every desk it has built now needs a limit, and every limit is a risk "
                          r"number someone must defend", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Risk numbers set capital: banks' trading capital, clearing houses' "
            "margins, funds' limits. Wrong one way and the firm is fragile, wrong the other and it is idle. "
            "<bookmark mark='b'/> They failed in public in twenty oh seven and oh eight, with exceptions in clusters and "
            "losses many times the stated VaR, as reported. <bookmark mark='c'/> And every desk the House has built now "
            "needs a limit, which is a risk number someone must defend."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_risk(self):
        cards = VGroup(
            desk_question(r"not the worst case", 'VaR is a quantile: under a continuous correctly calibrated model, the exceedance probability is one percent, and it says nothing about how much', width=12.4, font_size=19),
            desk_question(r"not a property of the position", r"it is a forecast from a model and a window; another model "
                          r"or window gives another number, and the difference is information", width=12.4, font_size=19),
            desk_question(r"not the whole risk", r"liquidity, dependence in the tail, and events the data never held sit "
                          r"outside any one number", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three things a risk number is not. <bookmark mark='a'/> It is not a worst-case bound: a correctly calibrated continuous ninety-nine percent VaR has one percent exceedance probability, with no promised maximum severity. Atoms can make strict exceedance less frequent. <bookmark mark='b'/> It depends on positions, horizon, valuation and the forecast distribution; another model or window can give a different number. <bookmark mark='c'/> One market-risk quantile does not exhaust liquidity, custody, legal or systemic risks."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Act six built every trading desk. Act seven steps back to the system: this part measures "
            "risk, Part forty-one follows leverage and liquidity into crises, Part forty-two lets machines into the "
            "market, and Part forty-three asks whether any of it beats the market."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1952, r"Roy's safety first", I), (1974, r"extreme-value tails", I), (1985, r"Osband", I),
                   (1994, r"RiskMetrics", I), (1996, r"Basel's VaR", I), (1999, r"coherent measures", I),
                   (2000, r"McNeil--Frey", I), (2004, r"CAViaR", I), (2008, r"the crisis", I),
                   (2011, r"Gneiting", I), (2016, r"FRTB; Fissler--Ziegel", I), (2019, r"the FZ0 score", I)]
        strip = era_strip(entries, y0=1948, y1=2025, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Seventy years of measuring risk", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "Seventy years. Andrew Roy's safety-first rule of nineteen fifty-two; the extreme-value theorems of the "
            "seventies; Kent Osband's thesis on eliciting; and J.P. Morgan's RiskMetrics. <bookmark mark='a'/> Then "
            "Basel's VaR, coherent risk measures, McNeil and Frey's GARCH with an extreme tail, and CAViaR. "
            "<bookmark mark='b'/> Then the crisis, Gneiting's elicitability, the move to expected shortfall in FRTB with "
            "Fissler and Ziegel's joint score, and its practical form."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"VaR three ways, RiskMetrics, and the square root of time",
            r"Coherence: why VaR is not subadditive and ES is",
            r"Backtests: Kupiec, Christoffersen, the traffic light, Acerbi--Székely",
            r"Tails and dependence: extreme-value theory, copulas, tail dependence",
            r"Stress, reverse stress, and the rearrangement algorithm",
            r"Learned risk: CAViaR and a quantile network against GARCH",
            r"For the researcher: elicitability, and what can be backtested",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: value at risk three ways; coherence and expected shortfall; backtests; tails and dependence; "
            "stress tests and model uncertainty; learned risk models; regulation and liquidity; and the theory of what "
            "can be backtested, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("portfolio", "compliance"))
        with self.voiceover(
            "In the House, the risk function takes over the evening report for every desk, and starts by asking how it "
            "would know if its own numbers were wrong."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
