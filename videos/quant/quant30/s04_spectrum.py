from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house.ml import mp_density
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, RMT_C, TRUE_C, fit_right, load


class Spectrum(VoiceoverScene):
    def construct(self):
        s = load("spectrum")
        self.card()
        self.law(s)
        self.histogram(s, "2019")
        self.modes(s)
        self.vectors(s)
        self.share(s)
        self.crisis(s)
        self.clip()
        self.question()

    def card(self):
        c = chapter_card(3, r"Covariance in high dimension", r"How much of a 49 by 49 covariance matrix is noise?",
                         part=PART)
        n_par = 49 * 50 // 2
        with self.voiceover(f"Chapter three. A covariance matrix of forty-nine industries has {n_par:,} distinct "
                            "numbers, estimated from a few years of data. How much of it is noise?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def law(self, s):
        y = s["years"]["2019"]
        lo, hi = y["edge"]
        T, N = y["T"], y["N"]
        rows = [cmath(r"E", r"=", r"\tfrac1T X^\top X,\quad X \in \mathbb R^{T\times N},\ X_{ti} \sim N(0, 1)\ \text{i.i.d.}",
                      font_size=30, colors={r"E": RMT_C}),
                cmath(r"\rho(\lambda)", r"=", r"\frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi q\lambda},\quad "
                      r"\lambda_\pm = (1 \pm \sqrt q)^2,\ q = N/T", font_size=30, colors={r"\rho(\lambda)": RMT_C}),
                cmath(rf"q = \tfrac{{{N}}}{{{T}}}", r"\Rightarrow", rf"\lambda \in [{lo:.2f},\ {hi:.2f}]\ \text{{even when the truth is }} I",
                      font_size=30)]
        whys = [why(r"an uncentred sample covariance of independent unit-variance series; a null benchmark"),
                why(r"Marchenko and Pastur (1967): as $N, T \to \infty$ with $N/T \to q$, its eigenvalues fill this "
                    r"density, though every true eigenvalue is one"),
                why(rf"a year of daily data on the 49 industries: pure noise spreads the eigenvalues over a factor of "
                    rf"{hi / lo:.0f}")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""A random-matrix null benchmark. <bookmark mark='a'/> Form the displayed uncentred sample covariance from independent standard Gaussian entries. <bookmark mark='b'/> As dimensions and observations grow at fixed ratio q between zero and one, Marchenko and Pastur's eigenvalue density has the shown support. Sample correlations have related asymptotic behaviour; the finite edges are not exact confidence bounds. <bookmark mark='c'/> At {N} series and {T} observations, the benchmark endpoints are about {lo:.1f} and {hi:.1f}. Dependence, changing volatility and missing-data treatment can change this reference."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def histogram(self, s, year):
        y = s["years"][year]
        lam = np.asarray(y["lam"], float)
        lz = np.asarray(y["shuffled"], float)
        q = y["N"] / y["T"]
        a, b = y["edge"]
        xm = float(np.ceil(max(lam.max(), lz.max()) * 1.05))
        bins = np.linspace(0, xm, 33)
        w = bins[1] - bins[0]
        h, _ = np.histogram(lam, bins)
        hz, _ = np.histogram(lz, bins)
        dens, densz = h / (len(lam) * w), hz / (len(lz) * w)
        ym = 1.6
        g = axes([0, xm], [0, ym], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of the correlation matrix",
                 ylabel=r"density", xticks=[0, xm / 2, xm], yticks=[0, 0.8, 1.6], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax

        def bars(dd, col, op):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0] - 0.01,
                                      height=max(ax.c2p(0, min(v, ym))[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                      fill_color=col, fill_opacity=op).move_to(ax.c2p(x0 + w / 2, 0), aligned_edge=DOWN)
                            for x0, v in zip(bins[:-1], dd) if v > 0])
        br, bz = bars(dens, EST_C, 0.8), bars(densz, GREY_B, 0.5)
        xs = np.linspace(a + 1e-3, b - 1e-3, 200)
        mp = curve(ax, xs, np.minimum(mp_density(xs, q), ym), RMT_C, stroke_width=3)
        edge = DashedLine(ax.c2p(b, 0), ax.c2p(b, ym), color=HURDLE, stroke_width=2)
        top = Arrow(ax.c2p(lam[0], 1.0), ax.c2p(lam[0], 0.12), buff=0.05, color=EST_C, stroke_width=3)
        toplab = MathTex(rf"\lambda_1 = {lam[0]:.1f}", font_size=26, color=EST_C).next_to(ax.c2p(lam[0], 1.0), UP, buff=0.1)
        leg = legend([(EST_C, rf"the 49 industries, daily, {year}"), (GREY_B, r"the same, each series shuffled in time"),
                      (RMT_C, r"Marchenko--Pastur")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{y['n_above']} eigenvalues above the edge $\lambda_+ = {b:.2f}$; the largest, "
                             rf"{lam[0]:.1f}, carries {100 * y['share1']:.0f}\% of the total", 3.4, 15, GREY_A
                             ).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"""Daily industry correlations for {year}. <bookmark mark='a'/> Independently permuting each series keeps its marginal observations but disrupts contemporaneous and temporal dependence; this is one shuffled control, compared with a Gaussian asymptotic reference. <bookmark mark='b'/> All forty-nine eigenvalues are plotted at their actual coordinates, including the top value {lam[0]:.1f}. There are {y['n_above']} above the reference edge, and the largest contributes {100 * y['share1']:.0f} percent of standardised variance. Being inside the band does not prove that an economic mode is noise. The original daily reader zero-fills missing values."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bz], lag_ratio=0.03), Create(mp), Create(edge))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in br], lag_ratio=0.03), GrowArrow(top),
                      FadeIn(toplab), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def modes(self, s):
        cards = VGroup(
            desk_question(r"the market mode", r"the top eigenvector is a broad direction in standardised returns: it "
                          r"is not a cap-weighted market portfolio", width=12.4, font_size=19),
            desk_question(r"a few sectors", r"the next one or two eigenvalues above the edge are groups of industries that "
                          r"move together beyond the market", width=12.4, font_size=19),
            desk_question(r"the bulk", r"the band is a null reference, not a classification test: inversion can amplify "
                          r"errors in small eigenvalues; weak real structure can also lie in the bulk, which is "
                          r"not proof of pure noise", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Read this decomposition cautiously. <bookmark mark='a'/> The leading eigenvector is a broad common direction in standardised industry returns; it is not the capitalization-weighted market portfolio. <bookmark mark='b'/> Other large modes can reflect sector comovement, with loadings and signs determined by this sample. <bookmark mark='c'/> The bulk contains sampling noise and may contain real weak structure. Inversion magnifies small estimated eigenvalues, so an optimiser can become sensitive to errors there. The MP benchmark alone does not identify the correct economic rank."
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def vectors(self, s):
        y = s["years"]["2019"]
        v1 = np.sort(np.asarray(y["v1"], float))
        g = axes([-0.5, 48.5], [-0.05, 0.25], x_length=7.4, y_length=4.0, xlabel=r"the 49 industries, sorted",
                 ylabel=r"loading on the top eigenvector", xticks=[], yticks=[0, 0.1, 0.2], yfmt=lambda v: f"{v:.1f}",
                 font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for k, v in enumerate(v1):
            h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            r = Rectangle(width=0.09, height=max(h, 0.002), stroke_width=0, fill_color=EST_C, fill_opacity=0.85)
            r.move_to([ax.c2p(k, 0)[0], (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
            bars.add(r)
        eq = DashedLine(ax.c2p(-0.5, 1 / 7), ax.c2p(48.5, 1 / 7), color=GREY_B, stroke_width=1.5)
        side = VGroup(label(r"the second eigenvector sets", font_size=17, color=GREY_B),
                      label(", ".join(y["v2_low"]), font_size=17, color=TRUE_C),
                      label(r"against", font_size=17, color=GREY_B),
                      label(", ".join(y["v2_high"]), font_size=17, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15
                                                                                       ).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"""Look at the two leading directions in the 2019 sample. <bookmark mark='a'/> The leading loadings are broad and close to the equal-loading reference one seventh, in standardised-return coordinates. This is a common mode, not an investable market-cap portfolio. <bookmark mark='b'/> The second contrasts the industry groups labelled on screen; its sign is arbitrary. The remaining {49 - y['n_above']} values sit below the reference edge, which does not establish that all those directions lack economic signal."""
        ) as vo:
            self.play(FadeIn(g), Create(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def share(self, s):
        yrs = np.asarray(s["share_years"], float)
        sh = 100 * np.asarray(s["share"], float)
        g = axes([1970, 2021], [0, 100], x_length=9.0, y_length=4.2, xlabel=r"",
                 ylabel=r"the largest eigenvalue's share of the total, \%", xticks=[1970, 1990, 2010, 2020],
                 yticks=[0, 50, 100], xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 0.4 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, yrs, sh, EST_C, stroke_width=3)
        k08 = int(np.argmax(sh))
        tag = MathTex(rf"{int(yrs[k08])}:\ {sh[k08]:.0f}\%", font_size=24, color=BAD).next_to(ax.c2p(yrs[k08], sh[k08]),
                                                                                          UP, buff=0.12)
        y19 = s["years"]["2019"]
        with self.voiceover(
            f"""The leading share changes across sample years. <bookmark mark='a'/> It peaks at {sh[k08]:.0f} percent in {int(yrs[k08])} and is {100 * y19['share1']:.0f} percent in 2019. These are proportions of standardised variance, not capital weights or counts of independent bets. Stronger common movement can weaken diversification in some stress periods; it does not make every remaining variance contribution vanish."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def crisis(self, s):
        a, b = s["years"]["2019"], s["years"]["2008"]
        hx = [-3.2, 0.6, 3.6]
        head = VGroup(label(r"daily, one year", font_size=18, color=GREY_B), label(r"2019", font_size=20, color=GREY_B),
                      label(r"2008", font_size=20, color=BAD))
        rows = [(r"largest eigenvalue", f"{a['lam'][0]:.1f}", f"{b['lam'][0]:.1f}"),
                (r"its share of the total", rf"{100 * a['share1']:.0f}\%", rf"{100 * b['share1']:.0f}\%"),
                (r"second eigenvalue", f"{a['lam'][1]:.2f}", f"{b['lam'][1]:.2f}"),
                (r"eigenvalues above the edge", f"{a['n_above']}", f"{b['n_above']}")]
        tab = VGroup(head)
        for t, x, y in rows:
            tab.add(VGroup(label(t, font_size=19), MathTex(x, font_size=26), MathTex(y, font_size=26, color=BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        with self.voiceover(
            f"""Compare two particular sample years. <bookmark mark='a'/> In 2008 the top eigenvalue is {b['lam'][0]:.1f}, accounting for {100 * b['share1']:.0f} percent of standardised variance. This shows stronger common movement in that sample. It does not reduce the covariance to exactly one factor, prove a universal crisis law, or eliminate all diversification. A covariance fitted in another regime may understate a concentrated common exposure."""
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def clip(self):
        rows = [cmath(r"C", r"=", r"\textstyle\sum_k \lambda_k v_k v_k^\top", font_size=34, colors={r"C": EST_C}),
                cmath(r"\tilde\lambda_k", r"=", r"\begin{cases}\lambda_k & \lambda_k > \lambda_+\\ \bar\lambda_{\text{bulk}} & "
                      r"\text{otherwise}\end{cases}", font_size=30, colors={r"\tilde\lambda_k": RMT_C}),
                cmath(r"\tilde C", r"=", r"\textstyle\sum_k \tilde\lambda_k v_k v_k^\top,\ \text{rescaled to unit diagonal}",
                      font_size=30, colors={r"\tilde C": RMT_C})]
        whys = [why(r"the spectral decomposition of the sample correlation matrix"),
                why('clipping (Laloux, Cizeau, Bouchaud and Potters 1999): retain values above the null edge and average the rest; this preserves trace before diagonal renormalisation'),
                why('equalising the bulk is a modelling choice, not proof of pure noise or identified sector factors; Bun, Bouchaud and Potters (2017) survey alternative cleaners')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "One proposed regularizer is eigenvalue clipping. <bookmark mark='a'/> Decompose the sample correlation matrix. <bookmark mark='b'/> In the local rule, replace every eigenvalue below the MP upper edge by that group's average, retaining values above it. This is a modelling choice inspired by random-matrix cleaning, not a test that the bulk lacks signal. <bookmark mark='c'/> The trace is preserved at that averaging step; subsequent diagonal renormalisation restores unit variances and can change the final spectrum again. Benefits depend on the population, window and loss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with 49 industries and only 60 months of data, where is the Marchenko--Pastur upper edge? "
                       r"And the lower?")
        with self.voiceover(
            "Pause and predict. With forty-nine industries and only sixty months of data, where are the edges of the "
            "noise band?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
