from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, load, mono,
                                  size_label)


class Oblivious(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.transpose()
        self.veb()

    def card(self):
        card = chapter_card(9, r"Cache-oblivious algorithms", r"Can code be fast for every cache at once?", lit=(1999,),
                            extra=((1999, r"Frigo, \ Leiserson, \ Prokop, \ Ramachandran"),), part=PART)
        with self.voiceover("Chapter nine. Cache-oblivious algorithms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"The ideal-cache model \ (1999)", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"one cache of $M$ words, \ lines of $B$ words, \ fully associative, \ optimal replacement",
                  font_size=25, color=GREY_A),
            label(r"cost of an algorithm: \ the number of lines moved, \ $Q(n; M, B)$", font_size=25, color=DATA),
            label(r"\textit{cache-oblivious}: \ the algorithm never mentions $M$ or $B$", font_size=26, color=HEAD),
            label(r"if it is optimal for every $M$ and $B$, \ it is optimal at every level of a real hierarchy at once",
                  font_size=25, color=YES),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Tiling has a flaw: the tile size is tuned to one cache, and a real machine has three. In 1999 Matteo "
            "Frigo, Charles Leiserson, Harald Prokop and Sridhar Ramachandran proposed a way round it. <bookmark "
            "mark='a'/> Model the memory as one cache of M words, moved in lines of B words, with perfect "
            "replacement. <bookmark mark='b'/> Measure an algorithm by how many lines it moves. <bookmark mark='c'/> "
            "And now the twist: write the algorithm without ever mentioning M or B. <bookmark mark='d'/> If it moves "
            "the fewest possible lines for every value of M and B, then it is simultaneously optimal for L1, for L2, "
            "for L3 and for the disk, without being told any of their sizes. The usual trick is to divide and "
            "conquer: halve the problem until it is tiny, and at some depth of the recursion, whatever the cache, the "
            "pieces fit."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def transpose(self):
        d = load("oblivious")
        head = label(rf"Transposing a {d['n']} $\times$ {d['n']} matrix: \ lines moved per element", font_size=32).to_edge(
            UP, buff=0.3)
        caps = d["caps_kb"]
        ax = Axes(x_range=[0, len(caps) - 1, 1], y_range=[0, 0.6, 0.1], x_length=8.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 1.0 + DOWN * 0.3)
        ax.y_axis.add_numbers([0, 0.2, 0.4, 0.6], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(size_label(k * 1024), font_size=16, color=GREY_B).next_to(ax.c2p(i, 0), DOWN, buff=0.12)
                      for i, k in enumerate(caps)])
        xl = note(r"cache size \ (fully associative, \ 64-byte lines)", font_size=18).next_to(xt, DOWN, buff=0.1)
        ideal = DashedLine(ax.c2p(0, 0.125), ax.c2p(len(caps) - 1, 0.125), color=GREY_B)
        il = label(r"one line per 8 elements: \ the best possible", font_size=18, color=GREY_B).next_to(
            ax.c2p(len(caps) - 1, 0.125), DOWN, buff=0.1).shift(LEFT * 1.0)
        curves = VGroup()
        labs = VGroup()
        for key, col, nm in (("naive", NO, r"row by row"), ("blocked", DATA, r"blocked, \ tuned for 16 KB"),
                             ("recursive", YES, r"recursive \ (oblivious)")):
            c = VMobject(color=col, stroke_width=5 if key == "recursive" else 3).set_points_as_corners(
                [ax.c2p(i, v) for i, v in enumerate(d["rows"][key])])
            curves.add(c)
        labs = VGroup(label(r"row by row", font_size=20, color=NO), label(r"blocked, \ tuned for 16 KB", font_size=20,
                                                                         color=DATA),
                      label(r"recursive \ (oblivious)", font_size=20, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        with self.voiceover(
            "Here is the simplest example: transposing a matrix, reading A by rows and writing B by columns. "
            "<bookmark mark='a'/> Done row by row, every write to B lands in a different line, and until the cache "
            "can hold a whole column's worth of lines, more than half the accesses miss. <bookmark mark='b'/> Blocked "
            "into tiles tuned for a sixteen-kilobyte cache, it reaches the best possible, one line moved for every "
            "eight elements, but only on caches at least that big: below four kilobytes it is as bad as the naive "
            "loop. <bookmark mark='c'/> The recursive version splits the matrix in half, and in half again, never "
            "mentioning any size. It is optimal on every cache in the picture, from one kilobyte up."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), Create(ideal), FadeIn(il))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def veb(self):
        head = label(r"The same idea for search trees: \ the van Emde Boas layout", font_size=32).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"store the top half of the tree's levels together, \ then each bottom subtree together, \ "
                  r"recursively", font_size=24, color=DATA),
            label(r"a search crosses $O(\log_B n)$ lines, \ for every $B$ at once \ (Prokop, \ 1999)", font_size=24,
                  color=YES),
            label(r"the cache-aware alternative, \ with $B$ built in: \ the B-tree \ (chapter 11)", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "The same trick works for search trees. <bookmark mark='a'/> Lay out a binary tree not level by level but "
            "recursively: the top half of its levels as one small tree, stored together, then each of the subtrees "
            "hanging below it, each stored together, laid out the same way inside. <bookmark mark='b'/> Then a search "
            "from root to leaf crosses only about log base B of n cache lines, for every line size B at once. "
            "<bookmark mark='c'/> The design that builds B in, instead, is the B-tree, two chapters on."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
