from __future__ import annotations

import cmath as cm
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load

PHASE_STOPS = (DATA, LAM, NO, YES)          # phase 0, pi/2, pi, 3pi/2, cyclically


def phase_color(phi: float):
    """A colour for a complex phase: 0 blue, a quarter turn purple, a half turn red, three quarters green."""
    t = (phi / (2 * math.pi)) % 1.0 * 4
    i = int(t) % 4
    return interpolate_color(ManimColor(PHASE_STOPS[i]), ManimColor(PHASE_STOPS[(i + 1) % 4]), t - int(t))


def phase_bars(amps, width=0.24, gap=0.08, scale=2.4):
    """Bars of |amplitude| on one baseline, coloured by phase; zero bars kept, invisible."""
    bars = VGroup()
    for i, a in enumerate(amps):
        m = abs(a)
        h = max(m * scale, 0.002)
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=phase_color(cm.phase(a)) if m > 1e-9
                      else GREY_D, fill_opacity=0.9 if m > 1e-9 else 0.0)
        r.move_to([i * (width + gap), 0, 0], aligned_edge=DOWN)
        bars.add(r)
    base = Line([-width, 0, 0], [(len(amps) - 1) * (width + gap) + width, 0, 0], color=GREY_C, stroke_width=1.5)
    return VGroup(base, bars)


def phase_legend(r=0.32, font_size=18):
    ring = Circle(radius=r, color=GREY_C, stroke_width=1.5)
    g = VGroup(ring)
    for k, t in enumerate((r"0", r"\tfrac{\pi}{2}", r"\pi", r"\tfrac{3\pi}{2}")):
        ang = k * PI / 2
        p = np.array([math.cos(ang), math.sin(ang), 0]) * r
        g.add(Dot(p, radius=0.07, color=PHASE_STOPS[k]))
        g.add(MathTex(t, font_size=font_size, color=PHASE_STOPS[k]).move_to(p * 1.85))
    return g


def dial(frac, color=HEAD, r=0.45):
    """A relative phase drawn as an arrow turned by ``frac`` of a full turn."""
    c = Circle(radius=r, color=GREY_C, stroke_width=1.5)
    a = Arrow(ORIGIN, r * np.array([math.cos(2 * PI * frac), math.sin(2 * PI * frac), 0]), buff=0, color=color,
              stroke_width=3, max_tip_length_to_length_ratio=0.3)
    zero = Line([r - 0.08, 0, 0], [r + 0.08, 0, 0], color=GREY_B, stroke_width=2)
    return VGroup(c, zero, a)


def sci(x: float) -> str:
    e = int(math.floor(math.log10(abs(x))))
    return rf"${x / 10 ** e:.1f} \times 10^{{{e}}}$"


def qft_circuit(n, x0, y0, dx=0.66, dy=0.62, box=0.5, size=22):
    """The textbook QFT circuit on n qubits: on qubit i, H then controlled R_k from each later qubit; then swaps.
    Returns (wires, list of gate groups in order, the wire ys)."""
    ys = [y0 - i * dy for i in range(n)]
    ops = []
    for i in range(n):
        ops.append(("H", i))
        for k in range(i + 1, n):
            ops.append(("R", i, k, k - i + 1))
    for i in range(n // 2):
        ops.append(("S", i, n - 1 - i))
    x1 = x0 + dx * (len(ops) + 1)
    wires = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=2) for y in ys])
    gates = []
    for j, op in enumerate(ops):
        x = x0 + dx * (j + 1)
        g = VGroup()
        if op[0] == "H":
            sq = Square(side_length=box, stroke_color=HEAD, stroke_width=2.2, fill_color=BG,
                        fill_opacity=1).move_to([x, ys[op[1]], 0])
            g.add(sq, MathTex(r"H", font_size=size + 2, color=HEAD).move_to(sq))
        elif op[0] == "R":
            _, t, c, k = op
            g.add(Line([x, ys[c], 0], [x, ys[t], 0], color=LAM, stroke_width=2),
                  Dot([x, ys[c], 0], radius=0.07, color=LAM))
            sq = Square(side_length=box, stroke_color=LAM, stroke_width=2.2, fill_color=BG,
                        fill_opacity=1).move_to([x, ys[t], 0])
            g.add(sq, MathTex(rf"R_{k}", font_size=size, color=LAM).move_to(sq))
        else:
            _, a, b = op
            g.add(Line([x, ys[a], 0], [x, ys[b], 0], color=KERN, stroke_width=2))
            for q in (a, b):
                g.add(Line([x - 0.12, ys[q] - 0.12, 0], [x + 0.12, ys[q] + 0.12, 0], color=KERN, stroke_width=2.5),
                      Line([x - 0.12, ys[q] + 0.12, 0], [x + 0.12, ys[q] - 0.12, 0], color=KERN, stroke_width=2.5))
        gates.append(g)
    return wires, gates, ys


