from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bst_children,
                                   draw_tree, grid_table, load, mono, words)


class Bst(VoiceoverScene):
    def construct(self):
        self.card()
        self.search()
        self.random()
        self.bijection()

    def card(self):
        card = chapter_card(5, r"Binary search trees", r"What if we need the keys in order?", lit=(1960,),
                            extra=((1960, r"Windley, \ Booth and Colin, \ Hibbard"),), part=PART)
        with self.voiceover("Chapter five. Binary search trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def search(self):
        d = load("bst")
        head = label(r"Smaller to the left, \ larger to the right", font_size=34).to_edge(UP, buff=0.3)
        root, ch = bst_children(d["small"])
        tree, nodes, edges = draw_tree(root, ch, dx=7.0, dy=1.0)
        tree.next_to(head, DOWN, buff=0.6)
        path = [50, 30, 40, 45]
        pts = VGroup(
            label(r"find 45: \ compare, \ go left or right, \ one level per step", font_size=22, color=GREY_A),
            label(r"an in-order walk lists the keys sorted: \ range queries, \ predecessor, \ successor", font_size=22,
                  color=YES),
            label(r"cost: \ the depth of the key, \ and the depth depends on the order of insertion", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Hash tables give up order: they cannot list keys alphabetically, or find the next key after a given "
            "one. <bookmark mark='a'/> A binary search tree keeps it. Each node holds a key, with smaller keys in "
            "its left subtree and larger ones in its right. <bookmark mark='b'/> To find a key, start at the root, "
            "compare, and go left or right: one level per comparison. <bookmark mark='c'/> And walking the tree "
            "left, node, right lists every key in sorted order, so the tree also answers range queries and finds "
            "neighbours. <bookmark mark='d'/> The cost of a find is the depth of the key, and the shape of the "
            "tree depends entirely on the order the keys arrived in."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(edges), LaggedStart(*[FadeIn(n) for n in nodes.values()], lag_ratio=0.08), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            for k in path:
                self.play(nodes[k][0].animate.set_stroke(HEAD, width=4), run_time=0.45)
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def random(self):
        d = load("bst")
        head = label(r"Random insertion order", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['depth']:.2f}", f"{r['theory']:.2f}", f"{r['height']:.1f}",
                 f"{r['lg']:.1f}"] for r in d["rows"]]
        tab = grid_table([r"$n$", r"average depth", r"$2(1 + \tfrac1n)H_n - 4$", r"height", r"$\lg n$"], rows,
                         widths=[2.0, 2.4, 3.6, 1.8, 1.6], row_h=0.48, font_size=20).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"the average depth is $2 \ln n + O(1) \approx 1.39 \lg n$: \ only 39\% worse than perfectly "
                  r"balanced", font_size=22, color=YES),
            label(r"the height, \ the worst key, \ is about $4.311 \ln n$ \ (Devroye, \ 1986)", font_size=21,
                  color=GREY_A),
            label(rf"but insert the keys in sorted order: \ a path of height {words(d['sorted_height'])} for 1,000 "
                  r"keys", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "If the keys arrive in random order, the tree is well behaved. <bookmark mark='a'/> We built trees from "
            "a hundred to a hundred thousand random keys and measured the average depth of a node. It matches "
            "the exact formula, two times one plus one over n times the harmonic number, minus four. <bookmark "
            "mark='b'/> That is two natural log n, about one point three nine times log base two n: only "
            "thirty-nine percent deeper than a perfectly balanced tree. <bookmark mark='c'/> The deepest node is "
            "about twice as deep again, as Luc Devroye proved. <bookmark mark='d'/> But insert the same keys in "
            "sorted order, and every key goes to the right of the last: the tree is a path, and every operation "
            "is linear. Real keys often arrive sorted."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def bijection(self):
        d = load("bst")
        head = label(r"The same number as quicksort", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"build a BST from $x_1, x_2, \ldots, x_n$: \ the root $x_1$ is compared with every later key",
                  font_size=22, color=GREY_A),
            label(r"quicksort with the first element as pivot: \ $x_1$ is compared with every other key", font_size=22,
                  color=GREY_A),
            label(r"then both recurse on the smaller keys and on the larger, \ in the same order", font_size=22,
                  color=GREY_A),
            label(r"so the comparisons are the \textbf{same pairs}: \ the tree is quicksort's recursion, \ frozen",
                  font_size=23, color=YES),
            label(rf"checked on 2,000 random keys: \ building the tree, \ {words(d['build_cmp'])} comparisons; \ "
                  rf"quicksort, \ {words(d['quick_cmp'])}", font_size=21, color=HEAD),
            label(r"so Part 16's $2n \ln n$ is the total depth of a random BST, \ and chapter 7's treaps inherit it",
                  font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "That two natural log n should look familiar. <bookmark mark='a'/> When the tree is built, the first "
            "key becomes the root and is compared with every key that comes after it. <bookmark mark='b'/> When "
            "quicksort runs with the first element as pivot, that element is compared with every other key. "
            "<bookmark mark='c'/> Both then split the rest into the smaller and the larger keys and do the same "
            "thing to each part, in the same order. <bookmark mark='d'/> So they compare exactly the same pairs. "
            "A binary search tree is quicksort's recursion, frozen into a data structure. <bookmark mark='e'/> We "
            "checked it on two thousand random keys: the counts are identical. <bookmark mark='f'/> Part 16's two "
            "n natural log n is the total depth of a random tree."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()
