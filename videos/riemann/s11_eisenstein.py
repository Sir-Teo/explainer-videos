from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import OMEGA, eis, eis_norm, eisenstein_primes, label, note, sextic_symbol_table

CENTER = np.array([-3.3, -0.35, 0.0])
UNIT = 0.41
RADIUS = 8.0
WIDE_UNIT, WIDE_RADIUS = 0.19, 17.5  # zoomed-out view for the prime snowflake
PI_A, PI_B = 4, 1  # the Eisenstein prime 4 + omega, of norm 13
SIX = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]  # hue for zeta6^k, k = 0..5


def to_screen(z: complex, center=CENTER, unit=UNIT) -> np.ndarray:
    return center + unit * np.array([z.real, z.imag, 0.0])


def lattice(radius=RADIUS):
    R = int(radius * 1.3) + 1
    return [(a, b) for a in range(-R, R + 1) for b in range(-R, R + 1) if abs(eis(a, b)) <= radius]


class EisensteinWorld(VoiceoverScene):
    def construct(self):
        self.the_lattice()
        self.primes()
        self.zeta_factors()
        self.sextic()

    # ------------------------------------------------------------------
    def the_lattice(self):
        pts = lattice()
        dots = VGroup(*[Dot(to_screen(eis(a, b)), radius=0.035, color=GREY_B) for a, b in pts])
        o = to_screen(0)
        one = Arrow(o, to_screen(1), buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        om = Arrow(o, to_screen(OMEGA), buff=0, color=C.CHARACTER, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        one_l = MathTex("1", font_size=30).next_to(to_screen(1), DOWN, buff=0.1)
        om_l = MathTex(r"\omega", font_size=34, color=C.CHARACTER).next_to(to_screen(OMEGA), LEFT, buff=0.1)
        text = VGroup(
            label(r"\textbf{Eisenstein integers}", font_size=38),
            MathTex(r"a + b\,\omega, \qquad a, b \in \mathbb{Z}", font_size=38),
            MathTex(r"\omega = e^{2\pi i/3} = \tfrac{-1 + i\sqrt3}{2}", font_size=34, color=C.CHARACTER),
            MathTex(r"\omega^2 + \omega + 1 = 0", font_size=34, color=C.CHARACTER),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.7 + UP * 1.6)

        with self.voiceover(
            "The proof doesn't work directly with ordinary whole numbers. <bookmark mark='m'/> It moves to the Eisenstein "
            "integers: numbers of the form a plus b omega, <bookmark mark='o'/> where omega is a cube root of one, one third of "
            "the way around the unit circle. <bookmark mark='t'/> Together they form a triangular lattice in the complex plane."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(text[:2]))
            vo.wait_until("o")
            self.play(GrowArrow(one), FadeIn(one_l), GrowArrow(om), FadeIn(om_l), FadeIn(text[2:]))
            vo.wait_until("t")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.003), run_time=2)

        units = VGroup(*[Dot(to_screen(np.exp(1j * np.pi * k / 3)), radius=0.08, color=YELLOW) for k in range(6)])
        hexagon = Polygon(*[to_screen(np.exp(1j * np.pi * k / 3)) for k in range(6)], color=YELLOW, stroke_width=2)
        ul = label(r"the 6 units $\pm1, \pm\omega, \pm\omega^2$:\\the sixth roots of one", font_size=30, color=YELLOW)
        ul.move_to(RIGHT * 3.7 + DOWN * 1.0)
        norm = MathTex(r"N(a + b\omega) = a^2 - ab + b^2", font_size=34).next_to(ul, DOWN, buff=0.5)
        with self.voiceover(
            "You can add and multiply them, just like integers. <bookmark mark='u'/> There are six units, numbers that divide "
            "one: the six sixth roots of one. <bookmark mark='n'/> And each has a size, its norm, a squared length that is always "
            "a whole number."
        ) as vo:
            vo.wait_until("u")
            self.play(Create(hexagon), FadeIn(units, scale=2), FadeIn(ul))
            vo.wait_until("n")
            self.play(FadeIn(norm))
        self.play(FadeOut(VGroup(one, om, one_l, om_l, hexagon, units, ul, norm, text)))
        self.dots = dots

    # ------------------------------------------------------------------
    def primes(self):
        ps = eisenstein_primes(WIDE_RADIUS)
        wide = VGroup(*[Dot(to_screen(eis(a, b), unit=WIDE_UNIT), radius=0.014, color=GREY_D) for a, b in lattice(WIDE_RADIUS)])
        pdots = VGroup(*[Dot(to_screen(eis(a, b), unit=WIDE_UNIT), radius=0.045, color=C.PRIME) for a, b in ps])
        self.play(FadeOut(self.dots), FadeIn(wide), run_time=1.2)
        txt = VGroup(
            label(r"\textbf{Eisenstein primes}", font_size=36, color=C.PRIME),
            label(r"factorization into primes\\is unique (up to units)", font_size=30),
            label(r"$7 = (3 + \omega)(2 - \omega)$ \ splits;\\$5$ stays prime", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.7 + UP * 0.6)
        assert abs((3 + OMEGA) * (2 - OMEGA) - 7) < 1e-12 and eis_norm(3, 1) == 7
        assert (5, 0) in ps and (7, 0) not in ps
        with self.voiceover(
            "And, crucially, every Eisenstein integer factors into Eisenstein primes in an essentially unique way. "
            "<bookmark mark='p'/> Here are the Eisenstein primes, with their six-fold symmetry. <bookmark mark='s'/> Some ordinary "
            "primes, like seven, split into two of them. Others, like five, stay prime."
        ) as vo:
            self.play(FadeIn(txt[:2]))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in pdots], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("s")
            self.play(FadeIn(txt[2]))
        self.wait(0.5)
        self.play(FadeOut(VGroup(pdots, txt, wide)), FadeIn(self.dots))

    # ------------------------------------------------------------------
    def zeta_factors(self):
        n7 = [(a, b) for a, b in lattice() if eis_norm(a, b) == 7]
        assert len(n7) == 12
        circ = Circle(radius=UNIT * np.sqrt(7), color=C.PRIME, stroke_width=1.5).move_to(CENTER)
        d7 = VGroup(*[Dot(to_screen(eis(a, b)), radius=0.08, color=C.PRIME) for a, b in n7])
        count = label(r"12 Eisenstein integers of norm 7", font_size=28, color=C.PRIME).next_to(circ, DOWN, buff=0.15)
        count.shift(DOWN * 1.6)
        count.add_background_rectangle(opacity=0.85, buff=0.05)
        f1 = MathTex(r"\zeta_{K}(s)", r"=", r"\zeta(s)", r"\cdot", r"L(s, \chi_{-3})", font_size=42)
        f1[0].set_color(C.PRIME)
        f1[4].set_color(C.CHARACTER)
        k = note(r"$K = \mathbb{Q}(\sqrt{-3})$: the Eisenstein world", font_size=26)
        f2 = MathTex(r"L_K(s, \chi \circ N)", r"=", r"L(s, \chi)", r"\cdot", r"L(s, \chi\chi_{-3})", font_size=36)
        f2[0].set_color(C.PRIME)
        f2[2].set_color(C.CHARACTER)
        f2[4].set_color(C.CHARACTER)
        concl = label(r"zero-free for the Eisenstein world's $L$-functions\\$\Rightarrow$ zero-free for $\zeta$ and every Dirichlet $L$",
                      font_size=27, color=C.ZERO_FREE)
        col = VGroup(f1, k, f2, concl).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.75)
        why = note(r"(counting by norm: \# of norm $n$ $= 6\sum_{d \mid n}\chi_{-3}(d)$)", font_size=22).next_to(f1, UP, buff=0.3)

        with self.voiceover(
            "Why go there? First, nothing is lost. The Eisenstein world has its own zeta function, built by counting its numbers "
            "by norm, <bookmark mark='n'/> like these twelve of norm seven. <bookmark mark='f'/> And it factors: it's Riemann's "
            "zeta times a Dirichlet L-function. <bookmark mark='g'/> The same thing happens with every Dirichlet character. "
            "<bookmark mark='c'/> So if you can keep zeros out of a half-plane for the Eisenstein world's L-functions, you get it "
            "for zeta, and for every Dirichlet L-function, for free."
        ) as vo:
            vo.wait_until("n")
            self.play(Create(circ), FadeIn(d7, scale=2), FadeIn(count))
            vo.wait_until("f")
            self.play(Write(f1), FadeIn(k), FadeIn(why))
            vo.wait_until("g")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(FadeIn(concl, shift=UP * 0.2))
        self.wait(0.5)
        self.play(FadeOut(VGroup(circ, d7, count, col, why)))

    # ------------------------------------------------------------------
    def sextic(self):
        sym = sextic_symbol_table(PI_A, PI_B)
        pts = lattice(7.6)
        arrows = VGroup()
        holes = VGroup()
        for a, b in pts:
            k = sym(a, b)
            c = to_screen(eis(a, b))
            if k is None:
                holes.add(Circle(radius=0.09, color=GREY_B, stroke_width=2).move_to(c))
                continue
            ang = k * PI / 3
            arr = Arrow(c, c + 0.3 * np.array([np.cos(ang), np.sin(ang), 0]), buff=0, color=SIX[k], stroke_width=3,
                        max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12)
            arr.k = k
            arrows.add(arr)
        defn = VGroup(
            label(r"\textbf{sixth-power residue symbol}", font_size=34, color=C.CHARACTER),
            MathTex(r"\Big(\frac{u}{\pi}\Big)_{\!6} \equiv u^{(N\pi - 1)/6} \pmod{\pi}", font_size=40),
            label(r"always one of the 6 sixth roots of one", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.7 + UP * 2.0)
        legend = VGroup()
        for k in range(6):
            ang = k * PI / 3
            legend.add(Arrow(ORIGIN, 0.45 * np.array([np.cos(ang), np.sin(ang), 0]), buff=0, color=SIX[k], stroke_width=4,
                             max_tip_length_to_length_ratio=0.3))
        legend.move_to(RIGHT * 3.7 + DOWN * 0.15)
        leg_l = MathTex(r"e^{2\pi i k/6}", font_size=28).next_to(legend, RIGHT, buff=0.4)
        example = label(rf"here: $\pi = {PI_A} + \omega$, \ of norm {eis_norm(PI_A, PI_B)}", font_size=28).next_to(legend, DOWN, buff=0.45)
        analog = label(r"like asking ``is $u$ a square mod $p$?'',\\but with six possible answers", font_size=28, color=GREY_A)
        analog.next_to(example, DOWN, buff=0.4)

        with self.voiceover(
            "Second, the Eisenstein integers contain the sixth roots of one, and that unlocks a tool: <bookmark mark='s'/> the "
            "sixth-power residue symbol. For an Eisenstein prime pi, and any u, the symbol 'u over pi, sub six' is always one of "
            "the six sixth roots of one. <bookmark mark='d'/> Here it is for every u in view, with pi equal to four plus omega, "
            "drawn as a little arrow pointing at the answer. <bookmark mark='a'/> It's the analog of asking whether u is a perfect "
            "square modulo p, but with six possible answers instead of two."
        ) as vo:
            self.play(self.dots.animate.set_opacity(0.25))
            vo.wait_until("s")
            self.play(FadeIn(defn))
            vo.wait_until("d")
            self.play(FadeIn(legend), FadeIn(leg_l), FadeIn(example))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.002), FadeIn(holes), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(analog))

        pi_z = complex(eis(PI_A, PI_B))
        cell = Polygon(*[to_screen(z) for z in (0, pi_z, pi_z + pi_z * OMEGA, pi_z * OMEGA)], color=WHITE, stroke_width=2.5)
        shift_v = to_screen(pi_z) - to_screen(0)
        cell2 = cell.copy().shift(shift_v)
        per = label(r"the pattern repeats: shift $u$ by any multiple of $\pi$", font_size=28).move_to(RIGHT * 3.7 + DOWN * 1.2)
        mult = MathTex(r"\Big(\frac{uv}{\pi}\Big)_{\!6} = \Big(\frac{u}{\pi}\Big)_{\!6}\Big(\frac{v}{\pi}\Big)_{\!6}", font_size=36)
        six = MathTex(r"\Big(\frac{v^6}{\pi}\Big)_{\!6} = \Big(\frac{v}{\pi}\Big)_{\!6}^{6} = 1", font_size=44, color=YELLOW)
        VGroup(mult, six).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.7 + DOWN * 2.2)
        sixth_pts = VGroup(*[a for a in arrows if a.k == 0])

        with self.voiceover(
            "Like the familiar symbol for squares, it repeats: <bookmark mark='r'/> shift u by any multiple of pi, and the answer "
            "doesn't change. <bookmark mark='m'/> It's also multiplicative. <bookmark mark='s'/> So the symbol of a perfect sixth "
            "power is always one: six times around the clock brings you back to the start. <bookmark mark='k'/> Keep this fact in "
            "mind. It's the key to the whole argument."
        ) as vo:
            self.play(FadeOut(VGroup(legend, leg_l, analog)), example.animate.move_to(RIGHT * 3.7 + UP * 0.1))
            vo.wait_until("r")
            self.play(Create(cell), FadeIn(per))
            self.play(TransformFromCopy(cell, cell2))
            vo.wait_until("m")
            self.play(FadeOut(per), FadeIn(mult))
            vo.wait_until("s")
            self.play(FadeIn(six))
            vo.wait_until("k")
            self.play(Indicate(six, color=YELLOW, scale_factor=1.1), *[Indicate(a, color=SIX[0], scale_factor=1.6) for a in sixth_pts])
        self.wait(0.8)
        self.clear_scene()
