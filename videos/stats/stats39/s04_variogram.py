from __future__ import annotations

import numpy as np

from explainer.stats.kit import spatial as SPK
from videos.stats.stats39.common import *  # noqa: F403


class Variogram(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.cloud()
        self.parts()
        self.robust()
        self.aniso()
        self.world()

    def card(self):
        card = chapter_card(3, r"Variograms", r"How different are values a distance $h$ apart?", lit=(1962, 1985), part=PART)
        with self.voiceover("Chapter three. Variograms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"\gamma(h)", r"=", r"\tfrac12\, E\,[Z(s + h) - Z(s)]^2", font_size=32),
            cmath(r"\text{stationary}", r":", r"\gamma(h) = C(0) - C(h)", font_size=30),
            cmath(r"\hat\gamma(h)", r"=", r"\dfrac{1}{2N(h)} \textstyle\sum_{|s_i - s_j| \approx h} (Z_i - Z_j)^2", font_size=30),
            cmath(r"\text{why not } C", r":", r"\gamma \text{ can describe intrinsic stationary increments without stationary levels}", font_size=28),
        ]
        rows[2][-1].set_color(VARC)
        whys = [why(r"the semivariogram"), why(r"the covariance, \ upside down"), why(r"Matheron (1962)"),
                why(r"the geostatistician's choice")]
        with self.voiceover(
            "<bookmark mark='a'/> Geostatisticians usually describe dependence by the semivariogram: half the expected "
            "squared difference between values a distance h apart. <bookmark mark='b'/> For a stationary field it is the "
            "variance minus the covariance: the covariance turned upside down. <bookmark mark='c'/> Matheron's estimate "
            "averages half the squared differences of all pairs whose separation falls in each distance bin. <bookmark "
            "mark='d'/> It needs no estimate of the mean, and it exists for fields with stationary increments even when "
            "the covariance does not, like the random walk of Part thirty-eight."
        ) as vo:
            intro=label('Semivariograms describe squared increments under stated stationarity',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _axes(self, top=0.9):
        return axes([0, 1.6], [0, top], x_length=7.4, y_length=4.2, xlabel=r"distance (km)", ylabel=r"semivariance of log zinc",
                    xticks=[0, 0.4, 0.8, 1.2, 1.6], yticks=[0, 0.3, 0.6, 0.9], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                    center=[-2.5, 0.2, 0])

    def cloud(self):
        d = load("meuse")
        v = d["v"]
        A = self._axes()
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(h, g_), radius=0.04 + 0.04 * min(n / 600, 1), color=VARC)
                        for h, g_, n in zip(v["lag"], v["gamma"], v["n"])])
        fs = d["fs"]
        hs = np.linspace(0.001, 1.6, 120)
        cs = polyline(ax, hs, SPK.model_variogram(hs, fs["nugget"], fs["sill"], fs["range"], "sph"), BANDC, 3)
        side = fit_rows(VGroup(
            label(r"Meuse, \ log zinc: \ 15 distance bins", font_size=22),
            label(r"dot size: \ number of pairs", font_size=22, color=GREY_A),
            label(r"rising, \ then levelling off", font_size=22, color=VARC),
            label(rf"spherical fit: \ nugget {fs['nugget']:.3f}, \ partial sill {fs['sill']:.2f}, \ range {fs['range']:.2f} km", font_size=22, color=BANDC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The empirical semivariogram of log zinc at Meuse, in fifteen distance bins, each "
            "dot sized by the number of pairs behind it. <bookmark mark='b'/> It rises with distance, as Tobler's law"
            " says it should, <bookmark mark='c'/> the fitted spherical model then levels off: beyond its range it "
            "assigns zero residual covariance, as if comparing two random ones. <bookmark mark='d'/> A spherical "
            "model, fitted by Noel Cressie's weighted least squares of 1985, has a nugget of " + say(fs["nugget"], 2) + ", a partial sill of " + say(fs["sill"], 2) + ", and a range of "
            + say(fs["range"], 1) + " kilometres."
        ) as vo:
            self.add(meuse_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs), FadeIn(side[3]))
        self.clear_scene()

    def parts(self):
        d = load("meuse")
        fs = d["fs"]
        A = self._axes()
        ax = A.ax
        hs = np.linspace(0.001, 1.6, 120)
        cs = polyline(ax, hs, SPK.model_variogram(hs, fs["nugget"], fs["sill"], fs["range"], "sph"), BANDC, 3)
        nug = DoubleArrow(ax.c2p(0.05, 0), ax.c2p(0.05, fs["nugget"] + 0.001), buff=0, color=PTC, stroke_width=3, tip_length=0.1)
        sill = DashedLine(ax.c2p(0, fs["nugget"] + fs["sill"]), ax.c2p(1.6, fs["nugget"] + fs["sill"]), color=TAUC, stroke_width=2)
        rng_ = DashedLine(ax.c2p(fs["range"], 0), ax.c2p(fs["range"], 0.9), color=FIELDC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"nugget: \ the jump at zero \ (measurement error, \ micro-scale)", font_size=22, color=PTC),
            label(r"sill: \ the plateau, \ the field's total variance", font_size=22, color=TAUC),
            label(r"range: \ the distance where correlation ends", font_size=22, color=FIELDC),
        ), 4.6, 0.45, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Its three features have names. The nugget is the jump at the origin: two samples a hair "
            "apart still differ, because of measurement error and variation at scales smaller than the sampling. <bookmark "
            "mark='b'/> The sill is the plateau, the total variance of the field. <bookmark mark='c'/> And the range is the "
            "distance at which the plateau is reached, where correlation ends."
        ) as vo:
            self.add(meuse_tag())
            self.play(FadeIn(A), Create(cs))
            vo.wait_until("a")
            self.play(GrowFromCenter(nug), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sill), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rng_), FadeIn(side[2]))
        self.clear_scene()

    def robust(self):
        d = load("meuse")
        v, vr = d["v"], d["vr"]
        A = self._axes(1.0)
        ax = A.ax
        c1 = polyline(ax, v["lag"], v["gamma"], VARC, 3)
        c2 = polyline(ax, vr["lag"], vr["gamma"], BANDC, 3)
        side = fit_rows(VGroup(
            label(r"squared differences: \ one outlier pair dominates its bin", font_size=22, color=MISSC),
            label(r"Cressie \& Hawkins (1980): \ average $|Z_i - Z_j|^{1/2}$, \ then raise to the 4th power", font_size=22, color=BANDC),
            label(r"gold: \ classical; \ green: \ robust", font_size=22, color=GREY_A),
            label(r"close here; similarity does not prove absence of outliers", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Squared differences are sensitive: one outlying sample enters every pair it belongs"
            " to, and can dominate a bin. <bookmark mark='b'/> Noel Cressie and Douglas Hawkins proposed in 1980 to "
            "average the square roots of the absolute differences instead, then raise the average to the fourth power"
            " and correct its bias, Part thirty's robustness applied to variograms. <bookmark mark='c'/> On log zinc "
            "the two estimates are close, <bookmark mark='d'/> consistent with the logs reducing the influence of "
            "large concentrations; agreement does not establish that no outliers remain."
        ) as vo:
            self.add(meuse_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def world(self):
        d = load("world")
        v = d["v"]
        f = d["fits"]["1.5"]
        tp = d["truth_params"]
        A = axes([0, 6], [0, 12], x_length=7.4, y_length=4.2, xlabel=r"distance", ylabel=r"semivariance",
                 xticks=[0, 2, 4, 6], yticks=[0, 4, 8, 12], center=[-2.5, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(h, g_), radius=0.06, color=VARC) for h, g_ in zip(v["lag"], v["gamma"])])
        hs = np.linspace(0.001, 6, 120)
        truth = polyline(ax, hs, tp["tau2"] + tp["sigma2"] - SPK.matern(hs, tp["sigma2"], tp["rho"], 1.5), TRUEC, 2.5)
        side = fit_rows(VGroup(
            label(r"the World's 300 stations, \ after removing the traffic trend", font_size=22),
            label(r"gold: \ nominal Mat\'ern variogram: partial sill 6.25, nugget 0.64", font_size=22, color=TRUEC),
            label(r"the empirical one keeps rising: \ the island is only a few ranges wide", font_size=22, color=VARC),
            label(r"one field, \ one island: \ the far bins rest on few, \ dependent pairs", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's stations, after subtracting the traffic trend. <bookmark mark='b'/> The"
            " true variogram, in gold, levels off at total sill six point eight nine, including the nugget. The World"
            " uses a very fine numerical approximation to the Matérn grid covariance. <bookmark mark='c'/> The "
            "empirical one tracks it at short distances, then keeps rising. <bookmark mark='d'/> The island is only a"
            " few ranges wide, and at large distances the bins rest on pairs that are all part of one realization, so"
            " they are noisy and dependent. Variograms are best trusted at the distances that matter for prediction: "
            "short ones."
        ) as vo:
            self.add(pollution_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def aniso(self):
        d = load("extra")
        A = axes([0, 1.6], [0, 1.2], x_length=7.4, y_length=4.2, xlabel=r"distance (km)", ylabel=r"semivariance of log zinc",
                 xticks=[0, 0.4, 0.8, 1.2, 1.6], yticks=[0, 0.4, 0.8, 1.2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0": FIELDC, "45": BANDC, "90": TAUC, "135": PTC}
        cs = {a: polyline(ax, v["lag"], v["gamma"], cols[a], 3) for a, v in d["dir"].items()}
        side = fit_rows(VGroup(
            label(r"pairs grouped by direction \ ($\pm 22.5^\circ$)", font_size=22),
            label(r"north--south \ (blue); \ east--west \ (gold)", font_size=22, color=GREY_A),
            label(r"north-east \ (green): \ along the river, \ lowest", font_size=22, color=BANDC),
            label(r"north-west \ (red): \ across it, \ highest", font_size=22, color=PTC),
            label(r"geometric anisotropy: \ stretch the coordinates, \ then fit as before", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Isotropy is an assumption, and it can be checked. Group the pairs of samples by the"
            " direction between them, and compute a variogram for each direction. <bookmark mark='b'/> North to south"
            " and east to west lie in between. <bookmark mark='c'/> Along the north-east diagonal, the direction the "
            "river runs, values change most slowly: <bookmark mark='d'/> across the river they change fastest, "
            "because moving away from the bank changes how often the soil was flooded. <bookmark mark='e'/> These raw"
            " directional differences can reflect the river-distance trend as well as anisotropic residual "
            "covariance. Genuine geometric anisotropy can be modelled by stretching the coordinates before using an "
            "isotropic model, and universal kriging's river-distance trend absorbs much of it here."
        ) as vo:
            self.add(meuse_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["0"]), Create(cs["90"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["45"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["135"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
