from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Barycenters(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Barycenters: averaging distributions by moving them, not by mixing them.", 6,
                            r"Barycenters", r"The Fr\'echet mean of laws", lit=(2011,))
        self.definition()
        self.chart()
        self.numbers()
        self.gaussian()
        self.computing()
        self.theory()
        self.uses()

    def definition(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> How should one average several distributions? <bookmark mark='b'/> The obvious answer, "
            "the mixture, averages the densities: it is the barycenter in the L two sense, and it is multimodal when the "
            "laws are shifted. <bookmark mark='c'/> Maurice Fréchet's definition of a mean in any metric space suggests "
            "another: the law minimizing the weighted sum of squared Wasserstein distances. Martial Agueh and Guillaume "
            "Carlier studied it in 2011. <bookmark mark='d'/> On the line it is explicit: average the quantile functions.",
            [(r"\text{mixture}", r":", r"\bar f = \sum_k w_k f_k", 40),
             (r"\text{Wasserstein barycenter}", r":", r"\bar\mu = \arg\min_\mu \sum_k w_k W_2^2(\mu, \mu_k)", 40),
             (r"\text{Fr\'echet}", r":", r"\text{a mean in any metric space}", 40),
             (r"d = 1", r":", r"\bar F^{-1} = \sum_k w_k F_k^{-1}", 40)],
            [r"averages heights", r"Agueh \& Carlier (2011)", r"Fr\'echet (1948)", r"averages positions"],
            colors=[(1, PLANC), (3, PLANC)])

    def chart(self):
        d = load("bary")
        xs = np.asarray(d["xs"])
        dens, mix, bary = [np.asarray(v) for v in d["dens"]], np.asarray(d["mix"]), np.asarray(d["bary"])
        top = float(max(max(v.max() for v in dens), bary.max())) * 1.12
        A = axes([80, 200], [0, top], x_length=7.4, y_length=4.4, xlabel=r"systolic pressure (mm Hg)", ylabel=r"density",
                 xticks=[80, 110, 140, 170, 200], yticks=[0, 0.01, 0.02, 0.03], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = [SRC, FLOWC, TGT]
        gs = [curve(ax, xs, v, c, 2.5) for v, c in zip(dens, cols)]
        cm = curve(ax, xs, mix, NAIVEC2, 4)
        cb = VGroup(shade(ax, xs, bary, PLANC, 0.25), curve(ax, xs, bary, PLANC, 4))
        side = side_groups([
            [(rf"NHANES: \ ages {d['groups'][0]}, \ {d['groups'][1]}, \ {d['groups'][2]}", WHITE),
             (rf"means {d['means'][0]:.0f}, \ {d['means'][1]:.0f}, \ {d['means'][2]:.0f}", GREY_A)],
            [(rf"red: \ the mixture, \ sd {d['mix_sd']:.1f}", NAIVEC2)],
            [(rf"green: \ the $W_2$ barycenter, \ sd {d['bary_sd']:.1f}", PLANC), (r"a typical shape, \ at the average place", PLANC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> NHANES systolic pressure in three age groups, eighteen to thirty-nine, forty to fifty-nine, "
            f"and sixty to eighty, with means {d['means'][0]:.0f}, {d['means'][1]:.0f} and {d['means'][2]:.0f}. <bookmark "
            f"mark='b'/> Their mixture, weighted by group size, in red: wide, with standard deviation {say(d['mix_sd'], 1)}, "
            f"because it stacks three laws at three places. <bookmark mark='c'/> Their Wasserstein barycenter, in green, "
            f"averages the quantiles instead: one law, at the average place, with the groups' typical spread, standard "
            f"deviation {say(d['bary_sd'], 1)}. It describes a representative adult, where the mixture describes the whole "
            f"population."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES (CDC)")))
            vo.wait_until("a")
            self.play(*[Create(g) for g in gs], FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(cb), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def numbers(self):
        d = load("bary")
        sbar = float(np.sum(np.asarray(d["wts"]) * np.asarray(d["sds"])))
        self.lad_voiceover(
            f"<bookmark mark='a'/> On the line the barycenter's moments are simple. <bookmark mark='b'/> Its mean is the "
            f"weighted mean of the group means, {say(d['bary_mean'], 1)}, the same as the mixture's. <bookmark mark='c'/> If the "
            f"groups differed only in location and scale, its standard deviation would be the weighted average of theirs, "
            f"{say(sbar, 1)}; their shapes differ a little, and it is {say(d['bary_sd'], 1)}. Either way there is no "
            f"between-group term. <bookmark mark='d'/> The mixture's variance adds the spread of the means, which is why it is "
            f"{say(d['mix_sd'], 1)}: Part eight's decomposition of variance into within and between, with the Wasserstein "
            f"barycenter keeping only the within.",
            [(r"\text{mean}", r":", rf"\textstyle\sum_k w_k m_k = {d['bary_mean']:.1f}", 40),
             (r"\text{sd}", r":", rf"\approx \textstyle\sum_k w_k \sigma_k = {sbar:.1f}; \ \text{{here}} \ {d['bary_sd']:.1f}", 40),
             (r"\text{mixture variance}", r"=", r"\text{within} + \text{between}", 40),
             (r"\text{barycenter}", r":", r"\text{within only, \ at the average shape}", 40)],
            [r"both agree", r"location-scale family", r"Part 8", r"a different question"],
            colors=[(1, PLANC)])

    def gaussian(self):
        d = load("bary")
        S = np.asarray(d["gauss_bary"])
        self.lad_voiceover(
            f"<bookmark mark='a'/> In many dimensions there is no closed form, except for Gaussians. <bookmark mark='b'/> The "
            f"barycenter of centred Gaussians is Gaussian, with a covariance solving a matrix fixed-point equation. <bookmark "
            f"mark='c'/> Pedro Álvarez-Esteban and co-authors' iteration solves it in a few steps. <bookmark mark='d'/> For "
            f"two Gaussians with covariances diag one four and diag four one, the barycenter is {say(S[0][0], 2)} times the "
            f"identity, the square of the average standard deviation: round, not the arithmetic mean's diag two and a half, "
            f"two and a half, and not a cross.",
            [(r"\bar\Sigma", r"=", r"\sum_k w_k\big(\bar\Sigma^{1/2}\Sigma_k\bar\Sigma^{1/2}\big)^{1/2}", 40),
             (r"\text{iterate}", r":", r"\bar\Sigma \leftarrow \bar\Sigma^{-1/2}\big(\textstyle\sum_k w_k(\cdots)^{1/2}\big)^2\bar\Sigma^{-1/2}", 36),
             (r"\text{example}", r":", r"\mathrm{diag}(1, 4), \ \mathrm{diag}(4, 1)", 40),
             (r"\bar\Sigma", r"=", rf"{S[0][0]:.2f}\,I = \big(\tfrac{{1 + 2}}{{2}}\big)^2 I", 40)],
            [r"Agueh \& Carlier", r"\'Alvarez-Esteban et al. (2016)", r"two ellipses", r"the average shape"],
            colors=[(3, PLANC)])

    def uses(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Where barycenters are used. <bookmark mark='b'/> Averaging growth curves, or brain images, "
            "after aligning them: Part twenty-nine's registration problem, solved by transport. <bookmark mark='c'/> "
            "Combining posteriors computed on separate shards of data, by averaging them in Wasserstein space. <bookmark "
            "mark='d'/> Fair prediction: mapping each group's score distribution onto the barycenter removes the group "
            "difference with the least change to the scores, Part sixty-three's subject. <bookmark mark='e'/> And Victor "
            "Panaretos and Yoav Zemel's book treats distributions themselves as data points, with barycenters as their means.",
            [(r"uses of barycenters:", GREY_A),
             (r"averaging curves and images after alignment", PLANC),
             (r"combining posteriors from shards", ENTC),
             (r"fair scores: \ map each group to the barycenter \ (Part 63)", TGT),
             (r"distributions as data \ (Panaretos \& Zemel)", FLOWC)])

    def computing(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For general laws in several dimensions, barycenters are computed with chapter four's "
            "tools. <bookmark mark='b'/> Marco Cuturi and Arnaud Doucet's entropic barycenters, in 2014, iterate Sinkhorn "
            "scalings for all the laws at once, on a common grid. <bookmark mark='c'/> On free support, the barycenter can be "
            "represented by points that move, each step a weighted average of its transport partners. <bookmark mark='d'/> "
            "The entropy blurs the answer, so a debiased version, built like the Sinkhorn divergence, keeps it sharp.",
            [(r"\text{entropic}", r":", r"\min_\mu \sum_k w_k \mathrm{OT}_\varepsilon(\mu, \mu_k)", 40),
             (r"\text{fixed grid}", r":", r"\text{iterated Bregman projections}", 40),
             (r"\text{free support}", r":", r"x_i \leftarrow \sum_k w_k T_k(x_i)", 40),
             (r"\text{blur}", r":", r"\text{debias, \ as for } S_\varepsilon", 40)],
            [r"Cuturi \& Doucet (2014)", r"Benamou et al. (2015)", r"a fixed-point step", r"Janati et al. (2020)"],
            colors=[(0, ENTC)])

    def theory(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The statistics of barycenters. <bookmark mark='b'/> If the k laws are themselves a random "
            "sample from a population of laws, the barycenter of the sample estimates a population Fréchet mean. Thibaut Le "
            "Gouic and Jean-Michel Loubes proved consistency in 2017. <bookmark mark='c'/> Rates depend on the curvature of "
            "Wasserstein space, which is nonnegative, unlike the spaces where Fréchet means behave best. <bookmark mark='d'/> "
            "On the line the space is flat, and the barycenter is just an average of quantile functions: the root k rate of "
            "Part six's law of large numbers.",
            [(r"\text{laws as data}", r":", r"\mu_1, \dots, \mu_k \sim \mathbb P \text{ on } \mathcal P_2", 40),
             (r"\text{consistency}", r":", r"\hat{\bar\mu}_k \to \bar\mu", 40),
             (r"\text{curvature}", r":", r"\text{nonnegative: \ rates need extra conditions}", 40),
             (r"d = 1", r":", r"\text{flat; \ the } \sqrt k \text{ rate}", 40)],
            [r"Panaretos \& Zemel", r"Le Gouic \& Loubes (2017)", r"Ahidar-Coutrix et al. (2020)", r"Part 6"],
            colors=[(1, PLANC)])
