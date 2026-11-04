from __future__ import annotations

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
        self.edf()

    def card(self):
        c = chapter_card(3, r"Distance to default, from prices", r"How far is a company from default today?", part=PART)
        with self.voiceover("Chapter three. Distance to default: Merton's model, run on real companies every day."):
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
        whys = [why(r"the market value of the shares, with the share count as of the latest filing known that day"),
                why(r"KMV's default point (Crosbie and Bohn, 2003): firms tend to default when assets fall to about "
                    r"their short-term debt plus half the long-term"),
                why(r"guess the asset volatility, invert the call every day for $V_t$, re-estimate the volatility from "
                    r"the $V$ path, repeat until it settles (Vassalou and Xing, 2004): a trailing year, every month"),
                why(r"the one-year distance to default: standard deviations of cushion")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.2, buff=0.5, edge=6.9)
        with self.voiceover(
            "Moody's KMV built a business on that last line. Run it on three companies the pandemic hit hard: Boeing, "
            "American Airlines and Norwegian Cruise Line. <bookmark mark='a'/> Equity: each day's share price times the "
            "shares outstanding in the latest filing then public. <bookmark mark='b'/> The default point: current "
            "liabilities plus half the long-term debt, KMV's rule of thumb for where firms actually fail. "
            "<bookmark mark='c'/> Then the iteration: guess the assets' volatility, invert Merton every day for the "
            "assets, measure their volatility, and repeat until it settles, on a trailing year of prices. "
            "<bookmark mark='d'/> The result is a distance to default, every day."
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
        g = axes([2019, 2026], [-1, 12], x_length=8.6, y_length=4.4, xlabel=r"year", ylabel=r"distance to default",
                 xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025], yticks=[0, 3, 6, 9, 12], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(2019, 0), ax.c2p(2026, 0), color=BAD, stroke_width=1.5)
        covid = DashedLine(ax.c2p(2020 + 2 / 12, -1), ax.c2p(2020 + 2 / 12, 12), color=GREY_B, stroke_width=1.5)
        lines = VGroup()
        for tk, c_ in FIRM_C.items():
            t, d = np.asarray(k[tk]["t"]), np.asarray(k[tk]["dtd"], float)
            ok = np.isfinite(d) & (t >= 2019)
            lines.add(curve(ax, t[ok], np.clip(d[ok], -1, 12), c_, stroke_width=2.4))
        side = VGroup(
            legend([(FIRM_C[t_], k[t_]["name"]) for t_ in FIRM_C], font_size=17),
            *[MathTex(rf"\text{{{k[t_]['name'].split()[0]}: }}\min DD = {k[t_]['worst']['dtd']:.2f}", font_size=24,
                      color=FIRM_C[t_]) for t_ in FIRM_C],
            wrapped_label(r"each firm's worst day came in 2020; a cushion built over years went in weeks, and came "
                          r"back only as slowly as the equity and as fast as the debt was repaid", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        worst = {t_: k[t_]["worst"] for t_ in FIRM_C}
        w = worst["NCLH"]
        with self.voiceover(
            "Here they are, 2019 to 2025. Before the pandemic, each sat several standard deviations from its default "
            "point. <bookmark mark='a'/> In March 2020, with planes grounded and ships tied up, the distances "
            "collapsed within weeks. Norwegian's fell to "
            f"{w['dtd']:.1f}, on the {w['date'] % 100} of {MONTHS[w['date'] // 100 % 100]}. <bookmark mark='b'/> "
            "Then the slow climb back, as each raised new money and its shares recovered. None of the three "
            "defaulted; a distance to default is a probability, not a verdict."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(covid), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in side[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.add(illustration(r"Yahoo Finance closes; shares and liabilities from each company's XBRL filings on EDGAR"))
        self.wait(0.4)
        self.clear_scene()

    def firm(self, k, tk):
        f = k[tk]
        t, E, D = np.asarray(f["t"]), np.asarray(f["E"]), np.asarray(f["DP"])
        g = axes([2018, 2026], [0, 25], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$ billion",
                 xticks=[2018, 2020, 2022, 2024, 2026], yticks=[0, 5, 10, 15, 20, 25], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        le = curve(ax, t, np.clip(E, 0, 25), EQUITY, stroke_width=2.4)
        ld = curve(ax, t, np.clip(D, 0, 25), DEBT, stroke_width=3)
        w = f["worst"]
        side = VGroup(
            legend([(EQUITY, r"market value of equity"), (DEBT, r"default point")], font_size=17),
            MathTex(rf"\text{{worst day: }} E = \${w['E']:.1f}\text{{bn}},\ D = \${w['DP']:.1f}\text{{bn}}", font_size=24),
            MathTex(rf"N(-DD) = {100 * w['pd']:.1f}\%\ \text{{(Merton's PD)}}", font_size=26, color=BAD),
            wrapped_label(r"the default point rose as the company borrowed to survive: more debt and less equity "
                          r"push the distance down from both sides", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Look inside {f['name']}. <bookmark mark='a'/> The market value of its shares, against its default point. "
            "In 2020 the equity fell by most of its value while the debt rose, because the company borrowed to "
            "survive months with no revenue. <bookmark mark='b'/> On its worst day Merton's model put the chance of "
            f"ending the year below the default point at about {100 * w['pd']:.0f} percent. KMV would then map the "
            "distance through its database of actual defaults, because the normal tail understates how often firms "
            "at a given distance really fail."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(le), Create(ld), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
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
                why(r"Bharath and Shumway (2008): a 'naive' version with no solving at all ranks defaults about as "
                    r"well. The model's value is the functional form, not the iteration")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Two refinements matter in practice. Moody's KMV turns the distance into an expected default frequency by "
            "looking up how often firms at that distance actually defaulted. <bookmark mark='a'/> And in 2008 Sreedhar "
            "Bharath and Tyler Shumway showed that a naive version, with no solving at all, forecasts defaults about "
            "as well. What carries the information is the combination of leverage and volatility in Merton's formula, "
            "not the precision of the iteration."
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
