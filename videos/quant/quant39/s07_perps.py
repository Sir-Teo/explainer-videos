from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
from videos.quant.quant39.common import (
    BAD,
    GOOD,
    HURDLE,
    PART,
    PERP_C,
    fit_right,
    load,
)


class Perps(VoiceoverScene):
    def construct(self):
        f = load("funding")
        self.card(f)
        self.mechanics()
        self.rule()
        self.no_arb()
        self.interest()
        self.series(f)
        self.by_year(f)
        self.scatter(f)
        self.who_pays()
        self.question(f)

    def card(self, f):
        b = f["BTCUSDT"]
        c = chapter_card(6, r"Perpetual futures", r"What holds a future with no expiry to its spot price?", part=PART)
        with self.voiceover(
            "Chapter six, and the answer to the pause: funding. Every eight hours, holders on one side pay the other, "
            "and the payment grows with the perpetual's premium over spot. Longs pay when it trades above, which on "
            f"Bitcoin has been most of the time: about {b['annual_pct']:.0f} percent a year on average since twenty "
            "twenty."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        rows = [cmath(r"\text{every 8 hours}", r":", r"\text{longs pay } r_f \times \text{position value}", font_size=36,
                      colors={r"\text{every 8 hours}": PERP_C}),
                cmath(r"r_f > 0", r"\Rightarrow", r"\text{longs pay shorts}", font_size=38),
                cmath(r"r_f < 0", r"\Rightarrow", r"\text{shorts pay longs}", font_size=38),
                cmath(r"\text{no expiry}", r":", r"\text{no roll, leverage up to } 100\times", font_size=36)]
        whys = [why('the sample uses the historical eight-hour convention; actual product intervals, caps and terms vary'),
                why(r"when the contract trades above the index of spot prices, holding it long costs money, which pulls "
                    r"longs out and shorts in"),
                why('a sufficiently negative premium can yield negative funding; a small negative premium can still have positive funding'),
                why(r"a future that never has to be rolled, margined as in Part 2")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Funding transfers cash between contract sides. <bookmark mark='a'/> In the sampled eight-hour contract convention, a positive settlement rate makes longs pay shorts on settlement notional. Actual products can use other intervals and caps. <bookmark mark='b'/> A sufficiently positive premium can raise funding, discouraging longs. <bookmark mark='c'/> A negative spot-perpetual premium does not automatically imply negative funding: the clamped interest term can keep it positive near zero. <bookmark mark='d'/> Perpetuals have no scheduled expiry, so linkage to spot depends on funding incentives, arbitrage constraints and contract rules, rather than a guaranteed terminal convergence date."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def rule(self):
        rows = [cmath(r"\text{premium index}", r"=", r"\text{average of } \tfrac{\text{perpetual} - \text{index}}{\text{index}}",
                      font_size=34),
                cmath(r"r_f", r"=", r"\bar p + \operatorname{clamp}(i - \bar p,\ \pm 0.05\%)", font_size=38,
                      colors={r"r_f": PERP_C}),
                cmath(r"|\bar p - i| < 0.05\%", r"\Rightarrow", r"r_f = i = 0.01\%", font_size=38,
                      colors={r"r_f = i = 0.01\%": HURDLE})]
        whys = [why(r"measured from the prices at which the perpetual can be bought and sold, over the eight hours"),
                why(r"Binance's published formula: the premium plus an interest term $i$ of 0.01\% per eight hours, "
                    r"pulled toward it within a band (the House's \texttt{binance\_funding\_rule})"),
                why(r"so whenever the premium is small, funding is exactly the interest rate: 0.01\% every eight hours, "
                    r"about 11\% a year")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The simplified rule in matching eight-hour units. <bookmark mark='a'/> The venue's premium index is a contract-defined index, not simply the difference of hourly closing prices. <bookmark mark='b'/> Funding equals average premium plus the interest-minus-premium term clamped between minus and plus five basis points, under the stated historical convention and before any other caps. <bookmark mark='c'/> If the absolute premium-minus-interest difference is at most five basis points, the rate equals the one-basis-point interest term. Product-specific intervals, index construction, caps and rules must be checked separately. This chosen representation is not a certification of today's venue terms."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def no_arb(self):
        rows = [cmath(r"\text{long perpetual}", r":", r"dF - \kappa\,(F - S)\,dt", font_size=38, colors={r"\text{long perpetual}": PERP_C}),
                cmath(r"\mathbb E^{\mathbb Q}[dF]", r"=", r"\kappa\,(F - S)\,dt", font_size=38),
                cmath(r"F = cS", r"\Rightarrow", r"c\,(r - q) = \kappa\,(c - 1)", font_size=38),
                cmath(r"F", r"=", r"\frac{\kappa}{\kappa - (r - q)}\,S", font_size=44, colors={r"F": HURDLE})]
        whys = [why(r"funding paid continuously at intensity $\kappa$ on the gap to spot; a futures position costs "
                    r"nothing to enter"),
                why(r"so its gains must be a martingale under the pricing measure of Part 9"),
                why(r"try a price proportional to spot; spot drifts at $r - q$ under $\mathbb Q$, where $q$ is what the coin "
                    r"earns when lent"),
                why('constant coefficients, matched time units, $\\kappa>r-q$ and transversality; separate from the discrete clamped rule')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A separate continuous-funding model. <bookmark mark='a'/> The long's gains are d F minus kappa times F minus S, times dt. <bookmark mark='b'/> Under a pricing measure, its zero-value gains have zero drift, and spot has drift r minus q. Assume constant coefficients, a linear contract and matching continuous-time units. <bookmark mark='c'/> Try F equal to a constant multiple of S, then equate that multiple times r minus q with kappa times the multiple minus one. <bookmark mark='d'/> This gives F equal to kappa S divided by kappa minus the quantity r minus q, requiring kappa greater than r minus q and a transversality condition to exclude bubbles. This model is distinct from the venue's discrete clamped rule."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def interest(self):
        rows = [cmath(r"i", r"=", r"0.01\% \times 3 \times 365 \approx 11\%\ \text{a year}", font_size=40,
                      colors={r"i": HURDLE}),
                cmath(r"\text{premium} \approx 0", r"\Rightarrow", r"\text{longs still pay } 11\%", font_size=38),
                cmath(r"\text{a short perpetual} + \text{spot}", r"=", r"\text{funding receipt; basis and margin remain}",
                      font_size=34, colors={r"\text{funding receipt; basis and margin remain}": GOOD})]
        whys = [why(r"the interest term, built into the rule: a stand-in for the difference between dollar and coin "
                    r"interest rates"),
                why(r"so even when the perpetual trades at spot, the rule charges longs about 11\% a year"),
                why('future funding and basis are uncertain; match capital, fees, collateral and settlement units')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Translate the interest term carefully. <bookmark mark='a'/> One basis point every eight hours gives ten point nine five percent a year by simple notional annualization, using three settlements a day and three hundred sixty-five days. <bookmark mark='b'/> That is neither compounding nor a return on committed strategy capital. <bookmark mark='c'/> Near zero premium, the simplified clamp can preserve this positive rate, so a short receives it at those settlements. Future rates, basis moves, financing, fees, margin and venue losses remain variable; there is no fixed contractual yield from merely buying spot and shorting the perpetual."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def series(self, f):
        b = f["BTCUSDT"]["series"]
        t = np.asarray(b["t"], float)
        yr = 2020 + (t - t[0]) / (365.25 * 86400)
        ann = 100 * np.asarray(b["rate"], float) * 3 * 365
        ann = np.clip(ann, -60, 120)
        g = axes([2020, 2026], [-60, 120], x_length=8.0, y_length=4.0, xlabel=r"Bitcoin's perpetual on Binance",
                 ylabel=r"funding, annualised \%", xticks=[2020, 2021, 2022, 2023, 2024, 2025, 2026],
                 yticks=[-60, 0, 11, 60, 120], font_size=15).move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.025, color=GOOD if y >= 0 else BAD) for x, y in zip(yr, ann)])
        base = DashedLine(ax.c2p(2020, 10.95), ax.c2p(2026, 10.95), color=HURDLE, stroke_width=2)
        with self.voiceover(
            "Six years of Bitcoin's funding, every ninth settlement, annualised. <bookmark mark='a'/> A dense line at "
            "about eleven percent: the interest term, whenever the premium is small. <bookmark mark='b'/> Spikes far "
            "above it in the bull market of twenty twenty-one, when leveraged longs paid over a hundred percent a year "
            "for their exposure. <bookmark mark='c'/> And spells below zero, in the crashes of twenty twenty-one and "
            "twenty twenty-two, when shorts paid."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(base))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def by_year(self, f):
        hx = [-4.6, -2.4, -0.4, 1.6, 3.6, 5.6]
        head = VGroup(*[label(t, font_size=14, color=GREY_B) for t in (r"year", r"BTC, a year", r"at 0.01\%",
                                                                         r"negative", r"ETH, a year", r"negative")])
        tab = VGroup(head)
        for yb, ye in zip(f["BTCUSDT"]["by_year"], f["ETHUSDT"]["by_year"]):
            tab.add(VGroup(MathTex(str(yb["year"]), font_size=24),
                           MathTex(rf"{yb['annual_pct']:.1f}\%", font_size=24, color=PERP_C),
                           MathTex(rf"{100 * yb['at_base']:.0f}\%", font_size=24, color=HURDLE),
                           MathTex(rf"{100 * yb['neg']:.0f}\%", font_size=24, color=BAD),
                           MathTex(rf"{ye['annual_pct']:.1f}\%", font_size=24, color=PERP_C),
                           MathTex(rf"{100 * ye['neg']:.0f}\%", font_size=24, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.66 * j, 0])
        b, e = f["BTCUSDT"], f["ETHUSDT"]
        y21 = b["by_year"][1]
        y22 = b["by_year"][2]
        with self.voiceover(
            f"Describe the frozen sample by year. <bookmark mark='a'/> Bitcoin's mean settlement rate, simply annualized, is {y21['annual_pct']:.0f} percent in twenty twenty-one and {y22['annual_pct']:.0f} in twenty twenty-two; {100 * y22['neg']:.0f} percent of twenty twenty-two settlements are negative. <bookmark mark='b'/> Across the sampled six years, {100 * b['at_base']:.0f} percent of rates fall within the code's tolerance of the one-basis-point base. Mean simple annualized rates are {b['annual_pct']:.0f} percent for Bitcoin and {e['annual_pct']:.0f} for ether. <bookmark mark='c'/> The twenty twenty-five Bitcoin mean is {b['by_year'][5]['annual_pct']:.0f} percent, with {100 * b['by_year'][5]['at_base']:.0f} percent near the base. Changing rates alone do not identify crowding, a policy change or the cause of a premium shift."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:6]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(tab[6]))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, f):
        b = f["BTCUSDT"]
        sp = 100 * np.asarray(b["scatter"]["prem"], float)
        sr = 100 * np.asarray(b["scatter"]["rate"], float)
        ok = (np.abs(sp) < 0.3) & (np.abs(sr) < 0.15)
        g = axes([-0.3, 0.3], [-0.3, 0.3], x_length=6.0, y_length=4.2, xlabel=r"perpetual over spot, prior 8 hours, \%",
                 ylabel=r"funding set, \%", xticks=[-0.3, 0, 0.3], yticks=[-0.25, 0, 0.25], font_size=15)
        g.move_to(LEFT * 2.2 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.025, color=PERP_C, fill_opacity=0.6) for x, y in zip(sp[ok], sr[ok])])
        xs = np.linspace(-0.3, 0.3, 121)
        rule = curve(ax, xs, 100 * D_rule(xs / 100), HURDLE, stroke_width=2.5)
        side = VGroup(label(rf"correlation with the premium: {b['corr_prem']:.2f}", font_size=18, color=PERP_C),
                      label(rf"with Binance's rule applied to it: {b['corr_rule']:.2f}", font_size=18, color=HURDLE),
                      label(r"flat at 0.01\% inside the band", font_size=18, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(side)
        with self.voiceover(
            f"An observable proxy, not an exact rule replication. <bookmark mark='a'/> Each selected point pairs a funding settlement with an average of hourly perpetual-to-spot close ratios from the preceding pre-settlement hours. The code permits some missing observations and uses candle-open timestamps for closes. Correlation with funding is {b['corr_prem']:.2f}. <bookmark mark='b'/> Applying the simplified clamp to that proxy gives correlation {b['corr_rule']:.2f}. The official impact-price premium index, weights, caps and exact observation clocks differ, so correlation does not validate the venue's full calculation or prove a causal mechanism. Display filtering removes points outside the plotted window."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(rule), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def who_pays(self):
        cards = VGroup(
            desk_question(r"the price of leverage", r"positive funding is what leveraged longs pay to hold exposure they "
                          r"could not finance in spot: an interest rate set by crypto's own demand for leverage",
                          width=12.4, font_size=19),
            desk_question(r"a sentiment gauge", r"funding rises in rallies and turns negative in crashes, and forced "
                          r"liquidations cluster at its extremes", width=12.4, font_size=19),
            desk_question(r"Part 2, recalled", r"the margin account of Part 2 paid this funding through March 2020's "
                          r"crash: it is a running cost of every leveraged long", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Who pays, and why. <bookmark mark='a'/> Positive funding is the price of leverage: what leveraged longs pay "
            "for exposure they could not finance in spot, an interest rate set by crypto's own demand for leverage. "
            "<bookmark mark='b'/> It is also a gauge of sentiment, high in rallies and negative in crashes, and "
            "forced liquidations cluster at its extremes. <bookmark mark='c'/> And it is the running cost that Part two's margin "
            "account paid through the crash of March twenty twenty."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self, f):
        q = prediction_card(rf"funding on ether's perpetual averaged about {f['ETHUSDT']['annual_pct']:.0f}\% a year. A desk "
                       r"matches spot and perpetual units. Which common price exposure cancels, which risks remain, and what capital denominator is used?")
        with self.voiceover(
            f"Pause and predict. In the frozen ether sample, the mean settlement rate has a simple notional annualization of {f['ETHUSDT']['annual_pct']:.0f} percent. A desk proposes to buy one unit of spot and short one linear perpetual unit. Which price exposures cancel in the matched-unit ledger, and which funding, basis, margin, custody and execution risks remain? State the capital denominator before turning any payment into a return."
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()


def D_rule(p):
    from explainer.quant.house import defi
    return defi.binance_funding_rule(p)
