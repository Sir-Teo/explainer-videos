from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats17.common import *  # noqa: F403


class Stationarity(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.trio()
        self.sample_acf()
        self.mean_variance()
        self.intervals()
        self.board()

    def card(self):
        card = chapter_card(1, r"Stationarity and the ACF", r"What stays the same while the series moves?", part=PART)
        with self.voiceover("Chapter one. Stationarity and the autocorrelation function."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"E[X_t]", r"=", r"\mu\ \ \text{for every } t", font_size=32),
            cmath(r"\mathrm{Cov}(X_t, X_{t+h})", r"=", r"\gamma(h)\ \ \text{depends only on the lag } h", font_size=32),
            cmath(r"\rho(h)", r"=", r"\gamma(h)/\gamma(0)", font_size=32),
            cmath(r"\text{white noise}", r":", r"\mu = 0,\ \ \gamma(h) = 0 \text{ for } h \ne 0", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"no drift in level"), why(r"weak stationarity: \ finite second moments"),
                why(r"the autocorrelation function, \ the ACF"), why(r"the building block: \ shocks $e_t$")]
        intro = label('Stationarity keeps moments stable over time', font_size=36)
        with self.voiceover(
            "If every observation depends on the past, what can we estimate at all? We need something that doesn't change "
            "over time. <bookmark mark='a'/> First, the mean is the same at every time: no drift in the level. "
            "<bookmark mark='b'/> Second, the covariance between two observations depends only on how far apart they are, "
            "the lag h, not on when they occur. With finite second moments, a series with these properties is weakly stationary: it moves, "
            "but its statistical character doesn't age. <bookmark mark='c'/> For positive variance, dividing by it gives the "
            "autocorrelation function, rho of h: the correlation of the series with itself h steps back. "
            "<bookmark mark='d'/> The simplest stationary series is white noise: zero mean, and no correlation at any lag. "
            "It's the raw material, the random shocks, from which every other model in this part is built."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def trio(self):
        d = load("trio")
        t = np.arange(200)
        rows = VGroup()
        cors = VGroup()
        names = [(r"white noise", "wn", "acf_wn", GREY_A), (r"AR(1), \ $\phi = 0.8$", "ar", "acf_ar", SERIES),
                 (r"random walk", "rw", "acf_rw", RES)]
        for k, (nm, key, akey, col) in enumerate(names):
            y = 2.2 - 2.15 * k
            x = np.asarray(d[key])
            lo, hi = x.min(), x.max()
            A = axes([0, 200], [lo, hi], x_length=6.4, y_length=1.5, center=[-3.0, y, 0])
            ln = series_line(A.ax, t, x, col, 1.8)
            B = axes([0, 21], [-1, 1], x_length=4.0, y_length=1.5, center=[3.6, y, 0], yticks=[-1, 0, 1], font_size=16)
            cg = Correlogram(B.ax, d[akey], band=d["band"], theory=d["theory_ar"] if key == "ar" else None, color=col,
                             hot=S.CTRL if key == "ar" else None)
            lab = label(nm, font_size=20, color=col).next_to(A, LEFT, buff=0.15).rotate(0)
            if lab.get_left()[0] < -6.9:
                lab.next_to(A, UP, buff=0.05).align_to(A, LEFT)
            rows.add(VGroup(A, ln, lab))
            cors.add(VGroup(B, cg))
        hs = VGroup(label(r"the series", font_size=22, color=GREY_B).move_to([-3.0, 3.55, 0]),
                    label(r"its sample ACF, \ lags 1--20", font_size=22, color=GREY_B).move_to([3.6, 3.55, 0]))
        tag = simulated_tag(r"200 steps each", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Three series of two hundred steps, and beside each its sample autocorrelations at lags one to "
            "twenty. <bookmark mark='b'/> White noise: the series is pure jitter, and its autocorrelations stay inside the "
            "dashed bands, which mark what chance alone produces. <bookmark mark='c'/> An autoregression, each value point "
            "eight of the last plus a shock: the series wanders in slow swells, and its autocorrelations decay geometrically, "
            "point eight, point six four, point five one, close to the theoretical values marked by dots. "
            "<bookmark mark='d'/> A random walk: each value is the last plus a shock, the case phi equals one. It has no pull toward a fixed mean, its sample autocorrelations die away only slowly, and it isn't stationary at all: its "
            "variance grows with time."
        ) as vo:
            self.play(FadeIn(hs), FadeIn(tag))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k][0]), FadeIn(rows[k][2]), Create(rows[k][1]), FadeIn(cors[k][0]), run_time=1.4)
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cors[k][1].bars], lag_ratio=0.05),
                          FadeIn(cors[k][1].zero), FadeIn(cors[k][1].bands), FadeIn(cors[k][1].theory))
        self.clear_scene()

    def sample_acf(self):
        rows = [
            cmath(r"\hat\gamma(h)", r"=", r"\frac1n \sum_{t=1}^{n-h} (x_t - \bar x)(x_{t+h} - \bar x)", font_size=32),
            cmath(r"\hat\rho(h)", r"=", r"\hat\gamma(h)/\hat\gamma(0)", font_size=32),
            cmath(r"\text{IID noise}", r":", r"\hat\rho(h) \approx N(0, 1/n)", font_size=32),
            cmath(r"\text{bands}", r":", r"\pm 2/\sqrt n = \pm 0.14\ \ (n = 200)", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"divide by $n$, \ not $n - h$: \ a valid covariance"), why(r"the sample ACF"),
                why(r"Bartlett (1946)"), why(r"about 1 lag in 20 crosses them by chance")]
        with self.voiceover(
            "<bookmark mark='a'/> The sample autocovariance averages the products of deviations h steps apart, dividing by n "
            "rather than n minus h, which keeps the whole function a valid covariance. <bookmark mark='b'/> Divide by the "
            "sample variance for the sample autocorrelation. <bookmark mark='c'/> For IID noise with suitable moments, the standard Bartlett approximation says, from "
            "1946 that each sample autocorrelation is approximately normal with variance one over n. "
            "<bookmark mark='d'/> Hence the bands at plus or minus two over root n. With twenty lags, about one bar in twenty "
            "will cross them by chance alone, so these are pointwise, not simultaneous bands; one marginal crossing among many is weak evidence by itself."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mean_variance(self):
        d = load("meanci")
        rows = [
            cmath(r"\mathrm{Var}(\bar X)", r"=", r"\frac{\gamma(0)}{n}\Big[1 + 2\sum_{k=1}^{n-1}\big(1 - \tfrac kn\big)\rho(k)\Big]", font_size=30),
            cmath(r"\text{AR(1)}", r":", r"\approx \frac{\gamma(0)}{n}\cdot\frac{1 + \rho}{1 - \rho}", font_size=30),
            cmath(r"\rho = 0.7", r":", rf"\frac{{1 + \rho}}{{1 - \rho}} = {d['inflation']:.2f}", font_size=30),
            cmath(r"n_{\text{eff}}", r"=", rf"n\,\frac{{1 - \rho}}{{1 + \rho}} = {d['neff']:.1f}\ \ (n = 100)", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"Part 5: \ the variance of a sum, \ with all its covariances"), why(r"the geometric sum"),
                why(r"the variance is 5.7 times the iid formula"), why(r"100 observations, \ worth 17.6 independent ones")]
        intro = label('Covariances change the precision of a sample mean', font_size=36)
        with self.voiceover(
            "Here is the first casualty of dependence: the standard error of the mean. <bookmark mark='a'/> Part 5's variance "
            "of a sum includes every covariance. For a stationary series it's the iid formula, gamma nought over n, times a "
            "bracket containing all the autocorrelations. <bookmark mark='b'/> For an autoregression with coefficient rho, the "
            "bracket sums to about one plus rho over one minus rho. <bookmark mark='c'/> With rho equal to point seven, that's "
            "five point six seven: the mean's variance is nearly six times what the iid formula says, and its standard error "
            "nearly two and a half times. <bookmark mark='d'/> Put differently, a hundred observations carry the information "
            "of seventeen and a half independent ones: the effective sample size. Positive correlation means each new "
            "observation mostly repeats the last."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def intervals(self):
        d = load("meanci")
        x = np.asarray(d["x"])
        A = axes([0, 100], [-4, 4], x_length=6.6, y_length=2.2, xlabel=r"", ylabel=r"", center=[-1.3, 2.1, 0], yticks=[-3, 0, 3],
                 font_size=16)
        ln = series_line(A.ax, np.arange(100), x, SERIES, 2)
        mline = DashedLine(A.ax.c2p(0, d["mean"]), A.ax.c2p(100, d["mean"]), color=OBS, stroke_width=2)
        blocks = VGroup(*[Rectangle(width=A.ax.c2p(10, 0)[0] - A.ax.c2p(0, 0)[0], height=2.2, stroke_color=GREY_C, stroke_width=1.2,
                                    fill_opacity=0).move_to(A.ax.c2p(10 * k + 5, 0)) for k in range(10)])
        B = axes([-1.1, 0.55], [0, 4], x_length=6.6, y_length=2.4, xlabel=r"the mean", xticks=[-1, -0.5, 0], center=[-1.3, -1.3, 0])
        bx = B.ax
        truth = DashedLine(bx.c2p(0, 0), bx.c2p(0, 3.8), color=S.TRUTH, stroke_width=3)
        items = [(r"iid $t$", d["iid"], S.ALT), (r"Newey--West", d["nw"], OBS), (r"basic block bootstrap", d["block"], BOOT)]
        segs = VGroup()
        for k, (nm, (lo, hi), col) in enumerate(items):
            y = 3.0 - k
            segs.add(VGroup(Line(bx.c2p(lo, y), bx.c2p(hi, y), color=col, stroke_width=7),
                            label(nm, font_size=20, color=col).next_to(bx.c2p(-1.1, y), LEFT, buff=0.15)))
        rows = fit_rows(VGroup(
            label(r"one AR(1) series, \ $\rho = 0.7$, \ true mean 0", font_size=22),
            MathTex(rf"\text{{iid SE}} = {d['iid_se']:.3f}", font_size=26, color=S.ALT),
            MathTex(rf"\text{{Newey--West}} = {d['nw_se']:.3f}", font_size=26, color=OBS),
            MathTex(rf"\text{{block bootstrap}} = {d['block_se']:.3f}", font_size=26, color=BOOT),
            MathTex(rf"\text{{true SD of the mean}} = {d['exact_sd']:.3f}", font_size=26, color=S.TRUTH),
        ), 4.2, 0.36, [4.8, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One series of a hundred from such an autoregression, with true mean zero. Its sample mean is "
            "minus point two seven. <bookmark mark='b'/> The iid standard error is point one four five, and the t-interval "
            "only just reaches zero: it all but declares the mean negative. <bookmark mark='c'/> Whitney Newey and Kenneth West, in "
            "1987, estimated the bracket directly, adding up the first few sample autocovariances with weights that taper off: "
            "a heteroskedasticity and autocorrelation consistent, or HAC, standard error, here point two six. "
            "<bookmark mark='d'/> Or resample in blocks. Hans Künsch's moving-block bootstrap of 1989 glues together random "
            "blocks of ten consecutive observations, so within-block dependence survives: point three oh. The interval uses the basic bootstrap, as on the Board. "
            "<bookmark mark='e'/> The true standard deviation of the mean, which we can compute for this model, is point three "
            "three. Both corrections are nearer the truth, and both still fall short here. HAC and block-bootstrap consistency require short-memory regularity and tuning that grows suitably with sample size."
        ) as vo:
            self.play(FadeIn(A), Create(ln), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(mline), FadeIn(B), Create(truth))
            vo.wait_until("b")
            self.play(Create(segs[0][0]), FadeIn(segs[0][1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(segs[1][0]), FadeIn(segs[1][1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(blocks))
            self.play(Create(segs[2][0]), FadeIn(segs[2][1]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=17) if r.part == 17 and r.setting.startswith("AR(1)")]
        b = coverage_board(rows, lit_part=17, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board: ten thousand such series, each with a ninety-five percent interval for the mean. "
            "<bookmark mark='a'/> The iid t-interval covers fifty-eight percent: badly broken, as the inflation factor "
            "predicted. "
            "<bookmark mark='b'/> Newey–West covers eighty-one percent: much better, still broken, because with a hundred "
            "observations it can't see enough lags to estimate the whole bracket. "
            "<bookmark mark='c'/> The block bootstrap, eighty-four percent, broken for the same reason: blocks of ten cut "
            "the longer-range dependence. Dependence is expensive. The corrections help, but a hundred correlated "
            "observations simply don't contain much information about the mean."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(b.body[k]))
        self.wait(1.0)
        self.clear_scene()
