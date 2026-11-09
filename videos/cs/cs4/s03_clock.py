from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bit_cells, load

R = 2.15


def wheel(center, signed=False, show_bits=True):
    ring = Circle(R, color=GREY_C, stroke_width=2).move_to(center)
    pos, labels, bits = [], VGroup(), VGroup()
    for k in range(16):
        ang = PI / 2 - 2 * PI * k / 16
        u = np.array([np.cos(ang), np.sin(ang), 0])
        pos.append(center + R * u)
        v = k - 16 if (signed and k >= 8) else k
        labels.add(MathTex(str(v), font_size=28, color=NO if v < 0 else DATA).move_to(center + (R + 0.42) * u))
        bits.add(MathTex(format(k, "04b"), font_size=18, color=GREY_B).move_to(center + (R - 0.48) * u))
    dots = VGroup(*[Dot(p, radius=0.05, color=GREY_B) for p in pos])
    g = VGroup(ring, dots, labels, bits) if show_bits else VGroup(ring, dots, labels)
    g.pos, g.labels, g.center_ = pos, labels, np.asarray(center)
    return g


def arc_path(w, a, steps, color=HEAD):
    """An arc along the wheel from position a, ``steps`` clicks clockwise."""
    c = w.center_
    ang0 = PI / 2 - 2 * PI * a / 16
    return Arc(radius=R + 0.9 - 0.0, start_angle=ang0, angle=-2 * PI * steps / 16, color=color, stroke_width=5,
               arc_center=c).add_tip(tip_length=0.2)


