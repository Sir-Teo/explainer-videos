from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class SpaceTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.separable()
        self.shapes()
        self.gneiting_row()
        self.world_acf()
        self.world_space()
        self.practice()

    def card(self):
        card = chapter_card(12, r"Space and time", r"Fields that change", lit=(2002,), part=PART)
        with self.voiceover("Chapter twelve. Space and time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def separable(self):
        rows = [
            cmath(r"C(h, u)", r"=", r"\text{Cov}\big(Z(s, t), Z(s + h, t + u)\big)", font_size=32),
            cmath(r"\text{separable}", r":", r"C(h, u) = C_S(h)\, C_T(u)", font_size=32),
            cmath(r"\text{so}", r":", r"K = K_T \otimes K_S: \ \text{Kronecker, \ cheap to invert}", font_size=30),
            cmath(r"\text{but}", r":", r"\text{the spatial shape is the same at every time lag}", font_size=30),
        ]
        rows[1][-1].set_color(FIELDC)
        whys = [why(r"a space--time covariance"), why(r"the easy choice"), why(r"Part 4's Kronecker product"),
                why(r"no interaction")]
        with self.voiceover(
            "<bookmark mark='a'/> When the field changes in time, the covariance depends on a spatial lag h and a time "
            "lag u. <bookmark mark='b'/> The easy choice is separable: a spatial covariance times a temporal one. "
            "<bookmark mark='c'/> On a full grid of sites and times the covariance matrix is then a Kronecker product, "
            "which is cheap to factor. <bookmark mark='d'/> But separability says the spatial pattern of correlation "
            "is the same at every time lag, only scaled down, which is physically odd: weather systems move, and what "
            "happens here today happens further away tomorrow."
        ) as vo:
            intro=label('Separable covariance fixes the spatial shape across time lags',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _panel(self, M, h, center, title, color):
        A = axes([0, 3], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"spatial lag $h$", ylabel=r"$C(h, u)/C(0, u)$",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=center)
        ax = A.ax
        cols = [FIELDC, TAUC, PTC]
        cs = VGroup(*[polyline(ax, h, M[i] / M[i][0], c, 3) for i, c in zip((0, 20, 40), cols)])
        t = label(title, font_size=24, color=color).next_to(A, UP, buff=0.15)
        return A, cs, t

    def shapes(self):
        d = load("spacetime")
        h = np.asarray(d["h"], float)
        sep, non = np.asarray(d["sep"], float), np.asarray(d["nonsep"], float)
        A1, c1, t1 = self._panel(sep, h, [-3.4, -0.2, 0], r"separable \ ($\beta = 0$)", FIELDC)
        A2, c2, t2 = self._panel(non, h, [3.4, -0.2, 0], r"Gneiting, \ $\beta = 1$", BANDC)
        key = label(r"time lag \ $u = 0$ \ (blue), \ $1$ \ (gold), \ $2$ \ (red)", font_size=22, color=GREY_A).move_to([0, -3.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The spatial shape at three time lags, normalized by the covariance at zero spatial "
            "lag for each time lag. This compares shapes rather than absolute cross-time correlations. <bookmark "
            "mark='b'/> Under separability the three curves are one curve: the spatial shape never changes. <bookmark"
            " mark='c'/> Under Tilmann Gneiting's non-separable family, the spatial correlation spreads out as the "
            "time lag grows: values far apart in space are related across a longer time gap."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A1), FadeIn(t1), FadeIn(key))
            vo.wait_until("b")
            self.play(Create(c1))
            vo.wait_until("c")
            self.play(FadeIn(A2), FadeIn(t2), Create(c2))
        self.clear_scene()

    def gneiting_row(self):
        rows = [
            cmath(r"C(h, u)", r"=", r"\dfrac{\sigma^2}{\psi(u^2)^{\delta + \beta d/2}} \exp\!\Big(-\dfrac{c\, h^{2\gamma}}{\psi(u^2)^{\beta\gamma}}\Big)", font_size=30),
            cmath(r"\psi(t)", r"=", r"a\, t^\alpha + 1", font_size=30),
            cmath(r"\beta \in [0, 1]", r":", r"\text{the space--time interaction; \ } \beta = 0 \text{ is separable}", font_size=30),
            cmath(r"\text{valid}", r":", r"\text{by a mixture argument: \ Gneiting (2002)}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"Gneiting's family"), why(r"how fast time decorrelates"), why(r"a parameter to test"),
                why(r"Bochner again")]
        with self.voiceover(
            "<bookmark mark='a'/> Gneiting's family of 2002, valid for positive variance, a and c, alpha and gamma "
            "between zero and one, beta between zero and one, and nonnegative delta, in the displayed spatial "
            "dimension. The time lag enters through a function psi, <bookmark mark='b'/> here a power plus one, "
            "<bookmark mark='c'/> and a single parameter beta between zero and one sets the space-time interaction. "
            "At zero, the model is separable, so separability becomes a hypothesis the data can test. <bookmark "
            "mark='d'/> Proving such functions valid, positive definite in space and time together, is the hard part,"
            " and Gneiting did it through Bochner's theorem and mixtures."
        ) as vo:
            intro=label('Space-time covariance validity requires parameter restrictions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world_acf(self):
        d = load("spacetime")
        acf = np.asarray(d["acf"], float)
        A = axes([0, 14], [-0.2, 1], x_length=7.4, y_length=4.0, xlabel=r"lag (days)", ylabel=r"autocorrelation",
                 xticks=[0, 7, 14], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = VGroup(*[Line(ax.c2p(k, 0), ax.c2p(k, a), color=FIELDC, stroke_width=6) for k, a in enumerate(acf)])
        ks = np.arange(15)
        reference = 0.7 ** ks * 4 / (4 + 1.5 ** 2 / 300)
        reference[0] = 1.0
        ref = polyline(ax, ks, reference, TAUC, 2.5)
        side = fit_rows(VGroup(
            label(r"the World's 300 stations, \ 365 days", font_size=22),
            label(r"day $t$ at station $s$: \ latent annual level + weather$_t$ + noise", font_size=22, color=GREY_A),
            label(rf"the station-average daily reading: \ lag-1 ACF {acf[1]:.2f}", font_size=22, color=FIELDC),
            label(r"gold: \ the AR(1) weather, \ $\phi = 0.7$", font_size=22, color=TAUC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's stations also report every day for a year. <bookmark mark='b'/> Each "
            "day's reading is the station's annual level, plus that day's weather, shared across the island, plus "
            "noise. <bookmark mark='c'/> The station-average daily reading has a lag-one autocorrelation of " + say(acf[1], 2) + ", "
            "<bookmark mark='d'/> which is the autoregressive weather of Part seventeen, with coefficient point seven."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ref), FadeIn(side[3]))
        self.clear_scene()

    def world_space(self):
        d = load("spacetime")
        b = np.asarray(d["bins"], float)
        sc = np.asarray(d["space_corr"], float)
        mids = (b[:-1] + b[1:]) / 2
        A = axes([0, 8], [0, 1], x_length=7.4, y_length=4.0, xlabel=r"distance between stations", ylabel=r"correlation of daily anomalies",
                 xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(m, c), radius=0.08, color=FIELDC) for m, c in zip(mids, sc)])
        ref = DashedLine(ax.c2p(0, d["share_weather"]), ax.c2p(8, d["share_weather"]), color=TAUC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"anomalies: \ each day minus the station's own mean", font_size=22),
            label(rf"their correlation: \ {sc[0]:.2f} at every distance", font_size=22, color=FIELDC),
            label(r"gold: \ $4/(4 + 1.5^2)$, \ weather's share of the daily variance", font_size=22, color=TAUC),
            label(r"a common signal looks like infinite range: \ model it first", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Subtract each station's own mean, and correlate the daily anomalies of pairs of "
            "stations. <bookmark mark='b'/> The correlation is " + say(sc[0], 2) + " at every distance, <bookmark mark='c'/> approximately the model's weather share of daily variance, with"
            " finite-series variation. <bookmark mark='d'/> A signal shared by the whole region looks, in the spatial"
            " covariance like a component that does not decay with distance. It cancels from same-day spatial "
            "differences and is invisible to that variogram. It must be modelled first, as a time series, before any "
            "spatial structure in what remains can be seen."
        ) as vo:
            self.add(pollution_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ref), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"dynamic models: \ a spatial field that evolves, \ $W_t = \phi\, W_{t-1} + \eta_t$ \ (a Kalman filter in space)", font_size=26, color=FIELDC),
            label(r"SPDEs in space and time: \ advection and diffusion, \ sparse precisions again", font_size=26, color=BANDC),
            label(r"climate reanalysis, \ air-quality forecasts, \ epidemic spread: \ all of this, \ at scale", font_size=26, color=TAUC),
            label(r"Cressie \& Wikle, \ \emph{Statistics for Spatio-Temporal Data} \ (2011)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice, space-time models are often dynamic: a spatial field that evolves by an "
            "autoregression, which is Part thirty-eight's Kalman filter with a field for a state. <bookmark mark='b'/> Or a "
            "stochastic partial differential equation with advection and diffusion, whose discretization is again sparse. "
            "<bookmark mark='c'/> Climate reanalyses, air-quality forecasts and maps of epidemic spread are built this "
            "way. <bookmark mark='d'/> Noel Cressie and Christopher Wikle's book of 2011 is the reference."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
