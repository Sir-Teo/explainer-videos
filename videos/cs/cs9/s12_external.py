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
        with self.voiceover(
            "Chapter eleven. External memory and B-trees."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"The external-memory model \ (Aggarwal and Vitter, \ 1988)", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"a memory of $M$ items; \ a disk read or written in blocks of $B$; \ cost = block transfers",
                  font_size=24, color=GREY_A),
            label(r"scanning: \ $\Theta(1+N/B)$; \ balanced search: \ $O(1+\log_B N)$", font_size=25, color=DATA),
            label(r"$N\ge1$, $M\ge2B$; \ comparison-based, indivisible items", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 1.4)
        sort = MathTex(r"\text{comparison sort: }\ \Theta\!\left(\left(1+\frac{N}{B}\right)\max\!\left\{1,\log_{M/B}\frac{N}{B}\right\}\right)", font_size=34,
                       color=HEAD).move_to(DOWN * 0.2)
        ex = VGroup(
            label(r"$N = 10^{10}$ records, \ $B = 10^5$ per block, \ $M = 10^9$ in memory", font_size=24,
                  color=GREY_B),
            label(r"$M$ counts items; \ 10 initial runs, \ one merge round: \ two read/write passes",
                  font_size=24, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The external-memory model counts block transfers between a limited fast memory and a larger slow store. "
            "It can describe more than a physical spinning disk. <bookmark mark='a'/> Memory holds M items and a "
            "transfer moves B items. Scanning requires order one plus N over B transfers, with ceilings for short "
            "inputs. <bookmark mark='b'/> The comparison-based, indivisible-record sorting bound includes a scan "
            "term and a logarithm with base M over B, under the usual memory-size assumptions. This is not a lower "
            "bound for every possible integer-sorting model. <bookmark mark='c'/> In this example M is one billion "
            "items, not one gigabyte. Ten initial runs fit into one merge round: two passes, each reading and "
            "writing the data, rather than two individual transfers per block."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(items))
            vo.wait_until("a")
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
        arrows = VGroup(*[Arrow(r.get_bottom(), merged.get_top() + RIGHT * (r.get_x() - merged.get_x()),
                               buff=0.1, color=GREY_C, stroke_width=1.5, tip_length=0.10) for r in runs])
        ml = label(r"merge fan-in $f \le \lfloor M/B\rfloor-1$: \ input blocks + output buffer", font_size=22,
                   color=YES).next_to(merged, DOWN, buff=0.3)
        tot = label(r"$R\ge1$, $f\ge2$: \ passes $=1+\lceil\log_f R\rceil$; \ read + write each pass",
                    font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "External merge sort separates run generation from merging. <bookmark mark='a'/> Read an in-memory "
            "batch, sort it and write a run. Ceilings and workspace determine the actual number of initial runs. "
            "<bookmark mark='b'/> During merging, reserve input blocks and an output buffer. A simple fan-in is "
            "floor M over B minus one, with more room potentially needed for metadata and computation. Refill an "
            "input block when consumed and flush output blocks when full. <bookmark mark='c'/> Count one "
            "run-generation pass plus enough merge rounds for the number of runs and chosen fan-in. Each complete "
            "pass reads and writes the data. Whether two passes suffice depends on these quantities, not simply on "
            "memory being large in absolute terms."
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
            label(r"height depends on fan-out, occupancy and cached upper nodes", font_size=25,
                  color=YES),
            label("Bayer and McCreight, \\ 1972; \\ common among several index families", font_size=25,
                  color=HIST),
            label(r"Parts 17 and 35 build them", font_size=25, color=HEAD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "B-trees organize search around blocks. Bayer and McCreight's work appeared in 1972. <bookmark "
            "mark='a'/> A node groups many ordered keys and child pointers, with a node size chosen for a page or "
            "other useful transfer unit. <bookmark mark='b'/> With maintained occupancy and fan-out on the order of "
            "B, search height is on the order of one plus log base B of N. Cached upper nodes can reduce slow-store "
            "reads, while variable-size records, updates and concurrency add design choices. B-tree relatives are "
            "common in databases and file systems, alongside hash indexes, log-structured merge trees and other "
            "structures. The drawing is a layout illustration, not a guarantee that every billion-key index has "
            "exactly three or four physical reads."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(root), Create(edges), FadeIn(kids), FadeIn(dots))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
