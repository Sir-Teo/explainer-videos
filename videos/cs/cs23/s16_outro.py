from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (BG, COST, CTRL, DATA, HEAD, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        tiles = Group(
            tile(MathTex(r"\max\, c^{\mathsf T} x", font_size=46, color=DATA), r"simplex: \ walk the edges", DATA),
            tile(MathTex(r"c^{\mathsf T} x \le b^{\mathsf T} y", font_size=44, color=YES), r"duality's certificate",
                 YES),
            tile(MathTex(r"2^n - 1", font_size=48, color=NO), r"Klee--Minty; \ smoothed analysis", NO),
            tile(MathTex(r"\det \in \{0, \pm 1\}", font_size=42, color=HEAD), r"free integrality", HEAD),
            tile(MathTex(r"0.878", font_size=50, color=LAM), r"a random hyperplane", LAM),
            tile(MathTex(r"\sqrt{\tfrac{T}{2}\ln n}", font_size=44, color=COST), r"online; \ multiplicative weights",
                 COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Optimization", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            'What we built: linear programs with exact primal-dual certificates; a feasible-basis simplex whose '
            'budget status is explicit; and Klee-Minty instances checked in exact arithmetic. A separate '
            'shadow-vertex theorem explains one specified perturbation model. Ellipsoids, residual-certified '
            'barrier points and total unimodularity show where polynomial methods and integrality apply. Exact '
            'knapsack bounds expose why a nearly integral relaxation still needs a valid branch. Covers, metric '
            'tours and hyperplane rounding distinguish general guarantees from finite local measurements. '
            'Discrete ski rental, unit-cost paging and multiplicative weights keep their adversary and '
            'expected-loss models explicit.'
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the PCP theorem, \ hardness of approximation, \ unique games", [27]),
            (r"page replacement in the kernel: \ CLOCK as cheap LRU", [32]),
            (r"packing virtual machines and scheduling jobs in the cloud", [45]),
            (r"load balancing online: \ two random choices", [48]),
            (r"condition numbers, \ and why solvers fight floating point", [52]),
            (r"online learning, \ regret and boosting, \ with proofs", [57]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 27 builds the PCP theorem behind this part's hardness results, and the "
            "unique games conjecture. Part 32's kernel replaces pages with CLOCK, a cheap approximation of least "
            "recently used. Part 45's cloud packs virtual machines onto servers, an integer program solved by "
            "heuristics every second, and Part 48 balances load online. Part 52 explains why linear programming "
            "solvers fight floating point. And Part 57 turns multiplicative weights into a theory of learning. The AI "
            "series used this part's tools throughout: gradient descent and Newton's method, boosting, and the "
            "convex losses that make training tractable."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"solvers", r"HiGHS, \ Gurobi, \ CPLEX, \ OR-Tools, \ SCIP: \ simplex, \ barrier, \ branch and cut"),
            (r"logistics", r"vehicle routing, \ airline crews, \ supply chains: \ integer programs with millions of "
                           r"variables"),
            (r"markets", r"ad auctions, \ power grids, \ kidney exchanges: \ duals as prices"),
            (r"caches", r"CPU, \ page and CDN caches: \ online eviction, \ LRU approximations"),
            (r"learning", r"convex losses, \ SGD and Adam, \ boosting, \ online learning to rank"),
        ])
        with self.voiceover(
            "In practice. HiGHS, Gurobi, CPLEX and OR-Tools run simplex, barrier and branch and cut on problems with "
            "millions of variables. Airlines schedule crews, carriers route vehicles, and supply chains plan with "
            "integer programs. Power grids and kidney exchanges are cleared by optimization, with dual prices. Every "
            "cache makes online decisions, and every model is trained by the descendants of gradient descent."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove weak duality from the definitions, \ and derive complementary slackness from strong duality.",
            r"Prove that every vertex of the vertex-cover LP is \textbf{half-integral}: \ each $x_v \in \{0, "
            r"\tfrac12, 1\}$.",
            r"Show that renting $B - 1$ days and then buying is $(2 - 1/B)$-competitive, \ and that no deterministic "
            r"rule does better.",
            r"Show that $\theta/(1 - \cos\theta)$ is minimized where $\theta = \tan(\theta/2)$, \ and compute "
            r"Goemans--Williamson's $\alpha$ to four digits.",
            '\\textit{Build.} \\ Design a bounded $3\\times3$ rational simplex port in Pebble; \\ prove word bounds, \\ then verify on the emulator. \\ Not executed here.',
            '$\\bigstar$ \\textit{Research.} \\ Generate certified bounded 3D polytopes; \\ independently check BFS diameters; \\ compare a fixed routing rule and report seeds and failures.',
        ], font_size=22)
        with self.voiceover(
            (
            'Six exercises in the notes have worked guidance. The fifth designs a bounded three-by-three '
            'rational simplex port in Pebble; prove intermediate word bounds and verify it on the emulator '
            'before claiming a working build. We have not executed that port here. The last is a finite '
            'reproducible study of certified bounded polytopes and routing rules, with independent '
            'breadth-first-search references. Its deliverable is measured evidence and explicit limits, not a '
            'solution to the polynomial Hirsch conjecture.'
        )
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 24, \ Algorithms in Practice", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"prefix sums, \ Fenwick and segment trees", DATA),
            (r"two pointers, \ monotonic stacks, \ bit tricks", YES),
            (r"algorithm engineering: \ caches, \ branches and SIMD", LAM),
            (r"benchmarking honestly", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"same big-O, \ twenty times apart", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, algorithms in practice. Big-O hides constants, and in production the constants and the "
            "machine decide. The everyday tools of real code: prefix sums, Fenwick and segment trees, two pointers, "
            "monotonic stacks and bit tricks. Then algorithm engineering, where a textbook hash table or binary "
            "search becomes many times faster by respecting the caches, branch predictors and vector units of Act "
            "Two, and how to measure that honestly. Part 24, Algorithms in Practice."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Bertsimas and Tsitsiklis, \textit{Introduction to Linear Optimization}; \ Chv\'atal, \textit{Linear "
             r"Programming}",
             r"Matou\v{s}ek and G\"artner, \textit{Understanding and Using Linear Programming}; \ Schrijver, "
             r"\textit{Theory of Linear and Integer Programming}",
             r"Williamson and Shmoys, \textit{The Design of Approximation Algorithms}; \ Borodin and El-Yaniv, "
             r"\textit{Online Computation}; \ Boyd and Vandenberghe"],
            [r"Dantzig (1947); \ Klee and Minty (1972); \ Khachiyan (1979); \ Karmarkar (1984); \ Spielman and Teng "
             r"(2001)",
             r"Hoffman and Kruskal (1956); \ Gomory (1958); \ Christofides (1976); \ Goemans and Williamson (1995)",
             r"Sleator and Tarjan (1985); \ Arora, Hazan and Kale (2012); \ Karlin, Klein and Oveis Gharan (2021)",
             r"Santos (2010); \ Cohen, Lee and Song (2019); \ Chen et al. (2022); \ Khot, Minzer and Safra (2018)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
