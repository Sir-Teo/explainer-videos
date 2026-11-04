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
        self.share(s)
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
        whys = [why(r"the sample correlation matrix of $N$ series that are in truth independent"),
                why(r"Marchenko and Pastur (1967): as $N, T \to \infty$ with $N/T \to q$, its eigenvalues fill this "
                    r"density, though every true eigenvalue is one"),
                why(rf"a year of daily data on the 49 industries: pure noise spreads the eigenvalues over a factor of "
                    rf"{hi / lo:.0f}")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Random matrix theory answers it. <bookmark mark='a'/> Take N series that are truly independent, T "
            "observations each, and form their sample correlation matrix. <bookmark mark='b'/> Vladimir Marchenko and "
            "Leonid Pastur proved in 1967 that its eigenvalues do not sit at one, where the truth is: they spread over a "
            "known interval with a known density, wider the larger N is relative to T. <bookmark mark='c'/> For "
            f"{N} series and a year of daily data, pure noise alone spreads the eigenvalues from about {lo:.1f} to about "
            f"{hi:.1f}."
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
        xm = 4.0
        bins = np.linspace(0, xm, 33)
        w = bins[1] - bins[0]
        h, _ = np.histogram(np.clip(lam, 0, xm - 1e-6), bins)
        hz, _ = np.histogram(np.clip(lz, 0, xm - 1e-6), bins)
        dens, densz = h / (len(lam) * w), hz / (len(lz) * w)
        ym = 1.6
        g = axes([0, xm], [0, ym], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of the correlation matrix",
                 ylabel=r"density", xticks=[0, 1, 2, 3, 4], yticks=[0, 0.8, 1.6], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
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
        top = Arrow(ax.c2p(3.6, 1.0), ax.c2p(3.95, 0.12), buff=0.05, color=EST_C, stroke_width=3)
        toplab = MathTex(rf"\lambda_1 = {lam[0]:.1f}", font_size=26, color=EST_C).next_to(ax.c2p(3.6, 1.0), UP, buff=0.1)
        leg = legend([(EST_C, rf"the 49 industries, daily, {year}"), (GREY_B, r"the same, each series shuffled in time"),
                      (RMT_C, r"Marchenko--Pastur")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{y['n_above']} eigenvalues above the edge $\lambda_+ = {b:.2f}$; the largest, "
                             rf"{lam[0]:.1f}, carries {100 * y['share1']:.0f}\% of the total", 3.4, 15, GREY_A
                             ).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"Now the industries, a year of daily returns from {year}. <bookmark mark='a'/> First, a control: shuffle "
            "each series in time, which destroys every correlation but keeps each industry's returns. Its eigenvalues "
            "fill the Marchenko-Pastur law almost exactly. <bookmark mark='b'/> The real eigenvalues mostly sit inside "
            f"the same band, which means they are indistinguishable from noise. Only {y['n_above']} escape above the "
            f"edge, and one of them is enormous: {lam[0]:.1f}, far off this axis, carrying {100 * y['share1']:.0f} "
            "percent of all the variance. That is the market: when it moves, every industry moves with it."
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
            desk_question(r"the market mode", r"the top eigenvector puts nearly equal weight on every industry: buying it "
                          r"is buying the market", width=12.4, font_size=19),
            desk_question(r"a few sectors", r"the next one or two eigenvalues above the edge are groups of industries that "
                          r"move together beyond the market", width=12.4, font_size=19),
            desk_question(r"the bulk", r"everything inside the band could be noise: an optimizer that trusts it is "
                          r"trading on randomness, and the smallest eigenvalues, the ones it leans on, are the most "
                          r"distorted", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So the spectrum has three parts. <bookmark mark='a'/> The market mode, whose eigenvector holds every "
            "industry in about equal measure. <bookmark mark='b'/> A few sector modes just above the edge. "
            "<bookmark mark='c'/> And the bulk, which could be noise. The optimizer inverts the matrix, so it leans on the "
            "smallest eigenvalues, and those are exactly the ones random matrix theory says are pushed down furthest by "
            "noise."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
            "The market mode is not constant. <bookmark mark='a'/> Year by year, the share of all variance carried by the "
            f"largest eigenvalue: it peaks at {sh[k08]:.0f} percent in {int(yrs[k08])}, and was "
            f"{100 * y19['share1']:.0f} percent in 2019. In a crisis, correlations rise together and diversification "
            "disappears exactly when it is wanted."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def clip(self):
        rows = [cmath(r"C", r"=", r"\textstyle\sum_k \lambda_k v_k v_k^\top", font_size=34, colors={r"C": EST_C}),
                cmath(r"\tilde\lambda_k", r"=", r"\begin{cases}\lambda_k & \lambda_k > \lambda_+\\ \bar\lambda_{\text{bulk}} & "
                      r"\text{otherwise}\end{cases}", font_size=30, colors={r"\tilde\lambda_k": RMT_C}),
                cmath(r"\tilde C", r"=", r"\textstyle\sum_k \tilde\lambda_k v_k v_k^\top,\ \text{rescaled to unit diagonal}",
                      font_size=30, colors={r"\tilde C": RMT_C})]
        whys = [why(r"the spectral decomposition of the sample correlation matrix"),
                why(r"clipping (Laloux, Cizeau, Bouchaud and Potters 1999): keep the eigenvalues above the noise edge, "
                    r"replace the rest by their average, so the trace is unchanged"),
                why(r"the cleaned matrix keeps the market and sector modes and treats the bulk as one undifferentiated "
                    r"noise level; Bun, Bouchaud and Potters (2017) survey better cleaners")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The first remedy follows directly. <bookmark mark='a'/> Decompose the correlation matrix into its "
            "eigenvalues and eigenvectors. <bookmark mark='b'/> Keep the eigenvalues above the noise edge, and replace "
            "every one inside the band by their average: Laurent Laloux, Pierre Cizeau, Jean-Philippe Bouchaud and Marc "
            "Potters, 1999. <bookmark mark='c'/> The cleaned matrix keeps the market and the sectors, and treats the "
            "rest as one level of noise. Better cleaners exist; the next chapter meets the best known."
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
