from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, gate, load, wire,
                                  wave)


def cell(bit, size=0.55, col=DATA):
    b = Square(size, stroke_color=GREY_C, stroke_width=2, fill_color=BG, fill_opacity=1)
    return VGroup(b, MathTex(str(bit), font_size=30, color=col if bit else GREY_B).move_to(b))


class Lfsr(VoiceoverScene):
    def construct(self):
        self.card()
        self.counters()
        self.lfsr()
        self.algebra()
        self.table()

    def card(self):
        card = chapter_card(8, r"Counters and shift registers", r"What can a register do with almost no logic?",
                            lit=(1954, 1967), part=PART)
        with self.voiceover("Chapter eight. Counters and shift registers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def counters(self):
        head = label(r"Two simple sequential circuits", font_size=38).to_edge(UP, buff=0.35)
        bits = [format(k, "04b") for k in range(16)]
        ctr = VGroup(*[MathTex(b, font_size=26, color=DATA) for b in bits]).arrange(DOWN, buff=0.05).move_to(LEFT * 4.4 + DOWN * 0.3)
        cl = label(r"a counter: \\ register $+ 1$ every cycle", font_size=24, color=GREY_A).next_to(ctr, RIGHT, buff=0.4)
        regs = VGroup(*[cell(b, col=YES) for b in (1, 0, 1, 1, 0, 0, 1, 0)]).arrange(RIGHT, buff=0.06).move_to(
            RIGHT * 2.6 + UP * 1.0)
        arrows = VGroup(*[Arrow(regs[i].get_right(), regs[i + 1].get_left(), buff=0.0, stroke_width=2, color=WIRE,
                                max_tip_length_to_length_ratio=0.5) for i in range(7)])
        sin = Arrow(regs[0].get_left() + LEFT * 0.6, regs[0].get_left(), buff=0, stroke_width=3, color=DATA)
        sl = label(r"a shift register: \ every bit moves one place per cycle", font_size=24, color=GREY_A).next_to(
            regs, DOWN, buff=0.35)
        uses = label(r"serial links \ (USB, \ PCIe, \ Ethernet) \ turn bytes into streams and back \\ with shift "
                     r"registers", font_size=22, color=HEAD).next_to(sl, DOWN, buff=0.4)
        with self.voiceover(
            "With registers and a clock, some useful circuits need almost no logic. <bookmark mark='a'/> A counter is "
            "a register whose next value is itself plus one: Part 4's adder, fed back. It steps through every number "
            "and wraps around, and it is how a processor keeps its place in a program. <bookmark mark='b'/> A shift "
            "register needs no logic at all: each flip-flop takes the value of its neighbour at every clock edge, so "
            "the whole pattern slides one place per cycle. Every serial link, USB, PCI Express, Ethernet, uses shift "
            "registers to turn parallel words into a stream of bits and back. And with one small change, a shift "
            "register becomes something remarkable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ctr), FadeIn(cl))
            vo.wait_until("a")
            self.play(Indicate(ctr, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(regs), Create(arrows), GrowArrow(sin), FadeIn(sl))
            self.play(FadeIn(uses))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lfsr(self):
        d = load("lfsr")
        seq = d["seq4"]
        head = label(r"A linear-feedback shift register", font_size=38).to_edge(UP, buff=0.35)
        val = ValueTracker(0)
        x = gate("XOR", size=0.7).rotate(PI).move_to(LEFT * 2.5 + UP * 2.0)

        def regs_at(k):
            v = seq[k]
            bits = [(v >> i) & 1 for i in range(4)]
            g = VGroup(*[cell(b) for b in bits]).arrange(RIGHT, buff=0.12).move_to(LEFT * 1.6 + UP * 0.6)
            return g

        regs = regs_at(0)
        hi, lo = sorted([x.inp[0](), x.inp[1]()], key=lambda p: -p[1])
        taps = VGroup(
            VMobject(color=WIRE, stroke_width=2.5).set_points_as_corners(
                [regs[3].get_top(), [regs[3].get_x(), hi[1], 0], hi]),
            VMobject(color=WIRE, stroke_width=2.5).set_points_as_corners(
                [regs[2].get_top(), [regs[2].get_x(), lo[1], 0], lo]))
        tw = VGroup(Dot(taps[0].get_start(), radius=0.05, color=WIRE), Dot(taps[1].get_start(), radius=0.05, color=WIRE))
        o = x.out()
        fb = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(
            [o, [regs[0].get_left()[0] - 0.45, o[1], 0], [regs[0].get_left()[0] - 0.45, 0.6, 0], regs[0].get_left()])
        fbt = Triangle(color=HEAD, fill_opacity=1, stroke_width=0).scale(0.07).rotate(-PI / 2).move_to(
            regs[0].get_left() + LEFT * 0.07)
        fb = VGroup(fb, fbt)
        shift_arrows = VGroup(*[Arrow(regs[i].get_right(), regs[i + 1].get_left(), buff=0.0, color=GREY_C,
                                      stroke_width=2, max_tip_length_to_length_ratio=0.5) for i in range(3)])
        taps.add(shift_arrows)
        idx = VGroup(*[MathTex(f"b_{i}", font_size=22, color=GREY_B).next_to(regs[i], DOWN, buff=0.12) for i in range(4)])
        hist = VGroup()
        for k, v in enumerate(seq[:15]):
            hist.add(MathTex(format(v, "04b")[::-1], font_size=22, color=DATA if k else HEAD))
        hist.arrange(DOWN, buff=0.04).move_to(RIGHT * 3.4 + DOWN * 0.2)
        hl = label(r"15 states, \ then it repeats", font_size=24, color=YES).next_to(hist, LEFT, buff=0.4)
        poly = MathTex(r"x^4 + x^3 + 1", font_size=34, color=CODE).move_to(LEFT * 2.4 + DOWN * 1.8)
        pl = label(r"every nonzero 4-bit pattern \ exactly once: \ period $2^4 - 1$", font_size=26,
                   color=HEAD).next_to(poly, DOWN, buff=0.3)
        with self.voiceover(
            "Take a four-bit shift register, and instead of feeding it from outside, feed it the exclusive-or of two "
            "of its own bits. <bookmark mark='a'/> Each clock cycle, the bits shift along, and the new bit is the "
            "exclusive-or of the last two. Start from one zero zero zero and watch the states. "
            "<bookmark mark='b'/> It runs through fifteen different patterns, every non-zero four-bit pattern exactly "
            "once, in a scrambled-looking order, before coming back to where it started. The all-zero state is the "
            "only one missing, since it would stay zero forever. <bookmark mark='c'/> This is a linear-feedback shift "
            "register, and the choice of taps corresponds to the polynomial x to the four plus x cubed plus one. "
            "With the wrong taps, the cycle would be shorter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(regs), FadeIn(idx), FadeIn(x), Create(taps), Create(tw), Create(fb))
            vo.wait_until("a")
            for k in range(1, 6):
                self.play(Transform(regs, regs_at(k)), FadeIn(hist[k - 1]), run_time=0.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h) for h in hist[5:]], lag_ratio=0.15), FadeIn(hl), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(poly), FadeIn(pl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        head = label(r"Why: \ arithmetic in $\mathrm{GF}(2^n)$", font_size=38).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"read the register as a polynomial over $\{0, 1\}$, \ with $1 + 1 = 0$ \ (in its Galois wiring)",
                  font_size=25, color=GREY_A),
            MathTex(r"b_0 + b_1 x + b_2 x^2 + b_3 x^3", font_size=36, color=CODE),
            label(r"one clock step \ $=$ \ multiply by $x$, \ then reduce modulo $p(x) = x^4 + x^3 + 1$", font_size=25,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(UP * 1.9)
        tail = VGroup(
            label(r"the states are the powers $1, x, x^2, x^3, \ldots$: \ the period is the order of $x$", font_size=25,
                  color=GREY_A),
            label(r"maximal period $2^n - 1$ \ $\iff$ \ $p$ is \textit{primitive}: \ $x$ generates every nonzero "
                  r"element", font_size=25, color=YES),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        size, gap = 0.7, 0.15
        boxes = VGroup(*[Square(size, stroke_color=GREY_C, stroke_width=2) for _ in range(5)]).arrange(RIGHT, buff=gap)
        boxes.move_to(DOWN * 0.45 + RIGHT * 0.4)
        boxes[4].set_stroke(NO, opacity=0.8).set_fill(opacity=0)
        ghost = DashedVMobject(boxes[4].copy().set_stroke(NO), num_dashes=16)
        boxes.remove(boxes[4])
        pw = VGroup(*[MathTex(t, font_size=26, color=GREY_B).next_to(boxes[i], DOWN, buff=0.12) for i, t in
                      enumerate(("1", "x", "x^2", "x^3"))])
        pw4 = MathTex("x^4", font_size=26, color=NO).next_to(ghost, DOWN, buff=0.12)

        def bits_mob(v):
            return VGroup(*[MathTex(str(b), font_size=32, color=DATA if b else GREY_B).move_to(boxes[i]) for i, b in
                            enumerate(v)])

        state = [0, 0, 0, 1]
        bm = bits_mob(state)
        sl = MathTex(r"x^3", font_size=32, color=CODE).next_to(boxes, LEFT, buff=0.5)
        red = MathTex(r"x^4 \equiv x^3 + 1", font_size=30, color=NO).next_to(ghost, RIGHT, buff=0.35)
        with self.voiceover(
            "The explanation is algebra over the field with two elements, where one plus one is zero and adding "
            "is exclusive-or. <bookmark mark='a'/> Read the register's bits as the coefficients of a polynomial; "
            "this is cleanest for the same taps wired in the so-called Galois form, which folds the exclusive-or "
            "into the shift. <bookmark mark='b'/> One clock step multiplies that polynomial by x, shifting every "
            "coefficient up, and the feedback reduces the result modulo the tap polynomial, exactly as an integer "
            "is reduced modulo a number. This quotient is a field when the polynomial is irreducible; reducible "
            "polynomials need not give a field. <bookmark mark='c'/> So the states the register visits are the "
            "powers of x, and its period is the smallest power of x that comes back to one; either wiring has the "
            "same period. <bookmark mark='d'/> The period is the maximum, two to the n minus one, exactly when "
            "the polynomial is primitive: when the powers of x run through every non-zero element of the finite "
            "field with two to the n elements. Solomon Golomb worked out this theory in the 1950s, and these "
            "registers have generated codes, ciphers and test patterns ever since."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("a")
            self.play(Indicate(lines[1], scale_factor=1.03))
            self.play(FadeIn(boxes), FadeIn(pw), FadeIn(bm), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(lines[2]), Create(ghost), FadeIn(pw4))
            moved = VGroup(*[bm[i].copy() for i in range(4)])
            self.play(*[m.animate.move_to(boxes[i + 1] if i < 3 else ghost) for i, m in enumerate(moved)],
                      FadeOut(bm), run_time=1.0)
            zero = MathTex("0", font_size=32, color=GREY_B).move_to(boxes[0])
            self.play(FadeIn(zero), Write(red))
            over = moved[3]
            c0, c3 = over.copy(), over.copy()
            self.play(c0.animate.move_to(boxes[0]).set_color(NO), c3.animate.move_to(boxes[3]).set_color(NO),
                      FadeOut(over), run_time=1.0)
            new = bits_mob([1, 0, 0, 1])
            sl2 = MathTex(r"x^4 = x^3 + 1", font_size=32, color=CODE).next_to(boxes, LEFT, buff=0.5)
            self.play(FadeOut(VGroup(zero, c0, c3, *moved[:3])), FadeIn(new), Transform(sl, sl2))
            vo.wait_until("c")
            self.play(FadeIn(tail[0]))
            # keep stepping: the register runs through the powers of x
            cur = [1, 0, 0, 1]
            for k in range(5, 8):
                top = cur[3]
                cur = [top, cur[0], cur[1], cur[2] ^ top]
                terms = [t for t, b in zip(("1", "x", "x^2", "x^3"), cur) if b][::-1]
                lab = MathTex(rf"x^{k} = " + " + ".join(terms), font_size=32, color=CODE).next_to(boxes, LEFT, buff=0.5)
                self.play(Transform(new, bits_mob(cur)), Transform(sl, lab), run_time=0.6)
                self.wait(0.4)
            vo.wait_until("d")
            self.play(FadeIn(tail[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("lfsr")
        head = label(r"Monic $p(x)$, degree 2--8, constant term 1", font_size=36).to_edge(UP, buff=0.35)
        hdr = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"degree $n$", r"polynomials", r"maximal (period "
                                                                       r"$2^n - 1$)", r"$\varphi(2^n - 1)/n$")])
        rows = VGroup(hdr)
        for r in d["rows"]:
            rows.add(VGroup(MathTex(str(r["n"]), font_size=28, color=GREY_A),
                            MathTex(str(r["polys"]), font_size=28, color=GREY_A),
                            MathTex(str(r["maximal"]), font_size=28, color=YES),
                            MathTex(str(r["expected"]), font_size=28, color=HEAD)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-3.8 + [0, 2.4, 5.0, 7.6][j], 2.2 - 0.5 * i, 0])
        uses = VGroup(
            label(r"CRC checksums: \ dividing by a polynomial over $\mathrm{GF}(2)$ \ (Part 28)", font_size=24,
                  color=GREY_A),
            label(r"stream ciphers, \ and why linearity makes them breakable \ (Part 29)", font_size=24, color=GREY_A),
            label(r"scramblers on every serial link; \ GPS codes; \ built-in self-test of chips", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here are all monic feedback polynomials of degrees two through eight with constant coefficient one, "
            "so the shift is invertible, each simulated from a nonzero seed until it repeats. <bookmark "
            "mark='a'/> At degree eight there are a hundred and twenty-eight of them, and sixteen give the "
            "maximal period of two hundred and fifty-five. In every row the count matches the formula from field "
            "theory: Euler's phi of two to the n minus one, divided by n. <bookmark mark='b'/> These little "
            "machines are everywhere. The checksums that catch errors on disks and networks divide by such "
            "polynomials, in Part 28. Stream ciphers were built from them, and Part 29 shows why their linearity "
            "makes them easy to break. Serial links scramble their bits with them, GPS satellites are told apart "
            "by them, and chips test themselves with them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(rows[1:]))
            vo.wait_until("a")
            self.play(Indicate(rows[1:], scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
