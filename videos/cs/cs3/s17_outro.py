from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import COST, CTRL, DATA, HEAD, NO, PART, WIRE, YES, gate, load, nmos, pmos, wire


def tile(content, caption, color, TW=3.6, TH=2.3):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color="#121722", fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(box.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.3)
    return Group(box, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        d = load("cmos")
        vin, vout = np.asarray(d["vin"]), np.asarray(d["vout"])
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=2.2, y_length=2.0, tips=False,
                  axis_config={"color": GREY_D})
        curve = VGroup(ax, VMobject(color=CTRL, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, y) for x, y in zip(vin[::8], vout[::8])]))
        nand = gate("NAND", size=1.0)
        eq = MathTex(r"x\,y \leftrightarrow \text{series}", r"\\ x + y \leftrightarrow \text{parallel}", font_size=30,
                     color=DATA)
        kmap = MathTex(r"f = A'D' + B'D' + BD", font_size=30, color=YES)
        bdd = MathTex(r"2k + 2 \ \text{vs} \ 2^{k+1}", font_size=34, color=COST)
        count = MathTex(r"\approx 2^n / n", font_size=44, color=NO)
        tiles = Group(
            tile(eq, r"Shannon: \ circuits are expressions", DATA),
            tile(curve, r"the CMOS inverter restores", CTRL),
            tile(nand, r"NAND alone is complete", YES),
            tile(kmap, r"maps and normal forms", YES),
            tile(bdd, r"BDDs: \ order matters", COST),
            tile(count, r"most functions are huge", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Logic from Switches", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Shannon's dictionary, which turns switching circuits into Boole's algebra and "
            "back. The transistor as a switch, and the CMOS inverter, whose steep curve throws noise away at every "
            "stage. NAND and NOR in four transistors each, and the proof that NAND alone builds everything. Normal "
            "forms, maps and decision diagrams, the ways to write a function down and to shrink it. And Shannon's "
            "counting argument: almost every function needs an enormous circuit, though nobody can name one."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"NAND, \ multiplexers, \ decoders", [4, 5, 6]),
            (r"depth and the critical path", [4, 5, 7]),
            (r"$P \approx \alpha C V^2 f$", [7, 10]),
            (r"BDDs and equivalence checking", [54]),
            (r"circuit lower bounds", [26, 27]),
            (r"reversible gates", [53]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. Gates, multiplexers and decoders build the adders of Part 4, the memories of Part "
            "5 and Pebble itself in Part 6. Depth and the critical path decide how fast those circuits run, and Part "
            "7's pipeline exists to shorten it. The power formula explains Part 10's turn to many cores. Decision "
            "diagrams come back in Part 54 to check hardware and software, circuit lower bounds in Parts 26 and 27, "
            "and reversible gates in Part 53's quantum computer."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"hardware description", r"Verilog, \ VHDL, \ Chisel: \ circuits written as programs, \ like our netlists"),
            (r"logic synthesis", r"Yosys, \ ABC, \ commercial tools: \ the laws of chapter one, \ at scale, \ "
                                 r"with heuristics"),
            (r"FPGAs", r"lookup tables and programmable wires: \ prototypes, \ networking, \ cloud accelerators"),
            (r"verification", r"BDD- and SAT-based equivalence checking \ before every chip is made"),
            (r"timing closure", r"making every critical path fit the clock: \ much of a chip team's year"),
        ])
        with self.voiceover(
            "In practice: hardware engineers write circuits as programs, in Verilog, VHDL or Chisel, much like this "
            "series' netlists. Synthesis tools apply the laws of chapter one, at enormous scale, to turn those programs "
            "into gates. FPGAs run them as lookup tables. Equivalence checkers, built on decision diagrams and "
            "satisfiability solvers, prove the optimized circuit still matches the specification. And a large part of "
            "every chip project is timing closure: making every critical path fit inside the clock."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that NOR alone is complete: \ build NOT, OR and AND from NOR gates, \ with as few as you can.",
            r"Use Post's test to show that $\{\textsc{xor}, \textsc{and}\}$ is not complete, \ but $\{\textsc{xor}, "
            r"\textsc{and}, 1\}$ is.",
            r"Find a minimal sum of products for $f = \sum m(1, 3, 4, 5, 9, 11, 12, 13)$ \ with a Karnaugh map.",
            r"How many Boolean functions of 3 inputs are there? \ How many of them are monotone?",
            r"$f = x\bar y + y z$ \ with $x = z = 1$: \ which input change causes a glitch, \ and what term removes it?",
            r"\textit{Build.} \ With \texttt{explainer/cs/pebble/hdl.py}, \ build a 4-to-1 multiplexer from NAND gates "
            r"only, \ verify it on all 64 inputs, \ and compare your count with \texttt{to\_nand()}.",
            r"$\bigstar$ \textit{Research.} \ Extend \texttt{compute\_census} to all 65{,}536 functions of four inputs "
            r"\ and recover Knuth's maximum of 7 gates. \ Open: \ is the Minimum Circuit Size Problem NP-complete?",
        ], font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in the part's notes. Pause on any of them. The sixth is a build "
            "problem: it asks you to use this series' hardware library yourself. The last, marked with a star, is a "
            "research problem: a computation that took Knuth real ingenuity, and a question nobody can answer."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 4, \ Arithmetic", font_size=44).to_edge(UP, buff=0.6)
        add = MathTex(r"\begin{array}{r} 1011 \\ +\ 0110 \\ \hline 10001 \end{array}", font_size=60, color=DATA)
        add.move_to(DOWN * 0.3)
        q = label(r"how do gates add, \ and how fast can they?", font_size=30, color=HEAD).next_to(add, DOWN, buff=0.5)
        with self.voiceover(
            "Next time: arithmetic. With gates in hand, we teach them to count. A half adder, a full adder, and a "
            "ripple of them that adds numbers of any length, slowly; then the tricks that make addition take log n "
            "time instead of n, two's complement for negative numbers, multiplication, and the arithmetic unit at the "
            "heart of Pebble."
        ):
            self.play(FadeIn(nxt), Write(add), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Harris and Harris, \textit{Digital Design and Computer Architecture}, ch. 1--2",
             r"Nisan and Schocken, \textit{The Elements of Computing Systems}, ch. 1",
             r"Petzold, \textit{Code}",
             r"Weste and Harris, \textit{CMOS VLSI Design}, ch. 1",
             r"Wegener, \textit{The Complexity of Boolean Functions}; \ Jukna, \textit{Boolean Function Complexity}",
             r"Knuth, \textit{The Art of Computer Programming}, vol. 4A, \S 7.1"],
            [r"Boole, \textit{An Investigation of the Laws of Thought} (1854); \ Shannon, ``A symbolic analysis of relay "
             r"and switching circuits'' (1938)",
             r"Post (1941); \ Shannon, ``The synthesis of two-terminal switching circuits'' (1949); \ Lupanov (1958); "
             r"\ Karnaugh (1953)",
             r"Landauer (1961); \ Moore (1965); \ Bennett (1973); \ Toffoli (1980); \ Bryant, ``Graph-based "
             r"algorithms for Boolean function manipulation'' (1986)",
             r"H\aa stad (1986); \ Umans (2001); \ Li and Yang, ``3.1n -- o(n) circuit lower bounds for explicit "
             r"functions'' (2022)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
