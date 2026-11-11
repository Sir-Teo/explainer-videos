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
            label(r"\textbf{union by rank}: \ link smaller rank under larger; \ rank bounds height after compression",
                  font_size=22, color=YES),
            label(r"uses: \ Kruskal's spanning trees \ (Part 18), \ type inference \ (Part 14), \ connected "
                  r"pixels, \ equivalent variables", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        newe = Arrow(nodes[5].get_center(), nodes[1].get_center(), buff=0.28, stroke_width=2.4, color=LAM,
                     max_tip_length_to_length_ratio=0.08)
        with self.voiceover(
            "Disjoint-set union tracks which items belong together. <bookmark mark='a'/> Each set is a "
            "parent-pointer tree, with the root as representative. <bookmark mark='b'/> Find follows "
            "parents to the root. <bookmark mark='c'/> Union links two distinct roots. <bookmark "
            "mark='d'/> Union by rank attaches the smaller rank under the larger and increments rank only"
            " when equal ranks merge. Without compression rank equals height; after compression it is an "
            "upper bound, not necessarily the current height. A rank-r root represents at least two to "
            "the r elements. <bookmark mark='e'/> Applications include Kruskal's spanning trees and "
            "equivalence classes; richer type unification needs additional structure."
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
            label(r"one upward edge from these nonroots, \ until a union moves the root", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Path compression makes an extra pass. <bookmark mark='a'/> After following parents to the "
            "root, point every visited node directly at that root. <bookmark mark='b'/> While the root "
            "stays the same, another find from those nonroot nodes traverses one edge. Later unions can "
            "move the root and add work again. Compression helps a sequence of operations; it does not "
            "promise every future find costs one step."
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
        tab = grid_table([r"", r"upward edges per find", r"deepest node"], rows, widths=[4.0, 3.6, 2.6], row_h=0.55,
                         font_size=22, mono_cols=(),
                         colors=[[NO, NO, NO], [GREY_A, YES, YES], [GREY_A, YES, YES], [HEAD, HEAD, HEAD]]).next_to(
            head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"counts upward discovery edges only; \ excludes compression pass and writes", font_size=22, color=GREY_A),
            label(r"together: \ amortized inverse-Ackermann bound with setup/model conventions "
                  r"\ (Fredman and Saks, \ 1989)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Here is one seeded sequence: forty thousand random unions, followed by forty thousand finds "
            "on twenty thousand elements. <bookmark mark='a'/> The table counts upward parent edges "
            "during those finds. It excludes the second compression pass, stores, and the earlier unions."
            " Both heuristics dramatically reduce that particular counter. <bookmark mark='b'/> With "
            "initialization and the usual operation-count conventions, union by rank plus compression has"
            " an amortized inverse-Ackermann bound. Matching lower bounds are model-dependent sequence "
            "results, not a claim that every individual operation must take that long on every input."
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
            MathTex(r"\alpha_{\rm demo}(n) = \min\{m : A(m, m) \ge n\},\quad \alpha_{\rm demo}(n)\le4\text{ for practical }n"
                    r"", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        ls = load("unionfind")["logstar"]
        tab = grid_table([r"$n$"] + [r["n"].replace("2^65536", r"$2^{65536}$") for r in ls],
                         [[r"$\log^* n$"] + [str(r["log*"]) for r in ls]], widths=[1.6, 1.0, 1.0, 1.0, 1.6, 1.8],
                         row_h=0.5, font_size=20, mono_cols=()).next_to(defs, DOWN, buff=0.45)
        note_ = label(r"$\log^*$ counts how often you take $\lg$ to reach 1: \ the simpler $O(m \log^* n)$ bound "
                      r"\ (Hopcroft and Ullman, \ 1973)", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Ackermann growth gives a useful scale comparison. <bookmark mark='a'/> Use exactly the "
            "displayed recurrence; different texts define variants. <bookmark mark='b'/> Its small values"
            " already jump from three to five to thirteen to sixty-five thousand five hundred and "
            "thirty-three. <bookmark mark='c'/> The next displayed value is two to sixty-five thousand "
            "five hundred and thirty-six, minus three. <bookmark mark='d'/> The displayed inverse is one "
            "illustrative diagonal convention. Formal union-find bounds may use a two-parameter inverse "
            "and setup terms; those conventions differ by small constants, not by practical growth. A "
            "worst-case sequence lower bound does not make every operation superconstant. <bookmark "
            "mark='e'/> The iterated logarithm is a simpler comparison: the table counts base-two "
            "logarithms needed to reach one. Neither this tiny table nor a finite timing experiment "
            "proves the asymptotic theorem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", defs):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            vo.wait_until("e")
            self.play(FadeIn(tab), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
