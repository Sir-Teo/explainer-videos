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
            "at two times models plausible couplings between snapshots, without identifying individual cell lineages from marginals alone; a survey statistician wants to adjust one population's "
            "covariates to look like another's. <bookmark mark='b'/> From n points of mu and n of nu, estimate the Brenier "
            "map T, the gradient of a convex function pushing mu onto nu. <bookmark mark='c'/> The loss is the mean squared "
            "error of the map under mu. <bookmark mark='d'/> Geoffrey Schiebinger and co-authors' Waddington-OT, in 2019, "
            "used growth-aware unbalanced transport to model developmental couplings; this is not direct observation of each cell trajectory.",
            [(r"\text{why maps}", r":", r"\text{trajectories, \ adjustments, \ couplings of data}", 38),
             (r"\text{target}", r":", r"T = \nabla\varphi, \ \ T_\#\mu = \nu", 40),
             (r"\text{loss}", r":", r"\int \|\hat T(x) - T(x)\|^2\,d\mu(x)", 40),
             (r"\text{example}", r":", r"\text{cells through development}", 40)],
            [r"where things go", r"Brenier", r"the $L^2(\mu)$ risk", r"Schiebinger et al. (2019)"],
            colors=[(1, PLANC)])

    def minimax(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Hutter and Rigollet derive minimax rates for a specified smooth transport-map class. <bookmark mark='b'/> Under bounded support and density, smoothness and Hessian conditions, squared-map risk has the displayed nonparametric term, together with a parametric one-over-n floor, up to logarithmic factors. Alpha describes map smoothness. <bookmark mark='c'/> The denominator differs from ordinary nonparametric regression because observations are unpaired marginals and the convex potential links them. This is not simply the usual regression formula with one extra derivative. <bookmark mark='d'/> Sufficient smoothness brings the rate near the parametric floor, under the theorem's remaining assumptions.",
            [(r"\text{minimax}", r":", r"\inf_{\hat T}\sup_T E\|\hat T - T\|^2_{L^2(\mu)}", 40),
             (r"\text{rate}", r"\asymp", r"n^{-1}\vee n^{-2\alpha/(2\alpha-2+d)}\quad\text{(up to logs; stated model)}", 40),
             (r"\text{like}", r":", r"\text{unpaired marginals + a smooth convex potential}", 38),
             (r"\alpha \to \infty", r":", r"\to n^{-1}", 40)],
            [r'H\"utter \& Rigollet (2021)', r"smoothness $\alpha$", r"Part 29's rates", r"smoothness helps"],
            colors=[(1, PLANC)])

    def estimators(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> We compare two finite-sample map estimators. <bookmark mark='b'/> The first matches two samples and extends each match by nearest source neighbor. It is one particular step-function extension. <bookmark mark='c'/> The entropic estimator uses the barycentric projection of the entropic plan and its target potential to define a smooth out-of-sample function. <bookmark mark='d'/> Statistical rates require specific smoothness and support conditions and a compatible epsilon schedule. They are not a blanket near-minimax guarantee for every smooth map. Our Gaussian simulation uses a heuristic half n-to-minus-one-third schedule and explicitly checks Sinkhorn convergence.",
            [(r"\text{empirical}", r":", r"\hat T(x) = y_{\sigma(\mathrm{nn}(x))}", 40),
             (r"\text{entropic}", r":", r"\hat T_\varepsilon(x) = \frac{\sum_j y_j e^{(g_j - \|x - y_j\|^2/2)/\varepsilon}}{\sum_j e^{(g_j - \|x - y_j\|^2/2)/\varepsilon}}", 32),
             (r"\text{properties}", r":", r"\text{smooth extension; \ solver and statistical error both matter}", 40),
             (r"\varepsilon", r"\asymp", r"\text{theorem-specific; simulation: }0.5n^{-1/3}", 40)],
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
            f"third, falls with slope {say(d['slope_ent'], 2)}, and has lower mean error at these tested sizes: {say(d['ent'][-1], 3)} against "
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
            [('Statistical applications of estimated transport maps', GREY_A),
             (r"single-cell trajectories \ (Waddington-OT)", PLANC),
             (r"domain adaptation \ (Part 60)", TGT),
             (r"transporting populations \ (Part 62)", FLOWC),
             (r"ranks and quantiles \ (chapter 7)", ENTC)], head_size=36)

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
