from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def t(s):
    if s is None:
        return r"---"
    return f"{s * 1e6:.0f} µs" if s < 1e-3 else (f"{s * 1000:.1f} ms" if s < 1 else f"{s:.2f} s")


class FftTwo(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.butterflies()
        self.inverse()
        self.measured()

    def card(self):
        card = chapter_card(6, r"The FFT, \ II: \ butterflies", r"What does the recursion look like unrolled?",
                            lit=(1965,), extra=((1965, r"Cooley and Tukey"), (1984, r"Gauss's notes found")),
                            part=PART)
        with self.voiceover("Chapter six. The fast Fourier transform, part two: butterflies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def history(self):
        head = label(r"Twice discovered", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"c. 1805: \ Carl Friedrich Gauss interpolates the orbits of the asteroids Pallas and Juno, \\ "
                  r"and splits the sums exactly this way; \ published after his death, \ in Latin", font_size=21,
                  color=GREY_A),
            label(r"1963: \ John Tukey, \ at President Kennedy's science advisory committee, \\ describes the idea "
                  r"to Richard Garwin of IBM", font_size=21, color=GREY_A),
            label(r"the motive: \ detecting Soviet nuclear tests from seismometer readings, \ fast", font_size=21,
                  color=HEAD),
            label(r"1965: \ James Cooley programs it; \ Cooley and Tukey publish", font_size=22, color=YES),
            label(r"1984: \ Heideman, \ Johnson and Burrus trace it back to Gauss", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The algorithm was found twice. <bookmark mark='a'/> Around 1805 Carl Friedrich Gauss, fitting the "
            "orbits of the newly found asteroids Pallas and Juno, split his trigonometric sums in exactly this way. "
            "He never published it; it appeared after his death, in Latin, and was forgotten. <bookmark mark='b'/> "
            "In 1963 the statistician John Tukey, sitting on President Kennedy's science advisory committee, "
            "sketched the idea to Richard Garwin of IBM. <bookmark mark='c'/> Garwin wanted it for a pressing "
            "reason: to detect Soviet nuclear tests from seismometer recordings, which meant Fourier transforms of "
            "long signals, quickly. <bookmark mark='d'/> He had James Cooley program it, and Cooley and Tukey's "
            "paper of 1965 became one of the most cited in mathematics. <bookmark mark='e'/> In 1984 Michael "
            "Heideman, Don Johnson and Sidney Burrus found Gauss's version in his collected works."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def butterflies(self):
        head = label(r"Unrolled: \ the butterfly network", font_size=34).to_edge(UP, buff=0.3)
        n, lv = 8, 3
        xs = [-5.6 + 2.0 * s for s in range(lv + 1)]
        ys = [2.1 - 0.6 * i for i in range(n)]
        rev = [int(f"{i:03b}"[::-1], 2) for i in range(n)]
        cols = [DATA, YES, HEAD]
        nodes = VGroup(*[VGroup(*[Dot([x, y, 0], radius=0.06, color=GREY_B) for y in ys]) for x in xs])
        inl = VGroup(*[mono(f"a{rev[i]}", 16, DATA).next_to([xs[0], ys[i], 0], LEFT, buff=0.2) for i in range(n)])
        outl = VGroup(*[mono(f"A{i}", 16, YES).next_to([xs[-1], ys[i], 0], RIGHT, buff=0.2) for i in range(n)])
        stages = VGroup()
        for s in range(lv):
            half = 2 ** s
            g = VGroup()
            for start in range(0, n, 2 * half):
                for k in range(half):
                    i, j = start + k, start + k + half
                    for a, b in ((i, i), (i, j), (j, i), (j, j)):
                        g.add(Line([xs[s], ys[a], 0], [xs[s + 1], ys[b], 0], color=cols[s], stroke_width=1.6))
            stages.add(g)
        bitrev = VGroup(*[mono(f"{i:03b}", 14, GREY_B).next_to(inl[i], LEFT, buff=0.15) for i in range(n)])
        side = VGroup(
            label(r"inputs in \textbf{bit-reversed} order: \\ 1 = 001 goes to 4 = 100", font_size=20, color=GREY_A),
            label(r"each stage: \ $n/2$ butterflies, \\ one twiddle multiply and an add and subtract", font_size=20,
                  color=HEAD),
            label(r"$\lg n$ stages: \ $\frac{n}{2} \lg n$ butterflies, \\ done in place", font_size=21, color=YES),
            label(r"the same wiring as Part 10's sorting networks \\ and parallel prefix", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Unroll the recursion and it becomes a network. <bookmark mark='a'/> The recursion splits by the last "
            "bit of the index first, then the next, so the inputs arrive in bit-reversed order: index one, binary "
            "zero zero one, sits where four, one zero zero, would. <bookmark mark='b'/> Then come log n stages. "
            "In each, pairs of values are combined by a butterfly: one multiplication by a twiddle factor, one "
            "addition, one subtraction. The first stage pairs neighbours, the next pairs at distance two, then four. "
            "<bookmark mark='c'/> n over two butterflies per stage, log n stages, and every value is overwritten in "
            "place, so the transform needs no extra memory. <bookmark mark='d'/> It is the same wiring as the "
            "sorting networks and parallel prefix of Part 10, which is why FFTs run so well on parallel hardware."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(inl), FadeIn(outl))
            vo.wait_until("a")
            self.play(FadeIn(bitrev), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            for s in stages:
                self.play(Create(s), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def inverse(self):
        head = label(r"Going back", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"A_k = \sum_{j=0}^{n-1} a_j\,\omega^{jk} \qquad \text{(the DFT, as a matrix } F_{kj} = "
                    r"\omega^{jk}\text{)}", font_size=32),
            MathTex(r"\sum_{k=0}^{n-1} \omega^{(j - l)k} = \begin{cases} n & j = l \\ 0 & j \ne l \end{cases}",
                    font_size=34, color=YES),
            MathTex(r"F^{-1} = \tfrac{1}{n}\,\overline{F}: \qquad a_j = \frac{1}{n} \sum_k A_k\,\omega^{-jk}",
                    font_size=34, color=HEAD),
        ).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.6)
        why = label(r"the powers of a root of unity other than 1 sum to zero: \ they are spread evenly round the "
                    r"circle", font_size=21, color=GREY_A).next_to(eqs[1], DOWN, buff=0.25)
        out = label(r"so the inverse is the same FFT with $\omega^{-1}$, \ divided by $n$", font_size=23,
                    color=LAM).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why is the inverse so cheap? <bookmark mark='a'/> Write the transform as a matrix whose entries are "
            "powers of omega. <bookmark mark='b'/> Multiply a row of it by a conjugated row. If the rows are the "
            "same, every term is one and the sum is n. If not, the terms are the powers of some root of unity other "
            "than one, spread evenly around the circle, and they cancel to zero. <bookmark mark='c'/> So the "
            "matrix's inverse is its own conjugate divided by n, the rows are orthogonal, and transforming back is "
            "the same fast algorithm with omega replaced by its inverse. <bookmark mark='d'/> This orthogonality of "
            "characters is the algebraic heart of Fourier analysis, from Analysis, Built's ninth part to Part 53's "
            "quantum computers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("fft")
        head = label(r"$n^2$ against $n \log n$, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['dft_products']:,}", f"{r['butterflies']:,}", t(r["dft_s"]), t(r["fft_s"]),
                 t(r["numpy_s"])] for r in d["rows"] if r["n"] >= 64]
        tab = grid_table([r"$n$", r"DFT products", r"butterflies", r"DFT, \ Python", r"FFT, \ Python",
                          r"FFT, \ numpy"], rows, widths=[1.4, 2.4, 2.0, 2.2, 2.2, 2.0], row_h=0.44, font_size=19,
                         colors=[[WHITE, NO, YES, NO, YES, LAM]] * len(rows)).next_to(head, DOWN, buff=0.45)
        last = [r for r in d["rows"] if r["dft_s"]][-1]
        big = d["big"][-1]
        pts = VGroup(
            label(rf"at {words(last['n'])} points: \ the same numbers \ (to {last['max_diff']:.0e}), \ "
                  rf"{last['dft_s'] / last['fft_s']:.0f}$\times$ faster in the same Python", font_size=21,
                  color=YES),
            label(rf"numpy's compiled FFT: \ {words(big['n'])} points in {t(big['numpy_s'])}", font_size=21,
                  color=LAM),
            label(r"every phone call, \ photograph, \ MRI scan and Wi-Fi packet passes through one", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Measured on this machine. <bookmark mark='a'/> The direct transform does n squared multiplications, "
            "the fast one n over two log n butterflies. At two thousand points, written in the same plain Python, "
            "they agree to ten decimal places and the fast one is almost three hundred times faster. <bookmark "
            "mark='b'/> Numpy's compiled FFT transforms four million points in under half a second. <bookmark "
            "mark='c'/> It runs inside every phone call, every compressed photograph, every MRI scan and every "
            "Wi-Fi packet, which is why it is often called the most important algorithm of the twentieth century."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
