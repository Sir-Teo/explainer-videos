from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono

EL, AZ = math.radians(18), math.radians(25)
R_VEC = np.array([-math.sin(AZ), math.cos(AZ), 0.0])
U_VEC = np.array([-math.sin(EL) * math.cos(AZ), -math.sin(EL) * math.sin(AZ), math.cos(EL)])
D_VEC = np.array([math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL)])


class Bloch(VGroup):
    """A Bloch sphere drawn in 2D: an orthographic view from slightly above, Bloch x toward the viewer (left),
    y to the right, z up.  Back halves of the circles are dimmed."""

    def __init__(self, center=ORIGIN, radius=2.0, labels=("0", "1", "+", "+i"), font_size=24):
        super().__init__()
        self.c = np.array(center, dtype=float)
        self.r = radius
        self.add(Circle(radius=radius, color=GREY_C, stroke_width=2).move_to(self.c))
        for fn in (lambda t: (math.cos(t), math.sin(t), 0.0), lambda t: (math.sin(t), 0.0, math.cos(t))):
            self.add(self._circle(fn))
        for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            a = np.array(v, dtype=float) * 1.12
            self.add(DashedLine(self.p(-a), self.p(a), color=GREY_D, stroke_width=1.5, dash_length=0.07))
        pos = {"0": (0, 0, 1), "1": (0, 0, -1), "+": (1, 0, 0), "+i": (0, 1, 0)}
        for k in labels:
            v = np.array(pos[k], dtype=float)
            t = MathTex(rf"|{k}\rangle", font_size=font_size, color=GREY_A)
            out = self.p(v) - self.c
            t.move_to(self.p(v) + out / (np.linalg.norm(out) + 1e-9) * 0.38)
            if k == "+i":
                t.move_to([self.c[0] + radius + 0.42, self.p(v)[1], 0])
            self.add(t)

    def p(self, v):
        v = np.asarray(v, dtype=float)
        return self.c + self.r * (np.dot(v, R_VEC) * RIGHT + np.dot(v, U_VEC) * UP)

    def front(self, v) -> bool:
        return float(np.dot(v, D_VEC)) >= 0

    def _circle(self, fn, n=96):
        g = VGroup()
        ts = [2 * math.pi * k / n for k in range(n + 1)]
        for a, b in zip(ts, ts[1:]):
            va, vb = np.array(fn(a)), np.array(fn(b))
            on = self.front((va + vb) / 2)
            g.add(Line(self.p(va), self.p(vb), color=GREY_B if on else GREY_D, stroke_width=1.8 if on else 1.2,
                       stroke_opacity=0.9 if on else 0.45))
        return g


GATE_COL = {"H": HEAD, "T": DATA, "Td": LAM, "S": DATA}
GATE_TEX = {"H": r"H", "T": r"T", "Td": r"T^\dagger", "S": r"S"}


def circuit(columns, nq, x0, dx, y0, dy, wire_len=None, size=26, box=0.5):
    """Wires and gates.  ``columns`` is a list of columns, each a list of ops: ("H", q), ("T", q), ("Td", q),
    ("C", control, target) or ("M", q).  Returns (wires, gates by column)."""
    ys = [y0 - i * dy for i in range(nq)]
    x1 = x0 + dx * (len(columns) + 1) if wire_len is None else x0 + wire_len
    wires = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=2) for y in ys])
    cols = VGroup()
    for j, col in enumerate(columns):
        x = x0 + dx * (j + 1)
        g = VGroup()
        for op in col:
            if op[0] == "C":
                yc, yt = ys[op[1]], ys[op[2]]
                sgn = 1 if yt < yc else -1
                g.add(Line([x, yc, 0], [x, yt - sgn * 0.18, 0], color=WHITE, stroke_width=2.2),
                      Dot([x, yc, 0], radius=0.08, color=WHITE),
                      Circle(radius=0.18, color=WHITE, stroke_width=2.2).move_to([x, yt, 0]),
                      Line([x - 0.18, yt, 0], [x + 0.18, yt, 0], color=WHITE, stroke_width=2.2),
                      Line([x, yt - 0.18, 0], [x, yt + 0.18, 0], color=WHITE, stroke_width=2.2))
            elif op[0] == "M":
                y = ys[op[1]]
                r = Rectangle(width=box + 0.1, height=box, stroke_color=KERN, stroke_width=2, fill_color=BG,
                              fill_opacity=1).move_to([x, y, 0])
                arc = Arc(radius=0.17, start_angle=PI / 6, angle=2 * PI / 3, color=KERN, stroke_width=2).move_to(
                    [x, y - 0.03, 0])
                g.add(r, arc, Line([x, y - 0.12, 0], [x + 0.15, y + 0.13, 0], color=KERN, stroke_width=2))
            else:
                y = ys[op[1]]
                c = GATE_COL[op[0]]
                r = Square(side_length=box, stroke_color=c, stroke_width=2.2, fill_color=BG,
                           fill_opacity=1).move_to([x, y, 0])
                g.add(r, MathTex(GATE_TEX[op[0]], font_size=size, color=c).move_to(r))
        cols.add(g)
    return wires, cols, ys


