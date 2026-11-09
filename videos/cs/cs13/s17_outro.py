from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (BG, CODE, COST, CTRL, DATA, DEMO_POS_SMALL, FUNC, HEAD, NO, PART, YES, cfg_view,
                                   code, graph, load, mono, region)


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
        ra = load("regalloc")["demo"]
        p = load("passes")
        cfg = cfg_view(load("ir")["func"], DEMO_POS_SMALL, size=14, lines=False)
        g = graph(ra["nodes"], [tuple(e) for e in ra["edges"]], colors=ra["colors"], radius=2.2, node_r=0.26,
                  font_size=11)
        bars = VGroup(*[Rectangle(width=3.4 * r["array"] / p["rows"][0]["array"], height=0.18, stroke_width=0,
                                  fill_color=YES if k else NO, fill_opacity=0.85) for k, r in enumerate(p["rows"])])
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        tiles = Group(
            tile(VGroup(*[region(2.6, 0.55, t, c, font_size=20) for t, c in
                          ((r"front end", DATA), (r"middle end", YES), (r"back end", FUNC))]).arrange(DOWN, buff=0.2),
                 r"the shape of a compiler", DATA),
            tile(cfg, r"CFGs and dominators", CTRL),
            tile(mono("%s.5 = φ(%s.4, %s.3)", 20, HEAD), r"SSA", HEAD),
            tile(MathTex(r"\mathrm{lfp}(F) = \bigsqcup_k F^k(\bot)", font_size=40), r"dataflow as fixed points",
                 YES),
            tile(g, r"allocation by colouring", FUNC),
            tile(bars, r"the Job, pass by pass", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ The Compiler", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            "We built a path from parsed source to Pebble machine code. A checker resolves names, scopes, types "
            "and layouts. Intermediate instructions and control-flow graphs make dependencies explicit. "
            "Dominators and frontiers support static single assignment, while dataflow equations compute "
            "conservative facts. We measured constant propagation, value numbering, dead-code elimination, loop "
            "transformations and inlining on a specified Job workload. Instruction selection chooses tiles; "
            "allocation maps live values to constrained storage; scheduling trades dependencies against machine "
            "resources. Strict SSA gives a particularly tractable graph-coloring model, not a complete solution "
            "to every allocation cost. Differential tests, semantic regression cases and encoded solver proofs "
            "supply different kinds of evidence. Candidate search then explores some transformations our "
            "hand-written rules miss."
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"types that are proved to keep their promises", [14]),
            (r"interpreters, \ JITs, \ garbage collectors", [15]),
            (r"the Job's algorithm, \ replaced", [16, 17]),
            (r"graph colouring, \ dynamic programming", [18, 19]),
            (r"Rice's theorem, \ proved; \ NP-hardness, \ explained", [25, 26]),
            (r"the build system that runs the compiler", [41]),
            (r"CompCert's proof; \ Trusting Trust", [54, 55]),
            (r"compilers for accelerators", [60]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 14 proves what the type checker's promises are worth, and Part 15 builds "
            "the runtimes where just-in-time compilers and garbage collectors live. Parts 16 and 17 replace the "
            "Job's algorithm, and the compiler carries the gain to the machine. Graph colouring and dynamic "
            "programming return in Parts 18 and 19, and Rice's theorem and NP-hardness are proved in Parts 25 and "
            "26. Part 41 builds the system that runs the compiler, CompCert's proof is Part 54, Ken Thompson's "
            "self-reproducing compiler is the finale, and Part 60 compiles for accelerators."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"levels", r"ship \texttt{-O2}; \ debug at \texttt{-O0} or \texttt{-Og}; \ \texttt{-O3} only when "
                        r"measured to help"),
            (r"read the output", r"Compiler Explorer (godbolt.org); \ \texttt{-S}; \ \texttt{-fopt-info}, \ "
                                 r"\texttt{-Rpass}"),
            (r"help the optimizer", r"\texttt{restrict}, \ \texttt{const}, \ \texttt{static}; \ profile-guided "
                                    r"and link-time optimization"),
            (r"JIT tiers", r"V8, \ the JVM, \ .NET: \ interpret, \ then compile what is hot"),
            (r"the job", r"compiler engineers: \ LLVM, \ GCC, \ GPU and ML compilers \ (XLA, \ MLIR, \ Triton)"),
        ])
        with self.voiceover(
            (
            "In practice, choose optimization and debugging settings for the workload and toolchain, then "
            "measure. O zero favors straightforward debugging; O two is a common release starting point, while O "
            "three, profile-guided optimization and link-time optimization can help or hurt a particular build. "
            "Read generated assembly and optimization reports to understand a missed opportunity. Express only "
            "contracts the program actually satisfies: C restrict has aliasing obligations, and const and static "
            "have several meanings that do not automatically imply independent memory. Managed runtimes can "
            "interpret, compile and recompile hot code in tiers, with startup and steady-state tradeoffs. "
            "Compiler work also serves accelerators and machine learning, through projects such as XLA, MLIR and "
            "Triton."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Compute the dominator tree and dominance frontiers of a \texttt{while} loop containing an "
            r"\texttt{if} with an early \texttt{return}, \ and place the $\phi$s for a variable assigned in both "
            r"branches.",
            r"Run liveness by hand on a three-block loop, \ and show that the iteration's result is the least "
            r"solution of the equations.",
            r"Show that $x \cdot 3 / 3 \to x$ is false on 32-bit integers, \ and find for which $c$ the rule "
            r"$x \cdot c / c \to x$ is sound.",
            r"Prove that if simplification removes every node, \ each with fewer than $k$ neighbours when removed, "
            r"\ the graph is $k$-colourable; \ then show that Chaitin's method spills on a 4-cycle with $k = 2$.",
            "\\textit{Build.} Merge loads only with valid memory and control proofs; test overlapping widths and guarded accesses.",
            "$\\bigstar$ \\textit{Investigate.} Reproduce fixed-register spill-everywhere DP; define a precise extension and review known results.",
        ], font_size=22)
        with self.voiceover(
            (
            "The notes contain six problems with worked guidance. Pause on any one. The fifth is a build problem: "
            "merge repeated loads only when the address and intervening memory effects justify it. Include "
            "overlapping byte and word accesses, guarded loads and negative cases, then compare outputs before "
            "measuring gains. The starred problem distinguishes a known fixed-register spill-everywhere algorithm "
            "from a research extension. First reproduce the restricted result. Then define the cost, register "
            "model and desired guarantee before investigating the literature. The exercise does not label that "
            "already-solved special case an open problem."
        )
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 14, \ Lambda and Types", font_size=42).to_edge(UP, buff=0.6)
        lam = MathTex(r"(\lambda x.\, x\,x)\,(\lambda x.\, x\,x)", font_size=48, color=HEAD).move_to(UP * 0.6)
        rule = MathTex(r"\frac{\Gamma,\, x : A \vdash e : B}{\Gamma \vdash \lambda x.\, e : A \to B}", font_size=44,
                       color=YES).next_to(lam, DOWN, buff=0.6)
        q = label(r"a language made of functions alone, \ and types that prove programs cannot go wrong",
                  font_size=28, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. A whole programming language made of nothing but functions, Church's lambda calculus. "
            "Types that tame it, a proof that well-typed programs cannot go wrong, and types inferred without "
            "being written. Part 14, Lambda and Types."
        ):
            self.play(FadeIn(nxt), FadeIn(lam))
            self.play(FadeIn(rule), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Aho, Lam, Sethi and Ullman, \textit{Compilers} (the Dragon Book), ch. 6--10",
             r"Cooper and Torczon, \textit{Engineering a Compiler}",
             r"Appel, \textit{Modern Compiler Implementation in ML}",
             r"Muchnick, \textit{Advanced Compiler Design and Implementation}; \ Rastello and Bouchez, "
             r"\textit{SSA-based Compiler Design}",
             r"Nielson, Nielson and Hankin, \textit{Principles of Program Analysis}"],
            [r"Backus, ``The history of FORTRAN I, II, and III'' (1978)",
             r"Kildall, ``A unified approach to global program optimization'' (1973)",
             r"Cytron, Ferrante, Rosen, Wegman, Zadeck, ``Efficiently computing static single assignment form'' "
             r"(1991)",
             r"Wegman and Zadeck, ``Constant propagation with conditional branches'' (1991)",
             r"Chaitin, ``Register allocation and spilling via graph coloring'' (1982)",
             r"Hack, Grund and Goos, ``Register allocation for programs in SSA-form'' (2006)",
             r"Poletto and Sarkar, ``Linear scan register allocation'' (1999)",
             r"Yang, Chen, Eide and Regehr, ``Finding and understanding bugs in C compilers'' (2011)",
             r"Leroy, ``Formal verification of a realistic compiler'' (2009); \ Lopes et al., Alive (2015)",
             r"Massalin (1987); \ Schkufza, Sharma, Aiken, STOKE (2013); \ Willsey et al., egg (2021)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
