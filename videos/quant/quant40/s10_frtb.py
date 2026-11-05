from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import (
    BAD,
    ES_C,
    PART,
    TAIL_C,
    load,
)


class FRTB(VoiceoverScene):
    def construct(self):
        q = load("liq")
        self.card(q)
        self.history()
        self.frtb()
        self.horizons(q)
        self.stressed()
        self.desks()
        self.lvar(q)
        self.impact()
        self.ccp()
        self.question()

    def card(self, q):
        hz = {h["lh"]: h["es"] for h in q["horizons"]}
        c = chapter_card(9, r"Regulation and liquidity", r"How long does it take to get out, and what does it cost?",
                         part=PART)
        with self.voiceover(
            "Chapter nine, and the answer to the pause: twice as much. FRTB scales a ten-day shortfall by the square root "
            "of the liquidity horizon over ten, so forty days doubles it: on this book, from "
            f"{hz[10]:.1f} to {hz[40]:.1f} million dollars. The rule's idea is right, that illiquid positions carry "
            "more risk; its square root is the assumption Chapter one questioned."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self):
        cards = VGroup(
            desk_question(r"1996", r"Basel's market-risk amendment: banks may use their own 99\% ten-day VaR, times at "
                          r"least three, with the traffic light of Chapter 3", width=12.4, font_size=19),
            desk_question(r"2009, Basel 2.5", r"after the crisis, a stressed VaR on a year of turmoil is added, and "
                          r"capital for trading books roughly doubles, as reported", width=12.4, font_size=19),
            desk_question(r"2016--2019, FRTB", r"the Fundamental Review of the Trading Book: 97.5\% ES, liquidity "
                          r"horizons, desk-level approval; still being phased in across jurisdictions", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three generations of rules. <bookmark mark='a'/> In nineteen ninety-six, banks could use their own "
            "ninety-nine percent ten-day VaR for capital, times at least three, policed by the traffic light. "
            "<bookmark mark='b'/> After the crisis, Basel two point five added a stressed VaR, measured on a year of "
            "turmoil. <bookmark mark='c'/> And the Fundamental Review of the Trading Book, from twenty sixteen: expected "
            "shortfall at ninety-seven and a half, liquidity horizons, and approval desk by desk, still being phased in."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def frtb(self):
        rows = [cmath(r"\text{ES}_{97.5\%}", r"\approx", r"\text{VaR}_{99\%}\ \text{for a normal}", font_size=38,
                      colors={r"\text{ES}_{97.5\%}": ES_C}),
                cmath(r"\text{ES}", r"=", r"\sqrt{\textstyle\sum_j \bigl(\text{ES}_j\sqrt{(LH_j - LH_{j-1})/10}\bigr)^2}",
                      font_size=34),
                cmath(r"\text{calibration}", r":", r"\text{a stressed 12-month period}", font_size=36,
                      colors={r"\text{calibration}": BAD})]
        whys = [why(r"Chapter 2: the switch from VaR to ES keeps normal-world capital the same and raises it where tails "
                    r"are fat"),
                why(r"liquidity horizons enter through a cascade: risk factors that take longer to exit are shocked over "
                    r"longer horizons"),
                why(r"and the shortfall is computed as if the worst year in the bank's history were happening now")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "FRTB's measure. <bookmark mark='a'/> Expected shortfall at ninety-seven and a half percent, the same as "
            "ninety-nine percent VaR for a normal and larger when tails are fat. <bookmark mark='b'/> Liquidity horizons "
            "enter through a cascade: factors that take longer to exit are shocked over longer horizons, and the pieces "
            "are combined by a square root of a sum of squares. <bookmark mark='c'/> And the shortfall is calibrated to a "
            "stressed year, as if the bank's worst year were happening now."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def horizons(self, q):
        hx = [-3.6, 0.8, 4.2]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"liquidity horizon, roughly", r"examples",
                                                                         r"ES, \$m")])
        tab = VGroup(head)
        for h in q["horizons"]:
            tab.add(VGroup(MathTex(rf"{h['lh']}\ \text{{days}}", font_size=26), label(h["what"], font_size=16, color=GREY_A),
                           MathTex(f"{h['es']:.1f}", font_size=26, color=ES_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.78 * j, 0])
        foot = wrapped_label(r"a \$100m book with the US market's 10-day 97.5\% ES since 2010, scaled by $\sqrt{LH/10}$ as "
                             r"if all of it sat in one bucket: an illustration of the scaling, not of a bank's capital",
                             11.4, 16, GREY_A).to_edge(DOWN, buff=0.4)
        hz = q["horizons"]
        with self.voiceover(
            "The horizons, roughly as the rules set them. <bookmark mark='a'/> Ten days for large-cap equity and major "
            f"currencies: on a hundred-million-dollar book, {hz[0]['es']:.1f} million. <bookmark mark='b'/> Forty for "
            f"sovereign credit, {hz[2]['es']:.1f}; a hundred and twenty for the least liquid credit, {hz[-1]['es']:.1f}. "
            "The same price risk costs three and a half times as much capital if it takes four months to sell."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def stressed(self):
        rows = [cmath(r"\text{ES}_{\text{stressed}}", r"=", r"\text{ES}_{R,S} \times \frac{\text{ES}_{F,C}}{\text{ES}_{R,C}}",
                      font_size=40, colors={r"\text{ES}_{\text{stressed}}": BAD}),
                cmath(r"R \subset F", r":", r"\text{reduced set of factors with stressed history}", font_size=34)]
        whys = [why(r"the shortfall on a reduced set of risk factors over the stressed year, scaled up by how much the "
                    r"full set adds today"),
                why(r"because many factors have no data for the stressed year: the reduced set must explain most of "
                    r"today's risk")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "How the stress enters. <bookmark mark='a'/> The shortfall of a reduced set of risk factors over the stressed "
            "year, scaled up by the ratio of the full set's shortfall to the reduced set's today. "
            "<bookmark mark='b'/> The reduced set exists because many of today's factors had no prices in the stressed "
            "year; it must explain most of today's risk for the scaling to be trusted."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def desks(self):
        cards = VGroup(
            desk_question(r"desk by desk", r"each trading desk must pass its own VaR backtest and a P\&L attribution test "
                          r"to use internal models; others fall back to standard formulas", width=12.4, font_size=19),
            desk_question(r"P\&L attribution", r"the risk model's P\&L must track the front office's: if the risk system "
                          r"misses a factor, the two diverge, and the desk fails", width=12.4, font_size=19),
            desk_question(r"non-modellable factors", r"risk factors with too few real prices get their own stress "
                          r"charge, outside the ES", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And who may use a model. <bookmark mark='a'/> Each desk must pass its own VaR backtest and a profit and loss "
            "attribution test. <bookmark mark='b'/> Attribution asks whether the risk model's profit and loss tracks the "
            "front office's: a missing factor makes them diverge. <bookmark mark='c'/> And factors with too few real "
            "prices get a separate stress charge, outside the shortfall."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lvar(self, q):
        rows = [cmath(r"\text{LVaR}", r"=", r"\text{VaR} + \tfrac12\bigl(\mu_s + k\,\sigma_s\bigr) \times \text{position}",
                      font_size=38, colors={r"\text{LVaR}": BAD}),
                cmath(r"\$100\text{m},\ \mu_s = 10\,\text{bp},\ \sigma_s = 5\,\text{bp}", r":",
                      rf"{q['var_m']:.2f} \to {q['lvar']:.2f}\ \text{{\$m}}", font_size=34)]
        whys = [why(r"Bangia, Diebold, Schuermann and Stroughair (1999): add the cost of crossing half the spread, at a "
                    r"stressed spread $\mu_s + k\sigma_s$"),
                why(r"for a liquid book the spread is small beside the price risk; for an illiquid one it is not, and the "
                    r"bigger cost is the impact of selling size")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-0.3, buff=0.7, edge=6.9)
        with self.voiceover(
            "Liquidity in the number itself. <bookmark mark='a'/> Anil Bangia and coauthors' liquidity-adjusted VaR adds "
            "the cost of crossing half a stressed spread. <bookmark mark='b'/> On a hundred million dollars with a ten "
            f"basis point spread, VaR rises from {q['var_m']:.2f} to {q['lvar']:.2f} million: little, for a liquid book. "
            "The larger cost of exiting size is impact."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def impact(self):
        frac = 0.2
        add = math.sqrt(frac)
        rows = [cmath(r"\text{impact}", r"\approx", r"\sigma_{\text{day}}\sqrt{Q/V}", font_size=42, colors={r"\text{impact}": TAIL_C}),
                cmath(r"Q/V = 20\%", r"\Rightarrow", rf"{add:.2f}\,\sigma_{{\text{{day}}}}", font_size=40),
                cmath(r"\text{against VaR}", r"=", r"2.33\,\sigma_{\text{day}}", font_size=40)]
        whys = [why(r"Part 37's square-root law, with $Y \approx 1$: the cost of selling $Q$ against daily volume $V$"),
                why(r"a position of a fifth of a day's volume costs almost half a day's volatility to sell"),
                why(r"so for size, the exit cost is a fifth of the VaR, and it rises in a crisis, when $V$ shrinks and "
                    r"$\sigma$ grows")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Part thirty-seven's square root again. <bookmark mark='a'/> Selling a quantity Q against daily volume V costs "
            "about a day's volatility times root Q over V. <bookmark mark='b'/> A position a fifth of a day's volume "
            f"costs {add:.2f} of a day's volatility to sell, <bookmark mark='c'/> a fifth of the ninety-nine percent VaR, "
            "and in a crisis volume shrinks as volatility grows. Liquidity risk is not a correction; for large books it is "
            "a second risk."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def ccp(self):
        cards = VGroup(
            desk_question(r"initial margin is a VaR", r"clearing houses set margin as a 99\% or 99.5\% loss over the time "
                          r"needed to close a defaulter's position, two to five days: Part 21's clearing", width=12.4,
                          font_size=19),
            desk_question(r"procyclicality", r"a VaR that reacts quickly, as Chapter 3 recommends, raises margin calls in "
                          r"the middle of a crash, forcing sales; March 2020's calls were large, as reported", width=12.4,
                          font_size=19),
            desk_question(r"the remedies", r"floors on margin, buffers released in stress, and a share of stressed data "
                          r"in every window: a forecast tempered so that it does not amplify what it measures", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Risk numbers also set margin. <bookmark mark='a'/> A clearing house's initial margin is a VaR: a ninety-nine "
            "or ninety-nine point five percent loss over the days needed to close a defaulter's position, Part "
            "twenty-one's clearing. <bookmark mark='b'/> But a VaR that reacts quickly, as Chapter three recommends, "
            "raises margin calls in the middle of a crash and forces sales: procyclicality, visible in March twenty "
            "twenty, as reported. <bookmark mark='c'/> So the rules add floors, buffers released in stress, and stressed "
            "data in every window: a forecast tempered so that it does not amplify what it measures."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House's evening risk report shows a 99\% one-day VaR. Which three other numbers should sit "
                       r"beside it, so that a reader can judge it?")
        with self.voiceover(
            "Pause and predict. The House's evening risk report shows a ninety-nine percent one-day VaR. Which three other "
            "numbers should sit beside it, so that a reader can judge it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
