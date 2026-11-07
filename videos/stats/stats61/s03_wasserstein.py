from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Wasserstein(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter two. Wasserstein distances: a geometry on probability distributions.", 2,
                            r"Wasserstein distances", r"Distance, \ geodesics, \ curvature", lit=(1969,))
        self.metric()
        self.kr()
        self.compare()
        self.bmi_chart()
        self.decompose()
        self.gaussians()
        self.geodesic_chart()
        self.mccann()

    def metric(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For p at least one, Wasserstein distance is the p-th root of the minimum p-power transport cost. <bookmark mark='b'/> It is a metric on laws with finite p-th moments. A gluing construction proves its triangle inequality. <bookmark mark='c'/> Convergence is equivalent to weak convergence together with convergence of p-th moments in Euclidean space. <bookmark mark='d'/> For such laws it can be finite across disjoint supports and quantify geometric separation. Total variation is also finite there, but does not measure that separation.",
            [(r"W_p(\mu, \nu)", r"=", r"\inf_{\pi \in \Pi(\mu, \nu)} \big(E_\pi\|X - Y\|^p\big)^{1/p}", 40),
             (r"\text{a metric}", r":", r"\text{on } \mathcal P_p(\mathbb R^d); \ \text{triangle by gluing}", 40),
             (r"W_p(\mu_n, \mu) \to 0", r"\iff", r"\mu_n \Rightarrow \mu \ \text{and} \ \textstyle\int\|x\|^p d\mu_n \to \int\|x\|^p d\mu", 34),
             (r"\text{disjoint supports}", r":", r"\text{finite, \ and geometric}", 40)],
            [r"Vaserstein (1969)", r"the gluing lemma", r"Part 43's weak convergence", r"unlike TV and KL"],
            colors=[(0, PLANC)])

    def kr(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For p equal to one, duality takes a special form, from Kantorovich and Gennadii "
            "Rubinstein in 1958. <bookmark mark='b'/> W one is the largest difference in expectations over all functions "
            "that are one-Lipschitz. <bookmark mark='c'/> That makes it an integral probability metric, like Part sixty's "
            "maximum mean discrepancy, but with Lipschitz functions instead of a kernel's unit ball. <bookmark mark='d'/> "
            "Chapter nine's Wasserstein GAN trains a neural network to approximate the best such function.",
            [(r"\text{Kantorovich--Rubinstein}", r":", r"W_1(\mu, \nu) = \sup_{\mathrm{Lip}(f) \le 1} E_\mu f - E_\nu f", 38),
             (r"\text{the witness}", r":", r"\text{a 1-Lipschitz } f", 40),
             (r"\text{an IPM}", r":", r"\text{like the MMD, \ another function class}", 40),
             (r"\text{WGAN}", r":", r"f \text{ a neural network}", 40)],
            [r"Kantorovich \& Rubinstein (1958)", r"the dual potential", r"Part 60", r"chapter 9"],
            colors=[(0, PLANC)])

    def bmi_chart(self):
        d = load("quantile")
        xs, Fm, Fw = np.asarray(d["xs"]), np.asarray(d["Fm"]), np.asarray(d["Fw"])
        A = axes([float(xs.min()), float(xs.max())], [0, 1.02], x_length=7.4, y_length=4.4, xlabel=r"body-mass index", ylabel=r"cumulative fraction",
                 xticks=[20, 30, 40, 50, 60], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cm, cw = curve(ax, xs, Fm, SRC, 3.5), curve(ax, xs, Fw, TGT, 3.5)
        pts = [ax.c2p(x, y) for x, y in zip(xs, Fm)] + [ax.c2p(x, y) for x, y in zip(xs[::-1], Fw[::-1])]
        area = Polygon(*pts, stroke_width=0, fill_color=PLANC, fill_opacity=0.45)
        side = side_groups([
            [(rf"NHANES: \ {d['n_m']:,} men \ (blue)", SRC), (rf"{d['n_w']:,} women \ (gold)", TGT)],
            [(rf"means {d['mean_m']:.2f} \ and \ {d['mean_w']:.2f}", GREY_A), (rf"sds {d['sd_m']:.2f} \ and \ {d['sd_w']:.2f}", GREY_A)],
            [(rf"green area $= W_1 = {d['w1']:.2f}$", PLANC)],
            [(rf"$W_2 = {d['w2']:.2f}$", PLANC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the body-mass index of {d['n_m']:,} men and {d['n_w']:,} women in NHANES, as two "
            f"cumulative distribution functions. <bookmark mark='b'/> Their means differ by less than one unit, "
            f"{say(d['mean_m'], 1)} against {say(d['mean_w'], 1)}, but the women's distribution is more spread out. "
            f"<bookmark mark='c'/> The green area between the curves is W one: {say(d['w1'], 2)} units of body-mass index. "
            f"It is the average distance each person's index would have to move, under the quantile matching, to turn one "
            f"distribution into the other. <bookmark mark='d'/> W two, which weights large moves more heavily, is "
            f"{say(d['w2'], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"NHANES unweighted empirical extract (CDC)")))
            vo.wait_until("a")
            self.play(Create(cm), Create(cw), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(area), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def decompose(self):
        d = load("quantile")
        dm2 = (d["mean_m"] - d["mean_w"]) ** 2
        ds2 = (d["sd_m"] - d["sd_w"]) ** 2
        self.lad_voiceover(
            f"<bookmark mark='a'/> In one dimension, the squared W two splits into three parts. <bookmark mark='b'/> The "
            f"squared difference in means: here {say(dm2, 2)}. <bookmark mark='c'/> The squared difference in standard "
            f"deviations: {say(ds2, 2)}, the largest part. <bookmark mark='d'/> And a shape term, from how far the "
            f"standardized quantile functions differ: {say(d['shape_term'], 2)}, since their correlation is "
            f"{say(d['rho'], 4)}. The sum matches the squared distance, {say(d['w2'] ** 2, 2)}, using exact integration of the empirical step quantiles: these two extract distributions differ mostly "
            f"in spread, not in centre or shape.",
            [(r"W_2^2", r"=", r"(\mu_1 - \mu_2)^2 + (\sigma_1 - \sigma_2)^2 + 2\sigma_1\sigma_2(1 - \rho)", 36),
             (r"\text{location}", r":", rf"{dm2:.2f}", 40),
             (r"\text{spread}", r":", rf"{ds2:.2f}", 40),
             (r"\text{shape}", r":", rf"{d['shape_term']:.2f}; \ \ \text{{total}} \ {d['w2'] ** 2:.2f}", 40)],
            [r"$\rho$: \ quantile correlation", r"means", r"standard deviations", r"a classical identity"],
            colors=[(2, PLANC)])

    def gaussians(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> For Gaussians, the distance has a closed form. <bookmark mark='b'/> W two squared is the "
            "squared distance between the means, plus the Bures distance between the covariance matrices. <bookmark "
            "mark='c'/> For positive-definite covariances, the optimal map is affine with a symmetric positive linear part, the unique one that pushes the first "
            "covariance onto the second. <bookmark mark='d'/> For commuting covariances it is just the ratio of standard "
            "deviations along each axis; in general its principal axes need not match the axes of either covariance. Its symmetric positive linear part has no separate rotation factor.",
            [(r"W_2^2", r"=", r"\|m_1 - m_2\|^2 + \mathcal B^2(\Sigma_1, \Sigma_2)", 40),
             (r"\mathcal B^2", r"=", r"\mathrm{tr}\big(\Sigma_1 + \Sigma_2 - 2(\Sigma_1^{1/2}\Sigma_2\Sigma_1^{1/2})^{1/2}\big)", 36),
             (r"T(x)", r"=", r"m_2 + A(x - m_1), \ \ A\Sigma_1A = \Sigma_2, \ A \succ 0", 38),
             (r"\text{commuting}", r":", r"A = \Sigma_2^{1/2}\Sigma_1^{-1/2}", 40)],
            [r"Dowson \& Landau; \ Olkin \& Pukelsheim (1982)", r"the Bures metric", r"a linear Brenier map", r"axis by axis"],
            colors=[(0, PLANC)])

    def geodesic_chart(self):
        d = load("geodesic")
        X, Y, perm = np.asarray(d["X"]), np.asarray(d["Y"]), np.asarray(d["perm"], int)
        A = axes([-4.4, 2.6], [-2.4, 4.0], x_length=6.6, y_length=5.4, xlabel=r"", ylabel=r"", center=[-2.6, -0.1, 0])
        ax = A.ax
        tf = TransportFlow(ax, X, Y, perm)
        c0 = tf.cloud(0.0, SRC, 0.04)
        paths = tf.paths(GREY_B, 0.8, 0.25, every=3)
        tgt = VGroup(*[Dot(ax.c2p(*y), radius=0.035, color=TGT, fill_opacity=0.5) for y in Y])
        side = side_groups([
            [(r"blue: \ a Gaussian cloud, \ 272 points", SRC), (r"gold: \ Old Faithful, \ standardized", TGT)],
            [(r"the optimal matching:", PLANC), (rf"mean squared move {d['cost']:.2f}", PLANC), (rf"a random matching: \ {d['cost_rand']:.2f}", NAIVEC2)],
            [(r"McCann's interpolation:", FLOWC), (r"$x_t = (1 - t)x + tT(x)$", FLOWC)],
            [(r"each midpoint is a law;", GREY_A), (r"the mixture would fade instead", GREY_A)],
        ], width=4.6, pos=(4.3, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> The part's instrument, the transport flow. A Gaussian cloud of two hundred and seventy-two "
            f"points, in blue, and Old Faithful's eruptions, standardized, in gold. <bookmark mark='b'/> The optimal "
            f"assignment matches each blue point to one gold point; the grey segments show every third pair. The mean "
            f"squared move is {say(d['cost'], 2)}, against {say(d['cost_rand'], 2)} for a random matching. <bookmark "
            f"mark='c'/> Now move every point along its segment at constant speed. <bookmark mark='d'/> Each intermediate "
            f"cloud is a distribution in its own right, a point on the Wasserstein geodesic. The cloud travels and reshapes, "
            f"splitting into Old Faithful's two clusters, where the straight mixture of the two laws would only fade one out "
            f"and fade the other in."
        ) as vo:
            self.play(FadeIn(A), FadeIn(c0), FadeIn(tgt), FadeIn(museum_tag(r"Old Faithful; \ Azzalini \& Bowman (1990)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(paths), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeOut(paths))
            for t in (0.25, 0.5, 0.75, 1.0):
                self.play(Transform(c0, tf.cloud(t, SRC if t < 1 else PLANC, 0.04)), run_time=1.6, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def mccann(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Robert McCann's displacement interpolation, in 1997, gives the space of distributions a "
            "geometry. <bookmark mark='b'/> Its geodesics are the clouds in transit; the distance along one grows linearly in "
            "t. <bookmark mark='c'/> A functional that is convex along these paths, displacement convexity, can be "
            "non-convex in the usual sense: negative differential entropy is an example; interaction energies require appropriate convexity conditions. <bookmark "
            "mark='d'/> Felix Otto's calculus, in 2001, adds gradients and Hessians, and turns some partial differential "
            "equations into gradient flows: chapter eight.",
            [(r"\mu_t", r"=", r"\big((1 - t)\,\mathrm{id} + tT\big)_\#\mu", 40),
             (r"W_2(\mu_s, \mu_t)", r"=", r"|t - s|\,W_2(\mu_0, \mu_1)", 40),
             (r"\text{displacement convex}", r":", r"t \mapsto \mathcal F(\mu_t) \text{ convex}", 40),
             (r"\text{Otto}", r":", r"\text{a Riemannian calculus on } \mathcal P_2", 40)],
            [r"McCann (1997)", r"constant speed", r"entropy is one", r"chapter 8"],
            colors=[(0, FLOWC)])

    def compare(self):
        self.list_voiceover(
            "<bookmark mark='a'/> These discrepancies answer different questions. <bookmark mark='b'/> Total variation and Hellinger reach their maximum for mutually singular probability laws, regardless of geometric separation. They remain finite. <bookmark mark='c'/> KL is infinite when the first law is not absolutely continuous with respect to the second; merely having different supports is not sufficient for infinity in both directions. <bookmark mark='d'/> MMD uses a kernel and has root-n empirical-error bounds for bounded fixed kernels, with kernel-dependent sensitivity. <bookmark mark='e'/> Wasserstein uses the ground distance, with sampling rates depending on dimension, moments, order and regularity.",
            [('Comparing Wasserstein distance with earlier metrics', GREY_A),
             (r"TV, \ Hellinger: \ pointwise, \ blind to distance \ (Part 50)", NAIVEC2),
             (r"KL: \ infinite without the needed absolute continuity \ (Part 22)", NAIVEC2),
             (r"MMD: \ geometry by a kernel, \ $n^{-1/2}$ \ (Part 60)", ENTC),
             (r"$W_p$: \ geometry by cost; \ rates depend on order, dimension and tails", PLANC)], head_size=36)
