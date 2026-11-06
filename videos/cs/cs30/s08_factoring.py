from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class Factoring(VoiceoverScene):
    def construct(self):
        self.card()
        self.rho()
        self.race()
        self.sieve()
        self.records()

    def card(self):
        card = chapter_card(7, r"Factoring", r"How hard is it to split $n$ into $p$ and $q$?", lit=(1975, 1981, 1990),
                            extra=((1975, r"Pollard's rho"), (1981, r"Pomerance: \ quadratic sieve"),
                                   (1990, r"the number field sieve")), part=PART)
        with self.voiceover("Chapter seven. Factoring."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rho(self):
        w = load("rhowalk")
        head = label(r"Pollard's rho", font_size=34).to_edge(UP, buff=0.3)
        walk, tail, cyc = w["walk"], w["tail"], w["cycle"]
        c0 = np.array([-2.6, 0.9, 0])
        R = 1.5
        pos = []
        for i in range(tail):
            pos.append(c0 + np.array([0, -R - 0.55 * (tail - i), 0]))
        for j in range(cyc):
            ang = -math.pi / 2 + 2 * math.pi * j / cyc
            pos.append(c0 + R * np.array([math.cos(ang), math.sin(ang), 0]))
        dots = VGroup(*[Dot(p, radius=0.07, color=HEAD if i >= tail else DATA) for i, p in enumerate(pos)])
        labs = VGroup(*[mono(str(walk[i]), 14, GREY_A).next_to(p, LEFT if i < tail or p[0] < c0[0] else RIGHT,
                                                               buff=0.08) for i, p in enumerate(pos)])
        links = VGroup(*[Arrow(pos[i], pos[i + 1], buff=0.08, stroke_width=1.8, color=GREY_B,
                               max_tip_length_to_length_ratio=0.25) for i in range(len(pos) - 1)])
        links.add(Arrow(pos[-1], pos[tail], buff=0.08, stroke_width=1.8, color=GREY_B, max_tip_length_to_length_ratio=0.25))
        notes = VGroup(
            label(rf"$n = {w['n']:,}$; \ iterate $x \mapsto x^2 + 1 \bmod n$".replace(",", "{,}"), font_size=21,
                  color=WHITE),
            label(rf"look at the values mod the unknown factor $p = {w['p']}$: \\ only $p$ possible values, \ so they "
                  r"must repeat", font_size=21, color=DATA),
            label(rf"a tail of {tail}, \ then a cycle of {cyc}: \ the Greek letter $\rho$", font_size=21, color=HEAD),
            label(r"a repeat mod $p$ means $p \mid x_i - x_j$, \ so $\gcd(x_i - x_j, n)$ reveals $p$", font_size=21,
                  color=YES),
            label(rf"here: \ $\gcd = {w['gcd']}$; \ by the birthday bound, \ about $\sqrt{{p}}$ steps", font_size=21,
                  color=YES),
            label(r"Floyd's tortoise and hare \ (Part 17) \ finds the cycle in constant memory", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.6, 0.3, 0])
        fit_right(notes)
        with self.voiceover(
            "The simplest fast factoring method is John Pollard's, from 1975. <bookmark mark='a'/> Pick a starting "
            "number and iterate: square it, add one, reduce modulo n. The values look random. <bookmark mark='b'/> Now "
            "imagine reducing them, also, modulo the factor p we are looking for, one thousand and nine. There are only "
            "p possible values, so by the birthday paradox they start repeating after about the square root of p "
            "steps. <bookmark mark='c'/> Here, after a tail of seven values, the sequence falls into a cycle of "
            "fourteen. Drawn out, it has the shape of the Greek letter rho. <bookmark mark='d'/> We cannot see the "
            "values mod p, but we don't need to. A repeat mod p means p divides the difference of two values, so the "
            "gcd of that difference with n is p. <bookmark mark='e'/> And it is: one thousand and nine. <bookmark "
            "mark='f'/> Part 17's tortoise-and-hare trick detects the cycle without storing the sequence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(dots, labs)],
                                  lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3),
                      run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]), Indicate(dots[tail], color=YES))
            vo.wait_until("f")
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()

    def race(self):
        f = load("factoring")
        head = label(r"Rho against the sieve, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = f["rows"]
        ax = Axes(x_range=[8, 36, 4], y_range=[0, 7, 1], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        lg = lambda s: math.log10(s) + 4      # noqa: E731
        rho = VMobject(color=DATA, stroke_width=3).set_points_as_corners([ax.c2p(r["digits"], lg(r["rho_s"]))
                                                                          for r in rows])
        qs = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([ax.c2p(r["digits"], lg(r["qs_s"]))
                                                                         for r in rows])
        dr = VGroup(*[Dot(ax.c2p(r["digits"], lg(r["rho_s"])), radius=0.05, color=DATA) for r in rows])
        dq = VGroup(*[Dot(ax.c2p(r["digits"], lg(r["qs_s"])), radius=0.05, color=HEAD) for r in rows])
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (10, 18, 26, 34)])
        yt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(8, y), LEFT, buff=0.08)
                      for y, t in ((1, "1 ms"), (4, "1 s"), (5.78, "1 min"))])
        xl = label(r"digits of $n = pq$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        keys = VGroup(label(r"Pollard's rho", font_size=18, color=DATA), label(r"our quadratic sieve", font_size=18,
                                                                               color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(14, 6.2))
        last = rows[-1]
        notes = VGroup(
            label(r"rho: \ about $\sqrt{p} \approx n^{1/4}$ steps: \\ exponential in the digits", font_size=20,
                  color=DATA),
            label(r"the sieve: \ $e^{\sqrt{\ln n \ln \ln n}}$: \\ \textbf{sub}-exponential", font_size=20, color=HEAD),
            label(rf"at {last['digits']} digits: \ rho {last['rho_s']:.0f} s, \\ sieve {last['qs_s']:.0f} s "
                  r"\ (Python)", font_size=20, color=WHITE),
            label(r"the sieve's lead appears past \\ about 40 digits, \ and grows \\ without limit", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How does rho scale? We factored products of two equal-sized primes, from ten digits to thirty-four. "
            "<bookmark mark='a'/> Rho needs about the square root of the smaller prime, the fourth root of n, so its "
            "time grows exponentially in the number of digits: a straight line on this logarithmic scale. <bookmark "
            "mark='b'/> The quadratic sieve, which we build next, grows more slowly than any exponential: "
            "sub-exponentially. <bookmark mark='c'/> In our Python, at these small sizes, the two are close: at "
            "thirty-four digits rho took forty-three seconds and the sieve eighty-seven. <bookmark mark='d'/> But the "
            "sieve's curve bends. Past about forty digits it wins, and the gap then grows without limit. For RSA-sized "
            "numbers, only the sieves matter."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(rho), FadeIn(dr), FadeIn(keys[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(qs), FadeIn(dq), FadeIn(keys[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def sieve(self):
        f = load("factoring")
        head = label(r"The quadratic sieve", font_size=34).to_edge(UP, buff=0.3)
        ex = f["qs_example"]
        st = f["qs_stats"]
        fac = r" \cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in sorted(ex["factors"].items(),
                                                                                    key=lambda kv: int(kv[0])))
        lines = VGroup(
            label(r"goal: \ $x^2 \equiv y^2 \pmod n$ with $x \ne \pm y$: \ then $n \mid (x - y)(x + y)$, \ and "
                  r"$\gcd(x - y, n)$ is a factor", font_size=22, color=WHITE),
            label(r"near $\sqrt{n}$, \ $x^2 - n$ is small: \ keep the $x$ whose $x^2 - n$ is \textbf{smooth} \ "
                  r"(only small prime factors)", font_size=22, color=DATA),
            label(rf"one of ours: \ $x = {ex['x']:,}$, \ $x^2 - n = {ex['value']:,} = {fac}$".replace(",", "{,}"),
                  font_size=22, color=HEAD),
            label(r"sieve, \ like Eratosthenes \ (Part 16): \ mark multiples of each small prime, \ not trial-divide",
                  font_size=22, color=GREY_A),
            label(r"each smooth value is a vector of exponents mod 2; \ a set summing to zero \ (linear algebra over "
                  r"GF(2)) \ multiplies to a square", font_size=22, color=LAM),
            label(rf"for our 20-digit $n$: \ {st['base']} small primes, \ {st['relations']} relations, \ a "
                  rf"dependency of {st['dependency']}: \ factor \texttt{{{f['qs_factor']}}}", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "The sieve rests on an old idea of Fermat's, sharpened by Carl Pomerance in 1981. <bookmark mark='a'/> If "
            "you can find x and y whose squares agree modulo n, but which are not equal or opposite, then n divides "
            "x minus y times x plus y, and a gcd splits it. <bookmark mark='b'/> To build such squares, take x just "
            "above the square root of n, so that x squared minus n is fairly small, and keep only the x for which it "
            "is smooth: a product of small primes. <bookmark mark='c'/> Here is one from our run: a twelve-digit value "
            "that factors entirely into primes below thirteen hundred. <bookmark mark='d'/> Finding them is a sieve, "
            "like Eratosthenes': for each small prime, mark the positions it divides, rather than testing each value. "
            "<bookmark mark='e'/> Write each smooth value's exponents mod two as a vector. A set of vectors summing to "
            "zero, which Gaussian elimination over the two-element field finds, multiplies to a perfect square on both "
            "sides. <bookmark mark='f'/> For our twenty-digit number: a hundred and sixteen small primes, a hundred and "
            "twenty-seven relations, a combination of forty-six of them, and the factor."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def records(self):
        head = label(r"How big a key?", font_size=34).to_edge(UP, buff=0.3)
        recs = [(1991, 100, r"RSA-100"), (1999, 155, r"RSA-155 \ (512 bits)"), (2009, 232, r"RSA-768"),
                (2020, 250, r"RSA-250 \ (829 bits)")]
        ax = Axes(x_range=[1985, 2030, 5], y_range=[0, 650, 100], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=1.0)
        dots = VGroup(*[Dot(ax.c2p(y, d), radius=0.07, color=HEAD) for y, d, _ in recs])
        labs = VGroup(*[label(t, font_size=16, color=HEAD).next_to(ax.c2p(y, d), UP + LEFT * 0.3, buff=0.1)
                        for y, d, t in recs])
        rsa2048 = DashedLine(ax.c2p(1985, 617), ax.c2p(2030, 617), color=NO, stroke_width=2)
        rl = label(r"RSA-2048: \ 617 digits", font_size=17, color=NO).next_to(rsa2048, DOWN, buff=0.08).align_to(
            ax, RIGHT)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (1990, 2000, 2010, 2020)])
        yl = label(r"digits factored", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        notes = VGroup(
            label(r"the \textbf{number field sieve} \ (1990s): \\ $\exp\bigl(1.92 (\ln n)^{1/3} "
                  r"(\ln\ln n)^{2/3}\bigr)$", font_size=20, color=WHITE),
            label(r"RSA-250: \ about 2{,}700 \\ core-years \ (2020)", font_size=20, color=HEAD),
            label(r"2048-bit RSA: \ far out of reach; \\ about 112 bits of security", font_size=20, color=YES),
            label(r"keys must grow fast: \ 3072 bits \\ for 128-bit security, \ 15360 for 256", font_size=20,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "The fastest known method is the number field sieve, from the early nineteen-nineties, which takes the "
            "same idea into algebraic number fields. <bookmark mark='a'/> Its running time grows like the exponential "
            "of the cube root of the number of digits, roughly. <bookmark mark='b'/> Public records track it: a "
            "hundred digits in 1991; RSA-155, a five-hundred-and-twelve-bit key, in 1999; RSA-250, eight hundred and "
            "twenty-nine bits, in 2020, at a cost of about two thousand seven hundred core-years. <bookmark mark='c'/> "
            "A two-thousand-and-forty-eight-bit key, six hundred and seventeen digits, is far beyond this line, and is "
            "rated at about a hundred and twelve bits of security. <bookmark mark='d'/> But the curve is "
            "sub-exponential, so key sizes must grow quickly for more security: three thousand and seventy-two bits for "
            "a hundred and twenty-eight, fifteen thousand for two hundred and fifty-six. Elliptic curves, chapter "
            "nine, do much better."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(dots, labs)],
                                  lag_ratio=0.4), FadeIn(notes[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(rsa2048), FadeIn(rl), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
