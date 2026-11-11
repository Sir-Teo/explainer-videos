from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono)


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
            tile(MathTex(r"\text{exchange}", font_size=40, color=YES), r"greedy and matroids", YES),
            tile(MathTex(r"3^{\lg n} = n^{1.585}", font_size=40, color=DATA), r"Karatsuba", DATA),
            tile(MathTex(r"7^{\lg n} = n^{2.807}", font_size=40, color=HEAD), r"Strassen", HEAD),
            tile(MathTex(r"\omega^{k + n/2} = -\omega^k", font_size=40, color=LAM), r"the FFT", LAM),
            tile(MathTex(r"D(i, j)", font_size=44, color=CTRL), r"dynamic programming", CTRL),
            tile(MathTex(r"L[R[x]] \gets x", font_size=40, color=FUNC), r"dancing links", FUNC),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ The Great Paradigms", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Greedy algorithms and the exchange argument; Huffman codes; matroids and "
            "the theorem that says exactly when greedy works. Karatsuba's three products and Strassen's seven. The "
            "fast Fourier transform, from the roots of unity to butterflies, and the multiplication of million-digit "
            "numbers. The closest pair. Dynamic programming, from Fibonacci through edit distance, knapsack, matrix "
            "chains, search trees and trees. Backtracking and dancing links. And one problem solved four ways."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"randomized algorithms: \ Freivalds, \ Karger, \ hashing", [20]),
            (r"strings: \ \texttt{diff} as a shortest path on the edit graph", [21]),
            (r"linear programming; \ branch and bound", [23]),
            ('decision knapsack, subset sum and generalized Sudoku: NP-completeness', [26]),
            (r"fine-grained complexity: \ SETH and edit distance", [27]),
            (r"big-number arithmetic and the NTT for cryptography", [30]),
            (r"the quantum Fourier transform", [53]),
        ], font_size=24)
        with self.voiceover(
            'Where this comes back. Part 20 adds randomness. Part 21 connects insert-delete scripts to paths on an edit graph and practical diff algorithms. Part 23 studies linear programming and branch and bound. Part 26 studies decision versions of knapsack and subset sum, and generalized Sudoku, as NP-complete problems. Part 27 develops conditional fine-grained hardness for exact worst-case edit distance. Part 30 uses big-integer arithmetic and modular transforms. Part 53 introduces the quantum Fourier transform, whose circuit and output access differ from a classical FFT.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"signals", 'spectral imaging, OFDM and signal analysis; FFT libraries include FFTW and cuFFT'),
            (r"numbers", r"GMP: \ schoolbook, \ Karatsuba, \ Toom, \ then FFT, \ switching at tuned sizes"),
            (r"matrices", r"BLAS: \ cubic, \ blocked and vectorized; \ Strassen rarely"),
            (r"text", r"\texttt{diff}, \ spelling, \ DNA alignment: \ dynamic programming"),
            (r"solvers", r"SAT, \ integer programming and constraint solvers: \ search with pruning"),
        ])
        with self.voiceover(
            'In applications, the details return. Fourier-transform libraries serve signal processing, imaging and '
            'communications. Big-number libraries switch among school multiplication, Karatsuba, Toom-Cook and '
            'transform methods according to operand sizes and tuned thresholds. Matrix software combines layout, '
            'blocking, vectorization, threading and sometimes fast algebraic schemes. Diff and sequence alignment use'
            ' related dynamic programs with different objectives and accelerations. Constraint and integer-'
            'programming solvers use search, propagation and bounds. The paradigm suggests a structure; correctness, '
            'numerical behavior and measurement scope still need checking.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that some optimal prefix code has the two rarest symbols as sibling leaves at the greatest "
            r"depth, \ and deduce that Huffman's algorithm is optimal.",
            'Solve $T(n)=3T(n/2)+cn$, $T(1)=1$, for $n=2^k$; count $3^k$ full-tree leaves, and explain skipped zero products.',
            r"Prove $\sum_{k=0}^{n-1} \omega^{jk} = 0$ for $n \nmid j$, \ and deduce $F^{-1} = \frac{1}{n}\overline{F}$ "
            r"for the DFT matrix.",
            r"Prove the edit-distance recurrence correct, \ and recover an optimal edit script from the table in "
            r"$O(n + m)$ extra time.",
            r"\textit{Build.} \ Implement the number-theoretic transform modulo $40961 = 5 \cdot 2^{13} + 1$ in the "
            r"Pebble language, \ multiply two 500-digit numbers on the emulator, \ and compare its instruction count "
            r"with Karatsuba.",
            '$\\bigstar$ \\textit{Research (open).} \\ Over $\\mathbb C$, must unrestricted linear circuits for the DFT need $\\Omega(n\\log n)$ arithmetic operations?',
        ], font_size=22)
        with self.voiceover(
            'The notes contain five worked exercises and a separate open research extension. Pause on any statement. '
            'The build exercise implements a number-theoretic transform for a five-hundred-digit product, with a '
            'transform length and coefficient bound that prevent modular ambiguity. Test it against an exact '
            'reference before comparing instruction counts; no crossover is promised in advance. The starred question'
            ' asks about the unrestricted linear-circuit model and explains how it differs from the known bounded-'
            'coefficient result.'
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 20, \ Randomness as a Resource", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"checking a matrix product in $n^2$ \ (Freivalds)", DATA),
            (r"a minimum cut by contracting random edges \ (Karger)", LAM),
            (r"primes in milliseconds \ (Miller--Rabin)", YES),
            (r"the top words of thirty novels in kilobytes: \ ledger row 9", COST))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"a coin flip can stand in for cleverness", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, a fifth paradigm. A coin flip can stand in for cleverness: checking a matrix product in n "
            "squared time, finding a minimum cut by contracting random edges, testing primes in milliseconds, and "
            "counting the top words of the thirty novels in a few kilobytes, the ledger's ninth row. Part 20, "
            "Randomness as a Resource."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Cormen, Leiserson, Rivest and Stein, \textit{Introduction to Algorithms}, \ chapters 4, 14--15, 30",
             r"Kleinberg and Tardos, \textit{Algorithm Design}, \ chapters 4--6",
             r"Dasgupta, Papadimitriou and Vazirani, \textit{Algorithms}, \ chapters 2, 5, 6",
             r"Knuth, \textit{The Art of Computer Programming}, \ volumes 2 \ (4.3.3) \ and 4B; \ Bentley, "
             r"\textit{Programming Pearls}"],
            [r"Huffman (1952); \ Rado (1957); \ Edmonds (1971); \ Karatsuba and Ofman (1962); \ Strassen (1969)",
             r"Cooley and Tukey (1965); \ Sch\"onhage and Strassen (1971); \ Harvey and van der Hoeven (2021)",
             r"Bellman (1957); \ Wagner and Fischer (1974); \ Knuth (1971); \ Shamos and Hoey (1975)",
             r"Knuth, \ ``Dancing links'' (2000); \ Coppersmith and Winograd (1990); \ Alman et al. (2024)",
             r"Backurs and Indyk (2015); \ Ambainis, Filmus and Le Gall (2015); \ Afshani et al. (2019)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