class Qft(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.product()
        self.butterfly()
        self.count()
        self.catch()

    def card(self):
        card = chapter_card(7, r"The quantum Fourier transform", r"Can $2^n$ amplitudes be transformed with $n^2$ "
                            r"gates?", lit=(1965, 1994),
                            extra=((1965, r"Cooley and Tukey: \ the FFT"),
                                   (1994, r"Coppersmith: \ the QFT circuit")), part=PART)
        with self.voiceover("Chapter seven. The quantum Fourier transform. Can two to the n amplitudes be transformed "
                            "with about n squared gates?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the definition
    def definition(self):
        head = label(r"The discrete Fourier transform, \ on amplitudes", font_size=36).to_edge(UP, buff=0.3)
        N = 8
        eq = MathTex(r"\mathrm{QFT}\,|j\rangle", r"=", r"\frac{1}{\sqrt N}\sum_{k=0}^{N-1} \omega^{jk}\,|k\rangle,",
                     r"\qquad \omega = e^{2\pi i/N}", font_size=34).next_to(head, DOWN, buff=0.35)
        # the clock of the eighth roots of unity
        cc = np.array([-4.7, -0.55, 0])
        R = 1.35
        clock = VGroup(Circle(radius=R, color=GREY_C, stroke_width=1.5).move_to(cc))
        for k in range(N):
            ang = 2 * PI * k / N
            p = cc + R * np.array([math.cos(ang), math.sin(ang), 0])
            clock.add(Dot(p, radius=0.07, color=phase_color(ang)))
            clock.add(MathTex(rf"\omega^{k}" if k else r"1", font_size=22, color=phase_color(ang)).move_to(
                cc + (R + 0.38) * np.array([math.cos(ang), math.sin(ang), 0])))
        cl = label(r"$N = 8$: \ the eighth roots of unity", font_size=18, color=GREY_B).next_to(clock, DOWN, buff=0.2)
        # the matrix, each entry an arrow at its phase
        cell = 0.4
        m0 = np.array([-0.35, 0.95, 0])
        grid = VGroup()
        rows = []
        for j in range(N):
            row = VGroup()
            for k in range(N):
                ang = 2 * PI * j * k / N
                c = m0 + np.array([(k + 0.5) * cell, -(j + 0.5) * cell, 0])
                row.add(Arrow(c, c + 0.16 * np.array([math.cos(ang), math.sin(ang), 0]), buff=0, stroke_width=2.2,
                              color=phase_color(ang), max_tip_length_to_length_ratio=0.45, tip_length=0.08))
            rows.append(row)
            grid.add(row)
        frame = Rectangle(width=N * cell, height=N * cell, color=GREY_D, stroke_width=1.2).move_to(
            m0 + np.array([N * cell / 2, -N * cell / 2, 0]))
        jl = label(r"row $j$", font_size=18, color=GREY_B).next_to(frame, LEFT, buff=0.12)
        kl = label(r"column $k$", font_size=18, color=GREY_B).next_to(frame, DOWN, buff=0.12)
        notes = VGroup(
            wrapped_label(r"row $j$ turns $j/N$ of a turn per column: \ row 1 once round, \ row 2 twice", 3.2,
                          font_size=19, color=WHITE),
            wrapped_label(r"exactly Part 19's DFT matrix $\omega^{jk}$, \ scaled by $1/\sqrt N$ so that it is "
                          r"unitary", 3.2, font_size=19, color=HEAD),
            wrapped_label(r"a classical FFT needs $N \log_2 N$ operations on $N = 2^n$ numbers", 3.2, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(frame, RIGHT, buff=0.45)
        with self.voiceover(
            "Part 19 met the discrete Fourier transform, and the fast algorithm that computes it. "
            "<bookmark mark='a'/> The quantum version is the same transform applied to amplitudes: basis state j goes "
            "to an equal superposition of every k, with phase omega to the j k. <bookmark mark='b'/> Omega is a root "
            "of unity, a fraction of a turn round the circle; for eight points, an eighth of a turn. "
            "<bookmark mark='c'/> Draw each entry of the matrix as an arrow at its phase. Row one turns an eighth of a "
            "turn per column, row two a quarter, and so on. <bookmark mark='d'/> It is exactly Part 19's matrix, scaled by "
            "one over root N so that it is unitary. Classically, the FFT needs about N log N "
            "operations on N numbers. For two to the n numbers, that is exponential in n."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Create(clock[0]), LaggedStart(*[FadeIn(m) for m in clock[1:]], lag_ratio=0.08), FadeIn(cl),
                      run_time=2)
            vo.wait_until("c")
            self.play(Create(frame), FadeIn(jl), FadeIn(kl))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=2.5)
            self.play(Indicate(rows[1], color=WHITE, scale_factor=1.05), FadeIn(notes[0]))
            self.play(Indicate(rows[2], color=WHITE, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the product formula
    def product(self):
        head = label(r"The output is a product of single qubits", font_size=36).to_edge(UP, buff=0.3)
        fs = 28
        rows = VGroup(
            MathTex(r"\mathrm{QFT}\,|j\rangle", r"=", r"\frac{1}{\sqrt{2^n}}\sum_{k}", r"e^{2\pi i\, jk/2^n}",
                    r"|k\rangle", font_size=fs),
            MathTex(r"=", r"\frac{1}{\sqrt{2^n}}\sum_{k_1, \dots, k_n}", r"\bigotimes_{l=1}^{n}",
                    r"e^{2\pi i\, j k_l/2^l}", r"|k_l\rangle", font_size=fs),
            MathTex(r"=", r"\bigotimes_{l=1}^{n}", r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\, j/2^l}|1\rangle\big)",
                    font_size=fs),
            MathTex(r"=", r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\, 0.j_n}|1\rangle\big)", r"\otimes",
                    r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\, 0.j_{n-1}j_n}|1\rangle\big)", r"\otimes \cdots \otimes",
                    r"\tfrac{1}{\sqrt2}\big(|0\rangle + e^{2\pi i\, 0.j_1 \cdots j_n}|1\rangle\big)", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.35)
        rows.set_x(0)
        for r in rows[1:]:
            r.shift(RIGHT * (rows[0][1].get_x() - r[0].get_x()))
        if rows.get_right()[0] > 6.85:
            rows.shift(LEFT * (rows.get_right()[0] - 6.85))
        if rows.get_left()[0] < -6.85:
            rows.shift(RIGHT * (-6.85 - rows.get_left()[0]))
        whys = VGroup(label(r"write $k$ in binary: \ $k = \sum_l k_l\, 2^{n-l}$, \ so $jk/2^n = \sum_l j k_l / 2^l$",
                            font_size=18, color=GREY_B),
                      label(r"a sum over all bit strings of a product is a product of sums", font_size=18,
                            color=GREY_B),
                      label(r"whole turns do nothing: \ $j/2^l$ keeps only the last $l$ bits of $j$, \ as a binary "
                            r"fraction", font_size=18, color=HEAD))
        for wl, r in zip(whys, rows[1:]):
            wl.next_to(r, DOWN, buff=0.08).align_to(rows[1][1], LEFT)
        # make room for the notes under rows 1 and 2
        rows[2].shift(DOWN * 0.3)
        whys[1].shift(DOWN * 0.3)
        rows[3].shift(DOWN * 0.6)
        whys[2].shift(DOWN * 0.6)
        whys[0].shift(DOWN * 0.0)
        # the example: j = 5 on three qubits
        fr = [(r"0.1", 1 / 2, r"\tfrac12"), (r"0.01", 1 / 4, r"\tfrac14"), (r"0.101", 5 / 8, r"\tfrac58")]
        dials = VGroup()
        for t, f, ft in fr:
            d = dial(f)
            cap = MathTex(rf"0.{t[2:]}_2 = {ft}", font_size=24, color=HEAD).next_to(d, DOWN, buff=0.12)
            dials.add(VGroup(d, cap))
        dials.arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.3).shift(RIGHT * 2.2)
        ex = wrapped_label(r"$j = 5 = 101_2$, \ $n = 3$: \ each output qubit's phase, \ in turns; \ no "
                           r"entanglement at all", 4.6, font_size=19, color=WHITE).next_to(dials, LEFT, buff=0.6)
        with self.voiceover(
            "Here is the fact that makes the quantum transform cheap. <bookmark mark='a'/> Write the output index k "
            "in binary. The phase of each term splits into one factor per bit of k, <bookmark mark='b'/> and a sum "
            "over all bit strings of a product is a product of sums. <bookmark mark='c'/> So the transform of a basis "
            "state is a product of n single qubits, each an equal mix of zero and one with its own phase. "
            "<bookmark mark='d'/> Whole turns do nothing, so the l-th qubit's phase only sees the last l bits of j, "
            "read as a binary fraction. <bookmark mark='e'/> For j equals five on three qubits: half a turn, a "
            "quarter turn, and five eighths. Nothing is entangled. Each output qubit needs only a Hadamard and a few "
            "rotations."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(ex), LaggedStart(*[FadeIn(d) for d in dials], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ butterflies and gates
    def butterfly(self):
        head = label(r"From Part 19's butterflies to gates", font_size=36).to_edge(UP, buff=0.3)
        N, nb = 8, 3
        X = [-6.2, -4.75, -3.3, -1.85]
        Y = [2.2 - 0.46 * i for i in range(N)]
        nodes = VGroup(*[VGroup(*[Dot([x, y, 0], radius=0.05, color=GREY_B) for y in Y]) for x in X])
        stages = VGroup()
        tw = VGroup()
        for s in range(nb):
            d = N >> (s + 1)
            g = VGroup()
            for i in range(N):
                j = i ^ d
                g.add(Line([X[s], Y[i], 0], [X[s + 1], Y[j], 0], color=HEAD, stroke_width=1.6))
                if i & d:
                    g.add(Line([X[s], Y[i], 0], [X[s + 1], Y[i], 0], color=HEAD, stroke_width=1.6))
                else:
                    g.add(Line([X[s], Y[i], 0], [X[s + 1], Y[i], 0], color=HEAD, stroke_width=1.6))
                # twiddles on the difference outputs, where nontrivial
                block = i % (2 * d)
                if block >= d and (block - d) > 0:
                    tw.add(Dot([X[s + 1] - 0.18, Y[i], 0], radius=0.07, color=LAM))
            stages.add(g)
        ins = VGroup(*[label(f"{i}", font_size=16, color=GREY_A).next_to([X[0], y, 0], LEFT, buff=0.12)
                       for i, y in enumerate(Y)])
        outs = VGroup(*[label(f"{int(format(i, '03b')[::-1], 2)}", font_size=16, color=KERN).next_to(
            [X[-1], y, 0], RIGHT, buff=0.12) for i, y in enumerate(Y)])
        bl = label(r"radix-2 FFT, \ $N = 8$", font_size=18, color=GREY_B).next_to(nodes, DOWN, buff=0.2)
        wires, gates, ys = qft_circuit(3, 0.0, 1.85, dx=0.78, dy=0.75)
        qk = VGroup(*[MathTex(rf"q_{i}", font_size=24, color=GREY_A).next_to([0.0, y, 0], LEFT, buff=0.1)
                      for i, y in enumerate(ys)])
        cl = label(r"the QFT circuit, \ $n = 3$", font_size=18, color=GREY_B).next_to(wires, DOWN, buff=0.35)
        notes = VGroup(
            wrapped_label(r"a stage of butterflies pairs entries that differ in one bit: \ exactly a Hadamard on "
                          r"that qubit \ (chapter 4's simulator)", 12.4, font_size=19, color=HEAD),
            wrapped_label(r"the twiddle factors $\omega^k$ depend on the other bits: \ controlled phase rotations "
                          r"$R_k = \mathrm{diag}(1, e^{2\pi i/2^k})$", 12.4, font_size=19, color=LAM),
            wrapped_label(r"in this form of the FFT the outputs come out in bit-reversed order: \ the final swaps", 12.4,
                          font_size=19,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The circuit comes straight from Part 19's fast Fourier transform. <bookmark mark='a'/> The FFT works in "
            "stages. Each stage combines entries in pairs that differ in one bit of their index: a butterfly. "
            "<bookmark mark='b'/> On a quantum computer, mixing every pair that differs in one bit is a single gate, "
            "a Hadamard on that qubit, as chapter four's simulator showed. <bookmark mark='c'/> Between stages the FFT "
            "multiplies by twiddle factors, powers of omega that depend on the other bits of the index. Those become "
            "phase rotations controlled by the other qubits. <bookmark mark='d'/> And in this form of the FFT the "
            "outputs emerge in bit-reversed order, which the circuit fixes with swaps at the end. Each stage of N "
            "over two butterflies has become a single Hadamard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(ins))
            vo.wait_until("a")
            for st in stages:
                self.play(Create(st), run_time=0.9)
            self.play(FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(wires), FadeIn(qk), FadeIn(cl))
            self.play(*[FadeIn(g) for g, op in zip(gates, range(len(gates))) if len(g) == 2], FadeIn(notes[0]),
                      Indicate(stages[0], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(tw), *[FadeIn(g) for g in gates if len(g) == 4], FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(outs), *[FadeIn(g) for g in gates if len(g) not in (2, 4)], FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ counting, and checking
    def count(self):
        q = load("qft")["rows"]
        head = label(r"$n(n+1)/2$ gates, \ plus swaps, \ for $2^n$ points", font_size=36).to_edge(UP, buff=0.3)
        n = 4
        wires, gates, ys = qft_circuit(n, -6.2, 2.25, dx=0.56, dy=0.5, box=0.42, size=18)
        qk = VGroup(*[MathTex(rf"q_{i}", font_size=22, color=GREY_A).next_to([-6.2, y, 0], LEFT, buff=0.08)
                      for i, y in enumerate(ys)])
        rows = VGroup(
            MathTex(r"n + (n-1) + \cdots + 1", r"=", r"\frac{n(n+1)}{2}", font_size=28),
            MathTex(r"+\;\lfloor n/2 \rfloor \text{ swaps}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 1.5, 0])
        if rows.get_right()[0] > 6.85:
            rows.shift(LEFT * (rows.get_right()[0] - 6.85))
        why = label(r"qubit $l$: \ one $H$ and $n - l$ rotations", font_size=18, color=GREY_B).next_to(
            rows, UP, buff=0.2).align_to(rows, LEFT)
        rows[0][2].set_color(HEAD)
        body = []
        for r in q:
            body.append([f"{r['n']}", f"{2 ** r['n']:,}", f"{r['gates']}", f"{r['fft_ops']:,}",
                         sci(r["max_diff_fft"])])
        tab = grid_table([r"$n$", r"points $2^n$", r"QFT gates", r"FFT: \ $N \log_2 N$",
                          r"largest difference"], body, widths=[0.9, 1.9, 1.9, 2.3, 2.9], row_h=0.4, font_size=19,
                         mono_cols=())
        for i in range(1, len(body) + 1):
            tab.cells[i][2].set_color(YES)
            tab.cells[i][3].set_color(NO)
            tab.cells[i][4].set_color(GREY_A)
        tab.move_to([-1.3, -1.45, 0])
        src = wrapped_label(r"our simulator's circuit against numpy's FFT, \ on a random state: \ the same numbers to "
                            r"rounding", 2.8, font_size=18, color=GREY_B).next_to(tab, RIGHT, buff=0.35)
        last = q[-1]
        foot = label(rf"$n = {last['n']}$: \ {last['gates']} gates against {last['fft_ops']:,} operations; \ "
                     r"the gap grows exponentially", font_size=20, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Count the gates. <bookmark mark='a'/> On four qubits: the first gets a Hadamard and three controlled "
            "rotations, the next a Hadamard and two, and so on down, then two swaps. <bookmark mark='b'/> Qubit l "
            "needs one Hadamard and n minus l rotations, so the total is n times n plus one over two, plus n over two "
            "swaps: order n squared gates for two to the n points. <bookmark mark='c'/> Our simulator runs this "
            "circuit on a random state and compares it with numpy's FFT. They agree to rounding error, about ten to "
            "the minus sixteen. <bookmark mark='d'/> On eight qubits the circuit has forty gates, where the FFT needs "
            "two thousand and forty-eight operations, and the gap grows exponentially with n."
        ) as vo:
            self.play(FadeIn(head), Create(wires), FadeIn(qk))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in gates], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(why), Write(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(src))
            vo.wait_until("d")
            self.play(*[Indicate(c, color=HEAD) for c in tab.cells[-1][2:4]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the catch
    def catch(self):
        head = label(r"What the QFT is good for", font_size=36).to_edge(UP, buff=0.3)
        N, r, x0 = 16, 4, 1
        inp = [complex(1 / math.sqrt(N // r)) if (x - x0) % r == 0 else 0j for x in range(N)]
        out = [sum(inp[x] * cm.exp(2j * math.pi * x * k / N) for x in range(N)) / math.sqrt(N) for k in range(N)]
        a_in = phase_bars(inp, scale=2.0).shift([-6.3, 0.9, 0])
        a_out = phase_bars(out, scale=2.0).shift([-6.3, -1.75, 0])
        xs = [b.get_x() for b in a_in[1]]
        t_in = VGroup(*[label(f"{x}", font_size=16, color=GREY_A).move_to([xs[x], 0.65, 0]) for x in (0, 1, 5, 9, 13)])
        t_out = VGroup(*[label(f"{k}", font_size=16, color=GREY_A).move_to([xs[k], -2.0, 0]) for k in (0, 4, 8, 12)])
        l_in = label(r"input: \ period 4 on 16 points, \ offset 1", font_size=18, color=GREY_A).next_to(
            a_in, UP, buff=0.15).align_to(a_in, LEFT)
        l_out = label(r"after the QFT: \ peaks at multiples of $16/4$", font_size=18, color=YES).next_to(
            t_out, DOWN, buff=0.12).set_x(a_out.get_x())
        arr = Arrow([xs[7], 0.35, 0], [xs[7], -0.55, 0], buff=0, color=GREY_B, stroke_width=3)
        al = label(r"QFT", font_size=20, color=HEAD).next_to(arr, RIGHT, buff=0.15)
        leg = VGroup(label(r"colour: \ phase", font_size=16, color=GREY_B), phase_legend()).arrange(DOWN, buff=0.25)
        leg.move_to([-0.6, -0.6, 0])
        ill = note(r"illustrative input; \ the amplitudes are exact", font_size=16).next_to(l_out, DOWN, buff=0.08)
        notes = VGroup(
            wrapped_label(r"the offset moves into the phases; \ the period moves into where the peaks are: \ "
                          r"\textbf{a measurement samples a multiple of $N/r$}, \ the heart of Shor \ (chapter 9)", 5.4,
                          font_size=19, color=YES),
            wrapped_label(r"but the $2^n$ Fourier coefficients cannot be read out: \ one run gives one sample $k$, \ "
                          r"with probability $|\text{amplitude}|^2$; \ and loading arbitrary data into amplitudes "
                          r"costs as much as the data", 5.4, font_size=19, color=NO),
            wrapped_label(r"Coppersmith \ (1994): \ drop the tiniest rotations and $O(n \log n)$ gates give a close "
                          r"approximation", 5.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.0, -0.2, 0])
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        with self.voiceover(
            "So what is it good for? <bookmark mark='a'/> Feed it a periodic state: four equal amplitudes, four apart, "
            "starting at one. <bookmark mark='b'/> After the transform, all the amplitude sits on multiples of sixteen "
            "over four, and everything between has interfered away. The offset has moved into the phases, shown "
            "here as colour, and the period into where the peaks are. <bookmark mark='c'/> A measurement then samples "
            "a multiple of N over r, which is exactly what Shor's algorithm needs in chapter nine. "
            "<bookmark mark='d'/> What it is not good for: reading out Fourier coefficients. One run yields one "
            "sample. And loading arbitrary data into amplitudes costs as much as the data. <bookmark mark='e'/> In "
            "1994 Don Coppersmith also showed that the tiniest rotations can be dropped, leaving order n log n "
            "gates for a close approximation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a_in), FadeIn(t_in), FadeIn(l_in))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(al))
            self.play(TransformFromCopy(a_in, a_out), run_time=1.5)
            self.play(FadeIn(t_out), FadeIn(l_out), FadeIn(ill), FadeIn(leg))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG, DATA, HEAD)
