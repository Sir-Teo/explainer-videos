from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def bnode(keys, col=DATA, kw=0.5):
    w = kw * len(keys) + 0.2
    r = RoundedRectangle(width=w, height=0.5, corner_radius=0.08, stroke_color=col, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    t = VGroup(*[mono(str(k), 17, WHITE) for k in keys]).arrange(RIGHT, buff=0.18).move_to(r)
    return VGroup(r, t)


class Btree(VoiceoverScene):
    def construct(self):
        self.card()
        self.shape()
        self.split()
        self.height()

    def card(self):
        card = chapter_card(9, r"B-trees", r"What if each step costs a disk read?", lit=(1970,),
                            extra=((1970, r"Bayer and McCreight"),), part=PART)
        with self.voiceover("Chapter nine. B-trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shape(self):
        head = label(r"Wide nodes, \ short paths", font_size=34).to_edge(UP, buff=0.3)
        root = bnode([20, 40, 60]).move_to(UP * 1.6)
        kids = VGroup(bnode([5, 9, 14]), bnode([24, 31, 37]), bnode([44, 50, 55]), bnode([65, 72, 80, 91])).arrange(
            RIGHT, buff=0.5).move_to(UP * 0.1)
        edges = VGroup(*[Line(root.get_bottom() + RIGHT * (i - 1.5) * 0.45, k.get_top(), color=GREY_B,
                              stroke_width=1.6) for i, k in enumerate(kids)])
        pts = VGroup(
            label(r"a node holds up to $2t - 1$ keys and $2t$ children \ (all but the root at least half full)",
                  font_size=22, color=GREY_A),
            label(r"all leaves at the same depth: \ height $\le \log_t \frac{n+1}{2}$", font_size=22, color=YES),
            label(r"chosen so that a node fills a disk block \ (4 KB): \ one read per level", font_size=22,
                  color=HEAD),
            label(r"the external-memory model of Part 16: \ count block transfers, \ not comparisons", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Binary trees assume that following a pointer is cheap. On a disk, every node visited is a read that "
            "takes thousands of times longer than a comparison. <bookmark mark='a'/> Rudolf Bayer and Edward "
            "McCreight's B-tree, from 1970, makes the nodes wide. A node holds many keys in sorted order, and has "
            "one child between each pair. Every node except the root is at least half full. <bookmark mark='b'/> "
            "All leaves are at the same depth, so the height is the logarithm of n to the base of the fan-out. "
            "<bookmark mark='c'/> The fan-out is chosen so that a node fills a disk block, and a search reads one "
            "block per level. <bookmark mark='d'/> This is the external-memory model from Part 16: what matters is "
            "the number of block transfers, and comparisons inside a block are nearly free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), Create(edges), FadeIn(kids))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def split(self):
        head = label(r"Growing at the root", font_size=34).to_edge(UP, buff=0.3)
        full = bnode([10, 20, 30, 40, 50], col=NO).move_to(UP * 1.4)
        new = mono("+ 35", 22, HEAD).next_to(full, RIGHT, buff=0.4)
        top = bnode([30], col=DATA).move_to(UP * 1.4)
        l = bnode([10, 20]).move_to(LEFT * 1.6 + DOWN * 0.1)
        r = bnode([35, 40, 50]).move_to(RIGHT * 1.6 + DOWN * 0.1)
        e = VGroup(Line(top.get_bottom(), l.get_top(), color=GREY_B), Line(top.get_bottom(), r.get_top(),
                                                                          color=GREY_B))
        pts = VGroup(
            label(r"a full node splits in two, \ and its middle key moves up to the parent", font_size=22,
                  color=GREY_A),
            label(r"the tree grows at the top, \ never at the bottom: \ that is why every leaf stays at one depth",
                  font_size=22, color=YES),
            label(r"a 2--3--4 tree is the B-tree with $t = 2$: \ chapter 6's red--black trees again", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How does a B-tree stay perfectly balanced? <bookmark mark='a'/> When a node is full and another key "
            "arrives, the node splits into two half-full nodes, and its middle key moves up into the parent. "
            "<bookmark mark='b'/> If the parent overflows it splits too, and if the root splits, a new root "
            "appears above it. The tree grows at the top, never at the bottom, which is why every leaf is at the "
            "same depth. <bookmark mark='c'/> With at most three keys per node, this is exactly the two–three–four "
            "tree that red–black trees encode."
        ) as vo:
            self.play(FadeIn(head), FadeIn(full), FadeIn(new))
            vo.wait_until("a")
            self.play(FadeOut(full), FadeOut(new), run_time=0.6)
            self.play(FadeIn(top, shift=UP * 0.2), FadeIn(l), FadeIn(r), Create(e), run_time=1.2)
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def height(self):
        d = load("btree")
        head = label(rf"{words(d['n'])} keys, \ measured", font_size=34).to_edge(UP, buff=0.3)
        rows = [[str(r["t"]), str(2 * r["t"] - 1), str(r["height"]), words(r["nodes"])] for r in d["rows"]]
        tab = grid_table([r"$t$", r"keys per node, \ at most", r"height", r"nodes"], rows,
                         widths=[1.4, 3.4, 1.8, 2.4], row_h=0.48, font_size=20).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(rf"a billion keys, \ 4 KB blocks of 8-byte keys and pointers: \ fan-out {d['disk_fan']}, \ "
                  rf"height {d['disk_height']}", font_size=22, color=YES),
            label(rf"a balanced binary tree would need {d['bst_height']} levels: \ {d['bst_height']} disk reads per "
                  r"lookup instead of 1 or 2 \ (the top levels stay cached)", font_size=21, color=GREY_A),
            label(r"every relational database and most file systems index with B+-trees: \ Part 35", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here are B-trees of two hundred thousand keys with different node sizes. <bookmark mark='a'/> As the "
            "nodes widen, the height falls from fourteen to three. <bookmark mark='b'/> On a real disk, with four "
            "kilobyte blocks and eight-byte keys and pointers, a node has two hundred and fifty-six children, and a "
            "billion keys fit in a tree of height four. A balanced binary tree would need thirty levels. Since the "
            "top levels stay in memory, a B-tree lookup costs one or two disk reads. <bookmark mark='c'/> That is "
            "why every relational database and most file systems are built on a variant, the B-plus tree, as Part "
            "35 will show."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for mk, p in zip("bc", (pts[:2], pts[2])):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
