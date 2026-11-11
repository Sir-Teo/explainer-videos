from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GAS, GOOD, OIL, PART, USD, ask, fit_right, illustration, load


class Gas(VoiceoverScene):
    def construct(self):
        g = load("gas_public_example")
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
            wrapped_label("Henry Hub spot, monthly, 2010--2025, each month against its year's average. Gas is burned for heat in winter and injected into storage from April to October: seasonal futures patterns vary by year; this normalized spot average is not an observed forward curve", 3.6, 17, GREY_A),
            MathTex(rf"\text{{January}} / \text{{April}} = {prof[0] / prof[3]:.2f}", font_size=26, color=GAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Gas moves through pipelines and specialized LNG shipping, and is stored in reservoirs, aquifers and caverns. Infrastructure and demand both have seasonal constraints. <bookmark mark='a'/> This chart is a normalized historical spot-price average: each month's price divided by its own year's mean. It is not a forward curve known at the beginning of that year, nor an executable seasonal return. <bookmark mark='b'/> Winter demand and storage cycles help explain seasonal futures patterns, which vary across years and locations. Heating, cooling, weather, production and transport disruptions can change the pattern. Seasonal spot averages provide context, rather than proving that every winter contract must be dearer than every summer contract."
        ) as vo:
            self.play(FadeIn(ax_), Create(base), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(Indicate(bars[0], scale_factor=1.03))
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
            "Amaranth's natural-gas positions were large calendar spreads extending well beyond the nearest contracts. The Senate investigation reported very large positions and the fund suffered losses of roughly six billion dollars in September 2006. <bookmark mark='a'/> The four plotted EIA nearest-contract series provide market context. They change delivery identity through time and do not reconstruct the fund's actual winter-versus-summer positions, prices, costs or liquidation. <bookmark mark='b'/> Concentration and market impact can make an exit much more expensive than a small quoted position suggests. The exact loss mechanism needs the book and transaction history; it cannot be inferred solely from a front-month decline or these four public curves."
        ) as vo:
            self.play(FadeIn(ax_), FadeIn(leg), FadeIn(cc))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(cc, scale_factor=1.01))
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
            wrapped_label('Reduced Russian supply, LNG and pipeline access, transport, contracts and operational constraints impeded convergence. Different regional benchmarks do not identify one bottleneck or a pure capacity shadow price', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"European and US gas prices diverged sharply during the energy crisis. <bookmark mark='a'/> Reduced Russian supply, demand, storage decisions and transport constraints all mattered. <bookmark mark='b'/> In the saved monthly series, the European peak is about {pk['v']:.0f} dollars per million British thermal units, compared with {g['hh_same']:.1f} at Henry Hub that month. They are different locations and benchmarks, rather than two immediately interchangeable delivered assets. Liquefaction, shipping, regasification, pipeline access, contracts and operational outages impede convergence. The gap illustrates the value of scarce intermediation capacity, without identifying a single binding bottleneck or assigning the entire spread to its shadow price."
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
                cmath('V_{\\mathrm{flex}}', r"=", '\\sum_h B(0,t_h)\\,\\mathbb E^{\\mathbb Q}[q_h(P_h^e-H P_h^g-c)^+]', font_size=36, colors={'V_{\\mathrm{flex}}': GAS})]
        whys = [why(r"a gas plant turns $H$ MMBtu of gas (the heat rate, about 7 for a modern plant) into one MWh of "
                    r"power: its margin is the spark spread"),
                why('it runs only when the spread covers its running cost $c$: an idealized flexible plant resembles discounted expected dispatch options; startup, ramp, outage, fuel, emissions and fixed costs are omitted')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Power storage exists, through batteries and other technologies, but capacity and costs constrain it. A gas plant converts a heat rate of fuel into a megawatt hour of power. <bookmark mark='a'/> For a fully flexible idealized plant, operating value resembles a sum of discounted expected positive dispatch margins under a chosen pricing model, with output quantity included. A real plant links hours through startup costs, ramp limits, outages and minimum run times; fuel delivery and emissions also matter. Fixed costs must be deducted. The option-strip analogy explains flexibility, but its simple sum is not a complete plant valuation and spot electricity is not freely storable or tradable."
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
            f"Here is a fixed Margrabe exchange-option example, using positive tradable-asset proxies with joint lognormal dynamics, constant volatilities and no running cost. It is not a calibrated electricity plant. <bookmark mark='a'/> With independent drivers its value is about {np.interp(0.0, rhos, by):.1f} dollars per megawatt hour; at correlation point six, {sp['value']:.1f}; at point nine five, {by[-1]:.1f}. Higher correlation reduces relative variance. Even at correlation one, unequal volatilities of forty-five and forty percent leave five percent relative volatility. Value reaches zero at the money only when relative volatility vanishes, with compatible carry. Perfect correlation alone is insufficient."
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
