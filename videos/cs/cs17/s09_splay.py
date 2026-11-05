from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, grid_table,
                                   load, mono, words)


class Splay(VoiceoverScene):
    def construct(self):
        self.card()
        self.steps()
        self.potential()
        self.sequences()

    def card(self):
        card = chapter_card(8, r"Splay trees", r"Can a tree learn what you look up?", lit=(1985,),
                            extra=((1985, r"Sleator and Tarjan"),), part=PART)
        with self.voiceover("Chapter eight. Splay trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def steps(self):
        head = label(r"Splaying: \ rotate the accessed node to the root", font_size=34).to_edge(UP, buff=0.3)

        def tree(pos, edges, hi):
            nodes = {k: VGroup(Circle(radius=0.26, stroke_color=HEAD if k == hi else DATA, stroke_width=2.2,
                                      fill_color=BG, fill_opacity=1), mono(str(k), 18, WHITE)).move_to([x, y, 0])
                     for k, (x, y) in pos.items()}
            lines = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.26, color=GREY_B,
                                  stroke_width=1.6) for a, b in edges])
            return VGroup(lines, *nodes.values())
        before = tree({5: [0, 1.6], 4: [-0.6, 0.85], 3: [-1.2, 0.1], 2: [-1.8, -0.65], 1: [-2.4, -1.4]},
                      ((5, 4), (4, 3), (3, 2), (2, 1)), 1).move_to(RIGHT * 1.2 + UP * 0.3)
        after = tree({5: [1.7, 0.1], 4: [1.0, 0.85], 3: [1.0, -0.65], 2: [0.4, 0.1], 1: [0, 1.6]},
                     ((1, 4), (4, 2), (2, 3), (4, 5)), 1).move_to(RIGHT * 4.8 + UP * 0.3)
        arr = Arrow(before.get_right() + RIGHT * 0.1, after.get_left() + LEFT * 0.1, color=HEAD, buff=0.1)
        al = label(r"splay(1): \ two zig-zigs", font_size=18, color=HEAD).next_to(arr, UP, buff=0.08)
        dl = label(r"depth 4 \ $\to$ \ the path's nodes now at depth $\le 3$", font_size=17, color=GREY_B).next_to(
            VGroup(before, after), DOWN, buff=0.3)
        cases = VGroup(
            VGroup(label(r"\textbf{zig}: \ $x$'s parent is the root", font_size=20, color=DATA),
                   label(r"one rotation", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(label(r"\textbf{zig-zig}: \ $x$ and its parent \ both left \ (or right) children", font_size=20,
                         color=LAM),
                   label(r"rotate the grandparent first, \ then the parent", font_size=18, color=GREY_B)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06),
            VGroup(label(r"\textbf{zig-zag}: \ $x$ is a right child of a left child", font_size=20, color=CTRL),
                   label(r"rotate $x$ up twice", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.06),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.6)
        if cases.width > 4.6:
            cases.scale_to_fit_width(4.6).to_edge(LEFT, buff=0.6)
        side = VGroup(
            label(r"no balance information at all: \ no heights, \ no colours; \ a single access can cost $O(n)$",
                  font_size=21, color=GREY_A),
            label(r"but zig-zig roughly halves the depth of every node on the path", font_size=21, color=YES),
            label(r"so any $m$ accesses cost $O(m \log n)$ in all: \ \textbf{amortized} $O(\log n)$", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Daniel Sleator and Robert Tarjan's splay tree, from 1985, keeps no balance information at all. "
            "<bookmark mark='a'/> Instead, every time a node is accessed, it is rotated all the way to the root, "
            "in steps of three kinds. Zig, when its parent is the root: one rotation. <bookmark mark='b'/> Zig-zig, "
            "when the node and its parent are both left children, or both right: rotate the grandparent first, "
            "then the parent. <bookmark mark='c'/> Zig-zag, when they bend: rotate the node up twice. <bookmark "
            "mark='d'/> There are no heights or colours to maintain. A single access can be slow, if the node is "
            "deep. <bookmark mark='e'/> But the zig-zig step, the one difference from simply rotating to the top, "
            "roughly halves the depth of every node on the access path. <bookmark mark='f'/> The result is that "
            "any sequence of m accesses costs at most order m log n in total: logarithmic amortized time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before))
            vo.wait_until("a")
            self.play(FadeIn(cases[0]))
            vo.wait_until("b")
            self.play(FadeIn(cases[1]))
            vo.wait_until("c")
            self.play(FadeIn(cases[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            vo.wait_until("e")
            self.play(GrowArrow(arr), FadeIn(al), TransformFromCopy(before, after), run_time=1.5)
            self.play(FadeIn(dl), FadeIn(side[1]))
            vo.wait_until("f")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def potential(self):
        head = label(r"The access lemma, \ by potential", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"give each node a weight $w$, \ and let $s(x)$ be the total weight of $x$'s subtree", font_size=22,
                  color=GREY_A),
            MathTex(r"\Phi = \sum_x \log_2 s(x)", font_size=36, color=LAM),
            label(r"each splay step costs at most $3\bigl(r'(x) - r(x)\bigr)$ in amortized time, \ "
                  r"where $r = \log_2 s$", font_size=22, color=GREY_A),
            MathTex(r"\text{amortized cost of an access} \le 3\bigl(r(\text{root}) - r(x)\bigr) + 1 "
                    r"= O\Bigl(\log \frac{W}{w(x)}\Bigr)", font_size=32, color=YES),
            label(r"all weights 1: \ $O(\log n)$; \ $w(x)$ = how often $x$ is accessed: \ the entropy, \ "
                  r"\textbf{static optimality}", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The proof is Part 16's potential method, with a clever potential. <bookmark mark='a'/> Give each node "
            "a weight, and let s of x be the total weight in x's subtree. <bookmark mark='b'/> The potential is the "
            "sum, over all nodes, of the logarithm of s. A tall, unbalanced tree has high potential: it has stored "
            "up credit. <bookmark mark='c'/> A case analysis of the three steps shows that each costs at most three "
            "times the increase in the rank of x, where rank is the log of s. <bookmark mark='d'/> The steps "
            "telescope: a whole access costs at most three times the rank difference between the root and x, plus "
            "one. That is the log of the total weight over x's weight. <bookmark mark='e'/> With all weights one, "
            "it is log n. But the weights are only in the proof, not in the code, so we may choose them after the "
            "fact. Choose each node's weight to be how often it is accessed, and the bound becomes the entropy "
            "of the access sequence: a splay tree is as good as the best static tree for that sequence, without "
            "knowing the frequencies."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def sequences(self):
        d = load("splay")
        head = label(rf"Splay against a balanced tree, \ {words(d['n'])} keys", font_size=34).to_edge(UP, buff=0.3)
        names = {"sequential": r"in order, \ five times", "uniform": r"uniform random",
                 "zipf": r"skewed \ (Zipf)", "hot ten": r"ten hot keys"}
        rows = []
        for k, v in d["seqs"].items():
            rows.append([names[k], f"{v['splay']:.2f}", f"{v['balanced']:.2f}", f"{v['entropy']:.2f}"])
        tab = grid_table([r"access sequence", r"splay: \ cost per access", r"AVL: \ depth", r"entropy (bits)"], rows,
                         widths=[3.6, 3.2, 2.4, 2.6], row_h=0.55, font_size=21, mono_cols=(),
                         colors=[[WHITE, YES, GREY_A, HEAD], [WHITE, NO, GREY_A, HEAD], [WHITE, YES, GREY_A, HEAD],
                                 [WHITE, YES, GREY_A, HEAD]]).next_to(head, DOWN, buff=0.55)
        pts = VGroup(
            label(r"in order: \ constant per access \ (the sequential access theorem)", font_size=21, color=YES),
            label(r"uniform: \ a constant factor slower than a balanced tree, \ the price of adapting", font_size=21,
                  color=NO),
            label(r"skewed or local: \ close to the entropy, \ far below $\lg n$", font_size=21, color=YES),
            label(r"\textbf{dynamic optimality} \ (Sleator and Tarjan, \ 1985): \ is a splay tree within a constant "
                  r"of \textit{every} BST algorithm? \ Open.", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Here is a splay tree against an AVL tree on four access sequences. <bookmark mark='a'/> Accessing "
            "every key in order costs a constant per access in the splay tree, under five, against ten for the "
            "balanced tree. <bookmark mark='b'/> Uniformly random accesses are the splay tree's worst case: it "
            "keeps reorganising for nothing, and pays about forty percent more. <bookmark mark='c'/> But on skewed "
            "or local sequences, where a few keys are popular, the splay tree's cost falls to near the entropy, "
            "a few comparisons per access, far below log n. <bookmark mark='d'/> Sleator and Tarjan conjectured "
            "more: that splay trees are within a constant factor of the best possible binary search tree "
            "algorithm for every access sequence, even one that knows the future. Forty years later, that "
            "dynamic optimality conjecture is still open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            self.play(FadeIn(pts[0]))
            for mk, p in zip("bcd", pts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()
