from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GAS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class Gas(VoiceoverScene):
    def construct(self):
        g = load("gas")
        self.card()
        self.season(g)
        self.amaranth(g)
        self.europe(g)
        self.spark()
        self.option(g)

    def card(self):
        c = chapter_card(9, r"Gas and power", r"What is a power plant worth?", lit=(2006, 2022), part=PART)
        with self.voiceover("Chapter nine. Natural gas and power: commodities with seasons, spikes, and the most famous "
                            "spread trade that ever failed."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def season(self, g):
        prof = np.asarray(g["profile"])
        months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        ax_ = axes([-0.6, 11.6], [0.85, 1.1], x_length=7.4, y_length=4.0, xlabel=r"month",
                   ylabel=r"price relative to the year's mean", xticks=[], yticks=[0.9, 1.0, 1.1], font_size=14
                   ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = ax_.ax
        base = DashedLine(ax.c2p(-0.6, 1.0), ax.c2p(11.6, 1.0), color=GREY_B, stroke_width=1.2)
        bars = VGroup()
        for i, (m, v) in enumerate(zip(months, prof)):
            y0, y1 = ax.c2p(0, 1.0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.45, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                                      fill_color=GAS if v >= 1 else USD, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), label(m, font_size=15).next_to(ax.c2p(i, 0.85), DOWN, buff=0.08)))
        side = VGroup(
            wrapped_label(r"Henry Hub spot, monthly, 2010--2025, each month against its year's average. Gas is burned "
                          r"for heat in winter and injected into storage from April to October: the curve of futures "
                          r"carries the same hump, every year", 3.6, 17, GREY_A),
            MathTex(rf"\text{{January}} / \text{{April}} = {prof[0] / prof[3]:.2f}", font_size=26, color=GAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Oil can be stored and shipped anywhere. Gas is harder: it moves by pipeline or, chilled to a liquid, by "
            "special ships, and it is stored in a few underground caverns. And demand has seasons. "
            "<bookmark mark='a'/> Henry Hub's spot price month by month, against each year's average: highest in "
            "winter, when gas is burned for heat, lowest in spring, when storage refills. "
            "<bookmark mark='b'/> The futures curve carries the same hump every year. Winter gas trades above summer "
            "gas, and the spread between them is a bet on the weather and on storage."
        ) as vo:
            self.play(FadeIn(ax_), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.add(illustration(r"FRED: MHHNGSP"))
        self.wait(0.4)
        self.clear_scene()

    def amaranth(self, g):
        a = g["amaranth"]
        t, P = np.asarray(a["t"]), np.asarray(a["P"])
        ax_ = axes([2006.58, 2006.84], [3.5, 11.5], x_length=6.4, y_length=4.2, xlabel=r"2006",
                   ylabel=r"\$ per MMBtu", xticks=[], yticks=[4, 6, 8, 10], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = ax_.ax
        cols = [BAD, GAS, OIL, USD]
        lines = VGroup(*[curve(ax, t, P[:, i], c_, stroke_width=2.6) for i, c_ in enumerate(cols)])
        cc = crisis_card(r"September 2006", r"Amaranth Advisors",
                         r"a multi-strategy hedge fund whose natural gas book held enormous calendar spreads, long winter "
                         r"against summer, on NYMEX and ICE; the US Senate's investigators found it held as many as "
                         r"100,000 contracts in a single month. As the spreads collapsed it lost about two thirds of its "
                         r"\$9.2 billion in about a week",
                         stats=[(r"\approx \$6\,\text{bn}", r"lost, mostly on gas, September 2006")], width=5.2,
                         font_size=16).to_edge(RIGHT, buff=0.3)
        leg = legend([(c_, rf"contract {i + 1}") for i, c_ in enumerate(cols)], font_size=15).next_to(ax_, UP, buff=0.1)
        with self.voiceover(
            "In 2006 the natural gas desk of Amaranth Advisors, a nine-billion-dollar hedge fund, led by one trader, built a position in gas "
            "spreads so large that the Senate's investigators later found it held as many as a hundred thousand "
            "contracts in a single month: long winter gas, short summer gas, years ahead. <bookmark mark='a'/> In "
            "September the market went the other way. Mild weather and full storage pushed the front contract from "
            "over seven dollars to near four, and the winter premium the fund was long shrank as it tried to sell. "
            "<bookmark mark='b'/> It lost about two thirds of its assets, some six billion dollars, in about a week. A "
            "position too big for its market has no exit price; the price is whatever the others will pay to take it."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(cc))
        self.add(illustration(r"EIA RNGC1--4; US Senate PSI, Excessive Speculation in the Natural Gas Market (2007)"))
        self.wait(0.4)
        self.clear_scene()

    def europe(self, g):
        te, ev = np.asarray(g["eu_t"]), np.asarray(g["eu"])
        th, hv = np.asarray(g["hh_t"]), np.asarray(g["hh"])
        sel_e, sel_h = te >= 2015, th >= 2015
        ax_ = axes([2015, 2026], [0, 75], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$ per MMBtu, monthly",
                   xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[0, 25, 50, 75], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = ax_.ax
        le = curve(ax, te[sel_e], ev[sel_e], BAD, stroke_width=2.6)
        lh = curve(ax, th[sel_h], hv[sel_h], GAS, stroke_width=2.6)
        pk = g["eu_peak"]
        side = VGroup(
            legend([(BAD, r"Europe (IMF, natural gas, EU)"), (GAS, r"United States (Henry Hub)")], font_size=17),
            MathTex(rf"\text{{August 2022}}:\ \${pk['v']:.0f}\ \text{{against}}\ \${g['hh_same']:.1f}", font_size=26,
                    color=BAD),
            wrapped_label(r"Russian pipeline supplies were cut through 2022; Europe bid for cargoes of liquefied gas. "
                          r"America's gas could not follow the price: export terminals were full, and the gap between "
                          r"the two prices was capped by liquefaction capacity, not by arbitrage", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Then Europe's crisis. <bookmark mark='a'/> Through 2021 and 2022 Russia cut the gas it piped to Europe, "
            "and Europe bid for every cargo of liquefied gas on the sea. <bookmark mark='b'/> In August 2022 European "
            f"gas averaged about {pk['v']:.0f} dollars per million British thermal units; American gas, "
            f"{g['hh_same']:.0f}. The same molecule, eight times the price. It could not be arbitraged, because "
            "America's export terminals were already running full. As with covered interest parity, a price gap "
            "stayed open because the arbitrage needed something scarce: there, balance sheet; here, the capacity to "
            "freeze gas and ship it."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lh), Create(le), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.add(illustration(r"FRED: PNGASEUUSDM (IMF), MHHNGSP"))
        self.wait(0.4)
        self.clear_scene()

    def spark(self):
        rows = [cmath(r"\text{spark spread}", r"=", r"P_{\text{power}} - H \times P_{\text{gas}}", font_size=40,
                      colors={r"\text{spark spread}": GOOD}),
                cmath(r"\text{plant}", r"=", r"\textstyle\sum_{\text{hours}} \max\big(P_{\text{power}} - H P_{\text{gas}} - "
                      r"c,\ 0\big)", font_size=36, colors={r"\text{plant}": GAS})]
        whys = [why(r"a gas plant turns $H$ MMBtu of gas (the heat rate, about 7 for a modern plant) into one MWh of "
                    r"power: its margin is the spark spread"),
                why(r"it runs only when the spread covers its running cost $c$: a power plant is a strip of options, one "
                    r"for every hour, to exchange gas for power")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Power is the strangest commodity of all: it cannot be stored, so its price can spike a hundredfold in an "
            "hour. A gas-fired plant turns a fixed quantity of gas, the heat rate, into a megawatt hour of power; its "
            "margin is the spark spread. <bookmark mark='a'/> And it runs only when that spread covers its costs. So "
            "a power plant is a strip of options, one for every hour of its life, to exchange gas for power. That is "
            "how traders value it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def option(self, g):
        sp = g["spark"]
        rhos, by = np.asarray(sp["rhos"]), np.asarray(sp["by_rho"])
        ax_ = axes([-0.6, 1.0], [0, 10], x_length=7.0, y_length=4.2, xlabel=r"correlation of power and gas",
                   ylabel=r"option value, \$ per MWh", xticks=[-0.5, 0, 0.5, 1.0], yticks=[0, 2, 4, 6, 8, 10],
                   font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = ax_.ax
        line = curve(ax, rhos, by, GAS, stroke_width=3.5)
        k = int(np.argmin(np.abs(rhos - 0.6)))
        dot = Dot(ax.c2p(rhos[k], by[k]), color=GOOD)
        side = VGroup(
            MathTex(rf"P_{{\text{{power}}}} = \${sp['power']:.0f},\ H P_{{\text{{gas}}}} = {sp['hr']:.0f}\times"
                    rf"\${sp['gas']:.0f}", font_size=24),
            MathTex(rf"\rho = 0.6:\ \${sp['value']:.2f}\ \text{{per MWh}}", font_size=26, color=GOOD),
            wrapped_label(r"Margrabe's exchange option (Part 15), six months, power volatility 45\%, gas 40\%, at the "
                          r"money; illustrative. The more power and gas move together, the less the option to swap one "
                          r"for the other is worth", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Value one hour's option with Margrabe's formula from Part fifteen: the right to exchange gas for power, "
            "at the money, six months out. <bookmark mark='a'/> Its value depends above all on how power and gas "
            f"move together. If they are independent, the option is worth about {np.interp(0.0, rhos, by):.0f} dollars a "
            f"megawatt hour; at a correlation of point six, about {sp['value']:.1f}; at point nine five, "
            f"{by[-1]:.1f}; in lockstep, nothing. A plant owner is long volatility of the spread, and short its correlation."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dot), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.add(illustration(r"the House's exotics.margrabe"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a gas plant's owner sells forward all its power and buys all its gas a year ahead. What risk has it "
                r"hedged, and what option has it given away?")
        with self.voiceover("A plant's owner sells all its power and buys all its gas a year ahead. What risk has it "
                            "hedged, and what option has it given away?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
