from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def t(s):
    return f"{s * 1e6:.0f} µs" if s < 1e-3 else (f"{s * 1000:.1f} ms" if s < 1 else f"{s:.2f} s")


class BigMul(VoiceoverScene):
    def construct(self):
        self.card()
        self.numbers()
        self.precision()
        self.ntt()
        self.timeline()

    def card(self):
        card = chapter_card(7, r"What the FFT multiplies", r"How do you multiply numbers a million digits long?",
                            lit=(1971,), extra=((1971, r"Sch\"onhage and Strassen"),
                                                (2019, r"Harvey and van der Hoeven")), part=PART)
        with self.voiceover("Chapter seven. What the FFT multiplies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def numbers(self):
        d = load("fft")
        p, q, r = d["poly"]
        head = label(r"An integer is a polynomial at $x = 10$", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"321 = 1 + 2x + 3x^2 \big|_{x=10}, \qquad 54 = 4 + 5x \big|_{x=10}", font_size=32),
            MathTex(rf"(1 + 2x + 3x^2)(4 + 5x) = {r[0]} + {r[1]}x + {r[2]}x^2 + {r[3]}x^3", font_size=32,
                    color=YES),
            MathTex(rf"\text{{carry: }} {r[0]} + {r[1]} \cdot 10 + {r[2]} \cdot 100 + {r[3]} \cdot 1000 = 17334 = "
                    r"321 \times 54", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        steps = VGroup(
            label(r"1. \ write each number's digits as coefficients \ (in practice, \ blocks of 4 digits)",
                  font_size=21, color=GREY_A),
            label(r"2. \ FFT both, \ multiply pointwise, \ inverse FFT: \ the convolution of the digits",
                  font_size=21, color=GREY_A),
            label(r"3. \ round to integers, \ and carry", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "To multiply integers, treat them as polynomials. <bookmark mark='a'/> Three hundred and twenty-one is "
            "one plus two x plus three x squared, at x equals ten. <bookmark mark='b'/> Multiply the polynomials, "
            "by the FFT for long ones, and the coefficients come out as four, thirteen, twenty-two and fifteen. "
            "<bookmark mark='c'/> They are too big to be digits, so carry: the result is seventeen thousand, three "
            "hundred and thirty-four, which is three hundred and twenty-one times fifty-four. <bookmark mark='d'/> "
            "In practice digits are grouped in blocks of four, transformed, multiplied pointwise and transformed "
            "back; then the results are rounded to whole numbers and the carries propagated."
        ) as vo:
            self.play(FadeIn(head))
            for mk, e in zip("abc", eqs):
                vo.wait_until(mk)
                self.play(FadeIn(e))
            vo.wait_until("d")
            self.play(FadeIn(steps))
        self.wait(0.3)
        self.clear_scene()

    def precision(self):
        c = load("fftcore")
        head = label(r"Is floating point exact enough?", font_size=34).to_edge(UP, buff=0.3)
        def sci(v):
            e = int(f"{v:e}".split("e")[1])
            return rf"${v / 10 ** e:.1f} \times 10^{{{e}}}$"
        rows = [[f"{r['digits']:,}", t(r["fft_core_s"]), sci(r["max_term"]), f"{r['max_residual']:.5f}"]
                for r in c["rows"]]
        tab = grid_table([r"digits", r"the transforms", r"largest coefficient", r"worst distance from an integer"],
                         rows, widths=[2.4, 2.6, 3.0, 4.4], row_h=0.5, font_size=21,
                         colors=[[WHITE, YES, GREY_A, HEAD]] * len(rows)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"each output coefficient is an integer: \ rounding is exact while the error stays below $\frac12$",
                  font_size=21, color=GREY_A),
            label(r"the error grows with the length: \ about tenfold per tenfold here", font_size=21, color=HEAD),
            label(r"at ten million digits: \ 0.05, \ still safe; \ beyond, \ use smaller blocks, \ or exact arithmetic",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Floating-point arithmetic is approximate, so is the answer right? <bookmark mark='a'/> Each "
            "coefficient of the true product is a whole number, so rounding gives it exactly as long as the "
            "accumulated error stays below one half. We measured the worst error over the whole product. "
            "<bookmark mark='b'/> It grows with the length, about tenfold for every tenfold here. <bookmark "
            "mark='c'/> At ten million digits it is five hundredths, comfortably safe, and the transforms take a "
            "little over a second. Much further, and the error would reach one half. Then one uses smaller digit "
            "blocks, or abandons floating point altogether."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def ntt(self):
        head = label(r"An exact FFT: \ the number-theoretic transform", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            MathTex(r"p = 998244353 = 119 \cdot 2^{23} + 1", font_size=34, color=YES),
            label(r"in arithmetic modulo $p$, \ $3^{119 \cdot 2^{23 - k}}$ is a primitive $2^k$-th root of unity",
                  font_size=22, color=GREY_A),
            label(r"the same butterflies, \ with whole numbers mod $p$: \ no rounding at all", font_size=22,
                  color=HEAD),
            label(r"Python's \texttt{decimal} module \ (libmpdec) \ multiplies huge numbers this way:", font_size=22,
                  color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.55)
        d = load("pi")
        rows = [[f"{r['digits']:,}", t(r["python_int_s"]), t(r["decimal_s"])] for r in d["rows"]]
        tab = grid_table([r"digits", r"Python \texttt{int} \ (Karatsuba)", r"\texttt{decimal} \ (NTT)"], rows,
                         widths=[2.4, 3.6, 3.6], row_h=0.42, font_size=20,
                         colors=[[WHITE, DATA, LAM]] * len(rows)).next_to(pts, DOWN, buff=0.35)
        with self.voiceover(
            "There is an exact version. <bookmark mark='a'/> Work modulo a prime such as this one, one hundred and "
            "nineteen times two to the twenty-three, plus one. <bookmark mark='b'/> In that arithmetic there are "
            "roots of unity too: suitable powers of three behave exactly like the points on the circle, squaring "
            "onto each other in pairs. <bookmark mark='c'/> So the same butterflies run on whole numbers, with "
            "nothing to round. This is the number-theoretic transform, and Part 30 will use it again for cryptography. "
            "<bookmark mark='d'/> Python's decimal module multiplies huge numbers this way. On short numbers it is slower than "
            "Python's Karatsuba integers; at a hundred thousand digits the two are level; at a million digits it "
            "is four times faster, and the gap keeps widening."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def timeline(self):
        d = load("pi")
        head = label(r"How fast can we multiply?", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            [r"antiquity", r"school method", r"$n^2$"],
            [r"1960", r"Karatsuba", r"$n^{1.585}$"],
            [r"1963--66", r"Toom--Cook", r"$n^{1 + \varepsilon}$"],
            [r"1971", r"Sch\"onhage and Strassen, \ FFT over rings", r"$n \log n \log\log n$"],
            [r"2007", r"F\"urer", r"$n \log n \, 2^{O(\log^* n)}$"],
            [r"2019", r"Harvey and van der Hoeven", r"$n \log n$"],
        ]
        tab = grid_table([r"year", r"method", r"time"], rows, widths=[2.0, 6.0, 3.6], row_h=0.5, font_size=21,
                         mono_cols=(), colors=[[GREY_B, GREY_A, NO]] + [[GREY_B, GREY_A, GREY_A]] * 4 +
                         [[YES, YES, YES]]).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"Sch\"onhage and Strassen conjectured $n \log n$ in 1971: \ proved 48 years later, \ and believed "
                  r"optimal", font_size=21, color=HEAD),
            label(rf"our million digits of $\pi$: \ {d['seconds']:.0f} s; \ the record, \ over two hundred trillion "
                  r"digits \ (2024), \ rests on the same idea", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the whole history of multiplication. <bookmark mark='a'/> The school method, then Karatsuba "
            "and Toom and Cook. In 1971 Arnold Schönhage and Volker Strassen made the FFT exact over cleverly "
            "chosen rings, reaching n log n log log n, and conjectured that n log n was the truth. Martin Fürer "
            "came closer in 2007. <bookmark mark='b'/> In 2019 David Harvey and Joris van der Hoeven proved n log n, "
            "forty-eight years after the conjecture. Most experts believe nothing faster is possible, though no one "
            "can prove it. <bookmark mark='c'/> Our million digits of pi took sixteen seconds; the record, over "
            "two hundred trillion digits in 2024, was computed with the same ideas, on a much larger computer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()
