from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import PART, load, gate, wire

GATE = C.CS_CONTROL
WIRE = C.CS_DATA
COSTC = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
LIMIT = C.CS_LIMIT
HEAD = C.CS_HEAD
HIST = C.HUMAN


class Frontier(VoiceoverScene):
    """The research tier (videos/cs/SYLLABUS.md 1.1): exact minimum circuits for small functions, why the census
    stops at five inputs, and the open problem of deciding a function's circuit size."""

    def construct(self):
        self.card()
        self.census()
        self.wall()
        self.elimination()
        self.mcsp()

    def card(self):
        card = chapter_card(15, r"Frontier: \ the smallest circuit", r"Can we find the best circuit, \ and can we "
                            r"prove it is best?", lit=(2000, 2022), part=PART,
                            extra=((2000, r"Kabanets and Cai: MCSP"), (2022, r"$3.1n$; partial MCSP is NP-hard")))
        with self.voiceover("Chapter fifteen. Frontier: the smallest circuit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def census(self):
        d = load("census")
        head = label(r"Every function of three inputs, \ solved exactly", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(*[label(rf"{k + 1} gate{'s' if k else ''}: \ {n:,} distinct search states".replace(",", "{,}"),
                               font_size=22, color=GREY_A) for k, n in enumerate(d["states"])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 4.2 + UP * 0.6)
        meth = label(r"breadth first: \ a search state is the set of functions on its wires; \\ add every possible gate, \ "
                     r"keep each new set once", font_size=20, color=GREY_B).next_to(steps, UP, buff=0.35).align_to(
            steps, LEFT)
        hist = d["hist"]
        bars = VGroup()
        for k, v in enumerate(hist):
            h = 3.4 * v / max(hist)
            r = Rectangle(width=0.8, height=max(h, 0.02), stroke_width=0, fill_color=GATE if k < 4 else LIMIT,
                          fill_opacity=0.8).move_to([0.8 + 1.05 * k, -1.9 + h / 2, 0])
            bars.add(VGroup(r, label(str(v), font_size=20, color=GREY_A).next_to(r, UP, buff=0.08),
                            label(str(k), font_size=20, color=GREY_B).next_to([0.8 + 1.05 * k, -1.9, 0], DOWN,
                                                                               buff=0.12)))
        bl = note(r"gates needed \ (all 256 functions)", font_size=20).next_to(bars, DOWN, buff=0.45)
        nm = d["named"]
        named = VGroup(
            label(rf"$x \oplus y \oplus z$: \ {nm['x xor y xor z']} gates", font_size=22, color=YES),
            label(rf"if $x$ then $y$ else $z$ \ (the multiplexer): \ {nm['if x then y else z']}", font_size=22,
                  color=GATE),
            label(rf"majority of three: \ {nm['majority']}, \ among the hardest", font_size=22, color=LIMIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3).align_to(steps, LEFT)
        with self.voiceover(
            "Chapter nine counted how many gates a typical function needs. For very small functions we can do better "
            "than count: we can find the best circuit for every one. <bookmark mark='a'/> Treat a search state as the set of "
            "functions its wires compute. Start from the three inputs and free constants, allow tied input pins, add every possible two-input gate, and keep each "
            "new set once. <bookmark mark='b'/> With constants and source wires free, one gate gives thirty-three distinct search states, two give eight hundred and "
            "twenty-eight, three give twenty thousand three hundred and sixty, four give over half a million, and at four gates every "
            "one of the two hundred and fifty-six functions of three inputs has appeared. <bookmark mark='c'/> So every "
            "function of three inputs needs at most four gates, and we know exactly how many each needs: parity of "
            "three needs two, the multiplexer three, and majority four, one of the twenty-four hardest. These are not "
            "estimates but proofs, by exhaustion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(meth), FadeIn(bars), FadeIn(bl))
            vo.wait_until("a")
            self.play(Circumscribe(bars[1], color=HEAD))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(Circumscribe(bars[4], color=LIMIT), run_time=2.0)
            self.play(FadeIn(named))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wall(self):
        d = load("census")
        head = label(r"The census hits a wall", font_size=36).to_edge(UP, buff=0.3)
        hdr = VGroup(label(r"inputs", font_size=22, color=GREY_B), label(r"functions", font_size=22, color=GREY_B),
                     label(r"hardest needs", font_size=22, color=GREY_B), label(r"settled", font_size=22, color=GREY_B))
        cols = [-4.6, -2.4, 0.2, 2.8]
        for x, h in zip(cols, hdr):
            h.move_to([x, 2.0, 0])
        who = [r"here, \ exhaustive search", r"Knuth \ (2005), \ by computer", r"by computer, \ 2019 \ (Knuth left a "
               r"few cases)", r"unknown"]
        rows = VGroup()
        for k, ((n, mx, cnt), w) in enumerate(zip(d["known"], who)):
            y = 1.35 - 0.62 * k
            c = LIMIT if mx == "?" else WHITE
            rows.add(VGroup(MathTex(str(n), font_size=32, color=c).move_to([cols[0], y, 0]),
                            MathTex(cnt, font_size=30, color=c).move_to([cols[1], y, 0]),
                            MathTex(mx if mx != "?" else r"?", font_size=32, color=HEAD if mx != "?" else LIMIT
                                    ).move_to([cols[2], y, 0]),
                            label(w, font_size=20, color=GREY_A).move_to([cols[3], y, 0], aligned_edge=LEFT)))
        notes = VGroup(
            label(r"$2^{2^n}$ functions: \ the count is squared with every input added", font_size=22, color=GREY_A),
            label(r"SAT solvers \ (Part 26) \ find circuits of 10 to 12 gates, \\ but struggle to prove that no 12-gate "
                  r"circuit exists for a 6-input function", font_size=22, color=GREY_A),
            label(r"exact answers end at five inputs; \ Shannon's bound says the hardest need about $2^n/n$", font_size=22,
                  color=LIMIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This cannot go much further. <bookmark mark='a'/> Four inputs give sixty-five thousand functions, and "
            "Donald Knuth computed all of their exact costs in 2005: the hardest need seven gates. Five inputs give "
            "four billion functions; Knuth settled almost all of them, and the last few were finished by computer in "
            "2019: the hardest needs twelve. <bookmark mark='b'/> At six inputs there are eighteen quintillion "
            "functions, and nobody knows the hardest cost. <bookmark mark='c'/> The number of functions squares with "
            "every input added. Modern SAT solvers, which Part 26 builds, can find circuits of ten or twelve gates, "
            "but proving that no twelve-gate circuit exists for a single six-input function is already at their limit. "
            "Exact knowledge of circuit size ends at five inputs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def elimination(self):
        head = label(r"How every linear lower bound is proved", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"pick an input $x_i$ \ and fix it to a constant", font_size=24, color=WIRE),
            label(r"fixing $x_i$ yields constants, copies or negations: \ simplify, folding negations into later gates",
                  font_size=24, color=GATE),
            label(r"if the function is chosen so that some choice always removes \textit{three} gates \\ and leaves a "
                  r"function of the same kind, \ induction on $n$ gives", font_size=24, color=GREY_A),
            MathTex(r"C(f) \;\ge\; C(f|_{x_i = c}) + 3 \;\ge\; \cdots \;\ge\; 3n - O(1)", font_size=40, color=HEAD),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.5)
        hist = VGroup(
            label(r"gate elimination: \ $2n$ \ (Kloss, \ Schnorr, \ 1960s--70s); \ $3n$ \ (Blum, \ 1984); \ "
                  r"\\ $(3 + \tfrac{1}{86})n$ \ (Find, Golovnev, Hirsch and Kulikov, \ 2016); \ $3.1n$ \ (Li and Yang, \ 2022)",
                  font_size=18, color=HIST),
            label(r"November 2026 preprint: \ $4n-O(\log n)$ \ reported by Mishra and Santhanam",
                  font_size=20, color=HEAD),
            label(r"each step needs a function where no input is ``cheap'': \ the 2016 and 2022 bounds use affine "
                  r"dispersers, \\ functions that are not constant on any large affine subspace", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        example_gate = gate("AND", size=0.65).move_to(LEFT * 3.8 + UP * 1.65)
        example = VGroup(example_gate,
                         MathTex("x", font_size=28, color=WIRE).next_to(example_gate.inp[0](), LEFT, buff=0.45),
                         MathTex("y", font_size=28, color=WIRE).next_to(example_gate.inp[1](), LEFT, buff=0.45),
                         wire(example_gate.inp[0]() + LEFT * 0.35, example_gate.inp[0]()),
                         wire(example_gate.inp[1]() + LEFT * 0.35, example_gate.inp[1]()),
                         MathTex(r"x\,y", font_size=28, color=GATE).next_to(example_gate.out(), RIGHT, buff=0.25))
        cases = VGroup(MathTex(r"x=0:\quad 0\wedge y=0", font_size=30, color=GATE),
                       MathTex(r"x=1:\quad 1\wedge y=y", font_size=30, color=YES)).arrange(DOWN, buff=0.24)
        cases.move_to(RIGHT * 2.5 + UP * 1.65)
        steps.scale(0.88).move_to(DOWN * 0.65)
        with self.voiceover(
            "How are the lower bounds that do exist proved? Almost all of them by one idea, gate elimination. "
            "<bookmark mark='a'/> Fix one input to a constant. <bookmark mark='b'/> A gate that input fed becomes "
            "a constant, a copy, or an inverted copy of its other input. Simplify constants and copies, and fold "
            "inversions into following gates; sometimes further gates disappear too. <bookmark mark='c'/> Choose the function so cleverly that, whatever the circuit, some input "
            "can always be fixed to remove at least three gates, and what remains is a function of the same kind with "
            "one input fewer. Then induction on the number of inputs gives three n. <bookmark mark='d'/> Norbert Blum "
            "reached three n in 1984. It took thirty-two years to add one eighty-sixth of n, and six more to reach three "
            "point one n, each by a longer case analysis of how a minimal circuit can look, for functions called affine "
            "dispersers, which stay non-constant on every large affine subspace. A November 2026 preprint by "
            "Mishra and Santhanam reports four n minus a logarithmic term, by eliminating independent parameters "
            "rather than only fixing input variables. The bound is still linear, a long way from two to the n over n."
        ) as vo:
            self.play(FadeIn(head), FadeIn(example), FadeIn(cases))
            for mk, st in zip("abc", steps[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=UP * 0.1))
            self.play(Write(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(hist[0]))
            self.play(FadeIn(hist[1]))
            self.play(FadeIn(hist[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mcsp(self):
        head = label(r"The Minimum Circuit Size Problem", font_size=36).to_edge(UP, buff=0.3)
        defn = VGroup(
            label(r"given: \ a truth table of $N = 2^n$ bits, \ and a number $s$", font_size=24, color=WIRE),
            label(r"question: \ does some circuit with at most $s$ gates compute it?", font_size=24, color=GATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(UP * 1.7)
        facts = VGroup(
            label(r"in NP: \ a circuit is a short certificate, \ checked on all $N$ rows \ (Part 26)", font_size=22,
                  color=YES),
            label(r"is it NP-complete? \ \ open \ (asked by Levin in the 1970s; \ Kabanets and Cai, \ 2000)",
                  font_size=22, color=LIMIT),
            label(r"Hirahara \ (2022): \ for partial truth tables, \ with some rows left free, \ it is NP-hard",
                  font_size=22, color=HEAD),
            label(r"Liu and Pass \ (2020): \ one-way functions exist \ iff \ a time-bounded version of Kolmogorov "
                  r"complexity \\ is mildly hard on average: \ cryptography rests on questions like this \ (Parts 29, "
                  r"30)", font_size=22, color=GREY_A),
            label(r"meta-complexity: \ how hard is it to tell how hard something is?", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(DOWN * 0.7)
        with self.voiceover(
            "So ask a computer the question directly. <bookmark mark='a'/> Given the truth table of a function and a "
            "number s, is there a circuit of at most s gates? This is the minimum circuit size problem. "
            "<bookmark mark='b'/> It is in NP, the class Part 26 defines: a small circuit, once found, is easy to check "
            "against every row. Is it as hard as everything in NP? Leonid Levin wondered in the 1970s, Valentine "
            "Kabanets and Jin-Yi Cai made the question famous in 2000, and it is still open. "
            "<bookmark mark='c'/> In 2022 Shuichi Hirahara proved the version with some rows left unspecified NP-hard, "
            "the closest anyone has come. <bookmark mark='d'/> And the question reaches cryptography: Yanyi Liu and "
            "Rafael Pass proved in 2020 that one-way functions, the foundation of Parts 29 and 30, exist exactly when a "
            "time-bounded version of Kolmogorov complexity is mildly hard on average. <bookmark mark='e'/> This young "
            "field, meta-complexity, asks how hard it is to tell how hard something is, and it is one of the most "
            "active in theory today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defn[0]), FadeIn(defn[1]))
            vo.wait_until("a")
            self.play(Circumscribe(defn, color=HEAD))
            for mk, f in zip("bcde", (facts[0:2], facts[2], facts[3], facts[4])):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
