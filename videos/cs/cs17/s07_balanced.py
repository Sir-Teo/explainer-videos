from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_tree, grid_table,
                                   load, mono, tree_layout, words)


def tri(label_, color, w=0.7, h=0.75):
    t = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [0, h / 2, 0], stroke_color=color, stroke_width=1.6,
                fill_color=color, fill_opacity=0.15)
    return VGroup(t, MathTex(label_, font_size=26, color=color).move_to(t.get_center() + DOWN * 0.1))


class Balanced(VoiceoverScene):
    def construct(self):
        self.card()
        self.rotation()
        self.avl()
        self.redblack()
        self.measured()

    def card(self):
        card = chapter_card(6, r"Balanced trees: \ AVL and red--black", r"Can a tree keep itself short?",
                            lit=(1962,), extra=((1962, r"Adelson-Velsky and Landis"),
                                                (1978, r"Guibas and Sedgewick: \ red--black")), part=PART)
        with self.voiceover("Chapter six. Balanced trees: AVL and red–black."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rotation(self):
        head = label(r"A rotation", font_size=34).to_edge(UP, buff=0.3)

        def node(k, col=DATA):
            return VGroup(Circle(radius=0.32, stroke_color=col, stroke_width=2.2, fill_color=BG, fill_opacity=1),
                          mono(k, 24, WHITE))

        def layout(top, mid, a, b, c, left_heavy=True):
            g = VGroup(top, mid, a, b, c)
            top.move_to(UP * 1.2)
            if left_heavy:
                mid.move_to(top.get_center() + DL * 1.1 + LEFT * 0.4)
                a.move_to(mid.get_center() + DL * 1.0 + DOWN * 0.3)
                b.move_to(mid.get_center() + DR * 1.0 + DOWN * 0.3)
                c.move_to(top.get_center() + DR * 1.1 + RIGHT * 0.4 + DOWN * 0.3)
            else:
                mid.move_to(top.get_center() + DR * 1.1 + RIGHT * 0.4)
                a.move_to(top.get_center() + DL * 1.1 + LEFT * 0.4 + DOWN * 0.3)
                b.move_to(mid.get_center() + DL * 1.0 + DOWN * 0.3)
                c.move_to(mid.get_center() + DR * 1.0 + DOWN * 0.3)
            return g
        y, x = node("y"), node("x", LAM)
        A, B, Cc = tri("A", GREY_A), tri("B", HEAD), tri("C", GREY_A)
        left = layout(y, x, A, B, Cc).move_to(LEFT * 3.2 + DOWN * 0.3)
        y2, x2 = node("y"), node("x", LAM)
        A2, B2, C2 = tri("A", GREY_A), tri("B", HEAD), tri("C", GREY_A)
        right = layout(x2, y2, A2, B2, C2, left_heavy=False).move_to(RIGHT * 3.2 + DOWN * 0.3)

        def edges(g, left_heavy=True):
            top, mid, a, b, c = g
            if left_heavy:
                pairs = ((top, mid), (mid, a), (mid, b), (top, c))
            else:
                pairs = ((top, a), (top, mid), (mid, b), (mid, c))
            return VGroup(*[Line(p.get_center(), q.get_top() if isinstance(q[0], Polygon) else q.get_center(),
                                 buff=0.32, color=GREY_B, stroke_width=1.6) for p, q in pairs])
        e1, e2 = edges(left), edges(right, False)
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=HEAD, buff=0).move_to(DOWN * 0.3)
        al = label(r"rotate right at $y$", font_size=20, color=HEAD).next_to(arrow, UP, buff=0.1)
        pts = VGroup(
            label(r"$A < x < B < y < C$ \ before and after: \ still a search tree", font_size=22, color=YES),
            label(r"three pointers change; \ $A$ rises one level, \ $C$ sinks one", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Every balanced tree is built from one operation. <bookmark mark='a'/> Here is a node y whose"
            " left child x has subtrees A and B; y's right subtree is C. <bookmark mark='b'/> A right "
            "rotation makes x the parent and y its right child, and the subtree B changes parents. "
            "<bookmark mark='c'/> The order is preserved: everything in A is less than x, B lies between "
            "x and y, C is greater than y. It is still a search tree. <bookmark mark='d'/> Only three "
            "pointers change, and the depths shift: A moves up a level, C moves down. Balanced trees "
            "rotate to keep every path short."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), Create(e1))
            vo.wait_until("a")
            self.play(Indicate(left, color=HEAD, scale_factor=1.04), run_time=0.7)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(al))
            self.play(TransformFromCopy(left, right), Create(e2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pts[0]))
            vo.wait_until("d")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def avl(self):
        d = load("balanced")
        head = label(r"AVL trees \ (Adelson-Velsky and Landis, \ 1962)", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"rule: \ at every node, \ the two subtrees' heights differ by at most one", font_size=23,
                  color=GREY_A),
            label(r"after an insert, \ walk back up; \ one or two rotations restore the rule", font_size=22,
                  color=GREY_A),
            label(r"the thinnest AVL tree of height $h$: \ a \textbf{Fibonacci tree}", font_size=22, color=LAM),
            MathTex(r"N(h) = N(h-1) + N(h-2) + 1 = F_{h+2} - 1 \;\Rightarrow\; h < \frac{\lg(n+2)}{\lg\varphi}", font_size=32,
                    color=YES),
        ).arrange(DOWN, buff=0.26).next_to(head, DOWN, buff=0.45)
        fib = d["fib"]
        rows = [[str(r["h"]), words(r["min_nodes"])] for r in fib if r["h"] in (2, 4, 6, 8, 10, 15)]
        tab = grid_table([r"height (levels)", r"fewest nodes"], rows, widths=[1.6, 2.4], row_h=0.38, font_size=18).next_to(
            steps, DOWN, buff=0.35)
        with self.voiceover(
            "AVL trees enforce a local height rule. <bookmark mark='a'/> Every node's two subtree heights"
            " differ by at most one. <bookmark mark='b'/> After insertion, rotations restore that "
            "invariant while preserving key order. <bookmark mark='c'/> Count height in node levels: an "
            "empty tree has height zero and a leaf height one. The sparsest height-h tree has subtree "
            "heights h minus one and h minus two. <bookmark mark='d'/> Thus its minimum node count is "
            "Fibonacci h plus two, minus one. The exact logarithmic coefficient is one over log base two "
            "of the golden ratio; one point four four zero five is only a rounded guide. This gives "
            "logarithmic worst-case height, unlike a random-tree expectation."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def redblack(self):
        head = label(r"Red--black trees are 2--3--4 trees \ (Guibas and Sedgewick, \ 1978)", font_size=32).to_edge(
            UP, buff=0.3)
        # a 2-3-4 tree and its red-black encoding
        def knode(keys, col=DATA):
            w = 0.55 * len(keys) + 0.15
            r = RoundedRectangle(width=w, height=0.5, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            t = VGroup(*[mono(k, 20, WHITE) for k in keys]).arrange(RIGHT, buff=0.22).move_to(r)
            return VGroup(r, t)
        top = knode(["M"]).move_to(LEFT * 3.4 + UP * 1.1)
        l = knode(["D", "H"]).move_to(LEFT * 5.0 + DOWN * 0.2)
        r_ = knode(["Q", "T", "X"]).move_to(LEFT * 1.8 + DOWN * 0.2)
        e234 = VGroup(Line(top.get_bottom(), l.get_top(), color=GREY_B), Line(top.get_bottom(), r_.get_top(),
                                                                              color=GREY_B))
        cap1 = label(r"a 2--3--4 tree: \ every leaf at the same depth", font_size=19, color=GREY_B).next_to(
            VGroup(l, r_), DOWN, buff=0.4)

        def rb(k, red):
            return VGroup(Circle(radius=0.27, stroke_color=NO if red else GREY_A, stroke_width=2.4,
                                 fill_color=NO if red else BG, fill_opacity=0.35 if red else 1), mono(k, 20, WHITE))
        pos = {"M": [3.4, 1.4], "H": [2.0, 0.4], "D": [1.3, -0.6], "T": [4.8, 0.4], "Q": [4.1, -0.6],
               "X": [5.5, -0.6]}
        red = {"D", "Q", "X"}
        nodes = {k: rb(k, k in red).move_to([x, y - 0.1, 0]) for k, (x, y) in pos.items()}
        links = [("M", "H"), ("H", "D"), ("M", "T"), ("T", "Q"), ("T", "X")]
        erb = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.27,
                            color=NO if b in red else GREY_B, stroke_width=3 if b in red else 1.6) for a, b in links])
        cap2 = label(r"red links glue a node's keys together", font_size=19, color=GREY_B).next_to(
            VGroup(*nodes.values()), DOWN, buff=0.4)
        pts = VGroup(
            label(r"no two reds in a row; \ every path has the same number of blacks", font_size=22, color=GREY_A),
            label(r"so height $\le 2 \lg (n + 1)$; \ a split of a 4-node is a colour flip", font_size=22, color=YES),
            label(r"left-leaning red--black trees \ (Sedgewick, \ 2008): \ insert in a dozen lines", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The balanced tree in most standard libraries is the red–black tree, and it is easiest to "
            "understand as something else. <bookmark mark='a'/> A two–three–four tree lets a node hold "
            "one, two or three keys, and keeps every leaf at exactly the same depth: when a node "
            "overflows it splits and pushes a key up. Perfectly balanced, but awkward to code. <bookmark "
            "mark='b'/> Leonidas Guibas and Robert Sedgewick saw in 1978 that each big node can be drawn "
            "as a little binary tree, with its internal links coloured red. <bookmark mark='c'/> The "
            "rules follow: no two red links in a row, and the same number of black links on every path, "
            "because the black links are the two–three–four tree. <bookmark mark='d'/> So the height is "
            "at most twice log n, and splitting a node is just flipping colours. Java's TreeMap and C++'s"
            " std::map are red–black trees. <bookmark mark='e'/> Sedgewick's later left-leaning variant "
            "writes insertion in a dozen lines."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(l), FadeIn(r_), Create(e234), FadeIn(cap1))
            vo.wait_until("b")
            self.play(Create(erb), *[FadeIn(n) for n in nodes.values()], FadeIn(cap2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pts[0]))
            vo.wait_until("d")
            self.play(FadeIn(pts[1]))
            vo.wait_until("e")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("balanced")
        head = label(r"Heights in node levels, \ measured", font_size=34).to_edge(UP, buff=0.3)
        b = load("bst")
        rows = []
        for r in d["rows"]:
            bh = next((x["height"] + 1 for x in b["rows"] if x["n"] == r["n"]), None)
            rows.append([words(r["n"]), f"{r['lg']:.1f}", f"{bh:.0f}" if bh else "--", str(r["avl_random_h"]),
                         str(r["llrb_random_h"]), words(r["n"])])
        tab = grid_table([r"$n$", r"$\lg n$", r"plain BST, \ random", r"AVL", r"red--black", r"plain BST, \ sorted"],
                         rows, widths=[1.8, 1.4, 2.8, 1.4, 2.0, 2.8], row_h=0.5, font_size=20,
                         colors=[[WHITE, GREY_B, GREY_A, YES, LAM, NO]] * len(rows)).next_to(head, DOWN, buff=0.55)
        r = d["rows"][-1]
        pts = VGroup(
            label(rf"rotations per insert: \ AVL {r['avl_random_rot']:.2f}, \ red--black {r['llrb_random_rot']:.2f} "
                  r"\ (random keys)", font_size=21, color=GREY_A),
            label(r"heights/rotations are counters; \ layout and implementation determine elapsed "
                  r"time", font_size=21, color=GREY_A),
            label(r"ordinary dictionary operations: \ logarithmic height; \ reporting also pays output size", font_size=23, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "These are measured heights for seeded insertion orders. <bookmark mark='a'/> The "
            "balanced-tree heights count node levels, so subtract one to compare with an edge depth. "
            "Sorted insertion can make the plain tree linear while the balanced variants remain "
            "logarithmic. <bookmark mark='b'/> The displayed rotations are insertion counters for these "
            "implementations and workloads, not a deletion benchmark. <bookmark mark='c'/> A shorter "
            "height can reduce visited nodes, but elapsed lookup or update time also depends on layout, "
            "metadata, branches and the implementation. These counts alone do not prove which tree is "
            "faster. <bookmark mark='d'/> AVL and red-black invariants provide logarithmic-height "
            "guarantees for ordinary dictionary search, insert and delete with bounded-cost keys. "
            "Traversal and range reporting still pay for the output."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
