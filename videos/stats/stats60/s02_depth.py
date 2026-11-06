from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class Depth(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter one. Depth: Tukey's way to find the centre of a cloud of points, whatever a minority "
                            "of them do.", 1, r"Depth", r"The centre of a cloud", lit=(1975,))
        self.definition()
        self.map_chart()
        self.contaminated()
        self.breakdown()
        self.minimax()
        self.cost()

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> John Tukey, in 1975, defined the depth of a point among data in many dimensions. Draw every "
            "half-plane, or half-space, whose boundary passes through the point. <bookmark mark='b'/> The depth is the "
            "smallest fraction of the data in any of them. <bookmark mark='c'/> Points far outside the cloud have depth near "
            "zero; points in its middle have depth near a half. <bookmark mark='d'/> The Tukey median is the deepest point: "
            "in one dimension, the ordinary median.",
            [(r"D(x)", r"=", r"\min_{\|u\| = 1} \tfrac1n\#\{i: u'X_i \ge u'x\}", 40),
             (r"\text{reading}", r":", r"\text{the smallest half-space mass through } x", 40),
             (r"\text{outside}", r":", r"D \approx 0; \ \ \text{centre: \ } D \approx \tfrac12", 40),
             (r"\text{Tukey median}", r"=", r"\arg\max_x D(x)", 40)],
            [r"Tukey (1975)", r"halfspace depth", r"from rim to core", r"the median, \ generalized"],
            colors=[(0, DEPTHC), (3, DEPTHC)])

    def map_chart(self):
        d = load("depth")
        X = np.asarray(d["X"])
        A = axes([1.4, 5.4], [4.0, 9.8], x_length=6.4, y_length=4.8, xlabel=r"eruption length (min)", ylabel=r"waiting time (10 min)",
                 xticks=[2, 3, 4, 5], yticks=[5, 6, 7, 8, 9], center=[-2.6, 0.0, 0])
        ax = A.ax
        dm = DepthMap(ax, d["grid"], d["depth_grid"])
        cells = dm.cells(DEPTHC)
        pts = dm.dots(X, WHITE, 0.035)
        med = dm.mark(d["median"], FIXC)
        mean = dm.mark(d["mean"], NAIVEC)
        side = side_groups([
            [(r"Old Faithful: \ 272 eruptions", WHITE)],
            [(r"shade: \ Tukey depth", DEPTHC), (r"deeper is brighter", DEPTHC)],
            [(rf"green: \ the Tukey median", FIXC), (rf"$({d['median'][0]:.2f}, \ {d['median'][1]:.2f})$, \ depth {d['depth']:.2f}", FIXC)],
            [(rf"red: \ the mean", NAIVEC), (rf"$({d['mean'][0]:.2f}, \ {d['mean'][1]:.2f})$", NAIVEC)],
            [(r"two clusters: \ the mean falls", GREY_A), (r"between them, \ the median", GREY_A), (r"sits in the larger", GREY_A)],
        ], width=4.6, pos=(4.3, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> The part's instrument, the depth map, on Old Faithful: eruption length against waiting time "
            f"for two hundred and seventy-two eruptions. <bookmark mark='b'/> The shading is Tukey depth, computed over seven "
            f"hundred and twenty directions: bright in the core, fading to the rim. <bookmark mark='c'/> The deepest point, "
            f"the Tukey median, sits inside the larger cluster of long eruptions. <bookmark mark='d'/> The mean falls between "
            f"the clusters, where few eruptions are. <bookmark mark='e'/> Depth is about the shape of the cloud; the mean is "
            f"about its balance."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Old Faithful; \ Azzalini \& Bowman (1990)")))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.005), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cells, lag_ratio=0.0005), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(med, scale=0.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(mean, scale=0.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def contaminated(self):
        d = load("depth")
        X, bad = np.asarray(d["X"]), np.asarray(d["bad"])
        A = axes([1.4, 6.0], [2.4, 9.8], x_length=6.4, y_length=4.8, xlabel=r"eruption length (min)", ylabel=r"waiting time (10 min)",
                 xticks=[2, 3, 4, 5, 6], yticks=[3, 5, 7, 9], center=[-2.6, 0.0, 0])
        ax = A.ax
        dm = DepthMap(ax, d["grid_c"], d["depth_grid_c"])
        pts = dm.dots(X, WHITE, 0.035)
        bpts = dm.dots(bad, BADC, 0.05)
        cells = dm.cells(DEPTHC)
        m0, m1 = dm.mark(d["mean"], GREY_B), dm.mark(d["mean_c"], NAIVEC)
        t0, t1 = dm.mark(d["median"], GREY_B), dm.mark(d["median_c"], FIXC)
        shift_mean = float(np.linalg.norm(np.asarray(d["mean_c"]) - np.asarray(d["mean"])))
        shift_med = float(np.linalg.norm(np.asarray(d["median_c"]) - np.asarray(d["median"])))
        side = side_groups([
            [(r"30 planted points:", BADC), (r"long eruptions, \ short waits", BADC)],
            [(rf"the mean moves {shift_mean:.2f}", NAIVEC)],
            [(rf"the Tukey median moves {shift_med:.2f}", FIXC)],
            [(r"grey: \ where each was before", GREY_B)],
        ], width=4.6, pos=(4.3, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> Now plant thirty false eruptions, ten percent of the data, in an empty corner: long "
            f"eruptions followed by short waits. <bookmark mark='b'/> The mean is dragged toward them, by {say(shift_mean, 2)} in "
            f"these units. <bookmark mark='c'/> The depth map grows a thin, shallow wedge toward them, but its bright core holds, and the "
            f"Tukey median moves by "
            f"{say(shift_med, 2)}. <bookmark mark='d'/> The grey marks show where each was: the median held its place."
        ) as vo:
            self.play(FadeIn(A), FadeIn(pts, lag_ratio=0.005), FadeIn(m0), FadeIn(t0), FadeIn(museum_tag(r"Old Faithful; \ 30 points planted")))
            vo.wait_until("a")
            self.play(FadeIn(bpts, lag_ratio=0.05), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(m1, scale=0.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cells, lag_ratio=0.0005), FadeIn(t1, scale=0.5), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def breakdown(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> How much contamination can depth survive? The mean breaks down with a single point: move "
            "it far enough, and the mean follows. <bookmark mark='b'/> The coordinatewise median survives up to half the data "
            "in each coordinate, but its error grows with the dimension, as chapter two will show. <bookmark mark='c'/> The "
            "Tukey median's breakdown point is at least one over d plus one, and for well-behaved distributions a third, in "
            "any dimension. <bookmark mark='d'/> Its error under an epsilon fraction of contamination is of order epsilon, not "
            "epsilon root d.",
            [(r"\text{mean}", r":", r"\text{breakdown } 1/n", 40),
             (r"\text{coordinatewise median}", r":", r"\text{breakdown } \tfrac12, \ \text{error } \propto \varepsilon\sqrt d", 38),
             (r"\text{Tukey median}", r":", r"\text{breakdown} \ge \tfrac1{d+1}; \ \tfrac13 \text{ if symmetric}", 38),
             (r"\text{error}", r":", r"O(\varepsilon), \ \text{free of } d", 40)],
            [r"Part 30's breakdown", r"chapter 2", r"Donoho \& Gasko (1992)", r"optimal"],
            colors=[(0, NAIVEC), (3, FIXC)])

    def minimax(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Mengjie Chen, Chao Gao and Zhao Ren proved in 2018 that depth is minimax-optimal for "
            "contaminated data. <bookmark mark='b'/> Under Huber contamination of a Gaussian, the best possible error for the "
            "mean is root of d over n plus epsilon: the first term is the price of the sample, the second of the "
            "contamination. <bookmark mark='c'/> The Tukey median attains it. <bookmark mark='d'/> So do depth-based "
            "estimators of covariance matrices, through matrix depth: robustness costs only an additive epsilon, not a "
            "factor of the dimension.",
            [(r"\text{model}", r":", r"(1 - \varepsilon)N(\theta, I_d) + \varepsilon Q", 40),
             (r"\text{minimax}", r":", r"\|\hat\theta - \theta\| \asymp \sqrt{d/n} + \varepsilon", 40),
             (r"\text{Tukey median}", r":", r"\text{attains it}", 40),
             (r"\text{covariance}", r":", r"\text{matrix depth, \ the same rate}", 40)],
            [r"Chen, \ Gao \& Ren (2018)", r"Part 50's minimax", r"optimal", r"robust PCA, \ too"],
            colors=[(1, FIXC), (2, FIXC)])

    def cost(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The catch is computation. Depth is defined by a minimum over all directions, and in d "
            "dimensions there are too many: computing the Tukey median exactly takes time exponential in d. <bookmark "
            "mark='b'/> In two dimensions it is easy, as the map showed; in fifty, hopeless. <bookmark mark='c'/> For decades, "
            "statistics had estimators that were robust or computable in high dimensions, not both. <bookmark mark='d'/> "
            "Chapter two is the 2016 breakthrough that ended the dilemma.",
            [(r"\text{computing depth}", r":", r"\text{a minimum over all directions}", 40),
             (r"\text{Tukey median}", r":", r"\text{exponential in } d", 40),
             (r"\text{the dilemma}", r":", r"\text{robust \ or \ computable}", 40),
             (r"\text{2016}", r":", r"\text{both}", 40)],
            [r"the hard part", r"NP-hard in general", r"for decades", r"chapter 2"],
            colors=[(1, NAIVEC), (3, FIXC)])
