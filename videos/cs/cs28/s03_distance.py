from __future__ import annotations

import itertools

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, bit_row, fit_right, grid_table, mono)


def cube_points(center, s=1.6):
    """Oblique projection of the 3-cube: bit 0 -> x, bit 1 -> y, bit 2 -> depth."""
    pts = {}
    for v in range(8):
        x, y, z = v & 1, (v >> 1) & 1, (v >> 2) & 1
        pts[v] = np.array(center) + np.array([s * x + 0.75 * s * z, s * y + 0.45 * s * z, 0])
    return pts


def tesseract_points(center, s=1.3):
    pts = {}
    for v in range(16):
        a, b, c, d = v & 1, (v >> 1) & 1, (v >> 2) & 1, (v >> 3) & 1
        inner = 0.45 if d else 1.0
        x = (a - 0.5) * inner * 2 * s + 0.55 * s * (c - 0.5) * inner
        y = (b - 0.5) * inner * 2 * s + 0.35 * s * (c - 0.5) * inner
        pts[v] = np.array(center) + np.array([x, y, 0])
    return pts


class Distance(VoiceoverScene):
    def construct(self):
        self.card()
        self.metric()
        self.cube()
        self.rule()

    def card(self):
        card = chapter_card(2, r"Hamming distance", r"What makes a set of words a good code?", lit=(1950, 1950),
                            extra=((1950, r"Hamming: \ distance, \ spheres"),), part=PART)
        with self.voiceover("Chapter two. Hamming distance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def metric(self):
        head = label(r"Counting the differences", font_size=34).to_edge(UP, buff=0.35)
        a = [1, 0, 1, 1, 1, 0, 1]
        b = [1, 0, 0, 1, 0, 0, 1]
        ra = bit_row(a, size=0.55, font=26).next_to(head, DOWN, buff=0.8)
        rb = bit_row(b, size=0.55, font=26).next_to(ra, DOWN, buff=0.25)
        marks = VGroup(*[SurroundingRectangle(VGroup(ra.boxes[i], rb.boxes[i]), color=NO, buff=0.05)
                         for i in range(7) if a[i] != b[i]])
        dl = label(r"$d(x, y) = 2$", font_size=30, color=NO).next_to(VGroup(ra, rb), RIGHT, buff=0.8)
        lines = VGroup(
            label(r"the \textbf{Hamming distance}: \ the number of positions where two words differ", font_size=23,
                  color=WHITE),
            label(r"a true distance: \ $d(x, z) \le d(x, y) + d(y, z)$", font_size=23, color=GREY_A),
            label(r"on the BSC, \ the likeliest codeword sent is the one \textbf{nearest} what arrived \ (for $p < "
                  r"\tfrac12$)", font_size=23, color=HEAD),
            label(r"so decoding is geometry: \ find the nearest codeword", font_size=23, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(VGroup(ra, rb), DOWN, buff=0.7)
        with self.voiceover(
            "Hamming's first idea was a way to measure how different two words are. <bookmark mark='a'/> The "
            "Hamming distance counts the positions where they differ: these two words differ in two places. "
            "<bookmark mark='b'/> It behaves like a distance: going from x to z never costs more than going through "
            "y. <bookmark mark='c'/> On the binary symmetric channel, every flip makes a received word less likely, "
            "so the codeword most likely to have been sent is the one closest to what arrived. <bookmark mark='d'/> "
            "Decoding becomes geometry: find the nearest codeword."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ra), FadeIn(rb))
            vo.wait_until("a")
            self.play(Create(marks), FadeIn(dl), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def cube(self):
        head = label(r"Codes as points in the Hamming cube", font_size=34).to_edge(UP, buff=0.3)
        P = cube_points([-5.6, -1.6, 0])
        edges = VGroup(*[Line(P[u], P[v], color=GREY_D, stroke_width=2) for u, v in itertools.combinations(range(8), 2)
                         if bin(u ^ v).count("1") == 1])
        code = {0, 7}
        dots, labs = VGroup(), VGroup()
        for v in range(8):
            col = YES if v in code else GREY_B
            dots.add(Dot(P[v], radius=0.13 if v in code else 0.09, color=col))
            labs.add(mono(f"{(v >> 2) & 1}{(v >> 1) & 1}{v & 1}", 17, col).next_to(P[v], DL if v < 4 else UR,
                                                                                    buff=0.08))
        ball0 = VGroup(*[Circle(radius=0.22, color=DATA, stroke_width=3).move_to(P[v]) for v in (1, 2, 4)])
        ball7 = VGroup(*[Circle(radius=0.22, color=HEAD, stroke_width=3).move_to(P[v]) for v in (6, 5, 3)])
        cl = label(r"the 3-cube: \ codewords 000 and 111 \ (repetition, \ $d = 3$)", font_size=19,
                   color=GREY_A).next_to(VGroup(edges, labs), DOWN, buff=0.3)
        T = tesseract_points([3.6, -0.6, 0])
        tedges = VGroup(*[Line(T[u], T[v], color=GREY_D, stroke_width=1.5)
                          for u, v in itertools.combinations(range(16), 2) if bin(u ^ v).count("1") == 1])
        even = [v for v in range(16) if bin(v).count("1") % 2 == 0]
        tdots = VGroup(*[Dot(T[v], radius=0.1 if v in even else 0.06, color=LAM if v in even else GREY_C)
                         for v in range(16)])
        tl = label(r"the 4-cube: \ the 8 even-weight words \ ($d = 2$)", font_size=19,
                   color=GREY_A).next_to(VGroup(tedges, tdots), DOWN, buff=0.3)
        lines = VGroup(
            label(r"each bit is an axis; \ an edge is one flip", font_size=21, color=WHITE),
            label(r"around each codeword, \ a \textbf{ball} of the words one flip away: \ the two balls do not "
                  r"meet", font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=1.0)
        lines2 = label(r"even weight: \ one flip lands on a non-codeword, \ \textbf{detected}; \ but it is equally "
                       r"close to several codewords", font_size=21, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Picture all words of three bits as the corners of a cube. <bookmark mark='a'/> Each bit is an axis, and "
            "each edge is a single flip. The repetition code uses just two corners, zero zero zero and one one one, "
            "three edges apart. <bookmark mark='b'/> Around each codeword draw a ball: the words one flip away. The "
            "two balls do not touch, so any single flip is corrected by moving back to the nearer codeword. "
            "<bookmark mark='c'/> In four dimensions, take the eight words with an even number of ones, every other "
            "corner of the hypercube. Any two are at least two apart. <bookmark mark='d'/> A single flip lands on "
            "an odd word, so it is detected, but that word is equally close to several codewords: the error cannot "
            "be corrected."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(dots), FadeIn(labs), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(ball0), Create(ball7), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(tedges), FadeIn(tdots), FadeIn(tl), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(lines2))
        self.wait(0.3)
        self.clear_scene()

    def rule(self):
        head = label(r"Minimum distance decides everything", font_size=34).to_edge(UP, buff=0.35)
        rows = [["1", "0", "0", r"no code: \ every word is a codeword"],
                ["2", "1", "0", r"a parity bit \ (the even-weight code)"],
                ["3", "2", "1", r"repetition $\times 3$; \ Hamming(7,4)"],
                ["4", "3", "1", r"extended Hamming \ (ECC memory)"],
                ["7", "6", "3", r"the Golay code \ (chapter 4)"],
                [r"$d$", r"$d - 1$", r"$\lfloor (d-1)/2 \rfloor$", r""]]
        tab = grid_table([r"minimum distance $d$", r"errors detected", r"errors corrected", r"example"], rows,
                         widths=[2.8, 2.4, 2.6, 5.0], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[WHITE, DATA, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(r"balls of radius $t$ around codewords stay disjoint exactly when $d \ge 2t + 1$", font_size=22,
                  color=YES),
            label(r"or mix: \ correct $t$ \textbf{and} detect $s > t$ errors when $d \ge t + s + 1$", font_size=22,
                  color=GREY_A),
            label(r"erasures are cheaper: \ $d - 1$ of them can be filled in, \ because their places are known",
                  font_size=22, color=DATA),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The smallest distance between two codewords decides what a code can do. <bookmark mark='a'/> With "
            "distance d, up to d minus one flips can never turn one codeword into another, so they are always "
            "detected. And up to half of d minus one can be corrected, because the balls of that radius around "
            "codewords do not overlap. <bookmark mark='b'/> You can also trade: correct a few errors and still "
            "detect more. <bookmark mark='c'/> Erasures are cheaper than errors. If you know which positions are "
            "missing, any d minus one of them can be filled in, because only one codeword agrees with what is left. "
            "Chapter seven's QR code will use exactly this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
