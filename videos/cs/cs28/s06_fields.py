from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class Fields(VoiceoverScene):
    def construct(self):
        self.card()
        self.prime()
        self.gf256()
        self.which()

    def card(self):
        card = chapter_card(5, r"Finite fields", r"Can bytes be added, multiplied and divided?", lit=(1830, 1960),
                            extra=((1830, r"Galois"), (1960, r"Reed--Solomon")), part=PART)
        with self.voiceover("Chapter five. Finite fields."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def prime(self):
        head = label(r"Arithmetic modulo a prime", font_size=34).to_edge(UP, buff=0.3)
        p = 7
        cells = VGroup()
        for a in range(p):
            for b in range(p):
                v = a * b % p
                sq = Square(side_length=0.48, stroke_color=GREY_D, stroke_width=1,
                            fill_color=YES if v == 1 else (BG if v else GREY_E), fill_opacity=0.6 if v == 1 else 1)
                sq.move_to([-5.3 + 0.5 * b, 1.6 - 0.5 * a, 0])
                cells.add(VGroup(sq, mono(str(v), 18, WHITE if v else GREY_B).move_to(sq)))
        rh = VGroup(*[mono(str(a), 18, DATA).move_to([-5.85, 1.6 - 0.5 * a, 0]) for a in range(p)])
        ch = VGroup(*[mono(str(b), 18, DATA).move_to([-5.3 + 0.5 * b, 2.15, 0]) for b in range(p)])
        tl = label(r"$a \times b \bmod 7$", font_size=20, color=GREY_A).next_to(cells, DOWN, buff=0.25)
        lines = VGroup(
            label(r"a \textbf{field}: \ add, \ subtract, \ multiply, \ and divide by anything but 0", font_size=22,
                  color=WHITE),
            label(r"the integers mod a prime $p$ form one, \ $\mathrm{GF}(p)$: \\ every row has exactly one 1, \ so "
                  r"every nonzero number has an inverse", font_size=22, color=YES),
            label(r"mod 8 fails: \ $2 \times 4 = 0$, \ and 2 has no inverse", font_size=22, color=NO),
            label(r"in a field, \ a nonzero polynomial of degree $d$ has at most $d$ roots: \\ the fact Reed--Solomon "
                  r"codes rest on", font_size=22, color=HEAD),
            label(r"Galois \ (1830): \ there is a field of every prime-power size, \ and only those", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(VGroup(cells, rh), RIGHT, buff=0.8).align_to(ch, UP)
        fit_right(lines)
        with self.voiceover(
            "The codes of the next chapters compute with polynomials, so they need numbers that behave like the "
            "rationals but come in a finite supply. <bookmark mark='a'/> That is a field: you can add, subtract, "
            "multiply, and divide by anything except zero. <bookmark mark='b'/> The integers modulo a prime form "
            "one. In this multiplication table modulo seven, every row contains exactly one 1, so every nonzero "
            "number has an inverse. <bookmark mark='c'/> Modulo eight it fails: two times four is zero, and two has "
            "no inverse. <bookmark mark='d'/> In any field, a nonzero polynomial of degree d has at most d roots. "
            "That one fact carries the Reed-Solomon codes. <bookmark mark='e'/> Évariste Galois found that there is "
            "a finite field for every power of a prime, and for no other size."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rh), FadeIn(ch), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01),
                      FadeIn(tl), run_time=2.0)
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def gf256(self):
        f = load("field")
        head = label(r"$\mathrm{GF}(256)$: \ a field of bytes", font_size=34).to_edge(UP, buff=0.3)
        o = np.array([-3.8, -0.8, 0])
        R = 2.4
        ring = VGroup(*[Dot(o + R * np.array([math.cos(PI / 2 - 2 * PI * i / 255), math.sin(PI / 2 - 2 * PI * i / 255),
                                              0]), radius=0.025, color=DATA) for i in range(255)])
        def at(i, r):
            t = PI / 2 - 2 * PI * i / 255
            return o + r * np.array([math.cos(t), math.sin(t), 0])
        labs = VGroup(*[Dot(at(i, R), radius=0.06, color=HEAD) for i in range(9)],
                      Arrow(at(0, R + 0.35), at(14, R + 0.35), buff=0, color=HEAD, stroke_width=2,
                            max_tip_length_to_length_ratio=0.3),
                      label(r"$\times \alpha$", font_size=18, color=HEAD).move_to(at(7, R + 0.65)))
        alab = MathTex(r"\alpha^0, \alpha^1, \alpha^2, \ldots, \alpha^{254}", font_size=26, color=DATA).move_to(o)
        seq = ", ".join(f"{v}" for v in f["powers"][:12])
        lines = VGroup(
            label(r"a byte is a polynomial with bits as coefficients: \\ \texttt{10000011} $= x^7 + x + 1$",
                  font_size=21, color=WHITE),
            label(r"add = XOR; \ multiply polynomials, \ then reduce \\ modulo $x^8 + x^4 + x^3 + x^2 + 1$", font_size=21,
                  color=GREY_A),
            label(rf"powers of $\alpha = x$: \ {seq}, \ $\ldots$ \\ at $\alpha^8$ the reduction kicks in: \ {f['alpha8']}",
                  font_size=21, color=HEAD),
            label(rf"all {f['order']} nonzero bytes appear exactly once: \\ $\alpha$ \textbf{{generates}} the field",
                  font_size=21, color=YES),
            label(rf"so multiply by adding logarithms: \ \texttt{{0x{f['a']:02x}}} $\times$ \texttt{{0x{f['b']:02x}}} "
                  rf"$= \alpha^{{{f['log_a']}}} \alpha^{{{f['log_b']}}}$ \\ $= \alpha^{{{(f['log_a'] + f['log_b']) % 255}}}$ "
                  rf"$=$ \texttt{{0x{f['product']:02x}}}: \ two table lookups", font_size=21, color=DATA),
            label(r"multiplying by $\alpha$ is a shift and a conditional XOR: \\ Part 5's linear-feedback shift "
                  r"register", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ring, RIGHT, buff=0.8).align_to(ring, UP).shift(UP * 0.4)
        fit_right(lines)
        with self.voiceover(
            "Computers want a field whose elements are bytes. Two hundred and fifty-six is two to the eighth, so one "
            "exists. <bookmark mark='a'/> Read a byte as a polynomial whose coefficients are its bits. <bookmark "
            "mark='b'/> Addition is exclusive or. To multiply, multiply the polynomials and take the remainder modulo "
            "a fixed polynomial of degree eight that cannot be factored; QR codes use this one. <bookmark mark='c'/> "
            "Now take alpha, the byte two, which stands for x, and keep multiplying by it: one, two, four, up to a "
            "hundred and twenty-eight, then the reduction kicks in and gives twenty-nine. <bookmark mark='d'/> All "
            "two hundred and fifty-five nonzero bytes appear exactly once before the sequence repeats. Alpha "
            "generates the whole field. <bookmark mark='e'/> So every nonzero byte is a power of alpha, and "
            "multiplication becomes adding exponents: two table lookups and an addition, the way slide rules "
            "multiplied with logarithms. <bookmark mark='f'/> And multiplying by alpha itself is a shift and a "
            "conditional exclusive or: exactly the linear-feedback shift register of Part 5."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in ring], lag_ratio=0.01), FadeIn(alab), run_time=3.0)
            self.play(FadeIn(labs), FadeIn(lines[2]))
            for mk, ln in zip("def", lines[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def which(self):
        g = load("gfpoly")
        head = label(r"Which polynomial?", font_size=34).to_edge(UP, buff=0.35)
        bars = VGroup()
        for i, (n, txt, col) in enumerate(((g["total_monic"], r"polynomials of degree 8", GREY_B),
                                           (g["irreducible"], r"irreducible: \ a field", DATA),
                                           (g["primitive"], r"primitive: \ $x$ generates it", YES))):
            r = Rectangle(width=8.0 * n / g["total_monic"], height=0.55, stroke_width=0, fill_color=col,
                          fill_opacity=0.8).move_to([-6.5, 1.6 - 1.0 * i, 0], aligned_edge=LEFT)
            bars.add(VGroup(r, label(str(n), font_size=22, color=WHITE).next_to(r, RIGHT, buff=0.15),
                            label(txt, font_size=20, color=col).next_to(r, RIGHT, buff=0.9)))
        lines = VGroup(
            label(r"any \textbf{irreducible} polynomial of degree 8 gives the field of 256 elements: \ they are all "
                  r"the same field, \ written differently", font_size=22, color=WHITE),
            label(rf"QR codes use \texttt{{{g['qr']}}}: \ primitive, \ so the powers of $x$ run through every byte",
                  font_size=22, color=YES),
            label(rf"AES \ (Part 29) \ uses \texttt{{{g['aes']}}}: \ irreducible but \textbf{{not}} primitive; "
                  r"\ there the generator is $x + 1$", font_size=22, color=HEAD),
            label(r"we checked all 256 by brute force: \ Gauss's formula predicts 30 irreducible, \ and $\varphi(255)/8"
                  r" = 16$ primitive", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bars, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        with self.voiceover(
            "Why that polynomial? <bookmark mark='a'/> There are two hundred and fifty-six polynomials of degree "
            "eight over the bits. Thirty of them cannot be factored, and any of those thirty builds a field of two "
            "hundred and fifty-six elements; in fact they all build the same field, labelled differently. <bookmark "
            "mark='b'/> Sixteen are primitive as well: the powers of x run through every nonzero byte. QR codes use "
            "one of those. <bookmark mark='c'/> AES, in Part 29, uses an irreducible polynomial that is not "
            "primitive, so its tables are built from the powers of x plus one instead. <bookmark mark='d'/> We "
            "checked all of them by brute force; Gauss's counting formula predicts the thirty, and Euler's totient "
            "predicts the sixteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]), FadeIn(lines[1]))
            for mk, ln in zip("cd", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
