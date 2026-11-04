from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load)


class External(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.merge()
        self.btree()

    def card(self):
        card = chapter_card(11, r"External memory and B-trees", r"What if the data is on a disk?", lit=(1972, 1988),
                            extra=((1972, r"Bayer and McCreight: \ B-trees"), (1988, r"Aggarwal and Vitter")), part=PART)
        with self.voiceover("Chapter eleven. External memory and B-trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"The external-memory model \ (Aggarwal and Vitter, \ 1988)", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"a memory of $M$ items; \ a disk read or written in blocks of $B$; \ cost = block transfers",
                  font_size=24, color=GREY_A),
            label(r"scanning $N$ items: \ $N/B$ \qquad searching: \ $\log_B N$", font_size=26, color=DATA),
        ).arrange(DOWN, buff=0.3).move_to(UP * 1.4)
        sort = MathTex(r"\text{sorting: }\ \Theta\!\left(\frac{N}{B} \log_{M/B} \frac{N}{B}\right)", font_size=44,
                       color=HEAD).move_to(DOWN * 0.2)
        ex = VGroup(
            label(r"$N = 10^{10}$ records, \ $B = 10^5$ per block, \ $M = 10^9$ in memory", font_size=24,
                  color=GREY_B),
            label(r"$\log_{M/B}(N/B) = \log_{10^4} 10^5 = 1.25$: \ about two passes over the data, \ not 33",
                  font_size=24, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Take the hierarchy one step further, to a disk, where a single access costs milliseconds and data moves in "
            "big blocks. <bookmark mark='a'/> In 1988 Alok Aggarwal and Jeffrey Vitter made this a model: a memory "
            "holding M items, a disk read and written in blocks of B items, and the cost of an algorithm is the number "
            "of blocks it moves. Scanning N items costs N over B. <bookmark mark='b'/> And they proved the cost of "
            "sorting, matching upper and lower bounds: N over B, times the logarithm of N over B, to the base M over "
            "B. <bookmark mark='c'/> That base is enormous. Sorting ten billion records with a gigabyte of memory and "
            "hundred-thousand-record blocks takes about two passes over the data, not the thirty-three that a binary "
            "merge sort would. Every large database sort works this way."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(items))
            vo.wait_until("b")
            self.play(Write(sort))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    def merge(self):
        head = label(r"External merge sort: \ two kinds of pass", font_size=34).to_edge(UP, buff=0.35)
        n_runs = 8
        blocks = VGroup(*[Rectangle(width=1.3, height=0.5, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n_runs)])
        blocks.arrange(RIGHT, buff=0.15).move_to(UP * 1.3)
        lab0 = label(r"the input: \ $N$ items on disk", font_size=20, color=GREY_B).next_to(blocks, UP, buff=0.15)
        runs = VGroup(*[b.copy().set_fill(DATA, opacity=0.4).set_stroke(DATA) for b in blocks])
        rl = label(r"pass 1: \ read $M$ items, \ sort them in memory, \ write a sorted run: \ $N/M$ runs", font_size=22,
                   color=DATA).next_to(blocks, DOWN, buff=0.3)
        merged = Rectangle(width=blocks.width, height=0.5, stroke_color=YES, stroke_width=2, fill_color=YES,
                           fill_opacity=0.35).move_to(DOWN * 1.2)
        arrows = VGroup(*[Arrow(r.get_bottom(), merged.get_top(), buff=0.1, color=GREY_C, stroke_width=2) for r in runs])
        ml = label(r"pass 2: \ merge up to $M/B$ runs at once, \ one block of each in memory", font_size=22,
                   color=YES).next_to(merged, DOWN, buff=0.3)
        tot = label(r"passes $= 1 + \lceil \log_{M/B} (N/M) \rceil$: \ each reads and writes everything once",
                    font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The algorithm that meets the sorting bound is external merge sort. <bookmark mark='a'/> First pass: read "
            "as much as fits in memory, M items, sort it there, and write it back as a sorted run. That makes N over "
            "M runs. <bookmark mark='b'/> Then merge: keep one block of each run in memory and repeatedly output the "
            "smallest front item. With M over B blocks of room, M over B runs can be merged at once. <bookmark "
            "mark='c'/> So the number of passes is one plus the logarithm, to the base M over B, of the number of "
            "runs, and each pass reads and writes everything once. With a large memory that is usually two passes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks), FadeIn(lab0))
            vo.wait_until("a")
            self.play(LaggedStart(*[Transform(b, r) for b, r in zip(blocks, runs)], lag_ratio=0.15), FadeIn(rl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), FadeIn(merged), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    def btree(self):
        head = label(r"The B-tree: \ a node is a block", font_size=36).to_edge(UP, buff=0.35)
        root = box(4.2, 0.6, r"\text{keys} \ 1 \ \dots \ B", HEAD, 20).move_to(UP * 1.6)
        kids = VGroup(*[box(2.0, 0.5, r"\dots", DATA, 18) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
        dots = label(r"$\cdots$", font_size=30, color=GREY_B).next_to(kids, RIGHT, buff=0.2)
        edges = VGroup(*[Line(root.get_bottom(), k.get_top(), color=GREY_D, stroke_width=2) for k in kids])
        facts = VGroup(
            label(r"$B$ around 100 to 1000 keys per node: \ a billion keys in 3 or 4 levels", font_size=25,
                  color=YES),
            label(r"Bayer and McCreight, \ 1972: \ every database and file system index since", font_size=25,
                  color=HIST),
            label(r"Parts 17 and 35 build them", font_size=25, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For searching, the answer is the B-tree, invented by Rudolf Bayer and Edward McCreight in 1972. <bookmark "
            "mark='a'/> Make each node of a search tree exactly one block, holding not one key but hundreds, with a "
            "child between each pair. <bookmark mark='b'/> With a few hundred keys per node, a billion keys need only "
            "three or four levels, so a lookup costs three or four block reads, and the top levels stay in memory "
            "anyway. Every relational database index and nearly every file system uses a B-tree or a relative. "
            "Parts 17 and 35 build them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(root), Create(edges), FadeIn(kids), FadeIn(dots))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
