from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Hilbert(VoiceoverScene):
    def construct(self):
        self.card()
        self.pell()
        self.dprm()
        self.primes()

    def card(self):
        card = chapter_card(7, r"Hilbert's tenth problem", r"Can you decide whether an equation has whole-number "
                            r"solutions?", lit=(1900, 1970), extra=((1900, r"Hilbert"), (1970, r"Matiyasevich")),
                            part=PART)
        with self.voiceover("Chapter seven. Hilbert's tenth problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pell(self):
        h = load("hilbert")
        head = label(r"Searching is not deciding", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["D"]), r["x"] if len(r["x"]) < 22 else r["x"][:20] + "...", str(r["digits"])]
                for r in h["rows"]]
        tab = grid_table([r"$D$", r"least $x$ with $x^2 - D y^2 = 1$", r"digits"], rows, widths=[1.2, 6.2, 1.4],
                         row_h=0.38, font_size=19, mono_cols=(1,), colors=[[WHITE, HEAD, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        b = {r["D"]: r for r in h["brute"]}
        notes = VGroup(
            label(rf"brute force over $y$: \ $D = 13$ in {b[13]['tried']} tries, \ $D = 29$ in {words(b[29]['tried'])}; "
                  rf"\ $D = 61$: \ {words(b[61]['tried'])} tries, \ nothing", font_size=21, color=NO),
            label(r"continued fractions find each in microseconds: \ Pell's equation always has a solution "
                  r"\ (Lagrange, 1768)", font_size=21, color=YES),
            label(r"a search that finds nothing proves nothing: \ is the answer far away, \ or absent?", font_size=21,
                  color=WHITE),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "In 1900 David Hilbert asked for a process that decides, for any polynomial equation with integer "
            "coefficients, whether it has a solution in integers. <bookmark mark='a'/> Pell's equation shows why "
            "searching is not enough. For D equal to thirteen, the smallest solution has x equal to six hundred and "
            "forty-nine; for sixty-one, a ten-digit number; for nine hundred and ninety-one, thirty digits. "
            "<bookmark mark='b'/> Brute force over y finds thirteen's in a hundred and eighty tries and twenty-nine's in "
            "eighteen hundred, but for sixty-one, seventy-eight million tries in twenty seconds find nothing. "
            "<bookmark mark='c'/> For Pell's equation we are lucky: continued fractions find the answer at once, and "
            "Lagrange proved one always exists. <bookmark mark='d'/> In general a search that has found nothing has "
            "proved nothing. The answer could be further out, or there could be none. Hilbert hoped for a method "
            "that always knows which."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.15))
            for mk, n_ in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def dprm(self):
        head = label(r"The answer: \ no such process", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a set $S$ is \textbf{Diophantine} if $\ n \in S \iff \exists x_1, \ldots, x_k: \ p(n, x_1, \ldots, "
                  r"x_k) = 0$", font_size=22, color=WHITE),
            label(r"Davis, \ Putnam and Robinson \ (1961): \ every recognizable set is Diophantine \textbf{if} "
                  r"exponentiation is", font_size=22, color=DATA),
            label(r"Matiyasevich \ (1970): \ it is: \ $y = 2^x$ is Diophantine, \ built from the Fibonacci numbers",
                  font_size=22, color=HEAD),
            label(r"\textbf{DPRM theorem}: \ recognizable $=$ Diophantine", font_size=24, color=YES),
            label(r"so some polynomial $p_K(n, \vec x)$ has a solution exactly when machine $n$ halts on itself",
                  font_size=22, color=WHITE),
            label(r"deciding solvability would decide halting: \ Hilbert's tenth problem has no solution",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The answer took seventy years and four people. <bookmark mark='a'/> Call a set of numbers Diophantine "
            "if it is exactly the set of parameters for which some polynomial equation has a solution. <bookmark "
            "mark='b'/> In 1961 Martin Davis, Hilary Putnam and Julia Robinson proved that every recognizable set is "
            "Diophantine, provided that exponentiation is. <bookmark mark='c'/> In 1970 Yuri Matiyasevich, aged "
            "twenty-two, closed the gap: the relation y equals two to the x is Diophantine, with a construction built "
            "on the Fibonacci numbers. <bookmark mark='d'/> So the recognizable sets and the Diophantine sets are the "
            "same. <bookmark mark='e'/> In particular there is a polynomial that has a solution exactly when machine "
            "number n halts on itself. <bookmark mark='f'/> A process for Hilbert's problem would decide halting. "
            "There is none."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def primes(self):
        head = label(r"A polynomial whose positive values are the primes", font_size=30).to_edge(UP, buff=0.3)
        poly = MathTex(
            r"(k+2)\Big(1 - (wz+h+j-q)^2 - ((gk+2g+k+1)(h+j)+h-z)^2 - (2n+p+q+z-e)^2",
            r"\\ - (16(k+1)^3(k+2)(n+1)^2+1-f^2)^2 - (e^3(e+2)(a+1)^2+1-o^2)^2 - ((a^2-1)y^2+1-x^2)^2",
            r"\\ - (16r^2y^4(a^2-1)+1-u^2)^2 - (((a+u^2(u^2-a))^2-1)(n+4dy)^2+1-(x+cu)^2)^2",
            r"\\ - (n+l+v-y)^2 - ((a^2-1)l^2+1-m^2)^2 - (ai+k+1-l-i)^2",
            r"\\ - (p+l(a-n-1)+b(2an+2a-n^2-2n-2)-m)^2 - (q+y(a-p-1)+s(2ap+2a-p^2-2p-2)-x)^2",
            r"\\ - (z+pl(a-p)+t(2ap-p^2-1)-pm)^2\Big)", font_size=21, color=HEAD)
        if poly.width > 13.2:
            poly.width = 13.2
        poly.next_to(head, DOWN, buff=0.4)
        notes = VGroup(
            label(r"Jones, \ Sato, \ Wada and Wiens \ (1976): \ 26 variables $a, \ldots, z$, \ degree 25", font_size=22,
                  color=WHITE),
            label(r"each positive value, \ over all non-negative integers, \ is a prime, \ and every prime occurs",
                  font_size=22, color=YES),
            label(r"the big bracket is $1 - \sum(\text{squares})$: \ positive only when every square is 0, \ i.e. "
                  r"when the 14 equations hold", font_size=21, color=DATA),
            label(r"useless for finding primes: \ the point is that ``$k + 2$ is prime'' \textbf{is} a Diophantine "
                  r"statement", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(poly, DOWN, buff=0.4)
        with self.voiceover(
            "A striking corollary. <bookmark mark='a'/> The primes are a recognizable set, so they are Diophantine, "
            "and James Jones, Daihachiro Sato, Hideo Wada and Douglas Wiens wrote the polynomial out in 1976: "
            "twenty-six variables, one for each letter of the alphabet, degree twenty-five. <bookmark mark='b'/> "
            "Plug in any non-negative integers. Whenever the value is positive, it is a prime, and every prime "
            "appears. <bookmark mark='c'/> The trick is the shape: k plus two, times one minus a sum of squares. That "
            "is positive only when every square is zero, that is, when fourteen equations hold at once, and they "
            "hold exactly when k plus two is prime. <bookmark mark='d'/> Nobody would find primes this way; random "
            "inputs give negative values almost always. The point is that primality, like halting, can be written "
            "as a single equation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(poly, lag_ratio=0.05), run_time=2.5)
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
