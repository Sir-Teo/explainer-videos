from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


def town_map(d, values, center, width, lo, hi):
    x, y, pop = (np.asarray(d[k], float) for k in ("x", "y", "pop"))
    F = FieldSurface(x, y, values, 0.3, width=width, center=center, lo=lo, hi=hi)
    rad = 0.03 + 0.09 * np.sqrt(pop / pop.max())
    dots = VGroup(*[Dot(F.p(a, b), radius=r, color=F.colour(v), fill_opacity=0.95) for a, b, v, r in zip(x, y, values, rad)])
    return F, dots


class Areal(VoiceoverScene):
    def construct(self):
        self.card()
        self.moran()
        self.test()
        self.smr()
        self.bym()
        self.carsar()
        self.maps()
        self.scatter_plot()

    def card(self):
        card = chapter_card(9, r"Areal data", r"Disease maps without the noise", lit=(1974, 1991), part=PART)
        with self.voiceover("Chapter nine. Areal data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def moran(self):
        rows = [
            cmath(r"W_{ij}", r"=", r"1 \text{ if regions } i, j \text{ are neighbours}, \ 0 \text{ otherwise}", font_size=30),
            cmath(r"I", r"=", r"\dfrac{n}{\sum_{ij} W_{ij}} \, \dfrac{\sum_{ij} W_{ij} (z_i - \bar z)(z_j - \bar z)}{\sum_i (z_i - \bar z)^2}", font_size=30),
            cmath(r"E[I]", r"=", r"-1/(n - 1) \ \text{under no dependence}", font_size=30),
            cmath(r"p\text{-value}", r":", r"\text{permute the values over the map}", font_size=30),
        ]
        rows[1][-1].set_color(AREAC)
        whys = [why(r"a graph, \ not distances"), why(r"Moran (1950): \ a spatial correlation"), why(r"near zero"),
                why(r"Part 16's permutation test")]
        with self.voiceover(
            "<bookmark mark='a'/> Areal data come as one value per region, and dependence is described by a graph: which "
            "regions are neighbours. <bookmark mark='b'/> Patrick Moran's statistic of 1950 is a correlation between each "
            "region's value and its neighbours' values. <bookmark mark='c'/> Without spatial dependence it is close to "
            "zero. <bookmark mark='d'/> To test, permute the values over the map, as in Part sixteen, and see how often a "
            "random arrangement looks as clustered."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def test(self):
        d = load("areal")
        mi = d["moran"]
        sd = mi["null_sd"]
        A = axes([-0.15, 0.15], [0, 11], x_length=7.4, y_length=4.0, xlabel=r"Moran's $I$", ylabel=r"density",
                 xticks=[-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15], yticks=[0, 5, 10], xfmt=lambda v: f"{v:g}",
                 yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.linspace(-0.15, 0.15, 200)
        ys = np.exp(-0.5 * ((xs - mi["E"]) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        nd = density(ax, xs, ys, NULLC)
        ob = DashedLine(ax.c2p(mi["I"], 0), ax.c2p(mi["I"], 10.5), color=OBS, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"the World's 200 towns: \ log case rates", font_size=22),
            label(rf"neighbours: \ the 5 nearest towns \ ({d['n_edges']} links)", font_size=22, color=GREY_A),
            label(r"grey: \ the permutation null", font_size=22, color=NULLC),
            label(rf"observed $I = {mi['I']:.3f}$, \ $p = {mi['p']:.3f}$", font_size=22, color=OBS),
            label(r"clustering: \ neighbouring towns have similar rates", font_size=22, color=AREAC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's two hundred towns, each with a count of new cases of a respiratory disease "
            "over a year, and its expected count from its population. <bookmark mark='b'/> Call two towns neighbours if "
            "either is among the other's five nearest. <bookmark mark='c'/> The permutation distribution of Moran's I is "
            "centred near zero. <bookmark mark='d'/> The observed value is " + say(mi["I"], 3) + ", with a p-value of "
            + say(mi["p"], 3) + ". <bookmark mark='e'/> Neighbouring towns have similar rates, because they breathe the same "
            "air: the pollution field of the earlier chapters."
        ) as vo:
            self.add(towns_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(nd), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ob), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def smr(self):
        d = load("areal")
        smr = np.asarray(d["smr"], float)
        rows = [
            cmath(r"\text{SMR}_i", r"=", r"y_i / E_i: \ \text{observed over expected cases}", font_size=32),
            cmath(r"\text{Var}(\text{SMR}_i)", r"\approx", r"\text{RR}_i / E_i: \ \text{huge for small towns}", font_size=30),
            cmath(r"\text{here}", r":", rf"\text{{the smallest towns' SMRs run from }} {d['range_smr_small'][0]:.1f} \text{{ to }} {d['range_smr_small'][1]:.2f}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the map's extremes are the smallest towns: \ Part 25 again}", font_size=30),
        ]
        rows[3][-1].set_color(MISSC)
        whys = [why(r"the standardized ratio"), why(r"Poisson noise"), why(rf"{int((smr == 0).sum())} towns with no cases"),
                why(r"the kidney cancer map")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual map shows the standardized morbidity ratio: observed over expected cases. "
            "<bookmark mark='b'/> Its variance is roughly the risk over the expected count, so for a small town it is huge. "
            "<bookmark mark='c'/> Among the smallest quarter of the World's towns, the ratios run from zero to "
            + say(d["range_smr_small"][1], 1) + ". <bookmark mark='d'/> The highest and lowest rates on the map are the "
            "smallest towns, Part twenty-five's kidney cancer map once more."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bym(self):
        rows = [
            cmath(r"y_i", r"\sim", r"\text{Poisson}\big(E_i\, e^{\mu + u_i + v_i}\big)", font_size=32),
            cmath(r"u_i \mid u_{-i}", r"\sim", r"N\big(\bar u_{\text{nbrs}(i)}, \ 1/(\tau_u m_i)\big)", font_size=30),
            cmath(r"v_i", r"\sim", r"N(0, 1/\tau_v) \ \text{independently}", font_size=30),
            cmath(r"\text{result}", r":", r"\text{each town shrinks toward its neighbours, \ more if it is small}", font_size=30),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"Besag, York \& Molli\'e (1991)"), why(r"the intrinsic CAR: \ a GMRF"), why(r"unstructured heterogeneity"),
                why(r"local partial pooling")]
        with self.voiceover(
            "<bookmark mark='a'/> Julian Besag, Jeremy York and Annie Mollié proposed in 1991 a model that became the "
            "standard for disease maps. The counts are Poisson, with a log relative risk made of two random effects. "
            "<bookmark mark='b'/> One is spatial: given its neighbours, each town's effect is normal around their average, "
            "the intrinsic conditional autoregression, a Markov random field. <bookmark mark='c'/> The other is "
            "independent noise for each town. <bookmark mark='d'/> The result is Part twenty-five's partial pooling, but "
            "local: each town is pulled toward its neighbours rather than toward the overall mean, and the smaller the "
            "town, the harder the pull."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def maps(self):
        d = load("areal")
        smr, sm, tr = (np.asarray(d[k], float) for k in ("smr", "rr_smooth", "true_rr"))
        lo, hi = 0.4, 2.0
        F1, d1 = town_map(d, smr, [-4.4, 0.3, 0], 4.0, lo, hi)
        F2, d2 = town_map(d, sm, [0.0, 0.3, 0], 4.0, lo, hi)
        F3, d3 = town_map(d, tr, [4.4, 0.3, 0], 4.0, lo, hi)
        t1 = label(r"raw SMR", font_size=24, color=MISSC).next_to(d1, UP, buff=0.25)
        t2 = label(r"BYM smoothed", font_size=24, color=BANDC).next_to(d2, UP, buff=0.25)
        t3 = label(r"the true risk", font_size=24, color=TRUEC).next_to(d3, UP, buff=0.25)
        key = F1.key(r"relative risk").move_to([0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The three maps, with dot size showing population. The raw ratios: a speckle, with the "
            "brightest and darkest dots mostly small towns. <bookmark mark='b'/> The smoothed relative risks: the speckle "
            "is gone, and a pattern appears, higher in the towns near the busy centres. <bookmark mark='c'/> And the true "
            "risks, which only the World knows: the smoothed map is much closer to them."
        ) as vo:
            self.add(towns_tag())
            vo.wait_until("a")
            self.play(FadeIn(d1), FadeIn(t1), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(d2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(d3), FadeIn(t3))
        self.clear_scene()

    def scatter_plot(self):
        d = load("areal")
        smr, sm, tr = (np.asarray(d[k], float) for k in ("smr", "rr_smooth", "true_rr"))
        A = axes([0, 2.2], [0, 3.4], x_length=6.0, y_length=4.6, xlabel=r"true relative risk", ylabel=r"estimate",
                 xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.4, 0.0, 0])
        ax = A.ax
        s1 = scatter(ax, tr, np.minimum(smr, 3.35), MISSC, 0.045, 0.7)
        s2 = scatter(ax, tr, sm, BANDC, 0.05, 0.9)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(2.2, 2.2), color=GREY_B, stroke_width=2)
        r1 = float(np.sqrt(np.mean((smr - tr) ** 2)))
        r2 = float(np.sqrt(np.mean((sm - tr) ** 2)))
        side = fit_rows(VGroup(
            label(r"each dot a town", font_size=22),
            label(rf"raw SMR \ (red): \ RMSE {r1:.2f}", font_size=22, color=MISSC),
            label(rf"BYM \ (green): \ RMSE {r2:.2f}", font_size=22, color=BANDC),
            label(r"smoothing flattens the true gradient a little: \ shrinkage's bias", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.4, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Against the truth, town by town. <bookmark mark='b'/> The raw ratios scatter widely, with a "
            "root mean squared error of " + say(r1, 2) + ". <bookmark mark='c'/> The smoothed risks hug the diagonal, with "
            + say(r2, 2) + ", about a third. <bookmark mark='d'/> They are a little too flat: the highest risks are "
            "underestimated and the lowest overestimated, the bias that buys the variance reduction, exactly as with "
            "James and Stein."
        ) as vo:
            self.add(towns_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(diag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(s1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(s2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def carsar(self):
        rows = [
            cmath(r"\text{CAR}", r":", r"Z_i \mid Z_{-i} \sim N\big(\rho \textstyle\sum_j w_{ij} Z_j, \ \tau^2_i\big)", font_size=30),
            cmath(r"\text{joint}", r":", r"Z \sim N\big(0, (I - \rho W)^{-1} T\big), \ \ T = \text{diag}(\tau_i^2)", font_size=30),
            cmath(r"\text{SAR}", r":", r"Z = \rho W Z + \varepsilon: \ \ \text{Var}\,Z = (I - \rho W)^{-1} \Sigma_\varepsilon (I - \rho W^\top)^{-1}", font_size=28),
            cmath(r"\text{intrinsic}", r":", r"\rho = 1: \ \text{improper, \ but fine as a prior on effects}", font_size=30),
        ]
        rows[1][-1].set_color(AREAC)
        whys = [why(r"Besag (1974): \ conditionals"), why(r"a sparse precision"), why(r"Whittle (1954): \ simultaneous"),
                why(r"the ICAR")]
        with self.voiceover(
            "<bookmark mark='a'/> Two classical models for areas. The conditional autoregression, Besag's CAR, specifies "
            "each region's distribution given its neighbours: normal, around a multiple rho of their weighted sum. "
            "<bookmark mark='b'/> The joint distribution then has a sparse precision matrix, I minus rho W, a Markov random "
            "field on the map's graph. <bookmark mark='c'/> The simultaneous autoregression, from Whittle and the "
            "econometricians, writes all the regions at once, as a regression on their neighbours plus noise. Its "
            "precision is a product, so it is less sparse, and the two models imply different correlations for the same "
            "W. <bookmark mark='d'/> With rho equal to one the CAR becomes intrinsic: improper as a model for data, but a "
            "perfectly good prior for random effects whose overall level is set elsewhere."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
