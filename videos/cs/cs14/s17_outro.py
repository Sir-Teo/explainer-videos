from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from explainer.cs.lam import parse
from videos.cs.cs14.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, church_boxes, code,
                                   deriv_tree, lam_tree, load, mono)


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
            tile(lam_tree(parse(r"(\x. x x) ((\y. y) z)"), font_size=18), r"terms and $\beta$", LAM),
            tile(church_boxes(3), r"Church encodings", FUNC),
            tile(MathTex(r"Y = \lambda f.\,(\lambda x.\, f\,(x\,x))\,(\lambda x.\, f\,(x\,x))", font_size=30),
                 r"recursion", CTRL),
            tile(deriv_tree(load("stlc")["small_deriv"], font_size=20), r"types and safety", YES),
            tile(mono("('a -> 'a) -> 'a -> 'a", 22, YES), r"inference", DATA),
            tile(MathTex(r"((A \to B) \to A) \to A", font_size=34, color=HEAD), r"propositions as types", HEAD),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Lambda and Types", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            (
            "We built lambda terms and capture-avoiding substitution, then compared beta reduction with weak "
            "evaluation. Church encodings supplied data, and fixed points supplied recursion, with delayed "
            "branches needed for the strict factorial. Confluence made beta normal forms unique up to alpha "
            "equivalence, while simple types supported progress, preservation and strong normalization in the "
            "specified recursion-free calculus. Random runs checked implementations, not the general proofs. "
            "Hindley Milner inferred the Job's types; shared type graphs distinguished representation blowup from "
            "typability complexity. Pure System F supplied parametric free theorems, and unrestricted equality "
            "showed why the same printed type in our toy ML core does not automatically supply them. "
            "Propositions-as-types connected proof search with programs, with Kripke countermodels certifying the "
            "displayed intuitionistic non-theorems."
        )
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"environments, \ closures, \ continuations, \ a VM, \ a garbage collector", [15]),
            (r"the Job in the $\lambda$-core, \ collected: \ ledger row 6", [15]),
            (r"diagonalization, \ the recursion theorem, \ Rice", [25]),
            (r"type-checked APIs and schemas", [43]),
            (r"proof assistants: \ Lean and Rocq", [54]),
            (r"Rust, \ and trusting the compiler", [55]),
            (r"semantics: \ what programs mean", [58]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 15 turns the lambda core into a real runtime, with environments, closures, "
            "continuations, a virtual machine and a garbage collector, and runs the Job on it for ledger row six. "
            "Part 25 proves the diagonal and recursion theorems that this part leaned on. Part 43 puts types on "
            "the boundaries between services. Part 54 proves programs correct in Lean and Rocq. Part 55 returns to "
            "Rust, and Part 58, in the research tier, asks what programs mean."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"inference", r"OCaml, \ Haskell, \ F\#, \ Rust and Swift's local inference, \ TypeScript"),
            (r"generics", r"Java, \ C\#, \ Go, \ Rust: \ parametric polymorphism, \ checked once"),
            (r"data", r"sum types and \texttt{match}: \ Rust, \ Swift, \ Kotlin, \ Scala, \ Python 3.10"),
            (r"gradual", r"TypeScript, \ mypy, \ Pyright: \ add types to a large codebase a file at a time"),
            (r"proofs", r"Lean's mathlib, \ CompCert, \ seL4: \ types as specifications"),
        ])
        with self.voiceover(
            (
            "In practice, inference and annotations are combined differently by OCaml, Haskell, Rust, Swift and "
            "TypeScript. Generic parameters, bounds, interfaces and runtime operations determine what a "
            "polymorphic function may observe; a generic-looking signature alone does not establish a pure System "
            "F free theorem. Sum types and pattern matching help express application invariants, with "
            "exhaustiveness guarantees that depend on the language and compiler settings. Optional or gradual "
            "typing lets teams adopt checks incrementally, with different runtime contracts. Dependent proof "
            "assistants can verify chosen mathematical and software properties, relative to explicit "
            "specifications, kernels and trusted assumptions."
        )
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Reduce $(\lambda x\,y.\; y\;x\;x)\;((\lambda z.\,z)\;a)\;(\lambda w.\,w)$ to normal form by normal order "
            r"and by applicative order, \ count the steps, \ and explain the difference.",
            "Define Church exponentiation, zero test and subtraction; measure a stated reduction strategy.",
            r"Prove progress for the cases \textsc{If} and \textsc{Succ}, \ stating the canonical forms lemma you need.",
            r"Infer by hand the principal type of $\lambda f\,g\,x.\; g\,(f\,x)\,x$, \ showing each unification.",
            "\\textit{Build.} Add an option ADT; define the pattern fragment before checking exhaustiveness.",
            "$\\bigstar$ \\textit{Investigate.} Reproduce space-efficient coercions; state a cost model and test a precise extension.",
        ], font_size=22)
        with self.voiceover(
            (
            "The notes contain six worked exercises. Compare reduction orders with exact parentheses; measure a "
            "stated Church-subtraction strategy; prove the progress cases; and infer a principal type while "
            "respecting the environment. The build exercise starts with a precisely limited constructor-pattern "
            "language before extending exhaustiveness checking. The starred investigation reproduces known "
            "space-efficient gradual coercions, then asks for one explicit extension and cost claim. A research "
            "prompt begins with definitions and a literature check; the presence of a star does not make an "
            "already solved subproblem open."
        )
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 15, \ Runtimes", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"closures and environments", LAM), (r"continuations: \ the stack as data", CTRL),
            (r"a bytecode VM", DATA), (r"garbage collection, \ in three colours", YES))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"a program needs a place to live: \ what does it cost to run a language like this?", font_size=26,
                  color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. The lambda core gets a runtime: closures and environments instead of substitution, "
            "continuations that turn the stack into data, a bytecode virtual machine, and a garbage collector kept "
            "correct by an invariant stated in three colours. Part 15, Runtimes."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pierce, \textit{Types and Programming Languages}",
             r"Harper, \textit{Practical Foundations for Programming Languages}",
             r"Barendregt, \textit{The Lambda Calculus: Its Syntax and Semantics}; \ Hindley and Seldin",
             r"S\o rensen and Urzyczyn, \textit{Lectures on the Curry--Howard Isomorphism}",
             r"Girard, Lafont and Taylor, \textit{Proofs and Types}"],
            [r"Church, ``An unsolvable problem of elementary number theory'' (1936); \ Church and Rosser (1936)",
             r"Church, ``A formulation of the simple theory of types'' (1940)",
             r"Tait, ``Intensional interpretations of functionals of finite type I'' (1967)",
             r"Milner, ``A theory of type polymorphism in programming'' (1978); \ Damas and Milner (1982)",
             r"Robinson, ``A machine-oriented logic based on the resolution principle'' (1965)",
             r"Girard (1972); \ Reynolds, ``Towards a theory of type structure'' (1974)",
             r"Wadler, ``Theorems for free!'' (1989); \ Howard (1969/1980); \ Griffin (1990)",
             r"Martin-L\"of, \textit{Intuitionistic Type Theory} (1984); \ Coquand and Huet (1988)",
             r"Siek and Taha, ``Gradual typing for functional languages'' (2006); \ Takikawa et al. (2016)",
             r"Jung et al., ``RustBelt'' (2018); \ Cohen, Coquand, Huber and M\"ortberg (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
