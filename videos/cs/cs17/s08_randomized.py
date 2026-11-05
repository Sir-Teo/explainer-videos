from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Randomized(VoiceoverScene):
    def construct(self):
        self.card()
        self.treap()
        self.skiplist()
        self.measured()

    def card(self):
        card = chapter_card(7, r"Treaps and skip lists", r"Can coin flips replace rebalancing rules?", lit=(1989,),
                            extra=((1989, r"Seidel and Aragon: \ treaps"), (1990, r"Pugh: \ skip lists")), part=PART)
        with self.voiceover("Chapter seven. Treaps and skip lists."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def treap(self):
        head = label(r"A treap: \ a tree on keys, \ a heap on priorities", font_size=34).to_edge(UP, buff=0.3)
        items = [("D", 91), ("B", 77), ("F", 83), ("A", 12), ("C", 40), ("E", 65), ("G", 30)]
        pos = {"D": [0, 1.4], "B": [-2.4, 0.3], "F": [2.4, 0.3], "A": [-3.5, -0.8], "C": [-1.3, -0.8],
               "E": [1.3, -0.8], "G": [3.5, -0.8]}
        nodes = {}
        for k, p in items:
            c = Circle(radius=0.36, stroke_color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1)
            t = VGroup(mono(k, 22, WHITE), mono(str(p), 14, HEAD)).arrange(DOWN, buff=0.02)
            nodes[k] = VGroup(c, t.move_to(c)).move_to([pos[k][0], pos[k][1] - 0.2, 0])
        edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.36, color=GREY_B,
                              stroke_width=1.6) for a, b in (("D", "B"), ("D", "F"), ("B", "A"), ("B", "C"),
                                                             ("F", "E"), ("F", "G"))])
        pts = VGroup(
            label(r"each key gets a \textbf{random priority} when it is inserted", font_size=22, color=HEAD),
            label(r"keys in search-tree order, \ priorities in heap order: \ the shape is then unique", font_size=22,
                  color=GREY_A),
            label(r"it is the BST you would get by inserting in order of priority: \ a \textbf{random} BST, \ always",
                  font_size=22, color=YES),
            label(r"insert: \ add as a leaf, \ rotate up while its priority beats its parent's", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Chapter five showed that a search tree built in random order is shallow. Raimund Seidel and Cecilia "
            "Aragon found a way to get random order whatever order the keys really arrive in. <bookmark "
            "mark='a'/> Give each key a random priority when it is inserted. <bookmark mark='b'/> Keep the keys in "
            "search-tree order and the priorities in heap order, every parent's priority above its children's. "
            "Those two rules fix the shape completely. <bookmark mark='c'/> And that shape is exactly the tree you "
            "would get by inserting the keys in order of priority, which is a random order. So a treap is always a "
            "random binary search tree, with expected depth two natural log n, even for sorted input. <bookmark "
            "mark='d'/> To insert, add the key as a leaf and rotate it up while its priority beats its parent's."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(n) for n in nodes.values()])
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def skiplist(self):
        head = label(r"A skip list \ (Pugh, \ 1990)", font_size=34).to_edge(UP, buff=0.3)
        keys = [3, 7, 12, 19, 25, 31, 38, 44, 50, 57]
        rng = random.Random(3)
        lv = [1 + (rng.random() < 0.5) + (rng.random() < 0.25) + (rng.random() < 0.125) for _ in keys]
        lv[3], lv[7] = 4, 3
        W, H = 1.05, 0.55
        x0 = -5.6
        cols = VGroup()
        tops = {}
        for i, (k, L) in enumerate(zip(keys, lv)):
            col = VGroup()
            for j in range(L):
                r = Rectangle(width=0.7, height=0.42, stroke_color=DATA if j == 0 else LAM, stroke_width=1.6,
                              fill_color=BG, fill_opacity=1).move_to([x0 + (i + 1) * W, -1.6 + j * H, 0])
                col.add(r)
            col.add(mono(str(k), 18, WHITE).move_to(col[0]))
            cols.add(col)
            tops[i] = L
        headcol = VGroup(*[Rectangle(width=0.7, height=0.42, stroke_color=GREY_B, stroke_width=1.6).move_to(
            [x0, -1.6 + j * H, 0]) for j in range(4)])
        links = VGroup()
        for j in range(4):
            prev = x0
            for i in range(len(keys)):
                if lv[i] > j:
                    x = x0 + (i + 1) * W
                    links.add(Arrow([prev + 0.35, -1.6 + j * H, 0], [x - 0.35, -1.6 + j * H, 0], buff=0.02,
                                    stroke_width=1.6, color=GREY_B, max_tip_length_to_length_ratio=0.15))
                    prev = x
        pts = VGroup(
            label(r"a sorted linked list, \ plus express lanes: \ each node joins the next level with probability "
                  r"$\tfrac12$", font_size=21, color=GREY_A),
            label(r"search: \ run along the top lane, \ drop down when the next key is too big", font_size=21,
                  color=GREY_A),
            label(r"expected $\sim 2 \lg n$ steps, \ 2 pointers per key; \ no rotations, \ easy to make "
                  r"concurrent \ (Java's \texttt{ConcurrentSkipListMap})", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "William Pugh's skip list gets the same expected behaviour without a tree at all. <bookmark mark='a'/> "
            "Start with a sorted linked list. Flip a coin for each node: heads, it also joins a second, sparser "
            "list above. Flip again for a third level, and so on. About half the nodes are on level two, a quarter "
            "on level three. <bookmark mark='b'/> To search, run along the top level until the next key would "
            "overshoot, drop a level, and repeat. Each level skips about half of what is left. <bookmark "
            "mark='c'/> The expected search is about two log n steps, and each key costs two pointers on average. "
            "There are no rotations, and that locality makes skip lists easy to update concurrently, which is "
            "why Java's concurrent sorted map is one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(headcol), FadeIn(cols[:]), Create(links), run_time=2)
            for mk, p in zip("abc", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("randomized")
        head = label(r"Measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[words(r["n"]), f"{r['treap_depth']:.1f}", f"{r['bst_theory']:.1f}", str(r["treap_height"]),
                 f"{r['skip_search']:.1f}", f"{r['skip_theory']:.1f}", f"{r['skip_pointers']:.2f}"] for r in d["rows"]]
        tab = grid_table([r"$n$", r"treap depth", r"random BST", r"treap height", r"skip-list search",
                          r"$2 \lg n$", r"pointers per key"], rows, widths=[1.6, 1.9, 1.9, 1.9, 2.3, 1.4, 2.3],
                         row_h=0.5, font_size=19).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"the treap was fed the keys \textbf{in sorted order}: \ the random priorities undo it", font_size=22,
                  color=YES),
            label(r"randomness inside the structure, \ not in the input: \ no adversary can choose a bad case",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.55)
        with self.voiceover(
            "Measured, both behave as promised. <bookmark mark='a'/> The treaps were built from keys in sorted "
            "order, the worst case for a plain tree, yet their average depth matches a random tree's. The skip "
            "lists search in about two log n steps with two pointers per key. <bookmark mark='b'/> This is the same "
            "lesson as quicksort's random pivot: when the randomness is inside the algorithm, no input can be "
            "bad; there are only unlucky coin flips, and they are rare."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()
