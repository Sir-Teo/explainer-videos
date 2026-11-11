from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, GOOD, INFL, PART, USD, ask, fit_right, illustration, load


class Inflation(VoiceoverScene):
    def construct(self):
        i = load("inflation")
        self.card()
        self.tips()
        self.history(i)
        self.forecast(i)
        self.surge(i)
        self.decompose()
        self.swaps(i)

    def card(self):
        c = chapter_card(12, r"Inflation: breakevens and the premium", r"What inflation does the bond market expect?",
                         lit=(2008, 2022), part=PART)
        with self.voiceover("Chapter twelve. Inflation, as the bond market prices it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tips(self):
        rows = [cmath('\\text{TIPS coupon}', r"=", 'c_h\\,N\\,R_t\\quad\\text{(lagged reference index ratio)}', font_size=40,
                      colors={'\\text{TIPS coupon}': INFL}),
                cmath(r"y_{\text{nom}} - y_{\text{real}}", r"\approx", r"\underbrace{\mathbb{E}[\pi]}_{\text{expected}} + "
                      r"\underbrace{\text{IRP}}_{\text{risk premium}} - \underbrace{\text{LP}}_{\text{TIPS liquidity}}",
                      font_size=34, colors={r"y_{\text{nom}} - y_{\text{real}}": BASIS})]
        whys = [why('Treasury Inflation-Protected Securities, sold since 1997: Coupon rate per payment period times indexed principal; the reference CPI is lagged, and principal redemption has a deflation floor under TIPS terms'),
                why(r"the breakeven, nominal less real, is the inflation at which the two bonds pay the same: expected "
                    r"inflation, plus a premium for bearing inflation risk, less a discount for TIPS being harder to "
                    r"trade")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "TIPS pay coupons on indexed principal. The coupon rate per payment period multiplies face value and a lagged reference-index ratio; principal redemption also has a contractual deflation floor. Their quoted yield is a real yield under those conventions. <bookmark mark='a'/> Nominal yield less a comparable real yield gives a breakeven measure. The displayed decomposition into expected inflation, inflation risk premium and TIPS liquidity compensation is approximate. Coupon profiles, duration, index lag, convexity, tax and the floor can matter. An inflation path making two specific bond returns equal depends on those cash flows, so a yield difference is not an exact universal expectation of future CPI growth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def history(self, i):
        t5, b5 = np.asarray(i["t5"]), 100 * np.asarray(i["b5"])
        t55, f55 = np.asarray(i["t55"]), 100 * np.asarray(i["f55"])
        g = axes([2003, 2026], [-2.5, 4.0], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\% a year",
                 xticks=[2005, 2010, 2015, 2020, 2025], yticks=[-2, 0, 2, 4], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        two = DashedLine(ax.c2p(2003, 2), ax.c2p(2026, 2), color=GREY_B, stroke_width=1.2)
        l5 = curve(ax, t5, b5, INFL, stroke_width=2.4)
        l55 = curve(ax, t55, f55, USD, stroke_width=2.2)
        mn, mx = i["min"], i["max"]
        side = VGroup(
            legend([(INFL, r"5-year breakeven"), (USD, r"5-year, 5 years ahead")], font_size=17),
            MathTex(rf"{mn['date'] // 10000}\text{{-}}{mn['date'] // 100 % 100:02d}:\ {100 * mn['v']:.2f}\%", font_size=24,
                    color=BAD),
            MathTex(rf"{mx['date'] // 10000}\text{{-}}{mx['date'] // 100 % 100:02d}:\ {100 * mx['v']:.2f}\%", font_size=24,
                    color=INFL),
            wrapped_label(f"daily, FRED. The 5y5y forward averaged {100 * i['f55_mean']:.2f}\\%: a forward breakeven price, still containing risk and liquidity premia, not an isolated long-run expectation", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The saved public series covers 2003 through 2025. <bookmark mark='a'/> Its five-year breakeven reaches {100 * mn['v']:.1f} percent in November 2008. This price alone cannot separate expectations from risk and liquidity premia. Model-based research attributes a substantial part of the crisis decline to market liquidity, with uncertainty about the decomposition. <bookmark mark='b'/> The March 2022 maximum is {100 * mx['v']:.1f}. The five-year rate five years forward averages {100 * i['f55_mean']:.1f} percent over its saved sample. That forward measure emphasizes later horizons, yet it does not remove all current shocks or premia and should not be read as a pure forecast of the central bank's target."
        ) as vo:
            self.play(FadeIn(g), Create(two), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l5), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Create(l55), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"FRED: T5YIE, T5YIFR"))
        self.wait(0.4)
        self.clear_scene()

    def forecast(self, i):
        tm, b5m = np.asarray(i["tm"]), 100 * np.asarray(i["b5m"])
        rt, real = np.asarray(i["real_t"]), 100 * np.asarray(i["real"])
        g = axes([2003, 2021.2], [-2.5, 5.0], x_length=8.2, y_length=4.4, xlabel=r"the month the breakeven was observed",
                 ylabel=r"\% a year", xticks=[2005, 2010, 2015, 2020], yticks=[-2, 0, 2, 4], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        sel = tm <= rt[-1] + 1e-9
        lb = curve(ax, tm[sel], b5m[sel], INFL, stroke_width=2.4)
        lr = curve(ax, rt, real, BAD, stroke_width=2.6)
        side = VGroup(
            legend([(INFL, r"5-year breakeven, that month"), (BAD, r"CPI inflation over the next 5 years")], font_size=17),
            MathTex(rf"\text{{breakeven}} - \text{{realised}}:\ {100 * i['gap_mean']:+.2f}\pm{100 * i['gap_sd']:.2f}",
                    font_size=24, color=BASIS),
            wrapped_label('start months 2003--2020 (the last whose five years are complete). Overlapping five-year windows; current-vintage seasonally adjusted CPI proxy, without contract index lag. Mean gaps do not identify a liquidity premium or forecasting skill', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Compare the saved monthly mean breakeven with annualized CPI growth over the following five years. This is an ex-post descriptive comparison, using current-vintage seasonally adjusted CPI rather than a contract's lagged reference index. <bookmark mark='a'/> Adjacent observations overlap for almost their entire five-year windows. A single inflation episode therefore affects many points, and the observations are not independent forecast trials. <bookmark mark='b'/> The sample mean price-minus-realization gap is {100 * i['gap_mean']:+.1f} percentage points; its sample standard deviation is {100 * i['gap_sd']:.1f}, not a standard error or prediction interval. Expectations errors and several premia contribute. The gap alone does not identify a causal liquidity discount or certify forecasting performance."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), Create(lb), Create(lr), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(lr, scale_factor=1.01))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.add(illustration(r"FRED: T5YIE (monthly mean), CPIAUCSL"))
        self.wait(0.4)
        self.clear_scene()

    def surge(self, i):
        tc, yoy = np.asarray(i["cpi_t"]), 100 * np.asarray(i["cpi_yoy"])
        t5, b5 = np.asarray(i["t5"]), 100 * np.asarray(i["b5"])
        sel = tc >= 2019
        s5 = t5 >= 2019
        g = axes([2019, 2026], [-1, 10], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\% a year",
                 xticks=[2019, 2021, 2023, 2025], yticks=[0, 2, 4, 6, 8, 10], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        lc = curve(ax, tc[sel], yoy[sel], BAD, stroke_width=2.8)
        lb = curve(ax, t5[s5], b5[s5], INFL, stroke_width=2.4)
        side = VGroup(
            legend([(BAD, r"CPI, 12-month change"), (INFL, r"5-year breakeven")], font_size=17),
            MathTex(rf"\text{{CPI peak}}:\ {i['cpi_peak'] * 100:.1f}\%", font_size=26, color=BAD),
            MathTex(rf"\text{{breakeven peak}}:\ {100 * i['max']['v']:.2f}\%", font_size=26, color=INFL),
            wrapped_label('the bond market looked through the surge: it priced inflation coming back toward the target within five years, and the 5y5y forward barely moved. Different horizons and embedded premia prevent a direct forecast-skill or policy-credibility verdict', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The 2021 and 2022 inflation surge contrasts a one-year realization with a five-year market price. <bookmark mark='a'/> The saved twelve-month CPI change peaks near {i['cpi_peak'] * 100:.0f} percent. <bookmark mark='b'/> The five-year breakeven maximum is about {100 * i['max']['v']:.1f}. A multi-year compounded rate need not track a single year's peak. Longer-horizon prices can contain expectations of disinflation, but also changing risk, liquidity and convexity premia. These series alone neither prove that markets correctly forecast the full five-year path nor identify confidence in a central bank. Evaluating that claim would require matched horizons and a point-in-time forecasting design."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lc), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"FRED: CPIAUCSL, T5YIE"))
        self.wait(0.4)
        self.clear_scene()

    def decompose(self):
        cards = VGroup(
            desk_question(r"expected inflation", r"surveys of forecasters, and models of the term structure fitted to "
                          r"nominal and real yields together, estimate it separately", width=12.0, font_size=21),
            desk_question(r"the inflation risk premium", r"positive when inflation surprises hurt in bad times; Fed staff "
                          r"models (D'Amico, Kim and Wei, 2018) find it small and sometimes negative in the 2010s, when "
                          r"the risk was deflation", width=12.0, font_size=21),
            desk_question(r"the liquidity premium", r"TIPS trade less than nominal notes, and in a panic far less: the "
                          r"same models attribute most of 2008's collapse in breakevens to it", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Untangling the three needs a model, and the Federal Reserve's staff maintain several. "
            "<bookmark mark='a'/> Expected inflation they pin with surveys and with a term-structure model of the "
            "kind in Part nineteen, fitted to nominal and real yields at once. <bookmark mark='b'/> The inflation risk "
            "premium comes out small, and in the 2010s, when the worry was deflation, sometimes negative: nominal "
            "bonds were the hedge then. <bookmark mark='c'/> And the liquidity premium accounts for most of the 2008 "
            "collapse. The breakeven moves for reasons that have nothing to do with inflation."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def swaps(self, i):
        rows = [cmath(r"(1 + K)^T", r"=", r"\mathbb{E}^{\mathbb{Q}_T}\Big[\frac{\text{CPI}_T}{\text{CPI}_0}\Big]", font_size=40,
                      colors={r"(1 + K)^T": INFL}),
                cmath(r"K - \text{breakeven}", r"=", r"\text{the swap--TIPS basis}", font_size=36,
                      colors={r"K - \text{breakeven}": BASIS})]
        whys = [why(r"a zero-coupon inflation swap: at maturity one side pays the CPI's growth, the other a fixed rate "
                    r"$K$ compounded; the fair compounded gross fixed payment $(1+K)^T$ equals the expected index ratio under the $T$-forward measure; $K$ is the annual rate"),
                why('A swap needs no initial bond purchase but still uses credit, collateral, capital and funding. Swap--TIPS differences also reflect liquidity, index conventions, floors and curve construction')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A zero-coupon inflation swap exchanges cumulative index growth against a fixed compounded payment at maturity. Under consistent discounting, the fair compounded gross fixed payment equals the expected index ratio under the payment-date forward measure. Taking the annualized root gives the quoted fixed rate; it is not the expectation of the annualized growth rate. <bookmark mark='a'/> Swaps avoid purchasing the bond principal but still need counterparty exposure, collateral, capital and funding. Their difference from a TIPS breakeven can reflect liquidity, financing, index lag, the TIPS floor and cash-flow conventions. It need not have a universal sign or a single balance-sheet explanation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"a pension fund must pay benefits that rise with inflation. Should it hedge with TIPS or with inflation "
                r"swaps, and what does each cost it when breakevens fall in a panic?")
        with self.voiceover("A pension fund owes benefits that rise with inflation. Should it hedge with TIPS or with "
                            "inflation swaps, and what does each cost it when breakevens fall in a panic?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
