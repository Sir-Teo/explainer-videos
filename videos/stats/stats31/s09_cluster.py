from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403

KC = [S.ACCENT, S.RESID, S.ALT]  # k-means clusters: gold, red, teal (not species colours)


class Cluster(VoiceoverScene):
    def construct(self):
        self.card()
        self.objective()
        self.lloyd()
        self.hard_em()
        self.mixture()
        self.pitfalls()
        self.compare()
        self.choose_k()
        self.cautions()

    def card(self):
        card = chapter_card(8, r"Clustering", r"Finding groups nobody told you about", lit=(1957, 1977), part=PART)
        with self.voiceover("Chapter eight. Clustering."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def objective(self):
        rows = [
            cmath(r"\min_{C, \, c_1..c_k}", r"", r"\textstyle\sum_i \|x_i - c_{C(i)}\|^2", font_size=32),
            cmath(r"C \text{ fixed}", r":", r"c_j = \text{the mean of cluster } j", font_size=30),
            cmath(r"c \text{ fixed}", r":", r"C(i) = \text{the nearest centre}", font_size=30),
            cmath(r"\text{each step}", r":", r"\text{the objective cannot increase}", font_size=30),
        ]
        rows[0][-1].set_color(MAPC)
        whys = [why(r"within-cluster sum of squares"), why(r"Lloyd (1957; \ published 1982)"),
                why(r"a Voronoi partition"), why(r"finite fixed point with consistent tie handling")]
        with self.voiceover(
            "<bookmark mark='a'/> Discriminant analysis needs the groups to be known. Clustering looks for groups "
            "nobody labelled. The k-means objective: choose k centres and an assignment of points to them to minimize"
            " the total squared distance from each point to its centre. <bookmark mark='b'/> Stuart Lloyd's "
            "algorithm, written at Bell Labs in 1957 and published only in 1982, alternates: with the assignment "
            "fixed, the best centres are the cluster means; <bookmark mark='c'/> with the centres fixed, the best "
            "assignment sends each point to its nearest centre. <bookmark mark='d'/> Neither step can increase the "
            "objective, so the algorithm stops, at a Lloyd fixed point with consistent tie handling, not necessarily "
            "the global optimum, which is why it is run from many starts."
        ) as vo:
            intro=label('K-means alternates nearest-center assignment and mean updates',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lloyd(self):
        d = load("lloyd")
        X2 = np.asarray(d["X2"])
        Cs, Ls, wss = np.asarray(d["centres"]), np.asarray(d["labels"]).astype(int), d["wss"]
        A = axes([0.5, 7.5], [-0.2, 2.8], x_length=7.4, y_length=4.8, xlabel=r"petal length (cm)", ylabel=r"petal width (cm)",
                 xticks=[1, 3, 5, 7], yticks=[0, 1, 2], center=[-2.1, 0.2, 0])
        ax = A.ax
        jit = np.random.default_rng(4).uniform(-0.03, 0.03, X2.shape)
        dots = VGroup(*[Dot(ax.c2p(*(v + j)), radius=0.05, color=GREY_B) for v, j in zip(X2, jit)])

        def crosses(C):
            return VGroup(*[VGroup(Line(ax.c2p(*c) + UL * 0.13, ax.c2p(*c) + DR * 0.13, stroke_width=6, color=KC[j]),
                                   Line(ax.c2p(*c) + UR * 0.13, ax.c2p(*c) + DL * 0.13, stroke_width=6, color=KC[j]))
                            for j, c in enumerate(C)])

        cr = crosses(Cs[0])
        it = label(r"start", font_size=24, color=GREY_A).move_to([4.6, 2.4, 0])
        w = label(rf"WSS {wss[0]:.0f}", font_size=24, color=MAPC).move_to([4.6, 1.8, 0])
        rows = fit_rows(VGroup(
            label(r"a bad start: \ two centres among the setosas", font_size=22),
            label(r"assign, \ move, \ repeat", font_size=22, color=MAPC),
            label(rf"{len(wss)} rounds; \ agreement with species: \ ARI {d['ari']:.2f}", font_size=22, color=PATH),
        ), 4.2, 0.42, [4.6, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Petal length and width again, this time without species labels, and a deliberately bad "
            "start: two of the three centres among the small setosa petals. <bookmark mark='b'/> Assign each flower to its "
            "nearest centre, move each centre to its cluster's mean, and repeat. The middle centre is pulled out of the "
            "setosas and up towards the versicolors, and the within-cluster sum of squares falls from three hundred and "
            "twenty-eight to thirty-one. <bookmark mark='c'/> After nine rounds nothing changes. The clusters match the "
            "species well, an adjusted Rand index of point eight nine, though nobody told the algorithm the species existed."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(cr), FadeIn(it), FadeIn(w), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), run_time=0.5)
            for t in range(len(Ls)):
                self.play(*[x.animate.set_color(KC[Ls[t][i]]) for i, x in enumerate(dots)],
                          Transform(it, label(rf"round {t + 1}: \ assign", font_size=24, color=GREY_A).move_to(it)),
                          Transform(w, label(rf"WSS {wss[t]:.1f}", font_size=24, color=MAPC).move_to(w)), run_time=0.7)
                if t + 1 < len(Cs):
                    self.play(Transform(cr, crosses(Cs[t + 1])),
                              Transform(it, label(rf"round {t + 1}: \ move", font_size=24, color=GREY_A).move_to(it)), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def hard_em(self):
        rows = [
            cmath(r"x \mid z = j", r"\sim", r"N(\mu_j, \Sigma_j), \ \ P(z = j) = \pi_j", font_size=30),
            cmath(r"\text{E-step}", r":", r"w_{ij} = P(z_i = j \mid x_i)", font_size=30),
            cmath(r"\text{M-step}", r":", r"\text{weighted means, \ covariances, \ proportions}", font_size=30),
            cmath(r"\Sigma_j = \sigma^2 I, \ \sigma \to 0", r":", r"w_{ij} \to \{0, 1\}: \ k\text{-means}", font_size=30),
        ]
        rows[3][-1].set_color(MAPC)
        whys = [why(r"a Gaussian mixture, \ Part 22"), why(r"soft assignments"), why(r"Dempster, Laird \& Rubin (1977)"),
                why(r"$k$-means is hard EM")]
        with self.voiceover(
            "<bookmark mark='a'/> A model makes the method clearer. Suppose each flower belongs to one of k unseen "
            "groups, each normal with its own mean and covariance: Part 22's Gaussian mixture. <bookmark mark='b'/> "
            "The E-step computes each point's probability of belonging to each group, <bookmark mark='c'/> and the "
            "M-step re-estimates the means, covariances and proportions with those weights. <bookmark mark='d'/> "
            "Force all covariances to be the same tiny sphere and the probabilities become zeros and ones: k-means is"
            " EM with hard assignments, as the zero-variance limit with positive fixed weights away from ties; "
            "classification EM at a fixed variance also retains assignment and weight terms."
        ) as vo:
            intro=label('A small-variance Gaussian-mixture limit produces hard assignments',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mixture(self):
        d = load("cluster")
        X2 = np.asarray(d["X2"])
        lab = np.asarray(d["gmm_labels"]).astype(int)
        mu, Sg = np.asarray(d["gmm_means2"]), np.asarray(d["gmm_covs2"])
        A = axes([0.5, 7.5], [-0.2, 2.8], x_length=7.4, y_length=4.8, xlabel=r"petal length (cm)", ylabel=r"petal width (cm)",
                 xticks=[1, 3, 5, 7], yticks=[0, 1, 2], center=[-2.1, 0.2, 0])
        ax = A.ax
        jit = np.random.default_rng(4).uniform(-0.03, 0.03, X2.shape)
        order = np.argsort(mu[:, 0])
        rank = {int(j): r for r, j in enumerate(order)}
        dots = VGroup(*[Dot(ax.c2p(*(v + j)), radius=0.05, color=KC[rank[k]]) for v, j, k in zip(X2, jit, lab)])
        ells = VGroup(*[ellipse(ax, mu[j], Sg[j], 2.0, KC[rank[j]], 2.5) for j in range(3)])
        rows = fit_rows(VGroup(
            label(r"three normal components, \ fitted by EM", font_size=22),
            label(r"ellipses: \ 2-SD contours, \ on the petals", font_size=22, color=MAPC),
            label(r"they lean and stretch; \ $k$-means cannot", font_size=22),
            label(rf"ARI: \ mixture {d['ari_gmm']:.2f}, \ $k$-means {d['ari_km']:.2f}", font_size=22, color=PATH),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A three-component normal mixture fitted by EM to all four measurements, shown on "
            "the petals. <bookmark mark='b'/> The ellipses are each component's two-standard-deviation contour. "
            "<bookmark mark='c'/> Unlike k-means, the components can lean and stretch, following the shape of each "
            "species. <bookmark mark='d'/> The adjusted Rand index against the true species, where one means perfect "
            "agreement and zero is the expectation under a fixed-margin random-partition reference, is point nine for"
            " the mixture and point seven three for k-means on the same four variables."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ells), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def compare(self):
        rows = [
            cmath(r"\mathrm{ARI}", r"=", r"\dfrac{\text{agreement} - E[\text{agreement}]}{\max - E[\text{agreement}]}", font_size=30),
            cmath(r"\text{labels}", r":", r"\text{arbitrary: \ only the partition matters}", font_size=30),
            cmath(r"1", r":", r"\text{the same partition}; \ \ 0: \ \text{chance}", font_size=30),
            cmath(r"\text{here}", r":", r"\text{an outside check we rarely have}", font_size=30),
        ]
        rows[0][-1].set_color(PATH)
        whys = [why(r"Hubert \& Arabie (1985)"), why(r"cluster 2 needn't be species 2"), why(r"corrected for chance"),
                why(r"the species were known all along")]
        with self.voiceover(
            "<bookmark mark='a'/> That index deserves a word. The adjusted Rand index of Lawrence Hubert and Phipps "
            "Arabie counts pairs of points that two partitions treat alike, corrected for the agreement expected by "
            "chance. <bookmark mark='b'/> Cluster labels are arbitrary, so it compares partitions, not names. "
            "<bookmark mark='c'/> One means the same partition, zero is chance-level expectation under that "
            "fixed-margin reference; negative values are possible. <bookmark mark='d'/> And we could only compute it "
            "because the species were known. In a real clustering problem there is no answer key."
        ) as vo:
            intro=label('Adjusted Rand agreement compares partitions under a chance reference',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def choose_k(self):
        d = load("cluster")
        bic = np.array([d["bic"][str(k)] for k in range(1, 7)])
        wss = np.array([d["wss"][str(k)] for k in range(1, 9)])
        A1 = axes([0.5, 8.5], [0, 720], x_length=5.4, y_length=3.8, xlabel=r"$k$", ylabel=r"$k$-means WSS",
                  xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[0, 300, 600], center=[-3.4, 0.5, 0])
        A2 = axes([0.5, 6.5], [540, 860], x_length=5.4, y_length=3.8, xlabel=r"$k$", ylabel=r"mixture BIC \ (lower is better)",
                  xticks=[1, 2, 3, 4, 5, 6], yticks=[600, 700, 800], center=[3.2, 0.5, 0])
        l1 = polyline(A1.ax, np.arange(1, 9), wss, MAPC, 3)
        p1 = VGroup(*[Dot(A1.ax.c2p(k + 1, v), radius=0.06, color=MAPC) for k, v in enumerate(wss)])
        l2 = polyline(A2.ax, np.arange(1, 7), bic, PATH, 3)
        p2 = VGroup(*[Dot(A2.ax.c2p(k + 1, v), radius=0.06, color=PATH) for k, v in enumerate(bic)])
        best = Circle(radius=0.18, color=RES, stroke_width=3).move_to(A2.ax.c2p(2, bic[1]))
        foot = fit_rows(VGroup(
            label(r"the WSS always falls: \ look for an elbow, \ at 2 or 3", font_size=22, color=MAPC),
            label(rf"BIC prefers $k = 2$ \ ({bic[1]:.0f} vs {bic[2]:.0f}): \ versicolor and virginica merge", font_size=22, color=RES),
            label(r"this regularized mixture BIC prefers two components; components are not species", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How many clusters? The k-means objective always falls as k grows, so one looks for "
            "an elbow, here at two or three. <bookmark mark='b'/> The fitted regularized mixture gives Part 28's BIC "
            "as a useful heuristic; mixture singularities limit its regular-model derivation. It is lowest at two, "
            "not three: versicolor and virginica overlap enough that one stretched component describes them about as "
            "well as two. <bookmark mark='c'/> There are three species, but this model and criterion prefer two "
            "components. That does not establish the true number of density modes or biological groups. A cluster is "
            "a region of high density, not a natural kind."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(p1), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(p2), Create(best), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"clustering always returns clusters, \ even from structureless data", font_size=24, color=RES),
            label(r"scaling the variables changes $k$-means's answer", font_size=24),
            label(r"other notions: \ hierarchical trees, \ density (DBSCAN), \ spectral", font_size=24, color=MAPC),
            label(r"is a cluster real? \ check it survives resampling \ (Part 16)", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cautions. K-means returns the requested partition even from structureless data; "
            "some density algorithms may instead label points as noise. <bookmark mark='b'/> Rescaling a variable "
            "changes k-means's answer, because it changes the distances. <bookmark mark='c'/> There are other notions"
            " of cluster: hierarchical trees that merge points step by step, density-based methods that find "
            "connected regions, and spectral methods that cut a similarity graph. <bookmark mark='d'/> Whether a "
            "cluster is real is a statistical question: at the least, check its resampling stability and relevance to"
            " the task. Stability alone does not prove a natural kind or a unique true partition."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def pitfalls(self):
        rows = [
            cmath(r"\Sigma_j", r"\to", r"\text{singular}: \ \text{likelihood} \to \infty", font_size=30),
            cmath(r"\text{labels}", r":", r"k! \text{ equivalent maxima}", font_size=30),
            cmath(r"\text{starts}", r":", r"\text{local maxima: \ run EM many times}", font_size=30),
            cmath(r"\text{cures}", r":", r"\text{floor the eigenvalues, \ or a prior}", font_size=30),
        ]
        rows[0][-1].set_color(RES)
        whys = [why(r"a component on one point"), why(r"label switching"), why(r"Part 22's EM, \ again"), why(r"regularize")]
        with self.voiceover(
            "<bookmark mark='a'/> Mixtures have pitfalls of their own. Put one component on a single point and shrink"
            " its covariance: the likelihood goes to infinity. The unconstrained global maximum does not exist. Our "
            "finite fits use a declared diagonal covariance ridge of one millionth; they are checked numerical local "
            "fits. <bookmark mark='b'/> Relabelling the components gives k factorial identical maxima, label "
            "switching, which matters for Bayesian mixtures. <bookmark mark='c'/> EM can settle at a stationary "
            "point, saddle or boundary behavior, so it is run from many starts, as k-means is. <bookmark mark='d'/> "
            "In practice the covariances are regularized or supplied with a suitable prior; the exact objective and "
            "convergence still need checking."
        ) as vo:
            intro=label('Unconstrained Gaussian mixture likelihoods can diverge',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
