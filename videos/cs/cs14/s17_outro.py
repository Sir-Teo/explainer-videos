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
            "What we built in this part. Lambda terms, substitution without capture, and beta reduction. Booleans, "
            "numbers, pairs and lists from functions alone, and recursion from the Y combinator. Strategies that "
            "decide whether we finish, and the Church Rosser theorem that says they cannot change the answer. "
            "Simple types, with progress, preservation and Tait's normalization theorem, checked on thousands of "
            "random programs. Hindley Milner inference, which typed the Job with no annotations, and its doubly "
            "exponential worst case. System F and free theorems. And propositions as types, with programs found "
            "by proof search and Kripke models for the laws that have none."
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
            "In practice. Type inference is everywhere: fully in OCaml and Haskell, locally in Rust, Swift and "
            "TypeScript. Generics in Java, C sharp, Go and Rust are parametric polymorphism, checked once for "
            "every type. Sum types with pattern matching have spread to Rust, Swift, Kotlin, Scala and even "
            "Python. Gradual type checkers let a team add types to a large codebase one file at a time. And the "
            "same ideas, pushed to dependent types, verify mathematics, a C compiler and an operating system "
            "kernel."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Reduce $(\lambda x\,y.\; y\;x\;x)\;((\lambda z.\,z)\;a)\;(\lambda w.\,w)$ to normal form by normal order "
            r"and by applicative order, \ count the steps, \ and explain the difference.",
            r"Define $\mathit{exp}$, \ $\mathit{iszero}$ and $\mathit{sub}$ on Church numerals, \ and explain why "
            r"$\mathit{sub}\;m\;n$ takes time proportional to $m \cdot n$.",
            r"Prove progress for the cases \textsc{If} and \textsc{Succ}, \ stating the canonical forms lemma you need.",
            r"Infer by hand the principal type of $\lambda f\,g\,x.\; g\,(f\,x)\,x$, \ showing each unification.",
            r"\textit{Build.} \ Add \texttt{type} declarations with constructors and exhaustive \texttt{match} to the "
            r"$\lambda$-core, \ with inference. \ Rewrite the Job's table with an \texttt{option}.",
            r"$\bigstar$ \textit{Research.} \ Design a sound gradual type system whose run-time checks cost a provably "
            r"bounded factor, \ or show that some program mix must pay unboundedly.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give the lambda core its own data types and pattern matching, with inference, and rewrite "
            "part of the Job with them. The last, marked with a star, is a research problem: its answer is not "
            "known, and the notes say where to start."
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
