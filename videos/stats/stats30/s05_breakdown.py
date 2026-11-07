from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Breakdown(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.implosion()
        self.picture()
        self.values()
        self.maxbias()
        self.hl_bound()
        self.limits()

    def card(self):
        card = chapter_card(4, r"Breakdown", r"How many bad points to ruin it?", lit=(1971,), part=PART)
        with self.voiceover("Chapter four. Breakdown."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\varepsilon^*_n(T, x)", r"=", r"\min\{\tfrac mn : \sup_{\text{replace } m} |T(y) - T(x)| = \infty\}", font_size=28),
            cmath(r"\text{mean}", r":", r"1/n \to 0", font_size=32),
            cmath(r"\text{median}", r":", r"\lfloor (n+1)/2 \rfloor / n \to \tfrac12", font_size=32),
            cmath(r"\tfrac12", r":", r"\text{the asymptotic upper bound for location-equivariant estimators}", font_size=30),
        ]
        rows[2][2].set_color(MEDC)
        whys = [why(r"Donoho \& Huber (1983): \ finite-sample"), why(r"one point suffices"), why(r"half the data must go bad"),
                why(r"beyond half, \ which half is the data?")]
        with self.voiceover(
            "<bookmark mark='a'/> Influence is local: one point, a small mass. Breakdown is global: the smallest "
            "fraction of the data that, replaced by arbitrary values, can carry the estimate arbitrarily far. Frank "
            "Hampel defined it in 1971, and David Donoho and Peter Huber gave this finite-sample form. <bookmark "
            "mark='b'/> The mean breaks down with a single point. <bookmark mark='c'/> The median survives until half"
            " the data are bad. <bookmark mark='d'/> And one half is the asymptotic upper breakdown bound for "
            "location-equivariant procedures: beyond it, nothing distinguishes the good half from the bad."
        ) as vo:
            intro=label('Replacement breakdown measures global adversarial sensitivity',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        d = load("breakdown")
        ms = np.asarray(d["ms"])
        A = axes([0, 40], [20, 60], x_length=7.4, y_length=4.4, xlabel=r"points replaced by 1,000 (of 64)",
                 ylabel=r"estimate", xticks=[0, 10, 20, 30, 40], yticks=[25, 35, 45, 55], center=[-2.0, 0.3, 0])
        ax = A.ax
        spec = (("mean", MEANC), ("trim10", TRIMC), ("trim20", TRIMC), ("hl", HLC), ("huber", HUBC), ("median", MEDC))
        cs = {k: clip_curve(ax, ms, np.asarray(d["est"][k]), c, 3, ymin=20, ymax=60) for k, c in spec}
        bd = d["bd"]
        rows = fit_rows(VGroup(
            label(r"Newcomb's clean data; \ the largest $m$ set to 1,000", font_size=22),
            label(r"mean: \ off the chart at $m = 1$", font_size=22, color=MEANC),
            label(rf"trimmed 10\%, \ 20\%: \ at $m$ = {round(bd['trim10'] * 64)}, \ {round(bd['trim20'] * 64)}", font_size=22, color=TRIMC),
            label(rf"Hodges--Lehmann: \ at {round(bd['hl'] * 64)} \ (29\%)", font_size=22, color=HLC),
            label(r"median, \ Huber: \ hold to 32", font_size=22, color=MEDC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On Newcomb's sixty-four clean measurements, replace the largest m by a thousand, one at a "
            "time. <bookmark mark='b'/> The mean leaves the chart at once. <bookmark mark='c'/> The ten and twenty percent "
            "trimmed means hold until their trimming is used up, at seven and thirteen bad points. <bookmark mark='d'/> "
            "Hodges–Lehmann holds to nineteen, twenty-nine percent. <bookmark mark='e'/> The median and Huber's estimate, "
            "with its MAD scale, hold until half the data are bad, though Huber's drifts upwards as the bad points "
            "accumulate: high breakdown limits the worst case, but bias still grows."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs["mean"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs["trim10"]), Create(cs["trim20"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cs["hl"]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(cs["median"]), Create(cs["huber"]), FadeIn(rows[4]))
        self.clear_scene()

    def values(self):
        d = load("breakdown")
        hdr = [r"\textbf{estimator}", r"\textbf{breakdown, \ asymptotic}", r"\textbf{here (of 64)}", r"\textbf{efficiency at the normal}"]
        eff = {"mean": "1.00", "trim10": "0.94", "trim20": "0.89", "hl": "0.955", "median": "0.64", "huber": "0.95"}
        spec = (("mean", r"mean", r"0"), ("trim10", r"10\% trimmed", r"0.10"), ("trim20", r"20\% trimmed", r"0.20"),
                ("hl", r"Hodges--Lehmann", r"0.293"), ("huber", r"Huber (MAD scale)", r"0.5"), ("median", r"median", r"0.5"))
        body = [[t, a, f"{round(d['bd'][k] * 64)}", eff[k]] for k, t, a in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.28, colors=[GREY_A, MEANC, TRIMC, TRIMC, HLC, HUBC, MEDC])
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"no free lunch for the mean; \ but Huber buys 95\% efficiency and 50\% breakdown", font_size=22),
            label(r"efficiency and breakdown are separate properties: \ both are needed", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.4, 0])
        intro = label('Breakdown and efficiency measure different properties', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        self.add(intro)
        with self.voiceover(
            "<bookmark mark='a'/> Breakdown and efficiency together. The mean: full efficiency, zero breakdown. Trimmed "
            "means: breakdown equal to the trimming, efficiency ninety-four and eighty-nine percent. Hodges–Lehmann: ninety-five "
            "point five percent efficient, twenty-nine percent breakdown. The median: half, but only sixty-four percent "
            "efficient. <bookmark mark='b'/> And Huber's estimate with a MAD scale gets both: ninety-five percent efficiency "
            "and fifty percent breakdown. The two properties are separate, and good estimators need both."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(tb[5]), FadeIn(foot[1]))
        self.clear_scene()

    def hl_bound(self):
        rows = [
            cmath(r"m \text{ bad points}", r":", r"\text{the Walsh averages with a bad point: } \approx n m - m^2/2", font_size=28),
            cmath(r"\text{break}", r":", r"\text{when half the } n^2/2 \text{ averages are bad}", font_size=30),
            cmath(r"2\varepsilon - \varepsilon^2", r"=", r"\tfrac12", font_size=34),
            cmath(r"\varepsilon^*", r"=", r"1 - 1/\sqrt 2 = 0.293", font_size=34),
        ]
        rows[3][2].set_color(HLC)
        whys = [why(r"a pair is clean only if both are"), why(r"the median of the Walsh averages goes"),
                why(r"clean share $(1 - \varepsilon)^2 = \frac12$"), why(r"Hodges--Lehmann's breakdown")]
        with self.voiceover(
            "<bookmark mark='a'/> Where twenty-nine percent comes from. A Walsh average is clean only if both of its "
            "points are. <bookmark mark='b'/> The estimate breaks when half of the Walsh averages are contaminated. "
            "<bookmark mark='c'/> With a share epsilon bad, the clean-pair share is the square of one minus epsilon. "
            "<bookmark mark='d'/> Setting that to a half gives one minus one over root two: twenty-nine point three "
            "percent."
        ) as vo:
            intro=label('A clean Walsh pair needs two uncontaminated observations',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"breakdown is a worst case: \ adversarial, \ arbitrary values", font_size=24, color=RES),
            label(r"maximal bias curves: \ how far, \ for each share $\varepsilon$ below breakdown", font_size=24, color=HUBC),
            label(r"in regression and many dimensions, \ 50\% is hard to reach: \ chapters seven and eight", font_size=24, color=BIWC),
            label(r"in high dimensions, \ with computation, \ Part 60", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Breakdown is a worst case: arbitrary values, chosen adversarially. <bookmark mark='b'/> "
            "Below it, maximal bias curves say how far an estimator can be pushed for each share of contamination. "
            "<bookmark mark='c'/> In regression and in many dimensions, fifty percent breakdown is much harder to achieve, the "
            "subject of chapters seven and eight. <bookmark mark='d'/> And achieving it with computation that scales to high "
            "dimensions is recent work, Part 60."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def maxbias(self):
        from scipy import optimize, stats as st
        from explainer.stats.kit import robust as RR
        eps = np.linspace(0.001, 0.45, 120)
        med = st.norm.ppf(1 / (2 * (1 - eps)))

        def hub(e, k=1.345):
            f = lambda b: (1 - e) * _epsi(b, k) + e * k
            return optimize.brentq(f, 0, 30)

        def _epsi(b, k):
            # E psi_k(Z - b) for Z ~ N(0, 1)
            a1, a2 = -k + b, k + b
            mid = -(st.norm.pdf(a2) - st.norm.pdf(a1)) - b * (st.norm.cdf(a2) - st.norm.cdf(a1))
            return mid + k * st.norm.sf(a2) - k * st.norm.cdf(a1)

        hb = np.array([hub(e) for e in eps])
        A = axes([0, 0.5], [0, 3.0], x_length=7.4, y_length=4.4, xlabel=r"share of contamination $\varepsilon$",
                 ylabel=r"maximal bias (in $\sigma$)", xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 1, 2, 3],
                 xfmt=lambda v: f"{v:g}", center=[-2.0, 0.3, 0])
        ax = A.ax
        cm = clip_curve(ax, eps, med, MEDC, 3.5, ymin=0, ymax=3)
        ch = clip_curve(ax, eps, hb, HUBC, 3.5, ymin=0, ymax=3)
        mean_v = DashedLine(ax.c2p(0.003, 0), ax.c2p(0.003, 3), color=MEANC, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"the worst shift a share $\varepsilon$ of contamination can cause", font_size=22),
            label(r"red: \ the mean: \ infinite for any $\varepsilon > 0$", font_size=22, color=MEANC),
            label(rf"green: \ the median, \ $\Phi^{{-1}}\bigl(\frac{{1}}{{2(1 - \varepsilon)}}\bigr)$: \ {med[np.searchsorted(eps, 0.1)]:.2f} at 10\%", font_size=22, color=MEDC),
            label(rf"gold: \ known-scale Huber, \ $k = 1.345$: \ {hb[np.searchsorted(eps, 0.1)]:.2f} at 10\%", font_size=22, color=HUBC),
            label(r"the median minimizes the maximal bias \ (Huber 1964)", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Below breakdown, how far can contamination push an estimate? The maximal bias curve"
            " plots the worst shift for each share epsilon, the contaminant placed adversarially, here at plus "
            "infinity. <bookmark mark='b'/> For the mean it is infinite for any epsilon at all. <bookmark mark='c'/> "
            "For the median it is the normal quantile at one over two times one minus epsilon: point one four "
            "standard deviations at ten percent, rising to infinity at a half. <bookmark mark='d'/> Huber's estimate "
            "is pushed a little further, point one nine at ten percent, the price of its efficiency. <bookmark "
            "mark='e'/> Within the stated normal-location contamination framework and equivariant class, the median "
            "minimizes maximal bias. This plot holds the scale known; it is not the maximal-bias curve of our "
            "MAD-scaled sample Huber algorithm."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mean_v), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ch), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def implosion(self):
        rows = [
            cmath(r"\text{explosion}", r":", r"\hat\sigma \to \infty", font_size=32),
            cmath(r"\text{implosion}", r":", r"\hat\sigma \to 0", font_size=32),
            cmath(r"\text{MAD}", r":", r"\text{may implode when a majority coincide}", font_size=30),
            cmath(r"\text{for scale}", r":", r"\text{breakdown counts both directions}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"outliers inflate a scale"), why(r"inliers can collapse it"), why(r"rounded data: \ a real risk"),
                why(r"Rousseeuw \& Croux (1993)")]
        with self.voiceover(
            "<bookmark mark='a'/> For scale estimates, breakdown has two directions. Outliers can blow a scale up: "
            "explosion. <bookmark mark='b'/> Or contamination can collapse it to zero: implosion. <bookmark "
            "mark='c'/> The MAD can implode when a majority of observations coincide, with exact finite-sample "
            "thresholds depending on the median convention, which heavily rounded data can produce, and then every "
            "other point looks infinitely far away. <bookmark mark='d'/> A scale's breakdown point is the smaller of "
            "the two, and Qn's design guards against both."
        ) as vo:
            intro=label('A scale can fail by growing without bound or by collapsing to zero',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
