from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import ASSET, BAD, DEBT, EQUITY, PART, ask, fit_right, illustration, load

MONTHS = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']
FIRM_C = {"BA": QC.SPOT, "AAL": QC.LOSS, "NCLH": QC.IMPLIED}


class KMV(VoiceoverScene):
    def construct(self):
        k = load("kmv")
        self.card()
        self.method()
        self.paths(k)
        self.firm(k, "NCLH")
        self.spreads(k)
        self.edf()
        self.feedback()

    def card(self):
        c = chapter_card(3, r"Distance to default, from prices", r"Retrospective fits: timing and calibration matter", part=PART)
        with self.voiceover('Chapter three. Distance to default from prices: a retrospective monthly calibration example, with explicit limits on timing and probability interpretation.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"E_t", r"=", r"\text{price}_t \times \text{shares outstanding (latest 10-Q)}", font_size=34,
                      colors={r"E_t": EQUITY}),
                cmath(r"D_t", r"=", r"\text{current liabilities} + \tfrac12\,\text{long-term debt}", font_size=34,
                      colors={r"D_t": DEBT}),
                cmath(r"V_t,\ \sigma_V", r"\leftarrow", r"E_t = C(V_t;\ D_t, \sigma_V),\ \ \sigma_V = \text{sd}\big(\Delta\ln "
                      r"V\big)\sqrt{252}\ \ \text{(iterate)}", font_size=30, colors={r"V_t,\ \sigma_V": ASSET}),
                cmath(r"DD_t", r"=", r"\frac{\ln(V_t / D_t) + (\mu - \frac12\sigma_V^2)}{\sigma_V}", font_size=36,
                      colors={r"DD_t": BAD})]
        whys = [why(r"the market value of the shares, with reported shares; historical availability and filing order require an audit"),
                why(r"KMV-inspired default point (Crosbie and Bohn, 2003): "
                    r"a heuristic boundary; not a universal legal trigger"),
                why(r"guess the asset volatility, invert the call every day for $V_t$, re-estimate the volatility from "
                    r"the $V$ path, repeat until it settles (Vassalou and Xing, 2004): trailing year fitted at month-end, then backfilled within that month: retrospective"),
                why(r"the one-year distance to default: standard deviations of cushion")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.5, edge=6.9)
        with self.voiceover(
            "The original example uses Boeing, American Airlines and Norwegian Cruise Line. It combines share prices with reported shares and liabilities. <bookmark mark='a'/> Share counts and balance sheets come from company filings, but this reconstruction does not certify a complete historical-vintage or filing-order audit. <bookmark mark='b'/> Current liabilities plus half of long-term debt is a heuristic default point, not a universal legal trigger. <bookmark mark='c'/> Each month-end calibration iterates asset values and volatility over a trailing year, then assigns that fit to earlier observations in the same month. That introduces future information relative to those earlier days, so the plotted daily curves are retrospective fits, not live forecasts. <bookmark mark='d'/> Distance is a standardized asset cushion. The original drift estimate is floored at the interest rate, an additional ad hoc assumption. A normal-tail transformation is neither Moody's calibrated expected default frequency nor a verified empirical probability."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def paths(self, k):
        values = np.concatenate([np.asarray(k[t]["dtd"], float) for t in FIRM_C])
        low, high = float(np.floor(np.nanmin(values))-1), float(np.ceil(np.nanmax(values))+1)
        g = axes([2019, 2026], [low, high], x_length=8.6, y_length=4.4, xlabel=r"year", ylabel=r"distance to default",
                 xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=np.linspace(low, high, 5), font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(2019, 0), ax.c2p(2026, 0), color=BAD, stroke_width=1.5)
        covid = DashedLine(ax.c2p(2020 + 2 / 12, low), ax.c2p(2020 + 2 / 12, high), color=GREY_B, stroke_width=1.5)
        lines = VGroup()
        for tk, c_ in FIRM_C.items():
            t, d = np.asarray(k[tk]["t"]), np.asarray(k[tk]["dtd"], float)
            ok = np.isfinite(d) & (t >= 2019)
            lines.add(curve(ax, t[ok], d[ok], c_, stroke_width=2.4))
        side = VGroup(
            legend([(FIRM_C[t_], k[t_]["name"]) for t_ in FIRM_C], font_size=17),
            *[MathTex(rf"\text{{{k[t_]['name'].split()[0]}: }}\min DD = {k[t_]['worst']['dtd']:.2f}", font_size=24,
                      color=FIRM_C[t_]) for t_ in FIRM_C],
            wrapped_label("retrospective month-end calibration shown at daily dates; no certified live probability. Equity, liabilities and fitted volatility jointly affect the distance; this chart does not identify each driver's causal contribution", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        worst = {t_: k[t_]["worst"] for t_ in FIRM_C}
        w = worst["NCLH"]
        with self.voiceover(
            f"These are the original retrospective monthly fits, shown at daily observation dates from twenty nineteen through twenty twenty-five. <bookmark mark='a'/> The fitted cushions decline sharply around the pandemic. This combines price changes, reported balance-sheet inputs and the month-end calibration procedure. The chart alone cannot identify their separate causal effects. Norwegian's saved minimum distance is {w['dtd']:.2f}. <bookmark mark='b'/> A subsequent recovery in the fitted distance is a change in model output, not evidence that the earlier values were calibrated probabilities. Distance itself is not a probability or a prediction of certain failure. A prospective implementation would freeze a fit using only data already public, apply it going forward and verify both input availability and forecast calibration on independent outcomes."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(covid), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in side[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.add(illustration(r"Retrospective month-end fits; Yahoo closes and EDGAR reports; original drift floor and filing-order assumptions"))
        self.wait(0.4)
        self.clear_scene()

    def firm(self, k, tk):
        f = k[tk]
        t, E, D = np.asarray(f["t"]), np.asarray(f["E"]), np.asarray(f["DP"])
        high = float(np.ceil(max(np.nanmax(E), np.nanmax(D))/5)*5+5)
        g = axes([2018, 2026], [0, high], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$ billion",
                 xticks=[2018, 2020, 2022, 2024, 2026], yticks=np.linspace(0, high, 5), font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        le = curve(ax, t, E, EQUITY, stroke_width=2.4)
        ld = curve(ax, t, D, DEBT, stroke_width=3)
        w = f["worst"]
        side = VGroup(
            legend([(EQUITY, r"market value of equity"), (DEBT, r"default point")], font_size=17),
            MathTex(rf"\text{{worst day: }} E = \${w['E']:.1f}\text{{bn}},\ D = \${w['DP']:.1f}\text{{bn}}", font_size=24),
            MathTex(rf"N(-DD) = {100 * w['pd']:.1f}\%\ \text{{(normal-tail proxy)}}", font_size=26, color=BAD),
            wrapped_label('the default point is a reported-liability heuristic. Its changes and the equity inputs jointly affect the fitted cushion; this chart does not establish a financing cause', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"For Norwegian Cruise Line, the chart compares market equity and the heuristic default point, using the original reconstruction. <bookmark mark='a'/> Market value and reported liabilities move on different clocks. Their changes, and the fitted volatility, affect the distance. We do not infer a causal financing effect from this plot. <bookmark mark='b'/> On the saved minimum-distance date the normal-tail transformation is {100 * w['pd']:.1f} percent. It assumes a lognormal terminal asset distribution and the original floored drift estimate; it is not an empirically validated bankruptcy probability. Moody's expected default frequency additionally uses proprietary historical calibration, which is not reproduced here. A live study would also audit filing availability and freeze its monthly parameters before the days being forecast."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(le), Create(ld), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def spreads(self, k):
        high = max(500., float(np.ceil(max(np.nanmax(k[t]["spread_bp"]) for t in FIRM_C)/500)*500+500))
        g = axes([2019, 2026], [0, high], x_length=8.4, y_length=4.4, xlabel=r"year",
                 ylabel=r"Merton's one-year spread, bp", xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025],
                 yticks=np.linspace(0, high, 5), font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        peaks = {}
        for tk, c_ in FIRM_C.items():
            t, s_ = np.asarray(k[tk]["t"]), np.asarray(k[tk]["spread_bp"], float)
            ok = np.isfinite(s_) & (t >= 2019)
            lines.add(curve(ax, t[ok], s_[ok], c_, stroke_width=2.4))
            j = int(np.nanargmax(np.where(ok, s_, -1)))
            peaks[tk] = s_[j]
        side = VGroup(
            legend([(FIRM_C[t_], k[t_]["name"]) for t_ in FIRM_C], font_size=17),
            *[MathTex(rf"\text{{{k[t_]['name'].split()[0]}: peak }} {peaks[t_]:,.0f}\ \text{{bp}}".replace(",", "{,}"),
                      font_size=24, color=FIRM_C[t_]) for t_ in FIRM_C],
            wrapped_label('hypothetical one-year zero-coupon debt at the heuristic default point, priced from the retrospective fitted assets and volatility; these are model spreads, not observed CDS quotes or certified forecasts', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The same fitted asset values and volatility produce model prices for hypothetical one-year zero-coupon debt struck at each firm's heuristic default point. These are retrospective model spreads, not observed bond quotes. <bookmark mark='a'/> The saved peak spreads are {peaks['BA']:,.0f} basis points for Boeing, {peaks['AAL']:,.0f} for American and {peaks['NCLH']:,.0f} for Norwegian. <bookmark mark='b'/> In calmer periods this diffusion-only terminal-default model can produce very small short-horizon spreads. A continuously diffusing firm a fixed positive distance from the boundary has vanishing short-term default probability. That is a limitation of this specification, not every structural model. Jumps, early-default mechanisms, stochastic rates, liquidity and pricing risk premia change the question. The chart does not validate the model against matched traded bonds."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=3),
                      LaggedStart(*[FadeIn(r_) for r_ in side[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def edf(self):
        rows = [cmath(r"\text{EDF}", r"=", r"\text{historical default rate of firms at the same } DD", font_size=34,
                      colors={r"\text{EDF}": BAD}),
                cmath(r"\pi^{\text{naive}}", r"=", r"N\Big(-\frac{\ln\frac{E + F}{F} + (r_{t-1} - \frac12\sigma_V^2)T}"
                      r"{\sigma_V\sqrt T}\Big),\ \ \sigma_V \approx \frac{E}{E + F}\sigma_E + \frac{F}{E + F}(0.05 + "
                      r"0.25\sigma_E)", font_size=26, colors={r"\pi^{\text{naive}}": BAD})]
        whys = [why(r"KMV's expected default frequency: the distance to default is the ranking, an empirical table is "
                    r"the scale"),
                why('Bharath and Shumway (2008): their naive distance proxy predicts competitively in their study. This does not establish universal equivalence, or make numerical accuracy irrelevant')]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Two refinements matter in practice. Moody's KMV maps distance to an expected default frequency using historical event experience; our normal-tail proxy is not that proprietary empirical mapping. <bookmark mark='a'/> Bharath and Shumway's two thousand eight study found competitive prediction from a naive distance proxy without the full nonlinear solve. That is evidence about their sample and specification, not universal equivalence. Leverage, equity risk, event definitions and timing all matter; solver precision and out-of-sample validation remain separate requirements."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"two firms have the same leverage. One's shares are twice as volatile. Which has the larger distance to "
                r"default, and what if the volatile one is a bank?")
        with self.voiceover("Two firms have the same leverage, and one's shares are twice as volatile. Which is closer "
                            "to default? And what changes if the volatile one is a bank?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: specify asset risk and the boundary first', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Equal leverage and different equity volatility do not alone identify DD. Compare asset volatility, drift, horizon and boundary; bank liabilities need a different audit.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Equal leverage and different equity volatility are insufficient to calculate distance to default. Under a fixed solvent asset cushion, physical drift and horizon, greater asset volatility generally reduces this model distance. Equity volatility must first be mapped consistently into asset risk. A bank adds deposit, funding, guarantee and regulatory mechanisms that a generic corporate boundary can miss.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
