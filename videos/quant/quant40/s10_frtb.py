from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from videos.quant.quant40.common import ladder, pause_card, desk_question
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
            "Chapter nine, and the chosen scaling answer: an eleven-million-dollar ten-day ES becomes twenty-two million at forty days under a single-factor-horizon square-root illustration. This is not the full bank capital calculation. The cached numerical table separately starts from one-day historical ES scaled by root ten; that synthetic base does not meet Basel's requirement to estimate the ten-day base from ten-day risk-factor changes. The distinction is material, not a rounding issue."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self):
        cards = VGroup(
            desk_question(r"1996", r"Basel's market-risk amendment: banks may use their own 99\% ten-day VaR, times at "
                          r"least three, with the traffic light of Chapter 3", width=12.4, font_size=19),
            desk_question(r"2009, Basel 2.5", 'after the crisis, a stressed VaR on a year of turmoil is added, and the framework adds a separate stressed-VaR charge; total capital depends on the prescribed components', width=12.4, font_size=19),
            desk_question(r"2016--2019, FRTB", 'the Fundamental Review of the Trading Book: 97.5\\% ES, liquidity horizons and desk-level approval; implementation dates and local rules vary by jurisdiction', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three historical generations of standards. <bookmark mark='a'/> The nineteen ninety-six market-risk amendment permitted eligible approved models to use ninety-nine percent ten-day VaR with multiplication and other requirements; the traffic-light example concerns a one-day backtest. <bookmark mark='b'/> Basel two point five added a separate stressed-VaR charge based on a qualifying twelve-month stress period. <bookmark mark='c'/> FRTB was issued in twenty sixteen and revised in twenty nineteen: expected shortfall at ninety-seven and a half percent, liquidity horizons and desk-level assessment. Actual implementation dates and local rules vary; this chapter is not a current-jurisdiction compliance determination."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def frtb(self):
        rows = [cmath(r"\text{ES}_{97.5\%}", r"\approx", r"\text{VaR}_{99\%}\ \text{for a normal}", font_size=38,
                      colors={r"\text{ES}_{97.5\%}": ES_C}),
                cmath(r"\text{ES}", r"=", r"\sqrt{\mathrm{ES}_{10}(P)^2+\sum_{j\ge2}\mathrm{ES}_{10}(P,j)^2\frac{LH_j-LH_{j-1}}{10}}",
                      font_size=34),
                cmath(r"\text{calibration}", r":", r"\text{a stressed 12-month period}", font_size=36,
                      colors={r"\text{calibration}": BAD})]
        whys = [why('Chapter 2: the switch from VaR to ES gives a nearby normal-tail coefficient; the complete capital formula and confidence-level comparison are distinct'),
                why(r"liquidity horizons enter through a cascade: risk factors that take longer to exit are shocked over "
                    r"longer horizons"),
                why('a qualifying stressed 12-month period; the prescribed search includes stress back to 2007')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The historical Basel standard specifies ninety-seven-and-a-half percent ES. <bookmark mark='a'/> Its zero-mean Gaussian coefficient is close to, not identical to, ninety-nine percent VaR; that does not equate full capital requirements. <bookmark mark='b'/> Start with ten-day ES for all factors, then add squared contributions from nested subsets of factors whose liquidity horizons exceed each threshold, weighted by successive horizon increments. The ten-day base must use ten-day factor changes rather than scaling shorter-horizon ES. <bookmark mark='c'/> Stress calibration, constrained aggregation, default risk and non-modellable factors add further requirements. This lecture illustrates methodology rather than certifying current local rules."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
            tab.add(VGroup(MathTex(rf"{h['lh']}\ \text{{days}}", font_size=26), label({10:r"large-cap equity price",20:r"IG sovereign spread; large-cap equity volatility",40:r"HY sovereign spread; IG corporate spread",60:r"HY corporate spread; small-cap equity volatility",120:r"credit-spread volatility; other credit spread"}[h["lh"]], font_size=15, color=GREY_A),
                           MathTex(f"{h['es']:.1f}", font_size=26, color=ES_C)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.78 * j, 0])
        foot = wrapped_label('chosen single-horizon scaling: the cached base itself scales one-day historical ES by root ten; not a compliant ten-day base or bank capital. Categories follow the 2019 Basel table, not a current local-law certification',
                             11.4, 16, GREY_A).to_edge(DOWN, buff=0.4)
        hz = q["horizons"]
        with self.voiceover(
            f"Single-horizon scaling illustrations with corrected categories from the twenty-nineteen Basel table. <bookmark mark='a'/> Large-cap equity price has a ten-day floor; investment-grade sovereign spreads and large-cap equity volatility have twenty. The synthetic ten-day base here is {hz[0]['es']:.1f} million dollars. <bookmark mark='b'/> High-yield sovereign and investment-grade corporate spreads use forty days, giving {hz[2]['es']:.1f} under this illustration. Credit-spread volatility uses one hundred and twenty, giving {hz[-1]['es']:.1f}. The original cached category strings were overbroad; these visible labels correct their interpretation without altering the computation. Single-bucket ES scaling is not total capital or a measured liquidation-cost forecast."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(tab[1], scale_factor=1.01), FadeIn(tab[2]))
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
            desk_question(r"P\&L attribution", 'compare risk-theoretical P\\&L with hypothetical P\\&L on the specified static portfolio; statistical thresholds and conditions determine eligibility', width=12.4, font_size=19),
            desk_question(r"non-modellable factors", r"risk factors with too few real prices get their own stress "
                          r"charge, outside the ES", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Internal-model eligibility is assessed at desk level. <bookmark mark='a'/> Historical Basel standards combine desk backtests with profit-and-loss attribution requirements. <bookmark mark='b'/> Attribution compares risk-theoretical P and L with hypothetical P and L for a specified static portfolio, not simply realized front-office trading P and L. A discrepancy is evidence to investigate under the prescribed metrics and thresholds, not an automatic result from any missing factor. <bookmark mark='c'/> Factors failing modellability criteria have separate stressed treatment. The exact current jurisdictional implementation is outside this methodological illustration."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
        whys = [why("Part 37's square-root law, with $Y \\approx 1$: a chosen terminal-impact scale with coefficient one; average execution cost requires a trajectory/integral"),
                why(r"a position of a fifth of a day's volume costs almost half a day's volatility to sell"),
                why(r"so for size, the exit cost is a fifth of the VaR, and it rises in a crisis, when $V$ shrinks and "
                    r"$\sigma$ grows")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Part thirty-seven's square-root impact is an empirical scale, not a universal execution-cost identity. <bookmark mark='a'/> With a chosen unit coefficient, the terminal-impact scale is daily volatility times root quantity over daily volume. <bookmark mark='b'/> At twenty percent participation in volume that is about nought point four five daily volatility. For a cumulative square-root trajectory, averaging over executed quantity gives two thirds of terminal impact before other costs. <bookmark mark='c'/> Comparing either with a two-point-three-three-sigma Gaussian VaR requires compatible price, dollar and horizon units. Liquidity and stress can change coefficients, volume and volatility."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                if k: vo.wait_until(m_)
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
                if k: vo.wait_until(m_)
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
        self.wait(6.0)
        self.clear_scene()
