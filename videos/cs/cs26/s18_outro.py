from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono)


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
        head = label(rf"Part {PART}: \ P versus NP", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\mathrm{P} \subsetneq \mathrm{EXP}", font_size=46, color=DATA), r"hierarchies; \ Savitch",
                 DATA),
            tile(MathTex(r"\exists c:\ V(x, c)", font_size=46, color=HEAD), r"NP and certificates", HEAD),
            tile(MathTex(r"x_{t,j,s}", font_size=54, color=LAM), r"Cook--Levin's tableau", LAM),
            tile(MathTex(r"\le_p", font_size=60, color=YES), r"the reduction web", YES),
            tile(MathTex(r"4.27", font_size=56, color=NO), r"CDCL; \ the phase transition", NO),
            tile(MathTex(r"\sqrt{t \log t}", font_size=50, color=COST), r"barriers; \ five worlds", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            'This part built a map of computational complexity. Polynomial time under standard cost models; the correct time hierarchy and Savitch proof ideas; NP certificates; a bounded Cook-Levin encoding with complete traces; concrete reductions and mapped witnesses; coNP, prime certificates and quantifier alternation; games and space; the multitape square-root-space theorem; and a clause-learning SAT solver with finite random-instance measurements. The experiments verify finite implementations, while theorems keep their model assumptions. Barriers, hypothetical worlds and meta-complexity explain both progress and what remains unresolved.'
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"randomness, \ interaction and PCPs", [27]),
            (r"one-way functions and pseudorandomness", [29]),
            (r"public keys on factoring and discrete logs", [30]),
            (r"dependency resolution with CDCL and PubGrub", [41]),
            (r"quantum computers and the extended thesis", [53]),
            (r"verification conditions checked by SAT", [54]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 27 adds randomness and interaction to proofs, and reaches the PCP theorem. "
            "Part 29 builds cryptography on one-way functions, Impagliazzo's Minicrypt, and Part 30 builds public "
            "keys on factoring and discrete logarithms, the suspects of chapter twelve. Part 41 resolves package "
            "dependencies with a SAT solver. Part 53 asks whether quantum computers break the extended "
            "Church-Turing thesis. And Part 54 proves programs correct by sending verification conditions to a "
            "solver like ours."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"recognize it", r"scheduling, \ packing, \ configuration, \ dependencies: \ NP-hard in general"),
            (r"then solve it anyway", r"SAT, \ SMT and ILP solvers; \ constraint programming; \ local search"),
            (r"or approximate", 'objective-specific guarantees; 0--1 knapsack has an FPTAS; weak hardness alone does not suffice'),
            (r"verification", r"model checking, \ equivalence checking, \ test generation: \ SAT inside"),
            (r"security", 'computational cryptography needs precise assumptions; information-theoretic ciphers differ'),
        ])
        with self.voiceover(
            'In practice, first specify the exact decision or optimization problem and its encoding. General scheduling, packing and dependency models may be NP-hard, while structured instances can be easy. SAT, SMT, integer programming and constraint solvers are useful tools. Approximation guarantees depend on the objective: weak hardness alone does not promise an FPTAS. Verification often uses SAT internally. For computational cryptography, identify the precise hardness assumption; information-theoretic ciphers require a different analysis.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that if $\mathrm{P} = \mathrm{NP}$ then $\mathrm{NP} = \mathrm{coNP}$, \ and that an NP-complete "
            r"problem in coNP implies $\mathrm{NP} = \mathrm{coNP}$.",
            r"Show that 2-SAT is in P \ (the implication graph and its strongly connected components, \ Part 18), \ "
            r"and explain where the 3-SAT gadgets fail.",
            r"Reduce 3-SAT to Hamiltonian path, \ drawing the gadget for one variable and one clause.",
            r"Show that if SAT can be \textit{decided} in polynomial time, \ a satisfying assignment can be "
            r"\textit{found} in polynomial time \ (self-reducibility).",
            r"\textit{Build.} \ Reduce Sudoku to SAT, \ solve a hard puzzle with this part's CDCL solver, \ and count "
            r"its conflicts.",
            r"$\bigstar$ \textit{Research.} \ For random 3-SAT, \ locate the threshold for $n \le 300$ with our "
            r"solver, \ estimate its width as a power of $n$, \ and compare the peak cost with the satisfiability "
            r"threshold.",
        ], font_size=22)
        with self.voiceover(
            'Six exercises, with worked guidance in the notes. Pause on any of them. The Sudoku build exercise retains the full formula, solver model and independently checked grid. The starred exercise estimates finite-size crossings and widths with uncertainty; it does not establish an asymptotic threshold or scaling exponent.'
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 27, \ Proofs and Randomness", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"zero-knowledge: \ convincing you without telling you", DATA),
            (r"interactive proofs: \ IP = PSPACE", YES),
            ('the PCP theorem: constant queries, with completeness and soundness', LAM),
            (r"why some problems are hard even to approximate", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            'Next, proofs that use randomness. Zero-knowledge protocols can convince a verifier while revealing no additional knowledge under their precise definition and assumptions. Interaction gives the class IP, equal to PSPACE; that equality does not prove a strict separation from NP. The PCP theorem uses logarithmically many random bits and a constant number of proof queries: true statements have an accepting proof, while false statements are rejected with bounded probability for every purported proof. It is not a guarantee to detect every changed bit in a proof. Part 27 develops those definitions and their consequences for approximation.'
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Sipser, \textit{Introduction to the Theory of Computation}, \ ch. 7--8; \ Arora and Barak, "
             r"\textit{Computational Complexity}",
             r"Papadimitriou, \textit{Computational Complexity}; \ Garey and Johnson, \textit{Computers and "
             r"Intractability}",
             r"Moore and Mertens, \textit{The Nature of Computation}; \ Goldreich, \textit{P, NP, and NP-Completeness}; "
             r"\ Fortnow, \textit{The Golden Ticket}"],
            [r"Cook (1971); \ Levin (1973); \ Karp (1972); \ Hartmanis and Stearns (1965); \ Savitch (1970); \ Ladner "
             r"(1975)",
             r"Baker, Gill and Solovay (1975); \ Razborov and Rudich (1994); \ Aaronson and Wigderson (2008); \ "
             r"Impagliazzo (1995)",
             r"Stockmeyer and Meyer (1973); \ Immerman (1988); \ Szelepcs\'enyi (1987); \ Cook and Mertz (2024); \ "
             r"Williams (2025)",
             r"Marques-Silva and Sakallah (1996); \ Heule, Kullmann and Marek (2016); \ Liu and Pass (2020); \ "
             r"Hirahara (2022)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
