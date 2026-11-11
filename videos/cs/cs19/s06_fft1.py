from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono, words)


class FftOne(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_ways()
        self.which_points()
        self.squaring()
        self.recursion()

    def card(self):
        card = chapter_card(5, r"The FFT, \ I: \ values instead of coefficients",
                            r"Where should a polynomial be evaluated?", lit=(1965,),
                            extra=((1805, r"Gauss, \ on the orbits of asteroids"), (1965, r"Cooley and Tukey")),
                            part=PART)
        with self.voiceover("Chapter five. The fast Fourier transform, part one: values instead of coefficients."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_ways(self):
        head = label(r"Two ways to hold a polynomial", font_size=34).to_edge(UP, buff=0.3)
        coef = VGroup(
            label(r"\textbf{coefficients}", font_size=24, color=DATA),
            MathTex(r"A(x) = a_0 + a_1 x + \cdots + a_{n-1} x^{n-1}", font_size=32),
            label(r"multiply two: \ every $a_i$ times every $b_j$: \ $n^2$", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.25)
        vals = VGroup(
            label(r"\textbf{values}", font_size=24, color=YES),
            MathTex(r"A(x_0),\ A(x_1),\ \ldots,\ A(x_{2n-1})", font_size=32),
            label('multiply values: $C(x_k)=A(x_k)B(x_k)$ at $N\\ge 2n-1$ distinct points', font_size=21, color=YES),
        ).arrange(DOWN, buff=0.25)
        VGroup(coef, vals).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.7)
        # a parabola through three points: three values determine it
        ax = Axes(x_range=[-2, 2, 1], y_range=[-1, 4, 1], x_length=4.2, y_length=2.6,
                  axis_config={"color": GREY_D, "include_ticks": False}).to_edge(DOWN, buff=0.4).shift(LEFT * 3.4)
        f = ax.plot(lambda x: 0.6 * x * x - 0.4 * x + 0.5, color=DATA, x_range=[-1.9, 1.9])
        dots = VGroup(*[Dot(ax.c2p(x, 0.6 * x * x - 0.4 * x + 0.5), color=HEAD, radius=0.08) for x in (-1.2, 0.3, 1.5)])
        pts = VGroup(
            label(r"$n$ values pin down a polynomial of degree $< n$ \ (interpolation)", font_size=21, color=GREY_A),
            label(r"so: \ evaluate, \ multiply pointwise, \ interpolate back", font_size=22, color=HEAD),
            label(r"the catch: \ evaluating at $2n$ points costs $2n \cdot n$ the obvious way", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.7)
        with self.voiceover(
            "Polynomial multiplication separates the algebra from carries. <bookmark mark='a'/> Two coefficient "
            'arrays of length n have a rectangular school product with n squared scalar multiplications. <bookmark '
            "mark='b'/> At each evaluation point, the product value is just the two factor values multiplied "
            "together. <bookmark mark='c'/> Distinct points determine a polynomial up to its degree bound. A product "
            'of two degree-below-n factors has degree at most two n minus two, so it needs at least two n minus one '
            "values. <bookmark mark='d'/> Pad to a suitable transform length, evaluate both factors, multiply "
            "pointwise and interpolate. <bookmark mark='e'/> Arbitrary evaluation can still cost quadratic work. The "
            "FFT's gain comes from choosing points that share recursive calculations."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(coef))
            vo.wait_until("b")
            self.play(FadeIn(vals))
            vo.wait_until("c")
            self.play(Create(ax), Create(f), FadeIn(dots), FadeIn(pts[0]))
            vo.wait_until("d")
            self.play(FadeIn(pts[1]))
            vo.wait_until("e")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def which_points(self):
        head = label(r"Plus and minus, \ for free", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"A(x) = A_{\text{even}}(x^2) + x\,A_{\text{odd}}(x^2)", font_size=40, color=YES),
            MathTex(r"A_{\text{even}}(y) = a_0 + a_2 y + a_4 y^2 + \cdots,\qquad A_{\text{odd}}(y) = a_1 + a_3 y + "
                    r"a_5 y^2 + \cdots", font_size=30),
            MathTex(r"A(+x) = A_{\text{even}}(x^2) + x\,A_{\text{odd}}(x^2)", font_size=34, color=DATA),
            MathTex(r"A(-x) = A_{\text{even}}(x^2) - x\,A_{\text{odd}}(x^2)", font_size=34, color=LAM),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        pts = VGroup(
            label(r"choose points in $\pm$ pairs: \ two values from one evaluation of each half", font_size=22,
                  color=GREY_A),
            label(r"the halves have half the degree, \ and need only the squares $x^2$: \ half as many points",
                  font_size=22, color=HEAD),
            label(r"to recurse, \ the squares must come in $\pm$ pairs too: \ which real numbers do that?",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Split the coefficients by parity. <bookmark mark='a'/> The even and odd parts are polynomials in x "
            "squared. <bookmark mark='b'/> Evaluate at opposite points, x and minus x. <bookmark mark='c'/> Both use "
            "the same two half-polynomial values; only the sign of the odd contribution changes. <bookmark mark='d'/>"
            " Each opposite pair therefore shares its recursive work. <bookmark mark='e'/> To keep halving, the "
            "squared points must again form opposite pairs. <bookmark mark='f'/> A large set of distinct real points "
            'cannot maintain this closure: real squares are nonnegative. Complex roots of unity supply the recursive '
            'pairing we need.'
        ) as vo:
            self.play(FadeIn(head),FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(Indicate(eqs[0],color=DATA))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(eqs[3]))
            vo.wait_until("d")
            self.play(FadeIn(pts[0]))
            vo.wait_until("e")
            self.play(FadeIn(pts[1]))
            vo.wait_until("f")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def squaring(self):
        head = label(r"The roots of unity", font_size=34).to_edge(UP, buff=0.3)
        c0 = LEFT * 3.0 + DOWN * 0.3
        R = 2.4
        circle = Circle(radius=R, color=GREY_D, stroke_width=1.5).move_to(c0)
        axes = VGroup(Line(c0 + LEFT * 2.8, c0 + RIGHT * 2.8, color=GREY_D, stroke_width=1),
                      Line(c0 + DOWN * 2.8, c0 + UP * 2.8, color=GREY_D, stroke_width=1))
        cols = [DATA, YES, HEAD, LAM, CTRL, NO, FUNC, COST]

        def ring(n, rad=0.11):
            return VGroup(*[Dot(c0 + R * np.array([np.cos(2 * np.pi * k / n), np.sin(2 * np.pi * k / n), 0]),
                                radius=rad, color=cols[k % n % 8]) for k in range(n)])
        r8 = ring(8)
        lab = MathTex(r"\omega = e^{2\pi i / 8}", font_size=30, color=HEAD).next_to(circle, UP, buff=0.15)
        side = VGroup(
            MathTex(r"\omega^k = e^{2\pi i k/n}: \ \text{the } n \text{ solutions of } z^n = 1", font_size=28),
            label(r"opposite points: \ $\omega^{k + n/2} = -\omega^k$", font_size=22, color=GREY_A),
            label(r"squaring doubles the angle: \ 8 points land on 4, \ then 2, \ then 1", font_size=22,
                  color=YES),
            label(r"and each new set again comes in $\pm$ pairs", font_size=22, color=HEAD),
            MathTex(r"T(n) = 2\,T(n/2) + O(n) = O(n \log n)", font_size=32, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        if side.width > 6.0:
            side.scale_to_fit_width(6.0).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Complex numbers can. <bookmark mark='a'/> Take the eight points equally spaced around the unit circle: "
            "the eighth roots of unity, the numbers whose eighth power is one. <bookmark mark='b'/> They come in "
            "opposite pairs: rotating by half a turn negates a point. <bookmark mark='c'/> Squaring a point on "
            "the circle doubles its angle. Watch what happens to all eight: opposite points land together, and the "
            "eight become the four fourth roots of unity. <bookmark mark='d'/> Those four are again two opposite "
            "pairs. Square again: two points, plus one and minus one. Square once more, and everything lands on "
            "one. At every level the points pair up, exactly as the recursion needs. <bookmark mark='e'/> So "
            "evaluating at the n-th roots of unity takes two half-size evaluations plus linear work: n log n. That "
            "evaluation is the discrete Fourier transform, and this way of computing it is the fast Fourier "
            "transform."
        ) as vo:
            self.play(FadeIn(head), Create(circle), FadeIn(axes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in r8], lag_ratio=0.12), FadeIn(lab), FadeIn(side[0]))
            vo.wait_until("b")
            pairs = VGroup(*[DashedLine(r8[k].get_center(), r8[k + 4].get_center(), color=GREY_B, stroke_width=1.5)
                             for k in range(4)])
            self.play(Create(pairs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(pairs), FadeIn(side[2]))
            cur = r8
            for n in (4, 2, 1):
                target = ring(n, 0.14)
                self.play(*[cur[k].animate.move_to(target[k % n].get_center()).set_color(target[k % n].get_color())
                            for k in range(len(cur))], run_time=1.6)
                if n == 4:
                    vo.wait_until("d")
                    self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def recursion(self):
        head = label(r"The whole algorithm", font_size=34).to_edge(UP, buff=0.3)
        prog = code([
            "def fft(a):",
            "    n = len(a)",
            "    if n == 1: return a",
            "    even, odd = fft(a[0::2]), fft(a[1::2])",
            "    out = [0] * n",
            "    for k in range(n // 2):",
            "        t = exp(-2j*pi*k/n) * odd[k]",
            "        out[k]        = even[k] + t",
            "        out[k + n//2] = even[k] - t",
            "    return out",
        ], size=20).scale_to_fit_width(7.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        pts = VGroup(
            label(r"ten lines, \ $n \log n$ time", font_size=24, color=YES),
            label(r"the inverse is the same transform \\ with $\omega^{-1}$, \ divided by $n$", font_size=22,
                  color=GREY_A),
            label('evaluate, multiply, invert: polynomial convolution \\\\ $O(n\\log n)$ arithmetic; bit work is a different metric', font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        if pts.width > 4.9: pts.scale_to_fit_width(4.9)
        pts.move_to([3.95,0,0])
        with self.voiceover(
            "The literal code uses a negative-angle forward root, matching NumPy's convention. <bookmark mark='a'/> "
            'For a nonempty power-of-two length, recursively transform even and odd coefficients, then combine each '
            'pair with one twiddle multiplication, an addition and a subtraction. Empty input returns empty; '
            "unsupported lengths are rejected. <bookmark mark='b'/> The inverse uses the opposite sign and divides by"
            " the transform length. <bookmark mark='c'/> With sufficient zero padding this computes a linear "
            'convolution in n log n arithmetic operations. Floating-point rounding and integer bit complexity are '
            'separate questions; a short arithmetic count is not an exactness proof.'
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
