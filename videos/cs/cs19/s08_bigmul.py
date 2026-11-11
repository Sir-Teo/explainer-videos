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
            "An integer is a polynomial evaluated at the digit base. <bookmark mark='a'/> Three hundred and twenty-"
            "one has coefficients one, two and three in increasing powers of ten. <bookmark mark='b'/> Multiplying by"
            " four plus five x gives coefficients four, thirteen, twenty-two and fifteen. <bookmark mark='c'/> "
            'Carrying gives seventeen thousand three hundred and thirty-four, exactly three hundred and twenty-one '
            "times fifty-four. <bookmark mark='d'/> Our floating candidate groups four decimal digits per coefficient"
            ' and zero-pads sufficiently to avoid circular aliasing. Conversion, transform, rounding and carry all '
            'belong to its end-to-end time. Each timed integer result is independently compared with exact '
            'multiplication.'
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
        c=load("fftcore")
        head=label("Certify every convolution coefficient",font_size=34).to_edge(UP,buff=.3)
        rows=[[f"{r['digits']:,}",t(r['fft_core_s']),f"{r['certificate']['coefficients']:,}",f"{r['max_residual']:.5f}"] for r in c['rows']]
        tab=grid_table(["decimal-digit equivalent","NumPy core + round","coefficients certified","nearest-integer distance"],rows,
                       widths=[3.0,2.8,3.0,3.6],row_h=.48,font_size=20,
                       colors=[[WHITE,YES,DATA,HEAD]]*len(rows)).next_to(head,DOWN,buff=.4)
        diagnostic=label("a small rounding distance alone does not prove the correct integer",font_size=21,color=HEAD).next_to(tab,DOWN,buff=.28)
        names=["rounded candidate","exact residues mod two primes","equal integer coefficients"]
        boxes=VGroup(*[VGroup(RoundedRectangle(width=3.7,height=.76,corner_radius=.10,color=color,stroke_width=1.5,fill_color=BG,fill_opacity=1),
                             label(name,font_size=19,color=color)).move_to([(i-1)*4.15,-.95,0])
                       for i,(name,color) in enumerate(zip(names,[HEAD,LAM,YES]))])
        for box in boxes:
            if box[1].width>3.35:box[1].scale_to_fit_width(3.35)
            box[1].move_to(box[0])
        arrows=VGroup(*[Arrow(boxes[i][0].get_right(),boxes[i+1][0].get_left(),buff=.08,color=GREY_B) for i in range(2)])
        proof=VGroup(boxes,arrows)
        uniqueness=VGroup(
            MathTex(r"0\le c_k,\widehat c_k\le \mathcal B<p_1p_2,\quad \widehat c_k\equiv c_k\pmod{p_1,p_2}\ \Longrightarrow\ \widehat c_k=c_k",font_size=27,color=YES),
            MathTex(r"p_1=998244353,\quad p_2=469762049,\quad \mathcal B=\min(|A|,|B|)\max A\max B",font_size=23,color=LAM),
            label("all coefficients and zero padding checked; reference and validation outside timer",font_size=20,color=GREY_A),
        ).arrange(DOWN,buff=.18).to_edge(DOWN,buff=.3)
        pts=[diagnostic,proof,uniqueness]
        with self.voiceover(
            "A floating value's distance to the nearest integer is not its distance to the correct integer. <bookmark"
            " mark='a'/> The yellow column is only a rounding diagnostic: it could be small even if a coefficient "
            "were wrong by one. <bookmark mark='b'/> To certify these particular experiments, an independent native "
            'program computes every coefficient modulo two primes using exact integer transforms. <bookmark '
            "mark='c'/> Each rounded candidate is nonnegative and below an explicit coefficient bound, and the "
            'product of the primes is larger than that bound. Agreement in both residues therefore proves integer '
            'equality for every coefficient, including the zero padding. Reference construction and checks are '
            'outside the NumPy timer. This certifies these outputs, not all floating FFT multiplications at arbitrary'
            ' lengths.'
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
            "The number-theoretic transform makes the transform arithmetic exact. <bookmark mark='a'/> Choose a prime"
            " whose multiplicative group contains a root of the required power-of-two order. <bookmark mark='b'/> For"
            " this prime, three supplies suitable roots, and we check the length and root order. <bookmark mark='c'/>"
            ' Butterflies then operate modulo the prime without rounding. Recovering unrestricted integer '
            'coefficients still requires a coefficient bound or enough moduli; modular exactness alone is not integer'
            " exactness. <bookmark mark='d'/> The decimal backend can use number-theoretic multiplication for large "
            'operands. Its complete-product timings here use the same fixed values as Python integers, with '
            'conversions excluded for both. Read the measured crossover from the table rather than extrapolating a '
            'fixed speed ratio.'
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
            label('2019 theorem: $O(n\\log n)$ bit-complexity upper bound; no matching general lower bound claimed', font_size=21, color=HEAD),
            label(rf"certified $\lfloor\pi 10^D\rfloor$, $D=10^6$: {d['seconds']:.0f} s; this run, not a record claim", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Keep the complexity model attached to the timeline. <bookmark mark='a'/> School multiplication, "
            "Karatsuba and Toom-Cook reduce digit work. Schönhage and Strassen's 1971 ring-based transform gives a "
            "bit-complexity bound of n log n log log n; Fürer's later construction improves the asymptotic factor. "
            "<bookmark mark='b'/> Harvey and van der Hoeven proved an n log n bit-complexity upper bound in their "
            '2019 work. This dated theorem is not a statement about the speed of our NumPy code or a survey of every '
            "later claim. <bookmark mark='c'/> Our million-decimal-place pi calculation uses exact binary splitting "
            'and certified final bounds. Its reported time belongs to this host and this implementation; the FFT-core'
            ' measurement is a different experiment.'
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
