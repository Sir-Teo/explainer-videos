from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.series()
        self.reservoir()
        self.rs()
        self.joseph()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1951,)).to_edge(UP, buff=0.35)
        hc = history_card(1951, r"Harold Edwin Hurst, \ \emph{Long-Term Storage Capacity of Reservoirs}",
                          r"A British hydrologist who spent sixty years measuring the Nile for the Egyptian government. "
                          r"To size a dam that could carry Egypt through droughts, \ he needed the range of the river's "
                          r"cumulative surplus and deficit, \ and found that it grew faster than any textbook series allowed",
                          color=LMC, width=11.2, font_size=22).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"independent years: \ the range grows like $n^{1/2}$", font_size=24, color=GREY_A),
            label(r"the Nile, \ and hundreds of other records: \ like $n^{0.7}$ and more", font_size=24, color=LMC),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Harold Edwin Hurst went to Egypt in 1906 and spent most of the next sixty years "
            "measuring the Nile. His question was practical: how big must a reservoir be to carry Egypt through a run"
            " of dry years, releasing the average flow every year? The answer depends on the range of the river's "
            "cumulative surplus and deficit. <bookmark mark='b'/> For independent finite-variance yearly increments, "
            "the typical range grows like the square root of the number of years. <bookmark mark='c'/> In 1951 Hurst "
            "reported that for the Nile, and for hundreds of other records of rivers, rainfall, tree rings and lake "
            "sediments, it grew faster, like the number of years to a power of about seven tenths or more."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def series(self):
        d = load("hurst")
        yrs, m = np.asarray(d["years"], float), np.asarray(d["minima"], float)
        A = axes([620, 1290], [900, 1500], x_length=10.4, y_length=4.0, xlabel=r"year", ylabel=r"yearly minimum level",
                 xticks=[700, 800, 900, 1000, 1100, 1200], yticks=[1000, 1200, 1400], xfmt=lambda v: f"{v:.0f}", center=[0, 0.4, 0])
        ax = A.ax
        line = series_line(ax, yrs, m, LMC, 1.8)
        mean = DashedLine(ax.c2p(620, d["mean"]), ax.c2p(1290, d["mean"]), color=GREY_B, stroke_width=1.5)
        foot = label(r"long stretches above the mean, \ and long stretches below: \ compare with white-noise and fitted AR(1) references",
                     font_size=24, color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is one of his records, from the Roda gauge on an island in Cairo: the yearly minimum "
            "level of the Nile from 622 to 1284, compiled by Prince Omar Toussoun in 1925. Six hundred and sixty-three "
            "years. <bookmark mark='b'/> Look at the long excursions: decades above the average, then decades below, at "
            "every scale. A series of independent years, or one with the short memory of Part seventeen's "
            "autoregressions, wanders back to its mean much faster."
        ) as vo:
            self.add(minima_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(foot))
        self.clear_scene()

    def reservoir(self):
        d = load("hurst")
        yrs, z = np.asarray(d["years"], float), np.asarray(d["cumdev"], float)
        A = axes([620, 1290], [float(z.min()) - 500, float(z.max()) + 500], x_length=10.4, y_length=4.0, xlabel=r"year",
                 ylabel=r"cumulative surplus", xticks=[700, 900, 1100], yticks=[0], xfmt=lambda v: f"{v:.0f}",
                 center=[0, 0.4, 0])
        ax = A.ax
        line = series_line(ax, yrs, z, TAUC, 2.2)
        i, j = int(np.argmax(z)), int(np.argmin(z))
        rng_ = DoubleArrow(ax.c2p(1270, z.min()), ax.c2p(1270, z.max()), buff=0, color=MISSC, stroke_width=3, tip_length=0.15)
        foot = label(rf"the range $R$ = {d['range']:,.0f}: \ cumulative level anomaly, not reservoir volume", font_size=24,
                     color=MISSC).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here we illustrate Hurst's construction using minimum water levels, not flow "
            "volumes. Add up each year's departure from the long-run mean: a cumulative level anomaly. For a "
            "flow-volume record, the analogous curve describes idealized storage while releasing the mean flow. "
            "<bookmark mark='b'/> The range of that curve summarizes cumulative deviations; for flow volumes under "
            "idealized operation it measures storage the reservoir needs. Divide it by the standard deviation to make"
            " it comparable across rivers: the rescaled range, R over S."
        ) as vo:
            self.add(minima_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(rng_), FadeIn(foot))
        self.clear_scene()

    def rs(self):
        d = load("hurst")
        r = d["rs"]
        ls, lr = np.log10(np.asarray(r["sizes"], float)), np.log10(np.asarray(r["rs"], float))
        A = axes([0.8, 2.6], [0.3, 1.8], x_length=7.2, y_length=4.2, xlabel=r"block length $n$ (years, log scale)",
                 ylabel=r"$R/S$ (log scale)", xticks=[1, 1.5, 2, 2.5], yticks=[0.5, 1, 1.5], xfmt=lambda v: f"{10 ** v:.0f}",
                 yfmt=lambda v: f"{10 ** v:.0f}", center=[-1.8, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=LMC) for a, b in zip(ls, lr)])
        fit = Line(ax.c2p(0.8, d["H"] * 0.8 + r["c"] / np.log(10)), ax.c2p(2.6, d["H"] * 2.6 + r["c"] / np.log(10)), color=LMC, stroke_width=3)
        half = Line(ax.c2p(0.8, 0.5 * 0.8 + lr[0] - 0.5 * ls[0]), ax.c2p(2.6, 0.5 * 2.6 + lr[0] - 0.5 * ls[0]), color=GREY_B, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(rf"the Nile's minima: \ $H$ = {d['H']:.2f}", font_size=22, color=LMC),
            label(rf"white noise, \ same length: \ {d['H_iid_mean']:.2f} \ ({d['H_iid_q'][0]:.2f}--{d['H_iid_q'][1]:.2f})", font_size=22, color=GREY_A),
            label(rf"an AR(1) with $\phi$ = {d['phi']:.2f}: \ {d['H_ar_mean']:.2f} \ ({d['H_ar_q'][0]:.2f}--{d['H_ar_q'][1]:.2f})", font_size=22, color=Y0C),
            label(r"grey: \ slope $\frac12$", font_size=22, color=GREY_B),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Compute R over S in blocks of every length, and plot it against the block length on log "
            "scales. The slope is Hurst's exponent, H. <bookmark mark='b'/> For the Nile's minima it is " + say(d["H"], 2)
            + ". <bookmark mark='c'/> White noise of the same length gives about " + say(d["H_iid_mean"], 2) + ", a "
            "little above one half in samples this short. <bookmark mark='d'/> Even an autoregression fitted to the "
            "Nile, with the same correlation between neighbouring years, gives only about " + say(d["H_ar_mean"], 2)
            + ". These summaries suggest persistent dependence; they do not by themselves prove a fractional model."
        ) as vo:
            self.add(minima_tag())
            self.play(FadeIn(A), Create(half), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def joseph(self):
        rows = fit_rows(VGroup(
            label(r"Mandelbrot \& Wallis (1968): \ the Joseph effect", font_size=26, color=LMC),
            label(r"``seven years of great plenty \ldots \ and seven years of famine'' \ (Genesis 41)", font_size=26, color=GREY_A),
            label(r"persistence at every scale: \ long memory", font_size=26, color=TAUC),
            label(r"Hurst's storage work informed Nile dam planning, \ built in the 1960s", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Benoit Mandelbrot and James Wallis named it the Joseph effect in 1968, <bookmark "
            "mark='b'/> after Pharaoh's dream of seven years of great plenty followed by seven years of famine. <bookmark "
            "mark='c'/> Persistence at every scale is now called long memory, and it breaks the short-memory models of "
            "Part seventeen. <bookmark mark='d'/> Hurst's analysis fed into the planning of the Aswan High Dam, built in the "
            "1960s with storage for years of flow, not one."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"Part 17: \ stationary, \ short memory, \ constant variance, \ everything observed", font_size=26, color=GREY_A),
            label(r"what if the memory is long? \ \ \ what if the series wanders without a mean?", font_size=26, color=LMC),
            label(r"what if the variance moves? \ \ \ what if the thing we care about is hidden?", font_size=26, color=VOLC),
            label(r"spectra, \ unit roots, \ volatility, \ long memory, \ state space, \ VARs", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part seventeen's series were stationary, with short memory and constant variance, and "
            "everything was observed. <bookmark mark='b'/> This part asks what changes when the memory is long, or when a "
            "series wanders with no mean to return to. <bookmark mark='c'/> When the variance itself moves, as in financial "
            "markets. And when the thing we care about cannot be seen, only noisy measurements of it. <bookmark mark='d'/> "
            "The tools: spectra, unit-root tests, volatility models, long-memory models, the state space and the Kalman "
            "filter, and vector autoregressions."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 38", font_size=34, color=GREY_B), label(r"Time Series in Depth", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"spectra: \ the periodogram, \ Welch, \ multitaper; \ the sunspot cycle",
            r"unit roots and Dickey--Fuller; \ spurious regression and cointegration",
            r"volatility: \ ARCH and GARCH; \ long memory and ARFIMA",
            r"state space: \ the Kalman filter, \ smoother, \ EM; \ nonlinear filters; \ regimes",
            r"VARs and Granger causality; \ the block bootstrap; \ the forecasting frontier",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 17 and 22").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ts} (II); \ the Kalman ellipses; \ data: \ the Nile, \ sunspots, \ DAX").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-eight: time series in depth. <bookmark mark='b'/> We'll decompose series into "
            "frequencies and find the sunspot cycle; test for unit roots, and see why regressions of one wandering series on "
            "another lie; model volatility that clusters, and memory that lasts centuries; filter, smooth and learn hidden "
            "states with Kalman's filter and its nonlinear successors; ask which series help forecast which; bootstrap "
            "dependent data; and end at the forecasting frontier."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
