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
        with self.voiceover(
            "Chapter nine. Cache-oblivious algorithms."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"The ideal-cache model \ (1999)", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"one cache of $M$ words, \ lines of $B$ words, \ fully associative, \ optimal replacement",
                  font_size=25, color=GREY_A),
            label(r"cost of an algorithm: \ the number of lines moved, \ $Q(n; M, B)$", font_size=25, color=DATA),
            label(r"\textit{cache-oblivious}: \ the algorithm never mentions $M$ or $B$", font_size=26, color=HEAD),
            label("model guarantees need algorithm, tall-cache and multilevel assumptions",
                  font_size=25, color=YES),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Cache-oblivious algorithms avoid explicit cache parameters in their code. <bookmark mark='a'/> The "
            "ideal-cache model specifies a fully associative fast memory of M words, B-word transfers and optimal "
            "replacement. <bookmark mark='b'/> Analysis counts transfers under that model and stated initial/output "
            "conditions. <bookmark mark='c'/> A recursive algorithm can discover useful subproblem sizes without "
            "testing M or B directly. Avoiding the parameters alone does not prove optimality. <bookmark mark='d'/> "
            "Bounds for specific algorithms may require a tall-cache assumption and regularity conditions. They can "
            "extend across suitably modeled memory levels, and LRU can have related guarantees with appropriate "
            "resource comparisons. None of this promises the exact fewest misses at every real cache level, where "
            "mapping, prefetching and instruction overhead matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    def transpose(self):
        d = load("oblivious")
        head = label(rf"Transpose {d['n']} $\times$ {d['n']}: \ line fills per data reference", font_size=32).to_edge(
            UP, buff=0.3)
        caps = d["caps_kb"]
        ax = Axes(x_range=[0, len(caps) - 1, 1], y_range=[0, 0.6, 0.1], x_length=8.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 1.0 + DOWN * 0.3)
        ax.y_axis.add_numbers([0, 0.2, 0.4, 0.6], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(size_label(k * 1024), font_size=16, color=GREY_B).next_to(ax.c2p(i, 0), DOWN, buff=0.12)
                      for i, k in enumerate(caps)])
        xl = note(r"FA-LRU capacity, \ 64-byte lines; \ write-back traffic excluded", font_size=16).next_to(xt, DOWN, buff=0.1)
        ideal = DashedLine(ax.c2p(0, 0.125), ax.c2p(len(caps) - 1, 0.125), color=GREY_B)
        il = label("cold fill floor: \\ one miss per 8 data references", font_size=18, color=GREY_B).next_to(
            ax.c2p(len(caps) - 1, 0.125), DOWN, buff=0.1).shift(LEFT * 1.0)
        curves = VGroup()
        labs = VGroup()
        for key, col, nm in (("naive", NO, r"row by row"), ("blocked", DATA, r"blocked, \ tuned for 16 KiB"),
                             ("recursive", YES, r"recursive \ (oblivious)")):
            c = VMobject(color=col, stroke_width=5 if key == "recursive" else 3).set_points_as_corners(
                [ax.c2p(i, v) for i, v in enumerate(d["rows"][key])])
            curves.add(c)
        labs = VGroup(label(r"row by row", font_size=20, color=NO), label(r"blocked, \ tuned for 16 KiB", font_size=20,
                                                                         color=DATA),
                      label(r"recursive \ (oblivious)", font_size=20, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        with self.voiceover(
            "The experiment transposes a row-major matrix and simulates a cold fully associative LRU cache. Each "
            "output element contributes two address references, one to the input and one to the output. The vertical "
            "axis is allocation misses per reference; it excludes dirty write-backs. <bookmark mark='a'/> The "
            "row-by-row traversal has poor output locality at small capacities. <bookmark mark='b'/> A fixed "
            "thirty-two-by-thirty-two block changes the curve, reaching the cold line-fill floor from four kibibytes "
            "in this experiment. <bookmark mark='c'/> The recursive traversal reaches that floor across all "
            "displayed capacities. One eighth here means one fill per eight references, or one quarter of a fill per "
            "output element. This LRU experiment illustrates locality; it does not establish exact transfer "
            "optimality for every size and cache."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), Create(ideal), FadeIn(il))
            for mk, k in zip("abc", range(3)):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.5)
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    def veb(self):
        head = label(r"The same idea for search trees: \ the van Emde Boas layout", font_size=32).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"store the top half of the tree's levels together, \ then each bottom subtree together, \ "
                  r"recursively", font_size=21, color=DATA).move_to(UP * 2.65),
            label("balanced static tree: \\ $O(1 + \\log_B n)$ block transfers under stated assumptions", font_size=22,
                  color=YES).move_to(DOWN * 2.7),
            label(r"the cache-aware alternative, \ with $B$ built in: \ the B-tree \ (chapter 11)", font_size=21,
                  color=HEAD).move_to(DOWN * 3.2),
        )
        # Node identities stay fixed between the logical tree and physical order.
        positions = [(0, 1.7), (-2.8, .9), (2.8, .9)]
        positions += [(x, -.1) for x in (-4.2, -1.4, 1.4, 4.2)]
        positions += [(x, -.9) for x in (-4.9, -3.5, -2.1, -.7, .7, 2.1, 3.5, 4.9)]
        clusters = [(0, 1, 2), (3, 7, 8), (4, 9, 10), (5, 11, 12), (6, 13, 14)]
        colors = (DATA, YES, HEAD, FUNC, INF)
        color_of = {node: col for group, col in zip(clusters, colors) for node in group}
        nodes = VGroup(*[VGroup(Circle(radius=.19, color=color_of[i], fill_color=BG, fill_opacity=1),
                               label(str(i), font_size=17, color=color_of[i])).move_to(RIGHT*x + UP*y)
                         for i, (x, y) in enumerate(positions)])
        edges = VGroup(*[Line(nodes[(i-1)//2].get_center(), nodes[i].get_center(),
                             buff=.2, color=GREY_C, stroke_width=1.5) for i in range(1, 15)])
        regions = VGroup(*[SurroundingRectangle(VGroup(*[nodes[i] for i in group]), buff=.14,
                            color=col, stroke_width=1.5, fill_color=col, fill_opacity=.05)
                          for group, col in zip(clusters, colors)])
        order = [i for group in clusters for i in group]
        memory = VGroup(*[VGroup(Rectangle(width=.57, height=.42, color=color_of[i], stroke_width=1.5,
                                            fill_color=color_of[i], fill_opacity=.12),
                                  label(str(i), font_size=17, color=color_of[i])) for i in order])
        memory.arrange(RIGHT, buff=.04).move_to(DOWN * 1.85)
        assert len(order) == len(set(order)) == 15
        with self.voiceover(
            "A static search layout can use recursive clustering too. <bookmark mark='a'/> For a balanced binary "
            "tree, the van Emde Boas layout stores a recursively arranged top tree, followed by recursively arranged "
            "lower subtrees. <bookmark mark='b'/> Under the usual block-transfer assumptions, a root-to-leaf search "
            "uses order one plus log base B of n block transfers. The extra one handles even a tree that fits in a "
            "block. This is a layout bound, not a claim about arbitrary unbalanced trees, dynamic updates or "
            "physical search latency. <bookmark mark='c'/> A B-tree instead chooses node capacity with the block "
            "size in mind. Both approaches organize related search steps to reduce data movement, under their "
            "respective models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items[0]))
            self.play(FadeIn(regions), Create(edges), FadeIn(nodes), FadeIn(memory))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(items[1]))
            vo.wait_until("c")
            self.play(FadeIn(items[2]))
        self.wait(0.3)
        self.clear_scene()
