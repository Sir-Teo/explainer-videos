from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, ask, fit_right, illustration, load


class Defaults(VoiceoverScene):
    def construct(self):
        d = load("defaults")
        self.card()
        self.counts(d)
        self.sorts(load("sorts"))
        self.labels()

    def card(self):
        c = chapter_card(7, r"Seventeen years of bankruptcies", r"How often do public companies fail?", part=PART)
        with self.voiceover("Chapter seven. Seventeen years of bankruptcies, from the companies' own filings."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def counts(self, d):
        yrs, n, baa = np.asarray(d["years"]), np.asarray(d["count"]), np.asarray(d["baa"])
        g = axes([2008.4, 2025.6], [0, 260], x_length=8.4, y_length=4.4, xlabel=r"year",
                 ylabel=r"companies filing for bankruptcy", xticks=[2009, 2012, 2015, 2018, 2021, 2024],
                 yticks=[0, 50, 100, 150, 200, 250], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.62, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=BAD, fill_opacity=0.75).move_to(
            [ax.c2p(y, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for y, v in zip(yrs, n)])
        sp = curve(ax, yrs, baa * 50, RISKY, stroke_width=3).set_stroke(color=QC.IMPLIED)
        k = {int(y): int(v) for y, v in zip(yrs, n)}
        side = VGroup(
            legend([(BAD, r"8-K Item 1.03 filers"), (QC.IMPLIED, r"Baa spread (\%, $\times 50$)")], font_size=17),
            MathTex(rf"\rho(\text{{count}},\ \text{{spread}}) = {d['corr']:.2f}", font_size=28),
            MathTex(rf"\rho(\text{{next year's count}},\ \text{{spread}}) = "
                    rf"{np.corrcoef(baa[:-1], n[1:])[0, 1]:.2f}", font_size=24),
            wrapped_label(rf"{k[2009]} in 2009; {k[2016]} in the 2016 oil bust; {k[2020]} in 2020; {k[2022]} in 2022, "
                          rf"with money cheap; {k[2023]} and {k[2024]} in 2023--24 as rates rose. {d['total']} filings "
                          rf"by {d['firms']} companies in all", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Every company registered with the SEC must file a current report within four business days of entering "
            "bankruptcy, under Item 1.03. EDGAR's full-text search finds every one. <bookmark mark='a'/> Counted by "
            f"company and year: {k[2009]} in 2009, as the financial crisis worked through; {k[2016]} in 2016, when the "
            f"oil price collapsed; {k[2020]} in 2020; then only {k[2022]} in 2022, with money cheap, and "
            f"{k[2023]} and {k[2024]} as rates rose. <bookmark mark='b'/> The Baa spread moves with the count, a "
            f"correlation of {d['corr']:.2f}: the price of credit and its failures share a cycle. On yearly data the "
            f"spread moves with the failures more than it foretells them: with next year's count the correlation is "
            f"{np.corrcoef(baa[:-1], n[1:])[0, 1]:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08, run_time=3))
            vo.wait_until("b")
            self.play(Create(sp), FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"EDGAR full-text search, 8-K filings reporting Item 1.03 (Bankruptcy or Receivership); a "
                              r"company's first filing per episode; FRED BAA10Y"))
        self.wait(0.4)
        self.clear_scene()

    def sorts(self, s):
        panels = VGroup()
        spec = [("leverage", r"liabilities / assets, decile", BAD), ("profit", r"operating profit / assets, decile",
                                                                       QC.SPOT), ("altman", r"Altman's Z, decile", QC.IMPLIED)]
        for k, xl, col in spec:
            r_ = np.asarray(s[k]["rate"]) * 100
            g = axes([0.4, 10.6], [0, 4.6], x_length=3.7, y_length=3.0, xlabel=xl, ylabel=r"bankruptcy rate, \%",
                     xticks=[1, 5, 10], yticks=[0, 1, 2, 3, 4], font_size=12)
            ax = g.ax
            bars = VGroup(*[Rectangle(width=0.28, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                      fill_color=col, fill_opacity=0.8).move_to(
                [ax.c2p(i + 1, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for i, v in enumerate(r_)])
            panels.add(VGroup(g, bars))
        panels.arrange(RIGHT, buff=0.5).shift(DOWN * 0.3)
        head = label(rf"Bankruptcy rate by decile, fit years 2010--2016 (average {100 * s['base']:.2f}\%)", font_size=24
                     ).to_edge(UP, buff=0.5)
        lev, pro, alt = (np.asarray(s[k]["rate"]) * 100 for k in ("leverage", "profit", "altman"))
        foot = wrapped_label(rf"the most indebted tenth filed at {lev[-1]:.1f}\% a year; the least profitable tenth at "
                             rf"{pro[0]:.1f}\%; the lowest tenth of Z at {alt[0]:.1f}\%. Outside the extremes the deciles "
                             r"are noisy: with 0.8\% of firms failing a year, a decile holds a few dozen bankruptcies",
                             12.4, 18, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Before any model, look at the raw rates. Sort the fit years' firms into tenths by a single ratio, and "
            "count how often each tenth filed for bankruptcy the next year. <bookmark mark='a'/> By leverage, the "
            f"most indebted tenth filed at {lev[-1]:.1f} percent a year, five times the average. By operating profit, "
            f"the least profitable tenth at {pro[0]:.1f}. By Altman's Z, the lowest tenth at {alt[0]:.1f}. "
            "<bookmark mark='b'/> Between the extremes the pattern is ragged, because bankruptcies are rare: a tenth "
            "of the sample holds only a few dozen of them. That noise is what any model has to see through."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.3, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def labels(self):
        rows = [cmath(r"y_{i,t}", r"=", r"\mathbb{1}\{\text{Item 1.03 filed 3 to 15 months after fiscal year } t\}",
                      font_size=32, colors={r"y_{i,t}": BAD}),
                cmath(r"x_{i,t}", r"=", r"\text{the accounts of fiscal year } t \text{ (XBRL frames)} + \text{public float}",
                      font_size=32, colors={r"x_{i,t}": RISKY})]
        whys = [why(r"the label: a bankruptcy filing between three months (the time to file a 10-K) and fifteen "
                    r"months after the year's end; firm-years already in bankruptcy are dropped"),
                why(r"the features, all from EDGAR's frames API: one concept for every filer at once; market equity from "
                    r"the public float on the 10-K's cover page. No paid database")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Those filings are labels. Pair each company's accounts for a year with whether it filed for bankruptcy in "
            "the following year, allowing three months for the annual report to appear. <bookmark mark='a'/> The "
            "accounts come from the same place: EDGAR's XBRL frames, every filer's assets, liabilities, earnings and "
            "cash flow, one concept at a time, and the market value of the shares from the public float each company "
            "reports on its cover page. A default-prediction dataset, built entirely from public filings."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"why might a bankruptcy count from 8-K filings understate defaults, and overstate them?")
        with self.voiceover("Why might a count of bankruptcy filings understate defaults? And why might it overstate "
                            "them?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
