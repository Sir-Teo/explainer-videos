from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
                cmath(r"r_f > 0", r"\Leftarrow", r"\text{perpetual above spot}", font_size=38),
                cmath(r"r_f < 0", r"\Rightarrow", r"\text{shorts pay longs}", font_size=38),
                cmath(r"\text{no expiry}", r":", r"\text{no roll, leverage up to } 100\times", font_size=36)]
        whys = [why(r"BitMEX's 2016 design, now the most traded crypto contract: at 00:00, 08:00 and 16:00 UTC on "
                    r"Binance"),
                why(r"when the contract trades above the index of spot prices, holding it long costs money, which pulls "
                    r"longs out and shorts in"),
                why(r"and the reverse below; the payment is between traders, the exchange keeps none of it"),
                why(r"a future that never has to be rolled, margined as in Part 2")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How it works. <bookmark mark='a'/> Every eight hours on Binance, holders of long positions pay a funding "
            "rate times their position's value to holders of short ones. <bookmark mark='b'/> The rate is positive when "
            "the perpetual trades above the spot index, which makes being long costly and pulls the price down. "
            "<bookmark mark='c'/> When it trades below, the rate turns negative and shorts pay. <bookmark mark='d'/> "
            "There is no expiry and no roll, which with high leverage made it the most traded contract in crypto."
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
            "Binance's rule. <bookmark mark='a'/> A premium index averages how far the perpetual trades from the spot "
            "index over the eight hours. <bookmark mark='b'/> The rate is that premium plus an interest term of one "
            "hundredth of a percent, clamped within a band. <bookmark mark='c'/> So whenever the premium is small, "
            "funding is exactly the interest term: a hundredth of a percent every eight hours, about eleven percent a "
            "year, paid by longs."
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
                why(r"He, Manela, Ross and von Wachter's no-arbitrage price, in continuous form: above spot when cash "
                    r"earns more than the coin, by about $(r - q)/\kappa$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Its no-arbitrage price. <bookmark mark='a'/> A long perpetual gains the price change and pays funding at "
            "intensity kappa on the gap to spot. <bookmark mark='b'/> A position costs nothing to enter, so under Part "
            "nine's pricing measure its gains are a martingale. <bookmark mark='c'/> Try a price proportional to spot, "
            "which drifts at the interest rate minus what the coin earns when lent. <bookmark mark='d'/> The answer: "
            "kappa over kappa minus r minus q, times spot, due to Songrun He, Asaf Manela, Omri Ross and Victor von "
            "Wachter. The perpetual sits above spot, by about r minus q over kappa, when dollars earn more than coins."
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
                cmath(r"\text{a short perpetual} + \text{spot}", r"=", r"\text{earns } i \text{ with no price risk}",
                      font_size=34, colors={r"\text{earns } i \text{ with no price risk}": GOOD})]
        whys = [why(r"the interest term, built into the rule: a stand-in for the difference between dollar and coin "
                    r"interest rates"),
                why(r"so even when the perpetual trades at spot, the rule charges longs about 11\% a year"),
                why(r"a fixed, contractual carry, unless the premium turns negative: the trade of the next chapter")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "That interest term matters. <bookmark mark='a'/> A hundredth of a percent three times a day is about "
            "eleven percent a year. <bookmark mark='b'/> So even when the perpetual trades at spot, longs pay it. "
            "<bookmark mark='c'/> And anyone who holds spot and is short the perpetual collects it, with no exposure to "
            "the price: the trade of the next chapter."
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
            f"Year by year. <bookmark mark='a'/> On Bitcoin, funding averaged {y21['annual_pct']:.0f} percent a year in "
            f"twenty twenty-one and {y22['annual_pct']:.0f} in twenty twenty-two, the year of Terra and FTX, when "
            f"{100 * y22['neg']:.0f} percent of settlements were negative. <bookmark mark='b'/> Over all six years, "
            f"{100 * b['at_base']:.0f} percent of settlements sat at exactly the interest term, and the average was "
            f"{b['annual_pct']:.0f} percent; for ether, {e['annual_pct']:.0f}. <bookmark mark='c'/> In twenty "
            f"twenty-five the share at the interest term fell to {100 * b['by_year'][5]['at_base']:.0f} percent, the "
            f"rate never once rose above it, and the carry thinned to {b['by_year'][5]['annual_pct']:.0f} percent: "
            "plausibly, more capital had come to collect it."
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
        g = axes([-0.3, 0.3], [-0.15, 0.15], x_length=6.0, y_length=4.2, xlabel=r"perpetual over spot, prior 8 hours, \%",
                 ylabel=r"funding set, \%", xticks=[-0.3, 0, 0.3], yticks=[-0.1, 0, 0.01, 0.1], font_size=15)
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
            "Does the rule explain the data? <bookmark mark='a'/> Each dot is a settlement: the perpetual's premium over "
            f"spot in the eight hours before, from hourly closes, against the rate that was set. Correlation "
            f"{b['corr_prem']:.2f}. <bookmark mark='b'/> Apply Binance's rule to the premium and the correlation rises to "
            f"{b['corr_rule']:.2f}: the flat stretch at a hundredth of a percent is the clamp, visible in the data."
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
        with self.voiceover(
            "Who pays, and why. <bookmark mark='a'/> Positive funding is the price of leverage: what leveraged longs pay "
            "for exposure they could not finance in spot, an interest rate set by crypto's own demand for leverage. "
            "<bookmark mark='b'/> It is also a gauge of sentiment, high in rallies and negative in crashes, and "
            "forced liquidations cluster at its extremes. <bookmark mark='c'/> And it is the running cost that Part two's margin "
            "account paid through the crash of March twenty twenty."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self, f):
        q = pause_card(rf"funding on ether's perpetual averaged about {f['ETHUSDT']['annual_pct']:.0f}\% a year. A desk "
                       r"buys ether and shorts the perpetual to collect it, with no exposure to ether's price. What could "
                       r"go wrong?")
        with self.voiceover(
            f"Pause and predict. Funding on ether's perpetual averaged about {f['ETHUSDT']['annual_pct']:.0f} percent a "
            "year. A desk buys ether and shorts the perpetual to collect it, with no exposure to ether's price. What "
            "could go wrong?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()


def D_rule(p):
    from explainer.quant.house import defi
    return defi.binance_funding_rule(p)
