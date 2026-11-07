from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Ranks(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Multivariate ranks and quantiles: transport to a reference law.", 7,
                            r"Multivariate ranks", r"Center-outward, \ by transport", lit=(2017,))
        self.problem()
        self.definition()
        self.properties()
        self.contours()
        self.free()
        self.test()
        self.board()
        self.power()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> On a line, the rank of a point is its position in the order, and ranks make Part sixteen's "
            "tests distribution-free: under the null, every arrangement of ranks is equally likely, whatever the law. "
            "<bookmark mark='b'/> In the plane there is no order. Coordinatewise ranks depend on the axes; depth gives "
            "contours but they are always convex. <bookmark mark='c'/> The key fact on the line: the rank is F of x, and F "
            "is the monotone map pushing the law onto the uniform. <bookmark mark='d'/> So define the multivariate rank as "
            "the optimal transport map onto a fixed reference law.",
            [(r"d = 1", r":", r"\text{ranks} \Rightarrow \text{distribution-free tests}", 40),
             (r"d > 1", r":", r"\text{no order; \ coordinatewise ranks depend on axes}", 38),
             (r"\text{on a line}", r":", r"\mathrm{rank} = F(x), \ \ F_\#P = U[0, 1]", 40),
             (r"\text{so}", r":", r"\text{rank} = \text{the transport map to a reference}", 40)],
            [r"Part 16", r"Part 60's depth: \ convex only", r"monotone", r"Chernozhukov et al. (2017)"],
            colors=[(3, PLANC)])

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Victor Chernozhukov, Alfred Galichon, Marc Hallin and Marc Henry, in 2017, and Hallin, "
            "Eustasio del Barrio, Juan Cuesta-Albertos and Carlos Matrán, in 2021, chose as reference the spherical uniform: "
            "uniform direction, uniform radius in the unit ball. <bookmark mark='b'/> The center-outward distribution "
            "function is the Brenier map from the law to that reference. <bookmark mark='c'/> Empirically, place n points on "
            "a regular grid of rings and rays in the unit disc, and solve the assignment from the data to the grid. "
            "<bookmark mark='d'/> A point's rank is the radius of its grid point; its sign is the direction. The quantile "
            "contour at level tau is the set of data mapped to the ring of radius tau.",
            [(r"\text{reference}", r":", r"U_d: \ \text{uniform direction} \times \text{uniform radius}", 38),
             (r"F_\pm", r"=", r"\nabla\varphi, \ \ (F_\pm)_\#P = U_d", 40),
             (r"\text{empirical}", r":", r"\text{assign the data to a grid of rings and rays}", 38),
             (r"\text{rank, \ sign}", r":", r"\|F_\pm(x)\|, \ \ F_\pm(x)/\|F_\pm(x)\|", 40)],
            [r"Hallin et al. (2021)", r"center-outward", r"an assignment", r"quantile contours"],
            colors=[(1, PLANC)])

    def contours(self):
        d = load("ranks")
        X = np.asarray(d["X"])
        A = axes([-2.4, 2.2], [-2.6, 2.2], x_length=5.6, y_length=5.4, xlabel=r"eruption length (standardized)", ylabel=r"waiting time (standardized)",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-2.9, -0.05, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(*x), radius=0.035, color=WHITE, fill_opacity=0.7) for x in X])
        levels = d["levels"]
        cols = [PLANC, FLOWC, TGT]
        cont = VGroup()
        for lev, c in zip(levels[1::2], cols):
            P = np.asarray(d["contours"][f"{lev:.4f}"])
            k = 7  # a circular moving average along the ring, for display
            Ps = np.array([P[np.arange(i - k // 2, i + k // 2 + 1) % len(P)].mean(0) for i in range(len(P))])
            poly = Polygon(*[ax.c2p(*p) for p in Ps], color=c, stroke_width=3, fill_opacity=0.0)
            cont.add(poly)
        ell = VGroup()
        for lev in levels[1::2]:
            E = np.asarray(d["ellipses"][f"{lev:.4f}"])
            ell.add(Polygon(*[ax.c2p(*p) for p in E], color=NAIVEC2, stroke_width=2, stroke_opacity=0.8).set_fill(opacity=0))
        med = Dot(ax.c2p(*d["median"]), radius=0.1, color=PLANC)
        side = side_groups([
            [(r"Old Faithful, \ standardized", WHITE), (r"272 points; \ 6 rings $\times$ 45 rays", GREY_A)],
            [(r"green, \ teal, \ gold: \ center-outward", PLANC), (r"contours, \ $\tau = \tfrac27, \tfrac47, \tfrac67$", PLANC), (r"(smoothed along each ring)", GREY_A)],
            [(r"red: \ Mahalanobis ellipses", NAIVEC2), (r"at the same normal levels", NAIVEC2)],
            [(r"the contours follow the two clusters;", GREY_A), (r"the ellipses cannot", GREY_A)],
        ], width=4.6, pos=(4.1, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> Old Faithful again, standardized, with a grid of six rings and forty-five rays. <bookmark "
            f"mark='b'/> The assignment maps each eruption to a grid point. Joining the eruptions mapped to each ring gives the "
            f"center-outward quantile contours; three of them are drawn, smoothed along each ring, from the innermost in green "
            f"to the outermost in gold. <bookmark mark='c'/> "
            f"In red, the Mahalanobis ellipses with the same probability under a normal model. <bookmark mark='d'/> The "
            f"contours bend to follow the two clusters and the gap between them; the ellipses, which see only a mean and a "
            f"covariance, put their centre in the gap, where few eruptions are."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts), FadeIn(museum_tag(r"Old Faithful; \ Azzalini \& Bowman (1990)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cont], lag_ratio=0.4), FadeIn(med), FadeIn(side[1]), run_time=3.5)
            vo.wait_until("c")
            self.play(*[Create(e) for e in ell], FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def free(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Transport ranks use a fixed reference grid and a sample-equivariant assignment rule. <bookmark mark='b'/> For IID observations with an almost surely unique assignment, exchangeability makes the assignment a uniform permutation of the fixed reference points. Randomized tie handling can preserve the symmetry when ties occur. <bookmark mark='c'/> Rank statistics then have a distribution-free null under these conditions; reference choice and sample sizes still determine that null. <bookmark mark='d'/> This extends the logic of scalar rank tests, with additional care about grid construction and ties.",
            [(r"H_0", r":", r"X_1, \dots, X_n \ \text{i.i.d.} \sim P, \ \text{a density}", 40),
             (r"\text{then}", r":", r"\text{the assignment to the grid is a uniform permutation}", 38),
             (r"\text{so}", r":", r"\text{rank statistics are distribution-free}", 40),
             (r"\text{like}", r":", r"\text{Wilcoxon, \ Kruskal--Wallis, \ in } \mathbb R^d", 40)],
            [r"exchangeability", r"the grid is fixed", r"tabulate once", r"Part 16"],
            colors=[(2, PLANC)])

    def test(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Deb and Sen's rank energy test compares pooled transport ranks. <bookmark mark='b'/> Our reference is a fixed distinct Halton set, and we randomize pooled row order before assignment to avoid label-dependent resolution of ties. <bookmark mark='c'/> Compute energy distance between the two groups' assigned reference points. Pairwise reference distances are cached once. <bookmark mark='d'/> Under independent IID samples from the same law, exchangeability and the randomized assignment give a valid permutation test without moment assumptions. We use one hundred and ninety-nine permutations with a plus-one p-value and reject at p at most five percent; discreteness and ties can make the test conservative.",
            [(r"\text{pool}", r":", r"Z = X \cup Y, \ \ N = n + m", 40),
             (r"\text{ranks}", r":", r"R = \text{assignment of } Z \text{ to a fixed reference set}", 38),
             (r"\text{statistic}", r":", r"\mathcal E(R_X, R_Y) = 2E\|R_X - R_Y\| - E\|R_X - R_X'\| - E\|R_Y - R_Y'\|", 32),
             (r"\text{null}", r":", r"\text{permutations, \ exact, \ for any } P", 40)],
            [r"Deb \& Sen (2023)", r"a Halton set here", r"the energy distance", r"distribution-free"],
            colors=[(3, PLANC)])

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("Hotelling", "rank energy"),
                   f"<bookmark mark='a'/> On the Board, under the null, with bivariate Cauchy data, forty points per sample, and a "
                   f"thousand repetitions. Hotelling's T squared rejects {100 * br[0]['achieved']:.1f} percent of the time at "
                   f"nominal five: conservative, its normal theory confused by the heavy tails. <bookmark mark='b'/> The rank "
                   f"energy test rejects {100 * br[1]['achieved']:.1f} percent: consistent with level control in this Monte Carlo experiment; exact equality to five percent is not promised.",
                   [("a", [0]), ("b", [1])])

    def power(self):
        d = load("tests")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Size is half the story. <bookmark mark='b'/> Shift the second Cauchy sample by one unit in "
            f"each coordinate. <bookmark mark='c'/> Hotelling's test detects it {100 * d['pow_hot']:.0f} percent of the time; "
            f"the sample means of Cauchy data are as variable as single observations. <bookmark mark='d'/> The rank energy "
            f"test detects it {100 * d['pow_rank']:.0f} percent of the time. Deb, Bhaswar Bhattacharya and Sen "
            f"showed that suitably scored rank tests lose little efficiency against Hotelling's even for Gaussian data: the trade made by Wilcoxon, in many dimensions.",
            [(r"\text{alternative}", r":", r"Y \sim \text{Cauchy} + (1, 1)", 40),
             (r"\text{Hotelling}", r":", rf"\text{{power}} \ {100 * d['pow_hot']:.0f}\%", 40),
             (r"\text{rank energy}", r":", rf"\text{{power}} \ {100 * d['pow_rank']:.0f}\%", 40),
             (r"\text{Gaussian data}", r":", r"\text{little efficiency lost}", 40)],
            [rf"{d['preps']} repetitions", r"means of Cauchy data", r"ranks are robust", r"Part 30's AREs"],
            colors=[(1, NAIVEC2), (2, PLANC)])

    def properties(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Define population quantile regions as inverse images, or quantile-map images, of reference balls under the appropriate regularity assumptions. <bookmark mark='b'/> Their nesting follows from nested reference balls. The spherical reference has a uniform radius, so probability content is tau when the transport has the needed inverse and no boundary mass. This is not a statement about any smoothed polygon drawn through finite data. <bookmark mark='c'/> Empirical center-outward maps have consistency results under specified population regularity and on the domains in the theorem. A global supremum over arbitrary out-of-sample extensions is not automatic. <bookmark mark='d'/> Population regions can be nonconvex. Our joined, smoothed ring points illustrate this geometry rather than supplying exact finite-sample confidence contours.",
            [(r"\text{nested}", r":", r"\tau < \tau' \Rightarrow \mathcal C_\tau \subset \mathcal C_{\tau'}", 40),
             (r"\text{probability content}", r":", r"P(\mathcal C_\tau)=\tau\quad\text{under population regularity}", 40),
             (r"\text{Glivenko--Cantelli}", r":", r"\text{empirical-map consistency under stated regularity}", 40),
             (r"\text{shape}", r":", r"\text{not necessarily convex}", 40)],
            [r"monotone maps", r"unlike ellipses", r"Hallin et al. (2021)", r"unlike depth"],
            colors=[(1, PLANC)])
