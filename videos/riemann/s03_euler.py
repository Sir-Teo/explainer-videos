from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import label, note


class EulerProduct(VoiceoverScene):
    def construct(self):
        self.definition()
        self.values()
        self.sieve()
        self.product()
        self.infinitely_many()

    # ------------------------------------------------------------------
    def definition(self):
        z = MathTex(r"\zeta(s)", r"=", r"1", r"+", r"\frac{1}{2^s}", r"+", r"\frac{1}{3^s}", r"+", r"\frac{1}{4^s}",
                    r"+", r"\frac{1}{5^s}", r"+", r"\cdots", font_size=60)
        z.move_to(UP * 0.5)
        sub = label(r"the zeta function", font_size=34, color=GREY_A).next_to(z, DOWN, buff=0.6)
        euler = note(r"studied by Euler in the 1730s; Riemann made it the key to the primes", font_size=26)
        euler.next_to(sub, DOWN, buff=0.3)
        with self.voiceover(
            "Riemann's tool was a function that Euler had studied more than a century earlier. "
            "<bookmark mark='t'/> Take every whole number, raise it to some power s, and add up the reciprocals. "
            "<bookmark mark='z'/> This is the zeta function."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(z[2:]), run_time=2.5)
            vo.wait_until("z")
            self.play(Write(z[:2]), FadeIn(sub))
            self.play(FadeIn(euler))
        self.play(FadeOut(VGroup(sub, euler)), z.animate.scale(0.75).to_edge(UP, buff=0.4))
        self.zdef = z

    # ------------------------------------------------------------------
    def values(self):
        scale = 4.5  # screen units per unit of sum
        x0 = -6.2
        def bar(s, N, y, color):
            g = VGroup()
            x = x0
            for n in range(1, N + 1):
                w = scale / n**s
                r = Rectangle(width=w, height=0.42, stroke_width=1.2, stroke_color=BACKGROUND,
                              fill_color=color, fill_opacity=0.85 if n % 2 else 0.6)
                r.move_to([x + w / 2, y, 0])
                g.add(r)
                x += w
            return g

        y2, y1 = 0.9, -1.6
        b2 = bar(2, 60, y2, C.SMOOTH)
        target = x0 + scale * np.pi**2 / 6
        tick = DashedLine([target, y2 - 0.5, 0], [target, y2 + 0.5, 0], color=YELLOW)
        v2 = MathTex(r"\zeta(2) = 1 + \tfrac14 + \tfrac19 + \tfrac1{16} + \cdots = \frac{\pi^2}{6} = 1.6449\ldots",
                     font_size=38).next_to(b2, UP, buff=0.35).align_to(b2, LEFT)
        with self.voiceover(
            "At s equals two, laying the terms end to end, they add up to pi squared over six, as Euler famously showed."
        ) as vo:
            self.play(Write(v2))
            self.play(LaggedStart(*[FadeIn(r) for r in b2], lag_ratio=0.03), run_time=2.5)
            self.play(Create(tick))

        b1 = bar(1, 400, y1, C.DANGER)
        # Only the part on screen is drawn; the harmonic series keeps going (ln N).
        b1 = VGroup(*[r for r in b1 if r.get_left()[0] < 7.2])
        v1 = MathTex(r"\zeta(1) = 1 + \tfrac12 + \tfrac13 + \tfrac14 + \cdots = \infty", font_size=38)
        v1.next_to(b1, UP, buff=0.35).align_to(b2, LEFT)
        arrow = Arrow([6.0, y1, 0], [7.1, y1, 0], buff=0, color=C.DANGER)
        with self.voiceover(
            "At s equals one, it's the harmonic series. <bookmark mark='g'/> Its terms shrink too slowly, and the sum grows "
            "without bound, like the logarithm of the number of terms."
        ) as vo:
            self.play(Write(v1))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(r) for r in b1], lag_ratio=0.01), run_time=2.5)
            self.play(GrowArrow(arrow))
        self.play(FadeOut(VGroup(b2, tick, v2, b1, v1, arrow)))

    # ------------------------------------------------------------------
    def sieve(self):
        N = 30
        tiles = VGroup()
        for n in range(1, N + 1):
            t = MathTex(rf"\frac{{1}}{{{n}^s}}", font_size=32)
            t.n = n
            tiles.add(t)
        tiles.arrange_in_grid(rows=5, cols=6, buff=(0.8, 0.22)).move_to(DOWN * 1.35)
        dots = MathTex(r"\cdots", font_size=40).next_to(tiles, RIGHT, buff=0.4).align_to(tiles[-1], DOWN)
        eq = MathTex(r"\zeta(s)", r"\Big(1 - \frac{1}{2^s}\Big)", r"\Big(1 - \frac{1}{3^s}\Big)", r"\Big(1 - \frac{1}{5^s}\Big)",
                     r"\Big(1 - \frac{1}{7^s}\Big)", r"\cdots", r"=", r"1", font_size=40).to_edge(UP, buff=0.35)
        prime_cols = {1: C.PRIME, 2: C.PRIME, 3: C.PRIME, 4: C.PRIME}
        for i in prime_cols:
            eq[i].set_color(C.PRIME)

        self.play(ReplacementTransform(self.zdef[:2].copy(), eq[0]), FadeOut(self.zdef))
        self.play(FadeIn(tiles, lag_ratio=0.02), FadeIn(dots), run_time=1.5)

        def kill(p, alive):
            return [t for t in alive if t.n % p == 0]

        alive = list(tiles)
        shifted = MathTex(r"\frac{1}{2^s}\,\zeta(s)", r"=", r"\frac{1}{2^s} + \frac{1}{4^s} + \frac{1}{6^s} + \frac{1}{8^s} + \cdots",
                          font_size=38).next_to(eq, DOWN, buff=0.35)
        shifted[0].set_color(C.PRIME)
        with self.voiceover(
            "Euler's great discovery was that the same function can be written using only the primes. Here's how. "
            "<bookmark mark='m'/> Multiply the whole sum by one over two to the s. Since one over n to the s, times one over two "
            "to the s, is one over two n to the s, <bookmark mark='e'/> that gives exactly the even terms. "
            "<bookmark mark='s'/> Subtract, and every even term vanishes."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(shifted, shift=DOWN * 0.2))
            vo.wait_until("e")
            evens = kill(2, alive)
            self.play(*[t.animate.set_color(C.PRIME) for t in evens], run_time=1.0)
            vo.wait_until("s")
            self.play(Write(eq[1]), *[t.animate.set_opacity(0.12) for t in evens], run_time=1.5)
            alive = [t for t in alive if t not in evens]

        with self.voiceover(
            "Now multiply what's left by one over three to the s, <bookmark mark='t'/> and subtract: every remaining multiple of "
            "three disappears. <bookmark mark='f'/> Then five, <bookmark mark='v'/> then seven. Each prime sieves out its "
            "multiples, exactly like the sieve of Eratosthenes."
        ) as vo:
            self.play(FadeOut(shifted))
            for p, mark, idx in [(3, "t", 2), (5, "f", 3), (7, "v", 4)]:
                vo.wait_until(mark)
                gone = kill(p, alive)
                self.play(*[t.animate.set_color(C.PRIME) for t in gone], Write(eq[idx]), run_time=0.7)
                self.play(*[t.animate.set_opacity(0.12) for t in gone], run_time=0.6)
                alive = [t for t in alive if t not in gone]

        rest = [t for t in alive if t.n > 1]
        with self.voiceover(
            "Eleven, thirteen, and every other prime each take their turn, <bookmark mark='o'/> until only the one at the very "
            "beginning is left. So zeta of s, times all of these factors, equals exactly one."
        ) as vo:
            self.play(*[t.animate.set_color(C.PRIME) for t in rest], run_time=0.8)
            self.play(*[t.animate.set_opacity(0.12) for t in rest], FadeOut(dots), Write(eq[5]), run_time=1.0)
            vo.wait_until("o")
            self.play(Indicate(tiles[0], scale_factor=1.4), Write(eq[6:]))
        self.play(FadeOut(tiles), eq.animate.move_to(UP * 2.4))
        self.eq = eq

    # ------------------------------------------------------------------
    def product(self):
        prod = MathTex(r"\zeta(s)", r"=", r"\sum_{n=1}^{\infty} \frac{1}{n^s}", r"=", r"\prod_{p\ \text{prime}} \frac{1}{1 - p^{-s}}",
                       font_size=58).move_to(UP * 0.4)
        prod[4].set_color(C.PRIME)
        box = SurroundingRectangle(prod, color=YELLOW, buff=0.25, corner_radius=0.1)
        name = label(r"Euler's product formula (1737)", font_size=32, color=YELLOW).next_to(box, UP, buff=0.2)
        b1 = Brace(prod[2], DOWN, buff=0.2)
        b1l = label(r"every whole number", font_size=30).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(prod[4], DOWN, buff=0.2, color=C.PRIME)
        b2l = label(r"only the primes", font_size=30, color=C.PRIME).next_to(b2, DOWN, buff=0.1)
        with self.voiceover(
            "Flip it around, <bookmark mark='f'/> and zeta becomes a product over the primes: Euler's product formula."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeOut(self.eq, shift=UP * 0.3), FadeIn(prod, shift=UP * 0.3), run_time=1.2)
            self.play(Create(box), FadeIn(name))

        geo = MathTex(r"\frac{1}{1 - 2^{-s}} = 1 + \frac{1}{2^s} + \frac{1}{4^s} + \frac1{8^s} + \cdots", font_size=34)
        ex = MathTex(r"\frac{1}{12^s}", r"=", r"\frac{1}{4^s}", r"\cdot", r"\frac{1}{3^s}", font_size=38)
        ex[2].set_color(C.PRIME)
        ex[4].set_color(C.PRIME)
        VGroup(geo, ex).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.5)
        uf = label(r"unique factorization, written as an equation", font_size=30, color=GREY_A).next_to(VGroup(geo, ex), UP, buff=0.3)
        with self.voiceover(
            "It's really the fact that every number factors into primes in exactly one way. <bookmark mark='g'/> Each factor on "
            "the right is a geometric series, and multiplying them out produces every term one over n to the s exactly once, "
            "<bookmark mark='x'/> built from n's prime factors. <bookmark mark='b'/> The left side is about all whole numbers, the "
            "kind of thing you can do analysis with. <bookmark mark='r'/> The right side is about the primes alone."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(geo), FadeIn(uf))
            vo.wait_until("x")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("r")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.wait(0.5)
        self.play(FadeOut(VGroup(geo, ex, uf, b1, b1l, b2, b2l, name)), VGroup(prod, box).animate.to_edge(UP, buff=0.5))
        self.prod = VGroup(prod, box)

    # ------------------------------------------------------------------
    def infinitely_many(self):
        line = MathTex(r"\infty", r"=", r"1 + \tfrac12 + \tfrac13 + \cdots", r"=", r"\frac{2}{1}\cdot\frac{3}{2}\cdot\frac{5}{4}\cdot\frac{7}{6}\cdots",
                       font_size=50)
        line[4].set_color(C.PRIME)
        line.move_to(DOWN * 0.3)
        s1 = label(r"at $s = 1$", font_size=32, color=GREY_A).next_to(line, UP, buff=0.4)
        concl = label(r"a product of finitely many factors is finite $\Rightarrow$ \textbf{infinitely many primes}",
                      font_size=34, color=C.PRIME).next_to(line, DOWN, buff=0.7)
        with self.voiceover(
            "Euler put it to work right away. <bookmark mark='s'/> At s equals one, the sum on the left is the harmonic series, "
            "which diverges. <bookmark mark='p'/> So the product on the right must be infinite too. <bookmark mark='c'/> But a "
            "product of finitely many factors is finite. So there must be infinitely many primes: a new proof of Euclid's "
            "theorem, and the first hint that the primes are hidden inside zeta."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(s1), Write(line[:3]))
            vo.wait_until("p")
            self.play(Write(line[3:]))
            vo.wait_until("c")
            self.play(FadeIn(concl, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
