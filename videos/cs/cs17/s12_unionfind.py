from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


def forest_node(k, col=DATA):
    return VGroup(Circle(radius=0.26, stroke_color=col, stroke_width=2, fill_color=BG, fill_opacity=1),
                  mono(str(k), 18, WHITE))


class UnionFind(VoiceoverScene):
    def construct(self):
        self.card()
        self.forest()
        self.compression()
        self.measured()
        self.ackermann()

    def card(self):
        card = chapter_card(11, r"Union--find", r"How slowly can a function grow?", lit=(1975,),
                            extra=((1964, r"Galler and Fischer"), (1975, r"Tarjan: \ inverse Ackermann")), part=PART)
        with self.voiceover("Chapter eleven. Union–find."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def forest(self):
        head = label(r"Disjoint sets as a forest", font_size=34).to_edge(UP, buff=0.3)
        pos = {1: [-4.0, 1.2], 2: [-4.8, 0.0], 3: [-3.2, 0.0], 4: [-3.2, -1.2],
               5: [1.0, 1.2], 6: [0.2, 0.0], 7: [1.8, 0.0]}
        nodes = {k: forest_node(k).move_to([x, y, 0]) for k, (x, y) in pos.items()}
        par = {2: 1, 3: 1, 4: 3, 6: 5, 7: 5}
        edges = VGroup(*[Arrow(nodes[c].get_center(), nodes[p].get_center(), buff=0.28, stroke_width=2, color=GREY_B,
                               max_tip_length_to_length_ratio=0.2) for c, p in par.items()])
        pts = VGroup(
            label(r"each set is a tree; \ each node points to its parent; \ the root names the set", font_size=22,
                  color=GREY_A),
            label(r"\textbf{find}$(x)$: \ follow parents to the root", font_size=22, color=DATA),
            label(r"\textbf{union}$(x, y)$: \ make one root point to the other", font_size=22, color=LAM),
            label(r"\textbf{union by rank}: \ hang the shorter tree under the taller: \ height $\le \lg n$",
                  font_size=22, color=YES),
            label(r"uses: \ Kruskal's spanning trees \ (Part 18), \ type inference \ (Part 14), \ connected "
                  r"pixels, \ equivalent variables", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        newe = Arrow(nodes[5].get_center(), nodes[1].get_center(), buff=0.28, stroke_width=2.4, color=LAM,
                     max_tip_length_to_length_ratio=0.08)
        with self.voiceover(
            "Some problems need only to know which items belong together, and to merge groups. <bookmark "
            "mark='a'/> Bernard Galler and Michael Fischer's structure, from 1964, stores each group as a tree in "
            "which every node points to its parent; the root names the group. <bookmark mark='b'/> To find an "
            "item's group, follow parents to the root. <bookmark mark='c'/> To merge two groups, make one root "
            "point to the other. <bookmark mark='d'/> Done carelessly, trees become long paths. Union by rank hangs "
            "the shorter tree under the taller one, and a tree's height can only grow when two equal trees merge, "
            "so heights stay below log n. <bookmark mark='e'/> This structure finds spanning trees in Part 18, "
            "unifies types in the inference of Part 14, and labels connected regions in images."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(n) for n in nodes.values()], Create(edges))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
                if mk == "c":
                    self.play(GrowArrow(newe))
        self.wait(0.3)
        self.clear_scene()

    def compression(self):
        head = label(r"Path compression", font_size=34).to_edge(UP, buff=0.3)
        chain = [1, 2, 3, 4, 5]
        before = VGroup(*[forest_node(k, DATA if k != 5 else HEAD) for k in chain]).arrange(UP, buff=0.45).move_to(
            LEFT * 3.2 + DOWN * 0.2)
        eb = VGroup(*[Arrow(before[i].get_center(), before[i + 1].get_center(), buff=0.27, stroke_width=2,
                            color=GREY_B, max_tip_length_to_length_ratio=0.2) for i in range(4)])
        root = forest_node(5, HEAD).move_to(RIGHT * 3.0 + UP * 1.2)
        kids = VGroup(*[forest_node(k) for k in (1, 2, 3, 4)]).arrange(RIGHT, buff=0.45).move_to(RIGHT * 3.0 +
                                                                                                    DOWN * 0.4)
        ea = VGroup(*[Arrow(k.get_center(), root.get_center(), buff=0.27, stroke_width=2, color=YES,
                            max_tip_length_to_length_ratio=0.15) for k in kids])
        arrow = Arrow(LEFT * 1.4, RIGHT * 0.9, color=HEAD).move_to(DOWN * 0.2)
        al = label(r"find(1)", font_size=20, color=HEAD).next_to(arrow, UP, buff=0.1)
        pts = VGroup(
            label(r"after finding the root, \ point every node on the path straight at it", font_size=22,
                  color=GREY_A),
            label(r"later finds from any of them take one step", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The second idea costs one extra pass. <bookmark mark='a'/> After a find walks up to the root, walk the "
            "path again and point every node on it directly at the root. <bookmark mark='b'/> The path flattens, "
            "and every later find from those nodes takes a single step. The work of one slow find is an investment "
            "that makes all its successors fast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before), Create(eb))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(pts[0]))
            self.play(FadeIn(root), FadeIn(kids), Create(ea), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("unionfind")
        head = label(rf"{words(d['n'])} elements, \ {words(2 * d['n'])} random unions, \ then finds",
                     font_size=32).to_edge(UP, buff=0.3)
        names = {"neither": r"neither", "rank": r"union by rank", "compression": r"path compression",
                 "both": r"both"}
        rows = [[names[r["name"]], f"{r['per_find']:,.2f}", words(r["max_depth"])] for r in d["rows"]]
        tab = grid_table([r"", r"parent steps per find", r"deepest node"], rows, widths=[4.0, 3.6, 2.6], row_h=0.55,
                         font_size=22, mono_cols=(),
                         colors=[[NO, NO, NO], [GREY_A, YES, YES], [GREY_A, YES, YES], [HEAD, HEAD, HEAD]]).next_to(
            head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"each idea alone turns thousands of steps into a few", font_size=22, color=GREY_A),
            label(r"together: \ $O(m\,\alpha(n))$ for $m$ operations \ (Tarjan, \ 1975), \ and that is optimal "
                  r"\ (Fredman and Saks, \ 1989)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "How much do the two ideas buy? <bookmark mark='a'/> With twenty thousand elements and forty thousand "
            "random unions, the careless version builds trees thousands deep, and an average find walks over two "
            "thousand parent pointers. Union by rank alone brings that down to about two. Path compression alone, "
            "to under one and a half. Both together, to one. <bookmark mark='b'/> Robert Tarjan proved in 1975 "
            "that with both, any m operations take m times alpha of n, where alpha is the inverse of Ackermann's "
            "function, and Michael Fredman and Michael Saks later proved that no structure can do better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def ackermann(self):
        head = label(r"How slowly does $\alpha(n)$ grow?", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"A(0, n) = n + 1, \quad A(m, 0) = A(m-1, 1), \quad A(m, n) = A\bigl(m-1, A(m, n-1)\bigr)",
                    font_size=30),
            MathTex(r"A(1,1) = 3,\ \ A(2,1) = 5,\ \ A(3,1) = 13,\ \ A(4,1) = 2^{16} - 3 = 65{,}533", font_size=30,
                    color=GREY_A),
            MathTex(r"A(4,2) = 2^{65536} - 3", font_size=30, color=NO),
            MathTex(r"\alpha(n) = \min\{m : A(m, m) \ge n\} \le 4 \text{ for every } n \text{ that fits in our "
                    r"universe}", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        ls = load("unionfind")["logstar"]
        tab = grid_table([r"$n$"] + [r["n"].replace("2^65536", r"$2^{65536}$") for r in ls],
                         [[r"$\log^* n$"] + [str(r["log*"]) for r in ls]], widths=[1.6, 1.0, 1.0, 1.0, 1.6, 1.8],
                         row_h=0.5, font_size=20, mono_cols=()).next_to(defs, DOWN, buff=0.45)
        note_ = label(r"$\log^*$ counts how often you take $\lg$ to reach 1: \ the simpler $O(m \log^* n)$ bound "
                      r"\ (Hopcroft and Ullman, \ 1973)", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Ackermann's function is the classic example of a computable function that grows faster than any "
            "primitive recursive one. <bookmark mark='a'/> It is defined by three short rules. <bookmark mark='b'/> "
            "A of one, one is three; A of two, one is five; A of three, one is thirteen; A of four, one is sixty-five "
            "thousand. <bookmark mark='c'/> A of four, two is two to the sixty-five thousand five hundred and "
            "thirty-six, minus three, a number with nearly twenty thousand digits. <bookmark mark='d'/> Its inverse, "
            "alpha, is therefore at most four for any input that could exist in the physical universe. Union–find "
            "is linear time in every practical sense, and yet, provably, not quite linear. <bookmark mark='e'/> An "
            "easier bound, from John Hopcroft and Jeffrey Ullman, uses the iterated logarithm, which is at most five "
            "for any n you will meet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", defs):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