class Circuits(VoiceoverScene):
    def construct(self):
        self.card()
        self.reading()
        self.exact()
        self.dense()
        self.kitaev()
        self.simulator()
        self.practice()

    def card(self):
        card = chapter_card(4, r"Circuits and universality", r"Which gates are enough?", lit=(1989, 1995, 1997),
                            extra=((1989, r"Deutsch: \ quantum circuits"),
                                   (1995, r"Barenco et al.: \ CNOT and one-qubit gates"),
                                   (1997, r"Kitaev: \ the Solovay--Kitaev theorem")), part=PART)
        with self.voiceover("Chapter four. Circuits and universality. Which gates are enough?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def reading(self):
        head = label(r"Reading a circuit", font_size=36).to_edge(UP, buff=0.3)
        wires, cols, ys = circuit([[("H", 0)], [("C", 0, 1)], [("T", 1)], [("M", 0), ("M", 1)]], 2, -3.6, 1.45,
                                  2.2, 0.85)
        kets = VGroup(*[MathTex(r"|0\rangle", font_size=28, color=GREY_A).next_to([-3.6, y, 0], LEFT, buff=0.1)
                        for y in ys])
        us = VGroup(*[MathTex(rf"U_{i + 1}", font_size=26, color=GREY_B).move_to([-3.6 + 1.45 * (i + 1), ys[1] - 0.6,
                                                                                    0]) for i in range(3)])
        time = Arrow([-3.6, ys[0] + 0.6, 0], [2.6, ys[0] + 0.6, 0], buff=0, color=GREY_D, stroke_width=2,
                     max_tip_length_to_length_ratio=0.03)
        tl = label(r"time", font_size=17, color=GREY_B).next_to(time, RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(r"|\psi_{\text{out}}\rangle", r"=", r"U_3", r"U_2", r"U_1", r"|00\rangle", font_size=34),
            MathTex(r"U_1", r"=", r"H \otimes I", font_size=34),
            MathTex(r"U_1", r"=", r"\tfrac{1}{\sqrt2}\begin{pmatrix} 1&0&1&0\\0&1&0&1\\1&0&-1&0\\0&1&0&-1"
                    r"\end{pmatrix}", font_size=30),
        )
        rows[0].move_to([-3.2, -0.55, 0])
        rows[1].next_to(rows[0], DOWN, buff=0.6).align_to(rows[0], LEFT)
        rows[2].move_to([3.6, -1.35, 0])
        whys = VGroup(
            label(r"circuits read left to right; \ matrices act right to left", font_size=18, color=GREY_B),
            label(r"$H$ on the first qubit, \ nothing on the second", font_size=18, color=GREY_B),
            wrapped_label(r"each entry of $H$ times a copy of $I$: \ $n$ qubits make $2^n \times 2^n$ matrices", 4.6,
                          font_size=18, color=HEAD),
        )
        whys[0].next_to(rows[0], DOWN, buff=0.12).align_to(rows[0], LEFT)
        whys[1].next_to(rows[1], DOWN, buff=0.12).align_to(rows[1], LEFT)
        whys[2].next_to(rows[2], DOWN, buff=0.15)
        with self.voiceover(
            "Deutsch's quantum circuit model of 1989 is the standard one. <bookmark mark='a'/> Each wire is a qubit, "
            "and time runs left to right: here a Hadamard, a CNOT, a T gate, and measurements. <bookmark mark='b'/> "
            "Each step is a unitary matrix and the circuit is their product. Matrices act right to left, so the "
            "first gate is written last. <bookmark mark='c'/> A gate on one qubit of two is a tensor product with "
            "the identity. <bookmark mark='d'/> Written out, each entry of H multiplies a copy of the identity: four "
            "by four. With n qubits these matrices are two to the n on a side, so no simulator builds them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(wires), FadeIn(kets), FadeIn(time), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(us), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def exact(self):
        head = label(r"Toffoli from $H$, \ $T$ and CNOT", font_size=36).to_edge(UP, buff=0.3)
        seq = [[("H", 2)], [("C", 1, 2)], [("Td", 2)], [("C", 0, 2)], [("T", 2)], [("C", 1, 2)], [("Td", 2)],
               [("C", 0, 2)], [("T", 1), ("T", 2)], [("H", 2)], [("C", 0, 1)], [("T", 0), ("Td", 1)], [("C", 0, 1)]]
        wires, cols, ys = circuit(seq, 3, -3.7, 0.72, 1.9, 0.85, size=22, box=0.46)
        tx = -5.6
        tof = VGroup(*[Line([tx - 0.6, y, 0], [tx + 0.6, y, 0], color=GREY_B, stroke_width=2) for y in ys],
                     Line([tx, ys[0], 0], [tx, ys[2] - 0.18, 0], color=WHITE, stroke_width=2.2),
                     Dot([tx, ys[0], 0], radius=0.08), Dot([tx, ys[1], 0], radius=0.08),
                     Circle(radius=0.18, color=WHITE, stroke_width=2.2).move_to([tx, ys[2], 0]),
                     Line([tx - 0.18, ys[2], 0], [tx + 0.18, ys[2], 0], stroke_width=2.2),
                     Line([tx, ys[2] - 0.18, 0], [tx, ys[2] + 0.18, 0], stroke_width=2.2))
        eq = MathTex(r"=", font_size=40).move_to([-4.45, ys[1], 0])
        n_c = sum(1 for c in seq for op in c if op[0] == "C")
        n_t = sum(1 for c in seq for op in c if op[0] in ("T", "Td"))
        n_h = sum(1 for c in seq for op in c if op[0] == "H")
        counts = label(rf"{n_c} CNOTs, \ {n_t} $T$ or $T^\dagger$, \ {n_h} $H$: \ multiplied out on our simulator, \ "
                       r"exactly Toffoli's permutation", font_size=20, color=YES).next_to(wires, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"Barenco et al. \ (1995): \ CNOT together with all one-qubit gates builds \textbf{any} "
                          r"unitary exactly; \ the two-qubit gate is essential, \ the rest are rotations", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"but ``all one-qubit gates'' is a continuum: \ a real machine offers a short, \ fixed "
                          r"menu, \ and every gate in it must be made reliable", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        src = note(r"the textbook construction \ (Nielsen and Chuang)", font_size=16).next_to(counts, DOWN, buff=0.15)
        with self.voiceover(
            "Which gates do we need? <bookmark mark='a'/> Take chapter one's Toffoli gate. <bookmark mark='b'/> It "
            "can be built from Hadamards, T gates and their inverses, and CNOTs. <bookmark mark='c'/> Six CNOTs, "
            "seven T gates and two Hadamards; multiplied out on our simulator, it is exactly Toffoli's permutation. "
            "So anything a classical computer does, a quantum computer can do. <bookmark mark='d'/> In 1995 Adriano "
            "Barenco and colleagues showed that CNOT with arbitrary one-qubit gates builds any unitary exactly. "
            "<bookmark mark='e'/> The catch is the word arbitrary: one-qubit gates form a continuum, but a real "
            "machine offers a short, fixed menu."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tof))
            vo.wait_until("b")
            self.play(FadeIn(eq), Create(wires))
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.2), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(counts), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def dense(self):
        head = label(r"Two gates approximate every rotation", font_size=36).to_edge(UP, buff=0.3)
        B = Bloch(center=[-3.4, -0.45, 0], radius=2.35)
        Hm = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
        Tm = np.diag([1, np.exp(1j * math.pi / 4)])
        R = Tm @ Hm @ Tm @ Hm
        psi = np.array([1, 0], dtype=complex)
        pts = []
        for _ in range(160):
            psi = R @ psi
            a, b = psi
            pts.append((float(2 * (np.conj(a) * b).real), float(2 * (np.conj(a) * b).imag),
                        float(abs(a) ** 2 - abs(b) ** 2)))
        dots = VGroup(*[Dot(B.p(p), radius=0.05, color=HEAD if B.front(p) else GREY_C) for p in pts])
        start = Dot(B.p((0, 0, 1)), radius=0.08, color=YES)
        c8, s8 = math.cos(math.pi / 8), math.sin(math.pi / 8)
        n = np.array([c8, s8, c8]) / math.sqrt(2 * c8 * c8 + s8 * s8)
        axis = DashedLine(B.p(-1.15 * n), B.p(1.15 * n), color=KERN, stroke_width=2.5, dash_length=0.08)
        rows = VGroup(
            MathTex(r"R", r"=", r"T", r"\,H T H", font_size=34),
            MathTex(r"R", r"=", r"R_z(\tfrac{\pi}{4})", r"\,R_x(\tfrac{\pi}{4})", font_size=34),
            MathTex(r"\cos\tfrac{\theta}{2}", r"=", r"\cos^2\tfrac{\pi}{8}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.3, 1.55, 0])
        rows.shift(RIGHT * (0.5 - rows.get_left()[0]))
        whys = VGroup(label(r"up to a global phase: \ $HTH$ is an eighth turn about $x$", font_size=18,
                            color=GREY_B),
                      label(r"one rotation, \ by an angle $\theta$:", font_size=18, color=GREY_B),
                      label(r"an irrational fraction of a turn", font_size=18, color=HEAD))
        whys[0].next_to(rows[0], DOWN, buff=0.1).align_to(rows[0], LEFT)
        whys[1].next_to(rows[1], DOWN, buff=0.1).align_to(rows[1], LEFT)
        whys[2].next_to(rows[2], DOWN, buff=0.1).align_to(rows[2], LEFT)
        notes = VGroup(
            wrapped_label(r"its powers never repeat: \ they fill a circle around its axis; \ conjugating by $H$ "
                          r"gives a second axis, \ and products of the two come as close as we like to any "
                          r"rotation", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"without $T$, \ circuits of $H$, \ $S$ and CNOT can be simulated efficiently on a "
                          r"classical computer \ (Gottesman--Knill, \ 1998)", 6.0, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(whys[2], DOWN, buff=0.4).align_to(rows, LEFT)
        src = note(r"dots: \ the first 160 powers of $R$ applied to $|0\rangle$", font_size=16).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Can two fixed gates, H and T, approximate every rotation? <bookmark mark='a'/> Take the product T H T "
            "H. <bookmark mark='b'/> H T H is an eighth of a turn about x, and T an eighth of a turn about z. "
            "<bookmark mark='c'/> Together they make one rotation, by an angle that is an irrational fraction of a "
            "turn. <bookmark mark='d'/> So its powers never return to the start: applied again and again to zero, "
            "the points fill a circle around its axis densely. Conjugating by H gives a second axis, and products of "
            "the two approach any rotation. <bookmark mark='e'/> T is essential: without it, circuits of H, S and "
            "CNOT can be simulated efficiently on an ordinary computer. That is the Gottesman–Knill theorem."
        ) as vo:
            self.play(FadeIn(head), Create(B), FadeIn(start), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(whys[1]), FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(axis))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.04), run_time=5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def kitaev(self):
        head = label(r"How many gates for accuracy $\varepsilon$?", font_size=36).to_edge(UP, buff=0.3)
        names = [r"U_{k-1}", r"W^\dagger", r"V^\dagger", r"W", r"V"]
        blocks = VGroup()
        for i, nm in enumerate(names):
            r = RoundedRectangle(width=1.25, height=0.75, corner_radius=0.1, stroke_color=DATA if i == 0 else LAM,
                                 stroke_width=2, fill_color=BG, fill_opacity=1)
            blocks.add(VGroup(r, MathTex(nm, font_size=30, color=DATA if i == 0 else LAM).move_to(r)))
        blocks.arrange(RIGHT, buff=0.18).move_to([-2.6, 2.2, 0])
        wire = Line(blocks.get_left() + LEFT * 0.4, blocks.get_right() + RIGHT * 0.4, color=GREY_B, stroke_width=2)
        lvl = label(r"each block: \ the previous level's approximation", font_size=17, color=GREY_B).next_to(
            blocks, DOWN, buff=0.15)
        expl = wrapped_label(r"the leftover error of $U_{k-1}$ is a small rotation; \ write it as a commutator "
                             r"$V W V^\dagger W^\dagger$ of two rotations of size about $\sqrt{\varepsilon}$, \ each "
                             r"approximated one level down", 4.6, font_size=18, color=WHITE).move_to([4.4, 2.0, 0])
        expo = math.log(5) / math.log(1.5)
        rows = VGroup(
            MathTex(r"\varepsilon_k", r"\approx", r"\varepsilon_{k-1}^{3/2}", r",\qquad", r"\ell_k", r"=",
                    r"5\,\ell_{k-1}", font_size=32),
            MathTex(r"\varepsilon_k", r"\approx", r"\varepsilon_0^{(3/2)^k}", r",\qquad", r"\ell_k", r"=",
                    r"5^k\,\ell_0", font_size=32),
            MathTex(r"(3/2)^k", r"\approx", r"\frac{\log(1/\varepsilon)}{\log(1/\varepsilon_0)}", font_size=32),
            MathTex(r"\ell_k", r"\propto", r"5^k", r"=", r"\big((3/2)^k\big)^{\log 5 / \log(3/2)}", r"\propto",
                    rf"\log^{{{expo:.2f}}}(1/\varepsilon)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([-1.6, -0.62, 0])
        rows[3][6].set_color(HEAD)
        whys = VGroup(
            label(r"error to the power $\tfrac32$, \ five times the gates \ (constants ignored)", font_size=18,
                  color=GREY_B),
            label(r"unroll $k$ levels", font_size=18, color=GREY_B),
            label(r"levels needed for accuracy $\varepsilon$", font_size=18, color=GREY_B),
            label(r"polylogarithmic in $1/\varepsilon$", font_size=18, color=HEAD),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.35)
            if w.get_right()[0] > 6.85:
                w.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        foot = wrapped_label(r"Solovay and Kitaev, \ independently, \ 1990s; \ this recursion: \ Dawson and Nielsen; "
                             r"\ for $H$ and $T$, \ number-theoretic methods need only a multiple of "
                             r"$\log(1/\varepsilon)$ gates \ (Ross and Selinger, \ 2016)", 12.4, font_size=18,
                             color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "But we also want few gates. Robert Solovay and Alexei Kitaev showed, independently, that the count "
            "grows only like a power of log one over the accuracy. <bookmark mark='a'/> The proof is a recursion: "
            "approximate roughly, then cancel the small leftover error with a commutator of two rotations of about "
            "its square root, each approximated one level down. <bookmark mark='b'/> Each level raises the error to "
            "the power three halves and multiplies the length by five. <bookmark mark='c'/> Unroll k levels. "
            "<bookmark mark='d'/> Reaching accuracy epsilon needs three halves to the k to grow like log one over "
            "epsilon. <bookmark mark='e'/> So the length grows like that logarithm to the power about four. For H "
            "and T, later number-theoretic methods need only a multiple of the logarithm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(wire), LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), FadeIn(lvl))
            self.play(FadeIn(expl))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(Circumscribe(rows[3][6], color=HEAD), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def simulator(self):
        head = label(r"Our state-vector simulator", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "def apply(self, U, *qubits):",
            "    k = len(qubits)",
            "    t = self.v.reshape((2,) * self.n)",
            "    t = np.moveaxis(t, qubits, range(k))",
            "    sh = t.shape",
            "    t = (U @ t.reshape(2 ** k, -1)).reshape(sh)",
            "    t = np.moveaxis(t, range(k), qubits)",
            "    self.v = t.reshape(-1)",
        ], size=15).move_to([-3.5, 1.2, 0])
        cap = label(r"\texttt{explainer/cs/quantum/sim.py}", font_size=17, color=GREY_B).next_to(code, UP, buff=0.2)
        cap.align_to(code, LEFT)
        cells = VGroup()
        for i in range(8):
            r = Square(side_length=0.6, stroke_color=DATA, stroke_width=1.8, fill_color=DATA, fill_opacity=0.15)
            cells.add(VGroup(r, mono(format(i, "03b"), size=15, color=WHITE).move_to(r)))
        cells.arrange(RIGHT, buff=0.12).move_to([3.4, -0.2, 0])

        def arcs(bit, col):
            g = VGroup()
            for i in range(8):
                j = i ^ (1 << (2 - bit))
                if i < j:
                    g.add(ArcBetweenPoints(cells[i].get_top() + UP * 0.05, cells[j].get_top() + UP * 0.05,
                                           angle=-PI * 0.75, color=col, stroke_width=2.5))
            return g
        a1 = arcs(1, HEAD)
        a0 = arcs(0, LAM)
        l1 = label(r"a gate on qubit 1 mixes amplitudes in pairs differing in that bit", font_size=18,
                   color=HEAD).next_to(cells, DOWN, buff=0.3)
        l0 = label(r"qubit 0: \ pairs four apart, \ like a stage of Part 19's FFT butterfly", font_size=18,
                   color=LAM).next_to(l1, DOWN, buff=0.15)
        for t_ in (l1, l0):
            if t_.get_right()[0] > 6.85:
                t_.shift(LEFT * (t_.get_right()[0] - 6.85))
        notes = VGroup(
            wrapped_label(r"$n$ qubits: \ $2^n$ complex amplitudes, \ 16 bytes each; \ the state viewed as a "
                          r"$2 \times 2 \times \cdots \times 2$ array, \ a gate is one small matrix product along "
                          r"its axes", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"every gate streams through all $2^n$ numbers and does little arithmetic on each: \ "
                          r"memory-bound, \ on the wrong side of Part 9's roofline", 12.4, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every result in this part comes from a simulator of about a hundred lines. <bookmark mark='a'/> It "
            "keeps all two to the n amplitudes in one array. To apply a gate it views the array as a cube with one "
            "axis per qubit, moves the gate's axes to the front, multiplies by the small matrix, and moves them "
            "back. <bookmark mark='b'/> A gate on one qubit mixes amplitudes in pairs whose indices differ only in "
            "that qubit's bit. <bookmark mark='c'/> On the first qubit the partners are four apart: one stage of "
            "Part 19's FFT butterfly, back in chapter seven. <bookmark mark='d'/> Every gate streams through all the "
            "amplitudes, sixteen bytes each, doing little arithmetic on each: memory-bound, on the wrong side of "
            "Part 9's roofline."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(code))
            vo.wait_until("a")
            self.play(Indicate(code[3], color=HEAD), Indicate(code[5], color=HEAD), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(cells))
            self.play(Create(a1), FadeIn(l1))
            vo.wait_until("c")
            self.play(ReplacementTransform(a1, a0), FadeIn(l0))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def practice(self):
        b = load("bell")
        head = label(r"The same circuit, \ three ways", font_size=36).to_edge(UP, buff=0.3)

        def panel(title, lines, col, w=4.1):
            body = code_block(lines, size=14)
            t = label(title, font_size=20, color=col)
            inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            fr = RoundedRectangle(width=w, height=2.3, corner_radius=0.12, stroke_color=col, stroke_width=1.8,
                                  fill_color=BG, fill_opacity=1)
            inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
            return VGroup(fr, inner)
        panels = VGroup(
            panel(r"ours", ["s = State(2)", "s.apply(H, 0)", "s.cnot(0, 1)", "s.probs()"], YES),
            panel(r"Qiskit \ (IBM)", ["qc = QuantumCircuit(2)", "qc.h(0)", "qc.cx(0, 1)", "qc.measure_all()"], DATA),
            panel(r"Cirq \ (Google)", ["a, b = cirq.LineQubit.range(2)", "cirq.Circuit(", "    cirq.H(a),",
                                      "    cirq.CNOT(a, b),", "    cirq.measure(a, b))"], LAM),
        ).arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.45)
        amps = ", \\ ".join(f"{a[0]:.3f}" for a in b["amplitudes"])
        out = label(rf"our amplitudes for $|00\rangle, |01\rangle, |10\rangle, |11\rangle$: \ {amps}", font_size=21,
                    color=YES).next_to(panels, DOWN, buff=0.4)
        notes = VGroup(
            wrapped_label(r"a real device returns only samples of the measured bits, \ about half 00 and half 11, "
                          r"\ never the amplitudes", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"before running, \ a compiler rewrites the circuit into the machine's native gates and "
                          r"routes two-qubit gates to qubits that are physically connected", 12.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(out, DOWN, buff=0.4)
        with self.voiceover(
            "Real programs use libraries that build these same circuits. <bookmark mark='a'/> Here is chapter "
            "three's Bell circuit on our simulator, in IBM's Qiskit, and in Google's Cirq. <bookmark mark='b'/> Our "
            "simulator prints the amplitudes: nought point seven zero seven on zero zero and on one one. <bookmark "
            "mark='c'/> A real device never shows those. It returns samples of the measured bits, about half zero "
            "zero and half one one. <bookmark mark='d'/> And before a circuit runs, a compiler rewrites it into the "
            "machine's native gates, routing each two-qubit gate to physically connected qubits inserting swaps "
            "where needed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in panels], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(out))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG, DATA, HEAD)
