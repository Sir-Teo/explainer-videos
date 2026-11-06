from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Toolkit(VoiceoverScene):
    def construct(self):
        self.card()
        self.clock()
        self.euclid()
        self.squaring()

    def card(self):
        card = chapter_card(2, r"The toolkit: \ modular arithmetic", r"How do you compute with numbers of 600 digits?",
                            lit=(1801,), extra=((1801, r"Gauss's \textit{Disquisitiones}"),), part=PART)
        with self.voiceover("Chapter two. The toolkit: modular arithmetic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def clock(self):
        head = label(r"Arithmetic on a clock", font_size=34).to_edge(UP, buff=0.3)
        n = 12
        c0 = np.array([-3.6, 0.2, 0])
        R = 2.0
        ring = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(c0)
        nums = VGroup(*[mono(str(i), 22, WHITE).move_to(c0 + 1.15 * R * np.array([math.sin(2 * math.pi * i / n),
                                                                                math.cos(2 * math.pi * i / n), 0]))
                        for i in range(n)])
        ticks = VGroup(*[Dot(c0 + R * np.array([math.sin(2 * math.pi * i / n), math.cos(2 * math.pi * i / n), 0]),
                             radius=0.06, color=GREY_B) for i in range(n)])
        hand = Arrow(c0, c0 + 0.85 * R * np.array([math.sin(2 * math.pi * 9 / n), math.cos(2 * math.pi * 9 / n), 0]),
                     buff=0, color=HEAD, stroke_width=4)
        hand2 = Arrow(c0, c0 + 0.85 * R * np.array([math.sin(2 * math.pi * 4 / n), math.cos(2 * math.pi * 4 / n), 0]),
                      buff=0, color=YES, stroke_width=4)
        notes = VGroup(
            label(r"$9 + 7 = 16 \equiv 4 \pmod{12}$", font_size=26, color=YES),
            label(r"keep only the remainder: \\ numbers never grow past $n$", font_size=22, color=WHITE),
            label(r"$+$, \ $-$, \ $\times$ all work; \ division by $a$ \\ needs an inverse: \ $a \cdot a^{-1} \equiv 1$",
                  font_size=22, color=HEAD),
            label(r"$a^{-1}$ exists exactly when $\gcd(a, n) = 1$: \\ $5 \cdot 5 = 25 \equiv 1$, \ but $4$ has none "
                  r"mod 12", font_size=22, color=DATA),
            label(r"Gauss \ (1801), \ \textit{Disquisitiones Arithmeticae}", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.2, 0])
        with self.voiceover(
            "Public-key cryptography computes with numbers hundreds of digits long, but always on a clock. <bookmark "
            "mark='a'/> On a twelve-hour clock, nine plus seven is four: keep only the remainder after dividing by "
            "twelve. Arithmetic modulo n never lets numbers grow past n. <bookmark mark='b'/> Addition, subtraction and "
            "multiplication work as usual. Division is the question: to divide by a you need an inverse, a number that "
            "multiplied by a gives one. <bookmark mark='c'/> An inverse exists exactly when a shares no factor with n. "
            "Five times five is twenty-five, which is one on this clock, so five is its own inverse; four has none. "
            "<bookmark mark='d'/> Gauss wrote the theory down in 1801. Finding inverses quickly needs an algorithm "
            "two thousand years older."
        ) as vo:
            self.play(FadeIn(head), Create(ring), FadeIn(ticks), FadeIn(nums))
            vo.wait_until("a")
            self.play(GrowArrow(hand))
            self.play(Transform(hand, hand2), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def euclid(self):
        d = load("euclid")
        head = label(r"Euclid, \ extended", font_size=34).to_edge(UP, buff=0.3)
        tr = d["trace"]
        # each remainder r_i with coefficients x_i, y_i such that 240 x_i + 46 y_i = r_i
        seqr = [240, 46] + [r["next"] for r in tr]
        xs, ys = [1, 0], [0, 1]
        qs = []
        for i in range(len(tr)):
            q = seqr[i] // seqr[i + 1]
            qs.append(q)
            xs.append(xs[-2] - q * xs[-1])
            ys.append(ys[-2] - q * ys[-1])
        body = [[str(seqr[i]), "" if i < 2 else str(qs[i - 2]), str(xs[i]), str(ys[i]),
                 rf"$240 \cdot ({xs[i]}) + 46 \cdot ({ys[i]})$"] for i in range(len(seqr) - 1)]
        tab = grid_table([r"remainder", r"quotient", r"$x$", r"$y$", r"check"], body,
                         widths=[1.6, 1.4, 1.0, 1.0, 4.4], row_h=0.48, font_size=21, mono_cols=(0, 1, 2, 3))
        tab.next_to(head, DOWN, buff=0.45)
        last = tab.cells[len(body)]
        ring = SurroundingRectangle(VGroup(*last), color=YES, buff=0.06)
        g, x, y = d["g"]
        lines = VGroup(
            label(r"divide, keep the remainder, repeat: \ $\gcd(240, 46) = 2$ \ (Euclid, \ c.\ 300 BC)", font_size=21,
                  color=WHITE),
            label(r"carry the coefficients along: \ every remainder is $240x + 46y$", font_size=21, color=DATA),
            label(rf"so $240 \cdot ({x}) + 46 \cdot {y} = {g}$: \ \textbf{{B\'ezout}}", font_size=21, color=YES),
            label(rf"when $\gcd(a, n) = 1$, \ the same gives $a^{{-1}}$: \ $17^{{-1}} \bmod 3120 = {d['inv']}$ \ "
                  r"(chapter 5's RSA key)", font_size=21, color=HEAD),
            label(r"steps $\approx$ the number of digits: \ fast for 600-digit numbers", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Euclid's algorithm, from about 300 BC, finds the greatest common divisor. <bookmark mark='a'/> Divide "
            "two hundred and forty by forty-six, keep the remainder, ten; divide forty-six by ten, and so on, until "
            "the remainder is zero. The last nonzero remainder, two, is the gcd. <bookmark mark='b'/> The extension: "
            "carry two coefficients along, so that every remainder is written as some multiple of two hundred and forty "
            "plus some multiple of forty-six. <bookmark mark='c'/> At the end, two equals two hundred and forty times "
            "minus nine, plus forty-six times forty-seven. That is Bézout's identity. <bookmark mark='d'/> When the gcd "
            "is one, the same identity hands you an inverse. The inverse of seventeen modulo three thousand one hundred "
            "and twenty is two thousand seven hundred and fifty-three, a number we will meet as an RSA key. <bookmark "
            "mark='e'/> The number of steps grows only with the number of digits, so this is instant even for numbers "
            "six hundred digits long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*row[:2])) for row in tab.cells[1:]], lag_ratio=0.3),
                      FadeIn(lines[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*row[2:])) for row in tab.cells[1:]], lag_ratio=0.3),
                      FadeIn(lines[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def squaring(self):
        d = load("euclid")
        head = label(r"Powers by repeated squaring", font_size=34).to_edge(UP, buff=0.3)
        e = 218
        bits = bin(e)[2:]
        steps = d["pow"]
        cells = VGroup()
        for i, (b, v) in enumerate(steps):
            op = r"square, \ $\times 3$" if b else r"square"
            col = VGroup(mono(str(b), 30, YES if b else GREY_B), label(op, font_size=17, color=GREY_A),
                         mono(str(v), 24, WHITE)).arrange(DOWN, buff=0.18)
            cells.add(col)
        cells.arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.9)
        el = label(rf"$3^{{{e}}} \bmod 1000$: \ the exponent in binary is \texttt{{{bits}}}", font_size=24,
                   color=WHITE).next_to(cells, UP, buff=0.35)
        res = label(rf"$= {d['pow_value']}$: \ {len(steps)} squarings and {bits.count('1')} multiplications, \ not "
                    rf"{e - 1}", font_size=24, color=YES).next_to(cells, DOWN, buff=0.4)
        lines = VGroup(
            label(r"read the exponent's bits from the top: \ square every time, \ multiply by the base on a 1",
                  font_size=21, color=WHITE),
            label(rf"a 2048-bit exponent: \ about {d['big_mults']:,} multiplications \ (instead of $2^{{2048}}$)"
                  .replace(",", "{,}"), font_size=21, color=HEAD),
            label(r"Part 16 counted its steps; \ Part 20's primality test runs on it; \ chapter 9 does it on a curve",
                  font_size=21, color=GREY_A),
            label(r"so: \ inverses, \ powers and gcds of 600-digit numbers take milliseconds", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The other tool is raising to a huge power. <bookmark mark='a'/> To compute three to the two hundred and "
            "eighteen, modulo a thousand, don't multiply two hundred and seventeen times. Write the exponent in binary. "
            "<bookmark mark='b'/> Then read its bits from the top. For every bit, square what you have; when the bit is "
            "a one, also multiply by three. Eight squarings and five multiplications, and the answer is four hundred "
            "and eighty-nine. <bookmark mark='c'/> A two-thousand-bit exponent needs about four thousand "
            "multiplications, rather than two to the two thousand. <bookmark mark='d'/> Part 16 counted its steps, "
            "Part 20's primality test ran on it, and it will reappear on elliptic curves. <bookmark mark='e'/> With Euclid and "
            "squaring, the basic operations on six-hundred-digit numbers take milliseconds. What makes them useful for "
            "secrets is structure, the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(el))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells], lag_ratio=0.35), FadeIn(lines[0]),
                      run_time=3.0)
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
