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
            "What we built in this part. Linear programs, and the simplex method walking the edges of a polytope. "
            "Duality, which turns every optimum into a certificate a sceptic can check. The Klee–Minty cube, which "
            "makes the walk exponential, and smoothed analysis, which explains why it never is in practice. The "
            "ellipsoid and the central path. Total unimodularity, which makes some integer programs free, and branch "
            "and bound for the rest. Approximation with proofs: covers, tours, knapsacks, and a random hyperplane "
            "through a sphere of vectors. And decisions without the future: ski rental, paging, and multiplicative "
            "weights."
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
            r"\textit{Build.} \ Bland's-rule simplex in the Pebble language, \ with fractions as pairs of integers: \ "
            r"solve chapter 1's LP on the emulator and print 13.",
            r"$\bigstar$ \textit{Research.} \ Our random polytopes have diameter about $\sqrt n$. \ Prove that every "
            r"$d$-polytope with $n$ facets has diameter polynomial in $n$ and $d$ \ (the polynomial Hirsch "
            r"conjecture), \ or build a family that defeats it.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: the simplex method in the Pebble language, with exact fractions, run on the emulator. The "
            "last, marked with a star, is a research problem: its answer is not known, and the notes say where to "
            "start."
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
