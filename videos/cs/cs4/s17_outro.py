from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, KIND_COLOR, NO, PART, YES, load


def tile(content, caption, color, TW=3.6, TH=2.3):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color=BG, fill_opacity=1)
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
        # the clock
        ring = Circle(0.9, color=GREY_C, stroke_width=2)
        lab = VGroup(*[MathTex(str(k if k < 8 else k - 16), font_size=16, color=NO if k >= 8 else DATA).move_to(
            1.15 * np.array([np.cos(PI / 2 - 2 * PI * k / 16), np.sin(PI / 2 - 2 * PI * k / 16), 0])) for k in range(16)])
        clock = VGroup(ring, lab)
        # a Kogge-Stone network
        lv = load("prefix")["kogge-stone"]["levels"]
        ks = VGroup()
        for k, level in enumerate(lv, start=1):
            for i, j in level:
                ks.add(Line([-0.2 * j, -0.4 * (k - 1), 0], [-0.2 * i, -0.4 * k, 0], color=YES, stroke_width=1.5))
        # Wallace dots
        dots = VGroup(*[Dot([-0.25 * k, 0.22 * r, 0], radius=0.05, color=DATA) for k in range(15)
                        for r in range(min(k + 1, 15 - k, 8))])
        # SRT table, small
        tab = load("divide")["table"]
        qcol = {-2: "#4C6EF5", -1: "#74C0FC", 0: "#5C677D", 1: "#FFD43B", 2: "#FF922B"}
        srt = VGroup(*[Rectangle(width=0.16, height=0.03, stroke_width=0, fill_color=qcol[q], fill_opacity=0.9).move_to(
            [0.16 * (di - 16), 0.03 * pi, 0]) for pi, di, q in tab])
        # the float ruler
        vals = [v["v"] for v in load("floats")["mini"]["values"]]
        ruler = VGroup(Line([0, 0, 0], [3.5, 0, 0], color=GREY_C),
                       *[Line([v / 4, 0, 0], [v / 4, 0.3, 0], color=FUNC, stroke_width=2) for v in vals])
        # Wilkinson's roots
        fr = load("wilkinson")["frames"][-1]
        roots = VGroup(Line([0, 0, 0], [4.2, 0, 0], color=GREY_C),
                       *[Dot([x / 5, y / 3, 0], radius=0.05, color=NO if abs(y) > 1e-3 else YES) for x, y in fr])
        tiles = Group(
            tile(clock, r"integers on a clock", DATA),
            tile(ks, r"carries as a parallel prefix", YES),
            tile(dots, r"multipliers: \ trees of adders", CTRL),
            tile(srt, r"SRT, \ and five missing cells", NO),
            tile(ruler, r"floats: \ a logarithmic ruler", FUNC),
            tile(roots, r"ill conditioning", HEAD),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Arithmetic", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Integers on a clock, with two's complement letting one adder serve signed "
            "and unsigned numbers. The ripple-carry adder, and the associative carry operator that turns addition into "
            "a parallel prefix, logarithmic in depth. Multipliers as trees of carry-save adders, and division by SRT, "
            "with the table that cost Intel half a billion dollars. Pebble's ALU, built and verified. And floating "
            "point: a ruler with the same relative precision everywhere, correctly rounded operations, and the "
            "difference between an unstable formula and an ill-conditioned problem."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the ALU, \ the multiplier \ and the divider", [6, 7]),
            (r"parallel prefix", [10]),
            (r"overflow and integer types", [13, 55]),
            (r"bignums and Karatsuba", [19, 30]),
            (r"rounding error and conditioning", [23, 52]),
            (r"machine-checked arithmetic", [54]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. Part 6 wires this ALU into Pebble, and Part 7 adds the multiplier and the "
            "divider to its pipeline. The parallel prefix returns in Part 10 as the scan, a basic tool of parallel "
            "programming. Overflow and integer types come back in the compiler of Part 13 and in the security of Part "
            "55. Big integers and fast multiplication meet in Part 19 and drive public-key cryptography in Part 30. "
            "Rounding and conditioning return in optimization and in Part 52's real numbers, and machine-checked "
            "arithmetic in Part 54."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"integer overflow", r"a classic source of security holes: \ a wrapped length becomes a buffer overflow; "
                                  r"\ Rust's checked arithmetic, \ sanitizers"),
            (r"money", r"integer cents or decimal types: \ SQL \texttt{NUMERIC}, \ Java's \texttt{BigDecimal}, \ "
                       r"Python's \texttt{decimal}"),
            (r"numerical libraries", r"LAPACK and BLAS under numpy, \ correctly rounded \texttt{math.fsum}, \ libm's "
                                     r"minimax polynomials"),
            (r"machine learning", r"bfloat16 and FP8 on GPUs and TPUs, \ mixed precision with loss scaling"),
            (r"hardware testing", r"after FDIV: \ formal proofs of floating-point units at Intel and AMD"),
        ])
        with self.voiceover(
            "In practice: integer overflow is still a common cause of security holes, when a length wraps around and "
            "a buffer is allocated too small, which is why Rust checks arithmetic and why sanitizers exist. Money is "
            "kept in integers or decimal types, never in binary floats. Numerical libraries, from LAPACK to the "
            "maths library behind every sine, are built on Wilkinson's analysis and minimax polynomials. Machine "
            "learning trains in bfloat16 and FP8. And since the FDIV bug, chip makers prove their floating-point "
            "units correct by machine."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Write $-37$ as an 8-bit two's complement number, \ and show that $x \mapsto \bar x + 1$ fixes only $0$ "
            r"and $-128$.",
            r"Prove that a signed addition overflows exactly when the carry into the top bit differs from the carry "
            r"out of it.",
            r"Show that a Kogge--Stone network on $n = 2^k$ positions has $n k - n + 1$ combines \ (49 for $n = 16$).",
            r"Show that, bit by bit, \ $x + y + z = (x \oplus y \oplus z) + 2\,\mathrm{maj}(x, y, z)$: \ carry-save "
            r"addition.",
            r"How many float32 values lie in $[1, 2)$? \ Why is $0.5 + 0.25 = 0.75$ exact, \ but $0.1 + 0.2 \ne 0.3$?",
            r"\textit{Build.} \ With \texttt{explainer/cs/pebble/blocks.py}, \ make an 8-bit carry-select adder with "
            r"blocks of 2, 3 and 3 bits; \ verify it on all inputs \ and compare its gates and delay with ripple and "
            r"Kogge--Stone.",
            r"$\bigstar$ \textit{Research.} \ Find the \texttt{float32} $x$ whose $e^x$ lies nearest a rounding "
            r"midpoint. \ How many bits must an \texttt{expf} compute to round every input correctly?",
        ], font_size=22)
        with self.voiceover(
            "Seven problems, with full solutions in the part's notes. Pause on any of them. The sixth is a build "
            "problem: it asks you to use this series' arithmetic library yourself. The last, marked with a star, is a "
            "research problem: a search over every single-precision number, the kind that underlies correctly "
            "rounded libraries."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 5, \ Memory and Time", font_size=44).to_edge(UP, buff=0.6)
        loop = VGroup(gate_pair()).move_to(DOWN * 0.3)
        q = label(r"how does a circuit remember?", font_size=30, color=HEAD).next_to(loop, DOWN, buff=0.5)
        with self.voiceover(
            "Next time: memory and time. Every circuit in this part forgets its answer the moment its inputs change. "
            "Feed a gate's output back into its own input, and it can remember. Part 5 builds latches and flip-flops, "
            "the clock that keeps them in step, the strange physics of metastability, finite state machines, and the "
            "registers and memories Pebble will run on."
        ):
            self.play(FadeIn(nxt), FadeIn(loop), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Harris and Harris, \textit{Digital Design and Computer Architecture}, ch. 1 and 5",
             r"Parhami, \textit{Computer Arithmetic}; \ Koren, \textit{Computer Arithmetic Algorithms}",
             r"Goldberg, ``What Every Computer Scientist Should Know About Floating-Point Arithmetic'' (1991)",
             r"Higham, \textit{Accuracy and Stability of Numerical Algorithms}, ch. 1--4",
             r"Muller et al., \textit{Handbook of Floating-Point Arithmetic}; \ Overton, \textit{Numerical Computing "
             r"with IEEE Floating Point Arithmetic}",
             r"Knuth, \textit{The Art of Computer Programming}, vol. 2, \S 4.1--4.3"],
            [r"Sklansky (1960); \ Kogge and Stone (1973); \ Brent and Kung (1982); \ Snir (1986)",
             r"Booth (1951); \ MacSorley (1961); \ Wallace (1964); \ Dadda (1965)",
             r"Robertson (1958); \ Tocher (1958); \ Edelman, ``The mathematics of the Pentium division bug'' (1997)",
             r"Volder, ``The CORDIC trigonometric computing technique'' (1959); \ Payne and Hanek (1983)",
             r"Wilkinson, \textit{Rounding Errors in Algebraic Processes} (1963) and ``The perfidious polynomial'' "
             r"(1984); \ IEEE 754 (1985, 2008, 2019)",
             r"GAO, IMTEC-92-26 (1992); \ Lions et al., \textit{Ariane 5 Flight 501 Failure} (1996)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()


def gate_pair():
    """Two cross-coupled NOR gates: the latch of Part 5."""
    from videos.cs.cs4.common import WIRE, gate
    g1 = gate("NOR", size=0.9).move_to(UP * 0.75)
    g2 = gate("NOR", size=0.9).move_to(DOWN * 0.75)

    def cross(o, i, dy):
        pts = [o, o + RIGHT * 0.35, [o[0] + 0.35, dy, 0], [i[0] - 0.35, -dy, 0], [i[0] - 0.35, i[1], 0], i]
        return VMobject(color=WIRE, stroke_width=3).set_points_as_corners([np.asarray(p, float) for p in pts])

    w1 = cross(g1.out(), g2.inp[0](), 0.25)
    w2 = cross(g2.out(), g1.inp[1](), -0.25)
    ins = VGroup(Line(g1.inp[0]() + LEFT * 0.7, g1.inp[0](), color=WIRE, stroke_width=3),
                 Line(g2.inp[1]() + LEFT * 0.7, g2.inp[1](), color=WIRE, stroke_width=3))
    return VGroup(g1, g2, w1, w2, ins)
