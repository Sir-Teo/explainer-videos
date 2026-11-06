from __future__ import annotations

import numpy as np

from videos.stats.stats61.common import *  # noqa: F403


class Maps(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. Estimating transport maps: not just how far, but where each point should go.", 5,
                            r"Estimating transport maps", r"From samples to a function", lit=(2021,))
        self.problem()
        self.minimax()
        self.regularity()
        self.estimators()
        self.semidiscrete()
        self.chart()
        self.uses()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Often the map matters more than the distance. A cell biologist with snapshots of a tissue "
            "at two times wants to know where each cell went; a survey statistician wants to adjust one population's "
            "covariates to look like another's. <bookmark mark='b'/> From n points of mu and n of nu, estimate the Brenier "
            "map T, the gradient of a convex function pushing mu onto nu. <bookmark mark='c'/> The loss is the mean squared "
            "error of the map under mu. <bookmark mark='d'/> Geoffrey Schiebinger and co-authors' Waddington-OT, in 2019, "
            "used entropic maps to trace cells through development.",
            [(r"\text{why maps}", r":", r"\text{trajectories, \ adjustments, \ couplings of data}", 38),
             (r"\text{target}", r":", r"T = \nabla\varphi, \ \ T_\#\mu = \nu", 40),
             (r"\text{loss}", r":", r"\int \|\hat T(x) - T(x)\|^2\,d\mu(x)", 40),
             (r"\text{example}", r":", r"\text{cells through development}", 40)],
            [r"where things go", r"Brenier", r"the $L^2(\mu)$ risk", r"Schiebinger et al. (2019)"],
            colors=[(1, PLANC)])

    def minimax(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Jan-Christian Hütter and Philippe Rigollet found the minimax rate in 2021. <bookmark "
            "mark='b'/> If the map has alpha derivatives, the best possible squared error is n to the minus two alpha over "
            "two alpha minus two plus d, up to logarithms: <bookmark mark='c'/> the rate of nonparametric regression for a "
            "function with one more derivative, as if the map's potential were being estimated. <bookmark mark='d'/> Smooth "
            "maps defeat the curse in a way the distance itself cannot: with alpha large, the rate approaches one over n.",
            [(r"\text{minimax}", r":", r"\inf_{\hat T}\sup_T E\|\hat T - T\|^2_{L^2(\mu)}", 40),
             (r"\text{rate}", r"\asymp", r"n^{-2\alpha/(2\alpha - 2 + d)} \ \text{(up to logs)}", 40),
             (r"\text{like}", r":", r"\text{regression of a function with } \alpha \text{ derivatives}", 38),
             (r"\alpha \to \infty", r":", r"\to n^{-1}", 40)],
            [r'H\"utter \& Rigollet (2021)', r"smoothness $\alpha$", r"Part 29's rates", r"smoothness helps"],
            colors=[(1, PLANC)])

    def estimators(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two estimators. <bookmark mark='b'/> The empirical map: solve the assignment between the "
            "two samples, and extend it to new points by sending each to the partner of its nearest sample point. It is a "
            "step function, and it inherits the curse. <bookmark mark='c'/> The entropic map, from Aram-Alexandre Pooladian "
            "and Jonathan Niles-Weed in 2021: the barycentric projection of the Sinkhorn plan, a soft average of target "
            "points weighted by the dual potential. <bookmark mark='d'/> It is smooth, defined everywhere, computed in a "
            "few Sinkhorn iterations, and with epsilon shrinking as n grows it is near minimax for smooth maps.",
            [(r"\text{empirical}", r":", r"\hat T(x) = y_{\sigma(\mathrm{nn}(x))}", 40),
             (r"\text{entropic}", r":", r"\hat T_\varepsilon(x) = \frac{\sum_j y_j e^{(g_j - \|x - y_j\|^2/2)/\varepsilon}}{\sum_j e^{(g_j - \|x - y_j\|^2/2)/\varepsilon}}", 32),
             (r"\text{properties}", r":", r"\text{smooth, \ fast, \ near minimax}", 40),
             (r"\varepsilon", r"\asymp", r"n^{-1/(d' + 4)} \ \text{or similar}", 40)],
            [r"a nearest-neighbour step", r"Pooladian \& Niles-Weed (2021)", r"Sinkhorn's dual", r"a tuning rate"],
            colors=[(1, ENTC)])

    def chart(self):
        d = load("maps")
        ns = np.asarray(d["ns"], float)
        A = axes([1.6, 3.0], [-1.25, 0.1], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ (log scale)", ylabel=r"$\|\hat T - T\|^2_{L^2(\mu)}$",
                 xticks=[np.log10(v) for v in (50, 100, 200, 400, 800)], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[np.log10(v) for v in (0.1, 0.3, 1)], yfmt=lambda v: f"{10 ** v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.log10(ns)
        le = VGroup(polyline(ax, xs, np.log10(d["emp"]), NAIVEC2, 3.5), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=NAIVEC2) for a, b in zip(xs, d["emp"])])
        lt = VGroup(polyline(ax, xs, np.log10(d["ent"]), ENTC, 3.5), *[Dot(ax.c2p(a, np.log10(b)), radius=0.06, color=ENTC) for a, b in zip(xs, d["ent"])])
        A_ = np.asarray(d["A"])
        side = side_groups([
            [(r"$N(0, I_2) \to N(0, \Sigma)$", WHITE), (rf"true map: \ $x \mapsto Ax$", GREY_A)],
            [(r"red: \ empirical map", NAIVEC2), (rf"slope {d['slope_emp']:.2f}", NAIVEC2)],
            [(r"purple: \ entropic map", ENTC), (rf"slope {d['slope_ent']:.2f}", ENTC), (rf"{d['ent'][-1]:.3f} vs {d['emp'][-1]:.3f} at 800", ENTC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A test where the truth is known: the standard Gaussian in the plane pushed to a correlated "
            f"Gaussian, whose Brenier map is linear. <bookmark mark='b'/> The empirical map's squared error falls with slope "
            f"{say(d['slope_emp'], 2)}. <bookmark mark='c'/> The entropic map, with epsilon shrinking like n to the minus a "
            f"third, falls with slope {say(d['slope_ent'], 2)}, and is lower at every n: {say(d['ent'][-1], 3)} against "
            f"{say(d['emp'][-1], 3)} at eight hundred points. Smoothing pays, because the true map is smooth."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 4 repetitions, \ 500 test points")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(le), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lt), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def uses(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Where estimated maps are used. <bookmark mark='b'/> Single-cell biology: trajectories from "
            "snapshots, since a cell can be measured only once. <bookmark mark='c'/> Domain adaptation, as in Part sixty: "
            "map the source covariates onto the target's, and train there. <bookmark mark='d'/> Counterfactual and causal "
            "questions, by transporting a treated population onto a control one. <bookmark mark='e'/> And chapter seven: "
            "the map to a reference law is a multivariate rank.",
            [(r"uses of estimated maps:", GREY_A),
             (r"single-cell trajectories \ (Waddington-OT)", PLANC),
             (r"domain adaptation \ (Part 60)", TGT),
             (r"transporting populations \ (Part 62)", FLOWC),
             (r"ranks and quantiles \ (chapter 7)", ENTC)])

    def semidiscrete(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Between the continuous and the discrete lies the semi-discrete problem: a law with a "
            "density, transported onto n points. <bookmark mark='b'/> The dual has one number per target point, g j, and the "
            "map sends x to the target point that minimizes the cost minus g j. <bookmark mark='c'/> So space is cut into n "
            "convex cells, Laguerre cells, one per target, each holding exactly that target's mass. <bookmark mark='d'/> "
            "Finding the g j is a smooth concave maximization, solved by Newton's method: Quentin Mérigot's and Bruno "
            "Lévy's algorithms compute such maps in three dimensions with millions of cells.",
            [(r"\text{semi-discrete}", r":", r"\mu \text{ a density}, \ \nu = \textstyle\sum_j b_j\delta_{y_j}", 40),
             (r"T(x)", r"=", r"y_{j^*(x)}, \ \ j^*(x) = \arg\min_j \tfrac12\|x - y_j\|^2 - g_j", 40),
             (r"\text{cells}", r":", r"\text{Laguerre cells, \ } \mu(\text{cell}_j) = b_j", 40),
             (r"\text{solve}", r":", r"\text{Newton on a concave dual}", 40)],
            [r"a mixed problem", r"the dual potential", r"power diagrams", r"M\'erigot; \ L\'evy"],
            colors=[(1, PLANC)])

    def regularity(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Rates need the true map to be smooth, so when is it? <bookmark mark='b'/> The potential "
            "solves a Monge–Ampère equation: the determinant of its Hessian equals the ratio of the two densities, composed "
            "with the map. <bookmark mark='c'/> Luis Caffarelli proved in the 1990s that if both densities are bounded above "
            "and below on convex sets, the map is Hölder continuous, and smoother if the densities are. <bookmark mark='d'/> "
            "Without convexity of the target's support, the map can be discontinuous: transporting a disc onto two separate "
            "discs must tear it somewhere.",
            [(r"\text{Monge--Amp\`ere}", r":", r"\det\nabla^2\varphi(x) = p(x)/q(\nabla\varphi(x))", 40),
             (r"\text{Caffarelli}", r":", r"\text{convex supports, \ bounded densities} \Rightarrow C^{0, \alpha}", 38),
             (r"\text{smoother data}", r":", r"\text{smoother maps}", 40),
             (r"\text{non-convex target}", r":", r"\text{the map can tear}", 40)],
            [r"a fully nonlinear PDE", r"Caffarelli (1992)", r"elliptic regularity", r"Old Faithful's two clusters"],
            colors=[(1, PLANC), (3, NAIVEC2)])