class Clock(VoiceoverScene):
    def construct(self):
        self.card()
        self.unsigned()
        self.twos()
        self.negate()
        self.overflow()

    def card(self):
        card = chapter_card(2, r"Integers on a clock", r"How does a fixed number of bits hold negative numbers?",
                            part=PART)
        with self.voiceover("Chapter two. Integers on a clock."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def unsigned(self):
        head = label(r"Four bits: \ arithmetic modulo 16", font_size=38).to_edge(UP, buff=0.35)
        w = wheel(LEFT * 2.6 + DOWN * 0.4)
        p = arc_path(w, 13, 5)
        eq = VGroup(MathTex(r"13 + 5 = 18", font_size=40, color=GREY_A),
                    MathTex(r"18 - 16 = 2", font_size=40, color=HEAD),
                    MathTex(r"13 + 5 \equiv 2 \pmod{16}", font_size=40, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.8 + UP * 0.6)
        carry = label(r"the lost 16 \ is the carry out of the top bit", font_size=26, color=GREY_A).next_to(
            eq, DOWN, buff=0.5).align_to(eq, LEFT)
        ring = MathTex(r"\mathbb{Z}/2^n\mathbb{Z}", font_size=44, color=CODE).next_to(carry, DOWN, buff=0.5).align_to(
            eq, LEFT)
        with self.voiceover(
            "Four bits make sixteen patterns. <bookmark mark='a'/> Lay them around a clock face, zero at the top, "
            "counting clockwise to fifteen. Adding is turning the hand: to add five, go five clicks. "
            "<bookmark mark='b'/> Thirteen plus five goes past fifteen and comes round to two. Eighteen does not fit "
            "in four bits, so the hardware keeps eighteen minus sixteen. <bookmark mark='c'/> The sixteen that went "
            "missing is the carry out of the top bit. This is arithmetic modulo two to the n, the integers on a clock, "
            "and every adder in this part computes it: it is the most honest description of what a register holds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.labels[13], color=HEAD))
            vo.wait_until("b")
            self.play(Create(p), run_time=1.5)
            self.play(Indicate(w.labels[2], color=HEAD), FadeIn(eq[0]), FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq[2]), FadeIn(carry), FadeIn(ring))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twos(self):
        head = label(r"Two's complement: \ relabel half the clock", font_size=38).to_edge(UP, buff=0.35)
        w = wheel(LEFT * 2.6 + DOWN * 0.4)
        ws = wheel(LEFT * 2.6 + DOWN * 0.4, signed=True)
        p = arc_path(w, 13, 5)
        eq = MathTex(r"-3 + 5 = 2", font_size=44, color=YES).move_to(RIGHT * 3.6 + UP * 2.0)
        same = label(r"the same bits, \ the same adder", font_size=28, color=HEAD).next_to(eq, DOWN, buff=0.3)
        val = MathTex(r"x = -b_{n-1}\,2^{n-1} + \sum_{i=0}^{n-2} b_i\, 2^i", font_size=38, color=CODE).move_to(
            RIGHT * 3.6 + DOWN * 0.2)
        ex = MathTex(r"1101 = -8 + 4 + 1 = -3", font_size=34, color=GREY_A).next_to(val, DOWN, buff=0.35)
        rng = label(r"range: \ $-2^{n-1} \dots 2^{n-1} - 1$; \ the top bit is the sign", font_size=26,
                    color=GREY_A).next_to(ex, DOWN, buff=0.4)
        with self.voiceover(
            "Now the trick that every computer uses for negative numbers. <bookmark mark='a'/> Keep the clock, and "
            "relabel patterns eight through fifteen: fifteen is one step before zero, so call it minus one; fourteen is minus two; "
            "down to eight, which becomes minus eight. <bookmark mark='b'/> Thirteen is now minus three, and turning "
            "five clicks still lands on two. Minus three plus five is two. Nothing changed but the labels: the same "
            "bits, and the same adder, serve signed and unsigned numbers. <bookmark mark='c'/> In formulas, the top bit "
            "counts as minus two to the n minus one instead of plus, and so it doubles as the sign. One, one, zero, "
            "one is minus eight plus four plus one: minus three. This is two's complement, proposed by John von "
            "Neumann in 1945, and it won because the hardware gets it for free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(*[Transform(w.labels[k], ws.labels[k]) for k in range(8, 16)], run_time=2.0)
            vo.wait_until("b")
            self.play(Create(p), run_time=1.5)
            self.play(FadeIn(eq), FadeIn(same))
            vo.wait_until("c")
            self.play(Write(val), FadeIn(ex), FadeIn(rng))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def negate(self):
        d = load("clock")
        head = label(r"Negation: \ invert every bit, \ then add 1", font_size=38).to_edge(UP, buff=0.35)
        proof = VGroup(MathTex(r"x + \bar{x} = 11\cdots1 = -1", font_size=40, color=GREY_A),
                       MathTex(r"\Rightarrow \quad -x = \bar{x} + 1", font_size=44, color=YES)).arrange(
            DOWN, buff=0.3).move_to(UP * 1.9)
        rows = VGroup()
        for e in d["neg_examples"]:
            x = e["x"]
            r = VGroup(MathTex(str(x), font_size=30, color=DATA if x >= 0 else NO),
                       MathTex(e["bits"], font_size=30, color=GREY_A),
                       MathTex(r"\xrightarrow{\text{invert}}", font_size=28, color=GREY_C),
                       MathTex(e["inv"], font_size=30, color=GREY_A),
                       MathTex(r"\xrightarrow{+1}", font_size=28, color=GREY_C),
                       MathTex(e["neg"], font_size=30, color=YES),
                       MathTex("= " + str(-x if x != -128 else -128), font_size=30, color=YES if x != -128 else NO))
            rows.add(r)
        for r in rows:
            for j, m in enumerate(r):
                m.move_to([-5.2 + [0, 1.5, 3.1, 4.6, 6.2, 7.7, 9.3][j], 0, 0])
        for i, r in enumerate(rows):
            r.shift(DOWN * (0.15 + 0.6 * i))
        odd = label(r"$-(-128) = -128$ in 8 bits: \ the range has one more negative than positive", font_size=26,
                    color=NO).to_edge(DOWN, buff=0.4)
        ext = MathTex(r"\text{sign extension: } \ 1101 \to 1111\,1101 \quad (-3 \text{ in 4 and 8 bits})",
                      font_size=30, color=CTRL).next_to(odd, UP, buff=0.3)
        with self.voiceover(
            "How do you negate a number? <bookmark mark='a'/> Add any x to its bitwise inverse, and every bit is a "
            "one: the pattern for minus one. So minus x equals the inverse of x, plus one. <bookmark mark='b'/> Six is "
            "zero zero zero zero zero one one zero; invert it, add one, and you have minus six. One hundred works the "
            "same way. <bookmark mark='c'/> To widen a number from four bits to eight, copy its sign bit into the new "
            "places: one one zero one is minus three, and so is one one one one, one one zero one, because the new "
            "minus one twenty-eight and the extra ones add up to the old minus eight. <bookmark mark='d'/> One oddity: "
            "the most negative number has no positive partner. Negate minus one hundred and twenty-eight in eight "
            "bits, and you get minus one hundred and twenty-eight back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(proof[0]))
            vo.wait_until("a")
            self.play(Indicate(proof[0], scale_factor=1.03))
            self.play(FadeIn(proof[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ext))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(odd))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overflow(self):
        head = label(r"Overflow", font_size=38).to_edge(UP, buff=0.35)
        w = wheel(LEFT * 3.6 + DOWN * 0.4, signed=True, show_bits=False)
        p = arc_path(w, 5, 4, color=NO)
        eq = MathTex(r"5 + 4 = -7 \ \ ?!", font_size=44, color=NO).move_to(RIGHT * 2.6 + UP * 2.0)
        add = MathTex(r"\begin{array}{r} 0101 \\ +\ 0100 \\ \hline 1001 \end{array}", font_size=40,
                      color=GREY_A).next_to(eq, DOWN, buff=0.35)
        rules = VGroup(
            label(r"unsigned overflow: \ a carry out of the top bit", font_size=26, color=GREY_A),
            label(r"signed overflow: \ the carry \textit{into} the top bit $\ne$ the carry out", font_size=26,
                  color=HEAD),
            label(r"(two positives make a negative, \ or two negatives a positive)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(add, DOWN, buff=0.45).shift(RIGHT * 0.4)
        langs = note(r"C: \ signed overflow is undefined behaviour; \ Java, Go: \ wraps; \ Rust: \ panics in debug "
                     r"builds; \ Python: \ never overflows (bignums)", font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The clock has an edge, and crossing it is overflow. <bookmark mark='a'/> In signed four-bit arithmetic, "
            "five plus four goes past seven and lands on minus seven. <bookmark mark='b'/> The adder cannot know "
            "whether you meant signed or unsigned, so it reports both kinds of trouble. For unsigned numbers, overflow "
            "is a carry out of the top bit. For signed numbers it is subtler: the result is wrong exactly when the "
            "carry into the top bit differs from the carry out of it, which happens when two positives give a negative "
            "or two negatives a positive. One exclusive-or gate detects it. <bookmark mark='c'/> Languages disagree "
            "about what to do. In C, signed overflow is undefined behaviour, and compilers optimize as if it never "
            "happens; Java and Go wrap around the clock; Rust panics in debug builds; Python's integers simply grow. "
            "Integer overflow is still behind a steady stream of security holes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(Create(p), run_time=1.4)
            self.play(FadeIn(eq), Write(add))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(langs))
        self.wait(0.3)
        self.clear_scene()
