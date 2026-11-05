from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Generating(VoiceoverScene):
    def construct(self):
        self.card()
        self.fibonacci()
        self.catalan()

    def card(self):
        card = chapter_card(12, r"Generating functions", r"Can a sequence be a single function?", lit=(1730,),
                            extra=((1730, r"de Moivre's generating functions"),), part=PART)
        with self.voiceover("Chapter twelve. Generating functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fibonacci(self):
        d = load("gf")
        head = label(r"A sequence, \ packed into a function", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            MathTex(r"F(z) = \sum_{n \ge 0} F_n z^n = 0 + z + z^2 + 2z^3 + 3z^4 + 5z^5 + \cdots", font_size=32),
            MathTex(r"F_n = F_{n-1} + F_{n-2} \;\Longrightarrow\; F(z) = z + zF(z) + z^2 F(z)", font_size=32),
            MathTex(r"F(z) = \frac{z}{1 - z - z^2} = \frac{1}{\sqrt5}\left(\frac{1}{1 - \varphi z} - "
                    r"\frac{1}{1 - \hat\varphi z}\right)", font_size=32),
            MathTex(r"F_n = \frac{\varphi^n - \hat\varphi^n}{\sqrt5}, \qquad \varphi = \tfrac{1 + \sqrt5}{2}",
                    font_size=34, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        chk = label(rf"checked against the recurrence for $n \le 61$: \ {'all equal' if d['fib_ok'] else 'mismatch'}",
                    font_size=20, color=GREY_B).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Recurrences like quicksort's are often solved by a trick from the eighteenth century: turn the whole "
            "sequence into one function. <bookmark mark='a'/> Make the Fibonacci numbers the coefficients of a "
            "power series, F of z. <bookmark mark='b'/> The recurrence, each term the sum of the two before, becomes "
            "an equation about the function itself: F equals z plus z F plus z squared F. <bookmark mark='c'/> "
            "Solve it like algebra: F is z over one minus z minus z squared, and partial fractions split it into "
            "two geometric series. <bookmark mark='d'/> Read off the coefficient, and out comes Binet's formula, "
            "with the golden ratio. We checked it against the recurrence for every n up to sixty-one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(Write(s))
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    def catalan(self):
        d = load("gf")
        head = label(r"Catalan numbers, \ and reading the singularity", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"binary trees with $n$ nodes: \ " + r", \ ".join(str(c) for c in d["catalan"][:9]) + r", \ \ldots",
                  font_size=22, color=GREY_A),
            MathTex(r"C(z) = 1 + z\,C(z)^2 \;\Longrightarrow\; C(z) = \frac{1 - \sqrt{1 - 4z}}{2z} \;\Longrightarrow\; "
                    r"C_n = \frac{1}{n+1}\binom{2n}{n}", font_size=30),
            label(r"the square root vanishes at $z = 1/4$: \ that singularity fixes the growth", font_size=22,
                  color=YES),
            MathTex(r"C_n \sim \frac{4^n}{\sqrt{\pi}\, n^{3/2}}", font_size=36, color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[str(a["n"]), f"{a['ratio']:.4f}"] for a in d["asym"] if a["n"] in (5, 10, 20, 40, 60)]
        tab = grid_table([r"$n$", r"$C_n \,/\, \text{asymptotic}$"], rows, widths=[1.4, 3.0], row_h=0.38,
                         font_size=18).next_to(steps, DOWN, buff=0.3)
        note = label(r"analytic combinatorics \ (Flajolet and Sedgewick, \ 2009): \ the growth of a sequence "
                     r"is written in its function's nearest singularity", font_size=19, color=GREY_B).to_edge(
            DOWN, buff=0.35)
        if note.width > 8.0:
            note.scale_to_fit_width(8.0)
        with self.voiceover(
            "A harder example. <bookmark mark='a'/> The number of binary trees with n nodes: one, one, two, five, "
            "fourteen, forty-two. These are the Catalan numbers, and they count recursion trees, bracketings and "
            "many other things. <bookmark mark='b'/> A tree is empty, or a root with two subtrees, so the "
            "generating function satisfies C equals one plus z C squared. Solve the quadratic, expand the square "
            "root, and the closed form appears: one over n plus one, times two n choose n. <bookmark mark='c'/> "
            "Even without the closed form, the function tells us how fast the numbers grow: the square root "
            "vanishes at one quarter, and that point alone fixes the growth. <bookmark mark='d'/> Four to the n, "
            "divided by the square root of pi times n to the three halves. The ratio of the true value to this "
            "approximation creeps up to one. Flajolet and Sedgewick built a whole subject, analytic "
            "combinatorics, on reading growth rates off singularities."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(tab), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
