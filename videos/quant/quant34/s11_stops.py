from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, PNL_C, STOP_C, fit_right, load

RULES = ["10%/3m", "10%/12m", "15%/3m", "15%/12m", "20%/3m", "20%/12m"]


class Stops(VoiceoverScene):
    def construct(self):
        s = load("stops")
        self.card()
        self.setup_()
        self.null()
        self.table(s)
        self.heat(s)
        self.why_(s)
        self.trials(s)
        self.question()

    def card(self):
        c = chapter_card(10, r"Do drawdown stops help?", r"On real premia, does cutting a losing strategy pay?", part=PART)
        with self.voiceover("Chapter ten. Platforms stop managers; do stops help a strategy with a real premium? The "
                            "House tests it on half a century of Kenneth French's factors, against a null that says "
                            "exactly what a stop should do if returns were independent."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"x_t", r"=", r"\frac{10\%/\sqrt{12}}{\hat\sigma_{t,36}}\, f_t", font_size=36, colors={r"x_t": PNL_C}),
                cmath(r"\text{stop}", r":", r"\text{drawdown} \ge D \Rightarrow \text{flat for } w \text{ months, then restart}",
                      font_size=30, colors={r"\text{stop}": STOP_C}),
                cmath(r"D \in \{10, 15, 20\}\%,\ w \in \{3, 12\}", r":", r"\text{six rules, six factors}", font_size=30)]
        whys = [why(r"each factor (market, size, value, profitability, investment, momentum) scaled to 10\% volatility "
                    r"with the trailing three years' volatility, from 1966 to 2020"),
                why(r"when the drawdown from the peak reaches $D$, stand aside for $w$ months, then start again from a "
                    r"new peak"),
                why(r"stops one to two volatilities deep, and short or long time-outs: 36 combinations")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The test. <bookmark mark='a'/> Six factors: the market, size, value, profitability, investment and "
            "momentum, each scaled to ten percent volatility using only the trailing three years. "
            "<bookmark mark='b'/> A stop: when the drawdown from the peak reaches D, stand aside for w months, then start "
            "again. <bookmark mark='c'/> Three depths, one to two volatilities, and two time-outs: six rules, on six "
            "factors, thirty-six combinations."
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

    def null(self):
        rows = [cmath(r"\text{i.i.d. returns}", r"\Rightarrow", r"\text{the past drawdown says nothing about the future}",
                      font_size=30),
                cmath(r"S_{\text{stop}}", r"\approx", r"S\sqrt{1 - \text{time out}}\ <\ S", font_size=36,
                      colors={r"S_{\text{stop}}": BAD}),
                cmath(r"\text{null}", r":", r"\text{the same rule on the months shuffled}", font_size=32,
                      colors={r"\text{null}": HURDLE})]
        whys = [why(r"if returns are independent, a stop throws away future months at random"),
                why(r"the mean falls with the time invested, the volatility with its square root: a stop can only lower "
                    r"the Sharpe ratio"),
                why(r"shuffling keeps each factor's distribution and destroys its serial dependence; 200 shuffles per "
                    r"rule give the change a stop makes by chance")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What theory predicts. <bookmark mark='a'/> If returns are independent, a drawdown says nothing about the "
            "future, and a stop throws away months at random. <bookmark mark='b'/> The mean falls in proportion to the "
            "time invested and the volatility only with its square root, so a stop can only lower the Sharpe ratio. "
            "<bookmark mark='c'/> So the null is the same rule on the months shuffled: the factor's own distribution, "
            "with every serial dependence removed. A stop helps only if it beats its shuffle."
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

    def table(self, s):
        hx = [-4.4, -2.0, 0.4, 2.8, 5.0]
        head = VGroup(label(r"factor", font_size=17, color=GREY_B), label(r"no stop", font_size=17, color=GREY_B),
                      label(r"15\%, 12 months", font_size=17, color=STOP_C), label(r"shuffled", font_size=17,
                                                                                   color=HURDLE),
                      label(r"stops taken", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for n, r in zip(s["names"], s["rows"]):
            q = r["15%/12m"]
            tab.add(VGroup(label(n, font_size=20), MathTex(f"{r['none']['sharpe']:.2f}", font_size=26),
                           MathTex(f"{q['sharpe']:.2f}", font_size=26),
                           MathTex(rf"{r['none']['sharpe'] + q['null_change']:.2f} \pm {q['null_sd']:.2f}", font_size=24),
                           MathTex(f"{q['stops']}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.65 * j, 0])
        start = s["start"]
        foot = wrapped_label(rf"monthly, {start // 100}-{start % 100:02d} to 2020-12; Sharpe ratios include the months "
                             r"spent flat; shuffled: the rule on 200 shuffles, mean $\pm$ sd", 11.4, 15,
                             GREY_A).to_edge(DOWN, buff=0.5)
        rv = dict(zip(s["names"], s["rows"]))
        hml, umd = rv["HML"], rv["UMD"]
        h0, h1 = hml["none"]["sharpe"], hml["15%/12m"]["sharpe"]
        u0, u1 = umd["none"]["sharpe"], umd["15%/12m"]["sharpe"]
        with self.voiceover(
            "One rule, a stop one and a half volatilities deep with a year out. <bookmark mark='a'/> Each factor's "
            "Sharpe ratio without it, and with it. <bookmark mark='b'/> And the shuffle: always a little lower than no "
            f"stop, as theory says. Value goes from {h0:.2f} to {h1:.2f}, well above its shuffle; momentum from "
            f"{u0:.2f} to {u1:.2f}, at its shuffle. The market and the others sit in between."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2], r_[4])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def heat(self, s):
        Z = np.array([[r[k]["change"] - r[k]["null_change"] for k in RULES] for r in s["rows"]])
        sd = np.array([[r[k]["null_sd"] for k in RULES] for r in s["rows"]])
        cells = VGroup()
        for i, n in enumerate(s["names"]):
            for j, k in enumerate(RULES):
                z = Z[i, j]
                t = float(np.clip((z + 0.25) / 0.5, 0, 1))
                sq = Rectangle(width=1.5, height=0.62, fill_color=interpolate_color(ManimColor(RED_D), ManimColor(GREEN_D), t),
                               fill_opacity=0.85, stroke_color=GREY_D, stroke_width=1)
                sq.move_to([-3.2 + 1.55 * j, 1.8 - 0.67 * i, 0])
                star = r"^{*}" if abs(z) > 2 * sd[i, j] else ""
                cells.add(VGroup(sq, MathTex(rf"{z:+.2f}{star}", font_size=22).move_to(sq)))
        rl = VGroup(*[label(n, font_size=18).move_to([-5.3, 1.8 - 0.67 * i, 0]) for i, n in enumerate(s["names"])])
        cl = VGroup(*[label(k.replace("%", r"\%"), font_size=15, color=GREY_B).move_to([-3.2 + 1.55 * j, 2.45, 0])
                      for j, k in enumerate(RULES)])
        foot = wrapped_label(r"each cell: the stop's change in Sharpe ratio less the shuffle's; $^*$ beyond two shuffle "
                             r"standard deviations", 11.0, 15, GREY_A).to_edge(DOWN, buff=0.45)
        n_pos = int(np.sum(Z > 2 * sd))
        n_neg = int(np.sum(Z < -2 * sd))
        with self.voiceover(
            "All thirty-six, measured against their shuffles. <bookmark mark='a'/> Green, the stop beat the shuffle; red, "
            f"it lost to it. {n_pos} combinations beat their shuffle by more than two standard deviations, and {n_neg} "
            "lost by as much. <bookmark mark='b'/> The pattern is by factor, not by rule: almost every premium here gains "
            "from a stop relative to its shuffle, because its losses persist; momentum is the exception, at its shuffle "
            "everywhere, and below it with the tightest stop and the longest time-out."
        ) as vo:
            self.play(FadeIn(rl), FadeIn(cl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*cells[-6:]), color=WHITE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def why_(self, s):
        cards = VGroup(
            desk_question(r"value and profitability: slow drawdowns", r"their losses come in long episodes (value in "
                          r"1998--2000 and 2018--2020), so a drawdown predicts more drawdown, and stepping aside avoids "
                          r"some of it", width=12.4, font_size=19),
            desk_question(r"momentum: crash and rebound", r"momentum's worst losses are sudden reversals that recover "
                          r"(2009, Part 24); a stop sells at the bottom and sits out the recovery", width=12.4,
                          font_size=19),
            desk_question(r"what a stop really bets on", r"that losses cluster and persist: serial dependence in "
                          r"returns, which some premia have and others do not", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why. <bookmark mark='a'/> Value and profitability lose in long, slow episodes, like value from 1998 to 2000 "
            "and again from 2018, so a drawdown predicts more drawdown, and stepping aside avoids some of it. "
            "<bookmark mark='b'/> Momentum's worst losses are sudden reversals that recover, as in 2009; a stop sells at "
            "the bottom and misses the rebound. <bookmark mark='c'/> A stop is a bet that losses persist. Some premia "
            "have that property, and some do not."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def trials(self, s):
        rows = [cmath(r"36\ \text{combinations}", r"\Rightarrow", r"\text{the best one is flattered}", font_size=32,
                      colors={r"36\ \text{combinations}": BAD}),
                cmath(r"\text{for a platform}", r":", r"\text{stops are about unknown skill, not premia}", font_size=30,
                      colors={r"\text{for a platform}": FIRM_C}),
                cmath(r"\text{not registered}", r":", r"\text{a finding about factors, with its trials stated}", font_size=30)]
        whys = [why(r"choosing the best stop for each factor after seeing these results would be Part 26's mistake"),
                why(r"Chapter 3's platform stops managers to learn about skill; here the skill is known to be a premium, "
                    r"and the question is only serial dependence"),
                why(r"the House records it as research with 36 trials; no stop rule is added to any registered book")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And the caveat. <bookmark mark='a'/> Thirty-six combinations were tried, so choosing the best stop for each "
            "factor now would be Part twenty-six's mistake. <bookmark mark='b'/> For a platform the question is "
            "different: it stops managers to learn about unknown skill, which these factors do not have to prove. "
            "<bookmark mark='c'/> So the House records this as research, with its thirty-six trials stated, and adds no "
            "stop to any registered book."
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

    def question(self):
        q = pause_card(r"a strategy with i.i.d. returns and Sharpe 0.6 is stopped out a quarter of the time. Roughly what "
                       r"Sharpe ratio does it show, counting the months flat?")
        with self.voiceover(
            "Pause and predict. A strategy with independent returns and a Sharpe ratio of point six is stopped out a "
            "quarter of the time. Roughly what Sharpe ratio does it show, counting the months it was flat?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
