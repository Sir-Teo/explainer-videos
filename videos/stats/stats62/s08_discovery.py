from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Discovery(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. Causal discovery: can the graph itself be learned from data?", 7,
                            r"Causal discovery", r"What data can say about arrows", lit=(2018,))
        self.pc()
        self.equivalence()
        self.faithfulness()
        self.restrictions()
        self.notears()
        self.interventions()
        self.chart()
        self.lessons()

    def pc(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Every chapter so far took the graph as given. Peter Spirtes and Clark Glymour's PC "
            "algorithm, from 1991, learns it from conditional independences. <bookmark mark='b'/> Start with every pair "
            "joined. Remove an edge between two variables as soon as some set of their neighbours makes them independent. "
            "<bookmark mark='c'/> Then orient the colliders: if X and Z are not adjacent, both are adjacent to Y, and Y was "
            "not in the set that separated them, the pattern is X into Y out of Z. <bookmark mark='d'/> Under faithfulness, "
            "and with correct tests, it recovers what can be recovered.",
            [(r"\text{skeleton}", r":", r"\text{remove } i - j \text{ if } X_i \perp X_j \mid X_S \text{ for some } S", 38),
             (r"\text{tests}", r":", r"\text{Fisher's } z \text{ on partial correlations}", 40),
             (r"\text{colliders}", r":", r"X - Y - Z, \ Y \notin S_{XZ} \Rightarrow X \to Y \leftarrow Z", 40),
             (r"\text{guarantee}", r":", r"\text{under faithfulness, \ correct tests}", 40)],
            [r"Spirtes \& Glymour (1991)", r"Part 31's partial correlations", r"v-structures", r"consistency"],
            colors=[(0, IDC)])

    def equivalence(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What can be recovered is less than the graph. <bookmark mark='b'/> X into Y into Z, X out "
            "of Y out of Z, and Y into both X and Z imply the same independences: X independent of Z given Y. <bookmark "
            "mark='c'/> They form a Markov equivalence class, and observational data cannot choose among them. <bookmark "
            "mark='d'/> Only the collider X into Y out of Z differs, which is why colliders orient edges. The output of PC "
            "is a partially directed graph: some arrows, some undirected edges.",
            [(r"X \to Y \to Z", r",", r"X \leftarrow Y \leftarrow Z, \ \ X \leftarrow Y \to Z", 40),
             (r"\text{all imply}", r":", r"X \perp Z \mid Y", 40),
             (r"\text{so}", r":", r"\text{a Markov equivalence class}", 40),
             (r"\text{output}", r":", r"\text{a CPDAG: \ some edges undirected}", 40)],
            [r"three chains and a fork", r"same independences", r"Verma \& Pearl (1990)", r"identifiable up to a class"],
            colors=[(2, HIDC)])

    def faithfulness(self):
        d = load("discovery")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Faithfulness assumes that every independence in the data comes from the graph, not from "
            f"coincidences of parameters. <bookmark mark='b'/> A coincidence: X affects Y directly with weight one, and "
            f"through M with weight one times minus one. The paths cancel. <bookmark mark='c'/> In five thousand simulated "
            f"units the correlation of X and Y is {say(d['cancel_corr'], 3)}: PC would remove the edge X to Y. <bookmark "
            f"mark='d'/> Exact cancellation has probability zero, but Caroline Uhler, Garvesh Raskutti, Peter Bühlmann and "
            f"Bin Yu showed in 2013 that near-cancellation, which ruins finite-sample tests, is common: strong faithfulness "
            f"fails for a large fraction of graphs.",
            [(r"\text{faithfulness}", r":", r"\text{independences come only from the graph}", 40),
             (r"\text{cancellation}", r":", r"X \to Y \ (+1), \ \ X \to M \to Y \ (+1 \times -1)", 40),
             (r"\text{here}", r":", rf"\mathrm{{corr}}(X, Y) = {d['cancel_corr']:.3f}", 40),
             (r"\text{near-cancellation}", r":", r"\text{common; \ strong faithfulness fails often}", 38)],
            [r"an assumption", r"a coincidence", r"the edge is lost", r"Uhler et al. (2013)"],
            colors=[(2, NAIVEC), (3, NAIVEC)])

    def restrictions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Within an equivalence class, more structure can orient every edge. <bookmark mark='b'/> "
            "Shohei Shimizu and co-authors' LiNGAM, in 2006: in linear models with non-Gaussian noise, the direction is "
            "identified, because only in the causal direction is the residual independent of the regressor. <bookmark "
            "mark='c'/> Patrik Hoyer and co-authors' additive noise models extend this to nonlinear functions. <bookmark "
            "mark='d'/> And with equal noise variances, Jonas Peters and Bühlmann showed, even linear Gaussian models are "
            "identified. Each is an assumption, and each is untestable from the class alone.",
            [(r"\text{LiNGAM}", r":", r"\text{linear, \ non-Gaussian noise} \Rightarrow \text{identified}", 40),
             (r"\text{ANM}", r":", r"Y = f(X) + N, \ N \perp X", 40),
             (r"\text{equal variances}", r":", r"\text{Gaussian, \ still identified}", 40),
             (r"\text{but}", r":", r"\text{each restriction is an assumption}", 40)],
            [r"Shimizu et al. (2006)", r"Hoyer et al. (2009)", r"Peters \& B\"uhlmann (2014)", r"no free arrows"],
            colors=[(0, IDC)])

    def notears(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Searching over graphs is combinatorial. Xun Zheng and co-authors' NOTEARS, in 2018, "
            "turned it into continuous optimization. <bookmark mark='b'/> A weighted adjacency matrix W is acyclic exactly "
            "when the trace of the matrix exponential of W squared, elementwise, equals the dimension. <bookmark mark='c'/> "
            "So minimize least squares plus a sparsity penalty, subject to that smooth constraint, by gradient methods. "
            "<bookmark mark='d'/> It performed impressively on standard benchmarks, which turned out to contain a shortcut.",
            [(r"\text{acyclicity}", r":", r"\mathrm{tr}\,e^{W \circ W} - d = 0", 40),
             (r"\text{NOTEARS}", r":", r"\min_W \tfrac{1}{2n}\|X - XW\|_F^2 + \lambda\|W\|_1 \ \text{s.t. acyclic}", 38),
             (r"\text{solved by}", r":", r"\text{augmented Lagrangian, \ gradients}", 40),
             (r"\text{benchmarks}", r":", r"\text{impressive, \ but}", 40)],
            [r"Zheng et al. (2018)", r"a smooth characterization", r"Part 21's methods", r"the next chart"],
            colors=[(0, IDC)])

    def chart(self):
        d = load("discovery")
        vs, vss = np.asarray([r["vs"] for r in d["rows"]]), np.asarray([r["vs_std"] for r in d["rows"]])
        A = axes([0, 1], [0, 1], x_length=6.4, y_length=4.4, xlabel=r"graph", ylabel=r"varsortability",
                 xticks=None, yticks=[0, 0.5, 1], center=[-2.8, 0.2, 0])
        ax = A.ax
        k = len(vs)
        xs = (np.arange(k) + 0.5) / k
        raw = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=NAIVEC) for a, b in zip(xs, vs)])
        std = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=IDC) for a, b in zip(xs, vss)])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(1, 0.5), color=GREY_B, stroke_width=1.5)
        side = side_groups([
            [(rf"{k} random linear SEMs, \ 10 nodes", WHITE), (r"weights $\pm[0.5, 2]$, \ unit noise", GREY_A)],
            [(rf"red: \ raw data, \ mean {d['vs']:.2f}", NAIVEC), (r"variance grows along the arrows", NAIVEC)],
            [(rf"green: \ standardized, \ mean {d['vs_std']:.2f}", IDC), (r"the shortcut is gone", IDC)],
            [(rf"PC (Fisher $z$, $\alpha = 0.01$): \ recall {d['recall']:.2f}, \ precision {d['precision']:.2f}", GREY_A)],
        ], width=4.8, pos=(4.1, 0.2, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> Alexander Reisach, Christof Seiler and Sebastian Weichwald noticed the shortcut in 2021. "
            f"In simulated linear models, with weights of moderate size and unit noise, each variable's variance tends to "
            f"grow along the causal order, since it accumulates its ancestors' noise. <bookmark mark='b'/> Here, over "
            f"{k} random graphs, sorting by variance puts {100 * d['vs']:.0f} percent of ancestral pairs in the right order: "
            f"a method could find the order by looking at the scale alone. <bookmark mark='c'/> Standardize the data and "
            f"the fraction drops to {100 * d['vs_std']:.0f} percent, chance, and, they showed, NOTEARS's accuracy collapses with it. <bookmark "
            f"mark='d'/> The scale-free PC skeleton, for comparison, recovers {100 * d['recall']:.0f} percent of the edges "
            f"with precision {100 * d['precision']:.0f} percent, either way."
        ) as vo:
            self.play(FadeIn(A), Create(half), FadeIn(simulated_tag(r"simulated, \ $n = 2{,}000$ per graph")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(raw, lag_ratio=0.05), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(std, lag_ratio=0.05), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lessons(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Lessons from causal discovery. <bookmark mark='b'/> Data identify a graph only up to an "
            "equivalence class, unless further assumptions are made. <bookmark mark='c'/> Benchmarks must be scale-free, "
            "or methods can win by reading units. <bookmark mark='d'/> Interventional data, from experiments on some "
            "variables, shrink the equivalence class, the basis of modern discovery from perturbation screens. <bookmark "
            "mark='e'/> And a learned graph is a hypothesis, to be tested, not a premise for chapter one's formulas.",
            [(r"lessons:", GREY_A),
             (r"identified up to equivalence, \ unless more is assumed", HIDC),
             (r"benchmarks must be scale-free \ (varsortability)", NAIVEC),
             (r"interventions shrink the class", IDC),
             (r"a learned graph is a hypothesis", GOLDC)])

    def interventions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Experiments on the variables themselves break the equivalence. <bookmark mark='b'/> If X "
            "is set by intervention and Y changes, the arrow runs from X to Y; if Y is set and X does not change, it does "
            "not run back. <bookmark mark='c'/> Alain Hauser and Peter Bühlmann characterized in 2012 which interventions "
            "identify which edges, and their greedy search learns from mixed observational and interventional data. "
            "<bookmark mark='d'/> Modern perturbation screens, which knock down thousands of genes one at a time, supply "
            "exactly such data, and are now the main testing ground for discovery methods.",
            [(r"\text{intervene on } X", r":", r"\text{does } Y \text{ change?}", 40),
             (r"\text{orients}", r":", r"\text{edges an observational class cannot}", 40),
             (r"\text{theory}", r":", r"\text{interventional equivalence classes}", 40),
             (r"\text{data}", r":", r"\text{gene perturbation screens}", 40)],
            [r"experiments, \ again", r"the arrow's direction", r"Hauser \& B\"uhlmann (2012)", r"Perturb-seq"],
            colors=[(1, IDC)])
